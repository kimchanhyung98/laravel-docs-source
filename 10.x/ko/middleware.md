# 미들웨어 (Middleware)

- [소개](#introduction)
- [미들웨어 정의하기](#defining-middleware)
- [미들웨어 등록하기](#registering-middleware)
    - [글로벌 미들웨어](#global-middleware)
    - [라우트에 미들웨어 할당하기](#assigning-middleware-to-routes)
    - [미들웨어 그룹](#middleware-groups)
    - [미들웨어 실행 순서 정렬하기](#sorting-middleware)
- [미들웨어 매개변수](#middleware-parameters)
- [종료 가능한 미들웨어](#terminable-middleware)

<a name="introduction"></a>
## 소개

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 검사하고 필터링하는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel은 사용자가 인증되었는지 확인하는 미들웨어를 포함하고 있습니다. 사용자가 인증되지 않았다면, 해당 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리디렉션합니다. 반면, 사용자가 인증되었다면 요청은 애플리케이션 내부로 더 진행됩니다.

인증 외에도 다양한 작업을 수행하는 미들웨어를 작성할 수 있습니다. 예를 들어, 로깅 미들웨어는 애플리케이션에 들어오는 모든 요청을 기록할 수 있습니다. Laravel 프레임워크에는 인증과 CSRF 보호 같은 여러 기본 미들웨어가 포함되어 있으며, 이들은 모두 `app/Http/Middleware` 디렉터리에 위치합니다.

<a name="defining-middleware"></a>
## 미들웨어 정의하기

새로운 미들웨어를 생성하려면 `make:middleware` Artisan 명령어를 사용하세요:

```shell
php artisan make:middleware EnsureTokenIsValid
```

이 명령어는 `app/Http/Middleware` 디렉터리에 새 클래스 `EnsureTokenIsValid`를 생성합니다. 이 미들웨어는 전달된 `token` 입력 값이 지정한 값과 일치할 때만 라우트에 접근을 허용하며, 그렇지 않으면 사용자들을 `home` URI로 리디렉션합니다:

```
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
            return redirect('home');
        }

        return $next($request);
    }
}
```

보시다시피, 전달된 `token`이 비밀 토큰과 일치하지 않으면 미들웨어는 HTTP 리디렉션을 클라이언트에 반환하고, 일치하면 요청이 애플리케이션 내부로 전달됩니다. 요청을 더 진행시키려면, `$next` 콜백을 `$request`와 함께 호출해야 합니다.

미들웨어를 HTTP 요청이 애플리케이션에 도달하기 전 통과해야 하는 "레이어"라고 생각하는 것이 좋습니다. 각 레이어는 요청을 검사하고, 아예 거부할 수도 있습니다.

> [!NOTE]  
> 모든 미들웨어는 [서비스 컨테이너](/docs/10.x/container)를 통해 해석되므로, 미들웨어 생성자의 의존성이 필요한 경우 타입 힌팅이 가능합니다.

<a name="middleware-and-responses"></a>
#### 미들웨어와 응답

미들웨어는 요청을 애플리케이션에 더 전달하기 전 또는 후 작업을 수행할 수 있습니다. 예를 들어, 아래 미들웨어는 요청이 애플리케이션에 처리되기 **전**에 작업을 수행합니다:

```
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

반면에, 이 미들웨어는 요청이 애플리케이션에 처리된 **후**에 작업을 수행합니다:

```
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
## 미들웨어 등록하기

<a name="global-middleware"></a>
### 글로벌 미들웨어

만약 미들웨어를 모든 HTTP 요청에서 실행하고 싶다면, `app/Http/Kernel.php` 클래스의 `$middleware` 속성에 미들웨어 클래스를 나열하세요.

<a name="assigning-middleware-to-routes"></a>
### 라우트에 미들웨어 할당하기

특정 라우트에 미들웨어를 할당하려면, 라우트를 정의할 때 `middleware` 메서드를 호출하면 됩니다:

```
use App\Http\Middleware\Authenticate;

Route::get('/profile', function () {
    // ...
})->middleware(Authenticate::class);
```

라우트에 여러 미들웨어를 할당할 경우, `middleware` 메서드에 미들웨어 이름 배열을 전달하면 됩니다:

```
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

편의를 위해, 애플리케이션의 `app/Http/Kernel.php` 파일에서 미들웨어 별칭(alias)을 설정할 수 있습니다. 기본적으로 이 클래스의 `$middlewareAliases` 속성에는 Laravel 기본 미들웨어가 포함되어 있으며, 여기에 직접 만든 미들웨어를 추가하고 원하는 별칭을 부여할 수 있습니다:

```
// App\Http\Kernel 클래스 내...

protected $middlewareAliases = [
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

HTTP 커널에 미들웨어 별칭을 정의한 후, 라우트에 미들웨어를 할당할 때 별칭을 사용할 수 있습니다:

```
Route::get('/profile', function () {
    // ...
})->middleware('auth');
```

<a name="excluding-middleware"></a>
#### 미들웨어 제외하기

미들웨어 그룹에 할당한 미들웨어가 특정 라우트에 적용되지 않게 하고 싶다면, `withoutMiddleware` 메서드를 사용하여 개별 라우트에서 미들웨어를 제외할 수 있습니다:

```
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

또는 특정 미들웨어를 전체 라우트 그룹에서 제외할 수도 있습니다:

```
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

여러 미들웨어를 하나의 키로 묶어 라우트에 할당을 쉽게 할 수 있습니다. HTTP 커널의 `$middlewareGroups` 속성을 사용하면 됩니다.

Laravel은 `web`과 `api`라는 미리 정의된 미들웨어 그룹을 포함하고 있으며, 웹과 API 라우트에 적용할 일반적인 미들웨어를 묶어 제공합니다. 이 미들웨어 그룹들은 애플리케이션의 `App\Providers\RouteServiceProvider` 서비스 프로바이더가 각각 `web`과 `api` 라우트 파일 내 라우트에 자동으로 적용합니다:

```
/**
 * 애플리케이션 라우트 미들웨어 그룹.
 *
 * @var array
 */
protected $middlewareGroups = [
    'web' => [
        \App\Http\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \App\Http\Middleware\VerifyCsrfToken::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

    'api' => [
        \Illuminate\Routing\Middleware\ThrottleRequests::class.':api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],
];
```

미들웨어 그룹은 개별 미들웨어와 같은 문법으로 라우트나 컨트롤러 액션에 할당할 수 있습니다. 미들웨어 그룹을 사용하면 한 번에 여러 미들웨어를 라우트에 편리하게 할당할 수 있습니다:

```
Route::get('/', function () {
    // ...
})->middleware('web');

Route::middleware(['web'])->group(function () {
    // ...
});
```

> [!NOTE]  
> 기본적으로 `web`과 `api` 미들웨어 그룹은 애플리케이션의 `routes/web.php`와 `routes/api.php` 파일에 `App\Providers\RouteServiceProvider`에 의해 자동으로 적용됩니다.

<a name="sorting-middleware"></a>
### 미들웨어 실행 순서 정렬하기

가끔 미들웨어가 반드시 특정 순서대로 실행되어야 하지만, 라우트에 미들웨어를 할당할 때 실행 순서를 직접 제어할 수 없는 경우가 있습니다. 이때 `app/Http/Kernel.php` 파일의 `$middlewarePriority` 속성을 사용하여 미들웨어 우선순위를 명시할 수 있습니다. 이 속성은 기본적으로 HTTP 커널에 없을 수 있으므로, 필요하면 아래 기본 정의를 복사해서 추가하세요:

```
/**
 * 우선순위 정렬된 미들웨어 목록.
 *
 * 이 설정은 글로벌이 아닌 미들웨어가 항상 지정한 순서로 실행되도록 강제합니다.
 *
 * @var string[]
 */
protected $middlewarePriority = [
    \Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests::class,
    \Illuminate\Cookie\Middleware\EncryptCookies::class,
    \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
    \Illuminate\Session\Middleware\StartSession::class,
    \Illuminate\View\Middleware\ShareErrorsFromSession::class,
    \Illuminate\Contracts\Auth\Middleware\AuthenticatesRequests::class,
    \Illuminate\Routing\Middleware\ThrottleRequests::class,
    \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
    \Illuminate\Contracts\Session\Middleware\AuthenticatesSessions::class,
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
    \Illuminate\Auth\Middleware\Authorize::class,
];
```

<a name="middleware-parameters"></a>
## 미들웨어 매개변수

미들웨어는 추가 매개변수를 받을 수도 있습니다. 예를 들어, 인증된 사용자가 특정 역할(role)을 가지고 있는지 확인해야 하는 경우, 역할 이름을 추가 인수로 받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

미들웨어에 전달하는 추가 매개변수는 `$next` 인수 다음에 옵니다:

```
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
            // 리디렉션 처리...
        }

        return $next($request);
    }

}
```

라우트를 정의할 때, 미들웨어 이름과 매개변수 사이는 `:`으로 구분하여 지정합니다:

```
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware('role:editor');
```

여러 매개변수는 쉼표로 구분할 수 있습니다:

```
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware('role:editor,publisher');
```

<a name="terminable-middleware"></a>
## 종료 가능한 미들웨어

때때로 미들웨어는 HTTP 응답이 브라우저로 전송된 후에 작업을 수행해야 할 수도 있습니다. 만약 미들웨어에 `terminate` 메서드를 정의하고 웹 서버가 FastCGI를 사용 중이라면, 응답이 브라우저로 전송된 후 자동으로 `terminate` 메서드가 호출됩니다:

```
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
     * 응답이 브라우저로 전송된 후 작업을 처리합니다.
     */
    public function terminate(Request $request, Response $response): void
    {
        // ...
    }
}
```

`terminate` 메서드는 요청과 응답 두 가지 모두를 매개변수로 받습니다. 종료 가능한 미들웨어를 정의한 후, 이를 `app/Http/Kernel.php` 파일의 라우트 또는 글로벌 미들웨어 목록에 추가해야 합니다.

`terminate` 메서드가 호출될 때 Laravel은 [서비스 컨테이너](/docs/10.x/container)에서 미들웨어의 새로운 인스턴스를 해석합니다. `handle`과 `terminate` 메서드 호출 시 동일한 미들웨어 인스턴스를 사용하려면, 컨테이너에 `singleton` 메서드를 통해 미들웨어를 등록하세요. 보통 `AppServiceProvider`의 `register` 메서드에서 다음과 같이 등록합니다:

```
use App\Http\Middleware\TerminatingMiddleware;

/**
 * 애플리케이션 서비스 등록.
 */
public function register(): void
{
    $this->app->singleton(TerminatingMiddleware::class);
}
```