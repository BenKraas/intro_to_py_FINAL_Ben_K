"""
Collection of functions, classes and methods used repeatedly over most of the 8 tasks.
I hope that this is not against the "rules" for the final exercise.

Author: Ben Kraas (https://github.com/KtRNofficial)
"""
# imports
import json
import math
import pandas as pd
from pathlib import Path
import random
import os


# read/write functions
def load_json(path: Path) -> dict:
    """loads and returns a json dict"""
    with open(path) as json_file:
        data = json.load(json_file)
    return data

def load_cams_air_qual_data(folderpath: str, start_year: int=2015, end_year: int=2050) -> pd.DataFrame:
    """
    Specific function to load all "cams_air_quality_analysis_".csv files.
    Returns all files concatinated and properly formated with basetime as datetime index.
    A path to the data folder must be provided
    Both start_year and end_year are included in the returned DataFrame
    """
    dflist = []
    # we can try to import every csv name up to 2050 (function default)
    # That way, no "end"-year needs to be defined

    for date in range(start_year, (end_year+1)):
        try:
            # sometimes broken, even though it should not be. Maybe because of whitespace in folder name. 
            datapath = Path(rf"{folderpath}\\cams_air_quality_analysis_{date}.csv").absolute() 
            df = pd.read_csv(datapath)
            dflist.append(df)
        except:
            print("This did not work even though it should :(\nThis problem can occurr if you have the repo saved in a path with whitespace")
            pass

    new_df = pd.concat(dflist, axis=0)
    new_df["basetime"] = pd.to_datetime(new_df["basetime"])
    new_df = new_df.set_index("basetime")
    return new_df

def beautydump(jsondict: dict, savepath: Path):
    """dumps a json at a path with indentation"""
    with open(savepath, "w") as f:
        json.dump(jsondict, f, indent=4)

def dump(jsondict: dict, savepath: Path):
    """dumps a json at a path without indentation"""
    with open(savepath, "w") as f:
        json.dump(jsondict, f)

# creator functions
def new_geojson() -> dict:
    """Return the structure of a geojson dictionary"""
    return {
        "type": "FeatureCollection",
        "features": []
    }

def new_feature(featuretype="MultiPoint", coordinates=None, properties=None) -> dict:
    """Returns the structure of a single Feature. Should be populated"""
    if coordinates is None: coordinates=[]
    if properties is None: properties={}
    return {
        "type": "Feature",
        "properties": properties,
        "geometry": {
            "type": featuretype,
            "coordinates": coordinates
        }
    }

# miscallaneous
def get_wd() -> Path:
    """Returns the working directory path. Hacky and not used"""
    return (Path("").absolute())

def clear():
    """Clears the console"""
    os.system("CLS")
    return


