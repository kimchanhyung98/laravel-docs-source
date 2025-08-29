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

[Redis](https://redis.io)은 오픈 소스 고급 키-값 저장소입니다. Redis는 키에 [문자열](https://redis.io/docs/latest/develop/data-types/strings/), [해시](https://redis.io/docs/latest/develop/data-types/hashes/), [리스트](https://redis.io/docs/latest/develop/data-types/lists/), [셋](https://redis.io/docs/latest/develop/data-types/sets/), [정렬된 셋](https://redis.io/docs/latest/develop/data-types/sorted-sets/)과 같은 다양한 데이터 구조를 담을 수 있기 때문에 흔히 데이터 구조 서버라고도 불립니다.

Laravel에서 Redis를 사용하기 전에, PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 기능을 설치하고 사용하는 것을 권장합니다. 이 확장 기능은 "유저랜드" PHP 패키지에 비해 설치가 조금 더 복잡하지만, Redis를 많이 사용하는 애플리케이션에서는 더 나은 성능을 얻을 수 있습니다. [Laravel Sail](/docs/11.x/sail)을 사용하고 있다면, 이 확장 기능은 애플리케이션의 Docker 컨테이너에 이미 설치되어 있습니다.

만약 PhpRedis 확장 기능을 설치할 수 없다면, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 추가 확장 기능이 필요 없는, PHP로만 작성된 Redis 클라이언트입니다:

```shell
composer require predis/predis:^2.0
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일 안에는 애플리케이션에서 사용하는 Redis 서버를 정의하는 `redis` 배열이 있습니다:

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

설정 파일에서 정의한 각 Redis 서버는 이름, 호스트, 포트가 필요하며, Redis 연결을 나타내는 단일 URL로도 정의할 수 있습니다:

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
#### 연결 스키마 설정

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스키마를 사용합니다. 하지만 `scheme` 설정 옵션을 Redis 서버 설정 배열에 명시하면 TLS / SSL 암호화를 사용할 수 있습니다:

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

애플리케이션에서 여러 대의 Redis 서버로 클러스터를 구성한다면, Redis 설정에서 `clusters` 키 하위에 해당 클러스터들을 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로, 애플리케이션의 `config/database.php` 설정 파일에 직접 추가해야 합니다:

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

기본적으로, `options.cluster` 설정 값이 `redis`로 지정되어 있기 때문에 Laravel은 네이티브 Redis 클러스터링을 사용합니다. Redis 클러스터링은 장애 발생 시 자동 전환(failover)을 우아하게 처리하므로 매우 좋은 선택입니다.

Laravel은 Predis를 사용할 때 클라이언트 측 샤딩도 지원합니다. 하지만 클라이언트 측 샤딩은 failover를 지원하지 않으므로, 주로 다른 데이터 저장소에서 얻을 수 있는 임시 캐시 데이터에 적합합니다.

네이티브 Redis 클러스터링 대신 클라이언트 측 샤딩을 사용하려면, 애플리케이션의 `config/database.php` 설정 파일에서 `options.cluster` 설정 값을 제거하면 됩니다:

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

애플리케이션에서 Predis 패키지를 통해 Redis와 상호작용하고 싶다면, `REDIS_CLIENT` 환경 변수의 값을 `predis`로 설정해야 합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 설정 옵션 이외에도, Predis는 각 Redis 서버별로 추가 [연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이러한 추가 설정을 적용하려면 `config/database.php` 설정 파일에서 해당 옵션들을 추가하면 됩니다:

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

Laravel은 기본적으로 Redis와 통신할 때 PhpRedis 확장 기능을 사용합니다. Redis와의 통신에 사용할 클라이언트는 `redis.client` 설정 옵션 값에 따라 결정되며, 이 값은 보통 `REDIS_CLIENT` 환경 변수에 의해 설정됩니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

기본 설정 옵션 외에도, PhpRedis는 다음과 같은 연결 파라미터를 추가로 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context`. 이러한 옵션은 `config/database.php` 설정 파일의 Redis 서버 설정에 추가할 수 있습니다:

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
#### PhpRedis 직렬화 및 압축

PhpRedis 확장 기능은 다양한 직렬화(Serializer) 및 압축 알고리즘을 사용할 수 있습니다. 이 설정들은 Redis 설정의 `options` 배열을 통해 지정할 수 있습니다:

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

현재 지원되는 직렬화 방식은 다음과 같습니다: `Redis::SERIALIZER_NONE`(기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`.

지원되는 압축 알고리즘은 다음과 같습니다: `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

여러분은 `Redis` [파사드](/docs/11.x/facades)의 다양한 메서드를 호출하여 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하여, [Redis 명령어](https://redis.io/commands) 어떤 것이든 파사드에 호출하면 해당 명령어가 그대로 Redis로 전달됩니다. 아래 예시에서는 Redis의 `GET` 명령을 `Redis` 파사드의 `get` 메서드를 호출하는 방식으로 사용합니다:

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

앞서 언급한 것처럼, Redis 파사드를 통해 Redis의 모든 명령어를 호출할 수 있습니다. Laravel은 매직 메서드를 사용해, 명령어를 Redis 서버로 전달합니다. 만약 Redis 명령어에 인수가 필요하다면, 파사드 메서드로 해당 인수들을 전달해야 합니다:

```
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또한, `Redis` 파사드의 `command` 메서드를 사용하여 명령어를 직접 서버에 보낼 수도 있습니다. 이 메서드는 첫 번째 인수로 명령어 이름을, 두 번째 인수로 값 배열을 받습니다:

```
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 설정 파일에서는 여러 개의 Redis 연결/서버를 정의할 수 있습니다. `Redis` 파사드의 `connection` 메서드를 사용해 특정 Redis 연결에 접속할 수 있습니다:

```
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스를 얻으려면, 인수 없이 `connection` 메서드를 호출하면 됩니다:

```
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` 파사드의 `transaction` 메서드는 Redis의 `MULTI`, `EXEC` 명령어를 간편하게 감싸주는 래퍼입니다. `transaction` 메서드는 클로저(익명 함수)를 유일한 인수로 받습니다. 이 클로저는 Redis 연결 인스턴스를 매개변수로 받아서, 그 인스턴스에 다양한 명령어를 실행할 수 있습니다. 이 클로저 내에서 실행되는 모든 Redis 명령어들은 하나의 원자적(atomic) 트랜잭션으로 실행됩니다:

```
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]  
> Redis 트랜잭션을 정의할 때, 트랜잭션 내에서는 Redis 연결로부터 값을 얻어올 수 없습니다. 트랜잭션은 하나의 전부 완결된 원자적 작업으로 수행되며, 클로저 내부 명령이 모두 끝나기 전까지 실제로 실행되지 않기 때문입니다.

#### Lua 스크립트

`eval` 메서드를 사용하면 여러 Redis 명령어를 하나의 원자적 작업으로 실행할 수 있습니다. 그리고 `eval` 메서드는 트랜잭션과 달리 Redis 키의 값을 조회하고 조작할 수 있다는 점이 특징입니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 처음에는 다소 어렵게 느껴질 수 있으나, 기본 예제부터 차근차근 익혀보겠습니다. 이 메서드는 여러 인자를 필요로 합니다. 첫 번째는 Lua 스크립트(문자열), 두 번째는 스크립트가 다루는 키의 개수(정수), 세 번째로는 그 키들의 이름입니다. 추가로, 스크립트 내부에서 사용하고자 하는 다른 인자도 이어서 전달할 수 있습니다.

아래 예시는, 카운터를 증가시키고 새 값을 확인한 뒤, 이 값이 5보다 크면 두 번째 카운터도 증가시키는 예입니다. 마지막으로 첫 번째 카운터의 값을 반환합니다:

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
> Redis 스크립팅에 대한 자세한 내용은 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 명령어 파이프라이닝 (Pipelining Commands)

때로는 여러 개의 Redis 명령어를 한꺼번에 실행해야 할 때가 있습니다. 이때, 각각의 명령어마다 서버와 네트워크 통신을 반복하기보다, `pipeline` 메서드를 사용하여 네트워크 왕복 횟수를 줄일 수 있습니다. `pipeline` 메서드는 하나의 클로저(익명 함수)를 인수로 받으며, 이 클로저에 Redis 인스턴스가 전달됩니다. 이 인스턴스에 여러 명령어를 실행하면, 모든 명령어가 한 번에 서버로 전송되고, 입력한 순서대로 처리됩니다:

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

Laravel은 Redis의 `publish`, `subscribe` 명령어를 쉽고 간편하게 사용할 수 있는 인터페이스를 제공합니다. 이 명령어들은 지정된 "채널"에서 메시지를 수신(listen)할 수 있도록 해줍니다. 메시지는 다른 애플리케이션에서, 혹은 다른 프로그래밍 언어로도 해당 채널에 발행할 수 있기에, 애플리케이션과 프로세스 간의 쉬운 통신이 가능합니다.

먼저, `subscribe` 메서드를 사용해 채널 리스너를 설정해봅시다. 이 메서드는 호출과 동시에 장시간 실행되는 프로세스를 시작하므로, 보통 [Artisan 명령어](/docs/11.x/artisan) 내에 작성하게 됩니다:

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

이제 `publish` 메서드를 이용해 해당 채널로 메시지를 발행할 수 있습니다:

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

`psubscribe` 메서드를 사용하면 와일드카드 채널에 구독할 수 있습니다. 이는 모든 채널의 메시지를 받거나, 특정 패턴의 채널 메시지를 받아야 할 때 유용합니다. 클로저의 두 번째 인수로 채널명이 전달됩니다:

```
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```