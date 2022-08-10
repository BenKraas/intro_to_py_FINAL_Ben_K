
# To read the `lakes.geojson` file use the following:
import json

with open("lakes.geojson", "r") as f:
    lakes = json.load(f)

# 1. What is the datatype of `lakes`?
type(lakes)
# => <class 'dict'>


# 2. How many items are in `lakes`?
len(lakes)
# => 3

# 3. How many items are in `features`?
len(lakes["features"])
# => 25


# 4. What is the datatype of `features`?
type(lakes["features"])
# => <class 'list'>

# 6. What is the datatype of the “name” property?
type(lakes["features"][0]["properties"]["name"])
# => <class 'str'>


# 7. What is the datatype of the “bbox” field?
type(lakes["bbox"])
# => <class 'list'>


# 8. What is the datatype of the “geometry” field?
type(lakes["features"][0]["geometry"])
# => <class 'dict'>


# 9. What is the datatype of the “coordinates” field?
type(lakes["features"][0]["geometry"]["coordinates"])
# => <class 'list'>