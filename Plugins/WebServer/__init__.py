#!/usr/bin/env python3

import atexit
from signal import SIGTERM
from os.path import dirname
from subprocess import Popen
from os import killpg, getpgid


if __name__ != '__main__':
    pro = Popen([dirname(__file__) + '/server/manage.py', 'runserver', '0.0.0.0:80'])
    atexit.register(lambda x: killpg(getpgid(x.pid), SIGTERM), pro)
