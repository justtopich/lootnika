<template>
  <div>
    <div class="section" id="diskusage">
<h1>Секция DiskUsage<a class="headerlink" href="#diskusage" title="Ссылка на этот заголовок">¶</a></h1>
<p>Отслеживание свободного места на диске сервера.</p>
<p>Во время выполнения заданий Лутника может отслеживать свободное место на заданном диске. Если во время выполнения задания по каким-то причинам будет достигнут лимит свободного места, то Лутника приостанавливает выполнение задания и переходит в режиме ожидания на <strong>30 минут</strong>. Если по истечению этого времени свободное места так и не станет больше заданного лимита - Лутника остановит выполнение текущего задания.</p>
<p>Доступны следующие параметры:</p>
<div class="contents local topic" id="id1">
<ul class="simple">
<li><p><a class="reference internal" href="#pathwatch">PathWatch</a></p></li>
<li><p><a class="reference internal" href="#critfreegb">CritFreeGb</a></p></li>
</ul>
</div>
<div class="section" id="pathwatch">
<h2>PathWatch<a class="headerlink" href="#pathwatch" title="Ссылка на этот заголовок">¶</a></h2>
<p>Диск, за свободным местом которого необходимо следить.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">PathWatch</span> <span class="o">=</span> <span class="s">C:\</span>
</pre></div>
</div>
</div>
<div class="section" id="critfreegb">
<h2>CritFreeGb<a class="headerlink" href="#critfreegb" title="Ссылка на этот заголовок">¶</a></h2>
<p>Минимальный размер свободного места. Измеряется в ГБ.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">CritFreeGb</span> <span class="o">=</span> <span class="s">10</span>
</pre></div>
</div>
</div>

    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>