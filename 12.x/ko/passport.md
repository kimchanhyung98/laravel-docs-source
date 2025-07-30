# 라라벨 패스포트 (Laravel Passport)

- [소개](#introduction)
    - [Passport와 Sanctum 중 무엇을 선택해야 할까요?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [Passport 업그레이드](#upgrading-passport)
- [설정](#configuration)
    - [토큰 만료 시간](#token-lifetimes)
    - [기본 모델 오버라이드](#overriding-default-models)
    - [기본 라우트 오버라이드](#overriding-routes)
- [Authorization Code Grant](#authorization-code-grant)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청하기](#requesting-tokens)
    - [토큰 관리하기](#managing-tokens)
    - [토큰 리프레시](#refreshing-tokens)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [PKCE가 적용된 Authorization Code Grant](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청하기](#requesting-auth-pkce-grant-tokens)
- [디바이스 인증 플로우](#device-authorization-grant)
    - [디바이스 인증 클라이언트 생성](#creating-a-device-authorization-grant-client)
    - [토큰 요청하기](#requesting-device-authorization-grant-tokens)
- [패스워드 그랜트(Password Grant)](#password-grant)
    - [패스워드 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청하기](#requesting-password-grant-tokens)
    - [모든 Scope 요청하기](#requesting-all-scopes)
    - [User Provider 커스터마이징](#customizing-the-user-provider)
    - [Username 필드 커스터마이징](#customizing-the-username-field)
    - [Password 유효성 검증 커스터마이징](#customizing-the-password-validation)
- [임플리싯 그랜트(Implicit Grant)](#implicit-grant)
- [클라이언트 자격(인증) 그랜트](#client-credentials-grant)
- [Personal Access 토큰](#personal-access-tokens)
    - [Personal Access 클라이언트 생성](#creating-a-personal-access-client)
    - [User Provider 커스터마이징](#customizing-the-user-provider-for-pat)
    - [Personal Access 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어 사용](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
- [토큰 스코프(Scopes)](#token-scopes)
    - [스코프 정의](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당](#assigning-scopes-to-tokens)
    - [스코프 체크하기](#checking-scopes)
- [SPA 인증](#spa-authentication)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Passport](https://github.com/laravel/passport)는 라라벨 애플리케이션에 단 몇 분 만에 적용할 수 있는 완전한 OAuth2 서버 구현체를 제공합니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server) 위에 구축되어 있습니다.

> [!NOTE]
> 이 문서는 OAuth2에 어느 정도 익숙하다고 가정합니다. 만약 OAuth2에 대해 잘 모른다면, 계속 진행하기 전에 [용어 정리](https://oauth2.thephpleague.com/terminology/)와 OAuth2의 핵심 기능에 대해 미리 알아보시기 바랍니다.

<a name="passport-or-sanctum"></a>
### Passport와 Sanctum 중 무엇을 선택해야 할까요?

시작하기 전에, 여러분의 애플리케이션에 Laravel Passport가 더 적합한지 아니면 [Laravel Sanctum](/docs/12.x/sanctum)이 더 적합한지 결정할 필요가 있습니다. 만약 여러분의 애플리케이션이 반드시 OAuth2 지원이 필요하다면 Laravel Passport를 사용해야 합니다.

반대로 단일 페이지 애플리케이션(SPA), 모바일 애플리케이션을 인증하거나 API 토큰만 발급하려는 경우에는 [Laravel Sanctum](/docs/12.x/sanctum)에 적합합니다. Laravel Sanctum은 OAuth2를 지원하지는 않지만, API 인증 개발 경험이 훨씬 단순합니다.

<a name="installation"></a>
## 설치

Laravel Passport는 `install:api` 아티즌 명령어를 통해 설치할 수 있습니다.

```shell
php artisan install:api --passport
```

이 명령은 OAuth2 클라이언트와 액세스 토큰을 저장하기 위한 애플리케이션의 테이블 생성을 위해 필요한 데이터베이스 마이그레이션을 배포(실행)합니다. 또한 보안 액세스 토큰을 생성하는 데 필요한 암호화 키도 생성합니다.

`install:api` 명령어를 실행한 후에는, 여러분의 `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가해야 합니다. 이 트레이트는 인증된 사용자의 토큰과 스코프 등 유틸리티 메서드를 제공해줍니다.

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

마지막으로, 애플리케이션의 `config/auth.php` 파일에서 `api` 인증 가드를 정의하고 `driver` 옵션을 `passport`로 지정합니다. 그러면 라라벨은 API 요청 인증 시 Passport의 `TokenGuard`를 사용하게 됩니다.

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

서버에 Passport를 처음 배포하는 경우에는 `passport:keys` 명령어를 실행해야 할 수 있습니다. 이 명령어는 Passport가 액세스 토큰을 생성하는 데 필요한 암호화 키를 생성합니다. 생성된 키는 보통 소스 컨트롤에는 포함시키지 않습니다.

```shell
php artisan passport:keys
```

필요하다면, Passport의 키가 로드될 경로를 직접 지정할 수도 있습니다. 이를 위해 `Passport::loadKeysFrom` 메서드를 사용하고, 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

또는, `vendor:publish` 아티즌 명령어를 사용해 Passport의 설정 파일을 배포할 수도 있습니다.

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일을 배포한 뒤에는 아래와 같이 암호화 키를 환경 변수로 직접 정의하여 로드할 수 있습니다.

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="upgrading-passport"></a>
### Passport 업그레이드

Passport를 새로운 메이저 버전으로 업그레이드할 때에는 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼭 종합적으로 확인해야 합니다.

<a name="configuration"></a>
## 설정

<a name="token-lifetimes"></a>
### 토큰 만료 시간

Passport는 기본적으로 1년 후에 만료되는 장기 액세스 토큰을 발행합니다. 더 긴/짧은 토큰 만료 주기를 원한다면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출해야 합니다.

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
> Passport의 데이터베이스 테이블에 있는 `expires_at` 컬럼은 읽기 전용이며 단순 표시 목적으로만 존재합니다. 실제로 토큰을 발행할 때는 만료 정보가 서명되고 암호화된 토큰 안에 저장됩니다. 만약 토큰을 무효화해야 한다면 [반드시 폐기(revoke)](#revoking-tokens)해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Passport가 내부적으로 사용하는 모델을 확장하려면 자신만의 모델을 만들고 해당 Passport 모델을 상속하면 됩니다.

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의한 뒤에는 `Laravel\Passport\Passport` 클래스를 통해 Passport가 여러분의 커스텀 모델을 사용하도록 지정할 수 있습니다. 일반적으로 이 작업도 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 처리합니다.

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

가끔은 Passport가 제공하는 기본 라우트를 직접 커스터마이즈해서 사용하고 싶을 수 있습니다. 이를 위해서는 우선 `AppServiceProvider`의 `register` 메서드에서 `Passport::ignoreRoutes`를 추가하여 Passport의 기본 라우트 등록을 무시해야 합니다.

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

그 다음, [Passport의 routes 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 복사해서 애플리케이션의 `routes/web.php` 파일에 붙여넣고 마음대로 수정하시면 됩니다.

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

OAuth2 인증을 위한 표준적인 방식 중 하나가 Authorization Code(인가 코드) 방식을 사용하는 것입니다. 이 방식에서 클라이언트 애플리케이션은 사용자를 여러분의 서버로 리디렉션시키고, 사용자는 클라이언트에게 액세스 토큰 발급을 허용하거나 거부할 수 있습니다.

우선, Passport에게 어떤 뷰(view)를 반환할지 알려주어야 합니다.

Authorization 뷰의 랜더링 동작은 `Laravel\Passport\Passport`에서 제공하는 메서드를 통해 자유롭게 커스터마이즈할 수 있습니다. 이 메서드도 보통 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 지정하는 방법...
    Passport::authorizationView('auth.oauth.authorize');

    // 클로저(익명 함수)로 정의하는 방법...
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

Passport는 자동으로 `/oauth/authorize` 라우트를 정의하여 위에서 지정한 뷰를 반환합니다. 여러분의 `auth.oauth.authorize` 뷰 템플릿에는 `passport.authorizations.approve` 라우트로 POST 요청을 보내 인가(승인)를 처리하고, `passport.authorizations.deny` 라우트로 DELETE 요청을 보내 거절을 처리하는 폼이 포함되어야 합니다. 이 두 라우트는 모두 `state`, `client_id`, `auth_token` 필드를 필요로 합니다.

<a name="managing-clients"></a>
### 클라이언트 관리

여러분의 애플리케이션과 API로 상호작용하려는 개발자는 애플리케이션 등록(클라이언트 생성)이 필요합니다. 주로 애플리케이션 이름과, 인가 후 리디렉션할 URI 정보를 제공합니다.

<a name="managing-first-party-clients"></a>
#### 1st-Party(자체) 클라이언트

가장 간단하게 클라이언트를 만드는 방법은 `passport:client` 아티즌 명령을 사용하는 것입니다. 이 명령은 자체 사용 클라이언트 생성 또는 OAuth2 기능 테스트에 유용합니다. 명령어 실행 시 클라이언트에 대한 추가 정보를 입력해야 하며, 입력이 끝나면 클라이언트 ID와 시크릿(비밀키)이 발급됩니다.

```shell
php artisan passport:client
```

클라이언트에 여러 개의 리디렉션 URI를 허용하고 싶다면, 명령어 실행 중 URI 입력 시 쉼표(,)로 구분해서 입력 가능합니다. 만약 URI에 쉼표가 포함된 경우, 미리 URI 인코딩을 해야 합니다.

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 3rd-Party(외부) 클라이언트

여러분의 서비스 사용자가 직접 `passport:client` 명령어를 사용할 수 없기 때문에, `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드를 통해 특정 사용자의 클라이언트를 서버에서 직접 생성할 수 있습니다.

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// 지정한 사용자에게 OAuth 앱 클라이언트 생성...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// 사용자가 보유한 모든 OAuth 앱 클라이언트 목록 가져오기...
$clients = $user->oauthApps()->get();
```

`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. 여러분은 `$client->id`를 클라이언트 ID로, `$client->plainSecret`을 클라이언트 시크릿으로 사용자가 직접 확인할 수 있도록 보여줄 수 있습니다.

<a name="requesting-tokens"></a>
### 토큰 요청하기

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인가(Authorization) 요청을 위한 리디렉션

클라이언트가 생성되면, 해당 개발자는 클라이언트 ID와 시크릿을 이용해 여러분의 애플리케이션에서 인가 코드와 액세스 토큰을 요청할 수 있습니다. 우선, API를 사용하는 쪽 앱에서 여러분의 애플리케이션의 `/oauth/authorize` 라우트로 리디렉션 요청을 보냅니다.

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

`prompt` 파라미터는 Passport 애플리케이션의 인증 동작 방식을 지정할 수 있습니다.

- `prompt` 값이 `none`이면, 이미 Passport 애플리케이션에 인증되어 있지 않은 사용자는 무조건 인증 오류가 발생합니다.
- `consent`이면, 클라이언트 앱이 요청한 모든 scope를 이미 허용했다 해도 무조건 인가 화면이 다시 노출됩니다.
- `login`이면, 기존 세션이 있더라도 반드시 사용자가 다시 로그인해야 합니다.

만약 `prompt` 파라미터가 없으면, 사용자는 요청한 scope에 대해 기존에 허용한 적이 없는 경우에만 인가 화면을 보게 됩니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 Passport에서 미리 정의되어 있으므로 별도로 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 인가 요청 승인하기

인가 요청을 수신하면, Passport는 `prompt` 파라미터 값에 따라 자동으로 반응하고, 사용자가 인가를 허용할지 거부할지 선택할 수 있는 화면을 보여줍니다. 승인이 되면, 사용자는 API 클라이언트 쪽에서 지정한 `redirect_uri`로 리디렉션됩니다. `redirect_uri`는 클라이언트 생성 시 등록했던 URI와 정확히 일치해야 합니다.

첫 번째 파티(1st-party) 클라이언트와 같이 인가 화면을 건너뛰고 싶은 경우도 있을 수 있습니다. 이럴 때는 [Client 모델을 확장](#overriding-default-models)하고 `skipsAuthorization` 메서드를 정의하여 `true`를 반환하게 만들면 됩니다. 단, 클라이언트에서 명시적으로 `prompt` 파라미터를 지정했을 경우에는 무시되지 않습니다.

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 클라이언트가 인가 화면을 건너뛸지 여부를 반환합니다.
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
#### 인가 코드를 액세스 토큰으로 변환하기

사용자가 인가 요청을 승인하면, 사용자는 클라이언트 앱으로 리디렉션됩니다. 리디렉션 시 함께 전달된 `state` 파라미터 값을 서버에서 등록해뒀던 값과 일치하는지 검증해야 합니다. 일치하면, 클라이언트는 여러분의 애플리케이션에 POST 요청을 보내 액세스 토큰을 요청해야 하며, 이때 인가 코드(authorization code)를 함께 전달합니다.

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

이때 `/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in`은 액세스 토큰이 얼마 뒤에 만료될지를 초 단위로 알려줍니다.

> [!NOTE]
> `/oauth/authorize`와 마찬가지로 `/oauth/token` 라우트도 Passport에서 알아서 정의해주므로 따로 라우트 등록이 필요하지 않습니다.

<a name="managing-tokens"></a>
### 토큰 관리하기

`Laravel\Passport\HasApiTokens` 트레이트의 `tokens` 메서드를 사용하면 사용자의 승인된 토큰 목록을 조회할 수 있습니다. 예를 들어, 여러분의 서비스 사용자가 서드파티 앱과의 연결 내역을 직접 확인할 수 있는 대시보드 UI를 만들 때 활용할 수 있습니다.

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 사용자의 유효한 토큰 전체 가져오기...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// 서드파티 OAuth 앱 클라이언트와의 연결 정보 모두 가져오기...
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
### 토큰 리프레시

만약 애플리케이션에서 액세스 토큰의 유효 기간을 짧게 설정한 경우, 사용자는 토큰 만료 후에 새롭게 토큰을 갱신(refresh)해야 합니다. 이때 토큰 발급 시 함께 제공된 리프레시 토큰(refresh token)이 사용됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // confidential(비공개) 클라이언트라면 필수...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 `/oauth/token` 라우트 역시 `access_token`, `refresh_token`, `expires_in`이 포함된 JSON 응답을 반환합니다.

<a name="revoking-tokens"></a>
### 토큰 폐기(무효화)

`Laravel\Passport\Token` 모델의 `revoke` 메서드를 호출하면 해당 토큰을 폐기할 수 있습니다. 또, 토큰의 리프레시 토큰도 `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드로 무효화할 수 있습니다.

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// 액세스 토큰 폐기...
$token->revoke();

// 리프레시 토큰 폐기...
$token->refreshToken?->revoke();

// 해당 사용자의 모든 토큰 일괄 폐기...
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### 토큰 정리(삭제)

폐기되었거나 만료된 토큰을 데이터베이스에서 아예 정리하고 싶을 때는 Passport가 제공하는 `passport:purge` 아티즌 명령어를 사용할 수 있습니다.

```shell
# 폐기된 또는 만료된 토큰, 인증 코드, 디바이스 코드를 정리...
php artisan passport:purge

# 6시간 이상 지난 만료 토큰만 정리...
php artisan passport:purge --hours=6

# 폐기된 토큰, 인증 코드, 디바이스 코드만 정리...
php artisan passport:purge --revoked

# 만료된 토큰, 인증 코드, 디바이스 코드만 정리...
php artisan passport:purge --expired
```

이 외에도 [스케줄링 작업](/docs/12.x/scheduling)을 이용해 위 명령어를 자동 실행할 수 있습니다. 예를 들어, `routes/console.php`에서 아래처럼 설정할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## PKCE가 적용된 Authorization Code Grant

Proof Key for Code Exchange(PKCE) 방식의 Authorization Code Grant는 SPA(싱글 페이지 애플리케이션)나 모바일 앱에서 API 접근을 안전하게 인증할 수 있는 방법입니다. 클라이언트 시크릿을 안전하게 저장할 수 없거나, 인가 코드 탈취 공격 위험을 줄이려는 경우 PKCE 인증 방식을 선택해야 합니다. PKCE 방식을 사용할 땐 "코드 검증자(code verifier)"와 "코드 챌린지(code challenge)" 조합이 클라이언트 시크릿 대신 사용됩니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성

PKCE 방식의 Authorization Code Grant로 토큰을 발급하려면, PKCE가 활성화된 클라이언트를 먼저 만들어야 합니다. `passport:client` 아티즌 명령어에 `--public` 옵션을 추가하면 됩니다.

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청하기

<a name="code-verifier-code-challenge"></a>
#### 코드 검증자(Code Verifier)와 코드 챌린지(Code Challenge)

이 인증 방식은 클라이언트 시크릿이 없기 때문에, 개발자는 반드시 "코드 검증자"와 "코드 챌린지"를 조합해서 토큰을 요청해야 합니다.

- 코드 검증자는 43~128글자 사이의 알파벳, 숫자, `"-"`, `"."`, `"_"`, `"~"`로 조합된 랜덤 문자열이어야 하며, [RFC 7636 스펙](https://tools.ietf.org/html/rfc7636)을 따릅니다.
- 코드 챌린지는 URL 및 파일명 안전(Base64 인코딩) 문자열이어야 하고, 끝의 `'='` 문자는 모두 제거되어야 하며, 줄바꿈, 공백 등 불필요한 문자가 들어가면 안 됩니다.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 인가(Authorization) 요청을 위한 리디렉션

클라이언트를 생성한 뒤에는, 클라이언트 ID와 코드 검증자/챌린지를 조합해 인가 코드 및 액세스 토큰 요청을 시작할 수 있습니다. API 소비자는 우선 여러분의 `/oauth/authorize` 라우트로 리디렉션 요청을 보냅니다.

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

사용자가 인가를 승인하면, 클라이언트는 리디렉션 전에 저장해둔 `state` 값을 다시 확인해서 검증해야 합니다(표준 Authorization Code Grant와 완전히 동일). 

`state` 값이 일치하면, 승인된 인가 코드와 처음 생성했던 코드 검증자(code verifier)를 포함해 여러분의 애플리케이션에 POST 요청을 보내 액세스 토큰을 요청해야 합니다.

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
## 디바이스 인증 플로우(Device Authorization Grant)

OAuth2 디바이스 인증 플로우는 TV, 게임 콘솔 등 브라우저가 없거나 입력 기능이 제한적인 디바이스에서도 "디바이스 코드"를 활용해 액세스 토큰을 획득할 수 있도록 해줍니다. 이 방식에서는 디바이스 클라이언트가 사용자에게 보조 디바이스(컴퓨터, 스마트폰 등)를 통해 별도의 서버 화면에 접근해 "user code"를 입력하고 권한 승인을 할 수 있도록 안내합니다.

시작하려면, Passport에게 어떤 "user code", "authorization" 뷰를 반환할지 알려주어야 합니다.

Authorization 뷰의 랜더링 동작은 `Laravel\Passport\Passport`에서 제공하는 메서드로 자유롭게 커스터마이즈할 수 있습니다. 보통 이 작업은 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 처리됩니다.

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

    // 클로저(익명 함수)로 정의하는 방법...
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

Passport는 위 뷰를 반환하는 라우트를 자동으로 정의해줍니다. 여러분의 `auth.oauth.device.user-code` 템플릿에는 `passport.device.authorizations.authorize` 라우트로 GET 요청을 보내는 폼이 포함되어야 하며, 이 라우트는 `user_code` 쿼리 파라미터가 필요합니다.

`auth.oauth.device.authorize` 템플릿에는 `passport.device.authorizations.approve`로 POST 요청을 보내는 폼(승인)과, `passport.device.authorizations.deny`로 DELETE 요청을 보내는 폼(거절)이 필요합니다. 이때 `state`, `client_id`, `auth_token` 필드를 전달해야 합니다.

<a name="creating-a-device-authorization-grant-client"></a>
### 디바이스 인증 클라이언트 생성

디바이스 인증 그랜트로 토큰을 발급하려면 먼저 디바이스 플로우가 활성화된 클라이언트를 만들어야 합니다. `passport:client` 아티즌 명령어에 `--device` 옵션을 추가하면, 해당 클라이언트가 생성되며 클라이언트 ID/시크릿도 함께 발급됩니다.

```shell
php artisan passport:client --device
```

또는 `ClientRepository` 클래스의 `createDeviceAuthorizationGrantClient` 메서드를 사용해 특정 사용자의 3rd-party 클라이언트를 서버에서 직접 등록할 수 있습니다.

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

클라이언트가 생성되면, 개발자는 클라이언트 ID를 사용하여 애플리케이션에서 디바이스 코드를 요청할 수 있습니다. 먼저 디바이스(소비자)는 애플리케이션의 `/oauth/device/code` 경로에 `POST` 요청을 보내 디바이스 코드를 요청해야 합니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 요청은 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in`은 디바이스 코드가 만료되기까지의 초 단위 시간을, `interval`은 디바이스가 `/oauth/token` 경로에 폴링(polling) 요청을 보낼 때 최소 대기해야 할 초 단위 간격을 의미합니다. 이 간격을 지켜야 레이트 리밋(rate limit) 에러를 피할 수 있습니다.

> [!NOTE]
> `/oauth/device/code` 경로는 이미 Passport에 의해 정의되어 있습니다. 이 경로를 따로 직접 정의할 필요가 없습니다.

<a name="user-code"></a>
#### 인증 URI 및 사용자 코드 표시하기

디바이스 코드 요청 후, 디바이스는 사용자에게 다른 디바이스를 사용하여 제공된 `verification_uri`에 접속하고, 해당 `user_code`를 입력하도록 안내해야 합니다. 사용자가 이를 통해 인가 요청을 승인(또는 거부)할 수 있습니다.

<a name="polling-token-request"></a>
#### 폴링 토큰 요청

사용자가 별도의 기기에서 접근 권한을 허용(또는 거부)하는 동안, 디바이스는 애플리케이션의 `/oauth/token` 경로에 폴링(polling)하여 사용자의 응답 상태를 확인해야 합니다. 이때, 디바이스 코드 요청시 JSON 응답으로 받은 최소 `interval` 값을 폴링 간격으로 사용해야 레이트 리밋 에러를 방지할 수 있습니다.

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // confidential client의 경우에만 필요...
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

만약 사용자가 인가 요청을 승인했다면, 여기서 `access_token`, `refresh_token`, `expires_in` 속성을 가진 JSON 응답을 반환받게 됩니다. `expires_in`은 액세스 토큰이 만료될 때까지의 초 단위 시간을 의미합니다.

<a name="password-grant"></a>
## 패스워드 방식 권한 부여(Password Grant)

> [!WARNING]
> 패스워드 방식 토큰의 사용은 더 이상 권장하지 않습니다. [OAuth2 Server에서 현재 추천하는 권한 부여 방식](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 사용하실 것을 권장합니다.

OAuth2의 패스워드 방식 권한 부여는 모바일 애플리케이션과 같은 자체 1st-party 클라이언트가 이메일 또는 사용자명과 비밀번호를 사용해 액세스 토큰을 발급받을 수 있도록 해줍니다. 이 방식은 사용자가 전체 OAuth2 인증 코드 리다이렉트 플로우를 거치지 않아도, 안전하게 액세스 토큰을 발급할 수 있도록 도와줍니다.

패스워드 그랜트를 활성화하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enablePasswordGrant` 메서드를 호출합니다.

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
### 패스워드 방식 클라이언트 생성

패스워드 방식으로 토큰을 발급받기 전에, 해당 방식이 적용된 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령에 `--password` 옵션을 추가해 수행할 수 있습니다.

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청하기

권한 부여를 활성화하고 패스워드 방식 클라이언트까지 생성했다면, 사용자 이메일과 비밀번호를 포함하여 `/oauth/token` 경로에 `POST` 요청을 보내 액세스 토큰을 발급받을 수 있습니다. 이 라우트(`/oauth/token`)는 이미 Passport에 의해 등록되어 있으므로, 따로 정의할 필요가 없습니다. 성공적으로 요청이 처리되면, 서버로부터 `access_token`, `refresh_token` 값을 가진 JSON 응답이 반환됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // confidential client의 경우에만 필요...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

> [!NOTE]
> 액세스 토큰은 기본적으로 유효기간이 길게 설정되어 있습니다. 필요하다면 [최대 액세스 토큰 유효기간을 직접 설정](#configuration)할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청

패스워드 방식 또는 클라이언트 크리덴셜 방식으로 토큰을 요청할 때, 애플리케이션이 지원하는 모든 스코프에 권한을 부여하고 싶을 수 있습니다. 이 경우 `*` 스코프를 요청하면 됩니다. `*` 스코프가 할당된 토큰의 경우, 토큰 인스턴스의 `can` 메서드는 항상 `true`를 반환합니다. 이 스코프는 `password` 또는 `client_credentials` 방식으로 발급된 토큰에만 적용할 수 있습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // confidential client의 경우에만 필요...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### 사용자 제공자 지정

애플리케이션에서 [여러 인증 사용자 제공자](/docs/12.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --password` 명령 실행 시 `--provider` 옵션을 사용해 패스워드 그랜트 클라이언트가 사용할 사용자 제공자를 지정할 수 있습니다. 지정한 제공자 이름은 `config/auth.php` 설정 파일에 정의된 유효한 provider여야 합니다. 이후 [미들웨어를 이용해 라우트를 보호](#multiple-authentication-guards)하면, 지정한 provider의 사용자만 접근할 수 있도록 보장할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명(Username) 필드 커스터마이징

패스워드 방식 권한 부여 시, Passport는 기본적으로 인증 가능 모델의 `email` 속성을 "username"으로 사용합니다. 이 동작을 변경하고 싶다면 모델에 `findForPassport` 메서드를 정의할 수 있습니다.

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
     * 주어진 사용자명으로 사용자 인스턴스 찾기
     */
    public function findForPassport(string $username): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### 비밀번호 검증 로직 커스터마이징

패스워드 방식 인증 시, Passport는 기본적으로 모델의 `password` 속성을 사용해 전달받은 비밀번호를 검증합니다. 만약 모델에 `password` 속성이 없거나, 비밀번호 검증 로직을 커스터마이즈 하고 싶다면 모델에 `validateForPassportPasswordGrant` 메서드를 정의할 수 있습니다.

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
     * Passport 패스워드 그랜트용 비밀번호 검증
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant"></a>
## 임플리싯(Implicit) 방식 권한 부여

> [!WARNING]
> 임플리싯 방식 토큰 사용은 더 이상 권장되지 않습니다. [OAuth2 Server에서 현재 권장하는 권한 부여 방식](https://oauth2.thephpleague.com/authorization-server/which-grant/) 중 하나를 선택하는 것을 추천합니다.

임플리싯 방식 권한 부여는 인증 코드 방식과 비슷하지만, 토큰이 인가 코드 교환 없이 직접 클라이언트에 반환됩니다. 이 방식은 주로 클라이언트 크리덴셜을 안전하게 저장할 수 없는 자바스크립트 애플리케이션이나 모바일 앱에서 사용됩니다. 임플리싯 그랜트를 활성화하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enableImplicitGrant`를 호출하면 됩니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

임플리싯 방식으로 토큰을 발급받으려면, 우선 임플리싯 방식 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령에 `--implicit` 옵션을 사용하세요.

```shell
php artisan passport:client --implicit
```

권한 부여를 활성화하고 임플리싯 클라이언트를 만들었다면, 개발자는 자신의 클라이언트 ID를 이용해 애플리케이션으로부터 액세스 토큰을 요청할 수 있습니다. 소비자 애플리케이션은 아래와 같이 애플리케이션의 `/oauth/authorize` 경로로 리다이렉트 요청을 보내야 합니다.

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
> `/oauth/authorize` 라우트도 Passport에서 이미 정의되어 있으므로, 별도로 정의할 필요가 없습니다.

<a name="client-credentials-grant"></a>
## 클라이언트 크리덴셜 방식 권한 부여(Client Credentials Grant)

클라이언트 크리덴셜 방식은 기계와 기계(서버 간) 인증에 적합합니다. 예를 들어, API를 통해 유지보수 작업을 하는 스케줄링 잡에서 이 방식을 사용할 수 있습니다.

클라이언트 크리덴셜 방식으로 토큰을 발급하려면, 해당 방식의 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령의 `--client` 옵션을 사용하세요.

```shell
php artisan passport:client --client
```

다음으로, `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 특정 라우트에 할당해 클라이언트가 실제 자원 소유자인지 검증할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하며, 클라이언트가 자원 소유자임이 확인됨...
})->middleware(EnsureClientIsResourceOwner::class);
```

특정 스코프에 대한 접근만 허용하고 싶다면, `using` 메서드에 필요한 스코프 목록을 전달하세요.

```php
Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하고, 클라이언트가 자원 소유자이며, "servers:read"와 "servers:create" 두 스코프 모두를 가짐...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create'));
```

<a name="retrieving-tokens"></a>
### 토큰 조회

이 방식으로 토큰을 받으려면 `oauth/token` 엔드포인트에 요청하세요.

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

때로는 사용자가 전형적인 인가 코드 리다이렉트 흐름 없이도 직접 자신의 액세스 토큰을 발급받고 싶어할 수 있습니다. 애플리케이션 UI를 통해 사용자가 자신의 토큰을 직접 발급받게 하면, API 실험 또는 간편한 액세스 토큰 발급 방식으로도 활용할 수 있습니다.

> [!NOTE]
> 만약 주로 개인 액세스 토큰 발급 용도로 Passport를 사용한다면, API 액세스 토큰 발급을 위한 라라벨의 경량 1st-party 라이브러리인 [Laravel Sanctum](/docs/12.x/sanctum) 사용을 검토해보세요.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성

개인 액세스 토큰을 발급하려면, 먼저 개인 액세스 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령에서 `--personal` 옵션을 사용하면 됩니다. 만약 이미 `passport:install`을 실행했다면, 이 명령을 다시 실행할 필요가 없습니다.

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### 사용자 제공자 커스터마이징

애플리케이션에서 [여러 인증 사용자 제공자](/docs/12.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --personal` 명령 실행 시 `--provider` 옵션을 사용해 어떤 제공자를 사용할 것인지 지정할 수 있습니다. 입력한 제공자명은 `config/auth.php`에서 정의된 유효한 provider여야 하며, 이후 [미들웨어로 라우트 보호](#multiple-authentication-guards)를 통해 해당 provider의 사용자만 인가할 수 있게 제어할 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리

개인 액세스 클라이언트를 생성한 후, 특정 사용자에 대해 모델 인스턴스의 `createToken` 메서드를 사용해 토큰을 발급할 수 있습니다. `createToken` 메서드는 토큰의 이름(필수)과 [스코프](#token-scopes)의 배열(선택적)을 인자로 받습니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 스코프 없이 토큰 생성...
$token = $user->createToken('My Token')->accessToken;

// 스코프 지정해서 토큰 생성...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// 모든 스코프 할당...
$token = $user->createToken('My Token', ['*'])->accessToken;

// 사용자에게 해당하는 모든 유효한 개인 액세스 토큰 조회...
$tokens = $user->tokens()
    ->with('client')
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get()
    ->filter(fn (Token $token) => $token->client->hasGrantType('personal_access'));
```

<a name="protecting-routes"></a>
## 라우트 보호

<a name="via-middleware"></a>
### 미들웨어를 통한 보호

Passport에는 들어오는 요청의 액세스 토큰을 검증하는 [인증 가드](/docs/12.x/authentication#adding-custom-guards)가 포함되어 있습니다. `api` 가드에 `passport` 드라이버를 사용하도록 설정했다면, 액세스 토큰이 필요한 라우트에 `auth:api` 미들웨어만 추가하면 됩니다.

```php
Route::get('/user', function () {
    // API 인증된 사용자만 접근 가능...
})->middleware('auth:api');
```

> [!WARNING]
> [클라이언트 크리덴셜 방식 권한 부여](#client-credentials-grant)를 사용하는 경우, `auth:api` 미들웨어 대신 반드시 [`Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어](#client-credentials-grant)를 사용해 라우트를 보호해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 다중 인증 가드

여러 종류의 사용자를 인증하려고(각각 전혀 다른 Eloquent 모델을 쓰는 경우 등) 한다면, 각 사용자 제공자 타입별로 별도의 가드 설정이 필요할 수 있습니다. 이렇게 하면 특정 제공자 전용 요청만 보호할 수 있습니다. 예를 들어 `config/auth.php` 환경설정에 다음과 같이 가드를 등록할 수 있습니다.

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

다음과 같이 `customers` 사용자 제공자를 사용하는 `api-customers` 가드로 라우트 인증이 가능해집니다.

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport에서 여러 사용자 제공자를 사용하는 방법에 대한 더 자세한 정보는 [개인 액세스 토큰 문서](#customizing-the-user-provider-for-pat)와 [패스워드 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달 방법

Passport로 보호되는 라우트에 요청할 때는, 사용자의 액세스 토큰을 요청 헤더의 `Authorization`에 `Bearer` 토큰 형태로 전달해야 합니다. 예를 들어, `Http` 파사드를 사용할 때는 아래와 같이 작성합니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => "Bearer $accessToken",
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
## 토큰 스코프

스코프(Scope)는 API 클라이언트가 액세스 권한을 요청할 때 어느 범위(권한)까지 허용받을 것인지 정의하는 기능입니다. 예를 들어, 쇼핑몰 애플리케이션의 경우 모든 API 소비자가 주문 생성 권한이 필요하지 않을 수 있습니다. 이럴 때 스코프를 활용하면 사용자가 제3자 애플리케이션에 허용할 권한(주문 조회 등)만 선택적으로 허용할 수 있습니다. 즉, 스코프를 통해 사용자가 제3자 애플리케이션이 자신의 계정으로 수행할 수 있는 작업 범위를 제한할 수 있습니다.

<a name="defining-scopes"></a>
### 스코프 정의

애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `Passport::tokensCan` 메서드를 사용해 API의 스코프를 정의할 수 있습니다. 이 메서드는 스코프 이름(키)과 스코프 설명(값)으로 구성된 배열을 받으며, 사용자는 인가 승인 화면에서 이 설명을 볼 수 있습니다.

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
### 기본 스코프 설정

클라이언트가 별도의 스코프를 요청하지 않을 경우, `Passport::defaultScopes` 메서드를 사용해 토큰에 기본 스코프를 부여할 수 있습니다. 일반적으로 이 메서드는 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출하면 됩니다.

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

인가 코드 그랜트로 액세스 토큰을 요청할 때, 소비자는 원하는 권한(스코프)을 `scope` 쿼리 파라미터로 전달하면 됩니다. 이 파라미터는 여러 스코프를 공백 문자로 구분해 나열해야 합니다.

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

`App\Models\User` 모델의 `createToken` 메서드로 개인 액세스 토큰을 발급하는 경우, 원하는 스코프 배열을 두 번째 인자로 전달하면 됩니다.

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 확인

Passport는 토큰이 특정 스코프를 부여받았는지 검증하는 두 가지 미들웨어를 제공합니다.

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어를 라우트에 할당하면, 해당 요청의 액세스 토큰이 지정된 모든 스코프를 가지고 있는지 확인할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // 액세스 토큰에 "orders:read"와 "orders:create" 두 스코프가 모두 할당됨...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create')]);
```

<a name="check-for-any-scopes"></a>
#### 하나 이상의 스코프 확인

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어를 사용하면, 액세스 토큰에 열거된 스코프 중 *하나 이상*만 있으면 접근을 허용할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // 액세스 토큰에 "orders:read" 또는 "orders:create" 중 하나라도 있으면 접근 허용...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create')]);
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인

액세스 토큰 기반 인증 요청이 애플리케이션에 들어오면, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드를 이용해 해당 토큰이 특정 스코프를 가지고 있는지 프로그램적으로 확인할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('orders:create')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
#### 추가적인 스코프 관련 메서드

`scopeIds` 메서드는 정의된 모든 ID/이름 배열을 반환합니다.

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

`scopes` 메서드는 정의된 모든 스코프를 `Laravel\Passport\Scope` 인스턴스 배열로 반환합니다.

```php
Passport::scopes();
```

`scopesFor` 메서드는 전달된 ID/이름에 해당하는 `Laravel\Passport\Scope` 인스턴스들을 배열로 반환합니다.

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

특정 스코프가 정의되어 있는지 확인하려면 `hasScope` 메서드를 사용할 수 있습니다.

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA 인증

API를 개발할 때, 자바스크립트 애플리케이션이 직접 API를 소비할 수 있게 하는 것이 매우 유용한 전략이 될 수 있습니다. 이런 방식으로 개발하면, 웹 앱, 모바일 앱, 외부 제3자 앱, 배포할 SDK 등 다양한 소비자가 모두 동일한 API를 사용할 수 있게 됩니다.

일반적으로 자바스크립트 앱에서 API를 호출하려면 액세스 토큰을 직접 전달해야 하며, 모든 요청마다 이 토큰을 포함해야 합니다. 하지만 Passport에는 이 과정을 자동화할 수 있는 미들웨어가 내장되어 있습니다. 애플리케이션의 `bootstrap/app.php`에서 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어를 추가하면 자동으로 처리가 가능합니다.

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어는 미들웨어 스택의 **가장 마지막**에 위치해야 합니다.

이 미들웨어를 사용하면 응답에 `laravel_token` 쿠키가 자동으로 포함됩니다. 이 쿠키는 암호화된 JWT를 담고 있으며, Passport는 이 JWT를 이용해 자바스크립트 애플리케이션이 보낸 API 요청을 인증합니다. JWT의 유효기간은 `session.lifetime` 설정값과 동일합니다. 이제 브라우저가 모든 후속 요청마다 해당 쿠키를 자동으로 포함해서 전송하므로, 별도로 액세스 토큰을 전달할 필요 없이 API 요청을 할 수 있습니다.

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이징

필요하다면 `Passport::cookie` 메서드로 `laravel_token` 쿠키의 이름을 변경할 수 있습니다. 이 메서드는 일반적으로 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출해야 합니다.

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

이 방식의 인증을 사용할 땐, 요청에 유효한 CSRF 토큰 헤더를 포함해야 합니다. 라라벨의 기본 자바스크립트 스캐폴딩과 모든 스타터 키트는 [Axios](https://github.com/axios/axios) 인스턴스를 포함하고 있으며, 이 인스턴스는 기본적으로 암호화된 `XSRF-TOKEN` 쿠키 값을 사용해 같은 도메인 요청마다 `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.

> [!NOTE]
> 만약 `X-XSRF-TOKEN` 대신 `X-CSRF-TOKEN` 헤더를 전송하고 싶다면, 반드시 `csrf_token()`에서 반환하는 **암호화되지 않은** 토큰을 사용해야 합니다.

<a name="events"></a>
## 이벤트

Passport는 액세스 토큰 및 리프레시 토큰 발급 시 event를 발생시킵니다. [이벤트 리스너](/docs/12.x/events)를 등록해, 데이터베이스에서 다른 액세스 토큰을 정리(prune)하거나 폐기(revoke)할 수도 있습니다.

<div class="overflow-auto">

| 이벤트 이름                                     |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## 테스트

Passport의 `actingAs` 메서드를 사용하면, 현재 인증된 사용자와 허용할 스코프를 테스트 환경에서 쉽게 지정할 수 있습니다. 첫 번째 인자는 사용자 인스턴스, 두 번째는 해당 사용자의 토큰에 부여할 스코프 배열입니다.

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

Passport의 `actingAsClient` 메서드는, 현재 인증된 클라이언트와 부여할 스코프를 테스트 내에서 지정하는 데 사용할 수 있습니다. 첫 번째 인자는 클라이언트 인스턴스, 두 번째는 해당 클라이언트 토큰에 부여할 스코프 배열입니다.

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