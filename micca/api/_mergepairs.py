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
import os
import os.path
import re
import warnings

import micca.ioutils
import micca.seq
import micca.tp


def mergepairs(input_fns, output_fn, reverse_fn=None, notmerged_fwd_fn=None,
               notmerged_rev_fn=None, minovlen=32, maxdiffs=8, pattern="_R1",
               repl="_R2", sep="_", nostagger=False):

    if not isinstance(input_fns, list):
        raise ValueError("input_fns must be of type list")

    if reverse_fn is not None:
        if not isinstance(reverse_fn, str):
            raise ValueError("reverse_fn must be of type string")

        if len(input_fns) != 1:
            raise ValueError("when the reverse filename is specified you must "
                             "indicate a single forward filename")

        if not os.path.isfile(reverse_fn):
            raise ValueError("{}: file does not exist or is not a regular "
                             "file".format(new_reverse_fn_base))

    # if reverse is not None create output files without appending sample names
    # to the sequence ids
    if reverse_fn is not None:
        micca.tp.vsearch.fastq_mergepairs(
            forward_fn=input_fns[0],
            reverse_fn=reverse_fn,
            fastqout_fn=output_fn,
            fastqout_notmerged_fwd_fn=notmerged_fwd_fn,
            fastqout_notmerged_rev_fn=notmerged_rev_fn,
            fastq_minovlen=minovlen,
            fastq_maxdiffs=maxdiffs,
            fastq_allowmergestagger=not nostagger,
            fastq_nostagger=nostagger)
    else:
        # output directory for temp files
        output_dir = os.path.dirname(output_fn)

        # close output files and create temp files
        output_fn_temp = micca.ioutils.make_tempfile(output_dir)
        output_fn_handle = open(output_fn, 'wb')

        if notmerged_fwd_fn is not None:
            notmerged_fwd_fn_temp = micca.ioutils.make_tempfile(output_dir)
            notmerged_fwd_handle = open(notmerged_fwd_fn, 'wb')
        else:
            notmerged_fwd_fn_temp = None

        if notmerged_rev_fn is not None:
            notmerged_rev_fn_temp = micca.ioutils.make_tempfile(output_dir)
            notmerged_rev_handle = open(notmerged_rev_fn, 'wb')
        else:
            notmerged_rev_fn_temp = None

        # for each input forward file
        for input_fn in input_fns:
            input_dir, input_fn_base = os.path.split(input_fn)

            # build the reverse filename
            reverse_fn_base, n = re.subn(pattern, repl, input_fn_base, count=1)
            if n == 0:
                warnings.warn(
                    "{0}: unable to find pattern '{1}', SKIP\n"
                    .format(input_fn_base, pattern))
                continue

            # check the reverse input file
            reverse_fn = os.path.join(input_dir, reverse_fn_base)
            if not os.path.isfile(reverse_fn):
                warnings.warn(
                    "{}: file does not exist or is not a regular file, SKIP\n"
                    .format(reverse_fn_base))
                continue

            # run VSEARCH
            try:
                micca.tp.vsearch.fastq_mergepairs(
                    forward_fn=input_fn,
                    reverse_fn=reverse_fn,
                    fastqout_fn=output_fn_temp,
                    fastqout_notmerged_fwd_fn=notmerged_fwd_fn_temp,
                    fastqout_notmerged_rev_fn=notmerged_rev_fn_temp,
                    fastq_minovlen=minovlen,
                    fastq_maxdiffs=maxdiffs,
                    fastq_allowmergestagger=not nostagger,
                    fastq_nostagger=nostagger)
            except micca.tp.vsearch.VSEARCHError as err:
                warnings.warn("{}: VSEARCH error: {}, SKIP\n"
                              .format(input_fn_base, err))
                continue

            # append sequences to the outuput files
            sample_name = re.sub('\s+', '_', input_fn_base.split(sep)[0])
            micca.seq.append(
                input_fn=output_fn_temp,
                output_handle=output_fn_handle,
                fmt="fastq",
                sample_name=sample_name)

            if notmerged_fwd_fn is not None:
                micca.seq.append(
                    input_fn=notmerged_fwd_fn_temp,
                    output_handle=notmerged_fwd_handle,
                    fmt="fastq",
                    sample_name=sample_name)

            if notmerged_rev_fn is not None:
                micca.seq.append(
                    input_fn=notmerged_rev_fn_temp,
                    output_handle=notmerged_rev_handle,
                    fmt="fastq",
                    sample_name=sample_name)

        # END for input_fn in input_fns:

        # close output files and remove temp files
        output_fn_handle.close()
        os.remove(output_fn_temp)
        if notmerged_fwd_fn is not None:
            notmerged_fwd_handle.close()
            os.remove(notmerged_fwd_fn_temp)
        if notmerged_rev_fn is not None:
            notmerged_rev_handle.close()
            os.remove(notmerged_rev_fn_temp)

    # END else:
