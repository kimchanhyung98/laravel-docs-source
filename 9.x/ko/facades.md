# 페이시드 (Facades)

- [소개](#introduction)
- [페이시드를 언제 사용하나요?](#when-to-use-facades)
    - [페이시드와 의존성 주입 비교](#facades-vs-dependency-injection)
    - [페이시드와 헬퍼 함수 비교](#facades-vs-helper-functions)
- [페이시드 작동 원리](#how-facades-work)
- [실시간 페이시드 (Real-Time Facades)](#real-time-facades)
- [페이시드 클래스 참조](#facade-class-reference)

<a name="introduction"></a>
## 소개 (Introduction)

라라벨 문서 전반에서 "페이시드(facades)"를 통해 라라벨의 기능들과 상호작용하는 예제 코드를 자주 보게 됩니다. 페이시드는 애플리케이션의 [서비스 컨테이너](/docs/9.x/container)에 등록된 클래스에 대해 "정적(static)" 인터페이스를 제공합니다. 라라벨은 거의 모든 기능에 접근할 수 있도록 다양한 페이시드를 기본 제공하고 있습니다.

라라벨 페이시드는 서비스 컨테이너 내부의 클래스에 대해 "정적 프록시" 역할을 하며, 전통적인 정적 메서드보다 더 유연하고 테스트하기 쉬운, 간결하고 표현력 있는 문법을 제공합니다. 페이시드가 어떻게 동작하는지 완벽히 이해하지 못해도 괜찮으니, 라라벨 학습을 계속 진행하면서 자연스럽게 익혀가면 됩니다.

라라벨의 모든 페이시드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 따라서 페이시드 사용은 아래처럼 간단합니다:

```
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

라라벨 문서 내 많은 예제에서 프레임워크의 다양한 기능을 보여주기 위해 페이시드를 활용합니다.

<a name="helper-functions"></a>
#### 헬퍼 함수 (Helper Functions)

페이시드를 보완하기 위해 라라벨은 다양한 전역 "헬퍼 함수"도 제공합니다. 이를 통해 자주 쓰이는 라라벨 기능에 훨씬 쉽게 접근할 수 있습니다. 자주 사용하는 헬퍼 함수의 예로는 `view`, `response`, `url`, `config` 등이 있습니다. 각 헬퍼 함수는 대응하는 기능과 함께 문서화되어 있으며, 전체 목록은 [헬퍼 함수 문서](/docs/9.x/helpers)에서 확인할 수 있습니다.

예를 들어, JSON 응답을 생성하려고 할 때 `Illuminate\Support\Facades\Response` 페이시드 대신 `response` 헬퍼 함수를 사용할 수도 있습니다. 헬퍼 함수는 전역적으로 사용 가능하기 때문에 별도로 클래스를 임포트할 필요가 없습니다:

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
## 페이시드를 언제 사용하나요? (When To Use Facades)

페이시드는 여러 가지 장점이 있습니다. 긴 클래스명을 기억하지 않고도 라라벨 기능을 사용할 수 있게 하는 간결하고 기억하기 쉬운 문법을 제공합니다. 또한, PHP의 동적 메서드 사용 덕분에 테스트하기도 수월합니다.

하지만 페이시드를 사용할 때는 주의가 필요합니다. 주요 위험은 클래스의 "범위 확장(scope creep)"입니다. 페이시드는 사용하기 쉽고 의존성 주입을 요구하지 않기 때문에, 하나의 클래스에 너무 많은 페이시드를 남용하며 클래스가 지나치게 비대해질 수 있습니다. 의존성 주입을 사용하면, 생성자에 많은 인수들이 나타나 클래스가 커지는 것이 눈에 보이기에 이를 자연스럽게 경계할 수 있습니다. 따라서 페이시드를 사용할 때는 클래스가 담당하는 책임의 범위를 좁게 유지하는 데 주의를 기울이세요. 만약 클래스가 너무 커지면 여러 개의 작은 클래스로 분리하는 것을 고려해야 합니다.

<a name="facades-vs-dependency-injection"></a>
### 페이시드와 의존성 주입 비교 (Facades Vs. Dependency Injection)

의존성 주입의 주요 장점 중 하나는 주입하는 클래스의 구현체를 쉽게 교체할 수 있다는 점입니다. 테스트 시에는 목(mock)이나 스텁(stub)을 주입하여 특정 메서드들이 호출되었는지 확인할 수 있어 매우 유용합니다.

일반적으로 진정한 정적 메서드는 모킹하거나 스텁 처리하기 어렵습니다. 그러나 페이시드는 서비스 컨테이너에서 객체를 동적으로 찾아내어 메서드 호출을 전달하는 동적 메서드를 이용하기 때문에, 실제로는 주입된 클래스 인스턴스를 테스트하듯 페이시드도 테스트할 수 있습니다. 예를 들어, 아래 라우트를 살펴보세요:

```
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

라라벨의 페이시드 테스트 메서드를 사용해 다음과 같은 테스트를 작성하여 `Cache::get` 메서드가 예상 인수로 호출되었는지 확인할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;

/**
 * 기본적인 기능 테스트 예제입니다.
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
### 페이시드와 헬퍼 함수 비교 (Facades Vs. Helper Functions)

페이시드 외에도 라라벨은 뷰 생성, 이벤트 호출, 작업 디스패치, HTTP 응답 전송과 같은 일반 작업을 수행하는 여러 "헬퍼 함수"를 포함합니다. 많은 헬퍼 함수는 대응하는 페이시드와 동일한 기능을 합니다. 예를 들어 다음 두 코드는 같습니다:

```
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

페이시드와 헬퍼 함수는 실질적으로 아무 차이가 없습니다. 헬퍼 함수도 대응하는 페이시드와 같은 방식으로 테스트할 수 있습니다. 예를 들어, 다음 라우트가 있다고 가정해 보죠:

```
Route::get('/cache', function () {
    return cache('key');
});
```

`cache` 헬퍼는 `Cache` 페이시드에 대응하는 클래스의 `get` 메서드를 호출합니다. 따라서 헬퍼 함수를 사용하더라도, 아래 테스트처럼 메서드가 예상 인수로 호출되었는지 확인할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;

/**
 * 기본적인 기능 테스트 예제입니다.
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
## 페이시드 작동 원리 (How Facades Work)

라라벨 애플리케이션에서 페이시드는 서비스 컨테이너로부터 객체에 접근할 수 있게 해주는 클래스입니다. 이 동작을 가능하게 하는 핵심은 `Facade` 클래스에 있습니다. 라라벨의 기본 페이시드와 직접 만든 커스텀 페이시드는 모두 `Illuminate\Support\Facades\Facade` 기본 클래스를 상속받습니다.

`Facade` 기본 클래스는 `__callStatic()` 매직 메서드를 이용해, 페이시드에 대한 호출을 컨테이너에서 해석한 객체로 연기(delegate)합니다. 아래 예제에서 Laravel 캐시 시스템을 호출하고 있습니다. 이 코드를 보면 마치 `Cache` 클래스의 정적 `get` 메서드를 호출하는 것처럼 보일 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 보여줍니다.
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

파일 상단에서 `Cache` 페이시드를 임포트한 것을 확인할 수 있습니다. 이 페이시드는 `Illuminate\Contracts\Cache\Factory` 인터페이스의 실제 구현체에 접근하는 프록시 역할을 합니다. 페이시드를 통해 호출하는 모든 메서드는 라라벨 캐시 서비스의 실제 인스턴스에 전달됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 보면, 실제로 `get`이라는 정적 메서드는 존재하지 않습니다:

```
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

이 클래스는 기본 `Facade` 클래스를 상속하며 `getFacadeAccessor()` 메서드를 정의하고 있습니다. 이 메서드는 서비스 컨테이너에 바인딩된 키 이름을 반환합니다. 사용자가 `Cache` 페이시드의 정적 메서드를 호출하면 라라벨은 `cache`라는 이름의 바인딩을 서비스 컨테이너에서 찾아 해당 객체에 메서드 호출(이 경우 `get`)을 실행합니다.

<a name="real-time-facades"></a>
## 실시간 페이시드 (Real-Time Facades)

실시간 페이시드를 사용하면, 애플리케이션의 어떤 클래스든 페이시드처럼 다룰 수 있습니다. 이를 설명하기 위해, 우선 실시간 페이시드를 사용하지 않는 코드를 살펴보겠습니다. 예를 들어, `Podcast` 모델이 `publish` 메서드를 가지고 있다고 합시다. 하지만 팟캐스트를 발행하려면 `Publisher` 인스턴스를 주입받아야 합니다:

```
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

메서드에 퍼블리셔 구현체를 주입받으면 쉽게 목(mock) 처리가 가능해 개별 메서드 테스트가 쉽습니다. 하지만 `publish` 메서드를 호출할 때마다 퍼블리셔 인스턴스를 반드시 전달해야 합니다. 실시간 페이시드를 활용하면 테스트 가능성을 유지하면서도 `Publisher` 인스턴스를 명시적으로 전달할 필요가 없습니다. 실시간 페이시드를 만들려면 임포트하는 클래스 네임스페이스 앞에 `Facades`를 붙이면 됩니다:

```
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

실시간 페이시드를 사용하면, 퍼블리셔 구현체는 자동으로 서비스 컨테이너에서 `Facades` 접두사 이후에 나오는 인터페이스 혹은 클래스 이름을 기준으로 찾아집니다. 테스트 시에는 라라벨 내장 페이시드 테스트 도구를 활용해 메서드 호출을 목 처리할 수 있습니다:

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
     * 테스트 예제입니다.
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
## 페이시드 클래스 참조 (Facade Class Reference)

아래는 대표적인 라라벨 페이시드와 그 기반 클래스, 그리고 해당 서비스 컨테이너 바인딩 키입니다. 특정 페이시드의 API 문서를 빠르게 확인하는 데 유용합니다.

| 페이시드 (Facade) | 클래스 (Class) | 서비스 컨테이너 바인딩 (Service Container Binding) |
|-------------|-------------|-------------|
| App  | [Illuminate\Foundation\Application](https://laravel.com/api/9.x/Illuminate/Foundation/Application.html) | `app` |
| Artisan  | [Illuminate\Contracts\Console\Kernel](https://laravel.com/api/9.x/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| Auth  | [Illuminate\Auth\AuthManager](https://laravel.com/api/9.x/Illuminate/Auth/AuthManager.html) | `auth` |
| Auth (인스턴스) | [Illuminate\Contracts\Auth\Guard](https://laravel.com/api/9.x/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Blade  | [Illuminate\View\Compilers\BladeCompiler](https://laravel.com/api/9.x/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast  | [Illuminate\Contracts\Broadcasting\Factory](https://laravel.com/api/9.x/Illuminate/Contracts/Broadcasting/Factory.html) |  |
| Broadcast (인스턴스) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://laravel.com/api/9.x/Illuminate/Contracts/Broadcasting/Broadcaster.html) |  |
| Bus  | [Illuminate\Contracts\Bus\Dispatcher](https://laravel.com/api/9.x/Illuminate/Contracts/Bus/Dispatcher.html) |  |
| Cache  | [Illuminate\Cache\CacheManager](https://laravel.com/api/9.x/Illuminate/Cache/CacheManager.html) | `cache` |
| Cache (인스턴스) | [Illuminate\Cache\Repository](https://laravel.com/api/9.x/Illuminate/Cache/Repository.html) | `cache.store` |
| Config  | [Illuminate\Config\Repository](https://laravel.com/api/9.x/Illuminate/Config/Repository.html) | `config` |
| Cookie  | [Illuminate\Cookie\CookieJar](https://laravel.com/api/9.x/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt  | [Illuminate\Encryption\Encrypter](https://laravel.com/api/9.x/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date  | [Illuminate\Support\DateFactory](https://laravel.com/api/9.x/Illuminate/Support/DateFactory.html) | `date` |
| DB  | [Illuminate\Database\DatabaseManager](https://laravel.com/api/9.x/Illuminate/Database/DatabaseManager.html) | `db` |
| DB (인스턴스) | [Illuminate\Database\Connection](https://laravel.com/api/9.x/Illuminate/Database/Connection.html) | `db.connection` |
| Event  | [Illuminate\Events\Dispatcher](https://laravel.com/api/9.x/Illuminate/Events/Dispatcher.html) | `events` |
| File  | [Illuminate\Filesystem\Filesystem](https://laravel.com/api/9.x/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate  | [Illuminate\Contracts\Auth\Access\Gate](https://laravel.com/api/9.x/Illuminate/Contracts/Auth/Access/Gate.html) |  |
| Hash  | [Illuminate\Contracts\Hashing\Hasher](https://laravel.com/api/9.x/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http  | [Illuminate\Http\Client\Factory](https://laravel.com/api/9.x/Illuminate/Http/Client/Factory.html) |  |
| Lang  | [Illuminate\Translation\Translator](https://laravel.com/api/9.x/Illuminate/Translation/Translator.html) | `translator` |
| Log  | [Illuminate\Log\LogManager](https://laravel.com/api/9.x/Illuminate/Log/LogManager.html) | `log` |
| Mail  | [Illuminate\Mail\Mailer](https://laravel.com/api/9.x/Illuminate/Mail/Mailer.html) | `mailer` |
| Notification  | [Illuminate\Notifications\ChannelManager](https://laravel.com/api/9.x/Illuminate/Notifications/ChannelManager.html) |  |
| Password  | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://laravel.com/api/9.x/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Password (인스턴스) | [Illuminate\Auth\Passwords\PasswordBroker](https://laravel.com/api/9.x/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Queue  | [Illuminate\Queue\QueueManager](https://laravel.com/api/9.x/Illuminate/Queue/QueueManager.html) | `queue` |
| Queue (인스턴스) | [Illuminate\Contracts\Queue\Queue](https://laravel.com/api/9.x/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue (기본 클래스) | [Illuminate\Queue\Queue](https://laravel.com/api/9.x/Illuminate/Queue/Queue.html) |  |
| Redirect  | [Illuminate\Routing\Redirector](https://laravel.com/api/9.x/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis  | [Illuminate\Redis\RedisManager](https://laravel.com/api/9.x/Illuminate/Redis/RedisManager.html) | `redis` |
| Redis (인스턴스) | [Illuminate\Redis\Connections\Connection](https://laravel.com/api/9.x/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Request  | [Illuminate\Http\Request](https://laravel.com/api/9.x/Illuminate/Http/Request.html) | `request` |
| Response  | [Illuminate\Contracts\Routing\ResponseFactory](https://laravel.com/api/9.x/Illuminate/Contracts/Routing/ResponseFactory.html) |  |
| Response (인스턴스) | [Illuminate\Http\Response](https://laravel.com/api/9.x/Illuminate/Http/Response.html) |  |
| Route  | [Illuminate\Routing\Router](https://laravel.com/api/9.x/Illuminate/Routing/Router.html) | `router` |
| Schema  | [Illuminate\Database\Schema\Builder](https://laravel.com/api/9.x/Illuminate/Database/Schema/Builder.html) |  |
| Session  | [Illuminate\Session\SessionManager](https://laravel.com/api/9.x/Illuminate/Session/SessionManager.html) | `session` |
| Session (인스턴스) | [Illuminate\Session\Store](https://laravel.com/api/9.x/Illuminate/Session/Store.html) | `session.store` |
| Storage  | [Illuminate\Filesystem\FilesystemManager](https://laravel.com/api/9.x/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| Storage (인스턴스) | [Illuminate\Contracts\Filesystem\Filesystem](https://laravel.com/api/9.x/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| URL  | [Illuminate\Routing\UrlGenerator](https://laravel.com/api/9.x/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator  | [Illuminate\Validation\Factory](https://laravel.com/api/9.x/Illuminate/Validation/Factory.html) | `validator` |
| Validator (인스턴스) | [Illuminate\Validation\Validator](https://laravel.com/api/9.x/Illuminate/Validation/Validator.html) |  |
| View  | [Illuminate\View\Factory](https://laravel.com/api/9.x/Illuminate/View/Factory.html) | `view` |
| View (인스턴스) | [Illuminate\View\View](https://laravel.com/api/9.x/Illuminate/View/View.html) |  |
| Vite  | [Illuminate\Foundation\Vite](https://laravel.com/api/9.x/Illuminate/Foundation/Vite.html) |  |