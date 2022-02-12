import macup.library.backup as bk
from macup.classes import RegexFilter, KeywordFilter

regexes = [
    RegexFilter(r'..l...1', bk.FILENAMES, bk.DIRECTORY, True),
    RegexFilter(r'.*calebhair.*', bk.PATHS, bk.BOTH, True),
]

keywords = [
    KeywordFilter('1', bk.FILENAMES, bk.BOTH, False),
]

print(bk.applyFilter(regexes, keywords, "/macup/tests/TestDir/Folder1"))
