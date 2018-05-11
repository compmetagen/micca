---
layout: default
---

Stable version: 1.7.0 (2018/04/20)

micca is a software pipeline for the processing
of **amplicon sequencing data**, from raw sequences to **OTU tables**,
**taxonomic classification** and **phylogenetic tree inference**. The pipeline
can be applied to a range of highly conserved genes/spacers, such as **16S rRNA
gene**, **Internal Transcribed Spacer (ITS)** and **28S rRNA**. micca is an
**open-source**, GPLv3-licensed software.


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

### Install

[![alt text](/assets/images/python_logo.png)](https://pypi.org/project/micca/) `$ pip install micca`

[![alt text](/assets/images/docker_logo.png)](https://hub.docker.com/r/compmetagen/micca/) `$ docker pull compmetagen/micca`

[![alt text](/assets/images/github_logo.png)](https://github.com/compmetagen/micca/releases) `$ python setup.py install`

### Examples
Dereplication, denoising and chimera filtering in one step, using 4 threads:

```bash

$ micca otu -m denovo_unoise -i input.fasta -o outdir -t 4 -c
```


Site under maintenance. 

[Documentation](http://micca.readthedocs.io).

[Old documentation (0.1->1.6.0)](ftp://ftp.fmach.it/metagenomics/micca/olddocs/index.html)