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

import os
import os.path
import csv
import re

import pandas as pd
from Bio.SeqIO.FastaIO import SimpleFastaParser

from Bio import SeqIO

import micca.ioutils
import micca.tp



_OTUTABLE_FN = "otutable.txt"
_OTUS_FN = "otus.fasta"
_OTUIDS_FN = "otuids.txt"
_HITS_FN = "hits.txt"
_OTUSCHIM_FN = "otuschim.fasta"


def _rename_seqids(input_fn, otuids_fn, prefix=""):
    output_dir = os.path.dirname(input_fn)

    tmp_fn = micca.ioutils.make_tempfile(output_dir)
    input_handle = open(input_fn, "rb")
    otuids_handle = open(otuids_fn, "wb")
    tmp_handle = open(tmp_fn, "wb")

    for i, (title, seq) in enumerate(SimpleFastaParser(input_handle)):
        origid = title.split()[0]
        newid = "{}{:d}".format(prefix, i+1)
        otuids_handle.write("{}\t{}\n".format(newid, origid))
        tmp_handle.write(">{}\n{}\n".format(newid, seq))

    tmp_handle.close()
    input_handle.close()
    otuids_handle.close()

    os.rename(tmp_fn, input_fn)


def _hits_to_otutable(hits_fn, otuids_fn, otutable_fn):

    with open(otuids_fn, 'rb') as otuids_handle:
        otuids_reader = csv.reader(otuids_handle, delimiter='\t')
        otuids = [(row[1], row[0]) for row in otuids_reader]
    ordered_otuids = [otuid[1] for otuid in otuids]
    otuids_dict = dict(otuids)

    otutable_dict = {}
    with open(hits_fn, 'rb') as hits_handle:
        hits_reader = csv.reader(hits_handle, delimiter='\t')
        for row in hits_reader:
            match = re.search("(^|;)sample=([^;]+)", row[0])
            if match:
                sample_name = match.group(2)
            else:
                sample_name = "noname"
            sample = otutable_dict.setdefault(sample_name, dict())
            otuid = otuids_dict[row[1]]
            sample.setdefault(otuid, 0)
            sample[otuid] += 1

    otutable = pd.DataFrame.from_dict(otutable_dict)
    otutable.fillna(0, inplace=True)
    otutable = otutable.astype(int)
    otutable = otutable.loc[ordered_otuids]
    otutable.to_csv(otutable_fn, sep='\t', index_label="OTU")


def _denovo_greedy(input_fn, otus_fn, otuids_fn, hits_fn, otuschim_fn,
                   otutable_fn=None, ident=0.97, threads=1, rmchim=False,
                   greedy="dgc", minsize=1):

    if greedy == "dgc":
        maxaccepts = 1
        sizeorder=False
    elif greedy == "agc":
        maxaccepts = 16
        sizeorder=True
    else:
        raise ValueError("greedy parameter must be 'dgc' or 'agc'")

    output_dir = os.path.dirname(otus_fn)

    # dereplication
    derep_fn = micca.ioutils.make_tempfile(output_dir)
    try:
        micca.tp.vsearch.derep_fulllength(input_fn, derep_fn, sizeout=True)
    except:
        os.remove(derep_fn)
        raise

    if os.stat(derep_fn).st_size == 0:
        os.remove(derep_fn)
        return

    # sort by size and filter by minimum size
    derep_sort_fn = micca.ioutils.make_tempfile(output_dir)
    try:
        micca.tp.vsearch.sortbysize(derep_fn, derep_sort_fn, minsize=minsize)
    except:
        os.remove(derep_sort_fn)
        raise
    finally:
        os.remove(derep_fn)

    if os.stat(derep_sort_fn).st_size == 0:
        os.remove(derep_sort_fn)
        return

    # greedy clustering
    otus_temp_fn = micca.ioutils.make_tempfile(output_dir)
    try:
        micca.tp.vsearch.cluster_smallmem(
            input_fn=derep_sort_fn,
            centroids_fn=otus_temp_fn,
            ident=ident,
            threads=threads,
            maxaccepts=maxaccepts,
            maxrejects=32,
            sizeorder=sizeorder,
            usersort=True,
            sizein=True,
            sizeout=rmchim,
            xsize=not rmchim)
    except:
        os.remove(otus_temp_fn)
        raise
    finally:
        os.remove(derep_sort_fn)

    # remove chimeras
    if rmchim:
        otus_nochim_fn = micca.ioutils.make_tempfile(output_dir)
        try:
            micca.tp.vsearch.uchime_denovo(
                input_fn=otus_temp_fn,
                chimeras_fn=otuschim_fn,
                nonchimeras_fn=otus_nochim_fn,
                xsize=True)
        except:
            os.remove(otus_nochim_fn)
            raise
        finally:
            os.remove(otus_temp_fn)

        if os.stat(otus_nochim_fn).st_size == 0:
            os.remove(otus_nochim_fn)
            return
    else:
        otus_nochim_fn = otus_temp_fn

    # map sequences to the representatives
    try:
        micca.tp.vsearch.usearch_global(
            input_fn=input_fn,
            db_fn=otus_nochim_fn,
            userout_fn=hits_fn,
            ident=ident,
            threads=threads,
            userfields="query+target+id",
            dbmatched_fn=otus_fn)
    finally:
        os.remove(otus_nochim_fn)

    _rename_seqids(otus_fn, otuids_fn, prefix="DENOVO")

    if otutable_fn is not None:
        _hits_to_otutable(hits_fn, otuids_fn, otutable_fn)


