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
    cfg,
    homeDir,
    logRest,
    get_svc_params)


routes = aioweb.RouteTableDef()


@routes.get('/a=getstatus')
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
        data['status'] = 'ok'
        status = 200
    except Exception as e:
        e = str(e)
        logRest.error(e)
        data['message'] = e
    finally:
        return aioweb.json_response(data, status=status, headers={'Access-Control-Allow-Origin': '*'})


@routes.get('/a=stop')
async def handler(request):
    data = {'status': 'error', 'message': ''}
    status = 500
    try:
        if request.path_qs == '/a=stop?stop':
            for task in asyncio.Task.all_tasks():
                task.cancel()
            loop.stop()
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


async def start_server():
    try:
        app = aioweb.Application(debug=devMode, logger=logRest, client_max_size=None)
        app.add_routes(routes)

        runner = aioweb.AppRunner(
            app,
            handle_signals=False,
            access_log=logRest,
            access_log_format='%a %s "%r" "%{Referer}i"'
        )
        await runner.setup()
        srv = aioweb.TCPSite(runner, cfg['rest']['host'], cfg['rest']['port'])
        await srv.start()

        logRest.info(f"Started at {cfg['rest']['host']}:{cfg['rest']['port']}")
        return srv, app, runner
    except Exception:
        traceback.print_exc()
        raise


async def stop_server(srv: aioweb.TCPSite, runner: aioweb.AppRunner, app: aioweb.Application):
    """
     стопит сайт, отдаёт порты, стопит AppRunner
    """
    await srv.stop()  # оповещает клиентов о закрытии сессий
    await runner.cleanup()
    await app.shutdown()


def start_me():
    try:
        loop.run_forever()
    except Exception:
        logRest.critical(f'Thread is dead by: {traceback.format_exc()}')
    finally:
        loop.run_until_complete(stop_server(srv, runner, app))
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ != "__main__":
    # TODO AppRunner вызывает свой луп, есть ли смысл в ProactorEventLoop?
    loop = asyncio.ProactorEventLoop()  # обход ограничений Windows на кол-во соединений
    asyncio.set_event_loop(loop)
    srv, app, runner = loop.run_until_complete(start_server())
