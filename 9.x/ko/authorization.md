# 인증 및 권한 부여(Authorization)

- [소개](#introduction)
- [Gate](#gates)
    - [Gate 작성하기](#writing-gates)
    - [동작 권한 검사](#authorizing-actions-via-gates)
    - [Gate 응답](#gate-responses)
    - [Gate 검사 가로채기](#intercepting-gate-checks)
    - [인라인 권한 부여](#inline-authorization)
- [Policy 생성하기](#creating-policies)
    - [Policy 생성](#generating-policies)
    - [Policy 등록](#registering-policies)
- [Policy 작성하기](#writing-policies)
    - [Policy 메서드](#policy-methods)
    - [Policy 응답](#policy-responses)
    - [모델이 없는 메서드](#methods-without-models)
    - [게스트 사용자](#guest-users)
    - [Policy 필터](#policy-filters)
- [Policy를 통한 동작 권한 검사](#authorizing-actions-using-policies)
    - [User 모델을 통한 권한 검사](#via-the-user-model)
    - [컨트롤러 헬퍼를 통한 권한 검사](#via-controller-helpers)
    - [미들웨어를 통한 권한 검사](#via-middleware)
    - [Blade 템플릿을 통한 권한 검사](#via-blade-templates)
    - [추가 컨텍스트 제공](#supplying-additional-context)

<a name="introduction"></a>
## 소개

Laravel은 내장된 [인증](/docs/{{version}}/authentication) 서비스 외에도 주어진 리소스에 대해 사용자 동작을 권한 검사(Authorization)하는 간단한 방법을 제공합니다. 예를 들어, 사용자가 인증되었더라도, 여러분의 애플리케이션이 관리하는 특정 Eloquent 모델이나 데이터베이스 레코드를 업데이트 또는 삭제할 권한이 없을 수 있습니다. Laravel의 권한 부여 기능은 이러한 권한 검사 작업을 쉽고 체계적으로 처리할 수 있도록 합니다.

Laravel에서 권한을 부여하는 주요 방법은 [Gate](#gates)와 [Policy](#creating-policies) 두 가지입니다. Gate와 Policy를 각각 라우트와 컨트롤러에 비유할 수 있습니다. Gate는 클로저를 기반으로 하는 간단한 권한 검사 방법이며, Policy는 특정 모델이나 리소스와 관련된 권한 로직을 그룹화하는 방법입니다. 본 문서에서는 먼저 Gate를 살펴보고, 이어서 Policy에 대해 알아봅니다.

애플리케이션을 개발할 때 Gate만 또는 Policy만 사용해야 하는 것은 아닙니다. 대부분의 경우, 두 방법을 혼합하여 사용하는 것이 일반적이며, 이는 문제가 되지 않습니다! Gate는 관리 대시보드 보기와 같이 특정 모델과 직접 관련되지 않은 동작에 적합합니다. 반면, Policy는 특정 모델이나 리소스에 대한 동작 권한을 검사할 때 사용해야 합니다.

<a name="gates"></a>
## Gate

<a name="writing-gates"></a>
### Gate 작성하기

> **경고**
> Gate는 Laravel 권한 기능의 기본 개념을 배우기에 좋은 방법입니다. 하지만 본격적인 Laravel 애플리케이션을 작성할 때는 권한 규칙을 체계적으로 관리하기 위해 [Policy](#creating-policies) 사용을 권장합니다.

Gate는 사용자가 특정 동작을 수행할 수 있는지 판단하는 단순한 클로저(익명 함수)입니다. 일반적으로 Gate는 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드 내에서 `Gate` 퍼사드(facade)를 사용해 정의합니다. Gate는 항상 첫 번째 인자로 사용자 인스턴스를 받고, 필요에 따라 추가로 적절한 Eloquent 모델 인스턴스를 받을 수 있습니다.

아래 예시에서는 사용자가 주어진 `App\Models\Post` 모델을 업데이트할 수 있는지 결정하는 Gate를 정의합니다. 사용자 `id`와 해당 게시글의 작성자(`user_id`)가 일치하는지 확인하여 권한을 검사합니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * 인증 및 권한 서비스 등록
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

컨트롤러와 마찬가지로, Gate를 클래스 콜백 배열로도 정의할 수 있습니다:

```php
use App\Policies\PostPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * 인증 및 권한 서비스 등록
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
### 동작 권한 검사

Gate를 사용해 권한을 검사하려면 `Gate` 퍼사드의 `allows` 또는 `denies` 메서드를 사용합니다. 현재 인증된 사용자를 직접 전달할 필요는 없습니다. Laravel이 자동으로 게이트 클로저에 사용자를 주입해줍니다. 일반적으로 컨트롤러에서 권한이 필요한 동작 전에 Gate 권한 검사를 수행합니다:

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
     * 주어진 게시글을 업데이트합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Models\Post  $post
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Post $post)
    {
        if (! Gate::allows('update-post', $post)) {
            abort(403);
        }

        // 게시글 업데이트...
    }
}
```

특정 사용자가(현재 인증된 사용자가 아닌) 어떤 동작을 수행할 권한이 있는지 확인하려면 `forUser` 메서드를 사용할 수 있습니다:

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // 사용자가 게시글을 업데이트할 수 있습니다...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // 사용자가 게시글을 업데이트할 수 없습니다...
}
```

여러 동작에 대해 동시에 권한을 검사할 때는 `any` 또는 `none` 메서드를 사용할 수 있습니다:

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // 사용자가 게시글을 업데이트 또는 삭제할 수 있습니다...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // 사용자가 게시글을 업데이트 또는 삭제할 수 없습니다...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 권한 검사 및 예외 처리

권한 검사를 시도하고, 권한이 없으면 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시키려면 `Gate::authorize` 메서드를 사용할 수 있습니다. 이 예외는 Laravel의 예외 핸들러에 의해 403 HTTP 응답으로 변환됩니다:

```php
Gate::authorize('update-post', $post);

// 동작이 허가되었습니다...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 제공

권한 검사에 사용하는 Gate 메서드(`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`)와 [Blade 지시어](#via-blade-templates)(`@can`, `@cannot`, `@canany`)는 두 번째 인자에 배열을 받을 수 있습니다. 이 배열의 각 요소들은 게이트 클로저의 파라미터로 전달되어, 권한 결정을 위한 추가적인 컨텍스트로 활용할 수 있습니다:

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
    // 사용자가 게시글을 생성할 수 있습니다...
}
```

<a name="gate-responses"></a>
### Gate 응답

지금까지 Gate에서 단순히 true/false 값만 반환하는 예시를 보았습니다. 그러나 좀 더 자세한 응답(예: 오류 메시지 포함)이 필요한 경우, Gate에서 `Illuminate\Auth\Access\Response`를 반환할 수 있습니다:

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

Gate에서 권한 응답을 반환하더라도, `Gate::allows`는 여전히 단순한 불리언 값을 반환합니다. Gate의 전체 응답 객체를 받고 싶다면 `Gate::inspect` 메서드를 사용하면 됩니다:

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // 동작이 허가되었습니다...
} else {
    echo $response->message();
}
```

`Gate::authorize`를 사용하면 권한 부족 시 예외가 발생하며, 이 때 권한 응답에서 제공한 에러 메시지가 HTTP 응답에도 포함됩니다:

```php
Gate::authorize('edit-settings');

// 동작이 허가되었습니다...
```

<a name="customising-gate-response-status"></a>
#### HTTP 응답 상태 코드 커스터마이징

Gate를 통해 동작이 거부될 때 기본적으로 `403` HTTP 응답이 반환되지만, 다른 HTTP 상태 코드를 반환하고 싶은 경우도 있습니다. 이럴 때 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용할 수 있습니다:

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

리소스를 `404` 응답으로 숨기는 것이 흔히 쓰이는 패턴이기 때문에 `denyAsNotFound` 메서드도 제공합니다:

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
### Gate 검사 가로채기

특정 사용자에게 모든 권한을 부여하고 싶은 경우가 있습니다. 이럴 때 `before` 메서드로 모든 권한 검사 전에 실행되는 클로저를 등록할 수 있습니다:

```php
use Illuminate\Support\Facades\Gate;

Gate::before(function ($user, $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저가 null이 아닌 값을 반환하면 해당 값이 권한 검사 결과로 사용됩니다.

모든 권한 검사가 끝난 후 추가 작업을 하고 싶을 경우, `after` 메서드에 클로저를 등록할 수 있습니다:

```php
Gate::after(function ($user, $ability, $result, $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after` 클로저 역시 null이 아닌 값을 반환하면 결과로 사용됩니다.

<a name="inline-authorization"></a>
### 인라인 권한 부여

가끔 현재 인증된 사용자가 특정 동작에 권한이 있는지 간단히 확인하고 싶으나, 그 동작에 대응되는 Gate를 따로 생성하기 힘든 경우가 있습니다. 이런 "인라인" 권한 검사는 `Gate::allowIf`와 `Gate::denyIf` 메서드로 간단히 처리할 수 있습니다:

```php
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn ($user) => $user->isAdministrator());

Gate::denyIf(fn ($user) => $user->banned());
```

권한이 없거나 현재 인증된 사용자가 없는 경우, Laravel은 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시키며, 이 예외는 403 HTTP 응답으로 변환됩니다.

<a name="creating-policies"></a>
## Policy 생성하기

<a name="generating-policies"></a>
### Policy 생성

Policy는 특정 모델이나 리소스를 중심으로 권한 로직을 체계적으로 관리하는 클래스입니다. 예를 들어, 블로그 애플리케이션의 경우 `App\Models\Post` 모델과 사용자 게시글 생성, 수정 등의 권한을 확인하는 `App\Policies\PostPolicy`가 있을 수 있습니다.

Policy는 `make:policy` Artisan 명령어로 생성할 수 있으며, 생성된 Policy는 `app/Policies` 디렉터리에 위치합니다. 해당 디렉터리가 없으면 Laravel이 자동 생성해줍니다:

```shell
php artisan make:policy PostPolicy
```

기본적으로 비어있는 Policy 클래스가 생성됩니다. 리소스에 대한 권한 메서드(보기, 생성, 수정, 삭제 등)가 미리 들어간 예제 클래스를 만들고 싶다면 `--model` 옵션을 사용하세요:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### Policy 등록

Policy를 생성한 후에는 반드시 등록해야 합니다. Policy 등록은 특정 모델에 대한 동작 권한 검사 시 어떤 Policy를 사용할지 Laravel에 알리는 과정입니다.

새로운 Laravel 애플리케이션에는 이미 `App\Providers\AuthServiceProvider` 클래스가 포함되어 있으며, 이 클래스의 `policies` 프로퍼티에서 Eloquent 모델과 해당하는 Policy를 매핑합니다. 등록된 Policy는 주어진 Eloquent 모델에 대한 권한 검사가 필요할 때 사용됩니다:

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
     * 애플리케이션의 policy 매핑
     *
     * @var array
     */
    protected $policies = [
        Post::class => PostPolicy::class,
    ];

    /**
     * 인증/권한 서비스를 등록
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
#### Policy 자동 발견

모델 Policy를 직접 등록하지 않고, Laravel이 규칙에 따라 자동으로 찾아 사용할 수도 있습니다. 이 경우 모델과 Policy 이름이 Laravel의 표준 네이밍 컨벤션을 따라야 합니다. 구체적으로, Policy는 모델을 포함하는 디렉터리와 같거나 그 상위에 위치한 `Policies` 디렉터리에 있어야 하며, Policy 클래스 이름은 모델 이름에 `Policy` 접미사를 붙여야 합니다. 예를 들어, `User` 모델은 `UserPolicy`와 연결됩니다.

커스텀 Policy 발견 로직을 사용하고 싶다면, `Gate::guessPolicyNamesUsing` 메서드로 콜백을 등록할 수 있습니다. 보통은 애플리케이션의 `AuthServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function ($modelClass) {
    // 주어진 모델에 대한 Policy 클래스명을 반환...
});
```

> **경고**
> `AuthServiceProvider`의 `policies` 배열에 명시적으로 등록된 Policy가 있으면, 자동 발견된 Policy보다 우선 적용됩니다.

<a name="writing-policies"></a>
## Policy 작성하기

<a name="policy-methods"></a>
### Policy 메서드

Policy 클래스를 등록한 후, 각 동작에 대한 메서드를 추가할 수 있습니다. 예를 들어, `PostPolicy`에 주어진 `App\Models\User`가 특정 `App\Models\Post` 인스턴스를 업데이트할 수 있는지 확인하는 `update` 메서드를 정의할 수 있습니다.

`update` 메서드는 `User`와 `Post` 인스턴스를 인자로 받아 주어진 게시글을 수정할 권한이 있는지 여부를 true/false로 반환해야 합니다. 아래 예시에서는 사용자 `id`가 게시글 작성자 `user_id`와 일치하는지 검사합니다:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 주어진 게시글을 사용자가 업데이트할 수 있는지 판단
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

이 외에도 필요한 동작(보기, 삭제 등)에 대해 추가 메서드를 자유롭게 정의할 수 있습니다. 메서드 명칭은 원하는 대로 지정이 가능합니다.

Artisan 콘솔에서 `--model` 옵션으로 Policy를 생성하면, `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 메서드도 미리 포함되어 있습니다.

> **참고**
> 모든 Policy는 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)로 해석되므로, Policy 생성자에 필요한 의존성을 타입힌트하면 자동으로 주입받을 수 있습니다.

<a name="policy-responses"></a>
### Policy 응답

지금까지 Policy 메서드는 단순한 불리언 값만 반환했습니다. 하지만, 오류 메시지를 포함한 보다 자세한 응답을 반환하고 싶다면, Policy 메서드에서 `Illuminate\Auth\Access\Response` 인스턴스를 반환할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 주어진 게시글을 사용자가 업데이트할 수 있는지 판단
 *
 * @param  \App\Models\User  $user
 * @param  \App\Models\Post  $post
 * @return \Illuminate\Auth\Access\Response
 */
public function update(User $user, Post $post)
{
    return $user->id === $post->user_id
                ? Response::allow()
                : Response::deny('You do not own this post.');
}
```

Policy에서 권한 응답을 반환해도, `Gate::allows`는 여전히 단순한 불리언 값을 반환합니다. 전체 응답을 얻고 싶으면 `Gate::inspect`를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // 동작이 허가되었습니다...
} else {
    echo $response->message();
}
```

`Gate::authorize`를 사용하면, 권한이 없으면 예외가 발생하고, 이 때 오류 메시지가 HTTP 응답에도 포함됩니다:

```php
Gate::authorize('update', $post);

// 동작이 허가되었습니다...
```

<a name="customising-policy-response-status"></a>
#### HTTP 응답 상태 코드 커스터마이징

Policy 메서드를 통한 동작이 거부될 경우 기본적으로 `403` HTTP 응답이 반환됩니다. 그러나 실패한 권한 체크에 대해 다른 HTTP 상태 코드를 반환하고 싶다면 `denyWithStatus` 정적 생성자를 사용할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 주어진 게시글을 사용자가 업데이트할 수 있는지 판단
 *
 * @param  \App\Models\User  $user
 * @param  \App\Models\Post  $post
 * @return \Illuminate\Auth\Access\Response
 */
public function update(User $user, Post $post)
{
    return $user->id === $post->user_id
                ? Response::allow()
                : Response::denyWithStatus(404);
}
```

마찬가지로 `denyAsNotFound` 메서드를 통해 더 간단히 `404`로 처리할 수도 있습니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 주어진 게시글을 사용자가 업데이트할 수 있는지 판단
 *
 * @param  \App\Models\User  $user
 * @param  \App\Models\Post  $post
 * @return \Illuminate\Auth\Access\Response
 */
public function update(User $user, Post $post)
{
    return $user->id === $post->user_id
                ? Response::allow()
                : Response::denyAsNotFound();
}
```

<a name="methods-without-models"></a>
### 모델이 없는 메서드

일부 Policy 메서드는 현재 인증된 사용자 인스턴스만을 인자로 받습니다. 주로 `create` 동작의 권한을 검사할 때 해당 상황이 많습니다. 예를 들어 블로그에서 사용자가 게시글을 생성할 수 있는지 확인하려면 다음과 같이 정의할 수 있습니다:

```php
/**
 * 사용자가 게시글을 생성할 수 있는지 판단
 *
 * @param  \App\Models\User  $user
 * @return bool
 */
public function create(User $user)
{
    return $user->role == 'writer';
}
```

<a name="guest-users"></a>
### 게스트 사용자

기본적으로 인증되지 않은 사용자의 HTTP 요청에 대해 모든 Gate와 Policy는 자동으로 `false`를 반환합니다. 그러나, 게스트 사용자에 대해서도 권한 검사가 통과되길 원한다면, Policy 메서드의 사용자 인자를 "nullable" 타입힌트하거나 기본값을 `null`로 지정해주면 됩니다:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 주어진 게시글을 사용자가 업데이트할 수 있는지 판단
     *
     * @param  \App\Models\User|null  $user
     * @param  \App\Models\Post  $post
     * @return bool
     */
    public function update(?User $user, Post $post)
    {
        return optional($user)->id === $post->user_id;
    }
}
```

<a name="policy-filters"></a>
### Policy 필터

특정 사용자에 대해 Policy 내의 모든 동작을 권한 부여하고 싶을 때, Policy 클래스에 `before` 메서드를 정의하세요. 이 메서드는 Policy의 다른 모든 메서드보다 먼저 실행되어 권한 여부를 미리 결정할 기회를 제공합니다. 주로 어드민(관리자) 등에게 전권을 허용할 때 사용합니다:

```php
use App\Models\User;

/**
 * 사전 인증(Pre-Authorization) 검사
 *
 * @param  \App\Models\User  $user
 * @param  string  $ability
 * @return void|bool
 */
public function before(User $user, $ability)
{
    if ($user->isAdministrator()) {
        return true;
    }
}
```

특정 유형의 사용자의 모든 권한을 거부하고 싶다면, `before`에서 `false`를 반환하세요. `null`을 반환하면, 해당 권한 검사는 Policy의 해당 메서드로 넘어갑니다.

> **경고**
> Policy 클래스에 검사하려는 동작명(ability)과 일치하는 메서드가 없다면 `before` 메서드는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## Policy를 통한 동작 권한 검사

<a name="via-the-user-model"></a>
### User 모델을 통한 권한 검사

Laravel에 기본 포함된 `App\Models\User`에는 권한 검사에 유용한 `can` 및 `cannot` 메서드가 있습니다. 두 메서드는 권한을 검사할 동작명과 관련 모델을 전달받아 권한 여부를 확인합니다. 예를 들어, 특정 `App\Models\Post` 인스턴스에 대해 사용자가 업데이트 권한이 있는지 컨트롤러에서 검사하려면 다음과 같이 작성할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 주어진 게시글을 업데이트합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Models\Post  $post
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Post $post)
    {
        if ($request->user()->cannot('update', $post)) {
            abort(403);
        }

        // 게시글을 업데이트합니다...
    }
}
```

해당 모델에 [Policy가 등록](#registering-policies)되어 있다면, `can` 메서드는 자동으로 알맞은 Policy를 호출하고 불리언 결과를 반환합니다. Policy가 없다면 이름이 일치하는 Gate를 호출합니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 동작

`create`와 같이 모델 인스턴스가 필요 없는 동작에 해당하는 Policy 메서드도 있습니다. 이 경우 클래스명을 `can` 메서드에 넘기면 어떤 Policy를 사용할지 자동으로 판단합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 게시글을 생성합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        if ($request->user()->cannot('create', Post::class)) {
            abort(403);
        }

        // 게시글을 생성합니다...
    }
}
```

<a name="via-controller-helpers"></a>
### 컨트롤러 헬퍼를 통한 권한 검사

`App\Models\User`에서도 다양한 권한 메서드를 제공하지만, Laravel의 컨트롤러(Controller)에서는 `authorize`라는 헬퍼 메서드를 사용할 수 있습니다. 이 메서드는 검사할 동작명과 모델을 받아, 권한이 없으면 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시킵니다. 이 예외는 Laravel에서 자동으로 403 응답으로 변환됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 주어진 블로그 게시글을 업데이트합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Models\Post  $post
     * @return \Illuminate\Http\Response
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post)
    {
        $this->authorize('update', $post);

        // 현재 사용자가 게시글을 업데이트할 수 있습니다...
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 동작

이미 설명했듯이, `create`처럼 모델 인스턴스가 필요 없는 동작에 대해선 클래스명을 `authorize`에 전달합니다. 어떤 Policy를 사용할지 결정하는 데 활용됩니다:

```php
use App\Models\Post;
use Illuminate\Http\Request;

/**
 * 새 블로그 게시글을 생성합니다.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\Response
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request)
{
    $this->authorize('create', Post::class);

    // 현재 사용자가 게시글을 생성할 수 있습니다...
}
```

<a name="authorizing-resource-controllers"></a>
#### 리소스 컨트롤러의 권한 검사

[리소스 컨트롤러](/docs/{{version}}/controllers#resource-controllers)를 사용할 때는 생성자에서 `authorizeResource` 메서드를 이용해 `can` 미들웨어를 각 메서드에 자동으로 할당할 수 있습니다.

`authorizeResource`의 첫 번째 인자는 모델 클래스명이고, 두 번째 인자는 라우트/요청 파라미터에서 해당 모델의 ID를 담고 있는 키입니다. [리소스 컨트롤러](/docs/{{version}}/controllers#resource-controllers)를 `--model` 플래그로 생성해, 필요한 시그니처와 타입힌트가 포함되도록 해야 합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 컨트롤러 인스턴스 생성
     *
     * @return void
     */
    public function __construct()
    {
        $this->authorizeResource(Post::class, 'post');
    }
}
```

아래는 컨트롤러 메서드와 Policy 메서드 간의 매핑 테이블입니다. 요청이 컨트롤러 메서드로 라우팅될 때마다 해당 Policy의 메서드가 자동으로 호출됩니다:

| 컨트롤러 메서드 | Policy 메서드 |
| --- | --- |
| index | viewAny |
| show | view |
| create | create |
| store | create |
| edit | update |
| update | update |
| destroy | delete |

> **참고**
> `make:policy` 명령을 `--model` 플래그와 함께 사용하면 주어진 모델에 대한 Policy 클래스를 빠르게 생성할 수 있습니다:  
> `php artisan make:policy PostPolicy --model=Post`

<a name="via-middleware"></a>
### 미들웨어를 통한 권한 검사

Laravel은 요청이 라우트나 컨트롤러에 도달하기 전에 권한을 검사할 수 있도록 `can` 미들웨어를 제공합니다. 기본적으로, `Illuminate\Auth\Middleware\Authorize` 미들웨어는 `App\Http\Kernel` 클래스에서 `can` 키에 할당되어 있습니다. 아래는 게시글을 업데이트할 권한을 `can` 미들웨어로 검사하는 예시입니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 게시글을 업데이트할 수 있습니다...
})->middleware('can:update,post');
```

여기서 첫 번째 인자는 권한 검사 동작명, 두 번째 인자는 Policy 메서드에 전달할 라우트 파라미터입니다. [암시적 모델 바인딩](/docs/{{version}}/routing#implicit-binding)을 사용하기 때문에 `App\Models\Post` 모델이 Policy로 전달됩니다. 권한이 없으면 403 상태코드의 HTTP 응답이 반환됩니다.

좀 더 편리하게 라우트에 `can` 미들웨어를 바로 연결하는 `can` 메서드를 사용할 수도 있습니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 게시글을 업데이트할 수 있습니다...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 동작

`create`처럼 Policy 메서드에 모델 인스턴스가 필요 없는 경우, 클래스명을 미들웨어에 직접 전달할 수 있습니다:

```php
Route::post('/post', function () {
    // 현재 사용자가 게시글을 생성할 수 있습니다...
})->middleware('can:create,App\Models\Post');
```

문자열로 클래스명을 지정하는 것이 번거로울 경우, 역시 `can` 메서드를 사용하는 것이 용이합니다:

```php
use App\Models\Post;

Route::post('/post', function () {
    // 현재 사용자가 게시글을 생성할 수 있습니다...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿을 통한 권한 검사

Blade 템플릿에서 사용자가 특정 동작을 수행할 권한이 있을 때만 일부 페이지를 보여주고 싶은 경우가 있습니다. 예를 들어, 게시글 수정 폼을 보여주는 경우, 사용자가 실제로 게시글을 수정할 수 있는지 확인해야 합니다. 이럴 때는 `@can`과 `@cannot` 지시어를 사용할 수 있습니다:

```blade
@can('update', $post)
    <!-- 현재 사용자가 게시글을 업데이트할 수 있습니다... -->
@elsecan('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 새로 만들 수 있습니다... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- 현재 사용자가 게시글을 업데이트할 수 없습니다... -->
@elsecannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 새로 만들 수 없습니다... -->
@endcannot
```

이 지시어들은 `@if` 및 `@unless` 문을 사용하는 간편한 방법입니다. 위의 `@can` 및 `@cannot` 구문은 다음과 동일합니다:

```blade
@if (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 업데이트할 수 있습니다... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 업데이트할 수 없습니다... -->
@endunless
```

주어진 여러 동작 중 사용자가 하나라도 권한이 있을 경우 블록을 노출하고 싶으면 `@canany` 지시어를 사용할 수 있습니다:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- 현재 사용자가 게시글을 업데이트, 보기 또는 삭제할 수 있습니다... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 있습니다... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델 인스턴스가 필요 없는 동작

다른 권한 검사 방법들처럼, 모델 인스턴스가 필요 없는 동작에 대해 `@can` 및 `@cannot` 지시어에 클래스명을 전달할 수 있습니다:

```blade
@can('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 있습니다... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 없습니다... -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 컨텍스트 제공

Policy를 통해 권한을 검사할 때, 여러 authorization 함수와 헬퍼에 두 번째 인자로 배열을 전달할 수 있습니다. 이 배열의 첫 번째 요소는 호출할 Policy를 결정하는 데 사용되며, 나머지는 Policy 메서드의 인자로 전달되어 추가 컨텍스트로 활용할 수 있습니다. 다음은 $category라는 인자를 추가로 받는 `PostPolicy` 예시입니다:

```php
/**
 * 주어진 게시글을 사용자가 업데이트할 수 있는지 판단
 *
 * @param  \App\Models\User  $user
 * @param  \App\Models\Post  $post
 * @param  int  $category
 * @return bool
 */
public function update(User $user, Post $post, int $category)
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```

이 Policy 메서드를 사용할 때는 아래와 같이 추가 인자를 배열로 전달하면 됩니다:

```php
/**
 * 주어진 블로그 게시글을 업데이트합니다.
 *
 * @param  \Illuminate\Http\Request  $request
 * @param  \App\Models\Post  $post
 * @return \Illuminate\Http\Response
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post)
{
    $this->authorize('update', [$post, $request->category]);

    // 현재 사용자가 게시글을 업데이트할 수 있습니다...
}
```