from superdict.processes.query_finder import finder
from superdict.processes.utils import list_index
from superdict.traversal import recursive_find

# def search_by_keys(obj, list_of_keys, strict=False):
#     return_values = None
#
#     for key in list_of_keys:
#         locations_of_found = recursive_find(finder, obj, key_query=key, value_query=None)  # gets the keys
#
#         for loc in locations_of_found:
#             return_values.append(getter(obj, loc))
#
#     if



def getter(obj, list_of_keys):
    ret = obj
    for key in list_of_keys:
        ret = ret[key]
    return ret

dicta = {
    "b": {
        0: [1, 2, 3]},
    "a": "A"}
