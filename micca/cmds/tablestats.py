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
    prog = "micca tablestats"

    description = textwrap.dedent('''\
        micca tablestats reports a sample summary, an OTU summary and
        the rarefaction curves for the input OTU table. The
        rarefaction curves are evaluated using the interval of 'step'
        (-t/--step) sample depths, always including 1 and the total
        sample size.

        micca filterstats returns in the output directory 4 files:

        * tablestats_samplesumm.txt: samples summary;
        * tablestats_otusumm.txt: OTUs summary;
        * tablestats_rarecurve.txt: rarefaction curves in text format.
        * tablestats_rarecurve_plot.txt: rarefaction curves in png format.
    ''')

    epilog = textwrap.dedent('''\
        Examples

        Compute OTU table statistics on otutable.txt:

            micca tablestats -i otutable.txt -o tablestats
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
    group.add_argument('-t', '--step', type=int, default=500,
                       help="sample depth interval (for rarefaction curves, "
                       "default %(default)s).")
    group.add_argument('-r', '--replace', default=False, action="store_true",
                       help="subsample with replacement (for rarefaction curves).")
    group.add_argument('-s', '--seed', type=int, default=0,
                       help="random seed (for rarefaction curves, default "
                       "%(default)s).")
    args = parser.parse_args(argv)


    try:
        micca.api.table.stats(
            input_fn=args.input,
            output_dir=args.output,
            step=args.step,
            replace=args.replace,
            seed=args.seed)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
