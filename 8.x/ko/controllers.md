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
    - [리소스 라우트 스코프 지정](#restful-scoping-resource-routes)
    - [리소스 URI 현지화](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 확장](#restful-supplementing-resource-controllers)
- [의존성 주입 & 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개

모든 요청 처리 로직을 라우트 파일의 클로저로 정의하는 대신, "컨트롤러" 클래스를 사용해 이 동작을 구조화할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스로 그룹화할 수 있습니다. 예를 들어, `UserController` 클래스는 사용자의 조회, 생성, 수정, 삭제 등 사용자와 관련된 모든 요청을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성하기

<a name="basic-controllers"></a>
### 기본 컨트롤러

아래는 기본 컨트롤러의 예제입니다. 컨트롤러는 라라벨에 포함된 기본 컨트롤러 클래스(`App\Http\Controllers\Controller`)를 확장합니다.

```php
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

다음과 같이 이 컨트롤러 메소드에 대한 라우트를 정의할 수 있습니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

들어오는 요청이 지정된 라우트 URI와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메소드가 호출되고, 라우트 파라미터가 메소드에 전달됩니다.

> {tip} 컨트롤러가 **반드시** 기본 클래스를 확장해야 하는 것은 아닙니다. 하지만 `middleware` 및 `authorize`와 같은 편리한 기능을 사용하려면 기본 클래스를 확장해야 합니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러

컨트롤러의 동작이 특히 복잡하다면, 해당 단일 액션에만 전념하는 컨트롤러 클래스를 만드는 것이 편리할 수 있습니다. 이를 위해 컨트롤러 내에 단일 `__invoke` 메소드를 정의하면 됩니다.

```php
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

단일 액션 컨트롤러를 위한 라우트를 등록할 때는, 컨트롤러 메소드를 별도로 지정할 필요가 없습니다. 컨트롤러 이름만 라우터에 전달하면 됩니다.

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` Artisan 명령의 `--invokable` 옵션을 사용해, 호출 가능한(invokable) 컨트롤러를 빠르게 생성할 수 있습니다.

```
php artisan make:controller ProvisionServer --invokable
```

> {tip} 컨트롤러 스텁은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

[미들웨어](/docs/{{version}}/middleware)는 라우트 파일에서 컨트롤러의 라우트에 할당할 수 있습니다.

```php
Route::get('profile', [UserController::class, 'show'])->middleware('auth');
```

또는, 컨트롤러의 생성자에서 미들웨어를 지정하는 것도 편리할 수 있습니다. 생성자 내에서 `middleware` 메소드를 사용하여 컨트롤러의 액션에 미들웨어를 할당할 수 있습니다.

```php
class UserController extends Controller
{
    /**
     * 새로운 컨트롤러 인스턴스를 생성합니다.
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

컨트롤러에서는 클로저를 사용하여 미들웨어를 등록할 수도 있습니다. 이를 통해 별도의 미들웨어 클래스를 정의하지 않고도, 개별 컨트롤러용 인라인 미들웨어를 편리하게 지정할 수 있습니다.

```php
$this->middleware(function ($request, $next) {
    return $next($request);
});
```

<a name="resource-controllers"></a>
## 리소스 컨트롤러

애플리케이션의 각 Eloquent 모델을 "리소스"로 간주하면, 보통 각 리소스에 대해 동일한 작업(예: 생성, 조회, 수정, 삭제)을 수행하게 됩니다. 예를 들어 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다면, 사용자가 이들 리소스를 생성, 읽기, 수정, 삭제할 수 있을 것입니다.

이러한 일반적인 케이스 때문에, 라라벨 리소스 라우팅은 컨트롤러에 한 줄의 코드만으로 CRUD 작업에 대한 라우트를 할당할 수 있도록 해줍니다. 먼저, `make:controller` Artisan 명령의 `--resource` 옵션을 사용해, 이 작업을 처리할 수 있는 컨트롤러를 빠르게 생성할 수 있습니다.

```
php artisan make:controller PhotoController --resource
```

이 명령은 `app/Http/Controllers/PhotoController.php` 위치에 컨트롤러를 생성합니다. 컨트롤러에는 각 리소스 작업에 맞는 메소드가 포함되어 있습니다. 다음으로, 이 컨트롤러를 가리키는 리소스 라우트를 등록합니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 라우트 선언 한 줄로 다양한 리소스 작업을 처리하는 여러 라우트가 생성됩니다. 생성된 컨트롤러에는 각 동작에 대한 스텁 메소드가 이미 포함되어 있습니다. `route:list` Artisan 명령어를 실행하면 애플리케이션의 라우트를 빠르게 확인할 수 있습니다.

여러 리소스 컨트롤러를 동시에 등록하고 싶다면, `resources` 메소드에 배열을 전달하면 됩니다.

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controller"></a>
#### 리소스 컨트롤러가 처리하는 동작

Verb      | URI                        | 동작        | 라우트 이름
----------|----------------------------|------------|---------------------
GET       | `/photos`                  | index      | photos.index
GET       | `/photos/create`           | create     | photos.create
POST      | `/photos`                  | store      | photos.store
GET       | `/photos/{photo}`          | show       | photos.show
GET       | `/photos/{photo}/edit`     | edit       | photos.edit
PUT/PATCH | `/photos/{photo}`          | update     | photos.update
DELETE    | `/photos/{photo}`          | destroy    | photos.destroy

<a name="customizing-missing-model-behavior"></a>
#### 모델 누락 시 동작 커스터마이즈

일반적으로, 명시적 바인딩된 리소스 모델을 찾을 수 없는 경우 404 HTTP 응답이 반환됩니다. 그러나, 리소스 라우트를 정의할 때 `missing` 메소드를 호출하여 이 동작을 커스터마이즈할 수 있습니다. `missing` 메소드는, 리소스의 명시적 바인딩 모델을 찾을 수 없을 때 호출되는 클로저를 인수로 받습니다.

```php
use App\Http\Controllers\PhotoController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::resource('photos', PhotoController::class)
        ->missing(function (Request $request) {
            return Redirect::route('photos.index');
        });
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정

[라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 사용하는 경우, 리소스 컨트롤러의 메소드에서 모델 인스턴스를 타입힌트 하고 싶다면, 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다.

```
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 리퀘스트 생성

리소스 컨트롤러를 생성할 때 `--requests` 옵션을 제공하면, Artisan이 컨트롤러의 저장 및 업데이트 메소드에 대한 [폼 리퀘스트 클래스](/docs/{{version}}/validation#form-request-validation)를 생성해줍니다.

```
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트를 선언할 때, 컨트롤러가 처리해야 하는 작업의 일부만 명시할 수도 있습니다.

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

API에서 사용될 리소스 라우트를 선언할 때는 `create`나 `edit`처럼 HTML 템플릿을 반환하는 라우트를 제외하는 것이 일반적입니다. 편의를 위해 `apiResource` 메소드를 사용하면 이 두 라우트가 자동으로 제외됩니다.

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

여러 API 리소스 컨트롤러를 동시에 등록하려면, `apiResources` 메소드에 배열을 전달할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`make:controller` 명령에서 `--api` 옵션을 사용하면 `create`, `edit` 메소드가 포함되지 않은 API용 리소스 컨트롤러를 빠르게 생성할 수 있습니다.

```
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스

때때로, 중첩 리소스에 대한 라우트를 정의해야 할 수 있습니다. 예를 들어, 하나의 사진 리소스에는 여러 댓글이 달릴 수 있습니다. 중첩 리소스 컨트롤러를 등록할 때는 라우트 선언에서 "점(dot) 표기법"을 사용합니다.

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 URI 형식으로 중첩 리소스에 접근할 수 있도록 합니다.

```
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스 스코프 지정

라라벨의 [암시적(implicit) 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능은, 자식 모델이 부모 모델에 속해있는지 자동으로 확인하도록 중첩 바인딩의 스코프를 지정할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메소드를 사용하면 자동 스코핑 및 어떤 필드로 자식 리소스를 조회할지 지정할 수 있습니다. 자세한 내용은 [리소스 라우트 스코프 지정 문서](#restful-scoping-resource-routes)를 참고하세요.

<a name="shallow-nesting"></a>
#### 얕은 중첩(Shallow Nesting)

대개 URI 내에 부모와 자식 ID 둘 다 필요하지 않을 수 있습니다. 자식 ID가 이미 고유 식별자인 경우에는 "shallow nesting"을 사용하는 것이 가능합니다.

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

이 라우트 정의는 아래와 같은 라우트를 만듭니다.

Verb      | URI                                   | 동작      | 라우트 이름
----------|---------------------------------------|----------|---------------------
GET       | `/photos/{photo}/comments`            | index    | photos.comments.index
GET       | `/photos/{photo}/comments/create`     | create   | photos.comments.create
POST      | `/photos/{photo}/comments`            | store    | photos.comments.store
GET       | `/comments/{comment}`                 | show     | comments.show
GET       | `/comments/{comment}/edit`            | edit     | comments.edit
PUT/PATCH | `/comments/{comment}`                 | update   | comments.update
DELETE    | `/comments/{comment}`                 | destroy  | comments.destroy

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정

기본적으로, 모든 리소스 컨트롤러 액션은 라우트 이름을 가집니다. 하지만, `names` 배열을 전달하여 원하시는 라우트 이름으로 오버라이드할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 이름 지정

기본적으로 `Route::resource`는 리소스 이름의 "단수형"을 사용해서 라우트 파라미터를 생성합니다. `parameters` 메소드를 사용해 리소스별로 손쉽게 오버라이드할 수 있습니다. `parameters` 메소드에 전달되는 배열은 리소스 이름과 파라미터 이름이 쌍을 이루는 연관 배열이어야 합니다.

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예시는 리소스의 `show` 라우트의 URI를 다음과 같이 생성합니다.

```
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 스코프 지정

라라벨의 [스코프된 암시적 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능은, 자식 모델이 부모 모델에 속해 있음을 자동으로 확인하도록 중첩 바인딩을 스코프할 수 있게 해줍니다. 중첩 리소스를 정의할 때 `scoped` 메소드를 사용하면, 자동 스코핑과 자식 리소스를 어떤 필드로 조회할지 지정할 수 있습니다.

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 아래와 같은 URI로 스코프가 적용된 중첩 리소스를 사용할 수 있게 해줍니다.

```
/photos/{photo}/comments/{comment:slug}
```

맞춤 키를 사용한 암시적 바인딩이 중첩 라우트 파라미터로 사용될 때, 라라벨은 부모와의 관계를 추정하여 자식 모델 쿼리에 자동으로 스코프를 적용합니다. 이 경우, `Photo` 모델에 `comments`라는(파라미터 명의 복수형) 관계가 있다고 가정하여 `Comment` 모델을 조회합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화

기본적으로 `Route::resource`는 리소스 URI에 영어 동사(create, edit 등)를 사용합니다. `create`, `edit` 등의 액션 동사를 현지화하려면, 앱의 `App\Providers\RouteServiceProvider` 클래스의 `boot` 메소드 내에서 `Route::resourceVerbs` 메소드를 사용할 수 있습니다.

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

동사가 커스터마이즈되면, 예를 들어 `Route::resource('fotos', PhotoController::class)`와 같은 리소스 라우트를 등록할 때 아래와 같은 URI가 생성됩니다.

```
/fotos/crear

/fotos/{foto}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 확장

기본 리소스 라우트 외에 추가적인 라우트를 리소스 컨트롤러에 등록하려면, 추가 라우트를 반드시 `Route::resource` 메소드보다 먼저 정의해야 합니다. 그렇지 않으면 `resource` 메소드에서 정의된 라우트가 추가 라우트보다 우선 적용될 수 있습니다.

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> {tip} 컨트롤러의 역할을 명확하게 유지하세요. 일반적인 리소스 액션 외의 메소드가 자주 필요하다면, 컨트롤러를 더 작은 두 개 이상의 컨트롤러로 분리하는 것을 고려하세요.

<a name="dependency-injection-and-controllers"></a>
## 의존성 주입 & 컨트롤러

<a name="constructor-injection"></a>
#### 생성자 주입

라라벨의 [서비스 컨테이너](/docs/{{version}}/container)는 모든 컨트롤러를 해석할 때 사용됩니다. 따라서, 컨트롤러의 생성자에서 필요한 의존성을 타입힌트 할 수 있습니다. 선언된 의존성은 자동으로 해석되어 컨트롤러 인스턴스에 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * 사용자 리포지터리 인스턴스.
     */
    protected $users;

    /**
     * 새로운 컨트롤러 인스턴스를 생성합니다.
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
#### 메소드 주입

생성자 주입 외에도, 컨트롤러의 메소드에서 의존성을 타입힌트 할 수도 있습니다. 메소드 주입의 일반적인 예로, `Illuminate\Http\Request` 인스턴스를 컨트롤러 메소드에 주입하는 것이 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새 사용자를 저장합니다.
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

컨트롤러 메소드가 라우트 파라미터의 입력값도 기대하는 경우, 라우트 인수를 다른 의존성 다음에 나열하면 됩니다. 예를 들어, 라우트가 아래와 같이 정의되어 있을 때,

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

아래와 같이 컨트롤러 메소드를 정의하면 `Illuminate\Http\Request`도 주입받고, `id` 파라미터도 받을 수 있습니다.

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