otu
===

See :doc:`/otu` for details.

.. code-block:: console

    usage: micca otu [-h] -i FILE [-o DIR] [-r FILE]
                    [-m {denovo_greedy,denovo_unoise,denovo_swarm,closed_ref,open_ref}]
                    [-d ID] [-n MINCOV] [-t THREADS] [-g {dgc,agc}] [-s MINSIZE]
                    [-a {both,plus}] [-c] [-S CHIM_ABSKEW]
                    [--swarm-differences SWARM_DIFFERENCES] [--swarm-fastidious]
                    [--unoise-alpha UNOISE_ALPHA]

    micca otu assigns similar sequences (marker genes such as 16S rRNA and
    the fungal ITS region) to operational taxonomic units (OTUs) or sequence 
    variants (SVs).

    Trimming the sequences to a fixed position before clustering is
    *strongly recommended* when they cover partial amplicons or if quality
    deteriorates towards the end (common when you have long amplicons and
    single-end sequencing).

    Removing ambiguous nucleotides 'N' (with the option --maxns 0 in micca
    filter) is mandatory if you use the de novo swarm clustering method.

    micca otu provides the following protocols:

    * de novo greedy clustering (denovo_greedy): useful for for the 
    identification of 97% OTUs; 

    * de novo unoise (denovo_unoise): denoise Illumina sequences using
    the UNOISE3 protocol;

    * de novo swarm (denovo_swarm): a robust and fast clustering method 
    (deprecated, it will be removed in version 1.8.0);

    * closed-reference clustering (closed_ref): sequences are clustered
    against an external reference database and reads that could not be
    matched are discarded.

    * open-reference clustering (open_ref): sequences are clustered
    against an external reference database and reads that could not be
    matched are clustered with the 'de novo greedy' protocol.

    Outputs:

    * otutable.txt: OTU x sample, TAB-separated OTU table file,
    containing the number of times an OTU is found in each sample.

    * otus.fasta: FASTA file containing the representative sequences (OTUs);

    * otuids.txt: OTU ids to original sequence ids (tab-delimited text
    file);

    * hits.txt: three-columns, TAB-separated file with matching sequence,
    representative (seed) and identity (if available, else '*');

    * otuschim.fasta (only for 'denovo_greedy', 'denovo_swarm' and
    'open_ref' when --rmchim is specified): FASTA file containing the
    chimeric otus.

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input fasta file (required).
    -o DIR, --output DIR  output directory (default .).
    -r FILE, --ref FILE   reference sequences in fasta format, required for
                            'closed_ref' and 'open_ref' clustering methods.
    -m {denovo_greedy,denovo_unoise,denovo_swarm,closed_ref,open_ref}, --method {denovo_greedy,denovo_unoise,denovo_swarm,closed_ref,open_ref}
                            clustering method (default denovo_greedy)
    -d ID, --id ID        sequence identity threshold (for 'denovo_greedy',
                            'closed_ref' and 'open_ref', 0.0 to 1.0, default
                            0.97).
    -n MINCOV, --mincov MINCOV
                            reject sequence if the fraction of alignment to the
                            reference sequence is lower than MINCOV (for
                            'closed_ref' and 'open_ref' clustering methods,
                            default 0.75).
    -t THREADS, --threads THREADS
                            number of threads to use (1 to 256, default 1).
    -g {dgc,agc}, --greedy {dgc,agc}
                            greedy clustering strategy, distance (DGC) or
                            abundance-based (AGC) (for 'denovo_greedy' and
                            'open_ref' clustering methods) (default dgc).
    -s MINSIZE, --minsize MINSIZE
                            discard sequences with an abundance value smaller than
                            MINSIZE after dereplication (>=1, default values are 2
                            for 'denovo_greedy' and 'open_ref', 1 for
                            'denovo_swarm' and 8 for 'denovo_unoise').
    -a {both,plus}, --strand {both,plus}
                            search both strands or the plus strand only (for
                            'closed_ref' and 'open_ref' clustering methods,
                            default both).

    Chimera removal specific options:
    -c, --rmchim          remove chimeric sequences (ignored in method
                            'closed_ref'
    -S CHIM_ABSKEW, --chim-abskew CHIM_ABSKEW
                            abundance skew. It is used to distinguish in a three-
                            way alignment which sequence is the chimera and which
                            are the parents. If CHIM_ABSKEW=2.0, the parents
                            should be at least 2 times more abundant than their
                            chimera (defaults values are 16.0 for 'denovo_unoise',
                            2.0 otherwise).

    Swarm specific options:
    --swarm-differences SWARM_DIFFERENCES
                            maximum number of differences allowed between two
                            amplicons. Commonly used d values are 1 (linear
                            complexity algorithm), 2 or 3, rarely higher. (>=0,
                            default 1).
    --swarm-fastidious    when working with SWARM_DIFFERENCES=1, perform a
                            second clustering pass to reduce the number of small
                            OTUs (recommended option).

    UNOISE specific options:
    --unoise-alpha UNOISE_ALPHA
                            specify the alpha parameter (default 2.0).

    Examples

    De novo clustering with a 97% similarity threshold and remove
    chimeric OTUs:

        micca otu -i input.fasta --method denovo_greedy --id 0.97 -c

    Open-reference OTU picking protocol with a 97% similarity
    threshold, without removing chimeras in the de novo protocol step
    and using 8 threads:

        micca otu -i input.fasta --method open_ref --threads 8 --id 0.97 \
        --ref greengenes_2013_05/rep_set/97_otus.fasta

    De novo swarm clustering with the protocol using 4 threads:

        micca otu -i input.fasta --method denovo_swarm --threads 4 \
        --swarm-fastidious --rmchim --minsize 1
