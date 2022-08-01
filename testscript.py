from pathlib import Path
import bk_functions as bk
import json

pathobj = Path("lakes.geojson")
jsonobj = bk.GeojsonObject()
jsonobj.loadwd(pathobj)
dicti = jsonobj.convert_to_multipoint()

