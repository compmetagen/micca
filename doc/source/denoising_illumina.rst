Denoising (Illumina only)
=========================

Usually, amplicon sequences are clustered into **Operational Taxonomic Units**
(OTUs) using a similarity threshold of 97%, which represents the common working
definition of bacterial species. 

Another approach consists to identify the **Sequence Variants** (SVs, see
:doc:`/otu` for details). This approach avoids clustering sequences at a
predefined similarity threshold and usually includes a denoising algorithm in
order to identify SVs.

In this tutorial we show how to perform the denoising of Illumina overlapping
paired-end sequences in order to detect the SVs. Athough this tutorial explains
how to apply the pipeline to 16S paired-end Illumina reads, it can be adapted to
Illumina single-end sequening or to others markers gene/spacers, e.g. **Internal
Transcribed Spacer (ITS)**, **18S** or **28S**.

.. contents:: Table of Contents
    :local:

Data download and preprocessing
-------------------------------

In this tutorial we analyze the same dataset used in :doc:`/pairedend_97`. Reads
merging, primer trimming and quality filtering are the same as in
:doc:`/pairedend_97`:

.. code-block:: sh

    wget ftp://ftp.fmach.it/metagenomics/micca/examples/garda.tar.gz
    tar -zxvf garda.tar.gz
    cd garda

    micca mergepairs -i fastq/*_R1*.fastq -o merged.fastq -l 100 -d 30
    micca trim -i merged.fastq -o trimmed.fastq -w CCTACGGGNGGCWGCAG -r GACTACNVGGGTWTCTAATCC -W -R -c
    micca filter -i trimmed.fastq -o filtered.fasta -e 0.75 -m 400

Denoising - Sequence Variants identification
--------------------------------------------

The :doc:`/commands/otu` command implements the UNOISE3 protocol
(``denovo_unoise``) which includes dereplication, denoising and chimera
filtering:

.. code-block:: sh

    micca otu -m denovo_unoise -i filtered.fasta -o denovo_unoise_otus -t 4 -c

The :doc:`/commands/otu` command returns several files in the output directory,
including the **SV table** (``otutable.txt``) and a FASTA file containing the
**representative sequences** (``otus.fasta``).

.. Note::

    See :doc:`/otu` to see how to apply the **de novo swarm**,
    **closed-reference** and the **open-reference** OTU picking strategies to
    these data.

Further steps
-------------

* :ref:`pairedend_97-taxonomy`

* :ref:`pairedend_97-tree`

* :ref:`pairedend_97-biom`

* :doc:`/phyloseq`

* :doc:`/table`
