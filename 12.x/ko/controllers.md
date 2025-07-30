# 컨트롤러 (Controllers)

- [소개](#introduction)
- [컨트롤러 작성하기](#writing-controllers)
    - [기본 컨트롤러](#basic-controllers)
    - [단일 액션 컨트롤러](#single-action-controllers)
- [컨트롤러 미들웨어](#controller-middleware)
- [리소스 컨트롤러](#resource-controllers)
    - [부분 리소스 라우트](#restful-partial-resource-routes)
    - [중첩 리소스](#restful-nested-resources)
    - [리소스 라우트 이름 지정](#restful-naming-resource-routes)
    - [리소스 라우트 파라미터 이름 지정](#restful-naming-resource-route-parameters)
    - [리소스 라우트 범위 지정](#restful-scoping-resource-routes)
    - [리소스 URI 로컬라이징](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 확장](#restful-supplementing-resource-controllers)
    - [싱글턴 리소스 컨트롤러](#singleton-resource-controllers)
    - [미들웨어와 리소스 컨트롤러](#middleware-and-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개

모든 요청 처리 로직을 라우트 파일에서 클로저로만 정의하는 대신, "컨트롤러" 클래스를 사용하여 이러한 동작을 정리하여 관리할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 한 클래스에 모아둘 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 보여주기, 생성, 수정, 삭제 등 모든 요청을 다룰 수 있습니다. 기본적으로 컨트롤러 클래스는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기

<a name="basic-controllers"></a>
### 기본 컨트롤러

새로운 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 사용할 수 있습니다. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉터리에 위치합니다.

```shell
php artisan make:controller UserController
```

기본 컨트롤러의 예시를 살펴보겠습니다. 컨트롤러에는 들어오는 HTTP 요청을 처리할 각종 public 메서드를 자유롭게 정의할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 표시합니다.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

컨트롤러 클래스와 메서드를 작성한 후에는 아래와 같이 해당 컨트롤러 메서드로 연결되는 라우트를 정의할 수 있습니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

요청이 위 라우트 URI와 일치하는 경우, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되며, 라우트 파라미터가 해당 메서드에 전달됩니다.

> [!NOTE]
> 컨트롤러가 반드시 어떤 기본 클래스를 상속받아야 하는 것은 아닙니다. 하지만 여러 컨트롤러에서 공통적으로 사용해야 할 메서드가 있다면, 기본 컨트롤러 클래스를 상속받아 이를 공유하는 것도 편리할 수 있습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러

컨트롤러 액션이 특히 복잡할 경우, 해당 액션만을 위한 전용 컨트롤러 클래스를 두는 것이 좋을 때가 있습니다. 이런 경우, 컨트롤러 내에 오직 하나의 `__invoke` 메서드만을 정의하면 됩니다.

```php
<?php

namespace App\Http\Controllers;

class ProvisionServer extends Controller
{
    /**
     * 새로운 웹 서버를 프로비저닝(provision)합니다.
     */
    public function __invoke()
    {
        // ...
    }
}
```

단일 액션 컨트롤러를 라우트에 등록할 때는 컨트롤러 메서드를 명시할 필요 없이, 컨트롤러 이름만 라우터에 전달하면 됩니다.

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` Artisan 명령어에 `--invokable` 옵션을 사용하면 호출 가능한(invokable) 컨트롤러를 쉽게 생성할 수 있습니다.

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁(stub) 파일은 [스텁 게시](/docs/12.x/artisan#stub-customization) 기능을 통해 커스터마이즈할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

[미들웨어](/docs/12.x/middleware)는 각 컨트롤러의 라우트에 라우트 파일에서 지정할 수 있습니다.

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

또는 컨트롤러 클래스 내부에서 미들웨어를 지정하는 것이 더 편리할 수도 있습니다. 이 경우 컨트롤러는 `HasMiddleware` 인터페이스를 구현해야 하며, 해당 인터페이스는 컨트롤러에 static `middleware` 메서드가 있어야 한다는 것을 의미합니다. 이 메서드에서 컨트롤러의 액션에 적용할 미들웨어 배열을 반환할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

class UserController extends Controller implements HasMiddleware
{
    /**
     * 이 컨트롤러에 할당할 미들웨어를 반환합니다.
     */
    public static function middleware(): array
    {
        return [
            'auth',
            new Middleware('log', only: ['index']),
            new Middleware('subscribed', except: ['store']),
        ];
    }

    // ...
}
```

컨트롤러 미들웨어를 클로저(익명 함수)로 정의하는 것도 가능합니다. 이렇게 하면 별도의 미들웨어 클래스를 작성하지 않고도 인라인 방식으로 미들웨어를 추가할 수 있어 편리합니다.

```php
use Closure;
use Illuminate\Http\Request;

/**
 * 이 컨트롤러에 할당할 미들웨어를 반환합니다.
 */
public static function middleware(): array
{
    return [
        function (Request $request, Closure $next) {
            return $next($request);
        },
    ];
}
```

<a name="resource-controllers"></a>
## 리소스 컨트롤러

애플리케이션의 각 Eloquent 모델을 "리소스"라고 생각하면, 일반적으로 각 리소스에 대해 동일한 작업(생성, 조회, 수정, 삭제 등)을 수행하게 됩니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다면 사용자는 이 리소스들에 대해 생성, 조회, 수정, 삭제 작업을 할 수 있을 것입니다.

이처럼 흔히 반복되는 작업을 위해, 라라벨의 리소스 라우팅은 일반적인 생성, 조회, 수정, 삭제("CRUD") 라우트를 한 줄의 코드로 컨트롤러에 할당할 수 있도록 합니다. 시작하려면 `make:controller` Artisan 명령어의 `--resource` 옵션으로 이러한 작업을 처리할 컨트롤러를 빠르게 생성할 수 있습니다.

```shell
php artisan make:controller PhotoController --resource
```

이 명령어는 `app/Http/Controllers/PhotoController.php` 위치에 컨트롤러를 생성합니다. 그리고 이 컨트롤러에는 각 리소스 작업에 해당하는 메서드가 준비되어 있습니다. 다음으로, 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

위처럼 하나의 라우트 선언만으로 리소스의 다양한 액션을 처리하는 여러 라우트가 자동으로 생성됩니다. 생성된 컨트롤러에는 이미 각각의 액션에 대한 스턱(stub) 메서드가 포함되어 있습니다. 참고로, `route:list` Artisan 명령어를 실행하면 애플리케이션에 등록된 모든 라우트들을 빠르게 확인할 수 있습니다.

여러 개의 리소스 컨트롤러를 동시에 등록하려면 `resources` 메서드에 배열을 전달하면 됩니다.

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`softDeletableResources` 메서드는 여러 리소스 컨트롤러를 등록하면서 모두 `withTrashed` 기능을 사용할 수 있습니다.

```php
Route::softDeletableResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션

<div class="overflow-auto">

| HTTP 메서드 | URI                           | 액션    | 라우트 이름         |
| ----------- | ---------------------------- | ------- | ------------------- |
| GET         | `/photos`                    | index   | photos.index        |
| GET         | `/photos/create`             | create  | photos.create       |
| POST        | `/photos`                    | store   | photos.store        |
| GET         | `/photos/{photo}`            | show    | photos.show         |
| GET         | `/photos/{photo}/edit`       | edit    | photos.edit         |
| PUT/PATCH   | `/photos/{photo}`            | update  | photos.update       |
| DELETE      | `/photos/{photo}`            | destroy | photos.destroy      |

</div>

<a name="customizing-missing-model-behavior"></a>
#### 모델이 없을 때의 동작 커스터마이징

일반적으로 암묵적 모델 바인딩(implicit model binding)에서 리소스 모델을 찾지 못하면, 404 HTTP 응답이 반환됩니다. 그러나, 리소스 라우트 정의 시 `missing` 메서드를 호출하면 이 동작을 원하는 대로 커스터마이징할 수 있습니다. `missing` 메서드는 해당 리소스의 어떤 라우트든 암묵적으로 바인딩된 모델을 찾지 못했을 때 실행되는 클로저를 인자로 받습니다.

```php
use App\Http\Controllers\PhotoController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::resource('photos', PhotoController::class)
    ->missing(function (Request $request) {
        return Redirect::route('photos.index');
    });
```

<a name="soft-deleted-models"></a>
#### 소프트 삭제된 모델

일반적으로 암묵적 모델 바인딩은 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)된 모델을 조회하지 않고, 대신 404 HTTP 응답을 반환합니다. 그러나 리소스 라우트 정의 시 `withTrashed` 메서드를 호출하면 소프트 삭제된(휴지통에 있는) 모델도 조회하도록 할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

`withTrashed`에 인자를 전달하지 않으면, `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델도 허용됩니다. 특정 라우트만 허용하려면, 라우트 이름 배열을 전달할 수 있습니다.

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정하기

[라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 사용 중이고, 리소스 컨트롤러의 메서드에서 모델 인스턴스를 타입 힌트로 받으려면 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### Form Request 생성

리소스 컨트롤러를 생성할 때 `--requests` 옵션을 추가하면, 해당 컨트롤러의 저장(store) 및 업데이트(update) 메서드에 필요한 [form request 클래스](/docs/12.x/validation#form-request-validation)도 Artisan이 자동 생성합니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트를 선언할 때 모든 기본 액션을 처리하는 대신, 일부 액션만 처리하도록 지정할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->only([
    'index', 'show'
]);

Route::resource('photos', PhotoController::class)->except([
    'create', 'store', 'update', 'destroy'
]);
```

<a name="api-resource-routes"></a>
#### API 리소스 라우트

API에서 사용되는 리소스 라우트에는 보통 HTML 템플릿을 반환하는 `create`, `edit` 라우트가 필요하지 않습니다. 이러한 경우, `apiResource` 메서드를 사용하면 이 두 라우트가 자동으로 제외됩니다.

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

여러 개의 API 리소스 컨트롤러를 동시에 등록하려면 `apiResources` 메서드에 배열로 전달할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`make:controller` 명령어에서 `--api` 옵션을 사용하면 `create`, `edit` 메서드가 포함되지 않은 API 전용 리소스 컨트롤러를 빠르게 생성할 수 있습니다.

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스

때로는 중첩된 리소스에 대한 라우트를 정의해야 할 때가 있습니다. 예를 들어, 한 사진(photo) 리소스가 여러 개의 댓글(comment)을 가질 수 있습니다. 이런 경우, 라우트 선언에서 "도트(dot) 표기법"을 사용해 리소스 컨트롤러를 중첩할 수 있습니다.

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 형태의 URI를 제공하는 중첩 리소스를 등록합니다.

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스의 범위 지정

라라벨의 [암묵적 모델 바인딩](/docs/12.x/routing#implicit-model-binding-scoping) 기능은 중첩된 바인딩에서도 자식 모델이 부모 모델에 속하는지 자동으로 확인할 수 있습니다. 중첩 리소스 정의 시 `scoped` 메서드를 사용하면 자동 범위 지정과, 자식 리소스를 어떤 필드로 조회할지 설정할 수 있습니다. 자세한 방법은 [리소스 라우트 범위 지정](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 얕은 중첩(Shallow Nesting)

자식 ID가 이미 고유 식별자인 경우, URI에 부모와 자식 ID를 모두 포함시킬 필요가 없는 상황이 많습니다. 모델을 URI 세그먼트에서 자동증가 PK 등 고유 값으로 구분하는 경우, "얕은 중첩(shallow nesting)"을 사용할 수 있습니다.

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

이렇게 정의하면 다음과 같이 라우트가 생성됩니다.

<div class="overflow-auto">

| HTTP 메서드 | URI                                    | 액션    | 라우트 이름                |
| ----------- | -------------------------------------- | ------- | -------------------------- |
| GET         | `/photos/{photo}/comments`             | index   | photos.comments.index      |
| GET         | `/photos/{photo}/comments/create`      | create  | photos.comments.create     |
| POST        | `/photos/{photo}/comments`             | store   | photos.comments.store      |
| GET         | `/comments/{comment}`                  | show    | comments.show              |
| GET         | `/comments/{comment}/edit`             | edit    | comments.edit              |
| PUT/PATCH   | `/comments/{comment}`                  | update  | comments.update            |
| DELETE      | `/comments/{comment}`                  | destroy | comments.destroy           |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정

기본적으로 모든 리소스 컨트롤러 액션에는 라우트 이름이 자동으로 할당됩니다. 그러나, 원하는 라우트 이름으로 직접 오버라이드할 수도 있습니다. 이때 `names` 배열을 전달하면 됩니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정

기본적으로 `Route::resource`는 리소스 이름의 "단수" 버전을 사용해 라우트 파라미터를 생성합니다. 필요하다면 `parameters` 메서드로 라우트별 파라미터 이름을 자유롭게 지정할 수 있습니다. 이때 전달하는 배열은 리소스 이름과 파라미터 이름의 쌍으로 이루어진 연관 배열이어야 합니다.

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예시의 경우, 해당 리소스의 `show` 라우트에 사용되는 URI는 아래와 같이 생성됩니다.

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 범위 지정

라라벨의 [스코프 암묵적 모델 바인딩](/docs/12.x/routing#implicit-model-binding-scoping) 기능을 사용하면, 중첩된 바인딩에서도 자식 모델이 반드시 부모 모델에 속하도록 자동으로 쿼리 범위를 제한할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면, 자동 스코핑과 더불어 자식 리소스를 어떤 필드로 찾을지 지정할 수 있습니다.

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

위와 같이 라우트를 정의하면 다음과 같이 스코프가 적용된 URI를 사용할 수 있습니다.

```text
/photos/{photo}/comments/{comment:slug}
```

커스텀 키 암묵적 바인딩을 중첩된 라우트 파라미터로 사용할 때, 라라벨은 자동으로 부모를 기준으로 자식 모델을 조회하는 쿼리 범위를 설정합니다. 예를 들어 이 경우에는 `Photo` 모델에 `comments`라는(`comments`는 라우트 파라미터의 복수형) 관계가 있다고 가정하여 `Comment` 모델을 조회합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 로컬라이징

`Route::resource`는 기본적으로 리소스 URI를 영어 동사와 복수 규칙으로 생성합니다. 만약 `create` 및 `edit`와 같은 액션 동사를 로컬라이즈해야 한다면, `Route::resourceVerbs` 메서드를 사용할 수 있습니다. 이 설정은 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider`에서 `boot` 메서드 초기에 수행합니다.

```php
/**
 * 애플리케이션 서비스 부팅시.
 */
public function boot(): void
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);
}
```

라라벨의 복수형 변환 기능은 [여러 언어를 지원](/docs/12.x/localization#pluralization-language)하며, 필요에 따라 원하는 언어로 설정할 수 있습니다. 이렇게 동사와 복수 규칙을 변경하면, 예를 들어 `Route::resource('publicacion', PublicacionController::class)`을 등록했을 때 아래와 같은 URI가 생성됩니다.

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 확장

리소스 컨트롤러에 기본 리소스 라우트 외의 추가 라우트가 필요하다면, `Route::resource` 메서드보다 **먼저** 해당 라우트를 정의해야 합니다. 그렇지 않으면 `resource` 메서드가 생성한 라우트가 추가 라우트보다 우선순위를 갖게 되어, 원치 않는 동작이 발생할 수 있습니다.

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러는 특정 목적에 집중해서 작성하세요. 리소스 컨트롤러의 기본 액션 세트 외에 추가 메서드가 자꾸 필요하다면, 컨트롤러를 둘로 나누어 더 작게 구성하는 것이 좋습니다.

<a name="singleton-resource-controllers"></a>
### 싱글턴 리소스 컨트롤러

애플리케이션에서 리소스가 하나의 인스턴스만 가질 수 있는 경우가 있습니다. 예를 들어, 사용자 "프로필"은 수정이나 업데이트만 가능하고, 사용자가 여러 개의 "프로필"을 가질 수는 없습니다. 마찬가지로, 이미지에 "썸네일"이 하나만 있을 때도 있습니다. 이런 리소스를 "싱글턴 리소스(singleton resource)"라고 부르며, 하나의 리소스 인스턴스만 존재할 수 있음을 의미합니다. 이런 경우 싱글턴 리소스 컨트롤러를 등록할 수 있습니다.

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위 싱글턴 리소스 정의는 다음 라우트를 등록합니다. 보시다시피, "생성(create)" 라우트는 등록되지 않으며, 오직 한 개의 리소스만 존재하므로 식별자를 필요로 하지 않습니다.

<div class="overflow-auto">

| HTTP 메서드 | URI                | 액션   | 라우트 이름         |
| ----------- | ------------------ | ------ | ------------------- |
| GET         | `/profile`         | show   | profile.show        |
| GET         | `/profile/edit`    | edit   | profile.edit        |
| PUT/PATCH   | `/profile`         | update | profile.update      |

</div>

싱글턴 리소스는 일반 리소스 내에 중첩해서 등록할 수도 있습니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 예시에서, `photos` 리소스는 [표준 리소스 라우트](#actions-handled-by-resource-controllers)를 모두 가지게 되지만, `thumbnail` 리소스는 싱글턴 리소스로 아래와 같은 라우트만 등록됩니다.

<div class="overflow-auto">

| HTTP 메서드 | URI                               | 액션   | 라우트 이름               |
| ----------- | --------------------------------- | ------ | ------------------------- |
| GET         | `/photos/{photo}/thumbnail`       | show   | photos.thumbnail.show     |
| GET         | `/photos/{photo}/thumbnail/edit`  | edit   | photos.thumbnail.edit     |
| PUT/PATCH   | `/photos/{photo}/thumbnail`       | update | photos.thumbnail.update   |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글턴 리소스

필요에 따라, 싱글턴 리소스에도 생성(create) 및 저장(store) 라우트를 정의하고 싶을 수 있습니다. 이럴 때는 싱글턴 리소스 등록 시 `creatable` 메서드를 호출하면 됩니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이렇게 하면 다음과 같은 라우트가 등록됩니다. 참고로 생성 가능한 싱글턴 리소스에는 `DELETE` 라우트도 추가됩니다.

<div class="overflow-auto">

| HTTP 메서드 | URI                                     | 액션    | 라우트 이름               |
| ----------- | --------------------------------------- | ------- | ------------------------- |
| GET         | `/photos/{photo}/thumbnail/create`      | create  | photos.thumbnail.create   |
| POST        | `/photos/{photo}/thumbnail`             | store   | photos.thumbnail.store    |
| GET         | `/photos/{photo}/thumbnail`             | show    | photos.thumbnail.show     |
| GET         | `/photos/{photo}/thumbnail/edit`        | edit    | photos.thumbnail.edit     |
| PUT/PATCH   | `/photos/{photo}/thumbnail`             | update  | photos.thumbnail.update   |
| DELETE      | `/photos/{photo}/thumbnail`             | destroy | photos.thumbnail.destroy  |

</div>

만약 싱글턴 리소스에 대해 `DELETE` 라우트만 등록하고, 생성(create), 저장(store) 라우트는 제외하고 싶다면, `destroyable` 메서드를 사용할 수 있습니다.

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글턴 리소스

`apiSingleton` 메서드를 사용하여, `create` 및 `edit` 라우트가 필요 없는 API용 싱글턴 리소스를 등록할 수 있습니다.

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론 API 싱글턴 리소스를 `creatable` 상태로 만들면, 해당 리소스에 대한 `store` 및 `destroy` 라우트도 함께 등록됩니다.

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```
<a name="middleware-and-resource-controllers"></a>
### 미들웨어와 리소스 컨트롤러

라라벨에서는 `middleware`, `middlewareFor`, `withoutMiddlewareFor` 메서드를 활용해, 리소스 라우트의 모든 메서드 또는 특정 메서드별로 미들웨어를 지정할 수 있습니다. 이들 메서드를 사용해 리소스 액션별로 미들웨어 적용 대상을 세밀하게 제어할 수 있습니다.

#### 모든 메서드에 미들웨어 적용하기

`middleware` 메서드를 이용하면 리소스 또는 싱글턴 리소스 라우트에서 생성되는 모든 라우트에 미들웨어를 적용할 수 있습니다.

```php
Route::resource('users', UserController::class)
    ->middleware(['auth', 'verified']);

Route::singleton('profile', ProfileController::class)
    ->middleware('auth');
```

#### 특정 메서드에만 미들웨어 적용하기

`middlewareFor` 메서드를 사용하면, 지정한 리소스 액션에만 미들웨어를 적용할 수 있습니다.

```php
Route::resource('users', UserController::class)
    ->middlewareFor('show', 'auth');

Route::apiResource('users', UserController::class)
    ->middlewareFor(['show', 'update'], 'auth');

Route::resource('users', UserController::class)
    ->middlewareFor('show', 'auth')
    ->middlewareFor('update', 'auth');

Route::apiResource('users', UserController::class)
    ->middlewareFor(['show', 'update'], ['auth', 'verified']);
```

`middlewareFor` 메서드는 싱글턴 및 API 싱글턴 리소스 컨트롤러에도 사용할 수 있습니다.

```php
Route::singleton('profile', ProfileController::class)
    ->middlewareFor('show', 'auth');

Route::apiSingleton('profile', ProfileController::class)
    ->middlewareFor(['show', 'update'], 'auth');
```

#### 특정 메서드에서 미들웨어 제외하기

`withoutMiddlewareFor` 메서드를 이용하면, 특정 리소스 액션에서만 미들웨어를 제외할 수 있습니다.

```php
Route::middleware(['auth', 'verified', 'subscribed'])->group(function () {
    Route::resource('users', UserController::class)
        ->withoutMiddlewareFor('index', ['auth', 'verified'])
        ->withoutMiddlewareFor(['create', 'store'], 'verified')
        ->withoutMiddlewareFor('destroy', 'subscribed');
});
```

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러

<a name="constructor-injection"></a>
#### 생성자 주입(Constructor Injection)

라라벨에서는 모든 컨트롤러를 [서비스 컨테이너](/docs/12.x/container)가 자동으로 해결(resolve)합니다. 따라서, 컨트롤러의 생성자에 필요한 의존성을 타입 힌트로 선언하면, 서비스 컨테이너가 해당 의존성을 자동으로 주입해줍니다.

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스를 생성합니다.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}
}
```

<a name="method-injection"></a>
#### 메서드 주입(Method Injection)

생성자 주입 외에도, 컨트롤러의 메서드에서 직접 의존성을 타입 힌트로 지정할 수도 있습니다. 대표적인 예로, `Illuminate\Http\Request` 인스턴스를 메서드 파라미터로 받아오는 경우가 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새로운 사용자를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->name;

        // 사용자 저장...

        return redirect('/users');
    }
}
```

컨트롤러 메서드에서 라우트 파라미터도 함께 받을 경우, 의존성 인자 다음에 라우트 인수를 나란히 작성하면 됩니다. 즉, 라우트가 다음과 같이 정의되어 있다면,

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메서드는 아래와 같이 타입 힌트와 라우트 파라미터를 함께 받을 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 주어진 사용자를 업데이트합니다.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 업데이트...

        return redirect('/users');
    }
}
```
