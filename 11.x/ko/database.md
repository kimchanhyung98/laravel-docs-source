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

대부분의 현대 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 다양한 지원 데이터베이스에 대해 원시 SQL, [플루언트 쿼리 빌더](/docs/{{version}}/queries), [Eloquent ORM](/docs/{{version}}/eloquent)를 사용하여 데이터베이스와 매우 쉽게 상호작용할 수 있도록 해줍니다. 현재 Laravel은 아래 다섯 가지 데이터베이스를 1차적으로 지원합니다:

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

추가적으로, MongoDB는 공식적으로 MongoDB에서 관리하는 `mongodb/laravel-mongodb` 패키지를 통해 지원됩니다. 더 자세한 정보는 [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 문서를 참고하세요.

<a name="configuration"></a>
### 설정

Laravel의 데이터베이스 서비스 설정은 애플리케이션의 `config/database.php` 설정 파일에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의하고, 기본으로 사용할 연결을 지정할 수 있습니다. 이 파일의 대부분 설정 옵션들은 애플리케이션의 환경 변수 값에 의해 제어됩니다. Laravel이 지원하는 대부분의 데이터베이스 시스템에 대한 예시가 이 파일에 제공됩니다.

기본적으로, Laravel의 샘플 [환경 설정](/docs/{{version}}/configuration#environment-configuration)은 [Laravel Sail](/docs/{{version}}/sail)과 함께 바로 사용할 수 있습니다. Sail은 로컬에서 Laravel 애플리케이션을 개발할 수 있는 Docker 환경입니다. 물론, 필요에 따라 로컬 데이터베이스에 맞게 데이터베이스 설정을 자유롭게 수정할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템상의 단일 파일에 저장됩니다. 터미널에서 `touch` 명령어를 사용해 새로운 SQLite 데이터베이스를 생성할 수 있습니다: `touch database/database.sqlite`. 데이터베이스가 생성되면, 환경 변수에 데이터베이스의 절대 경로를 `DB_DATABASE`로 지정하면 쉽게 설정할 수 있습니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

기본적으로, SQLite 연결에서는 외래 키 제약 조건이 활성화되어 있습니다. 이를 비활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `false`로 설정하세요:

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]  
> [Laravel 인스톨러](/docs/{{version}}/installation#creating-a-laravel-project)를 사용해 애플리케이션을 생성하고 데이터베이스로 SQLite를 선택하면, Laravel이 자동으로 `database/database.sqlite` 파일을 만들고 기본 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행합니다.

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면, `sqlsrv` 및 `pdo_sqlsrv` PHP 확장과 이들이 필요로 하는 Microsoft SQL ODBC 드라이버 등의 의존성을 설치해야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 이용한 설정

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 가지 설정 값을 사용하여 구성합니다. 각각의 설정 값은 별도의 환경 변수로 관리합니다. 즉, 프로덕션 서버에서 데이터베이스 연결 정보를 설정할 때 여러 환경 변수를 관리해야 합니다.

AWS나 Heroku와 같은 일부 관리형 데이터베이스 제공업체는 데이터베이스 연결에 필요한 모든 정보를 하나의 문자열인 데이터베이스 “URL”로 제공합니다. 데이터베이스 URL 예시는 다음과 같습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이 URL은 보통 다음과 같은 표준 스키마 형식을 따릅니다:

```html
driver://username:password@host:port/database?options
```

편의를 위해, Laravel은 여러 개의 설정 옵션 대신 이러한 URL도 지원합니다. 만약 `url`(또는 해당하는 `DB_URL` 환경 변수) 설정 옵션이 있으면, 이를 사용해 연결 및 자격 증명 정보를 추출합니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결

때때로 SELECT 구문에는 하나의 데이터베이스 연결을, INSERT, UPDATE, DELETE 구문에는 다른 연결을 사용하고 싶을 수 있습니다. Laravel을 사용하면, 원시 쿼리, 쿼리 빌더, Eloquent ORM 중 어떤 것을 사용하든 항상 적절한 연결이 자동으로 사용됩니다.

읽기/쓰기 연결을 어떻게 설정하는지 예제로 살펴보겠습니다:

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

`read`, `write`, `sticky` 세 가지 키가 설정 배열에 추가된 것을 볼 수 있습니다. `read`와 `write` 키는 각각 `host`라는 단일 키를 포함하는 배열 값입니다. 읽기/쓰기 연결의 나머지 데이터베이스 옵션은 기본 `mysql` 설정 배열에서 병합됩니다.

기본 `mysql` 배열의 값을 덮어쓰고 싶은 경우에만 `read`와 `write` 배열에 항목을 추가하면 됩니다. 이 예제에서 "read" 연결의 호스트로는 `192.168.1.1`이, "write" 연결의 호스트로는 `192.168.1.3`이 사용됩니다. 데이터베이스 자격 증명, 접두사, 문자 집합, 기타 모든 옵션은 두 연결에서 공유됩니다. `host` 배열에 여러 값이 있으면, 요청마다 임의로 하나의 데이터베이스 호스트가 선택됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 *선택적인* 값으로, 현재 요청 사이클 동안 데이터베이스에 기록된 레코드를 바로 읽을 수 있도록 해줍니다. 만약 `sticky` 옵션이 활성화되어 있고, 현재 요청에서 "쓰기" 작업이 수행되면 이후의 "읽기" 작업도 "쓰기" 연결을 사용하게 됩니다. 이로써 동일한 요청에서 기록된 데이터를 즉시 읽을 수 있습니다. 이 동작이 애플리케이션에 필요한지 여부는 직접 결정하면 됩니다.

<a name="running-queries"></a>
## SQL 쿼리 실행

데이터베이스 연결을 설정한 후에는, `DB` 파사드를 통해 쿼리를 실행할 수 있습니다. `DB` 파사드는 `select`, `update`, `insert`, `delete`, `statement`와 같은 다양한 쿼리 유형에 맞는 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### SELECT 쿼리 실행하기

기본적인 SELECT 쿼리를 실행하려면, `DB` 파사드의 `select` 메서드를 사용할 수 있습니다:

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

`select` 메서드의 첫 번째 인수는 SQL 쿼리, 두 번째 인수는 쿼리에 바인딩할 파라미터입니다. 일반적으로 where 절의 값이 들어갑니다. 파라미터 바인딩은 SQL 인젝션 공격을 방지해줍니다.

`select` 메서드는 항상 결과의 `array`를 반환합니다. 배열 내 각 결과는 데이터베이스 레코드를 나타내는 PHP `stdClass` 객체입니다:

    use Illuminate\Support\Facades\DB;

    $users = DB::select('select * from users');

    foreach ($users as $user) {
        echo $user->name;
    }

<a name="selecting-scalar-values"></a>
#### 스칼라 값 선택

데이터베이스 쿼리의 결과가 단일 스칼라 값일 때가 있습니다. 레코드 객체에서 꺼내지 않고 직접 값을 바로 가져오려면, `scalar` 메서드를 사용할 수 있습니다:

    $burgers = DB::scalar(
        "select count(case when food = 'burger' then 1 end) as burgers from menu"
    );

<a name="selecting-multiple-result-sets"></a>
#### 복수 결과 집합 선택

저장 프로시저를 호출해서 여러 결과 집합을 반환받을 경우, `selectResultSets` 메서드를 사용하여 모든 결과 집합을 가져올 수 있습니다:

    [$options, $notifications] = DB::selectResultSets(
        "CALL get_user_options_and_notifications(?)", $request->user()->id
    );

<a name="using-named-bindings"></a>
#### 네임드 바인딩 사용

파라미터 바인딩에 `?` 대신 이름 있는 바인딩을 사용할 수도 있습니다:

    $results = DB::select('select * from users where id = :id', ['id' => 1]);

<a name="running-an-insert-statement"></a>
#### Insert문 실행

`insert` 문을 실행하려면, `DB` 파사드의 `insert` 메서드를 사용합니다. `select`와 마찬가지로 첫 번째 인수는 SQL 쿼리, 두 번째 인수는 바인딩할 값입니다:

    use Illuminate\Support\Facades\DB;

    DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);

<a name="running-an-update-statement"></a>
#### Update문 실행

데이터베이스에 이미 존재하는 레코드를 수정하려면 `update` 메서드를 사용하세요. 이 메서드는 영향을 받은 행의 개수를 반환합니다:

    use Illuminate\Support\Facades\DB;

    $affected = DB::update(
        'update users set votes = 100 where name = ?',
        ['Anita']
    );

<a name="running-a-delete-statement"></a>
#### Delete문 실행

데이터베이스에서 레코드를 삭제하려면 `delete` 메서드를 사용하세요. `update`와 마찬가지로 영향을 받은 행의 수가 반환됩니다:

    use Illuminate\Support\Facades\DB;

    $deleted = DB::delete('delete from users');

<a name="running-a-general-statement"></a>
#### 일반 Statement 실행

일부 데이터베이스 명령문은 반환값이 없습니다. 이런 경우 `DB` 파사드의 `statement` 메서드를 사용하세요:

    DB::statement('drop table users');

<a name="running-an-unprepared-statement"></a>
#### Unprepared Statement 실행

때로는 값을 바인딩하지 않고 SQL을 실행하고 싶을 수 있습니다. 이런 경우 `DB` 파사드의 `unprepared` 메서드를 사용할 수 있습니다:

    DB::unprepared('update users set votes = 100 where name = "Dries"');

> [!WARNING]  
> Unprepared statement는 파라미터를 바인딩하지 않기 때문에 SQL 인젝션에 취약합니다. 사용자가 제공한 값을 절대 unprepared statement에 넣지 마세요.

<a name="implicit-commits-in-transactions"></a>
#### 암묵적 커밋

`DB` 파사드의 `statement` 및 `unprepared` 메서드를 트랜잭션 내에서 사용할 때는 [암묵적 커밋(implicit commit)](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 발생시키는 SQL문을 피해야 합니다. 이런 명령문은 데이터베이스 엔진이 트랜잭션 전체를 간접적으로 커밋하게 하여, Laravel이 트랜잭션 상태를 인지하지 못하게 만듭니다. 예를 들어 아래의 테이블 생성문이 해당됩니다:

    DB::unprepared('create table a (col varchar(1) null)');

암묵적 커밋을 유발하는 모든 명령문 목록은 MySQL 매뉴얼을 참조하세요. [관련 문서](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)

<a name="using-multiple-database-connections"></a>
### 다중 데이터베이스 연결 사용

애플리케이션의 `config/database.php`에서 여러 연결을 정의했다면, `DB` 파사드의 `connection` 메서드를 통해 각 연결에 접근할 수 있습니다. `connection` 메서드에 전달하는 연결명은 설정 파일에 나열된 이름이거나, 런타임에 `config` 헬퍼로 설정한 이름이어야 합니다:

    use Illuminate\Support\Facades\DB;

    $users = DB::connection('sqlite')->select(/* ... */);

각 연결의 원시 PDO 인스턴스는 `getPdo` 메서드로 가져올 수 있습니다:

    $pdo = DB::connection()->getPdo();

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 리스닝

애플리케이션이 실행하는 각 SQL 쿼리에 대해 실행되는 클로저를 지정하고 싶다면, `DB` 파사드의 `listen` 메서드를 사용할 수 있습니다. 이 방법은 쿼리 로깅이나 디버깅에 유용합니다. 쿼리 리스너 클로저는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 등록할 수 있습니다:

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

<a name="monitoring-cumulative-query-time"></a>
### 누적 쿼리 시간 모니터링

현대 웹 애플리케이션의 성능 병목 중 하나는 데이터베이스 쿼리에 소요되는 시간입니다. Laravel에서는 한 요청 내에서 쿼리 실행 시간이 너무 길어질 경우, 지정한 클로저나 콜백이 실행되도록 할 수 있습니다. 먼저, 임계값(밀리초 단위)과 클로저를 `whenQueryingForLongerThan` 메서드에 전달하세요. 이 메서드는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 호출할 수 있습니다:

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
                // 개발팀에 알림 전송 등...
            });
        }
    }

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션

