"""
Simple maintainance script to update .ui files to their python equivalents
"""

# pyuic6 .ui -o .py

import os
import re

for file in os.listdir():
    match = re.match(r'(.+).ui$', file)
    if match:
        os.system(f"pyuic6 {file} -o {match.group(1)}.py")
