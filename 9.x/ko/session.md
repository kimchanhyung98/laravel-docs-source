# HTTP 세션

- [소개](#introduction)
    - [구성](#configuration)
    - [드라이버 사전 요구사항](#driver-prerequisites)
- [세션과 상호작용하기](#interacting-with-the-session)
    - [데이터 조회](#retrieving-data)
    - [데이터 저장](#storing-data)
    - [Flash 데이터](#flash-data)
    - [데이터 삭제](#deleting-data)
    - [세션 ID 재생성](#regenerating-the-session-id)
- [세션 블로킹](#session-blocking)
- [커스텀 세션 드라이버 추가](#adding-custom-session-drivers)
    - [드라이버 구현](#implementing-the-driver)
    - [드라이버 등록](#registering-the-driver)

<a name="introduction"></a>
## 소개

HTTP 기반 애플리케이션은 상태가 없기 때문에, 세션은 여러 요청에 걸쳐 사용자 정보를 저장할 수 있는 방법을 제공합니다. 이 사용자 정보는 일반적으로 후속 요청에서 액세스할 수 있는 영구 저장소/백엔드에 저장됩니다.

Laravel은 표현력 있고 일관된 API를 통해 접근할 수 있는 다양한 세션 백엔드를 기본으로 제공합니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스 등과 같은 인기 있는 백엔드도 지원됩니다.

<a name="configuration"></a>
### 구성

애플리케이션의 세션 구성 파일은 `config/session.php`에 저장되어 있습니다. 이 파일의 다양한 옵션을 반드시 검토하세요. 기본적으로 Laravel은 `file` 세션 드라이버를 사용하도록 설정되어 있으며, 이는 많은 애플리케이션에 적합합니다. 만약 여러 웹 서버에 걸쳐 애플리케이션이 로드 밸런싱될 경우, 모든 서버에서 접근 가능한 Redis나 데이터베이스 같은 중앙 집중형 저장소를 선택해야 합니다.

세션의 `driver` 구성 옵션은 각 요청에 대해 세션 데이터가 저장되는 위치를 정의합니다. Laravel은 여러 훌륭한 드라이버를 기본으로 제공합니다:

<div class="content-list" markdown="1">

- `file` - 세션이 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션이 보안 및 암호화된 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 이러한 고속 캐시 기반 저장소에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며 영구적으로 저장되지 않습니다.

</div>

> **참고**
> `array` 드라이버는 주로 [테스트](/docs/{{version}}/testing) 중에 사용되며 세션에 저장되는 데이터가 영구적으로 저장되지 않도록 합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 때는 세션 레코드를 저장할 테이블을 생성해야 합니다. 아래는 테이블을 위한 예시 `Schema` 선언입니다:

    Schema::create('sessions', function ($table) {
        $table->string('id')->primary();
        $table->foreignId('user_id')->nullable()->index();
        $table->string('ip_address', 45)->nullable();
        $table->text('user_agent')->nullable();
        $table->text('payload');
        $table->integer('last_activity')->index();
    });

`session:table` Artisan 명령어를 사용하여 이 마이그레이션을 생성할 수 있습니다. 데이터베이스 마이그레이션에 대해 더 알고 싶다면 [마이그레이션 문서](/docs/{{version}}/migrations)를 참고하세요:

```shell
php artisan session:table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 구성에 대한 자세한 내용은 Laravel의 [Redis 문서](/docs/{{version}}/redis#configuration)를 참조하세요.

> **참고**
> `session` 구성 파일의 `connection` 옵션을 사용하면 세션이 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기

<a name="retrieving-data"></a>
### 데이터 조회

Laravel에서 세션 데이터를 다루는 주요 방법은 두 가지입니다: 전역 `session` 헬퍼와 `Request` 인스턴스를 사용하는 방법입니다. 먼저, 라우트 클로저나 컨트롤러 메소드에서 타입 힌팅을 통해 의존성 주입되는 `Request` 인스턴스를 사용한 세션 접근 예시를 살펴보겠습니다. 컨트롤러 메소드의 의존성은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입된다는 점을 기억하세요:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * 지정 사용자 프로필 표시
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function show(Request $request, $id)
        {
            $value = $request->session()->get('key');

            //
        }
    }

세션에서 항목을 조회할 때, `get` 메소드의 두 번째 인수로 기본값을 전달할 수 있습니다. 지정한 키가 세션에 없을 경우 이 기본값이 반환됩니다. `get`의 기본값에 클로저를 전달하면, 해당 키가 없을 때 클로저가 실행되고 그 반환값이 사용됩니다:

    $value = $request->session()->get('key', 'default');

    $value = $request->session()->get('key', function () {
        return 'default';
    });

<a name="the-global-session-helper"></a>
#### 전역 Session 헬퍼

전역 PHP 함수 `session`을 사용해 세션에 데이터를 저장하거나 조회할 수 있습니다. 이 헬퍼를 문자열 한 개로 호출하면 해당 세션 키의 값을 반환합니다. 키/값 쌍의 배열을 넘기면 값을 세션에 저장합니다:

    Route::get('/home', function () {
        // 세션에서 데이터 조회
        $value = session('key');

        // 기본값 지정
        $value = session('key', 'default');

        // 세션에 데이터 저장
        session(['key' => 'value']);
    });

> **참고**
> HTTP 요청 객체를 통해서든 전역 `session` 헬퍼를 통해서든 실질적인 차이는 거의 없습니다. 두 방법 모두 테스트에서 제공되는 `assertSessionHas` 메소드로 [테스트](/docs/{{version}}/testing)할 수 있습니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 조회

세션 내 모든 데이터를 조회하려면 `all` 메소드를 사용할 수 있습니다:

    $data = $request->session()->all();

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목 존재 여부 확인

세션에 항목이 존재하는지 확인하려면 `has` 메소드를 사용할 수 있습니다. `has`는 항목이 존재하고 `null`이 아닐 때 `true`를 반환합니다:

    if ($request->session()->has('users')) {
        //
    }

값이 `null`이어도 항목의 존재 자체만 확인하려면 `exists` 메소드를 사용합니다:

    if ($request->session()->exists('users')) {
        //
    }

항목이 세션에 존재하지 않을 때를 확인하려면 `missing` 메소드를 사용합니다. `missing`은 항목이 없으면 `true`를 반환합니다:

    if ($request->session()->missing('users')) {
        //
    }

<a name="storing-data"></a>
### 데이터 저장

세션에 데이터를 저장하려면 일반적으로 요청 인스턴스의 `put` 메소드 또는 전역 `session` 헬퍼를 사용합니다:

    // 요청 인스턴스를 통해 저장
    $request->session()->put('key', 'value');

    // 전역 "session" 헬퍼를 통해 저장
    session(['key' => 'value']);

<a name="pushing-to-array-session-values"></a>
#### 배열 세션 값에 추가

`push` 메소드를 사용하면 배열 타입의 세션 값에 새 값을 추가할 수 있습니다. 예를 들어, `user.teams` 키에 팀 이름의 배열이 있을 때 새 값을 다음과 같이 추가할 수 있습니다:

    $request->session()->push('user.teams', 'developers');

<a name="retrieving-deleting-an-item"></a>
#### 항목 조회 & 삭제

`pull` 메소드는 세션에서 항목을 조회하고 즉시 삭제합니다:

    $value = $request->session()->pull('key', 'default');

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가/감소

세션 데이터에 정수가 저장되어 있고 이를 증가 또는 감소시키고 싶을 때는 `increment`, `decrement` 메소드를 사용할 수 있습니다:

    $request->session()->increment('count');

    $request->session()->increment('count', $incrementBy = 2);

    $request->session()->decrement('count');

    $request->session()->decrement('count', $decrementBy = 2);

<a name="flash-data"></a>
### Flash 데이터

다음 요청까지만 세션에 임시로 값을 저장하고 싶을 때는 `flash` 메소드를 사용할 수 있습니다. 이렇게 저장된 데이터는 바로 다음 HTTP 요청까지 사용할 수 있으며, 그 이후에는 자동으로 삭제됩니다. Flash 데이터는 일시적 상태 메시지에 주로 유용합니다:

    $request->session()->flash('status', '작업이 성공적으로 완료되었습니다!');

Flash 데이터를 여러 요청 동안 유지하려면 `reflash` 메소드를 사용할 수 있습니다. 특정 Flash 데이터만 유지하려면 `keep` 메소드를 사용하세요:

    $request->session()->reflash();

    $request->session()->keep(['username', 'email']);

Flash 데이터를 현재 요청에서만 유지하려면 `now` 메소드를 사용하세요:

    $request->session()->now('status', '작업이 성공적으로 완료되었습니다!');

<a name="deleting-data"></a>
### 데이터 삭제

`forget` 메소드는 세션에서 특정 데이터를 삭제합니다. 세션의 모든 데이터를 삭제하려면 `flush` 메소드를 사용하면 됩니다:

    // 단일 키 삭제
    $request->session()->forget('name');

    // 여러 키 삭제
    $request->session()->forget(['name', 'status']);

    $request->session()->flush();

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성

세션 ID를 재생성하는 것은 애플리케이션이 [세션 고정 공격](https://owasp.org/www-community/attacks/Session_fixation)에 악용당하지 않도록 막기 위해 종종 필요합니다.

Laravel은 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)이나 [Laravel Fortify](/docs/{{version}}/fortify)를 사용하는 경우 인증 중에 자동으로 세션 ID를 재생성합니다. 그러나 세션 ID를 수동으로 재생성해야 한다면 `regenerate` 메소드를 사용할 수 있습니다:

    $request->session()->regenerate();

세션 ID를 재생성하고 세션의 모든 데이터를 동시에 삭제하려면 `invalidate` 메소드를 사용할 수 있습니다:

    $request->session()->invalidate();

<a name="session-blocking"></a>
## 세션 블로킹

> **경고**
> 세션 블로킹을 사용하려면 [원자적 락](/docs/{{version}}/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `dynamodb`, `redis`, `database` 드라이버가 해당합니다. 또한 `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 Laravel은 동일한 세션을 사용하는 요청이 동시에 실행될 수 있도록 허용합니다. 예를 들어, JavaScript HTTP 라이브러리를 사용하여 애플리케이션에 두 개의 HTTP 요청을 보내면 두 요청이 동시에 실행됩니다. 대부분의 애플리케이션에서는 문제가 없지만, 특정 상황에서는 두 엔드포인트가 동시에 세션에 데이터를 쓸 경우 세션 데이터 유실이 발생할 수 있습니다.

이를 방지하기 위해, Laravel은 특정 세션에 대한 동시 요청 수를 제한하는 기능을 제공합니다. 시작하려면 라우트 정의에 `block` 메소드를 연결하기만 하면 됩니다. 이 예시에서 `/profile` 엔드포인트로 들어오는 요청은 세션 락을 획득합니다. 이 락이 유지되는 동안 동일한 세션 ID를 공유하는 `/profile` 또는 `/order` 엔드포인트로의 요청은 첫 번째 요청이 끝날 때까지 대기합니다:

    Route::post('/profile', function () {
        //
    })->block($lockSeconds = 10, $waitSeconds = 10)

    Route::post('/order', function () {
        //
    })->block($lockSeconds = 10, $waitSeconds = 10)

`block` 메소드는 두 개의 선택적 인수를 받습니다. 첫 번째 인수는 세션 락이 최대 몇 초 동안 유지될지이며, 요청이 더 빨리 종료되면 락도 빨리 해제됩니다.

두 번째 인수는 요청이 세션 락을 획득하려고 시도하는 동안 대기할 최대 시간을 의미합니다. 정해진 시간 내에 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

두 인수 모두 생략할 경우 락은 최대 10초 동안 유지되며, 락 획득 대기 시간도 최대 10초가 됩니다:

    Route::post('/profile', function () {
        //
    })->block()

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가

<a name="implementing-the-driver"></a>
#### 드라이버 구현

기존 세션 드라이버가 애플리케이션 요구사항에 맞지 않을 경우, Laravel은 자체 세션 핸들러를 작성할 수 있도록 지원합니다. 커스텀 세션 드라이버는 PHP 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스에는 몇 가지 기본적인 메소드가 포함되어 있습니다. MongoDB에 대한 기본 예시는 다음과 같습니다:

    <?php

    namespace App\Extensions;

    class MongoSessionHandler implements \SessionHandlerInterface
    {
        public function open($savePath, $sessionName) {}
        public function close() {}
        public function read($sessionId) {}
        public function write($sessionId, $data) {}
        public function destroy($sessionId) {}
        public function gc($lifetime) {}
    }

> **참고**
> Laravel은 확장 코드를 저장할 디렉터리를 기본 제공하지 않습니다. 원하는 곳에 자유롭게 둘 수 있습니다. 이 예제에서는 `Extensions` 디렉터리를 생성해 `MongoSessionHandler`를 보관했습니다.

각 메소드의 역할을 간략히 살펴보면 다음과 같습니다:

<div class="content-list" markdown="1">

- `open` 메소드는 주로 파일 기반 세션 스토어에서 사용됩니다. Laravel의 `file` 세션 드라이버를 사용할 때도 거의 비워둘 수 있습니다.
- `close` 메소드도 `open`과 마찬가지로 대부분의 드라이버에서는 구현이 필요 없습니다.
- `read` 메소드는 주어진 `$sessionId`에 연결된 세션 데이터의 문자열 버전을 반환해야 합니다. 데이터의 직렬화나 인코딩은 Laravel이 담당하므로 직접 처리할 필요가 없습니다.
- `write` 메소드는 주어진 `$sessionId`와 연결된 `$data` 문자열을 MongoDB 또는 원하는 저장소에 기록해야 합니다. 역시 직렬화는 Laravel에서 이미 처리하므로 신경 쓸 필요 없습니다.
- `destroy` 메소드는 해당 `$sessionId`에 연결된 데이터를 영구 저장소에서 삭제해야 합니다.
- `gc` 메소드는 주어진 `$lifetime`(UNIX 타임스탬프)보다 오래된 모든 세션 데이터를 삭제해야 합니다. Memcached나 Redis처럼 자동 만료 시스템에서는 비워둘 수 있습니다.

</div>

<a name="registering-the-driver"></a>
#### 드라이버 등록

드라이버가 구현되면 Laravel에 등록할 수 있습니다. 세션 백엔드에 드라이버를 추가하려면 `Session` [파사드](/docs/{{version}}/facades)가 제공하는 `extend` 메소드를 사용하세요. [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메소드에서 호출해야 합니다. 기존의 `App\Providers\AppServiceProvider`에서 사용하거나 새로운 프로바이더를 만들어도 됩니다:

    <?php

    namespace App\Providers;

    use App\Extensions\MongoSessionHandler;
    use Illuminate\Support\Facades\Session;
    use Illuminate\Support\ServiceProvider;

    class SessionServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스 등록
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * 애플리케이션 서비스 부트스트랩
         *
         * @return void
         */
        public function boot()
        {
            Session::extend('mongo', function ($app) {
                // SessionHandlerInterface 구현 반환
                return new MongoSessionHandler;
            });
        }
    }

세션 드라이버 등록을 완료했다면, `config/session.php` 구성 파일에서 `mongo` 드라이버를 사용할 수 있습니다.