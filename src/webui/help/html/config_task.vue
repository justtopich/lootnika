<template>
  <div>
    
    <section id="task">
<h1>Секция Task<a class="headerlink" href="#task" title="Ссылка на этот заголовок">¶</a></h1>
<p>Параметры заданий.</p>
<p>Каждое задание должно иметь свою секцию. Название секции должно совпадать со значением объявленное в <router-link class="reference internal" href="/index/config/config_schedule" to="/index/config/config_schedule"><span class="doc">Schedule</span></router-link>.</p>
<div class="contents local topic" id="id1">
<ul class="simple">
<li><p><a class="reference internal" href="#type">Type</a></p></li>
<li><p><a class="reference internal" href="#exporter">Exporter</a></p></li>
<li><p><a class="reference internal" href="#overwritetaskstore">OverwriteTaskstore</a></p></li>
</ul>
</div>
<section id="type">
<h2>Type<a class="headerlink" href="#type" title="Ссылка на этот заголовок">¶</a></h2>
<p>Тип коннектора.</p>
<p>Доступные сборщики расположены в папке <code class="file docutils literal notranslate"><span class="pre">pickers</span></code>.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">type</span> <span class="o">=</span> <span class="s">lootnika_pyodbc</span>
</pre></div>
</div>
<div class="admonition attention">
<p class="admonition-title">Внимание</p>
<p>В текущей версии этот параметр недоступен</p>
</div>
</section>
<section id="exporter">
<h2>Exporter<a class="headerlink" href="#exporter" title="Ссылка на этот заголовок">¶</a></h2>
<p>Ссылка на экспортёр.</p>
<p>Вы можете использовать одновременно несколько разных экспортёров, а так же назначить для каждого задания свой (см. <router-link class="reference internal" href="/index/config/config_export" to="/index/config/config_export"><span class="doc">Export</span></router-link>.). Это необязательный параметр и в случае его отсутствия Лутника будет использовать секцию <code class="xref std std-option docutils literal notranslate"><span class="pre">[export]</span></code></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Exporter</span> <span class="o">=</span> <span class="s">mail2csv</span>
</pre></div>
</div>
<div class="admonition note">
<p class="admonition-title">Примечание</p>
<p>Этот параметр доступен для любого типа сборщика</p>
</div>
</section>
<section id="overwritetaskstore">
<h2>OverwriteTaskstore<a class="headerlink" href="#overwritetaskstore" title="Ссылка на этот заголовок">¶</a></h2>
<p>Создать новый журнал задания.</p>
<p>Каждое задание создаёт свою БД в которой записываются данные о документах. Эти данные используются для отслеживания изменений в источнике при следующем выполнении. Если активировать этот параметр, то при каждом выполнении задании будет создаваться новый журнал заданий.</p>
<p>Это не обязательный параметр и по умолчанию используется <code class="docutils literal notranslate"><span class="pre">False</span></code>.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">OverwriteTaskstore</span> <span class="o">=</span> <span class="s">True</span>
</pre></div>
</div>
<div class="admonition attention">
<p class="admonition-title">Внимание</p>
<p>При активации параметра все документы будут отмечены как новые, а информация о старых будет утеряна</p>
</div>
<div class="admonition note">
<p class="admonition-title">Примечание</p>
<p>Этот параметр доступен для любого типа сборщика</p>
</div>
<p>Список доступных коннекторов:</p>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme">lootnika ODBC</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#cnxstring" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#cnxstring'">cnxString</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#skipemptyrows" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#skipemptyrows'">SkipEmptyRows</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#docref" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#docref'">DocRef</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#selectid" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#selectid'">SelectID</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#id2" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#id2'">SelectFields</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#branchname" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#branchname'">BranchName</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_task/picker_lootnika_pyodbc_readme" to="/index/config/config_task/picker_lootnika_pyodbc_readme#id5" v-scroll-to="'/index/config/config_task/picker_lootnika_pyodbc_readme#id5'">SelectBranch</router-link></li>
</ul>
</li>
</ul>
</div>
</section>
</section>
    <div></div>
    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>