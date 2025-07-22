# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [제로 구성(Zero Configuration) 해석](#zero-configuration-resolution)
    - [컨테이너를 언제 사용해야 하는가](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [컨텍스트 바인딩](#contextual-binding)
    - [컨텍스트 속성(Contextual Attributes)](#contextual-attributes)
    - [프리미티브 타입 바인딩](#binding-primitives)
    - [타입 지정 가변 인자 바인딩](#binding-typed-variadics)
    - [태깅(Tagging)](#tagging)
    - [바인딩 확장(Extending Bindings)](#extending-bindings)
- [해결(Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 의존성 주입](#automatic-injection)
- [메서드 호출과 의존성 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
    - [리바인딩(Rebinding)](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개

라라벨의 서비스 컨테이너는 클래스 간의 의존성 관리와 의존성 주입(Dependency Injection)을 담당하는 강력한 도구입니다. 의존성 주입이란, 클래스에서 필요로 하는 객체(의존성)를 생성자나 경우에 따라 "setter" 메서드를 통해 **주입(Inject)** 받는다는 뜻입니다.

간단한 예제를 살펴보겠습니다.

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;
use Illuminate\View\View;

class PodcastController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스를 생성합니다.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * 지정한 팟캐스트 정보 출력.
     */
    public function show(string $id): View
    {
        return view('podcasts.show', [
            'podcast' => $this->apple->findPodcast($id)
        ]);
    }
}
```

위 예제에서 `PodcastController`는 Apple Music과 같은 데이터 소스에서 팟캐스트 정보를 가져와야 합니다. 그래서 팟캐스트를 조회할 수 있는 서비스를 **주입** 받습니다. 이렇게 서비스를 주입받으면, 테스트 시에 실제 `AppleMusic` 서비스 대신 모킹(mock)된, 즉 임시로 만든 가짜 구현체를 쉽게 사용해볼 수 있습니다.

라라벨의 서비스 컨테이너를 깊이 이해하면, 대규모의 강력한 애플리케이션을 구축하거나 라라벨 코어에 기여하려 할 때 큰 도움이 됩니다.

<a name="zero-configuration-resolution"></a>
### 제로 구성(Zero Configuration) 해석

클래스가 의존성이 없거나, 다른 구체 클래스(인터페이스가 아님)만을 의존한다면, 컨테이너는 해당 클래스를 어떻게 해석(생성)해야 하는지 별도의 설정 없이도 알아서 처리할 수 있습니다. 예를 들어, 다음과 같은 코드를 `routes/web.php`에 작성해 보세요.

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

이 예제에서, 애플리케이션의 `/` 라우트에 접속하면 `Service` 클래스가 자동으로 해석(resolved)되고, 해당 인스턴스가 라우트의 핸들러에 주입됩니다. 이는 개발 방식에 있어 매우 혁신적인 부분입니다. 개발자는 복잡한 설정 파일에 신경 쓰지 않고, 의존성 주입의 장점을 바로 사용할 수 있게 됩니다.

라라벨에서 애플리케이션을 만들 때 작성하는 대부분의 클래스(예: [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등)는 서비스 컨테이너에서 의존성을 알아서 주입받습니다. 또한, [큐 작업](/docs/12.x/queues)의 `handle` 메서드에서도 타입힌트를 통해 의존성을 자동 주입받을 수 있습니다. 이렇게 자동으로, 그리고 별도의 설정 없이 동작하는 의존성 주입의 힘을 경험하면, 더 이상 이전 방식으로 개발하기 어려울 정도입니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 언제 사용해야 하는가

제로 구성 해석 덕분에, 여러분은 라우트, 컨트롤러, 이벤트 리스너 등에서 의존성을 타입힌트로 선언하는 것만으로도, 컨테이너와 직접 상호작용하지 않고 편리하게 의존성 주입을 활용할 수 있습니다. 예를 들어, 현재 요청 객체를 받기 위해 `Illuminate\Http\Request`를 라우트 정의에 타입힌트로 나타낼 수 있습니다. 이렇게 직접 컨테이너와 상호작용하지 않아도, 내부적으로 컨테이너가 의존성 주입을 관리하고 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

이처럼 자동 의존성 주입과 [파사드](/docs/12.x/facades) 덕분에, 라라벨 애플리케이션에서는 **직접** 컨테이너에서 바인딩하거나 해석하는 일이 거의 없을 수 있습니다. **그렇다면 언제 직접 컨테이너와 상호작용해야 할까요?** 주요한 두 가지 상황이 있습니다.

첫 번째, 하나의 클래스가 인터페이스를 구현하고, 해당 인터페이스를 라우트나 클래스 생성자에 타입힌트로 지정하고 싶을 때, 그 인터페이스를 어떻게 해석할지 컨테이너에 [직접 알려줘야 합니다](#binding-interfaces-to-implementations). 두 번째, [라라벨 패키지](/docs/12.x/packages)를 만들어 다른 개발자들과 공유하려는 경우, 패키지에서 제공하는 서비스를 컨테이너에 바인딩할 필요가 있습니다.

<a name="binding"></a>
## 바인딩

<a name="binding-basics"></a>
### 바인딩 기본

<a name="simple-bindings"></a>
#### 단순 바인딩

거의 모든 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/12.x/providers) 내부에서 등록하게 됩니다. 따라서 예제들 대부분은 해당 상황을 기준으로 설명합니다.

서비스 프로바이더에서는 항상 `$this->app` 속성을 통해 컨테이너에 접근할 수 있습니다. 컨테이너의 `bind` 메서드에 바인딩할 클래스 또는 인터페이스 이름, 그리고 해당 클래스의 인스턴스를 반환하는 클로저(익명 함수)를 전달하여 바인딩을 등록할 수 있습니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

이때, 클로저의 인자로 서비스 컨테이너 본인($app)이 전달되며, 이를 사용해 객체가 필요로 하는 하위 의존성도 컨테이너를 통해 쉽게 해석할 수 있습니다.

앞서 언급한 것처럼, 주로 서비스 프로바이더 내부에서 컨테이너와 상호작용하지만, 서비스 프로바이더 밖에서 컨테이너를 사용해야 한다면, `App` [파사드](/docs/12.x/facades)를 활용할 수도 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

`bindIf` 메서드는 이미 해당 타입의 바인딩이 등록되어 있지 않은 경우에만 새로 바인딩을 등록할 수 있도록 해줍니다.

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

편의상, 등록할 클래스 또는 인터페이스 이름을 별도의 인수로 전달하지 않고, `bind` 메서드에 전달하는 클로저의 반환 타입을 통해 라라벨이 바인딩 대상을 추론할 수도 있습니다.

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 인터페이스에 의존하지 않는 클래스라면 컨테이너에 따로 바인딩할 필요가 없습니다. 컨테이너는 리플렉션을 활용하여 이러한 객체를 알아서 생성하여 주입할 수 있습니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩

`singleton` 메서드는 클래스나 인터페이스를 컨테이너에 단 한 번만 해석해서, 이후 여러 번 요청해도 항상 같은 객체 인스턴스를 반환하도록 등록합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`singletonIf` 메서드를 사용하면, 해당 타입의 바인딩이 이미 존재하지 않을 때만 싱글톤으로 바인딩할 수 있습니다.

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

또한, `#[Singleton]` 속성을 인터페이스나 클래스에 지정하여, 해당 타입이 싱글톤 방식으로 해석되도록 할 수 있습니다.

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
#### 스코프드(Scoped) 싱글톤 바인딩

`scoped` 메서드는 클래스나 인터페이스를 라라벨의 한 요청(request) 또는 잡(job) 라이프사이클 동안에만 해석되도록 바인딩합니다. 이는 `singleton`과 비슷하지만, [`Laravel Octane`](/docs/12.x/octane) 워커가 새로운 요청을 처리하거나 [큐 워커](/docs/12.x/queues)가 새 작업을 처리할 때마다 인스턴스가 초기화됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`scopedIf` 메서드는 해당 타입이 기존에 바인딩되지 않았다면 스코프드 바인딩을 등록합니다.

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

또한, `#[Scoped]` 속성을 통해 해당 타입이 각 요청 또는 잡 라이프사이클 당 단 한 번만 해석되도록 지정할 수 있습니다.

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
#### 인스턴스 바인딩

이미 생성된 객체 인스턴스를 컨테이너에 바인딩하려면 `instance` 메서드를 사용합니다. 이렇게 등록된 인스턴스는 이후 컨테이너에서 동일하게 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기

서비스 컨테이너의 강력한 기능 중 하나는, 인터페이스를 특정 구현체에 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher`라는 인터페이스와 `RedisEventPusher`라는 구현체가 있다고 가정해 봅시다. 구현체 코드를 완성한 후, 다음과 같이 컨테이너에 등록할 수 있습니다.

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이렇게 등록하면, 해당 인터페이스(`EventPusher`)를 필요로 하는 클래스에서 자동으로 `RedisEventPusher`가 주입됩니다. 컨트롤러, 이벤트 리스너, 미들웨어 등 라라벨 애플리케이션 내 여러 클래스에서 이 방식으로 의존성 주입을 활용할 수 있습니다.

```php
use App\Contracts\EventPusher;

/**
 * 새로운 클래스 인스턴스 생성.
 */
public function __construct(
    protected EventPusher $pusher,
) {}
```

<a name="contextual-binding"></a>
### 컨텍스트 바인딩

때로는 두 개의 클래스가 동일한 인터페이스를 사용하더라도, 각각 다른 구현체를 주입하고 싶을 때가 있습니다. 예를 들어 두 컨트롤러가 동일한 `Illuminate\Contracts\Filesystem\Filesystem` [컨트랙트](/docs/12.x/contracts)를 사용하지만, 서로 다른 구현체를 필요로 할 때 사용할 수 있습니다. 라라벨에서는 이런 요구를 위한 간단하고 플루언트(fluent)한 인터페이스를 제공합니다.

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
### 컨텍스트 속성(Contextual Attributes)

컨텍스트 바인딩은 드라이버나 설정 값 등 특정 구현체를 주입할 때 자주 사용됩니다. 라라벨은 이러한 값을 서비스 프로바이더에서 직접 바인딩하지 않고도 간편하게 주입할 수 있도록 다양한 컨텍스트 속성을 제공합니다.

예를 들어, `Storage` 속성을 활용해 특정 [스토리지 디스크](/docs/12.x/filesystem) 인스턴스를 주입할 수 있습니다.

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

`Storage`외에도, `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RouteParameter`, 그리고 [Tag](#tagging) 속성(attribute)을 사용할 수 있습니다.

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

또한, 라라벨에서는 현재 인증된 사용자를 주입받을 수 있는 `CurrentUser` 속성도 제공합니다.

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 커스텀 속성 정의하기

여러분만의 맞춤형 컨텍스트 속성이 필요하다면 `Illuminate\Contracts\Container\ContextualAttribute` 컨트랙트를 구현하여 직접 속성을 만들 수 있습니다. 이때 컨테이너는 속성의 `resolve` 메서드를 호출하며, 해당 클래스에 주입할 값을 반환하면 됩니다. 아래는 라라벨의 내장 `Config` 속성을 재구현한 예제입니다.

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
     * 새로운 속성 인스턴스 생성.
     */
    public function __construct(public string $key, public mixed $default = null)
    {
    }

    /**
     * 설정 값을 해석합니다.
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
### 프리미티브 타입 바인딩

클래스가 객체뿐 아니라 정수 등 기본형(primitive) 값도 주입받아야 할 때, 컨텍스트 바인딩을 이용해 필요한 값을 주입할 수 있습니다.

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

때로는 태깅([tagged](#tagging))된 여러 인스턴스가 배열로 주입되어야 할 수도 있습니다. `giveTagged` 메서드를 사용하면 해당 태그가 붙은 모든 바인딩을 한 번에 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

응용 설정 파일에서 값을 주입하고 싶다면, `giveConfig` 메서드를 사용할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입 지정 가변 인자 바인딩

가끔, 클래스의 생성자에 여러 개의 동일 타입 객체가 가변 인자(variadic)로 들어갈 수 있습니다.

```php
<?php

use App\Models\Filter;
use App\Services\Logger;

class Firewall
{
    /**
     * 필터 인스턴스 목록.
     *
     * @var array
     */
    protected $filters;

    /**
     * 클래스 인스턴스 생성.
     */
    public function __construct(
        protected Logger $logger,
        Filter ...$filters,
    ) {
        $this->filters = $filters;
    }
}
```

컨텍스트 바인딩을 활용해, 클로저에서 여러 `Filter` 인스턴스를 배열로 반환하도록 지정하면 이 의존성을 해결할 수 있습니다.

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

더 간단하게, 원하는 클래스를 배열로 지정하면 해당 클래스들이 자동으로 해석되어 주입됩니다.

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
#### 가변 인자 태그 의존성

클래스가 가변 인자(variadic) 방식으로 특정 클래스 타입(`Report ...$reports`)의 의존성을 요구할 때, `needs`와 `giveTagged` 메서드로 태깅된 바인딩을 한 번에 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅(Tagging)

가끔, 바인딩된 서비스 중 특정 "카테고리"에 속하는 모든 인스턴스를 한 번에 해석해야 할 때가 있습니다. 예를 들어, 다양한 `Report` 인터페이스 구현체들을 배열로 받아서 사용하는 리포트 분석기를 만든다고 가정해 보겠습니다. 먼저 구현체들을 바인딩한 후, `tag` 메서드로 태그를 부여합니다.

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

이제 컨테이너의 `tagged` 메서드를 사용해 태그된 모든 서비스를 쉽게 가져올 수 있습니다.

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장(Extending Bindings)

`extend` 메서드를 사용하면 이미 해석된 서비스에 추가적인 작업을 할 수 있습니다. 서비스가 해석될 때마다, 데코레이션하거나 추가 구성을 하고 싶다면 유용합니다. `extend`는 두 개의 인수(확장할 서비스 클래스, 수정된 서비스를 반환하는 클로저)를 받으며, 클로저에는 서비스 인스턴스와 컨테이너가 전달됩니다.

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해석(Resolving)

<a name="the-make-method"></a>
### `make` 메서드

컨테이너의 `make` 메서드를 사용하여 클래스 인스턴스를 해석(생성)할 수 있습니다. 이때 원하는 클래스나 인터페이스의 이름을 인수로 전달합니다.

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스의 의존성 중에, 컨테이너가 해석할 수 없는 값이 있다면, `makeWith` 메서드를 통해 연관 배열로 추가 인수를 직접 전달할 수 있습니다. 예를 들어, `Transistor` 서비스의 생성자에 `$id` 인자가 필요하다면 이렇게 사용할 수 있습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드를 사용하면, 특정 클래스나 인터페이스가 컨테이너에 명시적으로 바인딩되어 있는지 확인할 수 있습니다.

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더 밖, 즉 `$app` 변수를 사용할 수 없는 코드에서도, `App` [파사드](/docs/12.x/facades)나 `app` [헬퍼](/docs/12.x/helpers#method-app)를 이용해 컨테이너에서 클래스 인스턴스를 해석할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

만약 컨테이너에서 스스로를 주입받고 싶다면, 생성자의 타입힌트로 `Illuminate\Container\Container` 클래스를 지정할 수 있습니다.

```php
use Illuminate\Container\Container;

/**
 * 새로운 클래스 인스턴스 생성.
 */
public function __construct(
    protected Container $container,
) {}
```

<a name="automatic-injection"></a>
### 자동 의존성 주입

또한, 컨테이너에서 해석되는 대부분의 클래스에서는 생성자에 의존성을 타입힌트로 선언만 해도 자동으로 주입받을 수 있습니다. 이 방식은 [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware)는 물론, [큐 작업](/docs/12.x/queues)의 `handle` 메서드 같은 곳에서도 전부 활용할 수 있습니다. 실제로 대부분의 객체는 이 자동 의존성 주입을 활용하여 컨테이너에서 해석됩니다.

예를 들어, 컨트롤러의 생성자에 애플리케이션 서비스가 선언되어 있다면, 해당 서비스가 자동으로 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;

class PodcastController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스 생성.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * 지정한 팟캐스트 정보 출력.
     */
    public function show(string $id): Podcast
    {
        return $this->apple->findPodcast($id);
    }
}
```

<a name="method-invocation-and-injection"></a>
## 메서드 호출과 의존성 주입

때때로, 객체 인스턴스의 메서드를 호출할 때 컨테이너가 해당 메서드의 의존성도 자동으로 주입해 주길 원할 수 있습니다. 아래의 클래스 예제를 보겠습니다.

```php
<?php

namespace App;

use App\Services\AppleMusic;

class PodcastStats
{
    /**
     * 새로운 팟캐스트 통계 리포트 생성.
     */
    public function generate(AppleMusic $apple): array
    {
        return [
            // ...
        ];
    }
}
```

컨테이너의 `call` 메서드를 사용하면, 아래와 같이 `generate` 메서드를 호출하면서 의존성도 자동 주입할 수 있습니다.

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 PHP의 어떤 콜러블(callable)도 받을 수 있습니다. 여기에는 클로저도 포함되며, 이 경우에도 의존성 자동 주입이 가능합니다.

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트

서비스 컨테이너는 객체가 해석될 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 이용해 이 이벤트를 감지할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입의 객체가 해석될 때 호출됩니다...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 어떤 타입이든 객체가 해석될 때 호출됩니다...
});
```

이벤트 콜백 함수에는 해석된 객체가 전달되므로, 실제로 객체가 사용되기 전에 필요한 추가 속성을 설정할 수 있습니다.

<a name="rebinding"></a>
### 리바인딩(Rebinding)

`rebinding` 메서드를 사용하면, 특정 서비스가 컨테이너에 재등록(리바인딩, 즉 다시 바인딩되거나, 기존 바인딩이 덮어써질 때)되는 순간을 감지할 수 있습니다. 이는 바인딩이 변경될 때마다 의존성을 업데이트하거나 동작을 수정해야 할 때 유용합니다.

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

// 새로운 바인딩 시 리바인딩 콜백이 실행됩니다...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

라라벨의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서, PSR-11 컨테이너 인터페이스를 타입힌트로 지정해 라라벨 컨테이너 인스턴스를 받아올 수 있습니다.

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

지정한 식별자(identifier)를 해석할 수 없으면 예외가 발생합니다. 해당 식별자가 한 번도 바인딩된 적이 없다면 `Psr\Container\NotFoundExceptionInterface` 예외가, 식별자가 바인딩되어 있지만 해석할 수 없는 경우 `Psr\Container\ContainerExceptionInterface` 예외가 던져집니다.
