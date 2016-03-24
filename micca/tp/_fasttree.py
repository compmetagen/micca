import subprocess
import string
import os
import sys

from micca import THIRDPARTY_BIN_PATH


class FastTreeError(Exception):
    pass


def fasttree(input_fn, output_fn, gtr=False, fastest=False):
    fasttree_bin = os.path.join(THIRDPARTY_BIN_PATH, "fasttree")
    
    params = ["-nt", input_fn]
    if gtr:
        params.append("-gtr")
    if fastest:
        params.append("-fastest")

    params.insert(0, fasttree_bin)
    output_handle = open(output_fn, "wb")
    proc = subprocess.Popen(params, stdout=output_handle,
                            stderr=subprocess.PIPE)
    proc_stdout, proc_stderr = proc.communicate()
    output_handle.close()
    if proc.returncode:
        raise FastTreeError(proc_stderr)
