# 파사드 (Facades)

- [소개](#introduction)
- [파사드를 언제 사용할까](#when-to-use-facades)
    - [파사드와 의존성 주입 비교](#facades-vs-dependency-injection)
    - [파사드와 헬퍼 함수 비교](#facades-vs-helper-functions)
- [파사드는 어떻게 동작하는가](#how-facades-work)
- [실시간 파사드](#real-time-facades)
- [파사드 클래스 참조](#facade-class-reference)

<a name="introduction"></a>
## 소개 (Introduction)

라라벨 문서 전반에서 여러분은 "파사드(facades)"를 통해 라라벨의 기능과 상호작용하는 코드 예제를 많이 보게 됩니다. 파사드는 애플리케이션의 [서비스 컨테이너](/docs/{{version}}/container)에 등록된 클래스에 대해 "정적" 인터페이스를 제공합니다. 라라벨은 거의 모든 기능에 접근 가능한 다양한 파사드를 기본으로 제공합니다.

라라벨 파사드는 서비스 컨테이너 내의 실제 클래스를 대신하는 "정적 프록시" 역할을 수행합니다. 이를 통해 간결하고 표현력 있는 문법을 제공하면서도, 전통적인 정적 메서드보다 테스트 가능성과 유연성을 높이는 이점이 있습니다. 파사드가 내부적으로 어떻게 작동하는지 완전히 이해하지 못해도 괜찮으니, 편하게 따라오며 라라벨을 계속 학습하세요.

라라벨 파사드는 모두 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 따라서 다음과 같이 쉽게 파사드에 접근할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

라라벨 문서의 많은 예제에서 프레임워크 기능을 보여주기 위해 파사드가 사용됩니다.

<a name="helper-functions"></a>
#### 헬퍼 함수 (Helper Functions)

파사드를 보완하기 위해, 라라벨은 자주 사용하는 기능에 대해 전역에서 사용할 수 있는 다양한 헬퍼 함수를 제공합니다. 예를 들어 `view`, `response`, `url`, `config` 등이 자주 쓰이고, 각각 해당 기능에 맞는 문서가 있습니다. 모든 헬퍼 함수 목록은 전용 [헬퍼 문서](/docs/{{version}}/helpers)에서 확인할 수 있습니다.

예를 들어, JSON 응답을 생성할 때 `Illuminate\Support\Facades\Response` 파사드 대신 `response` 헬퍼 함수를 쓸 수 있습니다. 헬퍼 함수는 전역에서 바로 사용 가능하므로 별도의 클래스 import가 필요 없습니다:

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
## 파사드를 언제 사용할까 (When To Use Facades)

파사드는 여러 장점이 있습니다. 긴 클래스명을 주입하거나 직접 설정할 필요 없이 라라벨 기능을 간결하고 기억하기 쉬운 문법으로 사용할 수 있게 합니다. 또한 PHP의 동적 메서드 호출을 활용하기 때문에 테스트도 수월합니다.

하지만 파사드를 사용할 때는 주의가 필요합니다. 파사드는 너무 쉽게 사용할 수 있고 의존성 주입이 필요 없기 때문에, 한 클래스 내에서 여러 파사드를 무분별하게 사용해 클래스가 지나치게 커지는 "클래스 스코프 팽창(scope creep)" 문제가 생기기 쉽습니다. 의존성 주입을 사용하면 큰 생성자를 통해 클래스 크기가 커졌음을 시각적으로 인지하기 쉽지만, 파사드는 그렇지 않으니 클래스 크기와 책임범위가 넓어지지 않도록 신경 써야 합니다. 만약 너무 커진다면 클래스를 여러 개의 작은 클래스로 나누는 것을 고려하세요.

<a name="facades-vs-dependency-injection"></a>
### 파사드와 의존성 주입 비교 (Facades Vs. Dependency Injection)

의존성 주입의 주요 장점 중 하나는 주입받은 클래스 구현체를 쉽게 교체할 수 있다는 점입니다. 이는 테스트 시에 목(mock)이나 스텁(stub)을 주입하여 특정 메서드 호출 여부 등을 확인할 때 매우 유용합니다.

정말 정적(static) 메서드는 목(mock)이나 스텁으로 대체하기 어렵지만, 파사드는 동적 메서드 호출을 통해 서비스 컨테이너에서 객체를 받아 실제 메서드를 호출하므로, 주입받은 클래스 인스턴스를 테스트하는 것과 동일하게 파사드도 테스트할 수 있습니다. 예를 들어 다음과 같은 라우트가 있다고 합시다:

```
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

라라벨의 파사드 테스트 기능을 사용하면 `Cache::get` 메서드가 예상한 인수와 함께 호출되었는지 다음과 같이 테스트를 작성할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;

/**
 * 기본 기능 테스트 예제
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
### 파사드와 헬퍼 함수 비교 (Facades Vs. Helper Functions)

파사드 외에 라라벨은 뷰 생성, 이벤트 발생, 잡 배포, HTTP 응답 전송 같은 공통 작업을 수행하는 다양한 헬퍼 함수를 포함합니다. 많은 헬퍼 함수가 대응하는 파사드와 동일한 역할을 수행합니다. 예로 아래 두 코드는 동일한 결과를 만듭니다:

```
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

파사드와 헬퍼 함수는 실질적으로 차이가 없습니다. 헬퍼 함수를 사용할 때도 대응하는 파사드처럼 테스트할 수 있습니다. 예를 들어 다음 라우트가 있다고 합시다:

```
Route::get('/cache', function () {
    return cache('key');
});
```

`cache` 헬퍼는 내부적으로 `Cache` 파사드의 `get` 메서드를 호출합니다. 따라서 헬퍼 함수를 사용하더라도 다음과 같이 메서드 호출을 검증하는 테스트를 만들 수 있습니다:

```
use Illuminate\Support\Facades\Cache;

/**
 * 기본 기능 테스트 예제
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
## 파사드는 어떻게 동작하는가 (How Facades Work)

라라벨 애플리케이션에서 파사드는 컨테이너에 등록된 객체에 접근할 수 있도록 하는 클래스입니다. 이 동작의 핵심 코드는 `Facade` 클래스에 있습니다. 라라벨의 기본 파사드와 여러분이 새로 만드는 커스텀 파사드는 모두 기본 `Illuminate\Support\Facades\Facade` 클래스를 상속 받습니다.

`Facade` 기본 클래스는 `__callStatic()` 매직 메서드를 사용하여 파사드에서 호출된 정적 메서드를 서비스 컨테이너에서 꺼낸 실제 객체의 메서드 호출로 연기(defer)합니다. 아래 예제를 보면, 라라벨 캐시 시스템에 호출이 전달되는 모습을 볼 수 있습니다. 이 코드를 보면 마치 `Cache` 클래스의 정적 `get` 메서드를 호출하는 것처럼 보입니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 특정 사용자의 프로필을 보여줌
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

파일 상단에서 `Cache` 파사드를 import 한 것을 주목하세요. 이 파사드는 `Illuminate\Contracts\Cache\Factory` 인터페이스의 구현체에 접근하기 위한 프록시 역할을 합니다. 파사드를 통해 호출하는 모든 메서드는 실제로 라라벨 캐시 서비스의 인스턴스에 전달됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 살펴보면, `get`이라는 정적 메서드가 실제로 존재하지 않는 것을 알 수 있습니다:

```
class Cache extends Facade
{
    /**
     * 컴포넌트의 등록 이름을 반환
     *
     * @return string
     */
    protected static function getFacadeAccessor() { return 'cache'; }
}
```

`Cache` 파사드는 기본 `Facade` 클래스를 상속하고, `getFacadeAccessor()` 메서드를 정의하는데, 이 메서드는 서비스 컨테이너 바인딩 이름을 반환합니다. 사용자가 `Cache` 파사드의 어떤 정적 메서드를 호출하면 라라벨은 `cache` 바인딩에 해당하는 객체를 서비스 컨테이너에서 찾아내고, 그 객체의 요청된 메서드(여기서는 `get`)를 실행합니다.

<a name="real-time-facades"></a>
## 실시간 파사드 (Real-Time Facades)

실시간 파사드 기능을 사용하면, 애플리케이션 내 어떤 클래스든 마치 파사드처럼 사용할 수 있습니다. 이를 이해하기 위해 먼저 실시간 파사드를 사용하지 않는 코드를 보겠습니다. 예를 들어, `Podcast` 모델에 `publish` 메서드가 있다고 가정합시다. 하지만 방송을 발행하려면 `Publisher` 인스턴스를 메서드에 주입해야 합니다:

```
<?php

namespace App\Models;

use App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * 팟캐스트 발행
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

메서드에 퍼블리셔 구현체를 주입하는 것은 메서드를 분리해서 독립적으로 테스트하기 좋지만, 호출할 때마다 퍼블리셔 인스턴스를 넘겨줘야 한다는 불편이 있습니다. 실시간 파사드를 사용하면 테스트 가능성은 유지하면서도 퍼블리셔 인스턴스를 명시적으로 넘길 필요가 없게 됩니다. 실시간 파사드를 생성하려면 import 구문에서 클래스 네임스페이스 앞에 `Facades`를 붙이면 됩니다:

```
<?php

namespace App\Models;

use Facades\App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * 팟캐스트 발행
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

실시간 파사드를 사용하면, `Facades` 접두사 뒤에 있는 인터페이스나 클래스 이름을 기준으로 서비스 컨테이너에서 퍼블리셔 구현체가 자동으로 해결됩니다. 테스트 환경에서는 라라벨 내장 파사드 테스트 헬퍼를 사용해 메서드 호출을 목(mock)할 수 있습니다:

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
## 파사드 클래스 참조 (Facade Class Reference)

아래 표는 대표적인 각 파사드와 그 기반 클래스, 그리고 해당되는 서비스 컨테이너 바인딩 키를 보여줍니다. 파사드별 API 문서를 빠르게 탐색하는 데 유용합니다.

| Facade | Class | Service Container Binding |
| ------------- | ------------- | ------------- |
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