# HTTP 세션

- [소개](#소개)
    - [설정](#설정)
    - [드라이버 사전 요구사항](#드라이버-사전-요구사항)
- [세션과 상호작용하기](#세션과-상호작용하기)
    - [데이터 조회](#데이터-조회)
    - [데이터 저장](#데이터-저장)
    - [Flash 데이터](#flash-데이터)
    - [데이터 삭제](#데이터-삭제)
    - [세션 ID 재생성](#세션-id-재생성)
- [세션 차단](#세션-차단)
- [커스텀 세션 드라이버 추가](#커스텀-세션-드라이버-추가)
    - [드라이버 구현](#드라이버-구현)
    - [드라이버 등록](#드라이버-등록)

<a name="introduction"></a>
## 소개

HTTP 기반 애플리케이션은 상태를 유지하지 않기 때문에, 세션은 사용자의 정보를 여러 요청에 걸쳐 저장하는 방법을 제공합니다. 이 사용자 정보는 보통 지속적인 저장소/백엔드에 저장되어 이후의 요청에서 접근할 수 있습니다.

Laravel은 표현력이 뛰어난 통합 API를 통해 접근할 수 있는 다양한 세션 백엔드를 기본 제공하며, [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스 등 인기 있는 백엔드들을 지원합니다.

<a name="configuration"></a>
### 설정

애플리케이션의 세션 설정 파일은 `config/session.php`에 저장되어 있습니다. 이 파일에서 사용할 수 있는 옵션들을 반드시 검토하세요. Laravel은 기본적으로 `database` 세션 드라이버를 사용하도록 설정되어 있습니다.

세션의 `driver` 설정 옵션은 각 요청에 대해 세션 데이터가 어디에 저장될 것인지를 정의합니다. Laravel에서는 다양한 드라이버를 지원합니다:

<div class="content-list" markdown="1">

- `file` - 세션이 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션이 안전하게 암호화된 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 이 빠른 캐시 기반 저장소에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며, 지속적으로 저장되지 않습니다.

</div>

> [!NOTE]  
> `array` 드라이버는 주로 [테스트](/docs/{{version}}/testing) 환경에서 사용되며, 세션에 저장된 데이터가 영구적으로 저장되지 않도록 합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 때는 세션 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel의 기본 `0001_01_01_000000_create_users_table.php` [데이터베이스 마이그레이션](/docs/{{version}}/migrations)에 포함되어 있지만, 만약 `sessions` 테이블이 없다면 `make:session-table` Artisan 명령어로 해당 마이그레이션을 생성할 수 있습니다.

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하기 전에, PECL을 통해 PhpRedis PHP 확장자를 설치하거나, Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 설정에 대한 자세한 내용은 Laravel의 [Redis 문서](/docs/{{version}}/redis#configuration)를 참고하세요.

> [!NOTE]  
> 세션 저장소에 사용할 Redis 연결은 `SESSION_CONNECTION` 환경 변수 또는 `session.php` 설정 파일의 `connection` 옵션으로 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기

<a name="retrieving-data"></a>
### 데이터 조회

Laravel에서 세션 데이터를 사용할 때는, 전역 `session` 헬퍼와 `Request` 인스턴스 등 두 가지 주요 방법이 있습니다. 먼저, 라우트 클로저나 컨트롤러 메서드에서 타입 힌트를 사용해 `Request` 인스턴스를 통해 세션에 접근하는 방법을 보겠습니다. 컨트롤러 메서드의 의존성은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 표시합니다.
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

세션에서 값을 조회할 때, `get` 메서드의 두 번째 인수로 기본값을 전달할 수 있습니다. 지정한 키가 세션에 없을 경우 이 기본값이 반환됩니다. 만약 기본값으로 클로저를 전달하면, 요청한 키가 없을 때 클로저를 실행하고 그 결과를 반환합니다.

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 전역 Session 헬퍼

전역 `session` PHP 함수를 사용하여 세션에서 데이터를 조회하거나 저장할 수도 있습니다. `session` 헬퍼에 문자열 하나를 전달하면 해당 세션 키의 값을 반환합니다. 키/값 쌍의 배열을 전달하면 해당 값들이 세션에 저장됩니다.

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
> HTTP 요청 인스턴스를 통한 세션 사용과 전역 `session` 헬퍼 사용은 실질적인 차이가 거의 없습니다. 두 방법 모두 `assertSessionHas` 메서드를 통해 [테스트 가능](/docs/{{version}}/testing)하며, 이 메서드는 모든 테스트 케이스에서 사용할 수 있습니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 조회

세션의 모든 데이터를 조회하려면 `all` 메서드를 사용할 수 있습니다.

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 일부 세션 데이터만 조회

`only`와 `except` 메서드를 사용하면 세션 데이터의 일부만 선택적으로 조회할 수 있습니다.

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목이 존재하는지 확인하기

세션에 항목이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. `has`는 해당 항목이 존재하고 `null`이 아니면 `true`를 반환합니다.

```php
if ($request->session()->has('users')) {
    // ...
}
```

값이 `null`이더라도 세션에 항목이 존재하는지 확인하려면 `exists` 메서드를 사용합니다.

```php
if ($request->session()->exists('users')) {
    // ...
}
```

세션에 항목이 존재하지 않는지 확인하려면 `missing` 메서드를 사용할 수 있습니다. `missing`은 해당 항목이 없을 때 `true`를 반환합니다.

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### 데이터 저장

세션에 데이터를 저장하려면 보통 요청 인스턴스의 `put` 메서드 또는 전역 `session` 헬퍼를 사용합니다.

```php
// 요청 인스턴스를 통해...
$request->session()->put('key', 'value');

// 전역 "session" 헬퍼를 통해...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 세션 값에 push

세션 데이터가 배열일 때는 `push` 메서드로 새 값을 추가할 수 있습니다. 예를 들어, `user.teams` 키가 팀 이름의 배열이라면 새로운 값을 다음과 같이 추가합니다.

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 항목 조회와 삭제

`pull` 메서드는 세션에서 항목을 조회하고 동시에 삭제합니다.

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가/감소

세션 데이터에 정수가 있고, 이를 증가시키거나 감소시키려면 `increment`와 `decrement` 메서드를 사용할 수 있습니다.

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### Flash 데이터

세션에 데이터를 다음 요청에만 임시로 저장하고 싶다면 `flash` 메서드를 사용할 수 있습니다. 이 방법으로 저장한 데이터는 바로 사용할 수 있고, 다음 HTTP 요청에서도 사용할 수 있습니다. 이후 요청에는 flash 데이터가 삭제됩니다. flash 데이터는 주로 일시적인 상태 메시지에 유용합니다.

```php
$request->session()->flash('status', '작업이 성공적으로 완료되었습니다!');
```

여러 요청에 걸쳐 flash 데이터를 유지하려면 `reflash` 메서드를 사용할 수 있습니다. 특정 flash 데이터만 유지하려면 `keep` 메서드를 사용합니다.

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

flash 데이터를 현재 요청에서만 유지하려면 `now` 메서드를 사용합니다.

```php
$request->session()->now('status', '작업이 성공적으로 완료되었습니다!');
```

<a name="deleting-data"></a>
### 데이터 삭제

`forget` 메서드는 세션에서 특정 데이터를 삭제하고, 세션의 모든 데이터를 삭제하려면 `flush` 메서드를 사용할 수 있습니다.

```php
// 단일 키 삭제...
$request->session()->forget('name');

// 여러 키 삭제...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성

세션 ID를 재생성하는 것은 [세션 고정화 공격](https://owasp.org/www-community/attacks/Session_fixation)을 방지하기 위해 자주 사용됩니다.

Laravel의 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)이나 [Laravel Fortify](/docs/{{version}}/fortify)를 사용할 경우, Laravel은 인증 과정에서 자동으로 세션 ID를 재생성합니다. 하지만 수동으로 세션 ID를 재생성하고 싶다면 `regenerate` 메서드를 사용하면 됩니다.

```php
$request->session()->regenerate();
```

세션 ID를 재생성하고 동시에 세션의 모든 데이터를 삭제하려면 `invalidate` 메서드를 사용하세요.

```php
$request->session()->invalidate();
```

<a name="session-blocking"></a>
## 세션 차단

> [!WARNING]  
> 세션 차단을 사용하려면, 애플리케이션에서 [원자적 락](/docs/{{version}}/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 드라이버로는 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 `mongodb/laravel-mongodb` 패키지 포함), `database`, `file`, `array` 드라이버가 있습니다. 단, `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 Laravel은 동일한 세션을 사용하는 요청들이 동시에 실행될 수 있도록 허용합니다. 예를 들어, JavaScript HTTP 라이브러리를 사용해 두 개의 HTTP 요청을 동시에 보내면 두 요청이 동시에 실행됩니다. 대부분의 애플리케이션에서 이는 문제가 되지 않지만, 서로 다른 엔드포인트에 동시에 요청하여 모두 세션에 데이터를 기록하는 경우 소수의 애플리케이션에서 세션 데이터 손실이 발생할 수 있습니다.

이를 방지하기 위해, Laravel은 동일한 세션에 대한 동시 요청을 제한할 수 있는 기능을 제공합니다. 사용 방법은 라우트 정의에 `block` 메서드를 체이닝하면 됩니다. 아래 예시에서, `/profile` 엔드포인트로 들어온 요청은 세션 락을 획득합니다. 이 락이 유지되는 동안 동일한 세션 ID를 가진 `/profile` 또는 `/order` 엔드포인트의 다른 요청은 첫 번째 요청이 끝날 때까지 대기하게 됩니다.

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

`block` 메서드는 두 개의 선택적 인수를 받습니다. 첫 번째 인수는 락을 최대 몇 초 동안 유지할지, 두 번째 인수는 락을 획득하기 위해 요청이 대기할 최대 초 수를 지정합니다. 지정한 시간 내에 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다.

이 인수를 전달하지 않으면 락은 기본적으로 최대 10초이며 요청은 락 획득을 위해 최대 10초 동안 대기합니다.

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가

<a name="implementing-the-driver"></a>
### 드라이버 구현

기존 세션 드라이버가 애플리케이션의 요구사항에 맞지 않는 경우, Laravel은 직접 세션 핸들러를 작성할 수 있도록 지원합니다. 커스텀 세션 드라이버는 PHP의 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스는 몇 가지 간단한 메서드만 포함하고 있습니다. MongoDB에 대한 샘플 구현은 다음과 같습니다.

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

Laravel은 확장 기능을 위한 기본 디렉토리를 제공하지 않으므로, 자유롭게 원하는 위치에 파일을 둘 수 있습니다. 예제에서는 `Extensions` 디렉토리를 만들어 `MongoSessionHandler`를 배치했습니다.

각 메서드의 목적이 곧바로 이해되기 어렵기 때문에 간단한 설명을 드립니다.

<div class="content-list" markdown="1">

- `open` 메서드는 주로 파일 기반 세션 저장 시스템에서 사용됩니다. Laravel은 이미 `file` 세션 드라이버를 제공하므로 보통 별다른 구현 없이 비워 둘 수 있습니다.
- `close` 메서드도 일반적으로 고려하지 않아도 되며, 대부분의 드라이버에서는 필요하지 않습니다.
- `read` 메서드는 주어진 `$sessionId`에 연결된 세션 데이터의 문자열 버전을 반환해야 합니다. 직렬화 등 추가 인코딩을 수행할 필요가 없으며, Laravel이 담당합니다.
- `write` 메서드는 주어진 `$data` 문자열과 `$sessionId`를 영속적인 저장소에 기록해야 합니다(MongoDB 등). 직렬화는 Laravel이 이미 처리하므로, 별도의 작업이 필요 없습니다.
- `destroy` 메서드는 `$sessionId`에 연결된 데이터를 영구 저장소에서 삭제해야 합니다.
- `gc` 메서드는 주어진 `$lifetime`(UNIX 타임스탬프)보다 오래된 모든 세션 데이터를 삭제해야 합니다. Memcached, Redis와 같은 자동 만료 시스템의 경우 이 메서드는 비워둘 수 있습니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록

드라이버 구현이 완료되면, 이를 Laravel에 등록할 차례입니다. 추가 세션 드라이버를 Laravel 세션 시스템에 등록하려면, `Session` [파사드](/docs/{{version}}/facades)에서 제공하는 `extend` 메서드를 사용할 수 있습니다. 보통 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 호출하면 됩니다. 기존의 `App\Providers\AppServiceProvider`에서 하거나 별도의 프로바이더를 새로 만들어도 됩니다.

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
     * 애플리케이션의 서비스를 등록합니다.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션의 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Session::extend('mongo', function (Application $app) {
            // SessionHandlerInterface 구현체 반환...
            return new MongoSessionHandler;
        });
    }
}
```

세션 드라이버가 등록되면, `SESSION_DRIVER` 환경 변수나 애플리케이션의 `config/session.php` 설정 파일에 드라이버로 `mongo`를 지정해서 사용할 수 있습니다.