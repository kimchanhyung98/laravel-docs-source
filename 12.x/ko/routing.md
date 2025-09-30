# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리다이렉트 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 나열하기](#listing-your-routes)
    - [라우팅 커스터마이즈](#routing-customization)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [선택적 파라미터](#parameters-optional-parameters)
    - [정규식 제약 조건](#parameters-regular-expression-constraints)
- [이름이 지정된 라우트](#named-routes)
- [라우트 그룹](#route-groups)
    - [미들웨어](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [서브도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 프리픽스](#route-group-prefixes)
    - [라우트 이름 프리픽스](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암묵적 바인딩](#implicit-binding)
    - [암묵적 Enum 바인딩](#implicit-enum-binding)
    - [명시적 바인딩](#explicit-binding)
- [폴백 라우트](#fallback-routes)
- [요청 제한(Rate Limiting)](#rate-limiting)
    - [요청 제한자 정의하기](#defining-rate-limiters)
    - [라우트에 요청 제한자 적용하기](#attaching-rate-limiters-to-routes)
- [양식 메소드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근하기](#accessing-the-current-route)
- [크로스 오리진 리소스 공유(CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

가장 기본적인 Laravel 라우트는 URI와 클로저(익명함수)를 받아들여, 복잡하지 않은 라우팅 설정 파일 없이도 매우 간단하고 직관적으로 라우트와 동작을 정의할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일

모든 Laravel 라우트는 `routes` 디렉터리에 위치한 라우트 파일에서 정의합니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 설정된 구성에 따라 Laravel이 자동으로 로드합니다. `routes/web.php` 파일은 웹 인터페이스와 관련된 라우트를 정의합니다. 이 라우트들은 `web` [미들웨어 그룹](/docs/12.x/middleware#laravels-default-middleware-groups)에 할당되어, 세션 상태 관리나 CSRF 보호와 같은 기능을 제공합니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에서 라우트를 정의하는 것으로 시작합니다. `routes/web.php`에 정의된 라우트는 해당 라우트의 URL을 브라우저에 입력해 접근할 수 있습니다. 예를 들어, 아래 라우트는 브라우저에서 `http://example.com/user`로 접근할 수 있습니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트

애플리케이션에서 상태를 유지하지 않는 API도 제공하려면, `install:api` Artisan 명령어를 사용해 API 라우팅을 활성화할 수 있습니다.

```shell
php artisan install:api
```

`install:api` 명령어는 [Laravel Sanctum](/docs/12.x/sanctum)을 설치합니다. Sanctum은 타사 API 소비자나 SPA, 또는 모바일 애플리케이션을 인증할 때 사용할 수 있는 강력하고 간단한 API 토큰 인증 가드를 제공합니다. 또한, 이 명령어는 `routes/api.php` 파일을 생성합니다.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

`routes/api.php`의 라우트는 상태를 유지하지 않는 방식이 적용되며, `api` [미들웨어 그룹](/docs/12.x/middleware#laravels-default-middleware-groups)에 할당됩니다. 또한 이러한 라우트에는 `/api` URI 프리픽스가 자동으로 적용되므로 파일 내 모든 라우트에 직접 프리픽스를 추가할 필요가 없습니다. 프리픽스를 변경하려면 애플리케이션의 `bootstrap/app.php` 파일을 수정하면 됩니다.

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메서드

라우터는 모든 HTTP 메서드(VERB)에 응답하는 라우트를 등록할 수 있습니다.

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

여러 HTTP 메서드에 응답하는 라우트를 등록해야 하는 경우 `match` 메서드를 사용할 수 있습니다. 또는, 모든 HTTP 메서드에 응답하는 라우트는 `any` 메서드를 사용해 등록할 수 있습니다.

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일한 URI를 가진 여러 라우트를 정의할 때는, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트를 `any`, `match`, `redirect` 메서드를 사용하는 라우트보다 먼저 정의해야 합니다. 이렇게 해야 들어오는 요청을 올바른 라우트와 정확히 매칭할 수 있습니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백 시그니처에서 필요한 의존성을 타입힌트하면, Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 해석해 콜백에 주입해줍니다. 예를 들어, `Illuminate\Http\Request` 클래스를 타입힌트 하면 현재 HTTP 요청 객체가 자동으로 라우트 콜백에 주입됩니다.

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, 또는 `DELETE` 라우트로 전달되는 모든 HTML 폼에는 CSRF 토큰 필드를 반드시 포함해야 합니다. 그렇지 않으면 요청이 거부됩니다. CSRF 보호에 대해 더 자세한 내용은 [CSRF 문서](/docs/12.x/csrf)를 참조하세요.

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리다이렉트 라우트

다른 URI로 리다이렉트하는 라우트를 정의하려면 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 간단한 리다이렉트를 위해 전체 라우트나 컨트롤러를 별도로 정의하지 않아도 됩니다.

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 선택적 세 번째 인수로 상태 코드를 지정할 수도 있습니다.

```php
Route::redirect('/here', '/there', 301);
```

또는 `Route::permanentRedirect` 메서드를 사용해 `301` 상태 코드를 반환할 수 있습니다.

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리다이렉트 라우트에서 라우트 파라미터를 사용할 때, `destination`과 `status` 파라미터는 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트

라우트가 [뷰](/docs/12.x/views)만 반환해야 한다면 `Route::view` 메서드를 사용할 수 있습니다. 이 메서드는 간단하게 뷰만 반환해야 하는 경우 전체 라우트나 컨트롤러를 정의하지 않고도 사용할 수 있습니다. 첫 번째 인수로 URI, 두 번째 인수로 뷰 이름, 선택적으로 세 번째 인수로 뷰에 전달할 데이터를 배열로 넘길 수 있습니다.

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 파라미터를 사용할 때 `view`, `data`, `status`, `headers` 파라미터는 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 나열하기

`route:list` Artisan 명령어를 사용하면 애플리케이션에 정의된 모든 라우트의 개요를 쉽게 확인할 수 있습니다.

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 미들웨어는 `route:list` 출력에 표시되지 않습니다. 그러나 명령에 `-v` 옵션을 추가하여 라우트 미들웨어 및 미들웨어 그룹 이름을 표시할 수 있습니다.

```shell
php artisan route:list -v

# 미들웨어 그룹 확장...
php artisan route:list -vv
```

또한, Laravel에게 특정 URI로 시작하는 라우트만 표시하도록 할 수도 있습니다.

```shell
php artisan route:list --path=api
```

`route:list` 명령어 실행 시 `--except-vendor` 옵션을 제공하면, 서드파티 패키지에서 정의한 라우트를 숨길 수 있습니다.

```shell
php artisan route:list --except-vendor
```

반대로, `--only-vendor` 옵션을 제공하면, 서드파티 패키지에서 정의한 라우트만 표시할 수도 있습니다.

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우팅 커스터마이즈

기본적으로 애플리케이션의 라우트는 `bootstrap/app.php` 파일에서 구성 및 로드됩니다.

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

하지만, 애플리케이션의 특정 라우트 집합을 별도의 파일에 정의해야 할 때도 있습니다. 이 경우 `withRouting` 메서드의 `then` 클로저에 추가 라우트 등록 로직을 작성할 수 있습니다.

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

또는, `using` 클로저를 사용해 라우트 등록 전체를 직접 제어할 수도 있습니다. 이 인수를 전달하면 프레임워크에서 HTTP 라우트를 등록하지 않으므로 모든 라우트를 직접 수동으로 등록해야 합니다.

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

종종 라우트에서 URI의 특정 부분을 파라미터로 받아야 할 때가 있습니다. 예를 들어, URL에서 사용자의 ID를 받아와야 할 때 라우트 파라미터를 다음과 같이 정의할 수 있습니다.

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요한 만큼 많은 라우트 파라미터를 정의할 수도 있습니다.

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 파라미터는 항상 `{}` 중괄호로 감싸며, 알파벳 문자로 구성해야 합니다. 파라미터 이름에 언더스코어(`_`)도 사용할 수 있습니다. 파라미터 값은 순서대로 라우트 콜백이나 컨트롤러로 주입됩니다. 즉, 콜백 또는 컨트롤러의 인수 이름과는 무관하게 순서로 매칭됩니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입

라우트에서 Laravel 서비스 컨테이너가 자동으로 주입해줬으면 하는 의존성이 있다면, 라우트 파라미터를 의존성 인수 다음에 나열해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 파라미터

때때로 라우트 파라미터가 항상 없는 경우도 있습니다. 그런 경우 파라미터 이름 뒤에 `?`를 붙여 선택적으로 만들고, 해당 케이스의 변수를 기본값으로 지정하면 됩니다.

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규식 제약 조건

`where` 메서드를 사용해 라우트 파라미터의 형식을 정규식으로 제한할 수 있습니다. `where` 메서드는 제한할 파라미터 이름과 정규식을 인수로 받습니다.

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

자주 사용하는 정규식 패턴은 헬퍼 메서드를 통해 좀 더 간단히 제약을 추가할 수 있습니다.

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

들어온 요청이 라우트 패턴 제약 조건에 맞지 않을 경우 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약 조건

특정 라우트 파라미터에 항상 동일한 정규식 제약을 적용하려면 `pattern` 메서드를 사용할 수 있습니다. 이런 패턴은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의해야 합니다.

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

패턴을 정의하면, 해당 파라미터 이름을 사용하는 모든 라우트에 자동으로 적용됩니다.

```php
Route::get('/user/{id}', function (string $id) {
    // {id}가 숫자일 때만 실행...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시(/) 허용

Laravel 라우팅 컴포넌트는 기본적으로 라우트 파라미터에 `/`를 제외한 모든 문자가 올 수 있도록 허용합니다. `/` 문자가 포함된 값을 허용하려면 `where` 조건 정규식에 명시적으로 허용해야 합니다.

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 라우트의 마지막 세그먼트에서만 지원됩니다.

<a name="named-routes"></a>
## 이름이 지정된 라우트 (Named Routes)

이름이 지정된 라우트는 특정 라우트에 대한 URL 생성이나 리다이렉트를 편리하게 만들 수 있도록 해줍니다. 라우트를 정의할 때 `name` 메서드를 체이닝하여 라우트의 이름을 지정합니다.

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
> 라우트 이름은 반드시 유일해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 이름이 지정된 라우트로 URL 생성

라우트에 이름을 지정하면 Laravel의 `route` 및 `redirect` 헬퍼 함수를 이용해 해당 라우트의 URL 또는 리다이렉트를 생성할 수 있습니다.

```php
// URL 생성...
$url = route('profile');

// 리다이렉트 생성...
return redirect()->route('profile');

return to_route('profile');
```

이름이 지정된 라우트에 파라미터가 있다면, `route` 함수의 두 번째 인수로 파라미터 배열을 전달하면 됩니다. 지정한 파라미터는 알맞은 위치에 자동으로 들어가 URL이 생성됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

배열로 추가 파라미터를 전달하면 해당 key/value 쌍이 쿼리스트링으로 URL에 추가됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// /user/1/profile?photos=yes
```

> [!NOTE]
> 예를 들어, 현재 로케일과 같은 URL 파라미터에 요청 범위의 기본값을 지정하고 싶을 수도 있습니다. 이 경우 [URL::defaults 메서드](/docs/12.x/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 검사

현재 요청이 특정 이름의 라우트로 매칭되었는지 확인하고 싶다면, Route 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어, 라우트 미들웨어 내에서 현재 라우트 이름을 확인할 수 있습니다.

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

라우트 그룹을 사용하면 미들웨어 등 라우트 속성을 여러 라우트에 공유할 수 있습니다. 개별 라우트마다 속성을 반복 정의하지 않아도 됩니다.

중첩 그룹의 경우, 부모 그룹과 속성이 '지능적으로 병합'됩니다. 미들웨어와 `where` 조건은 병합되고, 이름과 프리픽스는 덧붙여집니다. 네임스페이스 구분자나 URI 프리픽스의 슬래시는 자동으로 적절히 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

[미들웨어](/docs/12.x/middleware)를 그룹 내 모든 라우트에 적용하려면 `middleware` 메서드를 그룹 정의 전에 사용하세요. 미들웨어는 배열에 나열된 순서대로 실행됩니다.

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first & second 미들웨어 적용...
    });

    Route::get('/user/profile', function () {
        // first & second 미들웨어 적용...
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러

그룹 내 라우트가 모두 동일한 [컨트롤러](/docs/12.x/controllers)를 사용할 때는, `controller` 메서드로 공통 컨트롤러를 지정할 수 있습니다. 라우트 정의 시에는 호출할 컨트롤러 메서드만 지정하면 됩니다.

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹은 서브도메인 라우팅을 처리할 때도 사용할 수 있습니다. 서브도메인도 라우트 파라미터로 지정할 수 있어, 라우트나 컨트롤러 내에서 활용할 수 있습니다. 서브도메인은 그룹 정의 전에 `domain` 메서드로 지정하면 됩니다.

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

> [!WARNING]
> 서브도메인 라우트가 정상적으로 동작하려면, 반드시 루트 도메인 라우트보다 먼저 등록해야 합니다. 그렇지 않으면 루트 도메인 라우트가 동일한 URI 경로에서 서브도메인 라우트를 덮어쓸 수 있습니다.

<a name="route-group-prefixes"></a>
### 라우트 프리픽스

`prefix` 메서드는 그룹 내 모든 라우트의 URI에 지정한 프리픽스를 붙일 때 사용합니다. 예를 들어, 그룹 내 모든 라우트 URI에 `admin`을 프리픽스로 붙일 수 있습니다.

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL과 매칭
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 프리픽스

`name` 메서드는 그룹 내 모든 라우트의 이름에 지정한 문자열을 프리픽스로 붙입니다. 예를 들어, 그룹 내 모든 라우트 이름에 `admin`을 프리픽스로 붙일 수 있습니다. 지정한 문자열이 라우트 이름에 그대로 앞에 붙으므로, 보통 접미사로 마침표(`.`)를 포함합니다.

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // "admin.users" 이름이 할당...
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

라우트나 컨트롤러 액션에서 모델의 ID를 주입받아 데이터베이스에서 모델을 조회하는 경우가 많습니다. 라우트 모델 바인딩 기능을 이용하면 해당 ID에 해당하는 모델 인스턴스를 라우트에 자동으로 주입할 수 있습니다. 즉, 사용자의 ID 대신, 바로 해당하는 `User` 모델 인스턴스를 주입받을 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩

라우트나 컨트롤러 액션에서 타입힌트된 변수명과 라우트 세그먼트 이름이 일치한다면, Laravel은 Eloquent 모델을 자동으로 주입합니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

`$user` 변수가 `App\Models\User` Eloquent 모델 타입이고, 변수명이 `{user}` URI 세그먼트와 일치하면, URL에 해당하는 ID를 가진 모델 인스턴스가 자동으로 주입됩니다. 일치하는 모델 인스턴스가 데이터베이스에 없으면 404 HTTP 응답이 자동으로 반환됩니다.

컨트롤러 메서드를 사용할 때도 동일하게 동작합니다. 역시 `{user}` URI 세그먼트와 컨트롤러의 `$user` 변수가 일치해야 합니다.

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
#### 소프트 삭제 모델

기본적으로 암묵적 모델 바인딩은 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 그러나 `withTrashed` 메서드를 라우트에 체이닝하여 소프트 삭제된 모델도 조회하도록 지정할 수 있습니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 키(Custom Key) 커스터마이즈

어떤 경우에는 Eloquent 모델에서 `id` 이외의 컬럼으로 조회하고 싶을 수 있습니다. 이 경우 라우트 파라미터 정의에 컬럼명을 다음과 같이 지정할 수 있습니다.

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

특정 모델 클래스의 기본 바인딩 컬럼을 항상 변경하고 싶다면, Eloquent 모델의 `getRouteKeyName` 메서드를 오버라이드하면 됩니다.

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
#### 커스텀 키와 스코핑

하나의 라우트에서 여러 Eloquent 모델을 암묵적으로 바인딩할 때, 두 번째 모델이 반드시 첫 번째 모델(부모)의 하위임을 스코프 처리하고 싶을 수 있습니다. 예를 들어, 특정 사용자의 게시글을 슬러그로 조회할 때 다음과 같이 작성할 수 있습니다.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

이처럼 중첩 라우트 파라미터에서 커스텀 키를 사용하면, Laravel은 루트 부모 모델의 연관관계명을 추측해 자동으로 쿼리의 스코프를 제한합니다. 위 예제에서는 `User` 모델이 `posts`(복수형 파라미터명)의 연관관계를 가진 것으로 간주해 이를 통해 `Post`를 조회합니다.

커스텀 키를 사용하지 않아도 "자식" 바인딩의 스코프 지정이 필요하다면, 라우트 정의 시 `scopeBindings` 메서드를 호출하십시오.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는, 라우트 그룹 전체에 스코프 바인딩을 적용할 수도 있습니다.

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로, `withoutScopedBindings` 메서드를 호출해 바인딩 스코프를 명시적으로 비활성화할 수도 있습니다.

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 모델을 찾지 못했을 때 동작 커스터마이즈

암묵적 모델 바인딩에서 일반적으로 모델을 찾지 못하면 404 HTTP 응답이 반환됩니다. 그러나 라우트 정의 시 `missing` 메서드에 클로저를 넘기면, 모델을 찾지 못했을 때 이 클로저가 호출되어 원하는 동작을 수행할 수 있습니다.

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

PHP 8.1에서는 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php) 기능이 도입되었습니다. 이를 보완하기 위해, Laravel에서는 [문자열 기반 Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 라우트에 타입힌트할 수 있으며, 해당 세그먼트가 Enum 값에 해당하는 경우에만 라우트가 실행됩니다. 일치하지 않으면 자동으로 404 HTTP 응답이 반환됩니다. 예를 들어, 다음과 같이 Enum이 정의되어 있다면,

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

아래 라우트는 `{category}` 값이 `fruits`, `people`일 때만 동작합니다. 그 외의 값은 404가 반환됩니다.

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩

Laravel의 암묵적, 컨벤션 기반 모델 바인딩을 반드시 사용할 필요는 없습니다. 라우트 파라미터와 모델이 어떻게 매칭되는지 명시적으로 정의할 수도 있습니다. 이를 위해 라우터의 `model` 메서드로 파라미터별 클래스를 지정합니다. 명시적 모델 바인딩은 `AppServiceProvider` 클래스의 `boot` 메서드 초반에 정의해야 합니다.

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

그 다음, `{user}` 파라미터를 포함한 라우트를 정의합니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

모든 `{user}` 파라미터가 `App\Models\User` 모델로 바인딩되었으므로, 해당 클래스 인스턴스가 라우트에 주입됩니다. 예를 들어 `users/1`로 요청하면 데이터베이스에서 ID가 1인 `User` 인스턴스가 주입됩니다.

일치하는 모델 인스턴스가 없으면 404 HTTP 응답이 자동으로 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 로직 커스터마이즈

모델 바인딩 해석 로직을 직접 정의하고 싶다면, `Route::bind` 메서드를 사용할 수 있습니다. 이 메서드에 넘기는 클로저는 URI 세그먼트 값을 받아, 라우트에 주입할 클래스 인스턴스를 반환해야 합니다. 이 커스터마이즈 역시 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이루어져야 합니다.

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

또한, Eloquent 모델의 `resolveRouteBinding` 메서드를 오버라이드해도 됩니다. 이 메서드는 URI 세그먼트 값을 받아, 라우트에 주입할 인스턴스를 반환해야 합니다.

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

[암묵적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용하는 라우트의 경우, 자식 바인딩 해석에선 `resolveChildRouteBinding` 메서드가 사용됩니다.

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

`Route::fallback` 메서드를 사용해, 들어온 요청과 일치하는 라우트가 없을 때 실행되는 라우트를 정의할 수 있습니다. 일반적으로 매칭되지 않은 요청은 예외 핸들러를 통해 "404" 페이지가 자동으로 렌더링됩니다. 하지만 `fallback` 라우트가 `routes/web.php`에 정의되어 있으므로, `web` 미들웨어 그룹이 모두 적용됩니다. 필요에 따라 추가 미들웨어도 자유롭게 적용할 수 있습니다.

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 요청 제한 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 요청 제한자 정의하기

Laravel은 라우트별 요청 횟수를 제한할 수 있는 강력하고 커스터마이즈 가능한 요청 제한(Rate Limiting) 서비스를 내장하고 있습니다. 먼저, 애플리케이션 요구사항에 맞는 요청 제한 구성(rate limiter configuration)을 정의해야 합니다.

요청 제한자는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의합니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
protected function boot(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
}
```

요청 제한자는 `RateLimiter` 파사드의 `for` 메서드를 사용해 정의합니다. 이 메서드는 제한자 이름, 그리고 해당 제한자를 적용할 라우트에 사용할 제한 설정(limit configuration)을 반환하는 클로저를 받습니다. 제한 설정은 `Illuminate\Cache\RateLimiting\Limit` 클래스의 인스턴스로, 여러 빌더 메서드를 통해 손쉽게 요청 제한을 정의할 수 있습니다. 제한자 이름은 아무 문자열이나 사용할 수 있습니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
protected function boot(): void
{
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });
}
```

들어온 요청이 제한수를 초과하면, Laravel이 자동으로 429 HTTP 상태 코드와 함께 응답을 반환합니다. 요청 제한 시 반환할 응답을 직접 정의하고 싶다면, `response` 메서드를 사용할 수 있습니다.

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

요청 제한자 클로저는 들어온 HTTP 요청 인스턴스를 전달받으므로, 요청 내용이나 인증 사용자에 따라 동적으로 제한을 설정할 수도 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perHour(10);
});
```

<a name="segmenting-rate-limits"></a>
#### 제한 기준 분할

경우에 따라 임의의 기준으로 요청 제한을 분할(세그먼트화)하고 싶을 수 있습니다. 예를 들어, 각 IP 주소별로 1분에 100회씩 라우트 접근을 허용하려면, 제한 설정시 `by` 메서드를 사용하면 됩니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

다른 예제로, 인증 사용자는 1분에 100회, 비회원(게스트)은 IP별 1분에 10회로 접근을 제한할 수도 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 여러 개의 요청 제한

필요하다면, 하나의 요청 제한자 구성에서 제한 설정 배열을 반환할 수 있습니다. 각 제한은 배열에 나열된 순서대로 라우트에 적용됩니다.

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

`by` 값이 동일한 여러 제한을 적용할 경우, 각 `by` 값이 유일하도록 만들어야 합니다. 가장 쉬운 방법은 `by` 메서드에 값을 접두어로 구분해 전달하는 것입니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="response-base-rate-limiting"></a>
#### 응답 기반 요청 제한

들어오는 요청 자체가 아니라 응답 결과를 바탕으로 요청 제한을 적용할 수도 있습니다. 이럴 때는 `after` 메서드를 사용합니다. 예를 들어, 특정 응답(유효성 검사 실패, 404 등)에 대해서만 제한을 적용하고 싶을 때 활용할 수 있습니다.

`after` 메서드는 응답 객체를 인자로 받는 클로저를 받아, 요청 제한에 포함 여부를 `true`/`false`로 반환해야 합니다. 예를 들어, 404 응답만 제한에 포함해 열거(Enumeration) 공격을 막거나, 유효성 검증 실패 시 제한 횟수를 차감하지 않도록 할 수 있습니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Symfony\Component\HttpFoundation\Response;

RateLimiter::for('resource-not-found', function (Request $request) {
    return Limit::perMinute(10)
        ->by($request->user()?->id ?: $request->ip())
        ->after(function (Response $response) {
            // 404 응답만 요청 제한에 포함...
            return $response->status() === 404;
        });
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 요청 제한자 적용하기

라우트 또는 라우트 그룹에 요청 제한자를 적용하려면, `throttle` [미들웨어](/docs/12.x/middleware)를 사용합니다. `throttle` 미들웨어에는 지정한 요청 제한자의 이름을 인수로 넘깁니다.

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
#### Redis로 요청 제한

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스에 매핑되어 있습니다. 하지만 애플리케이션의 캐시 드라이버로 Redis를 사용할 경우, 요청 제한도 Redis를 통해 관리하도록 지정하는 것이 좋습니다. 이를 위해 `bootstrap/app.php` 파일에서 `throttleWithRedis` 메서드를 사용하면 됩니다. 이 메서드는 `throttle` 미들웨어를 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 미들웨어 클래스에 매핑합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 양식 메소드 스푸핑 (Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 액션을 직접 지원하지 않습니다. 따라서, HTML 폼에서 `PUT`, `PATCH`, `DELETE` 라우트를 호출하려면 숨겨진 `_method` 필드를 폼에 추가해야 합니다. `_method` 필드에 입력한 값이 HTTP 요청 메서드로 인식됩니다.

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

편의상, [Blade 디렉티브](/docs/12.x/blade)인 `@method`를 사용해 `_method` 입력 필드를 손쉽게 만들 수 있습니다.

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 접근하기 (Accessing the Current Route)

`Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 사용해 들어온 요청을 처리 중인 라우트에 대한 정보를 얻을 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

라우터와 라우트 클래스의 모든 사용 가능한 메서드는 각각 [Route 파사드의 API 문서](https://api.laravel.com/docs/12.x/Illuminate/Routing/Router.html), [Route 인스턴스 API 문서](https://api.laravel.com/docs/12.x/Illuminate/Routing/Route.html)에서 확인할 수 있습니다.

<a name="cors"></a>
## 크로스 오리진 리소스 공유(CORS) (Cross-Origin Resource Sharing)

Laravel은 CORS `OPTIONS` HTTP 요청에 대해, 사용자가 지정한 설정 값으로 자동으로 응답할 수 있습니다. 이러한 `OPTIONS` 요청은 애플리케이션의 전역 미들웨어 스택에 기본 포함된 `HandleCors` [미들웨어](/docs/12.x/middleware)가 자동 처리합니다.

애플리케이션의 CORS 구성 값을 커스터마이즈해야 할 경우, `config:publish cors` Artisan 명령어로 `cors` 설정 파일을 퍼블리시하면 됩니다.

```shell
php artisan config:publish cors
```

이 명령어를 실행하면, 애플리케이션의 `config` 디렉터리에 `cors.php` 설정 파일이 생성됩니다.

> [!NOTE]
> CORS와 CORS 헤더에 대한 더 자세한 정보는 [MDN web documentation on CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

프로덕션 환경에 애플리케이션을 배포할 때는 라우트 캐시 기능을 활용하세요. 라우트 캐시를 사용하면 모든 애플리케이션 라우트 등록 시간이 크게 단축됩니다. 라우트 캐시를 생성하려면 `route:cache` Artisan 명령어를 실행합니다.

```shell
php artisan route:cache
```

이 명령어를 실행한 이후에는 모든 요청마다 캐시된 라우트 파일이 로드됩니다. 새로운 라우트를 추가했다면 반드시 라우트 캐시를 다시 생성해야 합니다. 따라서 실제 배포(Deploy) 과정에서만 이 명령어를 실행하는 것이 좋습니다.

라우트 캐시는 `route:clear` 명령어로 삭제할 수 있습니다.

```shell
php artisan route:clear
```
