import macup.library as mul
from macup.classes import RegexFilter, KeywordFilter

regexes = [
    RegexFilter(r'..l...1', mul.FILENAMES, mul.DIRECTORY, True),
    RegexFilter(r'.*calebhair.*', mul.PATHS, mul.BOTH, True),
]

keywords = [
    KeywordFilter('1', mul.FILENAMES, mul.BOTH, False),
]

print(mul.applyFilter(regexes, keywords, "/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder1"))
