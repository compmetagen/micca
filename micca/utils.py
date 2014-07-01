## This code is written by Davide Albanese, <davide.albanese@gmail.com>
## Copyright (C) 2013 Fondazione Edmund Mach
## Copyright (C) 2013 Davide Albanese

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import string
import random
import re
from itertools import product

import numpy as np
from numpy.random import RandomState
import scipy.stats
from Bio import SeqIO


def id_generator(size=8, chars=string.ascii_letters+string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def parse_taxonomy(taxonomy):
    # remove whitespaces and taxonomy prefixes ".*__"
    # (e.g. greengenes taxonomy files)

    
    taxonomy_list = []
    for t in taxonomy.split(';'):
        t = re.sub('.*__', '', t.strip())
        if not t:
            break
        taxonomy_list.append(t)
    return ';'.join(taxonomy_list)


def adna2udna(seq):
    """Ambiguous DNA (IUPAC) to unambiguous DNA.

    >>> for seq in adna2udna('ACGTMAAW'):
    ...     print seq
    ... 
    ACGTAAAA
    ACGTAAAT
    ACGTCAAA
    ACGTCAAT    
    """
    
    dna_iupac = {'A': 'A',
                 'C': 'C',
                 'G': 'G',
                 'T': 'T',
                 'M': 'AC',
                 'R': 'AG',
                 'W': 'AT',
                 'S': 'CG',
                 'Y': 'CT',
                 'K': 'GT',
                 'V': 'ACG',
                 'H': 'ACT',
                 'D': 'AGT',
                 'B': 'CGT',
                 'N': 'ACGT'}

    try:
        seqext = [dna_iupac[letter] for letter in seq]
    except KeyError:
        raise ValueError("seq must be a DNA IUPAC sequence")
        
    for seqtuple in product(*seqext):
        yield "".join(seqtuple)


def fastq_n_seqs(in_filename):
    n_reads = 0
    for record in SeqIO.parse(in_filename, "fastq"):
        n_reads += 1
    return n_reads


def fastq_stats(in_filename):

    per = [10, 25, 50, 75, 90]

    n_reads = 0
    read_length, avg_quality, perc_expected_errors = [], [], []

    for record in SeqIO.parse(in_filename, "fastq"):
        n_reads += 1
        read_length.append(len(record))
        phred_quality = record.letter_annotations["phred_quality"]
        avg_quality.append(np.mean(phred_quality))
        perc_expected_errors.append(np.sum([10**(-q/10) for q in
                                            phred_quality]))

    ret = dict()
    ret["n_reads"] = n_reads
    ret["read_length"] = scipy.stats.scoreatpercentile(read_length, per)
    ret["avg_quality"] = scipy.stats.scoreatpercentile(avg_quality, per)
    ret["perc_expected_errors"] = scipy.stats.scoreatpercentile(
        perc_expected_errors, per)

    return ret


def rarefy_seqs(in_filename, out_filename, depth=1000, fmt="fastq", seed=0):
    """Rarefy a sequence file.
    """

    prng = RandomState(seed)

    records = SeqIO.index(in_filename, fmt)
    record_ids = [record_id for record_id in records.iterkeys()]
    record_ids = prng.choice(record_ids, replace=False, size=depth)

    out_handle = open(out_filename, 'w')
    for record_id in record_ids:
        SeqIO.write(records[record_id], out_handle, fmt)
    out_handle.close()
