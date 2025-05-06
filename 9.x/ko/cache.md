# 캐시(Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 사전 준비](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 조회하기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 헬퍼](#the-cache-helper)
- [캐시 태그](#cache-tags)
    - [태그된 캐시 항목 저장하기](#storing-tagged-cache-items)
    - [태그된 캐시 항목 접근하기](#accessing-tagged-cache-items)
    - [태그된 캐시 항목 제거하기](#removing-tagged-cache-items)
- [원자적 락](#atomic-locks)
    - [드라이버 사전 준비](#lock-driver-prerequisites)
    - [락 관리하기](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가](#adding-custom-cache-drivers)
    - [드라이버 작성](#writing-the-driver)
    - [드라이버 등록](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

애플리케이션에서 수행하는 일부 데이터 조회 또는 처리 작업은 CPU 연산이 많이 필요하거나 몇 초가 걸릴 수 있습니다. 이럴 때는 조회된 데이터를 일정 시간 동안 캐시에 저장하여 같은 데이터에 대한 다음 요청 시 빠르게 불러올 수 있도록 하는 것이 일반적입니다. 캐시된 데이터는 주로 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히도 라라벨은 여러 캐시 백엔드를 위한 직관적이고 통합된 API를 제공하여, 이들 백엔드의 빠른 데이터 조회 기능을 활용하여 웹 애플리케이션의 속도를 크게 높일 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치해 있습니다. 이 파일에서 애플리케이션이 기본적으로 사용할 캐시 드라이버를 지정할 수 있습니다. 라라벨은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등 널리 쓰이는 캐시 백엔드를 기본적으로 지원합니다. 또한 파일 기반 캐시 드라이버도 제공하며, `array`와 "null" 캐시 드라이버는 자동화 테스트 시 편리한 캐시 백엔드를 제공합니다.

캐시 설정 파일에는 이외에도 다양한 옵션이 있으며, 각 옵션에 대한 설명이 파일 내에 문서화되어 있으니 꼭 읽어 보시기 바랍니다. 기본적으로 라라벨은 직렬화된 캐시 객체를 서버의 파일 시스템에 저장하는 `file` 캐시 드라이버를 사용하도록 되어있습니다. 규모가 큰 애플리케이션의 경우, 보다 견고한 드라이버인 Memcached나 Redis 사용을 권장합니다. 동일한 드라이버로 여러 캐시 구성을 할 수도 있습니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 때는 캐시 항목을 담을 테이블을 만들어야 합니다. 아래는 테이블의 예시 `Schema` 정의입니다:

    Schema::create('cache', function ($table) {
        $table->string('key')->unique();
        $table->text('value');
        $table->integer('expiration');
    });

> **참고**  
> `php artisan cache:table` Artisan 명령어를 사용하여 적절한 스키마로 마이그레이션 파일을 생성할 수도 있습니다.

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. `config/cache.php` 설정 파일에서 Memcached 서버를 모두 나열할 수 있으며, 이 파일에는 이미 시작을 위한 `memcached.servers` 항목이 포함되어 있습니다.

    'memcached' => [
        'servers' => [
            [
                'host' => env('MEMCACHED_HOST', '127.0.0.1'),
                'port' => env('MEMCACHED_PORT', 11211),
                'weight' => 100,
            ],
        ],
    ],

필요하다면 `host` 옵션에 UNIX 소켓 경로로도 설정할 수 있습니다. 이 경우 `port` 옵션은 `0`으로 설정해야 합니다:

    'memcached' => [
        [
            'host' => '/var/run/memcached/memcached.sock',
            'port' => 0,
            'weight' => 100
        ],
    ],

<a name="redis"></a>
#### Redis

라라벨에서 Redis 캐시를 사용하려면 PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. [Laravel Sail](/docs/{{version}}/sail)에는 이미 이 확장 모듈이 포함되어 있습니다. 또한, [Laravel Forge](https://forge.laravel.com), [Laravel Vapor](https://vapor.laravel.com) 등 공식 라라벨 배포 플랫폼에는 PhpRedis 확장 프로그램이 기본적으로 설치되어 있습니다.

Redis 설정에 대한 자세한 내용은 [라라벨 공식 문서](/docs/{{version}}/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전, 캐시된 모든 데이터를 보관할 DynamoDB 테이블을 만들어야 합니다. 이 테이블은 보통 `cache`라는 이름을 사용하지만, 애플리케이션의 `cache` 설정 파일에 있는 `stores.dynamodb.table` 값에 따라 이름을 정해야 합니다.

이 테이블에는 문자열 파티션 키가 있어야 하며, 이 이름도 역시 `stores.dynamodb.attributes.key` 설정 값에 맞춰야 합니다. 기본적으로 파티션 키 이름은 `key`입니다.

<a name="cache-usage"></a>
## 캐시 사용법

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드를 사용할 수 있습니다. 본 문서 전반에서도 `Cache` 파사드를 사용합니다. `Cache` 파사드는 라라벨 캐시 계약의 기본 구현체에 간편하고 직관적으로 접근할 수 있게 해줍니다:

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

<a name="accessing-multiple-cache-stores"></a>
#### 여러 캐시 저장소 접근하기

`Cache` 파사드를 사용하여 `store` 메서드로 여러 캐시 저장소에도 접근할 수 있습니다. `store` 메서드에 전달되는 키는 `cache` 설정 파일의 `stores` 구성 배열에 나열된 저장소 중 하나와 일치해야 합니다.

    $value = Cache::store('file')->get('foo');

    Cache::store('redis')->put('bar', 'baz', 600); // 10분

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 조회하기

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 조회할 때 사용됩니다. 항목이 캐시에 존재하지 않으면 `null`이 반환됩니다. 필요하다면 두 번째 인자를 통해 항목이 존재하지 않을 때 반환할 기본값을 지정할 수도 있습니다:

    $value = Cache::get('key');

    $value = Cache::get('key', 'default');

기본값으로 클로저를 전달할 수도 있습니다. 지정한 항목이 캐시에 없을 경우 클로저의 결과가 반환되며, 클로저를 사용하여 데이터베이스나 외부 서비스에서 기본값을 나중에 가져오게 할 수 있습니다:

    $value = Cache::get('key', function () {
        return DB::table(/* ... */)->get();
    });

<a name="checking-for-item-existence"></a>
#### 항목 존재 여부 확인

`has` 메서드를 통해 캐시에 항목이 존재하는지 확인할 수 있습니다. 이 메서드는 항목이 존재하더라도 값이 `null`이면 `false`를 반환합니다.

    if (Cache::has('key')) {
        //
    }

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소

`increment`와 `decrement` 메서드를 이용해 캐시에 저장된 정수값을 증가시키거나 감소시킬 수 있습니다. 두 메서드 모두 두 번째 인자로 증감할 값을 받을 수 있습니다:

    Cache::increment('key');
    Cache::increment('key', $amount);
    Cache::decrement('key');
    Cache::decrement('key', $amount);

<a name="retrieve-store"></a>
#### 조회 후 저장

가끔 캐시에서 항목을 조회하면서 동시에 요청한 항목이 없으면 기본값을 저장하고 싶을 수 있습니다. 예를 들어, 모든 사용자 정보를 캐시에서 조회하거나 없다면 데이터베이스에서 가져온 뒤 캐시에 저장할 수도 있습니다. 이런 경우 `Cache::remember` 메서드를 사용할 수 있습니다:

    $value = Cache::remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

캐시에 항목이 존재하지 않으면 클로저가 실행되며, 그 결과가 캐시에 저장됩니다.

항목을 영구적으로 저장하고 싶다면 `rememberForever` 메서드를 사용할 수 있습니다:

    $value = Cache::rememberForever('users', function () {
        return DB::table('users')->get();
    });

<a name="retrieve-delete"></a>
#### 조회 후 삭제

캐시에서 항목을 조회한 뒤, 바로 삭제하고 싶을 때는 `pull` 메서드를 사용할 수 있습니다. `get` 메서드와 마찬가지로, 항목이 없으면 `null`이 반환됩니다.

    $value = Cache::pull('key');

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

`Cache` 파사드의 `put` 메서드를 사용해 캐시에 항목을 저장할 수 있습니다:

    Cache::put('key', 'value', $seconds = 10);

만약 저장 시간을 지정하지 않으면 해당 항목은 영구적으로 저장됩니다:

    Cache::put('key', 'value');

정수형 초 값을 전달하는 대신, 캐시 만료 시점을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다:

    Cache::put('key', 'value', now()->addMinutes(10));

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장

`add` 메서드는 해당 항목이 캐시에 존재하지 않을 때에만 저장이 진행됩니다. 실제로 저장이 되면 `true`를 반환하고, 이미 존재한다면 `false`를 반환합니다. `add` 메서드는 원자적 동작입니다:

    Cache::add('key', 'value', $seconds);

<a name="storing-items-forever"></a>
#### 항목 영구 저장

`forever` 메서드를 사용하면 만료 없이 캐시에 영구적으로 항목을 저장할 수 있습니다. 영구 저장된 항목은 만료되지 않으므로, 직접 `forget` 메서드로 제거해야 합니다:

    Cache::forever('key', 'value');

> **참고**  
> Memcached 드라이버를 사용하는 경우, "영구"로 저장한 항목도 캐시 크기 제한에 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드를 사용해 캐시에서 항목을 제거할 수 있습니다:

    Cache::forget('key');

만료 시간(초 단위)에 0 또는 음수 값을 주면, 항목도 제거할 수 있습니다:

    Cache::put('key', 'value', 0);

    Cache::put('key', 'value', -5);

캐시 전체를 비우려면 `flush` 메서드를 사용하세요:

    Cache::flush();

> **경고**  
> 캐시 플러시는 설정된 캐시 "prefix"를 고려하지 않으며 캐시의 모든 항목을 삭제합니다. 다른 애플리케이션과 캐시를 공유할 경우 주의하셔야 합니다.

<a name="the-cache-helper"></a>
### 캐시 헬퍼

`Cache` 파사드를 사용하는 것 외에도, 전역 `cache` 함수를 통해 간편하게 캐시 저장 및 조회가 가능합니다. `cache` 함수에 문자열 형태의 단일 인자를 주면 해당 키에 대한 값을 반환합니다:

    $value = cache('key');

키/값 배열과 만료 시간을 함께 전달하면, 지정된 기간만큼 캐시에 저장합니다:

    cache(['key' => 'value'], $seconds);

    cache(['key' => 'value'], now()->addMinutes(10));

인자 없이 호출할 경우, `Illuminate\Contracts\Cache\Factory`의 인스턴스를 반환하므로 다른 캐시 관련 메서드를 사용할 수 있습니다:

    cache()->remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

> **참고**  
> 글로벌 `cache` 함수 호출을 테스트할 때도 [파사드 테스트 방법](/docs/{{version}}/mocking#mocking-facades)과 동일하게 `Cache::shouldReceive`를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그

> **경고**  
> 캐시 태그는 `file`, `dynamodb`, `database` 캐시 드라이버에서는 지원되지 않습니다. 또한, 여러 태그를 "영구" 캐시에 사용하는 경우 `memcached`와 같이 오래된 레코드를 자동으로 정리하는 드라이버를 쓰는 것이 성능에 이점이 있습니다.

<a name="storing-tagged-cache-items"></a>
### 태그된 캐시 항목 저장하기

캐시 태그를 사용하면 관련 항목을 캐시에 태그로 묶어두고, 특정 태그가 할당된 값들을 한 번에 모두 삭제할 수 있습니다. 태그가 적용된 캐시에 접근하려면 정렬된 태그명 배열을 전달하면 됩니다. 예를 들어, 다음과 같이 태그가 적용된 캐시에 값을 저장할 수 있습니다:

    Cache::tags(['people', 'artists'])->put('John', $john, $seconds);

    Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);

<a name="accessing-tagged-cache-items"></a>
### 태그된 캐시 항목 접근하기

태그로 저장한 항목은, 값을 저장할 때 썼던 태그 정보를 다시 제공해야만 접근할 수 있습니다. 즉, 같은 순서의 태그 목록과 항목 키를 `tags` 및 `get` 메서드에 전달해야 합니다:

    $john = Cache::tags(['people', 'artists'])->get('John');

    $anne = Cache::tags(['people', 'authors'])->get('Anne');

<a name="removing-tagged-cache-items"></a>
### 태그된 캐시 항목 제거하기

하나 또는 여러 태그가 할당된 모든 항목을 플러시(삭제)할 수 있습니다. 예를 들어, 아래와 같이 `people` 또는 `authors` 태그가 할당된 모든 캐시가 제거되며, 결과적으로 `Anne`과 `John` 모두 삭제됩니다:

    Cache::tags(['people', 'authors'])->flush();

반대로, 아래는 `authors` 태그만 붙은 값만 삭제하므로 `Anne`만 제거되고 `John`은 남게 됩니다:

    Cache::tags('authors')->flush();

<a name="atomic-locks"></a>
## 원자적 락(Atomic Locks)

> **경고**  
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버는 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="lock-driver-prerequisites"></a>
### 드라이버 사전 준비

<a name="atomic-locks-prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버로 락을 사용하려면, 앱의 캐시 락을 저장할 테이블을 만들어야 합니다. 아래는 예시 `Schema` 정의입니다:

    Schema::create('cache_locks', function ($table) {
        $table->string('key')->primary();
        $table->string('owner');
        $table->integer('expiration');
    });

<a name="managing-locks"></a>
### 락 관리하기

원자적 락을 사용하면 경쟁 조건(race condition) 없이 분산 락을 관리할 수 있습니다. 예를 들어, [Laravel Forge](https://forge.laravel.com)에서는 서버에서 한 번에 하나의 원격 작업만 실행되도록 원자적 락을 사용합니다. 락 생성 및 관리는 `Cache::lock` 메서드로 할 수 있습니다:

    use Illuminate\Support\Facades\Cache;

    $lock = Cache::lock('foo', 10);

    if ($lock->get()) {
        // 10초간 락을 획득함...

        $lock->release();
    }

`get` 메서드는 클로저도 받을 수 있는데, 클로저가 실행되고 나면 라라벨이 락을 자동으로 해제해줍니다:

    Cache::lock('foo', 10)->get(function () {
        // 10초간 락을 획득하고, 실행 후 자동 해제...
    });

요청 시 락이 아직 사용 중이라면, 라라벨에 몇 초간 대기하도록 지시할 수 있습니다. 주어진 시간 내에 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

    use Illuminate\Contracts\Cache\LockTimeoutException;

    $lock = Cache::lock('foo', 10);

    try {
        $lock->block(5);

        // 최대 5초 대기 후 락을 획득...
    } catch (LockTimeoutException $e) {
        // 락을 획득할 수 없음...
    } finally {
        optional($lock)->release();
    }

위 예시는 `block` 메서드에 클로저를 전달하면 더욱 간단하게 표현할 수 있습니다. 클로저가 실행된 후 락은 자동으로 해제됩니다:

    Cache::lock('foo', 10)->block(5, function () {
        // 최대 5초 대기 후 락을 획득...
    });

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

경우에 따라서는 한 프로세스에서 락을 획득하고, 다른 프로세스에서 락을 해제해야 할 수 있습니다. 예를 들어, 웹 요청 중에 락을 획득하고, 해당 요청이 트리거한 큐 작업의 마지막에 락을 해제해야 할 수 있습니다. 이때 락의 "owner 토큰"을 큐 작업에 전달하고, 작업이 토큰을 통해 동일한 락을 복원해 해제하도록 하면 됩니다.

아래 예제에선, 락을 성공적으로 획득하면 큐 작업을 디스패치하며, 락의 `owner` 메서드를 이용해 토큰을 전달합니다:

    $podcast = Podcast::find($id);

    $lock = Cache::lock('processing', 120);

    if ($lock->get()) {
        ProcessPodcast::dispatch($podcast, $lock->owner());
    }

`ProcessPodcast` 작업 내에서는 owner 토큰을 사용하여 락을 복원하고 해제할 수 있습니다:

    Cache::restoreLock('processing', $this->owner)->release();

현재 소유자를 무시하고 락을 강제 해제하려면 `forceRelease` 메서드를 사용할 수 있습니다:

    Cache::lock('processing')->forceRelease();

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가

<a name="writing-the-driver"></a>
### 드라이버 작성

커스텀 캐시 드라이버를 만들기 위해서는 먼저 `Illuminate\Contracts\Cache\Store` [계약](/docs/{{version}}/contracts)을 구현해야 합니다. MongoDB 캐시 구현은 다음과 유사하게 작성할 수 있습니다:

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

이 메서드들을 MongoDB 연결을 사용하여 실제로 구현하면 됩니다. 각 메서드의 구현 예는 라라벨 프레임워크의 `Illuminate\Cache\MemcachedStore` 소스([GitHub](https://github.com/laravel/framework))를 참고하세요. 구현이 끝나면, `Cache` 파사드의 `extend` 메서드를 호출해 커스텀 드라이버 등록을 마무리합니다:

    Cache::extend('mongo', function ($app) {
        return Cache::repository(new MongoStore);
    });

> **참고**  
> 커스텀 캐시 드라이버 코드를 어디에 둘지 고민될 경우 `app` 디렉터리 안에 `Extensions` 네임스페이스를 만들어 놓을 수 있습니다. 라라벨은 구조에 제한이 없으므로 자유롭게 구성하세요.

<a name="registering-the-driver"></a>
### 드라이버 등록

라라벨에 커스텀 캐시 드라이버를 등록하려면 `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 자신의 `boot` 메서드에서 캐시 값을 읽을 수 있으므로, 우리는 커스텀 드라이버 등록을 `booting` 콜백에서 처리합니다. 이렇게 하면, 서비스 프로바이더에서 `boot`가 호출되기 바로 전에 사용자 드라이버가 등록되며, 모든 프로바이더의 `register` 실행 이후에 호출 가능합니다. `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `booting` 콜백을 등록합니다:

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

`extend` 메서드에 전달된 첫 번째 인자는 드라이버 이름이며, 이는 `config/cache.php` 설정 파일의 `driver` 옵션과 일치해야 합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하는 클로저이며, 클로저에는 [서비스 컨테이너](/docs/{{version}}/container) 인스턴스인 `$app`이 전달됩니다.

확장 기능이 등록되면, `config/cache.php` 설정 파일의 `driver` 옵션을 여러분의 확장명으로 변경하세요.

<a name="events"></a>
## 이벤트(Events)

모든 캐시 동작 시 코드를 실행하고 싶다면, 캐시에서 발생하는 [이벤트](/docs/{{version}}/events)를 리스닝할 수 있습니다. 보통 이러한 이벤트 리스너는 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에 지정합니다:
    
    use App\Listeners\LogCacheHit;
    use App\Listeners\LogCacheMissed;
    use App\Listeners\LogKeyForgotten;
    use App\Listeners\LogKeyWritten;
    use Illuminate\Cache\Events\CacheHit;
    use Illuminate\Cache\Events\CacheMissed;
    use Illuminate\Cache\Events\KeyForgotten;
    use Illuminate\Cache\Events\KeyWritten;
    
    /**
     * 애플리케이션의 이벤트 리스너 매핑
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
