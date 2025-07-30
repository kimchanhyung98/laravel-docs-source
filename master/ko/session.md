# HTTP 세션 (HTTP Session)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 전제 조건](#driver-prerequisites)
- [세션과 상호작용하기](#interacting-with-the-session)
    - [데이터 가져오기](#retrieving-data)
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

HTTP 기반 애플리케이션은 상태가 없기 때문에, 세션은 여러 요청에 걸쳐 사용자의 정보를 저장하는 방법을 제공합니다. 이 사용자 정보는 일반적으로 지속 가능한 저장소(백엔드)에 저장되어 이후 요청에서 접근할 수 있습니다.

Laravel은 표현력이 풍부하고 통일된 API를 통해 접근할 수 있는 다양한 세션 백엔드를 기본 제공하며, [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스 등 인기 있는 백엔드를 지원합니다.

<a name="configuration"></a>
### 설정 (Configuration)

애플리케이션의 세션 설정 파일은 `config/session.php`에 위치합니다. 이 파일에서 사용할 수 있는 옵션들을 반드시 확인하세요. 기본적으로 Laravel은 `database` 세션 드라이버를 사용하도록 설정되어 있습니다.

세션 `driver` 설정 옵션은 요청별로 세션 데이터를 어디에 저장할지 정의합니다. Laravel은 다양한 드라이버를 제공합니다:

<div class="content-list" markdown="1">

- `file` - 세션 데이터를 `storage/framework/sessions` 디렉토리에 저장합니다.
- `cookie` - 세션 데이터를 안전하게 암호화된 쿠키에 저장합니다.
- `database` - 세션 데이터를 관계형 데이터베이스에 저장합니다.
- `memcached` / `redis` - 빠른 캐시 기반 저장소 중 하나에 세션을 저장합니다.
- `dynamodb` - AWS DynamoDB에 세션을 저장합니다.
- `array` - PHP 배열에 세션을 저장하며, 지속되지 않습니다.

</div>

> [!NOTE]
> `array` 드라이버는 주로 [테스트](/docs/master/testing) 중에 사용되며, 세션에 저장된 데이터가 영구적으로 유지되지 않도록 합니다.

<a name="driver-prerequisites"></a>
### 드라이버 전제 조건 (Driver Prerequisites)

<a name="database"></a>
#### 데이터베이스 (Database)

`database` 세션 드라이버를 사용할 때는 세션 데이터를 저장할 데이터베이스 테이블이 필요합니다. 보통 Laravel 기본 `0001_01_01_000000_create_users_table.php` [마이그레이션](/docs/master/migrations)에 포함되어 있지만, 만약 `sessions` 테이블이 없다면 다음 Artisan 명령어로 마이그레이션을 생성할 수 있습니다:

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하려면 PECL을 통해 PhpRedis PHP 확장 기능을 설치하거나 Composer로 `predis/predis` 패키지(~1.0 버전)를 설치해야 합니다. Redis 설정에 대해서는 Laravel의 [Redis 문서](/docs/master/redis#configuration)를 참고하세요.

> [!NOTE]
> `SESSION_CONNECTION` 환경 변수 또는 `session.php` 설정 파일 내 `connection` 옵션을 사용해 세션 저장에 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기 (Interacting With the Session)

<a name="retrieving-data"></a>
### 데이터 가져오기 (Retrieving Data)

Laravel에서 세션 데이터를 다루는 주요 방법은 전역 `session` 헬퍼 함수 또는 `Request` 인스턴스를 통한 방법이 있습니다. 먼저, 라우트 클로저나 컨트롤러 메서드에 타입힌트를 통해 주입받는 `Request` 인스턴스를 살펴보겠습니다. 컨트롤러 메서드의 의존성은 Laravel [서비스 컨테이너](/docs/master/container)를 통해 자동으로 주입됩니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자 프로필을 표시합니다.
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

세션에서 항목을 가져올 때, 두 번째 인수로 기본값을 전달할 수 있습니다. 지정한 키가 세션에 존재하지 않으면 이 기본값이 반환됩니다. 또한 기본값에 클로저를 전달하면, 해당 키가 없을 때 클로저가 실행되어 그 결과가 반환됩니다:

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 전역 세션 헬퍼 (The Global Session Helper)

전역 `session` PHP 함수를 사용해 세션에서 데이터를 가져오거나 저장할 수 있습니다. `session` 헬퍼에 문자열 하나를 전달하면 해당 세션 키의 값을 반환합니다. 배열 형태의 키-값 쌍을 전달하면 세션에 저장됩니다:

```php
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
> HTTP 요청 인스턴스를 통해 세션에 접근하는 것과 전역 `session` 헬퍼를 사용하는 것 사이에 실질적인 차이는 거의 없습니다. 두 방식 모두 테스트 시 `assertSessionHas` 메서드를 사용해 검증할 수 있습니다.

<a name="retrieving-all-session-data"></a>
#### 세션 데이터 전체 가져오기 (Retrieving All Session Data)

세션에 저장된 모든 데이터를 가져오려면 `all` 메서드를 사용할 수 있습니다:

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 세션 데이터 일부만 가져오기 (Retrieving a Portion of the Session Data)

`only`와 `except` 메서드를 사용하면 세션 데이터 중 일부만 가져올 수 있습니다:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목 존재 여부 확인하기 (Determining if an Item Exists in the Session)

세션에 특정 항목이 있는지 확인하려면 `has` 메서드를 사용합니다. 이 메서드는 해당 항목이 존재하고 `null`이 아닌 경우 `true`를 반환합니다:

```php
if ($request->session()->has('users')) {
    // ...
}
```

값이 `null`일지라도 항목이 세션에 있는지 확인하려면 `exists` 메서드를 사용하세요:

```php
if ($request->session()->exists('users')) {
    // ...
}
```

항목이 세션에 없는 경우를 확인하려면 `missing` 메서드를 사용합니다. 이 메서드는 항목이 없으면 `true`를 반환합니다:

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### 데이터 저장하기 (Storing Data)

세션에 데이터를 저장하려면 주로 요청 인스턴스의 `put` 메서드나 전역 `session` 헬퍼를 사용합니다:

```php
// 요청 인스턴스를 통해...
$request->session()->put('key', 'value');

// 전역 "session" 헬퍼를 통해...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 형태 세션 값에 추가하기 (Pushing to Array Session Values)

`push` 메서드는 세션 값이 배열일 때 새 값을 추가할 수 있습니다. 예를 들어, `user.teams` 키에 배열 형태의 팀 이름들이 저장되어 있다면, 다음과 같이 새 값을 추가할 수 있습니다:

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 항목 가져오기와 삭제를 동시에 하기 (Retrieving and Deleting an Item)

`pull` 메서드는 세션에서 항목을 가져오면서 동시에 삭제합니다:

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가 및 감소시키기 (Incrementing and Decrementing Session Values)

세션에 저장된 정수 값을 증가시키거나 감소시키려면 `increment` 및 `decrement` 메서드를 사용하세요:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### 플래시 데이터 (Flash Data)

때때로 다음 요청까지만 유지할 데이터를 세션에 저장하고 싶을 때가 있습니다. 이럴 때는 `flash` 메서드를 사용합니다. 이 방식으로 저장된 데이터는 즉시 사용 가능하며 다음 HTTP 요청 동안에도 유지됩니다. 이후 요청 후에는 자동으로 삭제됩니다. 플래시 데이터는 주로 일회성 상태 메시지에 유용합니다:

```php
$request->session()->flash('status', '작업이 성공적으로 완료되었습니다!');
```

여러 요청에 걸쳐 플래시 데이터를 유지하려면 `reflash` 메서드를 사용하세요. 특정 플래시 데이터만 계속 유지하려면 `keep` 메서드를 사용하면 됩니다:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

현재 요청에 한해서만 플래시 데이터를 유지하려면 `now` 메서드를 사용하세요:

```php
$request->session()->now('status', '작업이 성공적으로 완료되었습니다!');
```

<a name="deleting-data"></a>
### 데이터 삭제하기 (Deleting Data)

`forget` 메서드는 세션에서 특정 데이터를 제거합니다. 세션 내 모든 데이터를 삭제하려면 `flush` 메서드를 사용하세요:

```php
// 단일 키 삭제...
$request->session()->forget('name');

// 여러 키 삭제...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성하기 (Regenerating the Session ID)

세션 ID 재생성은 악의적인 사용자가 애플리케이션에 대한 [세션 고정(Session Fixation)](https://owasp.org/www-community/attacks/Session_fixation) 공격을 하는 것을 방지하기 위해 자주 수행됩니다.

Laravel은 Laravel [애플리케이션 스타터 키트](/docs/master/starter-kits)나 [Laravel Fortify](/docs/master/fortify)를 사용할 경우 인증 과정에서 자동으로 세션 ID를 재생성합니다. 수동으로 세션 ID를 재생성하려면 `regenerate` 메서드를 사용하세요:

```php
$request->session()->regenerate();
```

세션 ID를 재생성하고 동시에 세션 내 모든 데이터를 삭제하려면 `invalidate` 메서드를 사용하면 됩니다:

```php
$request->session()->invalidate();
```

<a name="session-blocking"></a>
## 세션 블로킹 (Session Blocking)

> [!WARNING]
> 세션 블로킹 기능을 사용하려면 애플리케이션이 [원자적 락(atomic locks)](/docs/master/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 이 조건을 충족하는 캐시 드라이버에는 `memcached`, `dynamodb`, `redis`, `mongodb` (공식 `mongodb/laravel-mongodb` 패키지 포함), `database`, `file`, `array`가 있습니다. 또한, `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 Laravel은 동일한 세션을 사용하는 요청들을 동시에 실행할 수 있도록 허용합니다. 예를 들어, JavaScript HTTP 라이브러리를 사용해 두 개의 HTTP 요청을 동시에 보내면, 두 요청은 병렬로 수행됩니다. 대부분의 애플리케이션에는 문제가 없지만, 일부 애플리케이션에서는 서로 다른 두 엔드포인트에 동시 요청을 보내며 세션 데이터를 동시에 수정할 때 데이터 손실이 발생할 수 있습니다.

이를 해결하기 위해 Laravel은 특정 세션에 대해 동시 요청 수를 제한하는 기능을 제공합니다. 시작하려면 라우트 정의에 단순히 `block` 메서드를 체인하세요. 예를 들어, `/profile` 엔드포인트로 오는 요청은 세션 락을 획득합니다. 이 락이 유지되는 동안 동일 세션 ID를 가진 `/profile` 또는 `/order` 엔드포인트로 오는 요청은 첫 번째 요청이 종료될 때까지 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

`block` 메서드는 두 개의 선택적 인자를 받습니다. 첫 번째 인자는 세션 락이 해제되기 전까지 유지할 최대 시간(초)입니다. 요청이 먼저 끝나면 락은 즉시 해제됩니다.

두 번째 인자는 세션 락을 얻으려고 대기할 최대 시간(초)입니다. 이 시간 내에 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

이 인자들이 전달되지 않으면, 락은 최대 10초간 유지되고 요청은 락 획득을 위해 최대 10초간 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가하기 (Adding Custom Session Drivers)

<a name="implementing-the-driver"></a>
### 드라이버 구현하기 (Implementing the Driver)

기본 제공되는 세션 드라이버가 애플리케이션 요구에 맞지 않는다면, 직접 세션 핸들러를 작성할 수 있습니다. 커스텀 세션 드라이버는 PHP 내장 `SessionHandlerInterface`를 구현해야 하며, 이 인터페이스는 몇 가지 메서드로 구성되어 있습니다. MongoDB용 기본 뼈대 구현 예시는 다음과 같습니다:

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

Laravel은 기본 확장 디렉터리를 제공하지 않으므로, 구현체는 원하시는 위치에 자유롭게 둘 수 있습니다. 위 예시는 `Extensions` 디렉터리에 `MongoSessionHandler`를 두었습니다.

각 메서드가 하는 역할은 다음과 같습니다:

<div class="content-list" markdown="1">

- `open` 메서드는 보통 파일 기반 세션 저장소 시스템에서 사용되며, Laravel 기본 드라이버인 `file`이 있어 이 메서드에 코드를 작성할 일은 거의 없습니다. 비워둬도 무방합니다.
- `close` 메서드도 `open`과 유사해 대부분의 드라이버에서는 구현할 필요가 없습니다.
- `read` 메서드는 주어진 `$sessionId`에 해당하는 세션 데이터를 문자열로 반환해야 합니다. 직렬화나 인코딩은 Laravel이 처리하므로 걱정할 필요 없습니다.
- `write` 메서드는 `$sessionId`와 연관된 `$data` 문자열 데이터를 MongoDB 혹은 선택한 영속 저장소에 기록합니다. 이때도 직렬화는 Laravel이 이미 처리했으므로 하지 않아야 합니다.
- `destroy` 메서드는 `$sessionId`에 해당하는 세션 데이터를 영속 저장소에서 삭제해야 합니다.
- `gc` 메서드는 `$lifetime`(UNIX 타임스탬프) 보다 오래된 세션 데이터를 삭제합니다. Memcached나 Redis처럼 자체 만료 기능이 있는 저장소는 이 메서드를 빈 상태로 둬도 됩니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록하기 (Registering the Driver)

드라이버를 구현한 뒤에는 Laravel에 등록할 준비가 된 것입니다. Laravel 세션 백엔드에 추가 드라이버를 등록하려면 `Session` [파사드](/docs/master/facades)가 제공하는 `extend` 메서드를 사용하세요. 이 메서드는 [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드에서 호출해야 합니다. 기존의 `App\Providers\AppServiceProvider`에서 하거나 별도의 프로바이더를 생성해도 됩니다:

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

드라이버를 등록한 후에는 `SESSION_DRIVER` 환경 변수나 `config/session.php` 설정 파일에서 `mongo` 드라이버를 지정해 사용할 수 있습니다.