import json
from macup.library.classes import Configuration


TEST_LOC = "/Users/calebhair/Documents/Projects/MacUp/macup/tests/jsonstorage.json"


def loadConfigs(json_path):
    """
    Extracts configurations stored in a json file, returning a list of config objects.

    :param json_path: The path to the json file
    :return: List of configuration objects
    """

    with open(json_path, "r") as f:
        json_configs = json.load(f)["configs"]
        configs = []
        for config in json_configs:
            configs.append(Configuration(config["name"], config["source_dir"], config["target_dir"],
                                         config["filters"], config["overwrite"]))
    return configs


# todo make test
def loadConfig(name, json_path):
    """ Searches through available configs, returns the one with a matching name as a config object"""

    cfgs = loadConfigs(json_path)
    for cfg in cfgs:
        if cfg.name == name:
            return cfg


def parseConfigToDict(config):
    """
    Convert a Configuration object to a dictionary that can be written to json files.

    :param config: A Configuration object
    :return: A dictionary, suitable for json storage
    """

    if not isinstance(config, Configuration):
        raise ValueError(f"Configuration must be a Configuration object, got {type(config)}")

    # Parse each filter
    filter_dicts = []
    for filter_ in config.filters:
        filter_dict = {
            "name": str(filter_.name),
            "filter_type": str(filter_.filter_type),
            "data": str(filter_.data),
            "application": str(filter_.application),
            "item_type": str(filter_.item_type),
            "whitelist": bool(filter_.whitelist)
        }
        filter_dicts.append(filter_dict)

    # Build configuration dict
    config_dict = {
        "name": str(config.name),
        "source_dir": str(config.source_dir),
        "target_dir": str(config.target_dir),
        "filters": filter_dicts,
        "overwrite": bool(config.overwrite)
    }

    return config_dict


def parseDictToConfig(dict_):
    """
    Parse a configuration dictionary from a json file into a Configuration object.

    :param dict_: A dict representing a configuration
    :return: Configuration object
    """

    if not isinstance(dict_, dict):
        raise ValueError(f"Configuration must be a dict, got {type(dict_)}")

    return Configuration(dict_["name"], dict_["source_dir"], dict_["target_dir"],
                         dict_["filters"], dict_["overwrite"])


def saveConfig(config, json_path):
    """
    Save the configuration supplied, to the json file path; if a configuration with the same name exists,
    it will be overwritten. Handles converting between objects and dictionaries.

    :param config: A config dictionary or object
    :param json_path: The json file path
    """

    if not isinstance(config, (dict, Configuration)):
        raise TypeError(f"Must be either dict or Configuration object, not {type(config)}")

    # Convert to dict
    if isinstance(config, Configuration):
        config = parseConfigToDict(config)

    f = open(json_path, "r")
    json_file = json.load(f)
    f.close()

    # Iterate through existing configs, replace config with same name if it exists
    overwritten = False  # if the config already exists, it will need to be overwritten instead of appended
    for i, json_config in enumerate(json_file["configs"]):
        if config["name"] == json_config["name"]:  # if name of new config = name of config in json file
            json_file["configs"][i] = config  # overwrite config
            overwritten = True
            break

    if not overwritten:  # Config with that name didn't exist, so wasn't overwritten, so make it exist!
        json_file["configs"].append(config)

    f = open(json_path, "w")
    json.dump(json_file, f, indent=4)
    f.close()


def saveNewBlankConfig(name, json_path):
    """Saves an almost blank configuration with just the name filled"""
    saveConfig(parseConfigToDict(Configuration(name, "", "", [], False)), json_path)

# todo: make test (already tested in ui)
def checkNameExists(name, json_path):
    """ Returns true if the name provided is already used in a configuration file """

    for cfg in loadConfigs(json_path):
        if name == cfg.name:
            return True

    return False


def deleteConfig(name, json_path):
    """ Deletes the config from the json file """

    f = open(json_path, "r")
    json_file = json.load(f)
    f.close()

    for i, config in enumerate(json_file["configs"]):
        if config["name"] == name:
            json_file["configs"].pop(i)

            f = open(json_path, "w")
            json.dump(json_file, f, indent=4)
            f.close()
            return True

    return False
