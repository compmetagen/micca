Run micca in 6 steps
====================

Open a terminal, download the sample data and prepare the working
directory:

.. code-block:: sh

   wget ftp://ftp.fmach.it/metagenomics/micca/examples/mwanihana.tar.gz
   tar -zxvf mwanihana.tar.gz
   cd mwanihana

Now we can run micca:

.. code-block:: sh

   # merge the samples
   micca merge -i fastq/*.fastq -o merged.fastq
   # trim primers
   micca trim -i merged.fastq -o trimmed.fastq -w AGAGTTTGATCMTGGCTCAG -r GTGCCAGCAGCCGCGGTAA -W
   # filter low quality reads and truncate at 350 bp
   micca filter -i trimmed.fastq -o filtered.fasta -e 0.5 -m 350 -t
   # denovo OTU picking protocol
   micca otu -i filtered.fasta -o denovo_greedy_otus -d 0.97 -c -t 4
   # classify taxonomies using RDP classifier
   micca classify -m rdp -i denovo_greedy_otus/otus.fasta -o denovo_greedy_otus/taxa.txt
   # export the BIOM file
   micca tobiom -i denovo_greedy_otus/otutable.txt -o denovo_greedy_otus/tables.biom -t denovo_greedy_otus/taxa.txt
   
