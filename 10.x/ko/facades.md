# 파사드 (Facades)

- [소개](#introduction)
- [파사드를 언제 사용할까](#when-to-use-facades)
    - [파사드와 의존성 주입 비교](#facades-vs-dependency-injection)
    - [파사드와 헬퍼 함수 비교](#facades-vs-helper-functions)
- [파사드는 어떻게 동작하는가](#how-facades-work)
- [실시간 파사드 (Real-Time Facades)](#real-time-facades)
- [파사드 클래스 참고 자료](#facade-class-reference)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 문서 전반에서, "파사드"를 통해 Laravel의 여러 기능과 상호작용하는 코드 예제를 자주 볼 수 있습니다. 파사드는 애플리케이션의 [서비스 컨테이너](/docs/10.x/container)에서 제공하는 클래스에 대해 "정적(static)" 인터페이스를 제공합니다. Laravel은 거의 모든 기능에 접근할 수 있도록 다양한 파사드를 기본 제공하고 있습니다.

Laravel 파사드는 서비스 컨테이너 내부의 클래스들을 "정적 프록시(static proxies)" 형태로 감싸며, 간결하고 표현력이 풍부한 문법을 제공하면서도, 전통적인 정적 메서드보다 테스트 용이성과 유연성을 더 높여줍니다. 파사드가 어떻게 작동하는지 완전히 이해하지 못해도 괜찮으니, 일단은 넘어가면서 Laravel 학습을 이어가시면 됩니다.

모든 Laravel 파사드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 따라서 파사드를 이렇게 간단히 사용할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel 문서 내에서 다양한 기능을 시연할 때 많은 예제는 파사드를 활용합니다.

<a name="helper-functions"></a>
#### 헬퍼 함수 (Helper Functions)

파사드를 보완하기 위해, Laravel은 전역에서 쉽게 사용할 수 있는 여러 "헬퍼 함수"를 제공합니다. 이 함수들은 Laravel의 자주 쓰이는 기능을 더욱 편리하게 사용할 수 있게 합니다. 대표적인 헬퍼 함수로는 `view`, `response`, `url`, `config` 등이 있습니다. 각 헬퍼 함수는 관련 기능 문서에 함께 설명되어 있지만, 전체 목록은 별도의 [헬퍼 문서](/docs/10.x/helpers)에서 확인할 수 있습니다.

예를 들어, `Illuminate\Support\Facades\Response` 파사드를 이용해 JSON 응답을 생성하는 대신, `response` 헬퍼 함수만 사용해도 됩니다. 헬퍼 함수는 전역적으로 사용 가능하므로 별도의 클래스를 import하지 않아도 됩니다:

```
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
## 파사드를 언제 사용할까 (When to Utilize Facades)

파사드는 여러 장점이 있습니다. 복잡한 클래스 이름을 주입하거나 수동으로 구성할 필요 없이, Laravel 기능을 간결하고 기억하기 쉬운 문법으로 사용할 수 있기 때문입니다. 또한 PHP의 동적 메서드를 활용하는 독특한 방식 덕분에 테스트하기도 쉽습니다.

하지만 파사드를 사용할 때 주의해야 할 점도 있습니다. 가장 큰 위험은 클래스가 너무 많은 파사드를 사용하며 책임 범위가 커지는 "클래스 스코프 확장"입니다. 파사드는 사용이 간편하고 의존성 주입이 필요 없기 때문에, 한 클래스에서 너무 많은 파사드를 사용하는 상황이 쉽게 발생할 수 있습니다. 의존성 주입에서는 생성자에 나열된 의존성 수를 보고 클래스를 분할할 필요가 있는지 시각적으로 확인할 수 있지만, 파사드는 이런 경고 신호가 없습니다. 따라서 파사드 사용할 때는 클래스 크기를 잘 살펴서 책임 범위가 너무 넓어지지 않도록 주의하세요. 만약 클래스가 너무 커진다면 여러 작은 클래스로 분리하는 것을 고려하세요.

<a name="facades-vs-dependency-injection"></a>
### 파사드와 의존성 주입 비교 (Facades vs. Dependency Injection)

의존성 주입의 주요 장점 중 하나는 주입된 클래스의 구현체를 교체할 수 있다는 점입니다. 이는 테스트 시 가짜(mock) 객체나 스텁(stub)을 주입하여 특정 메서드 호출 여부를 검증할 수 있어 매우 유용합니다.

일반적으로 정적(static) 메서드는 직접 가짜(mock)나 스텁으로 바꾸기 어렵습니다. 그러나 파사드는 동적 메서드를 이용해 서비스 컨테이너에서 객체를 찾아 메서드 호출을 위임하기 때문에, 마치 의존성 주입된 객체처럼 테스트할 수 있습니다. 예를 들어, 다음 경로(route)를 보겠습니다:

```
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel 파사드 테스트 기능을 활용해 `Cache::get` 메서드가 전달한 인수와 함께 호출되었는지 검증하는 테스트는 이렇게 작성할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;

/**
 * 기본 기능 테스트 예제
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
### 파사드와 헬퍼 함수 비교 (Facades vs. Helper Functions)

파사드 이외에도 Laravel은 여러 "헬퍼" 함수를 제공합니다. 헬퍼 함수는 뷰 생성, 이벤트 실행, 작업(job) 디스패치, HTTP 응답 발송 등 일반적인 작업을 수행할 수 있습니다. 이 중 많은 헬퍼 함수는 대응하는 파사드 기능과 동일합니다. 예를 들어, 아래 두 코드는 같은 결과를 만듭니다:

```
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

파사드와 헬퍼 함수는 실질적으로 차이가 없습니다. 헬퍼 함수를 사용할 때도 해당 파사드를 테스트하듯 동일하게 테스트할 수 있습니다. 예를 들어, 다음 경로 코드를 봅시다:

```
Route::get('/cache', function () {
    return cache('key');
});
```

`cache` 헬퍼 함수는 내부적으로 `Cache` 파사드가 근본적으로 호출하는 클래스의 `get` 메서드를 호출합니다. 따라서 헬퍼 함수를 사용해도 다음과 같이 메서드가 인수와 함께 호출됐는지 검증하는 테스트를 작성할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;

/**
 * 기본 기능 테스트 예제
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
## 파사드는 어떻게 동작하는가 (How Facades Work)

Laravel 애플리케이션에서 파사드는 서비스 컨테이너에서 객체를 꺼내 접근할 수 있게 해주는 클래스입니다. 이 동작의 핵심은 `Facade` 클래스에 있습니다. Laravel의 내장 파사드와 사용자가 직접 만든 커스텀 파사드는 모두 기본 `Illuminate\Support\Facades\Facade` 클래스를 상속합니다.

`Facade` 기본 클래스는 `__callStatic()` 매직 메서드를 활용하여, 파사드에서 발생하는 정적 메서드 호출을 서비스 컨테이너에서 꺼낸 객체에 위임합니다. 아래 예제를 보면, Laravel 캐시 시스템에 호출하는 코드가 있습니다. 이 코드를 보면 마치 `Cache` 클래스의 정적 메서드 `get`을 직접 호출하는 듯 보이지만:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Cache;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 보여줍니다.
     */
    public function showProfile(string $id): View
    {
        $user = Cache::get('user:'.$id);

        return view('profile', ['user' => $user]);
    }
}
```

위 파일 상단에서 `Cache` 파사드를 "import"하고 있음을 알 수 있습니다. 이 파사드는 `Illuminate\Contracts\Cache\Factory` 인터페이스의 실제 구현체에 접근하기 위한 프록시 역할을 합니다. 파사드를 통해 이루어지는 모든 메서드 호출은 Laravel 캐시 서비스의 실제 인스턴스에 전달됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 살펴보면, `get`이라는 정적 메서드는 정의되어 있지 않습니다:

```
class Cache extends Facade
{
    /**
     * 컴포넌트의 등록 이름을 반환합니다.
     */
    protected static function getFacadeAccessor(): string
    {
        return 'cache';
    }
}
```

`Cache` 파사드는 기본 `Facade` 클래스를 확장하며, `getFacadeAccessor()` 메서드를 정의하는데, 이 메서드는 서비스 컨테이너 내 바인딩 이름을 반환하는 역할을 합니다. 사용자가 `Cache` 파사드의 임의의 정적 메서드를 호출하면, Laravel은 컨테이너에서 `cache` 바인딩을 해석해 해당 객체에서 요청한 메서드(여기서는 `get`)를 실행합니다.

<a name="real-time-facades"></a>
## 실시간 파사드 (Real-Time Facades)

실시간 파사드를 이용하면, 애플리케이션 내 어떤 클래스든 파사드처럼 사용할 수 있습니다. 이를 설명하기 위해, 먼저 실시간 파사드를 쓰지 않은 코드를 봅시다. 예를 들어 `Podcast` 모델에 `publish` 메서드가 있다고 합시다. 그런데 팟캐스트를 발행하려면 `Publisher` 인스턴스를 주입 받아야 합니다:

```
<?php

namespace App\Models;

use App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * 팟캐스트를 발행합니다.
     */
    public function publish(Publisher $publisher): void
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this);
    }
}
```

이렇게 메서드에 `Publisher` 구현체를 주입하면 모킹(mocking)이 쉬워 메서드를 독립적으로 테스트할 수 있습니다. 하지만 `publish`를 호출할 때마다 꼭 `Publisher` 인스턴스를 넘겨야 하는 불편함이 있죠. 실시간 파사드를 사용하면 같은 테스트 용이성을 유지하면서도 `Publisher` 인스턴스를 명시적으로 전달할 필요가 없습니다. 실시간 파사드를 만들려면 기존 클래스 import 시 네임스페이스 앞에 `Facades`를 붙이면 됩니다:

```
<?php

namespace App\Models;

use App\Contracts\Publisher; // [tl! remove]
use Facades\App\Contracts\Publisher; // [tl! add]
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * 팟캐스트를 발행합니다.
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

실시간 파사드가 사용되면, `Facades` 접두어 뒤에 나오는 인터페이스 또는 클래스 이름을 기준으로 서비스 컨테이너에서 구현체가 해석됩니다. 테스트 시에는 Laravel 내장 파사드 테스트 도구를 사용해 아래처럼 해당 메서드 호출을 모킹할 수 있습니다:

```
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
     * 테스트 예제
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
## 파사드 클래스 참고 자료 (Facade Class Reference)

아래는 각 파사드와 연관된 실제 클래스입니다. 특정 파사드 루트의 API 문서로 빠르게 이동할 때 유용합니다. 가능한 경우 [서비스 컨테이너 바인딩](/docs/10.x/container) 키도 같이 포함되어 있습니다.

<div class="overflow-auto">

Facade  |  Class  |  Service Container Binding
------------- | ------------- | -------------
App  |  [Illuminate\Foundation\Application](https://laravel.com/api/10.x/Illuminate/Foundation/Application.html)  |  `app`
Artisan  |  [Illuminate\Contracts\Console\Kernel](https://laravel.com/api/10.x/Illuminate/Contracts/Console/Kernel.html)  |  `artisan`
Auth  |  [Illuminate\Auth\AuthManager](https://laravel.com/api/10.x/Illuminate/Auth/AuthManager.html)  |  `auth`
Auth (Instance)  |  [Illuminate\Contracts\Auth\Guard](https://laravel.com/api/10.x/Illuminate/Contracts/Auth/Guard.html)  |  `auth.driver`
Blade  |  [Illuminate\View\Compilers\BladeCompiler](https://laravel.com/api/10.x/Illuminate/View/Compilers/BladeCompiler.html)  |  `blade.compiler`
Broadcast  |  [Illuminate\Contracts\Broadcasting\Factory](https://laravel.com/api/10.x/Illuminate/Contracts/Broadcasting/Factory.html)  |  &nbsp;
Broadcast (Instance)  |  [Illuminate\Contracts\Broadcasting\Broadcaster](https://laravel.com/api/10.x/Illuminate/Contracts/Broadcasting/Broadcaster.html)  |  &nbsp;
Bus  |  [Illuminate\Contracts\Bus\Dispatcher](https://laravel.com/api/10.x/Illuminate/Contracts/Bus/Dispatcher.html)  |  &nbsp;
Cache  |  [Illuminate\Cache\CacheManager](https://laravel.com/api/10.x/Illuminate/Cache/CacheManager.html)  |  `cache`
Cache (Instance)  |  [Illuminate\Cache\Repository](https://laravel.com/api/10.x/Illuminate/Cache/Repository.html)  |  `cache.store`
Config  |  [Illuminate\Config\Repository](https://laravel.com/api/10.x/Illuminate/Config/Repository.html)  |  `config`
Cookie  |  [Illuminate\Cookie\CookieJar](https://laravel.com/api/10.x/Illuminate/Cookie/CookieJar.html)  |  `cookie`
Crypt  |  [Illuminate\Encryption\Encrypter](https://laravel.com/api/10.x/Illuminate/Encryption/Encrypter.html)  |  `encrypter`
Date  |  [Illuminate\Support\DateFactory](https://laravel.com/api/10.x/Illuminate/Support/DateFactory.html)  |  `date`
DB  |  [Illuminate\Database\DatabaseManager](https://laravel.com/api/10.x/Illuminate/Database/DatabaseManager.html)  |  `db`
DB (Instance)  |  [Illuminate\Database\Connection](https://laravel.com/api/10.x/Illuminate/Database/Connection.html)  |  `db.connection`
Event  |  [Illuminate\Events\Dispatcher](https://laravel.com/api/10.x/Illuminate/Events/Dispatcher.html)  |  `events`
File  |  [Illuminate\Filesystem\Filesystem](https://laravel.com/api/10.x/Illuminate/Filesystem/Filesystem.html)  |  `files`
Gate  |  [Illuminate\Contracts\Auth\Access\Gate](https://laravel.com/api/10.x/Illuminate/Contracts/Auth/Access/Gate.html)  |  &nbsp;
Hash  |  [Illuminate\Contracts\Hashing\Hasher](https://laravel.com/api/10.x/Illuminate/Contracts/Hashing/Hasher.html)  |  `hash`
Http  |  [Illuminate\Http\Client\Factory](https://laravel.com/api/10.x/Illuminate/Http/Client/Factory.html)  |  &nbsp;
Lang  |  [Illuminate\Translation\Translator](https://laravel.com/api/10.x/Illuminate/Translation/Translator.html)  |  `translator`
Log  |  [Illuminate\Log\LogManager](https://laravel.com/api/10.x/Illuminate/Log/LogManager.html)  |  `log`
Mail  |  [Illuminate\Mail\Mailer](https://laravel.com/api/10.x/Illuminate/Mail/Mailer.html)  |  `mailer`
Notification  |  [Illuminate\Notifications\ChannelManager](https://laravel.com/api/10.x/Illuminate/Notifications/ChannelManager.html)  |  &nbsp;
Password  |  [Illuminate\Auth\Passwords\PasswordBrokerManager](https://laravel.com/api/10.x/Illuminate/Auth/Passwords/PasswordBrokerManager.html)  |  `auth.password`
Password (Instance)  |  [Illuminate\Auth\Passwords\PasswordBroker](https://laravel.com/api/10.x/Illuminate/Auth/Passwords/PasswordBroker.html)  |  `auth.password.broker`
Pipeline (Instance)  |  [Illuminate\Pipeline\Pipeline](https://laravel.com/api/10.x/Illuminate/Pipeline/Pipeline.html)  |  &nbsp;
Process  |  [Illuminate\Process\Factory](https://laravel.com/api/10.x/Illuminate/Process/Factory.html)  |  &nbsp;
Queue  |  [Illuminate\Queue\QueueManager](https://laravel.com/api/10.x/Illuminate/Queue/QueueManager.html)  |  `queue`
Queue (Instance)  |  [Illuminate\Contracts\Queue\Queue](https://laravel.com/api/10.x/Illuminate/Contracts/Queue/Queue.html)  |  `queue.connection`
Queue (Base Class)  |  [Illuminate\Queue\Queue](https://laravel.com/api/10.x/Illuminate/Queue/Queue.html)  |  &nbsp;
RateLimiter  |  [Illuminate\Cache\RateLimiter](https://laravel.com/api/10.x/Illuminate/Cache/RateLimiter.html)  |  &nbsp;
Redirect  |  [Illuminate\Routing\Redirector](https://laravel.com/api/10.x/Illuminate/Routing/Redirector.html)  |  `redirect`
Redis  |  [Illuminate\Redis\RedisManager](https://laravel.com/api/10.x/Illuminate/Redis/RedisManager.html)  |  `redis`
Redis (Instance)  |  [Illuminate\Redis\Connections\Connection](https://laravel.com/api/10.x/Illuminate/Redis/Connections/Connection.html)  |  `redis.connection`
Request  |  [Illuminate\Http\Request](https://laravel.com/api/10.x/Illuminate/Http/Request.html)  |  `request`
Response  |  [Illuminate\Contracts\Routing\ResponseFactory](https://laravel.com/api/10.x/Illuminate/Contracts/Routing/ResponseFactory.html)  |  &nbsp;
Response (Instance)  |  [Illuminate\Http\Response](https://laravel.com/api/10.x/Illuminate/Http/Response.html)  |  &nbsp;
Route  |  [Illuminate\Routing\Router](https://laravel.com/api/10.x/Illuminate/Routing/Router.html)  |  `router`
Schema  |  [Illuminate\Database\Schema\Builder](https://laravel.com/api/10.x/Illuminate/Database/Schema/Builder.html)  |  &nbsp;
Session  |  [Illuminate\Session\SessionManager](https://laravel.com/api/10.x/Illuminate/Session/SessionManager.html)  |  `session`
Session (Instance)  |  [Illuminate\Session\Store](https://laravel.com/api/10.x/Illuminate/Session/Store.html)  |  `session.store`
Storage  |  [Illuminate\Filesystem\FilesystemManager](https://laravel.com/api/10.x/Illuminate/Filesystem/FilesystemManager.html)  |  `filesystem`
Storage (Instance)  |  [Illuminate\Contracts\Filesystem\Filesystem](https://laravel.com/api/10.x/Illuminate/Contracts/Filesystem/Filesystem.html)  |  `filesystem.disk`
URL  |  [Illuminate\Routing\UrlGenerator](https://laravel.com/api/10.x/Illuminate/Routing/UrlGenerator.html)  |  `url`
Validator  |  [Illuminate\Validation\Factory](https://laravel.com/api/10.x/Illuminate/Validation/Factory.html)  |  `validator`
Validator (Instance)  |  [Illuminate\Validation\Validator](https://laravel.com/api/10.x/Illuminate/Validation/Validator.html)  |  &nbsp;
View  |  [Illuminate\View\Factory](https://laravel.com/api/10.x/Illuminate/View/Factory.html)  |  `view`
View (Instance)  |  [Illuminate\View\View](https://laravel.com/api/10.x/Illuminate/View/View.html)  |  &nbsp;
Vite  |  [Illuminate\Foundation\Vite](https://laravel.com/api/10.x/Illuminate/Foundation/Vite.html)  |  &nbsp;

</div>