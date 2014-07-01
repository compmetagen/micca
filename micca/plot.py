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

from matplotlib import rcParams
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hierarchy
import scipy.spatial.distance as distance
import numpy as np


def stacked_bars(x, cmap=None):

    prng = np.random.RandomState(0)
    xa = np.asarray(x)
    
    if cmap is None:
        cmap = plt.cm.get_cmap(rcParams['image.cmap'])

    colors = [cmap(i) for i in np.linspace(0, 1, xa.shape[0])]
    prng.shuffle(colors)
    
    a = np.arange(xa.shape[1]) + 0.1
    bars  = []
    for i in range(xa.shape[0]):
        bm = xa[0:i, :].sum(axis=0)
        bar = plt.bar(a, xa[i, :], bottom=bm, color=colors[i], linewidth=0)
        bars.append(bar)
    return bars


def abundance_rank(x, cmap=None):
    xa = np.asarray(x)
    
    if cmap is None:
        cmap = plt.cm.get_cmap(rcParams['image.cmap'])

    colors = [cmap(i) for i in np.linspace(0, 1, xa.shape[0])]

    plots = []
    for i in range(xa.shape[0]):
        row = np.sort(xa[i])[::-1]
        row = row[row > 0.0]
        plot, = plt.plot(range(1, row.shape[0]+1), row, color=colors[i],
                         linewidth=2)
        plots.append(plot)
    return plots
