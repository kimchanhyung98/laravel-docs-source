# 권한 부여(Authorization)

- [소개](#introduction)
- [게이트(Gates)](#gates)
    - [게이트 작성하기](#writing-gates)
    - [게이트를 통한 액션 권한 부여](#authorizing-actions-via-gates)
    - [게이트 응답](#gate-responses)
    - [게이트 검사 가로채기](#intercepting-gate-checks)
    - [인라인 권한 부여](#inline-authorization)
- [정책(Policies) 생성하기](#creating-policies)
    - [정책 생성](#generating-policies)
    - [정책 등록](#registering-policies)
- [정책 작성하기](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델 없이 사용하는 메서드](#methods-without-models)
    - [게스트 사용자](#guest-users)
    - [정책 필터](#policy-filters)
- [정책을 이용한 액션 권한 부여](#authorizing-actions-using-policies)
    - [유저 모델을 통한 방식](#via-the-user-model)
    - [Gate 파사드를 통한 방식](#via-the-gate-facade)
    - [미들웨어를 통한 방식](#via-middleware)
    - [Blade 템플릿을 통한 방식](#via-blade-templates)
    - [추가 컨텍스트 전달](#supplying-additional-context)
- [권한 부여 & Inertia](#authorization-and-inertia)

<a name="introduction"></a>
## 소개

Laravel은 내장 [인증](/docs/{{version}}/authentication) 서비스 외에도, 주어진 리소스에 대해 사용자의 작업 권한을 쉽게 확인할 수 있는 기능을 제공합니다. 예를 들어, 사용자가 인증되었더라도 애플리케이션에서 관리하는 특정 Eloquent 모델 또는 데이터베이스 레코드를 수정하거나 삭제할 권한은 없을 수 있습니다. Laravel의 권한 부여 기능은 이러한 권한 검사 작업을 손쉽게 구성하고 관리할 수 있는 방법을 제공합니다.

Laravel에서는 두 가지 주요 방식([게이트(gates)](#gates), [정책(policies)](#creating-policies))으로 권한을 부여할 수 있습니다. 게이트와 정책을 라우트와 컨트롤러 관계처럼 생각하면 이해하기 쉽습니다. 게이트는 간단하고 클로저 기반 접근을 제공하며, 정책은 컨트롤러와 같이 특정 모델이나 리소스에 대한 로직을 그룹화합니다. 이 문서에서는 먼저 게이트를, 그리고 정책을 살펴봅니다.

애플리케이션을 개발할 때 게이트와 정책 중 하나만 선택해서 쓸 필요는 없습니다. 대부분의 애플리케이션은 게이트와 정책이 혼합되어 사용되고, 이는 전혀 문제가 되지 않습니다! 게이트는 모델이나 리소스와 직접적으로 관련 없는 액션(예: 관리자 대시보드 보기 등)에 가장 적합합니다. 반대로 특정 모델이나 리소스에 대한 액션 권한을 확인하고자 할 때는 정책 사용을 추천합니다.

<a name="gates"></a>
## 게이트(Gates)

<a name="writing-gates"></a>
### 게이트 작성하기

> [!WARNING]  
> 게이트는 Laravel의 권한 부여 기능의 기본 개념을 배우기에 훌륭하지만, 견고한 Laravel 애플리케이션을 개발할 때는 [정책](#creating-policies)으로 권한 규칙을 구성하는 것을 권장합니다.

게이트는 사용자가 특정 작업을 수행할 권한이 있는지 결정하는 클로저입니다. 일반적으로 게이트는 `App\Providers\AppServiceProvider`의 `boot` 메서드 내에서 `Gate` 파사드를 사용하여 정의합니다. 게이트는 항상 첫 번째 인자로 사용자 인스턴스를 받고, 필요한 경우 추가적으로 관련 Eloquent 모델 등의 인자를 받을 수 있습니다.

아래는 사용자가 주어진 `App\Models\Post` 모델을 수정할 수 있는지 확인하는 게이트 예시입니다. 게이트는 사용자의 `id`와 게시글을 생성한 사용자의 `user_id`를 비교합니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('update-post', function (User $user, Post $post) {
        return $user->id === $post->user_id;
    });
}
```

컨트롤러처럼, 게이트를 클래스 콜백 배열로도 정의할 수 있습니다:

```php
use App\Policies\PostPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('update-post', [PostPolicy::class, 'update']);
}
```

<a name="authorizing-actions-via-gates"></a>
### 액션 권한 부여

게이트를 사용하여 액션을 권한 검사하려면 `Gate` 파사드의 `allows` 또는 `denies` 메서드를 사용하면 됩니다. 현재 인증된 사용자를 직접 넘길 필요가 없으며, Laravel이 알아서 게이트 클로저에 유저를 전달합니다. 일반적으로 컨트롤러에서 권한이 필요한 액션 전에 게이트를 호출합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class PostController extends Controller
{
    /**
     * Update the given post.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if (! Gate::allows('update-post', $post)) {
            abort(403);
        }

        // 게시글 업데이트...

        return redirect('/posts');
    }
}
```

현재 인증된 유저가 아닌 다른 유저를 검사하고 싶다면 `Gate` 파사드의 `forUser` 메서드를 사용하세요:

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // 해당 유저는 게시글을 수정할 수 있습니다...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // 해당 유저는 게시글을 수정할 수 없습니다...
}
```

여러 액션을 한 번에 검사하려면 `any` 또는 `none` 메서드를 사용할 수 있습니다:

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // 유저는 게시글을 수정하거나 삭제할 수 있습니다...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // 유저는 게시글을 수정하거나 삭제할 수 없습니다...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 예외와 함께 권한 부여

권한이 없을 경우 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 던지고 싶다면, `Gate`의 `authorize` 메서드를 사용하세요. 이 예외는 Laravel이 자동으로 403 HTTP 응답으로 변환합니다:

```php
Gate::authorize('update-post', $post);

// 액션이 허가됨...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 전달

게이트의 `allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot` 등의 메서드와 [Blade 디렉티브](#via-blade-templates)(`@can`, `@cannot`, `@canany`)는 두 번째 인자로 배열을 받을 수 있습니다. 이 배열의 값들은 게이트 클로저의 인자로 전달되어, 추가적인 맥락이 필요한 경우 유용하게 활용할 수 있습니다:

```php
use App\Models\Category;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::define('create-post', function (User $user, Category $category, bool $pinned) {
    if (! $user->canPublishToGroup($category->group)) {
        return false;
    } elseif ($pinned && ! $user->canPinPosts()) {
        return false;
    }

    return true;
});

if (Gate::check('create-post', [$category, $pinned])) {
    // 유저가 게시글을 생성할 수 있습니다...
}
```

<a name="gate-responses"></a>
### 게이트 응답

지금까지는 단순히 불린값을 반환하는 게이트만 살펴봤습니다. 때로는 좀 더 상세한 응답, 예를 들어 에러 메시지가 필요한 경우가 있습니다. 이럴 때는 `Illuminate\Auth\Access\Response`를 반환할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::deny('You must be an administrator.');
});
```

이렇게 게이트에서 권한 응답 객체를 반환해도 `Gate::allows`는 여전히 불린값을 반환합니다. 더 자세한 응답이 필요하다면 `Gate::inspect`를 사용하세요:

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // 액션이 허가됨...
} else {
    echo $response->message();
}
```

`Gate::authorize`를 사용할 때는, 게이트에서 지정한 에러 메시지가 HTTP 응답에 그대로 전달됩니다:

```php
Gate::authorize('edit-settings');

// 액션이 허가됨...
```

<a name="customizing-gate-response-status"></a>
#### HTTP 응답 상태 커스터마이즈

게이트로 권한 검사에 실패하면 `403` HTTP 응답이 기본값으로 반환됩니다. 다른 HTTP 상태코드를 반환하려면 `Illuminate\Auth\Access\Response`의 `denyWithStatus` 정적 메서드를 사용하세요:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::denyWithStatus(404);
});
```

`404` 응답으로 리소스를 숨기는 것이 흔하다면, `denyAsNotFound` 메서드를 사용하세요:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::denyAsNotFound();
});
```

<a name="intercepting-gate-checks"></a>
### 게이트 검사 가로채기

특정 유저(예: 관리자)에게 모든 권한을 부여하고 싶을 때 `before` 메서드로 모든 권한 검사 전에 실행될 클로저를 지정할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저에서 null이 아닌 값을 반환하면 그 값이 최종 권한 검사 결과가 됩니다.

모든 권한 검사 후에 실행할 클로저는 `after` 메서드로 정의할 수 있습니다:

```php
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after` 클로저가 반환한 값은 게이트 또는 정책이 `null`을 반환한 경우에만 검사 결과를 덮어씁니다.

<a name="inline-authorization"></a>
### 인라인 권한 부여

특정 액션에 대해 전용 게이트를 따로 만들지 않고 즉석에서 권한을 검사하고 싶을 때 `Gate::allowIf`, `Gate::denyIf` 메서드를 사용할 수 있습니다. 인라인 권한 검사는 ["before" 또는 "after" 훅](#intercepting-gate-checks)을 실행하지 않습니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

액션이 허가되지 않았거나 인증된 유저가 없다면, Laravel은 `Illuminate\Auth\Access\AuthorizationException` 예외를 자동으로 던집니다. 이 예외는 403 HTTP 응답으로 변환됩니다.

<a name="creating-policies"></a>
## 정책(Policies) 생성하기

<a name="generating-policies"></a>
### 정책 생성

정책은 특정 모델이나 리소스에 대한 권한 로직을 클래스 단위로 그룹화합니다. 예를 들어 블로그 애플리케이션에서는 `App\Models\Post` 모델과 이에 대응하는 `App\Policies\PostPolicy`를 만들어 게시글 생성, 수정 등 권한을 관리할 수 있습니다.

`make:policy` Artisan 명령어로 정책을 생성할 수 있습니다. 생성된 정책 파일은 기본적으로 `app/Policies` 디렉터리에 생성됩니다. 이 디렉터리가 없다면 Laravel이 자동으로 만들어줍니다:

```shell
php artisan make:policy PostPolicy
```

생성된 기본 파일은 빈 정책 클래스입니다. 리소스(view, create, update, delete 등)에 맞는 예제 메서드도 포함하려면 `--model` 옵션을 추가하세요:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록

<a name="policy-discovery"></a>
#### 정책 자동 발견

기본적으로 Laravel은 모델과 정책 클래스가 표준 네이밍 컨벤션을 지키면 정책을 자동으로 연결합니다. 모델이 `app/Models`, 정책이 `app/Policies`에 존재해야 하며, 정책명은 모델명 + `Policy`이어야 합니다. 예를 들어, `User` 모델은 `UserPolicy` 정책과 매핑됩니다.

정책 자동화가 아니라 직접 탐색 로직을 작성하려면 `Gate::guessPolicyNamesUsing` 메서드로 콜백을 등록할 수 있습니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드 내에서 사용합니다:

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // 주어진 모델에 대한 정책 클래스명 반환...
});
```

<a name="manually-registering-policies"></a>
#### 정책 수동 등록

`Gate` 파사드를 사용해서 모델에 해당하는 정책을 직접 등록할 수도 있습니다. 역시 `AppServiceProvider`의 `boot` 메서드에서 선언합니다:

```php
use App\Models\Order;
use App\Policies\OrderPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::policy(Order::class, OrderPolicy::class);
}
```

<a name="writing-policies"></a>
## 정책 작성하기

<a name="policy-methods"></a>
### 정책 메서드

정책 클래스를 등록한 후에는 각 액션에 맞는 메서드를 추가할 수 있습니다. 예를 들어, `PostPolicy`에 게시글(`App\Models\Post`)을 수정할 수 있는지 검사하는 `update` 메서드를 정의할 수 있습니다.

`update` 메서드는 `User`와 `Post` 인스턴스를 받아 사용자가 해당 게시글을 수정할 권한이 있는지(`true`/`false`) 반환합니다:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the given post can be updated by the user.
     */
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}
```

이외에도 정책에서 `view`, `delete` 등 다양한 이름의 메서드를 자유롭게 추가하여 사용할 수 있습니다.

`--model` 옵션을 사용해 Artisan으로 정책을 생성하면, `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 액션에 해당하는 메서드가 기본적으로 포함됩니다.

> [!NOTE]  
> 모든 정책 클래스는 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 생성자에서 필요한 의존성을 타입-힌팅하면 자동으로 주입받을 수 있습니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지는 불린값을 반환하는 예만 살펴봤지만, 좀 더 상세한 메시지를 내보내려면, 정책 메서드에서 `Illuminate\Auth\Access\Response` 객체를 반환할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::deny('You do not own this post.');
}
```

정책에서 이와 같이 권한 응답을 반환하면, `Gate::allows`는 여전히 불린값을 반환합니다. 자세한 결과가 필요하면 `Gate::inspect`를 사용하세요:

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // 액션이 허가됨...
} else {
    echo $response->message();
}
```

`Gate::authorize`를 사용할 때는 지정한 메시지가 HTTP 응답으로 전달됩니다:

```php
Gate::authorize('update', $post);

// 액션이 허가됨...
```

<a name="customizing-policy-response-status"></a>
#### HTTP 응답 상태 커스터마이즈

정책 메서드에서 액션이 거부되면 기본적으로 `403` 이 반환됩니다. 다른 HTTP 상태코드를 반환하려면 `denyWithStatus`를 사용하세요:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyWithStatus(404);
}
```

또한, 리소스를 `404`으로 숨기고 싶다면 `denyAsNotFound`를 사용할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyAsNotFound();
}
```

<a name="methods-without-models"></a>
### 모델 없이 사용하는 메서드

일부 정책 메서드는 현재 인증된 사용자 인스턴스만 받는 경우가 있습니다. 주로 `create` 같은 액션일 때 그렇습니다. 예를 들어, 사용자가 게시글을 생성할 권한이 있는지 확인하려면:

```php
/**
 * Determine if the given user can create posts.
 */
public function create(User $user): bool
{
    return $user->role == 'writer';
}
```

<a name="guest-users"></a>
### 게스트 사용자

기본적으로 인증되지 않은(게스트) 사용자가 요청한 경우, 모든 게이트와 정책은 자동으로 `false`를 반환합니다. 하지만, 유저 인자를 "옵셔널" 타입힌트(`?User`)로 선언하거나 기본값을 `null`로 지정하면 통과시킬 수 있습니다:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the given post can be updated by the user.
     */
    public function update(?User $user, Post $post): bool
    {
        return $user?->id === $post->user_id;
    }
}
```

<a name="policy-filters"></a>
### 정책 필터

특정 유저가 정책 내 모든 액션에 대해 권한이 있다고 판단하려면 `before` 메서드를 정책에 정의하세요. `before` 메서드는 정책 내 어떤 메서드보다 먼저 실행되어, 권한을 일괄 허가할 수 있습니다. 주로 어드민 계정에 사용됩니다:

```php
use App\Models\User;

/**
 * 사전 권한 확인
 */
public function before(User $user, string $ability): bool|null
{
    if ($user->isAdministrator()) {
        return true;
    }

    return null;
}
```

특정 유형의 유저에 대해 모두 거부하려면 `false`를 반환하세요. `null`을 반환하면 개별 정책 메서드로 검사 흐름이 넘어갑니다.

> [!WARNING]  
> 정책 클래스에 해당 액션 메서드가 없으면 `before`는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 이용한 액션 권한 부여

<a name="via-the-user-model"></a>
### 유저 모델을 통한 방식

Laravel의 `App\Models\User` 모델에는 권한 부여를 쉽게 할 수 있는 `can`과 `cannot` 메서드가 있습니다. 두 메서드는 액션명과 관련 모델을 인자로 받습니다. 보통 컨트롤러 내에서 사용합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Update the given post.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if ($request->user()->cannot('update', $post)) {
            abort(403);
        }

        // 게시글 업데이트...

        return redirect('/posts');
    }
}
```

[정책이 등록](#registering-policies)된 모델이라면, `can` 메서드는 자동으로 적절한 정책을 호출해 결과를 반환합니다. 정책이 없다면 게이트 클로저를 찾습니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 액션

일부 액션(`create` 등)은 모델 인스턴스가 필요하지 않습니다. 이 경우 클래스명을 `can`의 두 번째 인자로 넘겨주면 됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Create a post.
     */
    public function store(Request $request): RedirectResponse
    {
        if ($request->user()->cannot('create', Post::class)) {
            abort(403);
        }

        // 게시글 생성...

        return redirect('/posts');
    }
}
```

<a name="via-the-gate-facade"></a>
### Gate 파사드를 통한 방식

User 모델의 헬퍼 메서드 외에도, 언제든지 `Gate` 파사드의 `authorize` 메서드로 권한을 검사할 수 있습니다.

이 메서드는 액션명과 관련 모델을 인자로 받으며, 권한이 거부되면 `Illuminate\Auth\Access\AuthorizationException` 예외를 던지고, 이 예외는 자동으로 403 HTTP 응답으로 변환됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class PostController extends Controller
{
    /**
     * Update the given blog post.
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        Gate::authorize('update', $post);

        // 현재 유저가 블로그 게시글을 수정할 수 있습니다...

        return redirect('/posts');
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 액션

앞서 설명한 것처럼, `create` 같은 일부 정책 메서드는 모델 인스턴스를 받지 않습니다. 이럴 때는 클래스명을 `authorize`의 두 번째 인자로 넘깁니다:

```php
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

/**
 * Create a new blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request): RedirectResponse
{
    Gate::authorize('create', Post::class);

    // 현재 유저가 블로그 게시글을 생성할 수 있습니다...

    return redirect('/posts');
}
```

<a name="via-middleware"></a>
### 미들웨어를 통한 방식

Laravel에는 요청이 라우트나 컨트롤러에 도달하기 전에 권한을 검사할 수 있는 미들웨어가 있습니다. 기본적으로 `Illuminate\Auth\Middleware\Authorize`는 `can` [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)으로 라우트에 붙일 수 있습니다. 다음은 사용자가 게시글을 업데이트할 권한이 있는지 미들웨어로 검사하는 예시입니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 유저가 게시글을 업데이트할 수 있습니다...
})->middleware('can:update,post');
```

위 예시에서 `can` 미들웨어에는 두 가지 인자를 전달합니다. 첫 번째는 권한 액션명이고, 두 번째는 정책 메서드로 전달할 라우트 파라미터(`post`)입니다. [암시적 모델 바인딩](/docs/{{version}}/routing#implicit-binding)이 작동해 `App\Models\Post` 인스턴스가 전달됩니다. 권한이 없을 경우, 403 상태로 응답이 반환됩니다.

보다 직관적으로 `can` 메서드 체인으로 미들웨어를 붙일 수도 있습니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 유저가 게시글을 업데이트할 수 있습니다...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 액션

`create`와 같이 모델 인스턴스가 필요 없는 정책에도 미들웨어에서 클래스명을 명시할 수 있습니다:

```php
Route::post('/post', function () {
    // 현재 유저가 게시글을 생성할 수 있습니다...
})->middleware('can:create,App\Models\Post');
```

클래스명을 문자열로 풀네임 써서 정의하는 게 번거롭다면, `can` 메서드 체인으로 넘길 수 있습니다:

```php
use App\Models\Post;

Route::post('/post', function () {
    // 현재 유저가 게시글을 생성할 수 있습니다...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿을 통한 방식

Blade 템플릿에서 특정 작업에 대한 권한이 있는 사용자에게만 화면의 일부를 보여주고 싶을 경우가 있습니다. 예를 들면, 사용자가 실제로 게시글을 수정할 수 있을 때만 수정 폼을 보여주는 역활입니다. 이때는 `@can`과 `@cannot` 디렉티브를 사용할 수 있습니다:

```blade
@can('update', $post)
    <!-- 현재 유저가 게시글을 수정할 수 있습니다... -->
@elsecan('create', App\Models\Post::class)
    <!-- 현재 유저가 새 게시글을 생성할 수 있습니다... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- 현재 유저가 게시글을 수정할 수 없습니다... -->
@elsecannot('create', App\Models\Post::class)
    <!-- 현재 유저가 새 게시글을 생성할 수 없습니다... -->
@endcannot
```

이 디렉티브는 `@if`/`@unless` 구문의 간편한 단축키입니다. 위의 코드는 아래와 동일합니다:

```blade
@if (Auth::user()->can('update', $post))
    <!-- 현재 유저가 게시글을 수정할 수 있습니다... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- 현재 유저가 게시글을 수정할 수 없습니다... -->
@endunless
```

액션 배열에서 하나라도 권한이 있으면 표시할 때는 `@canany` 디렉티브를 이용하세요:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- 현재 유저가 게시글을 수정, 조회, 삭제할 수 있습니다... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- 현재 유저가 게시글을 생성할 수 있습니다... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 액션

다른 권한 메서드와 마찬가지로, 모델 인스턴스가 필요 없는 액션은 클래스명을 `@can`, `@cannot`에 넘기면 됩니다:

```blade
@can('create', App\Models\Post::class)
    <!-- 현재 유저가 게시글을 생성할 수 있습니다... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- 현재 유저가 게시글을 생성할 수 없습니다... -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 컨텍스트 전달

정책을 사용할 때, 두 번째 인자로 배열을 넘겨 다양한 컨텍스트 정보를 전달할 수 있습니다. 배열의 첫 번째 요소는 사용할 정책을 결정하고, 나머지는 정책 메서드의 추가 인자로 전달됩니다. 예를 들어, 정책 메서드에 추가적으로 카테고리 값을 받는 경우:

```php
/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post, int $category): bool
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```

이 정책을 호출할 때는 다음과 같이 배열로 추가 값을 넘깁니다:

```php
/**
 * Update the given blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post): RedirectResponse
{
    Gate::authorize('update', [$post, $request->category]);

    // 현재 유저가 블로그 게시글을 업데이트할 수 있습니다...

    return redirect('/posts');
}
```

<a name="authorization-and-inertia"></a>
## 권한 부여 & Inertia

권한 부여는 항상 서버에서 처리해야 하지만, 프론트엔드 측에서 UI를 적절히 렌더링하기 위해 권한 정보를 제공하면 편리합니다. Laravel은 Inertia 기반 프론트엔드로 권한 정보를 노출하는 방식에 대한 규칙을 따로 정의하지 않습니다.

하지만, Laravel의 Inertia 기반 [스타터 킷](/docs/{{version}}/starter-kits)를 사용 중이라면, 애플리케이션에는 이미 `HandleInertiaRequests` 미들웨어가 있습니다. 이 미들웨어의 `share` 메서드에서 모든 Inertia 페이지에 공유될 데이터를 정의할 수 있습니다. 여기에 사용자 권한 정보를 정의하면 됩니다:

```php
<?php

namespace App\Http\Middleware;

use App\Models\Post;
use Illuminate\Http\Request;
use Inertia\Middleware;

class HandleInertiaRequests extends Middleware
{
    // ...

    /**
     * 기본적으로 공유되는 props 정의.
     *
     * @return array<string, mixed>
     */
    public function share(Request $request)
    {
        return [
            ...parent::share($request),
            'auth' => [
                'user' => $request->user(),
                'permissions' => [
                    'post' => [
                        'create' => $request->user()->can('create', Post::class),
                    ],
                ],
            ],
        ];
    }
}
```
