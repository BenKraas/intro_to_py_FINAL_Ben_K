from pathlib import Path
import bk_functions as bk

pathobj = Path("lakes.geojson")
jsonobj = bk.GeojsonObject()
jsonobj.loadwd(pathobj)
ptdict = jsonobj.convert_to_multipoint()