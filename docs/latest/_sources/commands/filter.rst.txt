filter
======

.. code-block:: console

    usage: micca filter [-h] -i FILE -o FILE [-e MAXEERATE] [-m MINLEN] [-t]
                        [-n MAXNS] [-f {fastq,fasta}]

    micca filter filters sequences according to the maximum allowed
    expected error (EE) rate %%. Optionally, you can:

    * discard sequences that are shorter than the specified length
    (suggested for Illumina overlapping paired-end (already merged)
    reads) (option --minlen MINLEN);

    * discard sequences that are shorter than the specified length AND
    truncate sequences that are longer (suggested for Illumina and 454
    unpaired reads) (options --minlen MINLEN --trunc);

    * discard sequences that contain more than a specified number of Ns
    (--maxns).

    Sequences are first shortened and then filtered. Overlapping paired
    reads with should be merged first (using micca-mergepairs) and then
    filtered.

    The expected error (EE) rate %% in a sequence of length L is defined
    as (doi: 10.1093/bioinformatics/btv401):

                    sum(error probabilities)
        EE rate %% = ------------------------ * 100
                                L

    Before filtering, run 'micca filterstats' to see how many reads will
    pass the filter at different minimum lengths with or without
    truncation, given a maximum allowed expected error rate %% and maximum
    allowed number of Ns.

    micca-filter is based on VSEARCH (https://github.com/torognes/vsearch).

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input FASTQ file, Sanger/Illumina 1.8+ format
                            (phred+33) (required).
    -o FILE, --output FILE
                            output FASTA/FASTQ file (required).
    -e MAXEERATE, --maxeerate MAXEERATE
                            discard sequences with more than the specified expeced
                            error rate % (values <=1%, i.e. less or equal than one
                            error per 100 bases, are highly recommended).
                            Sequences are discarded after truncation (if enabled)
                            (default 1).
    -m MINLEN, --minlen MINLEN
                            discard sequences that are shorter than MINLEN
                            (default 1).
    -t, --trunc           truncate sequences that are longer than MINLEN
                            (disabled by default).
    -n MAXNS, --maxns MAXNS
                            discard sequences with more than the specified number
                            of Ns. Sequences are discarded after truncation
                            (disabled by default).
    -f {fastq,fasta}, --output-format {fastq,fasta}
                            file format (default fasta).

    Examples

    Truncate reads at 300 bp, discard low quality sequences
    (with EE rate > 0.5%%) and write a FASTA file:

        micca filter -i reads.fastq -o filtered.fasta -m 300 -t -e 0.5