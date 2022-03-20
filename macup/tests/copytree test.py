"""
shutil.copytree is not going to be used because it restricts the current ability to filter;
filters can only be applied to filenames with copytree (which may be fine, but I don't want to change everything)
"""

import shutil
from pathlib import Path

ignore = ["copytreetest"]


def filter_(dirname, paths):
    print(paths)
    return filter(lambda path: Path(path).name in ignore, paths)


shutil.copytree("/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir",
                "/Users/calebhair/Documents/Projects/MacUp/macup/tests/TestDir/copytreetest",
                ignore=filter_,
                dirs_exist_ok=True)
