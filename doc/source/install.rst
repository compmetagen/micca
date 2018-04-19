Install
=======

Using Docker (that is, on MS Windows, Mac OS X and Linux!)
----------------------------------------------------------

The easiest way to run micca is through `Docker <https://www.docker.com/>`_.
Docker works similarly to a virtual machine image, providing a container in
which all the software has already been installed, configured and tested.

    #. Install Docker for `Linux <https://docs.docker.com/linux/>`_,
       `Mac OS X <https://docs.docker.com/mac/>`_ or
       `Windows <https://docs.docker.com/windows/>`_.

    #. Run the ``Docker Quickstart Terminal`` (Mac OS X, Windows) or the
       ``docker`` daemon (Linux, ``sudo service docker start``).

    #. Download the latest version:

       .. code-block:: sh

           docker pull compmetagen/micca

    #. Run an instance of the image, mounting the host working directory
       (e.g. ``/Users/davide/micca``) on to the container working directory
       ``/micca``:

       .. code-block:: sh

           docker run --rm -t -i -v /Users/davide/micca:/micca -w /micca compmetagen/micca /bin/bash

       You need to write something like ``-v //c/Users/davide/micca:/micca`` if
       you are in Windows or ``-v /home/davide/micca:/micca`` in Linux. The
       ``--rm`` option automatically removes the container when it exits.

    #. Now you can use micca:

       .. code-block:: sh

           root@68f6784e1101:/micca# micca -h

.. note::

    The RDP classifier is preinstalled in the Docker image, so you can check the
    software version by typing ``echo $RDPPATH``


Using pip
---------

At the moment, only Python 2.7 is supported.

On Ubuntu >= 12.04 and Debian >=7
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We suggest to install the following packages through the package manager:

.. code-block:: sh

    sudo apt-get update
    sudo apt-get install build-essential python-numpy gcc gfortran python-dev libblas-dev liblapack-dev cython pkg-config libfreetype6 libfreetype6-dev libpng-dev

Then, upgrade pip and install setuptools:

.. code-block:: sh

    pip install --upgrade pip
    pip install 'setuptools >=14.0'

Finally, install micca:

.. code-block:: sh

    sudo pip install micca

On Mac OS X
^^^^^^^^^^^

In Mac OS X, we recommend to install Python from `Homebrew <http://brew.sh/>`_:

   #. Install `Xcode <https://developer.apple.com/xcode/>`_;
   #. Install `Homebrew <http://brew.sh/>`_;
   #. Make sure the environment variable ``PATH`` is properly setted in your
      ``~/.bash_profile`` or ``~/.bashrc``::

      .. code-block:: sh

         export PATH=/usr/local/bin:$PATH

   #. Install Python:

      .. code-block:: sh

         brew update
         brew install python

Install the GNU Fortran and the NumPy package:

.. code-block:: sh

    brew install gcc
    pip install numpy

Finally, install micca:

.. code-block:: sh

    sudo pip install micca

Installation problems
^^^^^^^^^^^^^^^^^^^^^
* BIOM fatal error: 'numpy/arrayobject.h'. If the installation process returns
  a message like this:

  .. code-block:: sh

    biom/_filter.c:258:10: fatal error: 'numpy/arrayobject.h' file not found
    #include "numpy/arrayobject.h"
            ^
    1 error generated.
    error: command 'clang' failed with exit status 1

  then you need to run:

  .. code-block:: sh
  
    pip install --global-option=build_ext --global-option="-I/usr/local/lib/python2.7/site-packages/numpy/core/include/" biom-format

  After that you can install the micca package.

Install micca from source
-------------------------

In order to install micca from sources (with the standard procedure
``python setup.py install``), in addition to Python (>=2.7) and NumPy
(>=1.8.0), the following Python packages must be installed:

   * SciPy >=0.13.0
   * Pandas >=0.17.0
   * matplotlib >=1.3.0
   * Biopython >=1.50
   * cutadapt >=1.9
   * biom-format >=1.3.1

The easiest way to install these packages is to is using pip:

.. code-block:: sh

   sudo pip install 'scipy >=0.13.0' 'pandas >=0.17.0' 'matplotlib >=1.3.0' 'biopython >= 1.50' 'cutadapt >=1.9' 'biom-format >=1.3.1'

Download the latest version from
https://github.com/compmetagen/micca/releases and complete the
installation:

.. code-block:: sh

   tar -zxvf micca-X.Y.Z.tar.gz
   sudo python setup.py install

If you don’t have root access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Install micca in a local directory by specifying the ``--prefix`` argument. Then
you need to set the environment variable ``PYTHONPATH``:

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

The RDP Classifier is a naive bayesian classifier for taxonomic assignments
(http://sourceforge.net/projects/rdp-classifier/). The RDP classifier can be
used in the :doc:`/commands/classify` command (option ``-m/--method rdp``).

.. warning::

   Only RDP Classifier version >2.8 is supported. Install the standard Java or
   Java compatible runtime (``sudo apt-get install default-jre`` in
   Ubuntu/Debian or go to the `Oracle Java homepage <www.java.com>`_ for OS X)

Download and unzip the file (RDP classifier 2.11 2015-09-14):

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
