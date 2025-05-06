# 컨트롤러

- [소개](#introduction)
- [컨트롤러 작성](#writing-controllers)
    - [기본 컨트롤러](#basic-controllers)
    - [단일 액션 컨트롤러](#single-action-controllers)
- [컨트롤러 미들웨어](#controller-middleware)
- [리소스 컨트롤러](#resource-controllers)
    - [부분 리소스 라우트](#restful-partial-resource-routes)
    - [중첩 리소스](#restful-nested-resources)
    - [리소스 라우트 이름 지정](#restful-naming-resource-routes)
    - [리소스 라우트 파라미터 이름 지정](#restful-naming-resource-route-parameters)
    - [리소스 라우트 스코프 지정](#restful-scoping-resource-routes)
    - [리소스 URI 지역화](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 보완](#restful-supplementing-resource-controllers)
    - [싱글톤 리소스 컨트롤러](#singleton-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개

모든 요청 처리 로직을 라우트 파일에서 클로저로 정의하는 대신, "컨트롤러" 클래스를 사용하여 이러한 행위를 더 체계적으로 구성할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스로 묶을 수 있습니다. 예를 들어, `UserController` 클래스는 사용자 관련 요청(조회, 생성, 수정, 삭제 등)을 모두 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성

<a name="basic-controllers"></a>
### 기본 컨트롤러

새 컨트롤러를 빠르게 생성하려면 `make:controller` 아티즌 명령어를 사용할 수 있습니다. 기본적으로, 모든 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다:

```shell
php artisan make:controller UserController
```

기본 컨트롤러의 예시를 살펴보겠습니다. 컨트롤러는 들어오는 HTTP 요청에 응답하는 공개(public) 메서드를 여러 개 가질 수 있습니다:

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

컨트롤러 클래스와 메서드 작성이 끝났다면, 다음과 같이 컨트롤러 메서드에 대한 라우트를 정의할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

들어오는 요청이 지정된 라우트 URI와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고 라우트 파라미터가 해당 메서드로 전달됩니다.

> [!NOTE]
> 컨트롤러가 **반드시** 기본 클래스를 확장할 필요는 없습니다. 하지만 모든 컨트롤러에서 공통적으로 사용하는 메서드를 포함한 기본 컨트롤러 클래스를 확장하는 것이 편리할 수 있습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러

특정 컨트롤러 액션이 특별히 복잡하다면, 해당 액션 전용 컨트롤러 클래스를 만드는 것이 편리할 수 있습니다. 이를 위해 컨트롤러 내에 단일 `__invoke` 메서드를 정의하면 됩니다:

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

단일 액션 컨트롤러의 라우트를 등록할 때는 컨트롤러 메서드를 명시할 필요가 없습니다. 컨트롤러의 이름만 라우터에 전달하면 됩니다:

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` 아티즌 명령어의 `--invokable` 옵션을 사용하여 단일 호출 컨트롤러를 생성할 수도 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

[미들웨어](/docs/{{version}}/middleware)는 라우트 파일에서 컨트롤러의 라우트에 지정할 수 있습니다:

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

또는, 컨트롤러 클래스 내에서 미들웨어를 지정하는 것이 더 편리할 수도 있습니다. 이를 위해 컨트롤러가 `HasMiddleware` 인터페이스를 구현해야 하며, 정적 `middleware` 메서드를 가져야 합니다. 이 메서드에서 컨트롤러의 액션에 적용할 미들웨어 배열을 반환할 수 있습니다:

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

클로저로 컨트롤러 미들웨어를 정의할 수도 있습니다. 이렇게 하면 전체 미들웨어 클래스를 작성하지 않고도 인라인 미들웨어를 간편하게 정의할 수 있습니다:

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
> `Illuminate\Routing\Controllers\HasMiddleware`를 구현하는 컨트롤러는 `Illuminate\Routing\Controller`를 확장하지 않아야 합니다.

<a name="resource-controllers"></a>
## 리소스 컨트롤러

애플리케이션의 각 Eloquent 모델을 "리소스"로 생각한다면, 일반적으로 각 리소스마다 동일한 종류의 작업을 수행합니다. 예를 들어, `Photo` 모델과 `Movie` 모델이 있다면, 사용자들은 이 리소스들을 생성, 조회, 수정, 삭제할 수 있습니다.

이러한 일반적인 사용 사례 때문에, Laravel 리소스 라우팅은 한 줄의 코드로 일반적인 생성, 조회, 수정, 삭제("CRUD") 라우트를 컨트롤러에 할당할 수 있습니다. 시작하려면, `make:controller` 아티즌 명령어에서 `--resource` 옵션을 사용하여 이러한 작업을 처리하는 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

이 명령어는 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성합니다. 컨트롤러에는 각각의 리소스 작업을 처리하는 메서드가 포함되어 있습니다. 다음으로, 이 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 한 줄의 라우트 선언으로 다양한 작업을 처리하는 여러 라우트가 생성됩니다. 생성된 컨트롤러에는 각 작업을 위한 메서드 스텁이 이미 들어 있습니다. 참고로, `route:list` 아티즌 명령어를 실행하면 애플리케이션 라우트를 한눈에 확인할 수 있습니다.

여러 리소스 컨트롤러를 동시에 등록하려면 배열을 `resources` 메서드에 전달할 수 있습니다:

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션

<div class="overflow-auto">

| 메서드      | URI                    | 액션   | 라우트 이름         |
| ---------   | ---------------------- | -------| ------------------- |
| GET         | `/photos`              | index  | photos.index        |
| GET         | `/photos/create`       | create | photos.create       |
| POST        | `/photos`              | store  | photos.store        |
| GET         | `/photos/{photo}`      | show   | photos.show         |
| GET         | `/photos/{photo}/edit` | edit   | photos.edit         |
| PUT/PATCH   | `/photos/{photo}`      | update | photos.update       |
| DELETE      | `/photos/{photo}`      | destroy| photos.destroy      |

</div>

<a name="customizing-missing-model-behavior"></a>
#### 모델 미존재 시 동작 커스터마이징

일반적으로, 묵시적으로 바인딩된 리소스 모델을 찾지 못한 경우 404 HTTP 응답이 생성됩니다. 하지만, 리소스 라우트를 정의할 때 `missing` 메서드를 호출하여 이 동작을 커스터마이징할 수 있습니다. `missing` 메서드는 묵시적으로 바인딩된 모델을 해당 라우트에서 찾을 수 없을 경우 실행할 클로저를 받습니다:

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

일반적으로, [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)된 모델은 묵시적 모델 바인딩에서 반환되지 않으며, 대신 404 HTTP 응답이 반환됩니다. 하지만, 리소스 라우트를 정의할 때 `withTrashed` 메서드를 호출하여 소프트 삭제된 모델도 허용할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

인자를 전달하지 않고 `withTrashed`를 호출하면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델도 허용합니다. 배열을 인자로 넘기면 특정 라우트만 지정할 수 있습니다:

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정

[라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)를 사용하고 리소스 컨트롤러의 메서드에서 모델 인스턴스를 타입힌트하고 싶다면, 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 요청 생성

리소스 컨트롤러를 생성할 때 `--requests` 옵션을 제공하면, 컨트롤러의 저장 및 수정 메서드용 [폼 요청 클래스](/docs/{{version}}/validation#form-request-validation)가 자동으로 생성됩니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트를 선언할 때, 컨트롤러가 처리해야 할 액션의 일부만 지정할 수 있습니다:

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

API에서 사용할 리소스 라우트를 선언할 때는 `create`와 `edit`와 같이 HTML 템플릿을 제공하는 라우트는 보통 제외합니다. 편의를 위해 `apiResource` 메서드를 사용하면 이 두 라우트를 자동으로 제외할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

여러 API 리소스 컨트롤러를 동시에 등록하려면 배열을 `apiResources` 메서드에 전달할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`make:controller` 명령어 실행 시 `--api` 옵션을 사용하면 `create` 및 `edit` 메서드를 포함하지 않는 API 리소스 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스

때로는 중첩 리소스에 대한 라우트를 정의해야 할 수도 있습니다. 예를 들어, 사진(photo) 리소스에 여러 개의 댓글(comment)이 있을 수 있습니다. 리소스 컨트롤러를 중첩하려면, 라우트 선언에서 "점(dot) 표기법"을 사용할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 URI로 중첩 리소스를 사용할 수 있게 등록합니다:

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스의 스코프 지정

Laravel의 [묵시적 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능은 자식 모델이 부모 모델에 속하는지 자동으로 확인하는 중첩 바인딩 스코프를 지원합니다. 중첩 리소스 정의 시 `scoped` 메서드를 사용하면 자동 스코프 지정을 활성화할 수 있으며, 자식 리소스를 어떤 필드로 조회할지 Laravel에 지시할 수 있습니다. 자세한 방법은 [리소스 라우트 스코프 지정](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 얕은 중첩(Shallow Nesting)

흔히 자식 ID가 이미 고유 식별자라면 URI에 부모 ID와 자식 ID를 모두 포함할 필요가 없습니다. URI 세그먼트에서 자동 증가 기본 키와 같은 고유 식별자를 사용할 때, "얕은 중첩" 옵션을 사용할 수 있습니다:

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

이 라우트 정의는 다음과 같은 라우트를 만듭니다:

<div class="overflow-auto">

| 메서드      | URI                               | 액션   | 라우트 이름                 |
| ---------   | --------------------------------- | -------| -------------------------- |
| GET         | `/photos/{photo}/comments`        | index  | photos.comments.index      |
| GET         | `/photos/{photo}/comments/create` | create | photos.comments.create     |
| POST        | `/photos/{photo}/comments`        | store  | photos.comments.store      |
| GET         | `/comments/{comment}`             | show   | comments.show              |
| GET         | `/comments/{comment}/edit`        | edit   | comments.edit              |
| PUT/PATCH   | `/comments/{comment}`             | update | comments.update            |
| DELETE      | `/comments/{comment}`             | destroy| comments.destroy           |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정

기본적으로 모든 리소스 컨트롤러 액션에는 라우트 이름이 지정됩니다. 그러나 원하는 라우트 이름의 `names` 배열을 전달하여 이를 덮어쓸 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정

기본적으로 `Route::resource`는 리소스 라우트의 파라미터 이름을 리소스 이름의 "단수형"으로 생성합니다. 하지만 `parameters` 메서드를 사용해 리소스별로 쉽게 오버라이드할 수 있습니다. `parameters`에 전달하는 배열은 리소스 이름과 파라미터 이름의 연관 배열이어야 합니다:

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예제는 리소스 `show` 라우트에 대해 다음과 같은 URI를 생성합니다:

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코프 지정

Laravel의 [스코프가 적용된 묵시적 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능을 사용하면, 자식 모델이 부모 모델에 속하는지 자동으로 확인할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 스코프 지정 및 자식 리소스의 검색 필드를 지정할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 다음과 같은 URI로 스코프가 적용된 중첩 리소스를 등록합니다:

```text
/photos/{photo}/comments/{comment:slug}
```

중첩 라우트 파라미터에 커스텀 키 기반의 묵시적 바인딩을 사용할 때, Laravel은 부모와의 관계명을 컨벤션에 따라 자동으로 유추하여 자식 모델을 조회할 때 쿼리를 스코프 처리합니다. 이 예제에서 `Photo` 모델은 `comments`라는 관계(파라미터 이름의 복수형)를 가지고 있다고 가정합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 지역화

기본적으로, `Route::resource`는 리소스 URI를 영어 동사와 복수 규칙으로 생성합니다. `create`와 `edit` 액션 동사를 지역화해야 하는 경우 `Route::resourceVerbs` 메서드를 이용할 수 있습니다. 이 작업은 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드 초입에서 할 수 있습니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);
}
```

Laravel의 복수화 도구는 [여러 다른 언어를 지원하며, 필요에 따라 설정할 수 있습니다](/docs/{{version}}/localization#pluralization-language). 동사 및 복수화 언어를 커스터마이즈하면, `Route::resource('publicacion', PublicacionController::class)`와 같은 리소스 라우트 등록은 다음과 같은 URI를 생성합니다:

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보완

기본 리소스 라우트 세트 이외에 추가 라우트를 리소스 컨트롤러에 정의해야 하는 경우, `Route::resource` 호출 **이전**에 해당 라우트를 먼저 정의해야 합니다. 그렇지 않으면, `resource` 메서드가 정의한 라우트가 보완적 라우트보다 우선해버릴 수 있습니다:

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러의 관심사를 명확히 유지하세요. 만약 기본 리소스 액션 외에 자주 추가 메서드가 필요하다면 컨트롤러를 두 개로 분리하는 것을 고려하세요.

<a name="singleton-resource-controllers"></a>
### 싱글톤 리소스 컨트롤러

애플리케이션에 단 하나의 인스턴스만 존재할 수 있는 리소스가 있을 수 있습니다. 예를 들어, 사용자의 "프로필"은 수정 또는 업데이트할 수 있지만, 한 사용자는 프로필을 하나만 가질 수 있습니다. 마찬가지로, 이미지에는 하나의 "섬네일"만 있을 수 있습니다. 이런 리소스를 "싱글톤 리소스"라고 하며 한 인스턴스만 존재할 수 있음을 의미합니다. 이런 경우에는 "싱글톤" 리소스 컨트롤러를 등록할 수 있습니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위 싱글톤 리소스 정의는 다음과 같은 라우트를 등록합니다. "생성" 라우트는 등록되지 않으며 하나의 인스턴스이므로 식별자를 받지 않습니다:

<div class="overflow-auto">

| 메서드      | URI             | 액션  | 라우트 이름       |
| ---------   | --------------- | ------| ----------------- |
| GET         | `/profile`      | show  | profile.show      |
| GET         | `/profile/edit` | edit  | profile.edit      |
| PUT/PATCH   | `/profile`      | update| profile.update    |

</div>

싱글톤 리소스는 일반 리소스 내에 중첩시킬 수도 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 경우, `photos` 리소스에는 [표준 리소스 라우트](#actions-handled-by-resource-controllers)가 모두 생성되지만, `thumbnail` 리소스에는 싱글톤 리소스용 라우트가 생성됩니다:

<div class="overflow-auto">

| 메서드      | URI                              | 액션  | 라우트 이름                 |
| ---------   | -------------------------------- | ------| -------------------------- |
| GET         | `/photos/{photo}/thumbnail`      | show  | photos.thumbnail.show      |
| GET         | `/photos/{photo}/thumbnail/edit` | edit  | photos.thumbnail.edit      |
| PUT/PATCH   | `/photos/{photo}/thumbnail`      | update| photos.thumbnail.update    |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글톤 리소스

가끔은 싱글톤 리소스에 대해 생성 및 저장 라우트도 필요할 수 있습니다. 이 경우, 싱글톤 리소스 라우트를 등록할 때 `creatable` 메서드를 호출하면 됩니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이 예시에서는 다음과 같은 라우트들이 등록됩니다. 생성 가능한 싱글톤 리소스에는 `DELETE` 라우트도 등록됩니다:

<div class="overflow-auto">

| 메서드      | URI                                | 액션   | 라우트 이름                  |
| ---------   | ---------------------------------- | -------| ---------------------------- |
| GET         | `/photos/{photo}/thumbnail/create` | create | photos.thumbnail.create      |
| POST        | `/photos/{photo}/thumbnail`        | store  | photos.thumbnail.store       |
| GET         | `/photos/{photo}/thumbnail`        | show   | photos.thumbnail.show        |
| GET         | `/photos/{photo}/thumbnail/edit`   | edit   | photos.thumbnail.edit        |
| PUT/PATCH   | `/photos/{photo}/thumbnail`        | update | photos.thumbnail.update      |
| DELETE      | `/photos/{photo}/thumbnail`        | destroy| photos.thumbnail.destroy     |

</div>

싱글톤 리소스에 대해 `DELETE` 라우트만 등록하고 생성/저장 라우트는 원치 않는 경우, `destroyable` 메서드를 사용할 수 있습니다:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글톤 리소스

`apiSingleton` 메서드를 사용하면 API를 통한 조작에 사용할 싱글톤 리소스를 등록할 수 있으며, 이 경우 `create`와 `edit` 라우트는 등록되지 않습니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론, API 싱글톤 리소스도 `creatable`로써 생성 및 삭제 라우트를 등록할 수 있습니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러

<a name="constructor-injection"></a>
#### 생성자 주입

Laravel의 [서비스 컨테이너](/docs/{{version}}/container)는 모든 컨트롤러를 해석(인스턴스화)하는 데 사용됩니다. 따라서 컨트롤러의 생성자에서 필요한 의존성을 타입힌트로 지정할 수 있습니다. 지정된 의존성은 자동으로 해석되어 컨트롤러 인스턴스에 주입됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * 새 컨트롤러 인스턴스 생성.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}
}
```

<a name="method-injection"></a>
#### 메서드 주입

생성자 주입 외에도, 컨트롤러의 메서드에서 의존성을 타입힌트로 지정할 수 있습니다. 일반적인 예로, 컨트롤러 메서드에 `Illuminate\Http\Request` 인스턴스를 주입하는 것이 있습니다:

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

        // 사용자 저장...

        return redirect('/users');
    }
}
```

컨트롤러 메서드에서 라우트 파라미터 입력도 필요한 경우, 의존성 인자 뒤에 라우트 인자를 나열하면 됩니다. 예를 들어, 다음과 같이 라우트를 정의했다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메서드에서 `Illuminate\Http\Request` 타입힌트 및 `id` 파라미터도 아래와 같이 받을 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 주어진 사용자를 수정합니다.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 변경...

        return redirect('/users');
    }
}
```