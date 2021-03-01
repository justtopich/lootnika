from lootnika import sqlite3, Thread, Queue, token_hex
from conf import log


class Datastore(Thread):
    """
    Локальная БД SQLlite. База задаётся через db. Основной режим - inMemory.
    Для доступа из потоков реализована очередь. Доступны execute и select.
    Execute вернёт статус выполнения. If Execute!=0: raise exception. Используется autoCommit.
    Select вернёт генератор.
    """
    def __init__(self, db:str):
        super(Datastore, self).__init__()
        log.debug(f"Starting Datastore thread")
        self.db = db
        self.name = 'Datastore'
        self.status = {}
        self.requestQ = Queue()
        self.isRestored = False
        self.isMemory = False
        self.isReady = False
        if db == ':memory:':
            log.warning('Using inMemory Datastore')
            self.isMemory = True
        self.start()

    def run(self):
        cnx = self._create_db()
        cur = cnx.cursor()
        self.isReady = True
        while True:
            try:
                req, arg, res, token = self.requestQ.get()
                # print(token, self.status[token])
                # print(token,req)
                if req == '--close--':
                    if self.status[token] == -1:
                        self.status[token] = 0
                    self.requestQ.task_done()
                    break

                elif req == '--commit--':
                    cnx.commit()
                    if self.status[token] == -1:
                        self.status[token] = 0
                    self.requestQ.task_done()
                    continue

                # print(token,'!#run-run')
                cur.execute(req, arg)
                if res:
                    for row in cur: res.put(row)
                    res.put('--no more--')
                    if self.status[token] == -1:
                        self.status[token] = 0

                self.requestQ.task_done()
            except Exception as e:
                # print(token, 'error')
                e = f'Unable to access to {self.name}: {e}'
                log.error(e)
                self.status[token] = e
                self.requestQ.task_done()

        cnx.close()
        self.requestQ.task_done()
        log.debug("Stopped Datastore thread")


    def _create_db(self) -> sqlite3.Connection:
        """
        Создание локальной бд. Восстановление с диска и флаг принудительной синхронизации
        :return:
        """
        try:
            cnx = sqlite3.connect(self.db)
        except Exception as e:
            log.critical(f"Can't open local datastore {self.db}: {e}")
            raise Exception(e)

        # при старте всегда проверка статуса прошлого завершения работы
        fail = False
        try:
            cur = cnx.cursor()
            cur.execute('SELECT self_status FROM lootnika')
        except Exception:
            if self.db != ':memory:':
                log.warning(f'Creating new tasks journal scheme')
            fail = True

        if fail:
            try:
                cur.executescript("""
                    CREATE TABLE lootnika (self_status VARCHAR);
                    CREATE TABLE tasks (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
                        name                VARCHAR  NOT NULL,
                        start_time          DATETIME,
                        end_time            DATETIME,
                        status              VARCHAR,
                        count_total         INTEGER  DEFAULT (0),
                        count_seen          INTEGER  DEFAULT (0),
                        count_new           INTEGER  DEFAULT (0),
                        count_differ        INTEGER  DEFAULT (0),
                        count_delete        INTEGER  DEFAULT (0),
                        count_task_error    INTEGER  DEFAULT (0),
                        count_export_error  INTEGER  DEFAULT (0),
                        last_doc_id         VARCHAR);
                    CREATE TRIGGER delete_till_100 INSERT ON tasks WHEN (SELECT count(*) FROM tasks)>100 
                    BEGIN
                        DELETE FROM tasks WHERE tasks.id IN (
                            SELECT id FROM tasks ORDER BY id LIMIT (SELECT count(*) - 100 FROM tasks)
                        );
                    END;
                """)
                cnx.commit()
            except Exception as e:
                log.error(f'Unable to create datastore scheme in lootnika_tasks_journal.db: {e}')

        cur.execute('SELECT self_status FROM lootnika')
        rec = cur.fetchone()
        if rec is None:
            cur.execute("INSERT INTO lootnika('self_status') VALUES ('starting lootnika')")
        elif rec and rec[0] != 'shutdown successfully':
            log.warning(f'The previous shutdown was unexpected. Last lootnika status: {rec[0]}.')
            self.isRestored = True

        cur.execute("UPDATE lootnika SET self_status='starting lootnika'")
        cnx.commit()
        cur.close()
        return cnx


    def execute(self, req:str, arg:tuple=None, res=None, token=None, mode=0):
        """
        :param req: сам запрос
        :param arg: аргумент для cur.execute()
        :param res: Queue(); для результатов для select
        :param token: random str; генерит сам
        :param mode:
        :return:
        """
        if token is None:
            token = token_hex(8)
        self.status[token] = -1
        self.requestQ.put((req, arg or tuple(), res, token,))

        if res is None:
            self.requestQ.put(('--commit--', None, None, token))

        while True:
            if self.status[token] != -1:
                if mode == 1:
                    break
                else:
                    return self.status.pop(token)


    def select(self, req:str, arg=None):
        """
        для каждого результата запроса создаётся своя очередь, а не лист - это позволяет делать асинхронный вывод:
        пока там пусто - ждёт. Как только есть что-то - отдаёт. Для этого же тут генератор.
        Запросов может быть много, потому все они попадают в общую очередь requestQ.
        Запрос выполняется в потоке заказчика, requestQ в потоке текущего класса.

        :param req: сам запрос
        :param arg: аргумент для cur.execute()
        :return:
        """

        # sout.print(req,clr='violet')
        res = Queue()
        token = token_hex(8)
        self.execute(req, arg, res, token, 1)
        # first = True
        while True:
            if self.status[token] == -1:
                continue
            elif self.status[token] == 0:
                rec = res.get()
                if rec == '--no more--':
                    res.task_done()
                    self.status.pop(token)
                    break
                yield rec
                res.task_done()
            else:
                for i in [self.status.pop(token)]: yield i


    def get_status(self):
        return self.status


    def close(self, commit=True):
        # TODO закрывать через очередь
        self.execute("UPDATE lootnika SET self_status='shutdown successfully'")
        if commit:
            self.execute('--commit--')
        else:
            log.warning("Closing Datastore without commit")
        self.execute('--close--')
