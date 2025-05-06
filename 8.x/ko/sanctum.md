# Laravel Sanctum

- [소개](#introduction)
    - [작동 방식](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 오버라이드](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 권한(Abilities)](#token-abilities)
    - [라우트 보호하기](#protecting-routes)
    - [토큰 폐기(취소)](#revoking-tokens)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증하기](#spa-authenticating)
    - [라우트 보호하기](#protecting-spa-routes)
    - [프라이빗 브로드캐스트 채널 권한 부여](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호하기](#protecting-mobile-api-routes)
    - [토큰 폐기](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션, 그리고 단순한 토큰 기반 API를 위한 경량 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자는 자신의 계정에 대해 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰들은 수행할 수 있는 액션을 지정하는 "abilities/스코프"를 부여받을 수 있습니다.

<a name="how-it-works"></a>
### 작동 방식

Laravel Sanctum은 두 가지 별개의 문제를 해결하기 위해 존재합니다. 라이브러리를 더 깊이 살펴보기 전에 각 문제에 대해 논의해보겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰

첫째, Sanctum은 OAuth의 복잡성 없이 사용자에게 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 GitHub 등에서 제공하는 "개인 액세스 토큰"에서 영감을 받았습니다. 예를 들어, 애플리케이션의 "계정 설정" 화면에서 사용자가 자신의 계정용 API 토큰을 생성할 수 있습니다. 이러한 토큰의 만료 기간은 매우 길 수도 있는데(수년 이상), 사용자가 언제든 직접 폐기(삭제)할 수도 있습니다.

Laravel Sanctum은 단일 데이터베이스 테이블에 사용자 API 토큰을 저장하고, 유효한 토큰이 포함된 `Authorization` 헤더를 통해 들어오는 HTTP 요청을 인증합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증

둘째, Sanctum은 Laravel 기반 API와 통신해야 하는 SPA를 위한 인증 방식을 제공합니다. 이러한 SPA는 Laravel 애플리케이션과 동일한 저장소(레포지토리)에 있을 수도 있고, Vue CLI, Next.js 등 완전히 별도의 저장소에 존재할 수도 있습니다.

이 기능을 위해 Sanctum은 어떠한 토큰도 사용하지 않습니다. 대신, Laravel 자체의 "쿠키 기반 세션 인증 서비스"를 이용합니다. 일반적으로 `web` 인증 가드가 활용되며, 이를 통해 CSRF 보호, 세션 인증, XSS를 통한 인증 정보 유출 방지도 제공됩니다.

Sanctum은 오직 자신의 SPA 프론트엔드에서 유입된 경우에만 쿠키 인증을 시도합니다. 들어오는 HTTP 요청을 검사할 때 먼저 인증 쿠키가 있는지 확인하고, 쿠키가 없다면 `Authorization` 헤더에 유효한 API 토큰이 있는지 확인합니다.

> {tip} Sanctum은 API 토큰 인증, SPA 인증 둘 중 하나만 사용해도 무방합니다. Sanctum을 쓴다고 해서 반드시 두 가지 기능을 모두 사용할 필요는 없습니다.

<a name="installation"></a>
## 설치

> {tip} 최신 Laravel 버전에는 이미 Laravel Sanctum이 포함되어 있습니다. 하지만 프로젝트의 `composer.json`에 `laravel/sanctum`이 없다면 아래 안내를 따라 설치하세요.

Composer 패키지 관리자를 통해 Laravel Sanctum을 설치할 수 있습니다:

    composer require laravel/sanctum

다음으로, `vendor:publish` Artisan 명령어를 사용해 Sanctum 설정 및 마이그레이션 파일을 퍼블리시합니다. `sanctum` 설정 파일은 `config` 디렉터리에 만들어집니다:

    php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"

마지막으로 데이터베이스 마이그레이션을 실행하세요. Sanctum은 API 토큰을 저장할 단일 테이블을 생성합니다:

    php artisan migrate

SPA 인증을 이용할 계획이라면, `app/Http/Kernel.php` 파일의 `api` 미들웨어 그룹에 Sanctum 미들웨어를 추가하세요:

    'api' => [
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

<a name="migration-customization"></a>
#### 마이그레이션 커스터마이즈

Sanctum의 기본 마이그레이션을 사용하지 않을 경우, `App\Providers\AppServiceProvider`의 `register` 메소드에서 `Sanctum::ignoreMigrations`를 호출해야 합니다. 기본 마이그레이션은 `php artisan vendor:publish --tag=sanctum-migrations` 명령어로 추출할 수 있습니다.

<a name="configuration"></a>
## 설정

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

필수는 아니지만, 내부적으로 Sanctum이 사용하는 `PersonalAccessToken` 모델을 자유롭게 확장할 수 있습니다:

    use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

    class PersonalAccessToken extends SanctumPersonalAccessToken
    {
        // ...
    }

이후, Sanctum에서 커스텀 모델을 사용하도록 `usePersonalAccessTokenModel` 메서드로 지정할 수 있습니다. 보통 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

    use App\Models\Sanctum\PersonalAccessToken;
    use Laravel\Sanctum\Sanctum;

    /**
     * 어플리케이션 서비스 부트스트랩
     *
     * @return void
     */
    public function boot()
    {
        Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
    }

<a name="api-token-authentication"></a>
## API 토큰 인증

> {tip} 직접 개발한 1차 애플리케이션(SPA) 인증에는 API 토큰 대신 [Sanctum의 내장 SPA 인증](#spa-authentication)을 사용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급

Sanctum을 이용하면 사용자를 위한 API 토큰(개인 접근 토큰)을 발급해 API 요청 인증에 사용할 수 있습니다. 요청 시 `Authorization` 헤더에 토큰을 `Bearer` 형식으로 전달해야 합니다.

사용자 모델에서 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용하세요:

    use Laravel\Sanctum\HasApiTokens;

    class User extends Authenticatable
    {
        use HasApiTokens, HasFactory, Notifiable;
    }

토큰을 발급하려면 `createToken` 메소드를 사용할 수 있습니다. 이 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환하며, 생성된 토큰은 SHA-256으로 해싱되어 저장되지만, `plainTextToken` 프로퍼티로 평문 값을 조회할 수 있습니다. 생성 직후 사용자가 볼 수 있도록 즉시 반환해야 합니다:

    use Illuminate\Http\Request;

    Route::post('/tokens/create', function (Request $request) {
        $token = $request->user()->createToken($request->token_name);

        return ['token' => $token->plainTextToken];
    });

`HasApiTokens` 트레이트가 제공하는 `tokens` Eloquent 관계를 통해 특정 사용자의 모든 토큰에 접근할 수 있습니다:

    foreach ($user->tokens as $token) {
        //
    }

<a name="token-abilities"></a>
### 토큰 권한(Abilities)

Sanctum을 사용하여 토큰에 "abilities"(권한 또는 OAuth의 "스코프"와 유사)를 부여할 수 있습니다. `createToken` 메소드의 두 번째 인수로 문자열 배열을 전달하여 부여할 수 있습니다:

    return $user->createToken('token-name', ['server:update'])->plainTextToken;

인증된 요청에서 토큰이 특정 ability를 가지고 있는지 `tokenCan` 메소드를 통해 판단할 수 있습니다:

    if ($user->tokenCan('server:update')) {
        //
    }

<a name="token-ability-middleware"></a>
#### 토큰 권한 미들웨어

Sanctum에는 토큰에 특정 권한이 부여되어 있는지 확인할 수 있는 두 가지 미들웨어도 포함되어 있습니다. 먼저, `app/Http/Kernel.php`의 `$routeMiddleware` 프로퍼티에 아래 미들웨어를 추가하세요:

    'abilities' => \Laravel\Sanctum\Http\Middleware\CheckAbilities::class,
    'ability' => \Laravel\Sanctum\Http\Middleware\CheckForAnyAbility::class,

`abilities` 미들웨어는 요청의 토큰이 명시된 모든 권한을 가지고 있는지 확인합니다:

    Route::get('/orders', function () {
        // "check-status"와 "place-orders" 능력을 모두 가진 토큰만 가능
    })->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);

`ability` 미들웨어는 명시된 권한 중 한 가지라도 있으면 통과합니다:

    Route::get('/orders', function () {
        // "check-status" 또는 "place-orders" 권한이 있는 토큰만 가능
    })->middleware(['auth:sanctum', 'ability:check-status,place-orders']);

<a name="first-party-ui-initiated-requests"></a>
#### 1차 UI에서 발생한 요청

편의를 위해, 1차 SPA에서 내장 [SPA 인증](#spa-authentication)으로 인증된 경우, `tokenCan`은 항상 `true`를 반환합니다.

그러나 이것이 사용자가 액션을 반드시 할 수 있다는 뜻은 아닙니다. 보통 [인증 정책](/docs/{{version}}/authorization#creating-policies)에서 해당 토큰에 필요한 권한이 있는지와 더불어 실제 사용자가 작업 가능 대상인지도 확인합니다.

예를 들어 서버 관리 애플리케이션이라면, 토큰에 서버 업데이트 권한이 있는 것뿐만 아니라 서버가 해당 사용자 소유인지도 확인해야 할 수 있습니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

`tokenCan`은 1차 UI 인증 요청에서 항상 `true`를 반환하지만, 이를 통해 언제든 API 토큰이 있다고 간주하고 `tokenCan` 메소드를 정책 내에서 자유롭게 호출할 수 있는 장점이 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호하기

모든 요청이 인증되길 원한다면 `routes/web.php` 또는 `routes/api.php`에서 `sanctum` 인증 가드를 미들웨어로 붙이세요. 이 가드는 유입 요청이 쿠키 기반 인증 또는 유효한 API 토큰을 가진 경우 인증을 통과시킵니다.

`routes/web.php`에서 `sanctum` 가드를 사용하는 이유는 Sanctum이 먼저 세션 인증 쿠키를 확인하고, 없으면 토큰을 검사하기 때문입니다. 또한 인증 유저에서 항상 `tokenCan`을 호출할 수 있게 됩니다:

    use Illuminate\Http\Request;

    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

<a name="revoking-tokens"></a>
### 토큰 폐기(취소)

`Laravel\Sanctum\HasApiTokens` 트레이트의 `tokens` 관계를 이용해 토큰을 데이터베이스에서 삭제("폐기")할 수 있습니다:

    // 모든 토큰 폐기
    $user->tokens()->delete();

    // 현재 요청에 사용된 토큰만 폐기
    $request->user()->currentAccessToken()->delete();

    // 특정 토큰 폐기
    $user->tokens()->where('id', $tokenId)->delete();

<a name="spa-authentication"></a>
## SPA 인증

Sanctum은 Laravel 기반 API와 통신해야 하는 SPA의 인증을 위해서도 존재합니다. 이 SPA들은 애플리케이션과 같은 저장소에 있거나 별도의 저장소일 수 있습니다.

이 기능에서 Sanctum은 별도의 토큰을 사용하지 않으며, Laravel의 쿠키 기반 세션 인증을 사용합니다. 이 인증 방식은 CSRF 보호, 세션 인증 그리고 XSS를 통한 인증 정보 유출 방지의 이점을 제공합니다.

> {note} SPA와 API가 서로 다른 서브도메인은 허용하지만, 같은 최상위 도메인을 공유해야 하며, 요청에 반드시 `Accept: application/json` 헤더를 포함시켜야 합니다.

<a name="spa-configuration"></a>
### 설정

<a name="configuring-your-first-party-domains"></a>
#### 1차 도메인 설정하기

먼저, SPA가 어떤 도메인에서 요청할 것인지 `sanctum` 설정 파일의 `stateful` 옵션에 명시해야 합니다. 이 설정은 어떤 도메인에서 들어오는 요청이 "상태 정보가 있는(stateful)" 세션 인증을 유지할지 결정합니다.

> {note} 포트(`127.0.0.1:8000` 등)가 붙은 URL을 쓸 경우 포트 번호도 반드시 포함하세요.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

그리고 나서 `app/Http/Kernel.php`의 `api` 미들웨어 그룹에 Sanctum 미들웨어를 추가하세요. 이 미들웨어는 SPA로부터 들어오는 요청이 Laravel 세션 쿠키로 인증될 수 있도록 하며, 외부/모바일 앱에서는 API 토큰 인증도 허용합니다:

    'api' => [
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

<a name="cors-and-cookies"></a>
#### CORS & 쿠키

별도의 서브도메인에서 SPA를 인증하는 데 문제가 생긴다면, CORS(교차 출처 리소스 공유)나 세션 쿠키 관련 설정이 잘못되었을 가능성이 높습니다.

애플리케이션의 CORS 설정에서 `Access-Control-Allow-Credentials: True` 헤더가 반환되는지 확인하세요. 이는 `config/cors.php`의 `supports_credentials` 옵션을 `true`로 지정해 해결할 수 있습니다.

프론트엔드에서 axios를 사용할 경우, 글로벌 `axios` 인스턴스에 `withCredentials` 옵션도 활성화해야 합니다. 보통 `resources/js/bootstrap.js`에서 지정합니다. axios를 사용하지 않는 경우에도 HTTP 클라이언트에 해당 설정을 적용하세요:

    axios.defaults.withCredentials = true;

마지막으로, 세션 쿠키 도메인 설정이 루트 도메인의 모든 서브도메인을 지원하도록 `config/session.php`에서 도메인 앞에 `.`(dot)을 붙이세요:

    'domain' => '.domain.com',

<a name="spa-authenticating"></a>
### 인증하기

<a name="csrf-protection"></a>
#### CSRF 보호

SPA에서 인증을 시작하려면, 로그인 페이지에서 `/sanctum/csrf-cookie` 엔드포인트에 먼저 요청을 보냅니다. 이 엔드포인트는 CSRF 보호를 초기화합니다:

    axios.get('/sanctum/csrf-cookie').then(response => {
        // 로그인 요청...
    });

이 요청을 통해 Laravel은 `XSRF-TOKEN` 쿠키를 설정하며, 이 토큰은 이후 요청 시 `X-XSRF-TOKEN` 헤더로 전달되어야 합니다. axios, Angular HttpClient 등은 이 처리를 자동으로 해줍니다. 사용 중인 JavaScript HTTP 라이브러리가 자동 처리하지 않는다면 직접 `X-XSRF-TOKEN` 헤더에 해당 쿠키 값을 설정해야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호가 초기화된 후, Laravel 애플리케이션의 `/login` 라우트로 `POST` 요청을 보냅니다. 이 라우트는 [직접 구현](/docs/{{version}}/authentication#authenticating-users)하거나, [Laravel Fortify](/docs/{{version}}/fortify) 등 헤드리스 인증 패키지로 사용할 수 있습니다.

로그인 성공 시, 세션 쿠키를 통해 자동으로 후속 요청이 인증됩니다. `/sanctum/csrf-cookie`를 이미 요청했으므로, 이후 요청 모두 CSRF 보호를 받게 됩니다.

사용자의 세션이 만료(활동 없음 등)된 경우에는 401, 419 HTTP 오류가 발생할 수 있습니다. 이 경우 SPA의 로그인 페이지로 리다이렉트하세요.

> {note} `/login` 엔드포인트는 직접 만들어도 되지만 반드시 [Laravel 표준 세션 인증](/docs/{{version}}/authentication#authenticating-users)을 사용해야 합니다(일반적으로 `web` 가드를 활용).

<a name="protecting-spa-routes"></a>
### 라우트 보호하기

모든 API 경로에 인증 요구가 필요하다면, `routes/api.php`에서 `sanctum` 인증 가드를 미들웨어로 지정하세요. 이는 SPA의 상태 인증 및 외부의 API 토큰 인증 모두를 지원합니다:

    use Illuminate\Http\Request;

    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

<a name="authorizing-private-broadcast-channels"></a>
### 프라이빗 브로드캐스트 채널 권한 부여

SPA가 [프라이빗/프리젠스 브로드캐스트 채널](/docs/{{version}}/broadcasting#authorizing-channels) 인증이 필요하다면, `routes/api.php`에서 `Broadcast::routes`를 호출하세요:

    Broadcast::routes(['middleware' => ['auth:sanctum']]);

그리고, [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation) 초기화 시 Pusher의 `authorizer`를 커스터마이즈하여 cross-domain 요청이 정상적으로 작동하도록 axios 인스턴스를 사용합니다:

    window.Echo = new Echo({
        broadcaster: "pusher",
        cluster: process.env.MIX_PUSHER_APP_CLUSTER,
        encrypted: true,
        key: process.env.MIX_PUSHER_APP_KEY,
        authorizer: (channel, options) => {
            return {
                authorize: (socketId, callback) => {
                    axios.post('/api/broadcasting/auth', {
                        socket_id: socketId,
                        channel_name: channel.name
                    })
                    .then(response => {
                        callback(false, response.data);
                    })
                    .catch(error => {
                        callback(true, error);
                    });
                }
            };
        },
    })

<a name="mobile-application-authentication"></a>
## 모바일 애플리케이션 인증

모바일 애플리케이션에서 API 요청을 인증할 때도 Sanctum 토큰을 사용할 수 있습니다. 인증 절차는 외부 API 요청 인증과 유사하지만, 토큰 발급 방식에서 약간의 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급

먼저 사용자의 이메일/아이디, 비밀번호, 디바이스 이름을 받아 새로운 Sanctum 토큰으로 교환하는 엔드포인트를 만듭니다. "디바이스 이름"은 사용자 구분에 편리한 어떤 값이든 가능합니다(예: "철수의 iPhone 12").

일반적으로 모바일 앱의 로그인 화면에서 이 엔드포인트로 요청하며, 응답받은 평문 API 토큰을 디바이스에 저장해 추가 API 요청에 사용합니다:

    use App\Models\User;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Hash;
    use Illuminate\Validation\ValidationException;

    Route::post('/sanctum/token', function (Request $request) {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required',
            'device_name' => 'required',
        ]);

        $user = User::where('email', $request->email)->first();

        if (! $user || ! Hash::check($request->password, $user->password)) {
            throw ValidationException::withMessages([
                'email' => ['입력한 인증 정보가 올바르지 않습니다.'],
            ]);
        }

        return $user->createToken($request->device_name)->plainTextToken;
    });

모바일 애플리케이션이 API 요청 시 토큰을 쓸 때는 `Authorization` 헤더에 `Bearer` 토큰으로 전달해야 합니다.

> {tip} 모바일 애플리케이션 토큰 생성 시에도 [토큰 권한](#token-abilities) 지정이 가능합니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호하기

앞서 설명했듯이, `sanctum` 인증 가드를 이용해 경로를 보호할 수 있습니다:

    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

<a name="revoking-mobile-api-tokens"></a>
### 토큰 폐기

사용자가 모바일 디바이스에서 발급받은 API 토큰을 폐기할 수 있게, 웹 UI의 "계정 설정" 등에서 토큰 이름과 함께 "폐기" 버튼을 표시하세요. 버튼 클릭 시 데이터베이스에서 해당 토큰을 삭제하면 됩니다(`Laravel\Sanctum\HasApiTokens`의 `tokens` 관계 사용):

    // 모든 토큰 폐기
    $user->tokens()->delete();

    // 특정 토큰 폐기
    $user->tokens()->where('id', $tokenId)->delete();

<a name="testing"></a>
## 테스트

테스트 시, `Sanctum::actingAs` 메소드를 사용해 인증 사용자 및 부여할 ability를 지정할 수 있습니다:

    use App\Models\User;
    use Laravel\Sanctum\Sanctum;

    public function test_task_list_can_be_retrieved()
    {
        Sanctum::actingAs(
            User::factory()->create(),
            ['view-tasks']
        );

        $response = $this->get('/api/task');

        $response->assertOk();
    }

토큰에 모든 권한을 부여하려면 ability 목록에 `*`를 포함시키면 됩니다:

    Sanctum::actingAs(
        User::factory()->create(),
        ['*']
    );
