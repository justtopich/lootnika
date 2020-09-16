# Changelog

Look for new version on [https://github.com/justtopich/](https://github.com/justtopich/)



## 0.2.0-dev.0

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

