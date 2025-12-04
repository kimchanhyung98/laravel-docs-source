# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 선행 조건](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 조회하기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 삭제하기](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [Cache 헬퍼](#the-cache-helper)
- [캐시 태그](#cache-tags)
- [원자적 락(Atomic Locks)](#atomic-locks)
    - [락 관리](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
- [캐시 페일오버](#cache-failover)
- [커스텀 캐시 드라이버 추가](#adding-custom-cache-drivers)
    - [드라이버 작성](#writing-the-driver)
    - [드라이버 등록](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 수행하는 일부 데이터 조회 또는 처리 작업은 CPU 자원을 많이 소모하거나 몇 초가 걸릴 수 있습니다. 이런 경우, 동일한 데이터를 반복해서 조회할 때 빠르게 반환할 수 있도록 데이터를 일정 시간 동안 캐싱하는 것이 일반적입니다. 캐싱된 데이터는 일반적으로 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히도 Laravel은 다양한 백엔드 캐시 시스템을 위한 표현력 있고 일관된 API를 제공하므로, 빠른 데이터 조회의 장점을 살리면서 웹 애플리케이션의 속도를 크게 높일 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서 애플리케이션 전반에 기본적으로 사용할 캐시 저장소를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등 널리 사용되는 캐시 백엔드를 기본 지원합니다. 또한 파일 기반 캐시 드라이버가 제공되며, `array`와 `null` 캐시 드라이버는 자동화된 테스트에 유용한 백엔드를 제공합니다.

캐시 설정 파일에는 이 외에도 다양한 옵션이 있으니 확인해 보시기 바랍니다. 기본적으로 Laravel은 `database` 캐시 드라이버를 사용하도록 설정되어 있어, 직렬화된 캐시 객체가 애플리케이션의 데이터베이스에 저장됩니다.

<a name="driver-prerequisites"></a>
### 드라이버 선행 조건 (Driver Prerequisites)

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 경우, 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 이 테이블이 포함되어 있지만, 애플리케이션에 해당 마이그레이션이 없다면 `make:cache-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. 사용 가능한 모든 Memcached 서버는 `config/cache.php` 설정 파일에 나열할 수 있습니다. 이 파일에는 이미 시작할 수 있도록 `memcached.servers` 항목이 들어 있습니다:

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

필요하다면 `host` 옵션을 UNIX 소켓 경로로 설정할 수도 있습니다. 이 경우 `port` 옵션은 `0`으로 지정해야 합니다:

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

Laravel에서 Redis 캐시를 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer를 통해 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/12.x/sail)에는 이미 이 확장 모듈이 포함되어 있습니다. [Laravel Cloud](https://cloud.laravel.com) 및 [Laravel Forge](https://forge.laravel.com) 등 공식 Laravel 애플리케이션 플랫폼에도 PhpRedis 확장 모듈이 기본적으로 설치되어 있습니다.

Redis 설정에 대한 자세한 정보는 [Laravel 공식 Redis 문서](/docs/12.x/redis#configuration)를 참고하십시오.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 이 테이블의 이름은 `cache`가 되어야 하지만, `cache` 설정 파일 내 `stores.dynamodb.table` 설정 값에 따라 테이블명을 지정할 수 있으며, 환경 변수 `DYNAMODB_CACHE_TABLE`을 통해서도 지정할 수 있습니다.

이 테이블에는 파티션 키(partition key)로 사용할 문자열 타입의 컬럼이 필요하며, 이름 또한 애플리케이션의 `cache` 설정 파일 내 `stores.dynamodb.attributes.key` 항목의 값과 일치해야 합니다. 기본적으로 파티션 키는 `key`로 설정합니다.

대개 DynamoDB는 만료된 항목을 자동으로 삭제하지 않습니다. 따라서 테이블에서 [Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) 기능을 활성화하는 것이 좋습니다. 테이블의 TTL 설정 시, 속성 이름은 `expires_at`으로 지정해야 합니다.

다음으로, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다:

```shell
composer require aws/aws-sdk-php
```

또한, DynamoDB 캐시 저장소의 설정 옵션에 값이 제대로 지정되어 있는지 확인해야 합니다. 예를 들어, `AWS_ACCESS_KEY_ID` 및 `AWS_SECRET_ACCESS_KEY` 등은 애플리케이션의 `.env` 파일에서 정의하는 것이 일반적입니다:

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 `mongodb` 캐시 드라이버를 제공하며, `mongodb` 데이터베이스 연결을 통해 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하므로, 만료된 캐시 항목을 자동으로 삭제할 수 있습니다.

MongoDB 설정에 관한 자세한 내용은 MongoDB [Cache and Locks documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하십시오.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기 (Obtaining a Cache Instance)

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드(facade)를 사용할 수 있습니다. 이 문서에서는 `Cache` 파사드를 계속 사용할 예정입니다. `Cache` 파사드는 Laravel 캐시 계약의 기본 구현체에 편리하고 간결하게 접근할 수 있게 해줍니다:

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

`Cache` 파사드를 사용하면 `store` 메서드를 통해 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일의 `stores` 설정 배열에 있는 저장소명과 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분 동안 저장
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 조회하기 (Retrieving Items From the Cache)

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 조회하는 데 사용합니다. 해당 항목이 캐시에 없다면 `null`이 반환됩니다. 원한다면, 항목이 없을 때 반환할 기본 값을 두 번째 인자로 전달할 수 있습니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본 값으로 클로저(익명 함수)를 전달할 수도 있습니다. 항목이 캐시에 없을 때만 이 클로저의 결과가 반환됩니다. 클로저를 통해 기본 값을 데이터베이스나 외부 서비스에서 불러올 수 있습니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인

캐시에 항목이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. 해당 항목이 존재하지만 값이 `null`인 경우에도 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가 및 감소

캐시에 있는 정수형 항목의 값을 조정하려면 `increment`와 `decrement` 메서드를 사용할 수 있습니다. 두 메서드 모두 증가/감소할 값을 두 번째 인자로 지정할 수 있습니다:

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
#### 조회 후 저장

가끔은 캐시에서 항목을 조회하면서, 조회 실패 시 기본 값을 저장하고 싶을 때가 있습니다. 예를 들어, 모든 사용자를 캐시에서 조회하거나, 없다면 데이터베이스에서 조회 후 캐시에 추가하는 방식입니다. 이럴 때는 `Cache::remember` 메서드를 사용합니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

캐시에 해당 항목이 없다면, `remember` 메서드에 전달한 클로저가 실행되고, 그 반환값이 캐시에 저장됩니다.

항목을 영구적으로 저장하거나, 존재하지 않는 경우 영구적으로 저장하고 싶다면 `rememberForever` 메서드를 사용할 수 있습니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember` 메서드를 사용할 때, 캐시 값이 만료되면 일부 사용자가 느린 응답을 경험할 수 있습니다. 이러한 데이터의 경우, "부분적으로 만료된(stale)" 데이터를 반환하면서, 백그라운드에서 캐시 값을 다시 계산하는 것이 유용할 수 있습니다. 이렇게 하면 캐시 값 계산 중 일부 사용자는 느린 응답을 경험하지 않게 됩니다. 이를 흔히 "stale-while-revalidate" 패턴이라고 하며, `Cache::flexible` 메서드로 구현할 수 있습니다.

`flexible` 메서드는 캐시 값이 "신선(fresh)한" 기간과 "묵은(stale) 데이터"로 간주될 수 있는 기간을 명시하는 배열을 받습니다. 배열의 첫 번째 값은 캐시가 신선하게 유지되는(즉시 반환되는) 초 단위 시간이며, 두 번째 값은 묵은 데이터를 재계산 없이 반환할 수 있는 시간입니다.

신선 기간 내 요청 시 즉시 캐시를 반환하고, 묵은 데이터 기간에는 사용자에게는 기존 캐시 값을 반환하면서, 응답 이후 [지연 함수](/docs/12.x/helpers#deferred-functions)가 등록되어 캐시 값을 갱신합니다. 두 번째 시간 이후에는 캐시가 만료로 간주되어 값을 즉시 재계산하며, 이때 사용자는 느린 응답을 경험할 수 있습니다:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제

캐시에서 항목을 조회한 뒤, 해당 항목을 삭제하려면 `pull` 메서드를 사용할 수 있습니다. `get` 메서드와 마찬가지로, 항목이 없다면 `null`이 반환됩니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기 (Storing Items in the Cache)

`Cache` 파사드의 `put` 메서드를 이용하여 캐시에 항목을 저장할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

보관 시간을 생략하면 항목이 무기한 저장됩니다:

```php
Cache::put('key', 'value');
```

정수(초) 대신, 만료 시점을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다:

```php
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장

`add` 메서드는 해당 항목이 캐시에 아직 없을 때만 저장합니다. 항목이 실제로 캐시에 추가되면 `true`를 반환합니다. 이미 있다면 `false`를 반환합니다. `add` 메서드는 원자적 연산입니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 영구적으로 저장

`forever` 메서드를 사용하면 항목을 캐시에 영구적으로 저장할 수 있습니다. 이런 항목들은 만료되지 않으므로, 삭제하려면 반드시 `forget` 메서드를 사용해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용할 경우, "영구적으로" 저장한 항목도 캐시 용량 한도에 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 삭제하기 (Removing Items From the Cache)

`forget` 메서드를 사용하면 캐시에서 항목을 삭제할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간을 0 이하로 설정하여 삭제할 수도 있습니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

전체 캐시를 비우려면 `flush` 메서드를 사용합니다:

```php
Cache::flush();
```

> [!WARNING]
> 캐시 플러시(비우기)는 설정된 캐시 "prefix"를 고려하지 않고, 해당 캐시 저장소의 모든 항목을 삭제합니다. 다른 애플리케이션과 캐시를 공유 중이라면 주의해서 사용해야 합니다.

<a name="cache-memoization"></a>
### 캐시 메모이제이션 (Cache Memoization)

Laravel의 `memo` 캐시 드라이버는 단일 요청이나 작업 실행 중에 조회된 캐시 값을 임시로 메모리에 저장합니다. 이렇게 하면, 동일한 실행 내에서 같은 키에 대해 반복적으로 캐시 접근이 있을 때 성능이 크게 개선됩니다.

메모이즈드 캐시를 사용하려면 `memo` 메서드를 호출합니다:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드는 사용할 캐시 저장소명을 옵션으로 받을 수 있으며, 지정 시 해당 저장소를 데코레이트합니다:

```php
// 기본 캐시 저장소 사용...
$value = Cache::memo()->get('key');

// Redis 캐시 저장소 사용...
$value = Cache::memo('redis')->get('key');
```

특정 키에 대한 첫 `get` 호출은 실제 캐시 저장소에서 값을 가져오지만, 같은 실행 내 이후 호출은 메모리에 저장된 값을 반환합니다:

```php
// 실제 캐시에서 가져옴...
$value = Cache::memo()->get('key');

// 캐시 접근 없이, 메모이즈된 값 반환...
$value = Cache::memo()->get('key');
```

값을 변경하는 메서드(`put`, `increment`, `remember` 등)를 호출하면, 메모이즈된 값이 자동으로 제거되고, 실제 캐시 저장소에 동작이 위임됩니다:

```php
Cache::memo()->put('name', 'Taylor'); // 실제 캐시에 기록...
Cache::memo()->get('name');           // 실제 캐시에서 조회...
Cache::memo()->get('name');           // 메모이즈된 값 반환...

Cache::memo()->put('name', 'Tim');    // 메모이즈 값 제거, 새 값 기록...
Cache::memo()->get('name');           // 다시 실제 캐시에서 조회...
```

<a name="the-cache-helper"></a>
### Cache 헬퍼 (The Cache Helper)

`Cache` 파사드 외에도, 전역 `cache` 함수를 사용해 캐시에 데이터를 저장•조회할 수 있습니다. `cache` 함수를 문자열 인자 한 개로 호출하면 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키/값 배열 및 만료 시간을 전달하면, 해당 기간 동안 캐시에 값을 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

인자 없이 `cache` 함수를 호출하면 `Illuminate\Contracts\Cache\Factory` 인스턴스를 반환하므로, 다른 캐시 메서드도 사용할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수에 대한 테스트 작성 시, [파사드 테스트 방법](/docs/12.x/mocking#mocking-facades)과 동일하게 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그 (Cache Tags)

> [!WARNING]
> 캐시 태그는 `file`, `dynamodb`, `database` 캐시 드라이버에서는 지원되지 않습니다.

<a name="storing-tagged-cache-items"></a>
### 태그를 이용한 캐시 항목 저장

캐시 태그를 사용하면 관련된 항목을 태그로 묶어 캐시에 저장하고, 특정 태그가 붙은 모든 캐시를 한 번에 모두 삭제할 수 있습니다. 태그를 사용하려면, 태그 이름 배열을 전달하여 태그된 캐시에 접근하세요. 예시:

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### 태그된 캐시 항목 조회

태그를 사용하여 저장한 항목은 저장할 때 사용한 태그 목록을 그대로 전달해야만 접근할 수 있습니다. 항목을 검색하려면 같은 순서의 태그 배열을 `tags` 메서드에 전달한 뒤, `get` 메서드로 값을 조회합니다:

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### 태그된 캐시 항목 제거

특정 태그 또는 태그 목록이 붙은 항목을 모두 한 번에 삭제할 수 있습니다. 예를 들어, 아래 코드는 `people`, `authors` 혹은 두 태그 중 하나라도 포함된 모든 캐시를 제거합니다. 그래서 `Anne`과 `John` 모두 캐시에서 지워집니다:

```php
Cache::tags(['people', 'authors'])->flush();
```

반대로, 아래 코드는 `authors` 태그만 붙은 캐시를 삭제하므로, `Anne`만 삭제되고 `John`은 남게 됩니다:

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 원자적 락(Atomic Locks) (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면, 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버 중 하나를 사용하고 있어야 하며, 모든 서버가 동일한 중앙 캐시 서버에 연결되어야 합니다.

<a name="managing-locks"></a>
### 락 관리 (Managing Locks)

원자적 락은 경쟁 조건(race condition) 걱정 없이 분산 락을 다룰 수 있도록 해줍니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)는 원자적 락을 사용해 한 번에 한 개의 원격 작업만 실행되도록 보장합니다. 락을 생성하고 관리하려면 `Cache::lock` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 락 획득...

    $lock->release();
}
```

`get` 메서드는 클로저도 받을 수 있습니다. 클로저 실행 후 Laravel이 자동으로 락을 해제합니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 10초 락 획득 후, 자동 해제...
});
```

락이 즉시 사용 불가능한 경우, Laravel이 지정한 시간(초) 동안 락을 기다리도록 할 수 있습니다. 지정한 시간 내에도 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최대 5초간 대기 후, 락 획득...
} catch (LockTimeoutException $e) {
    // 락 획득 실패...
} finally {
    $lock->release();
}
```

위 예시는 클로저를 `block` 메서드에 전달하여 더 간결하게 표현할 수 있습니다. 클로저를 전달하면, 지정한 시간 동안 락 획득을 시도하고, 클로저 실행 후 락을 자동 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초간 대기 후 10초 동안 락 획득...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리 (Managing Locks Across Processes)

경우에 따라 한 프로세스에서 락을 획득하고, 다른 프로세스에서 락을 해제하고자 할 때가 있습니다. 예를 들어, 웹 요청에서 락을 획득하고, 해당 요청이 트리거하는 큐 작업이 끝날 때 락을 해제하고 싶을 수 있습니다. 이런 경우에는 락의 "owner token" 범위를 큐 작업에 전달하여, 주어진 토큰으로 다시 락을 복원할 수 있습니다.

아래 예시에서는 락을 성공적으로 획득하면 큐 작업을 디스패치하고, 락의 owner 토큰을 작업에 전달합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

`ProcessPodcast` 큐 작업 내에서는 토큰으로 락을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

현재 owner를 무시하고 락을 해제하려면 `forceRelease` 메서드를 사용할 수 있습니다:

```php
Cache::lock('processing')->forceRelease();
```

<a name="cache-failover"></a>
## 캐시 페일오버 (Cache Failover)

`failover` 캐시 드라이버는 캐시 조작 시 자동 페일오버 기능을 제공합니다. `failover` 저장소의 주 저장소에 장애가 발생하면 Laravel은 자동으로 목록에 지정된 다음 저장소를 사용합니다. 이는 실제 운영환경에서 캐시의 신뢰성과 고가용성이 중요한 경우 매우 유용합니다.

페일오버 캐시 저장소를 설정하려면, `failover` 드라이버를 지정하고, 시도할 저장소 목록을 배열로 지정하면 됩니다. 기본적으로 Laravel은 애플리케이션의 `config/cache.php` 설정 파일에 페일오버 예시 구성을 포함하고 있습니다:

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

`failover` 기능을 사용하려면, 애플리케이션의 `.env` 파일에서 기본 캐시 저장소를 페일오버 저장소로 지정해야 합니다:

```ini
CACHE_STORE=failover
```

캐시 저장소 작업이 실패해 페일오버가 발생하면, Laravel은 `Illuminate\Cache\Events\CacheFailedOver` 이벤트를 디스패치하여, 장애 상황을 로깅하거나 알릴 수 있게 합니다.

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성 (Writing the Driver)

커스텀 캐시 드라이버를 만들려면, 먼저 `Illuminate\Contracts\Cache\Store` [계약(Contract)](/docs/12.x/contracts)을 구현해야 합니다. 예를 들어, MongoDB 캐시 구현은 아래와 같이 만들 수 있습니다:

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

각 메서드를 MongoDB 연결을 통해 구현해야 합니다. 각 메서드 구현 예시는 [Laravel 프레임워크 소스의 `Illuminate\Cache\MemcachedStore`](https://github.com/laravel/framework)를 참고하십시오. 구현이 완료되면, `Cache` 파사드의 `extend` 메서드를 호출하여 드라이버 등록을 마무리할 수 있습니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 위치시켜야 할지 고민된다면, `app` 디렉터리 내에 `Extensions` 네임스페이스를 만들 수 있습니다. 하지만 Laravel은 엄격한 애플리케이션 구조가 없으니 자유롭게 구성하셔도 무방합니다.

<a name="registering-the-driver"></a>
### 드라이버 등록 (Registering the Driver)

커스텀 캐시 드라이버를 Laravel에 등록하려면, `Cache` 파사드의 `extend` 메서드를 사용합니다. 서비스 프로바이더의 `boot` 메서드에서 캐시를 읽는 경우가 있으므로, `boot` 직전에 커스텀 드라이버를 등록해야 합니다. 이를 위해 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `booting` 콜백을 등록합니다:

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

`extend` 메서드의 첫 번째 인자는 드라이버 이름이며, 이는 `config/cache.php` 설정 파일의 `driver` 옵션과 일치해야 합니다. 두 번째 인자(클로저)는 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하며, 클로저에는 [서비스 컨테이너](/docs/12.x/container) 인스턴스가 전달됩니다.

확장이 등록되면, 애플리케이션의 환경 변수 `CACHE_STORE` 또는 `config/cache.php`의 `default` 옵션을 확장명으로 변경하면 됩니다.

<a name="events"></a>
## 이벤트 (Events)

캐시 조작이 일어날 때마다 특정 코드를 실행하고 싶다면, 캐시에서 발생하는 다양한 [이벤트](/docs/12.x/events)를 청취(listen)할 수 있습니다:

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

성능 향상을 위해, 애플리케이션의 특정 캐시 저장소에 대해 `config/cache.php`의 `events` 설정 옵션을 `false`로 지정하여 캐시 이벤트 발생을 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
