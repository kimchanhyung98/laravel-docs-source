# 인가(Authorization)

- [소개](#introduction)
- [게이트(Gates)](#gates)
    - [게이트 작성하기](#writing-gates)
    - [행동 인가](#authorizing-actions-via-gates)
    - [게이트 응답](#gate-responses)
    - [게이트 체크 가로채기](#intercepting-gate-checks)
    - [인라인 인가](#inline-authorization)
- [정책 만들기](#creating-policies)
    - [정책 생성하기](#generating-policies)
    - [정책 등록하기](#registering-policies)
- [정책 작성하기](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델이 없는 메서드](#methods-without-models)
    - [게스트 사용자](#guest-users)
    - [정책 필터](#policy-filters)
- [정책을 이용한 행동 인가](#authorizing-actions-using-policies)
    - [유저 모델을 통한 인가](#via-the-user-model)
    - [컨트롤러 헬퍼를 통한 인가](#via-controller-helpers)
    - [미들웨어를 통한 인가](#via-middleware)
    - [블레이드 템플릿을 통한 인가](#via-blade-templates)
    - [추가 컨텍스트 제공하기](#supplying-additional-context)

<a name="introduction"></a>
## 소개

Laravel은 내장 [인증](docs/{{version}}/authentication) 서비스 외에도 주어진 리소스에 대한 사용자 행동을 인가(authorization)하는 간단한 방법을 제공합니다. 예를 들어, 사용자가 인증되었더라도, 어플리케이션이 관리하는 특정 Eloquent 모델이나 데이터베이스 레코드를 수정 또는 삭제하도록 인가되지 않았을 수 있습니다. Laravel의 인가 기능은 이러한 인가 검사를 관리하는 쉽고 조직적인 방법을 제공합니다.

Laravel은사용자 행동을 인가하는 두 가지 주요 방법을 제공합니다: [게이트](#gates)와 [정책](#creating-policies)입니다. 게이트와 정책은 각각 라우트와 컨트롤러처럼 생각할 수 있습니다. 게이트는 단순하고 클로저 기반 방식으로, 정책은 컨트롤러처럼 특정 모델이나 리소스를 중심으로 인가 로직을 그룹화합니다. 이 문서에서는 먼저 게이트를 살펴보고, 그 다음에 정책을 설명합니다.

애플리케이션을 만들 때 게이트와 정책을 반드시 하나만 선택해서 사용할 필요는 없습니다. 대부분의 애플리케이션은 게이트와 정책을 혼합해서 사용하게 될 것이고, 이는 전혀 문제없습니다! 게이트는 주로 특정 모델이나 리소스와 관계없는 행동(예: 어드민 대시보드 보기)에 적합합니다. 반면, 정책은 특정 모델이나 리소스에 대해 행동을 인가할 때 사용해야 합니다.

<a name="gates"></a>
## 게이트(Gates)

<a name="writing-gates"></a>
### 게이트 작성하기

> [!WARNING]  
> 게이트는 Laravel의 인가 기능 기본을 익히기에 좋은 방법이지만, 견고한 Laravel 애플리케이션을 구축할 때는 인가 규칙을 조직적으로 관리할 수 있는 [정책](#creating-policies) 사용을 고려해야 합니다.

게이트는 사용자가 특정 행동을 수행할 인가가 되었는지 여부를 판단하는 클로저입니다. 보통 게이트는 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드 안에서 `Gate` 파사드를 사용하여 정의합니다. 게이트는 항상 첫 번째 인자로 사용자 인스턴스를 받고, 필요시 관련된 Eloquent 모델 등 추가 인자도 받을 수 있습니다.

다음 예제는 사용자가 주어진 `App\Models\Post` 모델을 수정할 수 있는지 확인하는 'update-post' 게이트를 정의합니다. 이 게이트는 사용자의 id와 게시글의 작성자 user_id를 비교하여 인가 여부를 판단합니다:

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

컨트롤러와 유사하게, 게이트도 클래스 콜백 배열 형식으로 정의할 수 있습니다:

    use App\Policies\PostPolicy;
    use Illuminate\Support\Facades\Gate;

    /**
     * Register any authentication / authorization services.
     */
    public function boot(): void
    {
        Gate::define('update-post', [PostPolicy::class, 'update']);
    }

<a name="authorizing-actions-via-gates"></a>
### 행동 인가

게이트를 사용하여 행동을 인가하려면 `Gate` 파사드의 `allows` 또는 `denies` 메서드를 이용하면 됩니다. 이때 현재 인증된 사용자를 직접 전달할 필요는 없습니다. Laravel이 자동으로 해당 사용자를 게이트 클로저에 전달합니다. 일반적으로 인가가 필요한 행동을 수행하기 전에 컨트롤러 안에서 게이트 인가 메서드를 호출하는 것이 일반적입니다:

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

            // 게시글 수정...

            return redirect('/posts');
        }
    }

현재 인증된 사용자가 아닌 특정 사용자의 인가 여부를 판단하고 싶다면, `Gate` 파사드의 `forUser` 메서드를 사용하면 됩니다:

    if (Gate::forUser($user)->allows('update-post', $post)) {
        // 해당 사용자가 게시글을 수정할 수 있습니다...
    }

    if (Gate::forUser($user)->denies('update-post', $post)) {
        // 해당 사용자는 게시글을 수정할 수 없습니다...
    }

여러 행동을 한 번에 인가 확인하려면 `any` 또는 `none` 메서드를 사용할 수 있습니다:

    if (Gate::any(['update-post', 'delete-post'], $post)) {
        // 사용자가 게시글을 수정하거나 삭제할 수 있습니다...
    }

    if (Gate::none(['update-post', 'delete-post'], $post)) {
        // 사용자가 게시글을 수정하거나 삭제할 수 없습니다...
    }

<a name="authorizing-or-throwing-exceptions"></a>
#### 예외를 던지며 인가

만약 인가를 시도하고 사용자가 해당 행동을 허용받지 않으면 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시키고 싶다면, `Gate` 파사드의 `authorize` 메서드를 사용할 수 있습니다. `AuthorizationException` 인스턴스는 Laravel의 예외 핸들러에 의해 자동으로 403 HTTP 응답으로 변환됩니다:

    Gate::authorize('update-post', $post);

    // 인가된 행동...

<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 제공

인가 메서드 (`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`)와 [Blade 지시문](#via-blade-templates)(`@can`, `@cannot`, `@canany`)은 두 번째 인자로 배열을 받을 수 있습니다. 이 배열의 원소들은 게이트 클로저의 파라미터로 전달되며, 인가 결정 시 추가 컨텍스트로 활용할 수 있습니다:

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
        // 사용자가 게시글을 생성할 수 있습니다...
    }

<a name="gate-responses"></a>
### 게이트 응답

지금까지는 단순하게 참/거짓만 반환하는 게이트만 살펴보았습니다. 하지만 경우에 따라 오류 메시지 등의 더 자세한 응답을 반환하고 싶을 수 있습니다. 이런 경우 `Illuminate\Auth\Access\Response`를 게이트에서 반환할 수 있습니다:

    use App\Models\User;
    use Illuminate\Auth\Access\Response;
    use Illuminate\Support\Facades\Gate;

    Gate::define('edit-settings', function (User $user) {
        return $user->isAdmin
                    ? Response::allow()
                    : Response::deny('관리자여야 합니다.');
    });

게이트에서 인가 응답을 반환해도, `Gate::allows` 메서드는 여전히 불리언 값만 반환합니다. 하지만 `Gate::inspect` 메서드를 사용하면 게이트가 반환한 전체 인가 응답을 확인할 수 있습니다:

    $response = Gate::inspect('edit-settings');

    if ($response->allowed()) {
        // 인가됨...
    } else {
        echo $response->message();
    }

`Gate::authorize` 메서드를 사용할 경우(인가되지 않으면 `AuthorizationException`이 발생), 인가 응답에서 제공한 오류 메시지가 HTTP 응답에 그대로 포함됩니다:

    Gate::authorize('edit-settings');

    // 인가됨...

<a name="customising-gate-response-status"></a>
#### HTTP 상태 코드 커스터마이징

게이트를 통해 행동이 거부되면 기본적으로 `403` HTTP 상태 코드가 반환됩니다. 그러나 경우에 따라 다른 상태 코드를 반환하고 싶은 경우가 있을 수 있습니다. 이런 경우 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용해 실패한 인가 검사의 HTTP 코드도 커스터마이징할 수 있습니다:

    use App\Models\User;
    use Illuminate\Auth\Access\Response;
    use Illuminate\Support\Facades\Gate;

    Gate::define('edit-settings', function (User $user) {
        return $user->isAdmin
                    ? Response::allow()
                    : Response::denyWithStatus(404);
    });

웹 애플리케이션에서 리소스를 404 상태로 숨기는 패턴이 흔하기 때문에, 이를 위한 `denyAsNotFound` 메서드도 제공됩니다:

    use App\Models\User;
    use Illuminate\Auth\Access\Response;
    use Illuminate\Support\Facades\Gate;

    Gate::define('edit-settings', function (User $user) {
        return $user->isAdmin
                    ? Response::allow()
                    : Response::denyAsNotFound();
    });

<a name="intercepting-gate-checks"></a>
### 게이트 체크 가로채기

특정 사용자에게 모든 권한을 부여하고 싶을 때가 있을 수 있습니다. 이럴 때는 모든 인가 검사 전에 실행되는 클로저를 `before` 메서드로 정의할 수 있습니다:

    use App\Models\User;
    use Illuminate\Support\Facades\Gate;

    Gate::before(function (User $user, string $ability) {
        if ($user->isAdministrator()) {
            return true;
        }
    });

`before` 클로저가 null이 아닌 값을 반환하면, 그 값이 인가 검사 결과로 사용됩니다.

모든 인가 검사 후에 클로저를 실행하려면 `after` 메서드를 사용할 수 있습니다:

    use App\Models\User;

    Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
        if ($user->isAdministrator()) {
            return true;
        }
    });

`before`와 마찬가지로 `after` 클로저가 null이 아닌 값을 반환하면, 그 값이 인가 검사 결과가 됩니다.

<a name="inline-authorization"></a>
### 인라인 인가

때때로, 해당 행동에 대한 별도의 게이트를 만들 필요 없이, 현재 인증된 사용자가 주어진 행동을 할 수 있는지 인라인으로 판단하고 싶을 때가 있습니다. Laravel에서는 이와 같은 "인라인" 인가 검사를 `Gate::allowIf` 및 `Gate::denyIf` 메서드를 통해 할 수 있습니다. 인라인 인가는 ["before" 또는 "after" 인가 후크](#intercepting-gate-checks)를 실행하지 않습니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

행동이 인가되지 않았거나 인증된 사용자가 없으면, Laravel은 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 던집니다. 이 예외는 Laravel의 예외 핸들러에 의해 자동으로 403 HTTP 응답으로 변환됩니다.

<a name="creating-policies"></a>
## 정책 만들기

<a name="generating-policies"></a>
### 정책 생성하기

정책은 특정 모델이나 리소스를 중심으로 인가 로직을 조직화하는 클래스입니다. 예를 들어, 블로그 애플리케이션이라면, `App\Models\Post` 모델과 해당 모델에 대한 인가를 담당하는 `App\Policies\PostPolicy` 정책이 있을 수 있습니다.

`make:policy` Artisan 명령어를 사용해 정책을 생성할 수 있습니다. 생성된 정책은 `app/Policies` 디렉터리에 위치하게 됩니다. 해당 디렉터리가 없다면, Laravel이 자동으로 생성해줍니다:

```shell
php artisan make:policy PostPolicy
```

`make:policy` 명령은 비어있는 정책 클래스를 생성합니다. 리소스 보기, 생성, 수정, 삭제에 관련된 예시 정책 메서드가 포함된 클래스를 생성하려면, 명령 실행 시 `--model` 옵션을 추가하면 됩니다:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록하기

정책 클래스가 만들어졌다면, 이를 등록해야 합니다. 정책 등록은 Laravel에게 특정 모델 타입에 대한 인가 시 어떤 정책을 사용할지 알려주는 역할을 합니다.

새로운 Laravel 애플리케이션에 포함된 `App\Providers\AuthServiceProvider`에는 Eloquent 모델을 해당 정책과 매핑하는 `policies` 속성이 있습니다. 정책을 등록하면, Laravel은 지정된 Eloquent 모델에 대한 행동 인가 시 어떤 정책을 사용할지 알게 됩니다:

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

<a name="policy-auto-discovery"></a>
#### 정책 자동 발견

모델 정책을 수동으로 등록하지 않고도, Laravel은 표준 명명 규칙을 따를 경우 정책을 자동으로 발견할 수 있습니다. 특히, 정책은 모델보다 같거나 상위 디렉터리의 `Policies` 디렉터리에 있어야 합니다. 예를 들어, 모델은 `app/Models`에, 정책은 `app/Policies`에 있을 때, Laravel은 `app/Models/Policies`를 먼저 확인한 후 `app/Policies`를 확인합니다. 그리고 정책 클래스 이름은 모델 이름과 동일하고 'Policy' 접미사가 붙어 있어야 합니다. 즉, `User` 모델은 `UserPolicy` 정책 클래스와 매칭됩니다.

정책 발견 로직을 직접 제어하고 싶다면, `Gate::guessPolicyNamesUsing` 메서드를 사용해 커스텀 정책 발견 콜백을 등록할 수 있습니다. 보통 이 메서드는 `AuthServiceProvider`의 `boot` 메서드에서 호출합니다:

    use Illuminate\Support\Facades\Gate;

    Gate::guessPolicyNamesUsing(function (string $modelClass) {
        // 주어진 모델에 대한 정책 클래스 이름을 반환...
    });

> [!WARNING]  
> `AuthServiceProvider`에서 명시적으로 매핑된 정책은 자동 발견 정책보다 우선 적용됩니다.

<a name="writing-policies"></a>
## 정책 작성하기

<a name="policy-methods"></a>
### 정책 메서드

정책 클래스를 등록한 후에는, 인가할 각 행동별로 메서드를 추가할 수 있습니다. 예를 들어, 사용자가 주어진 `App\Models\Post` 인스턴스를 업데이트할 수 있는지 결정하는 `update` 메서드를 `PostPolicy`에 정의할 수 있습니다.

`update` 메서드는 `User`와 `Post` 인스턴스를 인자로 받아, 주어진 사용자가 해당 `Post`를 수정할 수 있는지를 나타내는 true/false를 반환해야 합니다. 즉, 다음과 같이 사용자의 id가 게시글의 user_id와 일치하는지 확인하게 됩니다:

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

필요에 따라 정책에 추가적인 메서드를 계속 정의할 수 있습니다. 예를 들어, `view`나 `delete` 등의 메서드를 정의하여 다양한 게시글 관련 행동을 인가할 수 있습니다. 단, 메서드 이름은 원하는 대로 정할 수 있습니다.

`--model` 옵션을 사용해서 Artisan으로 정책을 생성했다면 `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 등 다양한 행동에 대한 메서드가 이미 포함되어 있습니다.

> [!NOTE]  
> 모든 정책은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 정책 생성자에서 필요로 하는 의존성을 타입힌트하면 자동으로 주입받을 수 있습니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지는 참/거짓만 반환하는 정책 메서드를 살펴봤습니다. 경우에 따라, 오류 메시지 등 더 자세한 응답을 반환하고 싶을 수도 있습니다. 그런 경우, 정책 메서드에서 `Illuminate\Auth\Access\Response` 인스턴스를 반환하면 됩니다:

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

정책에서 인가 응답을 반환해도, `Gate::allows` 메서드는 여전히 불리언 값만 반환합니다. 전체 인가 응답을 확인하려면 `Gate::inspect`를 사용할 수 있습니다:

    use Illuminate\Support\Facades\Gate;

    $response = Gate::inspect('update', $post);

    if ($response->allowed()) {
        // 인가됨...
    } else {
        echo $response->message();
    }

`Gate::authorize` 메서드를 사용할 경우, 인가되지 않으면 인가 응답의 오류 메시지가 HTTP 응답에 포함됩니다:

    Gate::authorize('update', $post);

    // 인가됨...

<a name="customising-policy-response-status"></a>
#### HTTP 상태 코드 커스터마이징

정책 메서드에서 행동이 거부되면 기본적으로 `403` HTTP 응답이 반환됩니다. 다른 HTTP 응답 코드가 필요한 경우, `Illuminate\Auth\Access\Response`의 `denyWithStatus` 정적 생성자를 활용할 수 있습니다:

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

404 응답을 통해 리소스를 숨기는 경우가 잦으므로, 별도의 `denyAsNotFound` 메서드도 제공합니다:

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

<a name="methods-without-models"></a>
### 모델이 없는 메서드

일부 정책 메서드는 현재 인증된 사용자 인스턴스만을 인자로 받습니다. 이런 상황은 주로 `create` 행동을 인가할 때 자주 사용됩니다. 예를 들어, 사용자가 게시글을 작성할 자격이 있는지 확인하고 싶다면 사용자 인스턴스만 받으면 됩니다:

    /**
     * Determine if the given user can create posts.
     */
    public function create(User $user): bool
    {
        return $user->role == 'writer';
    }

<a name="guest-users"></a>
### 게스트 사용자

기본적으로 모든 게이트 및 정책은 요청이 인증된 사용자에 의해 시작되지 않은 경우 자동으로 `false`를 반환합니다. 하지만 사용자 인자 정의에 "옵셔널" 타입힌트 또는 `null` 기본값을 선언하면, 이러한 인가 검사가 게이트 및 정책으로 통과되도록 할 수 있습니다:

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

<a name="policy-filters"></a>
### 정책 필터

특정 사용자의 경우, 주어진 정책의 모든 행동을 인가하고 싶을 때가 있습니다. 이럴 때는 정책에 `before` 메서드를 정의하면 됩니다. 이 메서드는 정책 내 다른 메서드보다 먼저 실행되어, 주요 정책 메서드가 호출되기 전에 행동을 인가할 기회를 제공합니다. 이 기능은 주로 관리자가 모든 행동을 수행할 수 있게 허용할 때 사용됩니다:

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

특정 사용자 유형에 대해 모든 인가를 차단하고 싶다면 `before` 메서드에서 `false`를 반환하면 됩니다. `null`을 반환하면 인가 검사가 정책 메서드로 넘어가게 됩니다.

> [!WARNING]  
> 정책 클래스에 해당 권한이름과 일치하는 메서드가 없으면 `before` 메서드는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 이용한 행동 인가

<a name="via-the-user-model"></a>
### 유저 모델을 통한 인가

Laravel의 기본 `App\Models\User` 모델은 `can` 및 `cannot`이라는 두 가지 편리한 인가 메서드를 포함하고 있습니다. 이 메서드들은 인가하려는 행동의 이름과, 관련 모델을 인자로 받습니다. 예를 들어, 사용자가 특정 게시글을 수정할 수 있는지 여부는 컨트롤러 메서드에서 다음과 같이 판단할 수 있습니다:

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

            // 게시글 수정...

            return redirect('/posts');
        }
    }

[정책이 등록](#registering-policies)되어 있다면, `can` 메서드는 자동으로 적절한 정책을 호출하여 불리언 값을 반환합니다. 정책이 없다면, 이름이 일치하는 클로저 기반 게이트를 호출합니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 행동

일부 행동은 `create`와 같이 인스턴스를 필요로 하지 않는 정책 메서드에 해당할 수 있습니다. 이런 경우 `can` 메서드에 클래스 이름을 전달하면 됩니다. 클래스 이름을 바탕으로 어떤 정책을 적용할지 결정합니다:

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

<a name="via-controller-helpers"></a>
### 컨트롤러 헬퍼를 통한 인가

`App\Models\User`가 제공하는 메서드 외에도, `App\Http\Controllers\Controller`를 상속한 어떤 컨트롤러라도 사용할 수 있는 `authorize` 메서드가 제공됩니다.

`can` 메서드와 마찬가지로, 인가하려는 행동과 관련 모델을 인자로 받으며, 인가되지 않으면 `Illuminate\Auth\Access\AuthorizationException` 예외를 던집니다. 이 예외는 Laravel 예외 핸들러에 의해 403 상태의 HTTP 응답으로 자동 변환됩니다:

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

            // 현재 사용자가 블로그 게시글을 수정할 수 있습니다...

            return redirect('/posts');
        }
    }

<a name="controller-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 행동

앞서 언급했듯, `create`같이 모델 인스턴스가 필요 없는 정책 메서드도 있습니다. 이런 경우, 클래스 이름을 `authorize` 메서드에 전달하면 됩니다. 클래스 이름으로 어떤 정책을 사용할지 판단합니다:

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

        // 현재 사용자가 블로그 게시글을 생성할 수 있습니다...

        return redirect('/posts');
    }

<a name="authorizing-resource-controllers"></a>
#### 리소스 컨트롤러의 인가

[리소스 컨트롤러](/docs/{{version}}/controllers#resource-controllers)를 사용할 경우, 컨트롤러 생성자에서 `authorizeResource` 메서드를 활용할 수 있습니다. 이 메서드는 리소스 컨트롤러의 각 메서드에 적합한 `can` 미들웨어를 자동으로 연결해줍니다.

`authorizeResource`는 첫 번째 인자로 모델 클래스 이름, 두 번째 인자로 라우트/요청 파라미터 이름을 받습니다. [암시적 모델 바인딩](/docs/{{version}}/routing#implicit-binding)을 사용하면 해당 파라미터로 모델 인스턴스가 전달됩니다.

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Models\Post;

    class PostController extends Controller
    {
        /**
         * 컨트롤러 인스턴스 생성자.
         */
        public function __construct()
        {
            $this->authorizeResource(Post::class, 'post');
        }
    }

아래 표는 각 컨트롤러 메서드가 연결되는 정책 메서드를 보여줍니다. 요청이 전달되면, 해당 정책 메서드를 먼저 실행한 후 컨트롤러 메서드가 실행됩니다:

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
> `--model` 옵션을 넣어 `make:policy` 명령으로 원하는 모델에 대한 정책 클래스를 빠르게 생성할 수 있습니다: `php artisan make:policy PostPolicy --model=Post`.

<a name="via-middleware"></a>
### 미들웨어를 통한 인가

Laravel은 요청이 라우트나 컨트롤러에 도달하기 전에 행동 인가를 미리 수행하는 미들웨어를 제공합니다. 기본적으로 `Illuminate\Auth\Middleware\Authorize` 미들웨어는 `App\Http\Kernel` 클래스의 `can` 키에 할당되어 있습니다. 게시글 수정 권한 확인 예시는 다음과 같습니다:

    use App\Models\Post;

    Route::put('/post/{post}', function (Post $post) {
        // 현재 사용자가 게시글을 수정할 수 있습니다...
    })->middleware('can:update,post');

여기서는 `can` 미들웨어에 두 인자를 전달합니다. 첫 번째는 인가하려는 행동명, 두 번째는 정책 메서드에 전달할 라우트 파라미터입니다. [암시적 모델 바인딩](/docs/{{version}}/routing#implicit-binding)을 적용했기 때문에 `App\Models\Post` 인스턴스가 자동으로 전달됩니다. 인가에 실패하면 403 상태의 HTTP 응답이 반환됩니다.

좀 더 편하게 `can` 미들웨어는 `can` 메서드로 라우트에 직접 연결할 수도 있습니다:

    use App\Models\Post;

    Route::put('/post/{post}', function (Post $post) {
        // 현재 사용자가 게시글을 수정할 수 있습니다...
    })->can('update', 'post');

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 행동

`create` 등 모델 인스턴스가 필요하지 않은 행동은 미들웨어에 클래스 이름을 넘겨주면 됩니다. 클래스 이름으로 어떤 정책을 확인할지 결정합니다:

    Route::post('/post', function () {
        // 현재 사용자가 게시글을 생성할 수 있습니다...
    })->middleware('can:create,App\Models\Post');

문자열 미들웨어 정의에 클래스 전체 이름을 넣는 것이 번거로울 수 있으므로, `can` 메서드를 사용해 라우트에 연결하는 방법도 선호됩니다:

    use App\Models\Post;

    Route::post('/post', function () {
        // 현재 사용자가 게시글을 생성할 수 있습니다...
    })->can('create', Post::class);

<a name="via-blade-templates"></a>
### 블레이드 템플릿을 통한 인가

Blade 템플릿을 작성할 때, 사용자가 어떤 행동을 인가받았을 경우에만 페이지의 일부를 보여주고 싶을 때가 있습니다. 예를 들어, 사용자가 게시글을 수정할 수 있는 경우에만 수정 폼을 보여주고 싶을 때, `@can`과 `@cannot` 지시문을 사용할 수 있습니다:

```blade
@can('update', $post)
    <!-- 현재 사용자가 게시글을 수정할 수 있습니다... -->
@elsecan('create', App\Models\Post::class)
    <!-- 현재 사용자가 새 게시글을 만들 수 있습니다... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- 현재 사용자가 게시글을 수정할 수 없습니다... -->
@elsecannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 새 게시글을 만들 수 없습니다... -->
@endcannot
```

이 지시문은 `@if`, `@unless` 조건문을 더 간단하게 작성할 수 있도록 도와줍니다. 위의 `@can`, `@cannot` 문은 다음과 같습니다:

```blade
@if (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 수정할 수 있습니다... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 게시글을 수정할 수 없습니다... -->
@endunless
```

사용자가 여러 행동 중 하나라도 인가받았는지 확인하려면 `@canany` 지시문을 사용합니다:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- 현재 사용자가 게시글을 수정, 보기, 혹은 삭제할 수 있습니다... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- 현재 사용자가 게시글을 만들 수 있습니다... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 행동

대부분의 다른 인가 방법과 마찬가지로, `@can`과 `@cannot` 지시문에 클래스 이름을 전달해도 됩니다(행동이 모델 인스턴스를 요구하지 않을 때):

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

정책을 사용해 행동을 인가할 때, 두 번째 인자로 배열을 전달할 수 있습니다. 배열의 첫 번째 원소는 어떤 정책을 호출할지 결정하는 데 사용되고, 나머지 원소는 정책 메서드에 파라미터로 전달되어 추가 컨텍스트로 사용될 수 있습니다. 다음은 `$category` 파라미터를 추가로 받는 `PostPolicy` 예제입니다:

    /**
     * Determine if the given post can be updated by the user.
     */
    public function update(User $user, Post $post, int $category): bool
    {
        return $user->id === $post->user_id &&
               $user->canUpdateCategory($category);
    }

사용자가 주어진 게시글을 업데이트할 수 있는지 판단할 때, 이 정책 메서드는 다음과 같이 호출할 수 있습니다:

    /**
     * Update the given blog post.
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        $this->authorize('update', [$post, $request->category]);

        // 현재 사용자가 블로그 게시글을 수정할 수 있습니다...

        return redirect('/posts');
    }
