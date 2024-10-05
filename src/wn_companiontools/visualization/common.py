"""
Provides functions common to 2D and 3D visualization.
@Author: Jannik Stebani, 2024
"""
from numbers import Number
from typing import Sequence, Mapping

import numpy as np
import ipywidgets as wgt
import k3d

# the colormaps given in this k3d module are all just numpy ndarrays
# thus they can be used for both matplotlib and k3d
COLORMAPS: dict[str, np.ndarray] = {
    'viridis' : k3d.colormaps.matplotlib_color_maps.Viridis,
    'cividis' : k3d.colormaps.matplotlib_color_maps.Cividis,
    'inferno' : k3d.colormaps.matplotlib_color_maps.Inferno,
    'plasma' : k3d.colormaps.matplotlib_color_maps.Plasma,
    'magma' : k3d.colormaps.matplotlib_color_maps.Magma,
    'gray' : k3d.colormaps.matplotlib_color_maps.Gray,
    'jet' : k3d.colormaps.matplotlib_color_maps.Jet,
    'hot' : k3d.colormaps.matplotlib_color_maps.Hot,
    'cool' : k3d.colormaps.matplotlib_color_maps.Cool
}


def create_windowing_slider(data: np.ndarray,
                            initial_value: tuple[Number, Number] = (-100, 1000)
                            ) -> wgt.FloatRangeSlider:
    """
    Create float range slider with (min, max) deduced from data and given default setting

    Parameters
    ----------

    data : np.ndarray
        The data array for which the windowing slider should be created.

    initial_value : tuple[Number, Number]
        The initial windowing values to be set on the slider.

        
    Returns
    -------

    wgt.FloatRangeSlider
        The windowing slider.
    """
    min_, max_ = np.min(data), np.max(data)
    slider = wgt.FloatRangeSlider(min=min_, max=max_, value=initial_value,
                                  description='Window Levels')
    return slider


def create_slider(data: np.ndarray) -> wgt.IntSlider:
    """
    Create integer slider that facilitates slice index selection for the given data array.
    Note that the first axis of the data array is assumed to represent the slice index.

    Parameters
    ----------

    data : np.ndarray
        The data array for which the slice index slider should be created.

    Returns
    -------

    wgt.IntSlider
        The slice index slider.
    """
    desc = 'Slice Index'
    return wgt.IntSlider(value=0, min=0, max=data.shape[0] - 1, description=desc)


def create_aspect_buttons(shape: Sequence[int]) -> wgt.RadioButtons:
    """Create trio of radio buttons that facilitate aspect selection."""
    name: str = 'aspect'
    desc: str = 'Cross Section'
    mapping = {f'aspect {i+1}' : i for i in range(len(shape))}
    buttons = wgt.RadioButtons(options=mapping, description=desc)
    return buttons


def create_cmap_dropdown(default: str = 'viridis') -> wgt.Dropdown:
    """
    Create dropdown widget for matplotlib/k3d colormap selection.
    
    Parameters
    ----------

    default : str
        The default colormap to be selected on initialization.

    Returns
    -------

    wgt.Dropdown
        The colormap selection dropdown widget.
    """
    options = COLORMAPS.keys()
    dropdown = wgt.Dropdown(options=options,
                            value=default,
                            disabled=False,
                            description='Colormap'
    )
    return dropdown


