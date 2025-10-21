# Redis (Redis)

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Redis와 상호작용](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [파이프라이닝 명령어](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개 (Introduction)

[Redis](https://redis.io)는 오픈 소스의 고급 키-값 저장소입니다. 키에 [스트링](https://redis.io/docs/latest/develop/data-types/strings/), [해시](https://redis.io/docs/latest/develop/data-types/hashes/), [리스트](https://redis.io/docs/latest/develop/data-types/lists/), [셋](https://redis.io/docs/latest/develop/data-types/sets/), [정렬된 셋](https://redis.io/docs/latest/develop/data-types/sorted-sets/) 등 다양한 데이터 구조를 저장할 수 있으므로 흔히 데이터 구조 서버(Data Structure Server)로도 불립니다.

Laravel에서 Redis를 사용하기 전에 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 프로그램을 PECL을 통해 설치해 사용하는 것을 권장합니다. 이 확장 프로그램은 "유저랜드(User-land)" PHP 패키지에 비해 설치가 조금 더 복잡하지만, Redis를 많이 사용하는 애플리케이션에서 더 나은 성능을 낼 수 있습니다. [Laravel Sail](/docs/12.x/sail)을 사용하는 경우, 이 확장 프로그램이 이미 애플리케이션의 Docker 컨테이너에 설치되어 있습니다.

PhpRedis 확장을 설치할 수 없는 경우, Composer를 이용해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 PHP로만 구현된 Redis 클라이언트이며, 별도의 PHP 확장이 필요하지 않습니다:

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 할 수 있습니다. 이 파일 안에는 애플리케이션에서 사용하는 Redis 서버 목록을 담고 있는 `redis` 배열이 있습니다:

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

설정 파일에 정의된 각 Redis 서버에는 이름, 호스트, 포트가 반드시 필요합니다. 단, Redis 연결을 하나의 URL로만 지정하는 경우에는 예외입니다:

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

기본적으로 Redis 클라이언트는 Redis 서버 연결 시 `tcp` 스킴을 사용합니다. 하지만 TLS/SSL 암호화 연결을 사용하려면 Redis 서버 설정 배열에 `scheme` 옵션을 추가하면 됩니다:

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

애플리케이션에서 여러 대의 Redis 서버로 클러스터를 운영하는 경우, Redis 설정에 `clusters` 키 아래에 각 클러스터 정보를 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로, 애플리케이션의 `config/database.php` 파일에 직접 생성해야 합니다:

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

기본적으로 Laravel은 `options.cluster` 설정 값이 `redis`로 되어 있어서 네이티브 Redis 클러스터링을 사용합니다. Redis 클러스터링은 장애 조치(failover)를 효과적으로 처리하기 때문에 기본값으로 사용하기에 적합합니다.

Laravel에서는 Predis를 사용할 때 클라이언트 측 샤딩(Client-side sharding)도 지원합니다. 하지만 클라이언트 측 샤딩은 장애 조치를 처리하지 않으므로, 보통 다른 주요 데이터 저장소에서 가져올 수 있는 임시 캐시 데이터에 적합합니다.

만약 네이티브 Redis 클러스터링 대신 클라이언트 측 샤딩을 사용하려면, 애플리케이션의 `config/database.php` 파일에서 `options.cluster` 설정 값을 제거하면 됩니다:

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

애플리케이션에서 Predis 패키지를 통해 Redis와 상호작용하려면, `REDIS_CLIENT` 환경 변수 값이 `predis`로 설정되어 있어야 합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 설정 옵션 외에 Predis는 각 Redis 서버에 대해 추가로 [연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이러한 추가 설정 옵션을 사용하려면, `config/database.php`에서 해당 Redis 서버 설정에 옵션을 추가하면 됩니다:

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

Laravel은 기본적으로 PhpRedis 확장 프로그램을 사용해 Redis와 통신합니다. Laravel에서 사용할 Redis 클라이언트는 `redis.client` 설정 값(일반적으로 `REDIS_CLIENT` 환경 변수 값)에 의해 결정됩니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

기본 설정 옵션 외에도, PhpRedis에서는 다음과 같은 추가 연결 파라미터를 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context`. 이 옵션들은 모두 `config/database.php` 파일의 Redis 서버 설정에 추가할 수 있습니다:

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
#### 재시도와 백오프(backoff) 설정

`retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap` 옵션은 PhpRedis 클라이언트가 Redis 서버로 재연결을 시도하는 방식을 설정할 때 사용합니다. 지원하는 백오프 알고리즘에는 `default`, `decorrelated_jitter`, `equal_jitter`, `exponential`, `uniform`, `constant`가 있습니다:

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
#### 유닉스 소켓(Unix Socket) 연결

Redis 연결은 TCP 대신 유닉스 소켓을 사용할 수도 있습니다. 같은 서버에 있는 Redis 인스턴스에 연결할 때 TCP 오버헤드를 줄여 성능을 높일 수 있습니다. Redis를 유닉스 소켓으로 사용하려면, `REDIS_HOST` 환경 변수에 Redis 소켓 경로를, `REDIS_PORT` 변수에는 `0`을 설정하세요:

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

PhpRedis 확장 프로그램에서는 다양한 직렬화 및 압축 알고리즘을 사용할 수 있습니다. 이 알고리즘은 Redis 설정의 `options` 배열을 통해 지정할 수 있습니다:

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

현재 지원하는 직렬화 방식에는 `Redis::SERIALIZER_NONE`(기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`이 있습니다.

지원하는 압축 알고리즘에는 `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`가 있습니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용 (Interacting With Redis)

`Redis` [파사드](/docs/12.x/facades)의 다양한 메서드를 호출하여 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하므로, 원하는 [Redis 명령어](https://redis.io/commands)를 파사드에서 직접 호출하면 해당 명령어가 Redis로 바로 전달됩니다. 아래 예제에서는 Redis의 `GET` 명령어를 `Redis` 파사드의 `get` 메서드를 호출하여 사용합니다:

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

위에서 설명한 대로, `Redis` 파사드에서 Redis의 모든 명령어를 호출할 수 있습니다. Laravel은 매직 메서드를 사용하여 이 명령어들을 Redis 서버에 전달합니다. Redis 명령어에 인수가 필요한 경우, 각각의 메서드에 해당 인수를 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또한, `Redis` 파사드의 `command` 메서드를 사용해 명령어를 전달할 수도 있습니다. 첫 번째 인자에는 명령어 이름을, 두 번째 인자에는 값의 배열을 전달하면 됩니다:

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 개의 Redis 연결 사용

애플리케이션의 `config/database.php` 파일에서 여러 개의 Redis 연결(서버)을 정의할 수 있습니다. 특정 Redis 연결을 얻으려면 `Redis` 파사드의 `connection` 메서드를 사용하세요:

```php
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스를 얻으려면 인자를 생략해도 됩니다:

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` 파사드의 `transaction` 메서드는 Redis의 네이티브 `MULTI` 및 `EXEC` 명령어를 쉽게 사용할 수 있게 도와줍니다. 이 메서드는 하나의 클로저를 인자로 받으며, 해당 클로저는 Redis 연결 인스턴스를 전달받아 원하는 명령어들을 실행할 수 있습니다. 클로저 내부에서 실행된 모든 Redis 명령어는 단일 원자적 트랜잭션으로 실행됩니다:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션을 정의할 때는 Redis 연결에서 값을 조회할 수 없습니다. 트랜잭션은 하나의 원자적 연산으로 실행되며, 클로저가 모든 명령어를 실행한 뒤에 실제로 커밋되기 때문입니다.

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령어를 단일 원자적 연산으로 실행할 수 있는 또 다른 방법입니다. 이 메서드는 실행 도중에 Redis 키 값을 직접 다루고 검사할 수 있다는 장점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 사용법이 생소할 수 있지만, 기본 예제로 익숙해질 수 있습니다. 첫 번째 인수로 Lua 스크립트(문자열)를 전달하고, 두 번째 인수로 스크립트가 다루는 키의 개수(정수), 세 번째로는 그 키 이름들, 그리고 필요하다면 추가 인수도 넘길 수 있습니다.

아래 예제에서는 카운터 값을 증가시키고, 그 새 값을 검사하여 만약 첫 번째 카운터 값이 5를 초과하면 두 번째 카운터를 증가시키고, 마지막으로 첫 번째 카운터 값을 반환합니다:

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
> Redis 스크립트에 대해 자세히 알고 싶다면 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하시기 바랍니다.

<a name="pipelining-commands"></a>
### 파이프라이닝 명령어 (Pipelining Commands)

수십 개의 Redis 명령어를 한 번에 실행해야 할 때가 있습니다. 이런 경우 각 명령어마다 Redis 서버로 네트워크 통신이 일어나지 않도록, `pipeline` 메서드를 사용할 수 있습니다. `pipeline` 메서드는 인자로 클로저를 받으며, 이 클로저에서 Redis 인스턴스를 전달받아 여러 명령어를 실행할 수 있습니다. 모든 명령어는 동시에 Redis 서버로 전송되어 네트워크 통신 횟수를 줄일 수 있으며, 명령어 실행 순서는 보장됩니다:

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

Laravel은 Redis의 `publish` 및 `subscribe` 명령어를 쉽고 편리하게 사용할 수 있는 인터페이스를 제공합니다. 이 명령어들은 특정 "채널"에서 메시지를 듣고, 메시지를 발행(publish)하여 여러 애플리케이션이나 프로세스 간 통신을 쉽게 구현할 수 있습니다. 메시지는 다른 애플리케이션에서 또는 다른 프로그래밍 언어로도 해당 채널에 발행할 수 있습니다.

먼저, `subscribe` 메서드를 사용하여 채널 리스너를 설정해 보겠습니다. 이 메서드는 실행 시 장시간 실행되는 프로세스를 시작하므로 [Artisan 명령어](/docs/12.x/artisan)에서 호출하는 것이 좋습니다:

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

이제 `publish` 메서드를 사용해 채널에 메시지를 보낼 수 있습니다:

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

`psubscribe` 메서드를 사용하면 와일드카드 채널에 구독할 수 있습니다. 이를 통해 모든 채널 또는 일부 채널의 모든 메시지를 받아올 수 있습니다. 이 때 채널 이름은 두 번째 인수로 클로저에 전달됩니다:

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```
