OTUCLUST
========

OTUCLUST is a new open-source application specifically created to
divide a set of amplicon reads into clusters. Given an identity
threshold (e.g. 97%), a cluster is defined by a centroid
(i.e. representative sequence ) and by the sequences which have
similarity above the threshold with the representative. OTUCLUST is
the default clustering method used in
:doc:`command_ref/micca_otu_denovo`.

Definition of pair-wise identity
--------------------------------

Different definitions of pair-wise identity are used by different
clustering software. There is no general consensus of how internal
gaps should be treated in this calculation. In OTUCLUST internal and
external gaps are ignored [Hwang2013]_. Given a global alignment (GA),
between the sequences :math:`i` and :math:`j` the pair-wise identity
is defined as:

.. math::
      
    s^{\text{GA}}_{i, j} = \left[\frac{\text{\# of matches}}{\text{\# of matches} +
        \text{\# of mismatches}} \text{of the GA}_{i,j}\right]

where mismatch and gap penalties equal to one.

OTUCLUST algorithm overview
---------------------------

The OTUCLUST procedure is composed by three main steps: `a)`
dereplication and abundance estimation, `b)` denovo chimera removal
(optional, with UCHIME) and `c)` clustering using the dereplicated
sequences as centroids.

.. figure:: ../images/otuclust.png
      :align: center

Dereplication and chimera removal (optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal of the dereplication is the removal of duplicate
sequences. This step is performed by the clustering procedure
(described below) with an identity threshold of 100% or by exact
prefix matching (faster dereplication). At the end of the
dereplication step, singletons are discarded. Abundance is estimated
by counting the number of reads having a given unique sequence.
Dereplicated sequences are ordered by their abundance and passed to
UCHIME (denovo mode). Reads detected as chimeras are removed.

Clustering
^^^^^^^^^^

Finally, dereplicated and chimera-free sequences are used as cluster
seeds by the clustering algorithm. The clustering procedure relies on
a **search algorithm** defined as follows:

1. given a query sequence :math:`Q`, the sequence database is sorted by
   decreasing k-mer similarity. The k-mer similarity is defined as
   [Hwang2013]_:
   
   .. math::

       s^{\text{k-mer}}_{i, j} = \frac{\sum_\tau \min(n_i(\tau),
           n_j(\tau))}{\min(l_i, l_j)-k+1} 

   where :math:`\tau` is a k-mer, :math:`n` is the number of
   occurences of the k-mer in the sequences and :math:`l_i, l_j` are
   the lenght of sequences :math:`i` and :math:`j` respectively.

2. For each sequence in the sorted database (target sequence,
   :math:`T`) the similarity :math:`s^{\text{GA}}_{Q, T}` is
   computed. If :math:`s^{\text{GA}}_{Q, T}` is greater or equal than
   the identity threshold :math:`s^{\text{thr}}` (e.g. 0.97) the
   sequence :math:`Q` is added to the results and the reject counter
   :math:`n_{rej}` is set to zero. On the other hand :math:`n_{rej}`
   is incremented by one.

3. If :math:`n_{rej}` reaches the maximum number of consecutive
   rejects allowed :math:`m` (e.g. 32) it is rather unlikely that an
   other hit exist.

Given a query sequence Q and the sequence database, the clustering
procedure searches (through the search algorithm) all the sequences in
the DB that have similarity above the identity threshold, forming a
new cluster. After that these sequences are removed from the sequence
database.

OTUCLUST application
--------------------

.. command-output:: otuclust --help

Outputs:

**clust.txt**
    a tab-delimited file where each row contains the sequence
    identifiers assigned to the cluster. The first id corresponds to a
    representative sequence. Sequence identifiers are coded as
    ``SAMPLE_NAME||SEQ_ID``::

        sample1||F4HTPAO07H4B1Q sample1||F4HTPAO07ILHKH sample1||F4HTPAO07H8VJE  ...
        sample3||F4HTPAO05FO0LC sample2||F4HTPAO02BVI74 sample3||F4HTPAO05FQCOF ...
        ...

**rep.fasta**
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


.. [Hwang2013] Hwang et al. CLUSTOM: A Novel Method for Clustering 16S
               rRNA Next Generation Sequences by Overlap Minimization.
	       PLoS ONE, 2013.
