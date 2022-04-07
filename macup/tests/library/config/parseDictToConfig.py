import macup.library.config as general

config = {
      "name": "configname",
      "source_dir": "//",
      "target_dir": "///",
      "regex_filters": [
        {
          "name": "regexfiltername",
          "application": "PATHS",
          "item_type": "FILES",
          "whitelist": True,
          "regex": "..."
        }
      ],
      "keyword_filters": [
        {
          "name": "a",
          "application": "FILENAMES",
          "item_type": "DIRECTORY",
          "whitelist": True,
          "keyword": "b"
        }
    ]
}

print(general.parseDictToConfig(config))
