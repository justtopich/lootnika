<template>
  <div>
    
    <section id="lootnika-odbc">
<h1>lootnika ODBC<a class="headerlink" href="#lootnika-odbc" title="Ссылка на этот заголовок">¶</a></h1>
<p>Коннектор к БД с использованием протокола ODBC.</p>
<div class="admonition attention">
<p class="admonition-title">Внимание</p>
<p>Для работы коннектора необходимо предварительно установить ODBC драйвера</p>
</div>
<p>Доступны следующие параметры:</p>
<div class="contents local topic" id="id1">
<ul class="simple">
<li><p><a class="reference internal" href="#cnxstring">cnxString</a></p></li>
<li><p><a class="reference internal" href="#skipemptyrows">SkipEmptyRows</a></p></li>
<li><p><a class="reference internal" href="#docref">DocRef</a></p></li>
<li><p><a class="reference internal" href="#selectid">SelectID</a></p></li>
<li><p><a class="reference internal" href="#id2">SelectFields</a></p></li>
<li><p><a class="reference internal" href="#branchname">BranchName</a></p></li>
<li><p><a class="reference internal" href="#id5">SelectBranch</a></p></li>
</ul>
</div>
<section id="cnxstring">
<h2>cnxString<a class="headerlink" href="#cnxstring" title="Ссылка на этот заголовок">¶</a></h2>
<p>Параметры подключения. Для <span class="target" id="index-0"></span><code class="xref std std-envvar docutils literal notranslate"><span class="pre">DRIVER</span></code> укажите ODBC драйвер.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">cnxString</span> <span class="o">=</span> <span class="s">"</span>
        <span class="na">DRIVER</span><span class="o">=</span><span class="s">{PostgreSQL Unicode};</span>
        <span class="na">DATABASE</span><span class="o">=</span><span class="s">greenplum;</span>
        <span class="na">UID</span><span class="o">=</span><span class="s">medoed;</span>
        <span class="na">PWD</span><span class="o">=</span><span class="s">Ichi-Ni-San!;</span>
        <span class="na">SERVER</span><span class="o">=</span><span class="s">222.22.22.222; PORT=1234;"</span>
