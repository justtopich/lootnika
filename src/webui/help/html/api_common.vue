<template>
  <div>
    <div class="section" id="id1">
<h1>Общие команды<a class="headerlink" href="#id1" title="Ссылка на этот заголовок">¶</a></h1>
<p>Команды для пользовательского использования.</p>
<p>Для выполнения этих команд клиент должен быть в списке <code class="xref std std-option docutils literal notranslate"><span class="pre">QueryClients</span></code>.</p>
<div class="contents local topic" id="id2">
<ul class="simple">
<li><p><a class="reference internal" href="#getstatus">GetStatus</a></p></li>
</ul>
</div>
<div class="section" id="getstatus">
<h2>GetStatus<a class="headerlink" href="#getstatus" title="Ссылка на этот заголовок">¶</a></h2>
<p>Получение сведений о Лутнике.</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">action=</span><span class="n">getstatus</span>
</pre></div>
</div>
<p>Вернёт в формате <strong>json</strong> сведения о Лутнике, о клиенте и некоторые параметры:</p>
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
<td><p>Строка</p></td>
<td><p>Время работы</p></td>
</tr>
<tr class="row-odd"><td><p>product</p></td>
<td><p>Строка</p></td>
<td><p>Название сборки Лутники</p></td>
</tr>
<tr class="row-even"><td><p>version</p></td>
<td><p>Строка</p></td>
<td><p>Версия</p></td>
</tr>
<tr class="row-odd"><td><p>directory</p></td>
<td><p>Строка</p></td>
<td><p>Рабочая папка</p></td>
</tr>
<tr class="row-even"><td><p>service_name</p></td>
<td><p>Строка</p></td>
<td><p>Название службы</p></td>
</tr>
<tr class="row-odd"><td><p>scheduler_status</p></td>
<td><p>Строка</p></td>
<td><dl class="simple">
<dt>Статус планировщика заданий. Может иметь один из следующих статусов:</dt><dd><ul class="simple">
<li><p><strong>ready</strong> - готов к новому циклу заданий.</p></li>
<li><p><strong>wait</strong> - ждёт время старта следующего повтора.</p></li>
<li><p><strong>work</strong> - выполняет цикл заданий.</p></li>
<li><p><strong>pause</strong> - планировщик приостановлен пользователем.</p></li>
<li><p><strong>cancel</strong> - остановка выполнения текущего цикла заданий</p></li>
</ul>
</dd>
</dl>
</td>
</tr>
<tr class="row-even"><td><p>client_host</p></td>
<td><p>Строка</p></td>
<td><p>Адрес клиента</p></td>
</tr>
<tr class="row-odd"><td><p>client_role</p></td>
<td><p>Строка</p></td>
<td><p>Уровень привилегий клиента</p></td>
</tr>
<tr class="row-even"><td><p>allow_actions</p></td>
<td><p>Строка</p></td>
<td><p>Доступные команды для клиента</p></td>
</tr>
</tbody>
</table>
</div>

    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>