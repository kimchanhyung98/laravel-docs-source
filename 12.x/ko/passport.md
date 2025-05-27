# 라라벨 패스포트 (Laravel Passport)

- [소개](#introduction)
    - [패스포트와 생텀 중 어떤 것을 사용할까?](#passport-or-sanctum)
- [설치](#installation)
    - [패스포트 배포](#deploying-passport)
    - [패스포트 업그레이드](#upgrading-passport)
- [설정](#configuration)
    - [토큰 만료 기간](#token-lifetimes)
    - [기본 모델 오버라이드](#overriding-default-models)
    - [라우트 오버라이드](#overriding-routes)
- [Authorization Code Grant](#authorization-code-grant)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청](#requesting-tokens)
    - [토큰 관리](#managing-tokens)
    - [토큰 재발급(Refresh)](#refreshing-tokens)
    - [토큰 폐기(Revoking)](#revoking-tokens)
    - [토큰 정리(Purging)](#purging-tokens)
- [PKCE를 이용한 Authorization Code Grant](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청](#requesting-auth-pkce-grant-tokens)
- [Device Authorization Grant](#device-authorization-grant)
    - [디바이스 코드 그랜트 클라이언트 생성](#creating-a-device-authorization-grant-client)
    - [토큰 요청](#requesting-device-authorization-grant-tokens)
- [Password Grant](#password-grant)
    - [패스워드 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [사용자 프로바이더 커스터마이즈](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이즈](#customizing-the-username-field)
    - [비밀번호 유효성 검증 커스터마이즈](#customizing-the-password-validation)
- [Implicit Grant](#implicit-grant)
- [Client Credentials Grant](#client-credentials-grant)
- [Personal Access Tokens](#personal-access-tokens)
    - [Personal Access 클라이언트 생성](#creating-a-personal-access-client)
    - [사용자 프로바이더 커스터마이즈](#customizing-the-user-provider-for-pat)
    - [Personal Access Token 관리](#managing-personal-access-tokens)
- [라우트 보호](#protecting-routes)
    - [미들웨어를 이용한 보호](#via-middleware)
    - [액세스 토큰 전달 방식](#passing-the-access-token)
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

[Laravel Passport](https://github.com/laravel/passport)는 라라벨 애플리케이션을 위한 완전한 OAuth2 서버 구현을 몇 분 만에 제공해줍니다. 패스포트는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server)를 기반으로 만들어졌습니다.

> [!NOTE]
> 이 문서는 여러분이 이미 OAuth2에 대해 어느 정도 알고 있다는 것을 전제로 작성되었습니다. OAuth2에 대해 전혀 모른다면 계속해서 학습을 진행하기 전에 [용어](https://oauth2.thephpleague.com/terminology/)와 주요 특징을 먼저 익히는 것을 추천합니다.

<a name="passport-or-sanctum"></a>
### 패스포트와 생텀 중 어떤 것을 사용할까?

시작하기 전에, 여러분의 애플리케이션에 Laravel Passport와 [Laravel Sanctum](/docs/12.x/sanctum) 중 어떤 것이 더 적합할지 확인하는 것이 좋습니다. 만약 애플리케이션에 반드시 OAuth2 지원이 필요한 경우라면 Laravel Passport를 사용해야 합니다.

하지만 싱글 페이지 애플리케이션(SPA), 모바일 애플리케이션 인증, 또는 API 토큰 발급 등에 중점을 둔다면 [Laravel Sanctum](/docs/12.x/sanctum)을 사용하는 편이 좋습니다. Laravel Sanctum은 OAuth2를 지원하지는 않지만, 훨씬 간단하게 API 인증을 구현할 수 있도록 해줍니다.

<a name="installation"></a>
## 설치

`install:api` 아티즌 명령어를 통해 Laravel Passport를 설치할 수 있습니다:

```shell
php artisan install:api --passport
```

이 명령어는 OAuth2 클라이언트 및 액세스 토큰을 저장하는 데 필요한 데이터베이스 마이그레이션을 자동으로 퍼블리시하고 실행합니다. 또한, 보안성이 높은 액세스 토큰 생성을 위해 필요한 암호화 키도 생성합니다.

`install:api` 명령 실행 후에는 `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가해주어야 합니다. 이 트레이트를 사용하면 인증된 사용자의 토큰과 스코프를 확인할 수 있는 다양한 헬퍼 메서드를 사용할 수 있습니다:

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

마지막으로 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드의 `driver` 옵션을 `passport`로 설정해야 합니다. 이렇게 하면 API 요청 인증 시 Passport의 `TokenGuard`를 사용하게 됩니다:

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

패스포트를 애플리케이션 서버에 처음 배포할 때는 `passport:keys` 명령을 한 번 실행해야 할 수 있습니다. 이 명령은 패스포트가 액세스 토큰 생성에 사용하는 암호화 키를 생성하며, 생성된 키는 일반적으로 소스 제어에는 포함시키지 않습니다:

```shell
php artisan passport:keys
```

필요할 경우, 패스포트에서 사용할 키 파일 경로를 직접 지정할 수도 있습니다. 이를 위해서는 `Passport::loadKeysFrom` 메서드를 사용합니다. 보통 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다:

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
#### 환경 변수에서 키를 불러오기

또 다른 방법으로, `vendor:publish` 아티즌 명령어를 이용해 패스포트의 설정 파일을 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일을 퍼블리시한 뒤에는, 환경 변수로 애플리케이션의 암호화 키를 지정하면 됩니다:

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

패스포트를 새 주요 버전으로 업그레이드할 때에는 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼히 살펴보는 것이 중요합니다.

<a name="configuration"></a>
## 설정

<a name="token-lifetimes"></a>
### 토큰 만료 기간

패스포트는 기본적으로 1년 동안 유효한 장기 액세스 토큰을 발급합니다. 더 길거나 짧은 만료 기간을 원한다면 `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다:

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
> 패스포트가 사용하는 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며, 보기 용도로만 사용됩니다. 실제로 토큰이 발급될 때 만료 정보는 서명되고 암호화된 토큰 내부에 저장됩니다. 토큰을 무효화해야 할 경우에는 반드시 [토큰 폐기](#revoking-tokens)를 수행하세요.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

패스포트가 내부적으로 사용하는 모델을 여러분이 직접 정의한 모델로 확장하여 사용할 수도 있습니다. 이를 위해서는 우선 기본 Passport 모델을 상속받아 자신만의 모델을 만듭니다:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의했다면, `Laravel\Passport\Passport` 클래스의 메서드를 통해 커스텀 모델을 패스포트에서 사용하도록 지정할 수 있습니다. 보통 이 작업은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 수행합니다:

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

때때로 패스포트가 기본으로 등록하는 라우트를 직접 커스터마이즈하고 싶을 수 있습니다. 이때에는 먼저 애플리케이션의 `AppServiceProvider`의 `register` 메서드에서 `Passport::ignoreRoutes`를 호출해 패스포트가 기본 라우트를 등록하지 않도록 합니다:

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

이후 [패스포트 라우트 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 복사해서 자신의 애플리케이션 `routes/web.php` 파일에 붙여넣고 원하는 대로 수정할 수 있습니다:

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

OAuth2에서 Authorization Code Grant 방식은 많은 개발자들에게 가장 익숙한 인증 방식입니다. 이 방식에서는 클라이언트 애플리케이션이 사용자를 여러분의 서버로 리다이렉트시키고, 사용자는 해당 클라이언트에 액세스 토큰 발급을 승인(또는 거부)합니다.

먼저, 패스포트에 "authorization" 뷰를 어떻게 반환할지 알려주어야 합니다.

모든 authorization 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스의 메서드로 커스터마이즈 할 수 있습니다. 보통 이 작업은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 처리합니다:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 지정하는 경우...
    Passport::authorizationView('auth.oauth.authorize');

    // 클로저를 이용하여 렌더링 로직을 직접 작성하는 경우...
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

패스포트는 `/oauth/authorize` 라우트를 자동으로 등록하여 해당 뷰를 반환합니다. 여러분의 `auth.oauth.authorize` 템플릿에는, 권한을 승인하는 `passport.authorizations.approve` 라우트로 POST 요청을, 권한 허가를 거부하는 `passport.authorizations.deny` 라우트로 DELETE 요청을 보내는 폼이 포함되어 있어야 합니다. `passport.authorizations.approve` 및 `passport.authorizations.deny` 라우트에서는 `state`, `client_id`, `auth_token` 필드를 필요로 합니다.

<a name="managing-clients"></a>
### 클라이언트 관리

여러분의 애플리케이션의 API와 통합하려는 개발자들은 자신들의 애플리케이션(클라이언트)을 등록해야 합니다. 일반적으로 이는 애플리케이션 이름과 사용자가 권한을 승인한 뒤 리다이렉트할 URI를 제공하는 과정을 포함합니다.

<a name="managing-first-party-clients"></a>
#### 1차 파티(First-Party) 클라이언트

가장 간편하게 클라이언트를 생성하는 방법은 `passport:client` 아티즌 명령을 사용하는 것입니다. 이 명령어는 1차 파티 클라이언트 생성이나 OAuth2 기능 테스트를 위해 활용할 수 있습니다. 명령어를 실행하면, 패스포트가 클라이언트 정보를 입력받고 클라이언트 ID, 클라이언트 시크릿을 발급합니다:

```shell
php artisan passport:client
```

하나의 클라이언트에 여러 개의 리다이렉트 URI를 지정하고 싶은 경우, `passport:client` 명령 실행 시 URI 입력란에 쉼표(,)로 구분된 리스트를 입력하면 됩니다. 만약 일부 URI에 쉼표가 포함되어 있다면 URI 인코딩을 해줘야 합니다:

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 3차 파티(Third-Party) 클라이언트

애플리케이션의 사용자들은 `passport:client` 명령어를 직접 실행할 수 없으므로, `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드를 이용해 특정 사용자를 위한 클라이언트를 등록할 수 있습니다:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// 주어진 유저에 속하는 OAuth 앱 클라이언트 생성 예시...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// 해당 유저가 소유한 모든 OAuth 앱 클라이언트 목록 조회...
$clients = $user->oauthApps()->get();
```

`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. 사용자는 `$client->id`(클라이언트 ID)와 `$client->plainSecret`(클라이언트 시크릿)을 활용할 수 있습니다.

<a name="requesting-tokens"></a>
### 토큰 요청

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 권한 부여를 위한 리다이렉트

클라이언트가 생성되면, 개발자들은 클라이언트 ID와 시크릿을 이용해서 여러분의 애플리케이션에서 인가 코드와 액세스 토큰을 받을 수 있습니다. 먼저, 외부(소비) 애플리케이션은 다음과 같이 여러분의 `/oauth/authorize` 라우트로 리다이렉트 요청을 보냅니다:

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

`prompt` 파라미터를 통해 패스포트 애플리케이션의 인증 동작을 제어할 수 있습니다.

만약 `prompt` 값이 `none`이면, 사용자가 패스포트 애플리케이션에 이미 인증되지 않은 경우 인증 오류가 발생합니다. `consent` 값인 경우에는 이전에 모든 스코프에 대해 권한을 허용한 애플리케이션일지라도 항상 권한 승인 화면이 표시됩니다. `login` 값인 경우, 이미 세션이 있더라도 반드시 다시 로그인하도록 합니다.

`prompt` 값이 제공되지 않으면, 사용자가 해당 스코프에 대해 지정된 애플리케이션의 접근을 아직 승인하지 않은 경우에만 권한 승인이 요청됩니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 패스포트에서 이미 정의되어 있습니다. 별도로 직접 이 라우트를 추가할 필요는 없습니다.

<a name="approving-the-request"></a>
#### 요청 승인하기

인가(authorization) 요청을 받을 때, 패스포트는 `prompt` 파라미터 값에 따라 자동으로 적절하게 대응하고, 사용자에게 권한 요청 승인 또는 거부를 위한 화면을 표시할 수 있습니다. 사용자가 요청을 승인하면, 소비(외부) 애플리케이션에서 지정한 `redirect_uri`로 곧바로 리다이렉트됩니다. 이때 `redirect_uri` 값은 클라이언트 생성 시 등록한 리다이렉트 URL과 반드시 일치해야 합니다.

1차 파티(First-Party) 클라이언트와 같이 권한 승인을 생략하고 싶은 경우도 있을 수 있습니다. 이때에는 [Client 모델 오버라이드](#overriding-default-models) 후 `skipsAuthorization` 메서드를 정의해주면 됩니다. `skipsAuthorization`이 `true`를 반환하면 해당 클라이언트는 승인 화면을 건너뛰고 즉시 지정한 `redirect_uri`로 리다이렉트됩니다(단, 소비 애플리케이션이 `prompt`를 명시적으로 지정한 경우는 예외):

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 해당 클라이언트가 권한 요청 화면을 생략할지 판단합니다.
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
#### 인가 코드를 액세스 토큰으로 변환

사용자가 권한 요청을 승인하면, 소비 애플리케이션은 사용자를 자신 쪽으로 리다이렉트시킵니다. 이때 소비자 측에서는 먼저 리다이렉트 전에 세션에 저장했던 `state` 파라미터 값을 검증해야 합니다. 만약 `state` 값이 일치하면, 인가 코드와 함께 액세스 토큰을 요청하는 `POST` 요청을 여러분의 애플리케이션으로 보냅니다. 이 요청에는 사용자가 승인했을 때 발급된 인가 코드가 포함되어야 합니다:

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

`/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in` 값에는 액세스 토큰이 만료될 때까지 남은 시간이(초 단위로) 담겨 있습니다.

> [!NOTE]
> `/oauth/authorize` 라우트와 마찬가지로 `/oauth/token` 라우트는 패스포트에서 이미 정의되어 있으므로, 따로 직접 라우트를 추가할 필요는 없습니다.

<a name="managing-tokens"></a>
### 토큰 관리

`Laravel\Passport\HasApiTokens` 트레이트의 `tokens` 메서드를 이용하면 사용자가 승인한 토큰 목록을 조회할 수 있습니다. 예를 들어, 대시보드 등에서 사용자가 연동한 외부 애플리케이션 목록과 연결 상태를 보여주는 용도로 활용할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 해당 사용자의 유효한 토큰을 모두 조회
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// 사용자가 연동한 외부 OAuth 앱 클라이언트들의 목록을 조회
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
### 토큰 재발급(Refresh)

애플리케이션이 단기간(짧은 만료 기간)의 액세스 토큰을 발급하는 경우, 사용자는 최초 발급 시 제공된 리프레시 토큰을 이용해 액세스 토큰을 재발급 받을 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // confidential(비공개) 클라이언트에서만 필수...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 `/oauth/token` 라우트 역시 `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in` 값에는 해당 액세스 토큰 만료까지 남은 초(second)가 들어 있습니다.

<a name="revoking-tokens"></a>
### 토큰 폐기(Revoking)

`Laravel\Passport\Token` 모델의 `revoke` 메서드를 사용하면 액세스 토큰을 폐기할 수 있습니다. 리프레시 토큰 역시 `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드로 폐기할 수 있습니다:

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// 액세스 토큰 폐기
$token->revoke();

// 해당 토큰의 리프레시 토큰도 폐기
$token->refreshToken?->revoke();

// 사용자의 모든 토큰을 일괄 폐기
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### 토큰 정리(Purging)

토큰이 폐기 또는 만료된 뒤, 불필요한 토큰을 데이터베이스에서 삭제(purging)할 수 있습니다. 패스포트에서 제공하는 `passport:purge` 아티즌 명령어를 사용하세요:

```shell
# 폐기되었거나 만료된 토큰, 인증 코드, 디바이스 코드 모두 삭제...
php artisan passport:purge

# 6시간 이상 만료된 토큰만 삭제...
php artisan passport:purge --hours=6

# 폐기된 토큰, 인증 코드, 디바이스 코드만 삭제...
php artisan passport:purge --revoked

# 만료된 토큰, 인증 코드, 디바이스 코드만 삭제...
php artisan passport:purge --expired
```

또한, 애플리케이션의 `routes/console.php` 파일에서 [스케줄링된 작업](/docs/12.x/scheduling)을 등록해, 토큰 정리를 자동화할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## PKCE를 이용한 Authorization Code Grant

"Proof Key for Code Exchange(PKCE)" 기반의 Authorization Code Grant는 싱글 페이지 애플리케이션이나 모바일 애플리케이션에서 안전하게 API에 접근하게 하는 인증 방식입니다. 이 방식은 클라이언트 시크릿이 유출되거나 인가 코드가 공격자에게 가로채일 위험이 있을 때 특히 적합합니다. 인가 코드와 액세스 토큰 교환 시 클라이언트 시크릿 대신 "코드 베리파이어(code verifier)"와 "코드 챌린지(code challenge)"의 조합을 사용합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성

PKCE 기반 Authorization Code Grant로 토큰을 발급받으려면, PKCE를 지원하는 신규 클라이언트를 생성해야 합니다. 이를 위해 `passport:client` 아티즌 명령의 `--public` 옵션을 사용하세요:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청

<a name="code-verifier-code-challenge"></a>
#### 코드 베리파이어와 코드 챌린지

이 인증 방식에서는 클라이언트 시크릿을 제공하지 않으므로, 개발자는 토큰 요청에 사용할 코드 베리파이어(code verifier)와 코드 챌린지(code challenge)를 직접 만들어야 합니다.

코드 베리파이어는 43~128자의 랜덤 문자열이어야 하며, 알파벳, 숫자, 그리고 `"-"`, `"."`, `"_"`, `"~"` 문자만 포함해야 합니다(RFC 7636 요구사항).

코드 챌린지는 URL 및 파일명에 안전한 Base64 인코딩 문자열이어야 하며, 끝의 `'='` 문자를 제거하고 줄바꿈, 공백, 기타 불필요한 문자가 없어야 합니다.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>

#### 인가를 위한 리디렉션

클라이언트를 생성한 후, 클라이언트 ID와 생성된 코드 검증자(code verifier), 코드 챌린지(code challenge)를 사용해 애플리케이션에서 인가 코드와 엑세스 토큰을 요청할 수 있습니다. 먼저, 외부 애플리케이션은 여러분의 애플리케이션의 `/oauth/authorize` 경로로 리디렉션 요청을 보내야 합니다.

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
#### 인가 코드를 액세스 토큰으로 교환하기

사용자가 인가 요청을 승인하면, 사용자는 외부 애플리케이션으로 다시 리디렉션됩니다. 이 때, 외부 애플리케이션(컨슈머)은 `state` 파라미터가 리디렉션 이전에 저장한 값과 일치하는지 확인해야 합니다. 이는 표준 인가 코드 그랜트 방식과 동일합니다.

`state` 파라미터가 일치한다면, 컨슈머는 액세스 토큰을 요청하는 `POST` 요청을 여러분의 애플리케이션에 보내야 합니다. 이 요청에는 사용자가 인가 요청을 승인할 때 발급된 인가 코드와, 최초에 생성한 코드 검증자(code verifier)가 포함되어야 합니다.

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

OAuth2의 디바이스 인가 그랜트는 TV나 게임 콘솔처럼 브라우저가 없거나 입력이 제한된 디바이스에서도 "디바이스 코드(device code)"를 교환하여 액세스 토큰을 얻을 수 있도록 해줍니다. 디바이스 플로우를 사용할 때 디바이스 클라이언트는 사용자에게 컴퓨터나 스마트폰 등 보조 기기를 이용해 여러분의 서버에 접속하여 제공된 "유저 코드(user code)"를 입력하고, 접근 요청을 승인하거나 거부하도록 안내합니다.

먼저, Passport가 "유저 코드"와 "인가" 뷰를 어떻게 반환해야 하는지 알려야 합니다.

모든 인가 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스의 적절한 메서드를 사용해 커스터마이즈할 수 있습니다. 보통 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 직접 지정하는 경우...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // 클로저를 전달하는 경우...
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

Passport는 이 뷰를 반환하는 라우트를 자동으로 정의해 줍니다. `auth.oauth.device.user-code` 템플릿에는 `passport.device.authorizations.authorize` 라우트로 GET 요청을 보내는 폼을 포함해야 합니다. 이 라우트는 `user_code` 쿼리 파라미터를 기대합니다.

`auth.oauth.device.authorize` 템플릿에는 인가를 승인하기 위한 POST 요청을 `passport.device.authorizations.approve` 라우트로 보내는 폼과, 인가를 거부하기 위한 DELETE 요청을 `passport.device.authorizations.deny` 라우트로 보내는 폼을 각각 포함해야 합니다. 두 라우트는 모두 `state`, `client_id`, `auth_token` 필드를 필요로 합니다.

<a name="creating-a-device-authorization-grant-client"></a>
### 디바이스 인가 그랜트 클라이언트 생성

디바이스 인가 그랜트를 통해 토큰을 발급하려면 먼저 디바이스 플로우가 활성화된 클라이언트를 생성해야 합니다. 이를 위해 `passport:client` 아티즌 명령어에 `--device` 옵션을 사용할 수 있습니다. 이 명령어는 1st-party(일차) 디바이스 플로우 활성화 클라이언트를 생성하고, 클라이언트 ID와 secret을 제공합니다.

```shell
php artisan passport:client --device
```

또는, `ClientRepository` 클래스의 `createDeviceAuthorizationGrantClient` 메서드를 이용해 특정 사용자에 속한 3rd-party(서드파티) 클라이언트를 등록할 수도 있습니다.

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

클라이언트가 생성되면, 개발자는 클라이언트 ID를 사용해 애플리케이션에서 디바이스 코드를 요청할 수 있습니다. 우선, 사용 중인 디바이스가 애플리케이션의 `/oauth/device/code` 경로로 `POST` 요청을 보내 디바이스 코드를 발급받아야 합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 코드는 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in`은 디바이스 코드가 만료되기까지 남은 시간(초), `interval`은 `/oauth/token` 경로를 폴링(polling)할 때 속도 제한(rate limit) 오류를 방지하기 위해 디바이스가 대기해야 하는 최소 시간(초)을 의미합니다.

> [!NOTE]
> `/oauth/device/code` 라우트는 Passport에서 이미 정의되어 있습니다. 별도로 정의할 필요가 없습니다.

<a name="user-code"></a>
#### 인증 URI와 유저 코드 표시하기

디바이스 코드 요청이 성공하면, 사용 중인 디바이스는 사용자에게 안내 메시지를 통해 다른 기기에서 제공된 `verification_uri`로 접속하게 하고, 인가 요청을 승인하기 위해 `user_code`를 입력하도록 해야 합니다.

<a name="polling-token-request"></a>
#### 토큰 요청 폴링

사용자가 별도의 기기를 이용해 접근(또는 거부) 권한을 부여할 것이므로, 디바이스 쪽에서는 사용자가 요청에 응답할 때까지 여러분의 애플리케이션의 `/oauth/token` 경로를 폴링(polling)해야 합니다. 폴링 시에는 디바이스 코드 요청의 JSON 응답에 포함된 최소 `interval` 값만큼 대기하면서 속도 제한 오류를 방지해야 합니다.

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // 필요시(비공개 클라이언트)
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

만약 사용자가 인가 요청을 승인했다면 `access_token`, `refresh_token`, `expires_in` 정보를 포함한 JSON 응답을 반환합니다. `expires_in`은 액세스 토큰이 만료될 때까지 남은 시간(초)입니다.

<a name="password-grant"></a>
## 패스워드 그랜트(Password Grant)

> [!WARNING]
> 패스워드 그랜트 토큰은 더 이상 사용을 권장하지 않습니다. 대신 [OAuth2 서버에서 현재 권장하는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하는 것이 좋습니다.

OAuth2의 패스워드 그랜트는 모바일 애플리케이션 등 여러분의 1st-party 클라이언트에서 이메일 주소나 사용자명, 비밀번호로 액세스 토큰을 발급받을 수 있게 해줍니다. 이를 통해 사용자는 OAuth2 인가 코드 리디렉션 플로우 없이도 보안적으로 액세스 토큰을 얻을 수 있습니다.

패스워드 그랜트를 활성화하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enablePasswordGrant` 메서드를 호출하십시오.

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

패스워드 그랜트를 통해 토큰을 발급하려면 먼저 패스워드 그랜트 클라이언트를 생성해야 합니다. 이를 위해 `passport:client` 아티즌 명령어에 `--password` 옵션을 사용합니다.

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청하기

그랜트를 활성화하고 패스워드 그랜트 클라이언트를 생성했다면, 사용자의 이메일 주소와 비밀번호로 `/oauth/token` 라우트에 `POST` 요청을 보내 액세스 토큰을 발급받을 수 있습니다. 이 라우트는 Passport에서 미리 등록되어 있으므로 별도로 정의할 필요가 없습니다. 요청이 성공하면 서버에서 `access_token`과 `refresh_token`이 포함된 JSON 응답을 받게 됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // 필요시(비공개 클라이언트)
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

> [!NOTE]
> 액세스 토큰은 기본적으로 수명이 깁니다. 필요하다면 [최대 액세스 토큰 수명 설정](#configuration)도 가능합니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청하기

패스워드 그랜트 또는 클라이언트 크레덴셜 그랜트를 사용할 때, 애플리케이션이 지원하는 모든 스코프에 대해 토큰을 승인받고 싶을 수도 있습니다. 이때는 `*` 스코프를 요청하면 됩니다. `*` 스코프를 요청하면 토큰 인스턴스의 `can` 메서드는 항상 `true`를 반환합니다. 단, 이 스코프는 `password` 또는 `client_credentials` 그랜트로 발급한 토큰에만 할당할 수 있습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // 필요시(비공개 클라이언트)
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### 사용자 프로바이더 커스터마이징

애플리케이션에서 [둘 이상 인증 사용자 프로바이더](/docs/12.x/authentication#introduction)를 활용하는 경우, `artisan passport:client --password` 명령어로 패스워드 그랜트 클라이언트를 만들 때 `--provider` 옵션으로 사용할 사용자 프로바이더를 지정할 수 있습니다. 전달한 프로바이더 이름은 `config/auth.php` 파일에 정의된 프로바이더와 일치해야 합니다. 이후 [미들웨어로 라우트 보호](#multiple-authentication-guards)까지 적용하면, 각 가드의 프로바이더 별로 접근 권한을 제한할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명 필드 커스터마이징

패스워드 그랜트로 인증할 때, Passport는 인증 가능한 모델의 `email` 속성을 "사용자명"으로 사용합니다. 그러나, 원하는 경우 모델에 `findForPassport` 메서드를 정의하여 해당 동작을 커스터마이징할 수 있습니다.

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

패스워드 그랜트로 인증할 때 Passport는 모델의 `password` 속성을 사용해 주어진 비밀번호를 검증합니다. 만약 모델에 `password` 속성이 없거나 비밀번호 검증 로직을 직접 커스터마이즈하고 싶다면, 모델에 `validateForPassportPasswordGrant` 메서드를 정의할 수 있습니다.

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
> 임플리싯 그랜트 토큰은 더 이상 사용을 권장하지 않습니다. 대신 [OAuth2 서버에서 현재 권장하는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하는 것이 좋습니다.

임플리싯 그랜트는 인가 코드 그랜트와 유사하지만, 토큰을 획득할 때 인가 코드를 별도로 교환하지 않고, 바로 클라이언트에 반환합니다. 이 방식은 클라이언트 자격 증명을 안전하게 저장할 수 없는 자바스크립트나 모바일 애플리케이션에서 주로 사용됩니다. 임플리싯 그랜트를 활성화하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enableImplicitGrant`를 호출하십시오.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

임플리싯 그랜트 방식으로 토큰을 발급하려면, 먼저 임플리싯 그랜트 클라이언트를 생성해야 합니다. 이는 `passport:client` 아티즌 명령어에 `--implicit` 옵션을 사용하여 생성할 수 있습니다.

```shell
php artisan passport:client --implicit
```

그랜트를 활성화하고 임플리싯 클라이언트가 준비됐다면, 개발자는 클라이언트 ID를 사용해 애플리케이션에서 액세스 토큰을 요청할 수 있습니다. 외부 애플리케이션은 아래와 같이 `/oauth/authorize` 경로로 리디렉션 요청을 보내야 합니다.

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
> `/oauth/authorize` 라우트는 Passport에서 이미 정의되어 있습니다. 별도로 정의할 필요가 없습니다.

<a name="client-credentials-grant"></a>
## 클라이언트 크레덴셜 그랜트(Client Credentials Grant)

클라이언트 크레덴셜 그랜트는 서버-대-서버(머신 간) 인증에 적합합니다. 예를 들어, 예약된 작업이 API를 통해 유지보수 작업을 수행할 때 이 방식을 사용할 수 있습니다.

이 그랜트로 토큰을 발급하려면, 먼저 클라이언트 크레덴셜 그랜트 클라이언트를 생성해야 합니다. 이를 위해 `passport:client` 아티즌 명령어에 `--client` 옵션을 사용합니다.

```shell
php artisan passport:client --client
```

다음으로, 라우트에 `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 할당합니다.

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하며, 클라이언트가 리소스 소유자일 때만 접근 가능...
})->middleware(EnsureClientIsResourceOwner::class);
```

특정 스코프에 대해서만 접근을 제한하려면, `using` 메서드에 필요한 스코프 목록을 전달할 수 있습니다.

```php
Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하고, 클라이언트가 리소스 소유자이며 "servers:read"와 "servers:create" 스코프가 모두 있을 때만 접근 가능...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create');
```

<a name="retrieving-tokens"></a>
### 토큰 조회하기

이 그랜트 타입으로 토큰을 받으려면, `oauth/token` 엔드포인트로 요청을 보내십시오.

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

사용자가 일반적인 인가 코드 리디렉션 플로우를 거치지 않고도 직접 액세스 토큰을 발급하고 싶을 수도 있습니다. 애플리케이션의 UI를 통해 사용자 스스로 토큰을 발급하도록 허용하면, API 실험이나 간단한 액세스 토큰 발급이 필요할 때 유용하게 사용할 수 있습니다.

> [!NOTE]
> 애플리케이션에서 개인 액세스 토큰 발급만 필요하다면, 라라벨의 가볍고 1st-party 라이브러리인 [Laravel Sanctum](/docs/12.x/sanctum) 사용을 검토해보십시오.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성

개인 액세스 토큰을 발급하려면, 우선 개인 액세스 클라이언트를 생성해야 합니다. `passport:client` 아티즌 명령어에 `--personal` 옵션을 추가해 실행하면 됩니다. 이미 `passport:install` 명령어를 실행한 경우에는 이 과정을 반복할 필요가 없습니다.

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### 사용자 프로바이더 커스터마이징

애플리케이션에서 둘 이상 [인증 사용자 프로바이더](/docs/12.x/authentication#introduction)를 사용한다면, `artisan passport:client --personal` 명령어에 `--provider` 옵션을 추가해 개인 액세스 그랜트 클라이언트가 사용할 프로바이더를 지정할 수 있습니다. 지정하는 이름은 `config/auth.php`에 정의된 프로바이더와 일치해야 합니다. 이후 [미들웨어로 라우트 보호](#multiple-authentication-guards)까지 적용하면, 각 가드의 프로바이더 별로 사용자를 제한할 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리

개인 액세스 클라이언트를 생성한 후에는, `App\Models\User` 모델 인스턴스가 제공하는 `createToken` 메서드로 토큰을 발급할 수 있습니다. `createToken` 메서드는 첫 번째 인수로 토큰 이름을, 두 번째 인수로 [스코프](#token-scopes) 배열(선택 사항)을 받습니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 스코프 없이 토큰 생성...
$token = $user->createToken('My Token')->accessToken;

// 스코프를 포함해 토큰 생성...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// 모든 스코프로 토큰 생성...
$token = $user->createToken('My Token', ['*'])->accessToken;

// 사용자 소유의 모든 유효한 개인 액세스 토큰 조회...
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

Passport는 수신 요청에서 액세스 토큰을 검증해주는 [인증 가드](/docs/12.x/authentication#adding-custom-guards)를 제공합니다. `api` 가드가 `passport` 드라이버를 사용하도록 구성했다면, 유효한 액세스 토큰이 필요한 라우트에 `auth:api` 미들웨어만 지정하면 됩니다.

```php
Route::get('/user', function () {
    // API 인증된 사용자만 이 라우트에 접근할 수 있습니다.
})->middleware('auth:api');
```

> [!WARNING]
> [클라이언트 크레덴셜 그랜트](#client-credentials-grant)를 사용할 경우, 라우트 보호를 위해 `auth:api` 미들웨어 대신 [Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner 미들웨어](#client-credentials-grant)를 사용해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 다중 인증 가드

애플리케이션이 서로 다른 유형의 사용자(예: 각각 다른 Eloquent 모델 사용)를 인증해야 한다면, 애플리케이션의 각 사용자 프로바이더 유형별로 가드 구성을 정의해야 합니다. 이를 통해 각 프로바이더별로 요청을 보호할 수 있습니다. 아래는 `config/auth.php` 파일에 예시로 추가한 가드 설정입니다.

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

아래와 같이, `customers` 사용자 프로바이더를 사용하는 `api-customers` 가드를 활용해 특정 라우트를 인증할 수 있습니다.

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport에서 여러 사용자 프로바이더를 활용하는 방법에 대해서는 [개인 액세스 토큰 문서](#customizing-the-user-provider-for-pat), [패스워드 그랜트 문서](#customizing-the-user-provider)를 참고하십시오.

<a name="passing-the-access-token"></a>
### Access Token 전달 방식

Passport로 보호되는 라우트를 호출할 때, API 컨슈머는 요청의 `Authorization` 헤더에 액세스 토큰을 `Bearer` 토큰 방식으로 지정해야 합니다. 예를 들어, `Http` 파사드를 사용할 때는 다음과 같이 요청을 보낼 수 있습니다.

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

스코프(scope)는 여러분의 API 클라이언트가 계정에 접근할 때 특정 권한만을 요청하도록 제한할 수 있는 기능입니다. 예를 들어, 이커머스 애플리케이션을 만들었다면, 모든 API 컨슈머가 주문을 생성할 필요는 없습니다. 대신, 주문 상태 조회 등 제한된 권한만 얻을 수 있도록 할 수 있습니다. 즉, 스코프는 사용자들이 외부 애플리케이션이 자신을 대신해 할 수 있는 행동을 구체적으로 제한할 수 있게 해줍니다.

<a name="defining-scopes"></a>
### 스코프 정의하기

애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `Passport::tokensCan` 메서드를 사용해 API의 스코프를 정의할 수 있습니다. `tokensCan` 메서드는 스코프 이름과 설명(배열)을 받으며, 이 설명은 인가 승인 화면에서 사용자에게 안내 메시지로 표시됩니다.

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

### 기본 스코프

클라이언트가 특정 스코프를 요청하지 않은 경우, `defaultScopes` 메서드를 사용하여 Passport 서버가 액세스 토큰에 기본 스코프를 자동으로 부여하도록 설정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

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

Authorization code grant로 액세스 토큰을 요청할 때, 소비자는 원하는 스코프를 `scope` 쿼리 문자열 파라미터로 지정해야 합니다. `scope` 파라미터에는 공백으로 구분된 스코프 목록을 입력합니다.

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
#### Personal Access Token 발급 시

`App\Models\User` 모델의 `createToken` 메서드를 통해 personal access token을 발급할 때, 두 번째 인수로 원하는 스코프의 배열을 전달할 수 있습니다.

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 확인하기

Passport에는 인증된 요청의 토큰이 특정 스코프를 가지고 있는지 확인할 수 있는 두 개의 미들웨어가 제공됩니다.

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어를 라우트에 할당하면, 해당 요청의 액세스 토큰에 나열된 모든 스코프가 포함되어 있는지 확인할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // 액세스 토큰에 "orders:read"와 "orders:create" 스코프가 모두 포함되어 있어야 합니다...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create');
```

<a name="check-for-any-scopes"></a>
#### 일부 스코프 포함 여부 확인

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어는 해당 요청의 액세스 토큰이 나열된 스코프 중 *하나 이상*을 가지고 있는지 확인합니다.

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // 액세스 토큰에 "orders:read" 또는 "orders:create" 중 하나 이상의 스코프가 있어야 합니다...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create');
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인하기

액세스 토큰 인증이 완료된 요청에서, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드를 사용해 해당 토큰이 특정 스코프를 가지고 있는지 추가적으로 확인할 수 있습니다.

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

`scopeIds` 메서드는 정의된 모든 ID/이름의 배열을 반환합니다.

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

`scopes` 메서드는 정의된 모든 스코프를 `Laravel\Passport\Scope` 인스턴스의 배열로 반환합니다.

```php
Passport::scopes();
```

`scopesFor` 메서드는 지정한 ID/이름에 해당하는 `Laravel\Passport\Scope` 인스턴스의 배열을 반환합니다.

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

특정 스코프가 정의되어 있는지 여부는 `hasScope` 메서드로 판단할 수 있습니다.

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA 인증

API를 구축할 때, 자바스크립트 애플리케이션에서 직접 자신의 API를 소비할 수 있으면 매우 유용합니다. 이러한 API 개발 방식은 본인이 외부에 공개하는 것과 동일한 API를 본인 애플리케이션에서 직접 이용하게 해 줍니다. 같은 API를 웹 애플리케이션, 모바일 애플리케이션, 써드파티 애플리케이션, 그리고 패키지 매니저에 배포할 수 있는 SDK 등이 함께 사용할 수 있습니다.

일반적으로 자바스크립트 애플리케이션에서 API를 이용하려면, 액세스 토큰을 애플리케이션으로 직접 전달한 뒤 모든 요청에 해당 토큰을 실어 보내야 합니다. 하지만 Passport에서는 이를 처리해주는 미들웨어를 제공합니다. `bootstrap/app.php` 파일의 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어를 추가하기만 하면 됩니다.

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어가 미들웨어 스택의 마지막에 위치하도록 반드시 확인해야 합니다.

이 미들웨어는 응답에 `laravel_token` 쿠키를 추가합니다. 이 쿠키는 암호화된 JWT를 담고 있으며, Passport가 JavaScript 애플리케이션에서 오는 API 요청을 인증하는 데 사용합니다. JWT의 수명은 `session.lifetime` 설정 값과 동일합니다. 이제 브라우저가 모든 후속 요청에 자동으로 쿠키를 포함하므로, 명시적으로 액세스 토큰을 전송하지 않아도 애플리케이션의 API에 요청할 수 있습니다.

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이즈

필요하다면, `Passport::cookie` 메서드를 사용해 `laravel_token` 쿠키의 이름을 변경할 수 있습니다. 이 메서드는 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

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

이 인증 방식을 사용할 때는 요청에 유효한 CSRF 토큰 헤더가 반드시 포함되어야 합니다. 라라벨의 스켈레톤 애플리케이션과 모든 스타터 킷에 포함된 기본 JavaScript 구성에는 [Axios](https://github.com/axios/axios) 인스턴스가 들어 있으며, 이 인스턴스는 암호화된 `XSRF-TOKEN` 쿠키 값을 자동으로 사용해 동일 오리진 요청에 `X-XSRF-TOKEN` 헤더를 담아 보냅니다.

> [!NOTE]
> `X-XSRF-TOKEN` 대신 `X-CSRF-TOKEN` 헤더를 전송하려면, 반드시 `csrf_token()`이 반환하는 암호화되지 않은 토큰을 사용해야 합니다.

<a name="events"></a>
## 이벤트

Passport는 액세스 토큰 및 리프레시 토큰을 발급할 때마다 이벤트를 발생시킵니다. 이러한 이벤트를 [리스닝](/docs/12.x/events)하여, 데이터베이스의 다른 액세스 토큰을 정리(Prune)하거나 폐기(Revoked)할 수 있습니다.

<div class="overflow-auto">

| 이벤트 이름 |
| --- |
| `Laravel\Passport\Events\AccessTokenCreated` |
| `Laravel\Passport\Events\AccessTokenRevoked` |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## 테스트

Passport의 `actingAs` 메서드를 사용하면, 현재 인증된 사용자와 부여할 스코프를 지정할 수 있습니다. 이 메서드의 첫 번째 인수는 사용자 인스턴스이며, 두 번째 인수는 사용자 토큰에 부여할 스코프의 배열입니다.

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

Passport의 `actingAsClient` 메서드는, 현재 인증된 클라이언트와 부여할 스코프를 지정할 때 사용할 수 있습니다. 이 메서드의 첫 번째 인수는 클라이언트 인스턴스이고, 두 번째 인수는 클라이언트 토큰에 부여할 스코프의 배열입니다.

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