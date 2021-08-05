from lootnika import (
    PICKER_TYPE,
    __version__,
    sout,
    re,
    os,
    dtime,
    UPTIME,
    DEV_MODE,
    Thread,
    asyncio,
    aioweb)
from core import shutdown_me, traceback, scheduler, ds, selfControl
from conf import (
    homeDir,
    logRest,
    get_svc_params)
from restserv import get_client_role, taskListCopy


routes = aioweb.RouteTableDef()

@routes.get('/a=getinfo', role=['query', 'admin'])
async def handler(request):
    data = {'status': 'error', 'message': ''}
    status = 500
    try:
        data['product'] = 'Lootnika data collector'
        data['picker_type'] = PICKER_TYPE
        data['version'] = __version__
        data['service_name'] = get_svc_params()[0]
        data['directory'] = homeDir
        data['client_host'] = request.remote
        data['client_role'] = get_client_role(request.remote)
        data['pid'] = selfControl.pid
        data['pid_owner'] = selfControl.pidUser
        data['status'] = 'ok'
        status = 200
    except Exception as e:
        e = str(e)
        logRest.error(e)
        data['message'] = e
    finally:
        return aioweb.json_response(data, status=status, headers={'Access-Control-Allow-Origin': '*'})

@routes.get('/a=getstatus', role=['query', 'admin'])
async def handler(request):
    data = {'status': 'error', 'message': ''}
    status = 500
    try:
        data['status'] = 'ok'
        data['uptime'] = str(dtime.datetime.now() - UPTIME).split('.')[0]
        data = {**data, **selfControl.resourcesUsage}
        status = 200
    except Exception as e:
        e = str(e)
        logRest.error(e)
        data['message'] = e
    finally:
        return aioweb.json_response(data, status=status, headers={'Access-Control-Allow-Origin': '*'})

@routes.get('/a=stop', role=['admin'])
async def handler(request):
    data = {'status': 'error', 'message': ''}
    status = 500
    try:
        if request.path_qs == '/a=stop?stop':
            for task in asyncio.Task.all_tasks():
                task.cancel()
            asyncio.get_running_loop().stop()
        else:
            Thread(name='REST', target=shutdown_me).start()
            data['status'] = 'ok'
        status = 200
    except Exception as e:
        e = str(e)
        logRest.error(e)
        data['message'] = e
    finally:
        return aioweb.json_response(data, status=status, headers={'Access-Control-Allow-Origin': '*'})

@routes.get('/favicon.ico', role=['query','admin'])
async def grl(request):
    return aioweb.FileResponse('webui/admin/html/favicon.ico')

@routes.get('/help', role=['query','admin'])
async def grl(request):
    raise aioweb.HTTPFound('/help/index.html')

@routes.get('/admin', role=['admin'])
async def handler(request):
    return aioweb.FileResponse(f'{homeDir}webui/admin/html/index.html')

@routes.get('/admin/{view:.*}', role=['admin'])
async def handler(request):
    return aioweb.FileResponse(f'{homeDir}webui/admin/html/index.html')

@routes.get('/a=schedule', role=['admin'])
async def handler(request):
    data = {'status': 'error', 'message': ''}
    args = {k.lower():v.lower() for k, v in request.rel_url.query.items()}
    try:
        try:
            cmd = args['cmd']
        except KeyError:
            raise Exception("No 'cmd' parameter")

        # TODO async method
        if cmd in ['start', 'pause', 'cancel']:
            try:
                if 'taskname' in args:
                    if re.search("[;()@$]", args['taskname'], flags=re.IGNORECASE|re.DOTALL):
                        raise Exception('Incorrect characters in taskname parameter')

                    data['status'], data['message'] = scheduler.execute(cmd, args['taskname'])
                else:
                    data['status'], data['message'] = scheduler.execute(cmd)
            except Exception as e:
                raise Exception(f'Command {cmd } is failed: {e}')

        elif cmd == 'queueinfo':
            try:
                desc = ['id','name','start_time','end_time','status','count_total',
                        'count_seen','count_new','count_differ','count_delete',
                        'count_task_error','count_export_error','last_doc_id']

                q = 'SELECT * FROM tasks'

                if 'taskname' in args:
                    names = args['taskname'].replace(",", "','", -1)
                    q = f"{q} WHERE name in ('{names}')"

                q = f"{q} ORDER BY id DESC"

                if 'limit' in args:
                    try:
                        q = f"{q} LIMIT {int(args['limit'])}"
                    except:
                        raise Exception("Wrong parameter end")
                else:
                    q = f"{q} LIMIT 50"

                if 'start' in args:
                    try:
                        q = f"{q} OFFSET {int(args['start'])}"
                    except:
                        raise Exception("Wrong parameter start")

                dbData = ds.select(q)
                data['scheduler_status'] = scheduler.status
                data['next_start_time'] = str(scheduler.startTime).split('.')[0]

                # т.к. taskCycles счётчик, то он является числом и может принимать значение
                # Infinity если задан бесконечный повтор. Некоторые такое могут не понять и
                # потому оно заменяется на -1. На самом деле -1 означает выключенное
                # расписание, потому тут так...
                if scheduler.taskCycles == -1: data['cycles_left'] = 0
                elif scheduler.taskCycles == float('Inf'): data['cycles_left'] = -1
                else: data['cycles_left'] = scheduler.taskCycles

                data['tasks'] = []
                for row in dbData:
                    task = {}
                    for n,col in enumerate(row):
                        task[desc[n]] = col
                    data['tasks'].append(task)

                data['status'] = 'ok'
                data['message'] = f"returned {len(data['tasks'])} tasks"
            except Exception as e:
                raise Exception(f'Command {cmd} is failed: {e}')

        elif cmd == 'tasksinfo':
            try:
                data['tasks'] = taskListCopy
                data['status'] = 'ok'
            except Exception as e:
                raise Exception(f'Command {cmd} is failed: {e}')
        else:
            raise Warning('Command undefined')

