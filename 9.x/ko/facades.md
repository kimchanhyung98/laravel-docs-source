# 파사드(Facades)

- [소개](#introduction)
- [파사드를 언제 사용할까?](#when-to-use-facades)
    - [파사드 vs. 의존성 주입(Dependency Injection)](#facades-vs-dependency-injection)
    - [파사드 vs. 헬퍼 함수](#facades-vs-helper-functions)
- [파사드는 어떻게 동작할까?](#how-facades-work)
- [실시간 파사드(Real-Time Facades)](#real-time-facades)
- [파사드 클래스 레퍼런스](#facade-class-reference)

<a name="introduction"></a>
## 소개

Laravel 공식 문서 전체에서, 여러분은 Laravel의 다양한 기능에 "파사드(Facades)"를 통해 접근하는 코드 예시들을 자주 접할 수 있습니다. 파사드는 애플리케이션의 [서비스 컨테이너](/docs/{{version}}/container)에 등록된 클래스에 대한 "정적" 인터페이스를 제공합니다. Laravel에는 거의 모든 기능에 접근할 수 있도록 다양한 파사드가 내장되어 있습니다.

Laravel의 파사드는 서비스 컨테이너 내부의 클래스에 대한 "정적 프록시" 역할을 하므로, 기존의 정적 메소드들보다 더 높은 테스트 용이성과 유연성을 유지하면서도 간결하고 표현력 있는 문법을 제공합니다. 파사드의 동작 원리를 완전히 이해하지 못하더라도 사용에 지장이 없으니, 우선은 자연스럽게 따라오며 학습해도 괜찮습니다.

Laravel의 모든 파사드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 그래서 다음과 같이 파사드를 손쉽게 사용할 수 있습니다:

    use Illuminate\Support\Facades\Cache;
    use Illuminate\Support\Facades\Route;

    Route::get('/cache', function () {
        return Cache::get('key');
    });

공식 문서 내의 많은 예제가 프레임워크의 다양한 기능을 파사드를 활용하여 설명하고 있습니다.

<a name="helper-functions"></a>
#### 헬퍼 함수(Helper Functions)

파사드를 보완하기 위해 Laravel은 전역 "헬퍼 함수"도 다양하게 제공합니다. 헬퍼 함수들은 Laravel의 주요 기능과 상호작용할 때 더욱 쉽게 사용할 수 있도록 해줍니다. 자주 쓰이는 헬퍼 함수로는 `view`, `response`, `url`, `config` 등이 있습니다. 각 헬퍼 함수는 관련 기능 문서에서 따로 설명되어 있지만, 모든 헬퍼 함수의 전체 목록은 [헬퍼 함수 문서](/docs/{{version}}/helpers)에서 확인할 수 있습니다.

예를 들어, JSON 응답을 생성할 때 `Illuminate\Support\Facades\Response` 파사드 대신, `response` 함수를 사용할 수 있습니다. 헬퍼 함수는 전역적으로 사용할 수 있기 때문에 클래스 임포트가 필요 없습니다.

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

<a name="when-to-use-facades"></a>
## 파사드를 언제 사용할까?

파사드는 많은 장점을 갖습니다. 직접 클래스를 주입하거나 수동으로 설정하지 않아도 Laravel의 다양한 기능을 간결하고 기억하기 쉬운 문법으로 사용할 수 있습니다. 또한 PHP의 동적 메소드 특성 덕분에 테스트하기 쉬운 장점도 있습니다.

하지만 파사드를 사용할 때 주의할 점도 있습니다. 가장 큰 위험은 클래스의 "스코프 크리프(scope creep)", 즉 범위가 과도하게 확장되는 현상입니다. 파사드는 너무 사용이 쉽고, 의존성 주입 없이 바로 사용 가능하기 때문에 한 클래스 안에서 너무 많은 파사드를 사용할 수 있습니다. 반면, 의존성을 주입하면 생성자가 커지는 것을 보면서 해당 클래스가 지나치게 커졌음을 인지할 수 있습니다. 따라서 파사드를 사용할 때에는 클래스의 크기를 자주 확인하면서, 역할이 너무 넓어지지 않도록 신경 써야 합니다. 만약 클래스가 너무 커진다면 여러 개의 소규모 클래스로 분리하는 것을 고려하세요.

<a name="facades-vs-dependency-injection"></a>
### 파사드 vs. 의존성 주입(Dependency Injection)

의존성 주입의 가장 큰 장점 중 하나는 주입된 클래스의 구현체를 손쉽게 교체할 수 있다는 점입니다. 이 덕분에 테스트 시에는 스텁이나 목(Mock) 객체를 주입해서, 특정 메소드가 제대로 호출되는지 쉽게 검증할 수 있습니다.

전통적으로, 완전히 정적(static) 클래스 메소드는 목 객체로 대체하기가 어렵습니다. 그러나 파사드는 동적 메소드 호출을 통해 서비스 컨테이너에서 객체를 받아오므로, 실제 인스턴스를 주입한 것과 동일하게 테스트할 수 있습니다. 예를 들어, 아래와 같은 라우트를 보겠습니다:

    use Illuminate\Support\Facades\Cache;

    Route::get('/cache', function () {
        return Cache::get('key');
    });

Laravel의 파사드 테스트 기능을 사용해, 우리가 원하는 인자를 `Cache::get` 메소드에 전달했는지 다음과 같이 검증할 수 있습니다:

    use Illuminate\Support\Facades\Cache;

    /**
     * 기본 기능 테스트 예시.
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

<a name="facades-vs-helper-functions"></a>
### 파사드 vs. 헬퍼 함수

파사드 외에도, Laravel에는 뷰 생성, 이벤트 발생, 작업 디스패치, HTTP 응답 전송 등의 다양한 일반 작업을 수행하는 "헬퍼 함수"가 있습니다. 이런 헬퍼 함수 중 상당수가 파사드와 동일한 역할을 합니다. 예를 들면 다음과 같습니다:

    return Illuminate\Support\Facades\View::make('profile');

    return view('profile');

파사드와 헬퍼 함수 사이에는 실질적인 차이가 없습니다. 헬퍼 함수를 사용할 때에도 파사드와 똑같이 테스트할 수 있습니다. 예를 들어, 아래 라우트 코드를 보세요:

    Route::get('/cache', function () {
        return cache('key');
    });

`cache` 헬퍼 함수는 내부적으로 `Cache` 파사드가 사용하는 클래스의 `get` 메소드를 호출합니다. 따라서 헬퍼 함수를 사용할 때에도 다음과 같이 해당 메소드가 올바른 인자로 호출되었는지 테스트할 수 있습니다:

    use Illuminate\Support\Facades\Cache;

    /**
     * 기본 기능 테스트 예시.
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

<a name="how-facades-work"></a>
## 파사드는 어떻게 동작할까?

Laravel 애플리케이션에서 파사드는 서비스 컨테이너에 바인딩된 객체에 접근하는 클래스를 의미합니다. 이 메커니즘은 `Facade` 클래스에 구현되어 있습니다. Laravel의 내장 및 사용자 정의 파사드는 기본적으로 `Illuminate\Support\Facades\Facade` 클래스를 확장(extends)합니다.

`Facade`의 베이스 클래스는 `__callStatic()` 매직 메소드를 활용하여, 파사드에서 호출된 메소드를 서비스 컨테이너에서 해석된 실제 객체로 위임합니다. 아래 예시에서, Laravel 캐시 시스템에 접근하는 로직을 보겠습니다. 이 코드를 보면, 마치 `Cache` 클래스의 정적 `get` 메소드가 호출되는 듯 보입니다:

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

파일 상단에서 `Cache` 파사드를 임포트(import)한 것을 볼 수 있습니다. 이 파사드는 실제로 내부적으로 `Illuminate\Contracts\Cache\Factory` 인터페이스의 구현체에 대한 접근을 중개합니다. 즉, 파사드를 통해 메소드를 호출하면 해당 요청이 Laravel 캐시 서비스의 실제 인스턴스로 전달됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 살펴보면 `get`이라는 정적 메소드가 없는 것을 알 수 있습니다:

    class Cache extends Facade
    {
        /**
         * 컴포넌트의 등록된 이름을 얻습니다.
         *
         * @return string
         */
        protected static function getFacadeAccessor() { return 'cache'; }
    }

즉, `Cache` 파사드는 기본 `Facade` 클래스를 상속받아 `getFacadeAccessor()` 메소드만 정의합니다. 이 메소드는 서비스 컨테이너 바인딩의 이름을 반환합니다. 사용자가 `Cache` 파사드의 정적 메소드를 호출하면, Laravel은 [서비스 컨테이너](/docs/{{version}}/container)에서 해당 바인딩(`cache`)을 해석해 실제 객체의 요청된 메소드를 실행합니다.

<a name="real-time-facades"></a>
## 실시간 파사드(Real-Time Facades)

실시간 파사드를 사용하면, 애플리케이션 내 아무 클래스이든 마치 파사드처럼 사용할 수 있습니다. 이를 설명하기 위해, 우선 실시간 파사드를 사용하지 않은 코드 예시를 보겠습니다. 예를 들어, `Podcast` 모델에 `publish`라는 메소드가 있다고 가정해봅시다. 그런데 이 메소드는 팟캐스트를 퍼블리시하려면 `Publisher` 인스턴스를 주입받아야 합니다:

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

메소드에 퍼블리셔 구현체를 주입하면 독립적으로 테스트가 용이해집니다. 하지만 `publish`를 호출할 때마다 매번 퍼블리셔 인스턴스를 넘겨줘야 한다는 번거로움이 있습니다. 실시간 파사드를 사용하면, 테스트 용이성은 그대로 유지하면서도 퍼블리셔 인스턴스를 직접 넘길 필요가 없습니다. 실시간 파사드를 생성하려면, 임포트하는 클래스의 네임스페이스 앞에 `Facades`를 붙이기만 하면 됩니다:

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

실시간 파사드가 사용되면, 해당 인터페이스/클래스명에서 `Facades` 접두어 뒤의 부분을 사용해 서비스 컨테이너에서 구현체를 찾아 자동으로 해석해줍니다. 테스트 시에는 Laravel의 내장 파사드 테스트 기능을 활용하여 이 메소드 호출을 목(mock) 처리할 수 있습니다:

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

<a name="facade-class-reference"></a>
## 파사드 클래스 레퍼런스

아래 표는 각 파사드와 그에 대응하는 실제 클래스 목록입니다. 해당 파사드의 루트 API 문서를 빠르게 찾아볼 때 유용합니다. 또한, 해당되는 경우 [서비스 컨테이너 바인딩](/docs/{{version}}/container) 키도 함께 표기되어 있습니다.

| 파사드        | 실제 클래스 | 서비스 컨테이너 바인딩키 |
| ------------- | ------------- | ------------- |
| App  |  [Illuminate\Foundation\Application](https://laravel.com/api/{{version}}/Illuminate/Foundation/Application.html)  |  `app` |
| Artisan  |  [Illuminate\Contracts\Console\Kernel](https://laravel.com/api/{{version}}/Illuminate/Contracts/Console/Kernel.html)  |  `artisan` |
| Auth  |  [Illuminate\Auth\AuthManager](https://laravel.com/api/{{version}}/Illuminate/Auth/AuthManager.html)  |  `auth` |
| Auth (인스턴스)  |  [Illuminate\Contracts\Auth\Guard](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Guard.html)  |  `auth.driver` |
| Blade  |  [Illuminate\View\Compilers\BladeCompiler](https://laravel.com/api/{{version}}/Illuminate/View/Compilers/BladeCompiler.html)  |  `blade.compiler` |
| Broadcast  |  [Illuminate\Contracts\Broadcasting\Factory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Broadcasting/Factory.html)  |    |
| Broadcast (인스턴스)  |  [Illuminate\Contracts\Broadcasting\Broadcaster](https://laravel.com/api/{{version}}/Illuminate/Contracts/Broadcasting/Broadcaster.html)  |    |
| Bus  |  [Illuminate\Contracts\Bus\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html)  |    |
| Cache  |  [Illuminate\Cache\CacheManager](https://laravel.com/api/{{version}}/Illuminate/Cache/CacheManager.html)  |  `cache` |
| Cache (인스턴스)  |  [Illuminate\Cache\Repository](https://laravel.com/api/{{version}}/Illuminate/Cache/Repository.html)  |  `cache.store` |
| Config  |  [Illuminate\Config\Repository](https://laravel.com/api/{{version}}/Illuminate/Config/Repository.html)  |  `config` |
| Cookie  |  [Illuminate\Cookie\CookieJar](https://laravel.com/api/{{version}}/Illuminate/Cookie/CookieJar.html)  |  `cookie` |
| Crypt  |  [Illuminate\Encryption\Encrypter](https://laravel.com/api/{{version}}/Illuminate/Encryption/Encrypter.html)  |  `encrypter` |
| Date  |  [Illuminate\Support\DateFactory](https://laravel.com/api/{{version}}/Illuminate/Support/DateFactory.html)  |  `date` |
| DB  |  [Illuminate\Database\DatabaseManager](https://laravel.com/api/{{version}}/Illuminate/Database/DatabaseManager.html)  |  `db` |
| DB (인스턴스)  |  [Illuminate\Database\Connection](https://laravel.com/api/{{version}}/Illuminate/Database/Connection.html)  |  `db.connection` |
| Event  |  [Illuminate\Events\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Events/Dispatcher.html)  |  `events` |
| File  |  [Illuminate\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Filesystem/Filesystem.html)  |  `files` |
| Gate  |  [Illuminate\Contracts\Auth\Access\Gate](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Access/Gate.html)  |    |
| Hash  |  [Illuminate\Contracts\Hashing\Hasher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Hashing/Hasher.html)  |  `hash` |
| Http  |  [Illuminate\Http\Client\Factory](https://laravel.com/api/{{version}}/Illuminate/Http/Client/Factory.html)  |    |
| Lang  |  [Illuminate\Translation\Translator](https://laravel.com/api/{{version}}/Illuminate/Translation/Translator.html)  |  `translator` |
| Log  |  [Illuminate\Log\LogManager](https://laravel.com/api/{{version}}/Illuminate/Log/LogManager.html)  |  `log` |
| Mail  |  [Illuminate\Mail\Mailer](https://laravel.com/api/{{version}}/Illuminate/Mail/Mailer.html)  |  `mailer` |
| Notification  |  [Illuminate\Notifications\ChannelManager](https://laravel.com/api/{{version}}/Illuminate/Notifications/ChannelManager.html)  |    |
| Password  |  [Illuminate\Auth\Passwords\PasswordBrokerManager](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBrokerManager.html)  |  `auth.password` |
| Password (인스턴스)  |  [Illuminate\Auth\Passwords\PasswordBroker](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBroker.html)  |  `auth.password.broker` |
| Queue  |  [Illuminate\Queue\QueueManager](https://laravel.com/api/{{version}}/Illuminate/Queue/QueueManager.html)  |  `queue` |
| Queue (인스턴스)  |  [Illuminate\Contracts\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Contracts/Queue/Queue.html)  |  `queue.connection` |
| Queue (기본 클래스)  |  [Illuminate\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Queue/Queue.html)  |    |
| Redirect  |  [Illuminate\Routing\Redirector](https://laravel.com/api/{{version}}/Illuminate/Routing/Redirector.html)  |  `redirect` |
| Redis  |  [Illuminate\Redis\RedisManager](https://laravel.com/api/{{version}}/Illuminate/Redis/RedisManager.html)  |  `redis` |
| Redis (인스턴스)  |  [Illuminate\Redis\Connections\Connection](https://laravel.com/api/{{version}}/Illuminate/Redis/Connections/Connection.html)  |  `redis.connection` |
| Request  |  [Illuminate\Http\Request](https://laravel.com/api/{{version}}/Illuminate/Http/Request.html)  |  `request` |
| Response  |  [Illuminate\Contracts\Routing\ResponseFactory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html)  |    |
| Response (인스턴스)  |  [Illuminate\Http\Response](https://laravel.com/api/{{version}}/Illuminate/Http/Response.html)  |    |
| Route  |  [Illuminate\Routing\Router](https://laravel.com/api/{{version}}/Illuminate/Routing/Router.html)  |  `router` |
| Schema  |  [Illuminate\Database\Schema\Builder](https://laravel.com/api/{{version}}/Illuminate/Database/Schema/Builder.html)  |    |
| Session  |  [Illuminate\Session\SessionManager](https://laravel.com/api/{{version}}/Illuminate/Session/SessionManager.html)  |  `session` |
| Session (인스턴스)  |  [Illuminate\Session\Store](https://laravel.com/api/{{version}}/Illuminate/Session/Store.html)  |  `session.store` |
| Storage  |  [Illuminate\Filesystem\FilesystemManager](https://laravel.com/api/{{version}}/Illuminate/Filesystem/FilesystemManager.html)  |  `filesystem` |
| Storage (인스턴스)  |  [Illuminate\Contracts\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Contracts/Filesystem/Filesystem.html)  |  `filesystem.disk` |
| URL  |  [Illuminate\Routing\UrlGenerator](https://laravel.com/api/{{version}}/Illuminate/Routing/UrlGenerator.html)  |  `url` |
| Validator  |  [Illuminate\Validation\Factory](https://laravel.com/api/{{version}}/Illuminate/Validation/Factory.html)  |  `validator` |
| Validator (인스턴스)  |  [Illuminate\Validation\Validator](https://laravel.com/api/{{version}}/Illuminate/Validation/Validator.html)  |    |
| View  |  [Illuminate\View\Factory](https://laravel.com/api/{{version}}/Illuminate/View/Factory.html)  |  `view` |
| View (인스턴스)  |  [Illuminate\View\View](https://laravel.com/api/{{version}}/Illuminate/View/View.html)  |    |
| Vite  |  [Illuminate\Foundation\Vite](https://laravel.com/api/{{version}}/Illuminate/Foundation/Vite.html)  |    |