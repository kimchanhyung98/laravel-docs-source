# Laravel Folio

- [소개](#introduction)
- [설치](#installation)
    - [페이지 경로 / URI](#page-paths-uris)
    - [서브도메인 라우팅](#subdomain-routing)
- [라우트 생성](#creating-routes)
    - [중첩 라우트](#nested-routes)
    - [인덱스 라우트](#index-routes)
- [라우트 파라미터](#route-parameters)
- [라우트 모델 바인딩](#route-model-binding)
    - [소프트 삭제된 모델](#soft-deleted-models)
- [렌더 훅](#render-hooks)
- [네임드 라우트](#named-routes)
- [미들웨어](#middleware)
- [라우트 캐싱](#route-caching)

<a name="introduction"></a>
## 소개

[Laravel Folio](https://github.com/laravel/folio)는 라라벨 애플리케이션에서 라우팅을 간편하게 만들어 주는 강력한 페이지 기반 라우터입니다. Laravel Folio를 사용하면, 애플리케이션의 `resources/views/pages` 디렉터리에 Blade 템플릿을 생성하는 것만으로도 라우트를 간단히 만들 수 있습니다.

예를 들어, `/greeting` URL로 접근 가능한 페이지를 만들고 싶다면, 애플리케이션의 `resources/views/pages` 디렉터리에 `greeting.blade.php` 파일을 생성하세요.

```php
<div>
    Hello World
</div>
```

<a name="installation"></a>
## 설치

시작하려면, Composer 패키지 매니저를 사용해 Folio를 프로젝트에 설치하세요:

```shell
composer require laravel/folio
```

Folio 설치 후 `folio:install` 아티즌 명령어를 실행하면, Folio의 서비스 프로바이더가 애플리케이션에 등록됩니다. 이 서비스 프로바이더는 Folio가 라우트/페이지를 탐색할 디렉터리를 등록합니다:

```shell
php artisan folio:install
```

<a name="page-paths-uris"></a>
### 페이지 경로 / URI

기본적으로 Folio는 애플리케이션의 `resources/views/pages` 디렉터리에서 페이지를 제공합니다. 하지만, Folio 서비스 프로바이더의 `boot` 메서드에서 이 디렉터리를 맞춤 설정할 수 있습니다.

예를 들어, 하나의 라라벨 애플리케이션에서 여러 Folio 경로를 지정하고 싶을 수도 있습니다. 예를 들어, 애플리케이션의 "관리자" 영역에 대해 Folio 페이지를 별도의 디렉터리에 두고, 나머지 페이지들은 다른 디렉터리에 두고 싶을 수 있습니다.

이럴 때는 `Folio::path`와 `Folio::uri` 메서드를 사용할 수 있습니다. `path` 메서드는 Folio가 HTTP 요청을 라우팅할 때 페이지를 검색할 디렉터리를 등록하고, `uri` 메서드는 해당 페이지 디렉터리의 "기본 URI"를 지정합니다:

```php
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages/guest'))->uri('/');

Folio::path(resource_path('views/pages/admin'))
    ->uri('/admin')
    ->middleware([
        '*' => [
            'auth',
            'verified',

            // ...
        ],
    ]);
```

<a name="subdomain-routing"></a>
### 서브도메인 라우팅

요청의 서브도메인에 따라 페이지를 라우팅할 수도 있습니다. 예를 들어, `admin.example.com`에서 들어오는 요청을 Folio의 나머지 페이지와 다른 디렉터리로 라우팅하고 싶을 때가 있습니다. 이 경우엔 `Folio::path` 호출 후 `domain` 메서드를 사용하세요:

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));
```

`domain` 메서드는 도메인이나 서브도메인의 일부를 파라미터로 받아올 수 있게 해줍니다. 이 파라미터는 페이지 템플릿에서 사용할 수 있습니다:

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));
```

<a name="creating-routes"></a>
## 라우트 생성

Folio에 마운트된 디렉터리 중 하나에 Blade 템플릿을 두는 것만으로 Folio 라우트를 만들 수 있습니다. 기본적으로 Folio는 `resources/views/pages` 디렉터리에 마운트되어 있죠. 이 디렉터리들은 Folio 서비스 프로바이더의 `boot` 메서드에서 맞춤 설정할 수 있습니다.

Folio에 마운트된 디렉터리에 Blade 템플릿을 만들어 두면, 바로 브라우저에서 접근할 수 있습니다. 예를 들어, `pages/schedule.blade.php` 파일은 브라우저에서 `http://example.com/schedule`로 접근할 수 있습니다.

등록된 Folio 페이지/라우트 목록을 빠르게 확인하려면, `folio:list` 아티즌 명령어를 사용하세요:

```shell
php artisan folio:list
```

<a name="nested-routes"></a>
### 중첩 라우트

Folio 디렉터리 내에 하나 이상의 디렉터리를 생성해서 중첩 라우트를 만들 수 있습니다. 예를 들어, `/user/profile` 경로로 접근 가능한 페이지를 생성하려면, `pages/user` 디렉터리 안에 `profile.blade.php` 템플릿을 생성하세요:

```shell
php artisan folio:page user/profile

# pages/user/profile.blade.php → /user/profile
```

<a name="index-routes"></a>
### 인덱스 라우트

특정 디렉터리의 "인덱스" 역할을 하는 페이지를 만들고 싶다면, Folio 디렉터리에 `index.blade.php` 템플릿을 두면 됩니다. 해당 디렉터리의 루트로 들어오는 모든 요청이 이 페이지로 라우팅됩니다.

```shell
php artisan folio:page index
# pages/index.blade.php → /

php artisan folio:page users/index
# pages/users/index.blade.php → /users
```

<a name="route-parameters"></a>
## 라우트 파라미터

실무에서, 종종 들어오는 요청의 URL 일부를 페이지로 전달받아야 할 필요가 있습니다. 예를 들어, 특정 사용자의 프로필을 보여주는 페이지에서는 "ID"에 접근해야 할 수 있습니다. 이를 위해, 페이지 파일 이름의 일부를 대괄호(`[]`)로 감싸면 해당 URL 세그먼트가 파라미터로 바인딩됩니다.

```shell
php artisan folio:page "users/[id]"

# pages/users/[id].blade.php → /users/1
```

바인딩된 세그먼트는 Blade 템플릿 내에서 변수로 사용할 수 있습니다:

```html
<div>
    User {{ $id }}
</div>
```

여러 세그먼트를 바인딩하려면, 대괄호 앞에 `...`(점 3개)를 붙이세요:

```shell
php artisan folio:page "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3
```

여러 세그먼트를 바인딩할 경우, 배열 형태로 전달됩니다:

```html
<ul>
    @foreach ($ids as $id)
        <li>User {{ $id }}</li>
    @endforeach
</ul>
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩

페이지 템플릿 파일명 안의 와일드카드 세그먼트가 애플리케이션의 Eloquent 모델 중 하나와 일치하면, Folio는 라라벨의 라우트 모델 바인딩을 자동으로 이용해 해당 모델 인스턴스를 페이지로 주입합니다:

```shell
php artisan folio:page "users/[User]"

# pages/users/[User].blade.php → /users/1
```

바인딩된 모델은 Blade 템플릿 내에서 변수(카멜케이스)로 사용할 수 있습니다:

```html
<div>
    User {{ $user->id }}
</div>
```

#### 바인딩 키 커스터마이징

때로는 Eloquent 모델을 `id`가 아닌 다른 컬럼으로 바인딩하고 싶을 수 있습니다. 이 때는 파일명에서 모델명 뒤에 콜론(`:`)과 컬럼명을 지정하세요. 예를 들어, `[Post:slug].blade.php` 파일은 `id` 대신 `slug` 컬럼으로 모델을 바인딩합니다.

Windows 환경에서는 하이픈(`-`)으로 구분해야 합니다: `[Post-slug].blade.php`.

#### 모델 위치 지정

기본적으로 Folio는 애플리케이션의 `app/Models` 디렉터리에서 모델을 찾습니다. 다른 위치에 있다면, 파일명에서 전체 네임스페이스를 명시할 수 있습니다:

```shell
php artisan folio:page "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1
```

<a name="soft-deleted-models"></a>
### 소프트 삭제된 모델

기본적으로 소프트 삭제된(soft deleted) 모델은 암시적 모델 바인딩 시 조회되지 않습니다. 하지만 필요하다면, 페이지 템플릿 내에서 `withTrashed` 함수를 호출하여 소프트 삭제된 모델도 조회 가능하게 할 수 있습니다.

```php
<?php

use function Laravel\Folio\{withTrashed};

withTrashed();

?>

<div>
    User {{ $user->id }}
</div>
```

<a name="render-hooks"></a>
## 렌더 훅

기본적으로 Folio는 페이지의 Blade 템플릿 내용을 요청에 대한 응답으로 반환합니다. 하지만, 페이지 템플릿 안에서 `render` 함수를 호출해 응답을 자유롭게 커스터마이징할 수 있습니다.

`render` 함수는 클로저를 인자로 받으며, Folio에서 렌더링 중인 `View` 인스턴스를 매개변수로 전달합니다. 이 클로저를 통해 뷰에 추가 데이터를 전달하거나, 응답 전체를 변경할 수 있습니다. 추가로, 모든 라우트 파라미터 또는 모델 바인딩도 클로저에 함께 전달됩니다:

```php
<?php

use App\Models\Post;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

use function Laravel\Folio\render;

render(function (View $view, Post $post) {
    if (! Auth::user()->can('view', $post)) {
        return response('Unauthorized', 403);
    }

    return $view->with('photos', $post->author->photos);
}); ?>

<div>
    {{ $post->content }}
</div>

<div>
    This author has also taken {{ count($photos) }} photos.
</div>
```

<a name="named-routes"></a>
## 네임드 라우트

특정 페이지 라우트에 `name` 함수를 사용해 이름을 부여할 수 있습니다:

```php
<?php

use function Laravel\Folio\name;

name('users.index');
```

라라벨의 네임드 라우트처럼, `route` 함수를 이용해 이름이 지정된 Folio 페이지의 URL을 생성할 수 있습니다:

```php
<a href="{{ route('users.index') }}">
    All Users
</a>
```

페이지가 파라미터를 사용하는 경우, 값을 배열로 `route` 함수에 넘기면 됩니다:

```php
route('users.show', ['user' => $user]);
```

<a name="middleware"></a>
## 미들웨어

페이지별로 미들웨어를 적용하려면, 페이지 템플릿 내부에서 `middleware` 함수를 호출하세요:

```php
<?php

use function Laravel\Folio\{middleware};

middleware(['auth', 'verified']);

?>

<div>
    Dashboard
</div>
```

또는 여러 페이지에 일괄 미들웨어를 적용하려면, `Folio::path` 호출 뒤에 `middleware` 메서드를 체이닝하면 됩니다.

어떤 라우트에 미들웨어를 적용할지 지정하려면, 미들웨어 배열의 키로 해당 URL 패턴을 지정하세요. `*` 문자를 와일드카드로 사용할 수 있습니다:

```php
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages'))->middleware([
    'admin/*' => [
        'auth',
        'verified',

        // ...
    ],
]);
```

미들웨어 배열에 클로저를 추가해 인라인(익명) 미들웨어를 정의할 수도 있습니다:

```php
use Closure;
use Illuminate\Http\Request;
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages'))->middleware([
    'admin/*' => [
        'auth',
        'verified',

        function (Request $request, Closure $next) {
            // ...

            return $next($request);
        },
    ],
]);
```

<a name="route-caching"></a>
## 라우트 캐싱

Folio를 사용할 때는 반드시 [라라벨의 라우트 캐싱 기능](/docs/{{version}}/routing#route-caching)을 활용해야 합니다. Folio는 `route:cache` 아티즌 명령을 감지하여, Folio 페이지 정의와 라우트 이름을 최적의 성능을 위해 올바르게 캐시합니다.