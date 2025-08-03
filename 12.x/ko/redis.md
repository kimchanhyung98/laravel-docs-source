# Redis

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Redis와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [명령어 파이프라이닝](#pipelining-commands)
- [발행 / 구독(pub / sub)](#pubsub)

<a name="introduction"></a>
## 소개 (Introduction)

[Redis](https://redis.io)는 오픈 소스 고급 키-값 저장소입니다. Redis는 키에 [문자열](https://redis.io/docs/data-types/strings/), [해시](https://redis.io/docs/data-types/hashes/), [리스트](https://redis.io/docs/data-types/lists/), [셋](https://redis.io/docs/data-types/sets/), [정렬된 셋](https://redis.io/docs/data-types/sorted-sets/)과 같은 다양한 자료구조를 담을 수 있어서 보통 데이터 구조 서버(data structure server)라고도 불립니다.

Laravel에서 Redis를 사용하기 전에, PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 패키지를 설치해 사용하는 것을 권장합니다. 이 확장은 "유저랜드" PHP 패키지보다 설치가 복잡하지만, Redis를 많이 사용하는 애플리케이션에서 성능 향상을 가져올 수 있습니다. 만약 [Laravel Sail](/docs/12.x/sail)을 사용 중이라면, 이 확장이 애플리케이션 Docker 컨테이너에 이미 설치되어 있습니다.

PhpRedis 확장 설치가 어렵다면, Composer로 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 순수 PHP로 작성된 Redis 클라이언트로 별도의 확장 설치가 필요 없습니다:

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일 내 `redis` 배열에서 정의할 수 있습니다. 이 배열에는 애플리케이션이 사용하는 Redis 서버 정보가 들어 있습니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],

    'default' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'username' => env('REDIS_USERNAME'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_DB', '0'),
    ],

    'cache' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'username' => env('REDIS_USERNAME'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_CACHE_DB', '1'),
    ],

],
```

구성 파일에서 정의하는 각 Redis 서버는 이름, 호스트, 포트를 반드시 지정해야 합니다. 단일 URL로 Redis 연결 정보를 표현할 경우 이 제한이 적용되지 않습니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],

    'default' => [
        'url' => 'tcp://127.0.0.1:6379?database=0',
    ],

    'cache' => [
        'url' => 'tls://user:password@127.0.0.1:6380?database=1',
    ],

],
```

<a name="configuring-the-connection-scheme"></a>
#### 연결 스킴 구성하기

기본적으로 Redis 클라이언트는 Redis 서버에 접속할 때 `tcp` 스킴을 사용하지만, `scheme` 구성 옵션을 설정하면 TLS / SSL 암호화를 활성화할 수 있습니다. 다음은 TLS 연결 예시입니다:

```php
'default' => [
    'scheme' => 'tls',
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
],
```

<a name="clusters"></a>
### 클러스터 (Clusters)

Redis 서버 클러스터를 사용하는 경우, `config/database.php` 설정 파일 내 `redis` 배열에 `clusters` 키를 추가해 클러스터를 정의해야 합니다. 기본 설정에는 없으므로 직접 추가해야 합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],

    'clusters' => [
        'default' => [
            [
                'url' => env('REDIS_URL'),
                'host' => env('REDIS_HOST', '127.0.0.1'),
                'username' => env('REDIS_USERNAME'),
                'password' => env('REDIS_PASSWORD'),
                'port' => env('REDIS_PORT', '6379'),
                'database' => env('REDIS_DB', '0'),
            ],
        ],
    ],

    // ...
],
```

기본적으로 Laravel은 `options.cluster` 값이 `redis`로 설정된 경우 네이티브 Redis 클러스터링을 사용하며, 이 방식은 장애 조치(failover)를 부드럽게 처리합니다.

Predis를 사용할 경우, Laravel은 클라이언트 측 샤딩(client-side sharding)을 지원하지만 이 방식은 장애 조치를 지원하지 않아 주로 다른 기본 데이터 저장소에 접근 가능한 임시 캐시 데이터 용도로 적합합니다.

클라이언트 측 샤딩을 사용하고 싶다면 `config/database.php` 설정 파일에서 `options.cluster` 값을 제거하세요:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'clusters' => [
        // ...
    ],

    // ...
],
```

