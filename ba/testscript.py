from pathlib import Path
import bk_functions as bk
import json

pathobj = Path("lakes.geojson")
jsonobj = bk.GeojsonObject()
jsonobj.loadwd(pathobj)
jsonobj.convert_to_multipoint(inplace=True)

jsonobj.dump()