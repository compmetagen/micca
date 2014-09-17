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


import subprocess
import csv
import os
import os.path
import glob
import logging
import sys

import pandas as pd
from Bio import SeqIO
from Bio.Blast import NCBIXML
import utils


logger = logging.getLogger('otu')


def clustering_ref(in_filename, ref_filename, clust_filename, rep_filename,
                   similarity=0.97):
    """
    """

    logger = logging.getLogger('otu.clustering_ref')

    basepath = os.path.splitext(clust_filename)[0]
    clust_tmp_filename = basepath + "_CLUST_TMP.txt"

    # run dnaclust
    clust_tmp_handler = open(clust_tmp_filename, 'w')
    cmd = ["dnaclust", in_filename, "-s", str(similarity), "--recruit-only",
           "-l", "--predetermined-cluster-centers", ref_filename]
    logger.info(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=clust_tmp_handler,
                            stderr=subprocess.PIPE)
    _, out_stderr = proc.communicate()
    clust_tmp_handler.close()
    if proc.returncode:
        logger.error(out_stderr)
        raise Exception(out_stderr)

    # rewrite the cluster file and load the cluster representatives
    clust_tmp_handler = open(clust_tmp_filename, 'r')
    clust_tmp_reader = csv.reader(clust_tmp_handler, delimiter='\t')
    clust_handler = open(clust_filename, 'w')
    clust_writer = csv.writer(clust_handler, delimiter='\t',
                              lineterminator='\n')
    clust_reps = []
    for row in clust_tmp_reader:
        row = [elem for elem in row if elem != '']
        if len(row) > 1:
            clust_reps.append(row[0])
            clust_writer.writerow(row[1:])
    clust_tmp_handler.close()
    clust_handler.close()

    records = SeqIO.index(ref_filename, "fasta")
    rep_handle = open(rep_filename, "w")
    for rep in clust_reps:
        SeqIO.write(records[rep], rep_handle, "fasta")
    rep_handle.close()

    os.remove(clust_tmp_filename)


def clustering_denovo(in_filename, clust_filename, rep_filename,
                      format='fasta', similarity=0.97, minsize=2,
                      remove_chimeras=False, derep_fast=False,
                      derep_fast_len=200):
    """
    """

    logger = logging.getLogger('otu.clustering_denovo')

    # run otuclust
    cmd = ["otuclust", in_filename, "-s", str(similarity), "-m",
           str(minsize), "--out-clust", clust_filename,  "--out-rep",
           rep_filename, "-f", format, "-l", str(derep_fast_len)]
    if remove_chimeras:
        cmd.append("-c")
    if derep_fast:
        cmd.append("-d")
    logger.info(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=sys.stdout, stderr=subprocess.PIPE)
    _, out_stderr = proc.communicate()
    if proc.returncode:
        logger.error(out_stderr)
        raise Exception(out_stderr)