</pre></div>
</div>
</section>
<section id="skipemptyrows">
<h2>SkipEmptyRows<a class="headerlink" href="#skipemptyrows" title="Ссылка на этот заголовок">¶</a></h2>
<p>Булево значение отвечающее за пропуск пустых строк.</p>
<p>Испльзуйте этот параметр если не хотите чтобы пустые строки попадали в документ. При активации этого параметра, если запрос вернёт пустую строку, коннектор подставит для каждого поля значение <code class="docutils literal notranslate"><span class="pre">None</span></code></p>
<p>По умолчанию используется значение <code class="docutils literal notranslate"><span class="pre">True</span></code></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">SkipEmptyRows</span><span class="o">=</span><span class="s">True</span>
</pre></div>
</div>
</section>
<section id="docref">
<h2>DocRef<a class="headerlink" href="#docref" title="Ссылка на этот заголовок">¶</a></h2>
<p>Шаблон создания идентификаторов документов.</p>
<p>Reference должен быть уникальным для каждого документа. В нём можно использовать метаданные самого документа, например: его id, номер, название и т.д.</p>
<p>Используйте только те поля, которые всегда присутствуют документе. Если нужного поля не окажется в метаданных, то документ не будет создан, а значит не будет передан на экспорт. Если документ не имеет уникальных полей, используйте комбинацию различных полей и других указателей.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">DocRef</span><span class="o">=</span><span class="s">some_doc_@loot_id@</span>
<span class="na">DocRef</span><span class="o">=</span><span class="s">document_@number@</span>
<span class="na">DocRef</span><span class="o">=</span><span class="s">@id@-@name@-@data@</span>
</pre></div>
</div>
<p>Независимо от набора полей документа, вы всегда можете использовать его идентификатор в источнике <span class="target" id="index-1"></span><code class="xref std std-envvar docutils literal notranslate"><span class="pre">loot_id</span></code> (см. <a class="reference external" href="#SelectFields">SelectFields</a>).</p>
</section>
<section id="selectid">
<h2>SelectID<a class="headerlink" href="#selectid" title="Ссылка на этот заголовок">¶</a></h2>
<p>SQL запрос для получения идентификаторов документов в источнике.</p>
<p>Полученные ID используются в запросах на получение полей документа. Запрос обязательно должен возвращать только один столбец. Полученное значение доступно во всех SQL запросах как <span class="target" id="index-2"></span><code class="xref std std-envvar docutils literal notranslate"><span class="pre">loot_id</span></code></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">SelectID</span> <span class="o">=</span> <span class="s">SELECT id FROM topics WHERE status = "open"</span>
<span class="na">SelectID</span> <span class="o">=</span> <span class="s">SELECT login FROM users</span>
</pre></div>
</div>
</section>
<section id="id2">
<h2>SelectFields<a class="headerlink" href="#id2" title="Ссылка на этот заголовок">¶</a></h2>
<p>SQL запрос для получения полей документа.</p>
<p>Возвращаемые строки добавляются к метаданным документа в виде полей. Названия этих полей будут соответствовать названиям столбцов.</p>
<p>Для каждого документа можно выполнять любые SQL запросы подставляя в них его поля из предыдущих запросов. Для этого оберните их в <span class="guilabel">@</span>. Количество запросов не ограничено и начинаются с <code class="xref std std-option docutils literal notranslate"><span class="pre">SelectFields0</span></code>. В одном таком параметре может быть только один запрос.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">SelectFields0</span> <span class="o">=</span> <span class="s">SELECT id, title, author FROM topics WHERE topic = @loot_id@</span>
<span class="na">SelectFields1</span> <span class="o">=</span> <span class="s">SELECT nickname AS user_nickname FROM users WHERE id = @author@</span>
</pre></div>
</div>
<p>После вышеприведённого примера документ будет иметь следующую структуру:</p>
<div class="highlight-json notranslate"><div class="highlight"><pre><span></span><span class="p">{</span>
  <span class="nt">"id"</span> <span class="p">:</span> <span class="mi">535</span><span class="p">,</span>
  <span class="nt">"title"</span> <span class="p">:</span> <span class="s2">"Продам Peugeot"</span><span class="p">,</span>
  <span class="nt">"author"</span> <span class="p">:</span> <span class="mi">88</span><span class="p">,</span>
  <span class="nt">"user_nickname"</span> <span class="p">:</span> <span class="s2">"Daniel"</span>
<span class="p">}</span>
</pre></div>
</div>
<p>Все результаты из таких запросов будут добавлены в <strong>основные поля</strong> документа - это такие поля, которые доступны для подстановки в любые запросы (см. <a class="reference external" href="#SelectBranch">SelectBranch</a>).</p>
<div class="admonition warning">
<p class="admonition-title">Предупреждение</p>
<p>Такой запрос забирает только одну строку результатов. Если вам надо забрать несколько, то используйте <a class="reference external" href="#SelectBranch">SelectBranch</a>.</p>
</div>
</section>
<section id="branchname">
<h2>BranchName<a class="headerlink" href="#branchname" title="Ссылка на этот заголовок">¶</a></h2>
<p>Название ветви запросов.</p>
<p>Поле документа, в которое будут записаны результаты данной ветви запросов (см. <a class="reference external" href="#SelectBranch">SelectBranch</a>).
Количество ветвей не ограничено и начинаются с <code class="xref std std-option docutils literal notranslate"><span class="pre">BranchName0</span></code></p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">BranchName0</span> <span class="o">=</span> <span class="s">attachments</span>
</pre></div>
</div>
</section>
<section id="id5">
<h2>SelectBranch<a class="headerlink" href="#id5" title="Ссылка на этот заголовок">¶</a></h2>
<p>SQL запрос из вспомогательной ветви.</p>
<p>Позволяет собрать несколько значений одного поля или отдельные сущности со своим набором полей.</p>
<p>Для каждой ветви обязательно нужно указать её имя <a class="reference external" href="#BranchName">BranchName</a>.
Количество запросов внутри одной ветви не ограничено и начинаются с той же цифры что и её название</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">BranchName0</span> <span class="o">=</span> <span class="s">forum_posts</span>
<span class="na">SelectBranch0</span> <span class="o">=</span> <span class="s">SELECT * FROM posts</span>
<span class="na">BranchName1</span> <span class="o">=</span> <span class="s">forum_users</span>
<span class="na">SelectBranch1</span> <span class="o">=</span> <span class="s">SELECT * FROM users</span>
</pre></div>
</div>
<p>К примеру, можно получить посты из одной темы форума</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">SelectID</span> <span class="o">=</span> <span class="s">SELECT id FROM topics</span>
<span class="na">SelectFields0</span> <span class="o">=</span> <span class="s">SELECT id, title, author FROM topics WHERE topic = @loot_id@</span>

