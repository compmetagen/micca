## This code is written by Davide Albanese, <davide.albanese@gmail.com>
## Copyright (C) 2013 Fondazione Edmund Mach
## Copyright (C) 2013 Davide Albanese

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division

import os.path

import numpy as np
from numpy.random import RandomState
import pandas as pd


def rarefy_otu_table(in_filename, out_filename, perc=80, seed=0):
    """Rarefy OTU table to perc% of the least abundant sample. 
    """

    # Read OTU table
    otu_table = pd.read_csv(in_filename, sep='\t', index_col=0)
        
    # rarefaction
    prng = RandomState(seed)
    n_reads = otu_table.sum()
    depth = n_reads.min() * (perc / 100)
    for sample in otu_table:
        prob = otu_table[sample] / n_reads[sample]
        choice = prng.choice(otu_table.shape[0], depth, p=np.asarray(prob))
        otu_table[sample] = np.bincount(choice, minlength=otu_table.shape[0])

    # OTU pruning
    otu_table = otu_table.loc[otu_table.sum(axis=1) > 0]

    # Write OTU table
    otu_table.to_csv(out_filename, sep='\t')


def filter_otu_table(in_filename, out_filename, min_count=None, max_count=None):
    """Filter OTUs from an OTU table based on their observation counts.
    """
    
    otu_table = pd.read_csv(in_filename, sep='\t', index_col=0)
    counts = otu_table.sum(axis=1)
    
    if min_count:
        otu_table = otu_table.loc[counts >= min_count]
        
    if max_count:
        otu_table = otu_table.loc[counts <= max_count]
        
    otu_table.to_csv(out_filename, sep='\t')

    
def split_otu_table(in_filename, out_dirname):
    """Split the OTU table (with taxonomic information) into
    several OTU tables for each taxonomic level. OTU counts 
    are summed together if they have the same consensus at 
    the considered level.
    """

    # load OTU table
    otu_table = pd.read_csv(in_filename, sep='\t', index_col=0)

    # max number of levels
    n_levels = np.max([len(taxonomy.split(';')) 
                       for taxonomy in otu_table.index])
    
    # write taxonomy table for each taxonomic level
    prefix, ext = os.path.splitext(os.path.basename(in_filename))
    for i in range(1, n_levels+1):
        level_table = dict()
        for taxonomy, counts in otu_table.iterrows():
            taxonomy_list = taxonomy.split(';')
            n = len(taxonomy_list)
            if n < i:
                taxonomy = ";".join(taxonomy_list + (["Unknown"] * (i-n)))
            else:
                taxonomy = ";".join(taxonomy_list[:i])
            if not level_table.has_key(taxonomy):
                level_table[taxonomy] = counts
            else:
                level_table[taxonomy] += counts

        out_filename = os.path.join(out_dirname,
                                    prefix + "_level_%d" % (i) + ext)
        level_table = pd.DataFrame(level_table).T
        level_table.to_csv(out_filename, sep='\t', index_label="OTU")


def taxonomy_otu_table(otu_table_filename, taxonomy_filename,
                       otu_table_taxonomy_filename):
    """Build the OTU table with taxonomic information from a
    otu_table file and a taxonomy file. OTU counts are summed
    together if they have the same consensus.
    """

    otu_table = pd.read_csv(otu_table_filename, sep='\t', index_col=0)
    taxonomy = pd.read_csv(taxonomy_filename, sep='\t', index_col=0,
                           header=None, squeeze=True)
    otu_table_taxonomy = pd.DataFrame(
        index=pd.Series(taxonomy.unique(), name="OTU"),
        columns=otu_table.columns)
    otu_table_taxonomy = otu_table_taxonomy.fillna(0)

    # build the taxonomy table
    for id in otu_table.index:
        t = taxonomy[id]
        otu_table_taxonomy.loc[t] += otu_table.loc[id]

    # OTU pruning
    otu_table_taxonomy = \
        otu_table_taxonomy.loc[otu_table_taxonomy.sum(axis=1) > 0]

    otu_table_taxonomy.to_csv(otu_table_taxonomy_filename, sep='\t')
