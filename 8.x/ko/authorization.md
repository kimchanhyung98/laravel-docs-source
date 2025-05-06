# 인가(Authorization)

- [소개](#introduction)
- [게이트(Gates)](#gates)
    - [게이트 작성하기](#writing-gates)
    - [게이트를 통한 액션 인가](#authorizing-actions-via-gates)
    - [게이트 응답](#gate-responses)
    - [게이트 검사 가로채기](#intercepting-gate-checks)
    - [인라인 인가](#inline-authorization)
- [정책(Policies) 생성하기](#creating-policies)
    - [정책 생성](#generating-policies)
    - [정책 등록](#registering-policies)
- [정책 작성하기](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델이 없는 메서드](#methods-without-models)
    - [게스트 사용자](#guest-users)
    - [정책 필터](#policy-filters)
- [정책을 이용한 액션 인가](#authorizing-actions-using-policies)
    - [User 모델을 통한 인가](#via-the-user-model)
    - [컨트롤러 헬퍼를 통한 인가](#via-controller-helpers)
    - [미들웨어를 통한 인가](#via-middleware)
    - [Blade 템플릿을 통한 인가](#via-blade-templates)
    - [추가 컨텍스트 전달하기](#supplying-additional-context)

<a name="introduction"></a>
## 소개

Laravel은 기본적으로 내장된 [인증](/docs/{{version}}/authentication) 서비스 외에도, 주어진 리소스에 대해 사용자의 액션을 인가할 수 있는 간단한 방법을 제공합니다. 예를 들어, 사용자가 인증되었더라도, 해당 사용자가 애플리케이션이 관리하는 특정 Eloquent 모델이나 데이터베이스 레코드를 수정하거나 삭제할 권한이 없을 수 있습니다. Laravel의 인가 기능은 이러한 인가 검사를 쉽고 조직적으로 관리할 수 있는 방법을 제공합니다.

Laravel은 두 가지 주요 인가 방법을 제공합니다: [게이트(Gates)](#gates)와 [정책(Policies)](#creating-policies). 게이트와 정책은 라우트와 컨트롤러의 관계와 유사하게 동작합니다. 게이트는 클로저 기반의 간단한 인가 방식을 제공하고, 정책은 컨트롤러처럼 특정 모델이나 리소스 중심으로 인가 로직을 그룹화합니다. 이 문서에서는 먼저 게이트를 살펴보고, 이후에 정책을 살펴봅니다.

애플리케이션을 개발할 때 반드시 게이트만 쓰거나 정책만 써야 하는 것은 아닙니다. 대부분의 애플리케이션은 게이트와 정책을 혼합하여 사용합니다. 게이트는 모델이나 리소스에 직접적으로 연결되어 있지 않은 액션(예: 관리 대시보드 보기)에 알맞고, 정책은 특정 모델이나 리소스에 대한 액션을 인가할 때 사용해야 합니다.

<a name="gates"></a>
## 게이트(Gates)

<a name="writing-gates"></a>
### 게이트 작성하기

> {note} 게이트는 Laravel의 인가 특징의 기본 개념을 배우기에 좋은 방법입니다. 그러나 더욱 견고한 애플리케이션을 개발할 때는 인가 규칙을 [정책](#creating-policies)으로 정리하는 것을 권장합니다.

게이트는 사용자의 액션 인가 여부를 판단하는 클로저입니다. 일반적으로 게이트는 `App\Providers\AuthServiceProvider`의 `boot` 메서드 내에서 `Gate` 퍼사드를 이용해 정의합니다. 게이트는 항상 유저 인스턴스를 첫 번째 인자로 받고, 추가로 관련 Eloquent 모델 등 다른 인자를 받을 수 있습니다.

예를 들어, 특정 `App\Models\Post` 모델을 사용자가 수정할 수 있는지 결정하는 게이트를 다음과 같이 정의할 수 있습니다. 게이트에서는 사용자의 `id`와 게시글 작성자의 `user_id`를 비교합니다.

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * 인증/인가 서비스 등록
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Gate::define('update-post', function (User $user, Post $post) {
        return $user->id === $post->user_id;
    });
}
```

컨트롤러처럼 게이트도 클래스 콜백 배열로 정의할 수 있습니다.

```php
use App\Policies\PostPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * 인증/인가 서비스 등록
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Gate::define('update-post', [PostPolicy::class, 'update']);
}
```

<a name="authorizing-actions-via-gates"></a>
### 게이트를 통한 액션 인가

게이트를 사용해 액션을 인가하려면, `Gate` 퍼사드의 `allows` 또는 `denies` 메서드를 사용하면 됩니다. 이때 현재 인증된 사용자를 따로 전달할 필요는 없습니다. Laravel이 자동으로 사용자 인스턴스를 게이트 클로저에 전달합니다. 일반적으로 컨트롤러에서 인가가 필요한 액션 전에 게이트 인가 메서드를 호출합니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class PostController extends Controller
{
    /**
     * 게시글 수정
     *
     * @param  \Illuminate\Http\Request $request
     * @param  \App\Models\Post $post
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Post $post)
    {
        if (! Gate::allows('update-post', $post)) {
            abort(403);
        }

        // 게시글 수정 처리...
    }
}
```

현재 인증된 사용자 이외의 다른 사용자가 특정 액션 수행 권한이 있는지 확인하려면, `Gate` 퍼사드의 `forUser` 메서드를 사용할 수 있습니다.

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // 해당 사용자는 게시글을 수정할 수 있습니다.
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // 해당 사용자는 게시글을 수정할 수 없습니다.
}
```

`any` 또는 `none` 메서드를 사용해 여러 액션을 한 번에 인가할 수도 있습니다.

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // 사용자가 게시글을 수정 또는 삭제할 수 있습니다.
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // 사용자가 게시글을 수정 또는 삭제할 수 없습니다.
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 인가 검사 및 예외 발생

액션 인가를 시도하고, 허용되지 않을 경우 자동으로 `Illuminate\Auth\Access\AuthorizationException`을 throw하고 싶다면, `Gate` 퍼사드의 `authorize` 메서드를 사용할 수 있습니다. 이 예외는 Laravel 예외 핸들러에 의해 403 HTTP 응답으로 자동 변환됩니다.

```php
Gate::authorize('update-post', $post);

// 액션이 인가됨...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 전달하기

인가 메서드(`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`)와 [Blade 디렉티브](#via-blade-templates) (`@can`, `@cannot`, `@canany`)는 두 번째 인자로 배열을 받을 수 있습니다. 배열 요소들은 게이트 클로저의 추가 파라미터로 전달되어, 인가 결정 시 추가 정보를 사용할 수 있습니다.

```php
use App\Models\Category;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::define('create-post', function (User $user, Category $category, $pinned) {
    if (! $user->canPublishToGroup($category->group)) {
        return false;
    } elseif ($pinned && ! $user->canPinPosts()) {
        return false;
    }

    return true;
});

if (Gate::check('create-post', [$category, $pinned])) {
    // 사용자가 게시글을 생성할 수 있습니다.
}
```

<a name="gate-responses"></a>
### 게이트 응답

지금까지는 간단하게 불리언 값을 반환하는 게이트만 살펴봤습니다. 하지만 더 상세한 응답(예: 에러 메시지)이 필요할 때, 게이트에서 `Illuminate\Auth\Access\Response`를 반환할 수 있습니다.

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
                ? Response::allow()
                : Response::deny('관리자여야 합니다.');
});
```

게이트에서 인가 응답을 반환하더라도, `Gate::allows`는 여전히 단순히 불리언 값만 반환합니다. 하지만, `Gate::inspect` 메서드를 사용하면 전체 인가 응답을 받을 수 있습니다.

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // 액션 인가됨...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드(인가되지 않으면 예외를 throw함)를 쓸 때, 게이트 응답의 에러 메시지는 HTTP 응답으로 전달됩니다.

```php
Gate::authorize('edit-settings');

// 액션 인가됨...
```

<a name="intercepting-gate-checks"></a>
### 게이트 검사 가로채기

특정 사용자에게 모든 권한을 부여하고 싶을 때가 있습니다. 이럴 때 `before` 메서드를 사용해, 다른 모든 인가 검사 전에 실행되는 클로저를 정의할 수 있습니다.

```php
use Illuminate\Support\Facades\Gate;

Gate::before(function ($user, $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저가 null이 아닌 값을 반환하면, 그 값이 인가 검사에 사용됩니다.

모든 검사 이후에 실행되는 `after` 메서드도 사용할 수 있습니다.

```php
Gate::after(function ($user, $ability, $result, $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after` 클로저 역시 null이 아닌 값을 반환하면, 그 결과가 검사 결과가 됩니다.

<a name="inline-authorization"></a>
### 인라인 인가

가끔, 별도의 게이트를 작성하지 않고도, 현재 인증된 사용자가 특정 액션을 할 수 있는지 바로 확인하고 싶을 수 있습니다. 이 경우 `Gate::allowIf`와 `Gate::denyIf` 메서드로 "인라인" 인가 검사를 할 수 있습니다.

```php
use Illuminate\Support\Facades\Auth;

Gate::allowIf(fn ($user) => $user->isAdministrator());

Gate::denyIf(fn ($user) => $user->banned());
```

액션이 인가되지 않거나 인증된 사용자가 없으면, Laravel은 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 throw합니다. 이 예외는 403 응답으로 변환됩니다.

<a name="creating-policies"></a>
## 정책(Policies) 생성하기

<a name="generating-policies"></a>
### 정책 생성

정책(Policy)은 특정 모델이나 리소스에 대한 인가 로직을 정리하는 클래스입니다. 예를 들어, 블로그 애플리케이션에서 `App\Models\Post` 모델에 대해 사용자 액션(생성, 수정 등)을 인가하는 `App\Policies\PostPolicy`가 있을 수 있습니다.

정책은 Artisan 명령어 `make:policy`로 생성할 수 있으며, 기본적으로 `app/Policies` 디렉터리에 생성됩니다. 디렉터리가 없다면 자동으로 생성됩니다.

```bash
php artisan make:policy PostPolicy
```

기본적으로 비어있는 클래스가 생성되며, `--model` 옵션을 주면 리소스의 조회, 생성, 수정, 삭제 관련 예시 메서드를 포함한 클래스를 생성할 수 있습니다.

```bash
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록

정책 클래스를 생성한 후에는 등록해야 합니다. 정책 등록은 Laravel에 어떤 모델에 어떤 정책을 쓸지 알려주는 절차입니다.

Laravel 기본 `App\Providers\AuthServiceProvider`에는 Eloquent 모델과 정책 클래스를 매핑하는 `policies` 프로퍼티가 있습니다. 정책을 등록하면, 해당 Eloquent 모델의 인가시 어떤 정책을 사용할지 Laravel이 인식하게 됩니다.

```php
<?php

namespace App\Providers;

use App\Models\Post;
use App\Policies\PostPolicy;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Gate;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션의 정책 매핑
     *
     * @var array
     */
    protected $policies = [
        Post::class => PostPolicy::class,
    ];

    /**
     * 인증/인가 서비스 등록
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        //
    }
}
```

<a name="policy-auto-discovery"></a>
#### 정책 자동 발견

모델 정책을 일일이 등록하지 않고도, Laravel이 표준 네이밍 컨벤션을 지키는 한 자동으로 정책을 찾아줍니다. 구체적으로, 정책은 모델이 위치한 디렉터리의 상위 혹은 같은 위치의 `Policies` 디렉터리에 있어야 하며, 정책 클래스명은 모델명+`Policy`이어야 합니다.

예를 들어 모델이 `app/Models`에 있고, 정책이 `app/Policies`에 있다면, `User` 모델은 `UserPolicy` 정책 클래스와 자동으로 매치됩니다.

정책 자동 발굴 방식을 직접 지정하고 싶을 때는, `Gate::guessPolicyNamesUsing` 메서드로 커스텀 콜백을 등록할 수 있습니다. 일반적으로 `AuthServiceProvider`의 `boot` 메서드에 작성합니다.

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function ($modelClass) {
    // 주어진 모델에 대한 정책 클래스명 반환...
});
```

> {note} `AuthServiceProvider`에 명시적으로 매핑된 정책이 있으면, 자동 발견 정책보다 우선합니다.

<a name="writing-policies"></a>
## 정책 작성하기

<a name="policy-methods"></a>
### 정책 메서드

정책 클래스를 등록한 후, 인가할 액션별로 메서드를 추가할 수 있습니다. 예를 들어, 특정 `App\Models\User`가 특정 `App\Models\Post`를 수정할 수 있는지 판단하는 `update` 메서드를 정의할 수 있습니다.

`update` 메서드는 `User`와 `Post` 인스턴스를 인자로 받아, 수정 권한이 있는지 불리언 형태로 반환해야 합니다. 아래 예시에서는 사용자의 `id`와 게시글의 `user_id`가 같은지 확인합니다.

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 사용자가 해당 게시글을 수정할 수 있는지 결정
     *
     * @param  \App\Models\User  $user
     * @param  \App\Models\Post  $post
     * @return bool
     */
    public function update(User $user, Post $post)
    {
        return $user->id === $post->user_id;
    }
}
```

정책에서는 필요에 따라 추가 메서드(`view`, `delete` 등)를 정의할 수 있습니다. 메서드 명은 자유롭게 정할 수 있습니다.

아티즌에서 정책 생성 시 `--model` 옵션을 사용하면, 이미 `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 액션에 대한 메서드가 포함되어 생성됩니다.

> {tip} 모든 정책은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석됩니다. 따라서, 정책의 생성자에 의존성을 타입힌트하면 자동으로 주입됩니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지는 정책 메서드에서 불리언 값만 반환했습니다. 더 상세한 응답(에러 메시지 등)이 필요하다면, `Illuminate\Auth\Access\Response` 인스턴스를 반환하면 됩니다.

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 사용자가 게시글을 수정할 수 있는지 판단
 *
 * @param  \App\Models\User  $user
 * @param  \App\Models\Post  $post
 * @return \Illuminate\Auth\Access\Response
 */
public function update(User $user, Post $post)
{
    return $user->id === $post->user_id
                ? Response::allow()
                : Response::deny('해당 게시글의 소유자가 아닙니다.');
}
```

정책에서 인가 응답을 반환해도, `Gate::allows`는 여전히 불리언만 반환합니다. 전체 응답을 받고 싶으면, `Gate::inspect`를 사용하면 됩니다.

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // 액션 인가됨...
} else {
    echo $response->message();
}
```

`Gate::authorize`로 인가하지 않으면 예외를 throw하며, 에러 메시지는 HTTP 응답에 전달됩니다.

```php
Gate::authorize('update', $post);

// 액션 인가됨...
```

<a name="methods-without-models"></a>
### 모델이 없는 메서드

특정 정책 메서드는 인증된 사용자 인스턴스만 받는 경우도 있습니다. 주로 `create` 액션(예: 글 생성 가능 여부)에서 사용됩니다.

```php
/**
 * 사용자가 게시글을 생성할 수 있는지 판단
 *
 * @param  \App\Models\User $user
 * @return bool
 */
public function create(User $user)
{
    return $user->role == 'writer';
}
```

<a name="guest-users"></a>
### 게스트 사용자

기본적으로 인증되지 않은 사용자의 HTTP 요청에 대해 모든 게이트와 정책은 자동으로 `false`를 반환합니다. 그러나 게이트/정책의 사용자 인자에 "옵셔널" 타입힌트나 `null` 기본값을 지정하면, 게스트 사용자도 인가 검사가 통과되도록 할 수 있습니다.

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 사용자가 게시글을 수정할 수 있는지 판단
     *
     * @param  \App\Models\User|null $user
     * @param  \App\Models\Post $post
     * @return bool
     */
    public function update(?User $user, Post $post)
    {
        return optional($user)->id === $post->user_id;
    }
}
```

<a name="policy-filters"></a>
### 정책 필터

특정 사용자에게 정책 내 모든 액션을 인가하고 싶을 때는, 정책에 `before` 메서드를 정의하면 됩니다. 이 메서드는 정책의 다른 어떤 메서드보다 먼저 실행되므로, 정책의 각 메서드가 호출되기 전에 인가를 처리할 수 있습니다. 주로 관리자가 모든 액션을 수행할 수 있게 할 때 사용됩니다.

```php
use App\Models\User;

/**
 * 사전 인가 검사
 *
 * @param  \App\Models\User $user
 * @param  string $ability
 * @return void|bool
 */
public function before(User $user, $ability)
{
    if ($user->isAdministrator()) {
        return true;
    }
}
```

특정 사용자 유형에게 모든 인가 검사를 거부하려면, `before`에서 `false`를 반환하면 됩니다. `null`을 반환하면 정상적으로 본래 정책 메서드가 실행됩니다.

> {note} 정책 클래스에 해당 액션이름의 메서드가 없으면, `before`가 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 이용한 액션 인가

<a name="via-the-user-model"></a>
### User 모델을 통한 인가

Laravel의 `App\Models\User` 모델에는 인가에 유용한 두 가지 메서드(`can`, `cannot`)가 있습니다. 이 메서드들은 인가하려는 액션명과 모델 인스턴스를 받습니다. 예를 들어, 사용자가 특정 게시글을 업데이트할 권한이 있는지 확인하려면, 보통 컨트롤러 메서드에서 다음과 같이 합니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 게시글 수정
     *
     * @param \Illuminate\Http\Request $request
     * @param \App\Models\Post $post
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Post $post)
    {
        if ($request->user()->cannot('update', $post)) {
            abort(403);
        }

        // 게시글 수정 처리...
    }
}
```

[정책이 등록](#registering-policies)되어 있다면, `can` 메서드는 해당 정책의 메서드를 자동으로 호출해서 결과를 반환합니다. 정책이 없으면, 액션 이름에 매치되는 클로저 기반 게이트를 호출하게 됩니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 액션

`create`와 같이 모델 인스턴스가 필요 없는 일부 액션의 경우, 클래스명을 `can` 메서드에 전달하면 됩니다. 이 클래스명으로 어떤 정책을 사용할지 결정합니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 게시글 생성
     *
     * @param \Illuminate\Http\Request $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        if ($request->user()->cannot('create', Post::class)) {
            abort(403);
        }

        // 게시글 생성 처리...
    }
}
```

<a name="via-controller-helpers"></a>
### 컨트롤러 헬퍼를 통한 인가

User 모델의 인가 메서드 외에도, 모든 컨트롤러(기본적으로 `App\Http\Controllers\Controller`를 상속)에 `authorize` 메서드가 제공됩니다.

이 메서드는 인가 액션명과 모델 인스턴스를 받아들여, 인가되지 않으면 `Illuminate\Auth\Access\AuthorizationException`을 throw합니다. 이 예외는 Laravel에서 자동으로 403 HTTP 응답으로 변환됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 블로그 게시글 수정
     *
     * @param \Illuminate\Http\Request $request
     * @param \App\Models\Post $post
     * @return \Illuminate\Http\Response
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post)
    {
        $this->authorize('update', $post);

        // 수정 가능...
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

이미 설명한 것처럼, `create` 등 일부 정책 메서드는 모델 인스턴스가 필요 없습니다. 이때는 클래스명을 `authorize` 메서드에 전달합니다.

```php
use App\Models\Post;
use Illuminate\Http\Request;

/**
 * 블로그 게시글 생성
 *
 * @param \Illuminate\Http\Request $request
 * @return \Illuminate\Http\Response
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request)
{
    $this->authorize('create', Post::class);

    // 블로그 게시글 생성 가능...
}
```

<a name="authorizing-resource-controllers"></a>
#### 리소스 컨트롤러의 인가

[리소스 컨트롤러](/docs/{{version}}/controllers#resource-controllers)를 사용할 때 컨트롤러의 생성자에서 `authorizeResource` 메서드를 활용할 수 있습니다. 이 메서드는 해당 액션에 대한 적절한 `can` 미들웨어를 컨트롤러 메서드에 자동으로 부착합니다.

`authorizeResource`는 첫 번째 인자로 모델의 클래스명, 두 번째 인자로 라우트/요청 파라미터(모델 ID가 담기는 이름)를 받습니다. [리소스 컨트롤러](/docs/{{version}}/controllers#resource-controllers)는 `--model` 플래그로 생성하는 것이 좋습니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 컨트롤러 인스턴스 생성자
     *
     * @return void
     */
    public function __construct()
    {
        $this->authorizeResource(Post::class, 'post');
    }
}
```

아래 컨트롤러 메서드와 정책 메서드가 자동으로 매핑됩니다. 해당 컨트롤러 메서드로 라우팅되면, 먼저 관련 정책 메서드가 인가를 검사합니다.

| 컨트롤러 메서드 | 정책 메서드    |
| -------------- | -------------- |
| index          | viewAny        |
| show           | view           |
| create         | create         |
| store          | create         |
| edit           | update         |
| update         | update         |
| destroy        | delete         |

> {tip} `make:policy` 명령어에 `--model` 옵션을 사용하면, 해당 모델에 대한 정책 클래스를 빠르게 생성할 수 있습니다. 예: `php artisan make:policy PostPolicy --model=Post`

<a name="via-middleware"></a>
### 미들웨어를 통한 인가

Laravel은 HTTP 요청이 라우트/컨트롤러에 도달하기 전에 액션 인가를 처리하는 미들웨어를 제공합니다. 기본적으로 `Illuminate\Auth\Middleware\Authorize` 미들웨어는 `App\Http\Kernel`의 `can` 키에 할당되어 있습니다.

아래 예시는 `can` 미들웨어를 이용해 사용자가 게시글을 수정할 수 있는지 인가하는 방법입니다.

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 사용자가 게시글을 수정할 수 있습니다.
})->middleware('can:update,post');
```

`can` 미들웨어에는 두 가지 인자를 전달합니다. 첫 번째는 인가할 액션명, 두 번째는 정책 메서드에 전달할 라우트 파라미터입니다. [암시적 모델 바인딩](/docs/{{version}}/routing#implicit-binding)을 사용하고 있다면, `App\Models\Post` 인스턴스가 정책에 전달됩니다. 권한이 없으면 403 응답을 반환합니다.

좀 더 간편하게, `can` 메서드로 미들웨어를 라우트에 붙일 수도 있습니다.

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 사용자가 게시글을 수정할 수 있습니다.
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 미들웨어 액션

`create`와 같이 모델 인스턴스를 필요로 하지 않는 정책 메서드는, 미들웨어에 클래스명을 인자로 전달할 수 있습니다.

```php
Route::post('/post', function () {
    // 사용자가 게시글을 생성할 수 있습니다.
})->middleware('can:create,App\Models\Post');
```

문자열로 클래스명을 직접 작성하는 것이 번거롭다면, `can` 메서드를 쓰면 됩니다.

```php
use App\Models\Post;

Route::post('/post', function () {
    // 사용자가 게시글을 생성할 수 있습니다.
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿을 통한 인가

Blade 템플릿에서, 특정 액션 수행 권한이 있는 사용자에게만 화면 일부를 보여주고 싶을 때가 있습니다. 예를 들어, 사용자가 게시글을 수정할 수 있어야만 수정 폼을 노출하려는 상황입니다. 이럴 때 `@can`과 `@cannot` 디렉티브를 사용할 수 있습니다.

```html
@can('update', $post)
    <!-- 사용자가 게시글을 수정할 수 있습니다 -->
@elsecan('create', App\Models\Post::class)
    <!-- 사용자가 새 게시글을 생성할 수 있습니다 -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- 사용자가 게시글을 수정할 수 없습니다 -->
@elsecannot('create', App\Models\Post::class)
    <!-- 사용자가 게시글을 생성할 수 없습니다 -->
@endcannot
```

이 디렉티브는 `@if`/`@unless` 구문을 간편하게 사용할 수 있게 해주는 단축키입니다. 위에서 작성한 `@can`, `@cannot` 구문은 아래와 같습니다.

```html
@if (Auth::user()->can('update', $post))
    <!-- 사용자가 게시글을 수정할 수 있습니다 -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- 사용자가 게시글을 수정할 수 없습니다 -->
@endunless
```

여러 액션 중 하나라도 인가되었는지 Blade에서 확인하려면 `@canany` 디렉티브를 사용할 수 있습니다.

```html
@canany(['update', 'view', 'delete'], $post)
    <!-- 사용자가 게시글을 수정, 조회, 삭제할 수 있습니다 -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- 사용자가 게시글을 생성할 수 있습니다 -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 액션

다른 인가 방식과 마찬가지로, `@can`과 `@cannot`에도 모델 인스턴스가 필요 없으면 클래스명을 전달할 수 있습니다.

```html
@can('create', App\Models\Post::class)
    <!-- 사용자가 게시글을 생성할 수 있습니다 -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- 사용자가 게시글을 생성할 수 없습니다 -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 컨텍스트 전달하기

정책을 사용하여 액션을 인가할 때, 두 번째 인자로 배열을 전달할 수 있습니다. 배열의 첫 번째 요소는 어느 정책을 사용할지 결정하는데 쓰이고, 나머지 요소들은 정책 메서드의 파라미터로 전달되어 인가 시 추가 컨텍스트로 활용됩니다. 아래는 `PostPolicy`의 추가 `$category` 파라미터를 사용하는 예입니다.

```php
/**
 * 사용자가 게시글을 수정할 수 있는지 판단
 *
 * @param \App\Models\User $user
 * @param \App\Models\Post $post
 * @param int $category
 * @return bool
 */
public function update(User $user, Post $post, int $category)
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```

실제 코드에서 이 정책을 사용할 때는 다음과 같이 배열로 추가 컨텍스트를 전달할 수 있습니다.

```php
/**
 * 블로그 게시글 수정
 *
 * @param \Illuminate\Http\Request $request
 * @param \App\Models\Post $post
 * @return \Illuminate\Http\Response
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post)
{
    $this->authorize('update', [$post, $request->category]);

    // 블로그 게시글 수정 가능...
}
```
