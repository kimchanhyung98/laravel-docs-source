# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [Cache 헬퍼 함수](#the-cache-helper)
- [캐시 태그](#cache-tags)
- [원자적(Atomic) 락](#atomic-locks)
    - [락 관리하기](#managing-locks)
    - [프로세스 간 락 관리하기](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 수행하는 데이터 조회나 처리 작업 중 일부는 CPU를 많이 사용하거나 완료하는 데 몇 초가 걸릴 수도 있습니다. 이럴 경우, 조회한 데이터를 일정 시간 동안 캐싱하여 동일한 데이터가 다시 요청될 때 빠르게 응답할 수 있도록 하는 것이 일반적입니다. 캐시된 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히 Laravel은 다양한 캐시 백엔드에 대해 표현력이 뛰어난 통합 API를 제공하여, 이들의 빠른 데이터 조회 속도를 쉽게 활용할 수 있으며 웹 애플리케이션의 성능을 향상시킬 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서 애플리케이션 전역에서 기본적으로 사용할 캐시 저장소(store)를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등 인기 있는 캐시 백엔드를 기본적으로 지원합니다. 또한 파일 기반 캐시 드라이버도 제공되며, `array`, `null` 캐시 드라이버는 자동화된 테스트 시에 편리하게 사용할 수 있는 캐시 백엔드를 제공합니다.

캐시 설정 파일에는 이 외에도 다양한 옵션이 있으니 필요에 맞게 확인해 보시기 바랍니다. 기본적으로 Laravel은 `database` 캐시 드라이버를 사용하도록 설정되어 있으며, 이 경우 직렬화된(Serialized) 캐시 객체가 애플리케이션의 데이터베이스에 저장됩니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항 (Driver Prerequisites)

<a name="prerequisites-database"></a>
#### 데이터베이스 (Database)

`database` 캐시 드라이버를 사용할 때는 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 이 테이블은 보통 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 만약 애플리케이션에 해당 마이그레이션이 없다면, `make:cache-table` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. 사용하려는 Memcached 서버들을 `config/cache.php` 설정 파일에 나열할 수 있습니다. 이 파일에는 이미 시작하기 위한 `memcached.servers` 항목이 준비되어 있습니다.

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

필요하다면 `host` 옵션에 UNIX 소켓 경로를 설정할 수도 있습니다. 이 경우, `port` 옵션은 `0`으로 지정해야 합니다.

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

Laravel에서 Redis 캐시를 사용하려면 PECL을 통해 PhpRedis PHP 확장(extension)을 설치하거나 Composer를 통해 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/12.x/sail)에는 이미 이 확장이 포함되어 있습니다. 또한, [Laravel Cloud](https://cloud.laravel.com) 및 [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 애플리케이션 플랫폼에는 기본적으로 PhpRedis 확장이 설치되어 있습니다.

Redis 설정에 대한 자세한 내용은 [Laravel 문서의 Redis 페이지](/docs/12.x/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 먼저 생성해야 합니다. 이 테이블의 이름은 보통 `cache`여야 하지만, 실제로는 `cache` 설정 파일 내 `stores.dynamodb.table` 설정값을 참고하여 지정해야 합니다. 테이블 이름은 `DYNAMODB_CACHE_TABLE` 환경 변수로도 지정할 수 있습니다.

이 테이블에는 분할 키(partition key)로 사용할 문자열(String) 타입의 키가 필요하며, 이름은 애플리케이션의 `cache` 설정 파일 내 `stores.dynamodb.attributes.key` 값과 일치해야 합니다. 기본적으로 분할 키 이름은 `key`로 지정되어 있습니다.

DynamoDB는 기본적으로 만료된 항목을 테이블에서 자동으로 제거하지 않습니다. 따라서, [Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) 기능을 테이블에 활성화해야 합니다. TTL 속성명은 `expires_at`으로 지정하는 것이 좋습니다.

다음으로, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

또한 DynamoDB 캐시 저장소의 설정 옵션에도 값이 올바르게 입력되어 있는지 확인해야 합니다. 보통 `AWS_ACCESS_KEY_ID`와 `AWS_SECRET_ACCESS_KEY`와 같은 옵션은 애플리케이션의 `.env` 파일에 정의해야 합니다.

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지가 제공하는 `mongodb` 캐시 드라이버를 사용할 수 있으며, `mongodb` 데이터베이스 연결을 통해 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하므로, 만료된 캐시 항목을 자동으로 제거할 수 있습니다.

MongoDB 설정에 대한 자세한 내용은 MongoDB [Cache and Locks 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하세요.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기 (Obtaining a Cache Instance)

캐시 저장소 인스턴스를 얻으려면, 문서 전체에서 사용할 `Cache` 파사드(Facade)를 사용할 수 있습니다. `Cache` 파사드는 Laravel 캐시 계약의 실제 구현에 대해 편리하고 간결한 접근을 제공합니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * Show a list of all users of the application.
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

`Cache` 파사드를 사용하여 `store` 메서드로 다양한 캐시 저장소에 접근할 수 있습니다. 이때 전달하는 키는 `cache` 설정 파일의 `stores` 배열에 정의된 저장소 중 하나여야 합니다.

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기 (Retrieving Items From the Cache)

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 가져올 때 사용합니다. 해당 항목이 캐시에 없다면 `null`이 반환됩니다. 필요하다면 `get` 메서드의 두 번째 인수로 항목이 없을 때 반환할 기본값도 지정할 수 있습니다.

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저(Closure)를 전달할 수도 있습니다. 지정한 항목이 없다면 클로저가 실행되어 그 결과가 반환됩니다. 이를 통해, 예를 들어 데이터베이스나 외부 서비스에서 기본값을 지연하여 조회할 수 있습니다.

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 판단

`has` 메서드를 사용하여 특정 항목이 캐시에 존재하는지 확인할 수 있습니다. 만약 항목은 있지만 값이 `null`이라면, 이 메서드도 `false`를 반환합니다.

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소 (Incrementing / Decrementing Values)

정수(Integer) 항목의 값을 조정하려면 `increment` 및 `decrement` 메서드를 사용할 수 있습니다. 두 메서드 모두 두 번째 인수로 얼마만큼 값을 증감할지 지정할 수 있습니다.

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
#### 항목 조회 및 저장

가끔은 캐시에서 항목을 조회하는 동시에, 원하는 항목이 없으면 값을 저장하고 싶을 수 있습니다. 예를 들어, 모든 사용자를 캐시에서 조회하거나, 없을 경우 데이터베이스에서 조회한 뒤 캐시에 저장할 수 있습니다. 이때 `Cache::remember` 메서드를 사용할 수 있습니다.

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

항목이 캐시에 없으면, `remember` 메서드에 전달한 클로저가 실행되고 해당 결과가 캐시에 저장됩니다.

`rememberForever` 메서드를 사용하면 항목을 영구적으로 조회하거나, 없으면 영구적으로 캐시에 저장할 수 있습니다.

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember` 메서드를 사용할 때, 캐시 값이 만료된 경우 일부 사용자는 느린 응답을 경험하게 될 수 있습니다. 일부 데이터 타입에서는, 만료된 데이터도 임시로 제공하고 그 동안 백그라운드에서 캐시 값을 재계산하면 더 나은 사용자 경험을 제공할 수 있습니다. 이러한 패턴을 "stale-while-revalidate"라고 하며, Laravel은 이를 위한 `Cache::flexible` 메서드를 제공합니다.

`flexible` 메서드는 캐시가 "신선"한 기간과 "stale"(부분적으로 만료) 상태로 허용될 기간을 배열로 전달받아 지정합니다. 배열의 첫 번째 값은 캐시가 신선한 기간(초), 두 번째 값은 만료 이후 여전히 사용할 수 있는 기간(초)입니다.

- 신선 기간 내 요청 시: 즉시 캐시 값 반환, 재계산 없음
- stale 기간 내 요청 시: 만료된 값 제공, 사용자에게 응답 후 재계산 작업 등록
- 만료 이후 요청 시: 즉시 새로운 데이터로 재계산, 사용자는 느린 응답을 받을 수 있음

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제

캐시에서 항목을 가져온 뒤 즉시 삭제하려면, `pull` 메서드를 사용할 수 있습니다. 항목이 캐시에 없으면 `null`을 반환합니다.

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기 (Storing Items in the Cache)

캐시에 항목을 저장하려면 `Cache` 파사드의 `put` 메서드를 사용합니다.

```php
Cache::put('key', 'value', $seconds = 10);
```

저장 시간을 전달하지 않으면, 해당 항목은 무기한(영구적)으로 저장됩니다.

```php
Cache::put('key', 'value');
```

정수(초) 대신, 캐시 값의 만료 시간을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다.

```php
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때에만 저장

`add` 메서드는 항목이 캐시에 없을 때에만 항목을 추가합니다. 항목이 실제로 추가되면 `true`, 이미 존재해서 추가하지 않았다면 `false`를 반환합니다. `add` 메서드는 원자적(Atomic) 연산입니다.

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 항목 영구 저장

`forever` 메서드를 사용하면 항목을 만료 없이(영구적으로) 캐시에 저장할 수 있습니다. 이런 항목은 반드시 `forget` 메서드를 사용하여 수동으로 삭제해야 합니다.

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우 "영구" 저장된 항목도 저장소 용량 제한이 초과되면 제거될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기 (Removing Items From the Cache)

`forget` 메서드를 사용하여 캐시에서 항목을 삭제할 수 있습니다.

```php
Cache::forget('key');
```

만료 시간을 0 또는 음수로 설정하는 방식으로도 항목을 삭제할 수 있습니다.

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메서드를 사용하면 전체 캐시를 비울 수 있습니다.

```php
Cache::flush();
```

> [!WARNING]
> 캐시 플러시는 설정된 캐시 "prefix"를 고려하지 않으므로, 해당 캐시 내 모든 항목이 삭제됩니다. 여러 애플리케이션이 캐시를 공유하는 경우 플러시 사용에 각별히 주의하세요.

<a name="cache-memoization"></a>
### 캐시 메모이제이션 (Cache Memoization)

Laravel의 `memo` 캐시 드라이버는 하나의 요청 또는 작업 실행 중에 조회된 캐시 값을 임시로 메모리에 저장합니다. 이를 통해 동일한 실행 내에서 반복적으로 캐시에 접근할 때 실제 저장소를 여러 번 조회하지 않아 성능이 크게 향상됩니다.

메모이제이션된 캐시를 사용하려면 `memo` 메서드를 호출하세요.

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드에는 옵션으로 캐시 저장소 이름을 지정할 수도 있습니다. 이 이름에 해당하는 실제 캐시 저장소를 메모이제이션 드라이버가 감싸서 동작합니다.

```php
// 기본 캐시 저장소 사용
$value = Cache::memo()->get('key');

// Redis 캐시 저장소 사용
$value = Cache::memo('redis')->get('key');
```

특정 키에 대한 첫 번째 `get` 호출은 실제 캐시 저장소에 접근하지만, 같은 요청이나 작업 내에서 이후 호출은 메모리에서 값을 반환합니다.

```php
// 캐시 저장소 접근
$value = Cache::memo()->get('key');

// 캐시 접근 없이 메모리에서 반환
$value = Cache::memo()->get('key');
```

`put`, `increment`, `remember` 등 값을 변경하는 메서드를 호출하면, 메모이제이션된 값은 자동 제거되고, 변경 메서드는 실제 캐시 저장소에 위임됩니다.

```php
Cache::memo()->put('name', 'Taylor'); // 실제 저장소에 기록
Cache::memo()->get('name');           // 실제 저장소 접근
Cache::memo()->get('name');           // 메모리에서 반환

Cache::memo()->put('name', 'Tim');    // 메모이제이션 값 제거, 새로운 값 기록
Cache::memo()->get('name');           // 실제 저장소에 다시 접근
```

<a name="the-cache-helper"></a>
### Cache 헬퍼 함수 (The Cache Helper)

`Cache` 파사드 대신, 전역 `cache` 함수를 통해서도 캐시 데이터의 조회 및 저장이 가능합니다. `cache` 함수에 문자열 하나만 전달하면 해당 키의 값을 반환합니다.

```php
$value = cache('key');
```

키-값 배열과 만료 시간을 전달하면, 해당 데이터를 지정한 기간만큼 캐시에 저장합니다.

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

인수가 없이 `cache` 함수를 호출하면, `Illuminate\Contracts\Cache\Factory` 구현 인스턴스를 반환하여 캐시의 다양한 메서드를 호출할 수 있습니다.

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수 호출을 테스트할 때도 [파사드 테스트](/docs/12.x/mocking#mocking-facades)처럼 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그 (Cache Tags)

> [!WARNING]
> 캐시 태그는 `file`, `dynamodb`, `database` 캐시 드라이버에서 지원되지 않습니다.

<a name="storing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 저장

캐시 태그 기능을 이용하면, 서로 연관된 항목에 태그를 붙여 특정 태그가 부여된 모든 캐시 값을 한 번에 비울 수 있습니다. 태그는 이름이 지정된 배열로 전달하여 사용할 수 있습니다. 예를 들어, 아래와 같이 태그로 구분하여 값을 저장할 수 있습니다.

```
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 접근

태그를 사용해 저장한 항목은 동일한 태그 목록을 사용해서만 접근 가능합니다. 항목 조회 시, 동일한 순서의 태그 배열을 `tags` 메서드로 전달한 뒤, 해당 키로 `get` 메서드를 호출합니다.

```
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 제거

특정 태그(들)가 부여된 모든 항목을 비울 수 있습니다. 아래 예시는 `people` 또는 `authors` 태그가 있는 모든 캐시 데이터를 제거합니다. 따라서 `Anne`과 `John` 모두 캐시에서 삭제됩니다.

```
Cache::tags(['people', 'authors'])->flush();
```

반면, 아래의 코드는 `authors` 태그가 지정된 값만 삭제하므로, `Anne`만 제거되고 `John`은 남아 있습니다.

```
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 원자적(Atomic) 락 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리하기 (Managing Locks)

원자적 락(atomic lock)을 사용하면 경쟁 조건(race condition) 걱정 없이 분산 락을 조작할 수 있습니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)에서는 서버에서 한 번에 하나의 원격 작업만 실행되도록 원자적 락을 사용합니다. 락은 `Cache::lock` 메서드로 생성 및 관리할 수 있습니다.

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 락이 10초간 획득됨...

    $lock->release();
}
```

`get` 메서드는 클로저를 인수로 받아 실행 후 자동으로 락을 해제할 수도 있습니다.

```php
Cache::lock('foo', 10)->get(function () {
    // 락을 10초간 획득하고 자동 해제...
});
```

락을 요청했을 때 즉시 사용할 수 없다면, Laravel이 정해진 시간(초) 동안 대기하도록 할 수 있습니다. 해당 시간 내 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

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

위 예시는 `block` 메서드에 클로저를 전달하여 더욱 간단하게 구현할 수 있습니다. 지정된 시간만큼 락을 대기하며, 클로저 실행 후 자동으로 락을 해제합니다.

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초간 대기 후 10초 락 획득 및 자동 해제...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리하기 (Managing Locks Across Processes)

하나의 프로세스에서 락을 획득한 뒤, 다른 프로세스에서 해당 락을 해제하고 싶을 수도 있습니다. 예를 들어, 웹 요청 중에 락을 획득하고, 후속 큐 작업이 해당 락을 해제하는 경우가 있습니다. 이때 락의 범위 "owner 토큰"을 큐 작업에 전달하고, 주어진 토큰으로 락을 복원(재생성)하여 해제할 수 있습니다.

아래 예시는 락을 성공적으로 획득하면 큐 작업을 디스패치하고, 락의 owner 토큰을 큐 작업에 함께 전달하는 방법입니다.

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

큐 작업 `ProcessPodcast` 내부에서는 owner 토큰으로 락을 복원한 뒤 해제하면 됩니다.

```php
Cache::restoreLock('processing', $this->owner)->release();
```

락의 현재 owner를 무시하고 강제로 해제하려면 `forceRelease` 메서드를 사용할 수 있습니다.

```php
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성하기 (Writing the Driver)

커스텀 캐시 드라이버를 만들려면 우선 `Illuminate\Contracts\Cache\Store` [계약(Contract)](/docs/12.x/contracts)을 구현해야 합니다. 예를 들어, MongoDB 기반의 캐시 스토어는 아래와 같이 작성할 수 있습니다.

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

이 각 메서드를 MongoDB와 연동하여 구현하면 됩니다. 각 메서드 구현 예시는 [Laravel 프레임워크 소스코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고하면 좋습니다. 구현이 끝나면, `Cache` 파사드의 `extend` 메서드를 통해 커스텀 드라이버를 등록합니다.

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 두어야 할지 고민된다면, `app` 디렉터리 내에 `Extensions` 네임스페이스를 새로 만들어 넣을 수 있습니다. Laravel 애플리케이션 구조는 유연하므로 필요에 맞게 자유롭게 구조화해도 무방합니다.

<a name="registering-the-driver"></a>
### 드라이버 등록하기 (Registering the Driver)

커스텀 캐시 드라이버는 `Cache` 파사드의 `extend` 메서드에서 등록할 수 있습니다. 다른 서비스 프로바이더에서 `boot` 메서드 내에서 캐시 값을 읽으려고 할 수 있으므로, `booting` 콜백 내에 커스텀 드라이버 등록 코드를 작성하는 것이 좋습니다. 이렇게 하면, 모든 서비스 프로바이더의 `register` 메서드가 실행된 뒤, 각 서비스 프로바이더의 `boot` 메서드 직전에 드라이버 등록이 이루어집니다. 아래 예시는 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에서 `booting` 콜백을 등록하는 방법입니다.

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
     * Register any application services.
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
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // ...
    }
}
```

`extend` 메서드의 첫 번째 인수는 드라이버의 이름입니다. 이 값은 설정 파일인 `config/cache.php`의 `driver` 옵션 값과 일치해야 합니다. 두 번째 인수는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저입니다. 이 클로저에는 `$app` 인스턴스, 즉 [서비스 컨테이너](/docs/12.x/container) 인스턴스가 전달됩니다.

확장 드라이버가 등록되면, `CACHE_STORE` 환경 변수나 애플리케이션의 `config/cache.php` 파일 내 `default` 옵션을 확장 드라이버 이름으로 변경해 주어야 합니다.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 작업마다 코드를 실행하려면, 캐시에서 발생하는 다양한 [이벤트](/docs/12.x/events)를 리스닝(감지)할 수 있습니다.

<div class="overflow-auto">

| 이벤트명 (Event Name)                          |
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

성능을 높이기 위해, 애플리케이션의 `config/cache.php` 설정 파일에서 `events` 옵션을 `false`로 지정하여 특정 캐시 저장소에 대해 캐시 이벤트를 비활성화할 수 있습니다.

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
