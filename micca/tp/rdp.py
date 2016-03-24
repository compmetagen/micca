import subprocess
import os
import sys
from distutils.spawn import find_executable

__all__ = ["RDPError", "classify"]


class RDPError(Exception):
    pass


def _get_rdpjar():
    rdppath = os.getenv("RDPPATH")
    if rdppath is None:
        raise Exception("RDPPATH environment variable is not set")
    rdpjar = os.path.join(rdppath, "dist/classifier.jar")
    if not os.path.isfile(rdpjar):
        raise Exception("no dist/classifier.jar found in RDPPATH")
    return rdpjar


def _rdp_cmd(params, maxmem=2):
    java_bin = find_executable("java")
    if java_bin is None:
        raise RDPError("Error: java is not installed\n")
    
    try:
        rdpjar = _get_rdpjar()
    except Exception as e:
        raise RDPError("Error: {0}\n".format(e))
         
    exe = [java_bin, "-Xmx{:d}g".format(maxmem), "-jar", rdpjar]
    exe.extend(params)
    proc = subprocess.Popen(exe, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc_stdout, proc_stderr = proc.communicate()
    if proc.returncode:
        raise RDPError(proc_stderr)


def classify(input_fn, output_fn, gene="16srrna", maxmem=2):
    params = ["classify", "-c", "0", "-f", "fixrank", "-g", gene, "-o", 
              output_fn, input_fn]
    _rdp_cmd(params)
