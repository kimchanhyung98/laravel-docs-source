# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 요구사항](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 헬퍼](#the-cache-helper)
- [캐시 태그 (Cache Tags)](#cache-tags)
    - [태그가 지정된 캐시 항목 저장하기](#storing-tagged-cache-items)
    - [태그가 지정된 캐시 항목 접근하기](#accessing-tagged-cache-items)
    - [태그가 지정된 캐시 항목 제거하기](#removing-tagged-cache-items)
- [원자적 락 (Atomic Locks)](#atomic-locks)
    - [드라이버 요구사항](#lock-driver-prerequisites)
    - [락 관리하기](#managing-locks)
    - [프로세스간 락 관리](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

애플리케이션에서 수행하는 일부 데이터 조회나 처리 작업은 CPU 집약적이거나 완료하는 데 몇 초가 걸릴 수 있습니다. 이럴 때, 조회된 데이터를 잠시 캐시에 저장하여 이후 같은 데이터 요청 시 빠르게 가져올 수 있도록 하는 것이 일반적입니다. 캐시된 데이터는 주로 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 보관됩니다.

Laravel은 다양한 캐시 백엔드를 위한 표현력 있는 통합 API를 제공하므로, 이를 활용하여 빠른 데이터 조회 속도를 얻어 웹 애플리케이션을 가속화할 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치해 있습니다. 이 파일에서 애플리케이션 전반에서 기본으로 사용할 캐시 드라이버를 지정할 수 있습니다. Laravel은 기본으로 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스와 같은 인기 있는 캐시 백엔드를 지원합니다. 이 밖에도 파일 기반 캐시 드라이버가 제공되며, `array`와 `null` 드라이버는 자동화된 테스트에 편리한 캐시 백엔드로 사용됩니다.

캐시 설정 파일에는 다양한 옵션도 포함되어 있으며, 이들은 설정 파일 내에서 문서화되어 있으니 꼭 살펴보시길 바랍니다. 기본 설정은 `file` 캐시 드라이버로, 캐시된 객체를 직렬화하여 서버의 파일 시스템에 저장합니다. 대규모 애플리케이션에서는 Memcached 또는 Redis 같은 더 견고한 드라이버 사용을 권장합니다. 동일한 드라이버에 대해 여러 캐시 구성을 할 수도 있습니다.

<a name="driver-prerequisites"></a>
### 드라이버 요구사항

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 경우, 캐시 항목을 저장할 테이블을 설정해야 합니다. 아래는 테이블을 위한 `Schema` 선언 예시입니다:

```
Schema::create('cache', function ($table) {
    $table->string('key')->unique();
    $table->text('value');
    $table->integer('expiration');
});
```

> [!TIP]
> `php artisan cache:table` Artisan 명령어를 사용하면 올바른 스키마가 포함된 마이그레이션을 자동 생성할 수 있습니다.

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. `config/cache.php` 설정 파일에서 모든 Memcached 서버를 나열할 수 있습니다. 기본 설정에 이미 `memcached.servers` 항목이 포함되어 있습니다:

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

필요하다면 `host` 옵션을 UNIX 소켓 경로로 설정할 수도 있습니다. 이때 `port` 옵션은 `0`으로 설정해야 합니다:

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

Laravel에서 Redis 캐시를 사용하려면 PECL을 통한 PhpRedis PHP 확장 또는 Composer를 통한 `predis/predis` 패키지(~1.0 버전)를 설치해야 합니다. [Laravel Sail](/docs/{{version}}/sail)은 이 확장을 기본 포함하고 있습니다. 또한 [Laravel Forge](https://forge.laravel.com)와 [Laravel Vapor](https://vapor.laravel.com) 같은 공식 배포 플랫폼에도 PhpRedis 확장이 기본 설치되어 있습니다.

Redis 구성에 관한 자세한 내용은 Laravel 공식 문서의 [Redis 설정 페이지](/docs/{{version}}/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하려면, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 테이블 이름은 `cache`로 합니다. 그러나 애플리케이션의 캐시 설정 파일 내 `stores.dynamodb.table` 구성 값에 따라 테이블 이름을 지정해야 합니다.

이 테이블에는 문자열 파티션 키가 있어야 하며, 이름은 `stores.dynamodb.attributes.key` 설정 값과 일치해야 합니다. 기본 값은 `key`입니다.

<a name="cache-usage"></a>
## 캐시 사용법

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면, 이 문서 전반에서 사용할 `Cache` 퍼사드를 이용할 수 있습니다. `Cache` 퍼사드는 Laravel 캐시 계약의 내부 구현에 간편하게 접근할 수 있도록 합니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 보여줍니다.
     *
     * @return Response
     */
    public function index()
    {
        $value = Cache::get('key');

        //
    }
}
```

<a name="accessing-multiple-cache-stores"></a>
#### 여러 캐시 저장소 접근하기

`Cache` 퍼사드의 `store` 메서드를 사용하면 다양한 캐시 저장소에 접근할 수 있습니다. `store`에 전달하는 키는 `cache` 설정 파일 내 `stores` 배열에 정의된 저장소 이름과 일치해야 합니다:

```
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기

`Cache` 퍼사드의 `get` 메서드는 캐시에서 항목을 가져오는 데 사용됩니다. 해당 항목이 캐시에 없으면 `null`이 반환됩니다. 필요시 두 번째 인수로 기본값을 지정할 수도 있는데, 캐시에 값이 없을 경우 이 기본값이 반환됩니다:

```
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저를 전달할 수도 있습니다. 지정한 키가 캐시에 없으면 클로저가 실행되어 반환한 값을 대신 받습니다. 이렇게 하면 기본값을 데이터베이스나 외부 서비스에서 지연 조회할 수 있습니다:

```
$value = Cache::get('key', function () {
    return DB::table(...)->get();
});
```

<a name="checking-for-item-existence"></a>
#### 항목 존재 여부 확인

`has` 메서드는 캐시에 특정 항목이 존재하는지 확인하는 데 사용됩니다. 항목이 존재하지만 값이 `null`인 경우에도 `false`를 반환합니다:

```
if (Cache::has('key')) {
    //
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증감하기

`increment`와 `decrement` 메서드를 이용해 캐시에 저장된 정수 값 항목을 증가시키거나 감소시킬 수 있습니다. 두 메서드 모두 두 번째 인수로 증감할 수량을 지정할 수 있습니다:

```
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 값 조회 및 저장

가끔 캐시에서 값을 조회하되, 해당 키가 없으면 기본값을 데이터베이스에서 조회하여 캐시에 저장하고 싶을 수 있습니다. 예를 들어 모든 사용자를 캐시에서 가져오거나, 없으면 DB에서 조회 후 캐시에 저장할 때 `Cache::remember`를 사용합니다:

```
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

키가 없으면 `remember`에 넘긴 클로저가 실행되고, 반환값이 캐시에 저장됩니다.

`rememberForever` 메서드는 캐시에 값이 없을 때 영구 저장할 때 사용됩니다:

```
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제

캐시에서 항목을 조회하고 즉시 삭제하려면 `pull` 메서드를 이용합니다. 키가 없으면 `null`을 반환합니다:

```
$value = Cache::pull('key');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

`Cache` 퍼사드의 `put` 메서드를 사용하면 항목을 캐시에 저장할 수 있습니다:

```
Cache::put('key', 'value', $seconds = 10);
```

두 번째 인자인 저장 기간을 지정하지 않으면 항목은 무기한 저장됩니다:

```
Cache::put('key', 'value');
```

`put` 메서드에 저장 기간 대신 `DateTime` 인스턴스를 전달하여 만료 시간을 지정할 수도 있습니다:

```
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때에만 저장하기

`add` 메서드는 캐시에 해당 키가 없을 때만 항목을 추가합니다. 실제로 추가했다면 `true`, 이미 존재하면 `false`를 반환합니다. 이 작업은 원자적(atomic)입니다:

```
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 영구 저장하기

`forever` 메서드를 사용하면 만료되지 않는 항목을 저장할 수 있습니다. 이 항목은 직접 `forget` 메서드를 호출하여 삭제해야 합니다:

```
Cache::forever('key', 'value');
```

> [!TIP]
> Memcached 드라이버를 사용할 때, 영구 저장된 항목도 캐시 용량 한도에 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드로 캐시 항목을 삭제할 수 있습니다:

```
Cache::forget('key');
```

또한 만료 시간을 0 또는 음수로 지정하여 항목을 제거할 수도 있습니다:

```
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메서드를 호출하면 캐시 전체를 비울 수 있습니다:

```
Cache::flush();
```

> [!NOTE]
> `flush`는 설정된 캐시 접두사를 무시하고 캐시의 모든 항목을 삭제합니다. 다른 애플리케이션과 공유하는 캐시를 비울 때는 주의해야 합니다.

<a name="the-cache-helper"></a>
### 캐시 헬퍼

`Cache` 퍼사드 외에도 전역 `cache` 함수를 사용해 캐시에서 데이터 조회와 저장을 할 수 있습니다. 함수에 키값을 한 개만 전달하면 해당 키의 값을 반환합니다:

```
$value = cache('key');
```

배열 형태의 키/값 쌍과 만료 시간을 전달하면 지정한 시간 동안 캐시에 값을 저장합니다:

```
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

아무 인자 없이 호출하면 `Illuminate\Contracts\Cache\Factory` 구현체를 반환하여 다른 캐싱 메서드를 호출할 수 있습니다:

```
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!TIP]
> 전역 `cache` 함수를 테스트할 때도, `Cache::shouldReceive` 메서드를 사용하여 퍼사드 테스트 시와 같이 모킹할 수 있습니다. [퍼사드 테스트 문서](/docs/{{version}}/mocking#mocking-facades)를 참고하세요.

<a name="cache-tags"></a>
## 캐시 태그 (Cache Tags)

> [!NOTE]
> `file`, `dynamodb`, `database` 캐시 드라이버에서는 캐시 태그를 지원하지 않습니다. 또한 영구 저장된 캐시에서 여러 태그를 사용할 때는 `memcached`처럼 오래된 레코드를 자동으로 제거하는 드라이버가 성능상 유리합니다.

<a name="storing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 저장하기

캐시 태그는 관련된 캐시 항목에 태그를 지정하고, 이후 특정 태그가 붙은 캐시를 한꺼번에 삭제할 수 있도록 합니다. 태그 이름의 순서가 지정된 배열을 `tags` 메서드에 전달하여 태그가 지정된 캐시에 접근할 수 있습니다. 예를 들어, 태그가 지정된 캐시에 값을 저장하는 방법은 아래와 같습니다:

```
Cache::tags(['people', 'artists'])->put('John', $john, $seconds);

Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 접근하기

태그가 지정된 캐시 항목을 가져오려면, 동일한 순서의 태그 목록을 `tags` 메서드에 전달하고, `get` 메서드에 원하는 키를 넘깁니다:

```
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 제거하기

특정 태그 또는 태그 목록이 지정된 모든 항목을 삭제할 수 있습니다. 예를 들어, 아래 문장은 `people` 또는 `authors` 태그가 붙은 모든 캐시를 삭제하므로 `Anne`과 `John` 모두 제거됩니다:

```
Cache::tags(['people', 'authors'])->flush();
```

반면 아래 문장은 `authors` 태그가 붙은 항목만 삭제하므로 `Anne`만 제거되고 `John`은 유지됩니다:

```
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 원자적 락 (Atomic Locks)

> [!NOTE]
> 이 기능을 사용하려면, 애플리케이션이 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file` 또는 `array` 중 하나를 사용해야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="lock-driver-prerequisites"></a>
### 드라이버 요구사항

<a name="atomic-locks-prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 때는 애플리케이션의 캐시 락을 담을 테이블을 설정해야 합니다. 예시는 다음과 같습니다:

```
Schema::create('cache_locks', function ($table) {
    $table->string('key')->primary();
    $table->string('owner');
    $table->integer('expiration');
});
```

<a name="managing-locks"></a>
### 락 관리하기

원자적 락을 활용하면 경쟁 상태(race condition)를 걱정하지 않고 분산 락을 조작할 수 있습니다. 예를 들어, [Laravel Forge](https://forge.laravel.com)는 원자적 락을 사용해 한 서버에서 단 하나의 원격 작업만 실행되도록 보장합니다. `Cache::lock` 메서드를 이용해 락을 생성하고 관리할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초 동안 락을 획득...

    $lock->release();
}
```

`get` 메서드는 클로저도 받습니다. 클로저 실행이 끝나면 Laravel이 자동으로 락을 해제합니다:

```
Cache::lock('foo')->get(function () {
    // 락을 무기한 획득하고 실행 완료 후 자동 해제...
});
```

락을 요청할 때 즉시 획득하지 못하면, 지정한 시간만큼 대기할 수 있습니다. 락 획득에 실패하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다:

```
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // 최대 5초 대기 후 락 획득...
} catch (LockTimeoutException $e) {
    // 락 획득 실패...
} finally {
    optional($lock)->release();
}
```

위 예제는 `block` 메서드에 클로저를 전달하여 더 간단히 쓸 수도 있습니다. 이 경우 지정한 시간 동안 락 획득을 시도하고, 락 획득 후 클로저 실행이 끝나면 락이 자동 해제됩니다:

```
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 락 획득...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

특정 프로세스에서 락을 획득하고, 다른 프로세스에서 락 해제를 해야 할 수도 있습니다. 예를 들어, 웹 요청 시 락을 획득하고, 해당 요청에 의해 대기열 큐 작업이 실행될 때 락을 해제하는 경우입니다. 이럴 때는 락의 범위(owner) 토큰을 띄운 큐 작업에 전달해서, 해당 토큰을 이용해 큐 작업에서 락을 재생성하고 해제할 수 있습니다.

아래 예시는 락 획득에 성공하면 락의 소유자 토큰을 큐 작업에 전달하는 방법입니다:

```
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

애플리케이션의 `ProcessPodcast` 작업 내에서는 전달받은 소유자 토큰으로 락을 복원해 해제할 수 있습니다:

```
Cache::restoreLock('processing', $this->owner)->release();
```

현재 소유자를 무시하고 락을 강제로 해제하려면 `forceRelease` 메서드를 사용합니다:

```
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가하기

<a name="writing-the-driver"></a>
### 드라이버 작성하기

커스텀 캐시 드라이버를 만들려면 먼저 `Illuminate\Contracts\Cache\Store` [계약](/docs/{{version}}/contracts)을 구현해야 합니다. 예를 들어 MongoDB 캐시 구현은 다음과 같이 보일 수 있습니다:

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

MongoDB 연결을 활용해 각 메서드를 구현하면 됩니다. 참고용으로, Laravel 공식 소스코드 내 `Illuminate\Cache\MemcachedStore` 구현을 살펴볼 수 있습니다. 구현이 완료되면 `Cache` 퍼사드의 `extend` 메서드를 사용해 커스텀 드라이버를 등록합니다:

```
Cache::extend('mongo', function ($app) {
    return Cache::repository(new MongoStore);
});
```

> [!TIP]
> 커스텀 캐시 드라이버 코드는 `app` 디렉터리 내에 `Extensions` 네임스페이스를 생성해 두는 것이 한 방법입니다. 다만, Laravel은 엄격한 애플리케이션 구조를 요구하지 않으므로, 귀하의 취향대로 디렉터리 구조를 구성할 수 있습니다.

<a name="registering-the-driver"></a>
### 드라이버 등록하기

Laravel에 커스텀 캐시 드라이버를 등록하려면 `Cache` 퍼사드의 `extend` 메서드를 활용합니다. 다른 서비스 프로바이더가 `boot` 메서드 내에서 캐시 값을 읽을 수 있으므로, 커스텀 드라이버 등록은 `booting` 콜백 내에서 처리하는 편이 좋습니다. `booting` 콜백은 모든 서비스 프로바이더의 `register` 메서드가 호출된 이후, `boot` 메서드가 호출되기 직전에 실행됩니다. 일반적으로 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에 등록합니다:

```
<?php

namespace App\Providers;

use App\Extensions\MongoStore;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\ServiceProvider;

class CacheServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록.
     *
     * @return void
     */
    public function register()
    {
        $this->app->booting(function () {
             Cache::extend('mongo', function ($app) {
                 return Cache::repository(new MongoStore);
             });
         });
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
     *
     * @return void
     */
    public function boot()
    {
        //
    }
}
```

`extend` 메서드의 첫 번째 인자가 드라이버 이름이고, `config/cache.php` 내 `driver` 설정 옵션과 일치해야 합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저이며, `$app` 인자로 서비스 컨테이너 인스턴스가 전달됩니다.

커스텀 드라이버를 등록한 후에는 `config/cache.php` 파일 내 `driver` 옵션을 새 확장 이름으로 변경하세요.

<a name="events"></a>
## 이벤트

캐시 작업이 실행될 때마다 코드를 수행하려면 캐시에서 발생하는 [이벤트](/docs/{{version}}/events)를 리스닝할 수 있습니다. 보통 애플리케이션의 `App\Providers\EventServiceProvider` 클래스 내에 이벤트 리스너를 배치합니다:

```
/**
 * 애플리케이션 이벤트 리스너 매핑.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Cache\Events\CacheHit' => [
        'App\Listeners\LogCacheHit',
    ],

    'Illuminate\Cache\Events\CacheMissed' => [
        'App\Listeners\LogCacheMissed',
    ],

    'Illuminate\Cache\Events\KeyForgotten' => [
        'App\Listeners\LogKeyForgotten',
    ],

    'Illuminate\Cache\Events\KeyWritten' => [
        'App\Listeners\LogKeyWritten',
    ],
];
```