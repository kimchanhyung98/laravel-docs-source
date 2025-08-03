# Laravel Passport (Laravel Passport)

- [소개](#introduction)
    - [Passport 또는 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [Passport 업그레이드](#upgrading-passport)
- [구성](#configuration)
    - [토큰 수명 설정](#token-lifetimes)
    - [기본 모델 재정의하기](#overriding-default-models)
    - [라우트 재정의하기](#overriding-routes)
- [Authorization Code Grant(인가 코드 그랜트)](#authorization-code-grant)
    - [클라이언트 관리하기](#managing-clients)
    - [토큰 요청하기](#requesting-tokens)
    - [토큰 관리하기](#managing-tokens)
    - [토큰 갱신하기](#refreshing-tokens)
    - [토큰 폐기하기](#revoking-tokens)
    - [토큰 정리하기](#purging-tokens)
- [Authorization Code Grant With PKCE](#code-grant-pkce)
    - [클라이언트 생성하기](#creating-a-auth-pkce-grant-client)
    - [토큰 요청하기](#requesting-auth-pkce-grant-tokens)
- [Device Authorization Grant(기기 인증 그랜트)](#device-authorization-grant)
    - [기기 인증 그랜트 클라이언트 생성하기](#creating-a-device-authorization-grant-client)
    - [토큰 요청하기](#requesting-device-authorization-grant-tokens)
- [Password Grant(비밀번호 그랜트)](#password-grant)
    - [Password Grant 클라이언트 생성하기](#creating-a-password-grant-client)
    - [토큰 요청하기](#requesting-password-grant-tokens)
    - [모든 스코프 요청하기](#requesting-all-scopes)
    - [사용자 프로바이더 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 커스터마이징](#customizing-the-password-validation)
- [Implicit Grant(암묵적 그랜트)](#implicit-grant)
- [Client Credentials Grant(클라이언트 자격 증명 그랜트)](#client-credentials-grant)
- [Personal Access Tokens(개인 액세스 토큰)](#personal-access-tokens)
    - [개인 액세스 클라이언트 생성하기](#creating-a-personal-access-client)
    - [사용자 프로바이더 커스터마이징](#customizing-the-user-provider-for-pat)
    - [개인 액세스 토큰 관리하기](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어를 통해](#via-middleware)
    - [액세스 토큰 전달하기](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의하기](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당하기](#assigning-scopes-to-tokens)
    - [스코프 체크하기](#checking-scopes)
- [SPA 인증](#spa-authentication)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Passport](https://github.com/laravel/passport)는 Laravel 애플리케이션에서 몇 분 만에 완전한 OAuth2 서버 구현을 제공합니다. Passport는 Andy Millington과 Simon Hamp가 유지하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server) 위에 구축되어 있습니다.

> [!NOTE]
> 이 문서는 이미 OAuth2에 익숙하다고 가정합니다. OAuth2에 대해 전혀 모르는 경우, 계속하기 전에 일반적인 [용어 정리](https://oauth2.thephpleague.com/terminology/)와 OAuth2의 기능들을 먼저 익히시길 권장합니다.

<a name="passport-or-sanctum"></a>
### Passport 또는 Sanctum? (Passport or Sanctum?)

시작하기 전에, 애플리케이션에 Laravel Passport 또는 [Laravel Sanctum](/docs/12.x/sanctum) 중 어떤 것이 더 적합할지 판단하시길 바랍니다. 애플리케이션에서 OAuth2를 반드시 지원해야 한다면 Laravel Passport를 사용하세요.

반면, 싱글 페이지 애플리케이션, 모바일 애플리케이션 인증이나 API 토큰 발급이 목적이라면 [Laravel Sanctum](/docs/12.x/sanctum)을 사용하는 것이 좋습니다. Laravel Sanctum은 OAuth2를 지원하지 않지만, 훨씬 간단한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치 (Installation)

Laravel Passport는 `install:api` Artisan 명령어를 통해 설치할 수 있습니다:

```shell
php artisan install:api --passport
```

이 명령어는 OAuth2 클라이언트와 액세스 토큰을 저장하기 위해 필요한 데이터베이스 마이그레이션을 퍼블리시하고 실행합니다. 또한 안전한 액세스 토큰 생성을 위한 암호화 키도 생성합니다.

`install:api` 명령어 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가하세요. 이 트레이트는 인증된 사용자의 토큰과 스코프를 검사할 수 있는 몇 가지 헬퍼 메서드를 제공합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

마지막으로, 애플리케이션의 `config/auth.php` 구성 파일에서 `api` 인증 가드를 정의하고 `driver` 옵션을 `passport`로 설정해야 합니다. 이렇게 하면 들어오는 API 요청 인증 시 Passport의 `TokenGuard`을 사용하도록 지시합니다:

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],

    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],
],
```

<a name="deploying-passport"></a>
### Passport 배포하기 (Deploying Passport)

애플리케이션 서버에 처음 Passport를 배포할 때는 보통 `passport:keys` 명령어를 실행해야 합니다. 이 명령어는 액세스 토큰 생성에 필요한 암호화 키를 생성합니다. 생성된 키들은 일반적으로 버전 관리에 포함하지 않습니다:

```shell
php artisan passport:keys
```

필요에 따라 Passport 키를 로드할 경로를 정의할 수 있습니다. 이를 위해 `Passport::loadKeysFrom` 메서드를 사용하세요. 보통 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
}
```

<a name="loading-keys-from-the-environment"></a>
#### 환경 변수에서 키 로드하기 (Loading Keys From the Environment)

또는 `vendor:publish` Artisan 명령어로 Passport의 설정 파일을 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일이 퍼블리시된 후, 애플리케이션의 암호화 키를 환경 변수로 정의해서 로드할 수 있습니다:

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="upgrading-passport"></a>
### Passport 업그레이드 (Upgrading Passport)

새로운 메이저 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 주의 깊게 확인해야 합니다.

<a name="configuration"></a>
## 구성 (Configuration)

<a name="token-lifetimes"></a>
### 토큰 수명 설정 (Token Lifetimes)

기본적으로 Passport는 1년간 유효한 장기 액세스 토큰을 발급합니다. 토큰 수명을 더 길거나 짧게 설정하려면 `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용하세요. 이들은 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드 내에서 호출합니다:

```php
use Carbon\CarbonInterval;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensExpireIn(CarbonInterval::days(15));
    Passport::refreshTokensExpireIn(CarbonInterval::days(30));
    Passport::personalAccessTokensExpireIn(CarbonInterval::months(6));
}
```

> [!WARNING]
> Passport 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며 표시용입니다. 토큰 발급 시 만료 정보는 서명되고 암호화된 토큰 내부에 저장됩니다. 토큰을 무효화하려면 [토큰 폐기하기](#revoking-tokens)를 수행해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 재정의하기 (Overriding Default Models)

Passport 내부에서 사용하는 모델은 자유롭게 확장할 수 있습니다. 자신의 모델을 정의한 후, 해당 Passport 모델을 상속하면 됩니다:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의한 후, `Laravel\Passport\Passport` 클래스를 통해 Passport에 사용자 정의 모델을 사용하도록 지정할 수 있습니다. 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 설정합니다:

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\DeviceCode;
use App\Models\Passport\RefreshToken;
use App\Models\Passport\Token;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::useTokenModel(Token::class);
    Passport::useRefreshTokenModel(RefreshToken::class);
    Passport::useAuthCodeModel(AuthCode::class);
    Passport::useClientModel(Client::class);
    Passport::useDeviceCodeModel(DeviceCode::class);
}
```

<a name="overriding-routes"></a>
### 라우트 재정의하기 (Overriding Routes)

Passport가 정의한 라우트를 커스터마이징하려면, 먼저 `AppServiceProvider`의 `register` 메서드에서 `Passport::ignoreRoutes`를 호출해 Passport가 등록하는 라우트를 무시하도록 해야 합니다:

```php
use Laravel\Passport\Passport;

/**
 * Register any application services.
 */
public function register(): void
{
    Passport::ignoreRoutes();
}
```

그 다음, Passport의 [라우트 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 내용을 애플리케이션의 `routes/web.php`에 복사하여 원하는 대로 수정할 수 있습니다:

```php
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => '\Laravel\Passport\Http\Controllers',
], function () {
    // Passport 라우트들...
});
```

<a name="authorization-code-grant"></a>
## Authorization Code Grant (인가 코드 그랜트)

OAuth2의 인가 코드를 사용하는 방식은 가장 익숙한 OAuth2 인증 방식입니다. 인가 코드 그랜트는 클라이언트 애플리케이션이 사용자를 서버로 리다이렉트하여, 사용자가 해당 클라이언트에게 액세스 토큰 발급을 허용하거나 거부하도록 합니다.

시작하려면, Passport가 인가(authorization) 뷰를 어떻게 반환할지 지정해야 합니다.

인가 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스의 적절한 메서드로 자유롭게 커스터마이징할 수 있습니다. 보통 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 제공하는 경우...
    Passport::authorizationView('auth.oauth.authorize');

    // 클로저를 제공하는 경우...
    Passport::authorizationView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Authorize', [
            'request' => $parameters['request'],
            'authToken' => $parameters['authToken'],
            'client' => $parameters['client'],
            'user' => $parameters['user'],
            'scopes' => $parameters['scopes'],
        ])
    );
}
```

Passport는 자동으로 `/oauth/authorize` 라우트를 정의해 이 뷰를 반환합니다. `auth.oauth.authorize` 템플릿은 `passport.authorizations.approve` 라우트로 POST 요청을 보내 인가를 승인하는 폼과, `passport.authorizations.deny` 라우트로 DELETE 요청을 보내 인가를 거부하는 폼을 포함해야 합니다. 두 라우트 모두 `state`, `client_id`, `auth_token` 필드를 필요로 합니다.

<a name="managing-clients"></a>
### 클라이언트 관리하기 (Managing Clients)

애플리케이션 API와 상호작용하려는 개발자는 자신의 애플리케이션을 등록하기 위해 "클라이언트"를 생성해야 합니다. 보통 클라이언트는 애플리케이션 이름과 사용자가 인가 요청을 승인한 후 리다이렉트할 URI를 제공합니다.

<a name="managing-first-party-clients"></a>
#### 퍼스트 파티 클라이언트 (First-Party Clients)

클라이언트를 가장 쉽게 만드는 방법은 `passport:client` Artisan 명령어를 사용하는 것입니다. 이 명령어는 퍼스트파티 클라이언트 또는 OAuth2 기능 테스트용 클라이언트를 만듭니다. 명령어 실행 시 Passport가 클라이언트 정보(이름, 리다이렉션 URI 등)를 묻고 클라이언트 ID와 시크릿을 제공합니다:

```shell
php artisan passport:client
```

클라이언트가 여러 리다이렉트 URI를 허용하려면, `passport:client` 명령어 실행 시 URI 입력란에 쉼표로 구분된 목록을 지정할 수 있습니다. 쉼표가 포함된 URI는 반드시 URI 인코딩해야 합니다:

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 써드 파티 클라이언트 (Third-Party Clients)

사용자가 `passport:client` 명령어를 직접 사용할 수 없기 때문에, `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드를 사용해 특정 사용자에게 클라이언트를 등록할 수 있습니다:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// 주어진 사용자에게 속한 OAuth 앱 클라이언트 생성...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// 사용자의 모든 OAuth 앱 클라이언트 조회...
$clients = $user->oauthApps()->get();
```

`createAuthorizationCodeGrantClient`는 `Laravel\Passport\Client` 인스턴스를 반환합니다. `$client->id`를 클라이언트 ID로, `$client->plainSecret`을 클라이언트 시크릿으로 사용자에게 보여줄 수 있습니다.

<a name="requesting-tokens"></a>
### 토큰 요청하기 (Requesting Tokens)

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인가 요청으로 리다이렉트하기 (Redirecting for Authorization)

클라이언트가 생성되면, 개발자는 클라이언트 ID와 시크릿을 사용해 인가 코드와 액세스 토큰을 요청할 수 있습니다. 먼저, 클라이언트는 다음과 같이 `/oauth/authorize` 라우트로 리다이렉트 요청을 보내야 합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", 또는 "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

`prompt` 파라미터는 Passport 애플리케이션의 인증 동작 방식을 지정합니다.

- `none`이면, 사용자가 아직 인증되지 않았다면 항상 인증 오류를 발생시킵니다.
- `consent`이면, 이전에 모든 스코프를 승인했더라도 항상 인가 승인 화면이 표시됩니다.
- `login`이면 기존 세션이 있어도 사용자가 다시 로그인하도록 요청합니다.

`prompt`가 지정되지 않으면, 사용자가 이전에 해당 클라이언트를 위해 해당 스코프들에 대한 인가를 하지 않은 경우에만 인가 승인 화면이 표시됩니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 이미 Passport에서 정의되어 있으므로 수동으로 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 인가 승인하기 (Approving the Request)

Passport는 인가 요청을 받을 때 `prompt` 값에 따라 자동으로 처리하며, 사용자에게 인가 승인 또는 거부 화면을 보여줍니다. 사용자가 인가를 승인하면, 클라이언트가 지정했던 `redirect_uri`로 리다이렉트됩니다. `redirect_uri`는 클라이언트 생성시 지정한 리다이렉트 URL과 일치해야 합니다.

퍼스트파티 클라이언트를 인가할 때 인가 승인을 건너뛰고 싶을 수 있습니다. 이 경우 [기본 Client 모델 확장](#overriding-default-models) 후 `skipsAuthorization` 메서드를 정의할 수 있습니다. 이 메서드가 `true`를 반환하면 클라이언트는 자동으로 승인되고, `prompt` 파라미터가 명시적으로 설정되지 않았다면 사용자는 즉시 `redirect_uri`로 리다이렉트됩니다:

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 클라이언트가 인가 승인 프롬프트를 건너뛸지 여부 결정.
     *
     * @param  \Laravel\Passport\Scope[]  $scopes
     */
    public function skipsAuthorization(Authenticatable $user, array $scopes): bool
    {
        return $this->firstParty();
    }
}
```

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
#### 인가 코드를 액세스 토큰으로 변환하기 (Converting Authorization Codes to Access Tokens)

사용자가 인가를 승인하면 클라이언트 애플리케이션은 다시 리다이렉트됩니다. 클라이언트는 리다이렉트 전에 저장해둔 `state` 값과 리다이렉트 쿼리 스트링에 포함된 `state` 값을 비교해 무결성을 검증해야 합니다. 일치하면, 클라이언트는 인가 코드와 함께 액세스 토큰을 요청하는 POST 요청을 서버에 보냅니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class,
        'Invalid state value.'
    );

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'code' => $request->code,
    ]);

    return $response->json();
});
```

`/oauth/token` 라우트는 JSON 형태로 `access_token`, `refresh_token`, `expires_in` 정보를 반환합니다. `expires_in`은 토큰 만료까지 남은 초를 의미합니다.

> [!NOTE]
> `/oauth/token` 라우트 역시 Passport가 미리 정의하므로 별도 선언이 필요 없습니다.

<a name="managing-tokens"></a>
### 토큰 관리하기 (Managing Tokens)

`Laravel\Passport\HasApiTokens` 트레이트의 `tokens` 메서드를 사용해 사용자의 인가된 토큰을 조회할 수 있습니다. 예를 들어, 사용자가 자신의 서드파티 애플리케이션 연결 상태를 확인할 수 있는 대시보드에 활용할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 유효한 토큰만 조회...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// 서드파티 OAuth 앱 클라이언트에 대한 연결 상태 조회...
$connections = $tokens->load('client')
    ->reject(fn (Token $token) => $token->client->firstParty())
    ->groupBy('client_id')
    ->map(fn (Collection $tokens) => [
        'client' => $tokens->first()->client,
        'scopes' => $tokens->pluck('scopes')->flatten()->unique()->values()->all(),
        'tokens_count' => $tokens->count(),
    ])
    ->values();
```

<a name="refreshing-tokens"></a>
### 토큰 갱신하기 (Refreshing Tokens)

만약 짧은 수명의 액세스 토큰을 발급하는 경우, 사용자는 토큰이 만료됐을 때 제공받은 리프레시 토큰을 통해 액세스 토큰을 갱신해야 합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // 클라이언트가 confidential일 때만 필수...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

응답은 `access_token`, `refresh_token`, `expires_in`을 JSON으로 반환합니다.

<a name="revoking-tokens"></a>
### 토큰 폐기하기 (Revoking Tokens)

`Laravel\Passport\Token` 모델의 `revoke` 메서드를 호출하여 토큰을 폐기할 수 있습니다. 토큰에 연결된 리프레시 토큰도 `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드로 폐기할 수 있습니다:

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// 액세스 토큰 폐기...
$token->revoke();

// 관련 리프레시 토큰 폐기...
$token->refreshToken?->revoke();

// 사용자의 모든 토큰 폐기...
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### 토큰 정리하기 (Purging Tokens)

토큰이 폐기되거나 만료되었을 때 데이터베이스에서 정리하고 싶다면, 포함된 `passport:purge` Artisan 명령어를 사용할 수 있습니다:

```shell
# 폐기되거나 만료된 토큰, 인가 코드, 기기 코드 정리...
php artisan passport:purge

# 6시간 이상 만료된 토큰만 정리...
php artisan passport:purge --hours=6

# 폐기된 토큰, 인가 코드, 기기 코드만 정리...
php artisan passport:purge --revoked

# 만료된 토큰, 인가 코드, 기기 코드만 정리...
php artisan passport:purge --expired
```

또한, [스케줄러](/docs/12.x/scheduling)를 설정해 `routes/console.php`에서 주기적으로 토큰을 정리할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## Authorization Code Grant With PKCE (인가 코드 그랜트 - PKCE 사용)

PKCE(proof key for code exchange)를 활용한 인가 코드 그랜트는 싱글 페이지 앱 또는 모바일 앱처럼 클라이언트 시크릿을 안전하게 저장할 수 없는 환경에서 안전하게 토큰을 발급받는 방법입니다. 인가 코드를 액세스 토큰으로 교환할 때 클라이언트 시크릿 대신 "code verifier" 와 "code challenge" 조합을 사용해 보안을 강화합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성하기 (Creating the Client)

애플리케이션이 PKCE 인가 코드 그랜트를 통해 토큰을 발급하려면, PKCE가 활성화된 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령에 `--public` 옵션을 붙여 생성합니다:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청하기 (Requesting Tokens)

<a name="code-verifier-code-challenge"></a>
#### Code Verifier와 Code Challenge

클라이언트 시크릿이 없으므로, `code verifier` 와 `code challenge`를 생성해야 토큰을 요청할 수 있습니다.

`code verifier`는 43 ~ 128자 길이의 랜덤 문자열이며, RFC 7636에 명시된 대로 문자, 숫자, 그리고 `"-"`, `"."`, `"_"`, `"~"` 문자들을 포함할 수 있습니다.

`code challenge`는 SHA256 해시를 Base64 URL 안전한 형태로 인코딩한 문자열입니다. 끝의 `=` 문자는 제거하며, 줄 바꿈, 공백 등 추가 문자가 없어야 합니다:

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 인가 요청으로 리다이렉트하기

클라이언트 생성 후, 클라이언트 ID와 생성한 코드 검증자(verifier)와 도전문(challenge)를 포함하여 인가 코드와 액세스 토큰을 요청합니다. 먼저 다음과 같이 `/oauth/authorize` 라우트로 리다이렉트해야 합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $request->session()->put(
        'code_verifier', $codeVerifier = Str::random(128)
    );

    $codeChallenge = strtr(rtrim(
        base64_encode(hash('sha256', $codeVerifier, true))
    , '='), '+/', '-_');

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
        'state' => $state,
        'code_challenge' => $codeChallenge,
        'code_challenge_method' => 'S256',
        // 'prompt' => '', // "none", "consent", 또는 "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
#### 인가 코드를 액세스 토큰으로 변환하기

사용자가 인가를 승인하면, 클라이언트는 리다이렉트 후 세션에 저장한 `state`와 요청의 `state`를 비교합니다.

`state` 값이 일치하면, 인가 코드와 함께 원래 생성한 `code_verifier`를 포함하여 액세스 토큰을 요청하는 POST 요청을 보냅니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    $codeVerifier = $request->session()->pull('code_verifier');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class
    );

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'code_verifier' => $codeVerifier,
        'code' => $request->code,
    ]);

    return $response->json();
});
```

<a name="device-authorization-grant"></a>
## Device Authorization Grant (기기 인증 그랜트)

OAuth2의 기기 인증 그랜트는 TV, 게임 콘솔 같이 입력이 제한되거나 브라우저가 없는 기기에서 "device code"를 교환해 액세스 토큰을 얻는 방법입니다. 이 방식에서는 기기가 사용자가 별도의 컴퓨터나 스마트폰을 사용해 서버에 접속하여 받은 "user code"를 입력하고 인가 요청을 승인하거나 거부하도록 유도합니다.

시작하려면, Passport가 "user code"와 "authorization" 뷰를 반환하도록 지정해야 합니다.

인가 뷰 렌더링은 `Laravel\Passport\Passport` 클래스의 관련 메서드로 커스터마이징할 수 있습니다. 보통 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 호출합니다:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 지정하는 경우...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // 클로저를 지정하는 경우...
    Passport::deviceUserCodeView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Device/UserCode')
    );

    Passport::deviceAuthorizationView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Device/Authorize', [
            'request' => $parameters['request'],
            'authToken' => $parameters['authToken'],
            'client' => $parameters['client'],
            'user' => $parameters['user'],
            'scopes' => $parameters['scopes'],
        ])
    );

    // ...
}
```

Passport는 자동으로 해당 뷰를 반환하는 라우트를 정의합니다. `auth.oauth.device.user-code` 템플릿은 `passport.device.authorizations.authorize` 라우트로 GET 요청을 보내는 폼을 포함해야 하며, 이 라우트는 `user_code` 쿼리 파라미터를 기대합니다.

`auth.oauth.device.authorize` 템플릿은 인가 승인용 POST 요청을 `passport.device.authorizations.approve` 라우트로, 인가 거부용 DELETE 요청을 `passport.device.authorizations.deny` 라우트로 보내는 폼을 포함해야 합니다. 두 라우트는 `state`, `client_id`, `auth_token` 필드를 필요로 합니다.

<a name="creating-a-device-authorization-grant-client"></a>
### 기기 인증 그랜트 클라이언트 생성하기 (Creating a Device Authorization Grant Client)

애플리케이션이 기기 인증 그랜트를 사용해 토큰을 발급하려면, `passport:client` Artisan 명령어에 `--device` 옵션을 붙여 기기 플로우가 활성화된 퍼스트파티 클라이언트를 생성해야 합니다. 이 명령어는 클라이언트 ID와 시크릿을 알려줍니다:

```shell
php artisan passport:client --device
```

또한, 써드파티 클라이언트를 등록하려면 `ClientRepository` 클래스의 `createDeviceAuthorizationGrantClient` 메서드를 사용하여 특정 사용자에게 클라이언트를 생성할 수 있습니다:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

$client = app(ClientRepository::class)->createDeviceAuthorizationGrantClient(
    user: $user,
    name: 'Example Device',
    confidential: false,
);
```

<a name="requesting-device-authorization-grant-tokens"></a>
### 토큰 요청하기 (Requesting Tokens)

<a name="device-code"></a>
#### Device Code 요청하기

클라이언트가 생성되고 나면, 개발자는 클라이언트 ID를 사용해 기기 코드(device code)를 요청할 수 있습니다. 먼저, 클라이언트가 `/oauth/device/code` 라우트에 POST 요청을 보내 기기 코드를 받아야 합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

응답에는 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 정보가 담긴 JSON이 반환됩니다. `expires_in`은 기기 코드 만료까지 남은 초이며, `interval`은 클라이언트가 `/oauth/token` 경로를 폴링할 때 최소 대기 시간을 초 단위로 의미합니다. 폴링 간격을 줄이면 속도 제한 에러가 발생할 수 있습니다.

> [!NOTE]
> `/oauth/device/code` 라우트는 이미 Passport가 정의하므로 수동 선언하지 않아도 됩니다.

<a name="user-code"></a>
#### 검증 URI 및 사용자 코드 표시하기

기기 코드 요청에 성공하면, 클라이언트는 사용자에게 별도의 장치로 `verification_uri`에 접속해 `user_code`를 입력하여 인가 요청을 승인하거나 거부하도록 안내해야 합니다.

<a name="polling-token-request"></a>
#### 토큰 요청 폴링하기

사용자는 별도의 장치에서 인가를 승인/거부하므로, 기기 클라이언트는 `/oauth/token` 라우트를 일정 간격(`interval`)으로 폴링해서 사용자의 응답이 완료됐는지 확인해야 합니다. 폴링 시 `interval` 간격을 준수하지 않으면 속도 제한 오류가 발생하니 주의해야 합니다:

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // confidential 클라이언트 일 때만 필요...
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

사용자가 승인하면, JSON 응답으로 `access_token`, `refresh_token`, `expires_in`이 반환됩니다.

<a name="password-grant"></a>
## Password Grant (비밀번호 그랜트)

> [!WARNING]
> 비밀번호 그랜트는 더 이상 권장되지 않습니다. OAuth2 서버에서 현재 권장하는 [다른 그랜트 종류](https://oauth2.thephpleague.com/authorization-server/which-grant/)를 사용하는 것이 좋습니다.

Password grant는 모바일 앱 등 퍼스트파티 클라이언트가 이메일/사용자명과 비밀번호를 이용해 액세스 토큰을 받을 수 있게 합니다. 이 방식은 사용자가 모든 OAuth2 인가 코드 리디렉션 플로우를 거치지 않아도 되도록 안전하게 액세스 토큰을 발급받을 수 있게 해줍니다.

비밀번호 그랜트를 활성화하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enablePasswordGrant` 메서드를 호출합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enablePasswordGrant();
}
```

<a name="creating-a-password-grant-client"></a>
### Password Grant 클라이언트 생성하기 (Creating a Password Grant Client)

비밀번호 그랜트를 사용하려면 `passport:client` Artisan 명령의 `--password` 옵션으로 비밀번호 그랜트 클라이언트를 먼저 생성해야 합니다:

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청하기 (Requesting Tokens)

비밀번호 그랜트를 활성화하고 클라이언트를 만들면, 사용자 이메일과 비밀번호를 포함한 POST 요청으로 `/oauth/token` 경로에 액세스 토큰을 요청할 수 있습니다. 이 경로는 Passport가 미리 등록하므로 별도 정의할 필요가 없습니다. 요청이 성공하면 `access_token`과 `refresh_token`을 JSON으로 받습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // confidential 클라이언트만 필수...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

> [!NOTE]
> 액세스 토큰은 기본적으로 장기 토큰입니다. 필요에 따라 [최대 액세스 토큰 수명](#configuration)을 조절할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청하기 (Requesting All Scopes)

Password grant나 클라이언트 자격 증명 그랜트를 사용할 때, 애플리케이션이 지원하는 모든 스코프에 대해 토큰에 권한을 줄 수 있습니다. 이 경우 `*` 스코프를 요청하세요. 이 경우 토큰의 `can` 메서드는 항상 `true`를 반환합니다. `*` 스코프는 `password` 또는 `client_credentials` 그랜트에서만 토큰에 할당할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // confidential 클라이언트만 필수...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### 사용자 프로바이더 커스터마이징 (Customizing the User Provider)

애플리케이션이 여러 개의 [인증 사용자 프로바이더](/docs/12.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --password` 명령을 실행할 때 `--provider` 옵션으로 어떤 프로바이더를 사용할지 지정할 수 있습니다. 주어진 프로바이더 이름은 애플리케이션 `config/auth.php`에 정의된 프로바이더와 일치해야 합니다. 이후 [미들웨어를 이용해 적절한 가드로 라우트를 보호](#multiple-authentication-guards)할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명 필드 커스터마이징 (Customizing the Username Field)

비밀번호 그랜트 인증 시 Passport는 `email` 속성을 "사용자명"으로 사용하지만, `findForPassport` 메서드를 모델에 정의해 바꿀 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * 주어진 사용자명에 해당하는 사용자 인스턴스 찾기.
     */
    public function findForPassport(string $username): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### 비밀번호 검증 커스터마이징 (Customizing the Password Validation)

비밀번호 그랜트 인증 시 Passport는 모델의 `password` 속성을 이용해 비밀번호를 검증합니다. 만약 모델에 `password` 속성이 없거나 검증 로직을 바꾸고 싶으면, 모델에 `validateForPassportPasswordGrant` 메서드를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Support\Facades\Hash;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Passport 비밀번호 그랜트용 비밀번호 검증.
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant"></a>
## Implicit Grant (암묵적 그랜트)

> [!WARNING]
> 암묵적 그랜트는 더 이상 권장되지 않습니다. [OAuth2 서버가 권장하는 다른 그랜트](https://oauth2.thephpleague.com/authorization-server/which-grant/)를 선택하세요.

암묵적 그랜트는 인가 코드 획득과정 없이 토큰을 클라이언트에 직접 반환하는 방식입니다. 주로 클라이언트 시크릿을 안전하게 저장하기 어려운 JavaScript나 모바일 앱에서 사용합니다. 활성화하려면 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 `enableImplicitGrant`를 호출하세요:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

암묵적 그랜트를 사용하려면 먼저 `passport:client` Artisan 명령어에 `--implicit` 옵션을 주어 클라이언트를 만들어야 합니다:

```shell
php artisan passport:client --implicit
```

활성화하고 클라이언트를 만들면, 개발자는 클라이언트 ID를 이용해 `/oauth/authorize` 라우트로 리다이렉트해 액세스 토큰을 요청할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'token',
        'scope' => 'user:read orders:create',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", 또는 "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

> [!NOTE]
> `/oauth/authorize` 라우트는 Passport가 미리 정의합니다. 별도 정의 불필요합니다.

<a name="client-credentials-grant"></a>
## Client Credentials Grant (클라이언트 자격 증명 그랜트)

클라이언트 자격 증명 그랜트는 머신 간 인증용입니다. 예를 들어, API 유지보수 작업을 수행하는 예약된 작업에 적합합니다.

클라이언트 자격 증명 그랜트를 사용하려면 `passport:client` Artisan 명령어에 `--client` 옵션을 사용해 클라이언트를 생성합니다:

```shell
php artisan passport:client --client
```

그런 뒤, 라우트에 `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 할당하세요:

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하고, 클라이언트가 리소스 소유자인 경우...
})->middleware(EnsureClientIsResourceOwner::class);
```

특정 스코프 제한을 위해선 `using` 메서드에 스코프 목록을 전달할 수 있습니다:

```php
Route::get('/orders', function (Request $request) {
    // 토큰이 유효하고 리소스 소유자이며 "servers:read" 와 "servers:create" 스코프도 갖고 있을 때...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create'));
```

<a name="retrieving-tokens"></a>
### 토큰 조회하기

이 그랜트 타입으로 토큰을 요청하려면 `oauth/token` 엔드포인트에 다음과 같이 요청하세요:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'client_credentials',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret',
    'scope' => 'servers:read servers:create',
]);

return $response->json()['access_token'];
```

<a name="personal-access-tokens"></a>
## Personal Access Tokens (개인 액세스 토큰)

사용자가 전형적인 인가 코드 플로우 없이 스스로 액세스 토큰을 발급받고 싶을 때가 있습니다. 애플리케이션 UI에서 직접 토큰 발급을 허용하면, API를 실험하거나 단순히 액세스 토큰을 발급하는 간편한 방법이 될 수 있습니다.

> [!NOTE]
> 애플리케이션에서 주로 개인 액세스 토큰 발급용으로 Passport를 사용한다면, 라라벨의 가벼운 API 토큰 발급 라이브러리인 [Laravel Sanctum]을 사용하는 것을 고려하세요.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성하기

개인 액세스 토큰을 발급하려면 `passport:client` Artisan 명령어에 `--personal` 옵션을 붙여 개인 액세스 클라이언트를 생성해야 합니다. 이미 `passport:install` 명령을 실행했다면 이 명령은 불필요합니다:

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### 사용자 프로바이더 커스터마이징 (Customizing the User Provider)

애플리케이션이 여러 개의 [인증 사용자 프로바이더](/docs/12.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --personal` 명령 실행 시 `--provider` 옵션을 제공하여 어떤 프로바이더를 개인 액세스 클라이언트에 사용할지 지정할 수 있습니다. 지정한 프로바이더 이름은 `config/auth.php`에 정의된 유효한 프로바이더여야 합니다. 이후 [미들웨어를 이용해 라우트를 보호](#multiple-authentication-guards)할 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리하기

개인 액세스 클라이언트를 생성한 후, 특정 사용자에 대해 `App\Models\User` 모델 인스턴스의 `createToken` 메서드로 토큰을 발급할 수 있습니다. `createToken`의 첫 번째 인자는 토큰 이름, 두 번째 인자는 선택적 스코프 배열입니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 스코프 없는 토큰 생성...
$token = $user->createToken('My Token')->accessToken;

// 스코프가 포함된 토큰 생성...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// 모든 스코프 포함 토큰 생성...
$token = $user->createToken('My Token', ['*'])->accessToken;

// 유효한 개인 액세스 토큰 모두 조회...
$tokens = $user->tokens()
    ->with('client')
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get()
    ->filter(fn (Token $token) => $token->client->hasGrantType('personal_access'));
```

<a name="protecting-routes"></a>
## 라우트 보호하기 (Protecting Routes)

<a name="via-middleware"></a>
### 미들웨어를 통해 (Via Middleware)

Passport는 유효한 액세스 토큰을 검증하는 [인증 가드](/docs/12.x/authentication#adding-custom-guards)를 제공합니다. `api` 가드를 `passport` 드라이버로 설정한 후, 보호할 라우트에 `auth:api` 미들웨어를 적용하세요:

```php
Route::get('/user', function () {
    // API 인증된 사용자만 접근 가능...
})->middleware('auth:api');
```

> [!WARNING]
> 만약 [클라이언트 자격 증명 그랜트](#client-credentials-grant)를 사용하는 경우, `auth:api` 대신 [EnsureClientIsResourceOwner 미들웨어](#client-credentials-grant)를 사용해 라우트를 보호해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 여러 인증 가드 (Multiple Authentication Guards)

서로 다른 Eloquent 모델을 사용하는 복수 타입 사용자 인증이 필요한 경우, 각 사용자 프로바이더에 맞는 인증 가드를 `config/auth.php`에 정의해야 합니다. 이를 통해 특정 프로바이더용 요청을 보호할 수 있습니다. 예시:

```php
'guards' => [
    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],

    'api-customers' => [
        'driver' => 'passport',
        'provider' => 'customers',
    ],
],
```

이 경우, 다음 라우트는 `customers` 프로바이더를 사용하는 `api-customers` 가드를 사용해 요청을 인증합니다:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport에서 다중 사용자 프로바이더를 사용하는 자세한 내용은 [개인 액세스 토큰 문서](#customizing-the-user-provider-for-pat)와 [비밀번호 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달하기 (Passing the Access Token)

Passport로 보호된 라우트에 접근할 때, API 소비자는 요청의 `Authorization` 헤더에 `Bearer` 토큰 형태로 액세스 토큰을 지정해야 합니다. 예를 들어 `Http` 팩사드를 사용할 때:

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => "Bearer $accessToken",
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
## 토큰 스코프 (Token Scopes)

스코프는 API 클라이언트가 특정 권한 집합만 요청하도록 허용합니다. 예를 들어, 이커머스 앱에서는 모든 API 소비자가 주문 기능을 수행할 필요가 없으며, 대신 주문 상태 조회 권한만 부여할 수 있습니다. 스코프는 제3자 애플리케이션이 사용자 대리로 수행할 작업을 사용자가 제한할 수 있게 합니다.

<a name="defining-scopes"></a>
### 스코프 정의하기 (Defining Scopes)

스코프는 `Passport::tokensCan` 메서드를 이용해 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의할 수 있습니다. 이 메서드는 스코프 이름과 설명을 받고, 스코프 설명은 인가 승인 화면에 표시됩니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensCan([
        'user:read' => '사용자 정보 조회',
        'orders:create' => '주문 생성',
        'orders:read:status' => '주문 상태 확인',
    ]);
}
```

<a name="default-scope"></a>
### 기본 스코프 (Default Scope)

클라이언트가 특정 스코프를 요청하지 않으면, Passport 서버가 토큰에 기본 스코프를 할당하도록 `defaultScopes` 메서드를 사용해 설정할 수 있습니다. 이 역시 보통 `boot` 메서드에서 호출합니다:

```php
use Laravel\Passport\Passport;

Passport::tokensCan([
    'user:read' => '사용자 정보 조회',
    'orders:create' => '주문 생성',
    'orders:read:status' => '주문 상태 확인',
]);

Passport::defaultScopes([
    'user:read',
    'orders:create',
]);
```

<a name="assigning-scopes-to-tokens"></a>
### 토큰에 스코프 할당하기 (Assigning Scopes to Tokens)

<a name="when-requesting-authorization-codes"></a>
#### 인가 코드 요청 시 스코프 지정하기

인가 코드 그랜트에서 액세스 토큰 요청 시, 클라이언트는 `scope` 쿼리 파라미터로 원하는 스코프를 공백으로 구분해 지정해야 합니다:

```php
Route::get('/redirect', function () {
    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="when-issuing-personal-access-tokens"></a>
#### 개인 액세스 토큰 발급 시 스코프 지정하기

`App\Models\User` 모델의 `createToken` 메서드를 사용해 개인 액세스 토큰을 발급할 때, 두 번째 인자로 스코프 배열을 전달할 수 있습니다:

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 체크하기 (Checking Scopes)

Passport는 미들웨어 두 가지를 제공해, 들어오는 요청 토큰에 특정 스코프가 부여됐는지 검증할 수 있습니다.

<a name="check-for-all-scopes"></a>
#### 모든 스코프 검증하기

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어를 라우트에 지정하면, 들어오는 요청 토큰이 나열된 모든 스코프를 갖고 있는지 확인합니다:

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // 액세스 토큰이 "orders:read"와 "orders:create" 두 스코프 모두를 가진 경우...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create')]);
```

<a name="check-for-any-scopes"></a>
#### 일부 스코프 검증하기

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어는 나열된 스코프 중 적어도 하나라도 토큰에 포함됐는지 확인합니다:

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // 액세스 토큰이 "orders:read" 또는 "orders:create" 스코프 중 하나 이상을 가진 경우...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create')]);
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 체크하기

액세스 토큰이 인증된 상태의 애플리케이션 내에서, 현재 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드를 이용해 특정 스코프를 체크할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('orders:create')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
#### 추가 스코프 메서드

- `scopeIds` 메서드는 정의된 모든 스코프 ID(또는 이름) 배열을 반환합니다:

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

- `scopes` 메서드는 `Laravel\Passport\Scope` 인스턴스로 된 모든 스코프 배열을 반환합니다:

```php
Passport::scopes();
```

- `scopesFor` 메서드는 주어진 ID 배열에 대응하는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다:

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

- `hasScope` 메서드는 특정 스코프가 정의됐는지 여부를 반환합니다:

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

API를 구축할 때, 자바스크립트 애플리케이션에서 직접 API를 사용하면 매우 편리합니다. 이렇게 하면, 동일한 API를 웹, 모바일, 서드파티 애플리케이션, SDK 등이 공유하며 사용하게 됩니다.

통상, JavaScript 앱에서 API 호출 시 액세스 토큰을 수동으로 전달해야 합니다. 하지만 Passport는 이를 대신해주는 미들웨어를 제공하며, `bootstrap/app.php` 파일 내 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어를 추가하기만 하면 됩니다:

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어가 미들웨어 스택에서 가장 마지막에 위치하도록 해야 합니다.

이 미들웨어는 응답에 암호화된 JWT를 담은 `laravel_token` 쿠키를 첨부합니다. Passport는 이 쿠키를 사용해 자바스크립트 앱의 API 요청 인증을 처리합니다. JWT 수명은 `session.lifetime` 구성값과 같습니다. 브라우저가 쿠키를 자동으로 보내므로 액세스 토큰을 명시적으로 전달할 필요 없이 API 요청이 가능합니다:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이징

필요시 `Passport::cookie` 메서드를 사용해 `laravel_token` 쿠키의 이름을 변경할 수 있습니다. 보통 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::cookie('custom_name');
}
```

<a name="csrf-protection"></a>
#### CSRF 보호

이 인증 방식을 사용할 때, 유효한 CSRF 토큰 헤더가 요청에 포함돼야 합니다. 기본 Laravel JavaScript 스켈레톤과 스타터 키트들은 [Axios](https://github.com/axios/axios)를 포함하며, 같은 출처 요청에 대해 암호화된 `XSRF-TOKEN` 쿠키 값을 읽어 `X-XSRF-TOKEN` 헤더를 자동으로 설정합니다.

> [!NOTE]
> 만약 `X-CSRF-TOKEN` 헤더를 사용하려면, `csrf_token()` 함수가 제공하는 암호화되지 않은 토큰을 사용해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

Passport는 액세스 토큰과 리프레시 토큰이 발급되거나 폐기될 때 이벤트를 발생시킵니다. [이벤트 리스닝](/docs/12.x/events)을 이용해 데이터베이스 내 다른 토큰들을 정리하거나 폐기할 수 있습니다:

| 이벤트명                                       |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

<a name="testing"></a>
## 테스트 (Testing)

Passport의 `actingAs` 메서드를 사용하면 현재 인증된 사용자 및 부여할 스코프를 지정할 수 있습니다. `actingAs` 메서드 첫 번째 인자는 사용자 인스턴스이고, 두 번째 인자는 부여할 스코프 배열입니다:

```php tab=Pest
use App\Models\User;
use Laravel\Passport\Passport;

test('orders can be created', function () {
    Passport::actingAs(
        User::factory()->create(),
        ['orders:create']
    );

    $response = $this->post('/api/orders');

    $response->assertStatus(201);
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Passport\Passport;

public function test_orders_can_be_created(): void
{
    Passport::actingAs(
        User::factory()->create(),
        ['orders:create']
    );

    $response = $this->post('/api/orders');

    $response->assertStatus(201);
}
```

`actingAsClient` 메서드를 사용하면 현재 인증된 클라이언트와 부여할 스코프를 지정할 수 있습니다. 인자는 사용자와 동일하게 첫 번째는 클라이언트 인스턴스, 두 번째는 스코프 배열입니다:

```php tab=Pest
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

test('servers can be retrieved', function () {
    Passport::actingAsClient(
        Client::factory()->create(),
        ['servers:read']
    );

    $response = $this->get('/api/servers');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

public function test_servers_can_be_retrieved(): void
{
    Passport::actingAsClient(
        Client::factory()->create(),
        ['servers:read']
    );

    $response = $this->get('/api/servers');

    $response->assertStatus(200);
}
```