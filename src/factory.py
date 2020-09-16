from lootnika import (
    homeDir,
    os,
    dtime, time,
    Thread,
    traceback,
    Queue,
    token_hex,
    Logger)
from taskstore import Document


class Factory(Thread):
    def __init__(self, taskName: str, taskLog: Logger, exporter: "Exporter", syncCount: list):
        """
        :param taskName: required for creating subdir in SendFail path
        :param syncCount: collector syncCount. Required for count up exporting fails
        """
        super(Factory, self).__init__()
        self.log = taskLog
        self.syncCount = syncCount
        self.name = 'Factory'
        self.log.debug("Starting Factory thread")

        self.docs = Queue()
        self.status = 'work'
        self.parcelSize = 0
        self.exporter = exporter
        self.converter = exporter._converter
        self.batchSize = exporter.cfg['batchSize']
        # TODO оставить за экспортёром
        self.failPath = f"{homeDir}{exporter.cfg['failPath']}{dtime.date.today().strftime('%Y%m%d')}/{taskName}/"
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
                    parcel = self.converter.get()
                    self.send(parcel)
                    self.parcelSize = 0
                else:
                    self.parcelSize += 1
                    doc.raw['exporter'] = self.exporter.type
                    doc.raw['format'] = self.converter.type
                    self.converter.add(doc)
                    if self.parcelSize >= self.batchSize:
                        parcel = self.converter.get()
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
            self.exporter.export(parcel)
            fail = False
        except Exception as e:
            e = traceback.format_exc()
            self.log.error("Failed to export: %s" % str(e).split('rror')[-1])

        if fail:
            self.save_fail(bytearray(parcel, encoding=self.converter.encoding), self.failPath)

        self.status = 'work'

    def send_delete(self, refList: list):
        ...

    def save_fail(self, parcel: bytearray, failPath: str):
        self.syncCount[6] += 1
        try:
            os.makedirs(failPath)
        except:
            pass

        try:
            with open(f"{failPath}{token_hex(8)}", mode='wb') as f:
                f.write(parcel)
        except Exception as e:
            self.log.error(f"Fail to save parcel to {self.failPath}: {e}")
