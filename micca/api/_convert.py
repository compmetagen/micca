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

from Bio import SeqIO
from Bio.SeqIO.QualityIO import PairedFastaQualIterator


CONVERT_INPUT_FMTS = sorted(SeqIO._FormatToIterator.keys() + ["fasta-qual"])
CONVERT_OUTPUT_FMTS = sorted(SeqIO._FormatToWriter.keys())


def convert(input_fn, output_fn, qual_fn=None, input_fmt="fastq",
            output_fmt="fasta", defaultq=40):

    def add_phred_quality(records, defaultq):
        for record in records:
            if not record.letter_annotations.has_key("phred_quality"):
                record.letter_annotations["phred_quality"] = \
                  [defaultq] * len(record)
            yield record
    
    if input_fmt not in CONVERT_INPUT_FMTS:
        raise ValueError("invalid input format {}".format(input_fmt))

    if output_fmt not in CONVERT_OUTPUT_FMTS:
        raise ValueError("invalid output format {}".format(output_fmt))

    if (input_fmt == "fasta-qual") and (qual_fn is None):
        raise ValueError("output format 'fasta-qual' requires an input "
                         "quality file")

    # parse records
    input_handle = open(input_fn, 'r')
    if input_fmt == "fasta-qual":
        qual_handle = open(qual_fn, 'r')
        records = PairedFastaQualIterator(input_handle, qual_handle)
    else:
        records = SeqIO.parse(input_handle, input_fmt)

    # write records
    output_handle = open(output_fn, 'wb')
    count = SeqIO.write(add_phred_quality(records, defaultq),
                        output_handle, output_fmt)

    # close files
    output_handle.close()
    input_handle.close()
    if input_fmt == "fasta-qual":
        qual_handle.close()

    sys.stdout.write("{:d} sequences converted\n".format(count))
