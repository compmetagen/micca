Download and install
====================

Prerequisites
-------------

micca requires `Python <https://www.python.org/>`_ >=2.7, `NumPy
<http://scipy.org/>`_ (>= 1.8.0) and the software required in order to
install `SciPy <http://scipy.org/>`_ (>= 0.13.0) through pip.

On Ubuntu Linux >= 12.04
^^^^^^^^^^^^^^^^^^^^^^^^

In Ubuntu Linux >= 12.04, we suggest install NumPy and the requirements for
SciPy and matplotlib through the package manager:

.. code-block:: sh

   sudo apt-get -qq update
   sudo apt-get install build-essential
   sudo apt-get install python-numpy
   sudo apt-get install gcc gfortran python-dev libblas-dev liblapack-dev cython
   sudo apt-get install pkg-config libfreetype6 libfreetype6-dev libpng-dev

Then, upgrade pip and install setuptools:

.. code-block:: sh

   pip install --upgrade pip
   pip install 'setuptools >=14.0'


On OS X
^^^^^^^

In OS X, we recommend to install Python from `Homebrew <http://brew.sh/>`_:

   #. Install `Xcode <https://developer.apple.com/xcode/>`_;
   #. Install `Homebrew <http://brew.sh/>`_;
   #. Make sure the environment variable ``PATH`` is properly setted in your
      ``~/.bash_profile`` or ``~/.bashrc``::

      .. code-block:: sh
         export PATH=/usr/local/bin:$PATH

   #. Install Python and gfortran:

      .. code-block:: sh

         brew update
         brew install python
         brew install gfortran

Install NumPy:

      .. code-block:: sh

	 pip install numpy


Install micca using pip
-----------------------

The easiest way to install micca is to using pip, from PYPI:

.. code-block:: sh

   sudo pip install micca

or from the tarball (https://github.com/compmetagen/micca/releases):

.. code-block:: sh

   sudo pip install micca-X.Y.Z.tar.gz


Install micca from source
-------------------------

In order to install micca from sources (with the standard procedure
``python setup.py install``), in addition to Python (>=2.7, <3.0), NumPy
(>= 1.8.0) and SciPy (>= 0.13.0), the following Python packages must be
installed:

   * Pandas >=0.17.0
   * matplotlib >=1.3.0
   * Biopython >=1.50
   * cutadapt >=1.9
   * biom-format >=1.3.1

The easiest way to install these packages is to  is using pip:

.. code-block:: sh

   sudo pip install 'pandas >=0.17.0' 'matplotlib >=1.3.0' 'biopython >= 1.50' 'cutadapt >=1.9' 'biom-format >=1.3.1'

Download the latest version from
https://github.com/compmetagen/micca/releases and complete the
installation:

.. code-block:: sh

   tar -zxvf micca-X.Y.Z.tar.gz
   sudo python setup.py install

If you don’t have root access, install micca in a local directory by
specifying the ``--prefix`` argument. Then you need to set
``PYTHONPATH``:

.. code-block:: sh

   python setup.py install --prefix=/path/to/modules
   export PYTHONPATH=$PYTHONPATH:/path/to/modules/lib/python{version}/site-packages

.. note::

   In order to export the variable permanently add the command
   at the bottom of your ``~/.bash_profile`` or ``~/.bashrc`` file.


Testing the installation
------------------------

.. code-block:: sh

   micca -h


Install RDP classifier (optional)
---------------------------------

The RDP Classifier is a naive bayesian classifier for
taxonomic assignments
(http://sourceforge.net/projects/rdp-classifier/). The RDP classifier
can be used in the :doc:`/commands/classify` command (option
``-m/--method rdp``).

.. warning::

   Only RDP Classifier version >2.8 is supported.

Download and unzip the file (RDP cladssifier v2.11 2015-09-14):

.. code-block:: sh

   wget https://sourceforge.net/projects/rdp-classifier/files/rdp-classifier/rdp_classifier_2.11.zip
   unzip rdp_classifier_2.11.zip

Now you must set the environment variable ``RDPPATH`` by typing:

.. code-block:: sh

   $ export RDPPATH=/path-to-rdp-classifier/rdp_classifier_2.11/

e.g. ``export RDPPATH=/Users/David/rdp_classifier_2.11``.

.. note::

   In order to export the variable permanently add the latest command
   at the bottom of your ``.bashrc`` file.
