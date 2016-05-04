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

import argparse
import sys
import textwrap

from micca import argutils
import micca.api


def main(argv):
    prog = "micca otu"

    description = textwrap.dedent('''\
        micca otu assigns similar sequences (marker genes such as 16S rRNA and
        the fungal ITS region) to operational taxonomic units (OTUs).

        Trimming the sequences to a fixed position before clustering is
        *strongly recommended* when they cover partial amplicons or if quality
        deteriorates towards the end (common when you have long amplicons and
        single-end sequencing).

        Removing ambiguous nucleotides 'N' (with the option --maxns 0 in micca
        filter) is mandatory if you use the de novo swarm clustering method.

        micca otu provides the following protocols:

        * de novo greedy clustering (denovo_greedy): sequences are clustered
          without relying on an external reference database, using an
          approach similar to the UPARSE pipeline (doi: 10.1038/nmeth.2604):
          i) predict sequence abundances of each sequence by dereplication; ii)
          greedy clustering; iii) remove chimeric sequences (de novo, optional)
          from the representatives; iv) map sequences to the representatives.

        * de novo swarm (denovo_swarm): sequences are clustered without relying
          on an external reference database, using swarm (doi:
          10.7717/peerj.593, doi: 10.7717/peerj.1420,
          https://github.com/torognes/swarm): i) predict sequence abundances of
          each sequence by dereplication; ii) swarm clustering; iii) remove
          chimeric sequences (de novo, optional) from the representatives.

        * closed-reference clustering (closed_ref): sequences are clustered
          against an external reference database and reads that could not be
          matched are discarded.

        * open-reference clustering (open_ref): sequences are clustered
          against an external reference database and reads that could not be
          matched are clustered with the 'de novo greedy' protocol.

        Outputs:

        * otutable.txt: OTU x sample, TAB-separated OTU table file,
          containing the number of times an OTU is found in each sample.

        * otus.fasta: FASTA file containing the representative sequences (OTUs);

        * otuids.txt: OTU ids to original sequence ids (tab-delimited text file)

        * hits.txt: three-columns, TAB-separated file:

          1. matching sequence
          2. representative (seed)
          3. identity (if available, else '*'), defined as:

                      matching columns
             -------------------------------- ;
             alignment length - terminal gaps

        * otuschim.fasta (only for 'denovo_greedy', 'denovo_swarm' and
          'open_ref' when --rmchim is specified): FASTA file containing the
          chimeric otus;
    ''')

    epilog = textwrap.dedent('''\
        Examples

        De novo clustering with a 97% similarity threshold and remove
        chimeric OTUs:

            micca otu -i input.fasta --method denovo_greedy --id 0.97 -c

        Open-reference OTU picking protocol with a 97% similarity
        threshold, without removing chimeras in the de novo protocol step
        and using 8 threads:

            micca otu -i input.fasta --method open_ref --threads 8 --id 0.97 \\
            --ref greengenes_2013_05/rep_set/97_otus.fasta

        De novo swarm clustering with the protocol suggested by the authors
        using 4 threads (see https://github.com/torognes/swarm and
        https://github.com/torognes/swarm/wiki):

            micca otu -i input.fasta --method denovo_swarm --threads 4 \\
            --swarm-fastidious --rmchim --minsize 1
    ''')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=prog,
        description=description,
        epilog=epilog)

    group = parser.add_argument_group("arguments")

    group.add_argument('-i', '--input', metavar="FILE", required=True,
                       help="input fasta file (required).")
    group.add_argument('-o', '--output', metavar='DIR', default=".",
                       help="output directory (default %(default)s).",
                       type=argutils.outputdir)
    group.add_argument('-r', '--ref', metavar="FILE",
                       help="reference sequences in fasta format, required "
                       "for 'closed_ref' and 'open_ref' clustering methods.")
    group.add_argument('-m', '--method', default="denovo_greedy",
                       choices=["denovo_greedy", "denovo_swarm", "closed_ref",
                       "open_ref"],
                       help="clustering method (default %(default)s)")
    group.add_argument('-d', '--id', default=0.97, type=float,
                       help="sequence identity threshold (for 'denovo_greedy', "
                       "'closed_ref' and 'open_ref', 0.0 to 1.0, "
                       "default %(default)s).")
    group.add_argument('-n', '--mincov', default=0.75, type=float,
                       help="reject sequence if the fraction of alignment "
                       "to the reference sequence is lower than MINCOV. "
                       "This parameter prevents low-coverage alignments at "
                       "the end of the sequences (for 'closed_ref' and "
                       "'open_ref' clustering methods, default %(default)s).")
    group.add_argument('-t', '--threads', default=1, type=int,
                        help="number of threads to use (1 to 256, default "
                        "%(default)s).")
    group.add_argument('-c', '--rmchim', default=False, action="store_true",
                        help="remove chimeric sequences (for 'denovo_greedy', "
                        "'denovo_swarm' and 'open_ref' OTU picking methods).")
    group.add_argument('-g', '--greedy', default="dgc", choices=["dgc", "agc"],
                        help="greedy clustering strategy, distance (DGC) or "
                        "abundance-based (AGC) (for 'denovo_greedy' and "
                        "'open_ref' clustering methods) (default %(default)s).")
    group.add_argument('-s', '--minsize', default=2, type=int,
                        help="discard sequences with an abundance value "
                        "smaller than MINSIZE after dereplication (>=1, "
                        "default %(default)s). Recommended value is 2 (i.e. "
                        "discard singletons) for 'denovo_greedy' and "
                        "'open_ref', 1 (do not discard anything) for "
                        "'denovo_swarm'.")
    group.add_argument('-a', '--strand', default="both",
                        choices=["both", "plus"],
                        help="search both strands or the plus strand only "
                        "(for 'closed_ref' and 'open_ref' clustering methods, "
                        "default %(default)s).")

    # swarm options
    group_swarm = parser.add_argument_group("Swarm specific options")
    group_swarm.add_argument('--swarm-differences', type=int, default=1,
                             help="maximum number of differences allowed "
                             "between two amplicons. Commonly used d values "
                             "are 1 (linear complexity algorithm), 2 or 3, "
                             "rarely higher. (>=0, default %(default)s).")
    group_swarm.add_argument('--swarm-fastidious', default=False,
                             action="store_true",
                             help="when working with SWARM_DIFFERENCES=1, "
                             "perform a second clustering pass to reduce the "
                             "number of small OTUs (recommended option).")

    args = parser.parse_args(argv)


    if (args.method in ['closed_ref', 'open_ref']) and (args.ref is None):
        parser.error("%s OTU picking method requires reference sequences "
                     "(--ref)" % args.method)

    try:
        if args.method == "denovo_greedy":
            micca.api.otu.denovo_greedy(
                input_fn=args.input,
                output_dir=args.output,
                ident=args.id,
                threads=args.threads,
                rmchim=args.rmchim,
                greedy=args.greedy,
                minsize=args.minsize)

        elif args.method == "denovo_swarm":
            micca.api.otu.denovo_swarm(
                input_fn=args.input,
                output_dir=args.output,
                differences=args.swarm_differences,
                fastidious=args.swarm_fastidious,
                threads=args.threads,
                rmchim=args.rmchim,
                minsize=args.minsize)

        elif args.method == "closed_ref":
            micca.api.otu.closed_ref(
                input_fn=args.input,
                ref_fn=args.ref,
                output_dir=args.output,
                ident=args.id,
                threads=args.threads,
                mincov=args.mincov,
                strand=args.strand)

        else:
            micca.api.otu.open_ref(
                input_fn=args.input,
                ref_fn=args.ref,
                output_dir=args.output,
                ident=args.id,
                threads=args.threads,
                mincov=args.mincov,
                rmchim=args.rmchim,
                greedy=args.greedy,
                minsize=args.minsize,
                strand=args.strand)
    except Exception as err:
        sys.stderr.write("Error: {}\n".format(err))
        sys.exit(1)
