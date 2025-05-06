# 미들웨어(Middleware)

- [소개](#introduction)
- [미들웨어 정의하기](#defining-middleware)
- [미들웨어 등록하기](#registering-middleware)
    - [전역 미들웨어](#global-middleware)
    - [라우트에 미들웨어 할당하기](#assigning-middleware-to-routes)
    - [미들웨어 그룹](#middleware-groups)
    - [미들웨어 정렬](#sorting-middleware)
- [미들웨어 파라미터](#middleware-parameters)
- [종료 가능한 미들웨어](#terminable-middleware)

<a name="introduction"></a>
## 소개

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 검사하고 필터링할 수 있는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 사용자가 인증되었는지 확인하는 미들웨어가 포함되어 있습니다. 만약 사용자가 인증되지 않은 경우, 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리디렉션합니다. 그러나 사용자가 인증된 경우에는, 미들웨어가 요청을 애플리케이션 내부로 더 깊이 전달하게 됩니다.

추가적인 미들웨어를 작성하여 인증 외의 다양한 작업을 수행할 수 있습니다. 예를 들어, 모든 들어오는 요청을 기록하는 로깅 미들웨어를 만들 수 있습니다. Laravel 프레임워크에는 인증, CSRF 보호 등 여러 미들웨어가 기본적으로 포함되어 있습니다. 모든 미들웨어는 `app/Http/Middleware` 디렉토리에 위치합니다.

<a name="defining-middleware"></a>
## 미들웨어 정의하기

새로운 미들웨어를 생성하려면 `make:middleware` Artisan 명령어를 사용하세요:

```shell
php artisan make:middleware EnsureTokenIsValid
```

이 명령어는 `app/Http/Middleware` 디렉토리에 새로운 `EnsureTokenIsValid` 클래스를 생성합니다. 이 미들웨어에서는 입력받은 `token` 값이 지정된 값과 일치할 때만 해당 라우트에 접근을 허용합니다. 그렇지 않은 경우에는 사용자를 `home` URI로 리디렉션합니다.

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class EnsureTokenIsValid
    {
        /**
         * 들어오는 요청을 처리합니다.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @return mixed
         */
        public function handle($request, Closure $next)
        {
            if ($request->input('token') !== 'my-secret-token') {
                return redirect('home');
            }

            return $next($request);
        }
    }

보시다시피, 주어진 `token`이 우리의 비밀 키와 일치하지 않으면 미들웨어는 클라이언트에게 HTTP 리디렉션을 반환합니다. 그렇지 않은 경우 요청은 애플리케이션 내 더 깊은 단계로 전달됩니다. 요청을 계속 전달하려면 `$next` 콜백에 `$request`를 전달해야 합니다.

미들웨어는 애플리케이션에 도달하기 전에 HTTP 요청이 반드시 통과해야 하는 일련의 "레이어"로 생각하는 것이 좋습니다. 각 레이어는 요청을 검사할 수 있고, 필요하다면 전체적으로 거부할 수도 있습니다.

> **참고**  
> 모든 미들웨어는 [서비스 컨테이너](/docs/{{version}}/container)에 의해 해석되므로, 미들웨어의 생성자에서 필요한 의존성을 타입힌트로 선언할 수 있습니다.

<a name="middleware-and-responses"></a>
#### 미들웨어와 응답

물론, 미들웨어는 요청이 애플리케이션 내부로 넘어가기 **전**이나 **후**에 작업을 수행할 수 있습니다. 예를 들어, 다음 미들웨어는 요청이 애플리케이션에 의해 처리되기 **전**에 작업을 수행합니다.

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class BeforeMiddleware
    {
        public function handle($request, Closure $next)
        {
            // 작업 수행

            return $next($request);
        }
    }

반면, 다음 예시는 요청이 애플리케이션에 의해 처리된 **후**에 작업을 수행합니다.

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class AfterMiddleware
    {
        public function handle($request, Closure $next)
        {
            $response = $next($request);

            // 작업 수행

            return $response;
        }
    }

<a name="registering-middleware"></a>
## 미들웨어 등록하기

<a name="global-middleware"></a>
### 전역 미들웨어

모든 HTTP 요청마다 미들웨어가 실행되도록 하려면, `app/Http/Kernel.php` 클래스의 `$middleware` 속성에 해당 미들웨어 클래스를 추가하세요.

<a name="assigning-middleware-to-routes"></a>
### 라우트에 미들웨어 할당하기

특정 라우트에만 미들웨어를 할당하고 싶다면, 먼저 `app/Http/Kernel.php` 파일의 `$routeMiddleware` 속성에 미들웨어를 키와 함께 등록해야 합니다. 기본적으로 이 속성에는 Laravel에 기본 포함된 미들웨어가 등록되어 있습니다. 여기에 원하는 미들웨어를 추가하고 원하는 키로 할당할 수 있습니다:

    // App\Http\Kernel 클래스 내부...

    protected $routeMiddleware = [
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

미들웨어를 HTTP 커널에 정의한 후에는, `middleware` 메서드를 사용하여 라우트에 할당할 수 있습니다:

    Route::get('/profile', function () {
        //
    })->middleware('auth');

배열로 여러 미들웨어를 할당할 수도 있습니다:

    Route::get('/', function () {
        //
    })->middleware(['first', 'second']);

미들웨어 할당 시 전체 클래스명을 직접 지정할 수도 있습니다:

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::get('/profile', function () {
        //
    })->middleware(EnsureTokenIsValid::class);

<a name="excluding-middleware"></a>
#### 미들웨어 제외

여러 라우트가 그룹으로 묶여있는 경우, 특정 라우트에서만 일부 미들웨어 적용을 제외할 수 있습니다. 이를 위해 `withoutMiddleware` 메서드를 사용할 수 있습니다:

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::middleware([EnsureTokenIsValid::class])->group(function () {
        Route::get('/', function () {
            //
        });

        Route::get('/profile', function () {
            //
        })->withoutMiddleware([EnsureTokenIsValid::class]);
    });

특정 미들웨어 집합을 [라우트 그룹](/docs/{{version}}/routing#route-groups) 전체에서 제외할 수도 있습니다:

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
        Route::get('/profile', function () {
            //
        });
    });

`withoutMiddleware` 메서드는 라우트 미들웨어만 제거할 수 있으며, [전역 미들웨어](#global-middleware)에는 적용되지 않습니다.

<a name="middleware-groups"></a>
### 미들웨어 그룹

여러 미들웨어를 하나의 키로 묶어 라우트에 쉽게 할당하고 싶을 때가 있습니다. 이를 위해 HTTP 커널의 `$middlewareGroups` 속성에 그룹을 정의할 수 있습니다.

Laravel은 웹 및 API 라우트에 자주 사용되는 미들웨어가 포함된 `web`, `api` 미들웨어 그룹을 미리 정의해놓았습니다. 이 미들웨어 그룹은 애플리케이션의 `App\Providers\RouteServiceProvider` 서비스 프로바이더에 의해 각각의 `web`, `api` 라우트 파일에 자동으로 적용됨을 기억하세요:

    /**
     * 애플리케이션의 라우트 미들웨어 그룹
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
            'throttle:api',
            \Illuminate\Routing\Middleware\SubstituteBindings::class,
        ],
    ];

미들웨어 그룹도 개별 미들웨어와 동일한 문법으로 라우트 및 컨트롤러 액션에 할당할 수 있습니다. 여러 미들웨어를 한 번에 할당하고 싶을 때 미들웨어 그룹 사용을 권장합니다:

    Route::get('/', function () {
        //
    })->middleware('web');

    Route::middleware(['web'])->group(function () {
        //
    });

> **참고**  
> 기본적으로 `web` 및 `api` 미들웨어 그룹은 `App\Providers\RouteServiceProvider`에 의해 각각 `routes/web.php` 와 `routes/api.php` 파일에 자동 적용됩니다.

<a name="sorting-middleware"></a>
### 미들웨어 정렬

드물게, 미들웨어의 실행 순서를 특정한 방식으로 강제해야 하지만, 실제 라우트 할당시 그 순서를 완벽하게 제어할 수 없는 경우가 있습니다. 이럴 때는 `app/Http/Kernel.php` 파일의 `$middlewarePriority` 속성을 사용하여 미들웨어 우선순위를 지정할 수 있습니다. 이 속성은 기본적으로 존재하지 않을 수 있으므로, 없을 경우 아래 정의를 복사해서 추가하세요:

    /**
     * 우선순위가 지정된 미들웨어 리스트
     *
     * 이 리스트는 글로벌 미들웨어가 아닌 미들웨어의 순서를 강제합니다.
     *
     * @var string[]
     */
    protected $middlewarePriority = [
        \Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests::class,
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
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

미들웨어는 추가 파라미터도 받을 수 있습니다. 예를 들어, 인증된 사용자가 특정 "역할(role)"을 가졌는지 확인해야 한다면, 역할명을 추가 인자로 받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

추가 미들웨어 파라미터는 `$next` 인자 뒤에 파라미터로 전달됩니다.

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class EnsureUserHasRole
    {
        /**
         * 들어오는 요청을 처리합니다.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @param  string  $role
         * @return mixed
         */
        public function handle($request, Closure $next, $role)
        {
            if (! $request->user()->hasRole($role)) {
                // 리디렉션 처리 ...
            }

            return $next($request);
        }

    }

미들웨어 파라미터는 미들웨어 이름과 파라미터를 `:`로 구분하여 라우트에 지정합니다. 여러 개의 파라미터가 필요하다면 쉼표로 구분합니다.

    Route::put('/post/{id}', function ($id) {
        //
    })->middleware('role:editor');

<a name="terminable-middleware"></a>
## 종료 가능한 미들웨어(Terminable Middleware)

때로는 미들웨어가 브라우저로 HTTP 응답이 전송된 후에도 추가적인 작업을 수행해야 할 수도 있습니다. 미들웨어에 `terminate` 메서드를 정의하고 웹 서버가 FastCGI를 사용하고 있다면, 응답이 전송된 뒤 자동으로 `terminate` 메서드가 호출됩니다.

    <?php

    namespace Illuminate\Session\Middleware;

    use Closure;

    class TerminatingMiddleware
    {
        /**
         * 들어오는 요청을 처리합니다.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @return mixed
         */
        public function handle($request, Closure $next)
        {
            return $next($request);
        }

        /**
         * 브라우저로 응답이 전송된 후 작업을 처리합니다.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Illuminate\Http\Response  $response
         * @return void
         */
        public function terminate($request, $response)
        {
            // ...
        }
    }

`terminate` 메서드는 요청과 응답을 모두 받아야 합니다. 종료 가능한 미들웨어를 정의한 후에는 반드시 라우트 또는 전역 미들웨어 목록(`app/Http/Kernel.php` 파일)에 등록해야 합니다.

미들웨어의 `terminate` 메서드를 호출할 때, Laravel은 [서비스 컨테이너](/docs/{{version}}/container)로부터 해당 미들웨어의 새로운 인스턴스를 해석합니다. 만약 `handle`과 `terminate` 메서드 호출 시 동일한 미들웨어 인스턴스를 사용하고 싶다면, 컨테이너의 `singleton` 메서드를 사용해 미들웨어를 등록해야 합니다. 이는 보통 `AppServiceProvider`의 `register` 메서드에서 처리합니다:

    use App\Http\Middleware\TerminatingMiddleware;

    /**
     * 애플리케이션 서비스를 등록합니다.
     *
     * @return void
     */
    public function register()
    {
        $this->app->singleton(TerminatingMiddleware::class);
    }
