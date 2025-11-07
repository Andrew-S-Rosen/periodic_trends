from __future__ import annotations

import warnings

import pandas as pd
from bokeh.io import show as show_
from bokeh.models import (
    BasicTicker,
    ColorBar,
    ColumnDataSource,
)
from bokeh.plotting import figure, output_file
from bokeh.sampledata.periodic_table import elements  # type: ignore
from bokeh.transform import dodge
from matplotlib import cm
from matplotlib.colors import to_hex
from numpy import float64, isnan
from periodic_trends._bokeh_tools import _color_scale_maker
from pandas import options

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.colors import LinearSegmentedColormap


def plotter(
    df: pd.DataFrame,
    column_elements: str,
    column_data: str,
    show: bool = True,
    output_filename: str | None = None,
    width: int = 1050,
    height: int = 600,
    cmap: LinearSegmentedColormap = cm.plasma,  # type: ignore
    alpha: float = 0.65,
    extended: bool = True,
    periods_remove: list[int] | None = None,
    groups_remove: list[int] | None = None,
    rescale_canvas: bool = True,
    log_scale: bool = False,
    cbar_x: int = 0,
    cbar_y: int = 0,
    cbar_height: int | None = None,
    cbar_ticks: int = 10,
    cbar_title: str | None = None,
    cbar_standoff: int = 12,
    cbar_fontsize: int = 14,
    blank_color: str = "#c4c4c4",
    under_value: float | None = None,
    under_color: str = "#140F0E",
    over_value: float | None = None,
    over_color: str = "#140F0E",
    color_max: float | None = None,
    color_min: float | None = None,
    special_elements: list[str] | None = None,
    special_color: str = "#6F3023",
    print_data: bool = False,
    float_decimals: int = 1,
    data_unit: str | None = None,
    title: str | None = None,
) -> figure:
    """
    Plot a heatmap over the periodic table of elements.

    Parameters
    ----------
    df: pandas.DataFrame
        Dataframe containing the data to be plotted.
    column_elements: str
        Name of column in dataframe containing the element labels.
    column_data: str
        Name of column in dataframe containing the data to be plotted.
    show: str
        If True, the plot will be shown.
    output_filename : str
        If not None, the plot will be saved to the specified (.html) file.
    width: int
        Width of the plot.
    height: int
        Height of the plot.
    cmap: matplotlib.colors.LinearSegmentedColormap
        A matplotlib colourmap, both normal and divergent maps are supported.
    alpha: float
        Alpha value (transparency).
    extended: bool
        If True, the lanthanoids and actinoids will be shown.
    periods_remove: list[int]
        Period numbers to be removed from the plot.
    groups_remove: list[int]
        Group numbers to be removed from the plot.
    rescale_canvas_to_fit: bool;
        If True, rescale the canvas to account for removed periods/groups.
    log_scale: bool
        If True, the colorbar will be logarithmic.
    cbar_x: int
        x-position of the colorbar.
    cbar_y: int
        y-position of the colorbar.
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
    color_max: int | float
        Can be used to specify the value corresponding to the max edge of the colorpalette.
        Useful for syncing colour ranges between figures.
    color_min: int | float
        Can be used to specify the value corresponding to the min edge of the colorpalette.
        Useful for syncing colour ranges between figures.
    special_elements: list[str]
        List of elements to be colored with special_color.
    special_color: str
        Hexadecimal color to be used for the special elements.
    print_data: bool
        Whether the value of the data will be plotted as a number.
    data_unit: str
        Specifies a unit when the data is printed to the graph.
    title: str
        Specifies the title of the graph.

    Returns
    -------
    figure
        Bokeh figure object.
    """

    options.mode.chained_assignment = None

    df = df.set_index(column_elements, drop=True)
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

    # Breaks out the lanthanoids and actinoids
    if extended:
        period_label.append("blank")
        period_label.append("La")
        period_label.append("Ac")
        elements["period"] = elements["period"].astype(str)

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

    # Rescale the canvas to account for removed periods/groups
    if rescale_canvas:
        height = height * len(period_label) // 10
        width = width * (len(group_range) + 2) // 20

    # Define matplotlib and bokeh color map
    color_scale, color_mapper = _color_scale_maker(
        df[column_data],  # type: ignore
        cmap,
        log_scale=log_scale,
        lower_boundary=color_min,
        upper_boundary=color_max,
    )

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
            warnings.warn("Invalid chemical symbol: " + data_element, stacklevel=2)
        if color_list[element_index] != blank_color:  # type: ignore
            warnings.warn("Multiple entries for element " + data_element, stacklevel=2)
        elif isnan(df[column_data].iloc[i]):
            color_list[element_index] = blank_color  # type: ignore
        elif under_value is not None and df[column_data].iloc[i] <= under_value:
            color_list[element_index] = under_color  # type: ignore
        elif over_value is not None and df[column_data].iloc[i] >= over_value:
            color_list[element_index] = over_color  # type: ignore
        else:
            color_list[element_index] = to_hex(color_scale[i])  # type: ignore

    if special_elements:
        for k, v in elements["symbol"].iteritems():
            if v in special_elements:
                color_list[k] = special_color

    # Formatting of data_text
    if type(data_unit) is str:
        if df[column_data].dtype == float64:
            float_formatter = "{:." + str(float_decimals) + "f}"
            data_text = [
                float_formatter.format(x) + data_unit if not isnan(x) else x
                for x in df[column_data]
            ]
        else:
            data_text = [
                str(x) + data_unit if not isnan(x) else x for x in df[column_data]
            ]

    else:
        if df[column_data].dtype == float64:
            float_formatter = "{:." + str(float_decimals) + "f}"
            data_text = [float_formatter.format(x) for x in df[column_data]]
        else:
            data_text = df[column_data].tolist()

    # Define figure properties for visualizing data
    source = ColumnDataSource(
        data={
            "group": [str(x) for x in elements["group"]],
            "period": [str(y) for y in elements["period"]],
            "sym": elements["symbol"],
            "atomic_number": elements["atomic number"],
            "type_color": color_list,
            "data_text": data_text,
        }
    )

    # Plot the periodic table
    p = figure(
        x_range=group_range,
        y_range=list(reversed(period_label)),
        tools=["save"],
        title=title,
    )  # type: ignore
    p.width = width
    p.height = height
    p.outline_line_color = None
    p.background_fill_color = None
    p.border_fill_color = None
    p.toolbar_location = None
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
        p.text(x=data_x, y=data_y, text="data_text", text_font_size="8pt", **text_props)

    color_bar = ColorBar(
        color_mapper=color_mapper,
        ticker=BasicTicker(desired_num_ticks=cbar_ticks),
        border_line_color=None,
        label_standoff=cbar_standoff,
        location=(cbar_x, cbar_y),
        orientation="vertical",
        scale_alpha=alpha,
        major_label_text_font_size=f"{cbar_fontsize}pt",
        display_high=df[column_data].max(),  # type: ignore
        display_low=df[column_data].min(),  # type: ignore
        title=cbar_title,
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

