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
<li><p><a class="reference internal" href="#handlers">Handlers</a></p></li>
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
</section>
<section id="handlers">
<h2>Handlers<a class="headerlink" href="#handlers" title="Ссылка на этот заголовок">¶</a></h2>
<p>Список обработчиков документов.</p>
<p>Обработчики - это внешние скрипты с помощью которых вы можете изменять, отбраковывать или создавать новые
документы. Лутника вызывает скрипты из папки <code class="file docutils literal notranslate"><span class="pre">scripts</span></code> в указанном порядке. Скрипты перечисляются через <span class="guilabel">;</span> Обработка выполняется после того как сборщик передаст документ Лутнике, и перед тем как передать его экспортёру.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">handlers</span> <span class="o">=</span> <span class="s">py:extract_files.py; py:custom/filter_fields.py</span>
</pre></div>
</div>
<p>Обработчики пишутся на языке Python3 и выполняются интерпретатором Лутники, т.е. ограничений на использование методов нет.
Каждый скрипт должен содержать метод <code class="docutils literal notranslate"><span class="pre">handler</span></code> который обязательно должен вернуть либо <code class="docutils literal notranslate"><span class="pre">Document</span></code>, либо <code class="docutils literal notranslate"><span class="pre">None</span></code>.</p>
<div class="highlight-python3 notranslate"><div class="highlight"><pre><span></span><span class="c1"># extract binary content from document if exist</span>
<span class="c1"># and put it into another exporter</span>

<span class="k">def</span> <span class="nf">handler</span><span class="p">(</span><span class="n">doc</span><span class="p">:</span> <span class="s2">"Document"</span><span class="p">,</span> <span class="nb">vars</span><span class="p">):</span>
    <span class="n">log</span><span class="p">:</span> <span class="s2">"Logger"</span> <span class="o">=</span> <span class="nb">vars</span><span class="p">[</span><span class="s1">'log'</span><span class="p">]</span>
    <span class="n">put_new_doc</span> <span class="o">=</span> <span class="nb">vars</span><span class="p">[</span><span class="s1">'put_new_doc'</span><span class="p">]</span>

    <span class="n">files</span><span class="p">:</span> <span class="p">[</span><span class="nb">dict</span><span class="p">]</span> <span class="o">=</span> <span class="n">doc</span><span class="o">.</span><span class="n">get_field</span><span class="p">(</span><span class="s1">'files'</span><span class="p">)</span>
    <span class="k">if</span> <span class="n">files</span><span class="p">:</span>
        <span class="k">for</span> <span class="n">file</span><span class="p">:</span> <span class="nb">dict</span> <span class="ow">in</span> <span class="n">files</span><span class="p">:</span>

            <span class="n">newDoc</span> <span class="o">=</span> <span class="n">Document</span><span class="p">(</span>
              <span class="n">taskId</span><span class="o">=</span><span class="n">doc</span><span class="o">.</span><span class="n">taskId</span><span class="p">,</span>
              <span class="n">taskName</span><span class="o">=</span><span class="n">doc</span><span class="o">.</span><span class="n">taskName</span><span class="p">,</span>
              <span class="n">reference</span><span class="o">=</span><span class="sa">f</span><span class="s1">'file_</span><span class="si">{</span><span class="n">doc</span><span class="o">.</span><span class="n">reference</span><span class="si">}</span><span class="s1">_</span><span class="si">{</span><span class="n">file</span><span class="p">[</span><span class="s2">"id"</span><span class="p">]</span><span class="si">}</span><span class="s1">'</span><span class="p">,</span>
              <span class="n">loootId</span><span class="o">=</span><span class="sa">f</span><span class="s1">''</span><span class="p">,</span>
              <span class="n">fields</span><span class="o">=</span><span class="n">file</span>
            <span class="p">)</span>

            <span class="n">newDoc</span><span class="o">.</span><span class="n">export</span> <span class="o">=</span> <span class="s1">'post_file'</span>
            <span class="n">put_new_doc</span><span class="p">(</span><span class="n">newDoc</span><span class="p">)</span>

            <span class="n">newDoc</span><span class="o">.</span><span class="n">export</span> <span class="o">=</span> <span class="s1">'post_file_info'</span>
            <span class="k">del</span> <span class="n">newDoc</span><span class="o">.</span><span class="n">fields</span><span class="p">[</span><span class="s1">'content'</span><span class="p">]</span>
            <span class="n">put_new_doc</span><span class="p">(</span><span class="n">newDoc</span><span class="p">)</span>

        <span class="k">del</span> <span class="n">doc</span><span class="o">.</span><span class="n">fields</span><span class="p">[</span><span class="s1">'files'</span><span class="p">]</span>
    <span class="k">else</span><span class="p">:</span>
        <span class="n">log</span><span class="o">.</span><span class="n">warning</span><span class="p">(</span><span class="sa">f</span><span class="s1">'Not found files in document </span><span class="si">{</span><span class="n">doc</span><span class="o">.</span><span class="n">reference</span><span class="si">}</span><span class="s1">'</span><span class="p">)</span>

    <span class="k">return</span> <span class="n">doc</span>
</pre></div>
</div>
<p>Для отладки можно импортировать модели данных</p>
<div class="highlight-python3 notranslate"><div class="highlight"><pre><span></span><span class="k">try</span><span class="p">:</span>
        <span class="kn">from</span> <span class="nn">models</span> <span class="kn">import</span> <span class="n">Document</span>
        <span class="kn">from</span> <span class="nn">lootnika</span> <span class="kn">import</span> <span class="n">sout</span>
<span class="k">except</span><span class="p">:</span>
        <span class="kn">from</span> <span class="nn">..models</span> <span class="kn">import</span> <span class="n">Document</span>
        <span class="kn">from</span> <span class="nn">..lootnika</span> <span class="kn">import</span> <span class="n">sout</span>

<span class="kn">from</span> <span class="nn">logging</span> <span class="kn">import</span> <span class="n">Logger</span>
</pre></div>
</div>
<div class="admonition tip">
<p class="admonition-title">Совет</p>
<p>Лутника может выполнять обработку в несколько потоков. см. <router-link class="reference internal" href="/index/config/config_core" to="/index/config/config_core"><span class="doc">handlerThreads</span></router-link></p>
</div>
<p>Список доступных экспортёров:</p>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2">lootnika binary</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2#format" v-scroll-to="'/index/config/config_export/exporter_lootnika_binary_index2#format'">Format</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2#extension" v-scroll-to="'/index/config/config_export/exporter_lootnika_binary_index2#extension'">Extension</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2#path" v-scroll-to="'/index/config/config_export/exporter_lootnika_binary_index2#path'">Path</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_binary_index2" to="/index/config/config_export/exporter_lootnika_binary_index2#failpath" v-scroll-to="'/index/config/config_export/exporter_lootnika_binary_index2#failpath'">FailPath</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index">lootnika text</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#format" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#format'">Format</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#encoding" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#encoding'">Encoding</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#ignoreencodingerrors" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#ignoreencodingerrors'">IgnoreEncodingErrors</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#extension" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#extension'">Extension</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#delimiter" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#delimiter'">Delimiter</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#lineterminator" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#lineterminator'">LineTerminator</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#quoting" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#quoting'">Quoting</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/config/config_export/exporter_lootnika_text_index" to="/index/config/config_export/exporter_lootnika_text_index#quotechar" v-scroll-to="'/index/config/config_export/exporter_lootnika_text_index#quotechar'">Quotechar</router-link></li>
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