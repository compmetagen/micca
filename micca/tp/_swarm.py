import subprocess
import os

from micca import THIRDPARTY_BIN_PATH

class SwarmError(Exception):
    pass


def _swarm_cmd(params):
    swarm_bin = os.path.join(THIRDPARTY_BIN_PATH, "swarm")
    params.insert(0, swarm_bin)
    proc = subprocess.Popen(params, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc_stdout, proc_stderr = proc.communicate()
    if proc.returncode:
        raise SwarmError(proc_stderr)

def swarm(input_fn, output_fn, seeds_fn=None, differences=1, fastidious=False,
          threads=1, usearch_abundance=False):

    params = [input_fn, "--output", output_fn, "--differences",
              str(differences), "--threads", str(threads)]
    if seeds_fn is not None:
        params.extend(["--seeds", seeds_fn])
    if fastidious:
        params.append("--fastidious")
    if usearch_abundance:
        params.append("--usearch-abundance")

    _swarm_cmd(params)
