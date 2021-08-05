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


Handlers
----------------------------------------
Список обработчиков документов.

Обработчики - это внешние скрипты с помощью которых вы можете изменять, отбраковывать или создавать новые 
документы. Лутника вызывает скрипты из папки :file:`scripts` в указанном порядке. Скрипты перечисляются через :guilabel:`;` Обработка выполняется после того как сборщик передаст документ Лутнике, и перед тем как передать его экспортёру.

.. code-block:: cfg

	handlers = py:extract_files.py; py:custom/filter_fields.py

Обработчики пишутся на языке Python3 и выполняются интерпретатором Лутники, т.е. ограничений на использование методов нет.
Каждый скрипт должен содержать метод ``handler`` который обязательно должен вернуть либо ``Document``, либо ``None``.

.. code-block:: python3

  # extract binary content from document if exist 
  # and put it into another exporter
  
  def handler(doc: "Document", vars):
      log: "Logger" = vars['log']
      put_new_doc = vars['put_new_doc']
      
      files: [dict] = doc.get_field('files')
      if files:
          for file: dict in files:
		  
              newDoc = Document(
                taskId=doc.taskId,
                taskName=doc.taskName,
                reference=f'file_{doc.reference}_{file["id"]}',
                loootId=f'',
                fields=file
              )
			  
              newDoc.export = 'post_file'
              put_new_doc(newDoc)
  
              newDoc.export = 'post_file_info'
              del newDoc.fields['content']
              put_new_doc(newDoc)
			  
          del doc.fields['files']
      else:
          log.warning(f'Not found files in document {doc.reference}')
  
      return doc


Для отладки можно импортировать модели данных

.. code-block:: python3

	try:
		from models import Document
		from lootnika import sout
	except:
		from ..models import Document
		from ..lootnika import sout

	from logging import Logger


.. tip::
	Лутника может выполнять обработку в несколько потоков. см. :doc:`handlerThreads <config_core>`


Список доступных экспортёров:

.. toctree::

   exporter_lootnika_binary_index2
   exporter_lootnika_text_index
   