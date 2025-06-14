# 라라벨 페넌트 (Laravel Pennant)

- [소개](#introduction)
- [설치](#installation)
- [구성](#configuration)
- [기능 정의](#defining-features)
    - [클래스 기반 기능](#class-based-features)
- [기능 확인](#checking-features)
    - [조건부 실행](#conditional-execution)
    - [`HasFeatures` 트레이트](#the-has-features-trait)
    - [Blade 디렉티브](#blade-directive)
    - [미들웨어](#middleware)
    - [기능 확인 가로채기](#intercepting-feature-checks)
    - [인메모리 캐시](#in-memory-cache)
- [스코프](#scope)
    - [스코프 지정](#specifying-the-scope)
    - [기본 스코프](#default-scope)
    - [Nullable 스코프](#nullable-scope)
    - [스코프 식별](#identifying-scope)
    - [스코프 직렬화](#serializing-scope)
- [Rich Feature 값](#rich-feature-values)
- [여러 기능 조회](#retrieving-multiple-features)
- [사전 로딩](#eager-loading)
- [값 업데이트](#updating-values)
    - [대량 업데이트](#bulk-updates)
    - [기능 삭제](#purging-features)
- [테스트](#testing)
- [커스텀 페넌트 드라이버 추가](#adding-custom-pennant-drivers)
    - [드라이버 구현](#implementing-the-driver)
    - [드라이버 등록](#registering-the-driver)
    - [외부에서 기능 정의](#defining-features-externally)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Pennant](https://github.com/laravel/pennant)는 불필요한 요소가 없는, 간단하고 가벼운 기능 플래그(Feature Flag) 패키지입니다. 기능 플래그를 통해 새로운 애플리케이션 기능을 점진적으로 안정적으로 배포하거나, 새로운 UI 디자인의 A/B 테스트, trunk 기반 개발 전략 보완 등 다양한 목적에 활용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 관리자를 사용해 Pennant를 프로젝트에 설치합니다:

```shell
composer require laravel/pennant
```

다음으로, `vendor:publish` 아티즌 명령어로 Pennant의 설정 파일과 마이그레이션 파일을 배포해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. 이 과정에서 Pennant의 `database` 드라이버가 사용하는 `features` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
## 구성

Pennant의 에셋을 발행한 후에는 설정 파일이 `config/pennant.php` 경로에 생성됩니다. 이 설정 파일에서는 Pennant가 기능 플래그의 값을 저장할 때 사용할 기본 저장 메커니즘을 지정할 수 있습니다.

Pennant는 `array` 드라이버를 통해 인메모리 배열에 기능 플래그 값을 저장하는 방법과, 기본값인 `database` 드라이버를 통해 관계형 데이터베이스에 영구적으로 저장하는 방법을 모두 지원합니다.

<a name="defining-features"></a>
## 기능 정의

새로운 기능을 정의하려면, `Feature` 파사드가 제공하는 `define` 메서드를 사용합니다. 이때, 기능 이름과 해당 기능의 초깃값을 판단할 때 호출될 클로저를 함께 전달해야 합니다.

일반적으로 기능은 서비스 프로바이더에서 `Feature` 파사드를 사용해 정의합니다. 이 클로저는 기능 체크를 위한 "스코프"를 전달받는데, 대부분의 경우 현재 인증된 사용자입니다. 아래 예시에서는 새로운 API를 애플리케이션 사용자에게 점진적으로 배포하는 기능을 정의합니다:

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

위 예시에서 우리는 다음과 같은 규칙을 적용했습니다.

- 내부 팀 구성원들은 모두 새로운 API를 사용합니다.
- 트래픽이 많은 고객들은 새로운 API를 사용하지 않습니다.
- 그 외의 경우, 무작위로 100명 중 1명에게 기능이 활성화됩니다.

특정 사용자에 대해 처음으로 `new-api` 기능이 체크되면, 클로저의 반환값이 저장 드라이버에 저장됩니다. 이후 동일한 사용자에 대해 다시 기능을 체크할 때는 저장된 값을 가져오며, 클로저는 다시 실행되지 않습니다.

편의상, 기능 정의가 단순히 lottery 값만 반환한다면 클로저를 생략할 수 있습니다.

```
Feature::define('site-redesign', Lottery::odds(1, 1000));
```

<a name="class-based-features"></a>
### 클래스 기반 기능

Pennant는 클래스 기반 기능 정의도 지원합니다. 클로저 기반 기능과 달리, 클래스 기반 기능은 서비스 프로바이더에 별도로 등록할 필요가 없습니다. 클래스 기반 기능을 생성하려면 `pennant:feature` 아티즌 명령어를 사용하면 됩니다. 기본적으로 기능 클래스는 애플리케이션의 `app/Features` 디렉터리에 생성됩니다:

```shell
php artisan pennant:feature NewApi
```

기능 클래스를 작성할 때는, 주어진 스코프에 대해 기능의 초깃값을 판단하는 `resolve` 메서드만 정의하면 됩니다. 여기서도 스코프는 보통 현재 인증된 사용자입니다:

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

클래스 기반 기능의 인스턴스를 직접 생성해서 사용하고 싶을 때는 `Feature` 파사드의 `instance` 메서드를 호출하면 됩니다:

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]
> 기능 클래스는 [컨테이너](/docs/12.x/container)를 통해 생성되므로, 필요에 따라 생성자에 의존성을 주입할 수 있습니다.

#### 저장될 기능 이름 커스터마이징

기본적으로 Pennant는 기능 클래스의 전체 클래스명을 저장합니다. 만약 저장되는 기능 이름을 애플리케이션의 내부 구조와 분리하고자 한다면, 기능 클래스에 `$name` 속성을 정의할 수 있습니다. 이 속성의 값이 클래스명 대신 저장됩니다:

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
## 기능 확인

특정 기능이 활성화되어 있는지 확인하려면, `Feature` 파사드의 `active` 메서드를 사용하면 됩니다. 기본적으로 현재 인증된 사용자를 기준으로 기능이 체크됩니다:

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

기본값은 현재 인증된 사용자를 기준으로 체크하지만, 다른 사용자 또는 [스코프](#scope)에 대해서도 쉽게 기능을 확인할 수 있습니다. 이를 위해 `Feature` 파사드의 `for` 메서드를 사용하세요:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

Pennant는 기능이 활성화되었는지 판단할 때 유용한 여러 편의 메서드도 제공합니다:

```php
// 주어진 모든 기능이 활성화되어 있는지 확인합니다...
Feature::allAreActive(['new-api', 'site-redesign']);

// 주어진 기능 중 하나라도 활성화되어 있는지 확인합니다...
Feature::someAreActive(['new-api', 'site-redesign']);

// 특정 기능이 비활성화되어 있는지 확인합니다...
Feature::inactive('new-api');

// 주어진 모든 기능이 비활성화되어 있는지 확인합니다...
Feature::allAreInactive(['new-api', 'site-redesign']);

// 주어진 기능 중 하나라도 비활성화되어 있는지 확인합니다...
Feature::someAreInactive(['new-api', 'site-redesign']);
```

> [!NOTE]
> Pennant를 HTTP 환경이 아닌 곳(예: 아티즌 명령어나 큐 작업 등)에서 사용할 때는, 일반적으로 [기능의 스코프를 명시적으로 지정](#specifying-the-scope)해야 합니다. 또는 인증된 HTTP 컨텍스트와 인증되지 않은 컨텍스트 모두를 포괄하는 [기본 스코프](#default-scope)를 정의할 수도 있습니다.

<a name="checking-class-based-features"></a>
#### 클래스 기반 기능 확인

클래스 기반 기능의 경우, 기능 확인 시 클래스명을 전달하면 됩니다:

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

`when` 메서드를 사용하면, 기능이 활성화된 경우 해당 클로저를 실행할 수 있습니다. 또한 두 번째 클로저를 전달해 기능이 비활성화된 경우의 처리를 지정할 수도 있습니다:

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

`unless` 메서드는 `when`의 반대로 동작하여, 기능이 비활성화된 경우 첫 번째 클로저를 실행합니다:

```php
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
### `HasFeatures` 트레이트

Pennant의 `HasFeatures` 트레이트는 애플리케이션의 `User` 모델(또는 기능이 있는 다른 모델)에 추가하여 모델 자체에서 직접 기능을 편리하게 체크할 수 있도록 해줍니다:

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

이 트레이트를 모델에 적용한 후, `features` 메서드를 사용해 쉽게 기능을 확인할 수 있습니다:

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

물론 `features` 메서드를 통해 기능과 상호작용하는 다양한 편의 메서드도 사용할 수 있습니다:

```php
// 값 조회...
$value = $user->features()->value('purchase-button')
$values = $user->features()->values(['new-api', 'purchase-button']);

// 상태 확인...
$user->features()->active('new-api');
$user->features()->allAreActive(['new-api', 'server-api']);
$user->features()->someAreActive(['new-api', 'server-api']);

$user->features()->inactive('new-api');
$user->features()->allAreInactive(['new-api', 'server-api']);
$user->features()->someAreInactive(['new-api', 'server-api']);

// 조건부 실행...
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

Blade 템플릿에서 기능을 쉽게 확인할 수 있도록, Pennant는 `@feature`와 `@featureany` 디렉티브를 제공합니다:

```blade
@feature('site-redesign')
    <!-- 'site-redesign'가 활성화됨 -->
@else
    <!-- 'site-redesign'가 비활성화됨 -->
@endfeature

@featureany(['site-redesign', 'beta'])
    <!-- 'site-redesign' 또는 `beta`가 활성화됨 -->
@endfeatureany
```

<a name="middleware"></a>
### 미들웨어

Pennant는 현재 인증된 사용자가 기능에 접근 권한이 있는지 라우트를 실행하기 전에 검증하는 [미들웨어](/docs/12.x/middleware)도 제공합니다. 이 미들웨어를 라우트에 할당하고, 해당 라우트에 접근하기 위해 필요한 기능을 지정할 수 있습니다. 지정된 기능 중 하나라도 현재 인증된 사용자에게 비활성화되어 있다면, 라우트는 `400 Bad Request` HTTP 응답을 반환합니다. 여러 기능을 static `using` 메서드에 전달할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### 응답 커스터마이징

미들웨어에 지정된 기능 중 하나라도 비활성화일 때 반환되는 응답을 커스터마이징하고 싶다면, `EnsureFeaturesAreActive` 미들웨어의 `whenInactive` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 서비스 프로바이더의 `boot` 메서드 내에서 호출하면 됩니다:

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
### 기능 확인 가로채기

경우에 따라 저장된 기능 값을 가져오기 전에 인메모리로 특정 체크를 선행하고 싶을 때가 있습니다. 예를 들어, 새 API를 기능 플래그로 감싸두었을 때, 저장된 값은 그대로 유지하면서도 전체적으로 해당 API를 비활성화시키고 싶을 수 있습니다. 만약 새 API에서 버그가 발생했다면, 내부 팀 구성원을 제외한 모든 사용자에게 쉽게 비활성화한 뒤 버그를 수정하고, 기능의 접근 권한이 있던 사용자에게 다시 활성화할 수 있습니다.

이런 목적은 [클래스 기반 기능](#class-based-features)의 `before` 메서드로 달성할 수 있습니다. `before` 메서드를 정의하면 해당 메서드는 저장된 값을 불러오기 전에 항상 인메모리로 먼저 실행됩니다. 만약 `null`이 아닌 값이 반환되면, 해당 요청 동안에는 저장된 값 대신 반환된 값이 사용됩니다:

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

이 기능은 과거에 기능 플래그로 관리되던 기능의 전체 배포 시기 조정 등에도 사용할 수 있습니다:

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
### 인메모리 캐시

기능을 체크할 때 Pennant는 결과를 인메모리로 캐시합니다. 만약 `database` 드라이버를 사용하고 있다면, 동일한 기능 플래그를 단일 요청 내에서 여러 번 체크하더라도 추가적인 데이터베이스 쿼리가 발생하지 않습니다. 그리고 이렇게 하면 요청 전체 동안 기능값이 일관되게 유지됩니다.

인메모리 캐시를 수동으로 비우고 싶다면, `Feature` 파사드의 `flushCache` 메서드를 사용하면 됩니다:

```php
Feature::flushCache();
```

<a name="scope"></a>
## 스코프

<a name="specifying-the-scope"></a>
### 스코프 지정

앞서 설명했듯, Pennant의 기능 체크는 보통 현재 인증된 사용자를 기준으로 이루어집니다. 하지만 언제나 이 방식이 필요한 것은 아닙니다. 특정 기능을 확인할 때 사용하는 스코프를 명시적으로 지정하고 싶다면, `Feature` 파사드의 `for` 메서드를 사용하세요:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

기능의 스코프는 꼭 "사용자"로 한정되지 않습니다. 예를 들어, 개인 사용자 단위가 아닌 팀 전체를 대상으로 새로운 청구 경험을 점진적으로 배포하려고 할 수도 있습니다. 오래된 팀일수록 출시를 더 늦게 하고 싶을 수도 있겠죠. 이럴 경우 기능 판단용 클로저는 아래와 같이 작성할 수 있습니다:

```php
use App\Models\Team;
use Carbon\Carbon;
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

위 예시처럼 클로저는 `User` 대신 `Team` 모델을 인자로 받도록 정의할 수 있습니다. 사용자의 팀에 해당 기능이 활성화되어 있는지 확인하려면, `Feature` 파사드의 `for` 메서드에 팀을 전달하면 됩니다:

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### 기본 스코프

Pennant가 기능을 체크할 때 사용하는 기본 스코프도 커스터마이징할 수 있습니다. 예를 들어, 모든 기능을 항상 현재 인증된 사용자의 팀을 기준으로 체크해야 할 수도 있습니다. 매번 `Feature::for($user->team)`을 호출하는 대신, 팀을 기본 스코프로 지정할 수 있습니다. 이 작업은 일반적으로 애플리케이션의 서비스 프로바이더 중 한 곳에서 수행합니다:

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

이제, `for` 메서드를 통해 명시적으로 스코프를 지정하지 않는 한, 기능 체크는 현재 인증된 사용자의 팀을 기본 스코프로 사용합니다:

```php
Feature::active('billing-v2');

// 위 코드는 아래와 동일하게 동작합니다...

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>

### 널(Nullable) 스코프

Feature를 확인할 때 전달한 스코프가 `null`이고, 해당 feature 정의의 스코프 타입이 널 타입을 지원하지 않거나(Nullable 타입으로 선언하지 않았거나, 유니언 타입에 `null`이 포함되어 있지 않은 경우), Pennant는 자동으로 이 feature의 결과값을 `false`로 반환합니다.

따라서, feature에 전달하는 스코프가 `null`이 될 수 있고, feature 값 해석(Resolver)이 항상 호출되기를 원한다면, feature 정의에서 이를 고려해야 합니다. Artisan 명령어, 큐 작업, 인증되지 않은 라우트 등에서 feature를 확인할 때는, 일반적으로 인증된 사용자가 없기 때문에 기본 스코프가 `null`이 됩니다.

항상 [feature 스코프를 명시적으로 지정하지](#specifying-the-scope) 않는 경우, 스코프 타입을 널 허용(Nullable) 타입으로 지정하고, feature 정의 로직에서 `null`인 경우를 직접 처리해야 합니다:

```php
use App\Models\User;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

Feature::define('new-api', fn (User $user) => match (true) {// [tl! remove]
Feature::define('new-api', fn (User|null $user) => match (true) {// [tl! add]
    $user === null => true,// [tl! add]
    $user->isInternalTeamMember() => true,
    $user->isHighTrafficCustomer() => false,
    default => Lottery::odds(1 / 100),
});
```

<a name="identifying-scope"></a>
### 스코프 식별하기

Pennant의 기본 `array` 및 `database` 저장 드라이버는 모든 PHP 데이터 타입과 Eloquent 모델에 대해 스코프 식별자를 적절하게 저장할 수 있습니다. 하지만, 애플리케이션에서 서드파티 Pennant 드라이버를 사용한다면, 해당 드라이버가 Eloquent 모델이나 기타 커스텀 타입에 대한 식별자를 어떻게 저장할지 모를 수 있습니다.

이런 문제에 대비해, Pennant에서는 애플리케이션의 객체가 Pennant 스코프로 사용될 때 `FeatureScopeable` 계약(Contract)을 구현함으로써 저장용 스코프 값을 포맷팅할 수 있도록 지원합니다.

예를 들어, 하나의 애플리케이션에서 두 가지 다른 feature 드라이버(기본 `database` 드라이버와 서드파티 "Flag Rocket" 드라이버)를 함께 사용한다고 가정해 보겠습니다. "Flag Rocket" 드라이버는 Eloquent 모델을 직접 저장하지 못하고, 대신에 `FlagRocketUser` 인스턴스를 요구합니다. `FeatureScopeable` 계약에서 정의한 `toFeatureIdentifier`를 구현함으로써, 애플리케이션에서 사용하는 각각의 드라이버에 적합한 스코프 값을 반환할 수 있습니다:

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * 해당 드라이버에 맞는 feature 스코프 식별자로 객체를 캐스팅합니다.
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
### 스코프 직렬화(Serializing Scope)

기본적으로 Pennant는 Eloquent 모델과 연결된 feature를 저장할 때 완전한 클래스명을 사용합니다. 이미 [Eloquent morph map](/docs/12.x/eloquent-relationships#custom-polymorphic-types)을 사용하고 있다면, Pennant에서도 morph map을 사용하여 저장된 feature가 애플리케이션 구조에 결합되지 않도록 할 수 있습니다.

이를 위해 서비스 프로바이더에서 morph map을 정의한 후, `Feature` 파사드의 `useMorphMap` 메서드를 호출하면 됩니다:

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
## 리치(Rich) Feature 값

지금까지는 feature가 "활성/비활성"과 같은 2진 상태로만 동작하는 예시를 주로 다루었지만, Pennant는 리치(다양한) 값을 feature에 저장할 수도 있습니다.

예를 들어, 애플리케이션의 "Buy now" 버튼에 대해 세 가지 새로운 색상을 테스트한다고 가정해 보겠습니다. feature 정의에서 `true`나 `false` 대신, 문자열을 반환할 수 있습니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

`purchase-button` feature의 값을 가져올 때는 `value` 메서드를 사용할 수 있습니다:

```php
$color = Feature::value('purchase-button');
```

Pennant에서 기본 제공하는 Blade 디렉티브를 활용하면, feature의 현재 값에 따라 콘텐츠를 조건부로 렌더링하기도 쉽습니다:

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire'가 활성 상태입니다 -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green'이 활성 상태입니다 -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange'가 활성 상태입니다 -->
@endfeature
```

> [!NOTE]
> 리치 값을 사용할 때, feature의 값이 `false`가 아니라면 해당 feature는 "활성"으로 간주된다는 점을 알아두세요.

[조건부 `when`](#conditional-execution) 메서드를 호출할 경우, feature의 리치 값이 첫 번째 클로저에 전달됩니다:

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

마찬가지로, 조건부 `unless` 메서드를 호출하면, feature의 리치 값이 선택적으로 두 번째 클로저에 전달됩니다:

```php
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>
## 여러 Feature 가져오기

`values` 메서드는 주어진 스코프에 대해 여러 feature 값을 한 번에 가져올 수 있습니다:

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

또는, `all` 메서드를 사용하여 주어진 스코프에 대해 정의된 모든 feature의 값을 가져올 수도 있습니다:

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

단, 클래스 기반 feature는 동적으로 등록되므로, Pennant가 해당 feature를 직접 확인하기 전까지는 feature 목록에 나타나지 않을 수 있습니다. 즉, 현재 요청에서 아직 확인하지 않은 클래스 기반 feature는 `all` 메서드의 결과에 포함되지 않을 수 있습니다.

항상 feature 클래스가 `all` 메서드 사용 시 포함되도록 하려면, Pennant의 feature 디스커버리 기능을 사용할 수 있습니다. 먼저, 애플리케이션의 서비스 프로바이더 중 한 곳에서 `discover` 메서드를 호출하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Feature::discover();

        // ...
    }
}
```

`discover` 메서드는 애플리케이션의 `app/Features` 디렉터리에 있는 모든 feature 클래스를 자동으로 등록합니다. 이제 `all` 메서드는 해당 클래스 기반 feature를 포함시켜 결과를 반환합니다:

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
## Eager Loading

Pennant는 단일 요청 내에서 모든 feature의 해석 결과를 메모리에 캐싱하지만, 여전히 성능상의 이슈를 겪을 수 있습니다. 이를 해결하기 위해 Pennant는 feature 값을 미리 로드(eager load)하는 기능을 제공합니다.

예를 들어, 반복문 안에서 feature의 활성 여부를 검사하는 경우를 생각해보겠습니다:

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

데이터베이스 드라이버를 사용한다고 가정하면, 이 코드는 반복마다 개별 쿼리가 실행될 수 있어 수백 번의 쿼리가 발생할 수 있습니다. 하지만 Pennant의 `load` 메서드를 사용하면, 지정한 사용자 배열 또는 스코프 컬렉션의 feature 값을 미리 로딩함으로써, 이런 성능 병목 현상을 제거할 수 있습니다:

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

이미 로드되지 않은 feature 값만 미리 로드하고 싶다면, `loadMissing` 메서드를 사용할 수 있습니다:

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

정의된 모든 feature 값을 미리 로드하려면, `loadAll` 메서드를 활용하세요:

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
## 값 업데이트하기

feature의 값이 최초로 해석되면, 사용 중인 저장 드라이버가 해당 값을 스토리지를 통해 저장합니다. 이는 여러 요청에서 사용자에게 일관된 경험을 보장하는 데 필요합니다. 하지만, 때로는 저장된 feature 값을 직접 업데이트해야 할 수도 있습니다.

이럴 때는 `activate` 및 `deactivate` 메서드를 사용해 feature를 직접 "켜기" 또는 "끄기" 할 수 있습니다:

```php
use Laravel\Pennant\Feature;

// 기본 스코프에서 feature 활성화...
Feature::activate('new-api');

// 지정한 스코프에서 feature 비활성화...
Feature::for($user->team)->deactivate('billing-v2');
```

또한, `activate` 메서드의 두 번째 인자로 리치 값을 지정하여 feature 값을 직접 설정할 수도 있습니다:

```php
Feature::activate('purchase-button', 'seafoam-green');
```

Pennant에게 저장된 feature 값을 잊도록(삭제하도록) 지시하려면 `forget` 메서드를 사용합니다. 다시 feature를 확인하면, Pennant가 feature 정의값에서 새롭게 값을 해석하게 됩니다:

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### 대량(Bulk) 업데이트

feature 값을 다수의 사용자를 대상으로 한 번에 업데이트하려면, `activateForEveryone` 및 `deactivateForEveryone` 메서드를 사용할 수 있습니다.

예를 들어, 이제 `new-api` feature의 안정성에 확신을 갖고, 결제 플로우에 가장 어울리는 `'purchase-button'` 색상을 확정했다고 가정합시다. 모든 사용자에게 해당 값을 대량으로 업데이트할 수 있습니다:

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

반대로, feature를 모든 사용자에게 대량으로 비활성화할 수도 있습니다:

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> 이 작업은 Pennant의 저장 드라이버가 저장해 놓은(해석한) feature 값만 업데이트합니다. 실제 feature 정의 코드도 함께 최신 상태로 유지해야 한다는 점을 잊지 마세요.

<a name="purging-features"></a>
### Feature 전체 삭제(Purging)

특정 feature를 완전히 삭제하는 것이 필요할 때가 있습니다. 일반적으로 feature를 애플리케이션에서 제거했거나, feature 정의를 변경해 모든 사용자에게 재적용하고 싶을 때 유용합니다.

feature에 저장된 모든 값을 삭제하려면 `purge` 메서드를 사용합니다:

```php
// 단일 feature 삭제...
Feature::purge('new-api');

// 다수 feature 동시 삭제...
Feature::purge(['new-api', 'purchase-button']);
```

모든 feature를 스토리지에서 삭제하려면 인자 없이 `purge` 메서드를 호출하세요:

```php
Feature::purge();
```

애플리케이션 배포 파이프라인에서도 feature 삭제가 유용할 수 있기 때문에, Pennant에는 저장소에서 지정한 feature를 삭제하는 `pennant:purge` Artisan 명령어가 포함되어 있습니다:

```shell
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

지정한 feature 목록만 남기고 나머지 전체 feature를 삭제하고 싶다면, `--except` 옵션을 사용하면 됩니다. 예를 들어, "new-api"와 "purchase-button" feature만 유지하고 나머지는 모두 삭제하고 싶을 때 아래와 같이 입력합니다:

```shell
php artisan pennant:purge --except=new-api --except=purchase-button
```

또한, `pennant:purge` 명령어는 `--except-registered` 플래그도 지원합니다. 이 플래그를 지정하면, 서비스 프로바이더에서 명시적으로 등록된 feature를 제외한 나머지를 모두 삭제합니다:

```shell
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## 테스트(Test)

feature flag와 연동되는 코드를 테스트할 때, 테스트에서 feature flag의 반환 값을 제어하는 가장 쉬운 방법은 해당 feature를 재정의하는 것입니다. 예를 들어, 다음과 같이 애플리케이션의 서비스 프로바이더에서 feature가 정의되어 있다고 가정해 봅니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

테스트에서 feature의 반환 값을 변경하려면, 테스트 시작 시점에 feature를 재정의하면 됩니다. 아래 테스트는 `Arr::random()` 구현이 서비스 프로바이더에 남아 있더라도 항상 성공합니다:

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

이와 동일한 방법으로 클래스 기반 feature에도 활용할 수 있습니다:

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

만약 feature가 `Lottery` 인스턴스를 반환하는 경우에는 [테스트용 헬퍼 함수](/docs/12.x/helpers#testing-lotteries)도 제공합니다.

<a name="store-configuration"></a>
#### 저장소 설정

테스트 시 Pennant가 사용할 저장소를 설정하려면, 애플리케이션의 `phpunit.xml` 파일에서 `PENNANT_STORE` 환경변수를 지정하면 됩니다:

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
## 커스텀 Pennant 드라이버 추가

<a name="implementing-the-driver"></a>
#### 드라이버 구현

Pennant의 기본 저장 드라이버가 애플리케이션의 요구사항을 충족하지 못하는 경우, 직접 저장 드라이버를 구현할 수 있습니다. 커스텀 드라이버는 `Laravel\Pennant\Contracts\Driver` 인터페이스를 구현해야 합니다:

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

이제 Redis 연결을 활용하여 각각의 메서드를 구현하면 됩니다. 구체적인 구현 예시는 [Pennant 소스 코드의 `DatabaseDriver`](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)를 참고하시기 바랍니다.

> [!NOTE]
> Laravel은 기본적으로 확장(Extensions)을 위한 별도의 디렉터리를 제공하지 않습니다. 원하는 위치에 파일을 배치하면 되고, 위 예시에서는 `Extensions` 디렉터리에 `RedisFeatureDriver`를 생성했습니다.

<a name="registering-the-driver"></a>
#### 드라이버 등록

드라이버를 구현했다면 Laravel에 등록할 준비가 되었습니다. 추가로 Pennant에 드라이버를 등록하려면, `Feature` 파사드에서 제공하는 `extend` 메서드를 사용합니다. 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) 중 한 곳의 `boot` 메서드에서 호출해야 합니다:

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
     * 필요한 애플리케이션 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Feature::extend('redis', function (Application $app) {
            return new RedisFeatureDriver($app->make('redis'), $app->make('events'), []);
        });
    }
}
```

드라이버 등록이 완료되었으면, 이제 애플리케이션의 `config/pennant.php`에서 `redis` 드라이버를 지정해 사용할 수 있습니다:

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
### 외부에서 Feature 정의하기

만약 커스텀 드라이버가 서드파티 feature flag 플랫폼의 래퍼 역할이라면, 아마도 Pennant의 `Feature::define` 메서드가 아닌, 외부 플랫폼 내에서 feature를 정의할 가능성이 높습니다. 이런 경우에는 드라이버 역시 `Laravel\Pennant\Contracts\DefinesFeaturesExternally` 인터페이스를 함께 구현해야 합니다:

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;
use Laravel\Pennant\Contracts\DefinesFeaturesExternally;

class FeatureFlagServiceDriver implements Driver, DefinesFeaturesExternally
{
    /**
     * 주어진 스코프에 대해 정의된 feature 목록을 반환.
     */
    public function definedFeaturesForScope(mixed $scope): array {}

    /* ... */
}
```

`definedFeaturesForScope` 메서드는 제공된 스코프에 대해 정의된 feature 이름의 리스트를 반환해야 합니다.

<a name="events"></a>
## 이벤트(Events)

Pennant는 feature flag를 추적하거나 모니터링할 때 유용하게 사용할 수 있는 다양한 이벤트를 발생시킵니다.

### `Laravel\Pennant\Events\FeatureRetrieved`

[feature를 확인할 때](#checking-features)마다 발생하는 이벤트입니다. 이 이벤트를 활용하여 전체 애플리케이션에서 feature flag 사용량에 대한 메트릭 추적 등에 활용할 수 있습니다.

### `Laravel\Pennant\Events\FeatureResolved`

특정 스코프에 대해 feature 값이 처음으로 해석될 때 발생합니다.

### `Laravel\Pennant\Events\UnknownFeatureResolved`

특정 스코프에서 알 수 없는 feature가 처음 해석될 때 이 이벤트가 발생합니다. feature flag를 제거했음에도 불구하고, 코드 곳곳에 남아 있는 참조 때문에 예상치 못한 feature 해석이 발생할 때 이를 추적하는 데 유용합니다:

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
     * 애플리케이션 서비스 부트스트랩.
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

이 이벤트는 [클래스 기반 기능](#class-based-features)이 요청 중에 처음으로 동적으로 체크될 때 발생합니다.

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

이 이벤트는 [null을 지원하지 않는](#nullable-scope) 기능 정의에 `null` 스코프가 전달될 때 발생합니다.

이 상황은 Pennant가 별다른 오류 없이 부드럽게 처리하며, 해당 기능은 `false`를 반환합니다. 그러나 이러한 기본 동작을 사용하지 않고 별도로 처리하고 싶다면, 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 이 이벤트에 대한 리스너를 등록할 수 있습니다.

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

이 이벤트는 특정 스코프에 대한 기능을 업데이트할 때, 보통 `activate` 또는 `deactivate`를 호출할 때 발생합니다.

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

이 이벤트는 모든 스코프에 대해 기능을 업데이트할 때, 즉 `activateForEveryone` 또는 `deactivateForEveryone`을 호출할 때 발생합니다.

### `Laravel\Pennant\Events\FeatureDeleted`

이 이벤트는 특정 스코프의 기능을 삭제할 때, 즉 보통 `forget`을 호출할 때 발생합니다.

### `Laravel\Pennant\Events\FeaturesPurged`

이 이벤트는 특정 기능들을 완전히 제거(purge)할 때 발생합니다.

### `Laravel\Pennant\Events\AllFeaturesPurged`

이 이벤트는 모든 기능을 완전히 제거(purge)할 때 발생합니다.