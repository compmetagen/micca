An introduction to the downstream analysis with R and phyloseq
==============================================================

In this tutorial we describe what is needed to make some common analysis on the
data processed with micca using `R <https://www.r-project.org/>`_ and `phyloseq
<https://joey711.github.io/phyloseq/>`_. In particular, we will discuss the
following topics:

    - rarefaction;
    - taxonomy and relative abundances;
    - alpha diversity and non-parametric tests;
    - beta diversity and PERMANOVA;
    - differential abuncance test with DESeq2.

.. attention::

   * This tutorial requires :doc:`pairedend_97` to be done.
   
   * The tutorial is tested
   with R 3.5.3, phyloseq 1.26.1, ggplot2 3.1.0, vegan 2.5-4 and DESeq2 1.22.2.

Import data and preparation
---------------------------

We can import the micca processed data (the BIOM file, the phylogenetic tree and
the representative sequences) into the `R <https://www.r-project.org/>`_
environment using the ``import_biom()`` function available in `phyloseq
<https://joey711.github.io/phyloseq/>`_ library.

.. code-block:: R

    > library("phyloseq")
    > library("ggplot2")
    > library("vegan")
    > library("DESeq2")
    > setwd("denovo_greedy_otus") # set the working directory
    > ps = import_biom("tables.biom", treefilename="tree_rooted.tree", refseqfilename="otus.fasta")
    > sample_data(ps)$Month <- as.numeric(sample_data(ps)$Month)
    > ps
    phyloseq-class experiment-level object
    otu_table()   OTU Table:         [ 529 taxa and 34 samples ]
    sample_data() Sample Data:       [ 34 samples by 4 sample variables ]
    tax_table()   Taxonomy Table:    [ 529 taxa by 6 taxonomic ranks ]
    phy_tree()    Phylogenetic Tree: [ 529 tips and 528 internal nodes ]
    refseq()      DNAStringSet:      [ 529 reference sequences ]

The ``import_biom()`` function returns a phyloseq object which includes the OTU
table (which contains the OTU counts for each sample), the sample data matrix
(containing the metadata for each sample), the taxonomy table (the predicted
taxonomy for each OTU), the phylogenetic tree, and the OTU representative
sequences.

At this point, we can plot the rarefaction curves using vegan:

.. code-block:: R

    > rarecurve(t(otu_table(ps)), step=50, cex=0.5)

.. image:: /images/garda_rarecurves.png
    :align: center
    :scale: 95%

Now we can rarefy the samples. Rarefaction is used to simulate even number of
reads per sample. In this example, the rarefaction depth chosen is 90% of the
minimum sample depth in the dataset (459 reads per sample).

.. code-block:: R

    > # rarefy without replacement
    > ps.rarefied = rarefy_even_depth(ps, rngseed=1, sample.size=0.9*min(sample_sums(ps)), replace=F)

.. attention::

    * Rarefaction can waste a lot of data and would not be necessary. See
      https://doi.org/10.1371/journal.pcbi.1003531.

    * Remember to set the random seed (``rngseed``) for repeatable experiments.


.. admonition:: Exercise

    Plot the samples depths histogram before and after the rarefaction using the
    phyloseq function ``sample_sums()``.


Plot abundances
---------------

Using the rarefied dataset, plot the abundances and color each OTU according its
classified phylum (in this case ``Rank2``):

.. code-block:: R

    > plot_bar(ps.rarefied, fill="Rank2") + facet_wrap(~Season, scales = "free_x", nrow = 1)

.. image:: /images/garda_bar.png
    :align: center
    :scale: 75%

Alternatively, we can merge the OTU at the phylum level and build a new phyloseq
object:

.. code-block:: R

    > ps.phylum = tax_glom(ps.rarefied, taxrank = "Rank2", NArm = F)
    > ps.phylum
    phyloseq-class experiment-level object
    otu_table()   OTU Table:         [ 35 taxa and 34 samples ]
    sample_data() Sample Data:       [ 34 samples by 4 sample variables ]
    tax_table()   Taxonomy Table:    [ 35 taxa by 6 taxonomic ranks ]
    phy_tree()    Phylogenetic Tree: [ 35 tips and 34 internal nodes ]
    refseq()      DNAStringSet:      [ 35 reference sequences ]

Now we can make the new bar plot at the class level:

.. code-block:: R

    > plot_bar(ps.phylum, fill="Rank2") + facet_wrap(~Season, scales = "free_x", nrow = 1)

Alpha diversity
---------------

Now we can plot the number of observed OTUs in each month, coloring the values
according to the sampling depth:

.. code-block:: R

    > plot_richness(ps.rarefied, x="Month", color="Depth", measures=c("Observed"))

.. image:: /images/garda_alpha.png
    :align: center
    :scale: 75%

Moreover, we can make a boxplot of the number of OTUs and the Shannon entropy 
grouping the different months by season:

.. code-block:: R

    > plot_richness(ps.rarefied, x="Season", measures=c("Observed", "Shannon")) + geom_boxplot()

.. image:: /images/garda_alpha2.png
    :align: center
    :scale: 75%

Beta diversity
--------------

Now, we can plot the PCoA using the unweighted UniFrac as distance:

.. code-block:: R

    > # PCoA plot using the unweighted UniFrac as distance
    > wunifrac_dist = distance(ps.rarefied, method="unifrac", weighted=F)
    > ordination = ordinate(ps.rarefied, method="PCoA", distance=wunifrac_dist)
    > plot_ordination(ps.rarefied, ordination, color="Season") + theme(aspect.ratio=1)

.. image:: /images/garda_beta.png
    :align: center
    :scale: 75%

At this point, we test whether the seasons differ significantly from each other
using the permutational ANOVA (PERMANOVA) analysis:

.. code-block:: R

    > adonis(wunifrac_dist~sample_data(ps.rarefied)$Season)
    
    Call:
    adonis(formula = wunifrac_dist ~ sample_data(ps.rarefied)$Season) 

    Permutation: free
    Number of permutations: 999

    Terms added sequentially (first to last)

                                    Df SumsOfSqs  MeanSqs F.Model     R2 Pr(>F)    
    sample_data(ps.rarefied)$Season  3    0.6833 0.227765  4.3451 0.3029  0.001 ***
    Residuals                       30    1.5726 0.052419         0.6971           
    Total                           33    2.2559                  1.0000           
    ---
    Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1