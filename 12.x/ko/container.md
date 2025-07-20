# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [제로 설정(Zero Configuration) 해석](#zero-configuration-resolution)
    - [컨테이너를 언제 활용해야 할까](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [컨텍스트 바인딩](#contextual-binding)
    - [컨텍스트 속성](#contextual-attributes)
    - [프리미티브 바인딩](#binding-primitives)
    - [타입이 명확한 가변 인자 바인딩](#binding-typed-variadics)
    - [태깅(Tagging)](#tagging)
    - [바인딩 확장하기](#extending-bindings)
- [해결(Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 주입](#automatic-injection)
- [메서드 호출 및 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
    - [리바인딩(Rebinding)](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개

라라벨의 서비스 컨테이너는 클래스 간 의존성 관리와 의존성 주입(dependency injection)을 위한 강력한 도구입니다. 의존성 주입이란 결국 "클래스의 의존성을 생성자나(혹은 경우에 따라 setter 메서드) 통해 클래스 내부로 주입해 준다"는 뜻입니다.

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
     * 전달된 팟캐스트에 대한 정보를 표시합니다.
     */
    public function show(string $id): View
    {
        return view('podcasts.show', [
            'podcast' => $this->apple->findPodcast($id)
        ]);
    }
}
```

이 예시에서 `PodcastController`는 Apple Music과 같은 데이터 소스에서 팟캐스트 정보를 가져와야 합니다. 그래서 팟캐스트 정보를 조회할 수 있는 서비스를 **주입**합니다. 서비스가 주입되어 있기 때문에, 테스트 시에는 `AppleMusic` 서비스의 더미(모킹) 구현을 쉽게 만들어서 사용할 수도 있습니다.

라라벨 서비스 컨테이너에 대한 깊은 이해는 강력하고 규모가 큰 애플리케이션을 개발할 때, 그리고 라라벨 자체의 핵심에 기여할 때도 매우 중요합니다.

<a name="zero-configuration-resolution"></a>
### 제로 설정(Zero Configuration) 해석

클래스에 의존성이 없거나, 모든 의존성이 구체 클래스(인터페이스가 아님)인 경우에는 컨테이너에 별도의 해석 방법을 알려줄 필요가 없습니다. 예를 들어, 아래와 같이 `routes/web.php`에 코드를 작성할 수 있습니다.

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

이 예제에서 `/` 경로로 접속하면, `Service` 클래스가 자동으로 해석되어 이 라우트의 핸들러에 주입됩니다. 이것은 정말 혁신적인 변화입니다. 별도의 복잡한 설정 파일을 신경쓰지 않아도, 의존성 주입의 이점을 그대로 누리며 애플리케이션을 개발할 수 있습니다.

라라벨 애플리케이션을 개발하다 보면, [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등에서 여러분이 생성하는 대부분의 클래스는 컨테이너를 통해 자동으로 의존성을 주입받게 됩니다. 또한, [큐 작업](/docs/12.x/queues)의 `handle` 메서드에도 타입 힌트로 의존성을 선언할 수 있습니다. 자동적이고, 설정이 필요 없는 의존성 주입에 익숙해지면, 이 기능 없이는 개발하기 힘들 정도로 편리함을 느낄 것입니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 언제 활용해야 할까

제로 설정 해석 덕분에, 라우트, 컨트롤러, 이벤트 리스너 등 다양한 곳에서 단순히 타입 힌트만으로 의존성을 선언하면 컨테이너가 자동으로 처리해 줍니다. 예를 들어, 라우트 정의에 `Illuminate\Http\Request` 객체를 타입 힌트해두면, 현재 요청 객체를 쉽게 사용할 수 있습니다. 이런 코드에서 직접 컨테이너를 다루지 않아도, 컨테이너가 알아서 의존성을 주입해줍니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

사실 라라벨에서는 자동 의존성 주입과 [파사드](/docs/12.x/facades)만으로 대부분의 기능 구현이 가능합니다. **그렇다면 직접 컨테이너를 다뤄야 하는 경우는 언제일까요?** 대표적인 경우는 다음과 같습니다.

첫 번째, 인터페이스를 구현한 클래스를 만들고, 라우트 혹은 클래스 생성자 등에서 해당 인터페이스를 타입 힌트할 때는 [인터페이스와 실제 구현을 컨테이너에 등록](#binding-interfaces-to-implementations)해야 합니다. 두 번째, [라라벨 패키지를 작성](/docs/12.x/packages)하여 다른 개발자들과 공유할 계획이라면, 패키지의 서비스들을 컨테이너에 직접 바인딩해야 할 수 있습니다.

<a name="binding"></a>
## 바인딩

<a name="binding-basics"></a>
### 바인딩 기본

<a name="simple-bindings"></a>
#### 단순 바인딩

대부분의 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/12.x/providers)에서 등록합니다. 따라서 대부분의 예제는 이 맥락에서 컨테이너 사용법을 보여줍니다.

서비스 프로바이더 내부에서는 항상 `$this->app` 프로퍼티로 컨테이너에 접근할 수 있습니다. 바인딩을 등록하려면 `bind` 메서드에 클래스 또는 인터페이스명과, 해당 클래스 인스턴스를 반환하는 클로저를 전달합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

위 코드처럼, 객체를 생성하는 클로저의 인자로 컨테이너 자체를 받을 수 있으며, 이걸 활용해서 하위 의존성도 쉽게 해소할 수 있습니다.

앞서 언급한 대로, 보통 서비스 프로바이더 내에서 컨테이너와 상호작용하지만, 프로바이더 외부에서 [파사드](/docs/12.x/facades)를 이용해 컨테이너를 다룰 수도 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

`bindIf` 메서드를 사용하면, 해당 타입에 이미 바인딩이 등록되어 있지 않은 경우에만 바인딩을 등록할 수 있습니다.

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

좀 더 간편하게, 바인딩할 클래스나 인터페이스명을 별도 인자로 전달하지 않고도, `bind` 메서드에서 반환 타입을 통해 라라벨이 타입을 추론하게 할 수 있습니다.

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 의존성이 인터페이스가 아닌 클래스라면, 컨테이너에 바인딩이 필요하지 않습니다. 컨테이너는 리플렉션(reflection)을 통해 이런 객체들을 자동으로 생성할 수 있습니다.

<a name="binding-a-singleton"></a>
#### 싱글턴(Singleton) 바인딩

`singleton` 메서드는 해당 클래스 또는 인터페이스를 컨테이너에 단 한 번만 해석되도록 싱글턴으로 바인딩합니다. 싱글턴 바인딩은 최초 해석된 객체 인스턴스를 컨테이너에 저장하며, 이후에도 동일한 인스턴스가 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`singletonIf` 메서드를 사용하면, 이미 바인딩이 존재하지 않는 경우에만 싱글턴 바인딩이 등록됩니다.

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 스코프드(Scoped) 싱글턴 바인딩

`scoped` 메서드는 클래스나 인터페이스를 컨테이너에, 특정 라라벨 요청/작업 라이프사이클 내에서 단 한 번만 해석되도록 바인딩합니다. 이 방법은 `singleton`과 비슷하지만, 라라벨 애플리케이션이 새로운 "라이프사이클"을 시작할 때(예: [Laravel Octane](/docs/12.x/octane) 워커가 새 요청을 처리, 또는 [큐 워커](/docs/12.x/queues)에서 새 작업을 처리할 때) 인스턴스가 리셋됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`scopedIf` 메서드로, 이미 바인딩이 없을 때만 스코프드 바인딩을 추가할 수 있습니다.

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩

이미 생성된 객체 인스턴스를 `instance` 메서드로 컨테이너에 바인딩할 수도 있습니다. 이 경우, 항상 해당 인스턴스가 그대로 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기

서비스 컨테이너의 강력한 기능 중 하나는 인터페이스를 특정 구현체에 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher` 인터페이스와 이를 구현한 `RedisEventPusher` 클래스를 가정해봅시다. 해당 인터페이스를 `RedisEventPusher`에 연결하려면 다음과 같이 등록할 수 있습니다.

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이렇게 해두면, 컨테이너가 `EventPusher` 구현이 필요한 곳에 `RedisEventPusher`를 주입합니다. 이제 컨테이너가 해석하는 곳, 예를 들어 컨트롤러, 이벤트 리스너, 미들웨어 등에서는 생성자에 해당 인터페이스를 그냥 타입힌트해도 됩니다.

```php
use App\Contracts\EventPusher;

/**
 * 새로운 클래스 인스턴스를 생성합니다.
 */
public function __construct(
    protected EventPusher $pusher,
) {}
```

<a name="contextual-binding"></a>
### 컨텍스트 바인딩

동일한 인터페이스를 사용하는 클래스가 여러 개 있는데, 각 클래스에 서로 다른 구현을 주입하고 싶을 때가 있습니다. 예를 들어, 두 개의 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` [계약](/docs/12.x/contracts)에 의존하지만 각각 다른 구현체를 사용해야 한다고 생각해봅시다. 이때 라라벨이 Fluent한 인터페이스를 제공합니다.

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

컨텍스트 바인딩은 드라이버, 설정 값 등 특정 값을 주입할 때 자주 쓰입니다. 라라벨에서는 이를 더 편리하게 처리할 수 있는 다양한 컨텍스트 바인딩 속성을 제공합니다. 이러한 속성을 사용하면 서비스 프로바이더에 수동으로 바인딩을 추가하지 않아도 됩니다.

예를 들어, `Storage` 속성을 사용하여 특정 [스토리지 디스크](/docs/12.x/filesystem)를 주입할 수 있습니다.

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

`Storage` 외에도 `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RouteParameter`, 그리고 [Tag](#tagging) 등 다양한 속성을 사용할 수 있습니다.

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

또한, 라라벨은 현재 인증된 사용자를 경로 또는 클래스에 주입할 수 있는 `CurrentUser` 속성을 제공합니다.

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 커스텀 속성 정의하기

여러분만의 컨텍스트 속성을 만들고 싶다면 `Illuminate\Contracts\Container\ContextualAttribute` 계약을 구현하면 됩니다. 컨테이너는 해당 속성의 `resolve` 메서드를 호출하여 실제로 주입될 값을 얻어오게 됩니다. 아래는 라라벨 내장 `Config` 속성을 직접 구현해보는 예시입니다.

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
     * 새로운 속성 인스턴스를 생성합니다.
     */
    public function __construct(public string $key, public mixed $default = null)
    {
    }

    /**
     * 실제 설정 값을 해석합니다.
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
### 프리미티브 바인딩

클래스에서 의존성으로 객체만 주입받는 게 아니라, 정수와 같은 프리미티브 값도 필요한 경우가 있습니다. 컨텍스트 바인딩을 활용하면 원하는 값을 쉽게 주입할 수 있습니다.

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

클래스가 [태그](#tagging)된 인스턴스들의 배열에 의존하는 경우에는, `giveTagged` 메서드를 사용해 해당 태그로 바인딩된 모든 객체를 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션의 설정파일에서 값을 가져와 주입하고 싶다면, `giveConfig` 메서드를 사용할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입이 명확한 가변 인자 바인딩

가끔, 생성자에서 변수 개수(Variadic)로 타입이 명시된 객체 배열을 받을 때가 있습니다.

```php
<?php

use App\Models\Filter;
use App\Services\Logger;

class Firewall
{
    /**
     * 필터 인스턴스.
     *
     * @var array
     */
    protected $filters;

    /**
     * 새로운 클래스 인스턴스를 생성합니다.
     */
    public function __construct(
        protected Logger $logger,
        Filter ...$filters,
    ) {
        $this->filters = $filters;
    }
}
```

컨텍스트 바인딩에서, `give` 메서드에 클로저를 전달하여 원하는 `Filter` 인스턴스 배열을 반환하게 할 수 있습니다.

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

혹은, 더 간편하게 클래스명 배열을 직접 넘겨서 컨테이너가 알아서 해당 인스턴스를 필요할 때마다 해석하게 할 수도 있습니다.

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
#### 가변 태그 의존성

가변(variadic) 의존성이 특정 클래스에 타입 힌트로 선언된 경우(`Report ...$reports`), `needs`와 `giveTagged`를 함께 사용하면 해당 태그가 지정된 모든 바인딩을 쉽게 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅(Tagging)

때때로 특정 "카테고리"에 속하는 모든 바인딩을 한 번에 해석해야 할 수 있습니다. 예를 들어, 다양한 `Report` 인터페이스 구현을 여러 개 받아 분석하는 분석기를 만든다고 해봅시다. 각 구현을 등록한 뒤, `tag` 메서드로 하나의 태그를 지정할 수 있습니다.

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

태그가 지정된 서비스들은 컨테이너의 `tagged` 메서드를 통해 모두 한 번에 가져올 수 있습니다.

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장하기

`extend` 메서드를 이용하면 이미 해석된 서비스를 변경(데코레이터 패턴 등)하거나 추가 설정을 적용할 수 있습니다. 확장하려는 서비스 클래스와, 변경된 서비스를 반환하는 클로저 두 개가 필요합니다. 클로저는 해석된 서비스와 컨테이너 인스턴스를 매개변수로 전달받을 수 있습니다.

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해결(Resolving)

<a name="the-make-method"></a>
### `make` 메서드

컨테이너에서 클래스 인스턴스를 해석하려면 `make` 메서드를 사용합니다. 이 메서드는 해석할 클래스나 인터페이스명을 인자로 받습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

만약 해당 클래스의 일부 의존성이 컨테이너로 해석할 수 없다면, `makeWith` 메서드에 연관 배열로 직접 값을 전달해 줄 수 있습니다. 예를 들어, `Transistor` 서비스가 생성자에서 `$id` 값을 필요로 할 때 아래와 같이 쓸 수 있습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

지정한 클래스나 인터페이스가 컨테이너에 명시적으로 바인딩되어 있는지 확인하려면 `bound` 메서드를 사용할 수 있습니다.

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더 외부에서, `$app` 변수에 접근할 수 없는 위치에서는 [파사드](/docs/12.x/facades) `App`이나 [헬퍼 함수](/docs/12.x/helpers#method-app) `app`을 통해 쉽게 해석할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

라라벨 컨테이너 인스턴스 자체를 클래스 생성자에 주입받고 싶다면, `Illuminate\Container\Container` 클래스를 타입힌트 하면 됩니다.

```php
use Illuminate\Container\Container;

/**
 * 새로운 클래스 인스턴스를 생성합니다.
 */
public function __construct(
    protected Container $container,
) {}
```

<a name="automatic-injection"></a>
### 자동 주입

대부분의 경우, 컨테이너가 해석하는 클래스(예를 들어 [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등)의 생성자에서 의존성을 타입 힌트 해주면 자동으로 주입됩니다. 또한 [큐 작업](/docs/12.x/queues)의 `handle` 메서드에도 의존성을 타입 힌트로 선언할 수 있습니다. 실무에서 우리 객체 대부분은 이렇게 컨테이너에 의해 자동으로 해석, 주입받게 됩니다.

예를 들어, 애플리케이션에서 정의한 서비스를 컨트롤러 생성자에 타입 힌트로 선언하면, 서비스가 자동으로 해석되어 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;

class PodcastController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스를 생성합니다.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * 주어진 팟캐스트 정보를 표시합니다.
     */
    public function show(string $id): Podcast
    {
        return $this->apple->findPodcast($id);
    }
}
```

<a name="method-invocation-and-injection"></a>
## 메서드 호출 및 주입

특정 객체 인스턴스에서 메서드를 호출할 때, 해당 메서드의 의존성도 컨테이너가 자동으로 주입해주길 바랄 때가 있습니다. 예를 들어, 다음과 같은 클래스를 보겠습니다.

```php
<?php

namespace App;

use App\Services\AppleMusic;

class PodcastStats
{
    /**
     * 팟캐스트 통계 리포트를 생성합니다.
     */
    public function generate(AppleMusic $apple): array
    {
        return [
            // ...
        ];
    }
}
```

컨테이너의 `call` 메서드를 이용해 `generate` 메서드를 다음과 같이 호출할 수 있습니다.

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 어떤 PHP 콜러블(callable)이라도 인자로 받을 수 있습니다. 또한, 클로저도 의존성을 자동 주입받아 실행할 수 있습니다.

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트

서비스 컨테이너는 객체가 해석될 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 통해 이 이벤트를 감지해 처리할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입 객체가 해석될 때 호출...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 어떤 타입이든 객체가 해석될 때 호출...
});
```

이렇게 해석되는 객체를 콜백에서 전달받아, 객체의 속성을 추가로 설정하거나 원하는 작업을 수행할 수 있습니다.

<a name="rebinding"></a>
### 리바인딩(Rebinding)

`rebinding` 메서드를 사용하면, 서비스가 컨테이너에 다시 바인딩(즉, 재등록 또는 기존 바인딩이 덮어쓰기)될 때마다 감지할 수 있습니다. 특정 바인딩이 갱신될 때마다 의존하도록 설정을 추가하거나 동작을 수정하는 데 유용합니다.

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

// 새로운 바인딩이 등록되면 rebinding 콜백이 실행됩니다.
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

라라벨의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서 PSR-11 컨테이너 인터페이스를 타입힌트 하여 라라벨 컨테이너 인스턴스를 직접 받아올 수 있습니다.

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

만약 주어진 식별자를 해석할 수 없다면 예외가 발생합니다. 식별자가 한 번도 바인딩된 적이 없다면 `Psr\Container\NotFoundExceptionInterface` 예외가, 식별자가 바인딩되어 있지만 해석에 실패했다면 `Psr\Container\ContainerExceptionInterface` 예외가 던져집니다.
