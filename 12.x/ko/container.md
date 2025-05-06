# 서비스 컨테이너

- [소개](#introduction)
    - [제로 설정(Zero Configuration) 해결](#zero-configuration-resolution)
    - [컨테이너를 언제 사용할 것인가](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [상황별 바인딩](#contextual-binding)
    - [상황별 애트리뷰트](#contextual-attributes)
    - [원시값 바인딩(Primitives)](#binding-primitives)
    - [타입이 지정된 가변 인자 바인딩](#binding-typed-variadics)
    - [태깅(Tagging)](#tagging)
    - [바인딩 확장](#extending-bindings)
- [해결(Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 주입](#automatic-injection)
- [메서드 호출과 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
    - [리바인딩(Rebinding)](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개

Laravel 서비스 컨테이너는 클래스 간의 의존성을 관리하고 의존성 주입을 실행하는 강력한 도구입니다. 의존성 주입(Dependency Injection)은 클래스가 필요한 의존성을 생성자 또는 "세터(Setter)" 메서드를 통해 "주입"받는다는 의미입니다.

간단한 예제를 살펴보겠습니다.

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;
use Illuminate\View\View;

class PodcastController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스 생성자
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * 주어진 팟캐스트 정보 보여주기
     */
    public function show(string $id): View
    {
        return view('podcasts.show', [
            'podcast' => $this->apple->findPodcast($id)
        ]);
    }
}
```

이 예제에서 `PodcastController`는 Apple Music과 같은 데이터 소스에서 팟캐스트를 가져와야 합니다. 따라서 팟캐스트를 가져올 수 있는 서비스를 **주입**합니다. 서비스가 주입되기 때문에 테스트 시 `AppleMusic` 서비스의 더미 구현(mock)을 쉽게 사용할 수 있습니다.

Laravel 서비스 컨테이너에 대한 깊은 이해는 강력하고 대규모의 애플리케이션을 구축하거나, Laravel 코어에 기여할 때 매우 중요합니다.

<a name="zero-configuration-resolution"></a>
### 제로 설정(Zero Configuration) 해결

클래스가 의존성이 없거나, 다른 구체 클래스(인터페이스가 아님)에만 의존한다면, 컨테이너는 해당 클래스를 어떻게 해결할지 별도 지시가 필요하지 않습니다. 예를 들어, 아래와 같이 `routes/web.php`에 코드를 작성할 수 있습니다.

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

이 예제에서는, 애플리케이션의 `/` 라우트를 요청하면 `Service` 클래스가 자동으로 해결되어 핸들러로 주입됩니다. 이는 혁신적인 변화입니다. 별도의 복잡한 설정 파일 없이도 의존성 주입의 이점을 활용할 수 있습니다.

Laravel 애플리케이션을 빌드할 때 작성하는 많은 클래스(예: [컨트롤러](/docs/{{version}}/controllers), [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등)는 컨테이너를 통해 의존성이 자동으로 주입받습니다. 또한 [큐 작업](/docs/{{version}}/queues)의 `handle` 메서드에서도 의존성을 타입힌트로 지정할 수 있습니다. 자동·제로 설정 의존성 주입의 강력함을 경험하면, 이것 없이 개발하기가 불가능해집니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 언제 사용할 것인가

제로 설정 해결 기능 덕분에, 라우트, 컨트롤러, 이벤트 리스너 등에서 의존성을 타입힌트로 지정할 수 있으므로, 직접 컨테이너와 상호작용할 필요가 거의 없습니다. 예를 들어, 현재 요청을 쉽게 접근하기 위해 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입힌트로 사용할 수 있습니다. 이 코드를 작성할 때 직접 컨테이너를 다루지 않아도, 컨테이너가 이 의존성의 주입을 백그라운드에서 관리합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

자동 의존성 주입과 [파사드](/docs/{{version}}/facades) 덕분에, Laravel 애플리케이션을 **전혀** 직접 바인딩이나 해결을 하지 않고도 개발할 수 있습니다. **그렇다면 실제로 컨테이너를 직접 사용할 때는 언제일까요?** 두 가지 상황을 살펴보겠습니다.

첫째, 만약 인터페이스를 구현한 클래스를 작성하고, 그 인터페이스를 라우트나 클래스 생성자에서 타입힌트로 지정하고 싶다면, [컨테이너에 인터페이스를 어떻게 해결할지 알려줘야](#binding-interfaces-to-implementations) 합니다. 두 번째로, [Laravel 패키지](/docs/{{version}}/packages)를 작성하여 다른 개발자와 공유하려는 경우, 패키지의 서비스를 컨테이너에 바인딩해야 할 수 있습니다.

<a name="binding"></a>
## 바인딩

<a name="binding-basics"></a>
### 바인딩 기본

<a name="simple-bindings"></a>
#### 간단한 바인딩

대부분의 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/{{version}}/providers) 내에서 등록됩니다. 따라서 아래 예제들도 그 문맥 안에서 컨테이너를 사용하는 방식을 보여줍니다.

서비스 프로바이더 내에서는 항상 `$this->app` 속성을 통해 컨테이너에 접근할 수 있습니다. `bind` 메서드를 사용하여 바인딩을 등록할 수 있는데, 등록하려는 클래스 또는 인터페이스명과, 해당 클래스 인스턴스를 반환하는 클로저를 전달합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

해결자에는 컨테이너 자체가 인자로 전달됩니다. 따라서, 생성중인 객체의 하위 의존성도 컨테이너를 이용해 해결할 수 있습니다.

언급했듯, 보통 서비스 프로바이더 안에서 컨테이너와 상호작용하지만, 만약 서비스 프로바이더 바깥에서 컨테이너를 사용하려면, `App` [파사드](/docs/{{version}}/facades)를 사용할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

`bindIf` 메서드를 사용하면, 지정한 타입에 바인딩이 아직 등록되지 않았을 경우만 바인딩을 등록할 수 있습니다.

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

편의를 위해, 등록하려는 클래스/인터페이스명을 별도의 인자로 전달하지 않고, 클로저의 반환 타입에서 Laravel이 타입을 추론하게 할 수도 있습니다.

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 인터페이스에 의존하지 않는 클래스라면 굳이 컨테이너에 바인딩할 필요가 없습니다. 컨테이너는 리플렉션을 이용해 해당 객체를 자동으로 생성할 수 있습니다.

<a name="binding-a-singleton"></a>
#### 싱글턴 바인딩

`singleton` 메서드는 해당 클래스나 인터페이스를 한 번만 해결해야 함을 의미합니다. 한 번 해결된 싱글턴 바인딩은 이후 컨테이너에서 동일 인스턴스를 반환합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`sngletonIf` 메서드는, 이미 지정한 타입에 바인딩이 등록되어 있지 않은 경우에만 싱글턴 바인딩을 등록합니다.

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 스코프드(Scoped) 싱글턴 바인딩

`scoped` 메서드는, 해당 클래스/인터페이스가 Laravel의 요청/작업 라이프사이클 내에서 한 번만 해결됨을 의미합니다. 이 메서드는 `singleton`과 비슷하지만, [Laravel Octane](/docs/{{version}}/octane) 워커가 새 요청을 처리하거나, [큐 워커](/docs/{{version}}/queues)가 새 작업을 처리할 때마다 인스턴스가 초기화됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`scopedIf` 메서드는 조건부로 스코프드 바인딩을 등록합니다.

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩

이미 생성된 객체 인스턴스를 `instance` 메서드를 통해 컨테이너에 바인딩할 수도 있습니다. 해당 인스턴스는 이후 컨테이너에서 항상 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기

서비스 컨테이너의 매우 강력한 기능은 인터페이스에 대한 구체 구현체를 지정하여 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher` 인터페이스와 `RedisEventPusher` 구현체가 있다고 가정해 보겠습니다. 이제 해당 구현체를 서비스 컨테이너에 다음과 같이 등록할 수 있습니다.

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이 명령은, 어떤 클래스가 `EventPusher` 구현이 필요할 때마다 `RedisEventPusher`를 주입하라고 컨테이너에 알려줍니다. 이제 컨테이너가 해결하는 클래스의 생성자에서 `EventPusher` 인터페이스를 타입힌트로 지정할 수 있습니다. 컨트롤러, 이벤트 리스너, 미들웨어 등 대부분이 컨테이너를 통해 해결됩니다.

```php
use App\Contracts\EventPusher;

/**
 * 새로운 클래스 인스턴스 생성자
 */
public function __construct(
    protected EventPusher $pusher,
) {}
```

<a name="contextual-binding"></a>
### 상황별 바인딩

같은 인터페이스를 사용하는 두 개 클래스에, 각각 다른 구현체를 주입하고 싶을 때가 있습니다. 예를 들어 두 컨트롤러가 각기 다른 `Illuminate\Contracts\Filesystem\Filesystem` [계약](/docs/{{version}}/contracts) 구현체에 의존할 수 있습니다. 이 경우 Laravel은 간단하고 유창한 인터페이스를 제공합니다.

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
### 상황별 애트리뷰트

상황별 바인딩은 드라이버나 설정값 등의 구현 주입에 자주 사용됩니다. Laravel은 서비스 프로바이더에서 바인딩을 수동 정의하지 않고도 이런 값을 주입할 수 있는 다양한 상황별 애트리뷰트를 제공합니다.

예를 들어, `Storage` 애트리뷰트를 사용하여 특정 [스토리지 디스크](/docs/{{version}}/filesystem)를 주입할 수 있습니다.

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

이외에도, Laravel은 `Auth`, `Cache`, `Config`, `DB`, `Log`, `RouteParameter`, 그리고 [Tag](#tagging) 애트리뷰트를 제공합니다.

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

또한, 현재 인증된 사용자를 주입하는 `CurrentUser` 애트리뷰트도 제공합니다.

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 커스텀 애트리뷰트 정의

`Illuminate\Contracts\Container\ContextualAttribute` 계약을 구현하여 사용자 지정 상황별 애트리뷰트를 만들 수 있습니다. 컨테이너는 애트리뷰트의 `resolve` 메서드를 호출하여 주입할 값을 반환받습니다. 아래는 Laravel의 내장 `Config` 애트리뷰트를 재구현한 예시입니다.

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
     * 애트리뷰트 인스턴스 생성자
     */
    public function __construct(public string $key, public mixed $default = null)
    {
    }

    /**
     * 설정 값 해결
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

클래스가 일부는 객체 의존성이고, 일부는 정수 등 원시값을 필요로 할 때가 있습니다. 상황별 바인딩을 통해 아무 값이나 주입할 수 있습니다.

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

클래스가 [태그된](#tagging) 인스턴스의 배열에 의존할 수도 있습니다. `giveTagged` 메서드를 이용해 해당 태그로 바인딩된 모두를 쉽게 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

설정 파일에서 값을 주입하려면, `giveConfig` 메서드를 사용할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입이 지정된 가변 인자 바인딩

가끔, 가변 인자(variadic)로 타입이 지정된 객체 배열을 받아야 할 때가 있습니다.

```php
<?php

use App\Models\Filter;
use App\Services\Logger;

class Firewall
{
    /**
     * 필터 인스턴스들
     *
     * @var array
     */
    protected $filters;

    /**
     * 새로운 클래스 인스턴스 생성자
     */
    public function __construct(
        protected Logger $logger,
        Filter ...$filters,
    ) {
        $this->filters = $filters;
    }
}
```

상황별 바인딩에서, `give` 메서드에 해당 객체 배열을 반환하는 클로저를 제공하면 의존성을 해결할 수 있습니다.

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

또는, 바로 클래스명 배열만 넘겨주면 해당 타입 인스턴스가 컨테이너에서 해결됩니다.

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
#### 태그에 의한 가변 인자 의존성

클래스가 `Report ...$reports`처럼 특정 클래스를 타입힌트하는 가변 의존성을 가질 수 있습니다. `needs`와 `giveTagged` 메서드를 같이 쓰면 해당 [태그](#tagging)를 가진 모든 인스턴스를 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅

간혹 특정 "카테고리"의 바인딩 전체를 해결해야 할 때가 있습니다. 예를 들어, 다양한 `Report` 인터페이스 구현체 배열을 받아 처리하는 리포트 분석기를 만드는 경우입니다. 구현체들을 등록한 후, `tag` 메서드로 태그를 지정할 수 있습니다.

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

이후, `tagged` 메서드로 모두 한 번에 해결할 수 있습니다.

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장

`extend` 메서드는 이미 해결된 서비스를 수정할 수 있게 해줍니다. 예를 들어 서비스가 해결될 때 추가적인 데코레이션이나 구성 등의 코드를 실행할 수 있습니다. `extend` 메서드는 확장할 서비스 클래스와, 수정된 서비스를 반환하는 클로저를 인자로 받으며, 클로저에는 현재 서비스와 컨테이너 인스턴스가 전달됩니다.

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해결(Resolving)

<a name="the-make-method"></a>
### `make` 메서드

`make` 메서드를 사용하여 컨테이너에서 클래스 인스턴스를 해결할 수 있습니다. 인자로는 클래스 또는 인터페이스 이름을 지정합니다.

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스의 일부 의존성이 컨테이너로 해결할 수 없는 경우, `makeWith` 메서드의 두 번째 인자로 연관 배열을 전달해 직접 주입할 수 있습니다. 예를 들어, `Transistor` 서비스의 `$id` 생성자 인자를 직접 지정할 수 있습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드는 특정 클래스나 인터페이스가 컨테이너에 명시적으로 바인딩 되어있는지 여부를 판단합니다.

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더가 아닌 곳에서 `$app` 변수 없이 클래스 인스턴스를 얻으려면, `App` [파사드](/docs/{{version}}/facades)나 `app` [헬퍼](/docs/{{version}}/helpers#method-app)를 사용할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

컨테이너 인스턴스 자체를 주입받고 싶다면, 클래스 생성자에서 `Illuminate\Container\Container`를 타입힌트로 지정하면 됩니다.

```php
use Illuminate\Container\Container;

/**
 * 새로운 클래스 인스턴스 생성자
 */
public function __construct(
    protected Container $container,
) {}
```

<a name="automatic-injection"></a>
### 자동 주입

혹은, 클래스 생성자에 의존성을 타입힌트로 지정하면 컨테이너가 이를 자동으로 해결합니다. [컨트롤러](/docs/{{version}}/controllers), [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등과 [큐 작업](/docs/{{version}}/queues)의 `handle` 메서드에서도 동일합니다. 실제로 대부분의 객체는 이 방식을 통해 주입됩니다.

예를 들어, 컨트롤러 생성자에 직접 서비스 클래스를 타입힌트하면, 자동으로 해결되어 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;

class PodcastController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스 생성자
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * 주어진 팟캐스트 정보 보여주기
     */
    public function show(string $id): Podcast
    {
        return $this->apple->findPodcast($id);
    }
}
```

<a name="method-invocation-and-injection"></a>
## 메서드 호출과 주입

가끔, 객체 인스턴스의 메서드를 호출할 때, 그 메서드의 의존성을 컨테이너가 자동으로 주입하도록 하고 싶을 수 있습니다. 다음 클래스를 예로 들겠습니다.

```php
<?php

namespace App;

use App\Services\AppleMusic;

class PodcastStats
{
    /**
     * 새 팟캐스트 통계 리포트 생성
     */
    public function generate(AppleMusic $apple): array
    {
        return [
            // ...
        ];
    }
}
```

컨테이너를 통해 `generate` 메서드를 호출할 수 있습니다.

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 PHP의 어떤 콜러블도 받을 수 있습니다. 클로저의 의존성도 자동으로 주입할 수 있습니다.

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트

서비스 컨테이너는 객체를 해결(resolving)할 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 통해 이 이벤트를 구독할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입일 때 호출됨...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 모든 타입의 객체 해결 시 호출됨...
});
```

이벤트 콜백에서 해결되는 객체에 추가적인 속성을 세팅하거나 구성할 수 있습니다.

<a name="rebinding"></a>
### 리바인딩(Rebinding)

`rebinding` 메서드는 서비스가 컨테이너에 다시 바인딩되거나 초기 바인딩 후 덮어쓰기가 될 때마다 감지할 수 있게 해줍니다. 의존성 업데이트나 바인딩 변경 시 동작을 수정하고 싶을 때 유용합니다.

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

// 새로운 바인딩이 리바인딩 콜백을 트리거함...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

Laravel 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서, PSR-11 컨테이너 인터페이스를 타입힌트하여 Laravel 컨테이너 인스턴스를 받아올 수 있습니다.

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

만약 주어진 식별자를 해결할 수 없다면 예외가 발생합니다. 해당 식별자가 한 번도 바인딩된 적 없으면 `Psr\Container\NotFoundExceptionInterface` 예외가, 바인딩은 되었지만 해결할 수 없으면 `Psr\Container\ContainerExceptionInterface` 예외가 발생합니다.
