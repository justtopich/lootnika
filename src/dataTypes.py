from typing import OrderedDict, Generator, Dict, List
from types import FunctionType
from threading import Thread
import configparser
from logging import Logger
from queue import Queue
import sqlite3


class SortedFields(OrderedDict):
    def __init__(self, **kwargs):
        super(SortedFields, self).__init__()

    def __str__(self):
        ...

    def items(self):
        ...

    def keys_sorted(self):
        for key in sorted(self.keys()):
            yield key

    def values(self):
        ...


class Document:
    """
    Lootnika Document. Factory can work only with this format.
    It's just json with header and body - header field "fields". "fields"
    contain all your fields and they are used for custom processing and calculating hash
    """
    def __init__(self, taskId, str, taskName: str, reference: str, loootId: str, fields: dict):
        """
        Creating document and his reference.

        :param reference: template to create reference
        :param loootId: ID of the document in the source.
            use for replacing @loot_id@ in reference if
            that's not in fields
        """

        self.reference = reference
        self.uuid = ''
        self.taskName = taskName
        self.taskId = taskId
        self.create_dtm = -1
        self.export = ''
        self.format = ''
        self._preTasksDone = False
        self.fields = SortedFields

    def get_hash(self) -> str:
        """
        calculate hash only for meta fields, not header
        """
        ...

    def dumps(self) -> bytes:
        """
        return document in bson format
        """
        ...

    def loads(self, lootBson:bytes):
        """
        load loonika document from bytes
        """
        ...


    def get_field(self, path: str):
        """
        using syntax from dpath library
        dpath incorrect working with datetime types
        (issue #145 https://github.com/dpath-maintainers/dpath-python/issues/145)
        """
        # return dpath.get(self.fields, path)
        ...


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
        Finalyze parcel. After export, next documents
        will added to new parcel.
        :return: finished parcel. ready to export
        """
        ...


def create_dirs(paths: List[str]) -> None:
    ...


def handler(doc:Document, vars: Dict[str, any]) -> Document or False:
    ...

class Exporter:
    def __init__(self, name: str, env: Dict[str, any]):
        self.type = ''
        self.name = ''
        self.cfg = {}
        self._converter = Converter
        self.create_dirs = create_dirs
        self.defaultCfg: Dict[str, str] = {}
        self.transformTasks: List[FunctionType] = []

    def load_config(self, config: configparser) -> dict:
        ...

    def add(self, doc: Document) -> None:
        ...

    def export(self, parcel: any) -> None:
        ...

    def delete(self, refList: list) -> None:
        """Delete not supported by this Exporter"""
        ...


class TaskStats:
    def __int__(self):
        self.total = -1
        self.seen = -1
        self.new = -1
        self.differ = -1
        self.deleted = -1
        self.taskErrors = -1
        self.exportErrors = -1


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
    def __init__(
            self,
            logMain: Logger,
            threads: int,
            exporters: Dict[str, Exporter]):
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
