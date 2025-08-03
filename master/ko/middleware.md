# 미들웨어 (Middleware)

- [소개](#introduction)
- [미들웨어 정의하기](#defining-middleware)
- [미들웨어 등록하기](#registering-middleware)
    - [글로벌 미들웨어](#global-middleware)
    - [라우트에 미들웨어 할당하기](#assigning-middleware-to-routes)
    - [미들웨어 그룹](#middleware-groups)
    - [미들웨어 별칭](#middleware-aliases)
    - [미들웨어 순서 정하기](#sorting-middleware)
- [미들웨어 매개변수](#middleware-parameters)
- [종료 가능한 미들웨어](#terminable-middleware)

<a name="introduction"></a>
## 소개 (Introduction)

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 검사하고 필터링하는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel은 사용자가 인증되었는지 확인하는 미들웨어를 포함하고 있습니다. 사용자가 인증되지 않았다면 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리다이렉트합니다. 반면, 사용자가 인증되어 있다면 요청을 애플리케이션 내부로 계속 진행하도록 허용합니다.

인증 외에도 다양한 작업을 수행하는 추가 미들웨어를 작성할 수 있습니다. 예를 들어, 로깅 미들웨어는 애플리케이션으로 들어오는 모든 요청을 기록할 수 있습니다. Laravel에는 인증과 CSRF 보호를 위한 미들웨어 등 여러 미들웨어가 포함되어 있지만, 사용자 정의 미들웨어는 일반적으로 애플리케이션의 `app/Http/Middleware` 디렉토리에 위치합니다.

<a name="defining-middleware"></a>
## 미들웨어 정의하기 (Defining Middleware)

새로운 미들웨어를 생성하려면 `make:middleware` Artisan 명령어를 사용하세요:

```shell
php artisan make:middleware EnsureTokenIsValid
```

이 명령어는 `app/Http/Middleware` 디렉토리에 `EnsureTokenIsValid` 클래스를 생성합니다. 이 미들웨어에서는 전달된 `token` 입력 값이 지정된 값과 일치할 때만 라우트 접근을 허용하고, 그렇지 않으면 사용자를 `/home` URI로 리다이렉트합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureTokenIsValid
{
    /**
     * 들어오는 요청을 처리합니다.
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

보시다시피, 전달된 `token`이 비밀 토큰과 일치하지 않으면 미들웨어는 HTTP 리다이렉트를 클라이언트로 반환합니다. 그렇지 않으면 요청을 애플리케이션 내부로 전달합니다. 요청을 애플리케이션 내부로 전달(미들웨어를 "통과"시키려면) `$next` 콜백에 `$request`를 넘겨주면 됩니다.

미들웨어를 여러 겹의 "레이어"로 생각하는 것이 좋습니다. HTTP 요청은 애플리케이션에 도달하기 전에 이 레이어들을 차례대로 통과해야 하며, 각 레이어는 요청을 검사하고 완전히 거부할 수도 있습니다.

> [!NOTE]
> 모든 미들웨어는 [서비스 컨테이너](/docs/master/container)를 통해 해석되므로, 미들웨어의 생성자에서 필요한 의존성을 타입힌트할 수 있습니다.

<a name="middleware-and-responses"></a>
#### 미들웨어와 응답 처리

미들웨어는 요청을 애플리케이션 내부로 전달하기 전이나 후에 작업을 수행할 수 있습니다. 예를 들어, 다음 미들웨어는 요청이 애플리케이션에서 처리되기 **전에** 어떤 작업을 수행합니다:

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
        // 작업 수행

        return $next($request);
    }
}
```

반면, 이 미들웨어는 요청이 애플리케이션에서 처리된 **후에** 작업을 수행합니다:

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

        // 작업 수행

        return $response;
    }
}
```

<a name="registering-middleware"></a>
## 미들웨어 등록하기 (Registering Middleware)

<a name="global-middleware"></a>
### 글로벌 미들웨어 (Global Middleware)

애플리케이션의 모든 HTTP 요청에서 미들웨어를 실행하고 싶다면, `bootstrap/app.php` 파일에서 글로벌 미들웨어 스택에 추가할 수 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware) {
     $middleware->append(EnsureTokenIsValid::class);
})
```

`withMiddleware` 클로저에 전달되는 `$middleware` 객체는 `Illuminate\Foundation\Configuration\Middleware` 인스턴스이며, 애플리케이션 라우트에 할당된 미들웨어를 관리합니다. `append` 메서드는 미들웨어를 글로벌 미들웨어 목록의 끝에 추가합니다. 목록의 맨 앞에 추가하려면 `prepend` 메서드를 사용하세요.

<a name="manually-managing-laravels-default-global-middleware"></a>
#### Laravel 기본 글로벌 미들웨어 수동 관리

Laravel의 기본 글로벌 미들웨어 스택을 직접 관리하려면, 기본 글로벌 미들웨어 스택을 `use` 메서드에 넘기고, 필요에 따라 수정할 수 있습니다:

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
### 라우트에 미들웨어 할당하기 (Assigning Middleware to Routes)

특정 라우트에 미들웨어를 할당하려면, 라우트를 정의할 때 `middleware` 메서드를 호출하면 됩니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

여러 미들웨어를 할당하려면, 미들웨어 이름 배열을 `middleware` 메서드에 전달하세요:

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a name="excluding-middleware"></a>
#### 미들웨어 제외하기

미들웨어를 여러 라우트 그룹에 할당했는데, 특정 라우트에 미들웨어를 적용하지 않으려면 `withoutMiddleware` 메서드를 사용할 수 있습니다:

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

특정 미들웨어를 전체 라우트 그룹에서 제외할 수도 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

`withoutMiddleware` 메서드는 라우트 미들웨어만 제거할 수 있으며, [글로벌 미들웨어](#global-middleware)에는 적용되지 않습니다.

<a name="middleware-groups"></a>
### 미들웨어 그룹 (Middleware Groups)

여러 미들웨어를 하나의 키로 묶어 라우트에 할당을 쉽게 하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `appendToGroup` 메서드를 사용하세요:

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

미들웨어 그룹은 개별 미들웨어와 동일한 구문으로 라우트 및 컨트롤러 액션에 할당할 수 있습니다:

```php
Route::get('/', function () {
    // ...
})->middleware('group-name');

Route::middleware(['group-name'])->group(function () {
    // ...
});
```

<a name="laravels-default-middleware-groups"></a>
#### Laravel 기본 미들웨어 그룹

Laravel은 `web`과 `api`라는 미리 정의된 미들웨어 그룹을 포함하고 있으며, 각각 웹과 API 라우트에 적용할 공통 미들웨어를 담고 있습니다. Laravel은 `bootstrap/app.php` 파일에서 자동으로 이 미들웨어 그룹들을 `routes/web.php`와 `routes/api.php`에 적용합니다:

<div class="overflow-auto">

| `web` 미들웨어 그룹 |
| --- |
| `Illuminate\Cookie\Middleware\EncryptCookies` |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession` |
| `Illuminate\View\Middleware\ShareErrorsFromSession` |
| `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

<div class="overflow-auto">

| `api` 미들웨어 그룹 |
| --- |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

이 그룹에 미들웨어를 추가하거나 앞에 추가하려면 `bootstrap/app.php` 파일에서 `web` 및 `api` 메서드를 사용할 수 있습니다. 이는 `appendToGroup` 메서드의 간편한 대체 방법입니다:

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

기본 미들웨어 그룹 내의 항목을 사용자 정의 미들웨어로 교체할 수도 있습니다:

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

또는 미들웨어를 완전히 제거할 수도 있습니다:

```php
$middleware->web(remove: [
    StartSession::class,
]);
```

<a name="manually-managing-laravels-default-middleware-groups"></a>
#### Laravel 기본 미들웨어 그룹 수동 관리

Laravel의 기본 `web`과 `api` 미들웨어 그룹을 수동으로 관리하려면, 그룹을 완전히 다시 정의할 수 있습니다. 아래 예제는 기본 미들웨어로 `web`과 `api` 그룹을 정의하여 필요에 따라 사용자화할 수 있게 합니다:

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
> 기본적으로 `web`과 `api` 미들웨어 그룹은 `bootstrap/app.php` 파일에서 애플리케이션의 해당 `routes/web.php` 와 `routes/api.php` 파일에 자동으로 적용됩니다.

<a name="middleware-aliases"></a>
### 미들웨어 별칭 (Middleware Aliases)

애플리케이션의 `bootstrap/app.php` 파일에서 미들웨어에 별칭(alias)을 지정할 수 있습니다. 별칭은 미들웨어 클래스 이름이 길거나 복잡할 때 간단하고 짧은 이름을 사용할 수 있어 편리합니다:

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

`bootstrap/app.php` 파일에 별칭을 정의한 후, 라우트 할당 시 별칭을 사용할 수 있습니다:

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

참고로, Laravel의 내장 미들웨어는 기본으로 일부 별칭이 지정되어 있습니다. 예를 들어 `auth` 별칭은 `Illuminate\Auth\Middleware\Authenticate` 미들웨어에 할당됩니다. 기본 미들웨어 별칭 목록은 다음과 같습니다:

<div class="overflow-auto">

| 별칭 | 미들웨어 |
| --- | --- |
| `auth` | `Illuminate\Auth\Middleware\Authenticate` |
| `auth.basic` | `Illuminate\Auth\Middleware\AuthenticateWithBasicAuth` |
| `auth.session` | `Illuminate\Session\Middleware\AuthenticateSession` |
| `cache.headers` | `Illuminate\Http\Middleware\SetCacheHeaders` |
| `can` | `Illuminate\Auth\Middleware\Authorize` |
| `guest` | `Illuminate\Auth\Middleware\RedirectIfAuthenticated` |
| `password.confirm` | `Illuminate\Auth\Middleware\RequirePassword` |
| `precognitive` | `Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests` |
| `signed` | `Illuminate\Routing\Middleware\ValidateSignature` |
| `subscribed` | `\Spark\Http\Middleware\VerifyBillableIsSubscribed` |
| `throttle` | `Illuminate\Routing\Middleware\ThrottleRequests` 또는 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` |
| `verified` | `Illuminate\Auth\Middleware\EnsureEmailIsVerified` |

</div>

<a name="sorting-middleware"></a>
### 미들웨어 순서 정하기 (Sorting Middleware)

특정 미들웨어가 지정된 순서대로 실행되어야 하는데, 라우트에 할당할 때 그 순서를 제어할 수 없는 경우가 있습니다. 이럴 때는 `bootstrap/app.php` 파일에서 `priority` 메서드를 사용하여 미들웨어 우선순위를 지정할 수 있습니다:

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

미들웨어는 추가 매개변수를 받을 수도 있습니다. 예를 들어, 인증된 사용자가 특정 "역할(role)"을 가지고 있는지 확인해야 하는 경우, 역할 이름을 추가 인수로 받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

추가 미들웨어 매개변수는 `$next` 인수 다음에 전달됩니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserHasRole
{
    /**
     * 들어오는 요청을 처리합니다.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next, string $role): Response
    {
        if (! $request->user()->hasRole($role)) {
            // 리다이렉트 ...
        }

        return $next($request);
    }

}
```

미들웨어 매개변수는 라우트를 정의할 때, 미들웨어 이름과 매개변수를 `:`로 구분하여 지정할 수 있습니다:

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

여러 매개변수는 쉼표로 구분할 수 있습니다:

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```

<a name="terminable-middleware"></a>
## 종료 가능한 미들웨어 (Terminable Middleware)

어떤 경우에는 HTTP 응답이 브라우저에 전송된 후에도 미들웨어가 작업을 수행해야 할 수 있습니다. 미들웨어에 `terminate` 메서드를 정의하고 웹 서버가 FastCGI를 사용 중이라면, 응답이 전송된 후 자동으로 `terminate` 메서드가 호출됩니다:

```php
<?php

namespace Illuminate\Session\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class TerminatingMiddleware
{
    /**
     * 들어오는 요청을 처리합니다.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return $next($request);
    }

    /**
     * 응답이 브라우저에 전송된 후 작업을 처리합니다.
     */
    public function terminate(Request $request, Response $response): void
    {
        // ...
    }
}
```

`terminate` 메서드는 요청과 응답 모두를 인수로 받아야 합니다. 종료 가능한 미들웨어를 정의한 후에는, 애플리케이션의 `bootstrap/app.php` 파일에서 라우트 또는 글로벌 미들웨어 목록에 추가해야 합니다.

미들웨어의 `terminate` 메서드를 호출할 때 Laravel은 [서비스 컨테이너](/docs/master/container)에서 새로운 미들웨어 인스턴스를 해석합니다. 만약 `handle`과 `terminate` 메서드에서 동일한 미들웨어 인스턴스를 사용하려면, 컨테이너의 `singleton` 메서드를 사용하여 미들웨어를 등록하세요. 보통 이것은 `AppServiceProvider`의 `register` 메서드에서 수행합니다:

```php
use App\Http\Middleware\TerminatingMiddleware;

/**
 * 애플리케이션 서비스를 등록합니다.
 */
public function register(): void
{
    $this->app->singleton(TerminatingMiddleware::class);
}
```