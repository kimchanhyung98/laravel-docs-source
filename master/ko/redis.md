# Redis (Redis)

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Redis와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [명령어 파이프라인 처리](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개 (Introduction)

[Redis](https://redis.io)은 오픈 소스로 제공되는 고급 키-값 저장소입니다. 종종 데이터 구조 서버로 불리기도 하는데, 이는 키에 [문자열](https://redis.io/docs/latest/develop/data-types/strings/), [해시](https://redis.io/docs/latest/develop/data-types/hashes/), [리스트](https://redis.io/docs/latest/develop/data-types/lists/), [집합](https://redis.io/docs/latest/develop/data-types/sets/), [정렬된 집합](https://redis.io/docs/latest/develop/data-types/sorted-sets/) 등 다양한 자료 구조를 저장할 수 있기 때문입니다.

Laravel에서 Redis를 사용하기 전에, PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 설치해 사용하는 것을 권장합니다. 이 확장 모듈은 일반적인 PHP 패키지(user-land)보다 설치가 조금 더 복잡하지만, Redis를 많이 사용하는 애플리케이션에서는 더 나은 성능을 낼 수 있습니다. 만약 [Laravel Sail](/docs/master/sail)을 사용한다면, 이 확장 모듈은 이미 애플리케이션의 Docker 컨테이너에 설치되어 있습니다.

PhpRedis 확장 모듈 설치가 어려운 환경이라면, Composer를 통해 `predis/predis` 패키지를 설치해 사용할 수도 있습니다. Predis는 PHP만으로 작성된 Redis 클라이언트로, 별도의 추가 확장 모듈이 필요하지 않습니다.

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 제어할 수 있습니다. 이 파일 내에는 애플리케이션에서 사용하는 Redis 서버 정보를 담고 있는 `redis` 배열이 존재합니다.

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

설정 파일에 정의한 각 Redis 서버는 이름, 호스트, 포트를 반드시 가지고 있어야 하며, 혹은 하나의 URL로 Redis 연결을 표현할 수도 있습니다.

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

기본적으로 Redis 클라이언트는 Redis 서버에 접속할 때 `tcp` 스킴을 사용합니다. 하지만 Redis 서버 설정 배열에서 `scheme` 항목을 지정하면 TLS / SSL 암호화 연결도 사용할 수 있습니다.

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

애플리케이션이 여러 대의 Redis 서버로 이루어진 클러스터를 사용하는 경우, Redis 설정의 `clusters` 키에 클러스터 정보를 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로, 직접 `config/database.php` 설정 파일에 추가해야 합니다.

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

기본적으로 Laravel은 `options.cluster` 설정 값이 `redis`로 지정되어 있기 때문에, 네이티브 Redis 클러스터링을 사용합니다. Redis 클러스터링은 장애 조치(failover)를 자동으로 처리하므로, 기본 설정으로 적합한 옵션입니다.

Laravel은 또한 Predis 사용 시 클라이언트 측 샤딩(client-side sharding)도 지원합니다. 단, 클라이언트 측 샤딩은 장애 조치가 지원되지 않으므로, 주로 다른 주요 데이터 저장소에서 얻을 수 있는 임시 캐시 데이터에 적합합니다.

네이티브 Redis 클러스터링 대신 클라이언트 측 샤딩을 사용하고 싶다면, 애플리케이션의 `config/database.php`에서 `options.cluster` 설정 값을 제거하면 됩니다.

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

Predis 패키지를 통해 Redis와 상호작용하려면, `REDIS_CLIENT` 환경 변수의 값을 `predis`로 설정해야 합니다.

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 설정 외에도, Predis는 각 Redis 서버에 대해 추가적인 [연결 매개변수(connection parameters)](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이 추가 설정값들은 애플리케이션의 `config/database.php` 파일의 Redis 서버 설정 배열에 직접 추가해 사용할 수 있습니다.

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

Laravel은 기본적으로 Redis와 통신할 때 PhpRedis 확장 모듈을 사용합니다. Laravel에서 어떤 Redis 클라이언트를 사용할지는 `redis.client` 설정 옵션 값에 따라 결정되며, 일반적으로 이는 `REDIS_CLIENT` 환경 변수의 값을 따릅니다.

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

기본 설정 외에도, PhpRedis는 다음의 추가 연결 옵션을 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context`. 이 중 필요한 옵션을 `config/database.php`의 Redis 서버 설정에 직접 추가해 사용할 수 있습니다.

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

<a name="retry-and-backoff-configuration"></a>
#### 재시도 및 Backoff 설정

`retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap` 옵션을 사용하여 PhpRedis 클라이언트가 Redis 서버에 재접속을 시도할 때의 동작을 세부적으로 설정할 수 있습니다. 지원되는 backoff 알고리즘은 다음과 같습니다: `default`, `decorrelated_jitter`, `equal_jitter`, `exponential`, `uniform`, `constant`.

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'max_retries' => env('REDIS_MAX_RETRIES', 3),
    'backoff_algorithm' => env('REDIS_BACKOFF_ALGORITHM', 'decorrelated_jitter'),
    'backoff_base' => env('REDIS_BACKOFF_BASE', 100),
    'backoff_cap' => env('REDIS_BACKOFF_CAP', 1000),
],
```

<a name="unix-socket-connections"></a>
#### Unix 소켓 연결

Redis 연결은 TCP 대신 Unix 소켓을 사용하도록 설정할 수도 있습니다. 이 방식은 같은 서버 내에서 Redis 인스턴스와 연결할 때 TCP 오버헤드를 제거하여 성능을 높일 수 있습니다. Redis가 Unix 소켓을 사용하도록 하려면, `REDIS_HOST` 환경 변수를 Redis 소켓의 경로로, `REDIS_PORT` 변수는 `0`으로 설정하면 됩니다.

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축 설정

PhpRedis 확장 모듈은 다양한 직렬화(serialization) 및 압축(compression) 알고리즘을 사용할 수 있습니다. 이 알고리즘들은 Redis 설정의 `options` 배열에서 지정합니다.

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

현재 지원되는 직렬화 방식은 다음과 같습니다: `Redis::SERIALIZER_NONE`(기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`.

지원되는 압축 알고리즘으로는 `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`가 있습니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

[facade](/docs/master/facades)인 `Redis`를 통해 다양한 메서드로 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하므로, [Redis의 모든 명령어](https://redis.io/commands)를 파사드에서 직접 호출하면 해당 명령어가 Redis로 전달됩니다. 예를 들어, 아래 예시는 Redis의 `GET` 명령어를 `Redis` 파사드의 `get` 메서드로 호출합니다.

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

위에서 설명했듯이, Redis의 거의 모든 명령어를 `Redis` 파사드를 통해 호출할 수 있습니다. Laravel은 매직 메서드(magic method)를 활용하여 명령어를 Redis 서버에 전달합니다. Redis 명령어에 인수가 필요한 경우, 해당 메서드에 인수를 넘기면 됩니다.

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는, `Redis` 파사드의 `command` 메서드를 활용해 명령어 이름과 값을 배열로 전달할 수도 있습니다.

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 설정 파일에서는 여러 개의 Redis 연결(서버)을 정의할 수 있습니다. 특정 Redis 연결을 사용하려면 `Redis` 파사드의 `connection` 메서드에 해당 연결명을 지정해 인스턴스를 얻을 수 있습니다.

```php
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스는 인수를 추가로 전달하지 않고 `connection` 메서드를 호출하면 됩니다.

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` 파사드의 `transaction` 메서드는 Redis의 기본 `MULTI`와 `EXEC` 명령을 감싼 편리한 래퍼를 제공합니다. 이 메서드는 하나의 인수로 클로저(익명 함수)를 받으며, 이 클로저는 Redis 연결 인스턴스를 인자로 전달받아 다양한 명령을 실행할 수 있습니다. 이 클로저 내에서 실행된 모든 Redis 명령은 하나의 원자적(atomic) 트랜잭션으로 처리됩니다.

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션을 정의할 때, 트랜잭션 내에서 Redis로부터 값을 가져올 수 없습니다. 참고로, 트랜잭션은 전체 클로저의 명령이 모두 실행되고 나서 한 번에 실행되므로, 중간에 값을 읽어올 수 없습니다.

#### Lua 스크립트

`eval` 메서드는 여러 개의 Redis 명령을 하나의 원자적(atomic) 작업으로 실행할 수 있는 또 다른 방법입니다. 추가로, `eval` 메서드는 실행 도중 Redis의 키 값을 읽거나 조작할 수 있는 장점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성합니다.

`eval` 메서드는 여러 인수를 받습니다. 첫 번째로 Lua 스크립트(문자열)를 전달하고, 두 번째로 스크립트가 조작할 키의 개수(정수), 세 번째로 그 키의 이름들을 나열합니다. 이후 필요하다면 스크립트 내에서 사용될 추가 인수들도 전달할 수 있습니다.

예를 들어, 특정 카운터를 증가시키고, 그 새 값을 확인하여 해당 값이 5보다 크면 두 번째 카운터도 증가시킵니다. 마지막엔 첫 번째 카운터의 값을 반환합니다.

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
> Redis 스크립팅에 대한 더 자세한 내용은 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하시기 바랍니다.

<a name="pipelining-commands"></a>
### 명령어 파이프라인 처리 (Pipelining Commands)

때때로 수십 개의 Redis 명령어를 연속으로 실행해야 할 때가 있습니다. 이런 경우 각각의 명령마다 Redis 서버와 네트워크 통신을 반복하는 대신, `pipeline` 메서드를 사용하면 한 번의 네트워크 요청으로 여러 명령어를 동시에 보낼 수 있습니다. `pipeline` 메서드는 하나의 인수(클로저)를 받으며, 클로저의 인자로 전달되는 Redis 인스턴스를 사용해 원하는 모든 명령을 실행할 수 있습니다. 모든 명령은 실행 순서대로 처리됩니다.

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

Laravel에서는 Redis의 `publish` 및 `subscribe` 명령을 편리하게 사용할 수 있게 인터페이스를 제공합니다. 이 명령어들은 특정 "채널"에서 메시지를 주고받을 수 있도록 해주며, 다른 애플리케이션 또는 다른 프로그래밍 언어로 채널에 메시지를 publish/push할 수도 있어, 애플리케이션과 프로세스 간의 간편한 통신이 가능합니다.

먼저, `subscribe` 메서드를 사용해 채널 리스너를 만들어봅니다. 이 메서드는 실행이 길게 지속되기 때문에 [Artisan 명령어](/docs/master/artisan) 내에 코드를 작성하는 것이 적절합니다.

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

이제 `publish` 메서드를 사용해 해당 채널에 메시지를 발행(publish)할 수 있습니다.

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
#### 와일드카드 구독 (Wildcard Subscriptions)

`psubscribe` 메서드를 사용하면 와일드카드 패턴의 채널을 구독할 수 있습니다. 모든 채널의 메시지를 수신하거나, 특정 패턴에 해당하는 채널을 한 번에 구독하는 데 유용합니다. 구독 시, 채널명이 클로저의 두 번째 인자로 전달됩니다.

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```