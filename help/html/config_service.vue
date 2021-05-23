<template>
  <div>
    
    <section id="service">
<h1>Секция Service<a class="headerlink" href="#service" title="Ссылка на этот заголовок">¶</a></h1>
<p>Параметры службы Windows.</p>
<p>Данные параметры используются для установки, удаления и изменения службы приложения.
Это позволит работать вне зависимости от статуса пользователя, а так же задать параметры автоматического запуска, от имени какого пользователя запускать и т.д.</p>
<div class="admonition attention">
<p class="admonition-title">Внимание</p>
<p>Установка, удаление и изменение служб производится через исполняемый файл с правами администратора.</p>
</div>
<p>Доступны следующие параметры:</p>
<div class="contents local topic" id="id1">
<ul class="simple">
<li><p><a class="reference internal" href="#name">Name</a></p></li>
<li><p><a class="reference internal" href="#displayname">DisplayName</a></p></li>
<li><p><a class="reference internal" href="#description">Description</a></p></li>
</ul>
</div>
<section id="name">
<h2>Name<a class="headerlink" href="#name" title="Ссылка на этот заголовок">¶</a></h2>
<p>Имя службы. Оно используется для идентификации службы и будет отображаться в диспетчере задач.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Name</span> <span class="o">=</span> <span class="s">LootnikaSvc</span>
</pre></div>
</div>
</section>
<section id="displayname">
<h2>DisplayName<a class="headerlink" href="#displayname" title="Ссылка на этот заголовок">¶</a></h2>
<p>Название службы которое будет отображаться в диспетчере служб.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">DisplayName</span> <span class="o">=</span> <span class="s">Lootnika Service</span>
</pre></div>
</div>
</section>
<section id="description">
<h2>Description<a class="headerlink" href="#description" title="Ссылка на этот заголовок">¶</a></h2>
<p>Описание службы.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Description</span> <span class="o">=</span> <span class="s">Lootnika data collector</span>
</pre></div>
</div>
</section>
</section>
    <div></div>
    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>