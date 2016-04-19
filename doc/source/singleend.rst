Single-end sequencing
=====================

This tutorial describes a standard micca pipeline for the analysis
of single-end amplicon data. This pipeline is intended for different
platforms, such as **Roche 454**, **Illumina MiSeq/HiSeq** and **Ion
Torrent**. Although this tutorial explains how to apply the pipeline to
**16S rRNA** amplicons, it can be adapted to others markers gene/spacers,
e.g. **Internal Transcribed Spacer (ITS)** or **28S**.

.. contents:: Table of Contents
   :local:
   :depth: 1


Dataset download
----------------

The dataset used in this tutorial is taken from the Barelli et
al. paper *Habitat fragmentation is associated to gut microbiota
diversity of an endangered primate: implications for conservation*
(https://doi.org/doi:10.1038/srep14862). The dataset contains only a
subset of the entire study (Mwanihana samples only) for a total of
**15 samples** (in FASTQ format) and **235179 16S rRNA amplicon
reads** (V1-V3 hypervariable regions, 27-Forward
5'-AGAGTTTGATCMTGGCTCAG, 533-Reverse 5'-TTACCGCGGCTGCTGGCAC). The 454
pyrosequencing was carried out on the GS FLX+ system using the XL+
chemistry.

Open a terminal, download the data and prepare the working directory:

.. code-block:: sh

   wget ftp://ftp.fmach.it/metagenomics/micca/examples/mwanihana.tar.gz
   tar -zxvf mwanihana.tar.gz
   cd mwanihana


Merge files
-----------

Now the FASTQ files must be merged in a single file. This operation
can be performed with the :doc:`/commands/merge` command. Sample names
will be included into the sequence indentifiers.

.. code-block:: sh

   micca merge -i fastq/*.fastq -o merged.fastq

.. Note::

   The :doc:`/commands/merge` command works with FASTQ or FASTA
   files. If your sequences are in a different format (e.g. SFF or
   FASTA+QUAL) use :doc:`/commands/convert` to convert them.

.. Warning::

   In the case of multiplexed reads (with 5' barcode sequences) use
   :doc:`/commands/split` instead of :doc:`/commands/merge`. This
   command will perform demultiplexing and merging at the same time.

.. Warning::

   In the case of overlapping paired-end reads go to
   :doc:`/pairedend`.

.. _singleend-primer_trimming:

Primer trimming
---------------

Segments which match PCR primers should be now removed. Typical Roche
454 reads start with a sequence key (e.g. TCAG) followed by the
barcode (if it was not previously removed) and the forward primer.
For these types of data (and in general, for single-end sequencing) we
recommend to **trim both forward reverse primers and discard reads that
do not contain the forward primer**. Moreover, sequence preceding (for
the forward) or succeding (for the reverse, if found) primers should
be removed:

.. image:: /images/read454.png
   :align: center

These operations can be performed with the :doc:`/commands/trim` command:

.. code-block:: sh

   micca trim -i merged.fastq -o trimmed.fastq -w AGAGTTTGATCMTGGCTCAG -r GTGCCAGCAGCCGCGGTAA -W

The option ``-W/--duforward`` ensures that reads that do not contain
the forward primer will be discarded.

.. Warning::

   Do not use the ``-R/--dureverse`` with single-end reads.

.. Note::

   The :doc:`/commands/trim` command supports `IUPAC
   <http://www.bioinformatics.org/sms/iupac.html>`_ nucleotide codes
   and multiple primers. With the option ``-c/--searchrc`` the command
   searches reverse complement primers too. :doc:`/commands/trim`
   works with FASTQ or FASTA files.

.. _singleend-quality_filtering:

Quality filtering
-----------------

Producing high-quality OTUs requires high-quality reads. The
:doc:`/commands/filter` command filters sequences according to the
maximum allowed expected error (EE) rate % (see :doc:`/filtering`). We
recommend values <=1%. Moreover, to obtain good results in clustering
(see :doc:`/commands/otu`), reads should be **truncated at the same
length** when they cover partial amplicons or if quality deteriorates
towards the end (common when you have long amplicons in single-end
sequencing).

.. Warning::

   Parameters for the :doc:`/commands/filter` command should be chosen
   using the command :doc:`/commands/filterstats`.


Choosing parameters for filtering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The command :doc:`/commands/filterstats` reports the fraction of reads
that would pass for each specified maximum expected error (EE) rate %:

.. code-block:: sh

   micca filterstats -i trimmed.fastq -o filterstats

Open the PNG file ``filterstats/stats_plot.png``:

.. image:: /images/filterstats454.png
   :align: center

In this case we are interested in the plot below (minimum length
filtering + truncation). A truncation length of **350** and a maximum
error rate of **0.5%** seems to be a good compromise between read read
length, expected error rate and number of reads remaining. Inspecting
the file ``filterstats/trunclen_stats.txt``, you can see that more
than **92%** reads will pass the filter::

   L       0.25    0.5     0.75    1.0     1.25    1.5
   ...
   349     78.905  92.472  97.425  99.135  99.705  99.897
   350     78.639  92.385  97.389  99.126  99.704  99.896
   351     78.369  92.300  97.357  99.116  99.700  99.892
   ...

.. Note::

   To obtain general sequencing statistics, run
   :doc:`/commands/stats`.


Filter sequences
^^^^^^^^^^^^^^^^

Now we can run the :doc:`/commands/filter` command with
the selected parameters:

.. code-block:: sh

   micca filter -i trimmed.fastq -o filtered.fasta -e 0.5 -m 350 -t

.. Note::

   The maximum number of allowed Ns after truncation can be also
   specified in :doc:`/commands/filterstats` and in
   :doc:`/commands/filter`.


.. _singleend-otu_picking:

OTU picking
-----------

To characterize the taxonomic structure of the samples, the sequences
are now organized into `Operational Taxonomic Units (OTUs)
<https://en.wikipedia.org/wiki/Operational_taxonomic_unit>`_ at
varying levels of identity. An identity of **97%** represent the
common working definition of bacterial species. The
:doc:`/commands/otu` command implements several state-of-the-art
approaches for OTU clustering, but in this tutorial we will focus on
the **de novo greedy clustering** (see :doc:`/otu`):

.. code-block:: sh

   micca otu -i filtered.fasta -o denovo_greedy_otus -d 0.97 -c -t 4

The :doc:`/commands/otu` command returns several files in the output
directory, including the **OTU table** (``otutable.txt``) and a FASTA
file containing the **representative sequences** (``otus.fasta``).

.. Note::

   See :doc:`/otu` to see how to apply the **swarm de novo**,
   **closed-reference** and the **open-reference** OTU picking strategies to
   these data.


Assign taxonomy
---------------

Now we can assign taxonomy to each representative sequence using the
:doc:`/commands/classify` command. In this tutorial we use the RDP
(https://doi.org/10.1128/AEM.00062-07) classifier.

.. code-block:: sh

   micca classify -m rdp -i denovo_greedy_otus/otus.fasta -o denovo_greedy_otus/taxa.txt

:doc:`/commands/classify` returns a taxonomy file like this::

   DENOVO1 Bacteria;Firmicutes;Clostridia;Clostridiales
   DENOVO2 Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales
   DENOVO3 Bacteria;Verrucomicrobia;Opitutae
   DENOVO4 Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales
   ...


Infer the phylogenetic tree
---------------------------

These steps are necessary if you want to use phylogenetic-based
metrics such as the UniFrac distance
(https://doi.org/10.1128/AEM.01996-06) in the downstream analysis.


Multiple Sequence Alignment (MSA)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :doc:`/commands/msa` command provides two approaches for `MSA
<https://en.wikipedia.org/wiki/Multiple_sequence_alignment>`_: MUSCLE
(https://doi.org/10.1093/nar/gkh340) (de novo alignment) and Nearest
Alignment Space Termination (NAST)
(https://doi.org/10.1093/nar/gkl244) (which uses a template
alignment). In this tutorial we will use the NAST alignment
method. For 16S rRNA sequences, a good template alignment is the
Greengenes Core Set:

.. code-block:: sh

   wget ftp://ftp.fmach.it/metagenomics/micca/dbs/core_set.tar.gz
   tar -zxvf core_set.tar.gz

At this point we can run the :doc:`/commands/msa` command:

.. code-block:: sh

   micca msa -m nast -i denovo_greedy_otus/otus.fasta -o denovo_greedy_otus/msa.fasta --nast-template core_set_aligned.fasta.imputed --nast-threads 4


Build the phylogenetic tree
^^^^^^^^^^^^^^^^^^^^^^^^^^^

At this point we can build the phylogenetic tree from the MSA using
:doc:`/commands/tree`:

.. code-block:: sh

   micca tree -i denovo_greedy_otus/msa.fasta -o denovo_greedy_otus/tree.tree

.. Note::

   The output tree is in `Newick format
   <https://en.wikipedia.org/wiki/Newick_format>`_.


Midpoint rooting
^^^^^^^^^^^^^^^^

UniFrac metrics require phylogenetic trees to be rooted. The tree can
be rooted (in this case at midpoint between the two most distant tips
of the tree) using the :doc:`/commands/root` command:

.. code-block:: sh

   micca root -i denovo_greedy_otus/tree.tree -o denovo_greedy_otus/tree_rooted.tree

.. Note::

   Tree can also be rooted with the outgroup clade containing selected
   targets, see :doc:`/commands/root`.


Build the BIOM file
-------------------

The `Biological Observation Matrix (BIOM) <http://biom-format.org/>`_
is a common format for representing OTU tables and metadata and is the
core data type for downstream analyses in `QIIME <http://qiime.org>`_
and in `phyloseq
<https://joey711.github.io/phyloseq/>`_. :doc:`/commands/tobiom`
converts the OTU table and the taxonomy table produced by the previous
steps to the BIOM format. In addition, the :ref:`formats-sample_data` can
be added:

.. code-block:: sh

   micca tobiom -i denovo_greedy_otus/otutable.txt -o denovo_greedy_otus/tables.biom -t denovo_greedy_otus/taxa.txt -s sampledata.txt


Import and analyze the data into R and phyloseq
-----------------------------------------------

See :doc:`/phyloseq`


Compute basic OTU table statistics, rarefy and summarize OTU tables by taxa using micca
---------------------------------------------------------------------------------------

See :doc:`/table`
