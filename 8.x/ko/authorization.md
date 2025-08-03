# 권한 부여 (Authorization)

- [소개](#introduction)
- [게이트 (Gates)](#gates)
    - [게이트 작성하기](#writing-gates)
    - [게이트를 통한 작업 권한 부여](#authorizing-actions-via-gates)
    - [게이트 응답](#gate-responses)
    - [게이트 검사 가로채기](#intercepting-gate-checks)
    - [인라인 권한 부여](#inline-authorization)
- [정책 만들기 (Creating Policies)](#creating-policies)
    - [정책 생성](#generating-policies)
    - [정책 등록](#registering-policies)
- [정책 작성하기](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델이 없는 메서드](#methods-without-models)
    - [게스트 사용자](#guest-users)
    - [정책 필터](#policy-filters)
- [정책을 이용한 작업 권한 부여](#authorizing-actions-using-policies)
    - [유저 모델을 통해](#via-the-user-model)
    - [컨트롤러 헬퍼를 통해](#via-controller-helpers)
    - [미들웨어를 통해](#via-middleware)
    - [Blade 템플릿을 통해](#via-blade-templates)
    - [추가 컨텍스트 전달하기](#supplying-additional-context)

<a name="introduction"></a>
## 소개

Laravel은 기본 제공하는 [인증(authentication)](/docs/{{version}}/authentication) 서비스 외에도, 주어진 리소스에 대해 사용자의 작업 권한을 간단히 확인할 수 있는 방법을 제공합니다. 예를 들어, 사용자가 인증되었더라도, 애플리케이션에서 관리하는 특정 Eloquent 모델이나 데이터베이스 레코드를 업데이트하거나 삭제할 권한이 없을 수 있습니다. Laravel의 권한 부여 기능은 이러한 권한 검사를 쉽고 체계적으로 관리할 수 있는 방식을 제공합니다.

Laravel은 작업 권한 부여를 위한 두 가지 주요 방식을 제공합니다: [게이트(gates)](#gates)와 [정책(policies)](#creating-policies). 게이트와 정책은 각각 라우트(routes)와 컨트롤러(controllers)에 비유할 수 있습니다. 게이트는 간단한 클로저 기반 권한 부여 방식을 제공하며, 정책은 컨트롤러처럼 특정 모델이나 리소스에 관련된 권한 부여 로직을 그룹화합니다. 이 문서에서는 먼저 게이트를 살펴보고, 그 다음 정책을 다룰 것입니다.

애플리케이션을 만들 때 게이트만 사용하거나 정책만 사용해야 하는 것은 아닙니다. 대부분 애플리케이션은 게이트와 정책을 적절히 혼합하여 사용하며, 이는 전혀 문제되지 않습니다! 게이트는 주로 관리자 대시보드 조회 같이 특정 모델이나 리소스와 관련 없는 작업에 적합합니다. 반면, 정책은 특정 모델이나 리소스에 대해 작업 권한을 부여하고자 할 때 사용해야 합니다.

<a name="gates"></a>
## 게이트 (Gates)

<a name="writing-gates"></a>
### 게이트 작성하기

> [!NOTE]
> 게이트는 Laravel 권한 부여 기능의 기초를 배우기 위한 좋은 방법입니다. 그러나 견고한 Laravel 애플리케이션을 작성할 때는 권한 부여 규칙을 체계적으로 관리하기 위해 [정책](#creating-policies)을 사용하는 것이 좋습니다.

게이트는 사용자가 특정 작업을 수행할 수 있는 권한이 있는지 결정하는 단순한 클로저입니다. 보통 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드 내에서 `Gate` 파사드를 이용해 정의합니다. 게이트는 항상 첫 번째 인수로 사용자 인스턴스를 받고, 필요에 따라 관련된 Eloquent 모델과 같은 추가 인수를 받을 수도 있습니다.

다음 예시는 사용자가 주어진 `App\Models\Post` 모델을 업데이트할 수 있는지 판단하는 게이트를 정의합니다. 사용자의 `id`가 게시글을 생성한 사용자의 `user_id`와 일치하는지 비교하는 방식입니다:

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

컨트롤러와 마찬가지로, 게이트는 클래스 콜백 배열로도 정의할 수 있습니다:

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

게이트를 이용해 작업 권한을 부여하려면 `Gate` 파사드가 제공하는 `allows` 또는 `denies` 메서드를 사용하세요. 현재 인증된 사용자를 명시적으로 전달할 필요는 없습니다. Laravel이 자동으로 사용자 인스턴스를 게이트 클로저에 전달합니다. 일반적으로 애플리케이션의 컨트롤러 내에서 권한 검사 후 작업을 수행하기 전에 게이트 권한 부여 메서드를 호출합니다:

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

        // 게시물 업데이트...
    }
}
```

현재 인증된 사용자 이외의 사용자가 권한이 있는지 확인하려면 `Gate` 파사드의 `forUser` 메서드를 사용하세요:

```
if (Gate::forUser($user)->allows('update-post', $post)) {
    // 해당 사용자는 게시물을 업데이트할 수 있습니다.
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // 해당 사용자는 게시물을 업데이트할 수 없습니다.
}
```

한 번에 여러 작업의 권한을 확인하려면 `any` 또는 `none` 메서드를 사용할 수 있습니다:

```
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // 사용자가 게시물을 업데이트하거나 삭제할 수 있습니다.
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // 사용자가 게시물을 업데이트하거나 삭제할 수 없습니다.
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 권한 부여 시도 또는 예외 던지기

작업을 권한 부여하고, 허용되지 않은 경우 `Illuminate\Auth\Access\AuthorizationException` 예외를 자동으로 던지려면 `Gate` 파사드의 `authorize` 메서드를 사용할 수 있습니다. `AuthorizationException` 인스턴스는 Laravel의 예외 핸들러에 의해 403 HTTP 응답으로 자동 변환됩니다:

```
Gate::authorize('update-post', $post);

// 작업이 승인됨...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 전달하기

권한 부여 메서드(`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`)와 권한 부여 [Blade 디렉티브](#via-blade-templates) (`@can`, `@cannot`, `@canany`)는 두 번째 인수로 배열을 받을 수 있습니다. 이 배열의 요소들은 게이트 클로저에 전달되어 권한 결정 시 추가 컨텍스트로 활용할 수 있습니다:

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
    // 사용자가 게시물을 생성할 수 있습니다.
}
```

<a name="gate-responses"></a>
### 게이트 응답

지금까지는 단순히 boolean 값만 반환하는 게이트를 보았습니다. 하지만 경우에 따라 오류 메시지를 포함한 자세한 응답을 반환하고 싶을 때가 있습니다. 이때는 `Illuminate\Auth\Access\Response` 인스턴스를 게이트에서 반환할 수 있습니다:

```
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
                ? Response::allow()
                : Response::deny('관리자여야 합니다.');
});
```

권한 부여 응답을 반환해도 `Gate::allows` 메서드는 여전히 단순 boolean 값을 반환합니다. 하지만 `Gate::inspect` 메서드를 사용하면 게이트가 반환한 전체 권한 부여 응답을 얻을 수 있습니다:

```
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // 작업이 승인됨...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드는 권한이 없으면 `AuthorizationException`을 던집니다. 이때 권한 부여 응답에 포함된 에러 메시지가 HTTP 응답으로 전달됩니다:

```
Gate::authorize('edit-settings');

// 작업이 승인됨...
```

<a name="intercepting-gate-checks"></a>
### 게이트 검사 가로채기

특정 사용자에게 모든 권한을 허용하고 싶을 때, `before` 메서드를 사용해 모든 권한 검사 전에 실행할 클로저를 정의할 수 있습니다:

```
use Illuminate\Support\Facades\Gate;

Gate::before(function ($user, $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저가 null이 아닌 결과를 반환하면, 그 결과가 권한 검사 결과로 간주됩니다.

또한, `after` 메서드를 사용해 모든 권한 검사 후 실행할 클로저를 정의할 수도 있습니다:

```
Gate::after(function ($user, $ability, $result, $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after` 클로저 또한 null이 아닌 값을 반환하면 그 결과가 최종 권한 검사 결과로 간주됩니다.

<a name="inline-authorization"></a>
### 인라인 권한 부여

때때로 특정 작업에 대응하는 별도의 게이트를 작성하지 않고, 현재 인증된 사용자가 해당 작업을 수행할 권한이 있는지 즉석에서 확인하고 싶을 수 있습니다. Laravel은 `Gate::allowIf`와 `Gate::denyIf` 메서드를 사용한 이러한 "인라인" 권한 검사를 지원합니다:

```php
use Illuminate\Support\Facades\Auth;

Gate::allowIf(fn ($user) => $user->isAdministrator());

Gate::denyIf(fn ($user) => $user->banned());
```

작업이 권한 없거나 인증된 사용자가 없는 경우, Laravel은 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 던집니다. 이 예외도 403 HTTP 응답으로 자동 변환됩니다.

<a name="creating-policies"></a>
## 정책 만들기 (Creating Policies)

<a name="generating-policies"></a>
### 정책 생성

정책은 특정 모델이나 리소스를 중심으로 권한 부여 로직을 조직화하는 클래스입니다. 예를 들어, 블로그 애플리케이션에서는 `App\Models\Post` 모델과, 게시글 생성 및 수정과 같은 사용자 작업 권한을 부여하는 `App\Policies\PostPolicy`가 있을 수 있습니다.

`make:policy` Artisan 명령어를 사용하여 정책 클래스를 생성할 수 있습니다. 생성된 정책은 `app/Policies` 디렉토리에 위치합니다. 이 디렉토리가 없으면 Laravel이 자동으로 생성해 줍니다:

```
php artisan make:policy PostPolicy
```

`make:policy` 명령어는 빈 정책 클래스를 생성합니다. 만약 조회, 생성, 수정, 삭제와 관련된 예제 정책 메서드를 포함하는 클래스를 생성하려면 다음과 같이 `--model` 옵션을 제공하세요:

```
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록

정책 클래스를 생성한 후에는 등록이 필요합니다. 정책 등록은 Laravel에 특정 모델 유형에 대한 권한 부여 시 사용할 정책을 알리는 과정입니다.

초기 상태의 `App\Providers\AuthServiceProvider` 클래스에는 `policies` 속성이 있어, Eloquent 모델과 해당 정책을 매핑합니다. 정책을 등록하면 해당 Eloquent 모델 작업 권한 부여 시 어떤 정책을 사용하는지 Laravel에 알려주는 역할을 합니다:

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
#### 정책 자동 탐지

모델과 정책이 Laravel 표준 명명 규칙을 따르면 정책을 수동 등록하지 않아도 Laravel이 자동으로 정책을 탐지할 수 있습니다. 구체적으로, 정책은 모델을 포함하는 디렉토리 아래나 같은 레벨에 있는 `Policies` 디렉토리에 위치해야 합니다. 예를 들어 모델은 `app/Models`에, 정책은 `app/Policies`에 위치하면, Laravel은 `app/Models/Policies`와 `app/Policies`에서 정책을 찾습니다. 그리고 정책 클래스 이름은 모델 이름과 일치하며 `Policy` 접미어가 붙어야 합니다. 예를 들어 `User` 모델은 `UserPolicy` 정책 클래스에 대응합니다.

직접 정책 자동 탐지 로직을 정의하려면 `Gate::guessPolicyNamesUsing` 메서드를 통해 커스텀 콜백을 등록할 수 있습니다. 보통 이 메서드는 애플리케이션 `AuthServiceProvider`의 `boot` 메서드 내에서 호출합니다:

```
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function ($modelClass) {
    // 주어진 모델에 대한 정책 클래스 이름을 반환...
});
```

> [!NOTE]
> `AuthServiceProvider`에 명시적으로 등록된 정책이 자동 탐지된 정책보다 우선합니다.

<a name="writing-policies"></a>
## 정책 작성하기

<a name="policy-methods"></a>
### 정책 메서드

정책 클래스를 등록했다면, 권한 부여할 각 작업에 대한 메서드를 추가할 수 있습니다. 예를 들어, `PostPolicy`에 `update` 메서드를 정의해 `App\Models\User`가 특정 `App\Models\Post` 인스턴스를 업데이트할 수 있는지 판단할 수 있습니다.

`update` 메서드는 `User` 인스턴스와 `Post` 인스턴스를 인수로 받고, 사용자가 해당 게시글을 업데이트할 권한이 있으면 `true`, 없으면 `false`를 반환해야 합니다. 이 예에서는 사용자의 `id`와 게시글의 `user_id`가 같은지 검증합니다:

```
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 주어진 게시글을 사용자가 업데이트할 수 있는지 판단합니다.
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

필요에 따라 다양한 작업에 대해 추가 메서드를 정의할 수 있습니다. 예를 들어 `view`나 `delete` 메서드를 정의하여 다양한 `Post` 관련 권한을 부여할 수 있으며, 메서드 이름은 자유롭게 지을 수 있습니다.

`make:policy` Artisan 명령을 `--model` 옵션과 함께 실행하면 `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 메서드를 미리 포함한 정책 클래스가 생성됩니다.

> [!TIP]
> 모든 정책은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 필요에 따라 정책 클래스의 생성자에 의존성을 타입힌트하여 자동으로 주입 받을 수 있습니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지는 단순 boolean 값을 반환하는 정책 메서드를 살펴보았습니다. 하지만 경우에 따라 오류 메시지를 포함한 상세한 응답을 반환하고 싶을 수 있습니다. 이때 `Illuminate\Auth\Access\Response` 인스턴스를 반환할 수 있습니다:

```
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 주어진 게시글을 사용자가 업데이트할 수 있는지 판단합니다.
 *
 * @param  \App\Models\User  $user
 * @param  \App\Models\Post  $post
 * @return \Illuminate\Auth\Access\Response
 */
public function update(User $user, Post $post)
{
    return $user->id === $post->user_id
                ? Response::allow()
                : Response::deny('이 게시글의 소유자가 아닙니다.');
}
```

정책에서 권한 부여 응답을 반환해도 `Gate::allows` 메서드는 여전히 boolean 값을 반환합니다. 하지만 `Gate::inspect` 메서드를 사용하면 정책이 반환한 전체 권한 부여 응답을 얻을 수 있습니다:

```
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // 작업이 승인됨...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드를 사용하면 권한 없을 때 `AuthorizationException`이 던져지며, 이때 제공된 오류 메시지가 HTTP 응답에 전달됩니다:

```
Gate::authorize('update', $post);

// 작업이 승인됨...
```

<a name="methods-without-models"></a>
### 모델이 없는 메서드

일부 정책 메서드는 현재 인증된 사용자 인스턴스만 받습니다. 이런 경우는 일반적으로 `create` 작업 권한 부여 시 발생합니다. 예를 들어 블로그에서 사용자가 게시물을 생성할 권한이 있는지 판단하려면, 정책 메서드가 사용자만 인수로 받으면 됩니다:

```
/**
 * 주어진 사용자가 게시물을 생성할 수 있는지 판단합니다.
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

기본적으로, 모든 게이트와 정책은 인증되지 않은 요청 사용자에 대해서는 자동으로 `false`를 반환합니다. 하지만 권한 검사를 게이트와 정책으로 전달하고 싶다면, 사용자 인수에 "옵셔널" 타입힌트 또는 `null` 기본값을 지정하세요:

```
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 주어진 게시글을 사용자가 업데이트할 수 있는지 판단합니다.
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

특정 사용자에 대해 정책 내 모든 작업을 허용하고 싶다면, 정책에 `before` 메서드를 정의하세요. 이 메서드는 정책 내 다른 메서드 실행 전에 호출되며, 작업을 즉시 허용하거나 거부할 기회를 제공합니다. 주로 애플리케이션 관리자 권한을 처리할 때 유용합니다:

```
use App\Models\User;

/**
 * 사전 권한 검사 실행.
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

특정 유형의 사용자에 대해 모든 권한 검사를 거부하고 싶으면 `before` 메서드에서 `false`를 반환하세요. `null`을 반환하면 정책 메서드에서 권한 검사를 계속 진행합니다.

> [!NOTE]
> 정책 클래스에 검사할 능력과 일치하는 메서드가 없으면 `before` 메서드는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 이용한 작업 권한 부여

<a name="via-the-user-model"></a>
### 유저 모델을 통해

Laravel 애플리케이션에 기본 포함된 `App\Models\User` 모델에는 권한 부여에 유용한 `can`과 `cannot` 메서드가 있습니다. 이들은 권한 부여를 원하는 작업 이름과 관련 모델을 인수로 받습니다. 예를 들어, 사용자가 특정 `App\Models\Post` 모델을 수정할 권한이 있는지 확인하는 코드를 보겠습니다. 보통 컨트롤러 메서드 내에서 사용합니다:

```
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

        // 게시물 업데이트...
    }
}
```

[정책이 등록되어 있다면](#registering-policies), `can` 메서드는 자동으로 해당 정책을 호출하며 boolean 결과를 반환합니다. 등록된 정책이 없으면, `can` 메서드는 클로저 기반 게이트에서 해당 작업 이름을 찾아 호출합니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

`create`처럼 모델 인스턴스가 필요 없는 작업도 있습니다. 이때는 `can` 메서드에 클래스 이름을 전달할 수 있는데, 이 클래스 이름으로 어떤 정책을 사용할지 결정합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 게시글 생성합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        if ($request->user()->cannot('create', Post::class)) {
            abort(403);
        }

        // 게시물 생성...
    }
}
```

<a name="via-controller-helpers"></a>
### 컨트롤러 헬퍼를 통해

`App\Http\Controllers\Controller`를 상속받는 모든 컨트롤러에는 편리한 `authorize` 메서드가 제공됩니다.

`can` 메서드와 유사하게, 권한 부여할 작업 이름과 관련 모델을 인수로 받으며, 권한이 없으면 `AuthorizationException` 예외를 던집니다. 이 예외는 Laravel 예외 핸들러가 403 HTTP 응답 코드로 자동 변환합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 블로그 게시글을 업데이트합니다.
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

        // 현재 사용자는 게시글을 업데이트할 수 있습니다...
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

앞서 설명한 대로, `create` 같은 정책 메서드는 모델 인스턴스가 필요 없습니다. 이 경우 `authorize` 메서드에 클래스 이름을 전달하세요:

```
use App\Models\Post;
use Illuminate\Http\Request;

/**
 * 새 블로그 게시글 생성.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\Response
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request)
{
    $this->authorize('create', Post::class);

    // 현재 사용자는 게시물을 생성할 수 있습니다...
}
```

<a name="authorizing-resource-controllers"></a>
#### 리소스 컨트롤러 권한 부여

[리소스 컨트롤러](/docs/{{version}}/controllers#resource-controllers)를 사용할 경우, 컨트롤러 생성자에서 `authorizeResource` 메서드를 호출할 수 있습니다. 이 메서드는 리소스 컨트롤러의 메서드에 적절한 `can` 미들웨어를 자동으로 연결합니다.

`authorizeResource`는 첫 번째 인수로 모델 클래스 이름, 두 번째 인수로 라우트 혹은 요청 매개변수명(모델 ID 포함)를 받습니다. [리소스 컨트롤러](/docs/{{version}}/controllers#resource-controllers)는 `--model` 옵션으로 생성해 해당 타입힌트가 포함된 메서드를 갖도록 해야 합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 컨트롤러 인스턴스 생성.
     *
     * @return void
     */
    public function __construct()
    {
        $this->authorizeResource(Post::class, 'post');
    }
}
```

다음 컨트롤러 메서드와 정책 메서드가 자동으로 연결됩니다. 해당 컨트롤러 메서드에 들어오는 요청은 정책 메서드를 통과한 후 실행됩니다:

| 컨트롤러 메서드 | 정책 메서드 |
| --- | --- |
| index | viewAny |
| show | view |
| create | create |
| store | create |
| edit | update |
| update | update |
| destroy | delete |

> [!TIP]
> `make:policy` 명령어에 `--model` 옵션을 주어 빠르게 특정 모델용 정책 클래스를 생성할 수 있습니다: `php artisan make:policy PostPolicy --model=Post`

<a name="via-middleware"></a>
### 미들웨어를 통해

Laravel은 요청이 라우트나 컨트롤러에 도달하기 전에 권한을 검사하는 미들웨어를 포함합니다. 기본적으로 `Illuminate\Auth\Middleware\Authorize` 미들웨어는 `App\Http\Kernel` 클래스에서 `can` 키에 등록되어 있습니다. 다음 예제는 `can` 미들웨어로 사용자가 게시물을 업데이트할 권한이 있는지 검사합니다:

```
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자는 게시물을 업데이트할 수 있습니다...
})->middleware('can:update,post');
```

이 예에서 `can` 미들웨어에는 두 개의 인수가 전달됩니다. 첫 번째는 권한 부여할 작업 이름, 두 번째는 정책 메서드에 전달할 라우트 매개변수 이름입니다. 여기서는 [암묵적 모델 바인딩](/docs/{{version}}/routing#implicit-binding)을 사용하여 `App\Models\Post` 모델이 자동으로 정책 메서드에 전달됩니다. 만약 사용자가 권한이 없다면, 미들웨어가 403 HTTP 응답을 반환합니다.

편의를 위해 `can` 미들웨어를 라우트에서 `can` 메서드로 붙일 수도 있습니다:

```
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자는 게시물을 업데이트할 수 있습니다...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

다시 말하지만, `create` 같은 일부 정책 메서드는 모델 인스턴스가 필요하지 않습니다. 이때는 미들웨어에 클래스 이름을 전달하세요. 이 클래스 이름은 권한 부여할 정책을 결정하는 데 사용됩니다:

```
Route::post('/post', function () {
    // 현재 사용자는 게시물을 생성할 수 있습니다...
})->middleware('can:create,App\Models\Post');
```

전체 네임스페이스를 문자열로 입력하는 것이 번거롭다면, `can` 메서드를 활용해 다음처럼 작성할 수도 있습니다:

```
use App\Models\Post;

Route::post('/post', function () {
    // 현재 사용자는 게시물을 생성할 수 있습니다...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿을 통해

Blade 템플릿 작성 시, 특정 작업 권한이 있는 사용자만 페이지 일부를 보도록 하고 싶을 수 있습니다. 예를 들어, 게시글 업데이트 폼은 사용자가 해당 게시글을 수정할 수 있을 때만 보여주고 싶다면, `@can`과 `@cannot` 디렉티브를 사용할 수 있습니다:

```html
@can('update', $post)
    <!-- 현재 사용자는 게시글을 수정할 수 있습니다... -->
@elsecan('create', App\Models\Post::class)
    <!-- 현재 사용자는 새 게시글을 생성할 수 있습니다... -->
@else
    <!-- 기타 경우... -->
@endcan

@cannot('update', $post)
    <!-- 현재 사용자는 게시글을 수정할 수 없습니다... -->
@elsecannot('create', App\Models\Post::class)
    <!-- 현재 사용자는 새 게시글을 생성할 수 없습니다... -->
@endcannot
```

이 디렉티브는 `@if`와 `@unless`의 편리한 단축문입니다. 위 `@can`과 `@cannot` 예시는 아래 문과 동일합니다:

```html
@if (Auth::user()->can('update', $post))
    <!-- 현재 사용자는 게시글을 수정할 수 있습니다... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- 현재 사용자는 게시글을 수정할 수 없습니다... -->
@endunless
```

여러 작업 중 하나라도 권한이 있는지 확인하려면 `@canany` 디렉티브를 사용하세요:

```html
@canany(['update', 'view', 'delete'], $post)
    <!-- 현재 사용자는 게시글을 수정, 조회 또는 삭제할 수 있습니다... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- 현재 사용자는 게시글을 생성할 수 있습니다... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

다른 권한 부여 메서드와 마찬가지로, 작업에 모델 인스턴스가 필요 없다면 `@can`과 `@cannot` 디렉티브에 클래스 이름을 전달할 수 있습니다:

```html
@can('create', App\Models\Post::class)
    <!-- 현재 사용자는 게시글을 생성할 수 있습니다... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- 현재 사용자는 게시글을 생성할 수 없습니다... -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 컨텍스트 전달하기

정책을 통한 권한 부여 시, 여러 권한 부여 함수 및 헬퍼의 두 번째 인수로 배열을 넘길 수 있습니다. 배열의 첫 번째 요소는 어떤 정책 메서드를 호출할지 결정하는 데 쓰이고, 나머지 요소들은 정책 메서드에 전달되어 권한 부여 판단 시 추가 컨텍스트로 활용됩니다. 예를 들어, 다음 `PostPolicy` 메서드는 추가로 `$category` 매개변수를 받습니다:

```
/**
 * 주어진 게시글을 사용자가 업데이트할 수 있는지 판단합니다.
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

인증된 사용자가 해당 게시글을 수정할 수 있는지 확인할 때 다음과 같이 정책 메서드를 호출할 수 있습니다:

```
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

    // 현재 사용자는 해당 블로그 게시글을 업데이트할 수 있습니다...
}
```