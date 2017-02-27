otu
===

.. code-block:: console

    usage: micca otu [-h] -i FILE [-o DIR] [-r FILE]
                    [-m {denovo_greedy,denovo_swarm,closed_ref,open_ref}] [-d ID]
                    [-n MINCOV] [-t THREADS] [-c] [-g {dgc,agc}] [-s MINSIZE]
                    [-a {both,plus}] [--swarm-differences SWARM_DIFFERENCES]
                    [--swarm-fastidious]

    micca otu assigns similar sequences (marker genes such as 16S rRNA and
    the fungal ITS region) to operational taxonomic units (OTUs).

    Trimming the sequences to a fixed position before clustering is
    *strongly recommended* when they cover partial amplicons or if quality
    deteriorates towards the end (common when you have long amplicons and
    single-end sequencing).

    Removing ambiguous nucleotides 'N' (with the option --maxns 0 in micca
    filter) is mandatory if you use the de novo swarm clustering method.

    micca otu provides the following protocols:

    * de novo greedy clustering (denovo_greedy): sequences are clustered
    without relying on an external reference database, using an
    approach similar to the UPARSE pipeline (doi: 10.1038/nmeth.2604):
    i) predict sequence abundances of each sequence by dereplication; ii)
    greedy clustering; iii) remove chimeric sequences (de novo, optional)
    from the representatives; iv) map sequences to the representatives.

    * de novo swarm (denovo_swarm): sequences are clustered without relying
    on an external reference database, using swarm (doi:
    10.7717/peerj.593, doi: 10.7717/peerj.1420,
    https://github.com/torognes/swarm): i) predict sequence abundances of
    each sequence by dereplication; ii) swarm clustering; iii) remove
    chimeric sequences (de novo, optional) from the representatives.

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

    * otuids.txt: OTU ids to original sequence ids (tab-delimited text file)

    * hits.txt: three-columns, TAB-separated file:

    1. matching sequence
    2. representative (seed)
    3. identity (if available, else '*'), defined as:

                matching columns
        -------------------------------- ;
        alignment length - terminal gaps

    * otuschim.fasta (only for 'denovo_greedy', 'denovo_swarm' and
    'open_ref' when --rmchim is specified): FASTA file containing the
    chimeric otus;

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input fasta file (required).
    -o DIR, --output DIR  output directory (default .).
    -r FILE, --ref FILE   reference sequences in fasta format, required for
                            'closed_ref' and 'open_ref' clustering methods.
    -m {denovo_greedy,denovo_swarm,closed_ref,open_ref}, --method {denovo_greedy,denovo_swarm,closed_ref,open_ref}
                            clustering method (default denovo_greedy)
    -d ID, --id ID        sequence identity threshold (for 'denovo_greedy',
                            'closed_ref' and 'open_ref', 0.0 to 1.0, default
                            0.97).
    -n MINCOV, --mincov MINCOV
                            reject sequence if the fraction of alignment to the
                            reference sequence is lower than MINCOV. This
                            parameter prevents low-coverage alignments at the end
                            of the sequences (for 'closed_ref' and 'open_ref'
                            clustering methods, default 0.75).
    -t THREADS, --threads THREADS
                            number of threads to use (1 to 256, default 1).
    -c, --rmchim          remove chimeric sequences (for 'denovo_greedy',
                            'denovo_swarm' and 'open_ref' OTU picking methods).
    -g {dgc,agc}, --greedy {dgc,agc}
                            greedy clustering strategy, distance (DGC) or
                            abundance-based (AGC) (for 'denovo_greedy' and
                            'open_ref' clustering methods) (default dgc).
    -s MINSIZE, --minsize MINSIZE
                            discard sequences with an abundance value smaller than
                            MINSIZE after dereplication (>=1, default 2).
                            Recommended value is 2 (i.e. discard singletons) for
                            'denovo_greedy' and 'open_ref', 1 (do not discard
                            anything) for 'denovo_swarm'.
    -a {both,plus}, --strand {both,plus}
                            search both strands or the plus strand only (for
                            'closed_ref' and 'open_ref' clustering methods,
                            default both).

    Swarm specific options:
    --swarm-differences SWARM_DIFFERENCES
                            maximum number of differences allowed between two
                            amplicons. Commonly used d values are 1 (linear
                            complexity algorithm), 2 or 3, rarely higher. (>=0,
                            default 1).
    --swarm-fastidious    when working with SWARM_DIFFERENCES=1, perform a
                            second clustering pass to reduce the number of small
                            OTUs (recommended option).

    Examples

    De novo clustering with a 97% similarity threshold and remove
    chimeric OTUs:

        micca otu -i input.fasta --method denovo_greedy --id 0.97 -c

    Open-reference OTU picking protocol with a 97% similarity
    threshold, without removing chimeras in the de novo protocol step
    and using 8 threads:

        micca otu -i input.fasta --method open_ref --threads 8 --id 0.97 \
        --ref greengenes_2013_05/rep_set/97_otus.fasta

    De novo swarm clustering with the protocol suggested by the authors
    using 4 threads (see https://github.com/torognes/swarm and
    https://github.com/torognes/swarm/wiki):

        micca otu -i input.fasta --method denovo_swarm --threads 4 \
        --swarm-fastidious --rmchim --minsize 1
