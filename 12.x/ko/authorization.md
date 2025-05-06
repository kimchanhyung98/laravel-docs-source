# 인가(Authorization)

- [소개](#introduction)
- [게이트(Gates)](#gates)
    - [게이트 작성하기](#writing-gates)
    - [행위 인가하기](#authorizing-actions-via-gates)
    - [게이트 응답](#gate-responses)
    - [게이트 검사 가로채기](#intercepting-gate-checks)
    - [인라인 인가](#inline-authorization)
- [정책(Policy) 생성하기](#creating-policies)
    - [정책 생성](#generating-policies)
    - [정책 등록](#registering-policies)
- [정책 작성하기](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델이 없는 메서드](#methods-without-models)
    - [게스트 사용자](#guest-users)
    - [정책 필터](#policy-filters)
- [정책을 이용한 행위 인가](#authorizing-actions-using-policies)
    - [User 모델을 통한 인가](#via-the-user-model)
    - [Gate 파사드를 통한 인가](#via-the-gate-facade)
    - [미들웨어를 통한 인가](#via-middleware)
    - [Blade 템플릿을 통한 인가](#via-blade-templates)
    - [추가 정보 제공하기](#supplying-additional-context)
- [인가 & Inertia](#authorization-and-inertia)

<a name="introduction"></a>
## 소개

Laravel은 내장된 [인증](/docs/{{version}}/authentication) 서비스뿐만 아니라, 주어진 리소스에 대해 사용자의 행위를 인가(허가)하는 간단한 방법도 제공합니다. 예를 들어, 사용자가 인증되어 있다고 해도, 특정 Eloquent 모델이나 데이터베이스 레코드의 수정 또는 삭제 권한이 없을 수 있습니다. Laravel의 인가 기능을 통해 이러한 권한 검사 작업을 쉽고 체계적으로 관리할 수 있습니다.

Laravel에서는 행위 인가를 위한 두 가지 주요 방법을 제공합니다: [게이트(Gates)](#gates)와 [정책(Policy)](#creating-policies)입니다. 게이트와 정책은 각각 라우트와 컨트롤러와 비슷하게 생각할 수 있습니다. 게이트는 간단히 클로저(익명 함수) 기반으로 인가를 처리하며, 정책은 컨트롤러처럼 특정 모델이나 리소스에 대한 인가 로직을 그룹화합니다. 본 문서에서는 먼저 게이트를 다루고, 이후 정책에 대해 설명합니다.

애플리케이션 개발 시 반드시 게이트만 또는 정책만을 사용해야 하는 것은 아닙니다. 대부분의 애플리케이션은 게이트와 정책을 혼합해서 사용하며, 이는 전혀 문제되지 않습니다! 게이트는 모델이나 리소스와 무관한 행위(예: 관리자 대시보드 보기)에 최적입니다. 반면, 특정 모델이나 리소스에 대해 행동 인가가 필요할 때는 정책을 사용하는 것이 좋습니다.

<a name="gates"></a>
## 게이트(Gates)

<a name="writing-gates"></a>
### 게이트 작성하기

> [!WARNING]
> 게이트는 Laravel 인가 기능의 기본 개념을 익히는 데 아주 유용합니다. 하지만 규모가 큰 Laravel 애플리케이션을 개발할 때는 [정책(Policy)](#creating-policies)를 사용하여 인가 규칙을 체계적으로 관리하는 것을 추천합니다.

게이트는 사용자가 특정 행위를 수행해도 되는지를 결정하는 단순한 클로저입니다. 일반적으로, 게이트는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에서 `Gate` 파사드를 이용해 정의됩니다. 게이트는 항상 첫 번째 인자로 사용자 인스턴스를 받고, 필요에 따라 Eloquent 모델 등의 추가 인자를 받을 수 있습니다.

아래 예시에서는 특정 `App\Models\Post` 모델을 사용자가 수정할 수 있는지 결정하는 게이트를 정의합니다. 게이트는 사용자의 `id`와 포스트의 `user_id`를 비교하여 이를 판단합니다.

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * 부트스트랩 관련 애플리케이션 서비스
 */
public function boot(): void
{
    Gate::define('update-post', function (User $user, Post $post) {
        return $user->id === $post->user_id;
    });
}
```

컨트롤러처럼, 게이트도 클래스 콜백 배열로 정의할 수 있습니다.

```php
use App\Policies\PostPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * 부트스트랩 관련 애플리케이션 서비스
 */
public function boot(): void
{
    Gate::define('update-post', [PostPolicy::class, 'update']);
}
```

<a name="authorizing-actions-via-gates"></a>
### 행위 인가하기

게이트를 이용해 행위를 인가하려면, `Gate` 파사드에서 제공하는 `allows` 또는 `denies` 메서드를 사용해야 합니다. 현재 인증된 사용자를 이 메서드들에 직접 전달하지 않아도 되며, Laravel이 자동으로 게이트 클로저로 전달해줍니다. 대개, 인가가 필요한 액션을 수행하기 전에 컨트롤러 내에서 게이트 인가 메서드를 호출합니다.

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
     * 주어진 포스트를 수정합니다.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if (! Gate::allows('update-post', $post)) {
            abort(403);
        }

        // 포스트 업데이트...

        return redirect('/posts');
    }
}
```

현재 인증된 사용자 외의 사용자가 특정 액션을 수행할 수 있는지 확인하려면 `Gate` 파사드의 `forUser` 메서드를 사용할 수 있습니다.

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // 해당 사용자는 포스트를 수정할 수 있습니다...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // 해당 사용자는 포스트를 수정할 수 없습니다...
}
```

`any` 또는 `none` 메서드를 이용해 여러 액션을 동시에 인가할 수 있습니다.

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // 해당 사용자는 포스트를 수정 또는 삭제할 수 있습니다...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // 해당 사용자는 포스트를 수정하거나 삭제할 수 없습니다...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 인가 또는 예외 발생시키기

행위 인가 시, 인가되지 않은 경우 자동으로 `Illuminate\Auth\Access\AuthorizationException`을 발생시키고 싶다면 `Gate` 파사드의 `authorize` 메서드를 사용하면 됩니다. `AuthorizationException`은 Laravel에서 자동으로 403 HTTP 응답으로 변환됩니다:

```php
Gate::authorize('update-post', $post);

// 인가가 되었습니다...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 정보 제공하기

행위 인가를 위한 게이트 메서드(`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`)와 [Blade 인가 디렉티브](#via-blade-templates)(`@can`, `@cannot`, `@canany`)는 두 번째 인자로 배열을 받을 수 있습니다. 이 배열 내의 각각의 요소는 게이트 클로저의 매개변수로 전달되어, 인가 결정 시 추가 정보를 제공할 수 있습니다:

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
    // 사용자가 포스트를 생성할 수 있습니다...
}
```

<a name="gate-responses"></a>
### 게이트 응답

지금까지는 단순히 불린 값만 반환하는 게이트에 대해 알아보았습니다. 하지만 상세한 응답(에러 메시지 등)이 필요할 수도 있습니다. 이럴 때는 게이트에서 `Illuminate\Auth\Access\Response`를 반환할 수 있습니다:

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

게이트에서 인가 응답 객체를 반환해도, `Gate::allows`는 여전히 불린 값만 반환합니다. 그러나 `Gate::inspect`를 사용하면 게이트에서 반환한 전체 인가 응답 객체를 확인할 수 있습니다:

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // 인가되었습니다...
} else {
    echo $response->message();
}
```

`Gate::authorize`를 사용할 경우, 인가되지 않았을 때 인가 응답에서 제공한 에러 메시지가 HTTP 응답으로 전달됩니다:

```php
Gate::authorize('edit-settings');

// 인가되었습니다...
```

<a name="customizing-gate-response-status"></a>
#### HTTP 응답 상태 커스터마이징

게이트에서 인가가 거부되면 기본으로 `403` HTTP 응답이 반환되지만, 때때로 다른 상태 코드가 필요할 수 있습니다. 이럴 때는 `Illuminate\Auth\Access\Response`의 `denyWithStatus` 정적 생성자를 사용해 실패 응답의 상태 코드를 커스터마이징할 수 있습니다:

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

웹앱에서 리소스를 숨길 때 `404`로 응답하는 것이 보편적이므로, 편의를 위해 `denyAsNotFound` 메서드도 제공합니다:

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

특정 사용자에게 모든 권한을 부여하고 싶을 때가 있습니다. 이럴 때는 모든 인가 검사가 실행되기 전에 동작하는 클로저를 `before` 메서드로 정의할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저에서 null 이외의 값을 반환하면 그것이 인가 검사 결과로 사용됩니다.

모든 인가 검사 후 후처리를 진행하고 싶으면 `after` 메서드를 사용할 수 있습니다:

```php
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after` 클로저의 반환값은 게이트 혹은 정책이 null을 반환하지 않는 한, 인가 결과를 덮어쓰지 않습니다.

<a name="inline-authorization"></a>
### 인라인 인가

별도의 게이트를 정의하지 않고, 현재 로그인한 사용자가 특정 행위를 인가받았는지 즉석에서 판단하고 싶을 때도 있습니다. Laravel은 `Gate::allowIf`와 `Gate::denyIf` 메서드를 통해 이러한 "인라인" 인가 검사를 제공합니다. 인라인 인가는 정의된 ["before", "after" 인가 훅](#intercepting-gate-checks)을 실행하지 않습니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

행위가 인가되지 않거나, 현재 인증된 사용자가 없을 경우 `Illuminate\Auth\Access\AuthorizationException`이 자동으로 발생합니다. 이 예외는 Laravel에서 403 HTTP 응답으로 변환됩니다.

<a name="creating-policies"></a>
## 정책(Policy) 생성하기

<a name="generating-policies"></a>
### 정책 생성

정책(Policy)은 특정 모델이나 리소스별로 인가 로직을 체계적으로 그룹화하는 클래스입니다. 예를 들어, 블로그 애플리케이션이라면 `App\Models\Post` 모델에 대해 사용자의 게시글 생성/수정 등을 인가하는 `App\Policies\PostPolicy`를 만들 수 있습니다.

`make:policy` 아티즌 명령어로 정책을 생성할 수 있습니다. 생성된 정책은 `app/Policies` 디렉터리에 위치합니다. 이 디렉터리가 없다면 Laravel이 자동으로 생성해줍니다.

```shell
php artisan make:policy PostPolicy
```

`make:policy` 명령어는 기본적으로 빈 정책 클래스를 생성합니다. 생성/수정/삭제 등 리소스 관련 정책 메서드를 예시로 포함하려면 `--model` 옵션을 제공합니다:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록

<a name="policy-discovery"></a>
#### 정책 자동 탐지

Laravel은 모델 및 정책이 표준 네이밍 규칙을 따르면 정책을 자동으로 탐지합니다. 즉, 정책은 모델이 존재하는 디렉터리와 동일하거나 그 상위 디렉터리의 `Policies` 폴더에 위치해야 하며, 정책 클래스명은 모델명 뒤에 `Policy`가 붙어야 합니다. 예를 들어, `User` 모델은 `UserPolicy` 정책 클래스에 대응됩니다.

자동 탐지 규칙을 직접 정의하고 싶다면, `Gate::guessPolicyNamesUsing` 메서드를 사용해 커스텀 콜백을 등록할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // 주어진 모델에 대한 정책 클래스명을 반환...
});
```

<a name="manually-registering-policies"></a>
#### 정책 수동 등록

`Gate` 파사드를 사용해 `AppServiceProvider`의 `boot` 메서드 안에서 정책과 해당 모델을 직접 매핑하여 등록할 수도 있습니다.

```php
use App\Models\Order;
use App\Policies\OrderPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * 부트스트랩 관련 애플리케이션 서비스
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

정책 클래스가 등록되면, 인가할 각 행위별로 메서드를 추가할 수 있습니다. 예를 들어, `App\Models\User`가 주어진 `App\Models\Post` 인스턴스를 수정 가능한지 판단하는 `update` 메서드를 정의해봅니다.

`update` 메서드는 `User`와 `Post` 인스턴스를 인자로 받고, 수정 인가 여부에 따라 `true` 또는 `false`를 반환합니다. 예시에서는 사용자의 `id`가 게시글의 `user_id`와 일치하는지 확인합니다.

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 주어진 포스트를 해당 사용자가 수정할 수 있는지 여부를 판단합니다.
     */
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}
```

정책에서는 필요한 만큼 행위에 대응하는 추가 메서드를 정의할 수 있습니다. 예를 들어, `view`, `delete` 등의 메서드도 만들 수 있습니다. 정책 메서드명은 자유롭게 정할 수 있습니다.

아티즌으로 정책 생성 시 `--model` 옵션을 사용했다면 `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 등의 메서드가 기본으로 생성됩니다.

> [!NOTE]
> 모든 정책은 Laravel [서비스 컨테이너](/docs/{{version}}/container)로 해석됩니다. 따라서 정책 생성자에 필요한 의존성을 타입힌트하면 자동으로 주입됩니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지는 불린 값만 반환하는 정책 메서드만 살펴봤습니다. 더 상세한 응답(에러 메시지 등)이 필요하다면, 정책 메서드에서 `Illuminate\Auth\Access\Response` 인스턴스를 반환하면 됩니다.

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 주어진 포스트를 사용자가 수정 가능한지 판단합니다.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::deny('이 게시글에 대한 소유권이 없습니다.');
}
```

정책에서 인가 응답을 반환해도 `Gate::allows`는 불린 값만 반환합니다. 전체 인가 응답을 확인하려면 `Gate::inspect`를 사용합니다.

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // 인가되었습니다...
} else {
    echo $response->message();
}
```

`Gate::authorize`를 사용할 경우(인가되지 않을 때 `AuthorizationException` 발생), 정책 응답의 에러 메시지가 HTTP 응답으로 전달됩니다.

```php
Gate::authorize('update', $post);

// 인가되었습니다...
```

<a name="customizing-policy-response-status"></a>
#### HTTP 응답 상태 커스터마이징

정책 메서드에서 인가가 거부되면 기본적으로 `403` 응답이 반환됩니다. 다른 응답 코드가 필요할 경우, `Illuminate\Auth\Access\Response`의 `denyWithStatus` 정적 생성자를 통해 커스터마이즈할 수 있습니다.

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 주어진 포스트를 사용자가 수정 가능한지 판단합니다.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyWithStatus(404);
}
```

리소스를 `404`로 숨기는 것이 흔하므로, `denyAsNotFound` 메서드도 제공됩니다.

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 주어진 포스트를 사용자가 수정 가능한지 판단합니다.
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

일부 정책 메서드는 인증된 사용자 인스턴스만 받습니다. 주로 `create` 같은 행위에서 많이 사용됩니다. 예를 들어, 특정 사용자가 게시글을 생성할 수 있는지 판단하려면 아래처럼 구현할 수 있습니다.

```php
/**
 * 해당 사용자가 게시글을 생성할 수 있는지 판단합니다.
 */
public function create(User $user): bool
{
    return $user->role == 'writer';
}
```

<a name="guest-users"></a>
### 게스트 사용자

기본적으로 모든 게이트 및 정책은 인증되지 않은 사용자의 경우 자동으로 `false`를 반환합니다. 하지만, 사용자 인자에 "옵셔널" 타입힌트나 기본값 `null`을 지정하면 게스트 사용자에 대해 별도 로직을 적용할 수 있습니다.

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 주어진 포스트를 해당 사용자가 수정할 수 있는지 판단합니다.
     */
    public function update(?User $user, Post $post): bool
    {
        return $user?->id === $post->user_id;
    }
}
```

<a name="policy-filters"></a>
### 정책 필터

특정 사용자에게 정책 내 모든 행위를 인가하고 싶다면, 정책에 `before` 메서드를 정의하세요. `before`는 정책의 다른 메서드보다 앞서 실행되어, 실제 정책 메서드가 호출되기 전에 행위를 인가할 기회를 제공합니다. 보통 어플리케이션 관리자의 모든 기능을 허용할 때 사용합니다.

```php
use App\Models\User;

/**
 * 사전 인가 검사
 */
public function before(User $user, string $ability): bool|null
{
    if ($user->isAdministrator()) {
        return true;
    }

    return null;
}
```

특정 사용자 유형에 대해 모든 인가를 거부하려면 `before`에서 `false`를 반환하면 됩니다. `null`을 반환하면 일반 정책 메서드가 실행됩니다.

> [!WARNING]
> 정책 클래스에서 인가 검사 대상 행위와 동일한 이름의 메서드가 없으면 `before`는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 이용한 행위 인가

<a name="via-the-user-model"></a>
### User 모델을 통한 인가

Laravel의 `App\Models\User` 모델은 행위를 인가할 때 유용한 `can` 및 `cannot` 메서드를 제공합니다. 이 메서드들은 인가할 행위명과 관련된 모델을 받습니다. 예를 들어, 사용자가 특정 `App\Models\Post`를 수정할 권한이 있는지 확인할 수 있습니다. 보통 이는 컨트롤러 내에서 사용됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 주어진 포스트를 수정합니다.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if ($request->user()->cannot('update', $post)) {
            abort(403);
        }

        // 포스트 업데이트...

        return redirect('/posts');
    }
}
```

[정책이 등록](#registering-policies)된 모델인 경우 `can`은 자동으로 알맞은 정책 메서드를 호출합니다. 등록된 정책이 없다면 동일 이름의 클로저 기반 게이트를 호출합니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 행위

일부 행위(예: `create`)는 모델 인스턴스가 필요 없습니다. 이런 경우 클래스 이름을 `can`에 넘기면, 인가 시 해당 클래스의 정책이 자동 사용됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 포스트를 생성합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        if ($request->user()->cannot('create', Post::class)) {
            abort(403);
        }

        // 포스트 생성...

        return redirect('/posts');
    }
}
```

<a name="via-the-gate-facade"></a>
### Gate 파사드를 통한 인가

`App\Models\User` 모델의 메서드 외에도, 항상 `Gate` 파사드의 `authorize` 메서드로 행위를 인가할 수 있습니다.

`can` 메서드와 마찬가지로, 인가할 행위명과 관련된 모델을 인자로 받습니다. 인가되지 않았을 경우 `Illuminate\Auth\Access\AuthorizationException`이 발생하고, Laravel의 예외 핸들러에서 403 HTTP 응답으로 변환됩니다.

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
     * 주어진 블로그 포스트를 수정합니다.
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        Gate::authorize('update', $post);

        // 현재 사용자가 블로그 포스트를 수정할 수 있습니다...

        return redirect('/posts');
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 행위

앞서 설명한 것처럼, 일부 정책 메서드(예: `create`)는 모델 인스턴스 없이 클래스명만으로 인가할 수 있습니다.

```php
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

/**
 * 새 블로그 포스트를 생성합니다.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request): RedirectResponse
{
    Gate::authorize('create', Post::class);

    // 현재 사용자가 블로그 포스트를 생성할 수 있습니다...

    return redirect('/posts');
}
```

<a name="via-middleware"></a>
### 미들웨어를 통한 인가

Laravel은 라우트나 컨트롤러에 요청이 도달하기 전에 행위를 미리 인가할 수 있는 미들웨어를 제공합니다. 기본적으로 `Illuminate\Auth\Middleware\Authorize` 미들웨어는 `can` [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)으로 사용할 수 있습니다. 아래는, 사용자가 포스트를 수정할 수 있는지 인가하는 예시입니다.

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 포스트를 수정할 수 있습니다...
})->middleware('can:update,post');
```

여기서 `can` 미들웨어의 첫 번째 인자는 인가할 행위명, 두 번째 인자는 정책 메서드에 전달할 라우트 파라미터입니다. [암시적 모델 바인딩](/docs/{{version}}/routing#implicit-binding)을 사용했으므로, `App\Models\Post` 모델이 정책 메서드로 전달됩니다. 인가되지 않으면 403 상태의 HTTP 응답이 반환됩니다.

동일 작업을 위해 route의 `can` 메서드를 사용할 수도 있습니다.

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 포스트를 수정할 수 있습니다...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 행위

마찬가지로 `create`처럼 모델 인스턴스가 필요 없는 정책 메서드를 위해 미들웨어의 인자로 클래스명을 전달할 수 있습니다. 다음은 예시입니다.

```php
Route::post('/post', function () {
    // 현재 사용자가 포스트를 생성할 수 있습니다...
})->middleware('can:create,App\Models\Post');
```

미들웨어에 클래스명 전체를 문자열로 쓰는 것이 번거로울 수 있으니, 라우트의 `can` 메서드로도 편리하게 지정할 수 있습니다.

```php
use App\Models\Post;

Route::post('/post', function () {
    // 현재 사용자가 포스트를 생성할 수 있습니다...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿을 통한 인가

Blade 템플릿 내에서는, 사용자가 특정 행위를 인가받았을 때만 일부 화면을 보여주고 싶을 수 있습니다. 예를 들어, 블로그 게시글 수정 폼을 해당 사용자가 수정 가능할 때만 보여주는 경우, `@can`, `@cannot` 디렉티브를 사용할 수 있습니다.

```blade
@can('update', $post)
    <!-- 현재 사용자가 포스트를 수정할 수 있습니다... -->
@elsecan('create', App\Models\Post::class)
    <!-- 현재 사용자가 새 포스트를 생성할 수 있습니다... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- 현재 사용자가 포스트를 수정할 수 없습니다... -->
@elsecannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 새 포스트를 만들 수 없습니다... -->
@endcannot
```

이러한 디렉티브는 `@if` 및 `@unless` 문을 축약한 형태입니다. 위 예시는 다음과 동일합니다.

```blade
@if (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 포스트를 수정할 수 있습니다... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 포스트를 수정할 수 없습니다... -->
@endunless
```

여러 행위 중 하나라도 인가되었는지 확인하려면 `@canany` 디렉티브를 사용합니다.

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- 현재 사용자가 포스트를 수정, 보기, 삭제할 수 있습니다... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- 현재 사용자가 포스트를 만들 수 있습니다... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 행위

다른 인가 방식과 마찬가지로, 인스턴스가 필요 없는 경우 `@can`과 `@cannot`에 클래스명을 전달하면 됩니다.

```blade
@can('create', App\Models\Post::class)
    <!-- 현재 사용자가 포스트를 만들 수 있습니다... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 포스트를 만들 수 없습니다... -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 정보 제공하기

정책을 사용해 행위를 인가할 때, 두 번째 인자로 배열을 전달할 수 있습니다. 이때 배열의 첫 번째 요소는 인가할 대상(정책의 모델)이 되고, 나머지 요소들은 정책 메서드의 추가 인자로 전달되어 인가를 위한 추가 정보를 제공할 수 있습니다. 예를 들어 아래처럼 `category` 인자를 추가했습니다.

```php
/**
 * 해당 사용자가 주어진 포스트와 카테고리로 수정이 가능한지 판단합니다.
 */
public function update(User $user, Post $post, int $category): bool
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```

호출 예시는 다음과 같습니다.

```php
/**
 * 주어진 블로그 포스트를 수정합니다.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post): RedirectResponse
{
    Gate::authorize('update', [$post, $request->category]);

    // 현재 사용자가 블로그 포스트를 수정할 수 있습니다...

    return redirect('/posts');
}
```

<a name="authorization-and-inertia"></a>
## 인가 & Inertia

인가(Authorization)는 항상 서버에서 처리되어야 하지만, 때때로 프론트엔드에서 UI를 적절히 렌더링하기 위해 인가 정보를 제공하는 것이 편리할 수 있습니다. Laravel은 Inertia 기반 프론트엔드에 인가 정보를 노출하는 데 필수적인 규칙을 정의하지 않습니다.

하지만, Inertia 기반 [스타터 킷](/docs/{{version}}/starter-kits)을 사용하는 경우, 이미 애플리케이션에 `HandleInertiaRequests` 미들웨어가 포함되어 있습니다. 이 미들웨어의 `share` 메서드 내에서, 모든 Inertia 페이지에 전달될 공유 데이터를 정의할 수 있습니다. 이를 통해 사용자 인가 상태를 손쉽게 프론트엔드로 제공할 수 있습니다.

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
     * 기본으로 공유되는 props 정의
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
