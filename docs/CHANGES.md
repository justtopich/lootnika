# Changelog

Look for new version on [https://github.com/justtopich/](https://github.com/justtopich/)



## ???

### Features

* new tasks parameter: `overwriteTaskstore` - every start will create new task store

### Fixed

* Config parser erase comments in configuration file when write section



## 0.1.1.0 (20200905)

### Notes

Alfa release. Реализовано почти все запланированные возможности, для демнострации более чем достаочно. Пока доступен только сбор данных из MySQL с последующим сохранением документов на диск.

В ближайшие релизы работа будет сконцентрирована на добавление примеров других форматов экспорта документов (сохранять в csv, xml, другие БД и т.д.), других коннекторов (ODBC, файловые хранилища), дальнейшее разделение модулей на базовые (main, wrapper, datastore, schedule, etc) и изменяемых (converter, publisher, collector). В дальнейшем REST модуль со своим API и GUI, а так же вики с документацией.

