mergepairs
==========

.. code-block:: console

    usage: micca mergepairs [-h] -i FILE [FILE ...] -o FILE [-r FILE]
                            [-l MINOVLEN] [-d MAXDIFFS] [-p PATTERN] [-e REPL]
                            [-s SEP] [-n] [--notmerged-fwd FILE]
                            [--notmerged-rev FILE] [-t THREADS]

    micca mergepairs merges paired-end sequence reads into one sequence.

    A single merging of a pair of FASTQ files can be simply performed
    using both -i/--input and -r/--reverse options.

    When the option -r/--reverse is not specified:

    1. you can indicate several forward files (with the option -i/--input);

    2. the reverse file name will be constructed by replacing the string
    '_R1' in the forward file name with '_R2' (typical in Illumina
    file names, see options -p/--pattern and -e/--repl);

    3. after the merging of the paired reads, different samples will be
    merged in a single file and sample names will be appended to the
    sequence identifier (e.g. >SEQID;sample=SAMPLENAME), as in 'micca
    merge' and 'micca split'. Sample names are defined as the leftmost
    part of the file name splitted by the first occurence of '_'
    (-s/--sep option). Whitespace characters in names will be replaced
    with a single character underscore ('_').

    micca mergepairs wraps VSEARCH (https://github.com/torognes/vsearch).
    Statistical testing of significance is performed in a way similar to
    PEAR (doi: 10.1093/bioinformatics/btt593). The quality of merged bases
    is computed as in USEARCH (doi: 10.1093/bioinformatics/btv401).

    By default staggered read pairs (staggered pairs are pairs where the 3'
    end of the reverse read has an overhang to the left of the 5’ end
    of the forward read) will be merged. To override this feature (and 
    therefore to discard staggered alignments) set the -n/--nostagger 
    option.

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE [FILE ...], --input FILE [FILE ...]
                            forward FASTQ file(s), Sanger/Illumina 1.8+ format
                            (phred+33) (required).
    -o FILE, --output FILE
                            output FASTQ file (required).
    -r FILE, --reverse FILE
                            reverse FASTQ file, Sanger/Illumina 1.8+ format
                            (phred+33).
    -l MINOVLEN, --minovlen MINOVLEN
                            minimum overlap length (default 32).
    -d MAXDIFFS, --maxdiffs MAXDIFFS
                            maximum number of allowed mismatches in the overlap
                            region (default 8).
    -p PATTERN, --pattern PATTERN
                            when the reverse filename is not specified, it will be
                            constructed by replacing 'PATTERN' in the forward file
                            name with 'REPL' (default _R1).
    -e REPL, --repl REPL  when the reverse filename is not specified, it will be
                            constructed by replacing 'PATTERN' in the forward file
                            name with 'REPL' (default _R2).
    -s SEP, --sep SEP     when the reverse file name is not specified, sample
                            names are appended to the sequence identifier (e.g.
                            >SEQID;sample=SAMPLENAME). Sample names are defined as
                            the leftmost part of the file name splitted by the
                            first occurence of 'SEP' (default _)
    -n, --nostagger       forbid the merging of staggered read pairs. Without
                            this option the command will merge staggered read
                            pairs and the 3' overhang of the reverse read will be
                            not included in the merged sequence.
    --notmerged-fwd FILE  write not merged forward reads.
    --notmerged-rev FILE  write not merged reverse reads.
    -t THREADS, --threads THREADS
                            number of threads to use (1 to 256, default 1).

    Examples

    Merge reads with a minimum overlap length of 50 and maximum number
    of allowed mismatches of 3:

        micca mergepairs -i reads1.fastq -r reads2.fastq -o merged.fastq \
        -l 50 -d 3

    Merge several illumina paired reads (typically named *_R1*.fastq and
    *_R2*.fastq):

        micca mergepairs -i *_R1*.fastq -o merged.fastq --notmerged-fwd \
        notmerged_fwd.fastq --notmerged-rev notmerged_rev.fastq