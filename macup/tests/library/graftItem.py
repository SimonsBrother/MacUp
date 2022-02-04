from macup.library import graftItem


directory_to_copy = '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder1/SubFolder1'
source = '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder1'
target = '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder2'


print(graftItem(directory_to_copy, source, target))
