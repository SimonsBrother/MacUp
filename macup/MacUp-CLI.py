import os
import macup.library.classes as cls
import macup.library.backup as bk


def getDirectory(prompt):
    directory = None
    while directory is None or not os.path.isdir(directory):
        directory = input(prompt)

    return directory


def getOption(prompt):
    option = None
    while option != 'y' and option != 'n':
        option = input(prompt)

    return option


def getFilters(prompt, error_prompt, accepted_prompt, split_value, filtertype):
    filters = []
    input_ = None
    error = False
    while input_ != "exit":
        if input_ is None:
            input_ = input(prompt)
        elif error:
            input_ = input(error_prompt)
        else:
            input_ = input(accepted_prompt)

        split_input = input_.split(split_value)
        if len(split_input) != 5:
            error = True
        else:
            try:
                si = split_input  # simply exists to make the next line shorter
                filters.append(filtertype(si[0], si[1], si[2], si[3], si[4]))
                print(filters)
                error = False
            except ValueError:
                error = True

    return filters


source_dir = getDirectory("Input source directory: ")
target_dir = getDirectory("Input target directory: ")
overwrite = getOption("Overwrite files? (y/n): ")
# BROKEN - MIGHT FIX LATER
"""regex_filters = getFilters("Input regex filters, type exit to quit; usage-  Regex : Application['FILENAMES'/'PATHS'] : "
                           "Type['FILES'/'DIRECTORY'/'BOTH'] : Whitelist[True/False] : Name\nInput: ",
                           "Invalid regex filter: ", "Regex filter accepted: ", ':', cls.RegexFilter)

keyword_filters = getFilters(
    "Input keyword filters, type exit to quit; usage-  Keyword : Application['FILENAMES'/'PATHS'] : "
    "Type['FILES'/'DIRECTORY'/'BOTH'] : Whitelist[True/False] : Name\nInput: ",
    "Invalid keyword filter: ", "Keyword filter accepted: ", ':', cls.KeywordFilter)


bk.backup(source_dir, target_dir, regex_filters, keyword_filters, overwrite)"""
