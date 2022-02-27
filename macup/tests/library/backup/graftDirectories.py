from macup.library.backup import graftDirectories


directories = ['/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder2', '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder2/SubFolder1', '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder3', '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder3/Sub Folder 2', '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder3/SubFolder1', '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder4', '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder1', '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder1/SubFolder2', '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder1/SubFolder1']

source = '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir'
target = '/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/Folder4'


print(graftDirectories(directories, source, target))
