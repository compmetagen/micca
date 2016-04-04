CHANGES
=======

Version 1.2.0
-------------
* Hits output file option added to micca.api.msa.nast() (hits_fn
  option) and to the msa command (--nast-hits option);
* Improved setup.py.

Version 1.1.0
-------------

* strand option added in 'classify' (consensus-based classifier), 'msa' (NAST)
  and 'otu' (closed-reference and open reference OTU picking protolcols)
  commands. Now these commands search both strand (default) instead the plus
  strand only.

Version 1.0.0
-------------
* micca includes:

 * VSEARCH v1.9.5
 * MUSCLE v3.8.31
 * FastTree v2.1.8
