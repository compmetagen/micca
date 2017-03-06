convert
=======

.. code-block:: console

    usage: micca convert [-h] -i FILE -o FILE [-q FILE] [-d DEFAULTQ]
                        [-f INPUT_FORMAT] [-F OUTPUT_FORMAT]

    micca convert converts between sequence file formats. See
    http://biopython.org/wiki/SeqIO#File_Formats for a comprehnsive list
    of the supported file formats.

    Supported input formats:
    abi, abi-trim, ace, embl, embl-cds, fasta, fasta-qual, fastq, fastq-illumina, 
    fastq-sanger, fastq-solexa, gb, genbank, genbank-cds, ig, imgt, pdb-atom, 
    pdb-seqres, phd, pir, qual, seqxml, sff, sff-trim, swiss, tab, uniprot-xml

    Supported output formats:
    embl, fasta, fastq, fastq-illumina, fastq-sanger, fastq-solexa, gb, genbank,
    imgt, phd, qual, seqxml, sff, tab

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input sequence file (required).
    -o FILE, --output FILE
                            output sequence file (required).
    -q FILE, --qual FILE  input quality file (required for 'fasta-qual' input
                            format.
    -d DEFAULTQ, --defaultq DEFAULTQ
                            default phred quality score for format-without-quality
                            to format-with-quality conversion (default 40).
    -f INPUT_FORMAT, --input-format INPUT_FORMAT
                            input file format (default fastq).
    -F OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
                            input file format (default fasta).

    Examples

    Convert FASTA+QUAL files into a FASTQ (Sanger/Illumina 1.8+) file:

        micca convert -i input.fasta -q input.qual -o output.fastq \
        -f fasta-qual -F fastq

    Convert a SFF file into a FASTQ (Sanger/Illumina 1.8+) file:

        micca convert -i input.sff -o output.fastq -f sff -F fastq