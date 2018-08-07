micca - MICrobial Community Analysis
====================================

.. image:: https://travis-ci.org/compmetagen/micca.svg?branch=master
    :target: https://travis-ci.org/compmetagen/micca

micca (MICrobial Community Analysis) is a software pipeline for the
processing of amplicon sequencing data, **from raw sequences** to
**OTU tables**, **taxonomy classification** and **phylogenetic tree**
inference. The pipeline can be applied to a range of highly conserved
genes/spacers, such as **16S rRNA gene**, **Internal Transcribed
Spacer (ITS)** **18S** and **28S rRNA**. micca is an open-source, GPLv3-licensed
software.

* `Homepage <http://micca.org/>`_
* `Documentation (latest) <https://micca.readthedocs.io>`_
* `Issues <https://github.com/compmetagen/micca/issues>`_
* `Github page <https://github.com/compmetagen/micca>`_

Key features:

* supports **single-end** (Roche 454, Illumina MiSeq/HiSeq ,Ion
  Torrent) and **overlapping paired-end** reads (Illumina MiSeq/HiSeq);
* **multithread** de novo greedy, closed-reference, open-reference and swarm OTU
  picking protocols;
* **denoising** of Illumina reads;
* **state-of-the-art taxonomic classification** algorithms (RDP and 
  consensus-based classifier);
* fast and and memory efficient **NAST** multiple sequence alignment (MSA);
* filters low quality sequences according to the maximum allowed **expected
  error (EE) rate** %;
* runs on **Linux**, **Mac OS X** and **MS Windows** (through Docker
  containers)
* **simple, easy to use**.

**Docker** images are available (compmetagen/micca) starting from version 1.2.2,
see the documentation (>=1.3.0) to learn how to use them. `Docker hub page
<https://hub.docker.com/r/compmetagen/micca/>`_.

**How to cite**: Davide Albanese, Paolo Fontana, Carlotta De Filippo, Duccio 
Cavalieri and Claudio Donati. **MICCA: a complete and accurate software for
taxonomic profiling of metagenomic data**. Scientific Reports 5, Article number:
9743 (2015), doi:10.1038/srep09743, `Link 
<http://www.nature.com/articles/srep09743/>`_. Dataset download:
ftp://ftp.fmach.it/metagenomics/micca/scirep/.

micca wraps third party software packages and these **should be
cited** if they are used:

* VSEARCH (doi: 10.7717/peerj.2584) used in ``classify``,
  ``filter``, ``mergepairs``, ``otu`` and ``msa`` commands
* MUSCLE (doi: 10.1093/nar/gkh340) used in ``msa`` and ``tree`` commands
* FastTree (doi: 10.1371/journal.pone.0009490) used in the ``tree`` command
* Cutadapt (doi: 10.14806/ej.17.1.200) used in the ``trim`` command
* RDP classifier (doi: 10.1128/AEM.00062-07) used in the ``classify`` command
* swarm (doi: 10.7717/peerj.1420) used in the ``otu`` command
