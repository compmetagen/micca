##    Copyright 2015 Davide Albanese <davide.albanese@gmail.com>
##    Copyright 2015 Fondazione Edmund Mach (FEM)

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
    prog = "micca stats"

    description = textwrap.dedent('''\
        micca stats reports statistics on reads in a FASTQ file. micca stats
        returns in the output directory 3 tab-delimited text files:

        * stats_lendist.txt: length distribution;
        * stats_qualdist.txt: Q score distribution;
        * stats_qualsumm.txt: quality summary. For each read position, the
          following statistics are reported:
          - L: read position;
          - NPctCum: percent of reads with at least L bases;
          - QAv: average Q score at position L;
          - EERatePctAv: average expected error (EE) rate %.

        Moreover, micca stats returns the respective plots in PNG format,
        stats_lendist_plot.png, stats_qualdist_plot.png, and
        stats_qualsumm_plot.png.
    ''')

    epilog = textwrap.dedent('''\
        Examples

        Compute statistics on the top 10000 sequences of input.fastq:

            micca stats -i input.fastq -o stats -n 10000
    ''')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=prog,
        description=description,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', metavar="FILE", required=True,
                       help="input FASTQ file, Sanger/Illumina 1.8+ format "
                       "(phred+33) (required).")
    group.add_argument('-o', '--output', metavar='DIR', default=".",
                       help="output directory (default %(default)s).",
                       type=argutils.outputdir)
    group.add_argument('-n', '--topn', type=int,
                       help="perform statistics only on the first TOPN "
                       "sequences (disabled by default).")
    args = parser.parse_args(argv)


    try:
        micca.api.stats(
            input_fn=args.input,
            output_dir=args.output,
            topn=args.topn)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
