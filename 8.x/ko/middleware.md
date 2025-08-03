# 미들웨어 (Middleware)

- [소개](#introduction)
- [미들웨어 정의하기](#defining-middleware)
- [미들웨어 등록하기](#registering-middleware)
    - [글로벌 미들웨어](#global-middleware)
    - [미들웨어를 라우트에 할당하기](#assigning-middleware-to-routes)
    - [미들웨어 그룹](#middleware-groups)
    - [미들웨어 실행 순서 정렬하기](#sorting-middleware)
- [미들웨어 파라미터](#middleware-parameters)
- [종료 가능한 미들웨어](#terminable-middleware)

<a name="introduction"></a>
## 소개

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 검사하고 필터링하는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 사용자가 인증되었는지 확인하는 미들웨어가 포함되어 있습니다. 만약 사용자가 인증되지 않았다면, 해당 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리디렉션합니다. 반면 사용자가 인증되어 있다면, 요청이 애플리케이션 내부로 계속 진행될 수 있도록 허용합니다.

인증 이외에도 다양한 작업을 수행하는 추가 미들웨어를 작성할 수 있습니다. 예를 들어, 로깅 미들웨어는 애플리케이션에 들어오는 모든 요청을 기록할 수 있습니다. Laravel 프레임워크에는 인증 및 CSRF 보호를 위한 미들웨어 등 여러 미들웨어가 포함되어 있으며, 모든 미들웨어는 `app/Http/Middleware` 디렉터리 내에 위치합니다.

<a name="defining-middleware"></a>
## 미들웨어 정의하기

새로운 미들웨어를 만들려면 `make:middleware` Artisan 명령어를 사용하세요:

```
php artisan make:middleware EnsureTokenIsValid
```

이 명령어는 `app/Http/Middleware` 디렉터리에 `EnsureTokenIsValid` 클래스를 새로 생성합니다. 이 미들웨어에서는 전달된 `token` 입력값이 지정한 값과 일치하는 경우에만 해당 라우트에 접근을 허용합니다. 그 외의 경우에는 사용자를 `home` URI로 리디렉션합니다:

```
<?php

namespace App\Http\Middleware;

use Closure;

class EnsureTokenIsValid
{
    /**
     * 들어오는 요청을 처리합니다.
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

위 예제에서, 전달된 `token` 값이 비밀 토큰과 일치하지 않으면 미들웨어는 HTTP 리디렉션 응답을 반환합니다. 그렇지 않으면 요청은 애플리케이션 내부로 전달됩니다. 요청을 애플리케이션 내부로 전달하려면 `$next` 콜백에 `$request`를 전달하며 호출해야 합니다.

미들웨어를 HTTP 요청이 애플리케이션에 도착하기 전에 통과해야 하는 여러 "레이어"로 생각하는 것이 가장 좋습니다. 각 레이어는 요청을 검사하고 완전히 거부할 수도 있습니다.

> [!TIP]
> 모든 미들웨어는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 미들웨어 생성자에 필요한 의존성을 타입힌트로 주입할 수 있습니다.

<a name="middleware-and-responses"></a>
#### 미들웨어 & 응답

물론, 미들웨어는 요청을 애플리케이션 내부로 넘기기 전 또는 후에 작업을 수행할 수 있습니다. 예를 들어, 다음 미들웨어는 애플리케이션이 요청을 처리하기 **전에** 어떤 작업을 수행합니다:

```
<?php

namespace App\Http\Middleware;

use Closure;

class BeforeMiddleware
{
    public function handle($request, Closure $next)
    {
        // 작업 수행

        return $next($request);
    }
}
```

반면, 다음 미들웨어는 애플리케이션이 요청을 처리한 **후에** 작업을 수행합니다:

```
<?php

namespace App\Http\Middleware;

use Closure;

class AfterMiddleware
{
    public function handle($request, Closure $next)
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

모든 HTTP 요청에 대해 미들웨어가 실행되도록 하려면, `app/Http/Kernel.php` 클래스의 `$middleware` 속성에 미들웨어 클래스를 리스트에 추가하세요.

<a name="assigning-middleware-to-routes"></a>
### 미들웨어를 라우트에 할당하기

특정 라우트에 미들웨어를 지정하고 싶다면, 먼저 애플리케이션의 `app/Http/Kernel.php` 파일에서 미들웨어에 키를 할당해야 합니다. 기본적으로 이 클래스의 `$routeMiddleware` 속성에 Laravel이 포함하는 미들웨어가 미리 정의되어 있습니다. 여기에 직접 미들웨어를 추가하고 원하는 키를 할당할 수 있습니다:

```
// App\Http\Kernel 클래스 내부...

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

미들웨어를 HTTP 커널에 정의하면, `middleware` 메서드를 사용해 라우트에 미들웨어를 할당할 수 있습니다:

```
Route::get('/profile', function () {
    //
})->middleware('auth');
```

복수의 미들웨어를 지정하려면, `middleware` 메서드에 미들웨어 이름의 배열을 전달하세요:

```
Route::get('/', function () {
    //
})->middleware(['first', 'second']);
```

미들웨어를 할당할 때, 완전한 클래스 이름(FQCN)을 사용할 수도 있습니다:

```
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    //
})->middleware(EnsureTokenIsValid::class);
```

<a name="excluding-middleware"></a>
#### 미들웨어 제외하기

미들웨어를 라우트 그룹에 할당하는 경우, 특정 개별 라우트에 미들웨어를 적용하지 않도록 할 필요가 있을 수 있습니다. 이때 `withoutMiddleware` 메서드를 사용해 미들웨어 적용을 제외할 수 있습니다:

```
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

또한, 전체 라우트 그룹에서 특정 미들웨어 집합을 제외할 수도 있습니다:

```
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

가끔 여러 미들웨어를 하나의 키 아래 묶어 라우트에 쉽게 할당하고 싶을 때가 있습니다. 이럴 때 HTTP 커널의 `$middlewareGroups` 속성을 사용해 미들웨어 그룹을 정의할 수 있습니다.

Laravel은 기본적으로 `web`과 `api` 미들웨어 그룹을 제공합니다. 이는 일반적으로 웹과 API 라우트에 적용할 미들웨어들을 묶은 것입니다. 이 미들웨어 그룹들은 애플리케이션의 `App\Providers\RouteServiceProvider` 서비스 프로바이더에 의해 각각 `web`과 `api` 라우트 파일 내의 라우트에 자동으로 적용됩니다:

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

미들웨어 그룹은 개별 미들웨어와 동일한 방식으로 라우트나 컨트롤러 액션에 할당할 수 있습니다. 미들웨어 그룹을 사용하면 한 번에 여러 미들웨어를 라우트에 할당하는 작업이 더 편리해집니다:

```
Route::get('/', function () {
    //
})->middleware('web');

Route::middleware(['web'])->group(function () {
    //
});
```

> [!TIP]
> 기본적으로, `web`과 `api` 미들웨어 그룹은 `App\Providers\RouteServiceProvider`가 애플리케이션의 `routes/web.php`와 `routes/api.php` 파일에 자동으로 적용합니다.

<a name="sorting-middleware"></a>
### 미들웨어 실행 순서 정렬하기

가끔 미들웨어가 특정 순서로 실행되어야 하지만 라우트에 지정할 때 실행 순서를 제어할 수 없을 때가 있습니다. 이 경우, `app/Http/Kernel.php` 파일의 `$middlewarePriority` 속성을 사용해 미들웨어 실행 순서를 지정할 수 있습니다. 이 속성은 기본적으로 HTTP 커널에 없을 수 있는데, 없다면 아래 기본 정의를 복사하시면 됩니다:

```
/**
 * 우선 순위가 정렬된 미들웨어 목록.
 *
 * 이 설정은 비글로벌 미들웨어가 항상 지정된 순서대로 실행되도록 강제합니다.
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

미들웨어는 추가적인 파라미터를 받을 수 있습니다. 예를 들어, 인증된 사용자가 특정 "역할(role)"을 가지고 있는지 확인하고자 할 때, `EnsureUserHasRole` 미들웨어를 만들어 역할 이름을 추가 인수로 받을 수 있습니다.

추가 미들웨어 파라미터는 `$next` 인수 뒤에 전달됩니다:

```
<?php

namespace App\Http\Middleware;

use Closure;

class EnsureUserHasRole
{
    /**
     * 들어오는 요청을 처리합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @param  string  $role
     * @return mixed
     */
    public function handle($request, Closure $next, $role)
    {
        if (! $request->user()->hasRole($role)) {
            // 리디렉션 등 처리...
        }

        return $next($request);
    }

}
```

라우트 정의 시, 미들웨어 이름과 매개변수를 `:`로 구분하여 전달할 수 있습니다. 복수 매개변수는 쉼표로 구분합니다:

```
Route::put('/post/{id}', function ($id) {
    //
})->middleware('role:editor');
```

<a name="terminable-middleware"></a>
## 종료 가능한 미들웨어 (Terminable Middleware)

때때로 미들웨어가 HTTP 응답이 브라우저에 전송된 후 작업을 수행해야 할 수 있습니다. 미들웨어에 `terminate` 메서드를 정의하고 웹 서버가 FastCGI를 사용 중이라면, 응답이 브라우저에 전송된 후 자동으로 `terminate` 메서드가 호출됩니다:

```
<?php

namespace Illuminate\Session\Middleware;

use Closure;

class TerminatingMiddleware
{
    /**
     * 들어오는 요청을 처리합니다.
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
     * 응답이 브라우저에 전송된 후 작업을 처리합니다.
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

`terminate` 메서드에서는 요청과 응답 두 가지 모두를 받아야 합니다. 종료 가능한 미들웨어를 정의하면, 이를 `app/Http/Kernel.php` 파일의 라우트 또는 글로벌 미들웨어 목록에 추가해야 합니다.

`terminate` 메서드를 호출할 때, Laravel은 [서비스 컨테이너](/docs/{{version}}/container)에서 미들웨어의 새로운 인스턴스를 해석합니다. `handle`과 `terminate` 메서드가 동일한 미들웨어 인스턴스에서 실행되도록 하려면, 컨테이너의 `singleton` 메서드를 사용해 미들웨어를 싱글톤으로 등록해야 합니다. 일반적으로 이 작업은 `AppServiceProvider`의 `register` 메서드에서 수행합니다:

```
use App\Http\Middleware\TerminatingMiddleware;

/**
 * 애플리케이션 서비스 등록.
 *
 * @return void
 */
public function register()
{
    $this->app->singleton(TerminatingMiddleware::class);
}
```