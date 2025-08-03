# Laravel Folio

- [소개](#introduction)
- [설치](#installation)
    - [페이지 경로 / URI](#page-paths-uris)
    - [서브도메인 라우팅](#subdomain-routing)
- [라우트 생성하기](#creating-routes)
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
## 소개 (Introduction)

[Laravel Folio](https://github.com/laravel/folio)는 Laravel 애플리케이션에서 라우팅을 간편하게 할 수 있도록 설계된 강력한 페이지 기반 라우터입니다. Laravel Folio를 사용하면 라우트를 만드는 것이 애플리케이션의 `resources/views/pages` 디렉토리에 Blade 템플릿을 생성하는 것만큼 쉽습니다.

예를 들어 `/greeting` URL로 접근 가능한 페이지를 만들고 싶다면, 애플리케이션의 `resources/views/pages` 디렉토리에 `greeting.blade.php` 파일을 생성하면 됩니다:

```php
<div>
    Hello World
</div>
```

<a name="installation"></a>
## 설치 (Installation)

시작하려면 Composer 패키지 매니저를 사용해 Folio를 프로젝트에 설치하세요:

```bash
composer require laravel/folio
```

Folio를 설치한 후에는 `folio:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 Folio의 서비스 프로바이더를 애플리케이션에 등록하며, Folio가 라우트/페이지를 검색할 디렉토리를 등록합니다:

```bash
php artisan folio:install
```

<a name="page-paths-uris"></a>
### 페이지 경로 / URI (Page Paths / URIs)

기본적으로 Folio는 애플리케이션의 `resources/views/pages` 디렉토리에서 페이지를 제공합니다. 그러나 Folio 서비스 프로바이더의 `boot` 메서드에서 이 디렉토리를 변경하거나 여러 경로를 지정할 수도 있습니다.

예를 들어, 동일한 Laravel 애플리케이션 내에서 여러 Folio 경로를 지정해 "admin" 영역 전용 페이지 디렉토리를 따로 두고 나머지는 다른 디렉토리를 사용하는 것이 편리할 때가 있습니다.

이럴 경우 `Folio::path` 메서드와 `Folio::uri` 메서드를 사용해 설정할 수 있습니다. `path` 메서드는 Folio가 페이지를 검색할 디렉토리를 등록하고, `uri` 메서드는 그 디렉토리 페이지의 "기본 URI"를 지정합니다:

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
### 서브도메인 라우팅 (Subdomain Routing)

요청의 서브도메인에 따라 다른 페이지 디렉토리로 라우팅할 수도 있습니다. 예를 들어, `admin.example.com`에서 오는 요청은 다른 Folio 페이지 디렉토리로 라우팅하고 싶을 때, `Folio::path` 메서드 호출 후 `domain` 메서드를 사용하면 됩니다:

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));
```

`domain` 메서드는 도메인이나 서브도메인의 일부를 파라미터로 캡처하는 것도 지원하며, 이 파라미터들은 페이지 템플릿에 자동으로 주입됩니다:

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));
```

<a name="creating-routes"></a>
## 라우트 생성하기 (Creating Routes)

Folio가 마운트한 디렉토리에 Blade 템플릿을 배치하면 Folio 라우트가 자동 생성됩니다. 기본적으로 Folio는 `resources/views/pages` 디렉토리를 마운트하지만, 서비스 프로바이더의 `boot` 메서드에서 변경할 수 있습니다.

Blade 템플릿이 Folio 마운트된 디렉토리에 배치되면 즉시 웹 브라우저에서 접근이 가능합니다. 예를 들어 `pages/schedule.blade.php`에 페이지를 만들면 `http://example.com/schedule`로 접근할 수 있습니다.

모든 Folio 페이지/라우트 리스트를 빠르게 확인하려면 `folio:list` Artisan 명령어를 사용하세요:

```bash
php artisan folio:list
```

<a name="nested-routes"></a>
### 중첩 라우트 (Nested Routes)

하위 디렉토리를 만들어 중첩 라우트를 생성할 수 있습니다. 예를 들어 `/user/profile` 경로에 접근 가능한 페이지를 만들려면 `pages/user/profile.blade.php` 템플릿을 생성하세요:

```bash
php artisan folio:page user/profile

# pages/user/profile.blade.php → /user/profile
```

<a name="index-routes"></a>
### 인덱스 라우트 (Index Routes)

특정 디렉토리의 "인덱스" 페이지로 지정하고 싶다면 그 디렉토리에 `index.blade.php` 템플릿을 배치하세요. 그러면 그 디렉토리 루트로 요청이 들어왔을 때 해당 페이지로 라우팅됩니다:

```bash
php artisan folio:page index
# pages/index.blade.php → /

php artisan folio:page users/index
# pages/users/index.blade.php → /users
```

<a name="route-parameters"></a>
## 라우트 파라미터 (Route Parameters)

종종 요청 URL 경로의 일부를 페이지에 주입해서 활용해야 할 때가 있습니다. 예를 들어, 프로필 페이지라면 해당 사용자의 ID를 받아야 할 것입니다. 이때 페이지 파일명에서 URL 세그먼트를 대괄호로 감싸면 파라미터로 캡처됩니다:

```bash
php artisan folio:page "users/[id]"

# pages/users/[id].blade.php → /users/1
```

캡처된 세그먼트는 Blade 템플릿 내 변수로 접근할 수 있습니다:

```html
<div>
    User {{ $id }}
</div>
```

여러 개의 세그먼트를 캡처하려면 세그먼트 이름 앞에 세 개의 점(`...`)을 붙이세요:

```bash
php artisan folio:page "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3
```

이 경우 캡처된 여러 세그먼트는 배열로 페이지에 주입됩니다:

```html
<ul>
    @foreach ($ids as $id)
        <li>User {{ $id }}</li>
    @endforeach
</ul>
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

페이지 파일명에서 와일드카드 세그먼트가 애플리케이션의 Eloquent 모델 이름과 일치하면, Folio는 Laravel의 라우트 모델 바인딩 기능을 자동으로 활용해 모델 인스턴스를 페이지에 주입하려 시도합니다:

```bash
php artisan folio:page "users/[User]"

# pages/users/[User].blade.php → /users/1
```

바인딩된 모델은 Blade 템플릿 내에서 변수로 접근할 수 있으며, 변수명은 카멜 케이스(camel case)로 변환됩니다:

```html
<div>
    User {{ $user->id }}
</div>
```

#### 키 지정하기 (Customizing the Key)

때때로 `id` 컬럼이 아닌 다른 컬럼으로 모델을 바인딩해야 할 경우가 있습니다. 이때는 페이지 파일명에 컬럼명을 지정할 수 있습니다. 예를 들어 `[Post:slug].blade.php`는 `id` 대신 `slug` 컬럼으로 모델을 조회합니다.

Windows 환경에서는 콜론 대신 하이픈(`-`)을 사용해 모델명과 키를 구분하세요: `[Post-slug].blade.php`.

#### 모델 위치 (Model Location)

기본적으로 Folio는 모델을 애플리케이션의 `app/Models` 디렉토리에서 검색합니다. 하지만 필요하면 템플릿 파일명에 모델의 FQCN(fully-qualified class name)을 직접 지정할 수 있습니다:

```bash
php artisan folio:page "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1
```

<a name="soft-deleted-models"></a>
### 소프트 삭제된 모델 (Soft Deleted Models)

기본적으로 소프트 삭제된 모델은 암묵적 모델 바인딩 시 조회되지 않습니다. 하지만 원한다면 페이지 템플릿 내에서 `withTrashed` 함수를 호출해 소프트 삭제된 모델까지 조회할 수 있도록 할 수 있습니다:

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
## 렌더 훅 (Render Hooks)

기본적으로 Folio는 페이지의 Blade 템플릿 내용을 요청에 대한 응답으로 반환합니다. 하지만 `render` 함수를 페이지 템플릿 내에서 호출하면 응답을 사용자 지정할 수 있습니다.

`render` 함수는 클로저를 받으며, 이 클로저는 Folio가 렌더링하는 `View` 인스턴스를 전달받습니다. 이를 통해 뷰에 추가 데이터를 전달하거나 응답 전체를 맞춤 처리할 수 있습니다. 또, 라우트 파라미터나 모델 바인딩 인스턴스들도 클로저 인수로 함께 전달됩니다:

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
## 네임드 라우트 (Named Routes)

특정 페이지 라우트에 이름을 지정하려면 `name` 함수를 사용하세요:

```php
<?php

use function Laravel\Folio\name;

name('users.index');
```

Laravel 네임드 라우트와 마찬가지로, 이름이 지정된 Folio 페이지의 URL을 생성하려면 `route` 함수를 사용하면 됩니다:

```php
<a href="{{ route('users.index') }}">
    All Users
</a>
```

만약 페이지가 파라미터를 가진다면 해당 값을 `route` 함수에 넘겨주면 됩니다:

```php
route('users.show', ['user' => $user]);
```

<a name="middleware"></a>
## 미들웨어 (Middleware)

특정 페이지에 미들웨어를 적용하려면 페이지 템플릿 내에서 `middleware` 함수를 호출하세요:

```php
<?php

use function Laravel\Folio\{middleware};

middleware(['auth', 'verified']);

?>

<div>
    Dashboard
</div>
```

페이지 그룹에 미들웨어를 지정하려면 `Folio::path` 메서드 호출 후 `middleware` 메서드를 체이닝하세요.

미들웨어를 적용할 페이지를 URL 패턴별로 지정하려면, 각 URL 패턴을 키로 하는 배열 형식으로 미들웨어를 지정할 수 있습니다. `*` 문자를 와일드카드로 사용할 수 있습니다:

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

배열에 클로저를 포함해 인라인 익명 미들웨어를 정의하는 것도 가능합니다:

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
## 라우트 캐싱 (Route Caching)

Folio를 사용할 때는 반드시 [Laravel의 라우트 캐싱 기능](/docs/11.x/routing#route-caching)을 활용해야 합니다. Folio는 `route:cache` Artisan 명령어 실행 시 Folio 페이지 정의와 라우트 이름을 최적의 성능을 위해 올바르게 캐싱할 수 있도록 처리합니다.