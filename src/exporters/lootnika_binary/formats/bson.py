"""
    bson serialization for Lootnika document.
    Create parcel (final external document) for exporter.
"""

from lootnika import bson
from models import Document


__version__ = "1.0.0"


class Converter:
    def __init__(self, cfgSection: dict, cfgExporter: dict):
        """
        :param cfgSection: exporter section raw.
        :param cfgExporter: exporter validated configuration, no needed.
        """
        assert cfgExporter['batchSize'] == 1, "Allow only batchSize=1"
        self.type = "bson"
        self.adds = {}

    def add(self, doc: "Document"):
        self.adds = doc.fields

    def get(self) -> bytes:
        """
        Finalyze parcel. After export, next documents
        will added to new parcel.
        :return: finished parcel. ready to export
        """
        parcel = bson.dumps(self.adds)
        self.adds.clear()
        return parcel
