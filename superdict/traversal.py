import typing
from collections import namedtuple

import superdict.process.query_finder

primitives = tuple([str, int, float, bool])
composites = tuple([dict, list, tuple, set, frozenset])

"""
Traversal should call a function for at each level of the dict, passing in all of the parameters as **kwargs. It should
also pass in itself (recursive find) as wel so that the function can make a call at the next level.

Could make the function a class and define an abstract base class/interface.

Other possible functions:
- Get only leafs / primitives
"""

iterator = namedtuple("iterator", ("obj_type", "data"))


def recursive_find(process_function, obj, key_query=None, value_query=None):
    # key only applies to a dict.
    # Lists have no explicit match function; they are always iterated through until a primitive or dict is reached

    matched_paths = []

    validate_query(key_query, value_query)

    assert isinstance(obj, composites)

    obj_type, data = iterate_composite(obj)

    for identifier, value in data:  # identifier is either key (for dict) or index (for list)
        found_paths = process_function(obj_type, identifier, value, key_query, value_query)
        matched_paths.extend(found_paths)

        # # if obj is a composite, also recurse
        if isinstance(value, composites):
            new_paths = recursive_find(process_function, value, key_query, value_query)
            updated_paths = list_path_join(identifier, new_paths)
            matched_paths.extend(updated_paths)

    # make each of the paths tuples to signify that they are to be considered as a single entity
    matched_paths = [tuple(path) for path in matched_paths]
    return matched_paths


def iterate_composite(composite):

    if isinstance(composite, dict):
        data = tuple(composite.items())
        obj_type = "dict"
    elif isinstance(composite, (list, tuple, set, frozenset)):
        data = tuple(enumerate(composite))
        obj_type = "list"
    else:
        raise ValueError("Composite must be a dict or list/tuple/set/frozenset")

    return iterator(obj_type=obj_type, data=data)


def validate_query(key_query=None, value_query=None):
    all_search_parameters = tuple([key_query, value_query])

    # Explicitly check None because False is a valid (non empty) query
    assert not all(search is None for search in
                   all_search_parameters), "No search parameters provided. Must provide search parameters for at least one of key_query or value_query"

    assert valid_non_function_query(
        key_query), 'Invalid key_query provided. Must be str, int, float or compiled regex pattern'
    assert valid_non_function_query(
        value_query), 'Invalid value_query provided. Must be str, int, float or compiled regex pattern'


def valid_non_function_query(query):
    valid_non_none = isinstance(query, (str, int, float, bool, typing.Pattern))
    return valid_non_none or (query is None)


def path_join(base, rest_of_path):
    full_path = list(rest_of_path)
    full_path.insert(0, base)
    return full_path


def list_path_join(base, list_rest_of_path):
    return [path_join(base, path) for path in list_rest_of_path]


dicta = {
    "b": {
        "b": [1,2,3]},
    "a": "A"}

print(recursive_find(superdict.process.query_finder.finder, dicta, "b"))
