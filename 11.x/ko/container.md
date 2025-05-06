# 서비스 컨테이너

- [소개](#introduction)
    - [제로 설정(Zero Configuration) 해석](#zero-configuration-resolution)
    - [컨테이너를 언제 사용해야 하는가](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [컨텍스트 바인딩](#contextual-binding)
    - [컨텍스트 속성](#contextual-attributes)
    - [기본값(Primitive) 바인딩](#binding-primitives)
    - [타입별 가변 인자 바인딩](#binding-typed-variadics)
    - [태깅(Tagging)](#tagging)
    - [바인딩 확장](#extending-bindings)
- [해결(Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 주입](#automatic-injection)
- [메서드 호출과 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
    - [Rebinding](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개

Laravel 서비스 컨테이너는 클래스 간의 의존성 관리와 의존성 주입(Dependency Injection)을 수행하는 강력한 도구입니다. 의존성 주입은 복잡해 보일 수 있으나, 본질적으로 클래스의 의존 객체를 생성자 또는 "세터(Setter)" 메서드를 통해 "주입"하는 것을 의미합니다.

간단한 예제를 살펴봅시다:

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
     * 주어진 팟캐스트 정보를 보여줍니다.
     */
    public function show(string $id): View
    {
        return view('podcasts.show', [
            'podcast' => $this->apple->findPodcast($id)
        ]);
    }
}
```

이 예제에서 `PodcastController`는 Apple Music과 같은 데이터 소스에서 팟캐스트를 가져올 필요가 있습니다. 그래서 팟캐스트를 가져올 수 있는 서비스를 **주입**합니다. 서비스가 주입되기 때문에 애플리케이션을 테스트할 때 `AppleMusic` 서비스의 더미(모의) 구현을 손쉽게 사용할 수 있습니다.

Laravel 서비스 컨테이너에 대한 깊은 이해는 강력하고 대규모 애플리케이션을 구축할 때나 Laravel 코어에 기여할 때 필수적입니다.

<a name="zero-configuration-resolution"></a>
### 제로 설정(Zero Configuration) 해석

클래스가 의존성이 없거나, 인터페이스가 아닌 다른 구체 클래스에만 의존한다면, 컨테이너는 해당 클래스를 해석하는 방법을 별도로 알려줄 필요가 없습니다. 예를 들어, 다음 코드를 `routes/web.php` 파일에 넣을 수 있습니다:

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

위 예제에서, 애플리케이션의 `/` 라우트에 접속하면 `Service` 클래스가 자동으로 해석되어 라우트 핸들러에 주입됩니다. 이는 개발 방식에 혁신을 가져옵니다. 즉, 복잡한 설정 파일 없이도 의존성 주입의 이점을 누릴 수 있습니다.

Laravel 애플리케이션을 개발할 때 작성하는 많은 클래스(컨트롤러, [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등)는 컨테이너를 통해 자동으로 의존성을 받습니다. 또한 [큐 작업](/docs/{{version}}/queues)의 `handle` 메서드에도 타입힌트로 의존성을 주입할 수 있습니다. 자동·제로 설정 의존성 주입의 강력함을 경험하면, 더는 이 기능 없이 개발하기 힘들어질 것입니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 언제 사용해야 하는가

제로 설정 해석 덕분에, 여러분은 라우트, 컨트롤러, 이벤트 리스너 등에서 타입힌트만으로 의존성을 주입받을 수 있으며, 직접 컨테이너를 다룰 필요가 거의 없습니다. 예를 들어, 현재 요청 객체를 쉽게 사용하고 싶을 때 다음처럼 작성할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

이처럼 직접 컨테이너를 건드리지 않아도 의존성 주입이 자동으로 처리됩니다. 많은 경우, 자동 의존성 주입과 [파사드](/docs/{{version}}/facades) 기능 덕분에 컨테이너에서 무언가를 수동으로 바인딩하거나 해석할 필요 없이도 애플리케이션을 개발할 수 있습니다.  
**그렇다면 언제 직접 컨테이너에 접근해야 할까요?**  
대표적으로 두 가지 경우가 있습니다.

하나는 &mdash; 어떤 인터페이스를 구현한 클래스를 만들고, 그 인터페이스를 타입힌트로 사용하고 싶을 때는 [해당 인터페이스를 어떻게 해석할지 컨테이너에 알려줘야](#binding-interfaces-to-implementations) 합니다.  
또 다른 경우는 &mdash; [공개 패키지](/docs/{{version}}/packages)를 작성하며, 외부 개발자들과 공유하려면 패키지의 서비스를 컨테이너에 바인딩해야 할 수 있습니다.

<a name="binding"></a>
## 바인딩

<a name="binding-basics"></a>
### 바인딩 기본

<a name="simple-bindings"></a>
#### 기본 바인딩

대부분의 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/{{version}}/providers)에서 이루어집니다. 그래서 아래 예제들도 대부분 이 맥락을 사용합니다.

서비스 프로바이더 내에서는 `$this->app` 프로퍼티를 통해 컨테이너에 접근할 수 있습니다. `bind` 메서드를 사용하여 바인딩할 클래스 또는 인터페이스 이름과, 해당 클래스의 인스턴스를 반환하는 클로저를 전달합니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

이때 resolve 클로저의 인자로 컨테이너 자체를 받을 수 있으며, 이를 이용해 객체가 필요로 하는 하위 의존성도 컨테이너로부터 주입받을 수 있습니다.

일반적으로 서비스 프로바이더 내에서 컨테이너를 다루지만, 서비스 프로바이더 외부에서도 `App` [파사드](/docs/{{version}}/facades)를 통해 사용할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

특정 타입에 이미 바인딩이 없을 때만 바인딩을 추가하고 싶다면 `bindIf` 메서드를 사용할 수 있습니다:

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]  
> 어떤 클래스가 인터페이스에 의존하지 않는다면 별도의 바인딩은 필요 없습니다. 컨테이너는 객체 생성 방식을 별도로 알지 않아도, 리플렉션을 통해 자동으로 해석할 수 있기 때문입니다.

<a name="binding-a-singleton"></a>
#### 싱글톤(Singleton) 바인딩

`singleton` 메서드는 단 한 번만 해석되어야 하는 클래스나 인터페이스를 컨테이너에 바인딩합니다. 한 번 해석된 이후에는 동일한 인스턴스가 컨테이너 내에서 반환됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`singletonIf`를 사용하면 아직 바인딩되지 않은 경우에만 싱글톤을 바인딩할 수 있습니다:

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### Scoped 싱글톤 바인딩

`scoped` 메서드는 하나의 Laravel 요청/작업 생명주기 내에서만 한 번 해석되는 클래스나 인터페이스를 바인딩합니다.  
이 방법은 `singleton`과 비슷하지만, [Laravel Octane](/docs/{{version}}/octane) 워커가 새 요청을 처리하거나, Laravel [큐 워커](/docs/{{version}}/queues)가 새 작업을 처리할 때마다 인스턴스가 초기화됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

또한, 타입에 이미 바인딩이 없다면 `scopedIf`로 스코프 싱글톤 바인딩을 등록할 수 있습니다:

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩

`instance` 메서드로 이미 생성된 객체 인스턴스를 컨테이너에 바인딩할 수 있습니다. 이후 컨테이너에서는 항상 이 인스턴스가 반환됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기

서비스 컨테이너의 강력한 특징 중 하나는, 인터페이스를 특정 구현체에 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher` 인터페이스와 `RedisEventPusher` 구현체가 있다고 가정합시다. 구현체를 준비한 뒤 다음과 같이 바인딩할 수 있습니다:

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이제 컨테이너는 `EventPusher`가 필요할 때 `RedisEventPusher` 인스턴스를 주입하게 됩니다. 즉, 컨테이너에서 해석되는 클래스(컨트롤러, 이벤트 리스너, 미들웨어 등)의 생성자에서 `EventPusher`를 타입힌트로 사용하면 됩니다:

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
### 컨텍스트 바인딩

동일한 인터페이스를 사용하는 두 클래스에 서로 다른 구현체를 주입하고자 할 수 있습니다. 예를 들어, 두 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` [컨트랙트](/docs/{{version}}/contracts)의 서로 다른 구현에 의존할 수 있습니다. 다음처럼 컨텍스트 바인딩을 지정할 수 있습니다:

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

컨텍스트 바인딩은 드라이버의 구현체나 설정 값 등을 주입할 때 자주 사용되므로, Laravel에서는 이런 값들을 속성(Attribute)으로 주입할 수 있는 여러 컨텍스트 속성을 제공합니다.

예를 들어, `Storage` 속성은 [스토리지 디스크](/docs/{{version}}/filesystem) 인스턴스를 주입하는 데 사용할 수 있습니다:

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

`Storage` 속성 외에도 `Auth`, `Cache`, `Config`, `DB`, `Log`, `RouteParameter`, [`Tag`](#tagging) 등의 속성을 사용할 수 있습니다:

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

또한, 현재 인증된 사용자를 경로나 클래스에 주입할 수 있는 `CurrentUser` 속성도 지원됩니다:

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 사용자 정의 컨텍스트 속성 만들기

`Illuminate\Contracts\Container\ContextualAttribute` 인터페이스를 구현해서 나만의 컨텍스트 속성을 만들 수 있습니다. 컨테이너는 속성의 `resolve` 메서드를 호출하며, 이 메서드는 속성이 사용되는 클래스에 주입될 값을 반환합니다. 아래는 Laravel 내장 `Config` 속성을 재구현한 예시입니다:

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
     * 설정 값을 해석.
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

클래스가 클래스형 의존성뿐 아니라 정수 등의 기본(primitive) 값도 필요할 때, 컨텍스트 바인딩을 이용해 원하는 값을 주입할 수 있습니다:

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

클래스가 [태그된](#tagging) 인스턴스의 배열에 의존하는 경우도 있을 수 있습니다. `giveTagged` 메서드를 사용하면 해당 태그로 바인딩된 객체들을 한 번에 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

어플리케이션 설정 파일에서 값을 가져와 주입하고 싶다면 `giveConfig` 메서드를 사용할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입별 가변 인자 바인딩

때때로 가변 인자(variadic)로 타입 지정된 객체의 배열을 받는 클래스도 있습니다:

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

컨텍스트 바인딩의 `give`에 클로저를 전달해, `Filter`의 인스턴스로 구성된 배열을 리턴할 수 있습니다:

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

보다 간단히 클래스명 배열을 전달하여, 컨테이너가 필요시 객체로 해석할 수 있습니다:

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

가변 인자를 사용하는 클래스의 의존성이 특정 클래스(예: `Report ...$reports`)로 지정되어 있는 경우, `needs`와 `giveTagged` 메서드를 사용해 [태그된](#tagging) 바인딩 전부를 간편하게 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅(Tagging)

특정 "카테고리"의 바인딩 모두를 해석해야 할 때가 있습니다. 예를 들어, 다양한 `Report` 인터페이스의 구현체 배열을 받는 리포트 분석기를 개발한다고 가정해 봅시다. 각각의 구현체를 바인딩한 다음 `tag`로 태그를 지정할 수 있습니다:

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

이렇게 태그를 지정한 뒤에는 `tagged` 메서드로 해당 태그의 인스턴스 전부를 받아올 수 있습니다:

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장

`extend` 메서드를 통해 이미 해석된 서비스를 꾸미거나, 추가 설정을 할 수 있습니다. 이 메서드는 확장할 서비스 클래스와, 수정된 서비스를 반환하는 클로저를 전달받습니다. 클로저에는 현재 해석 중인 서비스 인스턴스와 컨테이너 인스턴스가 전달됩니다:

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해석(Resolving)

<a name="the-make-method"></a>
### `make` 메서드

`make` 메서드를 사용해 컨테이너에서 클래스 인스턴스를 해석할 수 있습니다. 이 메서드는 해석하려는 클래스 또는 인터페이스명을 인자로 받습니다:

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스의 일부 의존성이 컨테이너로 해석할 수 없을 경우, `makeWith` 메서드에 연관 배열로 값을 전달할 수 있습니다. 예를 들어, `Transistor` 서비스가 `$id` 생성자 인자를 필요로 할 때 다음과 같이 쓸 수 있습니다:

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드를 사용하면 컨테이너에 클래스나 인터페이스가 바인딩되어 있는지 확인할 수 있습니다:

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더 외부에서, `$app` 변수에 접근할 수 없는 곳이라면 `App` [파사드](/docs/{{version}}/facades)나 `app` [헬퍼](/docs/{{version}}/helpers#method-app)를 통해 인스턴스를 해석할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

컨테이너 자체를 클래스의 생성자에 주입받고 싶다면, `Illuminate\Container\Container` 클래스를 타입힌트할 수 있습니다:

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

또는, 컨테이너에서 해석되는 클래스의 생성자(컨트롤러, [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등)에 의존성을 타입힌트하면, 해당 의존성은 자동으로 주입됩니다. (또한 [큐 작업](/docs/{{version}}/queues)의 `handle` 메서드도 타입힌트가 가능합니다.) 실제로 애플리케이션에서 대부분의 의존성 주입은 이 방식을 사용합니다.

예시: 컨트롤러 생성자에서 애플리케이션 서비스를 타입힌트로 주입하면, 서비스가 자동 해석·주입됩니다:

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
     * 주어진 팟캐스트 정보 보여주기.
     */
    public function show(string $id): Podcast
    {
        return $this->apple->findPodcast($id);
    }
}
```

<a name="method-invocation-and-injection"></a>
## 메서드 호출과 주입

가끔 인스턴스 메서드를 호출할 때, 그 메서드의 의존성도 자동으로 주입받고 싶을 수 있습니다. 예를 들어, 다음 클래스가 있다고 합시다:

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

`generate` 메서드는 다음과 같이 컨테이너를 통해 호출할 수 있습니다:

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 어떤 PHP 콜러블도 받을 수 있습니다. 컨테이너의 `call` 메서드는, 의존성을 자동 주입하면서 클로저도 호출할 수 있습니다:

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트

서비스 컨테이너는 객체를 해석할 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 이용해 이 이벤트를 청취할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입 객체가 해석될 때마다 호출됨...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 모든 타입의 객체가 해석될 때마다 호출됨...
});
```

해석 중인 객체가 콜백에 전달되어, 객체 소비 전에 추가 속성 등을 설정할 수 있습니다.

<a name="rebinding"></a>
### Rebinding

`rebinding` 메서드를 사용하면, 컨테이너에 서비스가 다시 바인딩(즉, 재등록/재정의)될 때마다 이벤트를 청취할 수 있습니다.  
특정 바인딩이 업데이트될 때마다 의존 객체를 갱신하거나 동작을 변경해야 할 경우 유용합니다:

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

// 새로운 바인딩이 이루어지면 rebinding 콜백이 실행됨...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

Laravel의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 즉, PSR-11 컨테이너 인터페이스를 타입힌트로 전달해 Laravel 컨테이너 인스턴스를 얻을 수 있습니다:

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

만약 주어진 식별자를 해석할 수 없다면 예외가 발생합니다.  
식별자가 한 번도 바인딩된 적 없다면 `Psr\Container\NotFoundExceptionInterface` 예외가,  
바인딩되었으나 해석할 수 없을 경우에는 `Psr\Container\ContainerExceptionInterface` 예외가 발생합니다.