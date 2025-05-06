# 라우팅

- [기본 라우팅](#basic-routing)
    - [리디렉션 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [선택적 파라미터](#parameters-optional-parameters)
    - [정규식 제약 조건](#parameters-regular-expression-constraints)
- [네임드 라우트](#named-routes)
- [라우트 그룹](#route-groups)
    - [미들웨어](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [서브도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 접두사](#route-group-prefixes)
    - [라우트 이름 접두사](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암시적 바인딩](#implicit-binding)
    - [명시적 바인딩](#explicit-binding)
- [폴백 라우트](#fallback-routes)
- [요청 제한(Rate Limiting)](#rate-limiting)
    - [요청 제한기 정의](#defining-rate-limiters)
    - [라우트에 요청 제한기 적용](#attaching-rate-limiters-to-routes)
- [폼 메소드 속임수(Method Spoofing)](#form-method-spoofing)
- [현재 라우트에 접근하기](#accessing-the-current-route)
- [교차 출처 리소스 공유(CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅

Laravel의 가장 기본적인 라우트는 URI와 클로저를 받아 복잡한 라우팅 설정 파일 없이도 아주 간단하고 명확하게 라우트와 동작을 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
#### 기본 라우트 파일

모든 Laravel 라우트는 `routes` 디렉토리에 위치한 라우트 파일에 정의됩니다. 이 파일들은 애플리케이션의 `App\Providers\RouteServiceProvider`에 의해 자동으로 로드됩니다. `routes/web.php` 파일은 웹 인터페이스를 위한 라우트를 정의하며, `web` 미들웨어 그룹이 적용되어 세션 상태 및 CSRF 보호와 같은 기능을 제공합니다. `routes/api.php`의 라우트는 상태가 없으며 `api` 미들웨어 그룹이 할당됩니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에 라우트를 정의하는 것부터 시작합니다. 이 파일에 정의된 라우트는 브라우저에서 해당 URL을 입력하여 접근할 수 있습니다. 예를 들어 다음 라우트는 브라우저에서 `http://example.com/user`로 접근할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

`routes/api.php` 파일에 정의된 라우트는 `RouteServiceProvider`에 의해 라우트 그룹 내에 포함됩니다. 이 그룹 내에서는 `/api` URI 접두사가 자동으로 적용되므로, 모든 라우트에 수동으로 적용할 필요가 없습니다. 접두사나 기타 그룹 옵션은 `RouteServiceProvider` 클래스에서 수정 가능합니다.

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메소드

라우터는 모든 HTTP 메소드(HTTP Verb)에 대응하는 라우트를 등록할 수 있습니다:

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

여러 HTTP 메소드에 대응하는 라우트를 등록해야 할 때는 `match` 메소드를 사용할 수 있습니다. 또는, 모든 HTTP 메소드에 대응하는 라우트는 `any` 메소드를 사용할 수 있습니다:

```php
Route::match(['get', 'post'], '/', function () {
    //
});

Route::any('/', function () {
    //
});
```

> {tip} 동일한 URI로 여러 라우트를 정의할 때, `get`, `post`, `put`, `patch`, `delete`, `options` 메소드를 사용하는 라우트는 반드시 `any`, `match`, `redirect` 메소드를 사용하는 라우트보다 먼저 정의해야 합니다. 이는 요청이 올바른 라우트에 매칭되도록 보장합니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백 시그니처에서 필요한 의존성을 타입힌트 하면, Laravel [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 이를 주입합니다. 예를 들어, 현재 HTTP 요청을 자동으로 라우트 콜백에 주입하고 싶다면 `Illuminate\Http\Request` 클래스를 타입힌트 할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 라우트로 향하는 모든 HTML 폼에는 반드시 CSRF 토큰 필드가 포함되어야 합니다. 그렇지 않으면 요청이 거부됩니다. CSRF 보호에 대한 더 자세한 정보는 [CSRF 문서](/docs/{{version}}/csrf)를 참고하세요:

```html
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리디렉션 라우트

다른 URI로 리디렉션하는 라우트를 정의할 때는 `Route::redirect` 메소드를 사용할 수 있습니다. 이 메소드는 간단한 리디렉션을 위한 편리한 단축키입니다:

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 선택적 세 번째 파라미터로 상태 코드를 설정할 수 있습니다:

```php
Route::redirect('/here', '/there', 301);
```

또는, 항상 `301` 상태 코드를 반환하려면 `Route::permanentRedirect` 메소드를 사용할 수 있습니다:

```php
Route::permanentRedirect('/here', '/there');
```

> {note} 리디렉션 라우트에서 사용되는 라우트 파라미터 중 `destination`과 `status`는 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트

라우트가 단순히 [뷰](/docs/{{version}}/views)를 반환해야 할 경우, `Route::view` 메소드를 사용할 수 있습니다. 이 메소드는 전체 라우트 또는 컨트롤러를 정의하지 않아도 되는 간단한 단축 방법입니다. 첫 번째 인수로는 URI, 두 번째 인수로는 뷰 이름, 세 번째 인수로는 뷰에 전달할 데이터를 배열로 제공할 수 있습니다:

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> {note} 뷰 라우트에서 사용되는 라우트 파라미터 중 `view`, `data`, `status`, `headers`는 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="route-parameters"></a>
## 라우트 파라미터

<a name="required-parameters"></a>
### 필수 파라미터

경우에 따라 URI의 일부를 라우트 내에서 캡처해야 할 필요가 있습니다. 예를 들어, URL에서 사용자의 ID를 받아야 하는 경우, 라우트 파라미터를 정의할 수 있습니다:

```php
Route::get('/user/{id}', function ($id) {
    return 'User ' . $id;
});
```

필요에 따라 여러 개의 라우트 파라미터를 정의할 수 있습니다:

```php
Route::get('/posts/{post}/comments/{comment}', function ($postId, $commentId) {
    //
});
```

라우트 파라미터는 항상 `{}` 중괄호로 감싸며, 영문자 또는 언더스코어(`_`)를 사용할 수 있습니다. 라우트 파라미터는 정의된 순서대로 라우트 콜백/컨트롤러에 전달됩니다. 인수 이름은 중요하지 않습니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터 & 의존성 주입

라우트가 의존성이 필요한 경우, 라우트 파라미터는 모든 의존성 인수 뒤에 나열해야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, $id) {
    return 'User ' . $id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 파라미터

때로는 URI에 항상 존재하지 않을 수도 있는 라우트 파라미터를 지정해야 할 수도 있습니다. 이 경우에는 파라미터 이름 뒤에 `?`를 붙여서 지정하고, 해당 변수에 기본값을 부여해야 합니다:

```php
Route::get('/user/{name?}', function ($name = null) {
    return $name;
});

Route::get('/user/{name?}', function ($name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규식 제약 조건

라우트 인스턴스의 `where` 메소드를 활용해 라우트 파라미터의 형식을 제한할 수 있습니다. `where` 메소드는 파라미터 이름과 이를 제한하는 정규식을 입력 받습니다:

```php
Route::get('/user/{name}', function ($name) {
    //
})->where('name', '[A-Za-z]+');

Route::get('/user/{id}', function ($id) {
    //
})->where('id', '[0-9]+');

Route::get('/user/{id}/{name}', function ($id, $name) {
    //
})->where(['id' => '[0-9]+', 'name' => '[a-z]+']);
```

자주 사용되는 일부 정규식 패턴은 헬퍼 메소드를 통해 빠르게 적용할 수 있습니다:

```php
Route::get('/user/{id}/{name}', function ($id, $name) {
    //
})->whereNumber('id')->whereAlpha('name');

Route::get('/user/{name}', function ($name) {
    //
})->whereAlphaNumeric('name');

Route::get('/user/{id}', function ($id) {
    //
})->whereUuid('id');
```

요청이 라우트 패턴 제약을 만족하지 않으면, 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 글로벌 제약 조건

특정 라우트 파라미터에 항상 같은 정규식을 적용하고 싶다면, `App\Providers\RouteServiceProvider`의 `boot` 메소드에서 `pattern` 메소드를 사용해 제약 조건을 지정할 수 있습니다:

```php
/**
 * Define your route model bindings, pattern filters, etc.
 *
 * @return void
 */
public function boot()
{
    Route::pattern('id', '[0-9]+');
}
```

이렇게 패턴을 지정하면, 해당 파라미터 이름을 사용하는 모든 라우트에 자동으로 적용됩니다:

```php
Route::get('/user/{id}', function ($id) {
    // {id}가 숫자인 경우에만 실행됩니다...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시

Laravel 라우팅 컴포넌트는 `/`를 제외한 모든 문자를 라우트 파라미터 값에 허용합니다. `/`를 포함해야 한다면, `where` 조건의 정규식을 통해 이를 명시적으로 허용해야 합니다:

```php
Route::get('/search/{search}', function ($search) {
    return $search;
})->where('search', '.*');
```

> {note} 인코딩된 슬래시는 항상 마지막 라우트 구간에서만 지원됩니다.

<a name="named-routes"></a>
## 네임드 라우트

네임드 라우트는 특정 라우트에 대해 URL 생성이나 리다이렉션을 간편하게 도와줍니다. 라우트 정의에 `name` 메소드를 체이닝하여 라우트 이름을 지정할 수 있습니다:

```php
Route::get('/user/profile', function () {
    //
})->name('profile');
```

컨트롤러 액션에서도 라우트 이름을 지정할 수 있습니다:

```php
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> {note} 라우트 이름은 항상 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 네임드 라우트로 URL 생성

특정 라우트에 이름을 지정한 후에는 Laravel의 `route` 및 `redirect` 헬퍼로 URL이나 리다이렉션을 손쉽게 생성할 수 있습니다:

```php
// URL 생성...
$url = route('profile');

// 리다이렉션 생성...
return redirect()->route('profile');
```

네임드 라우트가 파라미터를 요구한다면 `route` 함수의 두 번째 인수로 전달할 수 있습니다. 파라미터는 해당 위치에 자동으로 삽입됩니다:

```php
Route::get('/user/{id}/profile', function ($id) {
    //
})->name('profile');

$url = route('profile', ['id' => 1]);
```

추가 파라미터를 배열로 넘기면 쿼리 스트링으로 자동 추가됩니다:

```php
Route::get('/user/{id}/profile', function ($id) {
    //
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// /user/1/profile?photos=yes
```

> {tip} 요청 전역적으로 URL 파라미터(예: 현재 언어/로케일)에 대한 기본값을 지정하려면 [`URL::defaults` 메소드](/docs/{{version}}/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 검사

현재 요청이 특정 네임드 라우트에 매칭됐는지 확인하려면 Route 인스턴스의 `named` 메소드를 사용할 수 있습니다. 예를 들어, 라우트 미들웨어 안에서 현재 라우트 이름을 확인할 수 있습니다:

```php
/**
 * Handle an incoming request.
 *
 * @param  \Illuminate\Http\Request  $request
 * @param  \Closure  $next
 * @return mixed
 */
public function handle($request, Closure $next)
{
    if ($request->route()->named('profile')) {
        //
    }

    return $next($request);
}
```

<a name="route-groups"></a>
## 라우트 그룹

라우트 그룹을 사용하면 미들웨어 등 특정 라우트 속성을 여러 라우트에 반복해서 정의하지 않고도 쉽게 공유할 수 있습니다.

중첩된 그룹은 상위 그룹과 "스마트하게" 속성을 병합합니다. 미들웨어와 `where` 조건은 병합되고, 이름과 접두사는 덧붙여집니다. 네임스페이스 및 URI 접두사의 슬래시는 자동으로 처리됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

[미들웨어](/docs/{{version}}/middleware)를 그룹 내 모든 라우트에 적용하려면, 그룹 정의 전에 `middleware` 메소드를 사용하세요. 미들웨어는 배열에 나열된 순서대로 실행됩니다:

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

한 그룹의 라우트가 동일한 [컨트롤러](/docs/{{version}}/controllers)를 사용할 경우, `controller` 메소드를 통해 공통 컨트롤러를 지정할 수 있습니다. 각 라우트 정의에서는 호출할 메소드만 나열하면 됩니다:

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹은 서브도메인 라우팅에도 사용할 수 있습니다. 서브도메인 역시 라우트 URI처럼 파라미터로 지정할 수 있어, 서브도메인의 일부를 라우트/컨트롤러에서 사용할 수 있습니다. `domain` 메소드를 사용해 서브도메인을 지정하세요:

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('user/{id}', function ($account, $id) {
        //
    });
});
```

> {note} 서브도메인 라우트가 올바르게 동작하도록, 반드시 루트 도메인 라우트보다 먼저 등록해야 합니다. 동일한 URI 경로를 가진 루트 도메인 라우트가 덮어쓰는 것을 방지합니다.

<a name="route-group-prefixes"></a>
### 라우트 접두사

`prefix` 메소드를 이용해 그룹 내 모든 라우트의 URI에 접두사를 붙일 수 있습니다. 예를 들어, 그룹 내 모든 라우트 URI에 `admin` 접두사를 붙일 수 있습니다:

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL과 매칭됨
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두사

`name` 메소드를 사용해 그룹 내 모든 라우트의 이름에 원하는 접두어를 붙일 수 있습니다. 예를 들어, 모든 라우트의 이름에 `admin.`을 붙이고자 한다면:

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // 라우트 이름: "admin.users"
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩

모델 ID를 라우트나 컨트롤러 액션에 주입할 때, 보통 데이터베이스에서 해당 모델을 조회해야 합니다. Laravel 라우트 모델 바인딩을 사용하면, 모델 인스턴스를 라우트에 바로 주입할 수 있습니다. 예를 들어, 사용자의 ID 대신 해당 ID에 매칭되는 전체 `User` 모델 인스턴스를 주입할 수 있습니다.

<a name="implicit-binding"></a>
### 암시적 바인딩

라우트 또는 컨트롤러 액션 내에서 변수 타입힌트와 라우트 세그먼트 이름이 일치하면, Laravel은 Eloquent 모델 인스턴스를 자동으로 주입합니다. 예시:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

`$user` 변수의 타입힌트가 `App\Models\User`이고, 변수명이 `{user}` 세그먼트명과 일치하므로, URI 파라미터 값과 일치하는 모델 인스턴스가 자동 주입됩니다. 데이터베이스에서 일치하는 모델이 없으면 404 응답이 반환됩니다.

암시적 바인딩은 컨트롤러 메소드에도 사용할 수 있습니다. 역시 `{user}` URI 세그먼트와 컨트롤러의 `$user` 변수명이 일치해야 합니다:

```php
use App\Http\Controllers\UserController;
use App\Models\User;

// 라우트 정의...
Route::get('/users/{user}', [UserController::class, 'show']);

// 컨트롤러 메소드 정의...
public function show(User $user)
{
    return view('user.profile', ['user' => $user]);
}
```

<a name="implicit-soft-deleted-models"></a>
#### 소프트 삭제된 모델

기본적으로 암시적 모델 바인딩은 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 그러나, 라우트 정의에 `withTrashed` 메소드를 체이닝 하면 소프트 삭제된 모델도 조회할 수 있습니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 키 커스터마이징

이따금 `id`가 아닌 다른 컬럼을 라우트 모델 바인딩에 사용하고 싶을 수 있습니다. 이 경우, 라우트 파라미터 정의에서 컬럼명을 명시할 수 있습니다:

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

특정 모델에서 항상 `id`가 아닌 다른 컬럼을 바인딩에 사용하려면 Eloquent 모델의 `getRouteKeyName` 메소드를 오버라이드하면 됩니다:

```php
/**
 * Get the route key for the model.
 *
 * @return string
 */
public function getRouteKeyName()
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
#### 커스텀 키 & 스코핑

하나의 라우트 정의에서 여러 개의 Eloquent 모델을 암시적으로 바인딩할 때, 두 번째 모델이 첫 번째 모델의 하위 자원이어야 할 수도 있습니다. 아래 예시는 특정 사용자의 블로그 게시물을 슬러그로 조회하는 경우입니다:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

이처럼 중첩 라우트 파라미터에서 커스텀 키를 사용하면, Laravel은 첫 번째 모델의 관계명을 이용해 하위 모델을 자동으로 스코핑합니다. 위 예시에선 `User` 모델이 `posts` 관계를 가지고 있다고 간주합니다.

커스텀 키가 없더라도 자식 바인딩에 스코프를 적용하고 싶다면 라우트 정의 시 `scopeBindings` 메소드를 사용할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

라우트 정의 그룹 전체에 스코프 바인딩을 적용할 수도 있습니다:

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

<a name="customizing-missing-model-behavior"></a>
#### 모델 미발견 시 동작 커스터마이징

일반적으로 암시적 바인딩에서 모델 인스턴스를 찾지 못하면 404 응답이 반환됩니다. 하지만, 라우트 정의에 `missing` 메소드를 통해 이 동작을 커스터마이징할 수 있습니다:

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

<a name="explicit-binding"></a>
### 명시적 바인딩

Laravel의 암시적 바인딩 대신 명확하게 모델 바인딩 방식을 정의할 수도 있습니다. 명시적 바인딩 등록은 라우터의 `model` 메소드를 사용하여 파라미터와 모델 클래스를 연결합니다. 이 코드는 `RouteServiceProvider`의 `boot` 메소드 초기에 정의하면 됩니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Define your route model bindings, pattern filters, etc.
 *
 * @return void
 */
public function boot()
{
    Route::model('user', User::class);

    // ...
}
```

이제 `{user}` 파라미터가 포함된 라우트를 정의하세요:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    //
});
```

모든 `{user}` 파라미터는 `App\Models\User` 모델에 바인딩되며, 예를 들어 `users/1` 요청에는 ID 1에 해당하는 `User` 인스턴스가 주입됩니다. 해당 모델 인스턴스가 없으면 자동으로 404 응답이 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 로직 커스터마이징

모델 바인딩 시 동작을 직접 정의하고 싶다면, `Route::bind` 메소드를 사용할 수 있습니다. 이때 전달하는 클로저는 URI 세그먼트 값을 받고, 해당 값에 대한 모델 인스턴스를 반환해야 합니다. 역시 애플리케이션의 `RouteServiceProvider` `boot` 메소드에서 정의합니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Define your route model bindings, pattern filters, etc.
 *
 * @return void
 */
public function boot()
{
    Route::bind('user', function ($value) {
        return User::where('name', $value)->firstOrFail();
    });

    // ...
}
```

또는, Eloquent 모델에서 `resolveRouteBinding` 메소드를 오버라이드할 수도 있습니다. 이 메소드는 URI 세그먼트 값을 받아 해당 인스턴스를 반환해야 합니다:

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

[암시적 바인딩 스코프](#implicit-model-binding-scoping)를 사용하는 경우에는 `resolveChildRouteBinding` 메소드가 자식 바인딩 해석에 활용됩니다:

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
## 폴백 라우트

`Route::fallback` 메소드를 사용하면, 다른 어떤 라우트와도 일치하지 않을 때 실행되는 라우트를 정의할 수 있습니다. 일반적으로 처리되지 않은 요청은 애플리케이션의 예외 핸들러를 통해 "404" 페이지가 렌더링됩니다. 하지만, 보통 `routes/web.php` 파일 내에서 `fallback` 라우트를 정의하게 되므로 `web` 미들웨어 그룹의 모든 미들웨어가 이 라우트에도 적용됩니다. 필요하다면 별도의 미들웨어를 추가할 수 있습니다:

```php
Route::fallback(function () {
    //
});
```

> {note} 폴백 라우트는 애플리케이션에서 항상 마지막에 등록되어야 합니다.

<a name="rate-limiting"></a>
## 요청 제한(Rate Limiting)

<a name="defining-rate-limiters"></a>
### 요청 제한기 정의

Laravel은 특정 라우트 또는 라우트 그룹에 대한 트래픽 양을 제한하는 강력하고 커스터마이즈 가능한 요청 제한 서비스를 제공합니다. 먼저, 애플리케이션 요구에 맞게 요청 제한기 설정을 정의해야 합니다. 보통 이 설정은 `App\Providers\RouteServiceProvider`의 `configureRateLimiting` 메소드 내에서 정의합니다.

요청 제한기는 `RateLimiter` 파사드의 `for` 메소드로 정의합니다. 이 메소드는 제한기 이름과, 라우트에 적용할 제한 설정을 반환하는 클로저를 받습니다. 제한 설정은 `Illuminate\Cache\RateLimiting\Limit` 클래스의 인스턴스여야 하며, 빌더 메소드로 빠르게 설정을 정의할 수 있습니다. 제한기 이름에는 임의의 문자열을 사용할 수 있습니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Configure the rate limiters for the application.
 *
 * @return void
 */
protected function configureRateLimiting()
{
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });
}
```

요청 제한을 초과하면, Laravel은 자동으로 429 HTTP 상태 코드로 응답합니다. 제한 초과 시 사용자 응답을 직접 정의하려면 `response` 메소드를 사용하세요:

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function () {
        return response('Custom response...', 429);
    });
});
```

제한기 클로저는 HTTP 요청 인스턴스를 받기 때문에, 요청 정보나 인증 사용자에 따라 제한을 동적으로 설정할 수 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
#### 제한 구분하기

경우에 따라 임의의 값별로 제한을 구분하고 싶을 수 있습니다. 예를 들어, IP 주소별로 분당 100회 접근을 허용하려면, 제한 생성 시 `by` 메소드를 사용할 수 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100)->by($request->ip());
});
```

또 다른 예시로, 인증된 사용자별로 분당 100회, 비회원(게스트)에 대해선 IP별로 분당 10회 제한을 둘 수도 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
                ? Limit::perMinute(100)->by($request->user()->id)
                : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 다중 요청 제한기

필요하다면, 하나의 제한기 설정에서 제한을 배열로 반환할 수도 있습니다. 배열 내 구성된 순서대로 각 제한이 평가됩니다:

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 요청 제한기 적용

요청 제한기는 `throttle` [미들웨어](/docs/{{version}}/middleware)를 사용해서 라우트나 라우트 그룹에 적용할 수 있습니다. throttle 미들웨어에는 적용할 제한기 이름을 전달합니다:

```php
Route::middleware(['throttle:uploads'])->group(function () {
    Route::post('/audio', function () {
        //
    });

    Route::post('/video', function () {
        //
    });
});
```

<a name="throttling-with-redis"></a>
#### Redis와 요청 제한

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스에 매핑되어 있습니다. 이 매핑은 애플리케이션 HTTP 커널(`App\Http\Kernel`)에서 정의됩니다. Redis를 캐시 드라이버로 사용하는 경우, 더 효율적인 제한 관리를 위해 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 클래스를 사용할 수 있습니다:

```php
'throttle' => \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
```

<a name="form-method-spoofing"></a>
## 폼 메소드 속임수(Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 메소드를 공식적으로 지원하지 않습니다. 따라서, HTML 폼에서 이러한 라우트를 호출할 때는 숨겨진 `_method` 필드를 추가해야 하며, 이 필드의 값이 HTTP 요청 메소드로 사용됩니다:

```html
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

편의를 위해, `@method` [Blade 디렉티브](/docs/{{version}}/blade)를 사용해 `_method` 필드를 생성할 수도 있습니다:

```html
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트에 접근하기

`Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메소드를 사용해서 요청을 처리하는 라우트 정보를 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

라우터 및 라우트 클래스에서 사용할 수 있는 모든 메소드는 [Route 파사드의 기본 클래스 API 문서](https://laravel.com/api/{{version}}/Illuminate/Routing/Router.html) 및 [Route 인스턴스 API 문서](https://laravel.com/api/{{version}}/Illuminate/Routing/Route.html)를 참고하세요.

<a name="cors"></a>
## 교차 출처 리소스 공유(CORS)

Laravel은 자동으로 CORS `OPTIONS` HTTP 요청에, 지정한 값으로 응답할 수 있습니다. 모든 CORS 설정은 애플리케이션의 `config/cors.php` 설정 파일에서 조정합니다. `OPTIONS` 요청은 전역 미들웨어 스택(애플리케이션의 HTTP 커널인 `App\Http\Kernel`에 정의됨)에 기본 포함된 `HandleCors` [미들웨어](/docs/{{version}}/middleware)가 처리합니다.

> {tip} CORS와 CORS 헤더에 대한 상세한 정보는 [MDN 웹 문서의 CORS 가이드](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하시기 바랍니다.

<a name="route-caching"></a>
## 라우트 캐싱

프로덕션 환경에 애플리케이션을 배포할 때는, Laravel의 라우트 캐시를 활용하세요. 라우트 캐시는 라우트 등록에 걸리는 시간을 크게 줄여줍니다. 라우트 캐시를 생성하려면 `route:cache` Artisan 명령을 실행하세요:

```bash
php artisan route:cache
```

이 명령 실행 후, 요청마다 캐시된 라우트 파일이 자동으로 로드됩니다. 신규 라우트를 추가했다면, 반드시 라우트 캐시를 새로 생성해야 합니다. 따라서, 라우트 캐시는 프로젝트 배포 시에만 실행하는 것이 좋습니다.

캐시를 비우려면 `route:clear` 명령을 사용하세요:

```bash
php artisan route:clear
```