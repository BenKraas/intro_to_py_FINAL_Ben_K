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

class GeojsonObject:
    """
    This class introduces an object-based approach to Geojson handling.
    Child objects on a per-feature basis could be implemented in the future.

    Author: Ben Kraas (https://github.com/KtRNofficial)
    """
    

    def __init__(self, geojson={}, name="default.geojson"):
        """
        Object can be populated by passing a geojson and name to the constructor 
        OR 
        it needs to be populated with loadwd() - specifying a path in working dir
        OR
        it needs to be populated with loadrel() - specifying a full path
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

    def dumpto(self, path: object):
        with open(path, "w") as fp:
            # use indent=4 to make json more readable
            json.dump(path.name, fp)
        
    def dump(self):
        self.dumpto(self.dict_path)
    
    def example():
        print(load_json("example.geojson"))

    def get_name(self, id):
        return self.dict["features"][id]["properties"]["name"]

    def get_names(self):
        name_list = []
        for feature in self.dict["features"]:
            name_list.append(feature["properties"]["name"])
        return name_list

    def get_type(self, id):
        """Returns the type of a single feature"""
        return self.dict["features"][id]["geometry"]["type"]

    def get_types(self):
        """Returns all types that occurr in the geojson"""
        type_set = set()
        for feature in self.dict["features"]:
            type_set.add(feature["geometry"]["type"])
        return type_set
    
    def get_feature_count(self):
        return len(self.dict["features"])
    
    def query_name(self, searchname):
        """
        search the geojson for a name
        Returns the ID for the first name found.
        If name was not found returns None 
        """
        for id, name in enumerate(self.get_names()):
            if name == searchname:
                return id
        return None

    def query_names(self, searchname):
        """
        Gives back a list of all IDs with a name
        If no items with the name are found returns None
        """
        nameids = []
        for id, name in enumerate(self.get_names()):
            if name == searchname:
                nameids.append(id)
        if nameids:
            return nameids
        return None

    def convert_to_multipoint(self, inplace=False):
        """Converts all """
        types = self.get_types()
        finalls = []
        if len(types) > 1:
            raise TypeError("Cannot convert more than one type")

        for feature in self.dict["features"]:
            for elem in feature["geometry"]["coordinates"]:
                partls = self.private_coordcrawler(elem)
                for elem in partls:
                    finalls.append(elem)

        if inplace:
            self.dict["features"] = []
            self.dict["features"].append(self.private_new_feature(type="MultiPoint"))
            self.dict["features"][0]["geometry"]["type"] = "MultiPoint"
            self.dict["features"][0]["geometry"]["coordinates"] = finalls

        else:
            retdict = self.dict
            retdict["features"][0]["geometry"]["type"] = "MultiPoint"
            retdict["features"][0]["geometry"]["coordinates"] = finalls
            return(self.private_set_features(retdict, finalls))

    def private_set_features(self, change_dict, content):
        change_dict["features"][0].append(content)
        return change_dict
    
    def private_new_feature(featuretype, coordinates):
        return {
            "type": "Feature",
            "geometry": {
                "type": featuretype,
                "coordinates": coordinates
            }
        }
        
    def convert_to_point(self):
        """Converts all coordinate pairs to points"""
        pass
    
    def private_coordcrawler(self, *args):
        coords = []
        for elem in args:
            if isinstance(elem[0], list):
                for atom in elem:
                    coords.append(atom)
            else:
                coords.append(elem)
        return coords