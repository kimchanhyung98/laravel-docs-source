# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리디렉션 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록 확인](#listing-your-routes)
    - [라우팅 커스터마이징](#routing-customization)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [선택적 파라미터](#parameters-optional-parameters)
    - [정규 표현식 제약조건](#parameters-regular-expression-constraints)
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
- [속도 제한(Rate Limiting)](#rate-limiting)
    - [속도 제한자 정의](#defining-rate-limiters)
    - [라우트에 속도 제한 적용](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 정보 접근](#accessing-the-current-route)
- [교차 출처 리소스 공유(CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

가장 기본적인 Laravel 라우트는 URI와 클로저(익명 함수)를 받아, 복잡한 라우팅 설정 파일 없이도 매우 간단하고 표현력 높게 라우트와 동작을 정의할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일

Laravel의 모든 라우트는 `routes` 디렉토리 내의 라우트 파일에 정의됩니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에서 지정된 설정에 따라 Laravel이 자동으로 로드합니다. `routes/web.php` 파일은 웹 인터페이스를 위한 라우트를 정의하며, 이 라우트에는 세션 상태, CSRF 보호 등 다양한 기능을 제공하는 `web` [미들웨어 그룹](/docs/12.x/middleware#laravels-default-middleware-groups)이 자동으로 할당됩니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에 라우트를 정의하는 것부터 시작합니다. 이 파일에서 정의한 라우트는 해당 URL을 브라우저에 입력하면 접근할 수 있습니다. 예를 들어, 아래의 라우트는 브라우저에서 `http://example.com/user`에 접속하면 실행됩니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트

애플리케이션에서 상태를 저장하지 않는 API를 제공하려는 경우, `install:api` Artisan 명령어로 API 라우팅을 활성화할 수 있습니다.

```shell
php artisan install:api
```

`install:api` 명령어는 [Laravel Sanctum](/docs/12.x/sanctum)을 설치하여, 타사 API 소비자, SPA, 모바일 애플리케이션 등에서 사용할 수 있는 간단하면서도 강력한 API 토큰 인증 가드를 제공합니다. 또한 이 명령어는 `routes/api.php` 파일을 생성합니다.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

`routes/api.php`에 정의된 라우트는 상태를 저장하지 않으며, `api` [미들웨어 그룹](/docs/12.x/middleware#laravels-default-middleware-groups)에 할당됩니다. 또한 이 파일의 모든 라우트에는 `/api` URI 접두사가 자동으로 적용되므로, 매 라우트마다 접두사를 따로 지정할 필요가 없습니다. 접두사를 변경하려면 애플리케이션의 `bootstrap/app.php` 파일을 수정하면 됩니다.

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메서드

라우터는 임의의 HTTP 메서드에 응답하는 라우트를 등록할 수 있도록 지원합니다.

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

여러 HTTP 메서드에 응답하는 라우트를 등록해야 할 때는 `match` 메서드를 사용할 수 있습니다. 또는 모든 HTTP 메서드에 응답하는 라우트를 등록하려면 `any` 메서드를 사용할 수도 있습니다.

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일한 URI를 공유하는 여러 라우트를 정의할 때, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트를 반드시 `any`, `match`, `redirect` 메서드를 사용하는 라우트보다 먼저 정의해야 합니다. 이렇게 하면 요청이 올바른 라우트에 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백 시그니처에 필요한 의존성을 타입힌트로 명시하면, [서비스 컨테이너](/docs/12.x/container)가 해당 의존성을 자동으로 주입해줍니다. 예를 들어, `Illuminate\Http\Request` 클래스를 타입힌트로 지정하면 현재 HTTP 요청 객체가 콜백에 자동으로 주입됩니다.

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에서 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 타입의 라우트로 데이터를 전송하는 모든 HTML 폼에는 반드시 CSRF 토큰 필드를 포함해야 합니다. 그렇지 않으면 요청이 거부됩니다. CSRF 보호에 관해서는 [CSRF 문서](/docs/12.x/csrf)를 참고하시기 바랍니다.

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리디렉션 라우트

다른 URI로 리디렉션하는 라우트를 정의할 때는 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 단순한 리디렉션을 위해 전체 라우트나 컨트롤러를 별도로 정의하지 않아도 되는 편리한 단축 메서드입니다.

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 선택적으로 세 번째 인자를 통해 상태 코드를 지정할 수 있습니다.

```php
Route::redirect('/here', '/there', 301);
```

또는, `Route::permanentRedirect` 메서드를 사용하여 항상 `301` 상태 코드를 반환하도록 할 수도 있습니다.

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리디렉션 라우트에서 라우트 파라미터를 사용할 때, `destination`과 `status` 파라미터는 Laravel에서 예약어로 사용되므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트

해당 라우트가 [뷰](/docs/12.x/views)만 반환하면 되도록 해야 할 경우, `Route::view` 메서드를 사용할 수 있습니다. 이 메서드는 `redirect`와 마찬가지로 간단한 단축 메서드를 제공하여 전체 라우트 또는 컨트롤러 정의 없이 사용할 수 있습니다. 첫 번째 인자는 URI, 두 번째 인자는 뷰 이름, 세 번째 인자로 뷰에 전달할 데이터 배열을 선택적으로 지정할 수 있습니다.

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 파라미터를 사용할 때, `view`, `data`, `status`, `headers` 파라미터는 Laravel에서 예약어로 사용되므로 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 확인

`route:list` Artisan 명령어를 사용하면, 애플리케이션에 정의된 모든 라우트 개요를 쉽게 확인할 수 있습니다.

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 미들웨어는 `route:list` 결과에 표시되지 않지만, 명령어 뒤에 `-v` 옵션을 추가하면 미들웨어 및 미들웨어 그룹 이름이 함께 표기됩니다.

```shell
php artisan route:list -v

# 미들웨어 그룹 확장 표시...
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 표시하고 싶을 때는 `--path` 옵션을 사용할 수 있습니다.

```shell
php artisan route:list --path=api
```

또한, `route:list` 명령어 실행 시 `--except-vendor` 옵션을 지정하면, 서드파티 패키지에서 정의된 라우트는 목록에서 제외됩니다.

```shell
php artisan route:list --except-vendor
```

반대로, `--only-vendor` 옵션을 사용하면 서드파티 패키지 라우트만 표시할 수 있습니다.

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우팅 커스터마이징

기본적으로, 애플리케이션의 라우트는 `bootstrap/app.php` 파일에서 설정 및 로드됩니다.

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

단, 특정 라우트 집합을 별도의 파일로 분리해야 할 경우, `withRouting` 메서드에 `then` 클로저를 제공하여 추가 라우트를 등록할 수 있습니다.

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

또한, 라우트 등록 절차 전반을 직접 제어해야 할 경우, `withRouting`의 `using` 클로저를 이용할 수 있습니다. 이 인자를 전달하면, 프레임워크에서 아무런 HTTP 라우트도 등록하지 않으며 개발자가 모든 라우트 등록을 직접 처리해야 합니다.

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

경우에 따라 라우트 URI의 일부를 파라미터로 캡처해야 할 때가 있습니다. 예를 들어, URL에서 사용자의 ID를 가져와야 할 경우 라우트 파라미터를 정의할 수 있습니다.

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

라우트에 필요한 만큼 여러 개의 파라미터를 정의할 수도 있습니다.

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 파라미터는 항상 `{}` 중괄호로 감싸서 정의하며, 알파벳 문자로만 이루어져야 합니다. 파라미터 이름에 언더스코어(`_`)도 사용할 수 있습니다. 라우트 파라미터는 콜백 또는 컨트롤러로 전달될 때 선언 순서대로 주입되며, 변수명은 중요하지 않습니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입

라우트에 의존성 주입이 필요한 경우, 라우트 파라미터는 의존성 뒤에 나열해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 파라미터

가끔 URI에 항상 존재하지 않는 라우트 파라미터를 명시해야 할 경우, 파라미터 이름 뒤에 `?`를 붙여 선택적으로 만들 수 있습니다. 이때 해당 변수에는 기본값을 제공해야 합니다.

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규 표현식 제약조건

라우트 파라미터의 형식을 정규 표현식을 사용하여 `where` 메서드로 제약할 수 있습니다. `where` 메서드에는 파라미터 이름과 제약할 정규 표현식을 인자로 전달합니다.

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

자주 사용되는 정규식 패턴은 헬퍼 메서드를 통해 더 빠르게 패턴 제약을 추가할 수 있습니다.

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

요청이 라우트의 패턴 제약조건과 일치하지 않으면 HTTP 404 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 글로벌 제약조건

기본적으로 특정 파라미터 이름에 대해 항상 적용될 정규 표현식을 지정하려면 `pattern` 메서드를 사용할 수 있습니다. 이러한 패턴은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의하면 됩니다.

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

패턴을 정의하면, 해당 파라미터 이름에 적용된 모든 라우트에서 자동으로 이 패턴이 적용됩니다.

```php
Route::get('/user/{id}', function (string $id) {
    // {id}가 숫자일 때만 실행!
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시(Forward Slash) 허용

Laravel 라우팅 컴포넌트는 `/`를 제외한 모든 문자를 파라미터 값으로 허용합니다. `/`를 포함해야 한다면 `where` 정규식을 사용해 직접 허용해야 합니다.

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 반드시 마지막 라우트 세그먼트에서만 지원됩니다.

<a name="named-routes"></a>
## 네임드 라우트 (Named Routes)

네임드 라우트는 특정 라우트에 대해 URL이나 리디렉션을 간편하게 생성할 수 있도록 해줍니다. 라우트 정의 뒤에 `name` 메서드를 연결하여 라우트에 이름을 지정할 수 있습니다.

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
> 라우트 이름은 반드시 고유하게 지정해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 네임드 라우트로 URL 생성

특정 라우트에 이름을 지정하면, 이후 Laravel의 `route` 및 `redirect` 헬퍼 함수를 사용하여 해당 이름으로 URL이나 리디렉션을 생성할 수 있습니다.

```php
// URL 생성...
$url = route('profile');

// 리디렉션 생성...
return redirect()->route('profile');

return to_route('profile');
```

네임드 라우트에 파라미터가 정의되어 있다면, 두 번째 인자로 파라미터를 배열로 전달할 수 있습니다. 전달한 파라미터는 자동으로 URL 내의 올바른 위치에 삽입됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

추가로 배열에 파라미터를 더 전달하면 키/값 쌍이 생성되는 쿼리 문자열로 자동 추가됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// http://example.com/user/1/profile?photos=yes
```

> [!NOTE]
> 가끔, 현재 로케일 등 URL 파라미터에 대해 요청 전체에 적용할 기본값을 지정하고 싶을 때가 있습니다. 이럴 땐 [URL::defaults 메서드](/docs/12.x/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 확인

현재 요청이 특정 네임드 라우트에 매칭되었는지 확인하려면, Route 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어, 미들웨어 내에서 현재 라우트 이름을 확인하려면 아래와 같이 사용합니다.

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

라우트 그룹을 사용하면 여러 개의 라우트에 같은 속성(예: 미들웨어 등)을 중복 정의하지 않고 한번에 적용할 수 있습니다.

중첩된 그룹의 경우, 부모 그룹의 속성과 지능적으로 병합합니다. 미들웨어와 `where` 조건은 병합되며, 이름과 접두사는 각각 이어 붙여집니다. 네임스페이스 구분자, URI 접두사 슬래시는 적절히 자동 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

라우트 그룹 내의 모든 라우트에 [미들웨어](/docs/12.x/middleware)를 적용하려면 `middleware` 메서드를 사용합니다. 배열에 나열된 순서대로 미들웨어가 실행됩니다.

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first & second 미들웨어가 적용됩니다...
    });

    Route::get('/user/profile', function () {
        // first & second 미들웨어가 적용됩니다...
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러

여러 라우트가 동일한 [컨트롤러](/docs/12.x/controllers)를 사용할 경우, `controller` 메서드로 그룹 전체에 컨트롤러를 지정할 수 있습니다. 이후 각 라우트에는 해당 컨트롤러의 메서드명만 지정하면 됩니다.

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹은 서브도메인 라우팅을 처리하는 데도 사용할 수 있습니다. 서브도메인에도 라우트 파라미터를 할당할 수 있으므로, URI 파라미터처럼 라우트 또는 컨트롤러에서 해당 값을 사용할 수 있습니다. 서브도메인은 그룹을 정의하기 전에 `domain` 메서드로 지정합니다.

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

> [!WARNING]
> 서브도메인 라우트가 올바르게 매칭되도록 하려면, 반드시 서브도메인 라우트를 루트 도메인 라우트보다 먼저 등록해야 합니다. 그렇지 않으면 경로가 동일한 경우 루트 도메인 라우트가 서브도메인 라우트를 덮어쓸 수 있습니다.

<a name="route-group-prefixes"></a>
### 라우트 접두사

`prefix` 메서드를 사용하면 그룹 내의 모든 라우트 URI에 지정한 접두사를 자동으로 추가할 수 있습니다. 예를 들어, 모든 라우트 URI에 `admin` 접두사를 붙이고 싶다면 아래와 같이 작성합니다.

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL과 매칭됩니다
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두사

`name` 메서드를 사용하면 그룹 내의 모든 라우트 이름에 지정한 접두사를 자동으로 붙일 수 있습니다. 예를 들어, `admin` 접두사를 모든 라우트 이름 앞에 추가하려면 아래와 같이 작성합니다. 접두사는 마지막에 점(`.`)이 포함되어야 하니 주의하세요.

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // "admin.users"라는 라우트 이름이 할당됨
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

라우트나 컨트롤러 액션에 모델 ID를 주입할 때 보통 데이터베이스에서 해당 모델을 조회해야 합니다. 라우트 모델 바인딩을 사용하면 이러한 모델 인스턴스를 라우트에 자동으로 주입할 수 있습니다. 예를 들어, 사용자 ID 대신 해당하는 `User` 모델 전체 인스턴스를 주입받을 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩

라우트 또는 컨트롤러 액션에서 타입힌트된 변수 이름이 라우트 세그먼트 이름과 일치하면, Laravel은 해당 Eloquent 모델을 자동으로 조회하여 주입합니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

위 예제에서 `$user`는 `App\Models\User`으로 타입힌트되어 있고, 변수명도 `{user}`와 일치하므로, URI 값과 일치하는 ID를 가진 User 인스턴스가 자동으로 주입됩니다. 만약 일치하는 모델 인스턴스가 데이터베이스에 없으면 HTTP 404 응답이 자동 반환됩니다.

당연히, 컨트롤러 메서드에서도 암묵적 바인딩을 사용할 수 있습니다. 이 때도 `{user}` URI 세그먼트와 컨트롤러의 `$user` 파라미터의 이름이 일치해야 합니다.

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

일반적으로 암묵적 모델 바인딩은 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 그러나 라우트 정의에 `withTrashed` 메서드를 추가하여 소프트 삭제된 모델도 조회하도록 할 수 있습니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 커스터마이징

특정 컬럼(예: `id`가 아닌 `slug`)으로 Eloquent 모델을 조회하여 바인딩하고 싶을 때는, 라우트 파라미터 정의에서 해당 컬럼을 지정할 수 있습니다.

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

특정 모델 클래스가 항상 `id`가 아닌 다른 컬럼으로 바인딩되기를 원한다면, Eloquent 모델에서 `getRouteKeyName` 메서드를 오버라이드하면 됩니다.

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

여러 Eloquent 모델을 한 라우트에서 암묵적으로 바인딩할 때, 두 번째 모델이 첫 번째 모델의 하위(연관)가 되어야 한다면 아래와 같이 사용할 수 있습니다. 예를 들어, 특정 사용자의 블로그 포스트를 슬러그로 받아오는 경우입니다.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

커스텀 키가 nested 파라미터로 주어지면, Laravel은 관례에 따라 부모와의 연관관계명을 추측하여 하위 모델을 부모 기준으로 쿼리합니다. 위 예제의 경우 User 모델에 `posts` 연관관계가 있다고 가정하여 Post를 조회합니다.

커스텀 키가 없어도 하위 바인딩을 스코프하도록 지시하려면 라우트 정의에 `scopeBindings` 메서드를 사용할 수 있습니다.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는 라우트 그룹 전체에 스코프 바인딩을 적용할 수도 있습니다.

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로, `withoutScopedBindings` 메서드로 스코프 바인딩을 비활성화할 수도 있습니다.

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 존재하지 않는 모델에 대한 커스텀 동작

보통 암묵적 바인딩에서 모델을 찾지 못하면 HTTP 404 응답이 반환됩니다. 해당 동작을 커스터마이징하고 싶다면 `missing` 메서드를 통해 클로저를 지정할 수 있습니다. 모델을 찾을 수 없을 때 이 클로저가 실행됩니다.

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

PHP 8.1부터 지원되는 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php) 기능에 따라, Laravel에서는 [문자열 기반 Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 타입힌트로 지정하면 해당 값이 유효할 때만 라우트가 동작하고, 그렇지 않으면 HTTP 404 응답이 반환됩니다. 예를 들어 아래와 같은 Enum이 있다고 가정합니다.

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

이제 `{category}` 라우트 세그먼트가 `fruits` 또는 `people`일 경우에만 라우트가 동작합니다. 그렇지 않으면 404가 반환됩니다.

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩

Laravel의 암묵적(Convention 기반) 모델 바인딩을 반드시 사용할 필요는 없습니다. 명시적으로 라우트 파라미터가 어떤 모델과 매핑되는지 직접 정의할 수도 있습니다. 명시적 바인딩을 등록하려면, 라우터의 `model` 메서드를 사용하여 파라미터명과 모델 클래스를 지정하면 됩니다. 이 코드는 `AppServiceProvider` 클래스의 `boot` 메서드 초반에 위치해야 합니다.

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

그리고 `{user}` 파라미터를 가진 라우트를 정의합니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

이제 모든 `{user}` 파라미터는 자동으로 `App\Models\User` 인스턴스와 바인딩됩니다. 예를 들어 `users/1` 요청 시 데이터베이스에서 ID가 1인 User 인스턴스가 주입됩니다.

일치하는 모델 인스턴스가 없으면 HTTP 404 응답이 자동 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 해석 논리 커스터마이징

바인딩 모델을 찾아주는 로직을 직접 정의하려면 `Route::bind` 메서드를 사용할 수 있습니다. 이 때 전달하는 클로저는 URI 세그먼트 값을 받아 해당 클래스 인스턴스를 반환해야 합니다. 역시 이 코드는 `AppServiceProvider`의 `boot` 메서드에서 작성해야 합니다.

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

또는, Eloquent 모델에서 `resolveRouteBinding` 메서드를 오버라이드하여 바인딩 로직을 지정할 수도 있습니다.

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

라우트에서 [암묵적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용하는 경우, `resolveChildRouteBinding` 메서드로 자식 바인딩 해석이 처리됩니다.

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

`Route::fallback` 메서드를 사용하면, 다른 라우트와 매칭되지 않는 모든 요청에 적용될 폴백 라우트를 정의할 수 있습니다. 보통은 처리되지 않은 요청이 예외 핸들러를 통해 "404" 페이지를 보여주게 되어 있지만, 주로 `routes/web.php`에 폴백 라우트를 정의하면 `web` 미들웨어 그룹이 적용됩니다. 필요에 따라 추가 미들웨어도 자유롭게 지정할 수 있습니다.

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 속도 제한(Rate Limiting) (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 속도 제한자 정의

Laravel에서는 지정한 라우트 또는 라우트 그룹에 요청 횟수 제한을 둘 수 있는 강력하고 커스터마이징 가능한 속도 제한 기능이 제공됩니다. 우선, 애플리케이션에 맞는 속도 제한 설정을 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의해야 합니다.

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

속도 제한자는 `RateLimiter` 파사드의 `for` 메서드를 사용해 정의합니다. `for` 메서드는 제한자 이름과, 적용할 제한 설정(클로저로 반환)을 인자로 받습니다. 제한 설정은 `Illuminate\Cache\RateLimiting\Limit` 클래스 인스턴스며, 빌더 메서드로 손쉽게 원하는 설정을 구성할 수 있습니다. 제한자 이름은 아무 문자열이나 가능합니다.

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

요청이 지정한 제한을 넘어서면 Laravel이 자동으로 429(Too Many Requests) 상태 코드의 응답을 반환합니다. 제한 초과 시 반환할 응답을 직접 정의하려면 `response` 메서드를 사용하면 됩니다.

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

속도 제한자 콜백은 요청 인스턴스를 받으므로, 요청 정보나 인증된 사용자에 따라 동적으로 제한을 설정할 수도 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perHour(10);
});
```

<a name="segmenting-rate-limits"></a>
#### 제한 분할(Segmenting Rate Limits)

특정 값을 기준으로 제한을 분할해야 하는 경우가 있습니다. 예를 들어, IP 주소별로 분 단위 100회 요청을 허용할 수 있습니다. `by` 메서드를 사용하여 제한 기준을 정할 수 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

다른 예시로, 인증된 사용자는 분당 100회, 비회원은 IP별 분당 10회로 제한할 수도 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 다중 속도 제한

필요하다면 하나의 제한자에 대해 제한 설정 배열을 반환할 수 있습니다. 배열 내 순서대로 각 제한이 평과되어 적용됩니다.

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

동일한 `by` 값을 기준으로 여러 제한을 지정해야 한다면, 각 `by` 값이 유일하도록 해야 합니다. 가장 쉬운 방법은 `by` 값에 접두사를 붙이는 것입니다.

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

들어오는 요청뿐만 아니라 라우트에서 반환된 응답을 기준으로도 속도 제한을 둘 수 있습니다. `after` 메서드를 사용하면, 특정 응답에만 제한이 적용되도록 할 수 있습니다. 예를 들어, 404나 유효성 검사 실패 등 특정 HTTP 상태 코드에 대해서만 제한을 증가시키거나, 해당하는 응답만 제한 횟수로 세고 싶을 때 유용합니다.

`after` 메서드는 응답을 인자로 받는 클로저를 받아, true/false로 제한 여부를 결정합니다. 이는 주로 404 응답에 연이어 요청이 발생하지 못하도록 하거나, 유효성 실패 요청을 제한 횟수에 포함시키지 않고 다시 시도할 수 있도록 하고 싶을 때 유용합니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Symfony\Component\HttpFoundation\Response;

RateLimiter::for('resource-not-found', function (Request $request) {
    return Limit::perMinute(10)
        ->by($request->user()?->id ?: $request->ip())
        ->after(function (Response $response) {
            // 404 응답에만 제한을 적용(Enumeration 방지)
            return $response->status() === 404;
        });
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 속도 제한 적용

제한자는 [미들웨어](/docs/12.x/middleware)인 `throttle`을 라우트 또는 라우트 그룹에 할당하여 사용할 수 있습니다. throttle 미들웨어에는 적용할 제한자 이름을 인자로 전달합니다.

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
#### Redis와 연동한 속도 제한

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스에 매핑되어 있습니다. 만약 애플리케이션의 캐시 드라이버로 Redis를 사용한다면, Laravel에게 속도 제한 관리를 Redis 기반으로 하라고 지정할 수 있습니다. 이때는 `bootstrap/app.php` 파일에서 `throttleWithRedis` 메서드를 사용합니다. 이렇게 하면, `throttle` 미들웨어가 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis`로 매핑됩니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 폼 메서드 스푸핑 (Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 메서드를 기본적으로 지원하지 않습니다. 따라서 이러한 타입의 라우트를 HTML 폼에서 호출하려면, 폼에 숨겨진 `_method` 필드를 추가해야 합니다. 이 필드의 값이 HTTP 요청 메서드로 사용됩니다.

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

더 편리하게는, [Blade 디렉티브](/docs/12.x/blade) `@method`를 사용하여 `_method` 입력 필드를 자동 생성할 수 있습니다.

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 정보 접근 (Accessing the Current Route)

`Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 사용하여 요청을 처리하는 라우트에 대한 정보를 얻을 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

라우터와 라우트 클래스에 존재하는 모든 메서드는 [Route 파사드의 실제 클래스](https://api.laravel.com/docs/12.x/Illuminate/Routing/Router.html)와 [Route 인스턴스](https://api.laravel.com/docs/12.x/Illuminate/Routing/Route.html) API 문서를 참고하세요.

<a name="cors"></a>
## 교차 출처 리소스 공유(CORS) (Cross-Origin Resource Sharing)

Laravel은 자동으로 CORS `OPTIONS` HTTP 요청에 대해 설정한 값으로 응답할 수 있습니다. 이러한 `OPTIONS` 요청은 애플리케이션의 글로벌 미들웨어 스택에 자동 포함된 `HandleCors` [미들웨어](/docs/12.x/middleware)에서 처리됩니다.

애플리케이션을 위한 CORS 설정 값을 커스터마이즈해야 한다면, `config:publish` Artisan 명령어로 `cors` 설정 파일을 배포할 수 있습니다.

```shell
php artisan config:publish cors
```

이 명령을 실행하면 `config` 디렉토리에 `cors.php` 설정 파일이 생성됩니다.

> [!NOTE]
> CORS 및 관련 헤더에 대한 자세한 내용은 [MDN CORS 웹 문서](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

애플리케이션을 프로덕션(environment)에 배포할 때는 Laravel의 라우트 캐시를 반드시 활용해야 합니다. 라우트 캐시를 사용하면 애플리케이션의 라우트를 등록하는 데 걸리는 시간이 획기적으로 단축됩니다. 라우트 캐시를 생성하려면 `route:cache` Artisan 명령어를 실행하면 됩니다.

```shell
php artisan route:cache
```

이 명령 실행 후에는 모든 요청마다 캐시된 라우트 파일이 바로 로드됩니다. 새로운 라우트를 추가했다면 반드시 캐시를 새로 생성해야 하며, 일반적으로 프로젝트 배포 과정에서만 `route:cache` 명령을 실행하도록 합니다.

라우트 캐시는 `route:clear` 명령으로 삭제할 수 있습니다.

```shell
php artisan route:clear
```
