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

[Redis](https://redis.io)은 오픈 소스의 고급 키-값 저장소입니다. 키에 [문자열](https://redis.io/docs/data-types/strings/), [해시](https://redis.io/docs/data-types/hashes/), [리스트](https://redis.io/docs/data-types/lists/), [셋](https://redis.io/docs/data-types/sets/), [정렬된 셋](https://redis.io/docs/data-types/sorted-sets/) 등 다양한 자료구조를 담을 수 있기 때문에 데이터 구조 서버(data structure server)라고도 불립니다.

Laravel에서 Redis를 사용하기 전에, 가능하다면 PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 설치해서 사용하는 것을 권장합니다. 이 확장 모듈은 사용자 공간("user-land") PHP 패키지에 비해 설치가 어렵지만, Redis를 많이 사용하는 애플리케이션에서 더 나은 성능을 보일 수 있습니다. 만약 [Laravel Sail](/docs/{{version}}/sail)을 사용하고 있다면, 이 확장 모듈은 애플리케이션의 Docker 컨테이너에 이미 설치되어 있습니다.

PhpRedis 확장 모듈을 설치할 수 없는 경우, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 순수 PHP로 작성된 Redis 클라이언트로 별도의 확장 모듈이 필요하지 않습니다:

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 설정

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 관리할 수 있습니다. 이 파일 내에서, 애플리케이션에서 사용할 Redis 서버를 담고 있는 `redis` 배열을 확인할 수 있습니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'default' => [
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', 6379),
            'database' => env('REDIS_DB', 0),
        ],

        'cache' => [
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', 6379),
            'database' => env('REDIS_CACHE_DB', 1),
        ],

    ],

설정 파일에 정의된 각 Redis 서버는 이름, 호스트, 포트가 반드시 필요합니다. 단, 하나의 URL로 Redis 연결을 표현하는 경우에는 제외됩니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'default' => [
            'url' => 'tcp://127.0.0.1:6379?database=0',
        ],

        'cache' => [
            'url' => 'tls://user:password@127.0.0.1:6380?database=1',
        ],

    ],

<a name="configuring-the-connection-scheme"></a>
#### 연결 스킴 설정하기

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 하지만, `scheme` 설정 옵션을 Redis 서버의 설정 배열에 지정하면 TLS / SSL 암호화도 사용할 수 있습니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'default' => [
            'scheme' => 'tls',
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', 6379),
            'database' => env('REDIS_DB', 0),
        ],

    ],

<a name="clusters"></a>
### 클러스터

애플리케이션이 여러 대의 Redis 서버로 구성된 클러스터를 사용할 경우, `config/database.php` 설정 파일의 Redis 설정 내에 `clusters` 키로 클러스터들을 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로, 직접 추가해야 합니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'clusters' => [
            'default' => [
                [
                    'host' => env('REDIS_HOST', 'localhost'),
                    'password' => env('REDIS_PASSWORD'),
                    'port' => env('REDIS_PORT', 6379),
                    'database' => 0,
                ],
            ],
        ],

    ],

기본적으로 클러스터는 클라이언트 사이드 샤딩(client-side sharding)으로 동작하여 여러 노드를 풀로 만들어 많은 양의 램을 사용할 수 있도록 해줍니다. 단, 클라이언트 사이드 샤딩은 장애 조치를 지원하지 않기 때문에, 주로 다른 주요 데이터 저장소에서 다시 얻을 수 있는 임시 캐시 데이터에 적합합니다.

클라이언트 사이드 샤딩 대신 Redis의 네이티브 클러스터링을 이용하고 싶다면, `config/database.php` 파일의 `options.cluster` 값을 `redis`로 설정하면 됩니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'options' => [
            'cluster' => env('REDIS_CLUSTER', 'redis'),
        ],

        'clusters' => [
            // ...
        ],

    ],

<a name="predis"></a>
### Predis

Predis 패키지를 통해 Redis와 상호작용하고 싶다면, `REDIS_CLIENT` 환경 변수의 값을 `predis`로 설정해야 합니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'predis'),

        // ...
    ],

