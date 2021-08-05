"""
    json serialization for Lootnika document.
    Create parcel (final external document) for exporter.
"""

from models import Document
from lootnika import orjson


__version__ = "1.1.0"


class Converter:
    def __init__(self, cfgSection: dict=None, cfgExporter: dict=None):
        """
        Converter must have:
            self.type - self name that can say about output format\n
        :param cfgSection: exporter section raw, no needed.
        :param cfgExporter: exporter validated configuration, no needed.
        """
        self.type = "json"
        self.adds = []

    def add(self, doc: Document):
        self.adds.append(doc.fields)

    def get(self) -> str:
        """
        Finalyze parcel. After export, next documents
        will added to new parcel.
        :return: finished parcel. ready to export
        """
        parcel = f"{orjson.dumps(self.adds).decode()}\n\n"
        self.adds.clear()
        return parcel
