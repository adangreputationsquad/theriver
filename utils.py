import fnmatch
from typing import Any


def _get_matching_elements(dictionary, pattern):
    matches = {}

    # Split the pattern into segments
    segments = pattern.split('/')

    # Iterate over the dictionary to find matching elements
    for key, value in dictionary.items():
        if fnmatch.fnmatch(key, segments[0]):
            if len(segments) > 1 and isinstance(value, dict):
                # Recursively search for matching elements in nested dictionaries
                submatches = _get_matching_elements(
                    value, '/'.join(segments[1:])
                    )
                if submatches:
                    matches[key] = submatches
            else:
                matches[key] = value

    return matches


def get_matching_elements(dictionary, pattern):
    return flatten_dict(_get_matching_elements(dictionary, pattern))


def flatten_dict(dictionary, prefix=''):
    flattened_dict = {}
    for key, value in dictionary.items():
        current_key = f"{prefix}/{key}" if prefix else key
        if isinstance(value, dict):
            flattened_dict.update(flatten_dict(value, prefix=current_key))
        else:
            flattened_dict[current_key] = value
    return flattened_dict


def remove_lists_from_json(json_data):
    if isinstance(json_data, list):
        return {str(i): remove_lists_from_json(item) for i, item in enumerate(json_data)}
    elif isinstance(json_data, dict):
        return {key: remove_lists_from_json(value) for key, value in json_data.items()}
    else:
        return json_data
