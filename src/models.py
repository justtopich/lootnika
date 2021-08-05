"""
this module contain models that are using
in different modules aside from primary
"""

from dataclasses import dataclass
from typing import OrderedDict, Union, Dict, List, Tuple, Callable
from threading import Thread
import configparser
from logging import Logger
from queue import Queue
import sqlite3

from document import SortedFields, Document


class Converter:
    def __init__(self, cfgSection: dict=None, cfgExporter: dict=None):
        """
        :param cfgSection: exporter section raw.
        :param cfgExporter: exporter validated configuration, no needed.
        """
        self.type = ''

    def add(self, doc: Document) -> None:
        ...

    def get(self) -> any:
        """
        Finalize parcel. After export, next documents
        will added to new parcel.
        :return: finished parcel. ready to export
        """
        ...


class Exporter:
    def __init__(self, name: str, env: Dict[str, any]):
        self.type = ''
        self.name = name
        self.cfg = {}
        self._converter = Converter
        self.create_dirs: Callable[[List[str]], None]
        self.defaultCfg: Dict[str, str] = {}
        self.transformTasks: List[Callable[[Document, Dict[str,any]], Document]] = []

    def load_config(self, config: configparser) -> dict:
        ...

    def add(self, doc: Document) -> None:
        ...

    def export(self, parcel: any) -> None:
        ...

    def delete(self, refList: list) -> None:
        """Delete not supported by this Exporter"""
        ...


@dataclass
class TaskStats:
    """
    task work statistics.
    Using for checking progress and
    final report
    """
    total = -1
    seen = -1
    new = -1
    differ = -1
    deleted = -1
    taskErrors = -1
    exportErrors = -1


class TaskStore:
    def __init__(self, taskName: str, log: Logger, overwrite: bool = False):
        """
        Open taskstore or create new if it doesn't exist.\n
        You must prepare taskstore before collect documents

        :param log: Use task logger
        :param overwrite: create new taskstore even if it exist
        """
        self.log = log
        self.overwrite = overwrite
        self.cnx = self._create_task_store(taskName)

    def _create_task_store(self, taskName: str) -> sqlite3.Connection:
        """
        Connector creating local DB for each task
        to store information about seen documents

        :param taskName: will create taskName.db file
        :return: None on error
        """
        ...

    def prepare(self) -> bool:
        """Mark all documents as old"""
        ...

    def check_document(self, ref: str, docHash: str) -> int:
        """
        Check document for changes by hash

        :param ref: reference
        :param docHash: cityHash64 from Document.get_hash()
        :return:
            operation status that can be:
                 0 - not changed\n
                 1 - changed (differ)\n
                 2 - new\n
                -1 - error\n
        """
        ...

    def delete_unseen(self) -> list:
        ...


class ExportBroker(Thread):
    """
    ExportBroker consolidate all exports as exportQueue.
    It takes Lootnika documents and redirect them to
    exportQueue that set in document

    :param taskName: required for creating subdir in SendFail path
    :param syncCount: Picker syncCount. Required for count up exporting fails

    Attributes:
        log: lootnika main logger
        exports: loaded exporters from config
        taskExports: copy of exports for each task instance

    """

    def __init__(
            self,
            logMain: Logger,
            threads: int,
            exporters: Dict[str, Exporter]):

        super(ExportBroker, self).__init__()
        self.log = logMain
        self.threads = threads
        self.name = ''

        self.workersQ = Queue
        self.workersLogging = Queue
        self.exports = exporters
        self.taskExports: Dict[str, Dict[str, Exporter]] = {}
        self.defaultExports = {}
        self.taskLoggers = {}
        self.workersStarted = {}
        self.workers: List[Thread] = []
        self.lock = False

    def _worker(self, number: int) -> None:
        ...

    def send(self, taskId) -> None:
        ...

    def mount_export(self, taskId: str, exportLs: List[str], default: str, taskLog: Logger) -> None:
        """
        Create copy of exporter for task instance
        :param taskId:
        :param exportLs:
        :param default:
        :param taskLog:
        :return:
        """
        ...

    def unmount_export(self, taskId: str) -> None:
        ...

    def put(self, taskId: str, doc: Document, export='', priority=5) -> None:
        """

        :param taskId:
        :param doc: Document or command '--send--'
        :param export: only that set in task
        :param priority:
        :return:
        """
        ...

    def run(self):
        ...


class Picker:
    def __init__(self, taskId: int, name: str, task: Dict[str, any], log: Logger,
                 taskStore: TaskStore, factory: ExportBroker, taskStats: TaskStats):
        """
        Initialization

        :param taskId: datastore._mark_task_start()
        :param name: task section name
        :param task: task section
        :param log: conf.create_task_logger()
        :param taskStore: TaskStore interface
        """
        self.type = ''
        self.taskName = name
        self.taskId = taskId
        self.ts = taskStore
        self.task = task
        self.log = log
        self.factory = factory
        self.syncCount = taskStats

    def run(self) -> None:
        ...


@dataclass
class WorkerLogMsg:
    owner: str
    level: int
    text: str
