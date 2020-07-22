import re
import typing

primitives = tuple([str, int, float, bool])
composites = tuple([dict, list, tuple, set, frozenset])

"""
Traversal should call a function for at each level of the dict, passing in all of the parameters as **kwargs. It should
also pass in itself (recursive find) as wel so that the function can make a call at the next level.

Could make the function a class and define an abstract base class/interface.


Other possible functions:
- Get only leafs / primitives
"""


def recursive_find(obj, key_query=None, value_query=None):
    # key only applies to a dict.
    # Lists have no explicit match function; they are always iterated through until a primitive or dict is reached

    matched_paths = []

    validate_query(key_query, value_query)

    if isinstance(obj, dict):
        for key in obj.keys():
            value = obj[key]

            found_paths = process_sub(key, None, value, key_query, value_query)
            matched_paths.extend(found_paths)

    elif isinstance(obj, (list, tuple, set, frozenset)):
        for items in enumerate(obj):
            index = items[0]
            value = items[1]

            found_paths = process_sub(None, index, value, key_query, value_query)
            matched_paths.extend(found_paths)

    # make each of the paths tuples to signify that they are to be considered as a single entity
    matched_paths = [tuple(path) for path in matched_paths]
    return matched_paths


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


def process_sub(key=None, index=None, value=None, key_query=None, value_query=None):
    # return None or a list of paths for matches

    list_of_matched_paths = []

    if key is not None:
        curr_path = key
    else:
        curr_path = index

    # check at current level
    if compare(key, value, key_query, value_query):
        list_of_matched_paths.append([curr_path])

    # if obj is a composite, also recurse
    if isinstance(value, composites):
        new_paths = recursive_find(value, key_query, value_query)
        updated_paths = list_path_join(curr_path, new_paths)
        list_of_matched_paths.extend(updated_paths)

    # if isinstance(value, primitives):
    #     if compare(key, value, key_query, value_query):
    #         list_of_matched_paths.append(curr_path)
    #
    # elif isinstance(value, composites):
    #     new_paths = recursive_find(value, key_query, value_query)
    #     updated_paths = list_path_join(curr_path, new_paths)
    #     list_of_matched_paths.extend(updated_paths)

    return list_of_matched_paths


def compare_query(search_against, query):
    def compare_regex(search_against, query):
        return re.search(query, search_against)

    def compare_primitive(search_against, query):
        return query == search_against

    if isinstance(query, typing.Pattern):
        return compare_regex(search_against, query)
    else:
        return compare_primitive(search_against, query)


def compare(key=None, value=None, key_query=None, value_query=None):
    def compare_single(search_against, query):
        """
        Return True if either there is nothing to search against or if the search matches.
        """
        if (search_against is None) or (query is None):
            return True  # simplifies logic so that I only have to check that compare_single is True for both key and value comparisons.
        else:
            return compare_query(search_against, query)

    key_match = compare_single(key, key_query)
    value_match = compare_single(value, value_query)

    return (key_match and value_match)


def list_path_join(base, list_rest_of_path):
    return [path_join(base, path) for path in list_rest_of_path]


def path_join(base, rest_of_path):
    full_path = list(rest_of_path)
    full_path.insert(0, base)
    return full_path


dicta = {
    "b": {
        "b": [1,2,3]},
    "a": "A"}

print(recursive_find(dicta, None, 2))
