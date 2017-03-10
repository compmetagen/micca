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

import os
import os.path
import csv

try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest
from collections import Counter

from Bio import SeqIO

import micca.ioutils
import micca.tax
import micca.tp

__all__ = ["cons", "rdp", "otuid"]


def cons(input_fn, ref_fn, ref_tax_fn, output_fn, ident=0.90,
         maxhits=3, minfrac=0.5, threads=1, mincov=0.75, strand="both"):
    """Consensus classifier.
    """

    def get_tax(seqids, tax_dict):
        tax = []
        for seqid in seqids:
            if tax_dict.has_key(seqid):
                tax.append(tax_dict[seqid])
            else:
                pass
        return tax

    def get_cons_tax(tax, minfrac):
        cons_tax = []
        for rank in izip_longest(*tax, fillvalue=""):
            rank = [elem for elem in rank if elem != ""]
            counter = Counter(rank)
            most_common = counter.most_common(1)[0]
            frac = most_common[1] / len(tax)
            if frac >= minfrac:
                cons_tax.append(most_common[0])
            else:
                break
        if len(cons_tax) == 0:
            cons_tax = ["Unclassified"]
        return cons_tax

    output_dir = os.path.dirname(output_fn)

    tax_dict = micca.tax.read(ref_tax_fn)

    hits_temp_fn = micca.ioutils.make_tempfile(output_dir)
    try:
        micca.tp.vsearch.usearch_global(
            input_fn=input_fn,
            db_fn=ref_fn,
            userout_fn=hits_temp_fn,
            ident=ident,
            threads=threads,
            query_cov=mincov,
            maxaccepts=maxhits,
            maxrejects=32,
            userfields="query+target+id",
            output_no_hits=True,
            top_hits_only=False,
            strand=strand)
    except:
        os.remove(hits_temp_fn)
        raise

    with open(hits_temp_fn, 'rb') as hits_temp_handle:
        with open(output_fn, 'wb') as output_handle:
            hits_temp_reader = csv.reader(hits_temp_handle, delimiter='\t')
            output_writer = csv.writer(
                output_handle, delimiter='\t',lineterminator='\n')
            prev, target, _ = hits_temp_reader.next()
            hits = [target]

            for row in hits_temp_reader:
                if row[0] != prev:
                    tax = get_tax(hits, tax_dict)
                    cons_tax = get_cons_tax(tax, minfrac)
                    output_writer.writerow([prev, ";".join(cons_tax)])
                    hits = [row[1]]
                else:
                    hits.append(row[1])
                prev = row[0]

            tax = get_tax(hits, tax_dict)
            cons_tax = get_cons_tax(tax, minfrac)
            output_writer.writerow([prev, ";".join(cons_tax)])

    os.remove(hits_temp_fn)


def rdp(input_fn, output_fn, gene="16srrna", maxmem=2, minconf=0.8):
    """RDP classifier.
    """

    output_dir = os.path.dirname(output_fn)

    rdp_temp_fn = micca.ioutils.make_tempfile(output_dir)
    try:
        micca.tp.rdp.classify(input_fn, rdp_temp_fn, gene=gene, maxmem=maxmem)
    except:
        os.remove(rdp_temp_fn)
        raise

    queryids = [record.id for record in SeqIO.parse(input_fn, "fasta")]

    rdp_temp_dict = dict()
    with open(rdp_temp_fn, 'rU') as rdp_temp_handle:
        rdp_temp_reader = csv.reader(rdp_temp_handle, delimiter='\t')

        for row in rdp_temp_reader:
            rdp_temp_dict[row[0]] = row[1:]

    with open(output_fn, 'wb') as output_handle:
        output_writer = csv.writer(
            output_handle, delimiter='\t', lineterminator='\n')

        for queryid in queryids:
            try:
                row = rdp_temp_dict[queryid]
            except KeyError:
                tax = []
            else:
                tax = [row[i] for i in range(1, len(row), 3)]
                conf = [row[i] for i in range(3, len(row), 3)]
                try:
                    last = [float(c)>=minconf for c in conf].index(False)
                except ValueError: # False not in list
                    pass
                else:
                    tax = tax[:last]

            if len(tax) == 0:
                tax = ["Unclassified"]

            output_writer.writerow([queryid, ";".join(tax)])

    os.remove(rdp_temp_fn)


def otuid(input_fn, ref_tax_fn, output_fn):
    """OTU ID classifier.
    """

    tax_dict = micca.tax.read(ref_tax_fn)

    input_handle = open(input_fn, 'rU')
    input_reader = csv.reader(input_handle, delimiter='\t')

    output_handle = open(output_fn, 'wb')
    output_writer = csv.writer(
        output_handle, delimiter='\t', lineterminator='\n')

    for row in input_reader:
        try:
            tax = tax_dict[row[1]]
        except KeyError:
            tax_str = "Unclassified"
        else:
            tax_str = ";".join(tax)
        output_writer.writerow([row[0], tax_str])

    input_handle.close()
    output_handle.close()
