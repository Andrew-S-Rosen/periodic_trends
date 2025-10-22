import pandas as pd
from periodic_trends import plotter
from matplotlib import cm

if __name__ == "__main__":
    df = pd.read_csv("ionization_energies.csv", names = ["Element", "Ionization Energy"])
    plotter(df, "Element", "Ionization Energy", print_data = True, cmap = cm.PiYG)

