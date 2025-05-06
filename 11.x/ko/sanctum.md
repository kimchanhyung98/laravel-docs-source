# Laravel Sanctum

- [소개](#introduction)
    - [동작 방식](#how-it-works)
- [설치](#installation)
- [구성](#configuration)
    - [기본 모델 오버라이딩](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 권한(Abilities)](#token-abilities)
    - [라우트 보호하기](#protecting-routes)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [구성](#spa-configuration)
    - [인증하기](#spa-authenticating)
    - [라우트 보호하기](#protecting-spa-routes)
    - [개인 브로드캐스트 채널 권한 부여](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호하기](#protecting-mobile-api-routes)
    - [토큰 폐기](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션, 그리고 단순한 토큰 기반 API를 위한 가벼운 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 자신의 계정에 대해 여러 개의 API 토큰을 생성할 수 있습니다. 이러한 토큰에는 토큰이 수행할 수 있는 동작을 지정하는 하나 이상의 권한(abilities)/스코프를 부여할 수 있습니다.

<a name="how-it-works"></a>
### 동작 방식

Laravel Sanctum은 두 가지 별도의 문제를 해결하기 위해 존재합니다. 라이브러리를 더 깊이 살펴보기 전에 각각을 간략하게 설명하겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰

첫째, Sanctum은 OAuth의 복잡함 없이 사용자에게 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 GitHub 및 기타 애플리케이션에서 제공하는 "개인 접근 토큰"에서 영감을 받았습니다. 예를 들어 애플리케이션의 "계정 설정" 화면에서 사용자가 자신의 계정용 API 토큰을 생성할 수 있는 UI를 제공한다고 생각해보세요. Sanctum으로 이 토큰들을 생성하고 관리할 수 있습니다. 이러한 토큰은 일반적으로 만료 기간이 매우 길지만(몇 년 등), 사용자가 언제든지 직접 폐기할 수 있습니다.

Laravel Sanctum은 사용자 API 토큰을 하나의 데이터베이스 테이블에 저장하고, 유효한 API 토큰이 포함된 `Authorization` 헤더를 통해 들어오는 HTTP 요청을 인증함으로써 이 기능을 제공합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증

둘째로, Sanctum은 Laravel 기반 API와 통신해야 하는 싱글 페이지 애플리케이션(SPA)을 간단하게 인증할 수 있는 방법을 제공합니다. 이러한 SPA는 Laravel 애플리케이션과 같은 저장소에 있거나 Next.js나 Nuxt로 제작된 별도의 저장소에 있을 수도 있습니다.

이 기능을 사용할 때 Sanctum은 어떠한 토큰도 사용하지 않습니다. 대신, Laravel의 내장 쿠키 기반 세션 인증 서비스를 사용합니다. 보통 Sanctum은 이 작업을 수행할 때 Laravel의 `web` 인증 가드를 활용합니다. 이 방식은 CSRF 보호, 세션 인증, 인증 자격 증명 정보가 XSS로 인해 유출되는 것을 방지하는 장점이 있습니다.

Sanctum은 들어오는 요청이 SPA 프론트엔드에서 기원한 경우에만 쿠키 기반 인증을 시도합니다. 들어오는 HTTP 요청을 검사할 때 먼저 인증 쿠키가 있는지 확인하고, 없으면 `Authorization` 헤더에 유효한 API 토큰이 있는지 확인합니다.

> [!NOTE]  
> Sanctum을 API 토큰 인증에만, 혹은 SPA 인증에만 사용하는 것도 완전히 괜찮습니다. Sanctum을 사용한다고 해서 두 가지 기능을 모두 반드시 사용할 필요는 없습니다.

<a name="installation"></a>
## 설치

`install:api` Artisan 명령어를 통해 Laravel Sanctum을 설치할 수 있습니다.

```shell
php artisan install:api
```

이후, SPA 인증을 위해 Sanctum을 활용하고자 한다면 이 문서의 [SPA 인증](#spa-authentication) 섹션을 참고하세요.

<a name="configuration"></a>
## 구성

<a name="overriding-default-models"></a>
### 기본 모델 오버라이딩

필수는 아니지만, Sanctum 내부적으로 사용하는 `PersonalAccessToken` 모델을 자유롭게 확장할 수 있습니다.

    use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

    class PersonalAccessToken extends SanctumPersonalAccessToken
    {
        // ...
    }

그런 다음 Sanctum에서 제공하는 `usePersonalAccessTokenModel` 메서드를 통해 커스텀 모델을 사용하도록 지시할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 파일의 `boot` 메서드에서 호출합니다.

    use App\Models\Sanctum\PersonalAccessToken;
    use Laravel\Sanctum\Sanctum;

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
    }

<a name="api-token-authentication"></a>
## API 토큰 인증

> [!NOTE]  
> 1차 애플리케이션의 SPA 인증에는 API 토큰을 사용하지 마세요. 대신 Sanctum의 내장 [SPA 인증 기능](#spa-authentication)을 사용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급

Sanctum을 사용하면 API 요청을 인증하는 데 사용할 수 있는 API 토큰/개인 접근 토큰을 발급할 수 있습니다. API 토큰을 사용할 때는 토큰 값을 `Bearer` 토큰으로 `Authorization` 헤더에 포함시켜야 합니다.

사용자에게 토큰을 발급하려면 User 모델이 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용해야 합니다.

    use Laravel\Sanctum\HasApiTokens;

    class User extends Authenticatable
    {
        use HasApiTokens, HasFactory, Notifiable;
    }

토큰을 발급하려면 `createToken` 메서드를 사용합니다. `createToken`은 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전 SHA-256 해싱 처리되며, 평문 토큰 값은 `NewAccessToken` 인스턴스의 `plainTextToken` 프로퍼티로 접근할 수 있습니다. 이 값은 토큰 생성 직후 반드시 사용자에게 표시해야 합니다.

    use Illuminate\Http\Request;

    Route::post('/tokens/create', function (Request $request) {
        $token = $request->user()->createToken($request->token_name);

        return ['token' => $token->plainTextToken];
    });

`HasApiTokens` 트레이트가 제공하는 `tokens` Eloquent 관계를 사용하여 사용자의 모든 토큰에 접근할 수 있습니다.

    foreach ($user->tokens as $token) {
        // ...
    }

<a name="token-abilities"></a>
### 토큰 권한(Abilities)

Sanctum에서는 토큰에 "권한(abilities)"을 할당할 수 있습니다. 권한은 OAuth 스코프와 비슷한 기능입니다. 토큰 생성 시 `createToken` 두 번째 인수로 문자열 배열을 전달하여 권한을 지정할 수 있습니다.

    return $user->createToken('token-name', ['server:update'])->plainTextToken;

Sanctum으로 인증된 요청을 처리할 때, 토큰에 특정 권한이 있는지 `tokenCan` 또는 `tokenCant` 메서드로 확인할 수 있습니다.

    if ($user->tokenCan('server:update')) {
        // ...
    }

    if ($user->tokenCant('server:update')) {
        // ...
    }

<a name="token-ability-middleware"></a>
#### 토큰 권한 미들웨어

Sanctum에는 토큰에 특정 권한이 부여되었는지 검증할 수 있는 두 개의 미들웨어도 제공합니다. 먼저, 애플리케이션의 `bootstrap/app.php` 파일에서 다음과 같이 미들웨어 별칭을 정의하세요.

    use Laravel\Sanctum\Http\Middleware\CheckAbilities;
    use Laravel\Sanctum\Http\Middleware\CheckForAnyAbility;

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->alias([
            'abilities' => CheckAbilities::class,
            'ability' => CheckForAnyAbility::class,
        ]);
    })

`abilities` 미들웨어는 들어오는 요청의 토큰이 지정된 모든 권한을 가지고 있는지 검증합니다.

    Route::get('/orders', function () {
        // "check-status"와 "place-orders" 권한을 모두 소유한 토큰...
    })->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);

`ability` 미들웨어는 토큰이 나열된 권한 중 *하나 이상*을 가지고 있는지만 확인합니다.

    Route::get('/orders', function () {
        // "check-status" 혹은 "place-orders" 권한 중 하나라도 있으면...
    })->middleware(['auth:sanctum', 'ability:check-status,place-orders']);

<a name="first-party-ui-initiated-requests"></a>
#### 1차 UI에서 시작된 요청

편의를 위해, 첫 번째 파티 SPA로부터 인증된 요청이라면 `tokenCan` 메서드는 항상 `true`를 반환합니다(내장 [SPA 인증](#spa-authentication) 사용 시).

그러나 이것이 반드시 사용자가 해당 동작을 해야 한다는 의미는 아닙니다. 일반적으로 애플리케이션의 [권한 정책](/docs/{{version}}/authorization#creating-policies)에서 토큰의 권한 부여, 그리고 사용자 인스턴스 자체가 작업을 수행할 수 있는지 추가로 확인합니다.

예를 들어, 서버를 관리하는 애플리케이션을 예로 들면, 토큰이 서버 업데이트 권한이 있고 **그리고** 해당 서버가 사용자 소유인지 확인할 수 있습니다.

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

처음에는 `tokenCan` 메서드가 1차 UI에서 시작된 요청 모두에 대해 항상 `true`를 반환하도록 허용하는 것이 이상해 보일 수 있습니다. 하지만, 항상 API 토큰이 존재하고 `tokenCan`을 자유롭게 호출할 수 있다고 가정할 수 있다는 점이 편리합니다. 이 방식을 사용하면, 요청이 애플리케이션 UI에서 유발된 것인지, API의 외부 소비자가 호출한 것인지를 따로 구분하지 않고 항상 권한 정책 내에서 `tokenCan`을 호출할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호하기

모든 요청이 인증되도록 라우트를 보호하려면 `routes/web.php` 또는 `routes/api.php` 파일의 보호 대상 라우트에 `sanctum` 인증 가드를 붙이세요. 이 가드는 들어오는 요청이 상태 기반(쿠키 인증) 또는 제3자에서 오는 경우 유효한 API 토큰 헤더를 갖추었는지 보장합니다.

왜 `routes/web.php`에서 `sanctum` 가드로 인증하라 권고하는지 궁금할 수 있습니다. Sanctum은 먼저 Laravel의 일반적인 세션 인증 쿠키를 사용하여 인증 시도합니다. 해당 쿠키가 없을 때만 `Authorization` 헤더에 토큰이 있는지 확인합니다. 또한, Sanctum으로 모든 요청을 인증하면 현재 인증된 사용자 인스턴스에서 언제든지 `tokenCan`을 호출할 수 있습니다.

    use Illuminate\Http\Request;

    Route::get('/user', function (Request $request) {
        return $request->user();
    })->middleware('auth:sanctum');

<a name="revoking-tokens"></a>
### 토큰 폐기

`Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 관계를 통해 데이터베이스에서 토큰을 삭제함으로써 "토큰 폐기"가 가능합니다.

    // 모든 토큰 폐기
    $user->tokens()->delete();

    // 현재 요청에 사용된 토큰 폐기
    $request->user()->currentAccessToken()->delete();

    // 특정 토큰만 폐기
    $user->tokens()->where('id', $tokenId)->delete();

<a name="token-expiration"></a>
### 토큰 만료

기본적으로 Sanctum 토큰은 만료되지 않으며, [토큰을 폐기](#revoking-tokens)하지 않는 한 계속 유효합니다. 단, 토큰 만료까지의 시간을 설정하려면 앱의 `sanctum` 설정 파일의 `expiration` 옵션을 이용하면 됩니다. 이 옵션은 토큰이 만료로 간주될 때까지의(분 단위) 시간을 지정합니다.

```php
'expiration' => 525600,
```

각 토큰의 만료 시간을 개별적으로 지정하고 싶다면, `createToken` 메서드의 세 번째 인수로 만료 시간을 전달하면 됩니다.

```php
return $user->createToken(
    'token-name', ['*'], now()->addWeek()
)->plainTextToken;
```

앱에서 토큰 만료 시간을 지정하였다면, 만료된 토큰을 정리하는 [태스크 예약](/docs/{{version}}/scheduling)도 고려할 수 있습니다. 다행히 Sanctum에는 만료된 토큰을 정리하는 `sanctum:prune-expired` Artisan 명령어가 있습니다. 예를 들어, 만료 후 24시간 이상 지난 토큰을 매일 정리하도록 예약할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증

Sanctum은 또한, Laravel 기반 API와 통신해야 하는 SPA(싱글 페이지 애플리케이션)를 간단하게 인증할 수 있는 방법을 제공합니다. 이런 SPA는 Laravel 애플리케이션과 같은 저장소에 있거나, 아니면 완전히 별도의 저장소에 있을 수 있습니다.

이 경우 토큰 대신 Laravel의 내장 쿠키 기반 세션 인증 서비스를 사용합니다. 이 방식은 CSRF 보호, 세션 인증, 인증 자격 증명 정보 누출 방지(XSS 방지)의 이점이 있습니다.

> [!WARNING]  
> 인증을 위해 SPA와 API는 반드시 동일한 최상위 도메인(Top-level domain)을 공유해야 합니다. 단, 서로 다른 서브도메인에 위치해도 무방합니다. 또한 반드시 `Accept: application/json` 헤더와 함께 요청에 `Referer` 또는 `Origin` 헤더를 포함해야 합니다.

<a name="spa-configuration"></a>
### 구성

<a name="configuring-your-first-party-domains"></a>
#### 1차 도메인 구성

먼저, SPA가 요청을 보낼 도메인을 구성해야 합니다. `sanctum` 설정 파일의 `stateful` 옵션을 통해 이 도메인들을 지정할 수 있습니다. 이 옵션은 API 요청 시 Laravel 세션 쿠키를 통한 "상태 기반" 인증을 유지할 도메인을 결정합니다.

> [!WARNING]  
> 포트(`127.0.0.1:8000`)가 포함된 URL로 앱을 접속할 경우, 도메인에 포트 번호도 반드시 포함해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

그 다음, SPA로부터 들어오는 요청은 Laravel의 세션 쿠키로 인증하도록, 제3자 또는 모바일 앱의 요청은 API 토큰으로 인증하도록 Laravel에 지시해야 합니다. 이는 `bootstrap/app.php` 파일에서 `statefulApi` 미들웨어 메서드를 호출하면 간단히 해결할 수 있습니다.

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->statefulApi();
    })

<a name="cors-and-cookies"></a>
#### CORS 및 쿠키

별도의 서브도메인에서 실행되는 SPA로부터 인증에 문제가 있다면, CORS(교차 출처 리소스 공유) 또는 세션 쿠키 설정이 잘못되어 있을 가능성이 높습니다.

`config/cors.php` 설정 파일은 기본적으로 공개되지 않습니다. CORS 옵션을 수정하려면 `config:publish` Artisan 명령어로 전체 `cors` 설정 파일을 공개해야 합니다.

```bash
php artisan config:publish cors
```

그 다음, 앱의 CORS 설정이 `Access-Control-Allow-Credentials` 헤더를 `True`로 반환하는지도 확인해야 합니다. 앱의 `config/cors.php`에서 `supports_credentials` 옵션을 `true`로 지정하면 됩니다.

또한, 앱의 전역 `axios` 인스턴스에서 `withCredentials` 및 `withXSRFToken` 옵션을 활성화해야 합니다. 이는 일반적으로 `resources/js/bootstrap.js` 파일에서 수행합니다. Axios를 사용하지 않는다면, 사용하는 HTTP 클라이언트에도 해당 옵션을 적용하세요.

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

마지막으로 앱의 세션 쿠키 도메인 설정이 루트 도메인의 모든 서브도메인을 지원하는지 확인해야 합니다. 이를 위해 도메인 앞에 마침표(`.`)를 붙여 `config/session.php`에 설정하세요.

    'domain' => '.domain.com',

<a name="spa-authenticating"></a>
### 인증하기

<a name="csrf-protection"></a>
#### CSRF 보호

SPA 인증을 위해서는 먼저 SPA의 "로그인" 페이지에서 `/sanctum/csrf-cookie` 엔드포인트로 요청을 보내, CSRF 보호를 초기화해야 합니다.

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // 로그인 진행...
});
```

이 요청을 처리하면 Laravel이 현재의 CSRF 토큰이 담긴 `XSRF-TOKEN` 쿠키를 세팅합니다. 이후 요청에서는 이 토큰을 URL 디코드하여 `X-XSRF-TOKEN` 헤더에 포함시켜야 하며, Axios 및 Angular HttpClient 등 일부 HTTP 클라이언트 라이브러리는 이를 자동으로 처리합니다. 사용하는 라이브러리가 자동으로 이를 처리하지 않는 경우, `XSRF-TOKEN` 쿠키의 URL 디코드 값을 직접 `X-XSRF-TOKEN` 헤더에 할당해야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호가 초기화된 후에는 Laravel 앱의 `/login` 경로로 `POST` 요청을 보내야 합니다. 이 `/login` 경로는 [직접 구현](/docs/{{version}}/authentication#authenticating-users)하거나 [Laravel Fortify](/docs/{{version}}/fortify)와 같은 헤드리스 인증 패키지를 사용할 수 있습니다.

로그인 요청이 성공하면 세션 쿠키가 발급되고 이후의 모든 요청은 자동으로 인증됩니다. 또한 `/sanctum/csrf-cookie` 라우트에 이미 접근했기 때문에, JS HTTP 클라이언트가 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더에 포함하는 한 자동으로 CSRF 보호도 받을 수 있습니다.

사용자 세션이 만료(비활동 시)되면 이후 요청에 401 또는 419 오류가 반환될 수 있으니, 이때는 SPA의 로그인 페이지로 사용자 리디렉션이 필요합니다.

> [!WARNING]  
> 직접 `/login` 엔드포인트를 구현할 수도 있으나, 반드시 Laravel의 표준 [세션 기반 인증 서비스](/docs/{{version}}/authentication#authenticating-users)로 사용자를 인증해야 합니다. 일반적으로는 `web` 인증 가드를 사용하게 됩니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호하기

모든 요청이 인증되도록 API 라우트(`routes/api.php`)에 `sanctum` 인증 가드를 부착하세요. 이 가드는 SPA에서 오는 상태 인증 요청이든, 제3자의 유효한 API 토큰이든 모두 인증을 보장합니다.

    use Illuminate\Http\Request;

    Route::get('/user', function (Request $request) {
        return $request->user();
    })->middleware('auth:sanctum');

<a name="authorizing-private-broadcast-channels"></a>
### 개인 브로드캐스트 채널 권한 부여

SPA가 [개인/프레즌스 브로드캐스트 채널](/docs/{{version}}/broadcasting#authorizing-channels)과 인증해야 한다면, `bootstrap/app.php`의 `withRouting` 메서드에서 `channels` 엔트리를 제거하고, `withBroadcasting` 메서드를 사용하여 브로드캐스팅 라우트에 올바른 미들웨어를 지정하세요.

    return Application::configure(basePath: dirname(__DIR__))
        ->withRouting(
            web: __DIR__.'/../routes/web.php',
            // ...
        )
        ->withBroadcasting(
            __DIR__.'/../routes/channels.php',
            ['prefix' => 'api', 'middleware' => ['api', 'auth:sanctum']],
        )

그 다음, Pusher의 인증 요청이 성공하려면, [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation)를 초기화할 때 커스텀 Pusher `authorizer`를 제공해야 합니다. 이로써 완전히 [교차 도메인 요청에 맞게 설정된 axios 인스턴스](#cors-and-cookies)를 사용할 수 있습니다.

```js
window.Echo = new Echo({
    broadcaster: "pusher",
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    encrypted: true,
    key: import.meta.env.VITE_PUSHER_APP_KEY,
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
```

<a name="mobile-application-authentication"></a>
## 모바일 애플리케이션 인증

모바일 애플리케이션의 API 요청 인증에도 Sanctum 토큰을 사용할 수 있습니다. 모바일 인증과 제3자 API 인증 방식은 유사하나, API 토큰을 발급하는 방식에서 약간 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급

먼저, 사용자의 이메일 혹은 사용자명, 비밀번호, 그리고 디바이스 이름을 전달받아 이 자격 증명과 교환으로 새 Sanctum 토큰을 발급하는 라우트를 생성하세요. 이 엔드포인트에 전달하는 "디바이스 이름"은 식별용이며, 예를 들어 "Nuno의 iPhone 12"와 같이 사용자가 인지할 수 있는 이름을 권장합니다.

보통 모바일 앱의 "로그인" 화면에서 이 토큰 엔드포인트로 요청을 보냅니다. 엔드포인트는 평문 API 토큰을 반환하고, 모바일 기기에 저장해 추가 API 요청에 사용할 수 있습니다.

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
                'email' => ['입력한 자격증명이 올바르지 않습니다.'],
            ]);
        }

        return $user->createToken($request->device_name)->plainTextToken;
    });

모바일 앱은 토큰을 API 요청 시 `Authorization` 헤더의 `Bearer` 토큰으로 전달해야 합니다.

> [!NOTE]  
> 모바일 앱용 토큰을 발급할 때도 [토큰 권한](#token-abilities)을 자유롭게 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호하기

앞서 설명한 대로, 모든 요청이 인증되도록 라우트에 `sanctum` 인증 가드를 부착할 수 있습니다.

    Route::get('/user', function (Request $request) {
        return $request->user();
    })->middleware('auth:sanctum');

<a name="revoking-mobile-api-tokens"></a>
### 토큰 폐기

모바일 기기용 API 토큰 폐기를 위해, 웹 애플리케이션의 "계정 설정" 섹션에서 각 토큰을 디바이스 이름과 함께 리스트로 보여주고 "폐기" 버튼을 제공할 수 있습니다. 사용자가 "폐기" 버튼을 클릭하면 데이터베이스에서 해당 토큰을 삭제하면 됩니다. 사용자 API 토큰에 접근하려면, `Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 관계를 사용하세요.

    // 모든 토큰 폐기
    $user->tokens()->delete();

    // 특정 토큰만 폐기
    $user->tokens()->where('id', $tokenId)->delete();

<a name="testing"></a>
## 테스트

테스트 시, `Sanctum::actingAs` 메서드를 활용해 사용자를 인증하고 토큰에 어떤 권한을 부여할지 지정할 수 있습니다.

```php tab=Pest
use App\Models\User;
use Laravel\Sanctum\Sanctum;

test('task list can be retrieved', function () {
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Sanctum\Sanctum;

public function test_task_list_can_be_retrieved(): void
{
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
}
```

토큰에 모든 권한을 부여하려면, `actingAs` 메서드에 능력 목록으로 `*`을 포함시키세요.

    Sanctum::actingAs(
        User::factory()->create(),
        ['*']
    );
