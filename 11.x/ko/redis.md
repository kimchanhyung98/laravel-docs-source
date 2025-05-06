# Redis

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
## 소개

[Redis](https://redis.io)는 오픈 소스이며 고급 키-값 저장소입니다. 키에 [문자열](https://redis.io/docs/data-types/strings/), [해시](https://redis.io/docs/data-types/hashes/), [리스트](https://redis.io/docs/data-types/lists/), [셋](https://redis.io/docs/data-types/sets/), [정렬된 셋](https://redis.io/docs/data-types/sorted-sets/) 등의 데이터 구조를 포함할 수 있기 때문에 종종 데이터 구조 서버라고 불립니다.

Laravel에서 Redis를 사용하기 전에, PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 설치하여 사용할 것을 권장합니다. 이 확장 모듈은 "유저랜드" PHP 패키지들에 비해 설치가 다소 복잡하지만, Redis를 많이 사용하는 애플리케이션에서는 더 나은 성능을 제공할 수 있습니다. 만약 [Laravel Sail](/docs/{{version}}/sail)을 사용 중이라면, 이 확장 모듈은 애플리케이션의 Docker 컨테이너에 이미 설치되어 있습니다.

PhpRedis 확장 모듈을 설치할 수 없다면 Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 완전히 PHP로 작성된 Redis 클라이언트로, 추가적인 확장 모듈 없이 사용할 수 있습니다:

```shell
composer require predis/predis:^2.0
```

<a name="configuration"></a>
## 설정

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일을 통해 할 수 있습니다. 이 파일 안에는 애플리케이션에서 사용하는 Redis 서버들을 포함하는 `redis` 배열이 있습니다:

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

설정 파일에 정의된 각 Redis 서버는 이름, 호스트, 포트를 반드시 포함해야 합니다. 단, Redis 연결을 대표하는 단일 URL을 정의했다면 이를 생략할 수 있습니다:

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

<a name="configuring-the-connection-scheme"></a>
#### 연결 방식(스킴) 설정

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 하지만, Redis 서버 설정 배열에 `scheme` 설정 옵션을 지정하여 TLS / SSL 암호화를 사용할 수도 있습니다:

    'default' => [
        'scheme' => 'tls',
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'username' => env('REDIS_USERNAME'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_DB', '0'),
    ],

<a name="clusters"></a>
### 클러스터

애플리케이션이 여러 Redis 서버로 구성된 클러스터를 사용하는 경우, Redis 설정의 `clusters` 키에서 클러스터를 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로 `config/database.php` 설정 파일 안에 직접 생성해야 합니다:

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

기본적으로 Laravel은 `options.cluster` 설정 값이 `redis`로 지정되어 있기 때문에 네이티브 Redis 클러스터링을 사용합니다. Redis 클러스터링은 장애 조치를 매끄럽게 처리하므로 기본값으로 적합합니다.

Predis를 사용할 경우 Laravel은 클라이언트 사이드 샤딩(client-side sharding)도 지원합니다. 하지만, 클라이언트 사이드 샤딩은 장애 조치를 지원하지 않으므로, 기본 데이터 저장소에서 가져올 수 있는 임시 캐시 데이터에 가장 적합합니다.

네이티브 Redis 클러스터링 대신 클라이언트 사이드 샤딩을 사용하려면 `config/database.php` 파일에서 `options.cluster` 설정 값을 제거하면 됩니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'clusters' => [
            // ...
        ],

        // ...
    ],

<a name="predis"></a>
### Predis

애플리케이션에서 Redis와 상호작용할 때 Predis 패키지를 사용하려면, `REDIS_CLIENT` 환경 변수의 값을 `predis`로 설정해야 합니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'predis'),

        // ...
    ],

