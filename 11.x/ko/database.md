# 데이터베이스: 시작하기 (Database: Getting Started)

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기 및 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행하기](#running-queries)
    - [여러 데이터베이스 연결 사용하기](#using-multiple-database-connections)
    - [쿼리 이벤트 리스닝](#listening-for-query-events)
    - [누적 쿼리 시간 모니터링](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 연결하기](#connecting-to-the-database-cli)
- [데이터베이스 검사하기](#inspecting-your-databases)
- [데이터베이스 모니터링](#monitoring-your-databases)

<a name="introduction"></a>
## 소개 (Introduction)

거의 모든 현대 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 다양한 지원 데이터베이스에서 원시 SQL, [플루언트 쿼리 빌더](/docs/11.x/queries), 및 [Eloquent ORM](/docs/11.x/eloquent)을 사용하여 데이터베이스와 상호작용하는 작업을 매우 간단하게 만듭니다. 현재 Laravel은 다섯 가지 데이터베이스를 공식적으로 지원합니다:

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

또한, MongoDB도 MongoDB에서 공식 유지하는 `mongodb/laravel-mongodb` 패키지를 통해 지원됩니다. 자세한 내용은 [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 문서를 참고하세요.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel 데이터베이스 서비스의 설정은 애플리케이션의 `config/database.php` 설정 파일에 위치해 있습니다. 이 파일에서 모든 데이터베이스 연결들을 정의할 수 있으며, 기본으로 사용할 연결을 지정할 수 있습니다. 이 파일 내 대부분의 설정 옵션은 애플리케이션의 환경 변수 값에 의해 작동합니다. Laravel이 지원하는 대부분의 데이터베이스 시스템 예제가 이 파일에 포함되어 있습니다.

기본적으로, Laravel의 기본 [환경 구성](/docs/11.x/configuration#environment-configuration)은 [Laravel Sail](/docs/11.x/sail)과 함께 바로 쓸 수 있도록 되어 있습니다. Laravel Sail은 로컬 개발을 위한 Docker 구성입니다. 물론, 필요에 따라 로컬 데이터베이스용으로 설정을 수정할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템 내 단일 파일로 저장됩니다. 터미널에서 `touch` 명령을 사용하여 새 SQLite 데이터베이스를 생성할 수 있습니다: `touch database/database.sqlite`. 데이터베이스가 생성되면 환경 변수 `DB_DATABASE`에 데이터베이스의 절대 경로를 지정하여 쉽게 연결할 수 있습니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

기본적으로 SQLite 연결은 외래 키 제약 조건이 활성화되어 있습니다. 이를 비활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `false`로 설정하세요:

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]  
> [Laravel 설치 도구](/docs/11.x/installation#creating-a-laravel-project)를 사용하여 Laravel 애플리케이션을 생성할 때 SQLite를 선택하면, Laravel이 자동으로 `database/database.sqlite` 파일을 만들고 기본 [데이터베이스 마이그레이션](/docs/11.x/migrations)을 실행합니다.

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면, `sqlsrv`와 `pdo_sqlsrv` PHP 확장 모듈과 Microsoft SQL ODBC 드라이버 같은 필요 의존성을 설치해야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 이용한 설정

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 같이 여러 설정 값을 통해 구성합니다. 각 설정에는 독립적인 환경 변수가 존재합니다. 따라서 운영 서버에서는 많은 환경 변수를 관리해야 합니다.

AWS, Heroku 같은 관리형 데이터베이스 제공자는 데이터베이스 연결 정보 전체를 하나의 문자열인 데이터베이스 "URL" 형태로 제공합니다. 예시는 아래와 같습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이 URL은 보통 표준 스키마 규칙을 따릅니다:

```html
driver://username:password@host:port/database?options
```

편의를 위해 Laravel은 여러 설정 대신 이 URL을 사용해 데이터베이스 연결과 인증 정보를 추출하는 방식을 지원합니다. `url` 설정 값이나 대응되는 `DB_URL` 환경 변수가 존재할 경우, 이 값을 우선적으로 사용합니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결 (Read and Write Connections)

때때로 SELECT 문에는 하나의 데이터베이스 연결을, INSERT, UPDATE, DELETE 문에는 다른 연결을 사용하고 싶을 수 있습니다. Laravel에서는 이를 쉽게 설정할 수 있으며, 원시 쿼리, 쿼리 빌더, Eloquent ORM을 사용할 때도 올바른 연결이 자동으로 선택됩니다.

예를 들어, 다음과 같이 읽기/쓰기 연결을 설정할 수 있습니다:

```php
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

    'database' => env('DB_DATABASE', 'laravel'),
    'username' => env('DB_USERNAME', 'root'),
    'password' => env('DB_PASSWORD', ''),
    'unix_socket' => env('DB_SOCKET', ''),
    'charset' => env('DB_CHARSET', 'utf8mb4'),
    'collation' => env('DB_COLLATION', 'utf8mb4_unicode_ci'),
    'prefix' => '',
    'prefix_indexes' => true,
    'strict' => true,
    'engine' => null,
    'options' => extension_loaded('pdo_mysql') ? array_filter([
        PDO::MYSQL_ATTR_SSL_CA => env('MYSQL_ATTR_SSL_CA'),
    ]) : [],
],
```

여기서 세 개의 키, `read`, `write`, `sticky`가 추가되었습니다. `read`와 `write`는 각각 배열이며 내부에 `host` 키가 있습니다. `read`와 `write` 연결의 나머지 데이터베이스 옵션은 주 설정 배열 `mysql`에서 병합됩니다.

즉, `read`와 `write` 배열에 값을 넣는 것은 기본 `mysql` 설정을 오버라이드하려는 경우에만 필요합니다. 위 예에서는 `192.168.1.1`과 `192.168.1.2`가 "읽기"용 호스트로 무작위 선택되고, `196.168.1.3`이 "쓰기"용 호스트로 사용됩니다. 데이터베이스 자격증명, 접두사, 문자 집합 등 나머지 옵션들은 두 연결에서 공통으로 공유됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 *선택 사항*으로, 현재 요청 주기 내에 데이터베이스에 "쓰기" 작업이 이뤄진 경우, 이후 "읽기" 작업을 동일한 "쓰기" 연결로 강제하는 기능입니다. 이렇게 하면 쓰기 작업 후 즉시 동일한 데이터를 읽을 수 있습니다. 이러한 동작이 애플리케이션에 적합한지 여부는 직접 판단해야 합니다.

<a name="running-queries"></a>
## SQL 쿼리 실행하기 (Running SQL Queries)

데이터베이스 연결을 설정한 후, `DB` 파사드를 사용해 쿼리를 실행할 수 있습니다. `DB` 파사드는 `select`, `update`, `insert`, `delete`, `statement`와 같은 쿼리 유형별 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### SELECT 쿼리 실행하기

기본적인 SELECT 쿼리는 `DB` 파사드의 `select` 메서드로 실행합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션 모든 사용자의 목록을 보여줍니다.
     */
    public function index(): View
    {
        $users = DB::select('select * from users where active = ?', [1]);

        return view('user.index', ['users' => $users]);
    }
}
```

`select` 메서드의 첫 번째 인수는 SQL 쿼리이며, 두 번째 인수는 쿼리에 바인딩할 파라미터 값들입니다. 보통 `where` 절 조건의 값들이며, 파라미터 바인딩 덕분에 SQL 인젝션 공격을 방어할 수 있습니다.

`select` 메서드는 항상 결과를 `array`로 반환합니다. 배열 내 각 원소는 데이터베이스 레코드를 나타내는 PHP의 `stdClass` 객체입니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="selecting-scalar-values"></a>
#### 스칼라 값 선택하기

가끔 쿼리 결과가 하나의 스칼라 값일 경우, 레코드 객체에서 직접 값을 꺼내는 대신 `scalar` 메서드를 사용해 바로 값을 가져올 수 있습니다:

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
#### 다중 결과 집합 선택하기

저장 프로시저가 여러 결과 집합을 반환할 경우, `selectResultSets` 메서드를 사용해 모든 결과 집합을 가져올 수 있습니다:

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
#### 명명된 바인딩 사용하기

`?` 대신 명명된 바인딩을 사용해 쿼리를 실행할 수도 있습니다:

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
#### INSERT 문 실행하기

`insert` 메서드를 사용해 INSERT 쿼리를 실행할 수 있습니다. 사용법은 `select`와 비슷하며, 첫 번째 인수가 SQL, 두 번째 인수가 바인딩 배열입니다:

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
#### UPDATE 문 실행하기

기존 레코드를 업데이트할 때는 `update` 메서드를 사용합니다. 영향 받은 행(row) 수가 반환됩니다:

```php
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
#### DELETE 문 실행하기

레코드를 삭제할 때는 `delete` 메서드를 사용하며, `update`처럼 영향 받은 행 수가 반환됩니다:

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
#### 일반 SQL 문 실행하기

결과를 반환하지 않는 SQL 문은 `statement` 메서드로 실행합니다:

```php
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
#### 준비되지 않은 SQL 문 실행하기

값 바인딩 없이 SQL 문을 실행하려면 `unprepared` 메서드를 사용합니다:

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]  
> 준비되지 않은(unprepared) 문은 파라미터 바인딩을 하지 않기 때문에 SQL 인젝션 공격에 취약할 수 있습니다. 사용자 입력값이 직접 포함된 쿼리는 절대 사용하지 마세요.

<a name="implicit-commits-in-transactions"></a>
#### 암묵적 커밋(Implicit Commits)

`DB` 파사드의 `statement` 와 `unprepared` 메서드를 트랜잭션 내에서 사용할 때는 [암묵적 커밋](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 유발하는 쿼리를 주의해야 합니다. 이런 쿼리는 트랜잭션 전체를 데이터베이스가 직접 커밋하도록 만들어 Laravel이 트랜잭션 상태를 인지하지 못하게 만듭니다. 예를 들어 테이블 생성 쿼리는 암묵적 커밋을 일으킵니다:

```php
DB::unprepared('create table a (col varchar(1) null)');
```

MySQL 매뉴얼에서 [암묵적 커밋을 유발하는 모든 쿼리](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) 목록을 참고하세요.

<a name="using-multiple-database-connections"></a>
### 여러 데이터베이스 연결 사용하기 (Using Multiple Database Connections)

`config/database.php`에 여러 연결이 정의되어 있다면, `DB` 파사드의 `connection` 메서드를 통해 특정 연결을 사용할 수 있습니다. `connection`에 넘긴 이름은 설정 파일에 존재하는 연결 이름이어야 합니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

특정 연결의 내부 PDO 인스턴스도 `getPdo` 메서드로 접근할 수 있습니다:

```php
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 리스닝 (Listening for Query Events)

애플리케이션에서 실행하는 모든 SQL 쿼리별로 클로저를 등록해 실행 후 동작을 처리할 수 있습니다. 이는 쿼리 로그 기록이나 디버깅에 유용합니다. 서비스 프로바이더의 `boot` 메서드에 다음과 같이 작성하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Database\Events\QueryExecuted;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        DB::listen(function (QueryExecuted $query) {
            // $query->sql;
            // $query->bindings;
            // $query->time;
            // $query->toRawSql();
        });
    }
}
```

<a name="monitoring-cumulative-query-time"></a>
### 누적 쿼리 시간 모니터링 (Monitoring Cumulative Query Time)

모던 웹 애플리케이션의 주요 성능 병목은 데이터베이스 쿼리에 소모하는 시간입니다. Laravel은 단일 요청에서 쿼리 시간이 지정한 임계값을 초과할 때 특정 클로저나 콜백을 호출하도록 할 수 있습니다. 서비스 프로바이더의 `boot` 메서드에 다음처럼 작성합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Database\Connection;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;
use Illuminate\Database\Events\QueryExecuted;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {
            // 개발팀에게 알림 등 작업 수행...
        });
    }
}
```

위 예시에서는 단일 요청에서 500ms 이상 쿼리가 지속되면 지정한 콜백이 실행됩니다.

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션 (Database Transactions)

`DB` 파사드의 `transaction` 메서드를 사용하면 트랜잭션 내에서 일련의 작업을 실행할 수 있습니다. 클로저 내부에서 예외가 발생하면 트랜잭션이 자동으로 롤백되고 예외가 다시 던져집니다. 클로저가 성공적으로 실행되면 자동으로 커밋됩니다. 직접 롤백이나 커밋을 신경 쓸 필요가 없습니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
#### 데드락 처리하기

`transaction` 메서드는 선택적 두 번째 인수로 데드락 발생 시 재시도 횟수를 정할 수 있습니다. 재시도 횟수 초과 시 예외가 던져집니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, 5);
```

<a name="manually-using-transactions"></a>
#### 트랜잭션 수동 사용

트랜잭션을 수동으로 시작하고 롤백 및 커밋을 직접 제어하려면 다음 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

롤백은 `rollBack` 메서드로 합니다:

```php
DB::rollBack();
```

커밋은 `commit` 메서드로 합니다:

```php
DB::commit();
```

> [!NOTE]  
> `DB` 파사드의 트랜잭션 메서드는 [쿼리 빌더](/docs/11.x/queries)와 [Eloquent ORM](/docs/11.x/eloquent) 모두에 적용됩니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 연결하기 (Connecting to the Database CLI)

데이터베이스 CLI에 연결하려면 `db` Artisan 명령어를 사용하세요:

```shell
php artisan db
```

기본 연결이 아닌 특정 데이터베이스 연결을 지정하려면 연결 이름을 명령어 뒤에 붙입니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 검사하기 (Inspecting Your Databases)

`db:show` 와 `db:table` Artisan 명령어를 통해 데이터베이스와 테이블에 관한 유용한 정보를 볼 수 있습니다. 데이터베이스 크기, 유형, 열려있는 연결 수, 테이블 요약 등을 확인하려면 `db:show` 명령어를 사용하세요:

```shell
php artisan db:show
```

검사할 데이터베이스 연결명을 `--database` 옵션으로 지정할 수 있습니다:

```shell
php artisan db:show --database=pgsql
```

또한, 테이블 행(row) 수와 데이터베이스 뷰(view) 상세 정보를 포함하려면 `--counts` 와 `--views` 옵션을 각각 지정하세요. 대규모 데이터베이스에서는 이 옵션들이 실행 속도를 늦출 수 있습니다:

```shell
php artisan db:show --counts --views
```

다음 `Schema` 메서드들을 사용해 데이터베이스를 검사할 수도 있습니다:

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

기본 연결이 아닌 다른 연결에서 검사하려면 `connection` 메서드를 사용하세요:

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```

<a name="table-overview"></a>
#### 테이블 개요

특정 데이터베이스 테이블의 개요를 보려면 `db:table` Artisan 명령어를 사용하세요. 이 명령어는 테이블의 컬럼, 타입, 속성, 키, 인덱스에 관한 정보를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링 (Monitoring Your Databases)

`db:monitor` Artisan 명령어를 통해 데이터베이스가 지정한 개수 이상의 열려있는 연결(오픈 커넥션)을 관리할 때 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 디스패치하도록 할 수 있습니다.

시작하려면, 이 명령어를 [1분마다 실행](/docs/11.x/scheduling)하도록 스케줄링하세요. 명령어는 모니터링할 데이터베이스 연결 이름들과 허용할 최대 연결 수를 인수로 받습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

명령어 실행만으로는 최대 연결 임계치를 초과했을 때 알림이 보내지지 않습니다. 임계 초과 시 `DatabaseBusy` 이벤트가 발생하므로, 애플리케이션의 `AppServiceProvider`에서 이 이벤트를 리스닝해 개발팀이나 본인에게 알림을 보내도록 구현해야 합니다:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 애플리케이션 서비스 부트스트랩.
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