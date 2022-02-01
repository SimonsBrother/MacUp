from macup.library import graftDirectory


directory_to_copy = '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder1/SubFolder1'
source = '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder1'
target = '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder2'


print(graftDirectory(directory_to_copy, source, target))
