# 미들웨어(Middleware)

- [소개](#introduction)
- [미들웨어 정의하기](#defining-middleware)
- [미들웨어 등록하기](#registering-middleware)
    - [글로벌 미들웨어](#global-middleware)
    - [라우트에 미들웨어 지정하기](#assigning-middleware-to-routes)
    - [미들웨어 그룹](#middleware-groups)
    - [미들웨어 정렬](#sorting-middleware)
- [미들웨어 파라미터](#middleware-parameters)
- [종료 가능한 미들웨어](#terminable-middleware)

<a name="introduction"></a>
## 소개

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 검사하고 필터링할 수 있는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 사용자가 인증되었는지 확인하는 미들웨어가 포함되어 있습니다. 사용자가 인증되지 않았다면, 이 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리디렉션합니다. 반면에 사용자가 인증된 경우에는 요청을 애플리케이션 내부로 더 진행시킵니다.

인증 외에도 다양한 작업을 수행하는 추가 미들웨어를 작성할 수 있습니다. 예를 들어, 로깅 미들웨어는 들어오는 모든 요청을 기록할 수 있습니다. Laravel 프레임워크에는 인증 및 CSRF 보호를 위한 미들웨어 등 여러 미들웨어가 포함되어 있습니다. 이 모든 미들웨어는 `app/Http/Middleware` 디렉터리에 위치합니다.

<a name="defining-middleware"></a>
## 미들웨어 정의하기

새로운 미들웨어를 생성하려면 `make:middleware` Artisan 명령어를 사용하세요:

```shell
php artisan make:middleware EnsureTokenIsValid
```

이 명령어는 `app/Http/Middleware` 디렉터리에 새로운 `EnsureTokenIsValid` 클래스를 생성합니다. 이 미들웨어에서는 입력받은 `token` 값이 지정된 값과 일치할 때만 라우트에 접근을 허용합니다. 그렇지 않을 경우 사용자를 `home` URI로 리디렉션합니다.

    <?php

    namespace App\Http\Middleware;

    use Closure;
    use Illuminate\Http\Request;
    use Symfony\Component\HttpFoundation\Response;

    class EnsureTokenIsValid
    {
        /**
         * Handle an incoming request.
         *
         * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
         */
        public function handle(Request $request, Closure $next): Response
        {
            if ($request->input('token') !== 'my-secret-token') {
                return redirect('home');
            }

            return $next($request);
        }
    }

위 예시에서, 전달된 `token`이 우리의 시크릿 토큰과 일치하지 않으면, 미들웨어는 클라이언트에게 HTTP 리디렉션을 반환합니다. 그렇지 않으면 요청이 애플리케이션 내부로 더 진행됩니다. 요청을 더 깊게 전달하려면(즉, 미들웨어를 "통과"시키려면), `$next` 콜백에 `$request`를 전달해야 합니다.

미들웨어는 HTTP 요청이 애플리케이션에 도달하기 전에 통과해야 하는 일련의 "레이어"로 생각하는 것이 가장 좋습니다. 각 레이어에서는 요청을 검사하고, 필요하다면 완전히 거절할 수도 있습니다.

> [!NOTE]  
> 모든 미들웨어는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 생성자에서 필요한 의존성을 타입힌트할 수 있습니다.

<a name="middleware-and-responses"></a>
#### 미들웨어와 응답

물론, 미들웨어는 요청을 애플리케이션 내부로 전달하기 **전** 또는 **후**에 작업을 수행할 수 있습니다. 예를 들어, 아래 미들웨어는 요청이 애플리케이션에 의해 처리되기 **전**에 어떤 작업을 수행합니다:

    <?php

    namespace App\Http\Middleware;

    use Closure;
    use Illuminate\Http\Request;
    use Symfony\Component\HttpFoundation\Response;

    class BeforeMiddleware
    {
        public function handle(Request $request, Closure $next): Response
        {
            // 작업 수행

            return $next($request);
        }
    }

반면, 이 미들웨어는 요청이 애플리케이션에 의해 처리된 **후**에 작업을 수행합니다:

    <?php

    namespace App\Http\Middleware;

    use Closure;
    use Illuminate\Http\Request;
    use Symfony\Component\HttpFoundation\Response;

    class AfterMiddleware
    {
        public function handle(Request $request, Closure $next): Response
        {
            $response = $next($request);

            // 작업 수행

            return $response;
        }
    }

<a name="registering-middleware"></a>
## 미들웨어 등록하기

<a name="global-middleware"></a>
### 글로벌 미들웨어

모든 HTTP 요청에서 항상 미들웨어가 실행되기를 원한다면, 해당 미들웨어 클래스를 `app/Http/Kernel.php`의 `$middleware` 속성에 추가하세요.

<a name="assigning-middleware-to-routes"></a>
### 라우트에 미들웨어 지정하기

특정 라우트에 미들웨어를 지정하고 싶다면, 라우트 정의 시 `middleware` 메서드를 호출하면 됩니다:

    use App\Http\Middleware\Authenticate;

    Route::get('/profile', function () {
        // ...
    })->middleware(Authenticate::class);

여러 개의 미들웨어를 배열로 전달하여 한 라우트에 지정할 수도 있습니다:

    Route::get('/', function () {
        // ...
    })->middleware([First::class, Second::class]);

편의를 위해, 애플리케이션의 `app/Http/Kernel.php` 파일에서 미들웨어에 별칭(alias)을 지정할 수 있습니다. 기본적으로 이 클래스의 `$middlewareAliases` 속성에는 Laravel에 포함된 미들웨어의 엔트리가 있습니다. 이 목록에 자신의 미들웨어를 추가하고 원하는 별칭을 지정하면 됩니다:

    // App\Http\Kernel 클래스 내부...

    protected $middlewareAliases = [
        'auth' => \App\Http\Middleware\Authenticate::class,
        'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
        'bindings' => \Illuminate\Routing\Middleware\SubstituteBindings::class,
        'cache.headers' => \Illuminate\Http\Middleware\SetCacheHeaders::class,
        'can' => \Illuminate\Auth\Middleware\Authorize::class,
        'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
        'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
        'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
        'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
    ];

미들웨어 별칭을 HTTP 커널에 정의했다면, 라우트에서 이 별칭을 사용할 수 있습니다:

    Route::get('/profile', function () {
        // ...
    })->middleware('auth');

<a name="excluding-middleware"></a>
#### 미들웨어 제외하기

라우트 그룹에 미들웨어를 지정할 때, 때로는 그룹 내 특정 라우트만 미들웨어 적용에서 제외하고 싶을 수 있습니다. 이 경우 `withoutMiddleware` 메서드를 사용하세요:

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::middleware([EnsureTokenIsValid::class])->group(function () {
        Route::get('/', function () {
            // ...
        });

        Route::get('/profile', function () {
            // ...
        })->withoutMiddleware([EnsureTokenIsValid::class]);
    });

특정 미들웨어 집합을 [그룹](/docs/{{version}}/routing#route-groups) 전체에서 제외할 수도 있습니다:

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
        Route::get('/profile', function () {
            // ...
        });
    });

`withoutMiddleware` 메서드는 라우트 미들웨어만 제거할 수 있으며, [글로벌 미들웨어](#global-middleware)에는 적용되지 않습니다.

<a name="middleware-groups"></a>
### 미들웨어 그룹

여러 미들웨어를 하나의 키에 그룹화하여 라우트에 할당하기 쉽게 만들고 싶을 때가 있습니다. 이 경우 HTTP 커널의 `$middlewareGroups` 속성을 사용하면 됩니다.

Laravel에는 `web`과 `api`라는 미리 정의된 미들웨어 그룹이 있으며, 각각 웹 및 API 라우트에 자주 사용하는 미들웨어가 포함되어 있습니다. 이 미들웨어 그룹들은 애플리케이션의 `App\Providers\RouteServiceProvider` 서비스 프로바이더에 의해, 해당 `web` 및 `api` 라우트 파일에 자동으로 적용됩니다:

    /**
     * The application's route middleware groups.
     *
     * @var array
     */
    protected $middlewareGroups = [
        'web' => [
            \App\Http\Middleware\EncryptCookies::class,
            \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
            \Illuminate\Session\Middleware\StartSession::class,
            \Illuminate\View\Middleware\ShareErrorsFromSession::class,
            \App\Http\Middleware\VerifyCsrfToken::class,
            \Illuminate\Routing\Middleware\SubstituteBindings::class,
        ],

        'api' => [
            \Illuminate\Routing\Middleware\ThrottleRequests::class.':api',
            \Illuminate\Routing\Middleware\SubstituteBindings::class,
        ],
    ];

미들웨어 그룹은 개별 미들웨어와 동일한 문법으로 라우트나 컨트롤러 액션에 지정할 수 있습니다. 미들웨어 그룹을 활용하면 여러 미들웨어를 한 번에 라우트에 적용할 수 있어 훨씬 편리합니다:

    Route::get('/', function () {
        // ...
    })->middleware('web');

    Route::middleware(['web'])->group(function () {
        // ...
    });

> [!NOTE]  
> 기본적으로 `web` 및 `api` 미들웨어 그룹은 `App\Providers\RouteServiceProvider`가 각 라우트 파일(`routes/web.php`, `routes/api.php`)에 자동으로 적용합니다.

<a name="sorting-middleware"></a>
### 미들웨어 정렬

드물게 라우트에 미들웨어를 지정할 때 실행 순서를 직접 제어하기 어려울 수도 있습니다. 이런 상황에서는 `app/Http/Kernel.php` 파일의 `$middlewarePriority` 속성을 통해 미들웨어 실행 순위를 강제할 수 있습니다. 이 속성이 기본적으로 존재하지 않는 경우, 아래 정의를 복사해서 추가하세요:

    /**
     * The priority-sorted list of middleware.
     *
     * This forces non-global middleware to always be in the given order.
     *
     * @var string[]
     */
    protected $middlewarePriority = [
        \Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests::class,
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Contracts\Auth\Middleware\AuthenticatesRequests::class,
        \Illuminate\Routing\Middleware\ThrottleRequests::class,
        \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
        \Illuminate\Contracts\Session\Middleware\AuthenticatesSessions::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        \Illuminate\Auth\Middleware\Authorize::class,
    ];

<a name="middleware-parameters"></a>
## 미들웨어 파라미터

미들웨어는 추가적인 파라미터도 받을 수 있습니다. 예를 들어, 인증된 사용자가 특정 "역할"을 가지고 있는지 확인해야 할 경우, 역할 이름을 추가 인자로 받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

추가 미들웨어 파라미터는 `$next` 인자 뒤에 전달됩니다:

    <?php

    namespace App\Http\Middleware;

    use Closure;
    use Illuminate\Http\Request;
    use Symfony\Component\HttpFoundation\Response;

    class EnsureUserHasRole
    {
        /**
         * Handle an incoming request.
         *
         * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
         */
        public function handle(Request $request, Closure $next, string $role): Response
        {
            if (! $request->user()->hasRole($role)) {
                // 리디렉션 등...
            }

            return $next($request);
        }

    }

미들웨어 파라미터는 라우트 정의 시 미들웨어 이름과 파라미터를 `:`로 구분하여 지정할 수 있습니다:

    Route::put('/post/{id}', function (string $id) {
        // ...
    })->middleware('role:editor');

여러 개의 파라미터가 있다면 쉼표로 구분하면 됩니다:

    Route::put('/post/{id}', function (string $id) {
        // ...
    })->middleware('role:editor,publisher');

<a name="terminable-middleware"></a>
## 종료 가능한 미들웨어

종종 미들웨어가 HTTP 응답이 브라우저에 전송된 *이후*에도 추가 작업을 해야 할 수 있습니다. 미들웨어에 `terminate` 메서드를 정의하고, 웹 서버가 FastCGI를 사용 중이라면, 응답이 브라우저로 전송된 후 해당 메서드가 자동으로 호출됩니다:

    <?php

    namespace Illuminate\Session\Middleware;

    use Closure;
    use Illuminate\Http\Request;
    use Symfony\Component\HttpFoundation\Response;

    class TerminatingMiddleware
    {
        /**
         * Handle an incoming request.
         *
         * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
         */
        public function handle(Request $request, Closure $next): Response
        {
            return $next($request);
        }

        /**
         * Handle tasks after the response has been sent to the browser.
         */
        public function terminate(Request $request, Response $response): void
        {
            // ...
        }
    }

`terminate` 메서드는 요청과 응답 모두를 인자로 받아야 합니다. 종료 가능한 미들웨어를 정의했다면, 해당 미들웨어를 `app/Http/Kernel.php` 파일의 라우트 또는 글로벌 미들웨어 목록에 추가하세요.

미들웨어의 `terminate` 메서드가 호출될 때, Laravel은 [서비스 컨테이너](/docs/{{version}}/container)로부터 미들웨어의 새로운 인스턴스를 해석합니다. 만약 `handle`과 `terminate` 메서드에서 동일한 미들웨어 인스턴스를 사용하고 싶다면, 컨테이너의 `singleton` 메서드를 사용해 미들웨어를 등록하세요. 일반적으로 이는 `AppServiceProvider`의 `register` 메서드 내에서 수행합니다:

    use App\Http\Middleware\TerminatingMiddleware;

    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->singleton(TerminatingMiddleware::class);
    }
