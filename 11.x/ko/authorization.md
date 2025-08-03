# 권한 부여 (Authorization)

- [소개](#introduction)
- [게이트 (Gates)](#gates)
    - [게이트 작성하기](#writing-gates)
    - [게이트를 통한 액션 권한 부여](#authorizing-actions-via-gates)
    - [게이트 응답 (Gate Responses)](#gate-responses)
    - [게이트 검사 가로채기](#intercepting-gate-checks)
    - [인라인 권한 부여](#inline-authorization)
- [정책 생성하기 (Creating Policies)](#creating-policies)
    - [정책 생성하기](#generating-policies)
    - [정책 등록하기](#registering-policies)
- [정책 작성하기 (Writing Policies)](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델이 없는 메서드](#methods-without-models)
    - [게스트 사용자](#guest-users)
    - [정책 필터](#policy-filters)
- [정책을 사용한 액션 권한 부여](#authorizing-actions-using-policies)
    - [User 모델을 통한 권한 부여](#via-the-user-model)
    - [Gate 파사드를 통한 권한 부여](#via-the-gate-facade)
    - [미들웨어를 통한 권한 부여](#via-middleware)
    - [Blade 템플릿에서 권한 부여](#via-blade-templates)
    - [추가 컨텍스트 제공](#supplying-additional-context)
- [권한 부여와 Inertia](#authorization-and-inertia)

<a name="introduction"></a>
## 소개

Laravel은 내장된 [인증](/docs/11.x/authentication) 서비스 외에도 특정 리소스에 대해 사용자의 액션을 권한 부여하는 간단한 방법을 제공합니다. 예를 들어 사용자가 인증되었다 하더라도 특정 Eloquent 모델이나 애플리케이션에서 관리하는 데이터베이스 레코드를 업데이트하거나 삭제할 권한이 없을 수 있습니다. Laravel의 권한 부여 기능은 이러한 권한 확인을 쉽고 체계적으로 관리할 수 있는 방식을 제공합니다.

Laravel에서는 권한 부여를 위해 두 가지 주요 방식을 제공합니다: [게이트](#gates)와 [정책](#creating-policies)입니다. 게이트와 정책은 각각 라우트와 컨트롤러처럼 생각할 수 있습니다. 게이트는 단순하고 클로저 기반 접근 방식을 제공하는 반면, 정책은 컨트롤러처럼 특정 모델이나 리소스와 관련된 권한 부여 로직을 그룹화합니다. 이 문서에서는 먼저 게이트를 살펴보고, 그 다음 정책을 다루겠습니다.

애플리케이션을 구축할 때 게이트 또는 정책 중 하나만 독점적으로 사용해야 하는 것은 아닙니다. 대부분의 애플리케이션은 게이트와 정책을 혼합해서 사용하며, 이는 전혀 문제되지 않습니다. 게이트는 관리자 대시보드 조회처럼 모델이나 리소스와 관련 없는 행동에 주로 적합합니다. 반면, 특정 모델이나 리소스에 대한 액션 권한을 부여하려면 정책을 사용해야 합니다.

<a name="gates"></a>
## 게이트 (Gates)

<a name="writing-gates"></a>
### 게이트 작성하기

> [!WARNING]  
> 게이트는 Laravel 권한 부여 기능의 기본을 배우기에 좋지만, 견고한 애플리케이션을 만들 때는 권한 규칙을 정리하는 데 [정책](#creating-policies)을 사용하는 것을 고려해야 합니다.

게이트는 특정 사용자가 주어진 액션을 수행할 권한이 있는지 결정하는 클로저(폐쇄 함수)입니다. 일반적으로 `Gate` 파사드를 사용해 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 정의합니다. 게이트는 항상 첫 번째 인수로 사용자 인스턴스를 받고, 상황에 따라 관련된 Eloquent 모델과 같은 추가 인수를 받을 수 있습니다.

아래 예제에서는 사용자가 특정 `App\Models\Post` 모델을 업데이트할 수 있는지 판단하는 게이트를 정의합니다. 이 게이트는 사용자의 `id`와 게시글을 작성한 사용자의 `user_id`를 비교하여 결정합니다:

```
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

컨트롤러와 마찬가지로, 게이트는 클래스 콜백 배열을 사용해 정의할 수도 있습니다:

```
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
### 게이트를 통한 액션 권한 부여

게이트를 사용해 액션을 권한 부여하려면, `Gate` 파사드가 제공하는 `allows` 또는 `denies` 메서드를 사용하세요. 현재 인증된 사용자를 이 메서드에 명시적으로 전달할 필요는 없습니다. Laravel이 자동으로 게이트 클로저에 사용자 인스턴스를 넣어줍니다. 주로 애플리케이션 컨트롤러 내에서 권한이 필요한 작업을 수행하기 전에 게이트 권한 부여 메서드를 호출합니다:

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

        // 게시글 업데이트...

        return redirect('/posts');
    }
}
```

현재 인증된 사용자가 아닌 다른 사용자가 액션을 수행할 권한이 있는지 확인하려면 `Gate` 파사드의 `forUser` 메서드를 사용하세요:

```
if (Gate::forUser($user)->allows('update-post', $post)) {
    // 해당 사용자가 게시글을 업데이트할 수 있음...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // 해당 사용자가 게시글을 업데이트할 수 없음...
}
```

한 번에 여러 액션 권한을 확인하려면 `any` 또는 `none` 메서드를 사용하세요:

```
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // 사용자가 게시글을 업데이트하거나 삭제할 수 있음...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // 사용자가 게시글을 업데이트하거나 삭제할 수 없음...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 권한 부여 실패 시 예외 던지기

액션 권한 부여를 시도하고, 권한이 없으면 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 던지고 싶다면, `Gate` 파사드의 `authorize` 메서드를 사용할 수 있습니다. `AuthorizationException`은 Laravel에서 자동으로 403 HTTP 응답으로 변환됩니다:

```
Gate::authorize('update-post', $post);

// 권한이 허용된 경우...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 제공하기

권한 부여를 위한 게이트 메서드들(`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`) 및 권한 부여용 Blade 지시자(`@can`, `@cannot`, `@canany`)는 두 번째 인수로 배열을 받을 수 있습니다. 이 배열 요소들은 게이트 클로저에 인자로 전달되어 추가 컨텍스트로 활용됩니다:

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
    // 사용자가 게시글을 생성할 수 있음...
}
```

<a name="gate-responses"></a>
### 게이트 응답 (Gate Responses)

지금까지는 부울값을 반환하는 단순한 게이트만 살펴봤습니다. 하지만 가끔은 상세한 응답과 에러 메시지를 함께 반환하고 싶을 때가 있습니다. 이때는 `Illuminate\Auth\Access\Response` 객체를 게이트에서 반환할 수 있습니다:

```
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::deny('관리자만 접근할 수 있습니다.');
});
```

게이트에서 권한 응답을 반환해도 `Gate::allows` 메서드는 여전히 단순 부울값을 반환합니다. 다만 `Gate::inspect` 메서드를 사용하면 게이트가 반환한 전체 권한 응답 객체를 얻을 수 있습니다:

```
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // 액션 권한이 허용됨...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드는 액션 권한이 없으면 `AuthorizationException`을 던지는데, 이 경우 권한 응답에서 지정한 에러 메시지가 HTTP 응답에 전달됩니다:

```
Gate::authorize('edit-settings');

// 액션 권한이 허용됨...
```

<a name="customizing-gate-response-status"></a>
#### HTTP 응답 상태 코드 사용자 지정

게이트에서 액션이 거부되면 기본적으로 `403` HTTP 응답이 반환됩니다. 하지만 때로는 다른 HTTP 상태 코드를 반환하는 것이 유용할 수 있습니다. 이럴 때는 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용해 권한 거부 시 반환할 상태 코드를 지정할 수 있습니다:

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

웹 애플리케이션에서 자원을 숨기기 위해 `404` 응답을 반환하는 것이 흔히 쓰이는 패턴이므로, `denyAsNotFound` 메서드도 편의 기능으로 제공됩니다:

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

때로는 특정 사용자에게 모든 권한을 부여하고 싶을 수 있습니다. 이럴 때는 `before` 메서드를 사용해 다른 모든 권한 검증 전에 실행할 클로저를 정의할 수 있습니다:

```
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저가 `null`이 아닌 값을 반환하면 해당 값이 권한 검증 결과로 간주됩니다.

또한 `after` 메서드를 사용해 모든 권한 검증 후에 실행할 클로저를 정의할 수도 있습니다:

```
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after` 클로저가 반환한 값은 게이트나 정책이 `null`을 반환한 경우를 제외하고 권한 검증 결과를 덮어쓰지 않습니다.

<a name="inline-authorization"></a>
### 인라인 권한 부여

가끔 특정 액션에 대응하는 별도의 게이트를 작성하지 않고 현재 인증된 사용자가 액션 권한이 있는지 확인하고 싶을 때가 있습니다. Laravel은 이러한 "인라인" 권한 부여를 `Gate::allowIf` 및 `Gate::denyIf` 메서드를 통해 지원합니다. 인라인 권한 부여는 정의된 [before 또는 after 권한 훅](#intercepting-gate-checks)을 실행하지 않습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

권한이 없거나 현재 인증된 사용자가 없으면 Laravel이 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 던집니다. 이 예외는 403 HTTP 응답으로 변환됩니다.

<a name="creating-policies"></a>
## 정책 생성하기 (Creating Policies)

<a name="generating-policies"></a>
### 정책 생성하기

정책은 특정 모델이나 리소스와 관련된 권한 부여 로직을 조직화하는 클래스입니다. 예를 들어 블로그 애플리케이션에 `App\Models\Post` 모델이 있다면, `App\Policies\PostPolicy`라는 정책 클래스가 있어 사용자의 게시글 생성이나 업데이트 권한을 결정합니다.

`make:policy` Artisan 명령어를 사용해 정책을 생성할 수 있으며, 생성된 정책은 `app/Policies` 디렉토리에 저장됩니다. `Policies` 디렉토리가 없으면 Laravel이 자동 생성합니다:

```shell
php artisan make:policy PostPolicy
```

`make:policy` 명령은 빈 정책 클래스를 생성합니다. 뷰, 생성, 업데이트, 삭제와 관련된 예제 정책 메서드를 포함한 클래스를 생성하려면 `--model` 옵션을 함께 사용하세요:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록하기

<a name="policy-discovery"></a>
#### 정책 자동 탐색 (Policy Discovery)

기본적으로 Laravel은 모델과 정책이 Laravel의 이름 규칙을 따르면 정책을 자동으로 탐색합니다. 일반적으로 모델은 `app/Models`에, 정책은 `app/Policies`에 위치합니다. Laravel은 우선 `app/Models/Policies`를 확인하고, 없으면 `app/Policies`를 확인합니다. 정책 이름은 모델 이름과 대응하며 `Policy` 접미사를 가져야 합니다. 예를 들어 `User` 모델은 `UserPolicy` 정책과 매칭됩니다.

직접 정책 탐색 로직을 정의하고 싶으면 애플리케이션의 `AppServiceProvider` 내 `boot` 메서드에서 `Gate::guessPolicyNamesUsing` 메서드로 사용자 지정 콜백을 등록할 수 있습니다:

```
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // 해당 모델에 대한 정책 클래스 이름 반환...
});
```

<a name="manually-registering-policies"></a>
#### 정책 수동 등록

`Gate` 파사드를 사용해 애플리케이션의 `AppServiceProvider` 클래스 `boot` 메서드 내에서 모델과 정책을 수동으로 등록할 수 있습니다:

```
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
## 정책 작성하기 (Writing Policies)

<a name="policy-methods"></a>
### 정책 메서드

정책 클래스가 등록된 후에는 권한을 부여할 각 액션에 대해 메서드를 추가할 수 있습니다. 예를 들어 `PostPolicy`에 `update` 메서드를 정의해 `App\Models\User`가 특정 `App\Models\Post` 인스턴스를 업데이트할 수 있는지 판단합니다.

`update` 메서드는 `User`와 `Post` 인스턴스를 인수로 받고, 사용자가 해당 게시글을 업데이트할 권한이 있으면 `true`, 없으면 `false`를 반환해야 합니다. 예를 들어 사용자 `id`와 게시글 `user_id`가 동일한지 확인하는 방식입니다.

```
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 사용자가 주어진 게시글을 업데이트할 수 있는지 판단합니다.
     */
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}
```

필요한 경우 정책에 다양한 권한 부여 액션에 대한 메서드를 계속 추가할 수 있습니다. 예를 들어 `view` 혹은 `delete` 메서드를 정의할 수도 있지만, 정책 메서드 이름은 원하는 대로 지정할 수 있습니다.

`--model` 옵션을 사용해 Artisan 콘솔로 정책을 생성하면, 이미 `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 액션에 대한 메서드가 포함되어 있습니다.

> [!NOTE]  
> 모든 정책은 Laravel [서비스 컨테이너](/docs/11.x/container)를 통해 해석되므로, 정책 생성자에서 필요한 의존성 주입을 타입힌트로 받을 수 있습니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지는 단순 부울값을 반환하는 정책 메서드를 살펴봤지만, 때로는 상세한 응답과 에러 메시지를 반환하고 싶을 수도 있습니다. 이때는 `Illuminate\Auth\Access\Response` 인스턴스를 반환할 수 있습니다:

```
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 사용자가 주어진 게시글을 업데이트할 수 있는지 판단합니다.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::deny('이 게시글의 소유자가 아닙니다.');
}
```

정책에서 권한 응답을 반환해도 `Gate::allows` 메서드는 여전히 단순 부울값을 반환하지만, `Gate::inspect` 메서드를 사용하면 정책에서 반환한 전체 권한 응답을 가져올 수 있습니다:

```
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // 액션 권한이 허용됨...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드를 사용해 액션 권한이 없으면 예외를 던질 때, 권한 응답에 포함된 에러 메시지도 HTTP 응답에 반영됩니다:

```
Gate::authorize('update', $post);

// 권한이 허용됨...
```

<a name="customizing-policy-response-status"></a>
#### HTTP 응답 상태 코드 사용자 지정

정책 메서드가 액션을 거부하면 기본적으로 `403` HTTP 응답이 반환됩니다. 다른 HTTP 상태 코드를 반환해야 할 때는 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 생성자를 사용해 실패 시 반환할 HTTP 상태 코드를 지정할 수 있습니다:

```
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 사용자가 주어진 게시글을 업데이트할 수 있는지 판단합니다.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyWithStatus(404);
}
```

웹 애플리케이션에서 자원을 숨기기 위해 `404` 응답을 반환하는 것은 흔한 패턴이므로, `denyAsNotFound` 메서드도 편리하게 제공합니다:

```
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 사용자가 주어진 게시글을 업데이트할 수 있는지 판단합니다.
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

일부 정책 메서드는 현재 인증된 사용자 인스턴스만 받는 경우가 있습니다. `create` 액션 권한 부여가 대표적인 사례입니다. 예를 들어 블로그에 게시글을 새로 생성할 권한이 있는지 판단하려고 한다면, 정책 메서드는 사용자 인스턴스만 인수로 받을 수 있습니다:

```
/**
 * 사용자가 게시글을 생성할 수 있는지 판단합니다.
 */
public function create(User $user): bool
{
    return $user->role == 'writer';
}
```

<a name="guest-users"></a>
### 게스트 사용자

기본적으로 인증되지 않은 사용자 요청은 모든 게이트와 정책에서 자동으로 `false`를 반환합니다. 하지만 사용자 인수를 "옵셔널" 타입힌트 또는 기본값으로 `null`을 허용하면 인증되지 않은 사용자도 권한 검증 대상에 포함할 수 있습니다:

```
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 사용자가 게시글을 업데이트할 수 있는지 판단합니다.
     */
    public function update(?User $user, Post $post): bool
    {
        return $user?->id === $post->user_id;
    }
}
```

<a name="policy-filters"></a>
### 정책 필터

특정 사용자에게는 정책 내 모든 액션에 대한 권한을 부여하고 싶을 수 있습니다. 이를 위해 정책에 `before` 메서드를 정의하세요. `before`는 정책 내 다른 모든 메서드 실행 전에 호출되어, 권한을 사전 판단할 기회를 제공합니다. 일반적으로 관리자 권한 체크에 사용됩니다:

```
use App\Models\User;

/**
 * 사전 권한 확인을 수행합니다.
 */
public function before(User $user, string $ability): bool|null
{
    if ($user->isAdministrator()) {
        return true;
    }

    return null;
}
```

특정 사용자 유형에 대해 모든 권한 체크를 거부하려면 `before`에서 `false`를 반환하세요. `null`이 반환되면 권한 검증이 해당 메서드로 계속 전달됩니다.

> [!WARNING]  
> 정책 클래스에 권한 이름과 일치하는 메서드가 없으면 `before` 메서드는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 사용한 액션 권한 부여

<a name="via-the-user-model"></a>
### User 모델을 통한 권한 부여

Laravel 애플리케이션에 제공되는 `App\Models\User` 모델에는 권한 부여를 돕는 `can` 및 `cannot` 메서드가 포함되어 있습니다. 이 메서드는 권한을 검사할 액션 이름과 관련 모델을 인수로 받습니다. 예를 들어 `App\Models\Post` 모델을 업데이트할 권한이 있는지 판단할 때 보통 컨트롤러 메서드에서 다음과 같이 사용합니다:

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
     * 주어진 게시글 업데이트하기
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

해당 모델에 [정책이 등록](#registering-policies)되어 있으면, `can` 메서드는 자동으로 적절한 정책 매서드를 호출해 결과 부울값을 반환합니다. 정책이 없으면 클로저 기반 게이트에서 액션 이름과 매칭되는 게이트를 시도합니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

일부 액션은 `create`와 같이 인스턴스가 필요 없는 정책 메서드에 대응할 수 있습니다. 이 경우 `can` 메서드에 클래스 이름을 전달하면 해당 정책을 찾아 권한을 판단합니다:

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
     * 새 게시글 생성하기
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
### `Gate` 파사드를 통한 권한 부여

`App\Models\User` 모델 외에도 `Gate` 파사드의 `authorize` 메서드를 사용해 액션 권한을 검사할 수 있습니다.

`authorize`는 권한을 검사할 액션 이름과 관련 모델을 인수로 받으며, 권한이 없으면 예외를 던집니다. Laravel 예외 핸들러가 이를 자동으로 403 HTTP 응답으로 변환합니다:

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
     * 주어진 블로그 게시글 업데이트하기
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        Gate::authorize('update', $post);

        // 현재 사용자가 게시글을 업데이트할 수 있음...

        return redirect('/posts');
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 컨트롤러 액션

앞서 설명한 것처럼, `create`와 같이 모델 인스턴스가 필요 없는 정책 메서드는 `authorize` 메서드에 클래스 이름을 전달해야 합니다:

```
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

/**
 * 새 블로그 게시글 생성하기
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request): RedirectResponse
{
    Gate::authorize('create', Post::class);

    // 현재 사용자가 게시글을 생성할 수 있음...

    return redirect('/posts');
}
```

<a name="via-middleware"></a>
### 미들웨어를 통한 권한 부여

Laravel은 라우트 또는 컨트롤러에 도달하기 전에 요청 권한을 검증하는 미들웨어를 제공합니다. 기본적으로 `Illuminate\Auth\Middleware\Authorize` 미들웨어는 `can` [미들웨어 별칭](/docs/11.x/middleware#middleware-aliases)으로 등록되어 있습니다. 예를 들어, 사용자가 게시글을 업데이트할 수 있는지 권한을 확인하려면 다음과 같이 합니다:

```
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 게시글을 업데이트할 수 있음...
})->middleware('can:update,post');
```

위 예시에서 `can` 미들웨어는 두 개의 인수를 받습니다. 첫 번째는 권한 부여할 액션 이름이고, 두 번째는 정책 메서드에 전달할 라우트 파라미터입니다. 여기서는 암묵적 모델 바인딩을 사용해 `App\Models\Post` 모델 인스턴스가 정책 메서드에 전달됩니다. 사용자가 권한이 없으면 403 HTTP 응답이 미들웨어에 의해 반환됩니다.

편의를 위해 `can` 메서드를 사용해 라우트에 미들웨어를 붙일 수도 있습니다:

```
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 게시글을 업데이트할 수 있음...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 미들웨어 액션

`create`와 같이 모델 인스턴스가 필요 없는 정책 메서드의 경우, 미들웨어에 클래스 이름을 전달하세요:

```
Route::post('/post', function () {
    // 현재 사용자가 게시글을 생성할 수 있음...
})->middleware('can:create,App\Models\Post');
```

문자열 미들웨어에 전체 클래스 이름을 쓰는 것이 불편할 경우, `can` 메서드로 미들웨어를 붙일 수 있습니다:

```
use App\Models\Post;

Route::post('/post', function () {
    // 현재 사용자가 게시글을 생성할 수 있음...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿에서 권한 부여

Blade 템플릿 작성 시, 사용자가 특정 액션을 수행할 권한이 있을 때만 페이지 일부를 보여주고자 할 수 있습니다. 예를 들어 사용자가 게시글을 업데이트할 수 있을 때만 업데이트 폼을 보여주는 경우입니다. 이 때 `@can` 및 `@cannot` 지시자를 사용할 수 있습니다:

```blade
@can('update', $post)
    <!-- 현재 사용자가 게시글을 업데이트할 수 있음... -->
@elsecan('create', App\Models\Post::class)
    <!-- 현재 사용자가 새로운 게시글을 생성할 수 있음... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- 현재 사용자가 게시글을 업데이트할 수 없음... -->
@elsecannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글 생성 권한이 없음... -->
@endcannot
```

이 지시자들은 `@if`와 `@unless` 구문의 편의형입니다. 위 코드는 다음과 동등합니다:

```blade
@if (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 업데이트할 수 있음... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 업데이트할 수 없음... -->
@endunless
```

`@canany` 지시자를 사용하면, 지정한 액션 배열 중 하나라도 권한이 있으면 특정 내용을 렌더링할 수 있습니다:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- 현재 사용자가 게시글을 업데이트, 조회, 삭제할 수 있음... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 있음... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 Blade 액션

다른 권한 함수처럼, `@can` 및 `@cannot` 에 클래스 이름을 전달해 모델 인스턴스가 필요 없는 액션도 검증할 수 있습니다:

```blade
@can('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글 생성 권한을 가짐... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 없음... -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 컨텍스트 제공

정책을 사용해 액션 권한을 검증할 때, 두 번째 인수로 배열을 전달할 수 있습니다. 배열의 첫 번째 요소는 호출할 정책을 결정하는 데 사용되며, 나머지 요소들은 정책 메서드에 인수로 전달되어 추가 컨텍스트로 활용할 수 있습니다.

예를 들어 `$category` 추가 매개변수를 가지는 `PostPolicy` 메서드는 다음과 같습니다:

```
/**
 * 사용자가 주어진 게시글을 업데이트할 수 있는지 판단합니다.
 */
public function update(User $user, Post $post, int $category): bool
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```

게시글 업데이트 시 다음과 같이 정책 메서드를 호출합니다:

```
/**
 * 주어진 블로그 게시글 업데이트하기
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post): RedirectResponse
{
    Gate::authorize('update', [$post, $request->category]);

    // 현재 사용자가 게시글을 업데이트할 수 있음...

    return redirect('/posts');
}
```

<a name="authorization-and-inertia"></a>
## 권한 부여와 Inertia

권한 부여는 항상 서버에서 처리되어야 하지만, 프론트엔드 애플리케이션이 UI를 올바르게 렌더링하도록 권한 정보를 제공하는 것이 편리할 수 있습니다. Laravel은 Inertia 기반 프론트엔드에 권한 정보를 노출하는 규칙을 강제하지 않습니다.

그러나 Laravel의 Inertia 기반 [스타터 킷](/docs/11.x/starter-kits)을 사용하는 경우, 이미 `HandleInertiaRequests` 미들웨어가 포함되어 있습니다. 이 미들웨어의 `share` 메서드에 인자를 반환하면 모든 Inertia 페이지에 공유 데이터로 전달할 수 있습니다. 이 곳에 사용자 권한 정보를 정의하면 편리합니다:

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