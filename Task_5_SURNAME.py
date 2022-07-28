# -*- coding: utf-8 -*-
"""
Introduction to Programming and Applied Statistics

======================
Final Project - TASK 5
======================

You are given the geojson file `rivers.geojson`, which
represents all the major rivers of the world as linestrings.

Answer the following 4 tasks.


def save(dict, path):
    with open(path, "w") as f:
        json.dump(dict, f, indent=4)


Subtask 5.1
-----------
Use a for loop to print the name of each river.

for feature in rivers["features"]
    print(feature["properties"]["name"]

Subtask 5.2
-----------
Create a new geojson file that includes only the river Nile.

new_rivers = rivers
for feature in rivers["features"]
    name = feature["properties"]["name"]
    if lower(name) == "nile"
        new_rivers["features"] = feature
        break
if new_rivers["features"]:
       

Subtask 5.3
-----------
Calculate the length of each river and add it as a property.


Subtask 5.4
-----------
Create a new geojson file that includes only as a feature 
the second longest river.


Note: The coordinates in `rivers.geojson` are in meters.
      The CRS is the ESRI:53008 (https://epsg.io/53008)
"""

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
    