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
- [원자적 락 (Atomic Locks)](#atomic-locks)
    - [락 관리하기](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 데이터를 가져오거나 처리하는 작업이 CPU 집약적일 수 있고 완료까지 몇 초가 걸릴 때가 있습니다. 이런 경우, 가져온 데이터를 일정 시간 동안 캐시해 두면 같은 데이터를 이후 요청에서 빠르게 불러올 수 있습니다. 일반적으로 캐시된 데이터는 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히도 Laravel은 여러 캐시 백엔드를 위한 통합되고 표현력 있는 API를 제공하여, 고속 데이터 조회를 통해 웹 애플리케이션의 성능을 향상시킬 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치해 있습니다. 이 파일에서 애플리케이션 전반에 걸쳐 기본으로 사용할 캐시 저장소를 지정할 수 있습니다. Laravel은 기본으로 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등 인기 있는 캐시 백엔드를 지원합니다. 또한, 파일 기반 캐시 드라이버와 자동화된 테스트에 편리한 `array` 및 "null" 캐시 드라이버도 제공됩니다.

설정 파일에는 이 외에도 여러 옵션이 있으므로 검토해 보시기 바랍니다. 기본적으로 Laravel은 `database` 캐시 드라이버를 사용하도록 구성되어 있으며, 이 드라이버는 직렬화된 캐시 객체를 애플리케이션 데이터베이스에 저장합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항 (Driver Prerequisites)

<a name="prerequisites-database"></a>
#### 데이터베이스 (Database)

`database` 캐시 드라이버를 사용할 경우 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 보통 Laravel의 기본 마이그레이션 `0001_01_01_000001_create_cache_table.php`에 포함되어 있습니다. 만약 애플리케이션에 이 마이그레이션이 없다면 `make:cache-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. 여러 Memcached 서버를 `config/cache.php`에서 `memcached.servers` 배열에 나열할 수 있습니다. 설정 파일에 시작용 기본값이 포함되어 있습니다:

```
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

필요하면 `host` 옵션에 UNIX 소켓 경로를 지정할 수 있으며, 이 경우 `port`는 `0`으로 설정해야 합니다:

```
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

Laravel에서 Redis 캐시를 사용하기 전에 PECL을 통해 PhpRedis 확장 프로그램을 설치하거나 Composer로 `predis/predis` (~2.0) 패키지를 설치해야 합니다. [Laravel Sail](/docs/11.x/sail)은 이미 이 확장을 포함하고 있으며, [Laravel Forge](https://forge.laravel.com)와 [Laravel Vapor](https://vapor.laravel.com) 같은 공식 배포 플랫폼에도 기본적으로 PhpRedis 확장이 설치되어 있습니다.

Redis 설정에 관한 자세한 내용은 Laravel의 [Redis 문서 페이지](/docs/11.x/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에는 모든 캐시 데이터를 저장할 DynamoDB 테이블을 미리 생성해야 합니다. 보통 테이블 이름은 `cache`로 설정하지만, 설정 파일 `cache`의 `stores.dynamodb.table` 값에 따라 테이블 이름을 지정할 수 있습니다. 환경 변수 `DYNAMODB_CACHE_TABLE`로도 설정할 수 있습니다.

이 테이블에는 문자열 파티션 키가 필요하며, 키 이름은 설정 파일 `stores.dynamodb.attributes.key` 값과 일치해야 합니다. 기본값은 `key`입니다.

DynamoDB는 만료된 아이템을 자동 삭제하지 않으므로, 테이블에서 [Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활성화해야 합니다. TTL 속성 이름은 `expires_at`으로 설정하세요.

이후 AWS SDK를 설치해 Laravel 애플리케이션에서 DynamoDB와 통신할 수 있게 합니다:

```shell
composer require aws/aws-sdk-php
```

그리고 DynamoDB 캐시 저장소 관련 설정(`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` 등)을 `.env` 파일에 제공해야 합니다:

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

MongoDB를 사용하는 경우 공식 `mongodb/laravel-mongodb` 패키지가 제공하는 `mongodb` 캐시 드라이버를 데이터베이스 연결과 함께 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하므로 만료된 캐시 항목을 자동으로 제거하는 데 활용할 수 있습니다.

MongoDB 설정에 관한 자세한 내용은 MongoDB [Cache and Locks 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하세요.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기 (Obtaining a Cache Instance)

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드를 사용할 수 있습니다. 이 문서 전체에서 `Cache` 파사드를 사용하여 Laravel 캐시 컨트랙트의 핵심 구현체에 간편하게 접근합니다:

```
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

`Cache` 파사드의 `store` 메서드를 사용하면 여러 캐시 저장소에 접근할 수 있습니다. `store`에 전달하는 키는 `cache` 설정 파일의 `stores` 배열에 정의된 저장소 이름과 일치해야 합니다:

```
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기 (Retrieving Items From the Cache)

`Cache::get` 메서드는 캐시에서 값을 가져올 때 사용합니다. 캐시에 항목이 없으면 `null`을 반환합니다. 기본값을 지정하려면 두 번째 인수로 기본값을 전달할 수 있습니다:

```
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저를 전달할 수도 있는데, 이 경우 캐시에 항목이 없을 때 클로저 실행 결과가 반환됩니다. 클로저를 사용하면 데이터베이스 같은 외부 서비스에서 필요한 값을 지연 조회할 수 있습니다:

```
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인하기

`has` 메서드를 사용하여 캐시에 항목이 존재하는지 확인할 수 있습니다. 단, 항목 값이 `null`이면 존재하지 않는 것으로 간주해 `false`를 반환합니다:

```
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가와 감소

`increment`와 `decrement` 메서드는 캐시에 저장된 정수 값을 증가 또는 감소시킬 때 사용합니다. 두 메서드는 두 번째 인수로 조정할 값을 지정할 수 있습니다:

```
// 값이 없으면 초기화...
Cache::add('key', 0, now()->addHours(4));

// 값 증가/감소...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 가져오기 및 저장 (Retrieve and Store)

캐시에서 항목을 가져오되, 요청한 항목이 없을 때 기본값을 저장하려면 `Cache::remember` 메서드를 사용합니다. 예를 들어, 캐시에서 모든 사용자를 가져오거나 없으면 데이터베이스에서 조회해 캐시에 저장할 때 유용합니다:

```
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

캐시에 항목이 없으면 클로저가 실행되고 그 결과가 캐시에 저장됩니다.

영구 저장하고 싶다면 `rememberForever` 메서드를 사용하세요:

```
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate (유효기간 만료 이후 캐시 사용 패턴)

`Cache::remember` 사용 시, 만료된 캐시 값을 다시 계산하는 동안 일부 사용자가 느린 응답을 경험할 수 있습니다. 이런 경우 배경에서 캐시 값을 재계산하면서 '일부 구식 데이터'를 제공하는 "stale-while-revalidate" 패턴이 유용합니다. `Cache::flexible` 메서드는 이를 지원합니다.

`flexible` 메서드는 첫 번째 값이 캐시가 '신선함'으로 간주되는 초, 두 번째 값이 '구식'으로 간주되면서 재계산 전까지 허용되는 초를 배열로 받습니다.

첫 번째 구간에서는 즉시 캐시 값이 반환됩니다. 두 번째 구간에서는 이전 값을 사용자에게 제공하면서, [지연 함수](/docs/11.x/helpers#deferred-functions)를 등록해 응답 완료 후 캐시 값을 갱신합니다. 두 번째 구간이 지나면 캐시는 만료되어 즉시 다시 계산됩니다. 이때는 응답 속도가 느려질 수 있습니다:

```
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 가져오기 및 삭제 (Retrieve and Delete)

캐시에서 항목을 가져오고 즉시 삭제하려면 `pull` 메서드를 사용합니다. 항목이 없으면 `get`과 마찬가지로 `null`을 반환합니다:

```
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기 (Storing Items in the Cache)

`Cache::put` 메서드로 캐시에 항목을 저장할 수 있습니다:

```
Cache::put('key', 'value', $seconds = 10);
```

만약 저장 시간을 지정하지 않으면 무기한 저장됩니다:

```
Cache::put('key', 'value');
```

저장 시간을 초 단위 정수 대신 만료 시점을 나타내는 `DateTime` 인스턴스로 전달할 수도 있습니다:

```
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장하기

`add` 메서드는 캐시에 항목이 없을 때만 저장합니다. 저장에 성공하면 `true`, 이미 존재하면 `false`를 반환하는 원자적 연산입니다:

```
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 영구 저장하기

`forever` 메서드는 만료 없이 영구 저장합니다. 이런 항목은 수동으로 `forget` 메서드를 호출해 삭제해야 합니다:

```
Cache::forever('key', 'value');
```

> [!NOTE]  
> Memcached 드라이버를 사용하는 경우 "영구 저장"된 아이템도 캐시 용량 한계에 도달하면 제거될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기 (Removing Items From the Cache)

`forget` 메서드로 캐시 항목을 삭제할 수 있습니다:

```
Cache::forget('key');
```

또는 만료 시간을 0 또는 음수로 지정해도 삭제됩니다:

```
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

전체 캐시를 비우려면 `flush` 메서드를 사용합니다:

```
Cache::flush();
```

> [!WARNING]  
> `flush`는 캐시 키 접두사(prefix)를 무시하고 모든 캐시 데이터를 삭제합니다. 여러 애플리케이션이 캐시를 공유하는 경우 주의해서 사용하세요.

<a name="the-cache-helper"></a>
### 캐시 헬퍼 (The Cache Helper)

`Cache` 파사드 외에도, 전역 `cache` 함수를 이용해 캐시 데이터를 조회하거나 저장할 수 있습니다. 문자열 인자 하나를 전달하면 해당 키의 값을 반환합니다:

```
$value = cache('key');
```

키와 값의 배열, 만료 시간을 함께 전달하면 지정된 기간 동안 값을 저장합니다:

```
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

인자를 전달하지 않으면 `Illuminate\Contracts\Cache\Factory` 구현체 인스턴스가 반환되어, 다른 캐시 메서드를 호출할 수 있습니다:

```
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]  
> 전역 `cache` 함수 호출을 테스트할 때는 `Cache::shouldReceive`를 사용해 파사드를 모킹(mocking)하는 것과 동일하게 처리할 수 있습니다.

<a name="atomic-locks"></a>
## 원자적 락 (Atomic Locks)

> [!WARNING]  
> 이 기능을 사용하려면 애플리케이션 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나여야 하며, 모든 서버가 같은 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리하기 (Managing Locks)

원자적 락을 사용하면 경쟁 상태(race condition)를 걱정하지 않고 분산 락을 조작할 수 있습니다. 예를 들어, [Laravel Forge](https://forge.laravel.com)에서는 한 서버에서 한번에 하나의 원격 작업만 실행되도록 원자적 락을 사용합니다. `Cache::lock` 메서드를 이용해 락을 만들고 관리할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 락 획득됨...

    $lock->release();
}
```

`get` 메서드는 클로저도 받습니다. 클로저 실행이 끝나면 자동으로 락이 해제됩니다:

```
Cache::lock('foo', 10)->get(function () {
    // 10초 동안 락 획득 후 자동 해제됨...
});
```

락이 해당 시점에 사용 불가능하면 Laravel에게 기다리도록 요청할 수 있습니다. 이 경우 지정한 시간 내에 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다:

```
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최대 5초 대기 후 락 획득...
} catch (LockTimeoutException $e) {
    // 락 획득 불가...
} finally {
    $lock->release();
}
```

위 예시를 간소화하려면 `block` 메서드에 클로저를 전달하세요. 락을 얻을 때까지 최대 지정 시간 동안 시도하며, 클로저가 실행 완료되면 자동으로 락이 해제됩니다:

```
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 락 획득...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리 (Managing Locks Across Processes)

