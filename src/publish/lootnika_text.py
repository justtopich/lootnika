from lootnika import (
    configparser,
    Logger)
from conf import log, create_dir
from taskstore import Document


# TODO вынести, исопльзовать несколько форматов
class Converter:
    """
    Convert internal format (lootnika document) into text.
    Create parcel (final external document) for publisher.
    """
    def __init__(self):
        """
        Converter must have:
            self.type - self name that can say about output format\n
            self.encoding - for bytearray(). Use None if you parcel is also like that
        """
        self.type = "lootnika_text"
        self.encoding = 'utf-8'
        self.adds = {"DOCUMENTS": []}

    def add(self, doc: Document):
        self.adds["DOCUMENTS"].append(doc.raw)

    def export(self) -> str:
        """
        Finalyze parcel. After export next documents
        will added to new parcel.
        :return: finished parcel & parcel in raw format
        """
        parcel = f"{self.adds}\n\n"
        self.adds = {"DOCUMENTS": []}
        return parcel


class Publisher:
    def __init__(self, name: str):
        self.type = "lootnika_text"
        self.name = name
        self.log = log
        self.cfg = {}
        self.filename = 0
        self.defaultCfg = {
            "type": self.type,
            "path": "outgoing",
            "failPath": "send_failed/",
            "extension": "txt"
            # "filename": "{{field:DOCUMENTS/0/REFERENCE}}_{{random(8)}}.txt"
        }

    def load_config(self, config: configparser):
        try:
            self.cfg['path'] = config.get(self.name, 'path')
            self.cfg['path'] = self.cfg['path'].replace('\\', '/', -1)
            if not self.cfg['path'].endswith("/"):
                self.cfg['path'] += "/"

            if config.has_option(self.name, 'extension'):
                self.cfg['extension'] = config.get(self.name, 'extension')
            else:
                self.cfg['extension'] = self.defaultCfg['extension']

        except Exception as e:
            e = f"Bad {self.name} configuration: {e}"
            log.error(e)
            raise Exception(e)

        create_dir([self.cfg['path']])
        return self.cfg

    # TODO use scheduler for that
    def set_logger(self, taskLog: Logger):
        """
        call at the beginning of each task
        """
        self.log = taskLog

    def publish(self, parcel: str):
        # filename = self.filename

        # match = re.findall(r"(?i)({{field:.*?}})", filename)
        # if match:
        #     for path in match:
        #         try:
        #             path = path
        #             field = dpath.get(raw, path[8:-2])
        #         except KeyError as e:
        #             self.log.warning(f"with creating filename: no document path: {e}")
        #             field = token_hex(8)

                # filename = filename.replace(path, field)

        # match = re.findall(r"(?i)({{random\(\d+\)?}})", filename)
        # if match:
        #     for rule in match:
        #         hx = token_hex(int(rule[9:-3]))
        #         filename = filename.replace(rule, hx)

        try:
            with open(f"{self.cfg['path']}{self.filename}.{self.cfg['extension']}", mode='a') as f:
                f.write(parcel)
            self.filename += 1
        except Exception as e:
            self.log.error(f'Fail to publish document: {e}')