# classes
class Feature:
    """
    This class introduces an object-based approach to feature handling.
    Compatible with GeojsonObject.

    Author: Ben Kraas (https://github.com/KtRNofficial)
    """
    def __init__(self, featuretype: str="Point", coordinates: list=None, \
                 properties: dict=None, dictionary: dict=None):
        """constructor for the Feature - class"""
        if coordinates is None: coordinates=[] # solve mutable default args problem 
        if properties  is None: properties={}
        if dictionary  is None: dictionary={}
        
        if dictionary:
            self.dict = dictionary
        else:
            self.new(featuretype, coordinates, properties)
        self.update()

    def force(self, dictionary: dict):
        """Brute sets the entire feature dictionary"""
        self.dict = dictionary
        self.update()
    
    def new(self, featuretype: str="Point", coordinates: list=None, \
            properties: dict=None):
        """Creates the foundation of a new feature. Should be populated"""
        if coordinates is None: coordinates=[] # solve mutable default args problem
        if properties  is None: properties={}

        self.dict = {
            "type": "Feature",
            "properties": properties,
            "geometry": {
                "type": featuretype,
                "coordinates": coordinates
            }
        }
        self.update()

    # populate object with some attributes. Not necessary but QOL
    def update(self):
        """This method serves the purpose of populating the objects' attributes."""
        self.type = self.dict["geometry"]["type"]

    def get_coordinates(self) -> list:
        """Returns the Feature's coordinate list"""
        return self.dict["geometry"]["coordinates"]

    def get_coordinates_raw(self):
        """
        WIP!
        Supposed to crawl through coordinate lists regardless of Featuretype. Redundant, remove.
        """
        pass

    def add_vertex(self, coordinates: list):
        """
        Add a vertex to the coordinate list. 
        Currently only supports MultiPoints and Polygons
            
        WIP (full method beyond scope for this project)
        """
        ftype = self.dict["geometry"]["type"]
        if ftype == "MultiPoint": 
            self.dict["geometry"]["coordinates"].append(coordinates)
        elif ftype == "Polygon": 
            self.dict["geometry"]["coordinates"].insert(-2, coordinates)

    # self-altering generators
    def gen_randscatter(self, extent: list, number: int=10):
        """Generates a random scatter MultiPoint"""
        lon_E, lat_S, lon_W, lat_N = extent # unpack
        coordlist = []
        for x in range(number):
            randlon = random.uniform(lon_W, lon_E)
            randlat = random.uniform(lat_N, lat_S)
            coordlist.append([randlon, randlat])
        self.dict["geometry"]["coordinates"] = coordlist
    
    def gen_grid(self, extent: list, x_dist: float, y_dist: float):
        """Generate a normal point grid"""
        self.gen_grid_adv(extent, x_dist, y_dist, matrixname="full")
        
    def gen_grid_adv(self, extent: list, x_dist: float, y_dist: float, \
                     matrixname: str="full", matrix: list=None):
        """
        Generate a MultiPoint grid.
        Spacing can fully customized by providing a two-dimensional matrix with
        1/True and 0/False values which will draw/not draw a point respectively.

        Lists in matrix should all be of the same length.
        You can ignore this if you know what you are doing.
        e.g.: [[1], [1, 0], [0, 1, 1, 0]] instead of 
        [[1, 1, 1, 1], [1, 0, 1, 0], [0, 1, 1, 0]]
        
        Alternatively, a matrixname for the grid can be passed which builds on a number of
        prebuilt matrices
        
        Possible matrixnames are: full, checkerboard, big_checkerboard, sparse,
        sparse_alt, diagonal,raster
        """
        if matrix == None and matrixname:
            matrix = self.PRIVATE_resolve_matrix(matrixname)
        # funct start
        matlen = len(matrix)
        lon_E, lat_S, lon_W, lat_N = extent
        pointer_lon, pointer_lat = lon_W, lat_N
        counter_lon, counter_lat = 0, 0
        while pointer_lat >= lat_S:
            # reset lon pointer
            matline = matrix[(counter_lat%matlen)]
            counter_lon, pointer_lon = 0, lon_W
            while pointer_lon <= lon_E:
                # create point
                matnum = matline[(counter_lon % len(matrix[counter_lat%matlen]))]
                if matnum:
                    self.add_vertex([pointer_lon, pointer_lat])
                # increment lon
                counter_lon += 1
                pointer_lon += x_dist
            # decrement lat
            counter_lat += 1
            pointer_lat -= y_dist

    # offset methods. Return features by default
    def offset_circular(self, offset: float, offset_fixed: bool=False, inplace: bool=False) -> object:
        """
        Randomly offsets a MultiPoint feature classes points
        by any random value in a circle around the origin (offset == radius).
        Maximum distance is specified by the offset
        If offset_fixed is True, it will put the points on the circumference instead

        This scatter method does not scatter evenly - density will increase towards the center.
        If this is not desired, use self.offset_circular_even()
        """
        if not self.dict["geometry"]["type"] == "MultiPoint":
            raise ValueError("Method can only handle multipoint features for now")
        
        coord_collection = []
        for point in self.dict["geometry"]["coordinates"]:
            j, k = point # circle's origin

            if offset_fixed: vari = 1       # no variation towards circles' center
            else: vari = random.random()    # random variation ranging from 1 (none) to 0 (full)

            t = random.uniform(0, 360)
            x, y = self.PRIVATE_draw_circle(offset, t, j, k, inwards_variation=vari)
            coord_collection.append([x, y])
        
        if inplace:
            self.dict["geometry"]["coordinates"] = coord_collection
        else:
           return Feature("MultiPoint", coord_collection)

    def offset_circular_even(self, offset: float, inplace: bool=False) -> object:
        """
        Superiour scattering method. 
        Scattering is even across the entire circular area.

        For center-biased scattering, use self.offset_circular()
        """
        # code should scatter randomly on a square and then keep only the points inside a circle

        if not self.dict["geometry"]["type"] == "MultiPoint":
            raise ValueError("Method can only handle multipoint features for now")
        
        coord_collection = []
        for point in self.dict["geometry"]["coordinates"]:
            x_origin, y_origin = point # circle's origin

            while True:
                x_scatter = random.uniform((x_origin - offset), (x_origin + offset))
                y_scatter = random.uniform((y_origin - offset), (y_origin + offset))

                check_val = math.sqrt( pow((x_scatter-x_origin), 2) + pow((y_scatter-y_origin), 2) )

                if check_val <= offset:
                    coord_collection.append([x_scatter, y_scatter])
                    break
        
        if inplace:
            self.dict["geometry"]["coordinates"] = coord_collection
        else:
           return Feature("MultiPoint", coord_collection)

    # /// Private methods
    def PRIVATE_draw_circle(self, offset: float, radian: float, origin_x: float, \
                            origin_y: float, inwards_variation: float) -> list:
        """
        Draws a point on a circle's circumference around a point
        or (if inwards_variation > 0) within.
        Radian defines at how many degrees the point is placed
        """
        x = (offset*inwards_variation) * math.cos(radian) + origin_x
        y = (offset*inwards_variation) * math.sin(radian) + origin_y
        return [x, y]
    
    def PRIVATE_inside_circle():
        """Private function for checking if a value is inside a circle. WIP or not needed"""
        pass

    def PRIVATE_resolve_matrix(self, matrixname: str) -> list:
        """Private function. Provides example matrices to self.gen_grid_adv()"""
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
        elif matrixname == "diagonal":
            matrix = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
        elif matrixname == "raster":
            matrix = [[1], [1, 0, 0], [1, 0, 0]]
        elif matrixname == "heart": # easter egg
            matrix = [[0, 1, 0, 0, 0, 1, 0, 0], 
                      [1, 0, 1, 1, 1, 0, 1, 0], 
                      [1, 0, 0, 0, 0, 0, 1, 0], 
                      [0, 1, 0, 0, 0, 1, 0, 0], 
                      [0, 0, 1, 0, 1, 0, 0, 0], 
                      [0, 0, 0, 1, 0, 0, 0, 0], 
                      [0]] 
                      # you can tell I had fun here :)
                      # my girlfriend approves, though she`d move matrix[1][3] down by one
        else:
            raise ValueError("A correct matrix name or matrix must be provided")
        return matrix


