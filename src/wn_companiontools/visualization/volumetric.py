"""
Provide functionality to dynamically visualize volumetric
with k3d and ipywidgets in the context of jupyter notebooks.

@Author: Jannik Stebani, 2024
"""
from typing import Mapping
import numpy as np
import ipywidgets as wgt
import k3d

from .common import COLORMAPS, create_windowing_slider, create_cmap_dropdown


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


class VolumeDisplay:
    """
    Render a 3D volumetric visualization with k3d and ipywidgets in a jupyter notebook.

    Parameters
    ----------

    data : np.ndarray
        The 3D data array to be visualized.

    Attributes
    ----------

    data : np.ndarray
        The 3D data array backing of the visualization.

    volume : k3d.objects.Volume
        The k3d volume object that is visualized.

    plot : k3d.plot.Plot
        The k3d plot object that contains the volume visualization.

    slider : wgt.FloatRangeSlider
        The slider widget that facilitates windowing level settings of the image.
    
    dropdown : wgt.Dropdown
        The dropdown widget that facilitates colormap selection.
    """
    DEFAULT_WINDOW_LEVELS_3D: tuple[float, float] = (-0.75, 1.0)
    DEFAULT_ALPHA_COEF: float = 50
    DEFAULT_COLORMAP_NAME: str = 'jet'
    
    def __init__(self, data: np.ndarray) -> None:
        self.data = data
        self.volume = self.build_volume(self.data)
        self.plot = self.create_plot()
        # set up slider
        slider = create_windowing_slider(self.data, initial_value=self.DEFAULT_WINDOW_LEVELS_3D)
        self.slider = connect_windowing_slider(self.volume, slider)
        # set up cmap dropdown
        dropdown = create_cmap_dropdown(default=self.DEFAULT_COLORMAP_NAME)
        self.dropdown = connect_cmap_dropdown(self.volume, dropdown)
        
    def build_volume(self,
                     data: np.ndarray,
                     color_range: tuple[float, float] | None = None,
                     alpha_coef: float | None = None,
                     color_map_name: str | None = None):
        """
        Create a `k3d` volume drawable from input parameters and class variables (defaults).
        """
        color_range = color_range or self.DEFAULT_WINDOW_LEVELS_3D
        alpha_coef = alpha_coef or self.DEFAULT_ALPHA_COEF
        color_map_name = color_map_name or self.DEFAULT_COLORMAP_NAME
        # convert to actual numerical table
        color_map = COLORMAPS[color_map_name]
        plot_volume = k3d.volume(data, color_range=color_range, alpha_coef=alpha_coef,
                                 color_map=color_map)
        return plot_volume
    
    
    def init_windowing_slide(self) -> wgt.FloatRangeSlider:
        slider = create_windowing_slider(self.data, )
    

    def create_plot(self):
        """Create the k3d plot object"""
        plot = k3d.plot(grid_visible=False)
        plot += self.volume
        return plot
        

    def get_controls(self):
        """Get joint controls for windowing and colormap selection."""
        return wgt.HBox([self.dropdown, self.slider])
        
    