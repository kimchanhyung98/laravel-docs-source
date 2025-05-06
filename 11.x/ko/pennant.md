# Laravel Pennant

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
- [기능(Feature) 정의하기](#defining-features)
    - [클래스 기반 기능](#class-based-features)
- [기능 확인하기](#checking-features)
    - [조건부 실행](#conditional-execution)
    - [`HasFeatures` 트레이트](#the-has-features-trait)
    - [Blade 지시어](#blade-directive)
    - [미들웨어](#middleware)
    - [기능 체크 가로채기](#intercepting-feature-checks)
    - [메모리 내 캐시](#in-memory-cache)
- [스코프(Scope)](#scope)
    - [스코프 지정](#specifying-the-scope)
    - [기본 스코프](#default-scope)
    - [Nullable 스코프](#nullable-scope)
    - [스코프 식별](#identifying-scope)
    - [스코프 직렬화](#serializing-scope)
- [풍부한 기능 값](#rich-feature-values)
- [여러 기능 한 번에 조회](#retrieving-multiple-features)
- [Eager Loading](#eager-loading)
- [값 업데이트](#updating-values)
    - [대량 업데이트](#bulk-updates)
    - [기능 삭제(Purging)](#purging-features)
- [테스트](#testing)
- [커스텀 Pennant 드라이버 추가](#adding-custom-pennant-drivers)
    - [드라이버 구현하기](#implementing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
    - [외부에서 기능 정의하기](#defining-features-externally)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Pennant](https://github.com/laravel/pennant)는 불필요한 요소 없이 심플하고 가벼운 **기능 플래그(Feature Flag)** 패키지입니다. 기능 플래그를 통해 새로운 애플리케이션 기능을 점진적으로 배포하고, A/B 테스트, 트렁크 기반 개발 전략 보완 등 다양한 작업을 안전하게 수행할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 이용해 Pennant를 프로젝트에 설치하세요.

```shell
composer require laravel/pennant
```

다음으로, `vendor:publish` Artisan 명령어를 사용해 Pennant 설정 및 마이그레이션 파일을 퍼블리시합니다.

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. 이 과정에서 Pennant의 `database` 드라이버에 필요한 `features` 테이블이 생성됩니다.

```shell
php artisan migrate
```

<a name="configuration"></a>
## 설정

Pennant의 에셋을 퍼블리시한 후, 설정 파일은 `config/pennant.php` 위치에 저장됩니다. 이 설정 파일에서 Pennant가 기능 플래그 값(Feature Flag Value)을 저장할 기본 스토리지 방식을 지정할 수 있습니다.

Pennant는 `array` 드라이버를 통해 인메모리 배열에 값을 저장하거나, 기본값으로 사용하는 `database` 드라이버를 통해 관계형 데이터베이스에 값을 영구적으로 저장할 수 있습니다.

<a name="defining-features"></a>
## 기능(Feature) 정의하기

기능을 정의하려면 `Feature` 파사드의 `define` 메서드를 사용하세요. 기능의 이름과, 해당 기능의 초기값을 결정하는 클로저(Closure)를 전달해야 합니다.

일반적으로 서비스 프로바이더 내부에서 Feature 파사드를 이용해 기능을 정의합니다. 전달되는 클로저에는 기능 체크의 "스코프"(대부분 현재 인증된 사용자)가 인자로 들어갑니다. 아래는 애플리케이션 사용자들에게 새로운 API를 점진적으로 배포하기 위한 기능 예시입니다:

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

위 예시의 규칙은 다음과 같습니다.

- 모든 내부 팀원은 새 API를 사용하게 됩니다.
- 트래픽이 많은 고객은 새 API를 사용하지 못합니다.
- 그 외는 1/100 확률로 기능이 활성화됩니다.

특정 사용자에 대해 `new-api` 기능이 처음 체크되면, 클로저의 결과가 스토리지 드라이버에 저장됩니다. 이후 같은 사용자에 대해 기능 체크가 발생하면 저장되어 있던 값이 반환되고, 클로저는 다시 호출되지 않습니다.

간단히, 기능 정의가 Lottery만 반환한다면 클로저 없이 아래처럼 정의할 수도 있습니다.

    Feature::define('site-redesign', Lottery::odds(1, 1000));

<a name="class-based-features"></a>
### 클래스 기반 기능

Pennant는 클래스 기반 기능 추가도 지원합니다. 클로저 방식과 달리, 서비스 프로바이더에 별도 등록이 필요 없습니다. 클래스 기반 기능을 생성하려면 `pennant:feature` Artisan 명령어를 실행하세요. 기본적으로 `app/Features` 디렉터리에 클래스가 생성됩니다:

```shell
php artisan pennant:feature NewApi
```

클래스 기반 기능 작성 시, 주로 `resolve` 메서드만 정의하면 됩니다. 이 메서드는 주어진 스코프에 대해 기능의 초기값을 반환하며, 스코프는 보통 현재 인증된 사용자입니다.

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

클래스 기반 기능 인스턴스를 직접 해결하고 싶다면, Feature 파사드의 `instance` 메서드를 사용하세요.

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]   
> Feature 클래스는 [서비스 컨테이너](/docs/{{version}}/container)를 통하므로, 필요 시 생성자에 의존성을 주입할 수 있습니다.

#### 저장되는 기능 이름 커스터마이징

기본적으로 Pennant는 기능 클래스의 전체 네임스페이스 이름을 저장합니다. 저장할 이름을 애플리케이션 내부 구조에서 분리하고 싶다면 클래스에 `$name` 프로퍼티를 지정할 수 있습니다.

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
## 기능 확인하기

기능이 활성 상태인지 확인하려면, `Feature` 파사드의 `active` 메서드를 사용하면 됩니다. 기본적으로 현재 인증된 사용자에 대해 체크가 이루어집니다.

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

기본값 외에 다른 사용자 또는 [스코프](#scope)로 체크하고 싶다면 `for` 메서드를 활용하세요.

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

Pennant는 활성/비활성 여부를 확인할 수 있는 각종 편의 메서드도 제공합니다:

```php
// 주어진 모든 기능이 활성인지 확인...
Feature::allAreActive(['new-api', 'site-redesign']);

// 일부라도 기능이 활성인지 확인...
Feature::someAreActive(['new-api', 'site-redesign']);

// 특정 기능이 비활성인지 확인...
Feature::inactive('new-api');

// 주어진 모든 기능이 비활성인지 확인...
Feature::allAreInactive(['new-api', 'site-redesign']);

// 일부라도 기능이 비활성인지 확인...
Feature::someAreInactive(['new-api', 'site-redesign']);
```

> [!NOTE]  
> Artisan 명령어나 큐 작업 등 HTTP 맥락 외에서 Pennant를 사용할 때는 보통 [기능의 스코프를 명시적으로 지정](#specifying-the-scope)해주어야 합니다. 또는, 인증 및 비인증 맥락 모두를 아우르는 [기본 스코프](#default-scope)를 정의해둘 수도 있습니다.

<a name="checking-class-based-features"></a>
#### 클래스 기반 기능 확인

클래스 기반 기능일 때는 기능 체크 시 클래스 이름을 인자로 전달해야 합니다.

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

`when` 메서드는 특정 기능이 활성화된 경우 지정된 클로저를 실행하고, 두 번째 클로저를 전달하면 기능이 비활성화된 경우 실행됩니다.

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

`unless` 메서드는 `when`의 반대이며, 기능이 비활성일 때 첫 번째 클로저를 실행합니다.

    return Feature::unless(NewApi::class,
        fn () => $this->resolveLegacyApiResponse($request),
        fn () => $this->resolveNewApiResponse($request),
    );

<a name="the-has-features-trait"></a>
### `HasFeatures` 트레이트

Pennant의 `HasFeatures` 트레이트를 애플리케이션의 `User` 모델(또는 기능 사용 대상인 다른 모델)에 추가하면, 모델을 통해 직접 기능을 확인할 수 있습니다.

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

트레이트를 추가하면 `features` 메서드를 통해 손쉽게 기능을 확인할 수 있습니다.

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

물론 아래와 같은 다양한 메서드도 함께 사용할 수 있습니다.

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
### Blade 지시어

Pennant는 Blade에서 편리하게 기능을 체크할 수 있도록 `@feature`와 `@featureany` 지시어를 제공합니다.

```blade
@feature('site-redesign')
    <!-- 'site-redesign'가 활성 상태일 때 -->
@else
    <!-- 'site-redesign'가 비활성 상태일 때 -->
@endfeature

@featureany(['site-redesign', 'beta'])
    <!-- 'site-redesign'이나 'beta' 중 하나라도 활성화된 경우 -->
@endfeatureany
```

<a name="middleware"></a>
### 미들웨어

Pennant에는 [미들웨어](/docs/{{version}}/middleware)도 포함되어 있어, 라우트 접근 전에 현재 인증된 사용자가 해당 기능에 접근 권한이 있는지 확인할 수 있습니다. 미들웨어는 라우트에 지정할 수 있으며, 접근에 필요한 기능을 지정해줄 수 있습니다. 지정한 기능 중 하나라도 현재 사용자에게 비활성 상태라면 `400 Bad Request` HTTP 응답이 반환됩니다. 여러 기능을 `using` 메서드에 넘겨줄 수 있습니다.

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### 응답 커스터마이징

기능 중 하나가 비활성일 때 미들웨어가 반환하는 응답을 커스터마이즈하고 싶다면, `EnsureFeaturesAreActive` 미들웨어의 `whenInactive` 메서드를 활용할 수 있습니다. 보통 서비스 프로바이더의 `boot` 메서드 내에서 호출합니다.

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
### 기능 체크 가로채기

때로는 저장된 기능 값 조회 전에 인메모리 체크를 먼저 하고 싶을 수 있습니다. 예를 들어, 기능 플래그 뒤에 새 API를 개발하는 중, 스토리지의 값은 유지하되 API 자체를 일시적으로 중단하고 싶을 때가 있을 수 있습니다. 버그가 발견되면 내부 팀원 외 전체에서 기능을 꺼두고, 버그 수정 후 다시 활성화하는 상황을 생각할 수 있습니다.

이를 위해 [클래스 기반 기능](#class-based-features)의 `before` 메서드를 사용할 수 있습니다. 이 메서드가 있을 경우, 스토리지의 값 조회 전 항상 인메모리에서 먼저 실행되며, 반환값이 `null`이 아니면 해당 값이 요청 동안 사용됩니다.

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

또한 아래처럼 특정 날짜 이후엔 모두에게 기능을 활성화하도록 할 수도 있습니다.

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

기능 체크 시 Pennant는 결과를 메모리 내 캐시에 저장합니다. `database` 드라이버 사용 시, 동일한 기능 플래그 체크가 하나의 요청 내에서 반복되어도 DB 쿼리는 한 번만 발생합니다. 요청이 끝날 때까지 일관적인 체크 결과가 보장됩니다.

캐시를 직접 비워야 할 경우, Feature 파사드의 `flushCache` 메서드를 사용하세요.

    Feature::flushCache();

<a name="scope"></a>
## 스코프(Scope)

<a name="specifying-the-scope"></a>
### 스코프 지정

앞서 설명했듯 기능은 보통 현재 인증 사용자 기준으로 체크됩니다. 하지만 항상 그러리라는 보장은 없으므로, `Feature` 파사드의 `for` 메서드를 사용해 원하는 스코프(예: 팀, 조직, 특정 오브젝트 등)를 직접 지정할 수 있습니다.

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

스코프는 단순히 'User'가 아니어도 됩니다. 예를 들어, 새 결제 시스템을 전체 팀 단위로 배포한다면 팀 모델을 스코프로 사용하는 식입니다. 다음은 팀 생성일에 따라 기능 활성화 여부와 확률을 다르게 지정한 예시입니다.

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

이렇게 정의하면, 실제로 기능이 활성화되었는지 체크할 때도 `for` 메서드에 팀 모델을 넘깁니다.

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### 기본 스코프

Pennant가 기능 체크 시 사용하는 기본 스코프도 커스터마이즈할 수 있습니다. 예를 들어, 모든 기능이 현재 인증 사용자의 팀 단위로 체크되는 구조라면, 매번 `Feature::for($user->team)`을 사용할 필요 없이 아래처럼 기본 스코프로 지정할 수 있습니다. 보통 서비스 프로바이더 내에서 설정합니다.

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

이제 `for`을 사용하지 않아도, 기본 스코프로 `user->team`이 적용됩니다.

```php
Feature::active('billing-v2');

// 위와 동일함

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### Nullable 스코프

기능 체크 시 전달된 스코프가 `null`인데, 기능 정의에 nullable 타입이나 유니언 타입에 `null`이 없으면 Pennant는 자동으로 `false`를 반환합니다.

따라서, 스코프가 `null`일 수 있고 그 경우에도 기능 값을 판단하고 싶다면, 기능 정의에서 이에 대한 처리를 해주어야 합니다. 예를 들어, Artisan 명령어, 큐 작업, 비인증 라우트에선 인증 사용자가 없으므로 스코프가 `null`이 될 수 있습니다.

스코프를 명시적으로 지정하지 않는다면, 스코프의 타입을 Nullable로 두고, `null`일 때의 로직을 추가하세요.

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

Pennant 기본 제공 `array`와 `database` 저장 드라이버는 모든 PHP 데이터 타입 및 Eloquent 모델의 스코프 식별자를 올바르게 저장할 수 있습니다. 하지만 서드파티 Pennant 드라이버를 사용한다면, Eloquent 모델이나 커스텀 타입의 식별자를 제대로 처리하지 못할 수 있습니다.

이때는, Pennant 스코프로 사용되는 오브젝트에 `FeatureScopeable` 계약을 구현해 스코프 값을 원하는 방식으로 포맷할 수 있습니다.

예를 들어, 내장 `database` 드라이버 외에 서드파티 "Flag Rocket" 드라이버도 함께 사용한다고 합시다. "Flag Rocket" 드라이버는 Eloquent 모델이 아닌 자체 객체(예: `FlagRocketUser`)를 요구할 수 있습니다. 이럴 땐 아래처럼 처리하세요.

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

Pennant는 기본적으로 Eloquent 모델에 연관된 기능을 저장할 때 전체 클래스 이름을 사용합니다. 이미 [Eloquent Morph Map](/docs/{{version}}/eloquent-relationships#custom-polymorphic-types)을 사용하고 있다면, 기능 저장 시에도 Morph Map을 적용할 수 있습니다.

Morph Map을 서비스 프로바이더에서 정의한 후, 아래처럼 `Feature` 파사드의 `useMorphMap` 메서드를 호출하세요.

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

지금까지 이진 상태(활성/비활성)로 기능을 표현했지만, Pennant는 더 다양한 "리치 값"도 저장할 수 있습니다.

예를 들어, "구매" 버튼의 색상을 세 가지 중 하나로 실험하려면, 기능 정의에서 불리언 대신 문자열을 반환하세요.

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

기능의 실제 값을 얻으려면 `value` 메서드를 사용합니다.

```php
$color = Feature::value('purchase-button');
```

Pennant의 Blade 지시어로 각 값에 따라 조건부 렌더링도 할 수 있습니다.

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire'가 활성 -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green'이 활성 -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange'가 활성 -->
@endfeature
```

> [!NOTE]   
> 리치 값을 사용할 때, 기능의 값이 `false`가 아닌 값이면 "활성"으로 간주합니다.

[조건부 `when`](#conditional-execution) 메서드에서는 리치 값이 첫 번째 클로저에 전달됩니다.

    Feature::when('purchase-button',
        fn ($color) => /* ... */,
        fn () => /* ... */,
    );

조건부 `unless` 메서드를 사용할 때는 두 번째 클로저에 리치 값이 전달됩니다.

    Feature::unless('purchase-button',
        fn () => /* ... */,
        fn ($color) => /* ... */,
    );

<a name="retrieving-multiple-features"></a>
## 여러 기능 한 번에 조회

`values` 메서드로 특정 스코프의 여러 기능 값을 한 번에 조회할 수 있습니다.

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

또는 `all` 메서드를 사용하면, 정의된 모든 기능 값을 조회할 수 있습니다.

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

단, 클래스 기반 기능은 동적으로 등록되므로, 해당 기능이 요청 중 한 번도 체크되지 않았다면 `all` 결과에 나타나지 않을 수 있습니다.

항상 클래스 기반 기능도 포함해서 조회하고 싶다면, Pennant의 기능 디스커버리 기능을 활성화할 수 있습니다. 애플리케이션 서비스 프로바이더에서 `discover` 메서드를 호출하세요.

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

이제 `all` 메서드가 요청 중 체크 여부와 관계없이 해당 디렉터리의 클래스 기반 기능까지 모두 포함해서 반환합니다.

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

Pennant는 요청 단위로 모든 기능 값을 메모리 내에 캐싱하지만, 반복적 체크가 잦은 곳에서는 여전히 성능 이슈가 발생할 수 있습니다. 이를 개선하기 위해 Pennant는 기능 값을 미리 로딩(eager loading)할 수 있습니다.

예시로, 루프 내에서 여러 사용자에 대해 기능 상태를 확인하는 상황입니다.

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

만약 데이터베이스 드라이버를 사용한다면, 사용자마다 한 번씩 DB 쿼리가 발생합니다. `load` 메서드로 기능 값을 미리 로드하면 이 문제를 피할 수 있습니다.

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

이미 로드된 값이 있으면 제외하고 로드하려면 `loadMissing` 메서드를 사용하세요.

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

모든 기능 값을 한 번에 로드하려면 `loadAll` 메서드를 사용합니다.

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
## 값 업데이트

처음 기능 값이 결정되면, 그 결과는 드라이버에 저장됩니다. 이는 여러 요청에 걸쳐 일관된 경험을 보장하기 위함입니다. 필요에 따라 기능의 저장값을 수동으로 변경할 수도 있습니다.

예를 들어, 아래와 같이 `activate`와 `deactivate` 메서드로 기능을 "켜고/끄기" 할 수 있습니다.

```php
use Laravel\Pennant\Feature;

// 기본 스코프에 대해 기능 활성화...
Feature::activate('new-api');

// 특정 스코프(예: 팀)에 대해 기능 비활성화...
Feature::for($user->team)->deactivate('billing-v2');
```

리치 값도 아래처럼 직접 지정해서 저장할 수 있습니다.

```php
Feature::activate('purchase-button', 'seafoam-green');
```

기능의 저장된 값을 잊고(Forget) 초기 정의로 되돌리려면 `forget` 메서드를 사용하세요.

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### 대량 업데이트

여러 스코프에 저장된 기능 값을 한꺼번에 변경하려면, `activateForEveryone`, `deactivateForEveryone` 메서드를 사용합니다.

예를 들어, `new-api`의 안정성에 자신이 있고 `'purchase-button'` 색상도 확정했다면, 다음과 같이 전체 사용자에게 적용할 수 있습니다.

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

또는 모든 사용자에게 기능을 비활성화할 때:

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]   
> 이 작업은 Pennant의 저장 드라이버에 저장된 값만 변경합니다. 앱의 기능 정의 역시 변경해야 활성/비활성 상태가 그대로 유지됩니다.

<a name="purging-features"></a>
### 기능 삭제(Purging)

때로는 기능을 저장소에서 완전히 삭제(purge)하는 것이 편리할 수 있습니다. 예를 들어 기능을 삭제했거나, 정의를 바꾸고 싶을 때 등입니다.

아래처럼 `purge` 메서드로 특정 기능의 저장값을 모두 삭제할 수 있습니다.

```php
// 단일 기능 삭제
Feature::purge('new-api');

// 복수 기능 삭제
Feature::purge(['new-api', 'purchase-button']);
```

아무 인자 없이 호출하면 **모든 기능**을 삭제할 수 있습니다.

```php
Feature::purge();
```

배포 과정에서 purge 작업이 자주 필요한 경우, Pennant의 Artisan 명령어 `pennant:purge`를 사용할 수 있습니다.

```sh
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

특정 기능만 남기고 **나머지 모두** 삭제하고 싶다면 `--except` 옵션을 이용하세요.

```sh
php artisan pennant:purge --except=new-api --except=purchase-button
```

`--except-registered` 플래그로, 서비스 프로바이더 등에 명시적으로 등록된 기능만 남길 수도 있습니다.

```sh
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## 테스트

기능 플래그가 사용된 코드를 테스트할 때, 테스트 내에서 기능의 반환값을 쉽게 제어하려면 기능을 재정의하면 됩니다. 예를 들어, 아래처럼 기능이 서비스 프로바이더에 정의되어 있다고 합시다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

테스트에서는 아래처럼 단일 값으로 재정의해 원하는 결과를 얻을 수 있습니다.

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

클래스 기반 기능에도 동일한 방식이 적용됩니다.

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

기능이 `Lottery` 인스턴스를 반환하는 경우, [별도 테스트 헬퍼](/docs/{{version}}/helpers#testing-lotteries)가 제공됩니다.

<a name="store-configuration"></a>
#### 저장소(store) 설정

테스트 중 사용할 Pennant 저장소는 `phpunit.xml` 파일의 `PENNANT_STORE` 환경변수로 지정할 수 있습니다.

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
#### 드라이버 구현하기

Pennant의 기존 저장 드라이버로 충분하지 않다면, 직접 저장 드라이버를 구현할 수 있습니다. 커스텀 드라이버는 `Laravel\Pennant\Contracts\Driver` 인터페이스를 구현해야 합니다.

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

이제 Redis 연결을 이용해 각 메서드를 구현하면 됩니다. 구체적 예시는 [Pennant 소스코드](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)의 `DatabaseDriver`를 참고하세요.

> [!NOTE]
> Laravel은 확장 클래스를 보관할 디렉터리를 기본 제공하지 않습니다. 원하는 위치에 생성하면 되며, 예시에서는 `Extensions` 디렉터리를 사용합니다.

<a name="registering-the-driver"></a>
#### 드라이버 등록하기

드라이버를 구현했다면, 이제 Laravel에 등록해야 합니다. Pennant에 추가 드라이버를 등록하려면 Feature 파사드의 `extend` 메서드를 사용하세요. 보통 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers)에서 `boot` 메서드 내에 작성합니다.

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

드라이버가 등록된 후 `config/pennant.php`에서 아래처럼 지정할 수 있습니다.

    'stores' => [

        'redis' => [
            'driver' => 'redis',
            'connection' => null,
        ],

        // ...

    ],

<a name="defining-features-externally"></a>
### 외부에서 기능 정의하기

서드파티 기능 플래그 플랫폼의 래퍼 드라이버라면, 보통 Pennant의 `Feature::define`이 아니라 외부 플래그 플랫폼에서 기능을 정의하게 됩니다. 이 경우, 커스텀 드라이버에서 `Laravel\Pennant\Contracts\DefinesFeaturesExternally` 인터페이스도 구현해야 합니다.

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

`definedFeaturesForScope` 메서드는 주어진 스코프에 대해 정의된 기능 목록을 반환해야 합니다.

<a name="events"></a>
## 이벤트

Pennant는 기능 플래그 추적에 유용한 다양한 이벤트를 dispatch합니다.

### `Laravel\Pennant\Events\FeatureRetrieved`

[기능이 체크될 때](#checking-features)마다 dispatch됩니다. 기능 사용량 추적에 활용할 수 있습니다.

### `Laravel\Pennant\Events\FeatureResolved`

특정 스코프에 대해 기능 값이 처음 결정될 때 dispatch됩니다.

### `Laravel\Pennant\Events\UnknownFeatureResolved`

특정 스코프에 대해 처음으로 존재하지 않는 기능이 체크될 때 dispatch됩니다. 의도치 않게 남아있는 기능 참조가 있는지 파악하는 데 도움이 됩니다.

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

[클래스 기반 기능](#class-based-features)의 첫 체크 시(동적으로 등록될 때) dispatch됩니다.

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

기능 정의에 [null 지원이 없는](#nullable-scope) 경우에 null 스코프가 주어질 때 dispatch됩니다.

이 상황은 기본적으로 오류가 아닌 `false` 반환으로 처리됩니다. 만약 이 기본 동작을 변경하고 싶다면, 아래처럼 이벤트 리스너에서 원하는 처리를 할 수 있습니다.

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

기능이 `activate` 또는 `deactivate` 등으로 갱신될 때 dispatch됩니다.

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

`activateForEveryone`, `deactivateForEveryone`로 전체 스코프에 대해 업데이트할 때 dispatch됩니다.

### `Laravel\Pennant\Events\FeatureDeleted`

`forget` 등으로 기능이 삭제될 때 dispatch됩니다.

### `Laravel\Pennant\Events\FeaturesPurged`

특정 기능들에 대해 purge 작업이 실행될 때 dispatch됩니다.

### `Laravel\Pennant\Events\AllFeaturesPurged`

모든 기능이 purge될 때 dispatch됩니다.