<template>
  <div>
    
    <section id="export">
<h1>Секция Export<a class="headerlink" href="#export" title="Ссылка на этот заголовок">¶</a></h1>
<p>Параметры экспорта документов.</p>
<p>Здесь задаются формат и место назначения данных, которая Лутника загрузила из источника.
Варианты экспорта зависят от используемых модулей. В состав данной версии входит <strong>lootnika_text</strong> и <strong>lootnika_binary</strong> для текстовых и бинарных файлов соответственно.</p>
<p>Вы можете использовать одновременно несколько разных экспортёров, а так же назначить для каждого задания свой (см. <router-link class="reference internal" href="/index/api/api_control" to="/index/api/api_control"><span class="doc">Schedule: TasksInfo</span></router-link>). Если задание не ссылается ни на какой экспорт, то для него Лутника будет использовать секцию <code class="xref std std-option docutils literal notranslate"><span class="pre">[export]</span></code>. Если такой секции нет, то Лутника создаст его с типом <code class="docutils literal notranslate"><span class="pre">lootnika_text</span></code> и форматом <code class="docutils literal notranslate"><span class="pre">json</span></code>.</p>
<div class="admonition attention">
<p class="admonition-title">Внимание</p>
<p>Набор доступных параметров в этой секции зависит от используемого типа экспорта.</p>
</div>
<p>Список доступных параметров:</p>
<div class="contents local topic" id="id1">
<ul class="simple">
<li><p><a class="reference internal" href="#type">Type</a></p></li>
<li><p><a class="reference internal" href="#batchsize">BatchSize</a></p></li>
</ul>
</div>
<section id="type">
<h2>Type<a class="headerlink" href="#type" title="Ссылка на этот заголовок">¶</a></h2>
<p>Тип экспортёра.</p>
<p>Доступные экспортёры расположены в папке <code class="file docutils literal notranslate"><span class="pre">exporters</span></code>.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">type</span> <span class="o">=</span> <span class="s">lootnika_text</span>
</pre></div>
</div>
</section>
<section id="batchsize">
<h2>BatchSize<a class="headerlink" href="#batchsize" title="Ссылка на этот заголовок">¶</a></h2>
<p>Размер очереди на экспорт.</p>
<p>Количество документов при достижении которого будет выполняться экспорт.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">BatchSize</span> <span class="o">=</span> <span class="s">100</span>
</pre></div>
</div>
<p>Список доступных экспортёров:</p>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2">lootnika_binary</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2#format" v-scroll-to="'/index/config/config_export/exporter_lootnika_binary_index2#format'">Format</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2#extension" v-scroll-to="'/index/config/config_export/exporter_lootnika_binary_index2#extension'">Extension</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2#path" v-scroll-to="'/index/config/config_export/exporter_lootnika_binary_index2#path'">Path</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2#failpath" v-scroll-to="'/index/config/config_export/exporter_lootnika_binary_index2#failpath'">FailPath</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index">lootnika_text</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#format" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#format'">Format</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#encoding" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#encoding'">Encoding</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#ignoreencodingerrors" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#ignoreencodingerrors'">IgnoreEncodingErrors</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#extension" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#extension'">Extension</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#delimiter" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#delimiter'">Delimiter</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#path" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#path'">Path</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#failpath" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#failpath'">FailPath</router-link></li>
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