<span class="na">BranchName0</span> <span class="o">=</span> <span class="s">posts</span>
<span class="na">SelectBranch0</span> <span class="o">=</span> <span class="s">SELECT dtm, user, text FROM posts WHERE topic = @loot_id@</span>
</pre></div>
</div>
<p>Тогда каждый документ получится примерно таким</p>
<div class="highlight-json notranslate"><div class="highlight"><pre><span></span><span class="p">{</span>
  <span class="nt">"id"</span> <span class="p">:</span> <span class="mi">535</span><span class="p">,</span>
  <span class="nt">"title"</span> <span class="p">:</span> <span class="s2">"Продам Peugeot"</span><span class="p">,</span>
  <span class="nt">"author"</span> <span class="p">:</span> <span class="mi">88</span><span class="p">,</span>
  <span class="nt">"posts"</span> <span class="p">:</span> <span class="p">[{</span>
    <span class="nt">"dtm"</span><span class="p">:</span> <span class="s2">"15:25:40"</span><span class="p">,</span>
    <span class="nt">"user"</span><span class="p">:</span> <span class="mi">88</span><span class="p">,</span>
    <span class="nt">"text"</span><span class="p">:</span> <span class="s2">"Не бита, не крашена, пробег не смотан, как новая, сел и поехал!"</span>
    <span class="p">},{</span>
    <span class="nt">"dtm"</span><span class="p">:</span> <span class="s2">"22:08:04"</span><span class="p">,</span>
    <span class="nt">"user"</span><span class="p">:</span> <span class="mi">623</span><span class="p">,</span>
    <span class="nt">"text"</span><span class="p">:</span> <span class="s2">"пробег точно родной?"</span>
    <span class="p">}]</span>
<span class="p">}</span>
</pre></div>
</div>
<p>Внутри вспомогательной ветви можно так же выполнять несколько запросов и подставлять в них как основные, так поля из этой же ветви</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">SelectID</span> <span class="o">=</span> <span class="s">SELECT id FROM topics</span>
<span class="na">SelectFields0</span> <span class="o">=</span> <span class="s">SELECT id, title, author FROM topics WHERE topic = @loot_id@</span>

<span class="na">BranchName0</span> <span class="o">=</span> <span class="s">posts</span>
<span class="na">SelectBranch0</span> <span class="o">=</span> <span class="s">SELECT dtm, user, text FROM posts WHERE topic = @loot_id@</span>
<span class="na">SelectBranch0-0</span> <span class="o">=</span> <span class="s">SELECT nickname FROM users WHERE id = @user@</span>
<span class="na">SelectBranch0-1</span> <span class="o">=</span> <span class="s">SELECT karma FROM users WHERE id = @user@</span>
</pre></div>
</div>
<p>Тогда каждый документ уже будет таким</p>
<div class="highlight-json notranslate"><div class="highlight"><pre><span></span><span class="p">{</span>
  <span class="nt">"id"</span> <span class="p">:</span> <span class="mi">535</span><span class="p">,</span>
  <span class="nt">"title"</span> <span class="p">:</span> <span class="s2">"Продам Peugeot"</span><span class="p">,</span>
  <span class="nt">"author"</span> <span class="p">:</span> <span class="mi">88</span><span class="p">,</span>
  <span class="nt">"posts"</span> <span class="p">:</span> <span class="p">[{</span>
    <span class="nt">"dtm"</span><span class="p">:</span> <span class="s2">"15:25:40"</span><span class="p">,</span>
    <span class="nt">"user"</span><span class="p">:</span> <span class="mi">88</span><span class="p">,</span>
    <span class="nt">"text"</span><span class="p">:</span> <span class="s2">"Не бита, не крашена, пробег не смотан, как новая, сел и поехал!"</span><span class="p">,</span>
    <span class="nt">"nickname"</span><span class="p">:</span> <span class="s2">"Daniel"</span><span class="p">,</span>
    <span class="nt">"karma"</span><span class="p">:</span> <span class="mi">2</span>
    <span class="p">},{</span>
    <span class="nt">"dtm"</span><span class="p">:</span> <span class="s2">"22:08:04"</span><span class="p">,</span>
    <span class="nt">"user"</span><span class="p">:</span> <span class="mi">623</span><span class="p">,</span>
    <span class="nt">"text"</span><span class="p">:</span> <span class="s2">"пробег точно родной?"</span><span class="p">,</span>
    <span class="nt">"nickname"</span><span class="p">:</span> <span class="s2">"Еmilien"</span><span class="p">,</span>
    <span class="nt">"karma"</span><span class="p">:</span> <span class="mi">145</span>
    <span class="p">}]</span>
<span class="p">}</span>
</pre></div>
</div>
<p>У таких запросов есть ещё одно свойство - в отличии от <a class="reference external" href="#SelectFields">SelectFields</a> они могут записать несколько значений в одно поле.</p>
<div class="highlight-cfg notranslate"><div class="highlight"><pre><span></span><span class="na">SelectID</span> <span class="o">=</span> <span class="s">SELECT id FROM topics</span>
<span class="na">SelectFields0</span> <span class="o">=</span> <span class="s">SELECT id, title, author FROM topics WHERE topic = @loot_id@</span>

