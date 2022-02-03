# Periodic Trend Plotter
Python script to plot periodic trends as a heat map over the periodic table of elements.

Usage
-----
This Python script (`ptable_trends.py`) can be used to plot a heat map over an image of the periodic table of elements for easy and automated visualization of periodic trends.

A minimal example is as follows:
```python
from ptable_trends import ptable_plotter
ptable_plotter("ionization_energies.csv")
```
![plot1](example_images/plot1.png)

The only required argument to `ptable_plotter()` is a single positional argument for the full filepath/name (with extension) of the data file containing your periodic trend data. The data file must be in a comma-separated value (`.csv`) format with the first entry in each row being the atom symbol and the second entry being the value you wish to plot. An example `.csv` file is included in this repository for testing purposes under the name `ionization_energies.csv`. After the `ptable_trends.py` script is run, it will show the plot in your web browser. To save the image, simply click the save icon that appears in the web browser figure.

There are numerous optional arguments, which can be used to modify the appearance of the figure. The full argument list is below:
```
    Parameters
    ----------
    filename : str
        Path to the .csv file containing the data to be plotted.
    show : str
        If True, the plot will be shown.
    output_filename : str
        If not None, the plot will be saved to the specified (.html) file.
    width : float
        Width of the plot.
    cmap : str
        plasma, infnerno, viridis, or magma
    alpha : float
        Alpha value (transparency).
    extended : bool
        If True, the lanthanoids and actinoids will be shown.
    periods_remove : List[int]
        Period numbers to be removed from the plot.
    groups_remove : List[int]
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

    Returns
    -------
    figure
        Bokeh figure object.
```

A couple of examples using various optional keyword arguments are as follows:
```python
from ptable_trends import ptable_plotter
ptable_plotter("ionization_energies.csv", log_scale = True)
```
![plot2](example_images/plot2.png)

```python
from ptable_trends import ptable_plotter
ptable_plotter("ionization_energies.csv", cmap="viridis", alpha=0.7, extended=False, periods_remove=[1]
```
![plot3](example_images/plot3.png)

Dependencies
-----

The script requires the following dependencies:
* [Bokeh](http://bokeh.pydata.org/en/latest/)
* [pandas](http://pandas.pydata.org/)
* [matplotlib](http://matplotlib.org/)

These packages can be installed using [pip](https://pip.pypa.io/en/stable/) via `pip install -r requirements.txt` in the `ptable_trends` base directory.
