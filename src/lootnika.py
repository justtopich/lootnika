"""
Lootnika ETL framework. Entry point.

⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣷⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣶⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣦⣀⡀⠀⢀⣴⣇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⣴⣿⣿⣿⣿⠛⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀
⠀⠀⣾⣿⣿⣿⣿⣿⣶⣿⣯⣭⣬⣉⣽⣿⣿⣄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
⢸⣿⣿⣿⣿⠟⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⣿⣿⣿⣿⡿⠛⠉⠉⠉⠉⠁
⠘⠛⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠛⠃⠀⠀⠀⠀⠀⠀⠀
- don't scold my code, I have little paws!
"""

from typing import Final
from __init__ import *


# WORK_ANYWAY: Final = True  # disable shutdown
WORK_ANYWAY: Final = False
DEV_MODE: Final = False
# DEV_MODE: Final = True
# sys.argv.append('run')  # only for debug mode
# sys.argv.append('make-doc')


def svc_init():
    class AppServerSvc(win32serviceutil.ServiceFramework):
        from conf import get_svc_params
        svcParams = get_svc_params()
        _svc_name_ = svcParams[0]
        _svc_display_name_ = svcParams[1]
        _svc_description_ = svcParams[2]

        def __init__(self, args):
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            socket.setdefaulttimeout(60)

        def SvcStop(self):
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.hWaitStop)

        def SvcDoRun(self):
            rc = None
            try:
                import core
            except Exception as e:
                with open(f'{homeDir}error.txt', 'w') as f:
                    f.write(f"{traceback.format_exc()}")
                os._exit(42)

            while rc != win32event.WAIT_OBJECT_0:
                time.sleep(1)
                rc = win32event.WaitForSingleObject(self.hWaitStop, 4000)
                # если стопим через команду или по внутренним причинам
                if core.selfControl.stop: return

            core.shutdown_me(1, '')
    return AppServerSvc


if __name__ == "__main__":
    try:
        if len(sys.argv) == 1 and not DEV_MODE:
            if homeDir.endswith('system32/'):
                # Server 2012 != Win 10
                homeDir = os.path.dirname(sys.executable) + '/' # Server 2012 != Win 10

            AppServerSvc = svc_init()
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(AppServerSvc)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            if 'install' in sys.argv or 'remove' in sys.argv or 'update' in sys.argv:
                AppServerSvc = svc_init()
                win32serviceutil.HandleCommandLine(AppServerSvc)

            elif 'doc' in sys.argv:
                print('Export documentation to ./docs')
                try:
                    os.mkdir(f'{homeDir}docs')
                except:
                    pass

                for i in os.listdir(f'{dataDir}docs'):
                    shutil.copy2(f'{dataDir}docs/{i}', f'{homeDir}docs/{i}')

            elif 'help' in sys.argv:
                raise Exception('Show help')
            elif 'run' in sys.argv:
                from conf import log, logRest, console
                if DEV_MODE:
                    print('\n!#RUNNING IN DEVELOPER MODE\n')
                    log.setLevel(10)
                    logRest.setLevel(10)
                    console.setLevel(10)

                import core

            elif 'make-doc' in sys.argv:
                from conf import log, logRest, console
                log.info(f"Compile documentation")
                sys.argv = sys.argv[:1]
                import sphinxbuilder
                sphinxbuilder.build()
            else:
                raise Exception('Show help')

    except Exception as e:
        e = traceback.format_exc()
        print(f'Fail to start main thread: {e}')

        with open(f"{homeDir}error.txt", 'w') as f:
            f.write(str(e))

        print(f'\nUsage: {os.path.basename(sys.argv[0])} [options]\n'
              'Options:\n'
              ' run: start me\n'
              ' doc: get documentation\n'
              ' install: install as windows service\n'
              ' remove: delete windows service\n'
              ' update: update windows service\n'
              ' make-doc: recompile documentation\n')
        # os._exit(42)
