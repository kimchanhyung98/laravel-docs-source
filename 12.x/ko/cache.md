# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 사전 준비](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [Cache 헬퍼](#the-cache-helper)
- [캐시 태그](#cache-tags)
- [원자적 락(Atomic Locks)](#atomic-locks)
    - [락 관리](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
    - [락과 함수 실행](#locks-and-function-invocations)
- [캐시 페일오버](#cache-failover)
- [커스텀 캐시 드라이버 추가](#adding-custom-cache-drivers)
    - [드라이버 작성](#writing-the-driver)
    - [드라이버 등록](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 수행하는 일부 데이터 조회 또는 처리 작업은 CPU 사용량이 높거나 완료하는 데 몇 초가 걸릴 수 있습니다. 이런 경우, 조회한 데이터를 일정 시간 동안 캐시에 저장하여 동일한 데이터에 대한 이후 요청에서 빠르게 불러올 수 있도록 하는 것이 일반적입니다. 캐시된 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같이 매우 빠른 데이터 저장소에 저장됩니다.

Laravel은 여러 가지 캐시 백엔드에 대해 표현력 있고 통합된 API를 제공하므로, 이들의 빠른 데이터 조회 속도를 쉽게 활용하여 웹 애플리케이션의 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php` 경로에 위치합니다. 이 파일에서 애플리케이션 전반에서 기본적으로 사용할 캐시 저장소(cache store)를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등과 같은 인기 있는 캐시 백엔드를 기본적으로 지원합니다. 추가로, 파일 기반 캐시 드라이버도 사용 가능하며, `array`와 `null` 드라이버는 자동화된 테스트에 유용한 임시 캐시 백엔드를 제공합니다.

캐시 설정 파일에는 그 밖에도 다양한 옵션이 포함되어 있으니 확인해 볼 수 있습니다. 기본적으로 Laravel은 캐시 객체를 애플리케이션의 데이터베이스에 직렬화하여 저장하는 `database` 캐시 드라이버를 사용하도록 설정되어 있습니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 (Driver Prerequisites)

<a name="prerequisites-database"></a>
#### Database

`database` 캐시 드라이버를 사용할 때는 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 이 테이블은 Laravel의 기본 제공 마이그레이션인 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 만약 애플리케이션에 해당 마이그레이션이 없다면, 다음 Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하기 위해서는 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. 모든 Memcached 서버는 `config/cache.php` 설정 파일에 나열할 수 있습니다. 이미 예시로 시작할 수 있는 `memcached.servers` 항목이 포함되어 있습니다:

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

필요하다면 `host` 옵션에 UNIX 소켓 경로를 지정할 수 있으며, 이 경우 `port` 옵션은 `0`으로 설정해야 합니다:

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

Laravel에서 Redis 캐시를 사용하기 위해서는 PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer로 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/12.x/sail)에는 이미 이 확장 모듈이 포함되어 있습니다. 또한, [Laravel Cloud](https://cloud.laravel.com)나 [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 애플리케이션 플랫폼에도 기본적으로 PhpRedis 확장이 설치되어 있습니다.

Redis 설정에 대한 자세한 내용은 [Laravel Redis 문서](/docs/12.x/redis#configuration)를 참고하십시오.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 테이블 이름은 `cache`이어야 하지만, `cache` 설정 파일 내의 `stores.dynamodb.table` 값에 따라 테이블명을 정해야 합니다. 테이블명은 `DYNAMODB_CACHE_TABLE` 환경 변수로도 지정할 수 있습니다.

이 테이블에는 또한 문자열 파티션 키가 있어야 하며, 이름은 애플리케이션의 `cache` 설정 파일 내 `stores.dynamodb.attributes.key` 항목 값과 일치해야 합니다. 기본적으로 파티션 키 이름은 `key`입니다.

일반적으로 DynamoDB는 만료된 항목을 테이블에서 자동으로 제거하지 않으므로, 테이블에서 [TTL(Time to Live) 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활성화해야 합니다. 테이블의 TTL 속성 이름은 `expires_at`으로 지정해야 합니다.

다음으로, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다:

```shell
composer require aws/aws-sdk-php
```

또한, DynamoDB 캐시 저장소 설정 옵션에 필요한 값들이 제공되어야 합니다. 일반적으로 `AWS_ACCESS_KEY_ID` 및 `AWS_SECRET_ACCESS_KEY` 같은 옵션은 애플리케이션의 `.env` 설정 파일에 정의합니다:

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

MongoDB를 사용하는 경우, 공식 패키지인 `mongodb/laravel-mongodb`에서 제공하는 `mongodb` 캐시 드라이버를 사용할 수 있으며, `mongodb` 데이터베이스 연결을 이용해 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하여 만료된 캐시 항목을 자동으로 제거할 수 있습니다.

MongoDB 설정에 대한 자세한 내용은 MongoDB [Cache and Locks documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)을 참고하십시오.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드(Facade)를 사용할 수 있습니다. 이 문서 전반에 걸쳐 이 파사드를 사용할 예정입니다. `Cache` 파사드는 Laravel의 캐시 계약(Contracts) 실제 구현체에 손쉽게 접근할 수 있도록 해줍니다:

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
#### 여러 캐시 저장소 접근하기

`Cache` 파사드의 `store` 메서드를 사용하여 다양한 캐시 저장소에 접근할 수 있습니다. 이때 전달하는 키는 `cache` 설정 파일의 `stores` 구성 배열에 정의된 저장소 이름 중 하나와 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 가져올 때 사용합니다. 만약 캐시에서 항목을 찾을 수 없다면 `null`이 반환됩니다. 더욱이, 두 번째 인수로 해당 항목이 존재하지 않을 때 반환될 기본값을 지정할 수도 있습니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저(Closure)를 넘길 수도 있습니다. 해당 캐시 항목이 존재하지 않을 때, 해당 클로저의 결과가 반환됩니다. 이를 통해 데이터베이스나 외부 서비스에서 기본값을 지연 조회할 수 있습니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인

`has` 메서드를 통해 캐시에 항목이 존재하는지 확인할 수 있습니다. 값이 `null`일 경우에도 이 메서드는 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소

`increment`와 `decrement` 메서드를 사용하면 캐시의 정수형 항목 값을 조정할 수 있습니다. 두 메서드 모두 증가/감소시킬 값을 두 번째 인수로 지정할 수 있습니다:

```php
// 존재하지 않을 경우 값을 초기화...
Cache::add('key', 0, now()->plus(hours: 4));

// 값 증가 및 감소...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 가져오고 저장하기

가끔 캐시에서 항목을 가져와야 하며, 없는 경우 기본값을 저장하고 반환하고 싶을 때가 있습니다. 예를 들어, 모든 사용자 정보를 캐시에서 가져오거나, 없으면 데이터베이스에서 불러와 캐시에 추가하고 싶은 경우입니다. 이런 경우 `Cache::remember` 메서드를 사용할 수 있습니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

만약 캐시에 항목이 없다면, 전달한 클로저가 실행되고 해당 결과가 캐시에 저장됩니다.

영구적으로 저장하고 싶을 경우 `rememberForever` 메서드를 사용할 수 있습니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate(만료 후 새로고침)

`Cache::remember` 메서드를 사용할 때, 캐시된 값이 만료되면 일부 사용자가 느린 응답을 경험할 수 있습니다. 일부 데이터의 경우, 만료된 데이터를 잠시 동안 계속 제공하고, 백그라운드에서 캐시 값을 갱신하도록 하는 것이 유용할 수 있습니다. 이를 "stale-while-revalidate" 패턴이라고 하며, Laravel에서는 `Cache::flexible` 메서드로 이를 구현할 수 있습니다.

`flexible` 메서드는 캐시 값을 "신선(fresh)"하게 취급할 기간과 "stale(만료된)"로 간주되는 시점을 배열로 전달받습니다. 첫 번째 값은 신선하게 유지되는 초(second) 단위 시간, 두 번째 값은 만료된 데이터를 얼마 동안 제공할지 정의합니다.

신선한 기간(첫 번째 값) 내 요청은 즉시 캐시된 내용이 반환됩니다. 만료(stale) 기간(두 값 사이) 내 요청은 만료된 값이 일단 제공되며, 요청 응답 후에 캐시가 갱신되도록 [지연 실행 함수](/docs/12.x/helpers#deferred-functions)가 등록됩니다. 두 기간 모두 지난 경우, 캐시가 만료되어 값을 즉시 재계산하며 이때는 사용자가 느린 응답을 받게 될 수 있습니다:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 가져오고 삭제하기

캐시에서 값을 가져온 뒤 해당 항목을 즉시 삭제하고 싶다면, `pull` 메서드를 사용할 수 있습니다. 이 메서드도 항목이 없을 경우 `null`을 반환하며, 두 번째 인수로 기본값을 지정할 수 있습니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

`Cache` 파사드의 `put` 메서드를 사용해 캐시에 데이터를 저장할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

만약 저장 시간을 전달하지 않으면, 해당 항목은 만료되지 않고 영구적으로 저장됩니다:

```php
Cache::put('key', 'value');
```

만료 시간을 초 단위 정수 대신 `DateTime` 인스턴스로 전달하여, 원하는 만료 시점을 지정할 수도 있습니다:

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장

`add` 메서드는 캐시에 해당 키가 아직 존재하지 않을 때만 새로 저장합니다. 실제로 추가될 경우 `true`, 이미 존재하면 `false`를 반환하며, 이 동작은 원자적(atomic)입니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 항목을 영구 저장하기

`forever` 메서드는 만료 없이 항목을 영구적으로 캐시에 저장합니다. 이런 항목은 `forget` 메서드를 사용해 직접 삭제해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우, "영구 저장"된 항목도 캐시 크기 제한이 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드를 사용해 캐시에서 특정 항목을 삭제할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간을 0 또는 음수로 지정하여 항목을 즉시 삭제할 수도 있습니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메서드를 사용해 전체 캐시를 비울 수도 있습니다:

```php
Cache::flush();
```

> [!WARNING]
> 캐시를 flush할 경우, 설정된 캐시 "prefix"와 무관하게 모든 캐시 항목이 삭제됩니다. 다른 애플리케이션과 캐시를 공유하는 경우 주의해야 합니다.

<a name="cache-memoization"></a>
### 캐시 메모이제이션 (Cache Memoization)

Laravel의 `memo` 캐시 드라이버를 이용하면 한 번 조회된 캐시 값을 단일 요청 또는 작업 실행 중에 임시로 메모리에 저장할 수 있습니다. 이로 인해 동일한 실행 흐름에서 반복적으로 캐시에 접근할 때 성능이 크게 향상됩니다.

메모이즈된 캐시를 사용하려면 `memo` 메서드를 호출합니다:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드는 옵션으로 캐시 저장소 이름을 지정할 수 있으며, 지정한 저장소 위에 메모이즈 드라이버가 동작하게 됩니다:

```php
// 기본 캐시 저장소 사용...
$value = Cache::memo()->get('key');

// Redis 캐시 저장소 사용...
$value = Cache::memo('redis')->get('key');
```

특정 키에 대해 최초의 `get` 호출은 실제 캐시 저장소에서 값을 가져오고, 이후 동일 요청이나 작업 내에서는 메모리에서 제공됩니다:

```php
// 실제 캐시 저장소 접근...
$value = Cache::memo()->get('key');

// 캐시 접근 없이 메모리에서 반환...
$value = Cache::memo()->get('key');
```

값을 변경하는 메서드(`put`, `increment`, `remember` 등)를 호출하면 메모이즈된 값을 자동 삭제하고, 해당 작업은 하위 캐시 저장소에 위임됩니다:

```php
Cache::memo()->put('name', 'Taylor'); // 실제 저장소에 기록
Cache::memo()->get('name');           // 실제 저장소 접근
Cache::memo()->get('name');           // 메모리에서 반환

Cache::memo()->put('name', 'Tim');    // 메모이즈 값 삭제, 새 값 기록
Cache::memo()->get('name');           // 다시 실제 캐시 저장소 접근
```

<a name="the-cache-helper"></a>
### Cache 헬퍼

`Cache` 파사드 외에도, 전역 함수 `cache`를 사용해 더 간단하게 데이터를 조회하거나 저장할 수 있습니다. 문자열 한 개만 인수로 넘기면 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키-값 배열과 만료 시간을 지정하면, 지정한 기간 동안 캐시에 값을 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```

아무 인수 없이 `cache` 함수를 호출할 경우, `Illuminate\Contracts\Cache\Factory` 구현 인스턴스를 반환하여 추가적인 캐시 메서드를 사용할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수 호출을 테스트할 때도 [파사드 테스트](/docs/12.x/mocking#mocking-facades)와 마찬가지로 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그 (Cache Tags)

> [!WARNING]
> 캐시 태그는 `file`, `dynamodb`, `database` 캐시 드라이버에서 지원되지 않습니다.

<a name="storing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 저장

캐시 태그를 사용하면 관련된 여러 캐시 항목에 태그를 부여하고, 해당 태그가 지정된 모든 캐시 값을 한 번에 삭제할 수 있습니다. 정렬된 태그 이름 배열을 전달하여 캐시에 접근할 수 있습니다. 예시로, 태그를 사용해 값을 저장하는 방법은 다음과 같습니다:

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 접근

태그로 저장한 항목을 조회할 때도 동일한 순서의 태그 배열을 `tags` 메서드에 전달한 뒤, 조회할 키를 `get`에 넘겨야 합니다:

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 삭제

특정 태그 또는 태그 목록이 지정된 모든 항목을 한 번에 삭제할 수 있습니다. 아래 코드는 `people`, `authors` 중 하나라도 해당 태그가 지정된 모든 캐시를 삭제합니다. 따라서 `Anne`과 `John` 모두 삭제됩니다:

```php
Cache::tags(['people', 'authors'])->flush();
```

반대로, 아래 코드는 `authors` 태그가 있는 항목만 삭제하므로 `Anne`만 삭제되고, `John`은 남아있습니다:

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 원자적 락 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리

원자적 락을 사용하면 경쟁 상태(race condition)에 신경 쓸 필요 없이 분산 락(Distributed Lock)을 제어할 수 있습니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)는 원자적 락을 이용하여 한 번에 한 서버에서 한 원격 작업만 실행되도록 보장합니다. 다음과 같이 `Cache::lock` 메서드로 락을 생성·관리할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 락이 획득됨...

    $lock->release();
}
```

`get` 메서드는 클로저를 직접 인수로 받을 수도 있습니다. 클로저 실행 이후 락이 자동으로 해제됩니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 10초 동안 락이 획득되고, 클로저 실행 후 자동 해제...
});
```

락이 현재 획득 불가일 때 Laravel이 일정 시간 동안 대기하도록 만들 수 있습니다. 지정한 시간 내 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다:

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최장 5초 동안 기다려 락을 획득함...
} catch (LockTimeoutException $e) {
    // 락 획득 실패...
} finally {
    $lock->release();
}
```

위 예시는 `block` 메서드에 클로저를 전달하여 더 간단하게 쓸 수 있습니다. Laravel은 지정한 시간만큼 락 획득을 시도하고, 클로저 실행 후 락을 자동으로 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최장 5초 대기 후 10초 동안 락 획득...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

때때로 한 프로세스에서 락을 획득하고, 다른 프로세스에서 락을 해제해야 할 수 있습니다. 예를 들어, 웹 요청 중 락을 걸고, 이 요청에서 발생한 큐 작업이 끝날 때 락을 해제하고 싶을 수 있습니다. 이런 경우, 락의 소유자 토큰(owner token)을 큐 작업에 전달하고, 해당 토큰으로 락을 복원해 해제합니다.

예시에서, 락을 성공적으로 획득했다면, 큐 작업을 디스패치하면서 락의 토큰을 함께 전달합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

`ProcessPodcast` 큐 작업 내에서는 락의 owner 토큰을 이용해 락을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

현재 소유자를 무시하고 강제로 락을 해제하고 싶다면, `forceRelease` 메서드를 사용할 수 있습니다:

```php
Cache::lock('processing')->forceRelease();
```

<a name="locks-and-function-invocations"></a>
### 락과 함수 실행

`withoutOverlapping` 메서드는 주어진 클로저를 원자적 락을 획득한 상태로 실행하는 간결한 문법을 제공합니다. 이를 통해 전체 인프라에서 특정 작업이 오직 한 번만 동시 실행되도록 보장할 수 있습니다:

```php
Cache::withoutOverlapping('foo', function () {
    // 최장 10초 대기 후 락 획득...
});
```

기본적으로 락은 클로저 실행이 끝날 때까지 유지되며, 락 획득을 위한 대기 시간은 10초입니다. 추가 인수로 해당 값을 조정할 수 있습니다:

```php
Cache::withoutOverlapping('foo', function () {
    // 최장 5초 대기, 락은 120초 유지...
}, lockFor: 120, waitFor: 5);
```

지정한 대기 시간 내 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

<a name="cache-failover"></a>
## 캐시 페일오버 (Cache Failover)

`failover` 캐시 드라이버를 사용하면 캐시 장애 발생 시 자동으로 다음 저장소로 전환하는 기능을 제공합니다. 즉, `failover` 저장소의 기본 캐시 저장소가 어떤 이유로든 실패할 경우, Laravel은 자동으로 다음에 지정한 저장소를 사용하려 시도합니다. 이는 운영 환경에서 캐시 신뢰성이 매우 중요한 경우 가용성을 보장하는데 특히 유용합니다.

페일오버 캐시 저장소를 설정하려면, `failover` 드라이버와 시도할 저장소 이름 배열을 지정합니다. Laravel은 기본적으로 애플리케이션의 `config/cache.php` 설정 파일에 예시 구성을 포함하고 있습니다:

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

페일오버 기능을 사용하려면, `.env` 파일에서 기본 캐시 저장소를 `failover`로 설정해야 합니다:

```ini
CACHE_STORE=failover
```

캐시 저장소 동작이 실패하여 페일오버가 작동될 때, Laravel은 `Illuminate\Cache\Events\CacheFailedOver` 이벤트를 디스패치합니다. 이 이벤트를 감지해 캐시 오류를 보고하거나 기록할 수 있습니다.

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성

커스텀 캐시 드라이버를 만들기 위해서는 먼저 `Illuminate\Contracts\Cache\Store` [컨트랙트](/docs/12.x/contracts)를 구현해야 합니다. 예를 들어, MongoDB 캐시 구현체는 다음과 같은 형태가 될 수 있습니다:

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

각 메서드는 MongoDB 연결을 이용해 구현하면 됩니다. 각 메서드의 구현 예시는 [Laravel 프레임워크의 `Illuminate\Cache\MemcachedStore` 소스코드](https://github.com/laravel/framework)를 참고할 수 있습니다. 구현을 마친 후, `Cache` 파사드의 `extend` 메서드를 호출해 커스텀 드라이버의 등록을 마칩니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 두어야 할지 궁금하다면, `app` 디렉토리 안에 `Extensions` 네임스페이스를 만들어 관리할 수 있습니다. 하지만 Laravel은 엄격한 애플리케이션 구조를 강제하지 않으니 자유롭게 구성해도 좋습니다.

<a name="registering-the-driver"></a>
### 드라이버 등록

커스텀 캐시 드라이버를 Laravel에 등록하려면 `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더의 `boot` 메서드에서 캐시 값을 읽으려 할 수 있으므로, 등록은 `booting` 콜백에서 해주는 것이 좋습니다. `booting` 콜백을 사용하면, 서비스 프로바이더들의 `register` 메서드 실행 후, `boot` 메서드가 호출되기 직전에 커스텀 드라이버가 등록됩니다. 아래 예시는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에서 `booting` 콜백을 등록하는 모습입니다:

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

`extend` 메서드의 첫 번째 인자는 드라이버 이름이며, 이는 `config/cache.php`에서 `driver` 옵션과 일치해야 합니다. 두 번째 인자는 반드시 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하는 클로저이며, 이 클로저에는 [서비스 컨테이너](/docs/12.x/container) 인스턴스 `$app`이 전달됩니다.

확장 등록이 완료되면, 환경 변수 `CACHE_STORE` 또는 `config/cache.php`의 `default` 옵션을 커스텀 드라이버 이름으로 변경하세요.

<a name="events"></a>
## 이벤트 (Events)

캐시 동작이 일어날 때마다 특정 코드를 실행하려면, 캐시가 디스패치하는 다양한 [이벤트](/docs/12.x/events)를 구독할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                    |
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

성능을 높이기 위해, 특정 캐시 저장소의 `events` 설정 옵션을 `config/cache.php`에서 `false`로 지정하여 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