`DB` 파사드의 `transaction` 메서드를 이용해 일련의 작업을 데이터베이스 트랜잭션 내에서 실행할 수 있습니다. 트랜잭션 클로저 내에서 예외가 발생하면 트랜잭션은 자동으로 롤백되고, 예외가 다시 던져집니다. 클로저가 성공적으로 실행되면 트랜잭션은 자동으로 커밋됩니다. 수동으로 롤백 또는 커밋할 필요가 없습니다:

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    });

<a name="handling-deadlocks"></a>
#### 교착상태(Deadlock) 처리

`transaction` 메서드는 선택적 두 번째 인수를 받으며, 이는 교착상태 발생 시 트랜잭션을 재시도할 횟수입니다. 재시도가 모두 실패하면 예외가 발생합니다:

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    }, 5);

<a name="manually-using-transactions"></a>
#### 트랜잭션 수동 제어

트랜잭션을 수동으로 시작하고, 롤백 및 커밋을 직접 제어하고 싶다면, `DB` 파사드의 `beginTransaction` 메서드를 사용하세요:

    use Illuminate\Support\Facades\DB;

    DB::beginTransaction();

`rollBack` 메서드로 트랜잭션을 롤백할 수 있습니다:

    DB::rollBack();

마지막으로, `commit` 메서드로 트랜잭션을 커밋할 수 있습니다:

    DB::commit();

