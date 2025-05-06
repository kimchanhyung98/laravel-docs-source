# 캐시(Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 필수조건](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 아이템 조회](#retrieving-items-from-the-cache)
    - [캐시에 아이템 저장](#storing-items-in-the-cache)
    - [캐시에서 아이템 제거](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [캐시 헬퍼](#the-cache-helper)
- [원자적 락](#atomic-locks)
    - [락 관리](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가](#adding-custom-cache-drivers)
    - [드라이버 구현](#writing-the-driver)
    - [드라이버 등록](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

애플리케이션이 수행하는 데이터 조회나 처리 작업 중 일부는 CPU를 많이 소모하거나 완료까지 몇 초가 걸릴 수 있습니다. 이럴 때는 조회된 데이터를 일정 시간 동안 캐시에 저장해 두고, 동일한 데이터를 다시 요청할 때 빠르게 응답할 수 있도록 하는 것이 일반적입니다. 캐시된 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히, Laravel은 다양한 캐시 백엔드에 대해 표현력 있고 통합된 API를 제공하므로, 이들의 매우 빠른 데이터 조회 속도를 쉽게 활용하여 웹 애플리케이션의 속도를 향상시킬 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치해 있습니다. 이 파일에서 애플리케이션 전체에서 기본적으로 사용할 캐시 저장소를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등 다양한 인기 있는 캐싱 백엔드를 기본으로 지원합니다. 이 밖에도 파일 기반 캐시 드라이버가 제공되며, `array`와 `null` 캐시 드라이버는 자동화된 테스트에 유용한 캐시 백엔드를 제공합니다.

캐시 설정 파일에는 이 외에도 다양한 옵션들이 포함되어 있으니 참고하시기 바랍니다. 기본적으로 Laravel은 애플리케이션 데이터베이스에 직렬화된 캐시 객체를 저장하는 `database` 캐시 드라이버로 설정되어 있습니다.

<a name="driver-prerequisites"></a>
### 드라이버 필수조건

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 경우, 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 이것은 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/{{version}}/migrations)에 포함되어 있습니다. 만약 애플리케이션에 이 마이그레이션이 없다면, 다음 Artisan 명령어를 사용하여 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. `config/cache.php` 설정 파일에 Memcached 서버들을 나열할 수 있습니다. 이 파일에는 이미 시작을 위한 `memcached.servers` 항목이 포함되어 있습니다:

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

필요하다면 `host` 옵션을 UNIX 소켓 경로로 설정할 수 있습니다. 이 경우 `port` 옵션은 반드시 `0`이어야 합니다:

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

Laravel에서 Redis 캐시를 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer로 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/{{version}}/sail)에는 이미 이 확장 모듈이 포함되어 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com) 및 [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 호스팅 플랫폼에서는 기본적으로 PhpRedis 확장 모듈이 설치되어 있습니다.

Redis 설정에 대한 자세한 정보는 [Laravel 공식 문서](/docs/{{version}}/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 캐시 데이터를 저장할 DynamoDB 테이블을 먼저 생성해야 합니다. 이 테이블의 기본 이름은 `cache`입니다. 하지만, 테이블 이름은 `cache` 설정 파일의 `stores.dynamodb.table` 설정값에 따라야 하며, `DYNAMODB_CACHE_TABLE` 환경 변수로도 지정할 수 있습니다.

이 테이블에는 또한 파티션 키로 문자열 타입의 필드가 필요하며, 이름은 `cache` 설정 파일 내의 `stores.dynamodb.attributes.key` 값과 일치해야 합니다. 기본적으로 이 파티션 키의 이름은 `key`입니다.

일반적으로 DynamoDB는 만료된 아이템을 자동으로 삭제하지 않습니다. 따라서 테이블에 대해 [Time to Live(TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활성화해야 합니다. TTL 속성의 이름은 `expires_at`으로 설정하세요.

그런 다음, Laravel 애플리케이션에서 DynamoDB와 통신할 수 있도록 AWS SDK를 설치하세요:

```shell
composer require aws/aws-sdk-php
```

또한 DynamoDB 캐시 저장소의 설정 옵션이 모두 환경변수로 제공되는지 확인해야 합니다. 일반적으로 `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` 같은 옵션은 애플리케이션의 `.env` 파일에 정의합니다:

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 `mongodb` 캐시 드라이버가 제공되며, `mongodb` 데이터베이스 연결을 통해 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하며, 이를 활용하여 만료된 캐시 항목을 자동으로 삭제할 수 있습니다.

MongoDB 설정에 대한 자세한 내용은 MongoDB [Cache and Locks 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하시기 바랍니다.

<a name="cache-usage"></a>
## 캐시 사용법

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드를 사용할 수 있으며, 본 문서 전체에서 이를 사용할 예정입니다. `Cache` 파사드는 Laravel 캐시 계약(contracts)의 실제 구현체에 간결하게 접근할 수 있도록 제공합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 표시합니다.
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

`Cache` 파사드를 사용하여 `store` 메서드를 통해 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달되는 키는 `cache` 설정 파일의 `stores` 배열에 나열된 저장소와 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분 동안 저장
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 아이템 조회

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 검색하는 데 사용됩니다. 캐시에 항목이 없으면 `null`이 반환됩니다. 필요하다면, 두 번째 인자를 `get` 메서드에 전달해 기본값을 지정할 수 있습니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값에 클로저를 전달할 수도 있습니다. 지정한 항목이 캐시에 없으면 이 클로저의 결과가 반환됩니다. 클로저를 전달하면 데이터베이스 등에서 기본값을 지연 평가해 가져올 수 있습니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인

`has` 메서드는 항목이 캐시에 존재하는지 확인하는 데 사용됩니다. 항목이 존재하나 값이 `null`이면 이 메서드는 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소

`increment`와 `decrement` 메서드는 캐시에 저장된 정수 값의 증감을 수행합니다. 두 메서드는 증감할 값(두 번째 인자)을 지정할 수 있습니다:

```php
// 값이 없으면 초기화
Cache::add('key', 0, now()->addHours(4));

// 값 증감
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 조회 및 저장

때로는 캐시에서 항목을 조회하되, 요청한 항목이 없으면 기본값 역시 저장하고 싶을 수 있습니다. 예를 들어, 전체 사용자를 캐시에서 가져오거나, 캐시에 없다면 데이터베이스에서 조회 후 캐시에 저장하는 경우입니다. 이는 `Cache::remember` 메서드로 구현할 수 있습니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

캐시에 항목이 없으면, `remember`에 전달된 클로저가 실행되어 결과가 캐시에 저장됩니다.

`rememberForever` 메서드를 사용하면, 항목이 없을 때 캐시에 영구적으로 저장하거나, 이미 있으면 가져옵니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate (Stale-While-Revalidate)

`Cache::remember` 메서드를 사용할 때, 캐시 값이 만료되면 일부 사용자가 느린 응답을 경험할 수 있습니다. 특정 데이터 유형에 대해서는, 캐시 값이 백그라운드에서 다시 계산되는 동안 일시적으로 만료된(stale) 데이터를 제공하여 일부 사용자가 느린 응답을 겪지 않도록 하는 것이 유용할 수 있습니다. 이를 "stale-while-revalidate" 패턴이라 하며, `Cache::flexible` 메서드가 이 패턴을 구현합니다.

`flexible` 메서드는 캐시 값이 "신선한" 기간과 "stale"로 간주되는 기간을 지정하는 배열을 받습니다. 배열의 첫 번째 값은 캐시가 신선하게 유지되는 초, 두 번째 값은 캐시가 만료(갱신 필요)되기 전까지 스테일 데이터로 제공될 수 있는 기간(초)을 의미합니다.

신선(duration 내) 기간에는 캐시를 즉시 반환합니다. 스테일 기간이면, 사용자에게 만료된 캐시 값을 반환하되, 사용자에게 응답을 보낸 후 백그라운드에서 새 값을 재계산합니다. 두 번째 값이 지난 뒤에는 캐시가 완전히 만료되어 새 값을 바로 계산합니다(사용자 응답이 느려질 수 있습니다):

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 및 삭제

캐시에서 항목을 조회한 뒤 삭제하려면 `pull` 메서드를 사용할 수 있습니다. 항목이 없으면 `null`이 반환됩니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 아이템 저장

캐시에 항목을 저장하려면 `Cache` 파사드의 `put` 메서드를 사용합니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

만약 `put` 메서드에 저장 시간을 지정하지 않으면, 영구적으로 저장됩니다:

```php
Cache::put('key', 'value');
```

seconds 대신 `DateTime` 인스턴스를 전달하여 만료시간을 지정할 수도 있습니다:

```php
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장

`add` 메서드는 캐시에 값이 없을 때만 항목을 저장합니다. 이미 존재한다면 저장되지 않고 false를 반환합니다. `add` 메서드는 원자적 작업(atomic operation)입니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 영구적으로 저장

`forever` 메서드는 항목을 영구적으로 캐시에 저장할 때 사용합니다. 이런 값은 만료되지 않으므로 반드시 `forget` 메서드로 직접 제거해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버에서 "forever"로 저장된 항목은, 캐시가 용량에 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 아이템 제거

`forget` 메서드를 사용해 캐시에서 값을 삭제할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간을 0 또는 음수로 주어도 동일하게 삭제됩니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메서드로 전체 캐시를 삭제할 수도 있습니다:

```php
Cache::flush();
```

> [!WARNING]
> 캐시를 플러시하면 설정한 캐시 "prefix"를 무시하고 모든 항목이 제거됩니다. 다른 애플리케이션과 캐시를 공유하는 경우 주의해서 사용하세요.

<a name="cache-memoization"></a>
### 캐시 메모이제이션

Laravel의 `memo` 캐시 드라이버는 하나의 요청 또는 작업 실행 동안, 이미 조회한 캐시 값을 메모리에 임시로 저장할 수 있습니다. 이는 같은 실행 내에서 캐시 접근이 반복될 때 성능을 크게 향상시킵니다.

메모이제이션 캐시를 사용하려면 `memo` 메서드를 호출하세요:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드는 추가적으로 캐시 저장소의 이름을 인자로 받아, 어떤 실제 캐시 저장소 위에 덮어쓸지 지정할 수도 있습니다:

```php
// 기본 캐시 저장소 사용
$value = Cache::memo()->get('key');

// Redis 캐시 저장소 사용
$value = Cache::memo('redis')->get('key');
```

특정 키에 대해 첫 번째 `get` 호출은 실제 캐시에서 값을 읽지만, 같은 실행 컨텍스트 내에서 두 번째 이후 호출은 메모리에서 값을 가져옵니다:

```php
// 실제 캐시 접근
$value = Cache::memo()->get('key');

// 실제 캐시 접근하지 않고 메모이제이션된 값 반환
$value = Cache::memo()->get('key');
```

값을 변경하는 메서드(`put`, `increment`, `remember` 등)를 호출하면, 메모이제이션 캐시는 해당 키를 잊고, 실제 캐시 저장소에 작업을 위임합니다:

```php
Cache::memo()->put('name', 'Taylor'); // 실제 캐시에 저장
Cache::memo()->get('name');           // 실제 캐시 접근
Cache::memo()->get('name');           // 메모이제이션, 실제 캐시 접근 안 함

Cache::memo()->put('name', 'Tim');    // 메모이제이션 값 제거, 값 새로 저장
Cache::memo()->get('name');           // 실제 캐시 접근 다시 수행
```

<a name="the-cache-helper"></a>
### 캐시 헬퍼

`Cache` 파사드 외에도, 전역 `cache` 함수를 사용해 데이터를 저장하고 조회할 수 있습니다. `cache` 함수에 문자열 하나를 전달하면 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키/값 쌍의 배열과 만료 시간을 전달하면, 해당 동안 값을 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

`cache` 함수를 인자 없이 호출하면, `Illuminate\Contracts\Cache\Factory`의 인스턴스를 반환하여 다양한 캐시 메서드를 사용할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 글로벌 `cache` 함수 호출을 테스트할 땐, [파사드 테스트](/docs/{{version}}/mocking#mocking-facades)에서처럼 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="atomic-locks"></a>
## 원자적 락(Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array`를 사용해야 합니다. 또한 모든 서버가 같은 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리

원자적 락은 분산 락을 레이스 컨디션 걱정 없이 관리할 수 있도록 합니다. 예를 들어 [Laravel Cloud](https://cloud.laravel.com)는 서버에서 한 번에 한 개만 원격 작업이 실행되도록 보장하기 위해 원자 락을 사용합니다. `Cache::lock` 메서드를 통해 락을 생성하고 관리할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 락 획득

    $lock->release();
}
```

`get` 메서드는 클로저도 받을 수 있으며, 클로저 실행 후 락이 자동 해제됩니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 10초 동안 락 획득, 실행 후 자동 해제
});
```

락이 사용중이라 획득할 수 없을 경우, Laravel에 지정한 초(최대 대기 시간)만큼 락 획득을 기다리게 할 수 있습니다. 제한 시간 내에 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다:

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최대 5초 기다린 후 락 획득
} catch (LockTimeoutException $e) {
    // 락 획득 실패
} finally {
    $lock->release();
}
```

위의 예제는 block 메서드에 클로저를 전달함으로써 더 간단하게 작성할 수 있습니다. 이 경우 지정한 시간 동안 락을 시도해서 락을 획득하면 클로저 실행 후 자동으로 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 기다린 후 10초 동안 락 획득
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

가끔 락을 한 프로세스에서 획득하고, 다른 프로세스(예: 큐 작업)에서 해제해야 할 수도 있습니다. 예를 들어, 웹 요청 중에 락을 획득하고 요청에 따라 트리거된 큐 작업의 마지막에 락을 해제하고 싶을 때가 있습니다. 이 때는, 락의 "owner 토큰"을 큐 작업에 함께 전달하여 주어진 토큰으로 락을 재생성할 수 있습니다.

아래 예제는 락 획득에 성공하면 큐 작업을 디스패치하고, 락 소유자 토큰은 락의 `owner` 메서드로 전달합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

`ProcessPodcast` 작업 내에서는 owner 토큰을 사용해 락을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

현재 소유자를 무시하고 락을 해제하려면 `forceRelease` 메서드를 사용할 수 있습니다:

```php
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가

<a name="writing-the-driver"></a>
### 드라이버 구현

커스텀 캐시 드라이버를 만들려면 `Illuminate\Contracts\Cache\Store` [계약](/docs/{{version}}/contracts)를 구현해야 합니다. 예를 들어 MongoDB 캐시 구현은 다음과 같습니다:

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

각 메서드를 MongoDB 연결을 사용해 구현하면 됩니다. 각 메서드의 구현 방법은 [Laravel 프레임워크 소스코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고하세요. 구현이 완료되면, `Cache` 파사드의 `extend` 메서드로 커스텀 드라이버를 최종 등록할 수 있습니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 내에 `Extensions` 네임스페이스를 만들어 둘 수 있습니다. 하지만 Laravel은 엄격한 디렉토리 구조를 강제하지 않으니 자유롭게 구성할 수 있습니다.

<a name="registering-the-driver"></a>
### 드라이버 등록

Laravel에 커스텀 캐시 드라이버를 등록하려면, `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 자신의 `boot` 메서드에서 캐시 값을 읽을 수도 있으므로, 커스텀 드라이버의 등록은 `booting` 콜백 안에서 처리합니다. 이렇게 하면 모든 서비스 프로바이더의 `register` 메서드가 호출된 후, `boot` 전에 드라이버가 등록됩니다.

이 콜백은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 안에 추가합니다:

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

`extend` 메서드의 첫 번째 인자는 드라이버 이름으로, `config/cache.php`의 `driver` 옵션에서 사용됩니다. 두 번째 인자는 반드시 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하는 클로저이며, 인자로는 [서비스 컨테이너](/docs/{{version}}/container) 인스턴스($app)가 전달됩니다.

등록이 끝나면 애플리케이션의 `CACHE_STORE` 환경 변수나 `config/cache.php` 파일의 `default` 옵션을 이 확장 이름으로 변경하세요.

<a name="events"></a>
## 이벤트

모든 캐시 작업 시 코드를 실행하고 싶다면, 캐시에서 발생하는 다양한 [이벤트](/docs/{{version}}/events)를 리스닝할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                   |
|-----------------------------------------------|
| `Illuminate\Cache\Events\CacheFlushed`        |
| `Illuminate\Cache\Events\CacheFlushing`       |
| `Illuminate\Cache\Events\CacheHit`            |
| `Illuminate\Cache\Events\CacheMissed`         |
| `Illuminate\Cache\Events\ForgettingKey`       |
| `Illuminate\Cache\Events\KeyForgetFailed`     |
| `Illuminate\Cache\Events\KeyForgotten`        |
| `Illuminate\Cache\Events\KeyWriteFailed`      |
| `Illuminate\Cache\Events\KeyWritten`          |
| `Illuminate\Cache\Events\RetrievingKey`       |
| `Illuminate\Cache\Events\RetrievingManyKeys`  |
| `Illuminate\Cache\Events\WritingKey`          |
| `Illuminate\Cache\Events\WritingManyKeys`     |

</div>

성능을 높이기 위해, 애플리케이션의 `config/cache.php`에서 특정 캐시 저장소에 대해 `events` 옵션을 `false`로 설정하면 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
