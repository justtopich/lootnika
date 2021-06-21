from lootnika import (
    traceback,
    Thread,
    time,
    copy,
    sout,
    PriorityQueue,
    logging,
    Logger,
)
from taskstore import Document
from conf import cfg
from exportWorker import worker

from multiprocessing import Process, JoinableQueue, Manager, Lock
from typing import List, Tuple, Dict
import pickle


lock = Lock()
exporters = cfg['exporters']
taskExports = {}


class WorkerLogMsg:
    def __init__(self, owner:str,  level: int, text: str):
        # assert owner in ['main', 'task'], f'owner must be main or task'

        self.owner = owner
        self.level = level
        self.text = text


class ExportBroker(Thread):
    def __init__(
            self,
            logMain: Logger,
            threads: int,
            exporters: dict):
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
        self.name = 'ExportBroker'
        self.log.debug("Starting ExportBroker thread")

        self.inputDocs = PriorityQueue()
        self.workersQ = JoinableQueue(maxsize=threads + 1)
        self.workersLogging = JoinableQueue(maxsize=1000)
        self.manager = Manager()
        self.exports = exporters
        self.taskExports = self.manager.dict()
        self.defaultExports = self.manager.dict()
        self.taskLoggers = self.manager.dict()
        self.workersStarted = self.manager.dict()
        self.workers = []
        for i in range(1, self.threads + 1):
            self.workersStarted[i] = False
            pr = Process(
                    name=f'worker_{i}',
                    target=worker,
                    args=(i, lock, self.workersLogging, self.workersQ, self.taskExports, self.workersStarted)
                )
            pr.start()
            self.workers.append(pr)

    def mount_export(self, taskId: str, exportLs: List[str], default: str, taskLog: Logger) -> None:
        """
        Create copy of exporter for task instance
        :param taskId:
        :param exportLs:
        :param default:
        :param taskLog:
        :return:
        """
        self.taskLoggers[taskId] = taskLog
        tmp = {}
        for exp in exportLs:
            taskLog.debug(f'mount export {exp}')

            tmp[exp] = copy.copy(self.exports[exp])
            tmp[exp].parcelSize = 0
            tmp[exp].queueSize = 0

        with lock:
            self.taskExports[taskId] = tmp
            self.defaultExports[taskId] = default

    def unmount_export(self, taskId: str) -> None:
        with lock:
            self.put(taskId, '--send--')
            # del self.taskExports[taskId]
            # del self.taskLoggers[taskId]
            # del self.defaultExports[taskId]

    def put(self, taskId: str, doc: Document, export=None, priority=5) -> None:
        if not export:
            export = self.defaultExports[taskId]

        with lock:
            self.taskExports[taskId]

        self.workersQ.put((taskId, doc, export))

    def run(self):
        self.status = 'work'
        while True:
            try:
                msg: WorkerLogMsg = self.workersLogging.get()
                if msg == '--stop--':
                    self.log.debug("Stopping ExportBroker thread")
                    break
                if msg.owner == 'main':
                    self.log._log(msg.level, msg.text, None)
                else:
                    self.taskLoggers[msg.owner]._log(msg.level, msg.text, None)
            except Exception as e:
                self.log.error(f"ExportBroker worker logging: {traceback.format_exc()}")
            finally:
                self.workersLogging.task_done()