#        data['status'] = 'ok'
        status = 200
    except Warning as w:
        status = 400
        w = str(w)
        logRest.error(w)
        data['message'] = w

    except Exception as e:
        status = 500
        e = str(e)
        logRest.error(e)
        data['message'] = e
    finally:
        return aioweb.json_response(data, status=status, headers={'Access-Control-Allow-Origin': '*'})

@routes.get('/a=log', role=['admin'])
async def handler(request):
    def log_reader(file: str, limit: int, offset: [int, None] = None, backward: bool = False) -> (int, int, [str]):
        """
        Read a file line by line from any place to any direction

        :param file: file location
        :param limit: count of retrieving lines
        :param offset: cursor position. By default read from the end.
            -1 mean that top of the file is reached
        :param backward: read backwards

        Returns:
        current offset, current content length, list with lines
        """
        tailLines = []
        if backward:
            with open(file, 'rb') as f:
                f.seek(-2, 2)
                end = f.tell() - 1

                if offset is None:
                    offset = f.tell()
                else:
                    if offset > end:
                        offset = end
                    elif offset < 0:
                        return -1, end, []

                while len(tailLines) < limit:
                    f.seek(offset, 0)
                    try:
                        while f.read(1) != b'\n':
                            f.seek(-2, 1)
                    except OSError:
                        limit = 0
                        f.seek(0, 0)

                    offset = f.tell() - 2
                    if offset < 0:
                        offset = -1
                    tailLines.append(f.readline().decode())
            end += 2
        else:
            with open(file, 'r') as f:
                f.seek(0, 2)
                end = f.tell() - 1

                if offset is None:
                    offset = 0

                while len(tailLines) < limit:
                    if offset >= end:
                        offset = end
                        break

                    f.seek(offset, 0)
                    s = f.readline()
                    if s != '\n':
                        tailLines.append(s)

                    try:
                        if f.read(1) != '\n':
                            offset = f.tell() - 1
                    except OSError:
                        limit = 0
            # offset += 2
        return offset, end, tailLines

    data = {'status': 'error', 'message': ''}
    args = {k.lower(): v.lower() for k, v in request.rel_url.query.items()}
    status = 500
    limit = 10
    backward = True
    offset = None

    try:
        try:
            cmd = args['cmd']
        except KeyError:
            raise Exception("No 'cmd' parameter")

        if cmd == 'read':
            try:
                file = args['file']
                assert not re.search(r"[\\d/]", file, flags=re.IGNORECASE|re.DOTALL)
                file = f'logs/{file}'
            except Exception:
                raise Exception("wrong 'file' parameter")

            if 'offset' in args:
                try:
                    offset = int(args['offset'])
                except Exception:
                    raise Exception("wrong 'offset' parameter")

            if 'limit' in args:
                try:
                    limit = int(args['limit'])
                except Exception:
                    raise Exception("wrong 'limit' parameter")

            if 'backward' in args:
                if args['backward'] == 'true':
                    pass
                elif args['backward'] == 'false':
                    backward = False
                else:
                    raise Exception("wrong 'backward' parameter")

            data['offset'], data['end'], data['records'] = log_reader(file, limit, offset, backward)
        elif cmd == 'list':
            # data['files'] = [i for i in os.listdir('logs/') if i.endswith('.log')]
            data['files'] = os.listdir(f'logs/')

        elif cmd == 'get':
            try:
                file = args['file']
                assert not re.search(r"[\\d/]", file, flags=re.IGNORECASE | re.DOTALL)
            except Exception:
                raise Exception("wrong 'file' parameter")

            return aioweb.FileResponse(
                f'logs/{file}',
                chunk_size=256 * 1024,
                headers={
                    'Access-Control-Allow-Origin': '*',
                    'content-disposition': f"attachment; filename*=UTF-8''{file}"
                })
        else:
            raise Warning('Command undefined')

        data['status'] = 'ok'
        status = 200
        return aioweb.json_response(data, status=status, headers={'Access-Control-Allow-Origin': '*'})
    except Exception as e:
        e = str(e)
        logRest.error(e)
        data['message'] = e
        return aioweb.json_response(data, status=status, headers={'Access-Control-Allow-Origin': '*'})


@routes.get('/{lol}')
async def handler(request):
    data = {'status': 'error', 'message': 'action undefined'}
    return aioweb.json_response(data=data, status=404, headers={'Access-Control-Allow-Origin': '*'})


@routes.post('/{lol}')
async def handler(request):
    data = {'status': 'error', 'message': 'action undefined'}
    return aioweb.json_response(data=data, status=404, headers={'Access-Control-Allow-Origin': '*'})


@routes.get('/')
async def handler(request):
    data = {'status': 'error', 'message': 'action undefined'}
    return aioweb.json_response(data=data, status=404, headers={'Access-Control-Allow-Origin': '*'})
