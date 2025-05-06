# 데이터베이스: 시작하기

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기 및 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행하기](#running-queries)
    - [여러 데이터베이스 연결 사용하기](#using-multiple-database-connections)
    - [쿼리 이벤트 리스닝](#listening-for-query-events)
    - [누적 쿼리 시간 모니터링](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI에 연결하기](#connecting-to-the-database-cli)
- [데이터베이스 점검하기](#inspecting-your-databases)
- [데이터베이스 모니터링하기](#monitoring-your-databases)

<a name="introduction"></a>
## 소개

대부분의 현대적인 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 다양한 지원 데이터베이스를 대상으로, 원시 SQL, [플루언트 쿼리 빌더](/docs/{{version}}/queries), 그리고 [Eloquent ORM](/docs/{{version}}/eloquent)를 통해 매우 간편하게 데이터베이스와 연동할 수 있도록 해줍니다. 현재 Laravel은 다섯 가지 데이터베이스에 대해 공식 지원을 제공합니다:

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.8.8+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

<a name="configuration"></a>
### 설정

Laravel의 데이터베이스 서비스 설정은 애플리케이션의 `config/database.php` 설정 파일에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의하고, 기본으로 사용할 연결도 지정할 수 있습니다. 이 파일의 대부분의 설정 옵션은 애플리케이션 환경 변수의 값에 따라 결정됩니다. Laravel에서 지원하는 대부분의 데이터베이스 시스템에 대한 예제 설정이 이 파일 내에 제공되어 있습니다.

기본적으로 Laravel의 샘플 [환경설정](/docs/{{version}}/configuration#environment-configuration)은 [Laravel Sail](/docs/{{version}}/sail)과 함께 바로 사용할 수 있도록 준비되어 있습니다. Sail은 로컬에서 Laravel 애플리케이션을 개발하기 위한 Docker 구성입니다. 하지만, 필요에 따라 로컬 데이터베이스에 알맞게 데이터베이스 설정을 자유롭게 변경할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템의 단일 파일 안에 저장됩니다. 터미널에서 `touch` 명령어를 사용해 새 SQLite 데이터베이스를 생성할 수 있습니다: `touch database/database.sqlite`. 데이터베이스가 생성된 후, 환경 변수에서 데이터베이스의 절대 경로를 `DB_DATABASE`에 지정해주면 됩니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

SQLite 연결에서 외래 키 제약 조건을 활성화하려면 `DB_FOREIGN_KEYS` 환경 변수 값을 `true`로 설정해야 합니다:

```ini
DB_FOREIGN_KEYS=true
```

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면, PHP의 `sqlsrv` 및 `pdo_sqlsrv` 확장과 이 확장에 필요한 Microsoft SQL ODBC 드라이버 등 종속성을 설치해야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 통한 설정

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 설정값을 통해 구성합니다. 이 모든 설정 항목은 각각 별도의 환경 변수로 분리됩니다. 즉, 프로덕션 서버에서 데이터베이스 연결 정보를 구성할 때 여러 환경 변수 항목을 관리해야 합니다.

AWS나 Heroku와 같은 일부 관리형 데이터베이스 서비스에서는 모든 연결 정보를 한 번에 담고 있는 단일 데이터베이스 "URL"을 제공합니다. 예시 URL은 다음과 같습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이들 URL은 일반적으로 표준 스키마 규약을 따릅니다:

```html
driver://username:password@host:port/database?options
```

Laravel에서는 편의를 위해 여러 설정 옵션 대신 이러한 데이터베이스 URL을 사용할 수 있습니다. `url`(또는 대응되는 `DATABASE_URL` 환경 변수) 설정 항목이 있으면, 이를 통해 데이터베이스 연결 및 자격 증명 정보를 추출합니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결

때로는 SELECT 문에는 하나의 데이터베이스 연결을, INSERT, UPDATE, DELETE 문에는 다른 연결을 사용하고 싶을 수 있습니다. Laravel에서는 이를 매우 쉽게 구현할 수 있으며, 원시 쿼리, 쿼리 빌더, Eloquent ORM을 사용할 때 상황에 맞는 연결을 자동으로 사용합니다.

읽기/쓰기 연결을 어떻게 설정하는지 예시를 통해 살펴봅시다:

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

설정 배열에는 `read`, `write`, `sticky`라는 세 가지 키가 추가되었습니다. `read`와 `write` 키는 각각 `host` 하나만을 가진 배열 형태입니다. `read`와 `write` 연결의 나머지 데이터베이스 옵션은 메인 `mysql` 설정 배열과 병합됩니다.

`read`/`write` 배열에는 메인 `mysql` 배열의 값을 오버라이드하려는 항목만 넣으면 됩니다. 따라서 이 예제에서는 "read" 연결에는 `192.168.1.1`, "write" 연결에는 `192.168.1.3`이 각각 사용됩니다. 나머지 자격증명, 접두사, 문자셋과 기타 옵션들은 두 연결에서 공유됩니다. `host` 배열에 값이 여러 개 있을 경우, 각 요청마다 무작위로 데이터베이스 호스트가 선택됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 *선택 사항*이며, 현재 요청 사이클 내에서 데이터베이스에 쓰기가 이루어진 경우 바로 읽기 연산에서 "write" 연결을 사용하도록 해줍니다. 만약 `sticky`가 활성화되어 있고, 현재 요청 사이클에서 "write" 작업이 발생했다면, 이어지는 모든 "read" 작업은 "write" 연결을 사용합니다. 이로 인해 같은 요청에서 갓 저장된 데이터를 즉시 읽을 수 있습니다. 이 동작 방식이 필요한지 여부는 애플리케이션의 요구에 따라 결정할 수 있습니다.

<a name="running-queries"></a>
## SQL 쿼리 실행하기

데이터베이스 연결을 설정한 후에는 `DB` 파사드를 사용해 쿼리를 실행할 수 있습니다. `DB` 파사드는 `select`, `update`, `insert`, `delete`, `statement` 등 각 쿼리 유형별 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### SELECT 쿼리 실행

기본 SELECT 쿼리를 실행하려면 `DB` 파사드의 `select` 메서드를 사용할 수 있습니다:

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

`select` 메서드의 첫 번째 인자는 SQL 쿼리이며, 두 번째 인자는 쿼리에 바인딩되어야 할 파라미터 바인딩 배열입니다. 일반적으로 이는 WHERE 절의 값들입니다. 파라미터 바인딩은 SQL 인젝션을 방지해줍니다.

`select` 메서드는 항상 결과의 `array`를 반환합니다. 배열 내 각각의 결과는 데이터베이스 레코드를 나타내는 PHP `stdClass` 객체입니다:

    use Illuminate\Support\Facades\DB;

    $users = DB::select('select * from users');

    foreach ($users as $user) {
        echo $user->name;
    }

<a name="selecting-scalar-values"></a>
#### 스칼라 값 선택

가끔 쿼리 결과가 하나의 스칼라 값일 때가 있습니다. 이럴 때는 레코드 객체를 통해 값을 꺼내오지 않고, `scalar` 메서드로 바로 값을 가져올 수 있습니다:

    $burgers = DB::scalar(
        "select count(case when food = 'burger' then 1 end) as burgers from menu"
    );

<a name="using-named-bindings"></a>
#### 이름 있는 바인딩 사용

파라미터 바인딩에 `?` 대신 이름 있는 바인딩을 사용할 수도 있습니다:

    $results = DB::select('select * from users where id = :id', ['id' => 1]);

<a name="running-an-insert-statement"></a>
#### INSERT 쿼리 실행

`insert` 구문을 실행하려면 `DB` 파사드의 `insert` 메서드를 사용합니다. `select`와 마찬가지로 첫 번째 인자는 SQL 쿼리, 두 번째는 바인딩 배열입니다:

    use Illuminate\Support\Facades\DB;

    DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);

<a name="running-an-update-statement"></a>
#### UPDATE 쿼리 실행

`update` 메서드는 데이터베이스의 기존 레코드를 갱신할 때 사용합니다. 해당 구문에 의해 영향을 받은 행(row)의 수를 반환합니다:

    use Illuminate\Support\Facades\DB;

    $affected = DB::update(
        'update users set votes = 100 where name = ?',
        ['Anita']
    );

<a name="running-a-delete-statement"></a>
#### DELETE 쿼리 실행

`delete` 메서드는 데이터베이스에서 레코드를 삭제할 때 사용합니다. `update`와 마찬가지로 영향을 받은 행(row)의 수를 반환합니다:

    use Illuminate\Support\Facades\DB;

    $deleted = DB::delete('delete from users');

<a name="running-a-general-statement"></a>
#### 일반 구문 실행

일부 데이터베이스 구문은 값을 반환하지 않습니다. 이러한 작업에는 `DB` 파사드의 `statement` 메서드를 사용할 수 있습니다:

    DB::statement('drop table users');

<a name="running-an-unprepared-statement"></a>
#### 언프리페어드(unprepared) 구문 실행

바인딩 값 없이 SQL 문을 실행해야 할 때가 있습니다. 이럴 때는 `DB` 파사드의 `unprepared` 메서드를 사용할 수 있습니다:

    DB::unprepared('update users set votes = 100 where name = "Dries"');

> **경고**  
> 언프리페어드 구문은 파라미터 바인딩을 지원하지 않기 때문에 SQL 인젝션에 취약할 수 있습니다. 사용자 값을 직접 넣는 구문에는 절대 사용하지 마세요.

<a name="implicit-commits-in-transactions"></a>
#### 암시적 커밋

트랜잭션 내에서 `DB` 파사드의 `statement` 및 `unprepared` 메서드를 사용할 때는 [암시적 커밋](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 유발하는 구문을 주의해야 합니다. 이런 구문은 데이터베이스 엔진이 트랜잭션 전체를 간접적으로 커밋하게 하여, Laravel이 트랜잭션 상태를 인지하지 못하는 상황을 만들 수 있습니다. 예를 들면 테이블 생성 명령이 있습니다:

    DB::unprepared('create table a (col varchar(1) null)');

[암시적 커밋을 유발하는 모든 명령 목록](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)은 MySQL 매뉴얼을 참조하세요.

<a name="using-multiple-database-connections"></a>
### 여러 데이터베이스 연결 사용하기

애플리케이션의 `config/database.php` 설정 파일에 여러 연결을 정의한 경우, `DB` 파사드의 `connection` 메서드를 통해 각 연결에 접근할 수 있습니다. `connection` 메서드에 전달하는 이름은 설정 파일에 정의된 연결 이름 또는 런타임에 `config` 헬퍼로 설정된 이름이어야 합니다.

    use Illuminate\Support\Facades\DB;

    $users = DB::connection('sqlite')->select(/* ... */);

연결 인스턴스에서 `getPdo` 메서드를 사용해 원시 PDO 인스턴스에 접근할 수 있습니다:

    $pdo = DB::connection()->getPdo();

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 리스닝

애플리케이션에서 실행되는 모든 SQL 쿼리에 대해 클로저를 지정하고 싶다면, `DB` 파사드의 `listen` 메서드를 사용할 수 있습니다. 이 방법은 쿼리 로깅이나 디버깅에 유용합니다. 쿼리 리스너 클로저는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에 등록할 수 있습니다:

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스를 등록합니다.
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * 애플리케이션 서비스를 부트스트랩합니다.
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

<a name="monitoring-cumulative-query-time"></a>
### 누적 쿼리 시간 모니터링

현대 웹 애플리케이션의 성능 병목 지점 중 하나는 데이터베이스 쿼리에 소비되는 시간입니다. Laravel에서는 한 요청 내에서 데이터베이스 쿼리에 너무 많은 시간이 소요될 경우, 원하는 클로저나 콜백을 실행할 수 있습니다. 시작하려면, `whenQueryingForLongerThan` 메서드에 쿼리 시간 임계값(밀리초)과 클로저를 전달하면 됩니다. 이 메서드는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드 내에서 호출하면 됩니다:

    <?php

    namespace App\Providers;

    use Illuminate\Database\Connection;
    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\ServiceProvider;
    use Illuminate\Database\Events\QueryExecuted;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스를 등록합니다.
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * 애플리케이션 서비스를 부트스트랩합니다.
         *
         * @return void
         */
        public function boot()
        {
            DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {
                // 개발팀에 알림 발송 등...
            });
        }
    }

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션

트랜잭션 내에서 일련의 작업을 실행하려면, `DB` 파사드가 제공하는 `transaction` 메서드를 사용할 수 있습니다. 트랜잭션 클로저 내에서 예외가 발생하면 자동으로 롤백되고 예외가 재발생합니다. 클로저가 정상적으로 실행되면 트랜잭션이 자동으로 커밋됩니다. 직접 롤백이나 커밋을 신경 쓸 필요가 없습니다.

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    });

<a name="handling-deadlocks"></a>
#### 데드락 처리

`transaction` 메서드는 옵션으로 두 번째 인자를 받을 수 있으며, 데드락 발생 시 트랜잭션을 재시도할 횟수를 정의합니다. 지정된 횟수만큼 시도 후에도 데드락이면 예외가 발생합니다.

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    }, 5);

<a name="manually-using-transactions"></a>
#### 트랜잭션 수동 제어

트랜잭션을 직접 관리(시작/커밋/롤백)하고 싶다면, `DB` 파사드의 `beginTransaction` 메서드를 사용할 수 있습니다:

    use Illuminate\Support\Facades\DB;

    DB::beginTransaction();

트랜잭션은 `rollBack` 메서드로 롤백할 수 있습니다:

    DB::rollBack();

마지막으로, `commit` 메서드로 트랜잭션을 커밋할 수 있습니다:

    DB::commit();

> **참고**  
> `DB` 파사드의 트랜잭션 메서드는 [쿼리 빌더](/docs/{{version}}/queries)와 [Eloquent ORM](/docs/{{version}}/eloquent) 모두의 트랜잭션을 제어합니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI에 연결하기

데이터베이스의 CLI에 연결하고 싶다면 `db` 아티즌(Artisan) 명령어를 사용할 수 있습니다:

```shell
php artisan db
```

필요하다면, 기본 연결이 아닌 다른 데이터베이스 연결 이름을 지정할 수 있습니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 점검하기

`db:show` 및 `db:table` 아티즌 명령을 사용해 데이터베이스 및 테이블 현황을 확인할 수 있습니다. 데이터베이스의 개요(용량, 유형, 열린 연결 수, 테이블 요약)를 보려면 `db:show` 명령을 사용하세요:

```shell
php artisan db:show
```

어떤 데이터베이스 연결을 점검할지 결정하려면 `--database` 옵션에 연결 이름을 지정할 수 있습니다:

```shell
php artisan db:show --database=pgsql
```

명령 결과에 테이블 행(row) 수와 데이터베이스 뷰 정보를 포함하려면 각각 `--counts`, `--views` 옵션을 줄 수 있습니다. 대규모 데이터베이스에서는 행 개수 및 뷰 정보를 가져오는 데 느릴 수 있습니다:

```shell
php artisan db:show --counts --views
```

<a name="table-overview"></a>
#### 테이블 개요

개별 테이블 정보를 확인하려면 `db:table` 아티즌 명령어를 실행할 수 있습니다. 이 명령어는 테이블의 컬럼, 타입, 속성, 키, 인덱스 등 전반적인 정보를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링하기

`db:monitor` 아티즌 명령어를 사용하면, 데이터베이스의 열린 연결 수가 지정한 기준을 초과할 경우 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 Laravel에서 발생시킬 수 있습니다.

먼저, `db:monitor` 명령어를 [매분 실행하도록 스케줄](docs/{{version}}/scheduling)해야 합니다. 이 명령은 모니터링할 데이터베이스 연결 이름들과, 이벤트 디스패치 전 허용 가능한 최대 열린 연결 수를 지정할 수 있습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

이 명령을 스케줄링한다고 해서 자동으로 알림이 전송되는 것은 아닙니다. 임계값을 초과한 데이터베이스 연결이 감지되면 `DatabaseBusy` 이벤트가 발생합니다. 애플리케이션의 `EventServiceProvider`에서 이 이벤트를 감지하도록 해야 이메일 알림 등을 보낼 수 있습니다:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 애플리케이션의 추가 이벤트를 등록합니다.
 *
 * @return void
 */
public function boot()
{
    Event::listen(function (DatabaseBusy $event) {
        Notification::route('mail', 'dev@example.com')
                ->notify(new DatabaseApproachingMaxConnections(
                    $event->connectionName,
                    $event->connections
                ));
    });
}
```
