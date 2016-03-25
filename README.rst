micca - MICrobial Community Analysis
====================================

.. image:: https://travis-ci.org/compmetagen/micca.svg?branch=master
    :target: https://travis-ci.org/compmetagen/micca

micca (MICrobial Community Analysis) is a software pipeline for the
processing of amplicon sequencing data, **from raw sequences** to
**OTU tables**, **taxonomy classification** and **phylogenetic tree**
inference. The pipeline can be applied to a range of highly conserved
genes/spacers, such as **16S rRNA gene**, **Internal Transcribed
Spacer (ITS)** and **28S rRNA**.

For more information, visit http://micca.org/.

* `Documentation (latest) <http://micca.org/docs/latest>`_
* `Issues <https://github.com/compmetagen/micca/issues>`_
* `Github page <https://github.com/compmetagen/micca>`_


Key features
------------

* supports **single-end** (Roche 454, Illumina MiSeq/HiSeq ,Ion
  Torren) as well **overlapping paired-end** reads (Illumina MiSeq/HiSeq);
* **multithread** de novo greedy clustering as well **closed-reference** and
  **open-reference** OTU picking protocols are available;
* **state-of-the-art taxonomic classification** algorithms are
  available (RDP and consensus-based classifier);
* fast (multithread) and and memory efficient implementation of the
  **NAST** multiple sequence alignment (MSA);
* filter low quality  sequences according to the maximum allowed
  **expected error (EE) rate** %;
* **simple, easy to use**.


Citing micca
------------

Davide Albanese, Paolo Fontana, Carlotta De Filippo, Duccio Cavalieri
and Claudio Donati. **MICCA: a complete and accurate software for
taxonomic profiling of metagenomic data**. Scientific Reports 5,
Article number: 9743 (2015), doi:10.1038/srep09743. `Link
<http://www.nature.com/articles/srep09743/>`_.

micca wraps third party software packages and these **should be
cited** if they are used:

* `VSEARCH <https://github.com/torognes/vsearch>`_ used in ``classify``,
  ``filter``, ``mergepairs``, ``otu`` and ``msa`` commands
* MUSCLE (doi: 10.1093/nar/gkh340) used in ``msa`` and ``tree`` commands
* FastTree (doi: 10.1371/journal.pone.0009490) used in the ``tree`` command
* Cutadapt (doi: 10.14806/ej.17.1.200) used in the ``trim`` command
* RDP classifier (doi:10.1128/AEM.00062-07) used in the ``classify`` command
