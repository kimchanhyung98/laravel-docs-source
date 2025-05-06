# 파사드(Facades)

- [소개](#introduction)
- [파사드를 사용할 때](#when-to-use-facades)
    - [파사드 vs. 의존성 주입](#facades-vs-dependency-injection)
    - [파사드 vs. 헬퍼 함수](#facades-vs-helper-functions)
- [파사드의 동작 원리](#how-facades-work)
- [실시간 파사드(Real-Time Facades)](#real-time-facades)
- [파사드 클래스 참고자료](#facade-class-reference)

<a name="introduction"></a>
## 소개

Laravel 공식 문서 전반에 걸쳐 "파사드(facade)"를 통해 Laravel의 기능과 상호작용하는 코드 예시를 볼 수 있습니다. 파사드는 애플리케이션의 [서비스 컨테이너](/docs/{{version}}/container)에 등록된 클래스들에 대해 "정적(static)" 인터페이스를 제공합니다. Laravel은 대부분의 기능에 접근할 수 있는 다양한 기본 파사드를 제공합니다.

Laravel 파사드는 서비스 컨테이너 내 실제 클래스에 대한 "정적 프록시" 역할을 하여, 간결하고 표현적인 문법의 장점은 살리면서도, 기존의 정적 메서드보다 더 나은 테스트 용이성과 유연성을 제공합니다. 파사드의 동작 원리를 완벽하게 이해하지 못해도 괜찮으니, 일단 사용하면서 Laravel을 계속 학습해도 무방합니다.

모든 Laravel의 파사드는 `Illuminate\Support\Facades` 네임스페이스로 정의되어 있습니다. 따라서 다음과 같이 파사드에 쉽게 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel 공식 문서의 많은 예제에서는 프레임워크의 다양한 기능을 설명하기 위해 파사드를 사용합니다.

<a name="helper-functions"></a>
#### 헬퍼 함수(Helper Functions)

파사드를 보완하기 위해, Laravel은 자주 사용하는 기능을 더 쉽게 사용할 수 있도록 다양한 글로벌 "헬퍼 함수"를 제공합니다. 자주 사용하는 대표적인 헬퍼 함수로는 `view`, `response`, `url`, `config` 등이 있습니다. 각 헬퍼 함수에 대한 자세한 내용은 대응하는 기능의 문서에서 확인할 수 있으며, [헬퍼 함수 문서](/docs/{{version}}/helpers)에서 전체 목록을 볼 수 있습니다.

예를 들어, JSON 응답을 생성할 때 `Illuminate\Support\Facades\Response` 파사드 대신 `response` 함수를 사용할 수 있습니다. 헬퍼 함수는 전역적으로 사용할 수 있기 때문에 별도의 클래스 임포트가 필요하지 않습니다:

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
## 파사드를 사용할 때

파사드는 여러 가지 장점을 가지고 있습니다. 긴 클래스 이름을 기억하거나 주입하거나 직접 설정할 필요 없이, Laravel의 기능을 간결하고 기억하기 쉬운 문법으로 사용할 수 있게 해줍니다. 또한 PHP의 동적 메서드 기능을 활용하기 때문에, 테스트하기도 편리합니다.

하지만 파사드를 사용할 때는 몇 가지 주의해야 할 점이 있습니다. 파사드의 가장 큰 위험은 클래스의 "스코프 크리프(scope creep)"입니다. 파사드는 쉽게 사용할 수 있고 주입 없이 접근 가능하기 때문에, 너무 많은 파사드를 한 클래스에서 남용하게 되어 클래스가 과도하게 비대해질 수 있습니다. 의존성 주입을 사용하면 생성자의 길이에서 클래스가 너무 커지고 있음을 바로 알 수 있지만, 파사드는 그 경계가 모호해지기 쉽습니다. 따라서 파사드를 사용할 때는 담당하는 역할이 좁게 유지되도록 클래스의 크기를 항상 주의 깊게 관리해야 합니다. 클래스가 너무 커진다면 여러 개의 더 작은 클래스로 분리하세요.

<a name="facades-vs-dependency-injection"></a>
### 파사드 vs. 의존성 주입

의존성 주입의 가장 큰 장점 중 하나는, 주입받은 클래스의 구현체를 쉽게 교체할 수 있다는 점입니다. 테스트할 때는 모의(mock) 객체나 스텁(stub)을 주입하고, 그 객체의 특정 메서드가 실제로 호출되었는지 검증할 수 있습니다.

일반적으로, 완전히 정적 메서드를 가진 클래스는 모킹이나 스텁이 불가능합니다. 그러나 파사드는 동적 메서드를 이용하여 서비스 컨테이너에서 객체를 가져와 프록시하므로, 실제로 파사드도 인스턴스를 주입받은 경우와 동일하게 테스트할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있을 때:

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel의 파사드 테스트 메서드를 사용하면, 다음과 같이 `Cache::get` 메서드가 기대한 인자로 호출되었는지 확인하는 테스트를 작성할 수 있습니다:

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
### 파사드 vs. 헬퍼 함수

파사드 외에도, Laravel은 뷰 생성, 이벤트 발생, 작업 디스패치, HTTP 응답 등 다양한 공통 작업을 수행할 수 있는 "헬퍼 함수"를 제공합니다. 이 중 다수는 각각의 파사드와 동일한 역할을 합니다. 예를 들어, 아래의 파사드 호출과 헬퍼 함수 호출은 동일하게 동작합니다:

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

실제로 파사드와 헬퍼 함수는 기능적으로 아무런 차이가 없습니다. 헬퍼 함수를 사용할 때도 해당 파사드와 동일하게 테스트할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있을 때:

```php
Route::get('/cache', function () {
    return cache('key');
});
```

`cache` 헬퍼는 내부적으로 `Cache` 파사드가 대표하는 클래스의 `get` 메서드를 호출합니다. 따라서 헬퍼 함수를 사용하더라도 아래처럼 같은 방식으로 메서드 호출을 테스트할 수 있습니다:

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
## 파사드의 동작 원리

Laravel 애플리케이션에서 파사드는 서비스 컨테이너의 객체에 접근할 수 있도록 하는 클래스입니다. 이 동작의 핵심은 `Facade` 클래스에 구현되어 있습니다. Laravel의 모든 기본 및 사용자 정의 파사드는 기본 `Illuminate\Support\Facades\Facade` 클래스를 확장하여 만듭니다.

`Facade` 기본 클래스는 `__callStatic()` 매직 메서드를 사용해 파사드로부터의 호출을 서비스 컨테이너에서 resolve된 실제 객체로 전달합니다. 아래 예제를 보면 Laravel의 캐시 시스템에 호출이 전달됩니다. 코드를 보면 마치 `Cache` 클래스의 정적 `get` 메서드가 직접 호출되는 것처럼 보일 수 있습니다:

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

파일 상단에 `Cache` 파사드를 "임포트"하는 부분을 주목하세요. 이 파사드는 실제로 `Illuminate\Contracts\Cache\Factory` 인터페이스의 구현체에 접근하는 프록시 역할을 합니다. 우리가 파사드를 통해 호출하는 모든 메서드는 실제 Laravel 캐시 서비스 인스턴스로 전달됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 확인해 보면, 정적 메서드 `get`이 실제로 선언되어 있지 않습니다:

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

대신에, `Cache` 파사드는 기본 `Facade` 클래스를 확장하고, `getFacadeAccessor()` 메서드를 통해 서비스 컨테이너 바인딩의 이름을 반환합니다. `Cache` 파사드의 정적 메서드가 호출되면, Laravel은 [서비스 컨테이너](/docs/{{version}}/container)에서 `cache` 바인딩을 resolve하고, 해당 객체에 요청된 메서드(`get`)를 실행합니다.

<a name="real-time-facades"></a>
## 실시간 파사드(Real-Time Facades)

실시간 파사드를 사용하면, 애플리케이션 내의 어떤 클래스라도 파사드처럼 사용할 수 있습니다. 먼저, 실시간 파사드를 사용하지 않는 예시를 살펴보겠습니다. 예를 들어, `Podcast` 모델에 `publish` 메서드가 있다고 가정합니다. 하지만 팟캐스트를 게시하려면 `Publisher` 인스턴스를 주입 받아야 합니다:

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

메서드에 퍼블리셔 구현체를 주입하면, 테스트 시 이 퍼블리셔를 모킹하여 독립적으로 쉽게 검증할 수 있습니다. 하지만 매번 `publish` 메서드를 호출할 때마다 Publisher 인스턴스를 직접 전달해야 하는 번거로움이 있습니다. 실시간 파사드를 사용하면 동일한 테스트 용이성은 유지하면서, 명시적으로 Publisher 인스턴스를 전달하지 않아도 됩니다. 실시간 파사드를 생성하려면, 임포트하는 클래스 네임스페이스 앞에 `Facades` 프리픽스를 붙이면 됩니다:

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

실시간 파사드를 사용하면, 인터페이스나 클래스 이름에서 `Facades` 프리픽스 이후 부분을 기준으로 서비스 컨테이너에서 구현체가 resolve됩니다. 테스트 시에는 Laravel의 내장 파사드 테스트 도우미를 통해 이 메서드 호출을 모킹할 수 있습니다:

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
## 파사드 클래스 참고자료

아래는 각 파사드와 그에 대응되는 실제 클래스의 목록입니다. 특정 파사드의 루트 클래스 API 문서를 빠르게 조회할 때 유용합니다. 해당하는 경우 [서비스 컨테이너 바인딩](/docs/{{version}}/container) 키도 함께 표시됩니다.

<div class="overflow-auto">

| 파사드(Facade) | 클래스(Class) | 서비스 컨테이너 바인딩 |
| --- | --- | --- |
| App | [Illuminate\Foundation\Application](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| Auth (인스턴스) | [Illuminate\Contracts\Auth\Guard](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Auth | [Illuminate\Auth\AuthManager](https://api.laravel.com/docs/{{version}}/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://api.laravel.com/docs/{{version}}/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast (인스턴스) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| Bus | [Illuminate\Contracts\Bus\Dispatcher](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| Cache (인스턴스) | [Illuminate\Cache\Repository](https://api.laravel.com/docs/{{version}}/Illuminate/Cache/Repository.html) | `cache.store` |
| Cache | [Illuminate\Cache\CacheManager](https://api.laravel.com/docs/{{version}}/Illuminate/Cache/CacheManager.html) | `cache` |
| Config | [Illuminate\Config\Repository](https://api.laravel.com/docs/{{version}}/Illuminate/Config/Repository.html) | `config` |
| Context | [Illuminate\Log\Context\Repository](https://api.laravel.com/docs/{{version}}/Illuminate/Log/Context/Repository.html) | &nbsp; |
| Cookie | [Illuminate\Cookie\CookieJar](https://api.laravel.com/docs/{{version}}/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://api.laravel.com/docs/{{version}}/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date | [Illuminate\Support\DateFactory](https://api.laravel.com/docs/{{version}}/Illuminate/Support/DateFactory.html) | `date` |
| DB (인스턴스) | [Illuminate\Database\Connection](https://api.laravel.com/docs/{{version}}/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://api.laravel.com/docs/{{version}}/Illuminate/Database/DatabaseManager.html) | `db` |
| Event | [Illuminate\Events\Dispatcher](https://api.laravel.com/docs/{{version}}/Illuminate/Events/Dispatcher.html) | `events` |
| Exceptions (인스턴스) | [Illuminate\Contracts\Debug\ExceptionHandler](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| Exceptions | [Illuminate\Foundation\Exceptions\Handler](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| File | [Illuminate\Filesystem\Filesystem](https://api.laravel.com/docs/{{version}}/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate | [Illuminate\Contracts\Auth\Access\Gate](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| Hash | [Illuminate\Contracts\Hashing\Hasher](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http | [Illuminate\Http\Client\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Http/Client/Factory.html) | &nbsp; |
| Lang | [Illuminate\Translation\Translator](https://api.laravel.com/docs/{{version}}/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://api.laravel.com/docs/{{version}}/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://api.laravel.com/docs/{{version}}/Illuminate/Mail/Mailer.html) | `mailer` |
| Notification | [Illuminate\Notifications\ChannelManager](https://api.laravel.com/docs/{{version}}/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| Password (인스턴스) | [Illuminate\Auth\Passwords\PasswordBroker](https://api.laravel.com/docs/{{version}}/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://api.laravel.com/docs/{{version}}/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Pipeline (인스턴스) | [Illuminate\Pipeline\Pipeline](https://api.laravel.com/docs/{{version}}/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| Process | [Illuminate\Process\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Process/Factory.html) | &nbsp; |
| Queue (기본 클래스) | [Illuminate\Queue\Queue](https://api.laravel.com/docs/{{version}}/Illuminate/Queue/Queue.html) | &nbsp; |
| Queue (인스턴스) | [Illuminate\Contracts\Queue\Queue](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue | [Illuminate\Queue\QueueManager](https://api.laravel.com/docs/{{version}}/Illuminate/Queue/QueueManager.html) | `queue` |
| RateLimiter | [Illuminate\Cache\RateLimiter](https://api.laravel.com/docs/{{version}}/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| Redirect | [Illuminate\Routing\Redirector](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (인스턴스) | [Illuminate\Redis\Connections\Connection](https://api.laravel.com/docs/{{version}}/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Redis | [Illuminate\Redis\RedisManager](https://api.laravel.com/docs/{{version}}/Illuminate/Redis/RedisManager.html) | `redis` |
| Request | [Illuminate\Http\Request](https://api.laravel.com/docs/{{version}}/Illuminate/Http/Request.html) | `request` |
| Response (인스턴스) | [Illuminate\Http\Response](https://api.laravel.com/docs/{{version}}/Illuminate/Http/Response.html) | &nbsp; |
| Response | [Illuminate\Contracts\Routing\ResponseFactory](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Router.html) | `router` |
| Schedule | [Illuminate\Console\Scheduling\Schedule](https://api.laravel.com/docs/{{version}}/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| Schema | [Illuminate\Database\Schema\Builder](https://api.laravel.com/docs/{{version}}/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| Session (인스턴스) | [Illuminate\Session\Store](https://api.laravel.com/docs/{{version}}/Illuminate/Session/Store.html) | `session.store` |
| Session | [Illuminate\Session\SessionManager](https://api.laravel.com/docs/{{version}}/Illuminate/Session/SessionManager.html) | `session` |
| Storage (인스턴스) | [Illuminate\Contracts\Filesystem\Filesystem](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| Storage | [Illuminate\Filesystem\FilesystemManager](https://api.laravel.com/docs/{{version}}/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator (인스턴스) | [Illuminate\Validation\Validator](https://api.laravel.com/docs/{{version}}/Illuminate/Validation/Validator.html) | &nbsp; |
| Validator | [Illuminate\Validation\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Validation/Factory.html) | `validator` |
| View (인스턴스) | [Illuminate\View\View](https://api.laravel.com/docs/{{version}}/Illuminate/View/View.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Vite.html) | &nbsp; |

</div>
