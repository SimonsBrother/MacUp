import json
from macup.library.classes import Configuration


TEST_LOC = "/Users/calebhair/Documents/Projects/MacUp/macup/tests/jsonstorage.json"


def loadConfigs(json_path):
    """
    Extracts configurations stored in a json file.

    :param json_path: The path to the json file
    :return: Configuration objects
    """

    with open(json_path, "r") as f:
        json_configs = json.load(f)["configs"]
        configs = []
        for config in json_configs:
            configs.append(Configuration(config["name"], config["source_dir"], config["target_dir"],
                                         config["regex_filters"], config["keyword_filters"]))
    return configs


def parseConfigToDict(config):
    """
    Convert a Configuration object to a dictionary that can be written to json files.

    :param config: A Configuration object
    :return: A dictionary, suitable for json storage
    """

    # todo: could be made less redundant (package filters to work with one for loop)

    # Parse each regex filter in each config
    regex_filters_dict = []
    for regex_filter in config.regex_filters:
        json_regex_filter = {
            "name": str(regex_filter.name),
            "application": str(regex_filter.application),
            "item_type": str(regex_filter.item_type),
            "whitelist": str(regex_filter.whitelist),
            "regex": str(regex_filter.regex)
        }
        regex_filters_dict.append(json_regex_filter)

    # Parse each keyword filter in each config
    kw_filters_dict = []
    for kw_filter in config.keyword_filters:
        json_kw_filter = {
            "name": str(kw_filter.name),
            "application": str(kw_filter.application),
            "item_type": str(kw_filter.item_type),
            "whitelist": str(kw_filter.whitelist),
            "keyword": str(kw_filter.keyword)
        }
        kw_filters_dict.append(json_kw_filter)

    # Build configuration dict
    config_dict = {
        "name": str(config.name),
        "source_dir": str(config.source_dir),
        "target_dir": str(config.target_dir),
        "regex_filters": regex_filters_dict,
        "keyword_filters": kw_filters_dict
    }

    return config_dict


def parseDictToConfig(dict_):
    """
    Parse a configuration dictionary from a json file into a Configuration object.

    :param dict_: A dict representing a configuration
    :return: Configuration object
    """

    return Configuration(dict_["name"], dict_["source_dir"], dict_["target_dir"],
                         dict_["regex_filters"], dict_["keyword_filters"])


def saveConfig(json_path, config):
    """
    Save the configuration dictionary supplied, to the json file path; if a configuration with the same name exists,
    it will be overwritten.

    :param json_path: The json file path
    :param config: A config dictionary
    """

    f = open(json_path, "r")
    json_file = json.load(f)
    f.close()

    # Iterate through existing configs, replace config with same name if it exists
    overwritten = False  # if the config already exists, it will need to be overwritten instead of appended
    for i, json_config in enumerate(json_file["configs"]):
        if config["name"] == json_config["name"]:  # if name of config in json file = name of new config
            json_file["configs"][i] = config  # overwrite config
            overwritten = True
            break

    if not overwritten:
        json_file["configs"].append(config)

    f = open(json_path, "w")
    json.dump(json_file, f, indent=4)
    f.close()
