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
    - [캐시 헬퍼](#the-cache-helper)
- [캐시 태그](#cache-tags)
- [원자적 락](#atomic-locks)
    - [락 관리하기](#managing-locks)
    - [프로세스 간 락 관리하기](#managing-locks-across-processes)
- [캐시 페일오버](#cache-failover)
- [커스텀 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 처리하는 데이터 조회나 연산 중 일부는 CPU 사용량이 높거나 완료하는 데 여러 초가 소요될 수 있습니다. 이러한 경우, 조회한 데이터를 일정 시간 동안 캐싱하여 같은 데이터에 대한 후속 요청에서 빠르게 데이터를 제공할 수 있습니다. 캐시된 데이터는 보통 [Memcached](https://memcached.org) 또는 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히도, Laravel은 다양한 캐시 백엔드에 대해 일관성 있고 표현력 있는 API를 제공하므로, 빠른 데이터 조회 성능을 바탕으로 웹 애플리케이션의 속도를 향상시킬 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서 전체 애플리케이션에서 기본적으로 사용할 캐시 저장소(cache store)를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스 등 인기 있는 캐싱 백엔드를 기본으로 지원합니다. 또한 파일 기반 캐시 드라이버를 사용할 수 있으며, `array`와 `null` 캐시 드라이버는 자동화된 테스트에 적합한 편리한 캐시 백엔드로 제공됩니다.

캐시 설정 파일에는 이외에도 다양한 옵션들이 포함되어 있으니 필요에 따라 검토하면 됩니다. 기본적으로 Laravel은 `database` 캐시 드라이버를 사용하도록 설정되어 있으며, 직렬화된 캐시 객체들을 애플리케이션의 데이터베이스에 저장합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항 (Driver Prerequisites)

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 때는 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 이 테이블은 Laravel 기본 [데이터베이스 마이그레이션](/docs/12.x/migrations)인 `0001_01_01_000001_create_cache_table.php`에 포함되어 있습니다. 만약 애플리케이션에 해당 마이그레이션이 없다면, 아래의 `make:cache-table` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. 모든 Memcached 서버는 `config/cache.php` 설정 파일에 나열할 수 있으며, 이미 `memcached.servers` 항목이 기본으로 포함되어 있습니다.

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

필요하다면 `host` 옵션을 UNIX 소켓 경로로 지정할 수 있습니다. 이때, `port` 옵션은 `0`으로 설정해야 합니다.

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

Laravel에서 Redis 캐시를 사용하기 전에 PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer를 통해 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/12.x/sail)에는 이미 이 확장이 포함되어 있으며, [Laravel Cloud](https://cloud.laravel.com)나 [Laravel Forge](https://forge.laravel.com) 같은 공식 Laravel 애플리케이션 플랫폼에도 PhpRedis 확장이 기본으로 설치되어 있습니다.

Redis 설정에 대한 자세한 내용은 [Laravel의 Redis 문서](/docs/12.x/redis#configuration)를 참고하시기 바랍니다.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 캐시된 모든 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 보통 이 테이블은 `cache`라는 이름을 사용하는 것이 일반적이지만, 실제로는 `cache` 설정 파일 내의 `stores.dynamodb.table` 값이나 `DYNAMODB_CACHE_TABLE` 환경 변수에 따라 이름을 정해야 합니다.

이 테이블에는 파티션 키(partition key)로 사용할 문자열 컬럼을 하나 생성해야 하며, 컬럼명은 애플리케이션의 `cache` 설정 파일에 있는 `stores.dynamodb.attributes.key` 설정 값과 일치해야 합니다. 기본적으로 파티션 키는 `key`라는 이름을 사용합니다.

일반적으로 DynamoDB는 테이블에서 만료된 항목을 자동으로 삭제하지 않습니다. 따라서 [Time to Live(TTL) 활성화](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)가 필요합니다. 테이블의 TTL 속성을 설정할 때, TTL 속성명은 `expires_at`으로 지정해야 합니다.

다음으로, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

또한, DynamoDB 캐시 저장소 설정값이 올바르게 채워져 있는지도 확인해야 합니다. 보통 `AWS_ACCESS_KEY_ID`와 `AWS_SECRET_ACCESS_KEY` 같은 옵션들은 애플리케이션의 `.env` 설정 파일 내에 정의해야 합니다.

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 제공하는 `mongodb` 캐시 드라이버를 사용할 수 있으며, `mongodb` 데이터베이스 연결을 통해 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하므로 만료된 캐시 항목을 자동으로 삭제할 수 있습니다.

MongoDB의 설정에 대한 자세한 내용은 MongoDB [캐시 및 락 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하시기 바랍니다.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드(facade)를 사용할 수 있으며, 본 문서의 예시에서는 모두 `Cache` 파사드를 사용합니다. `Cache` 파사드는 Laravel 캐시 컨트랙트의 실제 구현에 간편하고 직관적으로 접근할 수 있는 인터페이스를 제공합니다.

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

`Cache` 파사드의 `store` 메서드를 사용하면 다양한 캐시 저장소에 손쉽게 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일의 `stores` 배열에 명시되어 있어야 합니다.

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기

캐시에 저장된 항목을 가져오려면 `Cache` 파사드의 `get` 메서드를 사용합니다. 항목이 캐시에 존재하지 않을 경우 `null`이 반환됩니다. 필요하다면, 두 번째 인수를 전달하여 항목이 존재하지 않을 때 반환할 기본값을 지정할 수 있습니다.

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저(Closure)를 전달하는 것도 가능합니다. 지정한 항목이 캐시에 존재하지 않을 경우, 클로저의 실행 결과가 반환됩니다. 클로저를 사용하면 데이터베이스나 외부 서비스에서 기본값을 지연 조회(defer)할 수 있습니다.

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인하기

`has` 메서드를 사용하면 특정 항목이 캐시에 존재하는지 확인할 수 있습니다. 이 메서드는, 항목은 존재하지만 값이 `null`인 경우에도 `false`를 반환합니다.

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소 시키기

`increment`와 `decrement` 메서드를 사용하면 캐시에 저장된 정수형 값을 증감시킬 수 있습니다. 두 메서드 모두 두 번째 인수로 증가/감소시킬 값(숫자)을 입력할 수 있습니다.

```php
// 존재하지 않을 경우 초기값 설정
Cache::add('key', 0, now()->plus(hours: 4));

// 값 증가/감소
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 가져오기 및 저장하기

가끔 캐시에서 항목을 가져오는 동시에, 요청한 항목이 없으면 기본값을 저장하고 싶을 때가 있습니다. 예를 들어 모든 사용자를 캐시에서 가져오거나, 캐시에 없으면 데이터베이스에서 조회하여 캐시에 저장하려고 할 때 유용합니다. 이럴 때는 `Cache::remember` 메서드를 사용하면 됩니다.

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

캐시에 해당 항목이 없을 경우, `remember` 메서드에 전달한 클로저가 실행되고, 그 결과가 캐시에 저장됩니다.

항목을 영구적으로 저장하고 싶다면 `rememberForever` 메서드를 사용할 수 있습니다.

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember` 메서드를 사용할 때, 일부 사용자에게는 캐시된 값이 만료된 경우 응답 속도가 느려질 수 있습니다. 일부 데이터 유형의 경우, 캐시된 값이 백그라운드에서 새로 계산되는 동안 부분적으로 만료(stale)된 데이터를 우선 제공하여 사용자의 체감 속도를 높일 수 있습니다. 이를 "stale-while-revalidate" 패턴이라고 하며, `Cache::flexible` 메서드로 구현할 수 있습니다.

`flexible` 메서드는 캐시 값이 "신선(fresh)"한 기간과 "stale" 상태가 될 수 있는 기간을 배열로 전달받습니다. 배열의 첫 번째 값은 캐시가 신선한 기간(초)이고, 두 번째 값은 만료 후 stale 데이터로 제공될 수 있는 기간(초)입니다.

- 신선 기간 내 요청은 즉시 캐시된 값을 반환합니다.
- 스테일(stale) 기간 중 요청하면 만료된 값을 반환하고, 동시에 [지연 함수](/docs/12.x/helpers#deferred-functions)가 등록되어 응답 후 백그라운드에서 캐시가 갱신됩니다.
- 두 번째 값이 지난 후 요청하면 캐시가 만료되었으므로 값을 즉시 재계산하여 반환합니다. 이 때 사용자는 느린 응답을 경험할 수 있습니다.

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 가져오고 삭제하기

캐시에서 항목을 가져온 뒤 해당 항목을 바로 삭제하고 싶다면 `pull` 메서드를 사용하면 됩니다. 이 메서드는 `get`과 같이, 항목이 없으면 `null`을 반환합니다.

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

캐시에 데이터를 저장하려면 `Cache` 파사드의 `put` 메서드를 사용합니다.

```php
Cache::put('key', 'value', $seconds = 10);
```

`put` 메서드에 저장 시간을 지정하지 않으면, 해당 항목은 무기한 저장됩니다.

```php
Cache::put('key', 'value');
```

저장 시간은 정수형 초(second) 대신, 캐시 만료 시점을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다.

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장하기

`add` 메서드는 기존에 항목이 없는 경우에만 캐시에 데이터를 저장합니다. 실제로 캐시에 추가되면 `true`를 반환하고, 그렇지 않으면 `false`를 반환합니다. `add` 메서드는 원자적(atomic) 동작입니다.

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 항목을 영구적으로 저장하기

항목을 만료되지 않도록 영구적으로 저장하려면 `forever` 메서드를 사용할 수 있습니다. 영구 저장된 항목은 만료되지 않으므로, `forget` 메서드를 통해 직접 캐시에서 제거해야 합니다.

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우, "영구" 저장된 항목도 캐시가 용량 한도에 도달하면 제거될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드를 사용하여 캐시에서 지정한 항목을 제거할 수 있습니다.

```php
Cache::forget('key');
```

또는 만료 초(second)를 0이나 음수로 지정하여 항목을 제거할 수도 있습니다.

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

캐시 전체를 비우려면 `flush` 메서드를 사용하세요.

```php
Cache::flush();
```

> [!WARNING]
> 캐시를 플러시(전체 삭제)하면 설정된 캐시 "prefix"가 적용되지 않으며, 캐시 내 모든 항목이 삭제됩니다. 여러 애플리케이션에서 캐시를 공유하는 경우에는 캐시 전체 삭제를 신중하게 고려해야 합니다.

<a name="cache-memoization"></a>
### 캐시 메모이제이션 (Cache Memoization)

Laravel의 `memo` 캐시 드라이버는 요청이나 한 번의 작업 실행 중에, 조회한 캐시 값을 메모리 내에 임시 저장할 수 있도록 해줍니다. 이를 통해 같은 실행 중에 반복적으로 캐시를 조회하는 작업의 성능을 대폭 향상시킬 수 있습니다.

메모이제이션 캐시를 사용하려면, `memo` 메서드를 호출하면 됩니다.

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드에는 특정 캐시 저장소의 이름을 인수로 전달할 수 있습니다. 이를 통해 해당 저장소를 기반으로 메모이제이션 드라이버를 사용할 수 있습니다.

```php
// 기본 캐시 저장소 사용
$value = Cache::memo()->get('key');

// Redis 캐시 저장소 사용
$value = Cache::memo('redis')->get('key');
```

같은 키에 대해 최초의 `get` 호출 시에는 실제 캐시 저장소에서 값을 조회하지만, 이후 같은 실행 내 반복 호출에서는 메모리에서 값을 반환합니다.

```php
// 실제 캐시 저장소에서 조회
$value = Cache::memo()->get('key');

// 캐시를 통하지 않고, 메모리에 저장된 값 반환
$value = Cache::memo()->get('key');
```

캐시 값을 수정하는 메서드(예: `put`, `increment`, `remember` 등)를 호출하면, 메모이제이션된 값을 자동으로 잊고(삭제) 이후 캐시 저장소에 요청이 위임됩니다.

```php
Cache::memo()->put('name', 'Taylor'); // 실제 캐시 저장소에 저장
Cache::memo()->get('name');           // 실제 캐시 저장소에서 조회
Cache::memo()->get('name');           // 메모리에서 반환

Cache::memo()->put('name', 'Tim');    // 메모이제이션 값 초기화, 새 값 저장
Cache::memo()->get('name');           // 다시 캐시 저장소에서 조회
```

<a name="the-cache-helper"></a>
### 캐시 헬퍼

`Cache` 파사드 외에도, 전역 함수 `cache`를 사용해 손쉽게 캐시 데이터를 조회 및 저장할 수 있습니다. `cache` 함수에 문자열 하나를 전달하면, 해당 키에 대한 값을 반환합니다.

```php
$value = cache('key');
```

키/값 쌍의 배열과 만료 시간을 전달하면, 해당 값들이 지정한 시간 동안 캐시에 저장됩니다.

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```

인수를 전달하지 않고 `cache` 함수를 호출하면, `Illuminate\Contracts\Cache\Factory` 구현 인스턴스를 반환하므로 다른 캐싱 메서드를 사용할 수도 있습니다.

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수의 호출을 테스트할 때, [파사드 테스트](/docs/12.x/mocking#mocking-facades)와 동일하게 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그 (Cache Tags)

> [!WARNING]
> 캐시 태그 기능은 `file`, `dynamodb`, `database` 캐시 드라이버에서는 지원되지 않습니다.

<a name="storing-tagged-cache-items"></a>
### 태그가 포함된 캐시 항목 저장하기

캐시 태그를 사용하면 관련된 캐시 항목을 태그로 그룹화한 후, 특정 태그가 할당된 항목만 모두 삭제할 수 있습니다. 태그된 캐시는 태그 이름의 배열을 인수로 전달해 접근할 수 있습니다. 예를 들어, 다음은 태그를 지정해 값을 캐시에 저장하는 방법입니다.

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### 태그가 포함된 캐시 항목 조회하기

태그를 지정하여 저장한 항목은, 동일한 태그를 지정하지 않으면 접근할 수 없습니다. 특정 태그 조합으로 태그된 항목을 조회하려면, 같은 순서로 태그 배열을 `tags` 메서드에 전달한 후, `get` 메서드로 키를 지정합니다.

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### 태그가 포함된 캐시 항목 삭제하기

하나 또는 여러 개의 태그가 지정된 모든 캐시 항목을 한꺼번에 삭제할 수 있습니다. 예를 들어, 아래 코드는 `people`, `authors` 중 하나라도 태그로 할당된 모든 캐시를 삭제합니다. 따라서 `Anne`과 `John` 모두 캐시에서 삭제됩니다.

```php
Cache::tags(['people', 'authors'])->flush();
```

반면 아래 코드에서는 `authors` 태그가 할당된 캐시만 삭제하므로, `Anne`만 삭제되고 `John`은 남아 있습니다.

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 원자적 락 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션에서 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 캐시 드라이버 중 하나를 기본 캐시 드라이버로 지정해야 합니다. 또한, 모든 서버가 같은 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리하기

원자적 락을 사용하면 레이스 컨디션(race condition) 걱정 없이 분산(서버 간) 락을 제어할 수 있습니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)는 서버에서 한 번에 하나의 원격 작업만 실행되도록 원자적 락을 사용합니다. 락을 생성하고 관리하려면 `Cache::lock` 메서드를 사용합니다.

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 락이 획득됨

    $lock->release();
}
```

`get` 메서드는 클로저를 인수로 받을 수도 있습니다. 이 경우, 클로저가 실행된 후 Laravel이 자동으로 락을 해제합니다.

```php
Cache::lock('foo', 10)->get(function () {
    // 10초 동안 락이 획득되고, 작업 후 자동으로 해제됩니다.
});
```

요청 시점에 락을 직접 획득할 수 없다면, 지정한 초만큼 기다리도록 Laravel에 요청할 수 있습니다. 해당 시간 내에 락을 못 얻으면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최대 5초 대기 후 락 획득...
} catch (LockTimeoutException $e) {
    // 락을 얻지 못함...
} finally {
    $lock->release();
}
```

위 예시는 `block` 메서드에 클로저를 전달하여 더 간단하게 쓸 수 있습니다. 이 경우 Laravel이 지정한 시간만큼 락 획득을 시도하고, 클로저 실행 뒤 락을 자동 해제합니다.

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 10초 동안 락 획득
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리하기

때때로 한 프로세스에서 락을 획득한 후, 다른 프로세스에서 락을 해제해야 할 경우가 있습니다. 예를 들어 웹 요청 중에 락을 획득하고, 요청에 의해 트리거된 큐 작업이 끝날 때 락을 해제할 수 있습니다. 이럴 때는 락을 인스턴스화할 때 제공되는 고유 "소유자 토큰(owner token)"을 큐 작업에 전달해 해당 락을 다시 복원해야 합니다.

다음 예시에서는 락을 성공적으로 획득하면 큐 작업을 디스패치하고, 락의 소유자 토큰을 `owner` 메서드를 통해 큐 작업에 전달합니다.

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

큐 작업 `ProcessPodcast` 내부에서는, 전달받은 소유자 토큰을 사용해 락을 복원하고 해제할 수 있습니다.

```php
Cache::restoreLock('processing', $this->owner)->release();
```

특정 락의 현재 소유자에 상관없이 강제로 락을 해제하고 싶다면, `forceRelease` 메서드를 사용할 수 있습니다.

```php
Cache::lock('processing')->forceRelease();
```

<a name="cache-failover"></a>
## 캐시 페일오버 (Cache Failover)

`failover` 캐시 드라이버는 캐시에 접근할 때 자동 페일오버 기능을 제공합니다. 만약 `failover` 저장소의 기본 캐시 저장소가 어떤 이유로 실패하면, Laravel은 다음에 구성된 저장소를 자동으로 사용합니다. 이는 운영 환경에서 캐시의 가용성이 매우 중요할 때 특히 유용합니다.

페일오버 캐시 저장소를 설정하려면, `failover` 드라이버를 지정하고 사용할 저장소 이름을 배열로 나열하면 됩니다. 기본적으로 Laravel은 `config/cache.php` 파일에 예시 페일오버 구성을 포함하고 있습니다.

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

페일오버 기능을 사용하려면, `.env` 파일에서 기본 캐시 저장소로 페일오버 저장소를 지정해야 합니다.

```ini
CACHE_STORE=failover
```

캐시 저장소 작업이 실패해 페일오버가 실행되면, Laravel은 `Illuminate\Cache\Events\CacheFailedOver` 이벤트를 디스패치합니다. 이를 이용하여 캐시 저장소 실패 로그나 알림 처리를 할 수 있습니다.

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가하기 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성하기

커스텀 캐시 드라이버를 만들기 위해서는 먼저 `Illuminate\Contracts\Cache\Store` [컨트랙트](/docs/12.x/contracts)를 구현해야 합니다. 예를 들어, MongoDB 캐시 드라이버 구현체는 다음과 유사할 수 있습니다.

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

각 메서드는 MongoDB 연결을 사용해서 직접 구현해야 합니다. 구체적인 구현 방법이 궁금하다면 [Laravel 프레임워크 소스코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고하시면 도움이 됩니다. 구현이 완료되면, `Cache` 파사드의 `extend` 메서드로 커스텀 드라이버 등록을 마무리할 수 있습니다.

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 위치시킬지 고민된다면, `app` 디렉토리 밑에 `Extensions` 네임스페이스를 만들면 하나의 방법이 될 수 있습니다. 하지만 Laravel은 디렉토리 구조에 대해 엄격한 제약이 없으므로 원하는 대로 자유롭게 구성하실 수 있습니다.

<a name="registering-the-driver"></a>
### 드라이버 등록하기

Laravel에 커스텀 캐시 드라이버를 등록하려면, `Cache` 파사드의 `extend` 메서드를 사용해야 합니다. 서비스 프로바이더의 `boot` 메서드 안에서 캐시 값을 읽고자 하는 경우가 있으므로, 커스텀 드라이버 등록이 모든 서비스 프로바이더의 `register` 메서드가 실행된 다음 실행되도록, `booting` 콜백에서 등록하는 것이 안전합니다. `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에서 `booting` 콜백을 등록하면 됩니다.

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

`extend` 메서드에 전달하는 첫 번째 인자는 드라이버의 이름이며, 이는 `config/cache.php`에서 `driver` 옵션에 대응합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하는 클로저입니다. 이 클로저에는 [서비스 컨테이너](/docs/12.x/container)의 인스턴스인 `$app`이 전달됩니다.

커스텀 확장(익스텐션)이 등록되면, 애플리케이션의 `CACHE_STORE` 환경 변수나 `config/cache.php` 파일의 `default` 옵션을 커스텀 드라이버 이름으로 변경하면 사용할 수 있습니다.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 작업 시 코드를 실행하려면, 캐시에서 디스패치되는 다양한 [이벤트](/docs/12.x/events)를 리스닝할 수 있습니다.

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

성능 향상을 위해, 특정 캐시 저장소에 대해 `config/cache.php`의 `events` 설정 옵션을 `false`로 두어 캐시 이벤트를 비활성화할 수 있습니다.

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
