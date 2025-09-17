# HTTP 세션 (HTTP Session)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비](#driver-prerequisites)
- [세션과 상호작용하기](#interacting-with-the-session)
    - [데이터 조회](#retrieving-data)
    - [데이터 저장](#storing-data)
    - [Flash 데이터](#flash-data)
    - [데이터 삭제](#deleting-data)
    - [세션 ID 재생성](#regenerating-the-session-id)
- [세션 캐시](#session-cache)
- [세션 블로킹](#session-blocking)
- [커스텀 세션 드라이버 추가](#adding-custom-session-drivers)
    - [드라이버 구현](#implementing-the-driver)
    - [드라이버 등록](#registering-the-driver)

<a name="introduction"></a>
## 소개 (Introduction)

HTTP 기반 애플리케이션은 상태를 유지하지 않기 때문에, 세션은 여러 요청에 걸쳐 사용자에 대한 정보를 저장하는 방법을 제공합니다. 이러한 사용자 정보는 일반적으로 이후의 요청에서 접근할 수 있도록 영속적인 저장소(백엔드)에 저장됩니다.

Laravel은 다양한 세션 백엔드를 제공하며, 이는 표현적이고 통합된 API를 통해 접근할 수 있습니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스와 같은 인기 있는 백엔드는 기본적으로 지원됩니다.

<a name="configuration"></a>
### 설정 (Configuration)

애플리케이션의 세션 설정 파일은 `config/session.php`에 저장됩니다. 이 파일에서 사용할 수 있는 다양한 옵션을 반드시 검토하시기 바랍니다. 기본적으로 Laravel은 `database` 세션 드라이버를 사용하도록 설정되어 있습니다.

세션의 `driver` 설정 옵션은 각 요청에 대해 세션 데이터가 어디에 저장될지를 정의합니다. Laravel은 여러 드라이버를 포함하고 있습니다:

<div class="content-list" markdown="1">

- `file` - 세션이 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션이 보안이 유지되고 암호화된 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 이러한 빠른 캐시 기반 저장소에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며, 영구적으로 저장되지 않습니다.

</div>

> [!NOTE]
> `array` 드라이버는 주로 [테스트](/docs/12.x/testing) 환경에서 사용되며, 세션에 저장된 데이터가 영구적으로 저장되지 않도록 합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 (Driver Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 경우, 세션 데이터를 저장할 데이터베이스 테이블이 필요합니다. 보통 이 테이블은 Laravel의 기본 `0001_01_01_000000_create_users_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있지만, 만약 `sessions` 테이블이 없다면, `make:session-table` Artisan 명령어로 이 마이그레이션을 생성할 수 있습니다:

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 프로그램을 설치하거나 Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 설정에 대한 더 많은 정보는 Laravel의 [Redis 문서](/docs/12.x/redis#configuration)를 참고하세요.

> [!NOTE]
> `SESSION_CONNECTION` 환경 변수 또는 `session.php` 설정 파일의 `connection` 옵션은 세션 저장에 사용할 Redis 연결을 지정하는 데 사용할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기 (Interacting With the Session)

<a name="retrieving-data"></a>
### 데이터 조회 (Retrieving Data)

Laravel에서는 세션 데이터를 다루는 주된 방법이 두 가지 있습니다: 글로벌 `session` 헬퍼를 사용하거나, `Request` 인스턴스를 사용하는 방법입니다. 먼저, `Request` 인스턴스를 통해 세션에 접근하는 방법을 살펴보겠습니다. 이 인스턴스는 라우트 클로저나 컨트롤러 메서드에서 타입힌트로 주입할 수 있습니다. 컨트롤러 메서드의 의존성은 Laravel [서비스 컨테이너](/docs/12.x/container)에 의해 자동으로 주입된다는 점을 기억하세요.

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

세션에서 항목을 조회할 때, `get` 메서드의 두 번째 인수로 기본값을 전달할 수 있습니다. 지정한 키가 세션에 존재하지 않을 경우 이 기본값이 반환됩니다. 만약 클로저를 기본값으로 전달하면, 요청한 키가 존재하지 않을 때 해당 클로저가 실행되고 그 결과가 반환됩니다:

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 글로벌 Session 헬퍼

글로벌 `session` PHP 함수를 사용해서도 세션에서 데이터를 조회하고 저장할 수 있습니다. `session` 헬퍼를 하나의 문자열 인수와 함께 호출하면 해당 세션 키의 값을 반환하며, 키/값 쌍의 배열로 호출하면 해당 값들이 세션에 저장됩니다:

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
> HTTP 요청 인스턴스를 통한 세션 접근과 글로벌 `session` 헬퍼를 사용하는 데에는 실질적인 차이가 거의 없습니다. 두 방법 모두 `assertSessionHas` 메서드를 통해 모든 테스트 케이스에서 [테스트](/docs/12.x/testing)할 수 있습니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 조회

세션에 저장된 모든 데이터를 조회하고 싶다면, `all` 메서드를 사용할 수 있습니다:

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 일부 세션 데이터만 조회

`only` 및 `except` 메서드를 사용하면 세션 데이터 중 일부만 선택적으로 조회할 수 있습니다:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목이 있는지 확인하기

세션에 특정 항목이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. `has` 메서드는 해당 항목이 존재하고 그 값이 `null`이 아닐 경우 `true`를 반환합니다:

```php
if ($request->session()->has('users')) {
    // ...
}
```

특정 항목이 세션에 존재하는지(값이 `null`이어도 상관없이) 확인하려면 `exists` 메서드를 사용하세요:

```php
if ($request->session()->exists('users')) {
    // ...
}
```

세션에 항목이 존재하지 않는지 확인하려면 `missing` 메서드를 사용할 수 있습니다. `missing` 메서드는 해당 항목이 존재하지 않으면 `true`를 반환합니다:

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### 데이터 저장 (Storing Data)

세션에 데이터를 저장하려면, 보통 요청 인스턴스의 `put` 메서드나 글로벌 `session` 헬퍼를 사용합니다:

```php
// Request 인스턴스를 통해...
$request->session()->put('key', 'value');

// 글로벌 "session" 헬퍼를 통해...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 세션 값에 데이터 추가

`push` 메서드를 사용하면 배열 형태의 세션 값에 새로운 값을 추가할 수 있습니다. 예를 들어, `user.teams` 키가 팀 이름의 배열을 가지고 있다면 다음과 같이 값을 추가할 수 있습니다:

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 항목을 조회하고 동시에 삭제하기

`pull` 메서드는 특정 항목을 세션에서 조회하고, 그 항목을 즉시 삭제합니다:

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가 및 감소

세션 데이터에 정수가 저장되어 있고 이를 증가하거나 감소시키고 싶을 때는 `increment`, `decrement` 메서드를 사용할 수 있습니다:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### Flash 데이터 (Flash Data)

가끔 다음 요청에만 사용할 데이터를 세션에 저장하고 싶은 경우가 있습니다. 이럴 때는 `flash` 메서드를 사용할 수 있습니다. 이 방법으로 저장된 데이터는 즉시 사용 가능하며, 다음 HTTP 요청까지 유지됩니다. 이후에는 자동으로 삭제됩니다. Flash 데이터는 주로 잠깐 보여줄 상태 메시지 저장에 유용합니다:

```php
$request->session()->flash('status', 'Task was successful!');
```

여러 요청에 걸쳐 flash 데이터를 유지해야 한다면 `reflash` 메서드를 사용할 수 있고, 특정 flash 데이터만 유지하고 싶다면 `keep` 메서드를 사용할 수 있습니다:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

flash 데이터를 현재 요청에서만 유지하고 싶다면 `now` 메서드를 사용하세요:

```php
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
### 데이터 삭제 (Deleting Data)

`forget` 메서드는 세션에서 특정 데이터를 삭제합니다. 세션의 모든 데이터를 삭제하려면 `flush` 메서드를 사용할 수 있습니다.

```php
// 단일 키 삭제...
$request->session()->forget('name');

// 여러 키 삭제...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성 (Regenerating the Session ID)

세션 ID를 재생성하는 작업은 [세션 고정(Session Fixation)](https://owasp.org/www-community/attacks/Session_fixation) 공격을 방지하기 위해 자주 수행됩니다.

Laravel은 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)나 [Laravel Fortify](/docs/12.x/fortify)를 사용하는 경우 인증 과정 중에 세션 ID를 자동으로 재생성합니다. 그러나 필요하다면 직접 `regenerate` 메서드를 사용하여 세션 ID를 수동으로 재생성할 수 있습니다:

```php
$request->session()->regenerate();
```

세션 ID를 재생성하고 모든 세션 데이터를 한 번에 제거하려면 `invalidate` 메서드를 사용할 수 있습니다:

```php
$request->session()->invalidate();
```

<a name="session-cache"></a>
## 세션 캐시 (Session Cache)

Laravel의 세션 캐시는 개별 사용자 세션에 한정된 데이터를 캐시하는 편리한 방법을 제공합니다. 전역 애플리케이션 캐시와 달리, 세션 캐시 데이터는 세션별로 자동 분리되며, 세션이 만료되거나 삭제될 때 함께 정리됩니다. 세션 캐시는 [Laravel 캐시 메서드](/docs/12.x/cache)의 `get`, `put`, `remember`, `forget` 등을 동일하게 제공하지만, 현재 세션 범위로 제한되어 동작합니다.

세션 캐시는 같은 세션 내에서 여러 요청에 걸쳐 임시로 사용자별 데이터를 저장할 때 적합합니다. 예를 들어 폼 데이터, 임시 계산 결과, API 응답, 또는 특정 사용자 세션에 묶여야 하는 기타 임시 데이터들을 관리할 때 사용할 수 있습니다.

세션의 `cache` 메서드를 통해 세션 캐시에 접근할 수 있습니다:

```php
$discount = $request->session()->cache()->get('discount');

$request->session()->cache()->put(
    'discount', 10, now()->addMinutes(5)
);
```

Laravel의 캐시 메서드에 대한 더 많은 정보는 [캐시 문서](/docs/12.x/cache)를 참고하세요.

<a name="session-blocking"></a>
## 세션 블로킹 (Session Blocking)

> [!WARNING]
> 세션 블로킹을 사용하려면, 애플리케이션이 [원자적 락](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 캐시 드라이버는 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 `mongodb/laravel-mongodb` 패키지 포함), `database`, `file`, `array` 드라이버입니다. 또한, `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 Laravel은 같은 세션을 사용하는 요청이 동시에 실행되는 것을 허용합니다. 예를 들어, JavaScript HTTP 라이브러리를 통해 두 개의 HTTP 요청을 애플리케이션에 보내면 두 요청 모두 동시에 처리됩니다. 대부분의 애플리케이션에서는 문제가 없지만, 드물게 서로 다른 엔드포인트에 동시 요청하면서 두 요청 모두 세션에 데이터를 기록하는 경우 세션 데이터 손실이 발생할 수 있습니다.

이 문제를 완화하기 위해, Laravel은 특정 세션에 대해 동시 요청을 제한할 수 있는 기능을 제공합니다. 사용 방법은 간단하며, 라우트 정의에 `block` 메서드를 체이닝하면 됩니다. 다음 예시에서 `/profile` 엔드포인트에 들어오는 요청은 세션 락을 획득하게 됩니다. 이 락이 유지되는 동안 같은 세션 ID를 공유하는 사용자가 동시에 `/profile`이나 `/order` 엔드포인트로 추가 요청을 보낸 경우, 최초 요청이 처리될 때까지 대기하게 됩니다.

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

`block` 메서드는 두 가지 선택적 인수를 받을 수 있습니다. 첫 번째 인수는 세션 락을 최대 몇 초 동안 유지할지 지정하며, 요청이 더 빨리 처리될 경우 락은 빠르게 해제됩니다.

두 번째 인수는 세션 락을 얻기 위해 요청이 최대 몇 초까지 대기할지 의미합니다. 만약 해당 시간 내에 락을 얻지 못하면, `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다.

이러한 인수들을 생략하면 락은 최대 10초 동안 유지되며, 요청은 락을 얻기 위해 최대 10초까지 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가 (Adding Custom Session Drivers)

<a name="implementing-the-driver"></a>
### 드라이버 구현 (Implementing the Driver)

기존의 세션 드라이버가 애플리케이션의 요구사항을 충족하지 못하는 경우, Laravel에서는 직접 세션 핸들러를 작성할 수 있습니다. 커스텀 세션 드라이버는 PHP에서 내장된 `SessionHandlerInterface`를 구현해야 합니다. 해당 인터페이스에는 몇 가지 간단한 메서드만 포함되어 있습니다. 다음은 MongoDB 기반의 구현 예시입니다:

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

Laravel은 기본적으로 확장 기능을 위한 디렉터리를 제공하지 않습니다. 따라서 코드를 자유롭게 원하는 위치에 둘 수 있습니다. 위 예시에서는 `Extensions` 디렉터리를 생성하여 `MongoSessionHandler`를 보관했습니다.

각 메서드의 목적이 즉시 이해되지 않을 수 있으므로, 여기서는 각 메서드의 용도를 간단히 설명합니다:

<div class="content-list" markdown="1">

- `open` 메서드는 주로 파일 기반 세션 저장소 시스템에서 사용됩니다. Laravel에 이미 `file` 세션 드라이버가 있기 때문에, 대부분의 경우 이 메서드는 비워둬도 무방합니다.
- `close` 메서드 또한 대부분의 드라이버에서 특별히 구현할 필요가 없습니다.
- `read` 메서드는 지정된 `$sessionId`와 연관된 세션 데이터를 문자열 형태로 반환해야 합니다. 데이터 직렬화나 인코딩 처리는 필요하지 않습니다. Laravel이 이를 대신 처리합니다.
- `write` 메서드는 `$sessionId`와 연관된 `$data` 문자열을 MongoDB나 다른 저장소와 같은 영구 저장 시스템에 기록해야 합니다. 이 역시 직접 직렬화 작업을 할 필요는 없습니다. Laravel이 이미 처리합니다.
- `destroy` 메서드는 `$sessionId`와 연관된 데이터를 영구 저장소에서 제거해야 합니다.
- `gc` 메서드는 주어진 `$lifetime`(UNIX 타임스탬프)보다 오래된 모든 세션 데이터를 삭제해야 합니다. Memcached, Redis와 같이 자체 만료 기능이 있는 시스템을 사용할 경우, 이 메서드는 비워둬도 무방합니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록 (Registering the Driver)

드라이버를 구현했다면 이제 Laravel에 등록할 차례입니다. Laravel의 세션 백엔드에 추가적인 드라이버를 등록하려면, `Session` [파사드](/docs/12.x/facades)에서 제공하는 `extend` 메서드를 사용할 수 있습니다. 이 메서드는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출해야 합니다. 기존의 `App\Providers\AppServiceProvider`에서 호출해도 되고, 새로운 프로바이더를 생성해도 됩니다:

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
            // SessionHandlerInterface 구현체를 반환...
            return new MongoSessionHandler;
        });
    }
}
```

세션 드라이버 등록이 완료되면, `SESSION_DRIVER` 환경 변수나 애플리케이션의 `config/session.php` 설정 파일에서 `mongo` 드라이버를 세션 드라이버로 지정해 사용할 수 있습니다.
