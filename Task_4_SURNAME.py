# -*- coding: utf-8 -*-
"""
Introduction to Programming and Applied Statistics

======================
Final Project - TASK 4
======================

Subtask 4.1
-----------
Define a function that takes as input the bounding box
coordinates (lon_E, lat_S, lon_W, lat_N) and a savepath.
The function should create a geojson polygon from
the given coordinates and save it at the given savepath.

Hint:  See the example below on how to save a geojson dictionary.
"""



# To save a geojson dict to a file adopt the following example:
test_dictionary = {
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
    json.dump(test_dictionary, f, indent=4)


"""
Subtask 4.2
-----------
Define a function that takes as input a geojson dictionary representing 
a polygon, extracts the points, and returns them as a geojson feature collection.
Test your code with the following polygon:

"""

# To read the `polygon.geojson` file use the following:
import json

with open("polygon.geojson", "r") as f:
    polygon = json.load(f)







