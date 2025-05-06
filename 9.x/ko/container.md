# 서비스 컨테이너

- [소개](#introduction)
    - [제로 설정(Zero Configuration) 해석](#zero-configuration-resolution)
    - [컨테이너를 사용해야 할 때](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩](#binding-interfaces-to-implementations)
    - [컨텍스트 바인딩](#contextual-binding)
    - [기본값(Primitive) 바인딩](#binding-primitives)
    - [타입 명시 가변인자 바인딩](#binding-typed-variadics)
    - [태깅(Tagging)](#tagging)
    - [바인딩 확장](#extending-bindings)
- [해결(Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 주입](#automatic-injection)
- [메서드 호출 & 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개

Laravel 서비스 컨테이너는 클래스 의존성 관리와 의존성 주입을 수행하는 강력한 도구입니다. 의존성 주입(Dependency Injection)은 말 그대로 클래스에 필요한 의존성을 생성자나, 때로는 'setter' 메서드를 통해 "주입"하는 것을 의미합니다.

간단한 예제를 살펴보겠습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Repositories\UserRepository;
use App\Models\User;

class UserController extends Controller
{
    /**
     * 사용자 리포지토리 구현체.
     *
     * @var UserRepository
     */
    protected $users;

    /**
     * 새로운 컨트롤러 인스턴스 생성.
     *
     * @param  UserRepository  $users
     * @return void
     */
    public function __construct(UserRepository $users)
    {
        $this->users = $users;
    }

    /**
     * 주어진 사용자의 프로필을 보여줍니다.
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

이 예제에서, `UserController`는 데이터소스에서 사용자를 조회해야 합니다. 따라서 사용자를 조회할 수 있는 서비스를 **주입**합니다. 이 컨텍스트에서 `UserRepository`는 데이터베이스에서 사용자 정보를 조회하기 위해 [Eloquent](/docs/{{version}}/eloquent)를 사용할 가능성이 높습니다. 하지만 레포지토리가 주입되어 있기 때문에, 다른 구현체로 쉽게 교체할 수 있습니다. 또한 테스트 시 `UserRepository`의 목(Mock)이나 더미 구현체를 손쉽게 생성해서 사용할 수 있습니다.

Laravel 서비스 컨테이너를 깊이 있게 이해하는 것은 강력하고 대규모의 애플리케이션을 개발하거나, Laravel 코어에 기여할 때 필수입니다.

<a name="zero-configuration-resolution"></a>
### 제로 설정(Zero Configuration) 해석

클래스가 의존성이 없거나 오직 다른 구체 클래스(인터페이스가 아님)만을 의존한다면, 컨테이너에 해당 클래스를 어떻게 해석해야 하는지 별도로 알려줄 필요가 없습니다. 예를 들어, 아래와 같은 코드를 `routes/web.php` 파일에 작성할 수 있습니다:

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

이 예제에서, 애플리케이션의 `/` 경로로 접속하면 `Service` 클래스가 자동으로 해석되어 라우트 핸들러에 주입됩니다. 이 기능은 개발 패러다임을 크게 변화시킵니다. 별도의 설정 파일로 골치 아플 필요 없이, 의존성 주입의 이점을 누릴 수 있습니다.

다행히도, [컨트롤러](/docs/{{version}}/controllers), [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등 Laravel 애플리케이션에서 작성하게 되는 많은 클래스들은 자동으로 컨테이너를 통해 의존성을 주입받습니다. 또한 [큐 작업](/docs/{{version}}/queues)의 `handle` 메서드에도 의존성을 타입힌트할 수 있습니다. 일단 자동적이고 제로 설정의 의존성 주입의 위력을 경험하면, 그 없이는 개발이 불가능하다고 느껴질지도 모릅니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 사용해야 할 때

제로 설정 해석 기능 덕분에, 종종 컨테이너와 직접적으로 상호작용하지 않고도 라우트, 컨트롤러, 이벤트 리스너 등에서 의존성을 타입힌트할 수 있습니다. 예를 들어, 현재 요청을 쉽게 접근하기 위해 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입힌트할 수 있습니다. 비록 코드에서 직접 컨테이너를 다루지 않지만, 실제로 컨테이너가 이러한 의존성 주입을 백그라운드에서 관리합니다:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

많은 경우, 자동 의존성 주입과 [파사드](/docs/{{version}}/facades) 덕분에, 컨테이너에서 무언가를 직접 바인딩하거나 해석하지 않고도 Laravel 애플리케이션을 개발할 수 있습니다. **그렇다면, 언제 직접 컨테이너와 상호작용해야 할까요?** 두 가지 상황을 살펴봅시다.

첫째, 어떤 클래스가 인터페이스를 구현하고, 해당 인터페이스를 라우트나 클래스의 생성자에서 타입힌트하고 싶을 때는 [컨테이너에 해당 인터페이스의 해석 방법을 등록](#binding-interfaces-to-implementations)해야 합니다. 둘째, [Laravel 패키지](/docs/{{version}}/packages)를 작성하여 다른 개발자와 공유하고자 할 때, 패키지의 서비스들을 컨테이너에 바인딩해야 할 수도 있습니다.

<a name="binding"></a>
## 바인딩

<a name="binding-basics"></a>
### 바인딩 기본

<a name="simple-bindings"></a>
#### 단순 바인딩

대부분의 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/{{version}}/providers)에서 등록됩니다. 따라서 대부분의 예제에서는 서비스 프로바이더에서 컨테이너를 사용하는 방식을 다룹니다.

서비스 프로바이더 내에서는 항상 `$this->app` 속성을 통해 컨테이너에 접근할 수 있습니다. `bind` 메서드를 사용하여 등록할 클래스(또는 인터페이스) 이름과, 해당 클래스 인스턴스를 반환하는 클로저를 전달하면 바인딩할 수 있습니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$this->app->bind(Transistor::class, function ($app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

주의할 점은, 해석기(클로저)의 인자로 컨테이너 자체가 전달된다는 것입니다. 따라서, 우리가 생성하는 객체의 하위 의존성 또한 컨테이너를 통해 해석할 수 있습니다.

앞서 언급했듯, 보통은 서비스 프로바이더 내에서 컨테이너와 상호작용하지만, 서비스 프로바이더 외부에서 컨테이너와 상호작용하고 싶다면 `App` [파사드](/docs/{{version}}/facades)를 사용할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function ($app) {
    // ...
});
```

> **참고**
> 만약 클래스가 어떤 인터페이스에도 의존하지 않는다면, 컨테이너에 별도로 바인딩할 필요가 없습니다. 컨테이너는 리플렉션(reflection)을 통해 이러한 객체를 자동으로 해석할 수 있기 때문입니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩

`singleton` 메서드는 컨테이너에 한 번만 해석될 클래스 또는 인터페이스를 바인딩합니다. 싱글톤 바인딩이 한 번 해석되면, 이후에는 같은 인스턴스가 항상 반환됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$this->app->singleton(Transistor::class, function ($app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 스코프 싱글톤 바인딩

`scoped` 메서드는 클래스나 인터페이스를 바인딩하되, 한 Laravel 요청/작업(job) 라이프사이클 내에서 한 번만 해석하도록 합니다. 이 메서드는 `singleton`과 유사하지만, [Laravel Octane](/docs/{{version}}/octane) 워커가 새로운 요청을 처리할 때나 [큐 워커](/docs/{{version}}/queues)가 새로운 작업을 처리할 때마다 인스턴스가 초기화됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$this->app->scoped(Transistor::class, function ($app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩

이미 생성된 객체 인스턴스를 `instance` 메서드로 컨테이너에 바인딩할 수 있습니다. 이후 컨테이너에서는 항상 해당 인스턴스를 반환합니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩

서비스 컨테이너의 매우 강력한 기능 중 하나는, 인터페이스를 특정 구현체에 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher` 인터페이스와 `RedisEventPusher` 구현체가 있다고 가정해 봅니다. `RedisEventPusher` 구현을 완료했다면, 아래와 같이 서비스 컨테이너에 등록할 수 있습니다:

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이 코드는 컨테이너에 `EventPusher` 구현이 필요할 때마다 `RedisEventPusher`를 주입하라고 지시합니다. 이제 컨테이너에서 해석되는 클래스의 생성자에서 `EventPusher` 인터페이스를 타입힌트할 수 있습니다. 컨트롤러, 이벤트 리스너, 미들웨어 등 Laravel의 다양한 클래스는 항상 컨테이너를 통해 해석된다는 점을 기억하세요.

```php
use App\Contracts\EventPusher;

/**
 * 새로운 클래스 인스턴스 생성.
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
### 컨텍스트 바인딩

가끔씩, 두 클래스가 같은 인터페이스를 사용하더라도 서로 다른 구현체를 주입해야 할 때가 있습니다. 예를 들어, 두 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` [계약(Contract)](/docs/{{version}}/contracts)의 서로 다른 구현을 필요로 한다면, Laravel의 컨텍스트 바인딩 기능을 사용할 수 있습니다:

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
### 기본값(Primitive) 바인딩

클래스가 여러 의존성을 주입받으면서, 동시에 정수 등의 기본값(primitive)도 필요할 수 있습니다. 컨텍스트 바인딩을 이용하면 필요한 어떤 값도 주입할 수 있습니다:

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
          ->needs('$variableName')
          ->give($value);
```

클래스가 [태깅](#tagging) 인스턴스 배열에 의존하는 경우, `giveTagged` 메서드로 해당 태그의 모든 바인딩을 배열로 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션 구성 파일의 값을 주입해야 한다면, `giveConfig` 메서드를 사용할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입 명시 가변인자 바인딩

가끔 가변 인자(variadic) 생성자 인수를 통해 타입이 지정된 객체 배열을 받는 클래스가 있을 수 있습니다:

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
     * 새로운 클래스 인스턴스 생성.
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

컨텍스트 바인딩으로, `give` 메서드에 클로저를 전달하여 `Filter` 인스턴스들의 배열을 반환하도록 할 수 있습니다:

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

더 간편하게, 클래스 이름 배열만 제공해도, `Firewall`에서 `Filter` 인스턴스가 필요할 때 컨테이너가 해당 클래스를 자동으로 해석할 수 있습니다:

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

클래스가 가변 인자를 특정 클래스(예: `Report ...$reports`)로 타입힌트하는 경우, `needs` 및 `giveTagged` 메서드로 해당 태그에 바인딩된 모든 인스턴스를 배열로 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅(Tagging)

때로는 특정 "카테고리"의 바인딩을 모두 해석해야 할 때가 있습니다. 예를 들어, 여러 `Report` 인터페이스 구현체 배열을 받는 리포트 분석기를 만든다고 합시다. 각 리포트 구현체를 등록한 뒤, `tag` 메서드를 사용해 태그를 지정할 수 있습니다:

```php
$this->app->bind(CpuReport::class, function () {
    //
});

$this->app->bind(MemoryReport::class, function () {
    //
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

이제 서비스에 태그가 지정되었기 때문에, 컨테이너의 `tagged` 메서드로 모두 해석할 수 있습니다:

```php
$this->app->bind(ReportAnalyzer::class, function ($app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장

`extend` 메서드로 해석된 서비스 인스턴스를 수정할 수 있습니다. 예를 들어, 서비스가 해석될 때 꾸미기(Decorate)나 추가 설정 코드를 실행할 수 있습니다. `extend`는 2개의 인자를 받으며, 첫번째는 확장할 서비스 클래스이고, 두번째는 수정된 서비스를 반환하는 클로저입니다. 이 클로저는 해석 중인 서비스와 컨테이너 인스턴스를 전달받습니다:

```php
$this->app->extend(Service::class, function ($service, $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해석(Resolving)

<a name="the-make-method"></a>
### `make` 메서드

컨테이너의 `make` 메서드로 클래스 인스턴스를 해석할 수 있습니다. `make`에는 해석할 클래스 또는 인터페이스 이름을 전달합니다:

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스의 일부 의존성이 컨테이너에서 해석되지 않는 경우, `makeWith` 메서드에 연관 배열로 추가 인수를 직접 전달할 수 있습니다. 예를 들어, `Transistor` 서비스에서 `id` 생성자 인수를 직접 전달할 수 있습니다:

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

서비스 프로바이더 외부에서 `$app` 변수가 없는 코드 위치라면, `App` [파사드](/docs/{{version}}/facades)나 `app` [헬퍼 함수](/docs/{{version}}/helpers#method-app)로 컨테이너에서 클래스 인스턴스를 해석할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

컨테이너에서 해결되는 클래스의 생성자에 컨테이너 인스턴스 자체를 주입받고 싶다면, `Illuminate\Container\Container` 클래스를 타입힌트하면 됩니다:

```php
use Illuminate\Container\Container;

/**
 * 새로운 클래스 인스턴스 생성.
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
### 자동 주입

또한 컨테이너에서 해석되는 클래스의 생성자에서 의존성을 타입힌트(명시)하면, 컨테이너가 자동으로 주입합니다. [컨트롤러](/docs/{{version}}/controllers), [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등 다양한 곳에서 자동 주입을 활용할 수 있습니다. 또한 [큐 작업](/docs/{{version}}/queues)의 `handle` 메서드에서도 의존성을 타입힌트할 수 있습니다. 실무에서는 대부분 객체가 이렇게 자동으로 주입됩니다.

예를 들어, 컨트롤러의 생성자에 리포지토리를 타입힌트하면, 컨테이너가 이를 자동으로 해석해 주입합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * 사용자 리포지토리 인스턴스.
     *
     * @var \App\Repositories\UserRepository
     */
    protected $users;

    /**
     * 새로운 컨트롤러 인스턴스 생성.
     *
     * @param  \App\Repositories\UserRepository  $users
     * @return void
     */
    public function __construct(UserRepository $users)
    {
        $this->users = $users;
    }

    /**
     * 주어진 ID의 사용자를 보여줍니다.
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
## 메서드 호출 & 주입

객체 인스턴스의 메서드를 컨테이너가 자동으로 인자의 의존성을 주입하면서 호출하고 싶을 때가 있습니다. 예를 들어 아래와 같은 클래스가 있다면:

```php
<?php

namespace App;

use App\Repositories\UserRepository;

class UserReport
{
    /**
     * 새로운 유저 리포트 생성.
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

컨테이너의 `call` 메서드로 `generate`를 호출할 수 있습니다:

```php
use App\UserReport;
use Illuminate\Support\Facades\App;

$report = App::call([new UserReport, 'generate']);
```

`call` 메서드는 PHP의 어디서든 호출 가능한(callable) 것을 인자로 받습니다. 클로저에도 자동으로 의존성을 주입하면서 호출할 수 있습니다:

```php
use App\Repositories\UserRepository;
use Illuminate\Support\Facades\App;

$result = App::call(function (UserRepository $repository) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트

서비스 컨테이너는 객체가 해석될 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 통해 이 이벤트를 감지할 수 있습니다:

```php
use App\Services\Transistor;

$this->app->resolving(Transistor::class, function ($transistor, $app) {
    // "Transistor" 타입 객체가 해석될 때 호출됨...
});

$this->app->resolving(function ($object, $app) {
    // 모든 타입의 객체가 해석될 때 호출됨...
});
```

해석될 객체가 콜백에 전달되어, 최종적으로 소비자에게 전달되기 전에 추가 속성을 설정할 수 있습니다.

<a name="psr-11"></a>
## PSR-11

Laravel의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서 PSR-11 컨테이너 인터페이스를 타입힌트하여 Laravel 컨테이너 인스턴스를 얻을 수 있습니다:

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    //
});
```

주어진 식별자를 해석할 수 없다면 예외가 발생합니다. 식별자가 바인딩되지 않았다면 `Psr\Container\NotFoundExceptionInterface`의 인스턴스가 발생합니다. 식별자가 바인딩되었지만 해석할 수 없는 경우에는 `Psr\Container\ContainerExceptionInterface`의 인스턴스가 발생합니다.
