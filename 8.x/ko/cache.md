# 캐시(Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 필수 조건](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [Cache 헬퍼](#the-cache-helper)
- [캐시 태그](#cache-tags)
    - [태그가 지정된 캐시 항목 저장](#storing-tagged-cache-items)
    - [태그가 지정된 캐시 항목 접근](#accessing-tagged-cache-items)
    - [태그가 지정된 캐시 항목 제거](#removing-tagged-cache-items)
- [원자적(Atomic) 락](#atomic-locks)
    - [드라이버 필수 조건](#lock-driver-prerequisites)
    - [락 관리](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

애플리케이션에서 수행하는 데이터 조회 또는 처리 작업 중 일부는 높은 CPU 자원을 요구하거나 몇 초가 걸릴 수 있습니다. 이러한 경우, 데이터를 한 번 조회한 뒤 일정 시간 동안 캐시에 저장하여 동일한 데이터에 대한 후속 요청 시 빠르게 반환할 수 있도록 하는 것이 일반적입니다. 캐시된 데이터는 일반적으로 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히도, Laravel은 다양한 캐시 백엔드에 대해 직관적이고 통합된 API를 제공하여, 강력한 캐시 성능을 웹 애플리케이션에 손쉽게 적용할 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서 여러분은 애플리케이션 전체에서 기본적으로 사용할 캐시 드라이버를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등 널리 쓰이는 캐싱 백엔드를 기본적으로 지원합니다. 또한 파일 기반 캐시 드라이버와 더불어, 자동화된 테스트에 유용한 `array` 및 "null" 캐시 드라이버도 제공합니다.

캐시 설정 파일에는 이 외에도 여러 가지 옵션이 문서화되어 있으니 반드시 읽어보시기 바랍니다. 기본적으로 Laravel은 직렬화된 캐시 객체를 서버의 파일 시스템에 저장하는 `file` 캐시 드라이버를 사용하도록 설정되어 있습니다. 규모가 큰 애플리케이션의 경우 Memcached나 Redis 등 더 강력한 드라이버 사용을 권장합니다. 동일한 드라이버에 대해 여러 캐시 설정을 구성할 수도 있습니다.

<a name="driver-prerequisites"></a>
### 드라이버 필수 조건

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 때는 캐시 항목을 저장할 테이블을 생성해야 합니다. 아래는 테이블 생성을 위한 예시 `Schema` 선언입니다:

    Schema::create('cache', function ($table) {
        $table->string('key')->unique();
        $table->text('value');
        $table->integer('expiration');
    });

> {tip} `php artisan cache:table` Artisan 명령어를 사용하면 올바른 스키마로 마이그레이션을 생성할 수 있습니다.

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. 모든 Memcached 서버 정보는 `config/cache.php` 설정 파일에 나열할 수 있습니다. 이 파일에는 이미 시작을 위한 `memcached.servers` 항목이 포함되어 있습니다:

    'memcached' => [
        'servers' => [
            [
                'host' => env('MEMCACHED_HOST', '127.0.0.1'),
                'port' => env('MEMCACHED_PORT', 11211),
                'weight' => 100,
            ],
        ],
    ],

필요하다면, `host` 옵션에 UNIX 소켓 경로를 설정할 수도 있습니다. 이 경우, `port` 옵션은 `0`으로 설정해야 합니다:

    'memcached' => [
        [
            'host' => '/var/run/memcached/memcached.sock',
            'port' => 0,
            'weight' => 100
        ],
    ],

<a name="redis"></a>
#### Redis

Laravel에서 Redis 캐시를 사용하기 전에 PECL을 통해 PhpRedis PHP 확장 프로그램을 설치하거나 Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. [Laravel Sail](/docs/{{version}}/sail)에는 이미 이 확장 프로그램이 포함되어 있습니다. 또한 [Laravel Forge](https://forge.laravel.com) 및 [Laravel Vapor](https://vapor.laravel.com)와 같은 공식 Laravel 배포 플랫폼에도 PhpRedis 확장 프로그램이 기본 설치되어 있습니다.

Redis 설정에 대한 자세한 내용은 [Laravel 문서](/docs/{{version}}/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에 모든 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 이 테이블의 이름은 `cache`여야 합니다. 하지만 테이블명은 애플리케이션의 `cache` 설정 파일 내 `stores.dynamodb.table` 값에 따라 지정해야 합니다.

또한, 이 테이블에는 파티션 키로 문자열 타입의 필드가 포함되어야 하며, 이 키의 이름도 `stores.dynamodb.attributes.key` 설정 값과 일치해야 합니다. 기본적으로 파티션 키의 이름은 `key`입니다.

<a name="cache-usage"></a>
## 캐시 사용법

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드를 사용할 수 있습니다. 이 문서 전체에서 `Cache` 파사드를 주로 예시로 사용합니다. `Cache` 파사드는 Laravel 캐시 계약의 구현체에 간편하게 접근할 수 있도록 해줍니다:

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
#### 여러 캐시 저장소 접근

`Cache` 파사드를 사용하면 `store` 메서드를 통해 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일의 `stores` 배열에 정의된 저장소명과 일치해야 합니다:

    $value = Cache::store('file')->get('foo');

    Cache::store('redis')->put('bar', 'baz', 600); // 10분

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 가져오는 데 사용됩니다. 항목이 캐시에 없으면 `null`이 반환됩니다. 두 번째 인자로 기본값을 지정하여, 항목이 없을 때 반환될 값을 설정할 수도 있습니다:

    $value = Cache::get('key');

    $value = Cache::get('key', 'default');

기본값으로 클로저를 전달할 수도 있습니다. 지정된 항목이 캐시에 없을 경우 클로저의 결과가 반환됩니다. 클로저를 전달하면 데이터베이스나 외부 서비스에서 기본값을 나중에 불러오도록 할 수 있습니다:

    $value = Cache::get('key', function () {
        return DB::table(...)->get();
    });

<a name="checking-for-item-existence"></a>
#### 항목 존재 여부 확인

`has` 메서드를 사용하여 캐시에 항목이 존재하는지 확인할 수 있습니다. 이 메서드는 항목이 존재하지만 값이 `null`일 때도 `false`를 반환합니다:

    if (Cache::has('key')) {
        //
    }

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소

`increment`와 `decrement` 메서드는 캐시에 저장된 정수형 항목의 값을 조정하는 데 사용할 수 있습니다. 두 메서드 모두 두 번째 인자로 증감량을 받을 수 있습니다:

    Cache::increment('key');
    Cache::increment('key', $amount);
    Cache::decrement('key');
    Cache::decrement('key', $amount);

<a name="retrieve-store"></a>
#### 조회 & 저장

가끔 캐시에서 항목을 조회하되, 없다면 기본값을 저장하고 싶을 때가 있습니다. 예를 들어, 모든 사용자를 캐시에서 읽고, 없으면 데이터베이스에서 가져와 캐시에 저장할 수 있습니다. `Cache::remember` 메서드를 사용할 수 있습니다:

    $value = Cache::remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

항목이 캐시에 없으면 클로저가 실행되고, 해당 결과가 캐시에 저장됩니다.

`rememberForever` 메서드를 사용하면 캐시에 영구적으로 항목을 저장할 수도 있습니다:

    $value = Cache::rememberForever('users', function () {
        return DB::table('users')->get();
    });

<a name="retrieve-delete"></a>
#### 조회 & 삭제

캐시에서 항목을 가져온 후 삭제하려면 `pull` 메서드를 사용하세요. `get` 메서드와 마찬가지로, 항목이 없으면 `null`이 반환됩니다:

    $value = Cache::pull('key');

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

`Cache` 파사드에서 `put` 메서드를 사용해 캐시에 항목을 저장할 수 있습니다:

    Cache::put('key', 'value', $seconds = 10);

저장 시간을 생략하면 항목이 무기한 저장됩니다:

    Cache::put('key', 'value');

초 단위 대신 만료 시간에 해당하는 `DateTime` 인스턴스를 전달할 수도 있습니다:

    Cache::put('key', 'value', now()->addMinutes(10));

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장

`add` 메서드는 항목이 캐시에 아직 없을 때만 저장합니다. 실제로 캐시에 추가되면 `true`, 아니면 `false`를 반환합니다. `add` 메서드는 원자적(atomic) 연산입니다:

    Cache::add('key', 'value', $seconds);

<a name="storing-items-forever"></a>
#### 영구 저장

`forever` 메서드는 항목을 캐시에 영구적으로 저장할 수 있습니다. 이러한 항목은 만료되지 않으므로, 삭제가 필요할 경우 `forget` 메서드를 사용해 직접 삭제해야 합니다:

    Cache::forever('key', 'value');

> {tip} Memcached 드라이버를 사용할 경우, "영구 저장"된 항목도 캐시 용량이 한계에 도달하면 제거될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드를 사용하여 캐시에서 항목을 제거할 수 있습니다:

    Cache::forget('key');

만료 시간을 0 또는 음수로 설정해 항목을 제거할 수도 있습니다:

    Cache::put('key', 'value', 0);

    Cache::put('key', 'value', -5);

`flush` 메서드를 사용하면 캐시 전체를 비울 수 있습니다:

    Cache::flush();

> {note} 캐시 전체 비우기(Flush)는 설정된 캐시 "prefix"를 무시하고, 모든 항목을 제거합니다. 여러 애플리케이션이 캐시를 공유하는 경우, 전체 비우기는 신중히 사용하세요.

<a name="the-cache-helper"></a>
### Cache 헬퍼

`Cache` 파사드 외에도, 글로벌 `cache` 함수를 사용해 캐시를 조회·저장할 수 있습니다. 단일 문자열 인자로 호출하면 해당 키의 값을 반환합니다:

    $value = cache('key');

키-값의 배열과 만료 시간을 전달하면 지정된 기간 동안 값을 캐시에 저장합니다:

    cache(['key' => 'value'], $seconds);

    cache(['key' => 'value'], now()->addMinutes(10));

인자 없이 호출하면 `Illuminate\Contracts\Cache\Factory` 인스턴스를 반환하므로, 다른 캐시 메서드도 호출할 수 있습니다:

    cache()->remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

> {tip} 글로벌 `cache` 함수 호출을 테스트할 때 [파사드 테스트](/docs/{{version}}/mocking#mocking-facades)처럼 `Cache::shouldReceive`를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그

> {note} 캐시 태그는 `file`, `dynamodb`, `database` 캐시 드라이버에서 지원되지 않습니다. 또한 여러 태그를 "영구 저장"하는 경우, 낡은 레코드 정리가 자동으로 가능한 `memcached`와 같은 드라이버에서 가장 성능이 잘 나옵니다.

<a name="storing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 저장

캐시 태그를 사용하면 연관된 캐시 항목들을 태그로 묶고, 특정 태그가 지정된 모든 값을 한 번에 비울 수 있습니다. 태그 이름의 배열을 전달해 태그가 지정된 캐시에 접근하고, 다음처럼 항목을 저장할 수 있습니다:

    Cache::tags(['people', 'artists'])->put('John', $john, $seconds);

    Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);

<a name="accessing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 접근

태그가 지정된 캐시 항목을 가져오려면 동일한 태그 배열을 `tags` 메서드에 전달한 후, `get` 메서드로 조회합니다:

    $john = Cache::tags(['people', 'artists'])->get('John');

    $anne = Cache::tags(['people', 'authors'])->get('Anne');

<a name="removing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 제거

하나 이상의 태그가 지정된 모든 항목을 플러시(비우기)할 수 있습니다. 예를 들어 아래 코드는 `people`, `authors` 또는 두 태그 모두를 가진 모든 캐시 항목을 제거합니다. 이 때문에 `Anne`과 `John` 모두 캐시에서 삭제됩니다:

    Cache::tags(['people', 'authors'])->flush();

반대로, 아래 코드는 `authors` 태그가 지정된 항목만 삭제하기 때문에 `Anne`만 삭제되고 `John`은 남게 됩니다:

    Cache::tags('authors')->flush();

<a name="atomic-locks"></a>
## 원자적(Atomic) 락

> {note} 이 기능을 이용하려면 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array`를 사용해야 합니다. 또한, 모든 서버가 동일한 중앙 캐시 서버에 연결되어 있어야 합니다.

<a name="lock-driver-prerequisites"></a>
### 드라이버 필수 조건

<a name="atomic-locks-prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 때는 애플리케이션의 락 정보를 저장할 테이블도 생성해야 합니다. 아래는 예시 `Schema` 선언입니다:

    Schema::create('cache_locks', function ($table) {
        $table->string('key')->primary();
        $table->string('owner');
        $table->integer('expiration');
    });

<a name="managing-locks"></a>
### 락 관리

원자적 락은 경쟁 조건(race condition) 걱정 없이 분산 락을 처리할 수 있게 해줍니다. 예를 들어 [Laravel Forge](https://forge.laravel.com)에서는 동시에 오직 하나의 원격 작업만 서버에서 실행되도록 원자적 락을 사용합니다. `Cache::lock` 메서드로 락을 생성·관리할 수 있습니다:

    use Illuminate\Support\Facades\Cache;

    $lock = Cache::lock('foo', 10);

    if ($lock->get()) {
        // 10초 동안 락을 획득함...

        $lock->release();
    }

`get` 메서드는 클로저도 받을 수 있습니다. 클로저 실행 후 Laravel이 자동으로 락을 해제합니다:

    Cache::lock('foo')->get(function () {
        // 무기한 락을 얻고 자동 해제됨...
    });

락이 사용 불가할 때 Laravel이 락을 획득할 때까지 지정된 초수만큼 기다리도록 할 수 있습니다. 시간 내 락을 못 얻으면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

    use Illuminate\Contracts\Cache\LockTimeoutException;

    $lock = Cache::lock('foo', 10);

    try {
        $lock->block(5);

        // 최대 5초 기다린 뒤 락을 획득...
    } catch (LockTimeoutException $e) {
        // 락 획득 실패...
    } finally {
        optional($lock)->release();
    }

위 예제는 `block` 메서드에 클로저를 전달해서 더 간단히 쓸 수 있습니다. 클로저 실행 후 락이 자동 해제됩니다:

    Cache::lock('foo', 10)->block(5, function () {
        // 최대 5초 기다린 뒤 락을 획득...
    });

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

가끔 한 프로세스에서 락을 획득하고, 다른 프로세스에서 해제하고 싶을 수 있습니다. 예를 들어 웹 요청 중 락을 얻고, 해당 요청에 의해 트리거된 큐 작업의 끝에서 락을 해제하는 경우입니다. 이때는 락의 "owner token"을 큐 작업으로 전달해, 그 토큰을 사용하여 락을 재생성하고, 해제할 수 있습니다.

아래 예시에서는 락을 성공적으로 획득하면 큐 작업을 디스패치하며, 락의 owner 토큰을 큐 작업에 넘깁니다:

    $podcast = Podcast::find($id);

    $lock = Cache::lock('processing', 120);

    if ($lock->get()) {
        ProcessPodcast::dispatch($podcast, $lock->owner());
    }

애플리케이션의 `ProcessPodcast` 작업에서는 owner 토큰을 사용해 락을 복원하고 해제할 수 있습니다:

    Cache::restoreLock('processing', $this->owner)->release();

현재 owner를 무시하고 락을 강제로 해제하고 싶다면 `forceRelease` 메서드를 사용하세요:

    Cache::lock('processing')->forceRelease();

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가

<a name="writing-the-driver"></a>
### 드라이버 작성하기

커스텀 캐시 드라이버를 만들기 위해서는 먼저 `Illuminate\Contracts\Cache\Store` [계약](/docs/{{version}}/contracts)을 구현해야 합니다. 예를 들어 MongoDB 캐시 구현은 다음과 같을 수 있습니다:

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

각 메서드는 MongoDB 연결을 사용해 구현해야 합니다. 메서드 구현 예는 [Laravel 프레임워크 소스코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고하세요. 구현을 마쳤다면, `Cache` 파사드의 `extend` 메서드로 커스텀 드라이버 등록을 끝마칠 수 있습니다:

    Cache::extend('mongo', function ($app) {
        return Cache::repository(new MongoStore);
    });

> {tip} 커스텀 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 안에 `Extensions` 네임스페이스를 만들어 둘 수 있습니다. 다만, Laravel은 엄격한 어플리케이션 구조가 없으니 원하는 대로 조직할 수 있습니다.

<a name="registering-the-driver"></a>
### 드라이버 등록하기

커스텀 캐시 드라이버를 Laravel에 등록하려면 `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 `boot` 메서드에서 캐시 값을 읽으려 할 수 있으니, 커스텀 드라이버는 `booting` 콜백 내에서 등록하는 것이 좋습니다. 이렇게 하면 모든 서비스 프로바이더의 `register`가 끝난 뒤, `boot` 직전에 드라이버가 등록됩니다. 아래는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `booting` 콜백을 등록하는 예시입니다:

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

`extend` 메서드의 첫 번째 인자는 드라이버 이름이며, 이 이름은 `config/cache.php` 설정 파일의 `driver` 옵션과 일치해야 합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하는 클로저로, `$app` 인스턴스를 인자로 받습니다. `$app`은 [서비스 컨테이너](/docs/{{version}}/container) 인스턴스입니다.

등록이 끝나면, `config/cache.php`의 `driver` 옵션을 본인의 확장 드라이버 이름으로 업데이트해 주세요.

<a name="events"></a>
## 이벤트

모든 캐시 작업 시 코드 실행이 필요하다면, 캐시에서 발생하는 [이벤트](/docs/{{version}}/events)를 리스닝할 수 있습니다. 보통 이런 이벤트 리스너는 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에 정의합니다:

    /**
     * 애플리케이션 내 이벤트 리스너 매핑.
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