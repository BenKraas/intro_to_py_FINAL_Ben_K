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

because it completely messes up syntax highlighting in VSC  
and I can't have that during development.
"""

import json
import math
from pathlib import Path
import random

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


class Feature:
    """
    
    """
    def __init__(self, featuretype="Point", coordinates=[], properties={}, dictionary={}):
        if dictionary:
            self.dict = dictionary
        else:
            self.new(featuretype=featuretype, coordinates=coordinates, properties=properties)
        self.update()

    def set(self, dictionary):
        """Brute sets the entire feature dictionary"""
        self.dict = dictionary
        self.update()
    
    def new(self, featuretype="Point", coordinates=[], properties={}):
        """Creates the foundation of a new feature. Should be populated"""
        self.dict = {
            "type": "Feature",
            "properties": properties,
            "geometry": {
                "type": featuretype,
                "coordinates": coordinates
            }
        }
        self.update()

    def update(self):
        self.type = self.dict["geometry"]["type"]

    def get_coordinates(self):
        return self.dict["geometry"]["coordinates"]

    def get_coordinates_raw(self):
        pass

    def add_vertex(self, coordinates):
        ftype = self.dict["geometry"]["type"]
        if ftype == "MultiPoint": 
            self.dict["geometry"]["coordinates"].append(coordinates)
            insertindex = -1
        elif ftype == "Polygon": 
            self.dict["geometry"]["coordinates"].insert(-2, coordinates)

        

    def gen_randscatter(self, extent, number=10):
        """Generates a random scatter MultiPoint"""
        lon_E, lat_S, lon_W, lat_N = extent
        coordlist = []
        for x in range(number):
            randlon = random.uniform(lon_W, lon_E)
            randlat = random.uniform(lat_N, lat_S)
            coordlist.append([randlon, randlat])
        self.dict["geometry"]["coordinates"] = coordlist
    
    def gen_grid(self, extent, x_dist, y_dist):
        lon_E, lat_S, lon_W, lat_N = extent
        pointer_lon, pointer_lat = lon_W, lat_N

        print(pointer_lat, lat_S)
        while pointer_lat >= lat_S:
            # reset lon pointer
            pointer_lon = lon_W
            while pointer_lon <= lon_E:
                # create point
                self.add_vertex([pointer_lon, pointer_lat])
                # increment lon
                pointer_lon += x_dist
            # increment lat
            pointer_lat -= y_dist
        
    def gen_grid_adv(self, extent, x_dist, y_dist, matrixname="full", matrix=[[]]):
        """
        Creates a MultiPoint grid.
        Spacing can fully customized by providing a two-dimensional matrix with
        1/True and 0/False values which will draw/not draw a point respectively.

        Lists in matrix should all be of the same length.
        You can ignore this if you know what you are doing
        
        Alternatively, a matrixname for the grid can be passed, resulting in a 
        preconfigured grid.
        
        Possible names are: full, checkerboard, big_checkerboard, sparse, sparse_alt, diagonal,
        raster
        """
        if not matrix:
            if matrixname == "full":
                matrix = [[1]]
            elif matrixname == "checkerboard":
                matrix = [[1, 0], [0, 1]]
            elif matrixname == "big_checkerboard":
                matrix = [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]
            elif matrixname == "sparse":
                matrix = [[1, 0], [0, 0]]
            elif matrixname == "sparse_alt":
                matrix = [[0, 0], [0, 1]]
            elif matrixname == "diagonal":
                matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            elif matrixname == "raster":
                matrix = [[1], [1, 0, 0], [1, 0, 0]]
            else:
                raise ValueError("A correct matrix name or matrix must be provided")
        matlen, rowlen = len(matrix), len(matrix[0])

        # funct start
        lon_E, lat_S, lon_W, lat_N = extent
        pointer_lon, pointer_lat = lon_W, lat_N
        counter_lon, counter_lat = 0, 0
        while pointer_lat >= lat_S:
            # reset lon pointer
            matline = matrix[(counter_lat%matlen)]
            counter_lon, pointer_lon = 0, lon_W
            while pointer_lon <= lon_E:
                # create point
                matnum = matline[(counter_lon%len(matrix[counter_lat%matlen]))]
                if matnum:
                    self.add_vertex([pointer_lon, pointer_lat])
                # increment lon
                counter_lon += 1
                pointer_lon += x_dist
            # increment lat
            counter_lat += 1
            pointer_lat -= y_dist
        

class GeojsonObject:
    """
    This class introduces an object-based approach to geojson handling.
    Child objects on a per-feature basis could be implemented in the future.

    Author: Ben Kraas (https://github.com/KtRNofficial)
    """

    def __init__(self, geojson: dict={}, name: str="default.geojson"):
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
        if not geojson:
            geojson = new_geojson()
        self.dict = geojson
        self.dict_path = Path(name).absolute()

    # load data into object
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
        
    def set(self, dictionary: dict):
        """Sets the objects full dictionary to a provided one"""
        self.dict = dictionary
    
    def set_path(self, path: str):
        """Set the dictionarys' path including name"""
        self.dict_path = Path(path)
    
    def set_path_abs(self, abs_path: str):
        """Set the dictionarys' path including name in working dir"""
        self.dict_path = Path(abs_path).absolute()

    # manage data
    def append(self, feature):
        """
        Appends the specified feature to Geojson features.
        Can accept the Feature object
        """
        if isinstance(feature, dict):
            self.dict["features"].append(feature)
        else:
            self.dict["features"].append(feature.dict)

    def wipe(self):
        """Deletes all features from self.dict"""
        self.dict["features"] = []
    
    def clear(self):
        """Deletes all features from self.dict"""
        self.wipe() # is this function unnecessary and bad practice? Yes. I like both wipe and clear though

    # save data
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

    # get feature information
    def get_name(self, id: int):
        """Returns a features name from ID"""
        return self.dict["features"][id]["properties"]["name"]

    def get_names(self):
        """Returns all feature names"""
        name_list = []
        for feature in self.dict["features"]:
            name_list.append(feature["properties"]["name"])
        return name_list

    def get_type(self, id: int):
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

    def get_feature(self, id: int):
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
        
    def get_properties(self, id: int):
        if id is not None:
            return self.dict["features"][id]["properties"]
        raise ValueError(f"Properties for ID {id} is not accessible")
    
    # querys/searches
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

    # more advanced calculations (quite project specific)
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

        A conversion method is currently not planned (out of scope)
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

        A conversion method is currently not planned (out of scope)
        """
        # while it seems counterintuitive to have the same calculation take place
        # for both polygons and linestrings, it makes sense due to the way the dictionaries
        # are laid out
        return self.calc_circumference_geod(id)

    # type conversions
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
        
    def PRIVATE_coordcrawler(self, *args):
        """PRIVATE! Crawls through a coords dict and returns all coords individually"""
        coords = []
        for elem in args:
            if isinstance(elem[0], list):
                for atom in elem:
                    coords.append(atom)
            else:
                coords.append(elem)
        return coords