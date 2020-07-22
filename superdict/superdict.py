
"""
# Core is a find method that returns the full path to the found values
# Then, we can use this to either 'get' the values or change them

main objects: flex_dict finder


"""

import copy

class flexdict(dict):

    find_locations = None  # a list of the locations that will be populated on doing a search
    locations_dict_version = None  # Updated with the current dict for anything that updates find_locations.
    # Then if find_locations is used in any method such as get_paths or replace, a comparison of the object in find_source
    # is done with the current dict to see if it has changed. If it has, then a warning is given that the paths in
    # find_locations may no longer be valid for the current state of the dictionary


    def __init__(self, *args, **kwargs):
        """
        Standard initialization for a python dict.
        """
        super(flexdict, self).__init__(*args, **kwargs)

    def search_by_key(self, query_or_match_function, strict_or_not):
        # return nothing; only populate the find_locations
        # query either string ot regex. match_function must return boolean.
        pass

    def search_by_value(self, query, pre_processor):
        # return nothing; only populate the find_locations
        pass

    def get_values(self):
        # return the values of all paths stored in the find_locations
        pass

    def get_paths(self):
        # return the paths stored in find_locations. Should be in the same format as that taken
        # by the query in search_by_key
        pass

    def replace(self, index_or_query):
        # if index is given, then must have find_locations populated. Will replace the path in find_locations
        # if query is given, will replace all matches at query. Can do a search_by_key/value first and then use
        # get_paths which can be used as the query.
        pass

    def replace_all(self):
        # replace all of the found locations in found_locations
        pass


    def __get_dict_deep_copy(self):
        """
        Get a deep copy of the plain python dict of the current flex-dict.
        :return: python dict
        """
        return copy(dict(self))

    def do_something(self):
        return self.do_otherthing()

    def do_otherthing(self):
        pass


class TraverseComponent:
    obj = None

    def __init__(self, obj):
        self.obj = obj

    def traverse(self, obj, match_str_query_func):
        """

        :param obj:
        :param match_str_query_func:
        :return: matches and list of next level objects to traverse
        """
        pass

class TraverseSingle(TraverseComponent):
    pass

class TraverseGroup(TraverseComponent):
    list_of_traverse = None # of type TraverseComponent
    pass

class TraverseObject:
    pass

class ListTraverse(TraverseObject):
    pass

class DictTraverse(TraverseObject):
    pass