class GeojsonObject:
    """
    This class introduces an object-based approach to geojson handling.
    Child objects on a per-feature basis could be implemented in the future. (WIP)

    Author: Ben Kraas (https://github.com/KtRNofficial)
    """

    def __init__(self, geojson: dict=None, name: str="default.geojson"):
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
        if geojson is None: geojson={} # solve mutable default args problem
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
        
    def force(self, dictionary: dict):
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
        Can accept the Feature object or a feature dict
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
    def dumpto(self, path: Path):
        with open(path, "w") as fp:
            # use indent=4 to make json more readable
            json.dump(self.dict, fp, indent=4)
        
    def dump(self, name: str=None):
        if name:
            newname = Path(name).absolute()
        else:
            newname = Path("edited_" + self.dict_path.name).absolute()
        self.dumpto(newname)

    # get feature information
    def get_name(self, id: int) -> str:
        """Returns a features name from ID"""
        return self.dict["features"][id]["properties"]["name"]

    def get_names(self) -> list:
        """Returns all feature names"""
        name_list = []
        for feature in self.dict["features"]:
            name_list.append(feature["properties"]["name"])
        return name_list

    def get_type(self, id: int) -> str:
        """Returns a features type from ID"""
        return self.dict["features"][id]["geometry"]["type"]

    def get_types(self) -> set:
        """Returns all feature types that occurr in the geojson"""
        type_set = set()
        for feature in self.dict["features"]:
            type_set.add(feature["geometry"]["type"])
        if not type_set:
            return False
        return type_set

    def get_all_same_type(self) -> bool:
        """Returns type if all features are of the same type and False if not"""
        types = self.get_types()
        if len(types) > 1:
            return False
        return True

    def get_feature(self, id: int) -> dict:
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
        """Returns a features' (id) single property by name"""
        if id is not None and property:
            return self.dict["features"][id]["properties"].get(property)
        
    def get_properties(self, id: int, skipwarn=True) -> dict:
        """
        Returns the properties dict for a feature
        skipwarn can be used for debugging
        """
        if id is not None:
            return self.dict["features"][id]["properties"]
        if not skipwarn:
            raise ValueError(f"Properties for ID {id} is not accessible")
    
    # querys/searches
    def query_name(self, searchname: str, casesensitive: bool=False) -> int:
        """
        Searches the geojson for a searchname. 
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

    def query_names(self, searchname: str) -> list:
        """
        Returns a list of all IDs with the searchname
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
        """Returns a list of all characteristic values of a certain propertyname"""
        propls = []
        for id in range(self.get_feature_count()):
            propls.append(self.get_property(id, propertyname))
        return propls

    # more advanced calculations (quite project specific)
    def calc_total(self, function) -> float: 
        """
        Calculate a total value by running the passed function for every feature 
        Currently supported functions are:
        calc_length_geod
        calc_circumference_geod

        Example use would be: 
        total_len = lineobj.calc_total(lineobj.calc_length_geod())
        This would run the .calc_length_geod function for each feature in lineobj
        """
        total = 0
        for id in range(self.get_feature_count()):
            total += function(id)
        return float(total)

    def calc_circumference_geod(self, id: int) -> float:
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
        return float(ft_length)

    def calc_length_geod(self, id: int) -> float:
        """
        Calculates the length (m) of a LineString
        Can only handle METRIC "coordinates" 

        A conversion method is currently not planned (out of scope)
        """
        # while it seems counterintuitive to have the same calculation take place
        # for both polygons and linestrings, it makes sense due to the way the dictionaries
        # are laid out
        return float(self.calc_circumference_geod(id))

    # type conversions
    def convert_to_multipoint(self, inplace: bool=False) -> dict:
        """
        This function converts all polygons in a geojson to a single MultiPoint feature
        Properties are NOT conserved (Merge could be implemented at some point)
        """
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

    def convert_to_multipoint_alt(self, inplace: bool=False) -> dict:
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

    # /// Private methods
    def PRIVATE_coordcrawler(self, *args):
        """PRIVATE. Crawls through a coords dict and returns all coords individually"""
        coords = []
        for elem in args:
            if isinstance(elem[0], list):
                for atom in elem:
                    coords.append(atom)
            else:
                coords.append(elem)
        return coords