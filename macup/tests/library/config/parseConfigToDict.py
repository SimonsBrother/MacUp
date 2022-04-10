import macup.library.config as general
import macup.library.classes as cls
import macup.library.backup as bk

regex_filters = [
    cls.RegexFilter(r"test", bk.PATHS, bk.DIRECTORY, False, "RegName"),
    cls.RegexFilter(r"._.", bk.FILENAMES, bk.BOTH, True, "dot underscore dot"),
]
kw_filters = [
    cls.KeywordFilter(r"py", bk.PATHS, bk.FILES, False, "kw filter!!"),
]

#regex_filters2 = [{'name': 'RegName', 'application': 'PATHS', 'item_type': 'DIRECTORY', 'whitelist': 'False', 'regex': 'test'}, {'name': 'dot underscore dot', 'application': 'FILENAMES', 'item_type': 'BOTH', 'whitelist': 'True', 'regex': '._.'}]
#kw_filters2 = [{'name': 'kw filter!!', 'application': 'PATHS', 'item_type': 'FILES', 'whitelist': 'False', 'keyword': 'py'}]

cfg = cls.Configuration("write test", "source dir goes here", "target dir here", regex_filters, kw_filters, True)

print(general.parseConfigToDict(cfg))
