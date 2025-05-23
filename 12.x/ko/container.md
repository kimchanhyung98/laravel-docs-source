# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [제로 구성 해제(Zero Configuration Resolution)](#zero-configuration-resolution)
    - [컨테이너를 활용해야 할 때](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [문맥 바인딩](#contextual-binding)
    - [문맥 속성](#contextual-attributes)
    - [원시값 바인딩](#binding-primitives)
    - [타입 지정 가변 인자 바인딩](#binding-typed-variadics)
    - [태깅](#tagging)
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

라라벨의 서비스 컨테이너는 클래스 간의 의존성 관리와 의존성 주입을 위한 강력한 도구입니다. 의존성 주입(Dependency Injection)이란, 클래스가 필요로 하는 의존성을 생성자나, 경우에 따라서는 "세터(setter)" 메서드를 통해 "주입"받는 것을 말합니다.

간단한 예시를 살펴보겠습니다.

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

위 예시에서 `PodcastController`는 Apple Music 등과 같은 데이터 소스에서 팟캐스트 정보를 가져와야 합니다. 따라서, 팟캐스트를 조회할 수 있는 서비스를 **주입**받습니다. 이렇게 서비스를 주입하면, 테스트 시에도 `AppleMusic` 서비스를 손쉽게 "모킹(mock)"하거나 더미 구현체로 대체할 수 있습니다.

라라벨의 서비스 컨테이너를 깊이 있게 이해하는 것은 강력한 대규모 애플리케이션을 만들고, 라라벨 코어 자체에 기여하기 위해서도 꼭 필요합니다.

<a name="zero-configuration-resolution"></a>
### 제로 구성 해제(Zero Configuration Resolution)

클래스가 의존성이 없거나, 오직 다른 구체 클래스(인터페이스가 아님)만을 의존한다면, 컨테이너는 해당 클래스의 해법(해결 방법)을 별도로 지정하지 않아도 자동으로 주입할 수 있습니다. 예를 들어, `routes/web.php` 파일에 아래와 같이 작성할 수 있습니다.

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

이 예시에서, 애플리케이션의 `/` 라우트로 접근하면 컨테이너가 자동으로 `Service` 클래스를 해석하여 해당 라우트의 핸들러로 주입해줍니다. 이것은 매우 혁신적인 기능입니다. 즉, 별도의 복잡한 설정 파일을 신경 쓰지 않고도 의존성 주입을 충분히 활용하면서 애플리케이션을 개발할 수 있다는 뜻입니다.

다행히도, 라라벨 애플리케이션을 만들 때 작성하는 많은 클래스들은 별도의 작업 없이 서비스 컨테이너를 통해 자동으로 의존성을 주입받습니다. 여기에 [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등이 포함됩니다. 또한, [큐 작업](/docs/12.x/queues)의 `handle` 메서드에도 의존성을 타입힌트하여 주입받을 수 있습니다. 이렇게 자동, 그리고 제로 구성의 의존성 주입 기능은 없으면 아쉬울 정도로 개발 생산성을 높여줍니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 활용해야 할 때

제로 구성 해제 기능 덕분에, 대부분의 경우 라우트, 컨트롤러, 이벤트 리스너 등에서 의존성을 타입힌트만 해주면 직접 컨테이너를 다루지 않고도 자동으로 의존성을 주입받을 수 있습니다. 예를 들어, 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입힌트하면 현재 요청 객체에 곧바로 접근할 수 있습니다. 우리가 직접 서비스 컨테이너를 활용하지 않았더라도, 내부에서 컨테이너가 의존성 주입을 관리하고 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

많은 경우, 자동 의존성 주입과 [파사드](/docs/12.x/facades) 기능만으로도 라라벨 애플리케이션을 만들 수 있어서 **직접** 컨테이너에서 바인딩하거나 해제(resolving)하는 일은 사실 드뭅니다. **그렇다면 언제 직접 컨테이너를 다뤄야 할까요?** 대표적인 경우는 두 가지입니다.

첫째, 어떤 클래스가 인터페이스를 구현하고 있고 라우트나 클래스 생성자에서 해당 인터페이스를 타입힌트로 주입하고 싶을 때는 [인터페이스를 구현체에 바인딩](#binding-interfaces-to-implementations)하는 방법을 컨테이너에 알려주어야 합니다. 둘째, [라라벨 패키지](/docs/12.x/packages)를 만들어 다른 라라벨 개발자들과 공유할 계획이 있다면, 패키지의 서비스들을 컨테이너에 바인딩해야 할 수 있습니다.

<a name="binding"></a>
## 바인딩

<a name="binding-basics"></a>
### 바인딩 기본

<a name="simple-bindings"></a>
#### 단순 바인딩

서비스 컨테이너에 바인딩하는 작업의 대부분은 [서비스 프로바이더](/docs/12.x/providers)에서 수행하게 됩니다. 따라서 예제 대부분이 서비스 프로바이더에서 컨테이너를 사용하는 모습을 보여줍니다.

서비스 프로바이더 안에서는 언제나 `$this->app` 속성을 통해 컨테이너에 접근할 수 있습니다. 바인딩하려는 클래스나 인터페이스 이름, 그리고 해당 클래스의 인스턴스를 반환하는 클로저를 `bind` 메서드에 전달해서 바인딩을 등록할 수 있습니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

이때, 해석(해결) 함수의 매개변수로 컨테이너 자체가 주입되므로, 이 컨테이너를 이용해 각 객체를 만들 때 필요한 하위 의존성도 해결할 수 있습니다.

앞서 말했듯, 주로 서비스 프로바이더 안에서 컨테이너를 다루겠지만, 서비스 프로바이더 밖에서 컨테이너에 접근하고 싶다면, `App` [파사드](/docs/12.x/facades)를 사용할 수도 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

`bindIf` 메서드는 해당 타입으로 이미 바인딩이 등록되어 있지 않은 경우에만 컨테이너 바인딩을 등록할 때 사용합니다.

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

또한, 편의상 바인딩할 클래스 또는 인터페이스 이름을 별도의 인자로 전달하지 않고, 클로저의 반환 타입을 통해 라라벨이 타입을 자동 추론하게 할 수 있습니다.

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 클래스가 어떤 인터페이스에도 의존하지 않는다면, 굳이 컨테이너에 바인딩할 필요가 없습니다. 컨테이너는 이런 객체를 리플렉션(reflection)으로 자동 해결할 수 있기 때문에 별도의 지시가 필요하지 않습니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩

`singleton` 메서드는 클래스나 인터페이스를 한 번만 컨테이너에 바인딩하도록 합니다. 싱글톤 바인딩이 한 번 해석(해결)되면, 이후엔 동일한 객체 인스턴스를 계속 반환합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`singletonIf` 메서드는 해당 타입으로 이미 바인딩이 등록되어 있지 않은 경우에만 싱글톤을 등록합니다.

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 스코프 싱글톤 바인딩

`scoped` 메서드는 한 번의 라라벨 요청 또는 작업(Job) 라이프사이클 안에서만 한 번 해석되는 싱글톤을 바인딩합니다. 이 방식은 `singleton`과 비슷하지만, [Laravel Octane](/docs/12.x/octane) 워커가 새로운 요청을 처리하거나 [큐 워커](/docs/12.x/queues)가 작업을 처리할 때마다 인스턴스가 초기화(플러시)된다는 점이 다릅니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`scopedIf` 메서드는 해당 타입으로 이미 바인딩이 등록되어 있지 않을 때에만 스코프 바인딩을 등록합니다.

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩

이미 생성된 객체 인스턴스를 `instance` 메서드를 이용해 컨테이너에 바인딩할 수도 있습니다. 이렇게 등록된 인스턴스는 이후 컨테이너에서 계속 동일하게 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기

서비스 컨테이너의 강력한 점 중 하나는 인터페이스를 특정 구현체에 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher`라는 인터페이스와 `RedisEventPusher`라는 구현체가 있다고 해보겠습니다. 구현체를 만들었다면 아래와 같이 서비스 컨테이너에 바인딩할 수 있습니다.

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이 선언은 컨테이너가 `EventPusher` 구현체가 필요할 때 `RedisEventPusher`를 주입하도록 지정하는 것입니다. 이제 컨테이너에서 해결되는 클래스의 생성자 등에서 `EventPusher` 인터페이스를 타입힌트하면, 알아서 구현체가 주입됩니다. (컨트롤러, 이벤트 리스너, 미들웨어 등은 컨테이너로 항상 해결되기 때문에 가능)

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
### 문맥 바인딩

경우에 따라, 두 개의 클래스가 동일한 인터페이스를 사용하더라도 각각 서로 다른 구현체를 주입받길 원하는 경우가 있습니다. 예를 들어, 두 컨트롤러가 서로 다른 `Illuminate\Contracts\Filesystem\Filesystem` [계약(Contract)](/docs/12.x/contracts) 구현체를 쓰고 있다면, 아래와 같이 바인딩을 분리해 문맥에 따라 다르게 지정할 수 있습니다.

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
### 문맥 속성

문맥 바인딩은 주로 드라이버 구현체나 설정 값 등 특별한 값을 주입할 때 활용됩니다. 라라벨에서는 이런 값들을 명시적으로 서비스 프로바이더에서 바인딩하지 않아도, 여러 가지 문맥 바인딩 속성을 활용하여 간단하게 주입할 수 있습니다.

예를 들어, `Storage` 속성을 사용하면 특정 [스토리지 디스크](/docs/12.x/filesystem)를 지정하여 주입할 수 있습니다.

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

이 외에도 라라벨에서는 `Auth`, `Cache`, `Config`, `Context`, `DB`, `Log`, `RouteParameter`, 그리고 [Tag](#tagging) 속성도 지원합니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Photo;
use Illuminate\Container\Attributes\Auth;
use Illuminate\Container\Attributes\Cache;
use Illuminate\Container\Attributes\Config;
use Illuminate\Container\Attributes\Context;
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
        #[Context('uuid')] protected string $uuid,
        #[DB('mysql')] protected Connection $connection,
        #[Log('daily')] protected LoggerInterface $log,
        #[RouteParameter('photo')] protected Photo $photo,
        #[Tag('reports')] protected iterable $reports,
    ) {
        // ...
    }
}
```

더불어, 현재 인증된 사용자를 라우트 또는 클래스에 주입받고 싶을 때 사용할 수 있는 `CurrentUser` 속성도 있습니다.

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 커스텀 속성 정의하기

직접 커스텀 문맥 속성을 만들고 싶다면 `Illuminate\Contracts\Container\ContextualAttribute` 계약을 구현하면 됩니다. 컨테이너는 해당 속성의 `resolve` 메서드를 호출하여 실제로 주입할 값을 반환받습니다. 아래 예시는 라라벨 내장 `Config` 속성을 재구현한 코드입니다.

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
### 원시값 바인딩

때때로, 클래스가 의존성 주입을 통해 객체뿐 아니라 정수와 같은 단순한 값(원시값)도 필요로 할 수 있습니다. 이럴 때도 문맥 바인딩을 활용해 원하는 값을 쉽게 주입할 수 있습니다.

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

어떤 클래스가 [태그](#tagging)된 인스턴스의 배열에 의존한다면, `giveTagged` 메서드를 사용하여 해당 태그가 달린 모든 컨테이너 바인딩 인스턴스를 편리하게 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

설정 파일의 값을 직접 주입하고 싶다면 `giveConfig` 메서드를 사용할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입 지정 가변 인자 바인딩

클래스에서 가변 인자(variadic) 생성자 매개변수를 사용해 특정 타입의 객체들을 배열로 받도록 설계하는 경우가 있습니다.

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

이 경우, 문맥 바인딩에서 `give` 메서드에 `Filter` 인스턴스 배열을 반환하는 클로저를 전달하면 해당 의존성을 해결할 수 있습니다.

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

더 간편하게, 클래스 이름의 배열만 지정하면, 컨테이너가 `Firewall`에 `Filter` 인스턴스가 필요할 때마다 각 클래스를 자동으로 해결해 전달합니다.

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

클래스가 `Report ...$reports`처럼 타입힌트된 가변 의존성을 가진 경우, `needs`와 `giveTagged` 메서드를 활용해 해당 태그를 가진 컨테이너 바인딩 모두를 손쉽게 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅

특정 "분류"에 속하는 모든 바인딩을 한 번에 해석(resolving)해야 하는 경우가 있습니다. 예를 들어, 다양한 `Report` 인터페이스 구현체 배열을 받는 리포트 분석기를 만든다고 가정해봅시다. 각 `Report` 구현체 바인딩을 등록한 후, `tag` 메서드를 사용해 태깅할 수 있습니다.

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

이렇게 태깅하면 컨테이너의 `tagged` 메서드로 한 번에 모두 꺼내 쓸 수 있습니다.

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장

`extend` 메서드를 사용하면 이미 해석된 서비스에 추가 작업을 할 수 있습니다. 예를 들어, 서비스를 해석할 때 데코레이터 패턴이나 추가 설정 등 일부 코드를 실행할 수 있습니다. 첫 번째 인자는 확장할 서비스 클래스, 두 번째는 수정된 서비스 인스턴스를 반환하는 클로저입니다. 이 클로저에는 해석된 서비스와 컨테이너 인스턴스가 전달됩니다.

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해결(Resolving)

<a name="the-make-method"></a>
### `make` 메서드

`make` 메서드는 컨테이너에서 클래스 인스턴스를 해석(생성)할 때 사용합니다. 이 메서드는 해석하고자 하는 클래스나 인터페이스 이름을 인자로 받습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스 의존성 중 일부가 컨테이너에서 자동으로 해결되지 않는 경우, `makeWith` 메서드에 연관 배열로 필요한 생성자 인수를 직접 전달할 수 있습니다. 예를 들어, `Transistor` 서비스에서 `$id` 생성자 인자를 직접 전달하고 싶다면 다음과 같이 할 수 있습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드는 컨테이너에 해당 클래스나 인터페이스가 명시적으로 바인딩되어 있는지 확인할 때 사용합니다.

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더가 아닌, `$app` 변수가 없는 곳에서는 `App` [파사드](/docs/12.x/facades)나 `app` [헬퍼](/docs/12.x/helpers#method-app)를 사용해 컨테이너에서 클래스 인스턴스를 해석할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

해당 클래스를 해석하는 과정에서 라라벨 컨테이너 인스턴스 자체를 주입받고 싶다면, 생성자에 `Illuminate\Container\Container` 타입을 지정하면 됩니다.

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

라라벨 컨테이너로 해석되는(컨트롤러, 이벤트 리스너, 미들웨어 등) 클래스의 생성자에 의존성을 타입힌트로 지정하면, 자동으로 해당 서비스가 주입됩니다. [큐 작업](/docs/12.x/queues)의 `handle` 메서드에도 동일하게 적용됩니다. 실제로 대부분의 객체는 이 자동 의존성 주입 방식을 활용해 해석하는 것이 가장 편리합니다.

예를 들어, 컨트롤러 생성자에 애플리케이션 서비스 클래스를 타입힌트하면, 해당 서비스는 자동으로 주입됩니다.

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
## 메서드 호출과 주입

때로는 객체 인스턴스의 특정 메서드를 호출할 때, 그 메서드에서 요구하는 의존성을 컨테이너가 자동으로 주입해주기를 바랄 수 있습니다. 아래의 클래스를 예시로 보겠습니다.

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

컨테이너의 `call` 메서드를 사용해서 `generate` 메서드를 호출하면, 의존성이 자동으로 주입됩니다.

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 어떤 PHP 콜러블(callable)도 받을 수 있습니다. 클로저에 대해 의존성을 자동 주입해 호출할 수도 있습니다.

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트

서비스 컨테이너는 객체가 해석될 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 사용해서 이 이벤트를 구독할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입의 객체가 컨테이너에서 해석될 때 호출...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 어떤 타입의 객체든 컨테이너에서 해석될 때 호출...
});
```

이벤트 콜백에는 해석되는 객체가 전달되어, 해당 객체를 소비자에게 전달하기 전에 추가 속성을 지정할 수 있습니다.

<a name="rebinding"></a>
### 리바인딩(Rebinding)

`rebinding` 메서드는 어떤 서비스가 컨테이너에 재등록되거나 기존 바인딩이 덮어써질 때를 감지해 콜백을 실행합니다. 이 기능은 특정 바인딩이 갱신될 때마다 의존성이나 동작을 업데이트해야 할 때 유용합니다.

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

// 새로운 바인딩이 등록되면 rebinding 클로저가 실행됩니다...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

라라벨의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서, PSR-11 컨테이너 인터페이스를 타입힌트하면 라라벨 컨테이너 인스턴스를 얻을 수 있습니다.

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

식별자를 해석할 수 없는 경우 예외가 발생합니다. 만약 해당 식별자가 한 번도 바인딩된 적이 없다면 `Psr\Container\NotFoundExceptionInterface` 예외가, 바인딩은 되어 있지만 실제로 해석할 수 없는 경우라면 `Psr\Container\ContainerExceptionInterface` 예외가 발생합니다.