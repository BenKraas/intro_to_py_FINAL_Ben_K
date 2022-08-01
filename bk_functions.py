"""
Small collection of functions repeating over all 8 tasks

Author - Ben Kraas
"""

"""
Disclaimer:

I might not specify return values of functions as in
foo(bar: int) -> not_specified:
because it messes with syntax highlighting.
"""

import json
from pathlib import Path

def load_json(path):
    """loads and returns a json dict"""
    with open(path) as json_file:
        data = json.load(json_file)
    return data

def beautydump(jsondict: dict, savepath):
    with open(savepath, "w") as f:
        json.dump(jsondict, f, indent=4)

def dump(jsondict: dict, savepath):
    with open(savepath, "w") as f:
        json.dump(jsondict, f)

def new_geojson():
    """Return the structure of a geojson dictionary"""
    return {
        "type": "FeatureCollection",
        "features": []
    }

def new_feature(featuretype="MultiPoint", coordinates=[]):
    """Returns the structure of a single Feature. Can be populated"""
    return {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": featuretype,
            "coordinates": coordinates
        }
    }

class GeojsonObject:
    """
    This class introduces an object-based approach to geojson handling.
    Child objects on a per-feature basis could be implemented in the future.

    Author: Ben Kraas (https://github.com/KtRNofficial)
    """

    def __init__(self, geojson={}, name="default.geojson"):
        """
        Initializes the GeojsonObject

        Object must be populated by passing a geojson and name to the constructor 
        OR 
        it must be populated with loadwd() - specifying a path in working dir (EASIEST)
        OR
        it must be populated with loadrel() - specifying a full path
        OR
        it must be populated with loadsample() - a sample dictionary will be loaded
        """
        self.dict = geojson
        self.dict_path = Path(name).absolute()

    def loadwd(self, path):
        """
        Loads a geosjon dict from working directory.
        This is the EASIEST way to load
        """
        self.dict_path = Path(path).absolute()
        self.dict = load_json(self.dict_path)
    
    def loadrel(self, path):
        """Loads a geosjon dict from a full system path including name."""
        self.dict_path = Path(path)
        self.dict = load_json(self.dict_path)
    
    def loadsample(self):
        pt = Path("sample.geojson").absolute()
        try:
            self.dict = load_json(self.dict_path)
            self.dict_path = pt
        except:
            raise ImportError("Sample geojson not found :(")

    def dumpto(self, path):
        with open(path, "w") as fp:
            # use indent=4 to make json more readable
            json.dump(self.dict, fp, indent=4)
        
    def dump(self):
        newname = Path("edited_" + self.dict_path.name).absolute()
        self.dumpto(newname)

    def get_name(self, id):
        """Returns a features name from ID"""
        return self.dict["features"][id]["properties"]["name"]

    def get_names(self):
        """Returns all feature names"""
        name_list = []
        for feature in self.dict["features"]:
            name_list.append(feature["properties"]["name"])
        return name_list

    def get_type(self, id):
        """Returns a features type from ID"""
        return self.dict["features"][id]["geometry"]["type"]

    def get_types(self):
        """Returns all feature types that occurr in the geojson"""
        type_set = set()
        for feature in self.dict["features"]:
            type_set.add(feature["geometry"]["type"])
        return type_set

    def get_feature(self, id):
        """Returns a feature dictionary by feature ID"""
        if id:
            return self.dict["features"][id]
    
    def get_features(self, id_list):
        """Returns all feature dictionaries from an ID list"""
        features = []
        for id in id_list:
            features.append(self.get_feature(id))
        return features
    
    def get_feature_count(self):
        """Returns the number of individual features"""
        return len(self.dict["features"])
    
    def get_property(self, id, property):
        if id and property:
            return self.dict["features"][id]["properties"].get(property)
        
    def get_properties(self, id):
        if id:
            return self.dict["features"][id]["properties"]
        raise ValueError(f"Properties for ID {id} is not accessible")
    
    def query_name(self, searchname):
        """
        Search the geojson for a searchname
        Returns the ID for the first name found.
        If name was not found returns None 
        """
        for id, name in enumerate(self.get_names()):
            if name == searchname:
                return id
        return None

    def query_names(self, searchname):
        """
        Gives back a list of all IDs with the searchname
        If no items with the name are found returns None
        """
        nameids = []
        for id, name in enumerate(self.get_names()):
            if name == searchname:
                nameids.append(id)
        if nameids:
            return nameids
        return None

    def append(self, featuredict):
        """Appends the specified featuredict to features"""
        if featuredict:
            self.dict["features"].append(featuredict)

    def wipe(self):
        """Deletes all features from self.dict"""
        self.dict["features"] = []
    
    def clear(self):
        """Deletes all features from self.dict"""
        self.wipe() # is this function unnecessary and bad practice? Yes. I like both wipe and clear though

    def convert_to_multipoint(self, inplace=False):
        """This function converts all polygons in a geojson to a single MultiPoint feature"""
        types = self.get_types()
        finalls = []
        if len(types) > 1:
            raise TypeError("Cannot convert more than one type")

        for feature in self.dict["features"]:
            for elem in feature["geometry"]["coordinates"]:
                partls = self.PRIVATE_coordcrawler(elem)
                for elem in partls:
                    finalls.append(elem)

        if inplace:
            self.wipe()
            self.dict["features"].append(new_feature(featuretype="MultiPoint", coordinates=finalls))
            # self.dict["features"][0]["geometry"]["coordinates"] = finalls

        else:
            retdict = self.dict
            retdict["features"] = []
            retdict["features"].append(new_feature(featuretype="MultiPoint", coordinates=finalls))
            return retdict

    def convert_to_multipoint_alt(self, inplace=False):
        """
        DEPRECATED!

        This function converts all polygons in a geojson to a single MultiPoint feature
        """
        pointlist = []
        enddict = self.dict

        for polygon in self.dict["features"]:
            if polygon["geometry"]["type"] == "Polygon":
                for pointl in polygon["geometry"]["coordinates"]:
                    for point in pointl:
                        print(point)
                        pointlist.append(point)
        enddict["features"][0]["geometry"]["type"] = "MultiPoint"
        enddict["features"][0]["geometry"]["coordinates"] = pointlist

        if inplace:
            self.dict = enddict
        else:
            return enddict
    
    def new_feature(self, featuretype, coordinates):
        return {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": featuretype,
                "coordinates": coordinates
            }
        }
        
    def PRIVATE_coordcrawler(self, *args):
        coords = []
        for elem in args:
            if isinstance(elem[0], list):
                for atom in elem:
                    coords.append(atom)
            else:
                coords.append(elem)
        return coords