# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [리다이렉트 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
- [라우트 매개변수](#route-parameters)
    - [필수 매개변수](#required-parameters)
    - [선택적 매개변수](#parameters-optional-parameters)
    - [정규 표현식 제약 조건](#parameters-regular-expression-constraints)
- [이름이 지정된 라우트](#named-routes)
- [라우트 그룹](#route-groups)
    - [미들웨어](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [서브도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 접두사](#route-group-prefixes)
    - [라우트 이름 접두사](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암묵적 바인딩](#implicit-binding)
    - [명시적 바인딩](#explicit-binding)
- [폴백 라우트](#fallback-routes)
- [속도 제한](#rate-limiting)
    - [속도 제한기 정의](#defining-rate-limiters)
    - [라우트에 속도 제한기 적용](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근](#accessing-the-current-route)
- [교차 출처 리소스 공유(CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

가장 기본적인 Laravel 라우트는 URI와 클로저를 받아, 별도의 복잡한 라우팅 구성 파일 없이도 간단하고 표현력 있게 라우트와 동작을 정의할 수 있습니다:

```
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
#### 기본 라우트 파일

모든 Laravel 라우트는 `routes` 디렉터리에 위치한 라우트 파일에서 정의합니다. 이 파일들은 애플리케이션의 `App\Providers\RouteServiceProvider`에 의해 자동으로 로드됩니다. `routes/web.php` 파일은 웹 인터페이스를 위한 라우트를 정의하며, 이 라우트들은 세션 상태나 CSRF 보호 같은 기능을 제공하는 `web` 미들웨어 그룹에 할당됩니다. `routes/api.php`에 정의된 라우트들은 상태가 없으며 `api` 미들웨어 그룹에 할당됩니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에 라우트를 정의하는 것부터 시작합니다. `routes/web.php`에 정의된 라우트는 브라우저에서 해당 라우트의 URL로 접근할 수 있습니다. 예를 들어, 다음 라우트는 브라우저에서 `http://example.com/user`로 접근할 수 있습니다:

```
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

`routes/api.php` 파일에 정의된 라우트는 `RouteServiceProvider`에 의해 라우트 그룹 안에 포함됩니다. 이 그룹 내에서는 `/api` URI 접두사가 자동으로 적용되므로 파일 내 모든 라우트에 수동으로 붙일 필요가 없습니다. 접두사나 기타 라우트 그룹 옵션은 `RouteServiceProvider` 클래스를 수정하여 변경할 수 있습니다.

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메서드

라우터는 모든 HTTP 동사에 응답하는 라우트를 등록할 수 있습니다:

```
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

때때로 여러 HTTP 동사에 응답하는 라우트를 등록해야 할 때가 있습니다. 이럴 경우 `match` 메서드를 사용합니다. 또는 모든 HTTP 동사에 응답하는 라우트가 필요하면 `any` 메서드를 사용합니다:

```
Route::match(['get', 'post'], '/', function () {
    //
});

Route::any('/', function () {
    //
});
```

> [!TIP]
> 같은 URI를 공유하는 여러 라우트를 정의할 때, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트는 `any`, `match`, `redirect` 메서드보다 먼저 정의해야 합니다. 이렇게 해야 들어오는 요청이 올바른 라우트와 일치합니다.

<a name="dependency-injection"></a>
#### 의존성 주입 (Dependency Injection)

라우트의 콜백 시그니처에 필요한 의존성을 타입 힌트할 수 있습니다. 선언된 의존성은 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)에 의해 자동으로 해결되어 콜백에 주입됩니다. 예를 들어, `Illuminate\Http\Request` 클래스를 타입 힌트하여 현재 HTTP 요청을 자동으로 주입할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 라우트를 가리키는 모든 HTML 폼에는 반드시 CSRF 토큰 필드를 포함해야 합니다. 그렇지 않으면 요청이 거부됩니다. CSRF 보호에 관한 자세한 내용은 [CSRF 문서](/docs/{{version}}/csrf)를 참고하세요:

```
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리다이렉트 라우트 (Redirect Routes)

다른 URI로 리다이렉트하는 라우트를 정의할 때는 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 간단한 리다이렉트를 위해 전체 라우트나 컨트롤러를 정의할 필요 없는 편리한 단축 기능을 제공합니다:

```
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 상태 코드 302를 반환합니다. 선택적 세 번째 인수로 상태 코드를 지정할 수 있습니다:

```
Route::redirect('/here', '/there', 301);
```

또는 `Route::permanentRedirect` 메서드를 사용하여 301 상태 코드를 반환할 수도 있습니다:

```
Route::permanentRedirect('/here', '/there');
```

> [!NOTE]
> 리다이렉트 라우트에서 라우트 매개변수를 사용할 때 Laravel에서 예약된 다음 매개변수명은 사용할 수 없습니다: `destination` 및 `status`.

<a name="view-routes"></a>
### 뷰 라우트 (View Routes)

라우트가 단순히 [뷰](/docs/{{version}}/views)를 반환하기만 하면, `Route::view` 메서드를 사용할 수 있습니다. `redirect` 메서드처럼 전체 라우트나 컨트롤러를 정의하지 않고 간단히 쓸 수 있는 단축 메서드입니다. `view` 메서드는 첫 번째 인수로 URI, 두 번째 인수로 뷰 이름을 받으며, 선택적인 세 번째 인수로 뷰에 전달할 데이터를 배열 형태로 제공합니다:

```
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!NOTE]
> 뷰 라우트에서 라우트 매개변수를 사용할 때 다음 매개변수명은 Laravel에서 예약되어 있으므로 사용할 수 없습니다: `view`, `data`, `status`, `headers`.

<a name="route-parameters"></a>
## 라우트 매개변수 (Route Parameters)

<a name="required-parameters"></a>
### 필수 매개변수 (Required Parameters)

URI 조각을 캡처해야 할 때가 있습니다. 예를 들어, URL에서 사용자의 ID를 받아야 할 경우, 라우트 매개변수를 정의할 수 있습니다:

```
Route::get('/user/{id}', function ($id) {
    return 'User '.$id;
});
```

필요한 만큼 여러 라우트 매개변수를 정의할 수 있습니다:

```
Route::get('/posts/{post}/comments/{comment}', function ($postId, $commentId) {
    //
});
```

라우트 매개변수는 항상 `{}` 중괄호로 감싸고, 이름은 알파벳 문자여야 하며, 언더스코어(`_`)도 허용됩니다. 매개변수는 라우트 콜백이나 컨트롤러에 순서대로 주입되며, 인수 이름과는 무관합니다.

<a name="parameters-and-dependency-injection"></a>
#### 매개변수와 의존성 주입

라우트 콜백에 Laravel 서비스 컨테이너가 자동 주입할 의존성이 있고, 라우트 매개변수가 모두 있을 경우, 의존성은 매개변수보다 먼저 나열해야 합니다:

```
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 매개변수 (Optional Parameters)

때로는 URI에 항상 나타나지 않는 매개변수를 지정해야 할 때가 있습니다. 이때는 매개변수 이름 뒤에 `?`를 붙여 선택적으로 만들 수 있습니다. 라우트의 변수에도 기본값을 지정하세요:

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

라우트 매개변수 형식을 제한하려면 라우트 인스턴스의 `where` 메서드를 사용합니다. 첫 인수는 매개변수명, 두 번째 인수는 정규 표현식입니다:

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

자주 쓰이는 정규식 패턴은 헬퍼 메서드로 쉽게 추가할 수 있습니다:

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
```

요청이 패턴에 맞지 않으면 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약 조건

항상 특정 정규식으로 제한하고 싶은 매개변수가 있으면 `pattern` 메서드를 사용할 수 있습니다. 이 설정은 `App\Providers\RouteServiceProvider`의 `boot` 메서드에서 정의하세요:

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

정의 후에는 해당 이름의 매개변수가 있는 모든 라우트에 자동 적용됩니다:

```
Route::get('/user/{id}', function ($id) {
    // {id}가 숫자인 경우에만 실행
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시 포함 (Encoded Forward Slashes)

기본적으로 Laravel 라우트 컴포넌트는 `/` 문자를 제외한 모든 문자만 매개변수 값으로 허용합니다. 경로 매개변수를 슬래시를 포함하도록 하려면 `where` 조건에 적절한 정규식을 명시해 허용해야 합니다:

```
Route::get('/search/{search}', function ($search) {
    return $search;
})->where('search', '.*');
```

> [!NOTE]
> 인코딩된 슬래시는 라우트 URI의 마지막 세그먼트에서만 지원됩니다.

<a name="named-routes"></a>
## 이름이 지정된 라우트 (Named Routes)

이름이 지정된 라우트는 특정 라우트를 위한 URL이나 리다이렉트를 편리하게 생성할 수 있게 해줍니다. 라우트 정의에 `name` 메서드를 체이닝하여 이름을 지정할 수 있습니다:

```
Route::get('/user/profile', function () {
    //
})->name('profile');
```

컨트롤러 액션에도 라우트 이름을 지정할 수 있습니다:

```
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!NOTE]
> 라우트 이름은 항상 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 이름이 지정된 라우트의 URL 생성

한 번 라우트에 이름을 지정하면, Laravel의 `route` 및 `redirect` 헬퍼 함수를 통해 URL이나 리다이렉트를 생성할 때 이름으로 참조할 수 있습니다:

```
// URL 생성...
$url = route('profile');

// 리다이렉트 생성...
return redirect()->route('profile');
```

라우트가 매개변수를 정의했다면 `route` 함수의 두 번째 인수로 매개변수를 전달할 수 있습니다. 전달받은 매개변수는 URL 내 알맞은 위치에 자동 삽입됩니다:

```
Route::get('/user/{id}/profile', function ($id) {
    //
})->name('profile');

$url = route('profile', ['id' => 1]);
```

매개변수 배열에 추가 값이 있으면, 해당 키-값 쌍은 자동으로 URL 쿼리 스트링에 추가됩니다:

```
Route::get('/user/{id}/profile', function ($id) {
    //
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// 결과: /user/1/profile?photos=yes
```

> [!TIP]
> 현재 로케일 등 요청 전체에 적용할 URL 매개변수 기본값을 지정하려면 [`URL::defaults` 메서드](/docs/{{version}}/urls#default-values)를 참고하세요.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 확인

현재 요청이 특정 이름이 지정된 라우트인지 확인하려면 Route 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어, 라우트 미들웨어에서 현재 라우트 이름을 확인할 수 있습니다:

```
/**
 * 들어오는 요청 처리
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

라우트 그룹은 미들웨어 같은 라우트 속성을 여러 라우트에 걸쳐 공유할 수 있게 해줍니다. 개별 라우트마다 반복해서 정의할 필요가 없습니다.

중첩된 그룹은 부모 그룹과 속성을 "합병"하려 시도합니다. 미들웨어와 `where` 조건은 병합되고, 이름과 접두사는 덧붙여집니다. 네임스페이스 구분자와 URI 접두사의 슬래시는 필요한 위치에 자동 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

그룹 내 모든 라우트에 [미들웨어](/docs/{{version}}/middleware)를 할당하려면 그룹 정의 전에 `middleware` 메서드를 사용할 수 있습니다. 미들웨어는 배열에 명시된 순서대로 실행됩니다:

```
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // first 및 second 미들웨어 사용
    });

    Route::get('/user/profile', function () {
        // first 및 second 미들웨어 사용
    });
});
```

<a name="route-group-controllers"></a>
### 컨트롤러

같은 [컨트롤러](/docs/{{version}}/controllers)를 사용하는 여러 라우트 그룹이 있다면, `controller` 메서드로 공통 컨트롤러를 정의할 수 있습니다. 라우트 정의 시엔 호출할 컨트롤러 메서드만 지정하면 됩니다:

```
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 서브도메인 라우팅

라우트 그룹은 서브도메인 라우팅에도 사용할 수 있습니다. 서브도메인도 라우트 URI 매개변수처럼 매개변수를 할당할 수 있어 하위 도메인 일부를 캡처해 라우트나 컨트롤러에서 사용할 수 있습니다. 서브도메인은 그룹 정의 전에 `domain` 메서드로 설정합니다:

```
Route::domain('{account}.example.com')->group(function () {
    Route::get('user/{id}', function ($account, $id) {
        //
    });
});
```

> [!NOTE]
> 서브도메인 라우트가 연결되도록 하려면 루트 도메인 라우트보다 먼저 서브도메인 라우트를 등록해야 합니다. 그래야 동일 URI 경로를 가진 루트 도메인 라우트가 서브도메인 라우트를 덮어쓰는 일을 방지할 수 있습니다.

<a name="route-group-prefixes"></a>
### 라우트 접두사

`prefix` 메서드는 그룹 내 모든 라우트 URI 앞에 지정한 URI를 붙입니다. 예를 들어 모든 라우트 URI 앞에 `admin`을 붙이려면 다음과 같이 합니다:

```
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // "/admin/users" URL과 일치
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두사

`name` 메서드는 그룹 내 모든 라우트 이름 앞에 지정한 문자열을 붙입니다. 예를 들어 그룹 내 모든 라우트 이름 앞에 `admin`을 붙이고 싶으면, 접두사에는 반드시 뒤에 `.` 문자를 포함하세요:

```
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // "admin.users" 라우트 이름이 할당됨
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

라우트나 컨트롤러 액션에 모델 ID를 주입할 때, 해당 ID에 맞는 모델을 데이터베이스에서 조회하는 일이 자주 발생합니다. Laravel 라우트 모델 바인딩은 모델 인스턴스를 자동으로 주입할 수 있게 해 이 작업을 편리하게 만듭니다. 예를 들어, 사용자 ID를 주입하는 대신, 해당 ID에 대응하는 `User` 모델 인스턴스를 바로 주입할 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩 (Implicit Binding)

Laravel은 라우트 또는 컨트롤러 액션의 타입 힌트 변수 이름과 URI 세그먼트 이름이 일치할 경우, 자동으로 Eloquent 모델을 해결해 주입합니다. 예를 들어:

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

여기서 `$user` 변수는 `App\Models\User` 모델이고, 변수명은 `{user}` URI 세그먼트와 일치하므로 Laravel은 요청 URI의 값과 일치하는 ID를 가진 모델 인스턴스를 자동으로 주입합니다. 만약 데이터베이스에서 일치하는 모델 인스턴스를 찾지 못하면 404 HTTP 응답이 자동으로 생성됩니다.

물론, 컨트롤러 메서드 사용 시에도 암묵적 바인딩이 가능합니다. 마찬가지로 URI 세그먼트 `{user}`와 컨트롤러의 `$user` 변수 이름이 같고 타입 힌트도 `App\Models\User`를 가집니다:

```
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

일반적으로 암묵적 바인딩은 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 다만, `withTrashed` 메서드를 체이닝하면 해당 모델도 주입할 수 있습니다:

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 기본 키 이름 커스터마이징

`id`가 아닌 다른 컬럼으로 모델을 조회하고 싶다면, 라우트 매개변수에 컬럼명을 명시할 수 있습니다:

```
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

또는 모델 클래스에 `getRouteKeyName` 메서드를 오버라이드하여, 항상 기본 키 대신 다른 컬럼을 사용하도록 할 수 있습니다:

```
/**
 * 라우트 키 이름 반환
 *
 * @return string
 */
public function getRouteKeyName()
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
#### 커스텀 키 & 스코핑(범위 지정)

한 라우트에서 여러 모델을 암묵적으로 바인딩할 때, 두 번째 모델을 첫 번째 모델의 자식으로 한정하는 스코프 바인딩을 할 수 있습니다. 예를 들어, 특정 사용자의 슬러그로 블로그 글을 조회하는 경우:

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

커스텀 키를 사용하는 중첩된 라우트 매개변수인 경우, Laravel은 부모 모델에서 관계 이름을 추측해 쿼리를 스코핑합니다. 이 경우 `User` 모델에 `posts`라는 관계(라우트 매개변수 복수형 이름)가 있다고 가정합니다.

만약, 커스텀 키 없이도 스코프 바인딩을 적용하고 싶으면, 라우트에 `scopeBindings` 메서드를 호출하세요:

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는 여러 라우트에 한 번에 적용하려면 그룹에도 적용할 수 있습니다:

```
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

<a name="customizing-missing-model-behavior"></a>
#### 누락된 모델 행동 커스터마이징

암묵적 바인딩 대상 모델이 없으면 보통 404 응답이 발생하지만, `missing` 메서드를 호출해 이를 커스터마이징할 수 있습니다. `missing` 메서드는 모델이 없을 때 실행할 클로저를 받습니다:

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

<a name="explicit-binding"></a>
### 명시적 바인딩 (Explicit Binding)

Laravel의 암묵적 바인딩만 사용할 필요 없이, 라우트 매개변수가 모델 클래스와 어떻게 연결되는지 명시적으로 정의할 수 있습니다. 명시적 바인딩은 라우터의 `model` 메서드를 사용해 매개변수와 클래스를 매핑합니다. 보통 `RouteServiceProvider`의 `boot` 메서드 맨 처음에 정의합니다:

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

이후 `{user}` 매개변수가 포함된 라우트를 정의하면:

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    //
});
```

모든 `{user}` 매개변수는 `App\Models\User` 모델 인스턴스를 주입받습니다. 예를 들어 `users/1` 요청은 ID가 1인 User를 조회해 주입합니다.

모델을 못 찾으면 기본적으로 404 응답을 반환합니다.

<a name="customizing-the-resolution-logic"></a>
#### 해석 로직 커스터마이징

커스텀 모델 바인딩 해석 로직이 필요하면 `Route::bind` 메서드를 사용할 수 있습니다. 클로저에는 URI 세그먼트 값이 전달되고, 해당 값에 맞는 모델 인스턴스를 반환해야 합니다. 이 설정 또한 `RouteServiceProvider`의 `boot` 메서드에서 합니다:

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

또는 Eloquent 모델에서 `resolveRouteBinding` 메서드를 오버라이드하여 직접 바인딩 로직을 정의할 수도 있습니다. 이 메서드는 URI 세그먼트 값과 필드명을 받고, 주입할 모델 인스턴스를 반환해야 합니다:

```
/**
 * 바인딩된 값에 대한 모델 조회
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

[암묵적 바인딩 스코핑](#implicit-model-binding-scoping)을 사용하는 경우, 부모 모델의 자식 바인딩 해석 시 `resolveChildRouteBinding` 메서드가 사용됩니다:

```
/**
 * 바인딩된 값에 대한 자식 모델 조회
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

`Route::fallback` 메서드를 사용하면, 들어오는 요청 중 등록된 라우트와 매칭되지 않는 경우 실행되는 라우트를 정의할 수 있습니다. 보통은 처리하지 않은 요청이 애플리케이션의 예외 처리기를 통해 "404" 페이지를 렌더링합니다. 하지만 `routes/web.php`에 폴백 라우트를 둔다면 `web` 미들웨어 그룹이 적용됩니다. 필요하면 추가 미들웨어도 붙일 수 있습니다:

```
Route::fallback(function () {
    //
});
```

> [!NOTE]
> 폴백 라우트는 항상 애플리케이션에서 가장 마지막에 등록해야 합니다.

<a name="rate-limiting"></a>
## 속도 제한 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 속도 제한기 정의

Laravel은 강력하면서 유연한 속도 제한 서비스를 제공하여, 특정 라우트나 라우트 그룹에 대해 트래픽을 제한할 수 있습니다. 시작하려면, 애플리케이션 요구에 맞는 속도 제한기 구성을 정의해야 하며, 보통은 `App\Providers\RouteServiceProvider` 클래스의 `configureRateLimiting` 메서드에서 처리합니다.

속도 제한기는 `RateLimiter` 퍼사드의 `for` 메서드로 정의합니다. `for` 메서드는 제한기 이름과 클로저를 인수로 받습니다. 클로저는 요청에 적용할 제한 구성을 반환해야 합니다. 제한 구성은 `Illuminate\Cache\RateLimiting\Limit` 클래스의 인스턴스로, 빠르게 제한을 정의할 수 있는 빌더 메서드를 제공합니다. 제한기 이름은 자유롭게 지정 가능합니다:

```
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 속도 제한기를 설정합니다.
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

만약 요청이 지정한 제한을 초과하면 Laravel이 자동으로 429 HTTP 상태 코드를 반환합니다. 직접 응답을 정의하려면 `response` 메서드를 사용합니다:

```
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function () {
        return response('Custom response...', 429);
    });
});
```

콜백은 들어오는 HTTP 요청 인스턴스를 받으므로, 요청이나 인증된 사용자에 따라 제한 조건을 동적으로 설정할 수 있습니다:

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
#### 제한 구간 분리

특정 값에 따라 제한을 구분하고 싶을 때가 있습니다. 예를 들어, IP 주소별로 분당 100번 접근을 허용하려면, 제한 정의 시 `by` 메서드를 사용합니다:

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100)->by($request->ip());
});
```

다른 예로, 로그인한 사용자는 사용자 ID별로 분당 100회, 게스트는 IP 주소별로 분당 10회 제한할 수도 있습니다:

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
                ? Limit::perMinute(100)->by($request->user()->id)
                : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 복수 제한

필요하면 하나의 제한기에서 여러 제한을 배열로 반환할 수 있습니다. 각 제한은 배열 순서대로 평가됩니다:

```
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### 라우트에 속도 제한기 적용

속도 제한기는 `throttle` [미들웨어](/docs/{{version}}/middleware)를 통해 라우트나 라우트 그룹에 붙일 수 있습니다. `throttle` 미들웨어에 제한기 이름을 인수로 넘겨 지정합니다:

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
#### Redis를 이용한 제한

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스로 매핑됩니다. 이 매핑은 애플리케이션의 HTTP 커널(`App\Http\Kernel`)에 정의되어 있습니다. 그러나 캐시 드라이버로 Redis를 사용하는 경우, Redis를 더 효율적으로 다루는 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 클래스로 매핑을 변경할 수 있습니다:

```
'throttle' => \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
```

<a name="form-method-spoofing"></a>
## 폼 메서드 스푸핑 (Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 메서드를 지원하지 않습니다. 따라서 폼에서 해당 HTTP 메서드를 호출하려면 `_method`라는 숨겨진 필드를 추가해야 합니다. 그 값이 요청 HTTP 메서드로 간주됩니다:

```
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

편의상, Blade의 `@method` [디렉티브](/docs/{{version}}/blade)로 생성할 수 있습니다:

```
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 접근 (Accessing The Current Route)

`Route` 퍼사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 이용해 현재 요청을 처리 중인 라우트 정보를 얻을 수 있습니다:

```
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route 인스턴스
$name = Route::currentRouteName(); // 문자열
$action = Route::currentRouteAction(); // 문자열
```

`Route` 퍼사드의 기본 클래스와 라우트 인스턴스의 API 문서를 참고하면 라우터와 라우트 클래스에서 제공하는 모든 메서드를 확인할 수 있습니다.

<a name="cors"></a>
## 교차 출처 리소스 공유(CORS)

Laravel은 구성한 값에 따라 CORS `OPTIONS` HTTP 요청에 자동 응답할 수 있습니다. 모든 CORS 설정은 애플리케이션 `config/cors.php` 구성 파일에서 조정할 수 있습니다. `OPTIONS` 요청은 글로벌 미들웨어 스택에 기본 포함된 `HandleCors` [미들웨어](/docs/{{version}}/middleware)가 자동으로 처리합니다. 글로벌 미들웨어 스택은 애플리케이션 HTTP 커널(`App\Http\Kernel`)에 위치합니다.

> [!TIP]
> CORS와 CORS 헤더에 관한 자세한 내용은 [MDN 웹 문서 CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

애플리케이션을 운영 환경에 배포할 때는 Laravel의 라우트 캐시를 활용해야 합니다. 라우트 캐시는 모든 라우트 등록 속도를 대폭 감소시킵니다. 캐시를 생성하려면 Artisan의 `route:cache` 명령어를 실행하세요:

```
php artisan route:cache
```

이 명령어 실행 후, 캐시된 라우트 파일이 모든 요청마다 로드됩니다. 새 라우트를 추가할 때마다 캐시를 새로 생성해야 하므로, 이 명령어는 배포 시에만 실행하는 것이 좋습니다.

라우트 캐시는 `route:clear` 명령어로 삭제할 수 있습니다:

```
php artisan route:clear
```