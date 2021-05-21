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
    def __init__(self, taskName: str, taskLog: Logger, exporter: "Picker", syncCount: list):
        """
        Factory can have two status:
            work
            sending

        :param taskName: required for creating subdir in SendFail path
        :param syncCount: Picker syncCount. Required for count up exporting fails
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
        # TODO либо вынести save_fail в экспорт либо сделать тут для всех
        self.failPath = f"{homeDir}{exporter.cfg['failPath']}/{dtime.date.today().strftime('%Y%m%d')}/{taskName}/"
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
                    self.send()
                    self.parcelSize = 0
                else:
                    self.parcelSize += 1
                    doc.raw['exporter'] = self.exporter.type
                    doc.raw['format'] = self.converter.type
                    self.converter.add(doc)
                    if self.parcelSize >= self.batchSize:
                        self.send()
                        self.parcelSize = 0
            except Exception as e:
                self.syncCount[6] += 1
                if self.log.level == 10:
                    e = traceback.format_exc()
                self.log.error(f"Factory: {e}")
            finally:
                self.docs.task_done()
                self.status = 'work'

    def put(self, doc: Document or str):
        """
        Put lootnika document or command.
        Command can be:
            - --send-- - send parcel immediately\n
            - --stop-- - stop factory.

        Factory will loose the package if it has not been sent.
        Use it for hard stop. For safe stop must use: send, stop
        """
        self.docs.put(doc)

    def pre_process(self):
        ...

    def send(self):
        self.status = 'sending'
        self.log.info(f'New parcel sending, size: {self.parcelSize}')

        try:
            parcel = self.converter.get()
        except Exception as e:
            self.syncCount[6] += 1
            e = traceback.format_exc()
            raise Exception(f"Convert to {self.converter.type}: {str(e).split('rror')[-1]}")

        try:
            self.exporter.export(parcel)
            return True
        except Exception as e:
            self.syncCount[6] += 1
            e = traceback.format_exc()
            self.log.error(f"Failed to export: {str(e).split('rror')[-1]}")
            self.save_fail(bytearray(parcel, encoding=self.converter.encoding), self.failPath)

    def send_delete(self, refList: list):
        ttl = len(refList)
        if ttl > self.batchSize:
            start = 0
            while start < ttl:
                self.exporter.delete(refList[start:start + self.batchSize])
                start += self.batchSize
        else:
            self.exporter.delete(refList)

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
