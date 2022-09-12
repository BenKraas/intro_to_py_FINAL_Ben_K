# -*- coding: utf-8 -*-
"""
Introduction to Programming and Applied Statistics

======================
Final Project - TASK 7
======================
"""
# imports
import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd
# from pathlib import Path
import random
import seaborn as sns
# import time # because I'm curious about code performance

import bk_config as cfg
import bk_functions as bk

# clear console
bk.clear()

"""
Use the air-quality-covid19-response data from Lecture 10
(available on moodle) to address the following subtasks:

Subtask 7.1
-----------
Create a new dataframe with the 2015-2019 daily NO2 and
O3 concetrations for Athens. Add a new column with
the season (i.e., winter, spring, summer, and autumn).

Hint: Use the Path class from the pathlib module to point to
      the folder with air-quality-covid19-response data (see Lecture 10).
"""
# load data
df = bk.load_cams_air_qual_data(start_year=2015, end_year=2019)

# select only NO2 and O3 for athens
df = df.loc[df["city_id"] == "AQ003", ["NO2", "O3"]]

# cheeky month mapping
names = [None,"winter", "winter", "spring", "spring", "spring", "summer", 
         "summer", "summer", "fall", "fall", "fall", "winter"]
df["season"] = [names[row.month] for row in df.index]

# check whether only the 4 seasons occurr
seasons = df["season"].unique() 
# => this is the case



# legacy code:
# I shared the following code in our WhatsApp group:

    # season = []
    # for row in df.index:
    #     if   row.month in [12, 1, 2]: season.append("winter")
    #     elif row.month in [3, 4, 5]:  season.append("spring")
    #     elif row.month in [6, 7, 8]:  season.append("summer")
    #     elif row.month in [9, 10, 11]:season.append("fall")
    #     else: print("Won't happen")

    # df["season"] = season

# /// end of shared code


"""
Subtask 7.2
-----------
Randomly select 7000 rows from the dataframe of subtask 7.1. Use seaborn
to create a scatterplot presenting the randomly selected NO2 and O3 values.
Your figure should also include a linear regression line.

Hint: https://seaborn.pydata.org/generated/seaborn.lmplot.html#seaborn.lmplot (See example 1)
"""

def randselect(data: pd.DataFrame, iterations: int) -> pd.DataFrame:
    """
    Randomly selects a set number of rows from a dataset,
    concats and returns them as a dataframe
    """
    randlist = []
    for foo in range(iterations):
        randnum = random.randint(0, len(df)-1)
        value = data.iloc[[randnum]]
        randlist.append(value)
    return pd.concat(randlist, axis=0)


rand_df_7_2 = randselect(df, 700)

# plot
ax2 = sns.lmplot(x="O3", y="NO2", data=rand_df_7_2, aspect=2, markers=".", \
                 scatter_kws={'alpha':0.15})



"""

Subtask 7.3
-----------
Randomly select 28000 rows from the dataframe of subtask 7.1. Use seaborn
to create a scatterplot presenting the randomly selected NO2 and O3 values
per season. Each subplot should also include a linear regression line.

Hint: https://seaborn.pydata.org/generated/seaborn.lmplot.html#seaborn.lmplot (See example 7)
"""
# uncommmented for code performance

# randlist7_3 = randselect(df, 28000)
# sns.lmplot(x="O3", y="NO2", data=randlist7_3, aspect=2, markers=".", \
#            scatter_kws={'alpha':0.15}, col_wrap=2, col="season")

"""
Subtask 7.4
-----------
Use seaborn to create a figure that presents Athens' NO2 and O3 distributions
per season. The figure should include 8 subplots arranged in 2 rows and 4 columns.
Each row should include 4 histrogramms (one per season). The first row should present
the NO2 distribution and the the second the O3.

Hint: https://seaborn.pydata.org/examples/faceted_histogram.html
"""

# I was unable to pack NO3 and O3 into a single displot.
# This is my attempt with incorrect syntax:

# sns.displot(
#    df, y="O3", col="season", row=("O3", "NO2"),
#    binwidth=3, height=3, facet_kws=dict(margin_titles=True),
# )
#
# row=("O3", "NO2") not allowed!


# the diagrams have to be observed with caution: the ranges are not comparable.
# I could not figure out how to strech the diagrams 
# to x_range = [0, 100] and y = [0, 100]
sns.displot(df, x="NO2",col="season", kde=True, kde_kws={'cut': 0})
sns.displot(df, x="O3" ,col="season", kde=True, kde_kws={'cut': 0})

"""
Subtask 7.5
-----------
Calculate the mean NO2 concentration per month and year (for Athens) and
use seaborn to plot the result as a heatmap.

Hint: https://seaborn.pydata.org/generated/seaborn.heatmap.html#seaborn.heatmap
"""

# calculate monthly means as df
df75 = df.resample('M', axis=0).mean()

# add columns for month and year to easily use the pandas.pivot function
df75['year']  = df75.index.year
df75['month'] = df75.index.month

# pivot the table so months go on the y-axis and years on the x-axis
df75_2 = df75.pivot("month", "year", "NO2")

# plot  (uncomment to see in spyder - plots):
#ax = sns.heatmap(df75_2)


"""
Subtask 7.6
-----------
What format codes should be used for coverting the
following datestrings to datetime objects?

    Datestrings                                      Format Code
-----------------------------------------------------------------------------
   24-March-2014                    |           %e-%b-%Y
   24.03.2014 15:23 CEST            |           %d.%m.%Y %H:%M %Z
   Oct 24, 2020                     |           %b %e, %Y
   20210430                         |           %Y%m%d
   Sunday, September 8, 2013        |           %A, %B %e, %Y 

Hint: https://strftime.org/

"""
# 7.6 DONE! (just a reminder to myself)