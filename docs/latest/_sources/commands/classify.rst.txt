classify
========

.. code-block:: console

    usage: micca classify [-h] -i FILE -o FILE [-m {cons,rdp,otuid}] [-r FILE]
                        [-x FILE] [--cons-id CONS_ID]
                        [--cons-maxhits CONS_MAXHITS]
                        [--cons-minfrac CONS_MINFRAC]
                        [--cons-mincov CONS_MINCOV] [--cons-strand {both,plus}]
                        [--cons-threads THREADS]
                        [--rdp-gene {16srrna,fungallsu,fungalits_warcup,fungalits_unite}]
                        [--rdp-maxmem GB] [--rdp-minconf RDP_MINCONF]

    micca classify assigns taxonomy for each sequence in the input file
    and provides three methods for classification:

    * VSEARCH-based consensus classifier (cons): input sequences are
    searched in the reference database with VSEARCH
    (https://github.com/torognes/vsearch). For each query sequence the
    method retrives up to 'cons-maxhits' hits (i.e. identity >=
    'cons-id'). Then, the most specific taxonomic label that is
    associated with at least 'cons-minfrac' of the hits is
    assigned. The method is similar to the UCLUST-based consensus
    taxonomy assigner presented in doi: 10.7287/peerj.preprints.934v2
    and available in QIIME.

    * RDP classifier (rdp): only RDP classifier version >= 2.8 is
    supported (doi:10.1128/AEM.00062-07). In order to use this
    classifier RDP must be installed (download at
    http://sourceforge.net/projects/rdp-classifier/files/rdp-classifier/)
    and the RDPPATH environment variable setted. The available
    databases (--rdp-gene) are:

    - 16S (16srrna)
    - Fungal LSU (28S) (fungallsu)
    - Warcup ITS (fungalits_warcup, doi: 10.3852/14-293)
    - UNITE ITS (fungalits_unite)

    For more information about the RDP classifier go to
    http://rdp.cme.msu.edu/classifier/classifier.jsp

    * OTU ID classifier (otuid): simply perform a sequence ID matching
    with the reference taxonomy file. Recommended strategy when the
    closed reference clustering (--method closedref in micca-otu) was
    performed. OTU ID classifier requires a tab-delimited file where
    the first column contains the current OTU ids and the second column
    the reference taxonomy ids (see otuids.txt in micca-otu), e.g.:

    REF1[TAB]1110191
    REF2[TAB]1104777
    REF3[TAB]1078527
    ...

    The input reference taxonomy file (--ref-tax) should be a
    tab-delimited file where rows are either in the form:

    1. SEQID[TAB]k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__;g__;
    2. SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales;;;
    3. SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales
    4. SEQID[TAB]D_0__Bacteria;D_1__Firmicutes;D_2__Clostridia;D_3__Clostridiales;D_4__;D_5__;

    Compatible reference database are Greengenes
    (http://greengenes.secondgenome.com/downloads), QIIME-formatted SILVA
    (https://www.arb-silva.de/download/archive/qiime/) and UNITE
    (https://unite.ut.ee/repository.php).

    The output file is a tab-delimited file where each row is in the
    format:

    SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input FASTA file (for 'cons' and 'rdp') or a tab-
                            delimited OTU ids file (for 'otuid') (required).
    -o FILE, --output FILE
                            output taxonomy file (required).
    -m {cons,rdp,otuid}, --method {cons,rdp,otuid}
                            classification method (default cons)
    -r FILE, --ref FILE   reference sequences in FASTA format, required for
                            'cons' classifier.
    -x FILE, --ref-tax FILE
                            tab-separated reference taxonomy file, required for
                            'cons' and 'otuid' classifiers.

    VSEARCH-based consensus classifierspecific options:
    --cons-id CONS_ID     sequence identity threshold (0.0 to 1.0, default 0.9).
    --cons-maxhits CONS_MAXHITS
                            number of hits to consider (>=1, default 3).
    --cons-minfrac CONS_MINFRAC
                            for each taxonomic rank, a specific taxa will be
                            assigned if it is present in at least MINFRAC of the
                            hits (0.0 to 1.0, default 0.5).
    --cons-mincov CONS_MINCOV
                            reject sequence if the fraction of alignment to the
                            reference sequence is lower than MINCOV. This
                            parameter prevents low-coverage alignments at the end
                            of the sequences (default 0.75).
    --cons-strand {both,plus}
                            search both strands or the plus strand only (default
                            both).
    --cons-threads THREADS
                            number of threads to use (1 to 256, default 1).

    RDP Classifier/Database specific options:
    --rdp-gene {16srrna,fungallsu,fungalits_warcup,fungalits_unite}
                            marker gene/region
    --rdp-maxmem GB       maximum memory size for the java virtual machine in GB
                            (default 2)
    --rdp-minconf RDP_MINCONF
                            minimum confidence value to assign taxonomy to a
                            sequence (default 0.8)

    Examples

    Classification of 16S sequences using the consensus classifier and
    Greengenes:

        micca classify -m cons -i input.fasta -o tax.txt \
        --ref greengenes_2013_05/rep_set/97_otus.fasta \
        --ref-tax greengenes_2013_05/taxonomy/97_otu_taxonomy.txt

    Classification of ITS sequences using the RDP classifier and the
    UNITE database:

        micca classify -m rdp --rdp-gene fungalits_unite -i input.fasta \
        -o tax.txt

    OTU ID matching after the closed reference OTU picking protocol:

        micca classify -m otuid -i otuids.txt -o tax.txt \
        --ref-tax greengenes_2013_05/taxonomy/97_otu_taxonomy.txt
