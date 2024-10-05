"""
Provide functionality to dynamically visualize volumetric
with k3d and ipywidgets in the context of jupyter notebooks.

@Author: Jannik Stebani, 2024
"""
from typing import Mapping
import ipywidgets as wgt
import k3d

from .common import COLORMAPS


def connect_windowing_slider(volume: k3d.objects.Volume,
                             slider: wgt.FloatRangeSlider) -> wgt.FloatRangeSlider:
    """
    Connect a preexisting windowing slider to a volume instance to allow direct manipulation
    of windowing (upper, lower) parameters of 3D volumetric rendering.

    Parameter
    ---------

    volume : k3d.objects.Volume
        The k3d volume object that should be connected to the slider.

    slider : wgt.FloatRangeSlider
        The slider that manipulates the windowing parameters of the volume visualization.
        It should generally be intialized with the min and max values of the data.

    Returns
    -------

    wgt.FloatRangeSlider
        The connected slider.
    """
    def on_change(change: Mapping) -> None:
        newlo, newhi = change['new']
        volume.color_range = (newlo, newhi)
    
    slider.observe(on_change, names='value')
    return slider


def connect_cmap_dropdown(volume: k3d.objects.Volume,
                          dropdown: wgt.Dropdown) -> wgt.Dropdown:
    """
    Connect a preexisting color map dropdown selection menu to
    k3d volume visualization element to change the colormap on the fly.

    Parameters
    ----------

    volume : k3d.objects.Volume
        The k3d volume object that should be connected to the dropdown.

    dropdown : wgt.Dropdown
        The dropdown widget that facilitates colormap selection.
        Must be initialized with values representing the keys of the COLORMAPS dictionary.

    Returns
    -------

    wgt.Dropdown
        The connected colormap-changing dropdown widget.
    """
    def on_change(change: Mapping):
        cmap = COLORMAPS[change['new']]
        volume.color_map = cmap
    
    dropdown.observe(on_change, names='value')
    return dropdown