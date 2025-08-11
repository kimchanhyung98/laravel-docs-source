# 미들웨어 (Middleware)

- [소개](#introduction)
- [미들웨어 정의](#defining-middleware)
- [미들웨어 등록](#registering-middleware)
    - [글로벌 미들웨어](#global-middleware)
    - [미들웨어를 라우트에 할당](#assigning-middleware-to-routes)
    - [미들웨어 그룹](#middleware-groups)
    - [미들웨어 별칭](#middleware-aliases)
    - [미들웨어 순서 지정](#sorting-middleware)
- [미들웨어 매개변수](#middleware-parameters)
- [종료형(Terminable) 미들웨어](#terminable-middleware)

<a name="introduction"></a>
## 소개 (Introduction)

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 검사하고 필터링할 수 있는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 사용자가 인증되었는지 확인하는 미들웨어가 포함되어 있습니다. 사용자가 인증되지 않은 경우, 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리다이렉트합니다. 반면, 사용자가 인증된 경우에는 요청이 애플리케이션 내부로 계속 진행됩니다.

인증 외에도 다양한 작업을 수행하는 추가 미들웨어를 작성할 수 있습니다. 예를 들어, 로깅 미들웨어는 애플리케이션으로 들어오는 모든 요청을 기록할 수 있습니다. Laravel에는 인증, CSRF 보호 등 여러 종류의 미들웨어가 기본적으로 포함되어 있으며, 사용자가 직접 정의한 미들웨어는 보통 애플리케이션의 `app/Http/Middleware` 디렉터리에 위치합니다.

<a name="defining-middleware"></a>
## 미들웨어 정의 (Defining Middleware)

새로운 미들웨어를 생성하려면 `make:middleware` Artisan 명령어를 사용합니다:

```shell
php artisan make:middleware EnsureTokenIsValid
```

이 명령어는 새로운 `EnsureTokenIsValid` 클래스를 `app/Http/Middleware` 디렉터리에 생성합니다. 이 예시 미들웨어에서는, 전달된 `token` 입력값이 지정된 값과 일치할 때만 해당 라우트에 접근을 허용합니다. 그렇지 않으면 사용자를 `/home` URI로 리다이렉트합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureTokenIsValid
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->input('token') !== 'my-secret-token') {
            return redirect('/home');
        }

        return $next($request);
    }
}
```

보시는 것처럼, 제공된 `token`이 비밀 토큰과 일치하지 않으면, 미들웨어는 클라이언트에 HTTP 리다이렉트를 반환합니다. 반대로 토큰이 일치하면 요청이 애플리케이션 내부로 더 전달됩니다. 요청을 애플리케이션의 더 깊은 곳으로 전달하려면(즉, 미들웨어가 "통과"하도록 하려면) `$next` 콜백에 `$request`를 전달해야 합니다.

미들웨어는 애플리케이션에 도달하기 전에 HTTP 요청이 반드시 통과해야 하는 일련의 "레이어"로 생각하는 것이 가장 이해하기 쉽습니다. 각 레이어는 요청을 검사해, 필요에 따라 해당 요청을 거부할 수도 있습니다.

> [!NOTE]
> 모든 미들웨어는 [서비스 컨테이너](/docs/12.x/container)를 통해 해석되므로, 미들웨어 생성자의 모든 의존성을 타입힌트로 지정할 수 있습니다.

<a name="middleware-and-responses"></a>
#### 미들웨어와 응답

당연히, 미들웨어는 요청을 애플리케이션 내부로 전달하기 **전**이나 **후**에 작업을 수행할 수 있습니다. 예를 들어, 아래의 미들웨어는 요청이 실제 애플리케이션에서 처리되기 **전**에 어떤 작업을 실행합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class BeforeMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        // Perform action

        return $next($request);
    }
}
```

반면, 아래의 미들웨어는 요청이 애플리케이션에서 처리된 **후**에 작업을 수행합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class AfterMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);

        // Perform action

        return $response;
    }
}
```

<a name="registering-middleware"></a>
## 미들웨어 등록 (Registering Middleware)

<a name="global-middleware"></a>
### 글로벌 미들웨어 (Global Middleware)

모든 HTTP 요청마다 미들웨어를 실행하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 글로벌 미들웨어 스택에 미들웨어를 추가할 수 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware) {
     $middleware->append(EnsureTokenIsValid::class);
})
```

`withMiddleware` 클로저로 전달되는 `$middleware` 객체는 `Illuminate\Foundation\Configuration\Middleware`의 인스턴스이며, 애플리케이션의 라우트에 할당된 미들웨어를 관리하는 역할을 합니다. `append` 메서드는 글로벌 미들웨어 목록의 마지막에 미들웨어를 추가합니다. 만약 목록의 맨 앞에 미들웨어를 추가하고 싶다면 `prepend` 메서드를 사용하면 됩니다.

<a name="manually-managing-laravels-default-global-middleware"></a>
#### Laravel 기본 글로벌 미들웨어 수동 관리

Laravel의 기본 글로벌 미들웨어 스택을 직접 관리하고 싶다면, `use` 메서드에 Laravel의 기본 글로벌 미들웨어 배열을 전달한 후 필요에 따라 목록을 수정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->use([
        \Illuminate\Foundation\Http\Middleware\InvokeDeferredCallbacks::class,
        // \Illuminate\Http\Middleware\TrustHosts::class,
        \Illuminate\Http\Middleware\TrustProxies::class,
        \Illuminate\Http\Middleware\HandleCors::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestsDuringMaintenance::class,
        \Illuminate\Http\Middleware\ValidatePostSize::class,
        \Illuminate\Foundation\Http\Middleware\TrimStrings::class,
        \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    ]);
})
```

<a name="assigning-middleware-to-routes"></a>
### 미들웨어를 라우트에 할당 (Assigning Middleware to Routes)

특정 라우트에 미들웨어를 할당하고 싶다면, 라우트를 정의할 때 `middleware` 메서드를 사용할 수 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

여러 미들웨어를 라우트에 한 번에 할당하고 싶다면, 미들웨어 클래스명을 배열로 전달할 수 있습니다:

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a name="excluding-middleware"></a>
#### 미들웨어 제외

라우트 그룹에 미들웨어를 할당할 때, 그룹 내 개별 라우트에만 해당 미들웨어를 적용하지 않으려는 경우가 있을 수 있습니다. 이럴 때는 `withoutMiddleware` 메서드를 사용할 수 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::middleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/', function () {
        // ...
    });

    Route::get('/profile', function () {
        // ...
    })->withoutMiddleware([EnsureTokenIsValid::class]);
});
```

특정 [라우트 그룹](/docs/12.x/routing#route-groups) 전체에서 미들웨어를 제외하고자 할 때도 사용할 수 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

단, `withoutMiddleware` 메서드는 라우트 미들웨어만 제거할 수 있으며, [글로벌 미들웨어](#global-middleware)에는 적용되지 않습니다.

<a name="middleware-groups"></a>
### 미들웨어 그룹 (Middleware Groups)

여러 미들웨어를 하나의 이름으로 묶어, 라우트에 쉽게 할당하고 싶을 때가 있습니다. 이럴 때는 애플리케이션의 `bootstrap/app.php` 파일에서 `appendToGroup` 메서드를 사용하면 됩니다:

```php
use App\Http\Middleware\First;
use App\Http\Middleware\Second;

->withMiddleware(function (Middleware $middleware) {
    $middleware->appendToGroup('group-name', [
        First::class,
        Second::class,
    ]);

    $middleware->prependToGroup('group-name', [
        First::class,
        Second::class,
    ]);
})
```

이렇게 그룹화한 미들웨어는 단일 미들웨어와 동일한 방식으로 라우트나 컨트롤러 액션에 할당할 수 있습니다:

```php
Route::get('/', function () {
    // ...
})->middleware('group-name');

Route::middleware(['group-name'])->group(function () {
    // ...
});
```

<a name="laravels-default-middleware-groups"></a>
#### Laravel의 기본 미들웨어 그룹

Laravel에는 웹 라우트에 공통적으로 적용되는 `web` 미들웨어 그룹과, API 라우트에 공통적으로 적용되는 `api` 미들웨어 그룹이 기본으로 정의되어 있습니다. 참고로, Laravel은 각 미들웨어 그룹을 자동으로 해당하는 `routes/web.php` 및 `routes/api.php` 파일에 적용합니다:

<div class="overflow-auto">

| `web` 미들웨어 그룹                                 |
| -------------------------------------------------- |
| `Illuminate\Cookie\Middleware\EncryptCookies`             |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession`              |
| `Illuminate\View\Middleware\ShareErrorsFromSession`       |
| `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` |
| `Illuminate\Routing\Middleware\SubstituteBindings`        |

</div>

<div class="overflow-auto">

| `api` 미들웨어 그룹                          |
| -------------------------------------------- |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

이 그룹에 미들웨어를 추가하거나 맨 앞에 삽입하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `web` 및 `api` 메서드를 사용할 수 있습니다. 이 메서드들은 `appendToGroup` 메서드에 대한 편리한 대안입니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        EnsureUserIsSubscribed::class,
    ]);

    $middleware->api(prepend: [
        EnsureTokenIsValid::class,
    ]);
})
```

Laravel의 기본 미들웨어 그룹 원소 중 하나를 사용자 지정 미들웨어로 대체할 수도 있습니다:

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

또는 해당 미들웨어를 완전히 제거할 수도 있습니다:

```php
$middleware->web(remove: [
    StartSession::class,
]);
```

<a name="manually-managing-laravels-default-middleware-groups"></a>
#### Laravel 기본 미들웨어 그룹 수동 관리

Laravel의 기본 `web`, `api` 미들웨어 그룹에 포함된 모든 미들웨어를 수동으로 관리하고 싶다면, 그룹 전체를 재정의할 수 있습니다. 아래 예시는 `web`과 `api` 미들웨어 그룹을 직접 지정하면서 원하는대로 커스터마이징 할 수 있게 해줍니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->group('web', [
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Foundation\Http\Middleware\ValidateCsrfToken::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        // \Illuminate\Session\Middleware\AuthenticateSession::class,
    ]);

    $middleware->group('api', [
        // \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        // 'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ]);
})
```

> [!NOTE]
> 기본적으로, `web` 및 `api` 미들웨어 그룹은 `bootstrap/app.php` 파일에 의해 각각 애플리케이션의 `routes/web.php` 및 `routes/api.php` 파일에 자동으로 적용됩니다.

<a name="middleware-aliases"></a>
### 미들웨어 별칭 (Middleware Aliases)

애플리케이션의 `bootstrap/app.php` 파일에서 미들웨어별 별칭(alias)을 지정할 수 있습니다. 미들웨어 별칭을 사용하면 클래스 이름이 긴 미들웨어를 짧게 정의하여 사용할 수 있어 편리합니다:

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

한 번 별칭을 정의하면, 라우트에 미들웨어를 할당할 때 해당 별칭을 사용할 수 있습니다:

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

편의를 위해, Laravel의 일부 기본 미들웨어는 이미 별칭이 미리 정의되어 있습니다. 예를 들어, `auth` 미들웨어는 `Illuminate\Auth\Middleware\Authenticate` 미들웨어의 별칭입니다. 기본 미들웨어 별칭 목록은 아래와 같습니다:

<div class="overflow-auto">

| 별칭 (Alias)         | 미들웨어 (Middleware)                                                                   |
| ------------------ | -------------------------------------------------------------------------------------- |
| `auth`             | `Illuminate\Auth\Middleware\Authenticate`                                               |
| `auth.basic`       | `Illuminate\Auth\Middleware\AuthenticateWithBasicAuth`                                  |
| `auth.session`     | `Illuminate\Session\Middleware\AuthenticateSession`                                     |
| `cache.headers`    | `Illuminate\Http\Middleware\SetCacheHeaders`                                            |
| `can`              | `Illuminate\Auth\Middleware\Authorize`                                                  |
| `guest`            | `Illuminate\Auth\Middleware\RedirectIfAuthenticated`                                    |
| `password.confirm` | `Illuminate\Auth\Middleware\RequirePassword`                                            |
| `precognitive`     | `Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests`                      |
| `signed`           | `Illuminate\Routing\Middleware\ValidateSignature`                                       |
| `subscribed`       | `\Spark\Http\Middleware\VerifyBillableIsSubscribed`                                     |
| `throttle`         | `Illuminate\Routing\Middleware\ThrottleRequests` 또는 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` |
| `verified`         | `Illuminate\Auth\Middleware\EnsureEmailIsVerified`                                      |

</div>

<a name="sorting-middleware"></a>
### 미들웨어 순서 지정 (Sorting Middleware)

드물게, 미들웨어가 특정 순서대로 실행되어야 하지만 라우트에 할당할 때 해당 순서를 직접 제어하지 못하는 경우가 있을 수 있습니다. 이럴 때는 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 메서드를 사용해 미들웨어의 우선순위를 지정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->priority([
        \Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests::class,
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Foundation\Http\Middleware\ValidateCsrfToken::class,
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        \Illuminate\Routing\Middleware\ThrottleRequests::class,
        \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        \Illuminate\Contracts\Auth\Middleware\AuthenticatesRequests::class,
        \Illuminate\Auth\Middleware\Authorize::class,
    ]);
})
```

<a name="middleware-parameters"></a>
## 미들웨어 매개변수 (Middleware Parameters)

미들웨어는 추가적인 매개변수를 받을 수 있습니다. 예를 들어, 인증된 사용자가 특정 "역할(role)"을 가지고 있는지 확인해야 할 때, 추가 인수로 역할 이름을 받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

추가 미들웨어 매개변수는 `$next` 인수 뒤에 전달됩니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserHasRole
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next, string $role): Response
    {
        if (! $request->user()->hasRole($role)) {
            // Redirect...
        }

        return $next($request);
    }
}
```

라우트 정의 시, 미들웨어 이름과 매개변수를 `:`로 구분하여 지정할 수 있습니다:

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

다수의 매개변수가 필요할 경우 쉼표로 구분합니다:

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```

<a name="terminable-middleware"></a>
## 종료형(Terminable) 미들웨어 (Terminable Middleware)

때로는 HTTP 응답이 브라우저로 전송된 후에도 추가 작업을 해야 할 때가 있습니다. 만약 미들웨어에 `terminate` 메서드를 정의하고, 웹 서버가 [FastCGI](https://www.php.net/manual/en/install.fpm.php)를 사용 중이라면, 응답 전송 후 자동으로 `terminate` 메서드가 실행됩니다:

```php
<?php

namespace Illuminate\Session\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class TerminatingMiddleware
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return $next($request);
    }

    /**
     * Handle tasks after the response has been sent to the browser.
     */
    public function terminate(Request $request, Response $response): void
    {
        // ...
    }
}
```

`terminate` 메서드는 요청과 응답을 모두 인자로 받아야 합니다. 종료형 미들웨어를 정의했다면, 이 미들웨어를 라우트 또는 글로벌 미들웨어 목록에 등록해야 합니다.

Laravel이 미들웨어의 `terminate` 메서드를 호출할 때는 [서비스 컨테이너](/docs/12.x/container)에서 새 인스턴스를 생성합니다. 만약 `handle`과 `terminate`가 동일한 인스턴스에서 호출되길 원한다면, 컨테이너의 `singleton` 메서드로 미들웨어를 등록해야 합니다. 일반적으로 이는 `AppServiceProvider`의 `register` 메서드에서 처리합니다:

```php
use App\Http\Middleware\TerminatingMiddleware;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(TerminatingMiddleware::class);
}
```