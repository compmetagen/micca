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

import micca.ioutils
import micca.tp


def trim(input_fn, output_fn, forward=None, reverse=None, maxerate=0.1,
         searchrc=False, duforward=False, dureverse=False, fmt="fastq"):
    
    if (forward is None) and (reverse is None):
        raise ValueError("at least one option between forward and reverse is "
                         "required")

    output_dir = os.path.dirname(output_fn)
  
    output_tmp_fn = micca.ioutils.make_tempfile(output_dir)
    try:
        micca.tp.cutadapt(
            input_fn=input_fn,
            output_fn=output_tmp_fn,
            front=forward,
            error_rate=maxerate, 
            minimum_length=1, 
            discard_untrimmed=duforward,
            fmt=fmt,
            search_rc=searchrc)
    except:
        os.remove(output_tmp_fn)
        raise

    if os.stat(output_tmp_fn).st_size == 0:
        os.rename(output_tmp_fn, output_fn)
        return
    
    try:
        micca.tp.cutadapt(
            input_fn=output_tmp_fn,
            output_fn=output_fn,
            adapter=reverse,
            error_rate=maxerate,
            minimum_length=1, 
            discard_untrimmed=dureverse,
            fmt=fmt,
            search_rc=searchrc)
    finally:
        os.remove(output_tmp_fn)
