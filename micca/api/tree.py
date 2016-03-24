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

import micca.tp


def muscle(input_fn, output_fn, cluster="upgmb"):
    micca.tp.muscle.maketree(
        input_fn=input_fn,
        output_fn=output_fn,
        cluster=cluster)

    
def fasttree(input_fn, output_fn, gtr=False, fastest=False):
    micca.tp.fasttree(
        input_fn=input_fn,
        output_fn=output_fn,
        gtr=gtr,
        fastest=fastest)
