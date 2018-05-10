``micca-otu-denovo``
====================

Performs the OTU clustering the taxonomy assigment. Reads are
clustered without any external reference. The output directory will contain
the following:

**clusters.txt**
    a tab-delimited file where each row contains the sequence
    identifiers assigned to the cluster. The first id corresponds to a
    representative sequence. Sequence identifiers are coded as
    ``SAMPLE_NAME||SEQ_ID``::

        sample1||F4HTPAO07H4B1Q sample1||F4HTPAO07ILHKH sample1||F4HTPAO07H8VJE  ...
        sample3||F4HTPAO05FO0LC sample2||F4HTPAO02BVI74 sample3||F4HTPAO05FQCOF ...
        ...

**otu_table.txt**
    a tab-delimited file containing the number of times an OTU is
    found in each sample. The first column contains the representative
    sequence id::

        OTU                     sample1 sample2 sample3
        sample1||F4HTPAO07H4B1Q 12      5       4
        sample3||F4HTPAO05FO0LC 2       6       6
        ...

**representatives.fasta**
    a FASTA file containing the representative sequence for each OTU::
    
        >sample1||F4HTPAO07H4B1Q
	GTCCACGCCGTAAACGGTGGATGCTGGATGTGGGGCCCGTTCCACGGGTTCCGTGTCGGA
	GCTAACGCGTTAAGCATCCCGCCTGGGGAGTACGGCCGCAAGGCTAAAACTCAAAGAAAT
	TGACGGGGCCCGCACAAGCGGCGGAGCATGCGGATTAATTCGATGCAACGCGAAGAACCT
	TACCTGGGCTTGACATGTTCCCGACGGTCGTAGAGATACGGCTTCCCTTCGGGGCGGGTT
	CACAGGTGGTGCATGGTC
	>sample3||F4HTPAO05FO0LC
	GTCCACGCCGTAAACGATGAATACTAGGTGTTGGGAAGCATTGCTTCTCGGTGCCGTCGC
	AAACGCAGTAAGTATTCCACCTGGGGAGTACGTTCGCAAGAATGAAACTCAAAGGAATTG
	ACGGGGACCCGCACAAGCGGTGGAGCATGTGGTTTAATTCGAAGCAACGCGAAGAACCTT
	ACCAAGTCTTGACATCCTTCTGACCGGTACTTAACCGTACCTTCTCTTCGGAGCAGGAGT
	GACAGGTGGTGCATGGTT
	...

**taxonomy.txt**
    a two-columns, tab-delimited file containing the taxonomy assigned
    to each OTU::

        sample1||F4HTPAO07H4B1Q	Bacteria;Actinobacteria;Actinobact...
        sample3||F4HTPAO05FO0LC	Bacteria;Firmicutes;Clostridia;Clost...
        ...

**otu.log**
    the log file.

.. command-output:: micca-otu-denovo --help
