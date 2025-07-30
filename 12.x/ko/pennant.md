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
    - [기능 확인 가로채기](#intercepting-feature-checks)
    - [인메모리 캐시](#in-memory-cache)
- [스코프](#scope)
    - [스코프 지정하기](#specifying-the-scope)
    - [기본 스코프](#default-scope)
    - [널 가능 스코프](#nullable-scope)
    - [스코프 식별](#identifying-scope)
    - [스코프 직렬화](#serializing-scope)
- [풍부한 기능 값](#rich-feature-values)
- [여러 기능 조회하기](#retrieving-multiple-features)
- [지연 로딩](#eager-loading)
- [값 업데이트하기](#updating-values)
    - [일괄 업데이트](#bulk-updates)
    - [기능 초기화](#purging-features)
- [테스트](#testing)
- [커스텀 Pennant 드라이버 추가하기](#adding-custom-pennant-drivers)
    - [드라이버 구현하기](#implementing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
    - [외부에서 기능 정의하기](#defining-features-externally)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Pennant](https://github.com/laravel/pennant)는 불필요한 부분 없이 간단하고 가벼운 기능 플래그 패키지입니다. 기능 플래그는 새 애플리케이션 기능을 점진적으로 안전하게 배포하거나, 새로운 인터페이스 디자인에 대한 A/B 테스트, trunk 기반 개발 전략 보완 등 다양한 용도로 활용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 사용해 Pennant를 프로젝트에 설치하세요:

```shell
composer require laravel/pennant
```

그다음, `vendor:publish` Artisan 명령어를 이용해 Pennant의 설정 및 마이그레이션 파일을 퍼블리시하세요:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행하세요. 이 과정에서 Pennant의 `database` 드라이버가 사용하는 `features` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
## 설정

Pennant의 애셋을 퍼블리시하면 `config/pennant.php`에 설정 파일이 위치합니다. 이 설정 파일에서는 Pennant가 기능 플래그 값을 저장할 기본 저장소 방식을 지정할 수 있습니다.

Pennant는 `array` 드라이버를 통해 인메모리 배열에 기능 값을 저장할 수 있도록 지원하며, 기본적으로는 관계형 데이터베이스에 기능 값을 영구 저장하는 `database` 드라이버를 사용합니다.

<a name="defining-features"></a>
## 기능 정의하기

기능을 정의하려면 `Feature` 퍼사드의 `define` 메서드를 사용하며, 기능 이름과 초기 값을 결정하는 클로저를 제공해야 합니다.

보통 기능 정의는 서비스 프로바이더 안에서 `Feature` 퍼사드를 통해 이루어집니다. 클로저에는 기능 체크의 "스코프"(주로 현재 인증된 사용자)가 전달됩니다. 예를 들어, 점진적으로 새 API를 사용자에게 배포하는 기능을 정의하는 코드는 다음과 같습니다:

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

위 정의의 규칙은 다음과 같습니다:

- 모든 내부 팀원은 새 API를 사용해야 합니다.
- 트래픽이 많은 고객은 새 API를 사용하지 않습니다.
- 그 외엔 100분의 1 확률로 새 API를 할당받습니다.

`new-api` 기능이 특정 사용자에 대해 처음 체크될 때 클로저 결과가 저장되고, 이후 동일 사용자 체크 시 저장된 값이 반환되어 클로저는 다시 실행되지 않습니다.

클로저가 단순히 복권 확률만 반환하는 경우, 클로저 대신 값을 바로 넘겨 생략할 수도 있습니다:

```
Feature::define('site-redesign', Lottery::odds(1, 1000));
```

<a name="class-based-features"></a>
### 클래스 기반 기능

Pennant는 클래스 기반 기능 정의도 지원합니다. 클로저 기반과 달리 서비스 프로바이더에 등록할 필요가 없습니다. 클래스 기반 기능은 Artisan 명령어 `pennant:feature`로 생성하며, 기본적으로 애플리케이션 `app/Features` 디렉터리에 위치합니다:

```shell
php artisan pennant:feature NewApi
```

작성할 때는 `resolve` 메서드만 정의하면 됩니다. 이 메서드는 특정 스코프의 기능 초기 값을 반환합니다. 스코프는 주로 인증된 사용자입니다:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * 기능 초기 값을 결정합니다.
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

클래스 기반 기능 인스턴스를 명시적으로 생성할 필요가 있을 때는 `Feature` 퍼사드의 `instance` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]
> 기능 클래스는 [컨테이너](/docs/12.x/container)를 통해 해석되므로, 생성자에 의존성 주입이 가능합니다.

#### 저장되는 기능 이름 커스텀

기본적으로 Pennant는 클래스의 완전한 네임스페이스를 이름으로 저장합니다. 내부 구조와 저장 이름을 분리하고 싶다면, 클래스에 `$name` 속성을 정의해 이름을 지정할 수 있습니다:

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
## 기능 확인하기

기능이 활성화되었는지 확인하려면 `Feature` 퍼사드의 `active` 메서드를 사용하세요. 기본적으로 현재 인증된 사용자 기준으로 체크됩니다:

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

현재 인증된 사용자 외에 다른 사용자나 [스코프](#scope) 대상에 대해 체크할 수도 있습니다. `Feature` 퍼사드의 `for` 메서드를 사용해 스코프를 지정하세요:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

활성화 여부를 판단하는 데 유용한 추가 메서드들도 있습니다:

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
> Artisan 명령어나 큐 작업 등 HTTP 컨텍스트 밖에서 Pennant를 사용할 때는 보통 [명확히 스코프를 지정하는 것](#specifying-the-scope)이 좋습니다. 혹은 인증된 HTTP 컨텍스트와 인증되지 않은 컨텍스트 모두 고려하는 [기본 스코프](#default-scope)를 정의할 수도 있습니다.

<a name="checking-class-based-features"></a>
#### 클래스 기반 기능 확인하기

클래스 기반 기능을 확인할 때는 클래스명을 그대로 전달하세요:

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

`when` 메서드를 사용하면 기능이 활성화되었을 때만 클로저를 실행할 수 있습니다. 두 번째 클로저를 넘기면 비활성화되었을 때 실행됩니다:

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

`unless` 메서드는 `when`의 반대 역할로, 기능이 비활성 상태일 때 첫 번째 클로저를 실행합니다:

```php
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
### `HasFeatures` 트레이트

Pennant의 `HasFeatures` 트레이트를 `User` 모델 등 기능이 필요한 모델에 추가하면 모델 인스턴스에서 편리하게 기능을 확인할 수 있습니다:

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

트레이트를 추가하면 `features` 메서드로 쉽게 기능을 확인할 수 있습니다:

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

기능과 상호작용하기 위한 여러 편리한 메서드도 지원합니다:

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

Blade 안에서 기능을 쉽게 확인하도록 Pennant는 `@feature` 와 `@featureany` 디렉티브를 제공합니다:

```blade
@feature('site-redesign')
    <!-- 'site-redesign' 기능이 활성화됨 -->
@else
    <!-- 'site-redesign' 기능이 비활성화됨 -->
@endfeature

@featureany(['site-redesign', 'beta'])
    <!-- 'site-redesign' 혹은 'beta' 기능이 활성화됨 -->
@endfeatureany
```

<a name="middleware"></a>
### 미들웨어

Pennant는 현재 인증된 사용자가 특정 기능에 접근 권한을 갖고 있는지 라우트 접근 전에 확인하는 [미들웨어](/docs/12.x/middleware)를 제공합니다. 미들웨어에 기능 목록을 전달하면, 현재 사용자가 해당 기능들 중 하나라도 비활성일 경우 `400 Bad Request` 응답이 반환됩니다:

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### 응답 커스텀하기

미들웨어가 비활성 기능을 만났을 때 반환하는 응답을 직접 정의하려면 `EnsureFeaturesAreActive` 미들웨어의 `whenInactive` 메서드를 사용하세요. 보통 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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

어떤 경우에는 저장된 기능 값을 가져오기 전에 인메모리에서 별도 체크를 수행하는 것이 유용할 수 있습니다. 예를 들어, 새 API를 기능 플래그 뒤에서 개발 중이고, 버그 발견 시 기존 저장값을 잃지 않고 새 API를 일시 비활성화하고 싶을 수 있습니다.

클래스 기반 기능의 `before` 메서드를 활용하면, 저장된 값 조회 전에 항상 메모리 내에서 검사를 수행할 수 있습니다. 만약 `before`가 `null`이 아닌 값을 반환하면, 요청 동안 저장된 값 대신 해당 값을 사용합니다:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * 저장된 값 조회 전에 항상 메모리 내에서 검사 수행.
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }
    }

    /**
     * 기능 초기 값을 결정.
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

이 방법으로 과거 기능 플래그 뒤에 있었던 기능의 글로벌 롤아웃 일정도 관리할 수 있습니다:

```php
<?php

namespace App\Features;

use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Config;

class NewApi
{
    /**
     * 저장된 값 조회 전에 항상 메모리 내 검사 수행.
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

기능을 확인할 때 Pennant는 결과를 인메모리 캐시합니다. `database` 드라이버 사용 시, 같은 요청 내에서 반복적으로 같은 기능을 체크해도 추가 DB 쿼리를 발생시키지 않습니다. 또한, 요청 내내 일관된 기능 상태를 보장합니다.

인메모리 캐시를 수동으로 초기화하려면 `Feature` 퍼사드의 `flushCache` 메서드를 사용하세요:

```php
Feature::flushCache();
```

<a name="scope"></a>
## 스코프

<a name="specifying-the-scope"></a>
### 스코프 지정하기

앞서 설명했듯 기능은 보통 현재 인증된 사용자 기준으로 체크됩니다. 하지만 사용자 외 다른 스코프를 지정하고 싶을 때도 있습니다. `Feature` 퍼사드의 `for` 메서드에 원하는 스코프를 전달하세요:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

예를 들어 청구 기능을 개별 사용자가 아닌 팀 단위로 롤아웃하며, 오래된 팀일수록 느린 배포를 하려 한다고 가정해보겠습니다. 이 경우 스코프는 `User`가 아닌 `Team` 모델일 수 있습니다:

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

이렇게 정의된 기능을 사용자의 팀 기준으로 확인할 땐 `for` 메서드에 팀을 전달하세요:

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### 기본 스코프

Pennant가 기능 수행 시 기본으로 사용할 스코프도 커스텀할 수 있습니다. 예를 들어 모든 기능이 기본적으로 현재 인증된 사용자의 팀 기준이라면, 매번 `Feature::for($user->team)`을 호출할 필요 없이 서비스 프로바이더에서 기본 스코프를 지정할 수 있습니다:

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

이제 스코프를 명시하지 않아도 다음 두 호출이 동일하게 동작합니다:

```php
Feature::active('billing-v2');

// 동일 동작...

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### 널 가능 스코프

만약 기능 체크 시 스코프로 `null`이 전달되고, 기능 정의가 널 허용(nullable) 타입 또는 널 포함 유니온 타입을 지원하지 않으면 Pennant는 자동으로 기능을 비활성(결과 `false`)으로 판단합니다.

아티즌 명령어나 큐 작업, 인증되지 않은 라우트 등에서 기본 스코프가 `null`일 수 있기 때문에, 이러한 경우 기능 정의에서 널 가능 타입을 고려하고 처리하는 것이 좋습니다.

예시:

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

Pennant의 내장 `array` 및 `database` 드라이버는 PHP 기본 타입과 Eloquent 모델의 스코프 식별자를 올바르게 처리합니다. 하지만 서드파티 Pennant 드라이버를 사용하는 경우, Eloquent 모델 또는 사용자 정의 타입의 식별자를 제대로 처리하지 못할 수 있습니다.

이를 위해, 애플리케이션 내 Pennant 스코프로 사용하는 객체에 `FeatureScopeable` 계약을 구현해 스코프 값 변환을 커스텀할 수 있습니다.

예를 들어, 내장 `database` 드라이버와 서드파티 "Flag Rocket" 드라이버를 동시에 사용하고 있다고 가정해보겠습니다. "Flag Rocket" 드라이버는 Eloquent 모델을 직접 저장하지 않으며, 대신 `FlagRocketUser` 인스턴스가 필요합니다. 이때 아래처럼 구현할 수 있습니다:

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * 주어진 드라이버에 맞춰 객체를 기능 스코프 식별자로 캐스팅.
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

기본적으로 Pennant는 Eloquent 모델과 연관된 기능을 저장할 때 완전한 클래스 이름을 사용합니다. 만약 이미 [Eloquent morph map](/docs/12.x/eloquent-relationships#custom-polymorphic-types)을 사용하고 있다면, Pennant도 이 morph map을 사용해 저장 이름을 줄이고 내부 구조에 결합도를 낮출 수 있습니다.

이를 위해 서비스 프로바이더 내에서 morph map을 정의한 후 `Feature` 퍼사드의 `useMorphMap` 메서드를 호출하세요:

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

지금까지는 기능이 활성화/비활성 이진 상태인 예시를 주로 보여드렸지만, Pennant는 풍부한 값(리치 값)도 저장할 수 있습니다.

예를 들어, 애플리케이션의 "구매하기" 버튼에 대해 세 가지 새 색상을 테스트한다고 합시다. 기능 정의에서 `true` 또는 `false` 대신 문자열을 반환할 수 있습니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

`purchase-button` 기능 값을 `value` 메서드로 조회할 수 있습니다:

```php
$color = Feature::value('purchase-button');
```

Blade 디렉티브를 이용하면 현재 기능 값에 따라 조건부 렌더링도 간단합니다:

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire' 색상이 활성화됨 -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green' 색상이 활성화됨 -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange' 색상이 활성화됨 -->
@endfeature
```

> [!NOTE]
> 풍부한 값 사용 시, 값이 `false`가 아닌 한 기능을 "활성"으로 간주한다는 점을 명심하세요.

조건부 `when` 호출 시, 첫 번째 클로저에 기능의 풍부한 값이 전달됩니다:

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

유사하게, 조건부 `unless` 호출 시 두 번째 클로저에 기능 값이 전달됩니다:

```php
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>
## 여러 기능 조회하기

`values` 메서드를 사용해 특정 스코프에 대해 여러 기능 값을 한꺼번에 조회할 수 있습니다:

```php
Feature::values(['billing-v2', 'purchase-button']);

// 결과 예시:
// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

또한, `all` 메서드를 쓰면 스코프에 정의된 모든 기능 값을 가져올 수 있습니다:

```php
Feature::all();

// 결과 예시:
// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

단, 클래스 기반 기능은 동적으로 등록되고, 최초 체크 전까지 Pennant에 알려지지 않으므로 요청 내 한 번도 체크하지 않은 경우 `all` 결과에 포함되지 않을 수 있습니다.

항상 클래스 기반 기능을 `all` 결과에 포함하려면 Pennant의 기능 탐색(discovery) 기능을 사용할 수 있습니다. 애플리케이션 서비스 프로바이더에서 `discover` 메서드를 호출해 활성화하세요:

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

이제 `all` 메서드는 애플리케이션 `app/Features` 디렉터리에 있는 기능 클래스들도 항상 포함합니다:

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
## 지연 로딩

Pennant는 요청 동안 인메모리 캐시를 유지하지만, 여전히 성능 문제가 있을 수 있습니다. 이를 해결하기 위해 Pennant는 기능 값을 미리 로드하는 기능을 제공합니다.

예를 들어, 루프 안에서 기능 활성화를 확인할 때:

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

`database` 드라이버 사용 시, 사용자가 많으면 쿼리가 수백 번 실행되어 성능 문제가 생깁니다. 이때 `load` 메서드를 사용해 한꺼번에 기능 값을 미리 로드할 수 있습니다:

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

이미 로드된 기능 값만 불러오려면 `loadMissing`을 사용할 수 있습니다:

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

등록된 모든 기능을 로드하려면 `loadAll` 메서드를 사용하세요:

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
## 값 업데이트하기

기능 값이 처음 계산되면 저장소에 결과가 저장되어 사용자 경험 일관성을 보장합니다. 하지만 때로 기능의 저장 값을 수동으로 변경해야 할 수 있습니다.

기능을 켜거나 끄려면 `activate`와 `deactivate` 메서드를 사용하세요:

```php
use Laravel\Pennant\Feature;

// 기본 스코프 대상 기능 활성화...
Feature::activate('new-api');

// 특정 스코프 대상 기능 비활성화...
Feature::for($user->team)->deactivate('billing-v2');
```

`activate`에 두 번째 인자 전달 시 풍부한 값도 설정할 수 있습니다:

```php
Feature::activate('purchase-button', 'seafoam-green');
```

저장된 기능 값을 잊도록 하려면 `forget` 메서드를 사용하세요. 다시 체크 시 기능 정의에 따라 값을 새로 구합니다:

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### 일괄 업데이트

저장된 기능 값을 일괄 업데이트하려면 `activateForEveryone` 및 `deactivateForEveryone` 메서드를 사용하세요.

예를 들어, `new-api` 기능 안정성을 확신해 모든 사용자에게 활성화하고, `'purchase-button'` 색깔도 정했다면 다음과 같이 설정할 수 있습니다:

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

모든 사용자 기능을 비활성화하려면:

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> 이는 Pennant 저장소에 저장된 기존 기능 값에 대해서만 업데이트합니다. 기능 정의는 여전히 별도로 수정해야 합니다.

<a name="purging-features"></a>
### 기능 초기화

가끔 전체 기능 저장값을 초기화하는 것이 유용할 수 있습니다. 보통 애플리케이션에서 기능을 제거했거나, 기능 정의를 변경하고 변경 내용을 모든 사용자에게 즉시 반영하고 싶을 때 사용합니다.

특정 기능의 저장값을 모두 삭제하려면 `purge` 메서드를 사용하세요:

```php
// 단일 기능 초기화...
Feature::purge('new-api');

// 여러 기능 초기화...
Feature::purge(['new-api', 'purchase-button']);
```

모든 기능을 초기화하려면 인자 없이 호출하세요:

```php
Feature::purge();
```

배포 파이프라인에서 기능 초기화가 필요할 때는 Pennant의 `pennant:purge` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

초기화에서 특정 기능을 제외할 수도 있습니다. 예를 들어 `'new-api'`와 `'purchase-button'` 기능만 제외하고 모두 초기화하려면 다음과 같이 옵션을 지정하세요:

```shell
php artisan pennant:purge --except=new-api --except=purchase-button
```

더욱 편리하게, `--except-registered` 플래그를 사용하면 서비스 프로바이더에 명시적으로 등록된 기능을 제외하고 모두 초기화합니다:

```shell
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## 테스트

기능 플래그를 사용하는 코드를 테스트할 때 가장 쉬운 방법은 테스트 시작 시 기능을 다시 정의하는 것입니다.

예를 들어 애플리케이션 서비스 프로바이더에서 다음과 같은 기능을 정의했다면:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

테스트 내에서 이 값을 변경하려면 테스트 시작 부분에서 다시 정의하세요. 다음 테스트는 항상 통과합니다:

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

클래스 기반 기능도 같은 방식으로 제어할 수 있습니다:

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

`Lottery` 인스턴스를 반환하는 기능에 대해서는 [테스트용 헬퍼 함수](/docs/12.x/helpers#testing-lotteries)를 활용할 수 있습니다.

<a name="store-configuration"></a>
#### 저장소 설정

테스트 중 Pennant가 사용할 저장소는 `phpunit.xml`에 `PENNANT_STORE` 환경 변수로 지정할 수 있습니다:

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
#### 드라이버 구현하기

Pennant의 기본 드라이버가 맞지 않으면 직접 스토리지 드라이버를 구현할 수 있습니다. `Laravel\Pennant\Contracts\Driver` 인터페이스를 구현해야 합니다:

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

이후 Redis 연결을 이용해 메서드별 로직을 구현하면 됩니다. `Laravel\Pennant\Drivers\DatabaseDriver` 소스 코드를 참고할 수 있습니다:  
<https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php>

> [!NOTE]
> Laravel 기본 패키지에는 확장용 디렉터리가 없습니다. 원하는 위치에 구현하면 됩니다. 예제에서는 `Extensions` 디렉터리에 `RedisFeatureDriver`를 만들었습니다.

<a name="registering-the-driver"></a>
#### 드라이버 등록하기

드라이버 구현 후 Laravel에 등록합니다. `Feature` 퍼사드의 `extend` 메서드를 사용하며, 애플리케이션 서비스 프로바이더의 `boot` 메서드 내에서 호출하세요:

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
     * 서비스 등록.
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

이후 `config/pennant.php`에서 `redis` 드라이버를 설정 파일에 추가하면 됩니다:

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

서드파티 기능 플래그 플랫폼 래퍼인 드라이버라면 Pennant 내 `Feature::define` 대신 외부 플랫폼에서 기능을 정의할 가능성이 큽니다. 이때 드라이버는 `Laravel\Pennant\Contracts\DefinesFeaturesExternally` 인터페이스도 구현해야 합니다:

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;
use Laravel\Pennant\Contracts\DefinesFeaturesExternally;

class FeatureFlagServiceDriver implements Driver, DefinesFeaturesExternally
{
    /**
     * 주어진 스코프에 정의된 기능 목록을 반환.
     */
    public function definedFeaturesForScope(mixed $scope): array {}

    /* ... */
}
```

`definedFeaturesForScope` 메서드는 주어진 스코프에 대해 정의된 기능 이름 목록을 반환해야 합니다.

<a name="events"></a>
## 이벤트

Pennant는 애플리케이션 전반에서 기능 플래그 상태를 추적하는 데 유용한 다양한 이벤트를 발생시킵니다.

### `Laravel\Pennant\Events\FeatureRetrieved`

기능이 [체크될 때](#checking-features)마다 발생합니다. 기능 플래그 사용 통계 및 메트릭을 만드는 데 유용합니다.

### `Laravel\Pennant\Events\FeatureResolved`

특정 스코프에서 기능 값이 최초로 해석(결정)될 때 발생합니다.

### `Laravel\Pennant\Events\UnknownFeatureResolved`

알 수 없는 기능이 스코프에 대해 최초 해석될 때 발생합니다. 의도치 않게 기능 플래그를 삭제했는데도 참조가 남아 있을 때 이를 감지하는 데 사용하세요:

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
            Log::error("알 수 없는 기능 [{$event->feature}] 해석 중입니다.");
        });
    }
}
```

### `Laravel\Pennant\Events\DynamicallyRegisteringFeatureClass`

클래스 기반 기능이 요청 중 처음 동적으로 체크될 때 발생합니다.

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

`null` 스코프가 [널을 지원하지 않는 기능 정의에](#nullable-scope) 전달될 때 발생합니다.

이 상황은 정상적으로 처리되어 기능은 `false`를 반환하지만, 이 기본 동작을 무효화하려면 애플리케이션 `AppServiceProvider`의 `boot` 메서드에서 이벤트 리스너를 등록하세요:

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

기능이 특정 스코프에 대해 변경될 때 발생합니다. 보통 `activate` 또는 `deactivate` 호출 시입니다.

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

기능이 모든 스코프에 대해 변경될 때 발생합니다. 보통 `activateForEveryone` 또는 `deactivateForEveryone` 호출 시입니다.

### `Laravel\Pennant\Events\FeatureDeleted`

기능이 특정 스코프에서 삭제될 때 발생합니다. 보통 `forget` 호출 시입니다.

### `Laravel\Pennant\Events\FeaturesPurged`

특정 기능들을 저장소에서 초기화할 때 발생합니다.

### `Laravel\Pennant\Events\AllFeaturesPurged`

모든 기능을 저장소에서 초기화할 때 발생합니다.