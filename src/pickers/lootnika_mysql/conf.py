from lootnika import configparser


defaultCfg = {
            "docRef": "myDB-@id@",
            "DBhost": "localhost",
            "DBport": "3306",
            "DBscheme": "scheme",
            "DBusr": "user",
            "DBpsw": "password",
            "NotNullRows": "False",
            "selectID": "SELECT some_uid AS id FROM table1",
            "SelectFields0": "SELECT * FROM table2 where obj_id=@id@"}

def load_config(taskName:str, config: configparser) -> dict:
    cfg = {}
    try:
        cfg['DBhost'] = config.get(taskName, "DBhost")
        cfg['DBport'] = config.getint(taskName, "DBport")
        cfg['DBscheme'] = config.get(taskName, "DBscheme")
        cfg['DBusr'] = config.get(taskName, "DBusr")
        cfg['DBpsw'] = config.get(taskName, "DBpsw")
        cfg['NotNullRows'] = config.getboolean(taskName, "NotNullRows")  # разрешить возращать пустые строки
        cfg['docRef'] = config.get(taskName, "docRef")

        if config.has_option(taskName, "selectID"):
            n = 0
            subList = []
            selectList = []
            cfg['selectID'] = config.get(taskName, "selectID").lower()
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
            cfg['selectList'] = selectList.copy()
        else:
            raise Exception('not found first SQL request. Set <selectID>')

    except Exception as e:
        e = f"Bad {taskName} configuration: {e}"
        raise Exception(e)
    return cfg
