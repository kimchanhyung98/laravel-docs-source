# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 전제 조건](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 조회하기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [Cache 헬퍼 함수](#the-cache-helper)
- [원자적 잠금 (Atomic Locks)](#atomic-locks)
    - [잠금 관리](#managing-locks)
    - [프로세스 간 잠금 관리](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 수행하는 일부 데이터 조회나 처리 작업은 CPU를 많이 사용하거나 완료까지 여러 초가 걸릴 수 있습니다. 이런 경우, 데이터를 일정 시간 동안 캐시하여 이후 동일 데이터를 요청할 때 빠르게 가져오는 것이 일반적입니다. 캐시된 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io) 같은 매우 빠른 데이터 저장소에 보관됩니다.

Laravel은 다양한 캐시 백엔드에 대해 표현력이 뛰어난 통합 API를 제공하므로, 이들의 빠른 데이터 조회를 활용해 웹 애플리케이션의 속도를 쉽게 개선할 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치해 있습니다. 이 파일에서 애플리케이션 전체에 기본으로 사용할 캐시 저장소를 지정할 수 있습니다. Laravel은 기본적으로 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등 인기 있는 캐시 백엔드를 지원합니다. 또한, 파일 기반 캐시 드라이버가 제공되며, `array`와 `null` 드라이버는 자동화 테스트 시 편리하게 사용할 수 있는 캐시 백엔드를 제공합니다.

캐시 설정 파일에는 그 외에도 다양한 옵션이 포함되어 있습니다. 기본 설정은 `database` 캐시 드라이버를 사용하도록 되어 있으며, 이 드라이버는 직렬화된 캐시 데이터를 애플리케이션 데이터베이스에 저장합니다.

<a name="driver-prerequisites"></a>
### 드라이버 전제 조건 (Driver Prerequisites)

<a name="prerequisites-database"></a>
#### 데이터베이스 (Database)

`database` 캐시 드라이버를 사용할 경우, 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 보통 Laravel 기본 마이그레이션인 `0001_01_01_000001_create_cache_table.php`에 포함되어 있습니다. 만약 애플리케이션에 없다면, Artisan 명령어 `make:cache-table`을 사용해 테이블 마이그레이션을 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버 사용 시에는 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. `config/cache.php` 설정 파일에서 Memcached 서버를 모두 나열할 수 있으며, 기본적으로 `memcached.servers` 항목이 포함되어 있습니다:

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

필요하면 `host` 옵션에 UNIX 소켓 경로를 설정할 수도 있습니다. 이 경우 `port`는 `0`으로 지정해야 합니다:

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

Redis 캐시를 Laravel에서 사용하려면 PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer로 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/12.x/sail)에는 PhpRedis 확장이 기본으로 포함되어 있습니다. 또한, 공식 Laravel 애플리케이션 플랫폼인 [Laravel Cloud](https://cloud.laravel.com), [Laravel Forge](https://forge.laravel.com)에는 PhpRedis 확장이 기본 설치되어 있습니다.

Redis 설정 관련 자세한 내용은 Laravel [Redis 문서 페이지](/docs/12.x/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하려면, 먼저 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 보통 이 테이블 이름은 `cache`로 지정하지만, `cache` 설정 파일 내 `stores.dynamodb.table` 옵션 값에 따라 이름을 정할 수도 있습니다. `DYNAMODB_CACHE_TABLE` 환경 변수로도 테이블 이름 설정이 가능합니다.

테이블은 문자열 파티션 키를 가져야 하며, 이 키 이름은 `cache` 설정 파일 내 `stores.dynamodb.attributes.key` 설정 값과 일치해야 합니다. 기본값은 `key`입니다.

DynamoDB는 만료된 항목을 자동으로 삭제하지 않으므로, 테이블에 [Time to Live(TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활성화해야 합니다. TTL 설정 시 TTL 속성 이름은 `expires_at`으로 지정하세요.

그리고 Laravel과 DynamoDB 간 통신을 위해 AWS SDK를 설치해야 합니다:

```shell
composer require aws/aws-sdk-php
```

또한, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`와 같은 DynamoDB 캐시 저장소 설정에 필요한 환경 변수 값을 `.env` 파일에 정의해야 합니다:

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지가 제공하는 `mongodb` 캐시 드라이버를 이용할 수 있으며, `mongodb` 데이터베이스 연결 설정을 통해 구성합니다. MongoDB는 TTL 인덱스를 지원해 만료된 캐시 항목을 자동으로 삭제할 수 있습니다.

MongoDB 설정에 관한 자세한 내용은 MongoDB 공식 [Cache 및 Locks 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하세요.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기 (Obtaining a Cache Instance)

캐시 저장소 인스턴스를 얻으려면, 문서 전반에서 사용할 `Cache` 파사드를 사용할 수 있습니다. `Cache` 파사드는 Laravel 캐시 계약의 구현체에 간편하게 접근할 수 있도록 해줍니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 보여줍니다.
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
#### 여러 캐시 저장소 접근하기

`Cache` 파사드에서 `store` 메서드를 사용해 여러 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일 내 `stores` 배열에 정의된 저장소 이름과 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 조회하기 (Retrieving Items From the Cache)

`Cache` 파사드의 `get` 메서드를 사용해 캐시에서 항목을 조회합니다. 항목이 없으면 `null`을 반환합니다. 원하는 경우, 두 번째 인수로 기본값을 지정할 수도 있습니다. 항목이 없으면 기본값이 반환됩니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값 대신에 클로저를 넘겨서, 캐시에 항목이 없을 때 클로저의 결과를 반환하도록 할 수도 있습니다. 이 방식은 데이터베이스나 외부 서비스에서 값을 지연 조회할 때 유용합니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인하기

`has` 메서드는 캐시에 항목이 존재하는지 확인할 때 사용합니다. 단, 항목 값이 `null`이라도 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가 / 감소

`increment`와 `decrement` 메서드는 정수형 캐시 값을 증가 또는 감소시킬 때 사용합니다. 두 메서드는 두 번째 인수로 증감할 값(기본 1)을 받을 수 있습니다:

```php
// 값이 없으면 초기화...
Cache::add('key', 0, now()->addHours(4));

// 값 증가 또는 감소...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 조회 후 저장하기 (Retrieve and Store)

캐시에서 항목을 조회하면서, 없으면 기본값을 저장하고 싶을 때가 있습니다. 예를 들어, 사용자 목록을 캐시에서 가져오거나 없으면 데이터베이스에서 조회해 저장하는 경우입니다. 이때 `Cache::remember` 메서드를 사용합니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

항목이 없으면 `remember` 메서드의 클로저가 실행되어 결과를 캐시에 저장합니다.

`rememberForever` 메서드는 항목을 영구 저장하고 없을 때 가져오는 데 사용합니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate (SWR)

`Cache::remember`를 쓸 때, 캐시 값 만료 시 일부 사용자만 느린 응답을 받을 수 있습니다. 특정 데이터는 만료된 캐시를 잠시 유지하면서 백그라운드에서 재계산하는 것이 유용합니다. 이를 "stale-while-revalidate" 패턴이라고 하며, `Cache::flexible` 메서드가 구현체를 제공합니다.

`flexible`은 배열 형태로 캐시가 “신선(fresh)”한 기간과 “오래된(stale)” 기간을 받습니다. 배열 첫째 값은 신선 상태 유지 시간, 둘째는 만료 간격입니다.

- 신선 기간 내 요청 시 캐시 값을 즉시 반환하고 재계산하지 않습니다.
- 오래된 기간 내 요청 시, 오래된 값을 반환하고 응답 전송 후[지연 함수](/docs/12.x/helpers#deferred-functions)로 캐시를 갱신합니다.
- 둘째 값 초과 요청 시, 캐시는 만료된 것으로 간주하고 즉시 재계산하여 느린 응답이 발생할 수 있습니다:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제하기 (Retrieve and Delete)

캐시에서 항목을 조회한 다음 삭제하고 싶다면 `pull` 메서드를 사용하세요. 항목이 없으면 `null` 반환하며, 두 번째 인수로 기본값을 줄 수도 있습니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기 (Storing Items in the Cache)

`Cache` 파사드의 `put` 메서드로 캐시에 항목을 저장할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

만료 시간을 지정하지 않으면 항목은 무기한 저장됩니다:

```php
Cache::put('key', 'value');
```

만료 시간으로 초 단위 정수 대신, `DateTime` 인스턴스를 넘길 수도 있습니다:

```php
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 항목이 없을 때만 저장하기

`add` 메서드는 캐시에 항목이 없을 때만 저장하며, 성공적으로 저장했으면 `true`, 아니면 `false`를 반환합니다. `add`는 원자적 연산으로 작동합니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 항목을 영구 저장하기

`forever` 메서드는 항목을 만료 없이 캐시합니다. 영구 저장된 항목은 `forget` 메서드로 직접 삭제해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버 사용할 때, 영구 저장된 항목도 캐시 용량 한도에 도달하면 제거될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기 (Removing Items From the Cache)

`forget` 메서드로 캐시 항목을 삭제할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간을 0 또는 음수로 지정해도 삭제가 가능합니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메서드는 캐시 전체를 비웁니다:

```php
Cache::flush();
```

> [!WARNING]
> 캐시 전체 삭제 시 설정된 캐시 접두사(prefix)는 무시되며 캐시 내 모든 항목이 제거됩니다. 다른 애플리케이션과 캐시를 공유하는 경우 주의해서 사용하세요.

<a name="cache-memoization"></a>
### 캐시 메모이제이션 (Cache Memoization)

Laravel의 `memo` 캐시 드라이버는 단일 요청이나 작업 중에 조회된 캐시 값을 메모리에 임시 저장해 중복 조회를 방지합니다. 이를 통해 성능을 크게 향상시킬 수 있습니다.

`memo` 메서드를 호출해 메모이제이션 캐시를 사용합니다:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

선택적으로 `memo` 메서드에 캐시 저장소 이름을 넘길 수 있습니다. 그러면 메모이제이션 드라이버가 그 저장소를 장식(decorate)합니다:

```php
// 기본 캐시 저장소 사용...
$value = Cache::memo()->get('key');

// Redis 저장소 사용...
$value = Cache::memo('redis')->get('key');
```

같은 요청 또는 작업 내에서 처음 호출한 `get`은 기존 캐시를 조회하지만, 이후 호출은 메모리에 저장된 값을 반환합니다:

```php
// 캐시 조회...
$value = Cache::memo()->get('key');

// 캐시 조회하지 않고 메모이제이션 값 반환...
$value = Cache::memo()->get('key');
```

`put`, `increment`, `remember` 등 캐시 값을 변경하는 메서드를 호출하면 메모이제이션된 값이 자동으로 삭제되고, 변경 작업이 기본 캐시 저장소에 위임됩니다:

```php
Cache::memo()->put('name', 'Taylor'); // 기본 캐시에 쓰기...
Cache::memo()->get('name');           // 기본 캐시 조회...
Cache::memo()->get('name');           // 메모이제이션으로 캐시 조회 생략...

Cache::memo()->put('name', 'Tim');    // 메모이제이션 값 삭제 후 캐시에 새 값 쓰기...
Cache::memo()->get('name');           // 다시 기본 캐시를 조회...
```

<a name="the-cache-helper"></a>
### Cache 헬퍼 함수 (The Cache Helper)

`Cache` 파사드 외에도 전역 함수 `cache`를 사용해 캐시에서 데이터를 조회하거나 저장할 수 있습니다. 인수가 문자열 한 개일 경우, 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키-값 배열과 만료 시간을 인수로 주면, 캐시에 값을 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

인수를 넘기지 않으면 `Illuminate\Contracts\Cache\Factory` 구현체 인스턴스가 반환되고, 다양한 캐시 메서드를 호출할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수 호출을 테스트할 때도 `Cache::shouldReceive` 메서드를 사용하여 파사드 테스트와 동일하게 모킹할 수 있습니다. ([파사드 테스트 문서](/docs/12.x/mocking#mocking-facades))

<a name="atomic-locks"></a>
## 원자적 잠금 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신 중이어야 합니다.

<a name="managing-locks"></a>
### 잠금 관리 (Managing Locks)

원자적 잠금은 경쟁 조건 걱정 없이 분산 잠금을 조작할 수 있게 해줍니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)는 서버에서 동시에 하나의 원격 작업만 실행되도록 원자적 잠금을 사용합니다. `Cache::lock` 메서드로 잠금을 생성하고 관리할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 잠금 획득...

    $lock->release();
}
```

`get` 메서드에 클로저를 넘길 수도 있으며, 클로저 실행 후 Laravel이 자동으로 잠금을 해제합니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 10초 동안 잠금 획득 후 자동 해제...
});
```

잠금을 즉시 획득할 수 없으면 Laravel이 지정한 시간 동안 기다리도록 할 수 있습니다. 시간이 초과하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다:

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최대 5초 대기 후 잠금 획득...
} catch (LockTimeoutException $e) {
    // 잠금 획득 실패...
} finally {
    $lock->release();
}
```

위 예제는 클로저를 `block` 메서드에 넘겨 간략화할 수 있습니다. 이 경우 Laravel이 지정된 시간 동안 잠금 획득을 시도하고, 클로저 실행 후 자동으로 잠금을 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 10초 동안 잠금 획득...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 잠금 관리 (Managing Locks Across Processes)

가끔 잠금을 한 프로세스에서 획득해 다른 프로세스에서 해제해야 할 때가 있습니다. 예를 들어 웹 요청 도중 잠금을 얻고, 그 요청에 의해 트리거된 큐 작업 완료 시 잠금을 해제하는 경우입니다. 이때 잠금의 범위가 지정된 "소유자 토큰(owner token)"을 큐 작업에 전달해 작업이 해당 잠금을 재구성할 수 있게 해야 합니다.

아래 예에서는 잠금 획득 시 큐 작업을 디스패치하고, 잠금 소유자 토큰을 `owner` 메서드로 받아 큐 작업에 전달합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

`ProcessPodcast` 작업 내에서 소유자 토큰으로 잠금을 복원해 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

잠금을 소유자 확인 없이 강제로 해제하려면 `forceRelease` 메서드를 사용하세요:

```php
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가하기 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성하기 (Writing the Driver)

커스텀 캐시 드라이버를 만들려면 먼저 `Illuminate\Contracts\Cache\Store` [계약](/docs/12.x/contracts)을 구현해야 합니다. 예를 들어 MongoDB 캐시 구현은 다음과 비슷할 수 있습니다:

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

MongoDB 연결을 활용해 메서드들을 구현하면 됩니다. 구현 예시는 [Laravel 프레임워크 소스코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고하세요.

구현이 완료되면 `Cache` 파사드의 `extend` 메서드를 호출해 커스텀 드라이버 등록을 마칩니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드는 `app` 디렉토리에 `Extensions` 네임스페이스를 만들어 보관할 수 있습니다. Laravel은 엄격한 애플리케이션 구조가 없으니 자유롭게 원하는 구조로 조직하세요.

<a name="registering-the-driver"></a>
### 드라이버 등록하기 (Registering the Driver)

Laravel에 커스텀 캐시 드라이버를 등록하려면 `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 부트 과정에서 캐시를 참조할 수도 있으므로, 등록은 `boot` 메서드 호출 직전, 모든 서비스 프로바이더의 `register` 메서드 호출 후 실행되는 `booting` 콜백 내에서 하는 것이 좋습니다.

`App\Providers\AppServiceProvider` 클래스의 `register` 메서드에 `booting` 콜백을 다음과 같이 추가하세요:

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
     * 애플리케이션 서비스를 등록합니다.
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
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        // ...
    }
}
```

`extend` 메서드의 첫 번째 인수는 드라이버명으로, `config/cache.php`의 `driver` 옵션 값과 일치해야 합니다. 두 번째 인수는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저이며, `$app` 서비스 컨테이너 인스턴스를 받을 수 있습니다.

등록 후, 커스텀 드라이버명을 `.env` 변수 `CACHE_STORE` 또는 `config/cache.php`의 `default` 옵션에 지정하세요.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 작업 시 코드를 실행하려면, 캐시가 전송하는 다양한 [이벤트](/docs/12.x/events)를 리스닝할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                   |
|----------------------------------------------|
| `Illuminate\Cache\Events\CacheFlushed`       |
| `Illuminate\Cache\Events\CacheFlushing`      |
| `Illuminate\Cache\Events\CacheHit`           |
| `Illuminate\Cache\Events\CacheMissed`        |
| `Illuminate\Cache\Events\ForgettingKey`      |
| `Illuminate\Cache\Events\KeyForgetFailed`    |
| `Illuminate\Cache\Events\KeyForgotten`       |
| `Illuminate\Cache\Events\KeyWriteFailed`     |
| `Illuminate\Cache\Events\KeyWritten`         |
| `Illuminate\Cache\Events\RetrievingKey`      |
| `Illuminate\Cache\Events\RetrievingManyKeys` |
| `Illuminate\Cache\Events\WritingKey`         |
| `Illuminate\Cache\Events\WritingManyKeys`    |

</div>

성능 향상을 위해 캐시 저장소별로 `config/cache.php`에서 `events` 옵션을 `false`로 설정해 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```