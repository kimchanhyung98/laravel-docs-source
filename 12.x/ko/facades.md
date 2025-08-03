# 파사드 (Facades)

- [소개](#introduction)
- [파사드를 언제 사용할까](#when-to-use-facades)
    - [파사드와 의존성 주입의 비교](#facades-vs-dependency-injection)
    - [파사드와 헬퍼 함수의 비교](#facades-vs-helper-functions)
- [파사드는 어떻게 작동하는가](#how-facades-work)
- [실시간 파사드](#real-time-facades)
- [파사드 클래스 참고자료](#facade-class-reference)

<a name="introduction"></a>
## 소개 (Introduction)

라라벨 문서 전반에 걸쳐, 라라벨의 기능과 상호작용하는 코드를 "파사드(facades)"를 통해 접할 수 있습니다. 파사드는 애플리케이션의 [서비스 컨테이너](/docs/12.x/container)에 존재하는 클래스들에 대해 "정적" 인터페이스를 제공합니다. 라라벨은 거의 모든 기능에 접근할 수 있는 다양한 파사드를 기본적으로 제공합니다.

라라벨 파사드는 서비스 컨테이너 안에 있는 실체 클래스에 대한 "정적 프록시(static proxies)"로 작동합니다. 이로 인해 간결하고 표현력 높은 문법을 제공하면서도, 전통적인 정적 메서드보다 테스트 가능성과 유연성이 더 뛰어납니다. 파사드가 어떻게 동작하는지 완벽하게 이해하지 못해도 괜찮으니, 부담 갖지 말고 계속 라라벨 학습을 진행해 주세요.

모든 라라벨 파사드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 따라서 파사드를 다음과 같이 쉽게 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

라라벨 공식 문서 내 예제들에서 많은 기능 설명에 파사드를 사용하는 것을 볼 수 있습니다.

<a name="helper-functions"></a>
#### 헬퍼 함수

파사드를 보완하기 위해, 라라벨은 자주 쓰이는 기능과 상호작용하기 쉽게 다양한 전역 "헬퍼 함수"를 제공합니다. 흔히 사용되는 헬퍼 함수에는 `view`, `response`, `url`, `config` 등이 있습니다. 각각의 헬퍼 함수는 관련 기능 설명과 함께 문서화되어 있으며, 전체 목록은 전용 [헬퍼 함수 문서](/docs/12.x/helpers)에서 확인할 수 있습니다.

예를 들어, `Illuminate\Support\Facades\Response` 파사드를 사용하여 JSON 응답을 생성하는 대신, `response` 헬퍼 함수를 사용할 수도 있습니다. 헬퍼 함수는 전역으로 사용 가능하므로 별도의 클래스 임포트가 필요하지 않습니다:

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
## 파사드를 언제 사용할까 (When to Utilize Facades)

파사드에는 여러 이점이 있습니다. 복잡한 클래스 이름을 기억하거나 직접 의존성 주입이나 설정을 할 필요 없이, 간결하고 기억하기 쉬운 문법으로 라라벨의 기능을 사용할 수 있습니다. 또한 PHP의 동적 메서드(dynamic methods)를 활용하기 때문에 테스트도 용이합니다.

하지만 파사드를 사용할 때 주의할 점도 있습니다. 가장 큰 위험은 클래스의 "책임 범위가 커지는(scope creep)" 문제입니다. 파사드는 너무 쉽게 사용할 수 있고 주입이 필요 없기 때문에, 하나의 클래스가 지나치게 많은 파사드를 사용하면서 책임이 불분명해질 수 있습니다. 의존성 주입을 사용하면, 생성자의 인자가 많아지는 것으로 클래스 크기를 시각적으로 확인할 수 있어 이 문제를 완화할 수 있습니다. 따라서 파사드를 사용할 때는 클래스 크기와 책임 범위에 신경 써, 너무 커지면 더 작은 여러 클래스로 나누는 것을 고려하세요.

<a name="facades-vs-dependency-injection"></a>
### 파사드와 의존성 주입의 비교 (Facades vs. Dependency Injection)

의존성 주입의 주요 장점 중 하나는 주입한 클래스의 구현을 쉽게 교체할 수 있다는 점입니다. 이는 테스트 시 모의 객체(mock)나 스텁(stub)을 주입해 원하는 메서드 호출을 확인하는 데 유용합니다.

보통 정적(static) 메서드는 모킹(mocking)이나 스텁 처리하기 어렵지만, 파사드는 동적 메서드를 통해 서비스 컨테이너에서 해결한 객체에 메서드 호출을 위임하기 때문에, 의존성 주입한 인스턴스처럼 테스트할 수 있습니다. 예를 들어, 다음 라우트가 있다고 하면:

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

라라벨의 파사드 테스트 메서드를 사용해 `Cache::get` 메서드가 예상 인수와 함께 호출되었는지 확인하는 테스트를 이렇게 작성할 수 있습니다:

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
 * 기본 기능 테스트 예제.
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
### 파사드와 헬퍼 함수의 비교 (Facades vs. Helper Functions)

파사드 외에도 라라벨은 뷰 생성, 이벤트 실행, 작업 디스패치, HTTP 응답 전송 등 자주 쓰는 공통 작업을 위한 여러 "헬퍼 함수"들을 포함합니다. 많은 헬퍼 함수들은 해당 기능과 동일한 파사드 기능을 수행합니다. 예를 들어, 아래의 파사드 호출과 헬퍼 호출은 동등합니다:

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

파사드와 헬퍼 함수 사이에는 실제 사용상 차이가 전혀 없습니다. 헬퍼 함수를 사용할 때도 해당하는 파사드와 같이 테스트할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있을 때:

```php
Route::get('/cache', function () {
    return cache('key');
});
```

`cache` 헬퍼 함수는 `Cache` 파사드 밑에 있는 클래스에서 `get` 메서드를 호출합니다. 따라서 헬퍼 함수를 사용해도 다음과 같이 메서드 호출을 예상한 대로 했는지 테스트할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

/**
 * 기본 기능 테스트 예제.
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
## 파사드는 어떻게 작동하는가 (How Facades Work)

라라벨 애플리케이션에서 파사드는 서비스 컨테이너에서 객체에 접근할 수 있도록 해주는 클래스입니다. 이 기능을 구현하는 핵심 메커니즘은 `Facade` 클래스 안에 있습니다. 라라벨의 모든 파사드와 사용자가 만든 커스텀 파사드는 기본 `Illuminate\Support\Facades\Facade` 클래스를 상속합니다.

기본 `Facade` 클래스는 `__callStatic()` 매직 메서드(magic-method)를 활용해, 파사드에 대한 정적 메서드 호출을 서비스 컨테이너에서 해결된 객체에 위임합니다. 아래 예시 코드에서는 라라벨 캐시 시스템에 호출을 합니다. 코드를 보면 정적 `get` 메서드가 `Cache` 클래스에서 실행되는 것처럼 보입니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 특정 사용자의 프로필을 보여줍니다.
     */
    public function showProfile(string $id): View
    {
        $user = Cache::get('user:'.$id);

        return view('profile', ['user' => $user]);
    }
}
```

파일 상단에서 `Cache` 파사드를 "임포트"하는 것을 볼 수 있습니다. 이 파사드는 `Illuminate\Contracts\Cache\Factory` 인터페이스의 실제 구현체에 접근하기 위한 프록시 역할을 합니다. 파사드를 통해 호출한 모든 메서드는 라라벨 캐시 서비스의 실제 인스턴스로 전달됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 살펴보면, `get`이라는 정적 메서드는 정의되어 있지 않습니다:

```php
class Cache extends Facade
{
    /**
     * 컴포넌트의 등록명(서비스 컨테이너 바인딩 이름)을 반환합니다.
     */
    protected static function getFacadeAccessor(): string
    {
        return 'cache';
    }
}
```

`Cache` 파사드는 기본 `Facade` 클래스를 상속하며, `getFacadeAccessor()` 메서드를 정의해 해당 바인딩 이름을 반환합니다. 사용자가 `Cache` 파사드의 정적 메서드를 호출하면, 라라벨은 서비스 컨테이너에서 `cache` 바인딩을 찾아 이를 해결하고 요청된 메서드를 실행합니다(`get` 메서드 호출 등).

<a name="real-time-facades"></a>
## 실시간 파사드 (Real-Time Facades)

실시간 파사드를 사용하면 애플리케이션 내 어느 클래스든 마치 파사드처럼 사용할 수 있습니다. 이를 설명하기 위해, 우선 실시간 파사드를 사용하지 않는 코드를 살펴보겠습니다. 예를 들어, `Podcast` 모델에 `publish` 메서드가 있다고 가정해 봅니다. 이 팟캐스트를 "발행"하려면 `Publisher` 인스턴스를 주입받아야 합니다:

```php
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

`publish` 메서드에 퍼블리셔 구현체를 주입하므로 테스트 시 모킹이 쉬워집니다. 하지만 `publish`를 호출할 때마다 매번 퍼블리셔 인스턴스를 전달해야 하는 번거로움이 있습니다. 실시간 파사드를 쓰면 테스트 가능성은 유지하면서도 `Publisher` 인스턴스를 명시적으로 전달하지 않아도 됩니다. 실시간 파사드를 생성하려면, 임포트하는 클래스 네임스페이스 앞에 `Facades`를 붙입니다:

```php
<?php

namespace App\Models;

// use App\Contracts\Publisher; // [tl! remove]
use Facades\App\Contracts\Publisher; // [tl! add]
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * 팟캐스트를 발행합니다.
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

실시간 파사드를 사용하면, `Facades` 접두사 뒤에 나오는 인터페이스나 클래스 이름으로부터 서비스 컨테이너에서 구현체가 해결되어 해당 메서드가 호출됩니다. 테스트 중에는 라라벨 내장 파사드 테스트 도우미를 사용해 이 메서드 호출을 모킹할 수 있습니다:

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
     * 테스트 예제.
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
## 파사드 클래스 참고자료 (Facade Class Reference)

아래 표는 라라벨의 각 파사드와 그 하위 클래스 대응 관계를 정리한 것입니다. 각 파사드 루트에 대한 API 문서를 빠르게 찾아볼 때 유용합니다. 적용 가능한 경우 서비스 컨테이너 바인딩 키도 함께 표기되어 있습니다.

<div class="overflow-auto">

| 파사드 | 클래스 | 서비스 컨테이너 바인딩 |
| --- | --- | --- |
| App | [Illuminate\Foundation\Application](https://api.laravel.com/docs/12.x/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| Auth (인스턴스) | [Illuminate\Contracts\Auth\Guard](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Auth | [Illuminate\Auth\AuthManager](https://api.laravel.com/docs/12.x/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://api.laravel.com/docs/12.x/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast (인스턴스) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| Bus | [Illuminate\Contracts\Bus\Dispatcher](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| Cache (인스턴스) | [Illuminate\Cache\Repository](https://api.laravel.com/docs/12.x/Illuminate/Cache/Repository.html) | `cache.store` |
| Cache | [Illuminate\Cache\CacheManager](https://api.laravel.com/docs/12.x/Illuminate/Cache/CacheManager.html) | `cache` |
| Config | [Illuminate\Config\Repository](https://api.laravel.com/docs/12.x/Illuminate/Config/Repository.html) | `config` |
| Context | [Illuminate\Log\Context\Repository](https://api.laravel.com/docs/12.x/Illuminate/Log/Context/Repository.html) | &nbsp; |
| Cookie | [Illuminate\Cookie\CookieJar](https://api.laravel.com/docs/12.x/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://api.laravel.com/docs/12.x/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date | [Illuminate\Support\DateFactory](https://api.laravel.com/docs/12.x/Illuminate/Support/DateFactory.html) | `date` |
| DB (인스턴스) | [Illuminate\Database\Connection](https://api.laravel.com/docs/12.x/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://api.laravel.com/docs/12.x/Illuminate/Database/DatabaseManager.html) | `db` |
| Event | [Illuminate\Events\Dispatcher](https://api.laravel.com/docs/12.x/Illuminate/Events/Dispatcher.html) | `events` |
| Exceptions (인스턴스) | [Illuminate\Contracts\Debug\ExceptionHandler](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| Exceptions | [Illuminate\Foundation\Exceptions\Handler](https://api.laravel.com/docs/12.x/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| File | [Illuminate\Filesystem\Filesystem](https://api.laravel.com/docs/12.x/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate | [Illuminate\Contracts\Auth\Access\Gate](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| Hash | [Illuminate\Contracts\Hashing\Hasher](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http | [Illuminate\Http\Client\Factory](https://api.laravel.com/docs/12.x/Illuminate/Http/Client/Factory.html) | &nbsp; |
| Lang | [Illuminate\Translation\Translator](https://api.laravel.com/docs/12.x/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://api.laravel.com/docs/12.x/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://api.laravel.com/docs/12.x/Illuminate/Mail/Mailer.html) | `mailer` |
| Notification | [Illuminate\Notifications\ChannelManager](https://api.laravel.com/docs/12.x/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| Password (인스턴스) | [Illuminate\Auth\Passwords\PasswordBroker](https://api.laravel.com/docs/12.x/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://api.laravel.com/docs/12.x/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Pipeline (인스턴스) | [Illuminate\Pipeline\Pipeline](https://api.laravel.com/docs/12.x/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| Process | [Illuminate\Process\Factory](https://api.laravel.com/docs/12.x/Illuminate/Process/Factory.html) | &nbsp; |
| Queue (기본 클래스) | [Illuminate\Queue\Queue](https://api.laravel.com/docs/12.x/Illuminate/Queue/Queue.html) | &nbsp; |
| Queue (인스턴스) | [Illuminate\Contracts\Queue\Queue](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue | [Illuminate\Queue\QueueManager](https://api.laravel.com/docs/12.x/Illuminate/Queue/QueueManager.html) | `queue` |
| RateLimiter | [Illuminate\Cache\RateLimiter](https://api.laravel.com/docs/12.x/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| Redirect | [Illuminate\Routing\Redirector](https://api.laravel.com/docs/12.x/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (인스턴스) | [Illuminate\Redis\Connections\Connection](https://api.laravel.com/docs/12.x/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Redis | [Illuminate\Redis\RedisManager](https://api.laravel.com/docs/12.x/Illuminate/Redis/RedisManager.html) | `redis` |
| Request | [Illuminate\Http\Request](https://api.laravel.com/docs/12.x/Illuminate/Http/Request.html) | `request` |
| Response (인스턴스) | [Illuminate\Http\Response](https://api.laravel.com/docs/12.x/Illuminate/Http/Response.html) | &nbsp; |
| Response | [Illuminate\Contracts\Routing\ResponseFactory](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://api.laravel.com/docs/12.x/Illuminate/Routing/Router.html) | `router` |
| Schedule | [Illuminate\Console\Scheduling\Schedule](https://api.laravel.com/docs/12.x/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| Schema | [Illuminate\Database\Schema\Builder](https://api.laravel.com/docs/12.x/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| Session (인스턴스) | [Illuminate\Session\Store](https://api.laravel.com/docs/12.x/Illuminate/Session/Store.html) | `session.store` |
| Session | [Illuminate\Session\SessionManager](https://api.laravel.com/docs/12.x/Illuminate/Session/SessionManager.html) | `session` |
| Storage (인스턴스) | [Illuminate\Contracts\Filesystem\Filesystem](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| Storage | [Illuminate\Filesystem\FilesystemManager](https://api.laravel.com/docs/12.x/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://api.laravel.com/docs/12.x/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator (인스턴스) | [Illuminate\Validation\Validator](https://api.laravel.com/docs/12.x/Illuminate/Validation/Validator.html) | &nbsp; |
| Validator | [Illuminate\Validation\Factory](https://api.laravel.com/docs/12.x/Illuminate/Validation/Factory.html) | `validator` |
| View (인스턴스) | [Illuminate\View\View](https://api.laravel.com/docs/12.x/Illuminate/View/View.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://api.laravel.com/docs/12.x/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://api.laravel.com/docs/12.x/Illuminate/Foundation/Vite.html) | &nbsp; |

</div>