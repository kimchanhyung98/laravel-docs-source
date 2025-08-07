# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [제로 구성 해상 (Zero Configuration Resolution)](#zero-configuration-resolution)
    - [컨테이너 활용 시점](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스와 구현체 바인딩](#binding-interfaces-to-implementations)
    - [컨텍스트 바인딩](#contextual-binding)
    - [컨텍스트 속성](#contextual-attributes)
    - [원시값 바인딩](#binding-primitives)
    - [타입이 지정된 가변 인수 바인딩](#binding-typed-variadics)
    - [태깅](#tagging)
    - [바인딩 확장](#extending-bindings)
- [해결하기](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 주입](#automatic-injection)
- [메서드 호출과 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
    - [리바인딩](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 서비스 컨테이너는 클래스 간의 의존성을 관리하고, 의존성 주입(dependency injection)을 수행하는 강력한 도구입니다. 의존성 주입이란 어려운 용어처럼 보이지만, 사실 클래스의 의존성을 생성자나 경우에 따라 "setter" 메서드를 통해 클래스 안으로 "주입"한다는 뜻입니다.

아래의 간단한 예시를 살펴보세요:

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;
use Illuminate\View\View;

class PodcastController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * Show information about the given podcast.
     */
    public function show(string $id): View
    {
        return view('podcasts.show', [
            'podcast' => $this->apple->findPodcast($id)
        ]);
    }
}
```

이 예시에서 `PodcastController`는 Apple Music과 같은 데이터 소스에서 팟캐스트 정보를 얻어와야 합니다. 그래서 팟캐스트 정보를 조회할 수 있는 서비스를 **주입**받게 됩니다. 서비스가 주입되어 있기 때문에, 애플리케이션을 테스트할 때 `AppleMusic` 서비스의 목(mock) 또는 더미 구현체를 쉽게 만들 수 있습니다.

Laravel 서비스 컨테이너에 대한 깊은 이해는 강력하고 대규모 애플리케이션을 구축하거나 Laravel 코어에 직접 기여할 때 매우 중요합니다.

<a name="zero-configuration-resolution"></a>
### 제로 구성 해상 (Zero Configuration Resolution)

클래스가 별도의 의존성이 없거나, 오직 다른 구체 클래스(인터페이스가 아닌)만을 의존한다면, 컨테이너에 별도의 설정 없이도 해당 클래스를 바로 해석할 수 있습니다. 예를 들어, 다음과 같은 코드를 `routes/web.php`에 작성할 수 있습니다:

```php
<?php

class Service
{
    // ...
}

Route::get('/', function (Service $service) {
    dd($service::class);
});
```

이 예시에서는 애플리케이션의 `/` 경로로 접근하면 `Service` 클래스가 자동으로 해석되어 해당 경로의 콜백에 주입됩니다. 이 기능 덕분에 설정 파일을 복잡하게 다루지 않고도 의존성 주입의 이점을 누릴 수 있습니다.

이처럼 Laravel에서 애플리케이션을 개발할 때 직접 작성하는 클래스 대부분은 컨테이너를 통해 자동으로 의존성을 받게 됩니다. [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등도 모두 자동으로 주입을 받을 수 있습니다. 또한 [큐 작업](/docs/12.x/queues)의 `handle` 메서드에서도 의존성 타입 힌팅이 가능합니다. 이렇게 자동적이고 제로 구성의 의존성 주입을 한번 경험하면, 이를 빼고 개발하기 어려워질 정도로 매우 편리합니다.

<a name="when-to-use-the-container"></a>
### 컨테이너 활용 시점 (When to Utilize the Container)

제로 구성 해상(Zero Configuration Resolution) 덕분에, 라우트, 컨트롤러, 이벤트 리스너 등에서 타입 힌팅만으로도 의존성을 주입받을 수 있으며, 직접 컨테이너를 다루지 않아도 됩니다. 예를 들어, 아래처럼 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입 힌트로 선언하면 현재 요청 객체에 간편히 접근할 수 있습니다. 이 코드를 작성할 때 컨테이너를 직접 다룰 필요는 없지만, 실제로는 컨테이너가 뒤에서 필요한 의존성을 관리하고 주입해줍니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

대부분의 경우, 자동 의존성 주입과 [파사드](/docs/12.x/facades)를 사용하면 컨테이너에서 직접 바인딩하거나 해석할 일 없이도 Laravel 애플리케이션을 만들 수 있습니다.  
**그렇다면, 언제 직접 컨테이너를 다뤄야 할까요?** 두 가지 경우가 있습니다.

첫째, 어떤 클래스가 인터페이스를 구현하고 그 인터페이스를 라우트나 클래스 생성자에 타입 힌트로 지정하고자 할 때, [컨테이너에게 해당 인터페이스를 어떻게 해석할지 알려주어야 합니다](#binding-interfaces-to-implementations).  
둘째, 다른 Laravel 개발자들과 공유하고자 하는 [패키지](/docs/12.x/packages)를 작성할 때, 패키지 내부의 서비스를 컨테이너에 바인딩해야 할 수도 있습니다.

<a name="binding"></a>
## 바인딩 (Binding)

<a name="binding-basics"></a>
### 바인딩 기본 (Binding Basics)

<a name="simple-bindings"></a>
#### 단순 바인딩 (Simple Bindings)

대부분의 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/12.x/providers)에서 등록하게 됩니다. 아래 예시들도 대부분 이 컨텍스트에서 컨테이너를 어떻게 활용하는지 보여줍니다.

서비스 프로바이더 내에서는 항상 `$this->app` 프로퍼티를 통해 컨테이너에 접근할 수 있습니다. 바인딩을 등록할 때는 `bind` 메서드를 사용해서, 등록하고자 하는 클래스나 인터페이스 이름과 인스턴스를 반환하는 클로저를 전달하면 됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

이 때, 해석기에 컨테이너 자체가 인수로 주입됩니다. 이걸 활용해 의존성을 갖는 객체의 하위 의존성까지 컨테이너를 통해 해석할 수 있습니다.

앞서 언급했듯이, 주로 서비스 프로바이더 내에서 컨테이너를 다루겠지만, 필요하다면 서비스 프로바이더 외부에서는 `App` [파사드](/docs/12.x/facades)를 사용해 동일하게 바인딩 및 해석 작업을 할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

이미 해당 타입에 대한 바인딩이 등록되어 있지 않은 경우에만 바인딩을 등록하고 싶다면 `bindIf` 메서드를 사용할 수 있습니다.

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

편의를 위해, `bind` 메서드에 클로저의 반환 타입으로 바인딩하려는 클래스나 인터페이스를 지정하면, 인수를 생략하여 Laravel이 자동으로 타입을 추론하도록 할 수도 있습니다.

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 클래스가 별도의 인터페이스에 의존하지 않는다면, 컨테이너에 바인딩할 필요가 없습니다. 컨테이너는 리플렉션을 통해 이러한 객체들을 자동으로 해석할 수 있으므로 별도의 지시가 필요 없습니다.

<a name="binding-a-singleton"></a>
#### 싱글턴 바인딩 (Binding A Singleton)

`singleton` 메서드는 클래스나 인터페이스를 컨테이너에 한 번만 해석되도록 바인딩합니다. 싱글턴 바인딩이 처음 해석된 후, 이후 컨테이너에서 해당 타입을 요청하면 항상 같은 인스턴스를 반환합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`singletonIf` 메서드를 사용하면, 해당 타입에 대한 싱글턴 바인딩이 등록되어 있지 않은 경우에만 바인딩을 등록할 수 있습니다.

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

또는, 인터페이스나 클래스에 `#[Singleton]` 속성을 지정해서, 컨테이너가 해당 타입을 한 번만 해석하도록 할 수도 있습니다.

```php
<?php

namespace App\Services;

use Illuminate\Container\Attributes\Singleton;

#[Singleton]
class Transistor
{
    // ...
}
```

<a name="binding-scoped"></a>
#### 범위 싱글턴 바인딩 (Binding Scoped Singletons)

`scoped` 메서드는 클래스나 인터페이스를 컨테이너에 라라벨의 한 요청/잡 라이프사이클 동안 한 번만 해석하도록 바인딩합니다. `singleton`와 비슷하지만, `scoped`로 등록된 인스턴스는 [Laravel Octane](/docs/12.x/octane) 워커가 새 요청을 처리하거나 [큐 워커](/docs/12.x/queues)가 새 작업을 처리할 때마다 초기화되어, 라이프사이클이 새로 시작될 때마다 인스턴스가 새로 생성됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`scopedIf` 메서드를 사용하면, 이미 바인딩이 등록되어 있지 않은 경우에만 범위 싱글턴 바인딩을 등록할 수 있습니다.

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

또한, 인터페이스나 클래스에 `#[Scoped]` 속성을 지정하면 해당 타입이 각 요청/잡 라이프사이클에서 한 번만 해석되도록 지정할 수 있습니다.

```php
<?php

namespace App\Services;

use Illuminate\Container\Attributes\Scoped;

#[Scoped]
class Transistor
{
    // ...
}
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩 (Binding Instances)

이미 생성된 객체 인스턴스를 `instance` 메서드로 컨테이너에 바인딩할 수도 있습니다. 이렇게 등록하면, 이후 해당 타입의 해석 요청마다 항상 동일한 객체 인스턴스를 반환합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스와 구현체 바인딩 (Binding Interfaces to Implementations)

서비스 컨테이너의 가장 강력한 기능 중 하나는, 인터페이스를 특정 구현체와 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher` 인터페이스와 이를 구현한 `RedisEventPusher`가 있다고 가정해봅시다. `RedisEventPusher`를 구현한 후 아래와 같이 서비스 컨테이너에 등록할 수 있습니다.

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이렇게 하면, 컨테이너가 `EventPusher` 타입이 필요한 클래스를 해석할 때마다 `RedisEventPusher`가 주입됩니다. 즉, 컨테이너로 해석되는 클래스의 생성자에 인터페이스를 타입 힌트로 지정하면 그 구현체가 자동으로 주입됩니다. (컨트롤러, 이벤트 리스너, 미들웨어 등 다양한 클래스타입이 항상 컨테이너로 해석됩니다.)

```php
use App\Contracts\EventPusher;

/**
 * Create a new class instance.
 */
public function __construct(
    protected EventPusher $pusher,
) {}
```

<a name="bind-attributes"></a>
#### 바인드 속성 (Bind Attributes)

Laravel은 더욱 편리하게 바인딩할 수 있도록 `Bind` 속성을 제공합니다. 이 속성을 어떤 인터페이스에 지정하면, 해당 인터페이스가 필요할 때 Laravel이 자동으로 지정한 구현체를 주입해줍니다. 이 방식은 서비스 프로바이더에 별도로 등록할 필요가 없습니다.

여러 개의 `Bind` 속성을 한 인터페이스에 적용해서, 환경별로 다른 구현체를 주입하도록 구성할 수도 있습니다.

```php
<?php

namespace App\Contracts;

use App\Services\FakeEventPusher;
use App\Services\RedisEventPusher;
use Illuminate\Container\Attributes\Bind;

#[Bind(RedisEventPusher::class)]
#[Bind(FakeEventPusher::class, environments: ['local', 'testing'])]
interface EventPusher
{
    // ...
}
```

더불어, `Singleton` 및 `Scoped` 속성을 함께 지정하여 컨테이너 바인딩이 한 번만, 또는 요청/잡 라이프사이클당 한 번만 해석되도록 표시할 수 있습니다.

```php
use App\Services\RedisEventPusher;
use Illuminate\Container\Attributes\Bind;
use Illuminate\Container\Attributes\Singleton;

#[Bind(RedisEventPusher::class)]
#[Singleton]
interface EventPusher
{
    // ...
}
```

<a name="contextual-binding"></a>
### 컨텍스트 바인딩 (Contextual Binding)

같은 인터페이스를 사용하는 두 클래스가 있지만 각기 다른 구현체를 주입하고 싶을 때가 있습니다. 예를 들어, 두 개의 컨트롤러가 각각 다른 `Illuminate\Contracts\Filesystem\Filesystem` [컨트랙트](/docs/12.x/contracts) 구현체에 의존한다면 아래와 같이 정의할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\UploadController;
use App\Http\Controllers\VideoController;
use Illuminate\Contracts\Filesystem\Filesystem;
use Illuminate\Support\Facades\Storage;

$this->app->when(PhotoController::class)
    ->needs(Filesystem::class)
    ->give(function () {
        return Storage::disk('local');
    });

$this->app->when([VideoController::class, UploadController::class])
    ->needs(Filesystem::class)
    ->give(function () {
        return Storage::disk('s3');
    });
```

<a name="contextual-attributes"></a>
### 컨텍스트 속성 (Contextual Attributes)

컨텍스트 바인딩은 보통 드라이버 구현체나 설정 값 등의 구현을 주입할 때 많이 사용되기 때문에, Laravel은 이런 값들을 직접 서비스 프로바이더에서 바인딩하지 않고도 손쉽게 주입할 수 있도록 여러 컨텍스트 바인딩 속성을 제공합니다.

예를 들어, `Storage` 속성은 특정 [스토리지 디스크](/docs/12.x/filesystem)를 주입할 수 있게 해줍니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Container\Attributes\Storage;
use Illuminate\Contracts\Filesystem\Filesystem;

class PhotoController extends Controller
{
    public function __construct(
        #[Storage('local')] protected Filesystem $filesystem
    ) {
        // ...
    }
}
```

`Storage` 속성 외에도, Laravel은 `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RouteParameter`, [Tag](#tagging) 등의 속성을 제공합니다.

```php
<?php

namespace App\Http\Controllers;

use App\Contracts\UserRepository;
use App\Models\Photo;
use App\Repositories\DatabaseRepository;
use Illuminate\Container\Attributes\Auth;
use Illuminate\Container\Attributes\Cache;
use Illuminate\Container\Attributes\Config;
use Illuminate\Container\Attributes\Context;
use Illuminate\Container\Attributes\DB;
use Illuminate\Container\Attributes\Give;
use Illuminate\Container\Attributes\Log;
use Illuminate\Container\Attributes\RouteParameter;
use Illuminate\Container\Attributes\Tag;
use Illuminate\Contracts\Auth\Guard;
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Database\Connection;
use Psr\Log\LoggerInterface;

class PhotoController extends Controller
{
    public function __construct(
        #[Auth('web')] protected Guard $auth,
        #[Cache('redis')] protected Repository $cache,
        #[Config('app.timezone')] protected string $timezone,
        #[Context('uuid')] protected string $uuid,
        #[Context('ulid', hidden: true)] protected string $ulid,
        #[DB('mysql')] protected Connection $connection,
        #[Give(DatabaseRepository::class)] protected UserRepository $users,
        #[Log('daily')] protected LoggerInterface $log,
        #[RouteParameter('photo')] protected Photo $photo,
        #[Tag('reports')] protected iterable $reports,
    ) {
        // ...
    }
}
```

또한, 현재 인증된 사용자를 라우트나 클래스에 주입할 수 있도록 `CurrentUser` 속성도 제공합니다.

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 커스텀 속성 정의 (Defining Custom Attributes)

`Illuminate\Contracts\Container\ContextualAttribute` 컨트랙트를 구현하여 자신만의 컨텍스트 속성을 만들 수 있습니다. 컨테이너는 속성의 `resolve` 메서드를 호출해, 해당 속성을 활용하는 클래스에 어떤 값을 주입할지 결정합니다. 아래는 기본 제공되는 `Config` 속성을 직접 구현한 예시입니다.

```php
<?php

namespace App\Attributes;

use Attribute;
use Illuminate\Contracts\Container\Container;
use Illuminate\Contracts\Container\ContextualAttribute;

#[Attribute(Attribute::TARGET_PARAMETER)]
class Config implements ContextualAttribute
{
    /**
     * Create a new attribute instance.
     */
    public function __construct(public string $key, public mixed $default = null)
    {
    }

    /**
     * Resolve the configuration value.
     *
     * @param  self  $attribute
     * @param  \Illuminate\Contracts\Container\Container  $container
     * @return mixed
     */
    public static function resolve(self $attribute, Container $container)
    {
        return $container->make('config')->get($attribute->key, $attribute->default);
    }
}
```

<a name="binding-primitives"></a>
### 원시값 바인딩 (Binding Primitives)

어떤 클래스는 주입받는 클래스뿐만 아니라 정수 등과 같은 원시값(primitive)도 함께 필요할 때가 있습니다. 컨텍스트 바인딩을 사용하면 클래스가 필요로 하는 어떠한 값도 쉽게 주입할 수 있습니다.

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

어떤 클래스가 [태그](#tagging)된 인스턴스 배열에 의존한다면, `giveTagged` 메서드를 사용해 해당 태그로 바인딩된 모든 객체를 한 번에 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션의 설정 파일에서 값을 주입해야 한다면 `giveConfig` 메서드를 사용할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입이 지정된 가변 인수 바인딩 (Binding Typed Variadics)

가끔 클래스 생성자에서 배열 형태의 객체를 가변 인수(variadic)로 받는 경우가 있습니다.

```php
<?php

use App\Models\Filter;
use App\Services\Logger;

class Firewall
{
    /**
     * The filter instances.
     *
     * @var array
     */
    protected $filters;

    /**
     * Create a new class instance.
     */
    public function __construct(
        protected Logger $logger,
        Filter ...$filters,
    ) {
        $this->filters = $filters;
    }
}
```

이 경우 컨텍스트 바인딩의 `give` 메서드에 `Filter` 인스턴스들을 배열로 반환하는 클로저를 넘겨 해석할 수 있습니다.

```php
$this->app->when(Firewall::class)
    ->needs(Filter::class)
    ->give(function (Application $app) {
          return [
              $app->make(NullFilter::class),
              $app->make(ProfanityFilter::class),
              $app->make(TooLongFilter::class),
          ];
    });
```

편의를 위해, 클래스 배열만 전달해서 `Firewall`이 `Filter` 인스턴스들을 필요로 할 때 각각 컨테이너가 자동으로 해석하도록 할 수도 있습니다.

```php
$this->app->when(Firewall::class)
    ->needs(Filter::class)
    ->give([
        NullFilter::class,
        ProfanityFilter::class,
        TooLongFilter::class,
    ]);
```

<a name="variadic-tag-dependencies"></a>
#### 가변 태그형 의존성 (Variadic Tag Dependencies)

클래스에 타입이 지정된 가변 인수(예: `Report ...$reports`)가 필요할 수도 있습니다. 이런 경우에도 `needs`와 `giveTagged` 메서드를 함께 사용해 해당 [태그](#tagging)가 붙은 모든 바인딩을 쉽게 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅 (Tagging)

종종 특정 "카테고리"의 모든 바인딩을 한 번에 해석해야 할 수도 있습니다. 예를 들어, 여러 종류의 `Report` 인터페이스 구현체 배열을 받아서 처리하는 리포트 분석기를 만드는 경우, 각각의 `Report` 구현을 등록한 뒤 `tag` 메서드로 태그를 지정할 수 있습니다.

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

태그가 지정된 서비스는 컨테이너의 `tagged` 메서드를 통해 한 번에 모두 해석할 수 있습니다.

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장 (Extending Bindings)

`extend` 메서드를 이용하면 해석된 서비스를 수정할 수 있습니다. 예를 들어, 어떤 서비스가 해석될 때 추가 코드로 장식(decorate)하거나 설정을 변경하고 싶을 때 사용합니다. `extend`는 확장할 서비스 클래스와 수정을 적용할 클로저를 받으며, 이 클로저에는 해석된 서비스 인스턴스와 컨테이너가 제공됩니다.

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해결하기 (Resolving)

<a name="the-make-method"></a>
### `make` 메서드 (The `make` Method)

컨테이너에서 클래스 인스턴스를 해석하려면 `make` 메서드를 사용합니다. 이 메서드에는 해석하고자 하는 클래스나 인터페이스 이름을 전달합니다.

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스의 의존성 중 일부가 컨테이너로는 해석할 수 없는 값(예: 식별자 등)일 경우, `makeWith` 메서드로 연관 배열을 전달해 직접 주입할 수 있습니다. 예를 들어, `Transistor` 서비스가 `$id` 생성자 인수가 필요하다면 아래와 같이 사용할 수 있습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드를 사용하면 특정 클래스나 인터페이스가 컨테이너에 명시적으로 바인딩되어 있는지 확인할 수 있습니다.

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

만약 서비스 프로바이더 외부나 `$app` 변수가 없는 코드에서 인스턴스를 해석해야 한다면, `App` [파사드](/docs/12.x/facades)나 `app` [헬퍼](/docs/12.x/helpers#method-app)를 사용할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

클래스 생성자에서 Laravel 컨테이너 자체를 주입받고 싶다면, `Illuminate\Container\Container` 클래스를 타입 힌트로 선언하면 됩니다.

```php
use Illuminate\Container\Container;

/**
 * Create a new class instance.
 */
public function __construct(
    protected Container $container,
) {}
```

<a name="automatic-injection"></a>
### 자동 주입 (Automatic Injection)

또한 매우 중요한 점으로, 컨테이너로 해석되는 클래스의 생성자(예: [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등)에 의존성을 타입 힌트로 지정하면 이를 자동으로 해석해 주입해줍니다. [큐 작업](/docs/12.x/queues)의 `handle` 메서드에서도 동일하게 의존성을 타입 힌트할 수 있습니다. 실제로 대부분의 객체는 이런 방식으로 해석하여 사용하는 것이 권장됩니다.

아래는 애플리케이션에서 정의한 서비스를 컨트롤러 생성자에 타입 힌트로 지정한 예시입니다. 해당 서비스는 자동으로 해석되어 클래스에 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;

class PodcastController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * Show information about the given podcast.
     */
    public function show(string $id): Podcast
    {
        return $this->apple->findPodcast($id);
    }
}
```

<a name="method-invocation-and-injection"></a>
## 메서드 호출과 주입 (Method Invocation and Injection)

가끔 인스턴스의 메서드를 호출하면서, 컨테이너가 해당 메서드의 의존성을 자동으로 주입해주길 원할 수도 있습니다. 다음과 같은 클래스를 예로 들어보겠습니다.

```php
<?php

namespace App;

use App\Services\AppleMusic;

class PodcastStats
{
    /**
     * Generate a new podcast stats report.
     */
    public function generate(AppleMusic $apple): array
    {
        return [
            // ...
        ];
    }
}
```

아래와 같이 컨테이너를 이용해 `generate` 메서드를 호출할 수 있습니다.

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 어떠한 PHP 콜러블(callable)도 받을 수 있습니다. 심지어, 클로저도 컨테이너를 통해 의존성을 자동 주입하며 실행할 수 있습니다.

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트 (Container Events)

서비스 컨테이너는 객체를 해석할 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 통해 이 이벤트를 감지할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입 객체가 해석될 때마다 호출...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 모든 타입의 객체가 해석될 때마다 호출...
});
```

이처럼, 해석되는 객체가 콜백으로 전달되기 때문에, 객체가 실제 소비자에게 전달되기 전에 필요한 추가 설정을 미리 할 수 있습니다.

<a name="rebinding"></a>
### 리바인딩 (Rebinding)

`rebinding` 메서드는 서비스가 컨테이너에 다시 바인딩되거나(초기 바인딩 후 재등록 또는 오버라이드 등) 할 때마다 이벤트를 감지할 수 있게 해줍니다.  
특정 바인딩이 변경될 때마다 의존성을 갱신하거나 동작을 수정해야 할 때 활용할 수 있습니다.

```php
use App\Contracts\PodcastPublisher;
use App\Services\SpotifyPublisher;
use App\Services\TransistorPublisher;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(PodcastPublisher::class, SpotifyPublisher::class);

$this->app->rebinding(
    PodcastPublisher::class,
    function (Application $app, PodcastPublisher $newInstance) {
        //
    },
);

// 새로운 바인딩이 등록되면 리바인딩 콜백이 호출됨...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

Laravel의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다.  
따라서, PSR-11 컨테이너 인터페이스를 타입 힌트로 지정해 Laravel 컨테이너 인스턴스를 직접 주입받을 수 있습니다.

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

만약 해당 식별자(identifier)를 해석할 수 없다면 예외가 발생합니다.  
등록된 적이 없으면 `Psr\Container\NotFoundExceptionInterface` 예외가,  
바인딩은 되어 있으나 해석이 실패하면 `Psr\Container\ContainerExceptionInterface` 예외가 각각 발생합니다.
