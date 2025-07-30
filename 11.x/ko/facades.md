# Facades (파사드)

- [소개](#introduction)
- [파사드를 사용해야 할 때](#when-to-use-facades)
    - [파사드와 의존성 주입 비교](#facades-vs-dependency-injection)
    - [파사드와 헬퍼 함수 비교](#facades-vs-helper-functions)
- [파사드 작동 원리](#how-facades-work)
- [실시간 파사드](#real-time-facades)
- [파사드 클래스 레퍼런스](#facade-class-reference)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 문서 전반에 걸쳐 "파사드(facades)"를 통해 Laravel의 기능과 상호작용하는 코드 예시를 많이 볼 수 있습니다. 파사드는 애플리케이션의 [서비스 컨테이너](/docs/11.x/container)에 등록된 클래스들에 대해 "정적" 인터페이스를 제공합니다. Laravel은 거의 모든 프레임워크 기능에 접근할 수 있는 다양한 파사드를 기본으로 제공합니다.

Laravel 파사드는 서비스 컨테이너에 있는 기본 클래스를 "정적 프록시"로 감싸 간결하고 표현력 있는 문법을 제공하면서 전통적인 정적 메소드보다 더 높은 테스트 가능성과 유연성을 제공합니다. 파사드가 어떻게 동작하는지 완벽히 이해하지 못해도 괜찮으니, 자연스럽게 따라가며 Laravel 학습을 계속하세요.

모든 Laravel 파사드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 따라서 다음과 같이 간단히 파사드에 접근할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel 문서에서 다양한 프레임워크 기능을 설명할 때, 많은 예시가 파사드를 활용합니다.

<a name="helper-functions"></a>
#### 헬퍼 함수

파사드를 보완하기 위해, Laravel은 흔히 쓰이는 기능을 더 쉽게 사용할 수 있도록 여러 글로벌 "헬퍼 함수"도 제공합니다. 여러분이 자주 쓰게 될 대표적인 헬퍼 함수로는 `view`, `response`, `url`, `config` 등이 있습니다. Laravel에서 제공하는 각 헬퍼 함수는 관련 기능별 문서에 설명되어 있으며, 전체 목록은 [헬퍼 함수 문서](/docs/11.x/helpers)에서 확인할 수 있습니다.

예를 들어, `Illuminate\Support\Facades\Response` 파사드를 사용해 JSON 응답을 생성하는 대신, 간단히 `response` 함수를 사용할 수 있습니다. 헬퍼 함수는 전역에서 사용 가능하므로 별도의 클래스 임포트가 필요 없습니다:

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
## 파사드를 사용해야 할 때 (When to Utilize Facades)

파사드는 여러 장점이 있습니다. 길고 복잡한 클래스 이름을 기억하거나 직접 주입하거나 설정할 필요 없이 Laravel 기능을 손쉽게 사용할 수 있는 간결하고 기억하기 쉬운 문법을 제공합니다. 또한 PHP의 동적 메소드 활용 방식을 이용해 테스트도 용이합니다.

하지만 파사드를 사용할 때는 주의해야 할 점도 있습니다. 파사드 사용의 주요 위험은 클래스의 책임 범위가 너무 커지는 "스코프 확장(scope creep)" 문제입니다. 파사드는 매우 사용이 편리하고 주입이 필요 없기 때문에 한 클래스 안에 과도하게 많은 파사드를 사용하게 될 가능성이 큽니다. 의존성 주입을 사용하면, 큰 생성자의 존재가 클래스가 너무 커졌다는 시각적 신호 역할을 하지만, 파사드 사용 시엔 이런 신호를 받기가 어렵습니다. 따라서 파사드를 사용할 때는 클래스 크기와 책임 범위를 주의 깊게 관리해야 합니다. 만약 클래스가 너무 커진다면, 여러 개의 작은 클래스로 나누는 것을 고려하세요.

<a name="facades-vs-dependency-injection"></a>
### 파사드와 의존성 주입 비교 (Facades vs. Dependency Injection)

의존성 주입의 가장 큰 장점 중 하나는 주입된 클래스의 구현체를 교체할 수 있다는 점입니다. 이것은 테스트 과정에서 목(mock)이나 스텁(stub)을 주입하여 특정 메소드 호출 여부를 검증할 때 유용합니다.

정적(static) 메소드의 경우에는 일반적으로 목킹이나 스텁이 불가능하지만, 파사드는 동적 메소드를 활용해 서비스 컨테이너에서 객체를 찾아 호출을 위임하는 방식이기 때문에, 주입된 클래스 인스턴스를 테스트하듯 파사드도 테스트할 수 있습니다. 예를 들어 다음 라우트를 보겠습니다:

```
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel의 파사드 테스트 메서드를 사용하면, 다음 테스트 코드로 `Cache::get` 메소드가 기대하는 인수와 함께 호출되었는지 검증할 수 있습니다:

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
### 파사드와 헬퍼 함수 비교 (Facades vs. Helper Functions)

파사드 외에도 Laravel은 뷰 생성, 이벤트 발생, 잡 디스패치, HTTP 응답 전송 등 흔히 하는 작업을 처리하는 여러 "헬퍼 함수"를 제공합니다. 많은 헬퍼 함수들은 대응하는 파사드와 동일한 역할을 수행합니다. 예를 들어 다음 두 코드는 동등합니다:

```
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

파사드와 헬퍼 함수는 실전에서는 기능적으로 아무런 차이가 없습니다. 헬퍼 함수를 사용할 때도, 대응하는 파사드처럼 동일한 테스트 방법으로 테스트할 수 있습니다. 예를 들어 다음 라우트에서:

```
Route::get('/cache', function () {
    return cache('key');
});
```

`cache` 헬퍼는 `Cache` 파사드가 감싸는 클래스의 `get` 메서드를 호출합니다. 그러므로 헬퍼 함수를 사용하더라도 다음 테스트로 해당 메소드가 예상 인수와 함께 호출되었는지 검증할 수 있습니다:

```
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
## 파사드 작동 원리 (How Facades Work)

Laravel 애플리케이션에서 파사드는 컨테이너에서 객체에 접근할 수 있는 클래스를 의미합니다. 이를 가능하게 하는 핵심 코드는 `Facade` 클래스 내에 있습니다. Laravel의 모든 파사드와 사용자 정의 파사드는 기본 `Illuminate\Support\Facades\Facade` 클래스를 상속합니다.

`Facade` 기본 클래스는 `__callStatic()` 매직 메서드를 사용해서 파사드에 대한 호출을 서비스 컨테이너에서 찾아낸 객체로 위임합니다. 아래 예제에서는 Laravel 캐시 시스템에 호출이 이루어집니다. 코드만 보면 `Cache` 클래스의 정적 `get` 메서드를 호출하는 것처럼 보일 수 있습니다:

```
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

파일 상단에서 `Cache` 파사드를 "import" 한 것을 확인할 수 있습니다. 이 파사드는 `Illuminate\Contracts\Cache\Factory` 인터페이스를 구현하는 실제 캐시 기능에 접근하기 위한 프록시 역할을 합니다. 파사드를 통해 호출된 모든 메소드는 Laravel 캐시 서비스의 실제 인스턴스에 전달됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 살펴보면, `get` 같은 정적 메서드는 정의되어 있지 않습니다:

```
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

대신, `Cache` 파사드는 기본 `Facade` 클래스를 상속받아 `getFacadeAccessor()` 메서드를 정의하고 있습니다. 이 메서드는 서비스 컨테이너에 바인딩된 이름을 반환합니다. 사용자가 `Cache` 파사드의 정적 메서드를 호출하면, Laravel이 서비스 컨테이너에서 `cache` 키로 바인딩된 객체를 찾아 해당 메서드(여기서는 `get`)를 실행합니다.

<a name="real-time-facades"></a>
## 실시간 파사드 (Real-Time Facades)

실시간 파사드를 사용하면 애플리케이션 내의 어떤 클래스든 마치 파사드처럼 다룰 수 있습니다. 이 개념을 이해하기 위해, 실시간 파사드를 사용하지 않은 코드를 먼저 살펴봅시다. 예를 들어, `Podcast` 모델에 `publish` 메서드가 있다고 가정해봅니다. 하지만 팟캐스트 게시를 위해 `Publisher` 인스턴스를 주입해야 합니다:

```
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

메서드에 퍼블리셔 구현체를 주입하면, 목(mock) 객체를 쉽게 주입하여 메서드 단독 테스트가 가능하지만, `publish` 메서드를 호출할 때마다 퍼블리셔 인스턴스를 명시적으로 넘겨야 하는 불편함이 있습니다. 실시간 파사드를 이용하면 동일한 테스트 가능성을 유지하면서도 `Publisher` 인스턴스를 직접 전달하지 않아도 됩니다. 이를 위해 import 문에서 네임스페이스 앞에 `Facades` 접두어를 붙입니다:

```
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

실시간 파사드를 사용할 때는 `Facades` 접두어 뒤에 따라오는 인터페이스 또는 클래스 이름 부분이 서비스 컨테이너에서 찾아질 바인딩 키로 간주됩니다. 따라서 퍼블리셔 구현체가 서비스 컨테이너에서 자동으로 해결됩니다. 테스트 시에는 Laravel 내장 파사드 테스트 헬퍼를 이용해 이 메서드 호출을 목(mock)할 수 있습니다:

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
## 파사드 클래스 레퍼런스 (Facade Class Reference)

아래 표는 주요 파사드와 그에 대응하는 실제 클래스, 그리고 서비스 컨테이너 바인딩 키를 정리한 것입니다. 특정 파사드에 대한 API 문서를 빠르게 탐색할 때 유용합니다.

<div class="overflow-auto">

| 파사드 | 클래스 | 서비스 컨테이너 바인딩 |
| --- | --- | --- |
| App | [Illuminate\Foundation\Application](https://laravel.com/api/11.x/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://laravel.com/api/11.x/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| Auth (인스턴스) | [Illuminate\Contracts\Auth\Guard](https://laravel.com/api/11.x/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Auth | [Illuminate\Auth\AuthManager](https://laravel.com/api/11.x/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://laravel.com/api/11.x/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast (인스턴스) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://laravel.com/api/11.x/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://laravel.com/api/11.x/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| Bus | [Illuminate\Contracts\Bus\Dispatcher](https://laravel.com/api/11.x/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| Cache (인스턴스) | [Illuminate\Cache\Repository](https://laravel.com/api/11.x/Illuminate/Cache/Repository.html) | `cache.store` |
| Cache | [Illuminate\Cache\CacheManager](https://laravel.com/api/11.x/Illuminate/Cache/CacheManager.html) | `cache` |
| Config | [Illuminate\Config\Repository](https://laravel.com/api/11.x/Illuminate/Config/Repository.html) | `config` |
| Context | [Illuminate\Log\Context\Repository](https://laravel.com/api/11.x/Illuminate/Log/Context/Repository.html) | &nbsp; |
| Cookie | [Illuminate\Cookie\CookieJar](https://laravel.com/api/11.x/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://laravel.com/api/11.x/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date | [Illuminate\Support\DateFactory](https://laravel.com/api/11.x/Illuminate/Support/DateFactory.html) | `date` |
| DB (인스턴스) | [Illuminate\Database\Connection](https://laravel.com/api/11.x/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://laravel.com/api/11.x/Illuminate/Database/DatabaseManager.html) | `db` |
| Event | [Illuminate\Events\Dispatcher](https://laravel.com/api/11.x/Illuminate/Events/Dispatcher.html) | `events` |
| Exceptions (인스턴스) | [Illuminate\Contracts\Debug\ExceptionHandler](https://laravel.com/api/11.x/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| Exceptions | [Illuminate\Foundation\Exceptions\Handler](https://laravel.com/api/11.x/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| File | [Illuminate\Filesystem\Filesystem](https://laravel.com/api/11.x/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate | [Illuminate\Contracts\Auth\Access\Gate](https://laravel.com/api/11.x/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| Hash | [Illuminate\Contracts\Hashing\Hasher](https://laravel.com/api/11.x/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http | [Illuminate\Http\Client\Factory](https://laravel.com/api/11.x/Illuminate/Http/Client/Factory.html) | &nbsp; |
| Lang | [Illuminate\Translation\Translator](https://laravel.com/api/11.x/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://laravel.com/api/11.x/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://laravel.com/api/11.x/Illuminate/Mail/Mailer.html) | `mailer` |
| Notification | [Illuminate\Notifications\ChannelManager](https://laravel.com/api/11.x/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| Password (인스턴스) | [Illuminate\Auth\Passwords\PasswordBroker](https://laravel.com/api/11.x/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://laravel.com/api/11.x/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Pipeline (인스턴스) | [Illuminate\Pipeline\Pipeline](https://laravel.com/api/11.x/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| Process | [Illuminate\Process\Factory](https://laravel.com/api/11.x/Illuminate/Process/Factory.html) | &nbsp; |
| Queue (기본 클래스) | [Illuminate\Queue\Queue](https://laravel.com/api/11.x/Illuminate/Queue/Queue.html) | &nbsp; |
| Queue (인스턴스) | [Illuminate\Contracts\Queue\Queue](https://laravel.com/api/11.x/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue | [Illuminate\Queue\QueueManager](https://laravel.com/api/11.x/Illuminate/Queue/QueueManager.html) | `queue` |
| RateLimiter | [Illuminate\Cache\RateLimiter](https://laravel.com/api/11.x/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| Redirect | [Illuminate\Routing\Redirector](https://laravel.com/api/11.x/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (인스턴스) | [Illuminate\Redis\Connections\Connection](https://laravel.com/api/11.x/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Redis | [Illuminate\Redis\RedisManager](https://laravel.com/api/11.x/Illuminate/Redis/RedisManager.html) | `redis` |
| Request | [Illuminate\Http\Request](https://laravel.com/api/11.x/Illuminate/Http/Request.html) | `request` |
| Response (인스턴스) | [Illuminate\Http\Response](https://laravel.com/api/11.x/Illuminate/Http/Response.html) | &nbsp; |
| Response | [Illuminate\Contracts\Routing\ResponseFactory](https://laravel.com/api/11.x/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://laravel.com/api/11.x/Illuminate/Routing/Router.html) | `router` |
| Schedule | [Illuminate\Console\Scheduling\Schedule](https://laravel.com/api/11.x/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| Schema | [Illuminate\Database\Schema\Builder](https://laravel.com/api/11.x/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| Session (인스턴스) | [Illuminate\Session\Store](https://laravel.com/api/11.x/Illuminate/Session/Store.html) | `session.store` |
| Session | [Illuminate\Session\SessionManager](https://laravel.com/api/11.x/Illuminate/Session/SessionManager.html) | `session` |
| Storage (인스턴스) | [Illuminate\Contracts\Filesystem\Filesystem](https://laravel.com/api/11.x/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| Storage | [Illuminate\Filesystem\FilesystemManager](https://laravel.com/api/11.x/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://laravel.com/api/11.x/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator (인스턴스) | [Illuminate\Validation\Validator](https://laravel.com/api/11.x/Illuminate/Validation/Validator.html) | &nbsp; |
| Validator | [Illuminate\Validation\Factory](https://laravel.com/api/11.x/Illuminate/Validation/Factory.html) | `validator` |
| View (인스턴스) | [Illuminate\View\View](https://laravel.com/api/11.x/Illuminate/View/View.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://laravel.com/api/11.x/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://laravel.com/api/11.x/Illuminate/Foundation/Vite.html) | &nbsp; |

</div>