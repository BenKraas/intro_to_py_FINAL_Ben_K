# -*- coding: utf-8 -*-
"""
Introduction to Programming and Applied Statistics

======================
Final Project - TASK 2
======================

Use pandas to read the file `data.csv` and assign it to a variable named `df`.

Complete the following subtasks:

1. print the number of rows and columns of `df`?
2. print the datatype of each column.
3. What are the column names of `df`?
4. Use the methods `isna()` and `any()` to check if there any missing values.
5. Create a new dataframe called `df1` that includes only the columns `UID`, `land_cover` and `mast`.
6. Create a new dataframe called `df2` that includes only the rows in `df` where `land_cover` is equal to “urban”.
7. Create a new dataframe called `df3` that includes only the rows in `df` where `land_cover` is equal to “rural_bare” and `group` is equal to “workday”.
8. Create a new dataframe called `df4` that includes only the rows in `df` where `mast` is greater or equal to 295 and `yast` is lower than 20.
9. Calculate how many times “D” occurs in the column `overpass` of `df`.
10. Calculate the mean, min, max, std, and median of the column `mast` and `yast` in `df3`.
11. Subtract the value 273.15 from the column `mast` of `df`.
12. Create a new column in `df` called `result` by adding the corresponding rows from the columns `mast` and `yast`.
13. Delete the columns `theta` and `theta_unc` from `df`.
14. Rename the column `yast` of `df` to `YearlyAmplitude`.
15. Create a variable called `cities` that stores the unique `UID` values in `df`?
16. Create a histogram and a boxplot presenting the `mast` data in `df`.

"""

import pandas as pd
import os
import matplotlib.pyplot as plt

# empty console
os.system("cls")

# read the csv
df = pd.read_csv("data.csv")

# 1. print the number of rows and columns of `df`?
print(f"\nNr 1.\nRows: {len(df)}", f"Columns: {len(df.columns)}", end="\n")

# 2. print the datatype of each column.
print(f"\nNr 2.\nDatatypes by column: \n{str(df.dtypes)[:-14]} \n")

# 3. What are the column names of `df`?
print(f"\nNr 3.\nColumn names: \n{list(df.keys())}")

# 4. Use the methods `isna()` and `any()` to check if there any missing values.
print(f"\nNr 4.\nContains NaN values: \n{df.isna().any()}")

# 5. Create a new dataframe called `df1` that includes only the columns `UID`, `land_cover` and `mast`.
df1 = df.loc[:, ["UID", "land_cover", "mast"]]

# 6. Create a new dataframe called `df2` that includes only the rows in `df` where `land_cover` is equal to “urban”.
df2 = df.loc[df["land_cover"] == "urban"]

# 7. Create a new dataframe called `df3` that includes only the rows in `df` where `land_cover` is equal to “rural_bare” and `group` is equal to “workday”.
df3 = df.loc[(df["land_cover"] == "rural_bare") & \
             (df["group"] == "workday")]

# 8. Create a new dataframe called `df4` that includes only the rows in `df` where `mast` is greater or equal to 295 and `yast` is lower than 20.
df4 = df.loc[(df["mast"] >= 295) & \
             (df["yast"] <  20)]

# 9. Calculate how many times “D” occurs in the column `overpass` of `df`.
df9 = len( df.loc[df["overpass"] == "D"] ) # => 644

# 10. Calculate the mean, min, max, std, and median of the column `mast` and `yast` in `df3`.
df10 = df3.agg(
    {
        "mast": ["mean", "min", "max", "std", "median"],
        "yast": ["mean", "min", "max", "std", "median"],
    }
)

# 11. Subtract the value 273.15 from the column `mast` of `df`. 
"""Which df though? I'm guessing df3 since that's the one I did the .agg calculation on..."""
KELVIN = 273.15
with pd.option_context('mode.chained_assignment', None):
    # I realize that this is bad practice - suppressing a warning instead of fixing it.
    # However, I couldn't get the calculation done in a number of tried ways with this warning

    # Attempts:
    # df3["mast"] -= KELVIN
    # df3["mast"] = df3["mast"] - KELVIN
    # df3.loc[:, "mast"] = df3["mast"]
    # df3.loc[:, "mast"] = df3["mast"].apply(lambda x: x - KELVIN)
    # df3.loc[:, "mast"] = df3.loc[:, "mast"].apply(lambda x: x - KELVIN)

    # All yielded the "SettingWithCopyWarning" - warning
    
    # For now I'll stick with the easiest one, please let me know the proper way to do it!:
    df["mast"] -= KELVIN

# 12. Create a new column in `df` called `result` by adding the corresponding rows from the columns `mast` and `yast`.
df["result"] = df['mast'] + df["yast"]

# 13. Delete the columns `theta` and `theta_unc` from `df`.
df.drop(columns=['theta', 'theta_unc'], inplace=True)

# 14. Rename the column `yast` of `df` to `YearlyAmplitude`.
df.rename(columns={"yast": "YearlyAmplitude"}, inplace=True)

print(df)
# 15. Create a variable called `cities` that stores the unique `UID` values in `df`?
cities = df['UID'].unique()

# 16. Create a histogram and a boxplot presenting the `mast` data in `df`.
fig, axes = plt.subplots(nrows=2)

df.hist(column="mast", ax=axes[0])
df.boxplot(column="mast", grid=False, ax=axes[1])


# input("\nPress Enter to exit") # keeps console alive when running outside IDE