"""
Create basic data loadiong functions.

@Author: Jannik Stebani
"""
import numpy as np
from pathlib import Path
import h5py

PathLike = str | Path


def read_data_from_hdf5(path: PathLike, internal_path: str) -> np.ndarray:
    """
    Eagerly read full data array from a HDF5 file.

    Parameters
    ----------

    path : Path to the HDF5 file.

    internal_path : Path to the internal HDF5 dataset.

    Returns
    -------

    np.ndarray : The data from the HDF5 file.
    """
    with h5py.File(path, mode='r') as handle:
        data = handle[internal_path][...]
    return data


def read_fingerprint_from_hdf5(path: PathLike, internal_path: str) -> dict:
    """ Read the fingerprint from a HDF5 file.
    
    Parameters
    ----------
    path : Path to the HDF5 file.
    internal_path : Path to the internal HDF5 dataset.

    Returns
    -------

    dict : The fingerprint of the HDF5 file.
    """
    with h5py.File(path, 'r') as handle:
        fingerprint = {k : v for k, v in handle[internal_path].attrs.items()}
    return fingerprint