<a name="predis"></a>
### Predis

Predis 패키지를 통해 Redis와 상호작용하려면, `REDIS_CLIENT` 환경 변수 값을 `predis`로 설정해야 합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 설정 옵션 외에도 Predis는 [추가 연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이 옵션들을 각 Redis 서버 구성에 추가하려면 `config/database.php` 파일 내 Redis 서버 설정에 다음과 같이 포함하세요:

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'read_write_timeout' => 60,
],
```

<a name="phpredis"></a>
### PhpRedis

기본적으로 Laravel은 PhpRedis 확장으로 Redis와 통신합니다. 사용할 클라이언트는 `redis.client` 설정 옵션 값에 의해 결정되고, 이는 보통 `REDIS_CLIENT` 환경 변수 값을 반영합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

PhpRedis는 기본 연결 옵션 외에도 다음 추가 연결 파라미터를 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context`. 이러한 옵션들은 `config/database.php` 내 Redis 서버 구성에 추가할 수 있습니다:

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'read_timeout' => 60,
    'context' => [
        // 'auth' => ['username', 'secret'],
        // 'stream' => ['verify_peer' => false],
    ],
],
```

<a name="unix-socket-connections"></a>
#### 유닉스 소켓 연결

Redis 연결은 TCP 대신 유닉스 소켓을 사용하도록 구성할 수 있습니다. 애플리케이션 서버와 동일 서버에서 Redis 인스턴스에 접속할 때 TCP 오버헤드를 줄여 성능 향상을 기대할 수 있습니다. 유닉스 소켓을 사용하려면 환경 변수 `REDIS_HOST`를 Redis 소켓 경로로 설정하고 `REDIS_PORT`를 `0`으로 설정하세요:

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

PhpRedis 확장은 다양한 직렬화(serializer) 방식과 압축(compression) 알고리즘을 사용할 수 있도록 설정할 수 있습니다. 이 옵션들은 Redis 설정 내 `options` 배열에 구성합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
        'serializer' => Redis::SERIALIZER_MSGPACK,
        'compression' => Redis::COMPRESSION_LZ4,
    ],

    // ...
],
```

