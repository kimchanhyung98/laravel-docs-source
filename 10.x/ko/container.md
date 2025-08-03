# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [제로 구성 자동 해석 (Zero Configuration Resolution)](#zero-configuration-resolution)
    - [컨테이너를 언제 활용할까?](#when-to-use-the-container)
- [바인딩 (Binding)](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스와 구현체 바인딩](#binding-interfaces-to-implementations)
    - [컨텍스추얼 바인딩 (Contextual Binding)](#contextual-binding)
    - [기본 타입 바인딩 (Binding Primitives)](#binding-primitives)
    - [타입드 가변 인자 바인딩 (Binding Typed Variadics)](#binding-typed-variadics)
    - [태깅 (Tagging)](#tagging)
    - [바인딩 확장 (Extending Bindings)](#extending-bindings)
- [해결 (Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 주입 (Automatic Injection)](#automatic-injection)
- [메서드 호출 및 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 서비스 컨테이너는 클래스 의존성을 관리하고 의존성 주입을 수행하는 강력한 도구입니다. 의존성 주입은 쉽게 말해 클래스가 필요로 하는 의존성을 생성자나 경우에 따라 "세터" 메서드를 통해 "주입"하는 것을 의미합니다.

간단한 예제를 보겠습니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Repositories\UserRepository;
use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스를 생성합니다.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * 주어진 사용자 프로필을 보여줍니다.
     */
    public function show(string $id): View
    {
        $user = $this->users->find($id);

        return view('user.profile', ['user' => $user]);
    }
}
```

이 예제에서 `UserController`는 데이터 소스에서 사용자를 가져와야 합니다. 따라서 사용자 정보를 가져올 수 있는 서비스를 **주입**합니다. 여기서 우리의 `UserRepository`는 아마 [Eloquent](/docs/10.x/eloquent)를 사용해 데이터베이스에서 사용자 정보를 검색할 것입니다. 하지만 리포지토리가 주입되기 때문에 다른 구현체로 쉽게 교체할 수 있으며, 테스트 시에는 `UserRepository`의 대체용 "모의(mock)" 구현도 쉽게 만들 수 있습니다.

Laravel 서비스 컨테이너에 대한 깊은 이해는 강력하고 대규모 애플리케이션을 구축하는 것뿐 아니라 Laravel 코어에 기여하기 위해서도 필수적입니다.

<a name="zero-configuration-resolution"></a>
### 제로 구성 자동 해석 (Zero Configuration Resolution)

클래스가 의존성이 없거나 다른 구체 클래스(인터페이스가 아닌)만 의존하고 있다면, 컨테이너에 해당 클래스를 해석하는 방법을 따로 지시할 필요가 없습니다. 예를 들어, `routes/web.php` 파일에서 아래 코드처럼 작성할 수 있습니다:

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

이 경우 애플리케이션의 `/` 경로에 접근하면 `Service` 클래스가 자동으로 해결되고 라우트 핸들러에 주입됩니다. 이는 매우 편리한 기능으로, 복잡한 설정 파일 없이도 의존성 주입을 활용하며 애플리케이션을 개발할 수 있음을 의미합니다.

운 좋게도, Laravel 애플리케이션을 개발할 때 작성하는 많은 클래스들은 컨테이너를 통해 의존성을 자동으로 주입받습니다. 컨트롤러, 이벤트 리스너, 미들웨어 등 여러 클래스가 자동으로 의존성을 해결받습니다. 또한, [큐 작업](/docs/10.x/queues)의 `handle` 메서드에서도 타입힌트로 의존성을 받을 수 있습니다. 자동 의존성 주입의 강력함을 경험하면 이 기능 없이는 개발하기 어려울 정도입니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 언제 활용할까? (When to Utilize the Container)

제로 구성 자동 해석 덕분에 라우트, 컨트롤러, 이벤트 리스너 등 여러 위치에서 타입힌트만 해도 컨테이너와 직접 상호작용하지 않고 의존성이 자동으로 주입됩니다. 예를 들어, 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입힌트하여 현재 요청에 쉽게 접근할 수 있습니다. 사실 이렇게 직접 컨테이너에 관여하지 않아도 의존성 주입이 관리됩니다:

```
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

많은 경우 자동 의존성 주입과 [파사드](/docs/10.x/facades)를 활용해 컨테이너에서 직접 바인딩하거나 해석하는 일을 아예 하지 않고도 개발할 수 있습니다. 그렇다면 **한편으로는 언제 컨테이너를 직접 활용할까요?** 두 가지 상황을 살펴봅니다.

첫째, 인터페이스를 구현하는 클래스를 작성하고, 그 인터페이스를 라우트나 생성자에서 타입힌트하고 싶다면, 해당 인터페이스를 컨테이너에 어떤 클래스에 매핑할지 명확히 알려줘야 합니다([인터페이스 바인딩](#binding-interfaces-to-implementations) 참조). 둘째, 다른 Laravel 개발자와 공유할 계획인 패키지를 작성하는 경우, 패키지 서비스들을 컨테이너에 바인딩해야 할 수도 있습니다.

<a name="binding"></a>
## 바인딩 (Binding)

<a name="binding-basics"></a>
### 바인딩 기본 (Binding Basics)

<a name="simple-bindings"></a>
#### 간단한 바인딩 (Simple Bindings)

서비스 컨테이너에 거의 모든 바인딩은 [서비스 프로바이더](/docs/10.x/providers) 내에서 등록됩니다. 따라서 대부분의 예제는 이 컨텍스트를 기준으로 설명합니다.

서비스 프로바이더 내에서는 `$this->app` 속성으로 컨테이너에 접근할 수 있습니다. `bind` 메서드를 통해 바인딩을 등록할 수 있는데, 이때 바인딩하려는 클래스 또는 인터페이스 이름과 인스턴스를 반환하는 클로저를 함께 전달합니다:

```
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

이때 클로저에 컨테이너 인스턴스 자체가 `$app`으로 전달되므로, 하위 의존성을 컨테이너에서 해결해 객체 생성에 활용할 수 있습니다.

대부분 서비스 프로바이더 안에서 컨테이너와 상호작용하지만, 서비스 프로바이더 외부에서도 `App` [파사드](/docs/10.x/facades)를 통해 컨테이너에 접근할 수 있습니다:

```
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

`bindIf` 메서드를 사용하면 해당 타입에 바인딩이 아직 등록되지 않은 경우에만 바인딩을 등록합니다:

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]  
> 클래스가 인터페이스에 의존하지 않는다면 컨테이너에 바인딩할 필요가 없습니다. 이는 컨테이너가 리플렉션을 통해 해당 클래스들을 자동으로 해석할 수 있기 때문입니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩 (Binding A Singleton)

`singleton` 메서드는 클래스 또는 인터페이스를 컨테이너에 한 번만 해석해 같은 인스턴스를 반환하도록 바인딩합니다. 싱글톤이 해석된 후에는 이후 호출 시 동일 객체가 리턴됩니다:

```
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`singletonIf` 메서드를 사용하면 아직 등록되지 않은 타입에 대해서만 싱글톤 바인딩을 할 수 있습니다:

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 요청 범위 싱글톤 바인딩 (Binding Scoped Singletons)

`scoped` 메서드는 같은 Laravel 요청 또는 작업(job) 생명주기 내에서만 한 번 해석되고 같은 인스턴스를 반환하는 바인딩을 등록합니다. `singleton` 메서드와 비슷하지만, `scoped`로 등록된 인스턴스는 Laravel 애플리케이션이 새 "생명주기"(예: [Laravel Octane](/docs/10.x/octane) 워커가 새 요청을 처리하거나, 큐 워커가 새 작업을 처리하는 시점)를 시작할 때마다 초기화됩니다:

```
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩 (Binding Instances)

존재하는 객체 인스턴스를 `instance` 메서드로 컨테이너에 등록할 수 있습니다. 이후 해당 타입을 컨테이너에서 요청하면 이 인스턴스가 반환됩니다:

```
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스와 구현체 바인딩 (Binding Interfaces to Implementations)

서비스 컨테이너의 매우 강력한 기능은 인터페이스를 특정 구현체에 매핑하는 기능입니다. 예를 들어 `EventPusher` 인터페이스와 그 구현체인 `RedisEventPusher`가 있다고 가정해 보겠습니다. 인터페이스 구현체를 작성한 후 서비스 컨테이너에 다음과 같이 등록합니다:

```
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이 구문은 컨테이너에 클래스를 해석할 때 `EventPusher`가 필요하면 `RedisEventPusher` 인스턴스를 주입하라는 의미가 됩니다. 이제 컨트롤러나 다른 클래스의 생성자에 `EventPusher` 인터페이스를 타입힌트하면, 컨테이너가 자동으로 `RedisEventPusher`를 주입합니다. Laravel 컨트롤러, 이벤트 리스너, 미들웨어 등 많은 클래스가 컨테이너를 통해 이러한 방식으로 해석됩니다:

```
use App\Contracts\EventPusher;

/**
 * 새로운 클래스 인스턴스를 생성합니다.
 */
public function __construct(
    protected EventPusher $pusher
) {}
```

<a name="contextual-binding"></a>
### 컨텍스추얼 바인딩 (Contextual Binding)

가끔 같은 인터페이스를 사용하는 두 개의 클래스가 있지만, 각기 다른 구현체를 주입해야 할 때가 있습니다. 예를 들어 두 개의 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` 계약에 서로 다른 구현체를 의존하는 경우가 해당됩니다. Laravel은 이를 쉽게 처리할 수 있는 유창한 인터페이스를 제공합니다:

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

위 예제처럼 특정 클래스에 한해 필요한 타입에 다른 구현체를 주입하도록 지정할 수 있습니다.

<a name="binding-primitives"></a>
### 기본 타입 바인딩 (Binding Primitives)

종종 클래스가 다른 클래스들을 주입받으면서, 정수형과 같은 기본 타입 값도 같이 주입받아야 할 때가 있습니다. 이 경우도 컨텍스추얼 바인딩을 사용해 손쉽게 값을 주입할 수 있습니다:

```
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
          ->needs('$variableName')
          ->give($value);
```

경우에 따라 클래스가 여러 개의 [태그된](#tagging) 인스턴스 배열을 의존할 수 있습니다. 이때 `giveTagged` 메서드를 사용하면 해당 태그가 붙은 모든 컨테이너 바인딩을 주입 가능합니다:

```
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션 설정 파일에서 값을 주입하고 싶다면 `giveConfig` 메서드를 사용할 수 있습니다:

```
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입드 가변 인자 바인딩 (Binding Typed Variadics)

가끔 가변 인자(variadic) 생성자 인자를 통해 타입이 지정된 객체 배열을 주입받는 클래스가 있습니다:

```
<?php

use App\Models\Filter;
use App\Services\Logger;

class Firewall
{
    /**
     * 필터 인스턴스 배열입니다.
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

컨텍스추얼 바인딩을 사용해 `give` 메서드에 클로저를 넘기고, `Filter` 인스턴스 배열을 반환하여 이 의존성을 해결할 수 있습니다:

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

편의를 위해, `Firewall`이 `Filter` 배열을 필요로 할 때 컨테이너가 해석할 클래스명 배열을 직접 넘기는 것도 가능합니다:

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

클래스가 타입힌트된 가변 인자(`Report ...$reports`)를 의존할 때, `needs`와 `giveTagged` 메서드 조합을 사용해 주어진 태그가 붙은 모든 컨테이너 바인딩을 주입할 수 있습니다:

```
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅 (Tagging)

특정 "카테고리"에 속하는 모든 바인딩을 한꺼번에 해결해야 할 때가 있습니다. 예를 들어 다양한 `Report` 인터페이스 구현체를 배열로 주입받는 리포트 애널라이저가 있다고 가정해 보겠습니다. 해당 구현체들을 등록한 후, `tag` 메서드로 태그를 지정할 수 있습니다:

```
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

태그가 붙은 서비스는 컨테이너의 `tagged` 메서드를 이용해 한꺼번에 해결할 수 있습니다:

```
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장 (Extending Bindings)

`extend` 메서드는 해석된 서비스를 수정할 수 있게 해줍니다. 예를 들어 서비스가 해석될 때 추가 코드를 실행해서 서비스를 꾸미거나 설정할 수 있습니다. 인수로는 확장할 서비스 클래스와 수정된 서비스를 반환할 클로저를 받는데, 클로저는 해석된 서비스와 컨테이너 인스턴스를 전달받습니다:

```
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해결 (Resolving)

<a name="the-make-method"></a>
### `make` 메서드

`make` 메서드를 이용하여 컨테이너에서 클래스 인스턴스를 해석할 수 있습니다. `make`는 해석하고자 하는 클래스 또는 인터페이스 이름을 인수로 받습니다:

```
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

만약 클래스의 의존성 중 일부가 컨테이너에서 자동으로 해결되지 않는다면, `makeWith` 메서드에 연관 배열로 인자를 직접 전달해 주입할 수 있습니다. 예를 들어 `Transistor` 서비스의 `$id` 생성자 인자를 수동으로 전달할 경우:

```
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드는 특정 클래스 또는 인터페이스가 컨테이너에 명시적으로 바인딩되어 있는지 확인하는 데 사용합니다:

```
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더 외부 등 `$app` 변수에 접근할 수 없는 곳에서는 `App` [파사드](/docs/10.x/facades) 또는 `app` [헬퍼 함수](/docs/10.x/helpers#method-app)를 사용해 컨테이너에서 클래스 인스턴스를 얻을 수 있습니다:

```
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

만약 컨테이너 자체를 주입받고 싶다면, 클래스 생성자에 `Illuminate\Container\Container` 클래스를 타입힌트 할 수 있습니다:

```
use Illuminate\Container\Container;

/**
 * 새로운 클래스 인스턴스를 생성합니다.
 */
public function __construct(
    protected Container $container
) {}
```

<a name="automatic-injection"></a>
### 자동 주입 (Automatic Injection)

또 다른 중요한 점은, 컨테이너가 클래스를 해석할 때 생성자에서 타입힌트를 통해 의존성을 자동 주입한다는 점입니다. 이는 [컨트롤러](/docs/10.x/controllers), [이벤트 리스너](/docs/10.x/events), [미들웨어](/docs/10.x/middleware) 같은 대부분 클래스에서 적용됩니다. 또한, [큐 작업](/docs/10.x/queues)의 `handle` 메서드에서도 타입힌트 의존성 주입이 가능합니다. 실무에서는 거의 대부분 컨테이너가 이런 방식으로 객체를 해결합니다.

예를 들어, 컨트롤러 생성자에서 애플리케이션에 정의한 리포지토리를 타입힌트하면, 컨테이너가 이를 자동 해석해 주입합니다:

```
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;
use App\Models\User;

class UserController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스를 생성합니다.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * 주어진 ID를 가진 사용자를 보여줍니다.
     */
    public function show(string $id): User
    {
        $user = $this->users->findOrFail($id);

        return $user;
    }
}
```

<a name="method-invocation-and-injection"></a>
## 메서드 호출 및 주입 (Method Invocation and Injection)

가끔 객체 인스턴스에 특정 메서드를 호출할 때 해당 메서드의 의존성을 자동 주입받고 싶을 수 있습니다. 예를 들어 다음 클래스를 보겠습니다:

```
<?php

namespace App;

use App\Repositories\UserRepository;

class UserReport
{
    /**
     * 새로운 사용자 리포트를 생성합니다.
     */
    public function generate(UserRepository $repository): array
    {
        return [
            // ...
        ];
    }
}
```

컨테이너를 통해 `generate` 메서드를 아래처럼 호출할 수 있습니다:

```
use App\UserReport;
use Illuminate\Support\Facades\App;

$report = App::call([new UserReport, 'generate']);
```

`call` 메서드는 PHP 콜러블(callable) 타입을 모두 받을 수 있습니다. 심지어 클로저를 호출하면서 그 의존성을 자동 주입하는 데에도 사용할 수 있습니다:

```
use App\Repositories\UserRepository;
use Illuminate\Support\Facades\App;

$result = App::call(function (UserRepository $repository) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트 (Container Events)

서비스 컨테이너는 객체가 해석될 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 사용해 이 이벤트를 청취할 수 있습니다:

```
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // 컨테이너가 "Transistor" 타입 객체를 해석할 때 호출됩니다...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 컨테이너가 모든 타입의 객체를 해석할 때 호출됩니다...
});
```

해석되는 객체가 콜백에 전달되므로, 소비자에 전달되기 전에 추가 속성을 설정하는 등 작업을 할 수 있습니다.

<a name="psr-11"></a>
## PSR-11

Laravel 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서 PSR-11 컨테이너 인터페이스를 타입힌트하여 Laravel 컨테이너 인스턴스를 받을 수 있습니다:

```
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

만약 주어진 식별자를 해석할 수 없으면 예외가 발생합니다. 만약 식별자가 바인딩된 적이 없으면 `Psr\Container\NotFoundExceptionInterface` 타입 예외가, 바인딩됐으나 해석할 수 없으면 `Psr\Container\ContainerExceptionInterface` 타입 예외가 발생합니다.