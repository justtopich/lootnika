"""
    bson serialization for Lootnika document.
    Create parcel (final external document) for exporter.
"""

from taskstore import Document
from lootnika import bson


class Converter:
    def __init__(self, cfgSection: dict=None, cfgExporter: dict=None):
        """
        :param cfgSection: exporter section raw.
        :param cfgExporter: exporter validated configuration, no needed.
        """
        self.type = "bson"
        self.adds = {"DOCUMENTS": []}

    def add(self, doc: Document):
        self.adds["DOCUMENTS"].append(doc.fields)

    def get(self) -> bytes:
        """
        Finalyze parcel. After export, next documents
        will added to new parcel.
        :return: finished parcel. ready to export
        """
        parcel = bson.dumps(self.adds)
        self.adds = {"DOCUMENTS": []}
        return parcel
