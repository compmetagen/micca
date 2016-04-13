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
    prog = "micca split"

    description = textwrap.dedent('''\
        micca split assign the multiplexed reads to samples based on their 5'
        nucleotide barcode (demultiplexing) provided by the FASTA file
        (--barcode). micca split creates a single FASTQ or FASTA file with
        sample information (e.g. >SEQID;sample=SAMPLENAME) appended to the
        sequence identifier. Barcode and the sequence preceding it is removed
        by default, e.g.:

        Barcode file:        Input file:

        >SAMPLE1             >SEQ1
        TCAGTCAG             TCAGTCAGGCCACGGCTAACTAC...
        ...                  ...

        the output will be:

        >SEQ1;sample=SAMPLE1
        GCCACGGCTAACTAC...
        ...
    ''')

    epilog = textwrap.dedent('''\
        Examples

        Split 'reads.fastq' and write the notmatched sequences in the
        file 'notmatched.fastq':

            micca split -i input.fastq -o splitted.fastq -b barcode.fasta \\
            -n notmatched.fastq
    ''')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=prog,
        description=description,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', metavar="FILE", required=True,
                       help="input FASTQ/FASTA file (required).")
    group.add_argument('-o', '--output', metavar="FILE", required=True,
                       help="output FASTQ/FASTA file (required).")
    group.add_argument('-b', '--barcode', metavar="FILE", required=True,
                       help="barcode file in FASTA format (required).")
    group.add_argument('-n', '--notmatched', metavar="FILE",
                       help="write reads in which no barcode was found.")
    group.add_argument('-c', '--counts', metavar="FILE",
                       help="write barcode counts in a tab-delimited file.")
    group.add_argument('-s', '--skip', type=int, default=0, metavar="N",
                       help="skip N bases before barcode matching (e.g. "
                       "if your sequences start with the control sequence "
                       "'TCAG' followed by the barcode, set to 4) (>=0, default "
                       "%(default)s).")
    group.add_argument('-e', '--maxe', type=int, default=1,
                       help="maximum number of allowed errors (>=0, default "
                       "%(default)s).")
    group.add_argument('-t', '--notrim', action="store_true", default=False,
                       help="do not trim barcodes and the sequence preceding "
                       "it from sequences.")
    group.add_argument('-f', '--format', default="fastq",
                       choices=["fastq", "fasta"],
                       help="file format (default %(default)s).")
    args = parser.parse_args(argv)


    try:
        micca.api.split(
            input_fn=args.input,
            output_fn=args.output,
            barcode_fn=args.barcode,
            notmatched_fn=args.notmatched,
            counts_fn=args.counts,
            skip=args.skip,
            maxe=args.maxe,
            trim=(not args.notrim),
            fmt=args.format)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
