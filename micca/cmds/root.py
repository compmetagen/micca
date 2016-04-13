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

import sys
import argparse
import textwrap

import micca.api


def main(argv):
    prog = "micca root"

    description = textwrap.dedent('''\
        micca root reroot the input tree:

        * at the calculated midpoint between the two most distant tips of the
          tree (--method midpoint);

        * with the outgroup clade containing the given taxa (leaf nodes),
          i.e. the common ancestor of the outgroup (--method outgroup).
    ''')

    epilog = textwrap.dedent('''\
        Examples

        Midpoint rooting:

            micca root -i input.tree -o input_rooted.tree

        Rooting with outgroup:

            micca root -i input.tree -o input_rooted.tree -m outgroup DENOVO1 DENOVO2
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
    group.add_argument('-m', '--method', default="midpoint",
                       choices=["midpoint", "outgroup"],
                       help="rooting method (default %(default)s).")
    group.add_argument('-t', '--targets', nargs='+',
                       help="list of targets defining the outgroup (required "
                       "for the outgroup method).")
    args = parser.parse_args(argv)


    if (args.method == "outgroup") and (args.targets is None):
        parser.error("outgroup method requires a list of taxa (-t/--taxa)")

    try:
        if args.method == "midpoint":
            micca.api.root.midpoint(
                input_fn=args.input,
                output_fn=args.output)
        else:
            micca.api.root.outgroup(
                input_fn=args.input,
                output_fn=args.output,
                targets=args.targets)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
