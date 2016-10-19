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
from micca import argutils


def main(argv):
    prog = "micca tabletotax"

    description = textwrap.dedent('''\
        Given an OTU table and a taxonomy file, micca tabletotax
        creates in the output directory a table for each taxonomic
        level (taxtable1.txt, ..., taxtableN.txt). OTU counts are
        summed together if they have the same taxonomy at the
        considered level.

        The OTU table must be an OTU x sample, TAB-separated OTU table
        file (see 'micca otu'). The taxonomy file must be a
        tab-delimited file where where rows are either in the form
        (see 'micca classify'):

        1. SEQID[TAB]k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__;g__;
        2. SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales;;;
        3. SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales
        4. SEQID[TAB]D_0__Bacteria;D_1__Firmicutes;D_2__Clostridia;D_3__Clostridiales;D_4__;D_5__;
    ''')

    epilog = textwrap.dedent('''\
        Examples

            micca tabletotax -i otutable.txt -t tax.txt -o taxtables
    ''')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=prog,
        description=description,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', metavar="FILE", required=True,
                       help="input OTU table file (required).")
    group.add_argument('-t', '--tax', metavar="FILE", required=True,
                       help="input taxonomy file (required).")
    group.add_argument('-o', '--output', metavar='DIR', default=".",
                       help="output directory (default %(default)s).",
                       type=argutils.outputdir)
    args = parser.parse_args(argv)

    try:
        micca.api.table.totax(
            input_fn=args.input,
            tax_fn=args.tax,
            output_dir=args.output)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
