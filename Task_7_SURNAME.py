# -*- coding: utf-8 -*-
"""
Introduction to Programming and Applied Statistics

======================
Final Project - TASK 7
======================
"""
from pathlib import Path
import pandas as pd
import numpy as np
import random
import time # because I'm curious about code performance

import seaborn as sns

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

def load_cams_air_qual_data(folderpath: str, start_year: int=2015, end_year: int= 2050) -> pd.DataFrame:
    """
    Specific function to load all "cams_air_quality_analysis_".csv files.
    Returns all files concatinated and properly formated with basetime as datetime index.
    A path to the data folder must be provided
    Both start_year and end_year are included in the returned DataFrame
    """
    dflist = []
    # we can try to import every csv name up to 2050 (function default)
    # That way, no "end"-year needs to be defined
    try:
        for date in range(start_year, (end_year+1)):
            datapath = Path(rf"{folderpath}\cams_air_quality_analysis_{date}.csv")
            df = pd.read_csv(datapath)
            dflist.append(df)
    except:
        pass

    new_df = pd.concat(dflist, axis=0)
    new_df['basetime'] = pd.to_datetime(new_df['basetime'])
    new_df = new_df.set_index('basetime')
    return new_df

# load data
df = load_cams_air_qual_data("air-quality-covid19-response", 2015, 2019)

# select only NO2 and O3 for athens
df = df.loc[df["city_id"] == "AQ003", ["NO2", "O3"]]

# cheeky month mapping
names = ["winter", "winter", "spring", "spring", "spring",
         "summer", "summer", "summer", "fall", "fall", "fall", "winter"]
df["season"] = [names[(row.month-1)] for row in df.index]







# legacy code:
# I shared the following code in our Whatsapp group - hope this was OK:

    # season = []
    # for row in df.index:
    #     if   row.month in [12, 1, 2]: season.append("winter")
    #     elif row.month in [3, 4, 5]:  season.append("spring")
    #     elif row.month in [6, 7, 8]:  season.append("summer")
    #     elif row.month in [9, 10, 11]:season.append("fall")

    # df["season"] = season

# end of shared code


"""
Subtask 7.2
-----------
Randomly select 7000 rows from the dataframe of subtask 7.1. Use seaborn
to create a scatterplot presenting the randomly selected NO2 and O3 values.
Your figure should also include a linear regression line.

Hint: https://seaborn.pydata.org/generated/seaborn.lmplot.html#seaborn.lmplot (See example 1)
"""

# get df length
def randselect(data: pd.DataFrame, iterations: int) -> pd.DataFrame:
    randlist = []
    for foo in range(iterations):
        randnum = random.randint(0, len(df)-1)
        value = data.iloc[[randnum]]
        randlist.append(value)
    return pd.concat(randlist, axis=0)

randlist7_2 = randselect(df, 7000)
sns.lmplot(x="O3", y="NO2", data=randlist7_2, aspect=2, markers=".", \
           scatter_kws={'alpha':0.15})




"""

Subtask 7.3
-----------
Randomly select 28000 rows from the dataframe of subtask 7.1. Use seaborn
to create a scatterplot presenting the randomly selected NO2 and O3 values
per season. Each subplot should also include a linear regression line.

Hint: https://seaborn.pydata.org/generated/seaborn.lmplot.html#seaborn.lmplot (See example 7)
"""

randlist7_2 = randselect(df, 28000)
sns.lmplot(x="O3", y="NO2", data=randlist7_2, aspect=2, row="season", markers=".", \
           scatter_kws={'alpha':0.15})


"""
Subtask 7.4
-----------
Use seaborn to create a figure that presents Athens' NO2 and O3 distributions
per season. The figure should include 8 subplots arranged in 2 rows and 4 columns.
Each row should include 4 histrogramms (one per season). The first row should present
the NO2 distribution and the the second the O3.

Hint: https://seaborn.pydata.org/examples/faceted_histogram.html
"""


"""
Subtask 7.5
-----------
Calculate the mean NO2 concentration per month and year (for Athens) and
use seaborn to plot the result as a heatmap.

Hint: https://seaborn.pydata.org/generated/seaborn.heatmap.html#seaborn.heatmap
"""

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