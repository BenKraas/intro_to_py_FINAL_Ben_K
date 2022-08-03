from pathlib import Path
import bk_functions as bk
import json


gobj = bk.GeojsonObject(bk.new_geojson())

ft = bk.Feature(featuretype="MultiPoint")
extent=(90.00252, 20.225, 20.1, 40.3)
ft.gen_grid_adv(extent, 5.142245, 4.18884, matrixname="checkerboard")
gobj.append(ft)

print(gobj.dict)


