import warnings

from bokeh.io import show as show_
from bokeh.models import (
    BasicTicker,
    ColorBar,
    ColumnDataSource,
    LinearColorMapper,
    LogColorMapper,
)
from bokeh.plotting import figure, output_file
from bokeh.sampledata.periodic_table import elements #type: ignore
from bokeh.transform import dodge

from matplotlib.cm import (
    ScalarMappable,
    )
from matplotlib import cm
from bokeh.colors import RGB
from matplotlib.colors import LinearSegmentedColormap

from matplotlib.colors import LogNorm, Normalize, to_hex
import pandas as pd
from pandas import options
from numpy import isnan

def makeBokehColorPalette(cm_palette: LinearSegmentedColormap) -> tuple[list, bool]:
    palette_rgb = (255 * cm_palette(range(256))).astype("int")
    divergingPalette = cm_palette in [cm.coolwarm, cm.PiYG, cm.PRGn, #type: ignore
                                      cm.BrBG, cm.PuOr, cm.RdGy, #type: ignore
                                      cm.RdBu, cm.RdYlBu, cm.RdYlGn, #type: ignore
                                      cm.Spectral, cm.bwr, cm.seismic, #type: ignore
                                      cm.berlin, cm.managua, cm.vanimo] #type: ignore
    return [RGB(*tuple(rgb)).to_hex() for rgb in palette_rgb], divergingPalette
    
