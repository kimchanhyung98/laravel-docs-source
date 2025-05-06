# HTTP 세션

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
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

HTTP 기반 애플리케이션은 상태를 가지지 않기 때문에, 세션은 여러 요청에 걸쳐 사용자 정보를 저장할 수 있는 방법을 제공합니다. 이러한 사용자 정보는 일반적으로 지속적인 저장소/백엔드에 저장되어 이후의 요청에서 접근할 수 있습니다.

라라벨은 다양한 세션 백엔드를 기본적으로 제공하며, 직관적이고 통합적인 API를 통해 접근할 수 있습니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스와 같은 인기 있는 백엔드도 기본 지원합니다.

<a name="configuration"></a>
### 설정

애플리케이션의 세션 설정 파일은 `config/session.php`에 위치합니다. 이 파일에서 제공되는 다양한 옵션을 꼭 검토해보세요. 라라벨은 기본적으로 `file` 세션 드라이버를 사용하도록 설정되어 있으며, 이는 많은 애플리케이션에서 잘 동작합니다. 애플리케이션이 여러 웹 서버로 로드밸런싱 되는 경우, 모든 서버에서 접근 가능한 Redis나 데이터베이스 같은 중앙화된 저장소를 선택하는 것이 좋습니다.

세션의 `driver` 설정 옵션은 각 요청에서 세션 데이터가 어디에 저장될지를 정의합니다. 라라벨은 다음과 같은 훌륭한 드라이버를 기본 제공하며 즉시 사용할 수 있습니다:

<div class="content-list" markdown="1">

- `file` - 세션이 `storage/framework/sessions`에 저장됨
- `cookie` - 세션이 보안, 암호화된 쿠키에 저장됨
- `database` - 세션이 관계형 데이터베이스에 저장됨
- `memcached` / `redis` - 세션이 빠른 캐시 기반 저장소에 저장됨
- `dynamodb` - 세션이 AWS DynamoDB에 저장됨
- `array` - 세션이 PHP 배열에 저장되어, 지속되지 않음

</div>

> [!NOTE]  
> array 드라이버는 주로 [테스트](/docs/{{version}}/testing) 용도로 사용되며, 세션에 저장된 데이터가 영구적으로 저장되지 않도록 합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 때는 세션 레코드를 저장할 테이블을 생성해야 합니다. 아래는 예시 `Schema` 선언입니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::create('sessions', function (Blueprint $table) {
        $table->string('id')->primary();
        $table->foreignId('user_id')->nullable()->index();
        $table->string('ip_address', 45)->nullable();
        $table->text('user_agent')->nullable();
        $table->text('payload');
        $table->integer('last_activity')->index();
    });

이 마이그레이션을 생성하려면 `session:table` Artisan 명령어를 사용할 수 있습니다. 데이터베이스 마이그레이션에 대해 더 자세히 알아보려면 [마이그레이션 문서](/docs/{{version}}/migrations)를 참고하십시오:

```shell
php artisan session:table

php artisan migrate
```

<a name="redis"></a>
#### Redis

