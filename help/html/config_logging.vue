<template>
  <div>
    
    <section id="logging">
<h1>Секция Logging<a class="headerlink" href="#logging" title="Ссылка на этот заголовок">¶</a></h1>
<p>Параметры журналов событий работы приложения и хода выполнении заданий.</p>
<p>Лутника логирует все события в следующие файлы:</p>
<ul class="simple">
<li><p><strong>lootnika.log</strong> - журнал основных событий.</p></li>
<li><p><strong>rest.log</strong> - журнал исполнения REST запросов</p></li>
<li><p><strong>taskName.log</strong> - журнал событий задания. Для каждого задания создаётся свой журнал с именем задания.</p></li>
</ul>
<p>Доступны следующие параметры:</p>
<div class="contents local topic" id="id1">
<ul class="simple">
<li><p><a class="reference internal" href="#enable">Enable</a></p></li>
<li><p><a class="reference internal" href="#loglevel">LogLevel</a></p></li>
<li><p><a class="reference internal" href="#logmaxsizekbs">LogMaxSizeKbs</a></p></li>
<li><p><a class="reference internal" href="#logmaxfiles">LogMaxFiles</a></p></li>
</ul>
</div>
<section id="enable">
<h2>Enable<a class="headerlink" href="#enable" title="Ссылка на этот заголовок">¶</a></h2>
<p>Булево значение отвечающее за активацию журналирования.</p>
<p>При использовании <code class="docutils literal notranslate"><span class="pre">False</span></code> Лутника не будет вести никаких записей, но они всё равно будут выводится в консоль.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Enable</span> <span class="o">=</span> <span class="s">True</span>
</pre></div>
</div>
</section>
<section id="loglevel">
<h2>LogLevel<a class="headerlink" href="#loglevel" title="Ссылка на этот заголовок">¶</a></h2>
<p>Уровень событий которые будут записаны.</p>
<p>Доступно два уровня:</p>
<ul class="simple">
<li><p><strong>Full</strong> - запись всех событий включая <em>debug</em>.</p></li>
<li><p><strong>Normal</strong> - запись событий уровня <em>info</em> и выше.</p></li>
</ul>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">LogLevel</span> <span class="o">=</span> <span class="s">Full</span>
</pre></div>
</div>
</section>
<section id="logmaxsizekbs">
<h2>LogMaxSizeKbs<a class="headerlink" href="#logmaxsizekbs" title="Ссылка на этот заголовок">¶</a></h2>
<p>Максимальный размер файла журнала.</p>
<p>При достижении заданного лимита запись начнётся в новый файл, а предыдущий будет переименован.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">LogMaxSizeKbs</span> <span class="o">=</span> <span class="s">200</span>
</pre></div>
</div>
</section>
<section id="logmaxfiles">
<h2>LogMaxFiles<a class="headerlink" href="#logmaxfiles" title="Ссылка на этот заголовок">¶</a></h2>
<p>Максимальное количество файлов журнала.</p>
<p>При достижении заданного лимита Лутника будет удалять самые первые переименованные файлы.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">LogMaxFiles</span> <span class="o">=</span> <span class="s">50</span>
</pre></div>
</div>
</section>
</section>
    <div></div>
    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>