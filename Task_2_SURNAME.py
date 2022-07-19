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

