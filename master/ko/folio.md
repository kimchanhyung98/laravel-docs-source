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

[Laravel Folio](https://github.com/laravel/folio)는 라라벨 애플리케이션에서 라우팅을 간편하게 만들어주는 강력한 페이지 기반 라우터입니다. Laravel Folio를 사용하면, 루트 생성을 애플리케이션의 `resources/views/pages` 디렉터리 내에 Blade 템플릿을 생성하는 것만큼 쉽게 할 수 있습니다.

예를 들어, `/greeting` URL에서 접근 가능한 페이지를 만들고 싶다면, 애플리케이션의 `resources/views/pages` 디렉터리에 `greeting.blade.php` 파일을 생성하기만 하면 됩니다:

```php
<div>
    Hello World
</div>
```

<a name="installation"></a>
## 설치

시작하려면 Composer 패키지 매니저를 사용하여 Folio를 프로젝트에 설치하세요:

```shell
composer require laravel/folio
```

Folio를 설치한 후에는, `folio:install` 아티즌(Artisan) 명령어를 실행하여 Folio의 서비스 프로바이더를 애플리케이션에 설치할 수 있습니다. 이 서비스 프로바이더는 Folio가 라우트/페이지를 검색할 디렉터리를 등록합니다:

```shell
php artisan folio:install
```

<a name="page-paths-uris"></a>
### 페이지 경로 / URI

기본적으로 Folio는 애플리케이션의 `resources/views/pages` 디렉터리에서 페이지를 제공합니다. 그러나 Folio 서비스 프로바이더의 `boot` 메소드에서 이 디렉터리를 사용자 정의할 수 있습니다.

예를 들어, 경우에 따라 동일한 라라벨 애플리케이션에서 여러 개의 Folio 경로를 지정하는 것이 유용할 수 있습니다. 예를 들어, 애플리케이션의 "관리자(admin)" 영역에는 Folio 페이지를 별도의 디렉터리에 두고, 나머지 페이지는 또 다른 디렉터리에 둘 수 있습니다.

이는 `Folio::path`와 `Folio::uri` 메소드를 사용하여 설정할 수 있습니다. `path` 메소드는 Folio가 HTTP 요청을 라우팅할 때 페이지를 검색할 디렉터리를 등록하고, `uri` 메소드는 해당 페이지 디렉터리의 "기본 URI"를 지정합니다:

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

들어오는 요청의 서브도메인에 따라 페이지를 라우팅할 수도 있습니다. 예를 들어, `admin.example.com`에서 오는 요청을 Folio의 나머지 페이지들과는 다른 페이지 디렉터리로 라우팅하고 싶을 수 있습니다. 이는 `Folio::path` 메소드 호출 후 `domain` 메소드를 호출하여 설정할 수 있습니다:

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));
```

`domain` 메소드는 도메인 또는 서브도메인의 일부를 파라미터로 캡처할 수 있도록 해줍니다. 이렇게 캡처한 파라미터는 페이지 템플릿에 주입됩니다:

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));
```

<a name="creating-routes"></a>
## 라우트 생성

Folio 라우트는 Folio가 마운트한 디렉터리 중 하나에 Blade 템플릿을 추가하여 생성할 수 있습니다. 기본적으로 Folio는 `resources/views/pages` 디렉터리를 마운트하지만, Folio 서비스 프로바이더의 `boot` 메소드에서 디렉터리를 사용자 정의할 수 있습니다.

Blade 템플릿이 Folio 마운트 디렉터리에 추가되면 브라우저에서 즉시 접근이 가능합니다. 예를 들어, `pages/schedule.blade.php`에 생성된 페이지는 브라우저에서 `http://example.com/schedule`로 접근할 수 있습니다.

모든 Folio 페이지/라우트의 목록을 빠르게 확인하고 싶으면, `folio:list` 아티즌 명령어를 실행하세요:

```shell
php artisan folio:list
```

<a name="nested-routes"></a>
### 중첩 라우트

Folio 디렉터리 내에 하나 이상의 디렉터리를 생성하면 중첩 라우트를 만들 수 있습니다. 예를 들어, `/user/profile` 경로로 접근 가능한 페이지를 만들고 싶다면, `pages/user` 디렉터리 내에 `profile.blade.php` 템플릿을 생성하면 됩니다:

```shell
php artisan folio:page user/profile

# pages/user/profile.blade.php → /user/profile
```

<a name="index-routes"></a>
### 인덱스 라우트

때때로 특정 페이지를 디렉터리의 "인덱스"로 지정하고 싶을 수 있습니다. Folio 디렉터리 내에 `index.blade.php` 템플릿을 두면, 해당 디렉터리의 루트로 들어오는 요청이 이 페이지로 라우팅됩니다:

```shell
php artisan folio:page index
# pages/index.blade.php → /

php artisan folio:page users/index
# pages/users/index.blade.php → /users
```

<a name="route-parameters"></a>
## 라우트 파라미터

종종, 들어오는 요청의 URL 일부를 페이지로 주입받아 처리할 필요가 있습니다. 예를 들어, 프로필이 표시되고 있는 사용자의 "ID"에 접근해야 할 수도 있습니다. 이를 위해서는, 페이지 파일명 일부를 대괄호로 감싸면 됩니다:

