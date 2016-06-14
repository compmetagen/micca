import sys
import os
import stat
import shutil
import glob
import tarfile
import subprocess
from setuptools import setup, find_packages
from setuptools.command.sdist import sdist

from micca import __version__, THIRDPARTY_BIN_PATH
# THIRDPARTY_BIN_PATH is an absolute path but can be relative during building
# (e.g. bdist_wheel). Therefore, in the setup.py it is treated as a relative
# path.

_THIRDPARTY_SRC = "thirdparty"
_THIRDPARTY_TEMP = os.path.join(_THIRDPARTY_SRC, "temp")

_classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: C',
    'Programming Language :: C++',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Environment :: Console',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: Linux']

def _print_status(msg):
    sys.stdout.write(msg+'\n')
    sys.stdout.flush()

def _untar(name, dest):
    tar = tarfile.open(name)
    tar.extractall(dest)
    tar.close()

def _system_call(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc_stdout, proc_stderr = proc.communicate()
    if proc.returncode:
        sys.stderr.write(proc_stderr)
        exit(1)

def _build_vsearch():
    _print_status("Building VSEARCH...")
    cwd = os.getcwd()
    tar_fn = glob.glob(os.path.join(_THIRDPARTY_SRC, "vsearch*.tar.gz"))[0]
    _untar(tar_fn, _THIRDPARTY_TEMP)
    tar_dir = glob.glob(os.path.join(_THIRDPARTY_TEMP, "vsearch*/"))[0]
    os.chdir(tar_dir)
    _system_call(["./configure", "--disable-zlib", "--disable-bzip2",
                  "--disable-pdfman"])
    _system_call(["make"])
    os.chmod("bin/vsearch", os.stat("bin/vsearch").st_mode | stat.S_IEXEC)
    os.chdir(cwd)
    shutil.copy(os.path.join(tar_dir, "bin/vsearch"), THIRDPARTY_BIN_PATH)

def _build_muscle():
    _print_status("Building MUSCLE...")
    cwd = os.getcwd()
    tar_fn = glob.glob(os.path.join(_THIRDPARTY_SRC, "muscle*.tar.gz"))[0]
    _untar(tar_fn, _THIRDPARTY_TEMP)
    tar_dir = glob.glob(os.path.join(_THIRDPARTY_TEMP, "muscle*/src/"))[0]
    os.chdir(tar_dir)
    _system_call(["sed", "-i.bak", "/echo/d", "mk"])
    os.chmod("mk", os.stat("mk").st_mode | stat.S_IEXEC)
    _system_call(["make"])
    os.chmod("muscle", os.stat("muscle").st_mode | stat.S_IEXEC)
    os.chdir(cwd)
    shutil.copy(os.path.join(tar_dir, "muscle"), THIRDPARTY_BIN_PATH)

def _build_fasttree():
    _print_status("Building FastTree...")
    cwd = os.getcwd()
    shutil.copy(os.path.join(_THIRDPARTY_SRC, "FastTree.c"), _THIRDPARTY_TEMP)
    os.chdir(_THIRDPARTY_TEMP)
    _system_call(["gcc", "-O3", "-finline-functions", "-funroll-loops",
                  "-o", "fasttree", "FastTree.c", "-lm"])
    os.chmod("fasttree", os.stat("fasttree").st_mode | stat.S_IEXEC)
    os.chdir(cwd)
    shutil.copy(os.path.join(_THIRDPARTY_TEMP, "fasttree"), THIRDPARTY_BIN_PATH)

def _build_swarm():
    _print_status("Building swarm...")
    cwd = os.getcwd()
    tar_fn = glob.glob(os.path.join(_THIRDPARTY_SRC, "swarm*.tar.gz"))[0]
    _untar(tar_fn, _THIRDPARTY_TEMP)
    tar_dir = glob.glob(os.path.join(_THIRDPARTY_TEMP, "swarm*/src/"))[0]
    os.chdir(tar_dir)
    _system_call(["make"])
    os.chmod("swarm", os.stat("swarm").st_mode | stat.S_IEXEC)
    os.chdir(cwd)
    shutil.copy(os.path.join(tar_dir, "swarm"), THIRDPARTY_BIN_PATH)

class _sdist(sdist):
    """ Make sure third-party binaries will be removed before running sdist.
    """
    def run(self):
        try:
            os.remove(os.path.join(THIRDPARTY_BIN_PATH, "vsearch"))
            os.remove(os.path.join(THIRDPARTY_BIN_PATH, "muscle"))
            os.remove(os.path.join(THIRDPARTY_BIN_PATH, "fasttree"))
            os.remove(os.path.join(THIRDPARTY_BIN_PATH, "swarm"))
        except OSError:
            pass

        sdist.run(self)

if all([cmd not in sys.argv for cmd in ['sdist', 'egg_info', 'register']]):
    try:
        os.mkdir(_THIRDPARTY_TEMP)
    except OSError:
        pass

    _build_vsearch()
    _build_muscle()
    _build_fasttree()
    _build_swarm()

    shutil.rmtree(_THIRDPARTY_TEMP)

setup(
    name='micca',
    version = __version__,
    description='micca - MICrobial Community Analysis',
    long_description=open('README.rst').read(),
    url='http://www.micca.org',
    download_url='http://www.micca.org',
    license='GPLv3',
    author='Davide Albanese',
    author_email='davide.albanese@fmach.it',
    maintainer='Davide Albanese',
    maintainer_email='davide.albanese@fmach.it',
    install_requires=[
        'numpy >= 1.8.0',
        'scipy >=0.14.0',
        'matplotlib >= 1.3.0',
        'pandas >= 0.17.0',
        'biopython >= 1.50',
        'cutadapt >= 1.9',
        'biom-format >= 1.3.1'],
    scripts = ["scripts/micca"],
    use_2to3 = True,
    packages = find_packages(),
    include_package_data = True,
    classifiers=_classifiers,
    cmdclass={
        'sdist': _sdist,
    },
)
