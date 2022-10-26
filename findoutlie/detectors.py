""" Utilities for detecting outliers

These functions take a vector of values, and return a boolean vector of the
same length as the input, where True indicates the corresponding value is an
outlier.

The outlier detection routines will likely be adapted to the specific measure
that is being worked on.  So, some detector functions will work on values > 0,
other on normally distributed values etc.  The routines should check that their
requirements are met and raise an error otherwise.
"""

# Any imports you need
# +++your code here+++
import numpy as np

from scipy.stats import norm

def mad_voxel_detector(img,threshold=3.5):
    """ Detect outliers in 'img' using mediaan absolute deviation.
    Returns 2D vector of same shape as 'img', where True means the corresponding
    value in 'img' is an outlier.

    Call med as median per voxel and mad as median absolute deviation per voxel of the 'img' 
 
    Parameters
    ----------
    img : 2D array 
        Values for which we will detect outliers
    p : float, optional
        Scalar to multiply the median absolute deviation 
        to form the upper and lower threshold. Default is 3.5.

    Returns
    -------
    outlier_tf : 2D boolean array
        2D boolean array of same shape as 'img', where True means the corresponsding value in 'img' 
        is an outlier.
    """
    # Calculate median per voxel
    med = np.expand_dims(np.nanmedian(img,axis=-1),axis=1)
    # Calculate mean absolute deviation per voxel
    mad = np.expand_dims(np.nanmedian(np.abs(img-med),axis=-1),axis=1)
    # calculate the outliers
    outlier_tf = np.abs(img-med)>(threshold*mad)
    return outlier_tf

def mad_time_detector(measures, lower_bound, threshold=3.5):
    """ Detect outliers in 'measures' using median absolute deviation.
    Returns 1D vector of same length as 'measures', where True means the corresponsding 
    value in 'measures' is an outlier.

    Call med as median and mad as median absolute deviation of the 'measures'
    
    Parameters
    ----------
    measures : 1D array
        Values for which we will detect outliers
    threshold : float, optional
        Scalar to multiply the median aboslute deviation to form the upper threshold. 
        Default is 3.5.
    
    Returns
    -------
    outlier_tf : 1D boolean array
        1D boolean array of same length as 'measures', where True means the 
        corresponding value in 'measures' is an outlier. 
    """
    # Calculate median of measures
    med = np.median(measures)
    # Calculate median absoulte deviation of measures
    mad = np.median(np.abs(measures-med))
    # Calculate the outliers
    if lower_bound:
        outlier_tf = np.abs(measures-med)>threshold*mad
    else:
        outlier_tf = measures>med+threshold*mad
    return outlier_tf

def iqr_detector(measures, iqr_proportion=1.5):
    """ Detect outliers in `measures` using interquartile range.

    Returns a boolean vector of same length as `measures`, where True means the
    corresponding value in `measures` is an outlier.

    Call Q1, Q2 and Q3 the 25th, 50th and 75th percentiles of `measures`.

    The interquartile range (IQR) is Q3 - Q1.

    An outlier is any value in `measures` that is either:

    * > Q3 + IQR * `iqr_proportion` or
    * < Q1 - IQR * `iqr_proportion`.

    See: https://en.wikipedia.org/wiki/Interquartile_range

    Parameters
    ----------
    measures : 1D array
        Values for which we will detect outliers
    iqr_proportion : float, optional
        Scalar to multiply the IQR to form upper and lower threshold (see
        above).  Default is 1.5.

    Returns
    -------
    outlier_tf : 1D boolean array
        A boolean vector of same length as `measures`, where True means the
        corresponding value in `measures` is an outlier.
    """
    # Any imports you need
    # Hints:
    # * investigate np.percentile
    # * You'll likely need np.logical_or
    # https://textbook.nipraxis.org/numpy_logical.html
    # +++your code here+++
    # Calculate the quartiles of the data
    Q1 = np.percentile(measures, 25, interpolation="midpoint")
    Q2 = np.percentile(measures, 50, interpolation="midpoint")
    Q3 = np.percentile(measures, 75, interpolation="midpoint")
    # Calculate the interquartile range
    IQR = Q3 - Q1
    # Calculate the outliers
    outlier_tf = np.logical_or(measures > (Q3 + IQR * iqr_proportion), measures < (Q1 - IQR * iqr_proportion))
    return outlier_tf
    
