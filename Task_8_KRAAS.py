# -*- coding: utf-8 -*-
"""
Introduction to Programming and Applied Statistics

======================
Final Project - TASK 8
======================

Use the air-quality-covid19-response data from Lecture 10
(available on moodle) to address the following subtasks:
"""
# imports
import calendar
import pandas as pd
from pathlib import Path
import seaborn as sns

import bk_config as cfg 
import bk_functions as bk


# load all necessary data:

data = bk.load_cams_air_qual_data("air-quality-covid19-response", 2015, 2019)
keys = pd.read_csv(Path(r"air-quality-covid19-response\CAMS_AQ_LOCATIONS_V1.csv"))
keys_ge = keys.loc[keys["country"] == "Germany"] 
keys_ge_id_list = list(keys_ge["id"])
keys_ge_name_list = list(keys_ge["name"])

"""
Subtask 8.1
-----------
Create a new csv file that stores the 2015-2019 daily NO2 concetration
for all the cities in Germany. Replace the city_ids with the actual city
names. The result should be a single csv file.

Hint: Use the Path class from the pathlib module to point to 
      the folder with air-quality-covid19-response data (see Lecture 10).
"""

ls = []

# get df for every german city from "data"
for city_id in keys_ge_id_list:
    df1 = data.loc[data["city_id"] == city_id]
    ls.append(df1) # collect to list

# concatenate list
df_8_1 = pd.concat(ls)

# select only NO2 and city_id
df_8_1_no2 = df_8_1.loc[:, ["NO2", "city_id"]]

# replace city_id with city_name (as required - i'd instead make a new column)
for city_id, name in zip(keys_ge_id_list, keys_ge_name_list):
    df_8_1_no2.loc[(df_8_1_no2.city_id == city_id),'city_id'] = name

# save as .csv
df_8_1_no2.to_csv(cfg.data / "german_cities_NO2_Task_8.csv")

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

ls = []

# add columns for month and year to easily use the pandas.pivot function
df_8_1_no2["year"]  = df_8_1_no2.index.year
df_8_1_no2["month"] = df_8_1_no2.index.month

statistics_df = df_8_1_no2.groupby(["month","city_id"]).agg(
        NO2_mean = ("NO2", "mean"),
        NO2_sem = ("NO2", "sem"),
        NO2_min = ("NO2", "min"),
        NO2_max = ("NO2", "max"),
    )


# - In which city, the NO2 concetration is greatest and when?
newdf = statistics_df.loc[statistics_df["NO2_max"].idxmax()]

print("Task 1:\nGreatest NO2 concentration:", newdf.name[1], \
      "\nMonth:", calendar.month_name[newdf.name[0]])


# - Which month the NO2 becomes maximum and minimum in Cologne?

# I interpret this as: Month with minimum and maximum mean :)
CITY = "Cologne"

# setup indices
statistics_df = statistics_df.reset_index()
statistics_df.set_index(['month'], inplace=True)

# locate data
months_max_month = statistics_df.groupby('city_id')['NO2_mean'].idxmax()
months_min_month = statistics_df.groupby('city_id')['NO2_mean'].idxmin()

# convert to int to use calendar.month_name
cgn_max_month = calendar.month_name[int(months_max_month[CITY])]
cgn_min_month = calendar.month_name[int(months_min_month[CITY])]

# print
print(f"\nTask 2:\nMonth with maximum average NO2 in {CITY.lower()}:", cgn_max_month)
print(f"         \nMonth with minimum average NO2 in {CITY.lower()}:", cgn_min_month)


# - What is the NO2 inter-annual range (i.e., the difference between
#   the max and min NO2 concentration) in each city?

print("\nTask 3:")

for name in keys_ge_name_list:
    city_df = statistics_df.loc[statistics_df["city_id"] == name]
    difference = city_df["NO2_mean"].max() - city_df["NO2_mean"].min()
    print(f"Difference in {name}:".ljust(25), difference)



"""
Subtask 8.3
-----------
Using the data from subtask 8.2 calculate the 95% lower and upper
confidence intervals for each monthly mean.
"""

DATADIR = r"C:\Users\panosis\Desktop\air-quality-covid19-response"
VARIABLES = ["NO2", "O3", "PM10"]
CRITICAL_VAL = -1.65 # one-tail critical value for 95% confidence level.

