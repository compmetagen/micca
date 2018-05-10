OTU picking in micca
====================

To characterize the taxonomic structure of the samples, the sequences
are organized into `Operational Taxonomic Units (OTUs)
<https://en.wikipedia.org/wiki/Operational_taxonomic_unit>`_ at
varying levels of identity. An identity of **97%** represent the
common working definition of bacterial species. The
:doc:`commands/otu` command assigns similar sequences (marker genes
such as 16S rRNA and the fungal ITS region) to operational taxonomic
units (OTUs). The command :doc:`commands/otu` wraps `VSEARCH
<https://github.com/torognes/vsearch>`_ for low-level clustering,
chimera detection an searching operations.

The :doc:`commands/otu` command returns in a single directory 5 files:

   otutable.txt
      TAB-delimited file, containing the number of times an OTU is
      found in each sample (OTU x sample, see :doc:`formats`)::

         OTU     Mw_01 Mw_02 Mw_03 ...
         DENOVO1 151   178   177   ...
         DENOVO2 339   181   142   ...
         DENOVO3 533   305   63    ...
         ...     ...   ...   ...   ...

   otus.fasta
      FASTA containing the representative sequences (OTUs)::
     
         >DENOVO1
     	 GACGAACGCTGGCGGCGTGCCTAACACATGCAAGTCGAACGGGG...
     	 >DENOVO2
     	 GATGAACGCTAGCTACAGGCTTAACACATGCAAGTCGAGGGGCA...
     	 >DENOVO3
     	 AGTGAACGCTGGCGACGTGGTTAAGACATGCAAGTCGAGCGGTA...
	 ...

   otuids.txt
      TAB-delimited file which maps the OTU ids to original sequence
      ids::
 
         DENOVO1 IS0AYJS04JQKIS;sample=Mw_01
	 DENOVO2 IS0AYJS04JL6RS;sample=Mw_01
	 DENOVO3 IS0AYJS04H4XNN;sample=Mw_01
	 ...

   hits.txt
      TAB-separated file, three-columns, where each column contains:
      the matching sequence, the representative (seed) and the
      identity (if available), see :ref:`otu-definition_identity`::
      
         IS0AYJS04JE658;sample=Mw_01; IS0AYJS04I4XYN;sample=Mw_01 99.4
	 IS0AYJS04JPH34;sample=Mw_01; IS0AYJS04JVUBC;sample=Mw_01 98.0
	 IS0AYJS04I67XN;sample=Mw_01; IS0AYJS04JVUBC;sample=Mw_01 99.7
	 ...
	
   otuschim.fasta 
      (only for 'denovo_greedy' and 'open_ref' mathods, when
      ``-c/--rmchim`` is specified) FASTA file containing the chimeric
      otus.

.. warning::

   Trimming the sequences to a fixed position before clustering is
   strongly recommended when they cover partial amplicons or if
   quality deteriorates towards the end (common when you have long
   amplicons and single-end sequencing), see
   :ref:`singleend-quality_filtering`.

.. note::

   De novo OTUs are renamed to ``DENOVO[N]`` and reference OTUs to
   ``REF[N]``.


Clustering strategies
---------------------

:doc:`commands/otu` implements several state-of-the-art clustering
strategies:

.. contents::
   :local:


.. _otu-de_novo_greedy:

De novo greedy
^^^^^^^^^^^^^^

In denovo greedy clustering (parameter ``--method denovo_greedy``),
sequences are clustered without relying on an external reference
database, using an approach similar to the UPARSE pipeline
(https://doi.org/10.1038/nmeth.2604) and tested in
https://doi.org/10.7287/peerj.preprints.1466v1. :doc:`commands/otu`
includes in a single command dereplication, clustering and chimera
filtering:

   #. Dereplication. Predict sequence abundances of each sequence by
      dereplication, order by abundance and discard sequences with
      abundance value smaller than DEREP_MINSIZE (option
      ``--derep-minsize`` recommended value 2);
       
   #. Greedy clustering. Distance (DGC) and abundance-based (AGC)
      strategies are supported (option ``--greedy``, see
      https://doi.org/10.1186/s40168-015-0081-x and
      https://doi.org/10.7287/peerj.preprints.1466v1 ). Therefore, the
      candidate representative sequences are obtained;

   #. Chimera filtering (optional). Remove chimeric sequences from the
      representatives performing a de novo chimera detection (option
      ``--rmchim``, recommended);

   #. Map sequences. Map sequences to the representatives.

Example (requires :ref:`singleend-quality_filtering` in
:doc:`singleend` to be done):

.. code-block:: sh

   micca otu -m denovo_greedy -i filtered.fasta -o denovo_greedy_otus -d 0.97 -c -t 4


.. _otu-closed_reference:

Closed-reference
^^^^^^^^^^^^^^^^

Sequences are clustered against an external reference database and
reads that could not be matched are discarded. Example (requires
:ref:`singleend-quality_filtering` in :doc:`singleend` to be done):

Download the reference database (Greengenes), clustered at 97%
identity:

.. code-block:: sh

   wget ftp://ftp.fmach.it/metagenomics/micca/dbs/gg_2013_05.tar.gz
   tar -zxvf gg_2013_05.tar.gz

Run the closed-reference protocol:

.. code-block:: sh

   micca otu -m closed_ref -i filtered.fasta -o closed_ref_otus -r 97_otus.fasta -d 0.97 -t 4

Simply perform a sequence ID matching with the reference taxonomy
file (see :doc:`commands/classify`):

.. code-block:: sh
   
   cd closed_ref_otus
   micca classify -m otuid -i otuids.txt -o taxa.txt -x ../97_otu_taxonomy.txt


Open-reference
^^^^^^^^^^^^^^

Open-reference clustering (open_ref): sequences are clustered against
an external reference database (as in :ref:`otu-closed_reference`) and
reads that could not be matched are clustered with the
:ref:`otu-de_novo_greedy` protocol. Example (requires
:ref:`singleend-quality_filtering` in :doc:`singleend` to be done):

Download the reference database (Greengenes), clustered at 97%
identity:

.. code-block:: sh

   wget ftp://ftp.fmach.it/metagenomics/micca/dbs/gg_2013_05.tar.gz
   tar -zxvf gg_2013_05.tar.gz

Run the open-reference protocol:

.. code-block:: sh

   micca otu -m open_ref -i filtered.fasta -o open_ref_otus -r 97_otus.fasta -d 0.97 -t 7 -c

Run the VSEARCH-based consensus classifier or the RDP classifier (see
:doc:`commands/classify`):

.. code-block:: sh
   
   cd open_ref_otus
   micca classify -m cons -i otus.fasta -o taxa.txt -r ../97_otus.fasta -x ../97_otu_taxonomy.txt -t 4


De novo swarm
^^^^^^^^^^^^^

.. todo::

   Not yet implemented in micca.


.. _otu-definition_identity:

Definition of identity
----------------------

In micca, the pairwise identity is defined as the edit distance
excluding terminal gaps (same as in USEARCH and BLAST):

.. math::
   \frac{\textrm{\# matching columns}}{\textrm{alignment length} - \textrm{terminal gaps}}
