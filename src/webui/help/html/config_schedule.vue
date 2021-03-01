<template>
  <div>
    <div class="section" id="schedule">
<h1>Секция Schedule<a class="headerlink" href="#schedule" title="Ссылка на этот заголовок">¶</a></h1>
<p>Управление расписанием выполнения заданий.</p>
<p>Лутника имеет встроенную функцию планировщика заданий для их периодического выполнения. Каждое такое выполнение называется циклом. Цикл может состоять от одного до нескольких заданий. Если задание не может быть выполнено, планировщик приступит к следующему. Цикл будет завершён как только все задания будут закончены. После каждого цикла планировщик либо завершает выполнение расписания, либо ждёт заданное время до старта следующего цикла.</p>
<p>Список доступных параметров:</p>
<div class="contents local topic" id="id1">
<ul class="simple">
<li><p><a class="reference internal" href="#enable">Enable</a></p></li>
<li><p><a class="reference internal" href="#taskstarttime">TaskStartTime</a></p></li>
<li><p><a class="reference internal" href="#taskcycles">TaskCycles</a></p></li>
<li><p><a class="reference internal" href="#repeatmin">RepeatMin</a></p></li>
<li><p><a class="reference internal" href="#taskcount">TaskCount</a></p></li>
</ul>
</div>
<div class="section" id="enable">
<h2>Enable<a class="headerlink" href="#enable" title="Ссылка на этот заголовок">¶</a></h2>
<p>Булево значение отвечающее за активацию расписания.</p>
<p>При использовании <code class="docutils literal notranslate"><span class="pre">False</span></code> нижеописанные параметры будут не активны, а начать выполнение заданий можно только с помощью команды <router-link class="reference internal" href="/api/api_control" to="/api/api_control"><span class="doc">Schedule</span></router-link>.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">Enable</span> <span class="o">=</span> <span class="s">True</span>
</pre></div>
</div>
</div>
<div class="section" id="taskstarttime">
<h2>TaskStartTime<a class="headerlink" href="#taskstarttime" title="Ссылка на этот заголовок">¶</a></h2>
<p>Указывает время старта циклов заданий.</p>
<p>Можно старт при запуске коннектора или указать конкретное время. Время указывается в 24-часовом формате <em>HH:MM:SS</em></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">TaskStartTime</span> <span class="o">=</span> <span class="s">now</span>
<span class="na">TaskStartTime</span> <span class="o">=</span> <span class="s">15:50:30</span>
</pre></div>
</div>
</div>
<div class="section" id="taskcycles">
<h2>TaskCycles<a class="headerlink" href="#taskcycles" title="Ссылка на этот заголовок">¶</a></h2>
<p>Количество выполнений расписания.</p>
<p>Если укажите <code class="docutils literal notranslate"><span class="pre">0</span></code>, то расписание выполняться не будет, а если <code class="docutils literal notranslate"><span class="pre">-1</span></code> - будет повторятся бесконечно.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">TaskCycles</span> <span class="o">=</span> <span class="s">-1</span>
</pre></div>
</div>
</div>
<div class="section" id="repeatmin">
<h2>RepeatMin<a class="headerlink" href="#repeatmin" title="Ссылка на этот заголовок">¶</a></h2>
<p>Временной интервал между циклами заданий.</p>
<p>Этот интервал отсчитывается от старта каждого цикла. Если на момент старта очередного цикла предыдущий ещё будет выполняться, то Лутника пропустит его и начнёт новый отсчёт до следующего цикла. <strong>При этом счётчик TaskCycles всё равно засчитает его.</strong></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">RepeatMin</span> <span class="o">=</span> <span class="s">4320</span>
<span class="c1">; повтор каждые три дня</span>
</pre></div>
</div>
</div>
<div class="section" id="taskcount">
<h2>TaskCount<a class="headerlink" href="#taskcount" title="Ссылка на этот заголовок">¶</a></h2>
<p>Количество и порядок выполнения заданий.</p>
<p>Вы можете задать в расписании минимум одно задание. Значение этого параметра не должно превышать количество заданий, но может быть меньше.
Отсчёт заданий начинает от <code class="docutils literal notranslate"><span class="pre">0</span></code> и выполняются в порядке возрастания.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">TaskCount</span><span class="o">=</span><span class="s">2</span>
<span class="na">0</span><span class="o">=</span><span class="s">Forum_topics</span>
<span class="na">1</span><span class="o">=</span><span class="s">users</span>
<span class="na">2</span><span class="o">=</span><span class="s">not_used</span>
</pre></div>
</div>
<div class="admonition attention">
<p class="admonition-title">Внимание</p>
<p>Задания можно выполнить с помощью команд только если они будут здесь объявлены. Для того, чтобы узнать какие задания доступны для выполнения, отправьте команду <router-link class="reference internal" href="/api/api_control" to="/api/api_control"><span class="doc">Schedule: TasksInfo</span></router-link>.</p>
</div>
</div>

    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>