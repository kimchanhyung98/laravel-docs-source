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
    - [소프트 삭제 모델](#soft-deleted-models)
- [렌더 후크](#render-hooks)
- [네임드 라우트](#named-routes)
- [미들웨어](#middleware)
- [라우트 캐싱](#route-caching)

<a name="introduction"></a>
## 소개

[Laravel Folio](https://github.com/laravel/folio)는 라라벨 애플리케이션에서 라우팅을 간편하게 만들어주는 강력한 페이지 기반 라우터입니다. Folio를 사용하면, 애플리케이션의 `resources/views/pages` 디렉터리에 Blade 템플릿 파일을 만드는 것만으로 라우트를 생성할 수 있습니다.

예를 들어 `/greeting` URL에서 접근할 수 있는 페이지를 생성하려면, 애플리케이션의 `resources/views/pages` 디렉터리에 `greeting.blade.php` 파일 하나만 생성하면 됩니다:

```php
<div>
    Hello World
</div>
```

<a name="installation"></a>
## 설치

먼저 Composer 패키지 매니저를 사용하여 Folio를 프로젝트에 설치하세요:

```bash
composer require laravel/folio
```

Folio 설치 후, `folio:install` Artisan 명령어를 실행하여 Folio의 서비스 프로바이더를 애플리케이션에 등록할 수 있습니다. 이 서비스 프로바이더는 Folio가 라우트 및 페이지를 탐색할 디렉터리를 등록합니다:

```bash
php artisan folio:install
```

<a name="page-paths-uris"></a>
### 페이지 경로 / URI

기본적으로 Folio는 애플리케이션의 `resources/views/pages` 디렉터리에서 페이지를 제공합니다. 하지만 Folio 서비스 프로바이더의 `boot` 메서드에서 이 경로를 자유롭게 커스터마이징할 수 있습니다.

예를 들어, 하나의 라라벨 애플리케이션에 여러 Folio 경로를 지정하고 싶을 수 있습니다. "admin" 영역을 위해 별도의 Folio 페이지 디렉터리를 사용하고, 나머지 페이지들은 다른 디렉터리를 사용할 수 있습니다.

이때 `Folio::path`와 `Folio::uri` 메서드를 사용할 수 있습니다. `path` 메서드는 Folio가 HTTP 요청을 라우팅할 때 페이지를 탐색할 디렉터리를 등록하고, `uri` 메서드는 해당 디렉터리의 "기준 URI"를 지정합니다:

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

요청의 서브도메인에 따라 특정 디렉터리의 페이지로 라우팅할 수도 있습니다. 예를 들어, `admin.example.com`의 요청을 Folio의 나머지 페이지들과 다른 디렉터리에서 분리하여 제공하고 싶을 때는 `Folio::path` 호출 후 `domain` 메서드를 사용할 수 있습니다:

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));
```

`domain` 메서드는 도메인이나 서브도메인의 일부를 파라미터로 캡처할 수도 있습니다. 이 파라미터는 페이지 템플릿에서 사용할 수 있습니다:

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));
```

<a name="creating-routes"></a>
## 라우트 생성

Folio 라우트는 Folio가 마운트된 디렉터리에 Blade 템플릿 파일을 추가함으로써 생성할 수 있습니다. 기본적으로 Folio는 `resources/views/pages` 디렉터리를 마운트하지만, 서비스 프로바이더에서 디렉터리를 변경할 수도 있습니다.

Folio 마운트 디렉터리에 Blade 템플릿을 두면, 즉시 브라우저에서 해당 페이지를 열 수 있습니다. 예를 들어, `pages/schedule.blade.php`에 추가된 페이지는 `http://example.com/schedule` 주소로 접근할 수 있습니다.

모든 Folio 페이지/라우트 목록을 빠르게 확인하려면, `folio:list` Artisan 명령어를 사용할 수 있습니다:

```bash
php artisan folio:list
```

<a name="nested-routes"></a>
### 중첩 라우트

Folio의 디렉터리 안에 하위 폴더를 만들어 중첩 라우트를 생성할 수 있습니다. 예를 들어 `/user/profile` 경로에서 접근 가능한 페이지를 만들려면, `pages/user` 디렉터리 내부에 `profile.blade.php` 템플릿을 생성하세요:

```bash
php artisan make:folio user/profile

# pages/user/profile.blade.php → /user/profile
```

<a name="index-routes"></a>
### 인덱스 라우트

특정 디렉터리의 "인덱스" 페이지로 지정하고 싶을 때, 해당 Folio 디렉터리에 `index.blade.php` 파일을 추가하면 해당 디렉터리의 루트 요청이 이 페이지로 라우팅됩니다:

```bash
php artisan make:folio index
# pages/index.blade.php → /

php artisan make:folio users/index
# pages/users/index.blade.php → /users
```

<a name="route-parameters"></a>
## 라우트 파라미터

종종 요청된 URL의 일부 세그먼트를 페이지 내부에서 변수로 사용해야 할 때가 있습니다. 예를 들면, 한 사용자의 프로필을 표시할 때 그 "ID"를 받아와야 할 수 있습니다. 이를 위해 파일명 일부를 대괄호로 감싸 파라미터로 캡처할 수 있습니다:

```bash
php artisan make:folio "users/[id]"

# pages/users/[id].blade.php → /users/1
```

캡처된 세그먼트는 Blade 템플릿 안에서 변수로 바로 사용할 수 있습니다:

```html
<div>
    User {{ $id }}
</div>
```

복수의 세그먼트를 캡처하려면, 대괄호 부분 앞에 ...를 붙입니다:

```bash
php artisan make:folio "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3
```

여러 세그먼트를 캡처하면 배열로 페이지에 주입됩니다:

```html
<ul>
    @foreach ($ids as $id)
        <li>User {{ $id }}</li>
    @endforeach
</ul>
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩

페이지 템플릿 파일의 와일드카드 부분이 애플리케이션의 Eloquent 모델과 이름이 일치하면, Folio는 라라벨의 라우트 모델 바인딩 기능을 자동으로 활용하여 해당 모델 인스턴스를 페이지에 주입합니다:

```bash
php artisan make:folio "users/[User]"

# pages/users/[User].blade.php → /users/1
```

캡처된 모델은 Blade 템플릿에서 변수로 접근 가능합니다. 변수명은 "카멜 케이스"로 변환됩니다:

```html
<div>
    User {{ $user->id }}
</div>
```

#### 바인딩 키 커스터마이즈

때로는 Eloquent 모델을 기본값인 `id` 컬럼이 아닌, 다른 컬럼으로 바인딩하여 찾고 싶을 수 있습니다. 이 경우 파일명에 컬럼명을 명시할 수 있습니다. 예를 들면, `[Post:slug].blade.php` 파일은 `id` 대신 `slug` 컬럼으로 모델 인스턴스를 찾습니다.

Windows 환경에서는 모델명과 키를 연결할 때 `-`를 사용하세요: `[Post-slug].blade.php`.

#### 모델 위치 지정

기본적으로 Folio는 애플리케이션의 `app/Models` 디렉터리 내에서 모델을 탐색합니다. 파일명에 모델의 전체 네임스페이스를 명시하여 위치를 지정할 수도 있습니다:

```bash
php artisan make:folio "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1
```

<a name="soft-deleted-models"></a>
### 소프트 삭제 모델

기본적으로 소프트 삭제된 모델은 암시적 모델 바인딩 시 검색되지 않습니다. 하지만 필요하다면, 페이지 템플릿 내에서 `withTrashed` 함수를 호출하여 소프트 삭제 모델까지 바인딩되도록 할 수 있습니다:

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
## 렌더 후크

기본적으로 Folio는 페이지 Blade 템플릿의 내용을 HTTP 응답으로 반환합니다. 하지만 템플릿 내에서 `render` 함수를 호출해 응답을 직접 커스터마이징할 수도 있습니다.

`render` 함수는 클로저를 인수로 받아 Folio가 렌더하는 `View` 인스턴스를 전달합니다. 이를 통해 뷰 데이터 추가 또는 전체 응답을 원하는 대로 조작할 수 있습니다. 추가로, 라우트 파라미터나 모델 바인딩 값도 함께 클로저에 주입됩니다:

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

특정 페이지의 라우트에 이름을 지정하려면 `name` 함수를 사용합니다:

```php
<?php

use function Laravel\Folio\name;

name('users.index');
```

라라벨의 네임드 라우트와 마찬가지로, `route` 함수를 사용하여 해당 이름이 부여된 Folio 페이지의 URL을 생성할 수 있습니다:

```php
<a href="{{ route('users.index') }}">
    All Users
</a>
```

페이지에 파라미터가 있다면 값을 배열로 간단하게 `route` 함수에 전달하세요:

```php
route('users.show', ['user' => $user]);
```

<a name="middleware"></a>
## 미들웨어

특정 페이지에 미들웨어를 적용하려면 해당 페이지의 템플릿 내에서 `middleware` 함수를 호출하세요:

```php
<?php

use function Laravel\Folio\{middleware};

middleware(['auth', 'verified']);

?>

<div>
    Dashboard
</div>
```

또는, 여러 페이지에 미들웨어를 일괄 적용하려면 `Folio::path` 호출 후 `middleware` 메서드를 체이닝할 수 있습니다.

미들웨어가 적용되어야 할 페이지를 지정하려면, 미들웨어 배열의 키로 URL 패턴을 사용할 수 있습니다. `*`는 와일드카드로 동작합니다:

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

익명 미들웨어를 직접 정의하려면, 미들웨어 배열 안에 클로저를 추가할 수도 있습니다:

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

Folio를 사용할 때는 반드시 [라라벨의 라우트 캐싱 기능](/docs/{{version}}/routing#route-caching)을 활용해야 합니다. Folio는 `route:cache` Artisan 명령어를 감지하여, Folio 페이지 정의와 라우트 네임이 최대 성능으로 캐싱되도록 보장합니다.