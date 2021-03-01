from core import traceback
from lootnika import (
    os,
    copy,
    __version__,
    pickerType,
    homeDir,
    devMode,
    asyncio,
    aiohttp,
    aioweb)
from conf import (
    cfg,
    logRest)

from pathlib import Path, WindowsPath
from typing import Dict, List

from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request
from aiohttp.web_response import Response, StreamResponse
from aiohttp.web_exceptions import HTTPForbidden, HTTPNotFound


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

    def get_access(self, path: str, client: str = None, role: str or None = None) -> bool:
        if client is not None:
            role = self.get_role(client)

        if path is not None:
            for route in self.routeRoles:
                if path.startswith(route):
                    return role in self.routeRoles[route]
        return True  # for 404


class TmplRender:
    def __init__(self, templates: List[str], assets: dict):
        self.assets = assets
        if devMode:
            print('\n!#REST DISABLE PRERENDER FOR TEMPLATES\n')
            return
        for tmpl in templates:
            try:
                self.__dict__[tmpl] = self.load_tmpl(tmpl)
            except FileNotFoundError:
                logRest.warning(
                    f"Enable to load template from {homeDir}webui/admin/templates/{tmpl}.html: file not found")
            except Exception as e:
                logRest.warning(f"Enable to load template from {homeDir}webui/admin/templates/{tmpl}.html: {e}")

    def load_tmpl(self, tmpl: str):
        with open(f'{homeDir}webui/admin/templates/{tmpl}.html', 'r', encoding="utf-8") as f:
            tmpl = f.read()
            for k, v in self.assets.items():
                tmpl = tmpl.replace('{{%s}}' % k, v)
        return tmpl

    def get(self, page: str):
        if devMode:
            return self.load_tmpl(page)
        else:
            return self.__dict__[page]


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

        logRest.info(f"Started on {cfg['rest']['host']}:{cfg['rest']['port']}")
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


def patch_aiostatic(alterdirs: Dict[str, List[str]]) -> None:
    """
    AIOHTTP will search static file in few directories.
    alternative directories will be the first place for searching.
    append_version may not work

    :param alterdirs: alternative directories for static prefix url
    """

    async def _handle(self, request: Request) -> StreamResponse:
        rel_url = request.match_info['filename']
        try:
            filename = Path(rel_url)
            if filename.anchor:
                # rel_url is an absolute name like
                # /static/\\machine_name\c$ or /static/D:\path
                # where the static dir is totally different
                raise HTTPForbidden()

            # alternative directories is the first place for searching
            alt = False
            directory = self._directory
            if self.canonical in self._directory_alt:
                for v in self._directory_alt[self.canonical]:
                    filepath = v.joinpath(filename).resolve()
                    if filepath.exists():
                        directory = v
                        alt = True
                        break

            if not alt:
                filepath = directory.joinpath(filename).resolve()
            if not self._follow_symlinks:
                filepath.relative_to(directory)

        except (ValueError, FileNotFoundError) as error:
            # relatively safe
            raise HTTPNotFound() from error
        except HTTPForbidden:
            raise
        except Exception as error:
            # perm error or other kind!
            request.app.logger.exception(error)
            raise HTTPNotFound() from error

        # on opening a dir, load its contents if allowed
        if filepath.is_dir():
            if self._show_index:
                try:
                    return Response(text=self._directory_as_html(filepath),
                                    content_type="text/html")
                except PermissionError:
                    raise HTTPForbidden()
            else:
                raise HTTPForbidden()
        elif filepath.is_file():
            return FileResponse(filepath, chunk_size=self._chunk_size)
        else:
            raise HTTPNotFound

    def make_dir(dir: str) -> WindowsPath:
        try:
            directory = Path(dir)
            if str(directory).startswith('~'):
                directory = Path(os.path.expanduser(str(directory)))
            directory = directory.resolve()
            if not directory.is_dir():
                raise ValueError('Not a directory')
            return directory
        except (FileNotFoundError, ValueError) as error:
            raise ValueError(
                "No directory exists at '{}'".format(directory)) from error

    for k, v in alterdirs.items():
        alterdirs[k] = []
        for dir in v:
            try:
                alterdirs[k].append(make_dir(dir))
                logRest.info(f"Found alternative dir for static route {k}: {dir}")
            except ValueError:
                logRest.error(f"Fail to load alternative static route directory {k} {v}")

    aiohttp.web_urldispatcher.StaticResource._handle = _handle
    aiohttp.web_urldispatcher.StaticResource._directory_alt = alterdirs


if __name__ != "__main__":
    # tmplRender = TmplRender(['help'], {'build': __version__.replace('.', '')})

    taskListCopy = copy.deepcopy(cfg['schedule']['tasks'])

    ls = [f'{homeDir}pickers/{pickerType}/webui/help/html']
    for i in cfg['exporters'].values():
        if i.type not in ls:
            ls.append(f'{homeDir}exporters/{i.type}/webui/help/html')
    patch_aiostatic({'/help': ls})

    app = aioweb.Application(
        debug=devMode,
        logger=logRest,
        client_max_size=None,
        middlewares=[check_access])

    from restroutes import routes

    aclPolicy = ACLpolicy(routes, cfg['rest']['acl'])
    routes.static('/help', f'{homeDir}webui/help/html', append_version=devMode)
    app.add_routes(routes)

    # TODO AppRunner вызывает свой луп, есть ли смысл в ProactorEventLoop?
    loop = asyncio.ProactorEventLoop()  # обход ограничений Windows на кол-во соединений
    asyncio.set_event_loop(loop)
    srv, runner = loop.run_until_complete(start_server())
