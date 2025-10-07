# 컨트롤러 (Controllers)

- [소개](#introduction)
- [컨트롤러 작성](#writing-controllers)
    - [기본 컨트롤러](#basic-controllers)
    - [단일 액션 컨트롤러](#single-action-controllers)
- [컨트롤러 미들웨어](#controller-middleware)
- [리소스 컨트롤러](#resource-controllers)
    - [일부 리소스 라우트 등록](#restful-partial-resource-routes)
    - [중첩 리소스](#restful-nested-resources)
    - [리소스 라우트 이름 지정](#restful-naming-resource-routes)
    - [리소스 라우트 파라미터 이름 지정](#restful-naming-resource-route-parameters)
    - [리소스 라우트 스코핑](#restful-scoping-resource-routes)
    - [리소스 URI 현지화](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 보완](#restful-supplementing-resource-controllers)
    - [싱글턴 리소스 컨트롤러](#singleton-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개 (Introduction)

라우트 파일에서 모든 요청 처리 로직을 클로저로 정의하는 대신, "컨트롤러" 클래스를 사용해 이러한 동작을 구조화할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스로 묶어 관리할 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청(조회, 생성, 수정, 삭제 등)을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성 (Writing Controllers)

<a name="basic-controllers"></a>
### 기본 컨트롤러 (Basic Controllers)

새로운 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 실행합니다. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

```shell
php artisan make:controller UserController
```

기본 컨트롤러의 예제를 살펴보겠습니다. 하나의 컨트롤러는 여러 개의 public 메서드를 가질 수 있으며, 각각이 들어오는 HTTP 요청에 응답할 수 있습니다.

```
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

컨트롤러 클래스와 메서드를 작성한 후에는 아래와 같이 해당 컨트롤러 메서드로 라우트를 정의할 수 있습니다.

```
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

지정된 라우트 URI와 들어오는 요청이 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 실행되고, 라우트 파라미터가 해당 메서드로 전달됩니다.

> [!NOTE]  
> 컨트롤러는 **반드시** 어떤 기본 클래스를 상속해야 하는 것은 아닙니다. 하지만 여러 컨트롤러에서 공유해야 할 메서드가 있다면, 이러한 메서드를 가진 기본 컨트롤러 클래스를 상속하는 것이 편리할 수 있습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러 (Single Action Controllers)

특정 컨트롤러 액션의 로직이 복잡한 경우, 해당 액션만을 위해 독립된 컨트롤러 클래스를 할당할 수 있습니다. 이 경우 컨트롤러 안에 `__invoke` 메서드 하나만 정의하면 됩니다.

```
<?php

namespace App\Http\Controllers;

class ProvisionServer extends Controller
{
    /**
     * 새로운 웹 서버를 할당합니다.
     */
    public function __invoke()
    {
        // ...
    }
}
```

단일 액션 컨트롤러의 라우트를 등록할 때는 메서드 이름을 지정할 필요가 없습니다. 컨트롤러 클래스명만 라우터에 전달하면 됩니다.

```
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` Artisan 명령어에서 `--invokable` 옵션을 사용해 호출 가능한(invokable) 컨트롤러를 생성할 수 있습니다.

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]  
> 컨트롤러 스터브 파일은 [스터브 커스터마이징](/docs/11.x/artisan#stub-customization)을 통해 원하는 대로 수정할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어 (Controller Middleware)

[미들웨어](/docs/11.x/middleware)는 라우트 파일에서 해당 컨트롤러 라우트에 직접 지정할 수 있습니다.

```
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

또는, 각 컨트롤러 클래스 내에서 미들웨어를 지정하는 것도 가능합니다. 이를 위해서는 컨트롤러가 `HasMiddleware` 인터페이스를 구현해야 하는데, 이 인터페이스는 static `middleware` 메서드의 구현을 요구합니다. 이 메서드에서 컨트롤러의 각 액션에 적용할 미들웨어 배열을 반환하면 됩니다.

```
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

class UserController implements HasMiddleware
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

미들웨어를 클로저(Closure)로도 정의할 수 있는데, 이는 별도의 미들웨어 클래스를 작성하지 않고 인라인으로 미들웨어를 쉽게 정의할 수 있는 방법입니다.

```
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
> `Illuminate\Routing\Controllers\HasMiddleware`를 구현하는 컨트롤러는 `Illuminate\Routing\Controller`를 상속해서는 안 됩니다.

<a name="resource-controllers"></a>
## 리소스 컨트롤러 (Resource Controllers)

각각의 Eloquent 모델을 애플리케이션의 "리소스"로 생각할 때, 이 리소스에 대해 반복적으로 동일한 작업(생성, 조회, 수정, 삭제)을 수행하는 것이 일반적입니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다면, 사용자가 이 리소스들을 생성, 조회, 수정, 삭제할 수 있을 것입니다.

이와 같은 사용 패턴을 위해, Laravel의 리소스 라우팅은 전형적인 CRUD(생성, 조회, 수정, 삭제) 작업을 한 줄의 코드로 컨트롤러에 연결할 수 있게 해줍니다. 우선, `make:controller` Artisan 명령어의 `--resource` 옵션을 이용하여 해당 작업을 처리할 컨트롤러를 빠르게 생성할 수 있습니다.

```shell
php artisan make:controller PhotoController --resource
```

이 명령어는 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성하며, 각각의 리소스 작업 메서드를 미리 정의합니다. 이후, 아래와 같이 리소스 라우트를 컨트롤러에 연결할 수 있습니다.

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 한 줄의 라우트 선언만으로 다양한 리소스 작업을 위한 여러 라우트를 생성할 수 있으며, 생성된 컨트롤러에는 각 작업을 위한 스텁 메서드가 포함되어 있습니다. 애플리케이션의 전체 라우트 목록은 `route:list` Artisan 명령어로 빠르게 확인할 수 있습니다.

`resources` 메서드에 배열을 전달하여 여러 개의 리소스 컨트롤러를 한 번에 등록할 수도 있습니다.

```
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션

<div class="overflow-auto">

| Method    | URI                          | 액션     | 라우트 이름          |
| --------- | ---------------------------- | -------- | ------------------- |
| GET       | `/photos`                    | index    | photos.index        |
| GET       | `/photos/create`             | create   | photos.create       |
| POST      | `/photos`                    | store    | photos.store        |
| GET       | `/photos/{photo}`            | show     | photos.show         |
| GET       | `/photos/{photo}/edit`       | edit     | photos.edit         |
| PUT/PATCH | `/photos/{photo}`            | update   | photos.update       |
| DELETE    | `/photos/{photo}`            | destroy  | photos.destroy      |

</div>

<a name="customizing-missing-model-behavior"></a>
#### 존재하지 않는 모델 처리 커스터마이징

일반적으로, 암시적 모델 바인딩에서 리소스 모델을 찾지 못하면 404 HTTP 응답이 반환됩니다. 하지만 `missing` 메서드를 사용해 이 동작을 커스터마이징할 수 있습니다. `missing` 메서드는 모델을 찾지 못했을 때 호출되는 클로저를 인수로 받습니다.

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
#### 소프트 삭제된 모델

기본적으로 암시적 모델 바인딩은 [소프트 삭제](/docs/11.x/eloquent#soft-deleting)된 모델을 조회하지 않으며, 404 HTTP 응답을 반환합니다. 하지만 `withTrashed` 메서드를 사용해 소프트 삭제된 모델도 조회하도록 할 수 있습니다.

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

인수를 전달하지 않고 `withTrashed()`만 호출하면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델도 허용합니다. 특정 액션에서만 허용하려면 배열을 전달할 수 있습니다.

```
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정

[라우트 모델 바인딩](/docs/11.x/routing#route-model-binding)을 사용할 때, 리소스 컨트롤러의 메서드에서 모델 인스턴스를 타입 힌트하고 싶다면 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 리퀘스트 클래스 생성

리소스 컨트롤러를 생성할 때 `--requests` 옵션을 제공하면, 컨트롤러의 저장 및 수정 메서드에서 사용할 [폼 리퀘스트 클래스](/docs/11.x/validation#form-request-validation)도 함께 생성됩니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 일부 리소스 라우트 등록 (Partial Resource Routes)

리소스 라우트를 선언할 때, 컨트롤러가 처리해야 할 특정 액션만을 지정할 수도 있습니다.

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

API 용도로 사용할 리소스 라우트를 선언할 때 HTML 템플릿을 렌더링하는 `create`, `edit` 라우트는 보통 제외하고 싶을 것입니다. 이 경우, `apiResource` 메서드를 사용하면 두 라우트가 자동으로 제외됩니다.

```
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

여러 개의 API 리소스 컨트롤러를 한 번에 등록하려면 `apiResources` 메서드를 사용할 수 있습니다.

```
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`create`, `edit` 메서드를 포함하지 않는 API 리소스 컨트롤러를 빠르게 생성하려면 `make:controller` 명령어에서 `--api` 옵션을 사용하면 됩니다.

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스 (Nested Resources)

때때로, 중첩된 리소스에 대한 라우트를 정의해야 할 때가 있습니다. 예를 들어, 하나의 사진 리소스에 여러 개의 댓글이 달릴 수 있습니다. 이런 경우 아래와 같이 "dot" 표기법을 사용해 중첩 리소스 컨트롤러를 선언할 수 있습니다.

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 URI에서 중첩 리소스에 접근할 수 있도록 등록합니다.

```
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 스코핑

Laravel의 [암시적 모델 바인딩](/docs/11.x/routing#implicit-model-binding-scoping) 기능은 중첩된 모델 바인딩에서 자식 모델이 부모 모델에 올바르게 속하는지 자동으로 확인해줍니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 스코핑뿐만 아니라, 어떤 필드를 통해 자식 리소스를 조회할지 지정할 수 있습니다. 자세한 방법은 [리소스 라우트 스코핑](#restful-scoping-resource-routes) 항목을 참고하시기 바랍니다.

<a name="shallow-nesting"></a>
#### 얕은 중첩(Shallow Nesting)

자식 ID가 이미 고유 식별자인 경우 URI에 굳이 부모와 자식의 ID를 모두 포함할 필요가 없을 수 있습니다. URI 세그먼트에서 모델을 자동 증가 기본키 등으로 식별한다면, "얕은 중첩(Shallow Nesting)"을 적용할 수 있습니다.

```
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

위와 같이 라우트를 정의하면 다음과 같은 라우트들이 생성됩니다.

<div class="overflow-auto">

| Method    | URI                                  | 액션     | 라우트 이름               |
| --------- | ------------------------------------ | -------- | ------------------------ |
| GET       | `/photos/{photo}/comments`           | index    | photos.comments.index    |
| GET       | `/photos/{photo}/comments/create`    | create   | photos.comments.create   |
| POST      | `/photos/{photo}/comments`           | store    | photos.comments.store    |
| GET       | `/comments/{comment}`                | show     | comments.show            |
| GET       | `/comments/{comment}/edit`           | edit     | comments.edit            |
| PUT/PATCH | `/comments/{comment}`                | update   | comments.update          |
| DELETE    | `/comments/{comment}`                | destroy  | comments.destroy         |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정 (Naming Resource Routes)

기본적으로 모든 리소스 컨트롤러의 액션은 라우트 이름을 갖고 있습니다. 하지만 `names` 배열을 전달해 원하는 라우트 이름으로 오버라이드할 수 있습니다.

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정 (Naming Resource Route Parameters)

기본적으로 `Route::resource`는 리소스 라우트의 파라미터 이름을 리소스명에서 단수형으로 변환해서 생성합니다. 하지만, `parameters` 메서드를 사용해 라우트별로 쉽게 오버라이드할 수 있습니다. 전달하는 배열은 리소스명과 파라미터명을 key-value 쌍으로 작성합니다.

```
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예제는 해당 리소스의 `show` 라우트에 대한 URI를 다음과 같이 생성합니다.

```
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코핑 (Scoping Resource Routes)

Laravel의 [스코프드 암시적 모델 바인딩](/docs/11.x/routing#implicit-model-binding-scoping) 기능으로 중첩된 모델 바인딩에서 자식 모델이 부모 모델에 속하는지 자동으로 확인할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하여 자동 스코핑은 물론, 어떤 필드를 통해 자식 리소스를 가져올지 지정할 수 있습니다.

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 다음과 같은 URI로 접근 가능한 스코프드 중첩 리소스를 등록합니다.

```
/photos/{photo}/comments/{comment:slug}
```

사용자 정의 키로 바인딩된 중첩 라우트 파라미터를 사용할 때, Laravel은 부모의 연관관계명을 관례에 따라 추측하여 자식 모델을 쿼리할 때 부모와의 연결을 자동으로 스코프 처리합니다. 예시의 경우, `Photo` 모델이 `comments`라는 리턴명을 가진 연관관계를 통해 `Comment` 모델을 찾는 것으로 간주됩니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화 (Localizing Resource URIs)

기본적으로 `Route::resource`는 리소스 URI를 영어 동사와 복수 규칙을 적용하여 생성합니다. `create`, `edit` 같은 액션 동사를 현지화하려면 `Route::resourceVerbs` 메서드를 사용할 수 있습니다. 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드 시작 부분에 아래와 같이 설정할 수 있습니다.

```
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

Laravel의 복수형 변환기는 [다양한 언어를 지원](/docs/11.x/localization#pluralization-language)하므로, 필요에 따라 설정할 수 있습니다. 동사와 복수 언어 설정이 끝나면, 예를 들어 `Route::resource('publicacion', PublicacionController::class)`와 같이 리소스 라우트를 등록하게 되면 다음과 같은 URI가 생성됩니다.

```
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보완 (Supplementing Resource Controllers)

기본 리소스 라우트 외에 추가적인 라우트를 등록해야 할 경우, 반드시 `Route::resource` 메서드보다 앞서 추가 라우트를 정의해야 합니다. 그렇지 않으면 `resource` 메서드에서 생성된 라우트들이 추가 라우트를 덮어쓸 수 있습니다.

```
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]  
> 컨트롤러에는 관련 기능만 집중해서 작성하세요. 일반적인 리소스 액션 외에 반복적으로 추가 메서드가 필요하다면, 컨트롤러를 둘 이상의 작은 컨트롤러로 나누는 것이 좋습니다.

<a name="singleton-resource-controllers"></a>
### 싱글턴 리소스 컨트롤러 (Singleton Resource Controllers)

애플리케이션에서 하나의 인스턴스만 존재할 수 있는 리소스가 필요한 경우가 있습니다. 예를 들어, 사용자의 "프로필"은 오직 하나만 존재하며, 수정이나 업데이트는 가능하지만 여러 개의 프로필을 가질 수 없습니다. 마찬가지로 이미지의 "썸네일" 역시 하나만 존재할 수 있습니다. 이러한 리소스는 "싱글턴 리소스"라고 부르며, 인스턴스가 하나만 허용됩니다. 이러한 경우, "싱글턴" 리소스 컨트롤러를 등록할 수 있습니다.

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위 싱글턴 리소스 정의는 다음과 같이 라우트를 등록합니다. 보시는 것처럼 "생성" 라우트는 등록되지 않으며, 해당 리소스는 오직 하나만 존재할 수 있으므로 식별자 파라미터를 받지 않습니다.

<div class="overflow-auto">

| Method    | URI               | 액션   | 라우트 이름         |
| --------- | ----------------- | ------ | ------------------ |
| GET       | `/profile`        | show   | profile.show       |
| GET       | `/profile/edit`   | edit   | profile.edit       |
| PUT/PATCH | `/profile`        | update | profile.update     |

</div>

싱글턴 리소스는 일반적인 리소스 안에 중첩할 수도 있습니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 경우, `photos` 리소스는 [일반 리소스 라우트](#actions-handled-by-resource-controllers)를 모두 갖게 되지만, `thumbnail` 리소스는 아래와 같은 싱글턴 리소스 라우트만 갖게 됩니다.

<div class="overflow-auto">

| Method    | URI                                | 액션   | 라우트 이름                 |
| --------- | ---------------------------------- | ------ | -------------------------- |
| GET       | `/photos/{photo}/thumbnail`        | show   | photos.thumbnail.show      |
| GET       | `/photos/{photo}/thumbnail/edit`   | edit   | photos.thumbnail.edit      |
| PUT/PATCH | `/photos/{photo}/thumbnail`        | update | photos.thumbnail.update    |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글턴 리소스

때때로, 싱글턴 리소스에도 생성 및 저장 라우트가 필요할 때가 있습니다. 이럴 때는 싱글턴 리소스 라우트 등록 시 `creatable` 메서드를 사용하면 됩니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이 경우 아래와 같은 라우트가 등록됩니다. 확인해보면, `DELETE` 라우트도 함께 생성됩니다.

<div class="overflow-auto">

| Method    | URI                                   | 액션      | 라우트 이름                |
| --------- | ------------------------------------- | --------- | ------------------------- |
| GET       | `/photos/{photo}/thumbnail/create`    | create    | photos.thumbnail.create   |
| POST      | `/photos/{photo}/thumbnail`           | store     | photos.thumbnail.store    |
| GET       | `/photos/{photo}/thumbnail`           | show      | photos.thumbnail.show     |
| GET       | `/photos/{photo}/thumbnail/edit`      | edit      | photos.thumbnail.edit     |
| PUT/PATCH | `/photos/{photo}/thumbnail`           | update    | photos.thumbnail.update   |
| DELETE    | `/photos/{photo}/thumbnail`           | destroy   | photos.thumbnail.destroy  |

</div>

생성 및 저장 라우트는 등록하지 않고, 오직 `DELETE` 라우트만 싱글턴 리소스에 추가하고 싶다면 `destroyable` 메서드를 사용할 수 있습니다.

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글턴 리소스

`apiSingleton` 메서드는 API로 조작할 싱글턴 리소스를 등록할 때 사용하는데, 이 경우 `create` 및 `edit` 라우트는 필요하지 않습니다.

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론, API 싱글턴 리소스도 `creatable`로 등록 가능하며, 이 경우 해당 리소스에 대해 `store`, `destroy` 라우트가 등록됩니다.

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러 (Dependency Injection and Controllers)

<a name="constructor-injection"></a>
#### 생성자 주입 (Constructor Injection)

Laravel의 [서비스 컨테이너](/docs/11.x/container)는 모든 컨트롤러를 해석(resolve)할 때 사용됩니다. 따라서 컨트롤러 생성자에 타입-힌트된 모든 의존성을 자동으로 주입받을 수 있습니다. 선언된 의존성은 컨트롤러 인스턴스에 자동으로 주입됩니다.

```
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
#### 메서드 주입 (Method Injection)

생성자 주입 외에도, 컨트롤러의 메서드에 직접 의존성을 타입-힌트 해서 주입받을 수도 있습니다. 일반적으로는 `Illuminate\Http\Request` 인스턴스를 컨트롤러 메서드에 주입하는 경우가 많습니다.

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새 사용자를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->name;

        // 사용자를 저장...

        return redirect('/users');
    }
}
```

라우트 파라미터로부터 입력값도 받아야 한다면, 의존성 파라미터 다음에 라우트 인수를 나열하면 됩니다. 예를 들어, 라우트를 다음과 같이 정의했다면,

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메서드에서 `Illuminate\Http\Request` 타입 힌트와 라우트 파라미터 `id`를 동시에 받을 수 있습니다.

```
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
        // 사용자를 업데이트...

        return redirect('/users');
    }
}
```