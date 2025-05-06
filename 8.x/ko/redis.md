# Redis

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [phpredis](#phpredis)
- [Redis와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [파이프라이닝 명령어](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개

[Redis](https://redis.io)은 오픈 소스의 고급 키-값 저장소입니다. 키에 [문자열](https://redis.io/topics/data-types#strings), [해시](https://redis.io/topics/data-types#hashes), [리스트](https://redis.io/topics/data-types#lists), [셋](https://redis.io/topics/data-types#sets), [정렬된 셋](https://redis.io/topics/data-types#sorted-sets) 등 다양한 데이터 구조를 저장할 수 있기 때문에, 데이터 구조 서버라고도 불립니다.

Laravel에서 Redis를 사용하기 전에 [phpredis](https://github.com/phpredis/phpredis) PHP 확장 모듈을 PECL로 설치 및 사용하는 것을 권장합니다. 이 확장 모듈은 "user-land" PHP 패키지보다 설치가 복잡하지만, Redis를 많이 사용하는 애플리케이션에서 더 나은 성능을 제공할 수 있습니다. [Laravel Sail](/docs/{{version}}/sail)을 사용 중이라면, 이 확장 모듈은 애플리케이션의 Docker 컨테이너에 이미 설치되어 있습니다.

phpredis 확장 모듈을 설치할 수 없다면, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 순수 PHP로 작성된 Redis 클라이언트이며, 추가 확장 모듈이 필요하지 않습니다:

```bash
composer require predis/predis
```

<a name="configuration"></a>
## 설정

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 구성할 수 있습니다. 이 파일 내의 `redis` 배열에서 애플리케이션에서 사용하는 Redis 서버들을 지정하게 됩니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'default' => [
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD', null),
            'port' => env('REDIS_PORT', 6379),
            'database' => env('REDIS_DB', 0),
        ],

        'cache' => [
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD', null),
            'port' => env('REDIS_PORT', 6379),
            'database' => env('REDIS_CACHE_DB', 1),
        ],

    ],

설정 파일에 정의된 각 Redis 서버는 이름, 호스트, 포트가 필요합니다. 단, 단일 URL로 Redis 연결을 표현하는 경우에는 예외입니다:

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
#### 연결 스킴 구성하기

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 그러나 `scheme` 설정 옵션을 Redis 서버 구성 배열에 명시함으로써 TLS/SSL 암호화 연결도 가능합니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'default' => [
            'scheme' => 'tls',
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD', null),
            'port' => env('REDIS_PORT', 6379),
            'database' => env('REDIS_DB', 0),
        ],

    ],

<a name="clusters"></a>
### 클러스터

애플리케이션에서 여러 대의 Redis 서버로 구성된 클러스터를 사용할 경우, Redis 설정의 `clusters` 키에 클러스터를 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로, 애플리케이션의 `config/database.php`에 추가해주어야 합니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'clusters' => [
            'default' => [
                [
                    'host' => env('REDIS_HOST', 'localhost'),
                    'password' => env('REDIS_PASSWORD', null),
                    'port' => env('REDIS_PORT', 6379),
                    'database' => 0,
                ],
            ],
        ],

    ],

기본적으로 클러스터는 클라이언트 측 샤딩(client-side sharding)을 활용하며, 여러 노드를 묶어 많은 양의 사용 가능한 RAM을 확보할 수 있습니다. 단, 클라이언트 측 샤딩은 장애조치(failover)를 제공하지 않으므로, 주로 다른 주요 데이터 저장소에서 가져올 수 있는 임시 캐시 데이터를 저장하는 용도에 적합합니다.

클라이언트 측 샤딩 대신 원래의 Redis 클러스터링을 사용하고 싶다면, 애플리케이션의 `config/database.php` 파일에서 `options.cluster` 구성을 `redis`로 지정하면 됩니다:

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

애플리케이션이 Predis 패키지를 통해 Redis와 상호작용하도록 하려면, `REDIS_CLIENT` 환경 변수 값이 `predis`여야 합니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'predis'),

        // ...
    ],

