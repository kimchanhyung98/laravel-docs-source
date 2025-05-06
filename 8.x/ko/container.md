# 서비스 컨테이너

- [소개](#introduction)
    - [무설정(Zero Configuration) 해석](#zero-configuration-resolution)
    - [컨테이너를 언제 사용해야 할까?](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [컨텍스추얼 바인딩](#contextual-binding)
    - [원시 값 바인딩하기](#binding-primitives)
    - [타입 명시 가변 인자 바인딩](#binding-typed-variadics)
    - [태깅(Tagging)](#tagging)
    - [바인딩 확장하기](#extending-bindings)
- [해결(Resolving)](#resolving)
    - [make 메서드](#the-make-method)
    - [자동 주입](#automatic-injection)
- [메서드 호출 및 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개

Laravel 서비스 컨테이너는 클래스 의존성을 관리하고 의존성 주입을 수행할 수 있도록 해주는 강력한 도구입니다. 의존성 주입(Dependency Injection)이란 멋진 용어의 의미는, 클래스에 필요한 의존성을 생성자의 매개변수(혹은 경우에 따라 Setter 메서드)를 통해 **"주입"** 받는다는 뜻입니다.

간단한 예제를 살펴봅시다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Repositories\UserRepository;
use App\Models\User;

class UserController extends Controller
{
    /**
     * 유저 리포지토리 구현체.
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
     * 주어진 사용자의 프로필 표시.
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

이 예제에서 `UserController`는 데이터 소스에서 사용자를 조회해야 합니다. 따라서, 사용자 정보를 조회할 수 있는 서비스를 **주입**합니다. 여기서 우리의 `UserRepository`는 [Eloquent](/docs/{{version}}/eloquent)를 사용하여 데이터베이스에서 사용자 정보를 읽어오는 역할을 합니다. 하지만, 리포지토리를 주입받기 때문에, 언제든 다른 구현체로 쉽게 교체할 수 있습니다. 또한 애플리케이션 테스트 시 `UserRepository`의 모의(Mock) 혹은 더미 구현체를 쉽게 생성할 수 있습니다.

Laravel 서비스 컨테이너에 대한 깊은 이해는 강력하고 대규모 애플리케이션을 개발하기 위해 또는 Laravel 핵심에 기여하기 위해 꼭 필요합니다.

<a name="zero-configuration-resolution"></a>
### 무설정(Zero Configuration) 해석

클래스가 의존성이 없거나, 오직 다른 **구체 클래스**(인터페이스가 아닌 클래스)에만 의존한다면, 컨테이너에게 해당 클래스의 해석 방법을 따로 알려줄 필요가 없습니다. 예를 들어, 아래와 같은 코드를 `routes/web.php`에 둘 수 있습니다.

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

이 예시에서 애플리케이션의 `/` 라우트에 접근하면, 컨테이너는 `Service` 클래스를 자동으로 해석해서 라우트 핸들러에 주입해줍니다. 이것은 정말 획기적입니다. 이 기능을 통해 무거운 설정 파일 없이도, 의존성 주입의 장점을 누리며 개발할 수 있습니다.

다행히도, Laravel 애플리케이션을 개발할 때 작성하는 대부분의 클래스(예: [컨트롤러](/docs/{{version}}/controllers), [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등)는 컨테이너를 통해 의존성이 자동으로 주입됩니다. 추가적으로, [큐 작업](/docs/{{version}}/queues)의 `handle` 메서드에서도 타입 힌트로 의존성을 받을 수 있습니다. 자동 및 무설정 의존성 주입의 강력함을 경험하고 나면, 이를 사용하지 않고 개발하는 것이 불가능하게 느껴질 정도입니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 언제 사용해야 할까?

무설정 해석 기능 덕분에, 라우트, 컨트롤러, 이벤트 리스너 등 이곳저곳에서 타입 힌트만 작성하면 수동으로 컨테이너를 사용할 필요 없이 대부분의 의존성을 자동으로 주입받을 수 있습니다. 예를 들어, 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입 힌트만으로 손쉽게 사용할 수 있습니다. 실제로 코드를 작성하면서 컨테이너를 직접 다루지 않아도, 컨테이너가 내부적으로 이러한 의존성 주입을 관리하고 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

실제 현업에서도, 자동 의존성 주입 및 [파사드](/docs/{{version}}/facades)를 통해 컨테이너에 수동 바인딩이나 해석 없이도 Laravel 애플리케이션을 개발할 수 있습니다.  
**그렇다면 언제 수동으로 컨테이너와 상호작용해야 할까요?** 두 가지 경우가 대표적입니다.

첫째, 클래스가 특정 **인터페이스를 구현**하고, 그 인터페이스를 라우트나 클래스 생성자에 타입 힌트하고 싶을 때는 [해당 인터페이스의 해석 방법을 컨테이너에 명시](#binding-interfaces-to-implementations)해야 합니다.  
둘째, [Laravel 패키지](/docs/{{version}}/packages)를 직접 개발해 배포할 계획이 있다면, 패키지의 서비스를 컨테이너에 바인딩하게 됩니다.

<a name="binding"></a>
## 바인딩

<a name="binding-basics"></a>
### 바인딩 기본

<a name="simple-bindings"></a>
#### 단순 바인딩

서비스 컨테이너의 거의 모든 바인딩은 [서비스 프로바이더](/docs/{{version}}/providers) 안에서 등록됩니다. 따라서 아래의 예제들은 대부분 해당 문맥에서 컨테이너를 사용하는 방법을 보여줍니다.

서비스 프로바이더 내부에서는 항상 `$this->app` 속성을 통해 컨테이너에 접근할 수 있습니다. 클래스나 인터페이스 이름과, 인스턴스를 반환하는 클로저를 `bind` 메서드에 전달하여 바인딩을 등록할 수 있습니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$this->app->bind(Transistor::class, function ($app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

해결자(클로저)의 인자로 컨테이너 그 자체를 받을 수 있으며, 이를 활용해 객체를 생성할 때 필요한 하위 의존성도 컨테이너로부터 손쉽게 해석할 수 있습니다.

앞서 언급했듯, 주로 서비스 프로바이더 안에서 컨테이너와 상호작용합니다. 그러나 서비스 프로바이더 외부에서도 `App` [파사드](/docs/{{version}}/facades)를 통해 컨테이너를 사용할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function ($app) {
    // ...
});
```

> {tip} **인터페이스에 의존하지 않는 클래스는 컨테이너에 바인딩할 필요가 없습니다. 컨테이너는 리플렉션(Reflection)을 이용해 이러한 객체를 자동으로 해석할 수 있기 때문입니다.**

<a name="binding-a-singleton"></a>
#### 싱글턴 바인딩

`singleton` 메서드는 클래스나 인터페이스를 컨테이너에 단 한 번만 해석되는 싱글턴으로 바인딩합니다. 싱글턴 바인딩이 한 번 해석되면, 이후 동일한 요청에 대해 항상 같은 인스턴스를 반환합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$this->app->singleton(Transistor::class, function ($app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 스코프드 싱글턴 바인딩

`scoped` 메서드는 주어진 Laravel 요청 또는 작업(Job) 생명주기 내에서 한 번만 해석되는 인스턴스를 바인딩합니다. 이 메서드는 `singleton`과 비슷하지만, [Laravel Octane](/docs/{{version}}/octane) 워커가 새 요청을 처리하거나 [큐 워커](/docs/{{version}}/queues)가 새 작업을 처리할 때마다 인스턴스가 초기화(플러시)됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$this->app->scoped(Transistor::class, function ($app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
#### 인스턴스 바인딩

이미 생성된 객체 인스턴스를 `instance` 메서드를 사용해 컨테이너에 바인딩할 수도 있습니다. 이 인스턴스는 이후 요청에서도 계속 동일하게 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기

서비스 컨테이너의 가장 강력한 기능 중 하나는 인터페이스와 그 구현체를 바인딩하는 것입니다. 예를 들어, `EventPusher` 인터페이스와 `RedisEventPusher` 구현체가 있다고 가정해 봅시다. 이 구현체를 컨테이너에 아래와 같이 등록할 수 있습니다.

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이 구문은 컨테이너가 `EventPusher` 구현체가 필요한 클래스를 해석할 때 자동으로 `RedisEventPusher`를 주입하도록 지시합니다. 이제 컨테이너에서 해석되는 클래스의 생성자에서 `EventPusher` 인터페이스를 타입 힌트할 수 있습니다. 컨트롤러, 이벤트 리스너, 미들웨어 등은 모두 컨테이너를 통해 해석된다는 점을 기억하세요.

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
### 컨텍스추얼 바인딩

때로는 동일한 인터페이스를 사용하는 두 클래스가 각각 다른 구현체를 주입받아야 할 수도 있습니다. 예를 들어, 두 컨트롤러가 각기 다른 `Illuminate\Contracts\Filesystem\Filesystem` [계약](/docs/{{version}}/contracts) 구현체를 필요로 할 수 있습니다. Laravel은 이를 간단하고 명확하게 정의할 수 있는 유창한 인터페이스를 제공합니다.

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
### 원시 값 바인딩하기

클래스가 객체뿐만 아니라 정수와 같은 원시 값도 주입받아야 할 때가 있습니다. 컨텍스추얼 바인딩을 사용해 클래스가 필요로 하는 아무 값이나 간단히 주입할 수 있습니다.

```php
$this->app->when('App\Http\Controllers\UserController')
          ->needs('$variableName')
          ->give($value);
```

어떤 클래스가 [태그된](#tagging) 인스턴스 배열에 의존해야 할 때도 있습니다. `giveTagged` 메서드를 사용하면, 해당 태그를 가진 모든 컨테이너 바인딩을 배열로 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션의 설정 파일에서 값을 주입해야 한다면 `giveConfig` 메서드를 사용할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입 명시 가변 인자 바인딩

때로는 가변 인자(variadic) 생성자 매개변수를 통해 특정 타입의 객체 배열을 주입받는 클래스가 있을 수 있습니다.

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

컨텍스추얼 바인딩에서, `give` 메서드에 클로저를 전달해 의존하는 `Filter` 인스턴스를 배열로 반환할 수 있습니다.

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

간편하게, 클래스 이름 배열만 전달해도 컨테이너가 `Firewall`에 `Filter` 인스턴스가 필요할 때 자동으로 인스턴스를 생성해 전달합니다.

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

가변 인자에 특정 클래스 타입(`Report ...$reports`)을 타입 힌트하는 경우, `needs`와 `giveTagged`를 사용해 해당 태그의 모든 바인딩을 쉽게 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅(Tagging)

가끔, 특정 범주의 모든 바인딩 인스턴스를 해석해야 할 때가 있습니다. 예를 들어, 다양한 `Report` 인터페이스 구현체 배열을 받아 분석하는 "리포트 분석기"를 만든다고 가정해봅시다. `Report` 구현체들을 바인딩한 뒤, `tag` 메서드를 이용해 태그를 지정할 수 있습니다.

```php
$this->app->bind(CpuReport::class, function () {
    //
});

$this->app->bind(MemoryReport::class, function () {
    //
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

서비스들이 태그된 후에는, 컨테이너의 `tagged` 메서드를 이용해 모두 한 번에 해석할 수 있습니다.

```php
$this->app->bind(ReportAnalyzer::class, function ($app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장하기

`extend` 메서드는 이미 해석된 서비스를 수정할 수 있도록 해줍니다. 예를 들어, 서비스가 해석될 때 데코레이터 패턴 등을 적용하거나 추가 설정을 할 수 있습니다. `extend` 메서드는 단일 인자로 클로저를 받으며, 해당 클로저는 수정된 서비스를 반환해야 합니다. 클로저는 해석된 서비스와 컨테이너 인스턴스를 인자로 받습니다.

```php
$this->app->extend(Service::class, function ($service, $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해석(Resolving)

<a name="the-make-method"></a>
### `make` 메서드

`make` 메서드를 사용하면 컨테이너에서 원하는 클래스 인스턴스를 해석할 수 있습니다. 클래스나 인터페이스 이름을 인자로 전달하면 됩니다.

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스의 일부 의존성이 컨테이너로 해석되지 않을 경우, `makeWith` 메서드를 사용해 그 값을 연관 배열로 직접 전달할 수 있습니다. 예를 들어, `Transistor` 서비스의 생성자에 `$id` 인자가 필요한 경우 아래와 같이 사용할 수 있습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

서비스 프로바이더 외부에서, 즉 `$app` 변수에 접근할 수 없는 경우에도 `App` [파사드](/docs/{{version}}/facades)를 사용해 인스턴스를 해석할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);
```

컨테이너에서 해석되는 클래스의 생성자에서 `Illuminate\Container\Container` 자체를 주입받고 싶다면, 해당 클래스를 타입 힌트로 지정하면 됩니다.

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

또한 중요한 점으로, 컨테이너에서 해석되는 클래스(예: [컨트롤러](/docs/{{version}}/controllers), [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등)는 생성자에서 타입 힌트만 작성하면 의존성이 자동으로 주입됩니다. [큐 작업](/docs/{{version}}/queues)의 `handle` 메서드에서도 마찬가지입니다. 실제로, 대부분의 객체는 이런 방식으로 컨테이너가 자동으로 해석해야 합니다.

예를 들어, 컨트롤러 생성자에서 리포지토리를 타입 힌트로 작성하면, 해당 리포지토리가 자동으로 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * 유저 리포지토리 인스턴스.
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
     * 주어진 ID의 사용자 표시.
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
## 메서드 호출 및 주입

때로는 객체 인스턴스의 특정 메서드를 호출하면서, 해당 메서드의 의존성을 컨테이너가 자동으로 주입해주길 원할 수도 있습니다. 예를 들어, 아래와 같은 클래스가 있다고 가정합시다.

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

컨테이너를 통해 `generate` 메서드를 아래와 같이 호출할 수 있습니다.

```php
use App\UserReport;
use Illuminate\Support\Facades\App;

$report = App::call([new UserReport, 'generate']);
```

`call` 메서드는 어떤 PHP callable도 허용합니다. 또한, 컨테이너의 `call` 메서드는 클로저를 호출하며, 의존성을 자동으로 주입해 줄 수도 있습니다.

```php
use App\Repositories\UserRepository;
use Illuminate\Support\Facades\App;

$result = App::call(function (UserRepository $repository) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트

서비스 컨테이너는 객체가 해석될 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 사용해서 이 이벤트를 리스닝할 수 있습니다.

```php
use App\Services\Transistor;

$this->app->resolving(Transistor::class, function ($transistor, $app) {
    // 컨테이너가 "Transistor" 타입 객체를 해석할 때 호출됨...
});

$this->app->resolving(function ($object, $app) {
    // 컨테이너가 아무 객체나 해석할 때 호출됨...
});
```

이벤트 콜백에는 해석되는 객체가 전달되므로, 객체가 실제로 사용되기 전에 추가 프로퍼티를 설정하거나 후처리 작업을 할 수 있습니다.

<a name="psr-11"></a>
## PSR-11

Laravel의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서 PSR-11의 컨테이너 인터페이스를 타입 힌트로 사용할 수 있으며, Laravel 컨테이너 인스턴스를 얻을 수 있습니다.

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    //
});
```

전달한 식별자를 해석할 수 없다면 예외가 발생합니다. 해당 식별자가 한 번도 바인딩된 적이 없으면 `Psr\Container\NotFoundExceptionInterface` 타입의 예외가 던져집니다. 식별자가 바인딩되어 있지만 해석에 실패한 경우에는 `Psr\Container\ContainerExceptionInterface` 타입의 예외가 발생합니다.
