``micca-levels``
================

Given an OTU table and a taxonomy file, micca-taxonomy builds an OTU table with
the taxomomy information and several OTU tables for each taxonomic level. OTU 
counts are summed together if they have the same consensus at the considered
level.

.. command-output:: micca-levels --help
