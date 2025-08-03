# HTTP 세션 (HTTP Session)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 요구사항](#driver-prerequisites)
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

HTTP 기반 애플리케이션은 상태를 유지하지 않기 때문에, 세션은 여러 요청에 걸쳐 사용자에 대한 정보를 저장할 방법을 제공합니다. 사용자 정보는 일반적으로 후속 요청에서 접근할 수 있는 영속적인 저장소 또는 백엔드에 저장됩니다.

Laravel은 다양한 세션 백엔드를 제공하며, 이를 직관적이고 통합된 API를 통해 접근할 수 있습니다. Memcached, Redis, 데이터베이스와 같은 인기 있는 백엔드 지원도 포함되어 있습니다.

<a name="configuration"></a>
### 설정 (Configuration)

애플리케이션의 세션 설정 파일은 `config/session.php`에 저장되어 있습니다. 이 파일에 있는 옵션들을 반드시 확인하세요. 기본적으로 Laravel은 `file` 세션 드라이버를 사용하도록 설정되어 있으며, 이는 많은 애플리케이션에 적합합니다. 만약 여러 웹 서버에 워크로드가 분산되는 환경이라면, 모든 서버가 접근할 수 있는 중앙 저장소(예: Redis 또는 데이터베이스)를 선택해야 합니다.

세션 `driver` 설정 옵션은 각 요청에 대해 세션 데이터를 어디에 저장할지 정의합니다. Laravel은 기본으로 다음과 같은 훌륭한 드라이버들을 제공합니다:

<div class="content-list" markdown="1">

- `file` - 세션이 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션이 안전하게 암호화된 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 빠른 캐시 기반 저장소 중 하나에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며, 영속적으로 유지되지 않습니다.

</div>

