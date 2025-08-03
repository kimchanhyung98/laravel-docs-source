# Redis

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Redis와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [파이프라이닝 명령어](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개 (Introduction)

[Redis](https://redis.io)는 오픈 소스이자 고급 키-값 저장소입니다. 키가 [문자열](https://redis.io/docs/data-types/strings/), [해시](https://redis.io/docs/data-types/hashes/), [리스트](https://redis.io/docs/data-types/lists/), [셋](https://redis.io/docs/data-types/sets/), [정렬된 셋](https://redis.io/docs/data-types/sorted-sets/) 등 다양한 데이터 구조를 가질 수 있기 때문에 흔히 데이터 구조 서버라고 불립니다.

Laravel에서 Redis를 사용하기 전에, PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 설치하고 사용하는 것을 권장합니다. 이 확장은 "유저 레벨" PHP 패키지에 비해 설치가 다소 복잡하지만, Redis를 많이 사용하는 애플리케이션에서는 더 나은 성능을 제공할 수 있습니다. 만약 [Laravel Sail](/docs/10.x/sail)을 사용 중이라면, 이 확장은 이미 애플리케이션의 Docker 컨테이너에 설치되어 있습니다.

PhpRedis 확장을 설치할 수 없는 경우, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 완전히 PHP로 작성된 Redis 클라이언트로 추가 확장 설치가 필요 없습니다:

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 구성할 수 있습니다. 이 파일 내에는 애플리케이션에서 사용하는 Redis 서버들을 포함하는 `redis` 배열이 있습니다:

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

설정 파일에 정의된 각 Redis 서버는 이름, 호스트, 포트를 반드시 가져야 하며, 단일 URL로 Redis 연결을 정의하는 경우는 예외입니다:

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
#### 연결 스킴 구성하기

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 하지만 Redis 서버 설정 배열에 `scheme` 옵션을 지정하여 TLS / SSL 암호화를 사용할 수 있습니다:

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

애플리케이션이 Redis 서버 클러스터를 사용하는 경우, Redis 설정에서 `clusters` 키로 클러스터들을 정의해야 합니다. 기본 설정에는 이 키가 없으므로, 애플리케이션의 `config/database.php` 파일에 직접 추가해야 합니다:

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

기본적으로 클러스터는 클라이언트 사이드 샤딩을 수행하여 노드 전체에 메모리를 풀링할 수 있습니다. 하지만 클라이언트 사이드 샤딩은 자동 장애 조치를 지원하지 않으므로, 주로 다른 주요 데이터 저장소에서 사용할 수 있는 일시적인 캐시 데이터에 적합합니다.

네이티브 Redis 클러스터링을 사용하고 싶다면, 애플리케이션의 `config/database.php` 파일에서 `options.cluster` 설정 값을 `redis`로 지정하세요:

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

애플리케이션에서 Predis 패키지를 통해 Redis와 상호작용하려면, `REDIS_CLIENT` 환경 변수 값을 `predis`로 설정해야 합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

Predis는 기본 `host`, `port`, `database`, `password` 서버 설정 옵션 외에도 [추가적인 연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이러한 추가 옵션을 적용하려면, 애플리케이션의 `config/database.php` 파일에서 해당 Redis 서버 설정에 추가하면 됩니다:

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
#### Redis Facade 별칭

Laravel의 `config/app.php` 설정 파일에는 `aliases` 배열이 있어 프레임워크에서 등록할 클래스 별칭들을 정의합니다. 기본적으로 `Redis` 별칭은 포함되어 있지 않은데, 이는 PhpRedis 확장이 제공하는 `Redis` 클래스 이름과 충돌하기 때문입니다. Predis 클라이언트를 사용 중이고 `Redis` 별칭을 추가하고 싶다면, 애플리케이션의 `config/app.php` 파일에 다음과 같이 추가하세요:

```
'aliases' => Facade::defaultAliases()->merge([
    'Redis' => Illuminate\Support\Facades\Redis::class,
])->toArray(),
```

<a name="phpredis"></a>
### PhpRedis

기본적으로 Laravel은 PhpRedis 확장을 통해 Redis와 통신합니다. Laravel이 사용할 Redis 클라이언트는 `redis.client` 설정 옵션 값을 기준으로 하며, 이 값은 일반적으로 `REDIS_CLIENT` 환경 변수 값을 반영합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // 나머지 Redis 설정...
],
```

PhpRedis는 기본 `scheme`, `host`, `port`, `database`, `password` 설정 옵션 이외에도 `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `timeout`, `context` 같은 추가 연결 파라미터를 지원합니다. 이러한 옵션들을 `config/database.php` 파일 내 Redis 서버 설정에 추가할 수 있습니다:

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

PhpRedis 확장은 다양한 직렬화(serializer)와 압축 알고리즘도 사용할 수 있습니다. 이들은 Redis 설정의 `options` 배열을 통해 구성할 수 있습니다:

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

현재 지원되는 직렬화 방식은: `Redis::SERIALIZER_NONE` (기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`입니다.

지원되는 압축 알고리즘은: `Redis::COMPRESSION_NONE` (기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`입니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

`Redis` [페이사드](/docs/10.x/facades)를 통해 Redis와 다양한 메서드를 호출하면서 상호작용할 수 있습니다. `Redis` 페이사드는 동적 메서드를 지원하므로, Redis의 모든 [명령어](https://redis.io/commands)를 해당 메서드 이름으로 직접 호출할 수 있으며, 이 호출은 곧바로 Redis 서버에 전달됩니다. 다음 예시에서는 `Redis` 페이사드에서 `get` 메서드를 호출하여 Redis의 `GET` 명령어를 실행합니다:

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

앞서 언급했듯이, Redis의 모든 명령어는 `Redis` 페이사드에서 사용할 수 있습니다. Laravel은 매직 메서드를 통해 명령어를 Redis 서버로 전달합니다. 만약 Redis 명령어가 인수를 요구한다면, 해당 인수들을 메서드 호출 시 넘기면 됩니다:

```
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는 `Redis` 페이사드의 `command` 메서드를 사용해 명령어 이름을 첫 번째 인수로, 명령어 인수를 배열로 두 번째 인수로 넘기면서 명령어를 실행할 수도 있습니다:

```
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 설정 파일에서는 여러 Redis 연결(서버)을 정의할 수 있습니다. 특정 Redis 연결에 대한 인스턴스가 필요하면, `Redis` 페이사드의 `connection` 메서드에 연결 이름을 넘겨 호출하세요:

```
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스가 필요하면, 인수를 넘기지 않고 `connection` 메서드를 호출하면 됩니다:

```
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` 페이사드의 `transaction` 메서드는 Redis의 기본 `MULTI` 및 `EXEC` 명령어를 감싸 편리하게 사용할 수 있게 합니다. `transaction` 메서드는 클로저를 인수로 받고, 이 클로저는 Redis 연결 인스턴스를 받아 원하는 명령어들을 이 인스턴스에 실행할 수 있습니다. 클로저 내에서 실행된 모든 Redis 명령어들은 하나의 원자적 트랜잭션으로 처리됩니다:

```
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]  
> Redis 트랜잭션을 정의할 때는 Redis 연결에서 값을 가져올 수 없습니다. 트랜잭션은 하나의 원자적 작업으로 실행되며, 클로저 내에 작성된 모든 명령어들이 실행을 마친 후에 트랜잭션이 적용되기 때문입니다.

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령어를 단일 원자 작업으로 실행할 수 있는 또 다른 방법입니다. 하지만 `eval` 메서드는 Redis 키 값을 실행 중에 조작하거나 검사할 수 있다는 장점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 여러 인수를 요구하는데, 첫 번째는 Lua 스크립트 문자열, 두 번째는 스크립트에서 사용할 키의 개수, 세 번째부터 키 이름들, 이후에는 스크립트 내에서 접근할 추가 인수들입니다.

다음 예시는 첫 번째 카운터를 증가시키고, 그 값이 5보다 크면 두 번째 카운터도 증가시킨 뒤, 첫 번째 카운터 값을 반환하는 간단한 스크립트입니다:

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
### 파이프라이닝 명령어 (Pipelining Commands)

많은 Redis 명령어를 연속적으로 실행해야 할 때, 각 명령을 위해 Redis 서버와 네트워크를 주고받는 비용이 큽니다. 이때 `pipeline` 메서드를 사용하면 네트워크 왕복 횟수를 줄일 수 있습니다. `pipeline` 메서드는 클로저를 인수로 받으며, 이 클로저에서 받은 Redis 인스턴스에 명령어를 모두 전달하면, 한꺼번에 Redis 서버로 보내 실행합니다. 명령어는 여전히 작성된 순서대로 실행됩니다:

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

Laravel은 Redis의 `publish`와 `subscribe` 명령어에 대한 편리한 인터페이스를 제공합니다. 이 명령어들은 특정 채널에서 메시지를 수신하거나, 다른 애플리케이션 또는 프로그래밍 언어에서 채널로 메시지를 발행하는 기능을 하며, 애플리케이션과 프로세스 간의 쉽게 통신할 수 있게 해줍니다.

먼저 `subscribe` 메서드로 채널 리스너를 설정해보겠습니다. 이 메서드는 긴 실행 프로세스를 시작하므로, 일반적으로 [Artisan 명령어](/docs/10.x/artisan) 내에 배치합니다:

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

그다음, `publish` 메서드를 사용해 채널에 메시지를 발행할 수 있습니다:

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

`psubscribe` 메서드를 사용하면 와일드카드 채널을 구독할 수 있어, 모든 채널의 모든 메시지를 잡아내는 데 유용합니다. 이때 채널 이름은 클로저에 두 번째 인수로 전달됩니다:

```
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```