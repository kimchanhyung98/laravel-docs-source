# 레디스 (Redis)

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [레디스와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [명령어 파이프라이닝](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개

[Redis](https://redis.io)는 오픈 소스이며, 고급 기능을 제공하는 키-값(key-value) 저장소입니다. 보통 키 안에 [문자열](https://redis.io/docs/data-types/strings/), [해시](https://redis.io/docs/data-types/hashes/), [리스트](https://redis.io/docs/data-types/lists/), [셋](https://redis.io/docs/data-types/sets/), [정렬된 셋](https://redis.io/docs/data-types/sorted-sets/) 등 다양한 자료구조를 저장할 수 있기 때문에 데이터 구조 서버라고도 불립니다.

라라벨에서 Redis를 사용하기 전에, PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 설치해서 사용하시길 권장합니다. 이 확장 모듈은 일반적인 "user-land" PHP 패키지에 비해 설치 과정이 다소 복잡할 수 있지만, Redis를 많이 사용하는 애플리케이션에서는 더 나은 성능을 기대할 수 있습니다. 만약 [Laravel Sail](/docs/12.x/sail)을 사용 중이라면, 이 확장 모듈이 애플리케이션의 Docker 컨테이너에 이미 설치되어 있습니다.

PhpRedis 확장 모듈을 설치할 수 없는 경우, Composer를 통해 `predis/predis` 패키지를 설치하여 사용할 수 있습니다. Predis는 PHP로 작성된 Redis 클라이언트로, 별도의 확장 모듈 설치가 필요하지 않습니다.

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 설정

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 할 수 있습니다. 이 파일에는 애플리케이션에서 사용할 Redis 서버 정보를 담고 있는 `redis` 배열이 있습니다.

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

설정 파일에 정의된 각 Redis 서버는 반드시 이름, 호스트, 포트 정보를 가지고 있어야 합니다. 다만 Redis 연결을 하나의 URL로 지정할 수도 있습니다.

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
#### 연결 스킴(scheme) 설정

기본적으로 Redis 클라이언트는 Redis 서버에 접속할 때 `tcp` 스킴을 사용합니다. 하지만, Redis 서버의 설정 배열에 `scheme` 옵션을 지정하면 TLS / SSL 암호화를 적용할 수도 있습니다.

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

애플리케이션에서 여러 대의 Redis 서버로 구성된 클러스터를 사용할 경우, Redis 설정 배열에 `clusters` 키를 직접 만들어 클러스터 정보를 정의해야 합니다. 이 설정 키는 기본값에는 없으므로 `config/database.php` 파일에 직접 추가해야 합니다.

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

라라벨은 기본적으로 `options.cluster` 설정값이 `redis`로 되어 있으므로 네이티브 Redis 클러스터링을 사용합니다. Redis 클러스터링은 자동 장애 조치(failover)를 잘 처리하기 때문에 기본값으로 사용하기에 적합합니다.

라라벨은 Predis를 사용할 때 클라이언트 사이드 샤딩도 지원합니다. 다만 클라이언트 사이드 샤딩은 장애 조치가 지원되지 않으므로, 다른 원본 데이터 저장소에서 데이터를 다시 받아올 수 있는 임시 캐시 데이터(트랜지언트 데이터)에 주로 적합합니다.

네이티브 Redis 클러스터링 대신 클라이언트 사이드 샤딩을 사용하려면, 애플리케이션의 `config/database.php` 파일에서 `options.cluster` 설정을 제거하면 됩니다.

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

Redis와 상호작용하는 클라이언트를 Predis로 설정하려면, 환경 변수 `REDIS_CLIENT` 값을 `predis`로 지정하세요.

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 설정 외에도, Predis는 각 Redis 서버마다 추가적인 [연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이 옵션을 사용하려면 애플리케이션의 `config/database.php` 파일 Redis 서버 설정에 원하는 옵션을 추가하시면 됩니다.

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

라라벨은 기본적으로 PhpRedis 확장 모듈을 사용해서 Redis와 통신합니다. 라라벨이 어떤 Redis 클라이언트를 사용할지는 `redis.client` 설정값에 의해 결정되며, 보통 `REDIS_CLIENT` 환경 변수의 값을 따릅니다.

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

기본 설정 외에도, PhpRedis는 다음의 추가 연결 옵션들을 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context`. 이런 옵션들을 원한다면 `config/database.php` 파일의 Redis 서버 설정에 추가할 수 있습니다.

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

Redis 연결을 TCP 대신 유닉스 소켓을 사용하도록 설정할 수도 있습니다. 같은 서버 내에서 애플리케이션과 Redis 인스턴스 간 연결이라면, TCP 오버헤드를 없애 성능이 더 좋아질 수 있습니다. 유닉스 소켓을 사용하려면 `REDIS_HOST` 환경 변수에 Redis 소켓의 경로를 지정하고, `REDIS_PORT` 환경 변수는 `0`으로 설정하세요.

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

PhpRedis 확장 모듈은 다양한 직렬화(serialize) 방식과 압축(compression) 알고리즘을 사용할 수 있습니다. 이 설정들은 Redis 설정의 `options` 배열에서 지정할 수 있습니다.

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

지원되는 압축 알고리즘은 다음과 같습니다: `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`

<a name="interacting-with-redis"></a>
## 레디스와 상호작용하기

[파사드](/docs/12.x/facades)인 `Redis`를 통해 Redis와 다양한 방식으로 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하기 때문에, 거의 모든 [Redis 명령어](https://redis.io/commands)를 파사드를 통해 호출하면 해당 명령어가 직접 Redis로 전달됩니다. 아래 예시에서는 Redis의 `GET` 명령을 `Redis` 파사드의 `get` 메서드로 호출합니다.

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

위에서 본 것처럼, Redis의 어떠한 명령어도 `Redis` 파사드를 통해 호출할 수 있습니다. 라라벨은 매직 메서드(magic method)를 활용해 명령어를 Redis 서버로 전달합니다. 만약 명령어가 인수를 필요로 한다면 해당 메서드에 인수를 전달하면 됩니다.

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는, `Redis` 파사드의 `command` 메서드를 사용해 명령어를 전달할 수도 있습니다. 이 메서드는 첫 번째 인수로 명령어명을, 두 번째 인수로 값들의 배열을 받습니다.

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

`config/database.php` 설정 파일을 이용하면 여러 개의 Redis 연결 또는 서버를 정의할 수 있습니다. 특정 Redis 연결을 사용하려면 `Redis` 파사드의 `connection` 메서드에 연결 이름을 넘겨주면 됩니다.

```php
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스를 얻고 싶다면 인수 없이 `connection` 메서드를 호출하면 됩니다.

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션

`Redis` 파사드의 `transaction` 메서드는 Redis의 기본 `MULTI` 및 `EXEC` 명령어를 감싸는 편리한 래퍼를 제공합니다. `transaction` 메서드는 클로저(익명함수)를 인수로 받습니다. 이 클로저는 Redis 연결 인스턴스를 받아서 원하는 명령어를 모두 실행할 수 있습니다. 클로저 내에서 실행한 모든 Redis 명령어는 하나의 원자적(atomic) 트랜잭션으로 처리됩니다.

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션을 정의할 때는, 트랜잭션 내에서 Redis로부터 값을 조회하면 안 됩니다. 트랜잭션은 하나의 원자적 작업으로 실행되며, 해당 작업은 클로저의 모든 명령이 끝날 때까지 실제로 실행되지 않습니다.

#### Lua 스크립트

`eval` 메서드를 사용하면 여러 개의 Redis 명령을 하나의 원자적 작업으로 실행할 수 있습니다. 이 방법의 장점은 실행 중에 Redis 키의 값을 직접 확인하거나 조작할 수 있다는 점입니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 여러 개의 인수를 받습니다. 첫째로, Lua 스크립트(문자열)를 전달해야 합니다. 둘째로, 해당 스크립트가 다루는 키의 개수(정수)를 넘깁니다. 그다음, 그 키들의 이름을 차례대로 넘깁니다. 마지막으로, 스크립트 내에서 사용할 추가 인수를 계속 넘겨줄 수 있습니다.

다음은 카운터를 증가시키고, 그 값이 5보다 크면 또 다른 카운터도 증가시키는 예시입니다. 마지막으로 첫 번째 카운터의 값을 반환합니다.

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
> Redis 스크립트 관련 자세한 사항은 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하시기 바랍니다.

<a name="pipelining-commands"></a>
### 명령어 파이프라이닝

한 번에 수십 개, 수백 개의 Redis 명령을 실행해야 할 때, 각각의 명령마다 네트워크 요청을 반복하는 대신 `pipeline` 메서드를 사용할 수 있습니다. `pipeline` 메서드는 Redis 인스턴스를 받는 클로저를 인수로 받습니다. 이 클로저에서 원하는 만큼 명령을 호출할 수 있고, 모든 명령이 한 번에 Redis 서버로 전송되어 네트워크 왕복 횟수를 크게 줄일 수 있습니다. 명령은 호출한 순서대로 실행됩니다.

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

라라벨은 Redis의 `publish` 및 `subscribe` 명령어를 쉽게 사용할 수 있는 인터페이스를 제공합니다. 이 명령어들은 특정 "채널"에서 메시지를 수신(listen)하거나, 다른 애플리케이션(혹은 다른 프로그래밍 언어로 작성된 프로그램 등)에서 메시지를 발행(publish)하게 해주므로, 다양한 애플리케이션과 프로세스 사이에 쉽고 유연한 통신이 가능합니다.

먼저, `subscribe` 메서드를 사용해 채널 리스너를 설정해보겠습니다. 이 메서드는 실행하면 오랜 시간 실행 상태로 대기하는 프로세스이므로, [아티즌 명령어](/docs/12.x/artisan) 내에서 사용하는 것이 좋습니다.

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

이제, `publish` 메서드를 사용해 채널로 메시지를 발행할 수 있습니다.

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
#### 와일드카드(wildcard) 구독

`psubscribe` 메서드를 사용하면 와일드카드 채널 구독이 가능합니다. 이 기능은 모든 채널의 메시지를 한 번에 모니터링해야 할 때 유용합니다. 클로저의 두 번째 인수로 채널 이름이 전달됩니다.

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```