라라벨에서 Redis 세션을 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나, Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 구성에 대한 자세한 내용은 라라벨 [Redis 문서](/docs/{{version}}/redis#configuration)를 참조하세요.

> [!NOTE]  
> `session` 설정 파일에서, `connection` 옵션을 사용하여 세션에서 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기

<a name="retrieving-data"></a>
### 데이터 조회

라라벨에서 세션 데이터를 다루는 기본적인 방법은 두 가지가 있습니다: 글로벌 `session` 헬퍼와 `Request` 인스턴스를 사용하는 방법입니다. 먼저, 라우트 클로저나 컨트롤러 메서드에 타입힌트로 전달된 `Request` 인스턴스를 통해 세션에 접근하는 예시를 살펴보겠습니다. 참고로, 컨트롤러 메서드의 의존성은 라라벨 [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동 주입됩니다:

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use Illuminate\View\View;

    class UserController extends Controller
    {
        /**
         * 주어진 사용자의 프로필을 보여줍니다.
         */
        public function show(Request $request, string $id): View
        {
            $value = $request->session()->get('key');

            // ...

            $user = $this->users->find($id);

            return view('user.profile', ['user' => $user]);
        }
    }

세션에서 항목을 조회할 때, `get` 메서드의 두 번째 인자로 기본값을 지정할 수 있습니다. 지정한 키가 세션에 없으면 이 기본값이 반환됩니다. 기본값으로 클로저를 전달하면, 해당 키가 존재하지 않을 때 클로저가 실행되어 반환값을 돌려줍니다:

    $value = $request->session()->get('key', 'default');

    $value = $request->session()->get('key', function () {
        return 'default';
    });

<a name="the-global-session-helper"></a>
#### 글로벌 Session 헬퍼

세션의 데이터를 조회하고 저장할 때, 전역 `session` PHP 함수를 사용할 수도 있습니다. 이 헬퍼에 단일 문자열 인자를 전달하면 해당 세션 키의 값이 반환됩니다. 배열을 전달하면, 해당 key/value 쌍이 세션에 저장됩니다:

    Route::get('/home', function () {
        // 세션에서 데이터 조회...
        $value = session('key');

        // 기본값 지정...
        $value = session('key', 'default');

        // 세션에 데이터 저장...
        session(['key' => 'value']);
    });

> [!NOTE]  
> HTTP 요청 인스턴스를 통한 세션 사용과 글로벌 `session` 헬퍼 사용 간에는 실질적인 차이가 거의 없습니다. 두 방법 모두 모든 테스트 케이스에서 제공되는 `assertSessionHas` 메서드를 통해 [테스트](/docs/{{version}}/testing)할 수 있습니다.

<a name="retrieving-all-session-data"></a>
#### 세션의 모든 데이터 조회

세션에 저장된 모든 데이터를 조회하려면 `all` 메서드를 사용할 수 있습니다:

    $data = $request->session()->all();

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 세션 데이터의 일부분만 조회

세션 데이터의 일부만 조회하려면 `only`와 `except` 메서드를 사용할 수 있습니다:

    $data = $request->session()->only(['username', 'email']);

    $data = $request->session()->except(['username', 'email']);

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목 존재 여부 확인

세션에 항목이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. `has`는 항목이 존재하고 null이 아니면 `true`를 반환합니다:

    if ($request->session()->has('users')) {
        // ...
    }

값이 null이어도 세션에 항목이 존재하는지 확인하려면 `exists` 메서드를 사용하세요:

    if ($request->session()->exists('users')) {
        // ...
    }

세션에 항목이 없는지 확인하려면 `missing` 메서드를 사용하세요. 이 메서드는 항목이 없으면 `true`를 반환합니다:

    if ($request->session()->missing('users')) {
        // ...
    }

<a name="storing-data"></a>
### 데이터 저장

세션에 데이터를 저장하려면, 보통 요청 인스턴스의 `put` 메서드나 전역 `session` 헬퍼를 사용합니다:

    // 요청 인스턴스를 통해...
    $request->session()->put('key', 'value');

    // 글로벌 "session" 헬퍼를 통해...
    session(['key' => 'value']);

<a name="pushing-to-array-session-values"></a>
#### 배열 형태의 세션 값에 추가

세션 값이 배열인 경우, `push` 메서드를 사용해 새로운 값을 배열에 추가할 수 있습니다. 예를 들어, `user.teams` 키에 팀 이름 배열이 있을 때 다음처럼 값을 추가할 수 있습니다:

    $request->session()->push('user.teams', 'developers');

<a name="retrieving-deleting-an-item"></a>
#### 항목 조회 및 삭제

`pull` 메서드는 세션에서 항목을 조회한 뒤 삭제까지 한 번에 수행합니다:

    $value = $request->session()->pull('key', 'default');

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가 및 감소

세션 데이터가 정수이고, 이를 증가시키거나 감소시키고 싶다면 `increment`와 `decrement` 메서드를 사용할 수 있습니다:

    $request->session()->increment('count');

    $request->session()->increment('count', $incrementBy = 2);

    $request->session()->decrement('count');

    $request->session()->decrement('count', $decrementBy = 2);

<a name="flash-data"></a>
### Flash 데이터

가끔 다음 요청에서만 사용할 데이터를 세션에 저장하고 싶을 때가 있습니다. 이럴 때 `flash` 메서드를 사용할 수 있습니다. 이 방식으로 저장된 데이터는 즉시와 다음 HTTP 요청 시점에 사용할 수 있으며, 그 이후에는 삭제됩니다. Flash 데이터는 주로 일시적인 상태 메시지 등에 유용합니다:

    $request->session()->flash('status', '작업이 성공적으로 처리되었습니다!');

Flash 데이터를 여러 요청에 걸쳐 유지하고 싶다면 `reflash` 메서드를 사용하세요. 특정 데이터만 유지하고 싶다면 `keep` 메서드를 사용하면 됩니다:

    $request->session()->reflash();

    $request->session()->keep(['username', 'email']);

Flash 데이터를 현재 요청에서만 유지하고 싶다면 `now` 메서드를 사용할 수 있습니다:

    $request->session()->now('status', '작업이 성공적으로 처리되었습니다!');

<a name="deleting-data"></a>
### 데이터 삭제

`forget` 메서드는 세션에서 특정 데이터를 삭제합니다. 모든 세션 데이터를 삭제하려면 `flush` 메서드를 사용하세요:

    // 단일 키 삭제...
    $request->session()->forget('name');

    // 여러 키 삭제...
    $request->session()->forget(['name', 'status']);

    $request->session()->flush();

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성

세션 ID 재생성은 [세션 고정 공격(session fixation)](https://owasp.org/www-community/attacks/Session_fixation) 위험을 막기 위해 자주 사용됩니다.

라라벨의 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)이나 [Laravel Fortify](/docs/{{version}}/fortify)를 사용할 경우, 인증 시 자동으로 세션 ID가 재생성됩니다. 그러나 직접 세션 ID를 재생성해야 한다면 `regenerate` 메서드를 사용하세요:

    $request->session()->regenerate();

세션 ID 재생성과 동시에 모든 세션 데이터를 삭제하려면 `invalidate` 메서드를 사용할 수 있습니다:

    $request->session()->invalidate();

<a name="session-blocking"></a>
## 세션 블로킹

> [!WARNING]  
> 세션 블로킹을 사용하려면, 애플리케이션에서 [원자적 락(atomic locks)](/docs/{{version}}/cache#atomic-locks)를 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 드라이버로는 `memcached`, `dynamodb`, `redis`, `database`, `file`, `array`가 있습니다. 또한, `cookie` 세션 드라이버에서는 사용할 수 없습니다.

라라벨은 기본적으로 동일한 세션을 사용하는 요청이 동시에 실행될 수 있도록 허용합니다. 예를 들어, JavaScript HTTP 라이브러리로 두 개의 HTTP 요청을 동시에 보낼 경우, 두 요청이 동시에 실행됩니다. 대부분의 애플리케이션에서는 문제가 없지만, 서로 다른 엔드포인트에서 동시에 세션에 데이터를 기록하는 일부 애플리케이션에서는 세션 데이터가 손실될 수 있습니다.

이 문제를 완화하기 위해, 라라벨은 주어진 세션에 대한 동시 요청을 제한할 수 있는 기능을 제공합니다. 시작하려면, 라우트 정의에 `block` 메서드를 체이닝하면 됩니다. 예를 들면, `/profile` 엔드포인트로 들어오는 요청은 세션 락을 획득합니다. 이 락이 유지되는 동안 동일한 세션 ID를 공유하는 `/profile` 또는 `/order` 엔드포인트로의 다른 요청은 첫 번째 요청이 끝날 때까지 대기하게 됩니다:

    Route::post('/profile', function () {
        // ...
    })->block($lockSeconds = 10, $waitSeconds = 10)

    Route::post('/order', function () {
        // ...
    })->block($lockSeconds = 10, $waitSeconds = 10)

`block` 메서드는 두 개의 선택적 인자를 받습니다. 첫 번째 인자는 세션 락을 해제하기 전까지 락을 유지할 최대 초(seconds)입니다. 물론 요청이 더 일찍 종료되면 락도 더 빨리 해제됩니다.

두 번째 인자는 세션 락을 획득할 때까지 요청이 대기해야 할 초(seconds)입니다. 만약 이 시간 내에 세션 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

둘 다 인자를 전달하지 않으면, 락은 최대 10초 동안 획득되고, 요청은 최대 10초 동안 락을 기다립니다:

    Route::post('/profile', function () {
        // ...
    })->block()

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가

<a name="implementing-the-driver"></a>
### 드라이버 구현

기존 세션 드라이버 중에 애플리케이션에 적합한 것이 없다면, 라라벨은 직접 세션 핸들러를 작성할 수 있게 해줍니다. 커스텀 세션 드라이버는 PHP의 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스에는 소수의 간단한 메서드만 있습니다. 다음은 MongoDB 드라이버의 예시 골격입니다:

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

> [!NOTE]  
> 라라벨은 확장 기능을 위한 디렉토리를 기본 제공하지 않으므로, 원하는 위치에 자유롭게 둘 수 있습니다. 예제에서는 확장 기능을 보관할 `Extensions` 디렉토리를 생성했습니다.

이 메서드들의 목적이 명확하지 않을 수 있으므로, 각 메서드가 하는 일에 대해 간략히 설명하겠습니다:

<div class="content-list" markdown="1">

- `open` 메서드는 파일 기반 세션 저장 시스템에서 주로 사용됩니다. 라라벨의 `file` 드라이버는 이미 기본 제공되므로, 대개 이 메서드를 구현할 필요가 없습니다. 비워두셔도 됩니다.
- `close` 메서드 역시 대부분의 드라이버에서 무시할 수 있습니다.
- `read` 메서드는 주어진 `$sessionId`에 해당하는 세션 데이터를 문자열 형태로 반환해야 합니다. 세션 데이터의 직렬화나 인코딩 처리는 필요 없습니다. 라라벨이 알아서 처리해 줍니다.
- `write` 메서드는 주어진 `$sessionId`와 연결된 `$data` 문자열을 MongoDB 등 영구 저장소에 저장해야 합니다. 이 때 역시 직접 직렬화할 필요는 없습니다.
- `destroy` 메서드는 `$sessionId`와 연결된 데이터를 저장소에서 삭제해야 합니다.
- `gc` 메서드는 주어진 `$lifetime`(유닉스 타임스탬프)보다 오래된 모든 세션 데이터를 삭제해야 합니다. Memcached나 Redis처럼 자동 만료되는 시스템에서는 공란으로 둘 수 있습니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록

드라이버를 구현했다면, 이제 라라벨에 등록할 차례입니다. 라라벨의 세션 백엔드에 드라이버를 추가하려면, `Session` [파사드](/docs/{{version}}/facades)에서 제공하는 `extend` 메서드를 사용해야 합니다. [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 `extend`를 호출하면 됩니다. 기존의 `App\Providers\AppServiceProvider`를 수정하거나, 새로운 프로바이더를 만들어도 됩니다:

    <?php

    namespace App\Providers;

    use App\Extensions\MongoSessionHandler;
    use Illuminate\Contracts\Foundation\Application;
    use Illuminate\Support\Facades\Session;
    use Illuminate\Support\ServiceProvider;

    class SessionServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스 등록
         */
        public function register(): void
        {
            // ...
        }

        /**
         * 애플리케이션 서비스 부트스트랩
         */
        public function boot(): void
        {
            Session::extend('mongo', function (Application $app) {
                // SessionHandlerInterface 구현체 반환...
                return new MongoSessionHandler;
            });
        }
    }

세션 드라이버를 등록했다면, `config/session.php` 설정 파일에서 `mongo` 드라이버를 사용할 수 있습니다.