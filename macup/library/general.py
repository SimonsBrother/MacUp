import json
from macup.library.classes import Configuration


def loadConfigs(path):
    with open(path, "r") as f:
        json_configs = json.load(f)["configs"]
        configs = []
        for config in json_configs:
            configs.append(Configuration(config["name"], config["source_dir"], config["target_dir"],
                                         config["regex_filters"], config["keyword_filters"]))
    return configs