기본적인 `host`, `port`, `database`, `password` 설정 옵션 이외에도, Predis는 각 Redis 서버에 대해 추가 [연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이러한 구성 옵션들을 사용하려면 애플리케이션의 `config/database.php` 파일에 추가하면 됩니다:

    'default' => [
        'host' => env('REDIS_HOST', 'localhost'),
        'password' => env('REDIS_PASSWORD', null),
        'port' => env('REDIS_PORT', 6379),
        'database' => 0,
        'read_write_timeout' => 60,
    ],

<a name="the-redis-facade-alias"></a>
#### Redis 파사드 별칭(Facade Alias)

Laravel의 `config/app.php` 파일에는 프레임워크에서 등록할 클래스 별칭이 정의된 `aliases` 배열이 있습니다. 편의상, Laravel에서 제공하는 각 [파사드](/docs/{{version}}/facades)에 대해 별칭이 포함되어 있지만, `phpredis` 확장 모듈이 제공하는 `Redis` 클래스와 충돌하기 때문에 `Redis` 별칭은 기본적으로 비활성화되어 있습니다. Predis 클라이언트를 사용하고 별칭을 활성화하려면, 애플리케이션의 `config/app.php` 파일에서 해당 별칭의 주석을 해제하면 됩니다.

<a name="phpredis"></a>
### phpredis

Laravel은 기본적으로 Redis와 통신할 때 phpredis 확장 모듈을 사용합니다. Laravel이 사용할 Redis 클라이언트는 `redis.client` 설정 옵션 값에 의해 결정되며, 일반적으로 `REDIS_CLIENT` 환경 변수 값을 따릅니다:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        // 그 외 Redis 설정...
    ],

기본적인 `scheme`, `host`, `port`, `database`, `password` 설정 옵션 외에, phpredis는 추가적으로 `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `timeout`, `context` 등의 연결 파라미터를 지원합니다. 이 옵션들은 `config/database.php`에서 추가할 수 있습니다:

    'default' => [
        'host' => env('REDIS_HOST', 'localhost'),
        'password' => env('REDIS_PASSWORD', null),
        'port' => env('REDIS_PORT', 6379),
        'database' => 0,
        'read_timeout' => 60,
        'context' => [
            // 'auth' => ['username', 'secret'],
            // 'stream' => ['verify_peer' => false],
        ],
    ],

<a name="phpredis-serialization"></a>
#### phpredis 직렬화 및 압축(Serialization & Compression)

phpredis 확장 모듈은 다양한 직렬화 및 압축 알고리즘도 지원합니다. 이 알고리즘들은 Redis 설정의 `options` 배열을 통해 구성할 수 있습니다:

    use Redis;

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'options' => [
            'serializer' => Redis::SERIALIZER_MSGPACK,
            'compression' => Redis::COMPRESSION_LZ4,
        ],

        // 그 외 Redis 설정...
    ],

현재 지원되는 직렬화 알고리즘: `Redis::SERIALIZER_NONE` (기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`

