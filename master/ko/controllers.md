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
    - [리소스 라우트 범위 지정하기](#restful-scoping-resource-routes)
    - [리소스 URI 지역화하기](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 보충하기](#restful-supplementing-resource-controllers)
    - [싱글턴 리소스 컨트롤러](#singleton-resource-controllers)
    - [미들웨어와 리소스 컨트롤러](#middleware-and-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개 (Introduction)

모든 요청 처리 로직을 라우트 파일의 클로저로만 정의하는 대신, "컨트롤러(controller)" 클래스를 사용하여 이 로직을 더 체계적으로 관리할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스에 그룹화할 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청(조회, 생성, 수정, 삭제 등)을 담당할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기 (Writing Controllers)

<a name="basic-controllers"></a>
### 기본 컨트롤러 (Basic Controllers)

새로운 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 실행할 수 있습니다. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다:

```shell
php artisan make:controller UserController
```

기본 컨트롤러 예제를 살펴보겠습니다. 컨트롤러는 들어오는 HTTP 요청에 응답할 수 있는 임의 개수의 public 메서드를 가질 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

컨트롤러 클래스와 메서드를 작성하면 다음과 같이 해당 컨트롤러 메서드에 대한 라우트를 정의할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

들어오는 요청이 지정한 라우트 URI와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고 라우트 파라미터가 메서드로 전달됩니다.

> [!NOTE]
> 컨트롤러가 반드시 베이스 클래스를 상속해야 하는 것은 **아닙니다**. 하지만 모든 컨트롤러에서 공통으로 사용하는 메서드를 포함하는 기본 컨트롤러 클래스를 상속하는 것이 편리할 때도 있습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러 (Single Action Controllers)

컨트롤러 액션이 특히 복잡하다면, 해당 액션 하나만을 담당하는 컨트롤러 클래스를 따로 만드는 것이 더 편리할 수 있습니다. 이를 위해 컨트롤러 내에 단일 `__invoke` 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

class ProvisionServer extends Controller
{
    /**
     * Provision a new web server.
     */
    public function __invoke()
    {
        // ...
    }
}
```

단일 액션 컨트롤러에 대해 라우트를 등록할 때는 메서드 이름을 지정할 필요 없이 컨트롤러 클래스명만 라우터에 전달하면 됩니다:

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` Artisan 명령어에서 `--invokable` 옵션을 사용하여 호출 가능한(invokable) 컨트롤러를 생성할 수 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁은 [스텁 커스터마이징](/docs/master/artisan#stub-customization)을 통해 맞춤 설정할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어 (Controller Middleware)

[미들웨어](/docs/master/middleware)는 라우트 파일에서 컨트롤러의 라우트에 할당할 수 있습니다:

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

또는, 컨트롤러 클래스 내에서 미들웨어를 지정하는 것이 더 편리할 수 있습니다. 이를 위해 컨트롤러는 `HasMiddleware` 인터페이스를 구현해야 하며, 이 인터페이스는 컨트롤러에 static `middleware` 메서드가 있어야 함을 명시합니다. 이 메서드에서 컨트롤러의 액션에 적용할 미들웨어 배열을 반환할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

class UserController implements HasMiddleware
{
    /**
     * Get the middleware that should be assigned to the controller.
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

미들웨어를 클로저로도 정의할 수 있습니다. 이는 전체 미들웨어 클래스를 작성하지 않고도 인라인으로 미들웨어를 정의하는 편리한 방법을 제공합니다:

```php
use Closure;
use Illuminate\Http\Request;

/**
 * Get the middleware that should be assigned to the controller.
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

애플리케이션의 각 Eloquent 모델을 하나의 "리소스(resource)"로 간주하면, 애플리케이션에서 각 리소스에 대해 동일한 일련의 작업(생성, 조회, 수정, 삭제 등)을 수행하는 경우가 많습니다. 예를 들어 `Photo` 모델과 `Movie` 모델이 있을 때, 사용자들은 이 리소스들을 생성, 읽기, 수정, 삭제할 수 있습니다.

이와 같은 일반적인 사용 사례를 위해, Laravel의 리소스 라우팅은 대표적인 생성, 조회, 수정, 삭제("CRUD") 라우트를 컨트롤러에 단 한 줄로 할당할 수 있게 해 줍니다. 먼저, `make:controller` Artisan 명령어의 `--resource` 옵션을 사용하여 빠르게 해당 작업을 위한 컨트롤러를 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

이 명령어는 `app/Http/Controllers/PhotoController.php` 위치에 컨트롤러 파일을 생성합니다. 이 컨트롤러는 리소스별로 필요한 각 작업에 해당하는 메서드를 포함하게 됩니다. 다음으로, 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 한 줄의 라우트 선언으로 다양한 리소스 작업을 처리하는 여러 라우트를 한 번에 생성할 수 있습니다. 생성된 컨트롤러에는 각 작업(method)에 대응하는 메서드의 뼈대가 이미 포함되어 있습니다. 애플리케이션의 전체 라우트를 빠르게 확인하고 싶다면 `route:list` Artisan 명령어를 사용할 수 있습니다.

여러 개의 리소스 컨트롤러를 한 번에 배열로 `resources` 메서드에 전달하여 등록할 수도 있습니다:

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`softDeletableResources` 메서드는 모두 `withTrashed` 메서드를 사용하는 여러 리소스 컨트롤러를 등록합니다:

```php
Route::softDeletableResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션

<div class="overflow-auto">

| HTTP 동사     | URI                         | 액션    | 라우트 이름           |
| ------------- | --------------------------- | ------- | --------------------- |
| GET           | `/photos`                   | index   | photos.index          |
| GET           | `/photos/create`            | create  | photos.create         |
| POST          | `/photos`                   | store   | photos.store          |
| GET           | `/photos/{photo}`           | show    | photos.show           |
| GET           | `/photos/{photo}/edit`      | edit    | photos.edit           |
| PUT/PATCH     | `/photos/{photo}`           | update  | photos.update         |
| DELETE        | `/photos/{photo}`           | destroy | photos.destroy        |

</div>

<a name="customizing-missing-model-behavior"></a>
#### 존재하지 않는 모델 처리 방식 커스터마이징

일반적으로, 암묵적으로 바인딩된 리소스 모델이 존재하지 않을 경우 404 HTTP 응답이 반환됩니다. 그러나 리소스 라우트를 정의할 때 `missing` 메서드를 호출하여 이 동작을 커스터마이즈할 수 있습니다. `missing` 메서드는 암묵적으로 바인딩된 모델을 찾을 수 없을 경우 호출되는 클로저를 인수로 받습니다:

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

일반적으로, 암묵적 모델 바인딩은 [소프트 삭제](/docs/master/eloquent#soft-deleting)된 모델을 조회하지 않고 404 HTTP 응답을 반환합니다. 그러나 리소스 라우트 정의 시 `withTrashed` 메서드를 호출하여 소프트 삭제된 모델도 허용할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

`withTrashed` 메서드에 인수 없이 호출하면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델을 허용합니다. 필요한 라우트만 따로 지정하려면 배열로 전달할 수 있습니다:

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 명시하기

[라우트 모델 바인딩](/docs/master/routing#route-model-binding)을 사용하고 있고, 리소스 컨트롤러의 메서드에서 모델 인스턴스를 타입힌트로 받고 싶다면 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 리퀘스트(Form Requests) 생성

리소스 컨트롤러를 생성할 때 `--requests` 옵션을 함께 제공하면 컨트롤러의 저장 및 수정 메서드에 대한 [폼 리퀘스트 클래스](/docs/master/validation#form-request-validation)도 Artisan이 자동으로 생성해줍니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트 (Partial Resource Routes)

리소스 라우트를 선언할 때 컨트롤러가 처리할 기본 전체 액션이 아니라 일부 액션만 지정할 수 있습니다:

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

API에서 사용할 리소스 라우트를 선언할 때는 `create`, `edit`같은 HTML 템플릿을 반환하는 라우트를 생략하는 경우가 많습니다. 이러한 경우 편리하게 사용하도록 `apiResource` 메서드는 이 두 라우트를 자동으로 제외합니다:

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

여러 개의 API 리소스 컨트롤러를 한 번에 배열로 `apiResources` 메서드에 전달해 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`make:controller` 명령어 실행 시 `--api` 옵션을 사용하면 `create`, `edit` 메서드가 포함되지 않은 API 리소스 컨트롤러를 빠르게 만들 수 있습니다:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스 (Nested Resources)

경우에 따라 중첩된 리소스에 대한 라우트를 정의해야 할 때가 있습니다. 예를 들어, photo 리소스는 여러 개의 comment와 연결될 수 있습니다. 이처럼 리소스 컨트롤러를 중첩하려면 라우트 선언에서 "닷(dot)" 표기법을 사용하면 됩니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 URI로 중첩 리소스에 접근할 수 있게 됩니다:

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스의 범위 지정

Laravel의 [암묵적 모델 바인딩](/docs/master/routing#implicit-model-binding-scoping) 기능은 중첩된 바인딩에서 하위 모델이 상위 모델에 속하는지 자동으로 확인할 수 있습니다. 중첩 리소스 정의 시 `scoped` 메서드를 사용하면 자동 범위 지정이 활성화되고, 하위 리소스를 어떤 필드로 조회할지 Laravel에 지시할 수도 있습니다. 자세한 사용 방법은 [리소스 라우트의 범위 지정](#restful-scoping-resource-routes) 문서를 참고하십시오.

<a name="shallow-nesting"></a>
#### 얕은 중첩(Shallow Nesting)

보통 하위 ID는 유일한 식별자이기 때문에 URI에 상위와 하위 ID를 모두 포함할 필요가 없는 경우가 많습니다. URI에서 모델을 자동 증가 식별자 등 유일한 키로 식별한다면, "얕은 중첩(shallow nesting)"을 사용할 수 있습니다:

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

이 라우트 정의는 다음과 같은 라우트를 등록합니다:

<div class="overflow-auto">

| HTTP 동사     | URI                                   | 액션    | 라우트 이름              |
| ------------- | ------------------------------------- | ------- | ------------------------ |
| GET           | `/photos/{photo}/comments`            | index   | photos.comments.index    |
| GET           | `/photos/{photo}/comments/create`     | create  | photos.comments.create   |
| POST          | `/photos/{photo}/comments`            | store   | photos.comments.store    |
| GET           | `/comments/{comment}`                 | show    | comments.show            |
| GET           | `/comments/{comment}/edit`            | edit    | comments.edit            |
| PUT/PATCH     | `/comments/{comment}`                 | update  | comments.update          |
| DELETE        | `/comments/{comment}`                 | destroy | comments.destroy         |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정하기 (Naming Resource Routes)

기본적으로 모든 리소스 컨트롤러 액션에는 라우트 이름이 할당되지만, `names` 배열을 사용해 원하는 이름으로 덮어쓸 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정하기 (Naming Resource Route Parameters)

기본적으로 `Route::resource`는 리소스 이름의 "단수화" 버전을 사용해 라우트 파라미터를 생성합니다. 리소스별로 이 파라미터 이름을 쉽게 덮어쓸 수 있으며, `parameters` 메서드에 연관 배열을 전달하면 됩니다:

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예시의 경우, 리소스의 `show` 라우트는 다음과 같은 URI를 생성합니다:

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 범위 지정하기 (Scoping Resource Routes)

Laravel의 [scoped implicit model binding](/docs/master/routing#implicit-model-binding-scoping) 기능은 중첩된 바인딩에서 하위 모델이 상위 모델에 속하는지 자동으로 확인할 수 있습니다. 중첩 리소스 정의 시 `scoped` 메서드를 사용하면 자동 범위 지정이 이루어지며, 하위 리소스를 어떤 필드로 조회할지도 지정할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 다음과 같은 URI에서 범위가 적용된 중첩 리소스를 등록합니다:

```text
/photos/{photo}/comments/{comment:slug}
```

중첩 라우트 파라미터로 커스텀 키 암묵적 바인딩을 사용할 때, Laravel은 상위 모델의 연관관계명을 추론해 하위 모델을 범위 내에서 조회합니다. 이 경우, `Photo` 모델에 `comments`라는(라우트 파라미터 이름의 복수형) 연관관계가 있다고 간주하고, 이를 통해 `Comment` 모델을 조회하게 됩니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 지역화하기 (Localizing Resource URIs)

기본적으로 `Route::resource`는 리소스 URI를 영문 동사와 복수규칙에 따라 생성합니다. `create`, `edit`와 같은 액션 동사를 현지화해야 한다면 `Route::resourceVerbs` 메서드를 사용할 수 있습니다. 이는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 맨 앞에서 설정할 수 있습니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);
}
```

Laravel 플루랄라이저(pluralizer)는 [다양한 언어를 지원하며 필요에 따라 구성할 수 있습니다](/docs/master/localization#pluralization-language). 동사와 복수화 언어를 맞춤설정한 후, `Route::resource('publicacion', PublicacionController::class)`과 같이 resource 라우트를 등록하면 다음과 같은 URI가 생성됩니다:

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보충하기 (Supplementing Resource Controllers)

기본 리소스 라우트 외에 추가적인 라우트를 리소스 컨트롤러에 추가하려면, `Route::resource` 메서드 호출보다 먼저 해당 라우트를 정의해야 합니다. 그렇지 않으면, `resource` 메서드의 라우트가 추가 라우트보다 우선 적용될 수 있습니다:

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러는 특정 리소스 액션 집합에 집중하도록 설계하세요. 일반적인 리소스 액션 외의 메서드가 계속 필요하다면, 컨트롤러를 둘로 나누어 더 작게 분리하는 것이 좋습니다.

<a name="singleton-resource-controllers"></a>
### 싱글턴 리소스 컨트롤러 (Singleton Resource Controllers)

애플리케이션에 단일 인스턴스만 존재할 수 있는 리소스가 있을 때가 있습니다. 예를 들어, 사용자의 "프로필"은 한 명의 사용자당 하나만 존재하며, 수정이나 업데이트만 할 수 있습니다. 이와 마찬가지로, 이미지에 하나의 "썸네일"만 있을 수 있습니다. 이런 리소스들을 "싱글턴 리소스(singleton resource)"라고 하며, 오직 하나의 인스턴스만 존재합니다. 이 경우 "싱글턴" 리소스 컨트롤러를 등록할 수 있습니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위 싱글턴 리소스 정의는 다음과 같은 라우트를 등록합니다. 알 수 있듯이, 싱글턴 리소스는 "생성" 관련 라우트가 등록되지 않으며, 오직 한 개의 인스턴스만 존재하기 때문에 라우트에서 식별자를 사용하지 않습니다:

<div class="overflow-auto">

| HTTP 동사     | URI               | 액션    | 라우트 이름         |
| ------------- | ----------------- | ------- | ------------------- |
| GET           | `/profile`        | show    | profile.show        |
| GET           | `/profile/edit`   | edit    | profile.edit        |
| PUT/PATCH     | `/profile`        | update  | profile.update      |

</div>

싱글턴 리소스는 표준 리소스 내부에 중첩해서 사용할 수도 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 예시에서는, `photos` 리소스는 [표준 리소스 라우트](#actions-handled-by-resource-controllers) 모두를 받고, `thumbnail` 리소스는 다음과 같이 싱글턴 리소스 라우트만 등록하게 됩니다:

<div class="overflow-auto">

| HTTP 동사     | URI                                 | 액션    | 라우트 이름                  |
| ------------- | ----------------------------------- | ------- | ---------------------------- |
| GET           | `/photos/{photo}/thumbnail`         | show    | photos.thumbnail.show        |
| GET           | `/photos/{photo}/thumbnail/edit`    | edit    | photos.thumbnail.edit        |
| PUT/PATCH     | `/photos/{photo}/thumbnail`         | update  | photos.thumbnail.update      |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글턴 리소스 (Creatable Singleton Resources)

경우에 따라 싱글턴 리소스에도 생성 및 저장 라우트를 정의하고 싶을 때가 있습니다. 이때 `creatable` 메서드를 호출해 싱글턴 리소스 라우트로 등록할 수 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이 예시에서는 다음과 같은 라우트들이 등록됩니다. 생성, 저장을 위한 라우트뿐 아니라, `DELETE` 라우트도 함께 등록됩니다:

<div class="overflow-auto">

| HTTP 동사     | URI                                   | 액션    | 라우트 이름                    |
| ------------- | ------------------------------------- | ------- | ------------------------------ |
| GET           | `/photos/{photo}/thumbnail/create`    | create  | photos.thumbnail.create        |
| POST          | `/photos/{photo}/thumbnail`           | store   | photos.thumbnail.store         |
| GET           | `/photos/{photo}/thumbnail`           | show    | photos.thumbnail.show          |
| GET           | `/photos/{photo}/thumbnail/edit`      | edit    | photos.thumbnail.edit          |
| PUT/PATCH     | `/photos/{photo}/thumbnail`           | update  | photos.thumbnail.update        |
| DELETE        | `/photos/{photo}/thumbnail`           | destroy | photos.thumbnail.destroy       |

</div>

만약 싱글턴 리소스를 위해 `DELETE` 라우트만 등록하고, 생성 및 저장 라우트는 등록하고 싶지 않다면 `destroyable` 메서드를 사용할 수 있습니다:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글턴 리소스 (API Singleton Resources)

`apiSingleton` 메서드는 `create`, `edit` 라우트가 필요 없는 API 기반의 싱글턴 리소스를 등록하는데 사용할 수 있습니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론, API 싱글턴 리소스도 `creatable`을 적용하여 `store` 및 `destroy` 라우트를 함께 등록할 수 있습니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="middleware-and-resource-controllers"></a>
### 미들웨어와 리소스 컨트롤러 (Middleware and Resource Controllers)

Laravel에서는 `middleware`, `middlewareFor`, `withoutMiddlewareFor` 메서드를 활용해 전체 혹은 특정 리소스 라우트 메서드에 미들웨어를 자유롭게 할당할 수 있습니다. 이들 메서드를 통해 리소스 액션별로 미들웨어 적용 범위를 정밀하게 제어할 수 있습니다.

#### 전체 메서드에 미들웨어 적용

`middleware` 메서드를 사용하면 리소스 또는 싱글턴 리소스 라우트에서 생성되는 모든 라우트에 미들웨어를 할당할 수 있습니다:

```php
Route::resource('users', UserController::class)
    ->middleware(['auth', 'verified']);

Route::singleton('profile', ProfileController::class)
    ->middleware('auth');
```

#### 특정 메서드에 미들웨어 적용

`middlewareFor` 메서드로 원하는 하나 혹은 여러 메서드에만 미들웨어를 할당할 수 있습니다:

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

`s`inggleton 및 API 싱글턴 리소스 컨트롤러와 함께 `middlewareFor` 메서드도 사용할 수 있습니다:

```php
Route::singleton('profile', ProfileController::class)
    ->middlewareFor('show', 'auth');

Route::apiSingleton('profile', ProfileController::class)
    ->middlewareFor(['show', 'update'], 'auth');
```

#### 특정 메서드에서 미들웨어 제외

`withoutMiddlewareFor` 메서드로 리소스 컨트롤러의 특정 메서드에 미들웨어를 적용하지 않게 할 수 있습니다:

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
#### 생성자 주입(Constructor Injection)

Laravel의 [서비스 컨테이너](/docs/master/container)는 모든 Laravel 컨트롤러를 해석하는 데 사용됩니다. 이로 인해 컨트롤러의 생성자에서 필요한 모든 의존성을 타입힌트로 선언할 수 있습니다. 선언된 의존성은 자동으로 해석되어 컨트롤러 인스턴스에 주입됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}
}
```

<a name="method-injection"></a>
#### 메서드 주입(Method Injection)

생성자 주입 외에도, 컨트롤러의 메서드에서 의존성을 타입힌트로 지정할 수 있습니다. 흔히 사용되는 메서드 주입 예시는 컨트롤러 메서드에서 `Illuminate\Http\Request` 인스턴스를 받는 것입니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a new user.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->name;

        // Store the user...

        return redirect('/users');
    }
}
```

컨트롤러 메서드에서 라우트 파라미터 입력도 필요한 경우, 다른 의존성 뒤에 라우트 인수를 나열하면 됩니다. 예를 들어, 라우트를 이렇게 정의했다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

다음과 같이 컨트롤러 메서드를 정의하여 `Illuminate\Http\Request`도 타입힌트로 받고, `id` 파라미터도 함께 받을 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Update the given user.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // Update the user...

        return redirect('/users');
    }
}
```
