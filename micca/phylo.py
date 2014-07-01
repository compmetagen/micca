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
import logging

import dendropy

logger = logging.getLogger('phylo')


def malign_denovo_muscle(in_filename, align_filename, fast=False):
    # muscle -in IN_FILENAME -out ALIGN_FILENAME [-maxiters 2]

    logger = logging.getLogger('phylo.malign_denovo_muscle')
    
    # muscle
    devnull = open(os.devnull, "w")
    cmd = ["muscle", "-in", in_filename, "-out", align_filename]
    if fast:
        cmd.extend(["-maxiters", "2"])
    logger.info(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=devnull, stderr=subprocess.PIPE)
    _, out_stderr = proc.communicate()
    devnull.close()
    if proc.returncode:
        logger.error(out_stderr)
        raise Exception(out_stderr)


def malign_denovo_tcoffe(in_filename, align_filename, num_threads=1):

    logger = logging.getLogger('phylo.malign_denovo_tcoffe')

    basepath = os.path.splitext(align_filename)[0]
    newtree = basepath + '.dnd'

    devnull = open(os.devnull, "w")
    cmd = ["t_coffee", "-in", in_filename, "-mode", "regular", "-output",
           "fasta_aln", "-maxlen", "-1", "-case",
           "upper", "-outorder", "input", "-outfile", align_filename,
           "-newtree", newtree]

    if num_threads == 1:
        cmd.extend(["-multi_core", "no"])
    else:
        cmd.extend(["-multi_core", "jobs", "-n_core", str(num_threads)])

    logger.info(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=devnull, stderr=subprocess.PIPE)
    _, out_stderr = proc.communicate()
    devnull.close()
    if proc.returncode:
        logger.error(out_stderr)
        raise Exception(out_stderr)

    os.remove(newtree)


def malign_template(in_filename, template_filename, align_filename,
                    min_perc_identity=75, min_len=100):

    logger = logging.getLogger('phylo.malign_template')
    basepath = os.path.splitext(align_filename)[0]
    
    # pynast
    devnull = open(os.devnull, "w")
    log_filename = basepath + "_PYNAST_LOG_TMP.txt"
    failure_filename = basepath + "_PYNAST_FAILURE_TMP.txt"
    cmd = ["pynast", "-i", in_filename, "-t", template_filename, "-p",
           str(min_perc_identity), "-l", str(min_len), "-a",
           align_filename, "-g", log_filename, "-f", failure_filename]
    logger.info(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=devnull, stderr=subprocess.PIPE)
    _, out_stderr = proc.communicate()
    devnull.close()
    if proc.returncode:
        logger.error(out_stderr)
        raise Exception(out_stderr)

    os.remove(log_filename)
    os.remove(failure_filename)

    
def build_tree(in_filename, tree_filename,
               tree_model="jc", tree_format="newick",
               fast=False):
    # FastTree [-gtr] [-fastest] -nt IN_FILENAME > TREE_FILENAME
    # tree model: Jukes-Cantor (jc) or generalized time-reversible (gtr)
    # tree format: phyloxml newick nexus

    logger = logging.getLogger('phylo.build_tree')
    basepath = os.path.splitext(tree_filename)[0]

    # FastTree
    fasttree_out_filename = basepath + "_FASTTREE_OUT_TMP.tre"
    fasttree_out_handler = open(fasttree_out_filename, "w")
    cmd = ["FastTree", "-nt", in_filename]
    if tree_model == "gtr":
        cmd.append("-gtr")
    if fast:
        cmd.append("-fastest")
    logger.info(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=fasttree_out_handler, 
                            stderr=subprocess.PIPE)
    _, out_stderr = proc.communicate()
    fasttree_out_handler.close()
    if proc.returncode:
        logger.error(out_stderr)
        raise Exception(out_stderr)

    tree = dendropy.Tree.get_from_path(fasttree_out_filename, schema="newick",
                                       as_rooted=False)
    tree.write_to_path(tree_filename, schema=tree_format,
                       suppress_rooting=True)

    os.remove(fasttree_out_filename)


def midpoint_rooting(in_filename, out_filename, tree_format="newick"):

    tree = dendropy.Tree.get_from_path(in_filename, schema=tree_format,
                                       as_rooted=False)
    tree.reroot_at_midpoint()
    tree.write_to_path(out_filename, schema=tree_format, suppress_rooting=True)
