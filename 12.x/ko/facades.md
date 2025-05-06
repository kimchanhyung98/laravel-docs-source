# 파사드(Facades)

- [소개](#introduction)
- [파사드를 언제 사용해야 할까?](#when-to-use-facades)
    - [파사드 vs. 의존성 주입(Dependency Injection)](#facades-vs-dependency-injection)
    - [파사드 vs. 헬퍼 함수(Helper Functions)](#facades-vs-helper-functions)
- [파사드의 작동 원리](#how-facades-work)
- [실시간 파사드(Real-Time Facades)](#real-time-facades)
- [파사드 클래스 레퍼런스](#facade-class-reference)

<a name="introduction"></a>
## 소개

라라벨 공식 문서 전반에서 여러분은 "파사드(facade)"를 통해 라라벨의 기능과 상호작용하는 코드 예제를 자주 보게 됩니다. 파사드는 애플리케이션의 [서비스 컨테이너](/docs/{{version}}/container)에 등록된 클래스에 "정적" 인터페이스를 제공합니다. 라라벨에는 다양한 파사드가 제공되어 라라벨의 대부분의 기능에 접근할 수 있습니다.

라라벨 파사드는 서비스 컨테이너 안의 클래스에 대한 "정적 프록시" 역할을 하며, 간결하고 표현적인 문법의 이점을 제공하는 동시에 기존의 정적 메소드보다 더 높은 테스트 용이성과 유연성을 유지합니다. 파사드의 작동 방식을 완벽히 이해하지 못해도 괜찮으니, 일단 흐름을 따라가며 계속해서 라라벨을 학습하시길 바랍니다.

라라벨의 모든 파사드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 따라서, 다음과 같이 파사드에 쉽게 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

라라벨 공식 문서에서는 프레임워크의 다양한 기능을 설명할 때 파사드를 사용하는 예제들이 많이 등장합니다.

<a name="helper-functions"></a>
#### 헬퍼 함수(Helper Functions)

파사드를 보완하기 위해, 라라벨은 글로벌 "헬퍼 함수"를 제공합니다. 헬퍼 함수는 라라벨의 여러 공통 기능과의 상호작용을 더욱 쉽게 만들어줍니다. 예를 들어, `view`, `response`, `url`, `config` 등의 헬퍼 함수가 자주 사용됩니다. 각 헬퍼 함수는 관련 기능의 문서에 자세히 설명되어 있으며, 전체 목록은 별도의 [헬퍼 문서](/docs/{{version}}/helpers)에서 확인할 수 있습니다.

예를 들어, `Illuminate\Support\Facades\Response` 파사드를 사용하여 JSON 응답을 생성하는 대신, 단순히 `response` 함수를 사용할 수 있습니다. 헬퍼 함수는 전역적으로 사용할 수 있으므로, 별도로 클래스를 임포트하지 않아도 됩니다:

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
## 파사드를 언제 사용해야 할까?

파사드는 여러 장점을 가지고 있습니다. 파사드는 간결하고 기억하기 쉬운 문법을 제공하여, 복잡한 클래스명을 따로 기억하거나 수동으로 주입/설정하지 않고도 라라벨의 기능을 활용할 수 있게 해줍니다. 또한 PHP의 동적 메소드 방식을 사용하기 때문에, 테스트도 용이합니다.

하지만 파사드를 사용할 때 주의할 점도 있습니다. 파사드를 남용하면 클래스의 '역할 범위(scope)'가 불필요하게 커질 위험이 있습니다. 파사드는 사용이 간편하고 주입이 필요 없기 때문에, 한 클래스 안에서 여러 개의 파사드를 사용하게 되며 클래스가 점점 거대해질 수 있습니다. 의존성 주입을 사용하면 생성자에 많은 의존성이 추가되어 시각적으로 클래스가 너무 커지고 있다는 것을 쉽게 인식할 수 있습니다. 따라서 파사드를 사용할 때는 클래스의 크기에 특히 주의하여, 책임 범위가 좁게 유지되도록 하세요. 만약 클래스가 너무 커진다면, 여러 작은 클래스로 분리하는 것을 고려하십시오.

<a name="facades-vs-dependency-injection"></a>
### 파사드 vs. 의존성 주입(Dependency Injection)

의존성 주입의 주요 이점 중 하나는 주입받은 클래스의 구현체를 쉽게 교체할 수 있다는 점입니다. 이는 테스트 과정에서 매우 유용한데, 모의(mock) 객체 또는 스텁(stub) 객체를 주입하고 해당 메소드가 호출되었는지 검증할 수 있기 때문입니다.

진짜 정적(static) 클래스 메소드는 일반적으로 목/스텁 처리할 수 없지만, 파사드는 동적 메소드 호출 방식을 통해 서비스 컨테이너에서 객체를 불러오기 때문에, 마치 주입된 클래스 인스턴스처럼 파사드를 테스트할 수 있습니다. 예를 들면, 아래와 같은 라우트가 있다고 합시다:

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

라라벨에서 제공하는 파사드 테스트 메소드를 활용하면, 아래와 같이 `Cache::get` 메소드에 원하는 인자가 전달되었는지 확인하는 테스트 코드를 작성할 수 있습니다:

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
### 파사드 vs. 헬퍼 함수(Helper Functions)

파사드 외에도 라라벨에는 "헬퍼 함수"가 다양하게 내장되어 있어 뷰 생성, 이벤트 발생, 작업 디스패치, HTTP 응답 반환 등 여러 작업을 쉽게 처리할 수 있습니다. 많은 헬퍼 함수들은 해당 파사드와 동일한 기능을 수행합니다. 예를 들어, 아래 두 코드는 같은 동작을 합니다:

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

파사드와 헬퍼 함수 사이에는 실제로 실질적인 차이가 없습니다. 헬퍼 함수를 사용할 때도 파사드를 사용하는 것과 동일하게 테스트할 수 있습니다. 예를 들어, 아래 라우트를 보면:

```php
Route::get('/cache', function () {
    return cache('key');
});
```

`cache` 헬퍼 함수는 내부적으로 `Cache` 파사드의 기반 클래스의 `get` 메소드를 호출합니다. 그래서 헬퍼 함수를 사용하더라도, 전달된 인자가 올바른지 다음과 같이 테스트할 수 있습니다:

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
## 파사드의 작동 원리

라라벨 애플리케이션에서 파사드는 컨테이너에 등록된 객체에 접근할 수 있게 해주는 클래스입니다. 이런 동작을 가능하게 하는 핵심 역할을 `Facade` 클래스가 담당합니다. 라라벨의 파사드 또는 여러분이 직접 만드는 커스텀 파사드는 모두 기본 `Illuminate\Support\Facades\Facade` 클래스를 상속합니다.

`Facade` 기본 클래스는 `__callStatic()` 매직 메소드를 활용하여, 파사드의 메소드 호출을 서비스 컨테이너에서 불러온 객체로 위임합니다. 아래 예시에선 라라벨 캐시 시스템을 호출합니다. 이 코드만 보면 마치 `Cache` 클래스의 정적 `get` 메소드를 호출하는 것처럼 보입니다:

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

파일 상단에서 `Cache` 파사드를 "import"한 것을 볼 수 있습니다. 이 파사드는 실제로 `Illuminate\Contracts\Cache\Factory` 인터페이스의 구현체에 접근하는 프록시 역할을 합니다. 파사드를 거쳐 호출하는 모든 메소드는 실제로 라라벨의 캐시 서비스 인스턴스에 전달됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 살펴보면, 실제로 `get`이라는 정적 메소드가 없습니다:

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

대신, `Cache` 파사드는 기본 `Facade` 클래스를 확장하고, `getFacadeAccessor()`라는 메소드를 정의합니다. 이 메소드는 서비스 컨테이너에 등록된 바인딩 이름을 반환하는 역할을 합니다. 사용자가 `Cache` 파사드의 어떤 정적 메소드를 호출하면, 라라벨은 [서비스 컨테이너](/docs/{{version}}/container)에서 `cache` 바인딩을 가져와 해당 객체에서 실제 메소드를 실행합니다(이 예제에서는 `get` 메소드).

<a name="real-time-facades"></a>
## 실시간 파사드(Real-Time Facades)

실시간 파사드를 이용하면, 애플리케이션 내의 어떤 클래스든 파사드처럼 사용할 수 있습니다. 사용 예시를 들기 위해, 먼저 실시간 파사드를 사용하지 않는 코드를 살펴보겠습니다. 만약 `Podcast` 모델에 `publish` 메소드가 있다고 가정해 봅시다. 이때 팟캐스트를 게시하려면 `Publisher` 인스턴스를 주입해야 합니다:

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

이처럼 메소드에 퍼블리셔 구현체를 주입하면, 목(Mock) 객체를 사용할 수 있어 단위 테스트가 쉬워집니다. 하지만 메소드 호출마다 반드시 퍼블리셔 인스턴스를 전달해야 한다는 점이 번거로울 수 있습니다. 실시간 파사드를 활용하면, 테스트 용이성은 그대로 유지하면서도 명시적으로 `Publisher` 인스턴스를 전달하지 않아도 됩니다. 실시간 파사드를 생성하려면, 임포트하는 클래스 네임스페이스 앞에 `Facades`를 붙이면 됩니다:

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

실시간 파사드를 사용하면, 퍼블리셔 구현체는 `Facades` 접두사 뒤에 오는 인터페이스 혹은 클래스 이름 일부를 사용해 서비스 컨테이너에서 자동으로 해결(resolve)됩니다. 테스트 시에는 라라벨 내장 파사드 테스트 헬퍼를 이용해 쉽게 목(mock) 처리를 할 수 있습니다:

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

아래는 모든 파사드와 그 기반이 되는 클래스, 그리고 해당되는 경우 서비스 컨테이너 바인딩 키까지 정리한 표입니다. 원하는 파사드의 API 문서를 빠르게 찾아볼 때 매우 유용합니다. [서비스 컨테이너 바인딩](/docs/{{version}}/container) 키도 함께 확인할 수 있습니다.

<div class="overflow-auto">

| 파사드(Facade) | 클래스(Class) | 서비스 컨테이너 바인딩(Service Container Binding) |
| --- | --- | --- |
| App | [Illuminate\Foundation\Application](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| Auth (Instance) | [Illuminate\Contracts\Auth\Guard](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Auth | [Illuminate\Auth\AuthManager](https://api.laravel.com/docs/{{version}}/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://api.laravel.com/docs/{{version}}/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast (Instance) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| Bus | [Illuminate\Contracts\Bus\Dispatcher](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| Cache (Instance) | [Illuminate\Cache\Repository](https://api.laravel.com/docs/{{version}}/Illuminate/Cache/Repository.html) | `cache.store` |
| Cache | [Illuminate\Cache\CacheManager](https://api.laravel.com/docs/{{version}}/Illuminate/Cache/CacheManager.html) | `cache` |
| Config | [Illuminate\Config\Repository](https://api.laravel.com/docs/{{version}}/Illuminate/Config/Repository.html) | `config` |
| Context | [Illuminate\Log\Context\Repository](https://api.laravel.com/docs/{{version}}/Illuminate/Log/Context/Repository.html) | &nbsp; |
| Cookie | [Illuminate\Cookie\CookieJar](https://api.laravel.com/docs/{{version}}/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://api.laravel.com/docs/{{version}}/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date | [Illuminate\Support\DateFactory](https://api.laravel.com/docs/{{version}}/Illuminate/Support/DateFactory.html) | `date` |
| DB (Instance) | [Illuminate\Database\Connection](https://api.laravel.com/docs/{{version}}/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://api.laravel.com/docs/{{version}}/Illuminate/Database/DatabaseManager.html) | `db` |
| Event | [Illuminate\Events\Dispatcher](https://api.laravel.com/docs/{{version}}/Illuminate/Events/Dispatcher.html) | `events` |
| Exceptions (Instance) | [Illuminate\Contracts\Debug\ExceptionHandler](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| Exceptions | [Illuminate\Foundation\Exceptions\Handler](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| File | [Illuminate\Filesystem\Filesystem](https://api.laravel.com/docs/{{version}}/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate | [Illuminate\Contracts\Auth\Access\Gate](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| Hash | [Illuminate\Contracts\Hashing\Hasher](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http | [Illuminate\Http\Client\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Http/Client/Factory.html) | &nbsp; |
| Lang | [Illuminate\Translation\Translator](https://api.laravel.com/docs/{{version}}/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://api.laravel.com/docs/{{version}}/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://api.laravel.com/docs/{{version}}/Illuminate/Mail/Mailer.html) | `mailer` |
| Notification | [Illuminate\Notifications\ChannelManager](https://api.laravel.com/docs/{{version}}/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| Password (Instance) | [Illuminate\Auth\Passwords\PasswordBroker](https://api.laravel.com/docs/{{version}}/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://api.laravel.com/docs/{{version}}/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Pipeline (Instance) | [Illuminate\Pipeline\Pipeline](https://api.laravel.com/docs/{{version}}/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| Process | [Illuminate\Process\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Process/Factory.html) | &nbsp; |
| Queue (Base Class) | [Illuminate\Queue\Queue](https://api.laravel.com/docs/{{version}}/Illuminate/Queue/Queue.html) | &nbsp; |
| Queue (Instance) | [Illuminate\Contracts\Queue\Queue](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue | [Illuminate\Queue\QueueManager](https://api.laravel.com/docs/{{version}}/Illuminate/Queue/QueueManager.html) | `queue` |
| RateLimiter | [Illuminate\Cache\RateLimiter](https://api.laravel.com/docs/{{version}}/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| Redirect | [Illuminate\Routing\Redirector](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (Instance) | [Illuminate\Redis\Connections\Connection](https://api.laravel.com/docs/{{version}}/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Redis | [Illuminate\Redis\RedisManager](https://api.laravel.com/docs/{{version}}/Illuminate/Redis/RedisManager.html) | `redis` |
| Request | [Illuminate\Http\Request](https://api.laravel.com/docs/{{version}}/Illuminate/Http/Request.html) | `request` |
| Response (Instance) | [Illuminate\Http\Response](https://api.laravel.com/docs/{{version}}/Illuminate/Http/Response.html) | &nbsp; |
| Response | [Illuminate\Contracts\Routing\ResponseFactory](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Router.html) | `router` |
| Schedule | [Illuminate\Console\Scheduling\Schedule](https://api.laravel.com/docs/{{version}}/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| Schema | [Illuminate\Database\Schema\Builder](https://api.laravel.com/docs/{{version}}/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| Session (Instance) | [Illuminate\Session\Store](https://api.laravel.com/docs/{{version}}/Illuminate/Session/Store.html) | `session.store` |
| Session | [Illuminate\Session\SessionManager](https://api.laravel.com/docs/{{version}}/Illuminate/Session/SessionManager.html) | `session` |
| Storage (Instance) | [Illuminate\Contracts\Filesystem\Filesystem](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| Storage | [Illuminate\Filesystem\FilesystemManager](https://api.laravel.com/docs/{{version}}/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator (Instance) | [Illuminate\Validation\Validator](https://api.laravel.com/docs/{{version}}/Illuminate/Validation/Validator.html) | &nbsp; |
| Validator | [Illuminate\Validation\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Validation/Factory.html) | `validator` |
| View (Instance) | [Illuminate\View\View](https://api.laravel.com/docs/{{version}}/Illuminate/View/View.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Vite.html) | &nbsp; |

</div>