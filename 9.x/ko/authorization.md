# 권한부여 (Authorization)

- [소개](#introduction)
- [게이트 (Gates)](#gates)
    - [게이트 작성하기](#writing-gates)
    - [게이트를 통한 작업 권한 부여](#authorizing-actions-via-gates)
    - [게이트 응답](#gate-responses)
    - [게이트 체크 인터셉트](#intercepting-gate-checks)
    - [인라인 권한부여](#inline-authorization)
- [정책 만들기 (Creating Policies)](#creating-policies)
    - [정책 생성](#generating-policies)
    - [정책 등록](#registering-policies)
- [정책 작성하기](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델이 필요 없는 메서드](#methods-without-models)
    - [게스트 사용자](#guest-users)
    - [정책 필터](#policy-filters)
- [정책을 사용한 작업 권한 부여](#authorizing-actions-using-policies)
    - [User 모델을 통한 방법](#via-the-user-model)
    - [컨트롤러 헬퍼를 통한 방법](#via-controller-helpers)
    - [미들웨어를 통한 방법](#via-middleware)
    - [Blade 템플릿을 통한 방법](#via-blade-templates)
    - [추가 컨텍스트 제공하기](#supplying-additional-context)

<a name="introduction"></a>
## 소개

Laravel은 내장된 [인증(authentication)](/docs/9.x/authentication) 서비스뿐만 아니라, 특정 리소스에 대해 사용자의 작업 권한을 간단히 검증할 수 있는 방법도 제공합니다. 예를 들어, 사용자가 인증되었더라도 해당 사용자가 애플리케이션에서 관리하는 특정 Eloquent 모델이나 데이터베이스 레코드를 업데이트하거나 삭제할 권한이 없을 수 있습니다. Laravel에서 제공하는 권한부여 기능은 이러한 유형의 권한 검증을 쉽고 체계적으로 관리할 수 있도록 돕습니다.

Laravel은 권한부여를 위한 두 가지 주요 방식을 제공합니다: [게이트 (gates)](#gates)와 [정책 (policies)](#creating-policies). 게이트와 정책을 라우트(routes)와 컨트롤러(controllers)에 비유할 수 있습니다. 게이트는 간단하고 클로저 기반의 권한부여 방식을 제공하고, 정책은 컨트롤러처럼 특정 모델이나 리소스에 관한 권한부여 로직을 그룹화합니다. 이 문서에서는 게이트를 먼저 살펴보고 이후 정책을 다루겠습니다.

애플리케이션을 구축할 때는 게이트만 사용하거나 정책만 사용해야 하는 것은 아닙니다. 대부분의 애플리케이션은 게이트와 정책을 혼합하여 사용하는 경우가 많으며, 이는 전혀 문제되지 않습니다! 게이트는 관리자 대시보드 보기처럼 특정 모델이나 리소스와 관련 없는 작업에 적합합니다. 반면에, 특정 모델이나 리소스에 대해 작업 권한을 부여하고자 한다면 정책을 사용하는 것이 좋습니다.

<a name="gates"></a>
## 게이트 (Gates)

<a name="writing-gates"></a>
### 게이트 작성하기

> [!WARNING]
> 게이트는 Laravel 권한부여 기능의 기본을 익히기에 좋습니다. 하지만 견고한 Laravel 애플리케이션 개발 시에는 권한부여 규칙을 체계적으로 정리할 수 있는 [정책](#creating-policies) 사용을 고려하세요.

게이트는 사용자가 특정 작업을 수행할 권한이 있는지 판단하는 클로저(Closure)입니다. 일반적으로, `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드 안에서 `Gate` 파사드를 사용해 게이트를 정의합니다. 게이트는 항상 첫 번째 인수로 사용자 인스턴스를 받으며, 필요에 따라 관련 Eloquent 모델과 같은 추가 인수를 받을 수도 있습니다.

다음 예제에서는, 사용자가 특정 `App\Models\Post` 모델을 업데이트할 수 있는지 판단하는 게이트를 정의합니다. 이 게이트는 사용자의 `id`가 게시글을 작성한 사용자의 `user_id`와 같은지 비교하는 방식으로 권한을 확인합니다:

```
use App\Models\Post;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Register any authentication / authorization services.
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

컨트롤러처럼, 게이트는 클래스 콜백 배열을 사용해 정의할 수도 있습니다:

```
use App\Policies\PostPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * Register any authentication / authorization services.
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
### 게이트를 통한 작업 권한 부여

게이트를 사용해 작업을 권한부여하려면 `Gate` 파사드의 `allows` 또는 `denies` 메서드를 사용합니다. 현재 인증된 사용자를 해당 메서드에 직접 전달할 필요는 없습니다. Laravel이 게이트 클로저에 사용자를 자동으로 전달합니다. 애플리케이션 컨트롤러 내에서 보통 작업 실행 전 권한 확인을 위해 이 메서드를 호출합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class PostController extends Controller
{
    /**
     * Update the given post.
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

        // 게시글 업데이트 로직...
    }
}
```

현재 인증된 사용자가 아닌 다른 사용자의 권한을 확인하려면 `Gate` 파사드의 `forUser` 메서드를 사용하세요:

```
if (Gate::forUser($user)->allows('update-post', $post)) {
    // 사용자가 게시글을 업데이트할 수 있음...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // 사용자가 게시글을 업데이트할 수 없음...
}
```

`any` 또는 `none` 메서드를 사용하면 여러 권한을 한 번에 확인할 수 있습니다:

```
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // 사용자가 게시글을 업데이트하거나 삭제할 수 있음...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // 사용자가 게시글을 업데이트하거나 삭제할 수 없음...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 권한부여 또는 예외 발생

특정 작업에 대한 권한을 시도하면서, 권한이 없으면 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시키고 싶다면 `Gate` 파사드의 `authorize` 메서드를 사용하세요. `AuthorizationException` 인스턴스는 Laravel 예외 핸들러에 의해 자동으로 403 HTTP 응답으로 변환됩니다:

```
Gate::authorize('update-post', $post);

// 작업 권한 부여됨...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 제공하기

권한 부여를 위한 게이트 메서드(`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`)와 권한 관련 [Blade 디렉티브](#via-blade-templates) (`@can`, `@cannot`, `@canany`)의 두 번째 인수로 배열을 받을 수 있습니다. 이 배열 요소들은 게이트 클로저의 매개변수로 전달되어 권한 부여 판단 시 추가 컨텍스트로 활용할 수 있습니다:

```
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
    // 사용자가 게시글을 생성할 수 있음...
}
```

<a name="gate-responses"></a>
### 게이트 응답

지금까지는 단순 boolean 값을 반환하는 게이트를 살펴봤습니다. 하지만 때로는 에러 메시지를 포함한 더 상세한 응답을 반환하고 싶을 수 있습니다. 이럴 때는 게이트에서 `Illuminate\Auth\Access\Response`를 반환할 수 있습니다:

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

권한 응답을 반환하더라도 `Gate::allows` 메서드는 여전히 단순 boolean 값을 반환합니다. 그러나 `Gate::inspect` 메서드를 사용하면 게이트에서 반환된 전체 권한 응답을 받을 수 있습니다:

```
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // 작업 권한 부여됨...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드를 사용해 작업 권한이 없으면 `AuthorizationException` 예외를 던질 때, 권한 응답의 에러 메시지는 HTTP 응답에 포함되어 전파됩니다:

```
Gate::authorize('edit-settings');

// 작업 권한 부여됨...
```

<a name="customising-gate-response-status"></a>
#### HTTP 응답 상태 코드 커스터마이징

게이트에서 작업을 거부할 경우 기본으로 403 HTTP 상태 코드가 반환됩니다. 그러나 때때로 다른 HTTP 상태 코드를 응답하는 게 유용할 수 있습니다. 이럴 때 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용해 실패 응답 코드를 지정할 수 있습니다:

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

웹 애플리케이션에서 자원을 숨기기 위해 404 응답을 반환하는 것이 흔한 패턴이라 `denyAsNotFound` 메서드도 제공합니다:

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
### 게이트 체크 인터셉트

특정 사용자에게 모든 권한을 부여하고 싶을 때가 있습니다. 이때 `before` 메서드를 활용해 모든 권한부여 체크가 실행되기 전에 실행되는 클로저를 정의할 수 있습니다:

```
use Illuminate\Support\Facades\Gate;

Gate::before(function ($user, $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저가 `null`이 아닌 값을 반환하면 그 값이 권한 체크 결과로 간주되어 이후 권한 검사 로직은 실행되지 않습니다.

마찬가지로 `after` 메서드로 모든 권한 부여 체크 후 실행될 클로저를 정의할 수 있습니다:

```
Gate::after(function ($user, $ability, $result, $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after` 클로저도 `null`이 아닌 값을 반환하면 그 값이 결과로 간주됩니다.

<a name="inline-authorization"></a>
### 인라인 권한부여

경우에 따라, 해당 작업에 대한 전용 게이트를 작성하지 않고 현재 인증된 사용자가 권한을 가지고 있는지 바로 확인하고 싶을 수 있습니다. 이럴 때는 `Gate::allowIf` 및 `Gate::denyIf` 메서드를 이용한 "인라인" 권한부여를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn ($user) => $user->isAdministrator());

Gate::denyIf(fn ($user) => $user->banned());
```

권한이 없거나 현재 인증된 사용자가 없으면 Laravel은 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시킵니다. 이 예외는 Laravel 예외 처리기에 의해 403 HTTP 응답으로 변환됩니다.

<a name="creating-policies"></a>
## 정책 만들기 (Creating Policies)

<a name="generating-policies"></a>
### 정책 생성

정책은 특정 모델이나 리소스 주위에 권한부여 로직을 정리하는 클래스입니다. 예를 들어 블로그 애플리케이션을 만든다면, `App\Models\Post` 모델과 해당 모델 관련 작업(작성, 수정 등)을 권한부여하는 `App\Policies\PostPolicy` 클래스가 있을 수 있습니다.

`make:policy` Artisan 명령어로 정책을 생성할 수 있으며, 생성된 정책 파일은 `app/Policies` 디렉터리에 저장됩니다. 만약 해당 디렉터리가 없다면 Laravel이 자동으로 생성합니다:

```shell
php artisan make:policy PostPolicy
```

`make:policy` 명령어는 기본적으로 비어있는 정책 클래스를 생성합니다. 만약 `--model` 옵션을 지정하면 `view`, `create`, `update`, `delete` 등 리소스와 관련된 예제 정책 메서드가 포함된 클래스를 생성합니다:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록

정책 클래스를 만든 후에는 이를 등록해야 합니다. 정책 등록은 Laravel에 특정 Eloquent 모델에 대해 어떤 정책을 사용할지 알려주는 역할을 합니다.

Laravel 새 프로젝트에 포함된 `App\Providers\AuthServiceProvider` 클래스 안에는 `policies` 속성이 있어 Eloquent 모델과 정책 클래스를 매핑합니다. 정책을 등록하면 Laravel에서 해당 모델 권한부여 시 어느 정책을 참조해야 하는지 지정할 수 있습니다:

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
#### 정책 자동 탐색

정책을 수동 등록하는 대신, Laravel은 모델과 정책이 표준 명명 규칙을 따르면 자동으로 정책을 찾아 사용할 수 있습니다. 구체적으로, 정책은 모델보다 상위 디렉터리(또는 같은 위치)의 `Policies` 디렉터리에 있어야 합니다. 예를 들어, 모델 파일은 `app/Models`에 있고 정책은 `app/Policies`에 있다면, Laravel은 먼저 `app/Models/Policies`를, 그다음 `app/Policies`를 확인합니다. 또한 정책 이름은 모델 이름과 같아야 하며 `Policy` 접미사가 붙어야 합니다. 예컨대 `User` 모델이면 `UserPolicy`가 대응 정책입니다.

직접 정책 탐색 로직을 정의하려면 `Gate::guessPolicyNamesUsing` 메서드에 커스텀 콜백을 등록할 수 있습니다. 보통 이 메서드는 애플리케이션의 `AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function ($modelClass) {
    // 주어진 모델에 대응하는 정책 클래스명을 반환...
});
```

> [!WARNING]
> 명시적으로 `AuthServiceProvider`에 등록된 정책은 자동 탐색 정책보다 우선 적용됩니다.

<a name="writing-policies"></a>
## 정책 작성하기

<a name="policy-methods"></a>
### 정책 메서드

정책 클래스가 등록되면 각 작업 권한부여를 위한 메서드를 추가할 수 있습니다. 예를 들어 `PostPolicy`에서 `update` 메서드를 정의해 특정 `App\Models\User`가 특정 `App\Models\Post`를 수정할 권한이 있는지 판단하도록 할 수 있습니다.

`update` 메서드는 `User` 인스턴스와 `Post` 인스턴스를 인수로 받고, 사용자가 해당 게시글을 수정할 권한이 있으면 `true`, 없으면 `false`를 반환해야 합니다. 예로 사용자 `id`와 게시글의 `user_id`가 같은지 확인합니다:

```
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the given post can be updated by the user.
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

필요에 따라 정책에 다양한 작업 메서드를 계속 추가할 수 있습니다. 예를 들어 `view`, `delete` 메서드를 추가해 여러 게시글 관련 작업 권한을 제어할 수 있습니다. 정책 메서드는 원하는 이름으로 자유롭게 작성할 수 있습니다.

Artisan 콘솔에서 `--model` 옵션을 사용해 정책을 생성했다면, `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 메서드가 기본으로 포함되어 있습니다.

> [!NOTE]
> 모든 정책은 Laravel [서비스 컨테이너](/docs/9.x/container)를 통해 해결되므로, 정책 생성자에 필요한 의존성을 타입힌트하면 자동으로 주입됩니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지는 단순 boolean을 반환하는 정책 메서드를 봤습니다. 하지만, 에러 메시지 등 더 자세한 응답을 반환하고 싶을 때가 있습니다. 이럴 때는 정책 메서드에서 `Illuminate\Auth\Access\Response` 인스턴스를 반환할 수 있습니다:

```
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 *
 * @param  \App\Models\User  $user
 * @param  \App\Models\Post  $post
 * @return \Illuminate\Auth\Access\Response
 */
public function update(User $user, Post $post)
{
    return $user->id === $post->user_id
                ? Response::allow()
                : Response::deny('이 게시글을 소유하고 있지 않습니다.');
}
```

정책에서 권한 응답을 반환하더라도 `Gate::allows` 메서드는 여전히 boolean 값을 반환합니다. 그러나 `Gate::inspect` 메서드를 사용하면 게이트에서 반환된 전체 권한 응답 객체를 조회할 수 있습니다:

```
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // 작업 권한 부여됨...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드를 사용 시 권한이 없으면 `AuthorizationException` 예외가 발생하며, 응답 메시지는 HTTP 응답에 포함됩니다:

```
Gate::authorize('update', $post);

// 작업 권한 부여됨...
```

<a name="customising-policy-response-status"></a>
#### HTTP 응답 상태 코드 커스터마이징

정책 메서드가 권한을 거부할 때 기본으로 403 HTTP 응답이 반환됩니다. 그러나 다른 HTTP 상태 코드를 반환하고 싶을 수 있습니다. 이때 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용해 응답 코드를 지정할 수 있습니다:

```
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
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

웹 애플리케이션에서 자원을 숨길 때 404 응답을 반환하는 경우가 많아, `denyAsNotFound` 메서드도 편의용으로 제공합니다:

```
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
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
### 모델이 필요 없는 메서드

일부 정책 메서드는 현재 인증된 사용자 인스턴스만 받습니다. 이는 `create` 작업 권한부여에 가장 흔한 경우입니다. 예를 들어, 앱에서 사용자가 게시글을 아예 생성할 권한이 있는지 판단하려면, 정책 메서드에 사용자 인수만 전달합니다:

```
/**
 * Determine if the given user can create posts.
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

기본적으로, 게이트와 정책 모두 인증되지 않은 요청에 대해 자동으로 `false`를 반환합니다. 하지만 이 체크를 통과시키고 싶으면 사용자 인수에 "nullable" 타입힌트(`?User`)를 선언하거나 기본값을 `null`로 줄 수 있습니다:

```
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the given post can be updated by the user.
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
### 정책 필터

특정 사용자에게 해당 정책 내 모든 권한을 부여하고 싶을 때가 있습니다. 이를 위해 정책 클래스에 `before` 메서드를 정의할 수 있습니다. 이 메서드는 정책 내 다른 메서드가 호출되기 전에 실행되어 권한 부여를 처리할 수 있습니다. 주로 애플리케이션 관리자에게 모든 권한을 허용할 때 사용합니다:

```
use App\Models\User;

/**
 * Perform pre-authorization checks.
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

특정 유형 사용자에 대해 모든 권한을 거부하려면 `before` 메서드에서 `false`를 반환하면 됩니다. `null`을 반환하면 실제 정책 메서드로 넘어갑니다.

> [!WARNING]
> 권한체크하는 이름과 일치하는 메서드가 정책 클래스에 없으면 `before` 메서드는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 사용한 작업 권한 부여

<a name="via-the-user-model"></a>
### User 모델을 통한 방법

Laravel 기본 제공 `App\Models\User` 모델에는 작업 권한부여 메서드인 `can`과 `cannot`이 포함되어 있습니다. 이 메서드는 권한을 확인하려는 작업명과 관련 모델을 인수로 받습니다. 예를 들어, 사용자가 특정 `App\Models\Post` 모델을 수정할 권한이 있는지 확인하는 상황입니다. 일반적으로 컨트롤러 메서드 내에서 이 작업을 수행합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Update the given post.
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

        // 게시글 업데이트 로직...
    }
}
```

해당 모델에 [정책이 등록되어 있다면](#registering-policies), `can` 메서드는 자동으로 적절한 정책 메서드를 호출해 boolean 결과를 반환합니다. 정책이 없다면, 클로저 기반 게이트에서 같은 이름의 작업을 찾으려 시도합니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

앞서 말했듯이, `create` 같은 일부 작업은 모델 인스턴스를 요구하지 않습니다. 이런 경우 `can` 메서드에 클래스 이름을 넘길 수 있습니다. Laravel은 권한부여 시 이 클래스 이름으로 어떤 정책을 참조해야 하는지 판단합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Create a post.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        if ($request->user()->cannot('create', Post::class)) {
            abort(403);
        }

        // 게시글 생성 로직...
    }
}
```

<a name="via-controller-helpers"></a>
### 컨트롤러 헬퍼를 통한 방법

`App\Models\User` 모델에 포함된 유용한 메서드 외에도, Laravel은 `App\Http\Controllers\Controller`를 확장하는 모든 컨트롤러에 `authorize` 메서드를 제공합니다.

이 메서드는 권한 확인할 작업명과 관련 모델을 받습니다. 권한이 없으면 `Illuminate\Auth\Access\AuthorizationException` 예외를 던지며, Laravel 예외 핸들러가 자동으로 403 HTTP 응답으로 변환합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Update the given blog post.
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

        // 현재 사용자가 해당 블로그 게시글을 수정할 수 있음...
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

앞서 언급했듯, `create` 같은 작업은 모델 인스턴스를 요구하지 않습니다. 이런 경우 `authorize` 메서드에 클래스 이름을 지정할 수 있습니다:

```
use App\Models\Post;
use Illuminate\Http\Request;

/**
 * Create a new blog post.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\Response
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request)
{
    $this->authorize('create', Post::class);

    // 현재 사용자가 블로그 게시글을 생성할 수 있음...
}
```

<a name="authorizing-resource-controllers"></a>
#### 리소스 컨트롤러 권한 부여

[리소스 컨트롤러](/docs/9.x/controllers#resource-controllers)를 사용할 때는 컨트롤러 생성자에서 `authorizeResource` 메서드를 활용할 수 있습니다. 이 메서드는 리소스 컨트롤러의 각 메서드에 적절한 `can` 미들웨어를 자동으로 연결합니다.

`authorizeResource`는 첫 번째 인수로 모델 클래스명, 두 번째 인수로 라우트/요청 파라미터 이름을 받습니다. 리소스 컨트롤러는 `--model` 플래그로 생성해 필요한 메서드 시그니처와 타입힌트를 포함하도록 해야 합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Create the controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->authorizeResource(Post::class, 'post');
    }
}
```

컨트롤러 메서드는 다음과 같이 해당 정책 메서드와 자동 매핑됩니다. 해당 컨트롤러 메서드에 라우팅된 요청이 들어오면 정책 메서드의 권한부여가 자동으로 수행됩니다:

| 컨트롤러 메서드 | 정책 메서드 |
| --- | --- |
| index | viewAny |
| show | view |
| create | create |
| store | create |
| edit | update |
| update | update |
| destroy | delete |

> [!NOTE]
> `make:policy` 명령어에 `--model` 옵션을 추가하면 지정 모형에 맞춘 정책 클래스를 빠르게 생성할 수 있습니다:  
> `php artisan make:policy PostPolicy --model=Post`

<a name="via-middleware"></a>
### 미들웨어를 통한 방법

Laravel은 요청이 라우트나 컨트롤러에 도달하기 전에 권한을 검증하는 미들웨어를 제공합니다. 기본적으로 `Illuminate\Auth\Middleware\Authorize` 미들웨어가 `App\Http\Kernel`에 `can` 키로 할당되어 있습니다. `can` 미들웨어를 사용하여 사용자가 게시글을 수정할 권한이 있는지 검사하는 예제를 보겠습니다:

```
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 게시글을 수정할 수 있음...
})->middleware('can:update,post');
```

위 예에서 미들웨어에 두 개의 인자를 넘깁니다. 첫 번째는 권한 부여할 작업명, 두 번째는 정책 메서드에 전달할 라우트 파라미터 이름입니다. 여기서는 [암묵적 모델 바인딩](/docs/9.x/routing#implicit-binding) 덕분에 `App\Models\Post` 모델 인스턴스가 정책 메서드에 전달됩니다. 사용자가 권한이 없으면 미들웨어가 403 HTTP 응답을 반환합니다.

편의상, `can` 메서드를 사용해 라우트에 미들웨어를 붙일 수도 있습니다:

```
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 게시글을 수정할 수 있음...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

`create` 같은 정책 메서드는 모델 인스턴스가 필요 없습니다. 이런 경우 미들웨어에 클래스 이름을 전달할 수 있습니다. 그 클래스를 바탕으로 어떤 정책을 참조할지 결정합니다:

```
Route::post('/post', function () {
    // 현재 사용자가 게시글을 생성할 수 있음...
})->middleware('can:create,App\Models\Post');
```

미들웨어 정의에 클래스 이름 전체를 문자열로 쓰는 대신, `can` 메서드를 사용해 라우트에 미들웨어를 붙일 수도 있습니다:

```
use App\Models\Post;

Route::post('/post', function () {
    // 현재 사용자가 게시글을 생성할 수 있음...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿을 통한 방법

Blade 템플릿 작성 시, 사용자가 특정 작업 권한을 가졌을 때만 페이지 일부분을 보여주고 싶을 수 있습니다. 예를 들어, 사용자가 게시글 수정 권한이 있을 때 수정 폼을 보여주는 경우입니다. 이때 `@can`과 `@cannot` 디렉티브를 활용할 수 있습니다:

```blade
@can('update', $post)
    <!-- 현재 사용자가 게시글을 수정할 수 있음 -->
@elsecan('create', App\Models\Post::class)
    <!-- 현재 사용자가 새 게시글을 생성할 수 있음 -->
@else
    <!-- 기타 상황 -->
@endcan

@cannot('update', $post)
    <!-- 현재 사용자가 게시글을 수정할 수 없음 -->
@elsecannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 없음 -->
@endcannot
```

이 디렉티브는 `@if`와 `@unless` 문을 간단하게 쓴 문법입니다. 위 `@can`과 `@cannot` 문은 다음과 동등합니다:

```blade
@if (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 수정할 수 있음 -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 수정할 수 없음 -->
@endunless
```

여러 작업 중 하나라도 권한이 있는지 확인하려면 `@canany` 디렉티브를 사용할 수 있습니다:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- 현재 사용자가 게시글을 수정, 조회, 삭제할 수 있음 -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 있음 -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

대부분 권한부여 메서드와 마찬가지로 작업에 모델 인스턴스가 필요 없을 때 클래스 이름을 `@can`과 `@cannot`에 넘길 수 있습니다:

```blade
@can('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 있음 -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 생성할 수 없음 -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 컨텍스트 제공하기

정책을 활용해 작업 권한을 확인할 때, 여러 인자를 배열로 전달할 수 있습니다. 배열의 첫 번째 요소는 정책을 결정하는 데 사용하며, 나머지 요소들은 정책 메서드에 추가 인수로 전달되어 권한 판단에 참고할 수 있습니다. 예를 들어 다음은 추가 매개변수 `$category`를 포함하는 `PostPolicy` 메서드입니다:

```
/**
 * Determine if the given post can be updated by the user.
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

현재 인증 사용자 권한을 확인할 때 위 정책 메서드를 호출하는 예시는 다음과 같습니다:

```
/**
 * Update the given blog post.
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

    // 현재 사용자가 블로그 게시글을 수정할 수 있음...
}
```