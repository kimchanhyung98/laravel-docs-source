# Redis (Redis)

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Redis와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [명령어 파이프라이닝](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개 (Introduction)

[Redis](https://redis.io)는 오픈 소스의 고급 키-값 저장소입니다. 키에는 [문자열](https://redis.io/docs/latest/develop/data-types/strings/), [해시](https://redis.io/docs/latest/develop/data-types/hashes/), [리스트](https://redis.io/docs/latest/develop/data-types/lists/), [셋](https://redis.io/docs/latest/develop/data-types/sets/), 그리고 [정렬된 셋](https://redis.io/docs/latest/develop/data-types/sorted-sets/) 등 다양한 데이터 구조를 저장할 수 있어 데이터 구조 서버라고도 불립니다.

Laravel에서 Redis를 사용하기 전에, [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 PECL을 통해 설치하여 사용하는 것을 권장합니다. 이 확장 모듈은 "user-land" PHP 패키지보다 설치가 다소 복잡하지만, Redis를 자주 사용하는 애플리케이션에서는 더 나은 성능을 기대할 수 있습니다. [Laravel Sail](/docs/10.x/sail)을 사용하는 경우, 이 확장 모듈은 이미 애플리케이션의 Docker 컨테이너에 설치되어 있습니다.

PhpRedis 확장 모듈을 설치할 수 없다면, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 PHP로 작성된 Redis 클라이언트로, 별도의 확장 모듈 없이도 작동합니다:

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 구성할 수 있습니다. 이 파일의 `redis` 배열에는 애플리케이션에서 사용하는 Redis 서버들이 정의되어 있습니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'default' => [
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', 6379),
        'database' => env('REDIS_DB', 0),
    ],

    'cache' => [
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', 6379),
        'database' => env('REDIS_CACHE_DB', 1),
    ],

],
```

설정 파일에 정의된 각 Redis 서버에는 이름, 호스트, 포트가 필요합니다. 단, Redis 연결을 나타내는 단일 URL을 사용할 수도 있습니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'default' => [
        'url' => 'tcp://127.0.0.1:6379?database=0',
    ],

    'cache' => [
        'url' => 'tls://user:password@127.0.0.1:6380?database=1',
    ],

],
```

<a name="configuring-the-connection-scheme"></a>
#### 연결 스킴 구성

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 그러나, Redis 서버의 설정 배열에서 `scheme` 옵션을 지정하여 TLS / SSL 암호화를 사용할 수도 있습니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'default' => [
        'scheme' => 'tls',
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', 6379),
        'database' => env('REDIS_DB', 0),
    ],

],
```

<a name="clusters"></a>
### 클러스터 (Clusters)

애플리케이션에서 여러 대의 Redis 서버로 구성된 클러스터를 사용하는 경우, Redis 설정의 `clusters` 키에 클러스터를 정의해주어야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로, 애플리케이션의 `config/database.php` 설정 파일에 직접 추가해야 합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'clusters' => [
        'default' => [
            [
                'host' => env('REDIS_HOST', 'localhost'),
                'password' => env('REDIS_PASSWORD'),
                'port' => env('REDIS_PORT', 6379),
                'database' => 0,
            ],
        ],
    ],

],
```

기본적으로 클러스터는 클라이언트 측 샤딩(client-side sharding)을 통해 노드들에 데이터를 분산 저장합니다. 이를 통해 노드를 풀(pool)로 묶어 대용량의 RAM을 사용할 수 있습니다. 하지만 클라이언트 측 샤딩은 장애 조치(failover)를 지원하지 않으므로, 주로 다른 기본 데이터 저장소에서도 얻을 수 있는 임시 캐시 데이터에 적합합니다.

클라이언트 측 샤딩 대신 Redis의 네이티브 클러스터링을 사용하려면, 애플리케이션의 `config/database.php` 설정 파일에서 `options.cluster` 값을 `redis`로 지정하면 됩니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
    ],

    'clusters' => [
        // ...
    ],

],
```

<a name="predis"></a>
### Predis

Predis 패키지를 통해 Redis와 상호작용하고 싶다면, `REDIS_CLIENT` 환경변수의 값을 `predis`로 설정해야 합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 `host`, `port`, `database`, `password` 서버 설정 옵션 이외에도, Predis는 [추가적인 연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이러한 추가 설정 옵션은 애플리케이션의 `config/database.php` 파일 내 Redis 서버의 설정에 추가하면 사용할 수 있습니다:

```
'default' => [
    'host' => env('REDIS_HOST', 'localhost'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', 6379),
    'database' => 0,
    'read_write_timeout' => 60,
],
```

<a name="the-redis-facade-alias"></a>
#### Redis 파사드 별칭

Laravel의 `config/app.php` 설정 파일에는 프레임워크에서 등록되는 모든 클래스 별칭이 정의된 `aliases` 배열이 있습니다. 기본적으로는 `PhpRedis` 확장 모듈에서 제공하는 `Redis` 클래스와 충돌을 피하기 위해 `Redis` 별칭이 포함되어 있지 않습니다. Predis 클라이언트를 사용하는 경우, `Redis` 별칭을 추가하고 싶다면 애플리케이션의 `config/app.php` 파일의 `aliases` 배열에 아래와 같이 추가하세요:

```
'aliases' => Facade::defaultAliases()->merge([
    'Redis' => Illuminate\Support\Facades\Redis::class,
])->toArray(),
```

<a name="phpredis"></a>
### PhpRedis

Laravel은 기본적으로 PhpRedis 확장 모듈을 사용해 Redis와 통신합니다. 어떤 클라이언트를 사용할지는 보통 `REDIS_CLIENT` 환경변수의 값을 반영하는 `redis.client` 설정 옵션에 따라 달라집니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // 나머지 Redis 설정...
],
```

기본 `scheme`, `host`, `port`, `database`, `password` 서버 설정 옵션 외에, PhpRedis는 `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `timeout`, `context` 등의 추가 연결 옵션도 지원합니다. 이러한 옵션들을 `config/database.php` 설정 파일 내 Redis 서버 설정에 추가해 사용할 수 있습니다:

```
'default' => [
    'host' => env('REDIS_HOST', 'localhost'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', 6379),
    'database' => 0,
    'read_timeout' => 60,
    'context' => [
        // 'auth' => ['username', 'secret'],
        // 'stream' => ['verify_peer' => false],
    ],
],
```

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

PhpRedis 확장 모듈은 다양한 직렬화 및 압축 알고리즘 사용도 지원합니다. 이러한 알고리즘은 Redis 설정의 `options` 배열을 통해 지정할 수 있습니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'serializer' => Redis::SERIALIZER_MSGPACK,
        'compression' => Redis::COMPRESSION_LZ4,
    ],

    // 나머지 Redis 설정...
],
```

현재 지원하는 직렬화 방식은 다음과 같습니다: `Redis::SERIALIZER_NONE`(기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`.

지원되는 압축 알고리즘에는 `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`가 있습니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

`Redis` [파사드](/docs/10.x/facades)를 통해 다양한 방식으로 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하여, [Redis 명령어](https://redis.io/commands)를 파사드에 그대로 호출하면 해당 명령이 Redis로 직접 전달됩니다. 예를 들어, 다음은 `get` 메서드를 통해 Redis의 `GET` 명령을 호출하는 예시입니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Redis;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => Redis::get('user:profile:'.$id)
        ]);
    }
}
```

위에서 설명한 것처럼, 모든 Redis 명령어를 `Redis` 파사드에 그대로 호출할 수 있습니다. Laravel은 매직 메서드를 활용해 명령어를 Redis 서버로 전달합니다. Redis 명령이 인수를 필요로 한다면, 해당 메서드에 인수를 전달하면 됩니다:

```
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는, `Redis` 파사드의 `command` 메서드를 사용해 명령어를 서버에 전달할 수도 있습니다. 이 메서드는 첫 번째 인수로 명령어 이름, 두 번째 인수로 값 배열을 받습니다:

```
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 파일에서는 여러 개의 Redis 연결 또는 서버를 정의할 수 있습니다. 특정 Redis 연결에 대한 인스턴스를 얻으려면, `Redis` 파사드의 `connection` 메서드를 사용하세요:

```
$redis = Redis::connection('connection-name');
```

기본 Redis 연결을 얻고 싶다면 추가 인수 없이 `connection` 메서드를 호출하면 됩니다:

```
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` 파사드의 `transaction` 메서드는 Redis의 기본 `MULTI` 및 `EXEC` 명령을 간편하게 래핑하여 제공합니다. 이 메서드는 클로저를 인수로 받으며, 클로저는 Redis 연결 인스턴스를 받아 해당 인스턴스에 원하는 명령어를 발행할 수 있습니다. 클로저 내부에서 실행된 모든 Redis 명령은 하나의 원자적 트랜잭션으로 실행됩니다:

```
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]  
> Redis 트랜잭션을 정의할 때에는, 트랜잭션 내에서 Redis 값을 조회할 수 없습니다. 트랜잭션은 하나의 원자적 작업으로 실행되며, 클로저 내 모든 명령어가 실행 완료된 뒤에 실제로 실행되기 때문입니다.

#### Lua 스크립트

`eval` 메서드를 사용하면 여러 Redis 명령을 하나의 원자적 작업으로 실행할 수 있습니다. 그리고 `eval` 메서드는 실행 중 Redis 키의 값을 읽거나 검사할 수 있는 장점도 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 여러 인수를 받으며, 첫 번째는 Lua 스크립트(문자열), 두 번째는 해당 스크립트가 다루는 키의 개수(정수), 세 번째는 키 이름들, 마지막으로 활용할 추가 인수들을 입력할 수 있습니다.

아래 예시는 카운터를 증가시키고, 그 값이 5보다 크면 두 번째 카운터도 증가시키며, 마지막으로 첫 번째 카운터의 값을 반환하는 예시입니다:

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
> Redis 스크립트에 대한 더 자세한 정보는 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하십시오.

<a name="pipelining-commands"></a>
### 명령어 파이프라이닝 (Pipelining Commands)

여러 개의 Redis 명령을 실행해야 하는 경우가 있습니다. 이럴 때, 각각의 명령마다 Redis 서버에 네트워크 요청을 하는 대신, `pipeline` 메서드를 사용하면 여러 명령을 한번에 Redis 서버로 전송할 수 있습니다. `pipeline` 메서드는 Redis 인스턴스를 인수로 받는 클로저 하나만을 인수로 받습니다. 해당 클로저에서 여러 명령을 발행하면, 지정한 순서대로 서버에 한번에 전송되어 네트워크 트립을 줄일 수 있습니다:

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

Laravel은 Redis의 `publish` 및 `subscribe` 명령을 사용하는 편리한 인터페이스를 제공합니다. 이 명령어들을 통해 특정 "채널"의 메시지를 수신할 수 있습니다. 다른 애플리케이션 또는 다른 프로그래밍 언어로도 해당 채널에 메시지를 발행할 수 있어, 애플리케이션과 프로세스 간의 효율적인 통신이 가능합니다.

먼저, `subscribe` 메서드를 사용해 채널 리스너를 설정해보겠습니다. 이 메서드는 실행 시 장시간 동작하는 프로세스를 시작하므로, [Artisan 명령어](/docs/10.x/artisan) 내부에 작성하는 것이 일반적입니다:

```
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Redis;

class RedisSubscribe extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'redis:subscribe';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Subscribe to a Redis channel';

    /**
     * Execute the console command.
     */
    public function handle(): void
    {
        Redis::subscribe(['test-channel'], function (string $message) {
            echo $message;
        });
    }
}
```

이제 `publish` 메서드를 사용해 채널로 메시지를 발행할 수 있습니다:

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
#### 와일드카드 구독

`psubscribe` 메서드를 사용하면 와일드카드 채널에도 구독할 수 있습니다. 이는 모든 채널의 메시지를 수신하거나, 특정 패턴의 채널에 대한 메시지를 모두 받고 싶을 때 유용합니다. 해당 채널 이름은 클로저에 두 번째 인수로 전달됩니다:

```
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```
