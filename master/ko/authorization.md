# 권한 부여(Authorization)

- [소개](#introduction)
- [게이트(Gates)](#gates)
    - [게이트 작성하기](#writing-gates)
    - [게이트를 통한 액션 권한 확인](#authorizing-actions-via-gates)
    - [게이트 응답](#gate-responses)
    - [게이트 체크 가로채기](#intercepting-gate-checks)
    - [인라인 권한 확인](#inline-authorization)
- [정책 생성하기](#creating-policies)
    - [정책 생성](#generating-policies)
    - [정책 등록](#registering-policies)
- [정책 작성하기](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델이 없는 메서드](#methods-without-models)
    - [게스트 사용자](#guest-users)
    - [정책 필터](#policy-filters)
- [정책으로 액션 권한 부여](#authorizing-actions-using-policies)
    - [User 모델을 통해](#via-the-user-model)
    - [Gate 퍼사드를 통해](#via-the-gate-facade)
    - [미들웨어를 통해](#via-middleware)
    - [Blade 템플릿을 통해](#via-blade-templates)
    - [추가 컨텍스트 제공](#supplying-additional-context)
- [Authorization & Inertia](#authorization-and-inertia)

<a name="introduction"></a>
## 소개

Laravel은 기본 [인증](/docs/{{version}}/authentication) 서비스뿐만 아니라, 주어진 리소스에 대해 사용자의 액션을 권한 부여할 수 있는 간단한 방법도 제공합니다. 예를 들어, 사용자가 인증되어 있어도, 모든 Eloquent 모델이나 데이터베이스 레코드를 수정하거나 삭제할 권한이 없을 수 있습니다. Laravel의 권한 부여 기능은 이러한 권한 체크를 쉽고 체계적으로 관리할 수 있게 지원합니다.

Laravel은 액션을 권한 부여하는 두 가지 주요 방법을 제공합니다: [게이트(Gate)](#gates)와 [정책(Policy)](#creating-policies)입니다. 게이트와 정책은 각각 라우트(route)와 컨트롤러(controller)에 비유할 수 있습니다. 게이트는 간단하고 클로저 기반의 권한 방식이며, 정책은 컨트롤러처럼 특정 모델이나 리소스를 기준으로 권한 로직을 그룹화합니다. 이 문서에서는 먼저 게이트를 살펴본 후, 정책에 대해 설명합니다.

애플리케이션 구축 시 게이트만 또는 정책만 반드시 사용해야 하는 것은 아닙니다. 대부분의 애플리케이션은 게이트와 정책이 혼합되어 사용됩니다. 게이트는 관리자 대시보드 보기처럼 모델이나 리소스와 직접적으로 관련 없는 액션에 적용하는 것이 적합합니다. 반면, 정책은 특정 모델이나 리소스에 대해 액션을 권한 부여할 때 사용해야 합니다.

<a name="gates"></a>
## 게이트(Gates)

<a name="writing-gates"></a>
### 게이트 작성하기

> [!WARNING]
> 게이트는 라라벨 권한 부여 기능의 기본 개념을 배우기에 좋은 방법이지만, 본격적인 애플리케이션을 구축할 때는 권한 규칙을 관리하기 위해 [정책(Policy)](#creating-policies) 사용을 권장합니다.

게이트는 단순히 클로저로, 사용자가 특정 액션을 수행할 권한이 있는지 여부를 판단합니다. 일반적으로 게이트는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `Gate` 퍼사드를 사용하여 정의합니다. 게이트는 항상 첫 번째 인자로 사용자 인스턴스를 받고, 필요에 따라 관련된 Eloquent 모델 같은 추가 인자를 받을 수 있습니다.

아래 예제에서는 사용자가 특정 `App\Models\Post` 모델을 업데이트할 수 있는지 판단하는 게이트를 정의합니다. 이 게이트는 사용자의 `id`와 게시글을 생성한 사용자의 `user_id`를 비교해 권한을 판단합니다.

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

컨트롤러처럼, 게이트 또한 클래스 콜백 배열을 사용하여 정의할 수 있습니다:

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
### 액션 권한 확인

게이트를 사용하여 액션을 권한 부여하려면, `Gate` 퍼사드에서 제공하는 `allows` 또는 `denies` 메서드를 사용하면 됩니다. 현재 인증된 사용자를 이 메서드에 직접 전달할 필요는 없습니다. Laravel이 자동으로 사용자를 게이트 클로저에 전달해줍니다. 보통 컨트롤러 내에서 권한이 필요한 액션을 수행하기 전에 게이트 권한 메서드가 호출됩니다.

```php
<?php

namespace App\Http\Controllers;

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

        // 게시글 업데이트 코드...

        return redirect('/posts');
    }
}
```

현재 인증된 사용자가 아닌 다른 사용자의 권한을 확인하고 싶다면, `Gate` 퍼사드의 `forUser` 메서드를 사용할 수 있습니다.

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // 해당 사용자는 게시글을 업데이트할 수 있습니다...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // 해당 사용자는 게시글을 업데이트할 수 없습니다...
}
```

`any` 또는 `none` 메서드를 사용하여 여러 액션을 한 번에 권한 체크할 수도 있습니다.

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // 해당 사용자는 게시글을 업데이트 또는 삭제할 수 있습니다...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // 해당 사용자는 게시글을 업데이트 또는 삭제할 수 없습니다...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 예외 발생과 함께 권한 확인하기

권한 확인을 시도하고, 액션이 허용되지 않을 경우 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 던지려면 `Gate` 퍼사드의 `authorize` 메서드를 사용하세요. `AuthorizationException` 인스턴스는 Laravel에 의해 자동으로 403 HTTP 응답으로 변환됩니다.

```php
Gate::authorize('update-post', $post);

// 액션이 허용된 경우...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 제공

권한 확인 메서드(`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`)와 권한 [Blade 지시어](#via-blade-templates)(`@can`, `@cannot`, `@canany`)의 두 번째 인자에는 배열을 전달할 수 있습니다. 이 배열의 요소들은 게이트 클로저의 파라미터로 전달되어, 권한 결정 시 추가 컨텍스트로 활용할 수 있습니다.

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
    // 사용자는 게시글을 생성할 수 있습니다...
}
```

<a name="gate-responses"></a>
### 게이트 응답

지금까지는 게이트가 단순한 불리언 값을 반환하는 경우만 살펴보았습니다. 하지만, 더 자세한 응답(오류 메시지 포함 등)이 필요하다면, 게이트에서 `Illuminate\Auth\Access\Response`를 반환할 수 있습니다.

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::deny('관리자 권한이 필요합니다.');
});
```

게이트에서 권한 응답을 반환하더라도, `Gate::allows` 메서드는 여전히 불리언 값을 반환합니다. 전체 권한 응답을 얻으려면 `Gate::inspect` 메서드를 사용하세요.

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // 액션이 허용됨...
} else {
    echo $response->message();
}
```

`Gate::authorize`를 사용할 때(액션이 허용되지 않으면 `AuthorizationException`을 던짐), 반환되는 에러 메시지는 HTTP 응답에 전달됩니다.

```php
Gate::authorize('edit-settings');

// 액션이 허용됨...
```

<a name="customizing-gate-response-status"></a>
#### HTTP 응답 상태 커스터마이즈

게이트에서 액션이 거부되면, 기본적으로 `403` HTTP 응답이 반환됩니다. 그러나 경우에 따라 다른 상태 코드를 반환해야 할 수 있습니다. 이럴 때는 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용하세요.

```php
use App\Models.User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::denyWithStatus(404);
});
```

`404` 응답으로 리소스를 숨기는 패턴이 흔하기 때문에, `denyAsNotFound` 메서드를 사용할 수도 있습니다.

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
### 게이트 체크 가로채기

특정 사용자에게 모든 권한을 부여하고 싶을 때가 있습니다. 이럴 때는, 모든 권한 체크 전에 실행될 클로저를 `before` 메서드로 정의하세요.

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저에서 non-null 값을 반환하면, 그 결과가 최종 권한 체크 결과로 간주됩니다.

모든 권한 체크 이후에 클로저를 실행하려면 `after` 메서드를 사용할 수 있습니다.

```php
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after` 클로저에서 반환하는 값은 게이트나 정책에서 `null`이 반환된 경우를 제외하고 권한 결과를 덮어쓰지 않습니다.

<a name="inline-authorization"></a>
### 인라인 권한 확인

때로는, 특정 액션에 대응되는 별도의 게이트 없이 현재 인증된 사용자가 액션을 수행할 권한이 있는지 확인하고 싶을 수 있습니다. 이러한 "인라인" 권한 체크는 `Gate::allowIf` 및 `Gate::denyIf` 메서드를 통해 수행할 수 있습니다. 인라인 권한 확인은 ["before" 또는 "after" 권한 훅](#intercepting-gate-checks)을 실행하지 않습니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

액션이 허용되지 않거나 인증된 사용자가 없는 경우, Laravel은 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 던집니다. 이 예외는 Laravel의 예외 핸들러에 의해 자동으로 403 HTTP 응답으로 변환됩니다.

<a name="creating-policies"></a>
## 정책(Policy) 생성하기

<a name="generating-policies"></a>
### 정책 생성

정책은 특정 모델이나 리소스를 기준으로 권한 로직을 그룹화하는 클래스입니다. 예를 들어, 애플리케이션이 블로그라면, `App\Models\Post` 모델과 사용자의 포스트 작성이나 수정 권한 등을 담당하는 `App\Policies\PostPolicy` 정책이 있을 수 있습니다.

정책은 `make:policy` 아티즌 명령어를 사용하여 생성할 수 있습니다. 생성된 정책은 `app/Policies` 디렉토리에 위치하게 됩니다. 해당 디렉토리가 없으면 Laravel이 자동으로 생성해줍니다.

```shell
php artisan make:policy PostPolicy
```

`make:policy` 명령은 빈 정책 클래스를 생성합니다. 리소스의 조회, 생성, 수정, 삭제 관련 예제 메서드가 포함된 클래스를 생성하려면, 명령 실행 시 `--model` 옵션을 추가하세요.

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록

<a name="policy-discovery"></a>
#### 정책 자동 발견

기본적으로, Laravel은 모델과 정책이 표준 네이밍 컨벤션을 따르면 자동으로 정책을 찾습니다. 정책은 모델이 위치한 디렉토리 이하 혹은 그 이상 경로의 `Policies` 디렉토리에 있어야 합니다. 예를 들어, 모델은 `app/Models`에, 정책은 `app/Policies`에 둘 수 있습니다. Laravel은 `app/Models/Policies`, 그다음에 `app/Policies` 순으로 정책을 확인합니다. 그리고 정책명은 반드시 모델명 + `Policy` 접미사가 붙어야 합니다. 예를 들어 `User` 모델에 대응하는 정책 클래스는 `UserPolicy`가 됩니다.

정책 자동 발견 규칙을 커스터마이즈하고 싶다면, `Gate::guessPolicyNamesUsing` 메서드를 사용해 커스텀 콜백을 등록할 수 있습니다. 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출해야 합니다.

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // 주어진 모델에 대한 정책 클래스명을 반환...
});
```

<a name="manually-registering-policies"></a>
#### 정책 직접 등록

`Gate` 퍼사드를 사용해 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 모델과 정책을 수동으로 등록할 수도 있습니다.

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

정책 클래스가 등록되면, 각 액션에 대해 메서드를 추가할 수 있습니다. 예를 들어, `App\Models\User`가 `App\Models\Post` 인스턴스를 수정할 수 있는지 판단하는 `update` 메서드를 정의해보겠습니다.

`update` 메서드는 `User`와 `Post` 인스턴스를 인자로 받아, 해당 사용자가 특정 포스트를 수정할 권한이 있는지 `true`/`false`를 반환해야 합니다. 예제에서는 사용자 `id`와 포스트의 `user_id`를 비교합니다.

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

정책이 허용하는 다양한 액션별로 추가 메서드를 정의할 수 있습니다. 예를 들어, `view`나 `delete` 같은 메서드를 자유롭게 추가할 수 있으며, 메서드명도 자유롭게 지정할 수 있습니다.

Artisan 콘솔에서 정책 생성 시 `--model` 옵션을 사용했다면, `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 액션에 대한 메서드가 이미 포함된 정책이 생성됩니다.

> [!NOTE]
> 모든 정책은 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 생성자에 필요한 의존성 주입도 가능합니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지는 단순한 불리언을 반환하는 정책 기본형만 살펴보았습니다. 좀 더 자세한 응답(에러 메시지 등)을 원한다면, 정책 메서드에서 `Illuminate\Auth\Access\Response` 인스턴스를 반환할 수 있습니다.

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
        : Response::deny('이 게시글의 소유자가 아닙니다.');
}
```

정책에서 권한 응답을 반환해도, `Gate::allows`는 여전히 불리언만 반환합니다. 전체 권한 응답이 필요하면 `Gate::inspect`를 사용하세요.

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // 액션 허용됨...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드도 사용할 경우, 반환된 에러 메시지가 HTTP 응답에 전달됩니다.

```php
Gate::authorize('update', $post);

// 액션 허용됨...
```

<a name="customizing-policy-response-status"></a>
#### HTTP 응답 상태 커스터마이즈

정책 메서드를 통해 액션이 거부되면, 기본적으로 `403` HTTP 응답이 반환됩니다. 하지만 실행 실패 시 다른 HTTP 상태 코드를 반환해야 할 수도 있습니다. 이럴 땐 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus`를 사용하세요.

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

`404` 응답을 통해 리소스를 숨기는 패턴이 흔하기 때문에, `denyAsNotFound` 메서드를 사용할 수도 있습니다.

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
### 모델이 없는 메서드

일부 정책 메서드는 현재 인증된 사용자 인스턴스만 인자로 받을 때도 있습니다. 일반적으로 `create` 같은 액션에서 이렇게 합니다. 예를 들어, 블로그에서 사용자가 게시글을 생성할 권한이 있는지 확인해야 할 때, 정책 메서드는 사용자 인스턴스만 받도록
정의합니다.

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

기본적으로 인증되지 않은 사용자가 요청을 보낼 경우, 모든 게이트와 정책은 자동으로 `false`를 반환합니다. 그러나 사용자 인자를 선택적(nullable)로 선언하거나, 기본값으로 `null`을 주면 이러한 권한 체크도 가능해집니다.

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

특정 사용자에게 정책 내 모든 액션을 허용하고 싶을 수도 있습니다. 이럴 때는 `before` 메서드를 정책에 정의하세요. 이 메서드는 정책 내 다른 어떤 메서드보다 먼저 실행되어 해당 액션을 미리 권한 부여할 기회를 제공합니다. 주로 관리자에게 모든 액션을 허용할 때 사용합니다.

```php
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

특정 유형의 사용자에게 모든 권한을 거부하려면, `before` 메서드에서 `false`를 반환하세요. `null`을 반환하면 정책 메서드로 처리가 넘어갑니다.

> [!WARNING]
> 정책 클래스에 정책 메서드(ability 이름과 일치하는 메서드)가 없는 경우 `before`는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 사용한 액션 권한 부여

<a name="via-the-user-model"></a>
### User 모델을 통해

Laravel의 기본 `App\Models\User` 모델에는 `can`, `cannot` 메서드가 포함되어 있습니다. 이 둘은 권한을 확인할 액션명과 관련 모델(또는 클래스명)을 인자로 받습니다. 예를 들어, 사용자가 특정 `App\Models\Post`를 수정할 권한이 있는지 확인하려면 보통 아래와 같이 컨트롤러에서 수행합니다.

```php
<?php

namespace App\Http\Controllers;

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

주어진 모델에 [정책이 등록](#registering-policies)되어 있다면, `can` 메서드는 자동으로 해당 정책을 호출합니다. 정책이 없다면 동명의 클로저 기반 게이트를 실행합니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델이 필요없는 액션

일부 액션은 `create`처럼 실제 모델 인스턴스가 필요 없는 정책 메서드에 해당할 수 있습니다. 이럴 땐 클래스명을 `can`에 전달하세요. 어떤 정책을 참조할지 클래스명을 활용해 결정합니다.

```php
<?php

namespace App\Http\Controllers;

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
### Gate 퍼사드로

`App\Models\User` 모델의 메서드 외에도, `Gate` 퍼사드의 `authorize` 메서드를 사용할 수 있습니다.

`can`과 마찬가지로, 권한을 확인할 액션 명과 관련 모델을 인자로 전달합니다. 만약 권한이 허용되지 않을 경우, `authorize`는 `Illuminate\Auth\Access\AuthorizationException`을 던지며, 이 예외는 403 상태 코드의 HTTP 응답으로 변환됩니다.

```php
<?php

namespace App\Http\Controllers;

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

        // 현재 사용자는 블로그 게시글을 수정 가능...

        return redirect('/posts');
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

앞서 설명했듯이, 어떤 정책 메서드(예: `create`)는 실제 모델 인스턴스가 필요 없습니다. 이럴 땐 클래스명을 `authorize`에 전달해 어떤 정책을 사용할지 결정합니다.

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

    // 현재 사용자는 블로그 게시글을 작성 가능...

    return redirect('/posts');
}
```

<a name="via-middleware"></a>
### 미들웨어로

Laravel에는 요청이 라우트 혹은 컨트롤러에 도달하기 전 액션 권한을 부여할 수 있는 미들웨어가 포함되어 있습니다. 기본적으로, `Illuminate\Auth\Middleware\Authorize` 미들웨어는 Laravel에 의해 자동 등록된 `can` [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)을 통해 라우트에 부착할 수 있습니다. 예를 들어, 사용자가 게시글을 수정할 수 있는지를 `can` 미들웨어로 확인할 수 있습니다.

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 게시글을 수정 가능...
})->middleware('can:update,post');
```

위 예제에서 `can` 미들웨어에 두 가지 인자를 넘깁니다. 첫 번째는 권한 부여를 확인할 액션명, 두 번째는 정책 메서드에 전달할 라우트 파라미터입니다. [암시적 모델 바인딩](/docs/{{version}}/routing#implicit-binding)이 적용되어 있으므로, `App\Models\Post` 모델이 정책 메서드에 전달됩니다. 사용자가 액션을 수행할 권한이 없다면, 미들웨어가 403 상태 코드를 가진 HTTP 응답을 반환합니다.

`can` 미들웨어를 라우트에 부착하는 다른 방법으로 `can` 메서드를 사용할 수도 있습니다.

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 게시글을 수정 가능...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

다시, `create` 등 일부 정책 메서드는 모델 인스턴스가 필요 없습니다. 이럴 때는 미들웨어에 클래스명을 문자열로 지정하면 됩니다. 이 클래스명으로 참조할 정책을 결정합니다.

```php
Route::post('/post', function () {
    // 현재 사용자가 게시글을 작성 가능...
})->middleware('can:create,App\Models\Post');
```

미들웨어 정의에서 전체 클래스명을 문자열로 쓰는 것이 번거로울 수 있으므로, `can` 메서드를 사용하는 게 더 편리할 수 있습니다.

```php
use App\Models\Post;

Route::post('/post', function () {
    // 현재 사용자가 게시글을 작성 가능...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿에서

Blade 템플릿에서, 특정 액션에 대해 사용자가 권한이 있을 때만 페이지 일부를 보여주고 싶을 수 있습니다. 예를 들어, 현재 사용자가 게시글을 수정할 수 있는 경우에만 수정 폼을 보여주고 싶다면 `@can`, `@cannot` 지시어를 사용하세요.

```blade
@can('update', $post)
    <!-- 현재 사용자가 게시글을 수정 가능... -->
@elsecan('create', App\Models\Post::class)
    <!-- 현재 사용자가 새 게시글을 작성 가능... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- 현재 사용자가 게시글을 수정 불가... -->
@elsecannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 새 게시글을 작성할 수 없음... -->
@endcannot
```

이러한 지시어는 `@if`, `@unless` 문법의 편리한 축약입니다. 위의 `@can`/`@cannot` 구문은 아래와 동일합니다.

```blade
@if (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 수정 가능... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 수정할 수 없음... -->
@endunless
```

여러 액션 중 하나라도 권한이 있는지를 확인하려면 `@canany` 지시어를 사용하세요.

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- 현재 사용자가 게시글을 수정, 조회, 삭제 가능... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성 가능... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

다른 권한 체크 방법과 마찬가지로, 액션이 모델 인스턴스를 필요로 하지 않으면 클래스명을 `@can`, `@cannot`에 넘길 수 있습니다.

```blade
@can('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글 작성 가능... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글 작성 불가... -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 컨텍스트 제공

정책을 사용해 액션 권한을 체크할 때, 두 번째 인자로 배열을 전달할 수 있습니다. 배열의 첫 번째 요소는 어떤 정책을 사용할지 결정하며, 나머지 요소들은 정책 메서드의 추가 파라미터로 전달되어, 권한 결정에 필요한 추가 컨텍스트로 활용됩니다. 아래는 `$category` 추가 파라미터가 있는 `PostPolicy`의 예시입니다.

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

인증된 사용자가 해당 게시글을 수정할 수 있는지 정책 메서드를 호출하려면 다음과 같이 합니다.

```php
/**
 * Update the given blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post): RedirectResponse
{
    Gate::authorize('update', [$post, $request->category]);

    // 현재 사용자가 블로그 게시글을 수정 가능...

    return redirect('/posts');
}
```

<a name="authorization-and-inertia"></a>
## 권한과 Inertia

권한 부여는 항상 서버에서 처리해야 하지만, 프론트엔드 애플리케이션에서 UI를 적절히 렌더링하기 위해 권한 데이터를 미리 제공하는 것이 편리할 수 있습니다. Laravel은 Inertia 기반 프론트엔드에 권한 정보를 노출하는 필수 규칙을 정의하지는 않습니다.

하지만, Inertia 기반 [스타터 키트](/docs/{{version}}/starter-kits)를 사용하는 경우, 애플리케이션에는 이미 `HandleInertiaRequests` 미들웨어가 포함되어 있습니다. 이 미들웨어의 `share` 메서드에서 모든 Inertia 페이지에 공유할 데이터를 반환할 수 있습니다. 이 공유 데이터는 사용자 권한 정보를 정의하기에 편리한 위치를 제공합니다.

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
     * Define the props that are shared by default.
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