# Facades (파사드)

- [소개](#introduction)
- [파사드를 사용해야 할 때](#when-to-use-facades)
    - [파사드 vs. 의존성 주입](#facades-vs-dependency-injection)
    - [파사드 vs. 헬퍼 함수](#facades-vs-helper-functions)
- [파사드의 동작 원리](#how-facades-work)
- [실시간 파사드](#real-time-facades)
- [파사드 클래스 참고](#facade-class-reference)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 문서 전반에서, Laravel의 여러 기능과 상호작용하는 코드 예제를 "파사드(facades)"를 통해 자주 보게 됩니다. 파사드는 애플리케이션의 [서비스 컨테이너](/docs/master/container)에 등록된 클래스에 대해 "정적" 인터페이스를 제공합니다. Laravel은 거의 모든 기능에 접근할 수 있는 다양한 파사드를 기본으로 포함하고 있습니다.

Laravel 파사드는 서비스 컨테이너 내 실제 클래스에 대한 "정적 프록시" 역할을 하며, 간결하고 표현력 있는 문법을 제공하는 동시에 전통적인 정적 메서드보다 테스트 용이성과 유연성을 높여줍니다. 파사드의 내부 동작 방식을 완벽히 이해하지 못해도 전혀 문제가 없으니, 부담 갖지 말고 계속해서 Laravel을 학습해 나가시기 바랍니다.

모든 Laravel 파사드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 따라서 파사드에 다음과 같이 쉽게 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel 문서 전반에서 많은 예제들이 프레임워크의 다양한 기능을 설명하기 위해 파사드를 사용합니다.

<a name="helper-functions"></a>
#### 헬퍼 함수

파사드를 보완하기 위해, Laravel은 공통 Laravel 기능에 더 쉽게 접근할 수 있도록 다양한 글로벌 "헬퍼 함수"를 제공합니다. 자주 사용되는 헬퍼 함수로는 `view`, `response`, `url`, `config` 등이 있습니다. Laravel에서 제공하는 각 헬퍼 함수는 해당 기능 설명과 함께 문서화되어 있지만, 전체 목록은 전용 [헬퍼 문서](/docs/master/helpers)에서 확인할 수 있습니다.

예를 들어, `Illuminate\Support\Facades\Response` 파사드를 사용해 JSON 응답을 만들기보다, `response` 함수를 사용하는 편이 간편합니다. 헬퍼 함수는 전역에서 사용 가능하므로, 별도의 클래스를 임포트하지 않아도 됩니다:

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
## 파사드를 사용해야 할 때 (When to Utilize Facades)

파사드는 여러 장점이 있습니다. 간결하고 기억하기 쉬운 문법을 제공하여, 복잡한 클래스 이름을 기억하거나 직접 주입/설정하지 않아도 Laravel 기능을 사용할 수 있습니다. 또한 PHP의 동적 메서드 방식을 독특하게 활용해 테스트도 수월합니다.

하지만 파사드를 사용할 때 주의해야 할 점도 있습니다. 가장 큰 위험은 클래스의 "책임 범위(scope creep)"가 커져버리는 것입니다. 파사드는 너무 쉽게 사용할 수 있고 주입이 필요 없으므로, 단일 클래스에 여러 파사드를 남용하면서 클래스가 지나치게 커져 버릴 위험이 큽니다. 반면, 의존성 주입을 사용하면 커다란 생성자가 시각적으로 클래스가 너무 커졌음을 알려주어 이런 문제를 줄일 수 있습니다. 따라서 파사드를 쓸 때는 클래스 크기를 특히 주의하여 책임 범위가 좁게 유지되도록 해야 합니다. 만약 클래스가 너무 커진다면 여러 개의 작은 클래스로 분리하는 것을 고려하세요.

<a name="facades-vs-dependency-injection"></a>
### 파사드 vs. 의존성 주입 (Facades vs. Dependency Injection)

의존성 주입의 주요 장점 중 하나는 주입된 클래스 구현을 쉽게 교체할 수 있다는 점입니다. 이는 테스트 중에 모의(Mock)나 스텁(Stub)을 주입해 해당 메서드 호출을 검증할 때 매우 유용합니다.

정적으로 선언된 메서드는 일반적으로 모킹이나 스텁 구현이 불가능한데, 파사드는 서비스 컨테이너에서 객체를 해석(resolved)하여 동적 메서드를 통해 호출을 위임하기 때문에 실제로는 주입된 인스턴스를 테스트할 때와 동일하게 테스트할 수 있습니다. 예를 들어, 다음 라우트를 보면:

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel의 파사드 테스트 메서드를 활용하면, `Cache::get` 메서드가 우리가 기대한 인수와 함께 호출되었는지 다음과 같이 검증할 수 있습니다:

```php tab=Pest
use Illuminate\Support\Facades\Cache;

test('basic example', function () {
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
});
```

```php tab=PHPUnit
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
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
### 파사드 vs. 헬퍼 함수 (Facades vs. Helper Functions)

파사드 외에도 Laravel에는 뷰 생성, 이벤트 실행, 작업(job) 디스패치, HTTP 응답 전송 같은 작업을 쉽게 처리하는 다양한 "헬퍼" 함수들이 포함되어 있습니다. 많은 헬퍼 함수는 해당하는 파사드와 같은 기능을 수행합니다. 예를 들어, 다음 두 코드는 동일한 결과를 만듭니다:

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

파사드와 헬퍼 함수 사이에 실질적인 차이는 전혀 없습니다. 헬퍼 함수를 사용할 때도 대응되는 파사드를 테스트하듯 동일한 방식으로 테스트할 수 있습니다. 예를 들어, 다음 라우트를 보면:

```php
Route::get('/cache', function () {
    return cache('key');
});
```

`cache` 헬퍼 함수는 내부적으로 `Cache` 파사드가 사용하는 클래스의 `get` 메서드를 호출합니다. 따라서 헬퍼 함수를 사용하더라도 아래와 같이 메서드 호출이 예상대로 되었는지 검증하는 테스트를 작성할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
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
## 파사드의 동작 원리 (How Facades Work)

Laravel 애플리케이션에서 파사드는 서비스 컨테이너에서 객체에 접근할 수 있도록 하는 클래스입니다. 이 동작의 핵심 역할은 `Facade` 클래스에 있습니다. Laravel의 내장 파사드와 사용자가 직접 만드는 커스텀 파사드는 모두 기본 `Illuminate\Support\Facades\Facade` 클래스를 확장합니다.

`Facade` 기본 클래스는 PHP의 `__callStatic()` 매직 메서드를 활용해, 파사드 쪽에서 정적 메서드 호출을 서비스 컨테이너로부터 해석된 실제 객체의 메서드 호출로 위임(프록시)합니다. 다음 예제에서는 Laravel 캐시 시스템에 호출이 전달됩니다. 이 코드를 보면 `Cache` 클래스의 정적 `get` 메서드가 호출되는 것처럼 보입니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function showProfile(string $id): View
    {
        $user = Cache::get('user:'.$id);

        return view('profile', ['user' => $user]);
    }
}
```

파일 상단에서 `Cache` 파사드를 임포트한 것에 주목하세요. 이 파사드는 `Illuminate\Contracts\Cache\Factory` 인터페이스의 실제 구현체에 접근하는 프록시 역할을 합니다. 파사드를 통해 발생하는 모든 호출은 Laravel 캐시 서비스의 실제 인스턴스로 전달됩니다.

실제 `Illuminate\Support\Facades\Cache` 클래스를 보면, `get` 같은 정적 메서드는 정의되어 있지 않습니다:

```php
class Cache extends Facade
{
    /**
     * Get the registered name of the component.
     */
    protected static function getFacadeAccessor(): string
    {
        return 'cache';
    }
}
```

대신 `Cache` 파사드는 기본 `Facade` 클래스를 상속하며, `getFacadeAccessor()` 메서드를 정의합니다. 이 메서드는 서비스 컨테이너에서 바인딩된 이름을 반환하는 역할을 합니다. 사용자가 `Cache` 파사드의 정적 메서드를 호출하면, Laravel은 서비스 컨테이너에서 `cache` 바인딩을 해석해내고, 호출된 메서드(`get`)를 해당 인스턴스에서 실행합니다.

<a name="real-time-facades"></a>
## 실시간 파사드 (Real-Time Facades)

실시간 파사드를 사용하면 애플리케이션 내 어떤 클래스라도 파사드처럼 다룰 수 있습니다. 이 기능의 사용법을 설명하기 위해, 먼저 실시간 파사드를 사용하지 않은 상태의 코드를 살펴봅시다. 예를 들어, `Podcast` 모델에 `publish` 메서드가 있다고 가정합시다. 단, 팟캐스트를 발행하기 위해 `Publisher` 인스턴스를 주입해야 합니다:

```php
<?php

namespace App\Models;

use App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * Publish the podcast.
     */
    public function publish(Publisher $publisher): void
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this);
    }
}
```

메서드에 퍼블리셔 구현체를 주입하면, 주입된 퍼블리셔를 모킹해서 단위 테스트를 쉽게 할 수 있다는 장점이 있습니다. 하지만 매 번 `publish` 메서드를 호출할 때마다 퍼블리셔 인스턴스를 넘겨줘야만 하는 단점도 있습니다. 실시간 파사드를 사용하면, 동일한 테스트 가능성을 유지하면서도 `Publisher` 인스턴스를 명시적으로 전달할 필요 없이 사용할 수 있습니다. 실시간 파사드를 만들려면, 임포트하는 클래스 네임스페이스 앞에 `Facades` 접두사를 붙입니다:

```php
<?php

namespace App\Models;

use App\Contracts\Publisher; // [tl! remove]
use Facades\App\Contracts\Publisher; // [tl! add]
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * Publish the podcast.
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

실시간 파사드를 사용하면 `Facades` 접두사 뒤에 나오는 인터페이스나 클래스 이름의 일부를 기준으로 서비스 컨테이너에서 구현체가 자동으로 해석됩니다. 테스트 시에는 Laravel 내장 파사드 테스트 도구를 이용해 이 메서드 호출을 쉽게 모킹할 수 있습니다:

```php tab=Pest
<?php

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

test('podcast can be published', function () {
    $podcast = Podcast::factory()->create();

    Publisher::shouldReceive('publish')->once()->with($podcast);

    $podcast->publish();
});
```

```php tab=PHPUnit
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
     * A test example.
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
## 파사드 클래스 참고 (Facade Class Reference)

아래 표는 주요 파사드와 해당 파사드가 프록시하는 실제 클래스 및 관련 서비스 컨테이너 바인딩 키를 정리한 자료입니다. 특정 파사드의 API 문서를 빠르게 찾아볼 때 유용합니다.

<div class="overflow-auto">

| 파사드 (Facade) | 클래스 (Class) | 서비스 컨테이너 바인딩 (Service Container Binding) |
| --- | --- | --- |
| App | [Illuminate\Foundation\Application](https://api.laravel.com/docs/master/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://api.laravel.com/docs/master/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| Auth (인스턴스) | [Illuminate\Contracts\Auth\Guard](https://api.laravel.com/docs/master/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Auth | [Illuminate\Auth\AuthManager](https://api.laravel.com/docs/master/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://api.laravel.com/docs/master/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast (인스턴스) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://api.laravel.com/docs/master/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://api.laravel.com/docs/master/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| Bus | [Illuminate\Contracts\Bus\Dispatcher](https://api.laravel.com/docs/master/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| Cache (인스턴스) | [Illuminate\Cache\Repository](https://api.laravel.com/docs/master/Illuminate/Cache/Repository.html) | `cache.store` |
| Cache | [Illuminate\Cache\CacheManager](https://api.laravel.com/docs/master/Illuminate/Cache/CacheManager.html) | `cache` |
| Config | [Illuminate\Config\Repository](https://api.laravel.com/docs/master/Illuminate/Config/Repository.html) | `config` |
| Context | [Illuminate\Log\Context\Repository](https://api.laravel.com/docs/master/Illuminate/Log/Context/Repository.html) | &nbsp; |
| Cookie | [Illuminate\Cookie\CookieJar](https://api.laravel.com/docs/master/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://api.laravel.com/docs/master/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date | [Illuminate\Support\DateFactory](https://api.laravel.com/docs/master/Illuminate/Support/DateFactory.html) | `date` |
| DB (인스턴스) | [Illuminate\Database\Connection](https://api.laravel.com/docs/master/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://api.laravel.com/docs/master/Illuminate/Database/DatabaseManager.html) | `db` |
| Event | [Illuminate\Events\Dispatcher](https://api.laravel.com/docs/master/Illuminate/Events/Dispatcher.html) | `events` |
| Exceptions (인스턴스) | [Illuminate\Contracts\Debug\ExceptionHandler](https://api.laravel.com/docs/master/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| Exceptions | [Illuminate\Foundation\Exceptions\Handler](https://api.laravel.com/docs/master/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| File | [Illuminate\Filesystem\Filesystem](https://api.laravel.com/docs/master/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate | [Illuminate\Contracts\Auth\Access\Gate](https://api.laravel.com/docs/master/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| Hash | [Illuminate\Contracts\Hashing\Hasher](https://api.laravel.com/docs/master/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http | [Illuminate\Http\Client\Factory](https://api.laravel.com/docs/master/Illuminate/Http/Client/Factory.html) | &nbsp; |
| Lang | [Illuminate\Translation\Translator](https://api.laravel.com/docs/master/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://api.laravel.com/docs/master/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://api.laravel.com/docs/master/Illuminate/Mail/Mailer.html) | `mailer` |
| Notification | [Illuminate\Notifications\ChannelManager](https://api.laravel.com/docs/master/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| Password (인스턴스) | [Illuminate\Auth\Passwords\PasswordBroker](https://api.laravel.com/docs/master/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://api.laravel.com/docs/master/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Pipeline (인스턴스) | [Illuminate\Pipeline\Pipeline](https://api.laravel.com/docs/master/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| Process | [Illuminate\Process\Factory](https://api.laravel.com/docs/master/Illuminate/Process/Factory.html) | &nbsp; |
| Queue (기초 클래스) | [Illuminate\Queue\Queue](https://api.laravel.com/docs/master/Illuminate/Queue/Queue.html) | &nbsp; |
| Queue (인스턴스) | [Illuminate\Contracts\Queue\Queue](https://api.laravel.com/docs/master/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue | [Illuminate\Queue\QueueManager](https://api.laravel.com/docs/master/Illuminate/Queue/QueueManager.html) | `queue` |
| RateLimiter | [Illuminate\Cache\RateLimiter](https://api.laravel.com/docs/master/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| Redirect | [Illuminate\Routing\Redirector](https://api.laravel.com/docs/master/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (인스턴스) | [Illuminate\Redis\Connections\Connection](https://api.laravel.com/docs/master/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Redis | [Illuminate\Redis\RedisManager](https://api.laravel.com/docs/master/Illuminate/Redis/RedisManager.html) | `redis` |
| Request | [Illuminate\Http\Request](https://api.laravel.com/docs/master/Illuminate/Http/Request.html) | `request` |
| Response (인스턴스) | [Illuminate\Http\Response](https://api.laravel.com/docs/master/Illuminate/Http/Response.html) | &nbsp; |
| Response | [Illuminate\Contracts\Routing\ResponseFactory](https://api.laravel.com/docs/master/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://api.laravel.com/docs/master/Illuminate/Routing/Router.html) | `router` |
| Schedule | [Illuminate\Console\Scheduling\Schedule](https://api.laravel.com/docs/master/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| Schema | [Illuminate\Database\Schema\Builder](https://api.laravel.com/docs/master/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| Session (인스턴스) | [Illuminate\Session\Store](https://api.laravel.com/docs/master/Illuminate/Session/Store.html) | `session.store` |
| Session | [Illuminate\Session\SessionManager](https://api.laravel.com/docs/master/Illuminate/Session/SessionManager.html) | `session` |
| Storage (인스턴스) | [Illuminate\Contracts\Filesystem\Filesystem](https://api.laravel.com/docs/master/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| Storage | [Illuminate\Filesystem\FilesystemManager](https://api.laravel.com/docs/master/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://api.laravel.com/docs/master/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator (인스턴스) | [Illuminate\Validation\Validator](https://api.laravel.com/docs/master/Illuminate/Validation/Validator.html) | &nbsp; |
| Validator | [Illuminate\Validation\Factory](https://api.laravel.com/docs/master/Illuminate/Validation/Factory.html) | `validator` |
| View (인스턴스) | [Illuminate\View\View](https://api.laravel.com/docs/master/Illuminate/View/View.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://api.laravel.com/docs/master/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://api.laravel.com/docs/master/Illuminate/Foundation/Vite.html) | &nbsp; |

</div>