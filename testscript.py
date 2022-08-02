from pathlib import Path
import bk_functions as bk
import json

gobj = bk.GeojsonObject()
gobj.loadwd("rivers.geojson")

print(gobj.query_name("Mekong"))

var = "blub"
var.upper()
print(var)
