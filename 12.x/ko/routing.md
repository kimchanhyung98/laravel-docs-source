# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리다이렉트 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록 조회](#listing-your-routes)
    - [라우팅 커스터마이징](#routing-customization)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [옵션 파라미터](#parameters-optional-parameters)
    - [정규식 제약 조건](#parameters-regular-expression-constraints)
- [이름 있는 라우트](#named-routes)
- [라우트 그룹](#route-groups)
    - [미들웨어](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [서브도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 접두사](#route-group-prefixes)
    - [라우트 이름 접두사](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암묵적 바인딩](#implicit-binding)
    - [Enum 암묵적 바인딩](#implicit-enum-binding)
    - [명시적 바인딩](#explicit-binding)
- [폴백 라우트](#fallback-routes)
- [요청 제한(Rate Limiting)](#rate-limiting)
    - [요청 제한자 정의](#defining-rate-limiters)
    - [라우트에 요청 제한자 연결](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근](#accessing-the-current-route)
- [교차 출처 리소스 공유(CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

Laravel의 가장 기본적인 라우트는 URI와 클로저(closure)를 받아, 복잡한 라우팅 설정 파일 없이도 간단하고 직관적으로 라우트와 동작을 정의할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일

Laravel의 모든 라우트는 `routes` 디렉터리에 위치한 라우트 파일들에서 정의합니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 지정된 설정에 따라 Laravel이 자동으로 로드합니다. `routes/web.php` 파일은 웹 인터페이스용 라우트를 정의합니다. 이 라우트들은 `web` [미들웨어 그룹](/docs/12.x/middleware#laravels-default-middleware-groups)에 할당되어, 세션 상태 관리나 CSRF 보호 같은 기능을 제공합니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에 라우트를 정의하는 것으로 시작합니다. `routes/web.php`에 정의된 라우트는 해당 URL을 브라우저에 입력하여 접근할 수 있습니다. 예를 들어 다음 라우트는 `http://example.com/user`로 접근할 수 있습니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트

애플리케이션이 상태를 저장하지 않는 API도 제공하는 경우, `install:api` Artisan 명령어로 API 라우팅 기능을 활성화할 수 있습니다.

```shell
php artisan install:api
```

`install:api` 명령어는 [Laravel Sanctum](/docs/12.x/sanctum)을 설치하여, 외부 API 소비자, SPA, 모바일 애플리케이션 등에서 사용할 수 있는 간단하고 강력한 API 토큰 인증 방식(guard)을 제공합니다. 또한 `routes/api.php` 파일을 생성합니다.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

`routes/api.php`의 라우트는 상태를 저장하지 않으며, `api` [미들웨어 그룹](/docs/12.x/middleware#laravels-default-middleware-groups)에 할당됩니다. 또한 이 파일의 모든 라우트에는 `/api` URI 접두사가 자동으로 적용되므로, 매번 직접 지정할 필요가 없습니다. 필요하다면 애플리케이션의 `bootstrap/app.php` 파일을 수정해 접두사를 변경할 수 있습니다.

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

여러 HTTP 메서드에 응답하는 라우트가 필요하다면 `match` 메서드를 사용할 수 있고, 모든 HTTP 메서드에 반응하는 라우트를 만들고 싶다면 `any` 메서드를 사용할 수 있습니다.

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일한 URI를 공유하는 여러 라우트를 정의할 때는, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트를 `any`, `match`, `redirect` 메서드보다 먼저 정의하세요. 그래야 요청이 올바른 라우트와 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백에서 필요한 의존성을 타입 힌트로 지정하면, Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입해 줍니다. 예를 들어, `Illuminate\Http\Request` 클래스에 타입 힌트를 지정하면 현재 HTTP 요청 객체가 자동으로 콜백에 주입됩니다.

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에서 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 라우트로 향하는 모든 HTML 폼에는 반드시 CSRF 토큰 필드를 포함해야 합니다. 그렇지 않으면 요청이 거부됩니다. 자세한 내용은 [CSRF 문서](/docs/12.x/csrf)를 참고하세요.

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리다이렉트 라우트

다른 URI로 리다이렉션하는 라우트를 정의하려면 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 간단한 리다이렉션을 위해 전체 라우트나 컨트롤러를 별도로 작성하지 않아도 되는 편리한 단축키 역할을 합니다.

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 옵션 세 번째 인자를 통해 상태 코드를 커스터마이징할 수 있습니다.

```php
Route::redirect('/here', '/there', 301);
```

또한, `Route::permanentRedirect` 메서드를 사용해 `301` 상태 코드를 반환할 수도 있습니다.

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리다이렉트 라우트에서 라우트 파라미터를 사용할 때, `destination`과 `status` 파라미터는 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트

[뷰](/docs/12.x/views)만 반환하는 라우트가 필요한 경우, `Route::view` 메서드를 사용할 수 있습니다. 이 메서드는 단순히 뷰만 반환하는 라우트 또는 컨트롤러를 별도로 만들 필요 없이 간단히 정의할 수 있도록 도와줍니다. `view` 메서드는 첫 번째 인수로 URI, 두 번째 인수로 뷰 이름을 받고, 세 번째 옵션 인수로 뷰에 전달할 데이터를 배열로 지정할 수 있습니다.

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 파라미터를 사용할 때, `view`, `data`, `status`, `headers` 파라미터는 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 조회

`route:list` Artisan 명령어를 사용하면 애플리케이션에 정의된 모든 라우트의 개요를 쉽게 확인할 수 있습니다.

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 미들웨어는 `route:list` 출력 결과에 표시되지 않습니다. 그러나 `-v` 옵션을 추가하면 라우트 미들웨어와 미들웨어 그룹 이름을 표시할 수 있습니다.

```shell
php artisan route:list -v

# 미들웨어 그룹까지 확장하여 표시...
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 보고 싶으면 아래와 같이 경로 옵션을 사용할 수 있습니다.

```shell
php artisan route:list --path=api
```

서드파티 패키지에서 정의한 라우트를 숨기려면 `--except-vendor` 옵션을 제공하면 됩니다.

```shell
php artisan route:list --except-vendor
```

반대로, 서드파티 패키지에서 정의한 라우트만 표시하려면 `--only-vendor` 옵션을 사용합니다.

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

하지만 애플리케이션 라우트의 일부만을 담는 새로운 파일을 정의하고 싶을 수도 있습니다. 이럴 때는 `withRouting` 메서드에 `then` 클로저를 전달할 수 있습니다. 이 클로저 내부에서 필요한 추가 라우트를 자유롭게 등록할 수 있습니다.

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

또는 라우트 등록을 완전히 수동으로 제어하고 싶다면, `withRouting` 메서드에 `using` 클로저를 전달할 수 있습니다. 이 인자를 사용하면 프레임워크가 HTTP 라우트를 등록하지 않고, 직접 모든 라우트를 등록해야 합니다.

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

라우트에서 URI의 일부 구간을 변수로 받아야 하는 경우가 있습니다. 예를 들어 사용자 ID를 URL에서 받아오려면 다음과 같이 라우트 파라미터를 정의할 수 있습니다.

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요하다면 라우트 파라미터를 여러 개 정의할 수도 있습니다.

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 파라미터는 항상 중괄호 `{}`로 감싸며, 알파벳으로만 구성해야 합니다. 파라미터 이름에 언더스코어(`_`)도 사용할 수 있습니다. 라우트 파라미터는 등록된 순서대로(이름과 무관하게) 콜백이나 컨트롤러에 주입됩니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입

서비스 컨테이너가 자동으로 의존성을 주입해주길 원하는 경우, 라우트 파라미터를 의존성 뒤에 나열해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 옵션 파라미터

때로는 URI에 항상 존재하지 않는 라우트 파라미터가 필요할 수 있습니다. 파라미터 이름 뒤에 `?` 를 붙이면 옵션 파라미터가 되며, 해당 변수에 기본값을 반드시 지정해주어야 합니다.

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

`where` 메서드를 사용해 라우트 파라미터의 형식을 정규식으로 제한할 수 있습니다. `where` 메서드는 파라미터 이름과, 그 파라미터에 적용할 정규식을 인자로 받습니다.

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

자주 쓰는 정규 표현식에 대해선 편리하게 사용할 수 있는 헬퍼 메서드도 제공됩니다.

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

들어오는 요청이 라우트 패턴의 제약 조건을 충족하지 않으면, 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약 조건

특정 라우트 파라미터에 항상 동일한 정규식을 적용하고 싶다면, `pattern` 메서드를 사용할 수 있습니다. 해당 내용은 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의합니다.

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

한 번 패턴을 정의하면, 해당 파라미터 이름이 사용되는 모든 라우트에 자동으로 적용됩니다.

```php
Route::get('/user/{id}', function (string $id) {
    // {id}가 숫자일 때만 동작...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시(/) 허용

Laravel 라우팅 컴포넌트는 슬래시(`/`)를 제외한 모든 문자를 기본적으로 라우트 파라미터 값에 허용합니다. 만약 슬래시(`/`)까지 허용하려면 `where` 조건에 `.*`같은 정규식을 명시적으로 지정해야 합니다.

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시(`/`)는 반드시 마지막 라우트 세그먼트에서만 허용됩니다.

<a name="named-routes"></a>
## 이름 있는 라우트 (Named Routes)

이름 있는 라우트는 특정 라우트에 대해 URL이나 리다이렉션을 편리하게 생성할 수 있도록 도와줍니다. 라우트 정의 시 `name` 메서드를 체이닝 해서 이름을 지정할 수 있습니다.

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
> 라우트 이름은 반드시 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 이름 있는 라우트로 URL 생성

라우트에 이름을 지정하면, Laravel의 `route`와 `redirect` 헬퍼 함수를 사용해 해당 이름으로 URL이나 리다이렉션을 손쉽게 생성할 수 있습니다.

```php
// URL 생성
$url = route('profile');

// 리다이렉션 생성
return redirect()->route('profile');

return to_route('profile');
```

라우트 이름에 파라미터가 있다면, `route` 함수의 두 번째 인자로 파라미터 배열을 전달할 수 있습니다. 전달된 값이 URL의 해당 위치에 자동으로 삽입됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

배열에 추가적인 파라미터를 전달하면, 해당 키/값 쌍이 URL 쿼리스트링에 자동으로 추가됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// /user/1/profile?photos=yes
```

> [!NOTE]
> URL 파라미터의 요청 전체에 대해 기본값을 설정하고 싶을 때([예: 현재 로케일]), [URL::defaults 메서드](/docs/12.x/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 확인

현재 요청이 지정한 이름의 라우트로 라우팅 되었는지 확인하려면, Route 인스턴스에서 `named` 메서드를 사용할 수 있습니다. 예를 들어, 미들웨어에서 현재 라우트 이름을 확인할 수 있습니다.

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

라우트 그룹을 사용하면 미들웨어 같은 공통 라우트 속성을 개별 라우트에 일일이 정의하지 않고, 한 번에 여러 라우트에 공유할 수 있습니다.

중첩된 그룹에서는 부모 그룹의 속성과 합쳐지도록 ("지능적으로 병합") 동작합니다. 미들웨어와 `where` 조건은 병합되고, 이름과 접두사는 뒤에 붙습니다. 네임스페이스 구분자와 URI 접두사 슬래시는 자동으로 알맞게 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

[미들웨어](/docs/12.x/middleware)를 그룹 내 모든 라우트에 지정하려면, 그룹 정의 전에 `middleware` 메서드를 사용합니다. 배열에 나열된 순서대로 미들웨어가 실행됩니다.

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first & second 미들웨어를 사용합니다...
    });

    Route::get('/user/profile', function () {
        // first & second 미들웨어를 사용합니다...
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러

여러 라우트가 동일한 [컨트롤러](/docs/12.x/controllers)를 사용하는 경우, 그룹에 `controller` 메서드를 사용해 공통 컨트롤러를 지정할 수 있습니다. 이후 개별 라우트에서는 컨트롤러 메서드 이름만 지정하면 됩니다.

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹은 서브도메인 라우팅에도 사용할 수 있습니다. 서브도메인 역시 라우트 파라미터처럼 지정할 수 있어, 해당 부분을 라우트 또는 컨트롤러에서 사용할 수 있습니다. 서브도메인은 `domain` 메서드를 사용해 그룹에 지정합니다.

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

> [!WARNING]
> 서브도메인 라우트가 올바르게 동작하려면, 루트 도메인 라우트보다 먼저 등록해야 합니다. 그렇지 않으면 루트 도메인 라우트가 서브도메인 라우트를 덮어쓸 수 있습니다.

<a name="route-group-prefixes"></a>
### 라우트 접두사

`prefix` 메서드를 사용해 그룹 내 모든 라우트의 URI에 특정 접두사를 붙일 수 있습니다. 예를 들어, 모든 라우트에 `admin` 접두사를 붙이고 싶다면 다음과 같이 작성합니다.

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL과 매칭
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두사

`name` 메서드를 사용하면 그룹 내 모든 라우트의 이름에 문자열 접두사를 붙일 수 있습니다. 예를 들어, 그룹 내 모든 라우트 이름 앞에 `admin` 접두사를 붙이고 싶다면, 접미사로 `.`을 붙여 준비해야 합니다.

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // 라우트 이름이 "admin.users"로 할당됨...
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

라우트나 컨트롤러 액션에 모델 ID를 주입받는 경우, 해당 ID에 해당하는 모델을 데이터베이스에서 조회해야 합니다. Laravel 라우트 모델 바인딩은 해당 모델 인스턴스를 라우트에 자동으로 주입해주는 편리한 방법을 제공합니다. 예를 들어, 사용자 ID를 인수로 받는 대신 ID에 해당하는 전체 `User` 모델 인스턴스를 바로 주입받을 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩

Eloquent 모델을 타입 힌트로 명시하고, 변수 이름이 라우트 세그먼트 이름과 일치하면 Laravel이 해당 모델 인스턴스를 자동으로 주입해줍니다. 예시:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

`$user` 변수가 `App\Models\User` Eloquent 모델로 타입 힌트되어 있고, 변수명이 `{user}` URI 세그먼트와 일치하기 때문에, Laravel은 요청 URI에서 가져온 값과 일치하는 ID를 가진 모델 인스턴스를 자동으로 주입합니다. 데이터베이스에서 일치하는 모델 인스턴스를 찾지 못하면 404 HTTP 응답이 자동으로 반환됩니다.

물론, 컨트롤러 메서드에서도 암묵적 바인딩을 사용할 수 있습니다. 역시 `{user}` URI 세그먼트와 컨트롤러의 `$user` 변수명이 일치함을 유의하세요.

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
#### 소프트 삭제 모델(Soft Deleted Models)

기본적으로 암묵적 모델 바인딩은 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 그러나 라우트 정의에 `withTrashed` 메서드를 체이닝 하면, 소프트 삭제된 모델도 조회할 수 있습니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 커스터마이징

때로는 Eloquent 모델을 조회할 때 `id`가 아닌 다른 컬럼을 사용하고 싶을 수 있습니다. 이 경우, 라우트 파라미터 정의에서 해당 컬럼을 명시할 수 있습니다.

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

특정 모델 클래스의 조회 컬럼을 항상 `id` 대신 사용하고 싶다면, Eloquent 모델에서 `getRouteKeyName` 메서드를 오버라이드 하면 됩니다.

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
#### 커스텀 키 및 범위(Scoping)

하나의 라우트 정의에 여러 Eloquent 모델을 암묵적으로 바인딩할 경우, 두 번째 모델이 첫 번째 모델의 하위(자식)가 되도록 범위를 설정하고 싶을 수 있습니다. 예를 들어, 특정 사용자의 블로그 포스트를 slug로 조회하려면 다음과 같이 작성합니다.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

커스텀 키로 중첩된 라우트 파라미터를 암묵적 바인딩으로 사용할 경우, Laravel은 관례적으로 부모 모델과의 관계 이름을 추론해 자식 모델의 쿼리에 범위를 적용합니다. 위 예시에서는 `User` 모델이 `posts`라는 연관관계를 가진 것으로 간주합니다.

커스텀 키 없이도 바인딩 범위(scoping)를 적용하고 싶다면, 라우트 정의에 `scopeBindings` 메서드를 호출하면 됩니다.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

혹은 라우트 그룹 전체에 범위 바인딩을 적용할 수도 있습니다.

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로, 바인딩 범위를 적용하지 않으려면 `withoutScopedBindings` 메서드를 호출할 수 있습니다.

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 바인딩 모델이 없을 때 동작 커스터마이징

일반적으로, 암묵적 바인딩된 모델을 찾지 못하면 404 HTTP 응답이 반환됩니다. 하지만 `missing` 메서드로 이 동작을 커스터마이즈할 수 있습니다. `missing` 메서드는 모델을 찾지 못했을 때 실행될 클로저를 받습니다.

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
### Enum 암묵적 바인딩

PHP 8.1에서 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php) 지원이 도입되면서 Laravel에서도 [문자열 기반 Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 라우트에 타입 힌트로 지정하면, 해당 라우트 세그먼트 값이 Enum 값과 일치하는 경우에만 라우트가 실행됩니다. 그렇지 않으면 404 HTTP 응답이 반환됩니다. 예를 들어 다음과 같은 Enum이 있다고 가정합니다.

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

다음과 같이 라우트를 정의하면, `{category}` 세그먼트가 `fruits`나 `people`일 때만 라우트가 실행되고, 아니라면 404가 반환됩니다.

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩

Laravel의 암묵적 방식뿐 아니라, 명시적으로 라우트 파라미터와 모델을 직접 연결할 수도 있습니다. 명시적 바인딩을 등록하려면 라우터의 `model` 메서드로 파라미터와 모델 클래스를 지정합니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 정의합니다.

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

이후 `{user}` 파라미터가 포함된 라우트를 정의합니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

이렇게 하면 `{user}` 파라미터에 해당하는 값으로 데이터베이스에서 `User` 모델 인스턴스가 찾아져 주입됩니다. 예를 들어 `users/1` 요청이 오면, ID가 1인 `User` 인스턴스가 주입됩니다.

일치하는 모델 인스턴스를 찾지 못하면 404 HTTP 응답이 자동으로 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 조회 로직의 커스터마이징

모델 바인딩의 조회 로직을 직접 정의하고 싶으면, `Route::bind` 메서드를 사용할 수 있습니다. 이 메서드는 URI 세그먼트의 값을 인자로 받아, 라우트에 주입할 클래스 인스턴스를 반환해야 합니다. 역시 `AppServiceProvider`의 `boot`에서 작성합니다.

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

또는 Eloquent 모델의 `resolveRouteBinding` 메서드를 오버라이드할 수도 있습니다. 이 메서드는 URI 세그먼트 값을 받아 라우트에 주입할 인스턴스를 반환해야 합니다.

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

라우트가 [암묵적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용하는 경우, 부모 모델의 자식 바인딩은 `resolveChildRouteBinding` 메서드가 호출됩니다.

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

`Route::fallback` 메서드를 사용하면, 다른 어떤 라우트와도 매칭되지 않는 경우 실행되는 라우트를 정의할 수 있습니다. 보통 처리되지 않은 요청은 애플리케이션의 예외 핸들러를 통해 "404" 페이지를 렌더링합니다. 하지만 `routes/web.php` 파일에서 `fallback` 라우트를 정의하면, `web` 미들웨어 그룹의 모든 미들웨어가 이 라우트에도 적용됩니다. 필요에 따라 추가 미들웨어를 적용할 수도 있습니다.

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 요청 제한 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 요청 제한자 정의

Laravel은 강력하고 유연한 요청 제한(Rate Limiting) 서비스를 제공하여, 특정 라우트나 라우트 그룹의 트래픽을 제한할 수 있습니다. 먼저, 애플리케이션에 맞는 요청 제한자 구성을 정의해야 합니다.

요청 제한자는 `App\Providers\AppServiceProvider`의 `boot` 메서드 내에서 정의할 수 있습니다.

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

요청 제한자는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다. 이 메서드는 제한자 이름과, 해당 제한자가 적용될 라우트에 사용할 제한 구성(클로저가 반환)을 인자로 받습니다. 제한 구성은 `Illuminate\Cache\RateLimiting\Limit` 클래스 인스턴스를 사용하며, 다양한 "빌더" 메서드를 제공해 제한을 더 쉽게 지정할 수 있습니다. 이름에는 원하는 문자열을 쓸 수 있습니다.

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

입력된 요청이 제한 수치를 넘을 경우, Laravel에서 자동으로 429 HTTP 상태 코드가 포함된 응답을 반환합니다. 제한에 도달했을 때 반환할 응답을 직접 지정하고 싶다면 `response` 메서드를 사용할 수 있습니다.

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

요청 제한 콜백에서는 전달된 HTTP 요청 객체를 바탕으로 제한 값을 동적으로 계산할 수도 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perHour(10);
});
```

<a name="segmenting-rate-limits"></a>
#### 제한 세분화(Segmenting)

경우에 따라 제한 값을 임의의 값에 따라 세분화하고 싶을 수 있습니다. 예를 들어, 각 IP 주소별로 분당 100회까지만 허용하려면 `by` 메서드를 사용할 수 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

또 다른 예시로, 인증된 사용자는 ID별로 분당 100회, 비회원(게스트)은 IP별로 분당 10회로 제한할 수도 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 여러 제한 규칙(Multiple)

필요하다면 하나의 제한자 구성에서 제한 객체의 배열을 반환할 수도 있습니다. 배열에 정의된 각 제한이 해당 라우트에 적용됩니다(앞에 정의한 것부터 순서대로 평가됨).

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

같은 `by` 값으로 여러 제한 규칙을 적용한다면, 각 `by` 값이 고유해야 합니다. 가장 쉬운 방법은 `by` 메서드에 넘길 값을 접두사로 구분하는 것입니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 요청 제한자 연결

요청 제한자는 [throttle 미들웨어](/docs/12.x/middleware)를 통해 라우트나 라우트 그룹에 할당할 수 있습니다. 이 미들웨어는 제한자 이름을 인자로 받습니다.

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
#### Redis를 활용한 요청 제한

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스로 매핑됩니다. 하지만 애플리케이션의 캐시 드라이버로 Redis를 사용한다면, 요청 제한을 Redis로 관리하도록 Laravel에 지시할 수 있습니다. 이를 위해 `bootstrap/app.php`에서 `throttleWithRedis` 메서드를 사용하면 됩니다. 이 메서드는 `throttle` 미들웨어를 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis`로 매핑합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 폼 메서드 스푸핑 (Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 직접 지원하지 않습니다. 따라서 폼에서 이러한 HTTP 메서드가 필요한 라우트로 요청을 보낼 때는, 폼에 숨겨진 `_method` 필드를 추가해야 합니다. 이 필드의 값이 실제 HTTP 요청 메서드로 사용됩니다.

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

더 편리하게, [Blade 지시어](/docs/12.x/blade)인 `@method`를 사용해 `_method` 인풋 필드를 만들 수 있습니다.

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 접근 (Accessing the Current Route)

현재 요청을 처리하는 라우트의 정보를 확인하려면 `Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route 인스턴스
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

라우터 및 라우트 클래스에서 사용할 수 있는 전체 메서드를 확인하려면, [Route 파사드의 기반 클래스](https://api.laravel.com/docs/12.x/Illuminate/Routing/Router.html)와 [Route 인스턴스](https://api.laravel.com/docs/12.x/Illuminate/Routing/Route.html) API 문서를 참고하세요.

<a name="cors"></a>
## 교차 출처 리소스 공유 (CORS; Cross-Origin Resource Sharing)

Laravel은 CORS의 `OPTIONS` HTTP 요청에 대해, 여러분이 구성한 값으로 자동 응답할 수 있습니다. `OPTIONS` 요청은 전역 미들웨어 스택에 자동으로 포함되어 있는 `HandleCors` [미들웨어](/docs/12.x/middleware)에 의해 자동 처리됩니다.

때때로 애플리케이션에 맞게 CORS 설정 값을 직접 커스터마이징해야 하는 경우가 있습니다. 그럴 때는 `config:publish` Artisan 명령어로 `cors` 설정 파일을 퍼블리시할 수 있습니다.

```shell
php artisan config:publish cors
```

이 명령어를 실행하면 `config` 디렉터리에 `cors.php` 설정 파일이 생성됩니다.

> [!NOTE]
> CORS 및 CORS 헤더의 자세한 내용은 [MDN의 웹 문서](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

프로덕션 환경에 애플리케이션을 배포할 때는, Laravel의 라우트 캐시를 활용하는 것이 좋습니다. 라우트 캐싱을 사용하면, 애플리케이션의 모든 라우트 등록 시간이 대폭 단축됩니다. 라우트 캐시를 생성하려면 `route:cache` Artisan 명령어를 실행하세요.

```shell
php artisan route:cache
```

이 명령어를 실행한 후에는, 캐시된 라우트 파일이 모든 요청에서 로드됩니다. 새로운 라우트를 추가했다면 반드시 라우트 캐시를 새로 생성해야 합니다. 이러한 이유로, 라우트 캐시는 프로젝트 배포 시에만 실행하는 것이 좋습니다.

라우트 캐시는 `route:clear` 명령어로 삭제할 수 있습니다.

```shell
php artisan route:clear
```
