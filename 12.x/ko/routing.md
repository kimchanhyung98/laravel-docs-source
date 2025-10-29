# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리다이렉트 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록 확인](#listing-your-routes)
    - [라우팅 커스터마이징](#routing-customization)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [선택적 파라미터](#parameters-optional-parameters)
    - [정규 표현식 제약](#parameters-regular-expression-constraints)
- [이름이 지정된 라우트](#named-routes)
- [라우트 그룹](#route-groups)
    - [미들웨어](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [서브도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 접두사](#route-group-prefixes)
    - [라우트 이름 접두사](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암묵적 바인딩](#implicit-binding)
    - [암묵적 Enum 바인딩](#implicit-enum-binding)
    - [명시적 바인딩](#explicit-binding)
- [폴백 라우트](#fallback-routes)
- [속도 제한](#rate-limiting)
    - [속도 제한자 정의](#defining-rate-limiters)
    - [라우트에 속도 제한자 부착](#attaching-rate-limiters-to-routes)
- [폼 메서드 위조](#form-method-spoofing)
- [현재 라우트 정보 접근](#accessing-the-current-route)
- [교차 출처 리소스 공유(CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

가장 기본적인 Laravel 라우트는 URI와 클로저(익명 함수)를 받아, 복잡한 설정 없이 라우트와 동작을 매우 간단하고 직관적으로 정의할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일

모든 Laravel 라우트는 `routes` 디렉토리에 위치한 라우트 파일에 정의합니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 명시된 설정에 따라 Laravel이 자동으로 로드합니다. `routes/web.php` 파일에는 웹 인터페이스를 위한 라우트를 정의하며, 이 라우트들은 `web` [미들웨어 그룹](/docs/12.x/middleware#laravels-default-middleware-groups)에 할당되어 세션 상태 관리, CSRF 보호 등 웹 환경에 필요한 기능이 제공됩니다.

대부분의 애플리케이션은 `routes/web.php`에 라우트를 정의하는 것부터 시작합니다. 이 파일에 정의된 라우트는 지정한 URL로 브라우저에서 접속하여 확인할 수 있습니다. 예를 들어 다음 라우트는 브라우저에서 `http://example.com/user`로 접속하면 실행됩니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트

애플리케이션에서 상태를 저장하지 않는 API를 제공하려면 `install:api` Artisan 명령어를 사용하여 API 라우팅을 활성화할 수 있습니다.

```shell
php artisan install:api
```

`install:api` 명령어는 [Laravel Sanctum](/docs/12.x/sanctum)를 설치합니다. Sanctum은 외부 API 소비자, SPA, 모바일 애플리케이션 인증을 위한 쉽고 강력한 API 토큰 인증 가드를 제공합니다. 또한, `routes/api.php` 파일이 생성됩니다.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

`routes/api.php` 파일의 라우트들은 상태가 없는(stateless) 라우트로서, `api` [미들웨어 그룹](/docs/12.x/middleware#laravels-default-middleware-groups)에 할당됩니다. 또한 `/api` 접두사가 해당 라우트에 자동으로 적용되므로, 파일 내 각 라우트마다 직접 접두사를 추가할 필요가 없습니다. 접두사는 애플리케이션의 `bootstrap/app.php` 파일을 수정하여 변경할 수 있습니다.

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메서드

라우터는 다양한 HTTP 메서드에 응답하는 라우트를 등록할 수 있습니다.

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

여러 HTTP 메서드에 응답하는 라우트를 등록해야 할 때에는 `match` 메서드를 사용할 수 있습니다. 모든 HTTP 메서드에 응답하는 라우트는 `any` 메서드를 사용합니다.

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일한 URI를 사용하는 여러 라우트를 정의하는 경우, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트를 `any`, `match`, `redirect` 메서드를 사용하는 라우트보다 먼저 정의해야 올바른 라우트가 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백 시그니처에 필요한 의존성을 타입힌트(type-hint)로 선언할 수 있습니다. 선언된 의존성은 Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입합니다. 예를 들어, `Illuminate\Http\Request` 클래스를 타입힌트하면 현재 HTTP 요청 객체가 자동으로 콜백에 전달됩니다.

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일(`routes/web.php`)에서 정의한 `POST`, `PUT`, `PATCH`, `DELETE` 라우트로 데이터를 전송하는 모든 HTML 폼에는 반드시 CSRF 토큰 필드를 포함해야 합니다. 그렇지 않으면 요청이 거부됩니다. 자세한 내용은 [CSRF 문서](/docs/12.x/csrf)를 참고하세요.

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리다이렉트 라우트

다른 URI로 리다이렉트하는 라우트를 정의하려면 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 간단한 리다이렉션에 전체 라우트나 컨트롤러를 만들 필요 없이 바로 사용할 수 있어 편리합니다.

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 선택적 세 번째 파라미터를 사용해 상태 코드를 변경할 수 있습니다.

```php
Route::redirect('/here', '/there', 301);
```

또는 `Route::permanentRedirect` 메서드를 사용하면 항상 `301` 상태 코드를 반환합니다.

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리다이렉트 라우트에서 라우트 파라미터를 사용할 때, `destination`과 `status` 파라미터는 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트

라우트에서 단순히 [뷰](/docs/12.x/views)를 반환하기만 한다면, `Route::view` 메서드를 사용할 수 있습니다. `redirect`와 마찬가지로 전체 라우트나 컨트롤러를 만들 필요 없이 간단하게 활용할 수 있습니다. 첫 번째 인수는 URI, 두 번째 인수는 뷰 이름이며, 세 번째 인수(optional)로 뷰에 전달할 데이터를 배열로 줄 수 있습니다.

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 파라미터를 사용할 때, `view`, `data`, `status`, `headers` 파라미터는 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 확인

`route:list` Artisan 명령어로 애플리케이션에 정의된 모든 라우트를 한눈에 확인할 수 있습니다.

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 미들웨어는 `route:list` 출력에 표시되지 않습니다. 명령에 `-v` 옵션을 추가하면 라우트 미들웨어 및 미들웨어 그룹 이름을 볼 수 있습니다.

```shell
php artisan route:list -v

# 미들웨어 그룹 확장 보기...
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 보고 싶다면 다음과 같이 `--path` 옵션을 사용할 수 있습니다.

```shell
php artisan route:list --path=api
```

또한, 서드파티 패키지에서 정의한 라우트를 숨기려면 `--except-vendor` 옵션을 사용할 수 있습니다.

```shell
php artisan route:list --except-vendor
```

반대로, 서드파티 패키지에서 정의한 라우트만 표시하려면 `--only-vendor` 옵션을 사용할 수 있습니다.

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우팅 커스터마이징

기본적으로 애플리케이션의 라우트는 `bootstrap/app.php` 파일에서 설정 및 로드됩니다.

```php
<?php

use Illuminate\Foundation\Application;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )->create();
```

하지만 애플리케이션 라우트의 일부만 별도의 파일에서 관리하고 싶다면, `withRouting` 메서드에 `then` 클로저를 전달할 수 있습니다. 이 클로저에서 추가로 필요한 라우트를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up',
    then: function () {
        Route::middleware('api')
            ->prefix('webhooks')
            ->name('webhooks.')
            ->group(base_path('routes/webhooks.php'));
    },
)
```

또는, 완전히 커스텀하게 라우트 등록을 직접 제어하려면 `using` 클로저를 `withRouting` 메서드에 전달할 수 있습니다. 이 경우 프레임워크는 기본 HTTP 라우트를 등록하지 않으며, 모든 라우트 등록을 직접 처리해야 합니다.

```php
use Illuminate\Support\Facades\Route;

->withRouting(
    commands: __DIR__.'/../routes/console.php',
    using: function () {
        Route::middleware('api')
            ->prefix('api')
            ->group(base_path('routes/api.php'));

        Route::middleware('web')
            ->group(base_path('routes/web.php'));
    },
)
```

<a name="route-parameters"></a>
## 라우트 파라미터 (Route Parameters)

<a name="required-parameters"></a>
### 필수 파라미터

때로는 URI의 일부를 캡처해야 할 때가 있습니다. 예를 들어, URL에서 사용자 ID를 추출하는 경우입니다. 이럴 때는 라우트 파라미터를 정의하면 됩니다.

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요에 따라 여러 개의 라우트 파라미터를 정의할 수 있습니다.

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 파라미터는 항상 `{}` 중괄호로 감싸며, 알파벳 문자로 구성해야 합니다. 파라미터 이름에 밑줄(`_`)도 사용할 수 있습니다. 라우트 파라미터는 정의된 순서에 따라 라우트 콜백이나 컨트롤러에 주입되므로, 함수 인자의 이름과 무관하게 순서가 중요합니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입

라우트에 의존성을 주입하고 싶을 때는, 의존성 인자 다음에 라우트 파라미터를 나열해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 파라미터

어떤 경우에는 URI에 항상 파라미터가 있을 필요가 없습니다. 파라미터 이름 뒤에 `?`를 추가하면 해당 파라미터를 선택적으로 만들 수 있습니다. 이때 라우트 콜백의 해당 인자에 기본값을 지정해야 합니다.

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규 표현식 제약

`where` 메서드를 사용해 라우트 파라미터의 형식을 정규 표현식으로 제약할 수 있습니다. 파라미터 이름과 제한할 정규식을 전달합니다.

```php
Route::get('/user/{name}', function (string $name) {
    // ...
})->where('name', '[A-Za-z]+');

Route::get('/user/{id}', function (string $id) {
    // ...
})->where('id', '[0-9]+');

Route::get('/user/{id}/{name}', function (string $id, string $name) {
    // ...
})->where(['id' => '[0-9]+', 'name' => '[a-z]+']);
```

자주 사용하는 정규식 패턴은 헬퍼 메서드로 더 간단히 추가할 수 있습니다.

```php
Route::get('/user/{id}/{name}', function (string $id, string $name) {
    // ...
})->whereNumber('id')->whereAlpha('name');

Route::get('/user/{name}', function (string $name) {
    // ...
})->whereAlphaNumeric('name');

Route::get('/user/{id}', function (string $id) {
    // ...
})->whereUuid('id');

Route::get('/user/{id}', function (string $id) {
    // ...
})->whereUlid('id');

Route::get('/category/{category}', function (string $category) {
    // ...
})->whereIn('category', ['movie', 'song', 'painting']);

Route::get('/category/{category}', function (string $category) {
    // ...
})->whereIn('category', CategoryEnum::cases());
```

만약 들어오는 요청이 라우트 패턴 제약에 맞지 않을 경우, 404 HTTP 응답을 반환합니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약

라우트 파라미터가 항상 특정 정규식으로 제한되길 원한다면, `pattern` 메서드를 사용할 수 있습니다. 이 패턴은 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의해야 합니다.

```php
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::pattern('id', '[0-9]+');
}
```

한번 패턴이 정의되면, 해당 파라미터 이름을 사용하는 모든 라우트에 자동으로 적용됩니다.

```php
Route::get('/user/{id}', function (string $id) {
    // {id}가 숫자일 때만 실행됨...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시(`/`) 허용

Laravel 라우팅 컴포넌트는 라우트 파라미터 값에 `/`를 제외한 모든 문자를 허용합니다. `/`가 파라미터 값의 일부여야 하는 경우, `where` 조건의 정규식으로 명시적으로 허용해야 합니다.

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 마지막 라우트 세그먼트에만 사용할 수 있습니다.

<a name="named-routes"></a>
## 이름이 지정된 라우트 (Named Routes)

이름이 지정된 라우트는 특정 라우트에 대해 URL이나 리다이렉트를 편리하게 생성할 수 있는 기능을 제공합니다. 라우트 정의 시 `name` 메서드를 체이닝하여 이름을 지정할 수 있습니다.

```php
Route::get('/user/profile', function () {
    // ...
})->name('profile');
```

컨트롤러 액션에도 라우트 이름을 지정할 수 있습니다.

```php
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!WARNING]
> 라우트 이름은 항상 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 이름이 지정된 라우트로 URL 생성

라우트에 이름을 지정한 후에는, Laravel의 `route` 또는 `redirect` 헬퍼 함수를 이용해 해당 라우트의 URL이나 리다이렉트를 생성할 수 있습니다.

```php
// URL 생성...
$url = route('profile');

// 리다이렉트 생성...
return redirect()->route('profile');

return to_route('profile');
```

만약 라우트에 파라미터가 있다면, `route` 함수의 두 번째 인수로 파라미터를 배열로 전달할 수 있습니다. 전달된 파라미터는 URL 내 올바른 위치에 자동으로 삽입됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

추가적으로 배열에 더 많은 파라미터를 전달하면, 이들은 자동으로 쿼리 스트링으로 URL에 추가됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// http://example.com/user/1/profile?photos=yes
```

> [!NOTE]
> 예를 들어 현재 로케일(locale)처럼, URL 파라미터에 대한 기본값을 전역적으로 지정하고 싶다면 [URL::defaults 메서드](/docs/12.x/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 검사

현재 요청이 특정 이름의 라우트에 매핑되었는지 확인하려면, Route 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어, 라우트 미들웨어에서 현재 라우트 이름을 확인할 수 있습니다.

```php
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Handle an incoming request.
 *
 * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
 */
public function handle(Request $request, Closure $next): Response
{
    if ($request->route()->named('profile')) {
        // ...
    }

    return $next($request);
}
```

<a name="route-groups"></a>
## 라우트 그룹 (Route Groups)

라우트 그룹을 사용하면, 미들웨어와 같은 라우트 속성을 여러 라우트에 반복해서 지정하지 않고 한 번에 적용할 수 있습니다.

중첩 그룹의 경우, 부모 그룹과 속성이 지능적으로 병합됩니다. 미들웨어와 `where` 제약은 병합되고, 네임스페이스와 접두사, 이름 접두사는 올바르게 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

[미들웨어](/docs/12.x/middleware)를 그룹 내 모든 라우트에 적용하려면, 그룹 정의 전에 `middleware` 메서드를 사용합니다. 미들웨어는 배열에 나열된 순서대로 실행됩니다.

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first & second 미들웨어 사용됨...
    });

    Route::get('/user/profile', function () {
        // first & second 미들웨어 사용됨...
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러

여러 라우트가 동일한 [컨트롤러](/docs/12.x/controllers)를 사용할 경우, `controller` 메서드로 그룹 내 모든 라우트에 공통 컨트롤러를 지정할 수 있습니다. 이후 각 라우트 정의에서는 호출할 컨트롤러 메서드 이름만 명시하면 됩니다.

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹은 서브도메인 기반 라우팅에도 사용할 수 있습니다. 서브도메인에도 라우트 파라미터를 할당할 수 있어, 서브도메인 일부를 캡처하여 라우트나 컨트롤러에서 사용할 수 있습니다. `domain` 메서드로 서브도메인을 지정합니다.

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

> [!WARNING]
> 서브도메인 라우트가 정상적으로 동작하려면, 루트 도메인 라우트보다 먼저 서브도메인 라우트를 등록해야 합니다. 그렇지 않으면 동일한 URI 경로가 루트 도메인 라우트에 의해 덮어써질 수 있습니다.

<a name="route-group-prefixes"></a>
### 라우트 접두사

`prefix` 메서드를 사용하면 그룹 내 모든 라우트의 URI에 특정 접두사를 추가할 수 있습니다. 예를 들어, 그룹 내 모든 라우트의 URI를 `admin`으로 시작하도록 만들 수 있습니다.

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL과 매칭
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두사

`name` 메서드를 사용하면 그룹 내 모든 라우트 이름에 지정한 문자열을 접두사로 붙일 수 있습니다. 예를 들어, 그룹 내 라우트 이름에 `admin`을 접두사로 추가하고자 할 때, 접두사 끝에 반드시 `.`를 붙여주세요.

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // 라우트 이름은 "admin.users"로 할당...
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

라우트나 컨트롤러 액션에 모델 ID를 주입받을 때, 해당 ID에 대응하는 모델을 데이터베이스에서 직접 쿼리하는 일이 많습니다. Laravel의 라우트 모델 바인딩 기능을 사용하면, 라우트에 모델 인스턴스를 자동으로 주입시켜주는 편리한 기능을 제공합니다. 예를 들어, 사용자 ID 대신 해당 ID에 해당하는 `User` 모델 전체를 직접 주입할 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩

Laravel은 라우트나 컨트롤러 액션에서 타입힌트된 변수명이 URI의 세그먼트 이름과 일치할 경우, Eloquent 모델을 자동으로 해결해줍니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

여기서 `$user` 변수는 `App\Models\User` Eloquent 모델로 타입힌트되어 있고, `{user}` URI 세그먼트와 변수명이 일치하므로, Laravel은 요청 URI에 해당하는 ID로 모델 인스턴스를 찾아 자동으로 주입합니다. 일치하는 모델이 데이터베이스에 없으면 404 HTTP 응답이 자동으로 반환됩니다.

물론, 컨트롤러 메서드에서도 암묵적 바인딩을 사용할 수 있습니다. 마찬가지로, `{user}` URI 세그먼트와 타입힌트된 `$user` 변수가 연결됩니다.

```php
use App\Http\Controllers\UserController;
use App\Models\User;

// 라우트 정의...
Route::get('/users/{user}', [UserController::class, 'show']);

// 컨트롤러 메서드 정의...
public function show(User $user)
{
    return view('user.profile', ['user' => $user]);
}
```

<a name="implicit-soft-deleted-models"></a>
#### 소프트 삭제된 모델

기본적으로, 암묵적 모델 바인딩은 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 하지만 라우트에 `withTrashed` 메서드를 추가하면 소프트 삭제된 모델도 조회할 수 있습니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 키 커스터마이징

때로는 모델을 식별할 때 `id` 컬럼 이외의 컬럼을 사용하고 싶을 수 있습니다. 이 경우 라우트 파라미터 정의에서 컬럼명을 명시하면 됩니다.

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

특정 모델 클래스에서 바인딩을 항상 특정 컬럼(예: slug)으로 하려면, Eloquent 모델의 `getRouteKeyName` 메서드를 오버라이드하세요.

```php
/**
 * Get the route key for the model.
 */
public function getRouteKeyName(): string
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
#### 커스텀 키와 범위 지정

여러 Eloquent 모델을 하나의 라우트에 암묵적으로 바인딩할 때, 두 번째 모델이 첫 번째 모델의 하위 관계(자식) 이어야 할 때가 있습니다. 예를 들어, 특정 사용자의 블로그 게시물을 slug로 조회하는 라우트가 있을 수 있습니다.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

커스텀 키로 중첩 라우트 파라미터를 정의할 때, Laravel은 부모 모델(User)의 연관관계 컨벤션을 자동으로 유추해 자식 모델(Post)을 조회 범위로 제한합니다. 위 예시의 경우 User 모델에 `posts`(파라미터 이름의 복수형)라는 관계가 있다고 간주합니다.

커스텀 키 없이도 자식 모델을 범위로 제한하고 싶다면, 라우트 정의 시 `scopeBindings` 메서드를 체이닝하면 됩니다.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

혹은 라우트 그룹 전체에 범위 지정 바인딩을 적용할 수도 있습니다.

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로, 라우트에 `withoutScopedBindings` 메서드를 사용해 범위 제한을 적용하지 않을 수도 있습니다.

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 바인딩 모델이 없을 때 동작 커스터마이즈

보통, 암묵적으로 바인딩된 모델을 데이터베이스에서 찾지 못하면 404 HTTP 응답이 발생합니다. 하지만 라우트 정의 시 `missing` 메서드를 통해 해당 동작을 커스터마이즈할 수 있습니다. `missing` 메서드는 클로저를 받아 바인딩 대상 모델이 없을 때 이를 실행합니다.

```php
use App\Http\Controllers\LocationsController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::get('/locations/{location:slug}', [LocationsController::class, 'show'])
    ->name('locations.view')
    ->missing(function (Request $request) {
        return Redirect::route('locations.index');
    });
```

<a name="implicit-enum-binding"></a>
### 암묵적 Enum 바인딩

PHP 8.1에서 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php) 기능이 도입되었습니다. Laravel은 [string-backed Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 라우트에서 타입힌트로 지정하면, 해당 라우트 세그먼트가 Enum의 유효 값일 때에만 해당 라우트를 실행합니다. 그렇지 않으면 404 HTTP 응답이 자동으로 반환됩니다.

다음 Enum을 예시로 살펴봅니다.

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

아래와 같이, `{category}` 세그먼트가 `fruits` 또는 `people`일 때만 라우트가 실행되고, 그렇지 않으면 404가 반환됩니다.

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩

반드시 Laravel의 암묵적(컨벤션 기반) 모델 바인딩만을 사용할 필요는 없습니다. 명시적으로 라우트 파라미터가 어떤 모델과 매핑되는지도 지정할 수 있습니다. 명시적 바인딩을 등록하려면, 라우터의 `model` 메서드로 파라미터에 사용할 클래스를 지정하세요. 일반적으로 `AppServiceProvider` 클래스의 `boot` 메서드에서 이 작업을 수행합니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::model('user', User::class);
}
```

이제, `{user}` 파라미터가 포함된 라우트를 정의하면:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

모든 `{user}` 파라미터는 `App\Models\User` 모델에 바인딩되어, 해당 ID의 User 인스턴스가 자동으로 주입됩니다. 예를 들어 `users/1` 요청 시, ID가 1인 User 인스턴스가 주입됩니다.

만약 일치하는 모델이 없으면 자동으로 404 HTTP 응답을 반환합니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 해석 로직 커스터마이즈

바인딩 해석 논리를 직접 정의하고 싶다면, `Route::bind` 메서드를 사용할 수 있습니다. 이 메서드에 넘기는 클로저는 URI 세그먼트 값을 받고, 바인딩할 객체를 반환해야 합니다. 역시 `AppServiceProvider` 클래스의 `boot` 메서드에서 설정합니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::bind('user', function (string $value) {
        return User::where('name', $value)->firstOrFail();
    });
}
```

또는, Eloquent 모델에서 `resolveRouteBinding` 메서드를 오버라이드할 수도 있습니다. 이 메서드는 URI 세그먼트 값을 받아, 바인딩할 객체를 반환해야 합니다.

```php
/**
 * Retrieve the model for a bound value.
 *
 * @param  mixed  $value
 * @param  string|null  $field
 * @return \Illuminate\Database\Eloquent\Model|null
 */
public function resolveRouteBinding($value, $field = null)
{
    return $this->where('name', $value)->firstOrFail();
}
```

라우트가 [암묵적 바인딩 범위](#implicit-model-binding-scoping)를 사용할 때는, `resolveChildRouteBinding` 메서드가 자식 바인딩 로직에 사용됩니다.

```php
/**
 * Retrieve the child model for a bound value.
 *
 * @param  string  $childType
 * @param  mixed  $value
 * @param  string|null  $field
 * @return \Illuminate\Database\Eloquent\Model|null
 */
public function resolveChildRouteBinding($childType, $value, $field)
{
    return parent::resolveChildRouteBinding($childType, $value, $field);
}
```

<a name="fallback-routes"></a>
## 폴백 라우트 (Fallback Routes)

`Route::fallback` 메서드를 사용하면, 들어오는 요청이 다른 어떤 라우트와도 매칭되지 않을 때 실행되는 라우트를 정의할 수 있습니다. 일반적으로 매칭되지 않은 요청은 예외 핸들러를 통해 "404" 페이지가 표시되지만, `routes/web.php`에 폴백 라우트를 정의하면 `web` 미들웨어 그룹의 모든 미들웨어가 해당 라우트에도 적용됩니다. 필요에 따라 추가 미들웨어도 부착할 수 있습니다.

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 속도 제한 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 속도 제한자 정의

Laravel은 손쉽게 사용하고 확장 가능한 속도 제한(rate limiting) 서비스를 제공합니다. 각 라우트나 라우트 그룹에 할당할 속도 제한자(rate limiter) 구성을 정의하면 됩니다.

속도 제한자는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 정의할 수 있습니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
}
```

속도 제한자는 `RateLimiter` 파사드의 `for` 메서드를 사용해 정의합니다. 이 메서드는 제한자 이름과, 해당 제한자가 적용될 라우트에 사용할 제한 구성 리밋(객체)을 반환하는 클로저를 인수로 받습니다. 제한 구성은 `Illuminate\Cache\RateLimiting\Limit` 클래스의 인스턴스이며, "빌더" 메서드로 손쉽게 다양한 방식을 지정할 수 있습니다. 제한자 이름은 자유롭게 지정할 수 있습니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });
}
```

요청이 지정된 제한을 초과하면, Laravel이 자동으로 429 HTTP 상태 코드로 응답합니다. 제한을 초과했을 때 반환할 응답을 직접 정의하고 싶으면, `response` 메서드로 응답을 지정할 수 있습니다.

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

속도 제한자 콜백에서 들어오는 HTTP 요청 인스턴스를 받기 때문에, 요청 정보나 인증된 사용자에 따라 제한 정책을 동적으로 지정할 수 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perHour(10);
});
```

<a name="segmenting-rate-limits"></a>
#### 제한 세분화

경우에 따라 IP 주소 등 임의의 값별로 제한 구분을 하고 싶은 경우가 있습니다. 예를 들어 한 라우트에 대해 IP별로 분당 100회 제한을 적용하려면, `by` 메서드를 사용합니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

또 다른 예시로, 인증 사용자는 분당 100회, 비인증 사용자는 IP별로 분당 10회로 나누어 제한할 수도 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 복수 제한 정책

필요에 따라 한 제한자 내에서 여러 제한 정책을 배열로 반환할 수 있습니다. 배열 내 순서대로 각 제한이 적용됩니다.

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

동일한 `by` 값으로 여러 속도 제한을 둘 경우, 각 `by` 값이 고유해야 합니다. 가장 간단한 방법은 `by`에 전달하는 값을 접두사 등으로 구분하는 것입니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="response-base-rate-limiting"></a>
#### 응답 기반 속도 제한

들어오는 요청 수로만 제한할 필요 없이, 응답 결과(특정 HTTP 상태 코드 등)에 따라 제한을 적용하고 싶을 때는 `after` 메서드를 사용할 수 있습니다. `after` 메서드는 응답 객체를 받아, 제한에 카운트할지(true) 무시할지(false) 결정하는 클로저를 받습니다.

이 방법은, 연속된 404 응답 제한(열거형 공격 방지) 또는 검증 실패로 인한 재시도는 카운트하지 않고, 정상 종료된 경우에만 제한을 적용하는 등 다양한 보안 정책에 활용할 수 있습니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Symfony\Component\HttpFoundation\Response;

RateLimiter::for('resource-not-found', function (Request $request) {
    return Limit::perMinute(10)
        ->by($request->user()?->id ?: $request->ip())
        ->after(function (Response $response) {
            // 404 응답만 카운트해서 enumeration 시도 방지
            return $response->status() === 404;
        });
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 속도 제한자 부착

속도 제한자는 `throttle` [미들웨어](/docs/12.x/middleware)로 라우트나 라우트 그룹에 적용할 수 있습니다. 사용할 제한자 이름을 `throttle` 미들웨어의 인수로 전달하세요.

```php
Route::middleware(['throttle:uploads'])->group(function () {
    Route::post('/audio', function () {
        // ...
    });

    Route::post('/video', function () {
        // ...
    });
});
```

<a name="throttling-with-redis"></a>
#### Redis 기반 속도 제한

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스로 매핑됩니다. 만약 Redis를 캐시 드라이버로 사용하는 경우, Laravel이 Redis 기반 속도 제한을 사용하도록 하려면, 애플리케이션의 `bootstrap/app.php`에서 `throttleWithRedis` 메서드를 사용하세요. 이 메서드는 `throttle` 미들웨어를 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 미들웨어에 매핑합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 폼 메서드 위조 (Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 메서드를 지원하지 않습니다. 따라서 HTML 폼에서 이런 메서드를 사용하는 라우트로 요청을 전송하려면, 숨겨진 `_method` 필드를 추가해야 합니다. 이 필드의 값이 HTTP 요청 메서드로 사용됩니다.

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

보다 편하게 하려면, [Blade 디렉티브](/docs/12.x/blade)인 `@method`를 사용해 `_method` 입력 필드를 생성할 수 있습니다.

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 정보 접근 (Accessing the Current Route)

현재 요청을 처리하는 라우트 정보를 얻으려면 `Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

라우터 및 라우트 클래스의 전체 API 문서는 [Route 파사드의 내부 클래스](https://api.laravel.com/docs/12.x/Illuminate/Routing/Router.html) 및 [Route 인스턴스](https://api.laravel.com/docs/12.x/Illuminate/Routing/Route.html) 문서를 참고하세요.

<a name="cors"></a>
## 교차 출처 리소스 공유(CORS) (Cross-Origin Resource Sharing, CORS)

Laravel은 CORS `OPTIONS` HTTP 요청에 자동으로 응답할 수 있습니다. 이 요청들은 앱의 글로벌 미들웨어 스택에 포함된 `HandleCors` [미들웨어](/docs/12.x/middleware)에 의해 자동 처리됩니다.

애플리케이션별로 CORS 설정 값을 커스터마이즈해야 할 때는, `config:publish` Artisan 명령어로 `cors` 설정 파일을 퍼블리시할 수 있습니다.

```shell
php artisan config:publish cors
```

이 명령어는 애플리케이션의 `config` 디렉토리에 `cors.php` 설정 파일을 생성합니다.

> [!NOTE]
> CORS 및 CORS 헤더에 대한 추가 정보는 [MDN 웹 문서의 CORS 가이드](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

애플리케이션을 실제로 서비스할 때는 Laravel의 라우트 캐시 기능을 반드시 사용하는 것이 좋습니다. 라우트 캐싱을 활용하면 모든 라우트를 불러오는 속도가 크게 단축됩니다. 라우트 캐시를 생성하려면 `route:cache` Artisan 명령어를 실행하세요.

```shell
php artisan route:cache
```

이 명령을 실행한 후에는 모든 요청에서 캐시된 라우트 파일이 로드됩니다. 새로운 라우트를 추가하면 반드시 라우트 캐시를 다시 생성해야 하므로, 일반적으로 배포 시에만 이 명령어를 실행해야 합니다.

라우트 캐시는 `route:clear` 명령어로 삭제할 수 있습니다.

```shell
php artisan route:clear
```
