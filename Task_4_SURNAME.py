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



def bounds_to_geojson(coordinates: tuple, savepath: str):
    """
    This function creates a bounding box from four coordinates 
    (western and eastern longitude and northern and southern latitude) 
    in the format (lon_E, lat_S, lon_W, lat_N)

    GeoJSON is saved in the specified location - the savepath MUST 
    include the name and extension of the geojson

    Example: "script_dir//bounding_box.geojson"
    """

    cd = coordinates
    test_dictionary = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [cd[2], cd[3]],
                [cd[0], cd[3]],
                [cd[0], cd[1]],
                [cd[2], cd[1]],
                [cd[2], cd[3]]
            ]]
        }
    }
    with open(savepath, "w") as f:
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

with open(r"C:\Users\Kasto\OneDrive\Scripts\Python Seminar Übung\intro_to_py_FINAL_Ben_K\polygon.geojson", "r") as f:
    polygon = json.load(f)


# required by task
def single_poly_to_point(polydict: dict):
    """
    This function converts a single polygon to points.
    If multiple polygons are provided only the first one will be converted
    Returns a dict in geojson format
    """
    enddict = polydict
    print(enddict)
    enddict["features"][0]["geometry"]["type"] = "MultiPoint"
    enddict["features"][0]["geometry"]["coordinates"] = polydict["features"][0]["geometry"]["coordinates"][0]
    return enddict

# more versatile and likely more useful
def poly_to_point(polydict: dict):
    """
    This function converts all polygons in a geojson to points
    Returns a dict in geojson format
    """
    pointlist = []
    enddict = polydict
    for polygon in polydict["features"]:
        if polygon["geometry"]["type"] == "Polygon":
            for pointl in polygon["geometry"]["coordinates"]:
                for point in pointl:
                    print(point)
                    pointlist.append(point)
    enddict["features"][0]["geometry"]["type"] = "MultiPoint"
    enddict["features"][0]["geometry"]["coordinates"] = pointlist
    return enddict

print(poly_to_point(polygon))




