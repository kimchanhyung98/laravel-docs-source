# Laravel Sanctum

- [소개](#introduction)
    - [작동 원리](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 권한](#token-abilities)
    - [라우트 보호](#protecting-routes)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증하기](#spa-authenticating)
    - [라우트 보호](#protecting-spa-routes)
    - [프라이빗 방송 채널 권한 부여](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호](#protecting-mobile-api-routes)
    - [토큰 폐기](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(single page applications), 모바일 애플리케이션, 그리고 단순 토큰 기반 API를 위한 경량 인증 시스템을 제공합니다. Sanctum은 애플리케이션의 각 사용자에게 여러 개의 API 토큰을 생성할 수 있게 해줍니다. 이 토큰들에는 토큰이 허용된 동작을 지정하는 권한(abilities) 또는 스코프(scopes)를 부여할 수 있습니다.

<a name="how-it-works"></a>
### 작동 원리 (How it Works)

Laravel Sanctum은 두 가지 별개의 문제를 해결하기 위해 만들어졌습니다. 각각에 대해 설명한 후 라이브러리의 세부 내용을 살펴보겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰 (API Tokens)

첫째, Sanctum은 OAuth의 복잡함 없이 사용자에게 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 GitHub 등에서 발급하는 "personal access tokens"에서 영감을 받았습니다. 예를 들어, 애플리케이션의 "계정 설정" 화면에서 사용자가 자신의 계정에 대한 API 토큰을 생성할 수 있다고 가정해봅시다. Sanctum을 사용하면 이러한 토큰을 생성하고 관리할 수 있습니다. 이 토큰들은 보통 수년 단위로 매우 긴 만료 시간을 가지지만, 사용자가 언제든 수동으로 폐기할 수 있습니다.

Laravel Sanctum은 사용자 API 토큰을 단일 데이터베이스 테이블에 저장하고, 유효한 API 토큰을 포함한 요청의 `Authorization` 헤더를 통해 오는 HTTP 요청을 인증함으로써 이 기능을 제공합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증 (SPA Authentication)

둘째, Sanctum은 Laravel 기반 API와 통신해야 하는 싱글 페이지 애플리케이션(SPA)을 쉽게 인증하는 방법을 제공합니다. 이 SPA들은 라라벨 애플리케이션과 같은 저장소에 있을 수도 있고, Next.js 또는 Nuxt로 만든 완전히 별도의 저장소일 수도 있습니다.

이 기능을 위해 Sanctum은 어떠한 토큰도 사용하지 않습니다. 대신, Laravel의 내장 쿠키 기반 세션 인증 서비스를 활용합니다. 보통 Sanctum은 Laravel의 `web` 인증 가드를 사용하여 이 작업을 수행합니다. 이 방법은 CSRF 보호, 세션 인증의 이점을 제공하고, XSS에 의한 인증 정보 노출도 막아줍니다.

Sanctum은 클라이언트 요청이 자사 SPA 프론트엔드에서 오는 경우에만 쿠키 인증을 시도합니다. 요청을 검사할 때 Sanctum은 먼저 인증용 쿠키 존재를 확인하며, 만약 쿠키가 없으면 `Authorization` 헤더에 있는 API 토큰을 검사합니다.

> [!NOTE]  
> Sanctum은 API 토큰 인증 전용으로 혹은 SPA 인증 전용으로만 사용해도 무방합니다. Sanctum을 사용한다 해서 두 가지 기능을 모두 반드시 사용해야 하는 것은 아닙니다.

<a name="installation"></a>
## 설치 (Installation)

Laravel Sanctum은 `install:api` Artisan 명령어로 설치할 수 있습니다:

```shell
php artisan install:api
```

그 후, SPA 인증에 Sanctum을 활용할 예정이라면, 본 문서의 [SPA 인증](#spa-authentication) 섹션을 참고하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="overriding-default-models"></a>
### 기본 모델 재정의 (Overriding Default Models)

일반적으론 필요하지 않지만, Sanctum이 내부적으로 사용하는 `PersonalAccessToken` 모델을 자유롭게 확장할 수 있습니다:

```
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

그 다음, Sanctum이 사용자정의 모델을 사용하도록 지시하려면 `usePersonalAccessTokenModel` 메서드를 호출하면 됩니다. 보통 `AppServiceProvider` 파일의 `boot` 메서드에서 호출합니다:

```
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a name="api-token-authentication"></a>
## API 토큰 인증 (API Token Authentication)

> [!NOTE]  
> API 토큰을 이용해 자체 SPA를 인증하지 마세요. 대신 Sanctum의 내장된 [SPA 인증 기능](#spa-authentication)을 사용하십시오.

<a name="issuing-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

Sanctum을 사용하면 API 토큰(개인 액세스 토큰)을 발급하여 API 요청을 인증하는 데 활용할 수 있습니다. API 토큰을 사용하는 경우, 토큰을 `Authorization` 헤더에 `Bearer` 토큰 형식으로 포함시켜야 합니다.

사용자에게 토큰을 발급하려면 User 모델에 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용해야 합니다:

```
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

토큰을 발급하려면 `createToken` 메서드를 사용하세요. 이 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전에 SHA-256 해싱을 거치지만, `NewAccessToken` 인스턴스의 `plainTextToken` 속성으로 원문 토큰 값을 얻을 수 있습니다. 이 값을 토큰이 생성된 직후 사용자에게 보여줘야 합니다:

```
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->reateToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

`HasApiTokens` 트레이트가 제공하는 `tokens` Eloquent 연관관계를 사용해 사용자의 모든 토큰에 접근할 수도 있습니다:

```
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
### 토큰 권한 (Token Abilities)

Sanctum은 토큰에 "abilities"(권한)를 부여할 수 있습니다. abilities는 OAuth의 "scopes"와 유사한 역할을 합니다. `createToken` 메서드의 두 번째 인수로 abilities 문자열 배열을 전달할 수 있습니다:

```
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Sanctum으로 인증된 요청 처리 시, 토큰에 특정 권한이 있는지 `tokenCan` 또는 `tokenCant` 메서드를 통해 확인할 수 있습니다:

```
if ($user->tokenCan('server:update')) {
    // ...
}

if ($user->tokenCant('server:update')) {
    // ...
}
```

<a name="token-ability-middleware"></a>
#### 토큰 권한 미들웨어

Sanctum은 권한을 가진 토큰으로 인증된 요청인지 확인하는 두 개의 미들웨어를 제공합니다. 우선, 애플리케이션의 `bootstrap/app.php`에서 다음 미들웨어 별칭을 정의하세요:

```
use Laravel\Sanctum\Http\Middleware\CheckAbilities;
use Laravel\Sanctum\Http\Middleware\CheckForAnyAbility;

->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'abilities' => CheckAbilities::class,
        'ability' => CheckForAnyAbility::class,
    ]);
})
```

`abilities` 미들웨어는 라우트에 할당되어, 들어오는 요청 토큰이 지정된 모든 권한을 가지고 있는지 검사합니다:

```
Route::get('/orders', function () {
    // 토큰이 "check-status"와 "place-orders" 권한 모두를 가지고 있음...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` 미들웨어는 라우트에 할당되어, 토큰이 지정된 권한 중 *최소 하나*를 가지고 있는지 검사합니다:

```
Route::get('/orders', function () {
    // 토큰이 "check-status" 또는 "place-orders" 권한 중 하나 이상을 가지고 있음...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### 1차 UI에서 시작한 요청 (First-Party UI Initiated Requests)

편의를 위해, `tokenCan` 메서드는 들어오는 인증 요청이 1차 SPA에서 온 것이고 Sanctum의 내장 [SPA 인증 기능](#spa-authentication)을 사용하는 경우 항상 `true`를 반환합니다.

하지만 이것이 곧 애플리케이션이 사용자의 해당 권한 수행을 허용해야 함을 의미하는 것은 아닙니다. 보통 애플리케이션의 [인가 정책](/docs/11.x/authorization#creating-policies)이 토큰에 권한이 부여되었는지, 그리고 사용자 인스턴스가 실제로 해당 동작을 수행할 수 있는지 판단합니다.

예를 들어, 서버를 관리하는 애플리케이션이라면, 토큰이 서버 업데이트 권한이 있는지와 서버가 해당 사용자에게 속해있는지를 둘 다 확인하는 요건일 수 있습니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

처음에는 UI에서 온 요청에 대해 `tokenCan`이 항상 `true`를 반환하는 것이 이상할 수 있으나, API 토큰이 항상 존재한다고 가정하고 `tokenCan` 메서드를 활용할 수 있다는 점에서 편리합니다. 이렇게 하면 API가 3자 소비자에 의해 호출되었는지, 자체 UI에 의해 호출되었는지에 관계없이 애플리케이션 내 인가 정책에서 `tokenCan` 메서드를 일관되게 호출할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

모든 요청을 반드시 인증하도록 라우트를 보호하려면, `routes/web.php` 및 `routes/api.php` 파일 내 보호할 라우트에 `sanctum` 인증 가드를 연결하면 됩니다. 이 가드는 들어오는 요청이 상태 기반의 쿠키 인증 요청이거나, 만약 타사 요청이라면 유효한 API 토큰 헤더를 포함하는지 확인합니다.

왜 기본적으로 `routes/web.php`에서 `sanctum` 가드를 사용해 인증하라고 제안하는지 궁금할 수 있는데, Sanctum은 우선 Laravel의 일반 세션 인증 쿠키로 인증을 시도합니다. 쿠키가 없으면 `Authorization` 헤더 기반 API 토큰 인증을 시도합니다. 또한 `sanctum`을 사용하면 현재 인증된 사용자 인스턴스에서 항상 `tokenCan` 메서드를 호출할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-tokens"></a>
### 토큰 폐기 (Revoking Tokens)

DB에서 토큰을 삭제하여 "폐기"할 수 있습니다. 이는 `Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 연관관계를 통해 가능합니다:

```
// 모든 토큰 폐기...
$user->tokens()->delete();

// 현재 요청을 인증한 토큰 폐기...
$request->user()->currentAccessToken()->delete();

// 특정 토큰 폐기...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### 토큰 만료 (Token Expiration)

기본적으로 Sanctum 토큰은 만료되지 않으며, 오직 [폐기](#revoking-tokens)로만 무효화됩니다. 그러나 애플리케이션 API 토큰에 만료 시간을 설정하려면 `config/sanctum.php` 설정 파일의 `expiration` 옵션을 사용하세요. 이 옵션은 토큰 발급 후 만료까지의 분 단위 시간을 지정합니다:

```php
'expiration' => 525600,
```

각 토큰마다 개별 만료 시간을 지정하려면 `createToken` 메서드의 세 번째 인수로 만료 시간을 전달할 수 있습니다:

```php
return $user->createToken(
    'token-name', ['*'], now()->addWeek()
)->plainTextToken;
```

만료 시간 정의 시, [스케줄링](/docs/11.x/scheduling)을 활용해 만료된 토큰을 주기적으로 정리하는 것이 좋습니다. Sanctum은 만료된 토큰을 삭제하는 `sanctum:prune-expired` Artisan 명령어를 제공합니다. 예를 들어, 24시간 이상 만료된 토큰을 매일 삭제하도록 스케줄러를 설정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

Sanctum은 Laravel API와 통신하는 SPA를 위한 간단한 인증 방법도 제공합니다. 이 SPA들은 라라벨 애플리케이션과 동일한 저장소에 있을 수도 있고, 완전히 별도의 저장소에 존재할 수도 있습니다.

이 기능에서는 Sanctum이 어떠한 토큰도 사용하지 않고, Laravel의 쿠키 기반 세션 인증 서비스를 활용합니다. 이를 통해 CSRF 보호, 세션 인증, 인증 정보 XSS 유출 방지 효과를 얻습니다.

> [!WARNING]  
> SPA와 API는 동일한 최상위 도메인을 공유해야 합니다. 단, 서브도메인은 달라도 무방합니다. 또한, 요청에 `Accept: application/json` 헤더와 `Referer` 또는 `Origin` 헤더를 반드시 포함해야 합니다.

<a name="spa-configuration"></a>
### 설정 (Configuration)

<a name="configuring-your-first-party-domains"></a>
#### 1차 도메인 구성 (Configuring Your First-Party Domains)

먼저, SPA가 요청을 보낼 도메인을 설정해야 합니다. `sanctum` 설정 파일의 `stateful` 옵션에 도메인 목록을 등록하세요. 이 설정은 어떤 도메인이 Laravel 세션 쿠키를 통해 "상태를 유지하는" 인증을 할지를 결정합니다.

> [!WARNING]  
> 포트번호가 포함된 URL(`127.0.0.1:8000` 등)로 접근한다면, 도메인 설정에 포트번호도 반드시 포함해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

다음으로, SPA 요청은 Laravel 세션 쿠키를 통해 인증하고, 타사 또는 모바일 앱 요청은 API 토큰으로 인증할 수 있게 하려면, 애플리케이션 `bootstrap/app.php` 파일에 `statefulApi` 미들웨어 메서드를 호출하세요:

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->statefulApi();
})
```

<a name="cors-and-cookies"></a>
#### CORS와 쿠키

별도 서브도메인에서 동작하는 SPA가 인증에 실패한다면 CORS(Cross-Origin Resource Sharing) 혹은 세션 쿠키 설정이 잘못된 경우가 많습니다.

`config/cors.php` 설정 파일은 기본 공개되지 않습니다. CORS 설정을 커스터마이징하려면 `config:publish` Artisan 명령어로 전체 `cors` 설정 파일을 공개하세요:

```bash
php artisan config:publish cors
```

그리고 반드시 `config/cors.php`의 `supports_credentials` 옵션을 `true`로 설정하여 `Access-Control-Allow-Credentials` 헤더가 포함되도록 해야 합니다.

또한, 프론트엔드의 글로벌 axios 인스턴스에서 `withCredentials` 및 `withXSRFToken` 옵션을 활성화하세요. 보통 `resources/js/bootstrap.js`에 설정합니다. Axios 외 다른 HTTP 클라이언트를 사용한다면 이에 상응하는 설정을 적용해야 합니다:

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

마지막으로 세션 쿠키 도메인 설정(`config/session.php`의 `domain`)에 루트 도메인의 모든 서브도메인을 지원하려면, 도메인 앞에 점(`.`)을 붙여 명시하세요:

```
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 인증하기 (Authenticating)

<a name="csrf-protection"></a>
#### CSRF 보호

SPA 인증을 진행할 때, 로그인 페이지는 `/sanctum/csrf-cookie` 엔드포인트에 먼저 요청하여 CSRF 보호를 초기화해야 합니다:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // 로그인 처리...
});
```

이 요청에서 Laravel은 현재 CSRF 토큰이 담긴 `XSRF-TOKEN` 쿠키를 설정합니다. 이후 후속 요청에는 이 토큰을 URL 디코딩하여 `X-XSRF-TOKEN` 헤더에 담아 보내야 하며, Axios나 Angular HttpClient 같은 라이브러리는 이를 자동으로 처리합니다. 만약 HTTP 클라이언트가 자동 설정을 지원하지 않는다면, `XSRF-TOKEN` 쿠키 값을 수동으로 `X-XSRF-TOKEN` 헤더에 넣어줘야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호가 시작된 후, Laravel 애플리케이션의 `/login` 경로에 `POST` 요청을 보내 로그인합니다. `/login` 라우트는 수동 구현하거나 [Laravel Fortify](/docs/11.x/fortify) 같은 헤드리스 인증 패키지를 통해 구현할 수 있습니다.

로그인이 성공하면 세션 쿠키가 발급되어 해당 세션을 통해 후속 요청이 자동으로 인증됩니다. `/sanctum/csrf-cookie` 호출 덕분에 후속 요청에 CSRF 토큰도 적용됩니다.

사용자 세션이 활동 부족 등으로 만료되면 401 또는 419 HTTP 오류가 반환될 수 있습니다. 이 경우 SPA 로그인 페이지로 리다이렉트해야 합니다.

> [!WARNING]  
> `/login` 엔드포인트는 자유롭게 구현할 수 있으나, 반드시 Laravel이 제공하는 [표준 세션 기반 인증 서비스](/docs/11.x/authentication#authenticating-users)를 사용해야 합니다. 대개 `web` 인증 가드를 의미합니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호 (Protecting Routes)

SPA를 위해 API 라우트를 보호하려면, `routes/api.php`에서 해당 라우트에 `sanctum` 인증 가드를 적용하세요. 이 가드는 SPA에서 오는 상태 기반 인증 요청이거나 타사에서 온 유효한 API 토큰을 요구합니다:

```
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="authorizing-private-broadcast-channels"></a>
### 프라이빗 방송 채널 권한 부여 (Authorizing Private Broadcast Channels)

SPA가 [private / presence broadcast channels](/docs/11.x/broadcasting#authorizing-channels)를 인증하도록 하려면, `bootstrap/app.php`에서 `withRouting` 메서드의 `channels` 항목을 제거하고, 대신 `withBroadcasting` 메서드를 호출하여 적절한 미들웨어가 포함된 방송 라우트를 지정해야 합니다:

```
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        // ...
    )
    ->withBroadcasting(
        __DIR__.'/../routes/channels.php',
        ['prefix' => 'api', 'middleware' => ['api', 'auth:sanctum']],
    )
```

또한, Pusher의 권한 부여 요청이 성공하게 하려면, [Laravel Echo](/docs/11.x/broadcasting#client-side-installation)를 초기화할 때 커스텀 `authorizer`를 제공해야 합니다. 이 설정은 Pusher가 [올바르게 CORS와 쿠키 설정이 된 axios 인스턴스](#cors-and-cookies)를 사용하도록 돕습니다:

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
## 모바일 애플리케이션 인증 (Mobile Application Authentication)

Sanctum 토큰을 이용해 모바일 앱의 API 요청도 인증할 수 있습니다. 모바일 앱의 인증 과정은 서드파티 API 요청과 유사하지만, API 토큰 발급 방식은 약간 다를 수 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

시작하려면, 사용자의 이메일/아이디, 비밀번호, 디바이스 이름을 받아 토큰을 발급하는 라우트를 만듭니다. 디바이스 이름은 정보 제공용으로, 사용자가 인지할 수 있는 아무 값이나 됩니다. 예를 들어 "Nuno's iPhone 12"처럼요.

일반적으로 모바일 앱 로그인 화면에서 이 토큰 엔드포인트에 요청하여, 반환받은 원문 토큰을 모바일 기기에 저장하고 이후 API 요청에 사용합니다:

```
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
            'email' => ['The provided credentials are incorrect.'],
        ]);
    }

    return $user->createToken($request->device_name)->plainTextToken;
});
```

모바일 앱에서 API 요청 시, 토큰을 `Authorization` 헤더에 `Bearer` 형식으로 담아 전달해야 합니다.

> [!NOTE]  
> 모바일 앱용 토큰 발급 시에도 [토큰 권한](#token-abilities)을 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호 (Protecting Routes)

앞서 설명한 것과 같이, 모든 요청 인증이 필요하다면 `sanctum` 인증 가드를 해당 라우트에 붙이세요:

```
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-mobile-api-tokens"></a>
### 토큰 폐기 (Revoking Tokens)

모바일 기기에 발급된 API 토큰을 사용자가 폐기할 수 있게 하려면, 웹 UI의 계정 설정 등에서 토큰 이름과 함께 "폐기" 버튼을 노출하세요. 사용자가 클릭하면 DB에서 토큰을 삭제합니다. 토큰은 `Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 관계를 통해 접근할 수 있습니다:

```
// 모든 토큰 폐기...
$user->tokens()->delete();

// 특정 토큰 폐기...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 중에 `Sanctum::actingAs` 메서드를 사용해 특정 권한이 부여된 사용자로 인증을 시뮬레이션할 수 있습니다:

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

모든 권한을 부여하려면 `actingAs` 메서드에 `['*']`를 포함하세요:

```
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```