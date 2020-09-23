import sys, os
import traceback
import configparser
import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
import time
import datetime as dtime
import re
import signal
import shutil
import socket
from threading import Thread, Timer, enumerate as get_threads
from subprocess import Popen, PIPE, STDOUT, DEVNULL
from secrets import token_hex
from uuid import uuid4
import traceback
from queue import Queue
# from urllib.parse import quote, unquote
import copy
import sqlite3

import orjson
import dpath.util as dpath
import win32event
import win32service
import win32serviceutil
import servicemanager
import requests
from clickhouse_cityhash import cityhash


__version__ = "0.3.0-dev.0"
pickerType = "lootnika_mysql"
# Windows запускает модули exe из папки пользователя
# Папка должна определяться только исполняемым файлом
keys = os.path.split(os.path.abspath(os.path.join(os.curdir, __file__)))
appName = keys[1][:keys[1].find('.')].lower()
homeDir = sys.argv[0][:sys.argv[0].replace('\\', '/').rfind('/')+1]
uiDir = f"{homeDir}webui/"

if hasattr(sys, "_MEIPASS"):
    dataDir = sys._MEIPASS + '/'
else:
    dataDir = './'


class Sout:
    """
    Colored print for debugging
    """
    def __init__(self):
        self.color = {
            'white': '\x1b[37m',
            'green': '\x1b[0;30;32m',
            'sun': '\033[93m',
            'violet': '\x1b[0;30;35m',
            'breeze': '\x1b[0;30;36m',
            'red': '\x1b[0;30;31m'}

    def print(self, msg, clr = 'white'):
        """
        :param clr: colors available: white|green|sun|violet|breeze|red
        """
        print(f"{self.color[clr]}{msg}\x1b[0m")


sout = Sout()
__all__ = [
    'os', 'sys', 'servicemanager', 'traceback', 'RotatingFileHandler',
    'dtime', 'time', 'configparser', 're', 'logging', 'STDOUT', 'Queue',
    'shutil', 'signal', 'Thread', 'Timer', 'Popen', 'PIPE', 'DEVNULL',
    'get_threads', 'token_hex', 'uuid4', 'copy', 'Logger', 'socket',
    'pickerType',

    'win32event', 'win32service', 'win32serviceutil', 'win32event', 'sqlite3',
    'requests', 'dpath', 'orjson', 'cityhash',

    '__version__', 'homeDir', 'uiDir', 'dataDir', 'appName', 'sout'
]
