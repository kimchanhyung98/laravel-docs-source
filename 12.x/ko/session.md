# HTTP 세션 (HTTP Session)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
- [세션과 상호작용하기](#interacting-with-the-session)
    - [데이터 조회](#retrieving-data)
    - [데이터 저장](#storing-data)
    - [플래시 데이터](#flash-data)
    - [데이터 삭제](#deleting-data)
    - [세션 ID 재발급](#regenerating-the-session-id)
- [세션 블로킹](#session-blocking)
- [커스텀 세션 드라이버 추가하기](#adding-custom-session-drivers)
    - [드라이버 구현](#implementing-the-driver)
    - [드라이버 등록](#registering-the-driver)

<a name="introduction"></a>
## 소개

HTTP 기반 애플리케이션은 상태 정보를 유지하지 않기 때문에, 세션은 여러 요청에 걸쳐 사용자와 관련된 정보를 저장하는 역할을 합니다. 이렇게 저장된 사용자 정보는 일반적으로 지속적으로 접근 가능한 저장소(백엔드)에 보관되며, 이후의 요청에서도 다시 불러올 수 있습니다.

라라벨은 다양한 세션 백엔드를 지원하며, 이를 일관되고 직관적인 API를 통해 사용할 수 있습니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스와 같은 인기 있는 백엔드도 기본으로 지원됩니다.

<a name="configuration"></a>
### 설정

애플리케이션의 세션 설정 파일은 `config/session.php`에 위치합니다. 이 파일에 포함된 다양한 옵션들을 꼭 살펴보시기 바랍니다. 기본적으로 라라벨은 `database` 세션 드라이버를 사용하도록 설정되어 있습니다.

세션의 `driver` 옵션은 각 요청에서 세션 데이터가 어디에 저장될지를 지정합니다. 라라벨은 여러 종류의 드라이버를 제공합니다:

<div class="content-list" markdown="1">

- `file` - 세션 데이터가 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 보안이 적용된 암호화된 쿠키에 세션이 저장됩니다.
- `database` - 세션 데이터가 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 빠른 캐시 기반 저장소에 세션 데이터가 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션 데이터가 PHP 배열에 저장되며, 영구적으로 유지되지 않습니다.

</div>

> [!NOTE]
> `array` 드라이버는 주로 [테스트](/docs/12.x/testing)를 위해 사용되며, 세션에 저장된 데이터는 영구적으로 기록되지 않습니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 경우, 세션 데이터를 담을 데이터베이스 테이블이 필요합니다. 이 테이블은 라라벨의 기본 `0001_01_01_000000_create_users_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 일반적으로 포함되어 있습니다. 만약 `sessions` 테이블이 없다면, `make:session-table` 아티즌 명령어로 이 마이그레이션을 생성할 수 있습니다:

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

라라벨에서 Redis 세션을 사용하려면, PECL을 통해 PhpRedis PHP 확장 프로그램을 설치하거나, Composer를 통해 `predis/predis` 패키지(~1.0)를 추가해야 합니다. Redis 설정에 대한 자세한 내용은 라라벨의 [Redis 문서](/docs/12.x/redis#configuration)를 참고하세요.

> [!NOTE]
> 세션 저장에 사용할 Redis 연결은 `SESSION_CONNECTION` 환경 변수나 `session.php` 설정 파일의 `connection` 옵션을 통해 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기

<a name="retrieving-data"></a>
### 데이터 조회

라라벨에서 세션 데이터를 다루는 주요 방법은 전역 `session` 헬퍼와 `Request` 인스턴스를 사용하는 것입니다. 먼저, `Request` 인스턴스를 통해 세션에 접근하는 방법을 살펴보겠습니다. 이 인스턴스는 라우트 클로저나 컨트롤러 메서드에서 타입 힌트로 받아올 수 있습니다. 컨트롤러 메서드의 의존성은 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 주입됩니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
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

세션에서 항목을 조회할 때, `get` 메서드의 두 번째 인수로 기본값을 전달할 수 있습니다. 지정한 키가 세션에 존재하지 않을 경우, 이 기본값이 반환됩니다. 기본값으로 클로저(익명 함수)를 전달했을 때, 해당 키가 세션에 없으면 클로저가 실행되고 그 결과가 반환됩니다:

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 전역 세션 헬퍼

전역 PHP 함수인 `session`을 사용해 세션 데이터에 접근하거나 저장할 수도 있습니다. `session` 헬퍼를 문자열 하나로 호출하면 해당 세션 키의 값을 반환합니다. 키-값 쌍의 배열을 넘기면, 해당 값들이 세션에 저장됩니다:

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
> HTTP 요청 인스턴스나 전역 `session` 헬퍼를 사용하는 것에 실질적인 차이는 거의 없습니다. 두 방법 모두 [테스트](/docs/12.x/testing)에서 `assertSessionHas` 메서드를 활용해 테스트할 수 있습니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 조회

세션에 저장된 모든 데이터를 조회하려면 `all` 메서드를 사용할 수 있습니다:

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 일부 세션 데이터만 조회

`only` 및 `except` 메서드를 사용해 세션 데이터의 일부분만 얻을 수 있습니다:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목이 존재하는지 확인

세션에 특정 항목이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. `has` 메서드는 해당 항목이 존재하고 값이 `null`이 아니면 `true`를 반환합니다:

```php
if ($request->session()->has('users')) {
    // ...
}
```

값이 `null`이더라도 항목 자체가 세션에 존재하는지 확인하려면 `exists` 메서드를 사용하세요:

```php
if ($request->session()->exists('users')) {
    // ...
}
```

세션에 항목이 없는 경우를 확인하려면 `missing` 메서드를 사용할 수 있습니다. 항목이 존재하지 않으면 `true`를 반환합니다:

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### 데이터 저장

세션에 데이터를 저장하려면 일반적으로 요청 인스턴스의 `put` 메서드나 전역 `session` 헬퍼를 사용합니다:

```php
// 요청 인스턴스를 통해 저장...
$request->session()->put('key', 'value');

// 전역 "session" 헬퍼를 통해 저장...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 형태의 세션 값에 추가

`push` 메서드는 세션 값이 배열일 때 새로운 값을 추가할 때 사용합니다. 예를 들어, `user.teams` 키에 팀 이름의 배열이 저장되어 있다면, 새로운 팀을 다음과 같이 추가할 수 있습니다:

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 항목 조회와 동시에 삭제

`pull` 메서드는 세션에서 항목을 조회하면서 동시에 삭제합니다:

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가/감소시키기

세션 데이터가 정수일 경우, 값을 증가시키거나 감소시키고 싶다면 `increment` 및 `decrement` 메서드를 사용할 수 있습니다:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### 플래시 데이터

때로는 세션에 데이터를 저장하되, 다음 요청까지만 유지하고 싶을 때가 있습니다. 이럴 때는 `flash` 메서드를 사용하면 됩니다. 이 방식으로 저장된 데이터는 즉시 사용할 수 있고, 바로 다음 HTTP 요청까지 유지됩니다. 그 이후에는 자동으로 삭제됩니다. 플래시 데이터는 대개 짧은 상태 메시지를 전달하는 용도로 주로 사용됩니다:

```php
$request->session()->flash('status', 'Task was successful!');
```

플래시 데이터를 여러 요청 동안 유지하고 싶다면 `reflash` 메서드를 사용하면 모든 플래시 데이터가 한 번 더 유지됩니다. 특정 플래시 데이터만 유지하고 싶다면 `keep` 메서드를 사용할 수 있습니다:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

플래시 데이터를 현재 요청에서만 즉시 사용하려면 `now` 메서드를 사용할 수 있습니다:

```php
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
### 데이터 삭제

`forget` 메서드는 세션에서 특정 데이터를 제거합니다. 세션의 모든 데이터를 삭제하려면 `flush` 메서드를 사용하면 됩니다:

```php
// 단일 키 제거...
$request->session()->forget('name');

// 여러 키 제거...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재발급

세션 ID 재생성(Regeneration)은 [세션 고정(Session fixation)](https://owasp.org/www-community/attacks/Session_fixation) 공격을 방지하기 위해 종종 사용됩니다.

라라벨의 [스타터 키트](/docs/12.x/starter-kits)나 [Laravel Fortify](/docs/12.x/fortify)를 사용할 경우 인증 시 세션 ID가 자동으로 재발급됩니다. 하지만 직접 세션 ID를 재생성할 필요가 있다면 `regenerate` 메서드를 사용할 수 있습니다:

```php
$request->session()->regenerate();
```

세션 ID를 재생성함과 동시에 세션의 모든 데이터를 한 번에 삭제하고 싶다면 `invalidate` 메서드를 사용할 수 있습니다:

```php
$request->session()->invalidate();
```

<a name="session-blocking"></a>
## 세션 블로킹

> [!WARNING]
> 세션 블로킹 기능을 사용하려면, 애플리케이션에서 [원자적 락](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 캐시 드라이버로는 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 `mongodb/laravel-mongodb` 패키지 포함), `database`, `file`, `array` 등이 있습니다. 또한 `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 라라벨은 같은 세션을 사용하는 요청들이 동시에 실행되도록 허용합니다. 예를 들어, JavaScript HTTP 라이브러리를 사용하여 두 개의 HTTP 요청을 동시에 보내면, 두 요청이 동시에 실행됩니다. 대부분의 애플리케이션에서는 문제가 없지만, 서로 다른 엔드포인트에 동시에 세션 데이터를 쓰는 일부 경우에는 세션 데이터가 유실될 수 있습니다.

이런 현상을 방지하기 위해, 라라벨은 세션 당 동시 요청을 제한할 수 있는 기능을 제공합니다. 시작하려면, 라우트 정의에 `block` 메서드를 체이닝하면 됩니다. 아래 예시처럼 `/profile` 엔드포인트로 들어오는 요청은 세션 락을 획득하며, 이 락이 유지되는 동안 동일한 세션 ID를 공유하는 `/profile`이나 `/order` 엔드포인트로의 다른 요청들은 먼저 들어온 요청이 끝날 때까지 대기하게 됩니다:

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

`block` 메서드는 두 개의 선택적 인수를 받을 수 있습니다. 첫 번째 인수는 세션 락을 최대 몇 초 동안 유지할지를 지정합니다. 물론, 요청이 그보다 더 빨리 끝나면 락도 즉시 해제됩니다.

두 번째 인수는 세션 락을 획득할 때 최대 몇 초까지 대기할지를 지정합니다. 만약 이 시간 동안 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

이 인수들을 생략하면, 기본값으로 락은 최대 10초 동안 유지되고, 락을 얻으려는 요청도 최대 10초 동안 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가하기

<a name="implementing-the-driver"></a>
### 드라이버 구현

기존 세션 드라이버가 애플리케이션 요구사항에 맞지 않는 경우, 라라벨에서는 직접 세션 핸들러를 작성할 수 있습니다. 커스텀 세션 드라이버는 PHP의 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스에는 간단한 메서드 몇 개만 포함되어 있습니다. 아래는 MongoDB를 간단히 구현한 예시입니다:

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

라라벨은 확장 기능을 위한 기본 디렉터리를 제공하지 않으므로, 원하는 위치에 파일을 생성해도 무방합니다. 위 예시에서는 `Extensions` 디렉터리에 `MongoSessionHandler` 클래스를 추가했습니다.

각 메서드의 용도가 직관적으로 드러나지 않으니, 아래에 각 메서드의 역할을 간략히 설명합니다:

<div class="content-list" markdown="1">

- `open` 메서드는 주로 파일 기반 세션 저장소 시스템에서 사용됩니다. 라라벨은 이미 `file` 세션 드라이버를 기본 제공하므로, 이 메서드는 대부분 비워 두어도 무방합니다.
- `close` 메서드도 `open`과 마찬가지로 대부분의 드라이버에서 별도 구현이 필요 없습니다.
- `read` 메서드는 주어진 `$sessionId`에 해당하는 세션 데이터를 문자열로 반환해야 합니다. 데이터의 직렬화나 인코딩은 라라벨이 자동으로 처리해주므로 따로 신경 쓰지 않아도 됩니다.
- `write` 메서드는 `$sessionId`에 연관된 `$data` 문자열을 MongoDB 등 원하는 저장소에 쓴 뒤, 반환해야 합니다. 여기서도 별도의 직렬화는 필요 없습니다. 라라벨이 알아서 수행합니다.
- `destroy` 메서드는 `$sessionId`에 해당하는 데이터를 저장소에서 삭제해야 합니다.
- `gc` 메서드는 주어진 `$lifetime`(UNIX 타임스탬프)보다 오래된 세션 데이터를 모두 삭제해야 합니다. Memcached, Redis 등 자체적으로 만료 기능이 있는 시스템의 경우, 이 메서드는 비워도 괜찮습니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록

드라이버를 구현했다면, 이제 라라벨에 등록할 차례입니다. 라라벨에 커스텀 세션 드라이버를 추가하려면, `Session` [파사드](/docs/12.x/facades)가 제공하는 `extend` 메서드를 사용할 수 있습니다. 이 메서드는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드 안에서 호출해야 합니다. 기존의 `App\Providers\AppServiceProvider`에서 호출해도 되고, 별도의 프로바이더를 새로 만들어도 무방합니다:

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
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Session::extend('mongo', function (Application $app) {
            // SessionHandlerInterface를 구현한 객체 반환
            return new MongoSessionHandler;
        });
    }
}
```

세션 드라이버를 등록했다면, `SESSION_DRIVER` 환경 변수나 애플리케이션의 `config/session.php` 설정 파일에서 `mongo` 드라이버를 사용할 수 있습니다.
