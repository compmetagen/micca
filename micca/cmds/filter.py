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


def main(argv):
    prog = "micca filter"

    description = textwrap.dedent('''\
        micca filter filters sequences according to the maximum allowed
        expected error (EE) rate %%. Optionally, you can:

        * discard sequences that are shorter than the specified length
          (suggested for Illumina overlapping paired-end (already merged)
          reads) (option --minlen MINLEN);

        * discard sequences that are shorter than the specified length AND
          truncate sequences that are longer (suggested for Illumina and 454
          unpaired reads) (options --minlen MINLEN --trunc);

        * discard sequences that contain more than a specified number of Ns
          (--maxns).

        Sequences are first shortened and then filtered. Overlapping paired
        reads with should be merged first (using micca-mergepairs) and then
        filtered.

        The expected error (EE) rate %% in a sequence of length L is defined
        as (doi: 10.1093/bioinformatics/btv401):

                         sum(error probabilities)
            EE rate %% = ------------------------ * 100
                                    L

        Before filtering, run 'micca filterstats' to see how many reads will
        pass the filter at different minimum lengths with or without
        truncation, given a maximum allowed expected error rate %% and maximum
        allowed number of Ns.

        micca-filter is based on VSEARCH (https://github.com/torognes/vsearch).
    ''')

    epilog = textwrap.dedent('''\
        Examples

        Truncate reads at 300 bp, discard low quality sequences
        (with EE rate > 0.5%%) and write a FASTA file:

            micca filter -i reads.fastq -o filtered.fasta -m 300 -t -e 0.5
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
    group.add_argument('-o', '--output', metavar="FILE", required=True,
                       help="output FASTA/FASTQ file (required).")
    group.add_argument('-e', '--maxeerate', type=float, default=1,
                       help="discard sequences with more than the specified "
                       "expeced error rate %% (values <=1%%, i.e. less or "
                       "equal than one error per 100 bases, are highly recommended). "
                       "Sequences are discarded after truncation (if enabled) "
                       "(default %(default)s).")
    group.add_argument('-m', '--minlen', type=int, default=1,
                       help="discard sequences that are shorter than MINLEN "
                       "(default %(default)s).")
    group.add_argument('-t', '--trunc', default=False, action="store_true",
                       help="truncate sequences that are longer than MINLEN "
                       "(disabled by default).")
    group.add_argument('-n', '--maxns', type=int,
                       help="discard sequences with more than the specified "
                       "number of Ns. Sequences are discarded after truncation "
                       "(disabled by default).")
    group.add_argument('-f', '--output-format', default="fasta",
                       choices=["fastq", "fasta"],
                       help="file format (default %(default)s).")
    args = parser.parse_args(argv)


    try:
        micca.api.filter(
            input_fn=args.input,
            output_fn=args.output,
            maxee_rate=args.maxeerate,
            maxns=args.maxns,
            minlen=args.minlen,
            trunc=args.trunc,
            output_fmt=args.output_format)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
