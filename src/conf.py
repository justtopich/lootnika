from lootnika import (
    logging, RotatingFileHandler,
    configparser,
    dtime, time,
    re,
    os, sys,
    homeDir,
    traceback)
import publish

__all__ = ['log', 'logRest', 'console', 'cfg', 'create_task_logger', 'create_dir']
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
    "output": {
        "format": "raw",
        "publisher": "raw2text",
        "batchSize": "100",
        "failPath": "send_failed/",
    },
    "schedule": {
        "enable": "False",
        "taskStartTime": "Now",
        "taskCycles": "-1",
        "repeatMin": "60",
        "taskCount": "1",
        "0": "example"
    },
    "example": {
        "docRef": "myDB-@id@",
        "DBhost": "localhost",
        "DBport": "3306",
        "DBscheme": "scheme",
        "DBusr": "user",
        "DBpsw": "password",
        "NotNullRows": "False",
        "selectID": "SELECT some_uid AS id FROM sheme.table1",
        "SelectFields0": "SELECT * FROM sheme.table2 where obj_id=@id@"
    },
    "logging": {
        "Enable": "True",
        "LogLevel": "Normal",
        "# Normal or Full": "",
        "LogMaxSizeKbs": "10240",
        "logMaxFiles": "5"
    }
}
cfg = {
    'diskUsage': {},
    'rest': {
        'userRole': {
            'admin': {'users': 'AdminClients', 'actions': ''},
            'query': {'users': 'QueryClients', 'actions': ''}
        }
    },
    'output': {},
    'publishers': {},
    'schedule': {}
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
        open(f"{homeDir}lootnika.cfg", encoding='utf-8')
    except IOError:
        open(f"{homeDir}lootnika.cfg", 'tw', encoding='utf-8')

    config = configparser.RawConfigParser(comment_prefixes=('//'), allow_no_value=True)
    config = lowcase_sections(config)

    try:
        config.read(f"{homeDir}lootnika.cfg")
    except Exception as e:
        print(f"Fail to read configuration file: {e}")
        time.sleep(3)
        raise SystemExit(1)
    return config


def create_dir(paths: list) -> None:
    for i in paths:
        if not os.path.exists(i):
            try:
                os.makedirs(i)
            except Exception as e:
                raise Exception(f'Fail to create dir {i}: {e}')


def write_section(section: str, params: dict) -> bool:
    def lowcaseMe(val: str) -> str:
        return val.lower()

    def config_write():
        with open(f"{homeDir}lootnika.cfg", "w") as configFile:
            config.write(configFile)

    print(f'Write section {section}')
    config.optionxform = str  # позволяет записать параметр сохранив регистр
    config.add_section(section)

    for val in params:
        config.set(section, val, params[val])

    config.optionxform = lowcaseMe  # вернёт предопределённый метод назад
    config_write()
    return True


def check_sections(config: configparser.RawConfigParser):
    edited = False
    try:
        for k in ['server', 'service', 'diskusage', 'output', 'schedule', 'logging']:
            if not config.has_section(k):
                print(f"ERROR: no section {k}")
                edited = write_section(k, default[k])
                if k == 'schedule':
                    write_section('example', default['example'])

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
        f"{homeDir}logs/main.log",
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

    log = logging.getLogger('MainApp')
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
    handler = RotatingFileHandler(f"{homeDir}logs/{taskName}.log", )
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


def verify_config(config: configparser.RawConfigParser, log: logging.Logger) -> dict:
    def verify_rest():
        try:
            cfg['rest']['host'] = config.get("server", "host")
            cfg['rest']['port'] = config.getint("server", "port")

            # используется в ресте. actions наполняется там же
            for role in cfg['rest']['userRole']:
                p = cfg['rest']['userRole'][role]['users']
                val = config.get("server", p).strip()

                if '*' in val:
                    cfg['rest']['userRole'][role]['users'] = '*'
                elif val == '' or val == ';':
                    raise Exception(f"Not set {p}")
                elif ';' not in val:
                    raise Exception(f'No delimiter ; in {p}')
                else:
                    cfg['rest']['userRole'][role]['users'] = [ip.strip() for ip in val.split(';') if ip != '']

        except Exception as e:
            log.error("incorrect parameters in [Server]: %s" % e)
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

    def verify_output():
        try:
            # TODO verify publish & format
            cfg['output']['publisher'] = config.get("output", "publisher")
            cfg['output']['format'] = config.get("output", "format")
            cfg['output']['batchSize'] = config.getint("output", "BatchSize")

            if config.has_option('output', 'failPath'):
                cfg['output']['failPath'] = config.get("output", "failPath").replace("\\", "/", -1)
                if ":" not in cfg['output']['failPath']:
                    cfg['output']['failPath'] = f"{homeDir}{cfg['output']['failPath']}"
                if not cfg['output']['failPath'].endswith("/"):
                    cfg['output']['failPath'] += "/"
            else:
                cfg['output']['failPath'] = f"{homeDir}{default['output']['failPath']}"

            os.makedirs(cfg['output']['failPath'])
        except FileExistsError:
            pass
        except Exception as e:
            log.error(f"incorrect parameters in [output]: {e}")
            time.sleep(3)
            raise SystemExit(1)

    def verify_scheduler():
        def get_task_params(ls: list) -> list:
            taskList, args = [], {}
            for taskName in ls:
                try:
                    if config.has_option(taskName, 'overwriteTaskstore'):
                        args['overwriteTaskstore'] = config.getboolean(taskName, 'overwriteTaskstore')
                    else:
                        args['overwriteTaskstore'] = False

                    args['DBhost'] = config.get(taskName, "DBhost")
                    args['DBport'] = config.getint(taskName, "DBport")
                    args['DBscheme'] = config.get(taskName, "DBscheme")
                    args['DBusr'] = config.get(taskName, "DBusr")
                    args['DBpsw'] = config.get(taskName, "DBpsw")
                    args['NotNullRows'] = config.getboolean(taskName, "NotNullRows")  # разрешить возращать пустые строки
                    args['docRef'] = config.get(taskName, "docRef")

                    if config.has_option(taskName, "selectID"):
                        n = 0
                        subList = []
                        selectList = []
                        args['selectID'] = config.get(taskName, "selectID").lower()
                        while True:
                            try:
                                subList.append(config.get(taskName, f"selectFields{n}".lower()))
                            except:
                                if n == 0:
                                    raise Exception("Doesn't set selectFields0")
                                else:
                                    break

                            m = 0
                            while True:
                                try:
                                    subList.append(config.get(taskName, f"selectFields{n}-{m}".lower()))
                                    m += 1
                                except:
                                    break
                            if subList != []:
                                selectList.append(subList[:])
                                subList.clear()
                            n += 1
                        args['selectList'] = selectList.copy()
                    else:
                        raise Exception('not found first SQL request. Set <selectID>')
                except Exception as e:
                    log.error(f"incorrect parameters in [{taskName}]: {e}")
                    time.sleep(3)
                    raise SystemExit(1)

                taskList.append((taskName, args))
            return taskList

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
                taskList = []
            else:
                ls = [config.get("schedule", str(n)).lower() for n in range(tmp["taskCount"])]
                taskList = get_task_params(ls)

            if tmp["startTask"] and taskList == []:
                raise Exception('Schedule is enabled, but no one task is active')

            cfg['schedule']['tasks'] = taskList
        except Exception as e:
            log.error(f"incorrect parameters in [Schedule]: {e}")
            time.sleep(3)
            raise SystemExit(1)

    verify_rest()
    verify_diskUsage()
    verify_output()
    verify_scheduler()
    return cfg


# TODO many endpoints
def load_publisher(cfg: dict) -> dict:
    try:
        pubName = config.get('output', 'publisher')
        pubType = config.get(cfg['output']['publisher'], 'type')

        module = __import__(f'publish.{pubType}', globals=globals(), locals=locals(),  fromlist=['Publisher'])
        Publisher = getattr(module, 'Publisher')
        publisher = Publisher(pubName)

        try:
            if not config.has_section(pubName):
                log.warning(f'Create new section {pubName}')

                if write_section(pubName, publisher.defaultCfg):
                    print("WARNING: created new sections in config file. Restart me to apply them")
                    raise SystemExit(1)
        except Exception as e:
            log.error(f"Fail to load default publisher {pubName}: {e}")

        cfg['publishers'][pubName] = publisher
        publisher.load_config(config)
        return cfg
    except ModuleNotFoundError as e:
        log.error(f"No publisher {pubName}. Check if a module exists in directory publish")
        raise SystemExit(1)
    except AttributeError as e:
        log.error(f'Wrong publisher: {e}')
        raise SystemExit(1)
    except Exception as e:
        log.error(f'Fail load publisher: {e}')
        raise SystemExit(1)


if __name__ != '__main__':
    try:
        create_dir([f"{homeDir}{'logs'}", f"{homeDir}{'temp'}"])
    except Exception as e:
        print(e)
        time.sleep(3)
        raise SystemExit(-1)

    config = open_config()
    check_sections(config)
    log, logRest, console = create_logger(config)
    cfg = verify_config(config, log)
    cfg = load_publisher(cfg)
