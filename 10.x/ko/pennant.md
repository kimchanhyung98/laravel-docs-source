# Laravel Pennant

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
- [기능 정의](#defining-features)
    - [클래스 기반 기능](#class-based-features)
- [기능 체크](#checking-features)
    - [조건부 실행](#conditional-execution)
    - [`HasFeatures` 트레이트](#the-has-features-trait)
    - [Blade 지시문](#blade-directive)
    - [미들웨어](#middleware)
    - [인메모리 캐시](#in-memory-cache)
- [스코프](#scope)
    - [스코프 지정](#specifying-the-scope)
    - [기본 스코프](#default-scope)
    - [Nullable 스코프](#nullable-scope)
    - [스코프 식별](#identifying-scope)
    - [스코프 직렬화](#serializing-scope)
- [리치(다양한) 값 사용 기능](#rich-feature-values)
- [여러 기능 가져오기](#retrieving-multiple-features)
- [Eager Loading](#eager-loading)
- [값 업데이트하기](#updating-values)
    - [대량 업데이트](#bulk-updates)
    - [기능 제거(Purge)](#purging-features)
- [테스트](#testing)
- [커스텀 Pennant 드라이버 추가](#adding-custom-pennant-drivers)
    - [드라이버 구현](#implementing-the-driver)
    - [드라이버 등록](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Pennant](https://github.com/laravel/pennant)는 불필요한 부분 없이 간단하고 가벼운 기능 플래그(Feature Flag) 패키지입니다. 기능 플래그를 사용하면 새로운 애플리케이션 기능을 점진적으로 배포할 수 있고, UI의 A/B 테스트, trunk 기반 개발 전략 보완 등 다양한 활용이 가능합니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 사용하여 Pennant를 프로젝트에 설치하세요:

```shell
composer require laravel/pennant
```

다음으로, `vendor:publish` Artisan 명령어를 사용하여 Pennant의 설정 및 마이그레이션 파일을 퍼블리시하세요:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 수행하세요. Pennant가 `database` 드라이버에서 사용하는 `features` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
## 설정

Pennant의 에셋을 퍼블리시하면 설정 파일이 `config/pennant.php`에 생성됩니다. 이 파일에서 Pennant가 기능 플래그 값을 저장할 때 사용할 기본 스토리지를 지정할 수 있습니다.

Pennant는 메모리 내 배열에 값을 저장하는 `array` 드라이버를 제공합니다. 혹은 기본으로 사용되는 `database` 드라이버를 통해 관계형 데이터베이스에 기능 플래그 값을 영구적으로 저장할 수 있습니다.

<a name="defining-features"></a>
## 기능 정의

기능을 정의하려면 `Feature` 퍼사드에서 제공하는 `define` 메서드를 사용하세요. 기능의 이름과, 해당 기능의 초기 값을 결정할 클로저를 전달해야 합니다.

일반적으로 기능은 서비스 프로바이더 내에서 `Feature` 퍼사드를 통해 정의합니다. 이 클로저는 기능 체크 대상 스코프(대부분 현재 인증된 사용자)를 파라미터로 받습니다. 예를 들어, 아래는 새로운 API를 점진적으로 사용자에게 배포하는 기능 플래그 정의 예시입니다:

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

위 예시에서 각 규칙은 다음과 같습니다:

- 내부 팀원은 모두 새로운 API를 사용해야 합니다.
- 대량 트래픽 고객은 새로운 API를 사용하지 않습니다.
- 그 외의 사용자는 100명 중 1명의 확률로 랜덤하게 기능이 활성화됩니다.

특정 사용자에 대해 `new-api` 기능이 처음 체크될 때, 클로저 반환값이 스토리지 드라이버에 저장됩니다. 이후 동일 사용자에 대해 다시 체크하면, 저장된 값이 반환되고 클로저는 호출되지 않습니다.

간단히, 기능 정의가 단순히 로터리(Lottery)만 반환하는 경우라면 클로저를 생략할 수 있습니다:

    Feature::define('site-redesign', Lottery::odds(1, 1000));

<a name="class-based-features"></a>
### 클래스 기반 기능

Pennant는 클래스 기반으로 기능을 정의하는 것도 지원합니다. 클로저 기반 기능과는 달리, 클래스 기반 기능은 서비스 프로바이더에 별도로 등록할 필요가 없습니다. Artisan 명령어 `pennant:feature`로 생성할 수 있으며, 기본적으로 `app/Features` 디렉토리에 클래스가 생성됩니다:

```shell
php artisan pennant:feature NewApi
```

기능 클래스 작성 시, 단 하나의 `resolve` 메서드만 정의하면 됩니다. 이 메서드는 주어진 스코프(대부분 현재 인증된 사용자)에 대해 기능 활성화 여부를 결정합니다:

```php
<?php

namespace App\Features;

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

> [!NOTE]
> 기능 클래스는 [서비스 컨테이너](/docs/{{version}}/container)로부터 해석되므로, 필요하면 생성자에 의존성을 주입할 수 있습니다.

#### 저장되는 기능 이름 커스터마이징

기본적으로 Pennant는 기능 클래스의 전체 네임스페이스 경로를 저장합니다. 만약 스토리지 내 기능 이름을 내부 구조와 분리하고 싶다면, 클래스 내 `$name` 프로퍼티를 지정할 수 있습니다. 이 값이 클래스명 대신 저장됩니다:

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
## 기능 체크

기능이 활성화되어 있는지 확인하려면 `Feature` 퍼사드의 `active` 메서드를 사용하세요. 기본적으로 현재 인증된 사용자에 대해 기능 체크가 이뤄집니다:

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

기본적으로 현재 인증 사용자에 대해 체크하지만, `for` 메서드를 통해 다른 사용자나 [스코프](#scope)도 쉽게 지정할 수 있습니다:

```php
return Feature::for($user)->active('new-api')
        ? $this->resolveNewApiResponse($request)
        : $this->resolveLegacyApiResponse($request);
```

Pennant는 기능 활성화 여부를 확인할 때 유용한 다양한 보조 메서드도 제공합니다:

```php
// 주어진 모든 기능이 활성화되어 있는지 확인
Feature::allAreActive(['new-api', 'site-redesign']);

// 주어진 기능 중 하나라도 활성화되어 있는지 확인
Feature::someAreActive(['new-api', 'site-redesign']);

// 기능이 비활성화되어 있는지 확인
Feature::inactive('new-api');

// 주어진 모든 기능이 비활성화되어 있는지 확인
Feature::allAreInactive(['new-api', 'site-redesign']);

// 주어진 기능 중 하나라도 비활성화되어 있는지 확인
Feature::someAreInactive(['new-api', 'site-redesign']);
```

> [!NOTE]  
> Artisan 명령어나 큐 작업 등 HTTP 컨텍스트 외부에서 Pennant를 사용할 경우, [명시적으로 기능의 스코프를 지정](#specifying-the-scope)해야 합니다. 또는, 인증·비인증 환경 모두를 고려한 [기본 스코프](#default-scope)를 설정할 수 있습니다.

<a name="checking-class-based-features"></a>
#### 클래스 기반 기능 체크

클래스 기반 기능의 체크는 기능의 클래스명을 넘깁니다:

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

`when` 메서드는 기능이 활성화되어 있을 때 지정한 클로저를 실행합니다. 두 번째 클로저를 넘기면 비활성화 시 실행됩니다:

```php
return Feature::when(NewApi::class,
    fn () => $this->resolveNewApiResponse($request),
    fn () => $this->resolveLegacyApiResponse($request),
);
```

반대로, 기능이 비활성화 시 첫 번째 클로저를 실행하는 `unless`도 있습니다:

```php
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
### `HasFeatures` 트레이트

Pennant의 `HasFeatures` 트레이트를 애플리케이션의 `User` 모델 등 기능을 체크할 대상 모델에 추가하여, 더욱 간결하고 직관적으로 기능을 체크할 수 있습니다:

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

트레이트를 추가하면 모델에서 `features()` 메서드를 통해 기능을 바로 체크할 수 있습니다:

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

이 외에도 다양한 메서드를 사용할 수 있습니다:

```php
// 값 조회
$value = $user->features()->value('purchase-button');
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
### Blade 지시문

Pennant는 손쉽게 Blade에서 기능 체크가 가능하도록 `@feature` 지시문을 제공합니다:

```blade
@feature('site-redesign')
    <!-- 'site-redesign' 기능이 활성화 됨 -->
@else
    <!-- 'site-redesign' 기능이 비활성화 됨 -->
@endfeature
```

<a name="middleware"></a>
### 미들웨어

Pennant에는 인증된 사용자가 기능에 접근 권한이 있는지 확인하는 [미들웨어](/docs/{{version}}/middleware)도 포함되어 있습니다. 해당 미들웨어를 라우트에 할당하고, 접근에 필요한 기능명을 지정할 수 있습니다. 지정된 기능 중 하나라도 비활성화되어 있으면, 라우트에서는 `400 Bad Request` 응답을 반환합니다. 여러 기능명을 배열로 넘겨 지정할 수도 있습니다.

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### 응답 커스터마이징

미들웨어에서 지정한 기능 중 하나라도 비활성화되어 있을 때 반환되는 응답을 커스터마이징하려면, `EnsureFeaturesAreActive` 미들웨어의 `whenInactive` 메서드를 사용하세요. 일반적으로 서비스 프로바이더의 `boot` 메서드 내에서 설정합니다.

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
### 인메모리 캐시

기능을 체크할 때 Pennant는 결과를 메모리 내에 캐시합니다. `database` 드라이버를 사용할 경우, 동일 요청 내에서 같은 기능 플래그를 재차 체크해도 추가 DB 쿼리가 발생하지 않습니다. 또한 요청 동안 일관성 있는 결과를 보장합니다.

인메모리 캐시를 수동으로 플러시해야 한다면, `Feature` 퍼사드의 `flushCache` 메서드를 사용하세요:

    Feature::flushCache();

<a name="scope"></a>
## 스코프

<a name="specifying-the-scope"></a>
### 스코프 지정

앞서 설명했듯, 기능은 일반적으로 현재 인증 사용자를 대상으로 체크하지만, 상황에 따라 다를 수 있습니다. `Feature` 퍼사드의 `for` 메서드로 체크할 대상을 명시적으로 지정할 수 있습니다:

```php
return Feature::for($user)->active('new-api')
        ? $this->resolveNewApiResponse($request)
        : $this->resolveLegacyApiResponse($request);
```

기능의 스코프는 꼭 "사용자"가 아니어도 됩니다. 예를 들어, 새로운 결제 경험을 개별 사용자 대신 팀 단위로 롤아웃하고 싶을 때, 팀 생성일에 따라 점진적 배포 속도를 달리할 수 있습니다:

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

이런 구조에서는 클로저가 `User` 대신 `Team` 모델을 기대합니다. 사용자의 팀에 대해 해당 기능 활성 여부를 판단하려면, `Feature::for($user->team)` 형식으로 체크해야 합니다:

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect()->to('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### 기본 스코프

Pennant가 기능 체크 시 사용하는 기본 스코프도 커스터마이즈할 수 있습니다. 예를 들어, 모든 기능을 인증된 사용자의 팀 기준으로 체크하고 싶다면, 매번 `Feature::for($user->team)`를 쓸 필요 없이 기본 스코프를 지정할 수 있습니다. 일반적으로 서비스 프로바이더 내에서 설정합니다:

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

이제 `for` 메서드로 스코프를 넘기지 않으면, 기본적으로 현재 인증된 사용자의 팀이 스코프로 사용됩니다:

```php
Feature::active('billing-v2');

// 위 코드는 다음과 동일합니다...

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### Nullable 스코프

기능 체크 시 지정한 스코프가 `null`이고, 기능 정의에서 `null` 타입을 지원하지 않을 경우, Pennant는 해당 기능의 결과를 자동으로 `false`로 반환합니다.

따라서 `null`이 될 수 있는 스코프를 넘기면서 resolver가 반드시 호출되길 원한다면, 기능 정의에서 이를 적절히 처리해야 합니다. Artisan 명령어나 큐 작업, 인증 없는 라우트 등에서는 스코프가 `null`인 경우가 많은데 이때 기본 스코프 역시 `null`이 됩니다.

[명시적으로 기능 스코프를 지정](#specifying-the-scope)하지 않는다면, 타입 선언을 nullable로 하고, 기능 정의 로직 내에서 `null`을 처리하세요.

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

Pennant의 내장 `array` 및 `database` 저장 드라이버는 모든 PHP 데이터 타입과 Eloquent 모델 스코프에 대해 식별자를 올바르게 저장할 수 있습니다. 하지만 써드파티 드라이버를 사용할 경우, Eloquent 모델이나 커스텀 타입의 식별자를 올바로 저장하지 못할 수도 있습니다.

Pennant는 애플리케이션에서 스코프로 사용하는 객체에 `FeatureScopeable` 계약을 구현하여, 저장을 위한 스코프 값 포맷을 커스터마이징할 수 있습니다.

예를 들어, 내장 `database` 드라이버와 서드파티 "Flag Rocket" 드라이버를 모두 사용하는 상황에서, "Flag Rocket" 드라이버는 Eloquent 모델을 알지 못하고, 대신 `FlagRocketUser` 인스턴스를 요구한다면 아래처럼 처리할 수 있습니다:

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

Pennant는 Eloquent 모델과 연관된 기능을 저장할 때, 기본적으로 클래스의 전체 네임스페이스명을 사용합니다. 이미 [Eloquent Morph Map](/docs/{{version}}/eloquent-relationships#custom-polymorphic-types)을 사용한다면, 저장되는 기능과 애플리케이션 구조의 결합도를 낮추기 위해 Pennant 역시 morph map을 사용할 수 있습니다.

서비스 프로바이더에서 morph map을 지정한 후, `Feature` 퍼사드의 `useMorphMap` 메서드를 호출하세요:

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
## 리치(다양한) 값 사용 기능

지금까지는 기능이 "활성(on)" 혹은 "비활성(off)"의 이진 상태만 보여주었지만, Pennant는 그 외 다양한 값을 저장할 수도 있습니다.

예를 들어, "Buy now" 버튼에 세 가지 색상을 테스트하고 싶다면, true/false 대신 문자열을 반환할 수 있습니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

`purchase-button` 기능의 값을 `value` 메서드로 받을 수 있습니다:

```php
$color = Feature::value('purchase-button');
```

Pennant가 제공하는 Blade 지시문으로 값에 따라 조건부 렌더링도 쉽습니다:

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire'가 활성화 -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green'가 활성화 -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange'가 활성화 -->
@endfeature
```

> [!NOTE]
> 다양한 값(rich value)을 사용할 경우, 값이 `false`가 아닐 때 해당 기능은 "활성(active)"으로 간주됩니다.

[조건부 `when`](#conditional-execution) 메서드를 사용할 때, 기능의 리치 값이 첫 번째 클로저로 전달됩니다:

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

`unless` 메서드에서도, 리치 값이 (선택적) 두 번째 클로저로 전달됩니다:

```php
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>
## 여러 기능 가져오기

`values` 메서드로, 주어진 스코프에 대해 여러 기능 값을 동시 조회할 수 있습니다:

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

혹은 `all` 메서드로, 해당 스코프에서 정의된 모든 기능 값을 조회할 수도 있습니다:

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

단, 클래스 기반 기능은 동적으로 등록되어, 명시적으로 체크되기 전까지는 Pennant가 인식하지 못합니다. 그래서 현재 요청에서 아직 체크되지 않은 클래스 기반 기능은 `all` 결과에 나타나지 않을 수 있습니다.

기능 클래스가 항상 `all`에 포함되길 원한다면, Pennant의 기능 탐색(discovery) 기능을 사용하세요. 서비스 프로바이더에서 `discover` 메서드를 호출해 등록할 수 있습니다:

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

이제 `all` 메서드는 요청 중에 한 번이라도 체크되었는지와 무관하게, `app/Features` 디렉토리 내 클래스 기능을 모두 결과에 포함합니다:

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

Pennant는 단일 요청에서 해석한 모든 기능을 메모리에 캐시하지만, 대량의 기능 체크가 발생하면 성능 부하가 있을 수 있습니다. 이를 개선하기 위해 Pennant는 기능 값을 미리 적재(eager load)하는 기능도 제공합니다.

예를 들어, 아래처럼 루프에서 사용자별로 기능을 개별 체크할 경우:

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

`database` 드라이버를 쓴다면, 루프마다 DB 쿼리가 수백 번 발생할 수 있습니다. `load` 메서드를 이용해 전체 유저나 스코프에 대해 미리 기능 값을 적재할 수 있습니다:

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

이미 적재된 경우를 제외하고 필요한 기능만 적재하려면 `loadMissing` 메서드를 사용합니다:

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

<a name="updating-values"></a>
## 값 업데이트하기

기능의 값이 처음 해석되면, 해당 결과는 스토리지에 저장됩니다. 이는 여러 요청 간 사용자 경험의 일관성을 보장하기 위함입니다. 하지만 필요에 따라 기능의 저장 값을 수동으로 업데이트할 수도 있습니다.

이를 위해, `activate`, `deactivate` 등의 메서드로 기능을 직접 켜거나 끌 수 있습니다:

```php
use Laravel\Pennant\Feature;

// 기본 스코프에 대해 기능 활성화
Feature::activate('new-api');

// 특정 스코프(예: 팀)에 대해 비활성화
Feature::for($user->team)->deactivate('billing-v2');
```

리치 값을 직접 지정해 저장하려면, `activate`에 두 번째 인자(값)를 넘길 수 있습니다:

```php
Feature::activate('purchase-button', 'seafoam-green');
```

기능의 저장 값을 잊도록(Pennant가 다시 정의를 참조하게) 만들려면, `forget` 메서드를 사용하세요:

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### 대량 업데이트

여러 스코프에 대해 한 번에 기능값을 업데이트하려면 `activateForEveryone`, `deactivateForEveryone` 메서드를 사용하세요.

예를 들어, `new-api` 기능의 안정성이 확인되고, 구매 버튼(color)도 확정되었다면 다음과 같이 모든 사용자에 대해 일괄 값을 업데이트할 수 있습니다:

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

또는 모든 사용자에 대해 기능을 비활성화할 수도 있습니다:

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> 이 메서드는 Pennant 저장소에 이미 저장된 해석 값을 "업데이트"합니다. 애플리케이션의 기능 정의도 함께 갱신해야 합니다.

<a name="purging-features"></a>
### 기능 제거(Purge)

애플리케이션에서 기능을 삭제했거나, 기능 정의를 전체적으로 변경하여 모든 사용자가 새 정의를 적용받게 하려면, 전체 값을 purge 하는 것이 유용할 수 있습니다.

기능의 저장 값을 모두 제거하려면 `purge` 메서드를 사용하세요:

```php
// 특정 기능 하나만 purge
Feature::purge('new-api');

// 여러 기능 purge
Feature::purge(['new-api', 'purchase-button']);
```

모든 기능을 한 번에 purge 하려면, 인수 없이 호출합니다:

```php
Feature::purge();
```

배포 자동화 등과 연계해 purge를 명령어로 실행하려면, Pennant가 제공하는 `pennant:purge` Artisan 명령어를 이용하세요:

```sh
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

특정 목록의 기능만 제외하고 모두 purge하고 싶다면, `--except` 옵션을 사용하세요:

```sh
php artisan pennant:purge --except=new-api --except=purchase-button
```

추가로, `--except-registered` 플래그를 사용하면 서비스 프로바이더에서 명시적으로 등록한 기능만 제외한 모두를 purge 합니다:

```sh
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## 테스트

기능 플래그와 연동된 코드를 테스트할 때, 테스트에서 기능의 반환 값을 제어하는 가장 쉬운 방법은 기능을 다시 정의(override)하는 것입니다. 예를 들어, 애플리케이션의 서비스 프로바이더에 다음과 같이 정의되어 있다 가정합니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

테스트에서 기능 반환 값을 변경하려면, 테스트 시작 부분에 기능을 재정의하면 됩니다. 예시 테스트는 언제나 통과합니다:

```php
use Laravel\Pennant\Feature;

public function test_it_can_control_feature_values()
{
    Feature::define('purchase-button', 'seafoam-green');

    $this->assertSame('seafoam-green', Feature::value('purchase-button'));
}
```

동일 방식은 클래스 기반 기능에도 적용할 수 있습니다:

```php
use App\Features\NewApi;
use Laravel\Pennant\Feature;

public function test_it_can_control_feature_values()
{
    Feature::define(NewApi::class, true);

    $this->assertTrue(Feature::value(NewApi::class));
}
```

기능이 `Lottery` 인스턴스를 반환한다면, [유용한 테스트 헬퍼](/docs/{{version}}/helpers#testing-lotteries)도 사용할 수 있습니다.

<a name="store-configuration"></a>
#### 스토어 설정

Pennant가 테스트 중 사용할 스토어를 지정하려면, `phpunit.xml`에서 `PENNANT_STORE` 환경 변수를 설정하세요:

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

Pennant의 내장 스토리지 드라이버가 요구에 맞지 않는 경우, 직접 드라이버를 구현할 수 있습니다. 커스텀 드라이버는 `Laravel\Pennant\Contracts\Driver` 인터페이스를 구현해야 합니다:

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

각 메서드는 예시로 Redis 연결을 통해 구현할 수 있습니다. 구체적 예시는 [Pennant 소스코드의 DatabaseDriver](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)를 참고하세요.

> [!NOTE]  
> Laravel에 확장(extensions)을 위한 별도 디렉터리는 없습니다. 원하는 위치에 생성해도 무방합니다. 위 예시는 `Extensions` 디렉토리에 드라이버를 두었습니다.

<a name="registering-the-driver"></a>
#### 드라이버 등록

드라이버 구현이 끝났다면, Pennant에 등록해야 합니다. Pennant에 드라이버를 추가하려면, `Feature` 퍼사드의 `extend` 메서드를 사용하세요. 이 메서드는 서비스 프로바이더의 `boot` 메서드 내에서 호출하면 좋습니다.

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

이제 `config/pennant.php`의 드라이버에 `redis`를 사용할 수 있습니다:

```php
'stores' => [

    'redis' => [
        'driver' => 'redis',
        'connection' => null,
    ],

    // ...

],
```

<a name="events"></a>
## 이벤트

Pennant는 애플리케이션 전반의 기능 플래그 추적에 유용한 다양한 이벤트를 디스패치합니다.

### `Laravel\Pennant\Events\RetrievingKnownFeature`

요청 중, 특정 스코프에 대해 이미 알려진(정의된) 기능을 처음 조회할 때 발생합니다. 기능 플래그 사용 현황을 메트릭으로 수집·분석할 때 유용합니다.

### `Laravel\Pennant\Events\RetrievingUnknownFeature`

요청 중, 특정 스코프에 대해 미정의(정의 안 된) 기능이 처음 조회될 때 발생합니다. 기능 플래그 삭제 후 참조가 남아있는지 탐지할 때 활용할 수 있습니다.

예를 들어, 이 이벤트 핸들러에서 `report`(로깅)하거나 예외를 발생시킬 수 있습니다:

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

요청 중 클래스 기반 기능이 처음으로 동적으로 체크될 때 발생합니다.