기본 `host`, `port`, `database`, `password` 외에, Predis는 각 Redis 서버별로 [추가 연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)도 지원합니다. 이런 추가 설정이 필요하다면 `config/database.php`에서 Redis 서버 설정에 옵션을 추가할 수 있습니다:

    'default' => [
        'host' => env('REDIS_HOST', 'localhost'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', 6379),
        'database' => 0,
        'read_write_timeout' => 60,
    ],

<a name="the-redis-facade-alias"></a>
#### Redis 파사드 별칭

Laravel의 `config/app.php`에는 프레임워크에 등록될 클래스 별칭을 담은 `aliases` 배열이 있습니다. 기본적으로 `Redis` 별칭은 포함되어 있지 않은데, 이는 PhpRedis 확장 모듈이 제공하는 `Redis` 클래스명과 충돌을 피하기 위함입니다. Predis 클라이언트를 사용하고 `Redis` 별칭을 추가하고 싶을 경우, `config/app.php`의 `aliases` 배열에 직접 넣어주면 됩니다:

    'aliases' => Facade::defaultAliases()->merge([
        'Redis' => Illuminate\Support\Facades\Redis::class,
    ])->toArray(),

<a name="phpredis"></a>
### PhpRedis

Laravel은 기본적으로 PhpRedis 확장 모듈을 통해 Redis와 통신합니다. 어느 클라이언트로 통신할지는 보통 `REDIS_CLIENT` 환경 변수 또는 `redis.client` 설정 값으로 결정됩니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        // 나머지 Redis 설정...
    ],

기본 `scheme`, `host`, `port`, `database`, `password` 옵션 외에도, PhpRedis는 `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `timeout`, `context` 등 추가 연결 파라미터를 지원합니다. 이 옵션들도 `config/database.php` 서버 설정에 추가할 수 있습니다:

    'default' => [
        'host' => env('REDIS_HOST', 'localhost'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', 6379),
        'database' => 0,
        'read_timeout' => 60,
        'context' => [
            // 'auth' => ['username', 'secret'],
            // 'stream' => ['verify_peer' => false],
        ],
    ],

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

PhpRedis 확장 모듈은 다양한 직렬화(serialization) 및 압축(compression) 알고리즘을 사용할 수 있습니다. 이 알고리즘들은 Redis 설정의 `options` 배열로 지정합니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'options' => [
            'serializer' => Redis::SERIALIZER_MSGPACK,
            'compression' => Redis::COMPRESSION_LZ4,
        ],

        // 나머지 Redis 설정...
    ],

현재 지원되는 직렬화 방식은 `Redis::SERIALIZER_NONE`(기본), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`입니다.

