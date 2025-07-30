# 데이터베이스: 시작하기 (Database: Getting Started)

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기 및 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행하기](#running-queries)
    - [여러 데이터베이스 연결 사용하기](#using-multiple-database-connections)
    - [쿼리 이벤트 수신하기](#listening-for-query-events)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 연결하기](#connecting-to-the-database-cli)

<a name="introduction"></a>
## 소개 (Introduction)

거의 모든 현대 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 다양한 지원 데이터베이스에서 원시 SQL, [유창한 쿼리 빌더](/docs/{{version}}/queries), 그리고 [Eloquent ORM](/docs/{{version}}/eloquent)를 사용해 데이터베이스와의 상호작용을 매우 간단하게 만듭니다. 현재 Laravel은 다음 5가지 데이터베이스에 대해 공식 지원을 제공합니다:

<div class="content-list" markdown="1">

- MariaDB 10.2+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 9.6+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.8.8+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 데이터베이스 서비스 설정은 애플리케이션의 `config/database.php` 설정 파일에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의하고, 기본으로 사용할 연결을 지정할 수 있습니다. 대부분의 설정 옵션은 애플리케이션 환경 변수 값에 의해 결정됩니다. Laravel이 지원하는 대부분의 데이터베이스 시스템에 대한 예제도 이 파일에 포함되어 있습니다.

기본적으로 Laravel의 샘플 [환경 설정](/docs/{{version}}/configuration#environment-configuration)은 [Laravel Sail](/docs/{{version}}/sail)과 함께 바로 사용할 수 있도록 준비되어 있습니다. Laravel Sail은 로컬 머신에서 Laravel 애플리케이션 개발을 위한 Docker 설정입니다. 하지만 필요에 따라 로컬 데이터베이스에 맞게 데이터베이스 설정을 자유롭게 변경할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템 내 단일 파일 안에 저장됩니다. 터미널에서 `touch` 명령어로 새 SQLite 데이터베이스를 생성할 수 있습니다: `touch database/database.sqlite`. 데이터베이스가 생성된 후에는 절대 경로를 `DB_DATABASE` 환경 변수에 설정하여 환경 변수를 쉽게 구성할 수 있습니다:

```
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

SQLite 연결에서 외래 키 제약조건을 활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `true`로 설정하세요:

```
DB_FOREIGN_KEYS=true
```

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면 `sqlsrv` 및 `pdo_sqlsrv` PHP 확장과 이들이 필요로 하는 의존성(예: Microsoft SQL ODBC 드라이버)이 설치되어 있어야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 사용한 설정

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 설정 값으로 구성됩니다. 이 각각은 대응하는 환경 변수로 관리됩니다. 즉, 프로덕션 서버에서 데이터베이스 연결 정보를 설정할 때 여러 환경 변수를 관리해야 합니다.

AWS, Heroku와 같은 일부 관리형 데이터베이스 제공자는 모든 연결 정보를 한 문자열에 담아 제공하는 단일 데이터베이스 "URL"을 제공합니다. 이런 데이터베이스 URL 예시는 다음과 같습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

일반적으로 이 URL들은 아래와 같은 표준 스키마를 따릅니다:

```html
driver://username:password@host:port/database?options
```

Laravel은 이러한 URL을 여러 설정 값을 따로 구성하는 대신 편리하게 사용할 수 있도록 지원합니다. `url` (또는 대응하는 `DATABASE_URL` 환경 변수) 옵션이 있는 경우, 이 값을 통해 데이터베이스 연결 정보와 인증 정보를 추출합니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결 (Read & Write Connections)

SELECT 문에는 하나의 데이터베이스 연결을 사용하고, INSERT, UPDATE, DELETE 문에는 다른 연결을 사용하고 싶을 수 있습니다. Laravel은 이 작업을 매우 쉽게 처리하며, 원시 쿼리, 쿼리 빌더, Eloquent ORM 어느 쪽을 사용하든 올바른 연결이 자동으로 사용됩니다.

읽기 / 쓰기 연결을 설정하는 방법을 다음 예제를 통해 살펴보겠습니다:

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

`read`, `write`, `sticky` 세 가지 키가 설정 배열에 추가되어 있습니다. `read`와 `write` 키의 배열 값은 각각 `host` 키만 포함합니다. 나머지 `read`, `write` 연결에 필요한 데이터베이스 옵션은 메인 `mysql` 설정에서 병합됩니다.

`read`와 `write` 배열에 값을 넣는 것은 메인 `mysql` 배열의 값을 덮어쓰고자 할 때만 필요합니다. 이 경우, `"read"` 연결은 `192.168.1.1`과 `192.168.1.2`를 호스트 목록으로, `"write"` 연결은 `196.168.1.3` 하나의 호스트를 가집니다. 데이터베이스 자격증명, 접두어(prefix), 문자셋 등 다른 설정들은 두 연결 간에 공유됩니다. 만약 `host` 배열에 여러 값이 있을 경우, 요청할 때마다 데이터베이스 호스트가 임의로 선택됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 *선택적* 값으로, 현재 요청 사이클 동안 데이터베이스에 쓰기 작업이 이루어진 후, 즉시 그 기록을 읽을 수 있도록 합니다. `sticky`가 활성화되어 있고 현재 요청 사이클에 "쓰기" 작업이 수행된 경우, 그 이후의 "읽기" 작업은 모두 "쓰기" 연결을 사용합니다. 이렇게 하면 요청 사이클 중 작성된 데이터를 같은 요청 내에서 즉시 읽을 수 있습니다. 애플리케이션의 요구에 따라 이 동작 여부를 결정하면 됩니다.

<a name="running-queries"></a>
## SQL 쿼리 실행하기 (Running SQL Queries)

데이터베이스 연결을 설정한 후, `DB` 파사드를 통해 쿼리를 실행할 수 있습니다. `DB` 파사드는 `select`, `update`, `insert`, `delete`, `statement` 각 쿼리 유형에 맞는 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### SELECT 쿼리 실행하기

기본적인 SELECT 쿼리를 실행하려면 `DB` 파사드의 `select` 메서드를 사용하면 됩니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class UserController extends Controller
{
    /**
     * 애플리케이션 모든 사용자의 목록을 보여줍니다.
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

첫 번째 인수는 SQL 쿼리 문자열이고, 두 번째 인수는 쿼리에 바인딩할 인수(종종 `where` 절 값)입니다. 파라미터 바인딩은 SQL 인젝션 방어에 도움을 줍니다.

`select` 메서드는 항상 결과를 담은 `array`를 반환합니다. 배열 내 각 항목은 데이터베이스 레코드를 나타내는 PHP `stdClass` 객체입니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="using-named-bindings"></a>
#### 명명된 바인딩 사용하기

`?` 대신 이름이 지정된 바인딩을 사용할 수도 있습니다:

```
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
#### INSERT 문 실행하기

`insert` 문 실행을 위해 `DB` 파사드의 `insert` 메서드를 사용합니다. `select` 메서드와 마찬가지로 첫 번째 인수는 SQL 쿼리, 두 번째 인수는 바인딩 값입니다:

```
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
#### UPDATE 문 실행하기

`update` 메서드는 데이터베이스의 기존 기록을 수정할 때 사용하며, 영향을 받은 행 수를 반환합니다:

```
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
#### DELETE 문 실행하기

`delete` 메서드는 데이터베이스에서 기록을 삭제할 때 사용하며, 영향을 받은 행 수를 반환합니다:

```
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
#### 일반 문장 실행하기

결과 값을 반환하지 않는 데이터베이스 문장은 `DB` 파사드의 `statement` 메서드를 사용해 실행할 수 있습니다:

```
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
#### 준비되지 않은 문장 실행하기

때로는 바인딩 없이 SQL 문장을 직접 실행하고 싶을 수 있습니다. 이 경우 `DB` 파사드의 `unprepared` 메서드를 사용할 수 있습니다:

```
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!NOTE]
> 준비되지 않은 문장은 파라미터를 바인딩하지 않으므로 SQL 인젝션 공격에 취약할 수 있습니다. 사용자 입력값이 포함되지 않도록 반드시 주의하세요.

<a name="implicit-commits-in-transactions"></a>
#### 암묵적 커밋 (Implicit Commits)

트랜잭션 내부에서 `DB` 파사드의 `statement` 및 `unprepared` 메서드를 사용할 때, [암묵적 커밋](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 발생시키는 문장을 주의해야 합니다. 암묵적 커밋이 발생하면 데이터베이스 엔진이 트랜잭션을 간접적으로 커밋하지만, Laravel은 이를 인지하지 못합니다. 예를 들어 테이블 생성 문이 이에 해당합니다:

```
DB::unprepared('create table a (col varchar(1) null)');
```

암묵적 커밋을 유발하는 모든 명령어 목록은 MySQL 메뉴얼의 [관련 페이지](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)를 참고하세요.

<a name="using-multiple-database-connections"></a>
### 여러 데이터베이스 연결 사용하기 (Using Multiple Database Connections)

애플리케이션에서 `config/database.php` 파일에 다중 연결을 정의했다면, `DB` 파사드의 `connection` 메서드를 통해 각각의 연결을 사용할 수 있습니다. 메서드에 전달하는 연결 이름은 `config/database.php`에 등록된 이름과 일치해야 하거나, 실행 시 `config` 헬퍼로 동적으로 설정할 수도 있습니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(...);
```

연결 인스턴스에서 `getPdo` 메서드를 사용하면 기본 PDO 객체를 직접 얻을 수도 있습니다:

```
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 수신하기 (Listening For Query Events)

애플리케이션에서 실행되는 각 SQL 쿼리에 대해 호출되는 클로저를 지정하고 싶다면, `DB` 파사드의 `listen` 메서드를 사용할 수 있습니다. 이 방법은 쿼리 로그 기록이나 디버깅에 유용합니다. 쿼리 리스너 클로저는 서비스 프로바이더의 `boot` 메서드에 등록하는 것이 일반적입니다:

```
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
```

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션 (Database Transactions)

`DB` 파사드의 `transaction` 메서드를 사용해 데이터베이스 트랜잭션 내에서 여러 작업을 실행할 수 있습니다. 트랜잭션 클로저 내부에서 예외가 발생하면 자동으로 롤백되고 예외가 다시 던져집니다. 클로저가 성공적으로 실행되면 자동으로 커밋됩니다. `transaction` 메서드 사용 시 수동 롤백 및 커밋을 신경 쓸 필요가 없습니다:

```
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
#### 데드락 처리하기

`transaction` 메서드는 선택적 두 번째 인수를 받아, 데드락 발생 시 트랜잭션 재시도 횟수를 정의합니다. 재시도 횟수를 모두 소진하면 예외가 발생합니다:

```
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, 5);
```

<a name="manually-using-transactions"></a>
#### 트랜잭션 수동 사용하기

트랜잭션을 수동으로 시작하고 롤백 및 커밋을 직접 제어하고 싶다면 `DB` 파사드의 메서드를 사용할 수 있습니다:

트랜잭션 시작:

```
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

롤백:

```
DB::rollBack();
```

커밋:

```
DB::commit();
```

> [!TIP]
> `DB` 파사드의 트랜잭션 메서드는 [쿼리 빌더](/docs/{{version}}/queries)와 [Eloquent ORM](/docs/{{version}}/eloquent) 모두에 적용됩니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 연결하기 (Connecting To The Database CLI)

데이터베이스 CLI에 연결하려면 `db` Artisan 명령어를 사용할 수 있습니다:

```
php artisan db
```

필요시 기본 연결이 아닌 특정 연결 이름을 지정해서 접속할 수도 있습니다:

```
php artisan db mysql
```
