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

import micca.tp


def filter(input_fn, output_fn, maxee_rate, maxns=None, minlen=1, trunc=False,
           output_fmt="fasta"):
        
    if trunc:
        filter_minlen = 1
        filter_trunclen = minlen
    else:
        filter_minlen = minlen
        filter_trunclen = None
        
    fastqout_fn, fastaout_fn = None, None
    if output_fmt == "fasta":
        fastaout_fn = output_fn
    else:
        fastqout_fn = output_fn
        
    micca.tp.vsearch.fastq_filter(
        input_fn,
        fastqout_fn=fastqout_fn,
        fastaout_fn=fastaout_fn,
        fastq_trunclen=filter_trunclen,
        fastq_minlen=filter_minlen,
        fastq_maxee_rate=maxee_rate/100.,
        fastq_maxns=maxns)
