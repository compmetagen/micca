tabletotax
==========

.. code-block:: console

    usage: micca tabletotax [-h] -i FILE -t FILE [-o DIR]

    Given an OTU table and a taxonomy file, micca tabletotax
    creates in the output directory a table for each taxonomic
    level (taxtable1.txt, ..., taxtableN.txt). OTU counts are
    summed together if they have the same taxonomy at the
    considered level.

    The OTU table must be an OTU x sample, TAB-separated OTU table
    file (see 'micca otu'). The taxonomy file must be a
    tab-delimited file where where rows are either in the form
    (see 'micca classify'):

    1. SEQID[TAB]k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__;g__;
    2. SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales;;;
    3. SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales
    4. SEQID[TAB]D_0__Bacteria;D_1__Firmicutes;D_2__Clostridia;D_3__Clostridiales;D_4__;D_5__;

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input OTU table file (required).
    -t FILE, --tax FILE   input taxonomy file (required).
    -o DIR, --output DIR  output directory (default .).

    Examples

        micca tabletotax -i otutable.txt -t tax.txt -o taxtables
