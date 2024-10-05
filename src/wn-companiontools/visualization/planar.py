"""
Provides functions for visualizing planar images dznamically in an assumed
jupyter notebook context via matplotlib and ipywidgets.

@Author Jannik Stebani, 2024
"""
import matplotlib.pyplot as plt
import numpy as np
from collections.abc import Mapping
import ipywidgets as wgt

from .common import create_slider, create_aspect_buttons, create_windowing_slider, create_cmap_dropdown

class SliceDisplay:
    """
    Create a nice interactive slice-wise display for 3D array data with dynamic widget controls.

    Parameters
    ----------

    data : np.ndarray
        The 3D data array to be visualized as 3D planar slices.

    cmap : str, optional
        The colormap to be used for the visualization.
        Default is 'viridis'.

    figargs : Mapping, optional
        Additional arguments to be passed to the matplotlib figure creation.
        Example: {'figsize' : (10, 10)} for larger figure size.

    Attributes
    ----------

    data : np.ndarray
        The 3D data array backing of the visualization.

    cmap : str
        The colormap used for the visualization.

    max_ : float
        The maximum value of the data array.

    min_ : float
        The minimum value of the data array.

    startindex : int
        The initial slice index to be displayed.

    fig : matplotlib.figure.Figure
        Reference to the created matplotlib figure instance.
    
    ax : matplotlib.axes.Axes
        Reference to the created matplotlib axes instance.

    img : matplotlib.image.AxesImage
        Reference to the created matplotlib image instance.

    slider : wgt.IntSlider
        The slider widget that facilitates slice index selection.

    buttons : wgt.ToggleButtons
        The toggle buttons widget that facilitates aspect/POV.

    rangeslider : wgt.FloatRangeSlider
        The slider widget that facilitates windowing of the data.

    cmap_dropdown : wgt.Dropdown
        The dropdown widget that facilitates colormap selection.

    aspect_text : matplotlib.text.Text
        The text element that displays the current aspect.

    slice_text : matplotlib.text.Text
        The text element that displays the current slice index.

    Methods
    -------

    create_vmin_vmax_slider : wgt.FloatRangeSlider
        Create a slider widget for windowing the data.

    create_cmap_dropdown : wgt.Dropdown
        Create a dropdown widget for colormap selection.

    init_figure : tuple
        Initialize the matplotlib figure, axes and image instances.

    init_text : tuple
        Initialize the text elements for aspect and slice index.

    init_slider : None
        Initialize the slice index slider.

    init_vmin_vmax_slider : None
        Initialize the windowing slider.

    init_buttons : None
        Initialize the aspect buttons.

    init_cmap_dropdown : None
        Initialize the colormap dropdown.

    mutate_slider : None
        Mutate the slice index slider after changing the data layout.

    get_controls : wgt.HBox
        Get the widget controls as a horizontal box layout
    """
    figsize: tuple[float, float] = (8, 8)
    def __init__(self, data: np.ndarray, cmap: str = 'viridis', figargs: Mapping | None = None):
        assert data.ndim == 3, f'expecting 3D data, but got ndim = {data.ndim} array instead'
        self.data = data
        self.cmap = cmap
        self.max_ = np.max(data)
        self.min_ = np.min(data)
        
        figargs = figargs or {}
        kwargs = {'figsize' : self.figsize} | figargs
        self.startindex = 0
        self.fig, self.ax, self.img = self.init_figure(**kwargs)
        
        self.slider = create_slider(self.data)
        self.buttons = create_aspect_buttons(self.data.shape)
        
        self.init_slider()
        self.init_buttons()
        
        self.aspect_text, self.slice_text = self.init_text()
        
        self.rangeslider = self.create_vmin_vmax_slider()
        self.init_vmin_vmax_slider()
        
        self.cmap_dropdown = create_cmap_dropdown(default='viridis')
        self.init_cmap_dropdown()
        
        
    def create_vmin_vmax_slider(self) -> wgt.FloatRangeSlider:
        """Create windowing slider from the data extremal values."""
        slider = create_windowing_slider(self.data, initial_value=(self.min_, self.max_))
        return slider
    
    
    def create_cmap_dropdown(self) -> wgt.Dropdown:
        """Create colormap dropdown with all available colormaps."""
        dropdown = wgt.Dropdown(
            options=self.cmaps,
            value=self.cmap,
            disabled=False,
            description='Colormap'
        )
        return dropdown
        
    
    def init_figure(self, **kwargs) -> tuple:
        """Initialize matplotlib figure, axes and image instances."""
        fig, ax = plt.subplots(**kwargs)
        img = ax.imshow(self.data[self.startindex, ...], cmap=self.cmap,
                        vmin=self.min_, vmax=self.max_)
        ax.set_aspect('equal')
        ax.set(xlabel='$x$ coordinate', ylabel='$y$ coordinate')
        return (fig, ax, img)
    
    
    def init_text(self) -> None:
        """Initialize text elements for aspect and slice index."""
        fontdict = {'size' : 12}
        aspect_text = self.ax.text(0.3, 0.9, s='Aspect 1', fontdict=fontdict,
                                   transform=self.fig.transFigure)
        slice_text = self.ax.text(0.6, 0.9, s='Slice Index: 0', fontdict=fontdict,
                                  transform=self.fig.transFigure)
        return (aspect_text, slice_text)
        
        
    def init_slider(self) -> None:
        """Connect the slider to the image instance."""
        
        def on_change(change: Mapping) -> None:
            newindex = change['new']
            self.img.set_data(self.data[newindex, ...])
            self.slice_text.set_text(f'Slice Index: {newindex}')
            
        self.slider.observe(on_change, names='value')
        
    
    def init_vmin_vmax_slider(self) -> wgt.FloatRangeSlider:
        """Connect the windowing slider to the image instance."""
        
        def on_change(change: Mapping):
            new_low, new_high = change['new']
            self.img.set_clim(vmin=new_low, vmax=new_high)
            self.fig.canvas.draw_idle()
            
        self.rangeslider.observe(on_change, names='value')
        
        
    def mutate_slider(self) -> None:
        """
        Mutate slider after changing of basal data layout to respect to min/max values
        and reset viewport state to zero-th slice image.
        """
        reset_value = 0
        # mutate int slider instance
        self.slider.min = 0
        self.slider.max = self.data.shape[0] - 1
        self.slider.value = reset_value
        # reset viewport state
        self.img.set_data(self.data[reset_value, ...])
        self.fig.canvas.draw_idle()
        self.slice_text.set_text(f'Slice Index: {reset_value}')
        
        
    def init_buttons(self) -> None:
        """Connect the aspect buttons to the image instance."""
        
        def on_change(change: Mapping) -> None:
            newaxis = change['new']
            self.data = np.swapaxes(self.data, 0, newaxis)
            self.mutate_slider()
            self.aspect_text.set_text(self.buttons.label.capitalize())
            
        self.buttons.observe(on_change, names='value')
        
    
    def init_cmap_dropdown(self) -> None:
        """Connect the colormap dropdown to the image instance."""
        
        def on_change(change: Mapping) -> None:
            cmap = change['new']
            self.img.set_cmap(cmap)
            min_, max_ = self.rangeslider.value
            self.img.set_clim(min_, max_)
            self.fig.canvas.draw_idle()
            
        self.cmap_dropdown.observe(on_change, names='value')
        
        
    def get_controls(self) -> wgt.HBox:
        """Get the full widget control elements as a horizontal box layout."""
        box = wgt.HBox([self.slider, self.buttons, self.rangeslider, self.cmap_dropdown])
        return box
        
    