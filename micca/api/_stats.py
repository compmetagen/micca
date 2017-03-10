##    Copyright 2015-2016 Davide Albanese <davide.albanese@gmail.com>
##    Copyright 2015-2016 Fondazione Edmund Mach (FEM)

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

import matplotlib
matplotlib.use('Agg')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from Bio.SeqIO.QualityIO import FastqGeneralIterator


def _stats(input_fn, topn=None):

    fastq_ascii=33

    nseqs, nbases = 0, 0
    len_count = np.array([], dtype=np.int, order='C')
    qual_count = np.zeros(128, dtype=np.int, order='C')
    qual_sum = np.array([], dtype=np.int, order='C')
    eerate_sum = np.array([], dtype=np.float, order='C')

    with open(input_fn, "r") as input_handle:
        for title, seq, qualstr in FastqGeneralIterator(input_handle):

            seqlen = len(seq)
            if (seqlen < 1):
                continue

            nseqs += 1
            nbases += seqlen
            if seqlen > len_count.shape[0]:
                len_count.resize(seqlen)
                qual_sum.resize(seqlen)
                eerate_sum.resize(seqlen)

            # returns values in [0, 127]
            qualint = np.fromstring(qualstr, dtype=np.int8)

            # phred quality
            qual = qualint - fastq_ascii

            # probability of error
            pe = 10**(-qual / 10.)

            # expected error
            ee = np.cumsum(pe)

            # expected error rate %
            eerate = (ee / np.arange(1, seqlen+1)) * 100

            len_count[seqlen-1] += 1
            qual_count += np.bincount(qualint, minlength=128)

            qual_sum[:seqlen] += qual
            eerate_sum[:seqlen] += eerate

            if (topn == nseqs):
                break

    if nseqs == 0:
        raise EOFError("no valid sequences in input file")

    # length distribution
    len_min, len_max = np.flatnonzero(len_count)[[0,-1]] + 1
    len_trim_range = np.arange(len_min, len_max+1)
    len_trim = len_count[len_trim_range-1]
    len_trim_cum = len_trim[::-1].cumsum()[::-1]
    len_trim_pct = (len_trim / nseqs) * 100
    len_trim_pct_cum = (len_trim_cum / nseqs) * 100
    len_dist = pd.DataFrame({
        "L":len_trim_range,
        "N": len_trim,
        "NCum": len_trim_cum,
        "NPct": len_trim_pct,
        "NPctCum":len_trim_pct_cum},
        columns=["L", "N", "NCum", "NPct", "NPctCum"])

    # quality distribution
    qual_min, qual_max = np.flatnonzero(qual_count)[[0,-1]] - fastq_ascii
    qual_trim_range = np.arange(qual_min, qual_max+1)
    qual_trim = qual_count[qual_trim_range + fastq_ascii]
    qual_trim_cum = qual_trim[::-1].cumsum()[::-1]
    qual_trim_pct = (qual_trim / nbases) * 100
    qual_trim_pct_cum = (qual_trim_cum / nbases) * 100
    qual_dist = pd.DataFrame({
        "Q": qual_trim_range,
        "N": qual_trim,
        "NCum": qual_trim_cum,
        "NPct": qual_trim_pct,
        "NPctCum":qual_trim_pct_cum},
        columns=["Q", "N", "NCum", "NPct", "NPctCum"])

    # quality summary
    len_range = np.arange(1, len_count.shape[0]+1)
    len_count_cum = len_count[::-1].cumsum()[::-1]
    len_count_pct = (len_count / nseqs) * 100
    len_count_pct_cum = (len_count_cum / nseqs) * 100
    qual_av = qual_sum / len_count_cum
    eerate_av = eerate_sum / len_count_cum
    qual_summ = pd.DataFrame({
        "L": len_range,
        "NPctCum": len_count_pct_cum,
        "QAv": qual_av,
        "EERatePctAv": eerate_av},
        columns=["L", "NPctCum", "QAv", "EERatePctAv"])

    return len_dist, qual_dist, qual_summ


