<template>
  <div>
    <div class="section" id="export">
<h1>Секция Export<a class="headerlink" href="#export" title="Ссылка на этот заголовок">¶</a></h1>
<p>Параметры экспорта документов.</p>
<p>Здесь задаются формат и место назначения данных, которая Лутника загрузила из источника.
Варианты экспорта зависят от используемых модулей. В состав данной версии входит <strong>lootnika_text</strong> который умеет сохранять документы в формат <strong>json</strong> и <strong>csv</strong>.</p>
<p>Вы можете использовать одновременно несколько разных экспортёров, а так же назначить для каждого задания свой (см. <router-link class="reference internal" href="/api/api_control" to="/api/api_control"><span class="doc">Schedule: TasksInfo</span></router-link>). Если задание не ссылается ни на какой экспорт, то для него Лутника будет использовать секцию <code class="xref std std-option docutils literal notranslate"><span class="pre">[export]</span></code>. Если такой секции нет, то Лутника создаст его с типом <code class="docutils literal notranslate"><span class="pre">lootnika_text</span></code> и форматом <code class="docutils literal notranslate"><span class="pre">json</span></code>.</p>
<div class="admonition attention">
<p class="admonition-title">Внимание</p>
<p>Набор доступных параметров зависит от используемого экспортёра.</p>
</div>
<p>Список доступных параметров:</p>
<div class="contents local topic" id="id1">
<ul class="simple">
<li><p><a class="reference internal" href="#type">Type</a></p></li>
<li><p><a class="reference internal" href="#format">Format</a></p></li>
<li><p><a class="reference internal" href="#extension">Extension</a></p></li>
<li><p><a class="reference internal" href="#batchsize">BatchSize</a></p></li>
<li><p><a class="reference internal" href="#delimiter">Delimiter</a></p></li>
<li><p><a class="reference internal" href="#path">Path</a></p></li>
<li><p><a class="reference internal" href="#failpath">FailPath</a></p></li>
</ul>
</div>
<div class="section" id="type">
<h2>Type<a class="headerlink" href="#type" title="Ссылка на этот заголовок">¶</a></h2>
<p>Тип экспортёра.</p>
<p>Доступные экспортёры расположены в папке <code class="file docutils literal notranslate"><span class="pre">exporters</span></code>.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">type</span> <span class="o">=</span> <span class="s">lootnika_text</span>
</pre></div>
</div>
<div class="admonition note">
<p class="admonition-title">Примечание</p>
<p>Этот параметр обязателен для любого типа экспорта</p>
</div>
</div>
<div class="section" id="format">
<h2>Format<a class="headerlink" href="#format" title="Ссылка на этот заголовок">¶</a></h2>
<p>Формат документа.</p>
<p>Для каждого типа экспорта доступны свои форматы документов. Доступные форматы расположены в папке <code class="file docutils literal notranslate"><span class="pre">formats</span></code> в папке экспортёра. Например, для <code class="docutils literal notranslate"><span class="pre">lootnika_text</span></code> это <code class="file docutils literal notranslate"><span class="pre">exporters/lootnika_text/formats/</span></code></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Format</span> <span class="o">=</span> <span class="s">avro</span>
</pre></div>
</div>
<div class="admonition note">
<p class="admonition-title">Примечание</p>
<p>Этот параметр обязателен для любого типа экспорта</p>
</div>
</div>
<div class="section" id="extension">
<h2>Extension<a class="headerlink" href="#extension" title="Ссылка на этот заголовок">¶</a></h2>
<p>Расширение файла.</p>
<p>Если не задано, то <strong>lootnika_text</strong> будет сохранять в <code class="docutils literal notranslate"><span class="pre">json</span></code>.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Extension</span> <span class="o">=</span> <span class="s">txt</span>
</pre></div>
</div>
</div>
<div class="section" id="batchsize">
<h2>BatchSize<a class="headerlink" href="#batchsize" title="Ссылка на этот заголовок">¶</a></h2>
<p>Размер очереди на экспорт.</p>
<p>Чем больше метаданных в документах, тем меньше указывайте размер очереди.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">BatchSize</span> <span class="o">=</span> <span class="s">100</span>
</pre></div>
</div>
<div class="admonition note">
<p class="admonition-title">Примечание</p>
<p>Этот параметр обязателен для любого типа экспорта</p>
</div>
</div>
<div class="section" id="delimiter">
<h2>Delimiter<a class="headerlink" href="#delimiter" title="Ссылка на этот заголовок">¶</a></h2>
<p>Разделитель полей.</p>
<p>Доступен при использовании формата <code class="docutils literal notranslate"><span class="pre">csv</span></code></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Delimiter</span> <span class="o">=</span> <span class="s">|</span>
</pre></div>
</div>
</div>
<div class="section" id="path">
<h2>Path<a class="headerlink" href="#path" title="Ссылка на этот заголовок">¶</a></h2>
<p>Путь сохранение документов.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">path</span> <span class="o">=</span> <span class="s">outgoing/mytask</span>
</pre></div>
</div>
</div>
<div class="section" id="failpath">
<h2>FailPath<a class="headerlink" href="#failpath" title="Ссылка на этот заголовок">¶</a></h2>
<p>Директория сохранения документов в случае неудачного экспорта.</p>
<p>Коннектор будет создавать уникальную папку для каждого исполняемого экземпляра задания. Если одно задание выполнялось 3 раза и при каждом выполнении были неудачные попытки экспорта, то будут созданы 3 папки содержащие итоговые документы. Вы сможете сами отправить их на обработку без необходимости повторного выполнения задания.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">FailPath</span> <span class="o">=</span> <span class="s">txt</span>
</pre></div>
</div>
</div>

    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>