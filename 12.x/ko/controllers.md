# 컨트롤러 (Controllers)

- [소개](#introduction)
- [컨트롤러 작성하기](#writing-controllers)
    - [기본 컨트롤러](#basic-controllers)
    - [싱글 액션 컨트롤러](#single-action-controllers)
- [컨트롤러 미들웨어](#controller-middleware)
- [리소스 컨트롤러](#resource-controllers)
    - [부분 리소스 라우트](#restful-partial-resource-routes)
    - [중첩 리소스](#restful-nested-resources)
    - [리소스 라우트 이름 지정](#restful-naming-resource-routes)
    - [리소스 라우트 파라미터 이름 지정](#restful-naming-resource-route-parameters)
    - [리소스 라우트 스코핑](#restful-scoping-resource-routes)
    - [리소스 URI 현지화](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 보완하기](#restful-supplementing-resource-controllers)
    - [싱글톤 리소스 컨트롤러](#singleton-resource-controllers)
    - [미들웨어와 리소스 컨트롤러](#middleware-and-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개

모든 요청 처리 로직을 라우트 파일에서 클로저로 정의하는 대신, "컨트롤러" 클래스를 사용하여 이러한 동작을 체계적으로 관리할 수 있습니다. 컨트롤러는 관련 요청 처리 로직을 하나의 클래스로 묶을 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청 처리(사용자 조회, 생성, 수정, 삭제 등)를 담당할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기

<a name="basic-controllers"></a>
### 기본 컨트롤러

새 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 사용할 수 있습니다. 기본적으로 모든 애플리케이션 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다:

```shell
php artisan make:controller UserController
```

기본 컨트롤러 예제를 살펴보겠습니다. 컨트롤러는 HTTP 요청에 응답하는 임의 개수의 public 메서드를 가질 수 있습니다:

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

컨트롤러 클래스와 메서드를 작성한 후에는 다음과 같이 컨트롤러 메서드에 응답하는 라우트를 정의할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

들어오는 요청이 지정한 라우트 URI와 일치하면 `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고, 라우트 파라미터가 해당 메서드에 전달됩니다.

> [!NOTE]
> 컨트롤러가 반드시 기본 클래스를 상속받아야 하는 것은 아닙니다. 다만, 모든 컨트롤러에 공통으로 사용할 메서드를 포함하는 기본 컨트롤러 클래스를 상속받으면 편리한 경우가 있습니다.

<a name="single-action-controllers"></a>
### 싱글 액션 컨트롤러

컨트롤러 액션이 매우 복잡한 경우, 단일 액션에 전용 컨트롤러 클래스를 사용하는 것이 편리할 수 있습니다. 이를 위해 컨트롤러 내에 단 하나의 `__invoke` 메서드를 정의할 수 있습니다:

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

싱글 액션 컨트롤러에 대한 라우트를 등록할 때는 컨트롤러 메서드를 지정할 필요 없이, 컨트롤러 클래스 이름만 라우터에 전달하면 됩니다:

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` Artisan 명령어의 `--invokable` 옵션을 사용하여 인보커블 컨트롤러를 생성할 수 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁은 [stub publishing](/docs/12.x/artisan#stub-customization)를 통해 커스터마이징할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

라우트 파일 내에서 컨트롤러의 라우트에 미들웨어를 할당할 수 있습니다:

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

또한 컨트롤러 클래스 내에서 미들웨어를 지정하는 것이 편리할 수 있습니다. 이를 위해 컨트롤러는 `HasMiddleware` 인터페이스를 구현해야 하며, 해당 인터페이스는 정적 메서드 `middleware`를 정의하도록 요구합니다. 이 메서드 내부에서 컨트롤러 액션에 적용할 미들웨어 배열을 반환할 수 있습니다:

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

컨트롤러 미들웨어는 클래스를 작성하지 않고 클로저로 정의할 수도 있습니다. 이렇게 하면 간단한 인라인 미들웨어를 쉽게 구현할 수 있습니다:

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
## 리소스 컨트롤러

애플리케이션 내 각 Eloquent 모델을 "리소스"라고 생각할 때, 일반적으로 각 리소스에 대해 동일한 CRUD 작업(생성, 조회, 수정, 삭제)을 수행합니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다면 사용자가 이 리소스들을 생성, 조회, 수정, 삭제할 수 있을 것입니다.

이러한 공통 사례 때문에, Laravel은 리소스 라우팅을 통해 단 한 줄의 코드로 컨트롤러에 CRUD 라우트를 할당합니다. 시작하려면 `make:controller` Artisan 명령어의 `--resource` 옵션을 통해 이 작업을 처리하는 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

이 명령어는 `app/Http/Controllers/PhotoController.php` 위치에 컨트롤러를 생성하며, 해당 컨트롤러에는 리소스 작업별로 메서드가 미리 작성되어 있습니다. 다음으로 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 라우트 선언 하나가 해당 리소스에 다양한 작업을 처리하는 여러 라우트를 생성합니다. 생성된 컨트롤러는 이러한 작업 각각에 대한 메서드를 기본으로 제공합니다. `route:list` Artisan 명령어를 통해 애플리케이션 라우트를 빠르게 확인할 수 있습니다.

여러 리소스 컨트롤러도 배열로 한번에 등록할 수 있습니다:

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션

<div class="overflow-auto">

| HTTP 동사  | URI                     | 액션    | 라우트 이름          |
| ---------- | ----------------------- | ------- | -------------------- |
| GET        | `/photos`               | index   | photos.index         |
| GET        | `/photos/create`        | create  | photos.create        |
| POST       | `/photos`               | store   | photos.store         |
| GET        | `/photos/{photo}`       | show    | photos.show          |
| GET        | `/photos/{photo}/edit`  | edit    | photos.edit          |
| PUT/PATCH  | `/photos/{photo}`       | update  | photos.update        |
| DELETE     | `/photos/{photo}`       | destroy | photos.destroy       |

</div>

<a name="customizing-missing-model-behavior"></a>
#### 모델 미발견 시 동작 커스터마이징

암묵적 바인딩된 리소스 모델을 찾지 못하면 기본적으로 404 HTTP 응답이 반환됩니다. 그러나 리소스 라우트를 정의할 때 `missing` 메서드를 호출해 이 동작을 사용자 지정할 수 있습니다. `missing` 메서드는 암묵적 바인딩된 모델을 찾지 못했을 때 실행할 클로저를 받습니다:

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
#### Soft Deleted(소프트 삭제) 모델

암묵적 모델 바인딩은 기본적으로 [soft delete](/docs/12.x/eloquent#soft-deleting) 처리된 모델은 조회하지 않고 404 HTTP 응답을 반환합니다. 하지만 `withTrashed` 메서드를 호출하여 소프트 삭제된 모델을 포함하도록 할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

`withTrashed` 메서드를 인자 없이 호출하면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델을 허용합니다. 선택적으로 조회할 라우트 목록을 배열로 지정할 수도 있습니다:

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정하기

[라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 사용하면서 리소스 컨트롤러 메서드에서 모델 타입 힌트를 사용하고 싶다면, 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 요청 클래스 생성하기

`--requests` 옵션을 제공하면, 컨트롤러의 저장 및 업데이트 메서드에 사용할 [폼 요청 클래스](/docs/12.x/validation#form-request-validation)를 자동 생성하도록 Artisan에 지시할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트를 선언할 때 컨트롤러가 처리할 작업 세트를 기본 동작 전체가 아니라 일부만 지정할 수 있습니다:

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

API용 리소스 라우트를 선언할 경우 `create`와 `edit`처럼 HTML 뷰를 제공하는 라우트를 제외하는 경우가 많습니다. 이를 편리하게 처리하는 `apiResource` 메서드를 제공하며, 다음과 같이 사용할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

여러 API 리소스 컨트롤러를 배열로 한번에 등록할 수도 있습니다:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`create`나 `edit` 메서드를 포함하지 않는 API 리소스 컨트롤러를 빠르게 생성하려면 `make:controller` 명령어에 `--api` 옵션을 붙여 실행하세요:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스

리소스가 다른 리소스에 중첩되어 있을 때 라우트를 정의할 수 있습니다. 예를 들어, 사진에는 여러 코멘트가 붙을 수 있습니다. 중첩 리소스 컨트롤러는 다음과 같이 '점(dot)' 표기법으로 선언합니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 경우 다음과 같은 경로를 갖는 중첩 리소스가 등록됩니다:

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 스코핑

Laravel의 [암묵적 모델 바인딩 스코핑](/docs/12.x/routing#implicit-model-binding-scoping)을 활용하면, 자식 모델이 반드시 부모 모델에 속하는지 자동으로 확인하는 범위를 설정할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 호출해 자동 스코핑을 활성화하고 자식 리소스를 식별할 필드도 지정할 수 있습니다. 자세한 내용은 [리소스 라우트 스코핑](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 얕은 중첩(Shallow Nesting)

URI에 부모와 자식 ID가 모두 필요하지 않은 경우가 많습니다. 예를 들어, 자식 ID가 이미 고유 식별자라면 URI가 길어질 필요가 없기 때문입니다. 기본키 등 고유 식별자를 사용하는 경우 "얕은 중첩"을 적용할 수 있습니다:

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

이 선언에 의해 다음과 같은 라우트들이 등록됩니다:

<div class="overflow-auto">

| HTTP 동사  | URI                             | 액션    | 라우트 이름              |
| ---------- | -------------------------------| ------- | ------------------------ |
| GET        | `/photos/{photo}/comments`     | index   | photos.comments.index    |
| GET        | `/photos/{photo}/comments/create` | create  | photos.comments.create   |
| POST       | `/photos/{photo}/comments`     | store   | photos.comments.store    |
| GET        | `/comments/{comment}`          | show    | comments.show            |
| GET        | `/comments/{comment}/edit`     | edit    | comments.edit            |
| PUT/PATCH  | `/comments/{comment}`          | update  | comments.update          |
| DELETE     | `/comments/{comment}`          | destroy | comments.destroy         |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정

기본적으로 모든 리소스 컨트롤러 액션은 라우트 이름이 생성됩니다. 하지만 `names` 배열을 전달해 원하는 라우트 이름을 덮어쓸 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정

기본적으로 `Route::resource`는 리소스 이름의 단수형을 기준으로 라우트 파라미터 이름을 생성합니다. 이는 `parameters` 메서드로 쉽게 덮어쓸 수 있으며, 파라미터 이름들을 연관 배열 형태로 지정합니다:

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예제에서 `show` 라우트의 URI는 다음과 같이 생성됩니다:

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코핑

Laravel의 [스코프가 지정된 암묵적 모델 바인딩](/docs/12.x/routing#implicit-model-binding-scoping) 기능은 중첩 바인딩이 부모 모델에 속하는 자식 모델임을 자동으로 확인하도록 만듭니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하여 스코핑을 활성화하고 자식 리소스를 조회할 필드를 지정할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 다음과 같은 중첩 스코핑된 리소스를 등록합니다:

```text
/photos/{photo}/comments/{comment:slug}
```

커스텀 키 드 암묵적 바인딩을 중첩 라우트 파라미터로 사용하면, Laravel이 부모 모델의 관계 이름을 컨벤션에 따라 추론하여 자식 모델을 부모를 기준으로 자동 쿼리합니다. 예를 들어, `Photo` 모델에 `comments` 관계(라우트 파라미터명 복수형)가 존재하는 것으로 가정합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화

기본적으로 `Route::resource`는 영어 동사와 복수 규칙에 따라 리소스 URI를 생성합니다. `create`와 `edit` 같은 액션용 동사를 현지화하려면 `Route::resourceVerbs` 메서드를 사용할 수 있습니다. 이 설정은 애플리케이션의 `App\Providers\AppServiceProvider` 내 `boot` 메서드 시작 부분에서 적용할 수 있습니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);
}
```

Laravel의 복수화기는 [필요에 따라 여러 언어를 지원하도록 설정할 수 있습니다](/docs/12.x/localization#pluralization-language). 동사와 복수화 언어를 지정한 후 `Route::resource('publicacion', PublicacionController::class)` 같은 리소스 라우트를 등록하면 다음과 같은 URI를 생성합니다:

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보완하기

디폴트 리소스 라우트 집합을 넘어서 추가 라우트를 리소스 컨트롤러에 더해야 할 경우, `Route::resource` 호출보다 앞서 해당 라우트를 정의해야 합니다. 그렇지 않으면 `resource` 메서드로 정의된 라우트가 추가 라우트보다 우선 적용되어 의도치 않은 작동이 일어날 수 있습니다:

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러가 너무 많은 책임을 가지는 것을 피하세요. 리소스 액션 외에 자주 추가 메서드가 필요하다면, 컨트롤러를 두 개 이상의 작은 컨트롤러로 분리하는 것이 좋습니다.

<a name="singleton-resource-controllers"></a>
### 싱글톤 리소스 컨트롤러

애플리케이션에서 단 하나만 존재해야 하는 리소스가 있을 수 있습니다. 예를 들어, 사용자의 "프로필"은 하나만 존재하며, 여러 개가 있을 수 없습니다. 이미지가 단일 "썸네일"을 가질 수도 있습니다. 이런 리소스를 "싱글톤 리소스"라고 부르며, 한정된 인스턴스만 존재함을 의미합니다. 이러한 경우 "싱글톤" 리소스 컨트롤러를 등록할 수 있습니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위 싱글톤 리소스 정의는 다음 라우트를 등록합니다. 싱글톤 리소스에는 생성 라우트가 없고, 인스턴스가 하나뿐이라 식별자를 받지 않습니다:

<div class="overflow-auto">

| HTTP 동사  | URI           | 액션   | 라우트 이름      |
| ---------- | ------------- | ------ | ---------------- |
| GET        | `/profile`    | show   | profile.show     |
| GET        | `/profile/edit` | edit   | profile.edit     |
| PUT/PATCH  | `/profile`    | update | profile.update   |

</div>

싱글톤 리소스는 일반 리소스 내 중첩도 가능합니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 예시에서 `photos` 리소스는 [표준 리소스 라우트](#actions-handled-by-resource-controllers)를 갖고, `thumbnail`은 싱글톤 리소스로 다음과 같은 라우트가 등록됩니다:

<div class="overflow-auto">

| HTTP 동사  | URI                             | 액션   | 라우트 이름             |
| ---------- | -------------------------------| ------ | ----------------------- |
| GET        | `/photos/{photo}/thumbnail`     | show   | photos.thumbnail.show   |
| GET        | `/photos/{photo}/thumbnail/edit` | edit   | photos.thumbnail.edit   |
| PUT/PATCH  | `/photos/{photo}/thumbnail`     | update | photos.thumbnail.update |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글톤 리소스

싱글톤 리소스에 생성(create)과 저장(store) 라우트를 정의하고 싶을 때에는 `creatable` 메서드를 호출합니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이 경우 다음과 같은 라우트가 등록됩니다. 생성 가능한 싱글톤 리소스에는 삭제(Delete) 라우트도 함께 등록됩니다:

<div class="overflow-auto">

| HTTP 동사  | URI                               | 액션    | 라우트 이름               |
| ---------- | ---------------------------------| ------- | ------------------------- |
| GET        | `/photos/{photo}/thumbnail/create` | create  | photos.thumbnail.create   |
| POST       | `/photos/{photo}/thumbnail`       | store   | photos.thumbnail.store    |
| GET        | `/photos/{photo}/thumbnail`       | show    | photos.thumbnail.show     |
| GET        | `/photos/{photo}/thumbnail/edit`  | edit    | photos.thumbnail.edit     |
| PUT/PATCH  | `/photos/{photo}/thumbnail`       | update  | photos.thumbnail.update   |
| DELETE     | `/photos/{photo}/thumbnail`       | destroy | photos.thumbnail.destroy  |

</div>

`DELETE` 라우트만 등록하고 생성과 저장 라우트는 등록하지 않으려면 `destroyable` 메서드를 사용할 수 있습니다:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글톤 리소스

`apiSingleton` 메서드를 사용하면 싱글톤 리소스를 API로 다룰 때 필요 없는 `create`와 `edit` 라우트를 제외하고 등록할 수 있습니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론 API 싱글톤 리소스에도 `creatable` 옵션을 붙여 `store`와 `destroy` 라우트를 함께 등록할 수 있습니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="middleware-and-resource-controllers"></a>
### 미들웨어와 리소스 컨트롤러

Laravel은 리소스 라우트의 모든 메서드에 미들웨어를 할당하거나, 특정 메서드에만 미들웨어를 적용하거나 특정 메서드에서 미들웨어를 제외할 수 있는 메서드(`middleware`, `middlewareFor`, `withoutMiddlewareFor`)를 제공합니다. 이를 통해 각 리소스 액션별 미들웨어 적용을 세밀하게 제어할 수 있습니다.

#### 모든 메서드에 미들웨어 적용하기

`middleware` 메서드를 사용해 리소스 또는 싱글톤 리소스 라우트가 생성하는 모든 라우트에 미들웨어를 적용할 수 있습니다:

```php
Route::resource('users', UserController::class)
    ->middleware(['auth', 'verified']);

Route::singleton('profile', ProfileController::class)
    ->middleware('auth');
```

#### 특정 메서드에 미들웨어 적용하기

`middlewareFor` 메서드로 특정 메서드 하나 이상에 미들웨어를 할당할 수 있습니다:

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

`middlewareFor`는 싱글톤 및 API 싱글톤 리소스 컨트롤러에도 동일하게 적용할 수 있습니다:

```php
Route::singleton('profile', ProfileController::class)
    ->middlewareFor('show', 'auth');

Route::apiSingleton('profile', ProfileController::class)
    ->middlewareFor(['show', 'update'], 'auth');
```

#### 특정 메서드에서 미들웨어 제외하기

`withoutMiddlewareFor` 메서드를 사용하면 특정 메서드에서 미들웨어를 제외할 수 있습니다:

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

Laravel의 [서비스 컨테이너](/docs/12.x/container)는 모든 Laravel 컨트롤러를 해결(인스턴스화)하는 데 사용됩니다. 따라서 컨트롤러 생성자에 필요한 의존성을 타입 힌트하면, 자동으로 컨테이너가 관련 인스턴스를 주입해 줍니다:

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

생성자 주입 외에도, 컨트롤러 메서드 내에서 의존성을 타입 힌트해 주입받을 수 있습니다. 가장 흔한 용도는 컨트롤러 메서드에서 `Illuminate\Http\Request` 인스턴스를 주입받는 것입니다:

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

        // 사용자 저장 처리...

        return redirect('/users');
    }
}
```

컨트롤러 메서드가 라우트 파라미터도 기대하는 경우, 의존성 타입 힌트 뒤에 라우트 인수를 나열하면 됩니다. 예를 들어, 다음과 같은 라우트 정의가 있다고 가정하세요:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메서드는 다음과 같이 정의할 수 있습니다:

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
        // 사용자 정보 업데이트...

        return redirect('/users');
    }
}
```