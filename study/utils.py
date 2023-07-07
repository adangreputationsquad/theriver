import fnmatch


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
        return {str(i): remove_lists_from_json(item) for i, item in
                enumerate(json_data)}
    elif isinstance(json_data, dict):
        return {key: remove_lists_from_json(value) for key, value in
                json_data.items()}
    else:
        return json_data


def math_pattern_to_values(dictionary, pattern) -> dict:
    result = {}
    dictionary = flatten_dict(dictionary)
    for key in dictionary:
        if (key.startswith(pattern.split("*")[0])
                and key.endswith(pattern.split("*")[-1])):
            result[key] = dictionary[key]
    return result
