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
    - [리소스 컨트롤러 확장](#restful-supplementing-resource-controllers)
    - [싱글톤 리소스 컨트롤러](#singleton-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개 (Introduction)

모든 요청 처리 로직을 라우트 파일의 클로저로 정의하는 대신에, "컨트롤러" 클래스를 사용해 이 동작을 조직화할 수 있습니다. 컨트롤러는 관련 요청 처리 로직을 하나의 클래스로 묶어 관리할 수 있도록 도와줍니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청(사용자 조회, 생성, 수정, 삭제)을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기 (Writing Controllers)

<a name="basic-controllers"></a>
### 기본 컨트롤러 (Basic Controllers)

기본 컨트롤러의 예를 살펴보겠습니다. 이 컨트롤러는 Laravel에 포함된 기본 컨트롤러 클래스 `App\Http\Controllers\Controller`를 상속받습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 보여줍니다.
     *
     * @param  int  $id
     * @return \Illuminate\View\View
     */
    public function show($id)
    {
        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

이 컨트롤러 메서드에 대한 라우트는 다음과 같이 정의할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

들어오는 요청이 지정한 라우트 URI와 일치하면 `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고, 라우트 파라미터가 해당 메서드로 전달됩니다.

> [!NOTE]
> 컨트롤러가 반드시 기본 클래스를 상속해야 하는 것은 아닙니다. 다만, `middleware`나 `authorize` 같은 편리한 메서드는 상속받지 않으면 사용할 수 없습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러 (Single Action Controllers)

컨트롤러 액션이 특히 복잡한 경우, 하나의 액션만을 담당하는 전용 컨트롤러 클래스를 만들면 편리할 수 있습니다. 이를 위해 컨트롤러 내에 단일 `__invoke` 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;

class ProvisionServer extends Controller
{
    /**
     * 새로운 웹 서버를 구성합니다.
     *
     * @return \Illuminate\Http\Response
     */
    public function __invoke()
    {
        // ...
    }
}
```

단일 액션 컨트롤러의 라우트를 등록할 때는 메서드를 지정할 필요 없이 컨트롤러 클래스명만 전달하면 됩니다:

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` Artisan 명령어에 `--invokable` 옵션을 사용하여 단일 액션 컨트롤러를 생성할 수 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁은 [스텁 공개](/docs/9.x/artisan#stub-customization)를 사용해 커스터마이징할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어 (Controller Middleware)

[미들웨어](/docs/9.x/middleware)는 라우트 파일에서 컨트롤러의 라우트에 할당할 수 있습니다:

```php
Route::get('profile', [UserController::class, 'show'])->middleware('auth');
```

또는 컨트롤러 생성자에서 직접 미들웨어를 지정하는 것이 편리할 수 있습니다. 컨트롤러 생성자 내에서 `middleware` 메서드를 사용해 미들웨어를 컨트롤러 액션에 할당할 수 있습니다:

```php
class UserController extends Controller
{
    /**
     * 새 컨트롤러 인스턴스를 생성합니다.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('auth');
        $this->middleware('log')->only('index');
        $this->middleware('subscribed')->except('store');
    }
}
```

컨트롤러에서는 클로저를 사용해 미들웨어를 등록할 수도 있습니다. 이를 통해 전체 미들웨어 클래스를 정의하지 않고도 특정 컨트롤러에 대해 인라인 미들웨어를 간단히 정의할 수 있습니다:

```php
$this->middleware(function ($request, $next) {
    return $next($request);
});
```

<a name="resource-controllers"></a>
## 리소스 컨트롤러 (Resource Controllers)

애플리케이션의 각 Eloquent 모델을 "리소스"라고 생각하면, 각각의 리소스에 대해 같은 동작(생성, 조회, 수정, 삭제, 즉 CRUD)을 반복하는 일이 흔합니다. 예를 들어 `Photo` 모델과 `Movie` 모델이 있다면 사용자들이 이 리소스를 생성, 읽기, 업데이트, 삭제할 수 있습니다.

이 공통된 상황을 위해 Laravel의 리소스 라우팅은 단 한 줄의 코드로 리소스의 CRUD 라우트를 컨트롤러에 할당할 수 있게 해줍니다. 먼저 `make:controller` Artisan 명령어의 `--resource` 옵션을 사용하여 CRUD 액션을 처리할 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

이 명령은 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성하고, 각 리소스 작업을 처리하는 메서드들을 포함합니다. 그 후 다음과 같이 리소스 라우트를 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 한 줄의 라우트 선언은 리소스에 대해 다양한 액션을 처리하는 다수의 라우트를 생성합니다. 생성된 컨트롤러는 이미 각 기능에 필요한 메서드가 준비되어 있습니다. `route:list` Artisan 명령어를 사용하면 애플리케이션의 전체 라우트를 쉽게 확인할 수 있습니다.

또한 하나 이상의 리소스 컨트롤러를 배열 형태로 한 번에 등록할 수도 있습니다:

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controller"></a>
#### 리소스 컨트롤러가 처리하는 액션들

| HTTP 메서드 | URI                       | 액션    | 라우트 이름            |
| ----------- | ------------------------- | ------- | --------------------- |
| GET         | `/photos`                 | index   | photos.index          |
| GET         | `/photos/create`          | create  | photos.create         |
| POST        | `/photos`                 | store   | photos.store          |
| GET         | `/photos/{photo}`         | show    | photos.show           |
| GET         | `/photos/{photo}/edit`    | edit    | photos.edit           |
| PUT/PATCH   | `/photos/{photo}`         | update  | photos.update         |
| DELETE      | `/photos/{photo}`         | destroy | photos.destroy        |

<a name="customizing-missing-model-behavior"></a>
#### 누락된 모델 커스터마이징

암묵적 바인딩된 리소스 모델을 찾지 못하면 기본적으로 404 HTTP 응답이 생성됩니다. 하지만 리소스 라우트를 정의할 때 `missing` 메서드를 호출하여 이 동작을 커스터마이징할 수 있습니다. `missing` 메서드는 리소스의 라우트들 중 모델을 찾지 못했을 때 실행할 클로저를 받습니다:

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
#### Soft Deleted 모델

일반적으로 암묵적 모델 바인딩은 [소프트 삭제](/docs/9.x/eloquent#soft-deleting)된 모델을 검색하지 않으며, 404 응답을 반환합니다. 하지만 리소스 라우트를 정의할 때 `withTrashed` 메서드를 호출하면 소프트 삭제된 모델도 허용할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

인자를 주지 않고 `withTrashed`를 호출하면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델을 허용합니다. 특정 라우트에만 적용하고 싶으면 배열을 인자로 전달하세요:

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 명시

[라우트 모델 바인딩](/docs/9.x/routing#route-model-binding)을 활용해 리소스 컨트롤러의 메서드들이 모델 인스턴스를 타입힌트하도록 하려면, 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 리퀘스트 생성

`--requests` 옵션을 활용해 리소스 컨트롤러의 `store` 및 `update` 메서드에 대한 [폼 리퀘스트 클래스](/docs/9.x/validation#form-request-validation)도 함께 생성하도록 Artisan에 지시할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트 (Partial Resource Routes)

리소스 라우트를 선언할 때, 기본 액션 전체 대신 컨트롤러가 처리할 액션 일부만 지정할 수 있습니다:

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

API에서 사용하는 리소스 라우트를 선언할 때는 `create`와 `edit` 같은 HTML 템플릿을 보여주는 라우트를 보통 제외합니다. 이를 편리하게 처리하려면 `apiResource` 메서드를 사용하세요:

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

여러 API 리소스 컨트롤러를 배열로 한 번에 등록하려면 `apiResources` 메서드를 사용합니다:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`create`와 `edit` 메서드를 포함하지 않는 API 리소스 컨트롤러를 빠르게 생성하려면 `make:controller` 명령어 실행 시 `--api` 스위치를 사용하세요:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스 (Nested Resources)

때때로 중첩된 리소스에 대한 라우트가 필요할 수 있습니다. 예를 들어 사진(`photo`) 리소스에는 여러 개의 댓글(`comment`)이 붙을 수 있습니다. 이때 라우트 선언 시 "점(dot)" 표기법을 사용할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 형태의 URI에 접근할 수 있도록 중첩 리소스를 등록합니다:

```
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 스코핑

Laravel의 [암묵적 모델 바인딩 스코핑](/docs/9.x/routing#implicit-model-binding-scoping) 기능은 중첩된 바인딩을 자동으로 스코핑하여 자식 모델이 부모 모델에 속하는지 확인합니다. `scoped` 메서드를 사용해 중첩 리소스를 정의하면 자동 스코핑이 활성화되고, 자식 리소스를 어떤 필드로 검색할지 지정할 수 있습니다. 자세한 방법은 [리소스 라우트 스코핑](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 셀로우 네스팅 (Shallow Nesting)

URI에 부모와 자식 ID를 모두 포함하는 것이 항상 필요한 것은 아닙니다. 자식 ID가 이미 고유 식별자라면 셀로우 네스팅을 선택할 수 있습니다. 예를 들어, 오토 인크리먼트 기본키 같은 고유 식별자를 URI 세그먼트로 사용할 때 다음과 같이 정의합니다:

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

위 라우트 정의는 다음과 같은 라우트를 생성합니다:

| HTTP 메서드 | URI                                | 액션    | 라우트 이름                  |
| ----------- | --------------------------------- | ------- | --------------------------- |
| GET         | `/photos/{photo}/comments`         | index   | photos.comments.index       |
| GET         | `/photos/{photo}/comments/create`  | create  | photos.comments.create      |
| POST        | `/photos/{photo}/comments`         | store   | photos.comments.store       |
| GET         | `/comments/{comment}`              | show    | comments.show               |
| GET         | `/comments/{comment}/edit`         | edit    | comments.edit               |
| PUT/PATCH   | `/comments/{comment}`              | update  | comments.update             |
| DELETE      | `/comments/{comment}`              | destroy | comments.destroy            |

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정 (Naming Resource Routes)

기본적으로 모든 리소스 컨트롤러 액션은 라우트 이름을 가집니다. 하지만 원하는 라우트 이름 배열을 `names` 메서드에 전달해 이름을 직접 지정할 수도 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정 (Naming Resource Route Parameters)

기본적으로 `Route::resource`는 리소스 이름을 단수형으로 변환해 URI 파라미터 이름을 생성합니다. 하지만 `parameters` 메서드를 사용해 각 리소스별로 이 이름을 커스터마이즈할 수 있습니다. `parameters`에 넘기는 배열은 리소스 이름과 파라미터 이름의 연관 배열이어야 합니다:

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예시는 `show` 라우트의 URI를 다음과 같이 만듭니다:

```
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코핑 (Scoping Resource Routes)

Laravel의 [스코핑된 암묵적 모델 바인딩](/docs/9.x/routing#implicit-model-binding-scoping) 기능은 자식 모델이 반드시 부모 모델에 속하는지 검증할 수 있습니다. `scoped` 메서드를 사용해 중첩 리소스를 정의하면 자동 스코핑이 활성화되고, 자식 리소스를 검색할 필드를 지정할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 다음과 같은 URI를 등록합니다:

```
/photos/{photo}/comments/{comment:slug}
```

중첩 라우트 파라미터에 커스텀 키된 암묵적 바인딩을 사용할 경우, Laravel은 부모 모델의 관계 이름을 추론해 중첩 모델을 부모 기준으로 스코핑하여 조회합니다. 이 예에서는 `Photo` 모델이 `comments`라는 관계(라우트 파라미터 이름의 복수형)를 갖는다고 가정합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화 (Localizing Resource URIs)

기본적으로 `Route::resource`는 영어 동사 및 복수 규칙을 사용해 URI를 만듭니다. `create`와 `edit` 동사를 현지화해야 한다면, 애플리케이션의 `App\Providers\RouteServiceProvider` 내 `boot` 메서드 초기에 `Route::resourceVerbs` 메서드를 사용할 수 있습니다:

```php
/**
 * 라우트 모델 바인딩, 패턴 필터 등을 정의합니다.
 *
 * @return void
 */
public function boot()
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);

    // ...
}
```

Laravel의 복수형 변환기는 [여러 언어를 지원하며 사용자 필요에 따라 구성할 수 있습니다](/docs/9.x/localization#pluralization-language). 동사와 복수형 언어를 변경한 후 다음과 같은 리소스 라우트 등록 예시는 다음 URI들을 생성합니다:

```
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 확장 (Supplementing Resource Controllers)

기본 리소스 라우트 외에 추가 라우트를 리소스 컨트롤러에 등록해야 한다면, 반드시 `Route::resource` 호출 이전에 추가 라우트를 정의하세요. 그렇지 않으면 `resource` 메서드가 등록한 라우트가 우선권을 가져 의도하지 않은 동작이 발생할 수 있습니다:

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러는 역할이 명확해야 합니다. 일반적인 리소스 액션 범위를 벗어나 반복적으로 메서드가 필요하다면, 컨트롤러를 두 개 이상의 더 작은 컨트롤러로 분리하는 것을 고려하세요.

<a name="singleton-resource-controllers"></a>
### 싱글톤 리소스 컨트롤러 (Singleton Resource Controllers)

애플리케이션에 인스턴스가 하나만 존재하는 리소스가 있을 수 있습니다. 예를 들면, 사용자의 "프로필"은 하나만 존재하며 수정하거나 보여줄 수 있습니다. 마찬가지로 이미지는 하나의 "썸네일"만 가질 수 있습니다. 이러한 리소스는 "싱글톤 리소스"라고 하며, 단 하나의 인스턴스만 존재할 수 있습니다. 이런 경우 "싱글톤" 리소스 컨트롤러를 등록할 수 있습니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위 싱글톤 리소스 정의는 다음 라우트를 등록합니다. 보시다시피 "생성" 관련 라우트는 등록되지 않으며, 식별자를 받지 않습니다(인스턴스가 하나뿐이기 때문):

| HTTP 메서드 | URI           | 액션   | 라우트 이름       |
| ----------- | ------------- | ------ | ---------------- |
| GET         | `/profile`    | show   | profile.show     |
| GET         | `/profile/edit` | edit   | profile.edit     |
| PUT/PATCH   | `/profile`    | update | profile.update   |

싱글톤 리소스는 일반 리소스 내에 중첩해서 사용할 수도 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 경우 `photos` 리소스는 [기본 리소스 라우트](#actions-handled-by-resource-controller)를 받으며, `thumbnail` 리소스는 싱글톤 리소스로 아래와 같은 라우트를 가집니다:

| HTTP 메서드 | URI                              | 액션  | 라우트 이름               |
| ----------- | -------------------------------- | ------ | ------------------------ |
| GET         | `/photos/{photo}/thumbnail`      | show   | photos.thumbnail.show    |
| GET         | `/photos/{photo}/thumbnail/edit` | edit   | photos.thumbnail.edit    |
| PUT/PATCH   | `/photos/{photo}/thumbnail`      | update | photos.thumbnail.update  |

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글톤 리소스 (Creatable Singleton Resources)

가끔 싱글톤 리소스에 대해 생성(create)과 저장(store) 라우트를 정의하고 싶을 때가 있습니다. 이 경우 싱글톤 리소스 등록 시 `creatable` 메서드를 호출하세요:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

아래와 같은 라우트가 등록되며, `DELETE` 라우트도 생성됩니다:

| HTTP 메서드 | URI                                | 액션    | 라우트 이름               |
| ----------- | ---------------------------------- | ------- | ------------------------ |
| GET         | `/photos/{photo}/thumbnail/create` | create  | photos.thumbnail.create  |
| POST        | `/photos/{photo}/thumbnail`        | store   | photos.thumbnail.store   |
| GET         | `/photos/{photo}/thumbnail`        | show    | photos.thumbnail.show    |
| GET         | `/photos/{photo}/thumbnail/edit`   | edit    | photos.thumbnail.edit    |
| PUT/PATCH   | `/photos/{photo}/thumbnail`        | update  | photos.thumbnail.update  |
| DELETE      | `/photos/{photo}/thumbnail`        | destroy | photos.thumbnail.destroy |

생성 및 저장 라우트는 제외하되, `DELETE` 라우트만 등록하고 싶다면 `destroyable` 메서드를 활용할 수 있습니다:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글톤 리소스 (API Singleton Resources)

`apiSingleton` 메서드는 API를 통해 조작할 싱글톤 리소스를 등록할 때 사용하며, 이 경우 `create`와 `edit` 라우트는 필요 없습니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론 API 싱글톤 리소스도 `creatable`일 수 있으며, 이 경우 `store`와 `destroy` 라우트도 등록됩니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러 (Dependency Injection & Controllers)

<a name="constructor-injection"></a>
#### 생성자 주입 (Constructor Injection)

Laravel의 [서비스 컨테이너](/docs/9.x/container)는 모든 컨트롤러를 해석하는 데 사용됩니다. 따라서 컨트롤러 생성자에 필요한 의존성을 타입힌트하면, 해당 의존성이 자동으로 해결되어 컨트롤러 인스턴스에 주입됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * 유저 리포지토리 인스턴스.
     */
    protected $users;

    /**
     * 새 컨트롤러 인스턴스를 만듭니다.
     *
     * @param  \App\Repositories\UserRepository  $users
     * @return void
     */
    public function __construct(UserRepository $users)
    {
        $this->users = $users;
    }
}
```

<a name="method-injection"></a>
#### 메서드 주입 (Method Injection)

생성자 주입 외에도 컨트롤러 메서드에 의존성을 타입힌트할 수 있습니다. 대표적인 예는 컨트롤러 메서드에 `Illuminate\Http\Request` 인스턴스를 주입하는 것입니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새로운 사용자를 저장합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $name = $request->name;

        //
    }
}
```

컨트롤러 메서드가 라우트 파라미터도 기대하는 경우, 의존성 타입힌트가 라우트 인수 앞에 오도록 하세요. 예를 들어 라우트가 다음과 같다고 가정해봅시다:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

이때 `Illuminate\Http\Request`를 타입힌트하고 `id` 파라미터를 접근하려면 다음처럼 메서드를 정의하세요:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 주어진 사용자를 업데이트합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  string  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }
}
```