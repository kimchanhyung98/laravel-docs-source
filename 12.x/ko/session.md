# HTTP 세션 (HTTP Session)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 조건](#driver-prerequisites)
- [세션과 상호작용하기](#interacting-with-the-session)
    - [데이터 가져오기](#retrieving-data)
    - [데이터 저장하기](#storing-data)
    - [플래시 데이터(Flash Data)](#flash-data)
    - [데이터 삭제하기](#deleting-data)
    - [세션 ID 재생성하기](#regenerating-the-session-id)
- [세션 블로킹](#session-blocking)
- [커스텀 세션 드라이버 추가하기](#adding-custom-session-drivers)
    - [드라이버 구현하기](#implementing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)

<a name="introduction"></a>
## 소개 (Introduction)

HTTP 기반 애플리케이션은 상태를 가지지 않기 때문에, 세션은 여러 요청에 걸쳐 사용자에 대한 정보를 저장하는 방법을 제공합니다. 이 사용자 정보는 일반적으로 지속적으로 접근할 수 있는 저장소(백엔드)에 보관됩니다.

Laravel은 표현력 있고 통합된 API를 통해 접근하는 다양한 세션 백엔드들을 기본 제공하며, [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스와 같은 인기 있는 백엔드를 지원합니다.

<a name="configuration"></a>
### 설정 (Configuration)

애플리케이션의 세션 설정 파일은 `config/session.php`에 위치합니다. 이 파일에서 사용할 수 있는 설정 옵션들을 꼭 확인하세요. 기본적으로 Laravel은 `database` 세션 드라이버를 사용하도록 설정되어 있습니다.

세션 `driver` 설정 옵션은 각 요청에서 세션 데이터를 어디에 저장할지 정의합니다. Laravel은 여러 드라이버를 제공합니다:

<div class="content-list" markdown="1">

- `file` - 세션이 `storage/framework/sessions`에 파일로 저장됩니다.
- `cookie` - 세션이 안전하게 암호화된 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 빠른 캐시 기반 저장소에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며 영속성이 없습니다.

</div>

> [!NOTE]
> 배열 드라이버는 주로 [테스트](/docs/12.x/testing) 중에 사용되며, 세션에 저장된 데이터를 영속하지 않도록 합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 조건 (Driver Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 때는 세션 데이터를 저장하는 데이터베이스 테이블이 반드시 있어야 합니다. 일반적으로 Laravel의 기본 `0001_01_01_000000_create_users_table.php` [마이그레이션](/docs/12.x/migrations)에 포함되어 있지만, 만약 `sessions` 테이블이 없다면 `make:session-table` Artisan 명령어로 마이그레이션을 생성할 수 있습니다:

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis를 세션 저장소로 사용하려면 PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 설정에 대한 자세한 내용은 Laravel의 [Redis 문서](/docs/12.x/redis#configuration)를 참고하세요.

> [!NOTE]
> `SESSION_CONNECTION` 환경 변수나 `session.php` 설정 파일 내의 `connection` 옵션을 활용해 세션 저장에 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기 (Interacting With the Session)

<a name="retrieving-data"></a>
### 데이터 가져오기 (Retrieving Data)

Laravel에서 세션 데이터를 다루는 두 가지 주요 방법은 전역 `session` 헬퍼와 `Request` 인스턴스를 이용하는 것입니다. 먼저, 라우트 클로저나 컨트롤러 메서드에 타입히트할 수 있는 `Request` 인스턴스를 통해 세션에 접근하는 방법을 보겠습니다. 컨트롤러 메서드의 의존성들은 Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 주입됩니다.

```php
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
```

세션에서 항목을 가져올 때, `get` 메서드의 두 번째 인수로 기본값을 전달할 수도 있습니다. 세션에 키가 존재하지 않는 경우, 이 기본값이 반환됩니다. 만약 기본값으로 클로저를 전달하면, 키가 없을 때 해당 클로저가 실행되어 그 결과가 반환됩니다:

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 전역 세션 헬퍼 (The Global Session Helper)

글로벌 `session` PHP 함수를 이용해 세션에서 데이터를 조회하거나 저장할 수도 있습니다. `session` 헬퍼가 단일 문자열 인수로 호출되면 해당 세션 키의 값을 반환하며, 배열로 호출하면 그 배열의 키/값 쌍을 세션에 저장합니다:

```php
Route::get('/home', function () {
    // 세션에서 데이터 조회...
    $value = session('key');

    // 기본값 지정...
    $value = session('key', 'default');

    // 세션에 데이터 저장...
    session(['key' => 'value']);
});
```

> [!NOTE]
> HTTP 요청 인스턴스를 통해 세션을 다루는 것과 전역 `session` 헬퍼를 사용하는 것 사이에는 실질적인 차이가 거의 없습니다. 두 방식 모두 테스트 케이스에서 사용할 수 있는 `assertSessionHas` 메서드를 통해 [테스트 가능](/docs/12.x/testing) 합니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 가져오기 (Retrieving All Session Data)

세션 내 모든 데이터를 한 번에 가져오고 싶다면 `all` 메서드를 사용할 수 있습니다:

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 세션 데이터 일부만 가져오기 (Retrieving a Portion of the Session Data)

`only`와 `except` 메서드로 세션 데이터의 일부만 가져올 수도 있습니다:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목이 존재하는지 확인하기 (Determining if an Item Exists in the Session)

세션에 항목이 존재하는지 확인하려면 `has` 메서드를 사용하세요. 이 메서드는 해당 항목이 존재하고 값이 `null`이 아닐 때 `true`를 반환합니다:

```php
if ($request->session()->has('users')) {
    // ...
}
```

값이 `null`이라도 존재 여부를 확인하려면 `exists` 메서드를 사용하세요:

```php
if ($request->session()->exists('users')) {
    // ...
}
```

세션에 항목이 없음을 확인하려면 `missing` 메서드를 사용하세요. 항목이 없으면 `true`를 반환합니다:

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### 데이터 저장하기 (Storing Data)

세션에 데이터를 저장할 때는 요청 인스턴스의 `put` 메서드나 전역 `session` 헬퍼를 주로 사용합니다:

```php
// 요청 인스턴스로...
$request->session()->put('key', 'value');

// 전역 "session" 헬퍼로...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 세션 값에 값 추가하기 (Pushing to Array Session Values)

`push` 메서드는 세션 값이 배열일 때 새로운 값을 배열에 추가합니다. 예를 들어, `user.teams` 키에 팀 이름 배열이 들어있다면 다음과 같이 새로운 값을 추가할 수 있습니다:

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 값을 가져오면서 삭제하기 (Retrieving and Deleting an Item)

`pull` 메서드는 세션에서 값을 가져오면서 동시에 삭제할 때 사용합니다:

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증감하기 (Incrementing and Decrementing Session Values)

세션 데이터 중 정수 값을 증가시키거나 감소시킬 때는 `increment`와 `decrement` 메서드를 사용하세요:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### 플래시 데이터 (Flash Data)

가끔 다음 요청에만 유효한 임시 데이터를 세션에 저장하고 싶을 때가 있습니다. `flash` 메서드를 사용하면 이를 구현할 수 있습니다. 이 데이터는 즉시 사용 가능하며, 다음 HTTP 요청에서도 접근할 수 있지만 그 후에는 삭제됩니다. 주로 상태 메시지처럼 짧은 기간 동안 필요한 정보에 유용합니다:

```php
$request->session()->flash('status', 'Task was successful!');
```

여러 요청에 걸쳐 플래시 데이터를 유지하려면 `reflash` 메서드를 사용합니다. 특정 플래시 데이터만 유지하고 싶을 때는 `keep` 메서드를 사용하세요:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

현재 요청에서만 플래시 데이터를 유지하려면 `now` 메서드를 사용하세요:

```php
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
### 데이터 삭제하기 (Deleting Data)

`forget` 메서드는 세션에서 특정 데이터를 삭제합니다. 모든 데이터를 삭제하려면 `flush` 메서드를 사용할 수 있습니다:

```php
// 단일 키 삭제...
$request->session()->forget('name');

// 여러 키 삭제...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성하기 (Regenerating the Session ID)

세션 ID 재생성은 [세션 고정(Session Fixation)](https://owasp.org/www-community/attacks/Session_fixation) 공격을 방지하기 위해 자주 사용됩니다.

Laravel은 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)나 [Laravel Fortify](/docs/12.x/fortify)를 사용하는 경우 인증 시 자동으로 세션 ID를 재생성하지만, 수동으로 하고 싶다면 `regenerate` 메서드를 사용하세요:

```php
$request->session()->regenerate();
```

세션 ID를 재생성함과 동시에 세션 데이터를 모두 삭제하려면 `invalidate` 메서드를 사용하세요:

```php
$request->session()->invalidate();
```

<a name="session-blocking"></a>
## 세션 블로킹 (Session Blocking)

> [!WARNING]
> 세션 블로킹 기능을 사용하려면, 애플리케이션이 [원자 락(atomic locks)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 캐시 드라이버는 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 `mongodb/laravel-mongodb` 패키지 포함), `database`, `file`, `array`입니다. 또한 `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 Laravel은 동일 세션을 사용하는 요청들이 동시에 실행되는 것을 허용합니다. 예를 들어, JavaScript HTTP 라이브러리를 통해 동시에 두 개의 HTTP 요청이 애플리케이션에 보내지면, 두 요청은 동시에 실행됩니다. 대부분 애플리케이션에서는 문제가 없지만, 동시에 서로 다른 두 엔드포인트에 요청을 보내고 각기 세션에 데이터를 쓰는 경우 아주 드물게 세션 데이터가 손실될 수 있습니다.

이를 방지하기 위해 Laravel은 동일 세션에 대한 동시 요청을 제한하는 기능을 제공합니다. 시작하려면 간단히 라우트 정의에 `block` 메서드를 체인하면 됩니다. 예를 들어, `/profile` 엔드포인트에 들어오는 요청은 세션 락을 획득하며, 락이 유지되는 동안 동일한 세션을 가진 `/profile` 혹은 `/order` 엔드포인트로 들어오는 요청들은 첫 요청이 완료될 때까지 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

`block` 메서드는 두 개의 선택적 인수를 받습니다. 첫 번째는 세션 락을 최대 몇 초 동안 유지할지를 정하며, 요청이 이 시간 전에 완료되면 락은 즉시 해제됩니다.

두 번째 인수는 락을 획득하려 시도하는 동안 대기할 최대 시간을 초단위로 의미하며, 해당 시간 내 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

이 두 인수를 전달하지 않으면 락은 최대 10초 동안 유지되고, 요청은 락을 얻기 위해 최대 10초까지 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가하기 (Adding Custom Session Drivers)

<a name="implementing-the-driver"></a>
### 드라이버 구현하기 (Implementing the Driver)

기본 제공 드라이버가 애플리케이션 요구에 맞지 않는 경우, PHP의 내장 `SessionHandlerInterface`를 구현하여 직접 세션 핸들러를 작성할 수 있습니다. 이 인터페이스는 몇 가지 간단한 메서드로 구성되어 있습니다. MongoDB용 스텁 구현 예시는 다음과 같습니다:

```php
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

Laravel은 확장기능을 위한 기본 디렉터리를 제공하지 않으므로, 원하는 위치에 클래스를 배치할 수 있습니다. 이 예에서는 `Extensions` 디렉터리를 만들어 `MongoSessionHandler`를 두었습니다.

각 메서드의 목적을 요약하면 다음과 같습니다:

<div class="content-list" markdown="1">

- `open` 메서드는 보통 파일 기반 세션 저장 시스템에서 사용됩니다. Laravel은 자체 `file` 세션 드라이버를 포함하므로, 이 메서드에 코드를 작성할 필요는 거의 없습니다. 비워둬도 됩니다.
- `close` 메서드 역시 마찬가지로 대부분의 드라이버에서는 필요하지 않아서 비워둘 수 있습니다.
- `read` 메서드는 주어진 `$sessionId`와 연관된 세션 데이터를 문자열로 반환해야 합니다. 세션 데이터의 직렬화나 인코딩은 Laravel이 자동으로 처리해주므로 직접 하지 않아도 됩니다.
- `write` 메서드는 `$sessionId`에 대응하는 `$data` 문자열을 MongoDB 같은 지속적 저장소에 기록해야 합니다. 마찬가지로 직렬화는 Laravel이 처리하므로 하지 않습니다.
- `destroy` 메서드는 `$sessionId`에 해당하는 데이터를 저장소에서 삭제해야 합니다.
- `gc` 메서드는 `$lifetime`(리눅스 타임스탬프 기준)보다 오래된 세션 데이터를 모두 삭제해야 합니다. Memcached나 Redis처럼 자체 만료 시스템을 가진 드라이버라면 빈 메서드로 남겨둘 수 있습니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록하기 (Registering the Driver)

드라이버 구현이 완료되면 Laravel에 등록할 준비가 된 것입니다. 추가 세션 드라이버를 등록하려면 `Session` [파사드](/docs/12.x/facades)의 `extend` 메서드를 사용하면 됩니다. 일반적으로 이 작업은 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 수행합니다. 기존 `App\Providers\AppServiceProvider`에서 하거나 새 프로바이더를 만들어 사용해도 됩니다:

```php
<?php

namespace App\Providers;

use App\Extensions\MongoSessionHandler;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\ServiceProvider;

class SessionServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Session::extend('mongo', function (Application $app) {
            // SessionHandlerInterface 구현체를 반환합니다...
            return new MongoSessionHandler;
        });
    }
}
```

세션 드라이버가 등록된 후에는 `SESSION_DRIVER` 환경 변수나 `config/session.php` 설정 파일을 통해 `mongo` 드라이버를 애플리케이션 세션 드라이버로 지정할 수 있습니다.