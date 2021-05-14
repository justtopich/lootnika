# Lootnika. TODO

* В Лутнике может быть одновременно активно несколько экспортёров. Их страницы в хелпе так же должны быть доступны одновременно.

* Перестраивать оглавление при изменении страниц

* DBusr дважды в хелпе

* При долгом чтении sqlite возможны блокировки в части rest

* в хелпе в примерах команд исправить _action_ на _а_

* add for dev headers={'Access-Control-Allow-Origin': '*'}

* API execute schedule cmd return wrong status

* stop when paused:

  ```python
  Lootnika DEBUG: Stopping Scheduler thread
  Exception in thread Scheduler:
  Traceback (most recent call last):
    File "C:\Python\Python38\lib\threading.py", line 932, in _bootstrap_inner
      self.run()
    File "C:\Python\Python38\lib\threading.py", line 870, in run
      self._target(*self._args, **self._kwargs)
    File "D:\pydev\pet\lootnika\src\scheduler.py", line 214, in run
      ht.cancel()
  AttributeError: 'Thread' object has no attribute 'cancel'
  ```

  