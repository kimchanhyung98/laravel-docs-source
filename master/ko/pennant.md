# Laravel Pennant

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
- [기능 정의하기](#defining-features)
    - [클래스 기반 기능](#class-based-features)
- [기능 확인하기](#checking-features)
    - [조건부 실행](#conditional-execution)
    - [`HasFeatures` 트레이트](#the-has-features-trait)
    - [Blade 지시어](#blade-directive)
    - [미들웨어](#middleware)
    - [기능 체크 인터셉트하기](#intercepting-feature-checks)
    - [인-메모리 캐시](#in-memory-cache)
- [스코프](#scope)
    - [스코프 지정하기](#specifying-the-scope)
    - [기본 스코프](#default-scope)
    - [널러블 스코프](#nullable-scope)
    - [스코프 식별하기](#identifying-scope)
    - [스코프 직렬화하기](#serializing-scope)
- [풍부한 기능 값](#rich-feature-values)
- [여러 기능 조회하기](#retrieving-multiple-features)
- [지연 로딩 (Eager Loading)](#eager-loading)
- [값 업데이트하기](#updating-values)
    - [일괄 업데이트](#bulk-updates)
    - [기능 정리하기 (Purging)](#purging-features)
- [테스트](#testing)
- [사용자 정의 Pennant 드라이버 추가하기](#adding-custom-pennant-drivers)
    - [드라이버 구현하기](#implementing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
    - [기능을 외부에서 정의하기](#defining-features-externally)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Pennant](https://github.com/laravel/pennant)는 심플하고 가벼운 기능 플래그(feature flag) 패키지로, 불필요한 복잡함이 없습니다. 기능 플래그를 이용하면 새로운 애플리케이션 기능을 점진적이고 자신 있게 배포하며, A/B 테스트로 인터페이스 디자인을 시험하거나 trunk-based 개발 전략을 보완하는 등 다양하게 활용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저로 Pennant를 프로젝트에 설치하세요:

```shell
composer require laravel/pennant
```

그다음, `vendor:publish` Artisan 명령어를 사용하여 Pennant의 설정 파일과 마이그레이션 파일을 공개하세요:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행하면 Pennant가 사용하는 `features` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
## 설정

Pennant의 자산을 공개한 뒤에는 `config/pennant.php` 경로에 설정 파일이 위치합니다. 이 설정 파일을 통해 Pennant가 기능 플래그 값을 저장하는 기본 스토리지 방식을 지정할 수 있습니다.

Pennant는 `array` 드라이버를 통해 인-메모리 배열에 기능 플래그 값을 저장하는 방식을 지원합니다. 또한, 기본값인 `database` 드라이버를 사용해 관계형 데이터베이스에 지속적으로 저장할 수도 있습니다.

<a name="defining-features"></a>
## 기능 정의하기

기능을 정의하기 위해서는 `Feature` 파사드가 제공하는 `define` 메서드를 사용할 수 있습니다. 기능 이름과 초기 값을 계산하기 위한 클로저(콜백)를 제공해야 합니다.

일반적으로 서비스 프로바이더 내에서 `Feature` 파사드를 사용해 기능을 정의합니다. 이 클로저는 기능 체크의 "스코프"를 인수로 받으며, 보통 현재 인증된 사용자가 스코프가 됩니다. 예를 들어, 특정 사용자에게 새로운 API를 단계적으로 배포하는 기능을 정의할 수 있습니다:

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
     * 부트스트랩 애플리케이션 서비스 입니다.
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

위 예제에서 기능의 규칙은 다음과 같습니다:

- 모든 내부 팀 멤버는 새로운 API를 사용합니다.
- 고트래픽 고객은 새로운 API를 사용하지 않습니다.
- 그 외 경우에는 1% 확률로 기능을 활성화합니다.

`new-api` 기능이 특정 사용자에 대해 처음 체크될 때, 이 클로저 계산 결과가 저장소 드라이버에 저장됩니다. 이후 동일 사용자에 대해 기능 체크 시 저장된 값이 사용되며 클로저는 호출되지 않습니다.

만약 기능 정의가 무작위 배정만 한다면 클로저를 생략할 수도 있습니다:

```php
Feature::define('site-redesign', Lottery::odds(1, 1000));
```

<a name="class-based-features"></a>
### 클래스 기반 기능

Pennant는 클래스 기반 기능도 지원합니다. 클로저 기반 기능과 달리 서비스 프로바이더에서 별도 등록할 필요가 없습니다. 클래스 기반 기능은 `pennant:feature` Artisan 명령어로 생성합니다. 기본적으로 `app/Features` 디렉토리에 생성됩니다:

```shell
php artisan pennant:feature NewApi
```

기능 클래스 작성 시 `resolve` 메서드만 정의하면 되며, 이 메서드는 주어진 스코프에 대해 기능의 초기 값을 반환합니다. 스코프는 보통 현재 인증된 사용자입니다:

```php
<?php

namespace App\Features;

use App\Models\User;
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

직접 클래스 기반 기능 인스턴스를 불러올 때는 `Feature` 파사드의 `instance` 메서드를 이용하세요:

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]
> 기능 클래스는 [컨테이너](/docs/master/container)를 통해 해석되므로, 필요시 생성자 의존성 주입이 가능합니다.

#### 저장될 기능 이름 커스터마이징

기본적으로 Pennant는 기능 클래스의 FQCN(완전한 클래스명)을 저장합니다. 애플리케이션 구조와 독립적인 이름으로 저장하려면, 클래스에 `$name` 속성을 지정하세요. 이 값이 저장됩니다:

```php
<?php

namespace App\Features;

class NewApi
{
    /**
     * 저장할 기능 이름입니다.
     *
     * @var string
     */
    public $name = 'new-api';

    // ...
}
```

<a name="checking-features"></a>
## 기능 확인하기

기능이 활성화되었는지 확인하려면 `Feature` 파사드의 `active` 메서드를 사용합니다. 기본적으로 현재 인증된 사용자를 대상으로 체크합니다:

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

기능 체크 기본값은 현재 인증된 사용자지만, `Feature::for` 메서드를 사용하여 다른 사용자나 [스코프](#scope)에 대해서도 쉽게 체크할 수 있습니다:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

또한 유용한 편의 메서드도 제공합니다:

```php
// 주어진 모든 기능이 활성인지 확인
Feature::allAreActive(['new-api', 'site-redesign']);

// 주어진 기능 중 하나라도 활성인지 확인
Feature::someAreActive(['new-api', 'site-redesign']);

// 기능이 비활성인지 확인
Feature::inactive('new-api');

// 주어진 기능 모두 비활성인지 확인
Feature::allAreInactive(['new-api', 'site-redesign']);

// 주어진 기능 중 하나라도 비활성인지 확인
Feature::someAreInactive(['new-api', 'site-redesign']);
```

> [!NOTE]
> HTTP 컨텍스트 밖(예: Artisan 커맨드, 큐 작업)에서 Pennant를 사용할 경우 기능 스코프를 [명시적으로 지정](#specifying-the-scope)하는 것이 좋습니다. 또는 [기본 스코프](#default-scope)를 설정하여 인증/비인증 모두를 처리할 수도 있습니다.

<a name="checking-class-based-features"></a>
#### 클래스 기반 기능 확인하기

클래스 기반 기능은 기능 체크 시 클래스명을 제공해야 합니다:

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
### 조건부 실행

기능이 활성화된 경우 특정 코드 블록을 실행할 때는 `when` 메서드를 사용합니다. 두 번째 인자로 기능이 비활성일 때 실행할 클로저도 전달할 수 있습니다:

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
        return Feature::when(NewApi::class,
            fn () => $this->resolveNewApiResponse($request),
            fn () => $this->resolveLegacyApiResponse($request),
        );
    }

    // ...
}
```

`unless` 메서드는 `when`의 반대로, 기능이 비활성일 때 첫 번째 클로저를 실행합니다:

```php
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
### `HasFeatures` 트레이트

Pennant의 `HasFeatures` 트레이트는 `User` 모델(또는 기능이 관련된 다른 모델)에 추가해, 모델에서 바로 편리하게 기능을 체크할 수 있게 해줍니다:

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

트레이트를 추가하면 `features` 메서드 호출만으로 기능 상태를 쉽게 확인할 수 있습니다:

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

물론 `features` 메서드는 기능과 상호작용하는 다양한 편의 메서드를 제공합니다:

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
### Blade 지시어

Blade 뷰에서 기능 체크를 쉽게 하도록 `@feature` 와 `@featureany` 지시어를 제공합니다:

```blade
@feature('site-redesign')
    <!-- 'site-redesign' 기능이 활성인 경우 -->
@else
    <!-- 'site-redesign' 기능이 비활성인 경우 -->
@endfeature

@featureany(['site-redesign', 'beta'])
    <!-- 'site-redesign' 혹은 'beta' 기능이 활성인 경우 -->
@endfeatureany
```

<a name="middleware"></a>
### 미들웨어

Pennant는 특정 기능이 활성화된 경우에만 라우트 접근을 허용하는 미들웨어도 제공합니다. 라우트에 미들웨어를 할당하고 필수 기능을 지정하세요. 활성화되지 않은 기능이 있을 경우 `400 Bad Request` 응답을 반환합니다. 여러 기능은 `using` 정적 메서드에 전달할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### 응답 커스터마이징

비활성 기능 발견 시 미들웨어가 반환하는 응답을 사용자 정의하려면, 보통 애플리케이션 서비스 프로바이더의 `boot` 메서드 내에서 `EnsureFeaturesAreActive::whenInactive` 메서드를 호출하세요:

```php
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

/**
 * 애플리케이션 서비스 부트스트랩
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
### 기능 체크 인터셉트하기

가끔 저장된 기능 값을 불러오기 전에 인-메모리 상태로 먼저 체크하고 싶을 때가 있습니다. 예를 들어, 새로운 API가 버그가 있어 내부 팀원만 접근 가능하도록 임시로 비활성화 하고 싶거나, 특정 날짜부터 전사적으로 기능을 롤아웃하고 싶을 때 유용합니다.

클래스 기반 기능의 `before` 메서드를 활용하세요. 이 메서드는 저장된 값 조회 전 항상 실행되고, `null`이 아닌 값을 반환하면 요청 동안 해당 값이 저장된 값을 대체합니다:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * 저장된 값 조회 전 항상 실행되는 인-메모리 체크
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }
    }

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

글로벌 롤아웃 일정 등에도 활용할 수 있습니다:

```php
<?php

namespace App\Features;

use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Config;

class NewApi
{
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
### 인-메모리 캐시

기능 체크 시 Pennant는 결과를 인-메모리 캐시에 저장합니다. `database` 드라이버 사용 시, 같은 요청 내에서 동일 기능을 재차 체크해도 추가 DB 쿼리는 없습니다. 이렇게 하면 요청 동안 일관된 결과를 보증합니다.

인-메모리 캐시를 수동으로 초기화하려면 `Feature::flushCache()` 메서드를 사용하세요:

```php
Feature::flushCache();
```

<a name="scope"></a>
## 스코프

<a name="specifying-the-scope"></a>
### 스코프 지정하기

기능 체크 기본값은 현재 인증된 사용자입니다. 하지만 필요에 따라 다른 스코프를 지정할 수 있습니다. `Feature::for` 메서드에 원하는 스코프를 전달하면 됩니다:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

스코프는 사용자에 국한되지 않습니다. 예를 들어, 팀 전체 대상의 새 청구 경험을 롤아웃하는 경우가 있다고 가정해 보겠습니다. 오래된 팀일수록 롤아웃 속도를 늦추고 싶을 수 있습니다:

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

이 기능 정의에서는 `User` 대신 `Team` 모델이 스코프입니다. 따라서 기능 체크 시 유저의 팀을 `for` 메서드에 넘겨야 합니다:

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### 기본 스코프

Pennant가 기능 체크 시 기본으로 사용하는 스코프를 커스터마이징할 수 있습니다. 예를 들어 모든 기능을 현재 인증된 사용자의 팀으로 체크한다면, 매번 `Feature::for($user->team)`을 호출하는 대신 기본 스코프를 팀으로 지정할 수 있습니다. 보통 서비스 프로바이더 내에서 설정합니다:

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

명시적으로 `for` 메서드가 호출되지 않으면 이제 현재 인증된 사용자의 팀이 스코프로 사용됩니다:

```php
Feature::active('billing-v2');

// 위와 동일:

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### 널러블 스코프

기능 체크 시 스코프로 `null`이 전달되고, 기능 정의가 널(NULL) 지원 타입(널러블 타입이나 유니언 타입에 null 포함)을 지원하지 않으면 Pennant는 자동으로 `false`를 반환합니다.

따라서 스코프가 `null`일 가능성이 있고 기능의 값 해석기를 실행하고 싶다면, 기능 정의에서 `null` 지원을 처리해야 합니다. `null` 스코프 상황은 Artisan 커맨드, 큐 작업, 인증 필요 없는 라우트 등에서 발생할 수 있습니다.

명시적으로 [기능 스코프를 지정하지 않는 경우](#specifying-the-scope), 아래와 같이 스코프 타입에 `null`을 포함시키고 `null` 처리 로직을 작성하세요:

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

Pennant 내장 `array` 및 `database` 스토리지 드라이버는 모든 PHP 데이터 타입과 Eloquent 모델의 스코프 식별자를 적절히 저장하는 방법을 알고 있습니다. 하지만 서드파티 Pennant 드라이버는 Eloquent 모델이나 커스텀 타입을 올바르게 저장하지 못할 수도 있습니다.

이 경우, Pennant는 `FeatureScopeable` 계약을 구현해 스코프 객체를 저장 가능한 식별자로 변환할 수 있게 합니다.

예를 들어, `database` 드라이버와 서드파티 "Flag Rocket" 드라이버를 함께 사용하는 애플리케이션에서, "Flag Rocket" 드라이버가 Eloquent 모델 대신 `FlagRocketUser` 인스턴스를 필요로 한다고 할 때 다음과 같이 구현할 수 있습니다:

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * 드라이버 별 기능 스코프 식별자로 변환합니다.
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

기본적으로 Pennant는 Eloquent 모델에 연결된 기능 저장 시 클래스의 FQCN을 사용합니다. 만약 이미 [Eloquent 모프 맵(morph map)](/docs/master/eloquent-relationships#custom-polymorphic-types)을 사용 중이라면, Pennant가 모프 맵을 사용하도록 하여 기능 저장과 애플리케이션 구조를 분리할 수 있습니다.

모프 맵을 서비스 프로바이더에서 정의한 후 `Feature` 파사드의 `useMorphMap` 메서드를 호출하세요:

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

지금까지 기능을 `true` 또는 `false` 와 같은 이진 상태로만 설명했지만, Pennant는 풍부한 값도 저장할 수 있습니다.

예를 들어, "구매 버튼" 색상을 세 가지 버전으로 테스트한다고 가정해 보겠습니다. 기능 정의에서 `true`/`false` 대신 문자열을 반환하도록 할 수 있습니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

`purchase-button` 기능 값은 `value` 메서드로 조회할 수 있습니다:

```php
$color = Feature::value('purchase-button');
```

Blade 지시어를 이용해 현재 값에 따라 조건부 렌더링도 가능합니다:

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
> 풍부한 값을 사용하는 경우, 값이 `false`가 아니면 기능이 "활성"으로 간주된다는 것을 유의하세요.

[조건부 `when`](#conditional-execution) 메서드 호출 시 첫 번째 클로저에 풍부한 기능 값이 전달됩니다:

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

또한 `unless` 메서드 호출 시, 두 번째 클로저(선택 사항)에 풍부한 값이 전달됩니다:

```php
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>
## 여러 기능 조회하기

`values` 메서드로 주어진 스코프에 대해 여러 기능을 한번에 조회할 수 있습니다:

```php
Feature::values(['billing-v2', 'purchase-button']);

// 결과 예시
// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

또는 `all` 메서드를 사용해 해당 스코프에 정의된 모든 기능 값을 가져올 수도 있습니다:

```php
Feature::all();

// 결과 예시
// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

하지만 클래스 기반 기능은 동적으로 등록되므로, 명시적으로 체크되기 전까지 `all` 결과에 포함되지 않습니다.

`all` 메서드에 클래스 기반 기능 포함을 보장하려면 Pennant의 기능 탐색 기능을 사용하세요. 서비스 프로바이더에서 `discover` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Feature::discover();

        // ...
    }
}
```

이제 `all` 메서드는 `app/Features` 내 클래스 기반 기능들을 포함해 반환합니다:

```php
Feature::all();

// 결과 예시:
// [
//     'App\Features\NewApi' => true,
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

<a name="eager-loading"></a>
## 지연 로딩 (Eager Loading)

Pennant는 요청 내 인-메모리 캐시를 유지하지만, 반복문 등에서 기능 확인 시 성능 문제를 겪을 수도 있습니다. 이를 완화하기 위해 기능 값을 일괄 미리 불러오는 기능을 제공합니다.

예를 들어, 여러 사용자를 반복하며 기능을 체크하는 코드를 가정해 보겠습니다:

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

기본적으로 데이터베이스 드라이버를 사용한다면 사용자의 수만큼 쿼리가 실행됩니다. 하지만, `load` 메서드로 기능을 미리 불러오면 성능 병목을 제거할 수 있습니다:

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

이미 로드된 경우에만 추가 로드를 하는 `loadMissing` 메서드도 있습니다:

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

모든 정의된 기능을 불러오려면 `loadAll` 메서드를 사용하세요:

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
## 값 업데이트하기

기능 값이 최초 해석되면 스토리지에 저장되어 사용자 경험의 일관성을 보장합니다. 하지만 필요에 따라 저장된 값을 직접 변경할 수도 있습니다.

`activate` 및 `deactivate` 메서드로 기능을 활성화하거나 비활성화할 수 있습니다:

```php
use Laravel\Pennant\Feature;

// 기본 스코프에 대해 기능 활성화...
Feature::activate('new-api');

// 특정 스코프에 대해 기능 비활성화...
Feature::for($user->team)->deactivate('billing-v2');
```

`activate` 메서드의 두 번째 인수로 풍부한 값을 지정할 수도 있습니다:

```php
Feature::activate('purchase-button', 'seafoam-green');
```

저장된 값을 잊게 하려면 `forget` 메서드를 호출하세요. 다시 기능 체크 시 정의된 값으로 재해석됩니다:

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### 일괄 업데이트

저장된 기능 값을 모두 일괄 변경하려면 `activateForEveryone` 및 `deactivateForEveryone` 메서드를 사용하세요.

예를 들어, `new-api` 기능이 안정화되었고 `'purchase-button'` 색상을 확정한 경우 다음처럼 모든 사용자에 업데이트할 수 있습니다:

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

전체 비활성화도 가능합니다:

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> 이 작업은 저장소에 저장된 값만 변경하며, 애플리케이션 내 기능 정의는 별도로 수정해야 합니다.

<a name="purging-features"></a>
### 기능 정리하기 (Purging)

기능을 완전히 스토리지에서 삭제하고 싶을 때가 있습니다. 보통 기능을 제거했거나 정의를 변경해 전체 사용자 재롤아웃이 필요한 경우에 사용합니다.

`purge` 메서드로 기능별 저장된 모든 값을 삭제할 수 있습니다:

```php
// 단일 기능 정리...
Feature::purge('new-api');

// 여러 기능 정리...
Feature::purge(['new-api', 'purchase-button']);
```

전체 기능을 모두 정리하려면 인수 없이 호출하세요:

```php
Feature::purge();
```

배포 과정에서 기능 정리를 자동화할 수 있도록 `pennant:purge` Artisan 명령도 제공합니다:

```shell
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

특정 기능 목록을 제외하고 모두 정리하려면 `--except` 옵션을 사용하세요:

```shell
php artisan pennant:purge --except=new-api --except=purchase-button
```

또한, `--except-registered` 옵션으로 서비스 프로바이더에 명시적 등록된 기능만 제외할 수 있습니다:

```shell
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## 테스트

기능 플래그가 동작하는 코드를 테스트할 때 가장 쉬운 방법은 테스트 시작시 기능을 재정의하는 것입니다. 예를 들어, 서비스 프로바이더에 다음 기능이 정의되어 있다고 가정하세요:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

테스트 안에서 기능 값을 바꾸고 싶다면, 테스트 콜백 초기에 다시 정의하세요. 아래 시험은 항상 통과합니다:

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

클래스 기반 기능도 동일하게 재정의할 수 있습니다:

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

`Lottery` 인스턴스를 반환하는 기능에 대해서는 유용한 [테스트 헬퍼](/docs/master/helpers#testing-lotteries)도 있습니다.

<a name="store-configuration"></a>
#### 테스트용 스토어 설정

테스트 중 Pennant가 어떤 스토어를 사용할지 환경변수 `PENNANT_STORE`를 `phpunit.xml`에 정의해 설정할 수 있습니다:

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
### 드라이버 구현하기

기본 드라이버가 애플리케이션 요구를 충족하지 못한다면 직접 드라이버를 작성할 수 있습니다. 직접 작성한 드라이버는 `Laravel\Pennant\Contracts\Driver` 인터페이스를 구현해야 합니다:

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

이어서 Redis 커넥션을 이용해 각 메서드를 구현하세요. 구현 방법은 Pennant 소스 코드(`Laravel\Pennant\Drivers\DatabaseDriver`)를 참고하면 도움이 됩니다.

> [!NOTE]
> Laravel은 확장 코드를 위한 특정 디렉토리를 제공하지 않으므로, 원하는 경로에 자유롭게 작성하세요. 여기선 `Extensions` 디렉토리에 `RedisFeatureDriver`를 둔 예시입니다.

<a name="registering-the-driver"></a>
### 드라이버 등록하기

드라이버를 완성했다면 Laravel에 등록하세요. `Feature` 파사드의 `extend` 메서드로 새 드라이버를 추가할 수 있으며, 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Feature::extend('redis', function (Application $app) {
            return new RedisFeatureDriver($app->make('redis'), $app->make('events'), []);
        });
    }
}
```

등록 완료 후 `config/pennant.php` 설정 파일에 다음과 같이 드라이버를 추가해 사용할 수 있습니다:

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
### 기능을 외부에서 정의하기

만약 드라이버가 서드파티 기능 플래그 플랫폼 래퍼라면, Pennant의 `Feature::define` 메서드를 사용하지 않고 해당 플랫폼에서 기능을 정의할 가능성이 큽니다. 이 경우, 커스텀 드라이버는 `Laravel\Pennant\Contracts\DefinesFeaturesExternally` 인터페이스도 구현해야 합니다:

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;
use Laravel\Pennant\Contracts\DefinesFeaturesExternally;

class FeatureFlagServiceDriver implements Driver, DefinesFeaturesExternally
{
    /**
     * 주어진 스코프에 정의된 기능 목록을 반환합니다.
     */
    public function definedFeaturesForScope(mixed $scope): array {}

    /* ... */
}
```

`definedFeaturesForScope` 메서드는 전달받은 스코프에 대해 정의된 기능 이름 리스트를 반환해야 합니다.

<a name="events"></a>
## 이벤트

Pennant는 애플리케이션 내 기능 플래그 동작을 추적하는 데 유용한 여러 이벤트를 발생시킵니다.

### `Laravel\Pennant\Events\FeatureRetrieved`

기능이 [체크될 때](#checking-features)마다 발생합니다. 기능 사용 빈도나 지표 추적에 유용합니다.

### `Laravel\Pennant\Events\FeatureResolved`

특정 스코프에 대해 기능 값이 최초로 해석될 때 발생합니다.

### `Laravel\Pennant\Events\UnknownFeatureResolved`

알 수 없는 기능이 최초 해석될 때 발생합니다. 기능 플래그를 제거하려 했는데 코드에 남아있는 참조들을 찾아내는 데 도움됩니다:

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
     * 애플리케이션 서비스 부트스트랩
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

[클래스 기반 기능](#class-based-features)이 요청 중 최초로 동적 체크될 때 발생합니다.

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

널 스코프가 [지원하지 않는](#nullable-scope) 기능 정의에 전달될 때 발생합니다.

이 상황은 내부적으로 잘 처리되어 기능은 `false`를 반환합니다. 하지만 기본 동작을 비활성화하고 싶다면 서비스 프로바이더의 `boot` 메서드에서 이 이벤트 리스너를 등록할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;
use Laravel\Pennant\Events\UnexpectedNullScopeEncountered;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Event::listen(UnexpectedNullScopeEncountered::class, fn () => abort(500));
}
```

### `Laravel\Pennant\Events\FeatureUpdated`

주로 `activate`, `deactivate` 호출 시 스코프 대상 기능 업데이트 시 발생합니다.

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

대상 스코프 없이 모든 스코프에 대해 기능 업데이트 시 발생합니다(`activateForEveryone`, `deactivateForEveryone`).

### `Laravel\Pennant\Events\FeatureDeleted`

주로 `forget` 호출로 스코프 대상 기능이 삭제될 때 발생합니다.

### `Laravel\Pennant\Events\FeaturesPurged`

특정 기능 저장값 정리 시 발생합니다.

### `Laravel\Pennant\Events\AllFeaturesPurged`

모든 기능 저장값 정리 시 발생합니다.