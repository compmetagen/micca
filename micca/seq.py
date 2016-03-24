import os
import re
from Bio import SeqIO


def append(input_fn, output_handle, fmt="fastq", sep=".", sample_name=None):
    """Appends the sequences present in the input file to the output file
    handle. Sample names are appended to the sequence identifier
    (e.g. >SEQID;sample=SAMPLENAME). Sample names are defined as: i)
    the leftmost part of the file name splitted by the first occurence
    of 'sep' if 'sample_name' is None; ii) 'sample_name' if
    'sample_name' is a string. Moreover, any whitespace character in
    the sample name is replaced with a single character underscore
    ('_').
    """
    
    def append_sample_name(records, sample_name):
        for record in records:
            record.id = "{0};sample={1}".format(record.id, sample_name)
            try:
                description = record.description.split(None, 1)[1]
            except IndexError:
                description = ""
            record.description = description
            yield record

    if sample_name is None:
        sample_name = os.path.basename(input_fn).split(sep)[0]
        
    sample_name_nows = re.sub('\s+', '_', sample_name)
    records_in = SeqIO.parse(input_fn, fmt)
    records_out = append_sample_name(records_in, sample_name_nows)
    SeqIO.write(records_out, output_handle, fmt)
