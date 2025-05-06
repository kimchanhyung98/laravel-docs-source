# 컨트롤러

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
    - [리소스 라우트 스코프 지정](#restful-scoping-resource-routes)
    - [리소스 URI 현지화](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 보완](#restful-supplementing-resource-controllers)
    - [싱글턴 리소스 컨트롤러](#singleton-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개

모든 요청 처리 로직을 라우트 파일의 클로저로 정의하는 대신, "컨트롤러" 클래스를 사용해 이 동작을 체계적으로 관리할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스로 그룹화할 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청(조회, 생성, 수정, 삭제 등)을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기

<a name="basic-controllers"></a>
### 기본 컨트롤러

새 컨트롤러를 빠르게 생성하려면 `make:controller` 아티즌 명령을 사용할 수 있습니다. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다:

```shell
php artisan make:controller UserController
```

기본 컨트롤러 예제를 살펴보겠습니다. 컨트롤러는 요청을 처리할 공개 메서드를 여러 개 가질 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 지정한 사용자의 프로필을 보여줍니다.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

컨트롤러 클래스와 메서드를 작성한 후, 다음과 같이 해당 컨트롤러 메서드로 가는 라우트를 정의할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

요청이 지정된 라우트 URI와 일치할 때, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고, 라우트 파라미터가 해당 메서드로 전달됩니다.

> [!NOTE]
> 컨트롤러가 반드시 **기반 클래스**를 확장해야 하는 것은 아닙니다. 하지만 모든 컨트롤러에서 공유해야 할 메서드가 포함된 기본 컨트롤러 클래스를 확장하면 때로는 편리할 수 있습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러

컨트롤러 액션이 특히 복잡한 경우, 하나의 액션만을 담당하는 컨트롤러 클래스를 따로 두는 것이 편리할 수 있습니다. 이를 위해 컨트롤러 내에 단일 `__invoke` 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

class ProvisionServer extends Controller
{
    /**
     * 새 웹 서버를 프로비전합니다.
     */
    public function __invoke()
    {
        // ...
    }
}
```

단일 액션 컨트롤러에 라우트를 등록할 때는 별도의 컨트롤러 메서드를 지정할 필요 없이 컨트롤러 이름만 라우터에 전달하면 됩니다:

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` 아티즌 명령의 `--invokable` 옵션을 사용해 인보커블(호출 가능한) 컨트롤러를 생성할 수 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁은 [스텁 게시](/docs/{{version}}/artisan#stub-customization)를 사용해 커스터마이징할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

[미들웨어](/docs/{{version}}/middleware)는 라우트 파일의 컨트롤러 라우트에 할당할 수 있습니다:

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

또는, 컨트롤러 클래스 내에서 미들웨어를 지정하는 것이 편리할 수 있습니다. 이 경우, 컨트롤러는 `HasMiddleware` 인터페이스를 구현해야 하며, 이 인터페이스는 컨트롤러에 정적 `middleware` 메서드가 있어야 함을 명시합니다. 이 메서드에서 컨트롤러의 액션에 적용될 미들웨어 배열을 반환할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

class UserController extends Controller implements HasMiddleware
{
    /**
     * 컨트롤러에 할당할 미들웨어를 반환합니다.
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

클로저로 컨트롤러 미들웨어를 정의해 인라인 방식으로 작성할 수도 있습니다. 이는 전체 미들웨어 클래스를 작성하지 않고도 간편하게 사용할 수 있습니다:

```php
use Closure;
use Illuminate\Http\Request;

/**
 * 컨트롤러에 할당할 미들웨어를 반환합니다.
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

> [!WARNING]
> `Illuminate\Routing\Controllers\HasMiddleware`를 구현하는 컨트롤러는 `Illuminate\Routing\Controller`를 확장하면 안 됩니다.

<a name="resource-controllers"></a>
## 리소스 컨트롤러

애플리케이션 내의 각 Eloquent 모델을 "리소스"로 생각할 수 있으며, 일반적으로 각 리소스에 대해 동일한 일련의 작업을 수행합니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다면, 사용자는 이 리소스를 생성, 조회, 수정, 삭제(CRUD)할 수 있을 것입니다.

이러한 일반적인 사용 사례를 위해, 라라벨의 리소스 라우팅은 일반적인 생성, 조회, 수정, 삭제(CRUD) 라우트를 한 번에 컨트롤러에 할당합니다. 다음과 같이 `make:controller` 아티즌 명령에서 `--resource` 옵션을 사용해 이런 작업을 처리할 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

이 명령은 `app/Http/Controllers/PhotoController.php` 경로에 컨트롤러를 생성합니다. 이 컨트롤러에는 각각의 리소스 작업에 해당하는 메서드가 포함됩니다. 다음으로, 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 한 줄의 라우트 선언으로 리소스에 대한 다양한 작업을 처리할 여러 라우트가 생성됩니다. 생성된 컨트롤러에는 각 작업에 대한 스텁 메서드가 이미 포함되어 있습니다. 애플리케이션의 라우트 개요는 `route:list` 아티즌 명령으로 빠르게 확인할 수 있습니다.

배열을 이용해 한 번에 여러 리소스 컨트롤러를 등록할 수도 있습니다:

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션

<div class="overflow-auto">

| HTTP 메서드 | URI                        | 액션    | 라우트 이름       |
| ----------- | -------------------------- | ------- | ----------------- |
| GET         | `/photos`                  | index   | photos.index      |
| GET         | `/photos/create`           | create  | photos.create     |
| POST        | `/photos`                  | store   | photos.store      |
| GET         | `/photos/{photo}`          | show    | photos.show       |
| GET         | `/photos/{photo}/edit`     | edit    | photos.edit       |
| PUT/PATCH   | `/photos/{photo}`          | update  | photos.update     |
| DELETE      | `/photos/{photo}`          | destroy | photos.destroy    |

</div>

<a name="customizing-missing-model-behavior"></a>
#### 모델이 없을 때 동작 커스터마이즈

암시적 모델 바인딩에서 없는 리소스 모델이 요청되면, 기본적으로 404 HTTP 응답이 반환됩니다. 하지만 `missing` 메서드를 사용해 이 동작을 커스터마이즈할 수 있습니다. `missing` 메서드는 바인딩된 모델을 찾을 수 없을 때 호출되는 클로저를 받습니다:

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
#### 소프트 삭제 모델

암시적 모델 바인딩은 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)된 모델을 기본적으로 조회하지 않으며, 대신 404 HTTP 응답을 반환합니다. 하지만 `withTrashed` 메서드를 사용하면 소프트 삭제 모델도 허용할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

인자를 전달하지 않으면, `show`, `edit`, `update` 리소스 라우트에 한해 소프트 삭제 모델이 허용됩니다. 특정 라우트에만 허용하려면 배열을 인자로 전달하세요:

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정

[라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 사용할 때, 리소스 컨트롤러의 메서드에 모델 인스턴스를 타입힌트 하고 싶다면, 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 리퀘스트 생성

리소스 컨트롤러를 생성할 때 `--requests` 옵션을 제공하면, 아티즌이 [폼 리퀘스트 클래스](/docs/{{version}}/validation#form-request-validation)를 저장 및 갱신 메서드용으로 자동 생성합니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트를 선언할 때, 컨트롤러가 처리해야 할 액션 중 일부만 선택할 수 있습니다:

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

API에서 사용될 리소스 라우트를 선언할 때, 일반적으로 HTML 템플릿을 렌더링하는 `create`, `edit` 라우트는 제외합니다. 이를 위해 `apiResource` 메서드를 사용하면 두 라우트가 자동으로 제외됩니다:

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

배열을 이용해 여러 API 리소스 컨트롤러를 한 번에 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`make:controller` 명령에 `--api` 스위치를 사용하면, `create`, `edit` 메서드가 포함되지 않은 API 리소스 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스

경우에 따라 중첩 리소스에 대한 라우트를 정의해야 할 수 있습니다. 예를 들어, 하나의 사진(포토)에 여러 개의 댓글이 연결될 수 있습니다. 중첩 리소스 컨트롤러는 라우트 선언에서 점(`.`) 표기법을 사용해 정의할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 URI로 접근할 수 있는 중첩 리소스를 등록합니다:

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 스코프 지정

라라벨의 [암시적 모델 바인딩 스코프](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능은 중첩 바인딩에서 자식 모델이 부모 모델에 속하는지 자동으로 확인합니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 스코프 지정이 가능하고, 자식 리소스를 어떤 필드로 조회할지도 지정할 수 있습니다. 자세한 방법은 [리소스 라우트 스코프 지정](#restful-scoping-resource-routes) 문서에서 확인하세요.

<a name="shallow-nesting"></a>
#### 얕은 중첩(Shallow Nesting)

자식 ID가 이미 고유 식별자인 경우, URI에 부모와 자식 ID를 모두 포함할 필요가 없는 경우가 많습니다. URI 세그먼트에서 오토 인크리먼트 프라이머리 키 등 고유 식별자를 사용할 때는 "얕은 중첩(shallow nesting)"을 선택할 수 있습니다:

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

이 라우트 정의는 다음과 같은 라우트를 추가합니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                                  | 액션    | 라우트 이름               |
| ----------- | ------------------------------------ | ------- | ------------------------- |
| GET         | `/photos/{photo}/comments`           | index   | photos.comments.index     |
| GET         | `/photos/{photo}/comments/create`    | create  | photos.comments.create    |
| POST        | `/photos/{photo}/comments`           | store   | photos.comments.store     |
| GET         | `/comments/{comment}`                | show    | comments.show             |
| GET         | `/comments/{comment}/edit`           | edit    | comments.edit             |
| PUT/PATCH   | `/comments/{comment}`                | update  | comments.update           |
| DELETE      | `/comments/{comment}`                | destroy | comments.destroy          |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정

모든 리소스 컨트롤러 액션에는 기본적으로 라우트 이름이 지정됩니다. 하지만 원하는 라우트 이름으로 덮어쓸 수 있습니다. `names` 배열을 전달하세요:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정

`Route::resource`는 기본적으로 리소스 이름의 단수형을 사용해 파라미터명을 만듭니다. 하지만 `parameters` 메서드를 사용해 개별 리소스별로 쉽게 오버라이드할 수 있습니다. `parameters`에 전달되는 배열은 리소스 이름과 파라미터명을 키–값 쌍으로 지정합니다:

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예제는 `show` 라우트에 대해 다음과 같은 URI를 생성합니다:

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코프 지정

라라벨의 [스코프 암시적 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능은 중첩 바인딩에서 자식 모델이 반드시 부모 모델에 속하는지 자동으로 확인합니다. 중첩 리소스 정의 시 `scoped` 메서드를 사용하면 자동 스코프 적용과 자식 리소스의 조회 필드를 지정할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 다음과 같은 URI를 등록합니다:

```text
/photos/{photo}/comments/{comment:slug}
```

커스텀 키 암시적 바인딩을 중첩 라우트 파라미터로 사용할 때, 라라벨은 부모를 참조해 자식 모델을 쿼리하도록 자동으로 스코프를 적용합니다. 이런 경우 `Photo` 모델에 `comments`(즉, 파라미터명 복수형)라는 관계가 있다고 간주합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화

`Route::resource`는 기본적으로 영어의 동사 및 복수 규칙을 사용해 리소스 URI를 생성합니다. `create`와 `edit` 액션 동사를 현지화하려면 `Route::resourceVerbs` 메서드를 사용할 수 있습니다. 이는 애플리케이션의 `App\Providers\AppServiceProvider` 내 `boot` 메서드에서 설정할 수 있습니다:

```php
/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);
}
```

라라벨의 복수화(pluralizer)는 [여러 언어를 지원하므로 필요에 따라 설정할 수 있습니다](/docs/{{version}}/localization#pluralization-language). 동사와 복수 규칙을 커스터마이즈하면, 예를 들어 `Route::resource('publicacion', PublicacionController::class)` 등록 시 다음과 같은 URI가 생성됩니다:

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보완

기본 리소스 라우트 외에 추가 라우트를 컨트롤러에 정의해야 한다면, 반드시 `Route::resource` 호출 전에 해당 라우트들을 정의하세요. 그렇지 않으면, `resource` 메서드로 생성된 라우트가 별도의(보완) 라우트보다 우선 적용될 수 있습니다:

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러의 책임이 지나치게 많아진다면, 컨트롤러를 둘 이상의 작은 컨트롤러로 분리하는 것을 고려하세요.

<a name="singleton-resource-controllers"></a>
### 싱글턴 리소스 컨트롤러

애플리케이션에 오직 한 인스턴스만 존재할 수 있는 리소스가 있을 수 있습니다. 예를 들어, 한 사용자는 단 하나의 "프로필"만 가질 수 있으며, 이미지도 오직 하나의 "썸네일"만 가질 수 있습니다. 이러한 리소스를 "싱글턴 리소스(singleton resource)"라고 하며, 한 인스턴스만 존재할 수 있습니다. 이런 경우, "싱글턴" 리소스 컨트롤러를 등록할 수 있습니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위의 싱글턴 리소스 정의는 다음과 같은 라우트를 등록합니다. 보시는 것처럼 "생성" 라우트는 등록되지 않으며, 오직 한 인스턴스만 존재하므로 식별자 파라미터도 없습니다:

<div class="overflow-auto">

| HTTP 메서드 | URI             | 액션    | 라우트 이름      |
| ----------- | --------------- | ------- | ---------------- |
| GET         | `/profile`      | show    | profile.show     |
| GET         | `/profile/edit` | edit    | profile.edit     |
| PUT/PATCH   | `/profile`      | update  | profile.update   |

</div>

싱글턴 리소스는 표준 리소스 내에 중첩될 수도 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 예제에서, `photos` 리소스는 [표준 리소스 라우트](#actions-handled-by-resource-controllers)를 모두 갖지만, `thumbnail` 리소스는 아래와 같은 싱글턴 리소스로 등록됩니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                                 | 액션    | 라우트 이름                  |
| ----------- | ----------------------------------- | ------- | ---------------------------- |
| GET         | `/photos/{photo}/thumbnail`         | show    | photos.thumbnail.show        |
| GET         | `/photos/{photo}/thumbnail/edit`    | edit    | photos.thumbnail.edit        |
| PUT/PATCH   | `/photos/{photo}/thumbnail`         | update  | photos.thumbnail.update      |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글턴 리소스

가끔은 싱글턴 리소스에 대해 생성 및 저장 라우트도 정의하고 싶을 수 있습니다. 이런 경우, 싱글턴 리소스 라우트 등록 시 `creatable` 메서드를 호출할 수 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이 경우 다음과 같은 라우트가 등록됩니다. `DELETE` 라우트 역시 생성 가능한 싱글턴 리소스에 등록됩니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                                   | 액션     | 라우트 이름                  |
| ----------- | ------------------------------------- | -------- | ---------------------------- |
| GET         | `/photos/{photo}/thumbnail/create`    | create   | photos.thumbnail.create      |
| POST        | `/photos/{photo}/thumbnail`           | store    | photos.thumbnail.store       |
| GET         | `/photos/{photo}/thumbnail`           | show     | photos.thumbnail.show        |
| GET         | `/photos/{photo}/thumbnail/edit`      | edit     | photos.thumbnail.edit        |
| PUT/PATCH   | `/photos/{photo}/thumbnail`           | update   | photos.thumbnail.update      |
| DELETE      | `/photos/{photo}/thumbnail`           | destroy  | photos.thumbnail.destroy     |

</div>

생성과 저장 라우트는 필요 없지만, 싱글턴 리소스에 대해 `DELETE` 라우트만 등록하고 싶다면, `destroyable` 메서드를 사용할 수 있습니다:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글턴 리소스

`apiSingleton` 메서드는 API에서 다루어지는 싱글턴 리소스를 등록할 때 사용할 수 있으며, 이 경우 `create`, `edit` 라우트가 등록되지 않습니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```

API 싱글턴 리소스 역시 `creatable`하게 만들 수 있으며, 이 경우 `store`, `destroy` 라우트가 등록됩니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러

<a name="constructor-injection"></a>
#### 생성자 의존성 주입

라라벨의 [서비스 컨테이너](/docs/{{version}}/container)는 모든 컨트롤러 인스턴스를 해석할 때 사용됩니다. 따라서 컨트롤러에서 필요한 어떤 의존성이라도 생성자에 타입힌트만 하면 자동으로 해결되어 인스턴스에 주입됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * 새 컨트롤러 인스턴스를 생성합니다.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}
}
```

<a name="method-injection"></a>
#### 메서드 의존성 주입

생성자 주입 외에도, 컨트롤러의 개별 메서드에 의존성을 타입힌트로 주입받을 수 있습니다. 일반적인 예로는 `Illuminate\Http\Request` 인스턴스를 컨트롤러 메서드에 주입받는 경우가 있습니다:

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

컨트롤러 메서드에서 라우트 파라미터 입력도 함께 기대된다면, 다른 의존성 다음에 라우트 인자를 나열하면 됩니다. 예를 들어, 라우트가 다음과 같이 정의되어 있다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

다음과 같이 `Illuminate\Http\Request`를 타입힌트하면 `id`도 함께 받을 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정한 사용자를 업데이트합니다.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 업데이트...

        return redirect('/users');
    }
}
```
