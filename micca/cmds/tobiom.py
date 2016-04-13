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
    prog = "micca tobiom"

    description = textwrap.dedent('''\
        micca tobiom converts the micca OTU table into BIOM Version
        1.0 (JSON) format. Optionally, taxonomy and/or sample
        information can be added.  When you convert on
        (closed-reference) OTU table for PICRUSt, replace OTU IDs with
        the original sequence IDs use the option -u/--otuids.
        ''')

    epilog = textwrap.dedent('''\
        Example

            micca tobiom -i otutable.txt -o output.biom -t tax.txt -s sampledata.txt
    ''')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=prog,
        description=description,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', metavar="FILE", required=True,
                       help="input OTU table file (required).")
    group.add_argument('-o', '--output', metavar='FILE', required=True,
                       help="output BIOM file Version 1.0 (JSON) (required).")
    group.add_argument('-t', '--tax', metavar="FILE",
                       help="add taxonomy information from a taxonomy file.")
    group.add_argument('-s', '--sampledata', metavar="FILE",
                       help="add sample information from a sample data file.")
    group.add_argument('-u', '--otuids', metavar="FILE",
                       help="replace OTU IDs with the original sequence IDs. "
                       "Useful when the closed-reference OTU picking protocol "
                       "was performed for PICRUSt")
    args = parser.parse_args(argv)

    try:
        micca.api.tobiom(
            input_fn=args.input,
            output_fn=args.output,
            tax_fn=args.tax,
            sampledata_fn=args.sampledata,
            otuids_fn=args.otuids)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
