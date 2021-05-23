<template>
  <div>
    
    <section id="server">
<h1>Секция Server<a class="headerlink" href="#server" title="Ссылка на этот заголовок">¶</a></h1>
<p>Здесь задаются параметры использования <router-link class="reference internal" href="/index/api" to="/index/api"><span class="doc">REST API</span></router-link>:</p>
<div class="contents local topic" id="id1">
<ul class="simple">
<li><p><a class="reference internal" href="#host">Host</a></p></li>
<li><p><a class="reference internal" href="#port">Port</a></p></li>
<li><p><a class="reference internal" href="#queryclients">QueryClients</a></p></li>
<li><p><a class="reference internal" href="#adminclients">AdminClients</a></p></li>
</ul>
</div>
<section id="host">
<h2>Host<a class="headerlink" href="#host" title="Ссылка на этот заголовок">¶</a></h2>
<p>Задаёт адрес на котором приложение будет ожидать команды.</p>
<p>Можно использовать как IP адрес, так и hostname.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">host</span><span class="o">=</span><span class="s">localost</span>
<span class="na">host</span><span class="o">=</span><span class="s">172.22.16.54</span>
</pre></div>
</div>
<div class="admonition warning">
<p class="admonition-title">Предупреждение</p>
<p>Лутника будет принимать команды только по заданному адресу.</p>
</div>
</section>
<section id="port">
<h2>Port<a class="headerlink" href="#port" title="Ссылка на этот заголовок">¶</a></h2>
<p>Задаёт порт на котором он будет ожидать команды.</p>
<p>Этот порт используется как для управления приложением, так и для управления заданиями.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">port</span><span class="o">=</span><span class="s">7252</span>
</pre></div>
</div>
</section>
<section id="queryclients">
<h2>QueryClients<a class="headerlink" href="#queryclients" title="Ссылка на этот заголовок">¶</a></h2>
<p>Список адресов для которых разрешено выполнять <router-link class="reference internal" href="/index/api/api_common" to="/index/api/api_common"><span class="doc">Общие команды</span></router-link>.</p>
<p>Можно использовать как IP адрес, так hostname или укажите <span class="guilabel">*</span> чтобы дать разрешения всем.
Разделитель <span class="guilabel">;</span> используется для перечисления нескольких адресов.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">QueryClients</span><span class="o">=</span><span class="s">*</span>
<span class="na">QueryClients</span><span class="o">=</span><span class="s">localhost; 172.22.16.54;myserver</span>
</pre></div>
</div>
<div class="admonition warning">
<p class="admonition-title">Предупреждение</p>
<p>Все входящие команды от клиентов вне этого списка будут отклонены.</p>
</div>
</section>
<section id="adminclients">
<h2>AdminClients<a class="headerlink" href="#adminclients" title="Ссылка на этот заголовок">¶</a></h2>
<p>Список адресов для которых разрешено выполнять <router-link class="reference internal" href="/index/api/api_control" to="/index/api/api_control"><span class="doc">Контрольные команды</span></router-link>.</p>
<p>Указанные здесь клиенты уже имеют уровень доступа <code class="xref std std-option docutils literal notranslate"><span class="pre">QueryClients</span></code> и добавлять их туда не имеет смыла. Указывайте здесь только те адреса, с которых необходимо управлять приложением.</p>
<p>Можно использовать как IP адрес, так hostname или укажите <span class="guilabel">*</span> чтобы дать разрешения всем.
Разделитель <span class="guilabel">;</span> используется для перечисления нескольких адресов.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">AdminClients</span><span class="o">=</span><span class="s">*</span>
<span class="na">AdminClients</span><span class="o">=</span><span class="s">localhost; 172.22.16.54;myserver</span>
</pre></div>
</div>
<div class="admonition warning">
<p class="admonition-title">Предупреждение</p>
<p>Все входящие команды от клиентов вне этого списка будут отклонены.</p>
</div>
</section>
</section>
    <div></div>
    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>