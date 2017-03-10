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

import numpy as np
from Bio import SeqIO
from Bio.SeqIO.FastaIO import SimpleFastaParser

import micca.ioutils
import micca.tp

__all__ = ["nast", "muscle"]


class UnalignableError(Exception):
    pass


def _nast_core(template, template_aln, candidate_aln):

    # re-introduce template spacing in candidate and identify
    # template-extending insertions
    i, j, c = 0, 0, 0
    candidate_re = []
    insertions = []
    while True:
        if template[i] == template_aln[j]:
            candidate_re.append(candidate_aln[j])
            i+=1
            j+=1
        elif (template[i] == "-") and (template_aln[j] != "-"):
            candidate_re.append("-")
            i+=1
        elif (template[i] != "-") and (template_aln[j] == "-"):
            candidate_re.append(candidate_aln[j])
            insertions.append(c)
            j+=1
        else:
            raise ValueError("template and aligned template sequences do not "
                             "match")
        if (i == len(template)) or (j == len(template_aln)):
            break
        c+=1

    for k in range(i, len(template)):
        candidate_re.append('-')

    for k in range(j, len(template_aln)):
        candidate_re.append(candidate_aln[j])
        insertions.append(c)
        c+=1

    # search and remove nearest alignment spaces in candidate
    for i in insertions:
        dist_left, dist_right = 0, 0
        space_left, space_right = None, None

        # leftward search
        for j in range(i-1, -1, -1):
            dist_left += 1
            if candidate_re[j] == '-':
                space_left = j
                break

        # rightward search
        for j in range(i+1, len(candidate_re), 1):
            dist_right += 1
            if candidate_re[j] == '-':
                space_right = j
                break

        # choose the nearest space
        if (space_left is not None) and \
          ((space_right is None) or (dist_left <= dist_right)):
            candidate_re[space_left] = '!'
        elif (space_right is not None) and \
          ((space_left is None) or (dist_left > dist_right)):
            candidate_re[space_right] = '!'
        else:
            raise UnalignableError("too few spaces to remove in the aligned "
                                   "candidate sequence")

    candidate_nast = "".join([b for b in candidate_re if b != "!"])

    return candidate_nast


def _msa_count_columns(input_fn):
    """Count columns in a MSA in FASTA format.
    """
    with open(input_fn, "r") as input_handle:
        parser = SimpleFastaParser(input_handle)
        try:
            title, seq = parser.next()
        except StopIteration:
             raise ValueError("{} is not a valid FASTA template file"
                              .format(input_fn))
        seqlen = len(seq)
        for title, seq in parser:
            if len(seq) != seqlen:
                raise ValueError("sequences in template file must all be the "
                                 "same length")
    return seqlen


def _msa_remove_gaps(input_fn, output_fn):
    """Write a new file without gap characters (-).
    """

    input_handle = open(input_fn, "r")
    output_handle = open(output_fn, "wb")

    for title, seq in SimpleFastaParser(input_handle):
        seq = seq.replace('.', '-')
        output_handle.write(">{}\n{}\n".format(title, seq.replace('-', '')))

    input_handle.close()
    output_handle.close()


def _aln_to_seqs(aln, target, query):
    """Re-contruct query and target alignments from the VSEARCH alignment
    string.
    """

    query_aln, target_aln = [], []
    i, j = 0, 0
    for a in aln:
        if a == "I":
            query_aln.append("-")
            target_aln.append(target[j])
            j+=1
        elif a == "D":
            query_aln.append(query[i])
            target_aln.append('-')
            i+=1
        elif a =="M":
            query_aln.append(query[i])
            target_aln.append(target[j])
            i+=1
            j+=1
        else:
            raise ValueError("alignment string, query and target do not match")

    return "".join(target_aln), "".join(query_aln)


def _trim_candidate(template_aln, candidate_aln):

    alnlen = len(template_aln)

    if alnlen != len(candidate_aln):
        raise ValueError("template/candidate alignment do not match")

    for i in range(alnlen):
        if template_aln[i] != '-':
            start = i
            break

    for i in range(alnlen-1, -1, -1):
        if template_aln[i] != '-':
            end = i
            break

    return template_aln[start:end+1], candidate_aln[start:end+1]