한 프로세스에서 락을 획득하고 다른 프로세스에서 해제해야 하는 경우도 있습니다. 예를 들어, 웹 요청 중 락을 얻고, 해당 요청이 트리거한 큐 작업이 락을 해제하게 할 때입니다. 이럴 때는 락 소유자 토큰(owner token)을 큐 작업에 전달해, 락을 재생성하고 해제할 수 있도록 해야 합니다.

아래 예시는 락을 성공적으로 획득한 후 큐 작업에 소유자 토큰을 전달하는 코드입니다:

```
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

`ProcessPodcast` 작업 클래스에서 전달받은 토큰으로 락을 복원하고 해제할 수 있습니다:

```
Cache::restoreLock('processing', $this->owner)->release();
```

현재 락 소유자를 무시하고 락을 해제하려면 `forceRelease` 메서드를 사용하세요:

```
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가하기 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성하기 (Writing the Driver)

커스텀 캐시 드라이버를 만들려면 먼저 `Illuminate\Contracts\Cache\Store` [컨트랙트](/docs/11.x/contracts)를 구현해야 합니다. 예를 들어 MongoDB 캐시 구현은 다음과 같을 수 있습니다:

```
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

이 메서드들을 MongoDB 연결을 사용해 구현하면 됩니다. 구현 예시는 Laravel 프레임워크 소스 코드 내 `Illuminate\Cache\MemcachedStore`를 참고하세요. 구현이 끝나면 `Cache` 파사드의 `extend` 메서드로 커스텀 드라이버 등록을 마칩니다:

```
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]  
> 커스텀 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 내 `Extensions` 네임스페이스를 만들어 관리하는 방법이 있습니다. Laravel은 엄격한 애플리케이션 구조를 강제하지 않으므로 원하는 방식으로 자유롭게 조직하세요.

