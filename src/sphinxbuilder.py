from lootnika import (
    cityhash,
    shutil,
    os, sys,
    homeDir,
    traceback)
from datastore import Datastore
from conf import log, create_dirs


def check_rst(ds:Datastore) -> dict:
    log.debug("Check documentation sources")
    changed = False
    try:
        rows = ds.select('SELECT * FROM sphinxbuilder', )
        oldRst = {'lootnika': {'path': "docs/rst/", 'type': 'lootnika', 'rst': {} }}
        for row in rows:
            if row[1] not in oldRst:
                oldRst[row[1]] = {'rst': {}}

            oldRst[row[1]]['rst'][row[3]] = {'file': row[2], 'hash': row[4]}

        newRst = {'lootnika': {'path': "docs/rst/", 'type': 'lootnika', 'rst': {} }}
        for exporter in os.listdir(f'{homeDir}exporters'):
            path = f"exporters/{exporter}/docs/rst/"
            ls = os.listdir(f"{homeDir}{path}")
            if ls == []:
                log.warning(f"No documentation sources found for {exporter}")
                continue

            if exporter not in oldRst:
                log.info(f"Found new exporter dcos: {exporter}")
                oldRst[exporter] = {}
                changed = True

            newRst[exporter] = {'path': path, 'type': 'exporter', 'rst': {}}
            for file in ls:
                rst = f"{path}{file}"
                with open(f"{homeDir}{rst}", encoding='utf-8', mode='r') as cnt:
                    hsh = f"{cityhash.CityHash64(cnt.read())}"

                newRst[exporter]['rst'][rst] = {'file': file, 'hash': hsh}
                if rst in oldRst[exporter]['rst']:
                    if not oldRst[exporter]['rst'][rst]['hash'] == hsh:
                        changed = True
                else:
                    changed = True

        for picker in os.listdir(f'{homeDir}pickers'):
            path = f"pickers/{picker}/docs/rst/"
            ls = os.listdir(f"{homeDir}{path}")
            if ls == []:
                log.warning(f"No documentation sources found for {picker}")
                continue

            if picker not in oldRst:
                log.info(f"Found new picker dcos: {picker}")
                oldRst[picker] = {}
                changed = True

            newRst[picker] = {'path': path, 'type': 'picker', 'rst': {}}
            for file in ls:
                rst = f"{path}{file}"
                with open(f"{homeDir}{rst}", encoding='utf-8', mode='r') as cnt:
                    hsh = f"{cityhash.CityHash64(cnt.read())}"

                newRst[picker]['rst'][rst] = {'file': file, 'hash': hsh}
                if rst in oldRst[picker]['rst']:
                    if not oldRst[picker]['rst'][rst]['hash'] == hsh:
                        changed = True
                else:
                    changed = True

        exporter = "lootnika"
        path = newRst[exporter]['path']
        ls = os.listdir(f"{homeDir}{path}")
        for file in ls:
            rst = f"{path}{file}"
            with open(f"{homeDir}{rst}", encoding='utf-8', mode='r') as cnt:
                hsh = f"{cityhash.CityHash64(cnt.read())}"

            newRst[exporter]['rst'][rst] = {'file': file, 'hash': hsh}
            if rst in oldRst[exporter]['rst']:
                if not oldRst[exporter]['rst'][rst]['hash'] == hsh:
                    changed = True
            else:
                changed = True

        if changed:
            log.warning("Found changes in documentations. Start me with <make-doc> key.")

        return newRst
    except Exception as e:
        raise Exception(f"Fail check sources for help documentation: {traceback.format_exc()}")


def snapshot(ds: Datastore, newRst: dict) -> None:
    q = "INSERT INTO sphinxbuilder (owner, name, path, hash) values "
    for owner, attr in newRst.items():
        for path, v in attr['rst'].items():
            q += f"('{owner}', '{v['file']}', '{path}', '{v['hash']}'), "

    ds.execute("DELETE FROM sphinxbuilder")
    ds.execute(q[:-2])


def sphinxecutor(newRst: dict) -> None:
    try:
        shutil.rmtree(f'{homeDir}sphinx-doc/build')
        shutil.rmtree(f'{homeDir}sphinx-doc/temp')
    except:
        pass

    try:
        create_dirs([f'{homeDir}sphinx-doc/build', f'{homeDir}sphinx-doc/temp'])
    except:
        pass

    exporters = ""
    pickers = ""
    for owner in newRst:
        if newRst[owner]['type'] == 'exporter':
            root = f"exporter_{owner}_"
            for rst in newRst[owner]['rst'].values():
                exporters += f"{root}{rst['file'].replace('.rst', '')}\n   "

        elif newRst[owner]['type'] == 'picker':
            root = f"picker_{owner}_"
            for rst in newRst[owner]['rst'].values():
                pickers += f"{root}{rst['file'].replace('.rst', '')}\n   "

    for owner in newRst:
        if owner == 'lootnika':
            owner1 = kind = ''
        else:
            owner1 = f"{owner}_"
            kind = f"{newRst[owner]['type']}_"
        for path, rst in newRst[owner]['rst'].items():
            dst = f"{homeDir}sphinx-doc/temp/{kind}{owner1}{rst['file']}"
            shutil.copyfile(f"{homeDir}{path}", dst)

            if owner == 'lootnika':
                with open(dst, encoding='utf-8', mode='r+') as f:
                    cnt = f.read()
                    f.seek(0)
                    if '{{ exporters }}' in cnt:
                        cnt = cnt.replace('{{ exporters }}', exporters)
                        f.write(cnt)
                    if '{{ pickers }}' in cnt:
                        cnt = cnt.replace('{{ pickers }}', pickers)
                        f.write(cnt)

    shutil.copyfile(f"{homeDir}sphinx-doc/conf.py", f"{homeDir}sphinx-doc/temp/conf.py")

    sys.argv.append('-M')
    sys.argv.append('html')
    sys.argv.append(f'{homeDir}sphinx-doc/temp')
    sys.argv.append(f'{homeDir}sphinx-doc/build')

    from sphinx.cmd import build

    try:
        shutil.rmtree(f'{homeDir}webui/help/html')
    except:
        pass

    shutil.move(f'{homeDir}sphinx-doc/build/html', f'{homeDir}webui/help/')


def build():
    ds = Datastore(f'{homeDir}lootnika_tasks_journal.db')
    try:
        newRst = check_rst(ds)
    except Exception as e:
        log.fatal(f"Error: fail check docs rst: {traceback.format_exc()}")

    sphinxecutor(newRst)
    snapshot(ds, newRst)
    ds.close()
