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
    - [리소스 라우트 범위 지정](#restful-scoping-resource-routes)
    - [리소스 URI 현지화](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 보완](#restful-supplementing-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개 (Introduction)

라우트 파일 내에서 모든 요청 처리 로직을 클로저로 정의하는 대신, "컨트롤러" 클래스를 활용해 이 동작을 체계적으로 구성할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스로 묶어 관리할 수 있습니다. 예를 들어, `UserController` 클래스는 사용자의 조회, 생성, 수정, 삭제와 관련된 모든 요청을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기 (Writing Controllers)

<a name="basic-controllers"></a>
### 기본 컨트롤러 (Basic Controllers)

기본 컨트롤러의 예제를 살펴보겠습니다. 컨트롤러는 Laravel에서 제공하는 기본 컨트롤러 클래스를 상속하는 점에 주의하세요: `App\Http\Controllers\Controller`:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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

위 컨트롤러 메서드에 대응하는 라우트를 다음과 같이 정의할 수 있습니다:

```
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

요청이 지정한 라우트 URI와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고 라우트 파라미터가 해당 메서드에 전달됩니다.

> [!TIP]
> 컨트롤러가 반드시 기본 클래스를 상속해야 하는 것은 아닙니다. 다만, `middleware`나 `authorize` 같은 편리한 기능을 사용하려면 기본 클래스를 상속해야 합니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러 (Single Action Controllers)

특정 컨트롤러 액션이 매우 복잡할 경우, 해당 단일 액션을 전담하는 컨트롤러 클래스를 만드는 것이 편리할 수 있습니다. 이를 위해 컨트롤러에 단 하나의 `__invoke` 메서드를 정의할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;

class ProvisionServer extends Controller
{
    /**
     * 새로운 웹 서버를 프로비저닝합니다.
     *
     * @return \Illuminate\Http\Response
     */
    public function __invoke()
    {
        // ...
    }
}
```

단일 액션 컨트롤러의 라우트를 등록할 때는 컨트롤러 메서드를 지정할 필요 없이, 컨트롤러 클래스명만 라우터에 전달하면 됩니다:

```
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` Artisan 명령어의 `--invokable` 옵션을 사용해 단일 액션 컨트롤러를 생성할 수 있습니다:

```
php artisan make:controller ProvisionServer --invokable
```

> [!TIP]
> 컨트롤러 스텁은 [스텁 공개(stub publishing)](/docs/{{version}}/artisan#stub-customization)을 통해 사용자 정의할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어 (Controller Middleware)

[미들웨어](/docs/{{version}}/middleware)는 라우트 파일에서 컨트롤러에 할당할 수 있습니다:

```
Route::get('profile', [UserController::class, 'show'])->middleware('auth');
```

컨트롤러 생성자 내부에서 미들웨어를 지정하는 것도 편리합니다. 컨트롤러 생성자 내 `middleware` 메서드를 사용하여 컨트롤러 액션에 미들웨어를 할당할 수 있습니다:

```
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

컨트롤러는 클로저를 이용한 미들웨어 등록도 지원합니다. 이는 별도의 미들웨어 클래스를 정의하지 않고 단일 컨트롤러에 인라인 미들웨어를 정의하는 편리한 방법입니다:

```
$this->middleware(function ($request, $next) {
    return $next($request);
});
```

<a name="resource-controllers"></a>
## 리소스 컨트롤러 (Resource Controllers)

애플리케이션의 각 Eloquent 모델을 "리소스"라고 생각할 때, 보통 각 리소스에 대해 동일한 종류의 작업(생성, 조회, 수정, 삭제 등)을 수행합니다. 예를 들어, `Photo` 모델과 `Movie` 모델이 있다면 사용자들이 이 리소스들을 생성하고, 읽고, 업데이트하고, 삭제할 수 있을 것입니다.

이런 공통적인 요구사항을 위해 Laravel의 리소스 라우팅은 단 한 줄의 코드로 컨트롤러에 기본적인 CRUD(create, read, update, delete) 라우트를 할당합니다. 시작하려면 `make:controller` Artisan 명령어의 `--resource` 옵션을 사용해 이러한 작업을 처리하는 컨트롤러를 빠르게 생성할 수 있습니다:

```
php artisan make:controller PhotoController --resource
```

이 명령어는 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성하며, 각 리소스 작업을 위한 메서드를 포함합니다. 그리고 다음과 같이 리소스 라우트를 등록할 수 있습니다:

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 단일 라우트 선언은 리소스에서 다양한 작업을 처리할 여러 라우트를 생성합니다. 생성된 컨트롤러는 이들 각 작업에 대응하는 메서드를 기본적으로 포함합니다. 항상 `route:list` Artisan 명령어를 통해 애플리케이션의 라우트 전체를 빠르게 확인할 수 있습니다.

여러 리소스 컨트롤러를 한꺼번에 배열 형태로 `resources` 메서드에 전달해 등록할 수도 있습니다:

```
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controller"></a>
#### 리소스 컨트롤러가 처리하는 작업들

동사      | URI                    | 액션       | 라우트 이름
----------|------------------------|------------|---------------------
GET       | `/photos`              | index      | photos.index
GET       | `/photos/create`       | create     | photos.create
POST      | `/photos`              | store      | photos.store
GET       | `/photos/{photo}`      | show       | photos.show
GET       | `/photos/{photo}/edit` | edit       | photos.edit
PUT/PATCH | `/photos/{photo}`      | update     | photos.update
DELETE    | `/photos/{photo}`      | destroy    | photos.destroy

<a name="customizing-missing-model-behavior"></a>
#### 모델 미발견 동작 커스터마이징 (Customizing Missing Model Behavior)

통상적으로, 암묵적 모델 바인딩이 실패하면 404 HTTP 응답이 반환됩니다. 하지만, 리소스 라우트를 정의할 때 `missing` 메서드를 호출하여 이 동작을 커스터마이징할 수 있습니다. `missing` 메서드는 암묵적으로 바인딩된 모델을 찾을 수 없을 때 호출할 클로저를 인수로 받습니다:

```
use App\Http\Controllers\PhotoController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::resource('photos', PhotoController::class)
        ->missing(function (Request $request) {
            return Redirect::route('photos.index');
        });
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정하기 (Specifying The Resource Model)

[라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 사용하면서 리소스 컨트롤러 메서드에 모델 인스턴스를 타입힌트하고 싶다면 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다:

```
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 리퀘스트 생성 (Generating Form Requests)

`--requests` 옵션을 제공하면 리소스 컨트롤러의 저장 및 업데이트 메서드에서 사용할 [폼 리퀘스트 클래스](/docs/{{version}}/validation#form-request-validation)를 함께 생성하도록 Artisan에 지시할 수 있습니다:

```
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트 (Partial Resource Routes)

리소스 라우트를 선언할 때 기본 액션 전체 집합 대신 특정 액션들만 지정할 수도 있습니다:

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
#### API 리소스 라우트 (API Resource Routes)

API에서 사용되는 리소스 라우트의 경우 일반적으로 `create`나 `edit` 처럼 HTML 템플릿을 반환하는 라우트는 제외하고 싶을 때가 많습니다. 이럴 때 편리하게 `apiResource` 메서드를 사용하면 이 두 라우트를 자동 제외할 수 있습니다:

```
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

여러 API 리소스 컨트롤러도 `apiResources` 메서드에 배열로 한꺼번에 등록할 수 있습니다:

```
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`make:controller` 명령어를 실행할 때 `--api` 옵션을 사용하면 `create` 및 `edit` 메서드를 제외한 API 리소스 컨트롤러를 빠르게 생성할 수 있습니다:

```
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스 (Nested Resources)

가끔 중첩된 리소스 라우트를 정의해야 할 때가 있습니다. 예를 들어, 사진 리소스에 여러 댓글이 연관되어 있다면, 중첩 리소스 컨트롤러를 정의할 때 라우트 선언에서 "dot" 표기법을 사용할 수 있습니다:

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 URI로 접근 가능한 중첩 리소스를 등록합니다:

```
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 범위 지정 (Scoping Nested Resources)

Laravel의 [암묵적 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능은 자동으로 중첩된 바인딩에 대해 부모 모델에 속하는지 검증하는 범위 지정(scoping)을 지원합니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 범위 지정과 자식 리소스를 조회할 필드를 지정할 수 있습니다. 자세한 내용은 [리소스 라우트 범위 지정](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 얕은 중첩 (Shallow Nesting)

URI 내에 부모와 자식 ID가 모두 포함되는 것이 항상 필요한 것은 아닙니다. 자식 ID가 이미 고유 식별자라면, "얕은 중첩"을 사용해 자식 ID만 URI에 포함시키는 것도 가능합니다. 자동 증가하는 기본키 같은 고유 식별자를 URI 세그먼트에 사용할 때 적합합니다:

```
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

이 라우트 정의는 다음과 같이 작동합니다:

동사      | URI                               | 액션       | 라우트 이름
----------|-----------------------------------|------------|---------------------
GET       | `/photos/{photo}/comments`        | index      | photos.comments.index
GET       | `/photos/{photo}/comments/create` | create     | photos.comments.create
POST      | `/photos/{photo}/comments`        | store      | photos.comments.store
GET       | `/comments/{comment}`             | show       | comments.show
GET       | `/comments/{comment}/edit`        | edit       | comments.edit
PUT/PATCH | `/comments/{comment}`             | update     | comments.update
DELETE    | `/comments/{comment}`             | destroy    | comments.destroy

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정 (Naming Resource Routes)

기본적으로 모든 리소스 컨트롤러 액션에는 라우트 이름이 지정됩니다. 하지만 `names` 배열을 전달하여 원하는 라우트 이름으로 재정의할 수 있습니다:

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정 (Naming Resource Route Parameters)

기본적으로 `Route::resource`는 리소스 이름의 단수형을 기반으로 라우트 파라미터 이름을 생성합니다. `parameters` 메서드를 이용해 리소스별로 라우트 파라미터 이름을 쉽게 재정의할 수 있습니다. `parameters` 메서드에 전달하는 배열은 리소스 이름과 파라미터 이름을 키:값으로 매핑한 연관 배열이어야 합니다:

```
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예시에서는 `show` 라우트에 대해 다음 URI가 생성됩니다:

```
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 범위 지정 (Scoping Resource Routes)

Laravel의 [암묵적 범위 지정 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능은 중첩된 바인딩에 대해 부모 모델에 속하는지를 검증하는 범위 지정 기능을 지원합니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 범위 지정을 활성화하고, 자식 리소스를 조회할 필드를 직접 지정할 수 있습니다:

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

위와 같은 라우트는 다음 URI로 접근하는 범위 지정 중첩 리소스를 등록합니다:

```
/photos/{photo}/comments/{comment:slug}
```

중첩 라우트 파라미터로 커스텀 키를 사용하는 경우, Laravel은 부모 모델의 연관관계 이름을 추론하여 중첩 모델을 부모로 제한하는 범위 지정 쿼리를 자동 생성합니다. 이 경우 `Photo` 모델에 `comments`라는 연관관계가 있다고 가정합니다(라우트 파라미터 이름의 복수형).

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화 (Localizing Resource URIs)

기본적으로 `Route::resource`는 영어 동사를 사용해 리소스 URI를 생성합니다. `create`와 `edit` 액션 동사를 현지화하려면 `Route::resourceVerbs` 메서드를 사용합니다. 보통 애플리케이션 `App\Providers\RouteServiceProvider`의 `boot` 메서드 초반에 설정합니다:

```
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

동사 커스터마이징 후, 예를 들어 `Route::resource('fotos', PhotoController::class)`로 리소스를 등록하면 다음과 같은 URI가 생성됩니다:

```
/fotos/crear

/fotos/{foto}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보완 (Supplementing Resource Controllers)

기본 리소스 라우트 외에 추가 라우트를 컨트롤러에 더하고 싶다면, `Route::resource` 메서드 호출 이전에 추가 라우트를 정의해야 합니다. 그렇지 않으면 `resource` 메서드에서 만든 라우트가 추가 라우트보다 우선시될 수 있습니다:

```
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!TIP]
> 컨트롤러에 너무 많은 역할이 집중되지 않도록 하세요. 기본적인 리소스 액션 외에 계속 별도의 메서드가 필요하다면, 컨트롤러를 두 개 이상의 더 작은 단위로 분리하는 것을 고려해보세요.

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러 (Dependency Injection & Controllers)

<a name="constructor-injection"></a>
#### 생성자 주입 (Constructor Injection)

Laravel의 [서비스 컨테이너](/docs/{{version}}/container)는 모든 컨트롤러를 해결하는 데 사용됩니다. 따라서 컨트롤러 생성자에 필요한 의존성을 타입힌트하면, 선언한 의존성을 자동으로 해결하여 컨트롤러 인스턴스에 주입해줍니다:

```
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * 사용자 저장소 인스턴스.
     */
    protected $users;

    /**
     * 새 컨트롤러 인스턴스를 생성합니다.
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

생성자 주입 외에도, 컨트롤러 메서드의 인수에도 의존성을 타입힌트할 수 있습니다. `Illuminate\Http\Request` 인스턴스를 메서드에 주입하는 경우가 대표적입니다:

```
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

라운트 파라미터 인수도 동시에 기대하는 경우, 라우트 인수는 다른 의존성들 다음에 명시해야 합니다. 예를 들어, 다음과 같이 라우트를 정의했다고 가정하면:

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

`Illuminate\Http\Request` 타입힌트를 유지하면서 `id` 파라미터도 받으려면 다음과 같이 메서드를 정의할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정한 사용자 정보를 업데이트합니다.
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