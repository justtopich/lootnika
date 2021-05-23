<template>
  <div>
    
    <section id="id1">
<h1>Синтаксис команд<a class="headerlink" href="#id1" title="Ссылка на этот заголовок">¶</a></h1>
<p>Команды имеют следующий синтаксис:</p>
<p>a=<em>ActionName&amp;[Parameters]</em></p>
<dl class="simple">
<dt>Где:</dt><dd><ul class="simple">
<li><p><strong>ActionName</strong> - команда</p></li>
<li><p><strong>Parameters</strong> - параметры команды</p></li>
</ul>
</dd>
</dl>
<p>Параметры перечисляются через <strong>&amp;</strong> и могут быть в любом порядке. Например, команда на запуск задания под названием <em>DontWork</em>:</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="n">http</span><span class="p">:</span><span class="o">//</span><span class="n">localhost</span><span class="p">:</span><span class="mi">7252</span><span class="o">/</span><span class="ow">a=</span><span class="n">schedule</span><span class="o">?</span><span class="ow">cmd=</span><span class="n">Start</span><span class="o">&amp;</span><span class="ow">TaskName=</span><span class="n">DontWork</span>
</pre></div>
</div>
<p>Результат Лутника вернёт в формате json. Например, для вышеописанной команды результат будет такой:</p>
<div class="highlight-json notranslate"><div class="highlight"><pre><span></span><span class="p">{</span><span class="nt">"status"</span><span class="p">:</span> <span class="s2">"error"</span><span class="p">,</span> <span class="nt">"message"</span><span class="p">:</span> <span class="s2">"task undefined"</span><span class="p">}</span>
</pre></div>
</div>
<p>Команды <code class="xref std std-option docutils literal notranslate"><span class="pre">admin</span></code> и <code class="xref std std-option docutils literal notranslate"><span class="pre">help</span></code> вернут <strong>html</strong> страницы, остальные <strong>json</strong>. Последние всегда содержат минимум два поля:</p>
<blockquote>
<div><ul class="simple">
<li><p><strong>status</strong> - может иметь одно из двух значений: <em>ok</em> или <em>error</em>.</p></li>
<li><p><strong>message</strong> - сообщение от сервиса</p></li>
</ul>
</div></blockquote>
</section>
    <div></div>
    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>