# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [무설정 자동 해석 (Zero Configuration Resolution)](#zero-configuration-resolution)
    - [컨테이너 사용 시기](#when-to-use-the-container)
- [바인딩 (Binding)](#binding)
    - [바인딩 기초](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [컨텍스츄얼 바인딩 (Contextual Binding)](#contextual-binding)
    - [컨텍스츄얼 속성 (Contextual Attributes)](#contextual-attributes)
    - [원시 값 바인딩 (Binding Primitives)](#binding-primitives)
    - [타입드 가변 인자 바인딩 (Binding Typed Variadics)](#binding-typed-variadics)
    - [태깅 (Tagging)](#tagging)
    - [바인딩 확장 (Extending Bindings)](#extending-bindings)
- [해결 (Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 주입 (Automatic Injection)](#automatic-injection)
- [메서드 호출 및 주입 (Method Invocation and Injection)](#method-invocation-and-injection)
- [컨테이너 이벤트 (Container Events)](#container-events)
    - [재바인딩 (Rebinding)](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개 (Introduction)

라라벨 서비스 컨테이너는 클래스 간 의존관계를 관리하고 의존성 주입을 수행하는 강력한 도구입니다. 의존성 주입은 본질적으로 클래스가 필요로 하는 의존성을 생성자 혹은 경우에 따라 "세터(setter)" 메서드를 통해 주입받는 것을 의미하는 전문 용어입니다.

간단한 예제를 보겠습니다:

```
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;
use Illuminate\View\View;

class PodcastController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스 생성자.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * 지정된 팟캐스트 정보를 보여줍니다.
     */
    public function show(string $id): View
    {
        return view('podcasts.show', [
            'podcast' => $this->apple->findPodcast($id)
        ]);
    }
}
```

이 예제에서 `PodcastController`는 Apple Music 같은 데이터 소스에서 팟캐스트를 가져와야 합니다. 따라서 팟캐스트를 조회할 수 있는 서비스를 **주입(inject)** 합니다. 이 서비스가 주입되기 때문에, 테스트 시 이 `AppleMusic` 서비스를 쉽게 "모킹(mock)"하거나 더미 구현체를 만들어 사용할 수 있습니다.

라라벨 서비스 컨테이너를 깊게 이해하는 것은 강력하고 대규모 애플리케이션을 구축하고, 나아가 라라벨 코어 자체에 기여하는 데 필수적입니다.

<a name="zero-configuration-resolution"></a>
### 무설정 자동 해석 (Zero Configuration Resolution)

클래스에 의존성이 없거나 오직 구체 클래스(인터페이스가 아닌)만 의존성이 있을 경우, 컨테이너에 해당 클래스를 해석하는 방법을 명시하지 않아도 됩니다. 예를 들어, `routes/web.php` 파일에 다음 코드를 넣을 수 있습니다:

```
<?php

class Service
{
    // ...
}

Route::get('/', function (Service $service) {
    die($service::class);
});
```

이 예제에서 애플리케이션의 `/` 경로에 접근하면 `Service` 클래스가 자동으로 해석되어 라우트 핸들러에 주입됩니다. 이것은 큰 혁신입니다. 설정 파일 없이도 의존성 주입을 쉽게 이용하며 애플리케이션을 개발할 수 있음을 의미합니다.

행운스럽게도, 라라벨 애플리케이션을 구성하는 많은 클래스들은 (예: [컨트롤러](/docs/11.x/controllers), [이벤트 리스너](/docs/11.x/events), [미들웨어](/docs/11.x/middleware) 등) 자동으로 컨테이너를 통해 의존성을 받습니다. 또한 [큐 작업](/docs/11.x/queues) `handle` 메서드에서도 의존성을 타입힌팅할 수 있습니다. 이 자동 의존성 주입의 위력을 맛본 후에는 거의 없어서는 안 될 필수 기능처럼 느껴질 것입니다.

<a name="when-to-use-the-container"></a>
### 컨테이너 사용 시기 (When to Utilize the Container)

무설정 자동 해석 덕분에 라우트, 컨트롤러, 이벤트 리스너 등에서 대부분 의존성을 타입힌트하고 별도의 컨테이너 조작 없이 사용할 것입니다. 예를 들어 다음과 같이 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입힌팅해 현재 요청에 쉽게 접근할 수 있습니다. 이 코드를 작성할 때 컨테이너를 직접 다루지 않아도, 내부적으로 의존성 주입을 컨테이너가 처리합니다:

```
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

대부분 경우, 자동 의존성 주입과 [파사드](/docs/11.x/facades) 덕분에 라라벨 애플리케이션을 개발할 때 컨테이너에 명시적으로 바인딩하거나 해석을 시도할 필요가 **전혀 없을 수도 있습니다**. 그렇다면 **언제 컨테이너를 직접 다뤄야 할까요?** 두 가지 상황을 살펴봅시다.

첫째, 인터페이스를 구현한 클래스를 작성하고 그 인터페이스를 라우트나 생성자에서 타입힌팅할 경우, 그 인터페이스를 어떻게 해석할지 컨테이너에 알려줘야 합니다([인터페이스 바인딩](#binding-interfaces-to-implementations)). 둘째, 다른 라라벨 개발자와 공유할 라라벨 패키지를 작성할 때 패키지의 서비스를 컨테이너에 바인딩해야 할 수 있습니다.

<a name="binding"></a>
## 바인딩 (Binding)

<a name="binding-basics"></a>
### 바인딩 기초 (Binding Basics)

<a name="simple-bindings"></a>
#### 기본 바인딩 (Simple Bindings)

거의 모든 서비스 컨테이너 바인딩은 보통 [서비스 프로바이더](/docs/11.x/providers)에서 등록하기 때문에, 바인딩 예제들도 이 문맥에서 설명합니다.

서비스 프로바이더 내에서는 언제나 `$this->app` 속성을 통해 컨테이너에 접근할 수 있습니다. `bind` 메서드를 이용해 등록하려는 클래스 혹은 인터페이스 이름과, 해당 클래스를 반환하는 클로저를 넘겨 바인딩할 수 있습니다:

```
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

예제에서 알 수 있듯이, 클로저 인자로 컨테이너 인스턴스가 전달되며 이를 활용해 의존하는 서브 의존성을 직접 해석할 수 있습니다.

앞서 말했듯 보통은 서비스 프로바이더에서 컨테이너를 다루지만, 서비스 프로바이더 밖에서는 `App` [파사드](/docs/11.x/facades)를 통해 컨테이너와 상호작용할 수 있습니다:

```
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

또한 `bindIf` 메서드는 특정 타입에 대한 바인딩이 아직 등록되어 있지 않은 경우에만 바인딩을 등록합니다:

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]  
> 의존하는 인터페이스가 없는 클래스는 컨테이너에 바인딩할 필요가 없습니다. 리플렉션을 통해 자동으로 인스턴스 생성이 가능하기 때문입니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩 (Binding A Singleton)

`singleton` 메서드는 클래스나 인터페이스를 컨테이너에 단 한 번만 해석되도록 바인딩합니다. 이후 여러 번 요청 시 동일 객체 인스턴스가 반환됩니다:

```
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`singletonIf` 메서드는 아직 바인딩 등록이 안 된 타입에 한해 싱글톤 바인딩을 등록합니다:

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 요청 범위 내 싱글톤 바인딩 (Binding Scoped Singletons)

`scoped` 메서드는 특정 Laravel 요청 또는 작업 수명주기 내에서만 인스턴스가 하나만 생성되는 싱글톤으로 바인딩합니다. `singleton`과 유사하지만, `scoped` 바인딩은 Laravel 애플리케이션에서 새로운 "수명주기"가 시작되면 인스턴스가 초기화됩니다. 예를 들어 [Laravel Octane](/docs/11.x/octane) 워커가 새로운 요청을 처리하거나, [큐 워커](/docs/11.x/queues)가 새로운 작업을 처리할 때 초기화됩니다:

```
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`scopedIf` 메서드는 아직 바인딩이 등록되어 있지 않은 경우에만 scoped 바인딩을 설정합니다:

```
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩 (Binding Instances)

이미 생성된 객체 인스턴스를 컨테이너에 바인딩할 경우 `instance` 메서드를 사용합니다. 해당 인스턴스는 컨테이너에서 지속적으로 반환됩니다:

```
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기 (Binding Interfaces to Implementations)

서비스 컨테이너의 매우 강력한 기능은 인터페이스를 특정 구현체에 바인딩하는 것입니다. 예를 들어, `EventPusher`라는 인터페이스와 `RedisEventPusher` 구현체가 있다고 하면, `RedisEventPusher` 클래스를 서비스 컨테이너에 다음과 같이 등록할 수 있습니다:

```
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이 선언은 `EventPusher` 구현체가 필요하면 컨테이너가 `RedisEventPusher`를 주입해야 한다고 명시하는 것입니다. 이후 컨테이너가 해석하는 클래스 생성자에서 `EventPusher` 인터페이스를 타입힌팅하면 `RedisEventPusher`가 자동 주입됩니다. 라라벨 내에서 컨트롤러, 이벤트 리스너, 미들웨어 등 여러 클래스가 항상 컨테이너를 통해 해석된다는 점을 기억하세요:

```
use App\Contracts\EventPusher;

/**
 * 새 클래스 인스턴스 생성자.
 */
public function __construct(
    protected EventPusher $pusher,
) {}
```

<a name="contextual-binding"></a>
### 컨텍스츄얼 바인딩 (Contextual Binding)

같은 인터페이스를 여러 클래스가 사용하지만, 각 클래스마다 다른 구현체를 주입해야 할 때가 있습니다. 예를 들어, 두 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` [계약](/docs/11.x/contracts)을 다르게 구현한 객체를 필요로 하는 경우가 그런 경우입니다. 라라벨은 이를 위한 간단하고 직관적인 인터페이스를 제공합니다:

```
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
### 컨텍스츄얼 속성 (Contextual Attributes)

컨텍스츄얼 바인딩은 주로 드라이버 구현체나 설정 값을 주입할 때 사용되는데, 라라벨은 이를 더욱 쉽게 하도록 여러 컨텍스츄얼 바인딩 속성(Attribute)을 제공합니다.

예를 들어, `Storage` 속성은 특정 [스토리지 디스크](/docs/11.x/filesystem)를 주입하도록 도와줍니다:

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

`Storage` 속성 외에도, 라라벨은 `Auth`, `Cache`, `Config`, `DB`, `Log`, `RouteParameter`, 그리고 [`Tag`](#tagging) 속성을 제공합니다:

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

또한 현재 인증된 사용자를 특정 라우트나 클래스에 주입하는 `CurrentUser` 속성도 제공합니다:

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 사용자 정의 속성 만들기 (Defining Custom Attributes)

`Illuminate\Contracts\Container\ContextualAttribute` 계약을 구현해 직접 컨텍스츄얼 속성을 만들 수 있습니다. 컨테이너는 속성의 `resolve` 메서드를 호출하는데, 이 메서드 안에서 해당 속성이 주입할 값을 반환하면 됩니다. 아래 예시는 라라벨 내장 `Config` 속성을 재구현한 코드입니다:

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
     * 새 속성 인스턴스 생성자.
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
### 원시 값 바인딩 (Binding Primitives)

클래스가 일부는 클래스 의존성으로 받고, 또 일부는 정수 같은 원시 값이 주입되어야 하는 경우가 있습니다. 그런 경우 컨텍스츄얼 바인딩을 활용해 원하는 값을 주입할 수 있습니다:

```
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

간혹 클래스가 [태깅](#tagging)된 인스턴스 배열을 의존성으로 가질 수도 있습니다. 이때 `giveTagged` 메서드를 쓰면 해당 태그에 바인딩된 모든 인스턴스를 주입할 수 있습니다:

```
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션 설정 파일에서 값을 주입하고자 하면, `giveConfig` 메서드를 이용하세요:

```
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입드 가변 인자 바인딩 (Binding Typed Variadics)

가변 인자(variadic) 형태로 타입이 지정된 객체 배열을 생성자에서 받는 클래스가 있을 수 있습니다:

```
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
     * 새 클래스 인스턴스 생성자.
     */
    public function __construct(
        protected Logger $logger,
        Filter ...$filters,
    ) {
        $this->filters = $filters;
    }
}
```

컨텍스츄얼 바인딩을 활용해 `give` 메서드에 `Filter` 인스턴스를 반환하는 클로저를 전달하면 이 의존성을 해석할 수 있습니다:

```
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

편의상, 배열로 클래스 네임 목록만 전달해도 컨테이너가 자동으로 인스턴스를 해석해 줍니다:

```
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

때로는 가변 인자가 특정 클래스 타입으로 타입힌팅되어 있고(`Report ...$reports`), 이를 같은 태그를 가진 모든 바인딩을 주입해야 할 때가 있습니다:

```
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅 (Tagging)

특정 “카테고리”에 해당하는 바인딩을 모두 한꺼번에 해석해야 할 때가 있습니다. 예를 들어 여러 `Report` 인터페이스 구현체들을 모두 전달받는 리포트 분석기를 만든다고 가정해봅시다. 먼저 해당 구현체들을 바인딩하고, `tag` 메서드로 태그를 지정해 줍니다:

```
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

태깅한 서비스들은 컨테이너의 `tagged` 메서드를 통해 쉽게 모두 해석할 수 있습니다:

```
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장 (Extending Bindings)

`extend` 메서드를 사용하면 이미 해석된 서비스를 수정할 수 있습니다. 예를 들어, 서비스가 해석된 뒤 추가로 꾸미거나 설정하는 작업을 할 수 있습니다. `extend`는 두 개의 인자를 받는데, 하나는 확장할 서비스 클래스, 다른 하나는 수정된 서비스를 반환하는 클로저입니다. 클로저에는 현재 해석된 서비스와 컨테이너 인스턴스가 전달됩니다:

```
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해결 (Resolving)

<a name="the-make-method"></a>
### `make` 메서드 (The `make` Method)

컨테이너에서 클래스 인스턴스를 해석하려면 `make` 메서드를 사용하세요. 클래스나 인터페이스 이름을 인자로 넘겨줍니다:

```
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스 의존성 중 일부가 컨테이너에서 자동 해석되지 않는다면, `makeWith` 메서드에 배열로 직접 인자 값을 넘겨주어 주입할 수 있습니다. 예를 들어 `Transistor` 서비스의 생성자 인자인 `$id`를 직접 전달할 수 있습니다:

```
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드는 특정 클래스나 인터페이스가 컨테이너에 바인딩되어 있는지 확인할 때 사용합니다:

```
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

코드에서 `$app` 변수를 가진 서비스 프로바이더 밖이라면, `App` [파사드](/docs/11.x/facades)나 `app` 헬퍼 함수를 통해 컨테이너에서 인스턴스를 해석할 수 있습니다:

```
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

컨테이너 인스턴스 자체를 해석 중인 클래스에 주입하고 싶으면, 생성자에 `Illuminate\Container\Container` 클래스를 타입힌팅하세요:

```
use Illuminate\Container\Container;

/**
 * 새 클래스 인스턴스 생성자.
 */
public function __construct(
    protected Container $container,
) {}
```

<a name="automatic-injection"></a>
### 자동 주입 (Automatic Injection)

가장 중요한 점은, 컨테이너를 통해 해석되는 클래스의 생성자에 의존성을 타입힌팅하면 자동으로 주입된다는 점입니다. [컨트롤러](/docs/11.x/controllers), [이벤트 리스너](/docs/11.x/events), [미들웨어](/docs/11.x/middleware) 뿐만 아니라 [큐 작업](/docs/11.x/queues)의 `handle` 메서드에서도 마찬가지입니다. 실제로 대부분 객체는 이렇게 컨테이너를 통해 해석되어야 합니다.

예를 들어, 애플리케이션 내 정의된 서비스를 컨트롤러 생성자에 타입힌팅하면 자동으로 인스턴스가 만들어져 주입됩니다:

```
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;

class PodcastController extends Controller
{
    /**
     * 새 컨트롤러 인스턴스 생성자.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * 지정된 팟캐스트 정보 반환.
     */
    public function show(string $id): Podcast
    {
        return $this->apple->findPodcast($id);
    }
}
```

<a name="method-invocation-and-injection"></a>
## 메서드 호출 및 주입 (Method Invocation and Injection)

메서드를 호출하면서 컨테이너가 해당 메서드의 의존성을 자동으로 주입하도록 할 수 있습니다. 예를 들어, 다음과 같은 클래스가 있는 경우:

```
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

```
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 PHP에서 호출 가능한 어떤 것도 인자로 받을 수 있습니다. 클로저도 마찬가지로 주입되는 의존성을 자동으로 해석해 호출할 수 있습니다:

```
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트 (Container Events)

서비스 컨테이너는 객체를 해석할 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 사용해 이 이벤트를 청취할 수 있습니다:

```
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입의 객체가 컨테이너에서 해석될 때 호출됩니다...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 컨테이너에서 모든 타입의 객체가 해석될 때 호출됩니다...
});
```

해석 중인 객체가 콜백으로 전달되므로, 이후 객체를 사용하는 코드에 넘기기 전에 추가 속성을 설정하는 데 활용할 수 있습니다.

<a name="rebinding"></a>
### 재바인딩 (Rebinding)

`rebinding` 메서드는 서비스가 컨테이너에 재등록(초기 바인딩 이후에 다시 등록 또는 덮어쓰기)될 때를 감지해 이벤트를 수신합니다. 특정 바인딩이 갱신될 때마다 의존성 업데이트나 동작 변경이 필요할 때 유용합니다:

```
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

// 새 바인딩 등록 시 재바인딩 클로저가 호출됨
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

라라벨 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서 PSR-11 컨테이너 인터페이스를 타입힌팅해 라라벨 컨테이너 인스턴스를 얻을 수 있습니다:

```
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

주어진 식별자가 해석할 수 없으면 예외가 발생합니다. 식별자가 바인딩되지 않아 전혀 등록하지 않았다면 `Psr\Container\NotFoundExceptionInterface` 타입의 예외가, 바인딩은 되어있지만 해석 실패 시에는 `Psr\Container\ContainerExceptionInterface` 타입의 예외가 발생합니다.