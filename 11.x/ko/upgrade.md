# 업그레이드 가이드 (Upgrade Guide)

- [10.x에서 11.0으로 업그레이드](#upgrade-11.0)

<a name="high-impact-changes"></a>
## 주요 변경사항 (High Impact Changes)

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [애플리케이션 구조](#application-structure)
- [부동 소수점 타입 변경](#floating-point-types)
- [컬럼 수정 방식 변경](#modifying-columns)
- [SQLite 최소 버전 요구사항](#sqlite-minimum-version)
- [Sanctum 업데이트](#updating-sanctum)

</div>

<a name="medium-impact-changes"></a>
## 중간 영향 변경사항 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [Carbon 3 지원](#carbon-3)
- [비밀번호 재해싱](#password-rehashing)
- [초 단위 레이트 제한](#per-second-rate-limiting)
- [Spatie Once 패키지](#spatie-once-package)

</div>

<a name="low-impact-changes"></a>
## 영향이 적은 변경사항 (Low Impact Changes)

<div class="content-list" markdown="1">

- [Doctrine DBAL 제거](#doctrine-dbal-removal)
- [Eloquent 모델 `casts` 메서드](#eloquent-model-casts-method)
- [공간 타입 지원](#spatial-types)
- [`Enumerable` 계약 인터페이스](#the-enumerable-contract)
- [`UserProvider` 계약 인터페이스](#the-user-provider-contract)
- [`Authenticatable` 계약 인터페이스](#the-authenticatable-contract)

</div>

<a name="upgrade-11.0"></a>
## 10.x에서 11.0으로 업그레이드하기 (Upgrading To 11.0 From 10.x)

<a name="estimated-upgrade-time-??-minutes"></a>
#### 예상 소요 시간: 15분

> [!NOTE]  
> 가능한 모든 주요 변경사항을 문서로 기록하려 노력했습니다. 프레임워크 내에서 다루기 어려운 일부 변화들은 실제 애플리케이션에 영향을 미치지 않을 수 있습니다. 시간을 절약하려면 [Laravel Shift](https://laravelshift.com/)를 사용해 자동으로 애플리케이션 업그레이드를 진행할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트 (Updating Dependencies)

**영향도: 높음**

#### PHP 8.2.0 이상 필요

Laravel은 이제 PHP 8.2.0 이상을 필요로 합니다.

#### curl 7.34.0 이상 필요

Laravel HTTP 클라이언트는 curl 7.34.0 이상이 필요합니다.

#### Composer 의존성

`composer.json` 파일에서 다음 의존성 버전을 업데이트해야 합니다:

<div class="content-list" markdown="1">

- `laravel/framework` 를 `^11.0` 으로
- `nunomaduro/collision` 을 `^8.1` 로
- `laravel/breeze` 를 `^2.0` 으로 (설치한 경우)
- `laravel/cashier` 를 `^15.0` 으로 (설치한 경우)
- `laravel/dusk` 를 `^8.0` 으로 (설치한 경우)
- `laravel/jetstream` 을 `^5.0` 으로 (설치한 경우)
- `laravel/octane` 을 `^2.3` 으로 (설치한 경우)
- `laravel/passport` 를 `^12.0` 으로 (설치한 경우)
- `laravel/sanctum` 을 `^4.0` 으로 (설치한 경우)
- `laravel/scout` 를 `^10.0` 으로 (설치한 경우)
- `laravel/spark-stripe` 를 `^5.0` 으로 (설치한 경우)
- `laravel/telescope` 를 `^5.0` 으로 (설치한 경우)
- `livewire/livewire` 를 `^3.4` 로 (설치한 경우)
- `inertiajs/inertia-laravel` 을 `^1.0` 으로 (설치한 경우)

</div>

Laravel Cashier Stripe, Passport, Sanctum, Spark Stripe, 또는 Telescope를 사용하는 경우, 이제 이들의 마이그레이션이 자동으로 로드되지 않으므로, 아래 명령어로 각 패키지의 마이그레이션을 애플리케이션에 게시해야 합니다:

```bash
php artisan vendor:publish --tag=cashier-migrations
php artisan vendor:publish --tag=passport-migrations
php artisan vendor:publish --tag=sanctum-migrations
php artisan vendor:publish --tag=spark-migrations
php artisan vendor:publish --tag=telescope-migrations
```

각 패키지별 업그레이드 가이드도 반드시 검토하세요:

- [Laravel Cashier Stripe](#cashier-stripe)
- [Laravel Passport](#passport)
- [Laravel Sanctum](#sanctum)
- [Laravel Spark Stripe](#spark-stripe)
- [Laravel Telescope](#telescope)

직접 Laravel 설치 관리자를 설치했다면, Composer로 다음과 같이 업그레이드 해야 합니다:

```bash
composer global require laravel/installer:^5.6
```

마지막으로, 이전에 `doctrine/dbal` 패키지를 추가했다면 Laravel에서 더 이상 의존하지 않으니 `composer.json`에서 제거할 수 있습니다.

<a name="application-structure"></a>
### 애플리케이션 구조 (Application Structure)

Laravel 11은 기본적으로 서비스 프로바이더, 미들웨어, 구성 파일 등이 감소된 새로운 애플리케이션 구조를 도입했습니다.

하지만 Laravel 10 애플리케이션을 11로 업그레이드할 때는 기존 구조를 변경하지 않는 것을 권장합니다. Laravel 11은 Laravel 10 구조도 지원하도록 신중히 설계되었습니다.

<a name="authentication"></a>
### 인증 (Authentication)

<a name="password-rehashing"></a>
#### 비밀번호 재해싱 (Password Rehashing)

**영향도: 낮음**

Laravel 11은 인증 과정에서 사용자의 비밀번호 해시 알고리즘의 작업 강도(work factor)가 변경된 경우 자동으로 비밀번호를 재해싱합니다.

보통은 애플리케이션에 문제를 일으키지 않지만, 만약 당신의 `User` 모델 내 비밀번호 필드명이 `password` 가 아니라면 `authPasswordName` 속성으로 필드명을 지정해야 합니다:

```
protected $authPasswordName = 'custom_password_field';
```

또는, `config/hashing.php` 설정 파일에서 `rehash_on_login` 옵션을 `false`로 설정하여 재해싱 기능을 비활성화할 수 있습니다:

```
'rehash_on_login' => false,
```

<a name="the-user-provider-contract"></a>
#### `UserProvider` 계약 인터페이스

**영향도: 낮음**

`Illuminate\Contracts\Auth\UserProvider` 계약에 `rehashPasswordIfRequired` 메서드가 새롭게 추가되었습니다.

이 메서드는 해싱 알고리즘 작업 강도가 변경된 경우 비밀번호를 재해싱하여 저장하는 역할을 합니다.

해당 인터페이스를 구현하는 클래스가 있다면 아래 시그니처를 참고해 새 메서드를 추가해야 합니다:

```php
public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
```

참고용 기본 구현체는 `Illuminate\Auth\EloquentUserProvider` 클래스에 있습니다.

<a name="the-authenticatable-contract"></a>
#### `Authenticatable` 계약 인터페이스

**영향도: 낮음**

`Illuminate\Contracts\Auth\Authenticatable` 계약에 `getAuthPasswordName` 메서드가 새로 추가되었습니다.

이 메서드는 인증 대상의 비밀번호 컬럼명을 반환합니다.

해당 인터페이스를 구현하는 경우, 아래와 같이 메서드를 추가하세요:

```php
public function getAuthPasswordName()
{
    return 'password';
}
```

Laravel 기본 제공 `User` 모델은 `Illuminate\Auth\Authenticatable` 트레이트에 포함되어 있어 자동으로 이 메서드를 가집니다.

<a name="the-authentication-exception-class"></a>
#### `AuthenticationException` 클래스

**영향도: 매우 낮음**

`Illuminate\Auth\AuthenticationException` 클래스의 `redirectTo` 메서드는 이제 첫 번째 인자로 `Illuminate\Http\Request` 객체를 필요로 합니다.

이 예외를 수동으로 잡아서 `redirectTo` 메서드를 호출하는 경우, 코드를 아래처럼 수정해야 합니다:

```php
if ($e instanceof AuthenticationException) {
    $path = $e->redirectTo($request);
}
```

<a name="email-verification-notification-on-registration"></a>
#### 회원가입 시 이메일 인증 알림 (Email Verification Notification on Registration)

**영향도: 매우 낮음**

`Registered` 이벤트에 대해 `SendEmailVerificationNotification` 리스너가 애플리케이션의 `EventServiceProvider`에 등록되어 있지 않으면, Laravel은 자동으로 등록합니다.

원하지 않을 경우 `EventServiceProvider`에 아래 빈 메서드를 정의하여 자동 등록을 막을 수 있습니다:

```php
protected function configureEmailVerification()
{
    // 의도적으로 비워둠
}
```

<a name="cache"></a>
### 캐시 (Cache)

<a name="cache-key-prefixes"></a>
#### 캐시 키 접두사 (Cache Key Prefixes)

**영향도: 매우 낮음**

이전에는 DynamoDB, Memcached, Redis 캐시 저장소에서 캐시 키 접두사를 정의하면 Laravel이 접두사 뒤에 `:` 문자를 자동 추가했습니다.

Laravel 11부터는 접두사에 `:`가 자동으로 붙지 않습니다.

이전 동작을 유지하려면, 접두사에 수동으로 `:`를 추가하세요.

<a name="collections"></a>
### 컬렉션 (Collections)

<a name="the-enumerable-contract"></a>
#### `Enumerable` 계약 인터페이스

**영향도: 낮음**

`Illuminate\Support\Enumerable` 계약의 `dump` 메서드가 가변 인자 `...$args`를 받도록 변경되었습니다.

이 인터페이스를 구현하고 있다면 시그니처를 아래처럼 변경하세요:

```php
public function dump(...$args);
```

<a name="database"></a>
### 데이터베이스 (Database)

<a name="sqlite-minimum-version"></a>
#### SQLite 3.26.0 이상 필요

**영향도: 높음**

SQLite 데이터베이스를 사용하는 애플리케이션은 최소 SQLite 3.26.0 이상을 요구합니다.

<a name="eloquent-model-casts-method"></a>
#### Eloquent 모델 `casts` 메서드

**영향도: 낮음**

기본 Eloquent 모델 클래스에 이제 `casts` 메서드가 정의되어 있습니다.

따라서, 기존 애플리케이션 모델에서 `casts` 관계를 정의하는 경우가 있다면 이 메서드와 충돌할 수 있습니다.

<a name="modifying-columns"></a>
#### 컬럼 수정 (Modifying Columns)

**영향도: 높음**

컬럼을 수정할 때 변경 후에도 유지하려는 모든 컬럼 속성들을 명시적으로 포함해야 합니다.

예전에 마이그레이션에서 정의된 속성이 마이그레이션에서 누락되면, 해당 속성은 삭제됩니다.

예를 들어, 아래와 같이 컬럼을 생성했다고 가정합시다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('The vote count');
});
```

이후 컬럼을 nullable로 변경하려면 Laravel 10과는 다르게 다음과 같이 원래 속성을 모두 명시해야 합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')
        ->unsigned()
        ->default(1)
        ->comment('The vote count')
        ->nullable()
        ->change();
});
```

`change` 메서드는 인덱스 변경을 처리하지 않으므로, 인덱스 추가 또는 삭제는 명시적으로 다음과 같이 해야 합니다:

```php
// 인덱스 추가
$table->bigIncrements('id')->primary()->change();

// 인덱스 제거
$table->char('postal_code', 10)->unique(false)->change();
```

만약 모든 기존 "change" 마이그레이션을 수정하기 귀찮다면, [마이그레이션 스쿼싱](/docs/11.x/migrations#squashing-migrations)을 고려하세요:

```bash
php artisan schema:dump
```

스쿼싱 후에는 데이터베이스가 애플리케이션의 스키마 파일을 기반으로 먼저 마이그레이션 됩니다.

<a name="floating-point-types"></a>
#### 부동 소수점 타입 (Floating-Point Types)

**영향도: 높음**

`double`과 `float` 타입의 마이그레이션 컬럼이 모든 데이터베이스에서 일관되도록 재작성되었습니다.

- `double` 타입은 SQL 표준에 맞게 총 자리수 및 소수점 자리수 인자를 제거하고 `DOUBLE` 컬럼을 생성합니다:

```php
$table->double('amount');
```

- `float` 타입은 총 자리수 또는 소수점 자리수가 사라지고 대신 저장 정밀도 옵션 `$precision` 을 받아, 4바이트 단정밀도 또는 8바이트 배정밀도로 설정할 수 있습니다:

```php
$table->float('amount', precision: 53);
```

`unsignedDecimal`, `unsignedDouble`, `unsignedFloat` 메서드는 제거되었습니다. MySQL이 이들의 unsigned 수정자를 더 이상 지원하지 않고, 타 DB 시스템에서는 표준화하지 않았기 때문입니다.

만약 unsigned 속성을 계속 사용하고 싶다면, 아래처럼 `unsigned()` 메서드를 체인해 사용하세요:

```php
$table->decimal('amount', total: 8, places: 2)->unsigned();
$table->double('amount')->unsigned();
$table->float('amount', precision: 53)->unsigned();
```

<a name="dedicated-mariadb-driver"></a>
#### MariaDB 전용 드라이버

**영향도: 매우 낮음**

MariaDB 연결 시 항상 MySQL 드라이버를 사용하던 대신, Laravel 11부터는 MariaDB 전용 드라이버가 추가되었습니다.

MariaDB 데이터베이스에 연결할 경우 `driver` 설정을 다음과 같이 변경하면 MariaDB 전용 기능을 활용할 수 있습니다:

```
'driver' => 'mariadb',
'url' => env('DB_URL'),
'host' => env('DB_HOST', '127.0.0.1'),
'port' => env('DB_PORT', '3306'),
// ...
```

현재 MariaDB 드라이버는 MySQL 드라이버와 같으나, `uuid` 스키마 빌더 메서드는 네이티브 UUID 컬럼을 생성합니다(`char(36)`이 아님).

기존 마이그레이션에서 `uuid` 메서드를 사용한다면, 호환성 문제 방지를 위해 이를 `char`로 변경하세요:

```php
Schema::table('users', function (Blueprint $table) {
    $table->char('uuid', 36);
    // ...
});
```

<a name="spatial-types"></a>
#### 공간 타입 (Spatial Types)

**영향도: 낮음**

데이터베이스 마이그레이션의 공간 데이터 타입들이 모든 DB에서 일관된 형태로 재작성되었습니다.

`point`, `lineString`, `polygon`, `geometryCollection`, `multiPoint`, `multiLineString`, `multiPolygon`, `multiPolygonZ` 메서드 대신 다음을 사용하세요:

```php
$table->geometry('shapes');
$table->geography('coordinates');
```

MySQL, MariaDB, PostgreSQL에서 컬럼에 저장된 데이터 타입이나 공간 참조 시스템 식별자를 명시하려면 `subtype`과 `srid` 매개변수를 전달할 수 있습니다:

```php
$table->geometry('dimension', subtype: 'polygon', srid: 0);
$table->geography('latitude', subtype: 'point', srid: 4326);
```

PostgreSQL 문법에서 `isGeometry` 및 `projection` 컬럼 수정자는 제거되었습니다.

<a name="doctrine-dbal-removal"></a>
#### Doctrine DBAL 제거

**영향도: 낮음**

다음 Doctrine DBAL 관련 클래스와 메서드가 제거되었습니다. Laravel은 이제 이 패키지에 의존하지 않습니다. 다양한 컬럼 타입 생성 및 변경에 있어 사용자 정의 Doctrine 타입 등록이 더 이상 필요하지 않습니다:

<div class="content-list" markdown="1">

- `Illuminate\Database\Schema\Builder::$alwaysUsesNativeSchemaOperationsIfPossible` 클래스 프로퍼티
- `Illuminate\Database\Schema\Builder::useNativeSchemaOperationsIfPossible()` 메서드
- `Illuminate\Database\Connection::usingNativeSchemaOperations()` 메서드
- `Illuminate\Database\Connection::isDoctrineAvailable()` 메서드
- `Illuminate\Database\Connection::getDoctrineConnection()` 메서드
- `Illuminate\Database\Connection::getDoctrineSchemaManager()` 메서드
- `Illuminate\Database\Connection::getDoctrineColumn()` 메서드
- `Illuminate\Database\Connection::registerDoctrineType()` 메서드
- `Illuminate\Database\DatabaseManager::registerDoctrineType()` 메서드
- `Illuminate\Database\PDO` 디렉토리
- `Illuminate\Database\DBAL\TimestampType` 클래스
- `Illuminate\Database\Schema\Grammars\ChangeColumn` 클래스
- `Illuminate\Database\Schema\Grammars\RenameColumn` 클래스
- `Illuminate\Database\Schema\Grammars\Grammar::getDoctrineTableDiff()` 메서드

</div>

또한, `database` 설정 파일 내 `dbal.types`로 사용자 정의 Doctrine 타입을 등록할 필요가 없습니다.

이전에 Doctrine DBAL을 사용해 DB 스키마를 조사했다면, 이제 Laravel 자체의 네이티브 스키마 메서드(`Schema::getTables()`, `Schema::getColumns()`, `Schema::getIndexes()`, `Schema::getForeignKeys()` 등)를 대신 사용하세요.

<a name="deprecated-schema-methods"></a>
#### 더 이상 지원하지 않는 스키마 메서드

**영향도: 매우 낮음**

더 이상 사용하지 않는 Doctrine 기반 메서드인 `Schema::getAllTables()`, `Schema::getAllViews()`, `Schema::getAllTypes()`는 제거되었습니다.

대신 새로운 Laravel 네이티브 메서드인 `Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()`를 사용하세요.

PostgreSQL이나 SQL Server에서는 3단 구성의 참조(`database.schema.table`)를 메서드 인자로 넘길 수 없으므로, 대신 `connection()`으로 데이터베이스를 명시하세요:

```php
Schema::connection('database')->hasTable('schema.table');
```

<a name="get-column-types"></a>
#### 스키마 빌더의 `getColumnType()` 메서드

**영향도: 매우 낮음**

`Schema::getColumnType()` 메서드는 이제 Doctrine DBAL 동등 타입이 아닌, 주어진 컬럼의 실제 데이터베이스 타입을 항상 반환합니다.

<a name="database-connection-interface"></a>
#### 데이터베이스 연결 인터페이스

**영향도: 매우 낮음**

`Illuminate\Database\ConnectionInterface` 인터페이스에 새 `scalar` 메서드가 추가되었습니다.

해당 인터페이스를 직접 구현했다면 다음 시그니처를 추가하세요:

```php
public function scalar($query, $bindings = [], $useReadPdo = true);
```

<a name="dates"></a>
### 날짜 및 시간 (Dates)

<a name="carbon-3"></a>
#### Carbon 3

**영향도: 중간**

Laravel 11은 Carbon 2와 Carbon 3 모두를 지원합니다.

Carbon은 Laravel뿐 아니라 다양한 패키지에서 사용하는 날짜 조작 라이브러리입니다.

Carbon 3로 업그레이드하면 `diffIn*` 메서드들이 부동소수점 숫자를 반환하고, 시간의 방향성을 나타내기 위해 음수를 반환할 수 있습니다. 이는 Carbon 2와의 큰 차이점입니다.

변경 사항과 대응 방법에 대해서는 Carbon의 [변경 로그](https://github.com/briannesbitt/Carbon/releases/tag/3.0.0)와 [공식 문서](https://carbon.nesbot.com/docs/#api-carbon-3)를 참고하세요.

<a name="mail"></a>
### 메일 (Mail)

<a name="the-mailer-contract"></a>
#### `Mailer` 계약 인터페이스

**영향도: 매우 낮음**

`Illuminate\Contracts\Mail\Mailer` 계약에 `sendNow` 메서드가 추가되었습니다.

수동으로 구현하는 경우 아래 메서드를 포함하세요:

```php
public function sendNow($mailable, array $data = [], $callback = null);
```

<a name="packages"></a>
### 패키지 (Packages)

<a name="publishing-service-providers"></a>
#### 서비스 프로바이더 게시 방식 변경

**영향도: 매우 낮음**

자체 Laravel 패키지를 작성해 서비스 프로바이더를 `app/Providers`에 수동으로 게시하고, `config/app.php` 파일을 수동으로 변경해서 프로바이더를 등록하는 경우, 이제는 `ServiceProvider::addProviderToBootstrapFile` 메서드를 사용하세요.

이 메서드는 Laravel 11 신규 애플리케이션에서 `config/app.php`에 `providers` 배열이 없기 때문에 자동으로 `bootstrap/providers.php` 파일에 프로바이더를 추가합니다:

```php
use Illuminate\Support\ServiceProvider;

ServiceProvider::addProviderToBootstrapFile(Provider::class);
```

<a name="queues"></a>
### 큐 (Queues)

<a name="the-batch-repository-interface"></a>
#### `BatchRepository` 인터페이스

**영향도: 매우 낮음**

`Illuminate\Bus\BatchRepository` 인터페이스에 `rollBack` 메서드가 추가되었습니다.

직접 구현하는 경우 아래 메서드를 추가해야 합니다:

```php
public function rollBack();
```

<a name="synchronous-jobs-in-database-transactions"></a>
#### 데이터베이스 트랜잭션 내 동기 작업 처리

**영향도: 매우 낮음**

이전에는 동기 큐 작업 (`sync` 드라이버 사용) 이 즉시 실행되었고, `after_commit` 옵션 설정이나 작업의 `afterCommit` 호출 여부와 무관했습니다.

Laravel 11부터는 동기 큐 작업 또한 큐 연결의 "after commit" 설정을 준수합니다.

<a name="rate-limiting"></a>
### 레이트 제한 (Rate Limiting)

<a name="per-second-rate-limiting"></a>
#### 초 단위 레이트 제한 (Per-Second Rate Limiting)

**영향도: 중간**

Laravel 11은 분 단위 대신 초 단위 레이트 제한을 지원합니다. 이와 관련된 여러 변경사항에 주의해야 합니다.

- `GlobalLimit` 클래스 생성자는 분 대신 초 단위를 받습니다. (이 클래스는 주로 내부용입니다)

```php
new GlobalLimit($attempts, 2 * 60);
```

- `Limit` 클래스 생성자도 분 대신 초 단위를 받습니다.

```php
new Limit($key, $attempts, 2 * 60);
```

- `Limit` 클래스의 `decayMinutes` 프로퍼티는 `decaySeconds`로 이름과 값이 변경되었습니다.

- `Illuminate\Queue\Middleware\ThrottlesExceptions` 와 `ThrottlesExceptionsWithRedis` 클래스 생성자도 초 단위를 받도록 변경되었습니다.

```php
new ThrottlesExceptions($attempts, 2 * 60);
new ThrottlesExceptionsWithRedis($attempts, 2 * 60);
```

<a name="cashier-stripe"></a>
### Cashier Stripe

<a name="updating-cashier-stripe"></a>
#### Cashier Stripe 업데이트

**영향도: 높음**

Laravel 11은 Cashier Stripe 14.x를 지원하지 않습니다. 따라서 `composer.json`에서 Laravel Cashier Stripe 의존성을 `^15.0`으로 업그레이드해야 합니다.

Cashier Stripe 15.0은 자신의 마이그레이션 디렉터리에서 마이그레이션을 자동으로 로드하지 않습니다. 따라서 다음 명령어로 마이그레이션을 애플리케이션에 게시해야 합니다:

```shell
php artisan vendor:publish --tag=cashier-migrations
```

추가 브레이킹 변경사항은 [Cashier Stripe 업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/15.x/UPGRADE.md)를 참고하세요.

<a name="spark-stripe"></a>
### Spark (Stripe)

<a name="updating-spark-stripe"></a>
#### Spark Stripe 업데이트

**영향도: 높음**

Laravel 11은 Spark Stripe 4.x를 지원하지 않습니다. `composer.json`에서 Laravel Spark Stripe 의존성을 `^5.0`으로 업그레이드해야 합니다.

Spark Stripe 5.0은 마이그레이션 디렉터리에서 마이그레이션을 자동 로드하지 않습니다. 따라서 다음 명령어로 마이그레이션을 게시하세요:

```shell
php artisan vendor:publish --tag=spark-migrations
```

자세한 변경사항은 [Spark Stripe 업그레이드 가이드](https://spark.laravel.com/docs/spark-stripe/upgrade.html)를 참고하세요.

<a name="passport"></a>
### Passport

<a name="updating-telescope"></a>
#### Passport 업데이트

**영향도: 높음**

Laravel 11은 Passport 11.x를 지원하지 않습니다. `composer.json`에서 Laravel Passport 의존성을 `^12.0`으로 업그레이드해야 합니다.

Passport 12.0은 마이그레이션 디렉터리에서 자동 마이그레이션을 하지 않으므로, 다음 명령어로 마이그레이션을 게시하세요:

```shell
php artisan vendor:publish --tag=passport-migrations
```

또한, 패스워드 그랜트 타입은 기본적으로 비활성화되어 있습니다. 활성화하려면 애플리케이션 `AppServiceProvider`의 `boot` 메서드 내에서 다음을 호출하세요:

```
public function boot(): void
{
    Passport::enablePasswordGrant();
}
```

<a name="sanctum"></a>
### Sanctum

<a name="updating-sanctum"></a>
#### Sanctum 업데이트

**영향도: 높음**

Laravel 11은 Sanctum 3.x를 지원하지 않습니다. `composer.json`에서 Laravel Sanctum 의존성을 `^4.0`으로 업그레이드해야 합니다.

Sanctum 4.0은 마이그레이션 디렉터리에서 마이그레이션을 자동으로 로드하지 않으므로 다음 명령어로 게시해야 합니다:

```shell
php artisan vendor:publish --tag=sanctum-migrations
```

이후 `config/sanctum.php` 설정 파일 내 미들웨어 참조들을 아래와 같이 수정하세요:

```
'middleware' => [
    'authenticate_session' => Laravel\Sanctum\Http\Middleware\AuthenticateSession::class,
    'encrypt_cookies' => Illuminate\Cookie\Middleware\EncryptCookies::class,
    'validate_csrf_token' => Illuminate\Foundation\Http\Middleware\ValidateCsrfToken::class,
],
```

<a name="telescope"></a>
### Telescope

<a name="updating-telescope"></a>
#### Telescope 업데이트

**영향도: 높음**

Laravel 11은 Telescope 4.x를 지원하지 않습니다. `composer.json` 파일에서 Telescope 의존성을 `^5.0`으로 업그레이드하세요.

Telescope 5.0은 자체 마이그레이션 디렉터리의 마이그레이션을 자동 로드하지 않으므로, 다음 명령어로 게시해야 합니다:

```shell
php artisan vendor:publish --tag=telescope-migrations
```

<a name="spatie-once-package"></a>
### Spatie Once 패키지

**영향도: 중간**

Laravel 11은 클로저를 한 번만 실행하도록 보장하는 [`once` 함수](/docs/11.x/helpers#method-once)를 기본 제공합니다.

따라서 `spatie/once` 패키지를 의존하고 있다면 충돌을 막기 위해 `composer.json`에서 제거하는 것이 좋습니다.

<a name="miscellaneous"></a>
### 기타 사항 (Miscellaneous)

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경 내역도 확인하는 것을 권장합니다.

많은 변경 사항은 애플리케이션에 반드시 필요한 것은 아니지만, 구성 파일이나 주석 변경사항을 포함한 일부 변경을 동기화하는 것이 좋을 수 있습니다.

[GitHub 비교 도구](https://github.com/laravel/laravel/compare/10.x...11.x)로 변경 사항을 쉽게 확인하고 필요한 업데이트만 선택할 수 있습니다.