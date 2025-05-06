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
    - [정규 표현식 제약](#parameters-regular-expression-constraints)
- [네임드 라우트](#named-routes)
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
- [속도 제한](#rate-limiting)
    - [속도 제한자 정의](#defining-rate-limiters)
    - [라우트에 속도 제한자 추가](#attaching-rate-limiters-to-routes)
- [Form 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근](#accessing-the-current-route)
- [교차 출처 리소스 공유(CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅

가장 기본적인 Laravel 라우트는 URI와 클로저를 받아, 복잡한 라우팅 설정 파일 없이 간단하고 표현력 있게 라우트와 동작을 정의할 수 있습니다.

    use Illuminate\Support\Facades\Route;

    Route::get('/greeting', function () {
        return 'Hello World';
    });

<a name="the-default-route-files"></a>
### 기본 라우트 파일

모든 Laravel 라우트는 `routes` 디렉터리에 위치한 라우트 파일에서 정의합니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 지정된 설정에 따라 자동으로 불러와집니다. `routes/web.php` 파일은 웹 인터페이스용 라우트를 정의합니다. 이들 라우트에는 세션 상태, CSRF 보호와 같은 기능을 제공하는 `web` [미들웨어 그룹](/docs/{{version}}/middleware#laravels-default-middleware-groups)이 할당됩니다.

대부분의 애플리케이션은 `routes/web.php` 파일에서 라우트를 정의하는 것부터 시작합니다. `routes/web.php`에 정의된 라우트들은 브라우저에서 해당 URL로 접근할 수 있습니다. 예를 들어, 다음 라우트는 브라우저에서 `http://example.com/user`로 이동하여 접근할 수 있습니다.

    use App\Http\Controllers\UserController;

    Route::get('/user', [UserController::class, 'index']);

<a name="api-routes"></a>
#### API 라우트

애플리케이션에서 상태를 저장하지 않는 API도 제공하려면 `install:api` Artisan 명령어를 사용하여 API 라우팅을 활성화할 수 있습니다.

```shell
php artisan install:api
```

`install:api` 명령은 [Laravel Sanctum](/docs/{{version}}/sanctum)을 설치합니다. Sanctum은 써드파티 API, SPA 또는 모바일 앱 인증에 사용할 수 있는 강력하고 간단한 API 토큰 인증 가드를 제공합니다. 또한 `install:api` 명령은 `routes/api.php` 파일을 생성합니다.

    Route::get('/user', function (Request $request) {
        return $request->user();
    })->middleware('auth:sanctum');

`routes/api.php`의 라우트는 상태를 저장하지 않으며 `api` [미들웨어 그룹](/docs/{{version}}/middleware#laravels-default-middleware-groups)에 지정됩니다. 또한 `/api` URI 프리픽스가 자동으로 적용되므로, 매 라우트마다 수동으로 프리픽스를 지정할 필요가 없습니다. 프리픽스는 애플리케이션의 `bootstrap/app.php` 파일을 수정해서 변경할 수 있습니다.

    ->withRouting(
        api: __DIR__.'/../routes/api.php',
        apiPrefix: 'api/admin',
        // ...
    )

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메소드

라우터는 모든 HTTP 메서드에 응답하는 라우트를 등록할 수 있습니다.

    Route::get($uri, $callback);
    Route::post($uri, $callback);
    Route::put($uri, $callback);
    Route::patch($uri, $callback);
    Route::delete($uri, $callback);
    Route::options($uri, $callback);

여러 HTTP 메서드에 응답하는 라우트를 등록해야 하는 경우 `match` 메소드를 사용할 수 있습니다. 모든 HTTP 메서드에 대응시키려면 `any` 메서드를 사용합니다.

    Route::match(['get', 'post'], '/', function () {
        // ...
    });

    Route::any('/', function () {
        // ...
    });

> [!NOTE]
> 동일한 URI를 공유하는 여러 라우트를 정의할 때는, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트를 `any`, `match`, `redirect` 메서드보다 먼저 정의해야 요청이 올바른 라우트와 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백 시그니처에 필요한 의존성을 타입힌트로 지정할 수 있습니다. 명시된 의존성은 Laravel [서비스 컨테이너](/docs/{{version}}/container)에 의해 자동으로 주입됩니다. 예를 들어, `Illuminate\Http\Request` 클래스를 타입힌트로 지정하면 현재 HTTP 요청이 자동으로 주입됩니다.

    use Illuminate\Http\Request;

    Route::get('/users', function (Request $request) {
        // ...
    });

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 라우트로 전송하는 모든 HTML 폼에는 CSRF 토큰 필드를 반드시 포함해야 합니다. 그렇지 않으면 요청이 거부됩니다. 자세한 내용은 [CSRF 문서](/docs/{{version}}/csrf)를 참고하세요.

    <form method="POST" action="/profile">
        @csrf
        ...
    </form>

<a name="redirect-routes"></a>
### 리디렉션 라우트

다른 URI로 리디렉션하는 라우트를 정의할 때는 `Route::redirect` 메서드를 사용할 수 있습니다. 간단한 리디렉션에 굳이 라우트나 컨트롤러를 별도로 만들 필요 없이 편리하게 사용할 수 있습니다.

    Route::redirect('/here', '/there');

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 세 번째 인자를 통해 상태 코드를 지정할 수 있습니다.

    Route::redirect('/here', '/there', 301);

또는, `Route::permanentRedirect` 메서드를 사용하면 자동으로 `301` 상태 코드를 반환합니다.

    Route::permanentRedirect('/here', '/there');

> [!WARNING]
> 리디렉션 라우트에서 라우트 파라미터를 사용할 때는 `destination`과 `status`라는 파라미터명이 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트

라우트가 [뷰](/docs/{{version}}/views)만 반환하면 된다면 `Route::view` 메소드를 사용할 수 있습니다. `view` 메서드는 간단한 라우트 정의를 편리하게 만들어 줍니다. 첫 번째 인자로 URI, 두 번째 인자로 뷰 이름을 받고, 세 번째 인자로는 뷰에 전달할 데이터 배열을 옵션으로 지정할 수 있습니다.

    Route::view('/welcome', 'welcome');

    Route::view('/welcome', 'welcome', ['name' => 'Taylor']);

> [!WARNING]
> 뷰 라우트의 파라미터에서 `view`, `data`, `status`, `headers`라는 이름은 Laravel 예약 파라미터이므로 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 확인

`route:list` Artisan 명령을 사용하여 애플리케이션에 정의된 모든 라우트를 쉽게 확인할 수 있습니다.

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 미들웨어는 `route:list` 출력에 표시되지 않지만, `-v` 옵션을 추가하면 라우트 미들웨어와 미들웨어 그룹명을 볼 수 있습니다.

```shell
php artisan route:list -v

# 미들웨어 그룹 펼치기
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 확인하려면 다음과 같이 할 수 있습니다.

```shell
php artisan route:list --path=api
```

또한, 써드파티 패키지에서 정의한 라우트를 숨기고 싶다면 `--except-vendor` 옵션을 사용할 수 있습니다.

```shell
php artisan route:list --except-vendor
```

반대로, 오직 써드파티 패키지에서 정의한 라우트만 출력하고 싶다면 `--only-vendor` 옵션을 사용합니다.

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

하지만 라우트 일부를 별도의 파일에 분리해서 정의하고 싶을 때는 `withRouting` 메소드에 `then` 클로저를 넘길 수 있습니다. 이 클로저 내부에서 필요에 따라 추가 라우트를 등록할 수 있습니다.

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

더 나아가 라우트 등록을 완전히 직접 제어하고 싶으면 `withRouting` 메소드에 `using` 클로저를 사용할 수 있습니다. 이 경우 프레임워크는 HTTP 라우트를 자동으로 등록하지 않으며, 모든 라우트를 직접 수동 등록해야 합니다.

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

경우에 따라 라우트에서 URI의 일부를 캡처해야 할 수도 있습니다. 예를 들어, URL에서 사용자의 ID를 받아와야 할 때 라우트 파라미터를 사용할 수 있습니다.

    Route::get('/user/{id}', function (string $id) {
        return 'User '.$id;
    });

필요한 만큼 파라미터를 정의할 수 있습니다.

    Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
        // ...
    });

라우트 파라미터는 항상 `{}` 중괄호로 감싸야 하며, 알파벳 문자로 구성되어야 합니다. 파라미터 이름에는 밑줄(`_`)도 사용할 수 있습니다. 파라미터는 정의된 순서대로 콜백/컨트롤러에 주입되므로, 인자 이름은 중요하지 않습니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입

라우트에 필요로 하는 의존성(예: Request 등)이 있을 때는, 의존성 주입 인자 뒤에 라우트 파라미터를 나열해야 합니다.

    use Illuminate\Http\Request;

    Route::get('/user/{id}', function (Request $request, string $id) {
        return 'User '.$id;
    });

<a name="parameters-optional-parameters"></a>
### 선택적 파라미터

때로는 라우트 파라미터가 반드시 있을 필요가 없는 경우도 있습니다. 이럴 경우 파라미터명 뒤에 `?`를 붙이면 됩니다. 대응되는 변수에는 반드시 기본값을 지정해야 합니다.

    Route::get('/user/{name?}', function (?string $name = null) {
        return $name;
    });

    Route::get('/user/{name?}', function (?string $name = 'John') {
        return $name;
    });

<a name="parameters-regular-expression-constraints"></a>
### 정규 표현식 제약

`where` 메서드를 사용하면 라우트 파라미터의 형식을 정규 표현식으로 제한할 수 있습니다.

    Route::get('/user/{name}', function (string $name) {
        // ...
    })->where('name', '[A-Za-z]+');

    Route::get('/user/{id}', function (string $id) {
        // ...
    })->where('id', '[0-9]+');

    Route::get('/user/{id}/{name}', function (string $id, string $name) {
        // ...
    })->where(['id' => '[0-9]+', 'name' => '[a-z]+']);

자주 쓰이는 정규표현식 패턴은 헬퍼 메소드로도 빠르게 사용할 수 있습니다.

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

요청이 라우트 패턴 제한에 맞지 않으면 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약

특정 파라미터가 항상 정규 표현식 제약을 받도록 하려면 `pattern` 메서드를 사용할 수 있습니다. 이러한 패턴은 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의합니다.

    use Illuminate\Support\Facades\Route;

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Route::pattern('id', '[0-9]+');
    }

이렇게 하면 해당 파라미터명을 사용하는 모든 라우트에 자동으로 패턴 규칙이 적용됩니다.

    Route::get('/user/{id}', function (string $id) {
        // {id}가 숫자일 때만 실행
    });

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시(`/`)

Laravel 라우팅 컴포넌트는 `/`을 제외한 모든 문자가 라우트 파라미터 값에 포함될 수 있도록 허용합니다. 만약 슬래시(`/`)도 허용하려면 `where` 정규식 조건에 명시적으로 지정해야 합니다.

    Route::get('/search/{search}', function (string $search) {
        return $search;
    })->where('search', '.*');

> [!WARNING]
> 인코딩된 슬래시는 마지막 라우트 세그먼트 내에서만 지원됩니다.

<a name="named-routes"></a>
## 네임드 라우트

네임드 라우트는 특정 라우트의 URL 또는 리디렉트 주소를 간편하게 생성할 수 있습니다. 라우트 정의에 `name` 메서드를 체이닝하여 이름을 지정할 수 있습니다.

    Route::get('/user/profile', function () {
        // ...
    })->name('profile');

컨트롤러 액션에도 라우트 이름을 지정할 수 있습니다.

    Route::get(
        '/user/profile',
        [UserProfileController::class, 'show']
    )->name('profile');

> [!WARNING]
> 라우트 이름은 반드시 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 네임드 라우트로 URL 생성하기

특정 라우트에 이름을 지정하면, Laravel의 `route`, `redirect` 헬퍼 함수를 통해 해당 라우트로 URL을 생성하거나 리디렉트할 수 있습니다.

    // URL 생성
    $url = route('profile');

    // 리디렉트 생성
    return redirect()->route('profile');

    return to_route('profile');

파라미터를 사용하는 네임드 라우트라면 두 번째 인자로 파라미터 배열을 넘기면 됩니다.

    Route::get('/user/{id}/profile', function (string $id) {
        // ...
    })->name('profile');

    $url = route('profile', ['id' => 1]);

여분의 파라미터를 추가하면 쿼리스트링으로 자동 변환되어 URL에 추가됩니다.

    Route::get('/user/{id}/profile', function (string $id) {
        // ...
    })->name('profile');

    $url = route('profile', ['id' => 1, 'photos' => 'yes']);

    // /user/1/profile?photos=yes

> [!NOTE]
> 특정 URL 파라미터(예: 현재 로케일 등)에 대한 기본값을 요청 전역으로 지정하고 싶을 수 있습니다. 이 경우 [`URL::defaults` 메서드](/docs/{{version}}/urls#default-values)를 사용하세요.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 정보 확인

현재 요청이 지정된 네임드 라우트로 라우팅되었는지 확인하려면 Route 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어, 미들웨어에서 현재 라우트 이름을 검증하려면 다음과 같이 사용합니다.

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

<a name="route-groups"></a>
## 라우트 그룹

라우트 그룹을 사용하면 여러 라우트에 공통된 속성(예: 미들웨어)을 각 라우트마다 지정할 필요 없이 한꺼번에 적용할 수 있습니다.

중첩 그룹은 부모 그룹과 속성을 "병합"하려 시도합니다. 미들웨어와 `where` 조건은 병합되고, 이름과 프리픽스는 덧붙여집니다. 네임스페이스 구분자 및 URI 프리픽스의 슬래시는 필요한 곳에 자동 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

[미들웨어](/docs/{{version}}/middleware)를 그룹 내 모든 라우트에 적용하려면, 그룹 정의 앞에 `middleware` 메서드를 사용하세요. 미들웨어는 배열에 지정된 순서대로 실행됩니다.

    Route::middleware(['first', 'second'])->group(function () {
        Route::get('/', function () {
            // first & second 미들웨어 적용
        });

        Route::get('/user/profile', function () {
            // first & second 미들웨어 적용
        });
    });

<a name="route-group-controllers"></a>
### 컨트롤러

여러 라우트가 동일한 [컨트롤러](/docs/{{version}}/controllers)를 사용할 경우, `controller` 메서드로 그룹 내 모든 라우트에 공통 컨트롤러를 지정할 수 있습니다. 이때 개별 라우트 정의에서는 컨트롤러 메서드 이름만 명시하면 됩니다.

    use App\Http\Controllers\OrderController;

    Route::controller(OrderController::class)->group(function () {
        Route::get('/orders/{id}', 'show');
        Route::post('/orders', 'store');
    });

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹은 서브도메인 라우팅에도 사용할 수 있습니다. 서브도메인도 라우트 URI처럼 파라미터를 지정할 수 있어, 경로에 활용할 수 있습니다. 그룹 정의시 `domain` 메서드로 서브도메인을 지정하면 됩니다.

    Route::domain('{account}.example.com')->group(function () {
        Route::get('/user/{id}', function (string $account, string $id) {
            // ...
        });
    });

> [!WARNING]
> 서브도메인 라우트가 실제로 동작하려면 루트 도메인 라우트보다 먼저 등록해야 합니다. 그렇지 않으면 동일한 URI 경로를 가진 루트 도메인 라우트가 서브도메인 라우트를 덮어쓸 수 있습니다.

<a name="route-group-prefixes"></a>
### 라우트 프리픽스

`prefix` 메소드를 사용하면 그룹 내 모든 라우트 URI 앞에 공통 프리픽스를 붙일 수 있습니다. 예를 들어, 그룹 내 모든 라우트가 `admin`으로 시작하게 만들 수 있습니다.

    Route::prefix('admin')->group(function () {
        Route::get('/users', function () {
            // "/admin/users" URL에 매칭
        });
    });

<a name="route-group-name-prefixes"></a>
### 라우트 네임 프리픽스

`name` 메서드를 사용하면 그룹 내 모든 라우트 이름 앞에 공통 문자열을 붙일 수 있습니다. 예를 들어, 라우트 이름에 모두 `admin.`을 붙이고 싶다면 프리픽스 끝에 `.`을 붙여 명시하세요.

    Route::name('admin.')->group(function () {
        Route::get('/users', function () {
            // 라우트 이름: "admin.users"
        })->name('users');
    });

<a name="route-model-binding"></a>
## 라우트 모델 바인딩

모델 ID를 라우트나 컨트롤러 액션에 주입해야 할 때, 일반적으로 데이터베이스에서 해당 모델을 찾습니다. 라라벨의 라우트 모델 바인딩 기능을 사용하면, 라우트에서 모델 ID대신 전체 Eloquent 모델 인스턴스를 자동으로 주입할 수 있습니다.

<a name="implicit-binding"></a>
### 암시적 바인딩

변수명이 라우트 세그먼트명과 일치하는 타입힌트 Eloquent 모델은 라라벨이 자동으로 주입해줍니다.

    use App\Models\User;

    Route::get('/users/{user}', function (User $user) {
        return $user->email;
    });

`$user` 변수가 `App\Models\User` 타입이며, `{user}` URI 세그먼트와 변수명이 일치하므로, 해당 ID의 모델 인스턴스를 자동 주입합니다. 일치하는 모델이 없으면 404가 자동 반환됩니다.

컨트롤러 메서드에서도 사용 가능합니다.

    use App\Http\Controllers\UserController;
    use App\Models\User;

    // 라우트
    Route::get('/users/{user}', [UserController::class, 'show']);

    // 컨트롤러 메서드
    public function show(User $user)
    {
        return view('user.profile', ['user' => $user]);
    }

<a name="implicit-soft-deleted-models"></a>
#### Soft Delete된 모델 포함

기본적으로 암시적 바인딩은 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)된 모델을 가져오지 않습니다. 소프트 삭제된 모델까지 조회하려면 라우트 정의에 `withTrashed` 메서드를 체이닝합니다.

    use App\Models\User;

    Route::get('/users/{user}', function (User $user) {
        return $user->email;
    })->withTrashed();

<a name="customizing-the-default-key-name"></a>
#### 기본 키명 커스터마이징

기본적으로 `id` 컬럼이지만, 다른 컬럼(ex: `slug`)으로 바인딩하려면 라우트 파라미터에 지정 가능합니다.

    use App\Models\Post;

    Route::get('/posts/{post:slug}', function (Post $post) {
        return $post;
    });

특정 모델에서 항상 기본 키를 변경하려면 모델에서 `getRouteKeyName` 메서드를 오버라이딩합니다.

    /**
     * 모델의 라우트 키 반환
     */
    public function getRouteKeyName(): string
    {
        return 'slug';
    }

<a name="implicit-model-binding-scoping"></a>
#### 커스텀 키와 스코핑

한 라우트에서 여러 Eloquent 모델을 암시적으로 바인딩하는 경우, 두 번째 모델을 상위 모델의 하위로 한정하고 싶을 수 있습니다. 예시를 봅시다.

    use App\Models\Post;
    use App\Models\User;

    Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
        return $post;
    });

이 경우, 라라벨은 `User` 모델이 `posts`라는 관계(즉, 라우트 파라미터명 복수형)로 하위 모델을 가져온다고 가정합니다.  
만약 커스텀 키 없이도 하위 바인딩 스코프를 적용하길 원하면 라우트 정의에 `scopeBindings`를 추가하세요.

    use App\Models\Post;
    use App\Models\User;

    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    })->scopeBindings();

라우트 그룹 전체에 스코프 바인딩을 적용할 수도 있습니다.

    Route::scopeBindings()->group(function () {
        Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
            return $post;
        });
    });

반대로, 스코프 바인딩을 비활성화하려면 `withoutScopedBindings`를 사용하세요.

    Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
        return $post;
    })->withoutScopedBindings();

<a name="customizing-missing-model-behavior"></a>
#### 바인딩 실패시 동작 커스터마이즈

기본적으로 바인딩된 모델을 찾지 못하면 404가 발생합니다. 이 동작을 커스터마이징하려면 라우트 정의에 `missing` 메서드를 체이닝할 수 있습니다.

    use App\Http\Controllers\LocationsController;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Redirect;

    Route::get('/locations/{location:slug}', [LocationsController::class, 'show'])
        ->name('locations.view')
        ->missing(function (Request $request) {
            return Redirect::route('locations.index');
        });

<a name="implicit-enum-binding"></a>
### 암시적 Enum 바인딩

PHP 8.1부터 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)이 지원됩니다. 라라벨에서는 [String-backed Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 라우트에서 타입힌트로 사용할 수 있으며, 해당 세그먼트가 Enum 값 중 하나와 일치해야만 라우트가 실행됩니다. 그렇지 않으면 404가 반환됩니다.

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

아래처럼 `{category}` 세그먼트가 `fruits` 혹은 `people`일 때만 라우트가 실행됩니다.

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩

라라벨의 암시적(관례 기반) 모델 바인딩 대신 명시적으로 라우트 파라미터와 모델을 매핑할 수도 있습니다. 라우터의 `model` 메서드를 사용해 명시적 바인딩을 등록하며, `AppServiceProvider`의 `boot` 메서드 시작 부분에 정의하세요.

    use App\Models\User;
    use Illuminate\Support\Facades\Route;

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Route::model('user', User::class);
    }

그리고 `{user}` 파라미터가 있는 라우트를 정의합니다.

    use App\Models\User;

    Route::get('/users/{user}', function (User $user) {
        // ...
    });

이제 모든 `{user}` 파라미터는 `App\Models\User` 모델 인스턴스로 주입됩니다. 예를 들어 `users/1` 요청시, 데이터베이스에서 ID가 1인 User 인스턴스가 주입됩니다.

모델이 존재하지 않으면 자동으로 404 HTTP 응답이 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 해석 로직 커스터마이즈

커스텀 로직으로 모델을 바인딩하려면 `Route::bind` 메서드를 사용하세요. 이때 클로저는 URI 세그먼트의 값을 받아 해당 모델 인스턴스를 반환해야 합니다. 역시 `AppServiceProvider`의 `boot`에서 정의합니다.

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

또는 Eloquent 모델에서 `resolveRouteBinding` 메서드를 오버라이드할 수도 있습니다.

    /**
     * 바인딩된 값에 대한 모델 반환
     *
     * @param  mixed  $value
     * @param  string|null  $field
     * @return \Illuminate\Database\Eloquent\Model|null
     */
    public function resolveRouteBinding($value, $field = null)
    {
        return $this->where('name', $value)->firstOrFail();
    }

스코프 바인딩(상위-하위 모델 관계)을 사용하는 경우, `resolveChildRouteBinding` 메서드가 호출됩니다.

    /**
     * 바인딩된 값에 대한 하위 모델 반환
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

<a name="fallback-routes"></a>
## 폴백 라우트

`Route::fallback` 메소드를 사용해 다른 어떤 라우트와도 일치하지 않는 경우에 실행되는 라우트를 정의할 수 있습니다. 보통 미처리 요청은 예외 핸들러를 통해 자동으로 404 페이지를 렌더링하지만, `routes/web.php`에서 `fallback` 라우트를 정의하면 `web` 미들웨어 그룹의 미들웨어도 모두 적용됩니다. 필요하다면 추가 미들웨어도 지정할 수 있습니다.

    Route::fallback(function () {
        // ...
    });

<a name="rate-limiting"></a>
## 속도 제한

<a name="defining-rate-limiters"></a>
### 속도 제한자 정의

Laravel에는 라우트 또는 라우트 그룹의 트래픽을 제한할 수 있는 강력하고 커스터마이징 가능한 속도 제한 서비스가 내장되어 있습니다. 먼저, 애플리케이션에 맞는 속도 제한자 구성을 정의하세요.

속도 제한자는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 정의할 수 있습니다.

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

속도 제한자는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다. 이 메서드는 제한자 이름과 제한 설정을 반환하는 클로저를 전달받습니다. 설정은 `Illuminate\Cache\RateLimiting\Limit` 클래스의 인스턴스로 생성하며, 다양한 "빌더" 메서드로 쉽게 제한을 정의할 수 있습니다. 제한자 이름은 원하는 문자열을 사용할 수 있습니다.

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

요청이 제한을 초과하면 429 HTTP 응답이 자동으로 반환됩니다. 커스텀 응답을 반환하고 싶다면 `response` 메서드를 사용할 수 있습니다.

    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
            return response('Custom response...', 429, $headers);
        });
    });

콜백은 HTTP 요청 인스턴스를 받으므로, 사용자나 요청에 따라 동적으로 제한을 설정할 수도 있습니다.

    RateLimiter::for('uploads', function (Request $request) {
        return $request->user()->vipCustomer()
            ? Limit::none()
            : Limit::perMinute(100);
    });

<a name="segmenting-rate-limits"></a>
#### 제한 구간 분할

IP별 등 임의의 기준으로 제한 구간을 나누고 싶을 때는 `by` 메서드를 사용할 수 있습니다.

    RateLimiter::for('uploads', function (Request $request) {
        return $request->user()->vipCustomer()
            ? Limit::none()
            : Limit::perMinute(100)->by($request->ip());
    });

예를 들어, 인증 사용자는 1분에 100회, 게스트는 IP당 10회를 허용하려면 다음과 같이 설정할 수 있습니다.

    RateLimiter::for('uploads', function (Request $request) {
        return $request->user()
            ? Limit::perMinute(100)->by($request->user()->id)
            : Limit::perMinute(10)->by($request->ip());
    });

<a name="multiple-rate-limits"></a>
#### 다중 속도 제한

필요하다면 하나의 제한자에서 여러 속도 제한을 배열로 반환할 수 있습니다. 지정한 순서대로 모두 적용됩니다.

    RateLimiter::for('login', function (Request $request) {
        return [
            Limit::perMinute(500),
            Limit::perMinute(3)->by($request->input('email')),
        ];
    });

동일한 `by` 값으로 여러 제한을 두면 안되므로, `by` 값 앞에 접두사를 붙여 구분하는 게 좋습니다.

    RateLimiter::for('uploads', function (Request $request) {
        return [
            Limit::perMinute(10)->by('minute:'.$request->user()->id),
            Limit::perDay(1000)->by('day:'.$request->user()->id),
        ];
    });

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 속도 제한자 연결

라우트나 라우트 그룹에 속도 제한자를 연결하려면 `throttle` [미들웨어](/docs/{{version}}/middleware)를 사용하세요. throttle 미들웨어에는 제한자 이름을 명시합니다.

    Route::middleware(['throttle:uploads'])->group(function () {
        Route::post('/audio', function () {
            // ...
        });

        Route::post('/video', function () {
            // ...
        });
    });

<a name="throttling-with-redis"></a>
#### Redis와 함께 제한 적용

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스에 매핑되어 있습니다. 애플리케이션에서 Redis를 캐시 드라이버로 쓴다면, 라라벨이 Redis로 제한 관리를 하도록 할 수 있습니다. 이를 위해 `bootstrap/app.php`에서 `throttleWithRedis` 메서드를 사용하세요.

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->throttleWithRedis();
        // ...
    })

<a name="form-method-spoofing"></a>
## Form 메서드 스푸핑

HTML 폼은 `PUT`, `PATCH`, `DELETE` 메서드를 지원하지 않습니다. 따라서 HTML 폼에서 해당 라우트로 요청할 경우, 숨겨진 `_method` 필드를 추가해야 합니다. 이 값이 HTTP 요청 메서드로 사용됩니다.

    <form action="/example" method="POST">
        <input type="hidden" name="_method" value="PUT">
        <input type="hidden" name="_token" value="{{ csrf_token() }}">
    </form>

간편하게는 `@method` [Blade 디렉티브](/docs/{{version}}/blade)를 사용할 수 있습니다.

    <form action="/example" method="POST">
        @method('PUT')
        @csrf
    </form>

<a name="accessing-the-current-route"></a>
## 현재 라우트 접근

`Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드로 현재 요청을 처리하는 라우트 정보를 확인할 수 있습니다.

    use Illuminate\Support\Facades\Route;

    $route = Route::current(); // Illuminate\Routing\Route
    $name = Route::currentRouteName(); // string
    $action = Route::currentRouteAction(); // string

라우터 및 라우트 클래스에서 사용할 수 있는 모든 메서드는 [Route 파사드의 기본 클래스](https://laravel.com/api/{{version}}/Illuminate/Routing/Router.html)와 [Route 인스턴스](https://laravel.com/api/{{version}}/Illuminate/Routing/Route.html) API 문서에서 확인할 수 있습니다.

<a name="cors"></a>
## 교차 출처 리소스 공유(CORS)

라라벨은 설정값에 맞게 CORS `OPTIONS` HTTP 요청에 자동으로 응답할 수 있습니다. `OPTIONS` 요청은 애플리케이션의 글로벌 미들웨어 스택에 기본 포함된 `HandleCors` [미들웨어](/docs/{{version}}/middleware)에 의해 자동 처리됩니다.

종종 애플리케이션의 CORS 설정값을 커스터마이징해야 할 때가 있습니다. 이 때는 `config:publish` Artisan 명령어로 `cors` 설정 파일을 배포하세요.

```shell
php artisan config:publish cors
```

이 명령어는 `config` 디렉터리에 `cors.php` 설정 파일을 생성합니다.

> [!NOTE]
> CORS 및 CORS 헤더에 대한 자세한 정보는 [MDN의 CORS 웹 문서](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱

애플리케이션을 운영 환경에 배포할 때는 라라벨의 라우트 캐시를 활용해야 합니다. 라우트 캐시를 사용하면 모든 라우트 등록 시간이 대폭 단축됩니다. 라우트 캐시를 생성하려면 아래 Artisan 명령을 실행하면 됩니다.

```shell
php artisan route:cache
```

이 명령을 실행하면, 요청마다 캐시된 라우트 파일이 로드됩니다. 새로운 라우트를 추가할 때마다 캐시를 새로 생성해야 하며, 때문에 배포 시에만 실행해야 합니다.

라우트 캐시를 삭제하려면 아래 명령을 사용하세요.

```shell
php artisan route:clear
```
