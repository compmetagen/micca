Compute basic OTU table statistics, rarefy and summarize OTU tables by taxa using micca
=======================================================================================

.. note::

   This tutorial requires :doc:`singleend` to be done.

The command :doc:`commands/tablestats` reports a sample summary, an OTU summary and
the rarefaction curves for the input OTU table:

.. code-block:: sh 

   micca tablestats -i otutable.txt -o tablestats

Inspecting the file ``tablestats/tablestats_samplesumm.txt`` you can
see that the less abundant sample contains 9053 reads::

   Sample Depth NOTU NSingle
   Mw_03  9053  716  142
   Mw_02  9947  760  166
   Mw_12  10843 792  168
   ...    ...  ...   ...

.. note::

   Rarefaction curves can be inspected through
   ``tablestats/tablestats_rarecurve.txt`` and
   ``tablestats/tablestats_rarecurve_plot.png``.

To compare different samples, the OTU table must be subsampled
(`rarefied <https://en.wikipedia.org/wiki/Rarefaction_(ecology)>`_)
using the command :doc:`commands/tablerare`. In this case we are
interested in rarefy the table with the depth of the less abundant
sample (``Mw_03``):

.. code-block:: sh

   micca tablerare -i otutable.txt -o otutable_rare.txt -d 9053

Now we can summarize communities by their taxonomic composition.  The
:doc:`commands/tabletotax` creates in the output directory a table for
each taxonomic level (``taxtable1.txt``, ..., ``taxtableN.txt``). OTU
counts are summed together if they have the same taxonomy at the
considered level.

.. code-block:: sh

   micca tabletotax -i otutable_rare.txt -t taxa.txt -o taxtables

Finally, we can generate a relative abundance bar plot from
generated taxa tables, using the command :doc:`commands/tablebar`. In
this case only the bar plot relative to the taxonomy level 2 (phylum)
will be generated:

.. code-block:: sh
   
   micca tablebar -i taxtables/taxtable2.txt -o taxtables/taxtable2.png

.. image:: /images/taxtable.png
   :align: center
