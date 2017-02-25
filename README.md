# Periodic Trend Plotter
Python script to plot periodic trends as a heat map over the periodic table of elements

Usage
-----
This Python script can be used to plot a heat map over an image of the periodic table of elements for easy and automated visualization of periodic trends. The required input and arguments are shown below. 

**Required Arguments**

The only required argument is the `filename` argument. This is the full name (with extension) of the data file containing your periodic trend data. The data file must be in a comma-separated value (CSV) format with the first entry in each row being the atom symbol and the second entry being the value you wish to plot. The atomic symbol is not case-sensitive, and the elemental data can be put in any order. Any element not included in the CSV file will still be a default gray color. An example CSV file is included in this repository for testing purposes under the name `ionization_energies.csv`. After the Python script is run, it will show the plot in your web browser (to save the image, simply click the save icon that appears in the web browser figure).

**Optional Arguments**

There are a number of optional arguments that can be used to quickly change settings in the `ptable_trends.py` script. 

Use the `--width` flag followed by a positive integer to set the width (in pixels) of the figure. The default is a width of 1050 pixels. 

Use the `--palette_choice` flag followed by an integer ranging from 0 to 3 to select one of the default color maps. A value of 0 is the default and selects the [plasma](https://bids.github.io/colormap/images/screenshots/option_c.png) color map, a value of 1 selects the [inferno](https://bids.github.io/colormap/images/screenshots/option_b.png) color map, a value of 2 selects the [magma](https://bids.github.io/colormap/images/screenshots/option_a.png) color map, and a value of 3 selects the [viridis](https://bids.github.io/colormap/images/screenshots/option_d.png) color map. 

Use the `--fill_alpha` flag followed by a float ranging from 0 to 1 to select the RGBA alpha value (a measure of the transparency). The default alpha value is 0.85.

Use the `--extended` flag followed by either 0 or 1 to select if you want the periodic table to include the lanthanides and actinides. The default value is 0 (don't show lanthanides and actinides). However, if your CSV file contains data for any of the lanthanides or actinides, these rows on the table will automatically be included (unless you manually specify `--extended 0`).

Use the `--cbar_height` flag followed by a positive integer to set the height (in pixels) of the color bar axis. The default is automatically chosen to be the full height of the figure.

Use the `--help` flag to see the aforementioned usage instructions.

Dependencies
-----

This script works for both Python 2.x and 3.x versions. The script requires the following dependencies:
* [Bokeh](http://bokeh.pydata.org/en/latest/) (and its dependencies)
* [pandas](http://pandas.pydata.org/) (and its dependencies)
* [matplotlib](http://matplotlib.org/) (and its dependencies)

These packages can be  installed using [pip](https://pip.pypa.io/en/stable/). However, since both Bokeh and matplotlib have multiple dependencies, it is much easier to install through the `conda install` command if you have an [Anaconda distribution](https://www.continuum.io/downloads) of Python. 

Example
-----

I show below some examples of the script in action using the `ionization_energies.csv` file included in this repository. Note that since the CSV file contains data for some of the lanthanides and actinides, the value of `--extended` defaults to 1 (instead of the usual 0) unless manually set otherwise.

`python ptable_trends.py ionization_energies.csv`

![plot1](http://i.imgur.com/Uxb8V0p.png)

`python ptable_trends.py ionization_energies.csv --extended 0`

![plot2](http://i.imgur.com/Att5d9X.png)

`python ptable_trends.py ionization_energies.csv --extended 0 --width 1100 --palette_choice 3 --fill_alpha 0.9`

![plot3](http://i.imgur.com/KJnlriu.png)
