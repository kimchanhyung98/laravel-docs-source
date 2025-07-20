# 라라벨 페넌트 (Laravel Pennant)

- [소개](#introduction)
- [설치](#installation)
- [구성](#configuration)
- [기능 플래그 정의](#defining-features)
    - [클래스 기반 기능(Feature)](#class-based-features)
- [기능 플래그 확인](#checking-features)
    - [조건부 실행](#conditional-execution)
    - [`HasFeatures` 트레이트](#the-has-features-trait)
    - [Blade 디렉티브](#blade-directive)
    - [미들웨어](#middleware)
    - [기능 플래그 확인 가로채기](#intercepting-feature-checks)
    - [메모리 내 캐시](#in-memory-cache)
- [스코프(Scope)](#scope)
    - [스코프 지정하기](#specifying-the-scope)
    - [기본 스코프](#default-scope)
    - [Nullable 스코프](#nullable-scope)
    - [스코프 식별하기](#identifying-scope)
    - [스코프 직렬화](#serializing-scope)
- [리치 기능값(Rich Feature Values)](#rich-feature-values)
- [여러 기능 플래그 조회](#retrieving-multiple-features)
- [즉시 로드(Eager Loading)](#eager-loading)
- [값 업데이트](#updating-values)
    - [일괄 업데이트](#bulk-updates)
    - [기능 플래그 비우기(Purge)](#purging-features)
- [테스트](#testing)
- [커스텀 페넌트 드라이버 추가](#adding-custom-pennant-drivers)
    - [드라이버 구현하기](#implementing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
    - [기능 플래그 외부 정의](#defining-features-externally)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Pennant](https://github.com/laravel/pennant)는 불필요한 요소 없이 간단하고 가벼운 기능 플래그(Feature Flag) 패키지입니다. 기능 플래그를 사용하면 새로운 애플리케이션 기능을 점진적으로 롤아웃할 수 있고, 새로운 UI 디자인에 대해 A/B 테스트를 진행하거나, 트렁크 기반 개발 전략을 보완하는 등 다양한 목적으로 활용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 사용해 Pennant를 프로젝트에 설치합니다.

```shell
composer require laravel/pennant
```

다음으로, `vendor:publish` Artisan 명령어를 실행하여 Pennant의 설정 파일과 마이그레이션 파일을 배포해야 합니다.

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행합니다. Pennant에서 `database` 드라이버를 사용할 때 필요한 `features` 테이블이 생성됩니다.

```shell
php artisan migrate
```

<a name="configuration"></a>
## 구성

Pennant의 에셋을 배포한 후 설정 파일은 `config/pennant.php`에 위치하게 됩니다. 이 설정 파일에서는 Pennant가 기능 플래그 값을 저장할 때 사용할 기본 스토리지 방식을 지정할 수 있습니다.

Pennant는 `array` 드라이버를 통해 메모리 내 배열에 기능 플래그 값을 저장할 수 있도록 지원합니다. 또는 기본적으로 `database` 드라이버를 사용하는데, 이 경우 관계형 데이터베이스에 기능 플래그 값을 영구적으로 저장합니다.

<a name="defining-features"></a>
## 기능 플래그 정의

기능 플래그를 정의하려면, `Feature` 파사드에서 제공하는 `define` 메서드를 사용합니다. 이때, 해당 기능의 이름과 기능의 초깃값을 결정하는 클로저를 인자로 전달해야 합니다.

보통, 서비스 프로바이더 내에서 `Feature` 파사드를 이용해 기능 플래그를 정의합니다. 이 클로저는 기능 플래그를 확인할 스코프(scope)를 매개변수로 받으며, 대부분의 경우 스코프는 현재 인증된 사용자입니다. 다음은 애플리케이션 사용자에게 새로운 API를 점진적으로 배포하는 기능 플래그를 정의한 예시입니다.

```php
<?php

namespace App\Providers;

use App\Models\User;
use Illuminate\Support\Lottery;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::define('new-api', fn (User $user) => match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        });
    }
}
```

위 예시에서 기능 플래그는 다음 규칙을 따릅니다.

- 모든 내부 팀원은 반드시 새로운 API를 사용하게 됩니다.
- 트래픽이 많은 고객은 새로운 API를 사용하지 않도록 합니다.
- 그 밖의 나머지 사용자에게는 1/100 확률로 무작위로 기능이 활성화됩니다.

주어진 사용자에 대해 `new-api` 기능이 처음 확인될 때, 클로저의 반환값이 스토리지 드라이버에 저장됩니다. 이후 같은 사용자에 대해 다시 기능을 확인하면, 이전에 저장된 값이 반환되고 클로저는 다시 실행되지 않습니다.

편의상, 로터리(lottery)만 반환하는 기능 플래그 정의라면 클로저를 생략할 수 있습니다.

```
Feature::define('site-redesign', Lottery::odds(1, 1000));
```

<a name="class-based-features"></a>
### 클래스 기반 기능(Feature)

Pennant는 클래스 기반의 기능 플래그도 정의할 수 있습니다. 클로저 방식과는 달리 클래스 기반 기능은 서비스 프로바이더에 별도 등록할 필요가 없습니다. 클래스 기반 기능을 생성하려면 `pennant:feature` Artisan 명령어를 실행하면 됩니다. 기본적으로 생성되는 기능 클래스는 애플리케이션의 `app/Features` 디렉터리에 저장됩니다.

```shell
php artisan pennant:feature NewApi
```

기능 클래스를 작성할 때는, 주어진 스코프에 대해 기능의 초깃값을 결정하는 `resolve` 메서드만 정의하면 됩니다. 스코프는 보통 현재 인증된 사용자가 전달됩니다.

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * Resolve the feature's initial value.
     */
    public function resolve(User $user): mixed
    {
        return match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        };
    }
}
```

클래스 기반 기능의 인스턴스를 수동으로 생성하고 싶을 때는, `Feature` 파사드의 `instance` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]
> 기능(Feature) 클래스는 [서비스 컨테이너](/docs/12.x/container)를 통해 해결되므로, 필요한 경우 생성자에 의존성 주입이 가능합니다.

#### 저장되는 기능 이름 커스터마이징

기본적으로 Pennant는 기능 클래스의 전체 네임스페이스를 포함한 클래스 이름을 저장합니다. 저장되는 기능 이름을 애플리케이션의 내부 구조와 분리하고 싶다면, 기능 클래스에 `$name` 속성을 지정할 수 있습니다. 이 속성의 값은 클래스 이름 대신 저장에 사용됩니다.

```php
<?php

namespace App\Features;

class NewApi
{
    /**
     * The stored name of the feature.
     *
     * @var string
     */
    public $name = 'new-api';

    // ...
}
```

<a name="checking-features"></a>
## 기능 플래그 확인

특정 기능 플래그가 활성 상태인지 확인하려면, `Feature` 파사드의 `active` 메서드를 사용합니다. 기본적으로는 현재 인증된 사용자에 대해 기능 플래그가 확인됩니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        return Feature::active('new-api')
            ? $this->resolveNewApiResponse($request)
            : $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```

기본적으로는 현재 인증된 사용자를 기준으로 기능이 확인되지만, 원하는 경우 다른 사용자 또는 임의의 [스코프](#scope)에 대해 기능을 확인할 수도 있습니다. 이를 위해 `Feature` 파사드의 `for` 메서드를 사용하면 됩니다.

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

Pennant는 기능이 활성 또는 비활성 상태인지 확인할 때 편리하게 사용할 수 있는 여러 메서드를 추가로 제공합니다.

```php
// 주어진 모든 기능이 활성 상태인지 확인
Feature::allAreActive(['new-api', 'site-redesign']);

// 주어진 기능 중 하나라도 활성 상태인지 확인
Feature::someAreActive(['new-api', 'site-redesign']);

// 특정 기능이 비활성 상태인지 확인
Feature::inactive('new-api');

// 주어진 모든 기능이 비활성 상태인지 확인
Feature::allAreInactive(['new-api', 'site-redesign']);

// 주어진 기능 중 하나라도 비활성 상태인지 확인
Feature::someAreInactive(['new-api', 'site-redesign']);
```

> [!NOTE]
> 아티즌 명령어나 큐에 등록한 작업 등 HTTP 컨텍스트 외부에서 Pennant를 사용할 때는, 일반적으로 [기능의 스코프를 명시적으로 지정](#specifying-the-scope)해야 합니다. 또는 인증된 HTTP 컨텍스트와 인증되지 않은 컨텍스트를 모두 고려한 [기본 스코프](#default-scope)를 정의할 수도 있습니다.

<a name="checking-class-based-features"></a>
#### 클래스 기반 기능 플래그 확인

클래스 기반 기능 플래그를 확인할 때는 클래스 이름을 넘겨주면 됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Features\NewApi;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        return Feature::active(NewApi::class)
            ? $this->resolveNewApiResponse($request)
            : $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```

<a name="conditional-execution"></a>
### 조건부 실행

`when` 메서드를 사용하면, 특정 기능 플래그가 활성 상태일 때 지정한 클로저를, 비활성 상태일 때는 두 번째 클로저를 각각 실행할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use App\Features\NewApi;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        return Feature::when(NewApi::class,
            fn () => $this->resolveNewApiResponse($request),
            fn () => $this->resolveLegacyApiResponse($request),
        );
    }

    // ...
}
```

`unless` 메서드는 `when` 메서드의 반대로, 기능이 비활성 상태일 때 첫 번째 클로저를, 활성 상태일 때 두 번째 클로저를 실행합니다.

```php
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
### `HasFeatures` 트레이트

Pennant의 `HasFeatures` 트레이트(trait)를 애플리케이션의 `User` 모델(또는 기능 플래그를 가질 수 있는 다른 모델)에 추가하면, 모델에서 직접 기능 플래그를 확인하는 편리한 방식이 제공됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Pennant\Concerns\HasFeatures;

class User extends Authenticatable
{
    use HasFeatures;

    // ...
}
```

트레이트를 추가한 후에는 `features` 메서드를 호출해 기능을 손쉽게 확인할 수 있습니다.

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

물론, `features` 메서드를 통해 다양한 메서드로 기능 플래그와 상호작용할 수 있습니다.

```php
// 값 조회
$value = $user->features()->value('purchase-button')
$values = $user->features()->values(['new-api', 'purchase-button']);

// 상태 확인
$user->features()->active('new-api');
$user->features()->allAreActive(['new-api', 'server-api']);
$user->features()->someAreActive(['new-api', 'server-api']);

$user->features()->inactive('new-api');
$user->features()->allAreInactive(['new-api', 'server-api']);
$user->features()->someAreInactive(['new-api', 'server-api']);

// 조건부 실행
$user->features()->when('new-api',
    fn () => /* ... */,
    fn () => /* ... */,
);

$user->features()->unless('new-api',
    fn () => /* ... */,
    fn () => /* ... */,
);
```

<a name="blade-directive"></a>
### Blade 디렉티브

Blade에서 기능 플래그를 편리하게 확인할 수 있도록, Pennant는 `@feature`와 `@featureany` 디렉티브를 제공합니다.

```blade
@feature('site-redesign')
    <!-- 'site-redesign' 기능이 활성화되어 있음 -->
@else
    <!-- 'site-redesign' 기능이 비활성화되어 있음 -->
@endfeature

@featureany(['site-redesign', 'beta'])
    <!-- 'site-redesign' 또는 `beta` 기능이 활성화되어 있음 -->
@endfeatureany
```

<a name="middleware"></a>
### 미들웨어

Pennant에는 현재 인증된 사용자가 특정 기능 플래그에 접근 권한이 있는지 라우트 실행 전 검증할 수 있는 [미들웨어](/docs/12.x/middleware)도 포함되어 있습니다. 해당 미들웨어를 라우트에 할당할 때, 접근에 필요한 기능 플래그 이름을 지정할 수 있습니다. 지정된 기능 중 하나라도 현재 사용자에 대해 비활성화되어 있다면, 라우트는 `400 Bad Request` HTTP 응답을 반환합니다. 복수의 기능 플래그를 static `using` 메서드로 넘길 수 있습니다.

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### 미들웨어 응답 커스터마이징

특정 기능 중 하나라도 비활성일 때 미들웨어가 반환하는 응답을 커스터마이징하고 싶다면, `EnsureFeaturesAreActive` 미들웨어의 `whenInactive` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 호출합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    EnsureFeaturesAreActive::whenInactive(
        function (Request $request, array $features) {
            return new Response(status: 403);
        }
    );

    // ...
}
```

<a name="intercepting-feature-checks"></a>
### 기능 플래그 확인 가로채기

기능 플래그의 저장된 값을 불러오기 전에, 우선 메모리 내에서 조건을 점검해야 할 때가 있습니다. 예를 들어, 새로운 API를 기능 플래그로 감싸놓고 개발 중인데, 문제가 발생했을 때 저장된 값은 그대로 두면서 내부 팀원을 제외한 모든 사용자에 대해 해당 기능을 비활성화하고자 할 수 있습니다. 이렇게 하면 버그를 빠르게 수정한 뒤, 이전에 기능을 사용하던 사용자에게도 기능을 다시 활성화할 수 있습니다.

이런 요구는 [클래스 기반 기능](#class-based-features)의 `before` 메서드로 구현할 수 있습니다. 이 메서드가 있으면, 항상 메모리 내에서 먼저 실행되고 저장된 값을 불러오기 전에 체크할 수 있습니다. 메서드에서 `null` 이외의 값을 반환하면, 해당 값을 현재 요청 동안 기능의 실제 값으로 사용하게 됩니다.

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * Run an always-in-memory check before the stored value is retrieved.
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }
    }

    /**
     * Resolve the feature's initial value.
     */
    public function resolve(User $user): mixed
    {
        return match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        };
    }
}
```

이 기능을 활용하여, 이전에는 기능 플래그 뒤에 있던 기능을 특정 시점에 전체 롤아웃(전면 배포)하는 스케줄링에도 사용할 수 있습니다.

```php
<?php

namespace App\Features;

use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Config;

class NewApi
{
    /**
     * Run an always-in-memory check before the stored value is retrieved.
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }

        if (Carbon::parse(Config::get('features.new-api.rollout-date'))->isPast()) {
            return true;
        }
    }

    // ...
}
```

<a name="in-memory-cache"></a>
### 메모리 내 캐시

기능 플래그를 확인할 때, Pennant는 그 결과를 메모리 내에 캐싱합니다. `database` 드라이버를 사용하는 경우, 하나의 요청 안에서 동일한 기능 플래그를 여러 번 확인해도 추가적인 데이터베이스 쿼리가 발생하지 않습니다. 이것은 하나의 요청 동안 기능 플래그의 결과가 일관적으로 유지된다는 점에서도 유용합니다.

만약 메모리 캐시를 수동으로 비우고 싶다면, `Feature` 파사드의 `flushCache` 메서드를 사용할 수 있습니다.

```php
Feature::flushCache();
```

<a name="scope"></a>
## 스코프(Scope)

<a name="specifying-the-scope"></a>
### 스코프 지정하기

앞서 설명했듯이, 기능 플래그는 보통 현재 인증된 사용자에 대해 확인합니다. 하지만 모든 상황에 이 방식이 적합하지 않을 수 있으므로, 원하는 스코프를 직접 지정하여 기능을 확인할 수도 있습니다. 이를 위해 `Feature` 파사드의 `for` 메서드를 사용합니다.

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

물론, 기능 플래그의 스코프는 "User"에 한정되지 않습니다. 예를 들어, 개별 사용자 대신 전체 팀을 대상으로 새 결제 기능을 롤아웃할 수도 있습니다. 오래된 팀에는 점진적으로, 새로 만들어진 팀에는 더 빠르게 기능을 배포하고 싶다면, 다음과 같이 기능 플래그 정의 클로저를 작성할 수 있습니다.

```php
use App\Models\Team;
use Illuminate\Support\Carbon;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

Feature::define('billing-v2', function (Team $team) {
    if ($team->created_at->isAfter(new Carbon('1st Jan, 2023'))) {
        return true;
    }

    if ($team->created_at->isAfter(new Carbon('1st Jan, 2019'))) {
        return Lottery::odds(1 / 100);
    }

    return Lottery::odds(1 / 1000);
});
```

이 클로저는 `User` 대신 `Team` 모델 인스턴스를 매개변수로 받고 있습니다. 사용자가 속한 팀에 대해 해당 기능이 활성화되어 있는지 확인하려면, `Feature` 파사드의 `for` 메서드에 팀을 전달하면 됩니다.

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### 기본 스코프

Pennant가 기능 플래그를 확인할 때 사용하는 기본 스코프를 커스터마이징할 수도 있습니다. 예를 들어, 모든 기능에 대해 현재 인증된 사용자가 아닌 해당 사용자의 팀을 기본 스코프로 삼고 싶을 때, 매번 `Feature::for($user->team)`를 호출하지 않아도 되게끔 기본 스코프를 설정할 수 있습니다. 보통 서비스 프로바이더에서 아래와 같이 설정합니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::resolveScopeUsing(fn ($driver) => Auth::user()?->team);

        // ...
    }
}
```

`for` 메서드로 스코프를 명시적으로 지정하지 않는 경우 이제 기능 플래그는 현재 인증된 사용자의 팀을 기본적으로 대상으로 삼게 됩니다.

```php
Feature::active('billing-v2');

// 위 코드는 아래 코드와 동일하게 동작합니다.

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### Nullable 스코프

기능 플래그를 확인할 때 전달하는 스코프가 `null`이고, 기능 플래그 정의에서 nullable 타입이나 union 타입으로 `null` 처리가 되어 있지 않다면, Pennant는 자동으로 해당 기능의 결과 값을 `false`로 반환합니다.

따라서 기능 플래그의 스코프가 `null`일 수도 있고, 그럴 때에도 값 해석기(resolver)가 정상 동작하게 하고 싶다면, 기능 플래그 정의에서 이를 반영해야 합니다. `null` 스코프는 아티즌 명령어, 큐 작업, 인증되지 않은 라우트 등에서 기능을 확인할 때 자주 발생합니다. 이때는 인증된 사용자가 없는 경우가 대부분이어서 기본 스코프가 `null`이 됩니다.

항상 [기능 스코프를 명시적으로 지정](#specifying-the-scope)하지 않는다면, 스코프의 타입에 nullable 처리를 하고, `null`일 때의 로직을 기능 플래그 정의에 포함해야 합니다.

```php
use App\Models\User;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

Feature::define('new-api', fn (User|null $user) => match (true) {
    $user === null => true,
    $user->isInternalTeamMember() => true,
    $user->isHighTrafficCustomer() => false,
    default => Lottery::odds(1 / 100),
});
```

<a name="identifying-scope"></a>
### 스코프 식별하기

Pennant에 내장된 `array` 및 `database` 저장 드라이버는 모든 PHP 데이터 타입과 Eloquent 모델에 대한 스코프 식별자를 올바르게 저장할 수 있습니다. 하지만 서드 파티 Pennant 드라이버를 사용할 경우, 해당 드라이버가 Eloquent 모델이나 애플리케이션의 특정 타입을 식별자 형태로 저장하는 법을 모를 수도 있습니다.

이런 상황에 대비해, 애플리케이션에서 Pennant 스코프로 사용하는 객체에 `FeatureScopeable` 인터페이스를 구현하면 스코프 값을 직접 포맷해서 저장할 수 있습니다.

예를 들어, 하나의 애플리케이션에서 기본 `database` 드라이버와 서드 파티 "Flag Rocket" 드라이버를 동시에 사용하는 상황을 가정해봅시다. "Flag Rocket" 드라이버는 Eloquent 모델을 저장할 수 없고, 대신 `FlagRocketUser` 인스턴스를 필요로 합니다. 이럴 때 `FeatureScopeable` 인터페이스의 `toFeatureIdentifier` 메서드를 구현해서, 각 드라이버에 알맞은 스코프 값을 반환할 수 있습니다.

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * Cast the object to a feature scope identifier for the given driver.
     */
    public function toFeatureIdentifier(string $driver): mixed
    {
        return match($driver) {
            'database' => $this,
            'flag-rocket' => FlagRocketUser::fromId($this->flag_rocket_id),
        };
    }
}
```

<a name="serializing-scope"></a>
### 스코프 직렬화

기본적으로 Pennant는 Eloquent 모델과 연결된 기능 플래그를 저장할 때 전체 네임스페이스를 포함한 클래스 이름을 사용합니다. 이미 [Eloquent morph map](/docs/12.x/eloquent-relationships#custom-polymorphic-types)을 사용하고 있다면, Pennant 역시 morph map을 활용해 저장되는 기능 플래그 이름을 애플리케이션의 구조와 분리시킬 수 있습니다.

이를 위해 서비스 프로바이더에서 morph map을 정의한 이후, `Feature` 파사드의 `useMorphMap` 메서드를 호출하면 됩니다.

```php
use Illuminate\Database\Eloquent\Relations\Relation;
use Laravel\Pennant\Feature;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);

Feature::useMorphMap();
```

<a name="rich-feature-values"></a>
## 리치 기능값(Rich Feature Values)

지금까지 기능 플래그는 주로 "활성(true)" 또는 "비활성(false)"처럼 이진 상태만을 예시로 들었지만, Pennant는 풍부한 값을 저장할 수도 있습니다.

예를 들어, "구매하기" 버튼의 색상을 세 가지로 테스트하는 경우를 생각해봅시다. 기능 정의에서 `true` 또는 `false`를 반환하는 대신, 문자열을 반환할 수 있습니다.

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

`purchase-button` 기능의 값을 얻으려면, `value` 메서드를 사용합니다.

```php
$color = Feature::value('purchase-button');
```

Pennant의 Blade 디렉티브를 사용하면, 기능의 현재 값에 따라 콘텐츠를 조건부 렌더링할 수도 있습니다.

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire' 사용 중 -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green' 사용 중 -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange' 사용 중 -->
@endfeature
```

> [!NOTE]
> 리치 값(rich value)을 사용할 때, `false`가 아닌 값이 할당되어 있으면 해당 기능 플래그는 "활성"으로 간주된다는 점을 알아두어야 합니다.

[조건부 `when`](#conditional-execution) 메서드를 호출할 때, 기능 플래그의 리치 값이 첫 번째 클로저에 인자로 전달됩니다.

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

마찬가지로, 조건부 `unless` 메서드를 사용할 때는 두 번째 클로저에 기능의 리치 값이 인자로 전달됩니다.

```php
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>

## 여러 기능값 가져오기

`values` 메서드를 사용하면 지정한 스코프(scope)에 대해 여러 기능(feature)의 값을 조회할 수 있습니다.

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

또는, `all` 메서드를 사용하여 지정한 스코프에 정의된 모든 기능의 값을 가져올 수도 있습니다.

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

하지만, 클래스 기반 기능(class-based feature)은 동적으로 등록되므로 Pennant에서 명시적으로 확인(check)하기 전까지는 존재를 알지 못합니다. 즉, 현재 요청 중에 한 번도 확인되지 않은 클래스 기반 기능은 `all` 메서드의 반환 결과에 나타나지 않을 수 있습니다.

만약 `all` 메서드로 항상 기능 클래스들이 포함되길 원한다면, Pennant의 기능 탐색(feature discovery) 기능을 이용할 수 있습니다. 우선, 애플리케이션의 서비스 프로바이더 중 하나에서 `discover` 메서드를 호출하세요.

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::discover();

        // ...
    }
}
```

`discover` 메서드는 애플리케이션의 `app/Features` 디렉터리에 있는 모든 기능 클래스를 등록합니다. 이제 `all` 메서드는 요청 중 이미 확인되었는지 여부와 상관없이 이 클래스들도 결과에 포함시킵니다.

```php
Feature::all();

// [
//     'App\Features\NewApi' => true,
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

<a name="eager-loading"></a>
## 이른 로딩(Eager Loading)

Pennant는 단일 요청 동안에 해결된 모든 기능값을 메모리 캐시에 보관하지만, 여전히 성능 문제가 발생할 수 있습니다. 이를 완화하기 위해 Pennant는 기능값을 이른 로딩(eager loading)할 수 있는 메서드를 제공합니다.

예를 들어, 반복문 안에서 기능 활성화 여부를 확인(check)한다고 가정해 봅시다.

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

데이터베이스 드라이버를 사용하는 경우, 위 코드는 반복되는 사용자마다 데이터베이스 쿼리가 실행되어 수백 번의 쿼리 호출이 발생할 수 있습니다. 그러나 Pennant의 `load` 메서드를 사용하면 사용자 컬렉션이나 여러 스코프에 대한 기능값을 미리 가져와, 잠재적인 성능 병목을 제거할 수 있습니다.

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

이미 로드되지 않은 기능값만 이른 로딩하고 싶다면 `loadMissing` 메서드를 활용할 수 있습니다.

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

모든 정의된 기능값을 한 번에 로드하려면 `loadAll` 메서드를 사용합니다.

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
## 값 업데이트하기

기능값이 처음으로 resolve(해결, 조회)될 때, Pennant의 드라이버는 해당 값을 저장소에 기록합니다. 이는 여러 요청에서 일관된 사용자 경험을 보장하기 위해 종종 필요한 동작입니다. 그러나 경우에 따라, 저장된 기능값을 수동으로 갱신해야 할 수도 있습니다.

이럴 때는, `activate`와 `deactivate` 메서드를 사용해서 "켜기" 또는 "끄기" 토글이 가능합니다.

```php
use Laravel\Pennant\Feature;

// 기본 스코프에서 기능 활성화...
Feature::activate('new-api');

// 특정 스코프에 대해 기능 비활성화...
Feature::for($user->team)->deactivate('billing-v2');
```

또한, `activate` 메서드에 두 번째 인자를 전달하면 기능에 대한 다양한(리치) 값을 직접 지정할 수도 있습니다.

```php
Feature::activate('purchase-button', 'seafoam-green');
```

Pennant에 저장된 기능값을 잊게(삭제) 하고 싶다면, `forget` 메서드를 호출하세요. 기능을 다시 확인하면, Pennant는 기능 정의에서 새 값을 resolve하게 됩니다.

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### 다수의 값 일괄 업데이트

여러 저장된 기능값을 한 번에 일괄 업데이트하려면 `activateForEveryone`과 `deactivateForEveryone` 메서드를 사용할 수 있습니다.

예를 들어 `new-api` 기능이 충분히 안정적이고, 결제 흐름에 최적인 `'purchase-button'` 색상을 결정했다면, 모든 사용자에 대해 저장된 값을 업데이트할 수 있습니다.

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

또는 모든 사용자에 대해 해당 기능을 비활성화할 수도 있습니다.

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> 이 동작은 Pennant의 스토리지 드라이버에 저장된 기능값만을 갱신합니다. 애플리케이션의 기능 정의도 함께 업데이트해야 함을 잊지 마세요.

<a name="purging-features"></a>
### 기능 값 전체 삭제(Purging Features)

경우에 따라 저장소에서 기능 전체를 제거(purge)하는 것이 유용할 때가 있습니다. 예를 들어, 기능을 삭제했거나, 기능 정의를 변경하여 모든 사용자에게 새로운 정의를 반영하고자 할 때 전체 데이터 삭제가 필요할 수 있습니다.

`purge` 메서드로 기능에 대해 저장된 모든 값을 삭제할 수 있습니다.

```php
// 단일 기능 전체 삭제
Feature::purge('new-api');

// 여러 기능 전체 삭제
Feature::purge(['new-api', 'purchase-button']);
```

저장소의 _모든_ 기능을 한 번에 제거하고 싶다면 인자 없이 `purge` 메서드를 호출하세요.

```php
Feature::purge();
```

애플리케이션의 배포 파이프라인 등에서 기능 값 삭제를 자동화할 수 있도록, Pennant에는 관련 Artian 명령어 `pennant:purge`가 포함되어 있습니다. 이 명령어로 지정한 기능을 저장소에서 삭제할 수 있습니다.

```shell
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

주어진 기능 목록을 제외한 모든 기능을 삭제하는 것도 가능합니다. 예를 들어, "new-api"와 "purchase-button" 기능값만은 남겨두고 나머지 기능을 모두 purge하고자 한다면, `--except` 옵션에 해당 기능명을 넘겨주면 됩니다.

```shell
php artisan pennant:purge --except=new-api --except=purchase-button
```

편의상 `pennant:purge` 명령은 `--except-registered` 플래그도 제공합니다. 이 옵션은 서비스 프로바이더에 명시적으로 등록된 기능을 제외한 나머지 기능만 purge하도록 지정합니다.

```shell
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## 테스트

기능 플래그를 사용하는 코드를 테스트할 때, 가장 쉬운 방법은 테스트 내에서 해당 기능의 반환값을 원하는 대로 재정의하는 것입니다. 예를 들어, 아래와 같이 서비스 프로바이더에서 기능을 정의했다고 가정해보겠습니다.

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

테스트 코드에서는 테스트의 시작 부분에서 해당 기능을 원하는 값으로 재정의할 수 있습니다. 아래 테스트는 설령 서비스 프로바이더에 여전히 `Arr::random()`이 사용되고 있더라도 항상 성공하게 됩니다.

```php tab=Pest
use Laravel\Pennant\Feature;

test('it can control feature values', function () {
    Feature::define('purchase-button', 'seafoam-green');

    expect(Feature::value('purchase-button'))->toBe('seafoam-green');
});
```

```php tab=PHPUnit
use Laravel\Pennant\Feature;

public function test_it_can_control_feature_values()
{
    Feature::define('purchase-button', 'seafoam-green');

    $this->assertSame('seafoam-green', Feature::value('purchase-button'));
}
```

클래스 기반 기능에 대해서도 똑같은 방법을 사용할 수 있습니다.

```php tab=Pest
use Laravel\Pennant\Feature;

test('it can control feature values', function () {
    Feature::define(NewApi::class, true);

    expect(Feature::value(NewApi::class))->toBeTrue();
});
```

```php tab=PHPUnit
use App\Features\NewApi;
use Laravel\Pennant\Feature;

public function test_it_can_control_feature_values()
{
    Feature::define(NewApi::class, true);

    $this->assertTrue(Feature::value(NewApi::class));
}
```

기능이 `Lottery` 인스턴스를 반환하는 경우, 추가적인 [테스트 헬퍼](/docs/12.x/helpers#testing-lotteries)가 준비되어 있습니다.

<a name="store-configuration"></a>
#### 저장소(Store) 환경설정

테스트 환경에서 Pennant가 사용할 저장소는 애플리케이션의 `phpunit.xml` 파일에서 `PENNANT_STORE` 환경변수로 지정할 수 있습니다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit colors="true">
    <!-- ... -->
    <php>
        <env name="PENNANT_STORE" value="array"/>
        <!-- ... -->
    </php>
</phpunit>
```

<a name="adding-custom-pennant-drivers"></a>
## 커스텀 Pennant 드라이버 추가하기

<a name="implementing-the-driver"></a>
#### 드라이버 구현

Pennant에 포함된 기존 저장소 드라이버가 애플리케이션의 요구사항에 맞지 않는다면, 직접 저장소 드라이버를 작성할 수 있습니다. 커스텀 드라이버는 `Laravel\Pennant\Contracts\Driver` 인터페이스를 구현해야 합니다.

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;

class RedisFeatureDriver implements Driver
{
    public function define(string $feature, callable $resolver): void {}
    public function defined(): array {}
    public function getAll(array $features): array {}
    public function get(string $feature, mixed $scope): mixed {}
    public function set(string $feature, mixed $scope, mixed $value): void {}
    public function setForAllScopes(string $feature, mixed $value): void {}
    public function delete(string $feature, mixed $scope): void {}
    public function purge(array|null $features): void {}
}
```

이제 각 메서드를 Redis 연결을 사용하여 직접 구현하면 됩니다. 구체적인 예시는 [Pennant 소스코드의 `Laravel\Pennant\Drivers\DatabaseDriver`](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)를 참고하세요.

> [!NOTE]
> 라라벨은 익스텐션(확장 기능) 구현을 위한 디렉터리를 직접 제공하지는 않습니다. 원하는 위치에 파일을 배치해도 무방합니다. 여기서는 예시로 `Extensions` 디렉터리에 `RedisFeatureDriver`를 추가했습니다.

<a name="registering-the-driver"></a>
#### 드라이버 등록

드라이버 구현이 끝나면, 이제 라라벨에 해당 드라이버를 등록해야 합니다. Pennant에 드라이버를 추가하려면, `Feature` 파사드의 `extend` 메서드를 사용하세요. 이는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) 중 한 곳에서 `boot` 메서드 내에 호출해야 합니다.

```php
<?php

namespace App\Providers;

use App\Extensions\RedisFeatureDriver;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::extend('redis', function (Application $app) {
            return new RedisFeatureDriver($app->make('redis'), $app->make('events'), []);
        });
    }
}
```

드라이버 등록이 완료되면, 애플리케이션의 `config/pennant.php` 설정 파일에서 `redis` 드라이버를 선택하여 사용할 수 있습니다.

```php
'stores' => [

    'redis' => [
        'driver' => 'redis',
        'connection' => null,
    ],

    // ...

],
```

<a name="defining-features-externally"></a>
### 외부에서 기능 정의하기

만약 커스텀 드라이버가 외부의 서드파티 기능 플래그 플랫폼을 래핑하는 용도라면, Pennant의 `Feature::define` 메서드 대신 해당 플랫폼에서 직접 기능을 정의할 것입니다. 이 경우, 커스텀 드라이버는 `Laravel\Pennant\Contracts\DefinesFeaturesExternally` 인터페이스도 추가로 구현해야 합니다.

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;
use Laravel\Pennant\Contracts\DefinesFeaturesExternally;

class FeatureFlagServiceDriver implements Driver, DefinesFeaturesExternally
{
    /**
     * Get the features defined for the given scope.
     */
    public function definedFeaturesForScope(mixed $scope): array {}

    /* ... */
}
```

`definedFeaturesForScope` 메서드는 전달받은 스코프에 대해 정의된 기능명 목록을 반환해야 합니다.

<a name="events"></a>
## 이벤트

Pennant는 기능 플래그를 트래킹할 때 유용하게 활용할 수 있는 다양한 이벤트를 디스패치합니다.

### `Laravel\Pennant\Events\FeatureRetrieved`

이벤트는 [기능 확인](#checking-features)이 이뤄질 때마다 발생합니다. 이 이벤트는 기능 플래그의 사용 현황 메트릭을 구축·분석하는 데 유용합니다.

### `Laravel\Pennant\Events\FeatureResolved`

이벤트는 특정 스코프에 대해 기능값이 처음 resolve될 때 발생합니다.

### `Laravel\Pennant\Events\UnknownFeatureResolved`

이벤트는 지정된 스코프에서 미리 정의되지 않은 기능을 처음 resolve할 때 발생합니다. 만약 어떤 기능 플래그를 제거하려고 했지만, 애플리케이션 일부에 해당 기능에 대한 참조가 남아 있다면 이 이벤트로 감지할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Log;
use Laravel\Pennant\Events\UnknownFeatureResolved;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Event::listen(function (UnknownFeatureResolved $event) {
            Log::error("Resolving unknown feature [{$event->feature}].");
        });
    }
}
```

### `Laravel\Pennant\Events\DynamicallyRegisteringFeatureClass`

이벤트는 [클래스 기반 기능](#class-based-features)이 요청 중에 처음으로 동적으로 확인될 때 발생합니다.

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

이 이벤트는 [null을 지원하지 않는](#nullable-scope) 기능 정의에 `null` 스코프가 전달될 때 발생합니다.

이 상황은 안정적으로 처리되어 기능은 단순히 `false`를 반환합니다. 하지만, 해당 기능의 기본 동작을 선택적으로 거부하고 싶다면, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 해당 이벤트 리스너를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\Log;
use Laravel\Pennant\Events\UnexpectedNullScopeEncountered;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(UnexpectedNullScopeEncountered::class, fn () => abort(500));
}
```

### `Laravel\Pennant\Events\FeatureUpdated`

이벤트는 일반적으로 `activate` 또는 `deactivate`를 호출해서 기능 값을 갱신할 때 발생합니다.

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

이벤트는 `activateForEveryone` 혹은 `deactivateForEveryone`을 호출해 기능 값을 전체 스코프에 반영할 때 발생합니다.

### `Laravel\Pennant\Events\FeatureDeleted`

이벤트는 일반적으로 `forget`을 통해 특정 스코프에서 기능을 삭제할 때 발생합니다.

### `Laravel\Pennant\Events\FeaturesPurged`

이벤트는 여러 기능을 purge(전체 삭제)할 때 발생합니다.

### `Laravel\Pennant\Events\AllFeaturesPurged`

이벤트는 모든 기능을 한 번에 purge할 때 발생합니다.