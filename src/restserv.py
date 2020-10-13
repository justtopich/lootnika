from lootnika import (
    homeDir,
    devMode,
    asyncio,
    aioweb)
from core import traceback
from conf import (
    cfg,
    logRest)


class ACLpolicy:
    """
    Dirt hack for custom authorization, NOT authentication!
    Allow access by client address.

    aioweb.RouteTableDef() resent **kwargs when add a route,
    but finally aioweb don't allow unknown args. So, ACLpolicy
    picks them before aioweb.
    If route don't have role, ACLpolicy giving access for
    everyone.

    """
    def __init__(self, routers: aioweb.RouteTableDef, acl: dict):
        """
        Load ACL policy from routes

        :param routers: must have arg role with list of the roles
        :param acl: contain roles with list of the clients.
        """
        self.acl = acl
        self.routeRoles = {}
        for route in routers._items:
            if 'role' in route.kwargs:
                try:
                    self.routeRoles[route.path] = set(route.kwargs['role'])
                    del route.kwargs['role']
                except:
                    logRest.critical(f'fail to set role for {route.path}')
        # for i in self.acl.values():
        #     i['actions'] = i['actions'][:-1]

    def get_role(self, client: str) -> str or None:
        """
        :param client: use request.remote
        :return: role or None
        """
        for role in self.acl:
            if self.acl[role]['users'] == '*' or (client in self.acl[role]['users']):
                return role
        return None

    def get_access(self, path: str, client: str=None, role:str or None = None) -> bool:
        if client is not None:
            role = self.get_role(client)

        if path is not None:
            for route in self.routeRoles:
                if path.startswith(route):
                    return role in self.routeRoles[route]
        return True # for 404


@aioweb.middleware
async def check_access(request, handler):
    if aclPolicy.get_access(request.path, request.remote):
        response = await handler(request)
        return response
    else:
        raise aioweb.HTTPUnauthorized()


async def start_server():
    try:
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
        return srv, runner
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


def get_client_role(client: str) -> str or None:
    """
    used only for resroutes

    :param client: eat request.remote
    :return: role or None
    """
    return aclPolicy.get_role(client)


if __name__ != "__main__":
    app = aioweb.Application(
        debug=devMode,
        logger=logRest,
        client_max_size=None,
        middlewares=[check_access])

    from restroutes import routes
    aclPolicy = ACLpolicy(routes, cfg['rest']['acl'])
    routes.static('/help', f'{homeDir}webui/help/', append_version=devMode)
    app.add_routes(routes)

    # TODO AppRunner вызывает свой луп, есть ли смысл в ProactorEventLoop?
    loop = asyncio.ProactorEventLoop()  # обход ограничений Windows на кол-во соединений
    asyncio.set_event_loop(loop)
    srv, runner = loop.run_until_complete(start_server())
