# HTTP 세션 (HTTP Session)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 요구 사항](#driver-prerequisites)
- [세션과 상호작용하기](#interacting-with-the-session)
    - [데이터 조회](#retrieving-data)
    - [데이터 저장](#storing-data)
    - [플래시 데이터](#flash-data)
    - [데이터 삭제](#deleting-data)
    - [세션 ID 재생성](#regenerating-the-session-id)
- [세션 블로킹](#session-blocking)
- [커스텀 세션 드라이버 추가하기](#adding-custom-session-drivers)
    - [드라이버 구현하기](#implementing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)

<a name="introduction"></a>
## 소개

HTTP 기반 애플리케이션은 상태를 유지하지 않기 때문에, 세션은 여러 요청에 걸쳐 사용자에 대한 정보를 저장하는 방법을 제공합니다. 이 사용자 정보는 일반적으로 후속 요청에서 접근할 수 있도록 영구 저장소나 백엔드에 저장됩니다.

Laravel은 다양한 세션 백엔드를 하나의 표현력 있는 통합 API로 접근할 수 있도록 제공합니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스와 같은 인기 있는 백엔드도 기본적으로 지원합니다.

<a name="configuration"></a>
### 설정

애플리케이션의 세션 설정 파일은 `config/session.php`에 위치합니다. 이 파일에 어떤 옵션들이 있는지 반드시 확인하세요. 기본적으로 Laravel은 `database` 세션 드라이버를 사용하도록 설정되어 있습니다.

세션 `driver` 설정 옵션은 각 요청의 세션 데이터가 어디에 저장될지를 정의합니다. Laravel은 여러 드라이버를 포함합니다:

<div class="content-list" markdown="1">

- `file` - 세션 데이터는 `storage/framework/sessions` 디렉터리에 저장됩니다.
- `cookie` - 세션 데이터는 보안이 강화된 암호화된 쿠키에 저장됩니다.
- `database` - 세션 데이터는 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션 데이터는 빠른 캐시 기반 저장소 중 하나에 저장됩니다.
- `dynamodb` - 세션 데이터는 AWS DynamoDB에 저장됩니다.
- `array` - 세션 데이터는 PHP 배열에 저장되며 지속되지 않습니다.

</div>

> [!NOTE]  
> `array` 드라이버는 주로 [테스트](/docs/11.x/testing) 중에 사용되며, 세션에 저장된 데이터가 영구 저장되지 않도록 합니다.

<a name="driver-prerequisites"></a>
### 드라이버 요구 사항

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 경우, 세션 데이터를 담을 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel 기본 [마이그레이션](/docs/11.x/migrations)에 `sessions` 테이블이 포함되어 있지만, 만약 없다면 `make:session-table` Artisan 명령어로 마이그레이션을 생성할 수 있습니다:

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하려면, PECL을 통해 PhpRedis PHP 확장 기능을 설치하거나 Composer로 `predis/predis` 패키지를 (~1.0) 설치해야 합니다. Redis 설정에 대한 자세한 내용은 Laravel의 [Redis 문서](/docs/11.x/redis#configuration)를 참고하세요.

> [!NOTE]  
> `SESSION_CONNECTION` 환경 변수 또는 `session.php` 설정 파일의 `connection` 옵션을 통해 어떤 Redis 연결로 세션 저장을 할지 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기

<a name="retrieving-data"></a>
### 데이터 조회

Laravel에서 세션 데이터를 다루는 주요 방법은 글로벌 `session` 헬퍼 함수와 `Request` 인스턴스를 사용하는 방법 두 가지입니다. 먼저, 라우트 클로저나 컨트롤러 메서드에서 타입힌트로 주입받을 수 있는 `Request` 인스턴스를 통한 접근법을 살펴보겠습니다. 컨트롤러 의존성은 Laravel [서비스 컨테이너](/docs/11.x/container)가 자동으로 주입합니다:

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

세션에서 항목을 가져올 때, `get` 메서드의 두 번째 인자로 기본값을 전달할 수 있습니다. 지정한 키가 세션에 없으면 이 기본값이 반환됩니다. 기본값으로 클로저를 전달하면 해당 키가 없을 때 클로저가 실행되고 그 결과가 반환됩니다:

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 글로벌 session 헬퍼 함수

세션의 데이터를 가져오거나 저장할 때 글로벌 PHP 함수 `session`도 사용할 수 있습니다. `session` 헬퍼가 단일 문자열 인자로 호출되면, 해당 세션 키의 값을 반환합니다. 배열 형태의 키/값 쌍을 인자로 전달하면 그 값들은 세션에 저장됩니다:

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
> HTTP 요청 인스턴스를 이용한 세션 접근과 글로벌 `session` 헬퍼를 이용하는 것은 실질적으로 큰 차이가 없습니다. 두 가지 방법 모두 모든 테스트 케이스에서 사용 가능한 `assertSessionHas` 메서드를 통해 [테스트](/docs/11.x/testing)할 수 있습니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 조회

세션에 저장된 모든 데이터를 가져오려면 `all` 메서드를 사용할 수 있습니다:

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 세션 데이터의 일부만 조회하기

`only`와 `except` 메서드를 이용해 세션 데이터 일부만 조회할 수 있습니다:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목이 존재하는지 확인하기

세션에 특정 항목이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. 이 메서드는 항목이 존재하고 `null`이 아닐 경우 `true`를 반환합니다:

```php
if ($request->session()->has('users')) {
    // ...
}
```

값이 `null`이라도 세션에 존재하는지 확인하려면 `exists` 메서드를 사용하세요:

```php
if ($request->session()->exists('users')) {
    // ...
}
```

항목이 세션에 존재하지 않는지 확인하려면 `missing` 메서드를 사용합니다. 존재하지 않을 경우 `true`가 반환됩니다:

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### 데이터 저장

세션에 데이터를 저장할 때는 보통 요청 인스턴스의 `put` 메서드나 글로벌 `session` 헬퍼를 사용합니다:

```php
// 요청 인스턴스를 이용하여...
$request->session()->put('key', 'value');

// 글로벌 "session" 헬퍼를 이용하여...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 세션 값에 값 추가하기

`push` 메서드는 배열 형태인 세션 값에 새 값을 추가할 때 사용합니다. 예를 들어 `user.teams` 키가 팀 이름을 담은 배열이라면 다음과 같이 새 값을 추가할 수 있습니다:

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 항목 조회 후 삭제하기

`pull` 메서드는 세션에서 값을 가져오면서 동시에 삭제하는 기능을 합니다:

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가 및 감소

세션 데이터가 정수일 경우 `increment` 및 `decrement` 메서드로 값을 증가시키거나 감소시킬 수 있습니다:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### 플래시 데이터

다음 요청까지 일시적으로만 세션에 저장할 항목이 있을 때 `flash` 메서드를 사용합니다. 이 방식으로 저장한 데이터는 즉시 사용할 수 있고 그 다음 HTTP 요청 시에도 유효하지만, 그 이후에는 자동으로 삭제됩니다. 플래시 데이터는 주로 단기 상태 메시지를 전달할 때 유용합니다:

```php
$request->session()->flash('status', 'Task was successful!');
```

플래시 데이터를 여러 요청 동안 유지하려면 `reflash` 메서드를 사용해 전체 플래시 데이터를 한 요청 더 유지하거나, 특정 플래시 데이터만 유지하려면 `keep` 메서드를 사용하세요:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

현재 요청 동안만 플래시 데이터를 유지하려면 `now` 메서드를 사용할 수 있습니다:

```php
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
### 데이터 삭제

`forget` 메서드는 세션에서 특정 데이터를 제거합니다. 모든 세션 데이터를 삭제하려면 `flush` 메서드를 사용하세요:

```php
// 단일 키 삭제...
$request->session()->forget('name');

// 여러 키 삭제...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성

세션 ID를 재생성하는 것은 보통 악의적인 사용자가 [세션 고정(session fixation)](https://owasp.org/www-community/attacks/Session_fixation) 공격을 수행하지 못하도록 방지하기 위해 수행됩니다.

Laravel은 Laravel [애플리케이션 스타터 키트](/docs/11.x/starter-kits)나 [Laravel Fortify](/docs/11.x/fortify)를 사용할 경우 인증 과정에서 자동으로 세션 ID를 재생성합니다. 수동으로 세션 ID를 재생성해야 하는 경우 `regenerate` 메서드를 사용하세요:

```php
$request->session()->regenerate();
```

세션 ID를 재생성하면서 세션 데이터를 모두 삭제하려면 `invalidate` 메서드를 한 번에 사용할 수 있습니다:

```php
$request->session()->invalidate();
```

<a name="session-blocking"></a>
## 세션 블로킹

> [!WARNING]  
> 세션 블로킹 기능을 사용하려면, 애플리케이션이 [원자적 락(atomic locks)](/docs/11.x/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 드라이버는 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 `mongodb/laravel-mongodb` 패키지에 포함), `database`, `file`, `array`입니다. 단, `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 Laravel은 같은 세션을 사용하는 요청들이 동시에 실행되는 것을 허용합니다. 예를 들어, 자바스크립트 HTTP 라이브러리를 사용해 두 개의 HTTP 요청을 앱에 동시에 보내면, 두 요청 모두 동시에 실행됩니다. 대부분 애플리케이션에서 문제 되지 않지만, 세션에 데이터를 동시에 쓰는 다중 엔드포인트 요청에서 세션 데이터 손실이 일어날 수 있습니다.

이를 방지하기 위해 Laravel은 같은 세션에 대해 동시 요청 수를 제한하는 기능을 제공합니다. 시작하려면 라우트 정의에 `block` 메서드를 체인으로 붙이세요. 아래 예시는 `/profile` 엔드포인트에 들어오는 요청이 세션 락을 획득하도록 합니다. 락이 유지되는 동안, 같은 세션 ID를 공유하는 `/profile` 또는 `/order` 엔드포인트로 들어오는 요청들은 첫 번째 요청이 완료될 때까지 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

`block` 메서드는 두 개의 선택적 인수를 받습니다. 첫 번째 인수는 락이 유지될 최대 시간(초)입니다. 물론 요청이 먼저 끝나면 락은 그 즉시 해제됩니다.

두 번째 인수는 락 획득 시도할 때 요청이 기다리는 최대 시간(초)이며, 이 기간 내에 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

두 인수를 모두 지정하지 않으면 락은 최대 10초간 유지되고, 요청은 락 획득을 위해 최대 10초간 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가하기

<a name="implementing-the-driver"></a>
### 드라이버 구현하기

기본 제공되는 세션 드라이버들이 애플리케이션 요구사항에 맞지 않는 경우, 자체 세션 핸들러를 만들 수 있습니다. 커스텀 세션 드라이버는 PHP 내장 `SessionHandlerInterface`를 구현해야 하며, 이 인터페이스는 몇 가지 간단한 메서드로 구성되어 있습니다. MongoDB용 스텁 구현 예시는 다음과 같습니다:

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

Laravel은 기본적으로 확장 클래스를 위한 디렉터리를 별도로 제공하지 않으므로, 원하는 곳 어디에나 두면 됩니다. 이 예시에서는 `Extensions` 디렉터리를 만들어 `MongoSessionHandler`를 배치했습니다.

각 메서드의 역할은 다음과 같습니다:

<div class="content-list" markdown="1">

- `open` 메서드는 주로 파일 기반 세션 저장소에서 사용됩니다. Laravel에는 기본 `file` 세션 드라이버가 포함되어 있으므로 거의 구현할 필요가 없으며 빈 상태로 두어도 무방합니다.
- `close` 메서드도 `open`과 마찬가지로 대부분의 드라이버에서는 특별한 처리가 필요하지 않습니다.
- `read` 메서드는 `$sessionId`와 연관된 세션 데이터를 문자열 형태로 반환해야 합니다. 세션 데이터의 직렬화는 Laravel이 자동으로 처리하므로 직접 구현할 필요 없습니다.
- `write` 메서드는 `$sessionId`에 연관된 `$data` 문자열을 MongoDB 등 원하는 영구 저장소에 기록해야 합니다. 이 역시 직렬화는 Laravel이 담당합니다.
- `destroy` 메서드는 `$sessionId`에 해당하는 세션 데이터를 영구 저장소에서 삭제해야 합니다.
- `gc` 메서드는 주어진 `$lifetime` (UNIX 타임스탬프) 이후 만료된 모든 세션 데이터를 삭제합니다. Memcached나 Redis처럼 자체 만료 기능이 있는 저장소라면 이 메서드는 비워둬도 됩니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록하기

드라이버 구현이 완료되면 Laravel에 등록할 차례입니다. Laravel의 세션 백엔드에 커스텀 드라이버를 추가하려면 `Session` [파사드](/docs/11.x/facades)가 제공하는 `extend` 메서드를 사용하세요. 이 메서드는 [서비스 프로바이더](/docs/11.x/providers)의 `boot` 메서드에서 호출하면 됩니다. 기존 `App\Providers\AppServiceProvider`에 추가하거나 별도의 프로바이더를 만들 수 있습니다:

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

세션 드라이버가 등록되면, `SESSION_DRIVER` 환경 변수나 `config/session.php` 설정 파일에서 `mongo` 드라이버를 지정하여 애플리케이션에서 사용할 수 있습니다.