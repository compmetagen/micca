msa
===

.. code-block:: console

    usage: micca msa [-h] -i FILE -o FILE [-m {muscle,nast}]
                    [--muscle-maxiters MUSCLE_MAXITERS] [--nast-template FILE]
                    [--nast-id NAST_ID] [--nast-threads NAST_THREADS]
                    [--nast-mincov NAST_MINCOV] [--nast-strand {both,plus}]
                    [--nast-notaligned FILE] [--nast-hits FILE] [--nast-nofilter]
                    [--nast-notrim]

    micca msa performs a multiple sequence alignment (MSA) on the input
    file in FASTA format. micca msa provides two approaches for MSA:

    * MUSCLE (doi: 10.1093/nar/gkh340). It is one of the most widely-used
    multiple sequence alignment software;

    * Nearest Alignment Space Termination (NAST) (doi:
    10.1093/nar/gkl244). MICCA provides a very fast and memory
    efficient implementation of the NAST algorithm. The algorithm is
    based on VSEARCH (https://github.com/torognes/vsearch). It requires
    a pre-aligned database of sequences (--nast-template). For 16S
    data, a good template file is the Greengenes Core Set
    (http://greengenes.lbl.gov/Download/Sequence_Data/Fasta_data_files/
    core_set_aligned.fasta.imputed).

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input FASTA file (required).
    -o FILE, --output FILE
                            output MSA file in FASTA format (required).
    -m {muscle,nast}, --method {muscle,nast}
                            multiple sequence alignment method (default muscle).

    MUSCLE specific options:
    --muscle-maxiters MUSCLE_MAXITERS
                            maximum number of MUSCLE iterations. Set to 2 for a
                            good compromise between speed and accuracy (>=1
                            default 16).

    NAST specific options:
    --nast-template FILE  multiple sequence alignment template file in FASTA
                            format.
    --nast-id NAST_ID     sequence identity threshold to consider a sequence a
                            match (0.0 to 1.0, default 0.75).
    --nast-threads NAST_THREADS
                            number of threads to use (1 to 256, default 1).
    --nast-mincov NAST_MINCOV
                            reject sequence if the fraction of alignment to the
                            template sequence is lower than MINCOV. This parameter
                            prevents low-coverage alignments at the end of the
                            sequences (default 0.75).
    --nast-strand {both,plus}
                            search both strands or the plus strand only (default
                            both).
    --nast-notaligned FILE
                            write not aligned sequences in FASTA format.
    --nast-hits FILE      write hits on a TAB delimited file with the query
                            sequence id, the template sequence id and the
                            identity.
    --nast-nofilter       do not remove positions which are gaps in every
                            sequenceces (useful if you want to apply a Lane mask
                            filter before the tree inference).
    --nast-notrim         force to align the entire candidate sequence (i.e. do
                            not trim the candidate sequence to that which is bound
                            by the beginning and end points of of the alignment
                            span

    Examples

    De novo MSA using MUSCLE:

        micca msa -i input.fasta -o msa.fasta

    Template-based MSA using NAST, the Greengenes alignment as
    template (clustered at 97% similarity) 4 threads and a sequence
    identity threshold of 75%:

        micca msa -i input.fasta -o msa.fasta -m nast --nast-threads 4 \
        --nast-template greengenes_2013_05/rep_set_aligned/97_otus.fasta
