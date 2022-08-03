# -*- coding: utf-8 -*-
"""
Introduction to Programming and Applied Statistics

======================
Final Project - TASK 6
======================
"""
import bk_functions as bk

"""
Subtask 6.1
-----------
Define a function that creates a multipart geojson
with N points randomly distributed over a geographical domain.
The function should takes as arguments the number of points and
the bounding box coordinates (lon_E, lat_S, lon_W, lat_N) of the
geograhical domain.
"""
lon_E, lat_S, lon_W, lat_N = 90, 20, 20, 40

def gen_randpoint_dict(extent, number):
    feature = bk.Feature(featuretype="MultiPoint")
    feature.gen_randscatter(extent, number)
    mpgobj = bk.GeojsonObject()
    mpgobj.append(feature)
    return mpgobj

ftobj = gen_randpoint_dict((lon_E, lat_S, lon_W, lat_N), 200)

ftobj.set_path("randompoints.geojson")

ftobj.dump()

"""
Subtask 6.2
-----------
Define a function that creates a checkerboard grid of points for
a predifed geographic region. To do this your function should
generate points over a regular grid but keep only every second point.
The function should take as inputs:

- the distance between the points in the x- and in the y-dimension.
- the bounding box coordinates (lon_E, lat_S, lon_W, lat_N) of the
"""


"""
Subtask 6.3
-----------
Define a function that creates a randomized grid of points over
a predifed geographic region. To achieve this, your function should
generate points over a regular grid and then randomly shift them along
the x- and y-axis according to some random value. The random value should
not be greater than a max_shift threshold.

The function should take as inputs:

- the distance between the points in the x- and in the y-dimension.
- the max_shift value.
- the bounding box coordinates (lon_E, lat_S, lon_W, lat_N) of the
  geograhical domain


Hint: Check the material of L6.
"""
