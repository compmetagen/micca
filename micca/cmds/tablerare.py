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
    prog = "micca tablerare"

    description = textwrap.dedent('''\
        Rarefy an OTU table by subsampling, with or without
        replacement. Samples that have fewer counts then the depth are
        omitted from the output table. OTUs that are not present in at
        least one sample are omitted from the output table.
    ''')

    epilog = textwrap.dedent('''\
        Examples

        Rarefy an OTU table at a depth of 1000 sequences/sample:

            micca tablerare -i otutable.txt -o otutable_rare.txt -d 1000
    ''')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=prog,
        description=description,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', metavar="FILE", required=True,
                       help="input OTU table file (required).")
    group.add_argument('-o', '--output', metavar="FILE", required=True,
                       help="output rarefied OTU table file (required).")
    group.add_argument('-d', '--depth', type=int, required=True,
                       help="sample depth (>0, required).")
    group.add_argument('-r', '--replace', default=False, action="store_true",
                       help="subsample with replacement.")
    group.add_argument('-s', '--seed', type=int, default=0,
                       help="random seed (default %(default)s).")
    args = parser.parse_args(argv)


    try:
        micca.api.table.rare(
            input_fn=args.input,
            output_fn=args.output,
            depth=args.depth,
            replace=args.replace,
            seed=args.seed)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
