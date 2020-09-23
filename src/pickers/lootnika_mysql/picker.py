from lootnika import time, traceback, Logger
from taskstore import Document, TaskStore
from core import scheduler
from factory import Factory
from conf import cfg

import mysql.connector as mySqlCntr
from mysql.connector import errorcode


class Picker:
    # TODO create exporter in scheduler
    def __init__(self, taskId: int, name: str, task: dict, log: Logger, taskStore: TaskStore):
        """
        Initialization

        :param taskId: datastore._mark_task_start()
        :param name: task section name
        :param task: task section
        :param log: conf.create_task_logger()
        :param taskStore: TaskStore interface
        """
        self.type = "lootnika_mysql"
        self.taskName = name
        self.taskId = taskId
        self.ts = taskStore
        self.task = task
        self.log = log

        # [total ,seen, new, differ, delete, task error, export error, last doc id]
        self.syncCount = [-1, 0, 0, 0, 0, 0, 0, '']

        # self.factory, как и Datastore, работает в своём потоке и имеет свою очередь.
        # Документы из очереди он сразу добавляет в adds, которые отправляет по достижении лимита
        # (BatchSize) или если в очереди будет команда send. Отдельный поток и очередь позволяют
        # сразу формировать adds по ходу накопления документов, а не копить\таскасть список.
        self.factory = Factory(name, log, cfg['exporters'][task['exporter']], self.syncCount)

    def is_terminated(self) -> bool:
        if scheduler.status == 'pause':
            self.log.info('Task paused')
            scheduler.check_point(self.taskId, self.syncCount, 'pause')
            while scheduler.status == 'pause':
                time.sleep(1)

            # pause может сменить stop
            if scheduler.status == 'cancel':
                self.log.warning('Task is interrupted by the user')
                scheduler.check_point(self.taskId, self.syncCount, 'cancel')
                return True
            else:
                self.log.info('Task resumed')
                return False

        elif scheduler.status == 'work':
            return False
        elif scheduler.status == 'cancel':
            self.log.warning('Task is interrupted by the user')
            scheduler.check_point(self.taskId, self.syncCount, 'cancel')
            return True
        else:
            self.log.warning('Task refused. Sending collected changes')
            scheduler.check_point(self.taskId, self.syncCount, 'cancel')
            self.factory.put('--send--')
            self.factory.put('--stop--')
            self.factory.join()
            return True

    # TODO task error count +1
    def connect(self) -> mySqlCntr.connection:
        self.log.info("Connecting to source...")
        print("\n   -----------         ",
              f"\nMysql: {self.task['DBhost']}: {self.task['DBport']}",
              f"\nDataBase: {self.task['DBscheme']}",
              f"\nUser: {self.task['DBusr']}",
              "\n   -----------         \n")
        try:
            cnx = mySqlCntr.connect(
                user=self.task['DBusr'],
                password=self.task['DBpsw'],
                host=self.task['DBhost'],
                port=self.task['DBport'],
                database=self.task['DBscheme'])
            return cnx
        except mySqlCntr.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.log.error("Access denied by source")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                self.log.error("Wrong database. Does it exist?")
            else:
                self.log.error(f'Connection error: {e}')

    # TODO add selectSize param to batch retrieving fields
    def get_objects_id(self, cnx: mySqlCntr.connection, query: str) -> list:
        """
        Query selectID. Query must return only one column with name "id".
        :return: list with objects ID that you use in select query to get fields
        """
        cur = cnx.cursor()
        self.log.debug(query)
        try:
            cur.execute(query, )
            rows = cur.fetchall()
            if not rows:
                return []
            else:
                return [item[0] for item in rows]

        except NameError as err:
            self.log.error(str(err))
        finally:
            cur.close()

    def sql_parse(self, cnx: mySqlCntr.connection, fields: dict, task: dict) -> list:
        def do_select(subSelect, fields, fieldsRow, gen, subS, subR):
            while True:  # для повтора с изм запросом при пустом возрате
                try:
                    cur.execute(subSelect)
                except Exception as e:
                    self.log.error(f"Fail to execute query: {e}")
                    return

                try:
                    rows = cur.fetchall()
                except MemoryError:  # для кривых запросов в млрд строк
                    cur.close()
                    self.log.error("Not enough memory to fetch rows. Simplify your query")
                    cur.close()
                    return

                curDes = cur.description
                if not rows:
                    if task['NotNullRows']:
                        # таким образом я всегда получаю строку, даже если запрос ничего не вернёт.
                        self.log.warning('Query has returned empty row. Will replaced with <None>')
                        noneStr = ''  # make_doc() отсеит доку, если в reference попадёт @

                        for i in curDes:
                            noneStr += f" '@null@' as {i[0]},"
                        subSelect = f'SELECT{noneStr[:-1]}'
                        # print('!#newSelect',subSelect)

                        del noneStr
                        continue
                    else:
                        break
                else:
                    for row in rows:
                        for col, el in enumerate(row):
                            if el is not None:
                                # 6 лет прошло, а они это так и не фиксят ><
                                # MySQLCursor Bug #64392
                                colName: str = curDes[col][0]
                                if isinstance(colName, bytes):
                                    colName = colName.decode('utf-8')

                                if subS == 0 and len(rows) < 2:
                                    fields[colName] = el
                                elif subS > 0 and len(rows) < 2:
                                    # уходит в тело данной ветви, чтобы можно было
                                    # подставлять в след. запросы этой ветви
                                    fieldsRow[colName] = el
                                else:
                                    # множество строк уходит в массив и не
                                    # принимают участие в последующих запросах
                                    subfields[colName] = el

                        if subfields != {}:
                            subfieldsList.append(subfields.copy())

                    if subfieldsList != [] and subS < 1:
                        fields[f'subfields{gen}'] = subfieldsList.copy()
                    elif subfieldsList != [] and subS > 0:
                        fields[f'subfields{gen}/{subS}-{subR}'] = subfieldsList.copy()
                break
            subfieldsList.clear()
            subfields.clear()
            return fields

        cur = cnx.cursor()
        for gen, select in enumerate(task['selectList']):
            subfields = {}  # для подзапросов данной ветви
            subfieldsList = []
            for subS, subSelect in enumerate(select):
                # подстановка в шаблон
                for i in fields:  # значения основной ветви
                    subSelect = subSelect.replace(f'@{i}@', str(fields[i]), -1)

                if subS > 0:
                    for subR, fieldsRow in enumerate(fields[f'subfields{gen}']):
                        subSelect0 = subSelect
                        for p in fieldsRow:  # значения данной ветви подзапросов
                            subSelect0 = subSelect0.replace(f'@{p}@', str(fieldsRow[p]), -1)

                        self.log.debug(f"{subSelect0}")
                        fields = do_select(subSelect0, fields, fieldsRow, gen, subS, subR)
                        # print('!#fields', fields)
                else:
                    self.log.debug(f"{subSelect}")
                    fields = do_select(subSelect, fields, '', gen, subS, '')

                    if fields is None:
                        raise Exception('Failed to get an object')
                    # print('!#fields',fields)
        if fields != {}:
            cur.close()
            return fields

    def delete(self):
        refList = self.ts.delete_unseen()
        if refList:
            self.syncCount[4] = len(refList)
            self.factory.send_delete(refList)

    def run(self):
        self.log.info(f"Task is running")
        if self.is_terminated():
            return

        try:
            cnx = self.connect()
            if cnx is None:
                self.log.error('Fail to create query cursor')
                return

            if self.ts.cnx is None:
                self.log.error('Fail to create taskstore')
                return

            if not self.ts.prepare():
                self.log.error(f'Fail to update taskstore {self.taskName}.db')
                return

            if self.is_terminated():
                return

            self.log.info('Retrieving objects ID list')
            try:
                idList = self.get_objects_id(cnx, self.task['selectID'])
                self.syncCount[0] = len(idList)
                self.log.info(f'Retrieved {self.syncCount[0]} objects ID')
                scheduler.check_point(self.taskId, self.syncCount)
            except Exception as e:
                self.log.error(f'No objects ID: {e}')
                return

            if self.is_terminated():
                return

            for ongo, i in enumerate(idList):
                ongo += 1
                self.log.info('Receive ID %s (%s of %s)' % (i, ongo, self.syncCount[0]))
                fields = self.sql_parse(cnx, {'id': i}, self.task)

                try:
                    doc = Document(self.taskName, self.task['docRef'], fields)
                except Exception as e:
                    self.log.error(f"Fail to create reference for object with ID={fields['id']}: {e}")
                    self.syncCount[5] += 1
                    continue

                check = self.ts.check_document(doc.reference, doc.get_hash())
                if check == 1:
                    self.syncCount[3] += 1
                    self.factory.put(doc)
                elif check == 2:
                    self.syncCount[2] += 1
                    self.factory.put(doc)
                elif check == -1:
                    self.syncCount[5] += 1
                else:
                    pass

                # засчитывать документ только после его получения
                self.syncCount[1] += 1
                self.syncCount[7] = i

                # realtime ни к чему
                # TODO пусть этим занимается планировщик, там же задать частоту
                if ongo % 100 == 0:
                    scheduler.check_point(self.taskId, self.syncCount)

                if self.is_terminated():
                    return

            scheduler.check_point(self.taskId, self.syncCount)
            if self.is_terminated():
                return

            self.factory.put('--send--')
            self.delete()

            scheduler.check_point(self.taskId, self.syncCount)
            self.factory.put('--stop--')
            self.factory.join()

        except Exception as e:
            if self.log.level == 10:
                e = traceback.format_exc()
            self.log.error(f'An error happened on task running: {e}')
            scheduler.check_point(self.taskId, self.syncCount, 'fail')
