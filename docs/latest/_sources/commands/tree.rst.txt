tree
====

.. code-block:: console

    usage: micca tree [-h] -i FILE -o FILE [-m {fasttree,muscle}] [--fasttree-gtr]
                    [--fasttree-fastest]
                    [--muscle-cluster {upgmb,upgma,neighborjoining}]

    micca tree infers phylogenetic trees from alignments. It provides two
    methods:

    * FastTree (doi: 10.1371/journal.pone.0009490);
    * MUSCLE (doi: 10.1093/nar/gkl244).

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input FASTA file (required).
    -o FILE, --output FILE
                            output tree in Newick format (required).
    -m {fasttree,muscle}, --method {fasttree,muscle}
                            tree inference method (default fasttree).

    FastTree specific options:
    --fasttree-gtr        use the generalized time-reversible (GTR)+CAT model
                            instead of Jukes-Cantor+CAT (default False).
    --fasttree-fastest    speed up the neighbor joining phase and reduce memory
                            usage recommended for >50,000 sequences) (default
                            False).

    MUSCLE specific options:
    --muscle-cluster {upgmb,upgma,neighborjoining}
                            clustering algorithm (default upgmb).

    Examples

    Tree inference using FastTree and the generalized time-reversible
    (GTR)+CAT model:

        micca tree -i input.fasta -o tree.tree --fasttree-gtr

