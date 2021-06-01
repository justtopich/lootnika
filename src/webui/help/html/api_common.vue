<template>
  <div>
    
    <section id="id1">
<h1>Общие команды<a class="headerlink" href="#id1" title="Ссылка на этот заголовок">¶</a></h1>
<p>Команды для пользовательского использования.</p>
<p>Для выполнения этих команд клиент должен быть в списке <code class="xref std std-option docutils literal notranslate"><span class="pre">QueryClients</span></code>.</p>
<div class="contents local topic" id="id2">
<ul class="simple">
<li><p><a class="reference internal" href="#getinfo">GetInfo</a></p></li>
<li><p><a class="reference internal" href="#getstatus">GetStatus</a></p></li>
</ul>
</div>
<section id="getinfo">
<h2>GetInfo<a class="headerlink" href="#getinfo" title="Ссылка на этот заголовок">¶</a></h2>
<p>Получение общих сведений о Лутнике.</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">a=</span><span class="n">getinfo</span>
</pre></div>
</div>
<p>Возращаемые поля:</p>
<table class="colwidths-given docutils align-default">
<colgroup>
<col style="width: 25%"/>
<col style="width: 15%"/>
<col style="width: 60%"/>
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Поле</p></th>
<th class="head"><p>Формат</p></th>
<th class="head"><p>Значение</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p>product</p></td>
<td><p>строка</p></td>
<td><p>Название сборки Лутники</p></td>
</tr>
<tr class="row-odd"><td><p>version</p></td>
<td><p>строка</p></td>
<td><p>Версия</p></td>
</tr>
<tr class="row-even"><td><p>picker_type</p></td>
<td><p>строка</p></td>
<td><p>Используемы сборщик данных</p></td>
</tr>
<tr class="row-odd"><td><p>directory</p></td>
<td><p>строка</p></td>
<td><p>Рабочая папка</p></td>
</tr>
<tr class="row-even"><td><p>service_name</p></td>
<td><p>строка</p></td>
<td><p>Название службы</p></td>
</tr>
<tr class="row-odd"><td><p>client_host</p></td>
<td><p>строка</p></td>
<td><p>Адрес клиента</p></td>
</tr>
<tr class="row-even"><td><p>client_role</p></td>
<td><p>строка</p></td>
<td><p>Уровень привилегий клиента</p></td>
</tr>
<tr class="row-odd"><td><p>pid</p></td>
<td><p>число</p></td>
<td><p>PID процесса Лутники</p></td>
</tr>
<tr class="row-even"><td><p>pid_owner</p></td>
<td><p>строка</p></td>
<td><p>владелец процесса</p></td>
</tr>
</tbody>
</table>
</section>
<section id="getstatus">
<h2>GetStatus<a class="headerlink" href="#getstatus" title="Ссылка на этот заголовок">¶</a></h2>
<p>Получение сведений о работе Лутники.</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">a=</span><span class="n">getstatus</span>
</pre></div>
</div>
<p>Возращаемые поля:</p>
<table class="colwidths-given docutils align-default">
<colgroup>
<col style="width: 25%"/>
<col style="width: 15%"/>
<col style="width: 60%"/>
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Поле</p></th>
<th class="head"><p>Формат</p></th>
<th class="head"><p>Значение</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p>uptime</p></td>
<td><p>строка</p></td>
<td><p>Время работы</p></td>
</tr>
<tr class="row-odd"><td><p>cpu</p></td>
<td><p>число</p></td>
<td><p>информация о CPU</p></td>
</tr>
<tr class="row-even"><td><p>ram_total</p></td>
<td><p>число</p></td>
<td><p>общий размер памяти</p></td>
</tr>
<tr class="row-odd"><td><p>ram_percent</p></td>
<td><p>число</p></td>
<td><p>% занятой всей памяти</p></td>
</tr>
<tr class="row-even"><td><p>ram_used</p></td>
<td><p>число</p></td>
<td><p>размер занятой памяти</p></td>
</tr>
<tr class="row-odd"><td><p>ram_free</p></td>
<td><p>число</p></td>
<td><p>доступный размер реальной памяти (без swap)</p></td>
</tr>
<tr class="row-even"><td><p>ram_available</p></td>
<td><p>число</p></td>
<td><p>доступный размер всей памяти</p></td>
</tr>
<tr class="row-odd"><td><p>ram_lootnika_percent</p></td>
<td><p>число</p></td>
<td><p>% занятой памяти Лутникой</p></td>
</tr>
<tr class="row-even"><td><p>swap_total</p></td>
<td><p>число</p></td>
<td><p>общий размер SWAP памяти</p></td>
</tr>
<tr class="row-odd"><td><p>swap_used</p></td>
<td><p>число</p></td>
<td><p>размер использованного SWAP</p></td>
</tr>
<tr class="row-even"><td><p>swap_free</p></td>
<td><p>число</p></td>
<td><p>доступный размер SWAP</p></td>
</tr>
<tr class="row-odd"><td><p>swap_percent</p></td>
<td><p>число</p></td>
<td><p>% использованного SWAP</p></td>
</tr>
</tbody>
</table>
<p>Подробности про статистику использования ресурсов смотрите в официальной документации <a class="reference external" href="https://psutil.readthedocs.io/">psutil</a>.</p>
</section>
</section>
    <div></div>
    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>