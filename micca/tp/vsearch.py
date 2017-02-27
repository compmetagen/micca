import subprocess
import string
import os
import sys

from micca import THIRDPARTY_BIN_PATH

__all__ = ["VSEARCHError", "sortbysize", "derep_fulllength", "uchime_denovo",
           "cluster_smallmem", "usearch_global", "fastq_filter",
           "fastx_subsample", "fastq_mergepairs"]


class VSEARCHError(Exception):
    pass


def _vsearch_cmd(params):
    vsearch_bin = os.path.join(THIRDPARTY_BIN_PATH, "vsearch")
    params.insert(0, vsearch_bin)
    proc = subprocess.Popen(params, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc_stdout, proc_stderr = proc.communicate()
    if proc.returncode:
        raise VSEARCHError(proc_stderr)


def sortbysize(input_fn, output_fn, minsize=1, xsize=False):

    params = ["--sortbysize", input_fn, "--minsize", str(minsize), "--output",
              output_fn]
    if xsize:
        params.append("--xsize")

    _vsearch_cmd(params)


def derep_fulllength(input_fn, output_fn, uc_fn=None, sizein=False,
                     sizeout=False, xsize=False):

    params = ["--derep_fulllength", input_fn, "--output", output_fn]
    if uc_fn is not None:
        params.extend(["--uc", uc_fn])
    if sizein:
        params.append("--sizein")
    if sizeout:
        params.append("--sizeout")
    if xsize:
        params.append("--xsize")

    _vsearch_cmd(params)


def uchime_denovo(input_fn, chimeras_fn=None, nonchimeras_fn=None,
                  sizeout=False, xsize=False):

    params = ["--uchime_denovo", input_fn]
    if chimeras_fn is not None:
        params.extend(["--chimeras", chimeras_fn])
    if nonchimeras_fn is not None:
        params.extend(["--nonchimeras", nonchimeras_fn])
    if sizeout:
        params.append("--sizeout")
    if xsize:
        params.append("--xsize")

    _vsearch_cmd(params)


def cluster_smallmem(input_fn, centroids_fn=None, ident=0.97, threads=1,
                     maxaccepts=1, maxrejects=32, sizeorder=False,
                     dbmask='dust', qmask='dust', usersort=False,
                     sizein=False, sizeout=False, xsize=False):

    params = ["--cluster_smallmem", input_fn, "--id", str(ident), "--maxaccepts",
              str(maxaccepts), "--maxrejects", str(maxrejects), "--threads",
              str(threads), "--dbmask", dbmask, "--qmask", qmask]

    if centroids_fn is not None:
        params.extend(["--centroids", centroids_fn])
    if sizeorder:
        params.append("--sizeorder")
    if sizein:
        params.append("--sizein")
    if sizeout:
        params.append("--sizeout")
    if xsize:
        params.append("--xsize")
    if usersort:
        params.append("--usersort")

    _vsearch_cmd(params)


def usearch_global(input_fn, db_fn, userout_fn=None, fastapairs_fn=None,
                   matched_fn=None, notmatched_fn=None, dbmatched_fn=None,
                   dbnotmatched_fn=None, ident=0.97, threads=1, query_cov=None,
                   maxaccepts=1, maxrejects=32, userfields="query+target+id",
                   dbmask='dust', qmask='dust', top_hits_only=False,
                   output_no_hits=False, strand="plus", sizeout=False):

    params = ["--usearch_global", input_fn, "--db",
              db_fn, "--id", str(ident), "--threads", str(threads),
              "--maxaccepts", str(maxaccepts), "--maxrejects", str(maxrejects),
              "--userfields", userfields, "--dbmask", dbmask, "--qmask", qmask,
              "--strand", strand]

    if userout_fn is not None:
        params.extend(["--userout", userout_fn])
    if matched_fn is not None:
        params.extend(["--matched", matched_fn])
    if notmatched_fn is not None:
        params.extend(["--notmatched", notmatched_fn])
    if dbmatched_fn is not None:
        params.extend(["--dbmatched", dbmatched_fn])
    if dbnotmatched_fn is not None:
        params.extend(["--dbnotmatched", dbnotmatched_fn])
    if fastapairs_fn is not None:
        params.extend(["--fastapairs", fastapairs_fn])
    if output_no_hits:
        params.append("--output_no_hits")
    if top_hits_only:
        params.append("--top_hits_only")
    if query_cov is not None:
        params.extend(["--query_cov", str(query_cov)])
    if sizeout:
        params.append("--sizeout")

    _vsearch_cmd(params)



def fastq_filter(input_fn, fastaout_fn=None, fastqout_fn=None,
                 fastq_trunclen=None, fastq_minlen=1, fastq_maxee_rate=None,
                 fastq_maxns=None, xsize=False):

    params = ["--fastq_filter", input_fn, "--fastq_minlen", str(fastq_minlen)]
    if fastaout_fn is not None:
        params.extend(["--fastaout", fastaout_fn])
    if fastqout_fn is not None:
        params.extend(["--fastqout", fastqout_fn])
    if fastq_trunclen is not None:
        params.extend(["--fastq_trunclen", str(fastq_trunclen)])
    if fastq_maxee_rate is not None:
        params.extend(["--fastq_maxee_rate", str(fastq_maxee_rate)])
    if fastq_maxns is not None:
        params.extend(["--fastq_maxns", str(fastq_maxns)])
    if xsize:
        params.append("--xsize")

    _vsearch_cmd(params)


def fastx_subsample(input_fn, fastaout_fn=None, fastqout_fn=None,
                    sample_size=None, sample_pct=None, randseed=0,
                    sizein=False, sizeout=False, xsize=False):

    params = ["--fastx_subsample", input_fn, "--randseed", str(randseed)]
    if fastaout_fn is not None:
        params.extend(["--fastaout", fastaout_fn])
    if fastqout_fn is not None:
        params.extend(["--fastqout", fastqout_fn])
    if sample_size is not None:
        params.extend(["--sample_size", str(sample_size)])
    if sample_pct is not None:
        params.extend(["--sample_pct", str(sample_pct)])
    if sizein:
        params.append("--sizein")
    if sizeout:
        params.append("--sizeout")
    if xsize:
        params.append("--xsize")

    _vsearch_cmd(params)


def fastq_mergepairs(forward_fn, reverse_fn, fastaout_fn=None, fastqout_fn=None,
                     fastaout_notmerged_fwd_fn=None, fastaout_notmerged_rev_fn=None,
                     fastqout_notmerged_fwd_fn=None, fastqout_notmerged_rev_fn=None,
                     fastq_minovlen=10, fastq_maxdiffs=5,
                     fastq_allowmergestagger=False, fastq_nostagger=True):

    params = ["--fastq_mergepairs", forward_fn, "--reverse", reverse_fn,
              "--fastq_maxdiffs", str(fastq_maxdiffs), "--fastq_minovlen",
              str(fastq_minovlen)]

    if fastaout_fn is not None:
        params.extend(["--fastaout", fastaout_fn])
    if fastqout_fn is not None:
        params.extend(["--fastqout", fastqout_fn])
    if fastaout_notmerged_fwd_fn is not None:
        params.extend(["--fastaout_notmerged_fwd", fastaout_notmerged_fwd_fn])
    if fastaout_notmerged_rev_fn is not None:
        params.extend(["--fastaout_notmerged_rev", fastaout_notmerged_rev_fn])
    if fastqout_notmerged_fwd_fn is not None:
        params.extend(["--fastqout_notmerged_fwd", fastqout_notmerged_fwd_fn])
    if fastqout_notmerged_rev_fn is not None:
        params.extend(["--fastqout_notmerged_rev", fastqout_notmerged_rev_fn])
    if fastq_allowmergestagger:
        params.extend(["--fastq_allowmergestagger"])
    if fastq_nostagger:
        params.extend(["--fastq_nostagger"])

    _vsearch_cmd(params)
