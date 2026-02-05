# 미들웨어 (Middleware)

- [소개](#introduction)
- [미들웨어 정의하기](#defining-middleware)
- [미들웨어 등록하기](#registering-middleware)
    - [글로벌 미들웨어](#global-middleware)
    - [미들웨어를 라우트에 할당하기](#assigning-middleware-to-routes)
    - [미들웨어 그룹](#middleware-groups)
    - [미들웨어 별칭](#middleware-aliases)
    - [미들웨어 정렬하기](#sorting-middleware)
- [미들웨어 매개변수](#middleware-parameters)
- [종료 가능한 미들웨어](#terminable-middleware)

<a name="introduction"></a>
## 소개 (Introduction)

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 검사하고 필터링하기 위한 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 애플리케이션 사용자가 인증되었는지 확인하는 미들웨어가 포함되어 있습니다. 사용자가 인증되지 않은 경우, 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리디렉션합니다. 반대로, 사용자가 인증된 경우, 미들웨어는 요청을 애플리케이션의 다음 단계로 전달합니다.

인증 외에도 다양한 작업을 수행하는 추가 미들웨어를 작성할 수 있습니다. 예를 들어, 로깅 미들웨어는 애플리케이션에 들어오는 모든 요청을 기록할 수 있습니다. Laravel에는 인증 및 CSRF 보호 등 여러 미들웨어가 기본적으로 포함되어 있지만, 사용자가 직접 만든 모든 미들웨어는 일반적으로 애플리케이션의 `app/Http/Middleware` 디렉터리에 위치합니다.

<a name="defining-middleware"></a>
## 미들웨어 정의하기 (Defining Middleware)

새로운 미들웨어를 만들려면 `make:middleware` Artisan 명령어를 사용하세요:

```shell
php artisan make:middleware EnsureTokenIsValid
```

이 명령어는 새로운 `EnsureTokenIsValid` 클래스를 애플리케이션의 `app/Http/Middleware` 디렉터리에 생성합니다. 이 미들웨어에서는 전달된 `token` 입력값이 특정 값과 일치할 때만 라우트에 접근을 허용합니다. 그렇지 않으면 사용자를 `/home` URI로 리디렉션합니다:

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

위 코드에서처럼, 전달된 `token`이 비밀 토큰과 일치하지 않으면 미들웨어는 클라이언트에게 HTTP 리디렉션을 반환합니다. 반대로 일치한다면 요청은 애플리케이션의 더 깊은 곳으로 전달됩니다. 미들웨어가 요청을 더 깊이 전달(즉, "통과"시키기)하려면 `$next` 콜백에 `$request`를 인수로 전달하면 됩니다.

미들웨어는 HTTP 요청이 애플리케이션에 도달하기 전에 거쳐야 하는 "레이어"들의 집합으로 생각하면 이해가 쉽습니다. 각 레이어는 요청을 검사하고, 필요하다면 요청 자체를 거부할 수도 있습니다.

> [!NOTE]
> 모든 미들웨어는 [서비스 컨테이너](/docs/master/container)를 통해 해석되므로, 미들웨어의 생성자에서 필요한 의존성을 타입-힌트하여 주입받을 수 있습니다.

<a name="middleware-and-responses"></a>
#### 미들웨어와 응답

물론, 미들웨어는 요청이 애플리케이션으로 전달되기 **전**이나 **후**에 작업을 수행할 수도 있습니다. 예를 들어, 다음 미들웨어는 요청이 애플리케이션에서 처리되기 **전에** 어떤 작업을 수행합니다:

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

반면, 다음과 같은 미들웨어는 요청이 애플리케이션에서 처리된 **후에** 작업을 수행합니다:

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
## 미들웨어 등록하기 (Registering Middleware)

<a name="global-middleware"></a>
### 글로벌 미들웨어 (Global Middleware)

모든 HTTP 요청에 대해 미들웨어를 항상 실행하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 글로벌 미들웨어 스택에 추가하면 됩니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware): void {
     $middleware->append(EnsureTokenIsValid::class);
})
```

`withMiddleware` 클로저에 전달되는 `$middleware` 객체는 `Illuminate\Foundation\Configuration\Middleware`의 인스턴스로, 애플리케이션의 라우트에 할당된 미들웨어를 관리합니다. `append` 메서드는 전체 글로벌 미들웨어 목록의 마지막에 미들웨어를 추가합니다. 미들웨어를 목록의 맨 앞에 추가하려면 `prepend` 메서드를 사용하세요.

<a name="manually-managing-laravels-default-global-middleware"></a>
#### Laravel 기본 글로벌 미들웨어 수동 관리

Laravel의 글로벌 미들웨어 스택을 직접 관리하고 싶다면, Laravel이 제공하는 기본 글로벌 미들웨어 스택을 `use` 메서드에 전달한 후 필요에 따라 수정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
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
### 미들웨어를 라우트에 할당하기 (Assigning Middleware to Routes)

특정 라우트에만 미들웨어를 적용하고 싶다면, 라우트를 정의할 때 `middleware` 메서드를 호출하면 됩니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

여러 개의 미들웨어를 배열로 전달하여 한 번에 할당할 수도 있습니다:

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a name="excluding-middleware"></a>
#### 미들웨어 제외하기

라우트 그룹에 미들웨어를 할당했을 때, 그룹 내 특정 라우트에서는 미들웨어가 적용되지 않도록 할 때도 있습니다. 이럴 때는 `withoutMiddleware` 메서드를 사용하세요:

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

또는 전체 [그룹](/docs/master/routing#route-groups) 내의 모든 라우트에서 미들웨어를 제외할 수도 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

`withoutMiddleware` 메서드는 라우트 미들웨어만 제거할 수 있으며, [글로벌 미들웨어](#global-middleware)에 대해서는 적용되지 않습니다.

<a name="middleware-groups"></a>
### 미들웨어 그룹 (Middleware Groups)

여러 개의 미들웨어를 하나의 키로 묶어서 라우트에 쉽게 할당하고 싶을 때는, 애플리케이션의 `bootstrap/app.php` 파일 내에서 `appendToGroup` 메서드를 사용할 수 있습니다:

```php
use App\Http\Middleware\First;
use App\Http\Middleware\Second;

->withMiddleware(function (Middleware $middleware): void {
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

미들웨어 그룹 역시 개별 미들웨어처럼 라우트 및 컨트롤러 액션에 할당할 수 있습니다:

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

Laravel에는 웹 라우트와 API 라우트에 적용하기 좋은 기본 `web` 및 `api` 미들웨어 그룹이 사전 정의되어 있습니다. Laravel은 이 미들웨어 그룹을 자동으로 각 `routes/web.php`와 `routes/api.php` 파일에 적용합니다:

<div class="overflow-auto">

| `web` 미들웨어 그룹                                   |
| ---------------------------------------------------- |
| `Illuminate\Cookie\Middleware\EncryptCookies`             |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession`              |
| `Illuminate\View\Middleware\ShareErrorsFromSession`       |
| `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` |
| `Illuminate\Routing\Middleware\SubstituteBindings`        |

</div>

<div class="overflow-auto">

| `api` 미들웨어 그룹                            |
| ---------------------------------------------- |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

이 그룹에 미들웨어를 추가하거나 앞에 삽입하고 싶을 때는, `bootstrap/app.php` 파일에서 `web` 및 `api` 메서드를 사용할 수 있습니다. 이 메서드는 `appendToGroup` 메서드보다 더 간편하게 사용할 수 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        EnsureUserIsSubscribed::class,
    ]);

    $middleware->api(prepend: [
        EnsureTokenIsValid::class,
    ]);
})
```

또한, Laravel의 기본 미들웨어 그룹 항목 중 하나를 직접 만든 미들웨어로 교체할 수도 있습니다:

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

또는, 특정 미들웨어를 아예 제거할 수도 있습니다:

```php
$middleware->web(remove: [
    StartSession::class,
]);
```

<a name="manually-managing-laravels-default-middleware-groups"></a>
#### Laravel의 기본 미들웨어 그룹 직접 관리

Laravel의 기본 `web` 및 `api` 미들웨어 그룹의 모든 미들웨어를 직접 관리하고 싶다면, 그룹 전체를 새롭게 정의할 수 있습니다. 아래 예제는 `web` 및 `api` 미들웨어 그룹을 기본값으로 정의하며, 필요에 따라 자유롭게 커스터마이징할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
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
> 기본적으로, `web` 및 `api` 미들웨어 그룹은 `bootstrap/app.php` 파일에 의해 애플리케이션의 각 `routes/web.php` 및 `routes/api.php` 파일에 자동으로 적용됩니다.

<a name="middleware-aliases"></a>
### 미들웨어 별칭 (Middleware Aliases)

애플리케이션의 `bootstrap/app.php` 파일에서 미들웨어에 별칭을 지정할 수 있습니다. 미들웨어 별칭을 사용하면 긴 클래스명을 짧은 별칭으로 등록하여 라우트에 더욱 간단하게 할당할 수 있습니다:

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

한 번 별칭이 정의되면, 해당 별칭을 미들웨어 할당 시 사용할 수 있습니다:

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

편의를 위해, Laravel의 내장 미들웨어 중 일부는 기본적으로 별칭이 지정되어 있습니다. 예를 들어, `auth` 미들웨어는 `Illuminate\Auth\Middleware\Authenticate` 미들웨어에 대한 별칭입니다. 아래 표는 기본 미들웨어 별칭 목록입니다:

<div class="overflow-auto">

| 별칭                | 미들웨어                                                                                                        |
| ------------------- | --------------------------------------------------------------------------------------------------------------- |
| `auth`              | `Illuminate\Auth\Middleware\Authenticate`                                                                       |
| `auth.basic`        | `Illuminate\Auth\Middleware\AuthenticateWithBasicAuth`                                                          |
| `auth.session`      | `Illuminate\Session\Middleware\AuthenticateSession`                                                             |
| `cache.headers`     | `Illuminate\Http\Middleware\SetCacheHeaders`                                                                    |
| `can`               | `Illuminate\Auth\Middleware\Authorize`                                                                          |
| `guest`             | `Illuminate\Auth\Middleware\RedirectIfAuthenticated`                                                            |
| `password.confirm`  | `Illuminate\Auth\Middleware\RequirePassword`                                                                    |
| `precognitive`      | `Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests`                                              |
| `signed`            | `Illuminate\Routing\Middleware\ValidateSignature`                                                               |
| `subscribed`        | `\Spark\Http\Middleware\VerifyBillableIsSubscribed`                                                             |
| `throttle`          | `Illuminate\Routing\Middleware\ThrottleRequests` 또는 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` |
| `verified`          | `Illuminate\Auth\Middleware\EnsureEmailIsVerified`                                                              |

</div>

<a name="sorting-middleware"></a>
### 미들웨어 정렬하기 (Sorting Middleware)

매우 드물지만, 미들웨어를 어떤 순서대로 실행해야 하지만 라우트에 할당할 때 그 순서를 제어할 수 없는 경우가 있습니다. 이런 상황에서는 애플리케이션의 `bootstrap/app.php` 파일에 있는 `priority` 메서드를 사용해 미들웨어 우선순위를 지정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
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

미들웨어는 추가 매개변수도 받을 수 있습니다. 예를 들어, 인증된 사용자가 특정 "역할"을 가지고 있는지 확인해야 한다면, 역할 이름을 추가 인수로 받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

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

미들웨어 매개변수는 라우트 정의 시, 미들웨어 이름과 매개변수 사이에 `:`를 사용하여 전달할 수 있습니다:

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

여러 개의 매개변수는 쉼표로 구분할 수 있습니다:

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```

<a name="terminable-middleware"></a>
## 종료 가능한 미들웨어 (Terminable Middleware)

때로는 미들웨어에서 HTTP 응답이 브라우저에 전송된 후에도 추가 작업이 필요할 수 있습니다. 미들웨어에 `terminate` 메서드를 정의하고 웹 서버가 [FastCGI](https://www.php.net/manual/en/install.fpm.php)를 사용 중이라면, 응답이 브라우저로 전송된 뒤 자동으로 `terminate` 메서드가 호출됩니다:

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

`terminate` 메서드는 요청 객체와 응답 객체를 모두 인수로 받아야 합니다. 종료 가능한 미들웨어를 정의했다면, 해당 미들웨어를 라우트 또는 글로벌 미들웨어 목록에 `bootstrap/app.php` 파일을 통해 추가해야 합니다.

Laravel이 미들웨어의 `terminate` 메서드를 호출할 때는 [서비스 컨테이너](/docs/master/container)를 통해 새로운 미들웨어 인스턴스를 해석합니다. 만약 `handle`과 `terminate` 메서드가 호출될 때 동일한 미들웨어 인스턴스를 사용하고 싶다면, 컨테이너의 `singleton` 메서드로 미들웨어를 등록하세요. 보통은 `AppServiceProvider`의 `register` 메서드에서 등록합니다:

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