def taxonomy_blast(in_filename, ref_filename, ref_taxonomy_filename,
                   out_filename, task='blastn', num_threads=1, evalue=10e-30,
                   perc_identity=90):
    """Assign taxonomy.

    1) makeblastdb -in REF_FILENAME -parse_seqids -dbtype nucl -out DB_FILENAME
    2) blastn -task blastn -db DB_FILENAME -query IN_FILENAME -out BLAST_OUT_FILENAME[.xml]
       -evalue EVALUE -perc_identity PERC_IDENTITY -num_threads NUM_THREADS -outfmt 5
    3) load reference taxonomy file (REF_TAXONOMY_FILENAME)
    4) write the taxonomy file (OUT_FILENAME)
    """

    logger = logging.getLogger('otu.taxonomy_blast')
    basepath = os.path.splitext(out_filename)[0]

    # makeblastdb
    db_prefix = basepath + "_BLAST_DB_TMP"
    devnull = open(os.devnull, "w")
    cmd = ["makeblastdb", "-in", ref_filename, "-parse_seqids", "-dbtype",
           "nucl", "-out", db_prefix]
    logger.info(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=devnull, stderr=subprocess.PIPE)
    _, out_stderr = proc.communicate()
    devnull.close()
    if proc.returncode:
        logger.error(out_stderr)
        raise Exception(out_stderr)

    # blastn
    blast_out_filename = basepath + "_BLAST_OUT_TMP.xml"
    devnull = open(os.devnull, "w")
    cmd = ["blastn", "-task", task, "-db", db_prefix, "-query", in_filename,
           "-out", blast_out_filename, "-evalue", str(evalue), "-perc_identity",
           str(perc_identity), "-num_threads", str(num_threads), "-outfmt", "5"]
    logger.info(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=devnull, stderr=subprocess.PIPE)
    _, out_stderr = proc.communicate()
    devnull.close()
    if proc.returncode:
        logger.error(out_stderr)
        raise Exception(out_stderr)

    logger.info("write the taxonomy file %s" % os.path.basename(out_filename))

    # load reference taxonomy file
    ref_taxonomy_handler = open(ref_taxonomy_filename, 'r')
    ref_taxonomy_reader = csv.reader(ref_taxonomy_handler, delimiter='\t')
    ref_taxonomy = dict()
    for row in ref_taxonomy_reader:
        ref_taxonomy[row[0]] = utils.parse_taxonomy(row[1])
    ref_taxonomy_handler.close()

    # write the output file
    blast_out_handle = open(blast_out_filename, 'r')
    blast_out_records = NCBIXML.parse(blast_out_handle)
    out_handle = open(out_filename, 'w')
    out_writer = csv.writer(out_handle, delimiter='\t', lineterminator='\n')
    for record in blast_out_records:
        if len(record.alignments) > 0:
            best_hit_id = record.alignments[0].hit_id
            ta = ref_taxonomy[best_hit_id]
        else:
            ta = "Unknown"
        out_writer.writerow([record.query, ta])
    out_handle.close()
    blast_out_handle.close()

    # delete tmp files
    for filename in glob.glob(db_prefix + '*'):
        os.remove(filename)
    os.remove(blast_out_filename)


def taxonomy_rdp(in_filename, out_filename, max_memory=2000,
                 min_confidence=0.80, gene="16srrna"):
    """Assign taxonomy through RDP classifier/database. 
    Versions 2.6, 2.7 and 2.8 are supported.
    Gene options:
    16srrna or fungallsu for 2.6, 2.7
    16srrna, fungallsu, fungalits_warcup, fungalits_unite for 2.8
    """

    def get_rdpjar():
        rdppath = os.getenv("RDPPATH")
        if rdppath is None:
            raise Exception("RDPPATH environment variable is not set")
        rdpjar = os.path.join(rdppath, "dist/classifier.jar")
        if not os.path.isfile(rdpjar):
            raise Exception("no dist/classifier*.jar found in RDPPATH")
        return rdpjar

    logger = logging.getLogger('otu.taxonomy_rdp')
    ta_cols = [2, 5, 8, 11, 14, 17]
    confidence_cols = [4, 7, 10, 13, 16, 19]

    basepath = os.path.splitext(out_filename)[0]

    try:
        rdpjar = get_rdpjar()
        logger.info("RDP jar file found in %s" % rdpjar)
    except Exception, e:
        logger.error(e)
        raise Exception(e)

    # rdp classifier
    rdp_out_filename = basepath + "_RDP_OUT_TMP.txt"
    devnull = open(os.devnull, "w")
    cmd = ["java", "-Xmx%dm" % max_memory, "-jar", rdpjar, "classify", "-c",
           "0", "-f", "fixrank", "-g", gene, "-o", rdp_out_filename,
           in_filename]
    logger.info(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=devnull, stderr=subprocess.PIPE)
    _, out_stderr = proc.communicate()
    devnull.close()
    if proc.returncode:
        logger.error(out_stderr)
        raise Exception(out_stderr)

    logger.info("write the taxonomy file %s" % os.path.basename(out_filename))

    # load the sequence ids
    query_ids = [record.id for record in SeqIO.parse(in_filename, "fasta")]

    # load the rdp output file
    rdp = pd.read_csv(rdp_out_filename, sep='\t', header=None, index_col=0)

    # write the output file
    out_handle = open(out_filename, 'w')
    out_writer = csv.writer(out_handle, delimiter='\t', lineterminator='\n')
    for query_id in query_ids:
        try:
            row = rdp.loc[query_id]
        except KeyError:
            ta = "Unknown"
        else:
            ta_list = [row[i] for i in ta_cols]
            confidence = [row[i] for i in confidence_cols]

            # filter taxonomy by confidence
            w = len(confidence)
            for i in range(len(confidence)):
                if confidence[i] < min_confidence:
                    w = i
                    break
            ta_list = ta_list[:w]

            if len(ta_list) > 0:
                ta = ';'.join(ta_list)
            else:
                ta = "Unknown"

        out_writer.writerow([query_id, ta])
    out_handle.close()

    os.remove(rdp_out_filename)


