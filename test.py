import fnmatch


def get_matching_elements(dictionary, pattern):
    matches = {}

    # Split the pattern into segments
    segments = pattern.split('/')

    # Iterate over the dictionary to find matching elements
    for key, value in dictionary.items():
        if fnmatch.fnmatch(key, segments[0]):
            if len(segments) > 1 and isinstance(value, dict):
                # Recursively search for matching elements in nested dictionaries
                submatches = get_matching_elements(value, '/'.join(segments[1:]))
                if submatches:
                    matches[key] = submatches
            else:
                matches[key] = value

    return matches

a = {
    "key_1": {
        "day_1": {
            "item_1": 1,
            "item_2": 2
        },
        "day_2": {
            "item_1": 3,
            "item_2": 4
        }
    },
    "key_2": {
        "day_1": {
            "item_1": 5,
            "item_2": 6
        },
        "day_2": {
            "item_1": 7,
            "item_2": 8
        }
    }
}

if __name__ == '__main__':
    pattern = "key_1/day_*/item_2"
    matching_elements = get_matching_elements(a, pattern)

    print(matching_elements)
