# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [제로 구성(Zero Configuration) 해결](#zero-configuration-resolution)
    - [컨테이너를 언제 활용해야 하는가](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기초](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [컨텍스트 바인딩](#contextual-binding)
    - [컨텍스트 속성](#contextual-attributes)
    - [원시값(Primitive) 바인딩](#binding-primitives)
    - [타입드 가변 인자(Variadic) 바인딩](#binding-typed-variadics)
    - [태깅(Tagging)](#tagging)
    - [바인딩 확장(Extending)](#extending-bindings)
- [해결(Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 의존성 주입(Automatic Injection)](#automatic-injection)
- [메서드 호출 및 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
    - [재바인딩(Rebinding)](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개

라라벨의 서비스 컨테이너는 클래스 간의 의존성을 관리하고 의존성 주입(Dependency Injection)을 구현할 수 있게 해 주는 강력한 도구입니다. 의존성 주입이란 기본적으로 클래스가 필요로 하는 의존성을 생성자 또는 경우에 따라 "세터(setter)" 메서드를 통해 외부에서 "주입"받는다는 의미입니다.

간단한 예제를 살펴보겠습니다.

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

위 예제에서 `PodcastController`는 Apple Music과 같은 데이터 소스에서 팟캐스트 정보를 조회할 필요가 있습니다. 이를 위해 팟캐스트를 가져올 수 있는 서비스를 **주입(Inject)** 받습니다. 이처럼 서비스를 주입받게 되면, 실제 테스트 환경에서는 실제 AppleMusic 서비스 대신 "모킹(mock)"하거나 임의로 동작하는 구현을 넣는 것도 간편하게 할 수 있습니다.

라라벨 서비스 컨테이너를 깊이 있게 이해하는 것은 규모가 크고 강력한 애플리케이션을 개발할 때는 물론, 라라벨 코어에 직접 기여하고 싶을 때도 필수적인 역량입니다.

<a name="zero-configuration-resolution"></a>
### 제로 구성(Zero Configuration) 해결

어떤 클래스가 의존성이 전혀 없거나, 혹은 순수한 구체 클래스(인터페이스가 아닌)만 의존하고 있다면, 컨테이너에 해당 클래스를 어떻게 생성해야 하는지 미리 알려줄 필요가 없습니다. 예를 들어 아래 코드를 `routes/web.php`에 추가해보겠습니다.

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

위 예시처럼 애플리케이션의 `/` 경로로 접근하면, `Service` 클래스가 자동으로 컨테이너에 의해 해결되어 해당 핸들러에 주입됩니다. 이는 전체적인 개발 방식에 큰 변화를 가져다줍니다. 별도의 복잡한 구성 파일 작성 없이, 의존성 주입을 최대한 활용하여 애플리케이션을 개발할 수 있게 됩니다.

다행히 라라벨 애플리케이션을 만들 때 여러분이 작성하는 많은 클래스(예: [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등)는 컨테이너를 통해 자동으로 필요한 의존성을 주입받게 됩니다. 또한, [큐 작업](/docs/12.x/queues)의 `handle` 메서드에도 타입힌트로 의존성을 명시할 수 있습니다. 한 번이라도 이러한 자동 의존성 주입을 경험하면, 별도의 구성 없이 개발하는 것이 얼마나 효율적인지 알게 될 것입니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 언제 활용해야 하는가

제로 구성 해결 덕분에 여러분은 대부분의 경우 별도의 서비스 컨테이너 코드를 직접 작성하지 않고도 라우트, 컨트롤러, 이벤트 리스너 등에서 타입힌트로 의존성을 선언할 수 있습니다. 예를 들어 아래처럼 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입힌트로 지정하면 현재 요청 정보를 손쉽게 사용할 수 있습니다. 비록 컨테이너와 직접 상호작용하지는 않지만, 실제로는 컨테이너가 이 의존성 주입 과정을 자동으로 처리해 줍니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

대부분 자동 의존성 주입과 [파사드(Facades)](/docs/12.x/facades)의 힘으로, 굳이 컨테이너에 무언가를 직접 바인딩하거나 해결(Resolve)하지 않고도 애플리케이션을 만들 수 있습니다. **그렇다면, 언제 직접 컨테이너에 명시적으로 접근해야 할까요?** 대표적인 두 가지 상황을 보겠습니다.

첫째, 여러분이 어떤 인터페이스를 구현하는 클래스를 만들고, 해당 인터페이스를 의존성으로 타입힌트하고 싶을 때는 [컨테이너에 인터페이스가 실제 어떤 클래스로 해결되어야 하는지](#binding-interfaces-to-implementations)를 반드시 알려주어야 합니다. 둘째, 여러분이 [라라벨 패키지](/docs/12.x/packages)를 만들어 공개하려는 경우, 패키지의 서비스를 컨테이너에 바인딩해야 할 필요가 있습니다.

<a name="binding"></a>
## 바인딩

<a name="binding-basics"></a>
### 바인딩 기초

<a name="simple-bindings"></a>
#### 기본 바인딩

대부분의 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/12.x/providers) 내부에 등록됩니다. 그래서 이 문서의 예시들도 주로 서비스 프로바이더 내에서 컨테이너를 사용하는 방법을 보여줍니다.

서비스 프로바이더에서는 항상 `$this->app` 속성을 통해서 컨테이너에 접근할 수 있습니다. 바인딩은 `bind` 메서드를 통해 등록하며, 바인딩할 클래스 또는 인터페이스명과 해당 클래스의 인스턴스를 반환하는 클로저를 인수로 넘깁니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

위 예시처럼, 리졸버(Resolver) 클로저는 컨테이너 자체를 인수로 받을 수 있으므로, 해당 개체의 하위 의존성(서브 의존성)도 컨테이너를 사용하여 해결할 수 있습니다.

앞서 말했듯이 보통은 서비스 프로바이더 내에서 컨테이너를 사용하겠지만, 꼭 서비스 프로바이더가 아니더라도 `App` [파사드](/docs/12.x/facades)를 이용하여 컨테이너에 접근할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

또한 `bindIf` 메서드를 통해 같은 타입에 대한 바인딩이 아직 등록되지 않은 경우에만 바인딩을 수행할 수 있습니다.

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

편의를 위해, 바인딩하려는 클래스 또는 인터페이스명을 별도의 인수로 넘기는 대신, `bind` 메서드에 반환형 타입이 지정된 클로저를 전달하여 라라벨이 타입을 추론하도록 할 수도 있습니다.

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 만약 클래스가 인터페이스에 의존하고 있지 않다면, 컨테이너에 해당 클래스를 굳이 바인딩할 필요가 없습니다. 컨테이너는 이러한 객체들을 리플렉션(reflection)을 이용해 자동으로 생성할 수 있기 때문입니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩

`singleton` 메서드는 클래스나 인터페이스를 컨테이너에 **한 번만** 생성할 수 있도록 바인딩합니다. 한 번 싱글톤 바인딩이 해결되면, 이후에는 항상 동일한 객체 인스턴스가 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`singletonIf` 메서드를 사용하면, 같은 타입에 대해 싱글톤 바인딩이 없을 때만 싱글톤 바인딩을 등록할 수 있습니다.

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 스코프드 싱글톤 바인딩

`scoped` 메서드는 특정 라라벨 요청 또는 작업(Job) 라이프사이클 동안 **한 번만** 인스턴스가 만들어지는 형식으로 바인딩합니다. 이 메서드는 `singleton`과 비슷하지만, [라라벨 Octane](/docs/12.x/octane)에서 워커가 새로운 요청을 처리하거나, 라라벨 [큐 워커](/docs/12.x/queues)가 새로운 작업을 처리할 때마다 인스턴스가 초기화되어 새롭게 생성된다는 차이점이 있습니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`scopedIf` 메서드는 동일한 타입에 대해 스코프드 바인딩이 존재하지 않을 때만 바인딩을 등록합니다.

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩

이미 만들어진 객체 인스턴스를 `instance` 메서드를 통해 컨테이너에 바인딩할 수도 있습니다. 이렇게 등록된 인스턴스는 동일한 타입에 대한 컨테이너의 모든 후속 요청에서도 항상 동일하게 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기

서비스 컨테이너의 매우 강력한 기능 중 하나는, 특정 인터페이스를 원하는 구현체(Implementation)로 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher`라는 인터페이스와 이를 구현하는 `RedisEventPusher` 클래스가 있다고 가정해 봅시다. 이제 해당 구현체를 아래처럼 바인딩할 수 있습니다.

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

위 코드는 컨테이너에게 만약 `EventPusher` 인터페이스가 필요한 상황에서는 `RedisEventPusher` 클래스를 대신 주입해달라고 알려줍니다. 이제 컨테이너가 해결하는 클래스의 생성자에서 인터페이스를 타입힌트로 선언하면 위에서 바인딩한 구현체가 자동으로 주입됩니다. (이때, 컨트롤러, 이벤트 리스너, 미들웨어 등 다양한 클래스들이 컨테이너에 의해 해결됨을 기억하세요.)

```php
use App\Contracts\EventPusher;

/**
 * Create a new class instance.
 */
public function __construct(
    protected EventPusher $pusher,
) {}
```

<a name="contextual-binding"></a>
### 컨텍스트 바인딩

경우에 따라서는 같은 인터페이스를 사용하는 두 개의 클래스가 각기 다른 구현체가 주입되기를 원할 수 있습니다. 예를 들어 두 컨트롤러가 각각 `Illuminate\Contracts\Filesystem\Filesystem` [컨트랙트](/docs/12.x/contracts)의 서로 다른 구현체를 필요로 할 수 있습니다. 라라벨에서는 이러한 요구를 아주 간단하고 유연하게 해결할 수 있습니다.

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
### 컨텍스트 속성

컨텍스트 바인딩은 주로 드라이버 인스턴스나 설정값을 주입할 때 많이 쓰입니다. 라라벨은 이러한 값을 직접 서비스 프로바이더에서 바인딩하지 않아도, 여러 가지 **컨텍스트 바인딩 속성(Attribute)**을 제공하여 좀 더 간편하게 주입할 수 있도록 합니다.

예를 들어, 특정 [스토리지 디스크](/docs/12.x/filesystem)를 주입해야 할 경우 `Storage` 속성을 사용할 수 있습니다.

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

`Storage` 외에도 라라벨은 `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RouteParameter`, 그리고 [Tag](#tagging) 속성을 제공합니다.

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

추가로, 현재 인증된 사용자를 특정 라우트나 클래스에 쉽게 주입할 수 있도록 `CurrentUser` 속성도 제공합니다.

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 커스텀 속성 정의하기

여러분은 `Illuminate\Contracts\Container\ContextualAttribute` 컨트랙트를 구현함으로써 자신만의 컨텍스트 속성을 만들 수도 있습니다. 컨테이너는 속성의 `resolve` 메서드를 호출하여 실제 주입될 값을 결정합니다. 아래는 라라벨 내장 `Config` 속성의 간소화된 구현 예시입니다.

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
### 원시값(Primitive) 바인딩

클래스가 다른 클래스 인스턴스뿐만 아니라, 정수값과 같은 원시 타입의 값까지 주입받아야 할 때가 있습니다. 이런 경우에도 컨텍스트 바인딩을 통해 손쉽게 원하는 값을 주입할 수 있습니다.

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

또한, 클래스가 [태깅](#tagging)된 인스턴스의 배열을 의존하고 있는 경우, `giveTagged` 메서드를 사용하면 같은 태그로 바인딩된 인스턴스들을 배열로 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

설정 파일(configuration)에서 값을 가져와서 주입해야 한다면 `giveConfig` 메서드를 사용할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입드 가변 인자(Variadic) 바인딩

가끔씩 생성자에 가변 개수의 객체(특정 타입)를 배열처럼 받는 경우가 있습니다.

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

이런 의존성도 컨텍스트 바인딩의 `give` 메서드에 배열을 반환하는 클로저를 넘김으로써 쉽게 해결할 수 있습니다.

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

간단하게 클래스명 배열을 넘겨서 해당 타입의 인스턴스들이 필요한 상황에서 자동으로 Resolve하여 주입하게 할 수도 있습니다.

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
#### 태그 기반 Variadic 의존성

클래스가 variadic 형식(예: `Report ...$reports`)으로 의존성을 선언한 경우, `needs`와 `giveTagged` 메서드를 통해 원하는 태그로 바인딩된 모든 객체를 일괄 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅(Tagging)

어떤 "분류"의 바인딩들을 한 번에 모두 해결해야 하는 경우도 있습니다. 예를 들어, 여러 종류의 `Report` 인터페이스 구현체를 받아 분석하는 ReportAnalyzer를 개발한다면 각 구현체를 바인딩하고 `tag` 메서드로 같은 태그를 지정해줄 수 있습니다.

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

이제 `tagged` 메서드를 사용해 해당 태그에 바인딩된 모든 서비스를 한 번에 배열로 받아 처리할 수 있습니다.

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장

`extend` 메서드를 사용하면 이미 컨테이너에서 해결된 서비스에 추가 작업을 하거나, 서비스를 데코레이팅(Decorate) 및 구성하는 등 수정할 수 있습니다. `extend`는 두 개의 인수를 받으며, 첫 번째는 확장하고 싶은 서비스 클래스, 두 번째는 수정된 서비스를 반환하는 클로저입니다. 여기서 클로저는 기존 서비스 및 컨테이너를 매개변수로 제공합니다.

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해결(Resolving)

<a name="the-make-method"></a>
### `make` 메서드

`make` 메서드를 사용하여 컨테이너로부터 클래스 인스턴스를 직접 해결받을 수 있습니다. `make`는 해결하려는 클래스 또는 인터페이스명을 인수로 넘깁니다.

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스의 일부 의존성이 컨테이너로부터 자동 해결되지 않는 경우, `makeWith` 메서드에 연관 배열의 형태로 수동 인수를 전달할 수 있습니다. 예를 들어, `Transistor` 서비스의 생성자에 `id` 인자가 반드시 필요하다면 이렇게 사용합니다.

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

현재 타입에 대한 바인딩이 컨테이너에 명시적으로 등록되어 있는지 확인하려면 `bound` 메서드를 사용할 수 있습니다.

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더 바깥에서(즉 `$app` 변수가 없는 곳에서) 컨테이너를 사용해야 한다면, `App` [파사드](/docs/12.x/facades)나 `app` [헬퍼](/docs/12.x/helpers#method-app)를 사용할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

컨테이너 인스턴스 자체를 직접 클래스에 주입받고 싶다면, 생성자에서 `Illuminate\Container\Container` 클래스를 타입힌트로 지정하면 됩니다.

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
### 자동 의존성 주입(Automatic Injection)

또한, 컨테이너에 의해 해결되는 클래스의 생성자에 타입힌트로 의존성을 선언하면, 라라벨이 의존성을 자동으로 주입해줍니다. 이 방식은 [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등은 물론이고, [큐 작업](/docs/12.x/queues)의 `handle` 메서드에도 적용할 수 있습니다. 실무에서는 대부분의 의존성을 이 자동 주입 방식으로 해결하게 됩니다.

예를 들어, 아래처럼 컨트롤러의 생성자에 직접 애플리케이션에서 정의한 서비스를 타입힌트로 지정하면, 해당 서비스가 자동으로 인스턴스화되어 주입됩니다.

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
## 메서드 호출 및 주입

가끔은 객체 인스턴스의 특정 메서드를 호출할 때, 해당 메서드의 의존성 역시 컨테이너가 자동 주입해주기를 원할 수 있습니다. 예를 들어 아래 클래스를 보겠습니다.

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

위 `generate` 메서드는 다음과 같이 컨테이너의 `call` 메서드를 통해 호출할 수 있습니다.

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 어떤 종류의 PHP 콜러블(callable)도 허용합니다. 메서드뿐 아니라 클로저를 직접 넘겨서 의존성 자동 주입이 가능하게 할 수도 있습니다.

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트

서비스 컨테이너는 객체를 해결(resolving)할 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 통해 이 이벤트에 리스너를 등록할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입의 객체가 컨테이너에서 Resolve될 때 호출됩니다.
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 어떤 타입이든 객체가 Resolve될 때 호출됩니다.
});
```

위 예시처럼, 해결되는 객체가 콜백의 인수로 전달되므로, 실제 객체가 사용되기 전에 속성값을 추가로 셋팅하는 등의 작업을 할 수 있습니다.

<a name="rebinding"></a>
### 재바인딩(Rebinding)

`rebinding` 메서드를 사용하면 서비스가 컨테이너에 다시 바인딩(즉, 기존 바인딩이 덮어쓰이거나 초기 등록 이후 바뀔 때)될 때마다 콜백을 실행할 수 있습니다. 이것은 의존성을 갱신하거나, 특정 바인딩이 변할 때마다 동작을 수정해야 할 때 유용합니다.

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

// 새로운 바인딩이 추가되면 rebinding 콜백이 실행됩니다.
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

라라벨의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현하고 있습니다. 따라서, PSR-11 컨테이너 인터페이스를 타입힌트로 선언하면 라라벨 컨테이너 인스턴스를 제공받게 됩니다.

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

만약 주어진 식별자(identifier)를 해결할 수 없는 경우 예외가 발생합니다. 식별자가 한 번도 바인딩된 적이 없다면 `Psr\Container\NotFoundExceptionInterface` 예외가, 식별자는 바인딩되어 있지만 해결에 실패했다면 `Psr\Container\ContainerExceptionInterface` 예외가 각각 발생합니다.
