library(phyloseq)

import_micca = function(otufilename=NULL, taxonomyfilename=NULL,
                        samplefilename=NULL, treefilename=NULL) {
    rank = c("Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species")
    argumentlist = list()
    if (!is.null(otufilename)) {
        otu_frame = read.csv(otufilename, sep="\t", header=T, row.names=1,
            check.names=F, stringsAsFactors=F)
        otu = otu_table(otu_frame, taxa_are_rows=T)
        argumentlist = c(argumentlist, list(otu))
    }
    if (!is.null(taxonomyfilename)) {
        taxa_frame = read.table(taxonomyfilename, sep="\t", header=F,
            check.names=F, stringsAsFactors=F)
        taxa_split = strsplit(taxa_frame[,2], ";")
        names(taxa_split) = taxa_frame[,1]
        taxa = build_tax_table(sapply(taxa_split, parse_taxonomy_default))
        colnames(taxa) = rank[1:dim(taxa)[[2]]]
        argumentlist = c(argumentlist, list(taxa))
    }
    if (!is.null(samplefilename)) {
        sample_frame = read.csv(samplefilename, sep="\t", header=T, row.names=1,
            check.names=F, stringsAsFactors=F)
        sample = sample_data(sample_frame)
        argumentlist = c(argumentlist, list(sample))
    }
    if (!is.null(treefilename)) {
        tree = read_tree(treefilename)
        if (is.null(tree)) {
            warning("treefilename failed import. It will not be included.")
        }
        else {
            argumentlist = c(argumentlist, list(tree))
        }
    }
    
    do.call("phyloseq", argumentlist)
}
