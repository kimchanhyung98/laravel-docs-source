# 권한 부여 (Authorization)

- [소개](#introduction)
- [게이트 (Gates)](#gates)
    - [게이트 작성하기](#writing-gates)
    - [액션 권한 부여](#authorizing-actions-via-gates)
    - [게이트 응답](#gate-responses)
    - [게이트 검사 가로채기](#intercepting-gate-checks)
    - [인라인 권한 부여](#inline-authorization)
- [정책 만들기 (Creating Policies)](#creating-policies)
    - [정책 생성하기](#generating-policies)
    - [정책 등록하기](#registering-policies)
- [정책 작성하기](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델이 필요 없는 메서드](#methods-without-models)
    - [비인증 사용자 (Guest Users)](#guest-users)
    - [정책 필터](#policy-filters)
- [정책을 이용한 액션 권한 부여](#authorizing-actions-using-policies)
    - [User 모델을 통한 권한 부여](#via-the-user-model)
    - [컨트롤러 헬퍼를 통한 권한 부여](#via-controller-helpers)
    - [미들웨어를 통한 권한 부여](#via-middleware)
    - [Blade 템플릿을 통한 권한 부여](#via-blade-templates)
    - [추가 컨텍스트 전달하기](#supplying-additional-context)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 내장된 [인증](/docs/10.x/authentication) 서비스를 제공하는 것 외에도, 특정 리소스에 대해 사용자의 작업 권한을 간단히 검증할 수 있는 방법을 제공합니다. 예를 들어, 사용자가 인증되었더라도 애플리케이션에서 관리하는 특정 Eloquent 모델이나 데이터베이스 레코드를 수정하거나 삭제할 권한이 없을 수 있습니다. Laravel의 권한 부여 기능은 이러한 권한 검사들을 쉽고 체계적으로 관리할 수 있게 해줍니다.

Laravel에서 권한 부여를 처리하는 주요 방법은 두 가지가 있습니다: [게이트](#gates)와 [정책](#creating-policies)입니다. 게이트와 정책은 각각 라우트와 컨트롤러의 관계처럼 생각할 수 있습니다. 게이트는 클로저 기반의 간단한 권한 부여 방법을 제공하는 반면, 정책은 컨트롤러처럼 특정 모델이나 리소스에 관련된 로직을 그룹화합니다. 이 문서에서는 먼저 게이트를 살펴보고, 이후에 정책에 대해 알아보겠습니다.

애플리케이션을 구축할 때 반드시 게이트만 사용하거나 정책만 사용하는 것을 선택할 필요는 없습니다. 대부분의 애플리케이션은 게이트와 정책을 적절히 혼합하여 사용하고 있으며 이는 전혀 문제되지 않습니다! 게이트는 관리자 대시보드 조회 같은 모델 또는 리소스와 관련 없는 작업에 적합합니다. 반면, 정책은 특정 모델이나 리소스에 대한 작업을 권한 부여할 때 사용하면 좋습니다.

<a name="gates"></a>
## 게이트 (Gates)

<a name="writing-gates"></a>
### 게이트 작성하기

> [!WARNING]  
> 게이트는 Laravel 권한 부여 기능의 기본 개념을 익히기에 훌륭한 방법입니다. 그러나 견고한 Laravel 애플리케이션을 구축할 때는 권한 규칙을 체계적으로 관리할 수 있도록 [정책](#creating-policies)을 사용하는 편이 좋습니다.

게이트는 사용자가 특정 작업을 수행할 권한이 있는지 결정하는 클로저입니다. 일반적으로 게이트는 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드 내에서 `Gate` 파사드를 사용해 정의합니다. 게이트는 항상 첫 번째 인수로 사용자 인스턴스를 받고, 필요에 따라 관련 Eloquent 모델 등 추가 인수를 받을 수도 있습니다.

다음 예시는 사용자가 주어진 `App\Models\Post` 모델을 업데이트할 수 있는지 판단하는 게이트를 정의합니다. 사용자의 `id`와 게시물을 작성한 사용자의 `user_id`를 비교하여 권한을 부여합니다:

```
use App\Models\Post;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Register any authentication / authorization services.
 */
public function boot(): void
{
    Gate::define('update-post', function (User $user, Post $post) {
        return $user->id === $post->user_id;
    });
}
```

컨트롤러처럼 게이트도 클래스 콜백 배열을 사용해 정의할 수 있습니다:

```
use App\Policies\PostPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * Register any authentication / authorization services.
 */
public function boot(): void
{
    Gate::define('update-post', [PostPolicy::class, 'update']);
}
```

<a name="authorizing-actions-via-gates"></a>
### 액션 권한 부여

게이트를 통해 작업 권한을 부여하려면 `Gate` 파사드가 제공하는 `allows` 또는 `denies` 메서드를 사용해야 합니다. 현재 인증된 사용자를 명시적으로 넘길 필요는 없으며, Laravel이 자동으로 사용자 인스턴스를 게이트 클로저에 전달합니다. 일반적으로 권한이 필요한 작업을 수행하기 전에 애플리케이션 컨트롤러 내에서 게이트 권한 부여 메서드를 호출합니다:

```
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

        // Update the post...

        return redirect('/posts');
    }
}
```

현재 인증된 사용자 외에 다른 사용자가 작업 권한이 있는지 확인하려면 `Gate` 파사드의 `forUser` 메서드를 사용하세요:

```
if (Gate::forUser($user)->allows('update-post', $post)) {
    // The user can update the post...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // The user can't update the post...
}
```

복수의 작업 권한을 한 번에 확인할 때 `any` 또는 `none` 메서드를 사용하세요:

```
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // The user can update or delete the post...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // The user can't update or delete the post...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 권한 부여 또는 예외 발생

권한 부여를 시도하며, 해당 작업을 할 권한이 없으면 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 던지려면 `Gate` 파사드의 `authorize` 메서드를 사용하세요. `AuthorizationException` 인스턴스는 Laravel의 예외 핸들러에 의해 자동으로 403 HTTP 응답으로 변환됩니다:

```
Gate::authorize('update-post', $post);

// The action is authorized...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 전달

`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot` 같은 게이트 권한 부여 메서드와 권한 부여용 [Blade 디렉티브](#via-blade-templates) (`@can`, `@cannot`, `@canany`)는 두 번째 인수로 배열을 받을 수 있습니다. 배열 요소들은 게이트 클로저에 파라미터로 전달되어 권한 결정에 필요한 추가 정보를 전달할 수 있습니다:

```
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
    // The user can create the post...
}
```

<a name="gate-responses"></a>
### 게이트 응답

지금까지는 단순히 부울 값만 반환하는 게이트를 살펴보았지만, 때때로 권한 부여 결과에 대해 더 상세한 메시지를 포함하는 응답을 반환하고 싶을 수 있습니다. 이때는 `Illuminate\Auth\Access\Response` 인스턴스를 반환할 수 있습니다:

```
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
                ? Response::allow()
                : Response::deny('You must be an administrator.');
});
```

게이트에서 권한 응답을 반환해도 `Gate::allows` 메서드는 여전히 단순한 부울 값을 반환합니다. 하지만 `Gate::inspect` 메서드를 사용하면 게이트가 반환한 전체 권한 응답을 얻을 수 있습니다:

```
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드를 사용할 때는 권한이 없으면 예외를 던지며, 이때 응답에 포함된 오류 메시지가 HTTP 응답으로 전달됩니다:

```
Gate::authorize('edit-settings');

// The action is authorized...
```

<a name="customising-gate-response-status"></a>
#### HTTP 응답 상태 코드 커스터마이징

게이트가 권한을 거부하면 기본적으로 403 HTTP 상태 코드가 반환됩니다. 하지만 상황에 따라 다른 상태 코드를 반환하는 것이 유용할 수 있습니다. 이때 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용해 거부 시 반환할 HTTP 상태 코드를 지정할 수 있습니다:

```
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
                ? Response::allow()
                : Response::denyWithStatus(404);
});
```

웹 애플리케이션에서는 리소스를 숨기기 위해 404 응답을 사용하는 패턴이 흔하므로, 이를 위해 편리하게 `denyAsNotFound` 메서드도 제공합니다:

```
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

특정 사용자에게 모든 능력을 부여하고 싶을 때 `before` 메서드를 사용해 모든 다른 권한 부여 검사 이전에 실행되는 클로저를 정의할 수 있습니다:

```
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저가 null이 아닌 값을 반환하면 해당 값이 권한 부여 결과로 간주되어 이후 권한 검사는 건너뜁니다.

`after` 메서드를 사용하면 모든 권한 검사 후에 실행되는 클로저를 정의할 수 있습니다:

```
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after` 클로저도 null이 아닌 값을 반환하면 그 결과가 권한 부여 결과로 사용됩니다.

<a name="inline-authorization"></a>
### 인라인 권한 부여

때로는 별도의 게이트를 작성하지 않고 현재 인증된 사용자가 특정 액션 권한이 있는지 바로 확인하고 싶을 수 있습니다. Laravel에서는 `Gate::allowIf`와 `Gate::denyIf` 메서드를 사용해 이런 인라인 권한 검사를 지원합니다. 인라인 권한 부여는 ["before" 또는 "after" 권한 훅](#intercepting-gate-checks)을 실행하지 않습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

권한이 없거나 인증된 사용자가 없는 상태에서 이 메서드들을 사용하면 Laravel이 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 던집니다. 이 예외는 Laravel 예외 핸들러에 의해 403 HTTP 응답으로 변환됩니다.

<a name="creating-policies"></a>
## 정책 만들기 (Creating Policies)

<a name="generating-policies"></a>
### 정책 생성하기

정책은 특정 모델이나 리소스와 관련된 권한 로직을 그룹화한 클래스입니다. 예를 들어, 블로그 애플리케이션에서는 `App\Models\Post` 모델과 함께 사용자 액션(생성, 수정 등)을 권한 부여하는 `App\Policies\PostPolicy`가 있을 수 있습니다.

`make:policy` Artisan 명령어로 정책을 생성할 수 있습니다. 생성된 정책은 `app/Policies` 디렉토리에 저장됩니다. 해당 디렉토리가 없으면 Laravel이 생성해 줍니다:

```shell
php artisan make:policy PostPolicy
```

`make:policy` 명령어는 빈 정책 클래스를 생성합니다. 만약 조회, 생성, 수정, 삭제 관련 예제 정책 메서드가 포함된 클래스를 생성하려면 `--model` 옵션을 함께 지정하세요:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록하기

정책 클래스를 생성한 후에는 반드시 등록해야 합니다. 정책 등록은 Laravel에 특정 모델 타입에 대해 어떤 정책 클래스를 사용할지 알려주는 역할을 합니다.

새 Laravel 애플리케이션에 포함된 `App\Providers\AuthServiceProvider`에는 `policies` 속성이 있어 Eloquent 모델과 정책 클래스를 매핑할 수 있습니다. 정책을 등록하면 Laravel은 해당 Eloquent 모델에 대한 권한 부여 시 적절한 정책을 자동으로 사용합니다:

```
<?php

namespace App\Providers;

use App\Models\Post;
use App\Policies\PostPolicy;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Gate;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * The policy mappings for the application.
     *
     * @var array
     */
    protected $policies = [
        Post::class => PostPolicy::class,
    ];

    /**
     * Register any application authentication / authorization services.
     */
    public function boot(): void
    {
        // ...
    }
}
```

<a name="policy-auto-discovery"></a>
#### 정책 자동 발견

직접 정책을 등록하는 대신, Laravel의 기본 네이밍 규칙을 따를 경우 정책을 자동으로 발견할 수도 있습니다. 모델과 정책은 보통 모델을 담는 디렉토리보다 같은 위치거나 상위 위치에 `Policies` 디렉토리에 위치해야 합니다. 예를 들어, 모델은 `app/Models`에, 정책은 `app/Policies`에 두면 Laravel은 `app/Models/Policies`와 `app/Policies`에서 자동으로 정책을 찾습니다. 또한 정책 클래스 이름은 모델 이름에 `Policy` 접미사를 붙여야 합니다. 예를 들어 `User` 모델에 대응하는 정책은 `UserPolicy`가 되어야 합니다.

직접 정책 자동 발견 로직을 정의하려면 `Gate::guessPolicyNamesUsing` 메서드에 커스텀 콜백을 등록할 수 있습니다. 일반적으로 `AuthServiceProvider`의 `boot` 메서드에서 호출합니다:

```
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // 주어진 모델에 대한 정책 클래스 이름 반환...
});
```

> [!WARNING]  
> `AuthServiceProvider`에서 명시적으로 매핑된 정책이 있다면 자동 발견 정책보다 우선 적용됩니다.

<a name="writing-policies"></a>
## 정책 작성하기

<a name="policy-methods"></a>
### 정책 메서드

정책 클래스가 등록되고 나면, 권한을 판단할 각 액션별 메서드를 추가할 수 있습니다. 예를 들어, `PostPolicy`에 `update` 메서드를 정의해 `App\Models\User`가 특정 `App\Models\Post` 인스턴스를 수정할 수 있는지 판단합니다.

`update` 메서드는 `User`와 `Post` 인스턴스를 인수로 받고, 사용자가 해당 게시물을 수정할 권한이 있으면 `true`, 없으면 `false`를 반환해야 합니다. 여기서는 사용자의 `id`가 게시물의 `user_id`와 일치하는지 확인합니다:

```
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

필요에 따라 정책에 추가 메서드를 더 정의할 수 있습니다. 예를 들어, `view`나 `delete` 메서드 등을 정의해 다양한 `Post` 관련 작업 권한을 관리할 수 있습니다. 메서드 이름은 자유롭게 지정할 수 있습니다.

`--model` 옵션으로 정책을 만들었다면, `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 동작에 대한 메서드가 이미 포함되어 있습니다.

> [!NOTE]  
> 모든 정책 클래스는 Laravel [서비스 컨테이너](/docs/10.x/container)를 통해 해석되므로, 생성자에 필요한 의존성을 타입 힌트하면 자동으로 의존성 주입됩니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지는 단순한 부울 값 반환 정책 메서드만 살펴보았지만, 때로는 더 구체적인 권한 응답과 오류 메시지를 반환하고 싶을 수 있습니다. 이럴 때는 정책 메서드에서 `Illuminate\Auth\Access\Response` 인스턴스를 반환할 수 있습니다:

```
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

정책에서 권한 응답을 반환해도 `Gate::allows`는 단순 부울값을 반환합니다. 하지만 `Gate::inspect`를 사용해서 게이트가 반환한 전체 권한 응답을 확인할 수 있습니다:

```
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드를 사용하면 권한이 없을 때 `AuthorizationException`이 발생하는데, 이때 응답 메시지가 HTTP 응답에 전달됩니다:

```
Gate::authorize('update', $post);

// The action is authorized...
```

<a name="customising-policy-response-status"></a>
#### HTTP 응답 상태 코드 커스터마이징

정책 메서드에서 권한이 거부되면 기본적으로 403 HTTP 상태 코드를 반환합니다. 하지만 상황에 따라 다른 상태 코드를 반환하고 싶을 수 있습니다. 이때 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용해 실패 시 반환할 HTTP 상태 코드를 지정할 수 있습니다:

```
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

웹 애플리케이션에서 404 응답으로 리소스를 숨기는 패턴이 많으므로, 편의 메서드인 `denyAsNotFound`도 제공합니다:

```
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
### 모델이 필요 없는 메서드

일부 정책 메서드는 현재 인증된 사용자 인스턴스만 받습니다. 보통 `create` 액션 권한 부여에 많이 사용됩니다. 예를 들어, 블로그에서 사용자가 게시글을 생성할 권한이 있는지 판단하려면 아래처럼 메서드를 작성합니다:

```
/**
 * Determine if the given user can create posts.
 */
public function create(User $user): bool
{
    return $user->role == 'writer';
}
```

<a name="guest-users"></a>
### 비인증 사용자 (Guest Users)

기본적으로 인증되지 않은 HTTP 요청에서는 모든 게이트와 정책이 자동으로 `false`를 반환합니다. 하지만 권한 검사가 인증되지 않은 사용자에게도 통과하도록 허용하고 싶다면, 사용자 인수에 "옵셔널" 타입 힌트(`?User`)를 선언하거나 기본값으로 `null`을 지정하면 됩니다:

```
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

특정 사용자가 해당 정책 내 모든 작업 권한을 갖도록 하고 싶다면, 정책에 `before` 메서드를 정의하세요. `before` 메서드는 실제 정책 메서드가 호출되기 전에 실행되어 권한을 미리 부여할 수 있게 합니다. 보통 애플리케이션 관리자에게 모든 권한을 부여할 때 사용됩니다:

```
use App\Models\User;

/**
 * Perform pre-authorization checks.
 */
public function before(User $user, string $ability): bool|null
{
    if ($user->isAdministrator()) {
        return true;
    }

    return null;
}
```

특정 타입의 사용자에 대해 모두 권한을 거부하려면 `before` 메서드에서 `false`를 반환하면 됩니다. `null`을 반환하면 실제 정책 메서드로 권한 검사가 이어집니다.

> [!WARNING]  
> 정책 클래스에 검사하려는 능력 이름과 일치하는 메서드가 없으면, 정책의 `before` 메서드는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 이용한 액션 권한 부여

<a name="via-the-user-model"></a>
### User 모델을 통한 권한 부여

Laravel 애플리케이션에 포함된 `App\Models\User` 모델에는 액션 권한 부여에 편리한 `can`과 `cannot` 메서드가 있습니다. 이 메서드들은 권한을 체크하려는 액션 이름과 관련 모델을 받아 권한 여부를 불리언으로 반환합니다. 예를 들어, 아래 코드는 사용자가 주어진 `App\Models\Post` 모델을 수정할 권한이 있는지 확인하는 예시입니다. 보통 컨트롤러 내에서 사용합니다:

```
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

        // Update the post...

        return redirect('/posts');
    }
}
```

주어진 모델에 대해 [정책이 등록](#registering-policies)되어 있다면, `can` 메서드는 자동으로 해당 정책을 호출해 불리언 결과를 반환합니다. 만약 정책이 없다면, 같은 이름의 클로저 기반 게이트를 호출하려 시도합니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

`create` 같은 정책 메서드는 모델 인스턴스가 필요 없을 수 있습니다. 이때는 `can` 메서드에 클래스 이름을 전달해 어떤 정책을 사용할지 지정할 수 있습니다:

```
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

        // Create the post...

        return redirect('/posts');
    }
}
```

<a name="via-controller-helpers"></a>
### 컨트롤러 헬퍼를 통한 권한 부여

`App\Http\Controllers\Controller`를 상속받은 컨트롤러에서는 `authorize` 메서드를 사용해 권한 검사를 할 수 있습니다.

이 메서드는 검사할 액션 이름과 관련 모델을 인수로 받아, 권한이 없으면 `Illuminate\Auth\Access\AuthorizationException` 예외를 던집니다. Laravel 예외 핸들러가 이 예외를 받아 403 상태 코드를 가진 HTTP 응답을 자동으로 반환합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Update the given blog post.
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        $this->authorize('update', $post);

        // The current user can update the blog post...

        return redirect('/posts');
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

앞서 설명한 것처럼, `create` 같은 정책 메서드는 모델 인스턴스가 필요하지 않습니다. 이때는 클래스 이름을 넘겨 권한 부여할 정책을 지정해야 합니다:

```
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

/**
 * Create a new blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request): RedirectResponse
{
    $this->authorize('create', Post::class);

    // The current user can create blog posts...

    return redirect('/posts');
}
```

<a name="authorizing-resource-controllers"></a>
#### 리소스 컨트롤러 권한 부여

[리소스 컨트롤러](/docs/10.x/controllers#resource-controllers)를 사용할 때는 컨트롤러 생성자에서 `authorizeResource` 메서드를 호출해 각 리소스 컨트롤러 메서드에 적절한 `can` 미들웨어를 자동으로 연결할 수 있습니다.

`authorizeResource` 메서드는 첫 번째 인수로 모델 클래스 이름을, 두 번째 인수로 해당 모델 ID를 담는 라우트 / 요청 파라미터 이름을 받습니다. [--model] 플래그로 생성한 리소스 컨트롤러는 이를 위한 시그니처와 타입 힌트를 이미 포함합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;

class PostController extends Controller
{
    /**
     * Create the controller instance.
     */
    public function __construct()
    {
        $this->authorizeResource(Post::class, 'post');
    }
}
```

다음 컨트롤러 메서드들은 대응되는 정책 메서드에 매핑됩니다. 요청이 해당 컨트롤러 메서드에 라우팅되면, 정책 메서드가 자동으로 실행된 후 컨트롤러 메서드가 호출됩니다:

<div class="overflow-auto">

| 컨트롤러 메서드 | 정책 메서드 |
| --- | --- |
| index | viewAny |
| show | view |
| create | create |
| store | create |
| edit | update |
| update | update |
| destroy | delete |

</div>

> [!NOTE]  
> `make:policy` 명령어의 `--model` 옵션을 사용하면 특정 모델에 대한 정책 클래스가 빠르게 생성됩니다: `php artisan make:policy PostPolicy --model=Post`.

<a name="via-middleware"></a>
### 미들웨어를 통한 권한 부여

Laravel은 들어오는 요청이 라우트나 컨트롤러에 도달하기 전에 액션 권한을 검증하는 미들웨어를 포함합니다. 기본적으로 `Illuminate\Auth\Middleware\Authorize` 미들웨어가 `App\Http\Kernel` 클래스에서 `can` 키로 등록됩니다. 다음은 `can` 미들웨어를 사용해 사용자가 게시물을 수정할 권한이 있는지 확인하는 예시입니다:

```
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->middleware('can:update,post');
```

이 예제에서 `can` 미들웨어에 두 개의 인수를 전달했습니다. 첫 번째는 권한 부여할 액션 이름이고, 두 번째는 정책 메서드에 넘길 라우트 파라미터 이름입니다. 이 경우 [암묵적 모델 바인딩](/docs/10.x/routing#implicit-binding) 덕분에 `App\Models\Post` 모델 인스턴스가 정책 메서드로 전달됩니다. 사용자가 권한이 없으면 미들웨어가 403 상태 코드의 HTTP 응답을 반환합니다.

편의를 위해 다음처럼 `can` 메서드를 사용해 미들웨어를 라우트에 연결할 수도 있습니다:

```
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

`create` 같은 정책 메서드는 모델 인스턴스가 필요 없을 수 있습니다. 이때는 미들웨어에 클래스 이름을 전달해서 사용할 정책을 지정해야 합니다:

```
Route::post('/post', function () {
    // The current user may create posts...
})->middleware('can:create,App\Models\Post');
```

미들웨어 문자열에 전체 클래스 이름을 적는 것이 번거롭다면, `can` 메서드를 이용해 라우트에 미들웨어를 연결할 수 있습니다:

```
use App\Models\Post;

Route::post('/post', function () {
    // The current user may create posts...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿을 통한 권한 부여

Blade 템플릿에서 사용자가 특정 작업 권한이 있을 때에만 페이지 일부를 보여주고 싶을 때가 있습니다. 예를 들어, 사용자가 게시글을 실제로 수정할 수 있을 때만 수정 폼을 표시하고 싶을 수 있습니다. 이때 `@can`과 `@cannot` 디렉티브를 사용할 수 있습니다:

```blade
@can('update', $post)
    <!-- The current user can update the post... -->
@elsecan('create', App\Models\Post::class)
    <!-- The current user can create new posts... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- The current user cannot update the post... -->
@elsecannot('create', App\Models\Post::class)
    <!-- The current user cannot create new posts... -->
@endcannot
```

이 디렉티브는 `@if`와 `@unless` 문에 대한 편리한 축약입니다. 위의 `@can` 문은 아래와 동일합니다:

```blade
@if (Auth::user()->can('update', $post))
    <!-- The current user can update the post... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- The current user cannot update the post... -->
@endunless
```

한편, 배열에 담긴 여러 액션 중 하나라도 권한이 있으면 출력하는 문법도 있습니다. `@canany` 디렉티브를 사용하세요:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- The current user can update, view, or delete the post... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- The current user can create a post... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

대부분 권한 부여 메서드와 마찬가지로, 액션이 모델 인스턴스를 필요로 하지 않을 때는 `@can`과 `@cannot` 디렉티브에 클래스 이름을 넘겨서 정책을 지정할 수 있습니다:

```blade
@can('create', App\Models\Post::class)
    <!-- The current user can create posts... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- The current user can't create posts... -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 컨텍스트 전달하기

정책을 사용해 권한을 검사할 때, 여러 인수를 배열로 묶어 두 번째 인자로 전달할 수 있습니다. 이 배열의 첫 번째 요소는 정책이 적용될 모델이나 클래스를 지정하는 데 사용되고, 나머지 요소들은 정책 메서드가 권한 결정을 내릴 때 참조할 수 있는 추가 파라미터로 전달됩니다. 예를 들어 추가 `$category` 파라미터를 받는 `PostPolicy`의 `update` 메서드 정의는 다음과 같습니다:

```
/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post, int $category): bool
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```

이 정책 메서드를 호출해 권한을 검사하려면 다음처럼 배열로 인수를 넘길 수 있습니다:

```
/**
 * Update the given blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post): RedirectResponse
{
    $this->authorize('update', [$post, $request->category]);

    // The current user can update the blog post...

    return redirect('/posts');
}
```