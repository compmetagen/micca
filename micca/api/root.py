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


from Bio import Phylo


def midpoint(input_fn, output_fn):
    tree = Phylo.read(input_fn, 'newick')
    tree.root_at_midpoint()
    Phylo.write(tree, output_fn, 'newick')

    
def outgroup(input_fn, output_fn, targets):
    tree = Phylo.read(input_fn, 'newick')
    leaf_names = [elem.name for elem in tree.get_terminals()]
    for t in targets:
       if not t in leaf_names:
           raise ValueError("taxa {} is not a leaf node".format(t))
    outgroup = [{"name": t} for t in targets]
    tree.root_with_outgroup(*outgroup)
    Phylo.write(tree, output_fn, 'newick')
    
