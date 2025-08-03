# HTTP 세션 (HTTP Session)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 전제조건](#driver-prerequisites)
- [세션과 상호작용하기](#interacting-with-the-session)
    - [데이터 조회하기](#retrieving-data)
    - [데이터 저장하기](#storing-data)
    - [플래시 데이터](#flash-data)
    - [데이터 삭제하기](#deleting-data)
    - [세션 ID 재생성하기](#regenerating-the-session-id)
- [세션 블로킹](#session-blocking)
- [커스텀 세션 드라이버 추가하기](#adding-custom-session-drivers)
    - [드라이버 구현하기](#implementing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)

<a name="introduction"></a>
## 소개 (Introduction)

HTTP 기반 애플리케이션은 상태가 없는(stateless)이기 때문에, 세션은 여러 요청에 걸쳐 사용자 정보를 저장하는 방법을 제공합니다. 이 사용자 정보는 일반적으로 이후 요청에서도 접근할 수 있는 지속 가능한 저장소나 백엔드에 저장됩니다.

Laravel은 표현력이 풍부하고 통일된 API를 통해 접근할 수 있는 다양한 세션 백엔드를 기본으로 제공합니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 그리고 데이터베이스와 같은 인기 있는 백엔드에 대한 지원이 포함되어 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

애플리케이션의 세션 설정 파일은 `config/session.php`에 저장되어 있습니다. 이 파일에 있는 사용 가능한 옵션을 반드시 확인하세요. 기본적으로 Laravel은 많은 애플리케이션에 적합한 `file` 세션 드라이버를 사용하도록 설정되어 있습니다. 애플리케이션이 여러 웹 서버에 걸쳐 로드 밸런싱될 경우, 모든 서버가 접근할 수 있는 중앙 저장소(Redis 또는 데이터베이스 등)를 사용하는 것이 좋습니다.

세션 `driver` 설정 옵션은 각 요청에 대해 세션 데이터를 어디에 저장할지 정의합니다. Laravel은 기본적으로 다음과 같은 훌륭한 드라이버들을 제공합니다:

<div class="content-list" markdown="1">

- `file` - 세션은 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션은 안전하게 암호화된 쿠키에 저장됩니다.
- `database` - 세션은 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션은 이러한 빠른 캐시 기반 스토어에 저장됩니다.
- `dynamodb` - 세션은 AWS DynamoDB에 저장됩니다.
- `array` - 세션은 PHP 배열에 저장되며 지속되지 않습니다.

</div>

> [!TIP]
> `array` 드라이버는 주로 [테스트](/docs/{{version}}/testing) 중에 사용되며, 세션에 저장된 데이터가 유지되지 않도록 합니다.

<a name="driver-prerequisites"></a>
### 드라이버 전제조건 (Driver Prerequisites)

<a name="database"></a>
#### 데이터베이스 (Database)

`database` 세션 드라이버를 사용하는 경우, 세션 레코드를 저장할 테이블을 만들어야 합니다. 아래는 테이블을 생성하는 예제 `Schema` 선언입니다:

```
Schema::create('sessions', function ($table) {
    $table->string('id')->primary();
    $table->foreignId('user_id')->nullable()->index();
    $table->string('ip_address', 45)->nullable();
    $table->text('user_agent')->nullable();
    $table->text('payload');
    $table->integer('last_activity')->index();
});
```

`session:table` Artisan 명령어를 사용해 이 마이그레이션을 생성할 수 있습니다. 데이터베이스 마이그레이션에 대해 더 알고 싶으면 전체 [마이그레이션 문서](/docs/{{version}}/migrations)를 참고하세요:

```
php artisan session:table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하기 전, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer로 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 설정에 관한 자세한 내용은 Laravel의 [Redis 문서](/docs/{{version}}/redis#configuration)를 참고하세요.

> [!TIP]
> `session` 설정 파일의 `connection` 옵션을 사용해 세션이 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기 (Interacting With The Session)

<a name="retrieving-data"></a>
### 데이터 조회하기 (Retrieving Data)

Laravel에서 세션 데이터를 다루는 주요 방법은 전역 `session` 헬퍼와 `Request` 인스턴스를 통한 방법 두 가지입니다. 먼저, 라우트 클로저나 컨트롤러 메서드에 타입 힌트로 주입되는 `Request` 인스턴스를 통해 세션에 접근하는 방법을 살펴보겠습니다. 컨트롤러 메서드 의존성은 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입된다는 점을 기억하세요:

```
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
```

세션에서 항목을 조회할 때, `get` 메서드의 두 번째 인수로 기본값을 전달할 수 있습니다. 지정된 키가 세션에 없으면 이 기본값이 반환됩니다. 기본값으로 클로저를 전달하고 요청한 키가 존재하지 않으면 그 클로저가 실행되어 결과가 반환됩니다:

```
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 전역 세션 헬퍼 (The Global Session Helper)

전역 `session` PHP 함수를 이용해 세션 데이터를 조회하거나 저장할 수도 있습니다. `session` 헬퍼에 단일 문자열 인수를 넘기면 해당 세션 키의 값을 반환합니다. 배열 형태로 키와 값을 전달하면 그 값들이 세션에 저장됩니다:

```
Route::get('/home', function () {
    // 세션에서 데이터 조회...
    $value = session('key');

    // 기본값 지정...
    $value = session('key', 'default');

    // 세션에 데이터 저장...
    session(['key' => 'value']);
});
```

> [!TIP]
> HTTP 요청 인스턴스를 통한 세션 사용과 전역 `session` 헬퍼 사용 간에는 실질적인 차이가 거의 없습니다. 두 방법 모두 테스트 케이스에서 사용할 수 있는 `assertSessionHas` 메서드를 통해 [테스트](/docs/{{version}}/testing)가 가능합니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 조회하기 (Retrieving All Session Data)

세션에 저장된 모든 데이터를 가져오려면 `all` 메서드를 사용하세요:

```
$data = $request->session()->all();
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목의 존재 여부 확인하기 (Determining If An Item Exists In The Session)

세션에 특정 항목이 있는지 확인하려면 `has` 메서드를 사용합니다. `has`는 해당 항목이 존재하고 `null`이 아닐 때 `true`를 반환합니다:

```
if ($request->session()->has('users')) {
    //
}
```

값이 `null`이어도 항목이 세션에 존재하는지 확인하려면 `exists` 메서드를 사용하세요:

```
if ($request->session()->exists('users')) {
    //
}
```

세션에 항목이 없거나 값이 `null`일 때 이를 확인하려면 `missing` 메서드를 사용하면 됩니다:

```
if ($request->session()->missing('users')) {
    //
}
```

<a name="storing-data"></a>
### 데이터 저장하기 (Storing Data)

세션에 데이터를 저장하려면 보통 요청 객체의 `put` 메서드나 전역 `session` 헬퍼를 사용합니다:

```
// 요청 인스턴스를 통한 저장...
$request->session()->put('key', 'value');

// 전역 "session" 헬퍼를 통한 저장...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 세션 값에 값 추가하기 (Pushing To Array Session Values)

`push` 메서드는 세션 값이 배열일 때 새 값을 추가하는 데 사용됩니다. 예를 들어, `user.teams` 키가 팀 이름 배열을 담고 있다면 다음과 같이 새 값을 추가할 수 있습니다:

```
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 항목 조회 및 삭제 (Retrieving & Deleting An Item)

`pull` 메서드는 세션에서 항목을 조회하고 동시에 삭제할 때 사용합니다:

```
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가 및 감소 (Incrementing & Decrementing Session Values)

세션 데이터에 정수가 있을 때 이를 증가시키거나 감소시키려면 `increment` 및 `decrement` 메서드를 사용하세요:

```
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### 플래시 데이터 (Flash Data)

가끔 다음 요청을 위해 세션에 임시로 데이터를 저장하고 싶을 때가 있습니다. 이때 `flash` 메서드를 사용하세요. 이렇게 저장된 데이터는 즉시 사용 가능하며 바로 다음 HTTP 요청에서도 접근할 수 있습니다. 그 후 자동으로 삭제됩니다. 플래시 데이터는 주로 짧은 생명 주기의 상태 메시지에 유용합니다:

```
$request->session()->flash('status', '작업이 성공적으로 완료되었습니다!');
```

플래시 데이터를 여러 요청 동안 유지해야 할 경우 `reflash` 메서드를 사용해 모든 플래시 데이터를 한 번 더 유지할 수 있습니다. 특정 플래시 데이터만 유지하려면 `keep` 메서드를 사용하세요:

```
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

현재 요청 동안만 플래시 데이터를 유지하려면 `now` 메서드를 사용하면 됩니다:

```
$request->session()->now('status', '작업이 성공적으로 완료되었습니다!');
```

<a name="deleting-data"></a>
### 데이터 삭제하기 (Deleting Data)

`forget` 메서드는 세션에서 특정 데이터를 삭제합니다. 세션의 모든 데이터를 삭제하려면 `flush` 메서드를 사용하세요:

```
// 단일 키 삭제...
$request->session()->forget('name');

// 여러 키 삭제...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성하기 (Regenerating The Session ID)

세션 ID 재생성은 일반적으로 악의적인 사용자가 애플리케이션에서 [세션 고정(Session Fixation)](https://owasp.org/www-community/attacks/Session_fixation) 공격을 하는 것을 방지하기 위해 수행됩니다.

Laravel은 Laravel [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits) 또는 [Laravel Fortify](/docs/{{version}}/fortify)를 사용하는 경우 인증 과정 중 세션 ID를 자동으로 재생성합니다. 수동으로 세션 ID를 재생성해야 할 때는 `regenerate` 메서드를 사용하세요:

```
$request->session()->regenerate();
```

한 번에 세션 ID를 재생성하고 세션 데이터를 모두 삭제하려면 `invalidate` 메서드를 사용하면 됩니다:

```
$request->session()->invalidate();
```

<a name="session-blocking"></a>
## 세션 블로킹 (Session Blocking)

> [!NOTE]
> 세션 블로킹을 사용하려면 애플리케이션이 [원자적 락(atomic locks)](/docs/{{version}}/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 캐시 드라이버는 `memcached`, `dynamodb`, `redis`, `database`입니다. 또한 `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 Laravel은 동일한 세션을 사용하는 요청을 동시 실행(concurrently)할 수 있도록 허용합니다. 예를 들어, JavaScript HTTP 라이브러리를 통해 애플리케이션에 두 개의 HTTP 요청을 보내면, 두 요청은 동시에 실행됩니다. 대부분의 애플리케이션에는 문제가 되지 않지만, 두 개의 다른 엔드포인트가 모두 세션에 데이터를 쓰는 동시 요청 시 데이터 손실이 발생할 수 있습니다.

이를 방지하기 위해 Laravel은 특정 세션에 대한 동시 요청을 제한하는 기능을 제공합니다. 시작하려면 라우트 정의에 `block` 메서드를 체인으로 호출하면 됩니다. 아래 예제에서는 `/profile` 엔드포인트에 오는 요청이 세션 락을 획득합니다. 락이 유지되는 동안 동일한 세션 ID를 가진 `/profile` 또는 `/order` 엔드포인트로의 다른 요청은 첫 요청이 종료될 때까지 대기합니다:

```
Route::post('/profile', function () {
    //
})->block($lockSeconds = 10, $waitSeconds = 10)

Route::post('/order', function () {
    //
})->block($lockSeconds = 10, $waitSeconds = 10)
```

`block` 메서드는 두 개의 선택적 인수를 받습니다. 첫 번째 인수는 세션 락이 유지되는 최대 시간(초)이며, 요청이 이 시간을 넘기면 락이 해제됩니다. 물론 요청이 이 시간 전에 끝나면 락도 일찍 해제됩니다.

두 번째 인수는 세션 락을 획득하려 시도하는 동안 요청이 대기할 최대 시간(초)입니다. 이 시간을 초과하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

인수를 전달하지 않으면, 락은 최대 10초 동안 유지되고 요청은 락 획득을 위해 최대 10초간 기다립니다:

```
Route::post('/profile', function () {
    //
})->block()
```

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가하기 (Adding Custom Session Drivers)

<a name="implementing-the-driver"></a>
#### 드라이버 구현하기 (Implementing The Driver)

기존 세션 드라이버가 애플리케이션 요구를 충족하지 못한다면, Laravel은 직접 세션 핸들러를 작성할 수 있게 합니다. 커스텀 세션 드라이버는 PHP 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스는 몇 가지 간단한 메서드로 구성되어 있습니다. 아래는 MongoDB용 뼈대 구현 예시입니다:

```
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
```

> [!TIP]
> Laravel은 확장 기능을 위한 전용 디렉터리를 제공하지 않습니다. 원하는 위치에 자유롭게 작성할 수 있습니다. 위 예시에서는 `Extensions` 디렉터리를 만들어 `MongoSessionHandler`를 둔 것입니다.

메서드 목적이 직관적이지 않으니 각 메서드 기능을 간단히 설명합니다:

<div class="content-list" markdown="1">

- `open` 메서드는 주로 파일 기반 세션 저장 시스템에서 사용됩니다. Laravel은 기본으로 `file` 세션 드라이버를 제공하므로 보통 여기에 코드를 작성할 필요가 없습니다. 빈 상태로 놔둬도 무방합니다.
- `close` 메서드도 `open`과 마찬가지로 대부분의 드라이버에선 필요 없습니다.
- `read` 메서드는 주어진 `$sessionId`에 연관된 세션 데이터를 문자열로 반환해야 합니다. 직렬화나 인코딩 작업은 Laravel이 자동으로 처리하므로 직접 할 필요가 없습니다.
- `write` 메서드는 주어진 `$sessionId`와 `$data` 문자열을 MongoDB 등 원하는 영속 저장소에 기록해야 합니다. 여기서도 직렬화는 하지 않아도 됩니다.
- `destroy` 메서드는 주어진 `$sessionId`와 연관된 데이터를 영속 저장소에서 삭제해야 합니다.
- `gc` 메서드는 지정된 `$lifetime`보다 오래된 모든 세션 데이터를 삭제해야 합니다. Memcached, Redis 같은 자체 만료 시스템에서는 빈 구현으로 놔둬도 됩니다.

</div>

<a name="registering-the-driver"></a>
#### 드라이버 등록하기 (Registering The Driver)

드라이버 구현이 완료되면 Laravel에 등록할 준비가 된 것입니다. Laravel 세션 백엔드에 드라이버를 추가하려면 `Session` [파사드](/docs/{{version}}/facades)가 제공하는 `extend` 메서드를 사용하세요. 이 메서드는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 호출해야 합니다. 기존 `App\Providers\AppServiceProvider`에서 호출하거나 별도의 프로바이더를 만들어도 됩니다:

```
<?php

namespace App\Providers;

use App\Extensions\MongoSessionHandler;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\ServiceProvider;

class SessionServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록합니다.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        Session::extend('mongo', function ($app) {
            // SessionHandlerInterface 구현체를 반환합니다...
            return new MongoSessionHandler;
        });
    }
}
```

드라이버가 등록되면 `config/session.php` 설정 파일에서 `mongo` 드라이버를 사용할 수 있습니다.