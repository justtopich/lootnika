from lootnika import (
    traceback,
    Thread,
    Queue,
    time,
    copy,
    sout,
    logging,
    Logger,
)
from conf import cfg
from dataTypes import Document, Exporter

from typing import List, Tuple, Dict
from types import FunctionType


class WorkerLogMsg:
    def __init__(self, owner:str,  level: int, text: str):
        self.owner = owner
        self.level = level
        self.text = text


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
        self.name = 'ExportBroker'
        self.log.debug("Starting ExportBroker thread")

        self.workersQ = Queue(maxsize=threads + 1)
        self.workersLogging = Queue(maxsize=1000)
        self.exports = exporters
        self.taskExports: Dict[str, Dict[str, Exporter]] = {}
        self.defaultExports: Dict[str, str] = {}
        self.taskLoggers: Dict[str, Logger] = {}
        self.workersStarted: Dict[int, bool] = {}
        self.workers: List[Thread] = []
        self.lock = False
        for i in range(1, self.threads + 1):
            self.workersStarted[i] = False
            pr = Thread(
                    name=f'worker_{i}',
                    target=self._worker,
                    args=(i,)
                )
            pr.start()
            self.workers.append(pr)

    def _worker(self, number: int):
        self.log.debug(f"Start ExportBroker queue {number}")
        self.workersStarted[number] = True

        while True:
            taskId: str; doc: Document
            taskId, doc = self.workersQ.get()
            # sout(doc, 'violet')

            try:
                if doc == '--stop--':
                    self.log.debug(f"Stopping ExportBroker queue {number}")
                    break
                elif doc == '--send--':
                    while self.lock:
                        time.sleep(.05)

                    self.lock = True
                    # sout('worker lock', 'breeze')
                    for name, expOut in self.taskExports[taskId].items():
                        if expOut.parcelSize > 0:
                            try:
                                self._send(taskId, name)
                                expOut.parcelSize = 0
                            except Exception as e:
                                self.taskLoggers[taskId].error(f'{name}: {e}')

                    self.lock = False
                    # sout('worker unlock', 'breeze')
                else:
                    expOut = doc.export
                    expModule = self.taskExports[taskId][expOut]

                    if not doc._preTasksDone:
                        doc.exporter = expModule.type
                        doc.format = expModule._converter.type
                        doc = self._pre_process(taskId, doc)
                        if not doc:
                            continue

                    expModule.parcelSize += 1
                    expModule.add(doc)

                    while self.lock:
                        time.sleep(.05)

                    self.lock = True
                    # sout('worker lock', 'breeze')
                    for k, v in self.taskExports[taskId].items():
                        if v.parcelSize >= v.cfg['batchSize']:
                            try:
                                self._send(taskId, k)
                                v.parcelSize = 0
                            except Exception as e:
                                self.taskLoggers[taskId].error(f'{name}: {e}')

                    self.lock = False
            except Exception as e:
                # self.syncCount[6] += 1
                # if log.level == 10:
                e = traceback.format_exc()
                sout(e, 'red')
            #     log.error(f"Factory: {e}")
            finally:
                self.workersQ.task_done()

                if doc == '--send--':
                    for exp in self.taskExports[taskId].values():
                        exp.queueSize -= 1
                elif doc == '--stop--':
                    pass
                else:
                    self.taskExports[taskId][expOut].queueSize -= 1

                # for i in self.taskExports.values():
                #     for k, v in i.items():
                #         sout(f'{k} = {v.queueSize}', 'sun')

    def _send(self, taskId: str, export: str):
        expOut = self.taskExports[taskId][export]
        while expOut.status == 'sending':
            time.sleep(.2)

        if expOut.parcelSize < 1:
            return

        expOut.status = 'sending'
        self.taskLoggers[taskId].info(f'{export}: New export ({expOut.parcelSize})')

        try:
            parcel = expOut._converter.get()
        except Exception as e:
            expOut.status = 'work'
            # self.syncCount[6] += 1
            e = traceback.format_exc()
            raise Exception(f"Convert to {expOut._converter.type}: {str(e).split('rror')[-1]}")

        try:
            expOut.export(parcel)
            return True
        except Exception as e:
            # self.syncCount[6] += 1
            e = traceback.format_exc()
            self.log.error(f"Failed to export: {str(e).split('rror')[-1]}")
            # self.save_fail(bytearray(parcel, encoding=self.converter.encoding), self.failPath)
        finally:
            expOut.status = 'work'

    def mount_export(self, taskName: str, taskId: str, taskLog: Logger) -> None:
        """
        Create copy of exporter for task instance
        :param taskName:
        :param taskId:
        :param taskLog:
        :return:
        """
        while self.lock:
            time.sleep(.05)

        self.lock = True
        # sout('mount lock', 'breeze')
        self.taskLoggers[taskId] = taskLog
        taskCfg = cfg['schedule']['tasks'][taskName]
        tmp = {}
        for exp in taskCfg['export']:
            taskLog.debug(f'mount export {exp}')

            expModule = copy.copy(self.exports[exp])
            expModule.parcelSize = 0
            expModule.queueSize = 0
            expModule.transformTasks = [(i, self._load_transform_script(i)) for i in taskCfg['transformTasks']]
            expModule.status = 'work'
            tmp[exp] = expModule

        self.taskExports[taskId] = tmp
        self.defaultExports[taskId] = taskCfg['defaultExport']
        self.lock = False
        # sout('mount unlock', 'breeze')

    def unmount_export(self, taskId: str) -> None:
        self.put(taskId, '--send--')
        for exp in self.taskExports[taskId].values():
            while exp.queueSize > 0:
                time.sleep(.2)

        while self.lock:
            time.sleep(.05)

        self.lock = True
        # sout('unmount lock', 'breeze')
        del self.taskExports[taskId]
        del self.taskLoggers[taskId]
        del self.defaultExports[taskId]
        self.lock = False
        # sout('unmount unlock', 'breeze')

    def put(self, taskId: str, doc: Document, priority=5) -> None:
        """

        :param taskId:
        :param doc: Document or command '--send--'
        :param export: only that set in task
        :param priority:
        :return:
        """
        if doc == '--send--':
            for exp in self.taskExports[taskId].values():
                exp.queueSize += 1
        elif doc == '--stop--':
            pass
        else:
            if doc.export == '':
                doc.export = self.defaultExports[taskId]
            self.taskExports[taskId][doc.export].queueSize += 1

        while self.lock:
            time.sleep(.05)

        self.lock = True
        # sout('put lock', 'breeze')
        # sout(doc, 'green')
        # for i in self.taskExports.values():
        #     for k,v in i.items():
        #         sout(f'{k} = {v.queueSize}', 'green')

        self.lock = False
        # sout('put unlock', 'breeze')
        self.workersQ.put((taskId, doc,))

    def _load_transform_script(self, script: str) -> FunctionType:
        """
        Search scripts in path and compile for using in
        Factory module

        :return: module
        """
        ext, fileName = script.split(':')
        fileName = fileName[:-3]

        if ext != 'py':
            raise Exception(f"Wrong script extension {ext}")

        try:
            module = __import__(
                f'scripts.{fileName}',
                # globals=globals(),
                # locals=locals(),
                fromlist=['handler'])

            return getattr(module, 'handler')
        except ModuleNotFoundError as e:
            raise Exception(f"No script {fileName}. Try to set full path.")
        except AttributeError as e:
            raise Exception(f'Wrong script: {e}')
        except Exception as e:
            raise Exception(f'Fail import script: {e}')

    def _pre_process(self, taskId: str, doc: Document) -> Document or None:

        taskLog = self.taskLoggers[taskId]

        taskLog.debug(f"Processing {doc.reference}")
        exportName = doc.export
        for name, task in self.taskExports[taskId][exportName].transformTasks:
            try:
                doc = task(doc, {'log': self.taskLoggers[taskId], 'put_new_doc': self._pre_process_put})
                if not doc:
                    taskLog.debug(f"Reject document by pre-task {name} ")
                    return
            except Exception as e:
                taskLog.error(f"Pre-task {name}: {traceback.format_exc()}")

        doc._preTasksDone = True
        return doc

    def _pre_process_put(self, document: Document):
        doc = copy.deepcopy(document)
        doc._preTasksDone = True
        self.put(doc.taskId, doc)

    def stop(self):
        self.log.debug("Stopping ExportBroker thread")
        for i in self.taskExports:
            self.put(i, '--send--')

        for i in self.workers:
            self.workersQ.put(('', '--stop--',))

        self.workersLogging.put('--stop--')

    def run(self):
        while True:
            try:
                msg: WorkerLogMsg = self.workersLogging.get()
                if msg == '--stop--':
                    break
    #             if msg.owner == 'main':
    #                 self.log._log(msg.level, msg.text, None)
    #             else:
    #                 self.taskLoggers[msg.owner]._log(msg.level, msg.text, None)
            except Exception as e:
                self.log.error(f"ExportBroker worker logging: {traceback.format_exc()}")
            finally:
                self.workersLogging.task_done()
