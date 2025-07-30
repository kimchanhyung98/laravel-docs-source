# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 필수 조건](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 헬퍼 함수](#the-cache-helper)
- [캐시 태그](#cache-tags)
    - [태그된 캐시 항목 저장하기](#storing-tagged-cache-items)
    - [태그된 캐시 항목 접근하기](#accessing-tagged-cache-items)
    - [태그된 캐시 항목 제거하기](#removing-tagged-cache-items)
- [원자적 락 (Atomic Locks)](#atomic-locks)
    - [드라이버 필수 조건](#lock-driver-prerequisites)
    - [락 관리하기](#managing-locks)
    - [프로세스 간 락 관리하기](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

애플리케이션에서 수행하는 일부 데이터 조회나 처리 작업은 CPU를 많이 쓰거나 완료하는 데 몇 초가 걸릴 수 있습니다. 이런 경우, 조회된 데이터를 일정 시간 캐시에 저장해두고 이후 같은 데이터 요청이 있을 때 빠르게 반환하는 것이 일반적입니다. 캐시된 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io) 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히도, Laravel은 여러 캐시 백엔드에 대해 간결하고 통일된 API를 제공하여, 빠른 데이터 조회를 쉽고 효과적으로 활용해 웹 애플리케이션의 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서 애플리케이션 전반에 기본으로 사용할 캐시 드라이버를 지정할 수 있습니다. Laravel은 기본으로 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스 같은 여러 인기 캐시 백엔드를 지원합니다. 추가로, 파일 기반 캐시 드라이버도 사용할 수 있으며, `array` 및 "null" 캐시 드라이버는 자동화된 테스트용 간편한 캐시 백엔드를 제공합니다.

캐시 설정 파일에는 이외에도 여러 옵션들이 포함되어 있으니 꼭 확인해 보시기 바랍니다. 기본 설정은 `file` 캐시 드라이버로, 서버 파일 시스템에 직렬화된 캐시 객체를 저장합니다. 대형 애플리케이션의 경우, Memcached나 Redis 같은 더 강력한 드라이버 사용을 권장합니다. 또한 동일한 드라이버에 대해 여러 캐시 구성을 설정할 수도 있습니다.

<a name="driver-prerequisites"></a>
### 드라이버 필수 조건

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 경우, 캐시 항목을 저장할 테이블을 생성해야 합니다. 아래는 테이블의 `Schema` 예시 선언입니다:

```
Schema::create('cache', function ($table) {
    $table->string('key')->unique();
    $table->text('value');
    $table->integer('expiration');
});
```

> [!NOTE]
> `php artisan cache:table` Artisan 명령어를 사용하면 적절한 스키마를 가진 마이그레이션을 생성할 수 있습니다.

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. 모든 Memcached 서버를 `config/cache.php` 설정 파일에서 리스트할 수 있습니다. 아래 예시는 기본적으로 포함된 `memcached.servers` 항목입니다:

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

필요하다면 `host` 옵션에 UNIX 소켓 경로를 지정할 수 있습니다. 이 경우 `port` 옵션은 `0`으로 설정해야 합니다:

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

Laravel에서 Redis 캐시를 사용하려면 PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나, Composer로 `predis/predis` 패키지(~1.0)를 설치해야 합니다. [Laravel Sail](/docs/9.x/sail)에는 이 확장이 이미 포함되어 있습니다. 또한, 공식 Laravel 배포 플랫폼인 [Laravel Forge](https://forge.laravel.com)나 [Laravel Vapor](https://vapor.laravel.com)에는 PhpRedis 확장이 기본으로 설치되어 있습니다.

Redis 설정 방법에 대해서는 Laravel의 [Redis 문서 페이지](/docs/9.x/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하려면 우선 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 이 테이블 이름은 보통 `cache`로 지정하지만, 애플리케이션의 `cache` 설정 파일에 있는 `stores.dynamodb.table` 설정 값에 따라 결정해야 합니다.

이 테이블에는 `stores.dynamodb.attributes.key` 설정 항목에 대응되는 이름을 가진 문자열 파티션 키가 필요합니다. 기본값은 `key`라는 이름의 파티션 키입니다.

<a name="cache-usage"></a>
## 캐시 사용법

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드를 사용할 수 있습니다. 이 문서 전반에서 `Cache` 파사드를 기준으로 설명합니다. `Cache` 파사드는 Laravel 캐시 계약의 구현체를 간편하고 간결하게 사용할 수 있게 해줍니다:

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

`Cache` 파사드의 `store` 메서드를 사용하면 다양한 캐시 저장소에 접근할 수 있습니다. `store`에 전달하는 키는 `cache` 설정 파일의 `stores` 배열에 정의된 저장소 이름과 일치해야 합니다:

```
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10분
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기

`Cache` 파사드의 `get` 메서드를 사용하면 캐시에서 항목을 가져올 수 있습니다. 만약 해당 항목이 캐시에 없으면 `null`을 반환합니다. 원하는 경우 `get` 메서드의 두 번째 인수로 기본값을 지정할 수 있습니다. 항목이 없으면 이 기본값을 반환합니다:

```
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

클로저를 기본값으로 넘길 수도 있습니다. 클로저 결과가 캐시에 해당 키가 없을 때 반환됩니다. 클로저를 사용하면 데이터베이스 등 외부 서비스에서 기본값을 지연해서 조회할 수 있습니다:

```
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="checking-for-item-existence"></a>
#### 항목 존재 여부 확인하기

`has` 메서드는 캐시에 항목이 존재하는지 확인하는 데 사용합니다. 단, 항목이 존재하지만 값이 `null`인 경우에도 `false`를 반환합니다:

```
if (Cache::has('key')) {
    //
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가 / 감소

`increment`와 `decrement` 메서드를 사용해 캐시에 저장된 정수 값을 증가 또는 감소시킬 수 있습니다. 두 메서드는 선택적으로 두 번째 인수로 증감할 값을 받을 수 있습니다:

```
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
#### 조회 후 저장 (Retrieve & Store)

캐시에서 항목을 조회하되, 없으면 기본값을 저장하고 싶을 때가 있습니다. 예를 들어, 모든 사용자를 캐시에서 가져오거나 없으면 데이터베이스에서 조회해 캐시에 저장하고 싶을 수 있습니다. 이때 `Cache::remember` 메서드를 사용합니다:

```
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

캐시에 없으면 클로저가 실행되고 결과가 캐시에 저장됩니다.

`rememberForever` 메서드는 캐시에 영구 저장하거나 없으면 저장하는 기능을 제공합니다:

```
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제 (Retrieve & Delete)

캐시 항목을 조회하고 즉시 삭제하려면 `pull` 메서드를 사용합니다. `get`처럼 캐시에 항목이 없으면 `null`을 반환합니다:

```
$value = Cache::pull('key');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

`Cache` 파사드의 `put` 메서드를 사용해 캐시에 데이터를 저장할 수 있습니다:

```
Cache::put('key', 'value', $seconds = 10);
```

`put` 메서드에 저장 시간을 넘기지 않으면 항목이 무기한 저장됩니다:

```
Cache::put('key', 'value');
```

초 단위 값 대신 `DateTime` 객체를 넘겨 만료 시간을 명시할 수도 있습니다:

```
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
#### 없을 때만 저장하기

`add` 메서드는 캐시에 해당 키가 없을 때만 저장합니다. 저장에 성공하면 `true`를 반환하고, 그렇지 않으면 `false`를 반환합니다. 이 작업은 원자적(atomic)입니다:

```
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 항목을 영구 저장하기

`forever` 메서드는 캐시에 항목을 영구 저장할 때 사용합니다. 만료되지 않으므로 나중에 직접 `forget` 메서드로 삭제해야 합니다:

```
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우 "영구 저장"한 항목도 캐시 크기 한도에 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드를 사용해 캐시 항목을 제거할 수 있습니다:

```
Cache::forget('key');
```

만료 시간을 0 또는 음수로 지정해 저장하면 항목이 즉시 삭제됩니다:

```
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메서드를 사용하면 캐시를 완전히 비울 수 있습니다:

```
Cache::flush();
```

> [!WARNING]
> `flush`는 설정된 캐시 "프리픽스"를 무시하고 캐시의 모든 항목을 제거합니다. 다른 애플리케이션과 공유하는 캐시라면 신중히 고려해서 사용하세요.

<a name="the-cache-helper"></a>
### 캐시 헬퍼 함수

`Cache` 파사드를 사용하는 대신 전역 `cache` 함수를 사용해 캐시 작업을 할 수도 있습니다. `cache` 함수에 단일 문자열 인수를 넘기면 해당 키의 값을 반환합니다:

```
$value = cache('key');
```

키-값 배열과 만료 시간을 넘기면 캐시에 값을 저장합니다:

```
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

인수 없이 호출하면 `Illuminate\Contracts\Cache\Factory` 구현체 인스턴스를 반환하므로 추가 캐시 메서드를 사용할 수 있습니다:

```
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수 호출을 테스트할 때는 `Cache::shouldReceive` 메서드를 사용해 파사드를 테스트하는 것과 동일하게 진행할 수 있습니다. [파사드 테스트 문서](/docs/9.x/mocking#mocking-facades) 참고.

<a name="cache-tags"></a>
## 캐시 태그

> [!WARNING]
> `file`, `dynamodb`, `database` 캐시 드라이버에서는 캐시 태그가 지원되지 않습니다. 또한, 여러 태그를 사용하는 "영구 저장" 캐시에서는 `memcached` 같은 드라이버가 자동으로 오래된 레코드를 제거해주므로 성능이 가장 좋습니다.

<a name="storing-tagged-cache-items"></a>
### 태그된 캐시 항목 저장하기

캐시 태그는 관련된 항목들을 태그로 묶고 해당 태그가 지정된 모든 캐시 값을 한 번에 삭제할 수 있게 합니다. 태그 캐시에 접근하려면 태그 이름을 순서대로 배열로 전달합니다. 예를 들어, 태그된 캐시에 값을 `put` 하는 방법은 다음과 같습니다:

```
Cache::tags(['people', 'artists'])->put('John', $john, $seconds);

Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### 태그된 캐시 항목 접근하기

태그된 캐시 항목은 해당 태그와 함께 접근해야만 조회할 수 있습니다. 값이 저장된 태그와 같은 순서의 태그 리스트를 `tags` 메서드에 넘기고, `get` 메서드로 값을 가져옵니다:

```
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### 태그된 캐시 항목 제거하기

특정 태그나 태그들의 모든 항목을 제거하려면 `flush` 메서드를 사용할 수 있습니다. 예를 들어, 다음 코드는 `people`, `authors` 태그가 지정된 캐시 항목을 모두 삭제합니다. 따라서 `Anne`과 `John` 둘 다 캐시에서 삭제됩니다:

```
Cache::tags(['people', 'authors'])->flush();
```

반면 다음 코드는 `authors` 태그가 지정된 항목만 삭제합니다. 따라서 `Anne`만 삭제되고 `John`은 남습니다:

```
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 원자적 락 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 드라이버 중 하나여야 합니다. 또한 모든 서버가 같은 중앙 캐시 서버와 통신하고 있어야 합니다.

<a name="lock-driver-prerequisites"></a>
### 드라이버 필수 조건

<a name="atomic-locks-prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용한다면, 애플리케이션의 캐시 락을 저장할 테이블을 생성해야 합니다. 아래는 `Schema` 예시입니다:

```
Schema::create('cache_locks', function ($table) {
    $table->string('key')->primary();
    $table->string('owner');
    $table->integer('expiration');
});
```

<a name="managing-locks"></a>
### 락 관리하기

원자적 락을 사용하면 경쟁 상태를 걱정하지 않고 분산 락을 조작할 수 있습니다. 예를 들어 [Laravel Forge](https://forge.laravel.com)는 서버에서 한 번에 하나의 원격 작업만 실행되도록 원자적 락을 활용합니다. `Cache::lock` 메서드로 락을 생성하고 관리할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // 10초간 락 획득...

    $lock->release();
}
```

`get` 메서드는 클로저도 인수로 받습니다. 클로저 실행 후 Laravel이 락을 자동으로 해제합니다:

```
Cache::lock('foo', 10)->get(function () {
    // 10초간 락을 획득하고 클로저 실행이 끝나면 자동으로 해제...
});
```

락을 즉시 얻지 못하면 지정한 초만큼 기다릴 수도 있습니다. 제한 시간 내 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

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

위 예시는 클로저를 `block` 메서드에 전달해 다음과 같이 간략하게 작성할 수도 있습니다. 클로저가 실행 완료되면 락이 자동 해제됩니다:

```
Cache::lock('foo', 10)->block(5, function () {
    // 최대 5초 대기 후 락 획득 및 클로저 실행...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리하기

가끔 한 프로세스에서 락을 얻고 다른 프로세스에서 락을 해제해야 할 때가 있습니다. 예를 들어 웹 요청 중 락을 획득하고, 이 요청으로 트리거된 대기열 작업에서 락을 해제하는 경우입니다. 이 경우 락의 범위 내 "소유자 토큰"을 작업에 전달해, 작업이 락을 같은 토큰으로 다시 생성할 수 있게 해야 합니다.

예를 들어 락 획득에 성공하면 대기열 작업을 디스패치하고, 락 소유자 토큰을 함께 전달하는 코드입니다:

```
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

`ProcessPodcast` 작업에서는 소유자 토큰으로 락을 복원하고 해제할 수 있습니다:

```
Cache::restoreLock('processing', $this->owner)->release();
```

락을 현재 소유자 체크 없이 강제로 해제하려면 `forceRelease` 메서드를 사용합니다:

```
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가하기

<a name="writing-the-driver"></a>
### 드라이버 작성하기

새 커스텀 캐시 드라이버를 만들려면 우선 `Illuminate\Contracts\Cache\Store` [계약](/docs/9.x/contracts)을 구현해야 합니다. 예를 들어 MongoDB 캐시 드라이버 구현 코드는 다음과 같을 수 있습니다:

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

여기서 각 메서드는 MongoDB 연결을 사용해 구현하면 됩니다. Laravel 프레임워크 소스 코드의 `Illuminate\Cache\MemcachedStore` 클래스를 참고해 구현 방법을 익힐 수 있습니다. 구현이 완료되면 `Cache` 파사드의 `extend` 메서드를 호출해 커스텀 드라이버 등록을 마무리합니다:

```
Cache::extend('mongo', function ($app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 두어야 할지 고민된다면, `app` 디렉터리 내 `Extensions` 네임스페이스를 만들어 관리하는 것도 좋습니다. 다만 Laravel은 엄격한 애플리케이션 구조를 강제하지 않으므로 원하는 방식대로 자유롭게 조직하세요.

<a name="registering-the-driver"></a>
### 드라이버 등록하기

Laravel에 커스텀 캐시 드라이버를 등록하려면 `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더들이 `boot` 메서드 내에서 캐시를 읽으려 시도할 수 있으므로, 우리는 `booting` 콜백 안에서 드라이버를 등록하는 것이 안전합니다. 이렇게 하면 서비스 프로바이더들의 `register` 메서드 호출 이후, `boot` 메서드 호출 이전에 커스텀 드라이버가 등록됩니다.

아래 예시는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내 `register` 메서드에서 `booting` 콜백을 등록하는 방법입니다:

```
<?php

namespace App\Providers;

use App\Extensions\MongoStore;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\ServiceProvider;

class CacheServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
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
     * 애플리케이션 서비스 부트스트랩
     *
     * @return void
     */
    public function boot()
    {
        //
    }
}
```

`extend` 메서드의 첫 번째 인자는 드라이버 이름이며, 이는 `config/cache.php` 설정 파일의 `driver` 옵션 값과 일치해야 합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저입니다. 클로저에는 `$app` 인자가 전달되며, 이는 서비스 컨테이너 인스턴스입니다.

확장 드라이버를 등록한 후에는 `config/cache.php` 설정에서 `driver` 값을 새 드라이버 이름으로 변경하세요.

<a name="events"></a>
## 이벤트

모든 캐시 작업 시 실행할 코드를 정의하려면, 캐시가 발생시키는 [이벤트](/docs/9.x/events)를 감지할 수 있습니다. 일반적으로 이벤트 리스너는 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에 정의합니다:

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