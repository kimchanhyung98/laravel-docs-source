# Laravel Passport (Laravel Passport)

- [소개](#introduction)
    - [Passport 또는 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포](#deploying-passport)
    - [Passport 업그레이드](#upgrading-passport)
- [설정](#configuration)
    - [토큰 만료 기간](#token-lifetimes)
    - [기본 모델 오버라이드](#overriding-default-models)
    - [라우트 오버라이드](#overriding-routes)
- [인증 코드 그랜트](#authorization-code-grant)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청](#requesting-tokens)
    - [토큰 관리](#managing-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 철회](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [PKCE 인증 코드 그랜트](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청](#requesting-auth-pkce-grant-tokens)
- [기기 인증 그랜트](#device-authorization-grant)
    - [기기 코드 그랜트 클라이언트 생성](#creating-a-device-authorization-grant-client)
    - [토큰 요청](#requesting-device-authorization-grant-tokens)
- [비밀번호 그랜트](#password-grant)
    - [비밀번호 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [User Provider 커스터마이징](#customizing-the-user-provider)
    - [Username 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 커스터마이징](#customizing-the-password-validation)
- [임플리시트 그랜트](#implicit-grant)
- [클라이언트 자격 증명 그랜트](#client-credentials-grant)
- [퍼스널 액세스 토큰](#personal-access-tokens)
    - [퍼스널 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [User Provider 커스터마이징](#customizing-the-user-provider-for-pat)
    - [퍼스널 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호](#protecting-routes)
    - [미들웨어 사용](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당](#assigning-scopes-to-tokens)
    - [스코프 확인](#checking-scopes)
- [SPA 인증](#spa-authentication)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Passport](https://github.com/laravel/passport)는 여러분의 Laravel 애플리케이션에 수 분 만에 완전한 OAuth2 서버 구현을 제공합니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 서버](https://github.com/thephpleague/oauth2-server)를 기반으로 구축되었습니다.

> [!NOTE]
> 이 문서는 여러분이 이미 OAuth2에 대해 어느 정도 알고 있다는 것을 전제로 작성되었습니다. OAuth2에 대해 아무 것도 모르는 경우, 계속 진행하기 전에 [용어](https://oauth2.thephpleague.com/terminology/)와 주요 기능에 익숙해지는 것이 좋습니다.

<a name="passport-or-sanctum"></a>
### Passport 또는 Sanctum?

시작하기 전에, 여러분의 애플리케이션에 Laravel Passport가 더 적합한지, [Laravel Sanctum](/docs/12.x/sanctum)이 더 적합한지 먼저 판단하는 것이 좋습니다. 만약 애플리케이션이 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용해야 합니다.

하지만, 싱글 페이지 애플리케이션(SPA)이나 모바일 애플리케이션 인증 또는 API 토큰 발급이 목적이라면 [Laravel Sanctum](/docs/12.x/sanctum)을 사용하는 것을 추천합니다. Laravel Sanctum은 OAuth2를 지원하지 않지만, 훨씬 단순한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치 (Installation)

Laravel Passport는 `install:api` Artisan 명령어로 설치할 수 있습니다:

```shell
php artisan install:api --passport
```

이 명령어는 OAuth2 클라이언트와 액세스 토큰을 저장하기 위한 테이블을 만들기 위해 필요한 데이터베이스 마이그레이션을 생성하고 실행합니다. 또한, 보안 액세스 토큰 생성을 위한 암호화 키도 생성합니다.

`install:api` 명령어를 실행한 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가해야 합니다. 이 트레이트는 인증된 사용자의 토큰과 스코프 확인을 위한 여러 헬퍼 메서드를 제공합니다:

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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고, `driver` 옵션을 `passport`로 지정해야 합니다. 이렇게 하면, API 요청 인증 시 Passport의 `TokenGuard`를 사용하게 됩니다:

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

애플리케이션 서버에 Passport를 처음 배포할 때는 `passport:keys` 명령어를 실행해야 할 수 있습니다. 이 명령어는 액세스 토큰 생성을 위한 암호화 키를 만듭니다. 생성된 키 파일은 일반적으로 소스 컨트롤에 포함하지 않습니다:

```shell
php artisan passport:keys
```

필요하다면 Passport 키가 로드되어야 할 경로를 지정할 수도 있습니다. 이를 위해 `Passport::loadKeysFrom` 메서드를 사용할 수 있습니다. 보통 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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
#### 환경 변수에서 키 불러오기

또한, `vendor:publish` Artisan 명령어를 사용해 Passport의 설정 파일을 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일을 퍼블리시한 후, 아래와 같이 환경 변수로 암호화 키를 불러올 수 있습니다:

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

Passport를 새로운 메이저 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 신중히 검토하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="token-lifetimes"></a>
### 토큰 만료 기간 (Token Lifetimes)

Passport는 기본적으로 1년 후 만료되는 장기 액세스 토큰을 발급합니다. 좀 더 짧거나 긴 토큰 만료 기간을 원한다면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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
> Passport 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며, 단순 표시용입니다. 토큰을 발급할 때 Passport는 만료 정보를 토큰 자체(서명되고 암호화된 토큰)에 포함합니다. 만약 토큰을 무효화해야 한다면 [토큰 철회](#revoking-tokens)를 수행해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드 (Overriding Default Models)

Passport에서 내부적으로 사용하는 기본 모델을 확장할 수 있습니다. 여러분만의 모델을 정의하고 해당 Passport 모델을 상속하세요:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의한 후, `Laravel\Passport\Passport` 클래스를 통해 Passport에 커스텀 모델을 사용하도록 지시할 수 있습니다. 보통 이 코드는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 작성합니다:

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
### 라우트 오버라이드 (Overriding Routes)

Passport에서 기본적으로 정의하는 라우트를 커스터마이징하고 싶을 때가 있습니다. 이 경우, 먼저 `AppServiceProvider`의 `register` 메서드에 `Passport::ignoreRoutes`를 추가하여 Passport의 라우트 등록을 무시하세요:

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

그 다음, [Passport의 라우트 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 여러분의 애플리케이션 `routes/web.php`에 복사한 뒤 원하시는 대로 수정하시면 됩니다:

```php
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => '\Laravel\Passport\Http\Controllers',
], function () {
    // Passport routes...
});
```

<a name="authorization-code-grant"></a>
## 인증 코드 그랜트 (Authorization Code Grant)

OAuth2 인증 코드 방식을 사용하면, 많은 개발자들이 익숙한 인증 방식을 구현할 수 있습니다. 이 방식에서는 클라이언트 애플리케이션이 사용자를 여러분의 서버로 리디렉션하고, 사용자는 액세스 토큰 발급 요청을 승인하거나 거절하게 됩니다.

먼저, Passport에 "authorization" 뷰를 어떻게 반환할지 알려줘야 합니다.

모든 인증 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스의 적절한 메서드를 통해 커스터마이즈할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 전달하는 방식
    Passport::authorizationView('auth.oauth.authorize');

    // 클로저를 전달하는 방식
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

Passport는 자동으로 이 뷰를 반환하는 `/oauth/authorize` 라우트를 정의합니다. 여러분의 `auth.oauth.authorize` 템플릿에는 인증 승인을 처리하는 `passport.authorizations.approve` 라우트로의 POST 폼과, 인증 거부를 처리하는 `passport.authorizations.deny` 라우트로의 DELETE 폼이 필요합니다. 이 두 라우트는 `state`, `client_id`, `auth_token` 필드를 요구합니다.

<a name="managing-clients"></a>
### 클라이언트 관리 (Managing Clients)

여러분의 API와 상호작용해야 하는 다른 애플리케이션 개발자들은 "클라이언트"를 생성하여 자신의 애플리케이션을 등록해야 합니다. 보통 애플리케이션 이름과 인증 후 사용자를 리디렉션할 URI를 제공합니다.

<a name="managing-first-party-clients"></a>
#### 1st-party 클라이언트

가장 간단한 클라이언트 생성 방법은 `passport:client` Artisan 명령어를 사용하는 것입니다. 이 명령어는 1st-party 클라이언트 생성이나 OAuth2 기능 테스트 시 활용할 수 있습니다. 명령어 실행 시 필요한 정보를 입력받아, 클라이언트 ID와 시크릿을 제공합니다:

```shell
php artisan passport:client
```

여러 개의 리디렉션 URI를 허용하려면, URI 입력 시 콤마(,)로 구분하여 작성하면 됩니다. URI 내에 콤마가 포함된 경우 URI 인코딩을 해야 합니다:

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 3rd-party 클라이언트

애플리케이션 사용자가 `passport:client` 명령어를 직접 사용할 수 없는 경우, `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드로 주어진 사용자에 대한 클라이언트를 등록할 수 있습니다:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// 주어진 사용자에 속한 OAuth 앱 클라이언트 생성
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// 해당 사용자의 모든 OAuth 앱 클라이언트 조회
$clients = $user->oauthApps()->get();
```

`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. 사용자에게 `$client->id`(클라이언트 ID)와 `$client->plainSecret`(클라이언트 시크릿)을 제공할 수 있습니다.

<a name="requesting-tokens"></a>
### 토큰 요청 (Requesting Tokens)

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인증 요청용 리디렉션

클라이언트를 생성한 뒤, 개발자들은 애플리케이션의 클라이언트 ID와 시크릿을 사용해 인증 코드 및 액세스 토큰을 요청할 수 있습니다. 우선, 클라이언트를 사용하고자 하는 애플리케이션에서 여러분의 애플리케이션의 `/oauth/authorize` 라우트로 리디렉션 요청을 보냅니다:

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
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

`prompt` 파라미터는 Passport 애플리케이션의 인증 동작을 지정할 때 사용합니다.

- `none`: 사용자가 Passport에 인증되어 있지 않으면 무조건 인증 오류를 반환합니다.
- `consent`: 이전에 모든 스코프를 승인했더라도 인증 승인 화면을 항상 표시합니다.
- `login`: 이미 세션이 있더라도 항상 재로그인을 요구합니다.

`prompt` 값을 지정하지 않으면, 사용자가 요청된 스코프에 대해 권한을 부여한 적이 없을 때만 인증 요청 화면이 표시됩니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 Passport가 이미 정의하고 있습니다. 직접 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 요청 승인

인증 요청을 받으면, Passport는 `prompt` 파라미터 값에 맞게 자동으로 동작하며, 사용자가 인증 요청을 승인하거나 거절할 수 있는 화면을 보여줄 수 있습니다. 사용자가 요청을 승인하면, 원래 지정된 `redirect_uri`로 리디렉션됩니다. 이 URI는 클라이언트 등록 시 지정한 `redirect` URL과 일치해야 합니다.

1st-party 클라이언트 등 특수한 경우 인증 화면을 건너뛰고 싶을 때가 있습니다. 이 경우, [Client 모델을 확장](#overriding-default-models)한 후 `skipsAuthorization` 메서드를 정의하세요. `skipsAuthorization`가 `true`를 반환하면 인증 요청 승인 화면 없이 곧바로 `redirect_uri`로 이동합니다(단, consuming 앱에서 `prompt`를 명시적으로 설정한 경우에는 무시됨):

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 클라이언트가 인증 승인 화면을 건너뛸지 여부 결정
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
#### 인증 코드 → 액세스 토큰 변환

사용자가 인증 요청을 승인하면, consuming 애플리케이션으로 리디렉션됩니다. 이때, consuming 앱에서는 `state` 파라미터가 리디렉션 전 저장해둔 값과 동일한지 반드시 확인해야 합니다. 일치하면 여러분의 애플리케이션에 `POST` 요청을 보내 액세스 토큰을 요청합니다. 이 요청에는 사용자가 승인 때 받은 인증 코드가 포함되어야 합니다:

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

이 `/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in` 값은 액세스 토큰이 만료될 때까지 남은 초(second)입니다.

> [!NOTE]
> `/oauth/authorize` 라우트와 마찬가지로 `/oauth/token` 라우트도 Passport가 미리 정의하고 있으므로 직접 정의할 필요가 없습니다.

<a name="managing-tokens"></a>
### 토큰 관리 (Managing Tokens)

`Laravel\Passport\HasApiTokens` 트레이트의 `tokens` 메서드를 사용하여 사용자가 승인한 토큰들을 조회할 수 있습니다. 예를 들어, 사용자가 타사 애플리케이션과 연결한 내역을 대시보드로 제공할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 유효한 토큰 모두 조회
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// 타사 OAuth 앱 클라이언트 별 연결 내역 조회
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

단기 액세스 토큰을 발급하는 경우, 사용자는 토큰이 만료되었을 때 함께 제공된 리프레시 토큰으로 액세스 토큰을 갱신할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // 기밀 클라이언트에만 필요
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 `/oauth/token` 라우트도 마찬가지로 `access_token`, `refresh_token`, `expires_in` 값을 반환합니다.

<a name="revoking-tokens"></a>
### 토큰 철회 (Revoking Tokens)

토큰을 철회하려면 `Laravel\Passport\Token` 모델의 `revoke` 메서드를 사용하세요. 리프레시 토큰을 철회하려면 `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드를 사용합니다:

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// 액세스 토큰 철회
$token->revoke();

// 해당 토큰의 리프레시 토큰 철회
$token->refreshToken?->revoke();

// 해당 사용자의 모든 토큰 철회
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### 토큰 정리 (Purging Tokens)

토큰이 철회되었거나 만료된 경우, 데이터베이스에서 영구적으로 삭제하고 싶을 때에는 Passport의 `passport:purge` Artisan 명령어를 사용할 수 있습니다:

```shell
# 철회 및 만료된 토큰, 인증 코드, 기기 코드 정리
php artisan passport:purge

# 6시간을 초과해 만료된 토큰만 정리
php artisan passport:purge --hours=6

# 철회된 토큰만 정리
php artisan passport:purge --revoked

# 만료된 토큰만 정리
php artisan passport:purge --expired
```

애플리케이션의 `routes/console.php` 파일에서 [스케줄 작업](/docs/12.x/scheduling)을 설정하여 자동으로 토큰을 정리할 수도 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## PKCE 인증 코드 그랜트 (Authorization Code Grant With PKCE)

"Proof Key for Code Exchange"(PKCE) 방식의 인증 코드 그랜트는 SPA(싱글 페이지 애플리케이션)나 모바일 앱 등, 클라이언트 시크릿을 안전하게 보관할 수 없는 경우에 특히 안전한 방식입니다. "코드 검증자(code verifier)"와 "코드 챌린지(code challenge)"의 조합이 클라이언트 시크릿을 대신하여 사용됩니다. 이 방법은 중간자 공격에 의한 인증 코드 탈취 위험도 줄여줍니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성 (Creating the Client)

PKCE를 사용하는 인증 코드 그랜트로 토큰 발급을 시작하기 전에, 먼저 PKCE 지원 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령어에 `--public` 옵션을 추가해 생성할 수 있습니다:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청 (Requesting Tokens)

<a name="code-verifier-code-challenge"></a>
#### 코드 검증자(code verifier)와 코드 챌린지(code challenge) 생성

이 인증 방식은 클라이언트 시크릿을 제공하지 않으므로, 개발자는 토큰을 요청할 때 코드 검증자와 챌린지를 생성해야 합니다.

- 코드 검증자: 영문, 숫자, `"-"`, `"."`, `"_"`, `"~"` 문자로 이루어진 43~128자 랜덤 문자열([RFC 7636](https://tools.ietf.org/html/rfc7636) 규약 참고)
- 코드 챌린지: URL/파일명 안전(Base64), 마지막 `=`은 없고, 줄 바꿈·공백 등은 제거

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 인증 요청용 리디렉션

클라이언트가 생성되면, 클라이언트 ID와 위에서 만든 코드 검증자 및 챌린지를 조합하여 여러분의 애플리케이션 `/oauth/authorize`로 인증 코드 요청을 보냅니다:

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
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
#### 인증 코드 → 액세스 토큰 변환

사용자가 인증을 승인하면, PKCE 방식에서도 `state` 값이 이전에 저장한 값과 일치하는지 소비 애플리케이션에서 검증해야 합니다. 일치하면, 원래 저장한 code verifier와 함께 인증 코드를 포함해 액세스 토큰을 요청하면 됩니다:

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
## 기기 인증 그랜트 (Device Authorization Grant)

OAuth2 기기 인증 그랜트는 TV, 콘솔 등 키보드가 없거나 입력이 제한된 디바이스에서 "디바이스 코드"를 교환하여 액세스 토큰을 발급받게 해줍니다. 이 방식에서는 기기에서 사용자가 휴대폰/컴퓨터 등 다른 장치로 특정 인증 페이지(verification URI)에 접속한 뒤, 제공받은 "user code"를 입력해 권한 요청을 승인 또는 거절합니다.

먼저 Passport에 "user code"와 "authorization" 뷰를 어떻게 반환할지 알려줍니다.

모든 인증 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스의 적절한 메서드를 통해 커스터마이즈할 수 있으며, 보통 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 작성합니다.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름 사용하는 경우
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // 클로저 사용하는 경우
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

Passport는 위 뷰를 반환하는 라우트들을 자동으로 등록합니다. `auth.oauth.device.user-code` 템플릿 안에는 `passport.device.authorizations.authorize` 라우트로 `GET` 요청을 보내는 폼이 필요하며, 이 라우트는 `user_code` 쿼리 파라미터를 기대합니다.

`auth.oauth.device.authorize` 템플릿에는 인증 승인(POST: `passport.device.authorizations.approve`), 거부(DELETE: `passport.device.authorizations.deny`)를 위한 폼이 들어가야 하며, 두 라우트는 `state`, `client_id`, `auth_token` 필드를 요구합니다.

<a name="creating-a-device-authorization-grant-client"></a>
### 기기 코드 그랜트 클라이언트 생성 (Creating a Device Authorization Grant Client)

기기 인증 그랜트로 토큰을 발급하기 위해서는, 기기 플로우를 활성화한 클라이언트가 있어야 합니다. `passport:client` Artisan 명령어에 `--device` 옵션을 사용해 생성할 수 있습니다. 생성 시 클라이언트 ID와 시크릿을 받게 됩니다:

```shell
php artisan passport:client --device
```

또는, `ClientRepository` 클래스의 `createDeviceAuthorizationGrantClient` 메서드를 통해 3rd-party 클라이언트를 직접 생성할 수도 있습니다:

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
#### 디바이스 코드 요청

클라이언트가 준비되면, 개발자는 클라이언트 ID로여러분의 애플리케이션에 디바이스 코드를 요청할 수 있습니다. 소비 디바이스에서 `/oauth/device/code` 엔드포인트에 `POST`로 요청을 보냅니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

응답에는 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 필드가 포함된 JSON이 반환됩니다. `expires_in`은 디바이스 코드 만료까지 남은 초, `interval`은 사용자가 `/oauth/token` 엔드포인트 폴링 시 새 요청 전 대기해야 하는 최소 초 단위입니다.

> [!NOTE]
> `/oauth/device/code` 라우트도 Passport가 이미 정의하고 있으므로 직접 정의할 필요가 없습니다.

<a name="user-code"></a>
#### 인증 URI와 User Code 표시

디바이스 코드 응답을 받은 후, 사용자는 다른 장치(PC, 스마트폰 등)에서 `verification_uri`로 이동해 `user_code`를 입력하여 인증을 승인해야 합니다.

<a name="polling-token-request"></a>
#### 토큰 요청 폴링

사용자는 별도의 장치로 인증을 승인/거부하므로, 소비 디바이스에서는 지정된 `interval` 시간만큼 대기하며 `/oauth/token` 엔드포인트를 폴링해 인증이 처리되었는지 확인해야 합니다:

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // 기밀 클라이언트에만 필요
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

사용자가 인증을 승인하면 `access_token`, `refresh_token`, `expires_in` 값이 담긴 JSON이 반환됩니다.

<a name="password-grant"></a>
## 비밀번호 그랜트 (Password Grant)

> [!WARNING]
> 비밀번호 기반 그랜트 토큰 사용은 더 이상 권장하지 않습니다. 대신 [OAuth2 Server에서 현재 권장하는 다른 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

OAuth2 비밀번호 그랜트는, 다른 1st-party 클라이언트(예: 모바일 앱 등)가 이메일/아이디와 비밀번호를 이용해 액세스 토큰을 받을 수 있도록 해줍니다. 이를 통해, 사용자가 복잡한 OAuth2 인증 코드 리디렉션 과정을 거치지 않고도 토큰을 발급받을 수 있습니다.

비밀번호 그랜트를 활성화하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enablePasswordGrant`를 호출하세요:

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

비밀번호 그랜트로 토큰을 발급하려면, `passport:client` Artisan 명령어에 `--password` 옵션을 지정해 비밀번호 그랜트 전용 클라이언트를 생성해야 합니다.

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청 (Requesting Tokens)

그랜트를 활성화하고 비밀번호 그랜트 클라이언트를 만든 뒤에는, 이메일과 비밀번호로 `/oauth/token` 라우트에 `POST` 요청을 보내 액세스 토큰을 받을 수 있습니다. 이 라우트는 Passport가 이미 등록하고 있으므로 별도 정의는 필요하지 않습니다.

요청이 성공하면 서버에서 `access_token`과 `refresh_token`을 포함한 JSON 응답이 반환됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // 기밀 클라이언트에만 필요
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

> [!NOTE]
> 액세스 토큰은 기본적으로 장기 토큰입니다. 만약 필요하다면 [최대 액세스 토큰 만료 시간](#configuration)을 조정할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청 (Requesting All Scopes)

비밀번호 그랜트나 클라이언트 자격 증명 그랜트에서 토큰을 요청할 때, 애플리케이션의 모든 스코프에 권한을 주고 싶은 경우가 있습니다. 이때는 `*` 스코프를 요청하면 됩니다. `*` 스코프가 할당된 토큰의 `can` 메서드는 항상 `true`를 반환합니다(단, password/client_credentials 그랜트에만 해당):

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // 기밀 클라이언트에만 필요
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### User Provider 커스터마이징 (Customizing the User Provider)

애플리케이션에서 [인증 User Provider](/docs/12.x/authentication#introduction)를 여러 개 사용하는 경우, `artisan passport:client --password` 명령어로 클라이언트를 생성할 때 `--provider` 옵션으로 사용하고자 하는 provider를 지정할 수 있습니다. provider 이름은 여러분의 `config/auth.php`에 정의된 값이어야 합니다. 이후 [미들웨어로 라우트 보호](#multiple-authentication-guards)를 설정하면, guard가 사용할 provider에 해당하는 사용자만 인증할 수 있도록 제한할 수 있습니다.

<a name="customizing-the-username-field"></a>
### Username 필드 커스터마이징 (Customizing the Username Field)

비밀번호 그랜트 인증 시 Passport는 기본적으로 모델의 `email` 속성을 username으로 사용합니다. 이를 변경하려면, 모델에 `findForPassport` 메서드를 정의하세요:

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
     * 주어진 username으로 사용자 인스턴스 찾기
     */
    public function findForPassport(string $username): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### 비밀번호 검증 커스터마이징 (Customizing the Password Validation)

Passport는 기본적으로 모델의 `password` 속성을 사용해 비밀번호를 검증합니다. 만약 모델에 `password` 속성이 없거나, 비밀번호 검증 로직을 변경하고 싶다면, `validateForPassportPasswordGrant` 메서드를 모델에 정의하면 됩니다:

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
     * Passport 비밀번호 그랜트용 비밀번호 검증 로직
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant"></a>
## 임플리시트 그랜트 (Implicit Grant)

> [!WARNING]
> 임플리시트 그랜트 토큰 사용은 더 이상 권장하지 않습니다. 대신 [OAuth2 Server에서 권장하는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 사용하는 것이 좋습니다.

임플리시트 그랜트는 인증 코드 그랜트와 비슷하지만, 인증 코드를 교환하지 않고 곧바로 토큰을 클라이언트에 반환합니다. 일반적으로 JavaScript 앱, 모바일 앱 등 클라이언트 시크릿을 안전하게 저장할 수 없는 환경에서 사용합니다. 활성화하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enableImplicitGrant`를 호출합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

임플리시트 그랜트로 토큰을 발급하기 전에, `passport:client` Artisan 명령어의 `--implicit` 옵션으로 임플리시트 그랜트 클라이언트를 생성해야 합니다.

```shell
php artisan passport:client --implicit
```

임플리시트 그랜트가 활성화되고, 클라이언트를 생성한 후에는, 아래와 같이 클라이언트 ID로 인증 요청을 보낼 수 있습니다:

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
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

> [!NOTE]
> `/oauth/authorize` 라우트는 Passport가 이미 정의하고 있으니 따로 등록하지 않아도 됩니다.

<a name="client-credentials-grant"></a>
## 클라이언트 자격 증명 그랜트 (Client Credentials Grant)

클라이언트 자격 증명 그랜트는 머신-투-머신 인증에 적합합니다. 예를 들어, 예약된 작업(scheduled job)이나 API 유지 보수 작업을 수행하는 스크립트에서 이 그랜트를 사용할 수 있습니다.

이 그랜트로 토큰을 발급하려면 먼저 `passport:client` Artisan 명령어에서 `--client` 옵션을 사용해 클라이언트 자격 증명용 클라이언트를 만듭니다:

```shell
php artisan passport:client --client
```

그리고 `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 라우트에 적용합니다:

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하며 클라이언트가 리소스 소유자임
})->middleware(EnsureClientIsResourceOwner::class);
```

특정 스코프를 갖는 클라이언트만 접근하도록 제한하려면, `using` 메서드로 스코프 목록을 전달할 수 있습니다:

```php
Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하고, 리소스 소유자이면서 "servers:read" 및 "servers:create" 스코프 모두 소유
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create'));
```

<a name="retrieving-tokens"></a>
### 토큰 발급

이 그랜트 타입으로 토큰을 요청하려면 아래처럼 `oauth/token` 엔드포인트에 요청을 보냅니다:

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
## 퍼스널 액세스 토큰 (Personal Access Tokens)

때론 사용자가 직접 액세스 토큰을 발급받도록 하고 싶을 수도 있습니다. 클라이언트 측 UI에서 직접 토큰을 발급하게 하면, API를 테스트 하거나 인증 흐름이 복잡하지 않은 간단한 용도에 매우 유용합니다.

> [!NOTE]
> 만약 주로 퍼스널 액세스 토큰 발급만이 목적이라면, 보다 경량화된 [Laravel Sanctum](/docs/12.x/sanctum) 사용을 고려하세요.

<a name="creating-a-personal-access-client"></a>
### 퍼스널 액세스 클라이언트 생성 (Creating a Personal Access Client)

퍼스널 액세스 토큰을 발급하려면 `passport:client` Artisan 명령어에 `--personal` 옵션을 넣어 퍼스널 액세스 클라이언트를 생성해야 합니다. 만약 이미 `passport:install`을 실행했다면 따로 이 명령을 실행할 필요는 없습니다:

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### User Provider 커스터마이징 (Customizing the User Provider)

복수의 [인증 User Provider](/docs/12.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --personal` 명령어로 클라이언트 생성 시 `--provider` 옵션을 주어 해당 provider를 지정할 수 있습니다. provider 이름은 반드시 `config/auth.php`에 정의된 값이어야 하며, [미들웨어로 라우트 보호](#multiple-authentication-guards)도 적용할 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### 퍼스널 액세스 토큰 관리 (Managing Personal Access Tokens)

퍼스널 액세스 클라이언트를 생성한 후에는, 주어진 사용자에 대해 `App\Models\User` 인스턴스의 `createToken` 메서드로 토큰을 발급할 수 있습니다. 첫 번째 인자는 토큰 이름, 두 번째 인자는 [스코프](#token-scopes) 배열(생략 가능)입니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 스코프 없는 토큰 생성
$token = $user->createToken('My Token')->accessToken;

// 스코프 지정 토큰 생성
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// 전체 스코프 토큰 생성
$token = $user->createToken('My Token', ['*'])->accessToken;

// 사용자에게 속한 유효한 퍼스널 액세스 토큰 모두 조회
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
### 미들웨어 사용 (Via Middleware)

Passport는 [인증 가드](/docs/12.x/authentication#adding-custom-guards)를 내장하고 있어, 들어오는 요청의 액세스 토큰을 검증할 수 있습니다. `api` 가드를 `passport` 드라이버로 정상 설정했다면, 간단히 해당 라우트에 `auth:api` 미들웨어만 추가하면 됩니다:

```php
Route::get('/user', function () {
    // API 인증된 사용자만 이 라우트에 접근할 수 있습니다.
})->middleware('auth:api');
```

> [!WARNING]
> [클라이언트 자격 증명 그랜트](#client-credentials-grant)를 사용하는 경우, 반드시 [EnsureClientIsResourceOwner 미들웨어](#client-credentials-grant)로 라우트를 보호해야 하며, `auth:api` 미들웨어는 쓰지 않아야 합니다.

<a name="multiple-authentication-guards"></a>
#### 복수 인증 가드

만약 서로 다른 Eloquent 모델로 완전히 다른 사용자 유형 인증이 필요하다면, 각 User Provider 별로 가드 구성을 개별적으로 추가할 수 있습니다. 예를 들어, `config/auth.php`에 아래와 같이 guard를 정의했다면:

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

다음과 같이 `/customer` 라우트에 `auth:api-customers` 미들웨어를 사용하면, `customers` provider의 사용자만 인증할 수 있습니다:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport를 여러 User Provider와 함께 사용하는 법은 [퍼스널 액세스 토큰 문서](#customizing-the-user-provider-for-pat), [비밀번호 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달 (Passing the Access Token)

Passport로 보호된 라우트를 호출할 때, API 소비자는 요청의 `Authorization` 헤더에 `Bearer` 토큰 형식으로 액세스 토큰을 전달하면 됩니다. 예를 들어, `Http` 파사드를 사용하는 경우:

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

스코프는 API 클라이언트가 특정 액션만 할 수 있도록 권한을 제한할 수 있게 해줍니다. 예를 들어, 이커머스 앱에서 주문 생성 권한은 필요하지 않지만, 배송 상태 조회만 필요할 수도 있습니다. 즉, 스코프를 활용하면 사용자가 타사 애플리케이션에 허용할 수 있는 권한 범위를 세밀하게 제한할 수 있습니다.

<a name="defining-scopes"></a>
### 스코프 정의 (Defining Scopes)

API의 스코프는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `Passport::tokensCan` 메서드로 정의합니다. 스코프 이름과 설명(승인 화면에 보여줌)을 배열로 전달할 수 있습니다:

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

클라이언트가 특정 스코프를 요청하지 않으면, Passport 서버가 기본적으로 특정 스코프를 액세스 토큰에 지정할 수 있습니다. `defaultScopes` 메서드를 사용하면 되며, 보통 `boot` 메서드에서 함께 호출합니다:

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
#### 인증 코드 요청 시

인증 코드 그랜트로 액세스 토큰을 요청할 때, 소비자는 원하는 스코프를 `scope` 쿼리 파라미터(공백 구분)로 지정해야 합니다:

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
#### 퍼스널 액세스 토큰 발급 시

`App\Models\User` 모델의 `createToken` 사용 시, 두 번째 인자로 원하는 스코프 배열을 전달하면 됩니다:

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 확인 (Checking Scopes)

Passport는 특정 스코프가 부여된 토큰으로 인증되었는지 확인할 수 있는 두 개의 미들웨어를 제공합니다.

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어를 사용해, 들어오는 요청의 토큰에 지정된 모든 스코프가 있는지 확인할 수 있습니다:

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // "orders:read"와 "orders:create" 스코프가 모두 있어야 함...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create')]);
```

<a name="check-for-any-scopes"></a>
#### 하나 이상 스코프 확인

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어는 지정한 스코프 중 적어도 하나라도 있으면 허용합니다:

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // "orders:read" 또는 "orders:create" 중 하나라도 있으면 통과
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create')]);
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인

토큰으로 인증된 이후에도, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드로 개별 스코프를 확인할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('orders:create')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
#### 추가 스코프 관련 메서드

`scopeIds` 메서드는 정의된 모든 아이디/이름 배열을 반환합니다:

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

`scopes` 메서드는 정의된 모든 스코프를 `Laravel\Passport\Scope` 인스턴스 배열로 반환합니다:

```php
Passport::scopes();
```

`scopesFor` 메서드는 지정한 이름/아이디에 해당하는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다:

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

`hasScope` 메서드로 특정 스코프가 정의되었는지 여부를 판별할 수 있습니다:

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

API를 개발할 때, 자신의 자바스크립트 프론트엔드 애플리케이션에서 직접 API를 소비하는 것은 매우 유용합니다. 이 방식 덕분에 동일한 API를 웹앱, 모바일, 서드파티, SDK 등 다양한 환경에서 사용할 수 있습니다.

자바스크립트 앱에서 직접 액세스 토큰을 수동으로 전달하려면 불편할 수 있는데, Passport는 이를 자동화하는 미들웨어를 제공합니다. `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어를 추가(보통 `bootstrap/app.php`에서)만 하면 됩니다:

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어는 미들웨어 스택의 마지막에 위치해야 합니다.

이 미들웨어는 응답에 `laravel_token` 쿠키를 추가합니다. 이 쿠키에는 자바스크립트 앱의 API 요청을 인증하는 데 사용할 암호화된 JWT가 들어 있습니다(JWT의 만료 기간은 `session.lifetime` 설정값과 동일). 브라우저가 쿠키를 자동 전송하므로 토큰을 추가로 지정하지 않아도 인증이 가능합니다:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이징

필요하다면 Passport의 쿠키 이름을 `Passport::cookie`로 커스터마이징할 수 있습니다. 보통 이 코드는 `App\Providers\AppServiceProvider`의 `boot` 메서드에 작성합니다:

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

이 인증 방식을 사용할 때는 요청에 유효한 CSRF 토큰 헤더가 포함되어야 합니다. 라라벨의 기본 자바스크립트 스캐폴딩 및 모든 스타터 킷에는 [Axios](https://github.com/axios/axios) 인스턴스가 내장되어, 암호화된 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더로 자동 전송합니다.

> [!NOTE]
> 만약 `X-CSRF-TOKEN` 헤더를 사용하고 싶다면, 반드시 `csrf_token()`이 제공하는 _복호화되지 않은(unencrypted)_ 토큰을 사용해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

Passport는 액세스 토큰 발급 및 리프레시 토큰 발급 등 다양한 상황에서 이벤트를 발생시킵니다. [이벤트 리스너를 등록](/docs/12.x/events)하여 데이터베이스 내 다른 액세스 토큰을 정리(삭제/철회)할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                  |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## 테스트 (Testing)

Passport의 `actingAs` 메서드는 현재 인증된 사용자와 그 스코프를 지정해 테스트할 수 있게 해줍니다. 첫 번째 인자는 사용자 인스턴스, 두 번째 인자는 토큰에 부여할 스코프 배열입니다:

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

Passport의 `actingAsClient` 메서드는 현재 인증된 클라이언트와 그 스코프를 지정해 테스트할 수 있습니다. 첫 번째 인자는 클라이언트 인스턴스, 두 번째 인자는 토큰에 부여할 스코프 배열입니다:

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
