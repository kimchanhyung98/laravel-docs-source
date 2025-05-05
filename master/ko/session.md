# HTTP 세션

- [소개](#introduction)
    - [구성](#configuration)
    - [드라이버 필수 조건](#driver-prerequisites)
- [세션과 상호작용하기](#interacting-with-the-session)
    - [데이터 조회](#retrieving-data)
    - [데이터 저장](#storing-data)
    - [플래시 데이터](#flash-data)
    - [데이터 삭제](#deleting-data)
    - [세션 ID 재생성](#regenerating-the-session-id)
- [세션 블로킹](#session-blocking)
- [사용자 정의 세션 드라이버 추가](#adding-custom-session-drivers)
    - [드라이버 구현](#implementing-the-driver)
    - [드라이버 등록](#registering-the-driver)

<a name="introduction"></a>
## 소개

HTTP 기반 애플리케이션은 상태가 없으므로, 세션은 여러 요청에 걸쳐 사용자 정보를 저장할 수 있는 방법을 제공합니다. 이러한 사용자 정보는 일반적으로 후속 요청에서 접근할 수 있는 영속 저장소/백엔드에 저장됩니다.

Laravel은 다양한 세션 백엔드를 제공하며, 이는 명확하고 통일된 API를 통해 사용할 수 있습니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스 등 인기 있는 백엔드에 대한 지원이 내장되어 있습니다.

<a name="configuration"></a>
### 구성

애플리케이션의 세션 구성 파일은 `config/session.php`에 저장되어 있습니다. 이 파일에서 제공되는 옵션을 반드시 검토하세요. 기본적으로 Laravel은 `database` 세션 드라이버를 사용하도록 설정되어 있습니다.

세션 `driver` 구성 옵션은 각 요청에 대해 세션 데이터가 저장될 위치를 정의합니다. Laravel은 다양한 드라이버를 제공합니다:

<div class="content-list" markdown="1">

- `file` - 세션이 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션이 보안 및 암호화된 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 해당 빠른 캐시 기반 저장소에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며 영속되지 않습니다.

</div>

> [!NOTE]
> array 드라이버는 주로 [테스트](/docs/{{version}}/testing) 시에 사용되며, 세션에 저장된 데이터가 영구적으로 저장되지 않도록 방지합니다.

<a name="driver-prerequisites"></a>
### 드라이버 필수 조건

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 경우, 세션 데이터를 저장할 데이터베이스 테이블이 필요합니다. 보통 이는 Laravel 기본 제공 [데이터베이스 마이그레이션](/docs/{{version}}/migrations) `0001_01_01_000000_create_users_table.php`에 포함되어 있습니다. 하지만 어떤 이유로 `sessions` 테이블이 없다면, `make:session-table` Artisan 명령어로 마이그레이션을 생성할 수 있습니다:

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 설정에 대한 자세한 내용은 Laravel [Redis 문서](/docs/{{version}}/redis#configuration)를 참고하세요.

> [!NOTE]
> `SESSION_CONNECTION` 환경 변수 또는 `session.php` 구성 파일의 `connection` 옵션을 사용하여, 세션 저장에 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기

<a name="retrieving-data"></a>
### 데이터 조회

Laravel에서 세션 데이터를 다루는 주요 방법은 글로벌 `session` 헬퍼와 `Request` 인스턴스를 사용하는 두 가지입니다. 먼저, 라우트 클로저나 컨트롤러 메소드에서 타입 힌트된 `Request` 인스턴스를 통해 세션에 접근하는 방법을 살펴보겠습니다. 컨트롤러 메소드의 의존성은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입됩니다:

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

세션에서 항목을 조회할 때, `get` 메소드의 두 번째 인수에 기본값을 전달할 수 있습니다. 지정한 키가 세션에 없다면 이 기본값이 반환됩니다. 기본값으로 클로저를 전달하면, 해당 키가 존재하지 않을 때 클로저가 실행되고 그 결과가 반환됩니다:

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 글로벌 세션 헬퍼

세션 데이터를 조회 및 저장하려면 글로벌 `session` PHP 함수를 사용할 수도 있습니다. `session` 헬퍼에 문자열 하나를 전달하면, 해당 세션 키의 값을 반환합니다. 키-값 쌍의 배열을 전달하면, 해당 값들이 세션에 저장됩니다:

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
> HTTP 요청 인스턴스를 통한 세션 사용과 글로벌 `session` 헬퍼 사용 간의 실질적인 차이는 거의 없습니다. 두 방식 모두 모든 테스트 케이스에서 사용할 수 있는 `assertSessionHas` 메소드를 통해 [테스트](docs/{{version}}/testing)가 가능합니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 조회

세션의 모든 데이터를 조회하려면, `all` 메소드를 사용할 수 있습니다:

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 세션 데이터의 일부만 조회

`only` 와 `except` 메소드를 사용하여 세션 데이터의 일부만 조회할 수 있습니다:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목이 존재하는지 확인

세션에 항목이 존재하는지 확인하려면 `has` 메소드를 사용하세요. `has` 메소드는 항목이 존재하고 값이 `null`이 아닐 때 `true`를 반환합니다:

```php
if ($request->session()->has('users')) {
    // ...
}
```

항목이 존재하는지 확인하되, 값이 `null`여도 상관없다면 `exists` 메소드를 사용하세요:

```php
if ($request->session()->exists('users')) {
    // ...
}
```

항목이 세션에 존재하지 않는지 확인하려면 `missing` 메소드를 사용하세요. `missing` 메소드는 항목이 없으면 `true`를 반환합니다:

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### 데이터 저장

세션에 데이터를 저장하려면 보통 요청 인스턴스의 `put` 메소드나 글로벌 `session` 헬퍼를 사용합니다:

```php
// 요청 인스턴스로 저장...
$request->session()->put('key', 'value');

// 글로벌 "session" 헬퍼로 저장...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 세션 값에 추가

`push` 메소드를 사용하여 배열 형태의 세션 값에 새 값을 추가할 수 있습니다. 예를 들어, `user.teams` 키에 팀명 배열이 있을 경우, 아래와 같이 새 값을 추가할 수 있습니다:

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 항목을 조회 및 삭제

`pull` 메소드는 하나의 문장으로 세션에서 항목을 조회하고 삭제합니다:

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가 및 감소

세션 데이터가 정수형이고, 해당 값을 증가 또는 감소시키려면 `increment` 및 `decrement` 메소드를 사용할 수 있습니다:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### 플래시 데이터

가끔 요청 직후에만 세션에 항목을 저장하고 싶을 때가 있습니다. `flash` 메소드를 사용하면 다음 HTTP 요청까지 세션에 데이터를 저장할 수 있습니다. 해당 요청 후 플래시 데이터는 자동으로 삭제됩니다. 플래시 데이터는 주로 짧은 상태 메시지에 유용합니다:

```php
$request->session()->flash('status', '작업이 성공적으로 완료되었습니다!');
```

여러 요청에 걸쳐 플래시 데이터를 보존하려면 `reflash` 메소드를 사용할 수 있습니다. 특정 플래시 데이터만 유지하려면 `keep` 메소드를 사용하세요:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

플래시 데이터를 현재 요청에만 보존하려면 `now` 메소드를 사용할 수 있습니다:

```php
$request->session()->now('status', '작업이 성공적으로 완료되었습니다!');
```

<a name="deleting-data"></a>
### 데이터 삭제

`forget` 메소드는 특정 데이터를 세션에서 삭제합니다. 모든 세션 데이터를 삭제하려면 `flush` 메소드를 사용할 수 있습니다:

```php
// 단일 키 삭제...
$request->session()->forget('name');

// 여러 키 삭제...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성

세션 ID 재생성은 악의적인 사용자가 애플리케이션에서 [세션 고정 공격](https://owasp.org/www-community/attacks/Session_fixation)을 시도하는 것을 방지하기 위해 자주 수행됩니다.

Laravel의 [스타터 키트](/docs/{{version}}/starter-kits) 또는 [Laravel Fortify](/docs/{{version}}/fortify)를 사용하는 경우 인증 과정에서 자동으로 세션 ID가 재생성됩니다. 그러나 수동으로 세션 ID를 재생성해야 할 경우 `regenerate` 메소드를 사용할 수 있습니다:

```php
$request->session()->regenerate();
```

세션 ID를 재생성하고, 동시에 모든 세션 데이터를 삭제하려면 `invalidate` 메소드를 사용합니다:

```php
$request->session()->invalidate();
```

<a name="session-blocking"></a>
## 세션 블로킹

> [!WARNING]
> 세션 블로킹을 사용하려면, 애플리케이션에서 [원자적 락](/docs/{{version}}/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 캐시 드라이버는 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 `mongodb/laravel-mongodb` 패키지 포함), `database`, `file`, `array`입니다. 또한, `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로, Laravel은 동일한 세션을 사용하는 여러 요청이 동시에 실행되도록 허용합니다. 예를 들어, JavaScript HTTP 라이브러리를 사용해 애플리케이션에 두 개의 HTTP 요청을 보낼 경우 두 요청이 동시에 처리됩니다. 대부분의 애플리케이션에서는 문제가 없으나, 서로 다른 엔드포인트에 세션 데이터 쓰기 작업이 동시에 일어나면 세션 데이터 손실이 발생할 수 있습니다.

이를 완화하기 위해, Laravel은 특정 세션에 대해 동시 요청을 제한하는 기능을 제공합니다. 이를 시작하려면, 라우트 정의에 `block` 메소드를 체이닝해 사용하면 됩니다. 아래 예에서는 `/profile` 엔드포인트에 대한 요청이 세션 락을 획득하게 됩니다. 락이 유지되는 동안 같은 세션 ID를 공유하는 `/profile` 또는 `/order` 엔드포인트에 대한 추가 요청은 첫 번째 요청이 끝날 때까지 대기하게 됩니다:

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

`block` 메소드는 두 개의 선택적 인자를 받을 수 있습니다. 첫 번째 인자는 세션 락이 유지될 최대(초 단위) 시간을 지정하며, 요청이 더 빨리 완료되면 락도 더 일찍 해제됩니다.

두 번째 인자는 세션 락을 획득하기 위해 요청이 대기할(초 단위) 최대 시간입니다. 만약 주어진 시간 동안 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다.

이 인자들을 전달하지 않으면, 락은 최대 10초 동안 유지되고, 잠금을 획득하려고 최대 10초까지 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
## 사용자 정의 세션 드라이버 추가

<a name="implementing-the-driver"></a>
### 드라이버 구현

기존 세션 드라이버가 애플리케이션의 요구를 충족하지 않을 경우, Laravel은 자체 세션 핸들러를 직접 구현할 수 있도록 합니다. 사용자 정의 세션 드라이버는 PHP의 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스는 몇 가지 간단한 메소드만 포함합니다. 아래는 MongoDB 구현의 예시입니다:

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

Laravel은 확장 프로그램을 저장할 기본 디렉토리를 제공하지 않으므로, 여러분은 원하는 곳에 자유롭게 저장할 수 있습니다. 이 예시에서는 `Extensions` 디렉터리를 만들어 `MongoSessionHandler`를 저장하였습니다.

각 메소드의 용도가 직관적이지 않을 수 있으므로, 아래에 각 메소드의 역할을 간단히 설명합니다:

<div class="content-list" markdown="1">

- `open` 메소드는 파일 기반 세션 저장 시스템에서 주로 사용됩니다. Laravel은 이미 `file` 세션 드라이버를 제공하므로, 이 메소드는 보통 빈 상태로 놔두면 됩니다.
- `close` 메소드도 `open`과 마찬가지로 대부분의 드라이버에서는 무시할 수 있습니다.
- `read` 메소드는 주어진 `$sessionId`와 관련된 세션 데이터의 문자열 버전을 반환해야 합니다. 세션 데이터의 직렬화나 인코딩 처리는 할 필요가 없습니다. Laravel이 이를 자동으로 처리합니다.
- `write` 메소드는 주어진 `$sessionId`와 연결된 `$data` 문자열을 MongoDB 또는 원하는 영구 저장소에 저장해야 합니다. 마찬가지로, 직접 직렬화를 수행할 필요가 없습니다.
- `destroy` 메소드는 지정한 `$sessionId`의 데이터를 영구 저장소에서 제거해야 합니다.
- `gc` 메소드는 `$lifetime`(UNIX 타임스탬프)보다 오래된 모든 세션 데이터를 제거해야 합니다. Memcached, Redis처럼 자동 만료 시스템에서는 이 메소드를 비워두어도 됩니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록

드라이버 구현이 완료되었다면, Laravel에 등록할 준비가 된 것입니다. 세션 백엔드에 드라이버를 추가하려면 `Session` [파사드](/docs/{{version}}/facades)에서 제공하는 `extend` 메소드를 사용할 수 있습니다. 이 메소드는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메소드에서 호출해야 합니다. 기존의 `App\Providers\AppServiceProvider`에서 하거나, 별도의 프로바이더를 만들어 등록할 수 있습니다:

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
            // SessionHandlerInterface의 구현체를 반환합니다...
            return new MongoSessionHandler;
        });
    }
}
```

세션 드라이버가 등록되면, `SESSION_DRIVER` 환경 변수나 애플리케이션의 `config/session.php` 구성 파일에서 세션 드라이버를 `mongo`로 지정할 수 있습니다.