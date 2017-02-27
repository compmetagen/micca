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
import warnings

import micca.api


def _stdoutwarn(message, category, filename, lineno, file=None, line=None):
    sys.stdout.write(str(message))


def main(argv):
    prog = "micca mergepairs"

    description = textwrap.dedent('''\
        micca mergepairs merges paired-end sequence reads into one sequence.

        A single merging of a pair of FASTQ files can be simply performed
        using both -i/--input and -r/--reverse options.

        When the option -r/--reverse is not specified:

        1. you can indicate several forward files (with the option -i/--input);

        2. the reverse file name will be constructed by replacing the string
           '_R1' in the forward file name with '_R2' (typical in Illumina
           file names, see options -p/--pattern and -e/--repl);

        3. after the merging of the paired reads, different samples will be
           merged in a single file and sample names will be appended to the
           sequence identifier (e.g. >SEQID;sample=SAMPLENAME), as in 'micca
           merge' and 'micca split'. Sample names are defined as the leftmost
           part of the file name splitted by the first occurence of '_'
           (-s/--sep option). Whitespace characters in names will be replaced
           with a single character underscore ('_').

        micca mergepairs wraps VSEARCH (https://github.com/torognes/vsearch).
        Statistical testing of significance is performed in a way similar to
        PEAR (doi: 10.1093/bioinformatics/btt593). The quality of merged bases
        is computed as in USEARCH (doi: 10.1093/bioinformatics/btv401).

        By default staggered read pairs (staggered pairs are pairs where the 3'
        end of the reverse read has an overhang to the left of the 5’ end
        of the forward read) will be merged. To override this feature (and 
        therefore to discard staggered alignments) set the -n/--nostagger 
        option.
    ''')

    epilog = textwrap.dedent('''\
        Examples

        Merge reads with a minimum overlap length of 50 and maximum number
        of allowed mismatches of 3:

            micca mergepairs -i reads1.fastq -r reads2.fastq -o merged.fastq \\
            -l 50 -d 3

        Merge several illumina paired reads (typically named *_R1*.fastq and
        *_R2*.fastq):

            micca mergepairs -i *_R1*.fastq -o merged.fastq --notmerged-fwd \\
            notmerged_fwd.fastq --notmerged-rev notmerged_rev.fastq
    ''')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=prog,
        description=description,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', nargs='+', metavar="FILE",
                       required=True,
                       help="forward FASTQ file(s), Sanger/Illumina 1.8+ format "
                       "(phred+33) (required).")
    group.add_argument('-o', '--output', metavar='FILE', required=True,
                       help="output FASTQ file (required).")
    group.add_argument('-r', '--reverse', metavar="FILE",
                       help="reverse FASTQ file, Sanger/Illumina 1.8+ format "
                       "(phred+33).")
    group.add_argument('-l', '--minovlen', type=int, default=32,
                       help="minimum overlap length (default %(default)s).")
    group.add_argument('-d', '--maxdiffs', type=int, default=8,
                       help="maximum number of allowed mismatches in the "
                       "overlap region (default %(default)s).")
    group.add_argument('-p', '--pattern', default="_R1",
                       help="when the reverse filename is not specified, it "
                       "will be constructed by replacing 'PATTERN' in the "
                       "forward file name with 'REPL' (default %(default)s).")
    group.add_argument('-e', '--repl', default="_R2",
                       help="when the reverse filename is not specified, it "
                       "will be constructed by replacing 'PATTERN' in the "
                       "forward file name with 'REPL' (default %(default)s).")
    group.add_argument('-s', '--sep', default="_",
                       help="when the reverse file name is not specified, "
                       "sample names are appended to the sequence identifier "
                       "(e.g. >SEQID;sample=SAMPLENAME). Sample names are "
                       "defined as the leftmost part of the file name "
                       "splitted by the first occurence of 'SEP' (default "
                       "%(default)s)")
    group.add_argument('-n', '--nostagger', default=False, action="store_true",
                       help="forbid the merging of staggered read pairs. "
                       "Without this option the command will merge staggered "
                       "read pairs and the 3' overhang of the reverse read will " 
                       "be not included in the merged sequence.")
    group.add_argument('--notmerged-fwd', metavar="FILE",
                       help="write not merged forward reads.")
    group.add_argument('--notmerged-rev', metavar="FILE",
                       help="write not merged reverse reads.")

    args = parser.parse_args(argv)


    warnings.showwarning = _stdoutwarn

    try:
        micca.api.mergepairs(
            input_fns=args.input,
            output_fn=args.output,
            reverse_fn=args.reverse,
            notmerged_fwd_fn=args.notmerged_fwd,
            notmerged_rev_fn=args.notmerged_rev,
            minovlen=args.minovlen,
            maxdiffs=args.maxdiffs,
            pattern=args.pattern,
            repl=args.repl,
            sep=args.sep,
            nostagger=args.nostagger)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
