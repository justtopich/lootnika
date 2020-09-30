from lootnika import configparser
from conf import create_dirs


class Exporter:
    def __init__(self, name: str):
        self.type = "lootnika_text"
        self.name = name
        self.cfg = {}
        self._filename = -1
        self._converter = None
        self.defaultCfg = {
            "format": "json",
            "extension": "json",
            "path": "outgoing",
            "batchsize": "100",
            "failPath": "send_failed/"
        }

    def load_config(self, config: configparser) -> dict:
        try:
            self.cfg['batchSize'] = config.getint(self.name, "batchSize")
            self.cfg['path'] = config.get(self.name, 'path')
            self.cfg['path'] = self.cfg['path'].replace('\\', '/', -1)
            if not self.cfg['path'].endswith("/"):
                self.cfg['path'] += "/"

            # TODO тут по аналогии - параметры формата можно в него перенести
            if config.has_option(self.name, 'extension'):
                self.cfg['extension'] = config.get(self.name, 'extension')
            else:
                self.cfg['extension'] = self.defaultCfg['extension']

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
                self._converter = Converter(dict(config.items(self.name)))

            except ModuleNotFoundError as e:
                e = f"Not found format {self.cfg['format']} in exporter"
                raise Exception(e)

            except Exception as e:
                e = f"Bad export format {self.cfg['format']}: {e}"
                raise Exception(e)

        except Exception as e:
            e = f"Bad {self.name} configuration: {e}"
            raise Exception(e)

        create_dirs((self.cfg['path'], self.cfg['failPath']))
        return self.cfg

    def export(self, parcel: str):
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


        self._filename += 1
        with open(f"{self.cfg['path']}{self._filename}.{self.cfg['extension']}", mode='a') as f:
            f.write(parcel)

    def delete(self, refList: list):
        """Delete not supported by this Exporter"""
        ...
        # for ref in refList:
        #     try:
        #         os.remove(f"{self.cfg['path']}{self._filename}.{self.cfg['extension']}")
        #     except Exception as e:
        #         self.log.warning(f'')
