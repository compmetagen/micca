Importing micca outputs in R and ``phyloseq``
=============================================

``phyloseq`` is a popular R package for the analysis and visualization
of microbial data, but it does not have an official support for
``micca`` outputs.

From the `phyloseq <http://joey711.github.io/phyloseq/>`_ homepage:
| The phyloseq package is a tool to import, store, analyze, and
| graphically display complex phylogenetic sequencing data that has
| already been clustered into Operational Taxonomic Units (OTUs),
| especially when there is associated sample data, phylogenetic tree,
| and/or taxonomic assignment of the OTUs."


In order to import ``micca`` outputs in ``phyloseq``, you have to
define the following function or import the file ``R/micca2ps.R``.

.. literalinclude:: ../../../R/micca2ps.R
    :language: r

Now, you can import ``micca`` outputs defined in :doc:`16S`:
   
.. code-block:: r
    
    library(phyloseq)
    source("micca2ps.R")
    ps = import_micca(otufilename="otu_rdp/otu_table.txt",
                      taxonomyfilename="otu_rdp/taxonomy.txt", 
    		      treefilename="phylo_pynast/tree_rooted.tre")
