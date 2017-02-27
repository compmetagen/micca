tablerare
=========

.. code-block:: console

    usage: micca tablerare [-h] -i FILE -o FILE -d DEPTH [-r] [-s SEED]

    Rarefy an OTU table by subsampling, with or without
    replacement. Samples that have fewer counts then the depth are
    omitted from the output table. OTUs that are not present in at
    least one sample are omitted from the output table.

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input OTU table file (required).
    -o FILE, --output FILE
                            output rarefied OTU table file (required).
    -d DEPTH, --depth DEPTH
                            sample depth (>0, required).
    -r, --replace         subsample with replacement.
    -s SEED, --seed SEED  random seed (default 0).

    Examples

    Rarefy an OTU table at a depth of 1000 sequences/sample:

        micca tablerare -i otutable.txt -o otutable_rare.txt -d 1000
