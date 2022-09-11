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


# load all necessary data:

data = bk.load_cams_air_qual_data("air-quality-covid19-response", 2015, 2019)
keys = pd.read_csv(Path(r"air-quality-covid19-response\CAMS_AQ_LOCATIONS_V1.csv"))
keys_ge = keys.loc[keys["country"] == "Germany"] 
keys_ge_id_list = list(keys_ge["id"])
keys_ge_nm_list = list(keys_ge["name"])

"""
Subtask 8.1
-----------
Create a new csv file that stores the 2015-2019 daily NO2 concetration
for all the cities in Germany. Replace the city_ids with the actual city
names. The result should be a single csv file.

Hint: Use the Path class from the pathlib module to point to 
      the folder with air-quality-covid19-response data (see Lecture 10).
"""

df1 = df.loc[:, ["UID", "land_cover", "mast"]]




### legacy
# idls = [keys.iloc[row] for row in df.loc["city_ids"]]

# pandas map ?

# print(idls)

final_df.to_csv('Task_8_1.csv') 


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

ls = list()
for city_id in keys_ge_id_list:
    # this is not necessarily an elegant solution but one that is obvious.
    # I had issues with pd.DataFrame.agg() so I chose this solution.
    new_df = pd.DataFrame()
    new_df["mean"] = data.loc[data["city_id"] == city_id, ["NO2"]].mean()
    new_df["sem"]  = data.loc[data["city_id"] == city_id, ["NO2"]].sem()
    new_df["mini"] = data.loc[data["city_id"] == city_id, ["NO2"]].min()
    new_df["maxi"] = data.loc[data["city_id"] == city_id, ["NO2"]].max()
    
    xdf = keys_ge.loc[keys["id"] == city_id]
    new_df["city_name"] = xdf.iloc[0]['name']
    new_df["city_id"] = city_id
    
    ls.append(new_df)

final_df = pd.concat(ls)




print(final_df)

# - In which city, the NO2 concetration is greatest and when?

# - Which month the NO2 becomes maximum and minimum in Cologne?

# - What is the NO2 inter-annual range (i.e., the difference between

#   the max and min NO2 concentration) in each city?



### legacy
# ls, new_df= list(), pd.DataFrame()
# for city_id in keyslist:
#     newdf = df.loc[df["city_id"] == city_id].agg(
#         {
#             "NO2": ["mean", "sem", "min", "max"],
#         }
#     )
#     newdf.reset_index(drop=True)
#     newdf["city_id"] = city_id
#     xdf = keys_germany.loc[keys["id"] == city_id]
#     newdf["city_name"] = xdf.iloc[0]['name']
#     ls.append(newdf)


### Legacy
# for city_id in keyslist:
#     mean = float(df.loc[df["city_id"] == city_id, ["NO2"]].mean())
#     sem  = float(df.loc[df["city_id"] == city_id, ["NO2"]].sem())
#     mini = float(df.loc[df["city_id"] == city_id, ["NO2"]].min())
#     maxi = float(df.loc[df["city_id"] == city_id, ["NO2"]].max())
#     print(mean, sem, mini, maxi)


### Legacy
# ls, new_df= list(), pd.DataFrame()
# for city_id in keyslist:
#     newdf = df.loc[df["city_id"] == city_id].agg(
#         {
#             "NO2": ["mean", "sem", "min", "max"],
#         }
#     )
#     newdf.reset_index(drop=True)
#     newdf["city_id"] = city_id
#     ls.append(newdf)
#     print(newdf)

# new_df = pd.concat(ls)

# dfpivot = new_df.pivot(index="city_id", columns=)


"""
Subtask 8.3
-----------
Using the data from subtask 8.2 calculate the 95% lower and upper
confidence intervals for each monthly mean.
"""



"""
Subtask 8.4
-----------
Use the csv from subtask 8.1 and calculate the monthly mean, minimum, and maximum
NO2 per year and city. Create a figure with 3 lineplots (one subplot for each statistic)
that present the corresponding monthly values for each german city.
"""