기본 설정 옵션 외에도, Predis는 각 Redis 서버별로 정의할 수 있는 추가 [연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이러한 추가 설정 옵션을 사용하려면 애플리케이션의 `config/database.php` 설정 파일에서 Redis 서버 설정에 추가하면 됩니다:

    'default' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'username' => env('REDIS_USERNAME'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_DB', '0'),
        'read_write_timeout' => 60,
    ],

<a name="phpredis"></a>
### PhpRedis

기본적으로 Laravel은 Redis와 통신할 때 PhpRedis 확장 모듈을 사용합니다. Laravel이 사용할 Redis 클라이언트는 일반적으로 `REDIS_CLIENT` 환경 변수의 값과 매칭되는 `redis.client` 설정 옵션 값에 의해 결정됩니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        // ...
    ],

기본 설정 옵션 외에도, PhpRedis는 다음과 같은 추가 연결 파라미터를 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context`. 이러한 옵션들은 `config/database.php` 설정 파일의 Redis 서버 설정에 추가할 수 있습니다:

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

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

PhpRedis 확장 모듈은 직렬화기(serializer)와 압축 알고리즘을 다양하게 설정할 수 있습니다. 이러한 알고리즘들은 Redis 설정의 `options` 배열을 통해 설정할 수 있습니다:

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

현재 지원되는 직렬화기는 다음과 같습니다: `Redis::SERIALIZER_NONE` (기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`.

