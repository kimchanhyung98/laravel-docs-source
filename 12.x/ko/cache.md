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
    - [Cache 헬퍼](#the-cache-helper)
- [캐시 태그](#cache-tags)
- [원자적 락(Atomic Locks)](#atomic-locks)
    - [락 관리하기](#managing-locks)
    - [프로세스 간 락 관리하기](#managing-locks-across-processes)
- [캐시 장애 조치(Failover)](#cache-failover)
- [커스텀 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 수행하는 데이터 조회나 처리 작업 중에는 CPU를 집중적으로 사용하거나 몇 초 이상 걸릴 수 있는 작업도 있습니다. 이럴 때는 조회된 데이터를 일정 시간 동안 캐시에 저장하여, 동일한 데이터 요청이 다시 들어올 때 빠르게 응답할 수 있도록 하는 것이 일반적입니다. 이때 캐시된 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은, 아주 빠른 데이터 저장소에 저장됩니다.

Laravel은 다양한 캐시 백엔드를 위한 직관적이고 통합된 API를 제공하여, 이러한 빠른 데이터 조회의 이점을 쉽게 활용하고 웹 애플리케이션의 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서 애플리케이션 전체에 기본으로 사용할 캐시 저장소를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스와 같은 인기 있는 캐시 백엔드를 기본으로 지원합니다. 또한 파일 기반의 캐시 드라이버도 제공하며, `array` 및 `null` 캐시 드라이버는 자동화된 테스트를 위한 편리한 캐시 백엔드를 제공합니다.

캐시 설정 파일에는 이 외에도 다양한 옵션이 포함되어 있습니다. 기본적으로 Laravel은 `database` 캐시 드라이버로 설정되어 있으며, 직렬화된 캐시 객체를 애플리케이션의 데이터베이스에 저장합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항 (Driver Prerequisites)

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 때는 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로, 이 테이블은 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 애플리케이션에 이 마이그레이션이 없다면, 다음과 같이 `make:cache-table` Artisan 명령어를 사용하여 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. 모든 Memcached 서버는 `config/cache.php` 설정 파일에 나열할 수 있습니다. 이 파일에는 이미 시작을 위한 `memcached.servers` 항목이 포함되어 있습니다:

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

필요하다면 `host` 옵션을 UNIX 소켓 경로로 설정할 수도 있습니다. 이 경우 `port` 옵션은 반드시 `0`으로 지정해야 합니다:

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

Laravel에서 Redis 캐시를 사용하기 전에 PECL을 통해 PhpRedis PHP 확장 기능을 설치하거나 Composer를 통해 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/12.x/sail)에는 이미 이 확장 기능이 포함되어 있습니다. 또한, [Laravel Cloud](https://cloud.laravel.com), [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 애플리케이션 플랫폼 역시 PhpRedis 확장 기능이 기본적으로 설치되어 있습니다.

Redis 설정에 대한 더 자세한 내용은 [Redis 문서 페이지](/docs/12.x/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 보통 이 테이블의 이름은 `cache`로 지정합니다. 다만, 이 테이블의 이름은 `cache` 설정 파일 내 `stores.dynamodb.table` 설정 값에 따라 정할 수 있습니다. 테이블 이름은 `DYNAMODB_CACHE_TABLE` 환경 변수로도 설정할 수 있습니다.

이 테이블에는 문자열 파티션 키가 하나 필요하며, 이 키의 이름은 애플리케이션의 `cache` 설정 파일에 있는 `stores.dynamodb.attributes.key` 설정 값과 일치해야 합니다. 기본적으로 파티션 키의 이름은 `key`입니다.

일반적으로 DynamoDB는 테이블에서 만료된 항목을 자동 삭제하지 않습니다. 따라서 [Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) 기능을 활성화해야 하며, 테이블의 TTL 속성명으로는 `expires_at`을 사용해야 합니다.

다음으로 Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다:

```shell
composer require aws/aws-sdk-php
```

또한 DynamoDB 캐시 저장소의 설정 옵션에 값이 채워져 있는지 확인해야 합니다. 보통, `AWS_ACCESS_KEY_ID`와 `AWS_SECRET_ACCESS_KEY` 같은 옵션은 애플리케이션의 `.env` 파일에 정의해둡니다:

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 제공하는 `mongodb` 캐시 드라이버를 사용할 수 있으며, 이는 `mongodb` 데이터베이스 연결을 통해 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하여 만료된 캐시 항목을 자동으로 삭제할 수 있습니다.

MongoDB 설정에 관한 더 자세한 정보는 MongoDB [Cache and Locks 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하세요.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드를 사용할 수 있습니다. 이 문서 내의 모든 예시에서 이 파사드를 사용합니다. `Cache` 파사드는 Laravel 캐시 계약의 실제 구현에 간편하게 접근할 수 있도록 도와줍니다:

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

`Cache` 파사드의 `store` 메서드를 이용하여 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일의 `stores` 배열에 정의된 저장소 중 하나와 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 가져올 때 사용합니다. 해당 항목이 캐시에 없다면 `null`이 반환됩니다. 원하는 경우, 두 번째 인수로 기본 값을 지정할 수 있습니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저를 전달할 수도 있습니다. 지정한 항목이 캐시에 없으면 클로저의 결과가 반환됩니다. 클로저를 사용하면 기본 값을 데이터베이스나 외부 서비스에서 지연 조회할 수 있습니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인하기

캐시에 항목이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. 이 메서드는 항목이 존재하지만 값이 `null`일 경우에도 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소시키기

정수 값을 가진 항목의 값을 조정하려면 `increment` 및 `decrement` 메서드를 사용할 수 있습니다. 두 메서드 모두 값을 얼마나 늘리거나 줄일지를 나타내는 두 번째 인수를 선택적으로 받을 수 있습니다:

```php
// 값이 없다면 초기화...
Cache::add('key', 0, now()->addHours(4));

// 값 증가 또는 감소...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 획득 후 저장하기

캐시에서 항목을 가져오되, 없으면 기본 값을 캐시에 저장하고 싶을 때가 있습니다. 예를 들면, 모든 사용자를 캐시에서 가져오거나, 없으면 데이터베이스에서 조회한 뒤 캐시에 추가하는 식입니다. 이럴 때는 `Cache::remember` 메서드를 사용합니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

항목이 캐시에 없다면, `remember` 메서드에 전달된 클로저가 실행되고, 그 결과가 캐시에 저장됩니다.

데이터를 영구적으로 저장하거나 없으면 가져오는 방법은 `rememberForever` 메서드를 사용합니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember` 메서드를 사용할 때, 일부 사용자는 캐시된 값이 만료된 경우 느린 응답을 경험할 수 있습니다. 특정 데이터에 대해서는, 캐시된 값이 백그라운드에서 재계산되는 동안 일부 오래된(stale) 데이터를 계속 제공하고, 재계산이 끝난 후 새로운 데이터를 제공하는 것이 유용할 수 있습니다. 이는 "stale-while-revalidate" 패턴이라고 불리며, `Cache::flexible` 메서드가 이 패턴을 구현합니다.

`flexible` 메서드는 캐시가 "신선"하다고 간주되는 시간과 "stale" 상태가 되는 시간을 배열로 받습니다. 배열의 첫 번째 값은 캐시의 신선 기간(초), 두 번째 값은 오랫동안 stale 상태로 제공할 수 있는 최대 시간(초)입니다.

첫 번째 값 이내에 요청이 오면 캐시된 값을 즉시 반환합니다. 두 값 사이(stale 기간)에는 예전 데이터를 제공하고, 사용자에게 응답한 후 [지연 함수](/docs/12.x/helpers#deferred-functions)를 등록해 백그라운드에서 캐시를 갱신합니다. 두 번째 값이 지난 뒤에는 캐시가 만료된 것으로 간주되어, 즉시 새로 계산됩니다(이 경우 사용자는 느린 응답을 경험할 수 있습니다):

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 획득 후 삭제하기

캐시에서 항목을 받아온 뒤 바로 삭제하고 싶다면 `pull` 메서드를 사용할 수 있습니다. `get` 메서드와 마찬가지로, 해당 항목이 없을 경우 `null`을 반환합니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

캐시에 항목을 저장할 때는 `Cache` 파사드의 `put` 메서드를 사용합니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

`put` 메서드에 저장 시간을 전달하지 않으면, 해당 항목은 영구적으로 저장됩니다:

```php
Cache::put('key', 'value');
```

또한, 만료 시간을 나타내는 정수(초) 대신 `DateTime` 인스턴스를 전달할 수도 있습니다:

```php
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 이미 없을 때만 저장하기

`add` 메서드는 캐시에 항목이 없는 경우에만 값을 저장합니다. 항목이 실제로 캐시에 추가됐다면 `true`를, 이미 존재한다면 `false`를 반환합니다. `add` 메서드는 원자적(Atomic) 연산입니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 영구적으로 항목 저장하기

`forever` 메서드는 항목을 캐시에 영구적으로 저장할 때 사용합니다. 이러한 항목은 만료되지 않으므로, `forget` 메서드를 사용해 수동으로 제거해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우, "영구"로 저장된 항목이라도 캐시 용량 한도에 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드를 사용하여 캐시에서 항목을 제거할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간(초)을 0이나 음수로 지정하여 항목을 제거하는 방법도 있습니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

전체 캐시를 비우려면 `flush` 메서드를 사용합니다:

```php
Cache::flush();
```

> [!WARNING]
> 캐시를 비우는(Flush) 작업은 설정한 캐시 "prefix"와 상관없이 모든 캐시 항목을 삭제하므로, 다른 애플리케이션과 캐시를 공유할 경우 신중하게 사용해야 합니다.

<a name="cache-memoization"></a>
### 캐시 메모이제이션 (Cache Memoization)

Laravel의 `memo` 캐시 드라이버는 단일 요청 또는 작업 실행 중에 한 번 조회된 캐시 값을 메모리에 임시로 저장해줍니다. 이렇게 하면 동일 실행 내에서 반복적으로 캐시 접근이 일어날 때, 성능이 크게 향상됩니다.

메모이제이션된 캐시를 사용하려면 `memo` 메서드를 호출하세요:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드는 캐싱의 기반이 되는 실제 캐시 저장소의 이름을 인수로 받을 수도 있습니다:

```php
// 기본 캐시 저장소 사용
$value = Cache::memo()->get('key');

// Redis 캐시 저장소 사용
$value = Cache::memo('redis')->get('key');
```

특정 키에 대해 최초의 `get` 호출은 실제 캐시 저장소에서 값을 조회하지만, 같은 요청이나 작업 내에서 반복적으로 접근할 때는 메모리에서 값을 가져옵니다:

```php
// 실제 캐시 저장소에 조회
$value = Cache::memo()->get('key');

// 실제 저장소 접근 없이, 메모리에서 바로 반환
$value = Cache::memo()->get('key');
```

값을 변경하는 메서드(예: `put`, `increment`, `remember` 등)를 호출하면, 메모이제이션된 값을 자동으로 잊고, 실제 캐시 저장소에 변경을 위임합니다:

```php
Cache::memo()->put('name', 'Taylor'); // 실제 저장소에 기록
Cache::memo()->get('name');           // 실제 저장소에 접근
Cache::memo()->get('name');           // 메모리에서 반환

Cache::memo()->put('name', 'Tim');    // 메모이제이션 값 초기화 후 새 값 기록
Cache::memo()->get('name');           // 다시 실제 저장소 접근
```

<a name="the-cache-helper"></a>
### Cache 헬퍼

`Cache` 파사드 대신, 전역 `cache` 함수를 사용해 캐시에서 데이터를 조회하거나 저장할 수도 있습니다. 이 함수에 문자열 하나를 인수로 넣으면 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키/값 쌍의 배열과 만료 시간을 함께 넘기면, 주어진 기간 동안 값을 캐시에 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

인수 없이 `cache` 함수를 호출하면, `Illuminate\Contracts\Cache\Factory`의 구현 인스턴스를 반환하므로 다른 캐싱 메서드를 호출할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수 호출을 테스트할 때는, [파사드 테스트](/docs/12.x/mocking#mocking-facades)와 마찬가지로 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그 (Cache Tags)

> [!WARNING]
> `file`, `dynamodb`, `database` 캐시 드라이버 사용 시 캐시 태그는 지원되지 않습니다.

<a name="storing-tagged-cache-items"></a>
### 태그된 캐시 항목 저장하기

캐시 태그를 사용하면 관련된 캐시 항목들에 태그를 부여하고, 같은 태그를 가진 값을 한 번에 삭제(Flush)할 수 있습니다. 태그된 캐시에 접근하려면, 태그 이름의 순서가 있는 배열을 전달합니다. 예를 들어, 다음처럼 태그된 캐시에 값을 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### 태그된 캐시 항목 접근하기

태그가 지정된 항목을 조회할 때는, 저장할 때와 동일한 순서로 태그 배열을 전달해야 합니다. 그런 후 원하는 키로 `get` 메서드를 호출하세요:

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### 태그된 캐시 항목 삭제하기

특정 태그 또는 태그 목록으로 지정된 모든 캐시 항목을 한 번에 삭제할 수 있습니다. 예를 들어, 아래 코드는 `people`, `authors` 또는 둘 다에 태그된 모든 캐시를 삭제합니다. 즉, `Anne`과 `John` 모두 캐시에서 제거됩니다:

```php
Cache::tags(['people', 'authors'])->flush();
```

반대로, 아래 코드처럼 하나의 태그(`authors`)에만 삭제를 적용하면, `Anne`만 지워지고 `John`은 유지됩니다:

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 원자적 락 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 연결되어 있어야 합니다.

<a name="managing-locks"></a>
### 락 관리하기

원자적 락(Atomic Locks)은 분산 락을 사용할 때 레이스 컨디션에 대한 걱정 없이 락을 조작할 수 있게 해줍니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)는 원자적 락을 이용하여 한 번에 오직 하나의 원격 작업만 서버에서 실행되도록 보장합니다. 락을 생성하고 관리하려면 `Cache::lock` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 락을 10초 동안 획득함...

    $lock->release();
}
```

`get` 메서드는 클로저를 인수로 받을 수도 있습니다. 클로저가 실행된 후, Laravel이 자동으로 락을 해제해줍니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 락이 10초 동안 획득되었다가 자동 해제됨...
});
```

락을 요청한 시점에 사용할 수 없다면, Laravel이 지정한 초(seconds)만큼 락을 기다리게 할 수도 있습니다. 제한 시간 내에 락을 획득할 수 없다면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다:

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

위의 예시는, 클로저를 `block` 메서드에 전달해서 더 간단하게 작성할 수도 있습니다. 이 경우 Laravel이 지정된 시간 동안 락을 시도하게 되고, 클로저 실행 후 자동으로 락을 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 기다린 후 10초 동안 락을 획득...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리하기

때로는 한 프로세스에서 락을 획득하고, 다른 프로세스에서 그 락을 해제해야 할 수도 있습니다. 예를 들어, 웹 요청 중에 락을 획득한 뒤, 해당 요청에서 트리거한 큐 작업이 종료될 때 락을 해제해야 할 수 있습니다. 이 때는 락의 범위가 지정된 "owner 토큰"을 큐 작업에 전달해서, 해당 토큰으로 락을 다시 인스턴스화하고 해제해야 합니다.

아래 예시에서는, 락을 정상적으로 획득했을 경우 큐 작업을 디스패치하고, 락의 owner 토큰을 큐 작업에 함께 전달합니다(`owner` 메서드 사용):

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

애플리케이션의 `ProcessPodcast` 작업에서는 owner 토큰으로 락을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

현재 owner를 무시하고 강제로 락을 해제하려면 `forceRelease` 메서드를 사용할 수 있습니다:

```php
Cache::lock('processing')->forceRelease();
```

<a name="cache-failover"></a>
## 캐시 장애 조치(Failover) (Cache Failover)

`failover` 캐시 드라이버는 캐시 조작 시, 기본 캐시 저장소에 문제가 발생하면 다음으로 지정된 저장소를 자동으로 사용하는 장애 조치 기능을 제공합니다. 이 기능은 운영 환경에서 캐시의 신뢰성이 중요한 경우, 고가용성을 확보하는 데 유용합니다.

장애 조치 캐시 저장소를 설정하려면 `failover` 드라이버를 지정하고 시도할 저장소 이름의 배열을 순서대로 나열하면 됩니다. Laravel의 기본 `config/cache.php` 설정 파일에는 이미 예시 구성 예제가 포함되어 있습니다:

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

`failover` 드라이버를 사용하는 저장소를 설정한 뒤에는, 보통 `.env` 파일에서 장애 조치 저장소를 기본 캐시 저장소로 지정합니다:

```ini
CACHE_STORE=failover
```

캐시 저장소 조작 실패로 장애 조치가 활성화되면, Laravel은 `Illuminate\Cache\Events\CacheFailedOver` 이벤트를 발생시켜 캐시 저장소가 실패했다는 사실을 기록하거나 보고할 수 있도록 합니다.

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가하기 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성하기

커스텀 캐시 드라이버를 만들기 위해서는 우선 `Illuminate\Contracts\Cache\Store` [계약](/docs/12.x/contracts)을 구현해야 합니다. 예를 들어 MongoDB 캐시 구현은 다음과 같이 작성할 수 있습니다:

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

여기서는 각 메서드를 MongoDB 연결을 사용하여 구현하면 됩니다. 방법에 대한 예시는 [Laravel 프레임워크 소스 코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고하세요. 구현을 완료했다면, 이제 `Cache` 파사드의 `extend` 메서드를 호출하여 커스텀 드라이버를 등록할 수 있습니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 아래에 `Extensions` 네임스페이스를 만들 수 있습니다. 하지만 Laravel은 애플리케이션 구조에 강한 제약이 없으므로, 원하는 대로 구조를 잡아도 무방합니다.

<a name="registering-the-driver"></a>
### 드라이버 등록하기

Laravel에 커스텀 캐시 드라이버를 등록하려면 `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 자신의 `boot` 메서드 내에서 캐시 값을 읽으려 할 수 있으므로, 우리 커스텀 드라이버는 `booting` 콜백 내에서 등록해야 합니다. 이렇게 하면 모든 서비스 프로바이더의 `register` 메서드 실행 후, `boot` 메서드가 호출되기 직전에 드라이버가 등록됩니다. 아래와 같이 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에 `booting` 콜백을 추가할 수 있습니다:

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

`extend` 메서드의 첫 인수는 드라이버 이름이며, 이는 `config/cache.php`의 `driver` 옵션에 대응됩니다. 두 번째 인수는 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하는 클로저입니다. 이 클로저에는 [서비스 컨테이너](/docs/12.x/container) 인스턴스인 `$app`이 전달됩니다.

확장이 등록되면, 애플리케이션의 `CACHE_STORE` 환경 변수 또는 `config/cache.php`의 `default` 옵션을 확장 이름으로 변경해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 동작에 대해 코드를 실행하고 싶을 때는, 캐시에서 발생하는 다양한 [이벤트](/docs/12.x/events)를 청취(listen)할 수 있습니다:

<div class="overflow-auto">

| 이벤트명                                    |
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

성능을 높이기 위해, 애플리케이션의 `config/cache.php` 설정 파일 내의 특정 캐시 저장소에서 `events` 옵션을 `false`로 설정하여 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