> [!NOTE]  
> `DB` 파사드의 트랜잭션 메서드는 [쿼리 빌더](/docs/{{version}}/queries)와 [Eloquent ORM](/docs/{{version}}/eloquent) 모두에 적용됩니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 연결

데이터베이스의 CLI에 연결하려면 `db` 아티즌 명령어를 사용할 수 있습니다:

```shell
php artisan db
```

필요하다면, 기본 연결이 아닌 특정 데이터베이스 연결 이름을 지정할 수 있습니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 검사

`db:show` 및 `db:table` 아티즌 명령어를 사용해 데이터베이스 및 관련 테이블에 대한 유용한 정보를 얻을 수 있습니다. 데이터베이스의 전체적인 요약(용량, 타입, 열린 연결 수, 테이블 요약 등)을 보려면 다음 명령을 사용하세요:

```shell
php artisan db:show
```

`--database` 옵션으로 검사할 데이터베이스 연결 이름을 지정할 수 있습니다:

```shell
php artisan db:show --database=pgsql
```

명령의 출력에 테이블 행 개수와 데이터베이스 뷰 상세 정보를 포함하려면 각각 `--counts`와 `--views` 옵션을 사용할 수 있습니다. 대형 데이터베이스에서는 이 정보 조회가 느릴 수 있습니다:

