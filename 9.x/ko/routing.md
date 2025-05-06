# 라우팅(Routing)

- [기본 라우팅](#basic-routing)
    - [리디렉션 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록](#the-route-list)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [선택적 파라미터](#parameters-optional-parameters)
    - [정규식 제약 조건](#parameters-regular-expression-constraints)
- [이름 있는 라우트](#named-routes)
- [라우트 그룹](#route-groups)
    - [미들웨어](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [서브도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 프리픽스(Prefixes)](#route-group-prefixes)
    - [라우트 이름 프리픽스](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암시적 바인딩](#implicit-binding)
    - [암시적 Enum 바인딩](#implicit-enum-binding)
    - [명시적 바인딩](#explicit-binding)
- [폴백 라우트](#fallback-routes)
- [Rate Limiting(요청 제한)](#rate-limiting)
    - [요청 제한 정의하기](#defining-rate-limiters)
    - [라우트에 요청 제한 적용하기](#attaching-rate-limiters-to-routes)
- [Form Method Spoofing](#form-method-spoofing)
- [현재 라우트 정보 접근](#accessing-the-current-route)
- [CORS(교차 출처 리소스 공유)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅

가장 기본적인 라라벨 라우트는 URI와 클로저를 받아 복잡한 라우팅 설정 파일 없이도 라우트와 동작을 매우 간단하고 표현력 있게 정의할 수 있게 해줍니다:

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
#### 기본 라우트 파일

모든 라라벨 라우트는 `routes` 디렉터리 내에 위치한 라우트 파일에 정의되어 있습니다. 이 파일들은 애플리케이션의 `App\Providers\RouteServiceProvider`에 의해 자동으로 로드됩니다. `routes/web.php` 파일은 웹 인터페이스용 라우트를 정의합니다. 이 라우트들은 세션 상태 및 CSRF 보호와 같은 기능을 제공하는 `web` 미들웨어 그룹이 할당됩니다. `routes/api.php`의 라우트는 상태가 없으며 `api` 미들웨어 그룹이 할당됩니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에서 라우트 정의를 시작하게 됩니다. `routes/web.php`에 정의된 라우트는 브라우저에서 해당 URL로 접근할 수 있습니다. 예를 들어, 아래와 같은 라우트를 `http://example.com/user`로 접속하여 사용할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

`routes/api.php` 파일에 정의된 라우트는 `RouteServiceProvider`에 의해 라우트 그룹 안에 중첩되어 있습니다. 이 그룹 내에서는 `/api` URI 프리픽스가 자동으로 적용되므로, 파일의 모든 라우트에 수동으로 프리픽스를 추가할 필요가 없습니다. 프리픽스나 기타 라우트 그룹 옵션은 `RouteServiceProvider` 클래스를 수정하여 변경할 수 있습니다.

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메소드

라우터는 모든 HTTP 메소드에 대한 라우트 등록을 지원합니다:

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

여러 HTTP 메소드에 응답하는 라우트가 필요할 때는 `match` 메소드를 사용할 수 있습니다. 또는, 모든 HTTP 메소드에 응답하는 라우트를 `any` 메소드로 등록할 수 있습니다:

```php
Route::match(['get', 'post'], '/', function () {
    //
});

Route::any('/', function () {
    //
});
```

> **참고**
> 동일한 URI를 공유하는 여러 라우트를 정의할 때는 `get`, `post`, `put`, `patch`, `delete`, `options` 메소드로 정의한 라우트를 `any`, `match`, `redirect` 메소드로 정의한 라우트보다 먼저 등록해야 합니다. 이것은 요청이 올바른 라우트와 매칭되도록 보장합니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백 시그니처에 필요한 의존성을 타입힌트로 선언할 수 있습니다. 라라벨 [서비스 컨테이너](/docs/{{version}}/container)가 이 의존성을 자동으로 주입해줍니다. 예를 들어, 현재 HTTP 요청을 자동으로 주입받고 싶다면 `Illuminate\Http\Request` 클래스를 타입힌트로 사용할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에서 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 라우트로 향하는 모든 HTML 폼에는 CSRF 토큰 필드를 반드시 포함해야 합니다. 그렇지 않으면 요청이 거부됩니다. [CSRF 문서](/docs/{{version}}/csrf)를 참고하세요:

```html
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리디렉션 라우트

다른 URI로 리디렉션하는 라우트를 정의할 때는 `Route::redirect` 메소드를 사용할 수 있습니다. 이 메소드는 간단한 리디렉션 처리를 위해 전체 라우트나 컨트롤러를 따로 정의할 필요 없이 사용할 수 있는 편리한 단축키입니다:

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 선택적 세 번째 파라미터를 사용해 상태 코드를 변경할 수 있습니다:

```php
Route::redirect('/here', '/there', 301);
```

또는, `Route::permanentRedirect`로 `301` 상태 코드를 반환할 수도 있습니다:

```php
Route::permanentRedirect('/here', '/there');
```

> **경고**
> 리디렉션 라우트에서 라우트 파라미터를 사용할 때, `destination`과 `status` 파라미터는 라라벨에서 예약되어 있으니 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트

라우트가 단순히 [뷰](/docs/{{version}}/views)를 반환해야 할 때는 `Route::view` 메소드를 사용할 수 있습니다. 이 메소드는 `redirect`와 마찬가지로 전체 라우트나 컨트롤러를 정의하지 않아도 되며, 첫 번째 인수로 URI, 두 번째 인수로 뷰 이름, 그리고 세 번째 인수(선택적)로 뷰에 전달할 데이터를 배열로 넘길 수 있습니다:

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> **경고**
> 뷰 라우트에서 라우트 파라미터를 사용할 때, `view`, `data`, `status`, `headers` 파라미터는 라라벨에서 예약되어 있으므로 사용할 수 없습니다.

<a name="the-route-list"></a>
### 라우트 목록

`route:list` Artisan 명령어를 통해 애플리케이션에 정의된 모든 라우트를 쉽게 확인할 수 있습니다:

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 미들웨어는 출력에 표시되지 않지만, `-v` 옵션을 추가하면 미들웨어도 표시할 수 있습니다:

```shell
php artisan route:list -v
```

특정 URI로 시작하는 라우트만 보고 싶다면 아래처럼 사용할 수 있습니다:

```shell
php artisan route:list --path=api
```

제3자 패키지에서 정의된 라우트를 숨기고 싶을 때는 `--except-vendor` 옵션을 사용합니다:

```shell
php artisan route:list --except-vendor
```

반대로, 제3자 패키지가 정의한 라우트만 표시하려면 `--only-vendor` 옵션을 사용할 수 있습니다:

```shell
php artisan route:list --only-vendor
```

<a name="route-parameters"></a>
## 라우트 파라미터

<a name="required-parameters"></a>
### 필수 파라미터

때때로 URI의 일부 구간을 라우트 내에서 받아와야 할 수 있습니다. 예를 들어, URL에서 사용자의 ID 값을 받아와야 할 때 아래와 같이 라우트 파라미터를 정의합니다:

```php
Route::get('/user/{id}', function ($id) {
    return 'User ' . $id;
});
```

필요에 따라 여러 개의 라우트 파라미터도 정의할 수 있습니다:

```php
Route::get('/posts/{post}/comments/{comment}', function ($postId, $commentId) {
    //
});
```

라우트 파라미터는 항상 `{}` 중괄호로 감싸주며, 알파벳 또는 언더스코어(`_`)를 포함할 수 있습니다. 파라미터는 정의한 순서대로 라우트 콜백/컨트롤러에 주입되며, 변수의 이름은 큰 상관이 없습니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터 & 의존성 주입

라우트가 의존성을 필요로 하고 서비스를 주입받아야 한다면, 라우트 파라미터를 의존성 뒤에 선언하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, $id) {
    return 'User ' . $id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 파라미터

경우에 따라 URI 내 라우트 파라미터가 항상 존재하지 않을 수도 있습니다. 파라미터명 뒤에 `?`를 붙이고, 해당 변수에 기본값을 지정해 주면 됩니다:

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

`where` 메소드를 사용해 라우트 파라미터의 형식을 정규식으로 제한할 수 있습니다. 파라미터명과 해당 제약 조건을 넘기면 됩니다:

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

자주 사용하는 정규식 패턴은 아래와 같은 헬퍼 메소드로 추가할 수 있습니다:

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

Route::get('/user/{id}', function ($id) {
    //
})->whereUlid('id');

Route::get('/category/{category}', function ($category) {
    //
})->whereIn('category', ['movie', 'song', 'painting']);
```

요청이 라우트 패턴 제약 조건을 충족하지 않으면 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 글로벌 제약

특정 라우트 파라미터가 항상 동일한 정규식에 의해 제한되기를 원한다면, `RouteServiceProvider` 클래스의 `boot` 메소드에서 `pattern` 메소드를 사용하세요:

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

이렇게 패턴이 정의되면 해당 파라미터명을 사용하는 모든 라우트에 자동으로 적용됩니다:

```php
Route::get('/user/{id}', function ($id) {
    // {id}가 숫자일 때만 실행됩니다...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시(/) 허용

라라벨 라우팅 컴포넌트는 라우트 파라미터 값으로 `/`을 제외한 모든 문자를 허용합니다. 프레이스홀더에 `/`이 포함되도록 하려면 정규식을 명시적으로 추가해야 합니다:

```php
Route::get('/search/{search}', function ($search) {
    return $search;
})->where('search', '.*');
```

> **경고**
> 인코딩된 슬래시는 반드시 마지막 라우트 구간에서만 허용됩니다.

<a name="named-routes"></a>
## 이름 있는 라우트

이름 있는 라우트(named route)는 특정 라우트에 대한 URL이나 리디렉션을 편리하게 생성할 수 있도록 합니다. `name` 메소드를 체이닝하여 라우트에 이름을 지정할 수 있습니다:

```php
Route::get('/user/profile', function () {
    //
})->name('profile');
```

컨트롤러 액션에도 라우트 이름을 지정할 수 있습니다:

```php
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> **경고**
> 라우트 이름은 반드시 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 이름 있는 라우트의 URL 생성

특정 라우트에 이름을 지정했다면, 이 이름을 이용하여 `route` 및 `redirect` 헬퍼 함수로 URL이나 리디렉션을 생성할 수 있습니다:

```php
// URL 생성
$url = route('profile');

// 리디렉션 생성
return redirect()->route('profile');

return to_route('profile');
```

이름 있는 라우트가 파라미터를 요구한다면, 두 번째 인수로 파라미터 배열을 전달할 수 있습니다. 전달된 파라미터 값은 생성된 URL의 올바른 위치에 삽입됩니다:

```php
Route::get('/user/{id}/profile', function ($id) {
    //
})->name('profile');

$url = route('profile', ['id' => 1]);
```

또한, 추가적인 파라미터를 배열로 넘기면 자동으로 URL 쿼리 스트링에 추가됩니다:

```php
Route::get('/user/{id}/profile', function ($id) {
    //
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);
// /user/1/profile?photos=yes
```

> **참고**
> 요청 전체에 대해 URL 파라미터의 기본값(예: 현재 언어)을 지정하고 싶을 때는 [`URL::defaults` 메소드](/docs/{{version}}/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 검사

현재 요청이 주어진 이름의 라우트로 라우팅되었는지 확인하려면 Route 인스턴스의 `named` 메소드를 사용할 수 있습니다. 예를 들어, 미들웨어에서 현재 라우트 이름을 확인하려면 다음과 같이 할 수 있습니다:

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

라우트 그룹을 사용하면 동일한 미들웨어 등의 속성을 다수의 라우트에 반복해서 정의할 필요 없이 한 번에 공유할 수 있습니다.

중첩 그룹은 부모 그룹과 속성을 "지능적으로 병합"합니다. 미들웨어와 `where` 조건은 병합되고, 이름과 프리픽스는 덧붙여집니다. 네임스페이스 구분자나 URI 슬래시 프리픽스도 자동으로 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

라우트 그룹 내 모든 라우트에 [미들웨어](/docs/{{version}}/middleware)를 할당하려면, `middleware` 메소드를 사용해 그룹을 정의합니다. 배열 내에 있는 순서대로 미들웨어가 실행됩니다:

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first, second 미들웨어 사용
    });

    Route::get('/user/profile', function () {
        // first, second 미들웨어 사용
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러

같은 [컨트롤러](/docs/{{version}}/controllers)를 사용하는 라우트 그룹이 있다면, `controller` 메소드로 공통 컨트롤러를 지정하고 라우트 정의에서는 메소드명만 적으면 됩니다:

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹은 서브도메인 라우팅에도 사용할 수 있습니다. 서브도메인도 URI처럼 파라미터를 받아올 수 있으며, 이는 라우트 또는 컨트롤러에서 사용됩니다. 서브도메인은 `domain` 메소드를 사용해 지정합니다:

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('user/{id}', function ($account, $id) {
        //
    });
});
```

> **경고**
> 서브도메인 라우트가 접근 가능하려면, 반드시 루트 도메인 라우트보다 먼저 등록해야 합니다. 그렇지 않으면 동일한 URI 경로가 겹칠 때 루트 도메인 라우트가 서브도메인 라우트를 덮어쓸 수 있습니다.

<a name="route-group-prefixes"></a>
### 라우트 프리픽스(Prefix)

`prefix` 메소드를 이용해 그룹 내 모든 라우트의 URI 앞에 특정 프리픽스를 붙일 수 있습니다. 예를 들어, `admin`으로 프리픽스할 때는 아래와 같습니다:

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL과 매칭
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 프리픽스

`name` 메소드는 그룹의 모든 라우트 이름 앞에 특정 문자열을 붙일 때 사용합니다. 예를 들어, 모든 라우트의 이름 앞에 `admin`을 붙이고 싶다면 아래처럼 할 수 있습니다. 프리픽스에 후행 점(`.`)을 포함시키는 것이 중요합니다:

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // "admin.users"로 지정됨
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩

모델 ID를 라우트나 컨트롤러 액션에 주입할 때, 데이터베이스에서 해당 모델을 직접 쿼리하는 대신, 라라벨의 라우트 모델 바인딩 기능을 통해 모델 인스턴스를 자동으로 주입받을 수 있습니다. 예를 들어, 사용자 ID 대신 해당 ID에 일치하는 전체 `User` 모델 인스턴스를 받을 수 있습니다.

<a name="implicit-binding"></a>
### 암시적 바인딩

라우트 또는 컨트롤러 액션에서 타입힌트된 변수명이 라우트 세그먼트명과 같으면 라라벨이 `Eloquent` 모델을 자동으로 주입해 줍니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

`$user` 변수명이 `App\Models\User`이고, 변수명이 `{user}` URI 세그먼트와 일치하므로, 라라벨이 요청 URI 값과 일치하는 모델을 주입합니다. 일치하는 모델 인스턴스가 없으면 자동으로 404 HTTP 응답을 반환합니다.

암시적 바인딩은 컨트롤러 사용 시에도 가능합니다. `{user}` URI 세그먼트가 컨트롤러 메소드의 `$user` 변수와 매칭되어 아래와 같이 타입힌트된 모델이 전달됩니다:

```php
use App\Http\Controllers\UserController;
use App\Models\User;

// 라우트 정의
Route::get('/users/{user}', [UserController::class, 'show']);

// 컨트롤러 메소드
public function show(User $user)
{
    return view('user.profile', ['user' => $user]);
}
```

<a name="implicit-soft-deleted-models"></a>
#### 소프트 삭제된 모델

일반적으로 암시적 모델 바인딩은 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)된 모델을 가져오지 않습니다. 소프트 삭제된 모델도 포함하려면 라우트 정의에 `withTrashed` 메소드를 체이닝하세요:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 커스터마이징

Eloquent 모델을 `id` 칼럼 대신 다른 칼럼으로 조회하고 싶을 땐, 라우트 파라미터 정의 시 컬럼명을 지정할 수 있습니다:

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

항상 특정 컬럼으로 모델을 조회하려면 모델의 `getRouteKeyName` 메소드를 오버라이드하세요:

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
#### 사용자 지정 키 & 스코핑(Scoping)

단일 라우트에서 여러 Eloquent 모델을 암시적으로 바인딩할 때, 두 번째 모델이 첫 번째 모델의 하위(자식)임을 보장하고 싶다면 스코핑을 활용할 수 있습니다. 예를 들어, 특정 사용자의 블로그 포스트를 슬러그로 가져올 때:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

커스텀 키드 암시적 바인딩을 중첩 라우트 파라미터로 사용할 때, 라라벨은 부모 모델을 기준으로 자식 모델을 쿼리하도록 자동 스코프됩니다. 위 예시는 `User` 모델이 `posts`(복수형 파라미터명) 관계를 가지는 것으로 간주합니다.

커스텀 키 없이도 항상 자식 바인딩을 스코프하려면 `scopeBindings` 메소드를 사용하세요:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는 그룹 전체를 스코프 바인딩하도록 설정할 수도 있습니다:

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로 바인딩 스코프를 하지 않으려면 `withoutScopedBindings` 메소드를 사용하세요:

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 바인딩 실패 시 동작 커스터마이징

일반적으로 바인딩된 모델을 찾지 못하면 404 응답이 반환됩니다. `missing` 메소드를 이용해 이 동작을 커스터마이징할 수 있습니다. 이 메소드는 모델을 찾지 못했을 때 호출될 클로저를 받습니다:

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

PHP 8.1부터는 [Enums](https://www.php.net/manual/en/language.enumerations.backed.php)를 사용할 수 있습니다. 라라벨에서는 라우트 세그먼트에 [string-backed Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 타입힌트하면, 해당 값이 유효한 Enum일 때만 라우트가 실행됩니다. 아니라면 404 응답을 반환합니다. 예:

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

아래와 같이 `{category}`가 `fruits` 또는 `people`일 때만 라우트가 실행됩니다:

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩

라라벨의 암시적, 관례 기반의 모델 바인딩을 사용하지 않고도 사용할 수 있으며, 명시적으로 라우트 파라미터가 어떤 모델과 매핑될지 정의할 수 있습니다. 명시적 바인딩은 라우터의 `model` 메소드로 등록하며, `RouteServiceProvider` 클래스의 `boot` 메소드 초기에 정의해야 합니다:

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

다음은 `{user}` 파라미터를 포함하는 라우트입니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    //
});
```

이렇게 바인딩하면 `users/1` 요청이 데이터베이스의 `id`가 1인 `User` 인스턴스로 자동 주입됩니다. 일치 모델이 없으면 404 응답을 반환합니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 해석 논리(Resolve Logic) 커스터마이징

바인딩 해석을 커스터마이징하고 싶다면 `Route::bind` 메소드를 사용할 수 있습니다. 이때 전달한 클로저는 URI 세그먼트 값을 받아, 주입하고자 하는 모델 인스턴스를 반환해야 합니다. 역시 `RouteServiceProvider`의 `boot` 메소드에서 설정하는 것이 좋습니다:

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

또는, 모델의 `resolveRouteBinding` 메소드를 오버라이드할 수도 있습니다:

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

라우트가 [암시적 바인딩 스코프](#implicit-model-binding-scoping)를 사용할 때는 `resolveChildRouteBinding` 메소드가 부모 모델의 자식 바인딩 해석에 사용됩니다:

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

`Route::fallback` 메소드를 사용하면, 다른 어떤 라우트와도 일치하지 않는 요청이 들어왔을 때 실행되는 라우트를 정의할 수 있습니다. 보통 처리가 안 된 요청은 예외 핸들러를 통해 자동으로 "404" 페이지가 표시됩니다. 그러나 일반적으로 폴백 라우트는 `routes/web.php`에 등록하며, 이때는 `web` 미들웨어 그룹이 적용됩니다. 필요하다면 추가 미들웨어도 자유롭게 추가할 수 있습니다:

```php
Route::fallback(function () {
    //
});
```

> **경고**
> 폴백 라우트는 반드시 애플리케이션에서 마지막으로 등록해야 합니다.

<a name="rate-limiting"></a>
## Rate Limiting(요청 제한)

<a name="defining-rate-limiters"></a>
### 요청 제한 정의하기

라라벨은 강력하고 유연한 요청 제한 서비스를 내장하고 있어, 특정 라우트 또는 라우트 그룹의 트래픽을 제한할 수 있습니다. 설정은 보통 애플리케이션의 `App\Providers\RouteServiceProvider` 클래스 내 `configureRateLimiting` 메소드에서 합니다. 이 메소드에는 이미 `routes/api.php` 라우트에 적용되는 기본 요청 제한이 정의되어 있습니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Configure the rate limiters for the application.
 */
protected function configureRateLimiting(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
}
```

요청 제한 설정은 `RateLimiter` 퍼사드의 `for` 메소드에 정의합니다. 이 메소드는 제한 이름(name)과 제한 규칙(closure)을 받으며, 제한 규칙은 `Illuminate\Cache\RateLimiting\Limit` 클래스의 인스턴스를 반환합니다. 제한 이름은 원하는 아무 문자열이나 사용할 수 있습니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
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

요청이 지정된 제한을 초과하면, 라라벨은 자동으로 429 상태 코드를 반환합니다. 원하는 응답을 정의하려면 `response` 메소드를 사용할 수 있습니다:

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

요청 제한 콜백이 HTTP 요청 인스턴스를 받으므로, 인증된 사용자나 요청 정보에 따라 동적으로 제한 규칙을 만들 수도 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
#### 요청 제한 세분화

때로는 임의 값에 따라 제한을 세분화하고 싶을 수 있습니다. 예를 들어, IP별로 분당 100회씩 요청을 허용하려면 `by` 메소드를 사용하세요:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100)->by($request->ip());
});
```

또 다른 예로, 인증된 사용자는 분당 100회, 비회원은 IP별로 분당 10회로 제한할 수 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
                ? Limit::perMinute(100)->by($request->user()->id)
                : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 복수 요청 제한

필요하다면 하나의 요청 제한 규칙에 여러 제한 값을 배열로 반환할 수 있습니다. 배열에 정의된 순서대로 각각의 제한이 적용됩니다:

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 요청 제한 적용하기

요청 제한은 `throttle` [미들웨어](/docs/{{version}}/middleware)를 통해 라우트 또는 라우트 그룹에 적용할 수 있습니다. 미들웨어 파라미터로 요청 제한 이름을 전달하세요:

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
#### Redis 기반 요청 제한

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스에 매핑됩니다. 이 매핑은 `App\Http\Kernel`에 정의되어 있습니다. 만약 애플리케이션에서 Redis를 캐시 드라이버로 사용한다면, 이 매핑을 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 클래스로 변경하면 Redis 기반 요청 제한이 더 효율적으로 동작합니다:

```php
'throttle' => \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
```

<a name="form-method-spoofing"></a>
## Form Method Spoofing

HTML 폼은 `PUT`, `PATCH`, `DELETE` 동작을 지원하지 않습니다. 따라서 HTML 폼에서 위의 메소드로 라우트를 호출하려면, 숨겨진 `_method` 필드를 폼에 추가해야 하며, 여기에 전송하고자 하는 HTTP 메소드 값을 지정합니다:

```html
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

편의상 [`@method`](docs/{{version}}/blade) Blade 지시어를 이용해 `_method` 입력 필드를 만들 수도 있습니다:

```html
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 정보 접근

`Route` 퍼사드의 `current`, `currentRouteName`, `currentRouteAction` 메소드를 사용해 현재 요청을 처리하는 라우트 정보를 얻을 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

[Route 퍼사드의 기반 클래스](https://laravel.com/api/{{version}}/Illuminate/Routing/Router.html)와 [Route 인스턴스](https://laravel.com/api/{{version}}/Illuminate/Routing/Route.html) API 문서를 참조하시면 라우터 및 라우트 클래스에서 사용할 수 있는 모든 메소드를 확인할 수 있습니다.

<a name="cors"></a>
## 교차 출처 리소스 공유(CORS)

라라벨은 옵션(OPTIONS) HTTP 요청에 대해 자동으로 CORS 응답을 설정할 수 있습니다. 모든 CORS 설정은 애플리케이션의 `config/cors.php`에서 구성할 수 있습니다. `OPTIONS` 요청은 기본적으로 전역 미들웨어 스택에 포함된 `HandleCors` [미들웨어](/docs/{{version}}/middleware)에 의해 자동으로 처리됩니다. 전역 미들웨어 스택은 `App\Http\Kernel`에 위치합니다.

> **참고**
> CORS와 CORS 헤더에 대해 더 알고 싶으시다면 [MDN 웹 문서의 CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱

프로덕션(운영) 환경에서 애플리케이션을 배포할 때, 라라벨의 라우트 캐시를 사용하면 라우트 등록 속도를 크게 향상시킬 수 있습니다. 라우트 캐시 생성은 아래 Artisan 명령어로 수행합니다:

```shell
php artisan route:cache
```

이 명령 실행 후에는 모든 요청마다 캐시된 라우트 파일이 로드됩니다. 새로운 라우트를 추가하는 경우에는 반드시 캐시를 새로 생성해야 합니다. 따라서 프로젝트 배포 중에만 `route:cache` 명령을 사용하는 것이 좋습니다.

라우트 캐시를 지우려면 다음 명령을 사용합니다:

```shell
php artisan route:clear
```
