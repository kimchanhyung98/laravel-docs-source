# 라라벨 패스포트 (Laravel Passport)

- [소개](#introduction)
    - [Passport와 Sanctum 중 무엇을 사용할까요?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [Passport 업그레이드하기](#upgrading-passport)
- [구성](#configuration)
    - [토큰 수명](#token-lifetimes)
    - [기본 모델 오버라이드](#overriding-default-models)
    - [라우트 오버라이드](#overriding-routes)
- [Authorization Code Grant](#authorization-code-grant)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청하기](#requesting-tokens)
    - [토큰 관리](#managing-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 정리(purging)](#purging-tokens)
- [PKCE와 함께 사용하는 Authorization Code Grant](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청하기](#requesting-auth-pkce-grant-tokens)
- [Device Authorization Grant](#device-authorization-grant)
    - [Device Code Grant 클라이언트 생성](#creating-a-device-authorization-grant-client)
    - [토큰 요청하기](#requesting-device-authorization-grant-tokens)
- [Password Grant](#password-grant)
    - [Password Grant 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청하기](#requesting-password-grant-tokens)
    - [전체 스코프 요청하기](#requesting-all-scopes)
    - [사용자 제공자 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 커스터마이징](#customizing-the-password-validation)
- [Implicit Grant](#implicit-grant)
- [Client Credentials Grant](#client-credentials-grant)
- [Personal Access Token](#personal-access-tokens)
    - [Personal Access Client 생성](#creating-a-personal-access-client)
    - [사용자 제공자 커스터마이징](#customizing-the-user-provider-for-pat)
    - [Personal Access Token 관리](#managing-personal-access-tokens)
- [라우트 보호](#protecting-routes)
    - [미들웨어를 통한 보호](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의하기](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당](#assigning-scopes-to-tokens)
    - [스코프 확인](#checking-scopes)
- [SPA 인증](#spa-authentication)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Passport](https://github.com/laravel/passport)는 라라벨 애플리케이션에 몇 분 만에 OAuth2 서버를 완전히 구현할 수 있도록 도와주는 공식 패키지입니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server)를 기반으로 개발되었습니다.

> [!NOTE]
> 이 문서는 여러분이 이미 OAuth2에 익숙하다고 가정합니다. 만약 OAuth2에 대해 잘 모른다면, 계속해서 문서를 읽기 전에 [용어 정리](https://oauth2.thephpleague.com/terminology/) 및 OAuth2의 기본 개념을 먼저 익혀두시는 것을 권장합니다.

<a name="passport-or-sanctum"></a>
### Passport와 Sanctum 중 무엇을 사용할까요?

시작에 앞서, 여러분의 애플리케이션에 Laravel Passport가 더 적합한지, [Laravel Sanctum](/docs/12.x/sanctum)이 더 적합한지를 먼저 판단하는 것이 좋습니다. 만약 애플리케이션에서 반드시 OAuth2 지원이 필요하다면 라라벨 Passport를 사용해야 합니다.

반면, 싱글 페이지 애플리케이션(SPA), 모바일 애플리케이션과 같이 API 토큰 발급 목적이라면 [Laravel Sanctum](/docs/12.x/sanctum) 사용을 권장합니다. Sanctum은 OAuth2를 지원하지 않지만, 훨씬 간단한 방식으로 API 인증 기능을 개발할 수 있습니다.

<a name="installation"></a>
## 설치

`install:api` 아티즌 명령어를 사용해 Laravel Passport를 설치할 수 있습니다:

```shell
php artisan install:api --passport
```

이 명령어는 OAuth2 클라이언트와 액세스 토큰을 저장하기 위해 필요한 데이터베이스 마이그레이션을 배포 및 실행합니다. 또한 보안 액세스 토큰 생성을 위한 암호화 키도 자동으로 생성합니다.

`install:api` 명령을 실행한 후에는, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가해야 합니다. 이 트레이트는 인증된 사용자의 토큰과 스코프를 확인할 수 있는 여러 헬퍼 메서드를 모델에 제공합니다:

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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고, `driver` 옵션을 `passport`로 설정해야 합니다. 이렇게 하면 API 요청 인증 시 Passport의 `TokenGuard`를 사용하도록 애플리케이션이 동작합니다:

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
### Passport 배포하기

처음으로 Passport를 애플리케이션 서버에 배포할 때는 `passport:keys` 명령어를 실행해야 할 수도 있습니다. 이 명령어는 Passport가 액세스 토큰을 생성하는 데 필요한 암호화 키를 만듭니다. 이 키 파일들은 일반적으로 소스 버전 관리에는 포함하지 않습니다:

```shell
php artisan passport:keys
```

필요하다면, Passport의 키를 로드할 경로를 직접 지정할 수도 있습니다. `Passport::loadKeysFrom` 메서드를 사용해 이 경로를 설정할 수 있으며, 주로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내부에서 호출합니다:

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
#### 환경변수에서 키 로드하기

또는, `vendor:publish` 아티즌 명령어를 사용해 Passport의 설정 파일을 배포할 수도 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일을 배포한 후에는, 다음과 같이 환경 변수로 애플리케이션의 암호화 키를 지정할 수 있습니다:

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="upgrading-passport"></a>
### Passport 업그레이드하기

Passport의 새로운 메이저 버전으로 업그레이드할 때에는 반드시 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

<a name="configuration"></a>
## 구성

<a name="token-lifetimes"></a>
### 토큰 수명

기본적으로 Passport는 1년 동안 유효한 장기간 액세스 토큰을 발급합니다. 만약 더 길거나 짧은 토큰 수명을 설정하고 싶다면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드 내에서 호출해야 합니다:

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
> Passport의 데이터베이스 테이블에 있는 `expires_at` 컬럼은 읽기 전용이며, 표시 목적에만 사용됩니다. Passport는 토큰을 발급할 때 유효기간 정보를 서명되고 암호화된 토큰 내부에 저장합니다. 만약 토큰을 즉시 무효화해야 한다면 [토큰을 폐기](#revoking-tokens)해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Passport 내부적으로 사용되는 모델을 자유롭게 확장할 수 있습니다. 직접 클래스를 정의하고, 해당 클래스가 Passport의 기본 모델을 확장하도록 작성하면 됩니다:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의한 후에는 `Laravel\Passport\Passport` 클래스를 통해 Passport가 여러분의 커스텀 모델을 사용하도록 지정할 수 있습니다. 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 이를 설정합니다:

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
    Passport::useDeviceCodeModel(DeviceCode::class)
}
```

<a name="overriding-routes"></a>
### 라우트 오버라이드

때때로 Passport가 정의하는 라우트들을 커스터마이즈하고 싶을 수 있습니다. 이를 위해 먼저 애플리케이션의 `AppServiceProvider` 클래스의 `register` 메서드에서 `Passport::ignoreRoutes`를 호출해 Passport가 기본 라우트를 등록하지 않도록 합니다:

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

그 다음, [Passport의 라우트 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 여러분의 애플리케이션 `routes/web.php` 파일로 복사한 후, 필요에 맞게 수정하세요:

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

OAuth2를 authorization code 방식으로 사용하는 것은 대부분의 개발자가 익숙한 인증 방식입니다. 이 방식에서는 클라이언트 애플리케이션이 사용자를 서버로 리다이렉트시켜 액세스 토큰 발급을 승인 또는 거부할 수 있게 합니다.

먼저, Passport가 "authorization" 뷰를 어떻게 반환할지 지정해 주어야 합니다.

승인 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스에서 제공하는 메서드를 이용해 자유롭게 커스터마이즈할 수 있습니다. 보통 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 직접 지정하는 방식
    Passport::authorizationView('auth.oauth.authorize');

    // 클로저를 사용하는 방식
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

Passport는 `/oauth/authorize` 라우트를 자동으로 등록하며, 이 라우트는 위에서 지정한 뷰를 반환합니다. 여러분의 `auth.oauth.authorize` 템플릿에는 승인 시 `passport.authorizations.approve` 라우트(POST 요청)와 거부 시 `passport.authorizations.deny` 라우트(DELETE 요청)로 각각 폼을 제출하는 폼을 포함해야 합니다. 이 두 라우트는 `state`, `client_id`, `auth_token` 필드를 요구합니다.

<a name="managing-clients"></a>
### 클라이언트 관리

여러분의 애플리케이션 API와 통신해야 하는 외부 애플리케이션 개발자들은 자신의 애플리케이션을 등록(클라이언트 생성)해야 합니다. 일반적으로 클라이언트의 이름, 그리고 사용자가 인증을 승인한 이후 리디렉션될 URI를 입력받아 등록합니다.

<a name="managing-first-party-clients"></a>
#### 퍼스트파티 클라이언트

가장 간단하게 클라이언트를 생성하는 방법은 `passport:client` 아티즌 명령어를 사용하는 것입니다. 이 명령어는 퍼스트파티 클라이언트를 만들 때나 OAuth2 기능 테스트에 사용할 수 있습니다. 명령어를 실행하면 클라이언트에 대한 정보를 차례로 입력하라고 안내하며, 입력이 끝나면 클라이언트 ID와 Secret을 반환합니다:

```shell
php artisan passport:client
```

하나의 클라이언트에 여러 개의 리디렉션 URI를 지정하고 싶을 때는 입력 시 콤마(,)로 구분해서 URI를 입력하면 됩니다. 단, URI 자체에 콤마가 포함되어 있다면, 해당 URI는 URI 인코딩해야 합니다:

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 서드파티 클라이언트

여러분의 사용자(또는 외부 개발자)는 직접 `passport:client` 명령어를 사용할 수 없기 때문에, `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드를 통해 특정 사용자를 위한 클라이언트를 등록할 수 있습니다:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// 주어진 사용자에게 귀속되는 OAuth 앱 클라이언트 생성...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// 해당 사용자에게 속한 OAuth 앱 클라이언트 전체 조회...
$clients = $user->oauthApps()->get();
```

`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. 사용자는 `$client->id`를 클라이언트 ID로, `$client->plainSecret`을 클라이언트 시크릿으로 사용할 수 있습니다.

<a name="requesting-tokens"></a>
### 토큰 요청하기

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인증 승인을 위한 리다이렉트

클라이언트가 생성되면, 개발자는 이제 클라이언트 ID와 시크릿을 사용해 승인 코드와 액세스 토큰을 요청할 수 있습니다. 우선, 외부 애플리케이션에서는 다음과 같이 여러분의 애플리케이션 `/oauth/authorize`로 리다이렉트 요청을 보내야 합니다:

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

`prompt` 파라미터는 Passport 애플리케이션의 인증 동작을 세부적으로 지정할 때 사용할 수 있습니다.

- `prompt` 값이 `none`이면, Passport 애플리케이션에 아직 인증되어 있지 않은 경우 항상 인증 에러가 발생합니다.
- 값이 `consent`이면, 이전에 모든 스코프 승인을 했더라도 항상 인증 승인 화면을 보여줍니다.
- 값이 `login`이면, 이미 세션이 존재하더라도 항상 다시 로그인하도록 안내합니다.

아무 값도 전달하지 않으면, 해당 스코프에 대한 승인이 이전에 없었던 경우에만 인증 승인이 요청됩니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 Passport가 이미 정의합니다. 직접 라우트를 만들 필요가 없습니다.

<a name="approving-the-request"></a>
#### 인증 요청 승인

인증 요청을 수신하면 Passport는(요청에 `prompt` 파라미터가 있을 경우 이를 참고하여) 승인 화면을 자동으로 렌더링하거나, 직접 커스텀한 템플릿을 표시하여 사용자가 승인을 할 수 있도록 합니다. 사용자가 승인을 하면, 지정한 `redirect_uri`로 다시 리다이렉트됩니다. 이때 `redirect_uri`는 클라이언트 생성시 등록한 URI와 반드시 일치해야 합니다.

때에 따라서는 퍼스트파티 클라이언트와 같이 승인 창을 생략하고 싶을 수 있습니다. 이럴 때에는 [`Client` 모델을 확장](#overriding-default-models)한 후 `skipsAuthorization` 메서드를 정의하면 됩니다. 이 메서드가 `true`를 반환하면, 승인 절차를 건너뛰고 곧바로 사용자 리디렉트가 이루어집니다. 단, 외부 애플리케이션에서 리다이렉트 시 `prompt` 파라미터를 명시적으로 지정했다면 예외적으로 동작할 수 있습니다:

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 클라이언트가 인증 승인 단계를 건너뛰어야 하는지 확인합니다.
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

사용자가 인증 요청을 승인하면, 외부 애플리케이션으로 리디렉트됩니다. 이때, 애플리케이션은 먼저 `state` 파라미터 값이 redirect 전 저장해둔 값과 일치하는지 검증해야 합니다. 값이 일치하면, 여러분의 애플리케이션에 인증 코드와 함께 `POST` 요청을 보내 액세스 토큰을 요청할 수 있습니다. 요청에는 사용자가 승인 시 발급한 인증 코드가 포함되어야 합니다:

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

`/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in` 값은 액세스 토큰 만료까지 남은 초(seconds)입니다.

> [!NOTE]
> `/oauth/authorize` 라우트와 마찬가지로, `/oauth/token` 라우트 역시 Passport가 기본으로 정의합니다. 직접 추가할 필요가 없습니다.

<a name="managing-tokens"></a>
### 토큰 관리

`Laravel\Passport\HasApiTokens` 트레이트의 `tokens` 메서드를 사용하면, 사용자의 발급된(승인된) 토큰을 조회할 수 있습니다. 예를 들어, 사용자에게 자신의 외부 앱 연결 내역을 보여주는 대시보드 등을 구현할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 사용자에 대해 유효한 토큰 모두 조회...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// 사용자의 외부 OAuth 앱별 연결 내역(토큰) 그룹화 조회...
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

애플리케이션이 단기 액세스 토큰을 발급하는 경우, 사용자는 액세스 토큰 만료 시 함께 제공된 refresh token을 이용해 토큰을 갱신할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // confidential 클라이언트 전용...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

`/oauth/token` 경로는 `access_token`, `refresh_token`, `expires_in` 속성을 포함한 JSON 응답을 반환합니다. `expires_in` 값은 액세스 토큰의 남은 유효 시간(초)입니다.

<a name="revoking-tokens"></a>
### 토큰 폐기

발급한 토큰을 더이상 사용하지 않도록 하려면, `Laravel\Passport\Token` 모델의 `revoke` 메서드를 사용해 토큰을 폐기할 수 있습니다. 토큰의 refresh 토큰 역시 `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드를 이용해 폐기할 수 있습니다:

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// 액세스 토큰 폐기
$token->revoke();

// 해당 토큰의 refresh 토큰 폐기
$token->refreshToken?->revoke();

// 사용자의 모든 토큰 일괄 폐기
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### 토큰 정리(purging)

토큰이 폐기됐거나 만료된 경우, 데이터베이스에서 깨끗하게 정리하고 싶을 수 있습니다. Passport가 제공하는 `passport:purge` 아티즌 명령어로 이를 쉽게 처리할 수 있습니다:

```shell
# 폐기되거나 만료된 토큰, 인증 코드, 디바이스 코드 정리
php artisan passport:purge

# 6시간 이상 지난 만료된 항목만 정리
php artisan passport:purge --hours=6

# 폐기된 항목만 정리
php artisan passport:purge --revoked

# 만료된 항목만 정리
php artisan passport:purge --expired
```

또한, 애플리케이션의 `routes/console.php` 파일에서 [스케줄 작업](/docs/12.x/scheduling)을 등록해, 주기적으로 토큰을 자동 정리하도록 할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## PKCE와 함께 사용하는 Authorization Code Grant

"Proof Key for Code Exchange"(PKCE)를 활용한 Authorization Code Grant는 싱글 페이지 애플리케이션(SPA)이나 모바일 앱에서 보다 안전하게 API 인증을 수행하도록 고안된 방식입니다. 이 인증 타입은 클라이언트 시크릿이 외부에 노출될 가능성이 있거나, 인증 코드가 공격자에 의해 가로채일 위험이 있을 때 사용하면 매우 효과적입니다. PKCE 방식에서는 "코드 베리파이어(code verifier)"와 "코드 챌린지(code challenge)"의 조합이, 인증 코드와 액세스 토큰을 교환하는 과정에서 클라이언트 시크릿을 대체합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성

PKCE가 활성화된 Authorization Code Grant를 사용해 토큰을 발급하려면, 우선 PKCE가 활성화된 클라이언트를 생성해야 합니다. 다음과 같이 `--public` 옵션과 함께 `passport:client` 아티즌 명령어를 실행하면 됩니다:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청하기

<a name="code-verifier-code-challenge"></a>
#### 코드 베리파이어와 코드 챌린지

이 인증 방식은 클라이언트 시크릿을 제공하지 않으므로, 개발자는 토큰을 요청할 때 코드 베리파이어(code verifier)와 코드 챌린지(code challenge)의 조합을 생성해야 합니다.

- 코드 베리파이어는 영문자, 숫자, 그리고  `"-"`, `"."`, `"_"`, `"~"` 문자를 포함한 43~128자 사이의 랜덤 문자열이어야 하며, [RFC 7636 명세](https://tools.ietf.org/html/rfc7636)에 정의된 규칙을 따라야 합니다.
- 코드 챌린지는 URL 및 파일명에 안전한 문자로 이루어진 Base64 인코딩 문자열이어야 합니다. 끝의 `'='` 문자는 제거하며, 줄바꿈이나 공백 등 불필요한 문자가 있으면 안 됩니다.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>

#### 인가(Authorization)를 위한 리다이렉트

클라이언트가 생성되면, 클라이언트 ID와 생성한 code verifier 및 code challenge를 이용해 애플리케이션에 authorization code와 access token을 요청할 수 있습니다. 먼저, 소비자 애플리케이션에서 여러분 애플리케이션의 `/oauth/authorize` 라우트로 리다이렉트 요청을 해야 합니다:

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
#### Authorization Code를 Access Token으로 변환하기

사용자가 인가 요청을 승인하면, 사용자는 소비자 애플리케이션으로 다시 리다이렉트됩니다. 소비자 측에서는 표준 Authorization Code Grant 방식과 마찬가지로 리다이렉트 전에 저장해둔 값과 반환된 `state` 파라미터가 일치하는지 반드시 검증해야 합니다.

`state` 파라미터가 일치하면, 소비자 애플리케이션에서 애플리케이션으로 `POST` 요청을 보내 access token을 요청합니다. 이 요청에는 사용자가 인가 요청을 승인할 때 발급된 authorization code와, 최초에 생성한 code verifier가 함께 전달되어야 합니다:

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
## 디바이스 인가(Device Authorization) 그랜트

OAuth2 Device Authorization Grant(디바이스 인가 그랜트)는 TV, 게임 콘솔 등 브라우저를 사용할 수 없거나 입력이 제한된 디바이스가 "device code"(디바이스 코드)를 이용해 access token을 받을 수 있게 해줍니다. 디바이스 플로우를 사용할 때, 디바이스 클라이언트는 사용자가 다른(보조) 장치(예: 컴퓨터, 스마트폰 등)를 이용해 서버에 접근하도록 안내하고, 해당 디바이스에서 "user code"(사용자 코드)를 입력해 인가 요청을 승인하거나 거부할 수 있게 합니다.

먼저, Passport가 "user code"와 "authorization" 뷰를 어떻게 반환할지 지정해주어야 합니다.

모든 인가 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스의 적절한 메서드를 통해 자유롭게 커스터마이징할 수 있습니다. 일반적으로, 여러분의 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 이 메서드를 호출하면 됩니다.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 지정하는 방법...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // 클로저를 지정하는 방법...
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

Passport는 이러한 뷰를 반환하는 라우트를 자동으로 정의합니다. `auth.oauth.device.user-code` 템플릿에는 `passport.device.authorizations.authorize` 라우트로 GET 요청을 보내는 폼이 반드시 포함되어야 합니다. `passport.device.authorizations.authorize` 라우트는 `user_code` 쿼리 파라미터를 필요로 합니다.

`auth.oauth.device.authorize` 템플릿에는 인가를 승인하는 `passport.device.authorizations.approve` 라우트로 POST 요청을 보내는 폼, 인가를 거부하는 `passport.device.authorizations.deny` 라우트로 DELETE 요청을 보내는 폼이 각각 필요합니다. `passport.device.authorizations.approve` 및 `passport.device.authorizations.deny` 라우트에는 `state`, `client_id`, `auth_token` 필드가 기대됩니다.

<a name="creating-a-device-authorization-grant-client"></a>
### 디바이스 인가 그랜트 클라이언트 생성하기

애플리케이션이 디바이스 인가 그랜트를 통해 토큰을 발급할 수 있으려면, 먼저 디바이스 플로우를 지원하는 클라이언트를 생성해야 합니다. 다음 Artisan 명령어로 `--device` 옵션을 지정해 클라이언트를 생성할 수 있습니다. 이 명령은 1st-party 디바이스 플로우 클라이언트를 만들고, 클라이언트 ID와 secret 값을 제공합니다:

```shell
php artisan passport:client --device
```

또한, `ClientRepository` 클래스의 `createDeviceAuthorizationGrantClient` 메서드를 통해 지정한 사용자에 속하는 3rd-party 클라이언트를 등록할 수도 있습니다:

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
#### 디바이스 코드(device code) 요청

클라이언트가 생성되었다면, 개발자는 해당 클라이언트 ID를 이용해 애플리케이션에서 디바이스 코드를 요청할 수 있습니다. 먼저, 소비자 디바이스가 여러분 애플리케이션의 `/oauth/device/code` 라우트로 `POST` 요청을 보내 디바이스 코드를 받아야 합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 요청은 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in` 속성은 디바이스 코드가 만료되기까지의 초(second) 수를 나타냅니다. `interval` 속성은 디바이스가 `/oauth/token` 라우트로 폴링할 때 사용하는 요청 간 최소 대기시간(초)을 의미하며, 지나친 요청으로 인한 레이트 리밋 오류를 방지합니다.

> [!NOTE]
> `/oauth/device/code` 라우트는 이미 Passport에 의해 자동으로 정의되어 있습니다. 별도로 정의할 필요가 없습니다.

<a name="user-code"></a>
#### Verification URI와 User Code 표시하기

디바이스 코드 요청 결과를 받은 후에는, 소비자 디바이스가 사용자에게 다른 디바이스(PC, 스마트폰 등)에서 `verification_uri`로 접속하여, 인가 요청을 승인하기 위해 `user_code`를 입력하라고 안내해야 합니다.

<a name="polling-token-request"></a>
#### 토큰 요청 폴링(Polling)

사용자가 별도의 디바이스에서 인가(또는 거부) 작업을 수행하므로, 소비자 디바이스는 사용자가 해당 요청에 응답했는지 확인하기 위해 여러분 애플리케이션의 `/oauth/token` 라우트로 주기적으로 폴링해야 합니다. 레이트 리밋 오류를 피하려면, 디바이스 코드 요청 결과 반환된 JSON의 최소 `interval` 값을 따라 폴링 주기를 맞추어야 합니다:

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

만약 사용자가 인가 요청을 승인했다면, 이 요청은 `access_token`, `refresh_token`, `expires_in` 속성을 담은 JSON 응답을 반환합니다. `expires_in` 속성은 access token의 만료까지 남은 초(second) 단위 시간을 나타냅니다.

<a name="password-grant"></a>
## 패스워드 그랜트(Password Grant)

> [!WARNING]
> 패스워드 그랜트 토큰 사용은 더 이상 권장하지 않습니다. OAuth2 Server가 현재 권장하는 [다른 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 사용하시기 바랍니다.

OAuth2 패스워드 그랜트를 이용하면, 모바일 애플리케이션 등 여러분의 다른 1st-party 클라이언트가 이메일 주소/사용자명과 비밀번호로 access token을 받을 수 있습니다. 즉, 사용자가 전체 OAuth2 authorization code 리다이렉트 플로우를 거치지 않고도, 여러분의 1st-party 클라이언트에 안전하게 access token을 발급할 수 있습니다.

패스워드 그랜트를 활성화하려면, 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 `enablePasswordGrant` 메서드를 호출합니다:

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
### 패스워드 그랜트 클라이언트 생성하기

애플리케이션에서 패스워드 그랜트를 통해 토큰을 발급하려면, 패스워드 그랜트 클라이언트를 생성해야 합니다. 다음과 같이 `passport:client` Artisan 명령어에 `--password` 옵션을 추가해 생성할 수 있습니다.

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청하기

그랜트를 활성화하고 패스워드 그랜트 클라이언트를 만들었다면, 사용자의 이메일 주소와 비밀번호로 `/oauth/token` 라우트에 `POST` 요청을 보내 access token을 요청할 수 있습니다. 이 라우트는 Passport에 의해 이미 등록되어 있으므로, 별도로 정의할 필요가 없습니다. 요청이 성공하면, 서버에서 JSON 응답으로 `access_token`과 `refresh_token`을 반환합니다:

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
> access token은 기본적으로 수명이 깁니다. 필요하다면 [access token의 최대 수명](#configuration)을 직접 설정할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청하기

패스워드 그랜트나 클라이언트 크리덴셜 그랜트에서, 애플리케이션에서 지원하는 모든 스코프에 대해 토큰 인가를 받고 싶다면, `*` 스코프를 요청하면 됩니다. 이 스코프가 할당되면, 토큰 인스턴스의 `can` 메서드는 항상 `true`를 반환합니다. 이 스코프는 반드시 `password` 또는 `client_credentials` 그랜트로 발급된 토큰에만 할당할 수 있습니다.

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
### 사용자 프로바이더(User Provider) 커스터마이징

애플리케이션에서 [인증 사용자 프로바이더](/docs/12.x/authentication#introduction)를 여러 개 사용하는 경우, `artisan passport:client --password` 명령어로 클라이언트를 생성할 때 `--provider` 옵션을 추가해 그랜트 클라이언트가 사용할 프로바이더를 지정할 수 있습니다. 지정한 프로바이더 이름은 `config/auth.php` 설정 파일에 정의된 유효한 프로바이더와 일치해야 합니다. 이후에는 해당 가드의 프로바이더에 소속된 사용자만 인가받을 수 있도록 [라우트에 미들웨어를 적용](#multiple-authentication-guards)할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명(username) 필드 커스터마이징

패스워드 그랜트 인증 시, Passport는 기본적으로 인증 가능한 모델의 `email` 속성을 "username"으로 사용합니다. 그러나, 모델에 `findForPassport` 메서드를 정의하여 이 동작을 원하는 대로 커스터마이징할 수 있습니다:

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
### 비밀번호 검증 로직 커스터마이징

패스워드 그랜트 인증 시, Passport는 모델의 `password` 속성을 이용해 주어진 비밀번호를 검증합니다. 만약 모델에 `password` 속성이 없거나, 비밀번호 검증 로직을 커스터마이즈하고자 한다면, 모델에 `validateForPassportPasswordGrant` 메서드를 정의할 수 있습니다:

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
## 임플리싯 그랜트(Implicit Grant)

> [!WARNING]
> 임플리싯 그랜트 토큰은 더 이상 권장하지 않습니다. OAuth2 Server가 현재 권장하는 [다른 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하시기 바랍니다.

임플리싯 그랜트는 authorization code 그랜트와 유사하지만, 클라이언트가 authorization code를 별도로 주고받는 과정 없이 즉시 토큰을 받는 방식입니다. 이 방식은 주로 클라이언트 크리덴셜을 안전하게 저장할 수 없는 JavaScript 또는 모바일 애플리케이션에 적합합니다. 임플리싯 그랜트를 활성화하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enableImplicitGrant` 메서드를 호출합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

임플리싯 그랜트로 토큰을 발급하려면, `passport:client` Artisan 명령어에 `--implicit` 옵션을 추가해 임플리싯 그랜트 클라이언트를 생성해야 합니다.

```shell
php artisan passport:client --implicit
```

그랜트가 활성화되고 임플리싯 클라이언트가 생성된 후, 개발자는 클라이언트 ID를 사용해 애플리케이션에서 access token을 요청할 수 있습니다. 소비자 애플리케이션에서는 아래와 같이 `/oauth/authorize` 라우트로 리다이렉트 요청을 보내야 합니다:

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
> `/oauth/authorize` 라우트는 Passport에서 이미 자동으로 정의되어 있습니다. 직접 정의할 필요가 없습니다.

<a name="client-credentials-grant"></a>
## 클라이언트 크리덴셜 그랜트(Client Credentials Grant)

클라이언트 크리덴셜 그랜트는 머신 간 인증에 적합합니다. 예를 들어, 예약된 작업이 API를 통해 유지보수 작업을 수행할 때 이 방식을 사용할 수 있습니다.

클라이언트 크리덴셜 그랜트로 토큰을 발급하려면, 먼저 클라이언트 크리덴셜 그랜트용 클라이언트를 생성해야 합니다. 이를 위해 `passport:client` Artisan 명령어에 `--client` 옵션을 사용합니다:

```shell
php artisan passport:client --client
```

그리고 나서, `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 라우트에 할당합니다:

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // Access token is valid and the client is resource owner...
})->middleware(EnsureClientIsResourceOwner::class);
```

특정 스코프가 필요한 경우, `using` 메서드에 요구하는 스코프 목록을 전달해 라우트 접근을 제한할 수 있습니다:

```php
Route::get('/orders', function (Request $request) {
    // Access token is valid, the client is resource owner, and has both "servers:read" and "servers:create" scopes...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create');
```

<a name="retrieving-tokens"></a>
### 토큰 조회하기

이 그랜트 타입으로 토큰을 발급받으려면, `oauth/token` 엔드포인트로 요청하면 됩니다:

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
## Personal Access Token(개인 액세스 토큰)

때로는, 사용자가 일반적인 authorization code 리다이렉트 플로우를 거치지 않고 직접 access token을 발급 받고 싶어 할 수 있습니다. 애플리케이션 UI를 통해 사용자가 토큰을 직접 발급받도록 허용하는 기능은 API 사용 실험이나, 전반적으로 토큰 발급을 단순화하는 데에도 도움이 될 수 있습니다.

> [!NOTE]
> 애플리케이션에서 주로 Personal Access Token 발급용으로 Passport를 사용한다면, 라라벨의 경량화 1st-party API 토큰 발급 라이브러리인 [Laravel Sanctum](/docs/12.x/sanctum) 사용도 고려해보세요.

<a name="creating-a-personal-access-client"></a>
### Personal Access Client 생성하기

Personal Access Token을 발급하려면, Personal Access Client를 먼저 생성해야 합니다. 아래와 같이 `passport:client` Artisan 명령어에 `--personal` 옵션을 사용해 생성할 수 있습니다. 이미 `passport:install` 명령어를 한번 실행했다면 다시 실행할 필요는 없습니다:

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### Personal Access Token 클라이언트의 사용자 프로바이더 지정

애플리케이션에 [여러 인증 사용자 프로바이더](/docs/12.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --personal` 명령어로 Personal Access Token 클라이언트를 생성할 때 `--provider` 옵션으로 해당 클라이언트가 사용할 사용자 프로바이더를 지정할 수 있습니다. 이 이름은 반드시 `config/auth.php`에 정의된 유효한 프로바이더명과 일치해야 합니다. 이후 [라우트에 미들웨어를 적용](#multiple-authentication-guards)하여, 해당 가드의 프로바이더에 소속된 사용자만 인가할 수 있게 할 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### Personal Access Token 관리

Personal Access Client를 생성했다면, `App\Models\User` 모델 인스턴스에서 `createToken` 메서드를 사용해 해당 사용자에게 토큰을 발급할 수 있습니다. `createToken` 메서드는 첫 번째 인자로 토큰 이름, 두 번째(선택적) 인자로 [스코프](#token-scopes) 배열을 받습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 스코프 없이 토큰 생성...
$token = $user->createToken('My Token')->accessToken;

// 스코프를 지정해서 토큰 생성...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// 모든 스코프를 가진 토큰 생성...
$token = $user->createToken('My Token', ['*'])->accessToken;

// 해당 사용자가 가진 모든 유효한 Personal Access Token 조회...
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
### 미들웨어를 통한 보호

Passport는 요청에 포함된 access token을 검증할 수 있는 [인증 가드](/docs/12.x/authentication#adding-custom-guards)를 제공합니다. `api` 가드를 `passport` 드라이버로 설정했다면, access token이 반드시 필요한 라우트에서는 `auth:api` 미들웨어만 지정하면 됩니다:

```php
Route::get('/user', function () {
    // API 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware('auth:api');
```

> [!WARNING]
> [클라이언트 크리덴셜 그랜트](#client-credentials-grant)를 사용하는 경우, 라우트 보호를 위해 반드시 `auth:api` 미들웨어 대신 [Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner 미들웨어](#client-credentials-grant)를 사용해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 여러 인증 가드(Multiple Authentication Guards)

애플리케이션에서 서로 다른 타입의 사용자(각기 다른 Eloquent 모델 사용)를 인증한다면, 각 사용자 프로바이더 유형별로 별도의 가드 구성을 추가해야 할 수 있습니다. 이렇게 하면, 특정 사용자 프로바이더 대상의 요청만 보호할 수 있습니다. 예를 들어 `config/auth.php` 설정 파일에 다음과 같이 가드 구성을 한다면:

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

아래 라우트는 `api-customers` 가드를 사용하게 되며, `customers` 사용자 프로바이더를 이용해 들어오는 요청을 인증합니다:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport에서 여러 사용자 프로바이더를 사용하는 방법에 대한 자세한 내용은 [Personal Access Token 문서](#customizing-the-user-provider-for-pat)와 [Password Grant 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### Access Token 전달 방식

Passport로 보호된 라우트를 호출할 때, API 소비자는 요청의 `Authorization` 헤더에 반드시 `Bearer` 토큰으로 access token을 지정해야 합니다. 아래는 `Http` 파사드를 활용한 예시입니다:

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

스코프(scope)를 활용하면, API 클라이언트가 계정에 접근을 요청할 때 명확히 어떤 권한까지 인정받고자 하는지 세부적으로 지정할 수 있습니다. 예를 들어, 전자상거래 애플리케이션을 만드는 경우 모든 API 소비자가 주문 등록 권한까지 가질 필요는 없습니다. 대신, 특정 소비자에게는 주문 배송 상태만 가져올 수 있는 권한만 부여할 수 있습니다. 즉, 스코프를 이용해 사용자가 제3자 애플리케이션이 허용할 수 있는 행위 범위를 제한할 수 있습니다.

<a name="defining-scopes"></a>
### 스코프 정의하기

애플리케이션의 스코프는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `Passport::tokensCan` 메서드를 사용해 정의할 수 있습니다. `tokensCan`은 각 스코프 이름과 설명을 담은 배열을 받으며, 설명은 원하는 텍스트로 지정할 수 있고 인가 승인 화면에 표시됩니다:

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

클라이언트가 명시적으로 특정 스코프를 요청하지 않는 경우, `defaultScopes` 메서드를 사용하여 Passport 서버가 토큰에 기본 스코프를 자동으로 부여하도록 설정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 호출해야 합니다.

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

인가 코드 그랜트를 사용해 액세스 토큰을 요청할 때, 소비자는 원하는 스코프를 `scope` 쿼리 스트링 파라미터로 지정해야 합니다. 이 `scope` 파라미터에는 요청할 스코프들을 공백으로 구분하여 나열해야 합니다.

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

`App\Models\User` 모델의 `createToken` 메서드를 이용해 개인 액세스 토큰을 발급하는 경우, 두 번째 인수로 원하는 스코프들의 배열을 전달할 수 있습니다.

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 확인하기

Passport에는 들어오는 요청이 특정 스코프가 부여된 토큰으로 인증되었는지 확인할 수 있는 두 가지 미들웨어가 포함되어 있습니다.

<a name="check-for-all-scopes"></a>
#### 모든 스코프 일치 확인

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어는 라우트에 할당하여, 들어오는 요청의 액세스 토큰이 지정된 모든 스코프를 가지고 있는지 검증할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // 액세스 토큰에 "orders:read"와 "orders:create" 스코프가 모두 포함되어 있을 때...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create');
```

<a name="check-for-any-scopes"></a>
#### 하나 이상의 스코프 포함 여부 확인

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어는 라우트에 할당하여, 들어오는 요청의 액세스 토큰이 나열된 스코프 중 하나라도 포함되어 있는지 검증할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // 액세스 토큰에 "orders:read" 또는 "orders:create" 스코프가 하나 이상 포함되어 있을 때...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create');
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인

액세스 토큰으로 인증된 요청이 애플리케이션에 도달한 후에도, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드를 사용하여 해당 토큰에 특정 스코프가 포함되어 있는지 확인할 수 있습니다.

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

`scopeIds` 메서드는 정의된 모든 스코프의 ID(이름) 배열을 반환합니다.

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

`scopes` 메서드는 정의된 모든 스코프를 `Laravel\Passport\Scope` 인스턴스 배열로 반환합니다.

```php
Passport::scopes();
```

`scopesFor` 메서드는 전달한 ID(이름)에 해당하는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다.

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

`hasScope` 메서드를 사용하면 특정 스코프가 정의되어 있는지 확인할 수 있습니다.

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA 인증

API를 구축할 때, 자바스크립트 애플리케이션에서 자체 API를 소비할 수 있다는 점이 매우 유용할 수 있습니다. 이런 API 개발 방식은 여러분의 애플리케이션 스스로 동일 API를 활용하며, 이 API를 웹 애플리케이션, 모바일 앱, 서드파티 애플리케이션, 그리고 다양한 패키지 관리자에 공개한 SDK 등에서 모두 활용할 수 있게 해줍니다.

보통 자바스크립트 애플리케이션에서 API를 사용하려면, 액세스 토큰을 직접 받아 매번 요청 시마다 함께 전달해야 했습니다. 하지만 Passport에는 이 과정을 간편하게 처리할 수 있는 미들웨어가 포함되어 있습니다. 애플리케이션의 `bootstrap/app.php` 파일의 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어만 추가하면 됩니다.

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어가 미들웨어 스택의 마지막에 위치하도록 반드시 설정해야 합니다.

이 미들웨어는 응답에 `laravel_token`이라는 쿠키를 자동으로 부착합니다. 이 쿠키에는 Passport가 자바스크립트 애플리케이션의 API 요청을 인증하는 데 사용할 암호화된 JWT가 들어 있습니다. 이 JWT의 수명은 `session.lifetime` 설정 값과 동일합니다. 이제 브라우저가 이후의 모든 요청에 해당 쿠키를 자동으로 포함하므로, 별도 액세스 토큰을 명시적으로 전달하지 않고도 API 요청을 보낼 수 있습니다.

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이즈

필요하다면, `Passport::cookie` 메서드를 사용하여 `laravel_token` 쿠키의 이름을 사용자화할 수 있습니다. 이 메서드 역시 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출하는 것이 가장 일반적입니다.

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

이와 같은 인증 방식을 사용할 때는 요청에 반드시 유효한 CSRF 토큰 헤더가 포함되어야 합니다. 라라벨의 기본 자바스크립트 스캐폴딩과 모든 스타터 키트에는 [Axios](https://github.com/axios/axios) 인스턴스가 내장되어 있으며, 이는 자동으로 암호화된 `XSRF-TOKEN` 쿠키 값을 사용해 동일 출처 요청에 `X-XSRF-TOKEN` 헤더를 전송합니다.

> [!NOTE]
> 만약 `X-XSRF-TOKEN` 대신 `X-CSRF-TOKEN` 헤더를 직접 전송하고 싶다면, 반드시 `csrf_token()`에서 제공하는 **암호화되지 않은 토큰**을 사용해야 합니다.

<a name="events"></a>
## 이벤트

Passport는 액세스 토큰 및 리프레시 토큰을 발급할 때 이벤트를 발생시킵니다. [이벤트를 수신(Listen)](/docs/12.x/events)하여 데이터베이스에서 다른 액세스 토큰을 정리(prune)하거나 폐기(revoke)할 수 있습니다.

<div class="overflow-auto">

| 이벤트 이름                                   |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## 테스트

Passport의 `actingAs` 메서드를 사용하면 현재 인증된 사용자와, 해당 사용자의 토큰에 부여할 스코프를 지정할 수 있습니다. `actingAs` 메서드의 첫 번째 인수는 사용자 인스턴스이고, 두 번째는 사용자 토큰에 부여할 스코프들의 배열입니다.

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

Passport의 `actingAsClient` 메서드는 현재 인증된 클라이언트와 해당 클라이언트 토큰에 부여할 스코프를 지정하는 데 사용합니다. `actingAsClient`의 첫 번째 인수는 클라이언트 인스턴스, 두 번째는 클라이언트 토큰에 부여할 스코프 배열입니다.

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