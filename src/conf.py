from typing import Set, List, Union, Tuple, Dict, Any
from types import ModuleType
from lootnika import (
    sout,
    logging, RotatingFileHandler,
    configparser,
    dtime, time,
    re,
    devMode,
    os, sys,
    homeDir,
    pickerType,
    traceback)


__all__ = ['log', 'logRest', 'console', 'cfg', 'create_task_logger', 'create_dirs', 'get_svc_params']

cfgFileName = 'lootnika.cfg'
if devMode:
    cfgFileName = 'lootnika_dev.cfg'

cfg = {
    'diskUsage': {},
    'rest': {},
    'exporters': {},
    'schedule': {}
}
default = {
    "server": {
        "Host": "0.0.0.0",
        "Port": "7252",
        "AdminClients": "localhost;",
        "QueryClients": "*"
    },
    "service": {
        "; Windows Service": "",
        "Name": "Lootnika-Svc",
        "DisplayName": "Lootnika data collector",
        "Description": "Lootnika data collector"
    },
    "diskusage": {
        "# Disk free space monitoring": "",
        "pathWatch": "C:\\",
        "critFreeGb": "10"
    },
    "export": {
        "type": "lootnika_text"
    },
    "schedule": {
        "enable": "False",
        "taskStartTime": "Now",
        "taskCycles": "-1",
        "repeatMin": "60",
        "taskCount": "1",
        "0": "example",
        "tasks": "example"
    },
    "logging": {
        "Enable": "True",
        "LogLevel": "Normal",
        "# Normal or Full": "",
        "LogMaxSizeKbs": "10240",
        "logMaxFiles": "5"
    }
}


class FakeMatch:
    def __init__(self, match):
        self.match = match

    def group(self, name):
        return self.match.group(name).lower()


class FakeRe:
    def __init__(self, regex):
        self.regex = regex

    def match(self, text):
        m = self.regex.match(text)
        if m:
            return FakeMatch(m)


def lowcase_sections(parser: configparser.RawConfigParser) -> configparser.RawConfigParser:
    parser.SECTCRE = FakeRe(re.compile(r"\[ *(?P<header>[^]]+?) *]"))
    return parser


def open_config() -> configparser.RawConfigParser:
    try:
        open(f"{homeDir}{cfgFileName}", encoding='utf-8')
    except IOError:
        open(f"{homeDir}{cfgFileName}", 'tw', encoding='utf-8')

    config = configparser.RawConfigParser(comment_prefixes=(['//', '#', ';']), allow_no_value=True)
    config = lowcase_sections(config)

    try:
        config.read(f"{homeDir}{cfgFileName}")
    except Exception as e:
        print(f"Fail to read configuration file: {e}")
        time.sleep(3)
        raise SystemExit(1)
    return config


def create_dirs(paths: iter) -> None:
    for i in paths:
        if not os.path.exists(i):
            try:
                os.makedirs(i)
            except Exception as e:
                raise Exception(f'Fail to create dir {i}: {e}')


def write_section(section: str, params: dict) -> bool:
    try:
        with open(f'{homeDir}{cfgFileName}', "a") as configFile:
            configFile.write(f"\n[{section}]\n")
            for k, v in params.items():
                configFile.write(f"{k} = {v}\n")

        return True
    except Exception as e:
        print(f"Can't write to {cfgFileName}: {e}")
        return False


def check_base_sections(config: configparser.RawConfigParser) -> None:
    edited = False
    try:
        for k in ['server', 'service', 'logging', 'diskusage', 'schedule']:
            if not config.has_section(k):
                print(f"ERROR: no section {k}")
                edited = write_section(k, default[k])
                if k == 'schedule':
                    write_section('export', default['export'])

        if edited:
            print("WARNING: created new sections in config file. Restart me to apply them")
            time.sleep(3)
            raise SystemExit(1)
    except Exception as e:
        print(f"ERROR: Fail to create configuration file: {e}")
        time.sleep(3)
        raise SystemExit(1)


def create_logger(config: configparser.RawConfigParser) -> (logging.Logger, logging.Logger, logging.StreamHandler):
    level = logging.INFO
    logSize = 10240
    logCount = 5
    try:
        if not config.getboolean("logging", "enable"):
            level = 0
        else:
            logLevel = config.get("logging", "loglevel").lower()
            if logLevel == "full":
                level = logging.DEBUG

            logSize = config.getint("logging", "logmaxsizekbs")
            logCount = config.getint("logging", "logmaxfiles")
    except Exception as e:
        print("WARNING: Check parameters for Logging.", str(e))
        time.sleep(3)
        raise SystemExit(1)

    log_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    my_handler = RotatingFileHandler(
        f"{homeDir}logs/lootnika.log",
        maxBytes=logSize * 1024,
        backupCount=logCount,
        encoding='utf-8')
    my_handler.setFormatter(log_formatter)

    my_handler2 = RotatingFileHandler(
        f"{homeDir}logs/rest.log",
        maxBytes=logSize * 1024,
        backupCount=logCount,
        encoding='utf-8')
    my_handler2.setFormatter(log_formatter)

    console = logging.StreamHandler(stream=sys.stdout)  # вывод в основной поток
    console.setFormatter(log_formatter)
    console.setLevel(level)
    # logging.getLogger('root').addHandler(console)

    log = logging.getLogger('Lootnika')
    log.addHandler(my_handler)
    log.setLevel(level)
    log.addHandler(console)

    logRest = logging.getLogger('RestServer')
    logRest.addHandler(my_handler2)
    logRest.setLevel(level)
    logRest.addHandler(console)

    # disable requests logging
    logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)

    return log, logRest, console


