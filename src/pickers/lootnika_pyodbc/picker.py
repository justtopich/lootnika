from lootnika import time, traceback, Logger
from taskstore import Document, TaskStore
from core import scheduler, ExportBroker

import pyodbc


class Picker:
    def __init__(self, taskId: int, name: str, task: dict, log: Logger,
                 taskStore: TaskStore, factory: ExportBroker, syncCount: list):
        """
        Initialization

        :param taskId: datastore._mark_task_start()
        :param name: task section name
        :param task: task section
        :param log: conf.create_task_logger()
        :param taskStore: TaskStore interface
        """
        self.type = "lootnika_pyodbc"
        self.taskName = name
        self.taskId = taskId
        self.ts = taskStore
        self.task = task
        self.log = log
        self.factory = factory
        self.syncCount = syncCount

    def is_terminated(self) -> bool:
        if scheduler.status == 'pause':
            self.log.info('Task paused')
            scheduler.check_point(self.taskId, 'pause')
            while scheduler.status == 'pause':
                time.sleep(1)

            # pause может сменить stop
            if scheduler.status == 'cancel':
                self.log.warning('Task is interrupted by the user')
                scheduler.check_point(self.taskId, 'cancel')
                return True
            else:
                self.log.info('Task resumed')
                return False

        elif scheduler.status == 'work':
            return False
        elif scheduler.status == 'cancel':
            self.log.warning('Task is interrupted by the user')
            scheduler.check_point(self.taskId, 'cancel')
            return True
        else:
            self.log.warning('Task refused. Sending collected changes')
            scheduler.check_point(self.taskId, 'cancel')
            # self.factory.put(self.taskId, '--send--')
            # self.factory.put(self.taskId, '--stop--')
            self.factory.join()
            return True

    def connect(self) -> pyodbc.Connection:
        self.log.info("Connecting to source...")
        try:
            cnx = pyodbc.connect(self.task['cnxString'])
            # cnx = pyodbc.connect("")
            return cnx
        except pyodbc.Error as e:
            self.syncCount[5] += 1
            self.log.error(f'Connection error: {e}')

    def get_objects_id(self, cnx: pyodbc.Connection, query: str) -> list:
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
                return [i[0] for i in rows]

        except NameError as err:
            self.log.error(str(err))
        finally:
            cur.close()

    def sql_parse(self, cnx: pyodbc.Connection, lootId) -> dict:
        """
        Выполнение запросов

        :param cnx: current cnx
        :param lootId: document identifier from source
        """
        def parse_rows(select:str, fetchOne=False, group=False) -> [dict]:
            """
            Разбор строк. Каждая строка переводится в словарь.

            :param select: сам запрос
            :param fetchOne: заберёт одну строку, вернёт один словарь
            :param group: если придёт >1 строк, то упакует в один словарь,
                т.е. каждое поле будет содержать массив значений.
            :return: список со словарями, каждый со своим набором полей
            """
            def row_as_dict(cur, rows):
                columns = [column[0] for column in cur.description]
                for row in rows:
                    yield dict(zip(columns, row))

            try:
                self.log.debug(select)
                cur.execute(select)
            except Exception as e:
                self.log.error(f"Fail to execute query: {e}")
                self.syncCount[5] += 1
                return [{}]

            try:
                if fetchOne:
                    rows = cur.fetchone()
                else:
                    rows = cur.fetchall()
            except MemoryError:  # для кривых запросов в млрд строк
                self.log.error("Not enough memory to fetch rows. Simplify your query")
                self.syncCount[5] += 1
                cur.close()
                return [{}]

            if not rows:
                if not self.task['skipEmptyRows']:
                    # таким образом я всегда получаю строку, даже если запрос ничего не вернёт.
                    self.log.warning('Query has returned empty row. Will replaced with <None>')
                    body = {}
                    try:
                        curDes = cur.description
                        for col in curDes:
                            body[col[0]] = None

                    except Exception as e:
                        self.syncCount[5] += 1
                        self.log.error(f'Fail to parse emtpy row: {e}')
                    finally:
                        return [body]


            if fetchOne:
                return [dict(zip([column[0] for column in cur.description], rows))]
            else:
                rows = row_as_dict(cur, rows)

            ls = []
            groupBody = {}
            try:
                isFirst = True
                for row in rows:
                    body = {}
                    for col, val in row.items():
                        if val is not None:
                            # TODO allow get null value?
                            if group:
                                if isFirst:
                                    groupBody[col] = [val]
                                else:
                                    try:
                                        groupBody[col].append(val)
                                    except KeyError:
                                        groupBody[col] = [val]
                                    except AttributeError:
                                        groupBody[col] = [groupBody[col], val]
                            else:
                                body[col] = val

                    isFirst = False
                    if not group:
                        ls.append(body)
                if group:
                    ls.append(groupBody)
                return ls
            except Exception as e:
                self.log.error(f'Fail to parse row: {e}')
                self.syncCount[5] += 1
                return [{}]

        cur = cnx.cursor()
        fields = {}

        for select in self.task['simpleQuery']:
            select = select.replace('@loot_id@', str(lootId), -1)

            for i in fields:
                select = select.replace(f'@{i}@', str(fields[i]), -1)
            fields = {**fields, **parse_rows(select, fetchOne=True)[0]}

        # вложенные запросы
        for bundle in self.task['bundleQuery']:
            for name, selectList in bundle.items():
                select = selectList[0].replace('@loot_id@', str(lootId), -1)
                for i in fields:
                    select = select.replace(f'@{i}@', str(fields[i]), -1)

                subFields = parse_rows(select)
                if subFields:
                    fields[name] = []

                    if len(selectList) > 1:
                        for sub in subFields:
                            for select in selectList[1:]:
                                select = select.replace('@loot_id@', str(lootId), -1)

                                for i in sub:
                                    select = select.replace(f'@{i}@', str(sub[i]), -1)
                                for i in fields:
                                    select = select.replace(f'@{i}@', str(fields[i]), -1)

                                sub = {**sub, **parse_rows(select, group=False)[0]}
                            fields[name].append(sub)
                    else:
                        fields[name].extend(subFields)
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

            self.log.info('Retrieving objects ID')
            try:
                idList = self.get_objects_id(cnx, self.task['selectID'])
                self.syncCount[0] = len(idList)
                self.log.info(f'Retrieved {self.syncCount[0]} objects ID')
                scheduler.check_point(self.taskId)
            except Exception as e:
                self.log.error(f'No objects ID: {e}')
                self.syncCount[5] += 1
                return

            if self.is_terminated():
                return

            for ongo, i in enumerate(idList):
                ongo += 1
                self.log.info(f'Receive {i} ({ongo}/{self.syncCount[0]})')
                fields = self.sql_parse(cnx, i)

                try:
                    doc = Document(self.taskId, self.taskName, self.task['docRef'], str(i), fields)
                except Exception as e:
                    self.log.error(f"Fail to create reference for object with ID={fields['id']}: {e}")
                    self.syncCount[5] += 1
                    continue

                check = self.ts.check_document(doc.reference, doc.get_hash())
                if check == 1:
                    self.syncCount[3] += 1
                    self.factory.put(self.taskId, doc)
                elif check == 2:
                    self.syncCount[2] += 1
                    self.factory.put(self.taskId, doc)
                elif check == -1:
                    self.syncCount[5] += 1
                else:
                    pass

                # засчитывать документ только после его получения
                self.syncCount[1] += 1
                self.syncCount[7] = i

                # realtime ни к чему
                if ongo % 100 == 0:
                    scheduler.check_point(self.taskId)

                if self.is_terminated():
                    return

            scheduler.check_point(self.taskId)
            if self.is_terminated():
                return

            # self.factory.put(self.taskId, '--send--')
            self.delete()

            scheduler.check_point(self.taskId)
            # self.factory.put(self.taskId, '--stop--')
            # self.factory.join()

        except Exception as e:
            self.syncCount[5] += 1
            if self.log.level == 10:
                e = traceback.format_exc()
            self.log.error(f'An error happened on task running: {e}')
            scheduler.check_point(self.taskId, 'fail')
