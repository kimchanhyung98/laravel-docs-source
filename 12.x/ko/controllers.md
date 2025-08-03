# 컨트롤러 (Controllers)

- [소개](#introduction)
- [컨트롤러 작성하기](#writing-controllers)
    - [기본 컨트롤러](#basic-controllers)
    - [단일 액션 컨트롤러](#single-action-controllers)
- [컨트롤러 미들웨어](#controller-middleware)
- [리소스 컨트롤러](#resource-controllers)
    - [부분 리소스 라우트](#restful-partial-resource-routes)
    - [중첩 리소스](#restful-nested-resources)
    - [리소스 라우트 이름 지정하기](#restful-naming-resource-routes)
    - [리소스 라우트 파라미터 이름 지정하기](#restful-naming-resource-route-parameters)
    - [리소스 라우트 스코핑](#restful-scoping-resource-routes)
    - [리소스 URI 현지화](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 보충하기](#restful-supplementing-resource-controllers)
    - [싱글턴 리소스 컨트롤러](#singleton-resource-controllers)
    - [미들웨어와 리소스 컨트롤러](#middleware-and-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개 (Introduction)

라우트 파일에 모든 요청 처리 로직을 클로저로 정의하는 대신, "컨트롤러" 클래스를 사용하여 이 동작을 체계적으로 관리할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스로 묶을 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청(보기, 생성, 수정, 삭제 등)을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기 (Writing Controllers)

<a name="basic-controllers"></a>
### 기본 컨트롤러 (Basic Controllers)

새 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 실행하세요. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

```shell
php artisan make:controller UserController
```

기본 컨트롤러 예제를 살펴보겠습니다. 컨트롤러는 여러 개의 public 메서드를 가질 수 있으며, 이 메서드들은 들어오는 HTTP 요청에 응답합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 보여줍니다.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

컨트롤러 클래스와 메서드를 작성한 후, 다음과 같이 해당 컨트롤러 메서드에 대한 라우트를 정의할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

요청이 해당 라우트 URI와 일치하면 `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고, 라우트 파라미터가 메서드에 전달됩니다.

> [!NOTE]
> 컨트롤러가 반드시 기본 클래스를 상속해야 하는 것은 아닙니다. 하지만 모든 컨트롤러에서 공유해야 하는 메서드를 포함한 기본 컨트롤러 클래스를 상속하는 것이 편리한 경우가 많습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러 (Single Action Controllers)

컨트롤러 액션이 특히 복잡한 경우, 단일 액션에 전념하는 컨트롤러 클래스를 따로 만드는 것이 편리할 수 있습니다. 이를 위해 컨트롤러 내에 단일 `__invoke` 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

class ProvisionServer extends Controller
{
    /**
     * 새 웹 서버를 프로비저닝합니다.
     */
    public function __invoke()
    {
        // ...
    }
}
```

단일 액션 컨트롤러의 라우트를 등록할 때는 컨트롤러 메서드를 명시할 필요가 없습니다. 대신, 컨트롤러 이름만 라우터에 전달하면 됩니다:

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` Artisan 명령어에서 `--invokable` 옵션을 사용하면 단일 액션 컨트롤러를 생성할 수 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 사용해 사용자 지정할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어 (Controller Middleware)

[미들웨어](/docs/12.x/middleware)는 라우트 파일에서 컨트롤러의 라우트에 할당할 수 있습니다:

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

또는 컨트롤러 클래스 내에서 미들웨어를 지정하는 것이 편리할 수 있습니다. 이를 위해 컨트롤러는 `HasMiddleware` 인터페이스를 구현해야 하며, 이 인터페이스는 컨트롤러가 정적 `middleware` 메서드를 갖도록 요구합니다. 이 메서드에서 컨트롤러 액션에 적용할 미들웨어 배열을 반환할 수 있습니다:

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

또한 클로저 형태로 컨트롤러 미들웨어를 정의할 수도 있습니다. 이는 전체 미들웨어 클래스를 작성하지 않고 인라인 미들웨어를 정의하는 편리한 방법입니다:

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

<a name="resource-controllers"></a>
## 리소스 컨트롤러 (Resource Controllers)

애플리케이션의 각 Eloquent 모델을 "리소스"로 생각할 때, 보통 애플리케이션 내의 각 리소스에 대해 같은 작업 집합을 수행합니다. 예를 들면, `Photo` 모델과 `Movie` 모델이 있고 사용자는 이 리소스를 생성, 조회, 수정, 삭제할 수 있습니다.

이러한 공통 용례 때문에, Laravel의 리소스 라우팅은 컨트롤러에 반복적인 CRUD(create, read, update, delete) 작업을 한 줄 코드로 할당합니다. 시작하려면 `make:controller` Artisan 명령어에서 `--resource` 옵션을 사용해 이러한 작업을 처리할 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

이 명령어는 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성하며, 사용 가능한 리소스 작업별 메서드를 포함합니다. 다음으로, 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 단일 라우트 선언은 리소스에 대한 다양한 액션을 처리하는 여러 라우트를 생성합니다. 생성된 컨트롤러는 이러한 작업 각각에 대한 메서드 스텁을 이미 포함합니다. 애플리케이션의 라우트를 빠르게 확인하려면 `route:list` Artisan 명령어를 실행하면 됩니다.

여러 리소스 컨트롤러도 한 번에 등록할 수 있으며, `resources` 메서드에 배열을 전달하면 됩니다:

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`softDeletableResources` 메서드는 모두 `withTrashed` 메서드를 사용하는 리소스 컨트롤러를 한 번에 등록합니다:

```php
Route::softDeletableResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션들

<div class="overflow-auto">

| 메서드(Verb) | URI                    | 액션(Action) | 라우트 이름(Route Name)  |
| ------------ | ---------------------- | ------------ | ------------------------ |
| GET          | `/photos`              | index        | photos.index             |
| GET          | `/photos/create`       | create       | photos.create            |
| POST         | `/photos`              | store        | photos.store             |
| GET          | `/photos/{photo}`      | show         | photos.show              |
| GET          | `/photos/{photo}/edit` | edit         | photos.edit              |
| PUT/PATCH    | `/photos/{photo}`      | update       | photos.update            |
| DELETE       | `/photos/{photo}`      | destroy      | photos.destroy           |

</div>

<a name="customizing-missing-model-behavior"></a>
#### 누락된 모델 동작 사용자 정의

일반적으로 암묵적 바인딩된 리소스 모델을 찾을 수 없으면 404 HTTP 응답이 생성됩니다. 하지만 리소스 라우트를 정의할 때 `missing` 메서드를 호출해 이 동작을 사용자 정의할 수 있습니다. `missing` 메서드는 암묵적 바인딩된 모델을 찾지 못했을 때 호출할 클로저를 받습니다:

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

암묵적 모델 바인딩은 보통 [소프트 삭제된](/docs/12.x/eloquent#soft-deleting) 모델을 조회하지 않으며, 대신 404 HTTP 응답을 반환합니다. 하지만 리소스 라우트를 정의할 때 `withTrashed` 메서드를 호출해 소프트 삭제된 모델을 허용하도록 할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

인자 없이 `withTrashed`를 호출하면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델을 허용합니다. 배열 인자를 넘겨 특정 라우트만 지정할 수도 있습니다:

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정하기

[라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 사용 중이고, 리소스 컨트롤러의 메서드에서 모델 인스턴스를 타입 힌팅하고 싶다면 컨트롤러 생성 시 `--model` 옵션을 사용하세요:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 요청 클래스 생성

`--requests` 옵션을 사용하여 리소스 컨트롤러 생성 시, Artisan에게 저장(store) 및 업데이트(update) 메서드용 [폼 요청 클래스](/docs/12.x/validation#form-request-validation)를 생성하도록 지시할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트 (Partial Resource Routes)

리소스 라우트를 선언할 때, 컨트롤러가 처리할 액션들의 일부만 지정할 수 있습니다. 기본 액션 전체 대신 일부만 선택해 설정할 수 있습니다:

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

API에서 소비되는 리소스 라우트를 선언할 때, `create`와 `edit` 같이 HTML 템플릿을 제공하는 라우트는 보통 제외합니다. 이를 위해 `apiResource` 메서드를 사용하면 이 두 라우트를 자동으로 제외할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

한 번에 여러 API 리소스 컨트롤러도 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`create`와 `edit` 메서드가 포함되지 않는 API 리소스 컨트롤러를 빠르게 생성하려면 `make:controller` 명령에서 `--api` 옵션을 사용하세요:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스 (Nested Resources)

리소스에 대해 중첩된 리소스 라우트를 정의해야 하는 경우가 있습니다. 예를 들어, 사진 리소스에는 여러 댓글이 달릴 수 있습니다. 중첩 리소스 컨트롤러를 등록하려면 라우트 선언에 점(dot) 표기법을 사용합니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 URI를 가집니다:

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 스코핑

Laravel의 [암묵적 모델 바인딩 스코핑](/docs/12.x/routing#implicit-model-binding-scoping) 기능은 중첩 바인딩에서 자식 모델이 상위 모델에 속하는지 자동으로 스코핑합니다. 네스티드 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 스코핑을 활성화하고 자식 리소스를 조회할 필드를 지정할 수 있습니다. 자세한 내용은 [리소스 라우트 스코핑](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 얕은 중첩 (Shallow Nesting)

부모와 자식 ID가 URI에 모두 포함될 필요가 없는 경우가 많습니다. 특히, 자식 ID가 이미 고유 식별자인 경우가 그렇습니다. 이런 경우 자동 증가하는 기본 키 같은 고유 식별자를 URI 세그먼트에서 쓰면 "얕은 중첩"을 사용할 수 있습니다:

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

이렇게 정의하면 다음과 같은 라우트가 생성됩니다:

<div class="overflow-auto">

| 메서드(Verb) | URI                               | 액션(Action) | 라우트 이름(Route Name)          |
| ------------ | --------------------------------- | ------------ | ------------------------------- |
| GET          | `/photos/{photo}/comments`        | index        | photos.comments.index            |
| GET          | `/photos/{photo}/comments/create` | create       | photos.comments.create           |
| POST         | `/photos/{photo}/comments`        | store        | photos.comments.store            |
| GET          | `/comments/{comment}`             | show         | comments.show                   |
| GET          | `/comments/{comment}/edit`        | edit         | comments.edit                   |
| PUT/PATCH    | `/comments/{comment}`             | update       | comments.update                 |
| DELETE       | `/comments/{comment}`             | destroy      | comments.destroy                |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정하기 (Naming Resource Routes)

기본적으로 모든 리소스 컨트롤러의 액션은 라우트 이름을 갖지만, 원하는 라우트 이름을 지정하기 위해 `names` 배열을 전달해 이를 덮어쓸 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정하기 (Naming Resource Route Parameters)

기본적으로 `Route::resource`는 리소스 이름을 단수형으로 변환한 값을 라우트 파라미터 이름으로 만듭니다. 이를 리소스별로 쉽게 덮어쓰려면 `parameters` 메서드를 사용하세요. `parameters` 메서드에 전달하는 배열은 리소스 이름과 파라미터 이름의 연관 배열이어야 합니다:

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예제는 리소스의 `show` 라우트에 대해 다음 URI를 생성합니다:

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코핑 (Scoping Resource Routes)

Laravel의 [스코프된 암묵적 모델 바인딩](/docs/12.x/routing#implicit-model-binding-scoping) 기능은 중첩된 바인딩에서 자식 모델이 상위 모델에 속해 있는지 자동으로 스코핑합니다. 중첩 네스티드 리소스 정의 시 `scoped` 메서드를 사용해 자동 스코핑을 활성화하고, 자식 리소스를 조회할 필드를 지정할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 다음과 같은 URI를 가집니다:

```text
/photos/{photo}/comments/{comment:slug}
```

커스텀 키를 사용하는 암묵적 바인딩을 중첩 라우트 파라미터에서 사용하면, Laravel은 상위 모델의 관계 이름을 추측해 중첩 모델을 상위 모델로 스코핑합니다. 이 경우 `Photo` 모델은 `comments`라는 관계(라우트 파라미터 이름의 복수형)를 가졌다고 간주하여 `Comment` 모델을 조회합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화 (Localizing Resource URIs)

기본적으로 `Route::resource`는 영어 동사와 복수 규칙을 적용해 리소스 URI를 생성합니다. `create`와 `edit` 액션 동사를 현지화하려면 `Route::resourceVerbs` 메서드를 사용하세요. 보통 애플리케이션 `App\Providers\AppServiceProvider`의 `boot` 메서드 시작 부분에 설정합니다:

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

Laravel의 복수화(pluralizer)는 [다양한 언어 설정을 지원하며, 필요에 따라 변경할 수 있습니다](/docs/12.x/localization#pluralization-language). 동사와 복수 규칙을 현지화하면, 예를 들어 `Route::resource('publicacion', PublicacionController::class)`는 다음과 같은 URI를 만듭니다:

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보충하기 (Supplementing Resource Controllers)

기본 리소스 라우트 집합 외에 리소스 컨트롤러에 추가적인 라우트를 정의해야 하는 경우, `Route::resource` 메서드를 호출하기 전에 라우트를 정의하세요. 그렇지 않으면 `resource` 메서드에서 정의한 라우트가 보충 라우트보다 우선시될 수 있습니다:

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러는 역할을 명확히 유지하세요. 일반적인 리소스 액션 외 메서드가 자주 필요하다면 컨트롤러를 두 개로 나눠 더 작은 단위로 관리하는 것을 고려하세요.

<a name="singleton-resource-controllers"></a>
### 싱글턴 리소스 컨트롤러 (Singleton Resource Controllers)

간혹 애플리케이션 내 리소스가 단 하나의 인스턴스만 가질 수 있는 경우가 있습니다. 예를 들어, 사용자의 "프로필"은 수정하거나 업데이트할 수 있지만 한 사용자당 프로필은 하나뿐입니다. 마찬가지로 이미지에 "썸네일"은 하나만 있을 수 있습니다. 이러한 리소스를 "싱글턴 리소스"라고 하며, 하나의 인스턴스만 존재할 수 있습니다. 이 경우 "싱글턴" 리소스 컨트롤러를 등록할 수 있습니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위 싱글턴 리소스 정의는 다음 라우트를 등록합니다. 생성(create) 라우트가 등록되지 않고, 한 인스턴스만 존재하므로 식별자도 받지 않습니다:

<div class="overflow-auto">

| 메서드(Verb) | URI             | 액션   | 라우트 이름(Route Name) |
| ------------ | --------------- | ------ | ----------------------- |
| GET          | `/profile`      | show   | profile.show            |
| GET          | `/profile/edit` | edit   | profile.edit            |
| PUT/PATCH    | `/profile`      | update | profile.update          |

</div>

싱글턴 리소스는 일반 리소스 내 중첩으로도 등록할 수 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 예에서는 `photos` 리소스는 [표준 리소스 라우트](#actions-handled-by-resource-controllers)를 모두 받지만, `thumbnail` 리소스는 다음 라우트만 있는 싱글턴 리소스가 됩니다:

<div class="overflow-auto">

| 메서드(Verb) | URI                              | 액션   | 라우트 이름(Route Name)          |
| ------------ | -------------------------------- | ------ | ------------------------------- |
| GET          | `/photos/{photo}/thumbnail`      | show   | photos.thumbnail.show            |
| GET          | `/photos/{photo}/thumbnail/edit` | edit   | photos.thumbnail.edit            |
| PUT/PATCH    | `/photos/{photo}/thumbnail`      | update | photos.thumbnail.update          |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글턴 리소스

가끔 싱글턴 리소스에 대해 생성(create) 및 저장(store) 라우트를 정의하고 싶을 수 있습니다. 이 경우 싱글턴 리소스 등록 시 `creatable` 메서드를 호출하세요:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이때 다음 라우트가 등록됩니다. 생성 가능 싱글턴 리소스는 `DELETE` 라우트도 등록됩니다:

<div class="overflow-auto">

| 메서드(Verb) | URI                                | 액션    | 라우트 이름(Route Name)          |
| ------------ | ---------------------------------- | ------- | ------------------------------- |
| GET          | `/photos/{photo}/thumbnail/create` | create  | photos.thumbnail.create          |
| POST         | `/photos/{photo}/thumbnail`        | store   | photos.thumbnail.store           |
| GET          | `/photos/{photo}/thumbnail`        | show    | photos.thumbnail.show            |
| GET          | `/photos/{photo}/thumbnail/edit`   | edit    | photos.thumbnail.edit            |
| PUT/PATCH    | `/photos/{photo}/thumbnail`        | update  | photos.thumbnail.update          |
| DELETE       | `/photos/{photo}/thumbnail`        | destroy | photos.thumbnail.destroy         |

</div>

생성 및 저장 라우트는 등록하지 않고 `DELETE` 라우트만 등록하길 원하면 `destroyable` 메서드를 사용하세요:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글턴 리소스

`apiSingleton` 메서드는 API로 조작되는 싱글턴 리소스를 등록하는 데 사용하며, 이 경우 `create`와 `edit` 라우트는 불필요하므로 생성하지 않습니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론 API 싱글턴 리소스도 `creatable`로 설정할 수 있으며, 이럴 때 `store` 및 `destroy` 라우트를 등록합니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="middleware-and-resource-controllers"></a>
### 미들웨어와 리소스 컨트롤러 (Middleware and Resource Controllers)

Laravel은 `middleware`, `middlewareFor`, `withoutMiddlewareFor` 메서드를 통해 리소스 라우트 전체 또는 특정 메서드에 미들웨어를 정밀하게 할당할 수 있습니다.

#### 모든 메서드에 미들웨어 적용하기

`middleware` 메서드를 사용하면 리소스 또는 싱글턴 리소스의 모든 라우트에 미들웨어를 할당할 수 있습니다:

```php
Route::resource('users', UserController::class)
    ->middleware(['auth', 'verified']);

Route::singleton('profile', ProfileController::class)
    ->middleware('auth');
```

#### 특정 메서드에 미들웨어 적용하기

`middlewareFor` 메서드를 사용하면 특정 리소스 컨트롤러 메서드 한 개 또는 여러 개에 미들웨어를 할당할 수 있습니다:

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

`middlewareFor` 메서드는 싱글턴 및 API 싱글턴 리소스 컨트롤러와도 함께 사용할 수 있습니다:

```php
Route::singleton('profile', ProfileController::class)
    ->middlewareFor('show', 'auth');

Route::apiSingleton('profile', ProfileController::class)
    ->middlewareFor(['show', 'update'], 'auth');
```

#### 특정 메서드에서 미들웨어 제외하기

`withoutMiddlewareFor` 메서드로 특정 리소스 컨트롤러 메서드에서 미들웨어를 제외할 수 있습니다:

```php
Route::middleware(['auth', 'verified', 'subscribed'])->group(function () {
    Route::resource('users', UserController::class)
        ->withoutMiddlewareFor('index', ['auth', 'verified'])
        ->withoutMiddlewareFor(['create', 'store'], 'verified')
        ->withoutMiddlewareFor('destroy', 'subscribed');
});
```

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러 (Dependency Injection and Controllers)

<a name="constructor-injection"></a>
#### 생성자 의존성 주입 (Constructor Injection)

Laravel의 [서비스 컨테이너](/docs/12.x/container)는 모든 컨트롤러를 해결(resolution)합니다. 따라서 컨트롤러 생성자에 필요한 의존성을 타입 힌팅하면, 선언된 의존성이 자동으로 해결되어 컨트롤러 인스턴스에 주입됩니다:

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
#### 메서드 의존성 주입 (Method Injection)

생성자 주입 외에도 컨트롤러 메서드에서 의존성을 타입 힌팅할 수 있습니다. 흔한 사용 사례는 컨트롤러 메서드에 `Illuminate\Http\Request` 인스턴스를 주입하는 것입니다:

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

        // 사용자 저장 로직...

        return redirect('/users');
    }
}
```

라우트 파라미터의 입력도 기대한다면, 라우트 인수는 다른 의존성 뒤에 나열하세요. 예를 들어 라우트가 다음과 같이 정의되어 있다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

다음과 같이 컨트롤러 메서드를 정의해 `Illuminate\Http\Request`와 `id` 파라미터를 모두 사용할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 주어진 사용자를 갱신합니다.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 업데이트 로직...

        return redirect('/users');
    }
}
```