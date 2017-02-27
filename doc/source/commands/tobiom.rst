tobiom
======

.. code-block:: console

    usage: micca tobiom [-h] -i FILE -o FILE [-t FILE] [-s FILE] [-u FILE]

    micca tobiom converts the micca OTU table into BIOM Version
    1.0 (JSON) format. Optionally, taxonomy and/or sample
    information can be added.  When you convert on
    (closed-reference) OTU table for PICRUSt, replace OTU IDs with
    the original sequence IDs use the option -u/--otuids.

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input OTU table file (required).
    -o FILE, --output FILE
                            output BIOM file Version 1.0 (JSON) (required).
    -t FILE, --tax FILE   add taxonomy information from a taxonomy file.
    -s FILE, --sampledata FILE
                            add sample information from a sample data file.
    -u FILE, --otuids FILE
                            replace OTU IDs with the original sequence IDs. Useful
                            when the closed-reference OTU picking protocol was
                            performed for PICRUSt

    Example

        micca tobiom -i otutable.txt -o output.biom -t tax.txt -s sampledata.txt

