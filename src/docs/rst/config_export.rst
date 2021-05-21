Секция Export
=========================================
Параметры экспорта документов.

Здесь задаются формат и место назначения данных, которая Лутника загрузила из источника.
Варианты экспорта зависят от используемых модулей. В состав данной версии входит **lootnika_text** и **lootnika_binary** для текстовых и бинарных файлов соответственно.

Вы можете использовать одновременно несколько разных экспортёров, а так же назначить для каждого задания свой (см. :doc:`Schedule: TasksInfo <api_control>`). Если задание не ссылается ни на какой экспорт, то для него Лутника будет использовать секцию :option:`[export]`. Если такой секции нет, то Лутника создаст его с типом ``lootnika_text`` и форматом ``json``.


.. attention::
	Набор доступных параметров в этой секции зависит от используемого типа экспорта.

Список доступных параметров:

.. contents:: :local:


Type
----------------------------------------
Тип экспортёра.

Доступные экспортёры расположены в папке :file:`exporters`.

.. code-block:: cfg

	type = lootnika_text


BatchSize
----------------------------------------
Размер очереди на экспорт.

Количество документов при достижении которого будет выполняться экспорт.

.. code-block:: cfg

	BatchSize = 100


Список доступных экспортёров:

.. toctree::

   exporter_lootnika_binary_index2
   exporter_lootnika_text_index
   