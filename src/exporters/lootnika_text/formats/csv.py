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

from models import Document
import csv, io


__version__ = "1.1.0"


class Converter:
    def __init__(self, cfgSection: dict=None, cfgExporter: dict=None):
        """
        :param cfgSection: exporter section raw.
        :param cfgExporter: exporter validated configuration, no needed.
        """
        self.type = "csv"
        self.rows = []
        self.header = []
        self.isTitled = False
        self.delimiter = None
        self.quotechar = '"'
        self.lineterminator = '\n'

        if "delimiter" in cfgSection:
            self.delimiter = cfgSection["delimiter"]
        if "lineterminator" in cfgSection:
            self.lineterminator = cfgSection["lineterminator"].replace('\\n', "\n", -1).replace('\\r', "\r", -1)
        if "quotechar" in cfgSection:
            self.quotechar = cfgSection["quotechar"]
        if "quoting" in cfgSection:
            d = {
                "NONE": csv.QUOTE_NONE,
                "MINIMAL": csv.QUOTE_MINIMAL,
                "ALL": csv.QUOTE_ALL}

            quoting = cfgSection["quoting"].upper()
            if quoting in d:
                self.quoting = d[quoting]
            else:
                raise Exception(
                    f"Wrong parameter quoting: {cfgSection['quoting']}."
                    f" Available: {''.join(f'{i}, ' for i in d.keys())[:-2]}")

    def add(self, doc: Document):
        row = []
        for k, v in doc.fields.items():
            if k == 'fields':
                for kk, vv in doc.fields[k].items():
                    if not self.isTitled:
                        self.header.append(f"{k}.{kk}")
                    row.append(f"{vv}")
            else:
                if not self.isTitled:
                    self.header.append(k)
                row.append(f"{doc.fields[k]}")

        self.rows.append(row)
        self.isTitled = True

    def get(self) -> str:
        """
        Finalyze parcel. After export, next documents
        will added to new parcel.
        :return: finished parcel. ready to export
        """
        with io.StringIO() as f:
            csvMan = csv.writer(
                f,
                delimiter=self.delimiter,
                quoting=csv.QUOTE_MINIMAL,
                quotechar=self.quotechar,
                lineterminator=self.lineterminator,
            )
            csvMan.writerow(self.header)
            csvMan.writerows(self.rows)
            parcel = f.getvalue()

        self.rows.clear()
        self.header.clear()
        self.isTitled = False
        return parcel
