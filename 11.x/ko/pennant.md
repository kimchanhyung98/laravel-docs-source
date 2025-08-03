# Laravel Pennant

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
- [기능 정의하기](#defining-features)
    - [클래스 기반 기능](#class-based-features)
- [기능 확인하기](#checking-features)
    - [조건부 실행](#conditional-execution)
    - [`HasFeatures` 트레이트](#the-has-features-trait)
    - [Blade 디렉티브](#blade-directive)
    - [미들웨어](#middleware)
    - [기능 검사 가로채기](#intercepting-feature-checks)
    - [인메모리 캐시](#in-memory-cache)
- [스코프](#scope)
    - [스코프 지정하기](#specifying-the-scope)
    - [기본 스코프](#default-scope)
    - [널 가능한 스코프](#nullable-scope)
    - [스코프 식별하기](#identifying-scope)
    - [스코프 직렬화하기](#serializing-scope)
- [풍부한 기능 값](#rich-feature-values)
- [여러 기능 값 가져오기](#retrieving-multiple-features)
- [선행 로딩](#eager-loading)
- [값 업데이트](#updating-values)
    - [대량 업데이트](#bulk-updates)
    - [기능 정리하기](#purging-features)
- [테스트](#testing)
- [사용자 정의 Pennant 드라이버 추가하기](#adding-custom-pennant-drivers)
    - [드라이버 구현하기](#implementing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
    - [외부에서 기능 정의하기](#defining-features-externally)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Pennant](https://github.com/laravel/pennant)는 깔끔하고 경량화된 기능 플래그(feature flag) 패키지입니다. 기능 플래그를 사용하면 점진적으로 새로운 애플리케이션 기능을 자신 있게 배포할 수 있고, A/B 테스트를 진행하며, trunk 기반 개발 전략을 보완하는 등 다양한 활용이 가능합니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 관리자를 사용해 Pennant를 프로젝트에 설치하세요:

```shell
composer require laravel/pennant
```

다음으로 `vendor:publish` Artisan 명령어를 사용해 Pennant의 설정 파일과 마이그레이션 파일을 게시하세요:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

마지막으로 애플리케이션의 데이터베이스 마이그레이션을 실행하세요. 이 과정에서 Pennant가 사용하는 `features` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
## 설정

Pennant의 자산을 게시하면 `config/pennant.php` 경로에 설정 파일이 생성됩니다. 이 파일에서 Pennant가 기능 플래그 값을 저장하는 데 사용할 기본 저장소를 지정할 수 있습니다.

Pennant는 인메모리 배열을 사용하는 `array` 드라이버와, 관계형 데이터베이스에 지속적으로 저장하는 기본 드라이버인 `database` 드라이버를 지원합니다.

<a name="defining-features"></a>
## 기능 정의하기

기능은 `Feature` 파사드의 `define` 메서드를 사용해 정의할 수 있습니다. 기능 이름과 초기 값을 결정하는 클로저를 제공해야 합니다.

일반적으로 기능 정의는 서비스 프로바이더에서 `Feature` 파사드를 통해 이루어집니다. 클로저에는 기능을 검사할 "스코프"(대부분 현재 인증된 사용자)가 전달됩니다. 다음은 새로운 API 기능을 점진적으로 배포하는 예시입니다:

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

위 예시에서 기능의 규칙은 다음과 같습니다:

- 내부 팀 멤버는 모두 새로운 API를 사용합니다.
- 트래픽이 많은 고객은 새로운 API를 사용하지 않습니다.
- 그 외 사용자에게는 1/100 확률로 기능이 활성화됩니다.

처음으로 특정 사용자의 `new-api` 기능을 확인할 때 클로저 결과가 저장됩니다. 이후에는 저장된 값이 재사용되며 클로저는 호출되지 않습니다.

만약 기능 정의가 로터리 확률만 반환한다면 클로저를 생략할 수 있습니다:

```
Feature::define('site-redesign', Lottery::odds(1, 1000));
```

<a name="class-based-features"></a>
### 클래스 기반 기능

Pennant는 클래스 기반 기능 정의도 지원합니다. 클로저 기반과 달리 서비스 프로바이더에 등록할 필요가 없습니다. 클래스 기반 기능을 생성하려면 `pennant:feature` Artisan 명령어를 사용합니다. 기본적으로 `app/Features` 디렉토리에 생성됩니다:

```shell
php artisan pennant:feature NewApi
```

기능 클래스에서는 `resolve` 메서드만 정의하면 됩니다. 이 메서드는 주어진 스코프(대게 현재 인증된 사용자)를 받아 초기 값을 반환합니다:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * 기능 초기 값 해결.
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

클래스 기반 기능 인스턴스를 직접 해결하려면 `Feature` 파사드의 `instance` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]
> 기능 클래스는 [컨테이너](/docs/11.x/container)를 통해 해결되므로, 필요할 경우 클래스 생성자에 의존성을 주입할 수 있습니다.

#### 저장된 기능 이름 커스터마이징

기본적으로 Pennant는 기능 클래스의 전체 클래스 이름을 저장합니다. 그러나 저장된 이름을 애플리케이션 내부 구조와 분리하고 싶다면, 클래스 내에 `$name` 속성을 정의할 수 있습니다:

```php
<?php

namespace App\Features;

class NewApi
{
    /**
     * 저장될 기능 이름.
     *
     * @var string
     */
    public $name = 'new-api';

    // ...
}
```

<a name="checking-features"></a>
## 기능 확인하기

기능이 활성화되었는지 확인하려면 `Feature` 파사드의 `active` 메서드를 사용하세요. 기본적으로 현재 인증된 사용자에 대해 확인합니다:

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

기능은 기본적으로 인증된 사용자 스코프로 확인되지만, 다른 사용자나 스코프에 대해 확인할 수도 있습니다. 이를 위해 `Feature` 파사드의 `for` 메서드를 사용하세요:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

다음은 기능 활성 여부 확인에 도움이 되는 추가 메서드들입니다:

```php
// 주어진 모든 기능이 활성화되었는지 확인...
Feature::allAreActive(['new-api', 'site-redesign']);

// 주어진 기능 중 하나라도 활성화되었는지 확인...
Feature::someAreActive(['new-api', 'site-redesign']);

// 기능이 비활성화되었는지 확인...
Feature::inactive('new-api');

// 주어진 모든 기능이 비활성화되었는지 확인...
Feature::allAreInactive(['new-api', 'site-redesign']);

// 주어진 기능 중 하나라도 비활성화되었는지 확인...
Feature::someAreInactive(['new-api', 'site-redesign']);
```

> [!NOTE]
> Artisan 명령어나 큐 작업과 같이 HTTP 컨텍스트 외부에서 Pennant를 사용할 때는 일반적으로 [기능 스코프를 명시적으로 지정](#specifying-the-scope)하는 것이 좋습니다. 또는 [기본 스코프](#default-scope)를 설정해 인증된 HTTP 상황과 비인증 상황을 모두 다룰 수 있습니다.

<a name="checking-class-based-features"></a>
#### 클래스 기반 기능 확인

클래스 기반 기능을 확인할 때는 클래스명을 인자로 제공합니다:

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

`when` 메서드를 사용하면 기능이 활성화된 경우 특정 클로저를 실행할 수 있습니다. 비활성화 시 실행할 두 번째 클로저도 지정할 수 있습니다:

```
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

`unless` 메서드는 `when`의 반대 역할을 하며 기능이 비활성화된 경우 첫 번째 클로저를 실행합니다:

```
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
### `HasFeatures` 트레이트

Pennant의 `HasFeatures` 트레이트를 애플리케이션의 `User` 모델(또는 기능이 있는 모델)에 추가하면 모델에서 바로 기능을 쉽게 확인할 수 있습니다:

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

트레이트를 추가한 후에는 `features` 메서드를 통해 간편하게 기능을 확인할 수 있습니다:

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

이 외에도 `features` 메서드는 다양한 유용한 기능을 제공합니다:

```php
// 값 가져오기...
$value = $user->features()->value('purchase-button');
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

Blade 내에서 편리하게 기능을 확인할 수 있도록 Pennant는 `@feature` 및 `@featureany` 디렉티브를 제공합니다:

```blade
@feature('site-redesign')
    <!-- 'site-redesign' 활성화됨 -->
@else
    <!-- 'site-redesign' 비활성화됨 -->
@endfeature

@featureany(['site-redesign', 'beta'])
    <!-- 'site-redesign' 또는 'beta' 중 하나 이상 활성화됨 -->
@endfeatureany
```

<a name="middleware"></a>
### 미들웨어

Pennant는 특정 라우트 접근 전에 현재 인증된 사용자가 해당 기능에 접근 권한이 있는지 확인하는 [미들웨어](/docs/11.x/middleware)를 포함합니다. 이 미들웨어를 라우트에 할당하고 접근에 필요한 기능 목록을 지정할 수 있습니다. 만약 사용자가 기능 중 하나라도 비활성화되어 있으면 `400 Bad Request` 응답을 반환합니다. 여러 기능은 정적 `using` 메서드에 인자로 전달됩니다:

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### 응답 커스터마이징

비활성 기능이 있을 때 미들웨어가 반환하는 응답을 커스터마이징하려면, 애플리케이션 서비스 프로바이더의 `boot` 메서드 내에서 `EnsureFeaturesAreActive` 미들웨어의 `whenInactive` 메서드를 호출하면 됩니다:

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
### 기능 검사 가로채기

때로는 저장된 값 대신 메모리 상에서 기능 확인을 먼저 수행하는 것이 유용할 수 있습니다. 예를 들어, 새로운 API 기능에 버그가 발생했을 때 저장된 값을 유지하되 내부 팀 멤버를 제외한 모든 사용자에게 기능을 비활성화할 수 있습니다.

이것은 [클래스 기반 기능](#class-based-features)의 `before` 메서드를 통해 가능합니다. `before` 메서드가 정의되어 있으면, 저장된 값을 가져오기 전에 항상 호출됩니다. `null`이 아닌 값을 반환하면 해당 값이 요청 동안 저장된 값 대신 사용됩니다:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * 저장된 값 조회 전에 항상 메모리 상 검사 실행.
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }
    }

    /**
     * 기능 초기 값 해결.
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

이 기능을 사용해 기능 플래그 뒤에 있던 기능을 전역적으로 단계적으로 활성화할 수도 있습니다:

```php
<?php

namespace App\Features;

use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Config;

class NewApi
{
    /**
     * 저장된 값 조회 전에 항상 메모리 상 검사 실행.
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

기능을 확인할 때 Pennant는 결과값을 인메모리 캐시에 저장합니다. `database` 드라이버를 사용하는 경우, 같은 요청 동안 같은 기능을 여러 번 확인해도 추가 데이터베이스 쿼리가 발생하지 않아 일관된 결과를 보장합니다.

인메모리 캐시를 수동으로 비우려면 `Feature` 파사드의 `flushCache` 메서드를 사용하세요:

```
Feature::flushCache();
```

<a name="scope"></a>
## 스코프

<a name="specifying-the-scope"></a>
### 스코프 지정하기

기본적으로 기능 확인은 현재 인증된 사용자에 대해 수행됩니다. 하지만 상황에 따라 다른 스코프를 지정할 수 있습니다. `Feature` 파사드의 `for` 메서드를 사용해 원하는 스코프를 지정하세요:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

예를 들어 개별 사용자가 아닌 팀 단위로 새로운 결제 경험을 롤아웃하고 싶을 때, 스코프는 `User`가 아니라 `Team` 모델이 됩니다. 오래된 팀은 새로운 팀보다 느린 롤아웃을 경험하도록 할 수도 있습니다:

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

이 기능이 사용자의 팀에 대해 활성화되었는지 확인하려면 다음과 같이 `for` 메서드에 팀 인스턴스를 전달합니다:

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### 기본 스코프

Pennant가 기능을 확인할 때 사용하는 기본 스코프를 커스터마이징할 수 있습니다. 예를 들어 모든 기능을 현재 인증된 사용자의 팀에 대해 확인하려 한다면, 매번 `Feature::for($user->team)`을 호출하지 않고 기본 스코프로 설정할 수 있습니다. 보통 서비스 프로바이더에서 설정합니다:

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

이제 명시적으로 스코프를 지정하지 않으면 기본 스코프인 인증된 사용자의 팀이 사용됩니다:

```php
Feature::active('billing-v2');

// 다음과 동일한 효과입니다...

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### 널 가능한 스코프

기능 확인 시 전달된 스코프가 `null`이고, 기능 정의가 널 값을 허용하지 않는다면 Pennant는 자동으로 `false`를 반환합니다.

만약 스코프가 `null`일 수 있는 상황(예: Artisan 명령어, 큐 작업, 비인증 라우트)에서도 기능의 값 해석기를 호출하고 싶다면, 기능 정의의 스코프 타입을 널 가능(nullable)하게 지정하고 이를 처리해야 합니다:

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

Pennant의 기본 `array` 및 `database` 드라이버는 PHP 내장 타입과 Eloquent 모델의 스코프 식별자를 저장할 수 있습니다. 그러나 타사 Pennant 드라이버를 사용하는 경우, Eloquent 모델 같은 스코프 식별자 저장 방식을 모를 수 있습니다.

이럴 때는 애플리케이션 내 스코프 객체에 `FeatureScopeable` 계약을 구현해 드라이버별로 저장될 식별자 값을 커스터마이징할 수 있습니다.

예를 들어, 기본 `database` 드라이버와 서드파티 'Flag Rocket' 드라이버를 같이 쓰는 경우, 'Flag Rocket' 드라이버는 Eloquent 모델 대신 `FlagRocketUser` 인스턴스를 요구할 수 있습니다. 이떄 다음처럼 구현할 수 있습니다:

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * 주어진 드라이버에 맞는 기능 스코프 식별자로 객체 변환.
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
### 스코프 직렬화하기

기본적으로 Pennant는 Eloquent 모델과 연관된 기능을 저장할 때 전체 클래스 이름을 사용합니다. 이미 [Eloquent morph map](/docs/11.x/eloquent-relationships#custom-polymorphic-types)을 사용하고 있다면, Pennant도 morph map을 사용하도록 설정할 수 있습니다.

서비스 프로바이더에서 morph map을 정의한 뒤 `Feature` 파사드의 `useMorphMap` 메서드를 호출하면 됩니다:

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
## 풍부한 기능 값

지금까지 기능을 활성/비활성의 이진 상태로 설명했지만, Pennant는 풍부한 값도 저장할 수 있습니다.

예를 들어 "구매하기" 버튼의 세 가지 새로운 색상을 테스트하고 싶을 때, 기능 정의에서 `true`/`false` 대신 문자열을 반환할 수 있습니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

`purchase-button` 기능의 값을 가져오려면 `value` 메서드를 사용하세요:

```php
$color = Feature::value('purchase-button');
```

Blade 디렉티브도 풍부한 기능 값에 맞춰 조건부 렌더링을 쉽게 해줍니다:

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire' 활성화됨 -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green' 활성화됨 -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange' 활성화됨 -->
@endfeature
```

> [!NOTE]
> 풍부한 값을 사용할 때, 기능 값이 `false`가 아닌 모든 경우 기능이 "활성화"된 것으로 간주됩니다.

조건부 `when` 메서드를 호출할 때는 기능의 풍부한 값이 첫 번째 클로저의 인자로 제공됩니다:

```
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

마찬가지로 `unless` 메서드도 두 번째 옵션 클로저로 기능의 풍부한 값을 전달합니다:

```
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>
## 여러 기능 값 가져오기

`values` 메서드로 주어진 스코프에 대해 여러 기능 값을 한꺼번에 가져올 수 있습니다:

```php
Feature::values(['billing-v2', 'purchase-button']);

// 결과 예시
// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

또는 `all` 메서드를 사용해 주어진 스코프의 모든 정의된 기능 값을 가져올 수 있습니다:

```php
Feature::all();

// 결과 예시
// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

단, 클래스 기반 기능은 동적으로 등록되므로 현재 요청에서 명시적으로 확인하지 않으면 `all` 메서드 결과에 포함되지 않습니다.

`all` 호출 시 클래스 기반 기능도 항상 포함하려면 Pennant의 기능 검색 기능을 활용하세요. 서비스 프로바이더에서 `discover` 메서드를 호출하면 됩니다:

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

이제 `all` 호출 시 `app/Features` 디렉토리의 기능 클래스도 항상 결과에 포함됩니다:

```php
Feature::all();

// 예시 결과
// [
//     'App\Features\NewApi' => true,
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

<a name="eager-loading"></a>
## 선행 로딩

Pennant는 요청 동안 기능 결과를 인메모리 캐시에 저장하지만, 반복적인 기능 확인이 성능 문제를 일으킬 수 있습니다. 이를 완화하기 위해 Pennant는 기능 값을 선행 로딩할 수 있는 기능을 제공합니다.

예를 들어, 반복문 내에서 기능 활성 여부를 검사한다면:

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

`database` 드라이버일 경우 사용자 수만큼 쿼리가 발생합니다. `load` 메서드를 사용해 컬렉션 대상 기능 값을 미리 로딩하면 쿼리를 줄일 수 있습니다:

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

이미 로딩된 기능만 불러오려면 `loadMissing` 메서드를 사용하세요:

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

모든 정의된 기능을 선행 로딩하려면 `loadAll` 메서드를 사용하세요:

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
## 값 업데이트

기능 값이 처음 해결되면 Pennant 드라이버가 값을 스토리지에 저장해 사용자 경험 일관성을 보장합니다. 하지만 때로는 기능의 저장된 값을 수동으로 업데이트할 필요가 있습니다.

`activate`와 `deactivate` 메서드를 사용해 기능을 켜거나 끌 수 있습니다:

```php
use Laravel\Pennant\Feature;

// 기본 스코프에서 기능 활성화...
Feature::activate('new-api');

// 특정 스코프에서 기능 비활성화...
Feature::for($user->team)->deactivate('billing-v2');
```

또한 `activate` 메서드의 두 번째 인자로 풍부한 값을 직접 설정할 수도 있습니다:

```php
Feature::activate('purchase-button', 'seafoam-green');
```

기능 저장 값을 삭제하고 싶다면 `forget` 메서드를 사용하세요. 이후 기능을 확인하면 다시 정의된 클로저가 호출되어 값을 새로 결정합니다:

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### 대량 업데이트

`activateForEveryone`과 `deactivateForEveryone` 메서드를 사용하면 모든 사용자에 대해 기능값을 일괄 업데이트할 수 있습니다.

예를 들어 `new-api` 기능이 안정화되어 '구매 버튼' 색상도 확정되었다면 다음처럼 모든 사용자 값을 한꺼번에 업데이트할 수 있습니다:

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

또는 기능을 모든 사용자에 대해 끌 수도 있습니다:

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> 이는 Pennant 저장 드라이버에 저장된 값만 수정합니다. 애플리케이션 내 기능 정의도 별도로 업데이트해야 합니다.

<a name="purging-features"></a>
### 기능 정리하기

기능을 애플리케이션에서 제거하거나 정의를 변경했을 때 기존 저장된 값을 완전히 삭제하려면 `purge` 메서드를 사용하세요:

```php
// 단일 기능 정리...
Feature::purge('new-api');

// 복수 기능 정리...
Feature::purge(['new-api', 'purchase-button']);
```

모든 기능 값을 정리하려면 `purge` 메서드를 인자 없이 호출하면 됩니다:

```php
Feature::purge();
```

배포 파이프라인에서 기능 정리를 자주 한다면, Pennant에서 제공하는 `pennant:purge` Artisan 명령어를 사용할 수 있습니다:

```sh
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

특정 기능을 제외하고 모두 정리하고 싶다면 `--except` 옵션을 사용하세요. 다음은 'new-api'와 'purchase-button'을 제외하고 정리하는 예시입니다:

```sh
php artisan pennant:purge --except=new-api --except=purchase-button
```

그리고 `--except-registered` 플래그를 사용하면, 서비스 프로바이더에 명시적으로 등록된 기능을 제외한 모든 기능을 정리합니다:

```sh
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## 테스트

기능 플래그를 사용하는 코드를 테스트할 때 가장 쉽게 제어하는 방법은 테스트 시작 시 해당 기능을 재정의하는 것입니다.

예를 들어, 서비스 프로바이더에 아래와 같이 기능이 정의되어 있더라도:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

테스트에서는 다음처럼 항상 특정 값을 반환하도록 재정의할 수 있습니다:

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

`Lottery` 인스턴스를 반환하는 기능인 경우, [테스트 헬퍼들](/docs/11.x/helpers#testing-lotteries)을 활용하세요.

<a name="store-configuration"></a>
#### 저장소 설정

테스트 중 Pennant가 사용할 저장소는 `phpunit.xml`에서 `PENNANT_STORE` 환경 변수를 설정해 지정할 수 있습니다:

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
## 사용자 정의 Pennant 드라이버 추가하기

<a name="implementing-the-driver"></a>
#### 드라이버 구현하기

Pennant 내장 드라이버가 애플리케이션 요구에 맞지 않으면 직접 드라이버를 구현할 수 있습니다. 사용자 정의 드라이버는 `Laravel\Pennant\Contracts\Driver` 인터페이스를 구현해야 합니다:

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

메서드 구현 예시는 [Pennant 소스](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)의 `DatabaseDriver`를 참고하세요.

> [!NOTE]
> Laravel에 확장 디렉토리가 따로 지정되어 있지 않으므로 자유롭게 원하는 위치에 클래스를 배치하세요. 예시에서는 `Extensions` 디렉토리를 사용했습니다.

<a name="registering-the-driver"></a>
#### 드라이버 등록하기

구현한 드라이버를 Laravel에 등록하려면, `Feature` 파사드의 `extend` 메서드를 호출합니다. 보통 서비스 프로바이더의 `boot` 메서드에 작성합니다:

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

등록 후에는 `config/pennant.php` 설정에서 `redis` 드라이버를 사용할 수 있습니다:

```
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

서드파티 기능 플래그 플랫폼을 래핑하는 드라이버라면, Pennant의 `Feature::define` 대신 외부 플랫폼에 기능 정의가 있을 것입니다. 이 경우 사용자 정의 드라이버는 `Laravel\Pennant\Contracts\DefinesFeaturesExternally` 인터페이스도 구현해야 합니다:

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;
use Laravel\Pennant\Contracts\DefinesFeaturesExternally;

class FeatureFlagServiceDriver implements Driver, DefinesFeaturesExternally
{
    /**
     * 주어진 스코프에 정의된 기능 목록 반환.
     */
    public function definedFeaturesForScope(mixed $scope): array {}

    /* ... */
}
```

`definedFeaturesForScope` 메서드는 제공된 스코프에 대해 정의된 기능 이름 배열을 반환해야 합니다.

<a name="events"></a>
## 이벤트

Pennant는 애플리케이션 전반에서 기능 플래그를 추적하는 데 유용한 다양한 이벤트를 발생시킵니다.

### `Laravel\Pennant\Events\FeatureRetrieved`

기능이 [확인될 때](#checking-features)마다 발생합니다. 기능 사용 통계 수집 등에 유용합니다.

### `Laravel\Pennant\Events\FeatureResolved`

특정 스코프에 대해 기능 값이 처음으로 해결될 때 발생합니다.

### `Laravel\Pennant\Events\UnknownFeatureResolved`

알려지지 않은 기능이 특정 스코프에 대해 처음 해결될 때 발생합니다. 제거하려던 기능에 남은 참조가 있을 때 유용합니다:

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

클래스 기반 기능이 현재 요청에서 처음 동적으로 확인될 때 발생합니다.

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

널 값을 지원하지 않는 기능 정의에 `null` 스코프가 전달될 때 발생합니다.

이 상황은 기본적으로 정상 처리되어 기능 값은 `false`가 되지만, 이 기본 동작을 원하지 않으면 애플리케이션의 `AppServiceProvider` `boot` 메서드에서 이벤트 리스너를 등록할 수 있습니다:

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

주어진 스코프에 대해 `activate` 또는 `deactivate` 호출 등으로 기능 값을 변경할 때 발생합니다.

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

모든 스코프에 대해 기능 값을 변경할 때 (`activateForEveryone`, `deactivateForEveryone`) 발생합니다.

### `Laravel\Pennant\Events\FeatureDeleted`

특정 스코프에서 기능 값을 삭제할 때 (`forget`) 발생합니다.

### `Laravel\Pennant\Events\FeaturesPurged`

여러 기능을 정리할 때 발생합니다.

### `Laravel\Pennant\Events\AllFeaturesPurged`

모든 기능을 정리할 때 발생합니다.