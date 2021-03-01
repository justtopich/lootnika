from lootnika import (
    pickerType,
    __version__,
    sout,
    dtime,
    upTime,
    devMode,
    Thread,
    asyncio,
    aioweb)
from core import shutdown_me, traceback, scheduler, ds
from conf import (
    homeDir,
    logRest,
    get_svc_params)
from restserv import get_client_role, taskListCopy


routes = aioweb.RouteTableDef()


@routes.get('/a=getstatus', role=['query', 'admin'])
async def handler(request):
    data = {'status': 'error', 'message': ''}
    status = 500
    try:
        data['product'] = 'Lootnika data collector'
        data['picker_type'] = pickerType
        data['version'] = __version__
        data['uptime'] = str(dtime.datetime.now() - upTime).split('.')[0]
        data['service_name'] = get_svc_params()[0]
        data['directory'] = homeDir
        data['client_host'] = request.remote
        data['client_role'] = get_client_role(request.remote)
        data['status'] = 'ok'
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
        return aioweb.json_response(data, status=status)


@routes.get('/help', role=['query','admin'])
async def grl(request):
    raise aioweb.HTTPFound('/help/index.html')


@routes.get('/a=schedule', role=['admin'])
async def handler(request):
    data = {'status': 'error', 'message': ''}
    args = {k.lower():v.lower() for k, v in request.rel_url.query.items()}
    try:
        try:
            cmd = args['cmd']
        except KeyError:
            raise Exception('No command found for schedule action')

        # TODO async method
        if cmd in ['start', 'pause', 'cancel']:
            try:
                if 'taskname' in args:
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

                q = 'SELECT * FROM tasks ORDER BY id DESC'

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
                if scheduler.taskCycles == -1: data['remained_cycles'] = 0
                elif scheduler.taskCycles == float('Inf'): data['remained_cycles'] = -1
                else: data['remained_cycles'] = scheduler.taskCycles

                data['tasks'] = []
                for row in dbData:
                    task = {}
                    for n,col in enumerate(row):
                        task[desc[n]] = col
                    data['tasks'].append(task)

                data['message'] = f"returned {len(data['tasks'])} tasks"
            except Exception as e:
                raise Exception(f'Command {cmd} is failed: {e}')

        elif cmd == 'tasksinfo':
            try:
                data['tasks'] = taskListCopy
            except Exception as e:
                raise Exception(f'Command {cmd} is failed: {e}')
        else:
            raise Warning('Command undefined')

        data['status'] = 'ok'
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
        return aioweb.json_response(data, status=status)




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
