# HTTP 세션 (HTTP Session)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 전제 조건](#driver-prerequisites)
- [세션과 상호작용하기](#interacting-with-the-session)
    - [데이터 가져오기](#retrieving-data)
    - [데이터 저장하기](#storing-data)
    - [플래시 데이터](#flash-data)
    - [데이터 삭제하기](#deleting-data)
    - [세션 ID 재생성](#regenerating-the-session-id)
- [세션 블로킹](#session-blocking)
- [커스텀 세션 드라이버 추가하기](#adding-custom-session-drivers)
    - [드라이버 구현하기](#implementing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)

<a name="introduction"></a>
## 소개 (Introduction)

HTTP 기반 애플리케이션은 상태가 없기 때문에, 세션은 여러 요청에 걸쳐 사용자에 대한 정보를 저장하는 방법을 제공합니다. 이런 사용자 정보는 일반적으로 지속적인 저장소/백엔드에 저장되어 이후 요청에서 접근할 수 있습니다.

Laravel은 표현력이 풍부하고 통일된 API로 접근할 수 있는 다양한 세션 백엔드를 기본으로 제공합니다. Memcached, Redis, 데이터베이스 같은 인기 있는 백엔드에 대한 지원을 포함하고 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

애플리케이션의 세션 설정 파일은 `config/session.php`에 저장되어 있습니다. 이 파일 내의 옵션을 꼭 검토하세요. 기본적으로 Laravel은 `file` 세션 드라이버를 사용하도록 설정되어 있으며, 이는 많은 애플리케이션에서 잘 작동합니다. 만약 애플리케이션이 여러 웹 서버에 로드 밸런싱된다면, 모든 서버에서 접근 가능한 중앙화된 저장소(예: Redis 또는 데이터베이스)를 선택하는 것이 좋습니다.

세션 `driver` 설정 옵션은 각 요청에 대해 세션 데이터가 어디에 저장될지 정의합니다. Laravel은 기본적으로 다음과 같은 훌륭한 드라이버들을 제공합니다:

<div class="content-list" markdown="1">

- `file` - 세션 데이터가 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션 데이터가 보안되고 암호화된 쿠키에 저장됩니다.
- `database` - 세션 데이터가 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션 데이터가 이들 고속 캐시 기반 저장소에 저장됩니다.
- `dynamodb` - 세션 데이터가 AWS DynamoDB에 저장됩니다.
- `array` - 세션 데이터가 PHP 배열에 저장되며, 지속되지 않습니다.

</div>

> [!NOTE]
> `array` 드라이버는 주로 [테스트](/docs/9.x/testing) 시 사용하며, 세션에 저장된 데이터를 지속하지 못하게 합니다.

<a name="driver-prerequisites"></a>
### 드라이버 전제 조건 (Driver Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 경우, 세션 레코드를 저장할 테이블을 생성해야 합니다. 아래는 테이블을 위한 `Schema` 선언 예시입니다:

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

`session:table` Artisan 명령어로 이 마이그레이션을 생성할 수 있습니다. 데이터베이스 마이그레이션에 관한 자세한 내용은 [마이그레이션 문서](/docs/9.x/migrations)를 참고하세요:

```shell
php artisan session:table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하려면, PECL을 통해 PhpRedis PHP 확장을 설치하거나 Composer로 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 설정에 대한 자세한 내용은 Laravel의 [Redis 문서](/docs/9.x/redis#configuration)를 참고하세요.

> [!NOTE]
> `session` 설정 파일 내 `connection` 옵션을 사용해 세션에 사용할 Redis 연결을 명시할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기 (Interacting With The Session)

<a name="retrieving-data"></a>
### 데이터 가져오기 (Retrieving Data)

Laravel에서는 세션 데이터를 다루는 주요 방법이 두 가지 있습니다: 글로벌 `session` 헬퍼와 `Request` 인스턴스를 통한 방법입니다. 먼저, 라우트 클로저나 컨트롤러 메서드에 타입힌트를 걸어 `Request` 인스턴스로 세션에 접근하는 예시입니다. 컨트롤러 메서드의 의존성은 Laravel [서비스 컨테이너](/docs/9.x/container)를 통해 자동으로 주입됩니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 특정 사용자의 프로필 보여주기
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

세션에서 값을 가져올 때, `get` 메서드의 두 번째 인수로 기본값을 전달할 수 있습니다. 이 기본값은 세션에 해당 키가 없을 경우 반환됩니다. 만약 기본값으로 클로저를 전달하면, 해당 키가 없을 때 클로저가 실행되어 그 결과가 반환됩니다:

```
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 글로벌 세션 헬퍼

글로벌 `session` PHP 함수를 사용해 세션에서 데이터를 가져오거나 저장할 수도 있습니다. `session` 헬퍼를 문자열 인수 하나로 호출하면 해당 세션 키의 값을 반환합니다. 배열 형태로 키와 값을 넘기면 세션에 값을 저장합니다:

```
Route::get('/home', function () {
    // 세션에서 데이터 가져오기...
    $value = session('key');

    // 기본값 지정하기...
    $value = session('key', 'default');

    // 세션에 데이터 저장하기...
    session(['key' => 'value']);
});
```

> [!NOTE]
> HTTP 요청 인스턴스를 이용하는 방법과 글로벌 `session` 헬퍼를 사용하는 방법 사이의 실질적인 차이는 거의 없습니다. 두 방법 모두 모든 테스트 케이스에서 사용할 수 있는 `assertSessionHas` 메서드를 통해 [테스트](/docs/9.x/testing) 가능합니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 가져오기

세션에 저장된 모든 데이터를 가져오고 싶다면 `all` 메서드를 사용할 수 있습니다:

```
$data = $request->session()->all();
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 아이템 존재 여부 확인하기

세션에 특정 항목이 있고 그 값이 `null`이 아니라면 `has` 메서드는 `true`를 반환합니다:

```
if ($request->session()->has('users')) {
    //
}
```

값이 `null`이어도 세션에 해당 키가 있는지만 확인하고 싶다면 `exists` 메서드를 사용하세요:

```
if ($request->session()->exists('users')) {
    //
}
```

세션에 항목이 없음을 확인하려면 `missing` 메서드를 사용할 수 있습니다. 해당 키가 없으면 `true`를 반환합니다:

```
if ($request->session()->missing('users')) {
    //
}
```

<a name="storing-data"></a>
### 데이터 저장하기 (Storing Data)

세션에 데이터를 저장할 때는 보통 요청 인스턴스의 `put` 메서드나 글로벌 `session` 헬퍼를 사용합니다:

```
// 요청 인스턴스로 저장하기...
$request->session()->put('key', 'value');

// 글로벌 세션 헬퍼로 저장하기...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열형 세션 값에 추가하기

`push` 메서드는 세션 값이 배열일 때 새 값을 배열 끝에 추가할 수 있습니다. 예를 들어 `user.teams` 키가 팀 이름 배열일 경우, 아래처럼 새 팀을 추가할 수 있습니다:

```
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 값 가져오기 및 삭제하기

`pull` 메서드는 세션에서 값을 가져오면서 동시에 삭제합니다:

```
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가 및 감소

세션에 정수 값을 저장하고 있을 때, `increment`와 `decrement` 메서드로 값을 증가 또는 감소시킬 수 있습니다:

```
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### 플래시 데이터 (Flash Data)

일시적으로 다음 요청에만 세션 데이터를 저장하고 싶을 때는 `flash` 메서드를 사용합니다. 이렇게 저장한 데이터는 즉시 사용 가능하고 다음 HTTP 요청까지 유지됩니다. 그 이후에는 자동으로 삭제됩니다. 플래시 데이터는 주로 짧은 상태 메시지에 유용합니다:

```
$request->session()->flash('status', 'Task was successful!');
```

플래시 데이터를 여러 요청 동안 유지하려면 `reflash` 메서드를 사용할 수 있고, 특정 플래시 데이터만 유지하려면 `keep` 메서드를 사용할 수 있습니다:

```
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

현재 요청에만 플래시 데이터를 유지하고 싶다면 `now` 메서드를 사용하세요:

```
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
### 데이터 삭제하기 (Deleting Data)

`forget` 메서드는 세션에서 특정 데이터를 삭제합니다. 모든 데이터를 삭제하려면 `flush` 메서드를 사용하세요:

```
// 단일 키 삭제...
$request->session()->forget('name');

// 여러 키 삭제...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성 (Regenerating The Session ID)

세션 ID를 재생성하는 작업은 [session fixation](https://owasp.org/www-community/attacks/Session_fixation) 공격을 방지하기 위해 자주 수행됩니다.

Laravel은 Laravel [스타터 키트](/docs/9.x/starter-kits)나 [Laravel Fortify](/docs/9.x/fortify)를 사용하는 경우 인증 과정에서 자동으로 세션 ID를 재생성합니다. 필요 시 직접 세션 ID를 재생성하려면 `regenerate` 메서드를 사용하세요:

```
$request->session()->regenerate();
```

세션 ID를 재생성하면서 동시에 세션 데이터를 모두 삭제하려면 `invalidate` 메서드를 사용합니다:

```
$request->session()->invalidate();
```

<a name="session-blocking"></a>
## 세션 블로킹 (Session Blocking)

> [!WARNING]
> 세션 블로킹을 사용하려면, 애플리케이션이 [원자적 잠금](/docs/9.x/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원 드라이버는 `memcached`, `dynamodb`, `redis`, `database`입니다. 또한 `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 Laravel은 동일 세션을 사용하는 요청이 동시에 실행되는 것을 허용합니다. 예를 들어, JavaScript HTTP 라이브러리로 두 개의 HTTP 요청을 애플리케이션에 동시에 보내면 두 요청이 병행 실행됩니다. 대부분 애플리케이션에서는 문제가 없지만, 서로 다른 애플리케이션 엔드포인트에 병행 요청으로 세션에 데이터를 쓰는 경우 세션 데이터 손실이 발생할 수 있습니다.

이를 방지하기 위해, Laravel은 특정 세션에 대한 동시 요청 수를 제한할 수 있는 기능을 제공합니다. 시작하려면 라우트 정의에 `block` 메서드를 체인하면 됩니다. 아래 예시에서 `/profile` 엔드포인트로 들어오는 요청은 세션 잠금을 획득합니다. 이 잠금이 유지되는 동안 동일 세션 ID를 공유하는 `/profile` 또는 `/order` 엔드포인트로 들어오는 요청은 첫 번째 요청이 끝날 때까지 기다렸다가 실행됩니다:

```
Route::post('/profile', function () {
    //
})->block($lockSeconds = 10, $waitSeconds = 10)

Route::post('/order', function () {
    //
})->block($lockSeconds = 10, $waitSeconds = 10)
```

`block` 메서드는 두 개의 선택적 인수를 받습니다. 첫 번째 인수는 세션 잠금이 유지될 최대 시간을 초 단위로 지정합니다. 물론 요청이 이 시간보다 빨리 종료되면 잠금은 그 시점에서 풀립니다.

두 번째 인수는 잠금 획득 시도 중 요청이 대기할 최대 시간을 초 단위로 지정합니다. 만약 이 시간 내에 잠금을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

두 인수가 모두 없으면 기본으로 잠금은 최대 10초 동안 유지되고, 잠금을 얻기 위한 요청은 최대 10초 동안 대기합니다:

```
Route::post('/profile', function () {
    //
})->block()
```

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가하기 (Adding Custom Session Drivers)

<a name="implementing-the-driver"></a>
#### 드라이버 구현하기 (Implementing The Driver)

기존의 세션 드라이버가 애플리케이션 요구를 충족하지 못한다면, Laravel에서는 직접 세션 핸들러를 작성할 수 있습니다. 커스텀 세션 드라이버는 PHP 내장 인터페이스인 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스에는 몇 가지 단순한 메서드만 포함되어 있습니다. MongoDB용 예시 구현은 다음과 같습니다:

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

> [!NOTE]
> Laravel은 확장 기능을 저장할 디렉터리를 따로 제공하지 않습니다. 원하는 위치에 자유롭게 만들 수 있습니다. 위 예시는 `Extensions` 디렉터리를 만들어 `MongoSessionHandler`를 둔 경우입니다.

이 메서드들의 목적이 쉽게 이해되지 않을 수 있으니 간략히 설명합니다:

<div class="content-list" markdown="1">

- `open` 메서드는 보통 파일 기반 세션 저장 시스템에서 사용됩니다. Laravel이 기본 `file` 세션 드라이버를 제공하므로 대부분의 경우 구현하지 않아도 됩니다.
- `close` 메서드도 `open`과 마찬가지로 대다수 드라이버에서는 필요 없습니다.
- `read` 메서드는 주어진 `$sessionId`에 연결된 세션 데이터를 문자열로 반환해야 합니다. 세션 데이터의 직렬화나 인코딩은 Laravel이 처리하므로 직접 하지 않아도 됩니다.
- `write` 메서드는 `$sessionId`와 연결된 `$data` 문자열을 MongoDB 등 원하는 지속 저장소에 기록해야 합니다. 직렬화는 Laravel이 처리하므로 별도로 수행하지 않습니다.
- `destroy` 메서드는 `$sessionId`와 연관된 데이터를 저장소에서 제거해야 합니다.
- `gc`(가비지 콜렉터) 메서드는 $lifetime(UNIX 타임스탬프)보다 오래된 세션 데이터를 모두 삭제해야 합니다. Memcached나 Redis같이 자체 만료 시스템이 있는 경우 이 메서드를 비워 둬도 무방합니다.

</div>

<a name="registering-the-driver"></a>
#### 드라이버 등록하기 (Registering The Driver)

드라이버 구현이 끝났으면, Laravel에 이를 등록할 준비가 된 것입니다. Laravel 세션 백엔드에 새로운 드라이버를 추가하려면 `Session` [파사드](/docs/9.x/facades)의 `extend` 메서드를 사용할 수 있습니다. 이 메서드는 [서비스 프로바이더](/docs/9.x/providers)의 `boot` 메서드 안에서 호출해야 합니다. 기존의 `App\Providers\AppServiceProvider`에서 하거나, 별도의 프로바이더를 생성해도 됩니다:

```
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
            // SessionHandlerInterface 구현체 반환
            return new MongoSessionHandler;
        });
    }
}
```

드라이버를 등록한 후에는 `config/session.php` 설정 파일에서 `mongo` 드라이버를 사용할 수 있습니다.