# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 필수 조건](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 삭제하기](#removing-items-from-the-cache)
    - [캐시 헬퍼 함수](#the-cache-helper)
- [원자적 잠금 (Atomic Locks)](#atomic-locks)
    - [드라이버 필수 조건](#lock-driver-prerequisites)
    - [잠금 관리하기](#managing-locks)
    - [프로세스 간 잠금 관리하기](#managing-locks-across-processes)
- [사용자 정의 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 구현하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션이 수행하는 데이터 조회나 처리 작업 중 일부는 CPU 부하가 크거나 완료하는 데 몇 초가 걸릴 수 있습니다. 이런 경우, 같은 데이터를 다음 요청 시 빠르게 조회하기 위해 일정 기간 동안 데이터를 캐시에 저장하는 것이 일반적입니다. 보통 캐시된 데이터는 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같이 매우 빠른 데이터 저장소에 저장됩니다.

다행히도 Laravel은 다양한 캐시 백엔드에 대해 표현력 있고 통합된 API를 제공하여, 이들의 빠른 데이터 조회 특성을 활용해 웹 애플리케이션의 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 구성 파일은 `config/cache.php`에 위치합니다. 이 파일 안에서 애플리케이션 전반에 기본으로 사용할 캐시 드라이버를 지정할 수 있습니다. Laravel은 기본적으로 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등 대중적인 캐시 백엔드를 지원합니다. 추가로 파일 기반 캐시 드라이버가 제공되며, 자동화된 테스트 환경을 위해 `array` 및 "null" 캐시 드라이버도 사용 가능합니다.

해당 설정 파일 안에는 다양한 옵션이 포함되어 있으니 꼭 읽어보시길 권장합니다. 기본적으로 Laravel은 `file` 캐시 드라이버를 사용하도록 설정되어 있으며, 이는 직렬화된 캐시 객체를 서버 파일시스템에 저장합니다. 규모가 큰 애플리케이션에서는 Memcached나 Redis와 같은 더 견고한 드라이버 사용을 권장합니다. 동일한 드라이버에 대해 여러 캐시 설정을 구성하는 것도 가능합니다.

<a name="driver-prerequisites"></a>
### 드라이버 필수 조건 (Driver Prerequisites)

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 경우, 캐시 항목을 담을 테이블을 생성해야 합니다. 아래는 해당 테이블의 `Schema` 선언 예시입니다:

```
Schema::create('cache', function (Blueprint $table) {
    $table->string('key')->unique();
    $table->text('value');
    $table->integer('expiration');
});
```

> [!NOTE]  
> `php artisan cache:table` Artisan 명령어를 사용하면 적절한 스키마의 마이그레이션 파일이 자동으로 생성됩니다.

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. `config/cache.php` 파일 내에 Memcached 서버 목록을 설정할 수 있으며, 이미 `memcached.servers` 항목이 포함되어 있습니다:

```
'memcached' => [
    'servers' => [
        [
            'host' => env('MEMCACHED_HOST', '127.0.0.1'),
            'port' => env('MEMCACHED_PORT', 11211),
            'weight' => 100,
        ],
    ],
],
```

필요에 따라 `host` 옵션에 UNIX 소켓 경로를 지정할 수 있으며, 이 경우 `port` 옵션은 `0`으로 설정해야 합니다:

```
'memcached' => [
    [
        'host' => '/var/run/memcached/memcached.sock',
        'port' => 0,
        'weight' => 100
    ],
],
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 캐시를 사용하려면 PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나, Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. [Laravel Sail](/docs/10.x/sail)에는 이미 이 확장 모듈이 포함되어 있습니다. 또한, [Laravel Forge](https://forge.laravel.com)와 [Laravel Vapor](https://vapor.laravel.com) 같은 공식 배포 플랫폼에서는 PhpRedis 확장이 기본적으로 설치되어 있습니다.

Redis 설정에 관한 자세한 내용은 해당 [Laravel 문서 페이지](/docs/10.x/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하려면, 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 보통 이 테이블 이름은 `cache`로 지정하지만, 실제 테이블 이름은 애플리케이션의 `cache` 설정 파일 내 `stores.dynamodb.table` 설정값에 따라 달라질 수 있습니다.

이 테이블에는 `stores.dynamodb.attributes.key` 설정값에 해당하는 이름의 문자열 파티션 키가 필요하며, 기본값은 `key`입니다.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기 (Obtaining a Cache Instance)

캐시 저장소 인스턴스를 얻으려면, 이 문서 전반에서 사용할 `Cache` 파사드를 사용하세요. `Cache` 파사드는 Laravel 캐시 계약의 기본 구현체에 간결하게 접근할 수 있도록 도와줍니다:

```
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

`Cache` 파사드의 `store` 메서드를 사용하면 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일의 `stores` 배열에 정의된 저장소 이름이어야 합니다:

```
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기 (Retrieving Items From the Cache)

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 가져올 때 사용합니다. 만약 항목이 캐시에 없으면 `null`을 반환합니다. 두 번째 인수로 기본값을 지정할 수 있는데, 캐시에 항목이 없을 때 이 기본값이 반환됩니다:

```
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저를 전달할 수도 있습니다. 지정한 키가 캐시에 없으면 클로저 결과가 반환됩니다. 클로저를 사용하면 데이터베이스나 외부 서비스에서 기본 값을 지연 조회할 수 있습니다:

```
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인

`has` 메서드는 캐시에서 항목이 존재하는지 확인할 때 사용합니다. 단, 항목이 존재하지만 값이 `null`인 경우에는 `false`를 반환합니다:

```
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가 / 감소

`increment` 및 `decrement` 메서드로 캐시에 저장된 정수형 값을 증감할 수 있습니다. 두 메서드 모두 두 번째 인수로 증감할 양을 받을 수 있으며 기본값은 1입니다:

```
// 값이 없으면 초기화...
Cache::add('key', 0, now()->addHours(4));

// 값 증가 또는 감소
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 가져오고 저장하기

가끔 캐시에서 항목을 가져오되, 항목이 없는 경우 기본값을 저장하고 싶을 때가 있습니다. 예를 들어, 유저 목록을 캐시에서 가져오고 없으면 데이터베이스에서 조회한 뒤 캐시에 추가하는 경우입니다. `Cache::remember` 메서드를 사용하면 됩니다:

```
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

캐시에 없으면 클로저가 실행되어 반환값이 캐시에 저장됩니다.

항목을 영구 저장하려면 `rememberForever` 메서드를 사용할 수 있습니다:

```
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 가져오고 삭제하기

캐시에서 항목을 바로 가져온 다음 삭제해야 한다면 `pull` 메서드를 사용하세요. 항목이 없으면 `null`을 반환합니다:

```
$value = Cache::pull('key');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기 (Storing Items in the Cache)

`Cache` 파사드의 `put` 메서드를 이용해 캐시에 항목을 저장할 수 있습니다:

```
Cache::put('key', 'value', $seconds = 10);
```

만약 저장 시간을 생략하면 항목은 무기한 저장됩니다:

```
Cache::put('key', 'value');
```

초 단위가 아닌, 만료 시간의 `DateTime` 인스턴스를 전달하는 것도 가능합니다:

```
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 없을 때만 저장하기

`add` 메서드는 해당 키가 캐시에 없을 때만 항목을 추가합니다. 항목이 실제로 저장되면 `true`, 이미 존재하면 `false`를 반환합니다. 이 연산은 원자적입니다:

```
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 영구 저장하기

`forever` 메서드로 캐시에 항목을 영구 저장할 수 있습니다. 이 항목은 만료되지 않으므로 수동으로 `forget` 메서드로 삭제해야 합니다:

```
Cache::forever('key', 'value');
```

> [!NOTE]  
> Memcached 드라이버를 사용할 때는 "영구 저장"된 항목도 캐시 크기 한도에 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 삭제하기 (Removing Items From the Cache)

`forget` 메서드로 캐시에서 항목을 삭제할 수 있습니다:

```
Cache::forget('key');
```

만료 시간을 0 또는 음수로 전달해도 항목이 삭제됩니다:

```
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

전체 캐시를 비우려면 `flush` 메서드를 사용하세요:

```
Cache::flush();
```

> [!WARNING]  
> `flush` 메서드는 설정된 캐시 "접두사(prefix)"를 무시하고 캐시의 모든 항목을 삭제합니다. 다른 애플리케이션과 캐시를 공유하는 경우 주의해서 사용해야 합니다.

<a name="the-cache-helper"></a>
### 캐시 헬퍼 함수 (The Cache Helper)

`Cache` 파사드 외에도 전역 `cache` 함수를 사용해 캐시에서 데이터를 조회하거나 저장할 수 있습니다. 인수로 단일 문자열 키를 전달하면 해당 키의 값을 반환합니다:

```
$value = cache('key');
```

키-값 쌍 배열과 만료 시간을 전달하면 값들을 지정한 기간 동안 캐시에 저장합니다:

```
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

인수 없이 호출하면, `Illuminate\Contracts\Cache\Factory` 구현체 인스턴스를 반환해 다른 캐시 관련 메서드를 호출할 수 있습니다:

```
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]  
> 전역 `cache` 함수를 테스트할 때는 [파사드 테스트와 같이](/docs/10.x/mocking#mocking-facades) `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="atomic-locks"></a>
## 원자적 잠금 (Atomic Locks)

> [!WARNING]  
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나여야 하며, 모든 서버가 같은 중앙 캐시 서버와 통신 중이어야 합니다.

<a name="lock-driver-prerequisites"></a>
### 드라이버 필수 조건 (Driver Prerequisites)

<a name="atomic-locks-prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버 사용 시, 캐시 잠금을 저장할 테이블을 만들어야 합니다. 아래는 예시 `Schema` 선언입니다:

```
Schema::create('cache_locks', function (Blueprint $table) {
    $table->string('key')->primary();
    $table->string('owner');
    $table->integer('expiration');
});
```

> [!NOTE]  
> `cache:table` Artisan 명령어로 데이터베이스 캐시 테이블을 생성했다면, 이 명령어로 생성된 마이그레이션에 이미 `cache_locks` 테이블 정의가 포함되어 있습니다.

<a name="managing-locks"></a>
### 잠금 관리하기 (Managing Locks)

원자적 잠금은 경쟁 상태(race condition)를 걱정하지 않고 분산 잠금을 다룰 수 있게 해줍니다. 예를 들어, [Laravel Forge](https://forge.laravel.com)는 한 서버에서 한 번에 한 작업만 실행되도록 원자적 잠금을 활용합니다. 잠금은 `Cache::lock` 메서드를 사용해 생성 및 관리할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 잠금 획득...

    $lock->release();
}
```

`get` 메서드는 클로저를 인수로 받을 수도 있습니다. 클로저 실행이 끝나면 Laravel이 자동으로 잠금을 해제합니다:

```
Cache::lock('foo', 10)->get(function () {
    // 10초 동안 잠금 획득 후 자동 해제...
});
```

잠금이 즉시 사용 가능하지 않으면, 지정한 시간 동안 대기하도록 할 수 있습니다. 지정된 시간 내에 잠금을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 던져집니다:

```
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최대 5초 대기 후 잠금 획득...
} catch (LockTimeoutException $e) {
    // 잠금 획득 실패...
} finally {
    $lock?->release();
}
```

위 예시는 `block` 메서드에 클로저를 전달해 간단히 쓸 수도 있습니다. 이 경우 Laravel이 지정 시간 동안 잠금 획득을 시도하고, 클로저 실행 후 자동으로 잠금을 해제합니다:

```
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 잠금 획득...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 잠금 관리하기 (Managing Locks Across Processes)

어떤 경우에는 한 프로세스에서 잠금을 획득하고, 다른 프로세스에서 잠금을 해제하고 싶을 때가 있습니다. 예를 들어, 웹 요청 처리 중 잠금을 얻고, 이 요청에 의해 트리거된 큐 작업의 끝에서 잠금을 해제해야 한다면, 잠금의 고유 "소유자 토큰"을 큐 작업에 전달해야 합니다. 이 토큰을 사용해 잠금을 다시 인스턴스화할 수 있습니다.

아래 예시는 잠금 획득에 성공하면 큐 작업을 dispatch하고, 잠금 소유자 토큰을 함께 전달하는 모습입니다:

```
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

애플리케이션의 `ProcessPodcast` 작업 내에서는 소유자 토큰으로 잠금을 복원하고 해제할 수 있습니다:

```
Cache::restoreLock('processing', $this->owner)->release();
```

잠금 소유자와 관계없이 강제 해제하려면 `forceRelease` 메서드를 사용합니다:

```
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 사용자 정의 캐시 드라이버 추가하기 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 구현하기 (Writing the Driver)

사용자 정의 캐시 드라이버를 생성하려면 먼저 `Illuminate\Contracts\Cache\Store` [계약](/docs/10.x/contracts)을 구현해야 합니다. 예를 들어, MongoDB 캐시 구현은 다음과 비슷할 수 있습니다:

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

MongoDB 연결을 사용해 각 메서드를 구현하면 됩니다. 메서드 구현 예시는 [Laravel 프레임워크 소스코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore` 클래스를 참고하세요. 구현을 마친 후에는 `Cache` 파사드의 `extend` 메서드를 호출해 사용자 정의 드라이버 등록을 완료합니다:

```
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]  
> 사용자 정의 캐시 드라이버 코드는 `app` 디렉터리 내에 `Extensions` 네임스페이스를 만들어 저장할 수도 있습니다. 다만, Laravel은 엄격한 애플리케이션 구조를 강제하지 않으므로 본인의 선호에 따라 자유롭게 구조를 설계하세요.

<a name="registering-the-driver"></a>
### 드라이버 등록하기 (Registering the Driver)

사용자 정의 캐시 드라이버를 Laravel에 등록하려면 `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 `boot` 메서드에서 캐시 값을 읽으려 할 수 있으므로, 사용자 정의 드라이버 등록은 `boot` 호출 직전이자 `register` 메서드 호출 후에 실행되도록 `booting` 콜백 안에서 등록하는 게 좋습니다. 아래는 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에서 `booting` 콜백을 등록하는 예시입니다:

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

`extend` 메서드의 첫 번째 인수는 드라이버 이름이며, 이는 `config/cache.php` 내 `driver` 옵션 이름과 일치해야 합니다. 두 번째 인수는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저이고, 이 클로저는 서비스 컨테이너 `$app` 인스턴스를 인수로 받습니다.

확장 드라이버가 등록되면, `config/cache.php` 파일 내의 `driver` 옵션 값을 확장한 드라이버 이름으로 바꾸세요.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 작업 시 특정 코드를 실행하고 싶다면, 캐시 관련 [이벤트](/docs/10.x/events)를 리스닝하세요. 보통 이러한 이벤트 리스너는 애플리케이션의 `App\Providers\EventServiceProvider` 클래스 안에 배치합니다:

```
use App\Listeners\LogCacheHit;
use App\Listeners\LogCacheMissed;
use App\Listeners\LogKeyForgotten;
use App\Listeners\LogKeyWritten;
use Illuminate\Cache\Events\CacheHit;
use Illuminate\Cache\Events\CacheMissed;
use Illuminate\Cache\Events\KeyForgotten;
use Illuminate\Cache\Events\KeyWritten;

/**
 * 애플리케이션 이벤트-리스너 매핑
 *
 * @var array
 */
protected $listen = [
    CacheHit::class => [
        LogCacheHit::class,
    ],

    CacheMissed::class => [
        LogCacheMissed::class,
    ],

    KeyForgotten::class => [
        LogKeyForgotten::class,
    ],

    KeyWritten::class => [
        LogKeyWritten::class,
    ],
];
```