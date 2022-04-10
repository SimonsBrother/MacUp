import macup.library.config as general

config = {'name': 'write test', 'source_dir': 'source dir goes here', 'target_dir': 'target dir here', 'regex_filters': [{'name': 'RegName', 'application': 'PATHS', 'item_type': 'DIRECTORY', 'whitelist': 'False', 'regex': 'test'}, {'name': 'dot underscore dot', 'application': 'FILENAMES', 'item_type': 'BOTH', 'whitelist': 'True', 'regex': '._.'}], 'keyword_filters': [{'name': 'kw filter!!', 'application': 'PATHS', 'item_type': 'FILES', 'whitelist': 'False', 'keyword': 'py'}], 'overwrite': True}

print(general.parseDictToConfig(config))
