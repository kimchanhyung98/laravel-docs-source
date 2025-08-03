# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리디렉트 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록 보기](#listing-your-routes)
    - [라우팅 커스터마이징](#routing-customization)
- [라우트 매개변수](#route-parameters)
    - [필수 매개변수](#required-parameters)
    - [선택적 매개변수](#parameters-optional-parameters)
    - [정규 표현식 제약 조건](#parameters-regular-expression-constraints)
- [이름 있는 라우트](#named-routes)
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
- [요청 제한 (Rate Limiting)](#rate-limiting)
    - [요청 제한기 정의](#defining-rate-limiters)
    - [요청 제한기 라우트에 연결하기](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근하기](#accessing-the-current-route)
- [교차 출처 리소스 공유 (CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

가장 기본적인 Laravel 라우트는 URI와 클로저를 받아 간단하고 명확하게 라우트와 동작을 정의할 수 있도록 합니다. 복잡한 라우팅 설정 파일 없이도 쉽게 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일 (The Default Route Files)

모든 Laravel 라우트는 `routes` 디렉터리에 위치한 라우트 파일들에 정의됩니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 지정된 설정에 따라 Laravel이 자동으로 로드합니다. `routes/web.php` 파일은 웹 인터페이스용 라우트를 정의하며, 이 라우트들에는 세션 상태나 CSRF 보호 같은 기능을 제공하는 `web` [미들웨어 그룹](/docs/12.x/middleware#laravels-default-middleware-groups)이 할당됩니다.

대부분 애플리케이션에서는 `routes/web.php` 파일에서 라우트를 정의하는 것으로 시작합니다. `routes/web.php`에 정의한 라우트는 브라우저에서 해당 URL을 입력하면 접근할 수 있습니다. 예를 들어, 다음 라우트는 `http://example.com/user`로 접속 시 동작합니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트 (API Routes)

애플리케이션이 상태 비저장(stateless) API를 제공할 경우, `install:api` Artisan 명령어로 API 라우팅을 활성화할 수 있습니다:

```shell
php artisan install:api
```

`install:api` 명령어는 강력하면서도 간단한 API 토큰 인증 가드인 [Laravel Sanctum](/docs/12.x/sanctum)를 설치합니다. 이를 이용해 서드파티 API 소비자, SPA, 모바일 애플리케이션을 인증할 수 있습니다. 또한, `routes/api.php` 파일을 생성합니다:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

`routes/api.php`의 라우트들은 상태 비저장이며 `api` [미들웨어 그룹](/docs/12.x/middleware#laravels-default-middleware-groups)이 할당됩니다. 또한 `/api` URI 접두사가 자동으로 적용되므로 파일의 모든 라우트에 수동으로 접두사를 지정할 필요가 없습니다. 접두사를 변경하려면 애플리케이션의 `bootstrap/app.php` 파일을 수정하세요:

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메서드 (Available Router Methods)

라우터에서는 모든 HTTP 메서드(verb)에 응답하는 라우트를 등록할 수 있습니다:

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

때로는 여러 HTTP 메서드에 응답하는 라우트를 등록해야 할 수 있습니다. 이럴 때 `match` 메서드를 사용하거나, 모든 메서드에 응답하는 라우트는 `any` 메서드를 사용하세요:

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일한 URI를 갖는 여러 라우트를 정의할 때, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드 사용하는 라우트가 `any`, `match`, `redirect` 등의 메서드를 사용하는 라우트보다 먼저 정의되어야 합니다. 이렇게 해야 들어오는 요청이 올바른 라우트와 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입 (Dependency Injection)

라우트 콜백 함수의 시그니처에서 필요한 의존 객체를 타입 힌트로 지정하면, Laravel의 [서비스 컨테이너](/docs/12.x/container)가 자동으로 해당 의존성을 해결하고 주입합니다. 예를 들어, `Illuminate\Http\Request` 클래스를 타입 힌트로 지정하면 현재 HTTP 요청 객체가 자동으로 주입됩니다:

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호 (CSRF Protection)

`web` 라우트 파일에 정의된 POST, PUT, PATCH, DELETE 라우트로 연결되는 HTML 폼에는 반드시 CSRF 토큰 필드를 포함해야 합니다. 그렇지 않으면 요청이 거부됩니다. CSRF 보호에 대한 자세한 내용은 [CSRF 문서](/docs/12.x/csrf)를 참고하세요:

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리디렉트 라우트 (Redirect Routes)

다른 URI로 리디렉트하는 라우트를 정의할 때는 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 간단한 리디렉트를 위해 전체 라우트나 컨트롤러를 정의할 필요 없이 편리한 단축키를 제공합니다:

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 302 상태 코드를 반환합니다. 세 번째 옵션 인수로 상태 코드를 변경할 수 있습니다:

```php
Route::redirect('/here', '/there', 301);
```

또는 `Route::permanentRedirect` 메서드를 사용해 301 상태 코드를 반환할 수도 있습니다:

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리디렉트 라우트에서 라우트 매개변수를 사용할 때, Laravel이 예약한 매개변수인 `destination`과 `status`는 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트 (View Routes)

라우트가 단순히 [뷰](/docs/12.x/views)를 반환해야 할 경우 `Route::view` 메서드를 사용할 수 있습니다. `redirect` 메서드와 마찬가지로, 전체 라우트나 컨트롤러를 정의하지 않아도 되는 간단한 단축키입니다. `view` 메서드는 첫 번째 인자로 URI, 두 번째 인자로 뷰 이름을 받으며, 선택적으로 세 번째 인자로 뷰에 전달할 데이터를 배열 형태로 지정할 수 있습니다:

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 매개변수를 사용할 때, Laravel이 예약한 매개변수인 `view`, `data`, `status`, `headers`는 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 보기 (Listing Your Routes)

`route:list` Artisan 명령어로 애플리케이션에 정의된 모든 라우트를 쉽게 확인할 수 있습니다:

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 미들웨어는 표시되지 않습니다. `-v` 옵션을 추가하면 라우트 미들웨어 및 미들웨어 그룹 이름을 표시할 수 있습니다:

```shell
php artisan route:list -v

# 미들웨어 그룹 확장 보기...
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 표시하려면 `--path` 옵션을 사용하세요:

```shell
php artisan route:list --path=api
```

타사 패키지가 제공하는 라우트를 제외하고 보고 싶으면 `--except-vendor` 옵션을 사용하세요:

```shell
php artisan route:list --except-vendor
```

반대로 타사 패키지 라우트만 보고 싶으면 `--only-vendor` 옵션을 사용합니다:

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우팅 커스터마이징 (Routing Customization)

기본적으로 애플리케이션의 라우트는 `bootstrap/app.php` 파일에서 구성되며 로드됩니다:

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

필요에 따라 라우트를 별도의 파일에 나누어 정의하고자 할 수 있습니다. 이때 `withRouting` 메서드에 `then` 클로저를 제공하여 추가 라우트를 등록할 수 있습니다:

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

또는 `using` 클로저를 제공해서 라우트 등록을 완전히 직접 제어할 수도 있습니다. 이 경우 프레임워크가 HTTP 라우트를 자동 등록하지 않고, 모든 라우트를 수동으로 등록해야 합니다:

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
## 라우트 매개변수 (Route Parameters)

<a name="required-parameters"></a>
### 필수 매개변수 (Required Parameters)

URI에서 특정 구간을 캡처해야 할 때, 예를 들어 URL에서 사용자 ID를 추출하고 싶을 때는 라우트 매개변수를 정의할 수 있습니다:

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요에 따라 여러 개의 라우트 매개변수를 정의할 수도 있습니다:

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 매개변수는 항상 `{}` 중괄호로 감싸며, 문자로 이루어져야 합니다. 언더스코어(`_`)도 허용됩니다. 매개변수 이름은 중요하지 않고, 콜백 또는 컨트롤러 인수 순서대로 값이 주입됩니다.

<a name="parameters-and-dependency-injection"></a>
#### 매개변수와 의존성 주입

라우트 콜백에서 서비스 컨테이너의 자동 의존성 주입을 활용하려면 매개변수들을 의존성 뒤쪽에 위치시키세요:

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 매개변수 (Optional Parameters)

경우에 따라 URI에 항상 존재하지 않을 수도 있는 라우트 매개변수를 지정해야 합니다. 이런 매개변수 이름 뒤에 `?`를 붙이고, 콜백 변수에 기본값을 할당하세요:

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규 표현식 제약 조건 (Regular Expression Constraints)

`where` 메서드를 사용하여 라우트 매개변수 형식을 제한할 수 있습니다. 첫 번째 인자로 매개변수 이름, 두 번째 인자로 정규 표현식을 지정합니다:

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

자주 쓰이는 패턴을 검사하는 헬퍼 메서드도 있습니다:

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

요청이 라우트 패턴 제약 조건에 맞지 않으면 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약 조건 (Global Constraints)

특정 매개변수 이름에 항상 같은 정규 표현식 제약을 적용하고 싶다면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `pattern` 메서드로 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Route::pattern('id', '[0-9]+');
}
```

이 패턴이 정의되면, 해당 이름의 모든 라우트 매개변수에 자동 적용됩니다:

```php
Route::get('/user/{id}', function (string $id) {
    // {id}가 숫자일 때만 실행됨...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시 (Encoded Forward Slashes)

Laravel 라우팅은 `/`를 제외한 모든 문자를 라우트 매개변수 값에 허용합니다. 매개변수에 `/` 문자를 포함하려면 `where` 조건에 올바른 정규식으로 명시해야 합니다:

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 라우트 경로의 마지막 구간에만 지원됩니다.

<a name="named-routes"></a>
## 이름 있는 라우트 (Named Routes)

이름 있는 라우트를 사용하면 특정 라우트에 편리하게 URL 생성이나 리디렉트를 할 수 있습니다. `name` 메서드를 라우트 정의 끝에 체인으로 붙여 이름을 지정하세요:

```php
Route::get('/user/profile', function () {
    // ...
})->name('profile');
```

컨트롤러 액션에도 라우트 이름을 지정할 수 있습니다:

```php
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!WARNING]
> 라우트 이름은 항상 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 이름 있는 라우트로 URL 생성하기

라우트에 이름을 지정한 후에는 Laravel의 `route` 및 `redirect` 헬퍼 함수를 통해 URL 생성이나 리디렉트를 할 때 해당 라우트 이름을 사용할 수 있습니다:

```php
// URL 생성...
$url = route('profile');

// 리디렉트 생성...
return redirect()->route('profile');

return to_route('profile');
```

매개변수를 가진 라우트의 경우, 두 번째 인자로 매개변수를 배열로 넘겨주면 URL에 자동으로 올바른 위치에 삽입됩니다:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

추가로 배열에 포함된 키-값 쌍은 URL 쿼리스트링으로 자동 추가됩니다:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// 결과: /user/1/profile?photos=yes
```

> [!NOTE]
> 요청 전역에 걸쳐 URL 매개변수의 기본값을 설정하려면 [URL::defaults 메서드](/docs/12.x/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 검사하기

현재 요청이 특정 이름 있는 라우트에 속하는지 확인하려면, `Route` 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어, 라우트 미들웨어에서 현재 라우트 이름을 검사할 때:

```php
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * 전달된 요청 처리.
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

라우트 그룹은 다수의 라우트에 공통 속성(미들웨어 등)을 공유할 수 있도록 도와줍니다. 각 라우트 개별로 속성을 지정하지 않아도 됩니다.

중첩된 그룹들은 상위 그룹 속성과 “지능적”으로 병합됩니다. 미들웨어와 `where` 조건은 병합되고, 이름과 접두사는 덧붙여집니다. 네임스페이스 구분자와 URI 접두사의 슬래시는 적절히 자동 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어 (Middleware)

그룹 내 모든 라우트에 미들웨어를 일괄 적용하려면 `middleware` 메서드를 사용해 그룹 정의 전에 지정하세요. 미들웨어는 배열에 지정된 순서대로 실행됩니다:

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first & second 미들웨어 실행됨...
    });

    Route::get('/user/profile', function () {
        // first & second 미들웨어 실행됨...
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러 (Controllers)

하나의 컨트롤러를 공유하는 여러 라우트가 있다면, 그룹에 `controller` 메서드로 공통 컨트롤러를 지정할 수 있습니다. 라우트 정의 시에는 메서드 이름만 지정하면 됩니다:

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅 (Subdomain Routing)

라우트 그룹으로 서브도메인 라우팅을 처리할 수 있습니다. 서브도메인도 라우트 URI처럼 매개변수를 가질 수 있어, 서브도메인의 일부를 라우트 혹은 컨트롤러에서 사용할 수 있습니다. `domain` 메서드를 그룹 정의 전 호출해 서브도메인을 설정합니다:

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

> [!WARNING]
> 서브도메인 라우트를 루트 도메인 라우트보다 먼저 등록하세요. 그래야 URI 경로가 같은 루트 도메인 라우트가 서브도메인 라우트를 덮어쓰지 않습니다.

<a name="route-group-prefixes"></a>
### 라우트 접두사 (Route Prefixes)

`prefix` 메서드로 그룹 내 모든 라우트 URI 앞에 공통 접두사를 붙일 수 있습니다. 예를 들어 그룹 내 라우트를 `admin` 접두사로 시작하게 할 수 있습니다:

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // /admin/users URL에 매칭됨
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두사 (Route Name Prefixes)

`name` 메서드로 그룹 내 모든 라우트 이름에 공통 접두사를 붙일 수 있습니다. 접두사를 지정할 때는 후행 점(`.`)을 붙이는 것을 잊지 마세요. 예를 들어, 그룹 내 모든 라우트의 이름에 `admin.`을 붙이려면:

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // 라우트 이름은 "admin.users"가 됨
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

라우트나 컨트롤러에 모델 ID를 전달할 때, 모델을 직접 데이터베이스에서 조회해서 주입하는 기능이 라우트 모델 바인딩입니다. 예를 들어, 사용자 ID 대신 해당 사용자 `User` 모델 인스턴스를 바로 주입할 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩 (Implicit Binding)

암묵적 바인딩은 라우트 세그먼트 이름과 타입힌트된 변수명이 일치할 때, 자동으로 Eloquent 모델을 조회해 인스턴스를 주입합니다. 예:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

라우트 URI의 `{user}` 세그먼트 값과 일치하는 ID를 가진 `User` 인스턴스를 자동으로 데이터베이스에서 조회해 주입합니다. 일치하는 모델이 없으면 404 HTTP 응답이 반환됩니다.

컨트롤러 메서드 방식에서도 적용됩니다. `{user}` URI 세그먼트가 컨트롤러 내 `$user` 타입힌트 변수와 일치하므로 자동 주입됩니다:

```php
use App\Http\Controllers\UserController;
use App\Models\User;

// 라우트 정의...
Route::get('/users/{user}', [UserController::class, 'show']);

// 컨트롤러 메서드...
public function show(User $user)
{
    return view('user.profile', ['user' => $user]);
}
```

<a name="implicit-soft-deleted-models"></a>
#### Soft Delete된 모델

암묵적 바인딩은 기본적으로 [Soft Delete](/docs/12.x/eloquent#soft-deleting)된 모델은 조회하지 않습니다. 하지만 `withTrashed` 메서드를 체인해 호출하면 Soft Delete된 모델도 조회 대상에 포함됩니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 이름 커스터마이징

`id` 컬럼 외의 다른 컬럼을 키로 사용해 모델을 조회하려면 라우트 매개변수 정의에 컬럼명을 지정하세요:

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

또는, 모델 클래스에서 `getRouteKeyName` 메서드를 오버라이드해 항상 특정 컬럼을 기본 키로 사용하도록 할 수 있습니다:

```php
/**
 * 모델의 라우트 키명을 반환합니다.
 */
public function getRouteKeyName(): string
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
#### 스코핑된 커스텀 키

여러 모델을 암묵적 바인딩할 때 두 번째 모델이 이전 모델의 자식이어야 한다면 스코핑 바인딩을 활용하세요. 예를 들어 아래는 특정 사용자에 속한 포스트를 slug로 조회하는 라우트입니다:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

Laravel은 암묵적으로 부모 모델(`User`)의 관계 이름(`posts`)을 추정해 자식 모델 조회 시 이 관계 기준으로 제한합니다.

커스텀 키가 없더라도 스코핑 바인딩을 적용하려면 라우트에 `scopeBindings` 메서드를 호출하세요:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

라우트 그룹 전체에 스코핑 바인딩을 적용할 수도 있습니다:

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로 스코핑 바인딩을 적용하지 않으려면 `withoutScopedBindings`를 호출하세요:

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 일치하는 모델 없을 때 처리 커스터마이징

기본적으로 암묵적 바인딩된 모델이 없으면 404가 반환되지만, `missing` 메서드에 클로저를 전달해 일치하는 모델을 찾지 못했을 때의 동작을 직접 정의할 수 있습니다:

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
### 암묵적 Enum 바인딩 (Implicit Enum Binding)

PHP 8.1에서 도입된 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 활용해, Laravel은 라우트 정의 시 [string-backed Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 타입힌트로 지정할 수 있습니다. 해당 라우트 세그먼트가 Enum에 정의된 값 중 하나여야 해당 라우트가 실행됩니다. 그렇지 않으면 404 응답이 자동 반환됩니다. 예:

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

아래 라우트는 `{category}` 세그먼트가 `fruits` 혹은 `people`일 때만 호출됩니다:

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩 (Explicit Binding)

Laravel의 암묵적 바인딩을 사용하지 않고, 명시적으로 라우트 매개변수와 모델을 연결할 수도 있습니다. `AppServiceProvider` 클래스의 `boot` 메서드에서 `Route::model` 메서드로 명시적 바인딩을 등록하세요:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Route::model('user', User::class);
}
```

그 후 `{user}` 매개변수를 사용하는 라우트를 정의합니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

이제 `{user}` 매개변수에 대해 `User` 모델 인스턴스가 주입되고, 없는 경우 404가 자동 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 해결 로직 커스터마이징

커스텀 조회 로직을 정의하려면 `Route::bind` 메서드에 클로저를 전달합니다. 이 클로저는 URI 세그먼트 값을 받아, 주입할 모델 인스턴스를 반환해야 합니다. 역시 `AppServiceProvider`의 `boot` 메서드에서 정의합니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Route::bind('user', function (string $value) {
        return User::where('name', $value)->firstOrFail();
    });
}
```

또는, Eloquent 모델 내에서 `resolveRouteBinding` 메서드를 오버라이드해도 됩니다:

```php
/**
 * 바인딩 값을 위해 모델 조회.
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

만약 [암묵적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용하는 경우, 부모 모델의 자식 바인딩 해결용으로 `resolveChildRouteBinding` 메서드가 호출됩니다:

```php
/**
 * 자식 모델 바인딩 해결.
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

`Route::fallback` 메서드를 사용하면, 들어오는 요청과 매칭되는 라우트가 없을 때 실행할 라우트를 정의할 수 있습니다. 일반적으로 처리되지 않는 요청은 예외 핸들러에서 404 페이지로 처리됩니다. 하지만 `routes/web.php`에서 폴백 라우트를 정의하면 `web` 미들웨어 그룹이 자동 적용되므로, 필요하다면 추가 미들웨어도 붙일 수 있습니다:

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 요청 제한 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 요청 제한기 정의 (Defining Rate Limiters)

Laravel은 강력하고 사용자 맞춤형인 요청 제한 서비스를 제공합니다. 특정 라우트 혹은 라우트 그룹에 트래픽 제한을 걸 수 있습니다.

요청 제한기는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드 내에서 정의합니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
protected function boot(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
}
```

`RateLimiter::for` 메서드는 제한기 이름과 제한 로직 클로저를 받습니다. 클로저는 라우트에 할당된 제한 설정(`Illuminate\Cache\RateLimiting\Limit` 객체)을 반환해야 합니다.

제한기 이름은 자유롭게 지정할 수 있습니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
protected function boot(): void
{
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });
}
```

요청이 제한을 초과하면 자동으로 HTTP 429 응답이 반환됩니다. 응답을 커스터마이징하려면 `response` 메서드를 사용하세요:

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

요청 혹은 인증 사용자 상태에 따라 동적으로 제한 수치를 생성할 수도 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
#### 제한 분할 (Segmenting Rate Limits)

예를 들어, IP 주소별로 분할 제한을 걸고 싶을 때는 제한 빌더의 `by` 메서드를 활용해 분할 키를 지정하세요:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

다른 예로, 인증 사용자별로 분당 100회, 게스트 IP별로 분당 10회의 제한을 걸 수 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 다중 요청 제한 (Multiple Rate Limits)

필요에 따라 배열 형태로 여러 제한을 반환할 수 있습니다. 라우트 접근 시 배열에 나열된 순서대로 제한이 적용됩니다:

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

동일한 `by` 값이 중복되지 않도록 접두사를 붙이는 방식을 추천합니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 요청 제한기 라우트에 연결하기 (Attaching Rate Limiters to Routes)

라우트 혹은 라우트 그룹에 `throttle` [미들웨어](/docs/12.x/middleware)로 제한기를 연결할 수 있습니다. 미들웨어에 제한기 이름을 지정하세요:

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
#### Redis를 이용한 요청 제한

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스에 매핑됩니다. 그러나 Redis 캐시 드라이버를 쓴다면 `throttleWithRedis` 메서드를 `bootstrap/app.php`에서 호출해, Redis 기반 미들웨어(`Illuminate\Routing\Middleware\ThrottleRequestsWithRedis`)를 사용하도록 바꿀 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 폼 메서드 스푸핑 (Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` HTTP 메서드를 직접 지원하지 않습니다. 따라서 해당 HTTP 메서드를 사용하는 라우트를 호출하는 폼에는 숨겨진 `_method` 필드를 추가해야 합니다. 폼에 입력한 `_method`값이 실제 HTTP 메서드로 사용됩니다:

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

Blade 템플릿에서는 편리하게 `@method` 디렉티브를 이용해 `_method` 입력 필드를 생성할 수 있습니다:

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 접근하기 (Accessing the Current Route)

현재 요청을 처리 중인 라우트 정보는 `Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 통해 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route 인스턴스
$name = Route::currentRouteName(); // 라우트 이름 (문자열)
$action = Route::currentRouteAction(); // 라우트 액션 (문자열)
```

라우터 및 라우트 클래스의 모든 사용 가능한 메서드는 [Route 파사드 기본 클래스](https://api.laravel.com/docs/12.x/Illuminate/Routing/Router.html)와 [Route 인스턴스](https://api.laravel.com/docs/12.x/Illuminate/Routing/Route.html) API 문서를 참고하세요.

<a name="cors"></a>
## 교차 출처 리소스 공유 (CORS)

Laravel은 CORS `OPTIONS` 요청에 대해 자동으로 구성한 값으로 응답할 수 있습니다. `OPTIONS` 요청은 애플리케이션의 글로벌 미들웨어 스택에 등록된 `HandleCors` [미들웨어](/docs/12.x/middleware)에서 자동 처리합니다.

CORS 설정을 커스터마이징해야 할 때는 `config:publish` Artisan 명령어로 `cors` 구성 파일을 퍼블리시할 수 있습니다:

```shell
php artisan config:publish cors
```

이 명령 수행 후 `config` 디렉터리에 `cors.php` 설정 파일이 생성됩니다.

> [!NOTE]
> CORS 및 관련 헤더에 대한 더 자세한 정보는 [MDN 웹 문서의 CORS 가이드](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

애플리케이션을 프로덕션에 배포할 때 라우트 캐시를 활용하면 라우트 등록 속도를 대폭 향상시킬 수 있습니다. 캐시를 생성하려면 `route:cache` Artisan 명령어를 실행하세요:

```shell
php artisan route:cache
```

이후 캐시된 라우트 파일이 모든 요청에서 로드됩니다. 라우트를 새로 추가했다면 반드시 다시 캐시를 생성해야 하므로, `route:cache` 명령은 프로젝트 배포 시에만 실행하는 것이 좋습니다.

라우트 캐시를 삭제하려면 `route:clear` 명령어를 사용하세요:

```shell
php artisan route:clear
```