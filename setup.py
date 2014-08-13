from distutils.core import setup, Extension
from distutils.util import *


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
    "scripts/micca-test",
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