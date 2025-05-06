# 미들웨어

- [소개](#introduction)
- [미들웨어 정의하기](#defining-middleware)
- [미들웨어 등록하기](#registering-middleware)
    - [글로벌 미들웨어](#global-middleware)
    - [미들웨어를 라우트에 할당하기](#assigning-middleware-to-routes)
    - [미들웨어 그룹](#middleware-groups)
    - [미들웨어 정렬](#sorting-middleware)
- [미들웨어 파라미터](#middleware-parameters)
- [종료 가능한 미들웨어](#terminable-middleware)

<a name="introduction"></a>
## 소개

미들웨어는 애플리케이션으로 들어오는 HTTP 요청을 검사하고 필터링할 수 있는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 사용자가 인증되었는지 확인하는 미들웨어가 포함되어 있습니다. 사용자가 인증되지 않은 경우, 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리다이렉션합니다. 하지만 사용자가 인증되어 있다면 요청이 애플리케이션 내부로 더 진행될 수 있도록 허용합니다.

추가로, 인증 이외의 다양한 작업을 수행할 수 있도록 미들웨어를 직접 작성할 수 있습니다. 예를 들어, 로깅 미들웨어를 만들어 모든 들어오는 요청을 기록할 수 있습니다. Laravel 프레임워크에는 인증, CSRF 보호 등을 위한 여러 기본 미들웨어가 포함되어 있으며, 이 모든 미들웨어는 `app/Http/Middleware` 디렉터리에 위치합니다.

<a name="defining-middleware"></a>
## 미들웨어 정의하기

새로운 미들웨어를 생성하려면 `make:middleware` Artisan 명령어를 사용하세요:

    php artisan make:middleware EnsureTokenIsValid

이 명령어는 `app/Http/Middleware` 디렉터리 내에 새로운 `EnsureTokenIsValid` 클래스를 생성합니다. 이 미들웨어에서는 전달된 `token` 입력값이 지정된 값과 일치할 때만 라우트에 접근을 허용합니다. 그렇지 않으면 사용자를 `home` URI로 리다이렉션합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;

class EnsureTokenIsValid
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        if ($request->input('token') !== 'my-secret-token') {
            return redirect('home');
        }

        return $next($request);
    }
}
```

위 코드에서 볼 수 있듯이, 제공된 `token`이 우리의 시크릿 토큰과 일치하지 않으면 미들웨어는 클라이언트에게 HTTP 리다이렉트를 반환하고, 그렇지 않으면 요청이 애플리케이션 내로 더 전달됩니다. 요청을 더 깊게 전달(즉, 미들웨어가 "통과")하려면 `$next` 콜백을 `$request`와 함께 호출해야 합니다.

미들웨어는 애플리케이션에 도달하기 전 HTTP 요청이 통과해야 하는 일련의 "레이어"로 생각하는 것이 좋습니다. 각 레이어는 요청을 검사하고, 필요하다면 요청을 완전히 거부할 수도 있습니다.

> {tip} 모든 미들웨어는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해결되므로, 필요하다면 미들웨어의 생성자에서 의존성을 타입 힌트할 수 있습니다.

<a name="middleware-and-responses"></a>
#### 미들웨어와 응답

물론, 미들웨어는 요청이 애플리케이션에 더 깊이 전달되기 전 또는 후에 작업을 수행할 수 있습니다. 예를 들어, 아래 미들웨어는 요청이 애플리케이션에서 처리되기 **이전**에 작업을 수행합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;

class BeforeMiddleware
{
    public function handle($request, Closure $next)
    {
        // 작업 실행

        return $next($request);
    }
}
```

반면, 다음 미들웨어는 요청이 애플리케이션에서 처리된 **이후**에 작업을 수행합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;

class AfterMiddleware
{
    public function handle($request, Closure $next)
    {
        $response = $next($request);

        // 작업 실행

        return $response;
    }
}
```

<a name="registering-middleware"></a>
## 미들웨어 등록하기

<a name="global-middleware"></a>
### 글로벌 미들웨어

매 HTTP 요청마다 미들웨어를 실행하고 싶다면, `app/Http/Kernel.php` 클래스의 `$middleware` 프로퍼티에 해당 미들웨어 클래스를 추가하세요.

<a name="assigning-middleware-to-routes"></a>
### 미들웨어를 라우트에 할당하기

특정 라우트에 미들웨어를 할당하려면, 먼저 애플리케이션의 `app/Http/Kernel.php` 파일에서 미들웨어를 키와 함께 등록해야 합니다. 기본적으로 이 클래스의 `$routeMiddleware` 프로퍼티에는 Laravel의 기본 미들웨어 항목이 들어 있습니다. 여기에 직접 작성한 미들웨어를 추가하고, 원하는 키를 할당할 수 있습니다:

```php
// App\Http\Kernel 클래스 내...

protected $routeMiddleware = [
    'auth' => \App\Http\Middleware\Authenticate::class,
    'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
    'bindings' => \Illuminate\Routing\Middleware\SubstituteBindings::class,
    'cache.headers' => \Illuminate\Http\Middleware\SetCacheHeaders::class,
    'can' => \Illuminate\Auth\Middleware\Authorize::class,
    'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
    'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
    'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
    'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
];
```

미들웨어를 HTTP 커널에 정의한 후, `middleware` 메서드를 사용해 라우트에 미들웨어를 할당할 수 있습니다:

```php
Route::get('/profile', function () {
    //
})->middleware('auth');
```

여러 개의 미들웨어를 라우트에 할당하려면, 미들웨어 이름들의 배열을 `middleware` 메서드에 전달하면 됩니다:

```php
Route::get('/', function () {
    //
})->middleware(['first', 'second']);
```

미들웨어를 할당할 때, 클래스의 전체 네임스페이스를 직접 사용할 수도 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    //
})->middleware(EnsureTokenIsValid::class);
```

<a name="excluding-middleware"></a>
#### 미들웨어 제외하기

여러 라우트에 미들웨어를 그룹으로 할당할 때, 특정 라우트에서만 미들웨어가 적용되지 않도록 하고 싶을 수 있습니다. 이럴 땐 `withoutMiddleware` 메서드를 사용하면 됩니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::middleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/', function () {
        //
    });

    Route::get('/profile', function () {
        //
    })->withoutMiddleware([EnsureTokenIsValid::class]);
});
```

특정 미들웨어 세트를 전체 [라우트 그룹](/docs/{{version}}/routing#route-groups)에서 제외할 수도 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        //
    });
});
```

`withoutMiddleware` 메서드는 라우트 미들웨어만 제거할 수 있으며, [글로벌 미들웨어](#global-middleware)에는 적용되지 않습니다.

<a name="middleware-groups"></a>
### 미들웨어 그룹

여러 미들웨어를 하나의 키로 묶어서 더 쉽게 라우트에 할당하고 싶을 때가 있습니다. 이럴 땐 HTTP 커널의 `$middlewareGroups` 프로퍼티를 사용하면 됩니다.

기본적으로 Laravel에는 `web` 및 `api` 미들웨어 그룹이 제공되며, 각각 웹 및 API 라우트에 자주 사용되는 미들웨어가 포함되어 있습니다. 이 미들웨어 그룹들은, 해당하는 `web` 및 `api` 라우트 파일 내 라우트에 `App\Providers\RouteServiceProvider`가 자동으로 적용합니다:

```php
/**
 * The application's route middleware groups.
 *
 * @var array
 */
protected $middlewareGroups = [
    'web' => [
        \App\Http\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        // \Illuminate\Session\Middleware\AuthenticateSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \App\Http\Middleware\VerifyCsrfToken::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

    'api' => [
        'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],
];
```

미들웨어 그룹은 개별 미들웨어와 동일한 방식으로 라우트 및 컨트롤러 액션에 할당할 수 있습니다. 미들웨어 그룹을 사용하면 여러 미들웨어를 한 번에 라우트에 할당할 때 더욱 편리합니다:

```php
Route::get('/', function () {
    //
})->middleware('web');

Route::middleware(['web'])->group(function () {
    //
});
```

> {tip} 기본적으로, `web` 및 `api` 미들웨어 그룹은 `App\Providers\RouteServiceProvider`에 의해 애플리케이션의 `routes/web.php` 및 `routes/api.php`에 자동으로 적용됩니다.

<a name="sorting-middleware"></a>
### 미들웨어 정렬

드물게, 미들웨어가 특정 순서대로 실행되기를 원하지만 라우트에 할당하는 순서를 직접 제어할 수 없는 경우가 있습니다. 이럴 때는 `app/Http/Kernel.php` 파일의 `$middlewarePriority` 프로퍼티를 사용하여 미들웨어 우선순위를 지정할 수 있습니다. 이 프로퍼티가 기본적으로 HTTP 커널에 없을 수도 있으니, 아래의 기본 정의를 복사하여 사용하세요:

```php
/**
 * The priority-sorted list of middleware.
 *
 * This forces non-global middleware to always be in the given order.
 *
 * @var string[]
 */
protected $middlewarePriority = [
    \Illuminate\Cookie\Middleware\EncryptCookies::class,
    \Illuminate\Session\Middleware\StartSession::class,
    \Illuminate\View\Middleware\ShareErrorsFromSession::class,
    \Illuminate\Contracts\Auth\Middleware\AuthenticatesRequests::class,
    \Illuminate\Routing\Middleware\ThrottleRequests::class,
    \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
    \Illuminate\Session\Middleware\AuthenticateSession::class,
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
    \Illuminate\Auth\Middleware\Authorize::class,
];
```

<a name="middleware-parameters"></a>
## 미들웨어 파라미터

미들웨어는 추가 파라미터를 받을 수도 있습니다. 예를 들어, 인증된 사용자가 특정 "역할"을 가지고 있는지 확인해야 하는 경우, 역할 이름을 추가 인수로 받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

추가 미들웨어 파라미터는 `$next` 인자 이후에 전달됩니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;

class EnsureUserHasRole
{
    /**
     * Handle the incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @param  string  $role
     * @return mixed
     */
    public function handle($request, Closure $next, $role)
    {
        if (! $request->user()->hasRole($role)) {
            // 리다이렉트 등 처리...
        }

        return $next($request);
    }
}
```

라우트를 정의할 때, 미들웨어 이름과 파라미터를 `:`로 구분하여 지정할 수 있습니다. 여러 파라미터가 있을 때는 쉼표로 구분합니다:

```php
Route::put('/post/{id}', function ($id) {
    //
})->middleware('role:editor');
```

<a name="terminable-middleware"></a>
## 종료 가능한 미들웨어

가끔 미들웨어가 HTTP 응답이 브라우저로 전송된 후에 추가 작업을 수행해야 할 수 있습니다. 만약 미들웨어에 `terminate` 메서드를 정의하고 웹 서버가 FastCGI를 사용 중이라면, 응답 전송 후 `terminate` 메서드가 자동으로 호출됩니다:

```php
<?php

namespace Illuminate\Session\Middleware;

use Closure;

class TerminatingMiddleware
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        return $next($request);
    }

    /**
     * Handle tasks after the response has been sent to the browser.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Illuminate\Http\Response  $response
     * @return void
     */
    public function terminate($request, $response)
    {
        // ...
    }
}
```

`terminate` 메서드는 요청과 응답 객체를 모두 받아야 합니다. 종료 가능한 미들웨어를 정의했다면, `app/Http/Kernel.php` 파일의 라우트 미들웨어 또는 글로벌 미들웨어 목록에 추가해야 합니다.

Laravel이 미들웨어의 `terminate` 메서드를 호출할 때마다 [서비스 컨테이너](/docs/{{version}}/container)에서 새로운 미들웨어 인스턴스를 해결합니다. 만약 `handle`과 `terminate` 메서드가 동일한 미들웨어 인스턴스를 사용하기를 원한다면, 컨테이너의 `singleton` 메서드를 사용해 미들웨어를 등록해야 합니다. 일반적으로 이는 `AppServiceProvider`의 `register` 메서드에서 처리합니다:

```php
use App\Http\Middleware\TerminatingMiddleware;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->app->singleton(TerminatingMiddleware::class);
}
```