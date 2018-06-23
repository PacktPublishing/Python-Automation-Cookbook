def match_recursively(search_dict, field):
    """
    Walk through the dictionary finding keys that contains
    the string defined in field

    It will return a list of
    [(matched_key, value)...]
    """
    matching_fields = []

    # Iterate through the dictionary
    for key, value in search_dict.items():
        # This level matches
        if field in key:
            matching_fields.append((key, value))

        elif getattr(value, 'items', None):
            # Another dictionary, search recursively
            matching_fields.extend(match_recursively(value, field))

        elif isinstance(value, list):
            # A list, each of the elements needs to be analysed
            for item in value:
                matching_fields.extend(match_recursively(item, field))

    return matching_fields
