from lootnika import (
    time, dtime, sout,
    Timer,
    Thread,
    traceback)
from conf import log, console, create_task_logger, cfg
from core import selfControl, shutdown_me, ds
from taskstore import TaskStore
from factory import Factory


# TODO причесать или пояснить всё
class Scheduler:
    """
    Следит за командами управления заданиями и вывзывает их исполнителей.
    Сборщики делают задания из под work_manager - он же работает
    в своём отдельном потоке.
    Сборщика можно вызвать напрямую через команды минуя work_manager,
    но в одно время может работать только один (смотрит статус).
    Т.к. сборщики работают через таймер, то их может быть несколько,
    потому для их отмены есть список ждущих и активных.

    status
        ready - готов к новому циклу заданий\n
        wait - ждёт время старта следующего повтора\n
        work - выполняет цикл заданий\n
        pause - планировщик приостановлен пользователем.\n
            Пауза проверяется в самом исполнителе задания в Picker\n
        cancel - остановить немедленно текущий цикл заданий если он сейчас выполняется

    cmd
        "" - нет комманды\n
        start - начать/продолжить немедленно задание/цикл\n
        pause - приостановить работу\n
        cancel - остановить немедленно текущий цикл заданий если он сейчас выполняется\n
        stop - завершить работу. Она используется только из shutdown_me()

    делать очередь нету смысла, т.к. команды должны выполняться немедленно
    c возращением результата исполнения пользователю
    """

    def __init__(self, taskList: dict, taskCycles: int, repeatMin: int, startTime: dtime):
        self.taskList = taskList
        self.taskCycles = taskCycles
        self.repeatMin = repeatMin
        self.startTime = startTime
        self.status = 'ready'
        self.workers = []
        self.curTask = ''
        self.Picker = None
        self.cmd = ''
        self.syncCount = {}  # tasks statistics, see _start_task

    def _mark_task_start(self, taskName: str) -> int:
        """
        create record in datastore

        :return: taskId
        """
        startTaskTime = dtime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        taskId = None

        try:
            resMem = ds.execute(
                f"INSERT INTO tasks values(NULL,'{taskName}', "
                f"'{startTaskTime}',NULL,'run',0,0,0,0,0,0,0,NULL)")

            if resMem != 0:
                raise Exception(f'Failed to create an entry in taskstore: {resMem}')
            for i in ds.select(
                    f"SELECT id FROM tasks WHERE name='{taskName}' AND start_time='{startTaskTime}'"):
                taskId = i[0]
                break

            if taskId is None:
                raise Exception('Fail to create taskId for this task')

            return taskId
        except Exception as e:
            if log.level == 10:
                e = f'Task start failed: {traceback.format_exc()}'
                log.error(e)
                raise Exception(e)

    def check_point(self, taskId: int, status: str = 'run') -> None:
        """
        Task running progress updating. Statistics are saving in lootnika datastore.

        :param taskId: that given by schedule
        :param status: current status. Use one of: pause, cancel, work, fail
        """
        syncCount = self.syncCount[taskId]
        for n, i in enumerate(syncCount):
            if i is None: syncCount[n] = 'null'

        resMem = ds.execute(
            "UPDATE tasks SET end_time='{}', status='{}' ,count_total={}, count_seen={},"
            " count_new={}, count_differ={}, count_delete={}, count_task_error={},"
            "count_export_error={}, last_doc_id='{}' WHERE id={}"
                .format(dtime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), status,
                        syncCount[0], syncCount[1], syncCount[2], syncCount[3],
                        syncCount[4], syncCount[5], syncCount[6], syncCount[7],
                        taskId)
        )
        if resMem != 0:
            raise Exception(f'Failed to create an entry in taskstore: {resMem}')

    def _work_manager(self, taskName: str = '', lastTask: str = '', cmd=False):
        """
        Обёртка исполнителя задания (Picker). Работает как таймер чтобы
        отложить запуск до заданного времени. Потому проверка статуса
        планировщика так же выполняется здесь.

        NOTE: сейчас планировщик сам проверяет время старта и запускает
        задание сразу
        """
        self._update_startTime()
        if not (self.status == 'ready' or self.status == 'wait'):
            log.warning(f'Previous task is still running. Next start will be at {self.startTime}')
            return

        self.status = 'work'  # он должен работатьт только при ready
        if self.taskCycles > 0:
            self.taskCycles -= 1
        # if self.taskCycles==0: self.startTime = None

        # task может быть только при cmd=True
        if taskName != '':
            self._start_task(taskName)
        else:
            if not cmd:
                log.info('New tasks cycle')
            else:
                log.info('Start all tasks')

            for taskName in self.taskList:
                # в случае отмены не продолжать
                if self.status == 'cancel':  # далее уже сам воркер следит даже если пауза
                    self.curTask = ''
                    self.status = 'ready'
                    return
                else:
                    self._start_task(taskName)

        self.curTask = ''
        if self.taskCycles > 0:
            self.status = 'wait'
        else:
            self.status = 'ready'

        if cmd:
            log.info('All tasks completed')
        else:
            if self.startTime is None:
                log.info('Tasks cycle done. Task replays are over')
            else:
                log.info(f'Tasks cycle done. Left: {self.taskCycles}')

    def _get_workers(self):
        """обновит список активных рабочих"""
        ls = [i for i in self.workers if i.isAlive()]
        # TODO or not todo?
        self.workers = ls[:]

    def _isTaskTime(self):
        return dtime.datetime.now() >= self.startTime

    def _update_startTime(self):
        """обновит время старта, от которого считать время повтора"""
        if self.startTime is None:
            return
        self.startTime = self.startTime + dtime.timedelta(minutes=self.repeatMin)

    def run(self, Picker):
        log.debug("Starting Scheduler thread")
        self.Picker = Picker

        while not selfControl.started and self.cmd != 'stop':
            time.sleep(0.2)

        while self.cmd != 'stop':
            self._get_workers()
            # print('%s >= %s is %s' %(dtime.datetime.now(), self.startTime, self._isTaskTime()))
            # message(('self.status',  self.status), clrSun)

            if self.status == 'ready':
                # если расписание не включено или всё выполнилось,
                # то переходит в ждущий режим
                if self.taskCycles > 0:
                    self.status = 'wait'
                    if self._isTaskTime():
                        ht = Thread(name='work_manager', target=self._work_manager)
                        ht.start()
                        self.workers.append(ht)
                    # все последующие повторы отсчитываются от первого
            else:
                if self.taskCycles > 0:
                    if self._isTaskTime():
                        ht = Thread(name='work_manager', target=self._work_manager)
                        ht.start()
                        self.workers.append(ht)

                elif self.taskCycles == 0:  # -1 означает выкл. расписание
                    if self.status == 'ready':
                        log.info('Tasks cycle done')

            # print('!#cycle Status', self.status)
            time.sleep(1)

        # при выходе из цикла ждёт завершения работы рабочих и отменяет таймеры
        self.status = 'stop'
        for ht in self.workers:
            # message(ht,clrRed)
            ht.cancel()
        self._get_workers()
        for ht in self.workers:
            # message(ht,clrSun)
            ht.join()

        log.debug("Stopped Scheduler thread")
        return

    def execute(self, cmd: str, taskName: str =''):
        """интерфейс приёма команд от rest"""
        result = 'error'
        msg = ''
        try:
            # print('!#cmd.status', self.status)
            if cmd == 'start':
                if self.status == 'ready' or self.status == 'wait':
                    if self.status == 'wait':
                        # чтобы исключить одновременный запуск нескольких заданий
                        if self.startTime - dtime.datetime.now() < dtime.timedelta(seconds=2):
                            msg = f"Can't start task {taskName} because another task is starting now"
                            return result, msg
                        # если мы запустили задание, пока планировщик ждал старта следующего цикла
                        # и на момент старта ещё будет выполняться наше - тогда планировщик пропустит его
                        # и будет ждать время следующего старта. Тут определённо нужна очередь.

                    if taskName != '':
                        if taskName not in self.taskList:
                            msg = 'task is undefined'
                        else:
                            ht = Thread(
                                name='work_manager',
                                target=self._work_manager,
                                args=(taskName, self.curTask, True))
                            ht.start()
                            self.workers.append(ht)
                            result = 'ok'
                            msg = f'successfully started task {taskName}'
                    else:
                        ht = Thread(
                            name='work_manager',
                            target=self._work_manager,
                            args=('', '', True))
                        ht.start()
                        self.workers.append(ht)
                        result = 'ok'
                        msg = 'successfully started all tasks'

                elif self.status == 'pause':
                    # если это наша таска, то просто возобновляем её работу
                    if taskName != self.curTask:
                        msg = f'Scheduler suspended on task {self.curTask}, ' \
                              'but you trying to resume another task, that not allowed.'
                    else:
                        self.status = 'work'
                        result = 'ok'
                        msg = f'successfully continue task {taskName}'

                elif self.status == 'work':
                    if taskName == self.curTask:
                        msg = 'this task is already running'
                    else:
                        msg = "Can't do few tasks at one time"
                else:
                    msg = 'Current task is canceling now'

            elif cmd == 'pause':
                if self.status == 'work':
                    self.status = 'pause'
                    result = 'ok'
                    msg = f'successfully paused task {self.curTask}'
                elif self.status == 'pause':
                    msg = 'Current task is already paused'
                else:
                    msg = 'No running tasks'

            elif cmd == 'cancel':
                if self.status in ['work', 'pause']:
                    self.status = 'cancel'
                    result = 'ok'
                    msg = f'successfully canceled task {self.curTask}'
                elif self.status == 'cancel':
                    msg = 'Current task is canceling now'
                else:
                    msg = 'No running tasks'

        except Exception as e:
            msg = f'Scheduler fail to execute command "start": {e}'
        finally:
            return result, msg

    def _start_task(self, taskName: str):
        self.curTask = taskName
        log.info(f'Start task {taskName}')
        try:
            lg = create_task_logger(taskName, console)
            ts = TaskStore(taskName, lg, self.taskList[taskName]['overwriteTaskstore'])
            taskId = self._mark_task_start(taskName)

            # [total ,seen, new, differ, delete, task error, export error, last doc id]
            self.syncCount[taskId] = [-1, 0, 0, 0, 0, 0, 0, '']
            cf = self.taskList[taskName]

            fc = Factory(taskName, lg, cfg['exporters'][cf['exporter']], self.syncCount[taskId])
            picker = self.Picker(taskId, taskName, cf, lg, ts, fc, self.syncCount[taskId])
            picker.run()

            tab = '\n' + '\t' * 5
            lg.info(
                f"Task done"
                f"{tab}Total objects: {self.syncCount[taskId][0]}"
                f"{tab}Seen: {self.syncCount[taskId][1]}"
                f"{tab}New: {self.syncCount[taskId][2]}"
                f"{tab}Differ: {self.syncCount[taskId][3]}"
                f"{tab}Deleted: {self.syncCount[taskId][4]}"
                f"{tab}Task errors: {self.syncCount[taskId][5]}"
                f"{tab}Export errors: {self.syncCount[taskId][6]}")

            if self.syncCount[taskId][5] != 0:
                lg.warning('Task done with some errors. Check logs')
            if self.syncCount[taskId][6] != 0:
                log.warning(
                    'Task had errors with sending documents. '
                    f'Documents that were not sent are saved in a folder {picker.factory.failPath}')

            self.check_point(taskId, 'complete')
        except Exception as e:
            if log.level == 10:
                e = traceback.format_exc()
            log.error(f"Fail with task {taskName}: {e}")


