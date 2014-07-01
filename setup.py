import sys
import glob

from distutils.core import setup, Extension
from distutils.util import *
from distutils.spawn import find_executable

import numpy

from micca import __version__

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py


# extension module arguments
if get_platform() == "win32":
   libraries = []
else:
   libraries = ['m']
extra_compile_args = ['-Wall']
extra_link_args = []
include_dirs = [numpy.get_include(), "clust/uthash"]
ext_modules = [
    Extension("otuclust",
              ["otuclust/core_otuclust.c", "otuclust/otuclust.c"],
              libraries=libraries,
              include_dirs=include_dirs,
              extra_compile_args=extra_compile_args)
    ]


# setup arguments
packages = ['micca']
scripts = [
    "scripts/micca-preproc",
    "scripts/micca-preproc-check",
    "scripts/micca-otu-denovo",
    "scripts/micca-otu-ref",
    "scripts/micca-phylogeny",
    "scripts/micca-midpoint-root",
    "scripts/micca-rarefy",
    "scripts/micca-rarefy-seqs",
    "scripts/micca-filter",
    "scripts/micca-levels",
    "scripts/micca-sff2fastq",
    "scripts/micca-plot-rank",
    "scripts/micca-plot-abundance",
    "otuclust/scripts/otuclust"
]

data_files = []
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
]

setup(name='micca',
      version=__version__,
      description='',
      long_description=open('README.md').read(),
      author='Davide Albanese',
      author_email='davide.albanese@fmach.it',
      maintainer='Davide Albanese',
      maintainer_email='davide.albanese@fmach.it',
      url='',
      download_url='',
      license='GPLv3',
      packages=packages,
      scripts=scripts,
      data_files=data_files,
      classifiers=classifiers,
      ext_modules=ext_modules
)

# Check dependencies

HEADER = '\033[95m'
OK = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def find_module(name, module):
    sys.stdout.write("%s... " % name)
    try:
        __import__(module)
    except ImportError, e:
        sys.stdout.write("%snot installed%s\n" % (FAIL, ENDC))
    else:
        sys.stdout.write("%sOK%s\n" % (OK, ENDC))

def find_exe(name, exe):
    sys.stdout.write("%s... " % name)

    if find_executable(exe):
        sys.stdout.write("%sOK%s\n" % (OK, ENDC))
    else:
        sys.stdout.write("%snot installed%s\n" % (FAIL, ENDC))

def find_rdp():
    sys.stdout.write("RDP Classifier... ")
    rdppath = os.getenv("RDPPATH")
    if rdppath is None:
        sys.stdout.write("%sRDPPATH environment variable is not set%s\n" \
                         % (FAIL, ENDC))
        return

    rdpjar_list = glob.glob(os.path.join(rdppath, "rdp_classifier*.jar")) + \
                  glob.glob(os.path.join(rdppath, "dist/classifier.jar"))
    if not len(rdpjar_list):
        sys.stdout.write("%sno rdp_classifier*.jar or dist/classifier*.jar "
                         "found in RDPPATH%s\n" % (FAIL, ENDC))
        return

    sys.stdout.write("%sOK%s\n" % (OK, ENDC))
    
        
exes = {
    "SICKLE": "sickle",
    "CUTADAPT": "cutadapt",
    "UCHIME": "uchime",
    "DNACLUST": "dnaclust",
    "BLAST+": "blastn",
    "PyNAST": "pynast",
    "MUSCLE": "muscle",
    "T-Coffee": "t_coffee",
    "FastTree": "FastTree"
    }

modules = {
    "NumPy": "numpy",
    "SciPy": "scipy",
    "matplotlib": "matplotlib",
    "pandas": "pandas",
    "Biopython":  "Bio",
    "DendroPy": "dendropy"
    }

sys.stdout.write("\n%sChecking for dependencies...%s\n" % (HEADER, ENDC))
for name, exe in exes.iteritems():
    find_exe(name, exe)
for name, module in modules.iteritems():
    find_module(name, module)
find_rdp()