<span class="na">BranchName0</span> <span class="o">=</span> <span class="s">posts</span>
<span class="na">SelectBranch0</span> <span class="o">=</span> <span class="s">SELECT id, dtm, user, text FROM posts WHERE topic = @loot_id@</span>
<span class="na">SelectBranch0-0</span> <span class="o">=</span> <span class="s">SELECT nickname FROM users WHERE id = @user@</span>
<span class="na">SelectBranch0-1</span> <span class="o">=</span> <span class="s">SELECT id AS attach_id, name AS attach_name FROM files WHERE post_id = @id@</span>
</pre></div>
</div>
<p>В этом случае документ будет таким</p>
<div class="highlight-json notranslate"><div class="highlight"><pre><span></span><span class="p">{</span>
  <span class="nt">"id"</span> <span class="p">:</span> <span class="mi">535</span><span class="p">,</span>
  <span class="nt">"title"</span> <span class="p">:</span> <span class="s2">"Продам Peugeot"</span><span class="p">,</span>
  <span class="nt">"author"</span> <span class="p">:</span> <span class="mi">88</span><span class="p">,</span>
  <span class="nt">"posts"</span> <span class="p">:</span> <span class="p">[{</span>
    <span class="nt">"id"</span><span class="p">:</span> <span class="mi">27897</span><span class="p">,</span>
    <span class="nt">"dtm"</span><span class="p">:</span> <span class="s2">"15:25:40"</span><span class="p">,</span>
    <span class="nt">"user"</span><span class="p">:</span> <span class="mi">88</span><span class="p">,</span>
    <span class="nt">"text"</span><span class="p">:</span> <span class="s2">"Не бита, не крашена, пробег не смотан, как новая, сел и поехал!"</span><span class="p">,</span>
    <span class="nt">"nickname"</span><span class="p">:</span> <span class="s2">"Daniel"</span><span class="p">,</span>
    <span class="nt">"attach_id"</span><span class="p">:</span> <span class="p">[</span><span class="mi">440</span><span class="p">,</span> <span class="mi">441</span><span class="p">],</span>
    <span class="nt">"attach_name"</span><span class="p">:</span> <span class="p">[</span><span class="s2">"foto1.jpg"</span><span class="p">,</span> <span class="s2">"foto2.jpg"</span><span class="p">]</span>
    <span class="p">},{</span>
    <span class="nt">"id"</span><span class="p">:</span> <span class="mi">28002</span><span class="p">,</span>
    <span class="nt">"dtm"</span><span class="p">:</span> <span class="s2">"22:08:04"</span><span class="p">,</span>
    <span class="nt">"user"</span><span class="p">:</span> <span class="mi">623</span><span class="p">,</span>
    <span class="nt">"text"</span><span class="p">:</span> <span class="s2">"пробег точно родной?"</span><span class="p">,</span>
    <span class="nt">"nickname"</span><span class="p">:</span> <span class="s2">"Еmilien"</span>
    <span class="p">}]</span>
<span class="p">}</span>
</pre></div>
</div>
<div class="admonition attention">
<p class="admonition-title">Внимание</p>
<p>В запросе <code class="xref std std-option docutils literal notranslate"><span class="pre">SelectBranch0-1</span></code> используется поле <span class="target" id="index-3"></span><code class="xref std std-envvar docutils literal notranslate"><span class="pre">id</span></code>, которое есть и в основных и в вспомогательных полях. <strong>В приоритете подстановки поля из собственной ветви всегда выше основных.</strong></p>
</div>
<p>Таким образом можно сказать, что документ содержит тему с названием <em>Продам Peugeot</em> внутри которой есть два сообщения от <em>Daniel</em> и <em>Еmilien</em>, что в первом сообщении автор приложил два файла: <em>foto1.jpg</em> и <em>foto2.jpg</em>.</p>
<div class="admonition warning">
<p class="admonition-title">Предупреждение</p>
<dl class="simple">
<dt>Запросы из дополнительной ветви имеют свои ограничения:</dt><dd><ul class="simple">
<li><p>для них нельзя добавить ещё одну ветвь запросов типа <em>SelectBranch0-0-0</em></p></li>
<li><p>они могут использовать поля только из основной или своей ветви.</p></li>
<li><p>они могут переписать поля только внутри своей ветви.</p></li>
</ul>
</dd>
</dl>
</div>
</section>
</section>
    <div></div>
    <div id='vueBottomPage'></div>
    </div>
  </div>
</template>