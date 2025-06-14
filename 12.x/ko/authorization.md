# 인가 (Authorization)

- [소개](#introduction)
- [게이트(Gates)](#gates)
    - [게이트 작성하기](#writing-gates)
    - [동작 인가하기](#authorizing-actions-via-gates)
    - [게이트 응답](#gate-responses)
    - [게이트 검사 가로채기](#intercepting-gate-checks)
    - [인라인 인가](#inline-authorization)
- [정책 생성하기](#creating-policies)
    - [정책 생성](#generating-policies)
    - [정책 등록](#registering-policies)
- [정책 작성하기](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델이 없는 메서드](#methods-without-models)
    - [게스트 사용자](#guest-users)
    - [정책 필터](#policy-filters)
- [정책을 사용한 동작 인가](#authorizing-actions-using-policies)
    - [User 모델을 통한 인가](#via-the-user-model)
    - [Gate 파사드를 통한 인가](#via-the-gate-facade)
    - [미들웨어를 통한 인가](#via-middleware)
    - [Blade 템플릿을 통한 인가](#via-blade-templates)
    - [추가 정보 전달하기](#supplying-additional-context)
- [Authorization & Inertia](#authorization-and-inertia)

<a name="introduction"></a>
## 소개

라라벨은 기본 내장된 [인증](/docs/12.x/authentication) 기능 외에도, 사용자가 특정 리소스에 대해 동작을 수행할 수 있는지 간단하게 인가(Authorization)할 수 있는 방법을 제공합니다. 예를 들어, 사용자가 인증되었다고 해도, 애플리케이션에서 관리하는 특정 Eloquent 모델 또는 데이터베이스 레코드를 수정하거나 삭제할 권한이 없을 수도 있습니다. 라라벨의 인가 기능은 이러한 인가 검사를 쉽고, 체계적으로 관리할 수 있는 방법을 제공합니다.

라라벨에서는 동작 인가를 위한 두 가지 주요 방법, [게이트(Gate)](#gates)와 [정책(Policy)](#creating-policies)를 제공합니다. 게이트와 정책을 각각 라우트(route)와 컨트롤러(controller)로 생각하면 이해하기 쉽습니다. 게이트는 클로저(익명 함수)를 이용한 간단한 인가 검사를 제공하며, 정책은 컨트롤러처럼 특정 모델이나 리소스와 관련된 인가 로직을 묶어서 관리할 수 있습니다. 이 문서에서는 게이트를 먼저 설명한 뒤, 정책에 대해 살펴봅니다.

애플리케이션을 개발할 때 게이트 또는 정책 중 하나만 반드시 선택해서 사용해야 하는 것은 아닙니다. 실제로 대부분의 애플리케이션에서는 게이트와 정책을 혼합해서 사용하며, 이렇게 해도 전혀 문제가 없습니다. 게이트는 관리자 대시보드 보기처럼 특정 모델이나 리소스와 직접적인 연관이 없는 동작을 인가할 때 특히 유용합니다. 반면, 특정 모델이나 리소스에 대한 인가가 필요하다면 정책을 사용하는 것이 적합합니다.

<a name="gates"></a>
## 게이트(Gate)

<a name="writing-gates"></a>
### 게이트 작성하기

> [!WARNING]
> 게이트는 라라벨의 인가 기능을 배우기에 좋은 출발점이지만, 실전 애플리케이션에서는 인가 규칙을 더 체계적으로 관리할 수 있도록 [정책(Policy)](#creating-policies)를 사용하는 것이 좋습니다.

게이트는 기본적으로 사용자가 특정 동작을 수행할 수 있는지 여부를 판단하는 클로저(익명 함수)입니다. 일반적으로 게이트는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `Gate` 파사드를 사용해 정의합니다. 게이트는 첫 번째 인수로 무조건 사용자 인스턴스를 전달받고, 필요에 따라 Eloquent 모델 등 추가 인수도 받을 수 있습니다.

예를 들어, 특정 `App\Models\Post` 모델을 사용자가 수정할 수 있는지 확인하는 게이트를 정의해보겠습니다. 여기서는 사용자의 `id`와 게시글을 만든 사용자의 `user_id`를 비교해서 인가를 판단합니다:

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

컨트롤러와 마찬가지로, 게이트도 클래스 콜백 배열로 정의할 수도 있습니다:

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
### 동작 인가하기

게이트를 사용해 동작을 인가하려면, `Gate` 파사드에서 제공하는 `allows` 또는 `denies` 메서드를 사용하면 됩니다. 이때, 현재 인증된 사용자를 직접 전달할 필요는 없습니다. 라라벨이 자동으로 현재 사용자를 게이트 클로저에 넘겨줍니다. 인가가 필요한 동작을 수행하기 전에, 애플리케이션의 컨트롤러 등에서 게이트 인가 메서드를 호출하는 것이 일반적입니다:

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

        // Update the post...

        return redirect('/posts');
    }
}
```

현재 인증된 사용자 외의 다른 사용자가 특정 동작을 수행할 수 있는지 확인하려면, `Gate` 파사드의 `forUser` 메서드를 사용할 수 있습니다:

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // The user can update the post...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // The user can't update the post...
}
```

여러 동작을 한 번에 인가해야 한다면, `any` 혹은 `none` 메서드를 사용할 수 있습니다:

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // The user can update or delete the post...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // The user can't update or delete the post...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 인가 또는 예외 발생시키기

동작 인가 시도를 하면서, 인가되지 않은 경우에 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외가 발생하도록 하고 싶다면, `Gate` 파사드의 `authorize` 메서드를 사용하면 됩니다. 이 예외는 라라벨에 의해 자동으로 403 HTTP 응답으로 변환됩니다:

```php
Gate::authorize('update-post', $post);

// The action is authorized...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 정보 전달하기

동작 인가를 위한 게이트 메서드(`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`)와 인가 관련 [Blade 디렉티브](#via-blade-templates)(`@can`, `@cannot`, `@canany`)는 두 번째 인수로 배열을 받을 수 있습니다. 이 배열의 값들은 게이트 클로저의 파라미터로 순서대로 전달되며, 인가 결정에 필요한 추가 정보를 넘길 때 사용할 수 있습니다:

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
    // The user can create the post...
}
```

<a name="gate-responses"></a>
### 게이트 응답

지금까지 살펴본 게이트는 단순히 불(boolean) 값만 반환했습니다. 그러나 경우에 따라 더 자세한 응답(예: 에러 메시지 등)이 필요할 수도 있습니다. 이를 위해 게이트에서 `Illuminate\Auth\Access\Response` 객체를 반환할 수 있습니다:

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

이렇게 게이트에서 인가 응답을 반환하더라도, `Gate::allows` 메서드는 여전히 단순한 불린 값을 반환합니다. 다만, `Gate::inspect` 메서드를 이용하면 게이트에서 반환된 전체 인가 응답 객체를 받아올 수 있습니다:

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

동작이 인가되지 않았을 때 예외가 발생하며, 예외의 에러 메시지로 게이트의 메시지가 전달되게 하려면 `Gate::authorize` 메서드를 사용하면 됩니다:

```php
Gate::authorize('edit-settings');

// The action is authorized...
```

<a name="customizing-gate-response-status"></a>
#### HTTP 응답 상태 커스터마이즈

게이트를 통해 동작이 거부되면, 기본적으로 `403` HTTP 응답이 반환됩니다. 하지만 경우에 따라 다른 HTTP 상태 코드를 반환하고 싶을 때는 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용해 실패 시 반환할 상태 코드를 지정할 수 있습니다:

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

보안을 위해 `404` 응답으로 리소스를 숨기는 패턴이 웹 애플리케이션에서 자주 쓰이기 때문에, 이를 간편하게 적용할 수 있도록 `denyAsNotFound` 메서드도 제공합니다:

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

특정 사용자에게는 모든 동작에 대해 인가를 부여하고 싶을 수도 있습니다. 이럴 때는 `before` 메서드를 사용해, 모든 인가 검사 전에 실행되는 클로저를 정의할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저에서 `null`이 아닌 값을 반환하면, 그 값이 바로 인가 검사 결과로 사용됩니다.

모든 인가 검사 이후에 추가 처리를 하고 싶다면, `after` 메서드를 통해 클로저를 정의할 수 있습니다:

```php
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after` 클로저가 반환하는 값은 게이트나 정책이 `null`을 반환한 경우에만 최종 인가 결과에 영향을 미칩니다. 기존에 `true`나 `false`가 반환된 경우에는 덮어쓰지 않습니다.

<a name="inline-authorization"></a>
### 인라인 인가

가끔씩, 특정 동작을 위해 별도의 게이트를 만들지 않고, 현재 인증된 사용자가 그 동작을 수행할 수 있는지 간단하게 확인하고 싶을 수도 있습니다. 라라벨에서는 `Gate::allowIf` 및 `Gate::denyIf` 메서드를 사용해 이런 "인라인 인가" 검사를 수행할 수 있습니다. 인라인 인가는 [before/after 후크](#intercepting-gate-checks)를 실행하지 않습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

해당 동작에 권한이 없거나, 인증된 사용자가 없다면, 라라벨은 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시킵니다. 이 예외는 라라벨 예외 핸들러에 의해 403 HTTP 응답으로 처리됩니다.

<a name="creating-policies"></a>
## 정책 생성하기

<a name="generating-policies"></a>
### 정책 생성

정책(Policy)은 특정 모델이나 리소스 중심으로 인가 로직을 정리하는 클래스입니다. 예를 들어, 블로그 애플리케이션이라면 `App\Models\Post` 모델에 대한 사용자 동작(글 작성, 수정 등)을 인가하기 위한 `App\Policies\PostPolicy` 클래스를 만들 수 있습니다.

아티즌 Artisan의 `make:policy` 명령어를 사용해 정책 클래스를 생성할 수 있습니다. 생성된 정책 클래스는 `app/Policies` 디렉토리에 저장됩니다. 만약 해당 디렉토리가 없다면 라라벨이 자동으로 만들어줍니다:

```shell
php artisan make:policy PostPolicy
```

`make:policy` 명령은 비어 있는 정책 클래스를 생성합니다. 리소스의 `view`, `create`, `update`, `delete`와 같은 인가 관련 예시 메서드를 포함한 클래스를 생성하려면, 명령 실행 시 `--model` 옵션을 추가할 수 있습니다:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록

<a name="policy-discovery"></a>
#### 정책 자동 연결(Policy Discovery)

기본적으로 라라벨은 모델과 정책이 표준 네이밍 규칙을 따른다면 자동으로 정책을 연결(발견)합니다. 구체적으로, 정책은 모델이 위치한 디렉터리와 같거나 그보다 상위 경로의 `Policies` 디렉토리에 있어야 합니다. 예를 들어, 모델이 `app/Models` 디렉토리에 있다면, 정책은 `app/Policies`에 둘 수 있습니다. 라라벨은 정책을 찾을 때 `app/Models/Policies`와 `app/Policies`를 순서대로 확인합니다. 또한, 정책 클래스의 이름은 모델명과 같고 뒤에 `Policy`가 붙어야 합니다. 따라서 `User` 모델이라면 정책명은 `UserPolicy`가 됩니다.

정책 자동 연결 방식을 직접 정의하고 싶다면, `Gate::guessPolicyNamesUsing` 메서드를 사용해 커스텀 콜백을 등록할 수 있습니다. 보통 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // Return the name of the policy class for the given model...
});
```

<a name="manually-registering-policies"></a>
#### 정책 수동 등록

`Gate` 파사드를 이용해서, 정책과 해당 모델을 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 수동으로 연결(등록)할 수도 있습니다:

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

또는, 모델 클래스에 `UsePolicy` 속성을 부여해 해당 모델에 대응하는 정책을 라라벨에 알려줄 수도 있습니다:

```php
<?php

namespace App\Models;

use App\Policies\OrderPolicy;
use Illuminate\Database\Eloquent\Attributes\UsePolicy;
use Illuminate\Database\Eloquent\Model;

#[UsePolicy(OrderPolicy::class)]
class Order extends Model
{
    //
}
```

<a name="writing-policies"></a>
## 정책 작성하기

<a name="policy-methods"></a>
### 정책 메서드

정책 클래스가 등록되면, 해당 정책이 관리하는 각 동작에 대한 메서드를 작성할 수 있습니다. 예를 들어, `App\Models\User`가 특정 `App\Models\Post` 인스턴스를 수정할 수 있는지 판단하는 `update` 메서드를 `PostPolicy`에 정의해봅니다.

`update` 메서드는 `User` 인스턴스와 `Post` 인스턴스를 인수로 받아, 해당 사용자가 주어진 게시물을 수정할 권한이 있는지 `true`(인가됨) 또는 `false`(인가됨 아님)로 반환해야 합니다. 아래 예시에서는 사용자의 `id`가 게시글의 `user_id`와 같은지 비교합니다:

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

정책이 인가해야 하는 다양한 동작에 따라, 메서드를 계속 추가하면 됩니다. 예를 들어, `view`, `delete` 등 다양한 동작별로 메서드를 만들 수 있고, 메서드 이름은 자유롭게 정할 수 있습니다.

만약 아티즌 콘솔에서 정책 생성 시 `--model` 옵션을 사용했다면, 생성된 클래스에는 이미 `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 등의 동작별 메서드가 포함되어 있습니다.

> [!NOTE]
> 모든 정책은 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 해석되므로, 필요하다면 생성자에 의존성 주입을 위한 타입힌트를 자유롭게 사용할 수 있습니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지 살펴본 정책 메서드는 단순히 불린 값을 반환했습니다. 하지만 상황에 따라 에러 메시지 등 더 자세한 응답을 원할 수도 있습니다. 이럴 때는 정책 메서드에서 `Illuminate\Auth\Access\Response` 객체를 반환할 수 있습니다:

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

정책에서 인가 응답 객체를 반환하더라도, `Gate::allows` 메서드는 항상 bool 값만을 반환합니다. Gate에서 전체 인가 응답 객체를 받으려면 `Gate::inspect` 메서드를 활용하세요:

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

인가되지 않은 경우 예외와 함께 메시지가 HTTP 응답으로 전달되길 원한다면, `Gate::authorize` 메서드를 사용할 수 있습니다:

```php
Gate::authorize('update', $post);

// The action is authorized...
```

<a name="customizing-policy-response-status"></a>
#### HTTP 응답 상태 커스터마이즈

정책 메서드를 통해 동작이 거부될 때는 기본적으로 `403` HTTP 응답이 반환됩니다. 하지만 경우에 따라 다른 HTTP 상태 코드를 반환하고 싶다면, `Illuminate\Auth\Access\Response`의 `denyWithStatus` 정적 생성자를 사용해 실패 시 원하는 상태 코드를 반환할 수 있습니다:

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

웹 애플리케이션에서 특정 리소스를 숨기기 위해 `404` 응답을 보내는 경우가 많으므로, 간편하게 사용할 수 있도록 `denyAsNotFound` 메서드를 제공합니다:

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

일부 정책 메서드는 현재 인증된 사용자 인스턴스만을 인수로 받기도 합니다. 이 경우는 주로 `create` 동작을 인가할 때 자주 등장합니다. 예를 들어, 블로그에서 사용자가 새 글을 작성할 권한이 있는지 확인하려면, 다음처럼 메서드를 작성합니다:

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

기본적으로, 인증되지 않은 사용자가 요청할 경우 모든 게이트와 정책은 자동으로 `false`(인가 불가)를 반환합니다. 하지만, 인가 검사가 게이트나 정책 메서드까지 도달하도록 허용하려면, 사용자 인수의 타입힌트를 "optional"로 선언하거나, 기본값을 `null`로 지정하면 됩니다:

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

특정 사용자에게는 해당 정책 내 모든 동작에 대해 인가를 부여하고 싶을 수도 있습니다. 이럴 때는 정책 클래스에 `before` 메서드를 정의하세요. `before` 메서드는 정책 내 다른 메서드가 실행되기 전에 실행되므로, 인가 결과를 미리 결정할 수 있습니다. 주로 앱 관리자 등에게 모든 권한을 부여할 때 사용합니다:

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

특정 사용자 유형에 대해 모든 인가 검사를 거부하려면, `before` 메서드에서 `false`를 반환하면 됩니다. 만약 `null`을 반환하면, 해당 인가 검사는 정책 내 인가 메서드로 넘어가 처리됩니다.

> [!WARNING]
> 정책 클래스에 `before` 메서드가 있더라도, 정책 내에 검사하려는 동작명과 일치하는 메서드가 없다면 이 `before` 메서드는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 사용한 동작 인가

<a name="via-the-user-model"></a>
### User 모델을 통한 인가

라라벨의 `App\Models\User` 모델에는 동작 인가를 위한 유용한 메서드인 `can`과 `cannot`이 포함되어 있습니다. 이 메서드들은 인가하려는 동작명과 관련 모델을 인수로 받습니다. 예를 들어, 특정 사용자가 `App\Models\Post` 모델을 수정할 권한이 있는지 컨트롤러 메서드에서 다음과 같이 확인할 수 있습니다:

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

        // Update the post...

        return redirect('/posts');
    }
}
```

해당 모델에 대해 [정책이 등록](#registering-policies)되어 있다면, `can` 메서드는 자동으로 적절한 정책 메서드를 찾아 불린 값을 반환합니다. 만약 등록된 정책이 없다면, `can` 메서드는 주어진 동작명에 해당하는 클로저 기반 게이트를 실행해 결과를 반환하려 시도합니다.

<a name="user-model-actions-that-dont-require-models"></a>

#### 모델 인스턴스가 필요 없는 액션

정책 메서드 중에는 `create`와 같이 모델 인스턴스가 필요하지 않은 경우가 있습니다. 이런 상황에서는 `can` 메서드에 클래스명을 전달할 수 있습니다. 전달된 클래스명은 해당 액션을 인가할 때 어떤 정책을 사용할지 결정하는 데 사용됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 게시글 생성
     */
    public function store(Request $request): RedirectResponse
    {
        if ($request->user()->cannot('create', Post::class)) {
            abort(403);
        }

        // 게시글 생성 로직...

        return redirect('/posts');
    }
}
```

<a name="via-the-gate-facade"></a>
### Gate 파사드를 통한 인가

`App\Models\User` 모델에 유용한 메서드들이 제공되는 것 외에도, 언제든 `Gate` 파사드의 `authorize` 메서드를 사용해 액션을 인가할 수 있습니다.

`can` 메서드와 마찬가지로, 이 메서드는 인가하려는 액션의 이름과 관련 모델을 인자로 받습니다. 만약 액션이 인가되지 않은 경우, `authorize` 메서드는 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시키며, 이 예외는 라라벨의 예외 핸들러에 의해 자동으로 403 상태 코드의 HTTP 응답으로 변환됩니다.

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
     * 주어진 블로그 게시글 수정
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        Gate::authorize('update', $post);

        // 현재 사용자가 해당 게시글을 수정할 수 있습니다...

        return redirect('/posts');
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 컨트롤러 액션

앞서 설명했듯이, `create`와 같이 모델 인스턴스가 필요 없는 정책 메서드가 있습니다. 이런 경우에는 `authorize` 메서드에 클래스명을 전달하면 됩니다. 클래스명은 해당 액션을 인가할 때 사용할 정책을 결정하는 데 사용됩니다.

```php
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

/**
 * 블로그 게시글 생성
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request): RedirectResponse
{
    Gate::authorize('create', Post::class);

    // 현재 사용자가 블로그 게시글을 생성할 수 있습니다...

    return redirect('/posts');
}
```

<a name="via-middleware"></a>
### 미들웨어를 통한 인가

라라벨은 요청이 라우트나 컨트롤러에 도달하기 전에 액션을 인가할 수 있는 미들웨어를 기본 제공합니다. 기본적으로, `Illuminate\Auth\Middleware\Authorize` 미들웨어는 라라벨에 의해 자동 등록된 `can` [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)을 사용하여 라우트에 부착할 수 있습니다. 사용자가 게시글을 수정할 권한이 있는지 미들웨어를 통해 인가하는 예제를 살펴보겠습니다.

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 게시글을 수정할 수 있습니다...
})->middleware('can:update,post');
```

위 예제에서는 `can` 미들웨어에 두 개의 인수를 전달합니다. 첫 번째는 인가하려는 액션의 이름이고, 두 번째는 정책 메서드에 전달할 라우트 파라미터입니다. 이 경우 [암묵적 모델 바인딩](/docs/12.x/routing#implicit-binding)을 사용하므로, 정책 메서드에는 `App\Models\Post` 모델 인스턴스가 전달됩니다. 만약 사용자가 해당 액션을 수행할 권한이 없다면, 미들웨어가 403 상태 코드의 HTTP 응답을 반환합니다.

좀 더 편리하게, `can` 미들웨어는 라우트에 `can` 메서드를 사용해서도 부착할 수 있습니다.

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 게시글을 수정할 수 있습니다...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 액션

정책 메서드 중에는 `create`와 같이 모델 인스턴스가 필요하지 않은 경우도 있습니다. 이런 경우에는 미들웨어에 클래스명을 전달할 수 있습니다. 전달된 클래스명은 액션 인가 시 어떤 정책을 사용할지 결정하는 데 사용됩니다.

```php
Route::post('/post', function () {
    // 현재 사용자가 게시글을 생성할 수 있습니다...
})->middleware('can:create,App\Models\Post');
```

문자열로 전체 클래스명을 지정하는 방식은 다소 번거로울 수 있기 때문에, 보통 라우트에 `can` 메서드를 사용해 미들웨어를 직접 부착하는 것이 더 간단합니다.

```php
use App\Models\Post;

Route::post('/post', function () {
    // 현재 사용자가 게시글을 생성할 수 있습니다...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿에서의 인가

Blade 템플릿에서, 사용자가 특정 액션을 인가받았을 때만 페이지의 일부를 보여주고 싶을 수 있습니다. 예를 들어, 사용자가 실제로 게시글을 수정할 수 있을 때에만 블로그 게시글 수정 폼을 표시하고 싶을 때, `@can`과 `@cannot` 디렉티브를 사용할 수 있습니다.

```blade
@can('update', $post)
    <!-- 현재 사용자가 게시글을 수정할 수 있습니다... -->
@elsecan('create', App\Models\Post::class)
    <!-- 현재 사용자가 새 게시글을 생성할 수 있습니다... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- 현재 사용자는 게시글을 수정할 수 없습니다... -->
@elsecannot('create', App\Models\Post::class)
    <!-- 현재 사용자는 새 게시글을 생성할 수 없습니다... -->
@endcannot
```

이 디렉티브들은 `@if`나 `@unless` 문을 사용하는 것보다 훨씬 간편하게 활용할 수 있습니다. 위의 `@can` 및 `@cannot` 문은 다음과 동일합니다.

```blade
@if (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 수정할 수 있습니다... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 수정할 수 없습니다... -->
@endunless
```

또한 사용자가 지정한 여러 액션 중 하나라도 인가되어 있는지 확인하려면 `@canany` 디렉티브를 사용할 수 있습니다.

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- 현재 사용자가 게시글을 수정, 조회 또는 삭제할 수 있습니다... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 있습니다... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 액션

다른 인가 방식들과 마찬가지로, 액션 수행에 모델 인스턴스가 필요 없는 경우에는 `@can` 및 `@cannot` 디렉티브에 클래스명을 전달할 수 있습니다.

```blade
@can('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 있습니다... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 없습니다... -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 정보(컨텍스트) 전달

정책을 사용하여 액션을 인가할 때, 배열을 두 번째 인자로 전달할 수 있습니다. 배열의 첫 번째 요소는 어떤 정책이 사용될지 결정하는 데 활용되고, 나머지 요소들은 정책 메서드의 파라미터로 전달되어 인가 결정 시 추가 정보로 활용할 수 있습니다. 예를 들어, 아래의 `PostPolicy` 메서드는 `$category`라는 추가 파라미터를 가지고 있습니다.

```php
/**
 * 주어진 게시글이 사용자에 의해 수정될 수 있는지 결정
 */
public function update(User $user, Post $post, int $category): bool
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```

인증된 사용자가 주어진 게시글을 수정할 수 있는지 확인할 때, 다음과 같이 해당 정책 메서드를 호출할 수 있습니다.

```php
/**
 * 주어진 블로그 게시글 수정
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post): RedirectResponse
{
    Gate::authorize('update', [$post, $request->category]);

    // 현재 사용자가 블로그 게시글을 수정할 수 있습니다...

    return redirect('/posts');
}
```

<a name="authorization-and-inertia"></a>
## 인가와 이너시아(Inertia) 연동

인가(authorization)는 반드시 서버에서 처리해야 하지만, 때로는 프론트엔드 애플리케이션에서도 인가 정보를 활용해 UI를 적절하게 표시하는 것이 편리할 수 있습니다. 라라벨은 Inertia 기반 프론트엔드에 인가 정보를 노출하는 방법에 대해 필수 규약을 정하지는 않습니다.

하지만, 라라벨의 Inertia 기반 [스타터 키트](/docs/12.x/starter-kits)를 사용하는 경우, 애플리케이션에 이미 `HandleInertiaRequests` 미들웨어가 포함되어 있습니다. 이 미들웨어의 `share` 메서드 내에서 모든 Inertia 페이지에 제공되는 공통 데이터를 반환할 수 있습니다. 여기에서 사용자 인가 정보를 지정해 프론트로 전달하는 것이 편리합니다.

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
     * 기본적으로 공유되는 props 정의
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