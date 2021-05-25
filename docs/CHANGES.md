# Changelog

Check for the last version on [https://github.com/justtopich/lootnika](https://github.com/justtopich/lootnika)



## 1.1.2-beta.0 (2021.05.25)

### Improvements

  * extended information for exceptions with pickers initializing

### Fixes

* Config parser erase comments in configuration file when write new section
* Sphinx-doc don't see included themes
* Don't creating default settings (examples) for exporters sections
* no `cnxString` parameter in default settings for **lootnika_pyodbc** picker
* Admin panel not using custom API port and working if Lootnika started on 8080



## 1.1.1-beta.0 (2021.05.23)

### Improvements

  * Update forma **CSV** for **lootnika_text** exporter. Add parameters:
      * `LineTerminator`
      * `Quoting`
      * `Quotechar`


### Fixes

* Exporter **lootnika_pyodbc** can failed if parse documents with few rows



## 1.1.0-beta.0 (2021.05.21)

### Improvements

  * Develop: Exporters formats takes two args:
      * `cfgSection`: exporter section raw
      
      * `cfgExporter`: exporter validated configuration

* Improvements for Lootnika `Document.fields` methods


### Fixes

* Forgotten Lootnika doc sources
* Crashed on launch if else before not checked docs sources
* Console key `make-doc` didn't make html documentation
* Export to **json** can be in incorrect format (without escaping)
* Crash caused by stopping Lootnika when have paused task
* Export errors may not appeared in task statistics



## 1.0.0-beta.0 (2021.05.19)

### Features

* new settings for **lootnika_text** exporter: `encoding` and `ignoreEncodingErrors`
* new importer: **lootnika_pyodbc**
* new exporter: **lootnika_binary** with **bson** format
* Added resource usage info to API cmd `getstatus`
* Include Sphinx-doc v4
* Added console key `make-doc` to build documentation from docs sources
* Included Sphinx-doc theme *sphinx_lootnika_theme*

### Improvements

  * Lootnika `Document.fields` attribute has been changed: **dict** -> **SortedDict** (OrderDict with sorted nested OrderDict, sorting not break if add new keys)
  * Change `get_hash()` method for Lootnika Document: now it based on `bson.dumps()` instead of `orjson.dumps()`
  * Changed the structure of internal documentation storage: Lootnika, collectors and exporters can now contain only sources (restructured text) in their own `docs` directory. If Lootnika detects changes in them, it will offer to update documentation.
  * Updated help documentation

### Fixes

* Failed exports saving in in wrong path export_failed_{datetime}_.

* API cmd `schedule` can return wrong message

* Lootnika Document method `get_field()` failed if fields contain datetime types (**dpath** library issue #145 https://github.com/dpath-maintainers/dpath-python/issues/145). Replaced to native method.

### Notes

Tasks storages now store documents fields with new hash format and not capability with older versions.



## 0.8.0-beta.0 (2021.05.14)

### Features

* Add web admin panel! Available at http://*host:port*/admin


### Fixes

* add `CORS` for all API headers (maybe can be removed at release)
* API cmd `schedule` can return wrong message



## 0.7.0-dev.0 (2021.03.01)

### Features

* REST API: add new command **schedule** 

* Help updated

* Made alternative paths for online help pages. This patch allow to show pages from pickers and exporters. If you change picker or exporter - online help will changed too.

  Navigation is not changing yet

### Fixes

* **lootnika_text** exporter can't get default value for `batchSize`
* config parser don't write configuration examples for some main sections



## 0.6.0-dev.1 (2020.10.13)

### Features

* Add help, but only for configuration parameters. Available at http://*host:port*/help
* Add ACL for REST

### Fixes

* Lootnika not stopped if set `[server]host`  as `0.0.0.0` or `::1`



## 0.5.0-dev.0 (2020.10.06)

### Features

* REST API is coming -  AIOHTTP server included!

### Improvements

* `skipEmptyRows=True`  by default for **lootnika_mysql** picker

### Notes

REST API have only two commands: */a=getstatus*, */a=stop*. The first draft of documentation will be in next version.



## 0.4.0-dev.1 (2020.09.30)

### Features

* Tasks can use different exporters

### Fixes

* fail to create taskstore if it doesn't exist and set `overwritetaskstore=false`

### Improvements

* Simplified pickers: some method are moved to scheduler.
* Remove logger from exporters. 
* updated **lootnika_mysql** picker
* creating Lootnika document with new argument `lootId`



## 0.3.0-dev.0 (2020.09.23)

### Features

* Done `send_delete` method in Factory

### Fixed

* Lootnika marks identical documents as modified. Fixed by change calculating  document hash

* In the task beginning always have warning 

  > Previous task is still running

### Improvements

* Calculating document hash only for meta fields, without header
* Дальнейшее разделение модулей. По аналогии с экcпортом, сборщики подключаются как отдельный модуль. Теперь они располагаются в папке **pickers**



## 0.2.0-dev.0 (2020.09.16)

### Features

* new tasks parameter: `overwriteTaskstore` - every start will create new task store
* Added new fields to lootnika document header: **UUID**, **create_dtm**, **exporter**, **format**
* New format **CSV** for `lootnika_text` exporter

### Fixes

* Config parser erase comments in configuration file when write section
* Неизменённые документы засчитывались как ошибка задания

### Improvements

* `Publisher` module -> `Exporter`

* *output* config section rename to *export*
* Параметры  экспорта и формата экспорта объединены в одну секцию.
* Converter как отдельный модуль. Описание формата экспорта теперь находится в папке экспортёра `formats`.  Для каждого экспортёра теперь проще добавить новый формат, достаточно описать и добавить его в эту папку.
* Каждый `Exporter` теперь может обратиться лишь к своему `Converter`. Раньше для любого экспорта можно было указать любой формат. Однако, в большинстве случаев каждый экспорт работает со своими форматами.



## 0.1.1.0 (2020.09.05)

### Notes

Alfa release. Реализовано почти все запланированные возможности, для демонстрации более чем достаточно. Пока доступен только сбор данных из MySQL с последующим сохранением документов на диск.

В ближайшие релизы работа будет сконцентрирована на добавление примеров других форматов экспорта документов (сохранять в csv, xml, другие БД и т.д.), других коннекторов (ODBC, файловые хранилища), дальнейшее разделение модулей на базовые (main, wrapper, datastore, schedule, etc) и изменяемых (converter, publisher, collector). В дальнейшем REST модуль со своим API и GUI, а так же вики с документацией.

