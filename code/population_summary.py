import numpy as np
import pandas as pd
import os
import sys

def main(in_census_csv, out_summary_csv):
    # Creating the data frame
    df = pd.read_csv(in_census_csv)

    #Show rows where the column “DIM: Profile of Census Subdivisions (2247)” has the value of “Total - Age groups and average age of the population - 100% data”
    df_rows_filtered = df.loc[df["DIM: Profile of Census Subdivisions (2247)"] == "Total - Age groups and average age of the population - 100% data"]

    # filtering the resulting DataFrame for specific columns
    df_cols_filtered = df_rows_filtered[['GEO_CODE (POR)', 'GEO_NAME', 'Dim: Sex (3): Member ID: [1]: Total - Sex', 'Dim: Sex (3): Member ID: [2]: Male', 'Dim: Sex (3): Member ID: [3]: Female']]

    # Renaming the columns
    df_renamed = df_cols_filtered.rename(
        columns = {
            "GEO_CODE (POR)" : "GEOCODE",
            "GEO_NAME" : "GEONAME",
            "Dim: Sex (3): Member ID: [1]: Total - Sex" : "Total Pop.",
            "Dim: Sex (3): Member ID: [2]: Male" : "Male",
            "Dim: Sex (3): Member ID: [3]: Female" : "Female",
        }
    )

    #Filtering out the rows that have an 'x' value in the Total column
    df_without_x = df_renamed.loc[df_renamed["Total Pop."] != "x"]

    # exporting dataframe to csv
    df_without_x.to_csv(out_summary_csv, index=False)

if __name__ == '__main__':
    # Checking the number of arguments
    if len(sys.argv) != 3:
        print("Usage: population_summary.py in_census_csv out_summary_csv")
        sys.exit()

    # Checking if in_census_csv exists   
    if os.path.exists(sys.argv[1]):
        in_census_csv = sys.argv[1]
    else:
        print(f"The file {sys.argv[1]} does not exist.")
        sys.exit(1)
    
    out_summary_csv = sys.argv[2]
    
    main(in_census_csv, out_summary_csv)