지원하는 압축 알고리즘은 `Redis::COMPRESSION_NONE`(기본), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`입니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기

여러 가지 메서드를 통해 `Redis` [파사드](/docs/{{version}}/facades)에서 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하므로, [Redis 명령어](https://redis.io/commands)를 파사드에서 호출하면 해당 명령어가 직접 Redis로 전달됩니다. 다음은 `Redis` 파사드에서 `get` 메서드로 Redis의 `GET` 명령어를 호출하는 예시입니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
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

위에서 언급한 것처럼, 모든 Redis 명령어를 `Redis` 파사드로 호출할 수 있습니다. Laravel은 매직 메서드를 사용하여 명령어를 Redis 서버로 전달합니다. Redis 명령어에 인자가 필요하다면, 해당 값을 메서드의 인자로 넘겨주면 됩니다:

    use Illuminate\Support\Facades\Redis;

    Redis::set('name', 'Taylor');

    $values = Redis::lrange('names', 5, 10);

또는, `Redis` 파사드의 `command` 메서드를 사용해 명령어를 서버에 전달할 수도 있습니다. 이 메서드는 첫 번째 인자로 명령어 이름을, 두 번째 인자로 값을 배열로 받습니다:

    $values = Redis::command('lrange', ['name', 5, 10]);

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 설정 파일에서는 여러 개의 Redis 연결/서버를 정의할 수 있습니다. `Redis` 파사드의 `connection` 메서드를 사용해 특정 Redis 연결에 접속할 수 있습니다:

    $redis = Redis::connection('connection-name');

기본 Redis 연결 인스턴스를 얻으려면 추가 인자 없이 `connection` 메서드를 호출하면 됩니다:

    $redis = Redis::connection();

<a name="transactions"></a>
### 트랜잭션

`Redis` 파사드의 `transaction` 메서드는 Redis의 원래 `MULTI`, `EXEC` 명령어에 편리한 래퍼를 제공합니다. `transaction` 메서드는 하나의 클로저를 인자로 받는데, 이 클로저는 Redis 연결 인스턴스를 전달받아 원하는 명령을 내릴 수 있고, 클로저 내부의 모든 명령은 단일 원자적 트랜잭션으로 실행됩니다:

    use Redis;
    use Illuminate\Support\Facades;

    Facades\Redis::transaction(function (Redis $redis) {
        $redis->incr('user_visits', 1);
        $redis->incr('total_visits', 1);
    });

> [!WARNING]  
> Redis 트랜잭션을 정의할 때, 연결로부터 값을 조회할 수 없습니다. 트랜잭션은 단일 원자적 연산으로, 클로저가 모든 명령 실행을 마칠 때까지 실제로 실행되지 않습니다.

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령을 하나의 원자 연산으로 실행하는 다른 방법입니다. 특히 `eval` 메서드는 실행 중인 키의 값을 조회하고 조작할 수 있는 이점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 여러 인자를 받는데, 첫 번째는 Lua 스크립트(문자열), 두 번째는 스크립트에서 사용하는 키의 개수(정수), 세 번째로 키 이름들, 그 외에는 스크립트에서 사용할 추가 인자입니다.

다음 예제는 카운터를 증가시키고, 그 값이 5를 넘으면 두 번째 카운터를 증가시키는 기본 예시입니다. 마지막으로 첫 번째 카운터의 값을 반환합니다:

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

때때로 수십 개의 Redis 명령을 한 번에 실행해야 할 수 있습니다. 이때, 각 명령마다 네트워크 요청을 보내는 대신 `pipeline` 메서드를 사용할 수 있습니다. 이 메서드는 Redis 인스턴스를 받을 클로저 하나를 인자로 받고, 이 클로저 내에서 내린 모든 명령은 한 번에 서버로 전송되어 네트워크 트립을 최소화합니다. 단, 명령은 내린 순서대로 실행됩니다:

    use Redis;
    use Illuminate\Support\Facades;

    Facades\Redis::pipeline(function (Redis $pipe) {
        for ($i = 0; $i < 1000; $i++) {
            $pipe->set("key:$i", $i);
        }
    });

<a name="pubsub"></a>
## Pub / Sub

Laravel은 Redis의 `publish` 및 `subscribe` 명령어에 간편한 인터페이스를 제공합니다. 이 명령어들을 사용하면 특정 "채널"에서 메시지를 수신할 수 있습니다. 다른 애플리케이션 혹은 다른 언어로도 채널에 메시지를 보낼 수 있어서, 서로 다른 애플리케이션과 프로세스 간의 손쉬운 통신이 가능합니다.

먼저, `subscribe` 메서드로 채널 리스너를 설정해 봅시다. 이 메서드는 [Artisan 명령어](/docs/{{version}}/artisan) 내에 배치하는 것이 좋습니다. 왜냐하면 `subscribe`는 오래 실행되는 프로세스를 시작하기 때문입니다:

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
        protected $description = 'Redis 채널을 구독합니다';

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

이제 `publish` 메서드를 사용해 채널에 메시지를 보낼 수 있습니다:

    use Illuminate\Support\Facades\Redis;

    Route::get('/publish', function () {
        // ...

        Redis::publish('test-channel', json_encode([
            'name' => 'Adam Wathan'
        ]));
    });

<a name="wildcard-subscriptions"></a>
#### 와일드카드 구독

`psubscribe` 메서드를 사용하면 와일드카드 채널을 구독할 수 있습니다. 이는 모든 채널의 모든 메시지를 잡아내고 싶을 때 유용합니다. 채널 이름은 두 번째 인자로 클로저에 전달됩니다:

    Redis::psubscribe(['*'], function (string $message, string $channel) {
        echo $message;
    });

    Redis::psubscribe(['users.*'], function (string $message, string $channel) {
        echo $message;
    });
