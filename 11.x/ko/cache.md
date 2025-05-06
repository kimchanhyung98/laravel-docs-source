# 캐시(Cache)

- [소개](#introduction)
- [구성](#configuration)
    - [드라이버 사전 준비사항](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 아이템 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 아이템 저장하기](#storing-items-in-the-cache)
    - [캐시에서 아이템 삭제하기](#removing-items-from-the-cache)
    - [캐시 헬퍼](#the-cache-helper)
- [원자적 락(Atomic Locks)](#atomic-locks)
    - [락 관리](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
- [커스텀 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

응용 프로그램이 수행하는 일부 데이터 조회 또는 처리 작업은 CPU 사용량이 많거나 몇 초가 걸릴 수 있습니다. 이럴 때, 가져온 데이터를 일정 시간 캐시에 저장해 같은 데이터를 다시 요청했을 때 빠르게 조회할 수 있도록 하는 것이 일반적입니다. 캐시된 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히도, Laravel은 다양한 캐시 백엔드를 위한 표현력 있는 통합 API를 제공하여, 이러한 빠른 데이터 조회 기능을 손쉽게 활용하고 웹 애플리케이션의 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 구성

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서 애플리케이션에서 기본적으로 사용할 캐시 저장소를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스 등 인기 있는 캐싱 백엔드를 기본 지원합니다. 파일 기반 캐시 드라이버도 사용할 수 있으며, `array`와 "null" 캐시 드라이버는 자동화된 테스트를 위한 편리한 캐시 백엔드를 제공합니다.

캐시 설정 파일에는 이 외에도 여러 옵션이 있으니 참고하시기 바랍니다. 기본적으로 Laravel은 직렬화된 캐시 객체를 데이터베이스에 저장하는 `database` 캐시 드라이버를 사용하도록 설정되어 있습니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비사항

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 경우, 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/{{version}}/migrations)에 포함되어 있습니다. 애플리케이션에 이 마이그레이션이 없다면, `make:cache-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)를 설치해야 합니다. `config/cache.php` 설정 파일에 Memcached 서버 목록을 지정할 수 있습니다. 이 파일에는 이미 시작용 예시가 포함되어 있습니다:

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

필요하다면 `host` 옵션에 UNIX 소켓 경로를 지정할 수도 있습니다. 이 경우 `port` 옵션은 `0`으로 설정해야 합니다:

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

<a name="redis"></a>
#### Redis

Laravel에서 Redis 캐시를 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 또는 Composer를 통해 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/{{version}}/sail)에는 이미 해당 확장이 포함되어 있습니다. 또한, [Laravel Forge](https://forge.laravel.com)와 [Laravel Vapor](https://vapor.laravel.com) 같은 공식 Laravel 배포 플랫폼에도 PhpRedis 확장이 기본 설치되어 있습니다.

Redis 설정에 대한 자세한 내용은 [Laravel 공식 문서](/docs/{{version}}/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하려면, 우선 모든 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 이 테이블의 이름은 `cache`로 지정합니다. 그러나 `cache` 설정 파일의 `stores.dynamodb.table` 값에 따라 테이블 이름을 설정해야 하며, `DYNAMODB_CACHE_TABLE` 환경 변수로도 지정할 수 있습니다.

이 테이블에는 문자열 파티션 키가 필요하며, 이름은 애플리케이션의 `cache` 설정 파일 내 `stores.dynamodb.attributes.key` 값과 같아야 합니다. 기본적으로 이 키는 `key`입니다.

일반적으로 DynamoDB는 만료된 항목을 자동으로 제거하지 않으므로, 테이블에 [TTL(Time to Live)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활성화해야 합니다. 이때 TTL 속성 이름을 `expires_at`으로 설정해야 합니다.

다음으로, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치하세요:

```shell
composer require aws/aws-sdk-php
```

또한, DynamoDB 캐시 저장소 설정 옵션에 값이 입력되어 있는지 확인해야 합니다. 일반적으로 `AWS_ACCESS_KEY_ID`와 `AWS_SECRET_ACCESS_KEY` 같은 옵션은 애플리케이션의 `.env` 파일에서 정의해야 합니다:

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

MongoDB를 사용할 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 제공하는 `mongodb` 캐시 드라이버를 제공하며, `mongodb` 데이터베이스 연결을 통해 구성할 수 있습니다. MongoDB는 TTL 인덱스를 지원하므로, 만료된 캐시 항목을 자동으로 삭제할 수 있습니다.

MongoDB 설정에 대한 자세한 사항은 MongoDB [Cache and Locks 공식 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하세요.

<a name="cache-usage"></a>
## 캐시 사용법

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스는 `Cache` 파사드를 통해 얻을 수 있습니다. 이 문서에서도 계속 `Cache` 파사드를 사용합니다. `Cache` 파사드는 Laravel 캐시 컨트랙트의 내부 구현에 간편하게 접근할 수 있도록 해줍니다:

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Support\Facades\Cache;

    class UserController extends Controller
    {
        /**
         * 애플리케이션의 모든 유저 목록을 표시합니다.
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
#### 여러 캐시 저장소 접근하기

`Cache` 파사드의 `store` 메서드를 사용하면, 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드로 전달하는 키는 `cache` 설정 파일의 `stores` 배열에 정의된 저장소 중 하나여야 합니다:

    $value = Cache::store('file')->get('foo');

    Cache::store('redis')->put('bar', 'baz', 600); // 10분

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 아이템 가져오기

`Cache` 파사드의 `get` 메서드를 사용해 캐시에서 아이템을 가져올 수 있습니다. 해당 아이템이 캐시에 없다면 `null`이 반환됩니다. 존재하지 않을 때 반환할 기본값을 두 번째 인자로 전달할 수 있습니다:

    $value = Cache::get('key');

    $value = Cache::get('key', 'default');

기본값을 클로저로도 전달할 수 있습니다. 지정한 아이템이 캐시에 없으면 클로저의 결과가 반환되며, 데이터베이스나 외부 서비스에서 값을 가져오도록 지연시킬 수 있습니다:

    $value = Cache::get('key', function () {
        return DB::table(/* ... */)->get();
    });

<a name="determining-item-existence"></a>
#### 아이템 존재 여부 확인

`has` 메서드는 아이템이 캐시에 존재하는지 검사할 때 사용할 수 있습니다. 이 메서드는 아이템이 존재하지만 값이 `null`일 경우에도 `false`를 반환합니다:

    if (Cache::has('key')) {
        // ...
    }

<a name="incrementing-decrementing-values"></a>
#### 값 증가 / 감소

정수값을 가진 캐시 아이템의 값을 조정하려면 `increment`와 `decrement` 메서드를 사용할 수 있습니다. 두 메서드 모두 증가 또는 감소할 값(옵션)을 두 번째 인자로 받습니다:

    // 값이 없다면 먼저 초기화...
    Cache::add('key', 0, now()->addHours(4));

    // 값 증가 또는 감소...
    Cache::increment('key');
    Cache::increment('key', $amount);
    Cache::decrement('key');
    Cache::decrement('key', $amount);

<a name="retrieve-store"></a>
#### 조회 및 저장

캐시에서 데이터를 조회하되, 만약 없으면 기본값을 저장하고자 할 때가 있습니다. 예를 들어, 모든 유저 데이터를 우선 캐시에서 가져오고, 없으면 데이터베이스에서 조회 후 캐시에 저장하고 싶을 수 있습니다. 이럴 때 `Cache::remember` 메서드를 사용하면 됩니다:

    $value = Cache::remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

캐시에 아이템이 없으면, 전달한 클로저가 실행되고 그 반환값이 캐시에 저장됩니다.

`rememberForever` 메서드를 사용하면 아이템이 없을 경우 데이터를 영구적으로 저장하도록 할 수 있습니다:

    $value = Cache::rememberForever('users', function () {
        return DB::table('users')->get();
    });

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember` 메서드를 사용할 때, 일부 사용자에게는 캐시가 만료된 경우 느린 응답이 발생할 수 있습니다. 특정 데이터의 경우, 캐시된 값이 백그라운드에서 재계산되는 동안 일부 사용자는 "오래된" 데이터를 받아 즉각적인 응답을 받을 수 있도록 하는 것이 좋습니다. 이런 패턴을 "stale-while-revalidate"라고 하며, `Cache::flexible` 메서드가 이를 구현합니다.

flexible 메서드는 캐시 값이 “신선한” 기간과 “오래된” 기간을 배열로 지정받습니다. 배열의 첫 번째 값은 캐시가 신선한 상태로 간주되는 초 단위 기간이고, 두 번째 값은 신선한 기간이 끝난 뒤 최대 몇 초까지 오래된 데이터를 제공할지 의미합니다.

신선한 기간(첫 번째 값 이내)에 요청이 오면 즉시 캐시를 반환합니다. 오래된 기간(첫 번째 값과 두 번째 값 사이)에는, 사용자는 기존 캐시 값을 받고, [지연 함수](/docs/{{version}}/helpers#deferred-functions)가 등록되어 응답 이후 캐시 값이 새로 갱신됩니다. 두 번째 값을 초과한 경우, 캐시가 만료된 것으로 간주되어 즉시 재계산되므로 응답이 느려질 수 있습니다:

    $value = Cache::flexible('users', [5, 10], function () {
        return DB::table('users')->get();
    });

<a name="retrieve-delete"></a>
#### 조회 및 삭제

캐시에서 아이템을 조회한 후 바로 삭제해야 하는 경우, `pull` 메서드를 사용할 수 있습니다. 아이템이 없으면 `get`과 마찬가지로 `null`이 반환됩니다:

    $value = Cache::pull('key');

    $value = Cache::pull('key', 'default');

<a name="storing-items-in-the-cache"></a>
### 캐시에 아이템 저장하기

캐시에 아이템을 저장하려면 `Cache` 파사드의 `put` 메서드를 사용할 수 있습니다:

    Cache::put('key', 'value', $seconds = 10);

저장 기간을 생략하면, 아이템은 무기한 저장됩니다:

    Cache::put('key', 'value');

만료 시간을 나타내는 정수 대신 `DateTime` 인스턴스를 사용할 수 있습니다:

    Cache::put('key', 'value', now()->addMinutes(10));

<a name="store-if-not-present"></a>
#### 없을 때만 저장

`add` 메서드는 아이템이 캐시에 존재하지 않을 때만 저장합니다. 실제로 저장되면 true를 반환하고, 이미 존재한다면 false를 반환합니다. `add`는 원자적(atomic) 연산입니다:

    Cache::add('key', 'value', $seconds);

<a name="storing-items-forever"></a>
#### 영구 저장

`forever` 메서드로 아이템을 캐시에 영구적으로 저장할 수 있습니다. 이러한 아이템은 만료되지 않으므로, `forget` 메서드로 삭제해야 합니다:

    Cache::forever('key', 'value');

> [!NOTE]  
> Memcached 드라이버를 사용할 때, "영구 저장"된 아이템도 캐시 용량이 가득 찼을 때는 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 아이템 삭제하기

아이템을 삭제하려면 `forget` 메서드를 사용할 수 있습니다:

    Cache::forget('key');

또는, 만료 시간을 0 또는 음수로 지정해도 삭제됩니다:

    Cache::put('key', 'value', 0);

    Cache::put('key', 'value', -5);

전체 캐시를 비우려면 `flush` 메서드를 사용하세요:

    Cache::flush();

> [!WARNING]  
> 전체 캐시 비우기는 설정한 캐시 "prefix"를 무시하고 모든 엔트리를 제거합니다. 여러 애플리케이션이 캐시를 공유할 경우 신중하게 사용해야 합니다.

<a name="the-cache-helper"></a>
### 캐시 헬퍼

`Cache` 파사드 대신 전역 `cache` 함수를 이용해 데이터를 조회하고 저장할 수 있습니다. 문자열 하나를 전달하면 해당 키의 값을 바로 반환합니다:

    $value = cache('key');

키/값 쌍의 배열과 만료 시간을 함께 전달하면 지정한 기간 동안 값을 저장합니다:

    cache(['key' => 'value'], $seconds);

    cache(['key' => 'value'], now()->addMinutes(10));

인자가 없이 `cache` 함수를 호출하면, `Illuminate\Contracts\Cache\Factory` 인스턴스를 반환합니다. 이를 통해 다른 캐싱 메서드도 호출할 수 있습니다:

    cache()->remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

> [!NOTE]  
> 전역 `cache` 함수 테스트시에도, 파사드 [모킹](/docs/{{version}}/mocking#mocking-facades)과 동일하게 `Cache::shouldReceive`를 사용할 수 있습니다.

<a name="atomic-locks"></a>
## 원자적 락(Atomic Locks)

> [!WARNING]  
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 설정해야 하며, 모든 서버가 같은 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리

원자적 락은 레이스 컨디션에 대해 걱정하지 않고 분산 락을 조작할 수 있게 해줍니다. 예를 들어, [Laravel Forge](https://forge.laravel.com)는 한 번에 한 개의 원격 작업만 실행되도록 원자적 락을 사용합니다. 락을 생성 및 관리하려면 `Cache::lock` 메서드를 사용하세요:

    use Illuminate\Support\Facades\Cache;

    $lock = Cache::lock('foo', 10);

    if ($lock->get()) {
        // 10초짜리 락 획득...

        $lock->release();
    }

`get` 메서드는 클로저도 인자로 받을 수 있습니다. 클로저 실행 후 Laravel이 자동으로 락을 해제합니다:

    Cache::lock('foo', 10)->get(function () {
        // 10초 락 획득 및 자동 해제...
    });

락이 사용 중이라서 즉시 획득할 수 없는 경우, Laravel에게 일정 시간(초) 동안 대기하도록 지시할 수 있습니다. 이 시간 내에 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다:

    use Illuminate\Contracts\Cache\LockTimeoutException;

    $lock = Cache::lock('foo', 10);

    try {
        $lock->block(5);

        // 최대 5초 대기 후 락 획득...
    } catch (LockTimeoutException $e) {
        // 락 획득 실패...
    } finally {
        $lock->release();
    }

위 코드는 `block` 메서드에 클로저를 전달하여 더 간단하게 쓸 수 있습니다. 이 경우, 지정한 시간 안에 락을 획득하면 클로저가 실행되고 자동으로 락이 해제됩니다:

    Cache::lock('foo', 10)->block(5, function () {
        // 최대 5초 대기 후 락 획득...
    });

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

간혹 한 프로세스에서 락을 획득하고, 다른 프로세스에서 락을 해제하고 싶을 수 있습니다. 예를 들어, 웹 요청 처리 중 락을 획득한 뒤, 해당 요청이 트리거하는 큐 작업의 마지막에 락을 해제할 수 있습니다. 이 경우 락의 범위 지정 "owner token"을 큐 작업에 전달하고, 이 토큰으로 락을 재생성하여 해제해야 합니다.

아래 예시에서는 락을 성공적으로 획득하면 큐 작업을 dispatch 합니다. 또한 락의 owner token을 해당 작업에 전달합니다:

    $podcast = Podcast::find($id);

    $lock = Cache::lock('processing', 120);

    if ($lock->get()) {
        ProcessPodcast::dispatch($podcast, $lock->owner());
    }

`ProcessPodcast` 큐 작업 내에서는, owner 토큰으로 락을 복원 및 해제할 수 있습니다:

    Cache::restoreLock('processing', $this->owner)->release();

owner 무관하게 강제로 락을 해제하고 싶다면, `forceRelease` 메서드를 사용할 수 있습니다:

    Cache::lock('processing')->forceRelease();

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가하기

<a name="writing-the-driver"></a>
### 드라이버 작성하기

커스텀 캐시 드라이버를 만들려면 `Illuminate\Contracts\Cache\Store` [컨트랙트](/docs/{{version}}/contracts)를 구현해야 합니다. 예를 들어 MongoDB 캐시 드라이버 구현은 다음과 같이 작성할 수 있습니다:

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

각 메서드는 MongoDB 연결을 사용하여 구현하면 됩니다. 구현 예시로는 [Laravel 소스코드의 `Illuminate\Cache\MemcachedStore`](https://github.com/laravel/framework)를 참고하세요. 구현이 모두 끝나면, `Cache` 파사드의 `extend` 메서드로 커스텀 드라이버 등록을 완료할 수 있습니다:

    Cache::extend('mongo', function (Application $app) {
        return Cache::repository(new MongoStore);
    });

> [!NOTE]  
> 커스텀 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 내에 `Extensions` 네임스페이스를 만들어 넣을 수 있습니다. 다만, Laravel은 프로젝트 구조가 고정되어 있지 않으므로 원하는 대로 구조를 설계할 수 있습니다.

<a name="registering-the-driver"></a>
### 드라이버 등록하기

Laravel에 커스텀 캐시 드라이버를 등록하려면 `Cache` 파사드의 `extend` 메서드를 사용합니다. 또, 일부 서비스 프로바이더의 `boot` 메서드에서 캐시 값을 읽으므로, 등록은 `booting` 콜백 안에서 해야 합니다. 이 콜백을 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 안에 추가하면, 모든 서비스 프로바이더의 `register` 메서드 호출 이후, `boot` 메서드가 호출되기 직전에 커스텀 드라이버가 등록됩니다:

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

`extend` 메서드에 전달하는 첫 번째 인자는 드라이버의 이름입니다. 이는 `config/cache.php` 파일의 `driver` 옵션과 일치해야 합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저이며, 이 클로저는 [서비스 컨테이너](/docs/{{version}}/container) 인스턴스 `$app`을 전달받습니다.

확장 기능 등록이 완료되면, 애플리케이션 설정 파일 `config/cache.php`의 `CACHE_STORE` 환경 변수 또는 `default` 옵션을 해당 이름으로 변경해야 합니다.

<a name="events"></a>
## 이벤트

모든 캐시 동작마다 코드를 실행하고 싶다면, 캐시에서 디스패치되는 다양한 [이벤트](/docs/{{version}}/events)를 리스닝할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름 |
| --- |
| `Illuminate\Cache\Events\CacheHit` |
| `Illuminate\Cache\Events\CacheMissed` |
| `Illuminate\Cache\Events\KeyForgotten` |
| `Illuminate\Cache\Events\KeyWritten` |

</div>

성능 향상을 위해, `config/cache.php` 설정 파일에서 특정 캐시 저장소의 `events` 설정 옵션에 `false`를 지정하여 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```