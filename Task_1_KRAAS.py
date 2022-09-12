# -*- coding: utf-8 -*-
"""
Introduction to Programming and Applied Statistics

======================
Final Project - TASK 1
======================

You are given the geojson file “lakes.geojson”, which represents all the major
lakes of the world as polygon features. Answer the following 15 tasks.

Hint: To solve the tasks below, specify the keys and the indices you need manually.

"""

# imports
import bk_config as cfg
import bk_functions as bk

# clear console
bk.clear()

### config:
# printing the list will display all results
PRINT_LIST = True


# To read the `lakes.geojson` file use the following:
import json

with open(cfg.wd / "lakes.geojson", "r") as f:
    lakes = json.load(f)

ls = list() 

# 1. What is the datatype of `lakes`?
ls.append(type(lakes))
# => <class 'dict'>


# 2. How many items are in `lakes`?
ls.append(len(lakes))
# => 3

# 3. How many items are in `features`?
ls.append(len(lakes["features"]))
# => 25


# 4. What is the datatype of `features`?
ls.append(type(lakes["features"]))
# => <class 'list'>


# 5. What are the properties of each feature?
ls.append(str(lakes["features"][0]["properties"].keys())[11:-2]) # 
# => 'scalerank', 'featurecla', 'name', 'name_alt', 
#    'admin', 'min_zoom', 'min_label'


# 6. What is the datatype of the “name” property?
ls.append(type(lakes["features"][0]["properties"]["name"]))
# => <class 'str'>


# 7. What is the datatype of the “bbox” field?
ls.append(type(lakes["bbox"]))
# => <class 'list'>


# 8. What is the datatype of the “geometry” field?
ls.append(type(lakes["features"][0]["geometry"]))
# => <class 'dict'>


# 9. What is the datatype of the “coordinates” field?
ls.append(type(lakes["features"][0]["geometry"]["coordinates"]))
# => <class 'list'>




# Next, use python to assign the following to new variables:
#
# 10. The name of the first lake.
name_first_lake = lakes["features"][0]["properties"]["name"]
ls.append(name_first_lake) # variable
# => (Lake) Baikal


# 11. The name of the second lake.
name_second_lake = lakes["features"][1]["properties"]["name"]
ls.append(name_second_lake)
# => (Lake) Winnipeg


# 12. The name of the last lake.
name_last_lake = lakes["features"][-1]["properties"]["name"]
ls.append(name_last_lake)
# => (Lake) Michigan


# 13. The coordinates of Lake Ontario.
lake_name = "L. Ontario"
for feature in lakes["features"]:
	if feature["properties"]["name"] == lake_name:
		ls.append(f'Coordinates for {lake_name}:{feature["geometry"]["coordinates"]})')


# 14. The bbox of Lake Superior.
lake_name = "Lake Superior"
for feature in lakes["features"]:
	if feature["properties"]["name"] == lake_name:
		ls.append(f'Bounding box for {lake_name}: {feature["bbox"]})')


# Finally,
#
# 15. Delete the first three items, i.e. the lakes Baikal,
# Winnipeg, Slave Lake, from the “features” list.

lakes["features"] = lakes["features"][3:] # keeps 4 to end - effectively deleting index 0, 1, 2

ls.append(len(lakes["features"])) # confirm that the list has been shortened



if PRINT_LIST:
	for number in ls:
		print(str(number).replace("\n", ""))