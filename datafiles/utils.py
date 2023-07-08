
def flatten_dict(dictionary: dict, prefix: str = ''):
    """
    Flatten a dictionary
    :param dictionary: dictionary
    :param prefix: prefix
    :return: flattened dictionary

    :example:
        >>> flatten_dict({'a': 1, 'b': {'c': 2}})
        >>> {'a': 1, 'b/c': 2}
    """
    flattened_dict = {}
    for key, value in dictionary.items():
        current_key = f"{prefix}/{key}" if prefix else key
        if isinstance(value, dict):
            flattened_dict.update(flatten_dict(value, prefix=current_key))
        else:
            flattened_dict[current_key] = value
    return flattened_dict


def transform_lists_in_dict(dictionary: dict):
    """
    Transforms lists inside a dictionary into a dictionary
    :param dictionary: dictionary with lists in it
    :return: dictionary with no list in it

    :example:
        >>> transform_lists_in_dict({"a":[{"i":1, "j":2}, {"k":1, "l":2}])
        >>> {"a":{"0":{"i":1, "j":2}, "1":{"k":1, "l":2}}}
    """
    if isinstance(dictionary, list):
        return {str(i): transform_lists_in_dict(item) for i, item in
                enumerate(dictionary)}
    elif isinstance(dictionary, dict):
        return {key: transform_lists_in_dict(value) for key, value in
                dictionary.items()}
    else:
        return dictionary


def match_pattern_to_values(dictionary: dict, pattern: str) -> dict:
    """
    Matches a pattern to non nested dictionary keys and gets values with keys
    matching th pattern, this does not use regex implementation, just '*' as
    a wildcard
    :param dictionary: dictionary
    :param pattern: string containing a * wildcard
    :return: dictionary with keys matching the pattern
    """
    result = {}
    dictionary = flatten_dict(dictionary)
    for key in dictionary:
        if (key.startswith(pattern.split("*")[0])
                and key.endswith(pattern.split("*")[-1])):
            result[key] = dictionary[key]
    return result
