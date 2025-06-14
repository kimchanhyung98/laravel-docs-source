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
    - [리소스 컨트롤러 보충하기](#restful-supplementing-resource-controllers)
    - [싱글턴 리소스 컨트롤러](#singleton-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개

모든 요청 처리 로직을 라우트 파일에 클로저로 정의하는 대신, "컨트롤러" 클래스를 사용해 이러한 동작을 더 체계적으로 구성할 수 있습니다. 컨트롤러는 서로 연관된 요청 처리 로직을 하나의 클래스로 묶어 관리할 수 있게 해줍니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 요청들(보기, 생성, 수정, 삭제 등)을 모두 담당할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기

<a name="basic-controllers"></a>
### 기본 컨트롤러

새로운 컨트롤러를 빠르게 생성하려면 `make:controller` 아티즌 명령어를 실행하면 됩니다. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

```shell
php artisan make:controller UserController
```

기본 컨트롤러의 예제를 살펴보겠습니다. 컨트롤러에는 여러 개의 public 메서드를 정의할 수 있으며, 각각이 들어오는 HTTP 요청에 응답하게 됩니다.

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

컨트롤러 클래스와 메서드를 작성한 뒤에는, 아래와 같이 해당 컨트롤러 메서드로 라우트를 등록할 수 있습니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

지정된 라우트 URI와 들어오는 요청이 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고, 라우트 파라미터가 해당 메서드에 전달됩니다.

> [!NOTE]
> 컨트롤러는 반드시 어떤 기본 클래스를 상속할 필요는 없습니다. 하지만 여러 컨트롤러에서 공유해야 할 메서드가 있다면, 기본 컨트롤러 클래스를 상속하는 것이 편리할 때도 있습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러

특정 액션의 복잡성이 높은 경우, 그 액션만을 전담하는 컨트롤러 클래스를 따로 두는 것이 더 명확할 수 있습니다. 이를 위해 컨트롤러 안에 `__invoke`라는 단일 메서드만 정의하면 됩니다.

```php
<?php

namespace App\Http\Controllers;

class ProvisionServer extends Controller
{
    /**
     * 새로운 웹 서버를 프로비저닝합니다.
     */
    public function __invoke()
    {
        // ...
    }
}
```

단일 액션 컨트롤러를 라우트로 등록할 때는 별도의 컨트롤러 메서드를 지정할 필요 없이, 컨트롤러의 이름만 라우터에 전달하면 됩니다.

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

아티즌 명령어의 `--invokable` 옵션을 사용해 호출 가능한(Invokable) 컨트롤러를 생성할 수도 있습니다.

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁(stub)은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

[미들웨어](/docs/12.x/middleware)는 라우트 파일 내에서 컨트롤러의 라우트에 직접 지정할 수 있습니다.

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

또는, 컨트롤러 클래스 내에서 미들웨어를 지정하는 것이 더 편리할 수도 있습니다. 이를 위해 컨트롤러에서 `HasMiddleware` 인터페이스를 구현해야 하며, 이 인터페이스는 컨트롤러가 static `middleware` 메서드를 갖도록 요구합니다. 해당 메서드에서 각 액션에 적용할 미들웨어의 배열을 반환할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

class UserController extends Controller implements HasMiddleware
{
    /**
     * 컨트롤러에 할당될 미들웨어를 반환합니다.
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

또한, 미들웨어를 클로저 형태로 정의하여, 별도의 미들웨어 클래스를 만들지 않고 인라인 미들웨어를 편리하게 사용할 수도 있습니다.

```php
use Closure;
use Illuminate\Http\Request;

/**
 * 컨트롤러에 할당될 미들웨어를 반환합니다.
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

애플리케이션 내 각 Eloquent 모델을 "리소스"로 생각하면, 각 리소스에 대해 일반적으로 동일한 작업을 수행하게 됩니다. 예를 들어, `Photo` 모델과 `Movie` 모델이 있다면, 사용자들은 이 리소스를 생성, 조회, 수정, 삭제할 수 있습니다.

이처럼 자주 쓰이는 CRUD 작업을 위해, 라라벨의 리소스 라우팅은 단 한 줄로 이러한 라우트 전체를 컨트롤러에 연결할 수 있게 해줍니다. `make:controller` 아티즌 명령어의 `--resource` 옵션을 사용해 이런 작업을 처리하는 컨트롤러를 빠르게 만들 수 있습니다.

```shell
php artisan make:controller PhotoController --resource
```

이 명령어는 `app/Http/Controllers/PhotoController.php`에 컨트롤러 파일을 생성합니다. 이 컨트롤러는 각 리소스 작업을 위한 메서드를 포함합니다. 그 다음, 해당 컨트롤러와 연결되는 리소스 라우트를 등록할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 한 줄의 라우트 등록으로 해당 리소스에 대해 다양한 작업을 처리하는 여러 라우트가 만들어집니다. 생성된 컨트롤러에는 이미 각 작업을 위한 메서드의 골격이 포함되어 있습니다. 참고로, 프로젝트 라우트 목록을 빠르게 확인하고 싶다면 `route:list` 아티즌 명령어를 사용할 수 있습니다.

또한, 여러 리소스 컨트롤러를 한 번에 배열로 등록할 수도 있습니다.

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션

<div class="overflow-auto">

| HTTP 메서드 | URI                      | 액션    | 라우트 이름          |
| ---------- | ------------------------ | ------- | -------------------- |
| GET        | `/photos`                | index   | photos.index         |
| GET        | `/photos/create`         | create  | photos.create        |
| POST       | `/photos`                | store   | photos.store         |
| GET        | `/photos/{photo}`        | show    | photos.show          |
| GET        | `/photos/{photo}/edit`   | edit    | photos.edit          |
| PUT/PATCH  | `/photos/{photo}`        | update  | photos.update        |
| DELETE     | `/photos/{photo}`        | destroy | photos.destroy       |

</div>

<a name="customizing-missing-model-behavior"></a>
#### 존재하지 않는 모델 처리 방식 커스터마이징

일반적으로 암묵적(Implicit) 바인딩된 모델이 존재하지 않을 경우, 404 HTTP 응답이 발생합니다. 하지만 `missing` 메서드를 사용하면, 해당 모델을 찾을 수 없을 때 실행할 클로저를 지정하여 동작을 커스터마이즈할 수 있습니다.

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
#### 소프트 삭제(Soft Delete) 모델 처리

기본적으로 암묵적 모델 바인딩은 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)된 모델을 조회하지 않으며, 404 응답을 반환합니다. 그러나 리소스 라우트 등록시 `withTrashed` 메서드를 사용하면 소프트 삭제된 모델도 조회할 수 있게 할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

`withTrashed`에 인자를 전달하지 않으면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델 허용이 활성화됩니다. 특정 라우트만 지정하려면 배열로 전달할 수 있습니다.

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정

[라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 사용할 때, 리소스 컨트롤러 내부에서 모델 인스턴스를 타입힌트 방식으로 주입받고 싶다면 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 리퀘스트(Form Request) 클래스 생성

리소스 컨트롤러를 생성할 때 `--requests` 옵션을 추가하면, 컨트롤러의 저장 및 수정 메서드에 사용할 [폼 리퀘스트 클래스](/docs/12.x/validation#form-request-validation)도 함께 자동 생성됩니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트를 선언할 때, 전체 CRUD 액션 중 일부 액션만 라우트가 작동하도록 지정할 수 있습니다.

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

API에서 사용할 리소스 라우트를 선언할 때는 주로 HTML 템플릿을 반환하는 `create`나 `edit`와 같은 라우트가 필요하지 않을 수 있습니다. 이럴 땐, `apiResource` 메서드를 사용하면 이 두 가지 액션을 자동으로 제외한 라우트를 빠르게 생성할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

여러 API 리소스 컨트롤러 역시 배열로 한 번에 등록할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

또한, 아티즌 명령어에서 `--api` 플래그를 사용하면 `create`와 `edit` 메서드는 포함되지 않는 API 리소스 컨트롤러를 빠르게 생성할 수 있습니다.

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스

경우에 따라서는 중첩된 리소스에 대한 라우트가 필요할 때가 있습니다. 예를 들어, 사진(photos) 리소스 하나에 여러 개의 댓글(comment)이 달릴 수 있습니다. 이런 중첩된 리소스 컨트롤러는 라우트 선언 시 "점(.) 표기법"을 사용해 선언할 수 있습니다.

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 URI로 접근할 수 있는 중첩 리소스를 등록합니다.

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스의 스코핑

라라벨의 [암묵적 모델 바인딩](/docs/12.x/routing#implicit-model-binding-scoping) 기능은, 중첩된(하위) 모델이 실제로 상위 모델에 속하는지 자동으로 확인하는 스코핑을 지원합니다. 라우트 등록 시 `scoped` 메서드를 사용하면 이 기능을 간단히 활성화할 수 있습니다. 또한 어느 필드로 하위 리소스를 조회할지 지정할 수도 있습니다. 자세한 내용은 [리소스 라우트 스코핑](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 얕은(Shallow) 중첩

일부 상황에서는 URI에서 자식 리소스의 ID만 있으면 충분해서, 부모와 자식의 ID를 모두 넣을 필요가 없습니다. 모델의 식별자(예: 자동 증가 PK 등)가 충분히 고유하다면 "얕은 중첩(shallow nesting)"을 사용할 수 있습니다.

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

위와 같이 설정하면 아래와 같은 라우트가 정의됩니다.

<div class="overflow-auto">

| HTTP 메서드 | URI                                   | 액션    | 라우트 이름               |
| ----------- | ------------------------------------- | ------- | ------------------------- |
| GET         | `/photos/{photo}/comments`            | index   | photos.comments.index     |
| GET         | `/photos/{photo}/comments/create`     | create  | photos.comments.create    |
| POST        | `/photos/{photo}/comments`            | store   | photos.comments.store     |
| GET         | `/comments/{comment}`                 | show    | comments.show             |
| GET         | `/comments/{comment}/edit`            | edit    | comments.edit             |
| PUT/PATCH   | `/comments/{comment}`                 | update  | comments.update           |
| DELETE      | `/comments/{comment}`                 | destroy | comments.destroy          |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정

기본적으로 모든 리소스 컨트롤러 액션에는 라우트 이름이 자동으로 지정됩니다. 하지만 원하는 라우트 이름을 부여하고 싶다면 `names` 배열을 전달해 오버라이드할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정

`Route::resource`는 기본적으로 "리소스 이름의 단수형"을 라우트 파라미터 이름으로 사용합니다. 이 파라미터 이름을 변경하고 싶다면 `parameters` 메서드에 배열을 전달하면 됩니다. 배열 형식은 '리소스 이름' => '파라미터 이름' 으로 전달합니다.

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예제에서는 리소스의 `show` 라우트가 아래 URI로 생성됩니다.

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코핑

라라벨의 [스코프드 암묵적 모델 바인딩](/docs/12.x/routing#implicit-model-binding-scoping)은 하위 모델이 실제로 상위 모델에 속하는지 자동으로 스코프를 적용해줍니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면, 자동 스코핑을 활성화하고 어떤 필드 기준으로 하위 리소스를 조회할지 지정할 수 있습니다.

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 다음과 같은 형식의 URI로 접근 가능한 중첩 리소스를 등록합니다.

```text
/photos/{photo}/comments/{comment:slug}
```

커스텀 키가 적용된 암묵적 바인딩을 중첩 라우트 파라미터로 사용할 때, 라라벨은 자동으로 부모를 기준으로 자식 모델을 조회하도록 쿼리를 스코프합니다. 즉, 위 예시에서는 `Photo` 모델이 `comments`라는 관계를 가지고 있다고 가정하여, 해당 관계를 통해 `Comment` 모델을 조회합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화

기본적으로 `Route::resource`는 리소스 URI에서 영어 동사와 복수 규칙을 사용합니다. 만약 `create`, `edit`와 같은 액션 동사를 현지화하려면, `Route::resourceVerbs` 메서드를 사용하면 됩니다. 이 설정은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 초기에 추가할 수 있습니다.

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

라라벨의 복수화(Pluralizer) 기능은 [여러 언어를 지원](/docs/12.x/localization#pluralization-language)하므로, 필요에 맞게 언어를 설정할 수 있습니다. 동사와 복수화 언어가 커스터마이즈된 후에, 예를 들어 `Route::resource('publicacion', PublicacionController::class)`와 같이 리소스 라우트를 등록하면 아래와 같이 현지화된 URI가 생성됩니다.

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보충하기

리소스 컨트롤러에 기본 리소스 라우트 외에 추가적인 라우트를 등록해야 할 때는, 반드시 `Route::resource` 호출 전에 추가 라우트를 정의해야 합니다. 그렇지 않으면 `resource` 메서드의 라우트가 추가 라우트보다 우선 처리되어, 정상 동작하지 않을 수 있습니다.

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러 하나에 너무 많은 역할을 몰아넣지 않는 것이 좋습니다. 만약 자주 기본 리소스 액션 외의 메서드를 추가하게 된다면, 컨트롤러를 두 개 이상의 더 작은 단위로 분리하는 방안을 고려해 주세요.

<a name="singleton-resource-controllers"></a>
### 싱글턴 리소스 컨트롤러

애플리케이션에서 "하나의 인스턴스만 존재"하는 리소스를 다룰 때가 있습니다. 예를 들어, 사용자의 "프로필"은 오직 한 개만 있고, 이미지는 하나의 "썸네일"만 가질 수 있습니다. 이런 케이스에서 이 리소스를 "싱글턴 리소스"라고 부르며, 별도의 식별자가 필요하지 않습니다. 싱글턴 리소스 컨트롤러를 등록하려면 아래와 같이 하면 됩니다.

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위와 같이 등록하면 다음과 같은 라우트가 생성됩니다. 싱글턴 리소스는 생성(create) 관련 라우트가 없고, 식별자 파라미터도 필요 없습니다.

<div class="overflow-auto">

| HTTP 메서드 | URI              | 액션    | 라우트 이름         |
| ----------- | ---------------- | ------- | ------------------- |
| GET         | `/profile`       | show    | profile.show        |
| GET         | `/profile/edit`  | edit    | profile.edit        |
| PUT/PATCH   | `/profile`       | update  | profile.update      |

</div>

표준 리소스 내에 싱글턴 리소스를 중첩시킬 수도 있습니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

위의 경우, `photos` 리소스는 [일반적인 리소스 라우트](#actions-handled-by-resource-controllers)를 모두 갖게 되고, 중첩된 `thumbnail`은 아래와 같은 싱글턴 리소스 라우트를 가집니다.

<div class="overflow-auto">

| HTTP 메서드 | URI                                   | 액션    | 라우트 이름                  |
| ----------- | ------------------------------------- | ------- | ---------------------------- |
| GET         | `/photos/{photo}/thumbnail`           | show    | photos.thumbnail.show        |
| GET         | `/photos/{photo}/thumbnail/edit`      | edit    | photos.thumbnail.edit        |
| PUT/PATCH   | `/photos/{photo}/thumbnail`           | update  | photos.thumbnail.update      |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글턴 리소스

경우에 따라서는 싱글턴 리소스에도 생성 및 저장 라우트가 필요할 수 있습니다. 이럴 때는 싱글턴 라우트 등록 시 `creatable` 메서드를 사용하면 됩니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이렇게 하면 다음과 같은 라우트들이 함께 등록됩니다. 또한, 싱글턴 리소스가 삭제 가능하도록 `DELETE` 라우트도 포함됩니다.

<div class="overflow-auto">

| HTTP 메서드 | URI                                      | 액션     | 라우트 이름                   |
| ----------- | ---------------------------------------- | -------- | ----------------------------- |
| GET         | `/photos/{photo}/thumbnail/create`       | create   | photos.thumbnail.create       |
| POST        | `/photos/{photo}/thumbnail`              | store    | photos.thumbnail.store        |
| GET         | `/photos/{photo}/thumbnail`              | show     | photos.thumbnail.show         |
| GET         | `/photos/{photo}/thumbnail/edit`         | edit     | photos.thumbnail.edit         |
| PUT/PATCH   | `/photos/{photo}/thumbnail`              | update   | photos.thumbnail.update       |
| DELETE      | `/photos/{photo}/thumbnail`              | destroy  | photos.thumbnail.destroy      |

</div>

싱글턴 리소스에 `DELETE` 라우트만 추가하고 싶고, 생성/저장 라우트는 필요 없다면 `destroyable` 메서드를 사용할 수 있습니다.

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글턴 리소스

`apiSingleton` 메서드는 API에서 관리할 싱글턴 리소스를 등록할 때 사용할 수 있으며, 이 메서드를 쓰면 `create`와 `edit` 라우트는 자동으로 제외됩니다.

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론, API용 싱글턴 리소스도 `creatable` 메서드를 같이 사용하면 `store`, `destroy` 라우트가 등록됩니다.

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러

<a name="constructor-injection"></a>
#### 생성자 주입

라라벨의 [서비스 컨테이너](/docs/12.x/container)는 모든 컨트롤러를 자동으로 resolve합니다. 덕분에 컨트롤러 생성자에 필요한 의존성을 타입힌트로 선언하기만 하면, 라라벨이 인스턴스를 자동으로 주입해줍니다.

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
#### 메서드 주입

생성자 주입 외에도, 컨트롤러의 개별 메서드에서도 의존성을 타입힌트하여 주입받을 수 있습니다. 가장 대표적인 예로, 컨트롤러 메서드에서 `Illuminate\Http\Request` 인스턴스를 주입받는 경우가 많습니다.

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

        // 사용자 저장 작업...

        return redirect('/users');
    }
}
```

컨트롤러 메서드에서 라우트 파라미터도 함께 받으려면, 다른 의존성 뒤에 라우트 인자를 나열하면 됩니다. 예를 들어, 아래와 같이 라우트를 정의했다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

아래처럼 컨트롤러 메서드에서 `Illuminate\Http\Request`와 `id` 파라미터를 함께 받을 수 있습니다.

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
        // 사용자 업데이트 작업...

        return redirect('/users');
    }
}
```