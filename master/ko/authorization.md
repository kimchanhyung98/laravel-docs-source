# 권한 부여 (Authorization)

- [소개](#introduction)
- [게이트 (Gates)](#gates)
    - [게이트 작성하기](#writing-gates)
    - [게이트를 통한 작업 권한 부여](#authorizing-actions-via-gates)
    - [게이트 응답](#gate-responses)
    - [게이트 검사 가로채기](#intercepting-gate-checks)
    - [인라인 권한 부여](#inline-authorization)
- [정책 생성하기 (Creating Policies)](#creating-policies)
    - [정책 생성하기](#generating-policies)
    - [정책 등록하기](#registering-policies)
- [정책 작성하기 (Writing Policies)](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델이 필요 없는 메서드](#methods-without-models)
    - [게스트 사용자](#guest-users)
    - [정책 필터](#policy-filters)
- [정책을 사용한 작업 권한 부여](#authorizing-actions-using-policies)
    - [User 모델을 통한 권한 부여](#via-the-user-model)
    - [Gate 퍼사드를 통한 권한 부여](#via-the-gate-facade)
    - [미들웨어를 통한 권한 부여](#via-middleware)
    - [Blade 템플릿을 통한 권한 부여](#via-blade-templates)
    - [추가 컨텍스트 제공](#supplying-additional-context)
- [Authorization과 Inertia](#authorization-and-inertia)

<a name="introduction"></a>
## 소개

Laravel은 내장된 [인증(authentication)](/docs/master/authentication) 서비스를 제공하는 것 외에도, 주어진 리소스에 대하여 사용자의 작업 권한을 쉽게 관리할 수 있는 방식을 제공합니다. 예를 들어, 사용자가 인증되어 있더라도 특정 Eloquent 모델이나 애플리케이션이 관리하는 데이터베이스 레코드를 수정하거나 삭제할 권한이 없을 수 있습니다. Laravel의 권한 부여 기능은 이러한 종류의 권한 검사 관리를 쉽고 체계적으로 할 수 있게 해줍니다.

Laravel은 권한 부여를 위한 두 가지 주요 방식을 제공합니다: [게이트(gates)](#gates)와 [정책(policies)](#creating-policies). 게이트와 정책은 각각 라우트(routes)와 컨트롤러(controllers)의 관계와 비슷하게 생각할 수 있습니다. 게이트는 간단한 클로저 기반 방식을 제공하는 반면, 정책은 특정 모델이나 리소스 중심으로 권한 로직을 그룹화하는 컨트롤러 같은 역할을 합니다. 이 문서에서는 먼저 게이트를 살펴보고 이후 정책을 다룹니다.

애플리케이션을 만들 때 게이트만 또는 정책만 사용해야 하는 것은 아닙니다. 대부분의 애플리케이션은 게이트와 정책을 혼합하여 사용하며, 이는 완벽히 정상적인 방법입니다! 게이트는 관리자 대시보드와 같이 특정 모델이나 리소스와 관련 없는 작업에 가장 적합합니다. 반면, 정책은 특정 모델이나 리소스에 대한 작업 권한을 부여할 때 사용해야 합니다.

<a name="gates"></a>
## 게이트 (Gates)

<a name="writing-gates"></a>
### 게이트 작성하기

> [!WARNING]
> 게이트는 Laravel 권한 부여 기능의 기본을 배우기에 적합하지만, 견고한 Laravel 애플리케이션을 만들 때는 권한 규칙을 체계적으로 관리하기 위해 [정책](#creating-policies)의 사용을 고려해야 합니다.

게이트는 사용자가 주어진 작업을 수행할 권한이 있는지 결정하는 단순한 클로저입니다. 일반적으로 게이트는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 `Gate` 퍼사드를 사용하여 정의합니다. 게이트는 항상 첫 번째 인수로 사용자 인스턴스를 받고, 추가로 관련 Eloquent 모델 같은 인수를 받을 수도 있습니다.

아래 예시는 사용자가 특정 `App\Models\Post` 모델을 수정할 수 있는지를 판단하는 게이트를 정의합니다. 이 게이트는 사용자의 `id`가 게시글의 `user_id`와 일치하는지를 비교합니다:

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

컨트롤러처럼, 게이트도 클래스 콜백 배열로 정의할 수 있습니다:

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
### 작업 권한 부여하기

게이트를 사용해 작업 권한을 부여하려면 `Gate` 퍼사드에서 제공하는 `allows` 또는 `denies` 메서드를 사용하세요. 현재 인증된 사용자를 명시적으로 전달할 필요는 없습니다. Laravel이 게이트 클로저에 자동으로 사용자를 전달해 줍니다. 일반적으로 작업 수행을 시작하기 전에 애플리케이션 컨트롤러 내에서 게이트 권한 부여 메서드를 호출합니다:

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

        // 게시글을 업데이트...

        return redirect('/posts');
    }
}
```

현재 인증된 사용자가 아닌 다른 사용자의 권한을 확인해야 한다면 `Gate` 퍼사드의 `forUser` 메서드를 사용할 수 있습니다:

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // 사용자가 게시글을 수정할 수 있음
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // 사용자가 게시글을 수정할 수 없음
}
```

여러 작업을 한 번에 권한 확인하려면 `any`와 `none` 메서드를 사용하세요:

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // 사용자가 게시글을 수정하거나 삭제할 수 있음
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // 사용자가 게시글을 수정하거나 삭제할 수 없음
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 권한 부여 또는 예외 발생

만약 작업 권한 부여를 시도하고, 수행할 수 없으면 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 던지게 하려면 `Gate` 퍼사드의 `authorize` 메서드를 사용하세요. 이 예외는 Laravel에서 자동으로 403 HTTP 응답으로 변환합니다:

```php
Gate::authorize('update-post', $post);

// 작업 권한 부여됨...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 제공

권한 부여용 게이트 메서드 (`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`) 및 권한 부여용 [Blade 디렉티브](#via-blade-templates) (`@can`, `@cannot`, `@canany`)는 두 번째 인수로 배열을 받을 수 있습니다. 이 배열 요소들은 게이트 클로저로 전달되어 권한 판단 시 추가 상황 정보를 줄 때 사용할 수 있습니다:

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
    // 사용자가 게시글을 생성할 수 있음
}
```

<a name="gate-responses"></a>
### 게이트 응답

지금까지는 단순 boolean 값을 반환하는 게이트만 살펴보았습니다. 그러나 때로는 에러 메시지를 포함한 더 자세한 응답을 반환하고 싶을 수 있습니다. 이럴 때는 `Illuminate\Auth\Access\Response` 인스턴스를 게이트에서 반환할 수 있습니다:

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

게이트에서 권한 응답을 반환하더라도 `Gate::allows` 메서드는 여전히 단순 boolean 값을 반환합니다. 그러나 `Gate::inspect` 메서드를 사용하면 게이트가 반환한 전체 권한 응답을 얻을 수 있습니다:

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // 작업 권한 부여됨
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드를 사용할 때는 작업 권한이 없으면 `AuthorizationException`을 던지는데, 이때 권한 응답에 포함된 에러 메시지가 HTTP 응답 메시지로 전달됩니다:

```php
Gate::authorize('edit-settings');

// 작업 권한 부여됨
```

<a name="customizing-gate-response-status"></a>
#### HTTP 응답 상태 코드 사용자 정의하기

Gate에서 작업이 거부될 때 기본적으로 403 HTTP 응답이 반환됩니다. 가끔은 다른 HTTP 상태 코드를 주고 싶을 수도 있습니다. 이럴 때는 `Illuminate\Auth\Access\Response` 클래스의 정적 생성자 `denyWithStatus`를 사용해 실패한 권한 검사에 대해 반환할 HTTP 상태 코드를 지정할 수 있습니다:

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

웹 애플리케이션에서 404 응답으로 리소스를 숨기는 패턴이 매우 흔하므로, 편의상 `denyAsNotFound` 메서드도 제공합니다:

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

때로는 특정 사용자에게 모든 권한을 부여하고 싶을 수도 있습니다. 이때 `before` 메서드를 사용하여 다른 모든 권한 검사 전에 실행할 클로저를 정의할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저가 null이 아닌 값을 반환하면, 그 값이 권한 검사 결과로 간주됩니다.

또한 `after` 메서드를 사용해 다른 모든 권한 검사 후에 실행할 클로저를 정의할 수 있습니다:

```php
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after` 클로저가 반환한 값은 게이트나 정책이 `null`을 반환하지 않는 한 권한 검사 결과를 덮어쓰지 않습니다.

<a name="inline-authorization"></a>
### 인라인 권한 부여

가끔 특정 작업에 대응하는 전용 게이트를 작성하지 않고 현재 인증된 사용자가 작업 권한이 있는지 간단히 확인하고 싶을 때가 있습니다. Laravel은 `Gate::allowIf` 및 `Gate::denyIf` 메서드를 통해 이러한 종류의 "인라인" 권한 검사를 지원합니다. 인라인 권한 부여는 정의된 ["before" 또는 "after" 권한 후크](#intercepting-gate-checks)를 실행하지 않습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

작업이 허용되지 않거나, 인증된 사용자가 없으면 Laravel은 `Illuminate\Auth\Access\AuthorizationException` 예외를 자동으로 던집니다. 이 예외는 Laravel 예외 핸들러에 의해 403 HTTP 응답으로 자동 변환됩니다.

<a name="creating-policies"></a>
## 정책 생성하기 (Creating Policies)

<a name="generating-policies"></a>
### 정책 생성하기

정책은 특정 모델이나 리소스를 중심으로 권한 부여 로직을 체계적으로 관리하는 클래스입니다. 예를 들어 블로그 애플리케이션이라면, `App\Models\Post` 모델과, 게시글 생성 또는 수정 등의 사용자 작업 권한을 판단하는 `App\Policies\PostPolicy`가 있을 수 있습니다.

정책은 `make:policy` Artisan 명령어를 통해 생성할 수 있습니다. 생성된 정책 클래스는 `app/Policies` 디렉토리에 저장됩니다. 해당 디렉토리가 없으면 Laravel이 자동으로 생성합니다:

```shell
php artisan make:policy PostPolicy
```

`make:policy` 명령어는 빈 정책 클래스를 생성합니다. 만약 리소스에 대한 보기, 생성, 수정, 삭제 관련 예제 정책 메서드를 포함한 클래스를 생성하고 싶다면 `--model` 옵션을 명령어에 추가하세요:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록하기

<a name="policy-discovery"></a>
#### 정책 자동 탐지

기본적으로 Laravel은 모델과 정책의 네이밍 규칙을 따르는 한 자동으로 정책을 탐지합니다. 구체적으로, 정책은 모델이 위치한 디렉토리 위나 동일 위치의 `Policies` 디렉토리에 있어야 합니다. 예를 들어 모델은 `app/Models`에, 정책은 `app/Policies`에 있을 수도 있습니다. 이 경우 Laravel은 `app/Models/Policies`와 `app/Policies` 두 곳을 차례로 검색합니다. 또한 정책 클래스 이름은 모델 이름과 일치하고 `Policy` 접미사를 가져야 합니다. 예를 들어 `User` 모델에는 `UserPolicy` 정책 클래스를 대응시킵니다.

사용자 정의 정책 탐지 로직을 정의하려면 `Gate::guessPolicyNamesUsing` 메서드에 콜백을 등록할 수 있습니다. 이 메서드는 보통 애플리케이션의 `AppServiceProvider` 내 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // 주어진 모델에 대응하는 정책 클래스명을 반환
});
```

<a name="manually-registering-policies"></a>
#### 수동으로 정책 등록하기

`Gate` 퍼사드를 사용하여 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에서 정책과 해당 모델을 수동으로 등록할 수 있습니다:

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

정책 클래스가 등록되면, 권한 부여할 각 작업마다 메서드를 추가할 수 있습니다. 예를 들어 `PostPolicy`에 `update` 메서드를 정의하여, 특정 `App\Models\User`가 특정 `App\Models\Post` 인스턴스를 수정할 권한이 있는지 판단할 수 있습니다.

`update` 메서드는 `User`와 `Post` 인스턴스를 인수로 받고, 사용자가 주어진 게시글을 수정할 수 있으면 `true`, 그렇지 않으면 `false`를 반환해야 합니다. 아래 예는 사용자의 `id`가 게시글의 `user_id`와 일치하는지를 검사합니다:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 주어진 게시글을 사용자가 수정할 수 있는지 판단합니다.
     */
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}
```

필요에 따라 정책에 추가 메서드를 정의할 수 있습니다. 예를 들어 게시글 보기나 삭제 권한을 판단하는 `view`, `delete` 메서드를 만들 수도 있습니다. 정책 메서드는 원하는 이름을 자유롭게 사용할 수 있습니다.

`--model` 옵션을 사용해 정책을 생성했다면 `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 메서드가 이미 생성되어 있습니다.

> [!NOTE]
> 모든 정책은 Laravel [서비스 컨테이너](/docs/master/container)를 통해 해석되므로, 필요할 경우 정책의 생성자에 의존성을 타입힌트로 선언하면 자동 주입됩니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지는 정책 메서드가 단순 boolean만 반환하는 예시를 살펴봤습니다. 하지만 때로는 에러 메시지 같은 상세 정보를 포함한 응답을 반환하고 싶을 때가 있습니다. 이럴 때는 `Illuminate\Auth\Access\Response` 인스턴스를 반환할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 주어진 게시글을 사용자가 수정할 수 있는지 판단합니다.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::deny('이 게시글을 소유하고 있지 않습니다.');
}
```

정책에서 권한 응답을 반환해도 `Gate::allows` 메서드는 여전히 단순 boolean을 반환하지만, `Gate::inspect` 메서드를 사용하면 게이트에서 반환된 전체 권한 응답을 얻을 수 있습니다:

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // 작업 권한 부여됨
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드를 사용할 경우 작업 권한이 없으면 `AuthorizationException` 예외가 발생하며, 응답 메시지도 HTTP 응답에 포함됩니다:

```php
Gate::authorize('update', $post);

// 작업 권한 부여됨
```

<a name="customizing-policy-response-status"></a>
#### HTTP 응답 상태 코드 사용자 정의하기

정책 메서드에서 작업이 거부될 때 기본적으로 403 HTTP 응답을 반환하지만, 때로는 다른 상태 코드를 반환하고 싶을 수 있습니다. `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용해서 실패한 권한 검사 시 반환할 HTTP 상태 코드를 지정할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 주어진 게시글을 사용자가 수정할 수 있는지 판단합니다.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyWithStatus(404);
}
```

웹 애플리케이션에서 리소스를 404 응답으로 숨기는 패턴이 흔하므로, 편의를 위해 `denyAsNotFound` 메서드도 제공합니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 주어진 게시글을 사용자가 수정할 수 있는지 판단합니다.
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

일부 정책 메서드는 오직 현재 인증된 사용자 인스턴스만 받습니다. 이런 경우는 보통 `create` 같은 작업 권한을 결정할 때 나타납니다. 예를 들어 블로그에 게시글을 생성할 권한이 있는지 판단 시 정책 메서드는 사용자 인스턴스만 인수로 받으면 됩니다:

```php
/**
 * 주어진 사용자가 게시글을 생성할 수 있는지 판단합니다.
 */
public function create(User $user): bool
{
    return $user->role == 'writer';
}
```

<a name="guest-users"></a>
### 게스트 사용자

기본적으로 모든 게이트와 정책은 인증되지 않은 사용자의 HTTP 요청에 대해 자동으로 `false`를 반환합니다. 하지만 이 권한 검사 로직을 인증받지 않은 사용자도 사용할 수 있도록 하려면, 사용자 인수에 "optional" 타입 힌트 또는 기본값으로 `null`을 제공하면 됩니다:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 주어진 게시글을 사용자가 수정할 수 있는지 판단합니다.
     */
    public function update(?User $user, Post $post): bool
    {
        return $user?->id === $post->user_id;
    }
}
```

<a name="policy-filters"></a>
### 정책 필터

특정 사용자에게 주어진 정책 내 모든 작업 권한을 자동으로 허용하려면 정책에 `before` 메서드를 정의하세요. `before` 메서드는 정책 내 다른 메서드가 호출되기 전에 실행되어 작업을 허용할 기회를 제공합니다. 이 기능은 주로 애플리케이션 관리자가 모든 작업을 수행할 수 있도록 할 때 사용됩니다:

```php
use App\Models\User;

/**
 * 사전 권한 검사 수행.
 */
public function before(User $user, string $ability): bool|null
{
    if ($user->isAdministrator()) {
        return true;
    }

    return null;
}
```

특정 유형의 사용자에 대해 모든 권한 검사를 거부하려면 `before` 메서드에서 `false`를 반환하세요. `null`을 반환하면 권한 검사가 정책 메서드로 넘어갑니다.

> [!WARNING]
> 정책 클래스에 권한명과 일치하는 메서드가 없으면 `before` 메서드는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 사용한 작업 권한 부여

<a name="via-the-user-model"></a>
### User 모델을 통한 권한 부여

Laravel 기본 `App\Models\User` 모델에는 권한 부여를 위한 유용한 `can`과 `cannot` 메서드가 포함되어 있습니다. 이 두 메서드는 권한을 부여할 작업 이름과 관련 모델을 인수로 받습니다. 예를 들어 사용자가 특정 `App\Models\Post` 모델을 수정할 권한이 있는지 검사하는 코드는 보통 컨트롤러 메서드 내에서 다음과 같이 작성합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 주어진 게시글을 수정합니다.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if ($request->user()->cannot('update', $post)) {
            abort(403);
        }

        // 게시글 수정...

        return redirect('/posts');
    }
}
```

해당 모델에 등록된 [정책](#registering-policies)이 있다면 `can` 메서드는 자동으로 해당 정책을 호출하여 boolean 결과를 반환합니다. 정책이 등록되지 않은 모델에 대해서는 `can` 메서드가 동일 작업명을 가진 클로저 기반 게이트를 호출하려 시도합니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

일부 작업, 예를 들어 `create` 권한 부여는 모델 인스턴스를 필요로 하지 않는 정책 메서드에 대응됩니다. 이런 경우 `can` 메서드에 클래스명을 전달하세요. 클래스명을 통해 어떤 정책을 사용할지 결정합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 게시글 생성.
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
### Gate 퍼사드를 통한 권한 부여

`App\Models\User` 모델의 유용한 메서드 외에도 `Gate` 퍼사드의 `authorize` 메서드를 통해 작업 권한 부여를 할 수 있습니다.

이 메서드는 부여할 작업명과 관련 모델을 받으며, 권한이 없으면 `Illuminate\Auth\Access\AuthorizationException` 예외를 던집니다. Laravel 예외 핸들러는 이를 403 상태코드 HTTP 응답으로 자동 변환합니다:

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
     * 주어진 블로그 게시글을 수정합니다.
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        Gate::authorize('update', $post);

        // 현재 사용자가 게시글을 수정 가능함...

        return redirect('/posts');
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

앞에서 설명했듯이 `create` 같은 정책 메서드는 모델 인스턴스를 요구하지 않습니다. 이 경우 `authorize` 메서드에 클래스명을 전달하면, 어떤 정책을 사용할지 결정합니다:

```php
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

/**
 * 새로운 블로그 게시글 생성.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request): RedirectResponse
{
    Gate::authorize('create', Post::class);

    // 현재 사용자가 게시글을 생성 가능함...

    return redirect('/posts');
}
```

<a name="via-middleware"></a>
### 미들웨어를 통한 권한 부여

Laravel은 라우트 또는 컨트롤러에 도달하기 전에 작업 권한을 검사하는 미들웨어를 제공합니다. 기본적으로 `Illuminate\Auth\Middleware\Authorize` 미들웨어는 `can` [미들웨어 별칭](/docs/master/middleware#middleware-aliases)을 통해 라우트에 할당할 수 있으며, Laravel에서 자동으로 등록합니다. 예를 들어, 사용자가 게시글을 수정할 수 있는지 권한을 검사하는 `can` 미들웨어 예시는 다음과 같습니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 게시글을 수정할 수 있음...
})->middleware('can:update,post');
```

이 예제에서는 `can` 미들웨어에 두 개의 인수를 전달했습니다. 첫 번째는 권한 부여할 작업명, 두 번째는 정책 메서드에 전달할 라우트 파라미터 이름입니다. 이 예에서는 [암묵적 모델 바인딩](/docs/master/routing#implicit-binding)을 사용했으므로 라우트 파라미터 `post`에 대응하는 `App\Models\Post` 모델 인스턴스가 정책 메서드에 전달됩니다. 사용자가 작업 권한이 없으면 미들웨어가 403 상태 코드 HTTP 응답을 반환합니다.

편의를 위해 `can` 메서드를 사용해도 미들웨어 할당이 가능합니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 게시글을 수정할 수 있음...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

`create` 같은 일부 정책 메서드는 모델 인스턴스를 필요로 하지 않습니다. 이런 경우 클래스명을 미들웨어에 전달하세요. 클래스명을 근거로 어떤 정책을 사용할지 결정합니다:

```php
Route::post('/post', function () {
    // 현재 사용자가 게시글을 생성할 수 있음...
})->middleware('can:create,App\Models\Post');
```

클래스명을 문자열 미들웨어 정의에 모두 명시하는 것은 번거로울 수 있으므로, 다음과 같이 `can` 메서드를 사용해 미들웨어를 할당할 수도 있습니다:

```php
use App\Models\Post;

Route::post('/post', function () {
    // 현재 사용자가 게시글을 생성할 수 있음...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿을 통한 권한 부여

Blade 템플릿을 작성할 때 사용자가 특정 작업을 수행할 수 있는 경우에만 페이지 일부분을 보여주고 싶을 수 있습니다. 예를 들어, 사용자가 게시글을 실제로 수정할 수 있을 때에만 수정 폼을 보여주고 싶다면 `@can` 및 `@cannot` 디렉티브를 사용하세요:

```blade
@can('update', $post)
    <!-- 현재 사용자가 게시글을 수정할 수 있음... -->
@elsecan('create', App\Models\Post::class)
    <!-- 현재 사용자가 새 게시글을 생성할 수 있음... -->
@else
    <!-- 그 외 -->
@endcan

@cannot('update', $post)
    <!-- 현재 사용자가 게시글을 수정할 수 없음... -->
@elsecannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 새 게시글을 생성할 수 없음... -->
@endcannot
```

이 디렉티브들은 `@if`와 `@unless` 문을 작성하는 편리한 단축 구문입니다. 예를 들어 위 `@can`과 `@cannot` 문은 아래와 같이 작성한 것과 동일합니다:

```blade
@if (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 수정할 수 있음... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 수정할 수 없음... -->
@endunless
```

또한 사용자가 주어진 여러 작업 중 어느 하나라도 수행할 수 있는지 확인하고 싶다면 `@canany` 디렉티브를 사용하세요:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- 현재 사용자가 게시글을 수정, 조회, 또는 삭제할 수 있음... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 있음... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

다른 권한 부여 메서드와 마찬가지로, 작업에 모델 인스턴스가 필요 없으면 `@can`, `@cannot` 디렉티브에 클래스명을 전달할 수 있습니다:

```blade
@can('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글 생성 권한이 있음... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글 생성 권한이 없음... -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 컨텍스트 제공하기

정책을 사용해 작업 권한을 평가할 때, 다양한 권한 함수와 헬퍼에 두 번째 인수로 배열을 전달할 수 있습니다. 배열의 첫 번째 요소는 어떤 정책을 사용할지 결정하고, 나머지 배열 요소들은 정책 메서드에 인수로 전달되어 권한 판단 시 추가 컨텍스트로 활용됩니다. 예를 들어 다음은, 추가로 `$category` 인자를 받는 `PostPolicy`의 `update` 메서드 정의입니다:

```php
/**
 * 주어진 게시글을 사용자가 수정할 수 있는지 판단합니다.
 */
public function update(User $user, Post $post, int $category): bool
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```

이 정책 메서드를 호출하여, 인증된 사용자가 게시글을 수정할 권한이 있는지 판단하는 코드는 다음과 같습니다:

```php
/**
 * 주어진 블로그 게시글을 수정합니다.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post): RedirectResponse
{
    Gate::authorize('update', [$post, $request->category]);

    // 현재 사용자가 게시글을 수정 가능함...

    return redirect('/posts');
}
```

<a name="authorization-and-inertia"></a>
## Authorization과 Inertia

권한 부여는 항상 서버에서 처리되어야 하지만, 프론트엔드 앱에 권한 정보를 전달하여 UI를 적절하게 렌더링하는 게 편리할 때가 많습니다. Laravel은 Inertia 기반 프론트엔드에 권한 정보를 노출하는 요구 규칙을 정의하지 않습니다.

그러나 Laravel의 Inertia 기반 [스타터 킷](/docs/master/starter-kits)을 사용하는 경우, `HandleInertiaRequests` 미들웨어가 이미 애플리케이션에 포함되어 있습니다. 이 미들웨어의 `share` 메서드 내에서 모든 Inertia 페이지에 전달할 공유 데이터를 반환할 수 있습니다. 이를 권한 정보를 전달하는 편리한 장소로 사용할 수 있습니다:

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
     * 기본적으로 공유하는 props 정의.
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