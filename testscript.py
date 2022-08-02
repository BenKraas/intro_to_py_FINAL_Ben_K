from pathlib import Path
import bk_functions as bk
import json



dicti = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    -1,
                    1
                ],
                [
                    1,
                    1
                ],
                [
                    1,
                    -1
                ],
                [
                    -1,
                    -1
                ],
                [
                    -1,
                    1
                ]
            ]
        ]
    }
}

gobj = bk.GeojsonObject()
gobj.loadwd("rivers.geojson")
print(gobj.calc_total(gobj.calc_length_geod)/1000)


