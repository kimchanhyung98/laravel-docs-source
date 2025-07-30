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
    - [싱글톤 리소스 컨트롤러](#singleton-resource-controllers)
- [종속성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개 (Introduction)

라우트 파일에서 모든 요청 처리 로직을 클로저로 정의하는 대신, "컨트롤러" 클래스를 사용해 관련된 요청 처리 로직을 한 클래스로 조직할 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청, 즉 사용자 조회, 생성, 수정, 삭제 요청을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기 (Writing Controllers)

<a name="basic-controllers"></a>
### 기본 컨트롤러 (Basic Controllers)

새 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 실행하세요. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다:

```shell
php artisan make:controller UserController
```

기본 컨트롤러 예제를 살펴보겠습니다. 컨트롤러는 들어오는 HTTP 요청에 대응하는 여러 public 메서드를 가질 수 있습니다:

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

컨트롤러 클래스와 메서드를 작성했다면, 다음과 같이 라우트에서 컨트롤러 메서드를 지정할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

지정된 라우트 URI에 들어오는 요청이 매칭되면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고 라우트 파라미터가 메서드에 전달됩니다.

> [!NOTE]
> 컨트롤러는 기본 클래스를 상속받아야 하는 것이 **필수**는 아닙니다. 하지만 모든 컨트롤러에서 공유할 메서드를 포함하는 기본 컨트롤러 클래스를 상속받는 것이 편리할 때가 있습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러 (Single Action Controllers)

특정 컨트롤러 액션이 매우 복잡하다면, 그 액션 전용 컨트롤러 클래스를 만드는 것이 편리할 수 있습니다. 이를 위해 컨트롤러 내에 단일 `__invoke` 메서드를 정의할 수 있습니다:

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

단일 액션 컨트롤러의 라우트를 등록할 때는 메서드를 지정할 필요 없이 컨트롤러 이름만 전달하면 됩니다:

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` Artisan 명령어의 `--invokable` 옵션을 사용하면 단일 액션 컨트롤러를 생성할 수 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁은 [스텁 퍼블리싱](/docs/master/artisan#stub-customization)을 통해 사용자 정의할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어 (Controller Middleware)

[미들웨어](/docs/master/middleware)는 라우트 파일에서 컨트롤러 라우트에 할당할 수 있습니다:

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

또는 컨트롤러 클래스 내에서 미들웨어를 지정하는 것이 편리할 수 있습니다. 이를 위해 컨트롤러는 `HasMiddleware` 인터페이스를 구현해야 하며, 이 인터페이스는 컨트롤러가 정적 `middleware` 메서드를 가져야 함을 명시합니다. 이 메서드에서 컨트롤러의 액션에 적용되는 미들웨어 배열을 반환할 수 있습니다:

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

컨트롤러 미들웨어를 클로저로도 정의할 수 있는데, 이는 전체 미들웨어 클래스를 작성하지 않고 인라인 미들웨어를 정의하는 편리한 방법입니다:

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
> `Illuminate\Routing\Controllers\HasMiddleware`를 구현하는 컨트롤러는 `Illuminate\Routing\Controller`를 상속받지 않아야 합니다.

<a name="resource-controllers"></a>
## 리소스 컨트롤러 (Resource Controllers)

애플리케이션 내 각 Eloquent 모델을 "리소스"로 생각할 때, 보통 각 리소스에 대해 생성, 조회, 수정, 삭제(“CRUD”) 작업이 공통적으로 수행됩니다. 예를 들어 `Photo` 모델과 `Movie` 모델이 있다고 하면, 사용자는 이 리소스들을 생성, 조회, 수정, 삭제할 수 있을 것입니다.

이런 일반적인 상황을 위해 Laravel은 한 줄의 코드로 컨트롤러에 CRUD 라우트를 자동 할당하는 리소스 라우팅을 제공합니다. 시작하려면 `make:controller` Artisan 명령어의 `--resource` 옵션으로 이 액션들을 처리하는 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

이 명령은 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성하고, 각 리소스 작업에 해당하는 메서드를 포함합니다. 그 다음 리소스 라우트를 다음과 같이 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 단일 라우트 선언은 리소스의 여러 작업을 처리하는 여러 라우트를 자동으로 생성합니다. 생성된 컨트롤러에는 각 작업용 메서드 스텁이 포함되어 있습니다. 애플리케이션 라우트를 빠르게 확인하려면 `route:list` Artisan 명령어를 실행하세요.

여러 리소스 컨트롤러를 동시에 등록할 수도 있습니다:

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션

<div class="overflow-auto">

| HTTP 메서드 | URI                    | 액션    | 라우트 이름        |
| --------- | ---------------------- | ------- | -------------- |
| GET       | `/photos`              | index   | photos.index   |
| GET       | `/photos/create`       | create  | photos.create  |
| POST      | `/photos`              | store   | photos.store   |
| GET       | `/photos/{photo}`      | show    | photos.show    |
| GET       | `/photos/{photo}/edit` | edit    | photos.edit    |
| PUT/PATCH | `/photos/{photo}`      | update  | photos.update  |
| DELETE    | `/photos/{photo}`      | destroy | photos.destroy |

</div>

<a name="customizing-missing-model-behavior"></a>
#### 모델 미발견 동작 커스터마이징

암묵적 바인딩한 리소스 모델을 찾을 수 없으면 기본적으로 404 HTTP 응답을 반환합니다. 하지만 `missing` 메서드를 사용해 이를 커스터마이징할 수 있습니다. `missing`은 리소스의 라우트 중 암묵적으로 바인딩된 모델을 찾지 못했을 때 호출할 클로저를 받습니다:

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

암묵적 모델 바인딩은 기본적으로 [소프트 삭제](/docs/master/eloquent#soft-deleting)된 모델을 조회하지 않고 404 응답을 반환합니다. 그러나 `withTrashed` 메서드를 호출하면 소프트 삭제된 모델도 허용하도록 설정할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

`withTrashed`를 인자 없이 호출하면 `show`, `edit`, `update` 리소스 라우트에 대해 소프트 삭제 모델을 허용합니다. 특정 라우트만 지정하려면 배열을 인자로 넘길 수 있습니다:

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정하기

[라우트 모델 바인딩](/docs/master/routing#route-model-binding)을 사용하는 경우 리소스 컨트롤러 메서드에 모델 인스턴스를 타입 힌트하려면 `--model` 옵션을 사용해 컨트롤러를 생성하세요:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 요청 생성하기

리소스 컨트롤러를 생성할 때 `--requests` 옵션을 제공하면 저장 및 업데이트 메서드용 [폼 요청 클래스](/docs/master/validation#form-request-validation)도 함께 생성하도록 Artisan에 지시할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트 (Partial Resource Routes)

리소스 라우트를 선언할 때, 컨트롤러가 처리할 액션의 일부만 지정할 수도 있습니다:

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

API에서 소비되는 리소스 라우트의 경우, `create`와 `edit`처럼 HTML 템플릿을 표시하는 라우트를 제외하고 싶을 때가 많습니다. 이런 경우 `apiResource` 메서드를 사용해 이 두 라우트를 자동으로 제외할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

여러 API 리소스 컨트롤러를 한꺼번에 등록하려면 `apiResources` 메서드에 배열을 전달하세요:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`create`와 `edit` 메서드가 포함되지 않은 API 리소스 컨트롤러를 빠르게 생성하려면 `make:controller` 명령어 실행 시 `--api` 스위치를 사용하세요:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스 (Nested Resources)

때때로 중첩된 리소스에 대한 라우트를 정의해야 할 수 있습니다. 예를 들어, `Photo` 리소스에 여러 댓글(`comments`)이 달려 있을 경우, 라우트 선언에 점(dot) 표기법을 사용해 중첩 리소스 컨트롤러를 지정할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 URI로 접근 가능한 중첩 리소스를 등록합니다:

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 스코핑

Laravel의 [암묵적 모델 바인딩](/docs/master/routing#implicit-model-binding-scoping) 기능은 중첩 바인딩을 자동으로 스코핑하여, 하위 모델이 부모 모델에 속하는지 확인할 수 있습니다. 중첩 리소스 정의 시 `scoped` 메서드를 사용하면 자동 스코핑과 함께 하위 리소스를 조회할 필드를 지정할 수 있습니다. 자세한 내용은 [리소스 라우트 스코핑](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 얕은 중첩 (Shallow Nesting)

부모 ID와 자식 ID를 URI에 모두 포함하는 것이 꼭 항상 필요한 것은 아닙니다. 대부분 자식 ID는 고유 식별자이므로 자식 리소스를 식별하는 데 충분합니다. 자동 증가 기본 키 같은 고유 식별자를 URI 세그먼트로 사용할 경우, 얕은 중첩을 사용하는 것이 좋습니다:

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

위 선언은 다음과 같은 라우트를 생성합니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                               | 액션    | 라우트 이름              |
| --------- | --------------------------------- | ------- | ----------------------- |
| GET       | `/photos/{photo}/comments`        | index   | photos.comments.index  |
| GET       | `/photos/{photo}/comments/create` | create  | photos.comments.create |
| POST      | `/photos/{photo}/comments`        | store   | photos.comments.store  |
| GET       | `/comments/{comment}`             | show    | comments.show          |
| GET       | `/comments/{comment}/edit`        | edit    | comments.edit          |
| PUT/PATCH | `/comments/{comment}`             | update  | comments.update        |
| DELETE    | `/comments/{comment}`             | destroy | comments.destroy       |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정 (Naming Resource Routes)

기본적으로 모든 리소스 컨트롤러 액션에는 라우트 이름이 지정되지만, `names` 배열을 전달해 원하는 라우트 이름으로 덮어쓸 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정 (Naming Resource Route Parameters)

기본적으로 `Route::resource`는 리소스 이름의 단수형을 기준으로 라우트 파라미터를 생성합니다. 이를 리소스별로 쉽게 덮어쓰려면 `parameters` 메서드를 사용하세요. `parameters` 메서드에 전달하는 배열은 리소스 이름과 파라미터 이름의 연관 배열이어야 합니다:

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예시는 리소스의 `show` 라우트를 다음 URI로 생성합니다:

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코핑 (Scoping Resource Routes)

Laravel의 [스코프가 지정된 암묵적 모델 바인딩](/docs/master/routing#implicit-model-binding-scoping)은 중첩 바인딩을 자동으로 스코핑하여 하위 모델이 부모 모델에 속하는지 확인합니다. `scoped` 메서드 사용 시, 하위 리소스를 조회할 필드를 지정하면서 자동 스코핑을 활성화할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 다음과 같이 접근할 수 있는 스코프 지정 중첩 리소스를 등록합니다:

```text
/photos/{photo}/comments/{comment:slug}
```

중첩 라우트 파라미터에 커스텀 키 암묵 바인딩을 사용할 때, Laravel은 부모 모델의 관계 이름을 추론해 하위 모델을 스코프 내에서 조회합니다. 이 예에서는 `Photo` 모델이 `comments`라는 관계를 가지고 있어 `Comment` 모델을 조회하는 데 사용한다고 가정합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화 (Localizing Resource URIs)

기본적으로 `Route::resource`는 영어 동사 및 복수 규칙을 따르는 URI를 생성합니다. `create`와 `edit` 액션 동사를 현지화하려면 애플리케이션의 `App\Providers\AppServiceProvider` 내 `boot` 메서드 시작 부분에 `Route::resourceVerbs` 메서드를 사용하세요:

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

Laravel의 복수형 변환기는 [여러 언어를 지원하며 필요에 따라 구성 가능합니다](/docs/master/localization#pluralization-language). 따라서 동사와 복수형이 커스터마이징되면 다음과 같이 `Route::resource('publicacion', PublicacionController::class)` 선언이 URI들을 만듭니다:

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보완 (Supplementing Resource Controllers)

기본 리소스 라우트 집합에 더해 추가 라우트를 등록해야 할 경우, `Route::resource` 호출 전에 별도의 라우트를 먼저 정의해야 합니다. 그렇지 않으면 리소스 라우트가 보완 라우트를 덮어쓸 수 있습니다:

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러를 집중적으로 관리하세요. 기본적인 리소스 작업 이외 메서드를 자주 추가해야 한다면, 컨트롤러를 둘 이상의 더 작은 컨트롤러로 분리하는 것을 고려하세요.

<a name="singleton-resource-controllers"></a>
### 싱글톤 리소스 컨트롤러 (Singleton Resource Controllers)

때때로 애플리케이션에는 단 하나의 인스턴스만 가질 수 있는 리소스가 있습니다. 예를 들어 사용자의 "프로필"은 수정할 수 있지만 두 개 이상을 가질 수 없습니다. 이미지에 하나뿐인 "썸네일"이 있을 수도 있습니다. 이러한 리소스를 "싱글톤 리소스"라고 하며, 하나의 인스턴스만 존재할 수 있습니다. 이런 경우 싱글톤 리소스 컨트롤러를 등록할 수 있습니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위 싱글톤 리소스 정의는 다음과 같은 라우트를 등록합니다. 생성 경로는 등록되지 않으며, 리소스가 하나뿐이므로 식별자를 받지 않습니다:

<div class="overflow-auto">

| HTTP 메서드 | URI             | 액션   | 라우트 이름     |
| --------- | --------------- | ------ | -------------- |
| GET       | `/profile`      | show   | profile.show   |
| GET       | `/profile/edit` | edit   | profile.edit   |
| PUT/PATCH | `/profile`      | update | profile.update |

</div>

싱글톤 리소스는 종종 표준 리소스 내에 중첩되기도 합니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 경우 `photos`는 [표준 리소스 라우트](#actions-handled-by-resource-controllers)를 갖고, `thumbnail`은 다음의 싱글톤 리소스 라우트를 가집니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                              | 액션   | 라우트 이름              |
| --------- | -------------------------------- | ------ | ----------------------- |
| GET       | `/photos/{photo}/thumbnail`      | show   | photos.thumbnail.show   |
| GET       | `/photos/{photo}/thumbnail/edit` | edit   | photos.thumbnail.edit   |
| PUT/PATCH | `/photos/{photo}/thumbnail`      | update | photos.thumbnail.update |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글톤 리소스 (Creatable Singleton Resources)

때때로 싱글톤 리소스에도 생성 및 저장 라우트를 정의하고 싶을 수 있습니다. 이럴 때는 싱글톤 리소스 등록 시 `creatable` 메서드를 호출하세요:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이 경우 다음 라우트가 등록됩니다. `DELETE` 라우트도 함께 등록된 점에 주의하세요:

<div class="overflow-auto">

| HTTP 메서드 | URI                                | 액션   | 라우트 이름               |
| --------- | ---------------------------------- | ------ | ------------------------ |
| GET       | `/photos/{photo}/thumbnail/create` | create | photos.thumbnail.create  |
| POST      | `/photos/{photo}/thumbnail`        | store  | photos.thumbnail.store   |
| GET       | `/photos/{photo}/thumbnail`        | show   | photos.thumbnail.show    |
| GET       | `/photos/{photo}/thumbnail/edit`   | edit   | photos.thumbnail.edit    |
| PUT/PATCH | `/photos/{photo}/thumbnail`        | update | photos.thumbnail.update  |
| DELETE    | `/photos/{photo}/thumbnail`        | destroy| photos.thumbnail.destroy |

</div>

생성 및 저장 라우트 대신 `DELETE` 라우트만 등록하려면 `destroyable` 메서드를 사용하세요:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글톤 리소스 (API Singleton Resources)

`apiSingleton` 메서드는 API를 통해 조작되는 싱글톤 리소스를 등록할 때 사용합니다. 이 경우 `create`와 `edit` 라우트는 필요 없으므로 자동 제외됩니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론, API 싱글톤 리소스에도 `creatable`을 붙여 `store`와 `destroy` 라우트를 등록할 수 있습니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
## 종속성 주입과 컨트롤러 (Dependency Injection and Controllers)

<a name="constructor-injection"></a>
#### 생성자 주입 (Constructor Injection)

Laravel의 [서비스 컨테이너](/docs/master/container)는 모든 컨트롤러를 해결하는 데 사용되므로, 컨트롤러 생성자에서 필요한 의존성을 타입 힌트하면 자동으로 해결되어 주입됩니다:

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
#### 메서드 주입 (Method Injection)

생성자 주입 외에도, 컨트롤러 메서드의 파라미터로도 의존성을 타입 힌트할 수 있습니다. 일반적으로 `Illuminate\Http\Request` 인스턴스를 컨트롤러 메서드에 주입할 때 많이 쓰입니다:

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

        // 사용자를 저장하는 로직...

        return redirect('/users');
    }
}
```

컨트롤러 메서드가 라우트 파라미터 입력도 기대한다면, 다른 의존성 뒤에 라우트 인자를 나열하면 됩니다. 예를 들어 다음 라우트가 있다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

다음과 같이 컨트롤러 메서드를 정의해 `Illuminate\Http\Request`를 타입 힌트하고 `id` 파라미터도 받을 수 있습니다:

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
        // 사용자를 업데이트하는 로직...

        return redirect('/users');
    }
}
```