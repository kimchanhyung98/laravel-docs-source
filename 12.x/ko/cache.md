# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 사전 준비사항](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 아이템 조회하기](#retrieving-items-from-the-cache)
    - [캐시에 아이템 저장하기](#storing-items-in-the-cache)
    - [캐시에서 아이템 제거하기](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [캐시 헬퍼](#the-cache-helper)
- [원자적 락(Atomic Locks)](#atomic-locks)
    - [락 관리](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
- [사용자 정의 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성](#writing-the-driver)
    - [드라이버 등록](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 수행하는 데이터 조회나 처리 작업 중 일부는 CPU 연산이 많이 필요하거나, 완료까지 몇 초가 걸릴 수도 있습니다. 이런 경우, 한 번 조회된 데이터를 일정 시간 동안 캐시에 저장하여, 이후 동일한 데이터 요청 시 더 빠르게 응답할 수 있습니다. 캐시된 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히도 Laravel은 다양한 캐시 백엔드를 위한 통합 API를 제공하여, 이러한 고속 데이터 조회의 이점을 활용하고 웹 애플리케이션의 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일 내에서 애플리케이션 전반에서 기본으로 사용할 캐시 저장소(cache store)를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스 등 널리 쓰이는 캐싱 백엔드를 기본 지원합니다. 또한 파일 기반 캐시 드라이버도 제공되며, `array`와 `null` 캐시 드라이버는 자동화된 테스트 시 편리하게 사용할 수 있습니다.

캐시 설정 파일엔 이 외에도 다양한 옵션이 포함되어 있으니 참고하시기 바랍니다. 기본적으로 Laravel은 애플리케이션 데이터베이스에 직렬화된 캐시 오브젝트를 저장하는 `database` 캐시 드라이버로 설정되어 있습니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비사항

<a name="prerequisites-database"></a>
#### Database

`database` 캐시 드라이버를 사용할 때는 캐시 데이터를 담을 데이터베이스 테이블이 필요합니다. 이 테이블은 보통 Laravel의 기본 마이그레이션 파일인 `0001_01_01_000001_create_cache_table.php`에 포함되어 있습니다([데이터베이스 마이그레이션 참고](/docs/12.x/migrations)). 만약 애플리케이션에 해당 마이그레이션이 없다면, `make:cache-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. 모든 Memcached 서버는 `config/cache.php` 설정 파일에 나열할 수 있습니다. 해당 파일에는 이미 예시로 `memcached.servers` 항목이 있습니다:

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

필요하다면 `host` 옵션을 UNIX 소켓 경로로 설정할 수 있습니다. 이때 `port` 옵션은 `0`으로 지정해야 합니다:

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

Laravel에서 Redis 캐시를 사용하려면, PECL을 통한 PhpRedis PHP 확장자를 설치하거나 Composer로 `predis/predis` 패키지(~2.0) 중 하나를 설치해야 합니다. [Laravel Sail](/docs/12.x/sail)에는 이미 이 확장자가 포함되어 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com), [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 애플리케이션 플랫폼에서도 기본적으로 PhpRedis 확장자가 설치되어 있습니다.

Redis 설정에 관한 자세한 내용은 [Laravel Redis 문서](/docs/12.x/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 캐시 데이터를 저장할 DynamoDB 테이블을 먼저 생성해야 합니다. 보통 테이블 이름은 `cache`로 지정하면 되지만, 실제 이름은 `cache` 설정 파일의 `stores.dynamodb.table` 설정값을 따라야 합니다. 또는 `DYNAMODB_CACHE_TABLE` 환경 변수로도 테이블명을 지정할 수 있습니다.

테이블에는 파티션 키로 사용할 문자열 타입의 컬럼이 필요하며, 컬럼명은 `cache` 설정 파일의 `stores.dynamodb.attributes.key` 설정값을 따릅니다. 기본적으로 이 키 컬럼명은 `key`입니다.

일반적으로 DynamoDB는 만료된 항목을 테이블에서 자동으로 삭제하지 않으니, [Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) 기능을 활성화해야 합니다. 테이블의 TTL 속성명을 지정할 때는 `expires_at`으로 설정하세요.

다음으로, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다:

```shell
composer require aws/aws-sdk-php
```

아울러 DynamoDB 캐시 저장소의 설정 옵션에 필요한 값을 할당해야 하며, 대개 이러한 옵션(`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` 등)은 애플리케이션의 `.env` 파일에서 정의합니다:

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

MongoDB를 사용할 경우, 공식 패키지인 `mongodb/laravel-mongodb`를 통한 `mongodb` 캐시 드라이버를 사용할 수 있으며, 이는 `mongodb` 데이터베이스 연결 설정을 통해 구성할 수 있습니다. MongoDB는 TTL 인덱스를 지원해, 만료된 캐시 아이템을 자동으로 삭제할 수 있습니다.

MongoDB 설정에 대한 자세한 내용은 [MongoDB 캐시 및 락 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참조하세요.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면, 이 문서 전체에서 사용할 `Cache` 파사드를 활용하면 됩니다. `Cache` 파사드는 Laravel 캐시 컨트랙트의 다양한 구현체에 대해 간결하게 접근할 수 있도록 해줍니다:

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

`Cache` 파사드의 `store` 메서드를 사용하면 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일 내 `stores` 배열에 등록된 저장소 중 하나여야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 아이템 조회하기

`Cache` 파사드의 `get` 메서드를 사용해 캐시에서 아이템을 조회할 수 있습니다. 만약 해당 아이템이 캐시에 존재하지 않으면 `null`이 반환됩니다. 필요하다면, 두 번째 인수로 기본값을 지정할 수도 있습니다. 아이템이 없을 때 이 값이 반환됩니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저를 전달할 수도 있습니다. 만약 요청한 아이템이 없을 경우, 클로저의 반환값이 기본값으로 사용됩니다. 클로저를 이용하면, 데이터베이스나 외부 서비스로부터 기본값을 느리게(필요할 때만) 조회할 수 있습니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 아이템 존재 여부 확인

`has` 메서드를 사용해 캐시에 아이템이 존재하는지 확인할 수 있습니다. 이 메서드는 해당 키가 존재하지만 값이 `null`인 경우에도 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소

캐시에 저장된 정수값을 조정하려면 `increment` 및 `decrement` 메서드를 사용할 수 있습니다. 두 메서드 모두 두 번째 인수로 증가 또는 감소시킬 값을 지정할 수 있습니다:

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
#### 조회 또는 저장

캐시에서 아이템을 조회하고, 만약 존재하지 않으면 기본값을 저장하고 반환하고 싶을 때가 있습니다. 예를 들어, 사용자 목록을 조회하되, 캐시에 없으면 DB에서 조회 후 캐시에 저장하고 싶을 때 사용할 수 있습니다. 이런 경우에는 `Cache::remember` 메서드를 사용합니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

아이템이 캐시에 존재하지 않으면, `remember` 메서드에 전달한 클로저가 실행되고, 그 반환값이 캐시에 저장됩니다.

아이템을 영구히(만료 없이) 저장하거나 반환하려면, `rememberForever` 메서드를 사용하면 됩니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember` 메서드를 사용할 때, 캐시된 값이 만료되면 일부 사용자는 응답 속도가 느려지는 상황이 발생할 수 있습니다. 일부 데이터의 경우, 캐시 값이 백그라운드에서 갱신되는 동안 다소 오래된 데이터를 제공하는 것이 유용할 수 있습니다. 이를 통해 모든 사용자가 캐시 갱신 시 느린 응답을 경험하지 않게 할 수 있습니다. 이 패턴을 "stale-while-revalidate"라 하며, `Cache::flexible` 메서드로 구현할 수 있습니다.

`flexible` 메서드는 캐시가 "신선"한 시간과 "stale"로 제공될 수 있는 시간 구간을 배열로 전달받습니다. 첫 번째 값은 캐시가 신선하다고 간주되는 기간(초), 두 번째 값은 stale 데이터로 제공될 수 있는 기간(초)입니다.

- 신선 기간 내에 요청이 오면 즉시 캐시를 반환합니다.
- stale 기간엔 캐시된 오래된 값을 제공하고, [deferred function](/docs/12.x/helpers#deferred-functions)을 등록해 응답 후 캐시를 갱신합니다.
- 두 번째 값을 지나면 캐시가 만료된 것으로 간주하고, 즉시 값을 다시 계산하기 때문에 사용자가 느린 응답을 경험할 수 있습니다.

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제

캐시에서 아이템을 읽은 뒤 바로 삭제하려면 `pull` 메서드를 사용합니다. 아이템이 존재하지 않으면 `get`과 마찬가지로 `null`이 반환됩니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 아이템 저장하기

`Cache` 파사드의 `put` 메서드를 사용해 캐시에 아이템을 저장할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

만약 저장 시간을 전달하지 않으면, 해당 아이템은 만료 없이 영구적으로 저장됩니다:

```php
Cache::put('key', 'value');
```

저장할 시간(만료 시간)을 정수(초) 대신 `DateTime` 인스턴스로도 지정할 수 있습니다:

```php
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 이미 존재하지 않을 때만 저장

`add` 메서드는 해당 아이템이 캐시에 없는 경우에만 저장을 시도합니다. 실제로 캐시에 추가되면 `true`를 반환하며, 이미 존재하는 경우엔 `false`를 반환합니다. 이 메서드는 원자적 연산(atomic operation)입니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 아이템 영구 저장

`forever` 메서드를 사용하면 아이템을 캐시에 영구적으로 저장할 수 있습니다. 이러한 아이템은 만료되지 않으므로, 캐시에서 직접 삭제(`forget` 메서드)해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용할 경우, "영구"로 저장된 아이템이라 하더라도 캐시 용량이 가득 차면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 아이템 제거하기

`forget` 메서드를 사용해 캐시에서 특정 아이템을 제거할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간을 0이나 음수로 지정하면, 해당 아이템을 즉시 제거할 수도 있습니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

전체 캐시를 비우려면 `flush` 메서드를 사용하세요:

```php
Cache::flush();
```

> [!WARNING]
> 캐시를 flush(전체 삭제)할 때는 별도로 설정한 캐시 "prefix"가 적용되지 않으므로, 모든 엔트리가 삭제됩니다. 여러 애플리케이션에서 캐시를 공유하는 환경이라면 사용에 각별히 주의해야 합니다.

<a name="cache-memoization"></a>
### 캐시 메모이제이션

Laravel의 `memo` 캐시 드라이버를 사용하면, 한 요청 또는 하나의 작업 실행 내에서 캐시 결과값을 임시로 메모리 상에 저장할 수 있습니다. 이를 통해 같은 실행 흐름에서 중복된 캐시 조회를 피하고, 성능을 크게 향상할 수 있습니다.

메모이제이즈된 캐시를 사용하려면 `memo` 메서드를 호출하세요:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드는 선택적으로 캐시 저장소 이름을 지정할 수 있습니다. 이는 메모이제이션 드라이버가 어떤 캐시 저장소를 감쌀지 지정하는 역할입니다:

```php
// 기본 캐시 저장소 사용
$value = Cache::memo()->get('key');

// Redis 캐시 저장소 사용
$value = Cache::memo('redis')->get('key');
```

같은 키에 대해 첫 `get` 호출은 실제 캐시 저장소에서 값을 가져오지만, 이후 동일 실행 내의 추가 호출들은 메모리에 저장된 값을 사용합니다:

```php
// 캐시 저장소에서 조회함
$value = Cache::memo()->get('key');

// 이후는 캐시 저장소를 조회하지 않고 메모이제이션된 값 반환
$value = Cache::memo()->get('key');
```

캐시 값을 변경(예: `put`, `increment`, `remember` 등)하는 메서드를 호출하면, 내부적으로 메모이제이션 값을 초기화한 뒤, 변경 작업을 실제 캐시 저장소에 위임합니다:

```php
Cache::memo()->put('name', 'Taylor'); // 실제 캐시에 기록
Cache::memo()->get('name');           // 실제 캐시에서 조회
Cache::memo()->get('name');           // 메모이제이션 값 반환

Cache::memo()->put('name', 'Tim');    // 메모이제이션 값 초기화 및 새 값 기록
Cache::memo()->get('name');           // 다시 실제 캐시에 접근
```

<a name="the-cache-helper"></a>
### 캐시 헬퍼

`Cache` 파사드 외에도, 전역 함수인 `cache`를 사용해 캐시 데이터에 접근하거나 저장할 수 있습니다. `cache` 함수에 문자열 하나를 인수로 전달하면 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키/값 쌍을 배열로 묶어 만료 시간과 함께 전달하면, 지정한 기간 동안 값을 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

`cache` 함수를 인수 없이 호출하면, `Illuminate\Contracts\Cache\Factory` 구현 인스턴스를 반환하므로, 다른 캐시 메서드도 사용할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수 호출을 테스트할 때는 [`Cache` 파사드 테스트 방법](/docs/12.x/mocking#mocking-facades)과 마찬가지로 `Cache::shouldReceive` 메서드를 사용하면 됩니다.

<a name="atomic-locks"></a>
## 원자적 락(Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 합니다. 또한, 모든 서버는 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리

원자적 락(atomic lock)을 사용하면, 경쟁 상태(race condition)에 신경 쓰지 않고 분산 락을 안전하게 제어할 수 있습니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)에서는 한 번에 하나의 원격 작업만 서버에서 실행되도록 원자적 락을 사용합니다. 락은 `Cache::lock` 메서드로 생성하고 제어할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초간 락 획득됨...

    $lock->release();
}
```

`get` 메서드는 클로저를 인수로 받아 락을 획득한 후 클로저를 실행하고, 실행이 끝나면 락을 자동으로 해제할 수도 있습니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 10초간 락 획득 후 자동 해제...
});
```

락이 요청 시점에 바로 사용 불가할 경우, Laravel에게 정해진 시간만큼 대기하게 할 수 있습니다. 제한 시간 내 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다:

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최대 5초 대기 후 락 획득
} catch (LockTimeoutException $e) {
    // 락 획득 실패...
} finally {
    $lock->release();
}
```

위 코드는 `block` 메서드에 클로저를 전달해 더 간단하게 작성할 수 있습니다. 클로저를 전달하면, 지정한 시간 동안 락 시도를 하고, 클로저 실행 후 락이 자동으로 해제됩니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 락 획득, 10초간 유지...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

때때로 한 프로세스에서 락을 획득하고, 다른 프로세스에서 해제해야 할 필요가 있습니다. 예컨대 웹 요청 중 락을 획득해 놓고, 그 요청에서 트리거된 큐 작업의 마지막에 락을 해제하려는 경우가 있습니다. 이럴 때는 락 스코프의 "owner token"을 큐 작업에 전달해, 해당 작업에서 같은 토큰을 사용해 락을 복원하고 해제할 수 있습니다.

아래 예시에서는 락을 성공적으로 획득하면 큐 작업을 디스패치하며, 락의 owner 토큰을 `owner` 메서드로 큐 작업에 전달합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

애플리케이션의 `ProcessPodcast` 작업(job) 내에서는 owner 토큰을 사용해 락을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

현재 owner를 무시하고 락을 해제하려면 `forceRelease` 메서드를 사용할 수 있습니다:

```php
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 사용자 정의 캐시 드라이버 추가하기 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성

사용자 정의 캐시 드라이버를 만들려면, 먼저 `Illuminate\Contracts\Cache\Store` [컨트랙트](/docs/12.x/contracts)를 구현해야 합니다. 예를 들어 MongoDB용 캐시 드라이버는 다음과 같이 작성할 수 있습니다:

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

각 메서드를 MongoDB 연결을 통해 직접 구현해주면 됩니다. 각 메서드의 자세한 구현 예시는 [Laravel 프레임워크 소스의 `Illuminate\Cache\MemcachedStore`](https://github.com/laravel/framework)를 참고하세요. 구현이 끝나면, 사용자 정의 드라이버를 등록하기 위해 `Cache` 파사드의 `extend` 메서드를 호출하면 됩니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 사용자 정의 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 내에 `Extensions` 네임스페이스를 만들어서 관리할 수 있습니다. Laravel은 애플리케이션 구조에 대해 엄격한 규칙이 없으니, 원하는 대로 구성할 수 있습니다.

<a name="registering-the-driver"></a>
### 드라이버 등록

사용자 정의 캐시 드라이버를 Laravel에 등록하려면 `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 자신의 `boot` 메서드에서 캐시 값을 읽을 수도 있으므로, 사용자 정의 드라이버는 `boot` 직전에 등록해야 안전합니다. 이를 위해 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `booting` 콜백을 사용합니다:

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

`extend` 메서드의 첫 번째 인자는 드라이버 이름입니다. 이 값은 `config/cache.php` 설정 파일의 `driver` 옵션과 일치해야 합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저이며, 클로저에는 [서비스 컨테이너](/docs/12.x/container) 인스턴스인 `$app`이 주입됩니다.

확장 기능을 등록한 후, 애플리케이션의 `.env` 파일의 `CACHE_STORE` 환경 변수 또는 `config/cache.php`의 `default` 옵션을 해당 확장 드라이버 이름으로 업데이트합니다.

<a name="events"></a>
## 이벤트 (Events)

캐시 연산이 일어날 때마다 특정 코드를 실행하려면, 캐시에서 발생하는 다양한 [이벤트](/docs/12.x/events)를 리스닝할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                     |
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

성능 향상이 필요하다면, 애플리케이션의 `config/cache.php` 내 특정 캐시 저장소의 `events` 옵션을 `false`로 설정하여 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
