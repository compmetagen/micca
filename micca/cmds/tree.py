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
    prog = "micca tree"

    description = textwrap.dedent('''\
        micca tree infers phylogenetic trees from alignments. It provides two
        methods:

        * FastTree (doi: 10.1371/journal.pone.0009490);
        * MUSCLE (doi: 10.1093/nar/gkl244).
    ''')

    epilog = textwrap.dedent('''\
        Examples

        Tree inference using FastTree and the generalized time-reversible
        (GTR)+CAT model:

            micca tree -i input.fasta -o tree.tree --fasttree-gtr
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
                       help="output tree in Newick format (required).")
    group.add_argument('-m', '--method', default="fasttree",
                       choices=["fasttree", "muscle"],
                       help="tree inference method (default %(default)s).")

    # fasttree options
    group_fasttree = parser.add_argument_group("FastTree specific options")
    group_fasttree.add_argument('--fasttree-gtr', action="store_true",
                                default=False,
                                help="use the generalized time-reversible "
                                "(GTR)+CAT model instead of Jukes-Cantor+CAT "
                                "(default %(default)s).")
    group_fasttree.add_argument('--fasttree-fastest', action="store_true",
                                default=False,
                                help="speed up the neighbor joining phase and "
                                "reduce memory usage recommended for >50,000 "
                                "sequences) (default %(default)s).")

    # MUSCLE options
    group_muscle = parser.add_argument_group("MUSCLE specific options")
    group_muscle.add_argument('--muscle-cluster', default="upgmb",
                              choices=["upgmb", "upgma", "neighborjoining"],
                              help="clustering algorithm (default %(default)s).")
    args = parser.parse_args(argv)


    try:
        if args.method == "fasttree":
            micca.api.tree.fasttree(
                input_fn=args.input,
                output_fn=args.output,
                gtr=args.fasttree_gtr,
                fastest=args.fasttree_fastest)
        else:
            micca.api.tree.muscle(
                input_fn=args.input,
                output_fn=args.output,
                cluster=args.muscle_cluster)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
