<h1>Модуль 1. Разработка базы данных</h1>

<h2>Что такое 3НФ</h2>

<p>
3НФ — это третья нормальная форма базы данных. Она нужна для того, чтобы не хранить
одни и те же данные много раз в одной таблице.
</p>

<p>
Если какое-то значение часто повторяется, его лучше вынести в отдельную таблицу.
А в основной таблице хранить только ссылку на него через <code>id</code>.
</p>

<hr>

<h2>Пример по моему заданию</h2>

<p>
В задании основная сущность — вакансия. У вакансии есть компания, регион и специализация.
Эти данные могут повторяться в разных вакансиях, поэтому их нужно вынести в отдельные таблицы.
</p>

<p>Например, неправильно хранить так:</p>

<pre><code>vacancy
- id
- name
- region
- company
- specialization
- salary_from
- salary_to</code></pre>

<p>Правильнее хранить так:</p>

<pre><code>vacancy
- id
- name
- region_id
- company_id
- specialization_id
- salary_from
- salary_to</code></pre>

<p>
А сами регионы, компании и специализации находятся в отдельных таблицах.
</p>

<hr>

<h2>Какие таблицы нужны</h2>

<pre><code>region
- id
- region
- code

company
- company_id
- company_name
- email
- INN
- KPP
- OGRN

specialization
- id
- specialization

users
- id
- role
- full_name
- login
- password

vacancy
- id
- name
- data_create
- region_id
- company_id
- specialization_id
- salary_from
- salary_to</code></pre>

<hr>

<h2>Как работают связи</h2>

<p>
Таблица <code>vacancy</code> является основной. Именно она ссылается на справочники:
</p>

<pre><code>vacancy.region_id → region.id
vacancy.company_id → company.company_id
vacancy.specialization_id → specialization.id</code></pre>

<p>
То есть вакансия не хранит текстом название региона, компании и специализации.
Она хранит только их идентификаторы.
</p>

<hr>

<h2>Почему это 3НФ</h2>

<ul>
  <li>Данные не дублируются лишний раз.</li>
  <li>Компании вынесены в отдельную таблицу.</li>
  <li>Регионы вынесены в отдельную таблицу.</li>
  <li>Специализации вынесены в отдельную таблицу.</li>
  <li>Вакансия хранит только ссылки на эти таблицы.</li>
  <li>Связи между таблицами сделаны через внешние ключи.</li>
</ul>

<hr>

<h2>SQL-код создания базы данных</h2>

<pre><code class="language-sql">CREATE TABLE region (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT NOT NULL UNIQUE,
    code TEXT NOT NULL UNIQUE
);

CREATE TABLE specialization (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    specialization TEXT NOT NULL UNIQUE
);

CREATE TABLE company (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    company_name TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,   
    INN TEXT NOT NULL,                               
    KPP TEXT NOT NULL,
    OGRN TEXT NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,                        
    full_name TEXT NOT NULL,                   
    login TEXT NOT NULL UNIQUE,              
    password TEXT NOT NULL              
);

CREATE TABLE vacancy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,               
    name TEXT NOT NULL,                        
    data_create DATE NOT NULL,

    region_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,                     
    specialization_id INTEGER NOT NULL,

    salary_from REAL NOT NULL,
    salary_to REAL NOT NULL,

    FOREIGN KEY (region_id) REFERENCES region(id),
    FOREIGN KEY (company_id) REFERENCES company(company_id),
    FOREIGN KEY (specialization_id) REFERENCES specialization(id)
);</code></pre>

<hr>

<h2>Краткий итог</h2>

<p>
База данных была разделена на несколько таблиц, чтобы убрать повторяющиеся данные.
Основная таблица — <code>vacancy</code>. В ней хранятся данные вакансии и внешние ключи
на регион, компанию и специализацию. Такая структура соответствует третьей нормальной форме.
</p>
