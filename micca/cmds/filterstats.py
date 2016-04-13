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

from micca import argutils
import micca.api


def main(argv):
    prog = "micca filterstats"

    description = textwrap.dedent('''\
        micca filterstats reports the fraction of reads that would pass for each
        specified maximum expected error (EE) rate %% and the maximum number of
        allowed Ns after:

        * discarding sequences that are shorter than the specified length
          (suggested for Illumina overlapping paired-end (already merged)
          reads);

        * discarding sequences that are shorter than the specified length AND
          truncating sequences that are longer (suggested for Illumina and 454
          unpaired reads);

        Parameters for the 'micca filter' command should be chosen for each
        sequencing run using this tool.

        micca filterstats returns in the output directory 3 files:

        * filterstats_minlen.txt: fraction of reads that would pass the filter after
          the minimum length filtering;
        * filterstats_trunclen.txt: fraction of reads that would pass the filter after
          the minimum length filtering + truncation;
        * filterstats_plot.png: plot in PNG format.
    ''')

    epilog = textwrap.dedent('''\
        Examples

        Compute filter statistics on the top 10000 sequences, predicting
        the fraction of reads that would pass for each maximum EE error
        rate (default values):

            micca filterstats -i input.fastq -o stats -t 10000
    ''')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description,
        prog=prog,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', metavar="FILE", required=True,
                       help="input FASTQ file, Sanger/Illumina 1.8+ format "
                       "(phred+33) (required).")
    group.add_argument('-o', '--output', metavar='DIR', default=".",
                       help="output directory (default %(default)s).",
                       type=argutils.outputdir)
    group.add_argument('-t', '--topn', type=int,
                       help="perform statistics on the first TOPN sequences "
                       "(disabled by default)")
    group.add_argument('-e', '--maxeerates', nargs='+', type=float,
                       default=[0.25, 0.5, 0.75, 1, 1.25, 1.5],
                       help="max expected error rates (%%). (default "
                       "%(default)s)")
    group.add_argument('-n', '--maxns', type=int,
                       help="max number of Ns. (disabled by default).")
    args = parser.parse_args(argv)


    try:
        micca.api.filterstats(
            input_fn=args.input,
            output_dir=args.output,
            topn=args.topn,
            maxeerates=args.maxeerates,
            maxns=args.maxns)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
