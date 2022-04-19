"""

"""

from macup.library.constants import *

import os
import re


def applyFilter(regex_filters, keyword_filters, path):
    """
    Checks whether a certain path satisfies all the regular expressions provided.

    :param keyword_filters: An iterable container containing keywordFilters to be applied
    :param regex_filters: An iterable container containing RegexFilters to be applied
    :param path: A path for the filters to be applied on
    :return: True if the node path satisfies each filter, False otherwise
    """

    def handleFilter(filter_, type_, path_):
        """
        Handles the logic of the filter and applies it to the item path provided.

        :param filter_: The filter object, either RegexFilter or KeywordFilter
        :param type_: The type of filter applied, either REGEX or KEYWORD
        :param path_: The path to be analysed
        :return: Whether this item should be copied according to the filter
        """
        # Validate type
        if type_ not in [REGEX, KEYWORD]:
            raise ValueError(f"type_ must be either {REGEX} or {KEYWORD}, got {type_}")

        # Decide whether to apply the filter to the filename or the full path
        if filter_.application == FILENAMES:
            str_to_use = os.path.basename(path_)
        else:
            str_to_use = path_

        # Decide whether the filter should be applied to the item according to whether it is a file or directory
        if (filter_.item_type != FILES and os.path.isdir(path_)) \
                or (filter_.item_type != DIRECTORY and os.path.isfile(path_)):
            # The filter applies to directories and the item is a dir OR
            #   the filter applies to files and the item is a file:

            # If the match is true and a whitelist is used, the result is true, or if the match is false and a
            # blacklist is used, the result is true; whitelist allows items that match it through, and blacklist allows
            # items that don't match it through.
            if type_ == REGEX:
                match = bool(re.match(filter_.data, str_to_use))
                result = match is filter_.whitelist
            else:  # Type must be KEYWORD
                kw_in_str = filter_.data in str_to_use
                result = kw_in_str is filter_.whitelist
        else:
            # The regex does not apply to this item
            result = True

        return result

    results = []
    for regex_filter in regex_filters:
        results.append(handleFilter(regex_filter, REGEX, path))

    for keyword_filter in keyword_filters:
        results.append(handleFilter(keyword_filter, KEYWORD, path))

    return all(results)


def buildFilter(regex_filters, keyword_filters):
    """
    Builds the filter function to be passed to the FileTree constructors;
     the filter function has to have one parameter.

    :param regex_filters: Iterable container of RegexFilters
    :param keyword_filters: Iterable container of KeywordFilters
    :return: The filter function, which takes one argument, suitable for the FileTree constructor
    """

    def filter_(path):
        return applyFilter(regex_filters, keyword_filters, path)

    return filter_
