# Laravel Pennant

- [소개](#introduction)
- [설치](#installation)
- [구성](#configuration)
- [기능 정의하기](#defining-features)
    - [클래스 기반 기능](#class-based-features)
- [기능 확인하기](#checking-features)
    - [조건부 실행](#conditional-execution)
    - [`HasFeatures` 트레이트](#the-has-features-trait)
    - [Blade 디렉티브](#blade-directive)
    - [미들웨어](#middleware)
    - [기능 확인 가로채기](#intercepting-feature-checks)
    - [메모리 내 캐시](#in-memory-cache)
- [스코프](#scope)
    - [스코프 지정하기](#specifying-the-scope)
    - [기본 스코프](#default-scope)
    - [Nullable 스코프](#nullable-scope)
    - [스코프 식별하기](#identifying-scope)
    - [스코프 직렬화](#serializing-scope)
- [리치 값 기능](#rich-feature-values)
- [여러 기능 가져오기](#retrieving-multiple-features)
- [즉시 로딩(Eager Loading)](#eager-loading)
- [값 업데이트](#updating-values)
    - [일괄 업데이트](#bulk-updates)
    - [기능 삭제(Purging)](#purging-features)
- [테스트](#testing)
- [커스텀 Pennant 드라이버 추가](#adding-custom-pennant-drivers)
    - [드라이버 구현](#implementing-the-driver)
    - [드라이버 등록](#registering-the-driver)
    - [외부에서 기능 정의](#defining-features-externally)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Pennant](https://github.com/laravel/pennant)은 불필요한 요소 없이 간단하고 가벼운 피처 플래그 패키지입니다. 피처 플래그는 새로운 애플리케이션 기능을 점진적으로 배포할 수 있게 해주며, 인터페이스 A/B 테스트, trunk 기반 개발 전략 보완 등 다양한 용도로 사용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 사용하여 프로젝트에 Pennant를 설치하세요:

```shell
composer require laravel/pennant
```

다음으로, `vendor:publish` Artisan 명령어를 사용하여 Pennant의 구성 및 마이그레이션 파일을 퍼블리시합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행하세요. Pennant에서 사용하는 `features` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
## 구성

Pennant의 에셋을 퍼블리시한 후, 구성 파일은 `config/pennant.php`에 위치합니다. 이 구성 파일에서는 Pennant가 기능 플래그 값(Feature Flag Value)을 저장할 때 사용할 기본 저장 방식을 지정할 수 있습니다.

Pennant는 `array` 드라이버를 통해 메모리 내 배열에 기능 플래그 값을 저장하는 것을 지원합니다. 또는 `database` 드라이버를 통해 관계형 데이터베이스에 영구적으로 기능 플래그 값을 저장할 수도 있으며, 이것이 Pennant의 기본 저장 방식입니다.

<a name="defining-features"></a>
## 기능 정의하기

기능(Feature)을 정의하려면, `Feature` 파사드에서 제공하는 `define` 메서드를 사용할 수 있습니다. 기능의 이름과 해당 기능의 초기 값을 해석할 때 실행할 클로저를 제공해야 합니다.

일반적으로 기능은 서비스 프로바이더에서 `Feature` 파사드를 사용하여 정의합니다. 이 클로저는 기능 검사할 때 사용할 "스코프"를 받게 됩니다. 대부분의 경우 스코프는 현재 인증된 사용자입니다. 예를 들어, 애플리케이션 사용자에게 새로운 API를 점진적으로 배포할 기능을 다음과 같이 정의할 수 있습니다:

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
     * 애플리케이션 서비스를 부트스트랩합니다.
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

위 예시에서 기능에 대한 다음과 같은 규칙을 볼 수 있습니다:

- 모든 내부 팀 멤버는 새로운 API를 사용합니다.
- 트래픽이 많은 고객은 새로운 API를 사용하지 않습니다.
- 이외에는, 1/100 확률로 무작위로 기능이 활성화됩니다.

특정 사용자에 대해 `new-api` 기능이 처음 확인될 때, 클로저의 결과가 저장소 드라이버에 저장됩니다. 같은 사용자에 대해 다음번에 기능이 확인될 때에는 저장소에서 값을 가져오며, 클로저는 호출되지 않습니다.

편의를 위해, 기능 정의가 단순히 Lottery만 반환할 경우 클로저를 생략할 수 있습니다:

    Feature::define('site-redesign', Lottery::odds(1, 1000));

<a name="class-based-features"></a>
### 클래스 기반 기능

Pennant는 클래스 기반의 기능도 정의할 수 있습니다. 클로저 기반 기능과 달리, 클래스 기반 기능은 서비스 프로바이더에 등록할 필요가 없습니다. `pennant:feature` Artisan 명령어로 클래스 기반 기능을 생성합니다. 기본적으로 기능 클래스는 `app/Features` 디렉터리에 생성됩니다:

```shell
php artisan pennant:feature NewApi
```

기능 클래스에서는 `resolve` 메서드 하나만 정의하면 됩니다. 이 메서드는 주어진 스코프에 대해 기능의 초기 값을 반환합니다. 역시 스코프는 보통 현재 인증된 사용자입니다.

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * 기능의 초기 값을 반환합니다.
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

클래스 기반 기능 인스턴스를 수동으로 해석하고 싶다면, `Feature` 파사드의 `instance` 메서드를 사용하면 됩니다:

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]
> 기능 클래스는 [컨테이너](/docs/{{version}}/container)로 해석되기 때문에, 필요하면 생성자에 의존성을 주입할 수 있습니다.

#### 저장되는 기능 이름 커스터마이징

기본적으로 Pennant는 기능 클래스의 전체 클래스명을 저장합니다. 저장되는 기능 이름을 애플리케이션의 내부 구조와 분리하고 싶다면, 클래스에 `$name` 프로퍼티를 지정할 수 있습니다. 이 값이 클래스명 대신 저장됩니다.

```php
<?php

namespace App\Features;

class NewApi
{
    /**
     * 저장될 기능 이름
     *
     * @var string
     */
    public $name = 'new-api';

    // ...
}
```

<a name="checking-features"></a>
## 기능 확인하기

기능이 활성화되어 있는지 확인하려면 `Feature` 파사드의 `active` 메서드를 사용할 수 있습니다. 기본적으로 기능은 현재 인증된 사용자에 대해 확인됩니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * 리소스 목록 표시
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

기본 스코프는 현재 인증된 사용자지만, 다른 사용자 또는 [다른 스코프](#scope)로도 확인할 수 있습니다. 이때는 `Feature` 파사드의 `for` 메서드를 사용하세요:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

Pennant는 다음과 같은 추가적인 편의 메서드도 제공합니다:

```php
// 모든 기능이 활성화되어 있는지 확인
Feature::allAreActive(['new-api', 'site-redesign']);

// 일부 기능이 활성화되어 있는지 확인
Feature::someAreActive(['new-api', 'site-redesign']);

// 비활성화 확인
Feature::inactive('new-api');

// 모든 기능이 비활성화인지 확인
Feature::allAreInactive(['new-api', 'site-redesign']);

// 일부 기능이 비활성화인지 확인
Feature::someAreInactive(['new-api', 'site-redesign']);
```

> [!NOTE]
> Artisan 명령어나 큐 작업 등 HTTP 컨텍스트 외에서 Pennant를 사용할 때는 [스코프를 명확하게 지정](#specifying-the-scope)해야 합니다. 또는 인증된 HTTP 컨텍스트와 인증되지 않은 컨텍스트를 모두 고려할 수 있도록 [기본 스코프를 정의](#default-scope)할 수 있습니다.

<a name="checking-class-based-features"></a>
#### 클래스 기반 기능 확인

클래스 기반 기능의 경우, 확인할 때 클래스명을 전달해야 합니다:

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
     * 리소스 목록 표시
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

`when` 메서드를 사용하면 기능이 활성화되어 있을 때 특정 클로저를 실행할 수 있습니다. 두 번째 클로저를 제공하여, 기능이 비활성화된 경우에 실행되도록 할 수 있습니다:

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
     * 리소스 목록 표시
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

`unless` 메서드는 `when`의 반대로, 기능이 비활성화된 경우 첫 번째 클로저를 실행합니다:

```php
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
### `HasFeatures` 트레이트

Pennant의 `HasFeatures` 트레이트를 User 모델(또는 기능을 보유한 다른 모델)에 추가하면, 모델에서 직접 유연하게 기능 확인을 할 수 있습니다:

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

트레이트를 모델에 추가하면, `features` 메서드를 통해 손쉽게 기능을 확인할 수 있습니다:

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

`features` 메서드를 통해 다양한 편의 메서드에도 접근할 수 있습니다:

```php
// 값 확인
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

Blade에서 기능 확인을 더욱 편리하게 하기 위해, Pennant는 `@feature` 및 `@featureany` 디렉티브를 제공합니다:

```blade
@feature('site-redesign')
    <!-- 'site-redesign' 기능이 활성화됨 -->
@else
    <!-- 'site-redesign' 기능이 비활성화됨 -->
@endfeature

@featureany(['site-redesign', 'beta'])
    <!-- 'site-redesign' 또는 'beta'가 활성화됨 -->
@endfeatureany
```

<a name="middleware"></a>
### 미들웨어

Pennant는 경로가 호출되기 전에 현재 인증된 사용자가 기능에 접근 권한이 있는지 확인하는 [미들웨어](/docs/{{version}}/middleware)도 제공합니다. 라우트에 미들웨어를 할당하고, 접근에 필요한 기능을 지정할 수 있습니다. 지정한 기능 중 하나라도 비활성화되어 있으면 400 Bad Request가 반환됩니다. 여러 기능은 static `using` 메서드에 전달할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### 응답 커스터마이징

비활성화된 기능이 있을 때 미들웨어가 반환하는 응답을 커스터마이징하려면 `EnsureFeaturesAreActive` 미들웨어의 `whenInactive` 메서드를 사용하세요. 일반적으로 이 메서드는 애플리케이션의 서비스 프로바이더의 `boot` 메서드 내에서 호출됩니다:

```php
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

/**
 * 애플리케이션 서비스 초기화
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

일부 상황에서는 기능의 저장된 값을 가져오기 전에 인메모리에서 별도의 체크를 하고 싶을 수 있습니다. 예를 들어, 기능 플래그로 새로운 API를 개발 중이고, 저장된 모든 값을 잃지 않고도 해당 API를 비활성화하고 싶을 때 유용합니다. 버그가 발생하면 내부 팀에게만 기능을 남겨두고, 수정 후 다시 재개할 수도 있습니다.

이때는 [클래스 기반 기능의](#class-based-features) `before` 메서드를 사용할 수 있습니다. 해당 메서드가 있으면 요청 중 해당 기능의 값을 메모리에서 먼저 확인합니다. 반환값이 `null`이 아니면, 저장된 값 대신 이 값을 이번 요청에서 사용합니다:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * 저장된 값을 가져오기 전 항상 메모리에서 먼저 체크
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }
    }

    /**
     * 기능의 초기 값 반환
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

이 기능을 활용하여 전역적으로 기능을 롤아웃하는 스케줄을 구성할 수도 있습니다:

```php
<?php

namespace App\Features;

use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Config;

class NewApi
{
    /**
     * 저장된 값을 가져오기 전 항상 메모리에서 먼저 체크
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

Pennant는 기능을 확인할 때 결과를 메모리에 캐시합니다. `database` 드라이버를 사용할 때는 같은 요청 내에서 같은 기능 플래그를 다시 확인해도 추가적인 데이터베이스 쿼리가 발생하지 않습니다. 즉, 요청 동안 일관된 결과를 보장합니다.

인메모리 캐시를 수동으로 비우고 싶다면 `Feature` 파사드의 `flushCache` 메서드를 사용하세요:

```php
Feature::flushCache();
```

<a name="scope"></a>
## 스코프

<a name="specifying-the-scope"></a>
### 스코프 지정하기

앞서 설명했듯이, 기능은 주로 현재 인증된 사용자에 대해 확인됩니다. 그러나 항상 이 방식이 적합한 것은 아닐 수 있습니다. `Feature` 파사드의 `for` 메서드를 사용하여 원하는 스코프에 대해 기능을 확인할 수 있습니다:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

스코프는 반드시 사용자일 필요는 없습니다. 예를 들어, 새로운 결제 화면을 개별 사용자 대신 팀 전체에 단계적으로 배포하려는 경우 팀을 스코프로 사용할 수 있습니다:

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

위 클로저는 `User`가 아니라 `Team` 모델을 받습니다. 특정 사용자의 팀에 대해 기능이 활성화되어 있는지 확인하려면 해당 팀을 `for` 메서드에 전달하세요:

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### 기본 스코프

Pennant가 기능을 확인할 때 사용할 기본 스코프도 커스터마이징할 수 있습니다. 예를 들어, 모든 기능을 현재 인증된 사용자의 팀 기준으로 확인하려면, 매번 `Feature::for($user->team)`를 호출하는 대신 기본 스코프로 팀을 지정할 수 있습니다. 보통 이 작업은 서비스 프로바이더의 `boot` 메서드에서 수행합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Feature::resolveScopeUsing(fn ($driver) => Auth::user()?->team);

        // ...
    }
}
```

이제 `for` 메서드로 스코프를 명시적으로 제공하지 않아도 기본적으로 현재 인증된 사용자의 팀이 사용됩니다:

```php
Feature::active('billing-v2');

// 다음과 동등하게 동작합니다.

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### Nullable 스코프

기능을 확인할 때 전달한 스코프가 `null`이고, 기능의 정의가 `null` 타입을 지원하지 않는 경우 Pennant는 자동으로 해당 기능의 결과를 `false`로 반환합니다.

따라서, 스코프가 `null`일 가능성이 있고 기능 값 해석기가 호출되길 원한다면, 기능 정의 시 이를 고려해야 합니다. Artisan 명령어나 큐 작업, 인증되지 않은 라우트 등에서는 기본 스코프가 `null`이 될 수 있습니다.

항상 [명시적으로 스코프를 지정](#specifying-the-scope)하지 않는 경우, 스코프의 타입이 null 가능하도록(Nullable) 정의하고 `null` 스코프 값을 처리해야 합니다:

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

Pennant의 기본 제공 `array`와 `database` 드라이버는 모든 PHP 데이터 타입과 Eloquent 모델에 대해 스코프 식별자를 올바르게 저장할 수 있습니다. 하지만, 서드파티 Pennant 드라이버를 사용할 경우 Eloquent 모델이나 커스텀 타입의 식별자를 올바르게 저장하지 못할 수도 있습니다.

이를 위해, 애플리케이션에서 Pennant 스코프로 사용되는 객체에 `FeatureScopeable` 계약을 구현하면 스코프 값을 저장용 포맷으로 지정할 수 있습니다.

예를 들어, 하나의 애플리케이션에서 내장 `database` 드라이버와 서드파티 "Flag Rocket" 드라이버를 모두 사용할 때 "Flag Rocket" 드라이버는 Eloquent 모델을 인식하지 못하고 대신 `FlagRocketUser` 인스턴스를 요구한다고 가정합시다. `FeatureScopeable`의 `toFeatureIdentifier` 메서드를 구현하면 각 드라이버별 저장 방식에 맞게 값을 커스터마이징할 수 있습니다:

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * 드라이버 별로 피처 스코프 식별자로 변환
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

기본적으로 Pennant는 Eloquent 모델과 연결된 기능을 저장할 때 전체 클래스명을 사용합니다. 이미 [Eloquent morph 매핑](/docs/{{version}}/eloquent-relationships#custom-polymorphic-types)를 사용중이라면, Pennant도 morph 매핑을 활용하여 저장되는 기능과 애플리케이션 구조를 분리할 수 있습니다.

서비스 프로바이더에서 morph 매핑을 정의한 후, `Feature` 파사드의 `useMorphMap` 메서드를 호출하세요:

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
## 리치 값 기능

지금까지는 기능이 "활성" 또는 "비활성"인 2진 상태로만 동작한다고 가정했지만, Pennant는 더 풍부한 값을 저장할 수도 있습니다.

예를 들어, "Buy now" 버튼의 새로운 색상 3가지를 테스트하고 싶을 때 true나 false 대신 문자열을 반환할 수 있습니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

`value` 메서드를 사용하여 `purchase-button` 기능의 값을 가져올 수 있습니다:

```php
$color = Feature::value('purchase-button');
```

Pennant Blade 디렉티브를 사용하면 현재 기능 값에 따라 콘텐츠를 조건부로 랜더링하기도 쉽습니다:

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire'가 활성화됨 -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green'이 활성화됨 -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange'가 활성화됨 -->
@endfeature
```

> [!NOTE]
> 리치 값 사용 시, 기능 값이 `false`가 아니기만 하면 "활성"으로 간주합니다.

[조건부 `when`](#conditional-execution) 메서드를 호출할 때 기능의 리치 값이 첫 번째 클로저에 전달됩니다:

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

마찬가지로, 조건부 `unless` 메서드를 사용할 때는 선택적 두 번째 클로저에 기능의 리치 값이 전달됩니다:

```php
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>
## 여러 기능 가져오기

`values` 메서드를 사용하면 특정 스코프에 대해 여러 개의 기능을 한 번에 가져올 수 있습니다:

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

또는, `all` 메서드를 사용하여 특정 스코프에 대해 정의된 모든 기능의 값을 가져올 수도 있습니다:

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

하지만, 클래스 기반 기능은 동적으로 등록되므로 명시적으로 확인되기 전까지는 Pennant에서 인식할 수 없습니다. 즉, 요청 중 한번도 확인되지 않은 클래스 기반 기능은 `all` 결과에 포함되지 않을 수 있습니다.

항상 `all` 메서드에서 기능 클래스가 포함되길 원한다면 Pennant의 기능 자동 탐색 기능을 사용할 수 있습니다. `discover` 메서드를 서비스 프로바이더에서 호출하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 부트스트랩
     */
    public function boot(): void
    {
        Feature::discover();

        // ...
    }
}
```

`discover`는 `app/Features` 디렉터리에 있는 모든 기능 클래스를 등록합니다. 이제 `all` 메서드는 이 클래스들을 요청 중에 확인 여부와 관계없이 결과에 포함시킵니다:

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
## 즉시 로딩(Eager Loading)

Pennant는 한 요청 내에서 확인된 모든 기능을 메모리에 캐시하지만, 성능 문제가 발생할 수 있습니다. 이를 완화하기 위해 기능 값을 미리(즉시) 로딩할 수 있습니다.

예를 들어, 다음과 같이 루프에서 기능을 확인하는 상황을 생각해봅시다:

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

데이터베이스 드라이버를 사용하는 경우, 이 코드는 루프 내 사용자마다 한 번씩 쿼리를 실행하므로 비효율적일 수 있습니다. Pennant의 `load` 메서드를 사용하면 미리 값을 로딩해 이러한 병목을 해결할 수 있습니다:

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

이미 로딩되지 않은 경우에만 값을 로딩하려면 `loadMissing` 메서드를 사용하세요:

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

모든 정의된 기능을 로딩하려면 `loadAll` 메서드를 사용하세요:

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
## 값 업데이트

기능의 값이 처음 결정될 때, 드라이버는 결과를 저장합니다. 이는 사용자가 여러 번 요청을 보내더라도 일관된 경험을 제공하기 위함입니다. 그러나 경우에 따라 저장된 값을 수동으로 업데이트해야 할 수도 있습니다.

이럴 때는 `activate`와 `deactivate` 메서드로 기능을 켜거나(활성화), 끌(비활성화) 수 있습니다:

```php
use Laravel\Pennant\Feature;

// 기본 스코프에서 기능 활성화
Feature::activate('new-api');

// 특정 스코프에서 비활성화
Feature::for($user->team)->deactivate('billing-v2');
```

기능에 리치 값을 저장하려면 `activate`의 두 번째 인자로 값을 넘기면 됩니다:

```php
Feature::activate('purchase-button', 'seafoam-green');
```

기능의 저장된 값을 잊게 하고 싶다면 `forget` 메서드를 사용하세요. 이후 다시 기능이 확인될 때 기능 정의에서 값을 새로 해석합니다:

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### 일괄 업데이트

여러 사용자의 기능 값을 한 번에 대량으로 업데이트하려면 `activateForEveryone`과 `deactivateForEveryone` 메서드를 사용하세요.

예를 들어, 이제 `new-api` 기능의 안정성을 확신하고 구매 버튼 색상도 결정했다면 모든 사용자에 대해 값을 일괄적으로 바꿀 수 있습니다:

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

반대로 모든 사용자에 대해 기능을 비활성화할 수도 있습니다:

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> 이 메서드는 Pennant 저장 드라이버에 저장된 값만 업데이트합니다. 애플리케이션의 기능 정의 자체도 함께 업데이트해야 합니다.

<a name="purging-features"></a>
### 기능 삭제(Purging)

때로는 기능 전체를 저장소에서 완전히 삭제하는 것이 필요할 수 있습니다. 예를 들어, 기능을 애플리케이션에서 제거했거나, 기능 정의를 전면적으로 변경해 모든 사용자에게 새로 적용하고 싶을 때 유용합니다.

`purge` 메서드를 사용해 기능의 모든 저장 값을 삭제할 수 있습니다:

```php
// 단일 기능 삭제
Feature::purge('new-api');

// 여러 기능 삭제
Feature::purge(['new-api', 'purchase-button']);
```

모든 기능을 저장소에서 삭제하려면 인자 없이 `purge`를 호출하세요:

```php
Feature::purge();
```

애플리케이션 배포 파이프라인에서 purge 작업을 자동화하면 좋기 때문에, Pennant는 기능을 저장소에서 삭제하는 `pennant:purge` Artisan 명령어도 제공합니다:

```shell
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

특정 기능 목록에 포함된 기능만 남기고 나머지 모든 기능을 삭제할 수도 있습니다:

```shell
php artisan pennant:purge --except=new-api --except=purchase-button
```

`pennant:purge` 명령어는 `--except-registered` 플래그도 지원합니다. 이 플래그를 사용하면 서비스 프로바이더에서 명시적으로 등록된 기능을 제외하고 모두 삭제할 수 있습니다:

```shell
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## 테스트

기능 플래그와 상호작용하는 코드를 테스트할 때, 테스트 내에서 기능의 반환값을 제어하는 가장 쉬운 방법은 기능을 재정의하는 것입니다. 예를 들어, 아래와 같은 기능이 서비스 프로바이더에 정의되어 있다고 가정합시다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

테스트의 시작 부분에서 기능을 재정의하면 언제나 원하는 값을 반환하게 할 수 있습니다:

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

클래스 기반 기능도 같은 방식으로 테스트할 수 있습니다:

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

기능이 `Lottery` 인스턴스를 반환하는 경우, [테스트 헬퍼](/docs/{{version}}/helpers#testing-lotteries)를 활용할 수 있습니다.

<a name="store-configuration"></a>
#### 저장소(store) 구성

Pennant가 테스트 중 사용할 저장소를 지정하려면, 애플리케이션의 `phpunit.xml` 파일에 `PENNANT_STORE` 환경 변수를 정의하세요:

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

Pennant의 기본 드라이버가 요구사항에 맞지 않는다면, 직접 저장소 드라이버를 구현할 수 있습니다. 커스텀 드라이버는 `Laravel\Pennant\Contracts\Driver` 인터페이스를 구현해야 합니다:

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

이제 Redis 커넥션을 사용하여 각 메서드를 구현하면 됩니다. 구현 예시는 [Pennant 소스 코드](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)의 `DatabaseDriver`를 참고하세요.

> [!NOTE]
> Laravel에는 확장 기능을 위한 디렉토리 구조가 기본으로 제공되지 않으므로, 원하는 곳에 생성하면 됩니다. 예시에서는 `Extensions` 디렉터리에 `RedisFeatureDriver`를 위치시켰습니다.

<a name="registering-the-driver"></a>
#### 드라이버 등록

드라이버 구현이 끝났다면, 이제 Laravel에 등록할 차례입니다. 추가 드라이버를 등록하려면 `Feature` 파사드의 `extend` 메서드를 사용하십시오. 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) `boot` 메서드에서 호출하세요:

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
     * 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 서비스 부트스트랩
     */
    public function boot(): void
    {
        Feature::extend('redis', function (Application $app) {
            return new RedisFeatureDriver($app->make('redis'), $app->make('events'), []);
        });
    }
}
```

이제 `config/pennant.php`에서 `redis` 드라이버를 사용할 수 있습니다:

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

드라이버가 서드파티 피처 플래그 플랫폼을 감싸는 경우, Pennant의 `Feature::define` 대신 플랫폼에서 기능을 정의하게 될 것입니다. 이 경우, 커스텀 드라이버에 `Laravel\Pennant\Contracts\DefinesFeaturesExternally` 인터페이스도 구현하세요:

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;
use Laravel\Pennant\Contracts\DefinesFeaturesExternally;

class FeatureFlagServiceDriver implements Driver, DefinesFeaturesExternally
{
    /**
     * 해당 스코프에 대해 정의된 기능 목록 반환
     */
    public function definedFeaturesForScope(mixed $scope): array {}

    /* ... */
}
```

`definedFeaturesForScope` 메서드는 제공된 스코프에 대해 정의된 기능 이름의 목록을 반환해야 합니다.

<a name="events"></a>
## 이벤트

Pennant는 애플리케이션에서 피처 플래그를 추적할 때 유용한 다양한 이벤트를 발생시킵니다.

### `Laravel\Pennant\Events\FeatureRetrieved`

이 이벤트는 [기능이 확인될 때](#checking-features)마다 발생합니다. 애플리케이션 내에서 피처 플래그 사용량을 추적하거나 메트릭을 생성할 때 유용합니다.

### `Laravel\Pennant\Events\FeatureResolved`

이 이벤트는 특정 스코프에 대해 기능의 값이 처음 해석될 때 발생합니다.

### `Laravel\Pennant\Events\UnknownFeatureResolved`

이 이벤트는 특정 스코프에 대해 알려지지 않은 기능이 최초로 해석될 때 발생합니다. 기능 플래그를 제거했지만 여기저기에 참조가 남아있는 경우 이를 추적하는 데 유용합니다:

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
     * 부트스트랩
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

이 이벤트는 [클래스 기반 기능](#class-based-features)이 요청 중 처음 동적으로 확인될 때 발생합니다.

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

이 이벤트는 [null을 지원하지 않는](#nullable-scope) 기능 정의에 `null` 스코프가 전달될 때 발생합니다.

이런 상황은 문제없이 처리되어 기능은 `false`를 반환합니다. 그러나 기본 graceful 처리 대신 예외 처리 방식으로 동작하고 싶다면, `AppServiceProvider`의 `boot` 메서드에서 다음과 같이 리스너를 등록할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;
use Laravel\Pennant\Events\UnexpectedNullScopeEncountered;

/**
 * 부트스트랩
 */
public function boot(): void
{
    Event::listen(UnexpectedNullScopeEncountered::class, fn () => abort(500));
}
```

### `Laravel\Pennant\Events\FeatureUpdated`

이 이벤트는 스코프에 대해 기능이 업데이트될 때(주로 `activate` 또는 `deactivate` 호출 시) 발생합니다.

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

이 이벤트는 모든 스코프에 대해 기능이 업데이트될 때(주로 `activateForEveryone` 또는 `deactivateForEveryone` 호출 시) 발생합니다.

### `Laravel\Pennant\Events\FeatureDeleted`

이 이벤트는 스코프에 대해 기능이 삭제될 때(주로 `forget` 호출 시) 발생합니다.

### `Laravel\Pennant\Events\FeaturesPurged`

이 이벤트는 특정 기능을 저장소에서 삭제할 때 발생합니다.

### `Laravel\Pennant\Events\AllFeaturesPurged`

이 이벤트는 모든 기능을 저장소에서 삭제할 때 발생합니다.