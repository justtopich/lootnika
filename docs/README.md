# Lootnika

Lootnika is ETL framework written on Python3. 

Key futures:

* Tasks scheduler 
* Incremental data collecting
* Connectors for different sources
* Export into different formats
* Data transform 
* web GUI
* REST API
* Single point setup for all task and other settings
* Simple control and monitoring with logging and API 



## What's the trick

Only what you need is create the picker for your data source and documents exporter. Or use included solutions.

**Pickers** are connecting to source and collecting data. You do not need monitoring data changes, make schedule and e.t.c. Take a data and push them into Lootnika core in json format.

**Exporter** -  you can save data in another storage. Just write what need to do with json document from input.

<u>This tool is also in developing stage!</u> For production usage see something like NiFi or other.




## Quick start


```shell
pip install -r requirements.txt
python loothika.py run 
```

Lootnika will create configuration file `loothika.cfg` with examples if needed. 

After start check documentation at  `http://localhost:port/help` where *port* is **[server]port** in `loothika.cfg`.



------

alex1.beloglazov@yandex.ru