> [!NOTE]  
> `array` 드라이버는 주로 [테스트](/docs/10.x/testing) 환경에서 사용되며, 세션에 저장된 데이터를 영속화하지 않습니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항 (Driver Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 세션 드라이버를 사용할 때는 세션 레코드를 담을 테이블을 만들어야 합니다. 예시 `Schema` 선언은 다음과 같습니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::create('sessions', function (Blueprint $table) {
    $table->string('id')->primary();
    $table->foreignId('user_id')->nullable()->index();
    $table->string('ip_address', 45)->nullable();
    $table->text('user_agent')->nullable();
    $table->text('payload');
    $table->integer('last_activity')->index();
});
```

`session:table` Artisan 명령어를 사용하여 이 마이그레이션을 생성할 수도 있습니다. 데이터베이스 마이그레이션에 대해 더 알고 싶다면 [마이그레이션 문서](/docs/10.x/migrations)를 참고하세요:

```shell
php artisan session:table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하기 위해서는 먼저 PECL을 통해 PhpRedis PHP 확장기능을 설치하거나, Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 구성에 관해서는 Laravel의 [Redis 문서](/docs/10.x/redis#configuration)를 참조하세요.

> [!NOTE]  
> `session` 설정 파일 내에서 `connection` 옵션을 사용하면 세션에 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기 (Interacting With the Session)

<a name="retrieving-data"></a>
### 데이터 가져오기 (Retrieving Data)

Laravel에서 세션 데이터를 다루는 주요 방법은 두 가지입니다: 전역 `session` 헬퍼와 `Request` 인스턴스를 사용하는 방법입니다. 우선, 라우트 클로저 혹은 컨트롤러 메서드에 타입힌트하여 `Request` 인스턴스를 통해 세션에 접근하는 방식을 보겠습니다. Laravel의 [서비스 컨테이너](/docs/10.x/container)에 의해 컨트롤러 메서드의 의존성은 자동으로 주입됩니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 지정된 사용자의 프로필을 보여줍니다.
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

세션에서 값을 가져올 때 `get` 메서드에 두 번째 인자로 기본값을 전달할 수 있습니다. 해당 키가 세션에 없으면 기본값이 반환됩니다. 기본값으로 Closure를 넘기면, 키가 없을 때 Closure가 실행되어 그 결과가 반환됩니다:

```
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 전역 세션 헬퍼 (The Global Session Helper)

전역 `session` PHP 함수를 사용해서도 세션 데이터를 가져오거나 저장할 수 있습니다. `session` 헬퍼를 하나의 문자열 인자로 호출하면 해당 키의 값을 반환합니다. 배열 형태로 호출하면 키와 값을 세션에 저장합니다:

```
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
> HTTP 요청 인스턴스를 통해 세션을 사용하는 것과 전역 `session` 헬퍼를 사용하는 것 사이에 실질적인 차이는 거의 없습니다. 두 방법 모두 테스트 시 `assertSessionHas` 메서드를 통해 [테스트 가능](/docs/10.x/testing)합니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 가져오기 (Retrieving All Session Data)

세션에 저장된 모든 데이터를 가져오려면 `all` 메서드를 사용할 수 있습니다:

```
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 세션 데이터 일부만 가져오기 (Retrieving a Portion of the Session Data)

`only`와 `except` 메서드를 사용하면 세션 데이터의 일부만 선택해서 가져올 수 있습니다:

```
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목이 존재하는지 확인하기 (Determining if an Item Exists in the Session)

항목이 세션에 존재하고 `null`이 아닌지 확인하려면 `has` 메서드를 사용하세요. `has`는 항목이 있고 값이 `null`이 아니면 `true`를 반환합니다:

```
if ($request->session()->has('users')) {
    // ...
}
```

값이 `null`이어도 단지 존재 여부만 확인하려면 `exists` 메서드를 사용합니다:

```
if ($request->session()->exists('users')) {
    // ...
}
```

항목이 없으면 확인하려면 `missing` 메서드를 사용합니다. 항목이 없으면 `true`를 반환합니다:

```
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### 데이터 저장하기 (Storing Data)

세션에 데이터를 저장할 때는 보통 요청 인스턴스의 `put` 메서드 또는 전역 `session` 헬퍼를 사용합니다:

```
// 요청 인스턴스 사용...
$request->session()->put('key', 'value');

// 전역 "session" 헬퍼 사용...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 형태 세션 값에 추가하기 (Pushing to Array Session Values)

`push` 메서드는 세션 값이 배열일 때 그 배열에 새 값을 추가할 때 사용합니다. 예를 들어 `user.teams` 키가 팀 이름 배열일 경우 다음과 같이 새 팀을 추가할 수 있습니다:

```
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 항목 가져오고 삭제하기 (Retrieving and Deleting an Item)

`pull` 메서드는 세션에서 값을 가져오면서 동시에 삭제합니다:

```
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가와 감소 (Incrementing and Decrementing Session Values)

세션에 저장된 정수 값을 증가시키거나 감소시킬 때는 `increment`, `decrement` 메서드를 사용할 수 있습니다:

```
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### 플래시 데이터 (Flash Data)

때로는 다음 요청까지 세션에 잠시 저장될 데이터를 저장하고 싶을 때가 있습니다. 이럴 때 `flash` 메서드를 사용하세요. 이렇게 저장된 플래시 데이터는 즉시 사용 가능하며 다음 HTTP 요청에서도 유지되지만, 그 이후 요청부터는 삭제됩니다. 플래시 데이터는 짧은 상태 메시지 전달에 주로 유용합니다:

```
$request->session()->flash('status', 'Task was successful!');
```

플래시 데이터를 여러 요청 동안 유지하려면 `reflash` 메서드를 사용하세요. 특정 플래시 데이터만 유지하려면 `keep` 메서드를 사용할 수 있습니다:

```
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

현재 요청에만 플래시 데이터를 유지하려면 `now` 메서드를 사용하세요:

```
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
### 데이터 삭제하기 (Deleting Data)

`forget` 메서드는 세션에서 특정 데이터를 삭제합니다. 모든 데이터를 삭제하고 싶으면 `flush` 메서드를 사용하세요:

```
// 단일 키 삭제...
$request->session()->forget('name');

// 여러 키 삭제...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성하기 (Regenerating the Session ID)

세션 ID를 재생성하는 것은 [세션 고정(session fixation)](https://owasp.org/www-community/attacks/Session_fixation) 공격을 막기 위해 자주 필요합니다.

Laravel은 [애플리케이션 스타터 킷](/docs/10.x/starter-kits) 또는 [Laravel Fortify](/docs/10.x/fortify)를 사용 시 인증 과정에서 자동으로 세션 ID를 재생성합니다. 직접 재생성이 필요하다면 `regenerate` 메서드를 사용하세요:

```
$request->session()->regenerate();
```

세션 ID 재생성과 동시에 세션 데이터를 모두 삭제하려면 `invalidate` 메서드를 사용하면 됩니다:

```
$request->session()->invalidate();
```

<a name="session-blocking"></a>
## 세션 블로킹 (Session Blocking)

> [!WARNING]  
> 세션 블로킹을 사용하려면, 애플리케이션이 [원자적 락(atomic locks)](/docs/10.x/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 이 조건을 충족하는 캐시 드라이버는 `memcached`, `dynamodb`, `redis`, `database`, `file`, `array` 입니다. 또한, `cookie` 세션 드라이버는 사용할 수 없습니다.

기본적으로 Laravel은 같은 세션을 사용하는 요청들이 동시에 실행되는 것을 허용합니다. 예를 들어 자바스크립트 HTTP 라이브러리로 애플리케이션에 두 개의 HTTP 요청을 보낼 경우 두 요청이 동시에 실행됩니다. 대부분의 애플리케이션에서는 문제가 되지 않지만, 서로 다른 두 엔드포인트가 동시에 세션에 데이터를 기록할 경우 세션 데이터가 손실될 수 있습니다.

이 문제를 완화하기 위해 Laravel은 특정 세션에 대한 동시 요청을 제한할 수 있는 기능을 제공합니다. 사용하려면 간단히 라우트 정의에 `block` 메서드를 연결하면 됩니다. 예를 들어, `/profile` 엔드포인트에 들어오는 요청은 세션 락을 획득합니다. 해당 락이 유지되는 동안 동일 세션 ID를 가진 `/profile` 혹은 `/order` 엔드포인트에 들어오는 요청들은 첫 요청이 완료될 때까지 대기합니다:

```
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10)

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10)
```

`block` 메서드는 두 개의 선택적 인자를 받습니다. 첫 번째 인자는 세션 락이 유지되는 최대 시간(초)이며, 요청이 그 전에 종료되면 락도 조기 해제됩니다.

두 번째 인자는 세션 락을 얻기 위해 요청이 대기하는 최대 시간(초)입니다. 이 시간 내에 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

이 인자들을 넘기지 않으면 기본값으로 락은 최대 10초간 유지되고, 요청은 최대 10초간 락 대기 상태가 됩니다:

```
Route::post('/profile', function () {
    // ...
})->block()
```

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가하기 (Adding Custom Session Drivers)

<a name="implementing-the-driver"></a>
### 드라이버 구현하기 (Implementing the Driver)

기존 세션 드라이버들이 애플리케이션 요구에 맞지 않는 경우, 직접 세션 핸들러를 작성할 수 있습니다. 커스텀 세션 드라이버는 PHP 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스는 몇 가지 기본 메서드만 포함합니다. MongoDB 예시 구현은 다음과 같습니다:

```
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

> [!NOTE]  
> Laravel은 확장 코드를 위한 전용 디렉토리를 제공하지 않습니다. 원하는 위치에 자유롭게 확장 코드를 배치할 수 있습니다. 이 예시에서는 `Extensions` 디렉토리를 만들어 `MongoSessionHandler`를 두었습니다.

각 메서드가 수행하는 역할을 간단히 살펴보겠습니다:

<div class="content-list" markdown="1">

- `open` 메서드는 주로 파일 기반 세션 저장 시스템에서 사용됩니다. Laravel은 기본적으로 `file` 드라이버를 제공하므로 보통 이 메서드는 비워둬도 무방합니다.
- `close` 메서드도 `open` 메서드처럼 대부분 드라이버에서 크게 사용할 필요가 없습니다.
- `read` 메서드는 주어진 `$sessionId`에 연결된 세션 데이터를 문자열 형태로 반환해야 합니다. 데이터 직렬화나 인코딩은 Laravel이 처리하므로 직접 할 필요가 없습니다.
- `write` 메서드는 `$sessionId`에 해당하는 `$data` 문자열을 MongoDB 등의 영속 저장소에 기록해야 합니다. 마찬가지로 직렬화는 Laravel이 처리합니다.
- `destroy` 메서드는 `$sessionId`와 연결된 데이터를 영속 저장소에서 제거해야 합니다.
- `gc` 메서드는 주어진 `$lifetime`(UNIX 타임스탬프)보다 오래된 모든 세션 데이터를 삭제해야 합니다. Memcached나 Redis처럼 자체 만료를 지원하는 저장소에서는 빈 메서드로 두어도 됩니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록하기 (Registering the Driver)

드라이버 구현이 완료되면 Laravel에 등록하면 됩니다. Laravel의 세션 백엔드에 추가 드라이버를 등록하려면 `Session` [파사드](/docs/10.x/facades)가 제공하는 `extend` 메서드를 사용하세요. 이 메서드는 [서비스 프로바이더](/docs/10.x/providers)의 `boot` 메서드 내에서 호출해야 합니다. 기존 `App\Providers\AppServiceProvider`를 사용해도 되고 새 프로바이더를 만들어도 됩니다:

```
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

세션 드라이버가 등록된 후에는 `config/session.php` 파일에서 `mongo` 드라이버를 사용할 수 있습니다.