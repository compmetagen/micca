merge
=====

.. code-block:: console

    usage: micca merge [-h] -i FILE [FILE ...] -o FILE [-s SEP] [-f {fastq,fasta}]

    micca merge merges several FASTQ or FASTA files in a single file.
    Different samples will be merged in a single file and sample names
    will be appended to the sequence identifier
    (e.g. >SEQID;sample=SAMPLENAME). Sample names are defined as the
    leftmost part of the file name splitted by the first occurence of '.'
    (-s/--sep option). Whitespace characters in names will be replaced
    with a single character underscore ('_').

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE [FILE ...], --input FILE [FILE ...]
                            input FASTQ/FASTA file(s) (required).
    -o FILE, --output FILE
                            output FASTQ/FASTA file (required).
    -s SEP, --sep SEP     Sample names are defined as the leftmost part of the
                            file name splitted by the first occurence of 'SEP'
                            (default .)
    -f {fastq,fasta}, --format {fastq,fasta}
                            file format (default fastq).

    Examples

    Merge files in FASTA format:

        micca merge -i in1.fasta in2.fasta in3.fasta -o merged.fasta \
        -f fasta

