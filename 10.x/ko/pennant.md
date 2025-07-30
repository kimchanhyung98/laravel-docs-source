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
    - [인-메모리 캐시](#in-memory-cache)
- [스코프](#scope)
    - [스코프 지정하기](#specifying-the-scope)
    - [기본 스코프](#default-scope)
    - [널러블 스코프](#nullable-scope)
    - [스코프 식별하기](#identifying-scope)
    - [스코프 직렬화하기](#serializing-scope)
- [풍부한 기능 값](#rich-feature-values)
- [여러 기능 값 조회하기](#retrieving-multiple-features)
- [지연 로딩](#eager-loading)
- [값 업데이트하기](#updating-values)
    - [일괄 업데이트](#bulk-updates)
    - [기능 정리하기](#purging-features)
- [테스트](#testing)
- [커스텀 Pennant 드라이버 추가하기](#adding-custom-pennant-drivers)
    - [드라이버 구현하기](#implementing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pennant](https://github.com/laravel/pennant)는 불필요한 복잡함 없이 가볍고 단순한 기능 플래그(feature flag) 패키지입니다. 기능 플래그를 사용하면 새로운 애플리케이션 기능을 점진적으로 배포할 수 있고, A/B 테스트를 수행하거나 trunk 기반 개발 전략과 결합하는 등 다양한 활용이 가능합니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 사용해 Pennant를 프로젝트에 설치하세요:

```shell
composer require laravel/pennant
```

다음으로, Artisan의 `vendor:publish` 명령어로 Pennant의 설정 및 마이그레이션 파일을 공개합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행하세요. 이 과정에서 Pennant가 `database` 드라이버에서 사용하는 `features` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
## 설정 (Configuration)

Pennant의 리소스를 공개한 뒤에는 `config/pennant.php` 위치에 설정 파일이 생성됩니다. 이 설정 파일에서 기능 플래그 값을 저장하는 기본 저장소 방식을 지정할 수 있습니다.

Pennant는 `array` 드라이버를 통해 메모리 내에 기능 값을 저장하는 방법을 지원하며, 기본값은 관계형 데이터베이스를 활용하는 `database` 드라이버입니다. `database` 드라이버는 기능 값을 영구적으로 저장합니다.

<a name="defining-features"></a>
## 기능 정의하기 (Defining Features)

기능을 정의할 때는 `Feature` 파사드를 통해 제공하는 `define` 메서드를 사용합니다. 기능 이름과 초기 값을 판단할 클로저를 함께 전달해야 합니다.

보통 기능은 서비스 프로바이더 내에서 `Feature` 파사드를 활용해 정의합니다. 클로저에는 기능 확인 시 사용할 "스코프"가 전달됩니다. 일반적으로는 현재 인증된 사용자가 스코프입니다. 예를 들어, 새로운 API를 사용자에게 점진적으로 배포하는 기능을 정의하는 코드 예시는 다음과 같습니다:

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

위 정의에서 규칙은 다음과 같습니다:

- 내부 팀원은 모두 새 API를 사용합니다.
- 트래픽이 많은 고객은 새 API를 사용하지 않습니다.
- 그 외 사용자는 1/100 확률로 새 API가 활성화됩니다.

한 번 해당 사용자에 대해 `new-api` 기능이 확인되면, 클로저의 반환 결과가 저장소에 캐시됩니다. 이후 같은 사용자가 다시 기능을 확인할 때는 저장된 값이 사용되고 클로저는 호출되지 않습니다.

편의를 위해, 기능 정의가 복권형 반환(lottery)만 하는 경우 클로저를 생략할 수도 있습니다:

```
Feature::define('site-redesign', Lottery::odds(1, 1000));
```

<a name="class-based-features"></a>
### 클래스 기반 기능

Pennant는 클래스 기반 기능도 지원합니다. 클로저 기반 기능과 달리, 클래스 기반 기능은 서비스 프로바이더에 따로 등록할 필요가 없습니다. Artisan 명령어 `pennant:feature`를 사용해 기능 클래스를 생성할 수 있으며, 기본 위치는 애플리케이션의 `app/Features` 디렉터리입니다:

```shell
php artisan pennant:feature NewApi
```

기능 클래스 작성 시에는 `resolve` 메서드를 정의하면 되며, 이 메서드에서 특정 스코프(대개 현재 인증된 사용자)에 대한 기능 활성 여부를 판별해 반환합니다:

```php
<?php

namespace App\Features;

use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * 기능의 초기 값을 해석합니다.
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

> [!NOTE]
> 기능 클래스는 [컨테이너](/docs/10.x/container)를 통해 해석되므로, 필요 시 생성자에 의존성 주입이 가능합니다.

#### 저장되는 기능 이름 커스터마이징

기본적으로 Pennant는 기능 클래스의 완전한 네임스페이스 포함(class fully qualified) 이름을 저장합니다. 애플리케이션 내부 구조와 저장된 이름을 분리하고 싶다면, 클래스에 `$name` 속성을 정의할 수 있으며 이 값이 저장 이름으로 사용됩니다:

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
## 기능 확인하기 (Checking Features)

기능이 활성화되어 있는지 알고 싶으면, `Feature` 파사드의 `active` 메서드를 사용합니다. 기본적으로 기능은 현재 인증된 사용자에 대해 확인됩니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * 리소스 목록을 표시합니다.
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

기본값은 현재 인증된 사용자여도, `for` 메서드를 활용해 다른 사용자 또는 [다른 스코프](#scope)에 대해 기능을 확인할 수 있습니다:

```php
return Feature::for($user)->active('new-api')
        ? $this->resolveNewApiResponse($request)
        : $this->resolveLegacyApiResponse($request);
```

또한 Pennant는 기능 활성 상태 판단에 유용한 여러 편의 메서드를 제공합니다:

```php
// 주어진 모든 기능이 활성 상태인지 확인...
Feature::allAreActive(['new-api', 'site-redesign']);

// 주어진 기능 중 하나라도 활성 상태인지 확인...
Feature::someAreActive(['new-api', 'site-redesign']);

// 기능이 비활성 상태인지 확인...
Feature::inactive('new-api');

// 주어진 모든 기능이 비활성 상태인지 확인...
Feature::allAreInactive(['new-api', 'site-redesign']);

// 주어진 기능 중 하나라도 비활성 상태인지 확인...
Feature::someAreInactive(['new-api', 'site-redesign']);
```

> [!NOTE]
> Artisan 명령어나 큐된 작업처럼 HTTP 컨텍스트 외에서 Pennant를 사용할 때는 보통 [기능 스코프를 명시적으로 지정](#specifying-the-scope)하는 것이 좋습니다. 또는 [기본 스코프](#default-scope)를 설정해 인증된 HTTP 컨텍스트와 비인증 컨텍스트를 모두 커버할 수 있습니다.

<a name="checking-class-based-features"></a>
#### 클래스 기반 기능 확인하기

클래스 기반 기능을 확인할 때는, 기능 이름 대신 클래스명을 전달하세요:

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
     * 리소스 목록을 표시합니다.
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
### 조건부 실행 (Conditional Execution)

`when` 메서드를 사용하면, 기능이 활성 상태일 때만 특정 클로저를 실행할 수 있습니다. 두 번째 클로저를 전달하면 기능이 비활성 상태일 때 해당 클로저가 실행됩니다:

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
     * 리소스 목록을 표시합니다.
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

`unless` 메서드는 `when`과 반대로, 기능이 비활성 상태일 때 첫 번째 클로저를 실행합니다:

```
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
### `HasFeatures` 트레이트

Pennant의 `HasFeatures` 트레이트를 사용자 모델(또는 기능이 적용되는 다른 모델)에 추가하면, 모델 인스턴스에서 편리하게 기능을 확인할 수 있습니다:

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

트레이트를 추가한 뒤에는 `features` 메서드를 호출해 기능 상태를 손쉽게 확인할 수 있습니다:

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

`features` 메서드는 여러 편의 메서드도 제공합니다:

```php
// 값 조회...
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

Blade에서 기능 확인을 편리하게 하도록, Pennant는 `@feature` 디렉티브를 제공합니다:

```blade
@feature('site-redesign')
    <!-- 'site-redesign' 기능이 활성화된 경우 -->
@else
    <!-- 'site-redesign' 기능이 비활성화된 경우 -->
@endfeature
```

<a name="middleware"></a>
### 미들웨어

Pennant는 라우트가 실행되기 전에 현재 인증된 사용자가 해당 기능 접근 권한이 있는지 검증하는 [미들웨어](/docs/10.x/middleware)를 제공합니다. 라우트에 미들웨어를 적용하고 필요한 기능을 지정하면, 해당 기능이 비활성 상태일 경우 `400 Bad Request` 응답이 반환됩니다. 여러 기능을 `using` 메서드에 인수로 전달할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### 응답 커스터마이징

미들웨어에 의해 비활성 기능으로 응답이 반환될 때, 커스텀 응답을 지정하려면 `EnsureFeaturesAreActive` 미들웨어가 제공하는 `whenInactive` 메서드를 사용할 수 있습니다. 보통 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 설정합니다:

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

<a name="in-memory-cache"></a>
### 인-메모리 캐시

기능을 확인할 때 Pennant는 요청 중 발생하는 중복 조회 방지를 위해 결과를 인-메모리 캐시에 저장합니다. `database` 드라이버를 사용할 경우, 한 요청 중 같은 기능 조사를 반복해도 추가 쿼리가 발생하지 않습니다. 또한, 요청 내내 일관된 결과를 보장할 수 있습니다.

인-메모리 캐시를 수동으로 비우려면 `Feature` 파사드의 `flushCache` 메서드를 사용하세요:

```
Feature::flushCache();
```

<a name="scope"></a>
## 스코프 (Scope)

<a name="specifying-the-scope"></a>
### 스코프 지정하기

앞서 말했듯, 기능은 기본적으로 현재 인증된 사용자에 대해 확인됩니다. 하지만 때로는 다른 스코프가 필요할 수 있습니다. 이때는 `Feature` 파사드의 `for` 메서드로 원하는 스코프를 명시하세요:

```php
return Feature::for($user)->active('new-api')
        ? $this->resolveNewApiResponse($request)
        : $this->resolveLegacyApiResponse($request);
```

예를 들어, 개인 단위가 아닌 팀 단위로 기능을 롤아웃하는 새 결제 경험을 만든 상황을 상상해보세요. 오래된 팀에 대한 롤아웃은 더 느리게 해야 할 수도 있습니다. 이때는 아래처럼 팀 모델을 스코프로 사용하는 기능 정의를 할 수 있습니다:

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

이 클로저는 `User`가 아니라 `Team` 모델을 기대합니다. 특정 사용자의 팀에 대해 이 기능이 활성인지 확인하려면, `Feature::for`에 팀을 전달합니다:

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect()->to('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### 기본 스코프

Pennant가 기능을 확인할 때 사용할 기본 스코프를 커스터마이징 할 수도 있습니다. 예를 들어, 모든 기능 확인 시 기본적으로 현재 인증 사용자의 팀을 스코프로 사용하도록 할 수 있습니다. 매번 `Feature::for($user->team)`를 호출하지 않고, 앱의 서비스 프로바이더에서 기본 스코프를 지정하세요:

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

이제 `for` 메서드로 스코프를 명시하지 않으면, 기본적으로 현재 인증 사용자의 팀으로 기능 확인이 수행됩니다:

```php
Feature::active('billing-v2');

// 다음과 동일한 동작:

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### 널러블 스코프

기능 확인 시 전달하는 스코프가 `null`이고, 기능 정의가 널러블 타입 또는 널 포함 유니온 타입으로 대응하지 않으면, Pennant는 기능 결과값으로 자동으로 `false`를 반환합니다.

Artisan 명령어, 큐 작업, 비인증 라우트 등에서 기능을 확인할 때는 보통 인증된 사용자가 없기 때문에 기본 스코프가 `null`이 될 수 있습니다. 이 경우 기능 정의에서 `null`을 처리할 수 있게 타입에 `null`을 포함시키고 로직을 작성해야만 기능 값 계산이 정상 수행됩니다.

예시:

```php
use App\Models\User;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

// 기존 정의 (null 대응 X) :
// Feature::define('new-api', fn (User $user) => match (true) {

// 권장 정의 (null 대응 O):
Feature::define('new-api', fn (User|null $user) => match (true) {
    $user === null => true,
    $user->isInternalTeamMember() => true,
    $user->isHighTrafficCustomer() => false,
    default => Lottery::odds(1 / 100),
});
```

<a name="identifying-scope"></a>
### 스코프 식별하기

Pennant가 기본 제공하는 `array` 및 `database` 드라이버는 대부분 PHP 데이터 타입 및 Eloquent 모델에 대한 스코프 식별자를 올바르게 저장할 수 있습니다. 하지만 타사 Pennant 드라이버는 Eloquent 모델 등 애플리케이션 커스텀 타입의 스코프 식별을 처리하지 못할 수 있습니다.

이때 Pennant가 제공하는 `FeatureScopeable` 계약을 애플리케이션 내 기능 스코프로 사용할 객체에 구현하여, 드라이버별로 저장할 스코프 식별자 값을 맞춤 설정 가능하게 할 수 있습니다.

예를 들어, 내장 `database` 드라이버와 타사 "Flag Rocket" 드라이버를 함께 쓰는 경우, "Flag Rocket" 드라이버는 Eloquent 모델을 바로 저장할 수 없고 `FlagRocketUser` 인스턴스를 요구합니다. 이때 `FeatureScopeable` 계약의 `toFeatureIdentifier` 메서드로 드라이버별 식별자 반환 방식을 지정하는 예시는 다음과 같습니다:

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * 드라이버에 맞게 객체를 기능 스코프 식별자로 변환합니다.
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

기본적으로 Pennant는 Eloquent 모델과 연관된 기능을 저장할 때 완전한 네임스페이스 포함 클래스명을 사용합니다. 애플리케이션에서 이미 [Eloquent morph map](/docs/10.x/eloquent-relationships#custom-polymorphic-types)을 쓰고 있다면, Pennant가 저장 이름과 내부 구조 분리를 위해 morph map을 사용하도록 할 수 있습니다.

애플리케이션 서비스 프로바이더에서 morph map을 정의한 뒤, `Feature` 파사드의 `useMorphMap` 메서드를 호출하면 됩니다:

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
## 풍부한 기능 값 (Rich Feature Values)

앞서 예시는 기능이 활성/비활성과 같은 이진 상태만 다루었지만, Pennant는 더 풍부한 값도 저장할 수 있습니다.

예를 들어, 애플리케이션의 "구매하기" 버튼 색상 A/B 테스트에서 `true`/`false` 대신 문자열 값을 반환할 수 있습니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

값은 `value` 메서드로 조회 가능합니다:

```php
$color = Feature::value('purchase-button');
```

Blade 디렉티브 역시 현재 기능 값에 따라 콘텐츠를 조건부 렌더링할 수 있습니다:

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire' 색상 활성 -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green' 색상 활성 -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange' 색상 활성 -->
@endfeature
```

> [!NOTE]
> 풍부한 값에서는 `false`가 아닌 모든 값이 "활성"으로 간주됩니다.

[조건부 `when`](#conditional-execution) 호출 시, 첫 번째 클로저에 기능의 풍부한 값이 전달됩니다:

```
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

마찬가지로 `unless` 메서드 호출에서는 두 번째 클로저에 기능 값이 전달됩니다:

```
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>
## 여러 기능 값 조회하기 (Retrieving Multiple Features)

`values` 메서드는 지정한 여러 기능 값들을 한 번에 조회합니다:

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

또는 `all` 메서드로 주어진 스코프에 대해 정의된 모든 기능 값을 다 조회할 수 있습니다:

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

단, 클래스 기반 기능은 동적으로 등록되기 때문에, 명시적으로 한 번도 체크하지 않은 경우 `all` 메서드 결과에 나타나지 않을 수 있습니다.

항상 클래스 기반 기능도 결과에 포함시키고 싶다면, Pennant의 기능 탐색(discovery) 기능을 사용하세요. 애플리케이션 서비스 프로바이더의 `boot` 메서드에 `discover` 호출을 추가하면 됩니다:

```
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

`discover` 호출은 `app/Features` 디렉토리 내의 모든 기능 클래스를 등록하며, `all` 메서드는 해당 클래스도 꼭 결과에 포함합니다:

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
## 지연 로딩 (Eager Loading)

Pennant는 같은 요청 중 메모리 내에 모든 기능 값을 캐시하지만, 여전히 성능 이슈가 발생할 수 있습니다. 이를 완화하기 위해 기능 값을 미리 로드하는 기능을 제공합니다.

예를 들어, 반복문 내에서 기능 활성 여부를 점검하는 코드가 있다고 할 때:

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

`database` 드라이버를 쓰고 있다면, 각 `active` 호출마다 쿼리가 실행되어 수백 번 요청이 발생할 수 있습니다. 이럴 때 `load` 메서드를 써서 사용자 컬렉션에 대해 기능 값을 미리 로드할 수 있습니다:

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

또한, 이미 로드된 값은 건너뛰고 필요한 기능만 로드하려면 `loadMissing` 메서드를 사용하세요:

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

<a name="updating-values"></a>
## 값 업데이트하기 (Updating Values)

기능 값은 초기 조회 시 드라이버가 저장하지만, 가끔 직접 값 수정을 원할 수도 있습니다. 이 경우 `activate`와 `deactivate` 메서드로 기능을 켜고 끌 수 있습니다:

```php
use Laravel\Pennant\Feature;

// 기본 스코프에 대해 기능 활성화...
Feature::activate('new-api');

// 특정 스코프에 대해 기능 비활성화...
Feature::for($user->team)->deactivate('billing-v2');
```

또한 두 번째 인수로 풍부한 값을 직접 지정해 기능 값을 설정할 수도 있습니다:

```php
Feature::activate('purchase-button', 'seafoam-green');
```

저장된 기능 값을 잊고 싶다면, `forget` 메서드로 제거할 수 있습니다. 이후 기능이 다시 확인될 때 기능 정의에 따라 값을 재계산합니다:

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### 일괄 업데이트 (Bulk Updates)

저장된 기능 값을 대량으로 업데이트하려면 `activateForEveryone`과 `deactivateForEveryone` 메서드를 사용하세요.

예를 들어, `new-api` 기능이 안정적이라 판단되어 모든 사용자에 대해 활성화하거나, 최종 'purchase-button' 색상을 결정해 모든 사용자에 적용할 수 있습니다:

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

모든 사용자에 대해 기능을 비활성화할 수 있습니다:

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> 이는 저장된 기능 값만 변경하며, 애플리케이션의 기능 정의 변경도 병행해야 합니다.

<a name="purging-features"></a>
### 기능 정리하기 (Purging Features)

애플리케이션에서 더 이상 사용하지 않는 기능을 완전히 저장소에서 제거하거나, 기능 정의를 변경해 모든 사용자에게 롤아웃할 때 저장된 기능 값을 일괄 삭제할 수 있습니다.

특정 기능 값을 제거하려면 `purge` 메서드를 사용하세요:

```php
// 단일 기능 정리...
Feature::purge('new-api');

// 여러 기능 정리...
Feature::purge(['new-api', 'purchase-button']);
```

저장소 내 모든 기능 값을 정리하려면 인자 없이 호출하세요:

```php
Feature::purge();
```

배포 과정에서 기능 정리를 편리하게 하기 위해 Pennant는 `pennant:purge` Artisan 명령어를 제공합니다:

```sh
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

특정 기능 목록을 제외하고 모두 정리하려면 `--except` 옵션을 사용하세요. 예를 들어, `new-api`와 `purchase-button` 기능만 남기고 모두 정리하고 싶다면 다음과 같이 실행합니다:

```sh
php artisan pennant:purge --except=new-api --except=purchase-button
```

또한, 서비스 프로바이더에 명시된 기능을 제외하고 전부 정리하는 `--except-registered` 플래그도 지원합니다:

```sh
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## 테스트 (Testing)

기능 플래그와 상호작용하는 코드를 테스트할 때, 제일 쉬운 방법은 테스트 시작 시 기능을 재정의하는 것입니다. 예를 들어, 서비스 프로바이더에 아래와 같이 기능이 정의되어 있다면:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

테스트에서 특정 값을 반환하도록 기능을 다시 정의할 수 있습니다. 아래 테스트는 `seafoam-green`이 반환됨을 항상 검증합니다:

```php
use Laravel\Pennant\Feature;

public function test_it_can_control_feature_values()
{
    Feature::define('purchase-button', 'seafoam-green');

    $this->assertSame('seafoam-green', Feature::value('purchase-button'));
}
```

클래스 기반 기능에도 같은 방식을 적용할 수 있습니다:

```php
use App\Features\NewApi;
use Laravel\Pennant\Feature;

public function test_it_can_control_feature_values()
{
    Feature::define(NewApi::class, true);

    $this->assertTrue(Feature::value(NewApi::class));
}
```

`Lottery` 인스턴스를 반환하는 기능에 대해서는 [유용한 테스트 헬퍼](/docs/10.x/helpers#testing-lotteries)가 제공됩니다.

<a name="store-configuration"></a>
#### 저장소 설정

테스트 중 Pennant가 사용할 저장소를 환경변수 `PENNANT_STORE`로 설정할 수 있습니다. `phpunit.xml`에 다음을 추가하세요:

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
## 커스텀 Pennant 드라이버 추가하기 (Adding Custom Pennant Drivers)

<a name="implementing-the-driver"></a>
#### 드라이버 구현하기

내장 드라이버로 요구사항을 충족하지 못한다면, 직접 드라이버를 구현할 수 있습니다. 이 드라이버는 `Laravel\Pennant\Contracts\Driver` 인터페이스를 구현해야 합니다:

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

각 메서드 구현 예시는 Pennant 소스코드의 `Laravel\Pennant\Drivers\DatabaseDriver`를 참고하세요: [DatabaseDriver](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)

> [!NOTE]
> Laravel 기본 디렉토리 구조는 확장 코드 위치에 제한을 두지 않습니다. 이 예시에서는 `Extensions` 디렉터리를 만들어 `RedisFeatureDriver`를 두었습니다.

<a name="registering-the-driver"></a>
#### 드라이버 등록하기

드라이버를 구현한 후에는 Laravel에 등록해야 합니다. 추가 드라이버는 `Feature` 파사드의 `extend` 메서드를 이용해 서비스 프로바이더의 `boot` 메서드 내에서 등록할 수 있습니다:

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

등록하면 `config/pennant.php`에서 `redis` 드라이버를 사용할 수 있습니다:

```
'stores' => [

    'redis' => [
        'driver' => 'redis',
        'connection' => null,
    ],

    // ...

],
```

<a name="events"></a>
## 이벤트 (Events)

Pennant는 기능 플래그와 관련하여 애플리케이션 전역에서 추적에 유용한 다양한 이벤트를 발생시킵니다.

### `Laravel\Pennant\Events\RetrievingKnownFeature`

특정 스코프로 요청 중 처음 알려진(정의된) 기능을 조회할 때 발생합니다. 기능 플래그 사용 현황을 분석하는 지표 수집에 유용합니다.

### `Laravel\Pennant\Events\RetrievingUnknownFeature`

처음 알 수 없는(정의되지 않은) 기능이 요청 내에서 조회될 때 발생합니다. 본래 기능 플래그를 제거했는데도 애플리케이션 어딘가에서 참조가 남아 있을 때 이 이벤트가 유용합니다.

예를 들어, 이 이벤트 리스너를 등록하여 발생 시 `report`하거나 예외를 던지도록 할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Event;
use Laravel\Pennant\Events\RetrievingUnknownFeature;

class EventServiceProvider extends ServiceProvider
{
    /**
     * Register any other events for your application.
     */
    public function boot(): void
    {
        Event::listen(function (RetrievingUnknownFeature $event) {
            report("Resolving unknown feature [{$event->feature}].");
        });
    }
}
```

### `Laravel\Pennant\Events\DynamicallyDefiningFeature`

클래스 기반 기능이 요청 중 처음 동적으로 확인될 때 발생하는 이벤트입니다.