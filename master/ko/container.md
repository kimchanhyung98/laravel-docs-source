# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [무설정(Zero Configuration) 해석](#zero-configuration-resolution)
    - [컨테이너를 언제 활용해야 하는가](#when-to-use-the-container)
- [바인딩 (Binding)](#binding)
    - [바인딩 기초](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [컨텍스추얼 바인딩 (Contextual Binding)](#contextual-binding)
    - [컨텍스추얼 어트리뷰트 (Contextual Attributes)](#contextual-attributes)
    - [원시 값 바인딩 (Binding Primitives)](#binding-primitives)
    - [타입화된 가변인자 바인딩 (Binding Typed Variadics)](#binding-typed-variadics)
    - [태깅 (Tagging)](#tagging)
    - [바인딩 확장 (Extending Bindings)](#extending-bindings)
- [해결 (Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 주입 (Automatic Injection)](#automatic-injection)
- [메서드 호출 및 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
    - [재바인딩 (Rebinding)](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 서비스 컨테이너는 클래스의 의존성을 관리하고 의존성 주입을 수행하는 강력한 도구입니다. 의존성 주입은 간단히 말해 클래스가 필요한 의존성을 생성자나 때로는 "세터" 메서드를 통해 외부에서 주입받는 것을 의미합니다.

간단한 예제를 보겠습니다:

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

이 예제에서 `PodcastController`는 Apple Music과 같은 데이터 소스에서 팟캐스트 정보를 가져와야 합니다. 그래서 팟캐스트를 가져올 수 있는 서비스를 **주입(inject)** 합니다. 서비스가 주입되므로, 테스트 시에 `AppleMusic` 서비스를 쉽게 가짜(mock) 구현으로 바꿔 사용할 수 있게 됩니다.

Laravel 서비스 컨테이너에 대한 깊은 이해는 강력하고 대규모 애플리케이션을 구축하거나, 심지어 Laravel 코어에 기여할 때도 매우 중요합니다.

<a name="zero-configuration-resolution"></a>
### 무설정(Zero Configuration) 해석

클래스가 별도의 의존성이 없거나 다른 구체 클래스(인터페이스가 아닌)만 의존한다면, 컨테이너가 클래스를 해석하는 방법을 따로 알려줄 필요가 없습니다. 예를 들어, 다음 코드를 `routes/web.php`에 작성할 수 있습니다:

```php
<?php

class Service
{
    // ...
}

Route::get('/', function (Service $service) {
    die($service::class);
});
```

이 예제에서, 애플리케이션의 `/` 경로에 접근하면 컨테이너가 자동으로 `Service` 클래스를 해석하여 라우트 핸들러에 주입합니다. 이는 매우 강력한 기능으로, 별도의 복잡한 설정 파일 없이도 의존성 주입을 활용하여 애플리케이션을 개발할 수 있게 합니다.

다행히도, Laravel 애플리케이션에서 작성하는 많은 클래스들([컨트롤러](/docs/master/controllers), [이벤트 리스너](/docs/master/events), [미들웨어](/docs/master/middleware) 등)는 자동으로 컨테이너를 통해 의존성을 주입받도록 되어 있습니다. 또한, [큐에 등록된 작업(queued jobs)](/docs/master/queues) 의 `handle` 메서드에서도 타입 힌트를 통해 의존성을 주입받을 수 있습니다. 자동 및 무설정 의존성 주입의 강력함을 경험하면, 이를 사용하지 않고 개발하는 것은 어려워질 정도입니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 언제 활용해야 하는가

무설정 해석 덕분에, 라우트, 컨트롤러, 이벤트 리스너 등에서 의존성을 타입힌트만 해도 별도로 컨테이너와 직접 상호작용하지 않아도 됩니다. 예를 들어, 라우트에서 `Illuminate\Http\Request` 객체를 타입힌트하여 현재 요청에 쉽게 접근할 수 있습니다. 이때 코드는 컨테이너와 직접 상호작용하지 않지만, 컨테이너가 내부적으로 의존성을 주입해줍니다:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

대부분의 Laravel 애플리케이션은 자동 의존성 주입 및 [페이사드](/docs/master/facades) 덕분에 컨테이너를 수동으로 바인딩하거나 해석하지 않아도 개발이 가능합니다. 그런데, **그렇다면 언제 수동으로 컨테이너와 상호작용해야 할까요?**

두 가지 경우가 있습니다. 첫째, 인터페이스를 구현하는 클래스를 작성하고 그 인터페이스를 라우트나 클래스 생성자에서 타입힌트 하려면 [컨테이너에 해당 인터페이스의 구체 구현을 알려주어야 합니다](#binding-interfaces-to-implementations). 둘째, 다른 Laravel 개발자와 공유하려는 [Laravel 패키지](/docs/master/packages)를 작성하는 경우, 패키지의 서비스를 컨테이너에 바인딩해야 할 수 있습니다.

<a name="binding"></a>
## 바인딩 (Binding)

<a name="binding-basics"></a>
### 바인딩 기초

<a name="simple-bindings"></a>
#### 단순 바인딩

대부분의 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/master/providers) 내에서 등록하므로, 이 장의 예제들도 서비스 프로바이더 내에서 컨테이너를 활용하는 방식을 주로 보여줍니다.

서비스 프로바이더에서는 `$this->app` 속성을 통해 컨테이너에 접근할 수 있습니다. `bind` 메서드를 사용해 바인딩을 등록할 수 있으며, 바인딩할 클래스 또는 인터페이스 이름과 인스턴스를 반환하는 클로저를 인자로 전달합니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

여기서 주목할 점은, 클로저의 인수로 컨테이너 자체가 전달되며 이를 사용해 하위 의존성인 `PodcastParser`를 다시 해석(resolving)할 수 있다는 것입니다.

앞서 말한 것처럼 대부분 서비스 프로바이더 내에서 컨테이너와 상호작용하지만, 서비스 프로바이더 외부에서 컨테이너에 접근하고 싶다면 `App` [페이사드](/docs/master/facades)을 사용할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

`bindIf` 메서드는 주어진 타입에 대해 아직 바인딩이 등록되지 않은 경우에만 바인딩을 등록합니다:

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

편의를 위해, `bind` 메서드에 클래스 또는 인터페이스 이름을 별도로 명시하지 않고 클로저의 반환 타입으로부터 Laravel이 타입을 추론하도록 할 수도 있습니다:

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 클래스가 인터페이스에 의존하지 않는다면 컨테이너에 바인딩할 필요가 없습니다. Laravel 컨테이너는 리플렉션을 활용해 이런 클래스들을 자동으로 해석할 수 있기 때문입니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩

`singleton` 메서드는 한 번만 해석되어야 하는 클래스나 인터페이스를 바인딩합니다. 싱글톤 바인딩이 한 번 해석된 후에는 이후 호출에서는 항상 같은 객체 인스턴스를 반환합니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`singletonIf` 메서드를 사용하면 아직 등록되지 않은 타입에 대해서만 싱글톤 바인딩을 등록할 수 있습니다:

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 스코프드 싱글톤 바인딩 (Binding Scoped Singletons)

`scoped` 메서드는 Laravel 요청이나 작업(잡) 수명주기 내에서 한 번만 해석되는 클래스나 인터페이스를 바인딩할 때 사용합니다. `scoped`는 `singleton`과 비슷하지만, [Laravel Octane](/docs/master/octane)의 작업자가 새 요청을 처리하거나 Laravel의 [큐 작업자](/docs/master/queues)가 새 작업을 처리할 때 새로운 "수명주기"가 시작되며, 이때 `scoped` 바인딩으로 등록된 인스턴스는 초기화됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`scopedIf` 메서드를 사용하면 아직 동일한 타입에 대한 바인딩이 없을 때만 스코프드 싱글톤 바인딩을 추가할 수 있습니다:

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩

이미 생성한 객체 인스턴스를 컨테이너에 바인딩할 수도 있습니다. `instance` 메서드를 사용하면 이후 컨테이너를 통해 해당 타입을 요청할 때 항상 이 인스턴스가 반환됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기 (Binding Interfaces to Implementations)

서비스 컨테이너의 강력한 기능 중 하나는 인터페이스를 특정 구현체에 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher` 인터페이스와 이를 구현한 `RedisEventPusher` 클래스가 있다고 가정합시다. `RedisEventPusher` 구현을 작성한 후에, 다음과 같이 서비스 컨테이너에 등록할 수 있습니다:

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이 코드는 컨테이너에게 `EventPusher` 타입이 필요할 때 `RedisEventPusher`를 주입하도록 알려줍니다. 이제 컨트롤러 등 컨테이너가 책임지고 해석하는 클래스 생성자에서 `EventPusher` 인터페이스를 타입 힌트할 수 있습니다. 기억하세요, Laravel 내의 컨트롤러, 이벤트 리스너, 미들웨어 등 많은 클래스들은 항상 컨테이너로부터 해석됩니다.

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
### 컨텍스추얼 바인딩 (Contextual Binding)

때로는 서로 다른 두 클래스가 같은 인터페이스에 의존하지만, 각기 다른 구현체를 주입하고 싶을 때가 있습니다. 예를 들어, 두 개의 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` [계약(contract)](/docs/master/contracts)의 서로 다른 구현체를 의존한다고 합시다. Laravel은 이를 쉽게 정의할 수 있는 유창한(fluid) 인터페이스를 제공합니다:

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
### 컨텍스추얼 어트리뷰트 (Contextual Attributes)

컨텍스추얼 바인딩은 주로 드라이버 구현체나 설정값을 주입할 때 자주 사용됩니다. Laravel은 수동으로 서비스 프로바이더에서 바인딩을 정의하지 않고도 이러한 값을 주입할 수 있게 하는 다양한 컨텍스추얼 어트리뷰트를 제공합니다.

예를 들어, `Storage` 어트리뷰트를 사용해 특정 [스토리지 디스크](/docs/master/filesystem)를 주입할 수 있습니다:

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

`Storage` 어트리뷰트 외에도 `Auth`, `Cache`, `Config`, `DB`, `Log`, `RouteParameter`, 그리고 [`Tag`](#tagging) 어트리뷰트를 제공합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Photo;
use Illuminate\Container\Attributes\Auth;
use Illuminate\Container\Attributes\Cache;
use Illuminate\Container\Attributes\Config;
use Illuminate\Container\Attributes\DB;
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
        #[DB('mysql')] protected Connection $connection,
        #[Log('daily')] protected LoggerInterface $log,
        #[RouteParameter('photo')] protected Photo $photo,
        #[Tag('reports')] protected iterable $reports,
    )
    {
        // ...
    }
}
```

또한 Laravel은 현재 인증된 사용자를 라우트나 클래스에 주입할 수 있는 `CurrentUser` 어트리뷰트도 제공합니다:

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 커스텀 어트리뷰트 정의하기

`Illuminate\Contracts\Container\ContextualAttribute` 계약을 구현하여 자신만의 컨텍스추얼 어트리뷰트를 만들 수 있습니다. 컨테이너는 어트리뷰트의 `resolve` 메서드를 호출하는데, 이 메서드는 해당 어트리뷰트가 적용된 클래스에 주입할 값을 반환해야 합니다. 아래 예제는 Laravel의 기본 `Config` 어트리뷰트를 직접 구현한 코드입니다:

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
### 원시 값 바인딩 (Binding Primitives)

때때로 의존성이 있는 클래스가 클래스 타입 외에도 정수(integer)와 같은 원시 타입 값을 주입받아야 할 때가 있습니다. 이런 경우 컨텍스추얼 바인딩을 활용해 원하는 값을 주입할 수 있습니다:

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

클래스가 [태그된](#tagging) 인스턴스 배열을 의존할 경우, `giveTagged` 메서드를 사용해 해당 태그가 부여된 모든 바인딩을 한꺼번에 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션 설정 파일로부터 값을 주입해야 할 경우 `giveConfig` 메서드를 사용할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입화된 가변인자 바인딩 (Binding Typed Variadics)

가끔 클래스가 생성자에서 타입힌트된 배열 형태의 가변 인자를 받을 수도 있습니다:

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

이 경우, `give` 메서드에 클로저를 제공해 `Filter` 인스턴스 배열을 반환하도록 하여 의존성을 해결할 수 있습니다:

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

편의를 위해 `give` 메서드에 클래스명 배열을 직접 넘겨서 컨테이너가 자동으로 인스턴스를 생성하도록 할 수도 있습니다:

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
#### 가변 태그 의존성 (Variadic Tag Dependencies)

가변 인자가 특정 클래스로 타입힌트되었고(`Report ...$reports`), 해당 클래스에 대한 태그가 존재할 경우 `needs`와 함께 `giveTagged` 메서드를 사용해 해당 태그에 등록된 모든 바인딩을 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅 (Tagging)

특정 카테고리에 속하는 모든 바인딩을 한번에 해석해야 할 경우가 있습니다. 예를 들어, 여러 `Report` 인터페이스 구현체를 받는 리포트 분석기를 만든다고 합시다. `Report` 구현체를 바인딩한 뒤, `tag` 메서드를 사용해 태그를 지정할 수 있습니다:

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

태그가 지정된 서비스를 컨테이너가 `tagged` 메서드를 통해 모두 해석할 수 있습니다:

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장하기 (Extending Bindings)

`extend` 메서드는 이미 해석된 서비스를 수정할 때 사용합니다. 예를 들어 서비스가 해석될 때 추가 작업을 실행하거나 서비스를 감싸서 확장할 수 있습니다. 이 메서드는 두 개의 인자를 받는데, 확장하려는 서비스 클래스와 수정된 서비스를 반환하는 클로저입니다. 클로저는 해석된 서비스와 컨테이너 인스턴스를 인자로 받습니다:

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해결 (Resolving)

<a name="the-make-method"></a>
### `make` 메서드

`make` 메서드는 컨테이너로부터 클래스 인스턴스를 해석(생성)해 줍니다. 해석할 클래스 또는 인터페이스 이름을 인자로 받습니다:

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스의 일부 의존성을 컨테이너가 자동으로 해석하지 못할 경우, `makeWith` 메서드에 연관 배열로 직접 전달할 수도 있습니다. 예를 들어, `Transistor` 서비스 생성자에 필요한 `$id` 인수를 수동으로 넘기는 경우입니다:

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드는 특정 클래스나 인터페이스가 컨테이너에 명시적으로 바인딩되어 있는지 확인할 때 사용합니다:

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더 외부에서 `$app` 변수를 쓸 수 없는 경우, `App` [페이사드](/docs/master/facades)나 `app` [헬퍼](/docs/master/helpers#method-app)를 사용해 컨테이너에서 클래스 인스턴스를 해석할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

컨테이너 인스턴스 자체를 생성자에 주입하고 싶으면, 클래스 생성자에서 `Illuminate\Container\Container` 클래스를 타입힌트하면 됩니다:

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

또한, 생성자에 의존성을 타입힌트하기만 하면 컨테이너가 이를 자동으로 해석해서 주입합니다. [컨트롤러](/docs/master/controllers), [이벤트 리스너](/docs/master/events), [미들웨어](/docs/master/middleware) 등 Laravel 내 거의 모든 클래스에서 이 방식이 기본입니다. [큐 작업](/docs/master/queues)의 `handle` 메서드에서도 마찬가지입니다.

예를 들어, 애플리케이션이 정의한 서비스를 컨트롤러 생성자에서 타입힌트하면, 서비스가 자동으로 해석되어 주입됩니다:

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

때때로 객체 인스턴스의 메서드를 호출할 때 메서드 매개변수에 필요한 의존성을 자동으로 주입받고 싶을 수 있습니다. 예를 들어, 아래 클래스를 보세요:

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

컨테이너를 사용해 `generate` 메서드를 호출하며 의존성을 자동으로 주입할 수 있습니다:

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 PHP의 모든 callable 타입에 대해 사용할 수 있으며, 클로저를 호출할 때도 의존성을 자동으로 주입합니다:

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트

컨테이너는 객체가 해석될 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 사용해 이 이벤트를 청취(listen)할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입의 객체가 컨테이너에서 해석될 때 호출됩니다...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 어떤 타입이든 컨테이너에서 해석될 때 호출됩니다...
});
```

해석된 객체가 콜백으로 전달되므로, 이를 통해 객체에 추가 설정이나 속성 작업을 할 수 있습니다.

<a name="rebinding"></a>
### 재바인딩 (Rebinding)

`rebinding` 메서드는 이미 바인딩된 서비스가 컨테이너에 재등록(재바인딩)될 때 청취할 수 있게 합니다. 즉, 최초 등록 이후 바인딩이 덮어씌워질 때 동작합니다. 특정 바인딩이 바뀔 때마다 의존성을 업데이트하거나 행동을 변경할 때 유용합니다:

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

// 새 바인딩은 rebinding 클로저를 트리거합니다...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

Laravel 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서 PSR-11 컨테이너 인터페이스를 타입힌트하여 Laravel 컨테이너 인스턴스를 얻을 수 있습니다:

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

지정한 식별자를 해석할 수 없으면 예외가 발생합니다. 해당 식별자가 등록되지 않은 경우에는 `Psr\Container\NotFoundExceptionInterface` 인스턴스의 예외가, 등록은 됐지만 해석에 실패할 경우에는 `Psr\Container\ContainerExceptionInterface` 인스턴스의 예외가 던져집니다.