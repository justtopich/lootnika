from lootnika import (
    os,
    dtime, time,
    Thread,
    traceback,
    Queue,
    token_hex,
    Logger)
from taskstore import Document
from publish.lootnika_text import Publisher, Converter


class Factory(Thread):
    def __init__(self, taskName: str, cfg: dict, taskLog: Logger, publisher: Publisher):
        """
        :param taskName: create subdir in SendFail path
        :param cfg: output section
        """
        super(Factory, self).__init__()
        self.log = taskLog
        self.name = 'Factory'
        self.log.debug("Starting Factory thread")

        self.status = 'work'
        self.failed = 0
        self.parcelSize = 0
        self.publisher = publisher
        self.converter = Converter()
        self.docs = Queue()
        self.batchSize = cfg['batchSize']
        self.failPath = f"{cfg['failPath']}{dtime.date.today().strftime('%Y%m%d')}/{taskName}/"
        self.start()

    def run(self):
        while True:
            try:
                doc = self.docs.get()
                if doc == '--stop--':
                    self.log.debug("Stopping Factory thread")
                    while self.status != 'work':
                        time.sleep(1)
                    break
                elif doc == '--send--':
                    if self.parcelSize == 0: continue
                    parcel = self.converter.export()
                    self.send(parcel)
                    self.parcelSize = 0
                else:
                    self.parcelSize += 1
                    self.converter.add(doc)
                    if self.parcelSize >= self.batchSize:
                        parcel = self.converter.export()
                        self.send(parcel)
                        self.parcelSize = 0
            except Exception as e:
                if self.log.level == 10:
                    e = traceback.format_exc()
                self.log.error(f"Factory: {e}")
            finally:
                self.docs.task_done()

    def put(self, doc: Document):
        self.docs.put(doc)

    def pre_process(self):
        ...

    def send(self, parcel):
        self.status = 'sending'
        self.log.info(f'New parcel sending, size: {self.parcelSize}')
        fail = True

        try:
            self.publisher.publish(parcel)
            fail = False
        except Exception as e:
            e = traceback.format_exc()
            self.log.error("Failed to publish: %s" % str(e).split('rror')[-1])

        if fail:
            self.save_fail(bytearray(parcel, encoding=self.converter.encoding), self.failPath)

        self.status = 'work'

    def send_delete(self, refList: list):
        ...

    def save_fail(self, parcel: bytearray, failPath: str):
        self.failed += 1
        try:
            os.makedirs(failPath)
        except:
            pass

        try:
            with open(f"{failPath}{token_hex(8)}", mode='wb') as f:
                f.write(parcel)
        except Exception as e:
            self.log.error(f"Fail to save parcel to {self.failPath}: {e}")
