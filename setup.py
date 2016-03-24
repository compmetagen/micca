import ez_setup
ez_setup.use_setuptools()

import sys
import imp
import os
import stat
import shutil
import glob
import tarfile
import subprocess
from setuptools import setup, Extension, find_packages
from setuptools.command import easy_install
from setuptools.command.install import install

from micca import __version__, THIRDPARTY_BIN_PATH


thirdparty_src = "thirdparty"
thirdparty_temp = os.path.join(thirdparty_src, "temp")

def print_status(msg):
    sys.stdout.write(msg+'\n')
    sys.stdout.flush()

def untar(name, dest):
    tar = tarfile.open(name)
    tar.extractall(dest)
    tar.close()
    
def system_call(cmd):
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc_stdout, proc_stderr = proc.communicate()
    if proc.returncode:
        sys.stderr.write(proc_stderr)
        exit(1)

def build_vsearch():
    print_status("Building VSEARCH...")
    cwd = os.getcwd()
    tar_fn = glob.glob(os.path.join(thirdparty_src, "vsearch*.tar.gz"))[0]
    untar(tar_fn, thirdparty_temp)
    tar_dir = glob.glob(os.path.join(thirdparty_temp, "vsearch*/"))[0]
    os.chdir(tar_dir)
    system_call(["./configure", "--disable-zlib", "--disable-bzip2", 
                 "--disable-pdfman"])
    system_call(["make"])
    os.chmod("bin/vsearch", os.stat("bin/vsearch").st_mode | stat.S_IEXEC)
    shutil.copy("bin/vsearch", os.path.join(cwd, THIRDPARTY_BIN_PATH))
    os.chdir(cwd)

def build_muscle():
    print_status("Building MUSCLE...")
    cwd = os.getcwd()
    tar_fn = glob.glob(os.path.join(thirdparty_src, "muscle*.tar.gz"))[0]
    untar(tar_fn, thirdparty_temp)
    tar_dir = glob.glob(os.path.join(thirdparty_temp, "muscle*/src/"))[0]
    os.chdir(tar_dir)
    system_call(["sed", "-i.bak", "/echo/d", "mk"])
    os.chmod("mk", os.stat("mk").st_mode | stat.S_IEXEC)
    system_call(["make"])
    os.chmod("muscle", os.stat("muscle").st_mode | stat.S_IEXEC)
    shutil.copy("muscle", os.path.join(cwd, THIRDPARTY_BIN_PATH))
    os.chdir(cwd)

def build_fasttree():
    print_status("Building FastTree...")
    cwd = os.getcwd()
    shutil.copy(os.path.join(thirdparty_src, "FastTree.c"), thirdparty_temp)
    os.chdir(thirdparty_temp)
    system_call(["gcc", "-O3", "-finline-functions", "-funroll-loops", 
                 "-o", "fasttree", "FastTree.c", "-lm"])
    os.chmod("fasttree", os.stat("fasttree").st_mode | stat.S_IEXEC)
    shutil.copy("fasttree", os.path.join(cwd, THIRDPARTY_BIN_PATH))
    os.chdir(cwd)
    
    
class custom_install(install):
    def run(self):
        try:
            os.mkdir(thirdparty_temp)
        except OSError:
            pass
        
        try:
            os.mkdir(THIRDPARTY_BIN_PATH)
        except OSError:
            pass
            
        build_muscle()
        build_vsearch()
        build_fasttree()

        shutil.rmtree(thirdparty_temp)
        install.run(self)
        shutil.rmtree(THIRDPARTY_BIN_PATH)

        

ext_modules = []

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
]

setup(
    name='micca',
    version = __version__,
    description='micca - MICrobial Community Analysis',
    long_description=open('README.rst').read(),
    url='www.micca.org',
    download_url='',
    license='GPLv3',
    author='Davide Albanese',
    author_email='davide.albanese@fmach.it',
    maintainer='Davide Albanese',
    maintainer_email='davide.albanese@fmach.it',
    install_requires=[
        'numpy >= 1.8.0',
        'scipy >=0.14.0',
        'pandas >= 0.17.0, <0.18.0',
        'matplotlib >= 1.3.0',
        'biopython >= 1.50',
        'cutadapt >= 1.9',
        'biom-format >= 1.3.1',
        ],
    scripts = ["scripts/micca"],
    use_2to3 = True,
    packages = find_packages(),
    include_package_data = True,
    cmdclass={
        'install': custom_install,
    },
    classifiers=classifiers,
    ext_modules=ext_modules
)
