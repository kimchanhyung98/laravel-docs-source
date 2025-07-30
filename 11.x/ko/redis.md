# Redis

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Redis와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [파이프라인 명령](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개 (Introduction)

[Redis](https://redis.io)는 오픈 소스의 고급 키-값 저장소입니다. 키가 [문자열](https://redis.io/docs/data-types/strings/), [해시](https://redis.io/docs/data-types/hashes/), [리스트](https://redis.io/docs/data-types/lists/), [셋](https://redis.io/docs/data-types/sets/), [정렬된 셋](https://redis.io/docs/data-types/sorted-sets/)을 포함할 수 있기 때문에, 종종 데이터 구조 서버라고도 불립니다.

Laravel과 Redis를 사용하기 전에, PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 설치하고 사용하는 것을 권장합니다. 이 확장 모듈은 사용자 영역 PHP 패키지에 비해 설치가 더 복잡하지만, Redis를 많이 사용하는 애플리케이션에서는 더 나은 성능을 낼 수 있습니다. 만약 [Laravel Sail](/docs/11.x/sail)을 사용한다면, 이 확장 모듈은 이미 애플리케이션의 Docker 컨테이너에 설치되어 있습니다.

만약 PhpRedis 확장 모듈을 설치할 수 없다면, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 순수 PHP로 작성된 Redis 클라이언트로, 별도의 확장 모듈이 필요하지 않습니다:

```shell
composer require predis/predis:^2.0
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 구성할 수 있습니다. 이 파일 안에서 애플리케이션에서 사용하는 Redis 서버들을 포함하는 `redis` 배열을 확인할 수 있습니다:

```
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

설정 파일에 정의된 각 Redis 서버는 이름, 호스트, 포트를 반드시 지정해야 합니다. 단일 URL로 Redis 연결을 표현하는 경우는 예외입니다:

```
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
#### 연결 스킴 구성 (Configuring the Connection Scheme)

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 다만, Redis 서버 설정 배열 내에서 `scheme` 옵션을 지정하여 TLS/SSL 암호화를 사용할 수도 있습니다:

```
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

애플리케이션에서 Redis 서버 클러스터를 사용하는 경우, Redis 설정의 `clusters` 키 안에 클러스터를 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로 `config/database.php` 설정 파일 내에 직접 생성해야 합니다:

```
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

기본적으로 Laravel은 `options.cluster` 설정 값이 `redis`로 설정되어 있어 네이티브 Redis 클러스터링을 사용합니다. Redis 클러스터링은 장애 조치(failover)를 우아하게 처리하기 때문에 훌륭한 기본 선택입니다.

Laravel은 Predis를 사용할 때 클라이언트 사이드 샤딩도 지원합니다. 다만 클라이언트 사이드 샤딩에서는 장애 조치를 처리하지 않으므로, 주로 다른 기본 데이터 저장소에서 사용할 수 있는 일시적인 캐시 데이터에 적합합니다.

클라이언트 사이드 샤딩을 사용하고 싶다면, 애플리케이션의 `config/database.php` 설정 파일에서 `options.cluster` 설정 값을 제거하면 됩니다:

```
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

애플리케이션에서 Predis 패키지를 사용해 Redis와 상호작용하려면, 환경 변수 `REDIS_CLIENT`의 값을 `predis`로 설정해야 합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 설정 옵션 외에도, Predis는 각 Redis 서버별로 추가적인 [연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이러한 추가 옵션을 이용하려면 `config/database.php` 내 Redis 서버 설정에 다음과 같이 추가하세요:

```
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

기본적으로 Laravel은 PhpRedis 확장 모듈을 통해 Redis와 통신합니다. Laravel이 사용할 Redis 클라이언트는 일반적으로 `redis.client` 설정 옵션의 값 또는 `REDIS_CLIENT` 환경 변수 값을 따릅니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

PhpRedis는 기본 설정 옵션 외에도 `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context` 등의 추가 연결 파라미터를 지원합니다. 이 중 필요한 옵션을 `config/database.php`의 Redis 서버 설정에 추가할 수 있습니다:

```
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

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축 설정 (PhpRedis Serialization and Compression)

PhpRedis 확장 모듈은 여러 직렬화 및 압축 알고리즘을 설정할 수 있습니다. 이 설정들은 Redis 설정의 `options` 배열을 통해 구성할 수 있습니다:

```
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

현재 지원되는 직렬화 옵션은 다음과 같습니다: `Redis::SERIALIZER_NONE` (기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`.

지원되는 압축 알고리즘은 다음과 같습니다: `Redis::COMPRESSION_NONE` (기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

`Redis` [파사드](/docs/11.x/facades)의 다양한 메서드를 호출하여 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원해, 파사드에 임의의 [Redis 명령어](https://redis.io/commands)를 메서드로 호출하면 해당 명령어가 직접 Redis로 전달됩니다. 예를 들어, Redis의 `GET` 명령을 `Redis` 파사드의 `get` 메서드로 호출할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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

위에서 언급했듯이, 어떤 Redis 명령어든 `Redis` 파사드에서 호출할 수 있습니다. Laravel은 매직 메서드를 사용해 명령어를 Redis 서버에 전달합니다. 만약 Redis 명령어가 인수를 요구한다면, 해당 인수들을 파사드의 메서드에 넘기면 됩니다:

```
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또한, `Redis` 파사드의 `command` 메서드를 사용해 명령어 이름(첫 번째 인수)과 인수 배열(두 번째 인수)을 전달할 수도 있습니다:

```
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기 (Using Multiple Redis Connections)

`config/database.php` 설정 파일에서 여러 Redis 연결 또는 서버를 정의할 수 있습니다. 특정 Redis 연결에 접근하려면 `Redis` 파사드의 `connection` 메서드를 사용하세요:

```
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스가 필요하면, 인자를 전달하지 않고 `connection` 메서드를 호출하면 됩니다:

```
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` 파사드의 `transaction` 메서드는 Redis의 `MULTI`와 `EXEC` 명령을 묶어주는 편리한 래퍼입니다. `transaction` 메서드는 단 하나의 인수인 클로저를 받습니다. 이 클로저는 Redis 연결 인스턴스를 인수로 받고, 그 인스턴스를 통해 원하는 모든 명령어를 실행할 수 있습니다. 클로저 내부에서 실행된 모든 Redis 명령어는 하나의 원자적 트랜잭션으로 실행됩니다:

```
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]  
> Redis 트랜잭션을 정의할 때는 Redis 연결에서 값을 조회할 수 없습니다. 트랜잭션은 모든 명령이 실행된 후 한 번에 원자적으로 수행되므로, 클로저 내부 명령어가 모두 끝나기 전까지 작업이 처리되지 않는다는 점을 기억하세요.

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령어를 하나의 원자적 연산으로 실행하는 또 다른 방법입니다. 다만 `eval` 메서드는 Redis 키 값을 조작하고 검사할 수 있다는 장점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 처음에는 어려워 보일 수 있지만, 기본 예제를 함께 살펴보겠습니다. `eval` 메서드는 여러 인수를 받는데, 먼저 Lua 스크립트(문자열)를 전달하고, 두 번째는 스크립트가 접근하는 키의 개수(정수), 세 번째부터는 키의 이름들, 그리고 추가적인 인수를 넘길 수 있습니다.

다음 예제에서는 카운터를 증가시키고, 그 새 값을 검사하며, 카운터가 5보다 크면 두 번째 카운터도 증가시킨 후 첫 번째 카운터 값을 반환합니다:

```
$value = Redis::eval(<<<'LUA'
    local counter = redis.call("incr", KEYS[1])

    if counter > 5 then
        redis.call("incr", KEYS[2])
    end

    return counter
LUA, 2, 'first-counter', 'second-counter');
```

> [!WARNING]  
> Redis 스크립팅에 대한 자세한 내용은 [Redis 문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 파이프라인 명령 (Pipelining Commands)

가끔 수십 개의 Redis 명령어를 실행해야 하는 경우가 있습니다. 각각의 명령마다 Redis 서버에 네트워크 요청을 보내는 대신, `pipeline` 메서드를 활용할 수 있습니다. `pipeline` 메서드는 하나의 인수로 클로저를 받고, 이 클로저는 Redis 인스턴스를 인자로 받습니다. 이 인스턴스에 여러 명령어를 호출하면, 이들이 모두 모여 한 번에 Redis 서버에 전송되어 네트워크 왕복 횟수가 줄어듭니다. 물론 명령어는 호출된 순서대로 실행됩니다:

```
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::pipeline(function (Redis $pipe) {
    for ($i = 0; $i < 1000; $i++) {
        $pipe->set("key:$i", $i);
    }
});
```

<a name="pubsub"></a>
## Pub / Sub

Laravel은 Redis의 `publish`와 `subscribe` 명령을 쉽게 사용할 수 있도록 인터페이스를 제공합니다. 이 Redis 명령어들은 특정 "채널"에서 메시지를 수신(listen)하거나, 다른 애플리케이션이나 다른 프로그래밍 언어에서 해당 채널로 메시지를 발행(publish)할 수 있어, 애플리케이션과 프로세스 간의 손쉬운 통신이 가능합니다.

먼저, [Artisan 명령어](/docs/11.x/artisan) 안에 `subscribe` 메서드를 호출해 채널 수신기를 설정해봅시다. `subscribe`는 장시간 실행되는 프로세스를 시작하기 때문에 Artisan 명령어에서 실행하는 것이 적합합니다:

```
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Redis;

class RedisSubscribe extends Command
{
    /**
     * 콘솔 명령어 이름과 시그니처
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

이제 다른 곳에서 `publish` 메서드를 사용해 채널에 메시지를 발행할 수 있습니다:

```
use Illuminate\Support\Facades\Redis;

Route::get('/publish', function () {
    // ...

    Redis::publish('test-channel', json_encode([
        'name' => 'Adam Wathan'
    ]));
});
```

<a name="wildcard-subscriptions"></a>
#### 와일드카드 구독 (Wildcard Subscriptions)

`psubscribe` 메서드를 사용하면 와일드카드 채널을 구독할 수 있어, 모든 채널의 모든 메시지를 수신하는 데 유용합니다. 메시지와 함께 채널 이름도 클로저의 두 번째 인수로 전달됩니다:

```
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```