```shell
php artisan db:show --counts --views
```

추가로, 다음과 같은 `Schema` 메서드를 사용하여 데이터베이스를 검사할 수 있습니다:

    use Illuminate\Support\Facades\Schema;

    $tables = Schema::getTables();
    $views = Schema::getViews();
    $columns = Schema::getColumns('users');
    $indexes = Schema::getIndexes('users');
    $foreignKeys = Schema::getForeignKeys('users');

기본 연결 이외의 데이터베이스 연결을 검사하려면, `connection` 메서드를 사용할 수 있습니다:

    $columns = Schema::connection('sqlite')->getColumns('users');

<a name="table-overview"></a>
#### 테이블 개요

데이터베이스의 특정 테이블에 대한 개요를 확인하려면, `db:table` 아티즌 명령어를 실행할 수 있습니다. 이 명령어는 테이블의 컬럼, 타입, 속성, 키, 인덱스 등 일반적인 정보를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링

`db:monitor` 아티즌 명령어를 사용하면, 데이터베이스 관리 중 열린 연결 수가 지정한 수보다 많을 때 `Illuminate\Database\Events\DatabaseBusy` 이벤트가 발생하도록 Laravel에 지시할 수 있습니다.

먼저, 이 명령어가 [매 분마다 실행되도록 스케줄링](/docs/{{version}}/scheduling)해야 합니다. 명령어는 모니터링할 데이터베이스 연결 이름과, 이벤트 발생 전 허용되는 최대 연결 수를 매개변수로 받습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

이 명령어를 스케줄링하는 것만으로는 연결 수 초과 시 알림이 자동 전송되지는 않습니다. 임계값을 초과하면 `DatabaseBusy` 이벤트가 발생하며, 애플리케이션의 `AppServiceProvider`에서 이 이벤트를 리스닝하여 본인 또는 개발팀에게 알림을 전송해야 합니다:

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
