# 서비스 컨테이너

- [소개](#introduction)
    - [제로 구성 해상(Zero Configuration Resolution)](#zero-configuration-resolution)
    - [컨테이너를 언제 사용해야 하는가](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [상황별 바인딩](#contextual-binding)
    - [기본값 바인딩(Primitives)](#binding-primitives)
    - [타입 지정 가변 인수 바인딩](#binding-typed-variadics)
    - [태깅](#tagging)
    - [바인딩 확장](#extending-bindings)
- [해결(Resolving)](#resolving)
    - [Make 메서드](#the-make-method)
    - [자동 주입](#automatic-injection)
- [메서드 호출과 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개

Laravel 서비스 컨테이너는 클래스 의존성 관리와 의존성 주입(Dependency Injection)을 수행하는 강력한 도구입니다. 의존성 주입이란, 클래스가 필요로 하는 의존성을 생성자나 경우에 따라 "세터(setter)" 메서드를 통해 "주입"하는 것을 의미합니다.

간단한 예시를 살펴봅시다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Repositories\UserRepository;
use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스 생성자.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * 주어진 사용자의 프로필을 보여줍니다.
     */
    public function show(string $id): View
    {
        $user = $this->users->find($id);

        return view('user.profile', ['user' => $user]);
    }
}
```

이 예시에서 `UserController`는 데이터 소스에서 사용자를 조회해야 합니다. 따라서 사용자 정보를 조회할 수 있는 서비스를 **주입**합니다. 이 문맥에서 `UserRepository`는 대개 데이터베이스에서 사용자를 조회하기 위해 [Eloquent](/docs/{{version}}/eloquent)를 사용합니다. 그러나 저장소 레이어가 주입되어 있기 때문에 다른 구현체로 손쉽게 교체가 가능합니다. 또한 테스트시 `UserRepository`의 목(mock) 또는 더미 구현을 쉽게 만들 수도 있습니다.

Laravel 서비스 컨테이너에 대한 깊은 이해는 강력하고 대규모의 애플리케이션을 만들 때, 그리고 Laravel 코어에 기여할 때 필수적입니다.

<a name="zero-configuration-resolution"></a>
### 제로 구성 해상(Zero Configuration Resolution)

클래스가 의존성이 없거나 오직 다른 구체 클래스(인터페이스가 아닌)만 의존하고 있다면, 컨테이너는 해당 클래스를 어떻게 해석할지 지시를 받을 필요가 없습니다. 예를 들어, 다음 코드를 여러분의 `routes/web.php` 파일에 넣을 수 있습니다.

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

이 경우, 애플리케이션의 `/` 경로에 접속하면 `Service` 클래스가 자동으로 해석되어 라우트의 핸들러에 주입됩니다. 이는 엄청난 변화입니다. 즉, 여러분은 비대한 설정 파일을 신경 쓰지 않고도 애플리케이션을 개발할 때 의존성 주입의 이점을 누릴 수 있습니다.

다행히도, 여러분이 Laravel 애플리케이션을 구축할 때 작성하는 많은 클래스들은 [컨트롤러](/docs/{{version}}/controllers), [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등과 같이 컨테이너를 통해 자동으로 의존성을 받습니다. 또한, [큐 작업](/docs/{{version}}/queues)의 `handle` 메서드에서도 의존성을 타입힌트할 수 있습니다. 자동화되고 설정이 필요 없는 의존성 주입을 한번 경험하면 그 없이 개발하는 것이 어렵게 느껴질 것입니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 언제 사용해야 하는가

제로 구성 해상 덕분에 대부분의 경우 라우트, 컨트롤러, 이벤트 리스너 등에서 단순히 의존성을 타입힌트하면 수동으로 컨테이너에 직접 접근할 필요가 없습니다. 예를 들어, 현재 요청에 접근하기 위해 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입힌트할 수 있습니다. 우리는 직접 컨테이너를 다루지 않아도 되지만, 실제로는 컨테이너가 이 의존성들의 주입을 관리해줍니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

대부분의 경우, 자동 의존성 주입과 [파사드](/docs/{{version}}/facades) 덕분에 컨테이너에서 무언가를 수동으로 바인딩하거나 해석할 필요 없이 Laravel 애플리케이션을 만들 수 있습니다. **그렇다면 언제 직접 컨테이너와 상호작용해야 할까요?** 두 가지 상황을 살펴봅시다.

첫 번째는, 인터페이스를 구현하는 클래스를 작성하고 그 인터페이스를 라우트 또는 클래스 생성자에 타입힌트하려 할 때, 반드시 [컨테이너에 인터페이스 해석 방법](#binding-interfaces-to-implementations)을 알려주어야 합니다. 두 번째로, 다른 Laravel 개발자들과 공유할 [패키지](/docs/{{version}}/packages)를 작성할 때, 패키지의 서비스를 컨테이너에 바인딩해야 할 수도 있습니다.

<a name="binding"></a>
## 바인딩

<a name="binding-basics"></a>
### 바인딩 기본

<a name="simple-bindings"></a>
#### 간단한 바인딩

여러분의 거의 모든 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/{{version}}/providers) 내에 등록됩니다. 따라서 아래의 예제들은 이 맥락에서 컨테이너를 사용하는 방법을 보여줍니다.

서비스 프로바이더 내에서는 항상 `$this->app` 프로퍼티를 통해 컨테이너에 접근할 수 있습니다. `bind` 메서드를 사용해서 바인딩을 등록할 수 있으며, 등록하려는 클래스나 인터페이스 이름과 해당 클래스의 인스턴스를 반환하는 클로저를 전달합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

이 때, 클로저의 인자로 컨테이너 인스턴스 자체를 받습니다. 이를 이용해 하위 의존성들도 컨테이너로부터 해석할 수 있습니다.

앞서 언급한 것처럼, 대개 서비스 프로바이더에서 컨테이너를 사용하게 됩니다. 그러나 서비스 프로바이더 외부에서도 [파사드](/docs/{{version}}/facades)를 통해 컨테이너에 접근할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

`bindIf` 메서드를 사용하면, 해당 타입에 대해 이미 바인딩이 등록되지 않은 경우에만 바인딩을 등록할 수 있습니다.

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]  
> 어떤 클래스도 인터페이스에 의존하지 않는다면 굳이 컨테이너에 바인딩할 필요는 없습니다. 컨테이너는 리플렉션을 통해 이러한 오브젝트를 자동으로 해석할 수 있습니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩

`singleton` 메서드는 컨테이너에 클래스나 인터페이스를 한 번만 해석하도록 바인딩합니다. 싱글톤 바인딩이 한 번 해석되면, 이후의 요청에서는 동일 인스턴스가 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

`singletonIf` 메서드를 사용하면 해당 타입에 바인딩이 없을 때만 싱글톤으로 등록합니다.

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 스코프 싱글톤 바인딩

`scoped` 메서드는 주어진 Laravel 요청/잡(lifecycle) 내에서 한 번만 해석되어야 하는 클래스 또는 인터페이스를 바인딩합니다. 이 방법은 `singleton`과 비슷하지만, `scoped`로 등록된 인스턴스는 [Laravel Octane](/docs/{{version}}/octane) 워커가 새로운 요청을 처리하거나 [큐 작업자](/docs/{{version}}/queues)가 새로운 작업을 처리할 때마다 초기화됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩

이미 생성된 오브젝트 인스턴스를 `instance` 메서드를 통해 컨테이너에 바인딩할 수도 있습니다. 이렇게 하면, 이후의 요청에서는 항상 해당 인스턴스가 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기

서비스 컨테이너의 매우 강력한 기능 중 하나는 인터페이스를 특정 구현체에 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher` 인터페이스와 `RedisEventPusher` 구현체가 있다고 가정해 봅시다. 다음과 같이 등록할 수 있습니다.

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이 구문은 어떤 클래스가 `EventPusher`가 필요할 때 `RedisEventPusher`를 주입해야 함을 컨테이너에 알려줍니다. 이제 컨테이너가 해석하는 클래스의 생성자에 `EventPusher` 인터페이스를 타입힌트할 수 있습니다. 컨트롤러, 이벤트 리스너, 미들웨어 등 Laravel 애플리케이션의 다양한 클래스들은 항상 컨테이너를 통해 해석된다는 점을 기억하세요.

```php
use App\Contracts\EventPusher;

/**
 * 새로운 클래스 인스턴스 생성자.
 */
public function __construct(
    protected EventPusher $pusher
) {}
```

<a name="contextual-binding"></a>
### 상황별 바인딩(Contextual Binding)

동일한 인터페이스를 사용하는 두 개의 클래스가 있지만 각각에 서로 다른 구현체를 주입해야 할 수도 있습니다. 예를 들어, 두 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` [계약](/docs/{{version}}/contracts)의 서로 다른 구현에 의존할 수 있습니다. Laravel은 이를 위한 간결한 인터페이스를 제공합니다.

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

<a name="binding-primitives"></a>
### 기본값 바인딩(Primitives)

클래스가 주입받아야 하는 클래스들 외에 정수 등과 같은 기본값(primitive)도 주입받아야 할 때가 있습니다. 상황별 바인딩을 사용하여 이런 값을 손쉽게 주입할 수 있습니다.

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
          ->needs('$variableName')
          ->give($value);
```

어떤 클래스가 [태그된](#tagging) 인스턴스 배열에 의존하는 경우 `giveTagged` 메서드를 사용하면 해당 태그와 함께 바인딩된 모든 인스턴스를 손쉽게 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션의 설정 파일에서 값을 주입해야 할 경우 `giveConfig` 메서드를 사용할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입 지정 가변 인수 바인딩

가끔, 가변 인수(variadic) 생성자를 사용하여 객체 배열을 받는 클래스가 있을 수 있습니다.

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
     * 새로운 클래스 인스턴스 생성자.
     */
    public function __construct(
        protected Logger $logger,
        Filter ...$filters,
    ) {
        $this->filters = $filters;
    }
}
```

상황별 바인딩과 `give` 메서드에 클로저를 넘겨주면 `Filter` 인스턴스 배열을 주입할 수 있습니다.

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

혹은 더 간단하게, 클래스 이름 배열을 전달하면 `Firewall`이 `Filter` 인스턴스를 필요로 할 때마다 컨테이너가 해석합니다.

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

클래스에 가변(variadic) 의존성이 있고, 타입힌트가 특정 클래스(`Report ...$reports`)인 경우, `needs`와 `giveTagged` 메서드를 이용해 [태그](#tagging)된 컨테이너 바인딩 인스턴스 전체를 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅(Tagging)

가끔 특정 "카테고리"에 해당하는 바인딩 전체를 해석해야 할 때도 있습니다. 예를 들어, 다수의 서로 다른 `Report` 인터페이스 구현 배열을 받는 리포트 분석 도구를 만들고 있다고 가정합시다. 먼저 각각의 `Report` 구현을 등록한 후 `tag` 메서드로 태그를 지정합니다.

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

태깅된 서비스들은 `tagged` 메서드를 통해 모두 해석할 수 있습니다.

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장(Extending Bindings)

`extend` 메서드는 이미 해석된 서비스 인스턴스를 수정할 수 있게 해줍니다. 예를 들어, 서비스가 해석될 때 추가 코드를 실행해 서비스에 데코레이터를 적용하거나 설정을 변경할 수 있습니다. `extend`의 인자로는 확장할 서비스 클래스와, 수정된 서비스를 반환해야 하는 클로저가 들어갑니다. 이 클로저는 해석된 서비스와 컨테이너 인스턴스를 인자로 받습니다.

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해석(Resolving)

<a name="the-make-method"></a>
### `make` 메서드

`make` 메서드는 컨테이너에서 클래스 인스턴스를 해석할 때 사용합니다. 인자로 클래스 또는 인터페이스 이름을 넣습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스의 일부 의존성이 컨테이너로 해석이 불가능하면, 연관 배열을 `makeWith` 메서드에 전달하여 수동으로 인자를 넣을 수 있습니다. 예를 들어, `Transistor` 서비스의 `$id` 생성자 인자를 수동으로 전달할 수 있습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드는 클래스나 인터페이스가 컨테이너에 명시적으로 바인딩되어 있는지 확인할 때 사용합니다.

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더 외부에서 `$app` 변수가 없는 곳에서는 [파사드](/docs/{{version}}/facades) 또는 [helper](/docs/{{version}}/helpers#method-app)를 통해 인스턴스를 해석할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

컨테이너 인스턴스 자체를 주입받고 싶다면, 생성자에서 `Illuminate\Container\Container` 클래스를 타입힌트하면 됩니다.

```php
use Illuminate\Container\Container;

/**
 * 새로운 클래스 인스턴스 생성자.
 */
public function __construct(
    protected Container $container
) {}
```

<a name="automatic-injection"></a>
### 자동 주입(Automatic Injection)

또한, 컨테이너가 해석하는 클래스(예: [컨트롤러](/docs/{{version}}/controllers), [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등)의 생성자에 단순히 의존성을 타입힌트해 자동 주입받을 수 있습니다. [큐 작업](/docs/{{version}}/queues)의 `handle` 메서드에서도 의존성 타입힌트가 가능합니다. 실제로, 대부분의 오브젝트는 이 방법으로 컨테이너에 의해 해석되어야 합니다.

예를 들어, 컨트롤러 생성자에서 저장소를 타입힌트하면 저장소 인스턴스가 자동으로 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;
use App\Models\User;

class UserController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스 생성자.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * 주어진 ID의 사용자를 보여줍니다.
     */
    public function show(string $id): User
    {
        $user = $this->users->findOrFail($id);

        return $user;
    }
}
```

<a name="method-invocation-and-injection"></a>
## 메서드 호출과 주입

때때로, 오브젝트 인스턴스의 메서드를 호출할 때 그 메서드가 의존하는 객체들을 컨테이너가 자동으로 주입하도록 하고 싶을 수 있습니다. 예를 들어, 아래와 같은 클래스가 있다고 가정합시다.

```php
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

컨테이너를 통해 아래처럼 `generate` 메서드를 호출할 수 있습니다.

```php
use App\UserReport;
use Illuminate\Support\Facades\App;

$report = App::call([new UserReport, 'generate']);
```

`call` 메서드는 모든 PHP 콜러블을 받을 수 있습니다. 또한 클로저조차도 컨테이너의 `call` 메서드를 이용해 의존성을 자동 주입받아 호출할 수 있습니다.

```php
use App\Repositories\UserRepository;
use Illuminate\Support\Facades\App;

$result = App::call(function (UserRepository $repository) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트

서비스 컨테이너는 객체를 해석할 때마다 이벤트를 발생시킵니다. 이 이벤트는 `resolving` 메서드를 사용하여 감지할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입의 오브젝트가 해석될 때 호출됩니다...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 모든 타입의 오브젝트가 해석될 때 호출됩니다...
});
```

이벤트 콜백으로 해석된 오브젝트가 전달되므로, 오브젝트가 실제로 사용되기 전에 추가 속성을 세팅하는 등 다양한 처리가 가능합니다.

<a name="psr-11"></a>
## PSR-11

Laravel의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서, PSR-11 컨테이너 인터페이스를 타입힌트하여 Laravel 컨테이너 인스턴스를 얻을 수 있습니다.

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

주어진 식별자를 해석할 수 없는 경우 예외가 발생합니다. 만약 해당 식별자가 아예 바인딩된 적이 없으면 `Psr\Container\NotFoundExceptionInterface` 인스턴스가, 바인딩되었으나 해석할 수 없는 경우 `Psr\Container\ContainerExceptionInterface` 인스턴스가 예외로 던져집니다.