지원되는 압축 알고리즘: `Redis::COMPRESSION_NONE` (기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기

Redis와 상호작용할 때는 `Redis` [파사드](/docs/{{version}}/facades)의 다양한 메서드를 사용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하므로, [Redis 명령어](https://redis.io/commands)를 그대로 파사드 메서드로 호출하면 명령어가 Redis로 바로 전달됩니다. 아래 예시에서 `Redis` 파사드의 `get` 메서드를 호출하여 Redis의 GET 명령을 실행합니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\Redis;

    class UserController extends Controller
    {
        /**
         * 주어진 사용자의 프로필을 표시합니다.
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

앞에서 언급한 것처럼, `Redis` 파사드에서 Redis의 모든 명령어를 호출할 수 있습니다. Laravel은 매직 메서드(magic methods)를 활용해 명령을 Redis 서버로 전달합니다. Redis 명령어가 인자를 요구하는 경우, 해당 인자들을 파사드의 메서드에 전달하면 됩니다:

    use Illuminate\Support\Facades\Redis;

    Redis::set('name', 'Taylor');

    $values = Redis::lrange('names', 5, 10);

또는, `Redis` 파사드의 `command` 메서드를 사용해 명령어 이름을 첫 번째 인자로, 값들의 배열을 두 번째 인자로 전달하여 명령을 보낼 수 있습니다:

    $values = Redis::command('lrange', ['name', 5, 10]);

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 파일에서는 여러 Redis 연결/서버를 정의할 수 있습니다. 특정 Redis 연결로 접속하려면 `Redis` 파사드의 `connection` 메서드를 이용하면 됩니다:

    $redis = Redis::connection('connection-name');

기본 Redis 연결 인스턴스를 얻으려면 인자 없이 `connection` 메서드를 호출하세요:

    $redis = Redis::connection();

<a name="transactions"></a>
### 트랜잭션

`Redis` 파사드의 `transaction` 메서드는 Redis의 기본 `MULTI` 및 `EXEC` 명령어를 간편하게 래핑합니다. `transaction` 메서드는 하나의 클로저를 인자로 받으며, 이 클로저는 Redis 연결 인스턴스를 받아, 원하는 모든 명령어를 해당 인스턴스에 전달할 수 있습니다. 클로저 내에서 수행된 모든 명령어는 하나의 원자적 트랜잭션으로 실행됩니다:

    use Illuminate\Support\Facades\Redis;

    Redis::transaction(function ($redis) {
        $redis->incr('user_visits', 1);
        $redis->incr('total_visits', 1);
    });

> {note} Redis 트랜잭션을 정의할 때는 Redis 연결로부터 값을 가져올 수 없습니다. 트랜잭션은 하나의 원자적 작업으로 실행되며, 클로저 전체가 모든 명령어를 실행한 뒤에 비로소 진행됩니다.

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령을 하나의 원자적 작업으로 실행하는 또다른 방법을 제공합니다. `eval` 메서드는 그 과정에서 Redis 키의 값을 조회하고 조작할 수 있다는 장점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 몇몇 인자를 필요로 합니다. 첫 번째 인자는 메서드에 넘길 Lua 스크립트(문자열)이고, 두 번째 인자는 스크립트가 다루는 키의 개수(정수), 그 다음은 해당 키들의 이름, 마지막으로 스크립트 내에서 사용할 추가 인자를 순서대로 전달합니다.

아래 예시에서는 카운터를 증가시키고, 그 값이 5를 초과하면 두 번째 카운터도 증가시키며, 마지막으로 첫 번째 카운터의 값을 반환합니다:

    $value = Redis::eval(<<<'LUA'
        local counter = redis.call("incr", KEYS[1])

        if counter > 5 then
            redis.call("incr", KEYS[2])
        end

        return counter
    LUA, 2, 'first-counter', 'second-counter');

> {note} Redis 스크립팅에 대한 더 자세한 정보는 [Redis 공식문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 파이프라이닝 명령어

수십 개의 Redis 명령어를 한꺼번에 실행하고 싶을 때가 있을 수 있습니다. 이럴 때는 각 명령마다 Redis 서버로 네트워크 요청을 하기보다 `pipeline` 메서드를 사용할 수 있습니다. `pipeline` 메서드는 Redis 인스턴스를 받는 하나의 클로저를 인자로 받습니다. 클로저 내에서 모든 명령어를 해당 Redis 인스턴스로 발행하면 한 번에 모두 서버로 전송되어 네트워크 왕복 수를 줄일 수 있습니다. 명령어는 입력한 순서대로 실행됩니다:

    use Illuminate\Support\Facades\Redis;

    Redis::pipeline(function ($pipe) {
        for ($i = 0; $i < 1000; $i++) {
            $pipe->set("key:$i", $i);
        }
    });

<a name="pubsub"></a>
## Pub / Sub

Laravel은 Redis의 `publish`와 `subscribe` 명령을 위한 간편한 인터페이스를 제공합니다. 이 명령어들을 이용하면 특정 "채널"에서 메시지를 수신할 수 있습니다. 다른 애플리케이션이나 동작하는 프로세스, 혹은 다른 프로그래밍 언어로 채널에 메시지를 발행(publish)할 수 있으므로 애플리케이션과 프로세스 간 통신을 손쉽게 할 수 있습니다.

먼저, `subscribe` 메서드를 이용해 채널 리스너를 설정해보겠습니다. `subscribe` 메서드는 장시간 실행되는(블로킹) 프로세스이므로, [Artisan 커맨드](/docs/{{version}}/artisan) 내에서 호출하는 것이 좋습니다:

    <?php

    namespace App\Console\Commands;

    use Illuminate\Console\Command;
    use Illuminate\Support\Facades\Redis;

    class RedisSubscribe extends Command
    {
        /**
         * 콘솔 커맨드의 이름 및 시그니처
         *
         * @var string
         */
        protected $signature = 'redis:subscribe';

        /**
         * 콘솔 커맨드 설명
         *
         * @var string
         */
        protected $description = 'Redis 채널 구독';

        /**
         * 콘솔 커맨드 실행
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

`psubscribe` 메서드를 통해 와일드카드 채널을 구독할 수 있습니다. 이는 모든 채널 혹은 특정 패턴의 채널에서 발행된 메시지를 한꺼번에 수신할 때 유용합니다. 채널 이름은 두 번째 인자로 클로저에 전달됩니다:

    Redis::psubscribe(['*'], function ($message, $channel) {
        echo $message;
    });

    Redis::psubscribe(['users.*'], function ($message, $channel) {
        echo $message;
    });