def plotter(
    df: pd.DataFrame,
    column_elements: str,
    column_data: str,
    show: bool = True,
    output_filename: str | None = None,
    width: int = 1050,
    cmap: LinearSegmentedColormap = cm.plasma, #type: ignore
    alpha: float = 0.65,
    extended: bool = True,
    periods_remove: list[int] | None = None,
    groups_remove: list[int] | None = None,
    log_scale: bool = False,
    cbar_height: int | None= None,
    cbar_standoff: int = 12,
    cbar_fontsize: int = 14,
    blank_color: str = "#c4c4c4",
    under_value: float | None = None,
    under_color: str = "#140F0E",
    over_value: float | None = None,
    over_color: str = "#140F0E",
    special_elements: list[str] | None = None,
    special_color: str = "#6F3023",
    print_data: bool = False,
) -> figure:
    """
    Plot a heatmap over the periodic table of elements.

    Parameters
    ----------
    df: pandas.DataFrame
        Dataframe containing the data to be plotted
    column_elements: str
        Name of column in dataframe containing the element labels
    column_data: str
        Name of column in dataframe containing the data to be plotted
    show : str
        If True, the plot will be shown.
    output_filename : str
        If not None, the plot will be saved to the specified (.html) file.
    width : float
        Width of the plot.
    cmap : matplotlib.colors.LinearSegmentedColormap
        A matplotlib colourmap, both normal and divergent maps are supported
    alpha : float
        Alpha value (transparency).
    extended : bool
        If True, the lanthanoids and actinoids will be shown.
    periods_remove : list[int]
        Period numbers to be removed from the plot.
    groups_remove : list[int]
        Group numbers to be removed from the plot.
    log_scale : bool
        If True, the colorbar will be logarithmic.
    cbar_height : int
        Height of the colorbar.
    cbar_standoff : int
        Distance between the colorbar and the plot.
    cbar_fontsize : int
        Fontsize of the colorbar label.
    blank_color : str
        Hexadecimal color of the elements without data.
    under_value : float
        Values <= under_value will be colored with under_color.
    under_color : str
        Hexadecimal color to be used for the lower bound color.
    over_value : float
        Values >= over_value will be colored with over_color.
    under_color : str
        Hexadecial color to be used for the upper bound color.
    special_elements: list[str]
        List of elements to be colored with special_color.
    special_color: str
        Hexadecimal color to be used for the special elements.
    print_data: bool
        Whether the value of the data will be plotted as a number.

    Returns
    -------
    figure
        Bokeh figure object.
    """

    options.mode.chained_assignment = None

    bokeh_palette, divergingPalette = makeBokehColorPalette(cmap)

    df = df.set_index(column_elements, drop = True)
    df = df.reindex(elements.symbol)

    # Define number of and groups
    period_label = ["1", "2", "3", "4", "5", "6", "7"]
    group_range = [str(x) for x in range(1, 19)]

    # Remove any groups or periods
    if groups_remove:
        for gr in groups_remove:
            group_range.remove(str(gr))
    if periods_remove:
        for pr in periods_remove:
            period_label.remove(str(pr))

    period_label.append("blank")
    period_label.append("La")
    period_label.append("Ac")
    elements["period"] = elements["period"].astype(str)

    # Breaks out the lanthanoids and actinoids
    if extended:
        count = 0
        for i in range(56, 70):
            elements.loc[i, "period"] = "La"
            elements.loc[i, "group"] = str(count + 4)
            count += 1

        count = 0
        for i in range(88, 102):
            elements.loc[i, "period"] = "Ac"
            elements.loc[i, "group"] = str(count + 4)
            count += 1

    # Define matplotlib and bokeh color map
    if divergingPalette: #For colour palettes designed around being symmetric around zero.
        if df[column_data].max() >= abs(df[column_data].min()):
            boundary = df[column_data].max()
        else:
            boundary = abs(df[column_data].min())
        if log_scale:
            for datum in df[column_data]:
                if datum < 0:
                    raise ValueError(
                        f"Entry for element {datum} is negative but log-scale is selected"
                    )
            color_mapper = LogColorMapper(
                palette=bokeh_palette, low= -boundary, high= boundary #type: ignore
            )
            norm = LogNorm(vmin= -boundary, vmax= boundary #type: ignore
            )
        else:
            color_mapper = LinearColorMapper(
                palette=bokeh_palette, low= -boundary, high= boundary #type: ignore
            )
            norm = Normalize(vmin= -boundary, vmax= boundary) #type: ignore
        color_scale = ScalarMappable(norm=norm, cmap=cmap).to_rgba(df[column_data], alpha=None) #type: ignore
    else:
        if log_scale:
            for datum in df[column_data]:
                if datum < 0:
                    raise ValueError(
                        f"Entry for element {datum} is negative but log-scale is selected"
                    )
            color_mapper = LogColorMapper(
                palette=bokeh_palette, low=df[column_data].min(), high=df[column_data].max() #type: ignore

            )
            norm = LogNorm(vmin=df[column_data].min(), vmax=df[column_data].max()) #type: ignore
        else:
            color_mapper = LinearColorMapper(
                palette=bokeh_palette, low=df[column_data].min(), high=df[column_data].max() #type: ignore
            )
            norm = Normalize(vmin=df[column_data].min(), vmax=df[column_data].max()) #type: ignore
        color_scale = ScalarMappable(norm=norm, cmap=cmap).to_rgba(df[column_data], alpha=None) #type: ignore

    # Set blank color
    color_list = [blank_color] * len(elements)
    
    # Compare elements in dataset with elements in periodic table
    for i, data_element in enumerate(df.index):
        element_entry = elements.symbol[
            elements.symbol.str.lower() == data_element.lower()
        ]
        if not element_entry.empty:
            element_index = element_entry.index[0]
        else:
            warnings.warn("Invalid chemical symbol: " + data_element)
        if color_list[element_index] != blank_color: #type: ignore
            warnings.warn("Multiple entries for element " + data_element)
        elif isnan(df[column_data].iloc[i]):
            color_list[element_index] = blank_color #type: ignore
        elif under_value is not None and df[column_data].iloc[i] <= under_value:
            color_list[element_index] = under_color #type: ignore
        elif over_value is not None and df[column_data].iloc[i] >= over_value:
            color_list[element_index] = over_color #type: ignore
        else:
            color_list[element_index] = to_hex(color_scale[i]) #type: ignore

    if special_elements:
        for k, v in elements["symbol"].iteritems():
            if v in special_elements:
                color_list[k] = special_color

    # Define figure properties for visualizing data
    source = ColumnDataSource(
        data=dict(
            group=[str(x) for x in elements["group"]],
            period=[str(y) for y in elements["period"]],
            sym=elements["symbol"],
            atomic_number=elements["atomic number"],
            type_color=color_list,
            data_text = df[column_data].to_numpy()
        )
    )

    # Plot the periodic table
    p = figure(x_range=group_range, y_range=list(reversed(period_label)), tools="save") #type: ignore
    p.width = width
    p.outline_line_color = None
    p.background_fill_color = None
    p.border_fill_color = None
    p.toolbar_location = "above"
    p.rect("group", "period", 0.9, 0.9, source=source, alpha=alpha, color="type_color")
    p.axis.visible = False
    text_props = {
        "source": source,
        "angle": 0,
        "color": "black",
        "text_align": "left",
        "text_baseline": "middle",
    }
    x = dodge("group", -0.4, range=p.x_range)
    y = dodge("period", 0.32, range=p.y_range)
    p.text(
        x=x,
        y="period",
        text="sym",
        text_font_style="bold",
        text_font_size="16pt",
        **text_props,
    )
    p.text(x=x, y=y, text="atomic_number", text_font_size="11pt", **text_props)

    if print_data:
        text_props = {
            "source": source,
            "angle": 0,
            "color": "black",
            "text_align": "right",
            "text_baseline": "middle",
        }
        data_x = dodge("group", 0.4, range=p.x_range)
        data_y = dodge("period", -0.3, range=p.y_range)
        p.text(x=data_x, y = data_y, text = "data_text", text_font_size="8pt", **text_props)

    color_bar = ColorBar(
        color_mapper=color_mapper,
        ticker=BasicTicker(desired_num_ticks=10),
        border_line_color=None,
        label_standoff=cbar_standoff,
        location=(0, 0),
        orientation="vertical",
        scale_alpha=alpha,
        major_label_text_font_size=f"{cbar_fontsize}pt",
    )

    if cbar_height is not None:
        color_bar.height = cbar_height

    p.add_layout(color_bar, "right")
    p.grid.grid_line_color = None

    if output_filename:
        output_file(output_filename)

    if show:
        show_(p)

    return p
