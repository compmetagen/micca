# micca - Docker

micca (MICrobial Community Analysis) is a software pipeline for the processing
of amplicon sequencing data, from raw sequences to OTU tables, taxonomy
classification and phylogenetic tree inference. The pipeline can be applied to a
range of highly conserved genes/spacers, such as 16S rRNA gene, Internal
Transcribed Spacer (ITS) and 28S rRNA. Homepage: http://www.micca.org.

The RDP classifier is preinstalled in the Docker image, so you can check the
software version by typing ``echo $RDPPATH``
(see https://hub.docker.com/r/compmetagen/rdpclassifier/).

## Available Tags/Versions

- latest: GitHub snapshot (master)
- 1.7.0: micca 1.7.0 (RDP Classifier release 2.12 included)
- 1.6.2: micca 1.6.2 (RDP Classifier release 2.11 included)
- 1.6.1: micca 1.6.1 (RDP Classifier release 2.11 included)
- 1.6.0: micca 1.6.0 (RDP Classifier release 2.11 included)
- 1.5.0: micca 1.5.0 (RDP Classifier release 2.11 included)
- 1.4.0: micca 1.4.0 (RDP Classifier release 2.11 included)
- 1.3.0: micca 1.3.0 (RDP Classifier release 2.11 included)
- 1.2.2: micca 1.2.2 (RDP Classifier release 2.11 included)


## Quickstart

1. Download the latest version:

   `docker pull compmetagen/micca`

2. Run an instance of the image, mounting the host working directory
   (e.g. ``/Users/davide/micca``) on to the container working directory
   ``/micca``:

   `docker run --rm -t -i -v /Users/davide/micca:/micca -w /micca compmetagen/micca /bin/bash`

   You need to write something like ``-v //c/Users/davide/micca:/micca`` if
   you are in Windows or ``-v /home/davide/micca:/micca`` in Linux. The
   ``--rm`` option automatically removes the container when it exits.

3. Run micca without parameters:

   `root@68f6784e1101:/micca# micca`
