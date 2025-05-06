# 컨트롤러(Controllers)

- [소개](#introduction)
- [컨트롤러 작성하기](#writing-controllers)
    - [기본 컨트롤러](#basic-controllers)
    - [단일 액션 컨트롤러](#single-action-controllers)
- [컨트롤러 미들웨어](#controller-middleware)
- [리소스 컨트롤러](#resource-controllers)
    - [부분 리소스 라우트](#restful-partial-resource-routes)
    - [중첩 리소스](#restful-nested-resources)
    - [리소스 라우트 네이밍](#restful-naming-resource-routes)
    - [리소스 라우트 파라미터 네이밍](#restful-naming-resource-route-parameters)
    - [리소스 라우트 스코프 지정](#restful-scoping-resource-routes)
    - [리소스 URI 로컬라이징](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 보충](#restful-supplementing-resource-controllers)
    - [싱글톤 리소스 컨트롤러](#singleton-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개

모든 요청 처리 로직을 라우트 파일의 클로저로 정의하는 대신, 이를 "컨트롤러" 클래스 내부로 구성할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스로 묶을 수 있습니다. 예를 들어, `UserController` 클래스는 유저와 관련된 모든 요청(조회, 생성, 수정, 삭제 등)을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기

<a name="basic-controllers"></a>
### 기본 컨트롤러

기본 컨트롤러 예제를 살펴보겠습니다. 이 컨트롤러는 Laravel에 포함된 기본 컨트롤러 클래스인 `App\Http\Controllers\Controller`를 확장합니다:

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

아래와 같이 이 컨트롤러 메서드로 라우트를 지정할 수 있습니다.

    use App\Http\Controllers\UserController;

    Route::get('/user/{id}', [UserController::class, 'show']);

요청이 지정한 라우트 URI와 일치하면 `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고, 라우트 파라미터가 해당 메서드로 전달됩니다.

> **참고**  
> 컨트롤러가 **반드시** 기본 클래스를 확장할 필요는 없습니다. 그러나 이 경우에는 `middleware`, `authorize`와 같은 편의 메서드에 접근하지 못합니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러

특정 컨트롤러 액션이 특히 복잡한 경우, 해당 액션만을 담당하는 별도의 컨트롤러 클래스를 만들 수도 있습니다. 이를 위해 컨트롤러 내부에 단일 `__invoke` 메서드를 정의할 수 있습니다:

    <?php

    namespace App\Http\Controllers;
    
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

단일 액션 컨트롤러의 라우트를 등록할 때는 컨트롤러 메서드를 지정할 필요 없이 컨트롤러 클래스 이름만 라우터에 전달하면 됩니다:

    use App\Http\Controllers\ProvisionServer;

    Route::post('/server', ProvisionServer::class);

`make:controller` 아티즌 명령의 `--invokable` 옵션을 사용하여 호출 가능한(Invokable) 컨트롤러를 생성할 수 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```

> **참고**  
> 컨트롤러 스텁 파일은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

[미들웨어](/docs/{{version}}/middleware)는 라우트 파일에서 컨트롤러의 라우트에 할당할 수 있습니다:

    Route::get('profile', [UserController::class, 'show'])->middleware('auth');

또는 컨트롤러의 생성자에서 미들웨어를 지정할 수도 있습니다. 생성자 내부에서 `middleware` 메서드를 사용하여 컨트롤러 액션에 미들웨어를 할당할 수 있습니다:

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

컨트롤러에서는 클로저를 미들웨어로 등록하는 것도 가능합니다. 이는 전체 미들웨어 클래스를 따로 정의하지 않고 하나의 컨트롤러에서만 사용할 인라인 미들웨어를 정의할 때 편리합니다:

    $this->middleware(function ($request, $next) {
        return $next($request);
    });

<a name="resource-controllers"></a>
## 리소스 컨트롤러

애플리케이션의 각 Eloquent 모델을 "리소스"로 생각하면, 대개 각 리소스에 대해 동일한 작업(생성, 조회, 수정, 삭제)을 하게 됩니다. 예를 들어 `Photo`와 `Movie` 모델이 있다면 사용자들은 이 리소스들을 생성, 조회, 수정, 삭제할 수 있게 됩니다.

이러한 공통 패턴을 위해, Laravel 리소스 라우팅은 일반적인 CRUD(생성, 조회, 수정, 삭제) 라우트를 한 번에 컨트롤러에 할당할 수 있습니다. `make:controller` 아티즌 명령의 `--resource` 옵션을 사용해 리소스 액션을 처리할 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

이 명령은 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성하며, 각 리소스 작업별로 메서드가 포함됩니다. 다음으로, 아래와 같이 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다:

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class);

이 한 줄의 라우트 선언으로 다양한 리소스 작업에 대응하는 여러 라우트가 생성됩니다. 생성된 컨트롤러에는 각 작업에 대한 스텁 메서드도 이미 정의되어 있습니다. 라우트 리스트는 `route:list` 아티즌 명령으로 빠르게 확인할 수 있습니다.

또한, 배열을 `resources` 메서드에 전달하여 여러 리소스 컨트롤러를 한 번에 등록할 수도 있습니다:

    Route::resources([
        'photos' => PhotoController::class,
        'posts' => PostController::class,
    ]);

<a name="actions-handled-by-resource-controller"></a>
#### 리소스 컨트롤러가 처리하는 액션

| 메서드    | URI                        | 액션        | 라우트 이름
|-----------|----------------------------|-------------|---------------------
| GET       | `/photos`                  | index       | photos.index
| GET       | `/photos/create`           | create      | photos.create
| POST      | `/photos`                  | store       | photos.store
| GET       | `/photos/{photo}`          | show        | photos.show
| GET       | `/photos/{photo}/edit`     | edit        | photos.edit
| PUT/PATCH | `/photos/{photo}`          | update      | photos.update
| DELETE    | `/photos/{photo}`          | destroy     | photos.destroy

<a name="customizing-missing-model-behavior"></a>
#### 누락된 모델 동작 커스터마이즈

일반적으로, 암시적으로 바인딩된 리소스 모델을 찾을 수 없는 경우 404 HTTP 응답이 반환됩니다. 그러나 `missing` 메서드를 사용하여 해당 동작을 커스터마이즈할 수 있는데, 이 메서드는 어떤 리소스의 라우트에서도 모델을 찾지 못했을 때 호출되는 클로저를 받습니다:

    use App\Http\Controllers\PhotoController;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Redirect;

    Route::resource('photos', PhotoController::class)
            ->missing(function (Request $request) {
                return Redirect::route('photos.index');
            });

<a name="soft-deleted-models"></a>
#### 소프트 삭제된 모델

기본적으로, 암시적 모델 바인딩은 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)된 모델을 찾아주지 않고 404 HTTP 응답을 반환합니다. 하지만, `withTrashed` 메서드를 사용해 소프트 삭제된 모델도 조회하도록 지정할 수 있습니다:

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->withTrashed();

별도의 인자를 넘기지 않고 `withTrashed`를 호출하면, `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델도 허용됩니다. 특정 라우트만 지정하고 싶다면 배열로 전달할 수 있습니다:

    Route::resource('photos', PhotoController::class)->withTrashed(['show']);

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정

[라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 사용하고 있고, 리소스 컨트롤러의 메서드 시그니처에 모델 인스턴스를 사용할 계획이라면, 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 요청 클래스 생성

`--requests` 옵션을 사용해 리소스 컨트롤러를 생성하면, 컨트롤러의 저장 및 업데이트 액션에서 사용할 [폼 요청 클래스](/docs/{{version}}/validation#form-request-validation)를 아티즌이 자동으로 생성합니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트 선언 시, 컨트롤러가 처리할 액션의 일부만 지정할 수도 있습니다:

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->only([
        'index', 'show'
    ]);

    Route::resource('photos', PhotoController::class)->except([
        'create', 'store', 'update', 'destroy'
    ]);

<a name="api-resource-routes"></a>
#### API 리소스 라우트

API에서 사용될 리소스 라우트의 경우, 보통 `create`, `edit` 등 HTML 템플릿을 반환하는 라우트는 제외합니다. `apiResource` 메서드를 사용하면 이 두 라우트가 자동으로 제외된 API용 리소스 라우트를 등록할 수 있습니다:

    use App\Http\Controllers\PhotoController;

    Route::apiResource('photos', PhotoController::class);

또한, 여러 API 리소스 컨트롤러를 한 번에 등록하려면 `apiResources` 메서드에 배열로 넘겨주면 됩니다:

    use App\Http\Controllers\PhotoController;
    use App\Http\Controllers\PostController;

    Route::apiResources([
        'photos' => PhotoController::class,
        'posts' => PostController::class,
    ]);

`create`, `edit` 메서드를 포함하지 않는 API 리소스 컨트롤러를 빠르게 생성하려면, `make:controller` 명령에서 `--api` 옵션을 사용하세요:

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스

때때로 중첩된 리소스 라우트가 필요할 수 있습니다. 예를 들어, 하나의 사진(photo) 리소스에 여러 댓글(comment)이 연결될 수 있습니다. 이런 중첩 리소스 컨트롤러는 라우트 선언 시 "도트(.)" 표기법을 사용하면 됩니다:

    use App\Http\Controllers\PhotoCommentController;

    Route::resource('photos.comments', PhotoCommentController::class);

이 라우트는 아래와 같은 URI로 중첩된 리소스에 접근할 수 있도록 등록됩니다:

    /photos/{photo}/comments/{comment}

<a name="scoping-nested-resources"></a>
#### 중첩 리소스의 스코프 지정

Laravel의 [암시적 모델 바인딩의 스코프 지정](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능을 사용하면, 바인딩된 하위 모델이 상위 모델에 소속되는지 자동으로 확인할 수 있습니다. 중첩 리소스를 선언할 때 `scoped` 메서드를 사용하여 자동 스코프 지정과, 자식 리소스를 어떤 필드로 가져올 것인지 지정할 수 있습니다. 자세한 내용은 [리소스 라우트 스코프 지정](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### 얕은 중첩(Shallow Nesting)

자식 ID만으로 충분히 유일성이 보장되는 경우, URI 내에 부모와 자식 ID를 모두 포함할 필요가 없습니다. 자동 증가되는 프라이머리 키 등 고유 식별자를 쓰는 경우 "얕은 중첩(shallow nesting)"을 사용할 수 있습니다:

    use App\Http\Controllers\CommentController;

    Route::resource('photos.comments', CommentController::class)->shallow();

이 라우트 선언 시 아래와 같은 라우트들이 정의됩니다:

| 메서드    | URI                                | 액션        | 라우트 이름
|-----------|------------------------------------|-------------|------------------------
| GET       | `/photos/{photo}/comments`         | index       | photos.comments.index
| GET       | `/photos/{photo}/comments/create`  | create      | photos.comments.create
| POST      | `/photos/{photo}/comments`         | store       | photos.comments.store
| GET       | `/comments/{comment}`              | show        | comments.show
| GET       | `/comments/{comment}/edit`         | edit        | comments.edit
| PUT/PATCH | `/comments/{comment}`              | update      | comments.update
| DELETE    | `/comments/{comment}`              | destroy     | comments.destroy

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 네이밍

기본적으로, 모든 리소스 컨트롤러 액션은 라우트 이름이 자동 할당됩니다. 원하는 라우트 이름이 있다면 `names` 배열로 오버라이드할 수 있습니다:

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->names([
        'create' => 'photos.build'
    ]);

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 네이밍

기본적으로 `Route::resource`는 리소스의 "단수형"을 기준으로 파라미터 이름을 만듭니다. 이를 개별 리소스별로 덮어쓰려면 `parameters` 메서드를 사용하세요. 전달할 배열은 리소스명과 파라미터명이 짝지어진 연관 배열이어야 합니다:

    use App\Http\Controllers\AdminUserController;

    Route::resource('users', AdminUserController::class)->parameters([
        'users' => 'admin_user'
    ]);

 위의 예제는 리소스의 `show` 라우트에 아래와 같은 URI를 생성합니다:

    /users/{admin_user}

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코프 지정

Laravel의 [스코프 지정 암시적 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능을 사용하면, 바인딩된 하위 모델이 상위 모델에 속하는지 자동으로 확인해줍니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용해 자동 스코프 지정은 물론, 자식 리소스를 가져올 필드를 지정할 수 있습니다:

    use App\Http\Controllers\PhotoCommentController;

    Route::resource('photos.comments', PhotoCommentController::class)->scoped([
        'comment' => 'slug',
    ]);

이 라우트는 아래와 같은 URI로 접근 가능한 스코프 지정 중첩 리소스를 등록합니다:

    /photos/{photo}/comments/{comment:slug}

중첩 라우트 파라미터로 커스텀 키 값을 사용하는 암시적 바인딩 시에도, Laravel은 부모 모델의 관계명을 추론하여 자동으로 쿼리의 범위를 부모에 맞춰 제한합니다. 이 경우 `Photo` 모델은 `comments`(파라미터 명의 복수형) 관계를 가져야 합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 로컬라이징

기본적으로, `Route::resource`는 영문 동사와 복수형 규칙을 사용해 리소스 URI를 만듭니다. `create`, `edit`와 같은 액션 동사를 로컬라이즈하려면, `App\Providers\RouteServiceProvider`의 `boot` 메서드 초기에 `Route::resourceVerbs` 메서드로 재정의할 수 있습니다:

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

Laravel의 복수형 변환은 [여러 언어를 지원](/docs/{{version}}/localization#pluralization-language)하며, 필요에 따라 설정할 수 있습니다. 커스텀 동사 및 복수형 언어 지정 후, 예를 들어 `Route::resource('publicacion', PublicacionController::class)`과 같이 라우트 등록 시 아래와 같은 URI가 만들어집니다:

    /publicacion/crear

    /publicacion/{publicaciones}/editar

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보충

리소스 컨트롤러에 기본 리소스 라우트 외에 추가 라우트를 정의하려면, `Route::resource`를 호출하기 전에 추가 라우트를 먼저 등록해야 합니다. 그렇지 않으면 `resource` 메서드에서 정의하는 라우트가 의도치 않게 우선 적용될 수 있습니다:

    use App\Http\Controller\PhotoController;

    Route::get('/photos/popular', [PhotoController::class, 'popular']);
    Route::resource('photos', PhotoController::class);

> **참고**  
> 컨트롤러는 하나의 목적에 집중하세요. 자주 리소스 액션 외의 메서드가 추가될 경우, 컨트롤러를 두 개의 작은 컨트롤러로 분리하는 것이 좋습니다.

<a name="singleton-resource-controllers"></a>
### 싱글톤 리소스 컨트롤러

어떤 리소스는 단 하나의 인스턴스만 존재할 수도 있습니다. 예를 들어, 각 사용자는 하나의 "프로필"만 가질 수 있으며, 이미지는 하나의 "썸네일"만 가질 수 있습니다. 이를 "싱글톤 리소스"라고 하며, 하나의 인스턴스만 존재합니다. 이런 경우 "싱글톤" 리소스 컨트롤러를 등록할 수 있습니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위 싱글톤 리소스 정의는 다음과 같은 라우트를 등록합니다. "생성" 관련 라우트는 등록되지 않으며, 인스턴스가 하나이므로 라우트가 식별자를 받지 않습니다:

| 메서드    | URI                    | 액션    | 라우트 이름
|-----------|------------------------|---------|------------------------
| GET       | `/profile`             | show    | profile.show
| GET       | `/profile/edit`        | edit    | profile.edit
| PUT/PATCH | `/profile`             | update  | profile.update

싱글톤 리소스는 일반 리소스에 중첩할 수도 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 예제에서 `photos` 리소스는 [표준 리소스 라우트](#actions-handled-by-resource-controller)를 모두 받게 되지만, `thumbnail`은 아래와 같은 싱글톤 리소스 라우트만 가집니다:

| 메서드    | URI                               | 액션    | 라우트 이름
|-----------|-----------------------------------|---------|--------------------------
| GET       | `/photos/{photo}/thumbnail`       | show    | photos.thumbnail.show
| GET       | `/photos/{photo}/thumbnail/edit`  | edit    | photos.thumbnail.edit
| PUT/PATCH | `/photos/{photo}/thumbnail`       | update  | photos.thumbnail.update

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글톤 리소스

가끔 싱글톤 리소스에도 생성 및 저장 라우트가 필요할 수 있습니다. 이 경우, 싱글톤 리소스 라우트 등록 시 `creatable` 메서드를 호출하세요:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이 예제에서는 아래와 같은 라우트가 등록됩니다. 생성 가능한 싱글톤 리소스에는 `DELETE` 라우트도 등록됩니다:

| 메서드    | URI                                  | 액션    | 라우트 이름
|-----------|--------------------------------------|---------|--------------------------
| GET       | `/photos/{photo}/thumbnail/create`   | create  | photos.thumbnail.create
| POST      | `/photos/{photo}/thumbnail`          | store   | photos.thumbnail.store
| GET       | `/photos/{photo}/thumbnail`          | show    | photos.thumbnail.show
| GET       | `/photos/{photo}/thumbnail/edit`     | edit    | photos.thumbnail.edit
| PUT/PATCH | `/photos/{photo}/thumbnail`          | update  | photos.thumbnail.update
| DELETE    | `/photos/{photo}/thumbnail`          | destroy | photos.thumbnail.destroy

생성 및 저장 라우트 없이, 삭제 라우트만 등록하려면 `destroyable` 메서드를 사용합니다:

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글톤 리소스

`apiSingleton` 메서드는 API로 관리할 싱글톤 리소스를 등록할 때 사용하며, 이 경우 `create`, `edit` 라우트는 포함되지 않습니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```

API 싱글톤 리소스에도 `creatable` 메서드를 통해 `store`, `destroy` 라우트를 추가할 수 있습니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러

<a name="constructor-injection"></a>
#### 생성자 주입

Laravel의 [서비스 컨테이너](/docs/{{version}}/container)는 모든 컨트롤러를 해석할 때 사용됩니다. 따라서, 컨트롤러 생성자에 필요한 의존성을 타입힌트하면 자동으로 해결되어 인스턴스에 주입됩니다:

    <?php

    namespace App\Http\Controllers;

    use App\Repositories\UserRepository;

    class UserController extends Controller
    {
        /**
         * 사용자 리포지토리 인스턴스.
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

<a name="method-injection"></a>
#### 메서드 주입

생성자 주입 외에도, 컨트롤러의 메서드에서 직접 의존성을 타입힌트할 수 있습니다. 가장 흔한 예는 `Illuminate\Http\Request` 인스턴스를 컨트롤러 메서드로 주입받는 경우입니다:

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

컨트롤러 메서드에서 라우트 파라미터의 입력도 함께 받으려면, 의존성 뒤에 해당 파라미터를 나열하면 됩니다. 예를 들어 라우트가 다음과 같이 정의되어 있다면:

    use App\Http\Controllers\UserController;

    Route::put('/user/{id}', [UserController::class, 'update']);

`Illuminate\Http\Request`를 타입힌트하고, `id` 파라미터를 접근할 수 있습니다:

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