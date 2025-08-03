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

[Redis](https://redis.io)는 오픈 소스의 고급 키-값 저장소입니다. 키가 [문자열](https://redis.io/topics/data-types#strings), [해시](https://redis.io/topics/data-types#hashes), [리스트](https://redis.io/topics/data-types#lists), [셋](https://redis.io/topics/data-types#sets), [정렬된 셋](https://redis.io/topics/data-types#sorted-sets)을 포함할 수 있기 때문에 데이터 구조 서버(data structure server)로도 자주 불립니다.

Laravel에서 Redis를 사용하기 전에 PECL을 통해 [phpredis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 설치 및 사용하실 것을 권장합니다. 이 확장 모듈은 "사용자 공간(user-land)" PHP 패키지에 비해 설치가 더 복잡하지만, Redis를 많이 사용하는 애플리케이션에서는 더 나은 성능을 발휘할 수 있습니다. 만약 [Laravel Sail](/docs/{{version}}/sail)을 사용 중이라면, 이 확장 모듈은 애플리케이션의 Docker 컨테이너에 이미 설치되어 있습니다.

phpredis 확장 모듈을 설치할 수 없는 경우, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 PHP로 완전히 작성된 Redis 클라이언트로, 별도의 확장 모듈 설치가 필요 없습니다:

```bash
composer require predis/predis
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 구성할 수 있습니다. 이 파일 내에서 애플리케이션이 사용하는 Redis 서버들을 포함하는 `redis` 배열을 볼 수 있습니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'default' => [
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD', null),
        'port' => env('REDIS_PORT', 6379),
        'database' => env('REDIS_DB', 0),
    ],

    'cache' => [
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD', null),
        'port' => env('REDIS_PORT', 6379),
        'database' => env('REDIS_CACHE_DB', 1),
    ],

],
```

설정 파일에 정의된 각각의 Redis 서버는 이름, 호스트, 포트를 가져야 합니다. 다만 Redis 연결을 한 줄 URL 형식으로 정의하는 경우는 예외입니다:

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
#### 연결 프로토콜 설정

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 프로토콜을 사용합니다. 하지만 Redis 서버의 설정 배열에 `scheme` 옵션을 지정하여 TLS/SSL 암호화를 사용할 수 있습니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'default' => [
        'scheme' => 'tls',
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD', null),
        'port' => env('REDIS_PORT', 6379),
        'database' => env('REDIS_DB', 0),
    ],

],
```

<a name="clusters"></a>
### 클러스터 (Clusters)

애플리케이션에서 Redis 서버 클러스터를 사용 중이라면, `clusters` 키를 `config/database.php` 파일 내의 Redis 설정에 정의해야 합니다. 기본적으로 이 키는 없으므로 직접 만들어야 합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'clusters' => [
        'default' => [
            [
                'host' => env('REDIS_HOST', 'localhost'),
                'password' => env('REDIS_PASSWORD', null),
                'port' => env('REDIS_PORT', 6379),
                'database' => 0,
            ],
        ],
    ],

],
```

기본적으로 클러스터는 클라이언트 측 샤딩(client-side sharding)을 사용해 노드들을 풀링하고 많은 양의 RAM을 활용할 수 있게 합니다. 다만, 클라이언트 측 샤딩은 장애 조치(failover)를 처리하지 않기 때문에, 주로 다른 기본 데이터 저장소에서 제공 가능한 일시적 캐시 데이터에 적합합니다.

만약 클라이언트 측 샤딩 대신 네이티브 Redis 클러스터링을 사용하고 싶다면, `config/database.php` 파일의 `options.cluster` 설정 값을 `redis`로 지정하면 됩니다:

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

Predis 패키지를 통해 Redis와 상호작용하려면, `REDIS_CLIENT` 환경 변수 값을 `predis`로 설정해야 합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 `host`, `port`, `database`, `password` 옵션 외에도 Predis는 각 Redis 서버에 대해 추가 [연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이러한 추가 설정을 적용하려면, `config/database.php`에서 Redis 서버 설정에 해당 옵션들을 포함시키면 됩니다:

```
'default' => [
    'host' => env('REDIS_HOST', 'localhost'),
    'password' => env('REDIS_PASSWORD', null),
    'port' => env('REDIS_PORT', 6379),
    'database' => 0,
    'read_write_timeout' => 60,
],
```

<a name="the-redis-facade-alias"></a>
#### Redis Facade 별칭

Laravel의 `config/app.php` 설정 파일 안 `aliases` 배열은 프레임워크가 등록하는 모든 클래스 별칭들을 정의합니다. Laravel이 제공하는 각 [페이사드](/docs/{{version}}/facades)에 대해 편의를 위해 별칭이 포함되어 있으나, `Redis` 별칭은 phpredis 확장 모듈의 `Redis` 클래스명과 충돌하기 때문에 기본적으로 비활성화되어 있습니다. Predis 클라이언트를 사용하며 이 별칭을 활성화하고 싶다면 `config/app.php` 파일에서 주석을 해제하면 됩니다.

<a name="phpredis"></a>
### phpredis

기본적으로 Laravel은 phpredis 확장 모듈을 통해 Redis와 통신합니다. Laravel에서 사용할 Redis 클라이언트는 보통 `REDIS_CLIENT` 환경 변수 값과 같은 `redis.client` 설정 옵션으로 결정됩니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // 나머지 Redis 설정...
],
```

phpredis는 기본 `scheme`, `host`, `port`, `database`, `password` 설정 외에도 다음 연결 옵션을 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `timeout`, `context`. 필요하다면 `config/database.php`에서 Redis 서버 설정에 이 옵션들을 추가할 수 있습니다:

```
'default' => [
    'host' => env('REDIS_HOST', 'localhost'),
    'password' => env('REDIS_PASSWORD', null),
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
#### phpredis 직렬화 및 압축 설정

phpredis 확장 모듈은 다양한 직렬화 및 압축 알고리즘 사용도 지원합니다. 이들은 Redis 설정 내 `options` 배열을 통해 구성할 수 있습니다:

```
use Redis;

'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'serializer' => Redis::SERIALIZER_MSGPACK,
        'compression' => Redis::COMPRESSION_LZ4,
    ],

    // 나머지 Redis 설정...
],
```

현재 지원하는 직렬화 알고리즘은 `Redis::SERIALIZER_NONE` (기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`입니다.

지원하는 압축 알고리즘은 `Redis::COMPRESSION_NONE` (기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`입니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

`Redis` [페이사드](/docs/{{version}}/facades)를 통해 다양한 메서드를 호출함으로써 Redis와 상호작용할 수 있습니다. `Redis` 페이사드는 동적 메서드를 지원하여, 모든 [Redis 명령어](https://redis.io/commands)를 페이사드에서 직접 호출할 수 있게 합니다. 예를 들어 Redis `GET` 명령어를 페이사드의 `get` 메서드로 호출하는 예시는 다음과 같습니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Redis;

class UserController extends Controller
{
    /**
     * 지정된 사용자의 프로필을 보여줍니다.
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

앞서 말했듯이, Redis의 모든 명령어는 `Redis` 페이사드에서 호출할 수 있습니다. Laravel은 매직 메서드를 사용해 해당 명령을 Redis 서버에 전달합니다. 명령에 인수가 있으면 메서드의 인자로 전달해야 합니다:

```
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는 `Redis` 페이사드의 `command` 메서드를 이용하여 첫 번째 인자로 명령어 이름을, 두 번째 인자로 명령 인수를 배열로 전달할 수도 있습니다:

```
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 파일에서는 여러 Redis 연결(서버)를 정의할 수 있습니다. 특정 Redis 연결에 접근하려면 `Redis` 페이사드의 `connection` 메서드를 사용하세요:

```
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스를 얻으려면 인자를 주지 않고 `connection` 메서드를 호출하면 됩니다:

```
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` 페이사드의 `transaction` 메서드는 Redis의 기본 명령어인 `MULTI`와 `EXEC`를 감싸는 편리한 래퍼입니다. `transaction` 메서드는 클로저를 인자로 받으며, 이 클로저는 Redis 연결 인스턴스를 받습니다. 클로저 내에서 발행된 모든 명령은 하나의 원자적 트랜잭션으로 실행됩니다:

```
use Illuminate\Support\Facades\Redis;

Redis::transaction(function ($redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!NOTE]
> Redis 트랜잭션 내에서는 Redis 연결에서 값을 가져올 수 없습니다. 트랜잭션은 클로저 전체가 명령을 완료한 후 한 번에 실행되는 원자적 작업이라는 점을 기억하세요.

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령을 한 번에 실행하는 또 다른 방법입니다. 하지만 `eval` 메서드는 실행 중 Redis 키 값을 조회하거나 검사할 수 있다는 장점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

처음에는 `eval` 메서드가 다소 복잡해 보일 수 있지만, 간단한 예시로 이해해봅시다. `eval` 메서드는 여러 인수를 받는데, 첫 번째는 실행할 Lua 스크립트(문자열), 두 번째는 스크립트가 조작할 키의 개수(정수), 세 번째부터는 해당 키 이름, 추가 인자가 있다면 그 뒤에 붙입니다.

다음 예시는 카운터를 증가시키고 새 값을 확인하며, 첫 번째 카운터 값이 5를 초과하면 두 번째 카운터도 증가시키는 스크립트입니다. 마지막으로 첫 번째 카운터 값을 반환합니다:

```
$value = Redis::eval(<<<'LUA'
    local counter = redis.call("incr", KEYS[1])

    if counter > 5 then
        redis.call("incr", KEYS[2])
    end

    return counter
LUA, 2, 'first-counter', 'second-counter');
```

> [!NOTE]
> Redis 스크립팅에 대해 더 자세히 알고 싶으면 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 명령어 파이프라이닝 (Pipelining Commands)

때로는 수십 개의 Redis 명령어를 실행할 필요가 있습니다. 각 명령어마다 Redis 서버와 네트워크 왕복을 하지 않도록, `pipeline` 메서드를 사용할 수 있습니다. `pipeline` 메서드는 하나의 클로저를 인자로 받으며, 클로저 내에서 전달받은 Redis 인스턴스로 모든 명령어를 실행할 수 있습니다. 명령은 서버로 한꺼번에 전송되어 네트워크 왕복 횟수를 줄입니다. 명령은 발행된 순서대로 실행됩니다:

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

Laravel은 Redis의 `publish`와 `subscribe` 명령어에 편리한 인터페이스를 제공합니다. 이 명령어들은 특정 "채널"의 메시지를 구독하도록 도와줍니다. 다른 애플리케이션이나 다른 프로그래밍 언어로부터 해당 채널에 메시지를 발행할 수도 있어서 애플리케이션과 프로세스 간의 손쉬운 통신이 가능합니다.

먼저 `subscribe` 메서드를 사용해 채널 리스너를 설정해봅시다. 이 호출은 장시간 실행되는 프로세스이므로 [Artisan 명령어](/docs/{{version}}/artisan) 내에 위치시키는 것이 좋습니다:

```
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Redis;

class RedisSubscribe extends Command
{
    /**
     * 콘솔 명령어의 이름과 서명입니다.
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

이제 `publish` 메서드를 사용해 해당 채널에 메시지를 발행할 수 있습니다:

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

`psubscribe` 메서드를 사용하면 와일드카드 채널을 구독할 수 있어 모든 채널의 메시지를 수신할 때 유용합니다. 채널 이름은 콜백 함수의 두 번째 인수로 전달됩니다:

```
Redis::psubscribe(['*'], function ($message, $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function ($message, $channel) {
    echo $message;
});
```