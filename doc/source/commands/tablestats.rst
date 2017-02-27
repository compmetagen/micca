tablestats
==========

.. code-block:: console

    usage: micca tablestats [-h] -i FILE [-o DIR] [-t STEP] [-r] [-s SEED]

    micca tablestats reports a sample summary, an OTU summary and
    the rarefaction curves for the input OTU table. The
    rarefaction curves are evaluated using the interval of 'step'
    (-t/--step) sample depths, always including 1 and the total
    sample size.

    micca filterstats returns in the output directory 4 files:

    * tablestats_samplesumm.txt: samples summary;
    * tablestats_otusumm.txt: OTUs summary;
    * tablestats_rarecurve.txt: rarefaction curves in text format.
    * tablestats_rarecurve_plot.txt: rarefaction curves in png format.

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input FASTQ file, Sanger/Illumina 1.8+ format
                            (phred+33) (required).
    -o DIR, --output DIR  output directory (default .).
    -t STEP, --step STEP  sample depth interval (for rarefaction curves, default
                            500).
    -r, --replace         subsample with replacement (for rarefaction curves).
    -s SEED, --seed SEED  random seed (for rarefaction curves, default 0).

    Examples

    Compute OTU table statistics on otutable.txt:

        micca tablestats -i otutable.txt -o tablestats
