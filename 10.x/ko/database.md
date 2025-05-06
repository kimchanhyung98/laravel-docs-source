# 데이터베이스: 시작하기

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기 및 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행하기](#running-queries)
    - [다중 데이터베이스 연결 사용](#using-multiple-database-connections)
    - [쿼리 이벤트 리스닝](#listening-for-query-events)
    - [누적 쿼리 시간 모니터링](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 연결](#connecting-to-the-database-cli)
- [데이터베이스 검사](#inspecting-your-databases)
- [데이터베이스 모니터링](#monitoring-your-databases)

<a name="introduction"></a>
## 소개

대부분의 현대 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 다양한 데이터베이스에서 원시 SQL, [유연한 쿼리 빌더](/docs/{{version}}/queries), 그리고 [Eloquent ORM](/docs/{{version}}/eloquent)을 사용하여 데이터베이스와 손쉽게 상호작용할 수 있도록 지원합니다. 현재 Laravel은 다음 다섯 가지 데이터베이스를 공식적으로 지원합니다:

<div class="content-list" markdown="1">

- MariaDB 10.10+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 11.0+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.8.8+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

<a name="configuration"></a>
### 설정

Laravel의 데이터베이스 서비스에 대한 설정 파일은 애플리케이션의 `config/database.php`에 있습니다. 이 파일에서 모든 데이터베이스 연결을 정의하고, 기본으로 사용할 연결도 지정할 수 있습니다. 대부분의 설정 옵션들은 애플리케이션의 환경 변수 값을 통해 제어됩니다. Laravel이 지원하는 대부분의 데이터베이스 시스템에 대한 예시도 이 파일에 포함되어 있습니다.

기본적으로 Laravel 샘플 [환경 설정](/docs/{{version}}/configuration#environment-configuration)은 [Laravel Sail](/docs/{{version}}/sail)과 함께 바로 사용할 수 있도록 구성되어 있습니다. Laravel Sail은 로컬 개발을 위한 Docker 환경입니다. 물론, 필요하다면 로컬 데이터베이스에 맞게 설정을 자유롭게 변경할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템의 단일 파일 내에 저장됩니다. 터미널에서 `touch` 명령어를 통해 새 SQLite 데이터베이스를 만들 수 있습니다: `touch database/database.sqlite`. 데이터베이스를 생성한 후에는 환경 변수의 `DB_DATABASE`에 데이터베이스의 절대 경로를 지정하여 환경을 쉽게 설정할 수 있습니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

SQLite 연결에서 외래 키 제약 조건을 활성화하려면, 환경 변수 `DB_FOREIGN_KEYS`를 `true`로 설정해야 합니다:

```ini
DB_FOREIGN_KEYS=true
```

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면 `sqlsrv` 및 `pdo_sqlsrv` PHP 확장과 Microsoft SQL ODBC 드라이버 등 관련 종속성이 설치되어 있는지 확인해야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 이용한 설정

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 설정 값으로 구성됩니다. 이러한 값마다 별도의 환경 변수를 사용합니다. 따라서 실제 서버에서 데이터베이스 연결 정보를 설정할 때 여러 환경 변수를 관리해야 합니다.

AWS, Heroku와 같은 일부 관리형 데이터베이스 제공업체는 모든 연결 정보를 하나의 "URL" 문자열로 제공합니다. 데이터베이스 URL의 예시는 다음과 같을 수 있습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이러한 URL은 보통 표준 스키마 규칙을 따릅니다:

```html
driver://username:password@host:port/database?options
```

편의를 위해 Laravel은 여러 설정 옵션 대신 데이터베이스 URL을 지원합니다. 만약 `url`(또는 `DATABASE_URL` 환경 변수) 설정 옵션이 존재하면, 이를 통해 연결 정보와 인증 정보를 추출합니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결

경우에 따라 SELECT 문에는 하나의 연결을, INSERT/UPDATE/DELETE 문에는 다른 연결을 사용하고 싶을 수 있습니다. Laravel은 이를 간편하게 지원하며, 원시 쿼리, 쿼리 빌더, Eloquent ORM 어떤 방식을 사용하든 적절한 연결이 자동으로 선택됩니다.

읽기/쓰기 연결을 설정하는 방법은 다음 예시와 같습니다:

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

설정 배열에는 `read`, `write`, `sticky` 세 개의 키가 새로 추가된 것을 알 수 있습니다. `read`와 `write` 키는 각각 `host`라는 단일 키를 포함하는 배열 값을 가지고 있습니다. 나머지 데이터베이스 설정 값들은 메인 `mysql` 설정 배열에서 병합됩니다.

`read`와 `write` 배열에는 메인 `mysql` 배열의 값을 재정의하려는 경우에만 항목을 추가하면 됩니다. 위의 예시에서는 "읽기" 연결의 호스트로 `192.168.1.1`, "쓰기" 연결에는 `192.168.1.3`이 사용됩니다. 데이터베이스 인증 정보, prefix, 문자셋 등 `mysql` 배열의 다른 설정 값들은 두 연결 모두 공유합니다. `host` 배열에 여러 값이 있을 경우, 요청마다 무작위로 데이터베이스 호스트가 선택됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 현재 요청 중 데이터베이스에 "쓰기" 작업을 수행한 경우 즉시 해당 레코드를 읽을 수 있도록 해주는 *선택적* 값입니다. 이 옵션을 활성화하면, 현재 요청 중 "쓰기" 작업이 발생한 후의 "읽기" 작업들은 모두 "쓰기" 연결을 사용하게 됩니다. 이를 통해 요청 중 쓰인 데이터를 바로 데이터베이스에서 읽어올 수 있습니다. 이 동작이 애플리케이션에 필요한지 여부는 개발자가 결정해야 합니다.

<a name="running-queries"></a>
## SQL 쿼리 실행하기

데이터베이스 연결을 설정한 후에는 `DB` 파사드를 사용하여 쿼리를 실행할 수 있습니다. `DB` 파사드는 `select`, `update`, `insert`, `delete`, `statement` 각각의 쿼리 유형에 맞는 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### SELECT 쿼리 실행하기

기본 SELECT 쿼리를 실행하려면, `DB` 파사드의 `select` 메서드를 사용할 수 있습니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\DB;
    use Illuminate\View\View;

    class UserController extends Controller
    {
        /**
         * 애플리케이션의 모든 사용자 목록을 보여줍니다.
         */
        public function index(): View
        {
            $users = DB::select('select * from users where active = ?', [1]);

            return view('user.index', ['users' => $users]);
        }
    }

`select` 메서드의 첫 번째 인자는 SQL 쿼리이며, 두 번째 인자는 쿼리에 바인딩할 파라미터입니다. 보통 WHERE 절 제약 조건 값이 여기에 해당합니다. 파라미터 바인딩은 SQL 인젝션을 방지합니다.

`select` 메서드는 항상 결과의 `array`를 반환합니다. 배열 안의 각 결과는 데이터베이스 레코드를 나타내는 PHP `stdClass` 객체입니다:

    use Illuminate\Support\Facades\DB;

    $users = DB::select('select * from users');

    foreach ($users as $user) {
        echo $user->name;
    }

<a name="selecting-scalar-values"></a>
#### 스칼라 값 선택

때때로 데이터베이스 쿼리가 하나의 스칼라 값만 반환할 수 있습니다. 이럴 때는 결과 객체에서 값을 꺼낼 필요 없이 `scalar` 메서드를 직접 사용할 수 있습니다:

    $burgers = DB::scalar(
        "select count(case when food = 'burger' then 1 end) as burgers from menu"
    );

<a name="selecting-multiple-result-sets"></a>
#### 다중 결과 집합 조회

저장 프로시저 등에서 여러 결과 집합을 반환하는 경우, `selectResultSets` 메서드를 사용하여 모든 결과 집합을 한 번에 가져올 수 있습니다:

    [$options, $notifications] = DB::selectResultSets(
        "CALL get_user_options_and_notifications(?)", $request->user()->id
    );

<a name="using-named-bindings"></a>
#### 이름 있는 바인딩 사용

파라미터 바인딩에 `?` 대신 이름 있는 바인딩을 사용할 수도 있습니다:

    $results = DB::select('select * from users where id = :id', ['id' => 1]);

<a name="running-an-insert-statement"></a>
#### INSERT문 실행

`insert` 문을 실행하려면, `DB` 파사드의 `insert` 메서드를 사용합니다. `select`와 마찬가지로 첫 번째 인자는 SQL 쿼리, 두 번째 인자는 파라미터 바인딩 배열입니다:

    use Illuminate\Support\Facades\DB;

    DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);

<a name="running-an-update-statement"></a>
#### UPDATE문 실행

`update` 메서드는 데이터베이스 내 기존 레코드를 수정할 때 사용합니다. 영향을 받은 행의 수가 반환됩니다:

    use Illuminate\Support\Facades\DB;

    $affected = DB::update(
        'update users set votes = 100 where name = ?',
        ['Anita']
    );

<a name="running-a-delete-statement"></a>
#### DELETE문 실행

`delete` 메서드는 데이터베이스 레코드를 삭제할 때 사용합니다. 역시 영향을 받은 행의 수가 반환됩니다:

    use Illuminate\Support\Facades\DB;

    $deleted = DB::delete('delete from users');

<a name="running-a-general-statement"></a>
#### 일반 쿼리문 실행

결과를 반환하지 않는 데이터베이스 명령도 있습니다. 이런 경우 `DB` 파사드의 `statement` 메서드를 사용할 수 있습니다:

    DB::statement('drop table users');

<a name="running-an-unprepared-statement"></a>
#### Unprepared Statement 실행

파라미터 바인딩 없이 SQL을 실행하고자 할 때는 `DB` 파사드의 `unprepared` 메서드를 사용할 수 있습니다:

    DB::unprepared('update users set votes = 100 where name = "Dries"');

> [!WARNING]  
> unprepared 문장은 파라미터 바인딩을 사용하지 않으므로 SQL 인젝션에 취약할 수 있습니다. 사용자로부터 받아온 값을 unprepared 문의 인자로 절대 사용하지 마십시오.

<a name="implicit-commits-in-transactions"></a>
#### 암묵적 커밋 주의

트랜잭션 내에서 `DB` 파사드의 `statement`나 `unprepared` 메서드를 사용할 때, [암묵적 커밋](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 유발하는 문장을 피해야 합니다. 이런 문장을 실행하면 데이터베이스 엔진이 전체 트랜잭션을 암묵적으로 커밋하게 되고, Laravel은 트랜잭션 상태를 인지하지 못하게 됩니다. 예를 들어, 테이블을 새로 만드는 문장이 여기에 해당합니다:

    DB::unprepared('create table a (col varchar(1) null)');

어떤 문장이 암묵적 커밋을 발생시키는지에 대해서는 [MySQL 매뉴얼](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 참조하세요.

<a name="using-multiple-database-connections"></a>
### 다중 데이터베이스 연결 사용

애플리케이션의 `config/database.php` 설정 파일에 여러 연결을 정의한 경우, `DB` 파사드의 `connection` 메서드를 통해 각각의 연결을 사용할 수 있습니다. 전달하는 연결 이름은 설정 파일에 있는 연결명과 일치해야 하며, 또는 런타임의 `config` 헬퍼로 지정할 수도 있습니다:

    use Illuminate\Support\Facades\DB;

    $users = DB::connection('sqlite')->select(/* ... */);

연결 인스턴스의 `getPdo` 메서드를 사용하면 하위의 원시 PDO 인스턴스에 접근할 수 있습니다:

    $pdo = DB::connection()->getPdo();

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 리스닝

애플리케이션에서 실행되는 각 SQL 쿼리에 대해 호출되는 클로저를 지정하고 싶다면, `DB` 파사드의 `listen` 메서드를 사용할 수 있습니다. 이는 쿼리 로깅이나 디버깅에 유용합니다. [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 쿼리 리스너 클로저를 등록할 수 있습니다:

    <?php

    namespace App\Providers;

    use Illuminate\Database\Events\QueryExecuted;
    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스 등록
         */
        public function register(): void
        {
            // ...
        }

        /**
         * 애플리케이션 서비스 부트스트랩
         */
        public function boot(): void
        {
            DB::listen(function (QueryExecuted $query) {
                // $query->sql;
                // $query->bindings;
                // $query->time;
            });
        }
    }

<a name="monitoring-cumulative-query-time"></a>
### 누적 쿼리 시간 모니터링

현대 웹 애플리케이션의 주요 성능 병목 중 하나는 데이터베이스 쿼리에 소요되는 시간입니다. 다행히도 Laravel은 단일 요청에서 데이터베이스 쿼리 시간이 임계치(밀리초 단위)를 넘기면 지정한 클로저나 콜백을 호출할 수 있습니다. 시작하려면, `whenQueryingForLongerThan` 메서드에 쿼리 시간 임계값(밀리초)과 클로저를 전달하세요. 이 메서드는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드 내에서 호출할 수 있습니다:

    <?php

    namespace App\Providers;

    use Illuminate\Database\Connection;
    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\ServiceProvider;
    use Illuminate\Database\Events\QueryExecuted;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스 등록
         */
        public function register(): void
        {
            // ...
        }

        /**
         * 애플리케이션 서비스 부트스트랩
         */
        public function boot(): void
        {
            DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {
                // 개발팀에 알림...
            });
        }
    }

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 여러 작업을 실행하려면, `DB` 파사드의 `transaction` 메서드를 사용할 수 있습니다. 트랜잭션 클로저 안에서 예외가 발생하면 트랜잭션을 자동으로 롤백하고 예외를 다시 발생시킵니다. 클로저가 정상적으로 실행되면 트랜잭션이 자동으로 커밋됩니다. 즉, 수동으로 롤백이나 커밋을 걱정할 필요가 없습니다:

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    });

<a name="handling-deadlocks"></a>
#### 데드락(교착상태) 처리

`transaction` 메서드는 데드락이 발생했을 때 트랜잭션을 재시도할 횟수를 지정하는 선택적 두 번째 인자를 받을 수 있습니다. 재시도 횟수를 모두 소진하면 예외가 발생합니다:

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    }, 5);

<a name="manually-using-transactions"></a>
#### 수동 트랜잭션 실행

트랜잭션을 직접 시작하고 롤백 및 커밋을 완전히 제어하고 싶을 때는 `DB` 파사드의 `beginTransaction` 메서드를 사용할 수 있습니다:

    use Illuminate\Support\Facades\DB;

    DB::beginTransaction();

트랜잭션을 롤백하려면 `rollBack` 메서드를 사용하세요:

    DB::rollBack();

마지막으로, `commit` 메서드로 트랜잭션을 커밋할 수 있습니다:

    DB::commit();

> [!NOTE]  
> `DB` 파사드의 트랜잭션 메서드는 [쿼리 빌더](/docs/{{version}}/queries)와 [Eloquent ORM](/docs/{{version}}/eloquent) 모두의 트랜잭션을 제어합니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 연결

데이터베이스의 CLI에 연결하려면, `db` 아티즌 명령어를 사용할 수 있습니다:

```shell
php artisan db
```

필요하다면, 기본 연결이 아닌 특정 데이터베이스 연결명을 지정하여 연결할 수도 있습니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 검사

`db:show` 및 `db:table` 아티즌 명령어를 사용하면 데이터베이스와 관련 테이블에 대한 유용한 정보를 얻을 수 있습니다. 데이터베이스의 개요(크기, 타입, 열린 연결 수, 테이블 요약 등)를 확인하려면 `db:show` 명령어를 사용하세요:

```shell
php artisan db:show
```

`--database` 옵션으로 검사할 데이터베이스 연결명을 지정할 수 있습니다:

```shell
php artisan db:show --database=pgsql
```

테이블 행 수와 데이터베이스 뷰 정보까지 출력에 포함하려면 `--counts`, `--views` 옵션을 각각 추가하면 됩니다. 대용량 데이터베이스는 이 과정이 느릴 수 있습니다:

```shell
php artisan db:show --counts --views
```

<a name="table-overview"></a>
#### 테이블 개요

데이터베이스 내 개별 테이블의 정보를 확인하려면 `db:table` 아티즌 명령어를 실행하세요. 이 명령어는 테이블의 컬럼, 타입, 속성, 키, 인덱스 등을 포함해 전반적인 개요를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링

`db:monitor` 아티즌 명령어를 통해, 데이터베이스의 열린 연결 수가 지정한 임계치를 초과하면 Laravel이 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 디스패치하도록 할 수 있습니다.

먼저, 이 명령어가 [1분마다 실행](/docs/{{version}}/scheduling)되도록 예약하세요. 명령어는 모니터링할 데이터베이스 연결명과, 이벤트를 발생시키기 전 허용할 최대 연결 수를 인자로 받습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

이 명령어를 예약하는 것만으로는 경고 알림이 전송되지 않습니다. 임계치를 초과한 열린 연결이 발견되면 `DatabaseBusy` 이벤트가 디스패치됩니다. 알림을 받으려면 애플리케이션의 `EventServiceProvider`에서 이 이벤트를 리스닝하여 개발팀이나 사용자에게 알릴 수 있습니다:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 애플리케이션의 다른 이벤트 등록
 */
public function boot(): void
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
