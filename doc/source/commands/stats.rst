stats
=====

.. code-block:: console

    usage: micca stats [-h] -i FILE [-o DIR] [-n TOPN]

    micca stats reports statistics on reads in a FASTQ file. micca stats
    returns in the output directory 3 tab-delimited text files:

    * stats_lendist.txt: length distribution;
    * stats_qualdist.txt: Q score distribution;
    * stats_qualsumm.txt: quality summary. For each read position, the
    following statistics are reported:
    - L: read position;
    - NPctCum: percent of reads with at least L bases;
    - QAv: average Q score at position L;
    - EERatePctAv: average expected error (EE) rate %.

    Moreover, micca stats returns the respective plots in PNG format,
    stats_lendist_plot.png, stats_qualdist_plot.png, and
    stats_qualsumm_plot.png.

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input FASTQ file, Sanger/Illumina 1.8+ format
                            (phred+33) (required).
    -o DIR, --output DIR  output directory (default .).
    -n TOPN, --topn TOPN  perform statistics only on the first TOPN sequences
                            (disabled by default).

    Examples

    Compute statistics on the top 10000 sequences of input.fastq:

        micca stats -i input.fastq -o stats -n 10000
