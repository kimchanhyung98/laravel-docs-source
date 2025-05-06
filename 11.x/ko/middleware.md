# 미들웨어

- [소개](#introduction)
- [미들웨어 정의하기](#defining-middleware)
- [미들웨어 등록하기](#registering-middleware)
    - [글로벌 미들웨어](#global-middleware)
    - [미들웨어를 라우트에 할당하기](#assigning-middleware-to-routes)
    - [미들웨어 그룹](#middleware-groups)
    - [미들웨어 별칭](#middleware-aliases)
    - [미들웨어 정렬](#sorting-middleware)
- [미들웨어 파라미터](#middleware-parameters)
- [종료 가능한 미들웨어](#terminable-middleware)

<a name="introduction"></a>
## 소개

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 점검하고 필터링할 수 있는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel은 사용자가 인증되었는지 확인하는 미들웨어를 포함하고 있습니다. 사용자가 인증되지 않은 경우, 미들웨어는 사용자를 로그인 화면으로 리디렉션합니다. 하지만 사용자가 인증됐다면, 미들웨어는 요청이 애플리케이션의 더 깊은 곳까지 진행되도록 허용합니다.

추가 미들웨어를 작성하여 인증 이외의 다양한 작업도 수행할 수 있습니다. 예를 들어, 로깅 미들웨어는 애플리케이션으로 들어오는 모든 요청을 기록할 수 있습니다. Laravel에는 인증, CSRF 보호와 같은 다양한 미들웨어가 포함되어 있지만, 사용자가 정의한 미들웨어는 보통 애플리케이션의 `app/Http/Middleware` 디렉토리에 위치합니다.

<a name="defining-middleware"></a>
## 미들웨어 정의하기

새로운 미들웨어를 생성하려면 `make:middleware` Artisan 명령어를 사용하세요:

```shell
php artisan make:middleware EnsureTokenIsValid
```

이 명령어는 `app/Http/Middleware` 디렉토리에 새로운 `EnsureTokenIsValid` 클래스를 생성합니다. 이 미들웨어에서는 제공된 `token` 입력값이 지정한 값과 일치할 때만 해당 라우트 접근을 허용합니다. 그렇지 않은 경우, 사용자는 `/home` URI로 리디렉션됩니다.

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

보시다시피, 제공된 `token`이 비밀 토큰과 일치하지 않으면 미들웨어는 HTTP 리디렉션을 반환하고, 일치하면 요청이 애플리케이션에 더 깊이 전달됩니다. 요청을 애플리케이션 내부로 더 깊이 전달하려면(즉, 미들웨어를 "통과"시키려면) `$next` 콜백에 `$request`를 전달해야 합니다.

미들웨어는 애플리케이션에 도달하기 전에 HTTP 요청이 거쳐야 하는 "레이어"의 연속으로 상상하는 것이 가장 좋습니다. 각 레이어는 요청을 검사하고, 필요하다면 전체적으로 거부할 수도 있습니다.

> [!NOTE]  
> 모든 미들웨어는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 미들웨어의 생성자에 필요한 의존성을 타입힌트로 지정할 수 있습니다.

<a name="middleware-and-responses"></a>
#### 미들웨어와 응답

물론, 미들웨어는 요청이 애플리케이션에 더 깊이 전달되기 **전**이나 **후**에 작업을 수행할 수 있습니다. 예를 들어, 아래 미들웨어는 요청이 애플리케이션에 의해 처리되기 **전**에 작업을 수행합니다:

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
        // 여기서 작업 수행

        return $next($request);
    }
}
```

반면에, 다음 미들웨어는 요청이 애플리케이션에 의해 처리된 **후**에 작업을 수행합니다:

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

        // 여기서 작업 수행

        return $response;
    }
}
```

<a name="registering-middleware"></a>
## 미들웨어 등록하기

<a name="global-middleware"></a>
### 글로벌 미들웨어

모든 HTTP 요청마다 미들웨어를 실행하려면, 애플리케이션의 `bootstrap/app.php` 파일 내 글로벌 미들웨어 스택에 추가할 수 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware) {
     $middleware->append(EnsureTokenIsValid::class);
})
```

`withMiddleware` 클로저에 제공되는 `$middleware` 객체는 `Illuminate\Foundation\Configuration\Middleware`의 인스턴스이며, 라우트에 할당된 미들웨어를 관리합니다. `append` 메서드는 미들웨어를 글로벌 미들웨어 목록의 마지막에 추가합니다. 만약 목록의 앞에 추가하고 싶다면 `prepend` 메서드를 사용하세요.

<a name="manually-managing-laravels-default-global-middleware"></a>
#### Laravel 기본 글로벌 미들웨어 직접 관리하기

Laravel의 글로벌 미들웨어 스택을 직접 관리하려면, `use` 메서드에 Laravel의 기본 글로벌 미들웨어 스택을 제공한 후 필요에 따라 조정할 수 있습니다:

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
### 미들웨어를 라우트에 할당하기

특정 라우트에 미들웨어를 할당하려면 라우트를 정의할 때 `middleware` 메서드를 호출하세요:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

`middleware` 메서드에 미들웨어 이름 배열을 전달하여 여러 미들웨어를 한 라우트에 할당할 수 있습니다:

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a name="excluding-middleware"></a>
#### 미들웨어 제외하기

라우트 그룹에 미들웨어를 할당할 때, 가끔 특정 라우트에서 미들웨어를 제외해야 할 수도 있습니다. 이때는 `withoutMiddleware` 메서드를 사용할 수 있습니다:

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

또한, 전체 [라우트 그룹](/docs/{{version}}/routing#route-groups)에서도 미들웨어를 제외할 수 있습니다:

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
### 미들웨어 그룹

여러 미들웨어를 하나의 키로 그룹화하여 라우트에 더 쉽게 할당하고 싶을 때가 있습니다. 이를 위해서는 `bootstrap/app.php` 파일 내에서 `appendToGroup` 메서드를 사용할 수 있습니다:

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

미들웨어 그룹은 개별 미들웨어와 동일한 문법으로 라우트와 컨트롤러 액션에 할당할 수 있습니다:

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

Laravel에는 웹 및 API 라우트에 적용할 수 있는 기본 `web` 및 `api` 미들웨어 그룹이 포함되어 있습니다. Laravel은 이 미들웨어 그룹들을 자동으로 `routes/web.php` 및 `routes/api.php`에 적용합니다:

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

이 그룹에 미들웨어를 추가하거나 앞에 삽입하려면, `bootstrap/app.php` 파일에서 `web` 및 `api` 메서드를 사용할 수 있습니다. `web` 및 `api` 메서드는 `appendToGroup` 메서드의 편리한 대안입니다:

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

기본 미들웨어 그룹의 엔트리를 직접 커스텀 미들웨어로 대체할 수도 있습니다:

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

또한, 미들웨어를 아예 제거할 수도 있습니다:

```php
$middleware->web(remove: [
    StartSession::class,
]);
```

<a name="manually-managing-laravels-default-middleware-groups"></a>
#### Laravel 기본 미들웨어 그룹 직접 관리하기

Laravel의 기본 `web` 및 `api` 미들웨어 그룹을 수동으로 모두 관리하고 싶다면, 그룹을 완전히 재정의할 수 있습니다. 아래 예제는 기본 미들웨어로 두 그룹을 정의한 후 필요에 따라 커스터마이징할 수 있도록 합니다:

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
> 기본적으로, `web` 및 `api` 미들웨어 그룹은 `bootstrap/app.php` 파일에 의해 해당하는 `routes/web.php`와 `routes/api.php` 파일에 자동으로 적용됩니다.

<a name="middleware-aliases"></a>
### 미들웨어 별칭

애플리케이션의 `bootstrap/app.php` 파일에서 미들웨어에 별칭(에일리어스)을 지정할 수 있습니다. 별칭을 이용하면 긴 클래스 이름 대신 짧은 이름으로 미들웨어를 정의할 수 있어 편리합니다:

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

별칭이 정의된 후에는 라우트에 미들웨어를 할당할 때 별칭을 사용할 수 있습니다:

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

Laravel 내장 미들웨어 중 일부는 기본적으로 별칭이 지정되어 있습니다. 예를 들어, `auth` 미들웨어는 `Illuminate\Auth\Middleware\Authenticate`의 별칭입니다. 기본 미들웨어 별칭 목록은 다음과 같습니다:

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
### 미들웨어 정렬

드물지만, 미들웨어를 특정 순서대로 실행해야 하고 라우트에 할당할 때 그 순서를 제어할 수 없는 경우가 있습니다. 이럴 때는 `bootstrap/app.php` 파일의 `priority` 메서드를 이용해 미들웨어 우선순위를 지정할 수 있습니다:

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
## 미들웨어 파라미터

미들웨어는 추가 파라미터를 받을 수도 있습니다. 예를 들어, 인증된 사용자가 "역할"을 가지고 있는지 확인해야 할 경우, 추가 인자를 받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

추가 미들웨어 파라미터는 `$next` 인자 뒤에 전달됩니다:

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
            // 리디렉션 등의 동작...
        }

        return $next($request);
    }
}
```

라우트 정의 시 미들웨어 이름과 파라미터를 `:`로 구분하여 지정할 수 있습니다:

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

여러 개의 파라미터는 쉼표로 구분해 전달할 수 있습니다:

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```

<a name="terminable-middleware"></a>
## 종료 가능한 미들웨어

때로는 HTTP 응답이 브라우저로 전송된 이후에도 미들웨어가 작업을 수행해야 할 수 있습니다. 미들웨어에 `terminate` 메서드를 정의하고 웹서버가 FastCGI를 사용할 경우, 응답 전송 후 `terminate` 메서드가 자동으로 호출됩니다:

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
        // 추가 작업 수행...
    }
}
```

`terminate` 메서드는 요청과 응답을 모두 받아야 합니다. 종료 가능한 미들웨어를 정의했다면, 애플리케이션의 `bootstrap/app.php` 파일에서 라우트 또는 글로벌 미들웨어 목록에 추가해야 합니다.

Laravel이 미들웨어의 `terminate` 메서드를 호출할 때는 [서비스 컨테이너](/docs/{{version}}/container)에서 새로운 미들웨어 인스턴스를 해석합니다. `handle`과 `terminate` 메서드 모두 같은 인스턴스를 사용하려면, 컨테이너의 `singleton` 메서드를 사용하여 미들웨어를 등록해야 합니다. 일반적으로 이는 `AppServiceProvider`의 `register` 메서드에서 수행합니다:

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