def taxonomy_ref(in_filename, ref_taxonomy_filename, out_filename):
    """
    """


    logger = logging.getLogger('otu.taxonomy_ref')

    # load the taxonomy file
    ref_taxonomy_handler = open(ref_taxonomy_filename, 'r')
    ref_taxonomy_reader = csv.reader(ref_taxonomy_handler, delimiter='\t')
    ref_taxonomy = dict()
    for row in ref_taxonomy_reader:
        ref_taxonomy[row[0]] = utils.parse_taxonomy(row[1])
    ref_taxonomy_handler.close()

    # write the taxonomy file
    #logger.info("write the taxonomy file %s" % os.path.basename(out_filename)
    out_handle = open(out_filename, 'w')
    out_writer = csv.writer(out_handle, delimiter='\t', lineterminator='\n')
    for record in SeqIO.parse(in_filename, "fasta"):
        out_writer.writerow([record.id, ref_taxonomy[record.id]])
    out_handle.close()


def build_otu_table(clust_filename, rep_filename, otu_table_filename):
    """Build the OTU table from a clustering file.
    """

    logger = logging.getLogger('otu.build_otu_table')
    logger.info("build the OTU table %s" % os.path.basename(otu_table_filename))

    clust_handler = open(clust_filename, 'r')
    clust_reader = csv.reader(clust_handler, delimiter='\t')

    # get the sample names from the clustering file
    sample_names = set()
    for row in clust_reader:
        for elem in row:
            sample_names.add(elem.split('||')[0])
    sample_names = sorted(list(sample_names))

    # build OTU table
    clust_handler.seek(0)
    otu_table_handler = open(otu_table_filename, 'w')
    otu_table_writer = csv.writer(otu_table_handler, delimiter='\t',
                                  lineterminator='\n')
    otu_table_writer.writerow(["OTU"] + sample_names)
    otu_ids = [record.id for record in SeqIO.parse(rep_filename, "fasta")]
    for i, row in enumerate(clust_reader):
        otu_id = otu_ids[i]
        counts = [0] * len(sample_names)
        for elem in row:
            sample_name = elem.split('||')[0]
            idx = sample_names.index(sample_name)
            counts[idx] += 1
        otu_table_writer.writerow([otu_id] + counts)
    otu_table_handler.close()
    clust_handler.close()


def merge_seqs(in_filenames, out_filename, in_fmt='fastq', out_fmt='fastq'):
    """Merge seq files. Record ids are converted in 
    [FILENAME_WITHOUT_EXT]_N.
    """

    logger = logging.getLogger('otu.merge_seqs')
    logger.info("merge files: " + ', '.join(in_filenames))

    def convert_id(records, basename):
        for i, record in enumerate(records):
            record.id = "%s||%s" % (basename, record.id)
            record.description = record.id
            yield record

    in_basenames = [os.path.splitext(os.path.basename(in_filename))[0] \
                    for in_filename in in_filenames]
    if len(set(in_basenames)) != len(in_basenames):
        raise ValueError("input files must have different names")

    out_handle = open(out_filename, 'w')
    for filename, in_basename in zip(in_filenames, in_basenames):
        in_records = SeqIO.parse(filename, in_fmt)
        out_records = convert_id(in_records, in_basename)
        SeqIO.write(out_records, out_handle, out_fmt)
    out_handle.close()
