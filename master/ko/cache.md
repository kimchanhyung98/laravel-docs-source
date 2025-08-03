# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 사전 요구사항](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 헬퍼](#the-cache-helper)
- [원자적 잠금 (Atomic Locks)](#atomic-locks)
    - [잠금 관리](#managing-locks)
    - [프로세스 간 잠금 관리](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

애플리케이션에서 수행하는 데이터 조회나 처리 작업 중 일부는 CPU 자원을 많이 소모하거나 완료하는 데 몇 초가 걸릴 수 있습니다. 이런 경우, 조회한 데이터를 일정 시간 동안 캐시하여 이후 같은 데이터 요청에 대해 빠르게 응답하는 것이 일반적입니다. 캐시된 데이터는 대개 [Memcached](https://memcached.org)나 [Redis](https://redis.io) 같은 매우 빠른 데이터 저장소에 보관됩니다.

다행히도, Laravel은 다양한 캐시 백엔드에 대해 표현식이 풍부하고 통일된 API를 제공하기 때문에 이를 손쉽게 활용하여 데이터 조회 속도를 높이고 웹 애플리케이션을 빠르게 만들 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 있습니다. 이 파일에서 애플리케이션 전체에서 기본으로 사용할 캐시 저장소를 지정할 수 있습니다. Laravel은 기본적으로 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스 같은 인기 있는 캐시 백엔드를 지원합니다. 또한 파일 기반 캐시 드라이버도 제공하며, `array`와 "null" 캐시 드라이버는 자동화된 테스트용으로 편리한 캐시 백엔드를 제공합니다.

해당 캐시 설정 파일에는 다양한 옵션이 포함되어 있으니 필요에 따라 검토하세요. 기본적으로 Laravel은 `database` 캐시 드라이버를 사용하도록 설정되어 있는데, 이 드라이버는 직렬화된 캐시된 객체들을 애플리케이션의 데이터베이스에 저장합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="prerequisites-database"></a>
#### 데이터베이스 (Database)

`database` 캐시 드라이버를 사용할 때는 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 보통 이 테이블은 Laravel 기본 마이그레이션인 `0001_01_01_000001_create_cache_table.php`에 포함되어 있습니다. 만약 애플리케이션에 해당 마이그레이션이 없다면, Artisan 명령어 `make:cache-table`을 사용하여 테이블을 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. `config/cache.php` 설정 파일에서 모든 Memcached 서버를 지정할 수 있습니다. 이 파일에는 기본적으로 `memcached.servers` 항목이 포함되어 있어 쉽게 시작할 수 있습니다:

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

필요에 따라 `host` 옵션을 UNIX 소켓 경로로 설정할 수도 있습니다. 이 경우 `port` 옵션은 `0`으로 설정해야 합니다:

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

Laravel에서 Redis 캐시를 사용하기 전에, PECL을 통해 PhpRedis PHP 확장이나 Composer를 통해 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/master/sail)에는 이미 이 확장이 포함되어 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com)와 [Laravel Forge](https://forge.laravel.com) 같은 공식 Laravel 애플리케이션 플랫폼에는 기본적으로 PhpRedis 확장이 설치되어 있습니다.

Redis 설정에 대한 자세한 내용은 [Laravel 문서의 Redis 페이지](/docs/master/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에는, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 보통 이 테이블 이름은 `cache`로 지정하지만, `cache` 설정 파일 내 `stores.dynamodb.table` 설정 값에 따라 변경할 수 있습니다. 테이블 이름은 `DYNAMODB_CACHE_TABLE` 환경 변수로도 설정할 수 있습니다.

이 테이블에는 기본적으로 `stores.dynamodb.attributes.key` 설정 항목과 일치하는 이름을 가진 문자형 파티션 키가 필요하며, 기본값은 `key`입니다.

일반적으로 DynamoDB는 만료된 아이템을 자동으로 제거하지 않으므로 테이블에 [Time to Live(TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활성화하는 것이 좋습니다. TTL 속성 이름을 `expires_at`로 설정해야 합니다.

다음으로, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치하세요:

```shell
composer require aws/aws-sdk-php
```

추가로, DynamoDB 캐시 저장소 설정 옵션 값들이 적절히 제공되어야 합니다. 보통 `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`와 같은 값은 애플리케이션의 `.env` 파일에 정의합니다:

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 제공하는 `mongodb` 캐시 드라이버를 사용할 수 있으며, `mongodb` 데이터베이스 연결을 통해 설정합니다. MongoDB는 TTL 인덱스를 지원하여 만료된 캐시 항목을 자동으로 제거할 수 있습니다.

MongoDB 설정에 관한 자세한 내용은 MongoDB [Cache and Locks 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하세요.

<a name="cache-usage"></a>
## 캐시 사용법

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드를 사용할 수 있습니다. 이 문서 전반에서 `Cache` 파사드를 활용할 것이며, Laravel 캐시 계약의 내부 구현체를 간편하고 짧게 접근할 수 있도록 도와줍니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 애플리케이션에 등록된 모든 사용자 목록을 표시합니다.
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

`Cache` 파사드에서 `store` 메서드를 사용하면 여러 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일의 `stores` 배열 내 저장소 이름과 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 가져오는 데 사용합니다. 지정한 키가 캐시에 없으면 `null`이 반환됩니다. 두 번째 인자로 기본값을 전달하면, 해당 키가 존재하지 않을 경우 기본값을 대신 반환합니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저(익명 함수)를 전달할 수도 있습니다. 캐시에 해당 아이템이 없으면 클로저 실행 결과가 반환되며, 이는 데이터베이스나 외부 서비스에서 기본값을 지연해서 조회할 때 유용합니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 확인하기

`has` 메서드는 해당 키가 캐시에 존재하는지 확인할 때 사용합니다. 단, 키가 존재하더라도 값이 `null`이면 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가 / 감소

`increment`와 `decrement` 메서드는 캐시에 저장된 정수형 값의 증감에 사용합니다. 두 메서드는 증감할 양을 두 번째 인자로 전달할 수 있습니다:

```php
// 값이 없으면 처음에 초기화합니다...
Cache::add('key', 0, now()->addHours(4));

// 값을 증가 또는 감소시킵니다...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 가져오기 및 저장

때때로 캐시에서 항목을 가져오되, 해당 항목이 없을 때는 기본값을 생성해 캐시에 저장하고 결과를 반환하고자 할 때가 있습니다. 예를 들어, 모든 사용자를 캐시에서 가져오거나 없으면 데이터베이스에서 가져오고 캐시에 저장할 수 있습니다. `Cache::remember` 메서드를 통해 수행할 수 있습니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

캐시에 항목이 없으면, `remember` 메서드에 전달한 클로저가 실행되어 반환값이 캐시에 저장됩니다.

항목을 영구적으로 저장하려면 `rememberForever` 메서드를 사용하세요:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate (느슨한 재검증)

`Cache::remember` 메서드를 사용할 때, 캐시된 값이 만료되면 일부 사용자는 느린 응답 시간을 경험할 수 있습니다. 특정 데이터 유형에서는 약간 오래된 상태의 데이터를 제공하면서 백그라운드에서 재계산하여 응답 지연을 방지하는 것이 유용할 수 있습니다. 이를 흔히 "stale-while-revalidate" 패턴이라 하며, `Cache::flexible` 메서드는 이 패턴 구현을 제공합니다.

`flexible` 메서드는 배열을 통해 캐시가 "신선(fresh)"한 기간과 "딱딱해진(stale)" 기간(재계산이 필요해지는 시점)을 초 단위로 지정합니다.

- 배열의 첫 번째 값: 캐시가 신선한 기간 (초 단위)
- 두 번째 값: 신선하진 않지만 캐시된 값이 재계산되기 전까지 딱딱해진 상태로 제공할 수 있는 최대 기간

해당 시간 내 요청이 오면 즉시 캐시 값을 반환합니다. 만약 딱딱해진 기간 내 요청이 발생하면, 사용자에게는 딱딱해진 값이 전달되고 [지연 함수](/docs/master/helpers#deferred-functions)가 등록되어 응답 후 백그라운드에서 캐시가 갱신됩니다. 두 번째 기간이 지나면 캐시는 만료되고 새로운 값을 즉시 재계산하며, 이때 응답이 느려질 수 있습니다:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 가져오기 및 삭제

캐시에서 항목을 가져온 뒤 삭제하고 싶다면, `pull` 메서드를 사용하세요. `get` 메서드와 마찬가지로 키가 존재하지 않으면 `null`을 반환합니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

`Cache` 파사드의 `put` 메서드를 사용하여 캐시에 항목을 저장할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

저장 시간을 지정하지 않으면, 항목은 무기한 저장됩니다:

```php
Cache::put('key', 'value');
```

초 단위 정수가 아니라, 만료 일시를 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다:

```php
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장하기

`add` 메서드는 지정한 키가 캐시에 없을 때만 항목을 추가합니다. 캐시에 실제로 저장되었으면 `true`를, 이미 존재해서 추가되지 않았다면 `false`를 반환합니다. 이 메서드는 원자적(atomic) 연산입니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 무기한 저장하기

`forever` 메서드는 캐시에 항목을 만료 없이 영구 저장합니다. 이 항목은 수동으로 `forget` 메서드를 호출하여 제거해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우, "영구" 저장된 항목도 캐시 크기 제한에 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드를 통해 캐시에서 항목을 삭제할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간을 0 또는 음수로 설정하여 항목을 제거할 수도 있습니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메서드는 캐시를 전체 비웁니다:

```php
Cache::flush();
```

> [!WARNING]
> `flush`는 캐시의 접두사(prefix)를 무시하고 모든 캐시 항목을 제거합니다. 여러 애플리케이션에서 공유하는 캐시라면 신중히 사용하세요.

<a name="the-cache-helper"></a>
### 캐시 헬퍼 함수

`Cache` 파사드 외에 글로벌 `cache` 함수를 사용하여 캐시에 데이터를 저장하거나 조회할 수 있습니다. 한 개의 문자열 인자를 넘기면 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키와 값 쌍을 배열로 넘기고 만료 시간을 지정하면, 캐시에 데이터를 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

인자를 넘기지 않으면, `Illuminate\Contracts\Cache\Factory` 구현체 인스턴스를 반환해 다른 캐시 메서드를 호출할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 테스트 시 글로벌 `cache` 함수 호출을 모의할 때, `Cache::shouldReceive` 메서드를 `facade`를 테스트할 때처럼 사용할 수 있습니다. ([facade 테스트 문서](/docs/master/mocking#mocking-facades) 참고)

<a name="atomic-locks"></a>
## 원자적 잠금 (Atomic Locks)

> [!WARNING]
> 본 기능을 사용하려면 애플리케이션 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file` 또는 `array` 드라이버여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 잠금 관리

원자적 잠금은 경쟁 조건(race condition) 걱정 없이 분산 잠금을 다룰 수 있는 기능입니다. 예를 들어 [Laravel Cloud](https://cloud.laravel.com)는 원자적 잠금을 사용해 한 서버에서 한 번에 한 원격 작업만 실행되도록 보장합니다. `Cache::lock` 메서드로 잠금을 생성하고 관리할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 잠금 획득됨...

    $lock->release();
}
```

`get` 메서드는 클로저도 인자로 받습니다. 클로저가 실행된 뒤 자동으로 잠금이 해제됩니다:

```php
Cache::lock('foo', 10)->get(function () {
    // 10초 동안 잠금 획득 및 자동 해제...
});
```

잠금이 즉시 가능하지 않을 경우 지정한 시간만큼 대기할 수도 있습니다. 제한 시간 내 잠금을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다:

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최대 5초 대기 후 잠금 획득됨...
} catch (LockTimeoutException $e) {
    // 잠금 획득 실패...
} finally {
    $lock->release();
}
```

위 코드는 `block` 메서드에 클로저를 전달해 더 간결하게 작성할 수 있습니다. 이 경우 Laravel이 지정된 시간만큼 잠금 획득을 시도하고, 클로저 종료 후 자동으로 잠금을 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 10초간 잠금 획득...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 잠금 관리

가끔 한 프로세스에서 잠금을 획득하고 다른 프로세스에서 해제하는 경우가 있습니다. 예를 들어 웹 요청 시 잠금을 얻고, 해당 요청에 의해 큐 작업이 실행되어 작업 완료 시 잠금을 해제하는 상황입니다. 이때 잠금의 범위 "소유자 토큰(owner token)"을 큐 작업으로 전달하여, 작업이 이를 사용해 잠금을 복원하고 해제하도록 합니다.

아래 예시는 잠금 획득 성공 시 큐 작업을 디스패치하고, 잠금 소유자 토큰을 전달하는 코드입니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

애플리케이션의 `ProcessPodcast` 작업 안에서는 받은 소유자 토큰으로 잠금을 복원하고 해제합니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

잠금 소유자에 상관없이 잠금을 강제로 해제하고 싶다면 `forceRelease` 메서드를 사용하세요:

```php
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가하기

<a name="writing-the-driver"></a>
### 드라이버 작성하기

커스텀 캐시 드라이버를 만들려면 먼저 `Illuminate\Contracts\Cache\Store` [계약](/docs/master/contracts)을 구현해야 합니다. 예를 들어 MongoDB 캐시 구현은 아래와 같이 보일 수 있습니다:

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

MongoDB 연결을 사용해 위 각 메서드를 구현하면 됩니다. 구현 참고용으로, [Laravel 프레임워크 소스코드](https://github.com/laravel/framework)에서 `Illuminate\Cache\MemcachedStore`를 살펴보면 도움이 됩니다. 구현이 완료되면 `Cache` 파사드의 `extend` 메서드로 커스텀 드라이버 등록을 마칩니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드는 `app` 디렉터리에 `Extensions` 네임스페이스를 만들어 두는 것이 한 방법입니다. 다만 Laravel은 엄격한 애플리케이션 구조를 강제하지 않으니, 자유롭게 원하는 구조로 작성하세요.

<a name="registering-the-driver"></a>
### 드라이버 등록하기

Laravel에 커스텀 캐시 드라이버를 등록하려면 `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 `boot` 메서드에서 캐시 값을 읽으려 할 수 있으므로, 등록은 `booting` 콜백 안에서 진행하는 게 좋습니다. `booting` 콜백은 모든 서비스 프로바이더가 `register` 메서드를 호출한 뒤, `boot` 메서드 호출 직전에 실행됩니다. 따라서 `App\Providers\AppServiceProvider`의 `register` 메서드 안에 `booting` 콜백을 아래처럼 등록합니다:

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

`extend` 메서드의 첫 번째 인자는 드라이버 이름이며, `config/cache.php` 설정 파일의 `driver` 옵션과 일치시켜야 합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저이며, 이 클로저는 서비스 컨테이너 인스턴스인 `$app`을 인자로 받습니다.

확장이 등록된 후에는 `.env` 환경변수 `CACHE_STORE`나 `config/cache.php`의 `default` 옵션을 확장한 드라이버 이름으로 변경하세요.

<a name="events"></a>
## 이벤트

모든 캐시 동작 시 코드를 실행하려면 캐시가 발생시키는 여러 [이벤트](/docs/master/events)를 구독할 수 있습니다:

<div class="overflow-auto">

| 이벤트명 |
| --- |
| `Illuminate\Cache\Events\CacheHit` |
| `Illuminate\Cache\Events\CacheMissed` |
| `Illuminate\Cache\Events\KeyForgotten` |
| `Illuminate\Cache\Events\KeyWritten` |

</div>

성능 향상을 위해 특정 캐시 저장소에서 캐시 이벤트를 비활성화하려면, 애플리케이션 `config/cache.php`의 해당 저장소 설정 내 `events` 옵션을 `false`로 설정하세요:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```