import sys, os
import traceback
import configparser
import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
import datetime as dtime
import time
import re
import signal
import shutil
import socket
from http import client as httpClient
from collections import OrderedDict
from threading import Thread, Timer, enumerate as get_threads
from subprocess import Popen, PIPE, STDOUT, DEVNULL
from secrets import token_hex
from queue import Queue
from uuid import uuid4
import traceback
# from urllib.parse import quote, unquote
import copy
import sqlite3
import asyncio
import types

import orjson
import bson
import dpath.util as dpath
import aiohttp
from aiohttp import web as aioweb
from clickhouse_cityhash import cityhash
import psutil
import sphinx


__version__ = "1.1.0-beta.0"
pickerType = "lootnika_pyodbc"
upTime = dtime.datetime.now()
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


def sout(msg, clr='white'):
    """
    :param clr: colors available: white|green|sun|violet|breeze|red
    """
    colors = {
        'white': '\x1b[37m',
        'green': '\x1b[0;30;32m',
        'sun': '\033[93m',
        'violet': '\x1b[0;30;35m',
        'breeze': '\x1b[0;30;36m',
        'red': '\x1b[0;30;31m'}

    print(f"{colors[clr]}{msg}\x1b[0m")


__all__ = [
    'os', 'sys', 'traceback', 'RotatingFileHandler',
    'dtime', 'time', 'configparser', 're', 'logging', 'STDOUT', 'Queue',
    'shutil', 'signal', 'Thread', 'Timer', 'Popen', 'PIPE', 'DEVNULL',
    'get_threads', 'token_hex', 'uuid4', 'copy', 'Logger', 'socket',
    'pickerType', 'asyncio', 'httpClient', 'upTime', 'types',
    'OrderedDict',

    'sqlite3', 'dpath', 'orjson', 'cityhash', 'aioweb', 'aiohttp', 'bson',
    'psutil', 'sphinx',

    '__version__', 'homeDir', 'uiDir', 'dataDir', 'appName', 'sout', 'pickerType'
]

if os.name == "nt":
    import win32event
    import win32service
    import win32serviceutil
    import servicemanager

    __all__.extend(['win32event', 'win32service', 'win32serviceutil', 'servicemanager'])
    platform = 'nt'
else:
    # TODO supporting
    # from deamonizer import Daemonize  # custom wrapper
    __all__.append('Daemonize')
    platform = 'posix'

__all__.append('platform')
