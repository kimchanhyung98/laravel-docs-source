# 라우팅

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리디렉션 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록 확인](#listing-your-routes)
    - [라우팅 커스터마이징](#routing-customization)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [선택적 파라미터](#parameters-optional-parameters)
    - [정규식 제약조건](#parameters-regular-expression-constraints)
- [이름있는 라우트](#named-routes)
- [라우트 그룹](#route-groups)
    - [미들웨어](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [서브도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 프리픽스](#route-group-prefixes)
    - [라우트 네임 프리픽스](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암시적 바인딩](#implicit-binding)
    - [암시적 Enum 바인딩](#implicit-enum-binding)
    - [명시적 바인딩](#explicit-binding)
- [폴백 라우트](#fallback-routes)
- [요청 제한(Rate Limiting)](#rate-limiting)
    - [요청 제한자 정의](#defining-rate-limiters)
    - [라우트에 제한자 할당](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 정보 얻기](#accessing-the-current-route)
- [교차 출처 리소스 공유(CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅

가장 기본적인 Laravel 라우트는 URI와 클로저를 인자로 받아, 복잡한 라우팅 설정 파일 없이 매우 단순하고 직관적으로 라우트와 동작을 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일

모든 Laravel 라우트는 `routes` 디렉터리 내 라우트 파일에 정의되어 있습니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 지정된 설정에 따라 자동으로 Laravel에 의해 로드됩니다. `routes/web.php` 파일은 웹 인터페이스용 라우트를 정의합니다. 이 라우트들은 `web` [미들웨어 그룹](/docs/{{version}}/middleware#laravels-default-middleware-groups)에 할당되어, 세션 상태 및 CSRF 보호와 같은 기능을 제공합니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에 라우트를 정의하는 것으로 시작합니다. `routes/web.php`에 정의된 라우트는 브라우저 주소창에 정의된 라우트의 URL을 입력하여 접근할 수 있습니다. 예를 들어, 아래 라우트는 브라우저에서 `http://example.com/user`로 접근할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트

애플리케이션이 상태 비저장(stateless) API도 제공해야 하는 경우, `install:api` Artisan 명령어로 API 라우팅을 활성화할 수 있습니다:

```shell
php artisan install:api
```

`install:api` 명령은 강력하면서도 단순한 API 토큰 인증을 제공하는 [Laravel Sanctum](/docs/{{version}}/sanctum)를 설치합니다. 이로써 서드파티 API 소비자, SPA, 모바일 앱을 인증할 수 있습니다. 또한, 이 명령은 `routes/api.php` 파일을 생성합니다:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

`routes/api.php`의 라우트는 상태 비저장이며 `api` [미들웨어 그룹](/docs/{{version}}/middleware#laravels-default-middleware-groups)에 할당됩니다. 또한 이 라우트에는 `/api` URI 프리픽스가 자동으로 적용되므로, 파일 내의 각 라우트에 직접 프리픽스를 지정할 필요가 없습니다. 프리픽스를 변경하려면, 애플리케이션의 `bootstrap/app.php` 파일을 수정하세요:

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메서드

라우터는 모든 HTTP 메서드에 응답하는 라우트를 등록할 수 있습니다:

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

여러 HTTP 메서드에 응답하는 라우트를 등록해야 하는 경우 `match` 메서드를 사용할 수 있습니다. 또는, `any` 메서드로 모든 HTTP 메서드에 응답하는 라우트를 등록할 수 있습니다:

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일한 URI를 공유하는 여러 라우트를 정의할 때, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트는 `any`, `match`, `redirect` 메서드를 사용하는 라우트보다 먼저 정의해야 합니다. 이렇게 해야 들어오는 요청이 올바른 라우트와 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백 시그니처에 필요한 의존성을 타입힌트하면, Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통하여 자동으로 해석되어 주입됩니다. 예시로, 현재 HTTP 요청 객체를 자동으로 라우트 콜백에 주입받으려면 `Illuminate\Http\Request` 클래스를 타입힌트하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 요청을 사용하는 모든 HTML 폼에는 반드시 CSRF 토큰 필드가 포함되어야 합니다. 그렇지 않으면 요청이 거부됩니다. 자세한 내용은 [CSRF 문서](/docs/{{version}}/csrf)를 참고하세요:

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리디렉션 라우트

다른 URI로 리디렉션하는 라우트를 정의할 경우, `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드를 사용하면 단순 리디렉션을 위해 라우트나 컨트롤러 전체를 정의하지 않아도 됩니다:

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 선택적 세 번째 인자로 상태 코드를 지정할 수 있습니다:

```php
Route::redirect('/here', '/there', 301);
```

또는, `Route::permanentRedirect`를 사용해 `301` 상태 코드를 반환할 수 있습니다:

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리디렉션 라우트에 라우트 파라미터를 사용할 때, `destination`과 `status`는 Laravel이 예약한 파라미터명이므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트

라우트가 [뷰](/docs/{{version}}/views)만 반환하면, `Route::view` 메서드를 사용할 수 있습니다. `redirect` 메서드와 마찬가지로, 전체 라우트나 컨트롤러를 정의하지 않고 간단히 사용할 수 있습니다. 첫 번째 인자는 URI, 두 번째 인자는 뷰 이름입니다. 추가로 뷰에 전달할 데이터를 배열로 세 번째 인자에 전달할 수 있습니다:

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 파라미터를 사용할 경우, `view`, `data`, `status`, `headers` 파라미터명은 Laravel이 예약하였으므로 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 확인

`route:list` Artisan 명령어로 애플리케이션에 정의된 라우트 전체를 쉽게 확인할 수 있습니다:

```shell
php artisan route:list
```

기본적으로 라우트에 할당된 미들웨어는 `route:list` 출력에 표시되지 않습니다. 그러나, 명령에 `-v` 옵션을 추가하여 미들웨어와 미들웨어 그룹명을 표시하도록 할 수 있습니다:

```shell
php artisan route:list -v

# 미들웨어 그룹 확장...
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 보고 싶을 때는 다음과 같이 옵션을 사용할 수 있습니다:

```shell
php artisan route:list --path=api
```

또한, `route:list` 명령어 실행 시 `--except-vendor` 옵션을 사용하여 서드파티 패키지에서 정의한 라우트를 숨길 수 있습니다:

```shell
php artisan route:list --except-vendor
```

반대로, `--only-vendor` 옵션을 사용해 서드파티 패키지의 라우트만 표시할 수도 있습니다:

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우팅 커스터마이징

기본적으로, 애플리케이션의 라우트는 `bootstrap/app.php` 파일에서 설정 및 로드됩니다:

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

경우에 따라, 애플리케이션의 특정 라우트 모듈을 위해 별도의 라우트 파일을 정의하고 싶을 수 있습니다. 이럴 땐 `withRouting` 메서드의 `then` 클로저에 추가 라우트 등록 코드를 작성할 수 있습니다:

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

또는, `withRouting`에 `using` 클로저를 전달하여 라우트 등록을 완전히 수동으로 제어할 수도 있습니다. 이때는 HTTP 라우트가 프레임워크에서 등록되지 않으며, 모든 라우트를 직접 등록해야 합니다:

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

경우에 따라, URI의 일부를 라우트에서 파라미터로 캡처해야 할 수 있습니다. 예를 들어, URL로부터 사용자의 ID를 캡처할 필요가 있습니다. 이를 위해 라우트 파라미터를 정의할 수 있습니다:

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요에 따라 여러 개의 라우트 파라미터를 정의할 수 있습니다:

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 파라미터는 항상 `{}` 중괄호로 감싸며, 알파벳과 밑줄(`_`)을 사용할 수 있습니다. 파라미터는 라우트 콜백/컨트롤러의 인자 순서에 따라 주입되며, 인자 명칭은 상관없습니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입

라우트에 의존성 주입이 필요할 때, 서비스 컨테이너가 파라미터를 자동으로 주입하도록 하려면, 의존성 인자를 라우트 파라미터 앞에 배치해야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 파라미터

가끔 URI에 항상 존재하지 않을 수도 있는 라우트 파라미터가 필요할 수 있습니다. 이 경우, 파라미터명 뒤에 `?`를 붙여 선택적으로 만들 수 있습니다. 또한 라우트의 대응하는 변수에 디폴트 값을 할당해야 합니다:

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규식 제약조건

`where` 메서드를 사용하여 라우트 파라미터의 형식을 정규식으로 제약할 수 있습니다. `where`는 파라미터명과 정규식을 인자로 받습니다:

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

더 자주 쓰는 패턴을 위한 헬퍼 메서드도 있습니다:

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

요청이 라우트 패턴 제약에 맞지 않으면 404 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약조건

특정 파라미터에 항상 동일한 정규식 제약을 적용하려면, `pattern` 메서드를 사용할 수 있습니다. 이 패턴은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 정의하세요:

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

한 번 패턴을 정의하면, 해당 파라미터명을 사용하는 모든 라우트에 자동 적용됩니다:

```php
Route::get('/user/{id}', function (string $id) {
    // {id}가 numeric일 때만 실행됨...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시(`/`)

Laravel 라우팅은 `/`를 제외한 모든 문자를 라우트 파라미터 값에서 허용합니다. 슬래시(`/`)도 파라미터에 포함하려면 `where` 조건의 정규식으로 명시적으로 허용해야 합니다:

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 마지막 라우트 세그먼트에서만 지원됩니다.

<a name="named-routes"></a>
## 이름있는 라우트

이름있는 라우트는 특정 라우트에 대한 URL 생성이나 리디렉션을 편리하게 할 수 있게 해줍니다. 라우트 정의에서 `name` 메서드를 체이닝하여 이름을 지정할 수 있습니다:

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
#### 이름있는 라우트로 URL 생성

이름을 할당한 후, `route` 및 `redirect` 헬퍼 함수를 통해 URL이나 리디렉트시 라우트의 이름을 사용할 수 있습니다:

```php
// URL 생성하기...
$url = route('profile');

// 리디렉트 생성하기...
return redirect()->route('profile');

return to_route('profile');
```

이름있는 라우트가 파라미터를 정의한 경우, 두 번째 인자로 파라미터를 넘기면 URL에 올바르게 삽입됩니다:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

추가적으로 배열로 전달하는 값들은 쿼리 스트링으로 자동 첨부됩니다:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// /user/1/profile?photos=yes
```

> [!NOTE]
> 로케일과 같은 URL 파라미터에 대한 요청 전체의 기본값을 지정하고 싶다면 [URL::defaults 메서드](/docs/{{version}}/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 확인

현재 요청이 특정 이름의 라우트에 매핑되었는지 확인하려면, Route 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어, 미들웨어 내에서 현재 라우트 이름을 검사할 수 있습니다:

```php
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * 들어오는 요청을 처리
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

라우트 그룹을 사용하면 미들웨어 등 라우트 속성을 다수의 라우트에 반복적으로 지정하지 않고 공유할 수 있습니다.

중첩 그룹에서는 부모 그룹과 속성이 자동으로 "병합"됩니다. 미들웨어와 `where` 조건은 병합되며, 이름과 프리픽스는 추가(append)됩니다. 네임스페이스 구분자 및 슬래시는 자동으로 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

[미들웨어](/docs/{{version}}/middleware)를 그룹 내 모든 라우트에 적용하려면, 그룹 정의 전에 `middleware` 메서드를 사용하세요. 미들웨어는 배열에 나열된 순서대로 실행됩니다:

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first와 second 미들웨어가 적용됨...
    });

    Route::get('/user/profile', function () {
        // first와 second 미들웨어가 적용됨...
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러

여러 라우트가 동일한 [컨트롤러](/docs/{{version}}/controllers)를 사용하는 경우, `controller` 메서드로 그룹 전체에 공통 컨트롤러를 지정할 수 있습니다. 이후 라우트 정의시 컨트롤러 메서드만 지정하면 됩니다:

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹은 서브도메인 라우팅에도 사용할 수 있습니다. 서브도메인에도 라우트 파라미터를 설정할 수 있어, 서브도메인의 일부를 라우트/컨트롤러 내에서 사용 가능합니다. `domain` 메서드로 그룹 정의 전 서브도메인을 지정하세요:

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

> [!WARNING]
> 서브도메인 라우트의 접근성을 보장하려면, 루트 도메인 라우트보다 먼저 서브도메인 라우트를 등록해야 합니다. 그래야 동일 URI 경로를 가진 서브도메인 라우트가 루트 도메인 라우트에 의해 덮어쓰이지 않습니다.

<a name="route-group-prefixes"></a>
### 라우트 프리픽스

`prefix` 메서드는 그룹 내 각 라우트의 URI에 프리픽스를 붙일 때 사용합니다. 예를 들어, 그룹 내 모든 라우트 URI 앞에 `admin`을 붙이고 싶다면 다음과 같이 합니다:

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL에 매칭됨
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 프리픽스

`name` 메서드는 그룹 내 각 라우트의 이름에 정해진 문자열을 프리픽스로 붙일 때 사용합니다. 예시처럼 그룹 전체 라우트에 `admin.` 네임 프리픽스를 붙일 수 있습니다:

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // 이 라우트의 이름은 "admin.users"로 할당됨...
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩

라우트나 컨트롤러 액션에 모델 ID를 주입할 때, 종종 DB 쿼리를 통해 그 ID에 매칭되는 모델을 가져오게 됩니다. 라라벨의 라우트 모델 바인딩을 사용하면, 모델 인스턴스를 라우트에 자동 주입할 수 있어 더욱 편리합니다. 즉, ID 대신 매칭되는 전체 `User` 모델 인스턴스를 바로 주입받을 수 있습니다.

<a name="implicit-binding"></a>
### 암시적 바인딩

라우트나 컨트롤러 액션에 타입힌트된 변수 이름이 라우트 세그먼트명과 일치하면, Laravel이 Eloquent 모델을 자동으로 주입해줍니다. 예시:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

여기서 `$user` 변수는 `App\Models\User` Eloquent 모델로 타입힌트되어 있고, 변수명과 `{user}` 세그먼트가 일치하므로, URI 경로의 값과 일치하는 ID의 User 모델이 자동 주입됩니다. 모델 인스턴스를 DB에서 찾지 못하면 404 응답이 자동으로 반환됩니다.

물론, 컨트롤러에서 사용할 때도 마찬가지입니다. `{user}` 세그먼트가 컨트롤러의 `$user` 변수와 맞아야 합니다:

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

기본적으로 암시적 모델 바인딩은 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 하지만, 라우트 정의 시 `withTrashed` 메서드를 체이닝하면 소프트 삭제 모델도 조회 가능합니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 키 커스터마이징

Eloquent 모델을 `id` 대신 다른 컬럼으로 조회하고 싶은 경우, 라우트 파라미터 정의에서 해당 컬럼을 지정할 수 있습니다:

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

특정 모델 클래스가 항상 `id`가 아닌 다른 컬럼으로 바인딩되길 원한다면, 모델의 `getRouteKeyName` 메서드를 오버라이드하세요:

```php
/**
 * 라우트 키 반환
 */
public function getRouteKeyName(): string
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
#### 커스텀 키와 스코핑

하나의 라우트 정의에서 여러 Eloquent 모델을 암시적으로 바인딩할 때, 두 번째 모델이 반드시 첫 번째 모델의 자식임을 보장하고 싶다면 자동 스코핑이 가능합니다. 예를 들어 특정 유저의 블로그 포스트를 슬러그로 조회할 때:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

이처럼 중첩된 커스텀 키 암시적 바인딩을 사용하면, 라라벨은 부모 모델의 연관관계 명칭을 추정해 쿼리를 스코핑합니다. 위에서는 `User` 모델의 `posts` 관계가 있는지 자동으로 확인하여 `Post` 모델을 가져옵니다.

원한다면, 커스텀 키가 없더라도 `scopeBindings` 메서드로 항상 "자식" 바인딩을 스코프할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는, 라우트 그룹 전체에 대해 스코프 바인딩을 적용할 수 있습니다:

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로, `withoutScopedBindings`를 사용해 스코프 바인딩을 비활성화할 수도 있습니다:

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 모델 미발견시 동작 커스터마이징

기본적으로 암시적 바인딩 모델을 찾지 못하면 404 응답이 반환됩니다. 그러나, 라우트 정의시 `missing` 메서드에 클로저를 전달하여 동작을 커스터마이징할 수 있습니다:

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
### 암시적 Enum 바인딩

PHP 8.1부터 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)이 도입되었습니다. 이를 지원하기 위해 라라벨은 라우트 정의에서 [string-backed Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 타입힌트할 수 있도록 했습니다. 해당 세그먼트가 Enum 값과 일치할 경우에만 라우트가 실행되며, 그렇지 않으면 404가 반환됩니다. 예를 들어 아래 Enum이 있다면:

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

`{category}` 세그먼트가 `fruits` 또는 `people`일 때만 라우트가 실행되고 그 외에는 404가 반환됩니다:

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩

암시적/컨벤션 기반 모델 바인딩이 아닌 명시적으로도 모델 바인딩을 할 수 있습니다. 명시적 바인딩을 등록하려면, 라우터의 `model` 메서드로 파라미터와 클래스의 매핑을 지정하면 됩니다. 이는 `AppServiceProvider`의 `boot` 메서드 처음 부분에 정의하세요:

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

이후, `{user}` 파라미터가 있는 라우트를 정의하면:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

모든 `{user}` 파라미터는 `App\Models\User` 모델과 바인딩되어, 해당 ID의 User 인스턴스가 주입됩니다. 매칭 모델이 없으면 404가 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 로직 커스터마이징

자체적으로 바인딩 로직을 정의하려면 `Route::bind` 메서드를 사용하세요. 이때 클로저는 URI 세그먼트 값을 받고, 라우트에 주입할 클래스 인스턴스를 반환해야 합니다. 역시 `AppServiceProvider`의 `boot` 메서드에 정의하세요:

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

또는, Eloquent 모델에서 `resolveRouteBinding` 메서드를 오버라이드할 수도 있습니다:

```php
/**
 * 바인딩 값에 대한 모델 조회
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

라우트가 [암시적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용할 경우 `resolveChildRouteBinding` 메서드를 활용할 수 있습니다:

```php
/**
 * 바인딩 값에 대한 자식 모델 조회
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
## 폴백 라우트

`Route::fallback` 메서드로, 어떤 라우트에도 매칭되지 않는 요청이 들어왔을 때 실행되는 라우트를 정의할 수 있습니다. 기본적으로 매칭되지 않는 요청은 예외 핸들러를 통해 자동으로 "404" 페이지가 렌더링됩니다. `routes/web.php`에 폴백 라우트를 정의하는 경우, `web` 미들웨어 그룹의 모든 미들웨어가 해당 라우트에도 적용됩니다. 필요에 따라 추가적인 미들웨어도 자유롭게 추가할 수 있습니다:

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 요청 제한 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 요청 제한자 정의

Laravel은 라우트/라우트 그룹의 트래픽을 제한할 수 있도록 강력하고 커스터마이징 가능한 요청 제한 서비스를 제공합니다. 먼저, 애플리케이션 요구에 맞는 요청 제한자(rate limiter) 구성을 정의해야 합니다.

제한자는 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 정의합니다:

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

제한자는 `RateLimiter` 파사드의 `for` 메서드로 정의하며, 이름과 제한 설정을 반환하는 클로저가 필요합니다. 제한설정 객체는 `Illuminate\Cache\RateLimiting\Limit` 클래스 인스턴스입니다. 이름은 원하는 아무 문자열이나 가능합니다:

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

요청이 지정된 한도를 초과하면, Laravel이 자동으로 429 상태 코드를 반환합니다. 직접 응답을 커스터마이징하고 싶을 때는 `response` 메서드를 사용할 수 있습니다:

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

제한자 콜백에서는 들어온 HTTP 요청 인스턴스를 사용할 수 있으므로, 사용자/요청에 따라 동적으로 제한을 설정할 수도 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
#### 제한 세분화

제한을 일부 기준(예: IP별)으로 세분화하고 싶은 경우, `by` 메서드로 키값을 설정할 수 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

예를 들어, 인증 사용자는 분당 100회, 게스트는 IP기준 분당 10회로 각기 제한하려면 다음과 같이 할 수 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 다중 요청 제한

필요하다면, 하나의 제한자에 대해 여러 제한을 배열로 반환할 수 있습니다. 배열 내 순서대로 모든 제한이 평가됩니다:

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

동일한 `by` 값으로 여러 제한을 지정할 경우, 각 `by` 값이 반드시 고유하도록 해야 합니다. 가장 쉬운 방법은 prefix를 붙이는 것입니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 요청 제한자 할당

요청 제한자는 `throttle` [미들웨어](/docs/{{version}}/middleware)를 사용해 라우트/라우트 그룹에 할당할 수 있습니다. throttle 미들웨어에 제한자 이름을 전달합니다:

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

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스에 매핑됩니다. 하지만, 애플리케이션의 캐시 드라이버로 Redis를 사용하는 경우, Redis 기반 요청 제한을 사용할 수 있습니다. 이를 위해 `bootstrap/app.php`에서 `throttleWithRedis`를 사용하세요:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 폼 메서드 스푸핑

HTML 폼에서는 `PUT`, `PATCH`, `DELETE` 메서드를 직접 지원하지 않습니다. 따라서 이러한 메서드를 사용하는 라우트를 HTML 폼에서 호출할 때는 숨겨진 `_method` 필드를 추가해야 합니다. 이 필드의 값이 HTTP 요청 메서드로 인식됩니다:

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

편의상, `@method` [Blade 디렉티브](/docs/{{version}}/blade)로 `_method` 입력 필드를 쉽게 생성할 수 있습니다:

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 정보 얻기

`Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드로 현재 요청을 처리하는 라우트의 정보를 얻을 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

`Route` 파사드의 [내부 클래스](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Router.html)와 [Route 인스턴스](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Route.html)의 API 문서를 참조해, 라우터/라우트 클래스에서 사용 가능한 모든 메서드를 확인할 수 있습니다.

<a name="cors"></a>
## 교차 출처 리소스 공유(CORS)

라라벨은 여러분이 설정한 값에 따라, CORS `OPTIONS` HTTP 요청에 자동으로 응답할 수 있습니다. 이러한 `OPTIONS` 요청은 애플리케이션 글로벌 미들웨어 스택에 포함된 `HandleCors` [미들웨어](/docs/{{version}}/middleware)에 의해 자동 처리됩니다.

때로는 애플리케이션의 CORS 설정값을 직접 커스터마이즈할 수 있습니다. `config:publish` Artisan 명령어로 `cors` 설정 파일을 퍼블리싱하세요:

```shell
php artisan config:publish cors
```

이 명령은 `config` 디렉터리에 `cors.php` 설정 파일을 생성합니다.

> [!NOTE]
> CORS 및 CORS 헤더에 대한 자세한 정보는 [MDN 웹 문서](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱

프로덕션 서버에 애플리케이션을 배포할 때, 라라벨의 라우트 캐시를 적극 사용하는 것이 좋습니다. 라우트 캐시를 사용하면 애플리케이션의 모든 라우트를 등록하는 데 걸리는 시간이 현저히 감소합니다. 라우트 캐시 생성을 위해서는 다음 Artisan 명령을 실행하세요:

```shell
php artisan route:cache
```

이 명령을 실행하면, 모든 요청마다 캐시된 라우트 파일이 로드됩니다. 새로운 라우트를 추가했다면 반드시 라우트 캐시를 새로 생성해야 하므로, `route:cache`는 프로젝트 배포 시에만 실행하도록 하세요.

라우트 캐시는 다음 명령어로 삭제할 수 있습니다:

```shell
php artisan route:clear
```
