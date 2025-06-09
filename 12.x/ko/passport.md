# 라라벨 패스포트 (Laravel Passport)

- [소개](#introduction)
    - [패스포트와 Sanctum 중 어떤 것을 사용할까?](#passport-or-sanctum)
- [설치](#installation)
    - [패스포트 배포하기](#deploying-passport)
    - [패스포트 업그레이드하기](#upgrading-passport)
- [설정](#configuration)
    - [토큰 수명](#token-lifetimes)
    - [기본 모델 오버라이드](#overriding-default-models)
    - [라우트 오버라이드](#overriding-routes)
- [Authorization Code Grant](#authorization-code-grant)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청하기](#requesting-tokens)
    - [토큰 관리](#managing-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 취소](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [PKCE를 이용한 Authorization Code Grant](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청하기](#requesting-auth-pkce-grant-tokens)
- [Device Authorization Grant](#device-authorization-grant)
    - [Device Code Grant 클라이언트 생성](#creating-a-device-authorization-grant-client)
    - [토큰 요청하기](#requesting-device-authorization-grant-tokens)
- [Password Grant](#password-grant)
    - [Password Grant 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청하기](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [User Provider 커스터마이징](#customizing-the-user-provider)
    - [Username 필드 커스터마이징](#customizing-the-username-field)
    - [패스워드 검증 커스터마이징](#customizing-the-password-validation)
- [Implicit Grant](#implicit-grant)
- [Client Credentials Grant](#client-credentials-grant)
- [Personal Access Tokens](#personal-access-tokens)
    - [Personal Access Client 생성](#creating-a-personal-access-client)
    - [User Provider 커스터마이징](#customizing-the-user-provider-for-pat)
    - [Personal Access Tokens 관리](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어를 통한 보호](#via-middleware)
    - [Access Token 전달하기](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의하기](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당하기](#assigning-scopes-to-tokens)
    - [스코프 확인](#checking-scopes)
- [SPA 인증](#spa-authentication)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Passport](https://github.com/laravel/passport)는 여러분의 라라벨 애플리케이션에 몇 분 만에 완전한 OAuth2 서버 구현을 제공하는 패키지입니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server) 위에 구축되었습니다.

> [!NOTE]
> 이 문서는 독자가 이미 OAuth2에 익숙하다고 가정하고 작성되었습니다. 만약 OAuth2에 대해 전혀 모른다면, 계속 읽기 전에 [용어](https://oauth2.thephpleague.com/terminology/) 및 일반적인 OAuth2의 개념과 특징을 먼저 공부하시기를 추천합니다.

<a name="passport-or-sanctum"></a>
### 패스포트와 Sanctum 중 어떤 것을 사용할까?

시작하기 전에, 여러분의 애플리케이션에 Laravel Passport와 [Laravel Sanctum](/docs/12.x/sanctum) 중 어떤 것이 더 적합한지 결정하는 것이 좋습니다. 애플리케이션에서 반드시 OAuth2 지원이 필요한 경우에는 Laravel Passport를 사용해야 합니다.

하지만 단일 페이지 애플리케이션(SPA) 또는 모바일 애플리케이션 인증, 혹은 단순히 API 토큰을 발급하고 싶다면 [Laravel Sanctum](/docs/12.x/sanctum)을 사용하는 것이 좋습니다. Laravel Sanctum은 OAuth2를 지원하지 않지만, 훨씬 간단하게 API 인증 기능을 개발할 수 있도록 해줍니다.

<a name="installation"></a>
## 설치

라라벨 Passport는 `install:api` 아티즌 명령어를 통해 설치할 수 있습니다:

```shell
php artisan install:api --passport
```

이 명령어는 OAuth2 클라이언트와 액세스 토큰을 저장하는 데 필요한 데이터베이스 마이그레이션을 게시하고 실행합니다. 또한 보안 액세스 토큰 생성을 위한 암호화 키도 자동으로 생성합니다.

`install:api` 명령어 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가해야 합니다. 이 트레이트는 인증된 사용자의 토큰과 스코프를 확인할 수 있는 여러 헬퍼 메서드를 제공합니다:

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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고, `driver` 옵션을 `passport`로 설정해야 합니다. 이를 통해 API 요청 인증에 Passport의 `TokenGuard`를 사용하도록 지시할 수 있습니다:

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
### 패스포트 배포하기

애플리케이션 서버에 Passport를 처음 배포할 때는 `passport:keys` 명령어를 실행해야 할 경우가 많습니다. 이 명령어는 Passport가 액세스 토큰을 생성할 때 사용하는 암호화 키를 생성합니다. 이렇게 생성된 키는 보통 소스 컨트롤에는 포함시키지 않습니다:

```shell
php artisan passport:keys
```

필요하다면 Passport의 키를 불러올 경로를 직접 지정할 수도 있습니다. `Passport::loadKeysFrom` 메서드를 사용하면 됩니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출하면 됩니다:

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
#### 환경변수에서 키 불러오기

또는 `vendor:publish` 아티즌 명령어로 Passport의 설정 파일을 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일을 게시한 후에는, 아래와 같이 환경 변수로 암호화 키를 지정하여 키를 불러올 수 있습니다:

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="upgrading-passport"></a>
### 패스포트 업그레이드하기

Passport를 새로운 메이저 버전으로 업그레이드할 때에는, 반드시 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼하게 검토해야 합니다.

<a name="configuration"></a>
## 설정

<a name="token-lifetimes"></a>
### 토큰 수명

기본적으로 Passport는 1년 후 만료되는 장기간 유효한 액세스 토큰을 발급합니다. 토큰의 만료 시간을 더 길게 또는 더 짧게 조정하고 싶다면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 등의 메서드를 사용할 수 있습니다. 이런 설정은 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출해야 합니다:

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
> Passport의 데이터베이스 테이블에 있는 `expires_at` 컬럼은 읽기 전용이며 단순 표시 용도입니다. 실제 토큰 만료 정보는 서명 및 암호화된 액세스 토큰 내에 저장됩니다. 만약 토큰을 무효화(invalidate)해야 한다면 [토큰 폐기(취소, revoke)](#revoking-tokens)를 수행해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Passport 내부에서 사용하는 기본 모델을 자유롭게 확장할 수 있습니다. 직접 모델을 작성하고, 해당 모델이 Passport의 모델을 상속하도록 만드세요:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의했다면, Passport가 여러분이 만든 커스텀 모델을 사용하도록 `Laravel\Passport\Passport` 클래스에서 설정해야 합니다. 이 작업은 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에서 이뤄집니다:

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\DeviceCode;
use App\Models\Passport\RefreshToken;
use App\Models\Passport\Token;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::useTokenModel(Token::class);
    Passport::useRefreshTokenModel(RefreshToken::class);
    Passport::useAuthCodeModel(AuthCode::class);
    Passport::useClientModel(Client::class);
    Passport::useDeviceCodeModel(DeviceCode::class)
}
```

<a name="overriding-routes"></a>
### 라우트 오버라이드

Passport에서 기본으로 정의된 라우트를 커스터마이징하고 싶을 때도 있습니다. 이를 위해서는 먼저 Passport에서 등록하는 라우트를 무시하도록 `AppServiceProvider`의 `register` 메서드에 `Passport::ignoreRoutes`를 추가해야 합니다:

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

그 다음, [Passport의 라우트 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 여러분의 애플리케이션 `routes/web.php` 파일로 복사한 후 원하는 대로 수정하면 됩니다:

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
## Authorization Code Grant

가장 널리 사용되는 OAuth2 방식인 Authorization Code Grant(승인 코드 그랜트)는 개발자들이 OAuth2를 처음 배울 때 접하는 그 방식입니다. 이 방식에서는 클라이언트 앱이 사용자를 여러분의 서버로 리다이렉트하고, 사용자가 요청을 승인 또는 거부하면 클라이언트에 액세스 토큰을 발급합니다.

우선 Passport에게 우리가 사용할 "authorization(인가)" 뷰를 어떻게 반환할지 알려주어야 합니다.

Authorization 뷰의 렌더링 로직은 `Laravel\Passport\Passport` 클래스에서 제공하는 메서드로 원하는 대로 커스터마이징할 수 있습니다. 일반적으로 이 메서드는 여러분의 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 지정할 수 있습니다...
    Passport::authorizationView('auth.oauth.authorize');

    // 또는 클로저를 지정할 수도 있습니다...
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

Passport는 `/oauth/authorize` 라우트를 자동으로 정의하여 위에서 지정한 뷰를 반환합니다. 여러분의 `auth.oauth.authorize` 템플릿에는, 승인을 위해 `passport.authorizations.approve` 라우트로 POST 요청을 보내는 폼과, 거부를 위한 `passport.authorizations.deny` 라우트로 DELETE 요청을 보내는 폼이 포함되어야 합니다. 이 두 라우트 모두 `state`, `client_id`, `auth_token` 필드를 기대합니다.

<a name="managing-clients"></a>
### 클라이언트 관리

여러분의 애플리케이션 API와 연동하고 싶은 개발자들은, 그들의 앱(클라이언트)을 여러분의 서버에 등록해야 합니다. 보통, 클라이언트의 이름과 인가가 승인되었을 때 리다이렉트할 URI를 등록하게 됩니다.

<a name="managing-first-party-clients"></a>
#### 퍼스트 파티(자체) 클라이언트

클라이언트를 생성하는 가장 간단한 방법은 `passport:client` 아티즌 명령어를 사용하는 것입니다. 이 명령어는 퍼스트 파티(자체 개발/테스트용) 클라이언트뿐만 아니라 OAuth2 기능을 테스트할 때도 쓰입니다. `passport:client` 명령어를 실행하면, 클라이언트 관련 추가 정보를 입력하도록 안내하며, 클라이언트 ID와 시크릿을 제공합니다:

```shell
php artisan passport:client
```

클라이언트에 여러 개의 리다이렉트 URI를 허용하고 싶다면, 커맨드에서 URI 입력 시 콤마(,)로 구분하여 입력할 수 있습니다. 만약 콤마가 포함된 URI라면 URI 인코딩을 해주어야 합니다:

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 서드 파티(외부) 클라이언트

여러분의 애플리케이션 사용자가 `passport:client` 명령어를 사용할 수 없으므로, 지정한 사용자에게 `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드를 이용하여 클라이언트를 등록해줄 수 있습니다:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// 지정한 사용자에 소속된 OAuth 앱 클라이언트 생성...
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

`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. 사용자에게는 `$client->id`를 클라이언트 ID로, `$client->plainSecret`를 클라이언트 시크릿으로 안내할 수 있습니다.

<a name="requesting-tokens"></a>
### 토큰 요청하기

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인가(authorization) 요청을 위한 리다이렉트

클라이언트가 생성된 후, 개발자는 그들의 클라이언트 ID와 시크릿을 사용하여 여러분의 애플리케이션에서 인가 코드와 액세스 토큰을 요청할 수 있습니다. 우선, 서드 파티 애플리케이션은 아래와 같이 여러분 애플리케이션의 `/oauth/authorize` 라우트로 리다이렉트 요청을 보내야 합니다:

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

`prompt` 파라미터는 Passport 애플리케이션의 인증 방식 동작을 지정하는 데 사용할 수 있습니다.

- 만약 `prompt` 값이 `none`이라면, 사용자가 Passport 애플리케이션에 이미 인증되어 있지 않은 경우 무조건 인증 오류가 발생합니다.
- `consent`인 경우, 사용자가 이전에 모든 스코프에 대해 승인한 적이 있더라도 무조건 인가 화면이 표시됩니다.
- `login`이면, 세션이 남아 있더라도 무조건 재로그인이 요구됩니다.

`prompt` 값을 지정하지 않으면, 사용자가 해당 스코프의 접근을 최초로 승인하는 경우에만 인가 요청 화면이 표시됩니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 Passport에서 이미 정의되어 있으니, 따로 직접 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 요청 승인하기

Passport는 authorization 요청을 받을 때, (존재한다면) `prompt` 값에 따라 자동으로 응답하며, 사용자가 승인 또는 거부할 수 있는 템플릿을 보여줍니다. 사용자가 요청을 승인하면, 인가 때 지정한 `redirect_uri`로 리다이렉트됩니다. 이때, `redirect_uri`는 해당 클라이언트 생성 시 등록된 값과 일치해야 합니다.

퍼스트 파티(자체 애플리케이션) 클라이언트라서 승인 화면을 생략하고 싶을 수도 있습니다. 이럴 때에는 [Client 모델 오버라이드](#overriding-default-models)로 `skipsAuthorization` 메서드를 구현할 수 있습니다. 이 메서드가 `true`를 반환하면, 클라이언트는 자동으로 승인되고, 사용자는 인가 요청 시점에 특별히 `prompt` 파라미터를 명시하지 않은 이상 곧바로 `redirect_uri`로 이동합니다:

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 클라이언트가 인가 화면을 건너뛰어야 하는지 여부를 결정합니다.
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
#### 인가 코드를 액세스 토큰으로 교환하기

사용자가 인가 요청을 승인했다면, 지정한 `redirect_uri`로 리다이렉트됩니다. 소비하는 측 애플리케이션에서는 먼저 `state` 파라미터의 값이 리다이렉트 전에 저장했던 값과 일치하는지 확인해야 합니다. 일치한다면, 발급받은 인가코드를 포함하여 POST 방식으로 여러분의 애플리케이션에 액세스 토큰을 요청할 수 있습니다. 아래는 그 예시입니다:

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

`/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in`은 액세스 토큰 만료까지 남은 시간(초)을 나타냅니다.

> [!NOTE]
> `/oauth/authorize` 라우트와 마찬가지로 `/oauth/token` 라우트 또한 Passport에서 정의해 주므로, 따로 직접 라우트를 만들 필요가 없습니다.

<a name="managing-tokens"></a>
### 토큰 관리

`Laravel\Passport\HasApiTokens` 트레이트의 `tokens` 메서드를 사용하면 사용자가 승인한 토큰을 조회할 수 있습니다. 예를 들어, 사용자에게 서드 파티 애플리케이션 연결 내역 대시보드를 제공할 때 이 기능을 쓸 수 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 사용자의 유효한 토큰만 조회...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// 사용자가 연결한 서드 파티 OAuth 앱 클라이언트 목록...
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
### 토큰 갱신

여러분의 애플리케이션이 단기 수명의 액세스 토큰을 발급한다면, 사용자는 발급받았던 refresh token을 이용해 액세스 토큰을 갱신할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // confidential 클라이언트에서만 필수...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 `/oauth/token` 라우트 역시 `access_token`, `refresh_token`, `expires_in` 속성을 포함한 JSON 응답을 반환합니다. `expires_in`은 액세스 토큰 만료까지 남은 시간(초)을 담고 있습니다.

<a name="revoking-tokens"></a>
### 토큰 취소

`Laravel\Passport\Token` 모델의 `revoke` 메서드를 이용하여 액세스 토큰을 언제든지 취소할 수 있습니다. refresh token의 경우에는 `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드를 사용하면 됩니다:

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// 액세스 토큰 취소...
$token->revoke();

// 해당 토큰의 refresh token 취소...
$token->refreshToken?->revoke();

// 특정 사용자의 모든 토큰 취소...
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### 토큰 정리

토큰이 취소(폐기)되거나 만료되었다면, 데이터베이스에서 이를 정리하고 싶을 수 있습니다. Passport에는 이를 위한 `passport:purge` 아티즌 명령어가 포함되어 있습니다:

```shell
# 폐기 혹은 만료된 토큰, 인증 코드, 디바이스 코드를 모두 정리합니다...
php artisan passport:purge

# 6시간 이상 만료된 토큰만 정리합니다...
php artisan passport:purge --hours=6

# 취소(폐기)된 토큰, 인증 코드, 디바이스 코드만 정리합니다...
php artisan passport:purge --revoked

# 만료된 토큰, 인증 코드, 디바이스 코드만 정리합니다...
php artisan passport:purge --expired
```

애플리케이션의 `routes/console.php` 파일에서 [스케줄러 작업](/docs/12.x/scheduling)을 추가하여 자동으로 토큰을 정리하게 할 수도 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## PKCE를 이용한 Authorization Code Grant

"Proof Key for Code Exchange" (PKCE)를 적용한 Authorization Code Grant는 싱글 페이지 애플리케이션(SPA)이나 모바일 애플리케이션이 API를 보안적으로 인증할 수 있는 방식입니다. 이 방식은 클라이언트 시크릿 보호가 불가능하거나, 인가 코드가 공격자에게 탈취될 위험이 있는 상황에서 사용해야 합니다. 인가 코드를 액세스 토큰으로 교환할 때 클라이언트 시크릿 대신 "코드 검증자(code verifier)"와 "코드 챌린지(code challenge)" 쌍을 사용합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성

PKCE가 활성화된 클라이언트를 만들려면 `passport:client` 아티즌 명령어에 `--public` 옵션을 추가하여 실행하면 됩니다:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청하기

<a name="code-verifier-code-challenge"></a>
#### 코드 검증자(Code Verifier)와 코드 챌린지(Code Challenge)

이 인증 방식에서는 클라이언트 시크릿을 제공하지 않으므로, 토큰을 요청하려면 개발자가 직접 code verifier와 code challenge 조합을 생성해야 합니다.

code verifier는 RFC 7636 명세에 따라 알파벳, 숫자, 그리고 `"-"`, `"."`, `"_"`, `"~"` 문자를 포함한 43~128자의 랜덤 문자열이어야 합니다.

code challenge는 Base64로 인코딩되며, URL 및 파일 이름에 안전한 문자 조합으로 만들어야 하고, 마지막의 `'='` 문자는 제거해야 하며 줄바꿈, 공백 등은 없어야 합니다.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>

#### 인가를 위한 리다이렉트

클라이언트가 생성된 후, 클라이언트 ID와 생성한 코드 검증자(code verifier), 코드 챌린지(code challenge)를 사용해 애플리케이션에서 인가 코드 및 액세스 토큰을 요청할 수 있습니다. 먼저, 소비자 애플리케이션에서는 여러분 애플리케이션의 `/oauth/authorize` 경로로 리다이렉트 요청을 만들어야 합니다.

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
#### 인가 코드를 액세스 토큰으로 변환하기

만약 사용자가 인가 요청을 승인하면, 사용자는 소비자 애플리케이션으로 다시 리다이렉트됩니다. 소비자는 표준 Authorization Code Grant 방식과 동일하게 리다이렉트 전 저장한 `state` 값을 받아온 값과 비교해 검증해야 합니다.

`state` 파라미터가 일치한다면, 소비자는 애플리케이션에 액세스 토큰을 요청하기 위해 `POST` 요청을 보내야 합니다. 이 요청에는 사용자가 인가 요청을 승인할 때 발급받은 인가 코드와, 최초에 생성했던 코드 검증자가 포함되어야 합니다.

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
## 디바이스 인가(Authorization) 그랜트

OAuth2 디바이스 인가 그랜트는 TV나 게임 콘솔 등 브라우저 없이 입력이 제한된 장치에서 "디바이스 코드"를 교환하여 액세스 토큰을 받을 수 있도록 해줍니다. 디바이스 플로우를 사용할 때 디바이스 클라이언트는 사용자에게 다른 기기(예: 컴퓨터나 스마트폰)를 이용해 제공된 "사용자 코드(user code)"를 입력하고, 인가 요청을 승인 또는 거부하도록 안내합니다.

먼저, Passport에 "사용자 코드(user code)"와 "인가(authorization)" 뷰를 반환하는 방법을 알려주어야 합니다.

모든 인가 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스에서 제공하는 적절한 메서드를 이용해 커스터마이즈할 수 있습니다. 보통은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에서 이 메서드들을 호출합니다.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 직접 지정할 수도 있습니다...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // 클로저를 지정하여 렌더링할 수도 있습니다...
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

Passport는 자동으로 이 뷰들을 반환하는 라우트를 정의합니다. `auth.oauth.device.user-code` 템플릿에는 `passport.device.authorizations.authorize` 라우트로 GET 요청을 보내는 폼이 포함되어야 합니다. 이 라우트는 `user_code` 쿼리 파라미터를 기대합니다.

`auth.oauth.device.authorize` 템플릿에는 인가를 승인하는 POST 요청 폼(`passport.device.authorizations.approve` 라우트)과, 인가를 거부하는 DELETE 요청 폼(`passport.device.authorizations.deny` 라우트)이 모두 포함되어야 합니다. 두 라우트 모두 `state`, `client_id`, `auth_token` 필드를 요구합니다.

<a name="creating-a-device-authorization-grant-client"></a>
### 디바이스 인가 그랜트 클라이언트 만들기

애플리케이션에서 디바이스 인가 그랜트를 통해 토큰을 발급하려면, 디바이스 플로우가 활성화된 클라이언트를 생성해야 합니다. `--device` 옵션을 사용하여 `passport:client` Artisan 명령어로 이를 생성할 수 있습니다. 이 명령어는 1st-party(1자) 디바이스 플로우 클라이언트를 생성하고, 클라이언트 ID와 시크릿을 제공합니다.

```shell
php artisan passport:client --device
```

또한, `ClientRepository` 클래스의 `createDeviceAuthorizationGrantClient` 메서드를 사용해 특정 사용자에게 속한 3rd-party(3자) 디바이스 클라이언트를 등록할 수도 있습니다.

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
### 토큰 요청

<a name="device-code"></a>
#### 디바이스 코드 요청하기

클라이언트가 생성되면, 개발자는 해당 클라이언트 ID를 사용해 애플리케이션에서 디바이스 코드를 요청할 수 있습니다. 우선, 소비자 디바이스에서는 `/oauth/device/code` 경로에 `POST` 요청을 보내 디바이스 코드를 요청해야 합니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 요청은 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in`은 디바이스 코드가 만료되기까지의 초(second) 수이며, `interval`은 디바이스가 `/oauth/token` 경로를 폴링할 때(지속적으로 상태를 체크할 때) 얼마나 기다려야 하는지(초 단위) 나타냅니다. 이는 레이트 리밋(ratelimit) 오류를 피하기 위해 필요합니다.

> [!NOTE]
> `/oauth/device/code` 경로는 Passport에서 이미 정의되어 있습니다. 별도로 이 라우트를 직접 추가할 필요가 없습니다.

<a name="user-code"></a>
#### 인증 URI와 사용자 코드 표시하기

디바이스 코드 요청을 받은 후, 소비자 디바이스는 사용자가 다른 장치를 이용해 `verification_uri`에 방문하여 `user_code`를 입력하도록 안내해야 합니다. 사용자는 이 과정을 통해 인가 요청을 승인할 수 있습니다.

<a name="polling-token-request"></a>
#### 토큰 요청 폴링

사용자가 별도의 장치로 접근 권한을 승인(또는 거부)하기 때문에, 소비자 디바이스에서는 사용자가 응답을 완료했는지 알기 위해 애플리케이션의 `/oauth/token` 경로를 주기적으로 폴링해야 합니다. 폴링 간격은 디바이스 코드 요청 시 받은 JSON 응답의 `interval` 값을 최소값으로 적용해, 레이트 리밋 오류를 방지해야 합니다.

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // Required for confidential clients only...
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

만약 사용자가 인가 요청을 승인하면, 위 요청은 `access_token`, `refresh_token`, `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in`은 액세스 토큰이 만료되기까지의 초 수입니다.

<a name="password-grant"></a>
## 패스워드 그랜트(Password Grant)

> [!WARNING]
> 더 이상 패스워드 그랜트 토큰 사용을 권장하지 않습니다. 대신 [OAuth2 서버에서 현재 권장되는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/) 중 하나를 사용하시기 바랍니다.

OAuth2 패스워드 그랜트는 모바일 애플리케이션과 같은 다른 1st-party 클라이언트가 이메일 주소/사용자명과 비밀번호를 이용해 액세스 토큰을 받을 수 있게 해줍니다. 이 방식은 전체 OAuth2 인가 코드 리다이렉트 플로우 없이도 1st-party 클라이언트에 안전하게 액세스 토큰을 발급할 수 있습니다.

패스워드 그랜트를 활성화하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 `enablePasswordGrant` 메서드를 호출하세요.

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
### 패스워드 그랜트 클라이언트 생성

패스워드 그랜트를 통해 토큰을 발급하려면 우선 패스워드 그랜트 클라이언트를 생성해야 합니다. 이는 `--password` 옵션을 사용한 `passport:client` Artisan 명령어로 할 수 있습니다.

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청

그랜트를 활성화하고 클라이언트를 생성했다면, 사용자의 이메일 주소와 비밀번호를 포함하여 `/oauth/token` 경로에 `POST` 요청해 액세스 토큰을 신청할 수 있습니다. 이 라우트는 Passport가 이미 등록해두었으므로 별도 등록은 불필요합니다. 요청에 성공하면, 서버에서 `access_token`과 `refresh_token`이 포함된 JSON 응답을 받을 수 있습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

> [!NOTE]
> 액세스 토큰은 기본적으로 유효기간이 깁니다. 하지만 필요하다면 [최대 액세스 토큰 유효기간을 직접 설정](#configuration)할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청하기

패스워드 그랜트 또는 클라이언트 크레덴셜 그랜트 사용 시, 애플리케이션에서 지원하는 모든 스코프에 대한 토큰을 발급받고 싶을 때도 있습니다. 이럴 땐 `*` 스코프를 요청하시면 됩니다. `*` 스코프가 부여된 토큰의 `can` 메서드는 항상 `true`를 반환합니다. 이 스코프는 오직 `password` 또는 `client_credentials` 그랜트로 발급된 토큰에만 할당할 수 있습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### 사용자 프로바이더 커스터마이징

애플리케이션에 [사용자 인증 프로바이더](/docs/12.x/authentication#introduction)가 여러 개 있을 때, `artisan passport:client --password` 명령어로 클라이언트를 생성하면서 `--provider` 옵션을 지정해 패스워드 그랜트 클라이언트가 사용할 사용자 프로바이더를 지정할 수 있습니다. 이때 지정하는 프로바이더 이름은 애플리케이션의 `config/auth.php`의 유효한 프로바이더와 일치해야 합니다. 이후 [미들웨어를 사용해 라우트를 보호](#multiple-authentication-guards)함으로써 특정 가드에서 허용하는 사용자만 접근할 수 있도록 할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명 필드 커스터마이징

패스워드 그랜트를 이용해 인증할 때, Passport는 인증 가능한 모델의 `email` 속성을 사용자명으로 사용합니다. 하지만, 모델에서 `findForPassport` 메서드를 정의해 이 동작을 커스터마이즈할 수 있습니다.

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
     * Find the user instance for the given username.
     */
    public function findForPassport(string $username): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### 비밀번호 검증 커스터마이징

패스워드 그랜트로 인증할 때, Passport는 모델의 `password` 속성을 이용해 비밀번호를 검증합니다. 만약 모델에 `password` 속성이 없거나, 비밀번호 검증 로직을 직접 만들고 싶다면, 모델에 `validateForPassportPasswordGrant` 메서드를 정의할 수 있습니다.

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
     * Validate the password of the user for the Passport password grant.
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant"></a>
## 임플리시트 그랜트(Implicit Grant)

> [!WARNING]
> 더 이상 임플리시트 그랜트 토큰 사용을 권장하지 않습니다. 대신 [OAuth2 서버에서 현재 권장되는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/) 중 하나를 사용하시기 바랍니다.

임플리시트 그랜트는 인가 코드 그랜트와 비슷하지만, 토큰이 인가 코드 교환 없이 클라이언트로 반환된다는 차이가 있습니다. 이 방식은 자바스크립트나 모바일 애플리케이션처럼 클라이언트 크레덴셜을 안전하게 저장하기 어려운 환경에서 많이 사용됩니다. 임플리시트 그랜트를 활성화하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enableImplicitGrant` 메서드를 호출하면 됩니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

임플리시트 그랜트 토큰을 발급하려면, 먼저 임플리시트 그랜트 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령어에 `--implicit` 옵션을 사용해 생성할 수 있습니다.

```shell
php artisan passport:client --implicit
```

그랜트가 활성화되고 임플리시트 클라이언트가 생성되면, 개발자는 클라이언트 ID를 이용해 액세스 토큰을 요청할 수 있습니다. 소비자 애플리케이션은 다음과 같이 여러분 애플리케이션의 `/oauth/authorize` 경로로 리다이렉트 요청을 만들어야 합니다.

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
> `/oauth/authorize` 경로는 Passport에서 이미 정의되어 있습니다. 별도로 추가할 필요가 없습니다.

<a name="client-credentials-grant"></a>
## 클라이언트 크레덴셜 그랜트(Client Credentials Grant)

클라이언트 크레덴셜 그랜트는 서버 간 인증(machine-to-machine authentication)에 적합합니다. 예를 들어, 예약된 작업이 API를 통해 유지관리 작업 등을 실행할 때 이 방식을 사용할 수 있습니다.

클라이언트 크레덴셜 그랜트 토큰을 발급하려면, 먼저 클라이언트 크레덴셜 그랜트 클라이언트를 만들어야 합니다. 이를 위해 `passport:client` Artisan 명령어에 `--client` 옵션을 사용하세요.

```shell
php artisan passport:client --client
```

그 다음, `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 라우트에 할당해야 합니다.

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하고, 클라이언트가 리소스 소유자인 경우 실행됩니다...
})->middleware(EnsureClientIsResourceOwner::class);
```

특정 스코프를 가진 접근만 허용하고자 한다면, `using` 메서드에 필요한 스코프 목록을 전달할 수 있습니다.

```php
Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하고, 리소스 소유자인 클라이언트가 "servers:read"와 "servers:create" 두 가지 스코프를 모두 가지고 있는 경우 실행됩니다...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create');
```

<a name="retrieving-tokens"></a>
### 토큰 가져오기

이 그랜트 타입을 사용해 토큰을 받으려면, `oauth/token` 엔드포인트로 요청을 보내세요.

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
## 개인 액세스 토큰(Personal Access Tokens)

경우에 따라 사용자가 일반 OAuth2 인가 코드 리다이렉트 플로우를 거치지 않고, 직접 액세스 토큰을 발급받고 싶을 수도 있습니다. 애플리케이션의 UI를 통해 사용자가 자기 자신에게 토큰을 발급할 수 있게 하면, API를 실험할 때 매우 유용하며, 전체적으로 액세스 토큰 발급 과정을 단순화할 수 있습니다.

> [!NOTE]
> 애플리케이션이 주로 개인 액세스 토큰 발급을 위해 Passport를 사용하는 경우, 라라벨의 경량 API 토큰 발급 라이브러리인 [Laravel Sanctum](/docs/12.x/sanctum) 사용도 고려해볼 수 있습니다.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성

개인 액세스 토큰을 발급하려면 우선 개인 액세스 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령어에 `--personal` 옵션을 붙여 실행하면 됩니다. 만약 `passport:install` 명령어를 이미 실행했다면 이 명령어는 다시 실행할 필요가 없습니다.

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### 사용자 프로바이더 커스터마이징

애플리케이션이 [여러 사용자 인증 프로바이더](/docs/12.x/authentication#introduction)를 사용한다면, `artisan passport:client --personal` 명령어로 클라이언트를 생성할 때 `--provider` 옵션을 사용해 개인 액세스 그랜트 클라이언트가 사용할 프로바이더를 지정할 수 있습니다. 지정한 프로바이더명은 `config/auth.php`에 정의된 유효한 프로바이더와 일치해야 합니다. 이후 [미들웨어로 라우트를 보호](#multiple-authentication-guards)해, 가드에서 정한 프로바이더에 속한 사용자만 접근하도록 할 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리

개인 액세스 클라이언트를 생성한 후에는, `App\Models\User` 모델 인스턴스의 `createToken` 메서드로 해당 사용자에 대한 토큰을 발급할 수 있습니다. `createToken` 메서드는 첫 번째 인자로 토큰 이름, 두 번째 인자로 [스코프](#token-scopes) 배열(선택 사항)을 받습니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 스코프 없이 토큰 생성...
$token = $user->createToken('My Token')->accessToken;

// 스코프를 지정하여 토큰 생성...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// 모든 스코프를 가진 토큰 생성...
$token = $user->createToken('My Token', ['*'])->accessToken;

// 해당 사용자에게 속한 모든 유효한 개인 액세스 토큰 조회...
$tokens = $user->tokens()
    ->with('client')
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get()
    ->filter(fn (Token $token) => $token->client->hasGrantType('personal_access'));
```

<a name="protecting-routes"></a>
## 라우트 보호하기

<a name="via-middleware"></a>
### 미들웨어를 이용한 보호

Passport는 들어오는 요청의 액세스 토큰을 검증할 수 있는 [인증 가드](/docs/12.x/authentication#adding-custom-guards)를 제공합니다. `api` 가드를 `passport` 드라이버로 설정했다면, 유효한 액세스 토큰이 필요한 모든 라우트에 `auth:api` 미들웨어만 지정하면 됩니다.

```php
Route::get('/user', function () {
    // API 인증된 사용자만 접근할 수 있는 라우트...
})->middleware('auth:api');
```

> [!WARNING]
> [클라이언트 크레덴셜 그랜트](#client-credentials-grant)를 사용하는 경우, 라우트 보호에 `auth:api` 미들웨어 대신 [Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner 미들웨어](#client-credentials-grant)를 사용해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 다중 인증 가드 사용

서로 다른 타입의 사용자를 별도의 Eloquent 모델로 인증해야 하는 경우, 사용자 프로바이더별로 가드 구성을 각각 정의할 수 있습니다. 이를 통해 특정 사용자 프로바이더에만 요청을 허용할 수 있습니다. 아래는 `config/auth.php` 파일에 정의한 예시입니다.

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

다음 라우트는 `api-customers` 가드를 사용하므로, `customers` 사용자 프로바이더를 통해 인증된 요청만 허용합니다.

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport에서 여러 사용자 프로바이더를 사용하는 방법에 대해 더 자세히 알고 싶다면 [개인 액세스 토큰 문서](#customizing-the-user-provider-for-pat)와 [패스워드 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달

Passport로 보호되는 라우트에 호출할 때에는, API 소비자가 요청의 `Authorization` 헤더에 `Bearer` 토큰 방식으로 액세스 토큰을 명시해야 합니다. 예를 들어, `Http` 파사드를 사용할 때 다음과 같이 할 수 있습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => "Bearer $accessToken",
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
## 토큰 스코프(Token Scopes)

스코프(scope)를 사용하면, API 클라이언트가 계정 접근 권한을 요청할 때 허용 받고자 하는 권한(기능)에 따라 세부적으로 요청을 제어할 수 있습니다. 예를 들어, 전자상거래 애플리케이션의 경우 모든 API 소비자가 주문 생성 권한이 필요하지 않을 수 있습니다. 대신, 소비자에게 주문 배송 상태만 조회하는 권한만 요청하도록 제한할 수 있습니다. 즉, 스코프 사용으로 서드파티 애플리케이션이 자신을 대신해 할 수 있는 행동의 범위를 사용자가 직접 통제하게 할 수 있습니다.

<a name="defining-scopes"></a>
### 스코프 정의하기

API의 스코프는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 `Passport::tokensCan` 메서드로 정의할 수 있습니다. 이 메서드는 스코프 이름과 스코프 설명을 담은 배열을 받습니다. 스코프 설명은 자유롭게 지정할 수 있고, 인가 화면에서 사용자에게 보여집니다.

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

### 기본 스코프(Default Scope)

클라이언트가 별도의 스코프를 요청하지 않았을 때, `defaultScopes` 메서드를 사용해 해당 토큰에 기본 스코프를 자동으로 부여할 수 있습니다. 이 메서드는 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내의 `boot` 메서드에서 호출해야 합니다.

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
### 토큰에 스코프 할당하기

<a name="when-requesting-authorization-codes"></a>
#### 인가 코드 요청 시

인가 코드(grant)를 사용해서 액세스 토큰을 요청할 때, 클라이언트는 `scope` 쿼리 스트링 파라미터에 원하는 스코프를 지정할 수 있습니다. `scope` 파라미터에는 스코프들을 공백으로 구분해서 나열해야 합니다.

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
#### 개인 액세스 토큰 발급 시

`App\Models\User` 모델의 `createToken` 메서드를 사용해 개인 액세스 토큰을 발급할 때, 두 번째 인수로 원하는 스코프의 배열을 전달할 수 있습니다.

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 확인하기

Passport는 인증된 요청의 토큰이 지정한 스코프를 가지고 있는지 검증할 수 있도록 두 가지 미들웨어를 제공합니다.

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어를 라우트에 할당하면, 접근한 액세스 토큰이 지정한 모든 스코프를 가지고 있는지 확인할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // Access token has both "orders:read" and "orders:create" scopes...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create');
```

<a name="check-for-any-scopes"></a>
#### 하나 이상의 스코프 확인

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어를 라우트에 할당하면, 액세스 토큰에 지정한 *하나 이상의* 스코프가 존재하는지 확인합니다.

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // Access token has either "orders:read" or "orders:create" scope...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create');
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인

액세스 토큰이 인증된 요청이 애플리케이션에 들어온 이후, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드를 통해 토큰에 특정 스코프가 포함되어 있는지 추가로 확인할 수 있습니다.

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

`scopeIds` 메서드는 정의된 모든 ID/이름의 배열을 반환합니다.

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

`scopes` 메서드는 정의된 모든 스코프를 `Laravel\Passport\Scope` 인스턴스들의 배열로 반환합니다.

```php
Passport::scopes();
```

`scopesFor` 메서드는, 주어진 ID/이름에 해당하는 `Laravel\Passport\Scope` 인스턴스들의 배열을 반환합니다.

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

특정 스코프가 정의되어 있는지를 확인하려면 `hasScope` 메서드를 사용할 수 있습니다.

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA 인증

API를 만들 때, 직접 만든 자바스크립트 애플리케이션에서 자신의 API를 소비할 수 있다는 점은 매우 유용합니다. 이런 방식으로 API를 개발하면, 웹 애플리케이션, 모바일 앱, 타사 애플리케이션, 다양한 패키지 매니저를 통해 배포하는 SDK 등에서 동일한 API를 모두 활용할 수 있습니다.

일반적으로 자바스크립트 애플리케이션에서 API를 사용하고자 할 때, 별도로 애플리케이션에 액세스 토큰을 전달하고, 각 요청마다 토큰을 함께 전송해야 합니다. 그러나 Passport에는 이러한 번거로움을 대신 처리해주는 미들웨어가 포함되어 있습니다. `bootstrap/app.php` 파일에서 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어를 추가해주기만 하면 됩니다.

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어는 반드시 미들웨어 스택의 맨 마지막에 위치해야 합니다.

이 미들웨어는 응답에 `laravel_token` 쿠키를 추가합니다. 이 쿠키에는 암호화된 JWT가 포함되어 있는데, Passport가 자바스크립트 애플리케이션에서 오는 API 요청을 인증하는 데 사용됩니다. 이 JWT의 라이프사이클은 `session.lifetime` 설정값과 동일합니다. 브라우저는 다음 요청부터 이 쿠키를 자동으로 요청에 포함해서 보내므로, 액세스 토큰을 별도로 넘기지 않아도 API 요청이 가능합니다.

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이즈

필요하다면 `Passport::cookie` 메서드를 사용해 `laravel_token` 쿠키의 이름을 원하는 값으로 바꿀 수 있습니다. 이 메서드도 마찬가지로 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출하는 것이 일반적입니다.

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

이 인증 방식을 사용할 때는 요청에 올바른 CSRF 토큰 헤더가 포함되어 있는지 반드시 확인해야 합니다. 라라벨의 스켈레톤 애플리케이션 및 모든 스타터 키트에 포함된 기본 자바스크립트 구성에서는 [Axios](https://github.com/axios/axios) 인스턴스가 `XSRF-TOKEN` 쿠키의 암호화된 값을 이용해, 동일 출처 요청(same-origin)에 대해 자동으로 `X-XSRF-TOKEN` 헤더를 전송합니다.

> [!NOTE]
> 만약 `X-XSRF-TOKEN` 대신 `X-CSRF-TOKEN` 헤더를 직접 전송하고 싶다면, 반드시 `csrf_token()`이 제공하는 암호화되지 않은 값을 사용해야 합니다.

<a name="events"></a>
## 이벤트

Passport는 액세스 토큰 또는 리프레시 토큰을 발급/폐기할 때 이벤트를 발생시킵니다. [이벤트를 리스닝](/docs/12.x/events)하여 데이터베이스 내의 다른 액세스 토큰을 정리하거나 폐기하는 등의 처리를 구현할 수 있습니다.

<div class="overflow-auto">

| 이벤트 이름                                      |
| ------------------------------------------------ |
| `Laravel\Passport\Events\AccessTokenCreated`     |
| `Laravel\Passport\Events\AccessTokenRevoked`     |
| `Laravel\Passport\Events\RefreshTokenCreated`    |

</div>

<a name="testing"></a>
## 테스트

Passport의 `actingAs` 메서드는 현재 인증된 사용자와 부여할 스코프를 지정하는 데 사용할 수 있습니다. 첫 번째 인수는 사용자 인스턴스이며, 두 번째 인수는 토큰에 부여할 스코프 배열입니다.

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

또한 Passport의 `actingAsClient` 메서드는 현재 인증된 클라이언트 및 그 토큰에 부여할 스코프를 지정할 때 사용할 수 있습니다. 첫 번째 인수는 클라이언트 인스턴스이고, 두 번째 인수는 클라이언트의 토큰에 부여할 스코프 배열입니다.

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