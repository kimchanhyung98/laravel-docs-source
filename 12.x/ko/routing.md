# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리디렉션 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록 확인](#listing-your-routes)
    - [라우트 커스터마이징](#routing-customization)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [선택적 파라미터](#parameters-optional-parameters)
    - [정규 표현식 제약 조건](#parameters-regular-expression-constraints)
- [네임드 라우트](#named-routes)
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
- [요청 제한(Rate Limiting)](#rate-limiting)
    - [Rate Limiter 정의](#defining-rate-limiters)
    - [라우트에 Rate Limiter 연결](#attaching-rate-limiters-to-routes)
- [폼 메서드 변조(Form Method Spoofing)](#form-method-spoofing)
- [현재 라우트 정보 접근](#accessing-the-current-route)
- [교차 출처 리소스 공유(CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

가장 기본적인 Laravel 라우트는 URI와 클로저(익명 함수)를 받아 복잡한 라우팅 설정 없이도 아주 간단하고 직관적으로 라우트와 동작을 정의할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일

모든 Laravel 라우트는 `routes` 디렉터리에 위치한 라우트 파일에 정의됩니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 설정된 구성에 따라 Laravel이 자동으로 로드합니다. `routes/web.php` 파일은 웹 인터페이스를 위한 라우트를 정의합니다. 이 라우트들은 `web` [미들웨어 그룹](/docs/12.x/middleware#laravels-default-middleware-groups)에 할당되어 세션 상태 및 CSRF 보호와 같은 기능을 제공합니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에서 라우트 정의를 시작합니다. `routes/web.php`에 정의된 라우트는 브라우저에서 정의된 라우트의 URL에 접속하여 접근할 수 있습니다. 예를 들어, 아래와 같은 라우트는 브라우저에서 `http://example.com/user`로 접속해 접근할 수 있습니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트

애플리케이션이 비상태 API도 제공하려면 `install:api` Artisan 명령어로 API 라우팅을 활성화할 수 있습니다.

```shell
php artisan install:api
```

`install:api` 명령어는 [Laravel Sanctum](/docs/12.x/sanctum)을 설치합니다. Sanctum은 외부 API 소비자, SPA, 모바일 애플리케이션 인증에 사용할 수 있는 간단하지만 강력한 API 토큰 인증 가드를 제공합니다. 또한, `install:api` 명령어는 `routes/api.php` 파일도 생성합니다.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

`routes/api.php`의 라우트는 상태를 유지하지 않으며, `api` [미들웨어 그룹](/docs/12.x/middleware#laravels-default-middleware-groups)에 할당됩니다. 또한 `/api` URI 프리픽스(접두사)가 이 파일의 모든 라우트에 자동으로 적용되므로 별도로 직접 설정할 필요가 없습니다. 접두사를 변경하려면 애플리케이션의 `bootstrap/app.php` 파일을 수정하세요.

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메서드

라우터에서는 모든 HTTP 메서드에 응답할 수 있는 라우트를 등록할 수 있습니다.

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

여러 HTTP 메서드에 응답하는 라우트가 필요하다면 `match` 메서드를 사용할 수 있습니다. 또는, 모든 HTTP 메서드에 응답하는 라우트를 `any` 메서드로 등록할 수도 있습니다.

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일한 URI를 사용하는 여러 라우트를 정의할 때, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드 라우트를 `any`, `match`, `redirect` 메서드보다 먼저 정의해야 요청이 올바른 라우트와 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입(Dependency Injection)

라우트의 콜백 시그니처에 필요한 의존성을 타입힌트로 지정하면, Laravel [서비스 컨테이너](/docs/12.x/container)가 해당 의존성을 자동으로 해결하여 콜백 함수에 주입합니다. 예를 들어, `Illuminate\Http\Request` 클래스를 타입힌트로 지정하면 현재 HTTP 요청이 콜백에 자동 주입됩니다.

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 라우트로 연결되는 모든 HTML 폼에는 반드시 CSRF 토큰 필드를 포함해야 합니다. 그렇지 않으면 해당 요청은 거부됩니다. 자세한 내용은 [CSRF 보호 문서](/docs/12.x/csrf)를 참고하세요.

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리디렉션 라우트

다른 URI로 리디렉션하는 라우트를 정의할 때는 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 단순한 리디렉션을 위해 전체 라우트나 컨트롤러를 만들 필요 없이 편리한 단축 방법을 제공합니다.

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 세 번째 매개변수로 상태 코드를 변경할 수 있습니다.

```php
Route::redirect('/here', '/there', 301);
```

또는, `Route::permanentRedirect` 메서드를 사용해 `301` 상태 코드를 반환할 수 있습니다.

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리디렉션 라우트에서 라우트 파라미터를 사용할 때 `destination`과 `status` 파라미터는 Laravel에 예약되어 있으므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트

라우트가 단순히 [뷰](/docs/12.x/views)만 반환해야 하는 경우, `Route::view` 메서드를 사용할 수 있습니다. 이 역시 단순한 뷰 반환을 위해 전체 라우트나 컨트롤러를 만들 필요 없이 사용할 수 있는 편리한 단축 방법입니다. `view` 메서드는 첫 번째 인수로 URI, 두 번째 인수로 뷰 이름을 받으며, 세 번째 인수로 뷰에 전달할 데이터를 배열로 전달할 수도 있습니다.

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 파라미터를 사용할 때 `view`, `data`, `status`, `headers` 파라미터는 Laravel에 예약되어 있으므로 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 확인

`route:list` Artisan 명령어를 사용하면 애플리케이션에 정의된 모든 라우트를 쉽게 확인할 수 있습니다.

```shell
php artisan route:list
```

기본적으로 `route:list` 출력에는 각 라우트에 할당된 미들웨어가 표시되지 않습니다. 라우트 미들웨어 및 미들웨어 그룹 이름도 함께 보려면 명령어에 `-v` 옵션을 추가하세요.

```shell
php artisan route:list -v

# 미들웨어 그룹까지 펼쳐서 보기
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 표시하려면 `--path` 옵션을 사용할 수 있습니다.

```shell
php artisan route:list --path=api
```

또한, `--except-vendor` 옵션을 사용해 서드파티 패키지에서 정의한 라우트를 숨길 수 있습니다.

```shell
php artisan route:list --except-vendor
```

반대로, `--only-vendor` 옵션으로 서드파티 패키지가 정의한 라우트만 볼 수도 있습니다.

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우트 커스터마이징

기본적으로, 애플리케이션의 라우트는 `bootstrap/app.php` 파일에서 설정되고 로드됩니다.

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

하지만 때로는 애플리케이션의 라우트 일부를 완전히 새로운 파일에 정의하고 싶을 수 있습니다. 이 경우, `withRouting` 메서드에 `then` 클로저를 전달하면 추가적인 라우트를 등록할 수 있습니다.

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

또는, `withRouting` 메서드에 `using` 클로저를 전달하면 라우트 등록을 완전히 직접 제어할 수 있습니다. 이 경우, 프레임워크가 HTTP 라우트를 자동으로 등록하지 않으므로, 모든 라우트를 직접 등록해야 합니다.

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

라우트에서 URI의 일부 구간을 파라미터로 받아야 할 때가 있습니다. 예를 들어, 사용자 ID를 URL에서 받아야 할 경우 라우트 파라미터를 사용할 수 있습니다.

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요한 만큼 라우트 파라미터를 정의할 수 있습니다.

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 파라미터는 항상 `{}` 괄호로 감싸며, 알파벳 문자로만 구성해야 합니다. 파라미터 이름에 언더스코어(`_`)도 사용할 수 있습니다. 라우트 파라미터는 정의된 순서대로 라우트 콜백/컨트롤러에 주입되므로, 변수명과 라우트 파라미터 이름이 반드시 일치할 필요는 없습니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입

라우트 콜백에서 Laravel 서비스 컨테이너가 주입해야 할 의존성이 있다면, 라우트 파라미터를 의존성 뒤에 나열하면 됩니다.

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 파라미터

때로는 라우트 파라미터가 항상 존재하지 않을 수 있습니다. 이럴 때는 파라미터 이름 뒤에 `?` 기호를 붙여 선택적으로 만듭니다. 라우트 콜백의 해당 변수에는 반드시 기본값을 지정해야 합니다.

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규 표현식 제약 조건

라우트 파라미터의 형식을 `where` 메서드로 제한할 수 있습니다. `where` 메서드는 파라미터 이름과 정규 표현식을 받아 파라미터 형식을 제한합니다.

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

자주 사용하는 정규 표현식 패턴의 경우, 헬퍼 메서드를 사용해 빠르게 패턴 제약을 추가할 수 있습니다.

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

요청이 라우트 패턴 제약에 맞지 않으면 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약 조건

특정 파라미터가 항상 정규 표현식에 의해 제한되기를 원한다면, `pattern` 메서드를 사용할 수 있습니다. 이런 패턴은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의해야 합니다.

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

패턴이 정의되면, 해당 이름의 파라미터를 사용하는 모든 라우트에 자동으로 적용됩니다.

```php
Route::get('/user/{id}', function (string $id) {
    // {id}가 숫자일 때만 실행됩니다...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시(Forward Slashes)

Laravel 라우팅은 라우트 파라미터 값에 `/` 문자를 제외한 모든 문자를 허용합니다. `/` 문자를 허용하려면 `where` 조건의 정규 표현식으로 명시적으로 허용해야 합니다.

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 마지막 라우트 세그먼트에서만 지원됩니다.

<a name="named-routes"></a>
## 네임드 라우트 (Named Routes)

네임드 라우트는 특정 라우트의 URL 또는 리디렉션을 편리하게 생성할 수 있도록 합니다. 라우트 정의 후 `name` 메서드를 체이닝하여 라우트에 이름을 부여할 수 있습니다.

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
#### 네임드 라우트 URL 생성

이름이 지정된 라우트는 `route` 및 `redirect` 헬퍼 함수로 URL이나 리디렉션을 쉽고 빠르게 생성할 수 있습니다.

```php
// URL 생성
$url = route('profile');

// 리디렉션 생성
return redirect()->route('profile');

return to_route('profile');
```

네임드 라우트에 파라미터가 필요하다면, 파라미터를 두 번째 인수로 배열로 전달할 수 있습니다. 전달된 파라미터는 생성된 URL의 올바른 위치에 자동으로 삽입됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

배열에 추가 파라미터를 전달하면, 그 값들은 자동으로 생성된 URL의 쿼리 스트링에 포함됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// /user/1/profile?photos=yes
```

> [!NOTE]
> 현재 로케일과 같은 값에 대해 URL 파라미터의 기본값을 전체 요청에 걸쳐 지정하고 싶다면 [URL::defaults 메서드](/docs/12.x/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 검사

현재 요청이 특정 네임드 라우트와 매칭되는지 확인하려면, Route 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어, 미들웨어에서 현재 라우트 이름을 확인할 수 있습니다.

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

라우트 그룹을 사용하면 여러 라우트에 대해 미들웨어와 같은 라우트 속성을 반복해서 작성하지 않고도 한번에 공유할 수 있습니다.

중첩된 그룹은 상위 그룹과 속성을 지능적으로 "병합"합니다. 미들웨어와 `where` 조건은 병합되고, 이름과 접두사는 덧붙여집니다. 네임스페이스 구분자나 URI 접두사의 슬래시는 상황에 맞게 자동으로 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

[미들웨어](/docs/12.x/middleware)를 그룹 내 모든 라우트에 할당하려면, 그룹 정의 전 `middleware` 메서드를 사용합니다. 미들웨어는 배열에 나열된 순서대로 실행됩니다.

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first & second 미들웨어 사용
    });

    Route::get('/user/profile', function () {
        // first & second 미들웨어 사용
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러

여러 라우트가 동일한 [컨트롤러](/docs/12.x/controllers)를 사용할 경우, `controller` 메서드로 그룹 내 모든 라우트의 공통 컨트롤러를 지정할 수 있습니다. 라우트를 정의할 때는 컨트롤러의 메서드 이름만 명시하면 됩니다.

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹은 서브도메인 라우팅에도 사용할 수 있습니다. 서브도메인에도 파라미터를 할당할 수 있어, 서브도메인의 일부 값을 라우트나 컨트롤러에서 사용할 수 있습니다. 서브도메인은 그룹 정의 전 `domain` 메서드로 지정합니다.

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

> [!WARNING]
> 서브도메인 라우트가 올바로 동작하려면, 루트 도메인 라우트보다 먼저 등록해야 합니다. 그래야 루트 도메인 라우트가 동일한 URI 경로의 서브도메인 라우트를 덮어쓰지 않습니다.

<a name="route-group-prefixes"></a>
### 라우트 접두사

`prefix` 메서드로 그룹 내 모든 라우트 URI에 접두사를 붙일 수 있습니다. 예를 들어, 그룹 내 모든 라우트 URI에 `admin` 접두사를 붙이고 싶을 때 사용할 수 있습니다.

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL과 매칭
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두사

`name` 메서드는 그룹 내 모든 라우트 이름에 특정 문자열을 접두사로 붙일 수 있습니다. 예를 들어, 이름에 항상 `admin.` 접두사를 붙이고 싶을 때 사용합니다. 접두사 문자열은 지정한 그대로 라우트 이름에 추가되므로, 접두사 끝에 `.`을 포함하는 것이 좋습니다.

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // 라우트 이름: "admin.users"
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

라우트나 컨트롤러 액션에서 모델 ID를 받는 경우, 해당 ID에 대응하는 모델을 데이터베이스에서 조회해야 할 때가 많습니다. 라라벨의 라우트 모델 바인딩 기능을 사용하면, 해당 모델 인스턴스를 라우트에 자동으로 주입할 수 있습니다. 즉, 사용자의 ID 대신 해당 ID와 일치하는 전체 `User` 모델 인스턴스를 바로 받을 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩

Eloquent 모델을 라우트나 컨트롤러 액션의 타입힌트 변수명과 라우트 세그먼트 이름이 일치하도록 정의하면, Laravel이 자동으로 모델 인스턴스를 주입합니다. 예시:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

여기서 `$user` 변수는 `App\Models\User` Eloquent 모델을 타입힌트하고, 변수명과 `{user}` URI 세그먼트가 일치하므로, 요청 URI에서 해당 값과 일치하는 ID를 가진 모델 인스턴스가 자동으로 주입됩니다. 일치하는 모델 인스턴스를 데이터베이스에서 찾지 못하면 자동으로 404 HTTP 응답이 반환됩니다.

컨트롤러 메서드에서도 암묵적 바인딩을 사용할 수 있습니다. 이때도 `{user}` URI 세그먼트가 컨트롤러의 `$user` 변수와 일치해야 합니다.

```php
use App\Http\Controllers\UserController;
use App\Models\User;

// 라우트 정의
Route::get('/users/{user}', [UserController::class, 'show']);

// 컨트롤러 메서드
public function show(User $user)
{
    return view('user.profile', ['user' => $user]);
}
```

<a name="implicit-soft-deleted-models"></a>
#### 소프트 삭제된 모델

암묵적 모델 바인딩에서는 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)된 모델을 기본적으로 조회하지 않습니다. 하지만, 라우트 정의에 `withTrashed` 메서드를 체이닝하면 소프트 삭제된 모델도 조회할 수 있습니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 커스터마이징

Eloquent 모델을 조회할 때 `id`가 아닌 다른 컬럼을 사용하고 싶다면 라우트 파라미터 정의에서 해당 컬럼을 지정할 수 있습니다.

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

특정 모델 클래스의 라우트 바인딩에서 항상 `id`가 아닌 다른 데이터베이스 컬럼을 사용하고 싶다면, Eloquent 모델의 `getRouteKeyName` 메서드를 오버라이드하세요.

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
#### 커스텀 키 및 스코핑

하나의 라우트 정의에서 여러 Eloquent 모델을 암묵적으로 바인딩할 때, 두 번째 모델이 반드시 이전 모델의 "자식"이 되도록 스코프를 한정할 수 있습니다. 예를 들면, 아래와 같이 특정 사용자의 블로그 포스트를 가져오는 라우트를 정의할 수 있습니다.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

커스텀 키를 사용해 중첩된 라우트 파라미터를 암묵적으로 바인딩하면, Laravel은 자동으로 부모 모델의 연관관계(기본적으로 라우트 파라미터 이름의 복수형)를 활용해 자식 모델을 조회합니다. 위의 예시에서는 `User` 모델이 `posts`라는 연관관계를 가지고 있다고 가정합니다.

커스텀 키를 제공하지 않는 경우에도, `scopeBindings` 메서드를 호출하면 "자식" 바인딩의 스코프를 지정할 수 있습니다.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또한, 전체 라우트 그룹에도 스코프 바인딩을 지정할 수 있습니다.

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로, `withoutScopedBindings` 메서드로 스코프 바인딩을 비활성화할 수 있습니다.

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 모델 미조회시 동작 커스터마이징

기본적으로 암묵적으로 바인딩된 모델을 찾지 못하면 404 HTTP 응답이 반환됩니다. 이 동작을 커스터마이즈하려면 라우트 정의 시 `missing` 메서드에 클로저를 전달하세요. 바인딩된 모델을 찾을 수 없을 때 이 클로저가 실행됩니다.

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

PHP 8.1에서는 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)이 도입되었습니다. 이를 지원하기 위해 Laravel에서는 라우트 정의에서 [문자열 기반 Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 타입힌트로 지정할 수 있습니다. 해당 라우트 세그먼트가 유효한 Enum 값일 때만 라우트가 실행되며, 그렇지 않으면 404 HTTP 응답이 자동 반환됩니다. 예시:

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

아래와 같이 라우트를 정의하면 `{category}` 세그먼트가 `fruits` 또는 `people`일 때만 해당 라우트가 실행됩니다. 그 외엔 404가 반환됩니다.

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩

Laravel의 암묵적, 관례 기반의 모델 바인딩을 꼭 사용하지 않아도 됩니다. 명시적으로 라우트 파라미터와 모델을 연결할 수도 있습니다. 명시적 바인딩을 등록하려면, 라우터의 `model` 메서드로 파라미터에 해당하는 클래스를 지정합니다. 이 코드는 `AppServiceProvider` 클래스의 `boot` 메서드 초기에 작성하세요.

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

이제 `{user}` 파라미터가 포함된 라우트를 정의할 수 있습니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

이렇게 하면, 예를 들어 `users/1` 요청 시 데이터베이스에서 ID가 1인 `User` 인스턴스가 주입됩니다. 모델을 찾지 못하면 404가 자동으로 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 해석 로직 커스터마이징

직접 바인딩 해석 로직을 정의하려면 `Route::bind` 메서드를 사용할 수 있습니다. 클로저에는 URI 세그먼트 값이 전달되며, 라우트에 주입할 인스턴스를 반환해야 합니다. 이 코드 역시 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에 작성합니다.

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

또는, Eloquent 모델의 `resolveRouteBinding` 메서드를 오버라이드할 수도 있습니다. 이 메서드는 URI 값이 인자로 전달되며, 라우트에 주입할 인스턴스를 반환해야 합니다.

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

라우트가 [암묵적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용하는 경우, `resolveChildRouteBinding` 메서드를 사용해 자식 바인딩 처리 로직을 구현할 수 있습니다.

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

`Route::fallback` 메서드를 사용하면, 다른 어떤 라우트와도 매칭되지 않는 요청이 들어왔을 때 실행할 라우트를 정의할 수 있습니다. 처리되지 않은 요청은 보통 애플리케이션의 예외 핸들러에 의해 "404" 페이지로 렌더링됩니다. 하지만, `fallback` 라우트는 보통 `routes/web.php` 파일 내에 정의하므로 `web` 미들웨어 그룹의 모든 미들웨어가 이 라우트에 적용됩니다. 필요하다면 추가 미들웨어를 자유롭게 지정할 수 있습니다.

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 요청 제한(Rate Limiting)

<a name="defining-rate-limiters"></a>
### Rate Limiter 정의

Laravel에는 개별 라우트 또는 라우트 그룹의 트래픽 양을 제한할 수 있는 강력하고 유연한 Rate Limiting 서비스가 내장되어 있습니다. 먼저, 애플리케이션에 맞는 Rate Limiter 구성부터 정의해야 합니다.

Rate Limiter는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 정의합니다.

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

Rate Limiter는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다. 이 메서드는 Rate Limiter 이름과, 해당 Limiter를 적용할 라우트에 대한 제한 설정을 반환하는 클로저를 받습니다. 제한 설정은 `Illuminate\Cache\RateLimiting\Limit` 클래스의 인스턴스이며, 여러 "빌더" 메서드로 제한을 쉽게 정의할 수 있습니다. Rate Limiter 이름은 임의의 문자열을 사용할 수 있습니다.

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

요청이 지정된 제한을 초과하면, Laravel은 자동으로 429 HTTP 상태 코드로 응답합니다. 제한을 초과할 때 반환할 사용자 정의 응답을 지정하고 싶다면, `response` 메서드를 사용할 수 있습니다.

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

Rate Limiter의 클로저는 요청 인스턴스를 전달받기 때문에, 요청 내용이나 인증된 사용자별로 동적으로 Rate Limit을 지정할 수 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perHour(10);
});
```

<a name="segmenting-rate-limits"></a>
#### Rate Limit 세분화

Rate Limit을 임의 값(예: IP 주소 등) 별로 세분화하고 싶을 때는 `by` 메서드를 사용하세요. 예를 들어, 각 IP별로 분당 100회 접근을 제한하려면 다음과 같이 작성합니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

또다른 예시로, 인증된 유저에게는 분당 100회, 게스트는 분당 10회로 제한할 수도 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 다중 Rate Limit

필요하다면, 하나의 Rate Limiter 구성에서 여러 제한을 배열로 반환할 수도 있습니다. 배열 내 제한들은 모두 평가됩니다(앞쪽 순서부터).

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

`by` 값이 동일한 여러 Rate Limit을 지정할 경우, 각각의 `by` 값이 서로 다르도록 프리픽스를 붙여 관리할 수 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 Rate Limiter 연결

라우트 혹은 라우트 그룹에 Rate Limiter를 적용하려면 `throttle` [미들웨어](/docs/12.x/middleware)를 사용하세요. 이 미들웨어는 적용할 Rate Limiter의 이름을 옵션으로 받습니다.

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
#### Redis로 제한 관리

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스로 매핑됩니다. 하지만 애플리케이션의 캐시 드라이버로 Redis를 사용할 경우, Laravel이 Redis로 Rate Limiting을 관리하도록 할 수 있습니다. 이를 위해서는 애플리케이션의 `bootstrap/app.php` 파일에서 `throttleWithRedis` 메서드를 호출합니다. 이 메서드는 `throttle` 미들웨어를 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 미들웨어 클래스로 매핑합니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 폼 메서드 변조 (Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 액션을 지원하지 않습니다. 따라서 HTML 폼에서 `PUT`, `PATCH`, `DELETE` 라우트를 호출하려면, 폼에 숨겨진 `_method` 필드를 추가해야 합니다. 이 필드에 지정된 값이 실제 HTTP 요청 메서드로 사용됩니다.

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

간편하게 [Blade 디렉티브](/docs/12.x/blade)인 `@method`를 사용해 `_method` 입력 필드를 생성할 수 있습니다.

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 정보 접근

`Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드로 현재 요청을 처리하는 라우트 정보를 얻을 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

`Route` 파사드의 [기본 클래스](https://api.laravel.com/docs/12.x/Illuminate/Routing/Router.html)와 [Route 인스턴스](https://api.laravel.com/docs/12.x/Illuminate/Routing/Route.html)의 전체 API 문서에서 사용 가능한 메서드를 모두 확인할 수 있습니다.

<a name="cors"></a>
## 교차 출처 리소스 공유 (CORS)

Laravel은 CORS `OPTIONS` HTTP 요청에 대해 구성할 수 있는 값으로 자동 응답할 수 있습니다. `OPTIONS` 요청은 애플리케이션의 글로벌 미들웨어 스택에 자동 포함된 `HandleCors` [미들웨어](/docs/12.x/middleware)에 의해 처리됩니다.

애플리케이션의 CORS 구성 값을 커스터마이즈하려면, `config:publish` Artisan 명령어로 `cors` 설정 파일을 배포할 수 있습니다.

```shell
php artisan config:publish cors
```

이 명령어를 실행하면 애플리케이션의 `config` 디렉터리에 `cors.php` 설정 파일이 생성됩니다.

> [!NOTE]
> CORS 및 CORS 헤더에 대한 자세한 내용은 [MDN web documentation on CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

애플리케이션을 프로덕션 환경에 배포할 때는 Laravel의 라우트 캐시를 적극적으로 활용해야 합니다. 라우트 캐시를 사용하면 모든 라우트 등록 시간을 크게 줄일 수 있습니다. 라우트 캐시를 생성하려면 `route:cache` Artisan 명령어를 실행하세요.

```shell
php artisan route:cache
```

이 명령어를 실행하면, 모든 요청에서 캐시된 라우트 파일이 로드됩니다. 새 라우트를 추가할 경우 반드시 라우트 캐시를 다시 생성해야 하므로, 실제 프로젝트 배포 시에만 `route:cache` 명령을 사용하는 것이 좋습니다.

라우트 캐시는 `route:clear` 명령으로 지울 수 있습니다.

```shell
php artisan route:clear
```
