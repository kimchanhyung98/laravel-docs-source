# 캐시 (Cache)

- [소개](#introduction)
- [구성](#configuration)
    - [드라이버 필수 조건](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 조회하기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [캐시 헬퍼](#the-cache-helper)
- [캐시 태그](#cache-tags)
- [아토믹 락](#atomic-locks)
    - [락 관리](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
    - [락과 함수 실행](#locks-and-function-invocations)
- [캐시 페일오버](#cache-failover)
- [커스텀 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성](#writing-the-driver)
    - [드라이버 등록](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 수행되는 일부 데이터 조회나 처리 작업은 CPU를 많이 사용하거나 몇 초의 시간이 걸릴 수 있습니다. 이런 경우, 조회된 데이터를 일정 시간 동안 캐시에 저장해 두면 이후 같은 데이터를 빠르게 가져올 수 있습니다. 캐시된 데이터는 일반적으로 [Memcached](https://memcached.org)나 [Redis](https://redis.io)처럼 매우 빠른 데이터 저장소에 저장됩니다.

Laravel은 다양한 캐시 백엔드에 대해 표현력 있고 통합된 API를 제공하므로, 이러한 빠른 데이터 조회 기능을 활용해 웹 애플리케이션의 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 구성 (Configuration)

애플리케이션의 캐시 구성 파일은 `config/cache.php`에 위치합니다. 이 파일에서 애플리케이션 전역에서 기본적으로 사용할 캐시 저장소(cache store)를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등 널리 사용되는 캐시 백엔드를 기본으로 지원합니다. 또한 파일 기반 캐시 드라이버가 제공되며, `array`와 `null` 캐시 드라이버는 자동화 테스트를 위한 편리한 캐시 백엔드를 제공합니다.

캐시 구성 파일에는 이외에도 다양한 옵션이 있으니 참고하시기 바랍니다. 기본적으로 Laravel은 직렬화된 캐시 객체를 애플리케이션의 데이터베이스에 저장하는 `database` 캐시 드라이버를 사용하도록 설정되어 있습니다.

<a name="driver-prerequisites"></a>
### 드라이버 필수 조건 (Driver Prerequisites)

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 때는 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 이 테이블은 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 만약 애플리케이션에 해당 마이그레이션 파일이 없다면, `make:cache-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. 모든 Memcached 서버는 `config/cache.php` 구성 파일에 나열할 수 있습니다. 이 파일에는 이미 시작할 수 있도록 `memcached.servers` 항목이 포함되어 있습니다:

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

필요하다면 `host` 옵션을 UNIX 소켓 경로로 설정할 수도 있습니다. 이 경우 `port` 옵션은 `0`으로 설정해야 합니다:

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

Laravel에서 Redis 캐시를 사용하려면 PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer를 사용하여 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/12.x/sail)에는 이미 이 확장 모듈이 포함되어 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com), [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 애플리케이션 플랫폼에도 PhpRedis 확장 모듈이 기본으로 설치되어 있습니다.

Redis 구성에 관해 더 자세한 내용은 [Redis Laravel 문서](/docs/12.x/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하려면 먼저 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 이 테이블의 이름은 `cache`이어야 하며, 만약 다르게 지정하려면 `cache` 구성 파일의 `stores.dynamodb.table` 값에 따라 테이블 이름을 명시하세요. 테이블 이름은 환경 변수 `DYNAMODB_CACHE_TABLE`을 통해서도 설정할 수 있습니다.

이 테이블에는 문자열 파티션 키가 있어야 하며, 이 키의 이름은 애플리케이션의 `cache` 구성 파일 내 `stores.dynamodb.attributes.key` 값과 일치해야 합니다. 기본적으로 파티션 키 이름은 `key`입니다.

일반적으로 DynamoDB는 만료된 항목을 테이블에서 자동으로 제거하지 않으므로, 테이블에서 [Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) 기능을 활성화해야 합니다. TTL 속성 이름은 `expires_at`으로 설정해야 합니다.

다음으로, Laravel 애플리케이션에서 DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다:

```shell
composer require aws/aws-sdk-php
```

또한, DynamoDB 캐시 저장소 구성 옵션에 값을 제대로 입력했는지 확인하세요. 일반적으로 이 옵션들은 `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`와 같이 애플리케이션의 `.env` 파일에 정의합니다:

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 제공하는 `mongodb` 캐시 드라이버를 사용할 수 있으며, `mongodb` 데이터베이스 커넥션을 사용해 구성할 수 있습니다. MongoDB는 TTL 인덱스를 지원하므로, 만료된 캐시 항목을 자동으로 삭제할 수 있습니다.

MongoDB 구성에 대한 자세한 내용은 MongoDB [Cache and Locks documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)을 참고하세요.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드를 사용할 수 있으며, 이 문서 전체에서 이를 사용할 예정입니다. `Cache` 파사드는 Laravel 캐시 컨트랙트의 실제 구현체에 편리하게 접근할 수 있게 해줍니다:

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

`Cache` 파사드를 사용하면 `store` 메서드를 통해 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 구성 파일의 `stores` 배열에 정의된 저장소 이름과 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 조회하기

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 조회할 때 사용합니다. 해당 항목이 존재하지 않으면 `null`을 반환합니다. 존재하지 않을 때 반환할 기본값을 두 번째 인수로 전달할 수도 있습니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저를 전달할 수도 있습니다. 해당 항목이 존재하지 않을 경우, 클로저의 결과가 반환됩니다. 클로저를 사용하면 데이터베이스 등 외부 서비스에서 기본값을 나중에 불러올 수 있습니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인

`has` 메서드를 사용하면 캐시에 항목이 존재하는지 확인할 수 있습니다. 이 메서드는 항목이 존재하지만 값이 `null`일 때도 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소시키기

`increment` 및 `decrement` 메서드를 사용하여 캐시에 저장된 정수형 항목 값을 증감할 수 있습니다. 두 메서드 모두 두 번째 인수로 증감할 값을 지정할 수 있습니다:

```php
// 값이 존재하지 않을 경우 초기화합니다...
Cache::add('key', 0, now()->plus(hours: 4));

// 값 증가 또는 감소...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 조회 및 저장

캐시에서 항목을 조회하면서, 해당 항목이 없을 경우 기본값을 저장하고 싶을 때가 있습니다. 예를 들어, 모든 사용자를 캐시에서 가져오고, 없으면 데이터베이스에서 조회해 캐시에 추가하고자 할 수 있습니다. 이런 경우 `Cache::remember` 메서드를 사용할 수 있습니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

해당 항목이 캐시에 없으면, `remember` 메서드에 전달한 클로저가 실행되고 그 결과가 캐시에 저장됩니다.

항목을 영구적으로 저장하려면 `rememberForever` 메서드를 사용할 수 있습니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember` 메서드를 사용할 때 캐시된 값이 만료되면 일부 사용자가 느린 응답을 경험할 수 있습니다. 어떤 데이터 유형에서는, 캐시 값을 백그라운드에서 재계산하는 동안 오래된(stale) 데이터를 일시적으로 제공하여 사용자가 느린 응답을 받지 않도록 할 수 있습니다. 이를 흔히 "stale-while-revalidate" 패턴이라고 하며, `Cache::flexible` 메서드가 이를 구현합니다.

`flexible` 메서드는 배열을 인수로 받아, 캐시가 "신선한" 기간과 "오래된" 상태로 제공 가능한 기간을 지정합니다. 배열의 첫 번째 값은 신선한 기간(초 단위), 두 번째 값은 오래된 데이터로 제공될 수 있는 최대 기간(초 단위)입니다.

신선한(fresh) 기간 내에 요청이 오면, 계산 없이 캐시가 즉시 반환됩니다. 오래된(stale) 기간에는 사용자에게 오래된 값을 제공하고, [지연 함수](/docs/12.x/helpers#deferred-functions)를 등록해 사용자에게 응답을 보낸 후 캐시를 새로고침합니다. 두 번째 값(오래된 기간) 이후에는 캐시가 만료된 것으로 간주되어, 바로 값을 재계산하며 이는 느린 응답을 초래할 수 있습니다:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제

캐시에서 항목을 조회한 뒤 삭제하고 싶다면, `pull` 메서드를 사용할 수 있습니다. `get`과 마찬가지로, 해당 항목이 없으면 `null`을 반환합니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

`Cache` 파사드의 `put` 메서드를 사용하여 캐시에 데이터를 저장할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

`put` 메서드에 저장 시간을 지정하지 않으면 해당 항목은 영구적으로 저장됩니다:

```php
Cache::put('key', 'value');
```

초 단위로 시간을 지정하는 대신, 만료 시점을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다:

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```

<a name="store-if-not-present"></a>
#### 항목이 없을 때만 저장

`add` 메서드는 캐시 저장소에 해당 항목이 없을 때만 값을 추가하며, 실제로 값이 추가됐을 때 `true`를 반환합니다. 이미 존재하면 `false`를 반환합니다. `add`는 아토믹(atomic) 연산입니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 항목을 영구적으로 저장

`forever` 메서드는 항목을 영구적으로 저장할 때 사용합니다. 영구 저장된 항목은 만료되지 않으므로, 직접 `forget` 메서드로 삭제해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우, "영구적"으로 저장된 항목도 캐시 용량이 가득 차면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드를 사용해 캐시에서 항목을 제거할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간을 0 또는 음수로 지정하여 항목을 제거하는 방법도 있습니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메서드를 사용하면 전체 캐시를 비울 수 있습니다:

```php
Cache::flush();
```

> [!WARNING]
> 캐시를 flush(전체 비우기)하면 구성된 캐시 "prefix"와 상관없이 모든 항목이 삭제됩니다. 여러 애플리케이션이 동일 캐시를 공유한다면 이 점을 꼭 유의하세요.

<a name="cache-memoization"></a>
### 캐시 메모이제이션 (Cache Memoization)

Laravel의 `memo` 캐시 드라이버는 한 번의 요청 또는 작업 실행 내에서 조회된 캐시 값을 메모리에 임시로 저장(메모이제이션)합니다. 이를 통해 같은 값에 반복적으로 접근할 때 캐시 조회 비용을 크게 줄일 수 있습니다.

메모이즈된 캐시를 사용하려면 `memo` 메서드를 호출하면 됩니다:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드는 캐시 드라이버명을 인수로 지정하여, 어떤 캐시 드라이버 위에 메모이제이션을 적용할지 선택할 수 있습니다:

```php
// 기본 캐시 저장소 사용...
$value = Cache::memo()->get('key');

// Redis 캐시 저장소 사용...
$value = Cache::memo('redis')->get('key');
```

같은 키에 대해 처음 `get`을 호출하면 실제 캐시 저장소에서 값을 가져오고, 이후 같은 요청/작업 내의 호출은 메모리에 저장된 값을 바로 반환합니다:

```php
// 캐시 저장소에서 조회...
$value = Cache::memo()->get('key');

// 캐시 저장소 접근 없이, 메모이즈된 값 반환...
$value = Cache::memo()->get('key');
```

`put`, `increment`, `remember` 등과 같이 캐시 값을 변경하는 메서드를 호출하면, 메모이즈된 값을 자동으로 잊고(초기화), 실제 캐시 저장소에 해당 연산을 위임합니다:

```php
Cache::memo()->put('name', 'Taylor'); // 캐시 저장소에 기록
Cache::memo()->get('name');           // 저장소에서 조회
Cache::memo()->get('name');           // 메모이즈된 값 반환

Cache::memo()->put('name', 'Tim');    // 메모이즈 값 초기화, 새 값 기록
Cache::memo()->get('name');           // 캐시 저장소에서 다시 조회
```

<a name="the-cache-helper"></a>
### 캐시 헬퍼 (The Cache Helper)

`Cache` 파사드 외에도 글로벌 헬퍼 함수인 `cache`를 사용하여 데이터를 조회하거나 저장할 수 있습니다. 문자열을 단일 인수로 전달하면 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키/값 쌍의 배열과 만료 시간을 함께 전달하면, 해당 값이 지정 시간만큼 캐시에 저장됩니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```

인수 없이 `cache` 함수를 호출하면, `Illuminate\Contracts\Cache\Factory` 인스턴스를 반환하여 다양한 캐시 메서드를 호출할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 글로벌 `cache` 함수 호출을 테스트할 때는 [파사드 테스트](/docs/12.x/mocking#mocking-facades)와 마찬가지로 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그 (Cache Tags)

> [!WARNING]
> 캐시 태그는 `file`, `dynamodb`, `database` 캐시 드라이버에서는 지원되지 않습니다.

<a name="storing-tagged-cache-items"></a>
### 태그된 캐시 항목 저장

캐시 태그 기능을 사용하면 관련된 캐시 항목에 태그를 달고, 특정 태그가 부여된 캐시 값 전체를 한 번에 비울 수 있습니다. 태그된 캐시에 접근하려면 태그 이름의 배열을 전달합니다. 예를 들어, 아래와 같이 태그된 캐시에 값을 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### 태그된 캐시 항목 조회

태그로 저장된 항목을 조회할 때는, 저장할 때 사용했던 동일한 순서의 태그 배열을 `tags` 메서드로 전달한 뒤, 원하는 키로 `get`을 호출해야 합니다:

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### 태그된 캐시 항목 제거

특정 태그 또는 태그 조합에 할당된 모든 캐시 항목을 한 번에 비울 수 있습니다. 예를 들어, 아래 코드는 `people` 또는 `authors` 태그가 달린 모든 캐시를 삭제하며, 따라서 `Anne`과 `John` 모두 캐시에서 제거됩니다:

```php
Cache::tags(['people', 'authors'])->flush();
```

반면, 아래 코드는 `authors` 태그가 달린 값만 삭제하므로, `Anne`만 캐시에서 삭제되고 `John`은 남아 있게 됩니다:

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 아토믹 락 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션에서 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 사용해야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리

아토믹 락은 경쟁 상태(race condition)를 걱정하지 않고 분산 락(distributed lock)을 제어할 수 있도록 해줍니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)에서는 아토믹 락을 사용해 한 번에 하나의 원격 태스크만 서버에서 실행되도록 보장합니다. 락은 `Cache::lock` 메서드로 생성 및 제어할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 락을 획득함...

    $lock->release();
}
```

`get` 메서드에는 클로저를 전달할 수도 있습니다. 이 경우, 클로저가 실행된 후 락이 자동으로 해제됩니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 10초 동안 락을 획득하고 자동으로 해제...
});
```

요청시점에 락을 획득할 수 없다면, 대기 시간(초 단위)을 지정해 LDAP이 해당 시간 동안 기다렸다가 락을 시도할 수 있습니다. 지정한 시간 안에 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최대 5초 기다린 후 락을 획득...
} catch (LockTimeoutException $e) {
    // 락을 획득할 수 없음...
} finally {
    $lock->release();
}
```

위 예시를 더 간단하게, `block` 메서드에 클로저를 직접 전달할 수도 있습니다. 이 경우 Laravel은 해당 시간이 될 때까지 락을 기다렸다가 클로저 실행 후 락을 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 기다린 후 10초 동안 락 획득 및 클로저 실행...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

때로는 한 프로세스에서 락을 획득하고, 다른 프로세스에서 락을 해제하고 싶을 수 있습니다. 예를 들어, 웹 요청 시 락을 획득한 뒤, 해당 요청이 트리거한 큐 작업(queue job)이 끝날 때 락을 해제하는 시나리오가 있을 수 있습니다. 이때는 락의 범위 지정 "owner token"을 큐 작업에 전달하여, 해당 토큰으로 락을 복원하고 해제해야 합니다.

아래 예시에서는 락을 성공적으로 획득한 경우, 해당 owner 토큰을 전달하여 큐 작업을 디스패치합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

이후 큐 작업(`ProcessPodcast`)에서는 owner 토큰으로 락을 복원하고 해제하면 됩니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

특정 owner 여부와 무관하게 락을 강제로 해제하고 싶을 때는 `forceRelease` 메서드를 사용할 수 있습니다:

```php
Cache::lock('processing')->forceRelease();
```

<a name="locks-and-function-invocations"></a>
### 락과 함수 실행

`withoutOverlapping` 메서드는 아토믹 락을 획득한 상태에서 클로저를 실행하는 간단한 문법을 제공합니다. 이렇게 하면 인프라 전체에서 한 번에 하나의 클로저만 실행되도록 보장할 수 있습니다:

```php
Cache::withoutOverlapping('foo', function () {
    // 최대 10초 동안 락을 기다린 후 클로저 실행...
});
```

기본적으로 락은 클로저 실행이 끝날 때까지 유지되며, 락을 획득하기 위해 최대 10초까지 기다립니다. 이 값들은 추가 인수로 조정할 수 있습니다:

```php
Cache::withoutOverlapping('foo', function () {
    // 최대 5초 기다려 락을 획득, 120초 동안 유지...
}, lockSeconds: 120, waitSeconds: 5);
```

지정된 대기 시간 내에 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다.

<a name="cache-failover"></a>
## 캐시 페일오버 (Cache Failover)

`failover` 캐시 드라이버는 캐시 작업 중 기본 저장소에 장애가 발생했을 때 자동으로 다른 저장소로 전환해주는 기능을 제공합니다. `failover` 저장소의 기본 캐시 스토어에 문제가 생기면 Laravel이 리스트에 명시한 다음 저장소를 자동으로 사용합니다. 이는 특히 운영 환경에서 캐시의 신뢰도가 중요한 경우, 높은 가용성을 확보할 수 있게 해줍니다.

페일오버 캐시 저장소를 구성하려면, 드라이버를 `failover`로 지정하고, 순서대로 시도할 저장소 이름의 배열을 제공합니다. 기본적으로, Laravel의 `config/cache.php` 구성 파일에 예제 구성안이 포함되어 있습니다:

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

`failover` 드라이버를 사용하는 저장소를 구성했다면, 애플리케이션의 `.env` 파일에서 기본 캐시 저장소를 아래와 같이 설정해야 페일오버 기능을 사용할 수 있습니다:

```ini
CACHE_STORE=failover
```

캐시 저장소 작업 실패로 인해 페일오버가 활성화되면, Laravel은 `Illuminate\Cache\Events\CacheFailedOver` 이벤트를 디스패치하여 저장소 장애를 기록하거나 알릴 수 있도록 합니다.

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가하기 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성

커스텀 캐시 드라이버를 만들려면 먼저 `Illuminate\Contracts\Cache\Store` [컨트랙트](/docs/12.x/contracts)를 구현해야 합니다. 예를 들어, MongoDB 캐시 구현은 다음과 같이 구성할 수 있습니다:

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

각 메서드를 MongoDB 연결로 구현해주면 됩니다. 참고용으로 각 메서드 구현 방법은 [Laravel 프레임워크 소스코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 살펴보면 도움이 됩니다. 구현이 완료되면, `Cache` 파사드의 `extend` 메서드를 호출해 커스텀 드라이버 등록을 끝낼 수 있습니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 내에 `Extensions` 네임스페이스를 만들어 두는 것이 한 가지 방법입니다. 다만 Laravel에는 엄격한 디렉터리 구조가 없으므로, 본인이 원하는 대로 코드를 구조화해도 괜찮습니다.

<a name="registering-the-driver"></a>
### 드라이버 등록

커스텀 캐시 드라이버를 Laravel에 등록하려면, `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 `boot` 메서드에서 이미 캐시 값을 읽으려고 할 수 있으므로, 커스텀 드라이버는 `booting` 콜백 내부에서 등록하는 것이 좋습니다. 이렇게 하면, 서비스 프로바이더들의 `boot`가 호출되기 바로 전에, `register`가 모두 호출된 이후에 커스텀 드라이버가 등록됩니다.

아래는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에서 `register` 메서드를 이용해 `booting` 콜백을 등록하는 예시입니다:

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

`extend` 메서드의 첫 번째 인수는 드라이버의 이름입니다. 이 이름은 `config/cache.php`에서 `driver` 옵션과 대응됩니다. 두 번째 인수는 반드시 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저여야 하며, 이 클로저에는 [서비스 컨테이너](/docs/12.x/container) 인스턴스인 `$app`이 전달됩니다.

확장 등록을 마쳤다면, `CACHE_STORE` 환경 변수 또는 애플리케이션의 `config/cache.php`에서 `default` 옵션을 확장명으로 설정해 사용하면 됩니다.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 작업에 대해 코드를 실행하고 싶다면 캐시에서 디스패치하는 다양한 [이벤트](/docs/12.x/events)에 리스닝할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                      |
|--------------------------------------------------|
| `Illuminate\Cache\Events\CacheFlushed`           |
| `Illuminate\Cache\Events\CacheFlushing`          |
| `Illuminate\Cache\Events\CacheHit`               |
| `Illuminate\Cache\Events\CacheMissed`            |
| `Illuminate\Cache\Events\ForgettingKey`          |
| `Illuminate\Cache\Events\KeyForgetFailed`        |
| `Illuminate\Cache\Events\KeyForgotten`           |
| `Illuminate\Cache\Events\KeyWriteFailed`         |
| `Illuminate\Cache\Events\KeyWritten`             |
| `Illuminate\Cache\Events\RetrievingKey`          |
| `Illuminate\Cache\Events\RetrievingManyKeys`     |
| `Illuminate\Cache\Events\WritingKey`             |
| `Illuminate\Cache\Events\WritingManyKeys`        |

</div>

성능 향상을 위해 캐시 이벤트를 비활성화할 수도 있습니다. 이를 위해, 애플리케이션의 `config/cache.php` 파일에서 해당 캐시 저장소의 `events` 구성 옵션을 `false`로 설정하세요:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
