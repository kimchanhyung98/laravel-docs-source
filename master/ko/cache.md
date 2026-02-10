# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 조회하기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [항목의 수명 연장](#extending-item-lifetime)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [Cache 헬퍼](#the-cache-helper)
- [캐시 태그](#cache-tags)
- [원자적 락](#atomic-locks)
    - [락 관리하기](#managing-locks)
    - [프로세스 간 락 관리하기](#managing-locks-across-processes)
    - [락과 함수 호출](#locks-and-function-invocations)
- [캐시 장애 조치](#cache-failover)
- [사용자 정의 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션이 수행하는 데이터 조회나 처리 작업 중 일부는 CPU 사용량이 높거나 완료까지 몇 초가 걸릴 수 있습니다. 이러한 경우, 조회된 데이터를 일정 시간 동안 캐시에 저장하여 동일한 데이터에 대한 후속 요청 시 신속하게 응답하는 것이 일반적입니다. 캐시된 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 보관됩니다.

Laravel은 다양한 캐시 백엔드에 대해 직관적이고 통합된 API를 제공하므로, 이러한 빠른 데이터 조회 기능을 활용하여 웹 애플리케이션의 속도를 크게 높일 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서 애플리케이션 전체에 기본적으로 사용할 캐시 저장소(cache store)를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등 인기 있는 캐시 백엔드를 기본으로 지원합니다. 또한 파일 기반 캐시 드라이버도 제공되며, `array`와 `null` 드라이버는 자동화된 테스트에서 편리하게 사용할 수 있습니다.

캐시 설정 파일에는 검토할 수 있는 다양한 옵션이 포함되어 있습니다. 기본적으로, Laravel은 `database` 캐시 드라이버를 사용하도록 설정되어 있으며, 이는 직렬화된 캐시 객체를 애플리케이션의 데이터베이스에 저장합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항 (Driver Prerequisites)

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 때는, 캐시 데이터를 보관할 데이터베이스 테이블이 필요합니다. 이 테이블은 일반적으로 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/master/migrations)에 포함되어 있습니다. 만약 애플리케이션에 해당 마이그레이션 파일이 없다면, `make:cache-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. 모든 Memcached 서버는 `config/cache.php` 파일에서 설정할 수 있습니다. 이 파일에는 시작할 수 있도록 `memcached.servers` 항목이 이미 포함되어 있습니다:

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

필요하다면, `host` 옵션을 UNIX 소켓 경로로 지정할 수도 있습니다. 이 경우엔, `port` 옵션을 `0`으로 설정해야 합니다:

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

Laravel에서 Redis 캐시를 사용하려면, PECL을 통해 PhpRedis PHP 확장 프로그램을 설치하거나 Composer를 통해 `predis/predis` 패키지(~2.0)을 설치해야 합니다. [Laravel Sail](/docs/master/sail)에는 이 확장 프로그램이 이미 포함되어 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com)와 [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 애플리케이션 플랫폼도 기본적으로 PhpRedis 확장 프로그램이 설치되어 있습니다.

Redis 설정에 대한 자세한 내용은 [Laravel 문서의 Redis 관련 페이지](/docs/master/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하려면, 먼저 모든 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 이 테이블 이름은 `cache`여야 하지만, `cache` 설정 파일의 `stores.dynamodb.table` 설정 값에 따라 다릅니다. 이 테이블 이름은 `DYNAMODB_CACHE_TABLE` 환경 변수로도 지정할 수 있습니다.

이 테이블에는 문자열 파티션 키가 있어야 하며, 키 이름은 애플리케이션의 `cache` 설정 파일에 있는 `stores.dynamodb.attributes.key` 값과 일치해야 합니다. 기본적으로 이 파티션 키는 `key`로 지정되어 있습니다.

일반적으로 DynamoDB는 만료된 항목을 테이블에서 자동으로 제거하지 않습니다. 따라서 테이블에서 [Time to Live(TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활성화해야 합니다. 테이블의 TTL 설정에서는 TTL 속성 이름을 `expires_at`으로 지정하세요.

그 다음, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다:

```shell
composer require aws/aws-sdk-php
```

또한, DynamoDB 캐시 저장소 설정 옵션 값을 반드시 제공해야 합니다. 일반적으로 `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` 등과 같은 옵션은 애플리케이션의 `.env` 설정 파일에 정의해야 합니다:

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 제공하는 `mongodb` 캐시 드라이버를 사용할 수 있으며, `mongodb` 데이터베이스 연결로 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하여, 만료된 캐시 항목을 자동으로 제거할 수 있습니다.

MongoDB 설정에 대한 자세한 내용은 MongoDB [Cache and Locks documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)을 참고하세요.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기 (Obtaining a Cache Instance)

캐시 저장소 인스턴스를 얻으려면, `Cache` 파사드를 사용할 수 있습니다. 이 문서 전체에서 `Cache` 파사드를 활용할 예정입니다. `Cache` 파사드는 Laravel의 캐시 계약(contracts)의 기본 구현에 대해 간결하고 편리한 접근을 제공합니다:

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

`Cache` 파사드를 사용하면 `store` 메서드를 통해 여러 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일의 `stores` 배열에 나열된 저장소 중 하나와 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 조회하기 (Retrieving Items From the Cache)

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 조회하는 데 사용됩니다. 항목이 캐시에 존재하지 않으면 `null`이 반환됩니다. 필요하다면 `get` 메서드에 두 번째 인수를 전달해, 항목이 없을 때 반환할 기본값을 지정할 수 있습니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저를 전달할 수도 있습니다. 지정한 항목이 캐시에 없으면 클로저의 실행 결과가 반환됩니다. 클로저를 사용하면 데이터베이스나 외부 서비스에서 기본값을 지연 조회할 수 있습니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목의 존재 여부 확인

`has` 메서드는 캐시 항목의 존재 여부를 확인하는 데 사용할 수 있습니다. 이 메서드는 항목이 존재하지만 값이 `null`인 경우에도 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소

`increment` 및 `decrement` 메서드는 캐시에 저장된 정수형 항목의 값을 조정할 때 사용합니다. 두 메서드 모두 증가/감소할 값을 두 번째 인수로 전달할 수 있습니다:

```php
// 값이 존재하지 않으면 초기화...
Cache::add('key', 0, now()->plus(hours: 4));

// 값 증가 또는 감소...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 조회 및 저장

간혹 캐시에서 항목을 조회하는 동시에, 요청한 항목이 없으면 기본값을 저장하고 싶을 수 있습니다. 예를 들어, 모든 사용자를 캐시에서 조회하거나 없으면 데이터베이스에서 가져와 캐시에 저장하려 할 수 있습니다. 이를 위해 `Cache::remember` 메서드를 사용할 수 있습니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

항목이 캐시에 존재하지 않으면, `remember` 메서드에 전달된 클로저가 실행되고 그 결과가 캐시에 저장됩니다.

항목을 영구적으로 저장하거나 없을 때만 가져오는 용도로는 `rememberForever` 메서드를 사용할 수 있습니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember` 메서드 사용 시, 일부 사용자는 캐시 값이 만료된 경우 응답 지연을 겪을 수 있습니다. 일부 데이터의 경우, 캐시된 값이 백그라운드에서 재계산되는 동안 약간 오래된(stale) 데이터를 임시로 제공하여, 사용자 대다수가 느린 응답을 겪지 않도록 하는 것이 유용할 수 있습니다. 이를 "stale-while-revalidate" 패턴이라 하며, `Cache::flexible` 메서드가 이 방식을 제공합니다.

`flexible` 메서드는 캐시 값이 "신선"하다고 여기는 시간과 "stale" 상태로 제공 가능한 기간을 배열로 전달받습니다. 첫 번째 값은 신선한 상태의 시간(초), 두 번째 값은 stale 상태로 제공할 수 있는 최대 시간(초)입니다.

신선 기간(첫 번째 값 이내)에 요청하면 즉시 캐시 값을 반환합니다. stale 기간(두 값 사이)에 요청하면, 사용자에게는 오래된 데이터가 반환되고, 응답 이후에 [지연 함수](/docs/master/helpers#deferred-functions)가 등록되어 캐시 값이 백그라운드에서 새로고침됩니다. 두 번째 값(최대 시간)을 초과한 시점에 요청이 들어오면, 캐시가 만료된 것으로 간주되어 즉시 값을 재계산(느린 응답 가능)합니다:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제

캐시에서 항목을 조회한 후 해당 항목을 바로 제거해야 할 경우, `pull` 메서드를 사용하세요. `get` 메서드와 마찬가지로 항목이 없다면 `null`이 반환됩니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기 (Storing Items in the Cache)

`Cache` 파사드의 `put` 메서드를 사용해 캐시에 항목을 저장할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

저장 시간(초)을 지정하지 않으면, 해당 항목은 무기한 저장됩니다:

```php
Cache::put('key', 'value');
```

정수 대신 캐시 만료 시간을 지정하려면, `DateTime` 인스턴스를 전달할 수도 있습니다:

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장

`add` 메서드는 항목이 이미 캐시에 없다면 해당 값을 저장합니다. 항목이 실제로 추가되었다면 `true`를 반환하고, 아닐 경우엔 `false`를 반환합니다. `add` 메서드는 원자적(atomic) 동작을 합니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="extending-item-lifetime"></a>
### 항목의 수명 연장 (Extending Item Lifetime)

`touch` 메서드를 사용하면 기존 캐시 항목의 수명(Time To Live, TTL)을 연장할 수 있습니다. 캐시 항목이 존재하고, 그 만료 시간이 성공적으로 연장되면 `true`를 반환합니다. 항목이 없다면 `false`를 반환합니다:

```php
Cache::touch('key', 3600);
```

정확한 만료 시간을 지정하고 싶다면 `DateTimeInterface`, `DateInterval`, 또는 `Carbon` 인스턴스를 전달할 수 있습니다:

```php
Cache::touch('key', now()->addHours(2));
```

<a name="storing-items-forever"></a>
#### 영구적으로 항목 저장

`forever` 메서드는 항목을 영구적으로 캐시에 저장합니다. 이런 항목은 절대 만료되지 않으므로, 직접 `forget` 메서드로 수동 삭제해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우, "영구 저장"된 항목도 캐시 크기 제한에 도달했을 때 제거될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기 (Removing Items From the Cache)

`forget` 메서드로 캐시에서 항목을 제거할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간을 0 또는 음수로 지정해 저장하면 항목이 바로 제거됩니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메서드를 사용하면 전체 캐시를 비울 수 있습니다:

```php
Cache::flush();
```

> [!WARNING]
> 캐시를 flush할 경우, 설정된 캐시 "prefix"와는 무관하게 모든 항목이 삭제됩니다. 여러 애플리케이션이 캐시를 공유하는 환경에서는 이 점을 꼭 고려하십시오.

<a name="cache-memoization"></a>
### 캐시 메모이제이션 (Cache Memoization)

Laravel의 `memo` 캐시 드라이버는 한 요청 또는 작업 실행 도중, 이미 조회된 캐시 값을 메모리에 임시 저장합니다. 이로 인해 같은 실행 환경 내에서 반복적인 캐시 접근을 크게 줄여 성능이 향상됩니다.

메모이제이션을 사용하려면 `memo` 메서드를 호출합니다:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드는 메모이제이션 드라이버가 감싸야 할 기본 캐시 저장소 이름을 선택적으로 인수로 받을 수 있습니다:

```php
// 기본 캐시 저장소를 사용
$value = Cache::memo()->get('key');

// Redis 캐시 저장소를 사용할 때
$value = Cache::memo('redis')->get('key');
```

같은 key에 대해 첫 번째 `get` 호출만 실제 캐시 저장소를 조회하고, 같은 요청 혹은 작업 내의 재호출은 메모리에서 바로 반환됩니다:

```php
// 캐시 조회 발생
$value = Cache::memo()->get('key');

// 캐시 미조회, 메모리에서 반환
$value = Cache::memo()->get('key');
```

캐시 값을 변경하는 메서드(`put`, `increment`, `remember` 등)를 호출하면, 메모이제이션 값이 자동으로 잊혀지고 실제 캐시 저장소에 변경이 이루어집니다:

```php
Cache::memo()->put('name', 'Taylor'); // 실제 캐시에 저장
Cache::memo()->get('name');           // 실제 캐시에서 조회
Cache::memo()->get('name');           // 메모리에서 반환

Cache::memo()->put('name', 'Tim');    // 메모리 값 삭제, 새 값 저장
Cache::memo()->get('name');           // 실제 캐시에서 다시 조회
```

<a name="the-cache-helper"></a>
### Cache 헬퍼 (The Cache Helper)

`Cache` 파사드를 사용하는 것 외에도, 전역 함수 `cache`를 통해 캐시에서 데이터를 조회·저장할 수 있습니다. 문자열 인수 하나를 전달하면 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키/값 쌍을 배열로 전달하고 만료 시간도 함께 전달하면, 해당 기간 동안 캐시에 값을 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```

인수 없이 `cache` 함수를 호출하면, `Illuminate\Contracts\Cache\Factory` 구현 인스턴스가 반환되며 다양한 캐싱 메서드를 호출할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수 사용 시, [파사드 테스트](/docs/master/mocking#mocking-facades)처럼 `Cache::shouldReceive` 메서드를 활용해 테스트할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그 (Cache Tags)

> [!WARNING]
> `file`, `dynamodb`, 또는 `database` 캐시 드라이버 사용 시, 캐시 태그는 지원되지 않습니다.

<a name="storing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 저장

캐시 태그를 사용하면 서로 관련된 여러 항목에 태그를 지정하고, 해당 태그가 할당된 모든 값을 한 번에 삭제할 수 있습니다. 태그 이름의 배열을 전달해 태그가 지정된 캐시에 접근할 수 있습니다. 예를 들어, 다음과 같이 태그 캐시에 값을 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 조회

태그로 저장한 항목은 값을 저장할 때 사용한 동일한 태그 배열을 함께 전달해야 조회할 수 있습니다. 원하는 키를 `get` 메서드에 전달하면 됩니다:

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 제거

특정 태그나 태그 목록이 할당된 모든 캐시 항목을 한 번에 비울 수 있습니다. 아래 코드는 `people`, `authors`, 또는 두 태그 중 하나에 해당하는 모든 캐시를 제거합니다. 즉, `Anne`과 `John` 모두 삭제됩니다:

```php
Cache::tags(['people', 'authors'])->flush();
```

반면, 아래 코드는 `authors` 태그에만 해당하는 값만 제거하기 때문에, `Anne`만 삭제되고, `John`은 그대로 남습니다:

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 원자적 락 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 캐시 드라이버를 사용해야 합니다. 또한, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리하기 (Managing Locks)

원자적 락을 사용하면 경쟁 조건(race condition) 걱정 없이 분산 락을 제어할 수 있습니다. 예를 들어 [Laravel Cloud](https://cloud.laravel.com)는 한 번에 하나의 원격 작업만 서버에서 실행하도록 원자적 락을 사용합니다. `Cache::lock` 메서드로 락을 생성 및 관리할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 락 획득...

    $lock->release();
}
```

`get` 메서드는 클로저도 받을 수 있습니다. 클로저가 실행된 후 Laravel이 락을 자동으로 해제합니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 10초 동안 락을 획득하고 자동 해제...
});
```

요청 시점에 락을 바로 획득할 수 없다면, Laravel이 지정된 시간(초)만큼 락이 풀릴 때까지 기다리도록 할 수도 있습니다. 주어진 시간 내에 락을 획득하지 못할 경우 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

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

위 코드는, `block` 메서드에 클로저를 전달하여 더 간단하게 만들 수 있습니다. 클로저 실행 전 지정한 시간(초)만큼 락을 기다리고, 클로저 실행 후 락을 자동 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 10초 동안 락 획득...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리하기 (Managing Locks Across Processes)

때로는 한 프로세스에서 락을 획득하고, 또 다른 프로세스에서 락을 해제하고 싶을 수 있습니다. 예를 들어, 웹 요청 중에 락을 획득한 후, 이 요청에서 발생한 큐 작업이 끝나면 락을 해제하려는 경우입니다. 이런 시나리오에서는 락의 "owner token"(소유자 토큰)을 큐 작업에 전달해, 해당 작업에서 토큰으로 락을 다시 불러올 수 있습니다.

아래 예시에서는 락 획득에 성공하면 큐 작업을 디스패치하고, 락의 owner 토큰을 전달합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

큐 작업인 `ProcessPodcast`에서는 owner 토큰으로 락을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

현재 owner와 상관없이 강제로 락을 해제하려면 `forceRelease` 메서드를 사용하세요:

```php
Cache::lock('processing')->forceRelease();
```

<a name="locks-and-function-invocations"></a>
### 락과 함수 호출 (Locks and Function Invocations)

`withoutOverlapping` 메서드는 원자적 락을 걸고 주어진 클로저를 실행하는 간단한 문법을 제공합니다. 덕분에 인프라 전체에서 한 번에 하나의 클로저만 실행되도록 보장할 수 있습니다:

```php
Cache::withoutOverlapping('foo', function () {
    // 최대 10초 대기 후 락 획득...
});
```

기본적으로 락은 클로저 실행이 끝날 때까지 유지되고, 락 획득을 위해 최대 10초까지 대기합니다. 이 값들은 메서드에 추가 인수로 전달해 커스터마이징할 수 있습니다:

```php
Cache::withoutOverlapping('foo', function () {
    // 최대 5초 대기 후 120초간 락 획득...
}, lockFor: 120, waitFor: 5);
```

지정한 대기 시간 내에 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다.

<a name="cache-failover"></a>
## 캐시 장애 조치 (Cache Failover)

`failover` 캐시 드라이버는 캐시 동작 중 장애가 발생할 때 자동 장애 조치(failover) 기능을 제공합니다. `failover` 저장소의 기본 캐시 저장소가 어떤 이유로 실패하면, Laravel은 자동으로 목록에 지정된 다음 저장소를 사용하려 시도합니다. 이 기능은 운영 환경에서 캐시 신뢰성이 매우 중요한 경우, 고가용성을 확보하는 데 특히 유용합니다.

장애 조치 캐시 저장소를 구성하려면, `failover` 드라이버를 지정하고 사용할 저장소 이름을 배열로 전달하세요. Laravel은 기본적으로 예시 장애 조치 구성을 `config/cache.php` 설정 파일에 포함합니다:

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

`failover` 드라이버를 사용하는 저장소를 구성한 후에는, 애플리케이션의 `.env` 파일에서 기본 캐시 저장소를 장애 조치 저장소로 설정해야 장애 조치 기능이 동작합니다:

```ini
CACHE_STORE=failover
```

캐시 저장소 동작이 실패하고 장애 조치가 발동하면, Laravel은 `Illuminate\Cache\Events\CacheFailedOver` 이벤트를 발생시키므로, 이를 활용해 실패를 로깅하거나 알릴 수 있습니다.

<a name="adding-custom-cache-drivers"></a>
## 사용자 정의 캐시 드라이버 추가하기 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성하기 (Writing the Driver)

사용자 정의 캐시 드라이버를 만들기 위해, 먼저 `Illuminate\Contracts\Cache\Store` [계약](/docs/master/contracts)을 구현해야 합니다. 예를 들어, MongoDB 캐시 구현은 다음과 같이 작성할 수 있습니다:

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

각 메서드를 MongoDB 커넥션으로 구현하면 됩니다. 각 메서드를 어떻게 구현할 수 있는지는 [Laravel 프레임워크 소스의 `Illuminate\Cache\MemcachedStore`](https://github.com/laravel/framework)를 참고하세요. 구현이 완료되면, `Cache` 파사드의 `extend` 메서드로 사용자 드라이버 등록을 마무리할 수 있습니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 사용자 정의 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉토리 아래에 `Extensions` 네임스페이스를 만들 수 있습니다. 단, Laravel은 엄격한 폴더 구조를 강제하지 않으므로 자유롭게 정리해도 됩니다.

<a name="registering-the-driver"></a>
### 드라이버 등록하기 (Registering the Driver)

사용자 정의 캐시 드라이버를 Laravel에 등록하려면, `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 자신들의 `boot` 메서드에서 캐시 값을 읽을 수 있으므로, 사용자 드라이버를 `booting` 콜백 안에서 등록하는 것이 좋습니다. `booting` 콜백은 서비스 프로바이더의 `register` 호출이 모두 끝난 직후, `boot` 메서드 호출 직전에 실행되므로, 사용자 드라이버가 올바르게 등록됩니다. `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 아래와 같이 작성할 수 있습니다:

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

`extend` 메서드의 첫 번째 인자는 드라이버의 이름으로, `config/cache.php` 설정 파일의 `driver` 옵션 값과 일치해야 합니다. 두 번째 인자는 반드시 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저여야 하며, 클로저에는 [서비스 컨테이너](/docs/master/container) 인스턴스인 `$app`이 전달됩니다.

확장 기능이 등록되면, 애플리케이션 설정 파일(`CACHE_STORE` 환경 변수 또는 `config/cache.php`의 `default` 옵션)에서 해당 드라이버 이름으로 설정 값을 변경해 사용할 수 있습니다.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 동작마다 실행할 코드를 작성하고 싶다면, 캐시에서 발생하는 다양한 [이벤트](/docs/master/events)를 리스닝 할 수 있습니다:

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

성능 최적화를 위해, 애플리케이션의 `config/cache.php` 설정 파일에서 특정 캐시 저장소의 `events` 설정 값을 `false`로 지정해 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
