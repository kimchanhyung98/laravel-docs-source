# 서비스 컨테이너

- [소개](#introduction)
    - [제로 설정(Zero Configuration) 해석](#zero-configuration-resolution)
    - [컨테이너를 활용해야 할 때](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩](#binding-interfaces-to-implementations)
    - [컨텍스트별 바인딩](#contextual-binding)
    - [컨텍스트 속성](#contextual-attributes)
    - [기본값(Primitive) 바인딩](#binding-primitives)
    - [타입 지정 가변 인자 바인딩](#binding-typed-variadics)
    - [태깅(Tagging)](#tagging)
    - [바인딩 확장](#extending-bindings)
- [해결(Resolving)](#resolving)
    - [Make 메서드](#the-make-method)
    - [자동 주입](#automatic-injection)
- [메서드 호출과 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
    - [재바인딩(Rebinding)](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개

Laravel 서비스 컨테이너는 클래스 의존성 관리와 의존성 주입(Dependency Injection)을 수행하는 강력한 도구입니다. 의존성 주입이란, 본질적으로 클래스의 의존성을 생성자(constructor)나, 경우에 따라 "세터(setter)" 메서드를 통해 외부에서 "주입"하는 것을 말합니다.

간단한 예제를 살펴보겠습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;
use Illuminate\View\View;

class PodcastController extends Controller
{
    /**
     * 새 컨트롤러 인스턴스 생성.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * 주어진 팟캐스트의 정보 출력.
     */
    public function show(string $id): View
    {
        return view('podcasts.show', [
            'podcast' => $this->apple->findPodcast($id)
        ]);
    }
}
```

이 예제에서 `PodcastController`는 Apple Music과 같은 데이터 소스에서 팟캐스트를 가져와야 합니다. 따라서 팟캐스트를 가져오는 역할을 하는 서비스를 **주입**합니다. 서비스가 주입되므로, 애플리케이션을 테스트할 때 `AppleMusic` 서비스의 모의(Mock) 혹은 가짜 구현체를 쉽게 만들 수 있습니다.

Laravel 서비스 컨테이너를 깊이 있게 이해하는 것은 강력하고 대규모 애플리케이션을 구축하거나 Laravel 코어에 기여하는 데 필수적입니다.

<a name="zero-configuration-resolution"></a>
### 제로 설정(Zero Configuration) 해석

클래스가 의존성이 없거나, 다른 구체 클래스(인터페이스가 아님)에만 의존하는 경우, 컨테이너에 해당 클래스를 어떻게 해석해야 하는지 따로 지시할 필요가 없습니다. 예를 들어, `routes/web.php` 파일에 다음과 같이 작성할 수 있습니다:

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

이 예제에서 애플리케이션의 `/` 라우트에 접근하면 `Service` 클래스가 자동으로 해석되어 라우트 처리기로 주입됩니다. 이 기능은 매우 혁신적입니다. 즉, 복잡한 설정 파일을 신경쓰지 않고 의존성 주입을 통해 애플리케이션을 개발할 수 있다는 뜻입니다.

Laravel에서 애플리케이션을 작성할 때, 여러분이 작성하는 많은 클래스들은 컨테이너를 통해 자동으로 의존성을 주입받습니다. 여기에는 [컨트롤러](/docs/{{version}}/controllers), [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등이 포함됩니다. 또한 [큐 잡](/docs/{{version}}/queues)의 `handle` 메서드에서 의존성을 타입힌트로 지정할 수 있습니다. 자동(및 제로 설정) 의존성 주입 기능을 한번 맛보면, 이 기능 없이 개발하기가 불가능하게 느껴질 것입니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 활용해야 할 때

제로 설정 해석 기능 덕분에, 라우트·컨트롤러·이벤트 리스너 등 여러 곳에서 타입힌트만 지정하면 직접 컨테이너와 상호작용할 필요 없이 의존성을 바로 사용할 수 있습니다. 예를 들어, 현재 요청을 쉽게 다루기 위해 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입힌트로 지정할 수 있습니다. 컨테이너와 직접 상호작용하지 않아도, 그 뒤에서 의존성 주입을 관리합니다:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

대부분의 경우, 자동 의존성 주입과 [파사드](/docs/{{version}}/facades) 덕분에, 컨테이너에서 무언가를 직접 바인딩하거나 해석할 필요 없이도 Laravel 애플리케이션을 만들 수 있습니다.  
**그렇다면 언제 직접 컨테이너와 상호작용해야 할까요?** 대표적으로 두 가지 경우가 있습니다.

첫째, 만약 인터페이스를 구현하는 클래스를 작성하고, 그 인터페이스를 라우트 또는 클래스 생성자에 타입힌트로 지정하려면, [컨테이너에 해당 인터페이스를 어떤 구현체로 해석할지 알려주어야 합니다](#binding-interfaces-to-implementations).  
둘째, [라라벨 패키지](/docs/{{version}}/packages)를 작성하여 다른 개발자와 공유하려는 경우, 패키지에서 제공하는 서비스를 컨테이너에 바인딩해야 할 수 있습니다.

<a name="binding"></a>
## 바인딩

<a name="binding-basics"></a>
### 바인딩 기본

<a name="simple-bindings"></a>
#### 단순 바인딩

대부분의 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/{{version}}/providers) 내에서 등록됩니다. 따라서 대부분의 예제는 그 맥락에서 컨테이너를 사용하는 방법을 보여줍니다.

서비스 프로바이더에서는 `$this->app` 프로퍼티를 통해 항상 컨테이너에 접근할 수 있습니다. `bind` 메서드로 바인딩을 등록할 수 있으며, 바인딩할 클래스 또는 인터페이스명과 인스턴스를 반환하는 클로저를 인자로 전달합니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

위 예제에서 볼 수 있듯, 리졸버(클로저)의 인자로 컨테이너 자체를 받을 수 있습니다. 이를 통해 생성하려는 객체의 하위 의존성도 컨테이너를 사용해 해석할 수 있습니다.

대부분 서비스 프로바이더 내에서 컨테이너를 다루지만, 만약 서비스 프로바이더 외부에서 컨테이너와 상호작용하고 싶다면 `App` [파사드](/docs/{{version}}/facades)를 사용할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

이미 같은 타입에 대한 바인딩이 존재하지 않을 때만 바인딩하려면 `bindIf` 메서드를 사용할 수 있습니다:

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

편의상, 바인딩하려는 클래스 또는 인터페이스명을 별도의 인자로 제공하지 않고, `bind`에 전달한 클로저의 반환 타입에서 Laravel이 타입을 유추하도록 할 수 있습니다:

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 별도의 인터페이스에 의존하지 않는 클래스는 컨테이너에 바인딩할 필요가 없습니다. 컨테이너는 리플렉션을 통해 이런 객체들을 자동으로 해석할 수 있기 때문입니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩

`singleton` 메서드는 클래스 또는 인터페이스를 컨테이너에 한 번만 해석되도록 싱글톤으로 바인딩합니다. 한 번 싱글톤 바인딩이 해석되면, 이후에는 동일한 인스턴스를 반환합니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

이미 같은 타입에 대한 바인딩이 존재하지 않을 때만 싱글톤으로 바인딩하려면 `singletonIf` 메서드를 사용할 수 있습니다:

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 범위 지정 싱글톤(Scoped Singleton) 바인딩

`scoped` 메서드는 주어진 라라벨 요청/잡(lifecycle) 동안에만 한 번 해석되는 싱글톤으로 바인딩합니다. 이 메서드는 `singleton`과 비슷하지만, [Laravel Octane](/docs/{{version}}/octane) 워커가 새로운 요청을 처리하거나 라라벨 [큐 워커](/docs/{{version}}/queues)가 새로운 잡을 처리할 때마다 인스턴스가 초기화(flus한)됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`scopedIf` 메서드는 이미 바인딩이 존재하지 않을 때만 바인딩합니다:

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩

이미 생성된 객체 인스턴스를 컨테이너에 등록하려면 `instance` 메서드를 사용할 수 있습니다. 이후 호출에서도 항상 해당 인스턴스가 반환됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩

서비스 컨테이너의 강력한 기능 중 하나는 인터페이스에 원하는 구현체를 바인딩하는 것입니다. 예를 들어, `EventPusher` 인터페이스와 `RedisEventPusher` 구현체가 있다고 가정합시다. 인터페이스 구현을 마친 뒤 아래와 같이 서비스 컨테이너에 등록할 수 있습니다:

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이렇게 하면 `EventPusher`가 필요한 클래스에는 항상 `RedisEventPusher`가 주입됩니다. 이제 컨테이너로 해석되는 클래스 생성자에서 `EventPusher` 인터페이스를 타입힌트로 지정하면 됩니다. 컨트롤러, 이벤트 리스너, 미들웨어 등 Laravel의 많은 클래스들은 컨테이너를 통해 항상 해석된다는 것을 기억하세요:

```php
use App\Contracts\EventPusher;

/**
 * 새 클래스 인스턴스 생성.
 */
public function __construct(
    protected EventPusher $pusher,
) {}
```

<a name="contextual-binding"></a>
### 컨텍스트별 바인딩

동일한 인터페이스를 사용하는 두 클래스가 각기 다른 구현체를 주입받길 원할 때가 있습니다. 예를 들어 두 컨트롤러가 각각 다른 [`Illuminate\Contracts\Filesystem\Filesystem`](/docs/{{version}}/contracts) 구현체를 필요로 할 수 있습니다. 라라벨은 이런 동작을 쉽게 정의할 수 있는 유창한 인터페이스를 제공합니다:

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

컨텍스트별 바인딩은 드라이버 구현체나 설정값을 주입할 때 자주 사용되므로, 라라벨에서는 수동으로 서비스를 바인딩하지 않아도 다양한 컨텍스트 바인딩 어트리뷰트를 제공합니다.

예를 들어, `Storage` 어트리뷰트를 사용해 특정 [스토리지 디스크](/docs/{{version}}/filesystem)를 주입할 수 있습니다:

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

`Storage` 외에 `Auth`, `Cache`, `Config`, `DB`, `Log`, `RouteParameter`, [`Tag`](#tagging) 등의 어트리뷰트도 제공합니다:

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

또한, 현재 인증된 사용자를 라우트 또는 클래스에 주입할 수 있는 `CurrentUser` 어트리뷰트도 제공됩니다:

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 사용자 정의 어트리뷰트

`Illuminate\Contracts\Container\ContextualAttribute` 계약을 구현하여 나만의 컨텍스트 어트리뷰트를 만들 수 있습니다. 컨테이너는 어트리뷰트의 `resolve` 메서드를 호출하여, 주입할 값을 반환받습니다. 아래 예제는 라라벨의 내장 `Config` 어트리뷰트의 간단한 재구현입니다:

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
     * 새 어트리뷰트 인스턴스 생성.
     */
    public function __construct(public string $key, public mixed $default = null)
    {
    }

    /**
     * 설정값 해석.
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
### 기본값(Primitive) 바인딩

클래스에서 외부 클래스를 주입받으면서, 정수 등 프리미티브 값도 함께 주입해야 할 때가 있습니다. 이때 컨텍스트 바인딩을 이용해 간단하게 값을 주입할 수 있습니다:

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

어떤 클래스가 [태깅](#tagging)된 여러 인스턴스 배열을 필요로 할 때는 `giveTagged` 메서드를 사용할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션 설정 파일에서 값을 가져와 주입하려면 `giveConfig` 메서드를 사용할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입 지정 가변 인자 바인딩

간혹 생성자에서 가변 인자(variadic)로 타입이 지정된 객체 배열을 받는 클래스가 있을 수 있습니다:

```php
<?php

use App\Models\Filter;
use App\Services\Logger;

class Firewall
{
    /**
     * 필터 인스턴스들.
     *
     * @var array
     */
    protected $filters;

    /**
     * 새 클래스 인스턴스 생성.
     */
    public function __construct(
        protected Logger $logger,
        Filter ...$filters,
    ) {
        $this->filters = $filters;
    }
}
```

이런 경우, 컨텍스트 바인딩의 `give` 메서드에 클로저를 전달해, 여러 `Filter` 인스턴스 배열을 리턴하게 할 수 있습니다:

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

더 편하게, 클래스 이름 배열만 제공해도 필요할 때마다 자동으로 해석됩니다:

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

클래스가 `Report ...$reports`처럼 특정 클래스 타입의 가변 인자 의존성을 가질 때, `needs`와 `giveTagged`를 조합하여 [해당 태그](#tagging)로 등록된 모든 바인딩을 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅(Tagging)

특정 "카테고리"의 모든 바인딩을 해석해야 할 때가 있습니다. 예를 들어, 다양한 `Report` 인터페이스 구현체 배열을 받아서 분석하는 리포트 분석기를 만들고자 할 수 있습니다. 각 `Report` 구현체를 등록한 다음, `tag` 메서드로 태그를 추가합니다:

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

이렇게 태그가 지정되면, 컨테이너의 `tagged` 메서드로 한 번에 모두 가져올 수 있습니다:

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장

`extend` 메서드는 해석된 서비스를 수정할 수 있습니다. 예를 들어, 서비스가 해석될 때 데코레이터를 추가하거나 설정을 변경할 수 있습니다.  
`extend`는 두 개의 인자를 받습니다. 첫 번째는 확장하려는 서비스 클래스, 두 번째는 수정된 서비스를 반환하는 클로저입니다. 이 클로저에는 서비스와 컨테이너 인스턴스가 전달됩니다:

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해석(Resolving)

<a name="the-make-method"></a>
### make 메서드

`make` 메서드를 사용해 컨테이너에서 클래스 인스턴스를 가져올 수 있습니다. `make`는 해석하려는 클래스 또는 인터페이스명을 인자로 받습니다:

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

만약 클래스 의존성 중 일부를 컨테이너에서 해석할 수 없다면, `makeWith` 메서드에 연관 배열로 직접 전달할 수 있습니다.  
예를 들어, `Transistor` 서비스의 `$id` 생성자 인자를 직접 전달할 수 있습니다:

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드를 활용해 클래스나 인터페이스가 컨테이너에 명시적으로 바인딩되어 있는지 확인할 수 있습니다:

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더 외부에서 `$app` 변수에 접근할 수 없는 코드 위치에서도, `App` [파사드](/docs/{{version}}/facades)나 `app` [헬퍼](/docs/{{version}}/helpers#method-app)를 이용해 인스턴스를 해석할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

컨테이너 자체를 주입받고 싶으면, 생성자에서 `Illuminate\Container\Container` 클래스를 타입힌트로 지정하면 됩니다:

```php
use Illuminate\Container\Container;

/**
 * 새 클래스 인스턴스 생성.
 */
public function __construct(
    protected Container $container,
) {}
```

<a name="automatic-injection"></a>
### 자동 주입

특히 컨테이너에서 해석되는 클래스(예: [컨트롤러](/docs/{{version}}/controllers), [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등) 생성자에서 의존성을 타입힌트로 지정하면 자동으로 주입됩니다. 또한 [큐 잡](/docs/{{version}}/queues)의 `handle` 메서드에서도 의존성을 타입힌트할 수 있습니다.  
실제로 여러분 대부분의 객체는 이 방식으로 컨테이너에서 해석되길 원할 것입니다.

예를 들어, 애플리케이션에서 정의한 서비스를 컨트롤러 생성자에서 타입힌트하면, 해당 서비스가 자동으로 해석되어 주입됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;

class PodcastController extends Controller
{
    /**
     * 새 컨트롤러 인스턴스 생성.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * 주어진 팟캐스트의 정보 출력.
     */
    public function show(string $id): Podcast
    {
        return $this->apple->findPodcast($id);
    }
}
```

<a name="method-invocation-and-injection"></a>
## 메서드 호출과 주입

객체의 메서드를 호출하면서, 해당 메서드의 의존성도 컨테이너가 자동으로 주입해주길 원할 때가 있습니다. 예를 들어 다음과 같은 클래스가 있다고 합시다:

```php
<?php

namespace App;

use App\Services\AppleMusic;

class PodcastStats
{
    /**
     * 새 팟캐스트 통계 리포트 생성.
     */
    public function generate(AppleMusic $apple): array
    {
        return [
            // ...
        ];
    }
}
```

컨테이너를 통해 `generate` 메서드를 다음과 같이 호출할 수 있습니다:

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 PHP의 어떤 callable도 받을 수 있습니다. 컨테이너의 `call` 메서드는 클로저를 호출할 때도 자동으로 의존성을 주입해줍니다:

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트

서비스 컨테이너는 객체를 해석할 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 이용해 해당 이벤트를 리스닝할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입 객체가 해석될 때 호출됨...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 어떤 타입이든 객체가 해석될 때 호출됨...
});
```

이렇게 해석 중인 객체를 콜백에 전달받아, 소비자에게 전달되기 전에 필요한 속성을 추가로 설정할 수 있습니다.

<a name="rebinding"></a>
### 재바인딩(Rebinding)

`rebinding` 메서드는 서비스가 재등록되거나, 기존 바인딩이 덮어써질 때마다 동작하는 이벤트를 리스닝할 수 있게 해줍니다.  
이는 특정 바인딩이 업데이트될 때마다 의존성이나 동작을 수정하고 싶을 때 유용합니다:

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

// 새 바인딩이 등록되면 rebinding 콜백이 호출됨...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

라라벨의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다.  
따라서, PSR-11 컨테이너 인터페이스를 타입힌트로 지정하여 라라벨 컨테이너 인스턴스를 받아올 수 있습니다:

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

만약 주어진 식별자를 해석할 수 없다면 예외가 발생합니다.  
식별자가 한 번도 바인딩된 적 없으면 `Psr\Container\NotFoundExceptionInterface`의 인스턴스 예외가 발생하고,  
바인딩은 되어 있으나 해석에 실패하면 `Psr\Container\ContainerExceptionInterface`의 인스턴스 예외가 발생합니다.