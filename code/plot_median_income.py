import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt 
import seaborn as sns 
from matplotlib import rcParams 
import sys
import os

def main(in_csv, out_png):
    df = pd.read_csv(in_csv)

    #Filter 'DIM: Profile of Census Subdivisions (2247)' for 'Median total income in 2015 among recipients ($)'
    df_rows_filtered = df.loc[df["DIM: Profile of Census Subdivisions (2247)"] == "Median total income in 2015 among recipients ($)"]

    # filtering the resulting DataFrame for specific columns
    df_cols_filtered = df_rows_filtered[['GEO_CODE (POR)', 'Dim: Sex (3): Member ID: [1]: Total - Sex']]

    # Renaming the columns
    df_renamed = df_cols_filtered.rename(
        columns = {
            "GEO_CODE (POR)" : "GEOCODE",
            "Dim: Sex (3): Member ID: [1]: Total - Sex" : "Median Income",
        }
    )

    df_index = df_renamed.set_index('GEOCODE')

    #Filter out rows where the Median Income column is “x”, “F”, or “..”
    condition_1 = df_index['Median Income'] != 'x'
    condition_2 = df_index['Median Income'] != 'F'
    condition_3 = df_index['Median Income'] != '..'
    df_filtered = df_index[condition_1 & condition_2 & condition_3]

    # Use the pandas to_numeric method to convert the ‘Median Income’ column from strings (object) to numbers
    df_filtered.loc[:, 'Median Income'] = pd.to_numeric(df_filtered['Median Income'])

    # Use the Dataframe plot method with kind=’hist’ to plot the histogram using matplotlib
    # df_filtered['Median Income'].plot(kind = 'hist')

    # Use the seaborn histplot method to create a plot of the DataFrame’s one column of values (median income).  Assign the output of this method to a variable (e.g. histo)
    histo = sns.histplot(df_filtered['Median Income'])

    # The histo variable refers to a matplotlib AxesSubplot.  Use the get_figure method to get the matplotlib Figure associated with the AxesSubplot and assign that to a variable (e.g. fig)
    fig = histo.get_figure()

    # Use the savefig method on the matplotlib Figure object to save the figure to a file.  The file extension will determine the type of file created (e.g. png, jpg, etc.)
    fig.savefig(out_png)

if __name__ == '__main__':
    # Checking the number of arguments
    if len(sys.argv) != 3:
        print("Usage: plot_median_income.py in_csv out_png")
        sys.exit()

    # Checking if in_csv exists   
    if os.path.exists(sys.argv[1]):
        in_csv = sys.argv[1]
    else:
        print(f"The file {sys.argv[1]} does not exist.")
        sys.exit(1)
    
    out_png = sys.argv[2]

    main(in_csv, out_png)
