# 캐시 (Cache)

- [소개](#introduction)
- [구성](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 조회](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장](#storing-items-in-the-cache)
    - [캐시에서 항목 제거](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [Cache 헬퍼](#the-cache-helper)
- [원자적(Atomic) 락](#atomic-locks)
    - [락 관리](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
- [사용자 정의 캐시 드라이버 추가](#adding-custom-cache-drivers)
    - [드라이버 작성](#writing-the-driver)
    - [드라이버 등록](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션이 수행하는 데이터 조회나 처리 작업 중 일부는 CPU 부하가 크거나 완료하는 데 몇 초 이상 걸릴 수 있습니다. 이러한 경우, 조회된 데이터를 일정 시간 동안 캐시에 저장해두면 같은 데이터를 다시 요청할 때 빠르게 가져올 수 있습니다. 캐시된 데이터는 일반적으로 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 보관됩니다.

다행히도, Laravel은 여러 캐시 백엔드를 아우르는 직관적이고 통합된 API를 제공하므로, 다양한 고속 데이터 저장소의 이점을 활용하여 웹 애플리케이션의 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 구성 (Configuration)

애플리케이션의 캐시 구성 파일은 `config/cache.php`에 위치합니다. 이 파일에서 애플리케이션 전반에서 기본적으로 사용할 캐시 저장소를 지정할 수 있습니다. Laravel은 기본적으로 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등 인기 있는 캐시 백엔드를 지원합니다. 또한 파일 기반 캐시 드라이버도 제공되며, `array` 및 `null` 캐시 드라이버는 자동화된 테스트에 유용하게 사용할 수 있습니다.

캐시 구성 파일에는 그 밖에도 다양한 옵션들이 포함되어 있으니 참고하시기 바랍니다. 기본적으로 Laravel은 `database` 캐시 드라이버를 사용하도록 설정되어 있으며, 이는 직렬화된 캐시 객체를 애플리케이션의 데이터베이스에 저장합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 경우, 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있으나, 애플리케이션에 해당 마이그레이션이 없다면 `make:cache-table` Artisan 명령어를 사용하여 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하기 위해서는 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. 모든 Memcached 서버 목록은 `config/cache.php` 구성 파일에 명시할 수 있습니다. 이 파일에는 이미 `memcached.servers` 항목이 포함되어 있습니다:

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

필요하다면 `host` 옵션을 UNIX 소켓 경로로 설정할 수 있습니다. 이때는 `port` 옵션을 `0`으로 지정해야 합니다:

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

Laravel에서 Redis 캐시를 사용하기 전에 먼저 PECL을 통해 PhpRedis PHP 확장 프로그램을 설치하거나 Composer를 통해 `predis/predis` 패키지(~2.0 버전)를 설치해야 합니다. [Laravel Sail](/docs/12.x/sail)에는 해당 확장 프로그램이 이미 포함되어 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com), [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 애플리케이션 플랫폼에는 PhpRedis 확장 프로그램이 기본 탑재되어 있습니다.

Redis 구성에 대한 자세한 내용은 [Laravel 문서 페이지](/docs/12.x/redis#configuration)를 참고하십시오.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 테이블 이름은 `cache`로 지정하지만, 실제로는 `cache` 구성 파일의 `stores.dynamodb.table` 구성 값에 따라 테이블 이름을 지정해야 합니다. 이 테이블 이름은 환경 변수 `DYNAMODB_CACHE_TABLE`로도 지정할 수 있습니다.

이 테이블에는 문자열 타입의 파티션 키가 있어야 하며, 이 이름도 애플리케이션의 `cache` 구성 파일 내 `stores.dynamodb.attributes.key` 구성 항목의 값과 일치해야 합니다. 기본적으로 파티션 키의 이름은 `key`입니다.

DynamoDB는 만료된 항목을 자동으로 제거하지 않기 때문에, 테이블에서 [TTL(Time to Live)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) 기능을 활성화해야 합니다. 테이블 TTL 설정 시, TTL 속성 이름은 `expires_at`으로 설정해야 합니다.

다음으로, AWS SDK를 설치하여 Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 합니다:

```shell
composer require aws/aws-sdk-php
```

그리고 DynamoDB 캐시 저장소의 구성 옵션값도 반드시 지정해야 합니다. 보통 `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` 등은 애플리케이션의 `.env` 구성 파일에 정의해야 합니다:

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 `mongodb` 캐시 드라이버를 제공합니다. 이 드라이버는 `mongodb` 데이터베이스 연결을 통해 구성할 수 있습니다. MongoDB는 TTL 인덱스를 지원하므로, 만료된 캐시 항목을 자동으로 삭제할 수 있습니다.

MongoDB 구성 방법에 대한 자세한 내용은 MongoDB [캐시 및 락 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하세요.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스는 `Cache` 파사드(Facade)를 통해 얻을 수 있으며, 본 문서 전체에서 이를 사용합니다. `Cache` 파사드는 Laravel 캐시 계약(Contracts)의 실제 구현을 간편하게 다룰 수 있는 직관적 API를 제공합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자를 조회합니다.
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

`Cache` 파사드의 `store` 메서드를 사용하여 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 구성 파일의 `stores` 설정 배열 내에 정의된 저장소 이름과 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 조회

캐시에서 항목을 조회할 때는 `Cache` 파사드의 `get` 메서드를 사용합니다. 해당 항목이 캐시에 없다면 `null`이 반환됩니다. 원하는 경우, 두 번째 인수에 기본값을 지정할 수 있습니다. 항목이 없을 때 해당 값이 반환됩니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저(Closure)를 전달할 수도 있습니다. 지정한 항목이 캐시에 없으면 클로저 결과가 반환됩니다. 클로저를 사용하면 데이터베이스나 외부 서비스에서 기본값을 지연 조회할 수 있습니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인

`has` 메서드는 캐시에 해당 항목이 존재하는지 확인할 수 있습니다. 이 메서드는 항목이 존재하지만 값이 `null`인 경우에도 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소

`increment`와 `decrement` 메서드를 사용하면 캐시에 저장된 정수 값의 증감이 가능합니다. 두 메서드 모두 항목 값을 얼마나 조정할지 두 번째 인수로 지정할 수 있습니다:

```php
// 값이 존재하지 않으면 초기화합니다...
Cache::add('key', 0, now()->addHours(4));

// 값 증감...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 조회 및 저장

항목을 캐시에서 조회하되, 요청한 항목이 없으면 기본값을 저장하고 싶을 때가 있습니다. 예를 들어, 모든 사용자를 캐시에서 가져오거나, 없으면 데이터베이스에서 조회한 후 캐시에 저장할 수 있습니다. 이런 경우 `Cache::remember` 메서드를 사용하면 됩니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

캐시에 항목이 없으면, `remember` 메서드에 전달된 클로저가 실행되고 결과가 캐시에 저장됩니다.

항목을 영구적으로 저장하려면 `rememberForever` 메서드를 사용합니다. 항목이 없으면 저장하고, 있다면 캐시에서 읽습니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember` 메서드를 사용할 때, 일부 사용자는 캐시 값이 만료되었을 경우 응답 속도가 느려질 수 있습니다. 일부 타입의 데이터에서는 만료된(부분적으로 오래된) 데이터를 임시로 제공하고, 백그라운드에서 캐시 값을 재계산하도록 하는 것이 유용할 수 있습니다. 이렇게 하면 일부 사용자가 캐시 갱신 과정에서 느려지는 것을 방지할 수 있습니다. 이를 "stale-while-revalidate" 패턴이라고 하며, `Cache::flexible` 메서드를 통해 이 패턴을 구현할 수 있습니다.

`flexible` 메서드는 캐시 값이 "신선"하다고 간주되는 시간과 "오래됨"으로 간주될 때까지의 시간을 배열로 받습니다. 배열의 첫 번째 값은 신선 기간(초), 두 번째 값은 오래된 데이터 제공 최대 기간(초)을 의미합니다.

- 신선 기간 내 요청: 즉시 캐시 반환, 재계산 없음
- 오래된 기간 내 요청: 사용자에게 오래된 값 반환, 응답 후 비동기적으로 캐시 재계산
- 전체 기간 초과: 캐시가 만료되어 즉시 값을 재계산 후 반환(응답이 느려질 수 있음)

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제

캐시에서 항목을 조회한 뒤 바로 삭제해야 할 경우, `pull` 메서드를 사용할 수 있습니다. `get`과 마찬가지로 항목이 없으면 `null`이 반환됩니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장

`Cache` 파사드의 `put` 메서드를 이용해 캐시에 항목을 저장할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

저장 시간을 생략할 경우, 해당 항목은 만료 없이 영구 저장됩니다:

```php
Cache::put('key', 'value');
```

만료 시간을 초 단위 정수 대신, 원하는 만료 시점을 나타내는 `DateTime` 인스턴스로도 지정할 수 있습니다:

```php
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장

`add` 메서드는 캐시에 항목이 없을 때에만 값을 추가합니다. 실제로 항목이 추가되면 `true`, 이미 존재해서 추가되지 않으면 `false`를 반환합니다. `add` 메서드는 원자적(atomic) 연산입니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 영구 저장

`forever` 메서드는 항목을 영구적으로 캐시에 저장합니다. 이 항목들은 만료되지 않으므로, `forget` 메서드를 사용해 직접 삭제해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우, 영구 저장된 항목도 캐시 용량이 꽉 차면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거

캐시에서 항목을 제거하려면 `forget` 메서드를 사용합니다:

```php
Cache::forget('key');
```

만료 시간을 0 또는 음수로 지정하여 항목을 제거할 수도 있습니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

캐시 전체를 비우려면 `flush` 메서드를 사용합니다:

```php
Cache::flush();
```

> [!WARNING]
> 캐시를 flush(비우기)하면 설정된 캐시 "prefix"를 무시하고 전체 캐시가 비워집니다. 여러 애플리케이션이 같은 캐시 저장소를 공유하는 환경에서는 반드시 신중히 처리해야 합니다.

<a name="cache-memoization"></a>
### 캐시 메모이제이션 (Cache Memoization)

Laravel의 `memo` 캐시 드라이버는 한 요청이나 작업(job) 실행 중에 조회된 캐시 값을 메모리에 임시 저장합니다. 이를 통해 동일 실행 내에서 반복적으로 동일한 캐시 키에 접근하는 경우, 실제 캐시 저장소를 여러 번 조회하지 않아 성능이 크게 향상됩니다.

메모이제이션된 캐시를 사용하려면 `memo` 메서드를 호출합니다:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드는 원한다면 캐시 저장소의 이름을 인수로 받아, 해당 저장소를 기반으로 메모이제이션을 적용할 수 있습니다:

```php
// 기본 캐시 저장소 사용
$value = Cache::memo()->get('key');

// Redis 캐시 저장소 사용
$value = Cache::memo('redis')->get('key');
```

특정 키에 대해 처음 `get`을 호출하면 실제 캐시 저장소에서 값을 조회하고, 같은 실행 내에서 반복 호출 시에는 메모리에 저장된 값을 사용합니다:

```php
// 캐시에서 직접 조회
$value = Cache::memo()->get('key');

// 캐시 저장소를 다시 조회하지 않고, 메모리에 저장된 값 반환
$value = Cache::memo()->get('key');
```

캐시 값을 변경하는 메서드(`put`, `increment`, `remember` 등)를 호출하면, 메모이제이션 값이 자동으로 초기화되고, 값 변경 동작이 실제 캐시 저장소에 위임됩니다:

```php
Cache::memo()->put('name', 'Taylor'); // 실제 캐시에 저장...
Cache::memo()->get('name');           // 실제 캐시에서 조회...
Cache::memo()->get('name');           // 메모이제이션, 캐시 조회 없음...

Cache::memo()->put('name', 'Tim');    // 메모이제이션 값 초기화, 새 값 저장...
Cache::memo()->get('name');           // 다시 실제 캐시에서 조회...
```

<a name="the-cache-helper"></a>
### Cache 헬퍼

`Cache` 파사드 외에도, 전역 함수인 `cache`를 사용해 캐시 데이터의 저장 및 조회가 가능합니다. `cache` 함수를 문자열 하나로 호출하면 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키/값 쌍의 배열과 만료 시간을 전달하면, 해당 값들이 지정한 시간 동안 캐시에 저장됩니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

인수 없이 `cache` 함수만 호출하면, `Illuminate\Contracts\Cache\Factory` 구현 인스턴스가 반환되어, 다양한 캐싱 메서드를 체이닝하여 호출할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수를 테스트할 때는, [파사드(Facade) 테스트](/docs/12.x/mocking#mocking-facades)와 마찬가지로 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="atomic-locks"></a>
## 원자적(Atomic) 락 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버 중 하나를 사용해야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리

원자적 락은 분산 환경에서 레이스 컨디션(race condition) 걱정 없이 락을 다룰 수 있게 해줍니다. 예를 들어 [Laravel Cloud](https://cloud.laravel.com)에서는 한 번에 한 서버에서만 원격 작업이 실행되도록 원자적 락을 사용합니다. 락은 `Cache::lock` 메서드로 생성 및 관리할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초간 락을 획득...

    $lock->release();
}
```

`get` 메서드는 클로저를 인수로 받을 수도 있습니다. 클로저 실행이 끝나면 Laravel이 자동으로 락을 해제합니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 10초간 락을 획득 후 자동 해제...
});
```

락을 요청했을 때 즉시 획득할 수 없는 경우, Laravel이 지정 시간(초) 동안 락을 기다리게 할 수도 있습니다. 타임아웃 내에 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

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

위 코드는 `block` 메서드에 클로저를 전달하여 더 간결하게 만들 수 있습니다. 이 경우 Laravel이 지정된 시간(초) 동안 락을 획득 시도하고, 클로저 실행 후 자동으로 락을 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 10초간 락 획득...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

가끔, 한 프로세스에서 락을 획득하고, 다른 프로세스에서 락을 해제해야 할 필요가 있을 수 있습니다. 예를 들어, 웹 요청 중 락을 획득하고, 해당 요청에서 트리거된 큐 작업의 마지막에 락을 해제하려 할 때가 있습니다. 이때는 락의 범위(owner token)를 큐 작업에 전달한 뒤, 해당 토큰으로 락을 복원해 해제합니다.

다음 예제에서는 락 획득에 성공한 경우, 큐 작업을 디스패치합니다. 이때 락의 owner 토큰을 `owner` 메서드를 통해 큐 작업에 전달합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

애플리케이션의 `ProcessPodcast` 작업 내에서는 owner 토큰을 사용해 락을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

락 소유자를 무시하고 강제로 해제하고 싶으면 `forceRelease` 메서드를 사용할 수도 있습니다:

```php
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 사용자 정의 캐시 드라이버 추가 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성

사용자 정의 캐시 드라이버를 만들기 위해서는 먼저 `Illuminate\Contracts\Cache\Store` [계약(Contract)](/docs/12.x/contracts)를 구현해야 합니다. 예를 들어, MongoDB 캐시 구현은 다음과 비슷한 형태일 수 있습니다:

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

각 메서드를 MongoDB 연결을 사용하여 구현하면 됩니다. 각 메서드의 구체적 구현 방식은 [Laravel 프레임워크 소스 코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore` 구현 예제를 참고하시면 됩니다. 구현이 끝나면, `Cache` 파사드의 `extend` 메서드를 호출하여 사용자 정의 드라이버를 완성합니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 사용자 정의 캐시 드라이버 코드를 어디에 둘지 고민된다면 `app` 디렉터리 아래에 `Extensions` 네임스페이스를 만들어 관리할 수 있습니다. 하지만, Laravel 애플리케이션 구조는 엄격히 정해진 규칙이 없으니 원하는 방식대로 자유롭게 조직화할 수 있습니다.

<a name="registering-the-driver"></a>
### 드라이버 등록

사용자 정의 캐시 드라이버를 Laravel에 등록하려면, `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더의 `boot` 메서드에서 캐시 값을 읽으려 할 수 있으므로, 사용자 정의 캐시 드라이버는 `booting` 콜백 내에서 등록합니다. `booting` 콜백은 모든 서비스 프로바이더의 `register` 메서드가 호출된 후, 각 서비스 프로바이더의 `boot` 메서드가 호출되기 직전에 실행됩니다. 아래와 같이 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `booting` 콜백을 등록할 수 있습니다:

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

`extend` 메서드의 첫 번째 인수는 드라이버의 이름입니다. 이 이름은 `config/cache.php` 구성 파일의 `driver` 옵션과 일치해야 합니다. 두 번째 인수로는 반드시 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하는 클로저를 전달해야 합니다. 이 클로저에는 [서비스 컨테이너](/docs/12.x/container) 인스턴스인 `$app`이 넘어옵니다.

확장 기능이 등록되면, 애플리케이션의 `config/cache.php` 파일에서 `CACHE_STORE` 환경 변수나 `default` 옵션을 해당 확장 이름으로 수정해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 작업 시 코드를 실행하고 싶다면, 캐시에서 발생하는 여러 [이벤트](/docs/12.x/events)를 리스너로 처리할 수 있습니다:

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

성능 향상을 위해, 애플리케이션의 `config/cache.php` 구성 파일에서 각 캐시 저장소별로 `events` 옵션을 `false`로 설정하여 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```