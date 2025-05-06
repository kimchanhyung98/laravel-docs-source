# 파사드(Facade)

- [소개](#introduction)
- [파사드를 언제 사용해야 할까?](#when-to-use-facades)
    - [파사드 vs 의존성 주입](#facades-vs-dependency-injection)
    - [파사드 vs 헬퍼 함수](#facades-vs-helper-functions)
- [파사드는 어떻게 동작하나](#how-facades-work)
- [실시간(Real-Time) 파사드](#real-time-facades)
- [파사드 클래스 레퍼런스](#facade-class-reference)

<a name="introduction"></a>
## 소개

라라벨 공식 문서 전체에서, "파사드"를 통해 라라벨의 다양한 기능과 상호작용하는 코드 예제를 많이 볼 수 있습니다. 파사드는 애플리케이션의 [서비스 컨테이너](/docs/{{version}}/container)에 등록된 클래스에 대해 "정적" 인터페이스를 제공합니다. 라라벨은 거의 모든 라라벨 기능에 접근할 수 있도록 다양한 파사드를 기본적으로 제공합니다.

라라벨 파사드는 서비스 컨테이너에 존재하는 클래스에 대한 "정적 프록시" 역할을 하며, 간결하고 표현력 있는 문법의 이점을 제공하는 동시에 전통적인 정적 메서드보다 더 뛰어난 테스트 가능성과 유연성을 유지합니다. 파사드가 내부적으로 어떻게 동작하는지 완벽히 이해하지 못해도 괜찮습니다. 부담 가지지 말고 계속해서 라라벨을 학습해 보세요.

라라벨의 모든 파사드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 따라서 아래와 같이 쉽게 파사드에 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

라라벨 공식 문서의 많은 예제들은 프레임워크의 다양한 기능을 설명할 때 파사드를 사용합니다.

<a name="helper-functions"></a>
#### 헬퍼 함수

파사드를 보완하기 위해, 라라벨은 다양한 전역 "헬퍼 함수"를 제공하여 자주 사용하는 라라벨 기능을 훨씬 더 쉽게 사용할 수 있도록 해줍니다. 대표적인 헬퍼 함수로는 `view`, `response`, `url`, `config` 등이 있습니다. 각 헬퍼 함수는 관련된 기능 문서에서 따로 설명되지만, 모든 함수의 전체 목록은 [헬퍼 문서](/docs/{{version}}/helpers)에서 확인할 수 있습니다.

예를 들어, JSON 응답을 생성하기 위해 `Illuminate\Support\Facades\Response` 파사드를 사용하는 대신, 단순히 `response` 함수를 사용할 수도 있습니다. 헬퍼 함수는 전역적으로 사용할 수 있으므로 클래스 임포트가 필요하지 않습니다.

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

파사드는 다양한 이점을 제공합니다. 간결하고 기억하기 쉬운 문법 덕분에, 복잡한 클래스 이름이나 별도의 주입 또는 수동 설정 없이도 라라벨의 기능을 쉽게 사용할 수 있습니다. 또한 PHP의 동적 메서드를 활용하는 독특한 방식으로 구현되어 있어 테스트도 용이합니다.

그러나 파사드를 사용할 때 주의할 점도 있습니다. 대표적인 문제는 클래스 "스코프의 확장(scope creep)"입니다. 파사드는 너무 사용하기 쉬워서, 별다른 주입 과정이 필요 없으니 하나의 클래스에서 여러 파사드를 마구 사용하며, 클래스가 비대해지기 쉽습니다. 반면 의존성 주입을 사용할 경우, 생성자가 커지면 클래스가 너무 크다는 시각적인 피드백을 얻지만, 파사드는 그렇지 않습니다. 따라서 파사드를 사용할 때는 클래스의 책임 범위가 지나치게 넓어지지 않도록 특별히 주의해야 합니다. 클래스가 너무 커진다면 작은 클래스로 분리하는 것을 고려해보세요.

<a name="facades-vs-dependency-injection"></a>
### 파사드 vs 의존성 주입

의존성 주입(Dependency Injection)의 주요 이점 중 하나는, 주입한 클래스의 구현체를 쉽게 교체할 수 있다는 점입니다. 이는 테스트 중에 모킹(Mock)이나 스텁(Stub)을 주입해서 특정 메서드가 제대로 호출되었는지 확인하는 데 매우 유용합니다.

전통적인 정적 클래스 메서드는 모킹이나 스텁을 적용하기 어렵습니다. 하지만 파사드는 동적 메서드를 사용해 서비스 컨테이너에서 객체를 프록시하므로, 실제로 파사드를 의존성 주입 클래스와 동일하게 테스트할 수 있습니다. 예를 들어, 아래와 같은 라우트가 있다고 가정해봅시다.

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

라라벨의 파사드 테스트 메서드를 이용하면, 아래와 같이 `Cache::get` 메서드가 기대한 인자로 실제로 호출되었는지 검사하는 테스트를 작성할 수 있습니다.

```php
use Illuminate\Support\Facades\Cache;

/**
 * 기본 기능 테스트 예시
 *
 * @return void
 */
public function testBasicExample()
{
    Cache::shouldReceive('get')
         ->with('key')
         ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a name="facades-vs-helper-functions"></a>
### 파사드 vs 헬퍼 함수

파사드 외에도, 라라벨은 뷰 생성, 이벤트 발생, 작업 디스패치, HTTP 응답 전송 등 자주 사용하는 작업을 위한 다양한 "헬퍼" 함수를 제공합니다. 이들 헬퍼 함수의 많은 부분이 대응되는 파사드와 동일한 기능을 수행합니다. 예를 들어, 아래 두 코드는 완전히 동일하게 동작합니다.

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

실제로 파사드와 헬퍼 함수 사이에 실질적인 차이는 전혀 없습니다. 헬퍼 함수를 사용할 때도, 동일하게 파사드와 같이 테스트 할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있다고 해봅시다.

```php
Route::get('/cache', function () {
    return cache('key');
});
```

내부적으로 `cache` 헬퍼는 `Cache` 파사드의 기본 클래스에 있는 `get` 메서드를 호출합니다. 따라서, 헬퍼 함수로 사용하더라도 아래와 같이 실제로 메서드가 기대한 인자로 호출되었는지 확인하는 테스트를 작성할 수 있습니다.

```php
use Illuminate\Support\Facades\Cache;

/**
 * 기본 기능 테스트 예시
 *
 * @return void
 */
public function testBasicExample()
{
    Cache::shouldReceive('get')
         ->with('key')
         ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a name="how-facades-work"></a>
## 파사드는 어떻게 동작하나

라라벨 애플리케이션에서 파사드는 컨테이너의 객체에 접근할 수 있도록 해주는 클래스입니다. 이 기능을 구현하는 핵심은 `Facade` 클래스에 있습니다. 라라벨의 파사드나, 직접 만드는 커스텀 파사드는 모두 기본 `Illuminate\Support\Facades\Facade` 클래스를 확장합니다.

`Facade` 기본 클래스는 `__callStatic()` 매직 메서드를 사용하여, 여러분이 파사드에서 호출한 메서드를 컨테이너에서 실제 객체로 위임합니다. 아래 예제를 보시면, 라라벨의 캐시 시스템에 호출을 하고 있습니다. 코드를 보면 마치 `Cache` 클래스의 정적 메서드인 `get`이 호출되는 것처럼 보일 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 주어진 유저의 프로필을 표시합니다.
     *
     * @param  int  $id
     * @return Response
     */
    public function showProfile($id)
    {
        $user = Cache::get('user:'.$id);

        return view('profile', ['user' => $user]);
    }
}
```

파일 상단에서 `Cache` 파사드를 "임포트"하고 있다는 점을 주목하세요. 이 파사드는 실제로 `Illuminate\Contracts\Cache\Factory` 인터페이스의 구현체에 접근할 수 있는 프록시 역할을 합니다. 해당 파사드를 통해 메서드를 호출하면 컨테이너에 있는 실제 라라벨 캐시 서비스 인스턴스에 메서드가 전달됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 살펴보면, 정적 메서드 `get`이 실제로 구현되어 있지 않다는 것을 알 수 있습니다.

```php
class Cache extends Facade
{
    /**
     * 컴포넌트의 등록된 이름을 반환합니다.
     *
     * @return string
     */
    protected static function getFacadeAccessor() { return 'cache'; }
}
```

대신, `Cache` 파사드는 기본 `Facade` 클래스를 상속받아 `getFacadeAccessor()` 메서드를 구현합니다. 이 메서드는 서비스 컨테이너 바인딩의 이름을 반환하는 역할을 합니다. 사용자가 `Cache` 파사드에서 어떤 정적 메서드를 호출하면, 라라벨은 [서비스 컨테이너](/docs/{{version}}/container)에서 해당 바인딩(`cache`)을 찾아 객체를 반환하고, 요청된 메서드(`get`)를 해당 객체에서 실행합니다.

<a name="real-time-facades"></a>
## 실시간(Real-Time) 파사드

실시간(real-time) 파사드를 사용하면, 애플리케이션 내의 모든 클래스를 파사드처럼 사용할 수 있습니다. 어떻게 사용하는지 보기 위해, 우선 실시간 파사드를 사용하지 않은 코드를 살펴봅시다. 예를 들어, 우리가 가진 `Podcast` 모델에 `publish` 메서드가 있다고 가정합시다. 하지만 팟캐스트 발행을 위해서는 `Publisher` 인스턴스를 주입받아야 합니다.

```php
<?php

namespace App\Models;

use App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * 팟캐스트를 발행합니다.
     *
     * @param  Publisher  $publisher
     * @return void
     */
    public function publish(Publisher $publisher)
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this);
    }
}
```

메서드에 퍼블리셔 구현체를 주입하면, 퍼블리셔를 모킹하여 메서드를 독립적으로 쉽게 테스트할 수 있습니다. 그러나, 매번 `publish` 메서드를 호출할 때마다 퍼블리셔 인스턴스를 전달해야 한다는 번거로움이 있습니다. 실시간 파사드를 사용하면, 동일한 테스트 가능성을 유지하면서도 퍼블리셔 인스턴스를 명시적으로 전달할 필요가 없습니다. 실시간 파사드를 생성하려면, 임포트한 클래스의 네임스페이스 앞에 `Facades` 접두사를 붙이면 됩니다.

```php
<?php

namespace App\Models;

use Facades\App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * 팟캐스트를 발행합니다.
     *
     * @return void
     */
    public function publish()
    {
        $this->update(['publishing' => now()]);

        Publisher::publish($this);
    }
}
```

실시간 파사드를 사용할 경우, 퍼블리셔 구현체는 네임스페이스에서 `Facades` 접두사 이후의 인터페이스/클래스 이름 부분을 이용해 서비스 컨테이너에서 가져옵니다. 테스트를 진행할 때는 라라벨이 제공하는 내장 파사드 테스트 헬퍼를 사용해서 메서드 호출을 모킹할 수 있습니다.

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
     * 테스트 예시
     *
     * @return void
     */
    public function test_podcast_can_be_published()
    {
        $podcast = Podcast::factory()->create();

        Publisher::shouldReceive('publish')->once()->with($podcast);

        $podcast->publish();
    }
}
```

<a name="facade-class-reference"></a>
## 파사드 클래스 레퍼런스

아래 표는 각 파사드와 그에 연결된 실제 클래스, 그리고 (해당되는 경우) [서비스 컨테이너 바인딩](/docs/{{version}}/container) 키를 나열합니다. 각 파사드가 어떤 클래스에 연결되어 있는지 빠르게 API 문서를 확인할 때 유용합니다.

| 파사드(Facade) | 클래스(Class) | 서비스 컨테이너 바인딩 |
|---------|-------------------|---------------------|
| App | [Illuminate\Foundation\Application](https://laravel.com/api/{{version}}/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://laravel.com/api/{{version}}/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| Auth | [Illuminate\Auth\AuthManager](https://laravel.com/api/{{version}}/Illuminate/Auth/AuthManager.html) | `auth` |
| Auth (Instance) | [Illuminate\Contracts\Auth\Guard](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://laravel.com/api/{{version}}/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| Broadcast (Instance) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://laravel.com/api/{{version}}/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Bus | [Illuminate\Contracts\Bus\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| Cache | [Illuminate\Cache\CacheManager](https://laravel.com/api/{{version}}/Illuminate/Cache/CacheManager.html) | `cache` |
| Cache (Instance) | [Illuminate\Cache\Repository](https://laravel.com/api/{{version}}/Illuminate/Cache/Repository.html) | `cache.store` |
| Config | [Illuminate\Config\Repository](https://laravel.com/api/{{version}}/Illuminate/Config/Repository.html) | `config` |
| Cookie | [Illuminate\Cookie\CookieJar](https://laravel.com/api/{{version}}/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://laravel.com/api/{{version}}/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date | [Illuminate\Support\DateFactory](https://laravel.com/api/{{version}}/Illuminate/Support/DateFactory.html) | `date` |
| DB | [Illuminate\Database\DatabaseManager](https://laravel.com/api/{{version}}/Illuminate/Database/DatabaseManager.html) | `db` |
| DB (Instance) | [Illuminate\Database\Connection](https://laravel.com/api/{{version}}/Illuminate/Database/Connection.html) | `db.connection` |
| Event | [Illuminate\Events\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Events/Dispatcher.html) | `events` |
| File | [Illuminate\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate | [Illuminate\Contracts\Auth\Access\Gate](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| Hash | [Illuminate\Contracts\Hashing\Hasher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http | [Illuminate\Http\Client\Factory](https://laravel.com/api/{{version}}/Illuminate/Http/Client/Factory.html) | &nbsp; |
| Lang | [Illuminate\Translation\Translator](https://laravel.com/api/{{version}}/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://laravel.com/api/{{version}}/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://laravel.com/api/{{version}}/Illuminate/Mail/Mailer.html) | `mailer` |
| Notification | [Illuminate\Notifications\ChannelManager](https://laravel.com/api/{{version}}/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Password (Instance) | [Illuminate\Auth\Passwords\PasswordBroker](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Queue | [Illuminate\Queue\QueueManager](https://laravel.com/api/{{version}}/Illuminate/Queue/QueueManager.html) | `queue` |
| Queue (Instance) | [Illuminate\Contracts\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue (Base Class) | [Illuminate\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Queue/Queue.html) | &nbsp; |
| Redirect | [Illuminate\Routing\Redirector](https://laravel.com/api/{{version}}/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis | [Illuminate\Redis\RedisManager](https://laravel.com/api/{{version}}/Illuminate/Redis/RedisManager.html) | `redis` |
| Redis (Instance) | [Illuminate\Redis\Connections\Connection](https://laravel.com/api/{{version}}/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Request | [Illuminate\Http\Request](https://laravel.com/api/{{version}}/Illuminate/Http/Request.html) | `request` |
| Response | [Illuminate\Contracts\Routing\ResponseFactory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Response (Instance) | [Illuminate\Http\Response](https://laravel.com/api/{{version}}/Illuminate/Http/Response.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://laravel.com/api/{{version}}/Illuminate/Routing/Router.html) | `router` |
| Schema | [Illuminate\Database\Schema\Builder](https://laravel.com/api/{{version}}/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| Session | [Illuminate\Session\SessionManager](https://laravel.com/api/{{version}}/Illuminate/Session/SessionManager.html) | `session` |
| Session (Instance) | [Illuminate\Session\Store](https://laravel.com/api/{{version}}/Illuminate/Session/Store.html) | `session.store` |
| Storage | [Illuminate\Filesystem\FilesystemManager](https://laravel.com/api/{{version}}/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| Storage (Instance) | [Illuminate\Contracts\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| URL | [Illuminate\Routing\UrlGenerator](https://laravel.com/api/{{version}}/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator | [Illuminate\Validation\Factory](https://laravel.com/api/{{version}}/Illuminate/Validation/Factory.html) | `validator` |
| Validator (Instance) | [Illuminate\Validation\Validator](https://laravel.com/api/{{version}}/Illuminate/Validation/Validator.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://laravel.com/api/{{version}}/Illuminate/View/Factory.html) | `view` |
| View (Instance) | [Illuminate\View\View](https://laravel.com/api/{{version}}/Illuminate/View/View.html) | &nbsp; |