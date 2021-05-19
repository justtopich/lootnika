lootnika ODBC
=========================================
Коннектор к БД с использованием протокола ODBC.

.. attention::
	Для работы коннектора необходимо предварительно установить ODBC драйвера

Доступны следующие параметры:

.. contents:: :local:


cnxString
----------------------------------------
Параметры подключения. Для :envvar:`DRIVER` укажите ODBC драйвер.

.. code-block:: cfg

	cnxString = "
		DRIVER={PostgreSQL Unicode};
		DATABASE=greenplum;
		UID=medoed;
		PWD=Ichi-Ni-San!;
		SERVER=222.22.22.222; PORT=1234;"


SkipEmptyRows
----------------------------------------
Булево значение отвечающее за пропуск пустых строк.

Испльзуйте этот параметр если не хотите чтобы пустые строки попадали в документ. При активации этого параметра, если запрос вернёт пустую строку, коннектор подставит для каждого поля значение ``None``

По умолчанию используется значение ``True``

.. code-block:: cfg

	SkipEmptyRows=True


DocRef
----------------------------------------
Шаблон создания идентификаторов документов.

Reference должен быть уникальным для каждого документа. В нём можно использовать метаданные самого документа, например: его id, номер, название и т.д.

Используйте только те поля, которые всегда присутствуют документе. Если нужного поля не окажется в метаданных, то документ не будет создан, а значит не будет передан на экспорт. Если документ не имеет уникальных полей, используйте комбинацию различных полей и других указателей. 

.. code-block:: cfg

	DocRef=some_doc_@loot_id@
	DocRef=document_@number@
	DocRef=@id@-@name@-@data@

Независимо от набора полей документа, вы всегда можете использовать его идентификатор в источнике :envvar:`loot_id` (см. `SelectFields <#SelectFields>`_).


SelectID
----------------------------------------
SQL запрос для получения идентификаторов документов в источнике.

Полученные ID используются в запросах на получение полей документа. Запрос обязательно должен возвращать только один столбец. Полученное значение доступно во всех SQL запросах как :envvar:`loot_id`


.. code-block:: cfg

	SelectID = SELECT id FROM topics WHERE status = "open"
	SelectID = SELECT login FROM users


SelectFields
----------------------------------------
SQL запрос для получения полей документа.

Возвращаемые строки добавляются к метаданным документа в виде полей. Названия этих полей будут соответствовать названиям столбцов.

Для каждого документа можно выполнять любые SQL запросы подставляя в них его поля из предыдущих запросов. Для этого оберните их в :guilabel:`@`. Количество запросов не ограничено и начинаются с :option:`SelectFields0`. В одном таком параметре может быть только один запрос.

.. code-block:: cfg

	SelectFields0 = SELECT id, title, author FROM topics WHERE topic = @loot_id@
	SelectFields1 = SELECT nickname AS user_nickname FROM users WHERE id = @author@

После вышеприведённого примера документ будет иметь следующую структуру: 

.. code-block:: json

    {
      "id" : 535,
      "title" : "Продам Peugeot",
      "author" : 88,
      "user_nickname" : "Daniel"
    }

Все результаты из таких запросов будут добавлены в **основные поля** документа - это такие поля, которые доступны для подстановки в любые запросы (см. `SelectBranch <#SelectBranch>`_).


.. warning::
	Такой запрос забирает только одну строку результатов. Если вам надо забрать несколько, то используйте `SelectBranch <#SelectBranch>`_.

BranchName
----------------------------------------
Название ветви запросов.

Поле документа, в которое будут записаны результаты данной ветви запросов (см. `SelectBranch <#SelectBranch>`_).
Количество ветвей не ограничено и начинаются с :option:`BranchName0`

.. code-block:: cfg

    BranchName0 = attachments


SelectBranch
----------------------------------------
SQL запрос из вспомогательной ветви.

Позволяет собрать несколько значений одного поля или отдельные сущности со своим набором полей.

Для каждой ветви обязательно нужно указать её имя `BranchName <#BranchName>`_.
Количество запросов внутри одной ветви не ограничено и начинаются с той же цифры что и её название

