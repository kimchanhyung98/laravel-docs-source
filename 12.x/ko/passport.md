# 라라벨 패스포트 (Laravel Passport)

- [소개](#introduction)
    - [패스포트와 샹텀 중 어떤 것을 사용할까?](#passport-or-sanctum)
- [설치](#installation)
    - [패스포트 배포](#deploying-passport)
    - [패스포트 업그레이드](#upgrading-passport)
- [구성](#configuration)
    - [토큰 만료 시간](#token-lifetimes)
    - [기본 모델 오버라이드](#overriding-default-models)
    - [기본 라우트 오버라이드](#overriding-routes)
- [Authorization Code Grant](#authorization-code-grant)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청](#requesting-tokens)
    - [토큰 관리](#managing-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [PKCE가 적용된 Authorization Code Grant](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청](#requesting-auth-pkce-grant-tokens)
- [디바이스 인증 그랜트(Device Authorization Grant)](#device-authorization-grant)
    - [디바이스 코드 그랜트 클라이언트 생성](#creating-a-device-authorization-grant-client)
    - [토큰 요청](#requesting-device-authorization-grant-tokens)
- [Password Grant](#password-grant)
    - [패스워드 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [사용자 제공자 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 커스터마이징](#customizing-the-password-validation)
- [암시적 그랜트(Implicit Grant)](#implicit-grant)
- [클라이언트 크레덴셜 그랜트(Client Credentials Grant)](#client-credentials-grant)
- [개인 액세스 토큰(Personal Access Tokens)](#personal-access-tokens)
    - [개인 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [Personal Access Token용 사용자 제공자 커스터마이징](#customizing-the-user-provider-for-pat)
    - [개인 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어로 보호](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의](#defining-scopes)
    - [기본 스코프 설정](#default-scope)
    - [토큰에 스코프 할당](#assigning-scopes-to-tokens)
    - [스코프 확인](#checking-scopes)
- [SPA 인증](#spa-authentication)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Passport](https://github.com/laravel/passport)는 라라벨 애플리케이션에 몇 분 만에 완전한 OAuth2 서버 구현체를 제공합니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server) 위에 구축되어 있습니다.

> [!NOTE]
> 본 문서는 여러분이 이미 OAuth2에 익숙하다는 가정 하에 작성되었습니다. OAuth2에 대해 잘 모른다면, 진행하기 전에 [용어 설명](https://oauth2.thephpleague.com/terminology/) 및 전반적인 OAuth2 기능을 먼저 숙지해 보시기 바랍니다.

<a name="passport-or-sanctum"></a>
### 패스포트와 샹텀 중 어떤 것을 사용할까?

시작하기 전에, 여러분의 애플리케이션에 Laravel Passport와 [Laravel Sanctum](/docs/12.x/sanctum) 중 어느 것이 더 적합한지 판단해볼 필요가 있습니다. 만약 여러분의 애플리케이션이 반드시 OAuth2 지원이 필요하다면 Laravel Passport 사용을 권장합니다.

반면, 싱글 페이지 애플리케이션(SPA), 모바일 애플리케이션의 인증이나 API 토큰 발급만 필요하다면 [Laravel Sanctum](/docs/12.x/sanctum) 사용을 추천합니다. Laravel Sanctum은 OAuth2는 지원하지 않지만, 훨씬 간단하게 API 인증 기능을 개발할 수 있습니다.

<a name="installation"></a>
## 설치

Laravel Passport는 `install:api` 아티즌 명령어로 설치할 수 있습니다.

```shell
php artisan install:api --passport
```

이 명령어를 실행하면 OAuth2 클라이언트와 액세스 토큰을 저장할 데이터베이스 테이블을 만들기 위한 마이그레이션을 퍼블리시 및 실행합니다. 또한, 보안 액세스 토큰 생성을 위한 암호화 키도 생성됩니다.

`install:api` 명령어를 실행한 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가해주세요. 이 트레이트는 인증된 사용자의 토큰 및 스코프를 쉽게 확인할 수 있는 헬퍼 메서드들을 제공합니다.

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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 추가하고, `driver` 옵션을 `passport`로 지정하세요. 이렇게 하면 API 요청을 인증할 때 Passport의 `TokenGuard`를 사용하게 됩니다.

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

애플리케이션 서버에 Passport를 처음 배포할 때는 `passport:keys` 명령어를 실행해야 합니다. 이 명령어는 액세스 토큰 생성을 위해 필요한 암호화 키를 생성합니다. 생성된 키는 일반적으로 소스 제어에는 포함하지 않습니다.

```shell
php artisan passport:keys
```

필요하다면 Passport 키를 로드할 경로를 지정할 수 있습니다. 이를 위해 `Passport::loadKeysFrom` 메서드를 사용할 수 있으며, 보통 이 코드는 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

또는, `vendor:publish` 아티즌 명령어를 통해 Passport의 설정 파일을 퍼블리시 한 다음에

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일을 퍼블리시한 후에는, 환경 변수에 암호화 키를 정의하여 Passport에서 키를 로드할 수 있습니다.

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

Passport의 새로운 주요 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼히 확인하는 것을 권장합니다.

<a name="configuration"></a>
## 구성

<a name="token-lifetimes"></a>
### 토큰 만료 시간

Passport는 기본적으로 1년 후 만료되는 장기간 액세스 토큰을 발급합니다. 토큰 만료 시간을 더 길거나 짧게 설정하고 싶다면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

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
> Passport의 데이터베이스 테이블에서 `expires_at` 컬럼은 읽기 전용이며 단순 표시에만 사용됩니다. 실제 토큰 발급 시 만료 정보는 서명 및 암호화된 토큰에 저장됩니다. 토큰을 무효화하려면 반드시 [토큰 폐기](#revoking-tokens) 기능을 이용해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Passport가 내부적으로 사용하는 모델을 확장(Customizing)하려면, 직접 모델을 정의하고 Passport의 해당 모델을 상속하세요.

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의한 후에는 `Laravel\Passport\Passport` 클래스를 통해 Passport에게 커스텀 모델을 사용하도록 알려주어야 합니다. 보통 이 코드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 작성합니다.

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
### 기본 라우트 오버라이드

필요에 따라 Passport가 기본으로 정의한 라우트를 커스터마이즈(오버라이드) 하고 싶을 때가 있습니다. 이를 위해서는 먼저 `AppServiceProvider`의 `register` 메서드에 `Passport::ignoreRoutes`를 추가하여 Passport가 라우트를 등록하지 않도록 해야 합니다.

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

그 후, [Passport의 routes 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 여러분의 애플리케이션 `routes/web.php`로 복사한 뒤 원하는 대로 수정할 수 있습니다.

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

OAuth2를 사용하는 개발자 대부분은 Authorization Code(인가 코드) 방식을 익숙하게 사용합니다. 이 방식에서는 클라이언트 애플리케이션이 사용자를 여러분의 서버로 리다이렉트시키고, 사용자가 클라이언트에 액세스 토큰 발급 권한을 허용(혹은 거부)하게 됩니다.

먼저, Passport에 우리가 사용할 "authorization" 뷰를 어떻게 반환할지 알려주어야 합니다.

authorization 뷰의 렌더링 로직은 `Laravel\Passport\Passport` 클래스의 메서드를 사용해 자유롭게 커스터마이즈할 수 있습니다. 일반적으로 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 다음과 같이 작성합니다.

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

    // 클로저를 활용하여 반환하는 방법...
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

Passport는 자동으로 `/oauth/authorize` 라우트를 정의해 이 뷰를 반환합니다. `auth.oauth.authorize` 템플릿에는 인가를 승인하는 경우 `passport.authorizations.approve` 라우트로 POST 요청을 보내는 form과, 거부하는 경우 `passport.authorizations.deny` 라우트로 DELETE 요청을 보내는 form을 포함해야 합니다. 이 라우트들은 `state`, `client_id`, `auth_token` 필드를 기대합니다.

<a name="managing-clients"></a>
### 클라이언트 관리

애플리케이션의 API와 통신해야 하는 외부 개발자는 클라이언트 애플리케이션을 사전에 등록해야 합니다. 일반적으로 애플리케이션의 이름과, 사용자가 인가를 승인한 후 리디렉션할 URI를 제공합니다.

<a name="managing-first-party-clients"></a>
#### 1차 클라이언트(First-Party Clients)

클라이언트를 가장 쉽게 생성하는 방법은 `passport:client` 아티즌 명령어를 사용하는 것입니다. 이 명령어는 1차 클라이언트 생성을 비롯해 OAuth2 기능 테스트에도 사용할 수 있습니다. 명령어 실행 시 클라이언트 관련 정보를 차례로 입력하면, 클라이언트 ID와 시크릿을 받을 수 있습니다.

```shell
php artisan passport:client
```

클라이언트에 여러 개의 리디렉션 URI를 허용하려면, `passport:client` 명령 실행 시 URI 입력 단계에서 콤마(,)로 구분된 리스트로 입력하면 됩니다. 콤마가 포함된 URI라면 URI 인코딩 처리를 해주어야 합니다.

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 3차 클라이언트(Third-Party Clients)

애플리케이션의 사용자가 직접 `passport:client` 명령을 사용할 수 없기 때문에, 특정 사용자에게 클라이언트를 등록하려면 `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드를 사용할 수 있습니다.

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// 지정한 사용자($user) 소유의 OAuth 앱 클라이언트 생성...
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

`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. `$client->id`는 클라이언트 ID, `$client->plainSecret`는 클라이언트 시크릿으로 사용자가 확인할 수 있습니다.

<a name="requesting-tokens"></a>
### 토큰 요청

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인가 화면으로 리다이렉트

클라이언트가 생성되면, 개발자는 그 클라이언트 ID와 시크릿을 사용해 인가 코드와 액세스 토큰을 요청할 수 있습니다. 먼저 소비자 애플리케이션은 `/oauth/authorize` 라우트로 사용자를 리다이렉트해야 합니다.

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

`prompt` 파라미터를 활용하면 Passport 애플리케이션의 인증 동작 방식을 제어할 수 있습니다.

- `none` 값을 사용하면, 사용자가 이미 인증되지 않은 상태라면 Passport는 항상 인증 오류를 반환합니다.
- `consent` 값을 사용하면, 이전에 모든 스코프를 승인한 애플리케이션일지라도 항상 인가 승인 화면을 보여줍니다.
- `login` 값을 사용하면, Passport 애플리케이션이 이미 세션이 있더라도 무조건 재로그인을 요구합니다.

`prompt` 값을 지정하지 않는다면, 사용자가 요청된 스코프에 대해 이전에 인가한 적이 없는 경우에만 인가 화면이 표시됩니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 Passport가 이미 정의하고 있으므로 직접 라우트를 따로 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 인가 요청 승인

인가 요청을 받을 때 Passport는 `prompt` 파라미터 값에 따라 자동으로 응답하며, 필요한 경우 사용자에게 인가 승인 또는 거부 화면을 보여줍니다. 사용자가 요청을 승인하면 지정된 `redirect_uri`로 리다이렉트됩니다. 이 때, `redirect_uri`는 클라이언트 생성 시 설정한 URL과 반드시 일치해야 합니다.

특정 상황(예: 1차 클라이언트)에서는 인가 승인 화면을 생략하고 싶을 수도 있습니다. 이 경우 [Client 모델을 오버라이드](#overriding-default-models)하고 `skipsAuthorization` 메서드를 정의하면 됩니다. 이 메서드가 `true`를 반환하면 인가 승인 화면 없이 즉시 `redirect_uri`로 사용자 리다이렉트가 이루어지며, 단 소비자 애플리케이션에서 `prompt` 파라미터를 명시적으로 지정하면 화면이 표시됩니다.

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 해당 클라이언트의 인가 요청을 바로 승인할지 여부를 결정합니다.
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

사용자가 인가 요청을 승인하면, 소비자 애플리케이션으로 리다이렉트됩니다. 이 시점에서 먼저 `state` 파라미터가 리디렉트 전 저장한 값과 일치하는지 검증해야 하며, 값이 일치하면 다음과 같이 액세스 토큰을 요청하는 `POST` 요청을 보낼 수 있습니다. 요청에는 사용자가 인가 승인 시 받은 인가 코드가 포함되어야 합니다.

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

`/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성이 담긴 JSON 응답을 반환합니다. `expires_in` 값은 액세스 토큰이 만료되기까지 남은 초(second) 수를 의미합니다.

> [!NOTE]
> `/oauth/authorize` 라우트와 마찬가지로 `/oauth/token` 라우트도 Passport가 미리 정의합니다. 이 라우트 역시 직접 정의하지 않아도 됩니다.

<a name="managing-tokens"></a>
### 토큰 관리

`Laravel\Passport\HasApiTokens` 트레이트의 `tokens` 메서드를 사용하면 사용자가 인가한 토큰 목록을 조회할 수 있습니다. 예를 들어, 사용자에게 외부 애플리케이션과의 연결 내역을 보여주는 대시보드를 만들 때 활용할 수 있습니다.

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 해당 사용자의 유효한 토큰 전체 조회...
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
### 토큰 갱신

애플리케이션이 단기(Short-lived) 액세스 토큰을 발급하는 경우, 사용자는 토큰 만료 후 refresh token(갱신 토큰)을 통해 새 액세스 토큰을 받아야 합니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // confidential 클라이언트일 때만 필수...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 `/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성을 담은 JSON 응답을 반환합니다. `expires_in`은 액세스 토큰의 남은 만료 시간을 초로 나타냅니다.

<a name="revoking-tokens"></a>
### 토큰 폐기

액세스 토큰은 `Laravel\Passport\Token` 모델의 `revoke` 메서드를 사용해 폐기할 수 있습니다. refresh token은 `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드를 사용합니다.

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// 액세스 토큰 폐기...
$token->revoke();

// 해당 토큰의 refresh token 폐기...
$token->refreshToken?->revoke();

// 해당 사용자의 모든 토큰 폐기...
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### 토큰 정리

토큰이 폐기되었거나 만료된 경우, 데이터베이스에서 완전히 삭제하고 싶을 때가 있습니다. Passport에서 제공하는 `passport:purge` 아티즌 명령어를 사용하면 손쉽게 삭제할 수 있습니다.

```shell
# 폐기 또는 만료된 토큰, 인증 코드, 디바이스 코드 정리...
php artisan passport:purge

# 6시간 이상 만료된 토큰만 정리...
php artisan passport:purge --hours=6

# 폐기된 토큰, 인증 코드, 디바이스 코드만 정리...
php artisan passport:purge --revoked

# 만료된 토큰, 인증 코드, 디바이스 코드만 정리...
php artisan passport:purge --expired
```

또한, 애플리케이션의 `routes/console.php` 파일에 [스케줄 작업](/docs/12.x/scheduling)을 등록하여 정기적으로 토큰을 자동 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## PKCE가 적용된 Authorization Code Grant

Authorization Code Grant에서 "Proof Key for Code Exchange(PKCE, 코드 교환을 위한 인증 키)"는 싱글 페이지 애플리케이션(SPA)이나 모바일 애플리케이션에서 API를 안전하게 인증받을 수 있는 방식입니다. 이 방식을 사용하면 클라이언트 시크릿을 안전하게 저장할 수 없는 환경이나, 인가 코드가 탈취당할 위험을 완화해야 하는 경우에 적합합니다. 인가 코드를 액세스 토큰으로 교환할 때 클라이언트 시크릿 대신 "code verifier"와 "code challenge" 조합을 사용하게 됩니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성

PKCE 방식의 Authorization Code Grant로 토큰을 발급받으려면, 먼저 PKCE 지원 클라이언트를 생성해야 합니다. `passport:client` 아티즌 명령어에 `--public` 옵션을 사용하면 됩니다.

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청

<a name="code-verifier-code-challenge"></a>
#### 코드 검증자 및 코드 챌린지(Code Verifier & Code Challenge)

이 인증 방식은 클라이언트 시크릿을 제공하지 않으므로, 개발자는 토큰 요청 시 code verifier와 code challenge 조합을 직접 생성해야 합니다.

code verifier는 43자 이상 128자 이하의 알파벳, 숫자, 그리고 `"-"`, `"."`, `"_"`, `"~"` 문자로 이루어진 랜덤 문자열이어야 하며, [RFC 7636 명세](https://tools.ietf.org/html/rfc7636)를 따라야 합니다.

code challenge는 URL 및 파일명에 안전한 문자로 Base64 인코딩된 문자열이어야 합니다. 마지막에 붙을 수 있는 `'='` 문자는 제거하고, 줄바꿈이나 공백 등 불필요한 문자가 포함되어선 안 됩니다.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>

#### 인가를 위한 리디렉션

클라이언트가 생성되면, 클라이언트 ID와 생성된 코드 검증자(code verifier), 코드 챌린지(code challenge)를 사용해 애플리케이션에서 인가 코드와 액세스 토큰을 요청할 수 있습니다. 우선, 클라이언트를 사용하는 애플리케이션(소비자)은 여러분의 애플리케이션의 `/oauth/authorize` 경로로 리디렉션을 요청해야 합니다:

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

사용자가 인가 요청을 승인하면, 사용자는 소비자 애플리케이션으로 리디렉션됩니다. 이때, 소비자 측에서는 리디렉션 전에 저장해 두었던 `state` 파라미터와 응답 시의 값을 비교해 검증해야 합니다(표준 인가 코드 그랜트와 동일).

`state` 파라미터가 일치한다면, 소비자 측은 액세스 토큰을 요청하기 위해 여러분의 애플리케이션에 `POST` 요청을 보내야 합니다. 이 요청에는 사용자가 인가 요청을 승인할 때 발급된 인가 코드와, 최초에 생성한 코드 검증자(code verifier)를 함께 포함해야 합니다:

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

OAuth2 디바이스 인가 그랜트는 TV, 게임 콘솔 등과 같이 브라우저가 없거나 입력이 제한된 장치에서 "디바이스 코드(device code)"를 교환하여 액세스 토큰을 받을 수 있도록 허용합니다. 디바이스 플로우에서는 디바이스 클라이언트가 사용자가 컴퓨터나 스마트폰 등 보조 기기를 통해 제공받은 "유저 코드(user code)"를 입력하고, 접근 요청을 승인하거나 거부하도록 안내합니다.

먼저, Passport에게 "유저 코드"와 "인가" 뷰를 어떻게 반환할지 알려주어야 합니다.

모든 인가 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스에서 제공하는 메서드를 이용해 커스터마이징할 수 있습니다. 보통 이 작업은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내의 `boot` 메서드에서 수행합니다.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름 전달 방식...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // 클로저 전달 방식...
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

Passport는 자동으로 위 뷰들을 반환하는 라우트를 정의합니다. `auth.oauth.device.user-code` 템플릿에는 `passport.device.authorizations.authorize` 라우트로 GET 요청을 보내는 폼을 포함해야 하며, 이때 `user_code` 쿼리 파라미터가 필요합니다.

`auth.oauth.device.authorize` 템플릿에는 인가를 승인하는 `passport.device.authorizations.approve` 라우트로의 POST 폼, 그리고 인가를 거부하는 `passport.device.authorizations.deny` 라우트로의 DELETE 폼이 포함되어야 합니다. 두 라우트 모두 `state`, `client_id`, `auth_token` 필드를 필요로 합니다.

<a name="creating-a-device-authorization-grant-client"></a>
### 디바이스 인가 클라이언트 생성

애플리케이션에서 디바이스 인가 그랜트를 통해 토큰을 발급하려면 디바이스 플로우가 활성화된 클라이언트를 먼저 생성해야 합니다. `passport:client` Artisan 명령어에 `--device` 옵션을 주어 생성할 수 있습니다. 이 명령은 퍼스트 파티 디바이스 플로우 클라이언트를 생성하며, 클라이언트 ID와 시크릿을 제공합니다:

```shell
php artisan passport:client --device
```

또한, `ClientRepository` 클래스의 `createDeviceAuthorizationGrantClient` 메서드를 사용해 특정 사용자에게 속한 서드 파티 클라이언트를 등록할 수도 있습니다:

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

클라이언트가 생성된 후, 개발자는 클라이언트 ID를 사용하여 애플리케이션에서 디바이스 코드를 요청할 수 있습니다. 우선, 소비자 디바이스는 `/oauth/device/code` 경로에 `POST` 요청을 보내 디바이스 코드를 받아야 합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 요청은 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 속성을 포함한 JSON 응답을 반환합니다. `expires_in`은 디바이스 코드가 만료될 때까지의 초 단위 시간이며, `interval`은 디바이스가 `/oauth/token` 경로를 폴링할 때(주기적으로 반복 요청 시) 요청 간에 기다려야 할 최소 시간(초)을 나타냅니다. 이 값을 지키지 않으면 속도 제한(rate limit)에 걸릴 수 있습니다.

> [!NOTE]
> `/oauth/device/code` 경로는 Passport에서 이미 정의되어 있으므로 별도로 라우팅할 필요가 없습니다.

<a name="user-code"></a>
#### 인증 URI와 유저 코드 표시하기

디바이스 코드 요청을 받은 후, 소비자 디바이스는 사용자에게 다른 기기를 사용해 `verification_uri`로 접속하여 `user_code`를 입력하고 인가 요청을 승인하라고 안내해야 합니다.

<a name="polling-token-request"></a>
#### 토큰 폴링 요청

사용자가 별도의 기기를 사용해 접근 권한을 승인(또는 거부)하므로, 소비자 디바이스는 사용자가 요청에 응답할 때까지 여러분의 애플리케이션 `/oauth/token` 경로를 반복적으로 요청(폴링)해야 합니다. 이때 디바이스 코드 요청 시 JSON 응답으로 전달받은 최소 `interval` 값을 반드시 지켜야 하며, 이를 지키지 않으면 속도 제한 오류가 발생할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // confidential 클라이언트만 필요...
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

사용자가 인가 요청을 승인하면, `access_token`, `refresh_token`, `expires_in` 속성을 포함하는 JSON 응답이 반환됩니다. `expires_in`은 액세스 토큰의 만료 시간(초)입니다.

<a name="password-grant"></a>
## 패스워드 그랜트(Password Grant)

> [!WARNING]
> 패스워드 그랜트 토큰은 더 이상 사용을 권장하지 않습니다. 대신 [OAuth2 Server에서 현재 권장되는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 사용하세요.

OAuth2 패스워드 그랜트는 모바일 앱 등 기타 퍼스트 파티 클라이언트가 이메일/사용자명과 비밀번호를 사용해 액세스 토큰을 받을 수 있게 해줍니다. 즉, 사용자가 전체 OAuth2 인가 코드 리디렉션 과정을 거치지 않고도 퍼스트 파티 클라이언트에 안전하게 액세스 토큰을 발급할 수 있습니다.

패스워드 그랜트를 활성화하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enablePasswordGrant` 메서드를 호출하세요:

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

애플리케이션에서 패스워드 그랜트를 통해 토큰을 발급하려면 패스워드 그랜트 클라이언트를 먼저 생성해야 합니다. `passport:client` Artisan 명령어에 `--password` 옵션을 이용해 생성할 수 있습니다.

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청

그랜트를 활성화하고 패스워드 그랜트 클라이언트를 생성한 뒤에는, 사용자의 이메일(또는 사용자명)과 비밀번호로 `/oauth/token` 경로에 `POST` 요청하여 액세스 토큰을 받으면 됩니다. 이 라우트는 Passport에서 이미 등록되어 있으므로 별도로 정의하지 않아도 됩니다. 요청이 성공하면, 서버에서 반환되는 JSON 응답에서 `access_token`과 `refresh_token`을 받을 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // confidential 클라이언트만 필요...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

> [!NOTE]
> 액세스 토큰은 기본적으로 유효기간이 깁니다. 필요하다면 [액세스 토큰의 최대 수명을 설정](#configuration)할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청하기

패스워드 그랜트나 클라이언트 크레덴셜 그랜트를 사용할 때, 애플리케이션에서 지원되는 모든 스코프에 대해 토큰 인가를 원할 수도 있습니다. 이 경우 `*` 스코프를 요청하면 됩니다. `*` 스코프가 설정된 토큰에서 `can` 메서드는 항상 `true`를 반환합니다. 이 스코프는 반드시 `password` 또는 `client_credentials` 그랜트로 발급된 토큰에만 할당할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // confidential 클라이언트만 필요...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### 사용자 프로바이더 커스터마이즈

애플리케이션이 두 개 이상의 [인증 사용자 프로바이더](/docs/12.x/authentication#introduction)를 사용할 경우, `artisan passport:client --password` 명령으로 클라이언트를 생성할 때 `--provider` 옵션을 추가하여 패스워드 그랜트 클라이언트가 사용할 사용자 프로바이더를 지정할 수 있습니다. 지정한 프로바이더 이름은 애플리케이션의 `config/auth.php` 설정 파일에 정의된 유효한 프로바이더여야 합니다. 이후 [미들웨어로 라우트를 보호](#multiple-authentication-guards)해, 해당 가드의 프로바이더에 속한 사용자만 허용할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명 필드 커스터마이즈

패스워드 그랜트 인증 시 Passport는 인증 가능한 모델의 `email` 속성을 "사용자명"으로 사용합니다. 이 동작을 변경하려면, 모델에 `findForPassport` 메서드를 정의할 수 있습니다:

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
### 비밀번호 검증 커스터마이즈

패스워드 그랜트 인증 시 Passport는 모델의 `password` 속성을 이용해 비밀번호를 검증합니다. 만약 모델에 `password` 속성이 없거나, 비밀번호 검증 로직을 커스터마이즈하고 싶다면 모델에 `validateForPassportPasswordGrant` 메서드를 정의하면 됩니다:

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
     * Passport 패스워드 그랜트를 위한 비밀번호 유효성 검증.
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
> 임플리시트 그랜트 토큰은 더 이상 사용을 권장하지 않습니다. 대신 [OAuth2 Server에서 현재 권장되는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 사용하세요.

임플리시트 그랜트는 인가 코드 그랜트와 유사하지만, 인가 코드를 별도로 교환하지 않고 클라이언트로 직접 토큰을 반환합니다. 이 방식은 클라이언트 크리덴셜을 안전하게 저장할 수 없는 JavaScript 또는 모바일 애플리케이션에서 주로 사용됩니다. 이 그랜트를 활성화하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enableImplicitGrant` 메서드를 호출하세요:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

임플리시트 그랜트를 통해 토큰을 발급하려면, 임플리시트 클라이언트를 먼저 생성해야 합니다. `passport:client` Artisan 명령어에 `--implicit` 옵션을 사용하면 됩니다.

```shell
php artisan passport:client --implicit
```

그랜트를 활성화하고 임플리시트 클라이언트를 생성하면, 개발자는 클라이언트 ID를 사용하여 애플리케이션에 액세스 토큰을 요청할 수 있습니다. 소비자 애플리케이션은 여러분의 `/oauth/authorize` 경로로 리디렉션 요청을 보냅니다:

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
> `/oauth/authorize` 경로는 Passport에서 이미 정의되어 있으므로 별도로 라우팅할 필요가 없습니다.

<a name="client-credentials-grant"></a>
## 클라이언트 크리덴셜 그랜트(Client Credentials Grant)

클라이언트 크리덴셜 그랜트는 머신 간 인증(서버 간 통신 등)에 적합합니다. 예를 들어, 예약 작업이 API를 통해 유지보수 작업을 수행할 때 사용할 수 있습니다.

해당 그랜트를 통해 토큰을 발급하려면 클라이언트 크리덴셜 클라이언트를 먼저 생성해야 하며, `passport:client` Artisan 명령어의 `--client` 옵션을 사용합니다:

```shell
php artisan passport:client --client
```

그런 다음, 라우트에 `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 할당합니다:

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하고 클라이언트가 리소스 소유자인 경우...
})->middleware(EnsureClientIsResourceOwner::class);
```

특정 스코프에 대한 접근만 허용하려면, `using` 메서드에 필요한 스코프들을 나열해 전달할 수 있습니다:

```php
Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하고, 클라이언트가 리소스 소유자이며 "servers:read", "servers:create" 스코프가 모두 있는 경우...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create');
```

<a name="retrieving-tokens"></a>
### 토큰 조회

이 그랜트 타입으로 토큰을 받으려면, `oauth/token` 엔드포인트에 요청을 전송하세요:

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

때때로 사용자는 일반적인 인가 코드 리디렉션 과정을 거치지 않고도 직접 액세스 토큰을 만들고 싶어할 수 있습니다. 애플리케이션 UI에서 사용자 본인에게 토큰을 발급하도록 허용하면, API를 실험하거나 간단하게 액세스 토큰을 발급하는 데 유용합니다.

> [!NOTE]
> 애플리케이션에서 주로 개인 액세스 토큰 발급만 필요하다면, 라라벨의 경량 API 토큰 발급 라이브러리인 [Laravel Sanctum](/docs/12.x/sanctum) 사용을 고려해 보세요.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성

개인 액세스 토큰을 발급하려면, 먼저 개인 액세스 클라이언트를 생성해야 합니다. 이를 위해 `passport:client` Artisan 명령어에 `--personal` 옵션을 사용하세요. 이미 `passport:install` 명령을 실행했다면 이 명령은 필요하지 않습니다:

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### 사용자 프로바이더 커스터마이즈

애플리케이션에서 두 개 이상의 [인증 사용자 프로바이더](/docs/12.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --personal` 명령어로 클라이언트를 생성할 때 `--provider` 옵션을 제공하여 개인 액세스 그랜트 클라이언트가 이용할 사용자 프로바이더를 지정하세요. 지정한 이름은 `config/auth.php` 파일에 설정된 유효한 프로바이더여야 합니다. 그 후 [미들웨어를 통해 라우트를 보호](#multiple-authentication-guards)함으로써, 해당 가드의 프로바이더에 속한 사용자만 인가될 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리

개인 액세스 클라이언트를 만들었다면, `App\Models\User` 모델 인스턴스의 `createToken` 메서드를 사용해 해당 사용자에게 토큰을 발급할 수 있습니다. `createToken` 메서드의 첫 번째 인자는 토큰 이름이고, 두 번째 인자는 선택적으로 [스코프](#token-scopes) 배열입니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 스코프 없이 토큰 생성...
$token = $user->createToken('My Token')->accessToken;

// 스코프와 함께 토큰 생성...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// 모든 스코프를 가진 토큰 생성...
$token = $user->createToken('My Token', ['*'])->accessToken;

// 해당 사용자의 유효한 개인 액세스 토큰 모두 조회하기...
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
### 미들웨어로 보호

Passport는 요청에 담긴 액세스 토큰을 검증하는 [인증 가드](/docs/12.x/authentication#adding-custom-guards)를 함께 제공합니다. `api` 가드를 `passport` 드라이버로 설정하면, 보호할 라우트에 `auth:api` 미들웨어만 지정해도 액세스 토큰 검증이 적용됩니다:

```php
Route::get('/user', function () {
    // API 인증된 사용자만 이 라우트에 접근할 수 있습니다...
})->middleware('auth:api');
```

> [!WARNING]
> [클라이언트 크리덴셜 그랜트](#client-credentials-grant)를 사용할 경우, `auth:api` 미들웨어 대신 [Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner 미들웨어](#client-credentials-grant)로 라우트를 보호해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 복수 인증 가드 사용

애플리케이션에서 여러 종류의 사용자를 서로 다른 Eloquent 모델로 관리해야 할 수도 있습니다. 이 경우, 사용자 프로바이더별로 가드 구성을 각각 정의해 특정 사용자 프로바이더 전용 요청을 보호할 수 있습니다. 예를 들어, 아래는 `config/auth.php` 설정 파일에서의 예시입니다:

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

다음 예시처럼, `api-customers` 가드는 `customers` 사용자 프로바이더를 사용해 들어오는 요청을 인증합니다:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport에서 여러 사용자 프로바이더를 사용하는 추가 정보는 [개인 액세스 토큰 문서](#customizing-the-user-provider-for-pat) 및 [패스워드 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달 방식

Passport로 보호된 라우트를 호출할 때, API 소비자는 요청의 `Authorization` 헤더에 `Bearer` 토큰으로 액세스 토큰을 명시해야 합니다. 예를 들어, `Http` 파사드를 사용할 경우 아래와 같이 합니다:

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

스코프는 여러분의 API 클라이언트가 계정에 권한을 요청할 때 어떤 권한만 허용할지 지정할 수 있도록 해줍니다. 예를 들어, 전자상거래 앱을 개발할 때 모든 API 소비자에게 주문 생성 권한이 필요하지 않고, 운송 상태만 제공하고 싶을 수 있습니다. 즉, 스코프는 서드 파티 애플리케이션이 사용자를 대신해 수행할 수 있는 동작을 여러분의 애플리케이션 사용자가 제한하게 해줍니다.

<a name="defining-scopes"></a>
### 스코프 정의

여러분의 API 스코프는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 `Passport::tokensCan` 메서드를 이용해 정의할 수 있습니다. `tokensCan` 메서드는 스코프 이름과 설명으로 구성된 배열을 인자로 받습니다. 이 스코프 설명은 자유롭게 작성 가능하며, 인가 승인 화면에 사용자에게 표시됩니다:

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

클라이언트가 별도의 스코프를 요청하지 않은 경우, `defaultScopes` 메서드를 사용하여 Passport 서버에서 토큰에 기본 스코프를 자동으로 부여하도록 설정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

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

인가 코드 그랜트 방식으로 액세스 토큰을 요청할 때, 소비자는 원하는 스코프 목록을 `scope` 쿼리 스트링 파라미터로 지정해야 합니다. `scope` 파라미터 값은 각 스코프를 공백 문자로 구분해 입력합니다.

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

`App\Models\User` 모델의 `createToken` 메서드를 사용해 개인 액세스 토큰을 발급할 때, 원하는 스코프들의 배열을 두 번째 인수로 전달할 수 있습니다.

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 확인하기

Passport는 요청이 해당 스코프가 부여된 토큰으로 인증되었는지 확인할 수 있는 미들웨어 두 가지를 제공합니다.

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인 (Check For All Scopes)

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어를 라우트에 할당하면, 요청의 액세스 토큰이 나열된 모든 스코프를 갖고 있는지 검증할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // 액세스 토큰에 "orders:read" 및 "orders:create" 스코프가 모두 있음...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create');
```

<a name="check-for-any-scopes"></a>
#### 하나 이상의 스코프 확인 (Check for Any Scopes)

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어를 라우트에 할당하면, 요청의 액세스 토큰이 나열된 스코프 중 하나라도 갖고 있는지 검증할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // 액세스 토큰에 "orders:read" 또는 "orders:create" 스코프 중 하나가 있음...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create');
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인하기

액세스 토큰으로 인증된 요청이 애플리케이션에 도달한 뒤에도, 인증된 `App\Models\User` 인스턴스에서 `tokenCan` 메서드를 사용해 토큰에 특정 스코프가 부여되어 있는지 추가로 확인할 수 있습니다.

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

`scopesFor` 메서드는 전달한 ID/이름에 해당하는 `Laravel\Passport\Scope` 인스턴스의 배열을 반환합니다.

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

특정 스코프가 정의되어 있는지 확인하려면 `hasScope` 메서드를 사용하면 됩니다.

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA 인증

API를 구축할 때, JavaScript 애플리케이션에서 자신이 만든 API를 직접 소비(호출)할 수 있으면 매우 유용합니다. 이러한 방식의 API 개발은, 해당 API를 외부에 공개할 뿐만 아니라 자신이 만든 웹 애플리케이션, 모바일 앱, 서드파티 앱, 또는 직접 배포한 SDK 등에서도 동일하게 활용할 수 있게 해줍니다.

일반적으로 JavaScript 애플리케이션에서 API를 사용하려면 액세스 토큰을 애플리케이션(브라우저 등)으로 직접 전달하고, 이후 모든 요청에 해당 토큰을 첨부해야 합니다. 하지만 Passport는 이 과정을 대신 처리해주는 미들웨어를 제공합니다. 여러분이 해야 할 일은 애플리케이션의 `bootstrap/app.php` 파일에서 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어를 추가하는 것뿐입니다.

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어가 미들웨어 스택의 **마지막**에 등록되어 있는지 반드시 확인하십시오.

이 미들웨어는 응답에 `laravel_token`이라는 쿠키를 추가합니다. 이 쿠키에는 Passport가 API 요청 인증에 사용할 암호화된 JWT가 저장됩니다. JWT의 생명주기는 `session.lifetime` 설정값과 동일합니다. 브라우저는 이 쿠키를 이후 모든 요청에 자동으로 포함하므로, 액세스 토큰을 직접 헤더로 전달하지 않아도 애플리케이션의 API를 호출할 수 있습니다.

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이징

필요에 따라 `Passport::cookie` 메서드를 사용하여 `laravel_token` 쿠키의 이름을 변경할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

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

이 인증 방식을 사용할 때, 요청 헤더에 올바른 CSRF 토큰이 포함되어야 합니다. 라라벨 스켈레톤 애플리케이션에 기본 포함되어 있는 JavaScript 스캐폴딩 및 모든 스타터 킷은 [Axios](https://github.com/axios/axios) 인스턴스를 포함하며, 이 인스턴스가 자동으로 암호화된 `XSRF-TOKEN` 쿠키 값을 읽어 same-origin 요청에 `X-XSRF-TOKEN` 헤더로 전송합니다.

> [!NOTE]
> `X-XSRF-TOKEN` 대신 `X-CSRF-TOKEN` 헤더를 직접 보내고 싶다면, 반드시 `csrf_token()`이 반환하는 **암호화되지 않은** 토큰을 사용해야 합니다.

<a name="events"></a>
## 이벤트

Passport는 액세스 토큰 및 리프레시 토큰이 발급 또는 폐기될 때 이벤트를 발생시킵니다. 해당 이벤트를 [리스닝](/docs/12.x/events)하여 데이터베이스의 다른 액세스 토큰을 정리하거나 폐기할 수 있습니다.

<div class="overflow-auto">

| 이벤트 이름                                      |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## 테스트

`actingAs` 메서드를 사용하면, 테스트에서 어떤 사용자가 인증되어 있다고 지정할 수 있으며, 이때 부여할 스코프도 함께 지정할 수 있습니다. `actingAs` 메서드의 첫 번째 인수는 사용자 인스턴스, 두 번째 인수는 해당 사용자의 토큰에 부여할 스코프의 배열입니다.

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

`actingAsClient` 메서드는 테스트에서 인증된 클라이언트와 해당 토큰에 부여할 스코프들을 지정할 때 사용할 수 있습니다. 첫 번째 인수는 클라이언트 인스턴스, 두 번째 인수는 해당 클라이언트 토큰에 부여할 스코프들의 배열입니다.

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