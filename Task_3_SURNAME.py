# -*- coding: utf-8 -*-
"""
Introduction to Programming and Applied Statistics

======================
Final Project - TASK 3
======================

Define a function that uses the thresholds shown in `lcz_thresholds.png`
to classify a weather station to a Local Climate Zone (LCZ).

More information about LCZ can be found here: https://doi.org/10.1175/BAMS-D-11-00019.1

The function should take as input arguments the following variables:

- the sky view factor,
- the aspect ratio
- the building surface fraction,
- the impervious surface fraction,
- the pervious surface fraction,
- the height of roughness elements
- the terrain roughness

Your function should also check if the input values are valid!
For instance, that the fraction values are between 0 and 100!

The function should return two outputs:

- the LCZ code
- the LCZ name

Test your code with the following values

•	sky view factor: 0.4
•	aspect ratio: 0.90
•	building surface fraction: 50
•	impervious surface fraction: 40
•	pervious surface fraction: 25
•	height of roughness elements: 6
•	the terrain roughness class: 6

"""

import json
import pandas as pd
from os.path import exists


def convert_to_lcz(*args, **kwargs) -> list:
    """
    This functions calculates the LCZ (Local climate zone) given 7 parameters.

    Returns: (LCZ_code, LCZ_name)

    Accepted parameters are (in order):
    sky_view_f  : sky view factor
    aspect_r    : aspect ratio
    build_srf   : building surface fraction
    imperv_srf  : impervious surface fraction
    perv_srf    : pervious surface fraction
    hgt_rough   : height of roughness elements
    terr_rough  : terrain roughness

    Alternatively, you can pass ALL these values as key-value pairs (kwargs)
    You must however EITHER pass all as args OR as kwargs. No mixing ;)

    If a parameter is not given, the calculation can not take place 

    Author: Ben Kraas (https://github.com/KtRNofficial)
    """

    # nested functions
    def import_lcz_data() -> object:
        """
        Private function specific to convert_to_lcz()

        Imports/creates the lcz key data used to classify the lczs.
        Returns the data as a pandas DataFrame.

        The DataFrame is NOT zero-indexed! 
        It is instead a 1-based index
        This makes it much easier not to confuse the index with the LCZ codes!
        """

        if not exists('LCZ_key_data.json'):
            print("JSON created!")
            dump_data_json()
        
        with open('LCZ_key_data.json') as json_file:
            data = json.load(json_file)

        dataf = pd.DataFrame(data)
        dataf.set_index("code", inplace=True)

        return dataf

    def import_args(args: tuple, kwargs: dict) -> dict:
        """
        Private function specific to convert_to_lcz()

        This function correctly imports all the args and kwargs for 
        convert_to_lcz()
        """
        config_dict = {}
        config_dict_n = ["sky_view_f", "aspect_r", "build_srf", "imperv_srf", \
                            "perv_srf", "hgt_rough", "terr_rough"]

        # check if the correct number of parameters are given
        if len(args) != 7 and len(kwargs) != 7:
            raise ValueError("convert_to_lcz(): \
                Not the correct amout of numbers given")
        elif len(args) > 0 and len(kwargs) > 0:
            raise ValueError("convert_to_lcz(): \
                You can only provide either args or kwargs!")
        
        # if args are given
        if args and isinstance(args, tuple) and (len(args) == len(config_dict_n)):
            for arg, name in zip(args, config_dict_n):
                config_dict[name] = arg

        # if kwargs are given
        else:
            if all(name in kwargs.keys() for name in config_dict_n):
                config_dict = kwargs
            else:
                raise ValueError("convert_to_lcz(): \
                    Not all keys correspond to the required name! \
                    Check your spelling of kwargs ;) ")

        return config_dict

    def dump_data_json():
        """
        Private function specific to convert_to_lcz()

        Call this function to create the LCZ_key_data.json used in the function.
        Automatically called by convert_to_lcz() if json does not exist
        
        Source: Task_3_LCZ_Thresholds.png
        """

        idx_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        nam_list = ["Compact high-rise", "Compact midrise", "Compact low-rise", \
                    "Open high-rise", "Open midrise", "Open low-rise", \
                    "Lightweight low-rise", "Large low-rise", "Sparsely built"]
        svf_list = [[0.2, 0.4], [0.3, 0.6], [0.2, 0.6], [0.5, 0.7], \
                    [0.5, 0.8], [0.6, 0.9], [0.2, 0.5], [0.7, 999], [0.8, 999]]
        apr_list = [[2.00, 999], [0.75, 2.00], [0.75, 1.50],[0.75, 1.25], \
                    [0.30, 0.75], [0.30, 0.75], [1.00, 2.00],[0.10, 0.30],\
                    [0.10, 0.25]]
        bsf_list = [[40, 60], [40, 70], [40, 70], [20, 40], \
                    [20, 40], [20, 40], [60, 90], [30, 50], [10, 20]]
        isf_list = [[40, 60], [30, 50], [10, 50], [30, 40], \
                    [30, 50], [20, 50], [00, 20], [40, 50], [00, 20]]
        psf_list = [[00, 10], [00, 20], [00, 30], [30, 40], \
                    [20, 40], [30, 60], [00, 30], [00, 20], [60, 80]]
        hre_list = [[25, 999], [10, 25], [3, 10], [25, 999],\
                    [10, 25], [3, 10], [2, 4], [3, 10], [3, 10]]
        trc_list = [[8, 8], [6, 7], [6, 6], [7, 8], \
                    [5, 6], [5, 6], [4, 5], [5, 5], [5, 6]]
        
        LCZ_tresholds = {"code": idx_list,
                        "name": nam_list,
                        "sky_view_factor": svf_list,
                        "aspect_ratio": apr_list,
                        "building_surf_fract": bsf_list,
                        "impervious_surf_fract":isf_list,
                        "pervious_surf_fract":  psf_list,
                        "height_of_rough_elem": hre_list,
                        "terrain_rough_class":  trc_list
                        }

        with open("LCZ_key_data.json", "w") as fp:
            json.dump(LCZ_tresholds , fp) # use indent=4 to make json more readable

    def between(number: any, range_list: list) -> list:
        """Checks if a number is between two values"""
        if range_list[0] <= range_list[1]:
            return range_list[0] <= number <= range_list[1]
        else:
            raise ValueError("First value in range_list must be smaller \
                              than second value!")

    def comb(keys, param_row):
        """
        Goes through the data and returns a DataFrames full of booleans.

        A cell is set to 1 if it lies between the keys' required values

        A cell is det to 0 if it doesn't.
        """

        param_row_list = list(param_row.keys())

        # we need to add an arbitrary non-numeric value here ("x"). 
        # since we don't know "name", we cannot check whether evaluates to true
        # if we give "name" a string, it will skip this column in the for-loops
        param_row_list.insert(0, "x")

        finaldf = keys
        for row in keys.index:
            for col, key in zip(keys.columns, param_row_list):
                if not key == "x":
                    value = param_row[key]
                    range = keys.loc[row,col]
                    is_between = between(value, range)
                    # if the value lies between the range values, it's set to 1
                    if is_between:
                        final_val = 1
                    else:
                        final_val = 0
                    finaldf.loc[row,col] = final_val
        return finaldf

    # preparation of keys data 
    # this table will be used to determine whether a number is within a range
    LCZ_key = import_lcz_data()
    numeric_cols = list(LCZ_key.columns)[1:]
    
    # importing of args/kwargs
    # these are specifications which you want to check
    config_dict = import_args(args, kwargs)

    # return dataframe with number in range or not (1=in range, 0=not in range)
    comb_bool = comb(LCZ_key, config_dict)

    # calculate the mean for each row, but only for numeric columns
    means = pd.DataFrame(comb_bool[numeric_cols].mean(axis=1))

    if 1 in means[0].unique():
        LCZ_row = int(means[means[0] == 1].index[0])
        return (LCZ_row, LCZ_key["name"].iloc[2])
    

if __name__ == "__main__":
    convert_to_lcz(sky_view_f=0.4, aspect_r=0.90, build_srf=50, \
                   imperv_srf=40, perv_srf=25, hgt_rough=6, terr_rough=6)