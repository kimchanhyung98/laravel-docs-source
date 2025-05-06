# 파사드(Facades)

- [소개](#introduction)
- [파사드 사용 시점](#when-to-use-facades)
    - [파사드 vs. 의존성 주입](#facades-vs-dependency-injection)
    - [파사드 vs. 헬퍼 함수](#facades-vs-helper-functions)
- [파사드의 동작 원리](#how-facades-work)
- [실시간(Real-Time) 파사드](#real-time-facades)
- [파사드 클래스 참조](#facade-class-reference)

<a name="introduction"></a>
## 소개

Laravel 공식 문서 전체에서는 "파사드"를 통해 Laravel의 다양한 기능과 상호작용하는 코드 예시가 자주 등장합니다. 파사드는 애플리케이션의 [서비스 컨테이너](/docs/{{version}}/container)에 등록된 클래스를 "정적" 인터페이스로 접근할 수 있도록 해줍니다. Laravel은 거의 모든 주요 기능에 접근할 수 있는 다양한 파사드를 기본 제공하고 있습니다.

Laravel 파사드는 서비스 컨테이너의 기반 클래스에 대한 "정적 프록시" 역할을 하며, 전통적인 정적 메서드 방식에 비해 짧고, 표현력이 뛰어난 문법을 제공하면서도 더 나은 테스트 용이성과 유연성을 보장합니다. 만약 파사드가 정확히 어떻게 동작하는지 완전히 이해하지 못해도 괜찮습니다. 그냥 계속해서 Laravel을 배우면서 익숙해지면 됩니다.

Laravel의 모든 파사드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 따라서 아래와 같이 간단하게 파사드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel 공식 문서 전반에 걸쳐, 여러 예제들이 프레임워크 기능을 설명할 때 파사드를 활용하고 있습니다.

<a name="helper-functions"></a>
#### 헬퍼 함수

파사드 이외에도 Laravel은 다양한 글로벌 "헬퍼 함수"들을 제공합니다. 이 함수들은 일반적으로 자주 사용하는 Laravel 기능과 더욱 간편하게 상호작용할 수 있게 해줍니다. 자주 사용되는 헬퍼 함수로는 `view`, `response`, `url`, `config` 등이 있습니다. 각 헬퍼 함수는 해당 기능 문서에서 안내하고 있으며, 전체 목록은 [헬퍼 문서](/docs/{{version}}/helpers)에서 확인할 수 있습니다.

예를 들어, `Illuminate\Support\Facades\Response` 파사드를 사용하여 JSON 응답을 생성하는 대신, `response` 헬퍼 함수를 사용할 수 있습니다. 헬퍼 함수는 전역적으로 사용할 수 있으므로 클래스를 따로 import할 필요가 없습니다.

```php
use Illuminate\Support\Facades\Response;

Route::get('/users', function () {
    return Response::json([
        // ...
    ]);
});

Route::get('/users', function () {
    return response()->json([
        // ...
    ]);
});
```

<a name="when-to-use-facades"></a>
## 파사드 사용 시점

파사드는 많은 이점을 가지고 있습니다. 길고 복잡한 클래스 이름을 기억하거나 수동으로 주입/설정하지 않고도, 간결하고 기억하기 쉬운 문법으로 Laravel의 기능을 사용할 수 있게 합니다. 또한, PHP의 동적 메서드 사용 덕분에 테스트하기도 편리합니다.

하지만 파사드를 사용할 때 주의해야 할 사항도 있습니다. 파사드를 사용하면 너무 쉽게 기능을 사용할 수 있고 의존성 주입이 필요 없기 때문에, 한 클래스에서 여러 파사드를 남발하면서 클래스의 역할이 지나치게 커지는 "스코프 확장(scope creep)" 문제가 생길 수 있습니다. 의존성 주입을 쓰면 생성자에 여러 의존성이 시각적으로 드러나므로 클래스가 너무 커지고 있다는 경고를 받을 수 있습니다. 반면, 파사드를 쓸 때는 반드시 클래스가 너무 커지지 않도록 클래스의 책임 범위를 주의 깊게 관리해야 합니다. 클래스가 덩치가 커진다면, 여러 개의 작은 클래스로 분할하는 것을 고려하세요.

<a name="facades-vs-dependency-injection"></a>
### 파사드 vs. 의존성 주입

의존성 주입의 가장 큰 장점 중 하나는, 주입된 클래스의 구현을 쉽게 교체할 수 있다는 점입니다. 이는 테스트 시에, 주입된 클래스를 모킹(mock)하거나 스텁(stub)으로 대체해서 특정 메서드의 호출 여부 등을 검증할 수 있기에 유용합니다.

일반적으로 정적 클래스의 메서드는 모킹이나 스텁 처리가 어렵지만, 파사드는 동적 메서드를 통해 서비스 컨테이너에서 객체를 해결하므로, 의존성 주입과 동일한 방식으로 테스트가 가능합니다. 예를 들어, 아래와 같은 라우트가 있다고 가정해봅시다.

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel의 파사드 테스트 기능을 활용하면, `Cache::get` 메서드가 우리가 기대한 인자로 호출되었는지 다음과 같이 검증할 수 있습니다.

```php
use Illuminate\Support\Facades\Cache;

/**
 * 기본적인 기능 테스트 예시.
 */
public function test_basic_example(): void
{
    Cache::shouldReceive('get')
         ->with('key')
         ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a name="facades-vs-helper-functions"></a>
### 파사드 vs. 헬퍼 함수

파사드 외에도, Laravel에는 뷰 생성, 이벤트 발생, 작업 디스패치, HTTP 응답 전송 등 일반 작업을 수행할 수 있는 다양한 "헬퍼 함수"가 있습니다. 이들 헬퍼 함수 중 다수는 대응하는 파사드와 동일한 역할을 합니다. 예를 들어, 다음 두 코드는 완전히 같습니다.

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

파사드와 헬퍼 함수의 실질적인 차이는 없습니다. 헬퍼 함수를 사용하더라도, 파사드와 동일한 방식으로 테스트할 수 있습니다. 예를 들면 아래 라우트에서,

```php
Route::get('/cache', function () {
    return cache('key');
});
```

`cache` 헬퍼는 내부적으로 `Cache` 파사드를 구현하는 클래스의 `get` 메서드를 호출하게 됩니다. 따라서 헬퍼 함수를 사용해도, 다음과 같은 방식으로 해당 메서드가 기대한 인자로 호출됐는지 테스트할 수 있습니다.

```php
use Illuminate\Support\Facades\Cache;

/**
 * 기본적인 기능 테스트 예시.
 */
public function test_basic_example(): void
{
    Cache::shouldReceive('get')
         ->with('key')
         ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a name="how-facades-work"></a>
## 파사드의 동작 원리

Laravel 애플리케이션에서 파사드는 컨테이너에서 객체에 접근할 수 있도록 해주는 클래스입니다. 이 기능의 핵심은 `Facade` 클래스에 있습니다. Laravel의 모든 기본 파사드(그리고 여러분이 직접 만드는 커스텀 파사드)는 `Illuminate\Support\Facades\Facade` 기본 클래스를 확장(extend)합니다.

`Facade` 기본 클래스는 PHP의 매직 메서드 `__callStatic()`을 활용하여, 파사드로부터 발생한 호출을 서비스 컨테이너 내에서 객체를 가져온 후 그 객체로 전달합니다. 아래 예시에서, Laravel 캐시 시스템에 호출이 이루어집니다. 이 코드를 보면, 마치 `Cache` 클래스의 정적 메서드 `get`이 직접 호출되는 것처럼 보입니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Cache;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필 보여주기.
     */
    public function showProfile(string $id): View
    {
        $user = Cache::get('user:'.$id);

        return view('profile', ['user' => $user]);
    }
}
```

상단에서 `Cache` 파사드를 import한 것을 볼 수 있습니다. 이 파사드는 결국 `Illuminate\Contracts\Cache\Factory` 인터페이스 실체에 대한 프록시 역할을 합니다. 즉, 파사드로 실행하는 모든 호출은 실제로는 Laravel 캐시 서비스 인스턴스에 위임됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 들여다보면, 실제로는 정적 메서드 `get`이 정의되어 있지 않습니다.

```php
class Cache extends Facade
{
    /**
     * 해당 컴포넌트의 등록된 이름 가져오기.
     */
    protected static function getFacadeAccessor(): string
    {
        return 'cache';
    }
}
```

대신, `Cache` 파사드는 `Facade` 기본 클래스를 상속하고, `getFacadeAccessor()` 메서드를 정의합니다. 이 메서드는 서비스 컨테이너에서 바인딩된 서비스의 이름을 반환하는 역할을 합니다. 사용자가 `Cache` 파사드의 어떤 정적 메서드를 호출하면, Laravel은 [서비스 컨테이너](/docs/{{version}}/container)에서 `cache` 바인딩을 해결한 뒤, 해당 객체에 대해 요청한 메서드(여기서는 `get`)를 실행합니다.

<a name="real-time-facades"></a>
## 실시간(Real-Time) 파사드

실시간 파사드를 활용하면, 애플리케이션 내 어떤 클래스든 파사드처럼 사용할 수 있습니다. 어떻게 사용하는지 살펴보기 위해 먼저 실시간 파사드를 사용하지 않는 코드를 보겠습니다. 예를 들어, `Podcast` 모델에 `publish` 메서드가 있고, 팟캐스트를 발행하기 위해 `Publisher` 인스턴스를 주입해야 한다고 가정합시다.

```php
<?php

namespace App\Models;

use App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * 팟캐스트 발행.
     */
    public function publish(Publisher $publisher): void
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this);
    }
}
```

이렇게 구현하면, 테스트 시 `Publisher`를 모킹하여 메서드 동작을 쉽게 검증할 수 있지만, 매번 `publish` 메서드를 호출할 때마다 `Publisher` 인스턴스를 직접 전달해야 하는 번거로움이 있습니다. 실시간 파사드를 사용하면, 테스트 용이성을 그대로 유지하면서도 `Publisher` 인스턴스를 명시적으로 전달할 필요가 없습니다. 실시간 파사드를 생성하려면 import하는 클래스의 네임스페이스 앞에 `Facades`를 붙여주세요.

```php
<?php

namespace App\Models;

use App\Contracts\Publisher; // [tl! remove]
use Facades\App\Contracts\Publisher; // [tl! add]
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * 팟캐스트 발행.
     */
    public function publish(Publisher $publisher): void // [tl! remove]
    public function publish(): void // [tl! add]
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this); // [tl! remove]
        Publisher::publish($this); // [tl! add]
    }
}
```

실시간 파사드를 사용하면, 서비스 컨테이너에서 `Facades` 접두사 이후의 인터페이스 또는 클래스 이름을 이용해 구현체를 해결합니다. 테스트 시에는 Laravel의 내장 파사드 테스트 헬퍼를 활용해 메서드 호출을 모킹할 수 있습니다.

```php
<?php

namespace Tests\Feature;

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PodcastTest extends TestCase
{
    use RefreshDatabase;

    /**
     * 테스트 예시.
     */
    public function test_podcast_can_be_published(): void
    {
        $podcast = Podcast::factory()->create();

        Publisher::shouldReceive('publish')->once()->with($podcast);

        $podcast->publish();
    }
}
```

<a name="facade-class-reference"></a>
## 파사드 클래스 참조

아래 표에서는 모든 파사드와 대응하는 내부 클래스를 찾아볼 수 있습니다. 특정 파사드의 루트 클래스 API 문서를 빠르게 참조하고자 할 때 유용합니다. 또한, (해당하는 경우) [서비스 컨테이너 바인딩](/docs/{{version}}/container) 키도 함께 기재되어 있습니다.

<div class="overflow-auto">

파사드  |  클래스  |  서비스 컨테이너 바인딩
------------- | ------------- | -------------
App  |  [Illuminate\Foundation\Application](https://laravel.com/api/{{version}}/Illuminate/Foundation/Application.html)  |  `app`
Artisan  |  [Illuminate\Contracts\Console\Kernel](https://laravel.com/api/{{version}}/Illuminate/Contracts/Console/Kernel.html)  |  `artisan`
Auth  |  [Illuminate\Auth\AuthManager](https://laravel.com/api/{{version}}/Illuminate/Auth/AuthManager.html)  |  `auth`
Auth (인스턴스)  |  [Illuminate\Contracts\Auth\Guard](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Guard.html)  |  `auth.driver`
Blade  |  [Illuminate\View\Compilers\BladeCompiler](https://laravel.com/api/{{version}}/Illuminate/View/Compilers/BladeCompiler.html)  |  `blade.compiler`
Broadcast  |  [Illuminate\Contracts\Broadcasting\Factory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Broadcasting/Factory.html)  |  &nbsp;
Broadcast (인스턴스)  |  [Illuminate\Contracts\Broadcasting\Broadcaster](https://laravel.com/api/{{version}}/Illuminate/Contracts/Broadcasting/Broadcaster.html)  |  &nbsp;
Bus  |  [Illuminate\Contracts\Bus\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html)  |  &nbsp;
Cache  |  [Illuminate\Cache\CacheManager](https://laravel.com/api/{{version}}/Illuminate/Cache/CacheManager.html)  |  `cache`
Cache (인스턴스)  |  [Illuminate\Cache\Repository](https://laravel.com/api/{{version}}/Illuminate/Cache/Repository.html)  |  `cache.store`
Config  |  [Illuminate\Config\Repository](https://laravel.com/api/{{version}}/Illuminate/Config/Repository.html)  |  `config`
Cookie  |  [Illuminate\Cookie\CookieJar](https://laravel.com/api/{{version}}/Illuminate/Cookie/CookieJar.html)  |  `cookie`
Crypt  |  [Illuminate\Encryption\Encrypter](https://laravel.com/api/{{version}}/Illuminate/Encryption/Encrypter.html)  |  `encrypter`
Date  |  [Illuminate\Support\DateFactory](https://laravel.com/api/{{version}}/Illuminate/Support/DateFactory.html)  |  `date`
DB  |  [Illuminate\Database\DatabaseManager](https://laravel.com/api/{{version}}/Illuminate/Database/DatabaseManager.html)  |  `db`
DB (인스턴스)  |  [Illuminate\Database\Connection](https://laravel.com/api/{{version}}/Illuminate/Database/Connection.html)  |  `db.connection`
Event  |  [Illuminate\Events\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Events/Dispatcher.html)  |  `events`
File  |  [Illuminate\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Filesystem/Filesystem.html)  |  `files`
Gate  |  [Illuminate\Contracts\Auth\Access\Gate](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Access/Gate.html)  |  &nbsp;
Hash  |  [Illuminate\Contracts\Hashing\Hasher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Hashing/Hasher.html)  |  `hash`
Http  |  [Illuminate\Http\Client\Factory](https://laravel.com/api/{{version}}/Illuminate/Http/Client/Factory.html)  |  &nbsp;
Lang  |  [Illuminate\Translation\Translator](https://laravel.com/api/{{version}}/Illuminate/Translation/Translator.html)  |  `translator`
Log  |  [Illuminate\Log\LogManager](https://laravel.com/api/{{version}}/Illuminate/Log/LogManager.html)  |  `log`
Mail  |  [Illuminate\Mail\Mailer](https://laravel.com/api/{{version}}/Illuminate/Mail/Mailer.html)  |  `mailer`
Notification  |  [Illuminate\Notifications\ChannelManager](https://laravel.com/api/{{version}}/Illuminate/Notifications/ChannelManager.html)  |  &nbsp;
Password  |  [Illuminate\Auth\Passwords\PasswordBrokerManager](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBrokerManager.html)  |  `auth.password`
Password (인스턴스)  |  [Illuminate\Auth\Passwords\PasswordBroker](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBroker.html)  |  `auth.password.broker`
Pipeline (인스턴스)  |  [Illuminate\Pipeline\Pipeline](https://laravel.com/api/{{version}}/Illuminate/Pipeline/Pipeline.html)  |  &nbsp;
Process  |  [Illuminate\Process\Factory](https://laravel.com/api/{{version}}/Illuminate/Process/Factory.html)  |  &nbsp;
Queue  |  [Illuminate\Queue\QueueManager](https://laravel.com/api/{{version}}/Illuminate/Queue/QueueManager.html)  |  `queue`
Queue (인스턴스)  |  [Illuminate\Contracts\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Contracts/Queue/Queue.html)  |  `queue.connection`
Queue (기본 클래스)  |  [Illuminate\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Queue/Queue.html)  |  &nbsp;
RateLimiter  |  [Illuminate\Cache\RateLimiter](https://laravel.com/api/{{version}}/Illuminate/Cache/RateLimiter.html)  |  &nbsp;
Redirect  |  [Illuminate\Routing\Redirector](https://laravel.com/api/{{version}}/Illuminate/Routing/Redirector.html)  |  `redirect`
Redis  |  [Illuminate\Redis\RedisManager](https://laravel.com/api/{{version}}/Illuminate/Redis/RedisManager.html)  |  `redis`
Redis (인스턴스)  |  [Illuminate\Redis\Connections\Connection](https://laravel.com/api/{{version}}/Illuminate/Redis/Connections/Connection.html)  |  `redis.connection`
Request  |  [Illuminate\Http\Request](https://laravel.com/api/{{version}}/Illuminate/Http/Request.html)  |  `request`
Response  |  [Illuminate\Contracts\Routing\ResponseFactory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html)  |  &nbsp;
Response (인스턴스)  |  [Illuminate\Http\Response](https://laravel.com/api/{{version}}/Illuminate/Http/Response.html)  |  &nbsp;
Route  |  [Illuminate\Routing\Router](https://laravel.com/api/{{version}}/Illuminate/Routing/Router.html)  |  `router`
Schema  |  [Illuminate\Database\Schema\Builder](https://laravel.com/api/{{version}}/Illuminate/Database/Schema/Builder.html)  |  &nbsp;
Session  |  [Illuminate\Session\SessionManager](https://laravel.com/api/{{version}}/Illuminate/Session/SessionManager.html)  |  `session`
Session (인스턴스)  |  [Illuminate\Session\Store](https://laravel.com/api/{{version}}/Illuminate/Session/Store.html)  |  `session.store`
Storage  |  [Illuminate\Filesystem\FilesystemManager](https://laravel.com/api/{{version}}/Illuminate/Filesystem/FilesystemManager.html)  |  `filesystem`
Storage (인스턴스)  |  [Illuminate\Contracts\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Contracts/Filesystem/Filesystem.html)  |  `filesystem.disk`
URL  |  [Illuminate\Routing\UrlGenerator](https://laravel.com/api/{{version}}/Illuminate/Routing/UrlGenerator.html)  |  `url`
Validator  |  [Illuminate\Validation\Factory](https://laravel.com/api/{{version}}/Illuminate/Validation/Factory.html)  |  `validator`
Validator (인스턴스)  |  [Illuminate\Validation\Validator](https://laravel.com/api/{{version}}/Illuminate/Validation/Validator.html)  |  &nbsp;
View  |  [Illuminate\View\Factory](https://laravel.com/api/{{version}}/Illuminate/View/Factory.html)  |  `view`
View (인스턴스)  |  [Illuminate\View\View](https://laravel.com/api/{{version}}/Illuminate/View/View.html)  |  &nbsp;
Vite  |  [Illuminate\Foundation\Vite](https://laravel.com/api/{{version}}/Illuminate/Foundation/Vite.html)  |  &nbsp;

</div>
