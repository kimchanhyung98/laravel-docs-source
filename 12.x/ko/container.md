# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [무설정 해석 (Zero Configuration Resolution)](#zero-configuration-resolution)
    - [컨테이너를 언제 사용해야 하나?](#when-to-use-the-container)
- [바인딩 (Binding)](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [컨텍스트 바인딩](#contextual-binding)
    - [컨텍스트 속성](#contextual-attributes)
    - [기본 자료형 바인딩](#binding-primitives)
    - [타입을 지정한 가변 인자 바인딩](#binding-typed-variadics)
    - [태깅](#tagging)
    - [바인딩 확장하기](#extending-bindings)
- [해결 (Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 주입](#automatic-injection)
- [메서드 호출 및 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
    - [재바인딩](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 서비스 컨테이너는 클래스 의존성을 관리하고 의존성 주입(dependency injection)을 수행하는 강력한 도구입니다. 의존성 주입이라는 용어는 결국 다음을 의미합니다: 클래스가 필요한 의존성을 생성자 또는 경우에 따라 “세터(setter)” 메서드 등을 통해 “주입” 받는다는 뜻입니다.

간단한 예제를 살펴보겠습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;
use Illuminate\View\View;

class PodcastController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스 생성.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * 특정 팟캐스트 정보 조회.
     */
    public function show(string $id): View
    {
        return view('podcasts.show', [
            'podcast' => $this->apple->findPodcast($id)
        ]);
    }
}
```

이 예제에서 `PodcastController`는 Apple Music 같은 데이터 소스에서 팟캐스트를 가져와야 합니다. 그래서 팟캐스트를 가져올 수 있는 서비스를 **주입**합니다. 서비스가 주입되므로 애플리케이션 테스트 시 `AppleMusic` 서비스의 가짜(모의, mock) 구현을 쉽게 만들 수 있습니다.

Laravel 서비스 컨테이너에 대한 깊은 이해는 강력하고 큰 규모의 애플리케이션을 구축하고, Laravel 코어 개발에 기여하는 데 필수적입니다.

<a name="zero-configuration-resolution"></a>
### 무설정 해석 (Zero Configuration Resolution)

클래스가 의존성이 없거나 오직 구체 클래스(인터페이스가 아닌)에만 의존한다면, 컨테이너에 그 클래스를 어떻게 해결할지 명시할 필요가 없습니다. 예를 들어 다음 코드를 `routes/web.php`에 작성할 수 있습니다:

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

이 예에서, 애플리케이션의 `/` 라우트를 요청하면 자동으로 `Service` 클래스가 해석되어 라우트 핸들러에 주입됩니다. 이 기능은 매우 혁신적입니다. 즉, 뻥튀기된 설정 파일을 걱정하지 않고도 의존성 주입을 활용해 애플리케이션을 개발할 수 있다는 뜻입니다.

운 좋게도, Laravel 애플리케이션을 구축할 때 작성하는 많은 클래스는 [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등 컨테이너를 통해 의존성을 자동으로 주입받습니다. 또한, [큐 작업](/docs/12.x/queues)의 `handle` 메서드에서도 의존성 주입을 타입힌트할 수 있습니다. 자동 의존성 주입과 무설정 해석이 주는 강력함을 맛보면 없이는 개발하기 어려워집니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 언제 사용해야 하나? (When to Utilize the Container)

무설정 해석 덕분에 라우트, 컨트롤러, 이벤트 리스너 등에서 의존성을 타입힌트하는 일이 일반적이며 대부분 직접 컨테이너를 다룰 필요가 없습니다. 예를 들어 라우트 정의에 `Illuminate\Http\Request` 객체를 타입힌트해 현재 요청에 쉽게 접근할 수 있습니다. 컨테이너와 직접 상호 작용하지 않아도, 내부적으로는 해당 의존성이 자동으로 주입됩니다:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

대부분 경우, 자동 의존성 주입과 [파사드](/docs/12.x/facades) 덕분에 컨테이너에 수동으로 바인딩하거나 인스턴스를 해결하지 않아도 됩니다. 그렇다면 언제 컨테이너를 직접 조작할까요? 두 가지 상황을 살펴보겠습니다.

첫째, 인터페이스를 구현하는 클래스를 작성하고, 해당 인터페이스를 라우트 또는 생성자에 타입힌트할 때는 [컨테이너에 인터페이스를 어떻게 해결할지 알려줘야 합니다](#binding-interfaces-to-implementations). 둘째, 다른 Laravel 개발자와 공유할 Laravel 패키지를 작성 중이라면, 패키지 서비스들을 컨테이너에 바인딩해야 할 수도 있습니다.

---

<a name="binding"></a>
## 바인딩 (Binding)

<a name="binding-basics"></a>
### 바인딩 기본

<a name="simple-bindings"></a>
#### 단순 바인딩

대부분 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/12.x/providers) 내에서 등록하므로, 이 절의 예제 역시 그 환경에서 컨테이너를 사용하는 방식을 보여줍니다.

서비스 프로바이더 안에서는 `$this->app` 프로퍼티로 컨테이너에 접근할 수 있습니다. `bind` 메서드를 사용해 바인딩을 등록할 때는, 등록할 클래스 또는 인터페이스 이름과 해당 클래스의 인스턴스를 반환하는 클로저를 인자로 넘겨줍니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

위 예에서 클로저는 컨테이너 인스턴스를 인수로 받고, 컨테이너를 이용해 서브 의존성을 재귀적으로 해결할 수 있습니다.

앞서 말했듯 서비스 프로바이더 내부에서 컨테이너를 다루는 게 일반적입니다. 하지만 프로바이더 바깥에서 컨테이너를 다루고 싶으면, `App` [파사드](/docs/12.x/facades)를 사용할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

`bindIf` 메서드를 사용하면, 주어진 타입에 아직 바인딩이 없을 경우에만 바인딩을 등록할 수 있습니다:

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

편리하게도, 바인딩할 클래스 또는 인터페이스 이름을 별도로 넘기지 않고 클로저 반환 타입 선언으로 Laravel이 바인딩 타입을 유추하도록 할 수도 있습니다:

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 클래스가 인터페이스에 의존하지 않는다면 컨테이너에 바인딩할 필요가 없습니다. 이런 클래스는 리플렉션을 통해 자동으로 해결되기 때문입니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩

`singleton` 메서드는 클래스나 인터페이스를 컨테이너에 단 한 번만 생성/해결하도록 바인딩합니다. 싱글톤 바인딩의 경우, 첫 해석 이후에는 같은 인스턴스를 반환합니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`singletonIf` 메서드도 `bindIf`와 유사하게, 아직 등록되지 않은 타입에 한해 싱글톤 바인딩을 등록합니다:

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

또는 `#[Singleton]` 어트리뷰트를 클래스나 인터페이스에 붙여 컨테이너가 단일 인스턴스로 해석하도록 지정할 수도 있습니다:

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
#### 스코프드 싱글톤 바인딩

`scoped` 메서드는 싱글톤과 비슷하지만, Laravel 요청 또는 작업(job) 라이프사이클 동안에만 단일 인스턴스를 유지합니다. `scoped`로 등록된 인스턴스는 Laravel 애플리케이션이 새로운 라이프사이클을 시작할 때(예: [Laravel Octane](/docs/12.x/octane) 워커가 새 요청을 처리하거나, Laravel [큐 워커](/docs/12.x/queues)가 새 작업을 처리할 때) 초기화됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`scopedIf` 메서드를 사용하면 아직 바인딩이 등록되지 않은 경우에 스코프드 바인딩을 등록합니다:

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

또는 `#[Scoped]` 어트리뷰트를 붙여 Laravel 요청/작업 라이프사이클 내에서 단일 인스턴스가 되도록 지정할 수도 있습니다:

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

기존 객체 인스턴스를 컨테이너에 바인딩할 수도 있습니다. `instance` 메서드를 사용하며, 전달된 인스턴스는 컨테이너가 해결할 때 항상 반환됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기 (Binding Interfaces to Implementations)

서비스 컨테이너의 강력한 기능 중 하나는 인터페이스를 특정 구현체에 바인딩하는 능력입니다. 예를 들어 `EventPusher` 인터페이스와 `RedisEventPusher` 구현체가 있다고 가정하면, 구현체를 다음과 같이 바인딩할 수 있습니다:

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이 선언은 컨테이너에게 `EventPusher` 인터페이스가 필요할 때 `RedisEventPusher` 인스턴스를 주입하도록 지시합니다. 이제 컨테이너가 해석하는 클래스 생성자에 `EventPusher`를 타입힌트할 수 있습니다. 컨트롤러, 이벤트 리스너, 미들웨어 등 Laravel의 많은 클래스는 항상 컨테이너를 통해 해석되니까요:

```php
use App\Contracts\EventPusher;

/**
 * 클래스 인스턴스 생성.
 */
public function __construct(
    protected EventPusher $pusher,
) {}
```

<a name="contextual-binding"></a>
### 컨텍스트 바인딩 (Contextual Binding)

때때로 두 개 이상의 클래스가 같은 인터페이스를 사용하지만, 각 클래스에 서로 다른 구현체를 주입하고 싶을 수 있습니다. 예를 들어 두 개의 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` [컨트랙트](/docs/12.x/contracts)의 다른 구현체에 의존할 수 있습니다. Laravel은 이런 동작을 정의할 수 있는 간단하고 직관적인 인터페이스를 제공합니다:

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

컨텍스트 바인딩이 드라이버 구현체나 구성 값 주입에 자주 사용되므로, Laravel은 이를 수동으로 서비스 프로바이더에 정의하지 않고도 주입할 수 있는 여러 컨텍스트 바인딩용 어트리뷰트를 제공합니다.

예를 들어, 특정 [스토리지 디스크](/docs/12.x/filesystem)를 주입할 때 `Storage` 어트리뷰트를 사용할 수 있습니다:

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

`Storage` 어트리뷰트 외에도, Laravel은 `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RouteParameter`, [Tag](#tagging) 어트리뷰트를 제공합니다:

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

또한, 로그인한 현재 사용자 정보를 주입하는 `CurrentUser` 어트리뷰트도 Laravel에서 제공합니다:

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 커스텀 어트리뷰트 정의하기

`Illuminate\Contracts\Container\ContextualAttribute` 컨트랙트를 구현해 직접 컨텍스트 어트리뷰트를 만들 수 있습니다. 컨테이너는 해당 어트리뷰트의 `resolve` 메서드를 호출하여, 어트리뷰트를 사용하는 클래스에 주입할 값을 반환해야 합니다. 아래 예에서는 Laravel 내장 `Config` 어트리뷰트를 다시 구현해보았습니다:

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
     * 새로운 어트리뷰트 인스턴스 생성.
     */
    public function __construct(public string $key, public mixed $default = null)
    {
    }

    /**
     * 구성 값을 해결.
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
### 기본 자료형 바인딩 (Binding Primitives)

어떤 클래스는 클래스 인스턴스뿐 아니라 정수 같은 기본 자료형도 주입받아야 할 수 있습니다. 이런 경우 컨텍스트 바인딩을 통해 필요한 값을 주입할 수 있습니다:

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

클래스가 [태그된](#tagging) 인스턴스 배열에 의존할 때도 있습니다. 이 경우 `giveTagged` 메서드를 사용해 같은 태그를 가진 컨테이너 바인딩 모두를 쉽게 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션 설정 파일에서 값을 주입해야 한다면, `giveConfig` 메서드를 사용할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입을 지정한 가변 인자 바인딩 (Binding Typed Variadics)

가끔 클래스 생성자가 타입힌트된 가변 인자 배열을 받을 때가 있습니다:

```php
<?php

use App\Models\Filter;
use App\Services\Logger;

class Firewall
{
    /**
     * 필터 인스턴스 배열.
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

컨텍스트 바인딩을 사용해, `Give` 메서드에 `Filter` 인스턴스 배열을 반환하는 클로저를 제공해 이 의존성을 해결할 수 있습니다:

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

또는 편하게 `Filter` 클래스 이름 배열을 제공해도 컨테이너가 자동으로 해결합니다:

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

`Report ...$reports`와 같은 가변 인자가 특정 클래스로 타입힌트돼 있을 때는, `needs`와 `giveTagged` 메서드를 사용해 해당 태그(`reports`)가 붙은 모든 바인딩을 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅 (Tagging)

때로는 특정 “카테고리”의 바인딩 전부를 한꺼번에 해결해야 할 때가 있습니다. 예를 들어 여러 `Report` 인터페이스 구현체를 배열로 받는 리포트 분석기를 만들고 싶을 수 있습니다. 구현체를 바인딩한 후 `tag` 메서드로 태그를 할당할 수 있습니다:

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

태그가 할당된 서비스는 컨테이너의 `tagged` 메서드로 쉽게 모두 해결할 수 있습니다:

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장하기 (Extending Bindings)

`extend` 메서드를 사용하면 해석된 서비스를 수정할 수 있습니다. 예를 들어 서비스 해석 시 추가 로직을 실행해 서비스 인스턴스를 확장(데코레이트)하거나 설정할 수 있습니다. `extend`는 두 개의 인수를 받는데, 확장할 서비스 클래스와 수정된 서비스를 반환하는 클로저입니다. 클로저는 현재 서비스 인스턴스와 컨테이너 인스턴스를 받습니다:

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

---

<a name="resolving"></a>
## 해결 (Resolving)

<a name="the-make-method"></a>
### `make` 메서드

`make` 메서드를 사용해 컨테이너에서 클래스 인스턴스를 해결할 수 있습니다. `make`는 클래스 또는 인터페이스 이름을 인수로 받습니다:

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스 의존성 중 일부가 컨테이너에서 해결되지 않을 경우, `makeWith` 메서드를 사용해 연관 배열로 직접 주입할 수도 있습니다. 예를 들어, `Transistor` 서비스 생성자의 `$id` 인수를 수동으로 넘길 수 있습니다:

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드는 특정 클래스나 인터페이스가 컨테이너에 명시적으로 바인딩되었는지 확인할 때 사용합니다:

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더 밖에서 `$app` 변수를 쓸 수 없는 경우, `App` [파사드](/docs/12.x/facades) 또는 `app` [헬퍼](/docs/12.x/helpers#method-app)를 사용해 컨테이너에서 인스턴스를 해결할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

컨테이너 인스턴스 자체를 주입받고 싶다면, 클래스 생성자에 `Illuminate\Container\Container` 클래스를 타입힌트하면 됩니다:

```php
use Illuminate\Container\Container;

/**
 * 클래스 인스턴스 생성.
 */
public function __construct(
    protected Container $container,
) {}
```

<a name="automatic-injection"></a>
### 자동 주입 (Automatic Injection)

중요하게도, 컨테이너에 의해 해석되는 클래스 생성자에서 의존성을 타입힌트할 수 있습니다. 여기에는 [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등이 포함됩니다. 또한 [큐 작업](/docs/12.x/queues) `handle` 메서드에서도 의존성을 타입힌트할 수 있습니다. 실제로 대부분 객체는 이렇게 컨테이너가 자동 해결합니다.

예를 들어, 컨트롤러 생성자에 애플리케이션이 정의한 서비스를 타입힌트하면 컨테이너가 자동으로 인스턴스를 만들어 주입합니다:

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
     * 특정 팟캐스트 정보 조회.
     */
    public function show(string $id): Podcast
    {
        return $this->apple->findPodcast($id);
    }
}
```

---

<a name="method-invocation-and-injection"></a>
## 메서드 호출 및 주입 (Method Invocation and Injection)

컨테이너가 특정 객체 인스턴스의 메서드를 호출하면서, 해당 메서드가 필요로 하는 의존성을 자동으로 주입하도록 할 수 있습니다. 예를 들어 다음 클래스를 가정해봅시다:

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

이 객체의 `generate` 메서드를 컨테이너를 통해 호출하려면 다음과 같이 합니다:

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 어떤 PHP 호출(callable)도 받을 수 있으며, 클로저에 대해 자동으로 의존성을 주입해 실행할 수도 있습니다:

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

---

<a name="container-events"></a>
## 컨테이너 이벤트 (Container Events)

컨테이너는 객체를 해석할 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 사용해 이를 청취할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입 객체가 컨테이너에서 해석될 때 호출...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 모든 타입 객체가 컨테이너에서 해석될 때 호출...
});
```

객체가 콜백에 전달되므로, 서비스 사용자에게 넘겨지기 전에 추가 속성을 설정할 수 있습니다.

<a name="rebinding"></a>
### 재바인딩 (Rebinding)

`rebinding` 메서드는 서비스가 컨테이너에서 다시 바인딩(재등록 혹은 덮어쓰기) 될 때 청취할 수 있게 합니다. 특정 바인딩이 갱신될 때마다 의존성을 업데이트하거나 동작을 수정하고 싶을 때 유용합니다:

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

// 새로운 바인딩이 재바인딩 클로저를 트리거함...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

---

<a name="psr-11"></a>
## PSR-11

Laravel 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서 PSR-11 컨테이너 인터페이스를 타입힌트해 Laravel 컨테이너 인스턴스를 얻을 수 있습니다:

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

만약 주어진 식별자를 해결할 수 없으면 예외가 발생합니다. 식별자가 한 번도 바인딩되지 않은 경우엔 `Psr\Container\NotFoundExceptionInterface` 타입 예외가, 바인딩돼 있었지만 해결 실패 시 `Psr\Container\ContainerExceptionInterface` 타입 예외가 발생합니다.