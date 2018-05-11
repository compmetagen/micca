---
layout: default
---

`Stable version: 1.7.0 (2018/04/20)`

micca is an open-source, command-line software for the processing of **amplicon
sequencing data**, from raw sequences to **OTU tables**, **taxonomic
classification** and **phylogenetic tree inference**. The pipeline can be
applied to a range of highly conserved genes/spacers, such as **16S rRNA gene**
and **Internal Transcribed Spacer (ITS)**.

 * [Documentation (1.6.1-latest)](https://micca.readthedocs.io)
 * [Old documentation (0.1-1.6.0)](ftp://ftp.fmach.it/metagenomics/micca/olddocs/index.html))
 * [Issues](https://github.com/compmetagen/micca/issues)
 * [Users forum](https://groups.google.com/d/forum/micca-users)
 * [Github page](https://github.com/compmetagen/micca)

### Main features
* supports **single-end** (Roche 454, Illumina MiSeq/HiSeq ,Ion Torrent) and
  **overlapping paired-end** reads (Illumina MiSeq/HiSeq);
* multithread **de novo greedy**, **closed-reference**, **open-reference** and 
  **swarm** OTU picking protocols; 
* **denoising** of Illumina reads;
* state-of-the-art taxonomic classification algorithms (**RDP** and
  **consensus-based** classifier);
* fast and and **memory efficient NAST** multiple sequence alignment (MSA); 
* filters low quality sequences according to the **maximum allowed expected
  error (EE) rate %**;
* runs on Linux, Mac OS X and MS Windows (through **Docker** containers);
* **simple, easy to use**.

### Citing
Davide Albanese, Paolo Fontana, Carlotta De Filippo, Duccio Cavalieri and
Claudio Donati. MICCA: a complete and accurate software for taxonomic profiling
of metagenomic data. Scientific Reports 5, Article number: 9743 (2015),
doi:10.1038/srep09743, Link. Dataset download:
ftp://ftp.fmach.it/metagenomics/micca/scirep/.

### Install

* [Using PIP](https://pypi.org/project/micca/) `$ pip install micca`
* [Docker](https://hub.docker.com/r/compmetagen/micca/) images are availablesince version 1.2.2 `$ docker pull compmetagen/micca`
* [From sources](https://github.com/compmetagen/micca/releases) `$ python setup.py install`

### Examples
Dereplication, denoising and chimera filtering in one step, using 4 threads:

```bash
$ micca otu -m denovo_unoise -i input.fasta -o outdir -t 4 -c
```

Discard reads with expected error rate >0.5% and shorter than 300 bp:
```bash
$ micca filter -i input.fastq -o output.fasta -e 0.5 -m 300
```

### Third-party software
micca wraps third-party software packages and these should be cited if they are used:

* VSEARCH (doi: 10.7717/peerj.2584) used in `classify`, `filter`, `mergepairs`, `otu` and `msa` commands
* MUSCLE (doi: 10.1093/nar/gkh340) used in `msa` and `tree` commands
* FastTree (doi: 10.1371/journal.pone.0009490) used in the `tree` command
* Cutadapt (doi: 10.14806/ej.17.1.200) used in the `trim` command
* RDP classifier (doi: 10.1128/AEM.00062-07) used in the `classify` command
* swarm (doi: 10.7717/peerj.1420) used in the `otu` command