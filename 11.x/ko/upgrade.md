# 업그레이드 가이드

- [10.x에서 11.0으로 업그레이드](#upgrade-11.0)

<a name="high-impact-changes"></a>
## 영향도가 높은 변경사항

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [애플리케이션 구조](#application-structure)
- [부동 소수점 타입](#floating-point-types)
- [컬럼 수정](#modifying-columns)
- [SQLite 최소 버전](#sqlite-minimum-version)
- [Sanctum 업데이트](#updating-sanctum)

</div>

<a name="medium-impact-changes"></a>
## 영향도가 중간인 변경사항

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [비밀번호 리해싱](#password-rehashing)
- [초 단위 Rate Limiting](#per-second-rate-limiting)
- [Spatie Once 패키지](#spatie-once-package)

</div>

<a name="low-impact-changes"></a>
## 영향도가 낮은 변경사항

<div class="content-list" markdown="1">

- [Doctrine DBAL 제거](#doctrine-dbal-removal)
- [Eloquent 모델 `casts` 메서드](#eloquent-model-casts-method)
- [공간 타입(Spatial Types)](#spatial-types)
- [`Enumerable` 계약](#the-enumerable-contract)
- [`UserProvider` 계약](#the-user-provider-contract)
- [`Authenticatable` 계약](#the-authenticatable-contract)

</div>

<a name="upgrade-11.0"></a>
## 10.x에서 11.0으로 업그레이드

<a name="estimated-upgrade-time-??-minutes"></a>
#### 예상 소요 시간: 15분

> [!NOTE]  
> 가능한 모든 변경사항을 문서화하려고 노력하고 있습니다. 일부 변경사항은 프레임워크의 잘 알려지지 않은 부분에 해당할 수 있으므로, 실제로는 일부만이 귀하의 애플리케이션에 영향을 줄 수 있습니다. 시간을 절약하고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용하여 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트

**영향 가능성: 높음**

#### PHP 8.2.0 필수

Laravel은 이제 PHP 8.2.0 이상이 필요합니다.

#### curl 7.34.0 필수

Laravel의 HTTP 클라이언트는 curl 7.34.0 이상이 필요합니다.

#### Composer 의존성

애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다:

<div class="content-list" markdown="1">

- `laravel/framework` → `^11.0`
- `nunomaduro/collision` → `^8.1`
- `laravel/breeze` → `^2.0` (설치된 경우)
- `laravel/cashier` → `^15.0` (설치된 경우)
- `laravel/dusk` → `^8.0` (설치된 경우)
- `laravel/jetstream` → `^5.0` (설치된 경우)
- `laravel/octane` → `^2.3` (설치된 경우)
- `laravel/passport` → `^12.0` (설치된 경우)
- `laravel/sanctum` → `^4.0` (설치된 경우)
- `laravel/scout` → `^10.0` (설치된 경우)
- `laravel/spark-stripe` → `^5.0` (설치된 경우)
- `laravel/telescope` → `^5.0` (설치된 경우)
- `livewire/livewire` → `^3.4` (설치된 경우)
- `inertiajs/inertia-laravel` → `^1.0` (설치된 경우)

</div>

애플리케이션이 Laravel Cashier Stripe, Passport, Sanctum, Spark Stripe 또는 Telescope를 사용하는 경우, 해당 패키지의 마이그레이션을 애플리케이션에 퍼블리시해야 합니다. Cashier Stripe, Passport, Sanctum, Spark Stripe, Telescope는 **이제 더 이상 자체 migration 디렉터리에서 자동으로 마이그레이션을 로드하지 않습니다**. 따라서 다음 명령어를 실행하여 마이그레이션을 직접 퍼블리시해야 합니다:

```bash
php artisan vendor:publish --tag=cashier-migrations
php artisan vendor:publish --tag=passport-migrations
php artisan vendor:publish --tag=sanctum-migrations
php artisan vendor:publish --tag=spark-migrations
php artisan vendor:publish --tag=telescope-migrations
```

또한, 각 패키지의 업그레이드 가이드를 확인하여 추가적인 주의사항이 있는지 반드시 확인해야 합니다.

- [Laravel Cashier Stripe](#cashier-stripe)
- [Laravel Passport](#passport)
- [Laravel Sanctum](#sanctum)
- [Laravel Spark Stripe](#spark-stripe)
- [Laravel Telescope](#telescope)

Laravel 설치 프로그램을 수동으로 설치하였다면, Composer를 통해 설치 프로그램도 업데이트해야 합니다:

```bash
composer global require laravel/installer:^5.6
```

마지막으로, 이전에 `doctrine/dbal` Composer 의존성을 추가했다면, 이제 Laravel이 더 이상 이 패키지에 의존하지 않으므로 삭제해도 됩니다.

<a name="application-structure"></a>
### 애플리케이션 구조

Laravel 11은 더 적은 기본 파일을 가지는 신규 애플리케이션 기본 구조를 도입했습니다. 새 Laravel 애플리케이션에는 더 적은 서비스 프로바이더, 미들웨어, 설정 파일이 포함되어 있습니다.

하지만 **Laravel 10에서 11로 업그레이드하는 애플리케이션의 구조까지 새 버전 구조로 변경하는 것은 권장하지 않습니다.** Laravel 11은 Laravel 10의 애플리케이션 구조도 완벽하게 지원하도록 신중하게 설계되었습니다.

<a name="authentication"></a>
### 인증(Authentication)

<a name="password-rehashing"></a>
#### 비밀번호 리해싱

**영향 가능성: 낮음**

Laravel 11은 해싱 알고리즘의 "work factor"가 비밀번호가 마지막으로 해시되었을 때보다 증가한 경우, 인증 과정에서 자동으로 비밀번호를 다시 해시합니다.

일반적으로는 애플리케이션에 영향을 미치지 않지만, 만약 `User` 모델의 비밀번호 필드가 `password`가 아니라면, 모델의 `authPasswordName` 속성을 통해 필드의 이름을 지정해야 합니다:

    protected $authPasswordName = 'custom_password_field';

또는, 비밀번호 리해싱을 비활성화하려면 애플리케이션의 `config/hashing.php` 파일에서 다음을 추가할 수 있습니다:

    'rehash_on_login' => false,

<a name="the-user-provider-contract"></a>
#### `UserProvider` 계약

**영향 가능성: 낮음**

`Illuminate\Contracts\Auth\UserProvider` 계약에 새로운 `rehashPasswordIfRequired` 메서드가 추가되었습니다. 이 메서드는 해싱 알고리즘의 work factor가 변경된 경우 비밀번호를 리해시 및 저장하는 역할을 합니다.

이 계약을 구현하는 클래스가 있다면, 새 메서드를 추가해야 합니다. 참고 구현체는 `Illuminate\Auth\EloquentUserProvider` 클래스에서 찾을 수 있습니다:

```php
public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
```

<a name="the-authenticatable-contract"></a>
#### `Authenticatable` 계약

**영향 가능성: 낮음**

`Illuminate\Contracts\Auth\Authenticatable` 계약에 새로운 `getAuthPasswordName` 메서드가 추가되었습니다. 이 메서드는 인증 대상 엔티티의 비밀번호 컬럼 이름을 반환합니다.

이 계약을 구현하는 클래스가 있다면 해당 메서드를 추가해야 합니다:

```php
public function getAuthPasswordName()
{
    return 'password';
}
```

Laravel에서 기본적으로 제공하는 `User` 모델은 `Illuminate\Auth\Authenticatable` 트레이트를 통해 이미 이 기능을 제공합니다.

<a name="the-authentication-exception-class"></a>
#### `AuthenticationException` 클래스

**영향 가능성: 매우 낮음**

`Illuminate\Auth\AuthenticationException`의 `redirectTo` 메서드는 이제 첫 번째 인자로 `Illuminate\Http\Request` 인스턴스를 필요로 합니다. 만약 직접 이 예외를 잡아서 `redirectTo`를 호출한다면 코드를 다음과 같이 수정하세요:

```php
if ($e instanceof AuthenticationException) {
    $path = $e->redirectTo($request);
}
```

<a name="email-verification-notification-on-registration"></a>
#### 회원가입 시 이메일 인증 알림

**영향 가능성: 매우 낮음**

`SendEmailVerificationNotification` 리스너가 기존에 `EventServiceProvider`에서 등록되어 있지 않다면 `Registered` 이벤트에 자동으로 등록됩니다. 만약 해당 리스너가 자동 등록되길 원하지 않는다면, `EventServiceProvider`에 빈 `configureEmailVerification` 메서드를 추가하세요:

```php
protected function configureEmailVerification()
{
    // ...
}
```

<a name="cache"></a>
### 캐시(Cache)

<a name="cache-key-prefixes"></a>
#### 캐시 키 접두어

**영향 가능성: 매우 낮음**

기존에는 DynamoDB, Memcached, Redis 캐시 스토어에 접두어(:)가 추가됐지만, Laravel 11에서는 더 이상 자동으로 추가하지 않습니다. 예전과 동일하게 사용하려면 접두어에 직접 `:`를 추가하면 됩니다.

<a name="collections"></a>
### 컬렉션(Collections)

<a name="the-enumerable-contract"></a>
#### `Enumerable` 계약

**영향 가능성: 낮음**

`Illuminate\Support\Enumerable` 인터페이스의 `dump` 메서드는 이제 가변 인자(`...$args`)를 받도록 변경되었습니다. 이 인터페이스를 구현하고 있다면 구현체도 수정해야 합니다:

```php
public function dump(...$args);
```

<a name="database"></a>
### 데이터베이스

<a name="sqlite-minimum-version"></a>
#### SQLite 3.26.0 이상

**영향 가능성: 높음**

애플리케이션이 SQLite를 사용하는 경우, 이제 SQLite 3.26.0 이상이 필요합니다.

<a name="eloquent-model-casts-method"></a>
#### Eloquent 모델 `casts` 메서드

**영향 가능성: 낮음**

Eloquent 기본 모델 클래스에 이제 속성 캐스트를 위한 `casts` 메서드가 정의됩니다. 만약 애플리케이션의 어떤 모델이 `casts`라는 관계를 별도로 가지고 있다면, 이제 충돌이 발생할 수 있습니다.

<a name="modifying-columns"></a>
#### 컬럼 수정

**영향 가능성: 높음**

컬럼을 수정할 때, 이제 변경 후에도 유지하고자 하는 모든 수정자를 명시적으로 지정해야 합니다. 누락되는 속성은 삭제됩니다. 예를 들어, `unsigned`, `default`, `comment` 속성을 유지하려면, 변경할 때마다 모두 명시적으로 호출해야 합니다.

예시: 기존에 `votes` 컬럼을 다음과 같이 생성했다면,

```php
Schema::create('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('The vote count');
});
```

나중에 해당 컬럼에 nullable 속성을 추가하려면, 이제는 모든 속성을 아래와 같이 다시 지정해야 합니다:

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

`change` 메서드는 컬럼의 인덱스는 변경하지 않으므로, 인덱스를 추가/삭제하려면 별도로 인덱스 수정자를 사용하세요:

```php
// 인덱스 추가...
$table->bigIncrements('id')->primary()->change();

// 인덱스 삭제...
$table->char('postal_code', 10)->unique(false)->change();
```

모든 기존 "change" 마이그레이션을 일일이 수정하고 싶지 않다면, [마이그레이션 스쿼시](/docs/{{version}}/migrations#squashing-migrations) 기능을 사용할 수 있습니다:

```bash
php artisan schema:dump
```

스쿼시된 후에는 데이터베이스가 스키마 파일을 통해 마이그레이션되고, 남은 마이그레이션만 추가 적용됩니다.

<a name="floating-point-types"></a>
#### 부동 소수점 타입(Floating-Point Types)

**영향 가능성: 높음**

`double`과 `float` 마이그레이션 컬럼 타입이 모든 데이터베이스 간 일관되게 동작하도록 변경되었습니다.

- `double` 타입은 이제 표준 SQL 문법처럼 총 자릿수 및 소수점 이하 자릿수를 지정하지 않고, 단순한 `DOUBLE` 컬럼을 생성합니다. 기존의 `$total`, `$places` 인자를 삭제하세요:

```php
$table->double('amount');
```

- `float` 타입 역시 총 자릿수 및 소수점 이하 자릿수를 지정하지 않는 대신, 저장 크기를 결정하는 선택적 `$precision` 인자를 받습니다(4바이트 단정도, 8바이트 배정도). 따라서 `$total`, `$places` 인자를 삭제하고, 필요한 경우 `$precision`만 지정하세요:

```php
$table->float('amount', precision: 53);
```

- `unsignedDecimal`, `unsignedDouble`, `unsignedFloat` 메서드는 더는 지원되지 않습니다(MySQL에서 deprecated, 표준화도 안 됨). 계속 unsigned 속성을 사용하려면 `unsigned` 메서드를 체인해서 사용하세요:

```php
$table->decimal('amount', total: 8, places: 2)->unsigned();
$table->double('amount')->unsigned();
$table->float('amount', precision: 53)->unsigned();
```

<a name="dedicated-mariadb-driver"></a>
#### MariaDB 전용 드라이버

**영향 가능성: 매우 낮음**

MariaDB 접속 시 더 이상 MySQL 드라이버를 항상 사용하지 않고, MariaDB 전용 드라이버가 추가되었습니다.

MariaDB DB를 사용하는 경우, 커넥션 설정에서 `mariadb` 드라이버를 사용해 미래에 MariaDB의 특정 기능을 바로 활용할 수 있습니다:

    'driver' => 'mariadb',
    'url' => env('DB_URL'),
    'host' => env('DB_HOST', '127.0.0.1'),
    'port' => env('DB_PORT', '3306'),
    // ...

현재는 MySQL 드라이버와 동일하게 동작하나, 한 가지 차이점은 `uuid` 메서드로 Native UUID 컬럼을 생성합니다(기존엔 `char(36)`).

기존 마이그레이션에서 `uuid` 메서드를 사용했다면, `mariadb` 드라이버로 변경 시 `char`로 바꿔주어야 합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->char('uuid', 36);

    // ...
});
```

<a name="spatial-types"></a>
#### 공간 타입(Spatial Types)

**영향 가능성: 낮음**

마이그레이션의 공간 컬럼 타입이 데이터베이스별로 일관적으로 변경되었습니다. 따라서 기존의 `point`, `lineString`, `polygon`, `geometryCollection`, `multiPoint`, `multiLineString`, `multiPolygon`, `multiPolygonZ` 메서드를 대신하여 `geometry` 또는 `geography` 메서드를 사용하세요:

```php
$table->geometry('shapes');
$table->geography('coordinates');
```

MySQL, MariaDB, PostgreSQL에서 저장되는 값의 타입이나 SRID(공간 참조 시스템 식별자)를 제한하려면, `subtype`과 `srid`를 명시할 수 있습니다:

```php
$table->geometry('dimension', subtype: 'polygon', srid: 0);
$table->geography('latitude', subtype: 'point', srid: 4326);
```

PostgreSQL 문법의 `isGeometry`, `projection` 컬럼 수정자도 함께 제거되었습니다.

<a name="doctrine-dbal-removal"></a>
#### Doctrine DBAL 제거

**영향 가능성: 낮음**

다음과 같은 Doctrine DBAL 관련 클래스 및 메서드가 제거되었습니다. 이제 Laravel은 해당 패키지에 의존하지 않으며, 예전처럼 컬럼 타입 생성·수정 시 Doctrine 타입 등록이 필요하지 않습니다:

<div class="content-list" markdown="1">

- `Illuminate\Database\Schema\Builder::$alwaysUsesNativeSchemaOperationsIfPossible` 클래스 속성
- `Illuminate\Database\Schema\Builder::useNativeSchemaOperationsIfPossible()` 메서드
- `Illuminate\Database\Connection::usingNativeSchemaOperations()` 메서드
- `Illuminate\Database\Connection::isDoctrineAvailable()` 메서드
- `Illuminate\Database\Connection::getDoctrineConnection()` 메서드
- `Illuminate\Database\Connection::getDoctrineSchemaManager()` 메서드
- `Illuminate\Database\Connection::getDoctrineColumn()` 메서드
- `Illuminate\Database\Connection::registerDoctrineType()` 메서드
- `Illuminate\Database\DatabaseManager::registerDoctrineType()` 메서드
- `Illuminate\Database\PDO` 디렉터리
- `Illuminate\Database\DBAL\TimestampType` 클래스
- `Illuminate\Database\Schema\Grammars\ChangeColumn` 클래스
- `Illuminate\Database\Schema\Grammars\RenameColumn` 클래스
- `Illuminate\Database\Schema\Grammars\Grammar::getDoctrineTableDiff()` 메서드

</div>

또한, `dbal.types`를 통한 custom Doctrine 타입 등록도 더 이상 필요하지 않습니다.

기존에 DB 및 테이블 스키마 검사를 위해 Doctrine DBAL을 사용했다면, Laravel의 새로운 네이티브 스키마 메서드(`Schema::getTables()`, `Schema::getColumns()`, `Schema::getIndexes()`, `Schema::getForeignKeys()` 등)를 사용할 수 있습니다.

<a name="deprecated-schema-methods"></a>
#### 폐기된 스키마 메서드

**영향 가능성: 매우 낮음**

Doctrine 기반의 `Schema::getAllTables()`, `Schema::getAllViews()`, `Schema::getAllTypes()`는 제거되고, Laravel 네이티브 방식의 `Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()`로 대체되었습니다.

PostgreSQL 및 SQL Server에서는 새 스키마 메서드들이 3-part reference(예: `database.schema.table`)를 허용하지 않습니다. 대신 `connection()`을 통해 데이터베이스를 지정해야 합니다:

```php
Schema::connection('database')->hasTable('schema.table');
```

<a name="get-column-types"></a>
#### 스키마 빌더 `getColumnType()` 메서드

**영향 가능성: 매우 낮음**

`Schema::getColumnType()`는 이제 해당 컬럼의 실제 타입만 반환하며, 더 이상 Doctrine DBAL 타입을 반환하지 않습니다.

<a name="database-connection-interface"></a>
#### 데이터베이스 커넥션 인터페이스

**영향 가능성: 매우 낮음**

`Illuminate\Database\ConnectionInterface`에 새로운 `scalar` 메서드가 추가되었습니다. 이 인터페이스를 직접 구현한다면 아래 메서드를 추가해야 합니다:

```php
public function scalar($query, $bindings = [], $useReadPdo = true);
```

<a name="dates"></a>
### 날짜(Dates)

<a name="carbon-3"></a>
#### Carbon 3

**영향 가능성: 중간**

Laravel 11은 Carbon 2, Carbon 3을 모두 지원합니다. Carbon은 Laravel 및 많은 패키지에서 널리 사용되는 날짜 조작 라이브러리입니다. Carbon 3로 업그레이드 할 경우 `diffIn*` 메서드가 부동 소수점 수를 반환하고, 시간이 감소하는 방향이면 음수도 반환하므로(Caron 2와의 큰 차이점), [변경 로그](https://github.com/briannesbitt/Carbon/releases/tag/3.0.0) 및 [문서](https://carbon.nesbot.com/docs/#api-carbon-3)로 새 동작을 반드시 숙지하세요.

<a name="mail"></a>
### 메일(Mail)

<a name="the-mailer-contract"></a>
#### `Mailer` 계약

**영향 가능성: 매우 낮음**

`Illuminate\Contracts\Mail\Mailer` 계약에 새로운 `sendNow` 메서드가 추가되었습니다. 이 계약을 직접 구현하는 경우 아래 메서드도 추가해야 합니다:

```php
public function sendNow($mailable, array $data = [], $callback = null);
```

<a name="packages"></a>
### 패키지(Packages)

<a name="publishing-service-providers"></a>
#### 서비스 프로바이더 퍼블리시

**영향 가능성: 매우 낮음**

패키지에서 서비스 프로바이더를 직접 `app/Providers`에 퍼블리시하고, 애플리케이션의 `config/app.php`에 수동으로 등록했다면, 패키지를 업데이트하여 이제는 새 `ServiceProvider::addProviderToBootstrapFile` 메서드를 활용하도록 변경해야 합니다.

`addProviderToBootstrapFile` 메서드는 퍼블리시한 서비스 프로바이더를 자동으로 `bootstrap/providers.php`에 추가합니다. (Laravel 11부터는 `config/app.php`의 `providers` 배열이 존재하지 않습니다.)

```php
use Illuminate\Support\ServiceProvider;

ServiceProvider::addProviderToBootstrapFile(Provider::class);
```

<a name="queues"></a>
### 큐(Queues)

<a name="the-batch-repository-interface"></a>
#### `BatchRepository` 인터페이스

**영향 가능성: 매우 낮음**

`Illuminate\Bus\BatchRepository` 인터페이스에 새로운 `rollBack` 메서드가 추가되었습니다. 이 인터페이스를 구현하는 경우 아래 메서드를 추가해야 합니다:

```php
public function rollBack();
```

<a name="synchronous-jobs-in-database-transactions"></a>
#### 데이터베이스 트랜잭션 내 동기식(Job) 처리

**영향 가능성: 매우 낮음**

기존에는 동기식 큐 드라이버(sync)을 사용하는 Job이 언제나 즉시 실행되었지만, 이제는 큐 커넥션 또는 Job에 `after_commit` 옵션이 설정된 경우, 커밋 후에 실행됩니다.

<a name="rate-limiting"></a>
### Rate Limiting(요청 제한)

<a name="per-second-rate-limiting"></a>
#### 초 단위 Rate Limiting

**영향 가능성: 중간**

Laravel 11은 분 단위가 아닌 초 단위 Rate Limiting을 지원합니다. 이로 인해 여러 잠재적 변경사항이 있습니다:

- `GlobalLimit` 생성자는 이제 분이 아닌 초 단위로 인자를 받습니다. (문서화된 클래스가 아니므로 대부분의 앱에서는 직접 사용하지 않을 것입니다)

```php
new GlobalLimit($attempts, 2 * 60);
```

- `Limit` 생성자도 이제 초 단위로 인자를 받습니다. 보통의 사용은 `Limit::perMinute`, `Limit::perSecond`와 같은 정적 생성자를 사용하지만, 직접 인스턴스를 만들 경우 이제 초로 값을 전달해야 합니다:

```php
new Limit($key, $attempts, 2 * 60);
```

- `decayMinutes` 속성이 `decaySeconds`로 이름이 변경되었고, 단위도 분에서 초로 바뀌었습니다.
- `Illuminate\Queue\Middleware\ThrottlesExceptions`, `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 생성자 역시 초 단위 입력을 받습니다.

```php
new ThrottlesExceptions($attempts, 2 * 60);
new ThrottlesExceptionsWithRedis($attempts, 2 * 60);
```

<a name="cashier-stripe"></a>
### Cashier Stripe

<a name="updating-cashier-stripe"></a>
#### Cashier Stripe 업데이트

**영향 가능성: 높음**

Laravel 11은 Cashier Stripe 14.x를 더는 지원하지 않습니다. 따라서 필수 composer.json에서 Laravel Cashier Stripe 의존성을 `^15.0`으로 업데이트하세요.

Cashier Stripe 15.0은 마이그레이션을 직접 애플리케이션으로 퍼블리시해야 하며, 다음 명령어를 실행해야 합니다:

```shell
php artisan vendor:publish --tag=cashier-migrations
```

추가 변경사항은 [Cashier Stripe 업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/15.x/UPGRADE.md)를 참고하세요.

<a name="spark-stripe"></a>
### Spark (Stripe)

<a name="updating-spark-stripe"></a>
#### Spark Stripe 업데이트

**영향 가능성: 높음**

Laravel 11은 Spark Stripe 4.x를 더는 지원하지 않습니다. composer.json에서 Spark Stripe 의존성을 `^5.0`으로 업데이트하세요.

Spark Stripe 5.0에서 마이그레이션 퍼블리시 명령은 다음과 같습니다:

```shell
php artisan vendor:publish --tag=spark-migrations
```

추가 변경사항은 [Spark Stripe 업그레이드 가이드](https://spark.laravel.com/docs/spark-stripe/upgrade.html)를 참고하세요.

<a name="passport"></a>
### Passport

<a name="updating-telescope"></a>
#### Passport 업데이트

**영향 가능성: 높음**

Laravel 11은 Passport 11.x를 더는 지원하지 않습니다. composer.json에서 의존성을 `^12.0`으로 업데이트하세요.

마이그레이션 퍼블리시 명령은 아래와 같습니다:

```shell
php artisan vendor:publish --tag=passport-migrations
```

그리고 패스워드 grant 타입이 기본적으로 비활성화되어 있습니다. 이를 활성화하려면 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 아래를 호출하세요:

    public function boot(): void
    {
        Passport::enablePasswordGrant();
    }

<a name="sanctum"></a>
### Sanctum

<a name="updating-sanctum"></a>
#### Sanctum 업데이트

**영향 가능성: 높음**

Laravel 11은 Sanctum 3.x를 더는 지원하지 않습니다. composer.json에서 Laravel Sanctum 의존성을 `^4.0`으로 업데이트하세요.

마이그레이션 퍼블리시는 다음과 같이 실행해야 합니다:

```shell
php artisan vendor:publish --tag=sanctum-migrations
```

그리고 애플리케이션의 `config/sanctum.php`에서 `authenticate_session`, `encrypt_cookies`, `validate_csrf_token` 미들웨어의 레퍼런스를 아래와 같이 수정하세요:

    'middleware' => [
        'authenticate_session' => Laravel\Sanctum\Http\Middleware\AuthenticateSession::class,
        'encrypt_cookies' => Illuminate\Cookie\Middleware\EncryptCookies::class,
        'validate_csrf_token' => Illuminate\Foundation\Http\Middleware\ValidateCsrfToken::class,
    ],

<a name="telescope"></a>
### Telescope

<a name="updating-telescope"></a>
#### Telescope 업데이트

**영향 가능성: 높음**

Laravel 11은 Telescope 4.x를 더는 지원하지 않습니다. composer.json에서 Telescope 의존성을 `^5.0`으로 업데이트하세요.

마이그레이션 퍼블리시 명령어:

```shell
php artisan vendor:publish --tag=telescope-migrations
```

<a name="spatie-once-package"></a>
### Spatie Once 패키지

**영향 가능성: 중간**

Laravel 11은 클로저를 단 한 번만 실행하기 위한 자체 [`once` 함수](/docs/{{version}}/helpers#method-once)를 제공합니다. 따라서, `spatie/once` 패키지 의존성이 있다면 composer.json에서 삭제하세요.

<a name="miscellaneous"></a>
### 기타

`laravel/laravel`의 [GitHub 저장소](https://github.com/laravel/laravel)를 꼭 확인하시길 권장합니다. 이 중 많은 변경사항이 필수적이지는 않지만, 파일을 최신 상태로 맞춰두는 것이 좋습니다. 일부 변경사항은 본 가이드에 포함되어 있지 않으며, 설정 파일이나 주석 등은 별도로 관리해야 합니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/10.x...11.x)로 변경 내용을 쉽게 확인하고 필요한 것만 반영할 수 있습니다.
