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
    This functions calculates the LCZ (Local climate zone) given 7 parameters

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

    If a number is not given, the calculation will not take place 
    and the funtion will raise a ValueError

    Otherwise, the returned list will contain:
    [LCZ_code, LCZ_name]

    Author: Ben Kraas (https://github.com/KtRNofficial)
    """

    # nested functions
    def import_args(args: tuple, kwargs: dict) -> dict:
        """
        This function correctly imports all the args and kwargs for 
        convert_to_lcz()

        Author: Ben Kraas (https://github.com/KtRNofficial)
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
        elif len(kwargs) == len(config_dict_n):
            if all(name in kwargs.keys() for name in config_dict_n):
                config_dict = kwargs
            else:
                raise ValueError("convert_to_lcz(): \
                    Not all keys correspond to the required name! \
                    Check your spelling of the kwargs ;) ")

    # preparation
    if not exists('LCZ_key_data.json'):
        dump_data_json()
    
    with open('LCZ_key_data.json') as json_file:
        data = json.load(json_file)

    LCZ_data = pd.DataFrame(data)

    # importing of kwargs
    config_dict = import_args(args, kwargs)
    print(config_dict)

    # function body


    
    return config_dict

def dump_data_json():
    """
    Call this function to create the LCZ_key_data.json used in the function.
    Automatically called by convert_to_lcz() if json does not exist
    
    Source: Task_3_LCZ_Thresholds.png

    Author: Ben Kraas (https://github.com/KtRNofficial)
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
    
if __name__ == "__main__":
    convert_to_lcz(sky_view_f=1, aspect_r=1, build_srf=1, imperv_srf=1, perv_srf=1, hgt_rough=1, terr_rough=1)