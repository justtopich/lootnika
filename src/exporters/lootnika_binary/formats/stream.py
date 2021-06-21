"""
    bson serialization for Lootnika document.
    Create parcel (final external document) for exporter.
"""


class Converter:
    def __init__(self, cfgSection: dict, cfgExporter: dict):
        """
        :param cfgSection: exporter section raw.
        :param cfgExporter: exporter validated configuration, no needed.
        """
        assert cfgExporter['batchSize'] == 1, "Allow only batchSize=1"
        self.type = "stream"
        self.adds = b''

    def add(self, doc: "Document"):
        self.adds = doc.fields['content']

    def get(self) -> bytes:
        """
        Finalyze parcel. After export, next documents
        will added to new parcel.
        :return: finished parcel. ready to export
        """
        try:
            return self.adds
        except Exception as e:
            raise Exception(e)
        finally:
            self.adds = b''
