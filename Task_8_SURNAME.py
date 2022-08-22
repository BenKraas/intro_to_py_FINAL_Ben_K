# -*- coding: utf-8 -*-
"""
Introduction to Programming and Applied Statistics

======================
Final Project - TASK 8
======================

Use the air-quality-covid19-response data from Lecture 10
(available on moodle) to address the following subtasks:
"""

import bk_functions as bk
import pandas as pd
from pathlib import Path


"""
Subtask 8.1
-----------
Create a new csv file that stores the 2015-2019 daily NO2 concetration
for all the cities in Germany. Replace the city_ids with the actual city
names. The result should be a single csv file.

Hint: Use the Path class from the pathlib module to point to 
      the folder with air-quality-covid19-response data (see Lecture 10).
"""

df = bk.load_cams_air_qual_data("air-quality-covid19-response", 2015, 2019)
keys = pd.read_csv(Path(fr"air-quality-covid19-response\CAMS_AQ_LOCATIONS_V1.csv"))

# idls = [keys.iloc[row] for row in df.loc["city_ids"]]

# pandas map ?

# print(idls)


"""
Subtask 8.2
-----------
Calculate the monthly mean, SEM (standard error of the mean),
minimum, and maximum NO2 concentration per German city.
Answer the following:
- In which city, the NO2 concetration is greatest and when?
- Which month the NO2 becomes maximum and minimum in Cologne?
- What is the NO2 inter-annual range (i.e., the difference between
  the max and min NO2 concentration) in each city?
"""

keys_germany = keys.loc[keys["country"] == "Germany"] 

keyslist = list(keys_germany["id"])

new_df = pd.DataFrame()
ls = []

for city_id in keyslist:
    ls.append(df.loc[df["city_id"] == city_id].agg(
        {
            "NO2": ["mean", "sem", "min", "max"],
        }
    ))

new_df = pd.concat(ls)
print(new_df)
  
# df2 = df.agg(
#     {
#         "NO2": ["mean", "min", "max", "std", "median"],
#     }
# )


"""
Subtask 8.3
-----------
Using the data from subtask 8.2 calculate the 95% lower and upper
confidence intervals for each monhtly mean.
"""



"""
Subtask 8.4
-----------
Use the csv from subtask 8.1 and calculate the monthly mean, minimum, and maximum
NO2 per year and city. Create a figure with 3 lineplots (one subplot for each statistic)
that present the corresponding monthly values for each german city.
"""