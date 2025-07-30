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

HTTP 기반 애플리케이션은 상태 비저장(stateless)이기 때문에, 세션은 여러 요청에 걸쳐 사용자 정보를 저장하는 방법을 제공합니다. 이 사용자 정보는 보통 이후 요청에서도 접근할 수 있는 지속적인 저장소 또는 백엔드에 저장됩니다.

Laravel은 표현력이 풍부하고 통합된 API를 통해 접근할 수 있는 다양한 세션 백엔드를 제공합니다. 여기에는 [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스 같은 인기 있는 백엔드들이 포함되어 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

애플리케이션의 세션 설정 파일은 `config/session.php`에 저장되어 있습니다. 이 파일에서 제공되는 옵션을 반드시 검토하세요. 기본적으로 Laravel은 `database` 세션 드라이버를 사용하도록 구성되어 있습니다.

`driver` 설정 옵션은 각 요청에 대해 세션 데이터를 어디에 저장할지를 정의합니다. Laravel은 아래와 같은 다양한 드라이버를 포함합니다.

<div class="content-list" markdown="1">

- `file` - 세션 데이터가 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션 데이터가 안전하게 암호화된 쿠키에 저장됩니다.
- `database` - 세션 데이터가 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션 데이터가 이러한 빠른 캐시 기반 저장소 중 하나에 저장됩니다.
- `dynamodb` - 세션 데이터가 AWS DynamoDB에 저장됩니다.
- `array` - 세션 데이터가 PHP 배열에 저장되며, 영속적으로 저장되지 않습니다.

</div>

> [!NOTE]
> `array` 드라이버는 주로 [테스트](/docs/12.x/testing) 시 사용되며 세션에 저장된 데이터를 영속하지 않도록 합니다.

<a name="driver-prerequisites"></a>
### 드라이버 전제 조건 (Driver Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 경우, 세션 데이터를 담을 데이터베이스 테이블이 필요합니다. 보통 Laravel의 기본 `0001_01_01_000000_create_users_table.php` [마이그레이션](/docs/12.x/migrations)에 포함되어 있지만, 만약 `sessions` 테이블이 없을 경우, 다음 Artisan 명령어로 해당 마이그레이션을 생성할 수 있습니다:

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하려면 PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer로 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 설정에 관한 자세한 사항은 Laravel의 [Redis 문서](/docs/12.x/redis#configuration)를 참조하세요.

> [!NOTE]
> `SESSION_CONNECTION` 환경 변수 또는 `session.php` 설정 파일의 `connection` 옵션을 사용하여 세션 저장에 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기 (Interacting With the Session)

<a name="retrieving-data"></a>
### 데이터 가져오기 (Retrieving Data)

Laravel에서 세션 데이터를 다루는 기본적인 방법은 두 가지가 있습니다: 전역 `session` 헬퍼 함수와 `Request` 인스턴스를 통한 접근입니다. 먼저, 라우트 클로저(route closure)나 컨트롤러 메서드에서 타입힌트를 통해 주입받는 `Request` 인스턴스로 세션에 접근하는 법을 살펴보겠습니다. 컨트롤러 메서드의 의존성은 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자 프로필을 보여줍니다.
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

세션에서 항목을 가져올 때, `get` 메서드의 두 번째 인수로 기본값을 전달할 수 있습니다. 지정한 키가 세션에 없으면 이 기본값이 반환됩니다. 기본값으로 클로저(Closure)를 전달하면, 해당 키가 없을 때 클로저가 실행되고 이 결과가 반환됩니다:

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 전역 세션 헬퍼 (The Global Session Helper)

또한, 전역 `session` PHP 함수를 사용해 세션 데이터를 가져오거나 저장할 수 있습니다. `session` 헬퍼 함수에 문자열 하나를 전달하면 해당 키의 값을 반환하고, 배열 형태의 키/값 쌍을 전달하면 데이터를 세션에 저장합니다:

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
> HTTP 요청 인스턴스를 통한 세션 접근과 전역 `session` 헬퍼를 사용하는 것은 실무상 거의 차이가 없습니다. 두 방법 모두 모든 테스트 케이스에서 사용할 수 있는 `assertSessionHas` 메서드를 통해 [테스트 가능](/docs/12.x/testing)합니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 가져오기 (Retrieving All Session Data)

세션에 저장된 모든 데이터를 가져오려면 `all` 메서드를 사용하세요:

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 세션 데이터 일부 가져오기 (Retrieving a Portion of the Session Data)

`only` 메서드와 `except` 메서드는 세션 데이터의 일부를 선택적으로 가져올 때 사용합니다:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션 데이터 존재 여부 확인하기 (Determining if an Item Exists in the Session)

세션에 특정 항목이 존재하는지 확인하려면 `has` 메서드를 사용하세요. `has`는 해당 항목이 존재하고 값이 `null`이 아닌 경우 `true`를 반환합니다:

```php
if ($request->session()->has('users')) {
    // ...
}
```

만약 값이 `null`일지라도 세션에 항목이 존재하는지 확인하고 싶다면 `exists` 메서드를 사용합니다:

```php
if ($request->session()->exists('users')) {
    // ...
}
```

세션에 항목이 존재하지 않는지 확인하려면 `missing` 메서드를 사용하세요. 이 메서드는 해당 항목이 없으면 `true`를 반환합니다:

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### 데이터 저장하기 (Storing Data)

세션에 데이터를 저장할 때는 보통 요청 인스턴스의 `put` 메서드나 전역 `session` 헬퍼를 사용합니다:

```php
// 요청 인스턴스를 통해...
$request->session()->put('key', 'value');

// 전역 "session" 헬퍼를 통해...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 세션 값에 추가하기 (Pushing to Array Session Values)

`push` 메서드를 사용하면 배열 형태인 세션 값에 새 항목을 추가할 수 있습니다. 예를 들어, `user.teams` 키가 팀 이름 배열을 포함하는 경우 다음과 같이 새 팀을 추가할 수 있습니다:

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 항목 가져오고 삭제하기 (Retrieving and Deleting an Item)

`pull` 메서드는 세션에서 항목을 가져오면서 동시에 삭제할 때 사용합니다:

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증감하기 (Incrementing and Decrementing Session Values)

정수형 세션 값을 증가시키거나 감소시키려면 `increment` 및 `decrement` 메서드를 사용하세요:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### 플래시 데이터 (Flash Data)

때로는 다음 요청을 위해 세션에 단기적으로 데이터를 저장하고자 할 때가 있습니다. `flash` 메서드를 사용하면 이 목적을 달성할 수 있습니다. 플래시 데이터는 즉시 사용 가능하며 다음 HTTP 요청까지 유지되었다가 이후에는 삭제됩니다. 주로 상태 메시지와 같은 짧은 수명의 데이터에 유용합니다:

```php
$request->session()->flash('status', '작업이 성공적으로 완료되었습니다!');
```

플래시 데이터를 여러 요청에 걸쳐 유지하려면 `reflash` 메서드를 사용하세요. 특정 플래시 데이터만 유지하려면 `keep` 메서드를 사용할 수 있습니다:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

현재 요청에서만 플래시 데이터를 유지하려면 `now` 메서드를 사용하세요:

```php
$request->session()->now('status', '작업이 성공적으로 완료되었습니다!');
```

<a name="deleting-data"></a>
### 데이터 삭제하기 (Deleting Data)

`forget` 메서드는 세션에서 특정 데이터를 삭제합니다. 세션 내 모든 데이터를 삭제하고 싶으면 `flush` 메서드를 사용하세요:

```php
// 단일 키 삭제...
$request->session()->forget('name');

// 다중 키 삭제...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성하기 (Regenerating the Session ID)

세션 ID 재생성은 악의적인 사용자가 [세션 고정(Session Fixation)](https://owasp.org/www-community/attacks/Session_fixation) 공격을 활용하지 못하도록 막기 위해 주로 수행합니다.

Laravel은 Laravel [애플리케이션 스타터 키트](/docs/12.x/starter-kits) 또는 [Laravel Fortify](/docs/12.x/fortify)를 사용하는 경우 인증 과정에서 자동으로 세션 ID를 재생성합니다. 수동으로 세션 ID를 재생성하려면 `regenerate` 메서드를 사용하세요:

```php
$request->session()->regenerate();
```

세션 ID를 재생성하면서 세션 데이터도 모두 삭제하려면 `invalidate` 메서드를 사용합니다:

```php
$request->session()->invalidate();
```

<a name="session-blocking"></a>
## 세션 블로킹 (Session Blocking)

> [!WARNING]
> 세션 블로킹을 사용하려면 애플리케이션에서 [원자적 락(atomic locks)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원하는 캐시 드라이버는 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 `mongodb/laravel-mongodb` 패키지 포함), `database`, `file`, `array` 입니다. `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 Laravel은 같은 세션을 사용하는 요청이 동시에 실행되는 것을 허용합니다. 예를 들어, JavaScript HTTP 라이브러리로 애플리케이션에 두 개의 HTTP 요청을 보내면 두 요청이 병렬로 실행됩니다. 대부분의 애플리케이션에서는 문제가 없지만, 일부 특정 상황에서는 두 다른 엔드포인트에 동시에 요청하여 세션에 데이터를 쓸 때 세션 데이터 손실이 발생할 수 있습니다.

이런 문제를 해소하기 위해 Laravel은 특정 세션에 대한 동시 요청 제한 기능을 제공합니다. 사용 방법은 간단히 라우트 정의에 `block` 메서드를 연결하면 됩니다. 아래 예제에서 `/profile` 엔드포인트로 들어오는 요청은 세션 잠금(lock)을 획득합니다. 이 잠금이 유지되는 동안, 같은 세션 ID를 공유하는 `/profile` 또는 `/order` 엔드포인트로 들어오는 다른 요청들은 첫 요청이 끝날 때까지 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

`block` 메서드는 두 개의 선택 인수를 가집니다. 첫 번째 인수는 잠금이 해제되기 전까지 유지할 최대 시간(초)이고, 요청이 완료되면 잠금은 더 빨리 해제될 수 있습니다.

두 번째 인수는 요청이 잠금을 얻기 위해 대기할 최대 시간(초)입니다. 이 시간 안에 잠금을 받지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

두 인수를 모두 생략하면 잠금은 최대 10초간 유지되고, 요청은 잠금을 받기 위해 최대 10초간 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가하기 (Adding Custom Session Drivers)

<a name="implementing-the-driver"></a>
### 드라이버 구현하기 (Implementing the Driver)

기본 제공 세션 드라이버가 애플리케이션 요구에 맞지 않는 경우, 별도의 세션 핸들러를 구현할 수 있습니다. 커스텀 세션 드라이버는 PHP 내장 인터페이스인 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스에는 몇 가지 간단한 메서드가 정의되어 있습니다. 아래는 MongoDB 구현 예시 스텁입니다:

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

Laravel은 기본적으로 확장 모듈을 둔 디렉터리를 제공하지 않으니, 원하는 곳에 자유롭게 배치하면 됩니다. 위 예제에서는 `Extensions` 디렉터리를 만들어 `MongoSessionHandler`를 넣었습니다.

각 메서드의 역할에 대해 간단히 설명드립니다.

<div class="content-list" markdown="1">

- `open` 메서드는 보통 파일 기반 세션 저장소에서 사용합니다. Laravel이 기본 `file` 세션 드라이버를 제공하므로 이 메서드는 대부분 비워 둡니다.
- `close` 메서드 역시 `open`과 마찬가지로 보통 사용할 필요가 없습니다.
- `read` 메서드는 주어진 `$sessionId`에 연관된 세션 데이터를 문자열로 반환해야 합니다. 직렬화나 인코딩 처리는 하지 않아도 됩니다. Laravel이 처리합니다.
- `write` 메서드는 `$sessionId`와 관련된 `$data` 문자열을 MongoDB나 다른 영속 저장소에 기록해야 합니다. 직렬화는 하지 않아도 됩니다.
- `destroy` 메서드는 주어진 `$sessionId`에 해당하는 데이터를 영속 저장소에서 삭제합니다.
- `gc` 메서드는 `$lifetime` (UNIX 타임스탬프)보다 오래된 모든 세션 데이터를 삭제합니다. Memcached, Redis처럼 자체 만료 기능이 있는 시스템이라면 이 메서드는 비워 둘 수 있습니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록하기 (Registering the Driver)

드라이버 구현이 완료되었으면 Laravel에 등록할 준비가 된 것입니다. Laravel의 세션 백엔드에 드라이버를 추가하려면 `Session` [페이사드](/docs/12.x/facades)의 `extend` 메서드를 사용하세요. 이 메서드는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출하는 것이 일반적입니다. 기존 `App\Providers\AppServiceProvider`에 넣거나 새로운 프로바이더를 생성해도 됩니다:

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
            // SessionHandlerInterface 구현체 반환...
            return new MongoSessionHandler;
        });
    }
}
```

세션 드라이버를 등록한 뒤에는 `SESSION_DRIVER` 환경 변수나 `config/session.php` 구성 파일에서 `mongo` 드라이버를 지정하여 사용할 수 있습니다.