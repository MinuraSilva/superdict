import re

# Only for reference
# This is the original code written for a scraping project.

def extract_val_re(obj, keys):
    """
    Input:
        obj: A python dict (also allows a list of lists - not sure if that is valid JSON)
        keys: Either string or compiled regex object or a list of strings and/or compiled regex objects

    If a single key is given, finds all instance of the key at any level of the JSON object and returns a list of these values.
    If a list of keys is given, applies the keys iteratively; i.e. first apply the first key to get result_1, then apply the second key on result_1 and so on.

    Output: A list of the values of those keys.
    """

    # helper to extract a single key
    def extract_single(obj, key):
        ret = []
        if isinstance(obj, dict):
            keys = obj.keys()
            for k in keys:
                # if key name matches, add to ret
                if re.search(key, k):
                    ret.append(obj[k])
                # if dict, recurse
                if isinstance(obj[k], dict):
                    ret.extend(extract_val_re(obj[k], key))
                elif isinstance(obj[k], list):
                    for li in obj[k]:
                        ret.extend(extract_val_re(li, key))
        elif isinstance(obj, list):
            for item in obj:
                ret.extend(extract_val_re(item, key))

        return ret

    # convert keys to regex if they are not already
    def convert_regex(single_or_list):

        # helper to convert a single key to regex
        def convert_single(str_or_regex):
            if isinstance(str_or_regex, str):
                return re.compile(f"^{str_or_regex}$")
            elif isinstance(str_or_regex, type(re.compile("compiled_object"))):
                # do nothing if already regex
                return str_or_regex
            else:
                assert False, "key is not either a string or a compiled regex object"

        # convert all keys to regex
        if isinstance(single_or_list, list):
            new_list = []
            for itm in single_or_list:
                new_list.append(convert_single(itm))
            return new_list
        else:
            return convert_single(single_or_list)

    # extract either a single key or a series of keys
    if not (isinstance(keys, list)):
        regex_key = convert_regex(keys)
        return extract_single(obj, regex_key)
    elif isinstance(keys, list):
        filtered = obj

        for key in keys:
            regex_key = convert_regex(key)
            filtered = extract_single(filtered, regex_key)
        return filtered

