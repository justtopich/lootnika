<template>
  <div>
    
    <section id="lootnika-text">
<h1>lootnika text<a class="headerlink" href="#lootnika-text" title="Ссылка на этот заголовок">¶</a></h1>
<p>Экспорт документов в текстовые форматы.</p>
<div class="contents local topic" id="id1">
<ul class="simple">
<li><p><a class="reference internal" href="#format">Format</a></p></li>
<li><p><a class="reference internal" href="#encoding">Encoding</a></p></li>
<li><p><a class="reference internal" href="#ignoreencodingerrors">IgnoreEncodingErrors</a></p></li>
<li><p><a class="reference internal" href="#extension">Extension</a></p></li>
<li><p><a class="reference internal" href="#delimiter">Delimiter</a></p></li>
<li><p><a class="reference internal" href="#lineterminator">LineTerminator</a></p></li>
<li><p><a class="reference internal" href="#quoting">Quoting</a></p></li>
<li><p><a class="reference internal" href="#quotechar">Quotechar</a></p></li>
<li><p><a class="reference internal" href="#path">Path</a></p></li>
<li><p><a class="reference internal" href="#failpath">FailPath</a></p></li>
</ul>
</div>
<section id="format">
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
</section>
<section id="encoding">
<h2>Encoding<a class="headerlink" href="#encoding" title="Ссылка на этот заголовок">¶</a></h2>
<p>Кодировка документа.</p>
<p>По умолчанию для сохранения документов используется кодировка UTF-8, но можете указать иную доступную для Python3</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Encoding</span> <span class="o">=</span> <span class="s">ansii</span>
</pre></div>
</div>
</section>
<section id="ignoreencodingerrors">
<h2>IgnoreEncodingErrors<a class="headerlink" href="#ignoreencodingerrors" title="Ссылка на этот заголовок">¶</a></h2>
<p>Игнорировать ошибки кодировки</p>
<p>Пропускать проблемные символы которые нельзя сохранить в выбранной кодировке.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">ignoreEncodingErrors</span> <span class="o">=</span> <span class="s">true</span>
</pre></div>
</div>
<div class="admonition attention">
<p class="admonition-title">Внимание</p>
<p>При активации этого параметра нет гарантии что документ будет корректно сохранён!</p>
</div>
</section>
<section id="extension">
<h2>Extension<a class="headerlink" href="#extension" title="Ссылка на этот заголовок">¶</a></h2>
<p>Расширение файла.</p>
<p>Если не задано, то <strong>lootnika_text</strong> будет сохранять в <code class="docutils literal notranslate"><span class="pre">json</span></code>.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Extension</span> <span class="o">=</span> <span class="s">txt</span>
</pre></div>
</div>
</section>
<section id="delimiter">
<h2>Delimiter<a class="headerlink" href="#delimiter" title="Ссылка на этот заголовок">¶</a></h2>
<p>Разделитель полей.</p>
<p>По умолчанию используется <span class="guilabel">,</span></p>
<p>Доступен при использовании формата <strong>csv</strong></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Delimiter</span> <span class="o">=</span> <span class="s">|</span>
</pre></div>
</div>
</section>
<section id="lineterminator">
<h2>LineTerminator<a class="headerlink" href="#lineterminator" title="Ссылка на этот заголовок">¶</a></h2>
<p>Разделитель строки.</p>
<p>По умолчанию используется <span class="guilabel">\n</span></p>
<p>Доступен при использовании формата <strong>csv</strong></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">LineTerminator</span> <span class="o">=</span> <span class="s">\r\n</span>
</pre></div>
</div>
</section>
<section id="quoting">
<h2>Quoting<a class="headerlink" href="#quoting" title="Ссылка на этот заголовок">¶</a></h2>
<p>Режим экранирования.</p>
<p>Доступны:</p>
<ul class="simple">
<li><p>NONE</p></li>
<li><p>MINIMAL - только спец символы</p></li>
<li><p>ALL - всю строку</p></li>
</ul>
<p>По умолчанию используется <span class="guilabel">MINIMAL</span></p>
<p>Доступен при использовании формата <strong>csv</strong></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Quoting</span> <span class="o">=</span> <span class="s">None</span>
</pre></div>
</div>
</section>
<section id="quotechar">
<h2>Quotechar<a class="headerlink" href="#quotechar" title="Ссылка на этот заголовок">¶</a></h2>
<p>Экранирующий символ.</p>
<p>По умолчанию используется <code class="xref std std-option docutils literal notranslate"><span class="pre">"</span></code></p>
<p>Доступен при использовании формата <strong>csv</strong></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">quotechar</span> <span class="o">=</span> <span class="s">'</span>
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