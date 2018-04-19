Picking OTUs for use in PICRUSt
===============================

`PICRUSt <http://picrust.github.io/picrust/>`_ (doi: 10.1038/nbt.2676) is a
software designed to predict metagenome functional content from marker gene
(e.g., 16S rRNA) surveys and full genomes. This tutorial covers how to pick OTUs
from 16S rRNA sequences data to use with PICRUSt.

.. Note::

   Requires :ref:`singleend-quality_filtering` in :doc:`singleend` to
   be done and the PICRUSt software to be installed in your system.
   Warning: PICRUSt 1.0.0 requires the biom-format package v1.3.1 to
   be installed in your system (from the command line run: ``pip
   install biom-format==1.3.1``, for more information see
   http://biom-format.org/).

PICRUSt requires an :ref:`otu-closed_reference` OTU table computed against the
Greengenes reference (clustered at 97% identity). Download the reference
database (Greengenes, version 2013/05), clustered at 97% identity:

.. code-block:: sh

   wget ftp://ftp.fmach.it/metagenomics/micca/dbs/gg_2013_05.tar.gz
   tar -zxvf gg_2013_05.tar.gz

Run the micca closed-reference protocol:

.. code-block:: sh

   micca otu -m closed_ref -i filtered.fasta -o closed_ref_otus -r 97_otus.fasta -d 0.97 -t 4
   cd closed_ref_otus

Report the sample summary:

.. code-block:: sh 

   micca tablestats -i otutable.txt -o tablestats
   head tablestats/tablestats_samplesumm.txt

   Sample	Depth	NOTU	NSingle
   Mw_03	1084	132	39
   Mw_06	1387	122	27
   Mw_11	1485	155	44
   Mw_07	1528	150	36
   Mw_01	1537	143	35
   Mw_15	1565	144	35
   Mw_14	1610	149	42
   Mw_02	1670	143	43
   Mw_12	1710	153	54

Rarefy the OTU table for the PICRUSt analysis is always a good idea (see
https://groups.google.com/forum/#!topic/picrust-users/ev5uZGUIPrQ), so we will
rarefy the table at 1084 sequences per sample using :doc:`commands/tablerare`:

.. code-block:: sh

   micca tablerare -i otutable.txt -o otutable_rare.txt -d 1084

Convert the rarefied OTU table into the BIOM format replacing the OTU IDs with
the original sequence IDs using the :doc:`commands/tobiom` command:

.. code-block:: sh

   micca tobiom -i otutable_rare.txt -o tables.biom -u otuids.txt

Normalize the OTU table by dividing each OTU by the known/predicted 16S copy
number abundance using the PICRUSt script ``normalize_by_copy_number.py``:

.. code-block:: sh

   normalize_by_copy_number.py -i tables.biom -o normalized_otus.biom

Create the final metagenome functional predictions using the PICRUSt script
``predict_metagenomes.py``:

.. code-block:: sh

   predict_metagenomes.py -i normalized_otus.biom -o metagenome_predictions.biom

Now you can analyze the PICRUSt predicted metagenome as described in
http://picrust.github.io/picrust/tutorials/downstream_analysis.html#downstream-analysis-guide.
