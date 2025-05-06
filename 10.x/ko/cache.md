# 캐시(Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 필수 조건](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 아이템 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 아이템 저장하기](#storing-items-in-the-cache)
    - [캐시에서 아이템 제거하기](#removing-items-from-the-cache)
    - [캐시 헬퍼](#the-cache-helper)
- [원자적 락(Atomic Locks)](#atomic-locks)
    - [드라이버 필수 조건](#lock-driver-prerequisites)
    - [락 관리하기](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가](#adding-custom-cache-drivers)
    - [드라이버 작성](#writing-the-driver)
    - [드라이버 등록](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

애플리케이션에서 데이터 검색이나 처리 작업 중 일부는 CPU 사용량이 높거나 완료하는 데 수 초가 소요될 수 있습니다. 이런 경우 동일한 데이터에 대한 반복 요청 시 빠르게 응답하기 위해 데이터를 일정 시간 캐싱하는 것이 일반적입니다. 캐시된 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히도, Laravel은 다양한 캐시 백엔드에 대해 표현력 있고 통합된 API를 제공하여 초고속 데이터 검색의 이점을 쉽게 누릴 수 있도록 해줍니다. 이를 통해 웹 애플리케이션의 속도를 크게 향상시킬 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치해 있습니다. 이 파일에서 애플리케이션 전반에서 기본적으로 사용할 캐시 드라이버를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스 등 인기 있는 캐싱 백엔드를 기본 지원합니다. 또한 파일 기반 캐시 드라이버와, 자동화 테스트에 용이한 `array` 및 "null" 드라이버도 제공합니다.

캐시 설정 파일에는 이외에도 다양한 옵션이 포함되어 있으므로, 파일 내의 문서를 꼼꼼히 확인하세요. 기본적으로 Laravel은 서버 파일 시스템에 직렬화된 캐시 객체를 저장하는 `file` 캐시 드라이버를 사용하도록 설정돼 있습니다. 규모가 큰 애플리케이션의 경우 Memcached나 Redis와 같은 더 강력한 드라이버를 사용하는 것이 좋습니다. 동일한 드라이버에 대해 여러 개의 캐시 구성을 지정할 수도 있습니다.

<a name="driver-prerequisites"></a>
### 드라이버 필수 조건

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 때는 캐시 아이템을 저장할 테이블을 생성해야 합니다. 아래는 해당 테이블의 `Schema` 선언 예시입니다.

    Schema::create('cache', function (Blueprint $table) {
        $table->string('key')->unique();
        $table->text('value');
        $table->integer('expiration');
    });

> [!NOTE]  
> `php artisan cache:table` 아티즌 명령어를 사용하면, 적절한 스키마가 포함된 마이그레이션을 생성할 수 있습니다.

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. 모든 Memcached 서버는 `config/cache.php` 파일에서 설정할 수 있습니다. 기본적으로 이 파일에는 `memcached.servers` 항목이 포함되어 있습니다.

    'memcached' => [
        'servers' => [
            [
                'host' => env('MEMCACHED_HOST', '127.0.0.1'),
                'port' => env('MEMCACHED_PORT', 11211),
                'weight' => 100,
            ],
        ],
    ],

필요하다면 `host` 옵션에 UNIX 소켓 경로를 지정할 수도 있습니다. 이 경우 `port` 옵션은 `0`으로 설정해야 합니다.

    'memcached' => [
        [
            'host' => '/var/run/memcached/memcached.sock',
            'port' => 0,
            'weight' => 100
        ],
    ],

<a name="redis"></a>
#### Redis

Laravel에서 Redis 캐시를 사용하려면, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나, Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. [Laravel Sail](/docs/{{version}}/sail)에는 이 확장 모듈이 이미 포함되어 있습니다. 또한 [Laravel Forge](https://forge.laravel.com)나 [Laravel Vapor](https://vapor.laravel.com) 등 공식 배포 플랫폼에도 기본적으로 PhpRedis가 설치되어 있습니다.

Redis 설정에 대한 자세한 정보는 [Laravel 문서 Redis 페이지](/docs/{{version}}/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하려면, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 먼저 생성해야 합니다. 일반적으로 테이블 이름은 `cache`여야 하지만, 애플리케이션의 `cache` 설정 파일 내 `stores.dynamodb.table` 설정값에 따라 결정됩니다.

이 테이블에는 또한 파티션 키로 사용할 문자열 컬럼이 필요하며, 해당 키의 이름은 `stores.dynamodb.attributes.key` 설정값과 일치해야 합니다. 기본적으로 파티션 키의 이름은 `key`입니다.

<a name="cache-usage"></a>
## 캐시 사용법

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻기 위해 이 문서 전반에서 사용할 `Cache` 파사드를 이용할 수 있습니다. `Cache` 파사드는 Laravel 캐시 컨트랙트의 하위 구현에 간편하고 간결하게 접근할 수 있도록 도와줍니다.

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

<a name="accessing-multiple-cache-stores"></a>
#### 여러 캐시 저장소 접근

`Cache` 파사드를 사용하면 `store` 메서드를 통해 다양한 캐시 저장소를 접근할 수 있습니다. `store` 메서드에 전달되는 키 값은 `cache` 설정 파일의 `stores` 배열에 정의된 저장소 중 하나와 일치해야 합니다.

    $value = Cache::store('file')->get('foo');

    Cache::store('redis')->put('bar', 'baz', 600); // 10분

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 아이템 가져오기

`Cache` 파사드의 `get` 메서드는 캐시에서 아이템을 가져오는 데 사용됩니다. 만약 해당 아이템이 캐시에 없으면, `null`이 반환됩니다. 원하는 경우, 두 번째 인수로 아이템이 없을 때 반환할 기본값을 지정할 수 있습니다.

    $value = Cache::get('key');

    $value = Cache::get('key', 'default');

기본값으로 클로저를 전달할 수도 있습니다. 지정된 아이템이 캐시에 없을 경우, 클로저의 반환값이 대신 반환됩니다. 클로저를 이용하면 데이터베이스나 외부 서비스에서 기본값을 가져오는 동작을 지연시킬 수 있습니다.

    $value = Cache::get('key', function () {
        return DB::table(/* ... */)->get();
    });

<a name="determining-item-existence"></a>
#### 아이템 존재 여부 확인

`has` 메서드를 사용하면 캐시에 아이템이 존재하는지 확인할 수 있습니다. 이 메서드는 아이템이 존재하지만 값이 `null`인 경우에도 `false`를 반환합니다.

    if (Cache::has('key')) {
        // ...
    }

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소

`increment`와 `decrement` 메서드를 사용하여, 캐시에 저장된 정수 아이템의 값을 조정할 수 있습니다. 두 메서드 모두 두 번째 인수로 증가 또는 감소시킬 값을 지정할 수 있습니다.

    // 값이 없으면 초기화...
    Cache::add('key', 0, now()->addHours(4));

    // 값 증가 또는 감소...
    Cache::increment('key');
    Cache::increment('key', $amount);
    Cache::decrement('key');
    Cache::decrement('key', $amount);

<a name="retrieve-store"></a>
#### 가져오면서 저장(Retrieve and Store)

때로는 캐시에서 아이템을 가져오고, 없으면 기본 값을 저장하고 싶을 수 있습니다. 예를 들어, 모든 사용자를 캐시에서 가져오거나, 없다면 데이터베이스에서 조회해서 캐시에 저장하고 싶을 때가 있습니다. `Cache::remember` 메서드를 이용하면 쉽게 구현할 수 있습니다.

    $value = Cache::remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

아이템이 캐시에 없으면, `remember`에 전달한 클로저가 실행되고, 그 결과가 캐시에 저장됩니다.

`rememberForever` 메서드를 사용하면 아이템을 영구적으로 저장할 수 있습니다.

    $value = Cache::rememberForever('users', function () {
        return DB::table('users')->get();
    });

<a name="retrieve-delete"></a>
#### 가져오고 삭제(Retrieve and Delete)

캐시에서 아이템을 가져온 뒤 즉시 삭제하고 싶다면, `pull` 메서드를 사용할 수 있습니다. 아이템이 존재하지 않으면 `null`이 반환됩니다.

    $value = Cache::pull('key');

<a name="storing-items-in-the-cache"></a>
### 캐시에 아이템 저장하기

`Cache` 파사드의 `put` 메서드를 사용해 캐시에 아이템을 저장할 수 있습니다.

    Cache::put('key', 'value', $seconds = 10);

저장 시간을 전달하지 않으면 아이템은 무기한 저장됩니다.

    Cache::put('key', 'value');

초 단위 대신, 캐시 만료 시점을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다.

    Cache::put('key', 'value', now()->addMinutes(10));

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장

`add` 메서드는 아이템이 현재 캐시에 없을 때만 저장합니다. 실제로 추가되면 `true`, 이미 존재하면 `false`를 반환합니다. 이 메서드는 원자적(atomic)으로 동작합니다.

    Cache::add('key', 'value', $seconds);

<a name="storing-items-forever"></a>
#### 무기한 저장

`forever` 메서드를 사용하면 아이템을 만료없이 영구 저장할 수 있습니다. 이런 아이템은 반드시 `forget` 메서드로 직접 삭제해야 합니다.

    Cache::forever('key', 'value');

> [!NOTE]  
> Memcached 드라이버를 사용할 경우, "영구"로 저장된 아이템도 캐시의 용량 제한에 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 아이템 제거하기

`forget` 메서드를 사용해 캐시에서 아이템을 제거할 수 있습니다.

    Cache::forget('key');

만료 시간을 0 또는 음수로 지정해도 캐시에서 아이템이 제거됩니다.

    Cache::put('key', 'value', 0);

    Cache::put('key', 'value', -5);

전체 캐시를 비우려면 `flush` 메서드를 사용하면 됩니다.

    Cache::flush();

> [!WARNING]  
> 캐시 전체 삭제는 설정한 "접두사(prefix)"와 무관하게 모든 캐시를 제거합니다. 여러 애플리케이션에서 캐시를 공유하는 경우, 신중히 고려하고 실행하세요.

<a name="the-cache-helper"></a>
### 캐시 헬퍼

`Cache` 파사드뿐만 아니라, 전역 `cache` 함수를 사용해 데이터를 가져오거나 저장할 수 있습니다. 문자열 하나만 전달하면 해당 키의 값을 반환합니다.

    $value = cache('key');

키/값 쌍의 배열과 만료 시간을 전달하면, 지정한 기간 동안 캐시에 저장됩니다.

    cache(['key' => 'value'], $seconds);

    cache(['key' => 'value'], now()->addMinutes(10));

인수가 없으면 `Illuminate\Contracts\Cache\Factory` 인스턴스를 반환하므로, 다른 캐시 관련 메서드도 호출할 수 있습니다.

    cache()->remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

> [!NOTE]  
> 전역 `cache` 함수를 테스트할 때도 [파사드 테스트](/docs/{{version}}/mocking#mocking-facades)에서와 같이 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="atomic-locks"></a>
## 원자적 락(Atomic Locks)

> [!WARNING]  
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 반드시 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나여야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="lock-driver-prerequisites"></a>
### 드라이버 필수 조건

<a name="atomic-locks-prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버에서 애플리케이션의 캐시 락을 저장할 테이블을 설정해야 합니다. 아래는 해당 테이블의 `Schema` 선언 예시입니다.

    Schema::create('cache_locks', function (Blueprint $table) {
        $table->string('key')->primary();
        $table->string('owner');
        $table->integer('expiration');
    });

> [!NOTE]  
> 만약 `cache:table` 아티즌 명령어로 드라이버의 캐시 테이블을 생성했다면, 이 명령으로 생성된 마이그레이션에 `cache_locks` 테이블 정의도 포함되어 있습니다.

<a name="managing-locks"></a>
### 락 관리하기

원자적 락을 사용하면 경쟁 상태(race condition) 걱정 없이 분산 락을 조작할 수 있습니다. 예를 들어, [Laravel Forge](https://forge.laravel.com)에서는 단 한 번에 하나의 원격 작업만 서버에서 실행하도록 원자적 락을 사용합니다. 락을 생성 및 관리하려면 `Cache::lock` 메서드를 사용하세요.

    use Illuminate\Support\Facades\Cache;

    $lock = Cache::lock('foo', 10);

    if ($lock->get()) {
        // 락이 10초 동안 획득됨...

        $lock->release();
    }

`get` 메서드는 클로저를 인수로 받을 수도 있습니다. 클로저 실행 후 Laravel이 자동으로 락을 해제합니다.

    Cache::lock('foo', 10)->get(function () {
        // 락이 10초 동안 획득되고, 자동으로 해제됨...
    });

요청 시점에 락이 사용 불가능하다면, Laravel이 지정된 시간(초)만큼 대기하도록 할 수 있습니다. 지정 시간 내에 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다.

    use Illuminate\Contracts\Cache\LockTimeoutException;

    $lock = Cache::lock('foo', 10);

    try {
        $lock->block(5);

        // 최대 5초 동안 대기 후 락 획득...
    } catch (LockTimeoutException $e) {
        // 락 획득 실패...
    } finally {
        $lock?->release();
    }

위 예시는 `block` 메서드에 클로저를 전달해 더 간단하게 표현할 수 있습니다. 이 경우 Laravel이 지정한 시간만큼 락을 대기 후 획득한 뒤, 클로저 실행 후 락을 자동 해제합니다.

    Cache::lock('foo', 10)->block(5, function () {
        // 최대 5초 대기 후 락 획득...
    });

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

때로는 한 프로세스에서 락을 획득하고, 다른 프로세스(예: 큐 작업)에서 해제하고 싶을 수 있습니다. 예를 들어, 웹 요청 중에 락을 획득한 뒤, 그 요청으로 트리거된 큐 작업 마지막에 락을 해제할 수 있습니다. 이런 경우 락의 범위(owner 토큰)를 큐 작업에 전달해, 해당 토큰을 이용해 락을 재생성해야 합니다.

아래 예시에서는 락 획득에 성공하면 큐 작업을 Dispatch하고, 락 소유자 토큰을 함께 전달합니다.

    $podcast = Podcast::find($id);

    $lock = Cache::lock('processing', 120);

    if ($lock->get()) {
        ProcessPodcast::dispatch($podcast, $lock->owner());
    }

큐 작업 내에서는 전달받은 owner 토큰으로 락을 복원하고 해제할 수 있습니다.

    Cache::restoreLock('processing', $this->owner)->release();

현재 소유자와 무관하게 락을 해제해야 한다면, `forceRelease` 메서드를 사용할 수 있습니다.

    Cache::lock('processing')->forceRelease();

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가

<a name="writing-the-driver"></a>
### 드라이버 작성

커스텀 캐시 드라이버를 만들려면 `Illuminate\Contracts\Cache\Store` [컨트랙트](/docs/{{version}}/contracts)를 구현해야 합니다. 예를 들어, MongoDB 캐시 구현은 다음과 같을 수 있습니다.

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

이 메서드 각각을 MongoDB 접속을 통해 구현하면 됩니다. 각 메서드의 실제 구현 예시는 [Laravel 프레임워크 소스코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고하세요. 구현이 끝나면 `Cache` 파사드의 `extend` 메서드를 호출해 커스텀 드라이버 등록을 마칠 수 있습니다.

    Cache::extend('mongo', function (Application $app) {
        return Cache::repository(new MongoStore);
    });

> [!NOTE]  
> 커스텀 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 아래에 `Extensions` 네임스페이스를 만드는 것이 한 예시입니다. 하지만 Laravel은 엄격한 구조를 강제하지 않으므로, 자신의 성향에 따라 자유롭게 구성할 수 있습니다.

<a name="registering-the-driver"></a>
### 드라이버 등록

커스텀 캐시 드라이버를 Laravel에 등록하려면 `Cache` 파사드에서 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더에서 `boot` 메서드 내에서 캐시 값을 읽을 수 있으므로, 커스텀 드라이버 등록은 `booting` 콜백에서 이루어져야 합니다. 이렇게 하면 모든 서비스 프로바이더의 `register` 메서드 실행 후, `boot` 메서드가 실행되기 직전에 드라이버가 등록됩니다. 이 콜백은 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에서 등록하세요.

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

`extend` 메서드의 첫 번째 인수는 드라이버의 이름이며, 이것이 `config/cache.php` 설정 파일의 `driver` 옵션과 일치하게 됩니다. 두 번째 인수는 반드시 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저여야 하며, 이 클로저에는 `$app`(서비스 컨테이너 인스턴스)이 전달됩니다.

확장 기능 등록이 끝나면, `config/cache.php` 알맞은 설정의 `driver` 옵션 값을 새 확장 이름으로 변경하세요.

<a name="events"></a>
## 이벤트

캐시 동작마다 코드를 실행하고 싶다면, 캐시가 발생시키는 [이벤트](/docs/{{version}}/events)를 수신할 수 있습니다. 일반적으로 이런 이벤트 리스너는 애플리케이션의 `App\Providers\EventServiceProvider` 클래스 내에 정의하는 것이 좋습니다.
    
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