def nast(input_fn, template_fn, output_fn, notaligned_fn=None, hits_fn=None,
         ident=0.75, threads=1, mincov=0.75, strand="both", nofilter=False,
         notrim=False):

    output_dir = os.path.dirname(output_fn)

    # get the number of columns in template file
    ncols = _msa_count_columns(template_fn)

    # remove gaps from MSA template
    template_wogaps_temp_fn = micca.ioutils.make_tempfile(output_dir)
    _msa_remove_gaps(template_fn, template_wogaps_temp_fn)

    # run VSEARCH
    hits_temp_fn = micca.ioutils.make_tempfile(output_dir)
    try:
        micca.tp.vsearch.usearch_global(
            input_fn=input_fn,
            db_fn=template_wogaps_temp_fn,
            userout_fn=hits_temp_fn,
            notmatched_fn=notaligned_fn,
            ident=ident,
            threads=threads,
            query_cov=mincov,
            maxaccepts=8,
            maxrejects=32,
            userfields="query+target+id+aln+qstrand",
            top_hits_only=True,
            strand=strand)
    except:
        os.remove(template_wogaps_temp_fn)
        os.remove(hits_temp_fn)
        raise

    # indexing
    input_records = SeqIO.index(input_fn, "fasta")
    template_records = SeqIO.index(template_fn, "fasta")
    template_wogaps_temp_records = SeqIO.index(template_wogaps_temp_fn, "fasta")

    # set up output temp file
    output_temp_fn = micca.ioutils.make_tempfile(output_dir)
    output_temp_handle = open(output_temp_fn, "wb")

    # set up hits_out file
    hits_out_fn = micca.ioutils.make_tempfile(output_dir)
    hits_out_handle = open(hits_out_fn, "wb")

    # set up hits reader
    hits_temp_handle = open(hits_temp_fn, 'rb')
    hits_temp_reader = csv.reader(hits_temp_handle, delimiter='\t')

    # set MSA coverage to zero
    msa_cov = np.zeros(ncols, dtype=np.int)

    prev_candidate_id = None
    for candidate_id, template_id, idp, aln, qstrand in hits_temp_reader:

        # get only the first candidate in the top hits
        if candidate_id != prev_candidate_id:

            # get the template
            template = str(template_records[template_id].seq.upper())
            template = template.replace('.', '-')

            # get the template without gaps
            template_wogaps = str(template_wogaps_temp_records[template_id]
                .seq.upper())

            # get the candidate
            candidate_seq = input_records[candidate_id].seq.upper()
            if qstrand == '-':
                candidate_seq = candidate_seq.reverse_complement()
            candidate = str(candidate_seq)

            # re-contruct query and target alignments
            template_aln, candidate_aln = _aln_to_seqs(
                aln, template_wogaps, candidate)

            # trim the candidate sequence to that which is bound by the
            # beginning and end points of the alignment span
            if not notrim:
                template_aln, candidate_aln = _trim_candidate(
                    template_aln, candidate_aln)

            try:
                candidate_msa = _nast_core(template, template_aln,
                                           candidate_aln)
            except UnalignableError:
                if notaligned_fn is not None:
                    # append the candidate sequence to the notaligned file if
                    # unalignable
                    notaligned_handle = open(notaligned_fn, 'ab')
                    candidate_out = ">{}\n{}\n".format(candidate_id, candidate)
                    notaligned_handle.write(candidate_out)
                    notaligned_handle.close()
            else:
                # update the coverage
                msa_cov += (np.array(list(candidate_msa)) != '-')

                # write the candidate sequence to the output temp file
                candidate_out = ">{}\n{}\n".format(candidate_id, candidate_msa)
                output_temp_handle.write(candidate_out)

                # write the hit to the hits file
                hit = "{}\t{}\t{}\n".format(candidate_id, template_id, idp)
                hits_out_handle.write(hit)

            finally:
                prev_candidate_id = candidate_id

    # close SeqIO.index files
    input_records.close()
    template_records.close()
    template_wogaps_temp_records.close()

    # close handles
    hits_temp_handle.close()
    output_temp_handle.close()
    hits_out_handle.close()

    # remove tmp files
    os.remove(hits_temp_fn)
    os.remove(template_wogaps_temp_fn)

    # remove columns which are gaps in every sequence
    if nofilter:
        os.rename(output_temp_fn, output_fn)
    else:
        output_temp_handle = open(output_temp_fn, "r")
        output_handle = open(output_fn, "wb")
        for title, seq in SimpleFastaParser(output_temp_handle):
            seqout = "".join(np.array(list(seq))[msa_cov > 0])
            output_handle.write(">{}\n{}\n".format(title, seqout))
        output_temp_handle.close()
        output_handle.close()
        os.remove(output_temp_fn)

    if hits_fn is None:
        os.remove(hits_out_fn)
    else:
        os.rename(hits_out_fn, hits_fn)


def muscle(input_fn, output_fn, maxiters=16):
    micca.tp.muscle.muscle(input_fn=input_fn, output_fn=output_fn,
                           maxiters=maxiters)
