# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리다이렉트 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록 보기](#listing-your-routes)
    - [라우팅 커스터마이징](#routing-customization)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [선택적 파라미터](#parameters-optional-parameters)
    - [정규 표현식 제약](#parameters-regular-expression-constraints)
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
- [요청 속도 제한](#rate-limiting)
    - [속도 제한 정의](#defining-rate-limiters)
    - [속도 제한 미들웨어 연결](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근하기](#accessing-the-current-route)
- [크로스-오리진 리소스 공유 (CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

라라벨에서 가장 기본적인 라우트는 URI와 클로저를 받아서 복잡한 라우팅 설정 없이도 간결하고 명확하게 라우트와 동작을 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일 (The Default Route Files)

모든 라라벨 라우트는 `routes` 디렉토리 내의 라우트 파일에서 정의됩니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 지정된 설정에 따라 라라벨이 자동으로 로드합니다. `routes/web.php` 파일은 웹 인터페이스용 라우트를 정의하는데, 이 라우트들은 세션 상태와 CSRF 보호 같은 기능을 제공하는 `web` [미들웨어 그룹](/docs/master/middleware#laravels-default-middleware-groups)에 할당됩니다.

대부분의 애플리케이션은 `routes/web.php` 파일에서 라우트 정의를 시작합니다. `routes/web.php` 에 정의한 라우트들은 브라우저에 정의된 라우트의 URL을 입력하면 접근할 수 있습니다. 예를 들어, 아래와 같은 라우트는 브라우저에서 `http://example.com/user` 로 접속하여 접근할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트 (API Routes)

애플리케이션이 무상태(stateless) API도 제공하려는 경우, `install:api` Artisan 명령어를 사용해 API 라우팅 기능을 활성화할 수 있습니다:

```shell
php artisan install:api
```

`install:api` 명령어는 [Laravel Sanctum](/docs/master/sanctum)를 설치하는데, Sanctum은 서드파티 API 소비자, SPA, 모바일 애플리케이션 등을 인증할 수 있는 간단하지만 강력한 API 토큰 인증 가드를 제공합니다. 그리고 `routes/api.php` 파일도 생성합니다:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

`routes/api.php` 내의 라우트들은 무상태이며, `api` [미들웨어 그룹](/docs/master/middleware#laravels-default-middleware-groups)에 할당됩니다. 또한, `/api` URI 접두어가 자동으로 적용되므로 파일 내의 모든 라우트에 따로 적용할 필요가 없습니다. 접두어를 변경하려면 애플리케이션의 `bootstrap/app.php` 파일을 수정하세요:

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메서드 (Available Router Methods)

라우터는 모든 HTTP 메서드에 대응하는 라우트를 등록할 수 있습니다:

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

때로는 여러 HTTP 메서드에 대응하는 라우트를 등록해야 할 때가 있습니다. 이 경우 `match` 메서드를 사용할 수 있고, 모든 HTTP 메서드에 대응하려면 `any` 메서드를 사용하세요:

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일 URI를 갖는 여러 라우트를 정의할 때, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트를 `any`, `match`, `redirect` 메서드를 사용하는 라우트보다 먼저 정의해야 요청이 올바른 라우트에 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입 (Dependency Injection)

라우트 콜백의 시그니처에 필요한 의존성을 타입 힌트로 명시하면, 해당 의존성이 라라벨 [서비스 컨테이너](/docs/master/container)에 의해 자동으로 주입됩니다. 예를 들어, `Illuminate\Http\Request` 클래스를 타입 힌트하면 현재 HTTP 요청이 자동으로 주입됩니다:

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호 (CSRF Protection)

`web` 라우트 파일에서 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 라우트로 HTML 폼을 전송할 때는 반드시 CSRF 토큰 필드를 포함해야 합니다. 포함하지 않으면 요청이 거부됩니다. CSRF 보호에 관해서는 [CSRF 문서](/docs/master/csrf)를 참고하세요:

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리다이렉트 라우트 (Redirect Routes)

다른 URI로 리다이렉트하는 라우트를 정의할 때 `Route::redirect` 메서드를 사용할 수 있습니다. 이는 단순 리다이렉트를 위해 전체 라우트 또는 컨트롤러를 정의할 필요 없이 간단한 바로가기 역할을 합니다:

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 302 상태 코드를 반환합니다. 세 번째 선택 매개변수로 상태 코드를 지정해 변경할 수 있습니다:

```php
Route::redirect('/here', '/there', 301);
```

또는 영구 리다이렉트(301 상태 코드)를 반환하려면 `Route::permanentRedirect` 메서드를 사용하세요:

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리다이렉트 라우트에서 라우트 파라미터를 사용할 때, Laravel이 예약어로 사용하는 `destination`과 `status` 파라미터는 쓸 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트 (View Routes)

라우트가 단순히 [뷰](/docs/master/views)를 반환하기만 한다면 `Route::view` 메서드를 사용할 수 있습니다. 이 메서드는 리다이렉트 메서드처럼 전체 라우트와 컨트롤러를 정의하지 않고 간단히 처리할 수 있도록 도와줍니다. 첫 번째 인자로 URI를, 두 번째 인자로 뷰 이름을 지정합니다. 세 번째 인자로 선택적으로 뷰에 전달할 데이터를 배열로 넘길 수 있습니다:

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 파라미터를 사용할 경우, Laravel에서 예약어로 지정된 `view`, `data`, `status`, `headers` 파라미터는 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 보기 (Listing Your Routes)

`route:list` Artisan 명령어로 애플리케이션에 정의된 모든 라우트 목록을 쉽게 확인할 수 있습니다:

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 미들웨어는 출력되지 않지만, `-v` 옵션을 추가하면 미들웨어와 미들웨어 그룹 이름까지 확인할 수 있습니다:

```shell
php artisan route:list -v

# 미들웨어 그룹 확장 보기...
php artisan route:list -vv
```

특정 URI 접두어를 갖는 라우트만 표시하고 싶다면 `--path` 옵션을 사용하세요:

```shell
php artisan route:list --path=api
```

타사 패키지에서 정의한 라우트를 빼고 싶다면 `--except-vendor` 옵션을, 반대로 타사 패키지만 보려면 `--only-vendor` 옵션을 추가해서 실행할 수 있습니다:

```shell
php artisan route:list --except-vendor

php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우팅 커스터마이징 (Routing Customization)

기본적으로 애플리케이션의 라우트는 `bootstrap/app.php` 파일에서 설정되고 로드됩니다:

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

그러나 때로는 애플리케이션의 라우트 일부를 다른 파일에 정의하고 싶을 수 있습니다. 이 경우 `withRouting` 메서드에 `then` 클로저를 전달할 수 있고, 이 클로저 내에서 추가 라우트 그룹을 등록할 수 있습니다:

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

또는 `withRouting`에 `using` 클로저를 제공해 라우트 등록을 완벽히 직접 관리할 수도 있습니다. 이 경우 프레임워크가 기본 HTTP 라우트를 등록하지 않으므로 라우트를 직접 수동으로 등록해야 합니다:

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

때때로 URI 경로 일부분을 캡처해야 할 때가 있습니다. 예를 들어 URL에서 사용자 ID를 읽어와야 하는 경우입니다. 이런 경우 라우트 파라미터를 정의할 수 있습니다:

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요에 따라 라우트 파라미터를 여러 개 정의할 수도 있습니다:

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 파라미터는 항상 `{}` 중괄호로 감싸야 하며 알파벳 문자로 구성됩니다. 파라미터 이름에는 밑줄(`_`)도 허용됩니다. 라우트 파라미터는 순서에 따라 라우트 콜백 또는 컨트롤러 매개변수에 주입되므로, 매개변수 이름은 중요하지 않습니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입

라우트 콜백에 Laravel 서비스 컨테이너가 자동으로 주입해주길 원하는 의존성이 있다면, 라우트 파라미터 뒤에 위치하도록 선언해야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 파라미터 (Optional Parameters)

가끔 URI에 항상 포함되지 않을 수도 있는 라우트 파라미터가 필요할 때가 있습니다. 이런 경우 파라미터 이름 뒤에 `?`를 붙이고, 해당 변수에 기본값을 지정하세요:

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규 표현식 제약 (Regular Expression Constraints)

`where` 메서드를 사용해 라우트 파라미터의 형식을 제한할 수 있습니다. `where`는 파라미터 이름과 정규 표현식을 받아 제한 조건을 지정합니다:

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

몇 가지 편의를 위해 일반적으로 사용하는 패턴에 맞춘 헬퍼 메서드를 제공하므로 빠르게 제약 조건을 적용할 수 있습니다:

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

만약 요청이 패턴 제약과 일치하지 않으면 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약 (Global Constraints)

특정 이름의 라우트 파라미터가 언제나 같은 정규 표현식으로 제한되도록 하려면 `Route::pattern` 메서드를 사용할 수 있습니다. 보통 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의합니다:

```php
use Illuminate\Support\Facades\Route;

/**
 * 애플리케이션 서비스 부트스트랩 수행
 */
public function boot(): void
{
    Route::pattern('id', '[0-9]+');
}
```

이렇게 정의하면 해당 파라미터 이름을 사용하는 모든 라우트에 패턴이 자동으로 적용됩니다:

```php
Route::get('/user/{id}', function (string $id) {
    // {id}가 숫자인 경우에만 실행...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시 (Encoded Forward Slashes)

Laravel 라우팅은 `/` 문자를 제외한 모든 문자를 라우트 파라미터 값에 포함시킬 수 있도록 지원합니다. 만약 `/`도 파라미터에 포함시키려면 `where` 정규 표현식 조건으로 명시적으로 허용해야 합니다:

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 라우트 경로의 마지막 세그먼트에서만 지원됩니다.

<a name="named-routes"></a>
## 이름 있는 라우트 (Named Routes)

이름 있는 라우트를 통해 특정 라우트에 대한 URL 생성이나 리다이렉트를 편리하게 할 수 있습니다. 라우트 정의에 `name` 메서드를 체인으로 연결하여 이름을 지정할 수 있습니다:

```php
Route::get('/user/profile', function () {
    // ...
})->name('profile');
```

컨트롤러 액션에도 이름을 지정할 수 있습니다:

```php
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!WARNING]
> 라우트 이름은 항상 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 이름 있는 라우트의 URL 생성 (Generating URLs to Named Routes)

이름을 지정한 라우트는 Laravel의 `route` 및 `redirect` 헬퍼 함수를 통해 URL 생성이나 리다이렉트에 활용할 수 있습니다:

```php
// URL 생성...
$url = route('profile');

// 리다이렉트 생성...
return redirect()->route('profile');

return to_route('profile');
```

파라미터가 필요한 이름 있는 라우트는 배열로 파라미터를 두 번째 인자로 넘기면 자동으로 올바른 위치에 삽입됩니다:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

추가 파라미터를 배열에 넘기면 자동으로 쿼리 스트링으로 붙습니다:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// 결과: /user/1/profile?photos=yes
```

> [!NOTE]
> 요청 전역에 걸쳐 URL 파라미터의 기본값을 지정하고 싶을 때는 [`URL::defaults` 메서드](/docs/master/urls#default-values)를 사용하세요.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 검사하기 (Inspecting the Current Route)

현재 요청이 특정 이름 있는 라우트로 매핑되었는지 알고 싶으면, 라우트 인스턴스의 `named` 메서드를 이용할 수 있습니다. 예를 들어 라우트 미들웨어에서 현재 라우트 이름을 검사하는 방법은 다음과 같습니다:

```php
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * 들어오는 요청 처리
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

라우트 그룹을 사용하면 많은 라우트에 공통 미들웨어 등 속성을 공유할 수 있습니다. 각 개별 라우트에 속성을 일일이 지정할 필요 없이 그룹 단위로 일괄 적용이 가능합니다.

중첩된 그룹은 스마트하게 부모 그룹의 속성과 병합되며, 미들웨어나 `where` 조건은 병합되고 이름과 접두어는 이어 붙여집니다. 네임스페이스 구분자와 URI 접두어 내의 슬래시는 적절히 자동 처리됩니다.

<a name="route-group-middleware"></a>
### 미들웨어 (Middleware)

그룹 내 모든 라우트에 미들웨어를 지정하려면 `middleware` 메서드를 그룹 선언 전에 사용합니다. 미들웨어 배열에 등록된 순서대로 실행됩니다:

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first와 second 미들웨어가 실행됨...
    });

    Route::get('/user/profile', function () {
        // first와 second 미들웨어가 실행됨...
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러 (Controllers)

라우트 그룹 내 모든 라우트가 동일 컨트롤러를 사용하는 경우, `controller` 메서드로 그룹 컨트롤러를 지정할 수 있습니다. 그 후 라우트 선언 시 호출할 컨트롤러 메서드만 명시하면 됩니다:

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅 (Subdomain Routing)

서브도메인 라우팅도 라우트 그룹에서 처리할 수 있습니다. URI처럼 서브도메인 부분도 라우트 파라미터를 지정할 수 있어서, 서브도메인 일부를 라우트나 컨트롤러에서 활용할 수 있습니다. `domain` 메서드로 서브도메인을 지정하고 그룹을 만드세요:

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

<a name="route-group-prefixes"></a>
### 라우트 접두어 (Route Prefixes)

`prefix` 메서드를 사용하면 그룹 내 모든 라우트 URI에 특정한 접두어를 붙일 수 있습니다. 예를 들어 `admin` 접두어로 모든 라우트를 묶을 수 있습니다:

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL과 매칭됨
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두어 (Route Name Prefixes)

`name` 메서드로 그룹 내 모든 라우트 이름에 문자열을 접두어처럼 붙일 수 있습니다. 예를 들어 모든 라우트 이름을 `admin` 접두어로 시작하게 할 수 있습니다. 접두어 문자열에 꼭 마침표(`.`)를 붙여 주세요:

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // 라우트 이름이 "admin.users"로 지정됨
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

모델 ID를 라우트나 컨트롤러에 주입할 때, 보통 해당 ID에 맞는 모델을 데이터베이스에서 직접 조회해야 합니다. 라라벨 라우트 모델 바인딩 기능은 이를 자동으로 처리해, ID 대신 모델 인스턴스를 바로 주입할 수 있도록 해줍니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩 (Implicit Binding)

라우트나 컨트롤러 액션에서 타입힌트된 변수 이름이 URI 세그먼트 이름과 일치하고, Eloquent 모델인 경우 자동으로 해당 모델 인스턴스를 조회해 주입합니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

`$user` 변수는 `App\Models\User` 모델 타입힌트를 갖고 있고, URI 세그먼트 `{user}`와 이름이 같으므로, 라라벨이 요청 URI에서 받은 값과 매칭되는 ID를 가진 모델을 찾아서 주입합니다. 만약 매칭되는 모델이 없으면 자동으로 404 응답을 반환합니다.

컨트롤러 메서드에서도 동일하게 동작합니다:

```php
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
#### Soft Deleted 모델

보통 암묵적 바인딩은 [Soft Delete](/docs/master/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 하지만 라우트에 `withTrashed` 메서드를 체인하면 Soft Delete된 모델도 조회합니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 이름 변경하기

ID 컬럼이 아니라 다른 컬럼으로 모델을 조회하고 싶은 경우, 라우트 파라미터 정의 시 컬럼명을 명시할 수 있습니다:

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

항상 특정 모델 클래스가 `id` 이외의 컬럼으로 조회되도록 하려면, 해당 모델에서 `getRouteKeyName` 메서드를 오버라이드하세요:

```php
/**
 * 모델의 라우트 키 지정
 */
public function getRouteKeyName(): string
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
#### 커스텀 키와 스코핑

하나의 라우트 내에 여러 모델이 바인딩될 경우, 두 번째 모델을 첫 번째 모델의 자식 관계로 스코핑하고 싶다면 다음과 같이 사용할 수 있습니다. 예를 들어 특정 사용자의 특정 블로그 글을 slug로 조회하는 라우트입니다:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

커스텀 키를 사용하는 중첩 라우트 파라미터에서는 라라벨이 부모 모델이 아마 `posts`라는 이름의 관계를 가진 것으로 추정해, 이를 통해 자식 모델을 쿼리합니다.

커스텀 키가 없더라도 항상 "자식" 바인딩에 스코프를 적용하려면 라우트에 `scopeBindings` 메서드를 호출하세요:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는 그룹 단위로 스코프를 적용할 수도 있습니다:

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

스코프로 묶지 않으려면 `withoutScopedBindings` 메서드를 사용하세요:

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 바인딩 실패 시 커스터마이징

기본적으로 바인딩된 모델을 찾지 못하면 404 응답이 반환됩니다. 하지만 `missing` 메서드에 클로저를 전달하면, 바인딩 실패 시 해당 클로저가 호출되어 응답을 커스터마이징할 수 있습니다:

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

PHP 8.1부터 지원된 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php) 기능과 연동해 라우트에도 string-backed Enum을 타입힌트할 수 있습니다. 라우트 세그먼트가 Enum의 유효한 값과 일치할 경우에만 해당 라우트가 호출되며, 그렇지 않으면 404가 반환됩니다. 예를 들어 다음과 같은 Enum이 있다면:

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

다음 라우트는 `{category}`가 `fruits` 또는 `people`일 때만 호출됩니다:

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩 (Explicit Binding)

암묵적 바인딩 대신 명시적으로 파라미터와 모델 매핑 방식을 지정할 수도 있습니다. 명시적 바인딩은 라우터의 `model` 메서드를 사용해 특정 파라미터에 대응하는 모델 클래스를 지정하는 것입니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 정의합니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * 애플리케이션 서비스 부트스트랩 수행
 */
public function boot(): void
{
    Route::model('user', User::class);
}
```

이후 파라미터가 `{user}`인 라우트를 정의하면 자동으로 `User` 모델 인스턴스가 주입됩니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

일치하는 모델을 찾을 수 없으면 404가 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 해석 로직 커스터마이징

커스텀 로직으로 모델 바인딩을 처리하고 싶다면 `Route::bind` 메서드를 사용해 클로저를 등록하세요. 클로저는 URI 세그먼트 값을 받아서 주입할 클래스 인스턴스를 반환해야 합니다. 역시 `AppServiceProvider`의 `boot` 메서드에서 설정합니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * 애플리케이션 서비스 부트스트랩 수행
 */
public function boot(): void
{
    Route::bind('user', function (string $value) {
        return User::where('name', $value)->firstOrFail();
    });
}
```

또는 Eloquent 모델에서 `resolveRouteBinding` 메서드를 오버라이드해 URI 세그먼트 값을 받으면 요청을 처리할 수도 있습니다:

```php
/**
 * 바운드 값에 따른 모델 조회
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

만약 [암묵적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용하는 라우트라면 자식 바인딩에는 `resolveChildRouteBinding` 메서드가 활용됩니다:

```php
/**
 * 바운드 값에 따른 자식 모델 조회
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

`Route::fallback` 메서드를 사용하면 요청이 어떤 라우트와도 매칭되지 않을 때 실행될 라우트를 정의할 수 있습니다. 보통 매칭 실패 시 예외 핸들러가 "404 페이지"를 렌더링하지만, `routes/web.php` 내에서 폴백 라우트를 정의하면 `web` 미들웨어 그룹이 자동 적용됩니다. 필요에 따라 추가 미들웨어도 연결할 수 있습니다:

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 요청 속도 제한 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 속도 제한 정의 (Defining Rate Limiters)

라라벨은 라우트 또는 라우트 그룹에 트래픽 제한을 걸 수 있는 강력하고 유연한 요청 속도 제한 서비스를 제공합니다. 앱 요구사항에 맞는 제한 설정을 정의하여 사용하세요.

일반적으로 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 속도 제한 정의를 합니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 서비스 부트스트랩 수행
 */
protected function boot(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
}
```

`RateLimiter::for` 메서드는 제한자 이름과, 해당 제한자를 사용하는 라우트에 적용할 제한 설정을 반환하는 클로저를 받습니다. 제한 설정은 `Illuminate\Cache\RateLimiting\Limit` 클래스 인스턴스를 반환해야 합니다. 제한자 이름은 원하는 임의의 문자열을 사용할 수 있습니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 서비스 부트스트랩 수행
 */
protected function boot(): void
{
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });
}
```

제한을 초과하면 Laravel이 자동으로 429 HTTP 상태 코드 응답을 반환합니다. 커스텀 응답을 정의하려면 `response` 메서드로 응답 클로저를 등록하세요:

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

요청이나 인증 사용자의 상태에 따라 동적으로 제한값을 조절하는 것도 가능합니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
#### 제한 세분화하기 (Segmenting Rate Limits)

같은 라우트라도 IP 주소나 사용자별 등 세분화해서 제한할 수 있습니다. 이를 위해 제한 객체의 `by` 메서드에 구분값을 넘기면 됩니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

다른 예로 인증 사용자 ID별로 1분에 100회, 미인증자는 IP별로 1분에 10회로 제한하는 경우:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 여러 제한 정의하기 (Multiple Rate Limits)

필요하다면 배열을 반환해 여러 제한을 동시에 정의할 수도 있습니다. 각 제한은 배열 내 순서대로 평가됩니다:

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

동일한 `by` 값으로 여러 제한을 쓸 때는 각 `by` 값이 고유하도록 접두어를 붙이는 것이 좋습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 속도 제한 미들웨어 연결 (Attaching Rate Limiters to Routes)

정의한 속도 제한은 `throttle` [미들웨어](/docs/master/middleware)를 사용해 라우트나 라우트 그룹에 적용할 수 있습니다. 미들웨어 파라미터로 제한자 이름을 넘기면 됩니다:

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
#### Redis를 이용한 제한 (Throttling With Redis)

기본 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스를 사용합니다. 그러나 캐시 드라이버로 Redis를 쓰는 경우, `throttleWithRedis` 메서드를 `bootstrap/app.php`에서 호출해 Redis 기반 제한 미들웨어 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 클래스를 사용하도록 설정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 폼 메서드 스푸핑 (Form Method Spoofing)

HTML 폼은 기본적으로 `PUT`, `PATCH`, `DELETE` 메서드를 직접 지원하지 않습니다. 따라서 이런 라우트를 호출할 때는 숨겨진 `_method` 필드를 추가하고 그 값을 HTTP 메서드로 지정해야 합니다:

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

편의를 위해 Blade의 `@method` 디렉티브를 사용할 수 있습니다:

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 접근하기 (Accessing the Current Route)

`Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 사용해 현재 요청을 처리하는 라우트에 관한 정보를 조회할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route 객체
$name = Route::currentRouteName(); // 문자열 (라우트 이름)
$action = Route::currentRouteAction(); // 문자열 (컨트롤러 액션)
```

라우터와 라우트 클래스에서 사용할 수 있는 모든 메서드는 [Route 파사드의 기반 클래스 API 문서](https://api.laravel.com/docs/master/Illuminate/Routing/Router.html)와 [Route 인스턴스 API 문서](https://api.laravel.com/docs/master/Illuminate/Routing/Route.html)를 참고하세요.

<a name="cors"></a>
## 크로스-오리진 리소스 공유 (CORS)

라라벨은 CORS `OPTIONS` HTTP 요청에 대해 자동으로 구성한 값으로 응답합니다. 이 `OPTIONS` 요청은 애플리케이션의 글로벌 미들웨어 스택에 기본 포함된 `HandleCors` [미들웨어](/docs/master/middleware)가 처리합니다.

필요에 따라 CORS 설정 값을 커스터마이징하려면 `config:publish` Artisan 명령어로 `cors` 설정 파일을 퍼블리시하세요:

```shell
php artisan config:publish cors
```

명령어 실행 후, 애플리케이션 `config` 디렉토리에 `cors.php` 설정 파일이 생성됩니다.

> [!NOTE]
> CORS 및 CORS 헤더에 대한 더 자세한 내용은 [MDN 웹 문서의 CORS 관련 페이지](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

프로덕션에 배포할 때는 라우트 캐싱을 꼭 활용하세요. 라우트 캐시는 애플리케이션의 모든 라우트 등록 시간을 크게 단축합니다. 캐시를 생성하려면 `route:cache` Artisan 명령어를 실행하세요:

```shell
php artisan route:cache
```

명령어 실행 후부터는 캐시된 라우트 파일을 각 요청 시 로드합니다. 새로운 라우트를 추가하면 캐시를 재생성해야 하니, 보통 배포 단계에서만 실행하세요.

캐시를 삭제하려면 `route:clear` 명령어를 사용합니다:

```shell
php artisan route:clear
```