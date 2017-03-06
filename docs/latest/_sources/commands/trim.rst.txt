trim
====

.. code-block:: console

    usage: micca trim [-h] -i FILE -o FILE [-w FORWARD [FORWARD ...]]
                    [-r REVERSE [REVERSE ...]] [-e MAXERATE] [-c] [-W] [-R]
                    [-f {fastq,fasta}]

    micca trim trims forward and reverse primers from a FASTQ/FASTA file
    using Cutadapt (doi: 10.14806/ej.17.1.200) internally. Primer and the
    sequence preceding (for forward) or succeding (for reverse) it are
    removed. Optionally, reads that do not contain the primers (untrimmed
    reads) can be discarded with the options -W/--duforward and
    -R/--dureverse. Recommended options are:

    * always discard reads that do not contain the forward primer
    (-W/--duforward option);

    * for overlapping paired-end (already merged) reads, also discard
    reads that do not contain the reverse primer (using both
    -W/--duforward and -R/--dureverse options).

    IUPAC codes and multiple primers are supported.

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input FASTQ or FASTA file (required).
    -o FILE, --output FILE
                            output FASTQ or FASTA file (required).
    -w FORWARD [FORWARD ...], --forward FORWARD [FORWARD ...]
                            trim forward primer(s). Only the best matching primer
                            is removed.
    -r REVERSE [REVERSE ...], --reverse REVERSE [REVERSE ...]
                            trim reverse primer(s). Only the best matching primer
                            is removed.
    -e MAXERATE, --maxerate MAXERATE
                            maximum allowed error rate (default 0.1).
    -c, --searchrc        search reverse complement primers too (default False).
    -W, --duforward       discard untrimmed reads (reads that do not contain the
                            forward primer) (always recommended) (default False).
    -R, --dureverse       discard untrimmed reads (reads that do not contain the
                            reverse primer) (suggested option for overlapping
                            paired-end already merged reads) (default False).
    -f {fastq,fasta}, --format {fastq,fasta}
                            file format (default fastq).

    Examples

    454 or Illumina single-end reads: trim forward primer and discard reads
    that do not contain it. Moreover, trim reverse primer:

        micca trim -i input.fastq -o trimmed.fastq -w AGGATTAGATACCCTGGTA \
        -r CRRCACGAGCTGACGAC -W

    Illumina overlapping paired-end (already merged) reads: trim
    forward and reverse primers. Reads that do not contain the forward
    or the reverse primer will be discarded:

        micca trim -i reads.fastq -o trimmed.fastq -w AGGATTAGATACCCTGGTA \
        -r CRRCACGAGCTGACGAC -W -R
