# 데이터베이스: 시작하기 (Database: Getting Started)

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기 및 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행하기](#running-queries)
    - [다중 데이터베이스 연결 사용하기](#using-multiple-database-connections)
    - [쿼리 이벤트 청취하기](#listening-for-query-events)
    - [누적 쿼리 시간 모니터링](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 연결하기](#connecting-to-the-database-cli)
- [데이터베이스 점검하기](#inspecting-your-databases)
- [데이터베이스 모니터링](#monitoring-your-databases)

<a name="introduction"></a>
## 소개 (Introduction)

거의 모든 모던 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 다양한 지원 데이터베이스에서 원시 SQL, [유창한 쿼리 빌더](/docs/10.x/queries), 그리고 [Eloquent ORM](/docs/10.x/eloquent)을 사용해 데이터베이스와 매우 간단하게 연동할 수 있도록 도와줍니다. 현재 Laravel은 다섯 개의 데이터베이스를 공식 지원합니다:

<div class="content-list" markdown="1">

- MariaDB 10.10+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 11.0+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.8.8+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 데이터베이스 서비스 설정은 애플리케이션의 `config/database.php` 설정 파일에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의할 수 있으며 기본으로 사용할 연결도 지정할 수 있습니다. 대부분의 설정 옵션은 애플리케이션의 환경 변수 값을 기반으로 동작합니다. Laravel에서 지원하는 대부분의 데이터베이스 시스템용 설정 예제가 이 파일 내에 포함되어 있습니다.

기본적으로 Laravel의 샘플 [환경 설정](/docs/10.x/configuration#environment-configuration)은 로컬 개발을 위한 Docker 구성인 [Laravel Sail](/docs/10.x/sail)과 바로 사용할 수 있도록 준비되어 있습니다. 하지만 필요에 따라 로컬 데이터베이스 설정을 자유롭게 변경할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템 내 단일 파일로 존재합니다. 터미널에서 `touch database/database.sqlite` 명령어로 새 SQLite 데이터베이스 파일을 생성할 수 있습니다. 데이터베이스가 생성된 후, 환경 변수 `DB_DATABASE`에 데이터베이스의 절대 경로를 지정하여 데이터베이스를 연결할 수 있습니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

SQLite 연결에 대해 외래 키 제약 조건을 활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `true`로 설정해야 합니다:

```ini
DB_FOREIGN_KEYS=true
```

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면 `sqlsrv`와 `pdo_sqlsrv` PHP 확장 모듈과, Microsoft SQL ODBC 드라이버와 같은 필요한 종속성이 설치되어 있어야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 이용한 설정

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 설정 값으로 구성되며 각 값마다 대응하는 환경 변수가 존재합니다. 따라서 배포 서버에서 데이터베이스 연결 정보를 설정할 때 여러 환경 변수를 관리해야 합니다.

AWS, Heroku와 같은 일부 관리형 데이터베이스 제공자는 데이터베이스 연결 정보를 하나의 문자열로 요약한 "URL" 형식을 제공합니다. 예시 URL은 다음과 같습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이 URL은 일반적으로 다음과 같은 표준 스키마를 따릅니다:

```html
driver://username:password@host:port/database?options
```

Laravel은 이러한 URL 형식을 여러 개의 설정 옵션을 사용하는 대신 편리하게 지원합니다. `url` 설정값(또는 해당하는 `DATABASE_URL` 환경 변수)이 있다면 이 값을 사용해 데이터베이스 연결 및 인증 정보를 추출합니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결 (Read and Write Connections)

때때로 SELECT 문을 위한 데이터베이스 연결과 INSERT, UPDATE, DELETE 문을 위한 연결을 분리해서 사용하고 싶을 수 있습니다. Laravel은 이를 쉽게 처리하며, 원시 쿼리, 쿼리 빌더, Eloquent ORM 어디서든 올바른 연결을 자동으로 사용합니다.

읽기/쓰기 연결 설정 예시는 다음과 같습니다:

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

`read`, `write`, `sticky` 세 가지 키가 추가된 것을 볼 수 있습니다. `read`와 `write`는 `host` 키를 가진 배열 값을 가집니다. 나머지 데이터베이스 옵션은 `mysql` 메인 설정 배열에서 병합됩니다.

`read`와 `write` 배열에 값을 명시하는 것은 메인 `mysql` 배열에서 값을 덮어쓰고자 할 때만 필요합니다. 이 예시에서 `192.168.1.1`은 "읽기" 연결용 호스트로, `192.168.1.3`은 "쓰기" 연결용 호스트로 사용됩니다. 데이터베이스 인증 정보, 접두사, 문자셋 등의 나머지 옵션은 두 연결에 공통으로 적용됩니다. `host` 설정 배열에 여러 값이 있다면, 요청 시마다 무작위로 호스트가 선택됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 현재 요청 주기 내에서 데이터베이스에 "쓰기" 작업이 수행된 경우, 이후의 "읽기" 작업도 즉시 동일한 "쓰기" 연결을 사용하도록 하는 *선택적* 설정입니다. 이렇게 하면 해당 요청 중에 쓴 데이터를 바로 읽을 수 있어 일관성을 보장할 수 있습니다. 애플리케이션 상황에 따라 이 동작이 필요한지 여부를 결정하세요.

<a name="running-queries"></a>
## SQL 쿼리 실행하기 (Running SQL Queries)

데이터베이스 연결을 설정한 후에는 `DB` 파사드를 사용해 쿼리를 실행할 수 있습니다. `DB` 파사드는 `select`, `update`, `insert`, `delete`, `statement` 등 각 타입별 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### Select 쿼리 실행하기

기본적인 SELECT 쿼리는 `DB` 파사드의 `select` 메서드를 사용해 실행합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션 사용자의 목록을 보여줍니다.
     */
    public function index(): View
    {
        $users = DB::select('select * from users where active = ?', [1]);

        return view('user.index', ['users' => $users]);
    }
}
```

`select` 메서드의 첫 번째 인수는 SQL 쿼리이고, 두 번째 인수는 쿼리에 바인딩할 파라미터 값입니다. 보통 `where` 절의 조건 값입니다. 파라미터 바인딩은 SQL 인젝션 공격을 예방해 줍니다.

`select` 메서드는 항상 결과를 담은 `array`를 반환하며, 배열 안의 각 결과는 데이터베이스 레코드를 표현하는 PHP `stdClass` 객체입니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="selecting-scalar-values"></a>
#### 스칼라 값 선택하기

쿼리 결과가 단일 스칼라 값일 때, 결과 객체에서 스칼라 값을 추출할 필요 없이 `scalar` 메서드를 사용해 바로 해당 값을 얻을 수 있습니다:

```
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
#### 다중 결과 집합 선택하기

스토어드 프로시저가 여러 결과 집합을 반환하는 경우, `selectResultSets` 메서드로 반환된 모든 결과 집합을 받을 수 있습니다:

```
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
#### 명명된 바인딩 사용하기

`?` 대신 이름이 붙은 바인딩을 사용할 수도 있습니다:

```
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
#### Insert 문 실행하기

`insert` 문을 실행하려면 `DB` 파사드의 `insert` 메서드를 사용합니다. `select`와 마찬가지로 첫 번째 인수는 SQL, 두 번째 인수는 바인딩 값입니다:

```
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
#### Update 문 실행하기

기존 레코드를 갱신하려면 `update` 메서드를 사용합니다. 이 메서드는 영향받은 행(row)의 개수를 반환합니다:

```
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
#### Delete 문 실행하기

레코드를 삭제할 때는 `delete` 메서드를 사용합니다. `update`와 마찬가지로 영향받은 행 수가 반환됩니다:

```
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
#### 일반 SQL 실행하기

결과값을 반환하지 않는 SQL 문 실행 시에는 `statement` 메서드를 사용합니다:

```
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
#### 바인딩 없는 SQL 실행하기

값 바인딩 없이 SQL 문을 실행하려면 `DB` 파사드의 `unprepared` 메서드를 사용할 수 있습니다:

```
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]  
> 바인딩을 하지 않는 unprepared 문은 SQL 인젝션 공격에 취약할 수 있으니, 사용자 입력값이 포함되지 않도록 주의하세요.

<a name="implicit-commits-in-transactions"></a>
#### 암묵적 커밋 (Implicit Commits)

트랜잭션 내에서 `DB` 파사드의 `statement` 또는 `unprepared` 메서드를 사용할 때, 암묵적 커밋을 유발하는 SQL 문에 주의해야 합니다. 암묵적 커밋은 데이터베이스 엔진이 트랜잭션의 커밋을 간접적으로 실행하여 Laravel이 트랜잭션 상태를 인지하지 못하게 만듭니다. 예를 들어 테이블 생성문이 이에 해당합니다:

```
DB::unprepared('create table a (col varchar(1) null)');
```

암묵적 커밋을 일으키는 모든 명령어 목록은 MySQL 매뉴얼에서 확인할 수 있습니다: [암묵적 커밋 문서](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)。

<a name="using-multiple-database-connections"></a>
### 다중 데이터베이스 연결 사용하기 (Using Multiple Database Connections)

`config/database.php`에 여러 연결을 정의한 경우, `DB` 파사드의 `connection` 메서드를 사용해 각 연결에 접근할 수 있습니다. `connection` 메서드 인수는 설정 파일에 있는 연결 이름이어야 하며, 런타임에 `config` 헬퍼로도 구성할 수 있습니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

또한 연결 인스턴스의 `getPdo` 메서드를 사용해 PDO 인스턴스에 직접 접근할 수 있습니다:

```
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 청취하기 (Listening for Query Events)

애플리케이션에서 실행되는 모든 SQL 쿼리에 대해 콜백을 지정해 로그를 남기거나 디버깅할 수 있습니다. `DB` 파사드의 `listen` 메서드를 사용하면 됩니다. 보통 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

```
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
```

<a name="monitoring-cumulative-query-time"></a>
### 누적 쿼리 시간 모니터링 (Monitoring Cumulative Query Time)

데이터베이스 쿼리 시간이 웹 애플리케이션 성능 병목이 될 수 있습니다. Laravel은 하나의 요청 동안 쿼리 실행 시간이 일정 기준을 초과하면 지정한 콜백을 실행할 수 있게 지원합니다. `whenQueryingForLongerThan` 메서드에 밀리초 단위의 임계값과 콜백을 넘기면 됩니다. 보통 서비스 프로바이더의 `boot` 메서드에서 사용합니다:

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
            // 개발팀에게 알림 전송...
        });
    }
}
```

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션 (Database Transactions)

`DB` 파사드의 `transaction` 메서드를 사용하면 트랜잭션 내에서 여러 작업을 실행할 수 있습니다. 트랜잭션 클로저 내에서 예외가 발생하면 자동으로 롤백되고 예외가 다시 던져집니다. 정상적으로 실행되면 자동으로 커밋됩니다. 수동으로 롤백하거나 커밋할 필요가 없습니다:

```
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
#### 데드락 처리

`transaction` 메서드는 선택적 두 번째 인수로 데드락 발생 시 재시도 횟수를 지정할 수 있습니다. 재시도 횟수를 초과하면 예외가 던져집니다:

```
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, 5);
```

<a name="manually-using-transactions"></a>
#### 수동으로 트랜잭션 사용하기

트랜잭션을 직접 시작하고 롤백과 커밋을 완전히 제어하려면 `beginTransaction` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

롤백은 `rollBack` 메서드로 수행할 수 있습니다:

```
DB::rollBack();
```

커밋은 `commit` 메서드를 사용합니다:

```
DB::commit();
```

> [!NOTE]  
> `DB` 파사드의 트랜잭션 메서드는 [쿼리 빌더](/docs/10.x/queries)와 [Eloquent ORM](/docs/10.x/eloquent) 양쪽의 트랜잭션을 제어합니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 연결하기 (Connecting to the Database CLI)

데이터베이스 CLI에 연결하려면 `db` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan db
```

기본 연결이 아닌 다른 연결을 지정하려면 연결 이름을 추가로 넘기면 됩니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 점검하기 (Inspecting Your Databases)

`db:show`와 `db:table` Artisan 명령어로 데이터베이스와 테이블 정보를 확인할 수 있습니다. `db:show`는 데이터베이스 크기, 타입, 열린 연결 수, 테이블 요약 정보를 보여줍니다:

```shell
php artisan db:show
```

점검 대상 데이터베이스 연결을 `--database` 옵션으로 지정할 수 있습니다:

```shell
php artisan db:show --database=pgsql
```

출력에 테이블 행(row) 수와 뷰(view) 정보도 포함하려면 각각 `--counts`와 `--views` 옵션을 사용하세요. 대용량 데이터베이스에서는 이 옵션이 실행 속도를 느리게 할 수 있습니다:

```shell
php artisan db:show --counts --views
```

<a name="table-overview"></a>
#### 테이블 개요

개별 테이블의 개요를 보고 싶다면 `db:table` Artisan 명령어를 실행하세요. 이 명령은 컬럼, 타입, 속성, 키(key), 인덱스 정보를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링 (Monitoring Your Databases)

`db:monitor` Artisan 명령어를 사용하면 지정한 데이터베이스 연결에서 열린 연결이 일정 개수를 초과할 때 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 발생시킬 수 있습니다.

먼저 이 명령어를 [분 단위 예약 실행](/docs/10.x/scheduling) 하도록 스케줄 설정하세요. 명령어에는 모니터링할 데이터베이스 연결명과 최대 허용 연결 수를 인수로 지정할 수 있습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

이 명령어를 예약 실행하는 것만으로 알림이 자동 발생하는 것은 아닙니다. 열린 연결 수가 임계값을 넘는 데이터베이스가 발견되면 `DatabaseBusy` 이벤트가 디스패치됩니다. 해당 이벤트를 애플리케이션의 `EventServiceProvider`에서 청취해 개발팀에게 알림을 보내도록 구현해야 합니다:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 애플리케이션 이벤트를 등록합니다.
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