#! /usr/bin/env python

##    Copyright 2016 Davide Albanese <davide.albanese@gmail.com>
##    Copyright 2016 Fondazione Edmund Mach (FEM)

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


import subprocess
import string
import os
import sys
from distutils.spawn import find_executable

from Bio.Seq import Seq


class CutadaptError(Exception):
    pass


def _cutadapt_cmd(params):
    cutadapt_bin = find_executable("cutadapt")
    if cutadapt_bin is None:
        CutadaptError("Error: cutadapt is not installed\n")
    
    params.insert(0, cutadapt_bin)
    proc = subprocess.Popen(params, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc_stdout, proc_stderr = proc.communicate()
    if proc.returncode:
        raise CutadaptError(proc_stderr)

    
def cutadapt(input_fn, output_fn, adapter=None, front=None, error_rate=0.1, 
             minimum_length=0, discard_untrimmed=False, fmt="fastq", 
             overlap=3, search_rc=False):
    
    params = [input_fn, "-o", output_fn, "-e", str(error_rate), "--format", fmt,
              "--minimum-length", str(minimum_length), "--overlap", str(overlap)]

    if adapter is not None:
        for a in adapter:
            params.extend(["-a", a])
            if search_rc:
                params.extend(["-a", str(Seq(a).reverse_complement())])

    if front is not None:
        for f in front:
            params.extend(["-g", f])
            if search_rc:
                params.extend(["-g", str(Seq(f).reverse_complement())])
    
    if discard_untrimmed:
        params.append("--discard-untrimmed")
        
    _cutadapt_cmd(params)
