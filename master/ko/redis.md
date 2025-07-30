# Redis

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

[Redis](https://redis.io)는 오픈 소스 고급 키-값 저장소입니다. 키가 [문자열](https://redis.io/docs/data-types/strings/), [해시](https://redis.io/docs/data-types/hashes/), [리스트](https://redis.io/docs/data-types/lists/), [셋](https://redis.io/docs/data-types/sets/), [정렬된 셋](https://redis.io/docs/data-types/sorted-sets/)을 포함할 수 있기 때문에 데이터 구조 서버라고도 자주 불립니다.

Laravel에서 Redis를 사용하기 전에, PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 설치하고 사용하는 것을 권장합니다. 이 확장 모듈은 일반적인 PHP 사용자 레벨 패키지보다 설치가 다소 복잡하지만, Redis를 집중적으로 사용하는 애플리케이션에서는 더 나은 성능을 발휘할 수 있습니다. 만약 [Laravel Sail](/docs/master/sail)을 사용 중이라면, 이 확장 모듈은 이미 애플리케이션의 Docker 컨테이너에 설치되어 있습니다.

만약 PhpRedis 확장 모듈을 설치할 수 없는 경우, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 순수 PHP로 작성된 Redis 클라이언트로 별도의 확장 모듈이 필요 없습니다:

```shell
composer require predis/predis:^2.0
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일을 통해 지정할 수 있습니다. 이 파일 안에는 애플리케이션에서 사용하는 Redis 서버들을 나타내는 `redis` 배열이 있습니다:

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

설정 파일에 정의된 각 Redis 서버는 이름, 호스트, 포트를 반드시 가져야 하며, 단일 URL로 Redis 연결을 나타낼 수도 있습니다:

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
#### 연결 스킴 구성하기

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 하지만 Redis 서버 설정 배열에 `scheme` 구성 옵션을 지정하면 TLS / SSL 암호화를 사용할 수 있습니다:

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

애플리케이션에서 Redis 서버 클러스터를 사용하는 경우, Redis 설정의 `clusters` 키 아래에 클러스터를 정의해야 합니다. 기본적으로 이 키는 존재하지 않으므로 `config/database.php` 파일에 직접 추가해야 합니다:

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

기본적으로 Laravel은 `options.cluster` 설정 값이 `redis`로 되어 있으면 네이티브 Redis 클러스터링을 사용합니다. 네이티브 Redis 클러스터링은 장애 조치를 우아하게 처리하기 때문에 좋은 기본 옵션입니다.

Laravel은 Predis를 사용할 때 클라이언트 측 샤딩도 지원합니다. 하지만 클라이언트 측 샤딩은 장애 조치를 처리하지 않으므로, 주로 다른 주 데이터 저장소에서 가져올 수 있는 일시적인 캐시 데이터에 적합합니다.

네이티브 Redis 클러스터링 대신 클라이언트 측 샤딩을 사용하려면 `config/database.php` 설정 파일에서 `options.cluster` 값을 제거하면 됩니다:

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

애플리케이션이 Predis 패키지를 통해 Redis와 상호작용하도록 하려면, 환경 변수 `REDIS_CLIENT` 값이 `predis`여야 합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 설정 옵션 외에도 Predis는 [추가 연결 매개변수](https://github.com/nrk/predis/wiki/Connection-Parameters)를 각 Redis 서버 구성에 정의할 수 있습니다. 이 추가 옵션을 사용하려면 `config/database.php`에서 Redis 서버 설정에 추가하세요:

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

기본적으로 Laravel은 PhpRedis 확장 모듈을 통해 Redis와 통신합니다. Laravel이 사용하는 클라이언트는 `redis.client` 구성 옵션 값에 의해 결정되며, 보통 환경 변수 `REDIS_CLIENT` 값과 맞춰집니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

기본 옵션 외에 PhpRedis는 `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context` 등의 추가 연결 매개변수를 지원합니다. 이 옵션들은 `config/database.php` 파일의 Redis 서버 설정에 추가할 수 있습니다:

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

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

PhpRedis 확장 모듈은 다양한 직렬화(serialization) 및 압축(compression) 알고리즘을 설정할 수도 있습니다. 이 설정들은 Redis 구성의 `options` 배열을 통해 지정할 수 있습니다:

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

현재 지원되는 직렬화 방식에는 `Redis::SERIALIZER_NONE` (기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`가 있습니다.

지원되는 압축 알고리즘에는 `Redis::COMPRESSION_NONE` (기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`가 포함됩니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

`Redis` [파사드](/docs/master/facades)를 호출하여 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하는데, 이는 Redis의 모든 [명령어](https://redis.io/commands)를 파사드 메서드로 직접 호출하여 Redis 서버에 전달할 수 있다는 뜻입니다. 아래 예제에서는 Redis의 `GET` 명령어를 `Redis` 파사드의 `get` 메서드로 호출합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Redis;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 지정한 사용자의 프로필을 보여줍니다.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => Redis::get('user:profile:'.$id)
        ]);
    }
}
```

위와 같이 Redis의 모든 명령어를 `Redis` 파사드에 호출할 수 있습니다. Laravel은 마법 메서드를 사용하여 명령어들을 Redis 서버로 전달합니다. 만약 Redis 명령어가 인수를 필요로 하면, 파사드의 해당 메서드에 인수를 전달하세요:

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는 `Redis` 파사드의 `command` 메서드를 사용하여 명령어 이름과 인수 배열을 전달할 수 있습니다:

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 파일에서는 여러 Redis 연결(서버)를 정의할 수 있습니다. 특정 Redis 연결을 얻으려면 `Redis` 파사드의 `connection` 메서드에 연결 이름을 전달하세요:

```php
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스를 얻으려면, 인수 없이 `connection` 메서드를 호출하세요:

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` 파사드의 `transaction` 메서드는 Redis의 `MULTI`와 `EXEC` 명령어를 감싸는 편리한 래퍼입니다. `transaction` 메서드는 클로저 하나를 인수로 받으며, 이 클로저는 Redis 연결 인스턴스를 파라미터로 받습니다. 클로저 내에서 실행되는 모든 Redis 명령어는 하나의 원자적 트랜잭션으로 실행됩니다:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션을 정의할 때는 Redis 연결에서 어떠한 값도 조회할 수 없습니다. 트랜잭션은 클로저 내 모든 명령어가 실행 완료되어야 한 번에 원자적으로 처리되기 때문입니다.

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령어를 원자적으로 실행할 수 있는 또 다른 방법입니다. 그러나 `eval`은 그 과정에서 Redis 키 값을 검사하거나 조작할 수 있다는 장점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성합니다.

`eval` 메서드는 처음 보면 복잡해 보일 수 있지만, 간단한 예제로 풀어보겠습니다. `eval` 메서드는 여러 인수를 받는데, 첫 번째는 Lua 스크립트 문자열, 두 번째는 스크립트에서 접근하는 키 개수를 정수로, 세 번째 이후는 그 키 이름들, 그리고 마지막으로 스크립트 내에서 접근할 추가 인수들을 넘깁니다.

아래 예제에서는 첫 번째 카운터를 증가시키고, 그 값이 5보다 크면 두 번째 카운터도 증가시킵니다. 마지막으로 첫 번째 카운터 값을 반환합니다:

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
### 명령어 파이프라이닝 (Pipelining Commands)

때때로 수십 개의 Redis 명령어를 실행해야 할 때가 있습니다. 이 경우 각각의 명령어마다 네트워크 왕복을 하지 않기 위해 `pipeline` 메서드를 사용할 수 있습니다. `pipeline` 메서드는 Redis 인스턴스를 파라미터로 받는 클로저 하나를 인수로 받고, 클로저 내에서 실행한 모든 명령어를 한 번에 서버로 보내 네트워크 왕복을 줄입니다. 명령어들은 요청한 순서대로 실행됩니다:

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

Laravel은 Redis의 `publish` 와 `subscribe` 명령어를 편리하게 사용할 수 있는 인터페이스를 제공합니다. 이 명령어들은 주어진 "채널"에서 메시지를 듣고 기다릴 수 있습니다. 다른 애플리케이션이나 프로그램 언어에서 이 채널에 메시지를 발행하여 애플리케이션 간 혹은 프로세스 간 손쉬운 통신을 할 수 있습니다.

먼저, `subscribe` 메서드를 사용해 채널 구독자를 설정해보겠습니다. `subscribe` 메서드는 장기 실행 프로세스이므로 보통 [Artisan 명령어](/docs/master/artisan)에 위치시킵니다:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Redis;

class RedisSubscribe extends Command
{
    /**
     * 콘솔 명령어 이름과 시그니처.
     *
     * @var string
     */
    protected $signature = 'redis:subscribe';

    /**
     * 콘솔 명령어 설명.
     *
     * @var string
     */
    protected $description = 'Redis 채널 구독';

    /**
     * 콘솔 명령어 실행.
     */
    public function handle(): void
    {
        Redis::subscribe(['test-channel'], function (string $message) {
            echo $message;
        });
    }
}
```

이제 다른 곳에서 `publish` 메서드를 사용해 채널에 메시지를 보낼 수 있습니다:

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

`psubscribe` 메서드를 사용하면 와일드카드 채널에 구독할 수 있습니다. 이 기능은 모든 채널이나 특정 패턴에 맞는 여러 채널의 메시지를 한 번에 캐치할 때 유용합니다. 구독 콜백은 두 번째 인수로 채널 이름도 받습니다:

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```