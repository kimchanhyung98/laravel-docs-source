# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [항목 수명 연장하기](#extending-item-lifetime)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 헬퍼](#the-cache-helper)
- [원자적(Atomic) 락](#atomic-locks)
    - [락 관리](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 데이터 조회나 처리 작업 중 일부는 CPU를 많이 사용하거나 몇 초가 소요될 수 있습니다. 이런 경우 동일한 데이터에 대한 이후 요청에서 빠르게 데이터를 가져올 수 있도록 한동안 데이터를 캐시에 저장하는 것이 일반적입니다. 캐시된 데이터는 대개 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 보관됩니다.

다행히도, Laravel은 다양한 캐시 백엔드에 대해 일관되고 표현력 있는 API를 제공하여, 이러한 빠른 데이터 조회 기능을 활용하고 여러분의 웹 애플리케이션 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서 애플리케이션 전반에서 기본적으로 사용할 캐시 저장소를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스와 같은 대표적인 캐싱 백엔드를 기본으로 지원합니다. 또한, 파일 기반 캐시 드라이버도 제공하며, `array`와 "null" 캐시 드라이버는 자동화된 테스트에서 편리하게 사용할 수 있는 캐시 백엔드를 제공합니다.

캐시 설정 파일에는 검토할 수 있는 다양한 기타 옵션들도 포함되어 있습니다. 기본적으로 Laravel은 `database` 캐시 드라이버를 사용하도록 설정되어 있으며, 이는 직렬화된 캐시 객체를 애플리케이션의 데이터베이스에 저장합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항 (Driver Prerequisites)

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 때는 캐시 데이터를 담을 데이터베이스 테이블이 필요합니다. 보통 이 테이블은 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/master/migrations)에 포함되어 있습니다. 만약 애플리케이션에 이 마이그레이션이 없다면, `make:cache-table` Artisan 명령어를 사용하여 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. `config/cache.php` 설정 파일 내에 모든 Memcached 서버를 나열할 수 있습니다. 이 파일에는 이미 시작할 수 있도록 `memcached.servers` 항목이 포함되어 있습니다:

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

필요하다면, `host` 옵션을 UNIX 소켓 경로로 설정할 수도 있습니다. 이 경우에는 `port` 옵션을 `0`으로 지정해야 합니다:

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

Laravel에서 Redis 캐시를 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 기능을 설치하거나, Composer를 통해 `predis/predis` 패키지(~2.0 버전)를 설치해야 합니다. [Laravel Sail](/docs/master/sail)에는 이미 이 확장 기능이 포함되어 있습니다. 또한, [Laravel Cloud](https://cloud.laravel.com) 및 [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 애플리케이션 플랫폼도 PhpRedis 확장 기능을 기본적으로 설치하고 있습니다.

Redis 설정에 대한 자세한 내용은 [Laravel Redis 문서](/docs/master/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 보통 이 테이블의 이름은 `cache`로 지정하는 것이 일반적입니다. 하지만, 테이블 이름은 `cache` 설정 파일 내의 `stores.dynamodb.table` 설정값을 기준으로 지정해야 하며, 환경 변수 `DYNAMODB_CACHE_TABLE`을 통해서도 지정할 수 있습니다.

이 테이블에는 문자열 파티션 키가 필요하며, 키의 이름은 애플리케이션의 `cache` 설정 파일 내 `stores.dynamodb.attributes.key` 설정값과 일치해야 합니다. 기본적으로 이 파티션 키의 이름은 `key`입니다.

일반적으로 DynamoDB는 테이블에서 만료된 항목을 사전에 제거하지 않습니다. 따라서 테이블에 대해 [TTL(Time to Live)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활성화해야 합니다. 테이블의 TTL 설정을 구성할 때, TTL 속성 이름을 `expires_at`으로 지정해야 합니다.

다음으로, AWS SDK를 설치하여 Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 해야 합니다:

```shell
composer require aws/aws-sdk-php
```

또한, DynamoDB 캐시 저장소의 설정 옵션에 값이 제공되어야 합니다. 보통 `AWS_ACCESS_KEY_ID` 및 `AWS_SECRET_ACCESS_KEY`와 같은 옵션들은 애플리케이션의 `.env` 설정 파일에 정의해야 합니다:

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 `mongodb` 캐시 드라이버를 제공하며, `mongodb` 데이터베이스 연결로 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하므로, 만료된 캐시 항목을 자동으로 제거할 수 있습니다.

MongoDB 설정에 대한 자세한 내용은 MongoDB [Cache and Locks 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하세요.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면, 이 문서 전체에서 사용할 `Cache` 파사드(Facade)를 사용할 수 있습니다. `Cache` 파사드는 Laravel의 캐시 계약(Contract) 기본 구현체에 편리하고 간결하게 접근할 수 있게 해줍니다:

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
#### 여러 캐시 저장소 접근

`Cache` 파사드를 사용하면 `store` 메서드를 통해 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일의 `stores` 설정 배열에 나열된 저장소 중 하나와 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 가져올 때 사용합니다. 만약 해당 항목이 캐시에 존재하지 않으면, `null`이 반환됩니다. 필요하다면, 두 번째 인수로 해당 항목이 없을 때 반환할 기본값을 지정할 수 있습니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저(Closure)를 전달할 수도 있습니다. 지정한 항목이 캐시에 없는 경우, 클로저 실행 결과가 반환됩니다. 클로저를 사용하면 데이터베이스나 외부 서비스에서 기본값을 나중에 조회하도록 유예할 수 있습니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인

`has` 메서드를 사용하면 캐시에 항목이 존재하는지 확인할 수 있습니다. 이 메서드는 해당 항목이 존재하더라도 값이 `null`이면 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가 / 감소시키기

정수형 항목의 값을 조정하려면 `increment` 및 `decrement` 메서드를 사용할 수 있습니다. 이들 메서드는 두 번째 인수로 값을 얼마만큼 증가 또는 감소시킬지 지정할 수 있습니다:

```php
// 값이 존재하지 않으면 초기화...
Cache::add('key', 0, now()->addHours(4));

// 값 증가 또는 감소...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 조회 및 저장

캐시에서 항목을 조회하면서, 해당 항목이 없으면 기본값을 저장하려는 경우가 있습니다. 예를 들어, 모든 사용자를 캐시에서 가져오되, 없으면 데이터베이스에서 가져와서 캐시에 추가하고 싶을 수 있습니다. 이때 `Cache::remember` 메서드를 사용할 수 있습니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

캐시에 항목이 없다면, `remember` 메서드에 전달된 클로저가 실행되어 그 결과가 캐시에 저장됩니다.

캐시에 항목이 없을 때 영구적으로 저장하려면 `rememberForever` 메서드를 사용할 수 있습니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### 스테일-와일-리밸리데이트(Stale While Revalidate)

`Cache::remember` 메서드를 사용할 때, 캐시된 값이 만료된 경우 일부 사용자가 느린 응답을 경험할 수 있습니다. 특정 유형의 데이터에 대해서는, 만료된(스테일) 데이터를 임시로 제공하면서 백그라운드에서 새로운 캐시 값을 다시 계산하도록 하는 것이 유용할 수 있습니다. 이렇게 하면 일부 사용자가 값을 계산하는 동안 느린 응답을 경험하지 않아도 됩니다. 이 패턴을 "stale-while-revalidate"라고 하며, `Cache::flexible` 메서드에서 이를 구현할 수 있습니다.

`flexible` 메서드는 캐시 값이 "신선(fresh)"하다고 간주하는 시간과 "스테일(stale, 만료)" 상태가 되는 시점을 배열로 받아들입니다. 첫 번째 값은 '신선'하게 간주되는 초(sec), 두 번째 값은 '스테일' 상태로 데이터를 제공할 수 있는 최대 초(sec)입니다.

신선 기간(첫 번째 값 이전)에 요청하면, 바로 캐시를 반환합니다. 스테일 기간(첫 번째 값과 두 번째 값 사이)에 요청하면, 만료된 값을 사용자에게 제공하고, [지연 함수(deferred function)](/docs/master/helpers#deferred-functions)를 등록하여 응답이 끝난 후 새 값으로 캐시를 갱신합니다. 두 번째 값을 초과해서 요청하면 캐시가 만료된 것으로 간주되어 즉시 재계산하며, 이때는 사용자가 느린 응답을 경험할 수 있습니다:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제

캐시에서 항목을 가져온 후 바로 삭제하려면 `pull` 메서드를 사용할 수 있습니다. `get` 메서드와 마찬가지로, 항목이 없으면 `null`이 반환됩니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

`Cache` 파사드의 `put` 메서드를 사용하여 캐시에 항목을 저장할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

`put` 메서드에 저장 시간을 전달하지 않으면, 해당 항목은 무기한 저장됩니다:

```php
Cache::put('key', 'value');
```

정수로 초를 지정하는 대신, 만료 시점을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다:

```php
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않으면 저장

`add` 메서드는 해당 항목이 캐시 저장소에 없을 때만 추가합니다. 실제로 캐시에 항목이 추가되면 `true`, 그렇지 않으면 `false`를 반환합니다. `add` 메서드는 원자적(atomic) 연산입니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="extending-item-lifetime"></a>
### 항목 수명 연장하기

`touch` 메서드를 사용하면 기존 캐시 항목의 수명(Time-To-Live, TTL)을 연장할 수 있습니다. 캐시 항목이 존재하고 만료 시간 연장에 성공하면 `true`를 반환하고, 항목이 없으면 `false`를 반환합니다:

```php
Cache::touch('key', 3600);
```

만료 시간을 정밀하게 지정하려면 `DateTimeInterface`, `DateInterval`, `Carbon` 인스턴스를 전달할 수도 있습니다:

```php
Cache::touch('key', now()->addHours(2));
```

<a name="storing-items-forever"></a>
#### 영구적으로 항목 저장

`forever` 메서드를 사용하면 항목을 캐시에 영구적으로 저장할 수 있습니다. 이 항목들은 만료되지 않으므로, `forget` 메서드를 이용해 직접 삭제해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우, "영구"로 저장된 항목도 캐시 용량이 한계에 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드를 사용하면 캐시에서 항목을 삭제할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간을 0 또는 음수로 지정하여 항목을 삭제할 수도 있습니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

캐시 전체를 비우려면 `flush` 메서드를 사용할 수 있습니다:

```php
Cache::flush();
```

> [!WARNING]
> 캐시를 플러시하면 현재 설정된 캐시 "prefix"를 무시하고 모든 항목이 제거됩니다. 여러 애플리케이션이 캐시를 공유하고 있다면, 캐시 삭제에 주의하세요.

<a name="the-cache-helper"></a>
### 캐시 헬퍼

`Cache` 파사드를 사용하는 것 외에도, 전역 `cache` 함수를 사용해 데이터를 캐시에서 조회하거나 저장할 수 있습니다. `cache` 함수에 문자열을 하나 전달하면, 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키-값 쌍의 배열과 만료 시간을 함께 전달하면, 해당 값들을 지정된 기간 동안 캐시에 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

`cache` 함수를 인수 없이 호출하면, `Illuminate\Contracts\Cache\Factory` 구현체 인스턴스를 반환하므로, 다른 캐싱 메서드도 사용할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 글로벌 `cache` 함수 호출을 테스트할 때는 [파사드 테스트](/docs/master/mocking#mocking-facades)와 마찬가지로 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="atomic-locks"></a>
## 원자적(Atomic) 락 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 캐시 드라이버 중 하나를 사용해야 합니다. 또한, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리

원자적(Atomic) 락을 사용하면 경쟁 상태(race condition)에 대해 걱정하지 않고 분산 락을 관리할 수 있습니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)에서는 한 번에 하나의 원격 작업만 서버에서 실행되도록 보장하기 위해 원자적 락을 사용합니다. `Cache::lock` 메서드를 사용해 락을 생성하고 관리할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 락을 획득함...

    $lock->release();
}
```

`get` 메서드는 클로저도 받을 수 있습니다. 클로저 실행 후에는 Laravel이 자동으로 락을 해제합니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 10초 동안 락을 획득하고 자동 해제됨...
});
```

요청 시점에 락을 즉시 획득할 수 없는 경우, Laravel이 지정한 초만큼 대기하도록 할 수도 있습니다. 지정한 시간 내에 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

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

위 예제는 `block` 메서드에 클로저를 전달하여 더 간단하게 구현할 수도 있습니다. 이 경우 Laravel은 해당 시간만큼 락 획득을 시도하며, 클로저 실행 후 락을 자동으로 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 10초 동안 락 획득 및 자동 해제...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

때에 따라 한 프로세스에서 락을 획득하고, 다른 프로세스에서 락을 해제해야 하는 상황이 있을 수 있습니다. 예를 들어, 웹 요청 중 락을 획득하고, 해당 요청에서 트리거된 큐 작업(queued job) 끝에서 락을 해제하려 할 수 있습니다. 이런 경우, 락의 범위 내 'owner token'을 큐 작업에 전달하여, 해당 토큰으로 락을 다시 생성할 수 있습니다.

아래 예제에서는 락을 성공적으로 획득한 경우 큐 작업을 디스패치합니다. 이때 락의 owner token을 `owner` 메서드로 큐 작업에 함께 전달합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

애플리케이션의 `ProcessPodcast` 작업 내부에서는 owner token을 이용해 락을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

현재 owner와 상관없이 락을 강제로 해제하고 싶다면, `forceRelease` 메서드를 사용할 수 있습니다:

```php
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성하기

커스텀 캐시 드라이버를 만들려면 먼저 `Illuminate\Contracts\Cache\Store` [계약(Contract)](/docs/master/contracts)을 구현해야 합니다. 예를 들어, MongoDB 캐시 구현은 다음과 같이 작성할 수 있습니다:

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

각 메서드별로 MongoDB 연결을 활용해 로직을 구현하면 됩니다. 각 메서드를 어떻게 구현하는지 예제가 필요하다면, [Laravel 프레임워크 소스 코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참조하세요. 구현이 끝나면, `Cache` 파사드의 `extend` 메서드를 호출해 커스텀 드라이버 등록을 마무리합니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 두어야 할지 궁금하다면, `app` 디렉터리 내에 `Extensions` 네임스페이스를 생성해 둘 수 있습니다. 하지만 Laravel은 애플리케이션 구조가 엄격하지 않으므로, 자유롭게 구조를 조직할 수 있습니다.

<a name="registering-the-driver"></a>
### 드라이버 등록하기

커스텀 캐시 드라이버를 Laravel에 등록하려면, `Cache` 파사드의 `extend` 메서드를 사용해야 합니다. 다른 서비스 프로바이더가 `boot` 메서드에서 캐시 값을 읽으려고 시도할 수 있기 때문에, 커스텀 드라이버는 `booting` 콜백 내에서 등록하는 것이 좋습니다. `booting` 콜백을 사용하면, 서비스 프로바이더의 `boot` 메서드가 호출되기 직전이지만, 모든 프로바이더의 `register` 메서드가 호출된 이후에 커스텀 드라이버가 등록됩니다. `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에서 `booting` 콜백을 등록하면 됩니다:

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

`extend` 메서드의 첫 번째 인수는 드라이버의 이름입니다. 이는 `config/cache.php` 설정 파일의 `driver` 옵션명과 일치해야 합니다. 두 번째 인수는 반드시 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저여야 하며, 클로저에는 [서비스 컨테이너](/docs/master/container) 인스턴스인 `$app`이 전달됩니다.

확장이 등록되면, 애플리케이션의 `config/cache.php` 설정 파일 내 `CACHE_STORE` 환경 변수 또는 `default` 옵션을 확장 이름으로 변경해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

캐시 연산이 발생할 때마다 코드를 실행하고 싶다면, 캐시에서 디스패치되는 다양한 [이벤트](/docs/master/events)를 리스닝할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름 |
| --- |
| `Illuminate\Cache\Events\CacheHit` |
| `Illuminate\Cache\Events\CacheMissed` |
| `Illuminate\Cache\Events\KeyForgotten` |
| `Illuminate\Cache\Events\KeyWritten` |

</div>

성능 향상을 위해, 애플리케이션의 `config/cache.php` 설정 파일에서 특정 캐시 저장소의 `events` 설정 옵션을 `false`로 지정해 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```