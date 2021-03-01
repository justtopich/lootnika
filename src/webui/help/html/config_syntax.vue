<template>
  <div>
    <div class="section" id="id1">
<h1>Синтаксис настроек<a class="headerlink" href="#id1" title="Ссылка на этот заголовок">¶</a></h1>
<p>Конфигурационный файл состоит из секций, в котором есть параметры относящейся к ней.
Имеет следующую структуру:</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="k">[Секция1]</span>
<span class="na">Параметр1</span><span class="o">=</span><span class="s">значение</span>
<span class="na">Параметр2</span> <span class="o">=</span> <span class="s">значение</span>

<span class="k">[Секция2]</span>
<span class="na">Параметр1</span> <span class="o">=</span> <span class="s">значение</span>
<span class="na">Параметр2</span><span class="o">=</span><span class="s">значение</span>
<span class="c1">; комментарий</span>
<span class="c1"># это тоже комментарий</span>
</pre></div>
</div>
<p>Название каждой секции обозначено квадратными скобками (например, <code class="xref std std-option docutils literal notranslate"><span class="pre">[server]</span></code>). Секции не должны повторяться и могут находится в любом порядке. Параметр относится к секции до тех пор, пока не будет объявлена новая. Значения параметров пишутся в одну строку.</p>
<div class="admonition tip">
<p class="admonition-title">Совет</p>
<p>В параметрах при указании путей используйте обратные слешы <span class="guilabel">/</span> вместо <span class="guilabel">\</span>
Если в пути есть пробелы - укажите его в кавычках: <code class="docutils literal notranslate"><span class="pre">"home/var</span> <span class="pre">load/lootnika"</span></code></p>
</div>
<p>Файл должен быть в кодировке UTF-8.</p>

    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>