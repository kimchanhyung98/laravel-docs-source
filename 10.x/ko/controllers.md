# 컨트롤러(Controllers)

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
    - [리소스 라우트 스코핑](#restful-scoping-resource-routes)
    - [리소스 URI 지역화](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 보완](#restful-supplementing-resource-controllers)
    - [싱글톤 리소스 컨트롤러](#singleton-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개

모든 요청 처리 로직을 라우트 파일 내의 클로저로 정의하는 대신, 이 동작을 "컨트롤러" 클래스에 정리하여 사용할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스로 그룹화할 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청(보기, 생성, 수정, 삭제 등)을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성

<a name="basic-controllers"></a>
### 기본 컨트롤러

새로운 컨트롤러를 빠르게 생성하려면 `make:controller` 아티즌 명령어를 실행할 수 있습니다. 기본적으로, 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

```shell
php artisan make:controller UserController
```

기본 컨트롤러의 예시를 살펴보겠습니다. 컨트롤러는 들어오는 HTTP 요청에 응답하는 공개(public) 메서드를 여러 개 가질 수 있습니다.

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

컨트롤러 클래스와 메서드를 작성한 후, 다음과 같이 해당 컨트롤러 메서드에 대한 라우트를 정의할 수 있습니다.

    use App\Http\Controllers\UserController;

    Route::get('/user/{id}', [UserController::class, 'show']);

들어오는 요청이 지정된 라우트 URI와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되며, 라우트 파라미터가 해당 메서드에 전달됩니다.

> [!NOTE]  
> 컨트롤러는 **반드시** 기본 클래스를 상속할 필요는 없습니다. 하지만, `middleware` 및 `authorize`와 같은 편리한 기능을 사용할 수 없습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러

컨트롤러의 동작이 특히 복잡한 경우, 전체 컨트롤러 클래스를 해당 단일 동작에 전념하는 것이 편리할 수 있습니다. 이를 위해 컨트롤러 내에 단일 `__invoke` 메서드를 정의할 수 있습니다.

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

단일 액션 컨트롤러의 라우트를 등록할 때는 메서드를 명시할 필요가 없습니다. 컨트롤러 이름만 라우터에 전달하면 됩니다.

    use App\Http\Controllers\ProvisionServer;

    Route::post('/server', ProvisionServer::class);

`make:controller` 아티즌 명령어의 `--invokable` 옵션을 사용하여 호출 가능한(invokable) 컨트롤러를 생성할 수 있습니다.

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]  
> 컨트롤러 스텁은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

[미들웨어](/docs/{{version}}/middleware)는 라우트 파일에서 컨트롤러의 라우트에 할당할 수 있습니다.

    Route::get('profile', [UserController::class, 'show'])->middleware('auth');

또는, 컨트롤러의 생성자에서 미들웨어를 지정하는 것이 편리할 수 있습니다. 컨트롤러의 생성자 안에서 `middleware` 메서드를 사용하여 컨트롤러의 액션에 미들웨어를 지정할 수 있습니다.

    class UserController extends Controller
    {
        /**
         * 새로운 컨트롤러 인스턴스를 생성합니다.
         */
        public function __construct()
        {
            $this->middleware('auth');
            $this->middleware('log')->only('index');
            $this->middleware('subscribed')->except('store');
        }
    }

컨트롤러는 또한 클로저를 사용하여 미들웨어를 등록할 수 있습니다. 이 방법은 전체 미들웨어 클래스를 정의하지 않고 하나의 컨트롤러에 인라인 미들웨어를 정의하는 데 유용합니다.

    use Closure;
    use Illuminate\Http\Request;

    $this->middleware(function (Request $request, Closure $next) {
        return $next($request);
    });

<a name="resource-controllers"></a>
## 리소스 컨트롤러

애플리케이션의 각 Eloquent 모델을 "리소스"라고 생각한다면, 일반적으로 각 리소스에 대해 동일한 집합의 동작을 수행하게 됩니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다고 가정해 봅시다. 사용자는 아마도 이러한 리소스를 생성, 조회, 수정 또는 삭제할 수 있을 것입니다.

이러한 일반적인 사용 사례 때문에, Laravel 리소스 라우팅은 한 줄의 코드로 전형적인 생성, 조회, 수정, 삭제("CRUD") 라우트를 컨트롤러에 할당할 수 있습니다. 먼저, `make:controller` 아티즌 명령어의 `--resource` 옵션을 사용하여 이러한 동작을 처리하는 컨트롤러를 빠르게 생성할 수 있습니다.

```shell
php artisan make:controller PhotoController --resource
```

이 명령은 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성합니다. 이 컨트롤러에는 리소스 작업마다 메서드가 포함되어 있습니다. 다음으로, 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다.

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class);

이 한 줄의 라우트 선언으로 다양한 리소스 작업을 처리하는 여러 라우트가 생성됩니다. 생성된 컨트롤러에는 이미 각 작업에 대한 메서드 스텁이 포함되어 있습니다. 참고로, `route:list` 아티즌 명령어를 실행하여 애플리케이션의 라우트를 빠르게 확인할 수 있습니다.

배열을 `resources` 메서드에 전달하여 여러 리소스 컨트롤러를 한 번에 등록할 수도 있습니다.

    Route::resources([
        'photos' => PhotoController::class,
        'posts' => PostController::class,
    ]);

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 동작

Verb      | URI                    | 액션       | 라우트 이름
----------|------------------------|------------|---------------------
GET       | `/photos`              | index      | photos.index
GET       | `/photos/create`       | create     | photos.create
POST      | `/photos`              | store      | photos.store
GET       | `/photos/{photo}`      | show       | photos.show
GET       | `/photos/{photo}/edit` | edit       | photos.edit
PUT/PATCH | `/photos/{photo}`      | update     | photos.update
DELETE    | `/photos/{photo}`      | destroy    | photos.destroy

<a name="customizing-missing-model-behavior"></a>
#### 모델 누락 시 동작 커스터마이징

일반적으로, 암시적으로 바인딩된 리소스 모델을 찾을 수 없는 경우 404 HTTP 응답이 생성됩니다. 그러나, 리소스 라우트를 정의할 때 `missing` 메서드를 호출하여 이 동작을 커스터마이즈할 수 있습니다. `missing` 메서드는 암시적으로 바인딩된 모델을 찾을 수 없을 때 호출되는 클로저를 받습니다.

    use App\Http\Controllers\PhotoController;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Redirect;

    Route::resource('photos', PhotoController::class)
            ->missing(function (Request $request) {
                return Redirect::route('photos.index');
            });

<a name="soft-deleted-models"></a>
#### 소프트 삭제(Soft Delete) 모델

일반적으로, 암시적 모델 바인딩은 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)된 모델을 조회하지 않고 404 HTTP 응답을 반환합니다. 그러나, 리소스 라우트를 정의할 때 `withTrashed` 메서드를 호출하여 소프트 삭제된 모델도 허용할 수 있습니다.

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->withTrashed();

