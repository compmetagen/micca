from __future__ import division

import numpy as np
from numpy.random import RandomState
import pandas as pd


def read(input_fn):
    """Read OTU/Taxa tables.
    """

    table = pd.read_csv(input_fn, sep='\t', index_col=0)

    # cast index into string
    table.index = [str(elem) for elem in table.index]

    return table


def write(output_fn, table):
    """Write OTU/Taxa tables.
    """

    table.to_csv(output_fn, sep='\t')


def _subsample(counts, n, replace=False, seed=0):
    """Randomly subsample from a vector of counts.

    Parameters
    ----------
    counts : 1-D array_like
        Vector of counts.
    n : int
        Number of element to subsample (<= the total number of counts).
    replace : bool, optional
        Subsample with or without replacement.
    seed : int, optional
        Random seed.

    Returns
    -------
    subcounts : 1-D ndarray
        Subsampled vector of counts

    Raises
    ------
    ValueError, TypeError
    """

    if n < 0:
        raise ValueError("'n' must be > 0 ")

    counts = np.asarray(counts)

    if counts.ndim != 1:
        raise ValueError("counts must be an 1-D array_like object")

    counts = counts.astype(int, casting='safe')
    counts_sum = counts.sum()

    if n > counts_sum:
        raise ValueError("'n' must be <= the total number of counts")

    prng = RandomState(seed)

    if replace:
        p = counts / counts_sum
        subcounts = prng.multinomial(n, p)
    else:
        nonzero = np.flatnonzero(counts)
        expanded = np.concatenate([np.repeat(i, counts[i]) for i in nonzero])
        permuted = prng.permutation(expanded)[:n]
        subcounts = np.bincount(permuted, minlength=counts.size)

    return subcounts


def _subsample_nonzero(counts, ns, replace=False, seed=0):
    """Randomly subsample from a vector of counts and returns the number of
    nonzero values for each number of element to subsample specified.

    Parameters
    ----------
    counts : 1-D array_like of integers
        Vector of counts.
    ns : 1-D array_like of integers
        List of numbers of element to subsample.
    replace : bool, optional
        Subsample with or without replacement.
    seed : int, optional
        Random seed.

    Returns
    -------
    nonzero : 1-D ndarray
        Number of nonzero values for each value of ns.

    Raises
    ------
    ValueError, TypeError
    """

    counts = np.asarray(counts)
    ns = np.asarray(ns)

    if counts.ndim != 1:
        raise ValueError("'counts' must be an 1-D array_like object")

    if (ns < 0).sum() > 0:
        raise ValueError("values in 'ns' must be > 0 ")

    counts = counts.astype(int, casting='safe')
    ns = ns.astype(int, casting='safe')

    counts_sum = counts.sum()

    prng = RandomState(seed)
    nonzero = []

    if replace:
        p = counts / counts_sum
        for n in ns:
            if n > counts_sum:
                nonzero.append(np.nan)
            else:
                subcounts = prng.multinomial(n, p)
                nonzero.append(np.count_nonzero(subcounts))
    else:
        nz = np.flatnonzero(counts)
        expanded = np.concatenate([np.repeat(i, counts[i]) for i in nz])
        permuted = prng.permutation(expanded)
        for n in ns:
            if n > counts_sum:
                nonzero.append(np.nan)
            else:
                subcounts = np.bincount(permuted[:n], minlength=counts.size)
                nonzero.append(np.count_nonzero(subcounts))

    return np.array(nonzero)


def rarefy(table, depth, replace=False, seed=0):
    """Rarefy a table of counts.

    Rarefy a table of integers by subsampling, with or without
    replacement. Samples that have fewer counts then the depth are
    omitted from the output table. OTUs that are not present in at
    least one sample are omitted from the output table.

    Parameters
    ----------
    table : pandas DataFrame of integers
        Table of counts (observations x samples).
    depth : int
        Number of element to subsample in each sample.
    replace : bool, optional
        Subsample with or without replacement.
    seed : int, optional
        Random seed.

    Returns
    -------
    raretable : pandas DataFrame of integers
        subsampled table of counts

    Raises
    ------
    ValueError, TypeError
    """

    if depth < 0:
        raise ValueError("'depth' must be > 0 ")

    if not isinstance(table, pd.DataFrame):
        raise TypeError("'table' must be a pandas DataFrame object")

    if table.values.dtype != 'int':
        raise TypeError("values in 'table' must be integers")

    # prune samples that have fewer counts than 'depth'
    table = table.loc[:, table.sum(axis=0) >= depth]

    # apply subsampling to the remaining samples
    raretable = table.apply(_subsample, axis=0, n=depth, replace=replace,
                            seed=seed)

    # prune OTUs that are not present in at least one sample
    raretable = raretable.loc[raretable.sum(axis=1) > 0]

    return raretable


def rarecurve(table, step, replace=False, seed=0):
    """Compute the rarefaction curves from a table of counts.

    Compute the rarefaction curve for each sample in 'table'. The
    rarefaction curves are evaluated using the interval of 'step'
    sample depths, always including 1 and the total sample size.

    Parameters
    ----------
    table : pandas DataFrame of integers
        Table of counts (observations x samples).
    step : int
        Sample depth interval.
    replace : bool, optional
        Subsample with or without replacement.
    seed : int, optional
        Random seed.

    Returns
    -------
    rarecurve : pandas DataFrame of floats
        Rarefaction curve table (depths x samples)

    Raises
    ------
    ValueError, TypeError
    """

    if not isinstance(table, pd.DataFrame):
        raise TypeError("'table' must be a pandas DataFrame object")

    if table.values.dtype != 'int':
        raise TypeError("values in 'table' must be integers")

    # depth of each sample
    sample_depths = table.sum(axis=0)

    # maximum sample depth in table
    sample_depth_max = sample_depths.max()

    # compute the list of depths
    depths = sorted(set([1] + range(step, sample_depth_max+1, step) +
                        sample_depths.tolist()))

    # create an empty DataFrame, depths x samples
    rarecurve = pd.DataFrame(index=depths, columns=table.columns, dtype='float')
    rarecurve.index.name = "Depth"

    for sample in table.columns:
        rarecurve[sample] = _subsample_nonzero(
            table[sample], ns=depths, replace=replace, seed=seed)

    return rarecurve
