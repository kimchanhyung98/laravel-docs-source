# Redis (Redis)

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Redis와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [파이프라인 명령어](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개 (Introduction)

[Redis](https://redis.io)은 오픈 소스의 고급 key-value 저장소입니다. 키는 [문자열](https://redis.io/docs/latest/develop/data-types/strings/), [해시](https://redis.io/docs/latest/develop/data-types/hashes/), [리스트](https://redis.io/docs/latest/develop/data-types/lists/), [셋](https://redis.io/docs/latest/develop/data-types/sets/), [정렬된 셋](https://redis.io/docs/latest/develop/data-types/sorted-sets/) 등 다양한 자료구조를 가질 수 있기 때문에 데이터 구조 서버(data structure server)라고도 불립니다.

Laravel과 Redis를 함께 사용하려면, [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 PECL을 통해 설치해서 사용하는 것을 권장합니다. 이 확장 모듈은 PHP로만 구현된 "user-land" 패키지에 비해 설치가 더 복잡하지만, Redis를 빈번하게 사용하는 애플리케이션에서 더 나은 성능을 제공할 수 있습니다. [Laravel Sail](/docs/12.x/sail)을 사용하는 경우, 이 확장 모듈은 이미 애플리케이션의 Docker 컨테이너에 설치되어 있습니다.

PhpRedis 확장 모듈 설치가 어려운 경우, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 순수 PHP로 구현된 Redis 클라이언트로, 별도의 추가 확장 모듈 없이 사용할 수 있습니다:

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일을 통해 할 수 있습니다. 이 파일 내의 `redis` 배열에서 애플리케이션에서 사용하는 Redis 서버들을 정의하게 됩니다:

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

설정 파일에 정의된 각 Redis 서버는 이름, 호스트, 포트 정보를 가져야 합니다. 단, 단일 URL로 연결 정보를 표현할 경우에는 예외입니다:

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
#### 연결 스킴(Scheme) 설정

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 하지만, 연결 설정 배열에 `scheme` 옵션을 추가하여 TLS / SSL 암호화를 사용할 수도 있습니다:

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

애플리케이션에서 여러 Redis 서버로 구성된 클러스터를 사용하는 경우, Redis 설정에 `clusters` 키를 추가로 정의해야 합니다. 기본적으로 이 설정 키는 존재하지 않으므로, 직접 `config/database.php` 파일에 추가해야 합니다:

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

기본적으로 Laravel은 `options.cluster` 설정 값이 `redis`로 지정되어 있으므로, 네이티브 Redis 클러스터링을 사용합니다. Redis 클러스터링은 장애 조치(failover)를 원활하게 처리하므로 매우 좋은 선택지입니다.

Predis를 사용할 경우, 클라이언트 사이드 셰어딩(sharding)도 지원합니다. 단, 클라이언트 사이드 셰어딩은 장애 조치를 지원하지 않기 때문에, 일반적으로 다른 주요 데이터 저장소에서 얻을 수 있는 일시적인 캐시 데이터 용도로 가장 적합합니다.

네이티브 Redis 클러스터링 대신 클라이언트 사이드 셰어딩을 사용하려면, 설정 파일의 `options.cluster` 값을 제거하면 됩니다:

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

애플리케이션에서 Predis 패키지를 통해 Redis에 접근하려면, `REDIS_CLIENT` 환경 변수의 값을 `predis`로 설정해야 합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 설정 옵션 외에도, Predis는 각 Redis 서버에 대해 추가적인 [연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 추가 옵션을 사용하려면, 설정 파일에서 해당 옵션을 Redis 서버 설정에 추가하면 됩니다:

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

기본적으로 Laravel은 Redis와 통신할 때 PhpRedis 확장 모듈을 사용합니다. Laravel이 어떤 클라이언트를 사용할지는 일반적으로 `REDIS_CLIENT` 환경 변수의 값을 반영하는 `redis.client` 설정 값에 따라 결정됩니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

기본 설정 옵션 외에도, PhpRedis는 다음과 같은 추가 연결 파라미터들을 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context`. 이러한 옵션들을 설정 파일 내 Redis 서버 설정에 추가하여 사용할 수 있습니다:

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

Redis는 TCP 대신 유닉스 소켓을 이용해 연결하도록 설정할 수도 있습니다. 같은 서버 내에 있는 Redis 인스턴스에 연결할 경우, TCP 오버헤드가 사라져 더 나은 성능을 기대할 수 있습니다. 유닉스 소켓을 사용하려면, `REDIS_HOST` 환경 변수에 Redis 소켓 경로를, `REDIS_PORT` 변수에는 `0`을 지정하세요:

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

PhpRedis 확장 모듈은 다양한 직렬화(serializer) 및 압축(compression) 알고리즘을 사용할 수 있도록 설정할 수 있습니다. 이 알고리즘들은 Redis 설정의 `options` 배열에서 지정할 수 있습니다:

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

현재 지원되는 직렬화 옵션은 다음과 같습니다: `Redis::SERIALIZER_NONE`(기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`.

지원되는 압축 알고리즘은 다음과 같습니다: `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

`Redis` [파사드](/docs/12.x/facades)의 다양한 메서드를 호출하여 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 다이내믹 메서드(dynamically named methods)를 지원하므로, [Redis 명령어](https://redis.io/commands)를 바로 파사드에 호출하면 해당 명령이 곧장 Redis로 전달됩니다. 예를 들어, 아래는 `Redis` 파사드의 `get` 메서드를 호출하여 Redis의 `GET` 명령어를 사용하는 예시입니다:

```php
<?php

namespace App\Http\Controllers;

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

위에서 설명했듯이, Redis의 모든 명령어를 `Redis` 파사드에 메서드로 호출할 수 있습니다. Laravel은 매직 메서드(magic methods)를 이용하여 해당 명령을 Redis 서버에 전달합니다. 만약 Redis 명령이 인수를 필요로 한다면, 해당 인수들을 파사드의 메서드에 그대로 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또한, `Redis` 파사드의 `command` 메서드를 사용해 명령어를 서버로 전송할 수 있습니다. 이 메서드는 첫 번째 인수로 명령어 이름을, 두 번째 인수로 값의 배열을 받습니다:

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

`config/database.php` 파일에서 여러 개의 Redis 연결/서버를 정의할 수 있습니다. 특정 Redis 연결에 접근하려면 `Redis` 파사드의 `connection` 메서드를 사용하면 됩니다:

```php
$redis = Redis::connection('connection-name');
```

기본 Redis 연결을 얻으려면 추가 인수 없이 `connection` 메서드를 호출하면 됩니다:

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` 파사드의 `transaction` 메서드는 Redis의 기본 `MULTI` 및 `EXEC` 명령을 손쉽게 감쌀 수 있도록 도와줍니다. `transaction` 메서드는 하나의 클로저(익명 함수)를 인수로 받습니다. 이 클로저는 Redis 연결 인스턴스를 받아서, 그 인스턴스에 원하는 모든 명령을 실행할 수 있도록 합니다. 클로저 내에서 실행된 모든 명령은 하나의 원자적(atomic) 트랜잭션으로 실행됩니다:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션을 정의할 때는 트랜잭션 내에서 Redis 연결로부터 값을 조회(get)할 수 없습니다. 트랜잭션은 완전히 원자적(atomic)으로 실행되며, 클로저 내부의 모든 명령이 실행된 후에야 실제로 트랜잭션이 실행되기 때문입니다.

#### Lua 스크립트

`eval` 메서드를 사용하면 한 번에 여러 개의 Redis 명령을 원자적으로 실행할 수 있습니다. 특히 `eval` 메서드는 실행 중에 Redis 키 값을 확인하거나 수정하면서 상호작용할 수 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 몇 개의 인수를 받습니다. 첫 번째는 Lua 스크립트(문자열), 두 번째는 스크립트가 다루는 키의 개수(정수), 세 번째는 키 이름들, 마지막으로는 스크립트에서 접근할 수 있는 추가적인 인자들입니다.

예를 들어, 아래는 카운터 값을 증가시키고, 그 값이 5보다 크면 다른 카운터도 함께 증가시키며, 첫 번째 카운터의 값을 반환하는 스크립트입니다:

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
> Redis 스크립트에 대한 더 자세한 내용은 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 파이프라인 명령어 (Pipelining Commands)

때때로 수십 개의 Redis 명령을 실행해야 하는 경우가 있습니다. 각 명령마다 Redis 서버에 네트워크 요청을 보내는 대신, `pipeline` 메서드를 이용해 모든 명령을 한 번에 서버로 전송할 수 있습니다. `pipeline` 메서드는 하나의 클로저(익명 함수)를 인수로 받으며, 이 클로저에서 모든 명령을 실행하면 명령들이 한 번에 순서대로 전송됩니다. 결과적으로 서버로의 네트워크 트립(왕복)이 대폭 줄어듭니다:

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
## Pub / Sub

Laravel은 Redis의 `publish`와 `subscribe` 명령을 위한 간편한 인터페이스를 제공합니다. 이 명령어들은 지정된 "채널"의 메시지를 수신 대기(listen)하게 해 주며, 다른 애플리케이션이나 심지어 다른 프로그래밍 언어를 사용해서도 채널로 메시지를 발행(publish)할 수 있습니다. 이를 통해 애플리케이션과 프로세스 사이의 손쉬운 통신이 가능합니다.

먼저, `subscribe` 메서드를 이용해 채널 리스너를 설정해 보겠습니다. 오래 실행되는 작업이므로 이 코드는 [Artisan 명령어](/docs/12.x/artisan) 내에 두는 것이 좋습니다:

```php
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

이제 `publish` 메서드를 통해 채널에 메시지를 발행할 수 있습니다:

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

`psubscribe` 메서드를 이용하면 전체 채널 또는 특정 패턴을 가진 채널에 와일드카드 방식으로 구독할 수 있습니다. 모든 채널의 메시지를 수신하거나, 특정 패턴의 채널에만 반응해야 할 때 유용합니다. 클로저의 두 번째 인수로 채널 이름이 전달됩니다:

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```
