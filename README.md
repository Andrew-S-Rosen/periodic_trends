# Periodic Trend Plotter
Python script to plot periodic trends as a heat map over the periodic table of elements

Usage
-----
This Python script can be used to plot a heat map over an image of the periodic table of elements for easy and automated visualization of periodic trends. The inputs are shown below. 

**Required Arguments**

The only required argument is the `filename` argument. This is the full name (with extension) of the data file containing your periodic trend data. The data file must be in a comma-separated value (CSV) format with the first entry in each row being the atom symbol and the second entry being the value you wish to plot. The atomic symbol is not case-sensitive, and the elemental data can be put in any order. Any element not included in the CSV file will still be a default gray color. An example CSV file is included in this repository for testing purposes under the name `ionization_energies.csv`. After the Python script is run, it will show the plot in your web browser (to save the image, simply click the save icon that appears in the web browser figure).

**Optional Arguments**

There are a number of optional arguments that can be used to quickly change settings in the `ptable_trends.py` script. 

Use the `--width` flag followed by a positive integer to set the width (in pixels) of the figure. The default is a width of 1050 pixels. 

Use the `--palette_choice` flag followed by an integer ranging from 0 to 3 to select one of the default color maps. A value of 0 is the default and selects the [plasma](https://bids.github.io/colormap/images/screenshots/option_c.png) color map, a value of 1 selects the [inferno](https://bids.github.io/colormap/images/screenshots/option_b.png) color map, a value of 2 selects the [magma](https://bids.github.io/colormap/images/screenshots/option_a.png) color map, and a value of 3 selects the [viridis](https://bids.github.io/colormap/images/screenshots/option_d.png) color map. 

Use the `--fill_alpha` flag followed by a float ranging from 0 to 1 to select the RGBA alpha value (a measure of the transparency). The default alpha value is 0.85.

Use the `--extended` flag followed by either 0 or 1 to select if you want the periodic table to include the lanthanides and actinides. The default value is 0 (don't show lanthanides and actinides). However, if your CSV file contains data for any of the lanthanides or actinides, these rows on the table will automatically be included (unless you manually specify `--extended 0`).

Use the `--cbar_height` flag followed by a positive integer to set the height (in pixels) of the color bar axis. The default is automatically chosen to be the full height of the figure.

Typing `python ptable_trends.py --help` in the command line allows you see the aforementioned usage instructions, replicated below.

```
usage: ptable_trends.py [-h] [--width WIDTH]                            
                              [--palette_choice {0,1,2,3}]                    
                              [--fill_alpha FILL_ALPHA] [--extended {0,1}]    
                              [--cbar_height CBAR_HEIGHT]                     
                              filename                                        
                                                                              
Plot periodic trends as a heat map over the periodic table of elements        
                                                                              
positional arguments:                                                         
  filename              Filename (with extension) of CSV-formatted data       
                                                                              
optional arguments:                                                           
  -h, --help            show this help message and exit                       
  --width WIDTH         Width (in pixels) of figure                           
  --palette_choice {0,1,2,3}                                                  
                        Color palette choice: 0 = Plasma, 1 = Inferno, 2 =    
                        Magma, 3 = Viridis                                    
  --fill_alpha FILL_ALPHA                                                     
                        Alpha value for color scale (ranges from 0 to 1)      
  --extended {0,1}      Keyword for excluding (0) or including (1) the        
                        lanthanides and actinides (will automatically enable  
                        if lanthanides or actinides are present in the dataset
  --cbar_height CBAR_HEIGHT                                                   
                        Height (in pixels) of color bar
```


Dependencies
-----

This script works for both Python 2.x and 3.x versions. The script requires the following dependencies:
* [Bokeh](http://bokeh.pydata.org/en/latest/)
* [pandas](http://pandas.pydata.org/)
* [matplotlib](http://matplotlib.org/)

These packages can be easily installed using [pip](https://pip.pypa.io/en/stable/) and the simple `pip install` command or through the `conda install` command if you have an [Anaconda distribution](https://www.continuum.io/downloads) of Python. with an already installed version of Python. The latter is the easiest option, in my opinion.

Example
-----

I show below some examples of the script in action using the `ionization_energies.csv` file included in this repository.

`python ptable_trends.py ionization_energies.csv`

