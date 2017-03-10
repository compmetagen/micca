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

import os
import re
import csv


class TaxReader:
    def __init__(self, handle):
        self.__handle = handle
        self.__reader = csv.reader(handle, delimiter='\t')

    def __iter__(self):
        return self

    def __parse_tax(self, s):
        """Parse a taxonomy string and returns a list.
        """
        tax = []
        for elem in s.split(';'):
            elem = re.sub(r"^\S__|^D_\d+__", "", elem.strip())
            if elem == "":
                break
            tax.append(elem)
        return tax

    def next(self):
        row = self.__reader.next()
        return row[0], self.__parse_tax(row[1])


def read(input_fn):
    """Parse a tab-delimited taxonomy file where rows are in the form:
    SEQID[TAB]k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__; g__;
    or:
    SEQID[TAB]Bacteria;Firmicutes;Clostridia;Clostridiales;;;
    or:
    D_0__Bacteria;D_1__Firmicutes;D_2__Clostridia;D_3__Clostridiales;D_4__Clostridiaceae 1
    Any external whitespace character and taxonomy prefix (e.g. 'p__' in
    Greengenes and 'D_2__' in QIIME formatted Silva taxonomy files) are stripped
    out. Returns a dictionary containing 'sequence id'/'list of taxa' pairs.
    """

    tax_dict = dict()
    with open(input_fn, 'rU') as input_handle:
        taxreader = TaxReader(input_handle)
        for seqid, tax in taxreader:
            tax_dict[seqid] = tax
    return tax_dict
