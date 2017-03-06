filterstats
===========

.. code-block:: console

    usage: micca filterstats [-h] -i FILE [-o DIR] [-t TOPN]
                            [-e MAXEERATES [MAXEERATES ...]] [-n MAXNS]

    micca filterstats reports the fraction of reads that would pass for each
    specified maximum expected error (EE) rate %% and the maximum number of
    allowed Ns after:

    * discarding sequences that are shorter than the specified length
    (suggested for Illumina overlapping paired-end (already merged)
    reads);

    * discarding sequences that are shorter than the specified length AND
    truncating sequences that are longer (suggested for Illumina and 454
    unpaired reads);

    Parameters for the 'micca filter' command should be chosen for each
    sequencing run using this tool.

    micca filterstats returns in the output directory 3 files:

    * filterstats_minlen.txt: fraction of reads that would pass the filter after
    the minimum length filtering;
    * filterstats_trunclen.txt: fraction of reads that would pass the filter after
    the minimum length filtering + truncation;
    * filterstats_plot.png: plot in PNG format.

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input FASTQ file, Sanger/Illumina 1.8+ format
                            (phred+33) (required).
    -o DIR, --output DIR  output directory (default .).
    -t TOPN, --topn TOPN  perform statistics on the first TOPN sequences
                            (disabled by default)
    -e MAXEERATES [MAXEERATES ...], --maxeerates MAXEERATES [MAXEERATES ...]
                            max expected error rates (%). (default [0.25, 0.5,
                            0.75, 1, 1.25, 1.5])
    -n MAXNS, --maxns MAXNS
                            max number of Ns. (disabled by default).

    Examples

    Compute filter statistics on the top 10000 sequences, predicting
    the fraction of reads that would pass for each maximum EE error
    rate (default values):

        micca filterstats -i input.fastq -o stats -t 10000
