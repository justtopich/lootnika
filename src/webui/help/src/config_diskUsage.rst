Секция DiskUsage
=========================================
Отслеживание свободного места на диске сервера.

Во время выполнения заданий Лутника может отслеживать свободное место на заданном диске. Если во время выполнения задания по каким-то причинам будет достигнут лимит свободного места, то Лутника приостанавливает выполнение задания и переходит в режиме ожидания на **30 минут**. Если по истечению этого времени свободное места так и не станет больше заданного лимита - Лутника остановит выполнение текущего задания.

Доступны следующие параметры:

.. contents:: :local:


PathWatch
----------------------------------------
Диск, за свободным местом которого необходимо следить.

.. code-block:: cfg

	PathWatch = C:\


CritFreeGb
----------------------------------------
Минимальный размер свободного места. Измеряется в ГБ.

.. code-block:: cfg

	CritFreeGb = 10
