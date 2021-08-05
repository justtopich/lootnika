<template>
  <div>
    
    <section id="core">
<h1>Секция Core<a class="headerlink" href="#core" title="Ссылка на этот заголовок">¶</a></h1>
<p>Параметры основных компонентов Лутники.</p>
<p>Параметры в этой секции так или иначе могут влиять на работу всех остальных компонентов, таких как сборщики, экспортёры
расписание, REST сервер и т.д.</p>
<p>Список доступных параметров:</p>
<div class="contents local topic" id="id1">
<ul class="simple">
<li><p><a class="reference internal" href="#handlerthreads">handlerThreads</a></p></li>
</ul>
</div>
<section id="handlerthreads">
<h2>handlerThreads<a class="headerlink" href="#handlerthreads" title="Ссылка на этот заголовок">¶</a></h2>
<p>Количество потоков обработчиков.</p>
<p>Для каждого экспортёра можно указать обработчиков документов (см. <router-link class="reference internal" href="/index/config/config_export" to="/index/config/config_export"><span class="doc">Handlers</span></router-link>.). Все обработчики из всех заданий используют единый пул ресурсов.
Этим параметром можно регулировать сколько обработчиков будет работать параллельно. К примеру, если обработка документа
связана с длительным ожиданием внешнего фактора, то рационально использовать большой пул потоков. Если же обработка сильно
нагружает ресурсы, то наоборот - уменьшить пул.</p>
<div class="admonition attention">
<p class="admonition-title">Внимание</p>
<p>Лутника использует виртуальные потоки, которые выполняются в одном процессе (одно ядро CPU)</p>
</div>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">handlerThreads</span> <span class="o">=</span> <span class="s">8</span>
</pre></div>
</div>
</section>
</section>
    <div></div>
    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>