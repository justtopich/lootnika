# Changelog

Look for new version on [https://github.com/justtopich/](https://github.com/justtopich/)



## 0.4.0-dev.0 (20200930)

### Features

* Tasks can use different exporters

### Fixed

* fail to create taskstore if it doesn't exist and set `overwritetaskstore=false`

### Improvements

* Simplified pickers: some method are moved to scheduler.
* Remove logger from exporters. 
* updated **lootnika_mysql** picker
* creating Lootnika document with new argument `lootId`



## 0.3.0-dev.0 (20200923)

### Features

* Done `send_delete` method in Factory

### Fixed

* Lootnika marks identical documents as modified. Fixed by change calculating  document

* In the task beginning always have warning 

  > Previous task is still running

### Improvements

* Calculating  document hash only for meta fields, without header
* Далнейшее разделение модулей. По аналогии с экпортом, сборщики подключаются как отдельный модуль. Теперь они располанаются в папке **pickers**



## 0.2.0-dev.0 (20200916)

### Features

* new tasks parameter: `overwriteTaskstore` - every start will create new task store
* Added new fields to lootnika document header: **UUID**, **create_dtm**, **exporter**, **format**
* New format **CSV** for `lootnika_text` exporter

### Fixed

* Config parser erase comments in configuration file when write section
* Неизменённые документы засчитывались как ошибка задания

### Improvements

* `Publisher` module -> `Exporter`

* *output* config section rename to *export*
* Параметры  экспорта и формата экспорта объединены в одну секцию.
* Converter как отдельный модуль. Описание формата экспорта теперь находится в папке экспортёра `formats`.  Для каждого экспортёра теперь проще добавить новый формат, достаточно описать и добавить его в эту папку.
* Каждый `Exporter` теперь может обратиться лишь к своему `Converter`. Раньше для любого экспорта можно было указать любой формат. Однако, в большинстве случаев каждый экспорт работает со своими форматами.



## 0.1.1.0 (20200905)

### Notes

Alfa release. Реализовано почти все запланированные возможности, для демонстрации более чем достаточно. Пока доступен только сбор данных из MySQL с последующим сохранением документов на диск.

В ближайшие релизы работа будет сконцентрирована на добавление примеров других форматов экспорта документов (сохранять в csv, xml, другие БД и т.д.), других коннекторов (ODBC, файловые хранилища), дальнейшее разделение модулей на базовые (main, wrapper, datastore, schedule, etc) и изменяемых (converter, publisher, collector). В дальнейшем REST модуль со своим API и GUI, а так же вики с документацией.

