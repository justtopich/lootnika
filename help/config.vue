<template>
  <div>
    <div class="section" id="id1">
<h1>Настройки<a class="headerlink" href="#id1" title="Ссылка на этот заголовок">¶</a></h1>
<p>Все параметры хранятся в конфигурационном файле <code class="file docutils literal notranslate"><span class="pre">lootnika.cfg</span></code>. Если он отсутствует, то Лутника создаст его при запуске. В таком случае, в него будут записаны все обязательные параметры и демонстрационное задание. На его основе можно быстро сконфигурировать Лутнику и начать её использовать, но прежде стоит изучить параметры и ознакомиться с <span class="xref std std-doc">синтаксисом</span>.</p>
<p>Подразделы:</p>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><router-link class="reference internal" href="/config/config_syntax" to="/config/config_syntax">Синтаксис настроек</router-link></li>
<li class="toctree-l1"><router-link class="reference internal" href="/config/config_server" to="/config/config_server">Секция Server</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_server" to="/config/config_server#host" v-scroll-to="'/config/config_server#host'">Host</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_server" to="/config/config_server#port" v-scroll-to="'/config/config_server#port'">Port</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_server" to="/config/config_server#queryclients" v-scroll-to="'/config/config_server#queryclients'">QueryClients</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_server" to="/config/config_server#adminclients" v-scroll-to="'/config/config_server#adminclients'">AdminClients</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/config/config_service" to="/config/config_service">Секция Service</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_service" to="/config/config_service#name" v-scroll-to="'/config/config_service#name'">Name</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_service" to="/config/config_service#displayname" v-scroll-to="'/config/config_service#displayname'">DisplayName</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_service" to="/config/config_service#description" v-scroll-to="'/config/config_service#description'">Description</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/config/config_logging" to="/config/config_logging">Секция Logging</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_logging" to="/config/config_logging#enable" v-scroll-to="'/config/config_logging#enable'">Enable</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_logging" to="/config/config_logging#loglevel" v-scroll-to="'/config/config_logging#loglevel'">LogLevel</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_logging" to="/config/config_logging#logmaxsizekbs" v-scroll-to="'/config/config_logging#logmaxsizekbs'">LogMaxSizeKbs</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_logging" to="/config/config_logging#logmaxfiles" v-scroll-to="'/config/config_logging#logmaxfiles'">LogMaxFiles</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/config/config_diskUsage" to="/config/config_diskUsage">Секция DiskUsage</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_diskUsage" to="/config/config_diskUsage#pathwatch" v-scroll-to="'/config/config_diskUsage#pathwatch'">PathWatch</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_diskUsage" to="/config/config_diskUsage#critfreegb" v-scroll-to="'/config/config_diskUsage#critfreegb'">CritFreeGb</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/config/config_schedule" to="/config/config_schedule">Секция Schedule</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_schedule" to="/config/config_schedule#enable" v-scroll-to="'/config/config_schedule#enable'">Enable</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_schedule" to="/config/config_schedule#taskstarttime" v-scroll-to="'/config/config_schedule#taskstarttime'">TaskStartTime</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_schedule" to="/config/config_schedule#taskcycles" v-scroll-to="'/config/config_schedule#taskcycles'">TaskCycles</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_schedule" to="/config/config_schedule#repeatmin" v-scroll-to="'/config/config_schedule#repeatmin'">RepeatMin</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_schedule" to="/config/config_schedule#taskcount" v-scroll-to="'/config/config_schedule#taskcount'">TaskCount</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/config/config_export" to="/config/config_export">Секция Export</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_export" to="/config/config_export#type" v-scroll-to="'/config/config_export#type'">Type</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_export" to="/config/config_export#format" v-scroll-to="'/config/config_export#format'">Format</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_export" to="/config/config_export#extension" v-scroll-to="'/config/config_export#extension'">Extension</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_export" to="/config/config_export#batchsize" v-scroll-to="'/config/config_export#batchsize'">BatchSize</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_export" to="/config/config_export#delimiter" v-scroll-to="'/config/config_export#delimiter'">Delimiter</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_export" to="/config/config_export#path" v-scroll-to="'/config/config_export#path'">Path</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_export" to="/config/config_export#failpath" v-scroll-to="'/config/config_export#failpath'">FailPath</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/config/config_task" to="/config/config_task">Секция Task</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#exporter" v-scroll-to="'/config/config_task#exporter'">Exporter</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#overwritetaskstore" v-scroll-to="'/config/config_task#overwritetaskstore'">OverwriteTaskstore</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#dbhost" v-scroll-to="'/config/config_task#dbhost'">DBhost</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#dbport" v-scroll-to="'/config/config_task#dbport'">DBport</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#dbscheme" v-scroll-to="'/config/config_task#dbscheme'">DBscheme</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#dbusr" v-scroll-to="'/config/config_task#dbusr'">DBusr</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#dbpsw" v-scroll-to="'/config/config_task#dbpsw'">DBpsw</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#id2" v-scroll-to="'/config/config_task#id2'">DBusr</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#skipemptyrows" v-scroll-to="'/config/config_task#skipemptyrows'">SkipEmptyRows</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#docref" v-scroll-to="'/config/config_task#docref'">DocRef</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#selectid" v-scroll-to="'/config/config_task#selectid'">SelectID</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#id3" v-scroll-to="'/config/config_task#id3'">SelectFields</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#branchname" v-scroll-to="'/config/config_task#branchname'">BranchName</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/config/config_task" to="/config/config_task#id6" v-scroll-to="'/config/config_task#id6'">SelectBranch</router-link></li>
</ul>
</li>
</ul>
</div>

    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>