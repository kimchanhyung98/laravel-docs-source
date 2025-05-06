# 라우팅(Routing)

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리디렉션 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록 조회](#listing-your-routes)
    - [라우팅 커스터마이즈](#routing-customization)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [옵션 파라미터](#parameters-optional-parameters)
    - [정규식 제약](#parameters-regular-expression-constraints)
- [네임드 라우트](#named-routes)
- [라우트 그룹](#route-groups)
    - [미들웨어](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [서브도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 프리픽스](#route-group-prefixes)
    - [라우트 네임 프리픽스](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암시적 바인딩](#implicit-binding)
    - [Enum 암시적 바인딩](#implicit-enum-binding)
    - [명시적 바인딩](#explicit-binding)
- [폴백 라우트](#fallback-routes)
- [요청 제한(Rate Limiting)](#rate-limiting)
    - [요청 제한자 정의](#defining-rate-limiters)
    - [라우트에 제한자 적용](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근하기](#accessing-the-current-route)
- [교차 출처 리소스 공유(CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅

가장 기본적인 Laravel 라우트는 URI와 클로저(익명 함수)를 받아, 복잡한 라우팅 설정 파일 없이 쉽고 간결하게 라우트와 동작을 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일

모든 Laravel 라우트는 `routes` 디렉터리에 위치한 라우트 파일에 정의됩니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 지정된 설정에 따라 Laravel이 자동으로 불러옵니다. `routes/web.php` 파일은 웹 인터페이스를 위한 라우트를 정의합니다. 이 라우트들은 세션 상태와 CSRF 보호 기능을 제공하는 `web` [미들웨어 그룹](/docs/{{version}}/middleware#laravels-default-middleware-groups)에 할당됩니다.

대부분의 애플리케이션은 `routes/web.php` 파일에 라우트를 정의하는 것부터 시작합니다. `routes/web.php`에 정의된 라우트는 브라우저에서 해당 URL로 접속하여 접근할 수 있습니다. 예를 들어, 다음과 같은 라우트는 브라우저에서 `http://example.com/user`로 접속하면 호출됩니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트

애플리케이션이 상태 없는 API도 제공해야 한다면, `install:api` 아티즌 명령어로 API 라우팅을 활성화할 수 있습니다:

```shell
php artisan install:api
```

`install:api` 명령어는 [Laravel Sanctum](/docs/{{version}}/sanctum)를 설치해, 서드파티 API 소비자, SPA, 모바일 앱 등에서 인증에 사용할 수 있는 강력하면서도 간단한 API 토큰 인증 가드를 제공합니다. 또한 `routes/api.php` 파일도 생성됩니다:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

`routes/api.php` 파일 내의 라우트들은 상태가 없으며, `api` [미들웨어 그룹](/docs/{{version}}/middleware#laravels-default-middleware-groups)에 할당됩니다. 또, 이 라우트들에는 `/api` URI 프리픽스가 자동으로 적용되므로 파일의 모든 라우트에 프리픽스를 수동으로 지정할 필요가 없습니다. 프리픽스는 애플리케이션의 `bootstrap/app.php` 파일에서 변경할 수 있습니다:

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

여러 HTTP 메서드에 응답해야 하는 라우트를 등록해야 할 때도 있습니다. 이런 경우 `match` 메서드를 사용할 수 있습니다. 아니면, `any` 메서드를 사용해 모든 HTTP 메서드에 응답하는 라우트를 등록할 수 있습니다:

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일한 URI를 공유하는 여러 라우트를 정의할 때, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트는 `any`, `match`, `redirect` 메서드를 사용하는 라우트보다 먼저 정의해야 합니다. 이는 들어오는 요청이 올바른 라우트와 매칭될 수 있도록 하기 위함입니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백 함수 시그니처에 필요한 의존성을 타입힌트할 수 있습니다. 선언된 의존성들은 Laravel [서비스 컨테이너](/docs/{{version}}/container)에 의해 자동으로 주입됩니다. 예를 들어, `Illuminate\Http\Request` 클래스를 타입힌트하면 현재 HTTP 요청이 자동으로 라우트 콜백에 주입됩니다:

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 라우트로 향하는 모든 HTML 폼에는 CSRF 토큰 필드가 포함되어야 합니다. 그렇지 않으면 요청이 거부됩니다. CSRF 보호에 대해 자세히 알고 싶다면 [CSRF 문서](/docs/{{version}}/csrf)를 참고하세요:

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리디렉션 라우트

다른 URI로 리디렉션하는 라우트를 정의하려면 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 간단한 리디렉션을 위해 전체 라우트나 컨트롤러를 정의할 필요없이 편리하게 사용할 수 있습니다:

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 선택적 세 번째 파라미터로 상태 코드를 지정할 수 있습니다:

```php
Route::redirect('/here', '/there', 301);
```

또는, `Route::permanentRedirect` 메서드를 사용해 `301` 상태 코드를 반환할 수도 있습니다:

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리디렉션 라우트에서 라우트 파라미터를 사용할 때, `destination`과 `status` 파라미터는 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰(View) 라우트

라우트가 단순히 [뷰](/docs/{{version}}/views)만 반환하면 되는 경우, `Route::view` 메서드를 사용할 수 있습니다. 이 메서드는 `redirect`처럼 전체 라우트나 컨트롤러를 정의하지 않고도 쉽게 사용할 수 있게 해줍니다. 첫 번째 인자는 URI, 두 번째 인자는 뷰 이름이고, 세 번째 파라미터로 전달 데이터를 배열로 넘길 수 있습니다:

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 파라미터를 사용할 때, `view`, `data`, `status`, `headers` 파라미터는 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 조회

`route:list` 아티즌 명령어를 사용하면 애플리케이션에 정의된 모든 라우트를 한 눈에 확인할 수 있습니다:

```shell
php artisan route:list
```

기본적으로 `route:list` 출력에는 각 라우트에 할당된 라우트 미들웨어가 표시되지 않지만, 명령에 `-v` 옵션을 추가하면 라우트 미들웨어와 미들웨어 그룹 이름도 확인할 수 있습니다:

```shell
php artisan route:list -v

# 미들웨어 그룹 자세히 보기...
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 보고 싶다면 아래처럼 사용할 수 있습니다:

```shell
php artisan route:list --path=api
```

또한, `route:list` 명령 실행시 `--except-vendor` 옵션을 제공하면 서드파티 패키지에서 정의한 라우트를 숨길 수 있습니다:

```shell
php artisan route:list --except-vendor
```

반대로, `--only-vendor` 옵션을 제공하면 서드파티 패키지에서 정의한 라우트만 볼 수 있습니다:

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우팅 커스터마이즈

기본적으로, 애플리케이션의 모든 라우트는 `bootstrap/app.php` 파일에 의해 설정 및 로드됩니다:

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

하지만, 애플리케이션의 일부 라우트를 완전히 별도의 파일에서 관리하고 싶을 수도 있습니다. 이를 위해 `withRouting` 메서드에 `then` 클로저를 전달할 수 있습니다. 이 클로저 내부에서 필요한 추가 라우트 등록이 가능합니다:

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

또는, `withRouting` 메서드에 `using` 클로저를 전달해 라우트 등록을 완전히 직접 제어할 수도 있습니다. 이 파라미터를 전달하면 프레임워크가 HTTP 라우트를 자동 등록하지 않고, 모든 라우트를 수동으로 등록해야 합니다:

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

때로는 라우트에서 URI의 일부 세그먼트를 받아와야 할 필요가 있습니다. 예를 들어, URL에서 특정 사용자의 ID를 받아와야 할 수 있습니다. 아래와 같이 라우트 파라미터를 정의할 수 있습니다:

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요하다면 여러 개의 라우트 파라미터를 정의할 수도 있습니다:

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 파라미터는 항상 `{}` 중괄호로 감싸며, 파라미터 이름에는 영문자와 밑줄(`_`)만 사용할 수 있습니다. 파라미터들은 정의된 순서대로 콜백이나 컨트롤러로 주입됩니다. 파라미터 이름과 콜백/컨트롤러의 인자 이름이 일치할 필요는 없습니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입

라우트에 서비스 컨테이너가 자동으로 주입해주길 바라는 의존성이 있는 경우, 의존성을 먼저 선언한 후 라우트 파라미터를 적어 주어야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 옵션 파라미터

가끔 URI에 항상 존재하지 않을 수도 있는 라우트 파라미터가 필요할 수 있습니다. 이럴 때는 파라미터 이름 뒤에 `?`를 붙이면 됩니다. 라우트의 콜백 인자에도 기본 값을 지정해야 합니다:

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규식 제약

`where` 메서드를 사용하여 라우트 파라미터의 값을 정규식으로 제약할 수 있습니다. `where`의 첫 번째 인자는 파라미터 이름, 두 번째는 정규식 패턴입니다:

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

자주 쓰이는 정규식 패턴을 쉽게 적용할 수 있도록 헬퍼 메서드도 준비되어 있습니다:

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

들어오는 요청이 라우트 패턴의 제약을 충족하지 않으면 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 글로벌 제약

특정 라우트 파라미터를 항상 지정한 정규식으로 제약하고 싶다면 `pattern` 메서드를 사용할 수 있습니다. 이 패턴은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 정의하십시오:

```php
use Illuminate\Support\Facades\Route;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Route::pattern('id', '[0-9]+');
}
```

패턴이 정의되면 해당 파라미터 이름이 사용되는 모든 라우트에 자동으로 적용됩니다:

```php
Route::get('/user/{id}', function (string $id) {
    // {id}가 숫자일 때만 실행...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시(`/`)

Laravel 라우팅 컴포넌트는 `/` 를 제외한 모든 문자가 라우트 파라미터 값에 올 수 있도록 허용합니다. `/` 를 파라미터에 허용하려면 `where`에 정규식으로 명시적으로 허용해야 합니다:

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 마지막 라우트 세그먼트에서만 지원됩니다.

<a name="named-routes"></a>
## 네임드 라우트

네임드 라우트(named route)를 이용하면 특정 라우트에 대해 URL이나 리디렉션을 더욱 편리하게 생성할 수 있습니다. 라우트 정의에 `name` 메서드를 체이닝하여 이름을 지정할 수 있습니다:

```php
Route::get('/user/profile', function () {
    // ...
})->name('profile');
```

컨트롤러 액션에도 네임드 라우트를 지정할 수 있습니다:

```php
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!WARNING]
> 라우트 이름은 항상 유일해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 네임드 라우트의 URL 생성

라우트에 이름이 부여되면, `route`와 `redirect` 헬퍼 함수를 통해 해당 이름을 사용해 URL이나 리디렉션을 생성할 수 있습니다:

```php
// URL 생성...
$url = route('profile');

// 리디렉션 생성...
return redirect()->route('profile');

return to_route('profile');
```

네임드 라우트가 파라미터를 정의하고 있다면, `route` 함수의 두 번째 인자에 파라미터 배열을 전달할 수 있습니다. 전달된 파라미터는 알맞게 URL에 치환됩니다:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

파라미터 배열에 추가적인 값을 전달하면, 쿼리스트링에 자동으로 붙게 됩니다:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// /user/1/profile?photos=yes
```

> [!NOTE]
> URL 파라미터에 대해 요청 전역 기본값을 지정하고 싶을 때가 있습니다. 예를 들어 현재 로케일 값을 사용할 수도 있습니다. 이 경우 [`URL::defaults` 메서드](/docs/{{version}}/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 확인하기

현재 요청이 특정 네임드 라우트에 매칭되었는지 확인하려면, Route 인스턴스에서 `named` 메서드를 사용할 수 있습니다. 예를 들어, 미들웨어에서 현재 라우트 이름을 확인하려면 다음과 같이 할 수 있습니다:

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

라우트 그룹을 사용하면 미들웨어와 같은 라우트 속성을 여러 라우트에 반복 정의하지 않고 한번에 적용할 수 있습니다.

중첩 그룹에서는 속성이 "지능적으로" 병합됩니다. 미들웨어와 `where` 조건은 병합되고, 네임과 프리픽스는 덧붙여집니다. 네임스페이스 구분자와 URI 프리픽스의 슬래시는 자동으로 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

그룹 내 모든 라우트에 [미들웨어](/docs/{{version}}/middleware)를 적용하려면 라우트 그룹 선언 전에 `middleware` 메서드를 사용할 수 있습니다. 미들웨어는 배열에 작성된 순서대로 실행됩니다:

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first, second 미들웨어 사용...
    });

    Route::get('/user/profile', function () {
        // first, second 미들웨어 사용...
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러

여러 라우트가 모두 동일한 [컨트롤러](/docs/{{version}}/controllers)를 사용한다면, `controller` 메서드로 그룹 내 모든 라우트에 공통 컨트롤러를 지정할 수 있습니다. 개별 라우트 정의시에는 컨트롤러 메서드만 지정하면 됩니다:

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

서브도메인 라우팅에도 라우트 그룹을 사용할 수 있습니다. 서브도메인에도 라우트 파라미터를 사용할 수 있어, 라우트나 컨트롤러에서 서브도메인의 일부를 활용할 수 있습니다. `domain` 메서드로 서브도메인을 지정할 수 있습니다:

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

> [!WARNING]
> 서브도메인 라우트가 루트 도메인 라우트보다 먼저 등록되어야 정상적으로 동작합니다. 그렇지 않으면 동일한 URI 경로를 가지는 루트 도메인 라우트가 우선 처리됩니다.

<a name="route-group-prefixes"></a>
### 라우트 프리픽스

`prefix` 메서드를 사용하면 그룹 내 모든 라우트 URI에 지정한 프리픽스를 일괄 추가할 수 있습니다. 예를 들어, 그룹의 모든 URI를 `admin`으로 시작하도록 만들려면 다음처럼 합니다:

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL과 매칭됨
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 네임 프리픽스

`name` 메서드를 사용하면 그룹 내 모든 라우트의 이름에 지정한 접두사를 일괄 추가할 수 있습니다. 예를 들어, 그룹의 모든 라우트에 `admin` 접두사를 붙이려면 다음과 같이 합니다. 뒷부분에 `.`을 붙여줍니다:

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // 라우트 이름이 "admin.users"로 할당됨...
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩

라우트나 컨트롤러에서 모델 ID를 받을 때, 데이터베이스에서 해당 모델을 직접 조회하는 대신, Laravel의 라우트 모델 바인딩 기능을 사용해 자동으로 모델 인스턴스를 주입받을 수 있습니다. 즉, 사용자 ID 대신 해당하는 `User` 모델 인스턴스 전체를 바로 받을 수 있습니다.

<a name="implicit-binding"></a>
### 암시적(Implicit) 바인딩

Eloquent 모델을 라우트나 컨트롤러 액션에서 타입힌트하고, 변수 이름을 URI 세그먼트와 동일하게 하면, Laravel은 자동으로 해당 모델 인스턴스를 주입합니다. 예시:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

`$user` 변수가 `App\Models\User` Eloquent 모델로 타입힌트되고, 변수명도 `{user}` URI 세그먼트와 일치하므로, 해당 ID와 매칭되는 모델 인스턴스가 자동으로 주입됩니다. 데이터베이스에서 일치하는 모델이 없으면 404 HTTP 응답이 자동으로 발생합니다.

컨트롤러 사용시에도 동일하게 암시적 바인딩이 동작합니다. `{user}` URI 세그먼트가 컨트롤러의 `$user` 변수와 매칭되어 `App\Models\User` 인스턴스가 주입됩니다:

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

암시적 모델 바인딩은 기본적으로 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 하지만 라우트에 `withTrashed` 메서드를 체이닝하면, 소프트 삭제된 모델까지 조회할 수 있습니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 변경

항상 `id` 컬럼이 아닌, 다른 컬럼을 기준으로 모델을 조회하고 싶을 때는 라우트 파라미터에 컬럼명을 지정할 수 있습니다:

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

특정 모델 클래스에 대해 항상 `id` 이외의 컬럼을 키로 사용하고 싶다면, Eloquent 모델에서 `getRouteKeyName` 메서드를 오버라이드 하면 됩니다:

```php
/**
 * 모델의 라우트 키를 반환
 */
public function getRouteKeyName(): string
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
#### 커스텀 키와 "스코핑(Scoping)"

단일 라우트 정의에 여러 Eloquent 모델을 암시적으로 바인딩할 때, 두 번째 모델이 첫 번째 모델의 하위임을 보장하는 쿼리 스코핑을 원하는 경우가 있습니다. 예를 들어, 특정 유저의 블로그 포스트를 슬러그로 조회할 경우 다음과 같이 할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

이처럼 커스텀 키 암시적 바인딩이 중첩 파라미터로 사용되면, Laravel은 두 번째 Eloquent 모델을 첫 번째 모델의 자식으로 쿼리를 스코프합니다. 위 예시에서 `User` 모델이 `posts`라는 관계(파라미터 복수형)를 가진 것으로 간주하고, 그 관계를 통해 `Post` 모델을 찾습니다.

커스텀 키를 사용하지 않을 때도, `scopeBindings` 메서드를 호출해 하위 바인딩에 스코핑을 명시적으로 적용할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는, 라우트 그룹 전체에 스코프 바인딩을 적용할 수도 있습니다:

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로, 스코프 바인딩을 적용하지 않도록 하려면 `withoutScopedBindings` 메서드를 사용하세요:

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 모델이 없을 때의 동작 커스터마이즈

암시적 모델 바인딩에서 모델 인스턴스를 찾지 못하면 404 HTTP 응답이 반환되는 게 기본입니다. 하지만 이 동작을 변경하고 싶다면, 라우트 정의시 `missing` 메서드에 클로저를 넘기면 됩니다:

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
### Enum 암시적 바인딩

PHP 8.1부터는 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 지원합니다. 이를 활용해 Laravel에서는 라우트 파라미터를 [문자열 기반 Enum](https://www.php.net/manual/en/language.enumerations.backed.php)으로 타입힌트할 수 있습니다. 해당 세그먼트가 Enum 값으로 유효할 때만 라우트가 실행되며, 그렇지 않으면 404 HTTP 응답이 반환됩니다. 예를 들어:

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

이제 `{category}` 라우트 세그먼트가 `fruits` 또는 `people`일 때만 라우트가 실행됩니다. 그 외의 값이면 404가 반환됩니다:

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적(Explicit) 바인딩

암시적(관례 기반) 모델 바인딩을 사용할 필요는 없습니다. 라우트 파라미터와 모델 간의 매핑을 명시적으로 정의할 수도 있습니다. 명시적 바인딩을 등록하려면 라우터의 `model` 메서드를 사용해 특정 파라미터와 모델 클래스를 지정합니다. 보통은 `AppServiceProvider`의 `boot` 메서드 초반에 작성합니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Route::model('user', User::class);
}
```

이제 `{user}` 파라미터가 포함된 라우트를 정의합니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

이처럼 모든 `{user}` 파라미터는 `App\Models\User` 모델에 바인딩되며, 예를 들어 `users/1` 요청 시 ID가 1인 User 인스턴스가 주입됩니다. 데이터베이스에 모델이 없으면 404 HTTP 응답이 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 해법 커스터마이즈

커스텀한 모델 바인딩 로직을 직접 정의하고 싶다면 `Route::bind` 메서드를 사용하세요. 이 메서드에 전달한 클로저는 URI 세그먼트 값을 받고, 최종적으로 라우트에 주입할 모델 인스턴스를 반환해야 합니다. 역시 `AppServiceProvider`의 `boot` 메서드에서 작성하면 됩니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Route::bind('user', function (string $value) {
        return User::where('name', $value)->firstOrFail();
    });
}
```

또는, Eloquent 모델에서 `resolveRouteBinding` 메서드를 오버라이드 할 수도 있습니다. 이 메서드는 URI 세그먼트 값을 받아, 삽입할 모델 인스턴스를 반환해야 합니다:

```php
/**
 * 바인딩 값으로 모델을 찾음
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

라우트가 [암시적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용할 경우, `resolveChildRouteBinding` 메서드가 부모 모델 아래의 하위 바인딩을 해결하는 데 사용됩니다:

```php
/**
 * 바인딩 값으로 하위 모델을 찾음
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

`Route::fallback` 메서드를 사용하면 어떤 라우트와도 매칭되지 않았을 때 실행될 라우트를 정의할 수 있습니다. 처리되지 않은 요청은 예외 핸들러를 통해 자동으로 "404" 페이지를 렌더링합니다. 그러나, `fallback` 라우트는 보통 `routes/web.php`에 정의되기 때문에 `web` 미들웨어 그룹 내의 모든 미들웨어가 적용됩니다. 필요하다면 추가 미들웨어도 붙일 수 있습니다:

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 요청 제한(Rate Limiting)

<a name="defining-rate-limiters"></a>
### 요청 제한자 정의

Laravel은 특정 라우트 또는 라우트 그룹에 대한 트래픽을 제한할 수 있는 강력하고 커스터마이즈 가능한 요청 제한 서비스를 기본 제공합니다. 사용하려면 애플리케이션에 맞는 요청 제한자 구성을 먼저 정의해야 합니다.

요청 제한자는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의할 수 있습니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 서비스 부트스트랩
 */
protected function boot(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
}
```

요청 제한자는 `RateLimiter` 파사드의 `for` 메서드를 사용하여 정의합니다. 이 메서드는 제한자 이름과 제한 설정을 반환하는 클로저를 받습니다. 제한 설정은 `Illuminate\Cache\RateLimiting\Limit` 클래스의 인스턴스이며, 빌더 메서드를 통해 제한 조건을 쉽게 정의할 수 있습니다. 제한자 이름은 임의의 문자열을 지정할 수 있습니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 서비스 부트스트랩
 */
protected function boot(): void
{
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });
}
```

지정된 제한치를 넘는 요청이 들어오면 Laravel이 자동으로 429 HTTP 상태 코드로 응답합니다. 제한자를 위한 커스텀 응답을 지정하고 싶다면 `response` 메서드를 사용할 수 있습니다:

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

제한자 콜백은 요청 인스턴스를 전달받으므로, 인증된 사용자나 요청 정보를 바탕으로 동적으로 제한을 지정할 수 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
#### 제한 분할(Segmenting)

경우에 따라 특정 기준별로 제한을 분할하고 싶을 수 있습니다. 예를 들어, 모든 IP 주소당 1분에 100번씩 접근을 허용하려면 `by` 메서드를 쓸 수 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

또 다른 예로, 인증 유저 ID별로는 분당 100회, 비회원일 경우 IP별로 분당 10회로 제한할 수도 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 다중 제한자(Multiple Rate Limits)

필요하다면 하나의 제한자 구성에서 제한 설정을 배열로 여러 개 반환할 수 있습니다. 각 제한은 작성된 순서대로 해당 라우트에 평가됩니다:

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

동일한 `by` 값으로 분할된 제한을 여러 개 지정할 경우, 각 `by` 값이 유일하도록 프리픽스를 붙여주세요:

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 제한자 적용

요청 제한자는 `throttle` [미들웨어](/docs/{{version}}/middleware)를 사용하여 라우트나 라우트 그룹에 적용할 수 있습니다. `throttle` 미들웨어 파라미터로 제한자 이름을 지정합니다:

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

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스로 매핑되어 있습니다. 하지만 애플리케이션의 캐시 드라이버로 Redis를 사용한다면, Laravel에 Redis를 사용해 요청 제한을 관리하도록 지시할 수 있습니다. `bootstrap/app.php`에서 `throttleWithRedis` 메서드를 사용하면 됩니다. 이 경우 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 미들웨어로 매핑됩니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 폼 메서드 스푸핑(Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 메서드를 직접 지원하지 않습니다. 그래서 HTML 폼에서 `PUT`, `PATCH`, `DELETE` 라우트를 호출하려면, 폼 내에 숨겨진 `_method` 필드를 추가해야 합니다. `_method` 필드로 전달된 값이 HTTP 요청 메서드로 사용됩니다:

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

더 편리하게는, `@method` [Blade 지시어](/docs/{{version}}/blade)를 사용해 `_method` 입력 필드를 생성할 수 있습니다:

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 접근하기

`Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 사용해 현재 요청을 처리 중인 라우트 정보를 알 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

라우터와 라우트 클래스에서 사용 가능한 전체 메서드는 [Route 파사드의 클래스 문서](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Router.html)와 [Route 인스턴스 문서](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Route.html)를 참고하세요.

<a name="cors"></a>
## 교차 출처 리소스 공유(CORS)

Laravel은 CORS의 `OPTIONS` HTTP 요청에 대해, 구성 값에 따라 자동으로 응답할 수 있습니다. `OPTIONS` 요청은 전역 미들웨어 스택에 기본 포함된 `HandleCors` [미들웨어](/docs/{{version}}/middleware)에 의해 자동으로 처리됩니다.

애플리케이션의 CORS 구성 값을 커스터마이즈해야 할 경우, `config:publish` 아티즌 명령어로 `cors` 설정 파일을 퍼블리시할 수 있습니다:

```shell
php artisan config:publish cors
```

이 명령어는 애플리케이션의 `config` 디렉터리에 `cors.php` 설정 파일을 생성합니다.

> [!NOTE]
> CORS 및 CORS 헤더에 대한 추가 정보는 [MDN 웹 문서](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱(Route Caching)

프로덕션 서버에 애플리케이션을 배포할 때, Laravel의 라우트 캐시 기능을 사용하세요. 라우트 캐시는 모든 라우트 등록 시간을 획기적으로 단축해줍니다. 라우트 캐쉬를 생성하려면 `route:cache` 아티즌 명령어를 실행합니다:

```shell
php artisan route:cache
```

이 커맨드를 실행하면 모든 요청마다 캐시된 라우트 파일이 로드됩니다. 새로운 라우트를 추가하면 반드시 라우트 캐시를 다시 생성해야 하므로, 이 명령은 보통 배포 시점에만 실행하세요.

라우트 캐시는 `route:clear` 명령어로 삭제할 수 있습니다:

```shell
php artisan route:clear
```