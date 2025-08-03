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
    - [리소스 컨트롤러 보완하기](#restful-supplementing-resource-controllers)
    - [싱글톤 리소스 컨트롤러](#singleton-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개

라우트 파일에 모든 요청 처리 로직을 클로저로 정의하는 대신, "컨트롤러" 클래스를 사용하여 이 동작을 체계적으로 구성할 수 있습니다. 컨트롤러는 관련 요청 처리 로직을 하나의 클래스로 묶을 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청(보기, 생성, 업데이트, 삭제 등)을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기

<a name="basic-controllers"></a>
### 기본 컨트롤러

새 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 사용할 수 있습니다. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다:

```shell
php artisan make:controller UserController
```

기본 컨트롤러 예제를 살펴보겠습니다. 컨트롤러는 HTTP 요청에 응답하는 여러 개의 퍼블릭 메서드를 가질 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 특정 사용자의 프로필을 보여줍니다.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

컨트롤러 클래스와 메서드를 작성했다면, 다음과 같이 해당 메서드로 라우트를 정의할 수 있습니다:

```
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

요청이 이 라우트 URI와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고, 라우트 파라미터가 메서드에 전달됩니다.

> [!NOTE]  
> 컨트롤러가 반드시 기본 클래스를 상속받아야 하는 것은 아닙니다. 다만, `middleware`와 `authorize` 같은 편리한 기능을 사용할 수 없습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러

특정 컨트롤러 액션이 매우 복잡할 경우, 해당 액션에 전용 컨트롤러 클래스를 할당하는 것이 편리할 수 있습니다. 이를 위해 컨트롤러 내에 단 하나의 `__invoke` 메서드를 정의할 수 있습니다:

```
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

단일 액션 컨트롤러 라우트 등록 시, 메서드를 명시할 필요 없이 컨트롤러 이름만 전달하면 됩니다:

```
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`--invokable` 옵션을 사용하여 단일 액션 컨트롤러를 생성할 수 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]  
> 컨트롤러 스텁은 [stub publishing](/docs/10.x/artisan#stub-customization) 기능을 통해 사용자 정의가 가능합니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

[미들웨어](/docs/10.x/middleware)는 라우트 파일에서 컨트롤러 라우트에 할당할 수 있습니다:

```
Route::get('profile', [UserController::class, 'show'])->middleware('auth');
```

또한, 컨트롤러 생성자에서 `middleware` 메서드를 사용해 미들웨어를 지정할 수도 있습니다. 이를 통해 특정 컨트롤러 액션에 미들웨어를 할당할 수 있습니다:

```
class UserController extends Controller
{
    /**
     * 컨트롤러 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->middleware('auth');
        $this->middleware('log')->only('index');
        $this->middleware('subscribed')->except('store');
    }
}
```

컨트롤러에서는 클로저를 사용한 미들웨어 등록도 지원합니다. 이를 통해 전체 미들웨어 클래스를 만들지 않고도 단일 컨트롤러 내에 인라인 미들웨어를 정의할 수 있습니다:

```
use Closure;
use Illuminate\Http\Request;

$this->middleware(function (Request $request, Closure $next) {
    return $next($request);
});
```

<a name="resource-controllers"></a>
## 리소스 컨트롤러

애플리케이션 내 각 Eloquent 모델을 하나의 "리소스"라고 생각하면, 대개 각 리소스에 대해 생성, 조회, 수정, 삭제 같은 공통 동작을 수행하게 됩니다. 예를 들어, `Photo` 모델과 `Movie` 모델이 있다고 가정합시다. 이런 리소스는 사용자로부터 생성, 읽기, 수정, 삭제(CRUD) 요청을 받을 가능성이 큽니다.

이런 일반적인 작업을 위해, Laravel은 리소스 라우팅에서 한 줄의 코드로 컨트롤러에 CRUD 라우트를 할당합니다. 먼저, `make:controller` Artisan 명령어의 `--resource` 옵션으로 이 작업을 손쉽게 처리할 컨트롤러를 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

이 명령어는 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성하며, 모든 리소스 기본 동작에 대응하는 메서드가 포함됩니다. 그 다음, 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다:

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 라우트 선언 하나로 해당 리소스에 대한 다양한 동작을 처리하는 여러 라우트가 등록됩니다. 생성된 컨트롤러에는 각 동작 메서드의 기본 뼈대가 포함되어 있습니다. 애플리케이션 내 등록된 라우트를 빠르게 확인하려면 `route:list` Artisan 명령어를 사용하세요.

여러 리소스 컨트롤러를 한꺼번에 등록하려면, `resources` 메서드에 배열을 전달할 수 있습니다:

```
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션

| HTTP 메서드 | URI                     | 액션       | 라우트 이름          |
|-------------|-------------------------|------------|----------------------|
| GET         | `/photos`               | index      | photos.index         |
| GET         | `/photos/create`        | create     | photos.create        |
| POST        | `/photos`               | store      | photos.store         |
| GET         | `/photos/{photo}`       | show       | photos.show          |
| GET         | `/photos/{photo}/edit`  | edit       | photos.edit          |
| PUT/PATCH   | `/photos/{photo}`       | update     | photos.update        |
| DELETE      | `/photos/{photo}`       | destroy    | photos.destroy       |

<a name="customizing-missing-model-behavior"></a>
#### 누락된 모델 동작 커스터마이징

기본적으로, 암묵적 바인딩된 리소스 모델을 찾지 못하면 404 HTTP 응답이 반환됩니다. 하지만, 리소스 라우트를 정의할 때 `missing` 메서드를 호출하여 이 동작을 사용자 정의할 수 있습니다. `missing` 메서드에는 모델을 찾지 못했을 때 실행할 클로저를 전달합니다:

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

암묵적 모델 바인딩은 기본적으로 [소프트 삭제된(soft deleted)](/docs/10.x/eloquent#soft-deleting) 모델을 조회하지 않고 404 응답을 반환합니다. 그러나, 리소스 라우트를 정의할 때 `withTrashed` 메서드를 호출하면 소프트 삭제된 모델에 접근할 수 있도록 허용할 수 있습니다:

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

인자를 지정하지 않고 `withTrashed`를 호출하면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델을 허용합니다. 특정 라우트만 허용하려면 배열로 지정할 수 있습니다:

```
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정하기

[라우트 모델 바인딩](/docs/10.x/routing#route-model-binding)을 사용하며, 리소스 컨트롤러 메서드에서 모델 인스턴스에 타입힌트를 적용하려면, 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 요청 클래스 자동 생성

`--requests` 옵션으로 컨트롤러를 생성하면, 저장 및 갱신 메서드에 사용할 [폼 요청 클래스](/docs/10.x/validation#form-request-validation)를 Artisan이 자동으로 생성합니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트를 선언할 때, 기본 액션 전체 대신 일부 액션만 처리하도록 지정할 수 있습니다:

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

API에서 사용되는 리소스 라우트는 보통 HTML 템플릿을 보여주는 `create`와 `edit` 라우트를 제외합니다. 이를 쉽게 처리하려면 `apiResource` 메서드를 사용하세요:

```
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

여러 API 리소스 컨트롤러도 `apiResources` 메서드에 배열을 전달해 한 번에 등록할 수 있습니다:

```
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`create`와 `edit` 메서드를 제외한 API 리소스 컨트롤러를 빠르게 생성하려면 `--api` 옵션을 사용합니다:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스

중첩된 리소스에 대한 라우트를 정의해야 할 때가 있습니다. 예를 들어, 사진 리소스가 여러 댓글을 가질 수 있다면, 다음과 같이 "점(dot)" 표기법으로 라우트를 작성할 수 있습니다:

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 URI를 통해 중첩 리소스에 접근할 수 있게 합니다:

```
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 스코핑

Laravel의 [암묵적 모델 바인딩 스코핑](/docs/10.x/routing#implicit-model-binding-scoping) 기능은 중첩된 바인딩을 부모 모델과 자식 모델이 연결됐는지 자동으로 확인하도록 해 줍니다. `scoped` 메서드를 사용하여 중첩 리소스를 정의하면, 자동 스코핑을 활성화하며 자식 리소스를 어떤 필드로 조회할지 지정할 수 있습니다. 자세한 내용은 [리소스 라우트 스코핑](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 셸로우 네스팅(Shallow Nesting)

URI에 부모와 자식 ID를 모두 포함하는 것이 반드시 필요한 것은 아닙니다. 자식 ID가 이미 고유 식별자인 경우 다음과 같이 "shallow nesting"을 사용해서 단순화할 수 있습니다:

```
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

이 경우 등록되는 라우트는 다음과 같습니다:

| HTTP 메서드 | URI                               | 액션     | 라우트 이름               |
|-------------|----------------------------------|----------|--------------------------|
| GET         | `/photos/{photo}/comments`        | index    | photos.comments.index    |
| GET         | `/photos/{photo}/comments/create` | create   | photos.comments.create   |
| POST        | `/photos/{photo}/comments`        | store    | photos.comments.store    |
| GET         | `/comments/{comment}`             | show     | comments.show            |
| GET         | `/comments/{comment}/edit`        | edit     | comments.edit            |
| PUT/PATCH   | `/comments/{comment}`             | update   | comments.update          |
| DELETE      | `/comments/{comment}`             | destroy  | comments.destroy         |

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정하기

기본적으로 모든 리소스 컨트롤러 액션에 라우트 이름이 할당되어 있지만, `names` 배열을 전달해 원하는 이름으로 덮어쓸 수 있습니다:

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정하기

`Route::resource`는 기본적으로 리소스 이름의 단수형을 기준으로 라우트 파라미터 이름을 생성합니다. 특정 리소스에서 이를 변경하려면 `parameters` 메서드를 사용하세요. 이 메서드에는 리소스 이름과 파라미터 이름을 연관 배열 형태로 전달합니다:

```
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

이 예시는 다음과 같이 `show` 경로에 대한 URI를 생성합니다:

```
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코핑

Laravel의 [스코프 암묵적 모델 바인딩](/docs/10.x/routing#implicit-model-binding-scoping)을 사용하면, 부모 모델에 속하는 자식 모델인지 자동으로 확인해줍니다. `scoped` 메서드를 사용하여 중첩 리소스를 정의하면 이 기능이 활성화되며, 자식 리소스를 어떤 필드로 조회할지 지정할 수도 있습니다:

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 다음처럼 접근할 수 있습니다:

```
/photos/{photo}/comments/{comment:slug}
```

커스텀 키를 이용한 암묵적 바인딩이 중첩 라우트 파라미터에서 사용될 때, Laravel은 부모 모델과의 관계 이름을 추측하여 쿼리를 자동으로 스코핑합니다. 예를 들어, `Photo` 모델에 `comments`라는 연관관계가 있어야 자식 `Comment` 모델을 제대로 조회할 수 있습니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화

`Route::resource`는 기본적으로 영어 동사와 복수형 규칙을 사용해 리소스 URI를 생성합니다. `create`와 `edit` 액션 동사를 현지화하려면 `Route::resourceVerbs` 메서드를 사용하세요. 보통 애플리케이션의 `App\Providers\RouteServiceProvider` 클래스의 `boot` 메서드 초반에 설정합니다:

```
/**
 * 라우트 모델 바인딩, 패턴 필터 등을 정의합니다.
 */
public function boot(): void
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);

    // ...
}
```

Laravel의 복수형 변환기는 여러 언어를 지원하며, [필요에 따라 구성할 수 있습니다](/docs/10.x/localization#pluralization-language). 이렇게 동사와 복수형 언어를 설정한 후, 다음과 같이 리소스 라우트를 등록하면:

```
Route::resource('publicacion', PublicacionController::class)
```

다음과 같은 URI가 생성됩니다:

```
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보완하기

기본 리소스 라우트 이외에 추가 라우트를 등록해야 한다면, `Route::resource` 호출 이전에 라우트를 정의하세요. 그렇지 않으면 `resource` 메서드가 우선 적용되어 추가 라우트가 덮어써질 수 있습니다:

```
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]  
> 컨트롤러를 지나치게 방대하게 만들지 마세요. 기본 리소스 액션 외에 자주 메서드를 추가해야 한다면, 컨트롤러를 두 개 이상으로 분리하는 것을 고려하세요.

<a name="singleton-resource-controllers"></a>
### 싱글톤 리소스 컨트롤러

간혹 애플리케이션에 단 하나의 인스턴스만 존재하는 리소스가 필요할 때가 있습니다. 예를 들어, 사용자의 "프로필"은 하나만 존재하며 수정이나 갱신은 가능하지만, 여러 개 생성할 수는 없습니다. 이미지에 하나의 "썸네일"이 있는 경우도 마찬가지입니다. 이런 경우를 "싱글톤 리소스"라고 합니다. 싱글톤 리소스 컨트롤러는 다음과 같이 등록합니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위 선언으로 다음 라우트가 등록됩니다. 생성 관련 라우트는 등록되지 않으며, 리소스가 하나뿐이므로 URI에 식별자를 포함하지 않습니다:

| HTTP 메서드 | URI            | 액션   | 라우트 이름        |
|-------------|----------------|--------|--------------------|
| GET         | `/profile`     | show   | profile.show       |
| GET         | `/profile/edit`| edit   | profile.edit       |
| PUT/PATCH   | `/profile`     | update | profile.update     |

싱글톤 리소스는 표준 리소스 내에 중첩할 수도 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 경우, `photos`는 [표준 리소스 라우트](#actions-handled-by-resource-controller)를 갖지만, `thumbnail`은 아래와 같은 싱글톤 리소스 라우트를 갖습니다:

| HTTP 메서드 | URI                                   | 액션   | 라우트 이름               |
|-------------|-------------------------------------|--------|--------------------------|
| GET         | `/photos/{photo}/thumbnail`          | show   | photos.thumbnail.show    |
| GET         | `/photos/{photo}/thumbnail/edit`     | edit   | photos.thumbnail.edit    |
| PUT/PATCH   | `/photos/{photo}/thumbnail`          | update | photos.thumbnail.update  |

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글톤 리소스

가끔 싱글톤 리소스에 대해 생성 및 저장 라우트도 정의하고 싶을 때가 있습니다. 이럴 때는 싱글톤 리소스 등록 시 `creatable` 메서드를 호출하세요:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이 예시는 다음과 같은 라우트를 추가로 등록합니다. 생성 가능한 싱글톤 리소스는 `DELETE` 라우트도 포함됩니다:

| HTTP 메서드 | URI                                   | 액션    | 라우트 이름               |
|-------------|-------------------------------------|---------|--------------------------|
| GET         | `/photos/{photo}/thumbnail/create`   | create  | photos.thumbnail.create  |
| POST        | `/photos/{photo}/thumbnail`           | store   | photos.thumbnail.store   |
| GET         | `/photos/{photo}/thumbnail`           | show    | photos.thumbnail.show    |
| GET         | `/photos/{photo}/thumbnail/edit`      | edit    | photos.thumbnail.edit    |
| PUT/PATCH   | `/photos/{photo}/thumbnail`           | update  | photos.thumbnail.update  |
| DELETE      | `/photos/{photo}/thumbnail`           | destroy | photos.thumbnail.destroy |

`DELETE` 라우트만 등록하고 생성 및 저장 라우트는 제외하려면 `destroyable` 메서드를 사용하세요:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글톤 리소스

`apiSingleton` 메서드를 사용하면 API에서 조작할 싱글톤 리소스를 등록하며, `create`와 `edit` 라우트는 자동 제외됩니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```

API 싱글톤 리소스도 `creatable` 옵션을 사용할 수 있으며, 이 경우 `store`와 `destroy` 라우트가 함께 등록됩니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러

<a name="constructor-injection"></a>
#### 생성자 주입(Constructor Injection)

Laravel의 [서비스 컨테이너](/docs/10.x/container)는 모든 컨트롤러를 자동으로 해결(resolution)합니다. 따라서 컨트롤러 생성자에 필요한 의존성을 타입힌트로 선언하면, 컨테이너가 자동으로 해당 의존성을 주입합니다:

```
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
#### 메서드 주입(Method Injection)

생성자 주입 외에도 컨트롤러의 메서드에서도 의존성 타입힌트를 사용할 수 있습니다. 대표적인 예로 `Illuminate\Http\Request` 인스턴스를 컨트롤러 메서드에 주입하는 경우입니다:

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

        // 사용자 저장 로직...

        return redirect('/users');
    }
}
```

컨트롤러 메서드가 라우트 파라미터 입력도 받는다면, 라우트 인수는 타입힌트 의존성 다음에 정의하세요. 예를 들어, 다음과 같은 라우트가 있다면:

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메서드는 다음과 같이 작성할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 특정 사용자를 갱신합니다.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 갱신 로직...

        return redirect('/users');
    }
}
```