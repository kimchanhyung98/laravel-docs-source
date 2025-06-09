# 미들웨어 (Middleware)

- [소개](#introduction)
- [미들웨어 정의하기](#defining-middleware)
- [미들웨어 등록하기](#registering-middleware)
    - [글로벌 미들웨어](#global-middleware)
    - [미들웨어를 라우트에 지정하기](#assigning-middleware-to-routes)
    - [미들웨어 그룹](#middleware-groups)
    - [미들웨어 별칭](#middleware-aliases)
    - [미들웨어 정렬하기](#sorting-middleware)
- [미들웨어 파라미터](#middleware-parameters)
- [종료 가능한 미들웨어](#terminable-middleware)

<a name="introduction"></a>
## 소개

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 검사하고 필터링할 수 있는 편리한 메커니즘을 제공합니다. 예를 들어 라라벨에는 사용자가 인증되었는지 확인하는 미들웨어가 기본 포함되어 있습니다. 사용자가 인증되지 않은 경우, 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리디렉션합니다. 반면, 사용자가 인증된 경우에는 요청을 애플리케이션의 다음 단계로 계속 진행시킵니다.

인증 외에도 다양한 작업을 수행하는 미들웨어를 추가로 작성할 수 있습니다. 예를 들어 모든 요청을 로그로 남기는 로깅 미들웨어를 만들 수도 있습니다. 라라벨에는 인증, CSRF 보호 등 여러 기본 제공 미들웨어가 있으며, 사용자가 직접 작성한 미들웨어는 보통 애플리케이션의 `app/Http/Middleware` 디렉터리에 위치합니다.

<a name="defining-middleware"></a>
## 미들웨어 정의하기

새로운 미들웨어를 생성하려면 `make:middleware` 아티즌 명령어를 사용합니다.

```shell
php artisan make:middleware EnsureTokenIsValid
```

이 명령어를 실행하면 `app/Http/Middleware` 디렉터리에 새로운 `EnsureTokenIsValid` 클래스가 생성됩니다. 이 예제 미들웨어는 전달받은 `token` 입력값이 지정된 값과 일치할 때만 라우트 접근을 허용합니다. 그렇지 않으면 사용자를 `/home` URI로 리디렉션합니다.

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

위 코드에서 알 수 있듯이, `token` 값이 비밀 토큰과 일치하지 않을 경우 미들웨어는 클라이언트에게 HTTP 리디렉트 응답을 반환합니다. 일치할 경우에는 요청이 애플리케이션의 다음 단계로 전달됩니다. 미들웨어를 "통과(pass)"시키려면 `$next` 콜백에 `$request`를 전달해서 요청 흐름이 더 깊이 진행되도록 해야 합니다.

미들웨어는 HTTP 요청이 애플리케이션에 도달하기 전에 여러 개의 "레이어"를 순차적으로 통과한다고 생각하면 이해하기 쉽습니다. 각 레이어에서는 요청을 검사하거나 아예 거부할 수도 있습니다.

> [!NOTE]
> 모든 미들웨어는 [서비스 컨테이너](/docs/12.x/container)를 통해 resolve되므로, 미들웨어의 생성자에서 필요한 의존성을 타입힌트로 지정할 수 있습니다.

<a name="middleware-and-responses"></a>
#### 미들웨어와 응답

미들웨어는 요청을 애플리케이션에 통과시키기 전이나 후에 작업을 수행할 수 있습니다. 예를 들어 아래 미들웨어는 요청이 애플리케이션에 의해 처리되기 **전**에 특정 작업을 수행합니다.

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

반면, 아래 미들웨어는 요청이 애플리케이션에 의해 처리된 **후**에 작업을 수행합니다.

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
## 미들웨어 등록하기

<a name="global-middleware"></a>
### 글로벌 미들웨어

애플리케이션 내의 모든 HTTP 요청에 대해 특정 미들웨어를 매번 실행하고 싶다면, `bootstrap/app.php` 파일의 글로벌 미들웨어 스택에 추가할 수 있습니다.

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware) {
     $middleware->append(EnsureTokenIsValid::class);
})
```

`withMiddleware` 클로저에 전달되는 `$middleware` 객체는 `Illuminate\Foundation\Configuration\Middleware`의 인스턴스이며, 애플리케이션 라우트에 지정된 미들웨어를 관리합니다. `append` 메서드는 미들웨어를 글로벌 미들웨어 목록의 마지막에 추가합니다. 만약 맨 앞에 추가하고 싶다면 `prepend` 메서드를 사용하세요.

<a name="manually-managing-laravels-default-global-middleware"></a>
#### 라라벨의 기본 글로벌 미들웨어 수동 관리

기본 글로벌 미들웨어 스택을 직접 관리하려면, `use` 메서드에 라라벨의 기본 글로벌 미들웨어 배열을 넘겨준 뒤 필요에 따라 수정할 수 있습니다.

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
### 미들웨어를 라우트에 지정하기

특정 라우트에만 미들웨어를 적용하고 싶을 경우, 라우트를 정의할 때 `middleware` 메서드를 사용하면 됩니다.

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

여러 미들웨어를 배열로 전달하여 동시에 지정할 수도 있습니다.

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a name="excluding-middleware"></a>
#### 미들웨어 제외하기

라우트 그룹에 미들웨어를 지정할 때, 그룹 안의 특정 라우트에서만 해당 미들웨어가 적용되지 않도록 하고 싶을 수 있습니다. 이럴 때는 `withoutMiddleware` 메서드를 사용할 수 있습니다.

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

특정 미들웨어를 아예 한 [라우트 그룹](/docs/12.x/routing#route-groups) 전체에서 제외할 수도 있습니다.

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

`withoutMiddleware` 메서드는 라우트에 지정한 미들웨어만 제거할 수 있으며, [글로벌 미들웨어](#global-middleware)에는 적용되지 않습니다.

<a name="middleware-groups"></a>
### 미들웨어 그룹

여러 미들웨어를 하나의 키 아래 묶어서 라우트에 손쉽게 지정하고 싶을 때는, `bootstrap/app.php` 파일에서 `appendToGroup` 메서드를 사용할 수 있습니다.

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

미들웨어 그룹도 개별 미들웨어와 동일한 방식으로 라우트나 컨트롤러에 지정할 수 있습니다.

```php
Route::get('/', function () {
    // ...
})->middleware('group-name');

Route::middleware(['group-name'])->group(function () {
    // ...
});
```

<a name="laravels-default-middleware-groups"></a>
#### 라라벨의 기본 미들웨어 그룹

라라벨은 `web`과 `api`라는 두 가지 미들웨어 그룹을 미리 정의해 둡니다. 이 그룹에는 웹 및 API 라우트에 일반적으로 적용하는 미들웨어가 포함되어 있습니다. 참고로 라라벨은 각각의 `routes/web.php`, `routes/api.php` 파일에 이 미들웨어 그룹을 자동으로 적용합니다.

<div class="overflow-auto">

| `web` 미들웨어 그룹                                        |
| --------------------------------------------------------- |
| `Illuminate\Cookie\Middleware\EncryptCookies`             |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession`              |
| `Illuminate\View\Middleware\ShareErrorsFromSession`       |
| `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` |
| `Illuminate\Routing\Middleware\SubstituteBindings`        |

</div>

<div class="overflow-auto">

| `api` 미들웨어 그룹                               |
| -------------------------------------------------- |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

이 그룹에 미들웨어를 추가하거나 앞쪽에 붙이고 싶으면, `bootstrap/app.php` 파일의 `web`, `api` 메서드를 사용할 수 있습니다. 이 메서드는 `appendToGroup` 메서드보다 한 단계 더 편리한 옵션입니다.

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

심지어 라라벨의 기본 미들웨어 그룹 항목 중 일부를 사용자 지정 미들웨어로 교체할 수도 있습니다.

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

또는 미들웨어를 목록에서 완전히 제거할 수도 있습니다.

```php
$middleware->web(remove: [
    StartSession::class,
]);
```

<a name="manually-managing-laravels-default-middleware-groups"></a>
#### 라라벨의 기본 미들웨어 그룹 직접 관리

라라벨의 기본 `web` 및 `api` 미들웨어 그룹 전체를 직접 정의해서 완전히 제어할 수도 있습니다. 아래는 기본 미들웨어 항목과 함께 직접 그룹을 정의하고 필요에 따라 수정하는 예제입니다.

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
> 기본적으로 `web`과 `api` 미들웨어 그룹은 `bootstrap/app.php` 파일에 의해 각각의 `routes/web.php`, `routes/api.php` 파일에 자동으로 적용됩니다.

<a name="middleware-aliases"></a>
### 미들웨어 별칭

`bootstrap/app.php` 파일에서 미들웨어에 별칭(알리아스)을 지정할 수 있습니다. 별칭을 사용하면 긴 클래스명을 짧은 이름으로 대체해서 라우트에 할당할 수 있어 편리합니다.

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

별칭이 지정되면 라우트에 미들웨어를 적용할 때 해당 별칭을 사용할 수 있습니다.

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

일부 라라벨 내장 미들웨어에는 기본적으로 별칭이 지정되어 있습니다. 예를 들어 `auth` 별칭은 `Illuminate\Auth\Middleware\Authenticate` 미들웨어를 의미합니다. 아래는 기본 미들웨어 별칭 목록입니다.

<div class="overflow-auto">

| 별칭               | 미들웨어                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------- |
| `auth`             | `Illuminate\Auth\Middleware\Authenticate`                                                                     |
| `auth.basic`       | `Illuminate\Auth\Middleware\AuthenticateWithBasicAuth`                                                        |
| `auth.session`     | `Illuminate\Session\Middleware\AuthenticateSession`                                                           |
| `cache.headers`    | `Illuminate\Http\Middleware\SetCacheHeaders`                                                                  |
| `can`              | `Illuminate\Auth\Middleware\Authorize`                                                                        |
| `guest`            | `Illuminate\Auth\Middleware\RedirectIfAuthenticated`                                                          |
| `password.confirm` | `Illuminate\Auth\Middleware\RequirePassword`                                                                  |
| `precognitive`     | `Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests`                                            |
| `signed`           | `Illuminate\Routing\Middleware\ValidateSignature`                                                             |
| `subscribed`       | `\Spark\Http\Middleware\VerifyBillableIsSubscribed`                                                           |
| `throttle`         | `Illuminate\Routing\Middleware\ThrottleRequests` 또는 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` |
| `verified`         | `Illuminate\Auth\Middleware\EnsureEmailIsVerified`                                                            |

</div>

<a name="sorting-middleware"></a>
### 미들웨어 정렬하기

드물게, 미들웨어를 특정 순서로 실행해야 하지만 라우트에서 그 순서를 조정할 수 없는 경우가 있습니다. 이럴 때는 `bootstrap/app.php` 파일에서 `priority` 메서드를 사용하여 미들웨어 우선순위를 지정할 수 있습니다.

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

미들웨어는 추가 파라미터를 받을 수도 있습니다. 예를 들어 사용자가 특정 "역할(role)"을 가지고 있어야만 어떤 작업을 허용하고 싶을 때, 추가 인수로 역할명을 받을 수 있는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

추가 미들웨어 파라미터는 `$next` 인수 다음에 전달됩니다.

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

미들웨어에 파라미터를 전달하려면, 라우트 정의 시 미들웨어 이름과 파라미터를 `:`로 구분해서 지정하면 됩니다.

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

여러 개의 파라미터는 쉼표로 구분합니다.

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class:‘editor,publisher’);
```

<a name="terminable-middleware"></a>
## 종료 가능한 미들웨어

때때로, 응답이 브라우저로 전송된 후에 추가 작업을 해야 하는 미들웨어가 필요할 수 있습니다. 미들웨어 클래스에 `terminate` 메서드를 정의하고, 웹 서버가 FastCGI를 사용 중이라면 응답이 브라우저에 전송된 후 자동으로 `terminate` 메서드가 호출됩니다.

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

`terminate` 메서드는 반드시 요청과 응답을 인자로 받아야 합니다. 종료 가능한 미들웨어를 만들었다면, 앱의 `bootstrap/app.php` 파일 내 라우트나 글로벌 미들웨어 목록에 추가해야 합니다.

라라벨에서 미들웨어의 `terminate` 메서드를 호출할 때는 [서비스 컨테이너](/docs/12.x/container)로부터 미들웨어 인스턴스를 새로 resolve합니다. 만약 `handle`과 `terminate` 두 메서드 모두에서 동일한 미들웨어 인스턴스를 사용하고 싶다면, 컨테이너의 `singleton` 메서드를 통해 미들웨어를 싱글톤으로 등록해야 합니다. 일반적으로 이는 `AppServiceProvider`의 `register` 메서드에서 처리합니다.

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
