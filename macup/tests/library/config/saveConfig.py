import macup.library.config as general
import macup.library.classes as cls

regex_filters = [{'name': 'RegName', 'application': 'PATHS', 'item_type': 'DIRECTORY', 'whitelist': 'False', 'regex': 'test'}, {'name': 'dot underscore dot', 'application': 'FILENAMES', 'item_type': 'BOTH', 'whitelist': 'True', 'regex': '._.'}]
kw_filters = [{'name': 'kw filter!!', 'application': 'PATHS', 'item_type': 'FILES', 'whitelist': 'False', 'keyword': 'py'}]

cfg = cls.Configuration("write test", "source dir goes here", "target dir here", regex_filters, kw_filters, False)

print(general.saveConfig(general.TEST_LOC, general.parseConfigToDict(cfg)))
