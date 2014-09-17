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
import os
import os.path
import logging

from Bio import SeqIO
from Bio.Seq import Seq

import utils


logger = logging.getLogger('preproc')


def remove_fwd_primer(in_filename, out_filename, primer, max_error_rate=0.1,
                      min_overlap=10, search_rc=True):
    """Remove forward primers and discard untrimmed reads.

    cutadapt -g PRIMER [-a ...] -e MAX_ERROR_RATE -m 1 -O MIN_OVERLAP
        --discard-untrimmed IN_FILENAME > OUT_FILENAME
    """


    logger = logging.getLogger('preproc.remove_fwd_primer')
    out_handler = open(out_filename, 'w')
    
    cmd = ["cutadapt", "-f",  "fastq"]
    for uprimer in utils.adna2udna(primer.upper()):
        cmd.extend(["-g", uprimer])
        # reverse complement
        if search_rc:
            uprimer_rc = str(Seq(uprimer).reverse_complement())
            cmd.extend(["-g", uprimer_rc])
    cmd.extend(["-e", str(max_error_rate), "-m", "1", "-O", str(min_overlap),
                "--discard-untrimmed", in_filename])
    logger.info(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=out_handler, stderr=subprocess.PIPE)
    _, out_stderr = proc.communicate()
    out_handler.close()
    if proc.returncode:
        logger.error(out_stderr)
        raise Exception(out_stderr)


def remove_rev_primer(in_filename, out_filename, primer, max_error_rate=0.1,
                      min_overlap=10, search_rc=True):
    """Remove reverse primers.

    cutadapt -a PRIMER [-a ...] -e MAX_ERROR_RATE -m 1 -O MIN_OVERLAP 
        IN_FILENAME > OUT_FILENAME
    """

    logger = logging.getLogger('preproc.remove_rev_primer')
    out_handler = open(out_filename, 'w')

    cmd = ["cutadapt", "-f",  "fastq"]
    for uprimer in utils.adna2udna(primer.upper()):
        cmd.extend(["-a", uprimer])
        # reverse complement
        if search_rc:
            uprimer_rc = str(Seq(uprimer).reverse_complement())
            cmd.extend(["-a", uprimer_rc])
    cmd.extend(["-e", str(max_error_rate), "-m", "1", "-O", str(min_overlap),
                in_filename])
    logger.info(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=out_handler, stderr=subprocess.PIPE)
    _, out_stderr = proc.communicate()
    out_handler.close()
    if proc.returncode:
        logger.info(out_stderr)
        raise Exception(out_stderr)


def quality_trimming(in_filename, out_filename, min_length=200, min_quality=20,
                     fiveprime=False):
    """Quality trimming using sliding windows, ending Ns trimming,
    min length filtering.

     * sickle se -t sanger -l MIN_LENGTH -q MIN_QUALITY [-x] -f IN_FILENAME
         -o OUT_FILENAME
     * trim ending contiguous Ns
     * length trimming
    """


    def trim_ns(record):
        i = len(record) - 1
        while (record[i].upper() == 'N'):
            i -= 1
            if i < 0:
                break
        return record[:i+1]


    logger = logging.getLogger('preproc.quality_trimming')
    basepath, ext = os.path.splitext(out_filename)
    tmp_out_filename = basepath + "_SICKLE_TMP" + ext

    devnull = open(os.devnull, "w")
    cmd = ["sickle", "se", "-t", "sanger", "-l", str(min_length),
           "-q", str(min_quality), "-f", in_filename, "-o", tmp_out_filename]
    if not fiveprime:
        cmd.append("-x")
    logger.info(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=devnull, stderr=subprocess.PIPE)
    _, out_stderr = proc.communicate()
    devnull.close()
    if proc.returncode:
        logger.error(out_stderr)
        raise Exception(out_stderr)

    # remove ending Ns
    out_handler = open(out_filename, "w")
    logger.info("trimming contiguous ending Ns")
    for record in SeqIO.parse(tmp_out_filename, "fastq"):
        record_trimmed = trim_ns(record)
        if len(record_trimmed) >= min_length:
            SeqIO.write(record_trimmed, out_handler, "fastq")
    out_handler.close()

    os.remove(tmp_out_filename)
