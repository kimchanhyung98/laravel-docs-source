# Redis

- [소개](#introduction)
- [구성](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [phpredis](#phpredis)
- [Redis와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [명령어 파이프라이닝](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개

[Redis](https://redis.io)는 오픈 소스 고급 키-값 저장소입니다. 키에 [문자열](https://redis.io/topics/data-types#strings), [해시](https://redis.io/topics/data-types#hashes), [리스트](https://redis.io/topics/data-types#lists), [셋](https://redis.io/topics/data-types#sets), [정렬된 셋](https://redis.io/topics/data-types#sorted-sets)과 같은 다양한 데이터 구조를 저장할 수 있기 때문에 데이터 구조 서버라고도 불립니다.

Laravel에서 Redis를 사용하기 전에 PECL을 통해 [phpredis](https://github.com/phpredis/phpredis) PHP 확장 프로그램을 설치하여 사용하는 것을 권장합니다. 이 확장 프로그램은 "사용자 단" PHP 패키지에 비해 설치가 더 복잡하지만, Redis를 많이 사용하는 애플리케이션에서는 더 나은 성능을 얻을 수 있습니다. [Laravel Sail](/docs/{{version}}/sail)을 사용하는 경우, 이 확장 프로그램은 애플리케이션의 Docker 컨테이너에 이미 설치되어 있습니다.

phpredis 확장 프로그램을 설치할 수 없는 경우, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 완전히 PHP로 작성된 Redis 클라이언트이며 추가적인 확장 없이도 동작합니다:

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 구성

애플리케이션의 Redis 설정은 `config/database.php` 구성 파일에서 할 수 있습니다. 이 파일 안에는 애플리케이션에서 사용하는 Redis 서버 정보를 담은 `redis` 배열이 있습니다:

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

구성 파일에 정의된 각 Redis 서버는 이름, 호스트 및 포트를 반드시 지정해야 하며, 또는 단일 URL로 Redis 연결을 나타낼 수 있습니다:

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
#### 연결 스킴(scheme) 설정

기본적으로, Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 하지만, `scheme` 설정 옵션을 Redis 서버 구성 배열에 지정함으로써 TLS/SSL 암호화를 사용할 수도 있습니다:

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

애플리케이션이 여러 Redis 서버 클러스터를 사용하는 경우, Redis 구성의 `clusters` 키에 이 클러스터 정보를 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로 애플리케이션의 `config/database.php` 구성 파일에 직접 추가해야 합니다:

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

기본적으로 클러스터는 클라이언트 측 샤딩(client-side sharding)을 통해 각 노드에 분산 저장이 가능하며, 이를 통해 여러 노드를 풀로 묶고 더 많은 메모리를 사용할 수 있습니다. 단, 클라이언트 측 샤딩은 장애 조치를 처리하지 않으므로, 주로 다른 기본 데이터 저장소에서 다시 가져올 수 있는 임시 캐시 데이터에 적합합니다.

클라이언트 측 샤딩 대신 Redis의 네이티브 클러스터링을 사용하려면, 애플리케이션의 `config/database.php` 파일에서 `options.cluster` 설정 값을 `redis`로 지정하세요:

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

기본 `host`, `port`, `database`, `password` 서버 설정 이외에도, Predis는 추가적인 [연결 매개변수](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이 추가 설정 옵션들을 사용하려면, `config/database.php` 파일의 Redis 서버 구성에 옵션을 추가하면 됩니다:

    'default' => [
        'host' => env('REDIS_HOST', 'localhost'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', 6379),
        'database' => 0,
        'read_write_timeout' => 60,
    ],

<a name="the-redis-facade-alias"></a>
#### Redis 파사드 별칭

Laravel의 `config/app.php` 구성 파일에는 프레임워크에서 등록되는 클래스 별칭을 정의하는 `aliases` 배열이 포함되어 있습니다. 기본적으로, phpredis 확장프로그램이 제공하는 `Redis` 클래스명과의 충돌을 피하기 위해 `Redis` 별칭이 포함되어 있지 않습니다. 만약 Predis 클라이언트를 사용하면서 `Redis` 별칭을 추가하고 싶다면, `config/app.php` 파일의 `aliases` 배열에 다음과 같이 추가하세요:

    'aliases' => Facade::defaultAliases()->merge([
        'Redis' => Illuminate\Support\Facades\Redis::class,
    ])->toArray(),

<a name="phpredis"></a>
### phpredis

기본적으로 Laravel은 Redis와 통신할 때 phpredis 확장 프로그램을 사용합니다. Laravel에서 사용할 Redis 클라이언트는 `redis.client` 설정 옵션의 값에 따라 결정되며, 일반적으로는 `REDIS_CLIENT` 환경 변수의 값을 반영합니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        // 나머지 Redis 구성...
    ],

기본 `scheme`, `host`, `port`, `database`, `password` 서버 설정 이외에도, phpredis는 `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `timeout`, `context` 등의 연결 옵션을 추가로 지원합니다. 아래와 같이 `config/database.php` 파일의 Redis 설정에 이러한 옵션들을 추가할 수 있습니다:

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
#### phpredis 직렬화 및 압축

phpredis 확장 프로그램은 다양한 직렬화 및 압축 알고리즘을 사용할 수 있도록 설정할 수 있습니다. 이 알고리즘들은 Redis 설정의 `options` 배열에서 지정할 수 있습니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'options' => [
            'serializer' => Redis::SERIALIZER_MSGPACK,
            'compression' => Redis::COMPRESSION_LZ4,
        ],

        // 나머지 Redis 설정...
    ],

현재 지원되는 직렬화 알고리즘은: `Redis::SERIALIZER_NONE`(기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`입니다.

지원되는 압축 알고리즘은: `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`입니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기

`Redis` [파사드](/docs/{{version}}/facades)의 여러 메서드를 통해 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하므로, 모든 [Redis 명령어](https://redis.io/commands)를 파사드에서 직접 호출할 수 있고, 명령어는 Redis로 바로 전달됩니다. 예를 들어, 아래 예시처럼 `get` 메서드를 호출하여 Redis의 `GET` 명령어를 사용할 수 있습니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\Redis;

    class UserController extends Controller
    {
        /**
         * 주어진 사용자의 프로필 표시
         *
         * @param  int  $id
         * @return \Illuminate\Http\Response
         */
        public function show($id)
        {
            return view('user.profile', [
                'user' => Redis::get('user:profile:'.$id)
            ]);
        }
    }

앞서 언급한 것처럼, 모든 Redis 명령어를 `Redis` 파사드에서 호출할 수 있습니다. Laravel은 매직 메서드를 사용해 명령어를 Redis 서버로 전달합니다. Redis 명령어에 인자가 필요한 경우, 해당 인자를 파사드의 메서드에 넘기면 됩니다:

    use Illuminate\Support\Facades\Redis;

    Redis::set('name', 'Taylor');

    $values = Redis::lrange('names', 5, 10);

또는, `Redis` 파사드의 `command` 메서드를 사용하여 서버에 명령어를 전달할 수 있으며, 첫 번째 인자로 명령어 이름을, 두 번째 인자로 값의 배열을 넘깁니다:

    $values = Redis::command('lrange', ['name', 5, 10]);

<a name="using-multiple-redis-connections"></a>
#### 다수의 Redis 연결 사용

애플리케이션의 `config/database.php` 구성 파일에서 여러 개의 Redis 연결/서버를 정의할 수 있습니다. `Redis` 파사드의 `connection` 메서드를 사용하여 특정 Redis 연결 인스턴스를 가져올 수 있습니다:

    $redis = Redis::connection('connection-name');

기본 Redis 연결 인스턴스를 얻으려면, 추가 인자 없이 `connection` 메서드를 호출하면 됩니다:

    $redis = Redis::connection();

<a name="transactions"></a>
### 트랜잭션

`Redis` 파사드의 `transaction` 메서드는 Redis의 `MULTI`와 `EXEC` 명령을 간편하게 묶어서 사용할 수 있도록 래퍼를 제공합니다. `transaction` 메서드는 클로저를 인자로 받으며, 이 클로저에는 Redis 연결 인스턴스가 전달됩니다. 클로저 내에서 실행된 모든 Redis 명령은 하나의 원자적(atomic) 트랜잭션으로 실행됩니다:

    use Illuminate\Support\Facades\Redis;

    Redis::transaction(function ($redis) {
        $redis->incr('user_visits', 1);
        $redis->incr('total_visits', 1);
    });

> **경고**  
> Redis 트랜잭션을 정의할 때는, Redis 연결에서 값을 조회(get)해서는 안 됩니다. 트랜잭션은 하나의 원자적 연산으로 실행되며, 클로저 내 명령어가 모두 실행된 후에야 실행됩니다.

#### Lua 스크립트

`eval` 메서드는 다수의 Redis 명령을 한 번에 원자적으로 실행하는 또 다른 방법을 제공합니다. 특히, `eval` 메서드는 실행 중에 Redis의 키 값을 조회 및 조작할 수 있다는 장점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 몇 개의 인자를 필요로 하며, 첫 번째는 Lua 스크립트(문자열), 두 번째는 해당 스크립트가 특별히 다루는 키의 개수(정수), 세 번째는 키의 이름 배열입니다. 이후, 스크립트 내에서 사용할 추가 인수를 전달할 수 있습니다.

아래 예제에서는 카운터 값을 증가시키고, 그 값이 5보다 크면 두 번째 카운터도 증가시킵니다. 마지막으로 첫 번째 카운터 값을 반환합니다:

    $value = Redis::eval(<<<'LUA'
        local counter = redis.call("incr", KEYS[1])

        if counter > 5 then
            redis.call("incr", KEYS[2])
        end

        return counter
    LUA, 2, 'first-counter', 'second-counter');

> **경고**  
> Redis 스크립팅에 관한 더 많은 내용은 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 명령어 파이프라이닝

수십 개의 Redis 명령을 실행해야 하는 경우, 각각의 명령마다 서버에 네트워크 요청을 보내는 대신 `pipeline` 메서드를 사용할 수 있습니다. `pipeline` 메서드는 Redis 인스턴스를 인자로 받는 클로저를 받아들입니다. 인스턴스에 여러 명령을 순서대로 내리면, 모두 한 번에 서버로 전송되어 네트워크 트립을 줄일 수 있습니다. 각 명령은 내린 순서대로 실행됩니다:

    use Illuminate\Support\Facades\Redis;

    Redis::pipeline(function ($pipe) {
        for ($i = 0; $i < 1000; $i++) {
            $pipe->set("key:$i", $i);
        }
    });

<a name="pubsub"></a>
## Pub / Sub

Laravel은 Redis의 `publish` 및 `subscribe` 명령어에 대한 편리한 인터페이스를 제공합니다. Redis의 Pub/Sub을 사용하면 특정 "채널"에서 메시지를 수신할 수 있습니다. 다른 애플리케이션이나 다른 프로그래밍 언어로 해당 채널로 메시지를 발행할 수 있으므로, 손쉽게 애플리케이션 및 프로세스 사이에서 통신할 수 있습니다.

먼저, `subscribe` 메서드를 사용해 채널 리스너를 설정해보겠습니다. 이 메서드는 [Artisan 명령어](/docs/{{version}}/artisan) 내에 넣는 것이 좋은데, `subscribe` 메서드는 장시간 실행되는 프로세스를 시작하기 때문입니다:

    <?php

    namespace App\Console\Commands;

    use Illuminate\Console\Command;
    use Illuminate\Support\Facades\Redis;

    class RedisSubscribe extends Command
    {
        /**
         * 콘솔 명령 이름 및 시그니처
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
         *
         * @return mixed
         */
        public function handle()
        {
            Redis::subscribe(['test-channel'], function ($message) {
                echo $message;
            });
        }
    }

이제 `publish` 메서드를 사용해 채널에 메시지를 발행할 수 있습니다:

    use Illuminate\Support\Facades\Redis;

    Route::get('/publish', function () {
        // ...

        Redis::publish('test-channel', json_encode([
            'name' => 'Adam Wathan'
        ]));
    });

<a name="wildcard-subscriptions"></a>
#### 와일드카드 구독

`psubscribe` 메서드를 사용하면, 와일드카드 채널 구독이 가능합니다. 이는 모든 채널의 메시지를 포착하고자 할 때 유용합니다. 채널 이름은 클로저의 두 번째 인자로 전달됩니다:

    Redis::psubscribe(['*'], function ($message, $channel) {
        echo $message;
    });

    Redis::psubscribe(['users.*'], function ($message, $channel) {
        echo $message;
    });
