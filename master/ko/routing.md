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
    - [정규 표현식 제약 조건](#parameters-regular-expression-constraints)
- [이름있는 라우트](#named-routes)
- [라우트 그룹](#route-groups)
    - [미들웨어](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [서브도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 접두사](#route-group-prefixes)
    - [라우트 이름 접두사](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암묵적 바인딩](#implicit-binding)
    - [암묵적 Enum(열거형) 바인딩](#implicit-enum-binding)
    - [명시적 바인딩](#explicit-binding)
- [폴백 라우트](#fallback-routes)
- [요율 제한(Rate Limiting)](#rate-limiting)
    - [요율 제한기 정의](#defining-rate-limiters)
    - [요율 제한기 라우트에 적용하기](#attaching-rate-limiters-to-routes)
- [폼 메서드 속이기](#form-method-spoofing)
- [현재 라우트 정보 접근하기](#accessing-the-current-route)
- [교차 출처 리소스 공유(CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

가장 기본적인 Laravel 라우트는 URI와 클로저(익명 함수)를 받아, 복잡한 라우팅 설정 파일 없이도 매우 간단하고 직관적으로 라우트 및 동작을 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일

모든 Laravel 라우트는 `routes` 디렉터리에 위치한 라우트 파일들에 정의됩니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 지정된 설정을 통해 Laravel이 자동으로 불러옵니다. `routes/web.php` 파일은 웹 인터페이스용 라우트를 정의하며, 이 라우트들은 `web` [미들웨어 그룹](/docs/master/middleware#laravels-default-middleware-groups)으로 할당되어 세션 상태 및 CSRF 보호 기능을 제공합니다.

대부분의 애플리케이션에서는 우선적으로 `routes/web.php` 파일에 라우트를 정의하게 됩니다. `routes/web.php`에 정의된 라우트는 브라우저에서 해당 라우트의 URL을 입력해 접근할 수 있습니다. 예를 들어, 다음과 같이 라우트를 정의하면 `http://example.com/user`로 브라우저에서 접속할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트

애플리케이션이 상태를 저장하지 않는 API도 제공해야 하는 경우, `install:api` Artisan 명령어를 사용해 API 라우팅을 활성화할 수 있습니다:

```shell
php artisan install:api
```

`install:api` 명령어는 [Laravel Sanctum](/docs/master/sanctum)을 설치하여, 타사 API 소비자, SPA, 모바일 앱의 인증에 사용할 수 있는 쉽고 강력한 API 토큰 인증 가드를 추가합니다. 또한, `install:api` 명령은 `routes/api.php` 파일도 생성합니다:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

`routes/api.php`의 라우트는 상태를 저장하지 않으며, `api` [미들웨어 그룹](/docs/master/middleware#laravels-default-middleware-groups)에 할당됩니다. 또한, `/api` URI 접두사가 자동으로 적용되므로, 파일 내의 모든 라우트에 직접 접두사를 추가할 필요가 없습니다. 접두사를 변경하려면 애플리케이션의 `bootstrap/app.php` 파일을 수정하세요:

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메서드

라우터는 HTTP의 다양한 메서드에 대응하는 라우트를 등록할 수 있습니다:

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

여러 HTTP 메서드에 반응하는 라우트가 필요할 때는 `match` 메서드를 사용할 수 있습니다. 혹은, 모든 HTTP 메서드에 대응하는 라우트를 등록하려면 `any` 메서드를 사용합니다:

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일한 URI에 대해 여러 라우트를 정의할 때, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트를 `any`, `match`, `redirect` 메서드를 사용하는 라우트보다 먼저 정의해야 합니다. 이렇게 해야 들어오는 요청이 올바른 라우트에 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백 시그니처에 필요한 의존성을 타입힌트로 지정하면, Laravel [서비스 컨테이너](/docs/master/container)가 해당 의존성을 자동으로 해결하여 주입해줍니다. 예를 들어, 현재 HTTP 요청을 자동으로 주입받으려면 `Illuminate\Http\Request` 클래스를 타입힌트로 지정할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 라우트로 데이터를 전송하는 모든 HTML 폼에는 반드시 CSRF 토큰 필드가 포함되어야 합니다. 그렇지 않으면 요청이 거부됩니다. CSRF 보호에 대한 더 자세한 내용은 [CSRF 문서](/docs/master/csrf)를 참고하세요:

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리다이렉트 라우트

다른 URI로 리다이렉트하는 라우트를 정의하려면, `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 단순한 리다이렉트를 위해 별도의 라우트 또는 컨트롤러를 정의하지 않아도 되는 편리한 단축 방법입니다:

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 선택적 세 번째 인자로 상태 코드를 지정해 커스터마이즈할 수도 있습니다:

```php
Route::redirect('/here', '/there', 301);
```

또는, `Route::permanentRedirect` 메서드를 사용하여 `301` 상태 코드를 직접 반환할 수 있습니다:

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리다이렉트 라우트에서 라우트 파라미터를 사용할 때, `destination`과 `status` 파라미터는 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트

라우트가 단순히 [뷰](/docs/master/views)만 반환해야 하는 경우, `Route::view` 메서드를 사용할 수 있습니다. 이 메서드는 `redirect` 메서드처럼 간단한 뷰 렌더링을 위해 라우트나 컨트롤러 전체를 정의할 필요 없이 사용할 수 있는 단축 방법입니다. `view` 메서드는 첫 번째 인자로 URI, 두 번째 인자로 뷰 이름을, 세 번째 인자로 뷰에 전달할 데이터 배열(선택)을 받습니다:

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 파라미터를 사용할 때, `view`, `data`, `status`, `headers` 파라미터는 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 확인

`route:list` Artisan 명령어를 사용하면 애플리케이션에 정의된 모든 라우트를 한눈에 확인할 수 있습니다:

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 라우트 미들웨어는 `route:list` 출력에 표시되지 않습니다. 하지만 명령어에 `-v` 옵션을 추가하면 라우트 미들웨어와 그룹명을 확인할 수 있습니다:

```shell
php artisan route:list -v

# 미들웨어 그룹까지 확장 표시하려면...
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 표시하고 싶다면 다음 명령을 사용할 수 있습니다:

```shell
php artisan route:list --path=api
```

또한, 서드파티 패키지에 의해 정의된 라우트를 숨기려면 `--except-vendor` 옵션을 사용하세요:

```shell
php artisan route:list --except-vendor
```

반대로, 서드파티 패키지에서 정의된 라우트만 보고 싶을 때는 `--only-vendor` 옵션을 사용할 수 있습니다:

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우팅 커스터마이징

기본적으로 애플리케이션의 라우트들은 `bootstrap/app.php` 파일에서 설정 및 로딩됩니다:

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

하지만 경우에 따라 애플리케이션의 특정 라우트 집합을 위해 완전히 새로운 파일을 정의해야 할 수도 있습니다. 이럴 때는 `withRouting` 메서드에 `then` 클로저를 전달할 수 있습니다. 이 클로저 안에서 필요한 추가 라우트 등록을 할 수 있습니다:

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

또는, 라우트 등록 전체를 직접 제어하고 싶을 경우 `withRouting` 메서드에 `using` 클로저를 전달할 수 있습니다. 이 인자를 전달하면 프레임워크에서 HTTP 라우트를 자동으로 등록하지 않고, 모든 라우트 등록을 직접 해야 합니다:

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

경우에 따라 URI의 특정 구간을 캡처해야 할 때가 있습니다. 예를 들면, URL에서 회원의 ID를 받아와야 할 수 있습니다. 라우트 파라미터를 정의해서 구현할 수 있습니다:

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요하다면 라우트별로 여러 개의 파라미터를 정의할 수도 있습니다:

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 파라미터는 항상 `{}` 중괄호로 감싸며, 알파벳 문자로만 구성되어야 합니다. 파라미터 이름에 밑줄(`_`)도 사용할 수 있습니다. 라우트 파라미터는 정의된 순서에 따라 경로 콜백이나 컨트롤러에 주입되며, 콜백/컨트롤러에서 사용하는 변수명과는 무관하게 동작합니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입

라우트에서 서비스 컨테이너가 자동으로 주입해주길 원하는 의존성이 있다면, 라우트 파라미터를 그 뒤에 위치시켜야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 파라미터

경우에 따라 URI에 파라미터가 반드시 항상 존재하지 않아도 되는 라우트가 필요할 수 있습니다. 파라미터 이름 뒤에 `?`를 붙여서 선택적으로 만들 수 있습니다. 이때, 라우트 콜백의 해당 변수에 기본값을 지정해야 합니다:

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

라우트 인스턴스의 `where` 메서드를 사용하여 라우트 파라미터의 형식을 제약할 수 있습니다. `where` 메서드는 파라미터 이름과 정규 표현식을 인자로 받습니다:

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

자주 사용되는 정규 표현식 패턴은 헬퍼 메서드를 사용해 보다 쉽게 추가할 수 있습니다:

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

들어오는 요청이 라우트 패턴 제약 조건과 맞지 않으면 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 글로벌 제약 조건

특정 라우트 파라미터에 항상 동일한 정규 표현식 제약을 적용하려면, `pattern` 메서드를 사용할 수 있습니다. 이러한 패턴은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의하세요:

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

이제 해당 파라미터 이름을 사용하는 모든 라우트에 패턴이 자동으로 적용됩니다:

```php
Route::get('/user/{id}', function (string $id) {
    // {id}가 숫자일 때만 실행됩니다...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시(/) 사용

Laravel 라우터는 라우트 파라미터 값에 `/`를 제외한 모든 문자를 허용합니다. 만약 `/` 문자를 플레이스홀더의 일부로 허용해야 한다면, `where` 조건 정규 표현식으로 명시적으로 허용해야 합니다:

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 반드시 라우트의 마지막 세그먼트에서만 사용할 수 있습니다.

<a name="named-routes"></a>
## 이름있는 라우트 (Named Routes)

이름있는 라우트는 특정 라우트를 쉽게 URL로 생성하거나 리다이렉션할 수 있도록 해줍니다. `name` 메서드를 체이닝하여 라우트에 이름을 지정할 수 있습니다:

```php
Route::get('/user/profile', function () {
    // ...
})->name('profile');
```

컨트롤러 액션에 대해서도 라우트 이름을 지정할 수 있습니다:

```php
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!WARNING]
> 라우트 이름은 반드시 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 이름있는 라우트의 URL 생성

라우트에 이름을 지정했다면, Laravel의 `route` 및 `redirect` 헬퍼 함수에서 라우트 이름을 사용해 URL이나 리다이렉트를 생성할 수 있습니다:

```php
// URL 생성...
$url = route('profile');

// 리다이렉트 생성...
return redirect()->route('profile');

return to_route('profile');
```

만약 이름있는 라우트가 파라미터를 필요로 한다면, 이를 두 번째 인자로 배열로 전달하면 자동으로 URL의 적절한 위치에 해당 값이 삽입됩니다:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

배열에 추가적인 파라미터를 포함하면, 해당 키/값 쌍이 URL의 쿼리스트링에 자동으로 추가됩니다:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// http://example.com/user/1/profile?photos=yes
```

> [!NOTE]
> URL 파라미터에 대해 애플리케이션 전체에서 기본값을 지정하고 싶다면 [URL::defaults 메서드](/docs/master/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 검사

현재 요청이 특정 이름의 라우트에 매칭되었는지 확인하려면, Route 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어, 라우트 미들웨어에서 현재 라우트 이름을 검사하고 싶을 때 아래와 같이 쓸 수 있습니다:

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

라우트 그룹을 사용하면 여러 라우트에 걸쳐 동일한 라우트 속성(예: 미들웨어 등)을 중복 없이 한 번에 적용할 수 있습니다.

중첩된 그룹은 부모 그룹의 속성과 병합되어 동작합니다. 미들웨어와 `where` 조건은 병합되지만, 라우트 이름과 접두사는 덧붙여집니다. 네임스페이스 구분자와 URI 접두사의 슬래시는 적절하게 자동 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

[미들웨어](/docs/master/middleware)를 그룹 내 모든 라우트에 적용하려면, 그룹 정의 이전에 `middleware` 메서드를 사용하면 됩니다. 미들웨어는 배열에 지정된 순서대로 실행됩니다:

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first & second 미들웨어 사용...
    });

    Route::get('/user/profile', function () {
        // first & second 미들웨어 사용...
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러

동일한 [컨트롤러](/docs/master/controllers)를 사용하는 라우트 그룹이 있다면, `controller` 메서드를 통해 그룹 전체에 공통 컨트롤러를 지정할 수 있습니다. 이후 개별 라우트 정의 시에는 컨트롤러 메서드 이름만 지정하면 됩니다:

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹은 서브도메인 라우팅에도 사용할 수 있습니다. 서브도메인에서도 URI 파라미터와 동일하게 파라미터를 지정해, 라우트나 컨트롤러에서 사용할 수 있습니다. 서브도메인은 그룹 정의 전에 `domain` 메서드를 호출하여 지정합니다:

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

<a name="route-group-prefixes"></a>
### 라우트 접두사

`prefix` 메서드를 통해 그룹 내 각 라우트 URI 앞에 접두사를 붙일 수 있습니다. 예를 들어, 그룹 내 모든 라우트의 앞에 `admin`을 접두사로 붙일 수 있습니다:

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL과 매칭됩니다
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두사

`name` 메서드를 사용해 그룹 내 모든 라우트 이름에 접두사를 붙일 수 있습니다. 예를 들어, 그룹 내 모든 라우트 이름에 `admin`을 접두사로 붙이고 싶다면 아래와 같이 합니다. 지정한 문자열이 정확히 접두사로 사용되므로, 보통 마지막에 `.`를 붙입니다:

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // "admin.users" 라우트 이름이 할당됩니다...
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

라우트나 컨트롤러 액션에 모델 ID를 전달하는 경우, 해당 ID에 해당하는 모델을 데이터베이스에서 조회하는 로직이 자주 반복됩니다. Laravel의 라우트 모델 바인딩은 이런 과정을 자동화하여, 특정 ID에 해당하는 모델 인스턴스를 라우트에 바로 주입할 수 있도록 도와줍니다. 즉, 사용자의 ID 대신 해당 `User` 모델 전체 인스턴스를 직접 주입받을 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩

라우트 또는 컨트롤러 액션의 타입힌트된 변수명이 라우트 세그먼트 이름과 일치할 경우, Laravel은 해당 Eloquent 모델을 자동으로 해결합니다. 예시:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

위 코드에서 `$user` 변수가 `App\Models\User` Eloquent 모델로 타입힌트되고, 변수명이 `{user}` URI 세그먼트와 일치하므로, Laravel은 요청 URI에서 해당 값(ID)에 해당하는 모델 인스턴스를 자동으로 주입합니다. 만약 데이터베이스에서 일치하는 모델 인스턴스를 찾지 못할 경우, 404 HTTP 응답이 자동으로 반환됩니다.

마찬가지로 컨트롤러 메서드에서도 암묵적 바인딩이 동작합니다. `{user}` URI 세그먼트가 컨트롤러의 `$user` 변수와 일치하며, 이는 `App\Models\User` 타입힌트가 있습니다:

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
#### 소프트 삭제(Soft Deleted) 모델

기본적으로 암묵적 모델 바인딩은 [소프트 삭제](/docs/master/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 그러나 라우트 정의에 `withTrashed` 메서드를 체이닝하면, 소프트 삭제된 모델도 조회할 수 있습니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 커스터마이징

때로는 모델을 조회할 때 `id` 컬럼이 아닌 다른 컬럼을 사용하고 싶을 수 있습니다. 이럴 때는 라우트 파라미터 정의 시 컬럼명을 직접 명시하면 됩니다:

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

또는, Eloquent 모델에 `getRouteKeyName` 메서드를 오버라이드하면, 해당 모델 클래스가 항상 특정 컬럼을 기본 키로 사용하게 할 수 있습니다:

```php
/**
 * 모델의 라우트 키를 반환합니다.
 */
public function getRouteKeyName(): string
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
#### 커스텀 키와 스코핑(Scoping)

하나의 라우트에서 여러 Eloquent 모델을 암묵적으로 바인딩할 때, 두 번째 모델이 앞선 모델의 "자식"임을 보장해야 할 수도 있습니다. 예를 들어, 특정 사용자의 블로그 포스트를 슬러그로 조회하는 경우를 생각해봅시다:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

이처럼 중첩된 라우트 파라미터에서 커스텀 키 암묵적 바인딩을 사용할 경우, Laravel은 부모 모델에서 자식 모델을 조회하도록 쿼리를 자동으로 스코프합니다. 위 예시는 `User` 모델이 `posts`라는 연관관계를 가졌다고 가정합니다.

필요하다면, 커스텀 키를 지정하지 않아도 "자식" 모델 바인딩을 스코핑하도록 `scopeBindings` 메서드를 사용할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는, 라우트 그룹 전체에 스코프 바인딩을 적용할 수 있습니다:

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로, `withoutScopedBindings` 메서드를 사용해 스코프 바인딩을 명시적으로 적용하지 않을 수도 있습니다:

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 누락된 모델에 대한 동작 커스터마이징

일반적으로, 암묵적으로 바인딩된 모델을 찾지 못하면 404 HTTP 응답이 반환됩니다. 하지만, `missing` 메서드로 라우트 정의 시 커스텀 동작을 정의할 수 있습니다. `missing` 메서드는 모델을 찾지 못했을 때 호출되는 클로저를 인자로 받습니다:

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
### 암묵적 Enum(열거형) 바인딩

PHP 8.1부터 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)이 도입되었습니다. 이를 지원하기 위해, Laravel은 [문자열 기반 Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 라우트에서 타입힌트로 지정하면 해당 세그먼트가 Enum 값과 일치할 때만 라우트를 실행합니다. 불일치 시, 404 HTTP 응답이 반환됩니다. 예시로 아래와 같은 Enum이 있다고 가정합니다:

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

이제 `{category}`가 `fruits` 또는 `people`일 때만 라우트가 실행됩니다. 그 외 값이 입력되면 404 응답이 반환됩니다:

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩

반드시 Laravel의 암묵적(컨벤션 기반) 모델 해결만 사용할 필요는 없습니다. 명시적으로 라우트 파라미터와 모델의 매핑 방식을 정의할 수도 있습니다. 명시적 바인딩을 등록하려면, 라우터의 `model` 메서드를 사용해 각 파라미터에 대해 클래스를 지정하세요. 이러한 명시적 모델 바인딩은 `AppServiceProvider` 클래스의 `boot` 메서드 초반에 정의하는 것이 좋습니다:

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

다음으로, `{user}` 파라미터가 포함된 라우트를 정의합니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

이제 `{user}` 파라미터는 항상 `App\Models\User` 모델과 바인딩되어, 예를 들어 `users/1` 요청에 대해 데이터베이스에서 ID가 `1`인 User 인스턴스가 주입됩니다.

일치하는 모델 인스턴스를 찾지 못하면 404 HTTP 응답이 자동으로 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 로직 커스터마이징

모델 바인딩의 해석 방식을 직접 정의하고 싶을 땐, `Route::bind` 메서드를 사용할 수 있습니다. 이때 전달하는 클로저는 URI 세그먼트 값을 받아, 라우트에 주입해야 하는 모델 인스턴스를 반환해야 합니다. 이 커스터마이징 역시 애플리케이션의 `AppServiceProvider` 클래스 `boot` 메서드에서 정의하세요:

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

또는, Eloquent 모델에서 `resolveRouteBinding` 메서드를 오버라이드해 바인딩 로직을 구현할 수 있습니다. 이 메서드는 URI 세그먼트 값을 받아, 라우트에 주입할 인스턴스를 반환해야 합니다:

```php
/**
 * 주어진 값에 해당하는 모델을 반환합니다.
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

라우트가 [암묵적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용 중이라면, 부모 모델의 자식 바인딩을 위해 `resolveChildRouteBinding` 메서드가 사용됩니다:

```php
/**
 * 바인딩된 값에 대한 자식 모델을 반환합니다.
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

`Route::fallback` 메서드를 사용하면, 들어오는 요청과 일치하는 다른 라우트가 없을 때 실행되는 라우트를 정의할 수 있습니다. 일반적으로, 처리되지 않은 요청은 애플리케이션의 예외 핸들러를 통해 자동으로 "404" 페이지가 렌더링됩니다. 하지만 대체로 `fallback` 라우트는 `routes/web.php` 파일 내에 정의하므로, `web` 미들웨어 그룹의 모든 미들웨어가 이 라우트에도 적용됩니다. 추가 미들웨어도 자유롭게 붙일 수 있습니다:

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 요율 제한 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 요율 제한기 정의

Laravel은 특정 라우트나 라우트 그룹에 대해 트래픽을 제어할 수 있는 강력하고 사용자 정의가 가능한 요율 제한(Rate Limiting) 기능을 제공합니다. 애플리케이션의 요구 사항에 맞는 요율 제한기를 먼저 정의해야 합니다.

요율 제한기는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 정의할 수 있습니다:

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

요율 제한기는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다. `for` 메서드는 제한기의 이름과, 특정 제한 구성(Limit)을 반환하는 클로저를 인자로 받습니다. 제한 구성은 `Illuminate\Cache\RateLimiting\Limit` 클래스 인스턴스로, 다양한 빌더 메서드를 제공하여 손쉽게 제한 정의가 가능합니다. 제한기 이름은 임의의 문자열을 사용해도 됩니다:

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

지정한 요율 제한을 초과하면 Laravel이 자동으로 429 HTTP 상태 코드와 함께 응답을 반환합니다. 요율 제한을 초과했을 때 커스텀 응답을 반환하고 싶다면, `response` 메서드를 사용할 수 있습니다:

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

요율 제한기 콜백은 들어오는 HTTP 요청 인스턴스를 받으므로, 인증 사용자나 요청에 따라 제약을 동적으로 설정할 수도 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()?->vipCustomer()
        ? Limit::none()
        : Limit::perHour(10);
});
```

<a name="segmenting-rate-limits"></a>
#### 요율 제한 세분화(Segmenting)

경우에 따라, 특정 기준값(예: IP 주소)별로 요율 제한을 세분화하고 싶을 수 있습니다. 예를 들어, 동일한 라우트에 대해 IP별로 분당 100회를 허용하려면 `by` 메서드를 사용하세요:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

좀 더 복잡한 예시로, 인증 사용자는 ID별 분당 100회, 비로그인 사용자는 IP별 분당 10회 제한하는 것도 가능합니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 다중 요율 제한

필요하다면, 하나의 제한 구성에서 여러 개의 요율 제한을 배열로 반환할 수도 있습니다. 배열 내에 배치된 순서대로 각 제한이 평가됩니다:

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

동일한 `by` 값을 사용하는 다중 제한기를 할당할 경우, 각 `by` 값이 고유해야 합니다. 가장 쉬운 방법은 `by` 메서드에 전달하는 값에 접두사를 붙이는 것입니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="response-base-rate-limiting"></a>
#### 응답 기반 요율 제한

들어오는 요청뿐만 아니라, 응답을 기준으로 요율 제한을 걸 수도 있습니다. `after` 메서드를 사용하면 특정 응답에만 요율 제한을 적용할 수 있습니다. 예를 들어, 유효성 검증 실패나 404 응답 등 특정 HTTP 상태 코드에만 카운트하도록 할 수 있습니다.

`after` 메서드는 응답을 받는 클로저를 받아, 반환값이 `true`일 때만 카운트하도록 동작합니다. 이는 연속된 404 응답의 나쁜 의도(Enumeration 공격 등)를 막거나, 유효성 검사에 실패한 요청은 요율 제한에 카운트하지 않도록 할 때 유용하게 쓰입니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Symfony\Component\HttpFoundation\Response;

RateLimiter::for('resource-not-found', function (Request $request) {
    return Limit::perMinute(10)
        ->by($request->user()?->id ?: $request->ip())
        ->after(function (Response $response) {
            // 404 응답만 카운트하도록 설정(Enumeration 방지)
            return $response->status() === 404;
        });
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 요율 제한기 적용하기

요율 제한기는 `throttle` [미들웨어](/docs/master/middleware)를 사용해 라우트나 라우트 그룹에 적용할 수 있습니다. throttle 미들웨어는 제한기 이름을 인자로 받습니다:

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
#### Redis로 요율 제한하기

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스에 매핑되어 있습니다. 하지만 애플리케이션의 캐시 드라이버로 Redis를 사용한다면, 요율 제한 관리에 Redis를 사용하도록 Laravel에 지시할 수 있습니다. 이를 위해 `bootstrap/app.php` 파일의 미들웨어 설정에 `throttleWithRedis` 메서드를 사용하세요. 이 메서드는 `throttle` 미들웨어를 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis`로 매핑합니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 폼 메서드 속이기 (Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 액션을 지원하지 않습니다. 따라서, HTML 폼에서 `PUT`, `PATCH`, `DELETE` 라우트를 호출하려면 폼에 숨겨진 `_method` 필드를 추가해야 합니다. 이 필드의 값이 실제 HTTP 요청 메서드로 사용됩니다:

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

편리하게도, [Blade 지시문](/docs/master/blade)인 `@method`를 사용해 `_method` 입력 필드를 생성할 수 있습니다:

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 정보 접근하기 (Accessing the Current Route)

들어오는 요청을 처리하는 라우트 정보를 확인하려면, `Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

라우터 및 라우트 클래스에서 사용할 수 있는 모든 메서드는 [Route 파사드의 기본 클래스](https://api.laravel.com/docs/master/Illuminate/Routing/Router.html) 및 [Route 인스턴스](https://api.laravel.com/docs/master/Illuminate/Routing/Route.html) API 문서를 참고하세요.

<a name="cors"></a>
## 교차 출처 리소스 공유(CORS) (Cross-Origin Resource Sharing, CORS)

Laravel은 설정값에 따라 CORS `OPTIONS` HTTP 요청에 자동으로 응답할 수 있습니다. 이러한 `OPTIONS` 요청은 글로벌 미들웨어 스택에 자동 포함된 `HandleCors` [미들웨어](/docs/master/middleware)를 통해 처리됩니다.

애플리케이션의 CORS 설정값을 커스터마이즈해야 할 때는, `config:publish` Artisan 명령어로 `cors` 설정 파일을 퍼블리시할 수 있습니다:

```shell
php artisan config:publish cors
```

이 명령은 애플리케이션의 `config` 디렉터리에 `cors.php` 설정 파일을 생성합니다.

> [!NOTE]
> CORS 및 CORS 헤더에 대한 자세한 내용은 [MDN 웹 문서의 CORS 설명서](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

애플리케이션을 프로덕션 환경에 배포할 때는, Laravel의 라우트 캐시 기능을 활용하는 것이 좋습니다. 라우트 캐시를 사용하면 등록된 모든 라우트를 불러오는 속도가 크게 향상됩니다. 라우트 캐시를 생성하려면 `route:cache` Artisan 명령어를 실행하세요:

```shell
php artisan route:cache
```

이 명령 실행 후, 요청마다 캐시된 라우트 파일이 로드됩니다. 새로운 라우트를 추가할 경우 반드시 라우트 캐시를 새로 생성해야 함에 유의하세요. 따라서 `route:cache` 명령은 프로젝트 배포 과정에서만 실행하는 것이 적합합니다.

라우트 캐시는 `route:clear` 명령어로 삭제할 수 있습니다:

```shell
php artisan route:clear
```
