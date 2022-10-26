""" Scan outlier metrics
"""

# Any imports you need
# +++your code here+++
import numpy as np

def dvars_voxel(voxels):
    """ Calculate dvars metric on 2D array with voxels in rows and time-points(volumes) in columns

    The dvars calculation between two volumes is defined as the square root of 
    (the mean of the (voxel differences square)).

    Parameters
    ----------
    voxels : 2D array

    Returns
    -------
    dvals : 1D array
        One-dimensional array with n-1 elements, where n is the number of 
        volumes in 'img'.
    """
    vol_diff = voxels[..., 1:] - voxels[..., :-1]
    dvar_val = np.sqrt(np.mean(vol_diff ** 2, axis=0))
    return dvar_val


def dvars(img):
    """ Calculate dvars metric on Nibabel image `img`

    The dvars calculation between two volumes is defined as the square root of
    (the mean of the (voxel differences squared)).

    Parameters
    ----------
    img : nibabel image

    Returns
    -------
    dvals : 1D array
        One-dimensional array with n-1 elements, where n is the number of
        volumes in `img`.
    """
    # Hint: remember 'axis='.  For example:
    # In [2]: arr = np.array([[2, 3, 4], [5, 6, 7]])
    # In [3]: np.mean(arr, axis=1)
    # Out[2]: array([3., 6.])
    #
    # You may be be able to solve this in four lines, without a loop.
    # But solve it any way you can.
    # This is a placeholder, replace it to write your solution.
    data = img.get_fdata()
   
    voxel_by_time = np.reshape(data, (-1, data.shape[-1]))
    dvar_val = dvars_voxel(voxel_by_time)

    return dvar_val

    raise NotImplementedError("Code up this function")
