split
=====

.. code-block:: console

    usage: micca split [-h] -i FILE -o FILE -b FILE [-n FILE] [-c FILE] [-s N]
                    [-e MAXE] [-t] [-f {fastq,fasta}]

    micca split assign the multiplexed reads to samples based on their 5'
    nucleotide barcode (demultiplexing) provided by the FASTA file
    (--barcode). micca split creates a single FASTQ or FASTA file with
    sample information (e.g. >SEQID;sample=SAMPLENAME) appended to the
    sequence identifier. Barcode and the sequence preceding it is removed
    by default, e.g.:

    Barcode file:        Input file:

    >SAMPLE1             >SEQ1
    TCAGTCAG             TCAGTCAGGCCACGGCTAACTAC...
    ...                  ...

    the output will be:

    >SEQ1;sample=SAMPLE1
    GCCACGGCTAACTAC...
    ...

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input FASTQ/FASTA file (required).
    -o FILE, --output FILE
                            output FASTQ/FASTA file (required).
    -b FILE, --barcode FILE
                            barcode file in FASTA format (required).
    -n FILE, --notmatched FILE
                            write reads in which no barcode was found.
    -c FILE, --counts FILE
                            write barcode counts in a tab-delimited file.
    -s N, --skip N        skip N bases before barcode matching (e.g. if your
                            sequences start with the control sequence 'TCAG'
                            followed by the barcode, set to 4) (>=0, default 0).
    -e MAXE, --maxe MAXE  maximum number of allowed errors (>=0, default 1).
    -t, --notrim          do not trim barcodes and the sequence preceding it
                            from sequences.
    -f {fastq,fasta}, --format {fastq,fasta}
                            file format (default fastq).

    Examples

    Split 'reads.fastq' and write the notmatched sequences in the
    file 'notmatched.fastq':

        micca split -i input.fastq -o splitted.fastq -b barcode.fasta \
        -n notmatched.fastq

