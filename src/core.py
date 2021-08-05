from lootnika import (
    WORK_ANYWAY,
    time,
    signal,
    sout,
    Thread, get_threads,
    traceback,
    sys, os,
    homeDir,
    PICKER_TYPE,
    httpClient,
    PLATFORM,
    psutil,
    __version__)
from conf import (
    cfg,
    exports,
    log)
from datastore import Datastore
import sphinxbuilder

from types import ModuleType


def shutdown_me(signum=1, frame=1):
    """
    Останавливает модули в нужном порядке
    """
    log.warning(f'Lootnika stopping on {cfg["rest"]["host"]}:{cfg["rest"]["port"]}')
    if selfControl.exit:
        return

    selfControl.exit = True
    selfControl.rate = 0.3
    n = 0
    try:
        while True:
            time.sleep(0.3)
            if not bool(selfControl.myThreads):
                break

            if selfControl.myThreads['RestServer']:
                if n < 1:
                    log.debug("Stopping REST server")
                    try:
                        if cfg["rest"]["host"] in ['::1', '0.0.0.0']:
                            host = '127.0.0.1'
                        else:
                            host = cfg["rest"]["host"]

                        cnx = httpClient.HTTPConnection(host, cfg["rest"]["port"], timeout=12)
                        cnx.request(method="GET", url='/a=stop?stop')
                        cnx.getresponse()
                    except Exception:
                        pass
                    n = 1
                    continue
            elif selfControl.myThreads['Scheduler']:
                if n < 2:
                    log.debug("Stopping Scheduler thread")
                    scheduler.cmd = 'stop'
                    n = 2
            elif selfControl.myThreads['ExportBroker']:
                if n < 3:
                    exportBroker.stop()
                    n = 3
            elif selfControl.myThreads['Datastore']:
                if n < 4:
                    log.debug("Stopping Datastore thread")
                    ds.close()
                    n = 4
            else:
                break

    except Exception as e:
        log.error(f'Shutdown failed: {traceback.format_exc()}')
    finally:
        selfControl.stop = True
        log.info("Lootnika stopped")
        if not WORK_ANYWAY:
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
            'RestServer': False,
            'Scheduler': False,
            'ExportBroker': False,
            'Datastore': False}
        self.allThreads = []
        self.pid = os.getpid()
        self.pidUser =  psutil.Process(self.pid).username()
        self.resourcesUsage = {
            "cpu": 0.0
        }
        self.isVerified = False   # все модули работают
        self.started = False      # все модули запустились
        self.exit = False         # игнорит убитые модули
        self.rate = 0.5           # частота проверки
        self.start()

    def crash(self, s: str) -> bool:
        # TODO write in datastore error message
        log.critical(s)
        for i in self.myThreads:
            if not self.myThreads[i]:
                log.critical(f"Core thread {i} is dead")

        log.debug('Calling shutdown')
        Thread(name="shutdown", target=shutdown_me, args=(1, '')).start()
        return True

    def threads_names(self):
        self.allThreads.clear()
        for i in get_threads():
            self.allThreads.append(i.name)

    def resources_usage(self):
        for k,v in psutil.virtual_memory()._asdict().items():
            self.resourcesUsage[f'ram_{k}'] = v

        for k,v in psutil.swap_memory()._asdict().items():
            self.resourcesUsage[f'swap_{k}'] = v

        self.resourcesUsage['ram_lootnika_percent'] = round(psutil.Process(self.pid).memory_percent(), 2)
        self.resourcesUsage['cpu'] = psutil.cpu_percent(interval=None)

    def run(self):
        n = 1
        crash = False     # при краше нужно только обновлтяь статусы потоков
        while True:
            self.resources_usage()
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
                            log.info(f"Lootnika started - Executable version: {__version__}_{PLATFORM}")
                        else:
                            log.info(f"Lootnika started - Source version: {__version__}_{PLATFORM}")

                        log.info(f"Welcome to http://localhost:{cfg['rest']['port']}/admin")
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


def load_picker() -> ModuleType:
    try:
        module = __import__(f'pickers.{PICKER_TYPE}.picker', globals=globals(), locals=locals(), fromlist=['Picker'])
        return getattr(module, 'Picker')

    except ModuleNotFoundError as e:
        log.fatal(f"Can't initialize picker {PICKER_TYPE}: {e}")
        raise SystemExit(1)
    except AttributeError as e:
        log.fatal(f'Wrong picker initializing: {e}')
        raise SystemExit(1)
    except Exception as e:
        log.fatal(f'Fail initialize picker: {e}')
        raise SystemExit(1)


if __name__ != "__main__":
    log.debug("Starting main thread")

    selfControl = SelfControl()
    ds = Datastore(f'{homeDir}lootnika_tasks_journal.db')

    sphinxbuilder.check_rst(ds)

    from exportBroker import ExportBroker
    exportBroker = ExportBroker(logMain=log, threads=cfg['core']['handlerThreads'], exporters=cfg['exporters'])
    Thread(name='ExportBroker', target=exportBroker.run, args=()).start()
    while (False in exportBroker.workersStarted.values()):
        time.sleep(.5)

    from scheduler import Scheduler, first_start_calc
    startTime, taskCycles, repeatMin = first_start_calc(cfg['schedule'])

    # Scheduler и Picker должны видеть друг друга
    scheduler = Scheduler(cfg['schedule']['tasks'], taskCycles, repeatMin, startTime)
    Picker = load_picker()
    Thread(name='Scheduler', target=scheduler.run, args=(Picker, )).start()

    import restserv
    Thread(name='RestServer', target=restserv.start_me,).start()

    if 'run' in sys.argv:
        # захват клавиатуры возможен лишь из консоли
        signal.signal(signal.SIGTERM, shutdown_me)
        signal.signal(signal.SIGINT, shutdown_me)
        while not selfControl.exit:
            time.sleep(1)
