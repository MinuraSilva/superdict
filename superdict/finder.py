import re
import typing

def process_sub(obj_type, identifier, value, key_query=None, value_query=None):
    # return None or a list of paths for matches

    list_of_matched_paths = []

    # check at current level
    if compare(obj_type, identifier, value, key_query, value_query):
        list_of_matched_paths.append([identifier])

    return list_of_matched_paths


def compare(obj_type, identifier, value, key_query, value_query):


    def compare_single(search_against, query):
        """
        Return True if either there is nothing to search against or if the search matches.
        """
        if (search_against is None) or (query is None):
            return True  # simplifies logic so that I only have to check that compare_single is True for both key and value comparisons.
        else:
            return compare_query(search_against, query)

    value_match = compare_single(value, value_query)

    if (obj_type != "dict") and (key_query is not None):
        # if a key search parameter is given when searching in a list, there cannot be a match since the dict does not
        # have a key (the index is not considered a 'key').
        return False
    elif obj_type != "dict":
        # if obj_type is a list (or its variants), only need to check the value.
        return value_match
    else:
        # if obj_type is a dict, need to check both key and value.
        key_match = compare_single(identifier, key_query)
        return key_match and value_match


def compare_query(search_against, query):
    def compare_regex(search_against, query):
        return re.search(query, search_against)

    def compare_primitive(search_against, query):
        return query == search_against

    if isinstance(query, typing.Pattern):
        return compare_regex(search_against, query)
    else:
        return compare_primitive(search_against, query)


def list_path_join(base, list_rest_of_path):
    return [path_join(base, path) for path in list_rest_of_path]


def path_join(base, rest_of_path):
    full_path = list(rest_of_path)
    full_path.insert(0, base)
    return full_path