def _plot_len_dist(values, output_fn):
    fig = plt.figure(figsize=(10, 8))

    ax1 = plt.subplot(311)
    plt.bar(values["L"]-0.5, values["N"], width=1, log=False,
            linewidth=0.5, color="white")
    ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
    plt.ylabel("# of reads")
    ax1.grid(True)

    ax2 = plt.subplot(312, sharex=ax1)
    plt.bar(values["L"]-0.5, values["NPct"], width=1, log=False,
            linewidth=0.5, color="white")
    plt.ylabel("# of reads %")
    ax2.grid(True)

    ax3 = plt.subplot(313, sharex=ax1)
    plt.plot(values["L"], values["NPctCum"], linewidth=1, color='black')
    plt.ylabel("# of reads % (cumulative)")
    ax3.grid(True)

    plt.xlabel("Read length")
    plt.xlim(values["L"].min()-0.5, values["L"].max()+0.5)

    fig.savefig(output_fn, bbox_inches='tight', dpi=300, format='png')


def _plot_qual_dist(values, output_fn):
    fig = plt.figure(figsize=(10, 8))

    ax1 = plt.subplot(311)
    plt.bar(values["Q"]-0.5, values["N"], width=1, log=False,
            linewidth=0.5, color="white")
    ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
    plt.ylabel("# of bases")
    ax1.grid(True)

    ax2 = plt.subplot(312, sharex=ax1)
    plt.bar(values["Q"]-0.5, values["NPct"], width=1, log=False,
            linewidth=0.5, color="white")
    plt.ylabel("# of bases %")
    ax2.grid(True)

    ax3 = plt.subplot(313, sharex=ax1)
    plt.plot(values["Q"], values["NPctCum"], linewidth=1, color='black')
    plt.ylabel("# of bases % (cumulative)")
    ax3.grid(True)

    plt.xlabel("Q score")
    plt.xlim(values["Q"].min()-0.5, values["Q"].max()+0.5)

    fig.savefig(output_fn, bbox_inches='tight', dpi=300, format='png')


def _plot_qual_summ(values, output_fn):
    fig = plt.figure(figsize=(10, 8))

    ax1 = plt.subplot(311)
    plt.plot(values["L"], values["NPctCum"], linewidth=1, color='black')
    plt.ylabel("# of reads % (cumulative)")
    ax1.grid(True)

    ax2 = plt.subplot(312, sharex=ax1)
    plt.plot(values["L"], values["QAv"], linewidth=1, color='black')
    plt.ylabel("Average Q")
    ax2.grid(True)

    ax3 = plt.subplot(313, sharex=ax1)
    plt.plot(values["L"], values["EERatePctAv"], linewidth=1, color='black')
    plt.ylabel("Av. Expected Error Rate %")
    ax3.grid(True)

    plt.xlabel("Read position")
    plt.xlim(values["L"].min(), values["L"].max())

    fig.savefig(output_fn, bbox_inches='tight', dpi=300, format='png')


def stats(input_fn, output_dir, topn=None):

    if not os.path.isdir(output_dir):
        raise ValueError("directory {} does not exist".format(output_dir))

    len_dist_fn = os.path.join(output_dir, "stats_lendist.txt")
    qual_dist_fn = os.path.join(output_dir, "stats_qualdist.txt")
    qual_summ_fn = os.path.join(output_dir, "stats_qualsumm.txt")

    len_dist_plot_fn = os.path.join(output_dir, "stats_lendist_plot.png")
    qual_dist_plot_fn = os.path.join(output_dir, "stats_qualdist_plot.png")
    qual_summ_plot_fn = os.path.join(output_dir, "stats_qualsumm_plot.png")

    len_dist, qual_dist, qual_summ = _stats(input_fn=input_fn, topn=topn)

    len_dist.to_csv(len_dist_fn, sep="\t", float_format="%.3f", index=False)
    qual_dist.to_csv(qual_dist_fn, sep="\t", float_format="%.3f", index=False)
    qual_summ.to_csv(qual_summ_fn, sep="\t", float_format="%.3f", index=False)

    # custom rc. "svg.fonttype: none" corrects the conversion of text in PDF
    # and SVG files
    rc = {
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.labelsize": 10,
        "legend.fontsize": 10,
        "svg.fonttype": "none"}

    with plt.rc_context(rc=rc):
        _plot_len_dist(len_dist, len_dist_plot_fn)
        _plot_qual_dist(qual_dist, qual_dist_plot_fn)
        _plot_qual_summ(qual_summ, qual_summ_plot_fn)
