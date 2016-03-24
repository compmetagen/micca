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

import csv

try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest

from Bio import SeqIO


def split(input_fn, output_fn, barcode_fn, notmatched_fn=None, counts_fn=None,
          skip=0, maxe=1, trim=True, fmt="fastq"):

    def hamming(seq1, seq2):
        return sum(s1!=s2 for s1, s2 in izip_longest(seq1, seq2, fillvalue=""))

    # read barcodes
    bc = dict()
    for record in SeqIO.parse(barcode_fn, 'fasta'):
        bc[record.id] = str(record.seq.upper())

    # barcode counter
    bc_count = dict.fromkeys(bc.keys(), 0)
    bc_count["Unknown"] = 0

    # write the output and notmatched files 
    output_handle = open(output_fn,'wb')
    for record in SeqIO.parse(input_fn, fmt):
        seq = str(record.seq.upper())

        # compute the number of errors for each barcode
        bc_err = dict()
        for sn, bc_seq in bc.iteritems():
            end = skip+len(bc_seq)
            e = hamming(bc_seq, seq[skip:end])
            bc_err[sn] = e

        # minimum error
        mine = min(bc_err.values())

        # if the minimum error is <= maximum allowed error, write to the merged
        # file, else write to the notmatched file (if notmatched_fn is not None)
        if mine <= maxe:
            minsn = [sn for sn, e in bc_err.iteritems() if e == mine][0]

            record.id = "{0};sample={1}".format(record.id, minsn)

            try:
                description = record.description.split(None, 1)[1]
            except IndexError:
                description = ""
            record.description = description
            
            if trim:
                record = record[end:]
                
            SeqIO.write(record, output_handle, fmt)
            bc_count[minsn] += 1
        else:
            if notmatched_fn is not None:
                notmatched_handle = open(notmatched_fn,'ab')
                SeqIO.write(record, notmatched_handle, fmt)
                notmatched_handle.close()
            bc_count['Unknown'] += 1

    # END for record in SeqIO.parse(input_fn, fmt):
            
    output_handle.close()

    # write the sample counts file
    if counts_fn is not None:
        with open(counts_fn, 'wb') as counts_handle:
            counts_writer = csv.writer(counts_handle, delimiter='\t',
                                       lineterminator='\n')
            sns = bc_count.keys()
            sns.remove("Unknown")

            for sn in sorted(sns):
                counts_writer.writerow([sn, "{:d}".format(bc_count[sn])])
                
            counts_writer.writerow(["Unknown", 
                                    "{:d}".format(bc_count["Unknown"])])
            
