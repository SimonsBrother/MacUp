import macup.library.backup as bk
from macup.library.classes import RegexFilter, KeywordFilter

regexes = [

]

keywords = [
    KeywordFilter(name='Name', application='FILENAMES', item_type='DIRECTORY', whitelist=False, keyword='Computer Science')
]

print(bk.applyFilter(regexes, keywords, "/Users/calebhair/Documents/School/A-Level/Physics"))
