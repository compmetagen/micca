# micca - Docker

micca (MICrobial Community Analysis) is a software pipeline for the processing
of amplicon sequencing data, from raw sequences to OTU tables, taxonomy
classification and phylogenetic tree inference. The pipeline can be applied to a
range of highly conserved genes/spacers, such as 16S rRNA gene, Internal
Transcribed Spacer (ITS) and 28S rRNA. Homepage: http://www.micca.org.

The RDP Classifier is included.

## Available Tags/Versions

- latest: GitHub snapshot (master)

## Quickstart

1. Download the latest version:

   `docker pull compmetagen/micca`

2. Run an instance of the image, mounting the host directory:

   `docker run -t -i -v /Users/davide/micca:/micca -w /micca compmetagen/micca /bin/bash`

3. Run micca without parameters:

   `root@68f6784e1101:/micca# micca`
