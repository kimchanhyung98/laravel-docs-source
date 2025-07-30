# Laravel Passport

- [소개](#introduction)
    - [Passport 또는 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포](#deploying-passport)
    - [Passport 업그레이드](#upgrading-passport)
- [구성](#configuration)
    - [토큰 유효 기간](#token-lifetimes)
    - [기본 모델 재정의](#overriding-default-models)
    - [라우트 재정의](#overriding-routes)
- [Authorization Code Grant (인가 코드 그랜트)](#authorization-code-grant)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청](#requesting-tokens)
    - [토큰 관리](#managing-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [Authorization Code Grant 와 PKCE](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청](#requesting-auth-pkce-grant-tokens)
- [Device Authorization Grant (기기 인가 그랜트)](#device-authorization-grant)
    - [기기 코드 그랜트 클라이언트 생성](#creating-a-device-authorization-grant-client)
    - [토큰 요청](#requesting-device-authorization-grant-tokens)
- [Password Grant (비밀번호 그랜트)](#password-grant)
    - [비밀번호 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [사용자 제공자 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 커스터마이징](#customizing-the-password-validation)
- [Implicit Grant (암묵적 그랜트)](#implicit-grant)
- [Client Credentials Grant (클라이언트 자격 증명 그랜트)](#client-credentials-grant)
- [Personal Access Tokens (개인 액세스 토큰)](#personal-access-tokens)
    - [개인 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [사용자 제공자 커스터마이징](#customizing-the-user-provider-for-pat)
    - [개인 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호](#protecting-routes)
    - [미들웨어 방식](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당](#assigning-scopes-to-tokens)
    - [스코프 검사](#checking-scopes)
- [SPA 인증](#spa-authentication)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Passport](https://github.com/laravel/passport)는 Laravel 애플리케이션에 대해 몇 분 만에 완전한 OAuth2 서버 구현을 제공합니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server)를 기반으로 구축되었습니다.

> [!NOTE]
> 이 문서는 이미 OAuth2에 익숙하다는 것을 전제로 합니다. OAuth2에 대해 전혀 모르는 경우, 계속 진행하기 전에 [일반 용어](https://oauth2.thephpleague.com/terminology/)와 OAuth2의 기능을 숙지하는 것을 권장합니다.

<a name="passport-or-sanctum"></a>
### Passport 또는 Sanctum? (Passport or Sanctum?)

시작하기 전에, 애플리케이션에 Laravel Passport 또는 [Laravel Sanctum](/docs/12.x/sanctum) 중 무엇이 적합한지 결정할 필요가 있습니다. 애플리케이션이 OAuth2를 반드시 지원해야 한다면 Laravel Passport를 사용해야 합니다.

하지만 싱글 페이지 애플리케이션, 모바일 애플리케이션을 인증하거나 API 토큰을 발급하려는 경우에는 [Laravel Sanctum](/docs/12.x/sanctum)을 사용하는 것이 좋습니다. Laravel Sanctum은 OAuth2를 지원하지 않지만, 훨씬 간단한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치 (Installation)

Laravel Passport는 `install:api` Artisan 명령어로 설치할 수 있습니다:

```shell
php artisan install:api --passport
```

이 명령어는 OAuth2 클라이언트 및 액세스 토큰을 저장하는 데 필요한 데이터베이스 마이그레이션을 게시 및 실행하며, 안전한 액세스 토큰 생성을 위한 암호화 키도 생성합니다.

`install:api` 명령어를 실행한 후에는 `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가하세요. 이 트레이트는 인증된 사용자의 토큰과 스코프를 검사할 수 있는 몇 가지 도우미 메서드를 제공합니다:

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

마지막으로, 애플리케이션의 `config/auth.php` 구성 파일에서 `api` 인증 가드를 정의하고, `driver` 옵션을 `passport`로 설정하세요. 이렇게 하면 들어오는 API 요청 인증 시 Passport의 `TokenGuard`가 사용됩니다:

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
### Passport 배포 (Deploying Passport)

애플리케이션 서버에 처음 Passport를 배포할 때는 `passport:keys` 명령어를 실행해야 할 수 있습니다. 이 명령어는 액세스 토큰 생성에 필요한 암호화 키를 생성합니다. 생성된 키는 일반적으로 소스 관리에 포함하지 않습니다.

```shell
php artisan passport:keys
```

필요한 경우 Passport 암호화 키를 로드할 경로를 정의할 수 있습니다. `Passport::loadKeysFrom` 메서드를 사용하세요. 보통 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다:

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
#### 환경 변수에서 키 로드 (Loading Keys From the Environment)

또한, `vendor:publish` Artisan 명령어로 Passport 구성 파일을 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

구성 파일이 게시된 후에는 환경 변수로 암호화 키를 정의하여 애플리케이션에 암호화 키를 로드할 수 있습니다:

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

Passport의 새로운 메이저 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

<a name="configuration"></a>
## 구성 (Configuration)

<a name="token-lifetimes"></a>
### 토큰 유효 기간 (Token Lifetimes)

기본적으로 Passport는 만료 기간이 1년인 장기 액세스 토큰을 발급합니다. 토큰의 유효 기간을 더 길게 혹은 짧게 설정하고 싶다면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용하세요. 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다:

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
> Passport 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며 표시 용도로만 사용됩니다. 실제 토큰 발급 시 만료 정보는 서명되고 암호화된 토큰 안에 저장됩니다. 토큰을 무효화하려면 [토큰을 폐기](#revoking-tokens)해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 재정의 (Overriding Default Models)

Passport가 내부적으로 사용하는 모델을 자유롭게 확장할 수 있습니다. 직접 모델을 정의하고 적절한 Passport 모델을 확장하세요:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의한 후에는 `Laravel\Passport\Passport` 클래스를 통해 Passport가 사용자 정의 모델을 사용하도록 설정할 수 있습니다. 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 설정합니다:

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
### 라우트 재정의 (Overriding Routes)

Passport가 정의한 라우트를 커스터마이징하고 싶으면, 우선 Passport가 등록한 라우트를 무시하도록 `AppServiceProvider` 클래스의 `register` 메서드에 `Passport::ignoreRoutes`를 추가하세요:

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

그 후 [Passport 라우트 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 복사해서 애플리케이션의 `routes/web.php` 파일에 붙여넣고 원하는 대로 수정할 수 있습니다:

```php
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => '\Laravel\Passport\Http\Controllers',
], function () {
    // Passport 라우트...
});
```

<a name="authorization-code-grant"></a>
## Authorization Code Grant (인가 코드 그랜트)

OAuth2를 인가 코드 방식으로 사용하는 것은 일반적인 방식입니다. 인가 코드를 사용할 때 클라이언트 애플리케이션은 사용자를 서버로 리디렉션하며, 사용자는 접근 토큰 발급 요청을 승인하거나 거부합니다.

시작하려면, Passport에 "authorization" 뷰를 반환하는 방법을 알려야 합니다.

이 인가 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스를 통해 적절한 메서드로 모두 커스터마이징할 수 있습니다. 보통 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름 제공하기...
    Passport::authorizationView('auth.oauth.authorize');

    // 클로저 제공하기...
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

Passport는 `/oauth/authorize` 라우트를 자동으로 정의하여 이 뷰를 반환합니다. `auth.oauth.authorize` 템플릿은 `passport.authorizations.approve` 경로로 POST 요청하는 승인 폼과 `passport.authorizations.deny` 경로로 DELETE 요청하는 거부 폼을 포함해야 합니다. 이 경로들은 `state`, `client_id`, `auth_token` 필드를 기대합니다.

<a name="managing-clients"></a>
### 클라이언트 관리 (Managing Clients)

개발자가 애플리케이션 API와 상호작용하려면 자신의 애플리케이션을 "클라이언트"로 등록해야 합니다. 보통 이것은 애플리케이션 이름과 사용자가 인가를 승인한 후 리디렉션할 URI를 제공하는 것을 의미합니다.

<a name="managing-first-party-clients"></a>
#### 퍼스트파티 클라이언트 (First-Party Clients)

가장 간단한 클라이언트 생성 방법은 `passport:client` Artisan 명령어를 사용하는 것입니다. 이 명령은 퍼스트파티 클라이언트 또는 OAuth2 기능 테스트용으로도 사용됩니다. 명령어를 실행하면 Passport가 클라이언트 정보를 묻고, 클라이언트 ID와 비밀 키를 제공합니다:

```shell
php artisan passport:client
```

여러 리디렉션 URI를 허용하려면, `passport:client` 명령어에서 URI를 입력할 때 콤마로 구분된 목록을 지정할 수 있습니다. URI에 콤마가 포함된 경우 URI 인코딩해야 합니다:

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 서드파티 클라이언트 (Third-Party Clients)

사용자가 `passport:client` 명령어를 직접 사용할 수 없으므로, `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드로 주어진 사용자에게 클라이언트를 등록할 수 있습니다:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// 주어진 사용자에 속하는 OAuth 앱 클라이언트 생성...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// 사용자가 소유한 모든 OAuth 앱 클라이언트 조회...
$clients = $user->oauthApps()->get();
```

`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. 이때 `$client->id`는 클라이언트 ID, `$client->plainSecret`은 클라이언트 비밀 키로 사용자에게 보여줄 수 있습니다.

<a name="requesting-tokens"></a>
### 토큰 요청 (Requesting Tokens)

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인가를 위한 리디렉션 (Redirecting for Authorization)

클라이언트가 생성된 후, 개발자는 클라이언트 ID와 비밀 키를 사용하여 인가 코드와 액세스 토큰을 요청할 수 있습니다. 먼저 소비 앱은 애플리케이션의 `/oauth/authorize` 경로로 리디렉션 요청을 합니다:

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

`prompt` 파라미터로 Passport 애플리케이션의 인증 동작 방식을 지정할 수 있습니다.

`prompt` 값이 `none`이면, 사용자가 이미 인증되어 있지 않으면 항상 인증 오류가 발생합니다. `consent` 값이면, 모든 스코프에 대해 이전에 허용했더라도 항상 인가 승인 화면이 표시됩니다. `login`이면, 이미 세션이 있더라도 항상 재로그인하도록 사용자에게 요청합니다.

`prompt`가 주어지지 않으면, 요청된 스코프에 대해 이전에 승인한 적이 없을 때만 인가 창이 표시됩니다.

> [!NOTE]
> `/oauth/authorize` 경로는 Passport에 의해 이미 정의되어 있으므로 직접 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 요청 승인 (Approving the Request)

Passport는 인가 요청을 받을 때 `prompt` 파라미터 값에 따라 자동 응답하며, 사용자가 인가 요청을 승인 또는 거부할 수 있는 템플릿을 표시합니다. 사용자가 요청을 승인하면, 소비 애플리케이션이 지정한 `redirect_uri`로 리디렉션됩니다. `redirect_uri`는 클라이언트 생성 시 지정한 URL과 일치해야 합니다.

퍼스트파티 클라이언트를 인가 시 인가 창을 건너뛰려면, [커스텀 `Client` 모델](#overriding-default-models)을 확장하고 `skipsAuthorization` 메서드를 정의하세요. `skipsAuthorization`이 `true`를 반환하면, `prompt` 파라미터가 명시적으로 지정되지 않은 한 즉시 승인되고 리디렉션됩니다:

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 클라이언트가 인가 프롬프트를 건너뛸지 결정합니다.
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
#### 인가 코드를 액세스 토큰으로 변환 (Converting Authorization Codes to Access Tokens)

사용자가 인가 요청을 승인하면 소비 애플리케이션으로 리디렉션됩니다. 소비자는 리디렉션 전 저장했던 `state` 파라미터 값을 확인하여 일치하면, 다음과 같이 `POST` 요청을 보내 액세스 토큰을 요청해야 합니다. 요청에는 인가 승인 시 발급된 인가 코드를 포함해야 합니다:

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

`/oauth/token` 경로는 JSON 응답으로 `access_token`, `refresh_token`, `expires_in` 속성을 반환합니다. `expires_in`은 액세스 토큰 만료까지 남은 초 단위 시간을 나타냅니다.

> [!NOTE]
> `/oauth/token` 경로 역시 Passport에 의해 자동으로 정의되므로 직접 정의할 필요가 없습니다.

<a name="managing-tokens"></a>
### 토큰 관리 (Managing Tokens)

`Laravel\Passport\HasApiTokens` 트레이트의 `tokens` 메서드로 사용자에게 발급된 토큰을 조회할 수 있습니다. 이를 활용해 사용자가 자신의 서드파티 앱과의 연결 상태를 확인하는 대시보드를 만들 수 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 유효한 유저 토큰을 모두 조회...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// 서드파티 OAuth 앱 클라이언트와의 모든 연결 조회...
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
### 토큰 갱신 (Refreshing Tokens)

애플리케이션에서 단기 유효 토큰을 발급하는 경우, 사용자가 액세스 토큰 만료 시 토큰 발급 시 함께 제공된 리프레시 토큰으로 갱신해야 합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // 기밀 클라이언트에만 필요...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

응답은 `access_token`, `refresh_token`, `expires_in` 속성을 포함하는 JSON입니다.

<a name="revoking-tokens"></a>
### 토큰 폐기 (Revoking Tokens)

토큰은 `Laravel\Passport\Token` 모델의 `revoke` 메서드로 폐기할 수 있습니다. 해당 토큰의 리프레시 토큰도 `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드로 폐기할 수 있습니다:

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// 액세스 토큰 폐기...
$token->revoke();

// 토큰의 리프레시 토큰 폐기...
$token->refreshToken?->revoke();

// 사용자의 모든 토큰 폐기...
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### 토큰 정리 (Purging Tokens)

폐기되었거나 만료된 토큰을 데이터베이스에서 정리하려면 Passport에 포함된 `passport:purge` Artisan 명령어를 사용할 수 있습니다:

```shell
# 폐기 및 만료된 토큰, 인가 코드, 디바이스 코드 정리...
php artisan passport:purge

# 만료된 지 6시간 이상인 토큰만 정리...
php artisan passport:purge --hours=6

# 폐기된 토큰, 인가 코드, 디바이스 코드만 정리...
php artisan passport:purge --revoked

# 만료된 토큰, 인가 코드, 디바이스 코드만 정리...
php artisan passport:purge --expired
```

또한, 애플리케이션의 `routes/console.php`에 [스케줄링된 작업](/docs/12.x/scheduling)을 설정하여 정기적으로 토큰을 정리할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## Authorization Code Grant 와 PKCE

Authorization Code Grant와 "Proof Key for Code Exchange" (PKCE)는 싱글 페이지 앱 또는 모바일 앱을 안전하게 인증하는 방법입니다. 클라이언트 비밀 키를 안전하게 저장할 수 없거나, 공격자가 인가 코드를 가로채는 위협을 완화하기 위해 사용합니다. 인가 코드를 액세스 토큰으로 교환할 때 클라이언트 비밀 키 대신 "코드 검증자(code verifier)"와 "코드 챌린지(code challenge)" 조합이 사용됩니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성 (Creating the Client)

PKCE가 활성화된 클라이언트를 생성하려면 `passport:client` Artisan 명령어에 `--public` 옵션을 사용하세요:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청 (Requesting Tokens)

<a name="code-verifier-code-challenge"></a>
#### 코드 검증자 및 코드 챌린지 (Code Verifier and Code Challenge)

이 그랜트는 클라이언트 비밀 키를 제공하지 않으므로, 개발자가 토큰 요청 시 코드 검증자와 코드 챌린지를 생성해야 합니다.

코드 검증자는 RFC 7636 명세에 따라, 43~128자 범위의 영문자, 숫자, `"-"`, `"."`, `"_"`, `"~"` 문자로 이루어진 임의 문자열이어야 합니다.

코드 챌린지는 URL 및 파일명에 안전한 Base64 인코딩 문자열로, 끝의 `=` 문자는 제거하고 줄바꿈, 공백, 기타 문자가 없어야 합니다:

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 인가를 위한 리디렉션 (Redirecting for Authorization)

클라이언트가 생성된 후, 클라이언트 ID와 생성된 코드 검증자 및 코드 챌린지를 사용해 인가 코드 및 액세스 토큰을 요청합니다. 먼저 소비 앱은 `/oauth/authorize` 경로로 리디렉션 요청을 합니다:

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
#### 인가 코드를 액세스 토큰으로 변환 (Converting Authorization Codes to Access Tokens)

사용자가 인증을 승인하면 소비 애플리케이션으로 리디렉션됩니다. 소비자는 표준 Authorization Code Grant 방식처럼 `state` 값을 확인해야 하며, 일치한다면 `POST` 요청을 보내 액세스 토큰을 요청해야 합니다. 이때 인가 코드와, 원래 생성한 코드 검증자를 같이 보내야 합니다:

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
## Device Authorization Grant (기기 인가 그랜트)

OAuth2 Device Authorization Grant는 TV, 게임 콘솔과 같이 브라우저가 없거나 입력이 제한된 기기에서 "기기 코드"를 교환해 액세스 토큰을 받을 수 있게 합니다. 디바이스 클라이언트는 사용자가 두 번째 기기(예: 컴퓨터나 스마트폰)로 서버에 접속해 제공받은 "사용자 코드(user code)"를 입력하고 인가를 승인하거나 거부하도록 안내합니다.

이제 Passport에 "user code"와 "authorization" 뷰를 반환하는 방법을 알려야 합니다.

렌더링 로직은 `Laravel\Passport\Passport`의 적절한 메서드를 사용해 커스터마이징할 수 있으며, 일반적으로 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름 제공하기...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // 클로저 제공하기...
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

Passport는 이 뷰들을 반환하는 라우트를 자동으로 정의합니다. `auth.oauth.device.user-code` 템플릿에는 `passport.device.authorizations.authorize` 경로로 GET 요청하는 폼이 포함되어야 하며, 이 경로는 `user_code` 쿼리 파라미터를 기대합니다.

`auth.oauth.device.authorize` 템플릿에는 인가 승인 시 `passport.device.authorizations.approve` 경로로 POST 요청하는 승인 폼과, 거부 시 `passport.device.authorizations.deny` 경로로 DELETE 요청하는 거부 폼을 포함해야 합니다. 두 라우트 모두 `state`, `client_id`, `auth_token` 필드를 기대합니다.

<a name="creating-a-device-authorization-grant-client"></a>
### 기기 인가 그랜트 클라이언트 생성 (Creating a Device Authorization Grant Client)

애플리케이션이 기기 인가 그랜트를 통해 토큰을 발급하려면, 디바이스 플로우가 활성화된 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령어에 `--device` 옵션을 사용하세요. 이 명령은 퍼스트파티 디바이스 플로우 클라이언트를 만들고 클라이언트 ID와 비밀 키를 제공합니다:

```shell
php artisan passport:client --device
```

또는 `ClientRepository` 클래스의 `createDeviceAuthorizationGrantClient` 메서드를 사용해 특정 사용자에 속하는 서드파티 클라이언트를 등록할 수 있습니다:

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
### 토큰 요청 (Requesting Tokens)

<a name="device-code"></a>
#### 기기 코드 요청 (Requesting a Device Code)

클라이언트가 생성된 후, 개발자는 클라이언트 ID를 사용해 애플리케이션 `/oauth/device/code` 경로에 `POST` 요청하여 기기 코드를 요청할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

응답은 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 속성을 포함하는 JSON입니다. `expires_in`은 기기 코드 만료까지 남은 초이며, `interval`은 `/oauth/token` 경로를 폴링할 때 권장되는 간격 초입니다.

> [!NOTE]
> `/oauth/device/code` 경로는 Passport에 의해 이미 정의되어 있으므로 직접 정의할 필요가 없습니다.

<a name="user-code"></a>
#### 검증 URI 및 사용자 코드 표시 (Displaying the Verification URI and User Code)

기기 코드 요청이 완료되면, 소비 디바이스는 사용자에게 다른 기기를 사용해 `verification_uri`에 접속하고, 화면에 표시된 `user_code`를 입력해서 인가 요청을 승인하라고 안내해야 합니다.

<a name="polling-token-request"></a>
#### 토큰 요청 폴링 (Polling Token Request)

사용자가 인가 승인을 별도 기기에서 완료하기 때문에, 소비 디바이스는 `/oauth/token` 경로를 폴링하여 사용자의 응답을 대기해야 합니다. 폴링 간격은 기기 코드 요청 시 응답받은 `interval` 값을 사용해야 과도한 요청으로 인한 제한을 피할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // 기밀 클라이언트에만 필요...
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

사용자가 인가 요청을 승인하면, 이 요청은 `access_token`, `refresh_token`, `expires_in` 속성을 포함하는 JSON 응답을 반환합니다.

<a name="password-grant"></a>
## Password Grant (비밀번호 그랜트)

> [!WARNING]
> 비밀번호 그랜트 토큰 사용은 더 이상 권장되지 않습니다. 대신 [OAuth2 Server에서 권장하는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

OAuth2 비밀번호 그랜트는 모바일 앱과 같은 퍼스트파티 클라이언트가 이메일 주소 또는 사용자명과 비밀번호로 액세스 토큰을 받도록 합니다. OAuth2 인가 코드 리디렉션 과정을 거치지 않고도 안전하게 토큰을 발급할 수 있습니다.

비밀번호 그랜트를 활성화하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 `enablePasswordGrant` 메서드를 호출하세요:

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
### 비밀번호 그랜트 클라이언트 생성 (Creating a Password Grant Client)

비밀번호 그랜트를 사용하려면 `passport:client` 명령어에 `--password` 옵션을 지정해 클라이언트를 생성해야 합니다:

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청 (Requesting Tokens)

비밀번호 그랜트가 활성화되고 클라이언트가 생성된 후에는 `/oauth/token` 경로로 `POST` 요청하여 사용자의 이메일/비밀번호로 액세스 토큰을 요청할 수 있습니다. `/oauth/token` 경로는 Passport가 자동으로 등록하므로 직접 정의할 필요가 없습니다. 요청이 성공하면 JSON 응답으로 `access_token`과 `refresh_token`을 받습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // 기밀 클라이언트에만 필요...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

> [!NOTE]
> 액세스 토큰은 기본적으로 장기 유효입니다. 필요할 경우 [최대 액세스 토큰 수명을 구성](#configuration)할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청 (Requesting All Scopes)

비밀번호 그랜트 혹은 클라이언트 자격 증명 그랜트를 사용할 때, 애플리케이션에서 지원하는 모든 스코프를 한 번에 허용하도록 토큰을 요청할 수 있습니다. 이 경우 `*` 스코프를 지정하세요. `*` 스코프가 토큰에 부여되면, 해당 토큰의 `can` 메서드는 항상 `true`를 반환합니다. `*` 스코프는 오로지 `password` 또는 `client_credentials` 그랜트로 발급한 토큰에만 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // 기밀 클라이언트에만 필요...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### 사용자 제공자 커스터마이징 (Customizing the User Provider)

애플리케이션에서 여러 종류의 [인증 사용자 제공자(provider)](/docs/12.x/authentication#introduction)를 사용하는 경우, 비밀번호 그랜트 클라이언트 생성 시 `--provider` 옵션을 통해 어떤 사용자 제공자를 사용할지 지정할 수 있습니다. 지정한 제공자 이름은 `config/auth.php`에 정의된 유효한 사용자 제공자와 일치해야 합니다. 이후 [미들웨어로 해당 가드를 보호](#multiple-authentication-guards)해 해당 제공자의 사용자만 인증되도록 할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명 필드 커스터마이징 (Customizing the Username Field)

비밀번호 그랜트 인증 시, Passport는 기본적으로 인증 가능한 모델의 `email` 속성을 사용해 "사용자명"을 체크합니다. 하지만 모델에 `findForPassport` 메서드를 정의해 사용자명 필드를 커스터마이징할 수 있습니다:

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
     * 주어진 사용자명에 해당하는 사용자 인스턴스 조회.
     */
    public function findForPassport(string $username): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### 비밀번호 검증 커스터마이징 (Customizing the Password Validation)

비밀번호 그랜트 인증 시, Passport는 기본적으로 모델의 `password` 속성으로 주어진 비밀번호를 검증합니다. 만약 모델에 `password` 속성이 없거나 검증 로직을 수정하고 싶다면 `validateForPassportPasswordGrant` 메서드를 모델에 정의하세요:

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
     * Passport 비밀번호 그랜트용 사용자 비밀번호 검증.
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
> 암묵적 그랜트 토큰 사용은 더 이상 권장되지 않습니다. 대신 [OAuth2 Server에서 권장하는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

암묵적 그랜트는 인가 코드를 교환하지 않고 토큰을 바로 클라이언트에 반환하는 점이 다릅니다. 주로 클라이언트 자격 증명을 안전하게 저장할 수 없는 자바스크립트 또는 모바일 앱에서 사용됩니다. 활성화하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enableImplicitGrant`를 호출하세요:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

암묵적 그랜트 클라이언트를 생성하려면 `passport:client` 명령어에 `--implicit` 옵션을 지정하세요:

```shell
php artisan passport:client --implicit
```

이후 개발자는 클라이언트 ID를 사용해 `/oauth/authorize` 경로로 리디렉션하여 액세스 토큰을 요청할 수 있습니다:

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
> `/oauth/authorize` 경로는 Passport에서 미리 정의되어 있으므로 직접 정의하지 않아도 됩니다.

<a name="client-credentials-grant"></a>
## Client Credentials Grant (클라이언트 자격 증명 그랜트)

클라이언트 자격 증명 그랜트는 머신 간 인증에 적합합니다. 예를 들어, API를 사용한 예약 작업처럼 인증이 필요한 유지보수 작업에 사용할 수 있습니다.

클라이언트 자격 증명 그랜트용 클라이언트를 생성하려면 `passport:client` 명령어에 `--client` 옵션을 사용하세요:

```shell
php artisan passport:client --client
```

다음으로, 다음과 같이 라우트에 `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 할당하세요:

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하고, 클라이언트가 리소스 소유자인 경우...
})->middleware(EnsureClientIsResourceOwner::class);
```

라우트 접근을 특정 스코프로 제한하려면 `using` 메서드에 필수 스코프 목록을 전달할 수 있습니다:

```php
Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효, 클라이언트가 리소스 소유자이며 "servers:read"와 "servers:create" 스코프를 모두 보유...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create'));
```

<a name="retrieving-tokens"></a>
### 토큰 조회 (Retrieving Tokens)

이 그랜트 타입을 사용해 토큰을 받으려면 `oauth/token` 엔드포인트에 요청하세요:

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

때때로 사용자가 애플리케이션 UI를 통해 직접 액세스 토큰을 발급받길 원할 수 있습니다. 이 방법은 API를 직접 실험하거나 간단하게 액세스 토큰을 발급하는 용도로 유용합니다.

> [!NOTE]
> 애플리케이션이 주로 개인 액세스 토큰 발급용으로 Passport를 사용한다면, Laravel의 경량 1차 라이브러리인 [Laravel Sanctum](/docs/12.x/sanctum)은 대안으로 고려해보세요.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성 (Creating a Personal Access Client)

개인 액세스 토큰을 발급하려면 `passport:client` 명령어에 `--personal` 옵션을 지정해 개인 액세스 클라이언트를 생성해야 합니다. 만약 이미 `passport:install`을 실행했다면 이 명령은 생략해도 됩니다:

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### 사용자 제공자 커스터마이징 (Customizing the User Provider)

애플리케이션에서 여러 [인증 사용자 제공자](/docs/12.x/authentication#introduction)를 사용한다면, 개인 액세스 그랜트 클라이언트 생성 시 `--provider` 옵션으로 사용할 사용자 제공자를 지정할 수 있습니다. 지정한 이름은 `config/auth.php`에 정의된 유효한 제공자여야 합니다. 이후 [미들웨어로 가드 보호](#multiple-authentication-guards)해 해당 제공자의 사용자만 인증하게 할 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리 (Managing Personal Access Tokens)

개인 액세스 클라이언트를 생성한 후, 특정 사용자에 대해 `App\Models\User` 인스턴스의 `createToken` 메서드로 토큰을 발급할 수 있습니다. `createToken`은 첫 번째 인자로 토큰 이름, 두 번째 인자로 옵션인 [스코프](#token-scopes) 배열을 받습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 스코프 없이 토큰 생성...
$token = $user->createToken('My Token')->accessToken;

// 스코프 포함 토큰 생성...
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
## 라우트 보호 (Protecting Routes)

<a name="via-middleware"></a>
### 미들웨어 방식 (Via Middleware)

Passport는 들어오는 요청의 액세스 토큰을 검증하는 [인증 가드](/docs/12.x/authentication#adding-custom-guards)를 포함합니다. `api` 가드를 `passport` 드라이버로 설정한 후에는, 유효한 액세스 토큰이 필요한 라우트에 `auth:api` 미들웨어를 적용하기만 하면 됩니다:

```php
Route::get('/user', function () {
    // API 인증된 사용자만 접근 가능...
})->middleware('auth:api');
```

> [!WARNING]
> [클라이언트 자격 증명 그랜트](#client-credentials-grant)를 사용하는 경우, `auth:api` 미들웨어 대신 [Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner 미들웨어](#client-credentials-grant)를 사용해 라우트를 보호해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 다중 인증 가드 (Multiple Authentication Guards)

애플리케이션에서 서로 다른 Eloquent 모델을 사용하는 여러 유형의 사용자를 인증한다면, 각 사용자 제공자별로 가드 구성을 정의해야 할 것입니다. 이렇게 하면 특정 사용자 제공자에 맞춘 요청 보호가 가능합니다. 예를 들어, `config/auth.php`에 다음과 같이 정의된 경우:

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

다음 라우트는 `customers` 사용자 제공자를 사용하는 `api-customers` 가드를 이용해 인증합니다:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport에서 여러 사용자 제공자를 사용하는 자세한 내용은 [개인 액세스 토큰 문서](#customizing-the-user-provider-for-pat)와 [비밀번호 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달 (Passing the Access Token)

Passport로 보호된 라우트를 호출할 때 애플리케이션 API 소비자는 `Authorization` 헤더에 `Bearer` 토큰으로 액세스 토큰을 지정해야 합니다. 예를 들어 `Http` 파사드를 사용할 때:

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

스코프는 API 클라이언트가 계정에 접근 권한을 요청할 때 특정 권한 범위를 지정할 수 있게 합니다. 예를 들어, 전자상거래 앱이라면 모든 API 소비자가 주문을 생성하는 권한이 필요하지 않을 수 있습니다. 대신 배송 상태만 접근하게 허용할 수도 있습니다. 즉, 스코프는 사용자가 서드파티 애플리케이션에 위임하는 동작 제한을 할 수 있게 합니다.

<a name="defining-scopes"></a>
### 스코프 정의 (Defining Scopes)

애플리케이션의 스코프는 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 `Passport::tokensCan` 메서드를 사용해 정의합니다. 이 메서드는 스코프 이름과 설명을 배열로 받으며, 설명은 인가 승인 화면에 사용자에게 표시됩니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensCan([
        'user:read' => 'Retrieve the user info',
        'orders:create' => 'Place orders',
        'orders:read:status' => 'Check order status',
    ]);
}
```

<a name="default-scope"></a>
### 기본 스코프 (Default Scope)

클라이언트가 특정 스코프를 요청하지 않으면, Passport 서버가 기본적으로 토큰에 붙일 스코프를 `defaultScopes` 메서드로 설정할 수 있습니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Passport\Passport;

Passport::tokensCan([
    'user:read' => 'Retrieve the user info',
    'orders:create' => 'Place orders',
    'orders:read:status' => 'Check order status',
]);

Passport::defaultScopes([
    'user:read',
    'orders:create',
]);
```

<a name="assigning-scopes-to-tokens"></a>
### 토큰에 스코프 할당 (Assigning Scopes to Tokens)

<a name="when-requesting-authorization-codes"></a>
#### 인가 코드 요청 시 (When Requesting Authorization Codes)

인가 코드 그랜트를 사용할 때는, 소비자는 쿼리 파라미터 `scope`로 원하는 스코프들을 공백으로 구분해 지정해야 합니다:

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
#### 개인 액세스 토큰 발급 시 (When Issuing Personal Access Tokens)

`App\Models\User` 모델 인스턴스의 `createToken` 메서드를 사용할 때 두 번째 인자로 원하는 스코프 배열을 전달할 수 있습니다:

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 검사 (Checking Scopes)

Passport는 들어오는 요청이 특정 스코프를 가진 액세스 토큰으로 인증되었는지 확인하는 데 사용할 수 있는 두 개의 미들웨어를 제공합니다.

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인 (Check For All Scopes)

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어는 액세스 토큰이 모든 지정된 스코프를 갖고 있음을 검증합니다:

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // 액세스 토큰이 "orders:read" 및 "orders:create" 스코프 모두를 포함...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create')]);
```

<a name="check-for-any-scopes"></a>
#### 일부 스코프 확인 (Check for Any Scopes)

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어는 액세스 토큰이 지정한 스코프 중 *하나 이상*을 포함하는지 검증합니다:

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // 액세스 토큰이 "orders:read" 또는 "orders:create" 스코프 중 적어도 하나 포함...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create')]);
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인 (Checking Scopes on a Token Instance)

액세스 토큰 인증된 요청이 애플리케이션에 진입한 후, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드로 스코프 검사를 수행할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('orders:create')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
#### 추가 스코프 관련 메서드 (Additional Scope Methods)

- `scopeIds` 메서드는 정의된 모든 스코프 ID/이름의 배열을 반환합니다:

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

- `scopes` 메서드는 `Laravel\Passport\Scope` 인스턴스 배열로 모든 정의된 스코프를 반환합니다:

```php
Passport::scopes();
```

- `scopesFor` 메서드는 지정한 ID/이름에 해당하는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다:

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

- `hasScope` 메서드는 특정 스코프가 정의되어 있는지 여부를 반환합니다:

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

API를 구축할 때, 자바스크립트 애플리케이션에서 본인의 API를 소비할 수 있다면 매우 유용합니다. 이렇게 하면 웹 애플리케이션, 모바일 앱, 서드파티 앱, 여러 패키지 매니저에 배포하는 SDK 등 여러 곳에서 동일한 API를 사용하게 됩니다.

일반적으로 자바스크립트 앱에서 API를 소비하려면 액세스 토큰을 수동으로 전달해야 하지만, Passport는 이를 처리하는 미들웨어를 제공합니다. 단지 애플리케이션의 `bootstrap/app.php` 파일에서 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어만 추가하면 됩니다:

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어는 미들웨어 스택에서 마지막 미들웨어로 배치하는 것을 권장합니다.

이 미들웨어는 응답에 `laravel_token` 쿠키를 붙입니다. 이 쿠키에는 Passport가 API 요청을 인증하기 위한 암호화된 JWT가 포함되어 있으며, JWT의 수명은 `session.lifetime` 구성 값과 같습니다. 브라우저가 쿠키를 자동 전송하기 때문에, 명시적으로 액세스 토큰을 전달하지 않아도 API 요청이 가능합니다:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이징 (Customizing the Cookie Name)

필요하면 `Passport::cookie` 메서드로 `laravel_token` 쿠키 이름을 변경할 수 있습니다. 보통 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 설정합니다:

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
#### CSRF 보호 (CSRF Protection)

이 인증 방식을 사용할 때, 요청에 올바른 CSRF 토큰 헤더가 포함되어야 합니다. Laravel 기본 자바스크립트 스캐폴딩과 모든 스타터 킷에는 [Axios](https://github.com/axios/axios) 인스턴스가 포함되어 있으며, 동일 출처 요청에 암호화된 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더로 자동 전송합니다.

> [!NOTE]
> 직접 `X-CSRF-TOKEN` 헤더를 사용하려면, 암호화되지 않은 `csrf_token()` 값을 사용해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

Passport는 액세스 토큰 및 리프레시 토큰 발급 시 이벤트를 발생시킵니다. 이 이벤트들을 [리스닝](/docs/12.x/events)하여 데이터베이스 내 다른 토큰을 정리하거나 폐기하는 데 활용할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름           |
| -------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## 테스트 (Testing)

Passport의 `actingAs` 메서드는 현재 인증된 사용자와 해당 스코프를 지정하는 데 사용됩니다. 첫 번째 인자로 사용자 인스턴스를, 두 번째 인자로 스코프 배열을 받습니다:

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

Passport의 `actingAsClient` 메서드는 현재 인증된 클라이언트와 해당 스코프를 지정하는 데 사용됩니다. 첫 번째 인자로 클라이언트 인스턴스, 두 번째 인자로 스코프 배열을 받습니다:

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