인자를 전달하지 않으면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델이 허용됩니다. 배열을 `withTrashed`에 전달하여 이 중 일부만 지정할 수도 있습니다.

    Route::resource('photos', PhotoController::class)->withTrashed(['show']);

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정

[라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 사용하고, 리소스 컨트롤러의 메서드에서 모델 인스턴스를 타입힌트하고 싶다면 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 리퀘스트 클래스 생성

리소스 컨트롤러를 생성할 때 `--requests` 옵션을 제공하면, 아티즌이 컨트롤러의 저장 및 업데이트 메서드를 위한 [폼 리퀘스트 클래스](/docs/{{version}}/validation#form-request-validation)를 생성하도록 할 수 있습니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트를 선언할 때, 컨트롤러가 처리해야 할 작업의 일부만 지정할 수 있습니다.

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->only([
        'index', 'show'
    ]);

    Route::resource('photos', PhotoController::class)->except([
        'create', 'store', 'update', 'destroy'
    ]);

<a name="api-resource-routes"></a>
#### API 리소스 라우트

API에서 사용될 리소스 라우트를 선언할 때는, 보통 HTML 템플릿을 제공하는 `create`, `edit` 라우트를 제외하길 원할 것입니다. 편의를 위해, `apiResource` 메서드를 사용하여 이 두 라우트를 자동으로 제외할 수 있습니다.

    use App\Http\Controllers\PhotoController;

    Route::apiResource('photos', PhotoController::class);

배열을 `apiResources` 메서드에 전달하면 여러 API 리소스 컨트롤러를 한 번에 등록할 수 있습니다.

    use App\Http\Controllers\PhotoController;
    use App\Http\Controllers\PostController;

    Route::apiResources([
        'photos' => PhotoController::class,
        'posts' => PostController::class,
    ]);

`make:controller` 명령에 `--api` 옵션을 사용하여 `create` 및 `edit` 메서드를 포함하지 않는 API 리소스 컨트롤러를 빠르게 생성할 수 있습니다.

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스

때때로 중첩된 리소스에 대한 라우트를 정의해야 할 수도 있습니다. 예를 들어, 포토 리소스에는 여러 개의 댓글이 달릴 수 있습니다. 리소스 컨트롤러를 중첩하려면 라우트 선언에서 "점(.)" 표기법을 사용할 수 있습니다.

    use App\Http\Controllers\PhotoCommentController;

    Route::resource('photos.comments', PhotoCommentController::class);

이 라우트는 아래와 같은 URI로 중첩 리소스에 접근할 수 있게 만듭니다.

    /photos/{photo}/comments/{comment}

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 스코핑

Laravel의 [암시적 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능은 중첩 바인딩 시, 자식 모델이 부모 모델에 실제로 속하는지 자동으로 확인할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 스코핑을 활성화할 수 있으며, 자식 리소스를 어떤 필드로 조회할지도 지정할 수 있습니다. 자세한 정보는 [리소스 라우트 스코핑](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 얕은 중첩(Shallow Nesting)

종종 자식 ID가 이미 유일한 식별자인 경우 URI에 부모와 자식 ID를 모두 포함하는 것이 꼭 필요하지 않을 수 있습니다. URI 세그먼트에서 자동 증가 기본키 등 고유 식별자를 사용할 때는 "얕은 중첩"을 사용할 수 있습니다.

    use App\Http\Controllers\CommentController;

    Route::resource('photos.comments', CommentController::class)->shallow();

이 라우트 정의는 다음과 같은 라우트를 생성합니다.

Verb      | URI                               | 액션       | 라우트 이름
----------|-----------------------------------|------------|---------------------
GET       | `/photos/{photo}/comments`        | index      | photos.comments.index
GET       | `/photos/{photo}/comments/create` | create     | photos.comments.create
POST      | `/photos/{photo}/comments`        | store      | photos.comments.store
GET       | `/comments/{comment}`             | show       | comments.show
GET       | `/comments/{comment}/edit`        | edit       | comments.edit
PUT/PATCH | `/comments/{comment}`             | update     | comments.update
DELETE    | `/comments/{comment}`             | destroy    | comments.destroy

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정

기본적으로 모든 리소스 컨트롤러 동작에는 라우트 이름이 있지만, `names` 배열을 전달하여 원하는 라우트 이름으로 덮어쓸 수 있습니다.

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->names([
        'create' => 'photos.build'
    ]);

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정

기본적으로 `Route::resource`는 리소스 이름의 "단수형"을 기준으로 라우트 파라미터를 생성합니다. `parameters` 메서드를 사용하여 리소스별로 쉽게 재정의할 수 있습니다. `parameters`에 전달하는 배열은 리소스 이름과 파라미터 이름의 연관 배열이어야 합니다.

    use App\Http\Controllers\AdminUserController;

    Route::resource('users', AdminUserController::class)->parameters([
        'users' => 'admin_user'
    ]);

위 예시는 리소스의 `show` 라우트에 대해 다음과 같은 URI를 생성합니다.

    /users/{admin_user}

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코핑

Laravel의 [스코프 암시적 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능을 사용하면 중첩 바인딩 시 자식 모델이 부모 모델에 실제로 속하는지 자동으로 확인할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 스코핑을 활성화할 수 있으며, 자식 리소스를 어떤 필드로 조회할지도 Laravel에 지시할 수 있습니다.

    use App\Http\Controllers\PhotoCommentController;

    Route::resource('photos.comments', PhotoCommentController::class)->scoped([
        'comment' => 'slug',
    ]);

이 라우트는 아래와 같은 URI로 접근할 수 있는 스코프된 중첩 리소스를 등록합니다.

    /photos/{photo}/comments/{comment:slug}

중첩 라우트 파라미터에 커스텀 키 암시적 바인딩을 사용하는 경우, Laravel은 규칙에 따라 쿼리를 스코핑 하여 자식 모델을 부모를 통해 조회합니다. 이 경우, `Photo` 모델에 `comments`(라우트 파라미터 이름의 복수형) 관계가 있다고 간주하여 `Comment` 모델을 조회합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 지역화

기본적으로 `Route::resource`는 영어 동사와 복수 규칙을 사용하여 리소스 URI를 생성합니다. `create`, `edit` 동사 등을 지역화가 필요할 경우 `Route::resourceVerbs` 메서드를 사용할 수 있습니다. 이는 애플리케이션의 `App\Providers\RouteServiceProvider`의 `boot` 메서드 초기에 설정할 수 있습니다.

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

Laravel의 플루랄라이저는 [여러 언어를 지원하며 필요에 따라 설정](docs/{{version}}/localization#pluralization-language)할 수 있습니다. 동사와 복수화 언어 커스터마이즈 후, `Route::resource('publicacion', PublicacionController::class)`와 같이 리소스 라우트를 등록하면 아래와 같은 URI가 생성됩니다.

    /publicacion/crear

    /publicacion/{publicaciones}/editar

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보완

기본 리소스 라우트 집합 외에 추가 라우트를 리소스 컨트롤러에 추가해야 하는 경우, 반드시 `Route::resource` 호출 전에 이 라우트를 정의해야 합니다. 그렇지 않으면 `resource` 메서드가 정의한 라우트가 추가 라우트보다 우선하여 의도치 않은 결과가 생길 수 있습니다.

    use App\Http\Controller\PhotoController;

    Route::get('/photos/popular', [PhotoController::class, 'popular']);
    Route::resource('photos', PhotoController::class);

> [!NOTE]  
> 컨트롤러의 역할을 명확하게 유지하는 것이 중요합니다. 일반 리소스 액션 외의 메서드가 자주 필요하다면, 컨트롤러를 둘 혹은 더 작은 컨트롤러로 나누는 것을 고려하세요.

<a name="singleton-resource-controllers"></a>
### 싱글톤 리소스 컨트롤러

애플리케이션에는 단 하나의 인스턴스만 존재할 수 있는 리소스가 있을 수 있습니다. 예를 들어, 사용자의 "프로필"은 수정 또는 업데이트할 수 있지만, 하나의 사용자에게 둘 이상의 "프로필"이 있어서는 안 됩니다. 마찬가지로, 이미지에는 단 하나의 "썸네일"만 있을 수 있습니다. 이러한 리소스를 "싱글톤 리소스"라고 하며, 해당 리소스는 하나의 인스턴스만 존재할 수 있습니다. 이런 경우에는 "싱글톤" 리소스 컨트롤러를 등록할 수 있습니다.

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위의 싱글톤 리소스 정의는 다음과 같은 라우트를 등록합니다. 보다시피 싱글톤 리소스는 "생성" 라우트가 등록되지 않으며, 오직 한 인스턴스만 존재할 수 있기 때문에 식별자를 사용하지 않습니다.

Verb      | URI                               | 액션       | 라우트 이름
----------|-----------------------------------|------------|---------------------
GET       | `/profile`                        | show       | profile.show
GET       | `/profile/edit`                   | edit       | profile.edit
PUT/PATCH | `/profile`                        | update     | profile.update

싱글톤 리소스는 표준 리소스 내부에 중첩할 수도 있습니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 예시에서, `photos` 리소스는 [표준 리소스 라우트](#actions-handled-by-resource-controller)를 모두 가지지만, `thumbnail` 리소스는 아래와 같은 싱글톤 리소스 라우트를 갖게 됩니다.

| Verb      | URI                              | 액션     | 라우트 이름               |
|-----------|----------------------------------|----------|--------------------------|
| GET       | `/photos/{photo}/thumbnail`      | show     | photos.thumbnail.show    |
| GET       | `/photos/{photo}/thumbnail/edit` | edit     | photos.thumbnail.edit    |
| PUT/PATCH | `/photos/{photo}/thumbnail`      | update   | photos.thumbnail.update  |

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글톤 리소스

경우에 따라 싱글톤 리소스에 대해 생성 및 저장 라우트를 정의하고 싶을 수 있습니다. 이럴 때는 싱글톤 라우트를 등록할 때 `creatable` 메서드를 호출하세요.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이 경우, 아래와 같은 라우트가 등록됩니다. 또한, 생성 가능한 싱글톤 리소스에는 `DELETE` 라우트도 등록됩니다.

| Verb      | URI                                | 액션     | 라우트 이름               |
|-----------|------------------------------------|----------|--------------------------|
| GET       | `/photos/{photo}/thumbnail/create` | create   | photos.thumbnail.create  |
| POST      | `/photos/{photo}/thumbnail`        | store    | photos.thumbnail.store   |
| GET       | `/photos/{photo}/thumbnail`        | show     | photos.thumbnail.show    |
| GET       | `/photos/{photo}/thumbnail/edit`   | edit     | photos.thumbnail.edit    |
| PUT/PATCH | `/photos/{photo}/thumbnail`        | update   | photos.thumbnail.update  |
| DELETE    | `/photos/{photo}/thumbnail`        | destroy  | photos.thumbnail.destroy |

싱글톤 리소스에 대해 `DELETE` 라우트만 등록하고, 생성 또는 저장 라우트는 등록하지 않으려면, `destroyable` 메서드를 사용할 수 있습니다.

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글톤 리소스

`apiSingleton` 메서드는 API를 통해 관리되는 싱글톤 리소스를 등록하는 데 사용할 수 있습니다. 이 경우 `create`, `edit` 라우트는 생성되지 않습니다.

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론, API 싱글톤 리소스도 `creatable`일 수 있으며, 이 경우 `store` 및 `destroy` 라우트가 등록됩니다.

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러

<a name="constructor-injection"></a>
#### 생성자 주입

Laravel의 [서비스 컨테이너](/docs/{{version}}/container)는 모든 Laravel 컨트롤러를 해석(resolve)할 때 사용됩니다. 따라서 컨트롤러에서 필요로 하는 의존성을 생성자에서 타입힌트하면 됩니다. 선언된 의존성은 자동으로 컨트롤러 인스턴스에 주입됩니다.

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

<a name="method-injection"></a>
#### 메서드 주입

생성자 주입 외에도, 컨트롤러의 메서드에서 의존성을 타입힌트할 수 있습니다. 흔한 예로, `Illuminate\Http\Request` 인스턴스를 주입받아 컨트롤러 메서드에서 사용하는 경우가 있습니다.

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

            // 사용자 저장...

            return redirect('/users');
        }
    }

컨트롤러 메서드에서 라우트 파라미터도 함께 받고 싶은 경우, 의존성 인자 뒤에 라우트 인자(argument)를 나열하면 됩니다. 예를 들어, 라우트를 다음과 같이 정의했다면,

    use App\Http\Controllers\UserController;

    Route::put('/user/{id}', [UserController::class, 'update']);

컨트롤러 메서드는 다음과 같이 정의할 수 있습니다. 이때 `Illuminate\Http\Request`를 타입힌트하고, `id` 파라미터를 바로 사용할 수 있습니다.

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
            // 사용자 업데이트...

            return redirect('/users');
        }
    }
