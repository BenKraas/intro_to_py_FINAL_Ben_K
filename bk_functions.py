"""
Collection of functions and classes used repeatedly over all 8 tasks.
I hope that this is not against the "rules" for the final exercise.

Author: Ben Kraas (https://github.com/KtRNofficial)
"""

"""
Disclaimer:

I might not specify return values of functions as in

foo(bar: int) -> not_specified:
    pass

because it messes up syntax highlighting in VSC and 
I can't have that during development.
"""

import json
import math
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

def new_feature(featuretype="MultiPoint", coordinates=[], properties={}):
    """Returns the structure of a single Feature. Should be populated"""
    return {
        "type": "Feature",
        "properties": properties,
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

    def loadwd(self, path: object):
        """
        Loads a geosjon dict from working directory.
        This is the EASIEST way to load
        """
        self.dict_path = Path(path).absolute()
        self.dict = load_json(self.dict_path)
    
    def loadrel(self, path: object):
        """Loads a geosjon dict from a full system path including name."""
        self.dict_path = Path(path)
        self.dict = load_json(self.dict_path)
    
    def loadsample(self):
        pt = Path("sample.geojson").absolute()

        try:
            self.dict = load_json(pt)
            self.dict_path = pt
        except:
            raise ImportError("Sample geojson not found :(")

    def dumpto(self, path: object):
        with open(path, "w") as fp:
            # use indent=4 to make json more readable
            json.dump(self.dict, fp, indent=4)
        
    def dump(self, name=None):
        if name:
            newname = Path(name).absolute()
        else:
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
        if not type_set:
            return False
        return type_set

    def get_all_same_type(self):
        """Returns type if all features are of the same type and False if not"""
        types = self.get_types()
        if len(types) > 1:
            return False
        return True

    def get_feature(self, id):
        """Returns a feature dictionary by feature ID"""
        if id is not None:
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
        if id is not None and property:
            return self.dict["features"][id]["properties"].get(property)
        
    def get_properties(self, id):
        if id is not None:
            return self.dict["features"][id]["properties"]
        raise ValueError(f"Properties for ID {id} is not accessible")
    
    def query_name(self, searchname, casesensitive=False):
        """
        Search the geojson for a searchname. 
        Returns the ID for the first name found.
        If name was not found returns None.
        """
        if not casesensitive:
            searchname = searchname.lower()
        for id, name in enumerate(self.get_names()):
            if not casesensitive:
                name = name.lower()
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

    def query_all_property(self, propertyname):
        propls = []
        for id in range(self.get_feature_count()):
            propls.append(self.get_property(id, propertyname))
        return propls


    def calc_total(self, function):
        """
        Calculate a total value by running the passed function for every feature 
        Currently supported functions are:
        calc_length_geod
        calc_circumference_geod

        Example use would be: 
        total_len = lineobj.calc_total(lineobj.calc_length_geod)
        This would run the .calc_length_geod function for each feature in lineobj
        """
        total = 0
        for id in range(self.get_feature_count()):
            total += function(id)
        return total

    def calc_circumference_geod(self, id):
        """
        Calculates the circumference (m) of a Polygon
        Can only handle METRIC "coordinates" 

        A conversion method is currently not planned
        """
        coordlist = self.dict["features"][id]["geometry"]["coordinates"][0]

        ft_length = 0
        for coord, c_pair in enumerate(coordlist):
            if coord: # if id is used here to skip the zero-index - going from the second feature=>first to the end
                ft_length += math.dist(c_pair, coordlist[(coord-1)])
        return ft_length

    
    def calc_length_geod(self, id):
        """
        Calculates the length (m) of a LineString
        Can only handle METRIC "coordinates" 

        A conversion method is currently not planned
        """
        # while it seems counterintuitive to have the same calculation take place
        # for both polygons and linestrings, it makes sense due to the way the dictionaries
        # are laid out
        return self.calc_circumference_geod(id)

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