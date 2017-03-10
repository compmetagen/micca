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


def _stats(input_fn, topn=None, maxeerates=[0.25, 0.5, 0.75, 1, 1.25, 1.5],
           maxns=None):

    fastq_ascii = 33

    nseqs = 0
    eerate_minlen = np.array([], dtype=np.int, order='C')
    eerate_trunclen = np.array([], dtype=np.int, order='C')

    with open(input_fn, "r") as input_handle:
        for title, seq, qualstr in FastqGeneralIterator(input_handle):
            seqlen = len(seq)
            if (seqlen < 1):
                continue

            nseqs += 1
            if seqlen > eerate_minlen.shape[0]:
                eerate_minlen.resize((seqlen, len(maxeerates)))
                eerate_trunclen.resize((seqlen, len(maxeerates)))

            seq = seq.upper()
            qualint = np.fromstring(qualstr, dtype=np.int8)
            qual = qualint - fastq_ascii
            pe = 10**(-qual / 10.)
            ee = np.cumsum(pe)
            eerate = (ee / np.arange(1, seqlen+1)) * 100

            if maxns is None:
                for i, m in enumerate(maxeerates):
                    eerate_minlen[:seqlen, i] += (eerate[-1] <= m)
                    eerate_trunclen[:seqlen, i] += (eerate <= m)
            else:
                nnmask = (np.cumsum([s=='N' for s in seq]) <= maxns)
                for i, m in enumerate(maxeerates):
                    eerate_minlen[:seqlen, i] += (
                        (eerate[-1] <= m) and nnmask[-1])
                    eerate_trunclen[:seqlen, i] += np.logical_and(
                        (eerate <= m), nnmask)

            if (topn == nseqs):
                break

    if nseqs == 0:
        raise EOFError("no valid sequences in input file")

    lengths = pd.DataFrame({"L": np.arange(1, eerate_minlen.shape[0]+1)})

    eeratee_minlen_pct = pd.DataFrame(
        (eerate_minlen / nseqs) * 100, columns=maxeerates)
    minlen = pd.concat((lengths, eeratee_minlen_pct), axis=1)

    eeratee_trunclen_pct = pd.DataFrame(
        (eerate_trunclen / nseqs) * 100, columns=maxeerates)
    trunclen = pd.concat((lengths, eeratee_trunclen_pct), axis=1)

    return minlen, trunclen


def _plot(minlen, trunclen, output_fn):

    cmap = plt.cm.Paired
    colors = [cmap(i) for i in np.linspace(0, 1, minlen.shape[1])]

    fig = plt.figure(figsize=(10, 8))

    # minlen
    ax1 = plt.subplot(211)
    ax1.set_title("Min. length filtering (--minlen L)", fontsize=10)

    for i, maxeerate in enumerate(minlen.columns[1:]):
        plt.plot(minlen["L"], minlen[maxeerate], linewidth=2,
                 label="%.2f%%" % maxeerate, color=colors[i])

    plt.ylabel("# of reads %")
    plt.xlim(minlen["L"].min(), minlen["L"].max())
    plt.ylim((0, 100))
    ax1.grid(True)

    # minlen + truncation
    ax2 = plt.subplot(212, sharex=ax1)
    ax2.set_title("Min. length filtering + truncation (--minlen L --trunc)",
                  fontsize=10)

    for i, maxeerate in enumerate(trunclen.columns[1:]):
        plt.plot(trunclen["L"], trunclen[maxeerate], linewidth=2,
                 label="%.2f%%" % maxeerate, color=colors[i])

    plt.xlabel("L")
    plt.ylabel("# of reads %")
    plt.xlim(trunclen["L"].min(), trunclen["L"].max())
    plt.ylim((0, 100))
    ax2.grid(True)

    # legend
    lgd = ax1.legend(loc="center left", title="Max EE rate % (--maxeerate)",
                     bbox_to_anchor=(1, 0.5))
    plt.setp(lgd.get_title(), fontsize=10)

    fig.savefig(output_fn, bbox_inches='tight', dpi=300)


def filterstats(input_fn, output_dir, topn=None,
                maxeerates=[0.25, 0.5, 0.75, 1, 1.25, 1.5], maxns=None):

    if not os.path.isdir(output_dir):
        raise ValueError("directory {} does not exist".format(output_dir))

    minlen_fn = os.path.join(output_dir, "filterstats_minlen.txt")
    trunclen_fn = os.path.join(output_dir, "filterstats_trunclen.txt")
    plot_fn = os.path.join(output_dir, "filterstats_plot.png")

    minlen, trunclen = _stats(
        input_fn=input_fn,
        topn=topn,
        maxeerates=maxeerates,
        maxns=maxns)

    minlen.to_csv(minlen_fn, sep="\t", float_format="%.3f", index=False)
    trunclen.to_csv(trunclen_fn, sep="\t", float_format="%.3f", index=False)

    # custom rc. svg.fonttype": "none" corrects the conversion of text in PDF
    # and SVG files
    rc = {
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.labelsize": 10,
        "legend.fontsize": 10,
        "svg.fonttype": "none"}

    with plt.rc_context(rc=rc):
        _plot(minlen, trunclen, plot_fn)
