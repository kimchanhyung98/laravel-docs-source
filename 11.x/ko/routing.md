# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리다이렉트 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록 확인하기](#listing-your-routes)
    - [라우팅 커스터마이징](#routing-customization)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [선택적 파라미터](#parameters-optional-parameters)
    - [정규식 제약 조건](#parameters-regular-expression-constraints)
- [이름 있는 라우트](#named-routes)
- [라우트 그룹](#route-groups)
    - [미들웨어](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [서브도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 접두어](#route-group-prefixes)
    - [라우트 이름 접두어](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암묵적 바인딩](#implicit-binding)
    - [암묵적 Enum 바인딩](#implicit-enum-binding)
    - [명시적 바인딩](#explicit-binding)
- [폴백 라우트](#fallback-routes)
- [요청 제한 (Rate Limiting)](#rate-limiting)
    - [요청 제한기 정의](#defining-rate-limiters)
    - [라우트에 요청 제한기 적용](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근](#accessing-the-current-route)
- [교차 출처 리소스 공유 (CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

Laravel에서 가장 기본적인 라우트는 URI와 클로저(Closure)를 받아, 복잡한 라우팅 설정 없이도 간단하고 직관적으로 라우트와 동작을 정의할 수 있는 방법을 제공합니다:

```
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일 (The Default Route Files)

Laravel의 모든 라우트는 `routes` 디렉터리에 위치한 라우트 파일에서 정의합니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 지정된 설정에 따라 Laravel에서 자동으로 로드합니다. `routes/web.php` 파일은 웹 인터페이스용 라우트를 정의하며, 이 라우트들은 세션 상태 및 CSRF 보호 같은 기능을 제공하는 `web` [미들웨어 그룹](/docs/11.x/middleware#laravels-default-middleware-groups)에 할당됩니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에 라우트를 정의하는 것으로 시작합니다. 여기서 정의한 라우트는 브라우저에서 지정한 URL로 접근할 수 있습니다. 예를 들어, 다음 라우트는 브라우저 주소창에 `http://example.com/user`를 입력하여 접근할 수 있습니다:

```
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트 (API Routes)

애플리케이션에서 상태 비저장(stateless) API도 제공할 경우, `install:api` Artisan 명령어를 사용해 API 라우팅을 활성화할 수 있습니다:

```shell
php artisan install:api
```

`install:api` 명령어는 [Laravel Sanctum](/docs/11.x/sanctum)를 설치하는데, 이는 타사 API 소비자, SPA 또는 모바일 앱 인증에 활용할 수 있는 강력하면서도 간단한 API 토큰 인증 가드를 제공합니다. 또한 `install:api` 명령어는 `routes/api.php` 파일을 생성합니다:

```
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

`routes/api.php`의 라우트는 상태 비저장이고 `api` [미들웨어 그룹](/docs/11.x/middleware#laravels-default-middleware-groups)에 할당되며, 자동으로 `/api` URI 접두어가 적용되므로 파일 내 모든 라우트에 수동으로 붙일 필요가 없습니다. 접두어는 애플리케이션의 `bootstrap/app.php` 파일에서 변경할 수 있습니다:

```
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 지원하는 라우터 메서드 (Available Router Methods)

라우터는 모든 HTTP 동사(verb)에 반응하는 라우트를 등록할 수 있도록 지원합니다:

```
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

가끔 여러 HTTP 동사에 대응하는 라우트를 등록해야 할 경우 `match` 메서드를 사용할 수 있으며, 모든 HTTP 동사에 대응하는 라우트는 `any` 메서드로 등록할 수 있습니다:

```
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]  
> 동일한 URI를 사용하는 여러 라우트를 정의할 때는 `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 먼저 정의하고, 그 이후에 `any`, `match`, `redirect` 메서드를 정의해야 합니다. 이렇게 해야 요청이 정확한 라우트와 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입 (Dependency Injection)

라우트 콜백(Signature)에 필요한 의존성을 타입힌팅(type-hint)할 수 있으며, Laravel의 [서비스 컨테이너](/docs/11.x/container)가 자동으로 의존성을 해결해 주입합니다. 예를 들어, 현재 HTTP 요청을 자동으로 주입받으려면 `Illuminate\Http\Request` 클래스를 타입힌팅하세요:

```
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호 (CSRF Protection)

`web` 라우트 파일에서 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 라우트를 향하는 HTML 폼에는 반드시 CSRF 토큰 필드를 포함해야 합니다. 필수 토큰이 없으면 요청이 거절됩니다. CSRF 보호에 관한 자세한 내용은 [CSRF 문서](/docs/11.x/csrf)를 참고하세요:

```
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리다이렉트 라우트 (Redirect Routes)

다른 URI로 리다이렉트하는 라우트를 정의할 경우, `Route::redirect` 메서드를 사용할 수 있습니다. 이 방법은 리다이렉트를 위한 전체 라우트 또는 컨트롤러를 정의하지 않고 간편하게 리다이렉트를 구현할 수 있습니다:

```
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 HTTP 상태 코드 `302`를 반환하며, 선택적 세 번째 인자에 상태 코드를 지정하여 변경할 수 있습니다:

```
Route::redirect('/here', '/there', 301);
```

또는 `Route::permanentRedirect` 메서드를 사용하여 상태 코드 `301`을 반환할 수도 있습니다:

```
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]  
> 리다이렉트 라우트에서 라우트 파라미터를 사용할 경우, Laravel이 예약한 `destination` 및 `status` 파라미터 이름은 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트 (View Routes)

라우트가 단순히 [뷰](/docs/11.x/views)만 반환할 필요가 있을 때는 `Route::view` 메서드를 사용할 수 있습니다. `redirect` 메서드처럼, 전체 라우트나 컨트롤러를 정의하지 않고 간단히 뷰를 반환할 수 있기 때문에 편리합니다. `view` 메서드는 첫 번째 인자로 URI, 두 번째 인자로 뷰 이름을 받고, 선택적으로 세 번째 인자로 뷰에 전달할 데이터를 배열로 받을 수 있습니다:

```
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]  
> 뷰 라우트에서 라우트 파라미터를 사용할 경우, Laravel에서 예약한 `view`, `data`, `status`, 그리고 `headers` 파라미터 이름은 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 확인하기 (Listing Your Routes)

`route:list` Artisan 명령어는 애플리케이션에 정의된 모든 라우트의 개요를 쉽게 확인할 수 있습니다:

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 미들웨어는 출력되지 않습니다. 미들웨어 이름과 그룹명을 함께 보려면 `-v` 옵션을 명령어에 추가하세요:

```shell
php artisan route:list -v

# 미들웨어 그룹 확장 보기...
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 보고 싶다면 다음과 같이 `--path` 옵션을 사용하세요:

```shell
php artisan route:list --path=api
```

또한, 타사 패키지에서 정의한 라우트를 제외하려면 `--except-vendor` 옵션을 주고 실행할 수 있습니다:

```shell
php artisan route:list --except-vendor
```

그 반대로 타사 패키지 라우트만 보고 싶으면 `--only-vendor` 옵션을 사용하세요:

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우팅 커스터마이징 (Routing Customization)

기본적으로 애플리케이션 라우트는 `bootstrap/app.php` 파일에서 설정 및 로드됩니다:

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

경우에 따라 라우트 일부를 별도 파일로 나누어 정의하고 싶을 수 있습니다. 이럴 때 `withRouting` 메서드에 `then` 클로저를 제공하면, 추가로 필요한 라우트를 등록할 수 있습니다:

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

또는 `withRouting` 메서드에 `using` 클로저를 넘기면, 프레임워크가 HTTP 라우트를 전혀 등록하지 않고 완전한 라우트 등록을 직접 수행할 수 있습니다:

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
### 필수 파라미터 (Required Parameters)

때때로 URI 세그먼트의 일부를 캡처해야 할 때가 있습니다. 예를 들어, URL에서 사용자 ID를 캡처할 수 있습니다. 이때 라우트 파라미터를 정의할 수 있습니다:

```
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요에 따라 라우트 파라미터를 여러 개 정의할 수 있습니다:

```
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 파라미터는 항상 `{}` 중괄호로 감싸고, 알파벳 문자로 이름을 지정해야 합니다. 언더스코어(`_`)도 허용됩니다. 파라미터는 콜백 또는 컨트롤러 메서드 인자 순서에 따라 주입되며, 인자 이름은 중요하지 않습니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입 (Parameters and Dependency Injection)

라우트에 의존성도 함께 주입받으려면, 의존성을 먼저 타입힌팅하고 라우트 파라미터를 뒤에 나열하면 됩니다:

```
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 파라미터 (Optional Parameters)

때때로 URI에 항상 존재하지 않는 선택적 파라미터가 필요할 수 있습니다. 파라미터 이름 끝에 `?`를 추가해서 선택적으로 만들 수 있으며, 해당 변수에 기본값을 할당해야 합니다:

```
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규식 제약 조건 (Regular Expression Constraints)

`where` 메서드를 사용해 라우트 파라미터 값의 형식을 제한할 수 있습니다. 이 메서드는 파라미터 이름과 정규식 패턴을 인자로 받습니다:

```
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

자주 쓰는 정규식 패턴들을 위해 편리한 헬퍼 메서드도 제공됩니다:

```
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

패턴에 맞지 않는 요청이 들어오면, 자동으로 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약 조건 (Global Constraints)

특정 라우트 파라미터 이름에 대해 항상 같은 정규식 제약을 적용하려면, `Route::pattern` 메서드를 사용하세요. 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의하는 것이 좋습니다:

```
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::pattern('id', '[0-9]+');
}
```

이후 해당 이름의 모든 라우트 파라미터에 이 패턴이 자동 적용됩니다:

```
Route::get('/user/{id}', function (string $id) {
    // {id}가 숫자인 경우에만 실행...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시 (Encoded Forward Slashes)

Laravel 라우팅 컴포넌트는 기본적으로 `/` 문자를 제외한 모든 문자를 라우트 파라미터 값에 허용합니다. `/`를 포함시키려면 `where` 메서드에 적절한 정규식(예: `.*`)을 명시해야 합니다:

```
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]  
> 인코딩된 슬래시는 반드시 라우트의 마지막 세그먼트에서만 지원됩니다.

<a name="named-routes"></a>
## 이름 있는 라우트 (Named Routes)

이름 있는 라우트를 사용하면 특정 라우트에 대해 URL 생성이나 리다이렉트를 편리하게 할 수 있습니다. `name` 메서드를 라우트 정의에 체인으로 연결해 이름을 지정할 수 있습니다:

```
Route::get('/user/profile', function () {
    // ...
})->name('profile');
```

컨트롤러 액션에도 이름을 붙일 수 있습니다:

```
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!WARNING]  
> 라우트 이름은 항상 유니크해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 이름 있는 라우트로 URL 생성하기 (Generating URLs to Named Routes)

라우트에 이름을 지정한 이후 Laravel의 `route` 및 `redirect` 헬퍼 함수를 사용해 URL 생성이나 리다이렉트를 할 수 있습니다:

```
// URL 생성...
$url = route('profile');

// 리다이렉트 생성...
return redirect()->route('profile');

return to_route('profile');
```

이름 있는 라우트가 파라미터를 포함한다면, 두 번째 인자로 파라미터를 넘겨 URL에 자동으로 삽입할 수 있습니다:

```
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

추가로 배열에 키-값 쌍을 넘기면 쿼리 스트링으로 자동 변환됩니다:

```
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// 결과: /user/1/profile?photos=yes
```

> [!NOTE]  
> 요청 범위의 기본 URL 파라미터 값을 지정하고 싶을 때, 예를 들어 현재 로케일 등, [`URL::defaults` 메서드](/docs/11.x/urls#default-values)를 사용하세요.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 검사하기 (Inspecting the Current Route)

현재 요청이 특정 이름의 라우트에 매핑되었는지 확인하려면, 라우트 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어 라우트 미들웨어에서 현재 라우트 이름을 검사하려면:

```
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

라우트 그룹은 여러 라우트에 미들웨어 같은 공통 속성을 공유할 때 개별 라우트마다 속성을 따로 정의하지 않아도 되게 해줍니다.

중첩 그룹은 부모 그룹과 속성을 "스마트하게" 병합합니다. 미들웨어와 `where` 조건은 병합되고, 이름과 접두어는 덧붙여집니다. 네임스페이스 구분자 및 URI 접두어의 슬래시는 자동으로 적절히 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어 (Middleware)

그룹 내 모든 라우트에 [미들웨어](/docs/11.x/middleware)를 지정하려면, 그룹 정의 전에 `middleware` 메서드를 사용하세요. 미들웨어는 배열에 나열한 순서로 실행됩니다:

```
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first 및 second 미들웨어가 실행됨...
    });

    Route::get('/user/profile', function () {
        // first 및 second 미들웨어가 실행됨...
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러 (Controllers)

동일 컨트롤러를 사용하는 라우트 집합이 있다면, `controller` 메서드를 사용해 그룹의 공통 컨트롤러를 지정할 수 있습니다. 이후 라우트를 정의할 때는 호출할 메서드 이름만 지정하면 됩니다:

```
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅 (Subdomain Routing)

라우트 그룹은 서브도메인 라우팅도 지원합니다. URI처럼 서브도메인에도 라우트 파라미터를 지정할 수 있어, 서브도메인의 일부분을 캡처할 수 있습니다. `domain` 메서드로 서브도메인을 지정한 뒤 그룹을 정의합니다:

```
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

> [!WARNING]  
> 서브도메인 라우트가 정상 작동하려면, 루트 도메인 라우트 등록 전에 서브도메인 라우트를 등록해야 합니다. 그렇지 않으면 URI가 동일한 루트 도메인 라우트가 서브도메인 라우트를 덮어쓸 수 있습니다.

<a name="route-group-prefixes"></a>
### 라우트 접두어 (Route Prefixes)

`prefix` 메서드를 이용해 그룹 내 모든 라우트 URI에 공통 접두어를 붙일 수 있습니다. 예를 들어 그룹 내 모든 라우트에 `admin` 접두어를 붙이고 싶다면:

```
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" 경로와 매칭됨
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두어 (Route Name Prefixes)

`name` 메서드를 사용하면 그룹 내 모든 라우트 이름에 공통 접두어를 붙일 수 있습니다. 예를 들어 그룹 라우트 이름에 `admin.` 접두어를 붙이려면, 접두어 끝에 점(`.`)을 반드시 포함해야 합니다:

```
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // 라우트 이름이 "admin.users"로 지정됨
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

라우트나 컨트롤러 액션에 모델 ID를 전달받을 때, 보통 그 ID에 해당하는 모델을 데이터베이스에서 조회하는 코드를 작성합니다. Laravel의 라우트 모델 바인딩은 해당 모델 인스턴스를 자동으로 주입하는 편리한 방법을 제공합니다. 예컨대 사용자 ID 대신에 전체 `User` 모델 인스턴스를 바로 주입받을 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩 (Implicit Binding)

Laravel은 라우트 또는 컨트롤러 액션의 타입힌트 변수 이름이 URL 세그먼트 이름과 일치하는 경우, 자동으로 해당 Eloquent 모델을 찾아 주입해줍니다. 예:

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

`$user`가 `App\Models\User` 타입힌트이며, 라우트 URI 세그먼트 `{user}`와 이름도 일치하므로, URI 값과 일치하는 ID를 가진 모델 인스턴스를 자동으로 삽입해줍니다. 데이터베이스에서 일치하는 모델이 없으면 자동으로 404 응답을 반환합니다.

컨트롤러 메서드에서도 마찬가지입니다:

```
use App\Http\Controllers\UserController;
use App\Models\User;

// 라우트 정의
Route::get('/users/{user}', [UserController::class, 'show']);

// 컨트롤러 메서드 정의
public function show(User $user)
{
    return view('user.profile', ['user' => $user]);
}
```

<a name="implicit-soft-deleted-models"></a>
#### 소프트 삭제된 모델 (Soft Deleted Models)

기본적으로 암묵적 바인딩은 [소프트 삭제](/docs/11.x/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 하지만 `withTrashed` 메서드를 체인하면 소프트 삭제된 모델까지 조회할 수 있습니다:

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 이름 커스터마이징 (Customizing the Key)

ID가 아니라 다른 컬럼으로 모델을 조회하고 싶으면, 라우트 파라미터 정의 시 `:` 다음에 컬럼명을 명시하세요:

```
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

또한 항상 특정 컬럼으로 모델 바인딩을 하려면, Eloquent 모델에서 `getRouteKeyName` 메서드를 오버라이드하세요:

```
/**
 * 라우트 키로 사용할 컬럼명 반환
 */
public function getRouteKeyName(): string
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
#### 커스텀 키와 스코핑 (Custom Keys and Scoping)

한 라우트에서 여러 Eloquent 모델을 바인딩할 때, 두 번째 모델이 첫 번째 모델 하위 자식임을 보장하고 싶을 수 있습니다. 예를 들어, 특정 사용자의 블로그 포스트를 슬러그로 조회하는 경우:

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

Laravel은 첫 번째 모델이 가진 `posts` 관계를 자동으로 추측해 바인딩 쿼리에 스코프를 적용합니다.

커스텀 키를 사용하지 않는 경우에도 스코핑을 강제하려면, 라우트 정의 시 `scopeBindings` 메서드를 호출하세요:

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는 스코핑을 그룹 단위로 활성화할 수도 있습니다:

```
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로 스코핑을 명시적으로 비활성화하려면 `withoutScopedBindings` 메서드를 사용하세요:

```
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 모델 미발견 시 동작 커스터마이징 (Customizing Missing Model Behavior)

기본적으로 라우트 모델 바인딩 실패 시 404 응답이 생성됩니다. 하지만 `missing` 메서드에 콜백을 넘겨 동작을 커스터마이징할 수 있습니다:

```
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

PHP 8.1부터 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php) 지원이 추가되었습니다. Laravel은 문자열 기반 Enum 타입힌팅을 라우트에 사용하면, 해당 라우트 세그먼트가 유효한 Enum 값일 때만 라우트를 호출합니다. 그렇지 않으면 404를 자동 반환합니다. 예를 들어 다음 Enum이 있다면:

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

라우트를 다음과 같이 정의할 수 있습니다:

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

라우트 세그먼트 `{category}`가 `fruits` 또는 `people`이 아니면 자동으로 404 응답이 반환됩니다.

<a name="explicit-binding"></a>
### 명시적 바인딩 (Explicit Binding)

Laravel의 암묵적 바인딩 방식을 강제하지 않아도 되며, 라우트 파라미터와 모델을 명시적으로 바인딩할 수 있습니다. `Route::model` 메서드를 사용해 특정 파라미터에 생성할 모델 클래스를 지정하고, 보통 `AppServiceProvider` 클래스 `boot` 메서드에 정의합니다:

```
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

그 후 `{user}` 파라미터가 있는 라우트를 정의하세요:

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

이 설정으로 `users/1` 등의 요청 시 `id=1`인 `User` 모델 인스턴스가 자동으로 주입됩니다.

만약 일치하는 모델이 없으면 404가 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 해석 로직 커스터마이징 (Customizing the Resolution Logic)

자체적인 바인딩 해석 로직을 정의하고 싶다면 `Route::bind` 메서드를 사용하세요. 여기서 넘긴 클로저는 URI 세그먼트 값을 받아서 모델 인스턴스를 반환해야 합니다. 이 역시 `AppServiceProvider`의 `boot` 메서드에서 정의합니다:

```
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

또는 Eloquent 모델에서 `resolveRouteBinding` 메서드를 오버라이드해도 됩니다. 이 메서드는 URI 세그먼트 값을 받아 주입할 모델 인스턴스를 반환합니다:

```
/**
 * 바운딩된 값을 위한 모델 조회
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

[암묵적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용하는 경우, 부모 모델의 자식 바인딩을 위해 `resolveChildRouteBinding` 메서드가 호출됩니다:

```
/**
 * 바운딩된 자식 모델 조회
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

`Route::fallback` 메서드로 모든 라우트에 매칭되지 않았을 때 실행할 라우트를 정의할 수 있습니다. 보통 처리되지 않은 요청은 애플리케이션 예외 핸들러가 "404" 페이지를 렌더링합니다. 폴백 라우트는 보통 `routes/web.php`안에 정의되므로, `web` 미들웨어 그룹의 미들웨어들이 적용됩니다. 필요시 추가 미들웨어도 지정할 수 있습니다:

```
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 요청 제한 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 요청 제한기 정의 (Defining Rate Limiters)

Laravel은 강력하고 유연한 요청 제한(rate limiting) 기능을 제공하며, 특정 라우트나 라우트 그룹의 트래픽을 제한하는 데 사용할 수 있습니다. 설정을 시작하려면 애플리케이션 요구사항에 맞는 요청 제한기(rate limiter)를 정의해야 합니다.

요청 제한기는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의합니다:

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

`RateLimiter::for` 메서드는 제한기 이름과 제한 정책을 반환하는 클로저를 받습니다. `Limit` 클래스는 제한 설정에 유용한 빌더 메서드를 포함하고 있습니다. 제한기 이름은 임의의 문자열을 지정할 수 있습니다:

```
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

제한을 초과하면 Laravel은 자동으로 HTTP 상태 코드 429 응답을 반환합니다. 직접 응답을 커스터마이징하려면 `response` 메서드를 체인하면 됩니다:

```
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('사용자 정의 응답...', 429, $headers);
    });
});
```

요청 정보나 인증된 사용자 기반으로 동적 제한 정책을 만들 수도 있습니다:

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
#### 제한 분할 (Segmenting Rate Limits)

IP 주소와 같이 임의의 값으로 제한을 분할할 수도 있습니다. 예를 들어, IP당 분당 100번의 요청을 허용하려면 `by` 메서드를 사용하세요:

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

다른 예로, 인증된 사용자 ID별로 분당 100번, 비인증자 IP별로 분당 10번 제한할 수도 있습니다:

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 다중 제한 (Multiple Rate Limits)

필요 시, 특정 제한기 이름에 대해 여러 제한을 배열로 반환할 수도 있습니다. 제한은 배열 순서대로 평가됩니다:

```
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

동일한 `by` 값을 사용하는 다중 제한을 할 때는 각 값이 유니크하도록 접두어를 붙이는 것이 좋습니다:

```
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 요청 제한기 적용 (Attaching Rate Limiters to Routes)

요청 제한기는 `throttle` [미들웨어](/docs/11.x/middleware)를 통해 라우트 또는 라우트 그룹에 적용할 수 있습니다. 미들웨어 인자로 제한기 이름을 전달하세요:

```
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
#### Redis를 이용한 제한 (Throttling With Redis)

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스로 매핑되어 있습니다. 하지만 캐시 드라이버로 Redis를 쓸 경우, Redis 기반 요청 제한 클래스를 매핑할 수도 있습니다. 이것은 `bootstrap/app.php` 파일에서 `throttleWithRedis` 메서드로 설정하세요:

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 폼 메서드 스푸핑 (Form Method Spoofing)

HTML 폼은 기본적으로 `PUT`, `PATCH` 또는 `DELETE` 메서드를 지원하지 않습니다. 따라서 이들 메서드용 라우트를 정의하고 HTML 폼에서 호출할 때는, 폼 내에 숨긴 `_method` 필드를 추가해야 합니다. 이 필드의 값이 실제 HTTP 요청 메서드로 사용됩니다:

```
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

편리하게도 `@method` [Blade 디렉티브](/docs/11.x/blade)를 사용해 `_method` 필드를 생성할 수 있습니다:

```
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 접근 (Accessing the Current Route)

`Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 통해 현재 요청을 처리하는 라우트 정보를 얻을 수 있습니다:

```
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route 인스턴스
$name = Route::currentRouteName(); // 문자열
$action = Route::currentRouteAction(); // 문자열
```

라우터 및 라우트 클래스에서 지원하는 모든 메서드는 각각의 [Route facade 클래스 문서](https://laravel.com/api/11.x/Illuminate/Routing/Router.html)와 [Route 인스턴스 문서](https://laravel.com/api/11.x/Illuminate/Routing/Route.html)를 참고하세요.

<a name="cors"></a>
## 교차 출처 리소스 공유 (CORS)

Laravel은 CORS `OPTIONS` HTTP 요청에 대해 구성한 값을 자동으로 응답할 수 있습니다. 이 `OPTIONS` 요청 처리는 애플리케이션의 글로벌 미들웨어 스택에 기본 포함된 `HandleCors` [미들웨어](/docs/11.x/middleware)가 담당합니다.

애플리케이션에 맞추어 CORS 설정값을 변경하려면, `config:publish` Artisan 명령어로 `cors` 설정 파일을 퍼블리시하세요:

```shell
php artisan config:publish cors
```

명령어 실행 후 `config` 디렉터리에 `cors.php` 설정 파일이 생성됩니다.

> [!NOTE]  
> CORS 및 관련 HTTP 헤더에 대해 자세히 알고 싶다면, [MDN 웹 문서의 CORS 섹션](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)을 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

프로덕션 배포 시 Laravel의 라우트 캐싱 기능을 활용하세요. 라우트 캐시는 애플리케이션의 모든 라우트 등록 시간을 크게 단축합니다. 라우트 캐시 생성은 다음 명령어로 실행합니다:

```shell
php artisan route:cache
```

이 명령어 실행 후, 캐시된 라우트 파일이 모든 요청에 로드되므로 라우트 등록이 빨라집니다. 라우트를 새로 추가하는 경우는 반드시 캐시를 새로 생성해야 하므로, `route:cache` 명령어는 배포 시에만 실행하는 것이 좋습니다.

라우트 캐시를 비우려면 다음 명령어를 쓰세요:

```shell
php artisan route:clear
```