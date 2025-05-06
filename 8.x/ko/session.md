# HTTP 세션

- [소개](#소개)
    - [설정](#설정)
    - [드라이버 사전 준비 사항](#드라이버-사전-준비-사항)
- [세션과 상호작용하기](#세션과-상호작용하기)
    - [데이터 조회](#데이터-조회)
    - [데이터 저장](#데이터-저장)
    - [Flash 데이터](#flash-데이터)
    - [데이터 삭제](#데이터-삭제)
    - [세션 ID 재생성](#세션-id-재생성)
- [세션 블로킹](#세션-블로킹)
- [커스텀 세션 드라이버 추가](#커스텀-세션-드라이버-추가)
    - [드라이버 구현](#드라이버-구현)
    - [드라이버 등록](#드라이버-등록)

<a name="introduction"></a>
## 소개

HTTP 기반 애플리케이션은 상태를 유지하지 않기 때문에, 세션은 여러 요청에 걸쳐 사용자 정보를 저장할 수 있는 방법을 제공합니다. 이러한 사용자 정보는 일반적으로 지속 가능한 저장소(백엔드)에 저장되어 이후 요청에서 접근할 수 있습니다.

Laravel은 다양한 세션 백엔드를 제공하며, 표현적이고 통합된 API를 통해 접근할 수 있습니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스와 같은 인기 있는 백엔드에 대한 지원도 포함되어 있습니다.

<a name="configuration"></a>
### 설정

애플리케이션의 세션 설정 파일은 `config/session.php`에 저장됩니다. 이 파일에서 제공되는 옵션들을 반드시 검토하세요. 기본적으로 Laravel은 `file` 세션 드라이버를 사용하도록 설정되어 있으며, 이는 많은 애플리케이션에서 잘 동작합니다. 만약 애플리케이션이 여러 웹 서버에 분산되어 있다면, 모든 서버에서 접근 가능한 중앙 저장소(예: Redis, 데이터베이스 등)를 선택해야 합니다.

세션의 `driver` 설정 옵션은 각 요청마다 세션 데이터가 어디에 저장될지를 정의합니다. Laravel은 여러 훌륭한 드라이버를 기본으로 제공합니다:

<div class="content-list" markdown="1">

- `file` - 세션이 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션이 보안 암호화 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 이러한 빠른 캐시 기반 저장소에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며, 지속되지 않습니다.

</div>

> {tip} array 드라이버는 주로 [테스트](/docs/{{version}}/testing)용으로 사용되며, 세션에 저장된 데이터가 영구적으로 저장되지 않도록 합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 때는 세션 레코드를 저장할 테이블을 만들어야 합니다. 아래에 샘플 `Schema` 선언 예시가 있습니다:

    Schema::create('sessions', function ($table) {
        $table->string('id')->primary();
        $table->foreignId('user_id')->nullable()->index();
        $table->string('ip_address', 45)->nullable();
        $table->text('user_agent')->nullable();
        $table->text('payload');
        $table->integer('last_activity')->index();
    });

이 마이그레이션을 생성하려면 `session:table` 아티즌(Artisan) 명령어를 사용하면 됩니다. 데이터베이스 마이그레이션에 대해 더 알고 싶다면 전체 [마이그레이션 문서](/docs/{{version}}/migrations)를 참고하세요:

    php artisan session:table

    php artisan migrate

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하기 전에, PECL을 통해 PhpRedis PHP 확장을 설치하거나 Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 설정에 관한 자세한 내용은 Laravel의 [Redis 문서](/docs/{{version}}/redis#configuration)를 참고하세요.

> {tip} `session` 설정 파일에서, `connection` 옵션을 통해 세션에서 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기

<a name="retrieving-data"></a>
### 데이터 조회

Laravel에서 세션 데이터와 작업하는 기본적인 방법은 크게 두 가지가 있습니다: 전역 `session` 헬퍼와 `Request` 인스턴스를 사용하는 방법입니다. 먼저, `Request` 인스턴스를 통해 세션에 접근하는 방법을 살펴보겠습니다. 이는 라우트 클로저나 컨트롤러 메소드에서 타입 힌트로 사용할 수 있습니다. 참고로, 컨트롤러 메소드의 의존성은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입됩니다.

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * 주어진 사용자의 프로필을 보여줍니다.
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

세션에서 항목을 조회할 때, `get` 메소드의 두 번째 인자로 기본값을 전달할 수 있습니다. 지정한 키가 세션에 존재하지 않을 경우 이 기본값이 반환됩니다. 만약 기본값으로 클로저를 전달하고 요청한 키가 존재하지 않으면, 해당 클로저가 실행되어 그 결과가 반환됩니다:

    $value = $request->session()->get('key', 'default');

    $value = $request->session()->get('key', function () {
        return 'default';
    });

<a name="the-global-session-helper"></a>
#### 전역 Session 헬퍼

전역 `session` PHP 함수를 사용하여 세션 데이터를 조회하고 저장할 수도 있습니다. `session` 헬퍼에 단일 문자열 인자를 전달하면 해당 세션 키의 값을 반환합니다. 키/값 쌍의 배열을 전달하면 해당 값들을 세션에 저장합니다:

    Route::get('/home', function () {
        // 세션에서 데이터를 조회합니다...
        $value = session('key');

        // 기본값을 지정합니다...
        $value = session('key', 'default');

        // 세션에 데이터를 저장합니다...
        session(['key' => 'value']);
    });

> {tip} HTTP 요청 인스턴스를 사용하는 방법과 전역 `session` 헬퍼를 사용하는 방법 간에는 실제적인 차이가 거의 없습니다. 두 방법 모두 테스트 케이스에서 사용 가능한 `assertSessionHas` 메소드를 통해 [테스트할 수 있습니다](/docs/{{version}}/testing).

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 조회

세션 내의 모든 데이터를 조회하려면 `all` 메소드를 사용할 수 있습니다:

    $data = $request->session()->all();

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션 내에 항목 존재 여부 확인

세션에 항목이 존재하는지 확인하려면 `has` 메소드를 사용하세요. `has` 메소드는 값이 존재하고 `null`이 아닐 때 `true`를 반환합니다:

    if ($request->session()->has('users')) {
        //
    }

값이 `null`이라도 세션에 항목이 존재하는지 확인하고 싶다면 `exists` 메소드를 사용하세요:

    if ($request->session()->exists('users')) {
        //
    }

세션에 항목이 존재하지 않을 때를 확인하려면 `missing` 메소드를 사용하세요. 이 메소드는 값이 `null`이거나 항목이 존재하지 않으면 `true`를 반환합니다:

    if ($request->session()->missing('users')) {
        //
    }

<a name="storing-data"></a>
### 데이터 저장

세션에 데이터를 저장하려면 일반적으로 요청 인스턴스의 `put` 메소드나 전역 `session` 헬퍼를 사용합니다:

    // 요청 인스턴스를 통해...
    $request->session()->put('key', 'value');

    // 전역 "session" 헬퍼를 통해...
    session(['key' => 'value']);

<a name="pushing-to-array-session-values"></a>
#### 배열 세션 값에 값 추가하기

`push` 메소드를 사용하면 배열 타입의 세션 값에 새 값을 추가할 수 있습니다. 예를 들어, `user.teams` 키가 팀 이름의 배열을 포함하고 있다면 다음과 같이 새 값을 추가할 수 있습니다:

    $request->session()->push('user.teams', 'developers');

<a name="retrieving-deleting-an-item"></a>
#### 항목 조회 및 삭제

`pull` 메소드는 한 번에 세션에서 항목을 조회하고 삭제합니다:

    $value = $request->session()->pull('key', 'default');

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가 및 감소

세션 데이터가 정수형이고 이를 증가 또는 감소시키고 싶다면, `increment` 및 `decrement` 메소드를 사용할 수 있습니다:

    $request->session()->increment('count');

    $request->session()->increment('count', $incrementBy = 2);

    $request->session()->decrement('count');

    $request->session()->decrement('count', $decrementBy = 2);

<a name="flash-data"></a>
### Flash 데이터

때때로 다음 요청에서만 세션에 항목을 저장하고 싶을 수 있습니다. 이를 위해 `flash` 메소드를 사용할 수 있습니다. 이 메소드로 저장된 데이터는 즉시 사용할 수 있으며, 이후 HTTP 요청에서만 유지됩니다. 그 후에는 해당 데이터가 삭제됩니다. Flash 데이터는 보통 짧은 상태 메시지에 유용합니다:

    $request->session()->flash('status', '작업이 성공적으로 완료되었습니다!');

Flash 데이터를 여러 요청 동안 유지하려면 `reflash` 메소드를 사용하세요. 특정 Flash 데이터만 유지하려면 `keep` 메소드를 사용할 수 있습니다:

    $request->session()->reflash();

    $request->session()->keep(['username', 'email']);

Flash 데이터를 현재 요청에만 유지하려면 `now` 메소드를 사용할 수 있습니다:

    $request->session()->now('status', '작업이 성공적으로 완료되었습니다!');

<a name="deleting-data"></a>
### 데이터 삭제

`forget` 메소드는 세션에서 특정 데이터를 삭제합니다. 모든 세션 데이터를 삭제하려면 `flush` 메소드를 사용하세요:

    // 단일 키 삭제...
    $request->session()->forget('name');

    // 다중 키 삭제...
    $request->session()->forget(['name', 'status']);

    $request->session()->flush();

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성

세션 ID 재생성은 악의적인 사용자가 [세션 고정(Session Fixation)](https://owasp.org/www-community/attacks/Session_fixation) 공격을 악용하는 것을 방지하기 위해 자주 수행됩니다.

라라벨의 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits) 또는 [Laravel Fortify](/docs/{{version}}/fortify)를 사용할 경우, 인증 과정에서 라라벨이 세션 ID를 자동으로 재생성합니다. 그러나 수동으로 세션 ID를 재생성해야 한다면, `regenerate` 메소드를 사용할 수 있습니다:

    $request->session()->regenerate();

세션 ID를 재생성하고 동시에 모든 세션 데이터를 삭제하려면 `invalidate` 메소드를 사용하세요:

    $request->session()->invalidate();

<a name="session-blocking"></a>
## 세션 블로킹

> {note} 세션 블로킹을 활용하려면, 애플리케이션에서 [원자적 락](/docs/{{version}}/cache#atomic-locks)를 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 드라이버는 `memcached`, `dynamodb`, `redis`, `database`입니다. 또한 `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 Laravel은 동일한 세션을 사용하는 요청이 동시에 실행될 수 있도록 허용합니다. 예를 들어, JavaScript HTTP 라이브러리로 애플리케이션에 두 개의 HTTP 요청을 보낼 경우 모두 동시에 실행됩니다. 많은 애플리케이션에서는 이것이 문제가 되지 않지만, 서로 다른 엔드포인트에 동시 접근하여 세션에 데이터를 쓰는 특정 애플리케이션에서는 세션 데이터 손실이 발생할 수 있습니다.

이를 방지하기 위해 Laravel은 특정 세션에 대해 동시 요청을 제한할 수 있는 기능을 제공합니다. 시작하려면, 라우트 정의에 `block` 메소드를 체이닝하면 됩니다. 아래 예시에서, `/profile` 엔드포인트로 들어오는 요청은 세션 락을 획득합니다. 락이 유지되는 동안 동일 세션 ID를 공유하는 `/profile` 또는 `/order` 엔드포인트로 들어오는 모든 요청은 첫 번째 요청이 끝날 때까지 대기합니다:

    Route::post('/profile', function () {
        //
    })->block($lockSeconds = 10, $waitSeconds = 10)

    Route::post('/order', function () {
        //
    })->block($lockSeconds = 10, $waitSeconds = 10)

`block` 메소드는 두 개의 선택적 인자를 받습니다. 첫 번째 인자는 락이 해제되기 전까지 유지되는 최대 시간(초)입니다. 물론, 요청이 그보다 빨리 종료되면 락도 더 빨리 해제됩니다.

두 번째 인자는 세션 락을 얻기 위해 요청이 대기할 최대 시간(초)입니다. 해당 시간 동안 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다.

둘 다 생략하면 기본적으로 락 보유 최대 시간과 대기 시간이 10초입니다:

    Route::post('/profile', function () {
        //
    })->block()

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가

<a name="implementing-the-driver"></a>
#### 드라이버 구현

기존의 세션 드라이버가 애플리케이션의 니즈에 맞지 않는다면, Laravel은 커스텀 세션 핸들러를 작성할 수 있도록 지원합니다. 커스텀 세션 드라이버는 PHP의 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스에는 몇 가지 간단한 메소드만 포함되어 있습니다. 아래는 MongoDB의 스텁 구현 예시입니다:

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

> {tip} Laravel은 확장 기능을 저장하는 디렉터리를 기본적으로 제공하지 않습니다. 원하는 위치에 자유롭게 생성해 사용할 수 있습니다. 이 예시에서는 `Extensions` 디렉터리를 만들어 `MongoSessionHandler`를 저장했습니다.

이 메소드들의 역할이 바로 이해되지 않을 수 있으니, 각각이 무슨 일을 하는지 빠르게 정리해봅니다:

<div class="content-list" markdown="1">

- `open` 메소드는 일반적으로 파일 기반 세션 저장 시스템에서 사용됩니다. Laravel은 이미 `file` 세션 드라이버를 제공하므로, 보통 이 메소드에 구현이 필요하지 않습니다. 비워 두어도 됩니다.
- `close` 메소드는 `open`과 마찬가지로 대부분의 경우 무시할 수 있습니다. 대부분의 드라이버에서는 필요하지 않습니다.
- `read` 메소드는 주어진 `$sessionId`와 연관된 세션 데이터의 문자열 버전을 반환해야 합니다. 세션 데이터를 직렬화하거나 인코딩할 필요는 없습니다. Laravel이 자동으로 처리합니다.
- `write` 메소드는 주어진 `$sessionId`와 연관된 `$data` 문자열을 MongoDB와 같은 영속 저장소에 기록해야 합니다. 직렬화는 직접하지 않아도 됩니다. Laravel이 이미 처리합니다.
- `destroy` 메소드는 주어진 `$sessionId`와 연관된 데이터를 영구 저장소에서 제거해야 합니다.
- `gc` 메소드는 지정된 UNIX 타임스탬프 `$lifetime`보다 오래된 모든 세션 데이터를 삭제해야 합니다. Memcached 및 Redis처럼 자체 만료 기능이 있는 시스템에서는 이 메소드는 비워 둘 수 있습니다.

</div>

<a name="registering-the-driver"></a>
#### 드라이버 등록

드라이버를 모두 구현했다면, 이제 Laravel에 등록할 차례입니다. Laravel의 세션 백엔드에 드라이버를 추가하려면, `Session` [파사드](/docs/{{version}}/facades)에서 제공하는 `extend` 메소드를 사용할 수 있습니다. 이 메소드는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메소드 내에서 호출해야 합니다. 기존 `App\Providers\AppServiceProvider`에서 하거나, 별도의 프로바이더를 새로 작성할 수도 있습니다:

    <?php

    namespace App\Providers;

    use App\Extensions\MongoSessionHandler;
    use Illuminate\Support\Facades\Session;
    use Illuminate\Support\ServiceProvider;

    class SessionServiceProvider extends ServiceProvider
    {
        /**
         * 어떤 애플리케이션 서비스를 등록합니다.
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * 어떤 애플리케이션 서비스를 부트스트랩합니다.
         *
         * @return void
         */
        public function boot()
        {
            Session::extend('mongo', function ($app) {
                // SessionHandlerInterface 구현체를 반환합니다.
                return new MongoSessionHandler;
            });
        }
    }

세션 드라이버가 등록되면, `config/session.php` 설정 파일에서 `mongo` 드라이버를 사용할 수 있습니다.
