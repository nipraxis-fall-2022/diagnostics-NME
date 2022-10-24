""" Module with routines for finding outliers
"""

from pathlib import Path

import numpy as np

import nibabel as nib

from skimage.filters import threshold_otsu

from .metrics import dvars
from .detectors import iqr_detector,mad_voxel_detector,mad_time_detector

def segment_brain(img):
    """ Segments brain region from background and returns only brain voxels
    Parameters
    ----------
    img : array
        2D array with voxels in rows and timepoints in columns
    Returns
    -------
    thresholded_img : array
        2D array containing only brain voxels in rows and timepoints in columns
    """
    # calculate the mean of each voxel over time
    mean_img = np.mean(img, axis=-1)
    # calculate the threshold for segmenting brain from background
    threshold = threshold_otsu(mean_img)
    mask = np.expand_dims(mean_img > threshold, axis=1)
    mask_2D = np.tile(mask, (1, img.shape[-1]))
    thresholded_img = np.where(mask_2D, img, np.nan)
    # filter only brain voxels
    brain_voxels = thresholded_img[~np.isnan(thresholded_img).all(axis=1)]
    return brain_voxels
    
def detect_outliers_mean_absolute_deviation_mask(fname):
    """ Detect outliers given image file path 'filename'
     
    Parameters
    ----------
    fname : str or Path
        Filename of 4D image, as string or Path object
    
    Returns
    -------
    outliers : array
        Indices of outlier volumes.
    """
    # A mask is used to first segment the brain regions from the background, then mean absolute deviation is used to detect outliers
    img = nib.load(fname)
    img_data = img.get_fdata()
    # reshape from 4D to 2D
    img_data_2D = np.reshape(img_data, (-1,img_data.shape[-1]))
    # segment brain from background
    brain_voxels = segment_brain(img_data_2D)
    # find the outlying voxels
    outliers_voxel = mad_voxel_detector(brain_voxels)
    # calculate the number of outlying voxels for each time point
    voxel_outliers_per_time = np.nansum(outliers_voxel,axis=0)
    # find the outliers in the time-series    
    outliers_time = mad_time_detector(voxel_outliers_per_time)
    # Return indices of True values from Boolean array. 
    return np.nonzero(outliers_time)[0]


def detect_outliers(fname):
    """ Detect outliers given image file path `filename`

    Parameters
    ----------
    fname : str or Path
        Filename of 4D image, as string or Path object

    Returns
    -------
    outliers : array
        Indices of outlier volumes.
    """
    # This is a very simple function, using dvars and iqroutliers
    img = nib.load(fname)
    dvs = dvars(img)
    is_outlier = iqr_detector(dvs, iqr_proportion=2)
    # Return indices of True values from Boolean array.
    return np.nonzero(is_outlier)[0]


def find_outliers(data_directory):
    """ Return filenames and outlier indices for images in `data_directory`.

    Parameters
    ----------
    data_directory : str
        Directory containing containing images.

    Returns
    -------
    outlier_dict : dict
        Dictionary with keys being filenames and values being lists of outliers
        for filename.
    """
    image_fnames = Path(data_directory).glob("**/sub-*.nii.gz")
    outlier_dict = {}
    for fname in image_fnames:
        outliers = detect_outliers_mean_absolute_deviation_mask(fname)
        #outliers = detect_outliers(fname)
        outlier_dict[fname] = outliers
    return outlier_dict
