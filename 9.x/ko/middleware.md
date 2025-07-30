# 미들웨어 (Middleware)

- [소개](#introduction)
- [미들웨어 정의하기](#defining-middleware)
- [미들웨어 등록하기](#registering-middleware)
    - [글로벌 미들웨어](#global-middleware)
    - [미들웨어를 라우트에 할당하기](#assigning-middleware-to-routes)
    - [미들웨어 그룹](#middleware-groups)
    - [미들웨어 우선순위 설정](#sorting-middleware)
- [미들웨어 파라미터](#middleware-parameters)
- [종료 가능한 미들웨어](#terminable-middleware)

<a name="introduction"></a>
## 소개

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 검사하고 필터링할 수 있는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel은 사용자가 인증되었는지 확인하는 미들웨어를 포함합니다. 만약 사용자가 인증되지 않았다면, 이 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리디렉션합니다. 반면, 사용자가 인증되어 있다면 요청이 애플리케이션 내부로 계속 진행되도록 허용합니다.

인증 외에도 다양한 작업을 수행하는 미들웨어를 작성할 수 있습니다. 예를 들어, 로깅 미들웨어는 애플리케이션으로 들어오는 모든 요청을 기록할 수도 있습니다. Laravel 프레임워크에는 인증과 CSRF 보호 같은 여러 미들웨어가 내장되어 있으며, 이 모든 미들웨어는 `app/Http/Middleware` 디렉토리에 위치합니다.

<a name="defining-middleware"></a>
## 미들웨어 정의하기

새 미들웨어를 생성하려면 `make:middleware` Artisan 명령어를 사용하세요:

```shell
php artisan make:middleware EnsureTokenIsValid
```

이 명령어는 `app/Http/Middleware` 디렉토리에 `EnsureTokenIsValid` 클래스를 생성합니다. 이 미들웨어에서는 제공된 `token` 입력값이 지정된 값과 일치할 때만 라우트에 접근을 허용하고, 그렇지 않으면 사용자를 `home` URI로 리디렉션합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;

class EnsureTokenIsValid
{
    /**
     * 들어오는 요청 처리.
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

보시다시피, 주어진 `token`이 비밀 토큰과 일치하지 않으면 미들웨어는 HTTP 리디렉션 응답을 반환합니다. 그렇지 않으면 요청이 애플리케이션 내부로 전달되어 다음 단계로 진행됩니다. 요청을 더 깊게 전달하려면(미들웨어를 "통과"시키려면) `$next` 콜백에 `$request`를 전달하며 호출해야 합니다.

미들웨어는 HTTP 요청이 애플리케이션에 도달하기 전에 통과해야 할 일련의 "레이어"라고 생각하는 것이 좋습니다. 각 레이어에서 요청을 검사하고 완전히 차단할 수도 있습니다.

> [!NOTE]
> 모든 미들웨어는 [서비스 컨테이너](/docs/9.x/container)를 통해 해결되므로, 미들웨어 생성자의 의존성으로 필요한 것을 타입 힌트할 수 있습니다.

<a name="middleware-and-responses"></a>
#### 미들웨어와 응답

물론, 미들웨어는 요청을 애플리케이션 내부로 전달하기 전이나 후에 작업을 수행할 수 있습니다. 예를 들어, 아래 미들웨어는 요청이 처리되기 **전에** 작업을 수행합니다:

```php
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

반면, 이 미들웨어는 요청이 애플리케이션에서 처리된 **후에** 작업을 수행합니다:

```php
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

애플리케이션의 모든 HTTP 요청에 대해 미들웨어를 실행하고 싶다면, `app/Http/Kernel.php` 클래스 내의 `$middleware` 속성에 해당 미들웨어 클래스를 등록하세요.

<a name="assigning-middleware-to-routes"></a>
### 미들웨어를 라우트에 할당하기

특정 라우트에만 미들웨어를 할당하려면, 우선 애플리케이션의 `app/Http/Kernel.php` 파일에서 미들웨어에 키를 지정해야 합니다. 기본적으로 이 클래스의 `$routeMiddleware` 속성에는 Laravel에 포함된 미들웨어가 등록되어 있습니다. 이 목록에 새로운 미들웨어를 추가하고 원하는 키를 지정할 수 있습니다:

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

미들웨어가 HTTP 커널에 정의되면, `middleware` 메서드를 이용해 라우트에 미들웨어를 할당할 수 있습니다:

```php
Route::get('/profile', function () {
    //
})->middleware('auth');
```

여러 미들웨어를 동시에 할당하려면, `middleware` 메서드에 미들웨어 이름 배열을 전달하세요:

```php
Route::get('/', function () {
    //
})->middleware(['first', 'second']);
```

미들웨어를 할당할 때, 완전한 클래스 이름을 직접 넘길 수도 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    //
})->middleware(EnsureTokenIsValid::class);
```

<a name="excluding-middleware"></a>
#### 미들웨어 제외하기

미들웨어를 여러 라우트 그룹에 할당한 경우, 특정 그룹 내에서 특정 라우트에만 미들웨어가 적용되지 않도록 할 수 있습니다. 이때 `withoutMiddleware` 메서드를 사용하세요:

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

또한 특정 미들웨어 집합을 전체 라우트 그룹에서 제외시킬 수도 있습니다:

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

여러 미들웨어를 하나의 키 아래 묶어 라우트에 할당하기 쉽게 만들고 싶을 때가 있습니다. 이럴 때 HTTP 커널의 `$middlewareGroups` 속성을 사용하면 됩니다.

Laravel은 웹과 API 라우트에 흔히 적용되는 `web` 및 `api` 미들웨어 그룹을 기본으로 제공합니다. 이 미들웨어 그룹은 애플리케이션의 `App\Providers\RouteServiceProvider` 서비스 프로바이더가 자동으로 `web`과 `api` 라우트 파일 안의 라우트에 적용합니다:

```php
/**
 * 애플리케이션의 라우트 미들웨어 그룹.
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
        'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],
];
```

미들웨어 그룹은 개별 미들웨어와 동일한 방식으로 라우트나 컨트롤러 액션에 할당할 수 있습니다. 미들웨어 그룹을 사용하면 여러 미들웨어를 한 번에 라우트에 쉽게 할당할 수 있습니다:

```php
Route::get('/', function () {
    //
})->middleware('web');

Route::middleware(['web'])->group(function () {
    //
});
```

> [!NOTE]
> 기본적으로 `web`과 `api` 미들웨어 그룹은 애플리케이션의 `routes/web.php`와 `routes/api.php` 파일에 `App\Providers\RouteServiceProvider`에서 자동으로 적용됩니다.

<a name="sorting-middleware"></a>
### 미들웨어 우선순위 설정

가끔 미들웨어가 특정 순서로 실행되어야 하지만, 라우트에 할당할 때 미들웨어들이 어떤 순서로 적용될지 제어할 수 없는 경우가 있습니다. 이럴 때, `app/Http/Kernel.php` 파일의 `$middlewarePriority` 속성에 미들웨어 실행 순위를 지정할 수 있습니다. 이 속성은 기본적으로 HTTP 커널에 없을 수 있는데, 없다면 다음 기본 정의를 복사해서 사용할 수 있습니다:

```php
/**
 * 우선순위에 따른 미들웨어 목록.
 *
 * 이 설정은 글로벌 미들웨어가 아닌 미들웨어가 항상 지정된 순서대로 실행되도록 합니다.
 *
 * @var string[]
 */
protected $middlewarePriority = [
    \Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests::class,
    \Illuminate\Cookie\Middleware\EncryptCookies::class,
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
## 미들웨어 파라미터

미들웨어는 추가 파라미터를 받을 수도 있습니다. 예를 들어, 인증된 사용자가 특정 역할(role)을 가지고 있는지 확인해야 할 때, 역할 이름을 추가 인수로 받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

추가 미들웨어 파라미터는 `$next` 인수 뒤에 전달됩니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;

class EnsureUserHasRole
{
    /**
     * 들어오는 요청 처리.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @param  string  $role
     * @return mixed
     */
    public function handle($request, Closure $next, $role)
    {
        if (! $request->user()->hasRole($role)) {
            // 리디렉션 처리...
        }

        return $next($request);
    }
}
```

라우트를 정의할 때 미들웨어 이름과 파라미터를 `:`로 구분하여 지정할 수 있습니다. 여러 파라미터는 쉼표로 구분하세요:

```php
Route::put('/post/{id}', function ($id) {
    //
})->middleware('role:editor');
```

<a name="terminable-middleware"></a>
## 종료 가능한 미들웨어

때로는 HTTP 응답이 브라우저에 전송된 후에 미들웨어가 작업을 수행해야 할 때가 있습니다. 만약 미들웨어에 `terminate` 메서드를 정의하고 웹 서버가 FastCGI를 사용 중이라면, 응답이 브라우저에 전송된 뒤에 이 `terminate` 메서드가 자동으로 호출됩니다:

```php
<?php

namespace Illuminate\Session\Middleware;

use Closure;

class TerminatingMiddleware
{
    /**
     * 들어오는 요청 처리.
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
     * 응답이 브라우저에 전송된 후 작업 처리.
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

`terminate` 메서드는 요청과 응답 둘 다를 인수로 받아야 합니다. 종료 가능한 미들웨어를 정의한 후에는 `app/Http/Kernel.php` 파일에서 라우트용 미들웨어나 글로벌 미들웨어 목록에 추가해야 합니다.

미들웨어의 `terminate` 메서드를 호출할 때, Laravel은 [서비스 컨테이너](/docs/9.x/container)에서 미들웨어의 새로운 인스턴스를 생성해 사용합니다. 만약 `handle`과 `terminate` 메서드 호출 시 같은 미들웨어 인스턴스를 사용하고 싶다면, `AppServiceProvider`의 `register` 메서드에서 서비스 컨테이너의 `singleton` 메서드를 사용해 미들웨어를 등록하세요:

```php
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