```shell
php artisan folio:page "users/[id]"

# pages/users/[id].blade.php → /users/1
```

캡처된 세그먼트는 Blade 템플릿 내에서 변수로 사용할 수 있습니다:

```html
<div>
    User {{ $id }}
</div>
```

여러 세그먼트를 캡처하려면, 캡처 대상 앞에 점 세 개 `...`를 붙이면 됩니다:

```shell
php artisan folio:page "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3
```

여러 세그먼트를 캡처하면, 캡처된 세그먼트가 배열로 페이지에 주입됩니다:

```html
<ul>
    @foreach ($ids as $id)
        <li>User {{ $id }}</li>
    @endforeach
</ul>
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩

페이지 템플릿 파일 이름의 와일드카드 세그먼트가 애플리케이션의 Eloquent 모델 중 하나에 해당하면, Folio는 자동으로 라라벨의 라우트 모델 바인딩을 활용하여, 해당 모델 인스턴스를 해결해서 페이지에 주입하려고 시도합니다:

```shell
php artisan folio:page "users/[User]"

# pages/users/[User].blade.php → /users/1
```

캡처된 모델은 Blade 템플릿 내에서 변수로 접근할 수 있으며, 모델 변수 이름은 "카멜 케이스(camel case)"로 변환됩니다:

```html
<div>
    User {{ $user->id }}
</div>
```

#### 키 커스터마이징

경우에 따라, `id`가 아닌 다른 컬럼을 사용해 Eloquent 모델을 바인딩하고 싶을 수 있습니다. 그럴 때는, 파일명에 컬럼명을 지정하면 됩니다. 예를 들어, `[Post:slug].blade.php` 파일명은 `id` 컬럼 대신 `slug` 컬럼을 통해 모델을 해결합니다.

Windows 환경에서는 모델명과 키를 구분할 때 `-`를 사용하세요: `[Post-slug].blade.php`.

#### 모델 위치

기본적으로 Folio는 `app/Models` 디렉터리에서 모델을 검색합니다. 필요하다면, 템플릿 파일 이름에 전체 네임스페이스(fully-qualified) 모델 클래스명을 지정할 수 있습니다:

```shell
php artisan folio:page "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1
```

<a name="soft-deleted-models"></a>
### 소프트 삭제 모델

기본적으로, 소프트 삭제된(soft deleted) 모델은 암시적 모델 바인딩으로는 조회되지 않습니다. 그러나, 필요하다면 템플릿 내에서 `withTrashed` 함수를 호출하여 소프트 삭제된 모델도 Folio가 조회하도록 할 수 있습니다:

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

기본적으로 Folio는 들어오는 요청에 대해 페이지의 Blade 템플릿 내용을 응답으로 반환합니다. 하지만, 페이지 템플릿 내에서 `render` 함수를 호출하여 응답을 커스터마이징할 수 있습니다.

`render` 함수는 Folio가 렌더링 중인 `View` 인스턴스를 받는 클로저를 인자로 받아, 뷰에 추가 데이터를 전달하거나 전체 응답을 커스터마이징할 수 있습니다. 또, 뷰 인스턴스 외에도 라우트 파라미터 및 모델 바인딩 값이 클로저에 주입됩니다:

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

특정 페이지의 라우트에 이름을 지정하려면 `name` 함수를 사용하세요:

```php
<?php

use function Laravel\Folio\name;

name('users.index');
```

라라벨의 네임드 라우트와 같이, 이름이 지정된 Folio 페이지로 URL을 생성할 때 `route` 함수를 사용할 수 있습니다:

```php
<a href="{{ route('users.index') }}">
    All Users
</a>
```

페이지에 파라미터가 있는 경우, `route` 함수에 값을 전달하기만 하면 됩니다:

```php
route('users.show', ['user' => $user]);
```

<a name="middleware"></a>
## 미들웨어

특정 페이지에 미들웨어를 적용하려면, 페이지의 템플릿 내에서 `middleware` 함수를 호출하세요:

```php
<?php

use function Laravel\Folio\{middleware};

middleware(['auth', 'verified']);

?>

<div>
    Dashboard
</div>
```

또는, 여러 페이지에 미들웨어를 적용하려면 `Folio::path` 메소드 뒤에 `middleware` 메소드를 체이닝해서 사용할 수 있습니다.

어떤 페이지에 어떤 미들웨어를 적용할지 지정하려면, 미들웨어 배열의 키를 각각 적용할 페이지의 URL 패턴으로 지정해주세요. `*` 문자를 와일드카드 문자로 사용할 수 있습니다:

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

클로저를 사용해 인라인, 익명 미들웨어를 배열에 포함시킬 수 있습니다:

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

Folio를 사용할 때는 반드시 [라라벨의 라우트 캐싱 기능](/docs/{{version}}/routing#route-caching)을 활용해야 합니다. Folio는 최적의 성능을 위해, Folio 페이지 정의와 라우트 이름이 올바르게 캐시되도록 `route:cache` 아티즌 명령을 감지합니다.