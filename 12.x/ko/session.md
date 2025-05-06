# HTTP 세션

- [소개](#소개)
    - [구성](#구성)
    - [드라이버 사전 조건](#드라이버-사전-조건)
- [세션과 상호 작용하기](#세션과-상호-작용하기)
    - [데이터 조회](#데이터-조회)
    - [데이터 저장](#데이터-저장)
    - [플래시 데이터](#플래시-데이터)
    - [데이터 삭제](#데이터-삭제)
    - [세션 ID 재생성](#세션-id-재생성)
- [세션 블로킹](#세션-블로킹)
- [커스텀 세션 드라이버 추가](#커스텀-세션-드라이버-추가)
    - [드라이버 구현](#드라이버-구현)
    - [드라이버 등록](#드라이버-등록)

<a name="introduction"></a>
## 소개

HTTP 기반 애플리케이션은 상태가 없으므로, 세션은 여러 요청에 걸쳐 사용자 정보를 저장하는 방법을 제공합니다. 이러한 사용자 정보는 일반적으로 지속 가능한 저장소/백엔드에 저장되어 이후의 요청에서도 접근할 수 있습니다.

Laravel은 다양한 세션 백엔드를 제공하며, 이는 간결하고 통일된 API를 통해 액세스할 수 있습니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스와 같은 인기 있는 백엔드 지원도 포함되어 있습니다.

<a name="configuration"></a>
### 구성

애플리케이션의 세션 구성 파일은 `config/session.php`에 위치합니다. 이 파일의 사용 가능한 옵션들을 꼭 검토하세요. 기본적으로 Laravel은 `database` 세션 드라이버를 사용하도록 설정되어 있습니다.

세션의 `driver` 구성 옵션은 각 요청마다 세션 데이터가 어디에 저장될지 정의합니다. Laravel은 여러 가지 드라이버를 포함합니다:

<div class="content-list" markdown="1">

- `file` - 세션이 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션이 안전하고 암호화된 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 이러한 빠른 캐시 기반 저장소에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며, 영구적으로 저장되지 않습니다.

</div>

> [!NOTE]
> `array` 드라이버는 주로 [테스트](/docs/{{version}}/testing) 시 사용되며, 세션에 저장된 데이터가 영구적으로 저장되지 않도록 합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 조건

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 경우, 세션 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 이는 Laravel의 기본 `0001_01_01_000000_create_users_table.php` [데이터베이스 마이그레이션](/docs/{{version}}/migrations)에 포함되어 있지만, 만약 `sessions` 테이블이 없다면 `make:session-table` Artisan 명령어를 사용하여 마이그레이션 파일을 생성할 수 있습니다:

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 프로그램을 설치하거나 Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 구성에 대한 자세한 정보는 Laravel의 [Redis 문서](/docs/{{version}}/redis#configuration)를 참고하세요.

> [!NOTE]
> `SESSION_CONNECTION` 환경 변수 또는 `session.php` 구성 파일의 `connection` 옵션을 사용하여 세션 저장소에 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호 작용하기

<a name="retrieving-data"></a>
### 데이터 조회

Laravel에서 세션 데이터를 다루는 주요 방법은 전역 `session` 헬퍼와 `Request` 인스턴스를 이용하는 것입니다. 먼저, 라우트 클로저 또는 컨트롤러 메서드에서 타입 힌트로 주입할 수 있는 `Request` 인스턴스를 통한 세션 접근 방법을 살펴보겠습니다. 참고로, 컨트롤러 메서드 의존성은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입됩니다:

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

세션에서 항목을 가져올 때, `get` 메서드의 두 번째 인수로 기본값을 전달할 수도 있습니다. 지정한 키가 세션에 존재하지 않으면 이 기본값이 반환됩니다. 또한, 기본값으로 클로저를 전달하고 요청한 키가 없다면, 해당 클로저가 실행되어 그 결과가 반환됩니다:

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 전역 세션 헬퍼

전역 `session` PHP 함수를 사용하여 세션에서 데이터를 조회하거나 저장할 수도 있습니다. 이 헬퍼를 문자열 하나로 호출하면 해당 세션 키의 값을 반환합니다. 키/값 쌍의 배열로 호출하면, 해당 값들이 세션에 저장됩니다:

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
> HTTP 요청 인스턴스를 통한 세션 사용과 전역 `session` 헬퍼 사용 간에는 실질적인 차이가 거의 없습니다. 두 방법 모두 테스트 케이스에서 제공되는 `assertSessionHas` 메서드를 통해 [테스트](/docs/{{version}}/testing)가 가능합니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 조회

세션의 모든 데이터를 조회하려면, `all` 메서드를 사용할 수 있습니다:

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 일부 세션 데이터 조회

`only`와 `except` 메서드를 이용해 세션 데이터의 일부만 조회할 수 있습니다:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목이 존재하는지 확인

세션에 항목이 존재하는지 확인하려면, `has` 메서드를 사용할 수 있습니다. `has`는 항목이 존재하고 `null`이 아니라면 `true`를 반환합니다:

```php
if ($request->session()->has('users')) {
    // ...
}
```

항목이 세션에 존재하는지(값이 `null`이어도) 확인하려면, `exists` 메서드를 사용하세요:

```php
if ($request->session()->exists('users')) {
    // ...
}
```

세션에 항목이 없는지 확인하려면, `missing` 메서드를 사용할 수 있습니다. `missing` 메서드는 항목이 없을 때 `true`를 반환합니다:

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### 데이터 저장

세션에 데이터를 저장하려면, 보통 요청 인스턴스의 `put` 메서드나 전역 `session` 헬퍼를 사용합니다:

```php
// 요청 인스턴스를 통한 방법...
$request->session()->put('key', 'value');

// 전역 "session" 헬퍼를 통한 방법...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 세션 값에 값 추가

`push` 메서드를 사용해 배열로 이루어진 세션 값에 새 값을 추가할 수 있습니다. 예를 들어, `user.teams` 키가 팀 이름의 배열이라면, 새 값을 다음과 같이 추가할 수 있습니다:

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 항목 조회 및 삭제

`pull` 메서드는 세션에서 항목을 조회하면서 동시에 삭제합니다:

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값을 증가/감소시키기

세션 데이터가 정수일 경우, `increment`와 `decrement` 메서드를 통해 값을 증가 또는 감소시킬 수 있습니다:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### 플래시 데이터

가끔 다음 요청에만 사용할 데이터를 세션에 저장하고 싶을 때가 있습니다. 이럴 때는 `flash` 메서드를 사용하세요. 이 메서드로 저장된 데이터는 즉시 사용 가능하며, 다음 HTTP 요청 시까지 유지됩니다. 다음 요청 이후에는 플래시 데이터가 삭제됩니다. 플래시 데이터는 짧게 유지되어야 하는 상태 메시지에 주로 유용합니다:

```php
$request->session()->flash('status', '작업이 성공적으로 완료되었습니다!');
```

플래시 데이터를 여러 요청 간에 유지하고 싶으면 `reflash` 메서드를 사용할 수 있습니다. 특정 플래시 데이터만 유지하고 싶다면 `keep` 메서드를 사용하세요:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

플래시 데이터를 현재 요청에서만 유지하고 싶다면, `now` 메서드를 사용하세요:

```php
$request->session()->now('status', '작업이 성공적으로 완료되었습니다!');
```

<a name="deleting-data"></a>
### 데이터 삭제

`forget` 메서드는 세션에서 특정 데이터를 제거합니다. 모든 세션 데이터를 제거하고 싶다면 `flush` 메서드를 사용할 수 있습니다:

```php
// 단일 키 삭제...
$request->session()->forget('name');

// 여러 키 삭제...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성

세션 ID 재생성은 [세션 고정(Session Fixation)](https://owasp.org/www-community/attacks/Session_fixation) 공격을 방지하기 위해 종종 수행됩니다.

Laravel의 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)나 [Laravel Fortify](/docs/{{version}}/fortify)를 사용하는 경우, 인증 과정에서 세션 ID가 자동으로 재생성됩니다. 그러나 직접 세션 ID를 재생성해야 할 경우, `regenerate` 메서드를 사용할 수 있습니다:

```php
$request->session()->regenerate();
```

세션 ID를 재생성과 동시에 모든 세션 데이터를 제거하고 싶을 땐, `invalidate` 메서드를 사용할 수 있습니다:

```php
$request->session()->invalidate();
```

<a name="session-blocking"></a>
## 세션 블로킹

> [!WARNING]
> 세션 블로킹을 사용하려면 [원자적 락](/docs/{{version}}/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 `mongodb/laravel-mongodb` 패키지에 포함), `database`, `file`, `array` 드라이버가 지원됩니다. 또한, `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로, Laravel은 같은 세션을 사용하는 요청이 동시에 실행될 수 있도록 허용합니다. 예를 들어 자바스크립트 HTTP 라이브러리를 사용해 두 개의 요청을 동시에 보낼 경우, 두 요청 모두 동시에 처리됩니다. 대부분의 애플리케이션에서는 문제가 없지만, 서로 다른 엔드포인트에서 세션에 동시에 데이터를 쓰는 경우 세션 데이터 손실이 발생할 수도 있습니다.

이를 완화하기 위해, Laravel은 주어진 세션의 동시 요청을 제한하는 기능을 제공합니다. 시작하려면, 라우트 정의에서 `block` 메서드를 체이닝하면 됩니다. 다음 예제에서 `/profile` 엔드포인트로 들어오는 요청은 세션 락을 획득합니다. 락이 유지되는 동안 같은 세션 ID를 공유하는 `/profile`이나 `/order` 엔드포인트로 들어온 요청은 첫 번째 요청이 끝날 때까지 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

`block` 메서드는 두 개의 선택적 인자를 받을 수 있습니다. 첫 번째 인자는 세션 락이 해제되기 전까지 유지할 최대 초 단위 시간입니다. 요청이 그 전에 끝나면 락은 바로 해제됩니다.

두 번째 인자는 세션 락을 얻기 위해 요청이 대기할 최대 시간을 초 단위로 지정합니다. 주어진 시간 내 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다.

두 인자 모두 전달하지 않으면, 락은 최대 10초 동안 유지되며, 요청도 락을 얻기 위해 최대 10초 동안 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가

<a name="implementing-the-driver"></a>
### 드라이버 구현

기존 세션 드라이버가 애플리케이션 요구에 맞지 않는 경우, Laravel에서는 커스텀 세션 핸들러를 직접 작성할 수 있습니다. 커스텀 세션 드라이버는 PHP의 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스는 단 몇 개의 간단한 메서드로 이루어져 있습니다. 아래는 MongoDB에 대한 스터브 예시입니다:

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

Laravel은 확장 기능을 담아둘 기본 디렉토리를 제공하지 않으므로, 원하는 위치에 저장할 수 있습니다. 위 예시에서는 `Extensions` 디렉토리를 만들어 `MongoSessionHandler`를 저장했습니다.

각 메서드의 목적이 명확하지 않을 수 있으니, 아래에 역할을 정리합니다:

<div class="content-list" markdown="1">

- `open` 메서드는 주로 파일 기반 세션 저장소 시스템에서 사용됩니다. Laravel은 이미 `file` 기반 세션 드라이버를 제공하므로, 대부분의 경우 이 메서드를 비워둬도 됩니다.
- `close` 메서드도 `open`과 마찬가지로 대부분의 드라이버에서 필요하지 않습니다.
- `read` 메서드는 주어진 `$sessionId`에 해당하는 세션 데이터의 문자열 버전을 반환해야 합니다. Laravel이 자동으로 직렬화를 처리하므로 직접 직렬화/인코딩할 필요가 없습니다.
- `write` 메서드는 `$sessionId`에 해당하는 `$data` 문자열을 MongoDB나 원하는 저장소에 저장해야 합니다. 역시 직접 직렬화할 필요는 없습니다.
- `destroy` 메서드는 `$sessionId`에 해당하는 데이터를 저장소에서 삭제해야 합니다.
- `gc` 메서드는 주어진 `$lifetime`(UNIX 타임스탬프)보다 오래된 모든 세션 데이터를 제거해야 합니다. Memcached, Redis처럼 자체 만료 기능이 있는 시스템은 비워둬도 무방합니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록

드라이버 구현이 끝나면 이제 Laravel에 등록할 차례입니다. Laravel의 세션 백엔드에 추가 드라이버를 등록하려면 `Session` [파사드](/docs/{{version}}/facades)에서 제공하는 `extend` 메서드를 사용합니다. 이 호출은 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 수행해야 합니다. 기존의 `App\Providers\AppServiceProvider`나 새로운 프로바이더를 만들어 사용할 수 있습니다:

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
            // SessionHandlerInterface 구현체를 반환...
            return new MongoSessionHandler;
        });
    }
}
```

세션 드라이버가 등록되었다면, `SESSION_DRIVER` 환경 변수나 애플리케이션의 `config/session.php` 구성 파일에서 `mongo` 드라이버를 세션 드라이버로 지정할 수 있습니다.