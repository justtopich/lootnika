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
from core import shutdown_me, traceback
from conf import (
    homeDir,
    logRest,
    get_svc_params)
from restserv import get_client_role


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
    # redirect to routes.static
    raise aioweb.HTTPFound('/help/index.html')


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
