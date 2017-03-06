root
====

.. code-block:: console

    usage: micca root [-h] -i FILE -o FILE [-m {midpoint,outgroup}]
                    [-t TARGETS [TARGETS ...]]

    micca root reroot the input tree:

    * at the calculated midpoint between the two most distant tips of the
    tree (--method midpoint);

    * with the outgroup clade containing the given taxa (leaf nodes),
    i.e. the common ancestor of the outgroup (--method outgroup).

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input FASTA file (required).
    -o FILE, --output FILE
                            output MSA file in FASTA format (required).
    -m {midpoint,outgroup}, --method {midpoint,outgroup}
                            rooting method (default midpoint).
    -t TARGETS [TARGETS ...], --targets TARGETS [TARGETS ...]
                            list of targets defining the outgroup (required for
                            the outgroup method).

    Examples

    Midpoint rooting:

        micca root -i input.tree -o input_rooted.tree

    Rooting with outgroup:

        micca root -i input.tree -o input_rooted.tree -m outgroup DENOVO1 DENOVO2
