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
    prog = "micca merge"

    description = textwrap.dedent('''\
        micca merge merges several FASTQ or FASTA files in a single file.
        Different samples will be merged in a single file and sample names
        will be appended to the sequence identifier
        (e.g. >SEQID;sample=SAMPLENAME). Sample names are defined as the
        leftmost part of the file name splitted by the first occurence of '.'
        (-s/--sep option). Whitespace characters in names will be replaced
        with a single character underscore ('_').
    ''')

    epilog = textwrap.dedent('''\
        Examples

        Merge files in FASTA format:

            micca merge -i in1.fasta in2.fasta in3.fasta -o merged.fasta \\
            -f fasta
    ''')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=prog,
        description=description,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', nargs='+', metavar="FILE",
                       required=True,
                       help="input FASTQ/FASTA file(s) (required).")
    group.add_argument('-o', '--output', metavar="FILE", required=True,
                       help="output FASTQ/FASTA file (required).")
    group.add_argument('-s', '--sep', default=".",
                       help="Sample names are defined as the leftmost part of "
                       "the file name splitted by the first occurence of "
                       "'SEP' (default %(default)s)")
    group.add_argument('-f', '--format', default="fastq",
                       choices=["fastq", "fasta"],
                       help="file format (default %(default)s).")
    args = parser.parse_args(argv)


    try:
        micca.api.merge(
            input_fns=args.input,
            output_fn=args.output,
            sep=args.sep,
            fmt=args.format)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
