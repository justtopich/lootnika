"""
Convert internal format (lootnika document) into csv.
Create parcel (final external document) for exporter.

Single row will contain all fields from one document.
One column for each field. For example:

   >>> Document
    {
    'reference': 'myDB-1',
    'taskname': 'example',
    'fields': {
        'id': 1,
        'status': 'open',
        'subfields1': [{
            'post_id': 101,
            'post_user': 44
            }]
        }
    }

Convert to:

    >>> parcel
    reference | taskname | fields.id | fields.status | fields.subfields1
    myDB-1    | example  |    1      |    open       | [{'post_id': 101,'post_user': 44}]

Converter must have:
    self.type - self name that can say about output format\n
    self.encoding - for bytearray(). Use None if you parcel is also like that

"""

from taskstore import Document


class Converter:
    def __init__(self, cfgSection: dict=None, cfgExporter: dict=None):
        """
        :param cfgSection: exporter section raw.
        :param cfgExporter: exporter validated configuration, no needed.
        """
        self.type = "csv"
        self.adds = ''
        self.header = ''
        self.isTitled = False
        try:
            self.delimiter = cfgSection["delimiter"]
            self.tailcut = 0 - len(self.delimiter)
        except:
            raise Exception("incorrect parameters in exporter section: 'delimiter'")

    def add(self, doc: Document):
        for k, v in doc.raw.items():
            if k == 'fields':
                for kk, vv in doc.raw[k].items():
                    if not self.isTitled:
                        self.header += f"{k}.{kk}{self.delimiter}"
                    self.adds += f"{vv}{self.delimiter}"
            else:
                if not self.isTitled:
                    self.header += f"{k}{self.delimiter}"
                self.adds += f"{doc.raw[k]}{self.delimiter}"

        self.adds = f"{self.adds[:self.tailcut]}\n"
        self.isTitled = True

    def get(self) -> str:
        """
        Finalyze parcel. After export, next documents
        will added to new parcel.
        :return: finished parcel. ready to export
        """
        parcel = f"{self.header[:self.tailcut]}\n{self.adds}\n\n"
        self.adds = ''
        self.header = ''
        self.isTitled = False
        return parcel
