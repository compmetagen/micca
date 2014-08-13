Install
=======

micca is composed by several executable Python scripts and wraps lots of external
applications.

Requirements
------------
micca requires Python (http://www.python.org/) >= 2.7.

External Applications
^^^^^^^^^^^^^^^^^^^^^
* SICKLE (>=1.29)- A windowed adaptive trimming tool for FASTQ files using
  quality. (http://github.com/najoshi/sickle/releases)
* UCHIME - Chimeric sequences detection, public domain version
  (http://drive5.com/uchime/uchime_download.html)
* DNACLUST - Tool for clustering millions of short DNA sequences
  (http://dnaclust.sourceforge.net `Download Release 2 <http://sourceforge.net/projects/dnaclust/files/release_2/dnaclust_src.tar.gz/download>`_)
* BLAST+ - The Basic Local Alignment Search Tool
  (`BLAST+ executables <http://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download>`_)
* RDP Classifier (>=2.6) - Naive Bayesian classifier for taxonomic
  assignments
  (http://sourceforge.net/projects/rdp-classifier/). **After the
  installation set the environment variable ``RDPPATH`` by typing**::
  
      $ export RDPPATH=/path-to-rdp-classifier/
  
  (e.g. ``export RDPPATH=/Users/Pippo/rdp_classifier_2.5``).
  In order to export the variable permanently add the command at the
  bottom of your `.bashrc` file.
 
* PyNAST - NAST sequence aligner (http://biocore.github.io/pynast/)
* MUSCLE - Multiple Sequence Alignment (http://www.drive5.com/muscle/)
* T-Coffee - Simple MSA (http://tcoffee.crg.cat/apps/tcoffee)
* FastTree - Approximately-maximum-likelihood phylogenetic trees
  (http://www.microbesonline.org/fasttree/)

Python Modules
^^^^^^^^^^^^^^
* NumPy (http://scipy.org/)
* SciPy (http://scipy.org/)
* matplotlib (http://matplotlib.org/)
* pandas (http://pandas.pydata.org/)
* Biopython (http://biopython.org/)
* cutadapt (https://code.google.com/p/cutadapt/)
* DendroPy (http://pythonhosted.org/DendroPy/)

The easiest way to install the Python dependencies is by using pip::

    $ pip install numpy scipy matplotlib pandas biopython cutadapt dendropy

Install micca
-------------

1. Untar ``micca-X.Y.tar.gz``, creating ``micca-X.Y`` folder (where
   ``X.Y`` is the current version of micca)

2. Go into ``micca-X.Y`` folder and from a terminal run:

   .. code-block:: sh

      $ sudo python setup.py install

3. If you don't have root access, installing micca in a local
   directory by specifying the ``--prefix`` argument. Then you need to
   set ``PYTHONPATH``:

   .. code-block:: sh

      $ python setup.py install --prefix=/path/to/modules
      $ export PYTHONPATH=$PYTHONPATH:/path/to/modules/lib/python{version}/site-packages

4. Test the installation. From the command line run:

   .. code-block:: sh

      $ micca-test

   If all the required software is installed, you should see something like
   this::

      Checking for dependencies...
      DNACLUST... OK
      BLAST+... OK
      CUTADAPT... OK
      PyNAST... OK
      T-Coffee... OK
      MUSCLE... OK
      SICKLE... OK
      FastTree... OK
      UCHIME... OK
      Biopython... OK
      matplotlib... OK
      SciPy... OK
      DendroPy... OK
      NumPy... OK
      pandas... OK
      RDP Classifier... OK

