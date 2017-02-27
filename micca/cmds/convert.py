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
    prog = "micca convert"

    description = textwrap.dedent('''\
        micca convert converts between sequence file formats. See
        http://biopython.org/wiki/SeqIO#File_Formats for a comprehnsive list
        of the supported file formats.

        Supported input formats:
        {}

        Supported output formats:
        {}

    '''.format(
        ", ".join(micca.api.CONVERT_INPUT_FMTS),
        ", ".join(micca.api.CONVERT_OUTPUT_FMTS)))

    epilog = textwrap.dedent('''\
        Examples

        Convert FASTA+QUAL files into a FASTQ (Sanger/Illumina 1.8+) file:

            micca convert -i input.fasta -q input.qual -o output.fastq \\
            -f fasta-qual -F fastq

        Convert a SFF file into a FASTQ (Sanger/Illumina 1.8+) file:

            micca convert -i input.sff -o output.fastq -f sff -F fastq
    ''')


    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=prog,
        description=description,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', metavar="FILE", required=True,
                       help="input sequence file (required).")
    group.add_argument('-o', '--output', metavar="FILE", required=True,
                       help="output sequence file (required).")
    group.add_argument('-q', '--qual', metavar="FILE",
                       help="input quality file (required for 'fasta-qual' "
                       "input format.")
    group.add_argument('-d', '--defaultq', type=int, default=40,
                       help="default phred quality score for format-without-"
                       "quality to format-with-quality conversion "
                       "(default %(default)s).")
    group.add_argument('-f', '--input-format', default="fastq",
                       help="input file format (default %(default)s).")
    group.add_argument('-F', '--output-format', default="fasta",
                       help="input file format (default %(default)s).")
    args = parser.parse_args(argv)


    try:
        micca.api.convert(
            input_fn=args.input,
            output_fn=args.output,
            qual_fn=args.qual,
            input_fmt=args.input_format,
            output_fmt=args.output_format,
            defaultq=args.defaultq)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
