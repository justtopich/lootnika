from taskstore import Document
from lootnika import bson


class Converter:
    """
    Convert internal format (lootnika document) into bsonS.
    Create parcel (final external document) for exporter.
    """

    def __init__(self, cfg=None):
        """
        Converter must have:
            self.type - self name that can say about output format\n
        :param cfg: exporter section, no needed.
        """
        self.type = "bson"
        self.adds = {"DOCUMENTS": []}

    def add(self, doc: Document):
        self.adds["DOCUMENTS"].append(doc.raw)

    def get(self) -> bytes:
        """
        Finalyze parcel. After export, next documents
        will added to new parcel.
        :return: finished parcel. ready to export
        """
        parcel = bson.dumps(self.adds)
        self.adds = {"DOCUMENTS": []}
        return parcel
