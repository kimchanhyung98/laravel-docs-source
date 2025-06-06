# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리다이렉트 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록 확인](#listing-your-routes)
    - [라우팅 커스터마이징](#routing-customization)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [선택 파라미터](#parameters-optional-parameters)
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
    - [암묵적 Enum(열거형) 바인딩](#implicit-enum-binding)
    - [명시적 바인딩](#explicit-binding)
- [폴백 라우트](#fallback-routes)
- [요율 제한(Rate Limiting)](#rate-limiting)
    - [요율 제한자 정의](#defining-rate-limiters)
    - [라우트에 요율 제한자 연결](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근](#accessing-the-current-route)
- [CORS (Cross-Origin Resource Sharing)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅

라라벨에서 가장 기본적인 라우트 방식은 URI와 클로저를 받아, 복잡한 라우팅 설정 파일 없이도 매우 간단하고 직관적으로 라우트와 행동을 정의할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일

라라벨의 모든 라우트는 `routes` 디렉터리에 위치한 라우트 파일에 정의합니다. 이 파일들은 애플리케이션의 `bootstrap/app.php`에 지정된 설정을 따라 자동으로 로드됩니다. `routes/web.php` 파일은 웹 인터페이스용 라우트를 정의합니다. 이 라우트들은 `web` [미들웨어 그룹](/docs/master/middleware#laravels-default-middleware-groups)에 할당되어, 세션 상태 관리 및 CSRF 보호와 같은 기능을 제공합니다.

대부분의 애플리케이션은 `routes/web.php` 파일에서 라우트 정의를 시작합니다. `routes/web.php`에 정의된 라우트들은 해당 라우트의 URL을 브라우저에 입력해서 접근할 수 있습니다. 예를 들어, 아래 라우트는 브라우저에서 `http://example.com/user`로 접속해 확인할 수 있습니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트

애플리케이션이 상태가 없는 API를 제공해야 하는 경우, `install:api` 아티즌 명령어를 통해 API 라우팅을 활성화할 수 있습니다.

```shell
php artisan install:api
```

`install:api` 명령어는 [Laravel Sanctum](/docs/master/sanctum)을 설치합니다. Sanctum은 서드파티 API 소비자, SPA, 모바일 애플리케이션 인증에 사용할 수 있는 간단하면서 강력한 API 토큰 인증 가드를 제공합니다. 또한, `install:api` 명령어는 `routes/api.php` 파일을 생성합니다.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

`routes/api.php`에 정의된 라우트들은 상태를 저장하지 않으며, `api` [미들웨어 그룹](/docs/master/middleware#laravels-default-middleware-groups)에 할당됩니다. 또한, `/api` URI 접두사가 자동으로 적용되므로 파일 내 각 라우트에 직접 접두사를 지정할 필요가 없습니다. 접두사는 애플리케이션의 `bootstrap/app.php` 파일을 수정해 변경할 수 있습니다.

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메서드

라우터는 HTTP의 모든 메서드(HTTP verb)에 응답하는 라우트를 등록할 수 있도록 지원합니다.

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

경우에 따라 여러 HTTP 메서드에 동시에 응답하는 라우트가 필요할 수 있습니다. 이럴 때는 `match` 메서드를 사용할 수 있습니다. 또는, 모든 HTTP 메서드에 응답하는 라우트를 `any` 메서드로 등록할 수도 있습니다.

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일한 URI를 사용하는 여러 라우트를 정의할 때는, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트를 `any`, `match`, `redirect` 메서드를 사용하는 라우트보다 먼저 정의해야 합니다. 그래야 들어오는 요청이 올바른 라우트에 잘 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백 함수에서 필요로 하는 의존성을 타입힌트로 선언하면, 라라벨 [서비스 컨테이너](/docs/master/container)가 해당 의존성을 자동으로 해결해주고 주입해줍니다. 예를 들어, 현재 HTTP 요청 객체를 자동으로 주입받으려면 `Illuminate\Http\Request` 클래스를 타입힌트로 선언하면 됩니다.

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 메서드로 향하는 모든 HTML 폼에는 반드시 CSRF 토큰 필드를 포함해야 합니다. 그렇지 않으면 요청이 거부됩니다. 보다 자세한 CSRF 보호 방법은 [CSRF 문서](/docs/master/csrf)를 참고하세요.

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리다이렉트 라우트

다른 URI로 리다이렉트하는 라우트를 정의할 경우, `Route::redirect` 메서드를 활용할 수 있습니다. 이 메서드를 사용하면 간단하게 리다이렉트 라우트를 작성할 수 있어, 별도의 전체 라우트나 컨트롤러를 만들 필요가 없습니다.

```php
Route::redirect('/here', '/there');
```

기본적으로, `Route::redirect`는 `302` 상태 코드를 반환합니다. 세 번째 매개변수를 추가해 상태 코드를 직접 지정할 수 있습니다.

```php
Route::redirect('/here', '/there', 301);
```

또는, `Route::permanentRedirect` 메서드를 사용해 `301` 상태 코드를 반환하는 영구 리다이렉트 라우트를 만들 수 있습니다.

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 라우트 파라미터를 리다이렉트 라우트에서 사용할 때, 다음 파라미터 이름(`destination`, `status`)은 라라벨에서 예약되어 있으므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트

라우트가 [뷰](/docs/master/views)만 반환하면 되는 경우, `Route::view` 메서드를 사용할 수 있습니다. 이 메서드는 `redirect`와 마찬가지로 간단하게 라우트 정의가 가능하여, 전체 라우트나 컨트롤러를 따로 만들지 않아도 됩니다. 첫 번째 인수로 URI, 두 번째 인수로 뷰 이름을 넘기고, 필요한 경우 세 번째 인수로 뷰에 전달할 데이터를 배열로 제공할 수 있습니다.

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 파라미터를 사용하려면, 다음 파라미터 이름(`view`, `data`, `status`, `headers`)은 라라벨에서 예약되어 있으므로 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 확인

`route:list` 아티즌 명령어를 통해 애플리케이션에 정의된 모든 라우트를 한눈에 확인할 수 있습니다.

```shell
php artisan route:list
```

기본적으로 `route:list` 명령어는 각 라우트에 할당된 미들웨어를 표시하지 않습니다. 그러나 `-v` 옵션을 추가하면 라우트 미들웨어와 미들웨어 그룹 이름이 함께 출력됩니다.

```shell
php artisan route:list -v

# 미들웨어 그룹 펼치기...
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 보고 싶다면 다음과 같이 `--path` 옵션을 사용할 수 있습니다.

```shell
php artisan route:list --path=api
```

또한, `route:list` 명령어를 실행할 때 `--except-vendor` 옵션을 주면, 서드파티 패키지에서 정의된 라우트는 숨겨집니다.

```shell
php artisan route:list --except-vendor
```

반대로, `--only-vendor` 옵션을 사용하면 서드파티 패키지에서 정의된 라우트만 표시합니다.

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우팅 커스터마이징

기본적으로 애플리케이션의 라우트는 `bootstrap/app.php` 파일에서 설정되고 로드됩니다.

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

하지만 때로는 애플리케이션의 일부 라우트만 별도의 파일로 정의하고 싶을 수도 있습니다. 이 경우, `withRouting` 메서드에 `then` 클로저를 전달하면 됩니다. 이 클로저 안에서 추가 라우트를 자유롭게 등록할 수 있습니다.

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

또는, `withRouting` 메서드에 `using` 클로저를 전달하면 라라벨 프레임워크가 HTTP 라우트를 자동으로 등록하지 않고, 모든 라우트를 직접 수동으로 등록할 책임이 전적으로 여러분에게 있습니다.

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
## 라우트 파라미터

<a name="required-parameters"></a>
### 필수 파라미터

경우에 따라 라우트의 URI 일부를 캡처해야 할 때가 있습니다. 예를 들어, URL에서 사용자의 ID를 가져와야 할 수 있습니다. 이럴 때, 라우트 파라미터를 정의하여 해결할 수 있습니다.

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요하다면 라우트 파라미터를 여러 개도 정의할 수 있습니다.

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 파라미터는 항상 `{}` 중괄호로 감싸서 사용하며, 파라미터 이름은 영문자와 밑줄(`_`)만 포함할 수 있습니다. 라우트 콜백 또는 컨트롤러에는 파라미터가 선언된 순서대로 자동으로 값이 전달되며, 변수의 이름은 일치하지 않아도 상관 없습니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입

라우트의 콜백에서 라라벨 서비스 컨테이너가 자동으로 주입해주길 원하는 의존성이 있다면, 그 다음에 라우트 파라미터를 나열해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택 파라미터

때때로 라우트 파라미터가 항상 있을 필요는 없습니다. 파라미터 이름 뒤에 `?` 기호를 붙이면 해당 파라미터를 선택적으로 만들 수 있습니다. 이 경우, 해당 변수의 기본값도 반드시 설정해야 합니다.

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

`where` 메서드를 사용해 라우트 파라미터의 형식을 정규 표현식으로 제한할 수 있습니다. 이때 `where`에는 파라미터 이름과 허용할 정규 표현식을 지정하면 됩니다.

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

자주 사용하는 정규 표현식 패턴은 도우미 메서드를 통해 더 간단하게 라우트에 제약을 걸 수 있습니다.

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

만약 요청이 라우트 패턴 제약 조건과 일치하지 않으면, 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 글로벌 제약 조건

특정 라우트 파라미터에 항상 같은 정규 표현식 제약을 걸고 싶다면, `pattern` 메서드를 사용하세요. 보통 이 패턴은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의합니다.

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
    // {id}가 숫자인 경우에만 실행...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시(`/`) 처리

라라벨의 라우팅 컴포넌트에서는 슬래시(`/`)를 제외한 모든 문자를 라우트 파라미터 값에 허용합니다. 만약 파라미터에 슬래시 문자가 필요하다면, 반드시 `where` 조건의 정규 표현식으로 명시적으로 허용해야 합니다.

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 오직 마지막 라우트 세그먼트에서만 지원됩니다.

<a name="named-routes"></a>
## 네임드 라우트

네임드 라우트를 사용하면 특정 라우트의 URL이나 리다이렉트를 더 편리하게 생성할 수 있습니다. 라우트를 정의할 때 `name` 메서드를 체이닝해서 이름을 지정할 수 있습니다.

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
> 라우트 이름은 반드시 서로 겹치지 않도록 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 네임드 라우트로 URL 생성

라우트에 이름을 지정하면, 라라벨의 `route` 및 `redirect` 헬퍼 함수를 이용해 해당 라우트로 URL이나 리다이렉트를 쉽게 생성할 수 있습니다.

```php
// URL 생성...
$url = route('profile');

// 리다이렉트 생성...
return redirect()->route('profile');

return to_route('profile');
```

네임드 라우트에 파라미터가 있다면, 두 번째 인수로 배열을 전달해 값들을 넘길 수 있습니다. 지정한 파라미터는 URL 내 올바른 위치에 자동으로 삽입됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

추가 파라미터를 배열로 넘기면, 해당 키/값 쌍이 자동으로 URL의 쿼리스트링으로 추가됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// /user/1/profile?photos=yes
```

> [!NOTE]
> 때로는 요청 전반에 걸쳐 URL 파라미터의 기본값(예: 현재 로케일)을 지정하고 싶을 수 있습니다. 이럴 때는 [`URL::defaults` 메서드](/docs/master/urls#default-values)를 활용하세요.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 확인

현재 요청이 특정 네임드 라우트로 매칭됐는지 확인하려면, Route 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어, 라우트 미들웨어에서 현재 라우트 이름을 검사할 수 있습니다.

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
## 라우트 그룹

라우트 그룹이란 미들웨어 등과 같은 라우트 속성을 다수의 라우트에 중복해서 지정하지 않고 묶어서 한 번에 적용하는 기능입니다.

중첩된 라우트 그룹은 상위 그룹의 속성과 지능적으로 병합됩니다. 미들웨어와 `where` 조건은 합쳐지고, 이름과 URI 접두사는 이어서 붙습니다. 네임스페이스 구분자나 URI 접두사의 슬래시도 자동으로 적절하게 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

모든 라우트 그룹 내의 라우트에 [미들웨어](/docs/master/middleware)를 지정하고 싶을 땐, `middleware` 메서드를 사용하면 됩니다. 미들웨어는 배열에 지정된 순서대로 실행됩니다.

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // 'first', 'second' 미들웨어가 적용됨...
    });

    Route::get('/user/profile', function () {
        // 'first', 'second' 미들웨어가 적용됨...
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러

그룹 내 라우트들이 동일한 [컨트롤러](/docs/master/controllers)를 사용할 경우, `controller` 메서드로 그룹 전체에 컨트롤러를 지정하고, 각각 라우트 정의시에 호출할 컨트롤러 메서드만 작성하면 됩니다.

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹을 이용해 서브도메인 라우팅도 구성할 수 있습니다. 서브도메인도 라우트 URI처럼 파라미터를 받을 수 있어, 서브도메인의 일부 값을 라우트 파라미터로 활용할 수 있습니다. 서브도메인은 `domain` 메서드로 지정합니다.

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

<a name="route-group-prefixes"></a>
### 라우트 접두사

`prefix` 메서드를 사용하면, 그룹 내 모든 라우트 URI 앞에 지정한 경로를 접두사로 붙일 수 있습니다. 예를 들어, 그룹 내 모든 URL을 `admin`으로 시작하게 만들 수 있습니다.

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL과 매칭됨
    });
});
```

<a name="route-group-name-prefixes"></a>

### 라우트 이름 프리픽스

`name` 메서드를 사용하면 라우트 그룹 내 모든 라우트 이름에 지정한 문자열을 접두사로 붙일 수 있습니다. 예를 들어, 그룹 내 모든 라우트의 이름에 `admin` 접두사를 붙이고 싶다면, 아래와 같이 사용할 수 있습니다. 지정된 문자열이 라우트 이름 앞에 정확히 입력한 그대로 붙기 때문에, 접두사 끝에 반드시 `.`을 추가하시기 바랍니다.

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // Route assigned name "admin.users"...
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩

라우트나 컨트롤러 액션으로 모델 ID를 전달할 때, 해당 ID에 해당하는 모델을 데이터베이스에서 직접 조회하는 경우가 많습니다. 라라벨의 라우트 모델 바인딩 기능을 사용하면, 해당 모델 인스턴스를 라우트에 자동으로 주입할 수 있습니다. 즉, 단순히 사용자 ID를 주입받는 대신, 주어진 ID에 해당하는 `User` 모델 전체 인스턴스를 주입받을 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적(Implicit) 바인딩

라라벨은 라우트나 컨트롤러 액션에서 타입힌트된 변수명이 라우트 세그먼트 이름과 일치하면 Eloquent 모델을 자동으로 해결해줍니다. 예시를 보겠습니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

여기서 `$user` 변수가 `App\Models\User` Eloquent 모델로 타입힌트되어 있고, 변수명이 `{user}` URI 세그먼트와 일치하므로, 라라벨은 요청 URI의 해당 값(ID)과 일치하는 모델 인스턴스를 데이터베이스에서 자동으로 찾아서 주입합니다. 만약 해당 모델이 데이터베이스에 없다면, 자동으로 404 HTTP 응답이 반환됩니다.

물론, 컨트롤러 메서드를 사용할 때도 암묵적 바인딩이 가능합니다. 아래와 같이 URI 세그먼트 `{user}`가 컨트롤러의 `$user` 변수와 매칭되며, 타입힌트로 `App\Models\User`이 명시되어 있으면 동작합니다.

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

기본적으로, 암묵적 모델 바인딩은 [소프트 삭제](/docs/master/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 하지만 라우트 정의에 `withTrashed` 메서드를 추가하면 소프트 삭제된 모델도 함께 조회할 수 있습니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 변경하기

때때로, Eloquent 모델을 조회할 때 `id` 컬럼이 아닌 다른 컬럼을 기반으로 바인딩하고 싶을 수 있습니다. 이 경우 라우트 파라미터 정의에서 컬럼명을 직접 지정할 수 있습니다.

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

특정 모델 클래스에 대해 항상 `id`가 아닌 다른 컬럼을 사용하도록 하고 싶다면, Eloquent 모델에서 `getRouteKeyName` 메서드를 오버라이드하면 됩니다.

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
#### 커스텀 키와 범위(scoping)

하나의 라우트 정의에서 여러 Eloquent 모델을 암묵적으로 바인딩할 때, 두 번째 모델이 반드시 첫 번째 모델(부모)의 자식이어야 한다는 제약을 줄 수도 있습니다. 예를 들어, 특정 사용자의 블로그 게시물을 slug 값으로 조회하는 라우트는 다음과 같습니다.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

이렇게 중첩된(부모-자식) 라우트 파라미터에서 커스텀 키 기반 암묵적 바인딩을 사용할 경우, 라라벨은 자동으로 부모 모델을 기준으로 자식 모델(`Post`)을 조회하도록 쿼리 범위를 지정합니다. 이때, 라라벨은 부모(`User`) 모델이 `posts`(복수형)라는 연관관계 메서드를 가지고 있다고 가정해서 관련 모델을 조회합니다.

특정 키를 사용하지 않더라도, 라라벨이 자식 바인딩을 항상 부모 기준으로 제한하도록 하려면, 라우트 정의에 `scopeBindings` 메서드를 호출하면 됩니다.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는 라우트 그룹 전체에 대해 범위 지정 바인딩을 적용할 수도 있습니다.

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로, 명시적으로 바인딩 스코프를 적용하지 않도록 하려면 `withoutScopedBindings` 메서드를 사용할 수 있습니다.

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 모델 객체를 찾지 못했을 때 동작 커스터마이징

기본적으로, 암묵적 바인딩에서 모델을 찾지 못하면 404 HTTP 응답이 반환됩니다. 하지만 라우트 정의 시 `missing` 메서드를 이용해 이 동작을 커스터마이즈할 수 있습니다. `missing` 메서드는 모델을 찾지 못했을 때 실행되는 클로저를 받습니다.

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

PHP 8.1에서는 [Enum(열거형)](https://www.php.net/manual/en/language.enumerations.backed.php) 기능이 도입되었습니다. 라라벨도 이를 지원하여, 라우트 파라미터에 [문자열 기반 Enum](https://www.php.net/manual/en/language.enumerations.backed.php) 타입힌트가 지정되어 있으면, 해당 세그먼트가 올바른 Enum 값일 때만 해당 라우트가 실행됩니다. Enum 값에 해당하지 않으면 자동으로 404 HTTP 응답이 반환됩니다. 예를 들면 다음과 같습니다.

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

이렇게 정의된 Enum을 사용하여 `{category}` 세그먼트가 `fruits` 또는 `people`일 때만 라우트가 실행됩니다. 그렇지 않으면 404 응답이 반환됩니다.

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적(Explicit) 바인딩

라라벨의 암묵적, 관례 기반 모델 해석을 꼭 사용해야 하는 것은 아닙니다. 라우트 파라미터와 모델을 어떻게 매핑할지 직접 명시적으로 정의할 수도 있습니다. 이를 위해 라우터의 `model` 메서드를 사용해 특정 파라미터가 대응할 모델 클래스를 지정합니다. 명시적 모델 바인딩은 보통 `AppServiceProvider` 클래스의 `boot` 메서드에서 정의합니다.

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

그 다음 `{user}` 파라미터가 포함된 라우트를 정의합니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

이제 모든 `{user}` 파라미터는 자동으로 `App\Models\User` 모델과 연결되어, 해당 ID의 User 인스턴스가 데이터베이스에서 조회되어 자동으로 라우트에 주입됩니다. 예를 들어, `users/1` 요청이 들어오면 `id`가 1인 User 인스턴스가 주입됩니다.

해당 모델을 데이터베이스에서 찾지 못하면, 자동으로 404 HTTP 응답을 반환합니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 해석 로직 커스터마이즈

모델 바인딩 시 어떤 기준으로 객체를 주입할지 직접 커스텀하고 싶다면 `Route::bind` 메서드를 사용할 수 있습니다. 이 메서드에 전달하는 클로저는 URI 세그먼트 값을 받아서, 라우트에 주입할 객체를 반환해야 합니다. 이 역시 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 설정합니다.

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

또는 Eloquent 모델의 `resolveRouteBinding` 메서드를 오버라이드하여 바인딩 방식을 직접 지정할 수도 있습니다. 이 메서드는 URI 세그먼트 값을 받아서, 해당 값을 이용해 라우트에 주입할 인스턴스를 반환해야 합니다.

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

[암묵적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용하는 라우트에서는, 부모 모델의 자식 바인딩 처리를 위해 `resolveChildRouteBinding` 메서드가 사용됩니다.

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
## 폴백(Fallback) 라우트

`Route::fallback` 메서드를 사용하면, 들어오는 요청이 그 어떤 다른 라우트와도 일치하지 않을 때 실행되는 폴백 라우트를 정의할 수 있습니다. 일반적으로 처리되지 않은 요청은 애플리케이션의 예외 핸들러에 의해 자동으로 "404" 페이지가 렌더링됩니다. 하지만 보통 `fallback` 라우트는 `routes/web.php` 파일에 정의하기 때문에, `web` 미들웨어 그룹에 속한 모든 미들웨어가 이 라우트에도 적용됩니다. 필요에 따라 이 라우트에 추가 미들웨어도 적용할 수 있습니다.

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 요청 속도 제한(Rate Limiting)

<a name="defining-rate-limiters"></a>
### 속도 제한자(Rate Limiter) 정의

라라벨에는 특정 라우트 또는 라우트 그룹에 대해 트래픽 양을 제한할 수 있는 강력하고 유연한 속도 제한 서비스가 내장되어 있습니다. 먼저, 애플리케이션 요구에 맞는 속도 제한자 구성을 정의해야 합니다.

속도 제한자는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드 내에서 정의할 수 있습니다.

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

속도 제한자는 `RateLimiter` 파사드의 `for` 메서드를 사용해서 정의합니다. `for` 메서드는 제한자 이름과, 해당 제한이 적용될 라우트에 대한 제한 설정을 반환하는 클로저를 인수로 받습니다. 제한 설정은 모두 `Illuminate\Cache\RateLimiting\Limit` 클래스의 인스턴스입니다. 이 클래스는 여러 "빌더" 메서드를 제공하여 제한을 빠르게 정의할 수 있습니다. 제한자 이름은 자유롭게 지정 가능합니다.

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

요청이 지정된 속도 제한을 초과하면, 라라벨이 자동으로 429 HTTP 상태 코드의 응답을 반환합니다. 만약 제한을 초과했을 때 반환될 응답을 직접 정의하고 싶다면 `response` 메서드를 사용할 수 있습니다.

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

속도 제한자 콜백은 들어오는 HTTP 요청 인스턴스를 전달받으므로, 인증된 사용자나 요청 정보에 따라 제한을 동적으로 조정할 수 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
#### 속도 제한 세분화

경우에 따라, 특정 기준값으로 속도 제한을 세분화할 수 있습니다. 예를 들어, 특정 라우트를 IP별로 분리해서 분당 100회 접근 가능하도록 제한하고 싶다면 `by` 메서드를 사용하면 됩니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

또 다른 예로, 인증된 사용자의 ID별로는 분당 100회, 비회원 사용자의 경우 IP별로 분당 10회만 접근을 허용하고 싶다면 아래와 같이 설정할 수 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 다중 속도 제한

필요하다면, 하나의 속도 제한자에 대해 여러 개의 제한 규칙을 배열 형태로 반환할 수 있습니다. 배열에 정의된 순서대로 각 제한 규칙이 적용됩니다.

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

동일한 `by` 값을 기준으로 다중 속도 제한을 적용한다면, 각 `by` 값이 반드시 고유하도록 해야 합니다. 가장 좋은 방법은 `by` 메서드에 전달하는 값에 접두사를 붙이는 것입니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 속도 제한자 연결

속도 제한자는 [미들웨어](/docs/master/middleware) `throttle`를 이용해 라우트 또는 라우트 그룹에 지정할 수 있습니다. `throttle` 미들웨어는 연결하고자 하는 속도 제한자의 이름을 인수로 받습니다.

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
#### Redis와 함께 속도 제한 적용

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스에 매핑되어 있습니다. 하지만 애플리케이션의 캐시 드라이버로 Redis를 사용 중이라면, 라라벨이 Redis를 이용해 속도 제한을 관리하도록 설정할 수 있습니다. 이를 위해 `bootstrap/app.php` 파일에서 `throttleWithRedis` 메서드를 사용하세요. 이 메서드는 `throttle` 미들웨어를 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 미들웨어 클래스로 매핑합니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 폼 메서드 위장(Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 메서드를 지원하지 않습니다. 그래서 이런 라우트를 HTML 폼에서 호출하려면, 폼에 숨겨진 `_method` 필드를 추가해야 합니다. 이 필드에 지정된 값이 HTTP 요청 메서드로 인식됩니다.

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

편의를 위해, [Blade 디렉티브](/docs/master/blade)인 `@method`를 이용해 `_method` 입력 필드를 생성할 수도 있습니다.

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 정보 접근

`Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 이용해 현재 요청을 처리하는 라우트 정보를 확인할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

`Route` 파사드의 [기본 클래스](https://api.laravel.com/docs/master/Illuminate/Routing/Router.html)와 [Route 인스턴스](https://api.laravel.com/docs/master/Illuminate/Routing/Route.html)에 대해 더 자세한 API 문서도 참고하실 수 있습니다.

<a name="cors"></a>
## 교차 출처 리소스 공유(CORS)

라라벨은 CORS `OPTIONS` HTTP 요청에 대해, 여러분이 지정한 값으로 자동 응답할 수 있습니다. `OPTIONS` 요청은 애플리케이션의 글로벌 미들웨어 스택에 자동 포함된 `HandleCors` [미들웨어](/docs/master/middleware)에 의해 자동으로 처리됩니다.

경우에 따라 애플리케이션의 CORS 설정 값을 직접 커스터마이즈해야 할 수도 있습니다. 이때는 `config:publish` 아티즌 명령어를 통해 `cors` 설정 파일을 퍼블리시하면 됩니다.

```shell
php artisan config:publish cors
```

이 명령어를 실행하면 애플리케이션의 `config` 디렉터리에 `cors.php` 설정 파일이 생성됩니다.

> [!NOTE]
> CORS 및 CORS 헤더에 대한 더 자세한 정보는 [MDN 웹 문서의 CORS 안내](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하시기 바랍니다.

<a name="route-caching"></a>
## 라우트 캐싱(Route Caching)

프로덕션 환경에서 애플리케이션을 배포할 때는 라라벨의 라우트 캐시 기능을 활용하는 것이 좋습니다. 라우트 캐시를 사용하면 애플리케이션의 모든 라우트를 등록하는 데 걸리는 시간을 크게 단축할 수 있습니다. 라우트 캐시를 생성하려면 다음의 `route:cache` 아티즌 명령어를 실행하세요.

```shell
php artisan route:cache
```

이 명령어를 실행하면, 이제부터 모든 요청에 캐시된 라우트 파일이 사용됩니다. 새로운 라우트를 추가했다면 캐시를 반드시 새로 생성해야 합니다. 때문에 보통 배포 작업 시점에만 `route:cache` 명령어를 실행하는 것이 좋습니다.

라우트 캐시는 다음과 같이 `route:clear` 명령어로 삭제할 수 있습니다.

```shell
php artisan route:clear
```