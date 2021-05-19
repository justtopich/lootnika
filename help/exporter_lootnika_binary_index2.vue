<template>
  <div>
    
    <section id="lootnika-binary">
<h1>lootnika_binary<a class="headerlink" href="#lootnika-binary" title="Ссылка на этот заголовок">¶</a></h1>
<p>Экспорт документов в простые файлы.</p>
<div class="contents local topic" id="id1">
<ul class="simple">
<li><p><a class="reference internal" href="#format">Format</a></p></li>
<li><p><a class="reference internal" href="#extension">Extension</a></p></li>
<li><p><a class="reference internal" href="#path">Path</a></p></li>
<li><p><a class="reference internal" href="#failpath">FailPath</a></p></li>
</ul>
</div>
<section id="format">
<h2>Format<a class="headerlink" href="#format" title="Ссылка на этот заголовок">¶</a></h2>
<p>Формат документа.</p>
<p>Для каждого типа экспорта доступны свои форматы документов. Доступные форматы расположены в папке <code class="file docutils literal notranslate"><span class="pre">formats</span></code> в папке экспортёра. Например, для <code class="docutils literal notranslate"><span class="pre">lootnika_binary</span></code> это <code class="file docutils literal notranslate"><span class="pre">exporters/lootnika_binary/formats/</span></code></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Format</span> <span class="o">=</span> <span class="s">avro</span>
</pre></div>
</div>
<div class="admonition note">
<p class="admonition-title">Примечание</p>
<p>Этот параметр обязателен для любого типа экспорта</p>
</div>
</section>
<section id="extension">
<h2>Extension<a class="headerlink" href="#extension" title="Ссылка на этот заголовок">¶</a></h2>
<p>Расширение файла.</p>
<p>Если не задано, то <strong>lootnika_binary</strong> будет сохранять в <code class="docutils literal notranslate"><span class="pre">bson</span></code>.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Extension</span> <span class="o">=</span> <span class="s">bson</span>
</pre></div>
</div>
</section>
<section id="path">
<h2>Path<a class="headerlink" href="#path" title="Ссылка на этот заголовок">¶</a></h2>
<p>Путь сохранение документов.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">path</span> <span class="o">=</span> <span class="s">outgoing/mytask</span>
</pre></div>
</div>
</section>
<section id="failpath">
<h2>FailPath<a class="headerlink" href="#failpath" title="Ссылка на этот заголовок">¶</a></h2>
<p>Директория сохранения документов в случае неудачного экспорта.</p>
<p>Коннектор будет создавать уникальную папку для каждого исполняемого экземпляра задания. Если одно задание выполнялось 3 раза и при каждом выполнении были неудачные попытки экспорта, то будут созданы 3 папки содержащие итоговые документы. Вы сможете сами отправить их на обработку без необходимости повторного выполнения задания.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">FailPath</span> <span class="o">=</span> <span class="s">txt</span>
</pre></div>
</div>
</section>
</section>
    <div></div>
    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>