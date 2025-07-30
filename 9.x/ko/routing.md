# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [리디렉트 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록](#the-route-list)
- [라우트 매개변수](#route-parameters)
    - [필수 매개변수](#required-parameters)
    - [선택적 매개변수](#parameters-optional-parameters)
    - [정규 표현식 제약 조건](#parameters-regular-expression-constraints)
- [이름 있는 라우트](#named-routes)
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
- [요청 속도 제한](#rate-limiting)
    - [요청 속도 제한기 정의](#defining-rate-limiters)
    - [라우트에 요청 속도 제한기 적용](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근](#accessing-the-current-route)
- [교차 출처 리소스 공유 (CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

가장 기본적인 Laravel 라우트는 URI와 클로저를 받아, 복잡한 라우팅 설정 파일 없이 간단하고 표현력 있게 라우트와 동작을 정의할 수 있습니다:

```
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
#### 기본 라우트 파일 (The Default Route Files)

모든 Laravel 라우트는 `routes` 디렉터리에 위치한 라우트 파일에 정의됩니다. 이 파일들은 애플리케이션의 `App\Providers\RouteServiceProvider`에 의해 자동으로 로드됩니다. `routes/web.php` 파일은 웹 인터페이스용 라우트를 정의하며, 이 라우트들은 세션 상태, CSRF 보호와 같은 기능을 제공하는 `web` 미들웨어 그룹이 할당됩니다. 반면, `routes/api.php`에 정의된 라우트는 상태 비저장(stateless)이며 `api` 미들웨어 그룹이 할당됩니다.

대부분 애플리케이션은 `routes/web.php` 파일에서 라우트를 정의하는 것으로 시작합니다. `routes/web.php`에 정의된 라우트는 브라우저에서 해당 URL을 입력하면 접근할 수 있습니다. 예를 들어, 다음과 같은 라우트는 브라우저에서 `http://example.com/user`로 접속 시 접근 가능합니다:

```
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

`routes/api.php`에 정의된 라우트는 `RouteServiceProvider`에서 라우트 그룹 안에 중첩되어 있습니다. 이 그룹 내에서는 `/api` URI 접두사가 자동으로 적용되기 때문에, 파일 내 각 라우트에 수동으로 접두사를 추가할 필요가 없습니다. 접두사 및 기타 라우트 그룹 옵션은 `RouteServiceProvider` 클래스를 수정하여 변경할 수 있습니다.

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메서드 (Available Router Methods)

라우터는 다양한 HTTP 메서드에 응답하는 라우트를 등록할 수 있습니다:

```
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

여러 HTTP 메서드에 모두 응답하는 라우트가 필요할 경우 `match` 메서드를 사용할 수 있습니다. 또는 모든 HTTP 메서드에 응답하는 라우트를 `any` 메서드로 등록할 수도 있습니다:

```
Route::match(['get', 'post'], '/', function () {
    //
});

Route::any('/', function () {
    //
});
```

> [!NOTE]
> 같은 URI를 공유하는 여러 라우트를 정의할 때에는, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드로 정의한 라우트를 먼저 작성하세요. 그런 다음 `any`, `match`, `redirect` 메서드로 정의한 라우트를 작성하는 것이 좋습니다. 이렇게 하면 들어오는 요청이 올바른 라우트와 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입 (Dependency Injection)

라우트 콜백 함수에서 필요한 의존성을 타입 힌트로 지정하면, Laravel의 [서비스 컨테이너](/docs/9.x/container)가 자동으로 해당 의존성을 주입해줍니다. 예를 들어, 현재 HTTP 요청을 자동으로 주입받기 위해 `Illuminate\Http\Request` 클래스를 타입 힌트할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호 (CSRF Protection)

참고로, `web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 해당하는 HTML 폼에는 반드시 CSRF 토큰 필드를 포함해야 합니다. 그렇지 않으면 요청이 거부됩니다. CSRF 보호에 관한 자세한 내용은 [CSRF 문서](/docs/9.x/csrf)를 참고하세요:

```
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리디렉트 라우트 (Redirect Routes)

다른 URI로 리디렉트하는 라우트를 정의할 때는 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 간단한 리디렉트를 위해 전체 라우트나 컨트롤러를 정의할 필요 없이 편리한 단축키를 제공합니다:

```
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 302 상태 코드를 반환하며, 세 번째 선택 인자로 상태 코드를 변경할 수 있습니다:

```
Route::redirect('/here', '/there', 301);
```

또는, 301 상태 코드를 반환하고 싶다면 `Route::permanentRedirect` 메서드를 사용할 수 있습니다:

```
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리디렉트 라우트에서 라우트 매개변수를 사용할 때는 Laravel에서 예약한 `destination`과 `status` 매개변수는 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트 (View Routes)

라우트가 단순히 뷰를 반환하는 용도라면, `Route::view` 메서드를 사용할 수 있습니다. `redirect` 메서드와 유사하게, 전체 라우트나 컨트롤러를 정의하지 않아도 편리하게 사용할 수 있습니다. 첫 번째 인자로 URI, 두 번째 인자로 뷰 이름을 받고, 선택적으로 세 번째 인자로 뷰에 전달할 데이터를 배열로 넘길 수도 있습니다:

```
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 매개변수를 사용할 때는 Laravel에서 예약된 `view`, `data`, `status`, `headers` 이름은 사용할 수 없습니다.

<a name="the-route-list"></a>
### 라우트 목록 (The Route List)

`route:list` Artisan 명령어를 사용하면 애플리케이션에 정의된 모든 라우트를 쉽게 확인할 수 있습니다:

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 미들웨어는 `route:list` 명령어 출력에 표시되지 않습니다. 미들웨어를 포함한 자세한 정보를 보려면 `-v` 옵션을 추가하세요:

```shell
php artisan route:list -v
```

특정 URI 접두사로 시작하는 라우트만 확인하려면 다음과 같이 실행합니다:

```shell
php artisan route:list --path=api
```

또한, 서드파티 패키지에서 정의한 라우트를 숨기려면 `--except-vendor` 옵션을 사용하세요:

```shell
php artisan route:list --except-vendor
```

반대로 서드파티 패키지에서 정의한 라우트만 보려면 `--only-vendor` 옵션을 사용할 수 있습니다:

```shell
php artisan route:list --only-vendor
```

<a name="route-parameters"></a>
## 라우트 매개변수 (Route Parameters)

<a name="required-parameters"></a>
### 필수 매개변수 (Required Parameters)

때때로 URI의 특정 부분을 캡처해야 할 때가 있습니다. 예를 들어, URL에서 사용자의 ID를 캡처할 수 있습니다. 이는 라우트 매개변수를 정의하여 구현합니다:

```
Route::get('/user/{id}', function ($id) {
    return 'User '.$id;
});
```

필요한 만큼 많은 라우트 매개변수를 정의할 수도 있습니다:

```
Route::get('/posts/{post}/comments/{comment}', function ($postId, $commentId) {
    //
});
```

라우트 매개변수는 항상 중괄호 `{}` 로 감싸고, 알파벳 문자로 구성해야 합니다. 밑줄(`_`)도 매개변수 이름에 포함할 수 있습니다. 라우트 매개변수는 라우트 콜백이나 컨트롤러 메서드의 인수 순서에 맞춰 주입되며, 인수 이름은 중요하지 않습니다.

<a name="parameters-and-dependency-injection"></a>
#### 매개변수와 의존성 주입 (Parameters & Dependency Injection)

만약 라우트 콜백이 의존성을 갖고 있고 Laravel 서비스 컨테이너가 이를 자동 주입하기 원한다면, 라우트 매개변수는 의존성 인수 뒤에 위치시켜야 합니다:

```
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 매개변수 (Optional Parameters)

URI에 항상 포함될 필요가 없는 선택적 매개변수를 정의하려면 매개변수 이름 뒤에 `?` 를 붙이면 됩니다. 이 때, 해당 변수에는 기본값을 정의해야 합니다:

```
Route::get('/user/{name?}', function ($name = null) {
    return $name;
});

Route::get('/user/{name?}', function ($name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규 표현식 제약 조건 (Regular Expression Constraints)

라우트 매개변수 값의 형식을 제한하려면 라우트 인스턴스의 `where` 메서드를 사용해 제약 조건을 걸 수 있습니다. `where` 메서드는 제약할 매개변수 이름과 정규 표현식을 인자로 받습니다:

```
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

편리하게도, 자주 쓰는 패턴을 위한 헬퍼 메서드도 제공됩니다:

```
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

만약 들어오는 요청이 라우트 제약 조건과 일치하지 않으면 404 HTTP 응답이 자동으로 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약 조건 (Global Constraints)

특정 이름의 라우트 매개변수가 항상 특정 정규 표현식 제약 조건을 가지게 하려면 `pattern` 메서드를 사용하세요. 이러한 패턴은 `App\Providers\RouteServiceProvider` 클래스의 `boot` 메서드에 정의하는 것이 일반적입니다:

```
/**
 * 라우트 모델 바인딩, 패턴 필터 등을 정의합니다.
 *
 * @return void
 */
public function boot()
{
    Route::pattern('id', '[0-9]+');
}
```

패턴이 정의되면 해당 이름을 가진 모든 라우트 매개변수에 자동 적용됩니다:

```
Route::get('/user/{id}', function ($id) {
    // {id}가 숫자인 경우만 실행됨
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시 (Encoded Forward Slashes)

Laravel 라우트 컴포넌트는 `/` 문자를 제외한 모든 문자를 라우트 매개변수 값에 허용합니다. 만약 `/` 문자를 포함시키려면 `where` 메서드에 적절한 정규 표현식을 지정해 명시적으로 허용해야 합니다:

```
Route::get('/search/{search}', function ($search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 라우트의 마지막 세그먼트에서만 지원됩니다.

<a name="named-routes"></a>
## 이름 있는 라우트 (Named Routes)

이름 있는 라우트는 특정 라우트의 URL이나 리디렉트를 편리하게 생성할 수 있게 해줍니다. 라우트 정의에 `name` 메서드를 체인으로 연결해 이름을 지정할 수 있습니다:

```
Route::get('/user/profile', function () {
    //
})->name('profile');
```

컨트롤러 액션에도 이름을 지정할 수 있습니다:

```
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!WARNING]
> 라우트 이름은 반드시 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 이름 있는 라우트를 이용한 URL 생성 (Generating URLs To Named Routes)

라우트에 이름을 지정한 후에는 Laravel의 `route`와 `redirect` 헬퍼 함수를 사용하여 URL이나 리디렉트를 생성할 때 이름을 사용할 수 있습니다:

```
// URL 생성...
$url = route('profile');

// 리디렉트 생성...
return redirect()->route('profile');

return to_route('profile');
```

만약 이름 있는 라우트에 매개변수가 정의되어 있다면, 두 번째 인자로 매개변수 배열을 넘겨 해당 위치에 자동 삽입할 수 있습니다:

```
Route::get('/user/{id}/profile', function ($id) {
    //
})->name('profile');

$url = route('profile', ['id' => 1]);
```

추가로 넘긴 매개변수는 쿼리 문자열에 자동으로 추가됩니다:

```
Route::get('/user/{id}/profile', function ($id) {
    //
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// 결과: /user/1/profile?photos=yes
```

> [!NOTE]
> 때로 URL 매개변수에 대해 요청 전역의 기본값(예: 현재 로케일)을 지정할 필요가 있습니다. 이럴 때는 [`URL::defaults` 메서드](/docs/9.x/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 확인하기 (Inspecting The Current Route)

현재 요청이 지정된 이름 있는 라우트에 매칭되는지 확인하려면, 라우트 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어 라우트 미들웨어에서 현재 라우트 이름을 확인하는 코드는 아래와 같습니다:

```
/**
 * 들어오는 요청을 처리합니다.
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
## 라우트 그룹 (Route Groups)

라우트 그룹은 많은 라우트에 공통 속성(예: 미들웨어)을 반복해서 정의하지 않고 공유할 수 있도록 해줍니다.

중첩된 그룹은 부모 그룹의 속성들과 적절히 "병합"하려고 시도합니다. 미들웨어와 `where` 조건은 병합되고, 이름과 접두사는 뒤에 덧붙여집니다. 네임스페이스 구분자와 URI 접두사 슬래시는 필요한 위치에 자동으로 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어 (Middleware)

그룹 내 모든 라우트에 미들웨어를 할당하려면, 그룹을 정의하기 전에 `middleware` 메서드를 사용하세요. 미들웨어는 배열에 명시된 순서대로 실행됩니다:

```
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // 첫 번째 및 두 번째 미들웨어가 적용됨
    });

    Route::get('/user/profile', function () {
        // 첫 번째 및 두 번째 미들웨어가 적용됨
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러 (Controllers)

여러 라우트가 동일한 컨트롤러를 사용하는 경우, `controller` 메서드를 통해 그룹 내 모든 라우트에 공통 컨트롤러를 지정할 수 있습니다. 이후 각 라우트에서는 호출할 컨트롤러 메서드 이름만 지정하면 됩니다:

```
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅 (Subdomain Routing)

라우트 그룹은 서브도메인 라우팅에도 사용됩니다. 서브도메인에서도 라우트 URI처럼 매개변수를 지정할 수 있으며, 서브도메인의 일부를 캡처해 라우트나 컨트롤러에서 사용할 수 있습니다. 서브도메인은 `domain` 메서드로 정의합니다:

```
Route::domain('{account}.example.com')->group(function () {
    Route::get('user/{id}', function ($account, $id) {
        //
    });
});
```

> [!WARNING]
> 서브도메인 라우트가 정상 동작하려면, 루트 도메인 라우트를 등록하기 전에 서브도메인 라우트를 등록해야 합니다. 그렇지 않으면 동일한 URI 경로를 가진 루트 도메인 라우트가 서브도메인 라우트를 덮어쓸 수 있습니다.

<a name="route-group-prefixes"></a>
### 라우트 접두사 (Route Prefixes)

`prefix` 메서드로 그룹 내 모든 라우트 URI 앞에 동일한 접두사를 붙일 수 있습니다. 예를 들어, 그룹 내 모든 라우트 앞에 `admin`을 붙이고 싶을 때 다음과 같이 작성합니다:

```
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL에 매칭됨
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두사 (Route Name Prefixes)

`name` 메서드를 사용하면 그룹 내 모든 라우트 이름에 지정한 문자열을 접두사로 붙일 수 있습니다. 예를 들어, 그룹 내 모든 라우트 이름 앞에 `admin.`을 붙이고 싶을 때는 다음과 같이 작성합니다:

```
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // 라우트 이름이 "admin.users"가 됨
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

라우트나 컨트롤러 액션에 모델 ID를 주입할 때, 해당 ID에 맞는 모델을 데이터베이스에서 조회해야 하는 경우가 많습니다. Laravel의 라우트 모델 바인딩은 이러한 모델 인스턴스를 자동으로 주입해주는 편리한 기능입니다. 예를 들어, 사용자 ID 대신 해당 ID에 맞는 `User` 모델 인스턴스를 주입받을 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩 (Implicit Binding)

Laravel은 라우트나 컨트롤러에서 타입힌트된 Eloquent 모델이 있고, 변수명이 라우트 URI에 정의된 세그먼트 이름과 일치하면 이를 자동으로 모델 인스턴스로 변환합니다. 예를 들어:

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

`$user` 변수는 `App\Models\User` 모델 타입을 가지며, URI 세그먼트 `{user}`와 이름이 일치하기 때문에, 요청 URI의 값과 일치하는 ID를 가진 `User` 모델 인스턴스를 자동으로 주입합니다. 만약 데이터베이스에서 해당 인스턴스를 찾지 못하면 404 HTTP 응답이 자동으로 반환됩니다.

컨트롤러 메서드에서도 암묵적 바인딩을 사용할 수 있습니다. 아래처럼 URI 세그먼트 `{user}`와 컨트롤러 메서드의 `$user` 변수명이 일치해야 합니다:

```
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
#### 소프트 삭제된 모델 (Soft Deleted Models)

기본적으로 암묵적 바인딩은 [소프트 삭제된](/docs/9.x/eloquent#soft-deleting) 모델을 조회하지 않습니다. 하지만, `withTrashed` 메서드를 라우트 정의에 체인으로 붙여 해당 모델도 조회하도록 설정할 수 있습니다:

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 이름 커스터마이징 (Customizing The Key)

모델 조회 시 기본적으로 `id` 컬럼을 사용하지만, 다른 컬럼을 기준으로 하려면 라우트 매개변수에 컬럼명을 지정하면 됩니다:

```
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

항상 특정 모델 클래스가 `id` 외의 컬럼을 사용하도록 하려면 Eloquent 모델의 `getRouteKeyName` 메서드를 오버라이드하세요:

```
/**
 * 모델의 라우트 키 반환
 *
 * @return string
 */
public function getRouteKeyName()
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
#### 커스텀 키와 스코핑 (Custom Keys & Scoping)

하나의 라우트에서 여러 Eloquent 모델을 암묵적으로 바인딩할 때, 두 번째 모델을 첫 번째 모델의 자식 관계로 제한하고 싶을 수 있습니다. 예를 들어, 특정 사용자의 슬러그로 블로그 게시글을 조회하는 라우트를 다음과 같이 정의할 수 있습니다:

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

Laravel은 규칙에 따라 첫 번째 모델(`User`)가 `posts`라는 연관관계를 가지고 있다는 것을 추론하고, 두 번째 모델(`Post`) 조회 시 이 관계를 사용해 범위를 제한합니다.

명시적으로 해당 라우트에 대해 스코프 바인딩을 적용하려면 `scopeBindings` 메서드를 체인으로 호출하세요:

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는 그룹 전체에 스코핑을 적용할 수도 있습니다:

```
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

반대로, 스코핑을 아예 하지 않도록 하려면 `withoutScopedBindings` 메서드를 호출하세요:

```
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 모델 미발견 시 동작 커스터마이징 (Customizing Missing Model Behavior)

암묵적 바인딩된 모델을 찾지 못했을 때 기본적으로 404 HTTP 응답이 반환됩니다. 그러나 `missing` 메서드를 사용해 사용자 정의 동작을 지정할 수 있습니다. `missing` 메서드는 모델을 찾지 못했을 때 호출할 클로저를 받습니다:

```
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

PHP 8.1부터 [Enums](https://www.php.net/manual/en/language.enumerations.backed.php)이 지원됩니다. Laravel은 라우트 정의에 [문자열 기반 Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 타입힌트로 지정하면, 해당 라우트 세그먼트가 유효한 Enum 값인 경우에만 라우트를 실행합니다. 그렇지 않으면 404 HTTP 응답이 반환됩니다. 예를 들어 다음과 같은 Enum이 있다고 가정합시다:

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

해당 Enum을 타입힌트로 사용하는 라우트는 `{category}` 세그먼트가 `fruits` 또는 `people`일 때만 호출됩니다:

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩 (Explicit Binding)

Laravel의 암묵적 바인딩을 사용하지 않고도, 라우트 매개변수와 모델 간 연결을 명시적으로 정의할 수 있습니다. 라우트 서비스 프로바이더의 `boot` 메서드에서 라우터의 `model` 메서드를 사용하여 매개변수 이름과 모델 클래스를 매핑합니다:

```
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * 라우트 모델 바인딩, 패턴 필터 등을 정의합니다.
 *
 * @return void
 */
public function boot()
{
    Route::model('user', User::class);

    // ...
}
```

그 후, `{user}` 매개변수를 포함하는 라우트를 정의합니다:

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    //
});
```

`{user}` 매개변수는 `App\Models\User` 모델에 바인딩되었으므로, `users/1` 요청 시 ID가 1인 `User` 인스턴스가 자동 주입됩니다.

만약 일치하는 모델을 찾지 못하면 404 HTTP 응답이 자동으로 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 바인딩 해결 로직 커스터마이징 (Customizing The Resolution Logic)

모델 바인딩 해결 방식을 직접 정의하려면 `Route::bind` 메서드를 사용하세요. 이 메서드에 넘기는 클로저는 URI 세그먼트 값을 매개변수로 받고, 라우트에 주입할 모델 인스턴스를 반환해야 합니다. 역시 `RouteServiceProvider`의 `boot` 메서드에 정의합니다:

```
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * 라우트 모델 바인딩, 패턴 필터 등을 정의합니다.
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

또는 Eloquent 모델 내에서 `resolveRouteBinding` 메서드를 오버라이드하여 맞춤 해결 로직을 구현할 수도 있습니다:

```
/**
 * 바인딩 값에 맞는 모델을 조회합니다.
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

만약 [암묵적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용하는 라우트라면, 부모 모델의 자식 바인딩은 `resolveChildRouteBinding` 메서드로 해결됩니다:

```
/**
 * 바인딩 값에 맞는 자식 모델을 조회합니다.
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

`Route::fallback` 메서드를 사용하면, 들어오는 요청과 매칭되는 다른 라우트가 없을 때 실행할 라우트를 정의할 수 있습니다. 보통 미처리 요청은 애플리케이션의 예외 핸들러가 "404" 페이지를 자동으로 렌더링합니다. 하지만 `fallback` 라우트는 `routes/web.php`에 정의되므로 `web` 미들웨어 그룹의 모든 미들웨어가 적용됩니다. 필요한 경우 추가 미들웨어도 적용할 수 있습니다:

```
Route::fallback(function () {
    //
});
```

> [!WARNING]
> 폴백 라우트는 항상 애플리케이션에서 등록하는 가장 마지막 라우트여야 합니다.

<a name="rate-limiting"></a>
## 요청 속도 제한 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 요청 속도 제한기 정의 (Defining Rate Limiters)

Laravel은 특정 라우트나 라우트 그룹의 요청 트래픽을 제한할 수 있는 강력하고 커스터마이징 가능한 요청 속도 제한 서비스를 제공합니다. 먼저, 애플리케이션 요구사항에 맞는 제한기 설정을 정의하세요. 보통 `App\Providers\RouteServiceProvider` 클래스의 `configureRateLimiting` 메서드에서 정의하며, 이 곳에는 `routes/api.php` 라우트에 적용하는 기본 제한기가 포함되어 있습니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 요청 속도 제한기를 구성합니다.
 */
protected function configureRateLimiting(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
}
```

제한기는 `RateLimiter` 파사드의 `for` 메서드를 통해 정의합니다. `for`는 제한기 이름과 제한 설정을 반환하는 클로저를 받습니다. 제한 설정은 `Illuminate\Cache\RateLimiting\Limit` 클래스 인스턴스이며, 해당 클래스는 빠르게 제한을 정의할 수 있는 헬퍼 메서드를 제공합니다. 제한기 이름은 원하는 문자열로 지정 가능합니다:

```
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 요청 속도 제한기를 구성합니다.
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

들어오는 요청이 지정된 제한을 초과하면 Laravel은 자동으로 429 HTTP 상태 코드와 함께 응답을 반환합니다. 직접 응답을 정의하려면 `response` 메서드를 사용할 수 있습니다:

```
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

제한기 콜백은 들어오는 HTTP 요청 인스턴스를 받으므로, 인증된 사용자 정보 등 요청에 따라 제한을 동적으로 설정할 수 있습니다:

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
#### 요청 제한 분할 (Segmenting Rate Limits)

예를 들어, IP 주소별로 라우트 접근을 분할 제한하려면 제한 생성 시 `by` 메서드를 사용하세요:

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100)->by($request->ip());
});
```

또 다른 예시로, 인증된 사용자 ID별로 100회, 비회원(IP)별로 10회 제한을 설정할 수도 있습니다:

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
                ? Limit::perMinute(100)->by($request->user()->id)
                : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 다중 요청 제한 (Multiple Rate Limits)

필요에 따라 배열로 여러 제한을 반환할 수도 있습니다. 배열 내 제한들은 순서대로 평가됩니다:

```
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 요청 속도 제한기 적용 (Attaching Rate Limiters To Routes)

요청 속도 제한기는 `throttle` [미들웨어](/docs/9.x/middleware)에 이름을 전달하여 라우트나 라우트 그룹에 적용할 수 있습니다:

```
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
#### Redis를 이용한 요청 제한 (Throttling With Redis)

보통 `throttle` 미들웨어는 애플리케이션 HTTP 커널(`App\Http\Kernel`)에서 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스로 매핑되어 있습니다. 그러나 캐시 드라이버로 Redis를 사용하는 경우, Redis 기반 요청 제한에 효율적인 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 클래스로 매핑을 변경할 수 있습니다:

```
'throttle' => \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
```

<a name="form-method-spoofing"></a>
## 폼 메서드 스푸핑 (Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` HTTP 메서드를 직접 지원하지 않습니다. 따라서 이러한 메서드에 대응하는 라우트를 HTML 폼에서 호출할 때는 폼에 숨겨진 `_method` 필드를 추가해야 하며, 이 값이 HTTP 요청 메서드로 처리됩니다:

```
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

편리하게, `@method` [Blade 디렉티브](/docs/9.x/blade)를 사용해 `_method` 입력 필드를 생성할 수 있습니다:

```
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 접근 (Accessing The Current Route)

`Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 사용하면 요청을 처리하는 현재 라우트 정보를 얻을 수 있습니다:

```
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route 객체
$name = Route::currentRouteName(); // 문자열
$action = Route::currentRouteAction(); // 문자열
```

라우터 및 라우트 클래스의 모든 메서드는 [Route 파사드의 기반 클래스](https://laravel.com/api/9.x/Illuminate/Routing/Router.html)와 [라우트 인스턴스](https://laravel.com/api/9.x/Illuminate/Routing/Route.html) API 문서를 참고하세요.

<a name="cors"></a>
## 교차 출처 리소스 공유 (CORS)

Laravel은 CORS `OPTIONS` HTTP 요청에 대해 자동으로 설정한 값을 응답할 수 있습니다. 모든 CORS 설정은 애플리케이션 `config/cors.php` 설정 파일에서 관리합니다. `OPTIONS` 요청은 기본으로 글로벌 미들웨어 스택에 포함된 `HandleCors` [미들웨어](/docs/9.x/middleware)가 자동 처리합니다. 글로벌 미들웨어 스택은 애플리케이션 HTTP 커널(`App\Http\Kernel`)에 위치합니다.

> [!NOTE]
> CORS와 CORS 헤더에 관한 자세한 정보는 [MDN 웹 문서의 CORS 관련 페이지](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

애플리케이션을 프로덕션에 배포할 때는 Laravel의 라우트 캐시를 적극 활용하세요. 라우트 캐시는 모든 라우트를 등록하는 데 걸리는 시간을 크게 줄여줍니다. 라우트 캐시를 생성하려면 다음 Artisan 명령어를 실행하세요:

```shell
php artisan route:cache
```

이 명령을 실행하면 캐시된 라우트 파일이 매 요청마다 로드됩니다. 새로운 라우트를 추가한 경우에는 반드시 라우트 캐시를 새로 생성해야 하므로, 이 명령어는 프로젝트 배포 시에만 실행하는 것이 좋습니다.

라우트 캐시를 삭제하려면 다음 명령어를 사용하세요:

```shell
php artisan route:clear
```