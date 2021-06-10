from lootnika import (
    sqlite3,
    homeDir,
    Logger,
    orjson,
    cityhash,
    dpath,
    traceback,
    OrderedDict,
    time,
    uuid4,
    bson,
    os)


class TaskStore:
    def __init__(self, taskName: str, log: Logger, overwrite: bool = False):
        """
        Open taskstore or create new if it doesn't exist.\n
        You must prepare taskstore before collect documents

        :param log: Use task logger
        :param overwrite: create new taskstore even if it exist
        """
        self.log = log
        self.overwrite = overwrite
        self.cnx = self._create_task_store(taskName)

    def _create_task_store(self, taskName: str) -> sqlite3.Connection:
        """
        Connector creating local DB for each task
        to store information about seen documents

        :param taskName: will create taskName.db file
        :return: None on error
        """
        if self.overwrite:
            self.log.warning(f"Taskstore will overwrite!")
            try:
                os.remove(f'{taskName}.db')
            except FileNotFoundError:
                pass
            except Exception as e:
                self.log.error(f"Fail to delete old taskstore: {e}")

        try:
            cnx = sqlite3.connect(f'{homeDir}{taskName}.db')
        except Exception as e:
            self.log.error(f"Can't open task datastore {taskName}.db: {e}")

        while True:
            fail = False
            try:
                cur = cnx.cursor()
                cur.execute('SELECT ref, hash, status FROM documents LIMIT 1')
                # row = cur.fetchone()
                cur.close()
                break
            except Exception as e:
                if fail:
                    self.log.warning(f"Incorrect task datatstore: {e}")
                    return
                else:
                    if not self.overwrite:
                        self.log.warning(f"Fail to verify taskstore: {e}")
                    fail = True

            if fail:
                if not self.overwrite:
                    self.log.warning(f"Creating new taskstore scheme")
                try:
                    cur.execute(
                        """CREATE TABLE documents (
                        ref  VARCHAR UNIQUE ON CONFLICT REPLACE,
                        hash VARCHAR,
                        status VARCHAR);""")
                    cnx.commit()
                    cur.close()
                except Exception as e:
                    self.log.error(f"Can't create task datastore {taskName}.db: {e}")
        return cnx

    def prepare(self) -> bool:
        """Mark all documents as old"""
        try:
            cur = self.cnx.cursor()
            cur.execute("UPDATE documents SET status='old'")
            self.cnx.commit()
            cur.close()
            return True
        except:
            return False

    def check_document(self, ref: str, docHash: str) -> int:
        """
        Check document for changes by hash

        :param ref: reference
        :param docHash: cityHash64 from Document.get_hash()
        :return:
            operation status that can be:
                 0 - not changed\n
                 1 - changed (differ)\n
                 2 - new\n
                -1 - error\n
        """
        status = -1
        # self.log.debug(f'Check document {ref}')
        try:
            cur = self.cnx.cursor()
            cur.execute(f"SELECT hash FROM documents WHERE ref='{ref}'")
            row = cur.fetchone()
            if row:
                if docHash == row[0]:
                    cur.executemany("INSERT INTO documents values(?,?,?)", [(ref, docHash, 'same')])
                    status = 0
                else:
                    self.log.info(f'Document {ref} has changed')
                    cur.executemany("INSERT INTO documents values(?,?,?)", [(ref, docHash, 'differ')])
                    status = 1
            else:
                self.log.info(f'Document {ref} is new')
                cur.executemany("INSERT INTO documents values(?,?,?)", [(ref, docHash, 'new')])
                status = 2

            self.cnx.commit()
            cur.close()
            return status
        except Exception as e:
            self.log.error(f'{e}')
            return status

    def delete_unseen(self) -> list:
        try:
            cur = self.cnx.cursor()
            cur.execute("SELECT ref FROM documents WHERE status='old'")
            rows = cur.fetchall()
        except Exception as e:
            if self.log.level == 10:
                e = traceback.format_exc()
            self.log.warning(f"Taskstore can't define deleted objects: {e}")

        if rows:
            try:
                cur.execute("DELETE FROM documents WHERE status='old'")
                self.cnx.commit()
                cur.close()
            except Exception as e:
                if self.log.level == 10:
                    e = traceback.format_exc()
                self.log.warning(f"Fail to erase records about deleted objects from taskstore: {e}")
            return rows


class SortedFields(OrderedDict):
    def __init__(self, **kwargs):
        super(SortedFields, self).__init__()

        for key, value in sorted(kwargs.items()):
            # TODO sort list?
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
    def __init__(self, taskName: str, reference: str, loootId: str, fields: dict):
        """
        Creating document and his reference.

        :param reference: template to create reference
        :param loootId: ID of the document in the source.
            use for replacing @loot_id@ in reference if 
            that's not in fields
        """
        try:
            assert isinstance(taskName, str)
            assert isinstance(reference, str)
            assert isinstance(loootId, str)
            assert isinstance(fields, dict)
        except Exception:
            raise ValueError("Wrong value type")

        self.reference = reference.replace('@loot_id@', loootId, -1)
        self.uuid = f"{uuid4()}"
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

        # self.raw = {
        #     'reference': self.reference,
        #     'uuid': self.uuid,
        #     'taskName': taskName,
        #     'create_dtm': self.create_dtm,
        #     'export': self.export,
        #     'format': self.format,
        #     'fields': self.fields}

    def get_hash(self) -> str:
        """
        calculate hash only for meta fields, not header
        """
        return f"{cityhash.CityHash64(bson.dumps(self.fields))}"

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
