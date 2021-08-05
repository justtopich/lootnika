import configparser
from models import Document


class Exporter:
    def __init__(self, name: str, env):
        self.type = "lootnika_binary"
        self.name = name
        self.cfg = {}
        self.filename = ''
        self._converter = None
        self.create_dirs = env['create_dirs']
        self.defaultCfg = {
            "format": "bson",
            "path": "outgoing",
            "fileName": "@loot_id@.data",
            "batchSize": "100",
            "failPath": "export_failed"
        }

    def load_config(self, config: configparser) -> dict:
        try:
            self.cfg['batchSize'] = config.getint(self.name, "batchSize")
            self.cfg['fileName'] = config.get(self.name, 'fileName')
            self.cfg['path'] = config.get(self.name, 'path')
            self.cfg['path'] = self.cfg['path'].replace('\\', '/', -1)
            if not self.cfg['path'].endswith("/"):
                self.cfg['path'] += "/"

            try:
                if config.has_option(self.name, 'failPath'):
                    self.cfg['failPath'] = config.get(self.name, "failPath").replace("\\", "/", -1)
                    if not self.cfg['failPath'].endswith("/"):
                        self.cfg['failPath'] += "/"
                else:
                    self.cfg['failPath'] = self.defaultCfg['failPath']
            except FileExistsError:
                pass
            except Exception as e:
                e = f"Bad {self.name} configuration: {e}"
                raise Exception(e)

            try:
                self.cfg['format'] = config.get(self.name, 'format')
                module = __import__(f"exporters.{self.type}.formats.{self.cfg['format']}",
                                    globals=globals(),
                                    locals=locals(),
                                    fromlist=['Converter'])
                Converter = getattr(module, 'Converter')
                self._converter = Converter(dict(config.items(self.name)), self.cfg)

            except ModuleNotFoundError as e:
                e = f"Not found format {self.cfg['format']} in exporter"
                raise Exception(e)

            except Exception as e:
                e = f"Bad export format {self.cfg['format']}: {e}"
                raise Exception(e)

        except Exception as e:
            e = f"Bad {self.name} configuration: {e}"
            raise Exception(e)

        self.create_dirs((self.cfg['path'], self.cfg['failPath']))
        return self.cfg

    def add(self, doc: "Document"):
        if self.filename == '':
            filename = self.cfg['fileName']
            try:
                for i in doc.fields:
                    filename = filename.replace(f'@{i}@', f'{doc.fields[i]}', -1)
            except Exception as e:
                raise Exception(f'No field: {e}')

            self.filename = filename
        self._converter.add(doc)

    def export(self, parcel: bytes):
        with open(f'{self.cfg["path"]}{self.filename}', mode='wb') as f:
            f.write(parcel)

        self.filename = ''

    def delete(self, refList: list):
        """Delete not supported by this Exporter"""
        ...
        # for ref in refList:
        #     try:
        #         os.remove(f"{self.cfg['path']}{self._filename}.{self.cfg['extension']}")
        #     except Exception as e:
        #         self.log.warning(f'')
