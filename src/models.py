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
    """
    Some attributes ExportBroker set himself and you don't need
    use them.

    attributes:
        type: name of Exporter
        name: name of Export in lootnika cfg file
        cfg: Exporter actual configuration that give lootnika
        defaultCfg: Exporter configuration example
        _converter: format of Exporter that contain Converter class
        create_dirs: function for creating dirs

    attributes by Broker:
        parcelSize: count of documents that ready to export. Calc by Broker
        queueSize: count of documents that in queue to export. Calc by Broker
        handlersNew: handlers for new docs (set in lootnika cfg file)
        handlersDelete: handlers for deleted docs (set in lootnika cfg file)
        status: actual info about what Exporter doing
    """
    def __init__(self, name: str, env: Dict[str, any]):
        self.type = ''
        self.name = name
        self.cfg = {}
        self.parcelSize = 0
        self.queueSize = 0
        self._converter = Converter
        self.create_dirs: Callable[[List[str]], None]
        self.defaultCfg: Dict[str, str] = {}
        self.handlersNew: List[Callable[[Document, Dict[str, any]], Document]] = []
        self.handlersDelete: List[Callable[[Document, Dict[str, any]], Document]] = []
        self.status = ''

    def load_config(self, config: configparser) -> Dict[str, any]:
        ...

    def add_new(self, doc: Document) -> None:
        """
        new or changed Documents
        """
        ...

    def export(self, parcel: any) -> None:
        """
        Export Documents to your destination.

        """
        ...

    def add_deleted(self, doc: Document) -> None:
        """
        Documents that have been deleted in source.
        Exporter may not supported this operation, but
        method must be.
        """
        ...


class ExportBroker(Thread):
    """
    Manage Documents flow from pickers to exporters.
    """
    def __init__(self, logMain: Logger, threads: int, exporters: Dict[str, Exporter]):
        super(ExportBroker, self).__init__()
        self.log = logMain
        self.threads = threads
        self.name = 'ExportBroker'

        self.workersQ = Queue(maxsize=threads + 1)
        self.workersLogging = Queue(maxsize=1000)
        self.exports = exporters
        self.taskExports: Dict[int, Dict[str, Exporter]] = {}
        self.defaultExports: Dict[int, str] = {}
        self.taskLoggers: Dict[int, Logger] = {}
        self.workersStarted: Dict[int, bool] = {}
        self.workers: List[Thread] = []
        self.lock = False

    def _worker(self, number: int):
        ...

    def _send(self, taskId: int, exportName: str):
        ...

    def mount_export(self, taskName: str, taskId: int, taskLog: Logger) -> None:
        """
        Create copy of exporter for task instance
        :param taskName:
        :param taskId:
        :param taskLog:
        :return:
        """
        ...

    def unmount_export(self, taskId: int) -> None:
        ...

    def put(self, taskId: int, doc: Union[Document, str], deleted=False, priority=5) -> None:
        """

        :param taskId:
        :param doc: Document or command '--send--'
        :param deleted: flag for deleted Document
        :param priority:
        :return:
        """
        ...

    @staticmethod
    def _load_transform_script(script: str) -> Callable[[Document, Dict[str,any]], Union[Document, None]]:
        """
        Search scripts in path and compile for using in
        Factory module

        :return: module
        """
        ...

    def _pre_process(self, taskId: int, doc: Document, deleted: bool) -> Document or None:
        ...

    def _handler_create_document(self, document: Document, deleted=False) -> None:
        """
        Put Document from handler.
        It will added as new Document with all processing steps

        :param document: lootnika Document
        :param deleted: flag for deleted document
        """
        ...

    def stop(self):
        ...

    def run(self):
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
