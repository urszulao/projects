import requests
import json

# Perform a GET request and fetch JSON data
response = requests.get("https://coderbyte.com/api/challenges/json/wizard-list")
data = response.json()

def clean_empty(value):

# Recursively remove all "" ("empty") values from dictionaries and lists, and returns
# the result as a new dictionary or list.

    if isinstance(value, list):
        return [clean_empty(x) for x in value if x != ""]
    elif isinstance(value, dict):
        return {
            key: clean_empty(val)
            for key, val in value.items()
            if val != ""
        }
    else:
        return value

def remove_empty_properties(obj):
    if isinstance(obj, dict):
        return {k: remove_empty_properties(v) for k, v in obj.items() if v not in [None, "Unknown", []]}
    elif isinstance(obj, list):
        return [remove_empty_properties(item) for item in obj]
    else:
        return obj


def remove_duplicate_objects_in_array(data, array_key):
    for item in data:
        if array_key in item and isinstance(item[array_key], list):
            seen_objects = set()
            new_array = []

            for obj in item[array_key]:
                # Convert the object to a JSON string to check for duplicates
                obj_json = json.dumps(obj, sort_keys=True)

                if obj_json not in seen_objects:
                    seen_objects.add(obj_json)
                    new_array.append(obj)

            item[array_key] = new_array

    return data


# Remove duplicate friends from the "friends" arrays
data = remove_duplicate_objects_in_array(data, "friends")
data = clean_empty(data)
data = remove_empty_properties(data)

# alphabetical sort of the object keys, case-insensitive with perserved original data structure 
json_object = json.dumps(data, indent = 8, sort_keys = True)
print(json_object)

