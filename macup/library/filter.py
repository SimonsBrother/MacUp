"""

"""

from macup.library.constants import *

import os
import re


def applyFilters(filters, path):
    """
    Checks whether a certain path satisfies all the filters provided.

    :param filters: List of filters to be applied
    :param path: A path for the filters to be applied on
    :return: True if the node path satisfies each filter, False otherwise
    """

    def handleFilter(filter_, path_):
        """
        Handles the logic of the filter and applies it to the item path provided.

        :param filter_: A filter object
        :param path_: The path to be analysed
        :return: Whether this item should be copied according to the filter
        """

        # Decide whether to apply the filter to the filename or the full path
        if filter_.application == FILENAMES:
            str_to_use = os.path.basename(path_)
        else:
            str_to_use = path_

        # Decide whether the filter should be applied to the item according to whether it is a file or directory
        if (filter_.item_type != FILES and os.path.isdir(path_)) \
                or (filter_.item_type != DIRECTORY and os.path.isfile(path_)):
            # The filter applies to directories and the item is a dir OR
            # the filter applies to files and the item is a file OR the filter checks both:

            # If the item matches the filter and a whitelist is used, the result is true; the item should be copied
            # If the item doesn't match the filter and a blacklist is used, the result is also true, so copy
            # Else, the item should not be copied.
            # In other words, if the result is equal to the whitelist state, copy the item.
            # Whitelist allows items that match the filter, and blacklist allow items that don't match the filter.

            # Different filter logic here
            if filter_.filter_type == REGEX:
                # Regex filter
                match = bool(re.match(filter_.data, str_to_use))
                result = match is filter_.whitelist  # Apply whitelist
            else:  # Type must be KEYWORD
                # Keyword filter
                kw_in_str = filter_.data in str_to_use
                result = kw_in_str is filter_.whitelist  # Apply whitelist
        else:
            # The regex does not apply to this item
            result = True

        return result

    results = []
    for f in filters:
        results.append(handleFilter(f, path))

    return all(results)


def buildFilter(filters):
    """
    Builds the filter function to be passed to the FileTree constructors;
     the filter function has to have one parameter.

    :param filters: List of filters
    :return: The filter function, which takes one argument, suitable for the FileTree constructor
    """

    def filter_(path):
        return applyFilters(filters, path)

    return filter_


# todo untested
def parseFilterToDict(filter_):
    return {
        "name": str(filter_.name),
        "filter_type": str(filter_.filter_type),
        "data": str(filter_.data),
        "application": str(filter_.application),
        "item_type": str(filter_.item_type),
        "whitelist": bool(filter_.whitelist)
    }


# todo untested
def parseDictToFilter(dict_):
    from macup.library.classes import Filter
    return Filter(name=dict_["name"],
                  filter_type=dict_["filter_type"],
                  data=dict_["data"],
                  application=dict_["application"],
                  item_type=dict_["item_type"],
                  whitelist=dict_["whitelist"])
