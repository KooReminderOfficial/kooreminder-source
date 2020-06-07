#!/usr/bin/env python3

import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module == '__pycache__':
        continue
    __import__('Plugins.' + module, locals(), globals())
del module