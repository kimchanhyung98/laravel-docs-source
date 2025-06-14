# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [제로 구성(Zero Configuration) 해결](#zero-configuration-resolution)
    - [컨테이너를 언제 활용해야 하는가](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩의 기초](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [상황별 바인딩](#contextual-binding)
    - [상황별 어트리뷰트](#contextual-attributes)
    - [기본 타입 바인딩하기](#binding-primitives)
    - [타입이 지정된 가변 인자 바인딩](#binding-typed-variadics)
    - [태깅](#tagging)
    - [바인딩 확장](#extending-bindings)
- [해결(Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 주입](#automatic-injection)
- [메서드 호출 및 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
    - [재바인딩(Rebinding)](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개

라라벨 서비스 컨테이너는 클래스 간의 의존성 관리와 의존성 주입을 효과적으로 처리할 수 있는 강력한 도구입니다. 의존성 주입(Dependency Injection)이란 말은 다소 복잡하게 들릴 수 있지만, 본질적으로 클래스가 필요한 의존성을 생성자의 인수나, 경우에 따라 "setter" 메서드를 통해 **주입받는 것**을 의미합니다.

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

위 예시에서 `PodcastController`는 Apple Music과 같은 데이터 소스에서 팟캐스트 정보를 가져올 필요가 있습니다. 따라서, 팟캐스트를 조회할 수 있는 서비스를 **주입받아** 사용합니다. 서비스가 주입되므로, 테스트 시에는 `AppleMusic` 서비스를 "모킹(mock)"하거나 더미 구현체로 쉽게 대체할 수 있습니다.

라라벨 서비스 컨테이너에 대한 깊은 이해는 대규모 애플리케이션을 효과적으로 개발하는 데 반드시 필요하며, 라라벨 코어에 기여할 경우에도 필수적인 요소입니다.

<a name="zero-configuration-resolution"></a>
### 제로 구성(Zero Configuration) 해결

클래스가 의존성이 전혀 없거나, 혹은 다른 구체적인 클래스(인터페이스가 아닌)만을 의존하고 있다면, 컨테이너는 해당 클래스를 어떻게 해결할지 별도의 지시가 없어도 동작합니다. 예를 들어, 아래 코드를 `routes/web.php` 파일에 작성할 수 있습니다.

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

이 예시에서, 애플리케이션의 `/` 라우트에 접근하면 컨테이너가 자동으로 `Service` 클래스를 해결(resolve)해서 라우트 핸들러에 주입해줍니다. 이 기능은 개발 방식에 큰 변화를 가져옵니다. 즉, 복잡한 설정 파일을 걱정하지 않고도 의존성 주입의 이점을 누릴 수 있습니다.

이처럼, 라라벨 애플리케이션을 개발할 때 작성하게 되는 많은 클래스(예를 들어 [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등)는 서비스 컨테이너를 통해 자동으로 의존성을 주입받습니다. 또한, 큐에 등록된 작업의 `handle` 메서드에서도 의존성을 타입힌트 할 수 있습니다. 자동 의존성 주입과 제로 구성의 강력함을 한 번 경험하면, 이를 빼고 개발하는 것이 거의 불가능하다고 느껴질 것입니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 언제 활용해야 하는가

제로 구성 해결 덕분에, 일반적으로 라우트, 컨트롤러, 이벤트 리스너 등에서 타입힌트로 의존성을 선언하면 직접 컨테이너를 다룰 필요가 없습니다. 예를 들어, 현재의 요청(Request)을 쉽게 사용하고 싶을 때, 라우트에 `Illuminate\Http\Request` 객체를 타입힌트할 수 있습니다. 이런 코드를 작성할 때 컨테이너를 명시적으로 다루지 않아도, 내부적으로 의존성 주입은 컨테이너가 관리합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

이처럼, 자동 의존성 주입과 [파사드](/docs/12.x/facades)를 이용하면 **직접** 컨테이너에 무언가를 바인딩하거나 해결하지 않고 라라벨 애플리케이션을 개발할 수 있습니다. **그렇다면, 언제 직접 컨테이너를 다루어야 할까요?** 대표적으로 두 가지 상황이 있습니다.

첫째, 인터페이스를 구현하는 클래스를 작성하고 해당 인터페이스를 라우트나 클래스 생성자에 타입힌트로 명시하고 싶다면, [인터페이스와 구현체 사이의 관계를 컨테이너에 알려주어야 합니다](#binding-interfaces-to-implementations). 둘째, 다른 라라벨 개발자들과 공유할 [라라벨 패키지](/docs/12.x/packages)를 작성할 때, 패키지에서 사용하는 서비스를 직접 컨테이너에 바인딩할 필요가 있습니다.

<a name="binding"></a>
## 바인딩

<a name="binding-basics"></a>
### 바인딩의 기초

<a name="simple-bindings"></a>
#### 단순 바인딩

대부분의 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/12.x/providers) 내부에 등록됩니다. 따라서 아래 예시들도 이러한 상황을 기준으로 설명합니다.

서비스 프로바이더 내부에서는 항상 `$this->app` 프로퍼티를 통해 컨테이너에 접근할 수 있습니다. `bind` 메서드를 이용해 바인딩을 등록할 때, 바인딩할 클래스나 인터페이스의 이름과, 해당 클래스 인스턴스를 반환하는 클로저(익명 함수)를 전달합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

여기서 컨테이너 자체가 해결자(resolver)의 인자로 주어지므로, 우리가 만들려는 객체의 하위 의존성들도 컨테이너를 이용해 쉽게 해결할 수 있습니다.

앞서 설명했듯, 대부분의 경우 서비스 프로바이더 내부에서 컨테이너를 다루게 되지만, 서비스 프로바이더가 아닌 곳에서도 `App` [파사드](/docs/12.x/facades)를 통해 컨테이너에 접근할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

특정 타입에 대해 이미 바인딩이 등록되어 있지 않은 경우에만 바인딩을 등록하고 싶다면 `bindIf` 메서드를 사용할 수 있습니다.

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

편의를 위해, 바인딩할 클래스 또는 인터페이스 이름을 별도의 인수로 전달하지 않고, `bind` 메서드에 넘기는 클로저의 반환 타입을 보고 라라벨이 타입을 자동 추론하게 할 수도 있습니다.

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 만약 클래스가 어떤 인터페이스도 의존하지 않는다면, 컨테이너에 해당 클래스를 바인딩할 필요가 없습니다. 컨테이너는 리플렉션(reflection)을 통해 이런 객체들을 자동으로 생성할 수 있습니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩

`singleton` 메서드는 특정 클래스(또는 인터페이스)를 컨테이너에 한 번만 해결하도록 등록합니다. 싱글톤 바인딩이 한 번 해결되면, 이후 컨테이너에서 해당 타입을 요청할 때마다 같은 객체 인스턴스가 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

특정 타입에 이미 싱글톤 바인딩이 등록되어 있지 않은 경우에만 등록하려면 `singletonIf` 메서드를 사용할 수 있습니다.

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 스코프드(Scoped) 싱글톤 바인딩

`scoped` 메서드는 바인딩된 클래스 또는 인터페이스가 라라벨의 **요청(Request) 또는 작업(Job) 라이프사이클** 내에서 한 번만 해결되도록 등록합니다. 이 메서드는 `singleton`과 비슷하지만, `scoped`로 등록된 인스턴스는 라라벨 애플리케이션이 새로운 "라이프사이클"을 시작할 때(예: [Laravel Octane](/docs/12.x/octane)의 워커가 새 요청을 처리하거나, [큐 워커](/docs/12.x/queues)가 새 작업을 처리할 때) 모두 초기화됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

역시, 특정 타입에 이미 바인딩이 없다면 `scopedIf`를 사용할 수 있습니다.

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩

이미 생성된 객체 인스턴스를 컨테이너에 바인딩하려면 `instance` 메서드를 이용할 수 있습니다. 이 인스턴스는 이후 컨테이너에서 요청될 때마다 항상 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기

서비스 컨테이너의 가장 강력한 기능 중 하나는 **인터페이스를 특정 구현체에 바인딩**할 수 있다는 점입니다. 예를 들어, `EventPusher`라는 인터페이스와 그 구현체인 `RedisEventPusher`가 있다고 가정해봅시다. `RedisEventPusher`를 개발한 후, 아래와 같이 컨테이너에 등록할 수 있습니다.

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이렇게 하면, 컨테이너가 `EventPusher` 타입의 의존성이 필요할 때마다 `RedisEventPusher`를 자동으로 주입하게 됩니다. 이제 컨트롤러, 이벤트 리스너, 미들웨어 등 라라벨 애플리케이션의 여러 클래스에서 생성자에 `EventPusher` 인터페이스를 타입힌트로 사용할 수 있습니다.

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
### 상황별 바인딩

때로는 동일한 인터페이스를 사용하는 두 개 이상의 클래스가 있을 때, 각각에 서로 다른 구현체를 주입하고 싶을 수 있습니다. 예를 들어, 서로 다른 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` [컨트랙트](/docs/12.x/contracts)의 서로 다른 구현체를 필요로 하는 경우를 생각해 보십시오. 라라벨은 이를 손쉽게 정의할 수 있는 직관적인 인터페이스를 제공합니다.

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
### 상황별 어트리뷰트

상황별 바인딩(contextual binding)은 드라이버(예: 스토리지, 캐시 등)나 설정 값을 주입할 때 자주 사용됩니다. 라라벨은 상황별 값을 직접 서비스 프로바이더에서 명시하지 않고도 손쉽게 주입할 수 있는 다양한 상황별 바인딩 어트리뷰트(Attribute)를 제공합니다.

예를 들어, `Storage` 어트리뷰트를 사용하면 특정 [스토리지 디스크](/docs/12.x/filesystem)를 주입할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Container\Attributes\Storage;
use Illuminate\Contracts\Filesystem\Filesystem;

class PhotoController extends Controller
{
    public function __construct(
        #[Storage('local')] protected Filesystem $filesystem
    )
    {
        // ...
    }
}
```

`Storage` 외에도 `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RouteParameter`, 그리고 [Tag](#tagging)와 같은 여러 어트리뷰트를 사용할 수 있습니다.

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

또한, 현재 인증된 사용자를 라우트 또는 클래스에서 주입받고 싶다면 `CurrentUser` 어트리뷰트도 사용할 수 있습니다.

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 사용자 정의 어트리뷰트 만들기

직접 상황별 어트리뷰트를 만들고 싶다면 `Illuminate\Contracts\Container\ContextualAttribute` 컨트랙트를 구현하면 됩니다. 컨테이너는 어트리뷰트의 `resolve` 메서드를 호출해 실제 주입할 값을 결정합니다. 아래는 라라벨 내장 `Config` 어트리뷰트를 직접 재구현한 예시입니다.

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
### 기본 타입 바인딩하기

클래스가 객체 인스턴스 외에 숫자, 문자열 등 기본 타입의 값을 주입받아야 하는 경우에도, 상황별 바인딩을 이용해 손쉽게 필요한 값을 넣을 수 있습니다.

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

어떤 클래스가 [태그된](#tagging) 인스턴스 배열을 필요로 할 경우, `giveTagged` 메서드를 이용해 해당 태그로 바인딩된 모든 인스턴스를 쉽게 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

그리고 애플리케이션 설정 파일 값이 필요하다면 `giveConfig` 메서드를 사용할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입이 지정된 가변 인자 바인딩

때론 생성자 가변 인자(variadic argument)를 이용해 특정 타입 객체 배열을 인자로 받을 수 있습니다.

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

이런 식으로 타이핑된 가변 인자 의존성을 해결하려면, 상황별 바인딩의 `give` 메서드에 해당 타입 인스턴스 배열을 반환하는 클로저를 넘기면 됩니다.

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

더 간단하게, 클래스명 배열만 넘겨주면 컨테이너가 각 타입별 인스턴스를 생성해서 주입해줍니다.

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
#### 태그 기반 가변 인자 의존성

클래스가 주어진 타입(예: `Report ...$reports`)의 가변 인자 의존성을 가질 때, `needs`와 `giveTagged`를 함께 활용하면 해당 [태그](#tagging)로 바인딩된 모든 인스턴스를 배열로 자동 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅

때로는 동일한 "카테고리"에 속하는 여러 바인딩을 한 번에 모두 해결하고 싶을 수 있습니다. 예를 들어, 다양한 `Report` 인터페이스 구현체들을 하나의 배열로 받아 분석하는 리포트 분석기(report analyzer)를 만든다고 할 때 다음과 같이 태그를 활용할 수 있습니다.

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

이렇게 태그가 붙은 서비스들은 컨테이너의 `tagged` 메서드를 이용해 모두 한 번에 해결할 수 있습니다.

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장

`extend` 메서드를 사용하면, 이미 해결된 서비스를 수정(장식 또는 추가 설정)할 수 있습니다. 서비스가 컨테이너에서 해결될 때마다 추가 코드로 래핑하거나, 필요한 설정을 할 때 유용합니다. 이 메서드는 두 개의 인자를 받습니다. 첫 번째는 확장할 서비스 클래스, 두 번째는 서비스와 컨테이너를 인자로 받아 수정된 서비스를 반환하는 클로저입니다.

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해결(Resolving)

<a name="the-make-method"></a>
### `make` 메서드

컨테이너에서 클래스 인스턴스를 직접 만들고 싶다면 `make` 메서드를 사용할 수 있습니다. 인자로 주입받고자 하는 클래스나 인터페이스명을 전달하면 됩니다.

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

만약 일부 의존성이 컨테이너를 통해 자동으로 주입되지 않는다면, `makeWith` 메서드를 이용해 배열 형태로 직접 필요한 값을 넣을 수 있습니다. 아래는 `$id` 생성자 인수를 직접 전달하는 예시입니다.

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

컨테이너에 특정 클래스나 인터페이스가 이미 명시적으로 바인딩되어 있는지 확인하려면 `bound` 메서드를 사용할 수 있습니다.

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더 밖(이어서 `$app` 변수에 접근할 수 없는 위치)에서는 `App` [파사드](/docs/12.x/facades)나 `app` [헬퍼](/docs/12.x/helpers#method-app)를 통해서도 클래스 인스턴스를 해결할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

컨테이너 자신을 생성자에 직접 주입받고 싶다면, `Illuminate\Container\Container` 클래스를 타입힌트로 사용하면 됩니다.

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
### 자동 주입

또한, 컨테이너에서 해결되는 클래스(예: [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등)에서는 생성자에 타입힌트로 의존성을 선언하면 자동으로 주입됩니다. 큐 작업의 `handle` 메서드에서도 타입힌트로 의존성을 선언할 수 있습니다. 실제로, 여러분이 작성하게 될 대부분의 객체들은 이 방식으로 컨테이너에서 해결되도록 만드는 것이 이상적입니다.

예를 들어, 컨트롤러 생성자에서 직접 서비스 클래스를 타입힌트로 선언하면 해당 서비스가 자동으로 주입됩니다.

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

때로는 객체 인스턴스의 메서드를 호출할 때, 해당 메서드의 의존성 역시 컨테이너가 자동으로 주입해주길 원할 수 있습니다. 예를 들어 아래와 같은 클래스가 있을 때:

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

컨테이너를 사용해 `generate` 메서드를 호출하려면 아래와 같이 할 수 있습니다.

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 PHP의 어떤 callable이든 사용할 수 있습니다. 심지어 익명 함수(클로저)를 호출하면서도 의존성을 자동으로 주입받을 수 있습니다.

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트

서비스 컨테이너는 객체를 해결할 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 통해 이 이벤트에 대한 리스너를 등록할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입 객체가 컨테이너에서 해결될 때마다 호출됩니다...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 어떤 타입이든 객체가 해결될 때마다 호출됩니다...
});
```

이렇게 하면, 해결된 객체가 콜백으로 전달되어, 객체를 소비자에게 반환하기 전에 필요한 추가 설정을 할 수 있습니다.

<a name="rebinding"></a>
### 재바인딩(Rebinding)

`rebinding` 메서드를 이용하면, 특정 서비스가 컨테이너에 다시 바인딩(등록 혹은 오버라이드)될 때마다 알림을 받는 리스너를 등록할 수 있습니다. 즉, 바인딩이 갱신될 때마다 내부 의존성을 업데이트하거나 동작을 조정할 수 있습니다.

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

// 새로운 바인딩은 rebinding 콜백을 트리거합니다...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

라라벨의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현하고 있습니다. 따라서, PSR-11 컨테이너 인터페이스를 타입힌트로 사용해 라라벨 컨테이너 인스턴스를 주입받을 수 있습니다.

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

만약 주어진 식별자(identifier)를 컨테이너가 해결하지 못하면 예외가 발생합니다. 한 번도 바인딩된 적 없는 식별자인 경우에는 `Psr\Container\NotFoundExceptionInterface` 예외가, 바인딩은 되었으나 해결이 불가능한 경우에는 `Psr\Container\ContainerExceptionInterface` 예외가 던져집니다.