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
- [렌더 후크](#render-hooks)
- [네임드 라우트](#named-routes)
- [미들웨어](#middleware)
- [라우트 캐싱](#route-caching)

<a name="introduction"></a>
## 소개

[Laravel Folio](https://github.com/laravel/folio)는 Laravel 애플리케이션에서 라우팅을 간편하게 만들어주는 강력한 페이지 기반 라우터입니다. Laravel Folio를 사용하면, 라우트를 생성하는 일이 애플리케이션의 `resources/views/pages` 디렉터리에 Blade 템플릿을 생성하는 것만큼 쉬워집니다.

예를 들어, `/greeting` URL로 접근 가능한 페이지를 생성하려면, 애플리케이션의 `resources/views/pages` 디렉터리에 `greeting.blade.php` 파일을 만들면 됩니다:

```php
<div>
    Hello World
</div>
```

<a name="installation"></a>
## 설치

먼저 Composer 패키지 매니저를 사용하여 프로젝트에 Folio를 설치하세요:

```bash
composer require laravel/folio
```

Folio 설치가 완료되면, `folio:install` Artisan 명령어를 실행할 수 있습니다. 이 명령은 Folio의 서비스 프로바이더를 애플리케이션에 설치하며, 이 서비스 프로바이더는 Folio가 라우트/페이지를 검색할 디렉터리를 등록합니다:

```bash
php artisan folio:install
```

<a name="page-paths-uris"></a>
### 페이지 경로 / URI

기본적으로 Folio는 애플리케이션의 `resources/views/pages` 디렉터리에서 페이지를 제공하지만, 서비스 프로바이더의 `boot` 메서드에서 이 디렉터리를 커스터마이징할 수 있습니다.

예를 들어, 하나의 Laravel 애플리케이션에서 여러 Folio 경로를 명시하는 것이 편리할 때도 있습니다. 애플리케이션의 "admin" 영역을 위한 별도의 Folio 페이지 디렉터리를 두고, 나머지 페이지는 다른 디렉터리를 사용할 수 있습니다.

이렇게 하려면 `Folio::path`와 `Folio::uri` 메서드를 사용할 수 있습니다. `path` 메서드는 Folio가 들어오는 HTTP 요청을 라우팅할 때 페이지를 스캔할 디렉터리를 등록하고, `uri` 메서드는 해당 디렉터리의 "베이스 URI"를 지정합니다:

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

들어오는 요청의 서브도메인에 따라 페이지를 라우팅할 수도 있습니다. 예를 들어, `admin.example.com`에서의 요청을 Folio의 다른 페이지 디렉터리로 라우팅하고 싶을 수 있습니다. 이를 위해 `Folio::path` 메서드 호출 후 `domain` 메서드를 호출하세요:

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));
```

`domain` 메서드를 사용하면 도메인 또는 서브도메인의 일부를 파라미터로 캡처할 수도 있습니다. 캡처된 파라미터는 페이지 템플릿에 주입됩니다:

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));
```

<a name="creating-routes"></a>
## 라우트 생성

Folio 라우트는 Folio가 마운트한 디렉터리 중 하나에 Blade 템플릿을 배치함으로써 생성할 수 있습니다. Folio는 기본적으로 `resources/views/pages` 디렉터리를 마운트하지만, 서비스 프로바이더의 `boot` 메서드에서 이 디렉터리를 변경할 수 있습니다.

Folio가 마운트한 디렉터리에 Blade 템플릿을 배치하면, 브라우저에서 즉시 접근할 수 있습니다. 예를 들어, `pages/schedule.blade.php`에 페이지를 배치하면 브라우저에서 `http://example.com/schedule`로 접근할 수 있습니다.

모든 Folio 페이지/라우트 목록을 빠르게 보려면 `folio:list` Artisan 명령어를 실행하세요:

```bash
php artisan folio:list
```

<a name="nested-routes"></a>
### 중첩 라우트

Folio 디렉터리 내에 하위 디렉터리를 생성함으로써 중첩 라우트를 만들 수 있습니다. 예를 들어, `/user/profile`로 접근 가능한 페이지를 만들려면, `pages/user` 디렉터리에 `profile.blade.php` 템플릿을 생성합니다:

```bash
php artisan folio:page user/profile

# pages/user/profile.blade.php → /user/profile
```

<a name="index-routes"></a>
### 인덱스 라우트

특정 페이지를 디렉터리의 "인덱스"로 지정하고 싶을 때가 있습니다. Folio 디렉터리에 `index.blade.php`를 배치하면, 해당 디렉터리의 루트로 들어오는 모든 요청이 그 페이지로 라우팅됩니다:

```bash
php artisan folio:page index
# pages/index.blade.php → /

php artisan folio:page users/index
# pages/users/index.blade.php → /users
```

<a name="route-parameters"></a>
## 라우트 파라미터

URL의 일부를 페이지로 주입받아 활용해야 하는 경우가 많습니다. 예를 들어, 특정 사용자 프로필을 표시하기 위해 사용자의 "ID"에 접근해야 할 수 있습니다. 이를 위해서는 페이지 파일 이름의 일부분을 대괄호로 감싸세요:

```bash
php artisan folio:page "users/[id]"

# pages/users/[id].blade.php → /users/1
```

캡처된 파라미터는 Blade 템플릿 내에서 변수로 사용할 수 있습니다:

```html
<div>
    User {{ $id }}
</div>
```

여러 세그먼트를 캡처하려면, 대괄호 앞에 점 세 개 `...`를 붙이세요:

```bash
php artisan folio:page "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3
```

여러 세그먼트를 캡처하면, 배열로 변수에 주입됩니다:

```html
<ul>
    @foreach ($ids as $id)
        <li>User {{ $id }}</li>
    @endforeach
</ul>
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩

페이지 템플릿 파일 이름의 와일드카드 세그먼트가 애플리케이션의 Eloquent 모델과 일치하면, Folio는 자동으로 Laravel의 라우트 모델 바인딩 기능을 사용하여 해결된 모델 인스턴스를 페이지로 주입합니다:

```bash
php artisan folio:page "users/[User]"

# pages/users/[User].blade.php → /users/1
```

캡처된 모델은 Blade 템플릿 내에서 변수로 사용할 수 있습니다. 모델 변수 이름은 "카멜 케이스"로 변환됩니다:

```html
<div>
    User {{ $user->id }}
</div>
```

#### 키 커스터마이징

때로는 Eloquent 모델을 `id`가 아닌 다른 컬럼을 사용해 바인딩하고 싶을 수 있습니다. 이럴 때는 페이지 파일 이름에서 컬럼을 지정할 수 있습니다. 예를 들어, `[Post:slug].blade.php` 파일은 바인딩 시 `id` 대신 `slug` 컬럼을 사용합니다.

Windows 환경에서는 모델 이름과 키를 `-`로 구분하세요: `[Post-slug].blade.php`.

#### 모델 위치

기본적으로 Folio는 애플리케이션의 `app/Models` 디렉터리에서 모델을 찾습니다. 하지만 필요한 경우, 페이지 파일 이름에서 완전한 클래스명을 명시할 수 있습니다:

```bash
php artisan folio:page "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1
```

<a name="soft-deleted-models"></a>
### 소프트 삭제된 모델

기본적으로 소프트 삭제된(soft deleted) 모델은 암시적 모델 바인딩 시 조회되지 않습니다. 그러나 필요하다면, 페이지 템플릿 내에서 `withTrashed` 함수를 호출하여 소프트 삭제된 모델까지 조회하도록 Folio에 지시할 수 있습니다:

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

기본적으로 Folio는 페이지의 Blade 템플릿 내용을 들어오는 요청에 대한 응답으로 반환합니다. 그러나 페이지 템플릿 내에서 `render` 함수를 호출하여 응답을 커스터마이즈할 수도 있습니다.

`render` 함수는 Folio가 렌더링하는 `View` 인스턴스를 받는 클로저를 인자로 받으며, 이를 통해 뷰에 추가 데이터를 전달하거나 응답 전체를 커스터마이즈할 수 있습니다. 추가로, 라우트 파라미터나 모델 바인딩 값들도 `render` 클로저에 함께 전달됩니다:

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
    이 작성자는 {{ count($photos) }}장의 사진도 가지고 있습니다.
</div>
```

<a name="named-routes"></a>
## 네임드 라우트

`name` 함수를 사용해 특정 페이지 라우트에 이름을 할당할 수 있습니다:

```php
<?php

use function Laravel\Folio\name;

name('users.index');
```

Laravel 네임드 라우트와 마찬가지로, `route` 함수를 통해 이름이 지정된 Folio 페이지로 가는 URL을 생성할 수 있습니다:

```php
<a href="{{ route('users.index') }}">
    All Users
</a>
```

페이지에 파라미터가 있다면, 그 값을 `route` 함수에 전달하면 됩니다:

```php
route('users.show', ['user' => $user]);
```

<a name="middleware"></a>
## 미들웨어

페이지 템플릿 내에서 `middleware` 함수를 호출하여 특정 페이지에 미들웨어를 적용할 수 있습니다:

```php
<?php

use function Laravel\Folio\{middleware};

middleware(['auth', 'verified']);

?>

<div>
    Dashboard
</div>
```

또는 여러 페이지에 미들웨어를 적용하고 싶다면, `Folio::path` 호출 후 `middleware` 메서드를 체이닝하면 됩니다.

미들웨어가 적용될 페이지를 지정하려면, 미들웨어의 배열에 해당하는 URL 패턴을 키로 사용하세요. `*` 문자는 와일드카드로 사용할 수 있습니다:

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

배열에 클로저를 포함시켜 인라인 익명 미들웨어도 정의할 수 있습니다:

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

Folio를 사용하는 경우, [Laravel의 라우트 캐싱 기능](/docs/{{version}}/routing#route-caching)을 반드시 적극적으로 활용하는 것이 좋습니다. Folio는 `route:cache` Artisan 명령어를 감지하여 Folio의 페이지 정의와 라우트 이름이 최대한 성능을 발휘할 수 있도록 올바르게 캐싱되도록 보장합니다.