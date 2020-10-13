from lootnika import (
    sqlite3,
    homeDir,
    Logger,
    orjson,
    cityhash,
    dpath,
    traceback,
    time,
    uuid4,
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
            raise Exception("Wrong incoming type")

        self.reference = reference
        self.raw = {
            'reference': '',
            'uuid': str(uuid4()),
            'taskname': taskName,
            'create_dtm': int(time.time()),
            'exporter': '',
            'format': '',
            'fields': fields}

        self.reference = self.reference.replace(f'@loot_id@', loootId, -1)
        for i in fields:
            self.reference = self.reference.replace(f'@{i}@', str(fields[i]), -1)
            self.raw['reference'] = self.reference
        if '@' in self.reference:
            raise Exception(f"Missing the necessary @field@. Reference: {self.reference}")

    def get_hash(self) -> str:
        """
        calculate hash only for meta fields, not header
        """
        return str(cityhash.CityHash64(orjson.dumps(self.raw['fields'], option=orjson.OPT_SORT_KEYS)))

    def get_field(self, path: str):
        """
        using syntax from dpath library
        """
        return dpath.get(self.raw, f'fields/{path}')
