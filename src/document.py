from lootnika import (
    OrderedDict,
    cityhash,
    dpath,
    time,
    uuid4,
    bson)


class SortedFields(OrderedDict):
    def __init__(self, **kwargs):
        super(SortedFields, self).__init__()

        for key, value in sorted(kwargs.items()):
            # TODO sort list?
            # TODO sort dict in lists (any _iter_)?
            if isinstance(value, dict):
                self[key] = SortedFields(**value)
            else:
                self[key] = value

    def __str__(self):
        d = dict(self)
        for k in d:
            if isinstance(d[k], SortedFields):
                d[k] = f"{d[k]}"
        return f"{d}"

    def items(self):
        for key in self.keys_sorted():
            yield key, self.get(key)

    def keys_sorted(self):
        for key in sorted(self.keys()):
            yield key

    def values(self):
        for key in self.keys_sorted():
            yield self.get(key)


class Document:
    """
    Lootnika Document. Factory can work only with this format.
    It's just json with header and body - header field "fields". "fields"
    contain all your fields and they are used for custom processing and calculating hash
    """
    def __init__(self, taskId: int, taskName: str, reference: str, loootId: str, fields: dict):
        """
        Creating document and his reference.

        :param reference: template to create reference
        :param loootId: ID of the document in the source.
            use for replacing @loot_id@ in reference if
            that's not in fields
        """
        try:
            assert isinstance(taskId, int)
            assert isinstance(taskName, str)
            assert isinstance(reference, str)
            assert isinstance(loootId, str)
            assert isinstance(fields, dict)
        except Exception:
            raise ValueError("Wrong value type")

        self.reference = reference.replace('@loot_id@', loootId, -1)
        self.uuid = f"{uuid4()}"
        self.taskId = taskId
        self.taskName = taskName
        self.create_dtm = int(time.time())
        self.export = ""
        self.format = ""
        self._preTasksDone = False
        self.fields = SortedFields(**fields)

        for k, v in fields.items():
            self.reference = self.reference.replace(f'@{k}@', f'{v}', -1)
        if '@' in self.reference:
            raise Exception(f"Missing the necessary @field@. Reference: {self.reference}")

    def get_hash(self) -> str:
        """
        calculate hash only for meta fields, not header
        """
        return f"{cityhash.CityHash64(bson.dumps(self.fields))}"

    def dumps(self) -> bytes:
        """
        return document in bson format
        """
        return bson.dumps(self.__dict__)

    def loads(self, lootBson:bytes):
        """
        load loonika document from bytes
        """
        doc: dict = bson.loads(lootBson)
        for k, v in doc.items():
            setattr(self, k, v)

        return self


    def get_field(self, path: str):
        """
        using syntax from dpath library
        dpath incorrect working with datetime types
        (issue #145 https://github.com/dpath-maintainers/dpath-python/issues/145)
        """
        # return dpath.get(self.fields, path)

        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [v.get(key) if v else None for v in val]
                else:
                    val = val.get(key)
            else:
                val = dict.get(self.fields, key)

            if not val:
                break
        return val
