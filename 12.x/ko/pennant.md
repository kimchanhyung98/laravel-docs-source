# Laravel Pennant

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
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
- [풍부한 기능값 활용](#rich-feature-values)
- [여러 기능 조회](#retrieving-multiple-features)
- [사전 로딩(Eager Loading)](#eager-loading)
- [값 갱신](#updating-values)
    - [일괄 업데이트](#bulk-updates)
    - [기능 정리(Purging)](#purging-features)
- [테스트](#testing)
- [커스텀 Pennant 드라이버 추가](#adding-custom-pennant-drivers)
    - [드라이버 구현](#implementing-the-driver)
    - [드라이버 등록](#registering-the-driver)
    - [외부에서 기능 정의](#defining-features-externally)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Pennant](https://github.com/laravel/pennant)는 군더더기 없는 심플하고 가벼운 기능 플래그(feature flag) 패키지입니다. 기능 플래그를 활용하면 새로운 애플리케이션 기능을 점진적으로 롤아웃하거나, 새로운 인터페이스 디자인의 A/B 테스트, 트렁크 기반 개발 전략 보조 등 다양한 목적에 자신감을 가지고 적용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 사용해 Pennant를 프로젝트에 설치합니다:

```shell
composer require laravel/pennant
```

다음으로, `vendor:publish` Artisan 명령어를 사용해 Pennant의 설정 및 마이그레이션 파일을 게시합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

마지막으로 애플리케이션 데이터베이스 마이그레이션을 실행합니다. 이 작업은 Pennant가 `database` 드라이버를 사용할 때 필요한 `features` 테이블을 생성합니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
## 설정

Pennant 에셋을 게시한 후에는 설정 파일이 `config/pennant.php`에 위치합니다. 이 파일을 통해 Pennant가 기능 플래그 값을 저장하는 기본 저장소(storage) 방식을 지정할 수 있습니다.

Pennant는 `array` 드라이버를 통해 인메모리 배열에 값을 저장할 수도 있고, `database` 드라이버(기본값)를 통해 관계형 데이터베이스에 영구적으로 값을 저장할 수도 있습니다.

<a name="defining-features"></a>
## 기능 정의

기능을 정의하려면 `Feature` 파사드의 `define` 메서드를 사용합니다. 기능의 이름과, 기능의 초기값을 반환하는 클로저를 전달해야 합니다.

일반적으로 기능은 서비스 프로바이더 내에서 `Feature` 파사드를 사용해 정의합니다. 전달되는 클로저는 "스코프(scope)"를 인자로 받는데, 대부분의 경우 현재 인증된 사용자입니다. 아래 예시에서는 애플리케이션 사용자에게 새 API를 점진적으로 배포하기 위한 기능을 정의했습니다:

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
     * 애플리케이션 서비스 부트스트랩.
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

위 예시에서 적용되는 규칙은 다음과 같습니다:

- 내부 팀 멤버는 모두 새 API를 사용해야 합니다.
- 트래픽이 많은 고객은 새 API를 사용하지 않습니다.
- 그 외의 경우, 100명 중 1명 확률로 무작위로 기능이 할당됩니다.

`new-api` 기능이 특정 사용자에 대해 처음 체크될 때 클로저의 반환값이 저장소 드라이버에 저장됩니다. 동일한 사용자에 대해 이후에 기능을 체크할 때는 저장된 값이 반환되며 클로저는 다시 호출되지 않습니다.

편의상, 기능 정의가 로터리(Lottery)만 반환한다면 클로저를 생략할 수도 있습니다:

    Feature::define('site-redesign', Lottery::odds(1, 1000));

<a name="class-based-features"></a>
### 클래스 기반 기능

Pennant는 클래스 기반 기능 정의도 제공합니다. 클로저 기반 정의와 달리, 클래스 기반 기능은 서비스 프로바이더에서 등록할 필요가 없습니다. 클래스 기반 기능을 생성하려면 `pennant:feature` Artisan 명령어를 사용할 수 있습니다. 기본적으로 기능 클래스는 `app/Features` 디렉터리에 생성됩니다:

```shell
php artisan pennant:feature NewApi
```

기능 클래스 작성 시, 주로 `resolve` 메서드만 정의하면 됩니다. 이 메서드는 특정 스코프(일반적으로 인증된 사용자)에 대해 기능의 초기값을 반환하는 역할을 합니다:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * 기능의 초기값 반환.
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

클래스 기반 기능의 인스턴스를 수동으로 직접 해석하고 싶다면, `Feature` 파사드의 `instance` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]
> 기능 클래스는 [컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 필요하다면 생성자에 의존성을 주입할 수 있습니다.

#### 저장되는 기능 이름 커스터마이징

기본적으로 Pennant는 클래스의 완전한 네임스페이스 경로(FQCN)를 이름으로 저장합니다. 어플리케이션 내부 구조와 저장되는 기능명을 분리하고 싶다면, 클래스에 `$name` 프로퍼티를 지정할 수 있습니다. 이 값을 기능 이름으로 사용합니다:

```php
<?php

namespace App\Features;

class NewApi
{
    /**
     * 저장되는 기능 이름.
     *
     * @var string
     */
    public $name = 'new-api';

    // ...
}
```

<a name="checking-features"></a>
## 기능 확인

기능이 활성(active) 상태인지 확인하려면 `Feature` 파사드의 `active` 메서드를 사용하세요. 기본적으로 현재 인증된 사용자 기준으로 확인합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * 리소스 목록 표시.
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

기본적으로 인증된 사용자를 기준으로 확인하지만, 다른 사용자나 [스코프](#scope)로도 확인할 수 있습니다. 이를 위해 `for` 메서드를 사용하세요:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

Pennant는 기능 활성/비활성 여부를 판단할 때 사용할 수 있는 추가적인 편의 메서드도 제공합니다:

```php
// 모든 기능이 활성인지 확인...
Feature::allAreActive(['new-api', 'site-redesign']);

// 일부 기능이 활성인지 확인...
Feature::someAreActive(['new-api', 'site-redesign']);

// 특정 기능이 비활성인지 확인...
Feature::inactive('new-api');

// 모든 기능이 비활성인지 확인...
Feature::allAreInactive(['new-api', 'site-redesign']);

// 일부 기능이 비활성인지 확인...
Feature::someAreInactive(['new-api', 'site-redesign']);
```

> [!NOTE]
> Artisan 명령어나 큐 작업 등 HTTP 컨텍스트 외부에서 사용할 때는, 보통 [기능의 스코프를 명시적으로 지정](#specifying-the-scope)해야 합니다. 또는 인증된/비인증 컨텍스트 모두를 감안해 [기본 스코프](#default-scope)를 설정할 수도 있습니다.

<a name="checking-class-based-features"></a>
#### 클래스 기반 기능 확인

클래스 기반 기능의 경우, 기능 확인 시 클래스 이름을 전달해야 합니다:

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
     * 리소스 목록 표시.
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

`when` 메서드를 사용하면, 기능이 활성 상태일 때 지정한 클로저를 유연하게 실행할 수 있습니다. 추가로 두 번째 클로저를 전달하면 기능이 비활성일 때 실행됩니다:

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
     * 리소스 목록 표시.
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

`unless` 메서드는 `when`의 반대 동작으로, 기능이 비활성 상태일 때 첫 번째 클로저를 실행합니다:

```php
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
### `HasFeatures` 트레이트

Pennant의 `HasFeatures` 트레이트를 애플리케이션의 `User` 모델(또는 기능 플래그를 가질 수 있는 다른 모델)에 추가하면, 모델에서 바로 기능을 편리하게 확인할 수 있습니다:

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

트레이트를 모델에 추가한 후에는, `features` 메서드로 바로 기능을 확인할 수 있습니다:

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

물론, `features` 메서드는 다양한 기능 상태 확인 및 실행 관련 여러 편의 메서드를 제공합니다:

```php
// 값 조회...
$value = $user->features()->value('purchase-button');
$values = $user->features()->values(['new-api', 'purchase-button']);

// 상태 조회...
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

Blade에서 기능 확인을 쉽게 할 수 있도록, Pennant는 `@feature` 및 `@featureany` Blade 디렉티브를 제공합니다:

```blade
@feature('site-redesign')
    <!-- 'site-redesign'이 활성 상태일 때 -->
@else
    <!-- 'site-redesign'이 비활성 상태일 때 -->
@endfeature

@featureany(['site-redesign', 'beta'])
    <!-- 'site-redesign' 또는 `beta`가 활성 상태일 때 -->
@endfeatureany
```

<a name="middleware"></a>
### 미들웨어

Pennant는 [미들웨어](/docs/{{version}}/middleware)로, 현재 인증된 사용자가 특정 기능을 사용할 수 있는지 확인할 수 있습니다. 미들웨어는 라우트에 할당할 수 있으며, 해당 라우트에 접근하려면 지정한 기능들이 모두 활성 상태여야 합니다. 지정한 기능 중 하나라도 비활성인 경우 라우트는 `400 Bad Request` HTTP 응답을 반환합니다. 여러 기능을 `using` 메서드에 나열할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### 응답 커스터마이징

미들웨어가 비활성 기능을 감지했을 때 반환할 응답을 커스터마이징하려면, `EnsureFeaturesAreActive` 미들웨어의 `whenInactive` 메서드를 사용할 수 있습니다. 보통 이 메서드는 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

/**
 * 애플리케이션 서비스 부트스트랩.
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

경우에 따라 저장된 기능 값 조회 전에 인메모리 체크를 하고 싶을 수도 있습니다. 예를 들어, 신규 API를 기능 플래그로 배포 중 새 API를 긴급히 비활성화 하고 싶지만, 저장된 기능 값은 보존하고 싶다면 이 기능이 유용합니다. 버그 발견 시, 내부 팀만 예외로 제한하고 이후 수정 후 기존 사용자에게 다시 활성화할 수 있습니다.

이런 목적에는 [클래스 기반 기능](#class-based-features)의 `before` 메서드를 활용할 수 있습니다. 이 메서드가 구현되어 있으면 인메모리에서 항상 먼저 실행되며, `null`이 아닌 값을 반환하면 해당 요청 동안 그 값이 저장된 값 대신 사용됩니다:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * 저장된 값 조회 전 항상 인메모리 체크 실행.
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }
    }

    /**
     * 기능의 초기값 반환.
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

이 기능을 활용해 이전에 기능 플래그로 보호했던 기능의 전체 전역 공개(rollout)도 예약할 수 있습니다:

```php
<?php

namespace App\Features;

use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Config;

class NewApi
{
    /**
     * 저장된 값 조회 전 항상 인메모리 체크 실행.
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

Pennant는 기능 상태를 확인할 때마다 결과를 인메모리 캐시에 저장합니다. `database` 드라이버 사용 시, 동일 기능 플래그를 한 요청 내에서 반복 조회해도 추가적인 DB 쿼리가 발생하지 않습니다. 또한 한 요청 동안 해당 기능 상태가 일관되게 유지됩니다.

인메모리 캐시를 수동으로 비워야 할 경우, `Feature` 파사드의 `flushCache` 메서드를 사용하세요:

```php
Feature::flushCache();
```

<a name="scope"></a>
## 스코프

<a name="specifying-the-scope"></a>
### 스코프 지정

앞서 설명했듯, 기능은 보통 현재 인증된 사용자 기준으로 확인합니다. 하지만 필요에 따라 다른 스코프 기준으로 기능을 확인할 수 있습니다. 이 때는 `Feature` 파사드의 `for` 메서드를 이용해 스코프를 지정하세요:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

기능 스코프는 반드시 "유저"일 필요는 없습니다. 예를 들어, 새 빌링 경험을 사용자별이 아니라 팀 단위로 롤아웃하고 싶고, 오래된 팀은 더 천천히 적용하고 싶다면 다음과 같이 정의할 수 있습니다:

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

여기서 클로저가 `User`가 아닌 `Team` 모델을 인자로 받고 있습니다. 사용자의 팀 단위로 기능 활성여부를 확인하려면 `for` 메서드에 팀을 전달하세요:

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### 기본 스코프

Pennant가 기능을 확인할 때 사용하는 기본 스코프도 커스터마이징할 수 있습니다. 예를 들어 모든 기능을 사용자 대신 사용자 소속 팀 단위로 확인하고자 하는 경우, 반복적으로 `Feature::for($user->team)`을 호출하지 않고도 디폴트 스코프로 지정할 수 있습니다. 보통 서비스 프로바이더 내에서 설정합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Feature::resolveScopeUsing(fn ($driver) => Auth::user()?->team);

        // ...
    }
}
```

`for` 메서드로 별도 스코프 전달이 없으면, 이제 인증된 사용자의 팀이 디폴트 스코프로 사용됩니다:

```php
Feature::active('billing-v2');

// 위는 아래와 동일함

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### Nullable 스코프

기능 확인 시 전달한 스코프가 `null`이고, 기능 정의에서 이를 nullable 타입이나 union 타입에 포함해 지원하지 않으면, Pennant는 자동으로 `false`를 반환합니다.

즉, 전달한 스코프가 `null`이 될 수 있고, 해당 값에 대해 기능값 해석(closure)이 호출되길 원한다면, 기능 정의에서 이를 고려해야 합니다. Artisan 명령어나 큐 작업, 비인증 라우트 등에서는 기본 스코프가 `null`이 될 수 있습니다.

항상 [명시적으로 스코프를 지정](#specifying-the-scope)하지 않는다면, 스코프 타입을 nullable로 만들어서 내부에서 `null` 스코프를 적절히 처리하세요:

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
### 스코프 식별

Pennant의 내장 `array` 및 `database` 저장 드라이버는 PHP의 모든 데이터 타입과 Eloquent 모델에 대한 스코프 식별자를 올바르게 저장할 수 있습니다. 그러나 외부 Pennant 드라이버를 사용하는 경우, 그 드라이버는 Eloquent 모델이나 애플리케이션의 커스텀 타입에 대한 식별자를 알지 못할 수 있습니다.

따라서, 애플리케이션에서 Pennant 스코프로 사용되는 객체에 `FeatureScopeable` 인터페이스를 구현해 스코프 값을 저장할 수 있습니다.

예를 들어, 하나의 애플리케이션에서 내장 `database` 드라이버와 써드파티 "Flag Rocket" 드라이버를 함께 사용한다고 합시다. "Flag Rocket" 드라이버는 Eloquent 모델 저장방법을 모르지만, 자체 `FlagRocketUser` 인스턴스를 사용하도록 요구합니다. 이런 경우, 구현체에 FeatureScopeable 인터페이스의 `toFeatureIdentifier` 메서드를 구현해, 드라이버별 알맞은 값을 반환할 수 있습니다:

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * 드라이버별 기능 스코프 식별자로 변환
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

기본적으로 Pennant는 Eloquent 모델과 연결된 기능을 저장할 때 완전한 클래스 이름(FQCN)을 사용합니다. 이미 [Eloquent morph map](/docs/{{version}}/eloquent-relationships#custom-polymorphic-types)을 사용하는 경우, Pennant 또한 morph map을 사용하게 해 기능 저장값과 애플리케이션 구조 간의 결합을 줄일 수 있습니다.

이를 위해 서비스 프로바이더에서 morph map을 정의한 후, `Feature` 파사드의 `useMorphMap` 메서드를 호출하세요:

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
## 풍부한 기능값 활용

지금까지는 기능을 단순히 "활성/비활성" 이진 값으로만 사용했지만, Pennant는 풍부한 값(rich value)도 저장할 수 있습니다.

예를 들어, "구매하기" 버튼의 색상을 3가지로 A/B 테스트한다고 가정해 보겠습니다. 이 때 기능 정의에서 `true` 또는 `false` 대신 임의의 문자열을 반환할 수 있습니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

`purchase-button` 기능의 값은 `value` 메서드로 가져올 수 있습니다:

```php
$color = Feature::value('purchase-button');
```

Pennant의 Blade 디렉티브 역시 현재 기능값에 따라 조건부로 콘텐츠를 쉽게 렌더링할 수 있습니다:

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire'가 활성 상태일 때 -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green'이 활성 상태일 때 -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange'가 활성 상태일 때 -->
@endfeature
```

> [!NOTE]
> 풍부한 값 사용 시, 값이 `false`가 아닐 경우 모두 "활성"으로 간주된다는 점에 유의하세요.

[조건부 `when`](#conditional-execution) 메서드 호출 시, 기능의 값이 첫 클로저의 인자로 전달됩니다:

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

마찬가지로, `unless` 조건부 메서드는 기능값을 두 번째(선택적) 클로저에 전달합니다:

```php
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>
## 여러 기능 조회

`values` 메서드를 사용하여 한 번에 여러 기능 값을 조회할 수 있습니다:

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

또는, `all` 메서드로 스코프에 대해 정의된 모든 기능의 값을 조회할 수 있습니다:

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

하지만 클래스 기반 기능은 동적으로 등록되고, 실제로 확인되기 전까지 Pennant에서 인식되지 않습니다. 따라서 한 번도 체크되지 않은 기능 클래스는 `all`의 결과에 나타나지 않을 수 있습니다.

기능 클래스도 항상 `all`에 포함시키고 싶다면, Pennant의 기능 탐지 기능을 사용할 수 있습니다. 이를 위해, 서비스 프로바이더 등에서 `discover` 메서드를 호출하세요:

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

`discover` 메서드는 `app/Features` 디렉터리 내의 모든 기능 클래스를 등록하여, 현재 요청에서 한 번도 체크되지 않았어도 `all` 결과에 항상 포함시킵니다:

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
## 사전 로딩(Eager Loading)

Pennant는 단일 요청 동안 모든 해석된 기능값을 인메모리에 캐시하지만, 여전히 성능 문제가 발생할 수 있습니다. 이를 보완하기 위해 Pennant는 기능 값을 미리 로드(eager load)하는 방법을 제공합니다.

예를 들어, 다음처럼 반복문 내에서 기능 활성 여부를 확인하는 상황을 생각해봅시다:

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

`database` 드라이버를 사용하는 경우, 사용자마다 매번 DB 쿼리를 실행하므로 수백 번의 쿼리가 발생할 수 있습니다. 그러나 `load` 메서드를 이용해 미리 필요한 기능값을 모두 가져오면 이런 성능 저하를 방지할 수 있습니다:

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

이미 로드되지 않은 기능값만 가져오고 싶다는 경우, `loadMissing` 메서드를 사용할 수 있습니다:

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

정의된 모든 기능값을 한 번에 로드하려면 `loadAll` 메서드를 사용하세요:

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
## 값 갱신

기능의 값이 처음 해석될 때, 해당 결과가 저장소에 저장됩니다. 이것은 사용자에게 일관된 경험을 제공하기 위해 필요할 수 있습니다. 하지만 때로는 기능 저장값을 수동으로 갱신하고 싶을 수 있습니다.

이때 `activate` 및 `deactivate` 메서드로 기능을 "켜거나/끄는" 동작을 할 수 있습니다:

```php
use Laravel\Pennant\Feature;

// 기본 스코프에 기능 활성화...
Feature::activate('new-api');

// 특정 스코프(예: 팀)에 기능 비활성화...
Feature::for($user->team)->deactivate('billing-v2');
```

또한, `activate` 메서드에 두 번째 인자로 값(rich value)을 직접 전달해 저장할 수도 있습니다:

```php
Feature::activate('purchase-button', 'seafoam-green');
```

기능의 저장값을 잊고 다시 정의된 값으로 재해석하기 원한다면, `forget` 메서드를 사용하세요. 이후 해당 기능 확인 시, 다시 정의된 값이 사용됩니다:

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### 일괄 업데이트

여러 사용자 또는 모든 사용자에 대해 기능값을 일괄적으로 업데이트하려면 `activateForEveryone`, `deactivateForEveryone` 메서드를 사용할 수 있습니다.

예를 들어, `new-api` 기능의 안정성이 확보되고, 'purchase-button'의 최적색상이 결정된 경우 모든 사용자 데이터에 적용할 수 있습니다:

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

반대로, 모든 사용자에 대해 해당 기능을 비활성화할 수도 있습니다:

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> 이는 Pennant 저장소 드라이버에 저장된 해석값만 업데이트합니다. 애플리케이션의 기능 정의도 수정해야 할 수 있습니다.

<a name="purging-features"></a>
### 기능 정리(Purging)

기능을 완전히 앱에서 제거했거나, 기능 정의에 대해 모든 사용자에게 완전히 다시 적용하고 싶을 때 기능을 전체 정리(purge)할 수 있습니다.

`purge` 메서드로 특정 기능의 모든 저장값을 제거할 수 있습니다:

```php
// 단일 기능 정리
Feature::purge('new-api');

// 여러 기능 정리
Feature::purge(['new-api', 'purchase-button']);
```

또는, 모든 기능을 한 번에 정리하려면 인자를 생략하면 됩니다:

```php
Feature::purge();
```

애플리케이션 배포 파이프라인에서 기능 정리가 필요한 경우, Pennant는 Artisan 명령어 `pennant:purge`를 제공합니다:

```shell
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

특정 기능을 _제외_ 하고 나머지를 모두 정리하려면, `--except` 옵션을 사용하세요:

```shell
php artisan pennant:purge --except=new-api --except=purchase-button
```

또한, `pennant:purge` 명령은 `--except-registered` 플래그도 지원합니다. 이렇게 하면 서비스 프로바이더에 명확하게 등록된 기능 외 모두 정리됩니다:

```shell
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## 테스트

기능 플래그와 상호작용하는 코드를 테스트할 때, 테스트 내에서 간단하게 다시 기능을 정의하는 것이 가장 쉽게 반환값을 통제하는 방법입니다. 예를 들어, 서비스 프로바이더에서 다음과 같이 기능을 정의했다고 합시다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

테스트에서 반환 값을 고정하고 싶다면, 테스트 앞머리에 기능을 다시 정의하면 됩니다. 아래 테스트는 `Arr::random()`이 정의에 남아있어도 항상 통과합니다:

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

동일 방식으로 클래스 기반 기능도 처리할 수 있습니다:

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

기능이 `Lottery` 인스턴스를 반환한다면, 몇 가지 유용한 [테스트용 헬퍼](/docs/{{version}}/helpers#testing-lotteries)도 사용할 수 있습니다.

<a name="store-configuration"></a>
#### 저장소 설정

Pennant가 테스트 중에 활용할 저장소를 지정하려면, 애플리케이션의 `phpunit.xml` 파일에 `PENNANT_STORE` 환경 변수를 정의하세요:

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

Pennant의 기본 저장 드라이버가 요구사항에 맞지 않는다면, 직접 저장 드라이버를 구현할 수 있습니다. 커스텀 드라이버는 `Laravel\Pennant\Contracts\Driver` 인터페이스를 구현해야 합니다:

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

이제 각 메서드를 Redis 커넥션 등을 활용하여 구현하면 됩니다. 구체적인 구현 예시는 [Pennant 소스코드의 DatabaseDriver](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)를 참고하세요.

> [!NOTE]
> 라라벨에 확장용 디렉터리 구조가 기본 포함되어 있지 않습니다. 원하는 위치에 구현 클래스를 둘 수 있습니다. 예시에서는 `Extensions` 디렉터리에 `RedisFeatureDriver`를 뒀습니다.

<a name="registering-the-driver"></a>
#### 드라이버 등록

드라이버 구현이 끝났다면, Laravel에 등록해야 합니다. Pennant에 추가 드라이버를 등록하려면, `Feature` 파사드의 `extend` 메서드를 사용하세요. 보통 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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
     * 애플리케이션 서비스 등록.
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

등록 후에는 `config/pennant.php` 설정 파일에서 `redis` 드라이버를 사용할 수 있습니다:

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
### 외부에서 기능 정의

만약 커스텀 드라이버가 외부 써드파티 기능 플래그 플랫폼을 래핑하고 있다면, Pennant의 `Feature::define` 메서드 대신 외부 플랫폼에서 기능을 정의할 수 있습니다. 이 경우, 커스텀 드라이버는 `Laravel\Pennant\Contracts\DefinesFeaturesExternally` 인터페이스도 구현해야 합니다:

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;
use Laravel\Pennant\Contracts\DefinesFeaturesExternally;

class FeatureFlagServiceDriver implements Driver, DefinesFeaturesExternally
{
    /**
     * 주어진 스코프에 정의된 기능 목록 반환
     */
    public function definedFeaturesForScope(mixed $scope): array {}

    /* ... */
}
```

`definedFeaturesForScope` 메서드는 주어진 스코프에 정의된 기능명 배열을 반환하면 됩니다.

<a name="events"></a>
## 이벤트

Pennant는 기능 플래그의 상태 추적에 유용한 다양한 이벤트를 발생시킵니다.

### `Laravel\Pennant\Events\FeatureRetrieved`

[기능이 확인](#checking-features)될 때마다 발생합니다. 기능 플래그 사용 통계나 추적 등 메트릭 수집에 활용할 수 있습니다.

### `Laravel\Pennant\Events\FeatureResolved`

특정 스코프에 대해 기능 값이 처음 해석(resolved)될 때 발생합니다.

### `Laravel\Pennant\Events\UnknownFeatureResolved`

특정 스코프에 대해 Pennant가 알지 못하는 기능이 처음 해석될 때 발생합니다. 이 이벤트는 의도적으로 기능 플래그를 제거했으나, 애플리케이션에 남아있는 잘못된 참조를 추적할 때 유용합니다:

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

요청 도중 [클래스 기반 기능](#class-based-features)이 처음으로 동적으로 확인될 때 발생합니다.

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

[null 미지원](#nullable-scope) 기능 정의에 `null` 스코프가 전달될 때 발생합니다.

이 상황은 자동으로 안전하게 `false`를 반환하도록 처리됩니다. 하지만 원한다면 `AppServiceProvider`의 `boot` 메서드에서 이 이벤트 리스너를 등록해 기본 동작을 변경할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;
use Laravel\Pennant\Events\UnexpectedNullScopeEncountered;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Event::listen(UnexpectedNullScopeEncountered::class, fn () => abort(500));
}
```

### `Laravel\Pennant\Events\FeatureUpdated`

특정 스코프에 대해 기능이 업데이트(보통 `activate` 또는 `deactivate` 호출)될 때 발생합니다.

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

모든 스코프에 대해 기능이 업데이트(보통 `activateForEveryone` 또는 `deactivateForEveryone` 호출) 될 때 발생합니다.

### `Laravel\Pennant\Events\FeatureDeleted`

특정 스코프에 대해 기능이 삭제(보통 `forget` 호출)될 때 발생합니다.

### `Laravel\Pennant\Events\FeaturesPurged`

특정 기능이 정리(purge)될 때 발생합니다.

### `Laravel\Pennant\Events\AllFeaturesPurged`

모든 기능이 정리(purge)될 때 발생합니다.
