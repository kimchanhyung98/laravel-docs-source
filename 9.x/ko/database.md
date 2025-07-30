# 데이터베이스: 시작하기 (Database: Getting Started)

- [소개](#introduction)
    - [구성](#configuration)
    - [읽기 및 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행하기](#running-queries)
    - [다중 데이터베이스 연결 사용하기](#using-multiple-database-connections)
    - [쿼리 이벤트 청취하기](#listening-for-query-events)
    - [누적 쿼리 시간 모니터링](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 연결하기](#connecting-to-the-database-cli)
- [데이터베이스 검사하기](#inspecting-your-databases)
- [데이터베이스 모니터링하기](#monitoring-your-databases)

<a name="introduction"></a>
## 소개 (Introduction)

거의 모든 현대 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 다양한 지원 데이터베이스에서 원시 SQL(raw SQL), [유창한 쿼리 빌더(fluent query builder)](/docs/9.x/queries), 그리고 [Eloquent ORM](/docs/9.x/eloquent)을 이용해 데이터베이스와 상호작용하는 것을 매우 간단하게 만듭니다. 현재 Laravel은 다음 다섯 가지 데이터베이스에 대해 공식 지원을 제공합니다:

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.8.8+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

<a name="configuration"></a>
### 구성 (Configuration)

Laravel의 데이터베이스 서비스 구성은 애플리케이션의 `config/database.php` 설정 파일에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의할 수 있으며, 기본으로 사용될 연결을 지정할 수 있습니다. 이 파일 내 대부분 설정 옵션은 애플리케이션의 환경 변수 값을 기반으로 동작합니다. Laravel에서 지원하는 대부분의 데이터베이스 시스템 예제가 이 파일에 포함되어 있습니다.

기본적으로 Laravel 샘플 [환경 구성](/docs/9.x/configuration#environment-configuration)은 로컬 머신에서 Laravel 애플리케이션을 개발하기 위한 Docker 구성인 [Laravel Sail](/docs/9.x/sail) 사용에 적합하게 준비되어 있습니다. 그러나 필요에 따라 로컬 데이터베이스 구성을 자유롭게 수정할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 구성

SQLite 데이터베이스는 파일 시스템 내 한 개 파일로 유지됩니다. 터미널에서 `touch` 명령어로 새 SQLite 데이터베이스를 만들 수 있습니다: `touch database/database.sqlite`. 데이터베이스가 생성된 후에는 환경 변수 `DB_DATABASE`에 데이터베이스의 절대 경로를 지정해 환경 변수를 쉽게 구성할 수 있습니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

SQLite 연결에 대한 외래 키 제약을 활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `true`로 설정해야 합니다:

```ini
DB_FOREIGN_KEYS=true
```

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 구성

Microsoft SQL Server 데이터베이스를 사용하려면 `sqlsrv` 및 `pdo_sqlsrv` PHP 확장과 Microsoft SQL ODBC 드라이버 같은 필수 의존성이 설치되어 있어야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 이용한 구성

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 설정값을 이용해 구성합니다. 각각의 값은 대응하는 환경 변수로 제공됩니다. 즉, 운영 서버에서 데이터베이스 연결 정보를 설정할 경우 여러 환경 변수를 관리해야 합니다.

AWS, Heroku 같은 일부 관리형 데이터베이스 제공자는 데이터베이스 연결 정보를 모두 포함한 하나의 "URL"을 제공합니다. 예를 들어 다음과 같은 데이터베이스 URL이 있을 수 있습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

일반적으로 이 URL은 다음과 같은 표준 스키마 형식을 따릅니다:

```html
driver://username:password@host:port/database?options
```

편의를 위해 Laravel은 여러 설정값 대신 이 URL을 지원합니다. `url` 설정 또는 해당하는 `DATABASE_URL` 환경 변수가 존재하면 이 값으로부터 데이터베이스 연결 및 자격 정보가 추출되어 사용됩니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결 (Read & Write Connections)

때로는 SELECT 문에 하나의 데이터베이스 연결을 사용하고, INSERT, UPDATE 및 DELETE 문에는 다른 연결을 사용하고 싶을 때가 있습니다. Laravel은 이를 간편하게 처리하며, 원시 쿼리, 쿼리 빌더, Eloquent ORM 사용 여부에 관계 없이 적절한 연결을 항상 사용합니다.

읽기/쓰기 연결 구성이 어떻게 이루어지는지 다음 예제를 보겠습니다:

```
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
```

`read`, `write`, `sticky` 세 가지 키가 배열에 추가된 것을 볼 수 있습니다. `read`와 `write`는 `host`라는 키를 가진 배열 값을 가집니다. 나머지 `mysql` 설정 배열의 데이터베이스 옵션들은 `read`와 `write` 연결에 병합되어 사용됩니다.

`read`와 `write` 배열에는 기본 `mysql` 배열의 값을 덮어쓰고자 할 때만 값을 넣는 것이 필요합니다. 이 예에서 `192.168.1.1`은 "읽기" 연결의 호스트로 사용되고, `196.168.1.3`은 "쓰기" 연결의 호스트로 사용됩니다. 데이터베이스 자격증명, 접두사, 문자셋 등 나머지 옵션은 두 연결에 공유됩니다. `host` 배열에 값이 여러 개 있을 경우, 각 요청마다 무작위로 호스트가 선택됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 *선택 사항*으로, 현재 요청 주기 내에 데이터베이스에 "쓰기" 작업이 수행되었을 경우, 이후의 모든 "읽기" 작업을 같은 "쓰기" 연결에서 수행하도록 허용합니다. 이렇게 하면 요청 주기 내에 쓰여진 데이터가 즉시 동일 요청 내에서 다시 읽힐 수 있습니다. 애플리케이션에서 이 동작이 필요한지 여부는 여러분이 결정하시면 됩니다.

<a name="running-queries"></a>
## SQL 쿼리 실행하기 (Running SQL Queries)

데이터베이스 연결 구성을 완료하면 `DB` 파사드를 이용해 쿼리를 실행할 수 있습니다. `DB` 파사드는 `select`, `update`, `insert`, `delete`, `statement` 등의 쿼리 유형별 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### SELECT 쿼리 실행하기

기본 SELECT 쿼리를 실행하려면 `DB` 파사드의 `select` 메서드를 사용할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class UserController extends Controller
{
    /**
     * 애플리케이션에 등록된 모든 사용자 목록을 보여줍니다.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $users = DB::select('select * from users where active = ?', [1]);

        return view('user.index', ['users' => $users]);
    }
}
```

`select` 메서드의 첫 번째 인수는 SQL 쿼리이고, 두 번째 인수는 쿼리에 바인딩할 파라미터입니다. 보통 `where` 절 조건 값들이 여기 포함됩니다. 파라미터 바인딩은 SQL 인젝션 공격으로부터 보호해 줍니다.

`select` 메서드는 항상 결과 배열을 반환합니다. 배열의 각 결과는 데이터베이스 레코드를 표현하는 PHP의 `stdClass` 객체입니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="selecting-scalar-values"></a>
#### 단일 스칼라 값 선택하기

쿼리 결과가 하나의 단일 스칼라 값일 경우, 레코드 객체로부터 값을 꺼내지 않고 `scalar` 메서드로 직접 값을 얻을 수 있습니다:

```
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="using-named-bindings"></a>
#### 이름 있는 바인딩 사용하기

`?` 대신 이름이 지정된 바인딩(named bindings)을 사용할 수도 있습니다:

```
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
#### INSERT 문 실행하기

`insert` 명령문 실행 시 `DB` 파사드의 `insert` 메서드를 사용합니다. `select`와 동일하게 첫 번째 인수는 SQL, 두 번째 인수는 바인딩 값들을 받습니다:

```
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
#### UPDATE 문 실행하기

기존 레코드를 수정하려면 `update` 메서드를 사용합니다. 이 메서드는 영향을 받은 행의 수를 반환합니다:

```
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
#### DELETE 문 실행하기

레코드를 삭제하려면 `delete` 메서드를 사용합니다. `update`와 마찬가지로 영향을 받은 행 수를 반환합니다:

```
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
#### 일반 명령 실행하기

값을 반환하지 않는 SQL 명령을 실행할 때는 `statement` 메서드를 사용합니다:

```
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
#### 준비되지 않은 명령 실행하기

바인딩 없이 SQL 명령을 실행하고 싶을 때는 `unprepared` 메서드를 사용합니다:

```
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]
> 준비되지 않은 명령은 파라미터 바인딩을 하지 않으므로 SQL 인젝션 공격에 취약할 수 있습니다. 사용자 입력값을 포함시키는 것은 절대 허용해서는 안 됩니다.

<a name="implicit-commits-in-transactions"></a>
#### 암묵적 커밋 (Implicit Commits)

트랜잭션 안에서 `DB` 파사드의 `statement` 및 `unprepared` 메서드를 사용할 때는 [암묵적 커밋](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 발생시키는 문장에 주의해야 합니다. 암묵적 커밋이 일어나면 데이터베이스 엔진이 트랜잭션을 자동 커밋 하지만 Laravel은 이 상태를 알지 못합니다. 예를 들어 테이블을 생성하는 명령이 여기에 해당합니다:

```
DB::unprepared('create table a (col varchar(1) null)');
```

암묵적 커밋을 일으키는 모든 문장 목록은 MySQL 매뉴얼의 [암묵적 커밋 문서](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)를 참조하세요.

<a name="using-multiple-database-connections"></a>
### 다중 데이터베이스 연결 사용하기 (Using Multiple Database Connections)

`config/database.php`에 여러 데이터베이스 연결을 정의한 경우, 각각의 연결을 `DB` 파사드의 `connection` 메서드로 접근할 수 있습니다. `connection` 메서드에 넘기는 이름은 `config/database.php`에 정의된 연결 이름이어야 하며, 런타임에 `config` 헬퍼로 구성할 수도 있습니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

연결 인스턴스의 기초 PDO 객체는 `getPdo` 메서드로 직접 접근할 수 있습니다:

```
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 청취하기 (Listening For Query Events)

애플리케이션에서 실행되는 각 SQL 쿼리에 대해 호출할 클로저(Closure)를 등록하려면 `DB` 파사드의 `listen` 메서드를 사용합니다. 쿼리 로깅이나 디버깅에 유용합니다. 보통 [서비스 프로바이더](/docs/9.x/providers)의 `boot` 메서드에서 등록합니다:

```
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
```

<a name="monitoring-cumulative-query-time"></a>
### 누적 쿼리 시간 모니터링 (Monitoring Cumulative Query Time)

현대 웹 애플리케이션에서 자주 발생하는 성능 병목 중 하나는 데이터베이스 쿼리에 소요되는 시간입니다. 다행히도 Laravel은 한 요청에서 쿼리 시간이 너무 오래 걸릴 경우 지정한 클로저나 콜백을 호출할 수 있습니다. 시작하려면 밀리초 단위의 쿼리 시간 임계치와 클로저를 `whenQueryingForLongerThan` 메서드에 전달합니다. 이 역시 [서비스 프로바이더](/docs/9.x/providers)의 `boot` 메서드에서 호출합니다:

```
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
            // 개발팀에 알림을 보냅니다...
        });
    }
}
```

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션 (Database Transactions)

`DB` 파사드의 `transaction` 메서드를 사용하면 일련의 작업을 데이터베이스 트랜잭션 내에서 실행할 수 있습니다. 트랜잭션 클로저 내에서 예외가 발생하면 자동으로 롤백되며 예외가 다시 던져집니다. 클로저가 정상 실행되면 자동으로 커밋됩니다. `transaction` 메서드를 사용할 때 롤백이나 커밋을 직접 처리할 필요가 없습니다:

```
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
#### 데드락 처리

`transaction` 메서드는 선택적 두 번째 인수로 트랜잭션이 데드락 데서 재시도할 횟수를 지정할 수 있습니다. 지정된 횟수만큼 시도 후에도 실패하면 예외가 발생합니다:

```
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, 5);
```

<a name="manually-using-transactions"></a>
#### 수동으로 트랜잭션 사용하기

트랜잭션을 수동으로 시작하고 롤백이나 커밋을 직접 제어하려면 `DB` 파사드의 `beginTransaction` 메서드를 사용합니다:

```
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

트랜잭션 롤백은 `rollBack` 메서드로 수행합니다:

```
DB::rollBack();
```

마지막으로 커밋은 `commit` 메서드로 실행합니다:

```
DB::commit();
```

> [!NOTE]
> `DB` 파사드의 트랜잭션 메서드는 [쿼리 빌더](/docs/9.x/queries)와 [Eloquent ORM](/docs/9.x/eloquent) 모두에 대한 트랜잭션을 관리합니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 연결하기 (Connecting To The Database CLI)

데이터베이스의 CLI에 연결하려면 `db` Artisan 명령어를 사용합니다:

```shell
php artisan db
```

필요할 경우 기본 연결이 아닌 특정 데이터베이스 연결 이름을 지정할 수 있습니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 검사하기 (Inspecting Your Databases)

`db:show`와 `db:table` Artisan 명령어를 이용하면 데이터베이스 및 관련 테이블에 관한 유용한 정보를 얻을 수 있습니다. 데이터베이스의 크기, 타입, 열린 연결 수, 테이블 요약 정보를 확인하려면 `db:show` 명령어를 사용하세요:

```shell
php artisan db:show
```

점검할 데이터베이스 연결 이름을 `--database` 옵션에 지정할 수 있습니다:

```shell
php artisan db:show --database=pgsql
```

테이블의 행(row) 개수와 데이터베이스 뷰(view) 상세 정보를 포함하려면 각각 `--counts`와 `--views` 옵션을 지정하세요. 대용량 데이터베이스에서는 이 작업이 느릴 수 있습니다:

```shell
php artisan db:show --counts --views
```

<a name="table-overview"></a>
#### 테이블 개요

데이터베이스 내 특정 테이블에 대한 개요를 얻으려면 `db:table` Artisan 명령어를 사용하세요. 이 명령은 컬럼, 타입, 속성, 키, 인덱스 등 데이터베이스 테이블에 관한 일반적인 정보를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링하기 (Monitoring Your Databases)

`db:monitor` Artisan 명령어를 사용하면 특정 연결의 열린 연결 수가 지정 한계치를 초과할 경우 Laravel이 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 발송하게 할 수 있습니다.

시작하려면 이 명령어를 [매 분마다 실행](/docs/9.x/scheduling)되도록 예약해야 합니다. 모니터링할 데이터베이스 연결 이름들과 경고를 발생시킬 최대 열린 연결 수를 지정할 수 있습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

이 명령어 예약만으로는 열린 연결 수를 알리는 알림이 발생하지 않습니다. 명령어 실행 중 열린 연결 수가 임계치를 넘는 데이터베이스가 발견되어야 `DatabaseBusy` 이벤트가 발생합니다. 이 이벤트를 `EventServiceProvider`에서 감지하여 개발자나 담당자에게 알림을 보내도록 해야 합니다:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 애플리케이션에서 다른 이벤트를 등록합니다.
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