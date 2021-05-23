<template>
  <div>
    
    <section id="id1">
<h1>Настройки<a class="headerlink" href="#id1" title="Ссылка на этот заголовок">¶</a></h1>
<p>Все параметры хранятся в конфигурационном файле <code class="file docutils literal notranslate"><span class="pre">lootnika.cfg</span></code>. Если он отсутствует, то Лутника создаст его при запуске. В таком случае, в него будут записаны все обязательные параметры и демонстрационное задание. На его основе можно быстро сконфигурировать Лутнику и начать её использовать, но прежде стоит изучить параметры и ознакомиться с <span class="xref std std-doc">синтаксисом</span>.</p>
<p>Подразделы:</p>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_syntax" to="/index/config/config_syntax">Синтаксис настроек</router-link></li>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_server" to="/index/config/config_server">Секция Server</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_server" to="/index/config/config_server#host" v-scroll-to="'/index/config/config_server#host'">Host</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_server" to="/index/config/config_server#port" v-scroll-to="'/index/config/config_server#port'">Port</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_server" to="/index/config/config_server#queryclients" v-scroll-to="'/index/config/config_server#queryclients'">QueryClients</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_server" to="/index/config/config_server#adminclients" v-scroll-to="'/index/config/config_server#adminclients'">AdminClients</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_service" to="/index/config/config_service">Секция Service</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_service" to="/index/config/config_service#name" v-scroll-to="'/index/config/config_service#name'">Name</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_service" to="/index/config/config_service#displayname" v-scroll-to="'/index/config/config_service#displayname'">DisplayName</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_service" to="/index/config/config_service#description" v-scroll-to="'/index/config/config_service#description'">Description</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_logging" to="/index/config/config_logging">Секция Logging</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_logging" to="/index/config/config_logging#enable" v-scroll-to="'/index/config/config_logging#enable'">Enable</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_logging" to="/index/config/config_logging#loglevel" v-scroll-to="'/index/config/config_logging#loglevel'">LogLevel</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_logging" to="/index/config/config_logging#logmaxsizekbs" v-scroll-to="'/index/config/config_logging#logmaxsizekbs'">LogMaxSizeKbs</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_logging" to="/index/config/config_logging#logmaxfiles" v-scroll-to="'/index/config/config_logging#logmaxfiles'">LogMaxFiles</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_diskUsage" to="/index/config/config_diskUsage">Секция DiskUsage</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_diskUsage" to="/index/config/config_diskUsage#pathwatch" v-scroll-to="'/index/config/config_diskUsage#pathwatch'">PathWatch</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_diskUsage" to="/index/config/config_diskUsage#critfreegb" v-scroll-to="'/index/config/config_diskUsage#critfreegb'">CritFreeGb</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_schedule" to="/index/config/config_schedule">Секция Schedule</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_schedule" to="/index/config/config_schedule#enable" v-scroll-to="'/index/config/config_schedule#enable'">Enable</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_schedule" to="/index/config/config_schedule#taskstarttime" v-scroll-to="'/index/config/config_schedule#taskstarttime'">TaskStartTime</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_schedule" to="/index/config/config_schedule#taskcycles" v-scroll-to="'/index/config/config_schedule#taskcycles'">TaskCycles</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_schedule" to="/index/config/config_schedule#repeatmin" v-scroll-to="'/index/config/config_schedule#repeatmin'">RepeatMin</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_schedule" to="/index/config/config_schedule#taskcount" v-scroll-to="'/index/config/config_schedule#taskcount'">TaskCount</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_export" to="/index/config/config_export">Секция Export</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export" to="/index/config/config_export#type" v-scroll-to="'/index/config/config_export#type'">Type</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export" to="/index/config/config_export#batchsize" v-scroll-to="'/index/config/config_export#batchsize'">BatchSize</router-link><ul>
<li class="toctree-l3"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2">lootnika binary</router-link><ul>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2#format" v-scroll-to="'/index/config/config_export/exporter_lootnika_binary_index2#format'">Format</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2#extension" v-scroll-to="'/index/config/config_export/exporter_lootnika_binary_index2#extension'">Extension</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2#path" v-scroll-to="'/index/config/config_export/exporter_lootnika_binary_index2#path'">Path</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2#failpath" v-scroll-to="'/index/config/config_export/exporter_lootnika_binary_index2#failpath'">FailPath</router-link></li>
</ul>
</li>
<li class="toctree-l3"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index">lootnika text</router-link><ul>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#format" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#format'">Format</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#encoding" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#encoding'">Encoding</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#ignoreencodingerrors" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#ignoreencodingerrors'">IgnoreEncodingErrors</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#extension" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#extension'">Extension</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#delimiter" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#delimiter'">Delimiter</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#lineterminator" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#lineterminator'">LineTerminator</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#quoting" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#quoting'">Quoting</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#quotechar" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#quotechar'">Quotechar</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#path" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#path'">Path</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#failpath" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#failpath'">FailPath</router-link></li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_task" to="/index/config/config_task">Секция Task</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_task" to="/index/config/config_task#type" v-scroll-to="'/index/config/config_task#type'">Type</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_task" to="/index/config/config_task#exporter" v-scroll-to="'/index/config/config_task#exporter'">Exporter</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_task" to="/index/config/config_task#overwritetaskstore" v-scroll-to="'/index/config/config_task#overwritetaskstore'">OverwriteTaskstore</router-link><ul>
<li class="toctree-l3"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_mysql_readme" to="/index/config/config_task/picker_lootnika_mysql_readme">lootnika MySQL</router-link><ul>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_mysql_readme" to="/index/config/config_task/picker_lootnika_mysql_readme#dbhost" v-scroll-to="'/index/config/config_task/picker_lootnika_mysql_readme#dbhost'">DBhost</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_mysql_readme" to="/index/config/config_task/picker_lootnika_mysql_readme#dbport" v-scroll-to="'/index/config/config_task/picker_lootnika_mysql_readme#dbport'">DBport</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_mysql_readme" to="/index/config/config_task/picker_lootnika_mysql_readme#dbscheme" v-scroll-to="'/index/config/config_task/picker_lootnika_mysql_readme#dbscheme'">DBscheme</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_mysql_readme" to="/index/config/config_task/picker_lootnika_mysql_readme#dbusr" v-scroll-to="'/index/config/config_task/picker_lootnika_mysql_readme#dbusr'">DBusr</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_mysql_readme" to="/index/config/config_task/picker_lootnika_mysql_readme#dbpsw" v-scroll-to="'/index/config/config_task/picker_lootnika_mysql_readme#dbpsw'">DBpsw</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_mysql_readme" to="/index/config/config_task/picker_lootnika_mysql_readme#skipemptyrows" v-scroll-to="'/index/config/config_task/picker_lootnika_mysql_readme#skipemptyrows'">SkipEmptyRows</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_mysql_readme" to="/index/config/config_task/picker_lootnika_mysql_readme#docref" v-scroll-to="'/index/config/config_task/picker_lootnika_mysql_readme#docref'">DocRef</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_mysql_readme" to="/index/config/config_task/picker_lootnika_mysql_readme#selectid" v-scroll-to="'/index/config/config_task/picker_lootnika_mysql_readme#selectid'">SelectID</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_mysql_readme" to="/index/config/config_task/picker_lootnika_mysql_readme#id2" v-scroll-to="'/index/config/config_task/picker_lootnika_mysql_readme#id2'">SelectFields</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_mysql_readme" to="/index/config/config_task/picker_lootnika_mysql_readme#branchname" v-scroll-to="'/index/config/config_task/picker_lootnika_mysql_readme#branchname'">BranchName</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_mysql_readme" to="/index/config/config_task/picker_lootnika_mysql_readme#id5" v-scroll-to="'/index/config/config_task/picker_lootnika_mysql_readme#id5'">SelectBranch</router-link></li>
</ul>
</li>
<li class="toctree-l3"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme">lootnika ODBC</router-link><ul>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#cnxstring" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#cnxstring'">cnxString</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#skipemptyrows" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#skipemptyrows'">SkipEmptyRows</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#docref" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#docref'">DocRef</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#selectid" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#selectid'">SelectID</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#id2" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#id2'">SelectFields</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#branchname" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#branchname'">BranchName</router-link></li>
<li class="toctree-l4"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#id5" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#id5'">SelectBranch</router-link></li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
</section>
    <div></div>
    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>