def create_task_logger(taskName: str, console: logging.Logger) -> logging.Logger:
    logger = logging.getLogger(taskName)
    if taskName not in [i.name for i in logger.handlers]:
        handler = RotatingFileHandler(f"{homeDir}logs/{taskName}.log", )
        handler.name = taskName
        handler.setFormatter(console.formatter)
        logger.addHandler(handler)
        logger.addHandler(console)
        logger.setLevel(console.level)

    return logger


def get_svc_params() -> list:
    try:
        return [
            config.get("service", "Name"),
            config.get("service", "DisplayName"),
            config.get("service", "Description")]
    except Exception as e:
        e = f"incorrect parameters in [Service]: {e}"
        if 'log' in locals():
            log.error(e)
        else:
            print(e)
        time.sleep(3)
        raise SystemExit(1)


def verify_config(config: configparser.RawConfigParser, log: logging.Logger) -> Tuple[Dict[str, any], Set[str]]:
    def verify_rest():
        try:
            cfg['rest']['host'] = config.get("server", "host")
            cfg['rest']['port'] = config.getint("server", "port")

            # field actions is used for GetStatus action, so they filling in restserver
            acl = {
                'admin': {'users': 'AdminClients', 'actions': ''},
                'query': {'users': 'QueryClients', 'actions': ''}}

            for role in acl:
                val = (config.get('server', acl[role]['users'])).strip()
                if '*' in val:
                    acl[role]['users'] = '*'
                elif val == '' or val == ';':
                    raise Exception(f"Not set {acl[role]['users']}")
                elif ';' not in val:
                    raise Exception(f"No delimiter <;> in {acl[role]['users']}")
                else:
                    acl[role]['users'] = [ip.strip() for ip in val.split(';') if ip != '']
                    acl[role]['users'].extend(['::1', 'localhost', '127.0.0.1', cfg['rest']['host']])
                    acl[role]['users'] = set(acl[role]['users'])

            cfg['rest']['acl'] = acl
        except Exception as e:
            log.error(f"incorrect parameters in [Server]: {e}")
            time.sleep(3)
            raise SystemExit(1)

    def verify_diskUsage():
        try:
            cfg['diskUsage']['critFreeGb'] = config.getint("diskusage", "critFreeGb")
            cfg['diskUsage']['pathWatch'] = config.get("diskusage", "pathWatch")

            if ":" not in cfg['diskUsage']['pathWatch']:
                cfg['diskUsage']['pathWatch'] = f"{homeDir}{cfg['diskUsage']['pathWatch']}"

            if not os.path.exists(cfg['diskUsage']['pathWatch']):
                raise Exception('wrong directory pathWatch.')
        except Exception as e:
            log.error(f"incorrect parameters in [DiskUsage]: {e}")
            time.sleep(3)
            raise SystemExit(1)

    def verify_scheduler():
        tmp = cfg['schedule']
        try:
            tmp["startTask"] = config.getboolean("schedule", "enable")
            tmp["taskStartTime"] = config.get("schedule", "taskStartTime")
            if tmp["taskStartTime"].lower() != 'now':
                try:
                    dtime.datetime.strptime(tmp["taskStartTime"], '%H:%M:%S')
                except:
                    raise Exception('incorrect parameter taskStartTime. Use <HH:MM:SS> or <Now>')

            tmp["taskCycles"] = config.getint("schedule", "taskCycles")
            if tmp["taskCycles"] == -1:
                tmp["taskCycles"] = float('Inf')
            elif tmp["taskCycles"] < -1:
                raise Exception('incorrect parameter taskCycles')

            tmp["repeatMin"] = config.getint("schedule", "repeatMin")
            if tmp["repeatMin"] < 1:
                raise Exception('incorrect parameter repeatMin')

            tmp["taskCount"] = config.getint("schedule", "taskCount")
            if tmp["taskCount"] < 0:
                raise Exception('incorrect parameter taskCount')
            elif tmp["taskCount"] == 0:
                tmp['tasks'] = None
            else:
                tmp['tasks'] = {}
                for n in range(tmp["taskCount"]):
                    tmp['tasks'][config.get("schedule", str(n + 1)).lower()] = {}

            # tasks = config.get("schedule", 'tasks')
            # if tasks == '':
            #     tmp['tasks'] = None
            # else:
            #     tmp['tasks'] = {}
            #     for n in tasks.split(','):
            #         tmp['tasks'][n.strip()] = {}

            if tmp["startTask"]:
                if tmp['tasks'] is None:
                    raise Exception('Schedule is enabled, but no one task is active')
                elif tmp["taskCycles"] == 0:
                    raise Exception('Schedule is enabled, but taskCycles = 0')

        except Exception as e:
            log.error(f"incorrect parameters in [Schedule]: {e}")
            time.sleep(3)
            raise SystemExit(1)

    def verify_tasks() -> Set[str]:
        """
        Any Pickers can have options:
            - export
            - overwritetaskstore

        :return: set of tasks exports
        """
        try:
            module = __import__(
                f'pickers.{pickerType}.conf',
                globals=globals(),
                locals=locals(),
                fromlist=['load_config', 'defaultCfg'])

            load_config = getattr(module, 'load_config')
            defaultCfg = getattr(module, 'defaultCfg')

        except ModuleNotFoundError as e:
            log.fatal(f"No picker {pickerType}. Check if a module exists in directory pickers")
            raise SystemExit(1)
        except AttributeError as e:
            log.fatal(f'Wrong picker: {e}')
            raise SystemExit(1)
        except Exception as e:
            log.fatal(f'Fail load picker: {e}')
            raise SystemExit(1)

        if cfg['schedule']['tasks'] is None:
            log.warning("Lootnika have no tasks")
            return set()

        exports = []
        for taskName in cfg['schedule']['tasks']:
            if not config.has_section(taskName):
                log.warning(f'Not found task section {taskName}')

                if write_section(taskName, defaultCfg):
                    log.error("created new sections in config file. Restart me to apply them")
                    time.sleep(3)
                    raise SystemExit(1)

            try:
                task = load_config(taskName, config)

                if config.has_option(taskName, 'overwriteTaskstore'):
                    task['overwriteTaskstore'] = config.getboolean(taskName, 'overwriteTaskstore')
                else:
                    task['overwriteTaskstore'] = False

                task['transformTasks'] = []
                if config.has_option(taskName, 'transformTasks'):
                    val = config.get(taskName, 'transformTasks').strip()

                    if val == '' or val == ';':
                        raise Exception("Not set transformTasks")
                    elif ';' not in val:
                        raise Exception("No delimiter <;> in transformTasks")
                    else:
                        for el in val.split(';'):
                            if el != '':
                                task['transformTasks'].append(el.strip())

                exp = config.get(taskName, 'export')
                if exp == '':
                    exp = []
                else:
                    exp = [n.strip() for n in exp.split(',')]

                if config.has_option(taskName, 'defaultExport'):
                    task['defaultExport'] = config.get(taskName, 'defaultExport')
                else:
                    if len(exp) > 1:
                        task['defaultExport'] = config.get(taskName, 'defaultExport')
                    else:
                        task['defaultExport'] = exp[0]
                
                task['export'] = exp
                exports.extend(exp)
                cfg['schedule']['tasks'][taskName] = task
            except Exception as e:
                log.error(f"incorrect parameters in [{taskName}]: {e}")
                time.sleep(3)
                raise SystemExit(1)

        return set(exports)

    verify_rest()
    verify_diskUsage()
    verify_scheduler()
    exports = verify_tasks()
    return cfg, exports