def _closed_ref(input_fn, ref_fn, otus_fn, otuids_fn, hits_fn,
                notmatched_fn=None, otutable_fn=None, ident=0.97, threads=1,
                mincov=0.75, strand="both"):

    micca.tp.vsearch.usearch_global(
        input_fn=input_fn,
        db_fn=ref_fn,
        userout_fn=hits_fn,
        ident=ident,
        threads=threads,
        userfields="query+target+id",
        query_cov=mincov,
        dbmatched_fn=otus_fn,
        notmatched_fn=notmatched_fn,
        strand=strand)

    _rename_seqids(otus_fn, otuids_fn, prefix="REF")
    if otutable_fn is not None:
        _hits_to_otutable(hits_fn, otuids_fn, otutable_fn)


def denovo_greedy(input_fn, output_dir, ident=0.97, threads=1, rmchim=False,
                  greedy="dgc", minsize=2):

    if not os.path.isdir(output_dir):
        raise ValueError("directory {} does not exist".format(output_dir))

    otus_fn = os.path.join(output_dir, _OTUS_FN)
    otuids_fn = os.path.join(output_dir, _OTUIDS_FN)
    hits_fn = os.path.join(output_dir, _HITS_FN)
    otuschim_fn = os.path.join(output_dir, _OTUSCHIM_FN)
    otutable_fn = os.path.join(output_dir, _OTUTABLE_FN)

    _denovo_greedy(
        input_fn=input_fn,
        otus_fn=otus_fn,
        otuids_fn=otuids_fn,
        hits_fn=hits_fn,
        otuschim_fn=otuschim_fn,
        otutable_fn=otutable_fn,
        ident=ident,
        threads=threads,
        rmchim=rmchim,
        greedy=greedy,
        minsize=minsize)


def closed_ref(input_fn, ref_fn, output_dir, ident=0.97, threads=1,
               mincov=0.75, strand="both"):

    if not os.path.isdir(output_dir):
        raise ValueError("directory {} does not exist".format(output_dir))

    otus_fn = os.path.join(output_dir, _OTUS_FN)
    otuids_fn = os.path.join(output_dir, _OTUIDS_FN)
    hits_fn = os.path.join(output_dir, _HITS_FN)
    otutable_fn = os.path.join(output_dir, _OTUTABLE_FN)

    _closed_ref(
        input_fn=input_fn,
        ref_fn=ref_fn,
        otus_fn=otus_fn,
        otuids_fn=otuids_fn,
        hits_fn=hits_fn,
        otutable_fn=otutable_fn,
        ident=ident,
        threads=threads,
        mincov=mincov,
        strand=strand)


def open_ref(input_fn, ref_fn, output_dir, ident=0.97, threads=1, mincov=0.75,
             rmchim=False, greedy="dgc", minsize=1, strand="both"):

    if not os.path.isdir(output_dir):
        raise ValueError("directory {} does not exist".format(output_dir))

    otus_fn = os.path.join(output_dir, _OTUS_FN)
    otuids_fn = os.path.join(output_dir, _OTUIDS_FN)
    hits_fn = os.path.join(output_dir, _HITS_FN)
    otuschim_fn = os.path.join(output_dir, _OTUSCHIM_FN)
    otutable_fn = os.path.join(output_dir, _OTUTABLE_FN)

    notmatched_fn = micca.ioutils.make_tempfile(output_dir)
    try:
        _closed_ref(
            input_fn=input_fn,
            ref_fn=ref_fn,
            otus_fn=otus_fn,
            otuids_fn=otuids_fn,
            hits_fn=hits_fn,
            notmatched_fn=notmatched_fn,
            otutable_fn=None,
            ident=ident,
            threads=threads,
            mincov=mincov,
            strand=strand)
    except:
        os.remove(notmatched_fn)
        raise

    if os.stat(notmatched_fn).st_size != 0:
        denovo_otus_fn = micca.ioutils.make_tempfile(output_dir)
        denovo_otuids_fn = micca.ioutils.make_tempfile(output_dir)
        denovo_hits_fn = micca.ioutils.make_tempfile(output_dir)

        try:
            _denovo_greedy(
                input_fn=notmatched_fn,
                otus_fn=denovo_otus_fn,
                otuids_fn=denovo_otuids_fn,
                hits_fn=denovo_hits_fn,
                otuschim_fn=otuschim_fn,
                otutable_fn=None,
                ident=ident,
                threads=threads,
                rmchim=rmchim,
                greedy=greedy,
                minsize=minsize)
        except:
            os.remove(denovo_otus_fn)
            os.remove(denovo_otuids_fn)
            os.remove(denovo_hits_fn)
            raise

        with open(otus_fn,'a') as otus_handle:
            with open(denovo_otus_fn,'r') as denovo_otus_handle:
                otus_handle.write(denovo_otus_handle.read())

        with open(otuids_fn,'a') as otuids_handle:
            with open(denovo_otuids_fn,'r') as denovo_otuids_handle:
                otuids_handle.write(denovo_otuids_handle.read())

        with open(hits_fn,'a') as hits_handle:
            with open(denovo_hits_fn,'r') as denovo_hits_handle:
                hits_handle.write(denovo_hits_handle.read())

        os.remove(denovo_otus_fn)
        os.remove(denovo_otuids_fn)
        os.remove(denovo_hits_fn)

    # END if os.stat(notmatched_fn).st_size != 0:

    os.remove(notmatched_fn)

    _hits_to_otutable(hits_fn, otuids_fn, otutable_fn)
