# 라라벨 패스포트 (Laravel Passport)

- [소개](#introduction)
    - [패스포트 또는 생텀?](#passport-or-sanctum)
- [설치](#installation)
    - [패스포트 배포](#deploying-passport)
    - [패스포트 업그레이드](#upgrading-passport)
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
- [PKCE가 적용된 인증 코드 그랜트](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청](#requesting-auth-pkce-grant-tokens)
- [디바이스 인증 그랜트](#device-authorization-grant)
    - [디바이스 코드 그랜트 클라이언트 생성](#creating-a-device-authorization-grant-client)
    - [토큰 요청](#requesting-device-authorization-grant-tokens)
- [패스워드 그랜트](#password-grant)
    - [패스워드 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [User Provider 커스터마이징](#customizing-the-user-provider)
    - [Username 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 커스터마이징](#customizing-the-password-validation)
- [암시적(Implicit) 그랜트](#implicit-grant)
- [클라이언트 크레덴셜 그랜트](#client-credentials-grant)
- [퍼스널 액세스 토큰](#personal-access-tokens)
    - [퍼스널 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [User Provider 커스터마이징](#customizing-the-user-provider-for-pat)
    - [퍼스널 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어로 보호하기](#via-middleware)
    - [액세스 토큰 전달 방법](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당](#assigning-scopes-to-tokens)
    - [스코프 확인](#checking-scopes)
- [SPA 인증](#spa-authentication)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Passport](https://github.com/laravel/passport)는 여러분의 라라벨 애플리케이션에 몇 분 만에 완전한 OAuth2 서버 기능을 제공하는 솔루션입니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server)를 기반으로 만들어졌습니다.

> [!NOTE]
> 이 문서는 여러분이 이미 OAuth2에 익숙하다고 가정합니다. 만약 OAuth2에 대해 아는 것이 없다면, 계속 읽기 전에 [용어](https://oauth2.thephpleague.com/terminology/) 및 OAuth2의 기본적인 개념을 먼저 익혀보시기 바랍니다.

<a name="passport-or-sanctum"></a>
### 패스포트 또는 생텀?

시작에 앞서, 여러분의 애플리케이션에 Laravel Passport와 [Laravel Sanctum](/docs/12.x/sanctum) 중 어떤 것이 더 적합한지 결정하는 것이 좋습니다. 만약 반드시 OAuth2를 지원해야 하는 애플리케이션이라면 Laravel Passport를 사용해야 합니다.

반면, 싱글 페이지 애플리케이션(SPA)이나 모바일 앱, 또는 API 토큰 발급이 필요한 경우에는 [Laravel Sanctum](/docs/12.x/sanctum)을 사용하는 것이 더 좋습니다. Laravel Sanctum은 OAuth2를 지원하지 않지만, 훨씬 간단한 방식으로 API 인증 기능을 개발할 수 있습니다.

<a name="installation"></a>
## 설치

라라벨 Passport는 `install:api` 아티즌 명령어를 통해 설치할 수 있습니다.

```shell
php artisan install:api --passport
```

이 명령어는 OAuth2 클라이언트와 액세스 토큰을 저장하기 위한 테이블을 생성하는 데 필요한 데이터베이스 마이그레이션을 발행 및 실행합니다. 또한, 보안 액세스 토큰 생성을 위한 암호화 키도 생성해줍니다.

`install:api` 명령을 실행한 후에는, 여러분의 `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가해야 합니다. 이 트레이트는 인증된 사용자의 토큰과 스코프를 확인할 수 있는 여러 보조 메서드를 제공합니다.

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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고 `driver` 옵션을 반드시 `passport`로 변경해야 합니다. 이를 통해 들어오는 API 요청에 대해 패스포트의 `TokenGuard`를 사용하도록 지시할 수 있습니다.

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
### 패스포트 배포

서버 환경에 애플리케이션을 처음 배포할 때는, `passport:keys` 명령어를 실행해야 합니다. 이 명령은 패스포트가 액세스 토큰을 발급할 때 필요한 암호화 키를 생성합니다. 생성된 키 파일은 일반적으로 소스 관리에 포함시키지 않습니다.

```shell
php artisan passport:keys
```

필요하다면, 패스포트가 키 파일을 불러올 위치를 직접 지정할 수도 있습니다. `Passport::loadKeysFrom` 메서드를 사용하여 경로를 설정할 수 있으며, 보통 이 코드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

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

또는, `vendor:publish` 아티즌 명령어를 사용해 패스포트의 설정 파일을 발행할 수 있습니다.

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일이 발행된 후에는, 환경 변수로 애플리케이션의 암호화 키를 지정하여 사용할 수 있습니다.

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="upgrading-passport"></a>
### 패스포트 업그레이드

Passport의 새 메이저 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 주의 깊게 검토해야 합니다.

<a name="configuration"></a>
## 설정

<a name="token-lifetimes"></a>
### 토큰 만료 기간

기본적으로 Passport는 1년 후에 만료되는 장기 액세스 토큰을 발급합니다. 토큰 만료 기간을 더 길게 또는 짧게 설정하고 싶다면 `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에서 호출해야 합니다.

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
> Passport의 데이터베이스 테이블 내 `expires_at` 컬럼은 읽기 전용이며, 오직 표시용으로만 사용됩니다. 토큰을 발급할 때, 패스포트는 만료 정보를 서명되고 암호화된 토큰 내부에 저장합니다. 토큰을 무효화해야 한다면 [토큰을 철회(revoke)](#revoking-tokens)해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

패스포트에서 내부적으로 사용하는 모델을 자유롭게 확장해 사용할 수 있습니다. 여러분의 모델을 정의하고 Passport 모델을 확장하면 됩니다.

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의한 후에는, `Laravel\Passport\Passport` 클래스를 통해 커스텀 모델을 사용하도록 패스포트에 알려야 합니다. 이 설정 또한 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 해주어야 합니다.

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

가끔 필요에 따라 패스포트가 등록하는 라우트를 커스터마이징하고 싶을 수 있습니다. 이럴 때에는 먼저, 애플리케이션의 `AppServiceProvider`의 `register` 메서드에서 `Passport::ignoreRoutes`를 호출하여 패스포트의 기본 라우트 등록을 무시해야 합니다.

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

그 다음, [패스포트의 라우트 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 애플리케이션의 `routes/web.php` 파일로 복사한 후, 원하는 대로 수정하면 됩니다.

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
## 인증 코드 그랜트

OAuth2 인증 코드 방식은 대부분의 개발자가 익숙하게 사용하는 OAuth2 플로우입니다. 인증 코드를 사용하는 경우, 클라이언트 애플리케이션은 사용자를 서버로 리디렉션하여 액세스 토큰 발급 요청을 승인하거나 거부하게 만듭니다.

우선, 패스포트가 "authorization" 뷰를 반환하는 방식을 알려주어야 합니다.

모든 authorization 뷰의 렌더링 로직은 `Laravel\Passport\Passport` 클래스에서 제공하는 적절한 메서드로 커스터마이징할 수 있습니다. 보통 이 로직 역시 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 작성합니다.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 직접 지정하는 방법...
    Passport::authorizationView('auth.oauth.authorize');
    
    // 클로저를 전달하는 방법...
    Passport::authorizationView(fn ($parameters) => Inertia::render('Auth/OAuth/Authorize', [
        'request' => $parameters['request'],
        'authToken' => $parameters['authToken'],
        'client' => $parameters['client'],
        'user' => $parameters['user'],
        'scopes' => $parameters['scopes'],
    ]));
}
```

패스포트는 자동으로 이 뷰를 반환하는 `/oauth/authorize` 라우트를 정의합니다. 여러분의 `auth.oauth.authorize` 템플릿에는 인증 요청을 승인할 때 `passport.authorizations.approve` 라우트로 POST 요청을 보내는 폼과, 인증 요청을 거부할 때 `passport.authorizations.deny` 라우트로 DELETE 요청을 보내는 폼이 포함되어야 합니다. 이때 두 라우트는 `state`, `client_id`, `auth_token` 필드를 요구합니다.

<a name="managing-clients"></a>
### 클라이언트 관리

애플리케이션의 API와 상호작용해야 하는 외부 애플리케이션 개발자들은 자신의 애플리케이션을 "클라이언트"로 등록해야 합니다. 일반적으로 등록 과정에서 애플리케이션의 이름과, 인증이 승인된 후 사용할 리디렉트 URI를 입력받습니다.

<a name="managing-first-party-clients"></a>
#### 1st Party(자사) 클라이언트

가장 간단하게 클라이언트를 생성하려면 `passport:client` 아티즌 명령어를 사용할 수 있습니다. 이 명령어는 자체 애플리케이션을 위한 클라이언트이거나 OAuth2 기능을 테스트할 때에도 사용할 수 있습니다. 실행하면, 패스포트가 클라이언트 관련 정보를 입력받고, 클라이언트 ID와 시크릿 값을 제공해줍니다.

```shell
php artisan passport:client
```

한 클라이언트에 대해 여러 개의 리디렉트 URI를 허용하려면, `passport:client` 명령어에서 URI를 입력할 때 콤마로 구분해 여러 URI를 입력할 수 있습니다. URI에 콤마(,) 문자가 포함되어 있다면 URI 인코딩 처리해야 합니다.

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 3rd Party(타사) 클라이언트

외부 개발자는 `passport:client` 명령어를 직접 사용할 수 없으므로, `Laravel\Passport\ClientRepository`의 `createAuthorizationCodeGrantClient` 메서드를 통해서 특정 사용자에게 클라이언트를 등록해줄 수 있습니다.

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// 지정된 사용자 소유의 OAuth 앱 클라이언트 생성...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// 해당 사용자가 소유한 모든 OAuth 앱 클라이언트 조회...
$clients = $user->oauthApps()->get();
```

`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. 사용자에게 클라이언트 ID로 `$client->id`, 시크릿 값으로 `$client->plainSecret`을 안내하면 됩니다.

<a name="requesting-tokens"></a>
### 토큰 요청

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인증을 위한 리디렉션

클라이언트가 생성되면, 개발자는 클라이언트 ID와 시크릿을 사용하여 인증 코드와 액세스 토큰을 요청할 수 있습니다. 먼저, 클라이언트 애플리케이션은 여러분의 애플리케이션의 `/oauth/authorize` 라우트로 리디렉션 요청을 보내야 합니다.

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

`prompt` 파라미터는 패스포트 애플리케이션의 인증 동작 방식을 지정하는 용도로 사용할 수 있습니다.

만약 `prompt` 값이 `none`이라면, 사용자가 이미 패스포트 애플리케이션에 인증되어 있지 않은 경우 무조건 인증 에러가 발생합니다. 값이 `consent`이면, 이전에 모든 스코프를 승인했더라도 항상 인증 승인 화면을 표시하게 됩니다. `login`이면, 사용자가 이미 세션이 있더라도 애플리케이션에 다시 로그인하도록 항상 요청합니다.

만약 `prompt` 값을 지정하지 않았다면, 사용자가 해당 스코프에 대해 이전에 승인한 적이 없는 경우에만 인증 승인을 요청합니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 이미 패스포트에 의해 정의되어 있으므로 직접 라우트를 작성할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 인증 요청 승인

인증 요청이 들어오면, 패스포트는 `prompt` 파라미터(있을 경우)의 값에 따라 자동으로 응답하며, 사용자가 인증 요청을 승인하거나 거부할 수 있는 화면을 표시할 수 있습니다. 사용자가 요청을 승인하면, 등록된 `redirect_uri`로 다시 리디렉션됩니다. 이때 `redirect_uri`는 클라이언트 생성 시 설정했던 URI와 반드시 일치해야 합니다.

1st party(자사) 클라이언트처럼 인증 화면을 건너뛰고 싶다면, [Client 모델을 확장](#overriding-default-models)하고 `skipsAuthorization` 메서드를 정의하면 됩니다. 이 메서드가 `true`를 반환하면, 인증 화면을 건너뛰고 즉시 `redirect_uri`로 리디렉션됩니다. 단, consuming(요청) 애플리케이션이 인증 요청 시 `prompt` 파라미터를 명시적으로 지정한 경우에는 반드시 인증 화면을 띄웁니다.

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * Determine if the client should skip the authorization prompt.
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
#### 인증 코드를 액세스 토큰으로 변환하기

사용자가 인증 요청을 승인하면, 사용자(클라이언트)는 다시 consuming(요청) 애플리케이션으로 리디렉션됩니다. 이때 애플리케이션은 먼저 `state` 파라미터가 리디렉션 전 저장했던 값과 일치하는지 검증해야 합니다. 일치하면, 애플리케이션에서 여러분의 서버로 `POST` 요청을 보내 액세스 토큰을 발급받을 수 있습니다. 이 요청에는 사용자가 인증 요청을 승인할 때 받은 인증 코드가 포함되어야 합니다.

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

`/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in`은 액세스 토큰이 만료되기까지 남은 초(second)를 나타냅니다.

> [!NOTE]
> `/oauth/authorize` 라우트와 마찬가지로 `/oauth/token` 라우트도 패스포트가 직접 정의하므로, 따로 라우트를 생성할 필요가 없습니다.

<a name="managing-tokens"></a>
### 토큰 관리

`Laravel\Passport\HasApiTokens` 트레이트의 `tokens` 메서드를 사용해서 사용자가 승인한 토큰 목록을 조회할 수 있습니다. 이를 활용하면 사용자들이 인증된 외부 앱 목록을 확인할 수 있는 대시보드 등을 만들어 줄 수 있습니다.

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 해당 사용자의 유효한 토큰 모두 조회...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// 사용자와 연결된 외부 OAuth 앱 클라이언트 목록 구하기...
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

애플리케이션에서 단기(짧은 기간) 액세스 토큰을 발급하는 경우, 사용자는 토큰이 만료되면 발급받았던 리프레시 토큰을 이용해 액세스 토큰을 갱신해야 합니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // 기밀(Confidential) 클라이언트에만 필요...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 `/oauth/token` 라우트 역시 `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in`은 토큰의 남은 유효 시간(초)입니다.

<a name="revoking-tokens"></a>
### 토큰 철회

`Laravel\Passport\Token` 모델의 `revoke` 메서드를 사용해 토큰을 철회할 수 있습니다. 리프레시 토큰의 경우 `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드를 사용하세요.

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// 액세스 토큰 철회...
$token->revoke();

// 리프레시 토큰 철회...
$token->refreshToken?->revoke();

// 사용자의 모든 토큰 철회...
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### 토큰 정리

토큰이 만료되었거나 철회된 경우, 데이터베이스에서 이들 항목을 완전히 삭제할 수 있습니다. 패스포트에 포함된 `passport:purge` 아티즌 명령어를 사용하면 토큰, 인증 코드, 디바이스 코드까지 한 번에 정리할 수 있습니다.

```shell
# 만료되거나 철회된 토큰, 인증 코드, 디바이스 코드 정리
php artisan passport:purge

# 6시간 이상 만료된 항목만 정리
php artisan passport:purge --hours=6

# 철회된 항목만 정리
php artisan passport:purge --revoked

# 만료된 항목만 정리
php artisan passport:purge --expired
```

애플리케이션의 `routes/console.php` 파일에서 [스케쥴 작업](/docs/12.x/scheduling)을 등록하여 주기적으로 토큰을 자동으로 정리할 수도 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## PKCE가 적용된 인증 코드 그랜트

"코드 교환을 위한 검증자(Proof Key for Code Exchange, PKCE)"를 사용하는 인증 코드 그랜트는 싱글 페이지 애플리케이션이나 모바일 애플리케이션에서 API 접근을 안전하게 인증하는 데에 적합한 방식입니다. 클라이언트 시크릿을 완전히 안전하게 보관할 수 없거나, 인증 코드가 공격자에게 탈취되는 위험을 줄이고 싶을 때 이 방식을 사용해야 합니다. 이 때는 "코드 검증자(code verifier)"와 "코드 챌린지(code challenge)"를 조합해 클라이언트 시크릿을 대체합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성

PKCE 방식으로 토큰을 발급받으려면, 먼저 PKCE가 활성화된 클라이언트를 만들어야 합니다. `--public` 옵션을 더해 `passport:client` 아티즌 명령어로 생성할 수 있습니다.

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청

<a name="code-verifier-code-challenge"></a>
#### 코드 검증자와 코드 챌린지

이 방식은 클라이언트 시크릿을 제공하지 않으므로, 개발자는 토큰 요청을 위해 코드 검증자(code verifier)와 코드 챌린지(code challenge)를 만들어야 합니다.

코드 검증자는 최소 43자에서 128자 사이의 임의의 문자열이어야 하며, 영문자, 숫자, 그리고 `" - "`, `"."`, `"_"`, `"~"` 문자만을 포함해야 합니다. 자세한 내용은 [RFC 7636 명세](https://tools.ietf.org/html/rfc7636)를 참고하세요.

코드 챌린지는 URL 및 파일명 안전한(Base64 URL safe) 형식으로 인코딩된 문자열이어야 하며, 뒤쪽의 `'='` 문자는 제거되고, 줄바꿈, 공백 등 추가 문자가 없어야 합니다.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>

#### 인가를 위한 리디렉션

클라이언트가 생성되면, 해당 클라이언트 ID와 생성된 코드 검증(code verifier), 코드 챌린지(code challenge)를 사용하여 애플리케이션에서 인가 코드 및 액세스 토큰을 요청할 수 있습니다. 먼저, 외부 애플리케이션(소비자 애플리케이션)은 여러분의 애플리케이션의 `/oauth/authorize` 경로로 리디렉션 요청을 보내야 합니다.

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

사용자가 인가 요청을 승인하면, 사용자는 소비자 애플리케이션으로 다시 리디렉션됩니다. 이때, 소비자는 표준 Authorization Code Grant와 마찬가지로 리디렉션 전에 저장된 `state` 파라미터 값을 검증해야 합니다.

`state` 파라미터가 일치하는 경우, 소비자 애플리케이션은 여러분의 애플리케이션에 액세스 토큰을 요청하기 위한 `POST` 요청을 보내야 합니다. 이때 함께 전송해야 하는 값은 사용자가 인가 요청을 승인할 때 애플리케이션이 발행한 인가 코드와, 처음 생성했던 코드 검증값(code verifier)입니다.

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
## 디바이스 인가 그랜트(Device Authorization Grant)

OAuth2의 디바이스 인가 그랜트는 TV, 게임 콘솔 등처럼 브라우저가 없거나 입력이 제한된 디바이스가 "디바이스 코드(device code)"를 교환하여 액세스 토큰을 획득할 수 있도록 해줍니다. 디바이스 플로우를 사용할 때 디바이스 클라이언트는 사용자에게 컴퓨터 또는 스마트폰과 같은 2차 디바이스를 이용해 서버에 접속하고, 제공된 "사용자 코드(user code)"를 입력하여 접근 요청을 승인 또는 거부하도록 안내합니다.

우선, Passport에게 "user code" 및 "authorization" 화면을 어떻게 반환할 것인지 지시해야 합니다.

모든 인가 화면 렌더링 로직은 `Laravel\Passport\Passport` 클래스에서 제공하는 적절한 메서드를 통해 커스터마이즈할 수 있습니다. 보통 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 직접 지정하는 방법...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');
    
    // 클로저로 직접 뷰를 반환하는 방법...
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

Passport는 이 뷰를 반환하는 경로(routes)를 자동으로 정의합니다. `auth.oauth.device.user-code` 템플릿에는 반드시 `passport.device.authorizations.authorize` 경로로의 GET 요청을 수행하는 폼(form)이 포함되어야 하며, GET 요청 시 `user_code` 쿼리 파라미터가 전달되어야 합니다.

`auth.oauth.device.authorize` 템플릿에는 인가를 승인하는 `passport.device.authorizations.approve` 경로로의 POST 요청 폼, 그리고 인가 거절을 위한 `passport.device.authorizations.deny` 경로로의 DELETE 요청 폼이 포함되어야 합니다. `passport.device.authorizations.approve` 및 `passport.device.authorizations.deny` 경로에는 `state`, `client_id`, `auth_token` 필드를 전달해야 합니다.

<a name="creating-a-device-authorization-grant-client"></a>
### 디바이스 인가 그랜트 클라이언트 생성

애플리케이션에서 디바이스 인가 그랜트로 토큰을 발급하려면, 우선 디바이스 플로우가 활성화된 클라이언트를 생성해야 합니다. 이는 `passport:client` 아티즌 명령어에 `--device` 옵션을 추가하여 처리할 수 있습니다. 해당 명령어를 실행하면 퍼스트파티(자사) 디바이스 플로우 클라이언트가 생성되며, 클라이언트 ID와 시크릿을 발급 받습니다.

```shell
php artisan passport:client --device
```

또한, `ClientRepository` 클래스의 `createDeviceAuthorizationGrantClient` 메서드를 사용하면 주어진 사용자에 속한 서드파티 클라이언트도 등록할 수 있습니다.

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
### 토큰 요청하기

<a name="device-code"></a>
#### 디바이스 코드 요청

클라이언트가 생성되면, 개발자는 해당 클라이언트 ID를 사용해 애플리케이션에서 디바이스 코드를 요청할 수 있습니다. 먼저 디바이스(소비자)는 애플리케이션의 `/oauth/device/code` 경로에 `POST` 요청을 보내어 디바이스 코드를 받아야 합니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 요청의 응답으로는 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 속성이 포함된 JSON 데이터가 반환됩니다. `expires_in`은 디바이스 코드가 만료되기 전까지의 시간(초)을 담고 있습니다. `interval`은 토큰을 폴링할 때 `/oauth/token` 경로에 몇 초마다 요청해야 하는지를 의미하며, 이를 준수하지 않으면 레이트 리밋 에러가 발생할 수 있습니다.

> [!NOTE]
> `/oauth/device/code` 경로는 Passport가 이미 정의합니다. 별도로 라우트를 추가할 필요가 없습니다.

<a name="user-code"></a>
#### 인증 URI 및 사용자 코드 표시

디바이스 코드 요청을 받은 후엔, 소비자 디바이스(클라이언트)는 사용자에게 별도의 디바이스(예: 스마트폰, 컴퓨터)로 제공된 `verification_uri`에 접속하고, 화면에 보여지는 `user_code`를 입력하여 인가 요청을 승인하라고 안내해야 합니다.

<a name="polling-token-request"></a>
#### 토큰 요청 폴링

사용자가 별도의 디바이스에서 접근 권한을 승인(또는 거부)할 것이므로, 소비자 디바이스에서는 사용자의 응답 상태를 확인하기 위해 애플리케이션의 `/oauth/token` 경로를 일정 간격으로 폴링 요청해야 합니다. 디바이스 코드 요청 응답의 `interval` 값만큼 대기한 후 폴링을 반복해야 레이트 리밋 에러를 피할 수 있습니다.

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

사용자가 인가 요청을 승인했다면, 이 요청의 응답으로는 `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 데이터가 반환됩니다. `expires_in`은 액세스 토큰이 만료되기 전까지의 시간(초)입니다.

<a name="password-grant"></a>
## 패스워드 그랜트(Password Grant)

> [!WARNING]
> 패스워드 그랜트 토큰 사용은 더 이상 권장되지 않습니다. 대신 [OAuth2 Server에서 공식적으로 권장하는 grant 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택해야 합니다.

OAuth2 패스워드 그랜트를 사용하면, 모바일 애플리케이션 등과 같은 주요 퍼스트파티 클라이언트에서 사용자의 이메일 주소/사용자명과 비밀번호로 액세스 토큰을 획득할 수 있습니다. 이렇게 하면 사용자가 전체 OAuth2 인가 코드 리디렉션 과정을 거치지 않고도 퍼스트파티 클라이언트에 안전하게 액세스 토큰을 발행할 수 있습니다.

패스워드 그랜트를 활성화하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enablePasswordGrant` 메서드를 호출하세요.

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

패스워드 그랜트로 토큰을 발급하려면, 패스워드 그랜트 클라이언트를 먼저 생성해야 합니다. 이는 `passport:client` 아티즌 명령어에 `--password` 옵션을 추가하여 실행하면 됩니다.

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청하기

패스워드 그랜트를 활성화하고, 클라이언트를 생성했다면 `/oauth/token` 경로로 사용자의 이메일 주소와 비밀번호를 포함하는 `POST` 요청을 보내 액세스 토큰을 요청할 수 있습니다. 이 경로는 이미 Passport에 의해 등록되어 있으므로 별도 정의가 필요하지 않습니다. 요청이 성공하면 서버에서 `access_token`과 `refresh_token`을 포함한 JSON 응답을 받게 됩니다.

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
> 액세스 토큰은 기본적으로 수명이 깁니다. 하지만 필요에 따라 [최대 액세스 토큰 수명](#configuration)을 자유롭게 설정할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청하기

패스워드 그랜트 또는 클라이언트 자격증명 그랜트(client credentials grant)를 사용할 때, 토큰에 애플리케이션에서 지원하는 모든 스코프를 허용하고 싶을 수 있습니다. 이를 위해 `*` 스코프를 요청하면, 해당 토큰 인스턴스에서 `can` 메서드는 항상 `true`를 반환합니다. 이 스코프는 `password` 또는 `client_credentials` grant를 사용할 때만 토큰에 할당할 수 있습니다.

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
### 사용자 제공자(User Provider) 커스터마이징

애플리케이션에서 [여러 인증 사용자 제공자](/docs/12.x/authentication#introduction)를 사용하는 경우, 클라이언트 생성 시 `artisan passport:client --password` 명령어에 `--provider` 옵션을 추가함으로써 패스워드 그랜트 클라이언트가 사용할 사용자 제공자를 명시할 수 있습니다. 주어진 제공자 이름은 `config/auth.php` 설정 파일에 정의된 유효한 제공자명이어야 합니다. 이후 [미들웨어를 이용해 라우트를 보호](#multiple-authentication-guards)하여 가드에 명시된 제공자의 사용자만 인가하도록 할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명 필드 커스터마이징

패스워드 그랜트로 인증할 때, Passport는 기본적으로 인증 가능한 모델의 `email` 속성을 "사용자명"으로 사용합니다. 하지만, 모델에 `findForPassport` 메서드를 정의하여 이 동작을 커스터마이즈할 수 있습니다.

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
     * 주어진 사용자명으로 사용자 인스턴스를 찾습니다.
     */
    public function findForPassport(string $username): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### 비밀번호 검증 커스터마이징

패스워드 그랜트 인증 시, 기본적으로 Passport는 모델의 `password` 속성으로 전달된 비밀번호를 검증합니다. 만약 모델에 `password` 속성이 없거나, 비밀번호 검증 로직을 커스터마이즈하고 싶다면 모델에 `validateForPassportPasswordGrant` 메서드를 정의하면 됩니다.

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
     * Passport 패스워드 그랜트용 비밀번호를 검증합니다.
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant"></a>
## 임플리싯 그랜트(Implicit Grant)

> [!WARNING]
> 임플리싯 그랜트 토큰 사용은 더 이상 권장되지 않습니다. 대신 [OAuth2 Server에서 공식적으로 권장하는 grant 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택해야 합니다.

임플리싯 그랜트 방식은 인가 코드 그랜트와 유사하지만, 인가 코드 교환 없이 바로 토큰이 클라이언트에 반환됩니다. 이 방식은 클라이언트 자격정보를 안전하게 저장할 수 없는 JavaScript 또는 모바일 앱에서 주로 사용됩니다. 활성화하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enableImplicitGrant` 메서드를 호출하세요.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

임플리싯 그랜트로 토큰을 발급하려면, 우선 임플리싯 그랜트 클라이언트를 생성해야 합니다. `passport:client` 아티즌 명령어에 `--implicit` 옵션을 사용하세요.

```shell
php artisan passport:client --implicit
```

그랜트를 활성화하고 임플리싯 클라이언트가 생성되면, 개발자는 해당 클라이언트 ID를 사용해 애플리케이션에서 액세스 토큰을 요청할 수 있습니다. 소비자 애플리케이션은 여러분의 애플리케이션 `/oauth/authorize` 경로로 다음과 같이 리디렉션 요청을 보내야 합니다.

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
> `/oauth/authorize` 경로는 Passport가 이미 정의합니다. 별도로 라우트를 추가할 필요가 없습니다.

<a name="client-credentials-grant"></a>
## 클라이언트 자격증명 그랜트(Client Credentials Grant)

클라이언트 자격증명 그랜트는 서버 간 인증(m2m, 기계 대 기계) 시나리오에 적합합니다. 예를 들어, API를 통해 유지보수 작업을 수행하는 예약 작업 등에서 이 그랜트를 사용할 수 있습니다.

이 그랜트로 토큰을 발급하려면 우선 클라이언트 자격증명 그랜트 클라이언트를 생성해야 합니다. `passport:client` 아티즌 명령어에 `--client` 옵션을 사용하여 생성할 수 있습니다.

```shell
php artisan passport:client --client
```

그 다음, `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 라우트에 할당하세요.

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하며 클라이언트가 리소스 소유자입니다...
})->middleware(EnsureClientIsResourceOwner::class);
```

특정 스코프에만 접근을 제한하려면, `using` 메서드에 필요한 스코프 목록을 전달할 수 있습니다.

```php
Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하고 클라이언트가 리소스 소유자이며, "servers:read"와 "servers:create" 스코프 모두를 가집니다...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create');
```

<a name="retrieving-tokens"></a>
### 토큰 가져오기

이 그랜트 타입으로 토큰을 가져오려면, `oauth/token` 엔드포인트에 요청을 보내야 합니다.

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

사용자가 OAuth2 인가 코드 리디렉션 플로우를 거치지 않고 애플리케이션 UI 내에서 직접 자신에게 액세스 토큰을 발급하도록 허용하는 것이 필요할 때가 있습니다. 이런 기능은 사용자가 여러분의 API를 실험하거나, 복잡하지 않게 토큰을 발급받고자 할 때 유용합니다.

> [!NOTE]
> 여러분의 애플리케이션이 주로 개인 액세스 토큰 발급 용도로만 Passport를 사용한다면, API 토큰 발급을 위한 라라벨의 공식 경량 라이브러리인 [Laravel Sanctum](/docs/12.x/sanctum) 사용을 고려해 보세요.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성

개인 액세스 토큰을 발급하려면, 먼저 개인 액세스 클라이언트(Personal Access Client)를 생성해야 합니다. 이는 `passport:client` 아티즌 명령어에 `--personal` 옵션을 추가해 실행하면 됩니다. 만약 이미 `passport:install` 명령어를 한 번이라도 실행했다면 이 커맨드를 다시 실행할 필요가 없습니다.

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### 사용자 제공자 커스터마이징

애플리케이션에서 [여러 인증 사용자 제공자](/docs/12.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --personal` 명령어 실행시 `--provider` 옵션을 사용하여 개인 액세스 그랜트 클라이언트의 사용자 제공자를 지정할 수 있습니다. 제공자명은 반드시 `config/auth.php` 파일에 유효하게 등록되어 있어야 하며, 이후 [미들웨어를 이용해 라우트를 보호](#multiple-authentication-guards)하여 가드에 명시된 제공자의 사용자만 인가하도록 할 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리

개인 액세스 클라이언트를 생성하면, `App\Models\User` 모델 인스턴스의 `createToken` 메서드를 통해 해당 사용자에게 토큰을 발급할 수 있습니다. `createToken` 메서드는 토큰 이름(첫 번째 인수)과 [스코프](#token-scopes) 배열(두 번째 인수, 생략 가능)을 받을 수 있습니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 스코프 없이 토큰 생성...
$token = $user->createToken('My Token')->accessToken;

// 특정 스코프와 함께 토큰 생성...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// 모든 스코프를 포함해 토큰 생성...
$token = $user->createToken('My Token', ['*'])->accessToken;

// 해당 사용자의 유효한 개인 접근 토큰 전체 조회...
$tokens = $user->tokens()
    ->with('client')
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get()
    ->filter(fn (Token $token) => $token->client->hasGrantType('personal_access'));
```

<a name="protecting-routes"></a>
## 라우트 보호(Protecting Routes)

<a name="via-middleware"></a>
### 미들웨어를 통한 보호

Passport에는 요청에 전달된 액세스 토큰이 유효한지 검증해주는 [인증 가드](/docs/12.x/authentication#adding-custom-guards)가 내장되어 있습니다. `api` 가드에 `passport` 드라이버를 설정하면, 액세스 토큰이 필요한 라우트에 `auth:api` 미들웨어만 지정하면 됩니다.

```php
Route::get('/user', function () {
    // API 인증 사용자인 경우에만 이 라우트에 접근할 수 있습니다...
})->middleware('auth:api');
```

> [!WARNING]
> [클라이언트 자격증명 그랜트](#client-credentials-grant)를 사용하는 경우, 라우트 보호시 `auth:api` 미들웨어 대신 [Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner 미들웨어](#client-credentials-grant)를 사용해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 다중 인증 가드

애플리케이션에서 서로 다른 Eloquent 모델을 사용하는 여러 사용자 타입을 인증하는 경우, 각 사용자 제공자 유형별로 가드를 정의해야 할 수 있습니다. 이를 통해 특정 사용자 제공자에 특정 요청만 보호할 수 있습니다. 아래는 `config/auth.php` 파일의 예시입니다.

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

다음과 같은 라우트는 `api-customers` 가드를 통해 `customers` 사용자 제공자를 사용하여 요청을 인증하게 됩니다.

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport와 함께 여러 사용자 제공자를 사용하는 방법에 대한 자세한 내용은 [개인 액세스 토큰 문서](#customizing-the-user-provider-for-pat)와 [패스워드 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달하기

Passport로 보호된 라우트를 호출할 때, API 소비자는 요청의 `Authorization` 헤더에 자신이 발급받은 액세스 토큰을 `Bearer` 타입으로 지정해야 합니다. 예를 들어, `Http` 파사드를 사용하는 경우 다음과 같이 할 수 있습니다.

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

스코프는 API 클라이언트가 계정 접근 권한 요청 시, 요청 범위를 명확히 제한할 수 있도록 해줍니다. 예를 들어, 전자상거래 애플리케이션에서 모든 API 소비자가 주문 생성 권한이 필요한 것은 아닙니다. 대신 소비자마다 주문 조회 권한만 요청할 수 있도록 할 수 있습니다. 즉, 스코프를 이용하면 사용자가 자신의 리소스에 대해 서드파티 애플리케이션이 위임받을 수 있는 행동에 제한을 둘 수 있습니다.

<a name="defining-scopes"></a>
### 스코프 정의

`App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `Passport::tokensCan` 메서드를 사용해 API의 스코프를 정의할 수 있습니다. `tokensCan` 메서드는 스코프 이름과 설명이 포함된 배열을 인수로 받으며, 스코프 설명은 원하는 아무 내용이나 표시할 수 있으며 인가 승인 화면에 사용자에게 보여집니다.

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

### 기본 스코프

클라이언트가 별도의 특정 스코프를 요청하지 않는 경우, `defaultScopes` 메서드를 사용하여 Passport 서버에서 토큰에 기본 스코프를 자동으로 지정하도록 설정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

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
### 토큰에 스코프 지정하기

<a name="when-requesting-authorization-codes"></a>
#### 인가 코드 요청 시

인가 코드 그랜트를 사용해 액세스 토큰을 요청할 때, 클라이언트는 원래 필요로 하는 스코프를 `scope` 쿼리 문자열 파라미터로 지정해야 합니다. `scope` 파라미터에는 공백으로 구분된 스코프 목록을 전달합니다.

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

`App\Models\User` 모델의 `createToken` 메서드를 사용해 개인 액세스 토큰을 발급하는 경우, 원하는 스코프 배열을 두 번째 인수로 전달할 수 있습니다.

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 확인

Passport에는, 들어오는 요청이 특정 스코프가 부여된 토큰으로 인증되었는지 확인할 수 있도록 하는 미들웨어가 두 가지 제공됩니다.

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어를 라우트에 할당하면, 해당 요청의 액세스 토큰에 모든 지정한 스코프가 포함되어 있는지 검증할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // 액세스 토큰에 "orders:read"와 "orders:create" 스코프가 모두 포함되어 있는 경우...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create');
```

<a name="check-for-any-scopes"></a>
#### 하나라도 포함된 스코프 확인

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어를 라우트에 할당하면, 해당 요청의 액세스 토큰에 지정한 스코프 중 하나라도 포함되어 있는지 검증할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // 액세스 토큰에 "orders:read" 또는 "orders:create" 중 하나의 스코프가 포함된 경우...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create');
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인

액세스 토큰으로 인증된 요청이 애플리케이션에 도달한 후에도, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드를 이용해 해당 토큰이 특정 스코프를 가지고 있는지 추가로 확인할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('orders:create')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
#### 기타 스코프 관련 메서드

`scopeIds` 메서드는 정의된 모든 ID/이름의 배열을 반환합니다.

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

`scopes` 메서드는 정의된 모든 스코프를 `Laravel\Passport\Scope` 인스턴스 배열로 반환합니다.

```php
Passport::scopes();
```

`scopesFor` 메서드는 지정한 ID/이름에 해당하는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다.

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

특정 스코프가 정의되어 있는지 확인하려면 `hasScope` 메서드를 사용할 수 있습니다.

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA 인증

API를 개발할 때, JavaScript 애플리케이션에서 자신이 만든 API를 바로 소비할 수 있다면 매우 유용합니다. 이런 방식은 자신이 만든 API를 다른 외부 앱뿐 아니라, 자신의 웹 애플리케이션, 모바일 앱, 타사 애플리케이션, 그리고 각종 SDK에서도 동일하게 사용할 수 있도록 해줍니다.

대개 JavaScript 애플리케이션에서 API를 직접 호출하려면, 액세스 토큰을 별도로 관리하여 매 요청마다 토큰을 함께 전달해야 하지만, Passport는 이 과정도 쉽게 만들어 주는 미들웨어를 제공합니다. `CreateFreshApiToken` 미들웨어를 애플리케이션의 `bootstrap/app.php` 파일 내 `web` 미들웨어 그룹에 추가하면 됩니다.

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어가 반드시 미들웨어 스택의 마지막에 위치하도록 설정해야 합니다.

이 미들웨어는 응답에 `laravel_token` 쿠키를 추가합니다. 이 쿠키에는 Passport가 여러분의 JavaScript 애플리케이션에서 오는 API 요청을 인증하는 데 사용하는 암호화된 JWT가 포함됩니다. JWT의 유효기간은 `session.lifetime` 설정 값과 동일합니다. 이제 브라우저가 이후의 모든 요청에 이 쿠키를 자동으로 포함하게 되므로, 별도로 액세스 토큰을 넣지 않고도 애플리케이션의 API를 호출할 수 있습니다.

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이징

필요하다면, `Passport::cookie` 메서드를 사용해 `laravel_token` 쿠키의 이름을 변경할 수 있습니다. 일반적으로는 이 메서드를 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

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

이 인증 방식을 사용할 때는, 요청에 반드시 올바른 CSRF 토큰 헤더가 포함되어 있어야 합니다. 라라벨에서 기본 제공하는 JavaScript 스캐폴딩 및 모든 스타터 킷에는 [Axios](https://github.com/axios/axios) 인스턴스가 포함되어 있는데, 이 인스턴스는 같은 오리진 요청 시 암호화된 `XSRF-TOKEN` 쿠키 값을 활용해 `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.

> [!NOTE]
> 만약 `X-XSRF-TOKEN` 대신 `X-CSRF-TOKEN` 헤더를 보내고 싶다면, 반드시 `csrf_token()`이 반환한 암호화되지 않은 토큰을 사용해야 합니다.

<a name="events"></a>
## 이벤트

Passport는 액세스 토큰 및 리프레시 토큰을 발급할 때 관련 이벤트를 발생시킵니다. [이런 이벤트들을 리스닝하여](/docs/12.x/events) 데이터베이스 내의 다른 액세스 토큰을 정리(삭제)하거나 취소(revoke)할 수 있습니다.

<div class="overflow-auto">

| 이벤트 이름 |
| --- |
| `Laravel\Passport\Events\AccessTokenCreated` |
| `Laravel\Passport\Events\AccessTokenRevoked` |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## 테스트

Passport의 `actingAs` 메서드를 사용하면 현재 인증된 사용자와 그에 부여할 스코프를 지정할 수 있습니다. `actingAs` 메서드의 첫 번째 인자는 사용자 인스턴스, 두 번째 인자는 사용자 토큰에 부여할 스코프 배열입니다.

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

Passport의 `actingAsClient` 메서드를 사용하면, 현재 인증된 클라이언트와 클라이언트 토큰에 부여할 스코프를 지정할 수 있습니다. `actingAsClient`의 첫 번째 인자는 클라이언트 인스턴스, 두 번째 인자는 토큰에 포함할 스코프 배열입니다.

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