# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [리다이렉트 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록](#the-route-list)
- [라우트 매개변수](#route-parameters)
    - [필수 매개변수](#required-parameters)
    - [선택적 매개변수](#parameters-optional-parameters)
    - [정규표현식 제약조건](#parameters-regular-expression-constraints)
- [이름이 지정된 라우트](#named-routes)
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
- [속도 제한 (Rate Limiting)](#rate-limiting)
    - [속도 제한기 정의](#defining-rate-limiters)
    - [라우트에 속도 제한기 연결](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근하기](#accessing-the-current-route)
- [교차 출처 리소스 공유 (CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

가장 기본적인 Laravel 라우트는 URI와 클로저를 받아 간단하고 표현력 있는 방식으로 복잡한 라우팅 설정 파일 없이 라우트와 동작을 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
#### 기본 라우트 파일

모든 Laravel 라우트는 `routes` 디렉토리에 위치한 라우트 파일에 정의됩니다. 이 파일들은 애플리케이션의 `App\Providers\RouteServiceProvider`에 의해 자동으로 로드됩니다. `routes/web.php` 파일은 웹 인터페이스용 라우트를 정의하며, 해당 라우트들은 세션 상태와 CSRF 보호같은 기능을 제공하는 `web` 미들웨어 그룹이 할당됩니다. 반면 `routes/api.php` 내 라우트들은 상태가 없으며 `api` 미들웨어 그룹이 할당됩니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에서 라우트 정의를 시작합니다. `routes/web.php`에 정의된 라우트는 브라우저에서 해당 URL로 접속하여 접근할 수 있습니다. 예를 들어 다음 라우트는 `http://example.com/user` 주소로 접근할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

`routes/api.php` 파일에 정의된 라우트는 `RouteServiceProvider`가 라우트 그룹으로 감싸며, `/api` URI 접두사를 자동으로 적용하므로 수동으로 각 라우트에 접두사를 붙일 필요가 없습니다. 접두사 및 다른 라우트 그룹 옵션은 `RouteServiceProvider` 클래스를 수정하여 변경할 수 있습니다.

<a name="available-router-methods"></a>
#### 가능한 라우터 메서드

라우터는 모든 HTTP 메서드에 응답하는 라우트를 등록할 수 있습니다:

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

때로는 여러 HTTP 메서드에 모두 응답하는 라우트를 등록해야 할 수도 있습니다. 이 경우 `match` 메서드를 사용할 수 있고, 모든 HTTP 메서드에 응답하도록 하려면 `any` 메서드를 사용할 수 있습니다:

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]  
> 동일 URI에 대해 여러 라우트를 정의할 때, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드로 정의한 라우트를 `any`, `match`, `redirect` 메서드로 정의한 라우트보다 먼저 정의해야 합니다. 이는 들어오는 요청을 올바른 라우트와 매칭하기 위함입니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백 함수 시그니처에 필요한 의존성을 타입힌트로 지정할 수 있으며, Laravel의 서비스 컨테이너가 이를 자동으로 해결해 주입합니다. 예를 들어 `Illuminate\Http\Request` 클래스를 타입힌트하면 현재 HTTP 요청이 자동으로 주입됩니다:

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 메서드를 사용하는 HTML 폼에는 반드시 CSRF 토큰 필드가 포함되어야 합니다. 없으면 요청은 거부됩니다. CSRF 보호에 대한 자세한 내용은 [CSRF 문서](/docs/10.x/csrf)를 참고하세요:

```html
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리다이렉트 라우트 (Redirect Routes)

다른 URI로 리다이렉트하는 라우트를 정의할 때는 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 간단한 리다이렉트를 위해 완전한 라우트나 컨트롤러를 정의하지 않아도 되는 편리한 단축키입니다:

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 세 번째 인자를 통해 상태 코드를 변경할 수 있습니다:

```php
Route::redirect('/here', '/there', 301);
```

또는 `Route::permanentRedirect` 메서드를 사용하여 `301` 상태 코드를 반환할 수도 있습니다:

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]  
> 리다이렉트 라우트에서 라우트 매개변수를 사용할 때 `destination`과 `status`는 Laravel에서 예약된 매개변수명이므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트 (View Routes)

라우트가 단순히 [뷰](/docs/10.x/views)를 반환하기만 하면 `Route::view` 메서드를 사용할 수 있습니다. `redirect` 메서드와 마찬가지로, 완전한 라우트나 컨트롤러를 정의하지 않고 간단히 처리할 수 있습니다. `view` 메서드는 첫 번째 인자로 URI, 두 번째 인자로 뷰 이름을 받으며, 세 번째 인자로는 뷰에 전달할 데이터를 배열로 지정할 수 있습니다:

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]  
> 뷰 라우트에서 라우트 매개변수를 사용할 때 `view`, `data`, `status`, `headers`는 Laravel에서 예약된 매개변수명이므로 사용할 수 없습니다.

<a name="the-route-list"></a>
### 라우트 목록 (The Route List)

`route:list` Artisan 명령어로 애플리케이션에서 정의된 모든 라우트를 한눈에 확인할 수 있습니다:

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 미들웨어는 `route:list` 결과에 표시되지 않지만, `-v` 옵션을 추가하면 미들웨어와 미들웨어 그룹 이름을 볼 수 있습니다:

```shell
php artisan route:list -v

# 미들웨어 그룹 확장...
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 보려면 `--path` 옵션을 사용할 수 있습니다:

```shell
php artisan route:list --path=api
```

서드파티 패키지가 정의한 라우트를 숨기려면, `--except-vendor` 옵션을 사용하세요:

```shell
php artisan route:list --except-vendor
```

반대로, 서드파티 패키지 라우트만 보고 싶다면 `--only-vendor` 옵션을 사용하면 됩니다:

```shell
php artisan route:list --only-vendor
```

<a name="route-parameters"></a>
## 라우트 매개변수 (Route Parameters)

<a name="required-parameters"></a>
### 필수 매개변수 (Required Parameters)

URI의 일부를 캡쳐해야 할 때, 예를 들어 URL에서 사용자의 ID를 받아야 할 경우 라우트 매개변수를 정의할 수 있습니다:

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요한 만큼 여러 매개변수를 정의할 수도 있습니다:

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

매개변수는 항상 `{}` 중괄호로 감싸고, 알파벳 문자와 언더스코어(`_`)를 포함할 수 있습니다. 라우트 콜백이나 컨트롤러에 라우트 매개변수는 순서대로 주입되며 변수명은 중요하지 않습니다.

<a name="parameters-and-dependency-injection"></a>
#### 매개변수와 의존성 주입

라우트 콜백에 라우트 매개변수 외에 요청 객체 등 의존성을 주입하려면, 의존성 타입힌트를 먼저 작성하고 그 뒤에 라우트 매개변수를 나열해야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 매개변수 (Optional Parameters)

URI에 항상 매개변수가 포함되지 않을 경우 선택적 매개변수로 설정할 수 있습니다. 매개변수명 뒤에 `?`를 붙이고, 대응 변수에 기본값을 할당해야 합니다:

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규표현식 제약조건 (Regular Expression Constraints)

`where` 메서드로 라우트 매개변수의 형식을 제한할 수 있습니다. 첫 번째 인자로 매개변수명, 두 번째 인자로 정규표현식을 받습니다:

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

몇몇 자주 쓰이는 정규식 패턴은 헬퍼 메서드로 빠르게 추가 가능합니다:

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
    //
})->whereUlid('id');

Route::get('/category/{category}', function (string $category) {
    // ...
})->whereIn('category', ['movie', 'song', 'painting']);
```

요청이 제약조건과 일치하지 않으면 404 응답이 자동으로 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약조건

특정 이름의 라우트 매개변수에 항상 같은 정규패턴 제약조건을 적용하려면, `App\Providers\RouteServiceProvider` 클래스의 `boot` 메서드에서 `pattern` 메서드를 사용하세요:

```php
/**
 * 라우트 모델 바인딩, 패턴 필터 등을 정의합니다.
 */
public function boot(): void
{
    Route::pattern('id', '[0-9]+');
}
```

이후 같은 이름의 매개변수 모든 라우트에 자동으로 패턴이 적용됩니다:

```php
Route::get('/user/{id}', function (string $id) {
    // {id}가 숫자인 경우에만 실행됩니다...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시 허용

Laravel 라우팅 컴포넌트는 기본적으로 `/` 문자를 제외한 모든 문자를 라우트 매개변수에 허용합니다. 매개변수 내에 `/` 문자를 포함시키고 싶다면, 정규식 조건으로 명시적으로 허용해야 합니다:

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]  
> 인코딩된 슬래시는 라우트의 마지막 세그먼트에서만 지원됩니다.

<a name="named-routes"></a>
## 이름이 지정된 라우트 (Named Routes)

이름이 지정된 라우트는 특정 라우트에 대해 URL 생성이나 리다이렉트를 편리하게 할 수 있도록 합니다. 라우트에 이름을 지정하려면 `name` 메서드를 체인하면 됩니다:

```php
Route::get('/user/profile', function () {
    // ...
})->name('profile');
```

컨트롤러 액션에 대해서도 이름이 지정된 라우트를 설정할 수 있습니다:

```php
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!WARNING]  
> 라우트 이름은 항상 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 이름이 지정된 라우트로 URL 생성하기

라우트에 이름을 지정한 후에는 Laravel의 `route` 및 `redirect` 헬퍼를 활용하여 URL이나 리다이렉트를 생성할 수 있습니다:

```php
// URL 생성...
$url = route('profile');

// 리다이렉트 생성...
return redirect()->route('profile');

return to_route('profile');
```

라우트 매개변수가 있는 경우 두 번째 인자로 매개변수를 넘기면 URL의 적절한 위치에 자동으로 삽입됩니다:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

추가 매개변수를 배열에 포함하면 자동으로 URL 쿼리스트링으로 추가됩니다:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// 결과: /user/1/profile?photos=yes
```

> [!NOTE]  
> 요청 전체에 대해 URL 매개변수 기본값을 지정하고 싶을 때는 [`URL::defaults` 메서드](/docs/10.x/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 정보 확인하기

현재 요청이 특정 이름의 라우트에 매칭되었는지 확인하려면, 라우트 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어, 라우트 미들웨어 내에서 현재 라우트 이름을 확인할 수 있습니다:

```php
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * 들어오는 요청 처리 핸들러
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

라우트 그룹을 사용하면, 미들웨어 같은 라우트 속성을 여러 라우트에 일일이 지정하지 않고 그룹 단위로 공유할 수 있습니다.

중첩된 그룹은 부모 그룹의 속성과 "스마트"하게 병합됩니다. 미들웨어와 `where` 조건은 병합되고, 이름과 접두사는 이어서 붙여집니다. 네임스페이스 구분자와 URI 접두사의 슬래시는 적절히 자동 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

그룹 내 모든 라우트에 미들웨어를 할당하려면, `middleware` 메서드를 그룹 정의 전에 사용합니다. 미들웨어는 배열에 나열된 순서대로 실행됩니다:

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first와 second 미들웨어 사용
    });

    Route::get('/user/profile', function () {
        // first와 second 미들웨어 사용
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러

여러 라우트가 동일한 컨트롤러를 사용할 경우, 그룹에 `controller` 메서드를 사용해 공통 컨트롤러를 지정할 수 있습니다. 라우트 정의에서는 호출할 컨트롤러 메서드만 작성하면 됩니다:

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹은 서브도메인 라우팅도 처리할 수 있습니다. 서브도메인에도 라우트 매개변수를 지정할 수 있으며, 해당 값을 라우트나 컨트롤러에서 사용할 수 있습니다. 그룹 정의 전에 `domain` 메서드를 호출해서 서브도메인을 지정합니다:

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

> [!WARNING]  
> 서브도메인 라우트가 정상 작동하려면, 서브도메인 라우트를 최상위 도메인 라우트보다 먼저 등록해야 합니다. 그래야 동일 URI 경로의 루트 도메인 라우트가 서브도메인 라우트를 덮어쓰는 문제를 방지할 수 있습니다.

<a name="route-group-prefixes"></a>
### 라우트 접두사

`prefix` 메서드를 사용하면 그룹 내 각 라우트 URI 앞에 지정한 문자열을 붙일 수 있습니다. 예를 들어 모든 URI에 `admin` 접두사를 붙이려면 다음과 같이 합니다:

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URI와 매치됩니다.
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두사

`name` 메서드를 사용하면 그룹 내 모든 라우트 이름에 지정한 문자열을 접두사로 붙일 수 있습니다. 예를 들어, 모든 라우트 이름에 `admin.` 접두사를 붙이려면 점(`.`)을 포함해서 다음과 같이 지정합니다:

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // 이 라우트 이름은 "admin.users"로 지정됩니다.
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

라우트나 컨트롤러 액션에 모델 ID를 전달할 때, 보통 해당 ID에 맞는 모델을 데이터베이스에서 조회합니다. Laravel의 라우트 모델 바인딩은 매번 쿼리 작성 없이 해당 모델 인스턴스를 자동 주입해 주는 편리한 방법입니다. 예를 들어 사용자 ID 대신 해당 ID와 일치하는 `User` 모델 인스턴스를 주입할 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩 (Implicit Binding)

Laravel은 암묵적 바인딩으로, 타입힌트된 Eloquent 모델 변수명과 URI 세그먼트 이름이 일치하면 자동으로 매칭된 모델 인스턴스를 주입합니다. 예를 들어 다음과 같습니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

`$user` 변수는 `App\Models\User` 타입의 모델이고 URI의 `{user}` 세그먼트와 이름이 일치하므로, 요청 URI에서 해당하는 값을 가진 ID를 자동으로 찾아 모델 인스턴스를 주입합니다. 만약 일치하는 모델이 없으면 404 응답이 자동으로 반환됩니다.

암묵적 바인딩은 컨트롤러 메서드에서도 마찬가지로 동작합니다. 예를 들어 다음과 같습니다:

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
#### 소프트 삭제된 모델

기본적으로 암묵적 바인딩은 [소프트 삭제](/docs/10.x/eloquent#soft-deleting)된 모델은 조회하지 않습니다. 하지만 `withTrashed` 메서드를 라우트 정의에 체인하면 소프트 삭제된 모델도 조회할 수 있습니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 이름 변경하기

ID 컬럼이 아닌 다른 컬럼으로 모델을 조회하고 싶다면, 라우트 매개변수 정의에서 컬럼명을 지정할 수 있습니다:

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

또는 모델 클래스 내부에서 `getRouteKeyName` 메서드를 오버라이드하여 기본 키 컬럼을 변경할 수도 있습니다:

```php
/**
 * 라우트 바인딩에 사용할 키 반환
 */
public function getRouteKeyName(): string
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
#### 커스텀 키와 범위 스코핑

여러 Eloquent 모델이 한 라우트 내에 있을 때, 두 번째 모델이 첫 번째 모델의 자식 관계에 속하도록 범위를 제한할 수 있습니다. 예를 들어 특정 사용자의 블로그 게시글을 슬러그로 조회하는 라우트 정의입니다:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

Laravel은 내부적으로 `User` 모델에 `posts`라는 관계가 있다고 추측하고, 해당 범위 내에서 `Post` 모델을 조회합니다.

커스텀 키가 없어도 범위 지정 바인딩을 하려면, 라우트 정의에 `scopeBindings` 메서드를 추가하세요:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는 그룹 전체에 적용할 수도 있습니다:

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로 범위 지정을 해제하려면 `withoutScopedBindings` 메서드를 사용할 수 있습니다:

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 매칭 실패 시 동작 커스터마이징

기본적으로 암묵적 바인딩에서 모델을 찾지 못하면 404 응답을 생성합니다. `missing` 메서드에 클로저를 넘겨 원하는 동작으로 변경할 수 있습니다. 다음 예는 모델이 없으면 다른 라우트로 리다이렉트합니다:

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

PHP 8.1부터 지원하는 [문자열 백 Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 라우트 매개변수의 타입힌트로 지정하면 Laravel은 해당 URI 세그먼트가 Enum 값에 속해야만 라우트를 실행합니다. 그렇지 않으면 404 응답이 자동 반환됩니다.

예:

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

이 Enum을 사용하는 라우트는 `{category}` 세그먼트가 `fruits` 또는 `people`일 때만 호출됩니다:

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩 (Explicit Binding)

암묵적 바인딩 대신 라우트 매개변수가 어떤 모델과 매칭되는지 명시적으로 지정할 수도 있습니다. 이렇게 하려면 `Route::model` 메서드를 사용하여 파라미터와 모델 클래스를 바인딩하세요. 보통 `RouteServiceProvider` 클래스의 `boot` 메서드에서 정의합니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * 라우트 모델 바인딩, 패턴 필터 등 정의
 */
public function boot(): void
{
    Route::model('user', User::class);

    // ...
}
```

그 후 다음과 같이 `{user}` 파라미터를 가진 라우트 정의가 해당 모델과 바인딩됩니다:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

만약 데이터베이스에 일치하는 모델이 없으면 404 응답이 자동 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 로직 변경하기

커스텀 바인딩 로직을 정의하려면 `Route::bind` 메서드를 사용하세요. 클로저는 URI 세그먼트의 값을 받고, 라우트에 주입할 모델 인스턴스를 반환해야 합니다. 역시 `RouteServiceProvider`의 `boot` 메서드에 작성합니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * 라우트 모델 바인딩, 패턴 필터 등 정의
 */
public function boot(): void
{
    Route::bind('user', function (string $value) {
        return User::where('name', $value)->firstOrFail();
    });

    // ...
}
```

또는 Eloquent 모델의 `resolveRouteBinding` 메서드를 오버라이드해서 해당 값에 맞는 모델 인스턴스를 반환하도록 할 수 있습니다:

```php
/**
 * 바인딩된 값에 맞는 모델 조회
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

만약 [암묵적 바인딩 범위 지정](#implicit-model-binding-scoping)을 사용하는 경우, 자식 바인딩 시에는 `resolveChildRouteBinding` 메서드가 호출됩니다:

```php
/**
 * 바인딩된 값으로 자식 모델 조회
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

`Route::fallback` 메서드를 사용하면, 어떤 라우트도 매칭하지 못했을 때 처리할 라우트를 정의할 수 있습니다. 보통 매칭 실패 시에는 예외 핸들러에서 "404" 페이지를 띄우지만, `fallback` 라우트는 보통 `routes/web.php`에 정의되므로 `web` 미들웨어 그룹이 적용됩니다. 필요하면 추가 미들웨어도 지정 가능합니다:

```php
Route::fallback(function () {
    // ...
});
```

> [!WARNING]  
> 폴백 라우트는 애플리케이션에서 가장 마지막에 등록되어야 합니다.

<a name="rate-limiting"></a>
## 속도 제한 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 속도 제한기 정의

Laravel은 강력하고 유연한 속도 제한 기능을 제공하여 특정 라우트 또는 라우트 그룹에 대한 요청 빈도를 제한할 수 있습니다. 먼저 애플리케이션 요구에 맞게 속도 제한기 설정을 정의해야 합니다.

보통 `App\Providers\RouteServiceProvider` 클래스의 `boot` 메서드에서 정의하며, 기본적으로 이 클래스에는 `routes/api.php` 라우트에 적용되는 예시가 포함되어 있습니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 라우트 모델 바인딩, 패턴 필터, 기타 설정 정의
 */
protected function boot(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });

    // ...
}
```

`RateLimiter::for` 메서드는 속도 제한기 이름과, 해당 제한기를 적용할 때 반환할 제한 설정을 반환하는 클로저를 인자로 받습니다. 제한 설정은 `Illuminate\Cache\RateLimiting\Limit` 인스턴스입니다. 제한기 이름은 임의의 문자열로 지정 가능합니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 라우트 모델 바인딩, 패턴 필터 등 정의
 */
protected function boot(): void
{
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });

    // ...
}
```

요청이 제한을 초과하면 Laravel은 자동으로 429 HTTP 상태 코드를 반환합니다. 커스텀 응답을 정의하려면 `response` 메서드를 사용하세요:

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

속도 제한기 콜백은 HTTP 요청 인스턴스를 받으므로, 요청이나 인증된 사용자에 따라 동적으로 제한을 조정할 수 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
#### 제한 구분하기

특정 값에 따라 제한을 구분하고 싶을 수 있습니다. 예를 들어 IP별로 초당 100회 요청을 허용하려면, 제한에 `by` 메서드로 해당 값을 지정하세요:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100)->by($request->ip());
});
```

또 다른 예제로는, 인증 유저별로 초당 100회, 비회원 IP별로 초당 10회 제한하는 경우입니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
                ? Limit::perMinute(100)->by($request->user()->id)
                : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 여러 제한 동시에 적용하기

필요하면 제한 배열을 반환해 라우트에 대한 여러 제한을 순서대로 검사할 수 있습니다:

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 속도 제한기 연결

`throttle` 미들웨어를 통해 라우트 또는 그룹에 속도 제한기를 적용할 수 있습니다. 미들웨어 인자로 제한기 이름을 전달합니다:

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
#### Redis를 이용한 속도 제한 처리

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스에 맵핑됩니다. 하지만 Redis 캐시 드라이버를 사용할 경우, Redis 전용 `ThrottleRequestsWithRedis` 클래스를 사용하도록 HTTP 커널(`App\Http\Kernel`)에서 변경하면 더 효율적인 관리가 가능합니다:

```php
'throttle' => \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
```

<a name="form-method-spoofing"></a>
## 폼 메서드 스푸핑 (Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 메서드를 직접 지원하지 않으므로, 이러한 요청을 라우트에서 처리하려면 숨겨진 `_method` 필드를 추가해야 합니다. `_method` 값이 실제 HTTP 메서드로 사용됩니다:

```html
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

편의를 위해, Blade의 `@method` 디렉티브를 사용해 `_method` 필드를 생성할 수 있습니다:

```html
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 접근하기 (Accessing the Current Route)

`Route` 파사드를 통해 현재 요청을 처리 중인 라우트 정보에 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route 인스턴스
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

`Route` 파사드와 `Route` 인스턴스에 사용 가능한 모든 메서드는 API 문서의 [Router](https://laravel.com/api/10.x/Illuminate/Routing/Router.html)와 [Route](https://laravel.com/api/10.x/Illuminate/Routing/Route.html) 클래스를 참고하세요.

<a name="cors"></a>
## 교차 출처 리소스 공유 (CORS)

Laravel은 CORS `OPTIONS` HTTP 요청에 대해 애플리케이션에서 설정한 값으로 자동 응답할 수 있습니다. 이 설정은 `config/cors.php`에서 관리하며, `OPTIONS` 요청은 기본 글로벌 미들웨어 스택에 포함된 `HandleCors` 미들웨어에서 자동 처리됩니다. 글로벌 미들웨어 스택은 HTTP 커널(`App\Http\Kernel`)에 위치합니다.

> [!NOTE]  
> CORS와 관련 헤더에 대한 자세한 내용은 [MDN 웹 문서의 CORS 소개](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

프로덕션 배포 시 Laravel의 라우트 캐시를 활용하세요. 라우트 캐시는 애플리케이션의 모든 라우트를 등록하는 데 걸리는 시간을 크게 줄여줍니다. 캐시 생성은 `route:cache` Artisan 명령어로 수행합니다:

```shell
php artisan route:cache
```

명령어 실행 후 캐시된 라우트가 모든 요청에 로드됩니다. 라우트를 추가하거나 수정하면 반드시 캐시를 다시 생성해야 하므로, 보통 배포 시에만 이 명령어를 실행합니다.

생성된 라우트 캐시는 다음 명령어로 삭제할 수 있습니다:

```shell
php artisan route:clear
```