현재 지원하는 직렬화 방식은 `Redis::SERIALIZER_NONE`(기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK` 입니다.

지원하는 압축 알고리즘은 `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4` 입니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

`Redis` [파사드](/docs/12.x/facades)를 통해 다양한 Redis 명령어를 호출하며 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하여, Redis의 모든 [명령어](https://redis.io/commands)를 메서드 호출로 전달할 수 있습니다. 다음 예시에서는 `GET` 명령어를 `Redis` 파사드의 `get` 메서드로 호출합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Redis;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 보여줍니다.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => Redis::get('user:profile:'.$id)
        ]);
    }
}
```

위와 같이 Redis 명령어라면 어떤 것이든 `Redis` 파사드에서 호출할 수 있습니다. Laravel이 마법 메서드를 사용해 해당 명령을 Redis 서버로 전달해 줍니다. 명령어가 인수를 필요로 한다면, 메서드 인자로 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는, `Redis` 파사드의 `command` 메서드를 통해 명령어명과 인수를 배열로 전달할 수도 있습니다:

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

`config/database.php` 설정 파일에서 여러 Redis 연결/서버를 정의할 수 있습니다. 특정 Redis 연결을 얻으려면 `Redis` 파사드의 `connection` 메서드를 사용하세요:

```php
$redis = Redis::connection('connection-name');
```

기본 연결을 얻으려면 인자를 전달하지 않고 호출할 수 있습니다:

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` 파사드의 `transaction` 메서드는 Redis의 기본 `MULTI`, `EXEC` 명령어를 감싸는 편리한 래퍼입니다. `transaction` 메서드는 클로저를 인자로 받고, 이 클로저에는 Redis 연결 인스턴스가 주어집니다. 클로저 내에서 실행된 모든 Redis 명령어는 하나의 원자적(atomic) 트랜잭션으로 처리됩니다:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션 정의 시 Redis 연결로부터 값을 반환받을 수 없습니다. 트랜잭션은 클로저 내 모든 명령어 실행이 완료된 후 단일 원자적 작업으로 실행되기 때문입니다.

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령어를 단일 원자 작업으로 실행할 또 다른 방법입니다. `eval`의 장점은 Redis 키 값을 작업 중에 직접 조작하고 확인할 수 있다는 점입니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 인자를 여러 개 받습니다. 첫 번째 인자로 Lua 스크립트를 문자열로 전달하고, 두 번째 인자로 스크립트가 조작하는 키 개수(정수)를 전달합니다. 이후 키 이름과 필요 시 추가 인자들을 전달합니다.

다음 예시는 카운터를 증가시키고, 첫 번째 카운터 값이 5 초과일 때 두 번째 카운터를 증가시킨 후 첫 번째 카운터 값을 반환합니다:

```php
$value = Redis::eval(<<<'LUA'
    local counter = redis.call("incr", KEYS[1])

    if counter > 5 then
        redis.call("incr", KEYS[2])
    end

    return counter
LUA, 2, 'first-counter', 'second-counter');
```

> [!WARNING]
> Redis 스크립팅에 대해서는 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 명령어 파이프라이닝 (Pipelining Commands)

때로는 수십 개 이상의 Redis 명령어를 실행해야 할 때가 있습니다. 이때 서버마다 네트워크 요청을 보내는 대신 `pipeline` 메서드를 사용할 수 있습니다. `pipeline`은 Redis 인스턴스를 인자로 받는 클로저를 받고, 클로저 내에서 실행되는 모든 명령어를 한 번에 서버로 전송해 네트워크 왕복 횟수를 줄입니다. 명령어 실행 순서도 유지됩니다:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::pipeline(function (Redis $pipe) {
    for ($i = 0; $i < 1000; $i++) {
        $pipe->set("key:$i", $i);
    }
});
```

<a name="pubsub"></a>
## 발행 / 구독(pub / sub)

Laravel은 Redis의 `publish`, `subscribe` 명령어를 간편하게 다룰 인터페이스를 제공합니다. 이 명령어들은 특정 "채널"에서 메시지를 구독하거나 메시지를 발행할 수 있게 해주어, 애플리케이션과 프로세스 간 통신을 쉽게 합니다. 다른 프로그래밍 언어로 메시지를 발행할 수도 있습니다.

먼저, `subscribe` 메서드를 사용해 채널 리스너를 설정해 보겠습니다. 긴 시간 실행되는 작업이므로 보통은 [Artisan 명령어](/docs/12.x/artisan) 내에 배치합니다:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Redis;

class RedisSubscribe extends Command
{
    /**
     * 콘솔 명령어 이름 및 서명
     *
     * @var string
     */
    protected $signature = 'redis:subscribe';

    /**
     * 콘솔 명령어 설명
     *
     * @var string
     */
    protected $description = 'Subscribe to a Redis channel';

    /**
     * 콘솔 명령어 실행
     */
    public function handle(): void
    {
        Redis::subscribe(['test-channel'], function (string $message) {
            echo $message;
        });
    }
}
```

이제 `publish` 메서드를 사용해 해당 채널에 메시지를 발행할 수 있습니다:

```php
use Illuminate\Support\Facades\Redis;

Route::get('/publish', function () {
    // ...

    Redis::publish('test-channel', json_encode([
        'name' => 'Adam Wathan'
    ]));
});
```

<a name="wildcard-subscriptions"></a>
#### 와일드카드 구독

`psubscribe` 메서드를 사용하면 와일드카드 채널로 구독할 수 있어, 모든 채널의 메시지를 수신할 때 유용합니다. 채널 이름은 제공된 클로저의 두 번째 인자로 전달됩니다:

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```