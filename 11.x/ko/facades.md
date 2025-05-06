# 파사드 (Facades)

- [소개](#introduction)
- [파사드 활용 시점](#when-to-use-facades)
    - [파사드 vs. 의존성 주입](#facades-vs-dependency-injection)
    - [파사드 vs. 헬퍼 함수](#facades-vs-helper-functions)
- [파사드의 동작 원리](#how-facades-work)
- [실시간 파사드(Real-Time Facades)](#real-time-facades)
- [파사드 클래스 레퍼런스](#facade-class-reference)

<a name="introduction"></a>
## 소개

Laravel 공식 문서 전반에서, "파사드(facades)"를 통해 Laravel의 기능을 사용하는 코드 예제를 자주 볼 수 있습니다. 파사드는 애플리케이션의 [서비스 컨테이너](/docs/{{version}}/container)에 등록된 클래스에 "정적(static)" 인터페이스를 제공합니다. Laravel은 거의 모든 기능에 접근할 수 있는 다양한 파사드를 기본으로 제공합니다.

Laravel의 파사드는 서비스 컨테이너 안의 실제 클래스에 대한 "정적 프록시"로 동작하며, 간결하고 표현력 있는 문법을 제공하는 동시에 기존의 정적 메소드보다 테스트 용이성과 유연성을 높입니다. 파사드가 어떻게 동작하는지 완전히 이해하지 못해도 괜찮으니, 일단 편하게 사용하며 계속해서 Laravel을 학습해 나가시기 바랍니다.

Laravel의 모든 파사드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 따라서 다음과 같이 파사드에 쉽게 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel 공식 문서의 다양한 예제에서도 여러 프레임워크 기능을 설명할 때 파사드를 사용합니다.

<a name="helper-functions"></a>
#### 헬퍼 함수(Helper Functions)

파사드를 보완하는 기능으로, Laravel은 여러 전역 "헬퍼 함수"를 제공합니다. 헬퍼 함수를 통해 주요 Laravel 기능에 더욱 쉽게 접근할 수 있습니다. `view`, `response`, `url`, `config` 등 자주 쓰이는 헬퍼 함수들이 있습니다. 각 헬퍼 함수는 해당 기능의 공식 문서에서 설명되어 있으며, 전체 목록은 전용 [헬퍼 함수 문서](/docs/{{version}}/helpers)에서 확인할 수 있습니다.

예를 들어, `Illuminate\Support\Facades\Response` 파사드를 사용해서 JSON 응답을 생성하는 대신, `response` 헬퍼 함수를 사용할 수 있습니다. 헬퍼 함수는 전역적으로 사용 가능하므로 별도의 클래스 임포트 없이 바로 사용할 수 있습니다:

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
## 파사드 활용 시점

파사드는 여러 장점이 있습니다. 파사드는 길고 복잡한 클래스 이름을 기억하거나 직접 의존성 주입이나 수동 설정을 할 필요 없이, 간결하고 직관적인 문법으로 Laravel의 기능을 활용할 수 있게 도와줍니다. 또한, PHP의 동적 메서드 활용 덕분에 테스트가 쉽다는 장점도 있습니다.

하지만, 파사드 사용 시 주의할 점도 있습니다. 가장 큰 위험은 클래스의 "스코프 침식(scope creep)"입니다. 파사드는 너무 사용이 쉽고, 의존성 주입이 필요 없기 때문에, 하나의 클래스에서 너무 많은 파사드를 사용하며 클래스가 비대해질 위험이 있습니다. 의존성 주입 방식을 사용할 때는 생성자가 길어질수록 시각적으로 클래스가 너무 커지고 있다는 경고를 받게 되지만, 파사드를 쓰면 이를 쉽게 놓칠 수 있습니다. 따라서 파사드를 사용할 때는 클래스가 너무 커지지 않도록 꾸준히 관리하고, 크기가 커진다면 여러 개의 더 작은 클래스로 분리하는 것이 좋습니다.

<a name="facades-vs-dependency-injection"></a>
### 파사드 vs. 의존성 주입

의존성 주입의 가장 큰 장점 중 하나는 주입된 클래스의 구현을 쉽게 교체할 수 있다는 점입니다. 이는 테스트에서도 유용하게 쓰이며, 목(mock) 또는 스텁(stub)을 주입하여 메서드 호출을 검증할 수 있습니다.

전통적인 완전한 정적 클래스의 메소드는 모킹이나 스텁 처리가 어렵지만, 파사드는 동적 메서드를 통해 서비스 컨테이너에서 객체를 가져와서 호출하기 때문에, 주입된 클래스 인스턴스와 동일하게 테스트할 수 있습니다. 예를 들어, 아래 라우트 예시에서:

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel의 파사드 테스트 메서드를 활용하면 다음과 같이 `Cache::get` 메서드가 기대한 인자로 호출되었는지 테스트할 수 있습니다:

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

Laravel에는 파사드 외에도 다양한 "헬퍼" 함수가 내장되어 있습니다. 이 함수들은 뷰 생성, 이벤트 발행, 작업(Job) 디스패치, HTTP 응답 전송 등 여러 일반적인 작업을 수행할 수 있도록 도와줍니다. 이들 중 상당수는 대응되는 파사드와 동일한 역할을 합니다. 예를 들어, 아래 두 방법은 동일하게 동작합니다:

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

실제로, 파사드와 헬퍼 함수 간에는 실질적인 차이가 없습니다. 헬퍼 함수를 사용할 때도 동일하게 테스트 할 수 있습니다. 예를 들어 다음 라우트가 있을 때:

```php
Route::get('/cache', function () {
    return cache('key');
});
```

`cache` 헬퍼는 내부적으로 `Cache` 파사드가 감싸고 있는 클래스의 `get` 메서드를 호출합니다. 헬퍼 함수를 사용해도 아래와 같이 해당 메서드가 예상한 인자로 호출되었는지 테스트할 수 있습니다:

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

Laravel 애플리케이션에서 파사드는 컨테이너의 객체에 접근할 수 있도록 하는 클래스입니다. 이 뒤에서 실제 동작을 담당하는 것이 `Facade` 클래스입니다. Laravel의 모든 파사드와, 사용자가 직접 만드는 커스텀 파사드는 기본적으로 `Illuminate\Support\Facades\Facade`를 확장(extends)하여 만듭니다.

`Facade` 기본 클래스는 `__callStatic()` 매직 메서드를 이용해, 파사드의 호출을 컨테이너에서 resolve한 객체로 위임합니다. 아래 예시는 Laravel의 캐시 시스템을 사용하는 코드입니다. 이런 코드를 보면, `Cache` 클래스의 정적 메서드 `get`을 호출하는 것처럼 보일 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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

파일 상단에서 `Cache` 파사드를 임포트한 것을 볼 수 있습니다. 이 파사드는 `Illuminate\Contracts\Cache\Factory` 인터페이스의 실제 구현체에 접근하기 위한 프록시 역할을 합니다. 파사드를 이용해서 호출한 모든 메서드는 Laravel의 캐시 서비스의 실제 인스턴스로 전달됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 살펴보면, 실제로는 정적 메서드 `get`이 정의되어 있지 않습니다:

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

대신, `Cache` 파사드는 기본 `Facade` 클래스를 확장하고, `getFacadeAccessor()` 메서드를 구현합니다. 이 메서드는 서비스 컨테이너 결합(binding) 이름을 반환합니다. 사용자가 `Cache` 파사드에서 어떤 정적 메서드를 호출하면, Laravel은 [서비스 컨테이너](/docs/{{version}}/container)에서 `cache`를 resolve(해결)하고, 실제 객체에 해당 메서드(`get`)를 실행합니다.

<a name="real-time-facades"></a>
## 실시간 파사드(Real-Time Facades)

실시간 파사드(Real-Time Facade)를 사용하면, 애플리케이션 내의 어떤 클래스든 파사드처럼 사용할 수 있습니다. 먼저, 실시간 파사드를 사용하지 않을 땐 어떻게 하는지 예시를 보겠습니다. 예를 들어, 우리의 `Podcast` 모델에 `publish` 메서드가 있다고 가정합시다. 이때, 팟캐스트를 발행하려면, 반드시 `Publisher` 인스턴스를 주입 받아야 합니다:

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

이처럼 메서드에서 publisher를 주입받으면, publisher를 손쉽게 목(mock) 처리하여 테스트할 수 있습니다. 하지만, `publish` 메서드를 호출할 때마다 항상 publisher 인스턴스를 전달해야 한다는 번거로움이 있습니다. 실시간 파사드를 사용하면, 이러한 번거로움 없이도 동일한 테스트 용이성을 유지할 수 있습니다. 실시간 파사드를 생성하려면, 임포트하는 클래스 네임스페이스 앞에 `Facades`를 붙여주면 됩니다:

```php
<?php

namespace App\Models;

// use App\Contracts\Publisher; // [tl! remove]
use Facades\App\Contracts\Publisher; // [tl! add]
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * Publish the podcast.
     */
    // public function publish(Publisher $publisher): void // [tl! remove]
    public function publish(): void // [tl! add]
    {
        $this->update(['publishing' => now()]);

        // $publisher->publish($this); // [tl! remove]
        Publisher::publish($this); // [tl! add]
    }
}
```

실시간 파사드를 사용할 경우, `Facades` 프리픽스 뒤에 오는 인터페이스나 클래스 이름을 기반으로 해당 구현체가 서비스 컨테이너에서 resolve되어 사용됩니다. 테스트에서도 Laravel의 내장 파사드 테스트 헬퍼를 활용할 수 있습니다:

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
## 파사드 클래스 레퍼런스

아래 표에는 각 파사드와 해당하는 실제 클래스가 정리되어 있습니다. 각 파사드 루트의 API 문서를 빠르게 확인하고자 할 때 참고하실 수 있습니다. [서비스 컨테이너 바인딩](/docs/{{version}}/container) 키도 함께 기재되어 있습니다.

<div class="overflow-auto">

| 파사드(Facade) | 클래스(Class) | 서비스 컨테이너 바인딩 |
| --- | --- | --- |
| App | [Illuminate\Foundation\Application](https://laravel.com/api/{{version}}/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://laravel.com/api/{{version}}/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| Auth (인스턴스) | [Illuminate\Contracts\Auth\Guard](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Auth | [Illuminate\Auth\AuthManager](https://laravel.com/api/{{version}}/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://laravel.com/api/{{version}}/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast (인스턴스) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://laravel.com/api/{{version}}/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| Bus | [Illuminate\Contracts\Bus\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| Cache (인스턴스) | [Illuminate\Cache\Repository](https://laravel.com/api/{{version}}/Illuminate/Cache/Repository.html) | `cache.store` |
| Cache | [Illuminate\Cache\CacheManager](https://laravel.com/api/{{version}}/Illuminate/Cache/CacheManager.html) | `cache` |
| Config | [Illuminate\Config\Repository](https://laravel.com/api/{{version}}/Illuminate/Config/Repository.html) | `config` |
| Context | [Illuminate\Log\Context\Repository](https://laravel.com/api/{{version}}/Illuminate/Log/Context/Repository.html) | &nbsp; |
| Cookie | [Illuminate\Cookie\CookieJar](https://laravel.com/api/{{version}}/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://laravel.com/api/{{version}}/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date | [Illuminate\Support\DateFactory](https://laravel.com/api/{{version}}/Illuminate/Support/DateFactory.html) | `date` |
| DB (인스턴스) | [Illuminate\Database\Connection](https://laravel.com/api/{{version}}/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://laravel.com/api/{{version}}/Illuminate/Database/DatabaseManager.html) | `db` |
| Event | [Illuminate\Events\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Events/Dispatcher.html) | `events` |
| Exceptions (인스턴스) | [Illuminate\Contracts\Debug\ExceptionHandler](https://laravel.com/api/{{version}}/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| Exceptions | [Illuminate\Foundation\Exceptions\Handler](https://laravel.com/api/{{version}}/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| File | [Illuminate\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate | [Illuminate\Contracts\Auth\Access\Gate](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| Hash | [Illuminate\Contracts\Hashing\Hasher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http | [Illuminate\Http\Client\Factory](https://laravel.com/api/{{version}}/Illuminate/Http/Client/Factory.html) | &nbsp; |
| Lang | [Illuminate\Translation\Translator](https://laravel.com/api/{{version}}/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://laravel.com/api/{{version}}/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://laravel.com/api/{{version}}/Illuminate/Mail/Mailer.html) | `mailer` |
| Notification | [Illuminate\Notifications\ChannelManager](https://laravel.com/api/{{version}}/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| Password (인스턴스) | [Illuminate\Auth\Passwords\PasswordBroker](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Pipeline (인스턴스) | [Illuminate\Pipeline\Pipeline](https://laravel.com/api/{{version}}/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| Process | [Illuminate\Process\Factory](https://laravel.com/api/{{version}}/Illuminate/Process/Factory.html) | &nbsp; |
| Queue (기본 클래스) | [Illuminate\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Queue/Queue.html) | &nbsp; |
| Queue (인스턴스) | [Illuminate\Contracts\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue | [Illuminate\Queue\QueueManager](https://laravel.com/api/{{version}}/Illuminate/Queue/QueueManager.html) | `queue` |
| RateLimiter | [Illuminate\Cache\RateLimiter](https://laravel.com/api/{{version}}/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| Redirect | [Illuminate\Routing\Redirector](https://laravel.com/api/{{version}}/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (인스턴스) | [Illuminate\Redis\Connections\Connection](https://laravel.com/api/{{version}}/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Redis | [Illuminate\Redis\RedisManager](https://laravel.com/api/{{version}}/Illuminate/Redis/RedisManager.html) | `redis` |
| Request | [Illuminate\Http\Request](https://laravel.com/api/{{version}}/Illuminate/Http/Request.html) | `request` |
| Response (인스턴스) | [Illuminate\Http\Response](https://laravel.com/api/{{version}}/Illuminate/Http/Response.html) | &nbsp; |
| Response | [Illuminate\Contracts\Routing\ResponseFactory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://laravel.com/api/{{version}}/Illuminate/Routing/Router.html) | `router` |
| Schedule | [Illuminate\Console\Scheduling\Schedule](https://laravel.com/api/{{version}}/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| Schema | [Illuminate\Database\Schema\Builder](https://laravel.com/api/{{version}}/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| Session (인스턴스) | [Illuminate\Session\Store](https://laravel.com/api/{{version}}/Illuminate/Session/Store.html) | `session.store` |
| Session | [Illuminate\Session\SessionManager](https://laravel.com/api/{{version}}/Illuminate/Session/SessionManager.html) | `session` |
| Storage (인스턴스) | [Illuminate\Contracts\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| Storage | [Illuminate\Filesystem\FilesystemManager](https://laravel.com/api/{{version}}/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://laravel.com/api/{{version}}/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator (인스턴스) | [Illuminate\Validation\Validator](https://laravel.com/api/{{version}}/Illuminate/Validation/Validator.html) | &nbsp; |
| Validator | [Illuminate\Validation\Factory](https://laravel.com/api/{{version}}/Illuminate/Validation/Factory.html) | `validator` |
| View (인스턴스) | [Illuminate\View\View](https://laravel.com/api/{{version}}/Illuminate/View/View.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://laravel.com/api/{{version}}/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://laravel.com/api/{{version}}/Illuminate/Foundation/Vite.html) | &nbsp; |

</div>