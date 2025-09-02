# Redis (Redis)

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

[Redis](https://redis.io)은 오픈 소스이며, 고급 키-값 저장소입니다. 종종 데이터 구조 서버(data structure server)라고 불리기도 하는데, 이는 키에 [스트링(strings)](https://redis.io/docs/latest/develop/data-types/strings/), [해시(hashes)](https://redis.io/docs/latest/develop/data-types/hashes/), [리스트(lists)](https://redis.io/docs/latest/develop/data-types/lists/), [셋(sets)](https://redis.io/docs/latest/develop/data-types/sets/), [정렬된 셋(sorted sets)](https://redis.io/docs/latest/develop/data-types/sorted-sets/)과 같은 다양한 데이터 타입을 저장할 수 있기 때문입니다.

Laravel에서 Redis를 사용하기 전에, [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 PECL을 통해 설치하여 사용하는 것을 권장합니다. 이 확장 모듈은 "유저랜드(user-land)" PHP 패키지보다 설치가 좀 더 복잡할 수 있지만, Redis를 많이 사용하는 애플리케이션에서는 더 나은 성능을 기대할 수 있습니다. [Laravel Sail](/docs/12.x/sail)을 사용하는 경우, 해당 확장 모듈은 애플리케이션의 Docker 컨테이너 내에 이미 설치되어 있습니다.

PhpRedis 확장 모듈을 설치할 수 없는 경우, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 순수 PHP로 작성된 Redis 클라이언트이며, 별도의 추가 확장 모듈 없이 사용 가능합니다:

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 할 수 있습니다. 해당 파일에서는 애플리케이션이 사용하는 Redis 서버들이 `redis` 배열 항목으로 정의되어 있습니다:

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

설정 파일에 정의된 각 Redis 서버는 반드시 이름, 호스트, 포트를 가져야 하며, Redis 연결을 나타내는 단일 URL로도 정의할 수 있습니다:

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
#### 연결 방식(scheme) 설정

기본적으로, Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 방식을 사용합니다. 그러나, `scheme` 설정 옵션을 Redis 서버의 설정 배열에 지정하여 TLS / SSL 암호화를 사용할 수도 있습니다:

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

애플리케이션에서 여러 대의 Redis 서버로 이루어진 클러스터를 사용하는 경우, Redis 설정에서 `clusters` 키 아래에 해당 클러스터들을 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로, 직접 `config/database.php` 설정 파일에 추가해야 합니다:

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

기본적으로 Laravel은 `options.cluster` 설정 값이 `redis`로 지정되어 있기 때문에, 네이티브 Redis 클러스터링을 사용합니다. Redis 클러스터링은 장애 발생 시 자동으로 대처할 수 있는 기능이 있어 기본값으로 적합합니다.

또한 Laravel은 Predis를 사용할 때 클라이언트 측 샤딩(client-side sharding)도 지원합니다. 다만, 클라이언트 측 샤딩은 장애 조치 기능이 없으므로, 주로 다른 주요 저장소에서 다시 가져올 수 있는 임시 캐시 데이터에 적합합니다.

네이티브 Redis 클러스터링 대신 클라이언트 측 샤딩을 사용하려면, 애플리케이션의 `config/database.php` 설정 파일에서 `options.cluster` 값 자체를 제거하면 됩니다:

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

Predis 패키지를 통해 Redis와 상호작용하려면, 환경 변수 `REDIS_CLIENT`의 값을 `predis`로 설정해주어야 합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 설정 옵션 외에도, Predis는 각 Redis 서버에 정의할 수 있는 추가 [연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이 추가 설정 옵션을 사용하려면, `config/database.php` 파일의 Redis 서버 설정에 해당 옵션을 추가하면 됩니다:

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

Laravel은 기본적으로 PhpRedis 확장 모듈을 통해 Redis와 통신합니다. Laravel이 어떤 클라이언트로 Redis와 통신할지는 `redis.client` 설정 옵션의 값에 따라 결정되며, 일반적으로 이는 환경 변수 `REDIS_CLIENT`의 값을 반영합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

기본 설정 옵션 외에, PhpRedis는 `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context` 등의 추가 연결 파라미터를 지원합니다. 이 옵션들은 `config/database.php` 설정 파일의 Redis 서버 구성에 자유롭게 추가하여 사용할 수 있습니다:

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
#### 재시도 및 백오프(backoff) 설정

`retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap` 옵션을 활용하면 PhpRedis 클라이언트가 Redis 서버에 재접속을 시도하는 방식을 세세하게 조정할 수 있습니다. 지원되는 백오프 알고리즘은 다음과 같습니다: `default`, `decorrelated_jitter`, `equal_jitter`, `exponential`, `uniform`, `constant`:

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

Redis 연결을 TCP 대신 Unix 소켓으로 구성할 수도 있습니다. 이는 애플리케이션과 동일한 서버에서 Redis 인스턴스로 연결할 때 TCP 오버헤드를 제거하여 성능을 향상시킬 수 있습니다. Unix 소켓을 사용하도록 Redis를 설정하려면, `REDIS_HOST` 환경 변수를 Redis 소켓 경로로 지정하고, `REDIS_PORT` 환경 변수를 `0`으로 설정하세요:

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

PhpRedis 확장 모듈은 다양한 직렬화(serializer) 및 압축(compression) 알고리즘을 지원합니다. 이러한 알고리즘은 Redis 설정의 `options` 배열에서 지정할 수 있습니다:

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

현재 지원되는 직렬화 방식은 다음과 같습니다: `Redis::SERIALIZER_NONE`(기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`

지원되는 압축 알고리즘으로는 `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`가 있습니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

`Redis` [파사드](/docs/12.x/facades)를 통해 다양한 방법으로 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 다이나믹 메서드를 지원하므로, [Redis 커맨드](https://redis.io/commands)를 파사드에 그대로 호출하면 해당 명령이 Redis로 바로 전달됩니다. 아래 예시에서는 Redis의 `GET` 명령을 `Redis` 파사드의 `get` 메서드를 호출하여 사용하고 있습니다:

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

위에서 설명한 것처럼, `Redis` 파사드에서는 Redis의 모든 명령을 호출할 수 있습니다. Laravel은 매직 메서드를 이용해 명령을 Redis 서버에 전달합니다. 특정 Redis 명령에 인수가 필요한 경우, 해당 인수를 파사드의 메서드에 그대로 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는, `Redis` 파사드의 `command` 메서드를 사용하여 명령을 직접 전달할 수도 있습니다. 이 메서드는 첫 번째 인수로 명령어 이름, 두 번째 인수로 값의 배열을 받습니다:

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 다중 Redis 연결 사용하기

애플리케이션의 `config/database.php` 설정 파일에서는 여러 개의 Redis 연결 또는 서버를 정의할 수 있습니다. 특정 Redis 연결에 접속하려면, `Redis` 파사드의 `connection` 메서드를 사용하면 됩니다:

```php
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스를 얻고 싶을 경우, `connection` 메서드를 추가 인수 없이 호출하면 됩니다:

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` 파사드의 `transaction` 메서드는 Redis의 네이티브 `MULTI`와 `EXEC` 명령어를 감싸는 편리한 래퍼입니다. `transaction` 메서드는 클로저를 유일한 인수로 받습니다. 이 클로저에는 Redis 연결 인스턴스가 전달되며, 원하는 모든 명령을 해당 인스턴스에서 실행할 수 있습니다. 클로저 내에서 실행된 모든 Redis 명령은 하나의 원자적(atomic) 트랜잭션으로 처리됩니다:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션을 정의할 때, 트랜잭션 안에서는 Redis 연결에서 값을 가져올 수 없습니다. 트랜잭션은 하나의 원자적 작업으로 실행되며, 전체 클로저 내의 모든 명령이 실행된 후에 실제로 수행되기 때문입니다.

#### Lua 스크립트

`eval` 메서드는 여러 개의 Redis 명령을 하나의 원자적 작업으로 실행할 수 있는 또 다른 방법입니다. `eval` 메서드는 그 과정에서 Redis 키 값을 직접 다루고 검사할 수도 있는 장점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 처음에는 다소 낯설 수 있지만, 기본적인 사용 예시를 들어보겠습니다. 여러 개의 인수를 받는데, 첫 번째는 스크립트(문자열), 두 번째는 스크립트가 다루는 키의 개수(정수), 세 번째부터는 해당 키들의 이름, 마지막으로 스크립트 내에서 접근할 추가 인수들을 나열합니다.

아래 예시에서는 카운터를 증가시키고, 그 값이 5를 초과하면 두 번째 카운터도 증가시키며, 마지막으로 첫 카운터의 값을 반환합니다:

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
> Redis 스크립팅에 대한 자세한 정보는 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 파이프라이닝 명령어 (Pipelining Commands)

때로는 여러 개의 Redis 명령을 한꺼번에 실행해야 할 때가 있습니다. 이때 각 명령마다 매번 Redis 서버로 네트워크 요청을 보내는 대신, `pipeline` 메서드를 사용하면 여러 개의 명령을 한꺼번에 Redis 서버로 전송할 수 있습니다. 이 메서드는 하나의 인수, 즉 Redis 인스턴스를 받는 클로저를 받습니다. 클로저 내에서 모든 명령을 해당 인스턴스에 실행하면, 실행 순서대로 서버에 전송되어 네트워크 요청이 줄어듭니다:

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

Laravel에서는 Redis의 `publish`와 `subscribe` 명령어를 쉽게 사용할 수 있는 인터페이스를 제공합니다. 이 명령어들은 특정 "채널"에서 메시지를 수신(구독)하거나, 다른 애플리케이션 또는 심지어 다른 언어로 작성된 프로그램에서도 해당 채널로 메시지를 발행할 수 있어, 애플리케이션 간 또는 프로세스간 통신이 용이해집니다.

먼저, `subscribe` 메서드를 사용하여 채널 리스너를 설정해보겠습니다. `subscribe` 메서드는 장시간 실행되는 프로세스를 시작하므로, [Artisan 명령어](/docs/12.x/artisan) 내에서 호출하는 것이 좋습니다:

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

이제, `publish` 메서드를 사용해 해당 채널로 메시지를 발행할 수 있습니다:

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

`psubscribe` 메서드를 사용하면 와일드카드 채널에도 구독할 수 있습니다. 이는 모든 채널의 메시지를 받아야 할 때 유용합니다. 채널 이름은 클로저의 두 번째 인수로 전달됩니다:

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```
