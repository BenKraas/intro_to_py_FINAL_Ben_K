# -*- coding: utf-8 -*-
"""
Introduction to Programming and Applied Statistics

======================
Final Project - TASK 5
======================

You are given the geojson file `rivers.geojson`, which
represents all the major rivers of the world as linestrings.

Answer the following 4 tasks.
"""
# imports
import json
import pandas as pd
from pathlib import Path

import bk_config as cfg
import bk_functions as bk

# clear console
bk.clear()

"""
Subtask 5.1
-----------
Use a for loop to print the name of each river.
for river in rivers.
"""

rivers = bk.GeojsonObject()

rivers.loadwd('rivers.geojson')

print(rivers.get_names())


"""
Subtask 5.2
-----------
Create a new geojson file that includes only the river Nile.
"""

id = rivers.query_name("Nile")

new_gjson = bk.GeojsonObject(bk.new_geojson())

new_feature = rivers.get_feature(id)
new_gjson.append(new_feature)

       
"""
Subtask 5.3
-----------
Calculate the length of each river and add it as a property.
"""
# if you did calculations on small scale maps you should use 
# geopy.distance.geodesic for greater precision

for river_id in range(rivers.get_feature_count()):
    rivers.dict["features"][river_id]["properties"]["river_length"] \
        = rivers.calc_length_geod(river_id)


lens = rivers.query_all_property("river_length")
names = rivers.get_names()
df = pd.DataFrame({"length": lens, 
                   "name": names, 
                   "dict_id": list(range(rivers.get_feature_count()))
                   })

"""
Subtask 5.4
-----------
Create a new geojson file that includes only as a feature 
the second longest river.


Note: The coordinates in `rivers.geojson` are in meters.
      The CRS is the ESRI:53008 (https://epsg.io/53008)
"""

sorted_df = df.sort_values(by="length", ascending=False)
sec_longest_river_id = sorted_df["dict_id"].iloc[1]

sl_river_obj = bk.GeojsonObject(bk.new_geojson())

sl_river_obj.append(rivers.get_feature(sec_longest_river_id))

sl_river_obj.dump(cfg.data / "second_longest_river.geojson")

















# Additional remarks (no longer part of exercise)



# To read the `rivers.geojson` file use the following:

import json

with open("rivers.geojson", "r") as f:
    rivers = json.load(f)


# To save a geojson dict to a file adopt the following example:
import json

test_linestring = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [0.0, 0.0],
            [50.0, 40.0]
        ]
    }
}

savename = "test.geojson"

with open(savename, "w") as f:
    json.dump(test_linestring, f, indent=4)
    