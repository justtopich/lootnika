<template>
  <div>
    
    <section id="id1">
<h1>Команды<a class="headerlink" href="#id1" title="Ссылка на этот заголовок">¶</a></h1>
<p>Описание REST API.</p>
<p>Предоставляемое API позволяет управлять приложением и получать сведения о статусе его работы. Управление происходит через отправку http запросов на TCP порт Лутники. Такие запросы называются командами и делятся на 2 типа: <strong>общие</strong> и <strong>контрольные</strong>.</p>
<p>К общим относятся такие команды, как получение статуса работы. Обычно они доступны всем и потому позволяют выполнить только то, что может понадобиться лишь пользователю.
К контрольным относятся команды позволяющие получать все сведения о работе Лутники и контролировать её работу. Обычно они доступны только администраторам.</p>
<p>Параметры доступа к API задаются в секции <code class="xref std std-option docutils literal notranslate"><span class="pre">[Server]</span></code>. Команды имеют свой синтаксис.</p>
<p>Подразделы:</p>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><router-link class="reference internal" href="/index/api/api_syntax" to="/index/api/api_syntax">Синтаксис команд</router-link></li>
<li class="toctree-l1"><router-link class="reference internal" href="/index/api/api_common" to="/index/api/api_common">Общие команды</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/api/api_common" to="/index/api/api_common#getinfo" v-scroll-to="'/index/api/api_common#getinfo'">GetInfo</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/api/api_common" to="/index/api/api_common#getstatus" v-scroll-to="'/index/api/api_common#getstatus'">GetStatus</router-link></li>
</ul>
</li>
<li class="toctree-l1"><router-link class="reference internal" href="/index/api/api_control" to="/index/api/api_control">Контрольные команды</router-link><ul>
<li class="toctree-l2"><router-link class="reference internal" href="/index/api/api_control" to="/index/api/api_control#stop" v-scroll-to="'/index/api/api_control#stop'">Stop</router-link></li>
<li class="toctree-l2"><router-link class="reference internal" href="/index/api/api_control" to="/index/api/api_control#schedule" v-scroll-to="'/index/api/api_control#schedule'">Schedule</router-link><ul>
<li class="toctree-l3"><router-link class="reference internal" href="/index/api/api_control" to="/index/api/api_control#schedule-tasksinfo" v-scroll-to="'/index/api/api_control#schedule-tasksinfo'">Schedule: TasksInfo</router-link></li>
<li class="toctree-l3"><router-link class="reference internal" href="/index/api/api_control" to="/index/api/api_control#schedule-queueinfo" v-scroll-to="'/index/api/api_control#schedule-queueinfo'">Schedule: QueueInfo</router-link></li>
<li class="toctree-l3"><router-link class="reference internal" href="/index/api/api_control" to="/index/api/api_control#schedule-start" v-scroll-to="'/index/api/api_control#schedule-start'">Schedule: Start</router-link></li>
<li class="toctree-l3"><router-link class="reference internal" href="/index/api/api_control" to="/index/api/api_control#schedule-pause" v-scroll-to="'/index/api/api_control#schedule-pause'">Schedule: Pause</router-link></li>
<li class="toctree-l3"><router-link class="reference internal" href="/index/api/api_control" to="/index/api/api_control#schedule-cancel" v-scroll-to="'/index/api/api_control#schedule-cancel'">Schedule: Cancel</router-link></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
</section>
    <div></div>
    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>