def first_start_calc(cfg: dict, onStart=True):
    """
    расчёт времени до первого старта заданий.
    Следующие старты расчитывает сам планировщик
    :param cfg:
    :param onStart:
    :return:
    """

    def delay_calc(taskStartTime):
        startTime = dtime.datetime.now()
        if taskStartTime.lower() != 'now':
            now = dtime.datetime.now()
            now = now.hour * 3600 + now.minute * 60 + now.second
            try:
                nextStart = dtime.datetime.strptime(taskStartTime, '%H:%M:%S')
                nextStart = nextStart.hour * 3600 + nextStart.minute * 60 + nextStart.second
                if now > nextStart:
                    delay = 86400 - now + nextStart  # сегодня = что прошло+время завтра до старта
                    startTime += dtime.timedelta(seconds=delay)
                    if onStart:
                        log.info(f"Tasks will start at {taskStartTime}")
                else:
                    delay = nextStart - now
                    startTime += dtime.timedelta(seconds=delay)
                    if onStart:
                        log.info(f"Tasks will start today at {taskStartTime}")
            except Exception as e:
                log.error(f'Check parameter taskStartTime: {e}. Correct format used HH:MM:SS')
                time.sleep(2)
                shutdown_me(1, '')
        return startTime

    taskStartTime = cfg["taskStartTime"]
    taskCycles = cfg["taskCycles"]
    repeatMin = cfg["repeatMin"]
    taskList = cfg['tasks']

    if cfg["startTask"] and taskCycles != 0 and taskList is not None:
        log.debug(f"Tasks count: {len(taskList)}. Tasks cycles count: {taskCycles}")
        startTime = delay_calc(taskStartTime)
    else:
        # тут расписание можно запустить лишь командой.
        # Тогда taskCycles прибавит 1
        # Он тут же начнёт задания и выполнит цикл один раз.
        # taskCycles станет 0 и закончит расписание
        startTime = None
        taskCycles = -1
        repeatMin = -1

    return startTime, taskCycles, repeatMin