.. code-block:: cfg

    BranchName0 = forum_posts
    SelectBranch0 = SELECT * FROM posts
    BranchName1 = forum_users
    SelectBranch1 = SELECT * FROM users

К примеру, можно получить посты из одной темы форума
    
.. code-block:: cfg
    
    SelectID = SELECT id FROM topics
    SelectFields0 = SELECT id, title, author FROM topics WHERE topic = @loot_id@
    
    BranchName0 = posts
    SelectBranch0 = SELECT dtm, user, text FROM posts WHERE topic = @loot_id@

Тогда каждый документ получится примерно таким

.. code-block:: json

    {
      "id" : 535,
      "title" : "Продам Peugeot",
      "author" : 88,
      "posts" : [{
        "dtm": "15:25:40",
        "user": 88,
        "text": "Не бита, не крашена, пробег не смотан, как новая, сел и поехал!"
        },{
        "dtm": "22:08:04",
        "user": 623,
        "text": "пробег точно родной?"
        }]
    }

Внутри вспомогательной ветви можно так же выполнять несколько запросов и подставлять в них как основные, так поля из этой же ветви

.. code-block:: cfg
    
    SelectID = SELECT id FROM topics
    SelectFields0 = SELECT id, title, author FROM topics WHERE topic = @loot_id@
    
    BranchName0 = posts
    SelectBranch0 = SELECT dtm, user, text FROM posts WHERE topic = @loot_id@
    SelectBranch0-0 = SELECT nickname FROM users WHERE id = @user@
    SelectBranch0-1 = SELECT karma FROM users WHERE id = @user@

Тогда каждый документ уже будет таким

.. code-block:: json

    {
      "id" : 535,
      "title" : "Продам Peugeot",
      "author" : 88,
      "posts" : [{
        "dtm": "15:25:40",
        "user": 88,
        "text": "Не бита, не крашена, пробег не смотан, как новая, сел и поехал!",
        "nickname": "Daniel",
        "karma": 2
        },{
        "dtm": "22:08:04",
        "user": 623,
        "text": "пробег точно родной?",
        "nickname": "Еmilien",
        "karma": 145
        }]
    }

У таких запросов есть ещё одно свойство - в отличии от `SelectFields <#SelectFields>`_ они могут записать несколько значений в одно поле.

.. code-block:: cfg
    
    SelectID = SELECT id FROM topics
    SelectFields0 = SELECT id, title, author FROM topics WHERE topic = @loot_id@
    
    BranchName0 = posts
    SelectBranch0 = SELECT id, dtm, user, text FROM posts WHERE topic = @loot_id@
    SelectBranch0-0 = SELECT nickname FROM users WHERE id = @user@
    SelectBranch0-1 = SELECT id AS attach_id, name AS attach_name FROM files WHERE post_id = @id@

В этом случае документ будет таким

.. code-block:: json

    {
      "id" : 535,
      "title" : "Продам Peugeot",
      "author" : 88,
      "posts" : [{
        "id": 27897,
        "dtm": "15:25:40",
        "user": 88,
        "text": "Не бита, не крашена, пробег не смотан, как новая, сел и поехал!",
        "nickname": "Daniel",
        "attach_id": [440, 441],
        "attach_name": ["foto1.jpg", "foto2.jpg"]
        },{
        "id": 28002,
        "dtm": "22:08:04",
        "user": 623,
        "text": "пробег точно родной?",
        "nickname": "Еmilien"
        }]
    }

.. attention::
	В запросе :option:`SelectBranch0-1` используется поле :envvar:`id`, которое есть и в основных и в вспомогательных полях. **В приоритете подстановки поля из собственной ветви всегда выше основных.** 

Таким образом можно сказать, что документ содержит тему с названием *Продам Peugeot* внутри которой есть два сообщения от *Daniel* и *Еmilien*, что в первом сообщении автор приложил два файла: *foto1.jpg* и *foto2.jpg*.

.. warning::
    Запросы из дополнительной ветви имеют свои ограничения:
        - для них нельзя добавить ещё одну ветвь запросов типа *SelectBranch0-0-0*
        - они могут использовать поля только из основной или своей ветви.
        - они могут переписать поля только внутри своей ветви.
