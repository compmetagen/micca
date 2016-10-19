##    Copyright 2015-2016 Davide Albanese <davide.albanese@gmail.com>
##    Copyright 2015-2016 Fondazione Edmund Mach (FEM)

##    This file is part of micca.
##
##    micca is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    micca is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.

##    You should have received a copy of the GNU General Public License
##    along with micca.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

import sys
import argparse
import textwrap

import micca.api


def main(argv):
    prog = "micca classify"

    description = textwrap.dedent('''\
        micca classify assigns taxonomy for each sequence in the input file
        and provides three methods for classification:

        * VSEARCH-based consensus classifier (cons): input sequences are
          searched in the reference database with VSEARCH
          (https://github.com/torognes/vsearch). For each query sequence the
          method retrives up to 'cons-maxhits' hits (i.e. identity >=
          'cons-id'). Then, the most specific taxonomic label that is
          associated with at least 'cons-minfrac' of the hits is
          assigned. The method is similar to the UCLUST-based consensus
          taxonomy assigner presented in doi: 10.7287/peerj.preprints.934v2
          and available in QIIME.

        * RDP classifier (rdp): only RDP classifier version >= 2.8 is
          supported (doi:10.1128/AEM.00062-07). In order to use this
          classifier RDP must be installed (download at
          http://sourceforge.net/projects/rdp-classifier/files/rdp-classifier/)
          and the RDPPATH environment variable setted. The available
          databases (--rdp-gene) are:

          - 16S (16srrna)
          - Fungal LSU (28S) (fungallsu)
          - Warcup ITS (fungalits_warcup, doi: 10.3852/14-293)
          - UNITE ITS (fungalits_unite)

          For more information about the RDP classifier go to
          http://rdp.cme.msu.edu/classifier/classifier.jsp

        * OTU ID classifier (otuid): simply perform a sequence ID matching
          with the reference taxonomy file. Recommended strategy when the
          closed reference clustering (--method closedref in micca-otu) was
          performed. OTU ID classifier requires a tab-delimited file where
          the first column contains the current OTU ids and the second column
          the reference taxonomy ids (see otuids.txt in micca-otu), e.g.:

          REF1[TAB]1110191
          REF2[TAB]1104777
          REF3[TAB]1078527
          ...

        The input reference taxonomy file (--ref-tax) should be a
        tab-delimited file where rows are either in the form:

        1. SEQID[TAB]k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__;g__;
        2. SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales;;;
        3. SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales
        4. SEQID[TAB]D_0__Bacteria;D_1__Firmicutes;D_2__Clostridia;D_3__Clostridiales;D_4__;D_5__;

        Compatible reference database are Greengenes
        (http://greengenes.secondgenome.com/downloads), QIIME-formatted SILVA
        (https://www.arb-silva.de/download/archive/qiime/) and UNITE
        (https://unite.ut.ee/repository.php).

        The output file is a tab-delimited file where each row is in the
        format:

        SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales
    ''')

    epilog = textwrap.dedent('''\
        Examples

        Classification of 16S sequences using the consensus classifier and
        Greengenes:

            micca classify -m cons -i input.fasta -o tax.txt \\
            --ref greengenes_2013_05/rep_set/97_otus.fasta \\
            --ref-tax greengenes_2013_05/taxonomy/97_otu_taxonomy.txt

        Classification of ITS sequences using the RDP classifier and the
        UNITE database:

            micca classify -m rdp --rdp-gene fungalits_unite -i input.fasta \\
            -o tax.txt

        OTU ID matching after the closed reference OTU picking protocol:

            micca classify -m otuid -i otuids.txt -o tax.txt \\
            --ref-tax greengenes_2013_05/taxonomy/97_otu_taxonomy.txt
    ''')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=prog,
        description=description,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', metavar="FILE", required=True,
                       help="input FASTA file (for 'cons' and 'rdp') or a "
                       "tab-delimited OTU ids file (for 'otuid') (required).")
    group.add_argument('-o', '--output', metavar="FILE", required=True,
                       help="output taxonomy file (required).")
    group.add_argument('-m', '--method', default="cons",
                       choices=["cons", "rdp", "otuid"],
                       help="classification method (default %(default)s)")
    group.add_argument('-r', '--ref', metavar="FILE",
                       help="reference sequences in FASTA format, required "
                       "for 'cons' classifier.")
    group.add_argument('-x', '--ref-tax', metavar="FILE",
                       help="tab-separated reference taxonomy file, required "
                       "for 'cons' and 'otuid' classifiers.")

    # VSEARCH-based consensus classifier
    group_cons = parser.add_argument_group("VSEARCH-based consensus classifier"
                                           "specific options")
    group_cons.add_argument('--cons-id', default=0.9, type=float,
                            help="sequence identity threshold (0.0 to 1.0, "
                            "default %(default)s).")
    group_cons.add_argument('--cons-maxhits', default=3, type=int,
                            help="number of hits to consider (>=1, default "
                            "%(default)s).")
    group_cons.add_argument('--cons-minfrac', default=0.5, type=float,
                            help="for each taxonomic rank, a specific taxa "
                            "will be assigned if it is present in at least "
                            "MINFRAC of the hits (0.0 to 1.0, default "
                            "%(default)s).")
    group_cons.add_argument('--cons-mincov', default=0.75, type=float,
                            help="reject sequence if the fraction of alignment "
                            "to the reference sequence is lower than MINCOV. "
                            "This parameter prevents low-coverage alignments at "
                            "the end of the sequences (default %(default)s).")
    group_cons.add_argument('--cons-strand', default="both",
                            choices=["both", "plus"],
                            help="search both strands or the plus strand only "
                            "(default %(default)s).")
    group_cons.add_argument('--cons-threads', metavar='THREADS', default=1,
                            type=int,
                            help="number of threads to use (1 to 256, default "
                            "%(default)s).")

    # RDP Classifier/Database
    group_rdp = parser.add_argument_group("RDP Classifier/Database specific "
                                          "options")
    group_rdp.add_argument('--rdp-gene', default="16srrna",
                           choices=["16srrna", "fungallsu", "fungalits_warcup",
                                    "fungalits_unite"],
                           help="marker gene/region")
    group_rdp.add_argument('--rdp-maxmem', metavar='GB', default=2, type=int,
                           help="maximum memory size for the java virtual "
                                "machine in GB (default %(default)s)")
    group_rdp.add_argument('--rdp-minconf', type=float, default=0.8,
                           help="minimum confidence value to assign taxonomy "
                                "to a sequence (default %(default)s)")
    args = parser.parse_args(argv)


    if (args.method == "cons") and (args.ref is None):
        parser.error("cons classifier requires a reference file (--ref)")

    if (args.method in ["cons", "otuid"]) and (args.ref_tax is None):
        parser.error("{0} classifier requires a reference taxonomy file "
                     "(--ref-tax)".format(args.method))

    try:
        if args.method == "cons":
            micca.api.classify.cons(
                input_fn=args.input,
                ref_fn=args.ref,
                ref_tax_fn=args.ref_tax,
                output_fn=args.output,
                ident=args.cons_id,
                maxhits=args.cons_maxhits,
                minfrac=args.cons_minfrac,
                threads=args.cons_threads,
                mincov=args.cons_mincov,
                strand=args.cons_strand)

        elif args.method == "rdp":
            micca.api.classify.rdp(
                input_fn=args.input,
                output_fn=args.output,
                gene=args.rdp_gene,
                maxmem=args.rdp_maxmem,
                minconf=args.rdp_minconf)

        else:
            micca.api.classify.otuid(
                input_fn=args.input,
                ref_tax_fn=args.ref_tax,
                output_fn=args.output)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
