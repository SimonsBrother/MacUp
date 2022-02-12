from macup.library.backup import getAll, FILES
from macup.classes import FileTree

print(getAll(FILES, FileTree("/macup/tests/TestDir")))
