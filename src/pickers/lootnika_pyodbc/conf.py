from lootnika import configparser


defaultCfg = {
            "docRef": "myDB-@id@",
            "DBhost": "localhost",
            "DBport": "3306",
            "DBscheme": "scheme",
            "DBusr": "user",
            "DBpsw": "password",
            "skipEmptyRows": "True",
            "selectID": "SELECT some_uid AS loot_id FROM table1",
            "SelectFields0": "SELECT * FROM table2 where obj_id=@loot_id@"}

def load_config(taskName:str, config: configparser) -> dict:
    cfg = {
        'simpleQuery': [],
        'bundleQuery': []
    }
    try:
        # cfg['DBhost'] = config.get(taskName, "DBhost")
        # cfg['DBport'] = config.getint(taskName, "DBport")
        # cfg['DBscheme'] = config.get(taskName, "DBscheme")
        # cfg['DBusr'] = config.get(taskName, "DBusr")
        # cfg['DBpsw'] = config.get(taskName, "DBpsw")
        cfg['cnxString'] = config.get(taskName, "cnxString")[1:-2]
        cfg['docRef'] = config.get(taskName, "docRef")

        if config.has_option(taskName,  'skipEmptyRows'):
            cfg['skipEmptyRows'] = config.getboolean(taskName, "skipEmptyRows")  # пропускать пустые строки
        else:
            cfg['skipEmptyRows'] = defaultCfg['skipEmptyRows']

        if config.has_option(taskName, "selectID"):
            n = 0
            cfg['selectID'] = config.get(taskName, "selectID").lower()
            while True:
                try:
                    cfg['simpleQuery'].append(config.get(taskName, f"selectFields{n}".lower()))
                    n += 1
                except:
                    if n == 0:
                        raise Exception("Doesn't set selectFields0")
                    else:
                        break

            n = 0
            while True:
                subList = {}
                try:
                    bundleName = config.get(taskName, f"bundleName{n}".lower())
                    subList[bundleName] = [config.get(taskName, f"selectBundle{n}".lower())]
                except:
                    break

                m = 0
                while True:
                    try:
                        subList[bundleName].append(config.get(taskName, f"selectBundle{n}-{m}".lower()))
                        m += 1
                    except:
                        break
                n += 1
                cfg['bundleQuery'].append(subList)
        else:
            raise Exception('not found first SQL request. Set <selectID>')

    except Exception as e:
        e = f"Bad {taskName} configuration: {e}"
        raise Exception(e)
    return cfg
