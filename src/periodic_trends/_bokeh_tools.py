from __future__ import annotations

from typing import TYPE_CHECKING

from bokeh.colors import RGB
from bokeh.models import LinearColorMapper, LogColorMapper
from matplotlib import cm
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, LogNorm, Normalize

if TYPE_CHECKING:
    import pandas as pd
    from numpy import ndarray


def _color_scale_maker(
    data: pd.Series,
    cmap: LinearSegmentedColormap,
    log_scale: bool = False,
    lower_boundary: int | None = None,
    upper_boundary: int | None = None,
) -> tuple[ndarray, LogColorMapper | LinearColorMapper]:
    bokeh_palette, divergingPalette = _make_bokeh_color_palette(cmap)

    data_min = data.min()
    data_max = data.max()

    if (
        divergingPalette and lower_boundary is not None and upper_boundary is not None
    ):  # Forces the palette to remain centered on 0. May be broken if 0 is not in the range
        if upper_boundary >= abs(lower_boundary):
            lower_boundary = -upper_boundary
        elif upper_boundary < abs(lower_boundary):
            upper_boundary = -lower_boundary
    elif divergingPalette and lower_boundary is None and upper_boundary is not None:
        lower_boundary = -upper_boundary
    elif divergingPalette and lower_boundary is not None and upper_boundary is None:
        upper_boundary = -lower_boundary
    elif divergingPalette and lower_boundary is None and upper_boundary is None:
        if data_max >= abs(data_min):
            lower_boundary = -data_max
            upper_boundary = data_max
        elif data_max < abs(data_min):
            lower_boundary = data_min
            upper_boundary = -data_min
    elif not divergingPalette:
        if upper_boundary is None:
            upper_boundary = data_max
        if lower_boundary is None:
            lower_boundary = data_min
    else:
        raise ValueError(
            "Something went wrong when determining the boundaries of the color palette."
        )

    if log_scale:
        for datum in data:
            if datum < 0:
                raise ValueError(
                    f"Entry for element {datum} is negative but log-scale is selected"
                )
        color_mapper = LogColorMapper(
            palette=bokeh_palette, low=lower_boundary, high=upper_boundary
        )
        norm = LogNorm(vmin=lower_boundary, vmax=upper_boundary)
    else:
        color_mapper = LinearColorMapper(
            palette=bokeh_palette, low=lower_boundary, high=upper_boundary
        )
        norm = Normalize(vmin=lower_boundary, vmax=upper_boundary)

    color_scale = ScalarMappable(norm=norm, cmap=cmap).to_rgba(
        data.to_numpy(), alpha=None
    )

    return color_scale, color_mapper


def _make_bokeh_color_palette(cm_palette: LinearSegmentedColormap) -> tuple[list, bool]:
    palette_rgb = (255 * cm_palette(range(256))).astype("int")
    divergingPalette = cm_palette in [
        cm.coolwarm,
        cm.PiYG,
        cm.PRGn,  # type: ignore
        cm.BrBG,
        cm.PuOr,
        cm.RdGy,  # type: ignore
        cm.RdBu,
        cm.RdYlBu,
        cm.RdYlGn,  # type: ignore
        cm.Spectral,
        cm.bwr,
        cm.seismic,  # type: ignore
        cm.berlin,
        cm.managua,
        cm.vanimo,
    ]  # type: ignore
    return [RGB(*tuple(rgb)).to_hex() for rgb in palette_rgb], divergingPalette
