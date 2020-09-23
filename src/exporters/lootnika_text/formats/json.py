from taskstore import Document


class Converter:
    """
    Convert internal format (lootnika document) into text.
    Create parcel (final external document) for exporter.
    """

    def __init__(self, cfg=None):
        """
        Converter must have:
            self.type - self name that can say about output format\n
            self.encoding - for bytearray(). Use None if you parcel is also like that
        :param cfg: exporter section, no needed.
        """
        self.type = "json"
        self.encoding = 'utf-8'
        self.adds = {"DOCUMENTS": []}

    def add(self, doc: Document):
        self.adds["DOCUMENTS"].append(doc.raw)

    def get(self) -> str:
        """
        Finalyze parcel. After export, next documents
        will added to new parcel.
        :return: finished parcel. ready to export
        """
        parcel = f"{self.adds}\n\n"
        self.adds = {"DOCUMENTS": []}
        return parcel
