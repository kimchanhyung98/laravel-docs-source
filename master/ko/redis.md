# Redis

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Redis와 상호작용](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [명령 파이프라인 처리](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개

[Redis](https://redis.io)는 오픈 소스 고급 키-값 저장소입니다. 키에 [문자열](https://redis.io/docs/data-types/strings/), [해시](https://redis.io/docs/data-types/hashes/), [리스트](https://redis.io/docs/data-types/lists/), [셋](https://redis.io/docs/data-types/sets/), [정렬된 셋](https://redis.io/docs/data-types/sorted-sets/)처럼 다양한 데이터 구조를 저장할 수 있기 때문에 데이터 구조 서버로도 자주 불립니다.

Laravel에서 Redis를 사용하기 전에, [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 PECL을 통해 설치해서 사용하는 것을 권장합니다. 이 확장 모듈은 "유저랜드" PHP 패키지에 비해 설치가 더 복잡하지만, Redis를 많이 사용하는 애플리케이션에서는 더 나은 성능을 제공할 수 있습니다. [Laravel Sail](/docs/{{version}}/sail)을 사용하는 경우, 이 확장 모듈은 이미 애플리케이션의 Docker 컨테이너에 설치되어 있습니다.

PhpRedis 확장 모듈을 설치할 수 없는 경우, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 완전히 PHP로 작성된 Redis 클라이언트이며, 추가적인 확장 모듈이 필요하지 않습니다:

```shell
composer require predis/predis:^2.0
```

<a name="configuration"></a>
## 설정

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일 내에서 `redis` 배열에 애플리케이션에서 사용할 Redis 서버 정보가 포함되어 있습니다:

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

설정 파일에 정의된 각 Redis 서버는 이름, 호스트, 포트 정보를 가져야 하며, 하나의 URL로 Redis 연결을 지정할 수도 있습니다:

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
#### 연결 스킴 구성

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 하지만 Redis 서버 설정 배열에 `scheme` 설정 옵션을 지정함으로써 TLS/SSL 암호화도 사용할 수 있습니다:

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

애플리케이션에서 Redis 서버 클러스터를 사용하는 경우, `redis` 설정의 `clusters` 키에 클러스터를 정의할 수 있습니다. 이 설정 키는 기본적으로 존재하지 않으므로, 애플리케이션의 `config/database.php` 파일에 직접 만들어야 합니다:

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

Laravel은 기본적으로 `options.cluster` 설정 값이 `redis`로 되어 있기 때문에, 네이티브 Redis 클러스터링을 사용합니다. 네이티브 클러스터링은 장애 조치(failover)를 잘 처리하기 때문에 기본값으로 적합합니다.

Predis를 사용할 경우 클라이언트 단 샤딩(client-side sharding)도 지원합니다. 단, 클라이언트 단 샤딩은 장애 조치가 안되기 때문에, 주로 다른 주요 데이터 저장소로부터 다시 얻을 수 있는 캐시 데이터에 적합합니다.

네이티브 Redis 클러스터가 아닌 클라이언트 단 샤딩을 사용하려면, 설정 파일 `config/database.php`에서 `options.cluster` 항목을 제거하면 됩니다:

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

애플리케이션이 Predis 패키지를 통해 Redis와 상호작용하게 하려면, `REDIS_CLIENT` 환경 변수의 값을 `predis`로 설정해야 합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 설정 옵션 이외에도, Predis는 각 Redis 서버용으로 추가적인 [연결 매개변수](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이런 추가 옵션을 사용하려면, 애플리케이션의 `config/database.php` 파일 내 Redis 서버 설정에 옵션을 추가하면 됩니다:

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

Laravel은 기본적으로 PhpRedis 확장 모듈을 사용하여 Redis와 통신합니다. Laravel이 사용할 Redis 클라이언트는 일반적으로 `REDIS_CLIENT` 환경 변수 값을 반영하는 `redis.client` 설정 옵션으로 결정됩니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

기본 설정 옵션 이외에도, PhpRedis는 다음 연결 매개변수를 추가로 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context`. 이 옵션들은 `config/database.php`의 Redis 서버 설정에 추가할 수 있습니다:

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

PhpRedis 확장 모듈은 다양한 직렬화기(serializer)와 압축 알고리즘을 사용할 수 있습니다. 이 알고리즘들은 Redis 설정의 `options` 배열에서 설정할 수 있습니다:

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

현재 지원되는 직렬화기는 다음과 같습니다: `Redis::SERIALIZER_NONE`(기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`.

지원되는 압축 알고리즘은 다음과 같습니다: `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`.

<a name="interacting-with-redis"></a>
## Redis와 상호작용

`Redis` [파사드](/docs/{{version}}/facades)의 다양한 메서드를 호출하여 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하므로, 어떤 [Redis 명령어](https://redis.io/commands)도 그대로 호출할 수 있고 명령은 직접 Redis로 전달됩니다. 예를 들어, `Redis` 파사드의 `get` 메서드를 호출하면 Redis의 `GET` 명령을 실행하게 됩니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Redis;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 표시합니다.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => Redis::get('user:profile:'.$id)
        ]);
    }
}
```

위에서 언급한 것처럼, 모든 Redis 명령어를 `Redis` 파사드에 호출할 수 있습니다. Laravel은 매직 메서드를 활용하여 명령어를 Redis 서버로 전달합니다. Redis 명령어가 인자를 필요로 한다면, 파사드의 해당 메서드에 인자를 그대로 넘기면 됩니다:

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는, `Redis` 파사드의 `command` 메서드를 사용하여 명령을 전달할 수도 있습니다. 이 메서드는 첫 번째 인수로 명령 이름, 두 번째 인수로 값의 배열을 받습니다:

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 파일에서는 여러 개의 Redis 연결/서버를 정의할 수 있습니다. 특정 Redis 연결에 접근하려면, `Redis` 파사드의 `connection` 메서드를 사용하면 됩니다:

```php
$redis = Redis::connection('connection-name');
```

기본 Redis 연결을 얻으려면, `connection` 메서드에 인자를 주지 않아도 됩니다:

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션

`Redis` 파사드의 `transaction` 메서드는 Redis의 기본 `MULTI` 및 `EXEC` 명령에 대한 편리한 래퍼를 제공합니다. `transaction` 메서드는 클로저를 유일한 인자로 받는데, 이 클로저는 Redis 연결 인스턴스를 전달받아 원하는 명령을 실행할 수 있습니다. 클로저 내에서 실행된 모든 Redis 명령어는 하나의 원자적 트랜잭션으로 실행됩니다:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션을 정의할 때는, 트랜잭션 내에서 Redis 연결로부터 값을 조회할 수 없습니다. 트랜잭션은 클로저에서 모든 명령이 실행된 후 원자적으로 처리되기 때문입니다.

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령을 하나의 원자적 연산으로 실행하는 또 다른 방법을 제공합니다. 이 방법의 장점은, 트랜잭션 수행 중에 Redis 키 값을 읽고 검사할 수 있다는 점입니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 다소 복잡하게 보일 수 있지만, 간단한 예제를 통해 이해할 수 있습니다. `eval` 메서드는 첫 번째 인수로 Lua 스크립트(문자열로), 두 번째 인수로 스크립트가 사용하는 키 개수(정수), 세 번째 이후 인수로는 해당 키의 이름, 그리고 그 외 필요한 추가 인수를 받습니다.

예를 들어, 아래 코드는 첫 번째 카운터를 증가시키고, 새 값을 검사해 그 값이 5보다 크면 두 번째 카운터도 증가시키고, 마지막으로 첫 번째 카운터의 값을 반환합니다:

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
> Redis 스크립팅에 대한 더 자세한 내용은 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 명령 파이프라인 처리

여러 Redis 명령을 한꺼번에 실행해야 할 때가 있습니다. 명령마다 Redis 서버로 네트워크 요청을 보내는 대신, `pipeline` 메서드를 사용할 수 있습니다. `pipeline`은 하나의 클로저(인수로 Redis 인스턴스가 전달됨)를 받으며, 그 안에서 명령들을 모두 발행하면 해당 명령들이 한 번에 서버로 전송되어 네트워크 트립을 줄일 수 있습니다. 명령들은 지정된 순서대로 실행됩니다:

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

Laravel은 Redis의 `publish` 및 `subscribe` 명령에 편리한 인터페이스를 제공합니다. 이 명령어를 사용하면 특정 "채널"의 메시지를 구독하거나, 채널에 메시지를 발행할 수 있습니다. 다른 애플리케이션이나 심지어 다른 언어로 작성된 서비스에서도 메시지를 발행할 수 있기 때문에, 애플리케이션/프로세스 간 커뮤니케이션이 쉬워집니다.

먼저, `subscribe` 메서드를 사용해서 채널 리스너를 설정해봅시다. 이 메서드는 [Artisan 명령어](/docs/{{version}}/artisan)에서 실행하는 것이 일반적입니다. 왜냐하면 `subscribe`를 호출하면 장시간 실행되는 프로세스가 시작되기 때문입니다:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Redis;

class RedisSubscribe extends Command
{
    /**
     * 콘솔 명령어 이름 및 시그니처
     *
     * @var string
     */
    protected $signature = 'redis:subscribe';

    /**
     * 콘솔 명령어 설명
     *
     * @var string
     */
    protected $description = 'Redis 채널 구독';

    /**
     * 콘솔 명령어 실행
     */
    public function handle(): void
    {
        Redis::subscribe(['test-channel'], function (string $message) {
            echo $message;
        });
    }
}
```

이제 `publish` 메서드를 사용해서 채널에 메시지를 발행할 수 있습니다:

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

`psubscribe` 메서드를 사용하면, 와일드카드 채널에 구독할 수 있습니다. 이를 통해 모든 채널에 대한 메시지를 수신할 수 있습니다. 채널 이름은 클로저의 두 번째 인수로 전달됩니다:

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```
