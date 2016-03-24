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
import os
import sys

from micca import THIRDPARTY_BIN_PATH

__all__ = ["MUSCLEError", "muscle", "maketree"]


class MUSCLEError(Exception):
    pass


def _muscle_cmd(params):
    muscle_bin = os.path.join(THIRDPARTY_BIN_PATH, "muscle")
    
    params.insert(0, muscle_bin)
    proc = subprocess.Popen(params, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc_stdout, proc_stderr = proc.communicate()
    if proc.returncode:
        raise MUSCLEError(proc_stderr)

    
def muscle(input_fn, output_fn, maxiters=16):
    params =  ["-in", input_fn, "-out", output_fn, "-maxiters", str(maxiters)]
    _muscle_cmd(params)

    
def maketree(input_fn, output_fn, cluster="upgmb"):
    params =  ["-maketree", "-in", input_fn, "-out", output_fn, "-cluster", 
               cluster]
    _muscle_cmd(params)
