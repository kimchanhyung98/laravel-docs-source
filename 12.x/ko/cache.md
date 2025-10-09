# 캐시 (Cache)

- [소개](#introduction)
- [구성](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [캐시 헬퍼](#the-cache-helper)
- [캐시 태그](#cache-tags)
- [원자적 락](#atomic-locks)
    - [락 관리하기](#managing-locks)
    - [프로세스 간 락 관리하기](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 수행하는 일부 데이터 조회 혹은 처리 작업은 CPU를 많이 사용하거나 완료까지 몇 초가 걸릴 수 있습니다. 이런 경우, 조회한 데이터를 일정 시간 동안 캐시에 저장하면 동일한 데이터 요청에 대해 훨씬 빠르게 응답할 수 있습니다. 캐시된 데이터는 주로 [Memcached](https://memcached.org) 나 [Redis](https://redis.io) 같은 매우 빠른 데이터 저장소에 보관합니다.

Laravel은 다양한 캐시 백엔드를 위한 직관적이고 통합된 API를 제공하므로, 각 백엔드의 빠른 데이터 조회 성능을 활용하여 웹 애플리케이션의 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 구성 (Configuration)

애플리케이션의 캐시 구성 파일은 `config/cache.php`에 위치합니다. 이 파일에서 애플리케이션 전반에 사용될 기본 캐시 저장소(store)를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스와 같은 인기 있는 캐시 백엔드를 기본으로 지원합니다. 또한 파일 기반 캐시 드라이버가 제공되며, `array`와 `null` 캐시 드라이버는 자동화된 테스트에 유용한 캐시 백엔드를 제공합니다.

캐시 구성 파일에는 이 외에도 다양한 옵션이 포함되어 있으니, 내용을 확인해 보시기 바랍니다. 기본적으로 Laravel은 `database` 캐시 드라이버를 사용하도록 설정되어 있으며, 직렬화된 캐시 객체를 애플리케이션의 데이터베이스에 보관합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항 (Driver Prerequisites)

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 때는 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 보통 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있지만, 만약 이 마이그레이션이 없다면 `make:cache-table` Artisan 명령어를 사용하여 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. 모든 Memcached 서버를 `config/cache.php` 구성 파일에 나열할 수 있습니다. 이 파일에는 시작을 위한 `memcached.servers` 항목이 미리 포함되어 있습니다:

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

필요하다면, `host` 옵션에 UNIX 소켓 경로를 지정할 수 있습니다. 이 경우에는 `port` 옵션을 `0`으로 설정해야 합니다:

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

Laravel에서 Redis 캐시를 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer로 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/12.x/sail)에는 이미 이 확장 모듈이 포함되어 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com), [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 배포 플랫폼들도 PhpRedis 확장 모듈을 기본 탑재하고 있습니다.

Redis 구성에 관한 더 자세한 정보는 [Laravel Redis 문서](/docs/12.x/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 캐시 데이터를 저장할 DynamoDB 테이블을 먼저 생성해야 합니다. 일반적으로 이 테이블 이름은 `cache`이어야 합니다. 하지만 테이블 이름은 `cache` 구성 파일 내 `stores.dynamodb.table` 설정 값에 따라 지정해야 하며, 이 이름은 `DYNAMODB_CACHE_TABLE` 환경 변수로도 설정할 수 있습니다.

테이블에는 문자열 타입의 파티션 키가 있어야 하며, 이는 `cache` 구성 파일의 `stores.dynamodb.attributes.key` 항목의 값과 일치해야 합니다. 기본값은 `key`입니다.

DynamoDB는 만료된 항목을 테이블에서 자동으로 제거하지 않습니다. 따라서 반드시 [Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 테이블에 활성화해야 합니다. TTL 설정 시에는 속성(attribute) 이름을 `expires_at`으로 지정합니다.

다음으로, Laravel 애플리케이션에서 DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다:

```shell
composer require aws/aws-sdk-php
```

또한, DynamoDB 캐시 저장소 구성 옵션에 대한 값도 제대로 제공되어야 합니다. 보통 `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` 등과 같은 옵션은 애플리케이션의 `.env` 구성 파일에 정의되어야 합니다:

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 `mongodb` 캐시 드라이버를 제공하며, `mongodb` 데이터베이스 연결을 사용하여 구성할 수 있습니다. MongoDB는 TTL 인덱스를 지원하므로, 만료된 캐시 항목이 자동으로 삭제됩니다.

MongoDB 구성 방법에 대한 더 자세한 내용은 MongoDB [Cache and Locks 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하세요.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드(facade)를 사용할 수 있습니다. 본 문서 전체에서는 `Cache` 파사드를 사용합니다. `Cache` 파사드는 Laravel 캐시 계약의 내부 구현에 간편하고 직관적으로 접근할 수 있게 해줍니다:

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

`Cache` 파사드를 사용하면 `store` 메서드를 통해 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 구성 파일의 `stores` 배열에 정의된 저장소 이름과 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 가져오는 데 사용됩니다. 항목이 캐시에 없으면 `null`이 반환됩니다. 항목이 존재하지 않을 때 반환하려는 기본값을 두 번째 인수로 입력할 수도 있습니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값에 클로저를 전달할 수도 있습니다. 이 경우 항목이 없을 때 클로저의 결과가 반환됩니다. 클로저를 사용하면 기본값을 데이터베이스나 외부 서비스로부터 지연해서 가져올 수 있게 됩니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인

`has` 메서드는 항목이 캐시에 존재하는지 확인할 수 있습니다. 이 메서드는 항목이 존재하지만 그 값이 `null`인 경우에도 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가 및 감소

`increment`와 `decrement` 메서드는 캐시에 저장된 정수 항목의 값을 조정할 때 사용합니다. 두 메서드 모두 항목 값을 얼마만큼 증가 또는 감소시킬지 선택적으로 두 번째 인수를 받을 수 있습니다:

```php
// 값이 없으면 초기화합니다...
Cache::add('key', 0, now()->addHours(4));

// 값 증가 또는 감소...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 가져오고 저장하기

때로는 항목을 캐시에서 가져오되, 없으면 기본값을 저장하고 싶을 때가 있습니다. 예를 들어, 사용자 목록을 캐시에서 가져오거나 없다면 데이터베이스에서 가져와 캐시에 저장하는 경우입니다. 이런 경우에는 `Cache::remember` 메서드를 사용하면 됩니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

항목이 캐시에 없으면, `remember` 메서드에 전달된 클로저가 실행되어 그 결과가 캐시에 저장됩니다.

항목이 없을 때 영구적으로 저장하려면 `rememberForever` 메서드를 사용할 수도 있습니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember` 메서드를 사용할 때, 일부 사용자는 캐시 값이 만료된 경우 느린 응답을 경험할 수 있습니다. 어떤 데이터의 경우, 백그라운드에서 새로운 값이 계산되는 동안 만료된 데이터를 임시로 제공하는 것이 유용할 수 있습니다. 이렇게 하면 일부 사용자는 캐시 계산으로 인한 느린 응답 대신 약간 오래된 데이터를 받게 됩니다. 이를 "stale-while-revalidate" 패턴이라고 하며, `Cache::flexible` 메서드에서 이 패턴을 사용할 수 있습니다.

`flexible` 메서드는 "신선"한 기간과 만료 후 "stale"로 간주될 기간을 배열로 받습니다. 배열의 첫 번째 값은 캐시가 신선하게 유지되는 초 단위 시간이고, 두 번째 값은 데이터를 stale 상태로 제공할 수 있는 최대 시간입니다.

신선한 기간 내에 요청이 오면 캐시된 데이터를 바로 제공합니다. stale 기간 내에는 만료된 캐시를 우선 응답하고, 응답 이후 [지연된 함수](/docs/12.x/helpers#deferred-functions)가 실행되어 캐시 값을 업데이트합니다. 두 번째 시간 이후에는 즉시 캐시를 재계산해 반환하며, 이때는 사용자가 느린 응답을 경험할 수 있습니다:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 가져오고 삭제하기

캐시에서 항목을 가져오고 바로 삭제해야 한다면 `pull` 메서드를 사용할 수 있습니다. 해당 항목이 없으면 `null`이 반환됩니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

`Cache` 파사드의 `put` 메서드를 사용해 캐시에 항목을 저장할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

만약 저장 시간을 지정하지 않으면, 해당 항목은 만료되지 않고 무기한 저장됩니다:

```php
Cache::put('key', 'value');
```

저장 기간을 초 단위로 정수값 대신, 만료 시점을 나타내는 `DateTime` 인스턴스로 전달할 수도 있습니다:

```php
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장

`add` 메서드는 캐시에 해당 항목이 없을 때에만 추가합니다. 항목이 캐시에 실제로 저장되었을 경우 `true`를, 이미 존재할 경우에는 `false`를 반환합니다. 이 메서드는 원자적(atomic) 연산입니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 영구적으로 항목 저장하기

`forever` 메서드는 항목을 만료 없이 영구적으로 캐시에 저장합니다. 영구 저장된 항목은 반드시 `forget` 메서드를 사용해 직접 삭제해주어야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용할 경우, "영구적으로" 저장된 항목도 캐시 크기가 한도에 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

캐시의 항목을 제거하려면 `forget` 메서드를 사용합니다:

```php
Cache::forget('key');
```

만료 기간을 0이나 음수로 지정하여 항목을 제거할 수도 있습니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

전체 캐시를 비우려면 `flush` 메서드를 사용합니다:

```php
Cache::flush();
```

> [!WARNING]
> 캐시를 플러시할 경우, 캐시에 설정된 "prefix"와 무관하게 모든 캐시 항목이 삭제됩니다. 다른 애플리케이션과 캐시를 공유하는 경우에는 각별히 주의해서 사용하세요.

<a name="cache-memoization"></a>
### 캐시 메모이제이션 (Cache Memoization)

Laravel의 `memo` 캐시 드라이버를 사용하면, 한 번 해석된(조회된) 캐시 값을 한 요청(request) 또는 작업(job) 실행 동안 메모리(램)에 임시로 저장할 수 있습니다. 이렇게 하면 동일한 실행 내에서 동일 데이터를 반복적으로 읽을 때 캐시 저장소 접근을 생략할 수 있어 성능이 크게 향상됩니다.

메모이제이션 캐시를 사용하려면 `memo` 메서드를 호출하세요:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드는 선택적으로 캐시 저장소 이름을 받을 수 있으며, 이 경우 지정한 저장소를 기반으로 메모이제이션 드라이버가 동작합니다:

```php
// 기본 캐시 저장소 사용
$value = Cache::memo()->get('key');

// Redis 캐시 저장소 사용
$value = Cache::memo('redis')->get('key');
```

특정 키에 대해 첫 번째 `get` 호출은 캐시 저장소에서 값을 읽어오고, 동일 요청 중 이후 호출은 메모리에서 값을 반환하므로 캐시 저장소 접근이 발생하지 않습니다:

```php
// 캐시 저장소에서 읽음
$value = Cache::memo()->get('key');

// 이후에는 메모리에서 반환 (캐시 미접근)
$value = Cache::memo()->get('key');
```

캐시 값을 변경하는 메서드(`put`, `increment`, `remember` 등)를 호출하면, 메모이제이션된 값을 자동으로 잊고(삭제) 변경 요청을 실제 캐시 저장소에 전달합니다:

```php
Cache::memo()->put('name', 'Taylor'); // 실제 캐시 저장
Cache::memo()->get('name');           // 실제 캐시에서 읽음
Cache::memo()->get('name');           // 메모리에서 반환

Cache::memo()->put('name', 'Tim');    // 메모이제이션 값 초기화, 새 값 저장
Cache::memo()->get('name');           // 캐시 저장소에서 다시 읽음
```

<a name="the-cache-helper"></a>
### 캐시 헬퍼 (The Cache Helper)

`Cache` 파사드 대신, 전역 `cache` 함수를 이용해 캐시 데이터를 직접 조회하거나 저장할 수 있습니다. `cache` 함수에 문자열 하나만 넣으면 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키/값 쌍을 배열로 전달하고 만료 시간을 지정하면, 해당 값을 지정한 기간만큼 캐시에 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

인수가 없는 경우, `cache` 함수는 `Illuminate\Contracts\Cache\Factory` 구현체의 인스턴스를 반환하므로 다양한 캐시 관련 메서드를 호출할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수를 테스트할 때도 [파사드 테스트](/docs/12.x/mocking#mocking-facades)와 마찬가지로 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그 (Cache Tags)

> [!WARNING]
> `file`, `dynamodb`, 또는 `database` 캐시 드라이버 사용 시에는 캐시 태그를 지원하지 않습니다.

<a name="storing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 저장

캐시 태그를 사용하면 관련된 항목에 태그를 붙여두고, 해당 태그가 붙은 모든 캐시 값을 한 번에 삭제할 수 있습니다. 태그는 순서가 정해진 배열 형태로 전달하며, 아래 예시처럼 지정된 태그로 값을 등록할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 조회

태그로 저장한 항목을 조회할 때는 저장할 때 사용한 동일한 태그 목록을 `tags` 메서드에 전달한 후, 조회하려는 키로 `get`을 호출해야 합니다:

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 삭제

특정 태그나 태그 목록이 부여된 모든 항목을 삭제할 수 있습니다. 아래 코드는 `people`, `authors` 태그가 부여된 모든 캐시를 삭제하므로 `Anne`과 `John` 모두 캐시에서 제거됩니다:

```php
Cache::tags(['people', 'authors'])->flush();
```

반면 아래 코드는 `authors` 태그가 부여된 캐시만 삭제하므로, `Anne`만 삭제되고 `John`은 남게 됩니다:

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 원자적 락 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리하기

원자적(atomic) 락을 사용하면 경쟁 조건(race condition)에 대해 걱정하지 않고 분산 락을 안전하게 제어할 수 있습니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)는 한 번에 하나의 원격 작업만 서버에서 실행되도록 원자적 락을 사용합니다. 락을 생성하고 관리하려면 `Cache::lock` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 락 획득...

    $lock->release();
}
```

`get` 메서드는 클로저도 받을 수 있습니다. 클로저 실행 후, Laravel이 자동으로 락을 해제해줍니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 10초 동안 락 획득 후 자동 해제...
});
```

요청 당시 락을 사용할 수 없을 경우, 락을 획득할 때까지 지정한 시간(초) 동안 대기하도록 Laravel에 지시할 수 있습니다. 지정한 시간 내 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최대 5초 대기 후 락 획득 성공...
} catch (LockTimeoutException $e) {
    // 락 획득 실패...
} finally {
    $lock->release();
}
```

위 예시는 `block` 메서드에 클로저를 전달해 좀 더 간결하게 작성할 수도 있습니다. 클로저가 실행된 후 락은 자동 해제됩니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 10초간 락 획득...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리하기

경우에 따라 한 프로세스에서 락을 획득한 뒤, 다른 프로세스에서 락을 해제하고 싶을 때가 있습니다. 예를 들어, 웹 요청에서 락을 획득한 후, 해당 요청에서 트리거된 큐 작업(job)이 최종적으로 락을 해제해야 할 수도 있습니다. 이때 락의 범위(owner token)를 큐 작업에 전달하면, 작업 내에서 이 토큰으로 다시 락을 복원할 수 있습니다.

아래 예시에서는 락을 획득하면 큐 작업을 디스패치하며, 락의 owner 토큰을 작업에 넘깁니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

큐 작업(`ProcessPodcast` job) 내에서는 owner 토큰을 활용해 락을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

현재 owner 여부 상관 없이 락을 강제로 해제하려면 `forceRelease` 메서드를 사용하세요:

```php
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가하기 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성하기

커스텀 캐시 드라이버를 만들기 위해서는 먼저 `Illuminate\Contracts\Cache\Store` [계약](/docs/12.x/contracts)을 구현해야 합니다. 예를 들어, MongoDB 캐시 구현은 다음과 비슷할 수 있습니다:

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

각 메서드는 MongoDB 연결을 사용해 구현하면 됩니다. 각 메서드 구현 예시는 [Laravel 프레임워크 소스 코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고하면 좋습니다. 구현이 완료되면, `Cache` 파사드의 `extend` 메서드를 호출해 드라이버 등록을 마칩니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 내에 `Extensions` 네임스페이스를 만들어 둘 수 있습니다. Laravel은 애플리케이션 구조를 엄격하게 강제하지 않으므로, 원하는 방식으로 자유롭게 구성해도 괜찮습니다.

<a name="registering-the-driver"></a>
### 드라이버 등록하기

커스텀 드라이버를 Laravel에 등록하려면, `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더의 `boot` 메서드에서 캐시 값을 읽을 수도 있으므로, 드라이버 등록 코드는 `boot` 메서드 호출 직전에 실행되어야 합니다. 이를 위해 `App\Providers\AppServiceProvider`의 `register` 메서드에서 `booting` 콜백에 등록합니다:

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

`extend` 메서드의 첫 번째 인자는 드라이버 이름이며, 이는 `config/cache.php` 파일 `driver` 옵션 값에 해당합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하는 클로저입니다. 이 클로저에는 [서비스 컨테이너](/docs/12.x/container)의 인스턴스인 `$app`이 전달됩니다.

확장 드라이버를 등록했다면, 애플리케이션의 `CACHE_STORE` 환경 변수 혹은 `config/cache.php`의 `default` 옵션 값을 확장 드라이버 이름으로 변경하세요.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 작업마다 코드를 실행하고 싶다면, 캐시에서 발생하는 다양한 [이벤트](/docs/12.x/events)를 리스닝할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                     |
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

성능 향상을 위해, 애플리케이션의 `config/cache.php` 파일에서 특정 캐시 저장소에 대해 `events` 옵션을 `false`로 설정해 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
