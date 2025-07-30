# HTTP 세션 (HTTP Session)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사용 조건](#driver-prerequisites)
- [세션 다루기](#interacting-with-the-session)
    - [데이터 조회하기](#retrieving-data)
    - [데이터 저장하기](#storing-data)
    - [플래시 데이터](#flash-data)
    - [데이터 삭제하기](#deleting-data)
    - [세션 ID 재생성](#regenerating-the-session-id)
- [세션 블로킹](#session-blocking)
- [사용자 정의 세션 드라이버 추가](#adding-custom-session-drivers)
    - [드라이버 구현](#implementing-the-driver)
    - [드라이버 등록](#registering-the-driver)

<a name="introduction"></a>
## 소개

HTTP 기반 애플리케이션은 상태를 가지지 않기 때문에, 세션은 여러 요청에 걸쳐 사용자 정보를 저장할 수 있는 방법을 제공합니다. 이러한 사용자 정보는 일반적으로 이후의 요청에서 접근 가능한 영속적인 저장소(백엔드)에 저장됩니다.

라라벨은 표현력이 뛰어나고 일관된 API로 액세스할 수 있는 다양한 세션 백엔드를 기본으로 제공합니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스 등 다양한 인기 백엔드가 지원됩니다.

<a name="configuration"></a>
### 설정

애플리케이션의 세션 설정 파일은 `config/session.php`에 있습니다. 이 파일에서 사용 가능한 옵션들을 꼭 확인하시기 바랍니다. 기본적으로 라라벨은 `database` 세션 드라이버를 사용하도록 설정되어 있습니다.

세션의 `driver` 설정 옵션은 각 요청에 대해 세션 데이터가 어디에 저장될지 정의합니다. 라라벨은 아래와 같은 다양한 드라이버를 제공합니다.

<div class="content-list" markdown="1">

- `file` - 세션이 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션이 보안이 유지된 암호화된 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 이와 같은 빠른 캐시 기반 저장소에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며, 영구적으로 저장되지 않습니다.

</div>

> [!NOTE]
> `array` 드라이버는 주로 [테스트](/docs/12.x/testing) 시 사용되며, 세션에 저장된 데이터는 영구적으로 저장되지 않습니다.

<a name="driver-prerequisites"></a>
### 드라이버 사용 조건

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 때는 세션 데이터를 저장할 DB 테이블이 필요합니다. 일반적으로 라라벨의 기본 `0001_01_01_000000_create_users_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있지만, 만약 어떤 이유로 `sessions` 테이블이 없다면 `make:session-table` 아티즌 명령어로 마이그레이션 파일을 생성할 수 있습니다.

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

라라벨에서 Redis 세션을 사용하기 전에 PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나, Composer를 이용해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 환경설정에 대한 자세한 내용은 라라벨의 [Redis 문서](/docs/12.x/redis#configuration)를 참고하세요.

> [!NOTE]
> 세션 저장소로 사용되는 Redis 커넥션 지정은 `SESSION_CONNECTION` 환경 변수 또는 `session.php` 설정 파일의 `connection` 옵션을 통해 설정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션 다루기

<a name="retrieving-data"></a>
### 데이터 조회하기

라라벨에서 세션 데이터를 다루는 주요 방법은 전역 `session` 헬퍼와 `Request` 인스턴스를 이용하는 것입니다. 먼저, 라우트 클로저나 컨트롤러 메서드에서 타입 힌트로 주입받을 수 있는 `Request` 인스턴스를 통한 접근 방법을 살펴보겠습니다. 컨트롤러 메서드의 의존성은 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 주입됩니다.

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

세션에서 항목을 조회할 때, `get` 메서드의 두 번째 인수로 기본값을 지정할 수도 있습니다. 해당 키가 세션에 없으면 이 기본값이 반환됩니다. 또한, 기본값으로 클로저를 전달하면, 키가 존재하지 않을 때 해당 클로저가 실행되고 그 결과가 반환됩니다.

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 전역 Session 헬퍼

세션 데이터를 조회하거나 저장할 때, 전역 `session` PHP 함수를 사용할 수도 있습니다. `session` 헬퍼에 하나의 문자열 인수만 전달하면, 해당 세션 키의 값을 반환합니다. 키-값 쌍의 배열을 전달하면, 해당 값들이 세션에 저장됩니다.

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
> HTTP 요청 인스턴스로 세션에 접근하든, 전역 `session` 헬퍼를 사용하든 실질적인 차이가 거의 없습니다. 두 방법 모두 모든 테스트 케이스에서 사용 가능한 `assertSessionHas` 메서드로 [테스트가 가능합니다](/docs/12.x/testing).

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 조회

세션에 저장된 모든 데이터를 한 번에 조회하려면 `all` 메서드를 사용할 수 있습니다.

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 세션 데이터의 일부만 조회

`only`와 `except` 메서드를 이용해 세션 데이터의 부분집합을 조회할 수 있습니다.

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목이 존재하는지 확인

세션에 항목이 존재하는지 확인하려면 `has` 메서드를 사용합니다. 이 메서드는 해당 항목이 존재하고 값이 `null`이 아닌 경우 `true`를 반환합니다.

```php
if ($request->session()->has('users')) {
    // ...
}
```

항목이 세션에 존재하기만 하면(값이 `null`이더라도) 확인하려면 `exists` 메서드를 사용합니다.

```php
if ($request->session()->exists('users')) {
    // ...
}
```

항목이 세션에 존재하지 않는지 확인하려면 `missing` 메서드를 사용할 수 있습니다. 이 메서드는 항목이 없을 때 `true`를 반환합니다.

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### 데이터 저장하기

세션에 데이터를 저장하려면 일반적으로 요청 인스턴스의 `put` 메서드나 전역 `session` 헬퍼를 사용합니다.

```php
// Request 인스턴스 사용
$request->session()->put('key', 'value');

// 전역 "session" 헬퍼 사용
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 형태 세션 값에 값 추가

세션 값이 배열인 경우, `push` 메서드를 사용해 새 값을 추가할 수 있습니다. 예를 들어, `user.teams` 키에 팀 이름 배열이 저장되어 있다면, 아래와 같이 새로운 값을 추가할 수 있습니다.

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 항목 조회 및 삭제

`pull` 메서드는 세션에서 항목을 가져오고 동시에 삭제할 수 있습니다.

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증감

세션 데이터가 정수일 경우, 값을 증가시키거나 감소시킬 때는 `increment`와 `decrement` 메서드를 사용합니다.

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### 플래시 데이터

세션에 데이터를 잠깐 저장하고, 다음 요청에서만 사용하고자 할 때는 `flash` 메서드를 사용합니다. 이 방법으로 저장된 데이터는 즉시 사용할 수 있으며, 바로 다음 HTTP 요청까지 유지됩니다. 이후 해당 데이터는 삭제됩니다. 플래시 데이터는 주로 짧게 표시되는 상태 메시지 등에 유용합니다.

```php
$request->session()->flash('status', 'Task was successful!');
```

플래시 데이터를 여러 요청에 걸쳐 유지해야 한다면 `reflash` 메서드를 사용할 수 있습니다. 특정 플래시 데이터만 유지하려면 `keep` 메서드를 사용하세요.

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

현재 요청에서만 플래시 데이터를 유지하려면 `now` 메서드를 사용합니다.

```php
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
### 데이터 삭제하기

`forget` 메서드를 사용하면 세션에서 특정 데이터를 제거할 수 있습니다. 모든 데이터를 삭제하려면 `flush` 메서드를 사용하세요.

```php
// 단일 키 삭제
$request->session()->forget('name');

// 여러 키 삭제
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성

[세션 고정(Session fixation)](https://owasp.org/www-community/attacks/Session_fixation) 공격을 방지하기 위해, 일반적으로 세션 ID를 재생성합니다.

라라벨에서 제공하는 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)나 [Laravel Fortify](/docs/12.x/fortify)를 사용할 경우, 인증 과정에서 세션 ID가 자동으로 재생성됩니다. 직접 수동으로 세션 ID를 재생성해야 할 경우에는 `regenerate` 메서드를 사용하면 됩니다.

```php
$request->session()->regenerate();
```

세션 ID를 재생성하면서 세션의 모든 데이터도 한 번에 삭제하려면 `invalidate` 메서드를 사용하세요.

```php
$request->session()->invalidate();
```

<a name="session-blocking"></a>
## 세션 블로킹

> [!WARNING]
> 세션 블로킹을 사용하려면, 반드시 [원자적 락(atomic locks)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 드라이버로는 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 패키지인 `mongodb/laravel-mongodb`에 포함), `database`, `file`, `array` 드라이버가 있습니다. 또한, `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 라라벨은 동일한 세션을 사용하는 요청이 동시에 실행되는 것을 허용합니다. 예를 들어, JavaScript HTTP 라이브러리를 통해 동시에 두 개의 HTTP 요청을 보내면, 두 요청이 동시에 실행됩니다. 대부분의 애플리케이션에서는 큰 문제가 되지 않지만, 동시에 서로 다른 엔드포인트에서 모두 세션에 데이터를 저장하는 소수 애플리케이션에서는 세션 데이터 손실이 발생할 수 있습니다.

이 문제를 해결하기 위해, 라라벨은 특정 세션에 대해 동시에 실행되는 요청 수를 제한할 수 있는 기능을 제공합니다. 시작하려면, 라우트 정의에 `block` 메서드를 체이닝하면 됩니다. 아래 예시에서는 `/profile` 엔드포인트에 들어오는 요청이 세션 락을 획득하게 됩니다. 이 락이 유지되는 동안 같은 세션 ID를 공유하는 `/profile`이나 `/order` 엔드포인트로 들어오는 다른 요청들은 첫 번째 요청이 실행을 마칠 때까지 대기하게 됩니다.

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

`block` 메서드는 두 개의 선택적 인수를 받을 수 있습니다. 첫 번째 인수는 세션 락을 최대 몇 초간 유지할지 지정합니다. 요청 처리가 일찍 끝날 경우, 락도 그 즉시 해제됩니다.

두 번째 인수는 세션 락을 얻기 위해 요청이 최대 몇 초간 대기할지를 지정합니다. 주어진 시간 동안 세션 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

만약 인수를 따로 지정하지 않으면, 락은 최대 10초간 유지되며, 락 취득을 위해 요청도 최대 10초간 대기합니다.

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
## 사용자 정의 세션 드라이버 추가

<a name="implementing-the-driver"></a>
### 드라이버 구현

기존 세션 드라이버가 애플리케이션 요구에 맞지 않을 경우, 직접 세션 핸들러를 구현할 수 있습니다. 커스텀 세션 드라이버는 PHP의 내장 인터페이스인 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스에는 몇 가지 간단한 메서드만 정의되어 있습니다. 아래는 MongoDB를 예시로 한 스텁 코드입니다.

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

라라벨은 확장 기능을 위한 기본 디렉터리를 제공하지 않으므로, 원하는 위치에 자유롭게 저장할 수 있습니다. 위 예시에서는 `Extensions` 디렉터리를 만들어 `MongoSessionHandler`를 배치한 모습입니다.

각 메서드가 어떤 역할을 하는지 바로 이해하기 어려울 수 있으니, 간단히 설명을 추가합니다.

<div class="content-list" markdown="1">

- `open` 메서드는 보통 파일 기반 세션 스토어 시스템에서 사용됩니다. 라라벨에는 `file` 세션 드라이버가 포함되어 있으나, 대부분의 경우 이 메서드에는 특별한 처리가 필요하지 않으니 비워두어도 됩니다.
- `close` 메서드 역시 대부분의 드라이버에서 필요하지 않으므로, 대개 무시할 수 있습니다.
- `read` 메서드는 주어진 `$sessionId`에 연결된 세션 데이터를 문자열 형태로 반환해야 합니다. 세션 데이터의 직렬화나 인코딩 처리는 라라벨이 자동으로 처리하므로, 직접 신경쓸 필요가 없습니다.
- `write` 메서드는 주어진 `$sessionId`에 연결된 `$data` 문자열을 MongoDB나 기타 원하는 영구 저장소에 기록해야 합니다. 마찬가지로, 직접 직렬화할 필요는 없습니다.
- `destroy` 메서드는 주어진 `$sessionId`에 연결된 데이터를 저장소에서 삭제해야 합니다.
- `gc` 메서드는 `$lifetime`(UNIX 타임스탬프)보다 오래된 모든 세션 데이터를 삭제해야 합니다. Memcached나 Redis처럼 자동으로 만료되는 시스템에서는 이 메서드를 비워둬도 괜찮습니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록

드라이버를 구현했다면, 이제 라라벨에 등록할 준비가 되었습니다. 라라벨 세션 백엔드에 드라이버를 추가하려면 `Session` [파사드](/docs/12.x/facades)에서 제공하는 `extend` 메서드를 사용하면 됩니다. 이 메서드는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출해야 합니다. 기존의 `App\Providers\AppServiceProvider`에서 해도 되고, 완전히 새로운 프로바이더를 만들어도 됩니다.

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
            // SessionHandlerInterface 구현체 반환
            return new MongoSessionHandler;
        });
    }
}
```

세션 드라이버 등록이 끝났으면, 애플리케이션의 세션 드라이버를 `SESSION_DRIVER` 환경 변수나 `config/session.php` 설정 파일에서 `mongo`로 지정할 수 있습니다.
