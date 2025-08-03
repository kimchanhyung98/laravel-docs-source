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
    - [리소스 라우트 스코핑](#restful-scoping-resource-routes)
    - [리소스 URI 현지화](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 보완](#restful-supplementing-resource-controllers)
    - [싱글턴 리소스 컨트롤러](#singleton-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개

라우트 파일에 모든 요청 처리 로직을 클로저로 정의하는 대신, 컨트롤러 클래스를 사용해 이 동작들을 조직화할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스로 묶어 관리합니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청—보기, 생성, 수정, 삭제—을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기

<a name="basic-controllers"></a>
### 기본 컨트롤러

새 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 실행할 수 있습니다. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다:

```shell
php artisan make:controller UserController
```

간단한 기본 컨트롤러 예제를 살펴보겠습니다. 컨트롤러는 여러 개의 공개(public) 메서드를 가질 수 있으며, 이 메서드들이 들어오는 HTTP 요청에 대응합니다:

```
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 보여준다.
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

```
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

들어오는 요청이 지정한 라우트 URI와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고 라우트 파라미터가 해당 메서드에 전달됩니다.

> [!NOTE]  
> 컨트롤러가 반드시 어떤 기본 클래스를 상속해야 하는 것은 아니지만, 모든 컨트롤러에서 공유해야 하는 메서드를 포함하는 기본 컨트롤러 클래스를 상속하는 것이 편리할 수 있습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러

컨트롤러 액션이 특히 복잡한 경우, 해당 단일 액션에 전념하는 컨트롤러 클래스를 만드는 것이 편리할 수 있습니다. 이를 위해 컨트롤러 내에 단일 `__invoke` 메서드를 정의할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

class ProvisionServer extends Controller
{
    /**
     * 새로운 웹 서버를 프로비저닝한다.
     */
    public function __invoke()
    {
        // ...
    }
}
```

단일 액션 컨트롤러에 대한 라우트를 등록할 때는 메서드를 지정할 필요 없이, 단순히 컨트롤러 클래스 이름만 라우터에 전달하면 됩니다:

```
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` Artisan 명령어의 `--invokable` 옵션을 사용하여 invokable 컨트롤러를 생성할 수 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]  
> 컨트롤러의 스텁은 [스텁 게시](/docs/11.x/artisan#stub-customization)를 사용해 사용자화할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

[미들웨어](/docs/11.x/middleware)는 라우트 파일에서 컨트롤러 라우트에 할당할 수 있습니다:

```
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

또는 컨트롤러 클래스 내에서 미들웨어를 지정하는 것이 편리할 수 있습니다. 이를 위해 컨트롤러는 `HasMiddleware` 인터페이스를 구현해야 하며, 이 인터페이스는 컨트롤러가 정적 `middleware` 메서드를 갖도록 요구합니다. 이 메서드에서 컨트롤러 액션에 적용할 미들웨어 배열을 반환할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

class UserController extends Controller implements HasMiddleware
{
    /**
     * 컨트롤러에 할당할 미들웨어를 반환한다.
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

또한, 전체 미들웨어 클래스를 작성하지 않고도 간단히 클로저로 컨트롤러 미들웨어를 정의할 수 있습니다:

```
use Closure;
use Illuminate\Http\Request;

/**
 * 컨트롤러에 할당할 미들웨어를 반환한다.
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
> `Illuminate\Routing\Controllers\HasMiddleware`를 구현하는 컨트롤러는 `Illuminate\Routing\Controller`를 상속해서는 안 됩니다.

<a name="resource-controllers"></a>
## 리소스 컨트롤러

각 Eloquent 모델을 "리소스"로 생각할 때, 애플리케이션에서는 이러한 리소스 각각에 대해 흔히 동일한 작업 세트(생성, 읽기, 수정, 삭제 등)를 수행하게 됩니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다면, 사용자들이 이 리소스들을 생성, 조회, 수정, 삭제할 가능성이 큽니다.

이러한 공통적인 사용 사례 때문에, Laravel 리소스 라우팅은 한 줄의 코드로 컨트롤러에 대해 전형적인 생성, 읽기, 수정, 삭제("CRUD") 라우트를 할당합니다. 먼저, `make:controller` Artisan 명령어의 `--resource` 옵션을 사용해 이러한 작업을 처리할 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

이 명령어는 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성하며, 각 리소스 작업에 맞는 메서드를 포함합니다. 다음으로, 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다:

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 한 줄의 라우트 선언으로 리소스에 대한 다양한 작업을 처리하는 다수의 라우트가 생성됩니다. 생성된 컨트롤러는 이미 각 작업에 대한 메서드가 미리 정의되어 있습니다. 애플리케이션의 라우트를 한눈에 보고 싶다면 `route:list` Artisan 명령어를 실행해 보세요.

또한, `resources` 메서드에 배열을 전달하여 여러 리소스 컨트롤러를 한 번에 등록할 수도 있습니다:

```
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션

<div class="overflow-auto">

| HTTP 메서드 | URI                      | 액션    | 라우트 이름       |
| --------- | ------------------------ | ------ | -------------- |
| GET       | `/photos`                | index  | photos.index    |
| GET       | `/photos/create`         | create | photos.create   |
| POST      | `/photos`                | store  | photos.store    |
| GET       | `/photos/{photo}`        | show   | photos.show     |
| GET       | `/photos/{photo}/edit`   | edit   | photos.edit     |
| PUT/PATCH | `/photos/{photo}`        | update | photos.update   |
| DELETE    | `/photos/{photo}`        | destroy| photos.destroy  |

</div>

<a name="customizing-missing-model-behavior"></a>
#### 모델 미발견(Customizing Missing Model Behavior)

일반적으로 암묵적 바인딩된 리소스 모델이 발견되지 않으면 404 HTTP 응답이 반환됩니다. 하지만 리소스 라우트를 정의할 때 `missing` 메서드를 호출하여 이 동작을 커스터마이징할 수 있습니다. `missing` 메서드는 암묵적 바인딩이 실패했을 때 호출될 클로저를 받습니다:

```
use App\Http\Controllers\PhotoController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::resource('photos', PhotoController::class)
    ->missing(function (Request $request) {
        return Redirect::route('photos.index');
    });
```

<a name="soft-deleted-models"></a>
#### 소프트 삭제된 모델 (Soft Deleted Models)

암묵적 모델 바인딩은 기본적으로 [soft deleting](/docs/11.x/eloquent#soft-deleting) 된 모델을 반환하지 않고 404 응답을 반환합니다. 하지만 리소스 라우트를 정의할 때 `withTrashed` 메서드를 호출해 소프트 삭제된 모델도 허용할 수 있습니다:

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

인수를 주지 않고 `withTrashed`를 호출하면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델을 허용합니다. 특정 라우트만 지정하려면 배열을 전달하세요:

```
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정하기

[라우트 모델 바인딩](/docs/11.x/routing#route-model-binding)과 함께 리소스 컨트롤러 메서드 내에서 모델 인스턴스를 타입힌트하고 싶을 때, 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 요청 클래스 생성하기

리소스 컨트롤러 생성 시 `--requests` 옵션을 주면, 저장 및 업데이트 메서드용 [폼 요청 클래스](/docs/11.x/validation#form-request-validation)를 Artisan이 자동으로 생성하도록 할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트를 선언할 때, 컨트롤러가 처리할 액션의 일부만 지정할 수도 있습니다. 기본 액션 전체 세트 대신 하위 집합을 지정할 수 있습니다:

```
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

API에서 사용하는 리소스 라우트에는 일반적으로 `create`와 `edit` 같이 HTML 템플릿을 제공하는 라우트를 제외하고 싶습니다. 이를 편리하게 하기 위해 `apiResource` 메서드를 사용해 이 두 라우트를 자동으로 제외할 수 있습니다:

```
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

한 번에 여러 API 리소스 컨트롤러를 등록할 때도 배열을 `apiResources` 메서드에 전달할 수 있습니다:

```
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`create`나 `edit` 메서드가 없는 API 리소스 컨트롤러를 빠르게 생성하려면 `make:controller` 명령어에서 `--api` 스위치를 사용하세요:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스

때로는 중첩 리소스에 대한 라우트를 정의해야 할 때가 있습니다. 예를 들어, 사진 리소스에는 해당 사진에 달린 여러 댓글이 있을 수 있습니다. 이런 중첩 리소스 컨트롤러를 지정하려면 라우트 선언에서 "dot" 표기법을 사용할 수 있습니다:

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 URI를 가지는 중첩 리소스를 등록합니다:

```
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 스코핑

Laravel의 [암묵적 모델 바인딩 스코핑](/docs/11.x/routing#implicit-model-binding-scoping)을 이용하면, 중첩 바인딩에서 확인된 자식 모델이 부모 모델에 속하는지 자동으로 스코핑할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 스코핑을 활성화하고, 자식 리소스를 조회할 필드를 Laravel에 알려줄 수 있습니다. 이에 관한 자세한 내용은 [리소스 라우트 스코핑](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 얕은 중첩 (Shallow Nesting)

URI에 부모와 자식 ID를 모두 포함하는 것이 항상 필요한 것은 아닙니다. 자식 ID만으로도 고유 식별이 되기 때문입니다. URI 세그먼트에서 자동 증가 기본 키 같은 고유 식별자를 사용할 경우 "얕은 중첩"을 선택할 수 있습니다:

```
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

이 라우트 정의는 다음과 같은 라우트를 생성합니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                          | 액션    | 라우트 이름              |
| --------- | ---------------------------- | ------ | ----------------------- |
| GET       | `/photos/{photo}/comments`    | index  | photos.comments.index   |
| GET       | `/photos/{photo}/comments/create` | create | photos.comments.create  |
| POST      | `/photos/{photo}/comments`    | store  | photos.comments.store   |
| GET       | `/comments/{comment}`         | show   | comments.show           |
| GET       | `/comments/{comment}/edit`    | edit   | comments.edit           |
| PUT/PATCH | `/comments/{comment}`         | update | comments.update         |
| DELETE    | `/comments/{comment}`         | destroy| comments.destroy        |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정

기본적으로 모든 리소스 컨트롤러 액션에는 라우트 이름이 있지만, 원하는 라우트 이름으로 `names` 배열을 전달해 이 이름들을 재정의할 수 있습니다:

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정

기본적으로 `Route::resource`는 리소스 이름을 단수형으로 변환하여 라우트 파라미터를 생성합니다. `parameters` 메서드를 통해 리소스별로 이를 쉽게 재정의할 수 있습니다. 이 메서드에 전달하는 배열은 리소스 이름과 파라미터 이름의 연관 배열이어야 합니다:

```
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예제는 `show` 라우트에 대해 다음 URI를 생성합니다:

```
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코핑

Laravel의 [스코프된 암묵적 모델 바인딩](/docs/11.x/routing#implicit-model-binding-scoping) 기능을 사용하면, 중첩된 자식 모델이 반드시 부모 모델에 속하는지 확인하며 스코핑을 자동으로 적용할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 써서 자동 스코핑을 활성화하고, 자식 모델 조회에 사용할 필드를 지정할 수 있습니다:

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 다음과 같은 URI를 등록합니다:

```
/photos/{photo}/comments/{comment:slug}
```

중첩 라우트 파라미터에서 커스텀 키가 적용된 암묵적 바인딩을 사용할 때, Laravel은 부모와의 관계를 기준으로 쿼리를 자동 스코핑합니다. 컨벤션에 따라 `Photo` 모델이 `comments`라는(라우트 파라미터 이름의 복수형) 관계를 가지고 있다고 가정합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화

기본적으로 `Route::resource`는 영어 동사와 복수 규칙을 적용해 리소스 URI를 생성합니다. `create`와 `edit` 액션 동사를 현지화해야 할 경우, 애플리케이션의 `App\Providers\AppServiceProvider` 내 `boot` 메서드 초반에 `Route::resourceVerbs` 메서드를 사용할 수 있습니다:

```
/**
 * 애플리케이션 서비스를 부트스트랩한다.
 */
public function boot(): void
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);
}
```

Laravel의 복수형 처리기는 [필요에 따라 다양한 언어 설정이 가능합니다](/docs/11.x/localization#pluralization-language). 동사와 복수형 언어 설정을 변경한 뒤, 다음과 같은 리소스 라우트 등록이 생성됩니다:

```
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보완

기본 리소스 라우트 외에 추가 라우트를 리소스 컨트롤러에 더 추가해야 한다면, `Route::resource` 메서드를 호출하기 전에 라우트를 정의하는 것이 좋습니다. 그렇지 않으면 `resource` 메서드에서 정의한 라우트가 보완용 라우트를 덮어쓸 수 있습니다:

```
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]  
> 컨트롤러를 깔끔하게 유지하세요. 전형적인 리소스 액션 범위를 벗어난 메서드가 자주 필요하다면, 컨트롤러를 둘 이상의 작은 컨트롤러로 분리하는 것을 고려해 보세요.

<a name="singleton-resource-controllers"></a>
### 싱글턴 리소스 컨트롤러

애플리케이션에 하나뿐인 인스턴스만 가질 수 있는 리소스가 있을 수 있습니다. 예를 들어, 사용자의 "프로필"은 하나만 존재하며 수정하거나 업데이트할 수 있습니다. 마찬가지로 이미지에는 하나의 "썸네일"만 있을 수 있습니다. 이런 리소스를 "싱글턴 리소스"라고 하며, 단 하나의 인스턴스만 존재합니다. 이런 경우 "싱글턴" 리소스 컨트롤러를 등록할 수 있습니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위의 싱글턴 리소스 정의는 다음과 같은 라우트를 등록합니다. 생성 관련 라우트는 존재하지 않으며, 라우트에 식별자가 포함되지 않는다는 점이 특징입니다:

<div class="overflow-auto">

| HTTP 메서드 | URI             | 액션   | 라우트 이름    |
| --------- | --------------- | ------ | ------------- |
| GET       | `/profile`      | show   | profile.show  |
| GET       | `/profile/edit` | edit   | profile.edit  |
| PUT/PATCH | `/profile`      | update | profile.update|

</div>

싱글턴 리소스는 표준 리소스 내에 중첩될 수도 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 예시에서는 `photos` 리소스가 모든 [표준 리소스 라우트](#actions-handled-by-resource-controllers)를 가지며, `thumbnail` 리소스는 다음 라우트를 가지는 싱글턴 리소스입니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                               | 액션   | 라우트 이름              |
| --------- | --------------------------------- | ------ | ----------------------- |
| GET       | `/photos/{photo}/thumbnail`       | show   | photos.thumbnail.show   |
| GET       | `/photos/{photo}/thumbnail/edit`  | edit   | photos.thumbnail.edit   |
| PUT/PATCH | `/photos/{photo}/thumbnail`       | update | photos.thumbnail.update |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글턴 리소스

가끔은 싱글턴 리소스에 대해 생성 및 저장 라우트를 정의해야 할 때도 있습니다. 이를 위해 싱글턴 리소스 라우트를 등록할 때 `creatable` 메서드를 호출하세요:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이 경우, 다음과 같은 라우트들이 등록됩니다. `DELETE` 라우트도 함께 등록되는 점에 주의하세요:

<div class="overflow-auto">

| HTTP 메서드 | URI                                 | 액션    | 라우트 이름               |
| --------- | ----------------------------------- | ------- | ------------------------ |
| GET       | `/photos/{photo}/thumbnail/create`  | create  | photos.thumbnail.create  |
| POST      | `/photos/{photo}/thumbnail`          | store   | photos.thumbnail.store   |
| GET       | `/photos/{photo}/thumbnail`          | show    | photos.thumbnail.show    |
| GET       | `/photos/{photo}/thumbnail/edit`     | edit    | photos.thumbnail.edit    |
| PUT/PATCH | `/photos/{photo}/thumbnail`          | update  | photos.thumbnail.update  |
| DELETE    | `/photos/{photo}/thumbnail`          | destroy | photos.thumbnail.destroy |

</div>

만약 싱글턴 리소스에 대해 `DELETE` 라우트만 등록하고 생성 및 저장 라우트는 등록하지 않으려면 `destroyable` 메서드를 사용할 수 있습니다:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글턴 리소스

`apiSingleton` 메서드는 `create`와 `edit` 라우트가 필요 없는 API용 싱글턴 리소스를 등록할 때 사용합니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론 API 싱글턴 리소스도 `creatable` 하여 `store`와 `destroy` 라우트를 등록할 수 있습니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러

<a name="constructor-injection"></a>
#### 생성자 주입 (Constructor Injection)

Laravel의 [서비스 컨테이너](/docs/11.x/container)는 모든 컨트롤러를 해결(resolving)하는 데 사용됩니다. 따라서 컨트롤러가 필요로 하는 의존성을 생성자의 파라미터로 타입힌트할 수 있습니다. 선언한 의존성은 자동으로 해결되어 컨트롤러 인스턴스에 주입됩니다:

```
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * 새 컨트롤러 인스턴스를 생성한다.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}
}
```

<a name="method-injection"></a>
#### 메서드 주입 (Method Injection)

생성자 주입 외에도, 컨트롤러 메서드에서도 의존성을 타입힌트할 수 있습니다. 가장 일반적인 예는 `Illuminate\Http\Request` 인스턴스를 컨트롤러 메서드에 주입하는 것입니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새 사용자를 저장한다.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->name;

        // 사용자를 저장한다...

        return redirect('/users');
    }
}
```

만약 컨트롤러 메서드가 라우트 파라미터도 기대한다면, 다른 의존성 뒤에 라우트 인수를 나열하세요. 예를 들어, 다음과 같이 라우트가 정의되어 있을 때:

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

`Illuminate\Http\Request`를 타입힌트하면서 `id` 파라미터도 다음과 같이 받을 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정한 사용자를 수정한다.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자를 수정한다...

        return redirect('/users');
    }
}
```