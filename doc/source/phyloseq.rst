An introduction to the downstream analysis with R and phyloseq
==============================================================

.. note::

   This tutorial requires :doc:`pairedend_97` to be done.

.. note::

   This tutorial requires `R <https://www.r-project.org/>`_, `phyloseq
   <https://joey711.github.io/phyloseq/>`_ and ggplot2 (tested on R v3.4. and
   phyloseq v1.22.3) to be installed in your system.

We can import the micca processed data (the BIOM file, the phylogenetic tree and
the representative sequences) into the `R <https://www.r-project.org/>`_
environment using the `phyloseq <https://joey711.github.io/phyloseq/>`_ library.

The ``import_biom()`` function allows to simultaneously import the BIOM
file and an associated phylogenetic tree file and reference sequence
file. 

.. code-block:: R

    > library("phyloseq")
    > library("ggplot2")
    > setwd("denovo_greedy_otus") # set the working directory
    > ps = import_biom("tables.biom", treefilename="tree_rooted.tree",
    + refseqfilename="otus.fasta")
    > sample_data(ps)$Month <- as.numeric(sample_data(ps)$Month)
    > ps
    phyloseq-class experiment-level object
    otu_table()   OTU Table:         [ 529 taxa and 34 samples ]
    sample_data() Sample Data:       [ 34 samples by 4 sample variables ]
    tax_table()   Taxonomy Table:    [ 529 taxa by 6 taxonomic ranks ]
    phy_tree()    Phylogenetic Tree: [ 529 tips and 528 internal nodes ]
    refseq()      DNAStringSet:      [ 529 reference sequences ]

At this point, we can compute the number of OTUs as measure of alpha diversity
after the rarefaction:

.. code-block:: R

    > # rarefy without replacement
    > ps.rarefied = rarefy_even_depth(ps, rngseed=1, sample.size=0.9*min(sample_sums(ps)), replace=F)
    > # plot the number of observed OTUs
    > plot_richness(ps.rarefied, x="Month", color="Depth", measures=c("Observed"))

.. image:: /images/garda_alpha.png
    :align: center
    :scale: 75%

Finnaly, we can plot the PCoA using the unweighted UniFrac as distance:

.. code-block:: R

    > # PCoA plot using the unweighted UniFrac as distance
    > ordination = ordinate(ps.rarefied, method="PCoA", distance="unifrac", weighted=F)
    > plot_ordination(ps.rarefied, ordination, color="Season") + theme(aspect.ratio=1)

.. image:: /images/garda_beta.png
    :align: center
    :scale: 75%
