##    Copyright 2016 Davide Albanese <davide.albanese@gmail.com>
##    Copyright 2016 Fondazione Edmund Mach (FEM)

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
    prog = "micca msa"

    description = textwrap.dedent('''\
        micca msa performs a multiple sequence alignment (MSA) on the input
        file in FASTA format. micca msa provides two approaches for MSA:

        * MUSCLE (doi: 10.1093/nar/gkh340). It is one of the most widely-used
          multiple sequence alignment software;

        * Nearest Alignment Space Termination (NAST) (doi:
          10.1093/nar/gkl244). MICCA provides a very fast and memory
          efficient implementation of the NAST algorithm. The algorithm is
          based on VSEARCH (https://github.com/torognes/vsearch). It requires
          a pre-aligned database of sequences (--nast-template). For 16S
          data, a good template file is the Greengenes Core Set
          (http://greengenes.lbl.gov/Download/Sequence_Data/Fasta_data_files/
          core_set_aligned.fasta.imputed).
          ''')

    epilog = textwrap.dedent('''\
        Examples

        De novo MSA using MUSCLE:

            micca msa -i input.fasta -o msa.fasta

        Template-based MSA using NAST, the Greengenes alignment as
        template (clustered at 97% similarity) 4 threads and a sequence
        identity threshold of 75%:

            micca msa -i input.fasta -o msa.fasta -m nast --nast-threads 4 \\
            --nast-template greengenes_2013_05/rep_set_aligned/97_otus.fasta
        ''')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=prog,
        description=description,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', metavar="FILE", required=True,
                        help="input FASTA file (required).")
    group.add_argument('-o', '--output', metavar='FILE', required=True,
                        help="output MSA file in FASTA format (required).")
    group.add_argument('-m', '--method', default="muscle",
                        choices=["muscle", "nast"],
                        help="multiple sequence alignment method (default "
                        "%(default)s).")

    # MUSCLE options
    group_muscle = parser.add_argument_group("MUSCLE specific options")
    group_muscle.add_argument('--muscle-maxiters', type=int, default=16,
                              help="maximum number of MUSCLE iterations. Set "
                              "to 2 for a good compromise between speed and "
                              "accuracy (>=1 default %(default)s).")

    # NAST options
    group_nast = parser.add_argument_group("NAST specific options")
    group_nast.add_argument('--nast-template', metavar='FILE',
                            help="multiple sequence alignment template file "
                            "in FASTA format.")
    group_nast.add_argument('--nast-id', type=float, default=0.75,
                            help="sequence identity threshold to consider a "
                            "sequence a match (0.0 to 1.0, default "
                            "%(default)s).")
    group_nast.add_argument('--nast-threads', type=int, default=1,
                            help="number of threads to use (1 to 256, default "
                            "%(default)s).")
    group_nast.add_argument('--nast-mincov', default=0.75, type=float,
                            help="reject sequence if the fraction of alignment "
                            "to the template sequence is lower than MINCOV. "
                            "This parameter prevents low-coverage alignments at "
                            "the end of the sequences (default %(default)s).")
    group_nast.add_argument('--nast-strand', default="both",
                            choices=["both", "plus"],
                            help="search both strands or the plus strand only "
                            "(default %(default)s).")
    group_nast.add_argument('--nast-notaligned', metavar="FILE",
                            help="write not aligned sequences in FASTA format.")
    group_nast.add_argument('--nast-hits', metavar="FILE",
                            help="write hits on a TAB delimited file with the "
                            "query sequence id, the template sequence id and "
                            "the identity.")
    group_nast.add_argument('--nast-nofilter', default=False, action="store_true",
                            help="do not remove positions which are gaps in "
                            "every sequenceces (useful if you want to apply "
                            "a Lane mask filter before the tree inference).")
    group_nast.add_argument('--nast-notrim', default=False, action="store_true",
                            help="force to align the entire candidate sequence "
                            "(i.e. do not trim the candidate sequence to that "
                            "which is bound by the beginning and end points of "
                            "of the alignment span")
    args = parser.parse_args(argv)


    if (args.method == "nast") and (not args.nast_template):
        parser.error("NAST alignment method requires a template file "
                     "(--nast-template)")

    try:
        if args.method == "nast":
            micca.api.msa.nast(
                input_fn=args.input,
                template_fn=args.nast_template,
                output_fn=args.output,
                notaligned_fn=args.nast_notaligned,
                hits_fn=args.nast_hits,
                ident=args.nast_id,
                threads=args.nast_threads,
                mincov=args.nast_mincov,
                strand=args.nast_strand,
                nofilter=args.nast_nofilter,
                notrim=args.nast_notrim)
        else:
            micca.api.msa.muscle(
                input_fn=args.input,
                output_fn=args.output,
                maxiters=args.muscle_maxiters)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
