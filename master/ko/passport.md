# Laravel Passport

- [소개](#introduction)
    - [Passport와 Sanctum 중 선택하기](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [Passport 업그레이드하기](#upgrading-passport)
- [설정](#configuration)
    - [클라이언트 비밀 해싱](#client-secret-hashing)
    - [토큰 수명 설정](#token-lifetimes)
    - [기본 모델 재정의하기](#overriding-default-models)
    - [라우트 재정의하기](#overriding-routes)
- [액세스 토큰 발급](#issuing-access-tokens)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청](#requesting-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [PKCE를 사용하는 권한 부여 코드 그랜트](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청](#requesting-auth-pkce-grant-tokens)
- [패스워드 그랜트 토큰](#password-grant-tokens)
    - [패스워드 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청](#requesting-password-grant-tokens)
    - [모든 스코프 요청하기](#requesting-all-scopes)
    - [사용자 프로바이더 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 커스터마이징](#customizing-the-password-validation)
- [암시적 그랜트 토큰](#implicit-grant-tokens)
- [클라이언트 자격 증명 그랜트 토큰](#client-credentials-grant-tokens)
- [개인 액세스 토큰](#personal-access-tokens)
    - [개인 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [개인 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어를 통한 보호](#via-middleware)
    - [액세스 토큰 전달하기](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의하기](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당하기](#assigning-scopes-to-tokens)
    - [스코프 검사하기](#checking-scopes)
- [JavaScript에서 API 사용하기](#consuming-your-api-with-javascript)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Passport](https://github.com/laravel/passport)는 Laravel 애플리케이션에 완벽한 OAuth2 서버 구현을 몇 분 안에 제공합니다. Passport는 Andy Millington과 Simon Hamp가 유지 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server)를 기반으로 만들어졌습니다.

> [!WARNING]
> 이 문서는 OAuth2에 대한 기본 지식을 가지고 있다고 가정합니다. OAuth2에 대해 잘 모른다면, 계속 진행하기 전에 일반적인 [용어](https://oauth2.thephpleague.com/terminology/)와 기능들에 대해 먼저 익혀보시길 권장합니다.

<a name="passport-or-sanctum"></a>
### Passport와 Sanctum 중 선택하기 (Passport or Sanctum?)

시작하기 전에, Laravel Passport가 적합한지 아니면 [Laravel Sanctum](/docs/master/sanctum)을 사용하는 것이 더 나은지 결정하길 원할 수 있습니다. 애플리케이션에 반드시 OAuth2 지원이 필요하다면 Laravel Passport를 사용해야 합니다.

하지만 싱글 페이지 애플리케이션, 모바일 앱 인증, 또는 API 토큰 발급이 목적이라면 [Laravel Sanctum](/docs/master/sanctum)을 사용하세요. Sanctum은 OAuth2를 지원하지 않지만 더 간단한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치 (Installation)

Laravel Passport는 `install:api` Artisan 명령어로 설치할 수 있습니다:

```shell
php artisan install:api --passport
```

이 명령어는 OAuth2 클라이언트와 액세스 토큰을 저장하기 위한 테이블 생성에 필요한 데이터베이스 마이그레이션을 게시하고 실행합니다. 또한 안전한 액세스 토큰 생성을 위해 필요한 암호화 키도 생성합니다.

추가로, 이 명령어는 Passport `Client` 모델의 기본 키로 자동 증가 정수 대신 UUID를 사용할지 여부를 묻습니다.

`install:api` 명령어 실행 후 `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트를 추가하세요. 이 트레이트는 인증된 사용자의 토큰과 스코프를 검사할 수 있는 몇 가지 헬퍼 메서드를 제공합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

마지막으로, 애플리케이션 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고 `driver` 옵션을 `passport`로 설정하세요. 이렇게 하면 들어오는 API 요청을 인증할 때 Passport의 `TokenGuard`를 사용하게 됩니다:

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

애플리케이션 서버에 Passport를 처음 배포할 때, 보통 `passport:keys` 명령어를 실행해야 합니다. 이 명령은 액세스 토큰을 생성하는 데 필요한 암호화 키를 생성합니다. 생성된 키는 일반적으로 소스 관리에 포함하지 않습니다.

```shell
php artisan passport:keys
```

필요하다면 Passport 키를 불러올 경로를 지정할 수 있습니다. `Passport::loadKeysFrom` 메서드를 사용하면 됩니다. 보통 이 메서드는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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
#### 환경 변수에서 키 불러오기 (Loading Keys From the Environment)

또한 `vendor:publish` Artisan 명령어로 Passport 설정 파일을 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일이 게시된 후에는, 암호화 키를 환경 변수로 정의하여 애플리케이션에 로드할 수 있습니다:

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="upgrading-passport"></a>
### Passport 업그레이드하기 (Upgrading Passport)

Passport의 주요 버전을 업그레이드할 때는 꼭 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 주의 깊게 살펴보세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="client-secret-hashing"></a>
### 클라이언트 비밀 해싱 (Client Secret Hashing)

클라이언트 비밀을 데이터베이스에 저장할 때 해시 처리하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 `Passport::hashClientSecrets` 메서드를 호출하세요:

```php
use Laravel\Passport\Passport;

Passport::hashClientSecrets();
```

이 기능이 활성화되면, 클라이언트 비밀은 생성 직후에만 사용자에게 보여지고, 원본 문자열은 데이터베이스에 저장되지 않아 분실 시 복구할 수 없습니다.

<a name="token-lifetimes"></a>
### 토큰 수명 설정 (Token Lifetimes)

기본적으로 Passport는 1년 후 만료되는 장기 액세스 토큰을 발행합니다. 더 길거나 짧은 수명을 설정하고 싶다면 `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출할 수 있습니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensExpireIn(now()->addDays(15));
    Passport::refreshTokensExpireIn(now()->addDays(30));
    Passport::personalAccessTokensExpireIn(now()->addMonths(6));
}
```

> [!WARNING]
> Passport 데이터베이스 테이블의 `expires_at` 칼럼은 읽기 전용이며 표시용입니다. 토큰 발급 시, 만료 정보는 서명되고 암호화된 토큰 안에 저장됩니다. 토큰을 무효화하려면 [토큰을 폐기](#revoking-tokens)해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 재정의하기 (Overriding Default Models)

Passport 내부에서 사용하는 모델들을 원하는 대로 확장할 수 있습니다. 직접 모델을 정의하고 해당 Passport 모델을 상속하면 됩니다:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

정의한 모델을 Passport가 사용하도록 지시하려면 `Laravel\Passport\Passport` 클래스를 사용하세요. 보통 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 아래처럼 알립니다:

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\PersonalAccessClient;
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
    Passport::usePersonalAccessClientModel(PersonalAccessClient::class);
}
```

<a name="overriding-routes"></a>
### 라우트 재정의하기 (Overriding Routes)

Passport가 정의한 라우트를 커스터마이징하려면, 먼저 애플리케이션 `AppServiceProvider` 클래스의 `register` 메서드에 `Passport::ignoreRoutes`를 추가해 Passport 기본 라우트를 무시하세요:

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

그다음, Passport의 기본 라우트가 정의된 [routes 파일](https://github.com/laravel/passport/blob/12.x/routes/web.php)을 복사하여 애플리케이션 `routes/web.php`에 넣고 원하는 대로 수정할 수 있습니다:

```php
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => '\Laravel\Passport\Http\Controllers',
], function () {
    // Passport 라우트들...
});
```

<a name="issuing-access-tokens"></a>
## 액세스 토큰 발급 (Issuing Access Tokens)

OAuth2 권한 부여 코드 방식을 활용하는 경우가 가장 일반적입니다. 권한 부여 코드 방식에서는 클라이언트 애플리케이션이 사용자를 서버의 인증 화면으로 리다이렉션하여 액세스 토큰 발급 요청을 승인 또는 거부할 수 있게 합니다.

<a name="managing-clients"></a>
### 클라이언트 관리 (Managing Clients)

우선, API와 상호작용할 애플리케이션 개발자는 본인의 애플리케이션을 "클라이언트"로 등록해야 합니다. 보통 클라이언트 이름과 권한 승인 후 사용자 리다이렉트될 URL을 제공합니다.

<a name="the-passportclient-command"></a>
#### `passport:client` 명령어 (The `passport:client` Command)

클라이언트를 생성하는 가장 간단한 방법은 `passport:client` Artisan 명령어를 사용하는 것입니다. OAuth2 기능 테스트용 클라이언트를 위해 직접 생성할 수 있습니다. 명령 실행 시 클라이언트 관련 정보 입력을 요청하고 클라이언트 ID와 비밀을 제공합니다:

```shell
php artisan passport:client
```

**리다이렉트 URL**

여러 개의 리다이렉트 URL을 등록하려면, 쉼표로 구분한 URL 목록을 명령어에서 입력하세요. 쉼표가 포함된 URL은 URL 인코딩해야 합니다:

```shell
http://example.com/callback,http://examplefoo.com/callback
```

<a name="clients-json-api"></a>
#### JSON API

사용자가 직접 `client` 명령어를 사용할 수 없기 때문에, Passport는 클라이언트를 생성, 수정, 삭제할 수 있는 JSON API도 제공합니다. 이 API를 이용하려면, 사용자용 대시보드 프론트엔드와 연결해 관리할 수 있게 구현해야 합니다.

API는 `web`과 `auth` 미들웨어로 보호되어 있어 외부에서 호출할 수 없고, 반드시 내부 애플리케이션에서만 사용할 수 있습니다.

<a name="get-oauthclients"></a>
#### `GET /oauth/clients`

인증된 사용자의 모든 클라이언트를 반환합니다. 사용자가 자신의 클라이언트를 편집하거나 삭제할 때 주로 사용됩니다:

```js
axios.get('/oauth/clients')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthclients"></a>
#### `POST /oauth/clients`

새 클라이언트 생성 요청입니다. `name`과 승인/거부 후 리다이렉트할 `redirect` URL이 필요합니다. 성공하면 새 클라이언트 인스턴스를 반환합니다:

```js
const data = {
    name: 'Client Name',
    redirect: 'http://example.com/callback'
};

axios.post('/oauth/clients', data)
    .then(response => {
        console.log(response.data);
    })
    .catch (response => {
        // 응답의 오류 표시...
    });
```

<a name="put-oauthclientsclient-id"></a>
#### `PUT /oauth/clients/{client-id}`

클라이언트 정보 업데이트 요청입니다. `name`과 `redirect` URL이 필요하며, 수정된 클라이언트 인스턴스를 반환합니다:

```js
const data = {
    name: 'New Client Name',
    redirect: 'http://example.com/callback'
};

axios.put('/oauth/clients/' + clientId, data)
    .then(response => {
        console.log(response.data);
    })
    .catch (response => {
        // 응답의 오류 표시...
    });
```

<a name="delete-oauthclientsclient-id"></a>
#### `DELETE /oauth/clients/{client-id}`

클라이언트 삭제 요청입니다:

```js
axios.delete('/oauth/clients/' + clientId)
    .then(response => {
        // ...
    });
```

<a name="requesting-tokens"></a>
### 토큰 요청 (Requesting Tokens)

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인증을 위한 리다이렉트 (Redirecting for Authorization)

클라이언트를 생성한 후, 클라이언트 ID와 비밀로 권한 부여 코드와 액세스 토큰 요청이 가능합니다. 먼저, 소비 애플리케이션은 아래와 같이 `/oauth/authorize` 경로로 리다이렉트 요청을 해야 합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'client-id',
        'redirect_uri' => 'http://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => '',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", 또는 "login"
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

`prompt` 파라미터는 Passport 애플리케이션의 인증 동작을 제어합니다.  
- `none`일 경우, 사용자가 인증되어 있지 않으면 항상 인증 에러를 발생시킵니다.
- `consent`일 경우, 이전에 스코프 허용 여부와 관계없이 항상 승인 화면을 보여줍니다.
- `login`일 경우, 기존 세션이 있어도 항상 재로그인 요청을 합니다.

`prompt`가 없으면, 사용자가 요청한 스코프에 대해 아직 권한을 부여하지 않았다면 승인 화면이 나타납니다.

> [!NOTE]
> `/oauth/authorize` 경로는 Passport가 이미 정의하므로 직접 라우트를 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 요청 승인 (Approving the Request)

Passport는 `prompt` 값에 따라 자동으로 응답하며, 사용자가 승인 또는 거부할 수 있는 UI를 표시합니다. 사용자가 승인을 하면, 클라이언트가 생성 시 설정한 `redirect_uri`로 리다이렉트됩니다.

승인 화면을 커스터마이징하려면, Passport 뷰를 Artisan 명령어로 게시하세요. 게시된 뷰는 `resources/views/vendor/passport`에 위치합니다:

```shell
php artisan vendor:publish --tag=passport-views
```

첫 번째 파티 클라이언트 등 일부 경우에는 승인 프롬프트를 건너뛸 수도 있습니다. 이 경우 [기본 모델 재정의](#overriding-default-models)처럼 `Client` 모델을 확장해 `skipsAuthorization` 메서드를 정의하고 `true`를 반환하면 됩니다. 단, 클라이언트가 명시적으로 `prompt` 파라미터를 사용한 경우에는 무시됩니다:

```php
<?php

namespace App\Models\Passport;

use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 클라이언트가 승인 프롬프트를 건너뛸지 결정합니다.
     */
    public function skipsAuthorization(): bool
    {
        return $this->firstParty();
    }
}
```

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
#### 권한 부여 코드를 액세스 토큰으로 변환하기 (Converting Authorization Codes to Access Tokens)

사용자가 승인하면, 클라이언트 애플리케이션으로 리다이렉트되며 `state` 파라미터 값이 일치하는지 검증해야 합니다. 검증이 완료되면, 승인 시 발급된 코드를 포함하여 `/oauth/token` 경로로 `POST` 요청을 보내 액세스 토큰을 요청합니다:

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

    $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'client-id',
        'client_secret' => 'client-secret',
        'redirect_uri' => 'http://third-party-app.com/callback',
        'code' => $request->code,
    ]);

    return $response->json();
});
```

이 `/oauth/token` 경로는 JSON 형식으로 `access_token`, `refresh_token`, `expires_in` 값을 반환합니다. `expires_in`은 토큰 만료까지 남은 시간을 초 단위로 나타냅니다.

> [!NOTE]
> `/oauth/token` 경로 역시 Passport가 자동으로 정의하므로 직접 선언할 필요가 없습니다.

<a name="tokens-json-api"></a>
#### JSON API

Passport는 권한 있는 액세스 토큰 관리를 위한 JSON API도 제공합니다. 이를 프론트엔드와 결합해 사용자가 액세스 토큰을 관리할 수 있는 대시보드를 만들 수 있습니다. API는 `web` 및 `auth` 미들웨어로 보호되어 내부 애플리케이션에서만 호출할 수 있습니다.

<a name="get-oauthtokens"></a>
#### `GET /oauth/tokens`

인증된 사용자가 생성한 모든 권한 있는 액세스 토큰을 반환합니다. 사용자 토큰 목록을 보여주고 토큰을 폐기할 때 유용합니다:

```js
axios.get('/oauth/tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="delete-oauthtokenstoken-id"></a>
#### `DELETE /oauth/tokens/{token-id}`

권한 있는 액세스 토큰과 관련된 갱신 토큰(refresh token)을 폐기할 때 사용합니다:

```js
axios.delete('/oauth/tokens/' + tokenId);
```

<a name="refreshing-tokens"></a>
### 토큰 갱신 (Refreshing Tokens)

짧은 수명의 액세스 토큰을 발급하는 경우, 사용자는 갱신 토큰으로 토큰을 갱신해야 합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('http://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'client-id',
    'client_secret' => 'client-secret',
    'scope' => '',
]);

return $response->json();
```

`/oauth/token` 경로는 `access_token`, `refresh_token`, `expires_in` 값을 JSON으로 반환합니다.

<a name="revoking-tokens"></a>
### 토큰 폐기 (Revoking Tokens)

`Laravel\Passport\TokenRepository` 클래스의 `revokeAccessToken` 메서드로 액세스 토큰을 폐기할 수 있습니다. 또한 `Laravel\Passport\RefreshTokenRepository` 클래스의 `revokeRefreshTokensByAccessTokenId` 메서드를 사용해 해당 액세스 토큰의 갱신 토큰도 폐기할 수 있습니다. 아래는 Laravel 서비스 컨테이너를 이용해 이 클래스들을 resolve하는 예시입니다:

```php
use Laravel\Passport\TokenRepository;
use Laravel\Passport\RefreshTokenRepository;

$tokenRepository = app(TokenRepository::class);
$refreshTokenRepository = app(RefreshTokenRepository::class);

// 액세스 토큰 폐기...
$tokenRepository->revokeAccessToken($tokenId);

// 관련 갱신 토큰 모두 폐기...
$refreshTokenRepository->revokeRefreshTokensByAccessTokenId($tokenId);
```

<a name="purging-tokens"></a>
### 토큰 정리 (Purging Tokens)

폐기되었거나 만료된 토큰을 데이터베이스에서 삭제하려면 Passport의 `passport:purge` Artisan 명령어를 사용할 수 있습니다:

```shell
# 폐기 및 만료된 토큰과 인증 코드 정리
php artisan passport:purge

# 6시간 이상 만료된 토큰만 정리
php artisan passport:purge --hours=6

# 폐기된 토큰과 인증 코드만 정리
php artisan passport:purge --revoked

# 만료된 토큰과 인증 코드만 정리
php artisan passport:purge --expired
```

자동화하려면 애플리케이션 `routes/console.php` 파일에 스케줄러 작업을 추가할 수도 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## PKCE를 사용하는 권한 부여 코드 그랜트 (Authorization Code Grant With PKCE)

PKCE(Proof Key for Code Exchange)를 사용하는 권한 부여 코드 그랜트는 싱글 페이지 애플리케이션이나 네이티브 애플리케이션이 API에 안전하게 접근하는 방식입니다. 이는 클라이언트 비밀을 안전하게 저장하기 어렵거나 권한 부여 코드 탈취 공격 위험을 줄이는 목적으로 사용됩니다. 액세스 토큰 교환 시 클라이언트 비밀 대신 "코드 검증자(code verifier)"와 "코드 챌린지(code challenge)" 조합을 사용합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성 (Creating the Client)

PKCE 클라이언트를 생성하려면 `passport:client` 명령어와 `--public` 옵션을 사용하세요:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청 (Requesting Tokens)

<a name="code-verifier-code-challenge"></a>
#### 코드 검증자와 코드 챌린지 (Code Verifier and Code Challenge)

이 그랜트는 클라이언트 비밀을 제공하지 않으므로, 개발자는 코드 검증자와 코드 챌린지 쌍을 생성해야 합니다.

`code_verifier`는 43~128자의 무작위 문자열로, 영문자, 숫자, `"-"`, `"."`, `"_"`, `"~"` 문자를 포함할 수 있으며 [RFC 7636](https://tools.ietf.org/html/rfc7636) 규격을 따릅니다.

`code_challenge`는 `code_verifier`를 SHA256 해시한 뒤 URL 안전한 Base64 형식으로 인코딩한 문자열로, 끝에 있는 `'='` 문자는 제거하고 공백이나 추가 문자는 없어야 합니다.

```php
$encoded = base64_encode(hash('sha256', $code_verifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 인증을 위한 리다이렉트 (Redirecting for Authorization)

클라이언트 생성 후, 클라이언트 ID 및 위에서 생성한 코드 검증자와 코드 챌린지를 이용해 인증 코드를 요청할 수 있습니다. 클라이언트는 먼저 Passport 앱의 `/oauth/authorize` 경로로 리다이렉트 요청을 보냅니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $request->session()->put(
        'code_verifier', $code_verifier = Str::random(128)
    );

    $codeChallenge = strtr(rtrim(
        base64_encode(hash('sha256', $code_verifier, true))
    , '='), '+/', '-_');

    $query = http_build_query([
        'client_id' => 'client-id',
        'redirect_uri' => 'http://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => '',
        'state' => $state,
        'code_challenge' => $codeChallenge,
        'code_challenge_method' => 'S256',
        // 'prompt' => '', // "none", "consent", 또는 "login"
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
#### 권한 부여 코드를 액세스 토큰으로 변환하기 (Converting Authorization Codes to Access Tokens)

사용자가 승인을 하면 클라이언트 앱으로 리다이렉트되고, 클라이언트는 `state` 값을 검증합니다. 검증이 성공하면 권한 부여 코드와 원래의 코드 검증자를 포함해 `/oauth/token` 경로로 POST 요청을 보내 액세스 토큰을 요청합니다:

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

    $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'client-id',
        'redirect_uri' => 'http://third-party-app.com/callback',
        'code_verifier' => $codeVerifier,
        'code' => $request->code,
    ]);

    return $response->json();
});
```

<a name="password-grant-tokens"></a>
## 패스워드 그랜트 토큰 (Password Grant Tokens)

> [!WARNING]
> 패스워드 그랜트 토큰은 더 이상 권장하지 않습니다. 대신 [OAuth2 서버에서 현재 권장하는 그랜트 유형](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

OAuth2 패스워드 그랜트를 사용하면 모바일 앱과 같은 1차 클라이언트가 이메일과 비밀번호로 액세스 토큰을 안전하게 얻을 수 있습니다. 사용자에게 OAuth2 권한 부여 코드 리다이렉션 과정을 거치게 하지 않아도 됩니다.

활성화하려면 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 `enablePasswordGrant` 메서드를 호출하세요:

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
### 패스워드 그랜트 클라이언트 생성 (Creating a Password Grant Client)

패스워드 그랜트 토큰 발급 전에, `--password` 옵션으로 패스워드 그랜트 클라이언트를 생성해야 합니다. 이미 `passport:install` 명령을 실행했다면 이 명령은 다시 실행할 필요가 없습니다:

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청 (Requesting Tokens)

패스워드 그랜트 클라이언트를 생성한 뒤, `/oauth/token` 경로에 사용자 이메일과 비밀번호를 포함한 `POST` 요청으로 액세스 토큰을 요청할 수 있습니다. 이 경로도 Passport가 기본 제공하므로 별도 정의가 필요 없습니다. 성공 시 JSON 응답에 `access_token`과 `refresh_token`이 포함됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('http://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'client-id',
    'client_secret' => 'client-secret',
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '',
]);

return $response->json();
```

> [!NOTE]
> 액세스 토큰은 기본적으로 장기 토큰입니다. 필요시 [최대 토큰 수명 설정](#configuration)을 조정할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청하기 (Requesting All Scopes)

패스워드 그랜트나 클라이언트 자격 증명 그랜트에서, 토큰에 애플리케이션이 지원하는 모든 스코프 권한을 허용하려면 `*` 스코프를 요청하세요. 이 경우 토큰의 `can` 메서드는 항상 `true`를 반환합니다. `*` 스코프는 이 두 그랜트 유형에서만 사용 가능합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('http://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'client-id',
    'client_secret' => 'client-secret',
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### 사용자 프로바이더 커스터마이징 (Customizing the User Provider)

애플리케이션에서 여러 인증 사용자 프로바이더를 사용하는 경우, `passport:client --password` 명령어로 클라이언트를 생성할 때 `--provider` 옵션으로 사용할 프로바이더 이름을 지정할 수 있습니다. 지정한 프로바이더 이름은 `config/auth.php`에서 정의한 유효한 프로바이더 이름이어야 합니다. 이후 미들웨어에서 해당 가드로 보호하여 해당 프로바이더만 인증되도록 구성할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명 필드 커스터마이징 (Customizing the Username Field)

패스워드 그랜트 인증 시 Passport는 기본적으로 `email` 속성을 사용자명으로 사용합니다. 다르게 지정하려면 모델에 `findForPassport` 메서드를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable
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
### 비밀번호 검증 커스터마이징 (Customizing the Password Validation)

패스워드 그랜트 인증 시 Passport는 모델의 `password` 속성으로 전달된 비밀번호를 검증합니다. 모델에 `password` 속성이 없거나 커스텀 검증 로직이 필요하면 `validateForPassportPasswordGrant` 메서드를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Support\Facades\Hash;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Passport 패스워드 그랜트 인증용 비밀번호 유효성 검사
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant-tokens"></a>
## 암시적 그랜트 토큰 (Implicit Grant Tokens)

> [!WARNING]
> 암시적 그랜트 토큰은 권장하지 않습니다. 대신 [현재 OAuth2 서버가 추천하는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

암시적 그랜트는 권한 부여 코드 그랜트와 유사하지만, 권한 부여 코드 교환 과정 없이 토큰을 바로 클라이언트에 반환합니다. JavaScript나 모바일 앱처럼 클라이언트 자격 증명을 안전하게 저장할 수 없을 때 주로 사용합니다. 활성화하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 `enableImplicitGrant` 메서드를 호출하세요:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

활성화 된 후 개발자는 클라이언트 ID로 `/oauth/authorize` 경로에 리다이렉트하여 액세스 토큰을 요청할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'client-id',
        'redirect_uri' => 'http://third-party-app.com/callback',
        'response_type' => 'token',
        'scope' => '',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", 또는 "login"
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

> [!NOTE]
> `/oauth/authorize` 경로는 Passport가 이미 정의하므로 별도 정의할 필요가 없습니다.

<a name="client-credentials-grant-tokens"></a>
## 클라이언트 자격 증명 그랜트 토큰 (Client Credentials Grant Tokens)

클라이언트 자격 증명 그랜트는 기기간 인증에 적합합니다. 예를 들어, 예약 작업에서 API를 통해 유지보수 작업 등을 할 때 사용할 수 있습니다.

클라이언트 자격 증명 그랜트로 토큰을 발급하려면 우선 `passport:client` 명령어에서 `--client` 옵션을 사용해 클라이언트를 생성하세요:

```shell
php artisan passport:client --client
```

이 그랜트 유형을 사용할 때는 `CheckClientCredentials` 미들웨어에 별칭을 등록해야 합니다. `bootstrap/app.php` 파일에서 미들웨어 별칭을 설정할 수 있습니다:

```php
use Laravel\Passport\Http\Middleware\CheckClientCredentials;

->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'client' => CheckClientCredentials::class
    ]);
})
```

그 후, 필요한 라우트에 미들웨어를 할당하여 보호하세요:

```php
Route::get('/orders', function (Request $request) {
    // ...
})->middleware('client');
```

특정 스코프에만 접근 제한하려면, `client` 미들웨어에 쉼표 구분 스코프 목록을 전달할 수 있습니다:

```php
Route::get('/orders', function (Request $request) {
    // ...
})->middleware('client:check-status,your-scope');
```

<a name="retrieving-tokens"></a>
### 토큰 조회 (Retrieving Tokens)

이 그랜트를 통해 토큰을 얻으려면 `oauth/token` 엔드포인트로 요청하세요:

```php
use Illuminate\Support\Facades.Http;

$response = Http::asForm()->post('http://passport-app.test/oauth/token', [
    'grant_type' => 'client_credentials',
    'client_id' => 'client-id',
    'client_secret' => 'client-secret',
    'scope' => 'your-scope',
]);

return $response->json()['access_token'];
```

<a name="personal-access-tokens"></a>
## 개인 액세스 토큰 (Personal Access Tokens)

사용자가 일반 권한 부여 코드 흐름 없이 스스로 액세스 토큰을 발급하도록 허용할 수도 있습니다. 이는 사용자가 API를 실험하거나, 더 쉽게 액세스 토큰을 발급하도록 할 때 유용합니다.

> [!NOTE]
> 애플리케이션에서 주로 개인 액세스 토큰 발급 용도로 Passport를 쓴다면, 더 가벼운 1차 라이브러리인 [Laravel Sanctum](/docs/master/sanctum)을 고려하세요.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성 (Creating a Personal Access Client)

개인 액세스 토큰을 발급하려면 먼저 `passport:client` 명령어의 `--personal` 옵션으로 개인 액세스 클라이언트를 생성해야 합니다. 이미 `passport:install`을 실행했으면 생략 가능합니다:

```shell
php artisan passport:client --personal
```

생성 후, 해당 클라이언트 ID와 평문 비밀 값을 `.env` 파일에 입력하세요:

```ini
PASSPORT_PERSONAL_ACCESS_CLIENT_ID="client-id-value"
PASSPORT_PERSONAL_ACCESS_CLIENT_SECRET="unhashed-client-secret-value"
```

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리 (Managing Personal Access Tokens)

이후 사용자 모델 인스턴스에서 `createToken` 메서드를 사용해 특정 사용자에 대한 토큰을 생성할 수 있습니다. 첫 번째 인수는 토큰 이름이며, 두 번째 인수는 선택적 스코프 배열입니다:

```php
use App\Models\User;

$user = User::find(1);

// 스코프 없이 토큰 생성...
$token = $user->createToken('Token Name')->accessToken;

// 스코프 지정하여 토큰 생성...
$token = $user->createToken('My Token', ['place-orders'])->accessToken;
```

<a name="personal-access-tokens-json-api"></a>
#### JSON API

개인 액세스 토큰 관리를 위한 JSON API도 제공하며, 사용자 대시보드와 연동할 수 있습니다. 앞서 소개한 것처럼, API는 `web`과 `auth` 미들웨어로 보호되어 내부에서만 사용할 수 있습니다.

<a name="get-oauthscopes"></a>
#### `GET /oauth/scopes`

애플리케이션에 정의된 모든 스코프 목록을 반환합니다. 사용자가 개인 액세스 토큰에 할당 가능한 스코프를 볼 때 유용합니다:

```js
axios.get('/oauth/scopes')
    .then(response => {
        console.log(response.data);
    });
```

<a name="get-oauthpersonal-access-tokens"></a>
#### `GET /oauth/personal-access-tokens`

인증된 사용자가 생성한 모든 개인 액세스 토큰을 반환합니다:

```js
axios.get('/oauth/personal-access-tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthpersonal-access-tokens"></a>
#### `POST /oauth/personal-access-tokens`

새 개인 액세스 토큰을 생성합니다. `name`과 `scopes` 배열이 필요합니다:

```js
const data = {
    name: 'Token Name',
    scopes: []
};

axios.post('/oauth/personal-access-tokens', data)
    .then(response => {
        console.log(response.data.accessToken);
    })
    .catch (response => {
        // 응답 에러 표시...
    });
```

<a name="delete-oauthpersonal-access-tokenstoken-id"></a>
#### `DELETE /oauth/personal-access-tokens/{token-id}`

개인 액세스 토큰을 폐기할 때 사용합니다:

```js
axios.delete('/oauth/personal-access-tokens/' + tokenId);
```

<a name="protecting-routes"></a>
## 라우트 보호하기 (Protecting Routes)

<a name="via-middleware"></a>
### 미들웨어를 통한 보호 (Via Middleware)

Passport는 들어오는 요청에서 액세스 토큰을 검증하는 [인증 가드](/docs/master/authentication#adding-custom-guards)를 제공합니다. `api` 가드를 `passport` 드라이버로 설정했다면, 액세스 토큰이 필요한 라우트에 `auth:api` 미들웨어만 지정하면 됩니다:

```php
Route::get('/user', function () {
    // ...
})->middleware('auth:api');
```

> [!WARNING]
> 클라이언트 자격 증명 그랜트를 사용할 경우, `auth:api` 대신 [클라이언트 미들웨어](#client-credentials-grant-tokens)를 사용해 라우트를 보호해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 다중 인증 가드 (Multiple Authentication Guards)

애플리케이션에서 서로 다른 Eloquent 모델을 사용하는 다중 사용자 유형을 인증해야 한다면, 사용자 프로바이더 유형별로 가드를 정의해야 할 수 있습니다. 예를 들어, `config/auth.php`에 다음과 같이 가드를 정의할 수 있습니다:

```php
'api' => [
    'driver' => 'passport',
    'provider' => 'users',
],

'api-customers' => [
    'driver' => 'passport',
    'provider' => 'customers',
],
```

아래 라우트는 `customers` 프로바이더를 사용하는 `api-customers` 가드를 통해 요청을 인증합니다:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport와 다중 사용자 프로바이더에 대한 자세한 내용은 [패스워드 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달하기 (Passing the Access Token)

Passport로 보호된 라우트를 호출할 때는, API 소비자가 요청 헤더 `Authorization`에 `Bearer` 토큰 형식으로 액세스 토큰을 포함해야 합니다. 예를 들어 Guzzle HTTP 라이브러리를 사용할 때는 다음과 같습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => 'Bearer '.$accessToken,
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
## 토큰 스코프 (Token Scopes)

스코프는 API 클라이언트가 계정 접근 권한 요청 시 특정 권한 집합을 지정하게 해줍니다. 예를 들어 전자상거래 앱에서 주문을 생성할 필요 없는 클라이언트는 오직 주문 배송 상태 확인 권한만 요청하도록 제한할 수 있습니다. 즉, 스코프는 사용자가 타사 애플리케이션이 자신을 대신해 수행할 수 있는 행동 범위를 제한하게 합니다.

<a name="defining-scopes"></a>
### 스코프 정의하기 (Defining Scopes)

API 스코프는 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 `Passport::tokensCan` 메서드로 정의합니다. 배열 인수로 스코프 이름과 설명을 지정할 수 있으며, 설명은 승인 화면에 표시됩니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensCan([
        'place-orders' => 'Place orders',
        'check-status' => 'Check order status',
    ]);
}
```

<a name="default-scope"></a>
### 기본 스코프 (Default Scope)

클라이언트가 특정 스코프를 요청하지 않으면, Passport가 기본적으로 할당하는 스코프를 지정하려면 `setDefaultScope` 메서드를 사용하세요. 보통 `boot` 메서드에서 호출합니다:

```php
use Laravel\Passport\Passport;

Passport::tokensCan([
    'place-orders' => 'Place orders',
    'check-status' => 'Check order status',
]);

Passport::setDefaultScope([
    'check-status',
    'place-orders',
]);
```

> [!NOTE]
> 기본 스코프는 사용자 발급 개인 액세스 토큰에는 적용되지 않습니다.

<a name="assigning-scopes-to-tokens"></a>
### 토큰에 스코프 할당하기 (Assigning Scopes to Tokens)

<a name="when-requesting-authorization-codes"></a>
#### 권한 부여 코드 요청 시 (When Requesting Authorization Codes)

권한 부여 코드 그랜트 방식으로 액세스 토큰을 요청할 때, 원하는 스코프를 `scope` 쿼리 파라미터로 공백 구분 리스트 형태로 전달합니다:

```php
Route::get('/redirect', function () {
    $query = http_build_query([
        'client_id' => 'client-id',
        'redirect_uri' => 'http://example.com/callback',
        'response_type' => 'code',
        'scope' => 'place-orders check-status',
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="when-issuing-personal-access-tokens"></a>
#### 개인 액세스 토큰 발급 시 (When Issuing Personal Access Tokens)

`App\Models\User` 모델의 `createToken` 메서드로 개인 액세스 토큰을 발급할 때 스코프 배열을 두 번째 인수로 전달할 수 있습니다:

```php
$token = $user->createToken('My Token', ['place-orders'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 검사하기 (Checking Scopes)

Passport는 들어오는 요청 토큰이 특정 스코프를 포함하는지 검증하는 두 개의 미들웨어를 제공합니다. 먼저 `bootstrap/app.php`에서 다음 미들웨어 별칭을 정의하세요:

```php
use Laravel\Passport\Http\Middleware\CheckForAnyScope;
use Laravel\Passport\Http\Middleware\CheckScopes;

->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'scopes' => CheckScopes::class,
        'scope' => CheckForAnyScope::class,
    ]);
})
```

<a name="check-for-all-scopes"></a>
#### 모든 스코프 검사 (Check For All Scopes)

`scopes` 미들웨어는 요청에 포함된 토큰에 명시된 모든 스코프가 있어야 합니다:

```php
Route::get('/orders', function () {
    // 액세스 토큰에 "check-status"와 "place-orders" 모두 포함됨...
})->middleware(['auth:api', 'scopes:check-status,place-orders']);
```

<a name="check-for-any-scopes"></a>
#### 하나 이상 스코프 검사 (Check for Any Scopes)

`scope` 미들웨어는 요청 토큰에 특정 스코프 중 하나 이상이 포함되어 있으면 통과시킵니다:

```php
Route::get('/orders', function () {
    // 액세스 토큰에 "check-status" 또는 "place-orders" 중 하나 포함됨...
})->middleware(['auth:api', 'scope:check-status,place-orders']);
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 검사하기 (Checking Scopes on a Token Instance)

인증된 액세스 토큰이 있는 요청에 한해, `App\Models\User` 인스턴스의 `tokenCan` 메서드로 특정 스코프 보유 여부를 확인할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('place-orders')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
#### 추가 스코프 메서드들 (Additional Scope Methods)

`scopeIds` 메서드는 정의된 스코프 ID/이름 배열을 반환합니다:

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

`scopes` 메서드는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다:

```php
Passport::scopes();
```

`scopesFor` 메서드는 지정한 스코프 ID/이름에 매칭되는 `Scope` 인스턴스 배열을 반환합니다:

```php
Passport::scopesFor(['place-orders', 'check-status']);
```

`hasScope` 메서드로 특정 스코프가 정의되었는지 확인할 수 있습니다:

```php
Passport::hasScope('place-orders');
```

<a name="consuming-your-api-with-javascript"></a>
## JavaScript에서 API 사용하기 (Consuming Your API With JavaScript)

API를 구축할 때, JavaScript 애플리케이션에서 직접 자신의 API를 호출할 수 있으면 매우 유용합니다. 이 방법은 웹 앱, 모바일 앱, 타사 앱, SDK 등 다양한 클라이언트에서 동일 API를 활용하도록 합니다.

보통은 액세스 토큰을 수동으로 JavaScript 앱에 전달하고 요청마다 포함해야 하지만, Passport는 이 과정을 자동화하는 미들웨어를 제공합니다. 애플리케이션 `bootstrap/app.php`에서 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어를 추가하기만 하면 됩니다:

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어는 미들웨어 스택 내에서 반드시 마지막에 위치해야 합니다.

이 미들웨어는 `laravel_token` 쿠키를 응답에 첨부합니다. 쿠키 내용은 암호화된 JWT이며, Passport가 JavaScript에서 API 요청 인증에 사용합니다. JWT 수명은 `session.lifetime` 설정과 동일합니다. 브라우저가 쿠키를 자동으로 전송하므로, 별도 액세스 토큰 전달 없이 API 요청을 할 수 있습니다:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 변경하기 (Customizing the Cookie Name)

쿠키 이름을 변경할 필요가 있으면 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 `Passport::cookie` 메서드로 이름을 지정하세요:

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

이 인증 방식에서는 유효한 CSRF 토큰 헤더를 요청에 포함시켜야 합니다. 기본 Laravel JavaScript 스캐폴딩은 Axios 인스턴스를 포함하며, 암호화된 `XSRF-TOKEN` 쿠키 값을 자동으로 읽어 같은 출처 요청에 `X-XSRF-TOKEN` 헤더를 전송합니다.

> [!NOTE]
> `X-CSRF-TOKEN` 헤더를 보낼 경우, `csrf_token()`으로 제공되는 비암호화 토큰을 사용해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

Passport는 액세스 토큰 및 갱신 토큰 발급 시 이벤트를 발생시킵니다. 이 이벤트를 [리스닝](/docs/master/events)하여 데이터베이스 내 다른 토큰을 폐기하거나 정리할 수 있습니다:

| 이벤트 이름 |
| --- |
| `Laravel\Passport\Events\AccessTokenCreated` |
| `Laravel\Passport\Events\RefreshTokenCreated` |

<a name="testing"></a>
## 테스트 (Testing)

Passport의 `actingAs` 메서드는 현재 인증된 사용자와 그 사용자가 가진 스코프들을 지정할 때 사용합니다. 첫 번째 인수로 사용자 인스턴스, 두 번째 인수로 토큰에 부여할 스코프 배열을 전달합니다:

```php tab=Pest
use App\Models\User;
use Laravel\Passport\Passport;

test('servers can be created', function () {
    Passport::actingAs(
        User::factory()->create(),
        ['create-servers']
    );

    $response = $this->post('/api/create-server');

    $response->assertStatus(201);
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Passport\Passport;

public function test_servers_can_be_created(): void
{
    Passport::actingAs(
        User::factory()->create(),
        ['create-servers']
    );

    $response = $this->post('/api/create-server');

    $response->assertStatus(201);
}
```

또한 `actingAsClient` 메서드는 현재 인증된 클라이언트와 클라이언트 토큰의 스코프를 지정할 때 사용합니다. 첫 번째 인수로 클라이언트 인스턴스, 두 번째 인수로 스코프 배열을 전달합니다:

```php tab=Pest
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

test('orders can be retrieved', function () {
    Passport::actingAsClient(
        Client::factory()->create(),
        ['check-status']
    );

    $response = $this->get('/api/orders');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

public function test_orders_can_be_retrieved(): void
{
    Passport::actingAsClient(
        Client::factory()->create(),
        ['check-status']
    );

    $response = $this->get('/api/orders');

    $response->assertStatus(200);
}
```