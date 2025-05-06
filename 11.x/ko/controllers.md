# 컨트롤러(Controllers)

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
    - [싱글턴 리소스 컨트롤러](#singleton-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개

모든 요청 처리 로직을 라우트 파일의 클로저로 정의하는 대신 "컨트롤러" 클래스를 사용하여 이러한 동작을 체계적으로 구성할 수 있습니다. 컨트롤러를 사용하면 관련 있는 요청 처리 로직을 하나의 클래스로 그룹화할 수 있습니다. 예를 들어, `UserController` 클래스는 사용자의 표시, 생성, 수정, 삭제와 관련된 모든 요청을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기

<a name="basic-controllers"></a>
### 기본 컨트롤러

새 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 실행하면 됩니다. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다:

```shell
php artisan make:controller UserController
```

다음은 기본 컨트롤러의 예시입니다. 컨트롤러는 어떤 공개 메서드라도 가질 수 있으며, 이들은 들어오는 HTTP 요청에 응답합니다:

    <?php

    namespace App\Http\Controllers;

    use App\Models\User;
    use Illuminate\View\View;

    class UserController extends Controller
    {
        /**
         * 주어진 사용자의 프로필 표시.
         */
        public function show(string $id): View
        {
            return view('user.profile', [
                'user' => User::findOrFail($id)
            ]);
        }
    }

컨트롤러 클래스와 메서드를 작성했다면 다음과 같이 해당 컨트롤러 메서드로 라우트를 정의할 수 있습니다:

    use App\Http\Controllers\UserController;

    Route::get('/user/{id}', [UserController::class, 'show']);

요청이 지정된 라우트 URI와 일치하면 `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되며, 라우트 파라미터들이 메서드로 전달됩니다.

> [!NOTE]  
> 컨트롤러가 **반드시** 베이스 클래스를 상속할 필요는 없습니다. 하지만 모든 컨트롤러에서 공유해야 할 메서드가 있다면 베이스 컨트롤러 클래스를 상속하는 것이 편리할 수 있습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러

특정 컨트롤러 액션이 복잡하다면, 하나의 컨트롤러 클래스를 해당 액션 전용으로 사용하는 것이 편리할 수 있습니다. 이를 위해 컨트롤러 내부에 단일 `__invoke` 메서드를 정의할 수 있습니다:

    <?php

    namespace App\Http\Controllers;

    class ProvisionServer extends Controller
    {
        /**
         * 새로운 웹 서버 프로비저닝.
         */
        public function __invoke()
        {
            // ...
        }
    }

단일 액션 컨트롤러의 라우트를 등록할 때는 컨트롤러 메서드를 지정할 필요가 없습니다. 컨트롤러 이름만 라우터에 전달하면 됩니다:

    use App\Http\Controllers\ProvisionServer;

    Route::post('/server', ProvisionServer::class);

`make:controller` Artisan 명령어의 `--invokable` 옵션을 사용하면 인보커블 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]  
> 컨트롤러 스텁은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

[미들웨어](/docs/{{version}}/middleware)는 컨트롤러의 라우트에 라우트 파일에서 직접 할당할 수 있습니다:

    Route::get('/profile', [UserController::class, 'show'])->middleware('auth');

또는, 컨트롤러 클래스 내에서 미들웨어를 지정하는 것이 더 편리할 수 있습니다. 이를 위해, 컨트롤러는 `HasMiddleware` 인터페이스를 구현해야 하며, 이 인터페이스는 컨트롤러에 정적 `middleware` 메서드가 있어야 함을 명시합니다. 이 메서드에서 컨트롤러의 액션에 적용할 미들웨어 배열을 반환할 수 있습니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Routing\Controllers\HasMiddleware;
    use Illuminate\Routing\Controllers\Middleware;

    class UserController extends Controller implements HasMiddleware
    {
        /**
         * 컨트롤러에 할당할 미들웨어 반환.
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

미들웨어를 클로저로 정의할 수도 있는데, 이는 별도의 미들웨어 클래스를 작성하지 않고 인라인 미들웨어를 정의하는 편리한 방법입니다:

    use Closure;
    use Illuminate\Http\Request;

    /**
     * 컨트롤러에 할당할 미들웨어 반환.
     */
    public static function middleware(): array
    {
        return [
            function (Request $request, Closure $next) {
                return $next($request);
            },
        ];
    }

> [!WARNING]  
> `Illuminate\Routing\Controllers\HasMiddleware`를 구현하는 컨트롤러는 `Illuminate\Routing\Controller`를 확장해서는 안 됩니다.

<a name="resource-controllers"></a>
## 리소스 컨트롤러

애플리케이션의 각 Eloquent 모델이 "리소스"라고 생각하면, 일반적으로 각 리소스에 대해 동일한 작업 집합(생성, 읽기, 수정, 삭제 등)을 수행하게 됩니다. 예를 들어, `Photo` 모델과 `Movie` 모델이 있다면, 사용자는 이 리소스를 생성, 조회, 수정, 삭제할 가능성이 높습니다.

이러한 일반적인 사용 사례를 위해, Laravel의 리소스 라우팅은 한 줄의 코드로 "CRUD" 라우트를 특정 컨트롤러에 할당할 수 있습니다. 먼저, `make:controller` Artisan 명령어의 `--resource` 옵션을 사용하여 이런 작업을 처리할 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

이 명령은 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성합니다. 이 컨트롤러에는 모든 리소스 작업에 해당하는 메서드가 포함되어 있습니다. 그런 다음, 컨트롤러를 가리키는 리소스 라우트를 등록하면 됩니다:

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class);

이 라우트 선언 한 줄로 여러 가지 액션을 처리할 수 있는 다양한 라우트가 생성됩니다. 생성된 컨트롤러에는 이미 각 액션별로 스텁 메서드가 들어 있습니다. 여기서 `route:list` Artisan 명령어를 실행하면 애플리케이션의 라우트를 빠르게 확인할 수 있습니다.

배열을 `resources` 메서드에 전달하여 여러 리소스 컨트롤러를 한 번에 등록할 수도 있습니다:

    Route::resources([
        'photos' => PhotoController::class,
        'posts' => PostController::class,
    ]);

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러에서 처리하는 액션

<div class="overflow-auto">

| HTTP 메서드 | URI                           | 액션    | 라우트 이름      |
| ----------- | ---------------------------- | ------- | ---------------  |
| GET         | `/photos`                    | index   | photos.index     |
| GET         | `/photos/create`             | create  | photos.create    |
| POST        | `/photos`                    | store   | photos.store     |
| GET         | `/photos/{photo}`            | show    | photos.show      |
| GET         | `/photos/{photo}/edit`       | edit    | photos.edit      |
| PUT/PATCH   | `/photos/{photo}`            | update  | photos.update    |
| DELETE      | `/photos/{photo}`            | destroy | photos.destroy   |

</div>

<a name="customizing-missing-model-behavior"></a>
#### 존재하지 않는 모델 처리 방식 커스터마이징

일반적으로, 암시적 바인딩된 리소스 모델을 찾지 못하면 404 HTTP 응답이 생성됩니다. 그러나, `missing` 메서드를 사용해 이 동작을 커스터마이즈할 수 있습니다. `missing` 메서드에는 클로저를 전달할 수 있으며, 모델이 존재하지 않을 때 이 클로저가 호출됩니다:

    use App\Http\Controllers\PhotoController;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Redirect;

    Route::resource('photos', PhotoController::class)
        ->missing(function (Request $request) {
            return Redirect::route('photos.index');
        });

<a name="soft-deleted-models"></a>
#### 소프트 삭제(Soft Delete) 모델

일반적으로, 암시적 모델 바인딩은 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)된 모델을 조회하지 않으며, 404 HTTP 응답을 반환합니다. 그러나, 리소스 라우트를 정의할 때 `withTrashed` 메서드를 호출하면 소프트 삭제된 모델도 사용할 수 있습니다:

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->withTrashed();

`withTrashed`에 인수를 전달하지 않으면 `show`, `edit`, `update` 라우트에서 소프트 삭제된 모델이 허용됩니다. 특정 라우트만 지정하려면 배열로 전달할 수 있습니다:

    Route::resource('photos', PhotoController::class)->withTrashed(['show']);

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정하기

[라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 사용하고 있으며 각 컨트롤러 메서드에서 모델 인스턴스를 타입힌트하고 싶다면, 컨트롤러를 생성할 때 `--model` 옵션을 사용하세요:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 리퀘스트 생성하기

`--requests` 옵션을 사용하면 컨트롤러의 저장 및 수정 메서드를 위한 [폼 리퀘스트 클래스](/docs/{{version}}/validation#form-request-validation)도 Artisan이 자동으로 생성합니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트를 선언할 때 컨트롤러가 처리할 액션 중 일부만 지정할 수 있습니다:

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->only([
        'index', 'show'
    ]);

    Route::resource('photos', PhotoController::class)->except([
        'create', 'store', 'update', 'destroy'
    ]);

<a name="api-resource-routes"></a>
#### API 리소스 라우트

API에서 사용될 리소스 라우트를 선언할 때는 `create` 및 `edit` 등 HTML 템플릿을 반환하는 라우트를 제외하는 경우가 많습니다. 이를 위해, `apiResource` 메서드를 사용하면 이 두 라우트가 자동으로 제외됩니다:

    use App\Http\Controllers\PhotoController;

    Route::apiResource('photos', PhotoController::class);

배열을 `apiResources` 메서드에 전달하여 여러 API 리소스 컨트롤러를 한 번에 등록할 수도 있습니다:

    use App\Http\Controllers\PhotoController;
    use App\Http\Controllers\PostController;

    Route::apiResources([
        'photos' => PhotoController::class,
        'posts' => PostController::class,
    ]);

`make:controller` 명령어 실행 시 `--api` 스위치를 사용하면 `create` 및 `edit` 메서드가 없는 API 리소스 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스

가끔 한 리소스 안에 또 다른 리소스가 존재하는 관계의 라우트를 정의해야 할 필요가 있습니다. 예를 들어, 사진 리소스에는 해당 사진에 연결된 여러 개의 댓글이 있을 수 있습니다. 이런 중첩 리소스 컨트롤러를 만들기 위해서는 라우트 선언에 "도트" 표기법을 사용할 수 있습니다:

    use App\Http\Controllers\PhotoCommentController;

    Route::resource('photos.comments', PhotoCommentController::class);

이 라우트는 다음과 같은 URI로 중첩 리소스 접근이 가능하게 합니다:

    /photos/{photo}/comments/{comment}

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 스코핑

Laravel의 [암시적 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능은 자동으로 중첩 바인딩에서 자식 모델이 부모 모델에 속하는지 확인해주는 기능을 제공합니다. 중첩 리소스 정의 시 `scoped` 메서드를 사용하면, 자동 스코핑을 활성화하고 자식 리소스를 조회할 필드를 지정할 수 있습니다. 자세한 방법은 [리소스 라우트 스코핑](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 네스팅의 얕게 사용(Shallow Nesting)

자식 ID가 고유 식별자인 경우, URI 내에 부모와 자식 ID 모두가 반드시 필요하지 않을 수 있습니다. 자동 증가 기본키처럼 고유 식별자를 사용할 때에는 "shallow nesting(얕은 네스팅)"을 선택할 수 있습니다:

    use App\Http\Controllers\CommentController;

    Route::resource('photos.comments', CommentController::class)->shallow();

이렇게 정의하면 다음과 같은 라우트가 생성됩니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                                   | 액션    | 라우트 이름            |
| ----------- | ------------------------------------- | ------- | ---------------------- |
| GET         | `/photos/{photo}/comments`            | index   | photos.comments.index  |
| GET         | `/photos/{photo}/comments/create`     | create  | photos.comments.create |
| POST        | `/photos/{photo}/comments`            | store   | photos.comments.store  |
| GET         | `/comments/{comment}`                 | show    | comments.show          |
| GET         | `/comments/{comment}/edit`            | edit    | comments.edit          |
| PUT/PATCH   | `/comments/{comment}`                 | update  | comments.update        |
| DELETE      | `/comments/{comment}`                 | destroy | comments.destroy       |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정

기본적으로, 모든 리소스 컨트롤러 액션은 라우트 이름이 부여됩니다. 하지만 `names` 배열로 원하는 라우트 이름을 오버라이드할 수 있습니다:

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->names([
        'create' => 'photos.build'
    ]);

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정

기본적으로 `Route::resource`는 리소스 이름의 "단수형"을 사용해 라우트 파라미터를 생성합니다. `parameters` 메서드를 사용하면 리소스 별로 파라미터 이름을 쉽게 오버라이드할 수 있습니다. 전달하는 배열은 리소스 이름과 파라미터 이름의 연관 배열이어야 합니다:

    use App\Http\Controllers\AdminUserController;

    Route::resource('users', AdminUserController::class)->parameters([
        'users' => 'admin_user'
    ]);

위 예제는 `show` 라우트에 대해 다음과 같은 URI를 생성합니다:

    /users/{admin_user}

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코핑

Laravel의 [스코프드 암시적 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능은 중첩 바인딩에서 자식 모델이 부모 모델에 속하는지 자동으로 확인합니다. 중첩 리소스 정의 시 `scoped` 메서드를 사용하면 자동 스코핑과 자식 리소스를 조회할 필드를 지정할 수 있습니다:

    use App\Http\Controllers\PhotoCommentController;

    Route::resource('photos.comments', PhotoCommentController::class)->scoped([
        'comment' => 'slug',
    ]);

이렇게 하면 다음과 같은 URI로 스코프드 중첩 리소스에 접근할 수 있습니다:

    /photos/{photo}/comments/{comment:slug}

중첩 라우트 파라미터에 커스텀 키드 암시적 바인딩을 사용할 경우, Laravel은 규칙에 따라 부모를 통해 자식 모델을 조회하도록 쿼리를 자동으로 스코프합니다. 이때 `Photo` 모델에 `comments`라는(파라미터 이름의 복수형) 관계가 있다고 가정하여 `Comment` 모델을 조회합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화

기본적으로 `Route::resource`는 영문 동사 및 복수 규칙을 사용해 리소스 URI를 생성합니다. `create` 및 `edit` 동사를 현지화해야 할 경우, `Route::resourceVerbs` 메서드를 사용할 수 있습니다. 이는 애플리케이션의 `App\Providers\AppServiceProvider` 내 `boot` 메서드에서 설정 가능합니다:

    /**
     * 어플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Route::resourceVerbs([
            'create' => 'crear',
            'edit' => 'editar',
        ]);
    }

Laravel의 플러랄라이저는 [다양한 언어](/docs/{{version}}/localization#pluralization-language)를 지원하므로, 필요에 따라 언어를 설정할 수 있습니다. 동사와 복수화 언어를 커스터마이즈하면 `Route::resource('publicacion', PublicacionController::class)`로 등록할 때 다음과 같은 URI가 생성됩니다:

    /publicacion/crear

    /publicacion/{publicaciones}/editar

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보완

기본 리소스 라우트 외에 추가 라우트를 등록해야 한다면, 반드시 `Route::resource` 메서드 호출 **이전**에 해당 라우트를 정의하세요. 그렇지 않으면 `resource` 메서드가 등록한 라우트가 보조 라우트보다 우선시될 수 있습니다:

    use App\Http\Controller\PhotoController;

    Route::get('/photos/popular', [PhotoController::class, 'popular']);
    Route::resource('photos', PhotoController::class);

> [!NOTE]  
> 컨트롤러의 관심사를 집중하세요. 리소스 액션 외의 메서드가 자주 필요하다면, 컨트롤러를 두 개의 작고 명확한 역할로 분리하는 것이 좋습니다.

<a name="singleton-resource-controllers"></a>
### 싱글턴 리소스 컨트롤러

애플리케이션 내에서 한 개의 인스턴스만 존재하는 리소스가 있을 수 있습니다. 예를 들어, 사용자의 "프로필"은 한 번만 수정/조회가 가능하며 두 개 이상 가질 수 없습니다. 마찬가지로 이미지는 하나의 "썸네일"만 가질 수 있습니다. 이러한 리소스를 "싱글턴 리소스"라고 하며, 단일 인스턴스만 존재합니다. 이 경우 "싱글턴" 리소스 컨트롤러를 등록할 수 있습니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위 싱글턴 리소스 정의는 다음과 같은 라우트를 등록합니다. "생성" 라우트는 등록되지 않으며, 오직 하나의 인스턴스만 존재하므로 식별자도 필요하지 않습니다:

<div class="overflow-auto">

| HTTP 메서드 | URI             | 액션  | 라우트 이름       |
| ----------- | --------------- | ----- | ----------------- |
| GET         | `/profile`      | show  | profile.show      |
| GET         | `/profile/edit` | edit  | profile.edit      |
| PUT/PATCH   | `/profile`      | update| profile.update    |

</div>

싱글턴 리소스는 표준 리소스 내부에 중첩시킬 수도 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 예시에서 `photos` 리소스는 [표준 리소스 라우트](#actions-handled-by-resource-controllers)를 모두 갖지만, `thumbnail` 리소스는 아래와 같이 싱글턴 라우트만 갖게 됩니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                              | 액션  | 라우트 이름                |
| ----------- | -------------------------------- | ----- | -------------------------- |
| GET         | `/photos/{photo}/thumbnail`      | show  | photos.thumbnail.show      |
| GET         | `/photos/{photo}/thumbnail/edit` | edit  | photos.thumbnail.edit      |
| PUT/PATCH   | `/photos/{photo}/thumbnail`      | update| photos.thumbnail.update    |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글턴 리소스

가끔 싱글턴 리소스에 대해 생성 및 저장 라우트를 정의해야 할 수 있습니다. 이럴 때, 싱글턴 리소스 라우트 등록 시 `creatable` 메서드를 호출하세요:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이 예시에서는 다음과 같은 라우트가 등록됩니다. 생성 가능한 싱글턴 리소스에는 `DELETE` 라우트도 등록됩니다:

<div class="overflow-auto">

| HTTP 메서드 | URI                                | 액션    | 라우트 이름                |
| ----------- | ---------------------------------- | ------- | -------------------------- |
| GET         | `/photos/{photo}/thumbnail/create` | create  | photos.thumbnail.create    |
| POST        | `/photos/{photo}/thumbnail`        | store   | photos.thumbnail.store     |
| GET         | `/photos/{photo}/thumbnail`        | show    | photos.thumbnail.show      |
| GET         | `/photos/{photo}/thumbnail/edit`   | edit    | photos.thumbnail.edit      |
| PUT/PATCH   | `/photos/{photo}/thumbnail`        | update  | photos.thumbnail.update    |
| DELETE      | `/photos/{photo}/thumbnail`        | destroy | photos.thumbnail.destroy   |

</div>

싱글턴 리소스에 대해 `DELETE` 라우트만 등록하고 생성 및 저장 라우트는 등록하지 않으려면 `destroyable` 메서드를 사용하세요:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글턴 리소스

`apiSingleton` 메서드는 API를 통해 관리되는 싱글턴 리소스를 등록할 때 사용할 수 있으며, 이 경우 `create`, `edit` 라우트가 필요 없습니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론, API 싱글턴 리소스도 `creatable`일 수 있으며, 이 경우 `store`와 `destroy` 라우트가 등록됩니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러

<a name="constructor-injection"></a>
#### 생성자(컨스트럭터) 주입

Laravel [서비스 컨테이너](/docs/{{version}}/container)는 모든 컨트롤러를 해석(인스턴스 생성)할 때 사용됩니다. 따라서 컨트롤러 생성자에서 필요한 의존성을 타입힌트하면, 선언한 의존성을 서비스 컨테이너가 자동으로 주입해줍니다:

    <?php

    namespace App\Http\Controllers;

    use App\Repositories\UserRepository;

    class UserController extends Controller
    {
        /**
         * 컨트롤러 인스턴스 생성자.
         */
        public function __construct(
            protected UserRepository $users,
        ) {}
    }

<a name="method-injection"></a>
#### 메서드 주입

생성자 주입 외에도, 컨트롤러의 메서드에 의존성을 타입힌트할 수 있습니다. 보통 `Illuminate\Http\Request` 인스턴스를 주입받아 사용하는 경우가 많습니다:

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\RedirectResponse;
    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * 새 사용자 저장.
         */
        public function store(Request $request): RedirectResponse
        {
            $name = $request->name;

            // 사용자 저장...

            return redirect('/users');
        }
    }

컨트롤러 메서드가 라우트 파라미터로 입력값도 받을 경우, 의존성 인자 뒤에 라우트 인자를 나열하세요. 예를 들어, 라우트가 다음과 같이 정의된 경우:

    use App\Http\Controllers\UserController;

    Route::put('/user/{id}', [UserController::class, 'update']);

컨트롤러 메서드에서 `Illuminate\Http\Request`를 타입힌트하고, `id` 파라미터를 다음과 같이 정의하면 됩니다:

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\RedirectResponse;
    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * 주어진 사용자 업데이트.
         */
        public function update(Request $request, string $id): RedirectResponse
        {
            // 사용자 업데이트...

            return redirect('/users');
        }
    }
