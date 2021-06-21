from lootnika import logging, sout, traceback
from taskstore import Document

from multiprocessing import JoinableQueue, Lock
from typing import List, Tuple, Dict


class WorkerLogMsg:
    def __init__(self, owner:str,  level: int, text: str):
        # assert owner in ['main', 'task'], f'owner must be main or task'

        self.owner = owner
        self.level = level
        self.text = text

def worker(number: int, lock: Lock, workersLogging: JoinableQueue, workersQ: JoinableQueue,
            taskExports: Dict[str, "Exporter"], workersStarted: Dict[int, bool]):

    workersLogging.put(WorkerLogMsg('main', logging.DEBUG, f"Start ExportBroker queue {number}"))
    workersStarted[number] = True
    while True:
        try:
            taskId: str; doc: Document; expOut: str
            taskId, doc, expOut = workersQ.get()
            sout(doc, 'violet')
            if doc == '--stop--':
                workersLogging.put(WorkerLogMsg('main', logging.DEBUG, f"Stopping ExportBroker queue {number}"))
                break
            elif doc == '--send--':
                with lock:
                    for name, exp in taskExports[taskId].items():
                        sout(exp.parcelSize, 'green')
                        if exp.parcelSize > 0:
                            # exp.send()
                            exp.parcelSize = 0

                        taskExports[taskId][name] = exp
            else:
                doc.exporter = taskExports[taskId][expOut].type
                doc.format = taskExports[taskId][expOut]._converter.type
                with lock:
                    expUpdate = taskExports[taskId][expOut]
                    expUpdate.parcelSize = 1
                    expUpdate._converter.add(doc)
                    if expUpdate.parcelSize >= expUpdate.cfg['batchSize']:
                        expUpdate.send()
                        expUpdate.parcelSize = 0

                    taskExports[taskId][expOut] = expUpdate
        except Exception as e:
            # self.syncCount[6] += 1
            # if log.level == 10:
                e = traceback.format_exc()
                sout(e, 'red')
        #     log.error(f"Factory: {e}")
        finally:
            workersQ.task_done()