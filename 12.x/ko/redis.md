# Redis

- [소개](#introduction)
- [구성](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Redis와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [파이프라인 명령어](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개

[Redis](https://redis.io)는 오픈 소스 고급 키-값 저장소입니다. 키에 [문자열](https://redis.io/docs/data-types/strings/), [해시](https://redis.io/docs/data-types/hashes/), [리스트](https://redis.io/docs/data-types/lists/), [셋](https://redis.io/docs/data-types/sets/), [정렬된 셋](https://redis.io/docs/data-types/sorted-sets/)과 같은 다양한 데이터 구조를 저장할 수 있기 때문에 데이터 구조 서버(data structure server)라고 불리기도 합니다.

Laravel에서 Redis를 사용하기 전에 PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 기능을 설치하고 사용하는 것을 권장합니다. 이 확장 프로그램은 일반적인 PHP 패키지보다 설치가 다소 복잡할 수 있지만, Redis를 많이 사용하는 애플리케이션에는 더 나은 성능을 제공할 수 있습니다. [Laravel Sail](/docs/{{version}}/sail)을 사용하고 있다면, 이 확장 기능은 애플리케이션의 Docker 컨테이너에 이미 설치되어 있습니다.

PhpRedis 확장 프로그램을 설치할 수 없는 경우 Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 PHP로 작성된 Redis 클라이언트로, 추가 확장 없이 사용할 수 있습니다:

```shell
composer require predis/predis:^2.0
```

<a name="configuration"></a>
## 구성

애플리케이션의 Redis 설정은 `config/database.php` 구성 파일에서 할 수 있습니다. 이 파일 내에는 애플리케이션이 사용할 Redis 서버를 정의하는 `redis` 배열이 있습니다:

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

구성 파일에 정의된 각 Redis 서버는 Redis 연결을 나타내는 단일 URL을 정의하지 않는 이상, 반드시 이름, 호스트, 포트를 가져야 합니다:

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
#### 연결 스킴(Scheme) 구성

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 그러나 TLS / SSL 암호화를 사용하려면, Redis 서버의 구성 배열에 `scheme` 옵션을 지정할 수 있습니다:

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
### 클러스터

애플리케이션에서 Redis 서버 클러스터를 사용하는 경우, `clusters` 키 아래에 클러스터를 구성해야 합니다. 이 구성 키는 기본적으로 존재하지 않으므로 `config/database.php` 파일에 추가해야 합니다:

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

Laravel은 기본적으로 `options.cluster` 구성 값이 `redis`로 설정되어 있기 때문에 네이티브 Redis 클러스터링을 사용합니다. Redis 클러스터링은 장애 조치(failover) 처리를 우아하게 지원하기 때문에 매우 좋은 기본 선택지입니다.

Laravel은 Predis를 사용할 때 클라이언트 측 셰어딩(client-side sharding)도 지원합니다. 그러나 클라이언트 측 셰어딩은 장애 조치를 제공하지 않으므로, 다른 주요 데이터 저장소에서 사용할 수 있는 일시적인 캐시 데이터에 주로 적합합니다.

네이티브 Redis 클러스터링 대신 클라이언트 측 셰어딩을 사용하고 싶다면, 애플리케이션의 `config/database.php` 파일에서 `options.cluster` 구성 값을 제거하면 됩니다:

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

Predis 패키지를 통해 Redis와 상호작용하고자 한다면 `REDIS_CLIENT` 환경 변수의 값을 `predis`로 설정해야 합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 구성 옵션 외에도 Predis는 각 Redis 서버에 대해 추가적인 [연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이러한 추가 구성 옵션을 사용하려면 `config/database.php` 파일의 Redis 서버 구성에 옵션을 추가하면 됩니다:

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

Laravel은 기본적으로 PhpRedis 확장 기능을 사용해 Redis와 통신합니다. Laravel이 Redis와 통신할 때 사용하는 클라이언트는 `redis.client` 구성 옵션의 값으로 결정되며, 이 값은 보통 `REDIS_CLIENT` 환경 변수의 값을 따릅니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

기본 옵션 외에도 PhpRedis는 다음과 같은 추가 연결 파라미터를 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context`. 이 옵션들 중 원하는 것을 `config/database.php` 구성 파일에 추가할 수 있습니다:

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
#### Unix 소켓 연결

Redis 연결은 TCP 대신 Unix 소켓을 사용하도록 설정할 수도 있습니다. 소켓을 통해 애플리케이션과 동일한 서버 상의 Redis 인스턴스에 접속할 때 TCP 오버헤드를 제거하여 성능을 향상시킬 수 있습니다. Unix 소켓을 사용하려면 `REDIS_HOST` 환경 변수에 Redis 소켓 경로를, `REDIS_PORT`에는 `0`을 지정합니다:

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

PhpRedis 확장 기능은 여러 종류의 직렬화 및 압축 알고리즘도 지원합니다. 이 알고리즘들은 Redis 구성의 `options` 배열에서 지정할 수 있습니다:

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

현재 지원되는 직렬화기는 `Redis::SERIALIZER_NONE`(기본), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK` 등입니다.

지원되는 압축 알고리즘에는 `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`가 포함됩니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기

`Redis` [파사드](/docs/{{version}}/facades)의 다양한 메서드를 호출하여 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하므로, [Redis 명령어](https://redis.io/commands)를 파사드에서 직접 호출하면 해당 명령이 바로 Redis로 전달됩니다. 다음 예시에서는 `Redis` 파사드의 `get` 메서드를 호출하여 Redis의 `GET` 명령어를 사용합니다:

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

위에서 설명한 것처럼, 모든 Redis 명령은 `Redis` 파사드에서 호출할 수 있습니다. Laravel은 매직 메서드로 명령어를 Redis 서버로 넘깁니다. Redis 명령어에 인자가 필요한 경우, 해당 값을 파사드의 메서드 인자로 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는, `Redis` 파사드의 `command` 메서드를 사용해서 명령어를 서버에 전달할 수 있으며, 첫 번째 인자로 명령어 이름, 두 번째 인자로 값 배열을 넘깁니다:

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용

애플리케이션의 `config/database.php` 파일에서 여러 Redis 연결/서버를 정의할 수 있습니다. 특정 Redis 연결에 접속하려면, `Redis` 파사드의 `connection` 메서드를 사용하면 됩니다:

```php
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스를 얻으려면 추가 인자 없이 `connection` 메서드를 호출하세요:

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션

`Redis` 파사드의 `transaction` 메서드는 Redis의 `MULTI`, `EXEC` 명령어를 감싸는 편리한 래퍼를 제공합니다. `transaction` 메서드는 하나의 클로저를 인자로 받으며, 이 클로저는 Redis 연결 인스턴스를 받아 필요한 명령을 자유롭게 실행할 수 있습니다. 클로저 내에서 실행되는 모든 Redis 명령은 하나의 원자적 트랜잭션으로 실행됩니다:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션을 정의할 때, Redis 연결에서 값을 조회할 수 없습니다. 트랜잭션은 하나의 원자적 연산으로 처리되며, 클로저 내 모든 명령이 완료된 뒤에 실행됨을 기억하세요.

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령어를 하나의 원자적 연산으로 실행하는 또 다른 방법을 제공합니다. `eval` 메서드는 실행 중에 Redis 키 값에 접근 및 검사할 수 있는 이점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 여러 인자를 받습니다. 먼저 Lua 스크립트(문자열), 두 번째로 스크립트에서 사용하는 키의 수(정수), 세 번째로 그 키들의 이름, 그 뒤로는 스크립트 내에서 사용할 추가 인자를 전달합니다.

다음 예시는 카운터를 증가시키고, 그 새로운 값을 검사하여 카운터가 5보다 크면 두 번째 카운터도 증가시킨 후, 첫 번째 카운터의 값을 반환하는 간단한 예시입니다:

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
> Redis 스크립팅에 대한 자세한 내용은 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 파이프라인 명령어

수십 개의 Redis 명령을 실행해야 하는 경우도 있습니다. 각 명령마다 네트워크를 통해 Redis 서버와 통신하지 않고, `pipeline` 메서드를 사용할 수 있습니다. `pipeline` 메서드는 하나의 클로저를 인자로 받으며, 이 클로저는 Redis 인스턴스를 전달받습니다. 이 인스턴스에 여러 명령을 연속적으로 보내면, 모든 명령이 한 번에 Redis 서버로 전송되어 네트워크 왕복 횟수를 줄일 수 있습니다. 명령의 실행 순서는 호출한 순서를 따릅니다:

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

Laravel은 Redis의 `publish`, `subscribe` 명령에 대한 편리한 인터페이스를 제공합니다. 이 명령어는 주어진 "채널"의 메시지를 청취할 수 있도록 하며, 다른 애플리케이션이나 심지어 다른 언어에서도 해당 채널로 메시지를 보낼 수 있기 때문에 응용프로그램 및 프로세스 간 통신이 용이해집니다.

먼저 `subscribe` 메서드를 사용해 채널 리스너를 설정해보겠습니다. subscribe 메서드는 장시간 실행 프로세스이므로, [Artisan 커맨드](/docs/{{version}}/artisan)에서 호출하는 것이 일반적입니다:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Redis;

class RedisSubscribe extends Command
{
    /**
     * 콘솔 명령의 이름 및 시그니처
     *
     * @var string
     */
    protected $signature = 'redis:subscribe';

    /**
     * 콘솔 명령 설명
     *
     * @var string
     */
    protected $description = 'Redis 채널 구독';

    /**
     * 콘솔 명령 실행
     */
    public function handle(): void
    {
        Redis::subscribe(['test-channel'], function (string $message) {
            echo $message;
        });
    }
}
```

이제 `publish` 메서드를 사용해 해당 채널로 메시지를 보낼 수 있습니다:

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

`psubscribe` 메서드를 이용하면 와일드카드 채널 구독이 가능합니다. 이 기능은 모든 채널의 메시지를 수신해야 할 때 유용합니다. 채널 이름은 두 번째 인자로 클로저에 전달됩니다:

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```
