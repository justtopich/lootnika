Секция Export
=========================================
Параметры экспорта документов.

Здесь задаются формат и место назначения данных, которая Лутника загрузила из источника.
Варианты экспорта зависят от используемых модулей. В состав данной версии входит **lootnika_text** который умеет сохранять документы в формат **json** и **csv**.

Вы можете использовать одновременно несколько разных экспортёров, а так же назначить для каждого задания свой (см. :doc:`Schedule: TasksInfo <api_control>`). Если задание не ссылается ни на какой экспорт, то для него Лутника будет использовать секцию :option:`[export]`. Если такой секции нет, то Лутника создаст его с типом ``lootnika_text`` и форматом ``json``.



.. attention::
	Набор доступных параметров зависит от используемого экспортёра.

Список доступных параметров:

.. contents:: :local:


Type
----------------------------------------
Тип экспортёра.

Доступные экспортёры расположены в папке :file:`exporters`.

.. code-block:: cfg

	type = lootnika_text

.. note::
	Этот параметр обязателен для любого типа экспорта


Format
----------------------------------------
Формат документа.

Для каждого типа экспорта доступны свои форматы документов. Доступные форматы расположены в папке :file:`formats` в папке экспортёра. Например, для ``lootnika_text`` это :file:`exporters/lootnika_text/formats/`

.. code-block:: cfg

	Format = avro

.. note::
	Этот параметр обязателен для любого типа экспорта


Extension
----------------------------------------
Расширение файла.

Если не задано, то **lootnika_text** будет сохранять в ``json``.

.. code-block:: cfg

	Extension = txt
	

BatchSize
----------------------------------------
Размер очереди на экспорт.

Чем больше метаданных в документах, тем меньше указывайте размер очереди.


.. code-block:: cfg

	BatchSize = 100

.. note::
	Этот параметр обязателен для любого типа экспорта


Delimiter
----------------------------------------
Разделитель полей.

Доступен при использовании формата ``csv``

.. code-block:: cfg

	Delimiter = |


Path
----------------------------------------
Путь сохранение документов.

.. code-block:: cfg

	path = outgoing/mytask


FailPath
----------------------------------------
Директория сохранения документов в случае неудачного экспорта.

Коннектор будет создавать уникальную папку для каждого исполняемого экземпляра задания. Если одно задание выполнялось 3 раза и при каждом выполнении были неудачные попытки экспорта, то будут созданы 3 папки содержащие итоговые документы. Вы сможете сами отправить их на обработку без необходимости повторного выполнения задания.

.. code-block:: cfg

	FailPath = txt

