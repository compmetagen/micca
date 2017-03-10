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

from distutils.version import StrictVersion
import csv

import biom
if  StrictVersion(biom.__version__) >= StrictVersion("2.0.0"):
    from biom.table import Table
    _biom_version = 2
else:
    from biom.table import table_factory, SparseOTUTable
    _biom_version = 1

import micca.table
import micca.tax
from micca import __version__ as micca_version


def tobiom(input_fn, output_fn, tax_fn=None, sampledata_fn=None,
           otuids_fn=None):
    
    otutable = micca.table.read(input_fn)
    
    data = otutable.as_matrix()
    observation_ids = otutable.index.tolist()
    sample_ids = otutable.columns.tolist()
        
    if tax_fn is None:
        observ_metadata = None
    else:
        tax_dict = micca.tax.read(tax_fn)
        observ_metadata = []
        for oid in observation_ids:
            if tax_dict.has_key(oid):
                observ_metadata.append({"taxonomy": tax_dict[oid]})
            else:
                observ_metadata.append({"taxonomy": ["NA"]})
                
    if sampledata_fn is None:
        sample_metadata = None
    else:
        sampledata = micca.table.read(sampledata_fn)
        # re-index with the sample IDs in the OTU table
        sampledata = sampledata.reindex(sample_ids)
        sampledata.fillna("NA", inplace=True)
        sample_metadata = [sampledata.loc[sid].to_dict() for sid in sample_ids]

    # replace the OTU ids with the original sequence ids when found in otuids
    if otuids_fn is not None:
        with open(otuids_fn, "rU") as otuids_handle:
            otuids_reader = csv.reader(otuids_handle, delimiter="\t")
            otuids = dict([(row[0], row[1]) for row in otuids_reader])
            
        for i in range(len(observation_ids)):
            try:
                origid = otuids[observation_ids[i]]
            except KeyError:
                pass
            else:
                observation_ids[i] = origid

    generated_by="micca v.{}".format(micca_version)

    if _biom_version == 2:
        table = Table(
            data=data,
            sample_ids=sample_ids,
            observation_ids=observation_ids,
            sample_metadata=sample_metadata,
            observation_metadata=observ_metadata,
            type="OTU table")
        json_str = table.to_json(generated_by=generated_by)
    else:
        table = table_factory(
            data=data,
            sample_ids=sample_ids,
            observation_ids=observation_ids,
            sample_metadata=sample_metadata,
            observation_metadata=observ_metadata,
            constructor=SparseOTUTable)
        json_str = table.getBiomFormatJsonString(generated_by=generated_by)
        
    with open(output_fn, 'wb') as output_handle:
        output_handle.write(json_str)
