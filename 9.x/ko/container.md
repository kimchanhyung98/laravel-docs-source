# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [무설정 자동 해석(Zero Configuration Resolution)](#zero-configuration-resolution)
    - [컨테이너를 언제 사용해야 하나요?](#when-to-use-the-container)
- [바인딩 (Binding)](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [컨텍스트별 바인딩 (Contextual Binding)](#contextual-binding)
    - [원시 값 바인딩하기 (Binding Primitives)](#binding-primitives)
    - [타입별 가변 인자 바인딩하기 (Binding Typed Variadics)](#binding-typed-variadics)
    - [태깅 (Tagging)](#tagging)
    - [바인딩 확장하기 (Extending Bindings)](#extending-bindings)
- [해결하기 (Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 주입 (Automatic Injection)](#automatic-injection)
- [메서드 호출과 주입 (Method Invocation & Injection)](#method-invocation-and-injection)
- [컨테이너 이벤트 (Container Events)](#container-events)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 서비스 컨테이너는 클래스 의존성을 관리하고 의존성 주입(dependency injection)을 수행하기 위한 강력한 도구입니다. 의존성 주입이란 간단히 말해, 클래스가 필요한 의존성(다른 클래스의 인스턴스 등)을 보통 생성자(constructor)나 때로는 세터(setter) 메서드를 통해 주입(inject)하는 것을 뜻합니다.

간단한 예를 살펴보겠습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Repositories\UserRepository;
use App\Models\User;

class UserController extends Controller
{
    /**
     * 사용자 저장소 구현체.
     *
     * @var UserRepository
     */
    protected $users;

    /**
     * 새로운 컨트롤러 인스턴스 생성자.
     *
     * @param  UserRepository  $users
     * @return void
     */
    public function __construct(UserRepository $users)
    {
        $this->users = $users;
    }

    /**
     * 주어진 사용자 프로필을 보여줍니다.
     *
     * @param  int  $id
     * @return Response
     */
    public function show($id)
    {
        $user = $this->users->find($id);

        return view('user.profile', ['user' => $user]);
    }
}
```

이 예제에서 `UserController`는 데이터 소스에서 사용자를 가져와야 합니다. 그래서 우리는 사용자를 조회할 수 있는 서비스를 **주입**합니다. 이 상황에서 `UserRepository`는 대부분 [Eloquent](/docs/9.x/eloquent)를 사용해 데이터베이스에서 사용자 정보를 가져오는 역할을 합니다. 그러나 이 저장소가 주입되므로, 다른 구현체로 쉽게 교체할 수 있다는 장점이 있습니다. 또한, 테스트 시에 `UserRepository`의 목(mock) 또는 더미 구현체를 쉽게 만들 수도 있습니다.

Laravel 서비스 컨테이너를 깊이 이해하는 것은 강력하고 규모가 큰 애플리케이션을 구축하는 데 필수적이며, Laravel 코어 기여에도 중요합니다.

<a name="zero-configuration-resolution"></a>
### 무설정 자동 해석 (Zero Configuration Resolution)

클래스가 의존성이 없거나, 인터페이스가 아닌 구체적 클래스에만 의존한다면, 컨테이너에 해당 클래스를 해결하는 방법을 따로 알려줄 필요가 없습니다. 예를 들어, `routes/web.php`에 다음 코드를 작성할 수 있습니다:

```php
<?php

class Service
{
    //
}

Route::get('/', function (Service $service) {
    die(get_class($service));
});
```

이 예시에서 애플리케이션의 `/` 라우트를 호출하면 `Service` 클래스가 자동으로 해결되어 라우트 핸들러에 주입됩니다. 이는 매우 혁신적입니다. 즉, 별도의 복잡한 설정 파일을 걱정하지 않고도, 의존성 주입을 활용하며 애플리케이션을 개발할 수 있다는 뜻입니다.

다행히도, Laravel에서 작성하는 대부분의 클래스들은 [컨트롤러](/docs/9.x/controllers), [이벤트 리스너](/docs/9.x/events), [미들웨어](/docs/9.x/middleware) 등과 같이 의존성을 컨테이너를 통해 자동으로 주입받습니다. 또한, [큐 작업](/docs/9.x/queues)의 `handle` 메서드에서도 의존성 주입이 가능합니다. 이렇게 자동이고 무설정인 의존성 주입의 힘을 한 번 맛보면, 없이는 개발하기 어려울 정도입니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 언제 사용해야 하나요? (When To Use The Container)

무설정 자동 해석 덕분에 라우트, 컨트롤러, 이벤트 리스너 등에서 의존성을 타입힌트만 하면, 컨테이너를 직접 다루지 않고도 의존성은 자동으로 주입됩니다. 예를 들어, 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입힌트하여 현재 요청을 쉽게 접근할 수 있습니다. 코드를 작성할 때 컨테이너를 직접 다룰 필요는 없지만, 실제로는 컨테이너가 그 뒤에서 의존성들의 주입을 관리합니다:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

많은 경우, 자동 의존성 주입과 [파사드(facades)](/docs/9.x/facades) 덕분에 Laravel 애플리케이션을 개발할 때 **직접적으로** 컨테이너에 바인딩하거나 해결(resolving)하는 일을 전혀 하지 않아도 됩니다. **그렇다면 직접 컨테이너를 다뤄야 할 경우는 언제인가요?** 두 가지 상황을 살펴보겠습니다.

첫 번째는, 어떤 클래스가 인터페이스를 구현하며 그 인터페이스를 라우트나 클래스 생성자에서 타입힌트하려 할 때입니다. 이때는 [컨테이너에 그 인터페이스가 어떤 구현체와 연결되는지 알려줘야 합니다](#binding-interfaces-to-implementations). 두 번째는, 다른 Laravel 개발자와 공유할 [패키지](/docs/9.x/packages)를 작성할 때, 패키지의 서비스를 컨테이너에 바인딩해야 할 수도 있습니다.

<a name="binding"></a>
## 바인딩 (Binding)

<a name="binding-basics"></a>
### 바인딩 기본 (Binding Basics)

<a name="simple-bindings"></a>
#### 간단한 바인딩 (Simple Bindings)

대부분의 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/9.x/providers) 내에서 등록됩니다. 따라서 여기서의 예시 대부분은 서비스 프로바이더에서 컨테이너를 다루는 예시입니다.

서비스 프로바이더 안에서는 `$this->app` 속성을 통해 언제든 컨테이너에 접근할 수 있습니다. `bind` 메서드를 사용해 바인딩할 클래스 또는 인터페이스명을 전달하며, 콜백 함수 안에서 해당 클래스의 인스턴스를 반환합니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$this->app->bind(Transistor::class, function ($app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

주의할 점은, 콜백 함수의 인자로 컨테이너 자체가 전달된다는 것입니다. 따라서 생성하려는 객체의 하위 의존성도 컨테이너를 통해 해결할 수 있습니다.

대부분 서비스 프로바이더에서 컨테이너와 상호작용하지만, 서비스 프로바이더 밖에서도 `App` [파사드](/docs/9.x/facades)를 통해서 동일한 작업을 할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function ($app) {
    // ...
});
```

> [!NOTE]
> 만약 클래스가 인터페이스에 의존하지 않는다면, 굳이 컨테이너에 바인딩할 필요가 없습니다. 컨테이너는 리플렉션을 통해 이런 객체들을 자동으로 해결할 수 있기 때문입니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩하기 (Binding A Singleton)

`singleton` 메서드는 클래스나 인터페이스를 컨테이너에 한 번만 인스턴스화하여 바인딩합니다. 첫 요청 시 인스턴스를 생성한 후, 이후에 같은 인스턴스를 반환합니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$this->app->singleton(Transistor::class, function ($app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 스코프드 싱글톤 바인딩하기 (Binding Scoped Singletons)

`scoped` 메서드는 Laravel 요청이나 작업(job) 단위의 라이프사이클 동안에만 한 번 해결되어야 하는 클래스나 인터페이스를 바인딩합니다. `singleton`과 비슷하지만, `scoped`를 이용한 인스턴스는 [Laravel Octane](/docs/9.x/octane) 워커가 새 요청을 처리하거나 [큐 워커](/docs/9.x/queues)가 새 작업을 처리할 때마다 재설정됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$this->app->scoped(Transistor::class, function ($app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩하기 (Binding Instances)

이미 생성된 객체 인스턴스를 컨테이너에 바인딩할 수도 있습니다. `instance` 메서드를 사용하면, 이후에 해당 타입을 컨테이너에서 요청할 때 항상 같은 인스턴스가 반환됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기 (Binding Interfaces To Implementations)

서비스 컨테이너의 매우 강력한 기능 중 하나는 인터페이스를 특정 구현체에 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher` 인터페이스와 `RedisEventPusher` 구현체가 있다고 해봅시다. `RedisEventPusher` 구현체를 작성한 후, 다음과 같이 컨테이너에 등록할 수 있습니다:

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이 코드는 `EventPusher` 타입이 필요한 곳에 `RedisEventPusher`를 주입하라는 컨테이너에 대한 지시입니다. 이제 컨트롤러 등 컨테이너가 해결하는 클래스의 생성자에서 `EventPusher`를 타입힌트할 수 있습니다. 컨트롤러, 이벤트 리스너, 미들웨어 등 Laravel에서 다양한 클래스가 항상 컨테이너를 통해 해결됩니다:

```php
use App\Contracts\EventPusher;

/**
 * 새로운 클래스 인스턴스 생성자.
 *
 * @param  \App\Contracts\EventPusher  $pusher
 * @return void
 */
public function __construct(EventPusher $pusher)
{
    $this->pusher = $pusher;
}
```

<a name="contextual-binding"></a>
### 컨텍스트별 바인딩 (Contextual Binding)

때때로 같은 인터페이스를 사용하는 두 클래스가 있지만, 각각 다른 구현체를 주입받아야 할 수도 있습니다. 예를 들어, 두 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` [계약](/docs/9.x/contracts)에 의존하지만, 서로 다르게 구현된 파일시스템을 사용해야 할 경우가 있습니다. Laravel은 이를 손쉽게 처리할 수 있는 유창한 인터페이스를 제공합니다:

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

이 코드는 `PhotoController`에는 로컬 디스크를, `VideoController`와 `UploadController`에는 S3 디스크를 주입하도록 설정하고 있습니다.

<a name="binding-primitives"></a>
### 원시 값 바인딩하기 (Binding Primitives)

클래스가 주입받는 의존성 중에 다른 클래스뿐만 아니라 정수나 문자열 같은 원시 타입 값도 포함될 수 있습니다. 이때는 컨텍스트별 바인딩을 사용해 원하는 값을 주입할 수 있습니다:

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
          ->needs('$variableName')
          ->give($value);
```

만약 클래스가 [태깅](#tagging)된 여러 인스턴스 배열에 의존한다면, `giveTagged` 메서드를 사용해 해당 태그가 붙은 모든 바인딩 값을 쉽게 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션의 설정(config) 파일에 있는 값을 주입해야 할 때는 `giveConfig` 메서드를 사용할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입별 가변 인자 바인딩하기 (Binding Typed Variadics)

때로는 가변 인자(variadic)를 사용하는 생성자가 있을 수 있습니다. 예를 들어 다음과 같이 `Filter` 타입 객체들을 가변 인자로 받는 클래스가 있을 수 있습니다:

```php
<?php

use App\Models\Filter;
use App\Services\Logger;

class Firewall
{
    /**
     * 로거 인스턴스.
     *
     * @var \App\Services\Logger
     */
    protected $logger;

    /**
     * 필터 인스턴스 배열.
     *
     * @var array
     */
    protected $filters;

    /**
     * 새로운 클래스 인스턴스 생성자.
     *
     * @param  \App\Services\Logger  $logger
     * @param  array  $filters
     * @return void
     */
    public function __construct(Logger $logger, Filter ...$filters)
    {
        $this->logger = $logger;
        $this->filters = $filters;
    }
}
```

컨텍스트별 바인딩을 활용해 `give` 메서드에 필터 인스턴스들을 반환하는 콜백을 전달해 의존성을 해결할 수 있습니다:

```php
$this->app->when(Firewall::class)
          ->needs(Filter::class)
          ->give(function ($app) {
                return [
                    $app->make(NullFilter::class),
                    $app->make(ProfanityFilter::class),
                    $app->make(TooLongFilter::class),
                ];
          });
```

편의상, `Firewall` 클래스가 `Filter` 인스턴스들을 필요로 할 때마다 컨테이너가 해결할 클래스명 배열을 직접 줄 수도 있습니다:

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

가변 인자를 받는 의존성이 특정 클래스 타입으로 타입힌트되어 있다면 (`Report ...$reports`), `needs`와 `giveTagged`를 조합해 해당 태그가 붙은 모든 컨테이너 바인딩 인스턴스들을 쉽게 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅 (Tagging)

특정 "카테고리"에 속하는 모든 바인딩을 한꺼번에 해결해야 할 때가 있습니다. 예를 들어, 여러 `Report` 인터페이스 구현체 배열을 받는 리포트 분석기를 만든다고 해봅시다. 구현체를 등록한 후, `tag` 메서드를 사용해 해당 구현체들에 태그를 붙일 수 있습니다:

```php
$this->app->bind(CpuReport::class, function () {
    //
});

$this->app->bind(MemoryReport::class, function () {
    //
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

태그를 붙인 후에는 컨테이너의 `tagged` 메서드를 사용해 쉽게 태그된 모든 서비스를 해결할 수 있습니다:

```php
$this->app->bind(ReportAnalyzer::class, function ($app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장하기 (Extending Bindings)

`extend` 메서드를 사용하면, 이미 해결된 서비스를 수정하거나 꾸밀 수 있습니다. 예를 들어, 서비스가 컨테이너에서 해결된 후 추가 작업을 하는 데 사용할 수 있습니다. `extend`는 두 개의 인자를 받습니다: 확장하려는 서비스 클래스명과, 수정된 서비스를 반환하는 클로저입니다. 클로저는 현재 서비스 인스턴스와 컨테이너 인스턴스를 인자로 받습니다:

```php
$this->app->extend(Service::class, function ($service, $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해결하기 (Resolving)

<a name="the-make-method"></a>
### `make` 메서드

컨테이너에서 클래스 인스턴스를 해결할 때 `make` 메서드를 사용할 수 있습니다. 해결하려는 클래스 또는 인터페이스명을 인자로 넘기면 됩니다:

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스의 의존성 중 일부가 컨테이너에서 자동 해결되지 않는 경우, `makeWith` 메서드를 사용해 연관 배열로 생성자 인자를 직접 전달할 수 있습니다. 예를 들어 `Transistor` 서비스가 생성자 인자로 `$id`가 필요할 때는 다음과 같이 작성합니다:

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

서비스 프로바이더 밖에서 `$app` 변수에 접근할 수 없는 경우, `App` [파사드](/docs/9.x/facades) 또는 `app` [헬퍼](/docs/9.x/helpers#method-app)를 사용해 컨테이너에서 클래스 인스턴스를 생성할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

컨테이너 자체 인스턴스를 주입해야 할 경우, 생성자에 `Illuminate\Container\Container` 클래스를 타입힌트하면 됩니다:

```php
use Illuminate\Container\Container;

/**
 * 새로운 클래스 인스턴스 생성자.
 *
 * @param  \Illuminate\Container\Container  $container
 * @return void
 */
public function __construct(Container $container)
{
    $this->container = $container;
}
```

<a name="automatic-injection"></a>
### 자동 주입 (Automatic Injection)

또는, 클래스가 컨테이너에서 해결될 때 생성자에 의존성을 타입힌트하면 자동으로 주입됩니다. 이 기능은 [컨트롤러](/docs/9.x/controllers), [이벤트 리스너](/docs/9.x/events), [미들웨어](/docs/9.x/middleware), [큐 작업](/docs/9.x/queues)의 `handle` 메서드 등에서 기본으로 활용됩니다. 실제로 대부분 객체를 해결할 때는 이렇게 자동 주입을 사용하는 것이 권장됩니다.

예를 들어, 애플리케이션에서 정의한 저장소(repository)를 컨트롤러 생성자에서 타입힌트하면, 컨테이너가 자동으로 해당 저장소 인스턴스를 해결하고 주입합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * 사용자 저장소 인스턴스.
     *
     * @var \App\Repositories\UserRepository
     */
    protected $users;

    /**
     * 새로운 컨트롤러 인스턴스 생성자.
     *
     * @param  \App\Repositories\UserRepository  $users
     * @return void
     */
    public function __construct(UserRepository $users)
    {
        $this->users = $users;
    }

    /**
     * 주어진 ID에 해당하는 사용자를 보여줍니다.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        //
    }
}
```

<a name="method-invocation-and-injection"></a>
## 메서드 호출과 주입 (Method Invocation & Injection)

가끔 어떤 객체 인스턴스의 메서드를 호출할 때, 그 메서드가 필요로 하는 의존성들을 컨테이너가 자동으로 주입해주길 원할 수 있습니다. 예를 들어, 다음과 같은 클래스가 있다고 합시다:

```php
<?php

namespace App;

use App\Repositories\UserRepository;

class UserReport
{
    /**
     * 새로운 사용자 보고서를 생성합니다.
     *
     * @param  \App\Repositories\UserRepository  $repository
     * @return array
     */
    public function generate(UserRepository $repository)
    {
        // ...
    }
}
```

컨테이너의 `call` 메서드를 사용해 `generate` 메서드를 호출할 수 있습니다:

```php
use App\UserReport;
use Illuminate\Support\Facades\App;

$report = App::call([new UserReport, 'generate']);
```

`call` 메서드는 PHP의 모든 콜러블(callable)을 받습니다. 클로저를 호출할 때도, 해당 클로저가 필요한 의존성을 자동으로 주입해 호출할 수 있습니다:

```php
use App\Repositories\UserRepository;
use Illuminate\Support\Facades\App;

$result = App::call(function (UserRepository $repository) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트 (Container Events)

서비스 컨테이너는 객체가 해결될 때마다 이벤트를 발행합니다. `resolving` 메서드를 사용하여 특정 타입 또는 모든 타입이 컨테이너에 의해 해결될 때 리스닝할 수 있습니다:

```php
use App\Services\Transistor;

$this->app->resolving(Transistor::class, function ($transistor, $app) {
    // "Transistor" 타입 객체가 컨테이너에서 해결될 때 호출됩니다...
});

$this->app->resolving(function ($object, $app) {
    // 컨테이너가 모든 타입의 객체를 해결할 때 호출됩니다...
});
```

콜백에는 해결 중인 객체와 컨테이너 인스턴스가 전달되므로, 이 시점에 객체의 추가 속성을 설정하는 등의 작업을 할 수 있습니다.

<a name="psr-11"></a>
## PSR-11

Laravel 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서 PSR-11 컨테이너 인터페이스를 타입힌트하여 Laravel 컨테이너 인스턴스를 받을 수 있습니다:

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    //
});
```

만약 지정한 식별자(identifier)를 해결할 수 없으면 예외가 발생합니다. 식별자가 바인딩된 적이 없다면 `Psr\Container\NotFoundExceptionInterface`를 구현하는 예외가, 바인딩은 됐지만 해결할 수 없는 경우에는 `Psr\Container\ContainerExceptionInterface`를 구현하는 예외가 던져집니다.