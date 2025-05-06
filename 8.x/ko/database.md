# 데이터베이스: 시작하기

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기 및 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행하기](#running-queries)
    - [다중 데이터베이스 연결 사용](#using-multiple-database-connections)
    - [쿼리 이벤트 감지하기](#listening-for-query-events)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI에 연결하기](#connecting-to-the-database-cli)

<a name="introduction"></a>
## 소개

거의 모든 최신 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 다양한 데이터베이스를 지원하며, 원시 SQL, [플루언트 쿼리 빌더](/docs/{{version}}/queries), [Eloquent ORM](/docs/{{version}}/eloquent)을 사용하여 데이터베이스와 매우 쉽게 상호작용할 수 있도록 도와줍니다. 현재, Laravel은 다음 다섯 가지 데이터베이스에 대해 1차 지원을 제공합니다:

<div class="content-list" markdown="1">

- MariaDB 10.2+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 9.6+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.8.8+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

<a name="configuration"></a>
### 설정

Laravel의 데이터베이스 서비스 설정은 애플리케이션의 `config/database.php` 설정 파일에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의할 수 있으며, 기본으로 사용할 연결도 지정할 수 있습니다. 이 파일 내 대부분의 설정 옵션은 애플리케이션 환경 변수의 값을 기반으로 동작합니다. 대부분의 지원되는 데이터베이스 시스템에 대한 예시가 이 파일에 제공됩니다.

기본적으로 Laravel의 샘플 [환경설정](/docs/{{version}}/configuration#environment-configuration)은 [Laravel Sail](/docs/{{version}}/sail)과 바로 사용할 수 있도록 준비되어 있습니다. Laravel Sail은 로컬 환경에서 Laravel 애플리케이션을 개발하기 위한 Docker 환경입니다. 물론, 필요에 따라 로컬 데이터베이스에 맞게 데이터베이스 설정을 자유롭게 변경할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템 내 단일 파일에 저장됩니다. 터미널에서 `touch` 명령어를 사용하여 새 SQLite 데이터베이스를 생성할 수 있습니다: `touch database/database.sqlite`. 데이터베이스 생성 후, 환경 변수의 `DB_DATABASE`에 해당 데이터베이스의 절대 경로를 지정하면 쉽게 환경설정을 마칠 수 있습니다:

    DB_CONNECTION=sqlite
    DB_DATABASE=/absolute/path/to/database.sqlite

SQLite 연결에서 외래 키 제약조건을 활성화하려면, `DB_FOREIGN_KEYS` 환경변수를 `true`로 설정해야 합니다:

    DB_FOREIGN_KEYS=true

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면, `sqlsrv` 및 `pdo_sqlsrv` PHP 확장과 필요한 모든 의존성(예: Microsoft SQL ODBC 드라이버)이 설치되어 있어야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 이용한 설정

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 설정 값으로 구성합니다. 각각의 설정 값은 별도의 환경 변수에 해당합니다. 즉, 운영 서버에서 데이터베이스 연결 정보를 구성할 때 여러 환경 변수를 관리해야 합니다.

AWS, Heroku와 같은 일부 매니지드 데이터베이스 제공업체는 모든 연결 정보를 단일 문자열로 포함하는 데이터베이스 "URL"을 제공합니다. 예시 URL은 다음과 비슷합니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이러한 URL은 일반적으로 표준 스키마 규칙을 따릅니다:

```html
driver://username:password@host:port/database?options
```

편의상, Laravel은 다중 설정을 대신하여 이러한 URL을 지원합니다. 만약 `url`(혹은 해당하는 `DATABASE_URL` 환경 변수) 설정 옵션이 존재한다면, 이를 사용해 데이터베이스 연결 및 인증 정보를 추출합니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결

때로는 SELECT문에는 한 데이터베이스 연결을, INSERT, UPDATE, DELETE문에는 다른 연결을 사용하고 싶을 수 있습니다. Laravel에서는 이를 아주 쉽게 처리할 수 있으며, 원시 쿼리, 쿼리 빌더, Eloquent ORM을 사용할 때 항상 올바른 연결이 사용됩니다.

읽기/쓰기 연결을 어떻게 설정하는지 예시로 살펴보겠습니다:

    'mysql' => [
        'read' => [
            'host' => [
                '192.168.1.1',
                '196.168.1.2',
            ],
        ],
        'write' => [
            'host' => [
                '196.168.1.3',
            ],
        ],
        'sticky' => true,
        'driver' => 'mysql',
        'database' => 'database',
        'username' => 'root',
        'password' => '',
        'charset' => 'utf8mb4',
        'collation' => 'utf8mb4_unicode_ci',
        'prefix' => '',
    ],

위 설정 배열에는 `read`, `write`, `sticky` 세 가지 키가 추가되어 있습니다. `read`와 `write` 키에는 각각 `host`라는 단일 키를 가지는 배열 값을 할당합니다. 읽기/쓰기 연결의 나머지 옵션은 주 `mysql` 설정 배열에서 병합됩니다.

만약 `read`와 `write` 배열에 값을 넣었다면, 주 `mysql` 배열의 값을 재정의합니다. 위 예시의 경우, "읽기" 연결에는 `192.168.1.1`이, "쓰기" 연결에는 `192.168.1.3`이 사용됩니다. 데이터베이스 인증정보, prefix, 문자셋 등 나머지 옵션은 두 연결에 모두 공유됩니다. `host` 배열에 여러 값이 있다면, 각 요청마다 무작위로 하나의 데이터베이스 호스트를 선택합니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 *선택 사항*으로, 현재 요청 사이클에서 데이터베이스에 기록된 레코드를 즉시 읽을 수 있도록 허용합니다. `sticky` 옵션이 활성화되어 있고, 현재 요청 사이클에서 "쓰기" 작업이 발생했다면, 이후의 "읽기" 작업 역시 "쓰기" 연결을 사용합니다. 이렇게 하면 동일한 요청 내에서 쓰기 작업 후 즉시 데이터베이스에서 데이터를 읽어올 수 있습니다. 이 동작이 애플리케이션에 적합한지 여부는 직접 판단하셔야 합니다.

<a name="running-queries"></a>
## SQL 쿼리 실행하기

데이터베이스 연결을 설정한 후에는 `DB` 파사드를 사용하여 쿼리를 실행할 수 있습니다. `DB` 파사드에는 쿼리 종류별로 메서드가 제공됩니다: `select`, `update`, `insert`, `delete`, 그리고 `statement`.

<a name="running-a-select-query"></a>
#### SELECT 쿼리 실행하기

기본적인 SELECT 쿼리를 실행하려면, `DB` 파사드의 `select` 메서드를 사용하면 됩니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\DB;

    class UserController extends Controller
    {
        /**
         * 애플리케이션의 모든 사용자 목록을 보여줍니다.
         *
         * @return \Illuminate\Http\Response
         */
        public function index()
        {
            $users = DB::select('select * from users where active = ?', [1]);

            return view('user.index', ['users' => $users]);
        }
    }

`select` 메서드의 첫 번째 인자는 SQL 쿼리, 두 번째 인자는 쿼리에 바인딩할 파라미터 배열입니다. 일반적으로 이는 `where` 절의 값들입니다. 파라미터 바인딩을 통해 SQL 인젝션 공격을 예방할 수 있습니다.

`select` 메서드는 항상 결과의 `array`를 반환합니다. 이 배열의 각 항목은 해당 레코드를 나타내는 PHP `stdClass` 객체입니다:

    use Illuminate\Support\Facades\DB;

    $users = DB::select('select * from users');

    foreach ($users as $user) {
        echo $user->name;
    }

<a name="using-named-bindings"></a>
#### 이름 있는 바인딩 사용하기

파라미터 바인딩에 `?` 대신 이름 있는 바인딩을 사용할 수 있습니다:

    $results = DB::select('select * from users where id = :id', ['id' => 1]);

<a name="running-an-insert-statement"></a>
#### INSERT문 실행하기

`insert`문을 실행하려면, `DB` 파사드의 `insert` 메서드를 사용하세요. `select`와 마찬가지로 첫 번째 인자는 SQL 쿼리, 두 번째 인자는 바인딩 배열입니다:

    use Illuminate\Support\Facades\DB;

    DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);

<a name="running-an-update-statement"></a>
#### UPDATE문 실행하기

기존 레코드를 갱신하려면 `update` 메서드를 사용하세요. 이 메서드는 영향을 받은 행의 수를 반환합니다:

    use Illuminate\Support\Facades\DB;

    $affected = DB::update(
        'update users set votes = 100 where name = ?',
        ['Anita']
    );

<a name="running-a-delete-statement"></a>
#### DELETE문 실행하기

레코드를 삭제하려면 `delete` 메서드를 사용하세요. `update`와 마찬가지로, 영향을 받은 행의 수를 반환합니다:

    use Illuminate\Support\Facades\DB;

    $deleted = DB::delete('delete from users');

<a name="running-a-general-statement"></a>
#### 일반적인 SQL문 실행하기

일부 데이터베이스 명령문은 반환값이 없습니다. 이런 경우에는 `DB` 파사드의 `statement` 메서드를 사용할 수 있습니다:

    DB::statement('drop table users');

<a name="running-an-unprepared-statement"></a>
#### 미준비 Statement 실행하기

때로는 값 바인딩 없이 SQL문을 실행해야 할 수도 있습니다. 이럴 때는 `DB` 파사드의 `unprepared` 메서드를 사용하세요:

    DB::unprepared('update users set votes = 100 where name = "Dries"');

> {note} 미준비 statement는 파라미터를 바인딩하지 않기 때문에 SQL 인젝션에 취약할 수 있습니다. 사용자 입력값이 미준비 statement에 포함되지 않도록 해야 합니다.

<a name="implicit-commits-in-transactions"></a>
#### 암시적 커밋

트랜잭션 내에서 `DB` 파사드의 `statement`와 `unprepared` 메서드를 사용할 때는 [암시적 커밋](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 발생시키는 statement를 주의해야 합니다. 이런 statement는 데이터베이스 엔진이 트랜잭션 전체를 간접적으로 커밋하게 하여, Laravel이 트랜잭션 레벨을 파악할 수 없게 만듭니다. 예를 들어, 데이터베이스 테이블을 생성하는 statement가 있습니다:

    DB::unprepared('create table a (col varchar(1) null)');

암시적 커밋을 유발하는 모든 statement 목록은 MySQL 매뉴얼의 [해당 문서](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)를 참고하세요.

<a name="using-multiple-database-connections"></a>
### 다중 데이터베이스 연결 사용

애플리케이션이 `config/database.php` 설정 파일에 여러 연결을 정의한다면, `DB` 파사드의 `connection` 메서드를 통해 각각의 연결에 접근할 수 있습니다. `connection` 메서드에 전달하는 연결 이름은 설정 파일 또는 `config` 헬퍼를 통해 런타임에 구성된 연결 이름과 일치해야 합니다:

    use Illuminate\Support\Facades\DB;

    $users = DB::connection('sqlite')->select(...);

또한, 연결 인스턴스의 `getPdo` 메서드로 원시 PDO 인스턴스에 접근할 수 있습니다:

    $pdo = DB::connection()->getPdo();

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 감지하기

애플리케이션에서 실행되는 모든 SQL 쿼리에 대해 클로저를 지정하고 싶다면, `DB` 파사드의 `listen` 메서드를 사용할 수 있습니다. 이 메서드는 쿼리 로깅이나 디버깅에 유용합니다. [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에 쿼리 리스너 클로저를 등록할 수 있습니다:

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스 등록
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * 애플리케이션 서비스 부트스트랩
         *
         * @return void
         */
        public function boot()
        {
            DB::listen(function ($query) {
                // $query->sql;
                // $query->bindings;
                // $query->time;
            });
        }
    }

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션

`DB` 파사드의 `transaction` 메서드를 이용하면 데이터베이스 트랜잭션 내에서 일련의 작업을 실행할 수 있습니다. 트랜잭션 클로저 내에서 예외가 발생하면 트랜잭션은 자동으로 롤백되고 예외가 다시 던져집니다. 클로저가 정상적으로 실행되면 트랜잭션은 자동으로 커밋됩니다. 이 메서드를 사용하는 동안에는 트랜잭션 롤백/커밋을 직접 관리할 필요가 없습니다:

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    });

<a name="handling-deadlocks"></a>
#### 교착상태(Deadlock) 처리

`transaction` 메서드는 선택적으로 두 번째 인자를 받을 수 있습니다. 이는 교착상태 발생 시 트랜잭션을 재시도할 횟수를 지정합니다. 모든 시도가 실패하면 예외가 발생합니다:

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    }, 5);

<a name="manually-using-transactions"></a>
#### 트랜잭션을 수동으로 사용하기

트랜잭션을 수동으로 시작하여 롤백과 커밋을 직접 제어하고 싶다면, `DB` 파사드의 `beginTransaction` 메서드를 사용하면 됩니다:

    use Illuminate\Support\Facades\DB;

    DB::beginTransaction();

트랜잭션을 롤백하려면 `rollBack` 메서드를 호출하세요:

    DB::rollBack();

마지막으로, 트랜잭션을 커밋하려면 `commit` 메서드를 호출하세요:

    DB::commit();

> {tip} `DB` 파사드의 트랜잭션 메서드는 [쿼리 빌더](/docs/{{version}}/queries)와 [Eloquent ORM](/docs/{{version}}/eloquent) 모두의 트랜잭션을 제어합니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI에 연결하기

데이터베이스의 CLI에 연결하고 싶다면 `db` Artisan 명령어를 사용할 수 있습니다:

    php artisan db

필요하다면, 기본 연결이 아닌 데이터베이스 연결 이름을 지정해 특정 데이터베이스에 연결할 수 있습니다:

    php artisan db mysql
