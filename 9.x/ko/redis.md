# Redis

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [phpredis](#phpredis)
- [Redis와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [명령어 파이프라이닝](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개 (Introduction)

[Redis](https://redis.io)는 오픈 소스이며 고급 키-값 저장소입니다. 키가 [문자열](https://redis.io/topics/data-types#strings), [해시](https://redis.io/topics/data-types#hashes), [리스트](https://redis.io/topics/data-types#lists), [셋](https://redis.io/topics/data-types#sets), [정렬된 셋](https://redis.io/topics/data-types#sorted-sets) 등 다양한 자료구조를 포함할 수 있기 때문에 데이터 구조 서버(data structure server)로 자주 불립니다.

Laravel과 Redis를 함께 사용하기 전에, 먼저 [phpredis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 PECL을 통해 설치하고 사용하는 것을 권장합니다. 이 확장은 사용자 영역(user-land) PHP 패키지보다 설치가 다소 복잡하지만, Redis를 많이 사용하는 애플리케이션에서 더 좋은 성능을 낼 수 있습니다. 만약 [Laravel Sail](/docs/9.x/sail)을 사용 중이라면, 애플리케이션의 Docker 컨테이너 내에 이미 이 확장이 설치되어 있습니다.

phpredis 확장 모듈을 설치할 수 없는 경우에는 `predis/predis` 패키지를 Composer를 통해 설치할 수 있습니다. Predis는 PHP로만 작성된 Redis 클라이언트이며 추가 확장 모듈이 필요 없습니다:

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 할 수 있습니다. 이 파일 내에는 애플리케이션에서 사용하는 Redis 서버를 정의한 `redis` 배열이 있습니다:

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

설정 파일에 정의된 각 Redis 서버는 이름, 호스트, 포트를 반드시 가져야 하며, Redis 연결을 나타내는 단일 URL을 정의하는 경우는 예외입니다:

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
#### 연결 스킴 설정하기

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 하지만 Redis 서버 설정 배열에 `scheme` 옵션을 지정하여 TLS / SSL 암호화를 사용할 수도 있습니다:

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

애플리케이션에서 여러 Redis 서버의 클러스터를 사용한다면, `clusters` 키에 Redis 클러스터를 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로 `config/database.php` 설정 파일에 직접 추가해야 합니다:

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

기본적으로 클러스터는 노드 사이 클라이언트 측 샤딩(client-side sharding)을 수행하여 여러 노드를 묶고 많은 양의 RAM을 사용할 수 있게 합니다. 하지만 클라이언트 측 샤딩은 장애 조치(failover)를 지원하지 않으므로, 주로 다른 기본 데이터 저장소에서 사용할 수 있는 일시적인 캐시 데이터에 적합합니다.

네이티브 Redis 클러스터링을 사용하려면 `config/database.php` 설정 파일에서 `options.cluster` 값을 `redis`로 지정하면 됩니다:

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

애플리케이션에서 Predis 패키지를 통해 Redis와 상호작용하려면, `REDIS_CLIENT` 환경 변수의 값을 `predis`로 설정해야 합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본적인 `host`, `port`, `database`, `password` 외에도 Predis는 각 Redis 서버에 대해 추가 [연결 매개변수](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이러한 추가 설정을 사용하려면, 애플리케이션의 `config/database.php` 설정 파일 내 해당 Redis 서버 설정에 추가하면 됩니다:

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
#### Redis 페이스(facade) 별칭 설정

`config/app.php` 설정 파일에는 프레임워크가 등록할 클래스 별칭들을 담은 `aliases` 배열이 있습니다. 기본적으로 `Redis` 별칭은 포함되어 있지 않는데, 이는 phpredis 확장에서 제공하는 `Redis` 클래스 이름과 충돌하기 때문입니다. Predis 클라이언트를 사용하고 `Redis` 별칭을 추가하고 싶다면, 애플리케이션의 `config/app.php` 파일 내 `aliases` 배열에 아래처럼 추가할 수 있습니다:

```
'aliases' => Facade::defaultAliases()->merge([
    'Redis' => Illuminate\Support\Facades\Redis::class,
])->toArray(),
```

<a name="phpredis"></a>
### phpredis

Laravel은 기본적으로 phpredis 확장을 사용해 Redis와 통신합니다. Laravel이 Redis와 통신하는 데 사용하는 클라이언트는 `redis.client` 설정 옵션의 값에 따라 결정되며, 보통은 `REDIS_CLIENT` 환경 변수 값을 반영합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // 나머지 Redis 설정...
],
```

기본 `scheme`, `host`, `port`, `database`, `password` 서버 설정 외에도 phpredis는 다음과 같은 추가 연결 매개변수를 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `timeout`, `context`. 이러한 옵션은 `config/database.php` 설정 파일 내 해당 Redis 서버 설정에 추가할 수 있습니다:

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
#### phpredis 직렬화 및 압축

phpredis 확장은 다양한 직렬화 및 압축 알고리즘을 사용할 수 있도록 설정할 수 있습니다. 이러한 알고리즘은 Redis 설정 내 `options` 배열을 통해 구성할 수 있습니다:

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

현재 지원하는 직렬화 알고리즘은 `Redis::SERIALIZER_NONE`(기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`이 있습니다.

지원하는 압축 알고리즘으로는 `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`가 있습니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

`Redis` [facade](/docs/9.x/facades)의 다양한 메서드를 호출해 Redis와 상호작용할 수 있습니다. `Redis` facade는 동적 메서드를 지원하므로, Redis의 어떤 [명령어](https://redis.io/commands)도 facade에서 메서드 형태로 호출할 수 있으며, 해당 명령어는 Redis에 직접 전달됩니다. 아래 예시는 Redis의 `GET` 명령어를 `Redis` facade의 `get` 메서드를 호출하여 실행하는 예시입니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Redis;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 보여줍니다.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        return view('user.profile', [
            'user' => Redis::get('user:profile:'.$id)
        ]);
    }
}
```

앞서 말한 것처럼 `Redis` facade에서 Redis 명령어를 자유롭게 호출할 수 있습니다. Laravel은 매직 메서드로 명령어를 Redis 서버에 전달합니다. Redis 명령어가 인수를 요구하면, 해당 인수를 facade 메서드에 전달하세요:

```
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는 첫 번째 인수로 명령어 이름, 두 번째 인수로 명령어 인수 배열을 받는 `command` 메서드를 사용해 명령어를 서버에 전달할 수도 있습니다:

```
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 파일에서는 여러 Redis 연결 또는 서버를 정의할 수 있습니다. 특정 Redis 연결을 얻으려면 `Redis` facade의 `connection` 메서드를 사용하세요:

```
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스가 필요하면 인수를 전달하지 않고 `connection` 메서드를 호출할 수 있습니다:

```
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` facade의 `transaction` 메서드는 Redis의 기본 `MULTI`와 `EXEC` 명령어를 편리하게 감싸는 기능을 제공합니다. `transaction` 메서드는 클로저를 유일한 인수로 받으며, 이 클로저는 Redis 연결 인스턴스를 전달받아 원하는 명령어를 실행할 수 있습니다. 클로저 안에서 실행되는 모든 Redis 명령어는 하나의 원자적 트랜잭션으로 실행됩니다:

```
use Illuminate\Support\Facades\Redis;

Redis::transaction(function ($redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션 내에서는 Redis 연결에서 값을 조회할 수 없습니다. 트랜잭션은 단일 원자적 작업으로 실행되며, 클로저 내 모든 명령어가 실행을 마친 후에야 실제로 수행되기 때문입니다.

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령어를 하나의 원자적 작업으로 실행하는 또 다른 방법입니다. 그러나 `eval`은 작업 도중 Redis 키 값을 접근하고 검사할 수 있다는 이점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 여러 인수를 기대합니다. 첫 번째는 Lua 스크립트(문자열), 두 번째는 스크립트가 다루는 키의 개수(정수), 세 번째 이후는 해당 키 이름들과 스크립트 내에서 사용할 추가 인수들입니다.

아래 예제는 하나의 카운터를 증가시키고, 증가된 값이 5보다 크면 두 번째 카운터를 증가시키며, 첫 번째 카운터 값을 반환합니다:

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
> Redis 스크립트 사용에 더 자세한 내용은 [Redis 문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 명령어 파이프라이닝 (Pipelining Commands)

대량의 Redis 명령어를 실행해야 할 때가 있습니다. 각 명령어마다 Redis 서버와 네트워크 왕복을 하는 대신에 `pipeline` 메서드를 사용할 수 있습니다. `pipeline`은 하나의 클로저를 인수로 받으며, 이 클로저는 Redis 인스턴스를 전달받습니다. 클로저 내에서 수행한 모든 명령어는 한꺼번에 Redis 서버로 전달되어 네트워크 요청 횟수를 줄입니다. 명령어는 클로저 내 호출된 순서대로 실행됩니다:

```
use Illuminate\Support\Facades\Redis;

Redis::pipeline(function ($pipe) {
    for ($i = 0; $i < 1000; $i++) {
        $pipe->set("key:$i", $i);
    }
});
```

<a name="pubsub"></a>
## Pub / Sub

Laravel은 Redis의 `publish`와 `subscribe` 명령어를 쉽게 사용할 수 있도록 인터페이스를 제공합니다. 이 명령어들은 특정 "채널"에서 메시지를 수신할 수 있도록 해줍니다. 다른 애플리케이션이나 다른 프로그래밍 언어로도 채널에 메시지를 발행할 수 있어, 애플리케이션과 프로세스 간 효율적인 통신이 가능합니다.

먼저, `subscribe` 메서드로 채널 리스너를 설정해보겠습니다. 이 메서드는 오래 실행되는 프로세스를 시작하므로, [Artisan 명령어](/docs/9.x/artisan) 내에서 호출하는 것이 일반적입니다:

```
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Redis;

class RedisSubscribe extends Command
{
    /**
     * 콘솔 명령어 이름과 서명입니다.
     *
     * @var string
     */
    protected $signature = 'redis:subscribe';

    /**
     * 콘솔 명령어 설명입니다.
     *
     * @var string
     */
    protected $description = 'Subscribe to a Redis channel';

    /**
     * 콘솔 명령어를 실행합니다.
     *
     * @return mixed
     */
    public function handle()
    {
        Redis::subscribe(['test-channel'], function ($message) {
            echo $message;
        });
    }
}
```

이제 `publish` 메서드로 동일 채널에 메시지를 발행할 수 있습니다:

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

`psubscribe` 메서드를 사용하면 와일드카드 채널 구독이 가능합니다. 이는 모든 채널의 모든 메시지를 수신하는 데 유용할 수 있습니다. 두 번째 인수로 전달된 클로저에 채널 이름이 전달됩니다:

```
Redis::psubscribe(['*'], function ($message, $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function ($message, $channel) {
    echo $message;
});
```