def load_exporter(name: str) -> dict:
    """
    load exporters what collected in verify_tasks

    :param name: exporter section. Default is "export"
    """
    log.debug(f"Enabled exporter: {name}")
    try:
        expType = config.get(name, 'type')

        module = __import__(f'exporters.{expType}.exporter', globals=globals(), locals=locals(),  fromlist=['Exporter'])
        Exporter = getattr(module, 'Exporter')
        exporter = Exporter(name)

        # нужен если указан в задаче, а его нет
        try:
            if len(config.items(name)) == 1:
                log.warning(f'Create new section {name}')

                if write_section(name, {**{'type': expType}, **exporter.defaultCfg}):
                    print("WARNING: created new sections in config file. Restart me to apply them")
                    raise SystemExit(1)
        except Exception as e:
            log.error(f"Fail to load exporter {name}: {e}")

        cfg['exporters'][name] = exporter
        exporter.load_config(config)
        return cfg
    except ModuleNotFoundError as e:
        log.fatal(f"No exporter {name}. Check if a module exists in directory exporters")
        raise SystemExit(1)
    except AttributeError as e:
        log.fatal(f'Wrong exporter: {e}')
        raise SystemExit(1)
    except Exception as e:
        log.fatal(f'Fail load exporter: {e}')
        raise SystemExit(1)


if __name__ != '__main__':
    try:
        create_dirs([
            f"{homeDir}{'logs'}",
            f"{homeDir}{'temp'}",
            f"{homeDir}{'temp'}",
            f"{homeDir}{'sphinx-doc'}",
        ])
    except Exception as e:
        print(e)
        time.sleep(3)
        raise SystemExit(-1)

    config = open_config()
    check_base_sections(config)
    log, logRest, console = create_logger(config)
    log.info(f"starting...")
    cfg, exports = verify_config(config, log)

    for i in exports:
        cfg = load_exporter(i)
