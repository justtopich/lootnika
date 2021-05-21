"""
    json serialization for Lootnika document.
    Create parcel (final external document) for exporter.
"""

from taskstore import Document
from lootnika import orjson


class Converter:
    def __init__(self, cfgSection: dict=None, cfgExporter: dict=None):
        """
        Converter must have:
            self.type - self name that can say about output format\n
        :param cfgSection: exporter section raw, no needed.
        :param cfgExporter: exporter validated configuration, no needed.
        """
        self.type = "json"
        self.adds = {"DOCUMENTS": []}

    def add(self, doc: Document):
        self.adds["DOCUMENTS"].append(doc.raw)

    def get(self) -> str:
        """
        Finalyze parcel. After export, next documents
        will added to new parcel.
        :return: finished parcel. ready to export
        """
        parcel = f"{orjson.dumps(self.adds).decode()}\n\n"
        self.adds = {"DOCUMENTS": []}
        return parcel