<a name="registering-the-driver"></a>
### 드라이버 등록하기 (Registering the Driver)

Laravel에 커스텀 캐시 드라이버를 등록하려면 `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 `boot` 메서드에서 캐시된 값을 읽으려 할 수 있으므로, `register` 메서드 내에서 `booting` 콜백을 등록해 드라이버를 등록하는 것이 좋습니다. 이렇게 하면 모든 서비스 프로바이더의 `register`가 다 호출된 후, `boot`가 호출되기 전에 드라이버가 등록됩니다. 다음은 `App\Providers\AppServiceProvider` 클래스 내 예시입니다:

```
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

`extend` 메서드 첫 번째 인자는 드라이버 이름으로, `config/cache.php` 설정 파일의 `driver` 옵션과 동일해야 합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저이며, 클로저 인자로 서비스 컨테이너 `$app`이 전달됩니다.

등록 후 `.env`의 `CACHE_STORE`나 `config/cache.php`의 `default` 옵션을 커스텀 드라이버 이름으로 변경하세요.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 작업에서 코드를 실행하려면 다음과 같이 캐시가 발생시키는 [이벤트](/docs/11.x/events)에 리스너를 등록할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름 |
| --- |
| `Illuminate\Cache\Events\CacheHit` |
| `Illuminate\Cache\Events\CacheMissed` |
| `Illuminate\Cache\Events\KeyForgotten` |
| `Illuminate\Cache\Events\KeyWritten` |

</div>

성능 향상을 위해 애플리케이션 `config/cache.php`에서 각 캐시 저장소 설정에 `events` 옵션을 `false`로 설정해 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```