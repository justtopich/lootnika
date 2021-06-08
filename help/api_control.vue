<template>
  <div>
    
    <section id="id1">
<h1>Контрольные команды<a class="headerlink" href="#id1" title="Ссылка на этот заголовок">¶</a></h1>
<p>Команды, которые используются для контроля работы Лутники.</p>
<div class="contents local topic" id="id2">
<ul class="simple">
<li><p><a class="reference internal" href="#stop">Stop</a></p></li>
<li><p><a class="reference internal" href="#schedule">Schedule</a></p>
<ul>
<li><p><a class="reference internal" href="#schedule-tasksinfo">Schedule: TasksInfo</a></p></li>
<li><p><a class="reference internal" href="#schedule-queueinfo">Schedule: QueueInfo</a></p></li>
<li><p><a class="reference internal" href="#schedule-start">Schedule: Start</a></p></li>
<li><p><a class="reference internal" href="#schedule-pause">Schedule: Pause</a></p></li>
<li><p><a class="reference internal" href="#schedule-cancel">Schedule: Cancel</a></p></li>
</ul>
</li>
<li><p><a class="reference internal" href="#log">Log</a></p></li>
</ul>
</div>
<section id="stop">
<h2>Stop<a class="headerlink" href="#stop" title="Ссылка на этот заголовок">¶</a></h2>
<p>Остановка Лутники.</p>
<p>Настоятельно рекомендуется останавливать Лутнику либо через службу, либо данной командой, либо через консоль комбинацией <kbd class="kbd docutils literal notranslate">ctrl</kbd> + <kbd class="kbd docutils literal notranslate">c</kbd>.
При штатной остановке Лутники прекращает выполнять задания, экспортирует документы которые успела получить и сохраняет все данные в журнал заданий.</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">a=</span><span class="n">stop</span>
</pre></div>
</div>
</section>
<section id="schedule">
<h2>Schedule<a class="headerlink" href="#schedule" title="Ссылка на этот заголовок">¶</a></h2>
<p>Управление заданиями.</p>
<p>Вы можете запускать и останавливать задания, а так же следить за ходом их выполнения.
Все команды планировщика задания задаются в параметре <code class="xref std std-option docutils literal notranslate"><span class="pre">cmd</span></code></p>
<section id="schedule-tasksinfo">
<h3>Schedule: TasksInfo<a class="headerlink" href="#schedule-tasksinfo" title="Ссылка на этот заголовок">¶</a></h3>
<p>Получение заданий и их параметров.</p>
<p>Лутника вернёт только те задания, которые объявлены в секции <router-link class="reference internal" href="/index/config/config_schedule" to="/index/config/config_schedule"><span class="doc">Schedule</span></router-link>.</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">a=</span><span class="n">schedule</span><span class="o">?</span><span class="ow">cmd=</span><span class="n">TasksInfo</span>
</pre></div>
</div>
<div class="admonition warning">
<p class="admonition-title">Предупреждение</p>
<p>Параметры заданий могут отличаться от таковых в настройках. Такое происходит после инициализации задания и нужны для работы Лутники. В настройках эти изменения не сохраняются.</p>
</div>
</section>
<section id="schedule-queueinfo">
<h3>Schedule: QueueInfo<a class="headerlink" href="#schedule-queueinfo" title="Ссылка на этот заголовок">¶</a></h3>
<p>Просмотр журнал заданий.</p>
<p>Получение списка завершённых и текущих заданий, их статуса и прогресса выполнения. По умолчанию вернёт 20 последних записей.</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">a=</span><span class="n">schedule</span><span class="o">?</span><span class="ow">cmd=</span><span class="n">QueueInfo</span><span class="o">&amp;</span><span class="ow">taskName=</span><span class="n">news</span><span class="p">,</span><span class="n">posts</span><span class="o">&amp;</span><span class="ow">limit=</span><span class="mi">100</span>
</pre></div>
</div>
<dl class="simple">
<dt>Дополнительные параметры:</dt><dd><ul class="simple">
<li><p><strong>taskName</strong> - список заданий по которым делать выборку. Задания перечисляются через запятую</p></li>
<li><p><strong>start</strong> - указывает пропустить указанное число заданий, прежде чем выдать результат</p></li>
<li><p><strong>limit</strong> - ограничение размера выдачи</p></li>
</ul>
</dd>
</dl>
<p>Команда вернёт следующие поля:</p>
<table class="colwidths-given docutils align-default">
<colgroup>
<col style="width: 20%"/>
<col style="width: 10%"/>
<col style="width: 70%"/>
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Поле</p></th>
<th class="head"><p>Формат</p></th>
<th class="head"><p>Значение</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p>scheduler_status</p></td>
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
<tr class="row-odd"><td><p>next_start_time</p></td>
<td><p>Строка</p></td>
<td><p>Дата и время следующего старта заданий</p></td>
</tr>
<tr class="row-even"><td><p>cycles_left</p></td>
<td><p>Число</p></td>
<td><p>Количество оставшихся повторов заданий. Значение <em>-1</em> означает бесконечное повторение.</p></td>
</tr>
<tr class="row-odd"><td><p>Tasks</p></td>
<td><p>Массив</p></td>
<td><p>Статистика заданий</p></td>
</tr>
</tbody>
</table>
<p>Объект <code class="docutils literal notranslate"><span class="pre">tasks</span></code> содержит объекты со следующим набором полей:</p>
<table class="colwidths-given docutils align-default">
<colgroup>
<col style="width: 25%"/>
<col style="width: 10%"/>
<col style="width: 65%"/>
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Поле</p></th>
<th class="head"><p>Формат</p></th>
<th class="head"><p>Значение</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p>id</p></td>
<td><p>Число</p></td>
<td><p>ID задания</p></td>
</tr>
<tr class="row-odd"><td><p>name</p></td>
<td><p>Строка</p></td>
<td><p>Имя задания</p></td>
</tr>
<tr class="row-even"><td><p>start_time</p></td>
<td><p>Строка</p></td>
<td><p>Время старта задания</p></td>
</tr>
<tr class="row-odd"><td><p>end_time</p></td>
<td><p>Строка</p></td>
<td><p>Последнее время обновления статуса задания</p></td>
</tr>
<tr class="row-even"><td><p>status</p></td>
<td><p>Строка</p></td>
<td><dl class="simple">
<dt>Статус задания. Задание может иметь одно из следующих:</dt><dd><ul class="simple">
<li><p><strong>run</strong> - выполняется</p></li>
<li><p><strong>pause</strong> - приостановлено</p></li>
<li><p><strong>complete</strong> - выполнено</p></li>
<li><p><strong>cancel</strong> - отменено</p></li>
<li><p><strong>fail</strong> - не выполнено или прервано</p></li>
</ul>
</dd>
</dl>
</td>
</tr>
<tr class="row-odd"><td><p>count_total</p></td>
<td><p>Число</p></td>
<td><p>Кол-во документов которые будут обработаны</p></td>
</tr>
<tr class="row-even"><td><p>count_seen</p></td>
<td><p>Число</p></td>
<td><p>Кол-во документов которые коннектор просмотрел</p></td>
</tr>
<tr class="row-odd"><td><p>count_new</p></td>
<td><p>Число</p></td>
<td><p>Кол-во новых документов</p></td>
</tr>
<tr class="row-even"><td><p>count_differ</p></td>
<td><p>Число</p></td>
<td><p>Кол-во изменённых документов</p></td>
</tr>
<tr class="row-odd"><td><p>count_delete</p></td>
<td><p>Число</p></td>
<td><p>Кол-во удалённых документов</p></td>
</tr>
<tr class="row-even"><td><p>count_task_error</p></td>
<td><p>Число</p></td>
<td><p>Кол-во ошибок возникших во время выполнения задания</p></td>
</tr>
<tr class="row-odd"><td><p>count_export_error</p></td>
<td><p>Число</p></td>
<td><p>Кол-во ошибок связанных с экспортом документов</p></td>
</tr>
<tr class="row-even"><td><p>last_doc_id</p></td>
<td><p>Строка</p></td>
<td><p>ID последнего обработанного документа</p></td>
</tr>
</tbody>
</table>
</section>
<section id="schedule-start">
<h3>Schedule: Start<a class="headerlink" href="#schedule-start" title="Ссылка на этот заголовок">¶</a></h3>
<p>Старт или возобновление заданий.</p>
<p>Запускает цикл заданий, даже если расписание выключено (см. <router-link class="reference internal" href="/index/config/config_schedule" to="/index/config/config_schedule"><span class="doc">Schedule</span></router-link> ). Выполнение этих заданий произойдёт один раз в порядке, указанном в настройках.</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">a=</span><span class="n">schedule</span><span class="o">?</span><span class="ow">cmd=</span><span class="n">Start</span>
</pre></div>
</div>
<p>Используя параметр <code class="xref std std-option docutils literal notranslate"><span class="pre">TaskName</span></code> можно запустить одну конкретную задачу:</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">a=</span><span class="n">schedule</span><span class="o">?</span><span class="ow">cmd=</span><span class="n">Start</span><span class="o">&amp;</span><span class="ow">TaskName=</span><span class="n">FuriKuri</span>
</pre></div>
</div>
<p>Этот параметр обязателен при возобновлении задания.</p>
<div class="admonition attention">
<p class="admonition-title">Внимание</p>
<p>Таким способом можно запустить только те задания, которые заданы в расписании.
Счётчик выполнений <router-link class="reference internal" href="/index/config/config_schedule" to="/index/config/config_schedule"><span class="doc">Schedule: TaskCycles</span></router-link> не учитывает задания запущенные таким образом.</p>
</div>
</section>
<section id="schedule-pause">
<h3>Schedule: Pause<a class="headerlink" href="#schedule-pause" title="Ссылка на этот заголовок">¶</a></h3>
<p>Приостановка выполнения заданий.</p>
<p>Приостановка выполняется на неограниченное время, однако, отсчёт времени старта до следующего цикла продолжается. Если наступит время выполнения очередного цикла задания во время паузы - запуск будет засчитан счётчиком заданий <router-link class="reference internal" href="/index/config/config_schedule" to="/index/config/config_schedule"><span class="doc">TaskCycles</span></router-link>, но цикл будет пропущен, т.к. Лутника не может выполнять несколько заданий одновременно.</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">a=</span><span class="n">schedule</span><span class="o">?</span><span class="ow">cmd=</span><span class="n">Pause</span>
</pre></div>
</div>
</section>
<section id="schedule-cancel">
<h3>Schedule: Cancel<a class="headerlink" href="#schedule-cancel" title="Ссылка на этот заголовок">¶</a></h3>
<p>Отмена выполнения заданий.</p>
<p>Если во время отмены выполняется задание из цикла, будет прерван весь цикл.
При отмене Лутника выполнит экспорт всех документов что успела собрать, но при этом не будет отправлять команду на удаление старых документов из источника.</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">a=</span><span class="n">schedule</span><span class="o">?</span><span class="ow">cmd=</span><span class="n">Cancel</span>
</pre></div>
</div>
</section>
</section>
<section id="log">
<h2>Log<a class="headerlink" href="#log" title="Ссылка на этот заголовок">¶</a></h2>
<p>Чтение журналов событий.</p>
<p>Лутника позволяет как просматривать содержимое логов, так и скачивать их. Но для таких операций всегда нужно указывать
конкретный файл.</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">a=</span><span class="n">log</span><span class="o">?</span><span class="ow">cmd=</span><span class="n">list</span>
</pre></div>
</div>
<div class="highlight-json notranslate"><div class="highlight"><pre><span></span><span class="p">{</span><span class="nt">"files"</span><span class="p">:</span> <span class="p">[</span><span class="s2">"lootnika.log"</span><span class="p">,</span> <span class="s2">"rest.log"</span><span class="p">,</span> <span class="s2">"rest.log.1"</span><span class="p">,</span> <span class="s2">"rest.log.2"</span><span class="p">]}</span>
</pre></div>
</div>
<div class="admonition warning">
<p class="admonition-title">Предупреждение</p>
<p>Лутника работает только с логами находящиеся в папке <code class="file docutils literal notranslate"><span class="pre">logs</span></code>.</p>
</div>
<p>Параметры:</p>
<table class="colwidths-given docutils align-default">
<colgroup>
<col style="width: 10%"/>
<col style="width: 10%"/>
<col style="width: 10%"/>
<col style="width: 70%"/>
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Параметр</p></th>
<th class="head"><p>Требует</p></th>
<th class="head"><p>Формат</p></th>
<th class="head"><p>Значение</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p>cmd</p></td>
<td></td>
<td><p>строка</p></td>
<td><dl class="simple">
<dt>принимает значения:</dt><dd><ul class="simple">
<li><p><strong>list</strong> - получить список файлов</p></li>
<li><p><strong>read</strong> - прочитать указанный файл</p></li>
<li><p><strong>get</strong> - скачать указанный файл</p></li>
</ul>
</dd>
</dl>
</td>
</tr>
<tr class="row-odd"><td><p>file</p></td>
<td><p>cmd=read cmd=get</p></td>
<td><p>строка</p></td>
<td><p>лог файл котрый нужно прочесть.</p></td>
</tr>
<tr class="row-even"><td><p>limit</p></td>
<td><p>cmd=read</p></td>
<td><p>число</p></td>
<td><p>лимит возращаемых строк. По умолчанию <code class="docutils literal notranslate"><span class="pre">10</span></code></p></td>
</tr>
<tr class="row-odd"><td><p>backward</p></td>
<td><p>cmd=read</p></td>
<td><p>булево</p></td>
<td><p>Чтение c конца файла. По умолчанию <code class="docutils literal notranslate"><span class="pre">True</span></code></p></td>
</tr>
<tr class="row-even"><td><p>offset</p></td>
<td><p>cmd=read</p></td>
<td><p>число</p></td>
<td><p>Положение курсора в файле.</p></td>
</tr>
</tbody>
</table>
<p>Вместе со строками, Лутника возвращает текущий <code class="xref std std-option docutils literal notranslate"><span class="pre">offset</span></code> который можно использовать для получения следующих
строк от последней прочитанной позиции, и <code class="xref std std-option docutils literal notranslate"><span class="pre">end</span></code> по которому можно отслеживать изменился ли файл.</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">a=</span><span class="n">log</span><span class="o">?</span><span class="ow">cmd=</span><span class="n">read</span><span class="o">&amp;</span><span class="ow">file=</span><span class="n">lootnika</span><span class="o">.</span><span class="n">log</span><span class="o">&amp;</span><span class="ow">limit=</span><span class="mi">3</span>
</pre></div>
</div>
<div class="highlight-json notranslate"><div class="highlight"><pre><span></span><span class="p">{</span>
<span class="nt">"offset"</span><span class="p">:</span> <span class="mi">54392</span><span class="p">,</span>
<span class="nt">"end"</span><span class="p">:</span> <span class="mi">54553</span><span class="p">,</span>
<span class="nt">"records"</span><span class="p">:</span> <span class="p">[</span>
    <span class="s2">"2021-29-04 19:58:00 Lootnika INFO: Welcome to http://localhost:8080/admin\r\n"</span><span class="p">,</span>
    <span class="s2">"2021-29-04 19:58:00 Lootnika INFO: Lootnika started - Source version: 1.2.0-beta.0_nt\r\n"</span><span class="p">,</span>

<span class="p">]}</span>
</pre></div>
</div>
<p>Указывая <code class="xref std std-option docutils literal notranslate"><span class="pre">offset</span></code> который возвращает Лутника вы будете читать файл последовательно пока не достигните его конца или начала.
Если указать конец файла, то список строк будет пустым. Однако, если указать начало файла, то вы получите первую строку:</p>
<div class="highlight-monte notranslate"><div class="highlight"><pre><span></span><span class="ow">a=</span><span class="n">log</span><span class="o">?</span><span class="ow">cmd=</span><span class="n">read</span><span class="o">&amp;</span><span class="ow">file=</span><span class="n">lootnika</span><span class="o">.</span><span class="n">log</span><span class="o">&amp;</span><span class="ow">limit=</span><span class="mi">3</span><span class="o">&amp;</span><span class="ow">offset=</span><span class="mi">0</span>
</pre></div>
</div>
<div class="highlight-json notranslate"><div class="highlight"><pre><span></span><span class="p">{</span>
<span class="nt">"offset"</span><span class="p">:</span> <span class="mi">-1</span><span class="p">,</span>
<span class="nt">"end"</span><span class="p">:</span> <span class="mi">54553</span><span class="p">,</span>
<span class="nt">"records"</span><span class="p">:</span> <span class="p">[</span>
    <span class="s2">"2021-26-04 21:34:10 Lootnika INFO: Starting...\r\n"</span>
<span class="p">]}</span>
</pre></div>
</div>
<p>Так получается потому что Лутника читает строку с той позиции, на которой стоит курсор и только потом переходит на следующую.</p>
</section>
</section>
    <div></div>
    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>