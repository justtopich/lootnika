from lootnika import (
    sqlite3,
    homeDir,
    Logger,
    traceback,
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
