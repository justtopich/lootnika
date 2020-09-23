from lootnika import (
    time,
    signal,
    sout,
    Thread, get_threads,
    traceback,
    sys, os,
    homeDir,
    pickerType,
    __version__)
from conf import (
    cfg,
    log)
from datastore import Datastore


def shutdown_me(signal, frame):
    """
    ловит ctrl-C. Останавливает модули в нужном порядке
    :param signal:
    :param frame:
    :return:
    """
    log.warning(f'Lootnika stopping on {cfg["rest"]["host"]}:{cfg["rest"]["port"]}')
    if selfControl.exit:
        return

    stopping = [False, False, False]  # logging antispam
    try:
        selfControl.exit = True
        selfControl.rate = 0.3
        time.sleep(1)
        while True:
            time.sleep(0.3)
            # sout.print(selfControl.myThreads, 'red')
            if not bool(selfControl.myThreads):
                break

            if selfControl.myThreads['Scheduler']:
                if not stopping[0]:
                    stopping[0] = True
                    log.debug("Stopping Scheduler thread")
                    scheduler.cmd = 'stop'
            elif selfControl.myThreads['Datastore']:
                if not stopping[1]:
                    stopping[1] = True
                    log.debug("Stopping Datastore thread")
                    ds.close()
            else:
                break

    except Exception as e:
        log.error(f'Shutdown failed: {traceback.format_exc()}')
    finally:
        selfControl.stop = True
        log.info("Lootnika stopped")
        os._exit(1)


class SelfControl(Thread):
    """
    содержит список обязательных модулей и следит за статусом
    их работы. Так же, мониторит запуск коннектора
    """

    def __init__(self):
        log.debug("Starting SelfControl thread")
        super(SelfControl, self).__init__()
        self.name = 'SelfControl'
        self.myThreads = {
            'Scheduler': False,
            'Datastore': False}
        self.allThreads = []
        self.isVerified = False   # все модули работают
        self.started = False      # все модули запустились
        self.exit = False         # игнорит убитые модули
        self.rate = 0.5           # частота проверки
        self.start()

    def crash(self, s):
        log.critical(s)
        for i in self.myThreads:
            log.error(f"Core Thread {i} is alive: {self.myThreads[i]}")

        log.debug('Calling shutdown')
        Thread(name="shutdown", target=shutdown_me, args=(1, '')).start()
        return True

    def threads_names(self):
        self.allThreads.clear()
        for i in get_threads():
            self.allThreads.append(i.name)

    def run(self):
        n = 1
        crash = False     # при краше нужно только обновлтяь статусы потоков
        while True:
            self.threads_names()

            # for i in get_threads():
            #     sout.print(f'{i} {i.isAlive()}', 'green')
            # print('------')

            for i in self.myThreads:
                if i in self.allThreads:
                    # message(i+ ' Run',clrSun)
                    self.myThreads[i] = True
                else:
                    self.myThreads[i] = False

            # отмечает какие модули запустились
            self.isVerified = True
            for i in self.myThreads:
                if not self.myThreads[i]:
                    self.isVerified = False

            if not crash:
                # ждёт запуска всех модулей
                if not self.started:
                    if self.isVerified:
                        if sys.argv[0].lower().endswith('.exe'):
                            log.info(f"Lootnika started - Executable version: {__version__}")
                        else:
                            log.info(f"Lootnika started - Source version: {__version__}")

                        ds.execute("UPDATE lootnika SET self_status='working'")
                        self.started = True
                        self.rate = 2 # уже можно реже смотреть
                    else:
                        n += 1
                        if n == 20: # ограничение времени запуска
                            crash = self.crash('One of the modules does not work correctly')
                        elif n == 10:
                            log.warning("detected slow Lootnika startup")
                # иначе следит за их работой
                else:
                    if not self.isVerified and not self.exit:
                        crash = self.crash("One of the modules does not work correctly")

            time.sleep(self.rate)


def load_picker():
    try:
        module = __import__(f'pickers.{pickerType}.picker', globals=globals(), locals=locals(),  fromlist=['Picker'])
        return getattr(module, 'Picker')

    except ModuleNotFoundError as e:
        log.fatal(f"No picker {pickerType}. Check if a module exists in directory pickers")
        raise SystemExit(1)
    except AttributeError as e:
        log.fatal(f'Wrong picker: {e}')
        raise SystemExit(1)
    except Exception as e:
        log.fatal(f'Fail load picker: {e}')
        raise SystemExit(1)


if __name__ != "__main__":
    log.debug("Starting main thread")
    # port = cfg['rest']['port']
    # host = cfg['rest']['host']

    selfControl = SelfControl()
    ds = Datastore(f'{homeDir}lootnika_tasks_journal.db')

    from scheduler import Scheduler, first_start_calc
    startTime, taskCycles, repeatMin = first_start_calc(cfg['schedule'])

    # Scheduler и Picker должны видеть друг друга
    scheduler = Scheduler(cfg['schedule']['tasks'], taskCycles, repeatMin, startTime)
    Picker = load_picker()
    Thread(name='Scheduler', target=scheduler.run, args=(Picker, )).start()

    if 'run' in sys.argv:
        # захват клавиатуры возможен лишь из консоли
        signal.signal(signal.SIGTERM, shutdown_me)
        signal.signal(signal.SIGINT, shutdown_me)
        while not selfControl.exit:
            time.sleep(1)
