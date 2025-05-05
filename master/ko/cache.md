# 캐시

- [소개](#introduction)
- [구성](#configuration)
    - [드라이버 사전 준비](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 아이템 조회하기](#retrieving-items-from-the-cache)
    - [캐시에 아이템 저장하기](#storing-items-in-the-cache)
    - [캐시에서 아이템 제거하기](#removing-items-from-the-cache)
    - [캐시 헬퍼](#the-cache-helper)
- [원자적(Atomic) 락](#atomic-locks)
    - [락 관리하기](#managing-locks)
    - [프로세스 간 락 관리하기](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

애플리케이션에서 수행하는 일부 데이터 조회 또는 처리 작업은 CPU를 많이 소모하거나 몇 초가 걸릴 수 있습니다. 이럴 경우, 조회한 데이터를 일정 시간 동안 캐시에 저장하여 동일한 데이터에 대한 후속 요청에서는 더 빠르게 데이터를 가져올 수 있도록 하는 것이 일반적입니다. 캐시 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히도, Laravel은 다양한 캐시 백엔드를 대상으로 하는 간결하고 통합된 API를 제공하여, 아주 빠른 데이터 조회를 활용하고 웹 애플리케이션의 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 구성

애플리케이션의 캐시 구성 파일은 `config/cache.php`에 위치해 있습니다. 이 파일에서 애플리케이션 전역에 사용할 기본 캐시 저장소를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스와 같은 인기 있는 캐시 백엔드를 기본 지원합니다. 또한 파일 기반 캐시 드라이버, 자동화된 테스트에 유용한 `array` 및 "null" 드라이버도 제공합니다.

캐시 구성 파일에는 그 외에도 다양한 옵션들이 있으니 참고하시길 바랍니다. 기본적으로 Laravel은 애플리케이션의 데이터베이스에 직렬화된 캐시 객체를 저장하는 `database` 캐시 드라이버를 사용하도록 설정되어 있습니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 경우, 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 이 테이블은 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/{{version}}/migrations)에 포함되어 있습니다. 만약 애플리케이션에 이 마이그레이션이 없다면, `make:cache-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. `config/cache.php` 설정 파일에 Memcached 서버 목록을 지정할 수 있습니다. 이 파일에는 이미 시작을 위한 `memcached.servers` 항목이 포함되어 있습니다:

```php
'memcached' => [
    // ...

    'servers' => [
        [
            'host' => env('MEMCACHED_HOST', '127.0.0.1'),
            'port' => env('MEMCACHED_PORT', 11211),
            'weight' => 100,
        ],
    ],
],
```

필요하다면, `host` 옵션에 UNIX 소켓 경로를 지정할 수 있습니다. 이 경우 `port` 옵션은 `0`으로 설정해야 합니다:

```php
'memcached' => [
    // ...

    'servers' => [
        [
            'host' => '/var/run/memcached/memcached.sock',
            'port' => 0,
            'weight' => 100
        ],
    ],
],
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 캐시를 사용하기 전에 PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나, Composer를 통해 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/{{version}}/sail)에는 이 확장 모듈이 이미 포함되어 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com), [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 애플리케이션 플랫폼에는 기본적으로 PhpRedis 확장 모듈이 설치되어 있습니다.

Redis 설정에 대한 더 자세한 내용은 [Laravel의 Redis 문서](/docs/{{version}}/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 캐시된 모든 데이터를 저장할 DynamoDB 테이블을 만들어야 합니다. 일반적으로 이 테이블의 이름은 `cache`이어야 하지만, `cache` 설정 파일의 `stores.dynamodb.table` 구성 값에 따라 이름을 정해야 합니다. 또한 테이블 이름은 `DYNAMODB_CACHE_TABLE` 환경 변수로도 설정할 수 있습니다.

이 테이블에는 애플리케이션의 `cache` 설정 파일 내 `stores.dynamodb.attributes.key` 설정값에 해당하는 이름의 문자열 파티션 키가 있어야 합니다. 디폴트로 파티션 키 이름은 `key`입니다.

일반적으로 DynamoDB는 만료된 항목을 자동으로 제거하지 않습니다. 따라서 [Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) 기능을 테이블에 활성화해야 합니다. TTL 설정 시 속성 이름을 `expires_at`으로 지정하세요.

다음으로, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다:

```shell
composer require aws/aws-sdk-php
```

또한, DynamoDB 캐시 저장소 설정 옵션에도 값을 지정해야 합니다. 보통 `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`와 같은 옵션은 애플리케이션의 `.env` 파일에 정의해야 합니다:

```php
'dynamodb' => [
    'driver' => 'dynamodb',
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => env('DYNAMODB_CACHE_TABLE', 'cache'),
    'endpoint' => env('DYNAMODB_ENDPOINT'),
],
```

<a name="mongodb"></a>
#### MongoDB

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 제공하는 `mongodb` 캐시 드라이버를 설정하여 사용할 수 있습니다. MongoDB는 만료된 캐시 항목을 자동으로 지우는데 사용할 수 있는 TTL 인덱스를 지원합니다.

MongoDB 설정에 대한 추가 정보는 MongoDB의 [Cache and Locks documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)을 참조하세요.

<a name="cache-usage"></a>
## 캐시 사용법

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스는 문서 전체에서 사용할 `Cache` 파사드를 통해 얻을 수 있습니다. `Cache` 파사드는 Laravel 캐시 계약의 기본 구현체에 간편한 접근을 제공합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록 표시
     */
    public function index(): array
    {
        $value = Cache::get('key');

        return [
            // ...
        ];
    }
}
```

<a name="accessing-multiple-cache-stores"></a>
#### 여러 캐시 저장소 접근

`Cache` 파사드를 사용하면 `store` 메서드를 통해 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일에 명시된 `stores` 배열 중 하나를 가리켜야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 아이템 조회하기

`Cache` 파사드의 `get` 메서드를 사용하면 캐시에서 아이템을 조회할 수 있습니다. 해당 아이템이 캐시에 없으면 `null`이 반환됩니다. 두 번째 인수를 통해 아이템이 없을 때 반환할 기본값을 지정할 수도 있습니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저를 전달할 수도 있습니다. 만약 지정한 아이템이 캐시에 존재하지 않을 경우 클로저 실행 결과가 반환됩니다. 클로저를 사용하면 데이터베이스나 외부 서비스에서 기본값을 지연 조회할 수 있습니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 아이템 존재 여부 확인

`has` 메서드로 캐시에 아이템이 존재하는지 확인할 수 있습니다. 해당 아이템이 존재하지만 값이 `null`인 경우에도 `false`가 반환됩니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가 / 감소

정수형 아이템의 값을 조정할 때는 `increment` 및 `decrement` 메서드를 사용할 수 있습니다. 두 메서드 모두 증가/감소할 값을 두 번째 인수로 전달할 수 있습니다:

```php
// 값이 없으면 0으로 초기화...
Cache::add('key', 0, now()->addHours(4));

// 값 증가 또는 감소...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 조회 후 저장

캐시에서 아이템을 조회하되, 요청한 아이템이 없으면 기본값을 저장하고 싶은 경우가 있습니다. 예를 들어, 모든 사용자 데이터를 캐시에서 가져오되, 없으면 데이터베이스에서 조회하여 캐시에 넣고 싶을 수 있습니다. `Cache::remember` 메서드를 사용하면 가능합니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

아이템이 캐시에 존재하지 않으면 클로저가 실행되며, 결과값이 캐시에 저장됩니다.

`rememberForever` 메서드는 캐시에서 아이템을 조회하거나 없으면 영구적으로 저장합니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember` 메서드를 사용할 때, 캐시된 값이 만료되면 일부 사용자에게 느린 응답을 제공할 수도 있습니다. 특정 데이터에 대해서는, 만료된 캐시 값을 재계산하는 동안 부분적으로 오래된(stale) 데이터를 제공함으로써 일부 사용자가 느린 응답을 겪지 않도록 할 수 있습니다. 이를 "stale-while-revalidate"(SWR) 패턴이라고 하며, `Cache::flexible` 메서드에서 해당 패턴을 지원합니다.

flexible 메서드는 캐시 값이 "신선"하다고 간주될 기간과 "stale"로 간주되는 기간을 배열로 지정받습니다. 첫 번째 값은 신선한 기간(초), 두 번째 값은 재계산이 필요해지기 전까지 stale 데이터로 제공할 수 있는 기간(초)입니다.

신선한 기간 중 요청이 들어오면 즉시 캐시를 반환합니다. stale 기간인 경우, stale 값을 반환하되 사용자 응답 이후 [deferred function](/docs/{{version}}/helpers#deferred-functions)이 등록되어 캐시를 백그라운드로 갱신합니다. 두 기간이 모두 지나 만료된 경우, 즉시 값을 새로 계산해 반환하므로 응답이 느려질 수 있습니다:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제

캐시에서 아이템을 조회한 뒤 바로 삭제하려면 `pull` 메서드를 사용합니다. `get`과 마찬가지로, 아이템이 없으면 `null`을 반환합니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 아이템 저장하기

`Cache` 파사드의 `put` 메서드로 캐시에 아이템을 저장할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

시간을 지정하지 않으면 해당 아이템은 영구적으로 저장됩니다:

```php
Cache::put('key', 'value');
```

초 단위 숫자 대신, 만료 시간을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다:

```php
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장

`add` 메서드는 저장소에 해당 아이템이 존재하지 않을 때만 캐시에 저장합니다. 실제로 저장될 경우 `true`를 반환, 아니면 `false`를 반환합니다. `add` 메서드는 원자적(atomic) 연산입니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 영구 저장

`forever` 메서드를 사용하면 아이템을 만료 없이 영구적으로 캐시에 저장할 수 있습니다. 이 경우 명시적으로 `forget` 메서드로 삭제해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용할 경우, "영구" 저장된 항목도 캐시 용량 초과 시 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 아이템 제거하기

`forget` 메서드를 사용하여 캐시에서 아이템을 제거할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간을 0 또는 음수로 지정하면 해당 아이템을 제거할 수도 있습니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

전체 캐시를 지우려면 `flush` 메서드를 사용하세요:

```php
Cache::flush();
```

> [!WARNING]
> 캐시를 flush할 경우 설정된 캐시 "prefix"와 관계없이 모든 엔트리가 삭제됩니다. 다른 애플리케이션과 캐시 공간을 공유한다면 신중히 사용해야 합니다.

<a name="the-cache-helper"></a>
### 캐시 헬퍼

`Cache` 파사드 외에 전역 `cache` 함수를 이용해 데이터를 저장/조회할 수도 있습니다. `cache` 함수에 문자열 하나만 전달하면 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키/값 쌍의 배열과 만료 시간을 전달하면 해당 기간 동안 값을 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

인수를 전달하지 않으면 `Illuminate\Contracts\Cache\Factory` 인스턴스를 반환하여 다른 캐시 메서드를 사용할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수 사용 시, [파사드 테스트](/docs/{{version}}/mocking#mocking-facades)와 동일하게 `Cache::shouldReceive` 메서드를 활용할 수 있습니다.

<a name="atomic-locks"></a>
## 원자적(Atomic) 락

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리하기

원자적 락은 경쟁조건을 걱정하지 않고 분산 락을 조작할 수 있게 해줍니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)에서는 하나의 원격 작업만 서버에서 동시에 실행되도록 원자적 락을 사용합니다. `Cache::lock` 메서드로 락을 생성하고 관리할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 락을 10초 동안 획득...

    $lock->release();
}
```

`get` 메서드는 클로저도 받을 수 있습니다. 클로저 실행 후 Laravel이 자동으로 락을 해제합니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 10초 동안 락을 획득하고 자동 해제...
});
```

요청 시 락이 사용 불가능하다면, Laravel이 지정한 초만큼 대기하도록 할 수 있습니다. 시간 내에 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최대 5초 대기 후 락 획득...
} catch (LockTimeoutException $e) {
    // 락 획득 실패...
} finally {
    $lock->release();
}
```

위 예시는 `block` 메서드에 클로저를 전달해 더 간단히 구현할 수도 있습니다. 클로저를 전달하면 지정한 시간 동안 락 획득을 시도하고, 클로저 실행 후 자동 해제됩니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 10초 락 획득...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리하기

때로는 한 프로세스에서 락을 획득하고, 다른 프로세스에서 해제하고 싶을 수도 있습니다. 예를 들어, 웹 요청 중 락을 얻고, 해당 요청에 의해 트리거된 큐 작업의 마지막에서 락을 해제하고 싶을 수 있습니다. 이 경우 락의 스코프 "owner token"을 큐 작업에 전달하여, 해당 토큰으로 락을 복원할 수 있습니다.

아래 예시에서는 락을 성공적으로 획득하면 큐 작업을 디스패치하고, 락의 owner 토큰을 함께 전달합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

`ProcessPodcast` 잡에서는 owner 토큰을 사용해 락을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

현재 owner를 무시하고 락을 강제로 해제하고 싶다면, `forceRelease` 메서드를 사용하세요:

```php
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가하기

<a name="writing-the-driver"></a>
### 드라이버 작성하기

커스텀 캐시 드라이버를 만들려면, 먼저 `Illuminate\Contracts\Cache\Store` [계약(Contract)](/docs/{{version}}/contracts)를 구현해야 합니다. 예를 들어, MongoDB 캐시 구현은 다음과 유사할 수 있습니다:

```php
<?php

namespace App\Extensions;

use Illuminate\Contracts\Cache\Store;

class MongoStore implements Store
{
    public function get($key) {}
    public function many(array $keys) {}
    public function put($key, $value, $seconds) {}
    public function putMany(array $values, $seconds) {}
    public function increment($key, $value = 1) {}
    public function decrement($key, $value = 1) {}
    public function forever($key, $value) {}
    public function forget($key) {}
    public function flush() {}
    public function getPrefix() {}
}
```

이 메서드들을 모두 MongoDB 커넥션을 이용해 구현하면 됩니다. 각 메서드의 구현 예시는 [Laravel 프레임워크 소스 코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고하세요. 구현을 완료했다면, `Cache` 파사드의 `extend` 메서드로 커스텀 드라이버 등록을 마무리할 수 있습니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 내에 `Extensions` 네임스페이스를 생성하는 것도 좋습니다. 하지만 Laravel은 엄격한 애플리케이션 구조를 요구하지 않으니, 원하는 대로 조직화해도 됩니다.

<a name="registering-the-driver"></a>
### 드라이버 등록하기

커스텀 캐시 드라이버는 `Cache` 파사드의 `extend` 메서드를 사용해 등록합니다. 다른 서비스 제공자가 자신의 `boot` 메서드에서 캐시 값을 읽으려고 할 수 있으니, 커스텀 드라이버는 `booting` 콜백에서 등록해야 합니다. 이렇게 하면 모든 서비스 제공자의 `register` 메서드가 호출된 후, 각 서비스 제공자의 `boot` 메서드 호출 직전에 커스텀 드라이버가 등록됩니다. 아래 예시처럼 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 booting 콜백을 등록하세요:

```php
<?php

namespace App\Providers;

use App\Extensions\MongoStore;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        $this->app->booting(function () {
             Cache::extend('mongo', function (Application $app) {
                 return Cache::repository(new MongoStore);
             });
         });
    }

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        // ...
    }
}
```

`extend` 메서드의 첫 번째 인자는 드라이버명이며, 이는 `config/cache.php`의 `driver` 옵션과 일치해야 합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저입니다. 클로저에는 [서비스 컨테이너](/docs/{{version}}/container)의 `$app` 인스턴스가 전달됩니다.

확장 등록이 끝나면, 애플리케이션의 `CACHE_STORE` 환경 변수나 `config/cache.php` 설정 파일의 `default` 옵션을 확장명으로 수정하세요.

<a name="events"></a>
## 이벤트

모든 캐시 작업 시마다 코드를 실행하려면 캐시에서 발생하는 다양한 [이벤트](/docs/{{version}}/events)를 감지할 수 있습니다:

<div class="overflow-auto">

| 이벤트 명칭 |
| --- |
| `Illuminate\Cache\Events\CacheHit` |
| `Illuminate\Cache\Events\CacheMissed` |
| `Illuminate\Cache\Events\KeyForgotten` |
| `Illuminate\Cache\Events\KeyWritten` |

</div>

성능 향상을 위해, `config/cache.php` 설정 파일에서 특정 캐시 저장소의 `events` 옵션을 `false`로 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