def hypothesis_testing(var="NO2"):
    """
    Test if the drop in Air quality during the first lockdown is statistically significant.

    Original code author: Panagiotis Sismanidis
    Edited by: Ben Kraas
    
    Not functional
    """
    
    if var not in VARIABLES:
        raise ValueError("Invalid variable name.")
    
    data = pd.read_csv(cfg.wd / "city_means_lockdown1.csv")  
    data.set_axis(data["name"], inplace=True)
    
    z_scores = (data[f"{var}_mean_lockdown"] - data[f"{var}_mean_precovid"]) / data[f"{var}_sem_precovid"]
    
    # Print the test results
    print(f"\nIs the drop in {var} statistically significant at the 5/% level?")
    for name, z in zip(z_scores.index, z_scores.values):    
        if z < CRITICAL_VAL:
            print(f"{name:<10} Yes")
        else:
           print(f"{name:<10} No")
    
    return z_scores

# unable


"""
Subtask 8.4
-----------
Use the csv from subtask 8.1 and calculate the monthly mean, minimum, and maximum
NO2 per year and city. Create a figure with 3 lineplots (one subplot for each statistic)
that present the corresponding monthly values for each german city.
"""
# load data
df_8_4 = pd.read_csv(cfg.data / "german_cities_NO2_Task_8.csv")
df_8_4["basetime"] = pd.to_datetime(df_8_4["basetime"])
df_8_4.set_index("basetime", inplace=True)

# calculate table
df_8_4["year"] = df_8_4.index.year
df_8_4["months"] = df_8_4.index.month
for city in keys_ge_id_list:
    df_8_41 = df_8_4.groupby(["year","months","city_id"]).agg(
        NO2_mean = ("NO2", "mean"),
        NO2_min = ("NO2", "min"),
        NO2_max = ("NO2", "max"),
    )

# not able to present this as a lineplot as I am using a multi-index to structure the data
















#######################################################
### Legacy
#######################################################

# code garbage for your enjoyment. I hope I don't forget to delete this.

# # legacy
# for city_name in keys_ge_namm_list:
#     per_city_df = df_8_1_no2.loc[df_8_1_no2["city_id"] == city_name]

#     months = per_city_df.index.month.rename("month")
#     monthly_means = per_city_df.groupby([months]).mean()
    
#     monthly_means.rename(columns={"NO2": city_name}, inplace=True)

#     #monthly_means.reset_index(drop=True, inplace=True)
#     ls.append(monthly_means)
#     #print(monthly_means)

# # concatenate into one nice dataframe
# final_df = pd.concat([ls[0].stack(), 
#                       ls[1].stack(), 
#                       ls[2].stack(), 
#                       ls[3].stack()], axis=0).unstack()

# # legacy
# ls = list()
# for city_id in keys_ge_id_list:
#     # this is not necessarily an elegant solution but one that is obvious.
#     # I had issues with pd.DataFrame.agg() so I chose this solution.
#     new_df = pd.DataFrame()
#     new_df["mean"] = data.loc[data["city_id"] == city_id, ["NO2"]].mean()
#     new_df["sem"]  = data.loc[data["city_id"] == city_id, ["NO2"]].sem()
#     new_df["min"] = data.loc[data["city_id"] == city_id, ["NO2"]].min()
#     new_df["max"] = data.loc[data["city_id"] == city_id, ["NO2"]].max()
    
#     xdf = keys_ge.loc[keys["id"] == city_id]
#     new_df["city_name"] = xdf.iloc[0]['name']
#     new_df["city_id"] = city_id
    
#     ls.append(new_df)

# final_df = pd.concat(ls)


# # Legacy: 

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


# # Legacy
# for city_id in keyslist:
#     mean = float(df.loc[df["city_id"] == city_id, ["NO2"]].mean())
#     sem  = float(df.loc[df["city_id"] == city_id, ["NO2"]].sem())
#     mini = float(df.loc[df["city_id"] == city_id, ["NO2"]].min())
#     maxi = float(df.loc[df["city_id"] == city_id, ["NO2"]].max())
#     print(mean, sem, mini, maxi)


# # Legacy
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

