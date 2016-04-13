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
    prog = "micca trim"

    description = textwrap.dedent('''\
        micca trim trims forward and reverse primers from a FASTQ/FASTA file
        using Cutadapt (doi: 10.14806/ej.17.1.200) internally. Primer and the
        sequence preceding (for forward) or succeding (for reverse) it are
        removed. Optionally, reads that do not contain the primers (untrimmed
        reads) can be discarded with the options -W/--duforward and
        -R/--dureverse. Recommended options are:

        * always discard reads that do not contain the forward primer
          (-W/--duforward option);

        * for overlapping paired-end (already merged) reads, also discard
          reads that do not contain the reverse primer (using both
          -W/--duforward and -R/--dureverse options).

        IUPAC codes and multiple primers are supported.
    ''')

    epilog = textwrap.dedent('''\
        Examples

        454 or Illumina single-end reads: trim forward primer and discard reads
        that do not contain it. Moreover, trim reverse primer:

            micca trim -i input.fastq -o trimmed.fastq -w AGGATTAGATACCCTGGTA \\
            -r CRRCACGAGCTGACGAC -W

        Illumina overlapping paired-end (already merged) reads: trim
        forward and reverse primers. Reads that do not contain the forward
        or the reverse primer will be discarded:

            micca trim -i reads.fastq -o trimmed.fastq -w AGGATTAGATACCCTGGTA \\
            -r CRRCACGAGCTGACGAC -W -R
    ''')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=prog,
        description=description,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', metavar="FILE", required=True,
                       help="input FASTQ or FASTA file (required).")
    group.add_argument('-o', '--output', metavar="FILE", required=True,
                       help="output FASTQ or FASTA file (required).")
    group.add_argument('-w', '--forward', help="trim forward primer(s). "
                       "Only the best matching primer is removed.", nargs='+')
    group.add_argument('-r', '--reverse', help="trim reverse primer(s). "
                       "Only the best matching primer is removed.", nargs='+')
    group.add_argument('-e', '--maxerate', type=float, default=0.1,
                       help="maximum allowed error rate (default %(default)s).")
    group.add_argument('-c', '--searchrc', action="store_true", default=False,
                       help="search reverse complement primers too (default "
                       "%(default)s).")
    group.add_argument('-W', '--duforward', action="store_true", default=False,
                       help="discard untrimmed reads (reads that do not "
                       "contain the forward primer) (always recommended) "
                       "(default %(default)s).")
    group.add_argument('-R', '--dureverse', action="store_true", default=False,
                       help="discard untrimmed reads (reads that do not "
                       "contain the reverse primer) (suggested option "
                       "for overlapping paired-end already merged reads) "
                       "(default %(default)s).")
    group.add_argument('-f', '--format', default="fastq",
                       choices=["fastq", "fasta"],
                       help="file format (default %(default)s).")
    args = parser.parse_args(argv)

    if (args.forward is None) and (args.reverse is None):
        parser.error("at least one option between -w/--forward and "
                     "-r/--reverse is required")

    try:
        micca.api.trim(
            input_fn=args.input,
            output_fn=args.output,
            forward=args.forward,
            reverse=args.reverse,
            maxerate=args.maxerate,
            searchrc=args.searchrc,
            duforward=args.duforward,
            dureverse=args.dureverse,
            fmt=args.format)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
