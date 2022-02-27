from macup.library.backup import graftItem


directory_to_copy = '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder1/SubFolder1'
source = '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir'
target = '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder4'


print(graftItem(directory_to_copy, source, target))
