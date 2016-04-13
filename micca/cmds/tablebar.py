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

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import micca.api


def main(argv):

    PLOT_OUTPUT_FMTS = plt.gcf().canvas.get_supported_filetypes()

    prog = "micca tablebar"

    description = textwrap.dedent('''\
        micca tablebar generates a relative abundance bar plot from
        OTU or taxa tables. The table must be an OTU/taxon x sample,
        TAB-separated file (see 'micca otu').
    ''')

    epilog = textwrap.dedent('''\
        Example

            micca tablebar -i otutable.txt -o otutable_plot.png
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
                       help="output image file (required).")
    group.add_argument('-r', '--raw', default=False, action="store_true",
                       help="plot raw values (i.e. counts) instead of relative "
                       "abundances.")
    group.add_argument('-t', '--topn', metavar="N", type=int, default=12,
                       help="plot the top N abundant taxa (default "
                       "%(default)s).")
    group.add_argument('--xticklabelsize', type=float, metavar="SIZE",
                       default=8,
                       help="x tick label size (default %(default)s).")
    group.add_argument('-f', '--format', default="png",
                       choices=PLOT_OUTPUT_FMTS,
                       help="output file format (default %(default)s).")
    args = parser.parse_args(argv)


    try:
        micca.api.table.bar(
            input_fn=args.input,
            output_fn=args.output,
            raw=args.raw,
            topn=args.topn,
            xticklabelsize=args.xticklabelsize,
            fmt=args.format)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
