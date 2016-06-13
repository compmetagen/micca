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

from __future__ import division

import os
import os.path
import itertools

import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import micca.table
import micca.tax


def bar(input_fn, output_fn, raw=False, topn=12, xticklabelsize=8, fmt="png"):
    """plt.gcf().canvas.get_supported_filetypes()
    """
    table = micca.table.read(input_fn)

    # if raw is False, plot relative abundances
    if not raw:
        table = table / table.sum(axis=0)

    if topn > table.shape[0]:
        topn = table.shape[0]

    # sort by taxa abundances in decreasing order
    taxsum = table.sum(axis=1)
    taxsum.sort_values(ascending=False, inplace=True)
    table = table.reindex(taxsum.index)

    # sort by sample names
    table.sort_index(axis=1, inplace=True)

    # colors, hatches and edgecolors iterators
    ncolors = 12
    colors = [plt.cm.Paired(i) for i in np.linspace(0, 1, ncolors)]
    edgecolors = ['k', 'w']
    hatches = [None]*ncolors + ['////']*ncolors + ['xxxx']*ncolors
    itercolors = itertools.cycle(colors)
    iterhatches = itertools.cycle(hatches)
    iteredgecolors = itertools.cycle(edgecolors)

    # custom rc. "svg.fonttype: none" corrects the conversion of text in PDF
    # and SVG files
    rc = {"svg.fonttype": "none"}

    with plt.rc_context(rc=rc):

        fig = plt.figure(1)

        ax = plt.subplot(111)
        bars, bottom  = [], 0
        for i in range(topn):
            bar = plt.bar(np.arange(table.shape[1])+0.1, table.iloc[i],
                          bottom=bottom, linewidth=0, color=itercolors.next(),
                          hatch=iterhatches.next(),
                          edgecolor=iteredgecolors.next())

            bars.append(bar)
            bottom = table.iloc[0:i+1].sum(axis=0)

        lgd = ax.legend(bars, list(table.index), loc='center left',
                        frameon=False, bbox_to_anchor=(1, 0.5),
                        fontsize=8)

        ax.set_xticks(np.arange(table.shape[1])+0.5)
        ax.set_xticklabels(list(table.columns), rotation=90,
                           horizontalalignment='center', size=xticklabelsize)

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')

        plt.xlabel("Sample")
        plt.ylabel("Abundance")
        plt.xlim((0.0, table.shape[1]))
        if not raw:
            plt.ylim((0.0, 1.0))

        fig.savefig(output_fn, bbox_extra_artists=(lgd,), dpi=300,
                    bbox_inches='tight', format=fmt)


def rare(input_fn, output_fn, depth, replace=False, seed=0):

    table = micca.table.read(input_fn)
    raretable = micca.table.rarefy(table, depth=depth, replace=replace,
                                   seed=seed)
    micca.table.write(output_fn, raretable)


def totax(input_fn, tax_fn, output_dir):

    otutable = micca.table.read(input_fn)
    tax_dict = micca.tax.read(tax_fn)

    # keys() and values() always align so we can do the following
    # (https://docs.python.org/2/library/stdtypes.html#dict.items):
    tax_df = pd.DataFrame(tax_dict.values(), index=tax_dict.keys())
    tax_df.fillna("Unclassified", inplace=True)

    # build the table with taxonomy for each level
    for i in range(tax_df.shape[1]):
        taxtable = dict()
        for otuid, tax in tax_df.iloc[:, 0:i+1].iterrows():
            if otuid in otutable.index:
                tax = ";".join(tax)
                if taxtable.has_key(tax):
                    taxtable[tax] += otutable.loc[otuid]
                else:
                    taxtable[tax] = otutable.loc[otuid]
        taxtable = pd.DataFrame(taxtable).T
        taxtable.sort_index(inplace=True)
        taxtable.index.name = "OTU"
        taxtable_fn = os.path.join(output_dir, "taxtable{:d}.txt".format(i+1))
        micca.table.write(taxtable_fn, taxtable)


def stats(input_fn, output_dir, step=100, replace=False, seed=0):

    if not os.path.isdir(output_dir):
        raise ValueError("directory {} does not exist".format(output_dir))

    sample_summ_fn = os.path.join(output_dir, "tablestats_samplesumm.txt")
    otu_summ_fn = os.path.join(output_dir, "tablestats_otusumm.txt")
    rarecurve_fn = os.path.join(output_dir, "tablestats_rarecurve.txt")
    rarecurve_plot_fn = os.path.join(output_dir, "tablestats_rarecurve_plot.png")

    table = micca.table.read(input_fn)

    # sample summary
    sample_summ = pd.DataFrame({
        "Depth": table.sum(),
        "NOTU": (table > 0).sum(),
        "NSingle": (table == 1).sum()},
        columns=["Depth", "NOTU", "NSingle"])
    sample_summ.index.name = "Sample"
    sample_summ.sort_values(by="Depth", inplace=True)
    sample_summ.to_csv(sample_summ_fn, sep='\t')

    # OTU summary
    otu_summ = pd.DataFrame({
        "N": table.sum(axis=1),
        "NSample": (table > 0).sum(axis=1)},
        columns=["N", "NSample"])
    otu_summ.index.name = "OTU"
    otu_summ.sort_values(by="N", inplace=True, ascending=False)
    otu_summ.to_csv(otu_summ_fn, sep='\t')

    # rarefaction curves
    rarecurve = micca.table.rarecurve(table, step=step, replace=replace,
                                      seed=seed)
    rarecurve.to_csv(rarecurve_fn, sep='\t', float_format="%.0f", na_rep="NA")

    # custom rc. "svg.fonttype: none" corrects the conversion of text in PDF
    # and SVG files
    rc = {
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.labelsize": 10,
        "legend.fontsize": 10,
        "svg.fonttype": "none"}

    with plt.rc_context(rc=rc):
        fig = plt.figure(figsize=(10, 6))
        plt.plot(rarecurve.index, rarecurve.as_matrix(), color="k")
        plt.xlabel("Depth")
        plt.ylabel("#OTUs")
        fig.savefig(rarecurve_plot_fn, dpi=300, bbox_inches='tight', format="png")
