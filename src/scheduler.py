from lootnika import (
    time, dtime,
    Timer,
    traceback)
from conf import log
from core import selfControl, shutdown_me, ds


class Scheduler:
    """
    Следит за командами управления заданиями и вывзывает их исполнителей
    collector. Сборщики делают задания из под work_manager - он же работает
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
            Пауза проверяется в самом исполнителе задания в Collector\n
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

    def __init__(self, taskList, taskCycles, repeatMin, startTime):
        # super(Scheduler, self).__init__()
        self.taskList = taskList
        self.taskCycles = taskCycles
        self.repeatMin = repeatMin  # время повторов
        self.startTime = startTime  # времени старта заданий
        self.status = 'ready'
        self.workers = []
        self.curTask = ''
        self.LootPicker = None
        self.cmd = ''

    def _mark_task_start(self, taskName: str) -> int:
        startTaskTime = dtime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        log.info(f'Start task {taskName}')
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

    # TODO get count of factory fails
    def check_point(self, taskId: str, syncCount: list, status: str = 'run') -> None:
        """
        Task running progress updating. Statistics are saving in lootnika datastore.

        :param taskId: that given you by schedule
        :param syncCount: [total ,seen, new, differ, delete, task error, send error, last doc id]
        :param status: current status. Use one of: pause|cancel|work|fail
        """
        for n, i in enumerate(syncCount):
            if i is None: syncCount[n] = 'null'

        resMem = ds.execute(
            "UPDATE tasks SET end_time='{}', status='{}' ,count_total={}, count_seen={},"
            " count_new={}, count_differ={}, count_delete={}, count_task_error={},"
            "count_send_error={}, last_doc_id='{}' WHERE id={}"
                .format(dtime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), status,
                        syncCount[0], syncCount[1], syncCount[2], syncCount[3],
                        syncCount[4], syncCount[5], syncCount[6], syncCount[7],
                        taskId)
        )
        if resMem != 0:
            raise Exception(f'Failed to create an entry in taskstore: {resMem}')

    # вызывает исполнителя
    def work_manager(self, task='', lastTask='', cmd=False):
        # проверка выполняется тут, т.к. запускается по таймеру и статус может поменяться
        self.update_startTime()
        log.warning(f'Previous task is still running. Next start will be at {self.startTime}')
        if not (self.status == 'ready' or self.status == 'wait'):
            return

        self.status = 'work'  # он должен работатьт только при ready
        if self.taskCycles > 0:
            self.taskCycles -= 1
        # if self.taskCycles==0: self.startTime = None

        # task может быть только при cmd=True
        if task != '':
            self.curTask = task[0]
            taskId = self._mark_task_start(task[0])
            try:
                lootPicker = self.LootPicker(taskId, task[0], task[1])
                lootPicker.run()
            except Exception as e:
                if log.level == 10:
                    e = traceback.format_exc()
                log.error(f"Scheduler: {e}")
        else:
            if not cmd:
                log.info('New tasks cycle')
            else:
                log.info('Start all tasks')

            for i in self.taskList:
                # в случае отмены не продолжать
                if self.status == 'cancel':  # далее уже сам воркер следит даже если пауза
                    self.curTask = ''
                    self.status = 'ready'
                    return
                self.curTask = i[0]
                try:
                    taskId = self._mark_task_start(i[0])
                    lootPicker = self.LootPicker(taskId, i[0], i[1])
                    lootPicker.run()
                except Exception as e:
                    if log.level == 10:
                        e = traceback.format_exc()
                    log.error(f"Scheduler: {e}")

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
        return

    # вернёт конкретное задание или пустой кортеж
    def get_task(self, taskName: str) -> tuple:
        for i in self.taskList:
            if taskName == i[0]:
                return i
        return ()

    # обновит список активных рабочих
    def get_workers(self):
        ls = []
        for i in self.workers:
            if i.isAlive():
                ls.append(i)
            self.workers = ls[:]

    def isTaskTime(self):
        return dtime.datetime.now() >= self.startTime

    # обновит время старта, от которого считать время повтора
    def update_startTime(self):
        if self.startTime is None:
            return
        self.startTime = self.startTime + dtime.timedelta(minutes=self.repeatMin)

    def run(self, LootPicker):
        log.debug("Starting Scheduler thread")
        self.LootPicker = LootPicker

        while not selfControl.started and self.cmd != 'stop':
            time.sleep(0.2)

        while self.cmd != 'stop':
            self.get_workers()
            # print('%s >= %s is %s' %(dtime.datetime.now(), self.startTime, self.isTaskTime()))
            # message(('self.status',  self.status), clrSun)

            if self.status == 'ready':
                # если расписание не включено или всё выполнилось,
                # то переходит в ждущий режим
                if self.taskCycles > 0:
                    self.status = 'wait'
                    if self.isTaskTime():
                        ht = timer_named('work_manager', 0, self.work_manager, )
                        ht.start()
                        self.workers.append(ht)

                    # все последующие повторы отсчитываются от первого
                    else:
                        pass
            else:
                if self.taskCycles > 0:
                    if self.isTaskTime():
                        ht = timer_named('work_manager', 0, self.work_manager, )
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
        self.get_workers()
        for ht in self.workers:
            # message(ht,clrSun)
            ht.join()

        log.debug("Stopped Scheduler thread")
        return

    # интерфейс приёма команд от rest
    def execute(self, cmd, taskName=''):
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
                        task = self.get_task(taskName)
                        if task == ():
                            msg = 'task is undefined'
                        else:
                            ht = timer_named('work_manager', 0, self.work_manager, args=(task, self.curTask, True))
                            ht.start()
                            self.workers.append(ht)
                            result = 'ok'
                            msg = f'successfully started task {taskName}'
                    else:
                        ht = timer_named(
                            'work_manager', 0, self.work_manager,
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


def timer_named(name, interval, function, *args, **kwargs):
    # тот же таймер, только можно указать имя потока
    # т.к. сам таймер это тот же tread
    timer = Timer(interval, function, *args, **kwargs)
    timer.name = name
    return timer


def first_start_calc(cfg: dict, onStart=True):
    """
    расчёт времени до первого старта заданий.
    Следующие старты раситывает сам планировщик
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

    if cfg["startTask"] and taskCycles != 0 and taskList != []:
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
