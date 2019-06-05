library("phyloseq")
library("ggplot2")
library("vegan")
library("DESeq2")

setwd("denovo_greedy_otus") # set the working directory as necessary

ps = import_biom("tables.biom", treefilename="tree_rooted.tree", refseqfilename="otus.fasta")
sample_data(ps)$Month <- as.numeric(sample_data(ps)$Month)
ps

sample_data(ps)

rarecurve(t(otu_table(ps)), step=50, cex=0.5)
ps.rarefied = rarefy_even_depth(ps, rngseed=1, sample.size=0.9*min(sample_sums(ps)), replace=F)

# Ex #############################################
plot(sample_sums(ps))
plot(sample_sums(ps.rarefied))
##################################################

plot_bar(ps.rarefied, fill="Rank2")
plot_bar(ps.rarefied, fill="Rank2") + facet_wrap(~Season, scales="free_x", nrow=1)

ps.phylum = tax_glom(ps.rarefied, taxrank="Rank2", NArm=FALSE)
ps.phylum

plot_bar(ps.phylum, fill="Rank2") + facet_wrap(~Season, scales= "free_x", nrow=1)

# Ex #############################################
ps.class = tax_glom(ps.rarefied, taxrank="Rank3", NArm=FALSE)
plot_bar(ps.class, fill="Rank3") + facet_wrap(~Season, scales= "free_x", nrow=1)
##################################################

plot_richness(ps.rarefied, x="Month", color="Depth", measures=c("Observed"))

plot_richness(ps.rarefied, x="Season", measures=c("Observed", "Shannon")) + geom_boxplot()

rich = estimate_richness(ps.rarefied)
rich

pairwise.wilcox.test(rich$Observed, sample_data(ps.rarefied)$Season)

# Ex #############################################
pairwise.wilcox.test(rich$Shannon, sample_data(ps.rarefied)$Season)
##################################################

wunifrac_dist = phyloseq::distance(ps.rarefied, method="unifrac", weighted=F)
ordination = ordinate(ps.rarefied, method="PCoA", distance=wunifrac_dist)
plot_ordination(ps.rarefied, ordination, color="Season") + theme(aspect.ratio=1)

adonis(wunifrac_dist ~ sample_data(ps.rarefied)$Season)

# Ex #############################################
bray_diss = phyloseq::distance(ps.rarefied, method="bray")
ordination = ordinate(ps.rarefied, method="PCoA", distance=bray_diss)
plot_ordination(ps.rarefied, ordination, color="Season") + theme(aspect.ratio=1)
adonis(bray_diss ~ sample_data(ps.rarefied)$Season)
##################################################

sample_data(ps)$Season <- as.factor(sample_data(ps)$Season)
ds = phyloseq_to_deseq2(ps, ~ Season)
ds = DESeq(ds)

alpha = 0.01
res = results(ds, contrast=c("Season", "Spring", "Fall"), alpha=alpha)
res = res[order(res$padj, na.last=NA), ]
res_sig = res[(res$padj < alpha), ]
res_sig

res_sig = cbind(as(res_sig, "data.frame"), as(tax_table(ps)[rownames(res_sig), ], "matrix"))
ggplot(res_sig, aes(x=Rank6, y=log2FoldChange, color=Rank2)) + 
  geom_jitter(size=3, width = 0.2) + 
  theme(axis.text.x = element_text(angle = -90, hjust = 0, vjust=0.5))

# Ex #############################################
res_summer = results(ds, contrast=c("Season", "Summer", "Fall"), alpha=alpha)
res_summer = res_summer[order(res_summer$padj, na.last=NA), ]
res_summer_sig = res_summer[(res_summer$padj < alpha), ]
res_summer_sig = cbind(as(res_summer_sig, "data.frame"), as(tax_table(ps)[rownames(res_summer_sig), ], "matrix"))
res_sig$test = "Spring vs. Fall"
res_summer_sig$test = "Summer vs. Fall"
res_merged_sig = rbind(res_sig, res_summer_sig)
ggplot(res_merged_sig, aes(x=Rank6, y=log2FoldChange, color=Rank2)) + 
  geom_jitter(size=3, width = 0.2) + 
  facet_wrap(~ test, ncol = 1) +
  theme(axis.text.x = element_text(angle = -90, hjust = 0, vjust=0.5))
##################################################
