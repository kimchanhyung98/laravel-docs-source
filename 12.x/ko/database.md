# 데이터베이스: 시작하기

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기 및 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행](#running-queries)
    - [다중 데이터베이스 연결 사용](#using-multiple-database-connections)
    - [쿼리 이벤트 리스닝](#listening-for-query-events)
    - [누적 쿼리 시간 모니터링](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 연결](#connecting-to-the-database-cli)
- [데이터베이스 검사](#inspecting-your-databases)
- [데이터베이스 모니터링](#monitoring-your-databases)

<a name="introduction"></a>
## 소개

거의 모든 현대 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 지원되는 여러 데이터베이스와의 상호작용을 매우 간단하게 만들어줍니다. 이는 원시 SQL, [유연한 쿼리 빌더](/docs/{{version}}/queries), [Eloquent ORM](/docs/{{version}}/eloquent)을 통해 가능합니다. 현재 Laravel은 5가지 데이터베이스에 대해 공식적으로 1차 지원을 제공합니다:

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

추가적으로, MongoDB는 공식적으로 MongoDB에서 관리하는 `mongodb/laravel-mongodb` 패키지를 통해 지원됩니다. 자세한 내용은 [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 문서를 참고하세요.

<a name="configuration"></a>
### 설정

Laravel의 데이터베이스 서비스 설정은 애플리케이션의 `config/database.php` 파일에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의할 수 있으며, 기본으로 사용할 연결도 지정할 수 있습니다. 이 파일의 대부분의 설정 옵션은 애플리케이션의 환경 변수 값에 의해 결정됩니다. Laravel에서 지원하는 대부분의 데이터베이스 시스템에 대한 예제가 이 파일에 포함되어 있습니다.

기본적으로, Laravel의 샘플 [환경 변수 설정](/docs/{{version}}/configuration#environment-configuration)은 [Laravel Sail](/docs/{{version}}/sail)과 함께 사용할 준비가 되어 있습니다. Laravel Sail은 로컬 개발을 위한 Docker 기반 환경입니다. 하지만 필요에 따라 로컬 데이터베이스 설정을 자유롭게 수정할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템 내의 하나의 파일로 구성됩니다. 터미널에서 `touch database/database.sqlite` 명령어를 사용해 새 SQLite 데이터베이스 파일을 생성할 수 있습니다. 데이터베이스가 생성된 후에는 환경 변수 파일에 데이터베이스의 절대 경로를 `DB_DATABASE`에 지정해 설정할 수 있습니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

기본적으로 SQLite 연결에서는 외래 키 제약 조건이 활성화되어 있습니다. 이를 비활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `false`로 설정하세요:

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]
> [Laravel 설치 도구](/docs/{{version}}/installation#creating-a-laravel-project)로 Laravel 애플리케이션을 만들 때 SQLite를 데이터베이스로 선택했다면, Laravel이 `database/database.sqlite` 파일을 자동으로 생성하고 기본 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행합니다.

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면 `sqlsrv` 및 `pdo_sqlsrv` PHP 확장 프로그램과 해당 확장이 필요로 하는 Microsoft SQL ODBC 드라이버와 같은 종속성이 설치되어 있어야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 이용한 설정

보통 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 설정 값을 사용해 구성됩니다. 각 설정 값은 별도의 환경 변수를 갖고 있으며, 이는 배포 서버에서 여러 환경 변수를 관리해야 함을 의미합니다.

AWS, Heroku와 같은 일부 관리형 데이터베이스 공급자는 모든 연결 정보를 하나의 문자열인 데이터베이스 "URL"로 제공합니다. 예시는 다음과 같습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이 URL은 일반적으로 표준 스키마 규칙을 따릅니다:

```html
driver://username:password@host:port/database?options
```

편의를 위해 Laravel은 여러 설정 값을 사용하는 대신 이러한 URL을 지원합니다. 만약 `url`(혹은 `DB_URL` 환경 변수) 설정 옵션이 존재한다면, 해당 값이 데이터베이스 연결 및 자격 증명 정보를 추출하는 데 사용됩니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결

때때로 SELECT 문에는 하나의 데이터베이스 연결, INSERT, UPDATE, DELETE 문에는 또 다른 연결을 사용하고 싶을 수 있습니다. Laravel은 이 작업을 매우 쉽게 해주며, 원시 쿼리, 쿼리 빌더, Eloquent ORM을 사용할 때에도 올바른 연결이 항상 사용됩니다.

읽기/쓰기 연결을 어떻게 구성하는지 보기 위해 예제를 살펴보겠습니다:

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

설정 배열에 `read`, `write`, `sticky` 세 개의 키가 추가된 것을 볼 수 있습니다. `read` 및 `write` 키는 단일 `host` 키를 포함한 배열 값을 가집니다. `read`와 `write` 연결에 대한 나머지 데이터베이스 옵션은 메인 `mysql` 설정 배열에서 병합됩니다.

기본 배열 값을 덮어쓰고 싶을 경우에만 `read`와 `write` 배열에 값을 추가하면 됩니다. 위 예제에서 `"read"` 연결에는 `192.168.1.1`, `"write"` 연결에는 `192.168.1.3`가 사용됩니다. 데이터베이스 자격 증명, 접두사, 문자셋 등 기타 옵션은 메인 `mysql` 배열에서 두 연결 모두에 공유됩니다. `host` 배열에 여러 값이 있다면, 요청마다 무작위로 데이터베이스 호스트가 선택됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 *선택사항*이며, 현재 요청에서 데이터베이스에 쓰기 작업이 일어난 경우 즉시 해당 레코드를 읽을 수 있도록 해줍니다. `sticky` 옵션이 활성화되고, 요청 주기 내에 "쓰기" 작업이 발생하면 이후 "읽기" 작업은 "쓰기" 연결을 사용합니다. 이는 요청 주기 동안 작성한 데이터를 즉시 DB에서 읽을 수 있게 보장합니다. 이 동작이 애플리케이션에 필요한지는 직접 판단해야 합니다.

<a name="running-queries"></a>
## SQL 쿼리 실행

데이터베이스 연결을 설정한 후에는 `DB` 파사드를 사용하여 쿼리를 실행할 수 있습니다. `DB` 파사드는 각 쿼리 유형별로 `select`, `update`, `insert`, `delete`, `statement` 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### Select 쿼리 실행

기본 SELECT 쿼리를 실행하려면 `DB` 파사드의 `select` 메서드를 사용합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록 표시
     */
    public function index(): View
    {
        $users = DB::select('select * from users where active = ?', [1]);

        return view('user.index', ['users' => $users]);
    }
}
```

`select` 메서드의 첫 번째 인자는 SQL 쿼리, 두 번째 인자는 바인딩할 매개변수입니다. 일반적으로 이것은 WHERE 절의 값입니다. 매개변수 바인딩은 SQL 인젝션으로부터 보호해줍니다.

`select` 메서드는 항상 결과의 `array`를 반환하며, 배열 내 개별 결과는 데이터베이스의 레코드를 나타내는 PHP `stdClass` 객체입니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="selecting-scalar-values"></a>
#### 스칼라 값 선택

쿼리 결과가 단일 스칼라 값이 될 때가 있습니다. 이 값을 레코드 객체에서 꺼낼 필요 없이, Laravel은 `scalar` 메서드를 사용해 바로 가져올 수 있습니다:

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
#### 다중 결과셋 선택

스토어드 프로시저를 호출해 여러 결과셋을 반환받고 싶다면, `selectResultSets` 메서드를 사용할 수 있습니다:

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
#### 명명된 바인딩 사용

매개변수 바인딩에 `?` 대신 명명된 매개변수를 사용할 수도 있습니다:

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
#### Insert 구문 실행

`insert` 구문을 실행하려면 `DB` 파사드의 `insert` 메서드를 사용합니다. 첫 번째 인자는 SQL, 두 번째 인자는 바인딩 값입니다:

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
#### Update 구문 실행

`update` 메서드는 데이터베이스의 기존 레코드를 수정하는 데 사용되며, 영향받은 행의 개수를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
#### Delete 구문 실행

`delete` 메서드는 레코드를 삭제하는 데 사용되며, 영향받은 행의 개수를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
#### 일반 구문 실행

값을 반환하지 않는 데이터베이스 명령어는 `DB` 파사드의 `statement` 메서드를 사용할 수 있습니다:

```php
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
#### Unprepared 구문 실행

값을 바인딩하지 않고 SQL을 직접 실행하려면 `DB` 파사드의 `unprepared` 메서드를 사용할 수 있습니다:

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]
> Unprepared 쿼리는 매개변수를 바인딩하지 않으므로 SQL 인젝션에 취약할 수 있습니다. 사용자 입력값을 직접 사용할 때는 절대 피하세요.

<a name="implicit-commits-in-transactions"></a>
#### 암시적 커밋

트랜잭션 내에서 `DB` 파사드의 `statement` 또는 `unprepared` 메서드를 사용할 때는 [암시적 커밋](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 발생시키는 SQL 구문을 주의해야 합니다. 이런 SQL은 트랜잭션 전체를 비의도적으로 커밋하여 Laravel이 트랜잭션 상태를 모르게 할 수 있습니다. 예시로 데이터베이스 테이블 생성이 있습니다:

```php
DB::unprepared('create table a (col varchar(1) null)');
```

암시적 커밋이 발생하는 모든 SQL 구문 목록은 MySQL 매뉴얼의 [관련 페이지](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)를 확인하세요.

<a name="using-multiple-database-connections"></a>
### 다중 데이터베이스 연결 사용

애플리케이션에서 `config/database.php` 파일에 여러 연결을 정의했다면, `DB` 파사드의 `connection` 메서드로 각각의 연결에 접근할 수 있습니다. 메서드에 넘기는 이름은 설정 파일 혹은 런타임에서 정의한 연결 이름이어야 합니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

연결 인스턴스의 `getPdo` 메서드를 통해 내부의 원시 PDO 인스턴스에도 접근할 수 있습니다:

```php
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 리스닝

애플리케이션이 실행하는 모든 SQL 쿼리에 대해 호출되는 클로저를 지정하고 싶다면, `DB` 파사드의 `listen` 메서드를 사용하세요. 이 기능은 쿼리 로깅이나 디버깅에 유용합니다. 쿼리 리스너 클로저는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에 등록할 수 있습니다:

```php
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
            // $query->toRawSql();
        });
    }
}
```

<a name="monitoring-cumulative-query-time"></a>
### 누적 쿼리 시간 모니터링

웹 애플리케이션의 주요 성능 병목 요인 중 하나는 데이터베이스 쿼리에 소요되는 시간입니다. Laravel에서는 한 요청 내에서 쿼리에 너무 많은 시간이 사용될 때 지정한 콜백이나 클로저를 호출할 수 있습니다. 시작하려면 임계값(밀리초)과 클로저를 `whenQueryingForLongerThan` 메서드에 전달하세요. 이 메서드는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 호출할 수 있습니다:

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
            // 개발팀 알림 등...
        });
    }
}
```

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션

`DB` 파사드의 `transaction` 메서드를 사용하면 여러 쿼리를 하나의 트랜잭션에서 실행할 수 있습니다. 트랜잭션 클로저 내부에서 예외가 발생하면 자동으로 롤백되고, 예외가 다시 던져집니다. 클로저가 정상적으로 실행되면 트랜잭션이 자동으로 커밋됩니다. 별도의 롤백이나 커밋을 신경 쓸 필요가 없습니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
#### 데드락 처리

`transaction` 메서드는 데드락이 발생했을 때 트랜잭션을 재시도할 횟수를 두 번째 인자로 받을 수 있습니다. 지정한 횟수만큼 시도하다가 실패하면 예외가 발생합니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, 5);
```

<a name="manually-using-transactions"></a>
#### 트랜잭션 수동 처리

트랜잭션을 직접 시작하고 커밋 및 롤백을 완전히 제어하고 싶다면 `DB` 파사드의 `beginTransaction` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

트랜잭션 롤백은 `rollBack` 메서드로 할 수 있습니다:

```php
DB::rollBack();
```

커밋은 `commit` 메서드로 수행합니다:

```php
DB::commit();
```

> [!NOTE]
> `DB` 파사드의 트랜잭션 관련 메서드는 [쿼리 빌더](/docs/{{version}}/queries)와 [Eloquent ORM](/docs/{{version}}/eloquent) 모두에 적용됩니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 연결

데이터베이스의 CLI에 접속하고 싶다면, `db` 아티즌 명령어를 사용할 수 있습니다:

```shell
php artisan db
```

필요하다면, 기본이 아닌 특정 데이터베이스 연결 이름을 명시하여 접속할 수 있습니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 검사

`db:show` 및 `db:table` 아티즌 명령어를 사용하면, 데이터베이스와 그에 속한 테이블에 대한 유용한 정보를 얻을 수 있습니다. 데이터베이스의 개요(크기, 타입, 열린 연결 수, 테이블 요약 등)를 확인하려면 `db:show` 명령어를 사용하세요:

```shell
php artisan db:show
```

어떤 데이터베이스 연결을 검사할지 `--database` 옵션으로 지정할 수 있습니다:

```shell
php artisan db:show --database=pgsql
```

명령어 출력에 테이블 행 수와 데이터베이스 뷰 정보를 포함하고 싶으면 `--counts`와 `--views` 옵션을 각각 추가하세요. 데이터가 많은 경우 행 수 및 뷰 정보를 조회하는 데 시간이 걸릴 수 있습니다:

```shell
php artisan db:show --counts --views
```

또한 다음과 같은 `Schema` 메서드를 사용해 데이터베이스를 코드상에서 직접 검사할 수 있습니다:

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

기본이 아닌 데이터베이스 연결을 검사하려면 `connection` 메서드를 사용하세요:

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```

<a name="table-overview"></a>
#### 테이블 개요

데이터베이스 내 개별 테이블의 개요를 확인하고 싶으면 `db:table` 아티즌 명령어를 실행하세요. 이 명령은 테이블의 컬럼, 유형, 속성, 키, 인덱스에 대한 정보를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링

`db:monitor` 아티즌 명령어를 사용하면, 데이터베이스에서 열린 연결 수가 지정한 임계값을 초과할 경우 Laravel이 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 발생시키도록 할 수 있습니다.

먼저, `db:monitor` 명령을 [매 분마다 실행](/docs/{{version}}/scheduling)되도록 스케줄링하세요. 이 명령은 모니터링할 데이터베이스 연결 이름과 이벤트 발생 전 허용할 최대 연결 수를 인자로 받습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

이 명령만 스케줄링한다고 즉시 알림이 전송되지는 않습니다. 지정한 임계값을 초과하는 데이터베이스 연결 수가 감지되면 `DatabaseBusy` 이벤트가 트리거됩니다. 개발팀 또는 자신에게 알림을 보내려면 애플리케이션의 `AppServiceProvider`에서 이 이벤트를 리스닝해야 합니다:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 애플리케이션 서비스 부트스트랩
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