지원되는 압축 알고리즘은 다음과 같습니다: `Redis::COMPRESSION_NONE` (기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기

`Redis` [파사드](/docs/{{version}}/facades)의 다양한 메소드를 호출하여 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메소드를 지원하므로, 파사드에 모든 [Redis 명령](https://redis.io/commands)을 호출하면 해당 명령이 Redis로 바로 전달됩니다. 예시에서, `Redis` 파사드의 `get` 메소드를 호출하여 Redis의 `GET` 명령을 사용할 수 있습니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
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

위에서 언급한 것처럼, Redis의 모든 명령을 `Redis` 파사드로 호출할 수 있습니다. Laravel은 매직 메소드를 사용하여 명령을 Redis 서버로 전달합니다. Redis 명령이 인자를 필요로 한다면, 해당 메소드에 인자를 전달하세요:

    use Illuminate\Support\Facades\Redis;

    Redis::set('name', 'Taylor');

    $values = Redis::lrange('names', 5, 10);

혹은, `Redis` 파사드의 `command` 메소드를 사용하여 명령어 이름을 첫 번째 인자로, 값 배열을 두 번째 인자로 서버에 직접 전달할 수도 있습니다:

    $values = Redis::command('lrange', ['name', 5, 10]);

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 설정 파일에서는 여러 Redis 연결/서버를 정의할 수 있습니다. `Redis` 파사드의 `connection` 메소드를 이용하여 특정 Redis 연결에 접근할 수 있습니다:

    $redis = Redis::connection('connection-name');

기본 Redis 연결 인스턴스를 얻고 싶다면 추가 인자 없이 `connection` 메소드를 호출하면 됩니다:

    $redis = Redis::connection();

<a name="transactions"></a>
### 트랜잭션

`Redis` 파사드의 `transaction` 메소드는 Redis의 기본 `MULTI` 및 `EXEC` 명령을 편리하게 감싸줍니다. `transaction` 메소드는 클로저 하나만 받아들이며, 이 클로저는 Redis 연결 인스턴스를 전달받아 원하는 명령을 실행할 수 있습니다. 클로저 안에서 실행된 모든 Redis 명령은 단일 원자적 트랜잭션으로 처리됩니다:

    use Redis;
    use Illuminate\Support\Facades;

    Facades\Redis::transaction(function (Redis $redis) {
        $redis->incr('user_visits', 1);
        $redis->incr('total_visits', 1);
    });

> [!WARNING]
> Redis 트랜잭션을 정의할 때 트랜잭션 내부에서는 Redis 연결로부터 값을 조회할 수 없습니다. 트랜잭션은 클로저가 모든 명령을 실행 완료한 후 원자적으로 실행된다는 점을 명심하세요.

#### Lua 스크립트

`eval` 메소드는 여러 Redis 명령을 한번에 원자적으로 실행할 수 있는 또 다른 방법입니다. `eval` 메소드는 그 과정에서 Redis 키 값을 조회하거나 조작할 수 있는 장점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메소드는 여러 인자를 기대합니다. 첫 번째로는 Lua 스크립트(문자열)를, 두 번째로는 스크립트가 접근하는 키의 개수(정수), 세 번째로는 해당 키의 이름, 마지막으로 필요한 추가 인자를 전달하면 됩니다.

다음은 카운터를 증가시키고, 새 값을 확인하여 만약 5보다 크다면 두 번째 카운터도 증가시키며, 마지막으로 첫 번째 카운터의 값을 반환하는 예시입니다:

    $value = Redis::eval(<<<'LUA'
        local counter = redis.call("incr", KEYS[1])

        if counter > 5 then
            redis.call("incr", KEYS[2])
        end

        return counter
    LUA, 2, 'first-counter', 'second-counter');

> [!WARNING]
> Redis 스크립팅에 대한 자세한 정보는 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 파이프라이닝 명령어

가끔 여러 개의 Redis 명령을 실행해야 할 수도 있습니다. 각 명령마다 Redis 서버로 네트워크 트립을 발생시키지 않고, `pipeline` 메소드를 사용할 수 있습니다. 이 메소드는 Redis 인스턴스를 인자로 받는 클로저 하나만 받아들입니다. 클로저에서 모든 명령을 실행하면 이들은 한 번에 모여서 Redis 서버로 전송되어 네트워크 트립을 줄일 수 있습니다. 명령은 입력한 순서대로 실행됩니다:

    use Redis;
    use Illuminate\Support\Facades;

    Facades\Redis::pipeline(function (Redis $pipe) {
        for ($i = 0; $i < 1000; $i++) {
            $pipe->set("key:$i", $i);
        }
    });

<a name="pubsub"></a>
## Pub / Sub

Laravel은 Redis의 `publish`와 `subscribe` 명령에 편리하게 접근할 수 있는 인터페이스를 제공합니다. 이 명령어를 사용하면 특정 "채널"에서 메시지를 구독하고, 다른 애플리케이션이나 다른 프로그래밍 언어에서도 메시지를 발송할 수 있으므로 다양한 프로세스와 애플리케이션 간 통신이 용이해집니다.

먼저, `subscribe` 메소드를 사용해 채널 리스너를 설정해봅니다. [Artisan 명령](/docs/{{version}}/artisan) 안에서 해당 메소드를 호출하는 것이 좋습니다. 왜냐하면, `subscribe` 호출은 긴 시간 실행되는 프로세스이기 때문입니다:

    <?php

    namespace App\Console\Commands;

    use Illuminate\Console\Command;
    use Illuminate\Support\Facades\Redis;

    class RedisSubscribe extends Command
    {
        /**
         * 콘솔 명령의 이름과 시그니처입니다.
         *
         * @var string
         */
        protected $signature = 'redis:subscribe';

        /**
         * 콘솔 명령의 설명입니다.
         *
         * @var string
         */
        protected $description = 'Redis 채널 구독';

        /**
         * 콘솔 명령 실행.
         */
        public function handle(): void
        {
            Redis::subscribe(['test-channel'], function (string $message) {
                echo $message;
            });
        }
    }

이제 `publish` 메소드를 사용해 채널에 메시지를 발송할 수 있습니다:

    use Illuminate\Support\Facades\Redis;

    Route::get('/publish', function () {
        // ...

        Redis::publish('test-channel', json_encode([
            'name' => 'Adam Wathan'
        ]));
    });

<a name="wildcard-subscriptions"></a>
#### 와일드카드 구독

`psubscribe` 메소드를 사용하면 와일드카드 채널을 구독할 수 있습니다. 이는 모든 채널에서 발생하는 메시지를 받아야 할 때 유용합니다. 채널명은 클로저의 두 번째 인자로 전달됩니다:

    Redis::psubscribe(['*'], function (string $message, string $channel) {
        echo $message;
    });

    Redis::psubscribe(['users.*'], function (string $message, string $channel) {
        echo $message;
    });