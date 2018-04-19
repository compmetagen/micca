Supported file formats
======================

Sequence files
--------------

`FASTA <https://en.wikipedia.org/wiki/FASTA_format>`_ and `FASTQ
<https://en.wikipedia.org/wiki/FASTQ_format>`_ Sanger/Illumina 1.8+ format
(phred+33) formats are supported. micca provides the :doc:`/commands/convert`
command to convert between sequence file formats.

Taxonomy files
--------------

Taxonomy files map sequence IDs to taxonomy. Input taxonomy files must
be TAB-delimited files where rows are either in the form:
  
#. ``SEQID[TAB]k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__;g__;``
#. ``SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales;;;``
#. ``SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales``
#. ``SEQID[TAB]D_0__Bacteria;D_1__Firmicutes;D_2__Clostridia;D_3__Clostridiales;D_4__;D_5__;``

Compatible taxonomy files are:

  * Greengenes (http://greengenes.secondgenome.com/downloads);
  * QIIME-formatted SILVA (https://www.arb-silva.de/download/archive/qiime/);
  * UNITE (https://unite.ut.ee/repository.php);
  * Human Oral Microbiome Database (HOMD) (http://www.homd.org/).

The output taxonomy file returned by :doc:`/commands/classify` is a
TAB-delimited file where each row is in the format::

   SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales

OTU/SV tables and taxonomy tables
---------------------------------

The OTU table returned by :doc:`/commands/otu` is an OTU x sample, TAB-delimited
text file, containing the number of times an OTU is found in each sample::

   OTU     Mw_01 Mw_02 Mw_03 ...
   DENOVO1 151   178   177   ...
   DENOVO2 339   181   142   ...
   DENOVO3 533   305   63    ...
   DENOVO4 166   299   115   ...
   ...     ...   ...   ...   ...

The :doc:`/commands/tabletotax` command returns the "taxonomy tables" for each
taxonomic level, e.g.::

   OTU                                Mw_01 Mw_02 Mw_03 ...
   Bacteria;Bacteroidetes             1363  1543  1168  ...
   Bacteria;Cyanobacteria/Chloroplast 0     0     0     ...
   Bacteria;Firmicutes                6257  5780  6761  ...
   Bacteria;Lentisphaerae             0     1     0     ...
   ...                                ...   ...   ...   ...


.. _formats-sample_data:

Sample data
-----------

The sample data file contains all of the information about the samples. In QIIME
this file is called `Mapping File
<http://qiime.org/tutorials/tutorial.html#mapping-file-tab-delimited-txt>`_. In
micca, the sample data file must be a TAB-delimited text file (a row for each
sample). The first column must be the sample identifier (assigned in
:doc:`/commands/merge`, :doc:`/commands/split` or :doc:`/commands/mergepairs`)::

   ID    Group Altitude
   Mw_01 Mw1   492
   Mw_02 Mw1   492
   Mw_09 Mw1   492
   Mw_12 Mw1   492
   ...   ...   ...


Phylogenetic tree
-----------------

Only the `Newick format <https://en.wikipedia.org/wiki/Newick_format>`_ is
supported.

BIOM file
---------

The :doc:`/commands/tobiom` command generates OTU/SV tables in the biom version
1.0 JSON file format
(http://biom-format.org/documentation/format_versions/biom-1.0.html).