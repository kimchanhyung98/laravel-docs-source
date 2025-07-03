# 컨트롤러 (Controllers)

- [소개](#introduction)
- [컨트롤러 작성하기](#writing-controllers)
    - [기본 컨트롤러](#basic-controllers)
    - [단일 동작 컨트롤러](#single-action-controllers)
- [컨트롤러 미들웨어](#controller-middleware)
- [리소스 컨트롤러](#resource-controllers)
    - [부분 리소스 라우트](#restful-partial-resource-routes)
    - [중첩 리소스](#restful-nested-resources)
    - [리소스 라우트 이름 지정](#restful-naming-resource-routes)
    - [리소스 라우트 파라미터 이름 지정](#restful-naming-resource-route-parameters)
    - [리소스 라우트 스코프 지정](#restful-scoping-resource-routes)
    - [리소스 URI 현지화](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 보완하기](#restful-supplementing-resource-controllers)
    - [싱글턴 리소스 컨트롤러](#singleton-resource-controllers)
    - [미들웨어와 리소스 컨트롤러](#middleware-and-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개

모든 요청 처리 로직을 라우트 파일에서 클로저로 정의하는 대신, "컨트롤러" 클래스를 활용해 이러한 동작을 체계적으로 정리할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직들을 하나의 클래스에 모아서 관리할 수 있도록 도와줍니다. 예를 들어, `UserController` 클래스는 사용자 관련 요청(표시, 생성, 수정, 삭제 등)을 모두 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기

<a name="basic-controllers"></a>
### 기본 컨트롤러

새 컨트롤러를 빠르게 생성하려면 `make:controller` 아티즌 명령어를 실행하면 됩니다. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다:

```shell
php artisan make:controller UserController
```

아래는 기본 컨트롤러 예시입니다. 컨트롤러는 여러 개의 public 메서드를 가질 수 있으며, 각각이 들어오는 HTTP 요청에 응답할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 표시합니다.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

컨트롤러 클래스와 메서드를 작성했다면, 아래와 같이 해당 컨트롤러 메서드로 라우트를 정의할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

들어오는 요청이 지정한 라우트 URI와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되며, 라우트 파라미터가 해당 메서드로 전달됩니다.

> [!NOTE]
> 컨트롤러가 반드시 기본 클래스(Controller 등)를 상속할 필요는 없습니다. 하지만, 여러 컨트롤러에서 공통적으로 사용하는 메서드가 있다면, 이를 포함한 기본 컨트롤러 클래스를 상속하는 것이 편리할 수 있습니다.

<a name="single-action-controllers"></a>
### 단일 동작 컨트롤러

컨트롤러에서 수행하는 작업이 특히 복잡하다면, 하나의 동작만을 위해 전용 컨트롤러 클래스를 만드는 것이 더 명확할 수 있습니다. 이를 위해, 컨트롤러 내에 단일 `__invoke` 메서드만 정의하면 됩니다:

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

이와 같이 단일 동작 컨트롤러의 라우트를 등록할 때는 컨트롤러 메서드를 명시할 필요가 없습니다. 대신, 컨트롤러의 클래스명만 라우터에 전달하면 됩니다:

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`--invokable` 옵션을 추가하여 invokable(호출 가능한) 컨트롤러를 빠르게 생성할 수도 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁(stub)은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 사용해 커스터마이징할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

[미들웨어](/docs/12.x/middleware)는 라우트 파일에서 컨트롤러의 라우트에 지정할 수 있습니다:

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

또는 컨트롤러 클래스 내부에서 미들웨어를 지정하는 것이 편리할 수 있습니다. 이를 위해 컨트롤러는 `HasMiddleware` 인터페이스를 구현해야 하며, 이 인터페이스는 컨트롤러가 static `middleware` 메서드를 가지도록 요구합니다. 이 메서드에서 컨트롤러의 액션에 적용할 미들웨어 배열을 반환할 수 있습니다:

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

미들웨어를 클로저로 정의할 수도 있습니다. 이렇게 하면 전체 미들웨어 클래스를 작성하지 않고도 인라인으로 미들웨어를 편리하게 작성할 수 있습니다:

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

애플리케이션의 각 Eloquent 모델을 "리소스"로 본다면, 각 리소스에 대해 동일한 작업 집합을 수행하는 경우가 많습니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다면, 사용자들은 주로 이 리소스들을 생성, 조회, 수정, 삭제할 수 있습니다.

이러한 패턴이 흔하기 때문에, 라라벨 리소스 라우팅은 일반적으로 사용되는 생성(create), 조회(read), 수정(update), 삭제(delete) 동작("CRUD")을 한 줄의 코드로 컨트롤러에 매핑해줍니다. 우선, `make:controller` 아티즌 명령어의 `--resource` 옵션을 사용해 이러한 동작을 처리할 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

이 명령어는 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성합니다. 해당 컨트롤러에는 각 리소스 동작을 처리하는 메서드가 포함됩니다. 이제 아래와 같이 해당 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 한 줄의 라우트 선언만으로 다양한 리소스 동작을 처리할 여러 라우트가 생성됩니다. 생성된 컨트롤러에는 이미 각 동작별로 필요한 메서드 스텁이 포함되어 있습니다. 참고로, `route:list` 아티즌 명령어를 실행하면 애플리케이션의 전체 라우트를 빠르게 확인할 수 있습니다.

아래와 같이 한 번에 여러 리소스 컨트롤러를 배열로 등록할 수도 있습니다:

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 동작

<div class="overflow-auto">

| HTTP 메서드 | URI                       | 액션    | 라우트 이름        |
| ----------- | ------------------------- | ------- | ------------------ |
| GET         | `/photos`                 | index   | photos.index       |
| GET         | `/photos/create`          | create  | photos.create      |
| POST        | `/photos`                 | store   | photos.store       |
| GET         | `/photos/{photo}`         | show    | photos.show        |
| GET         | `/photos/{photo}/edit`    | edit    | photos.edit        |
| PUT/PATCH   | `/photos/{photo}`         | update  | photos.update      |
| DELETE      | `/photos/{photo}`         | destroy | photos.destroy     |

</div>

<a name="customizing-missing-model-behavior"></a>
#### 존재하지 않는 모델의 동작 커스터마이징

일반적으로, 암묵적(implicit)으로 바인딩되는 리소스 모델이 존재하지 않을 경우 404 HTTP 응답이 반환됩니다. 하지만, 리소스 라우트 정의 시 `missing` 메서드를 호출하여 이 동작을 직접 정의할 수 있습니다. `missing` 메서드는 클로저를 받아서, 해당 리소스의 어떤 라우트에서라도 암묵적으로 바인딩된 모델이 없으면 실행됩니다:

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
#### 소프트 삭제된 모델 사용

일반적으로, 암묵적 모델 바인딩은 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)된 모델을 조회하지 않고, 대신 404 응답을 반환합니다. 그러나, 리소스 라우트 정의 시 `withTrashed` 메서드를 사용하면 소프트 삭제된 모델도 허용할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

인자를 지정하지 않고 `withTrashed`를 호출하면 `show`, `edit`, `update` 라우트에서 소프트 삭제된 모델을 허용합니다. 특정 라우트만 지정하려면, 배열로 전달하면 됩니다:

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정하기

[라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 사용하고, 리소스 컨트롤러 메서드에서 모델 인스턴스를 타입힌트하고 싶다면, 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 요청 클래스 자동 생성

리소스 컨트롤러 생성 시 `--requests` 옵션을 사용하면, 아티즌이 [폼 요청 클래스](/docs/12.x/validation#form-request-validation)를 저장 및 수정 메서드용으로 자동 생성해 줍니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트를 선언할 때, 전체 기본 동작 대신 컨트롤러가 처리할 동작 일부만 명시할 수 있습니다:

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

API에서 사용할 리소스 라우트를 선언할 때는, 일반적으로 HTML 템플릿을 제공하는 `create`와 `edit` 라우트는 제외하는 경우가 많습니다. 편의를 위해 `apiResource` 메서드를 사용하면 이 두 라우트를 자동으로 제외할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

마찬가지로, 배열을 전달해 여러 API 리소스 컨트롤러를 동시에 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`make:controller` 명령어를 실행할 때 `--api` 스위치를 주면, `create`나 `edit` 메서드가 없는 API 리소스 컨트롤러를 바로 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스

때로는 중첩 리소스에 대한 라우트를 정의해야 할 때가 있습니다. 예를 들어, 하나의 사진 리소스에 여러 개의 댓글이 연결될 수 있습니다. 중첩 리소스 컨트롤러는 라우트 정의에서 "점(.) 표기법"을 사용해 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 아래와 같은 URI로 중첩 리소스에 접근할 수 있도록 등록합니다:

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 스코프 지정

라라벨의 [암묵적 모델 바인딩](/docs/12.x/routing#implicit-model-binding-scoping) 기능은 중첩된 바인딩을 자동으로 스코프 처리해, 자식 모델이 상위 모델에 실제로 속하는지 확인할 수 있습니다. 중첩 리소스 정의 시 `scoped` 메서드를 사용하면 자동 스코프 기능을 활성화하고, 자식 리소스를 어떤 필드로 조회할지 지정할 수 있습니다. 구체적인 방법은 [리소스 라우트 스코프 지정](#restful-scoping-resource-routes) 문서를 참고하십시오.

<a name="shallow-nesting"></a>
#### 얕은 중첩(Shallow Nesting)

많은 경우, URI에서 상위와 하위 ID를 모두 포함할 필요는 없습니다. 자식 ID가 이미 고유하다면, 오토 인크리먼트 PK 등으로 URI 세그먼트에서 모델을 식별할 때 "shallow nesting"을 사용할 수 있습니다:

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

이렇게 하면 아래와 같은 라우트들이 정의됩니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                                 | 액션    | 라우트 이름                |
| ----------- | ----------------------------------- | ------- | -------------------------- |
| GET         | `/photos/{photo}/comments`          | index   | photos.comments.index      |
| GET         | `/photos/{photo}/comments/create`   | create  | photos.comments.create     |
| POST        | `/photos/{photo}/comments`          | store   | photos.comments.store      |
| GET         | `/comments/{comment}`               | show    | comments.show              |
| GET         | `/comments/{comment}/edit`          | edit    | comments.edit              |
| PUT/PATCH   | `/comments/{comment}`               | update  | comments.update            |
| DELETE      | `/comments/{comment}`               | destroy | comments.destroy           |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정

기본적으로, 모든 리소스 컨트롤러의 액션에는 라우트 이름이 자동으로 지정됩니다. 하지만 원하는 라우트 이름을 `names` 배열로 전달해 직접 지정할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정

`Route::resource`는 기본적으로 리소스 이름의 "단수형"을 사용하여 라우트 파라미터를 생성합니다. 특정 리소스에 대해 이를 오버라이드하려면 `parameters` 메서드로 쉽게 재정의할 수 있습니다. 이때 매개변수로 전달하는 배열은 리소스명과 원하는 파라미터명을 매핑하는 형태의 연관 배열이어야 합니다:

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예제는 아래와 같은 URI를 `show` 라우트로 생성합니다:

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코프 지정

라라벨의 [스코프 암묵적 모델 바인딩](/docs/12.x/routing#implicit-model-binding-scoping) 기능은 중첩된 바인딩에서 자식 모델이 실제로 상위 모델에 속하는지 자동으로 확인해줍니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면, 자동 스코프는 물론 자식 리소스를 어떤 필드로 조회할지도 지정할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이렇게 하면 아래와 같은 URI로 스코프된 중첩 리소스에 접근할 수 있게 됩니다:

```text
/photos/{photo}/comments/{comment:slug}
```

중첩 라우트 파라미터로 커스텀 키 암묵적 바인딩을 사용할 때, 라라벨은 부모 모델의 관계명을 추론하여 자동으로 쿼리를 스코프 처리합니다. 이 경우, `Photo` 모델에는 `comments`라는 이름의 관계(라우트 파라미터의 복수형)가 있다고 가정합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화

기본적으로, `Route::resource`는 리소스 URI를 영어 동사와 복수 규칙에 따라 생성합니다. 만약 `create`와 `edit` 동작 등의 action 동사를 현지화해야 한다면, `Route::resourceVerbs` 메서드를 사용할 수 있습니다. 이 코드는 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드 시작 부분에 작성하면 됩니다:

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

라라벨의 pluralizer(복수화 도구)는 [여러 언어를 지원하며, 필요에 따라 설정할 수 있습니다](/docs/12.x/localization#pluralization-language). 이렇게 동사와 복수화 언어를 커스터마이즈한 후에 `Route::resource('publicacion', PublicacionController::class)`와 같이 리소스 라우트를 등록하면, 다음과 같은 URI가 생성됩니다:

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보완하기

리소스 컨트롤러에 기본 리소스 라우트 외에 추가 라우트를 정의할 필요가 있다면, 이러한 추가 라우트를 `Route::resource` 메서드보다 먼저 정의해야 합니다. 그렇지 않으면, `resource` 메서드가 생성하는 라우트가 의도치 않게 여러분이 정의한 추가 라우트보다 앞서 우선권을 가질 수 있습니다:

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러는 한 가지 역할에 집중하도록 유지하는 것이 좋습니다. 만약 일반적인 리소스 액션 이외의 메서드가 자주 추가된다면, 두 개의 더 작은 컨트롤러로 분리할 것을 고려해보세요.

<a name="singleton-resource-controllers"></a>
### 싱글턴 리소스 컨트롤러

어떤 경우, 애플리케이션에서 한 인스턴스만 존재하는 리소스가 있을 수 있습니다. 예를 들어, 사용자의 "프로필"은 수정이나 갱신이 가능하지만, 한 명의 사용자는 여러 개의 "프로필"을 가질 수 없습니다. 이처럼 하나의 리소스 인스턴스만 허용되는 경우(예: 이미지의 "썸네일" 등), "싱글턴 리소스" 컨트롤러로 등록할 수 있습니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위 싱글턴 리소스 정의는 아래와 같은 라우트를 등록합니다. 알 수 있듯, 생성 관련 라우트는 등록되지 않으며, URI에 식별자를 포함하지 않습니다(리소스 인스턴스가 오직 하나이기 때문입니다):

<div class="overflow-auto">

| HTTP 메서드 | URI              | 액션   | 라우트 이름         |
| ----------- | ---------------- | ------ | ------------------- |
| GET         | `/profile`       | show   | profile.show        |
| GET         | `/profile/edit`  | edit   | profile.edit        |
| PUT/PATCH   | `/profile`       | update | profile.update      |

</div>

싱글턴 리소스는 일반 리소스 내부에 중첩으로 추가하는 것도 가능합니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 예시에서 `photos` 리소스는 [일반 리소스 라우트](#actions-handled-by-resource-controllers)를 모두 받게 되지만, `thumbnail`은 아래와 같은 싱글턴 라우트를 가지게 됩니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                                 | 액션   | 라우트 이름                  |
| ----------- | ----------------------------------- | ------ | ---------------------------- |
| GET         | `/photos/{photo}/thumbnail`         | show   | photos.thumbnail.show        |
| GET         | `/photos/{photo}/thumbnail/edit`    | edit   | photos.thumbnail.edit        |
| PUT/PATCH   | `/photos/{photo}/thumbnail`         | update | photos.thumbnail.update      |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글턴 리소스

가끔은 싱글턴 리소스에 대해 생성 및 저장 라우트도 정의하고 싶을 수 있습니다. 이러한 경우, 싱글턴 리소스 라우트 등록 시 `creatable` 메서드를 호출해주면 됩니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이렇게 하면 아래와 같은 라우트들이 추가로 등록됩니다. 참고로, `DELETE` 라우트도 생성 가능한 싱글턴 리소스에 대해 등록됩니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                                    | 액션    | 라우트 이름                 |
| ----------- | -------------------------------------- | ------- | --------------------------  |
| GET         | `/photos/{photo}/thumbnail/create`     | create  | photos.thumbnail.create     |
| POST        | `/photos/{photo}/thumbnail`            | store   | photos.thumbnail.store      |
| GET         | `/photos/{photo}/thumbnail`            | show    | photos.thumbnail.show       |
| GET         | `/photos/{photo}/thumbnail/edit`       | edit    | photos.thumbnail.edit       |
| PUT/PATCH   | `/photos/{photo}/thumbnail`            | update  | photos.thumbnail.update     |
| DELETE      | `/photos/{photo}/thumbnail`            | destroy | photos.thumbnail.destroy    |

</div>

싱글턴 리소스에 대해 `DELETE` 라우트만 등록하고, 생성/저장 라우트는 등록하지 않으려면 `destroyable` 메서드를 사용할 수 있습니다:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글턴 리소스

`apiSingleton` 메서드를 사용하면 API에서 관리하는 싱글턴 리소스를 등록할 수 있으며, 이 경우 `create`와 `edit` 라우트는 등록되지 않습니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론, API 싱글턴 리소스도 `creatable`로 생성 및 저장 라우트를 등록할 수 있습니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="middleware-and-resource-controllers"></a>
### 미들웨어와 리소스 컨트롤러

라라벨에서는 `middleware`, `middlewareFor`, `withoutMiddlewareFor` 메서드를 통해 리소스 라우트의 전역 또는 특정 메서드에 미들웨어를 적용할 수 있습니다. 이 덕분에 각 리소스 액션별로 어느 미들웨어를 적용할지 세밀하게 제어할 수 있습니다.

#### 모든 메서드에 미들웨어 적용하기

`middleware` 메서드를 사용하면 리소스 또는 싱글턴 리소스 라우트 전체에 미들웨어를 적용할 수 있습니다:

```php
Route::resource('users', UserController::class)
    ->middleware(['auth', 'verified']);

Route::singleton('profile', ProfileController::class)
    ->middleware('auth');
```

#### 특정 메서드에만 미들웨어 적용하기

`middlewareFor` 메서드는 주어진 리소스 컨트롤러의 한 개 또는 여러 액션에만 미들웨어를 적용할 수 있습니다:

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

싱글턴 및 API 싱글턴 리소스 컨트롤러와 함께 사용할 수도 있습니다:

```php
Route::singleton('profile', ProfileController::class)
    ->middlewareFor('show', 'auth');

Route::apiSingleton('profile', ProfileController::class)
    ->middlewareFor(['show', 'update'], 'auth');
```

#### 특정 메서드에서 미들웨어 제외하기

`withoutMiddlewareFor` 메서드로 리소스 컨트롤러 특정 동작에서 미들웨어를 제외할 수 있습니다:

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
#### 생성자 주입

라라벨의 [서비스 컨테이너](/docs/12.x/container)는 모든 라라벨 컨트롤러를 해결(실행)할 때 사용됩니다. 결과적으로, 컨트롤러 생성자에 필요한 의존성을 타입힌트로 선언할 수 있으며, 선언된 의존성은 자동으로 주입됩니다:

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
#### 메서드 인젝션

생성자 주입 외에도, 컨트롤러의 개별 메서드에 의존성을 타입힌트로 선언할 수도 있습니다. `Illuminate\Http\Request` 인스턴스를 액션별로 직접 주입하는 것이 대표적인 예입니다:

```php
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

컨트롤러 메서드에서 라우트 파라미터의 입력 값도 필요한 경우, 다른 의존성 뒤에 해당 파라미터를 나열하면 됩니다. 예를 들어, 아래와 같이 라우트를 정의했다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메서드에서는 아래처럼 `Illuminate\Http\Request`와 함께 `id` 파라미터도 받을 수 있습니다:

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
        // 사용자 업데이트 로직...

        return redirect('/users');
    }
}
```