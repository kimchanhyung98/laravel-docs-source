# Laravel Passport

- [소개](#introduction)
    - [Passport 또는 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포](#deploying-passport)
    - [Passport 업그레이드](#upgrading-passport)
- [설정](#configuration)
    - [클라이언트 시크릿 해싱](#client-secret-hashing)
    - [토큰 수명](#token-lifetimes)
    - [기본 모델 재정의](#overriding-default-models)
    - [라우트 재정의](#overriding-routes)
- [액세스 토큰 발급](#issuing-access-tokens)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청](#requesting-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [PKCE를 이용한 권한 부여 코드 그랜트](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청](#requesting-auth-pkce-grant-tokens)
- [패스워드 그랜트 토큰](#password-grant-tokens)
    - [패스워드 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [사용자 프로바이더 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [패스워드 검증 커스터마이징](#customizing-the-password-validation)
- [암묵적 그랜트 토큰](#implicit-grant-tokens)
- [클라이언트 자격 증명 그랜트 토큰](#client-credentials-grant-tokens)
- [개인 액세스 토큰](#personal-access-tokens)
    - [개인 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [개인 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호](#protecting-routes)
    - [미들웨어 사용법](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당](#assigning-scopes-to-tokens)
    - [스코프 체크](#checking-scopes)
- [JavaScript로 API 사용하기](#consuming-your-api-with-javascript)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Passport](https://github.com/laravel/passport)는 Laravel 애플리케이션에 몇 분 만에 완전한 OAuth2 서버 구현을 제공합니다. Passport는 Andy Millington과 Simon Hamp가 유지보수하는 [League OAuth2 서버](https://github.com/thephpleague/oauth2-server)를 기반으로 만들어졌습니다.

> [!WARNING]  
> 이 문서는 이미 OAuth2에 익숙하다고 가정하고 있습니다. OAuth2에 대해 모른다면, 계속 진행하기 전에 일반적인 [용어](https://oauth2.thephpleague.com/terminology/)와 OAuth2의 기능들을 먼저 익히시기 바랍니다.

<a name="passport-or-sanctum"></a>
### Passport 또는 Sanctum?

시작하기 전에, 애플리케이션에 Laravel Passport와 [Laravel Sanctum](/docs/11.x/sanctum) 중 어느 쪽이 더 적합한지 판단할 수 있습니다. 애플리케이션이 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용해야 합니다.

반면, SPA(single-page application), 모바일 애플리케이션을 인증하거나 API 토큰을 발급하려는 경우, [Laravel Sanctum](/docs/11.x/sanctum)을 사용하는 것이 더 간단한 API 인증 개발 경험을 제공합니다. Sanctum은 OAuth2를 지원하지 않습니다.

<a name="installation"></a>
## 설치

`install:api` Artisan 명령어를 사용하여 Laravel Passport를 설치할 수 있습니다:

```shell
php artisan install:api --passport
```

이 명령어는 OAuth2 클라이언트와 액세스 토큰을 저장하는 데 필요한 데이터베이스 테이블의 마이그레이션을 게시 및 실행합니다. 또한 보안 액세스 토큰을 생성하는 데 필요한 암호화 키를 생성합니다.

추가로, Passport `Client` 모델의 기본 키로 자동 증가 정수 대신 UUID 사용 여부도 묻습니다.

`install:api` 명령어 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트를 추가해야 합니다. 이 트레이트는 인증된 사용자의 토큰과 스코프를 검사할 수 있도록 몇 가지 헬퍼 메서드를 제공합니다:

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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고, `driver` 옵션을 `passport`로 설정해야 합니다. 이렇게 하면 들어오는 API 요청을 인증할 때 Passport의 `TokenGuard`를 사용하게 됩니다:

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
### Passport 배포

애플리케이션 서버에 Passport를 처음 배포할 때는 `passport:keys` 명령어를 실행해야 할 수 있습니다. 이 명령어는 액세스 토큰 생성에 필요한 암호화 키를 생성합니다. 생성된 키는 보통 소스 컨트롤에 포함하지 않습니다:

```shell
php artisan passport:keys
```

필요하다면, Passport 키를 불러올 경로를 정의할 수 있습니다. `Passport::loadKeysFrom` 메서드를 사용하세요. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
}
```

<a name="loading-keys-from-the-environment"></a>
#### 환경 변수에서 키 불러오기

대안으로, `vendor:publish` Artisan 명령어를 사용해 Passport 설정 파일을 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일이 게시된 후, 환경 변수에 암호화 키를 정의하여 애플리케이션 키를 불러올 수 있습니다:

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

Passport의 새 메이저 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 주의 깊게 검토하세요.

<a name="configuration"></a>
## 설정

<a name="client-secret-hashing"></a>
### 클라이언트 시크릿 해싱

클라이언트 시크릿을 데이터베이스에 저장할 때 해싱하고 싶다면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드 내에서 `Passport::hashClientSecrets` 메서드를 호출하세요:

```php
use Laravel\Passport\Passport;

Passport::hashClientSecrets();
```

이 설정을 활성화하면 클라이언트 시크릿은 생성 직후에만 출력되며, 평문 시크릿 값은 데이터베이스에 저장되지 않으므로 분실 시 복구할 수 없습니다.

<a name="token-lifetimes"></a>
### 토큰 수명

기본적으로 Passport는 1년 후 만료되는 장기 액세스 토큰을 발급합니다. 더 길거나 짧은 토큰 수명을 설정하려면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들도 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 호출하세요:

```php
/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Passport::tokensExpireIn(now()->addDays(15));
    Passport::refreshTokensExpireIn(now()->addDays(30));
    Passport::personalAccessTokensExpireIn(now()->addMonths(6));
}
```

> [!WARNING]  
> Passport 데이터베이스 테이블의 `expires_at` 칼럼은 읽기 전용이며 단지 표시 목적으로만 사용됩니다. 실제로 토큰 만료 정보는 서명되고 암호화된 토큰 내에 저장됩니다. 토큰을 무효화하려면 [폐기](#revoking-tokens)해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 재정의

Passport에서 내부적으로 사용하는 모델을 확장하여 자신의 커스텀 모델을 정의할 수 있습니다. Passport 모델을 상속해 새 클래스를 만든 후:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 `Laravel\Passport\Passport` 클래스를 통해 Passport에 자신의 모델을 알려줄 수 있습니다:

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\PersonalAccessClient;
use App\Models\Passport\RefreshToken;
use App\Models\Passport\Token;

/**
 * 애플리케이션 서비스 부트스트랩
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
### 라우트 재정의

가끔 Passport가 제공하는 라우트를 커스터마이징해야 할 때가 있습니다. 이때는 먼저 애플리케이션의 `AppServiceProvider` 클래스 `register` 메서드에서 `Passport::ignoreRoutes`를 호출해 Passport가 라우트를 등록하지 못하게 해야 합니다:

```php
use Laravel\Passport\Passport;

/**
 * 애플리케이션 서비스 등록
 */
public function register(): void
{
    Passport::ignoreRoutes();
}
```

그리고 Passport의 [라우트 파일](https://github.com/laravel/passport/blob/11.x/routes/web.php)에서 라우트 정의를 복사해 애플리케이션의 `routes/web.php`에 붙여넣고 원하는 대로 수정하세요:

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
## 액세스 토큰 발급

OAuth2의 권한 부여 코드를 사용하는 방식은 대부분 개발자가 OAuth2를 가장 많이 접하는 방법입니다. 권한 부여 코드를 사용할 경우, 클라이언트 애플리케이션이 사용자를 서버의 인증 페이지로 리디렉션하여 액세스 토큰 발급 요청을 승인하거나 거부하게 됩니다.

<a name="managing-clients"></a>
### 클라이언트 관리

애플리케이션 API와 상호작용할 다른 개발자는 자신의 애플리케이션을 "클라이언트"로 등록해야 합니다. 보통 클라이언트 이름과, 사용자가 애플리케이션 승인을 마친 후 리디렉션할 URL을 입력하게 됩니다.

<a name="the-passportclient-command"></a>
#### `passport:client` 명령

클라이언트를 생성하는 가장 간단한 방법은 `passport:client` Artisan 명령어를 사용하는 것입니다. 이 명령어는 OAuth2 기능 테스트용 클라이언트를 쉽게 생성할 수 있습니다. 실행 시, Passport가 클라이언트에 관한 정보를 묻고 클라이언트 ID와 시크릿을 제공합니다:

```shell
php artisan passport:client
```

**리디렉션 URL**

여러 개의 리디렉션 URL을 허용하려면, 쉼표로 구분된 목록으로 입력하세요. 쉼표가 포함된 URL은 URL 인코딩해야 합니다:

```shell
http://example.com/callback,http://examplefoo.com/callback
```

<a name="clients-json-api"></a>
#### JSON API

사용자가 직접 `client` 명령을 사용할 수 없으니, Passport가 제공하는 JSON API를 이용해 클라이언트를 생성할 수 있습니다. 이를 통해 컨트롤러를 직접 작성하지 않고도 클라이언트 생성, 수정, 삭제가 가능합니다.

다만, 사용자가 클라이언트를 관리할 수 있는 대시보드를 별도로 만들어야 하며, 아래는 클라이언트 관리 API의 엔드포인트들입니다. 예시로 [Axios](https://github.com/axios/axios)를 사용해 HTTP 요청하는 모습을 보여드립니다.

JSON API는 `web`과 `auth` 미들웨어로 보호되므로, 외부에서 호출할 수 없고 애플리케이션 내부에서만 호출 가능합니다.

<a name="get-oauthclients"></a>
#### `GET /oauth/clients`

인증된 사용자가 생성한 모든 클라이언트를 반환합니다. 주로 사용자가 자신의 클라이언트들을 편집하거나 삭제하기 위한 목록 기능에 쓰입니다:

```js
axios.get('/oauth/clients')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthclients"></a>
#### `POST /oauth/clients`

새 클라이언트를 생성합니다. 클라이언트 `name`과 승인 후 리디렉션할 `redirect` URL 두 가지 데이터가 필요합니다.

생성 성공 시 클라이언트 ID와 시크릿이 부여되고, 새 클라이언트 인스턴스가 반환됩니다:

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
        // 에러 처리...
    });
```

<a name="put-oauthclientsclient-id"></a>
#### `PUT /oauth/clients/{client-id}`

클라이언트 정보를 수정합니다. `name`과 `redirect` 필드를 넘겨야 하며 수정된 클라이언트 인스턴스를 반환합니다:

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
        // 에러 처리...
    });
```

<a name="delete-oauthclientsclient-id"></a>
#### `DELETE /oauth/clients/{client-id}`

클라이언트를 삭제합니다:

```js
axios.delete('/oauth/clients/' + clientId)
    .then(response => {
        // ...
    });
```

<a name="requesting-tokens"></a>
### 토큰 요청

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 권한 부여를 위한 리디렉션

클라이언트가 생성된 이후, 클라이언트 ID와 시크릿을 사용해 권한 부여 코드와 액세스 토큰을 요청할 수 있습니다. 먼저, 클라이언트 애플리케이션은 `/oauth/authorize` 경로로 리디렉션 요청을 수행합니다:

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
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

`prompt` 매개변수로 Passport 애플리케이션의 인증 동작을 제어할 수 있습니다.

- `none`: 사용자가 이미 인증되어 있지 않으면 인증 오류를 발생시킵니다.
- `consent`: 모든 스코프를 이미 승인했더라도 항상 승인 화면을 표시합니다.
- `login`: 기존 세션이 있어도 항상 재로그인 요구합니다.

`prompt`가 없으면, 이전에 승인하지 않은 스코프에 대해서만 승인 화면이 표시됩니다.

> [!NOTE]  
> `/oauth/authorize` 라우트는 Passport가 기본 정의하므로 직접 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 요청 승인

권한 부여 요청을 받으면 Passport는 `prompt` 값에 따라 자동으로 응답하며, 승인 또는 거부할 수 있는 화면을 사용자에게 보여줍니다. 사용자가 승인하면 소비자 애플리케이션에서 지정한 `redirect_uri`로 리디렉션됩니다. 이 URI는 클라이언트 생성 시 입력한 리디렉션 URL과 일치해야 합니다.

승인 화면을 커스터마이징하고 싶으면, `vendor:publish` Artisan 명령어로 뷰를 게시할 수 있습니다. 게시된 뷰는 `resources/views/vendor/passport`에 위치합니다:

```shell
php artisan vendor:publish --tag=passport-views
```

첫 번째 당사자 클라이언트 인증 시 승인 프롬프트를 생략하고 싶다면, [`Client` 모델 확장](#overriding-default-models) 후 `skipsAuthorization` 메서드를 정의하여 true를 반환하세요. 단, 클라이언트가 명시적으로 `prompt` 파라미터를 설정하지 않은 경우만 작동합니다:

```php
<?php

namespace App\Models\Passport;

use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 클라이언트가 승인 프롬프트를 건너뛸지 여부 결정
     */
    public function skipsAuthorization(): bool
    {
        return $this->firstParty();
    }
}
```

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
#### 권한 부여 코드를 액세스 토큰으로 변환

사용자가 권한 부여 요청을 승인하면 소비자 애플리케이션으로 리디렉션됩니다. 소비자 애플리케이션은 리디렉션 전 저장했던 `state` 값과 응답 받은 `state` 값을 확인해야 합니다. 두 값이 일치하면 `POST` 요청을 보내 액세스 토큰을 요청합니다. 요청에는 사용자 승인 시 발급받은 권한 부여 코드가 포함되어야 합니다:

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

`/oauth/token` 경로는 `access_token`, `refresh_token`, `expires_in` 속성을 포함한 JSON 응답을 반환합니다. `expires_in`은 액세스 토큰 만료까지 남은 초 단위 시간입니다.

> [!NOTE]  
> `/oauth/token` 경로도 Passport가 기본 제공하므로 따로 정의할 필요가 없습니다.

<a name="tokens-json-api"></a>
#### JSON API

Passport는 승인된 액세스 토큰 관리를 위한 JSON API도 제공합니다. 이를 자신의 프론트엔드와 결합해 사용자가 토큰을 관리하는 대시보드를 제공할 수 있습니다.

JSON API는 `web`, `auth` 미들웨어가 적용되어 애플리케이션 내부에서만 호출 가능합니다.

<a name="get-oauthtokens"></a>
#### `GET /oauth/tokens`

인증된 사용자가 생성한 모든 액세스 토큰을 반환합니다. 사용자가 토큰을 나열하고 필요 시 폐기할 때 유용합니다:

```js
axios.get('/oauth/tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="delete-oauthtokenstoken-id"></a>
#### `DELETE /oauth/tokens/{token-id}`

이 경로로 토큰과 이에 관련된 리프레시 토큰을 폐기할 수 있습니다:

```js
axios.delete('/oauth/tokens/' + tokenId);
```

<a name="refreshing-tokens"></a>
### 토큰 갱신

짧은 수명 토큰을 사용하는 경우, 액세스 토큰 발급 시 함께 받은 리프레시 토큰으로 토큰을 갱신해야 합니다:

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

`/oauth/token` 경로는 위와 같이 새 액세스 토큰, 리프레시 토큰, 만료 시간 정보를 반환합니다.

<a name="revoking-tokens"></a>
### 토큰 폐기

`Laravel\Passport\TokenRepository`의 `revokeAccessToken` 메서드를 사용해 액세스 토큰을 폐기할 수 있습니다. 또한 `Laravel\Passport\RefreshTokenRepository`의 `revokeRefreshTokensByAccessTokenId` 메서드로 토큰의 모든 리프레시 토큰도 폐기할 수 있습니다. 이 클래스들은 [서비스 컨테이너](/docs/11.x/container)에서 의존성을 주입받아 사용합니다:

```php
use Laravel\Passport\TokenRepository;
use Laravel\Passport\RefreshTokenRepository;

$tokenRepository = app(TokenRepository::class);
$refreshTokenRepository = app(RefreshTokenRepository::class);

// 액세스 토큰 폐기
$tokenRepository->revokeAccessToken($tokenId);

// 해당 토큰 리프레시 토큰 전부 폐기
$refreshTokenRepository->revokeRefreshTokensByAccessTokenId($tokenId);
```

<a name="purging-tokens"></a>
### 토큰 정리

토큰이 폐기됐거나 만료된 후 데이터베이스에서 제거하고 싶을 수 있습니다. Passport의 `passport:purge` Artisan 명령어가 이를 도와줍니다:

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

자동으로 주기적으로 정리하려면, 애플리케이션의 `routes/console.php` 파일에 [스케줄 작업](/docs/11.x/scheduling)을 추가하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## PKCE를 이용한 권한 부여 코드 그랜트

"Proof Key for Code Exchange"(PKCE)를 사용하는 권한 부여 코드 그랜트는 SPA나 네이티브 앱에서 API를 안전하게 인증하는 방법입니다. 클라이언트 시크릿이 안전하게 저장된다는 보장이 없을 때 혹은 권한 부여 코드가 공격자에게 가로채이는 위험을 줄이기 위해 사용합니다. 클라이언트 시크릿 대신 "코드 검증자(code verifier)"와 "코드 챌린지(code challenge)" 조합을 사용합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성

PKCE 지원 클라이언트를 생성하려면 `passport:client` Artisan 명령어에 `--public` 옵션을 사용하세요:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청

<a name="code-verifier-code-challenge"></a>
#### 코드 검증자와 코드 챌린지

이 그랜트는 클라이언트 시크릿을 제공하지 않으므로, 토큰 요청 시 사용할 코드 검증자와 코드 챌린지를 생성해야 합니다.

- 코드 검증자: 43~128자 길이의 임의 문자열로, 영문자, 숫자, `"-"`, `"."`, `"_"`, `"~"` 문자를 포함합니다. [RFC 7636 규격](https://tools.ietf.org/html/rfc7636)을 따릅니다.
- 코드 챌린지: URL 및 파일명 안전한 Base64 인코딩 문자열이며, 끝의 `'='`는 제거하고 줄바꿈, 공백 등 추가 문자 없어야 합니다.

```php
$encoded = base64_encode(hash('sha256', $code_verifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 권한 부여를 위한 리디렉션

클라이언트가 생성된 후, 클라이언트 ID와 코드 검증자, 코드 챌린지를 사용해 권한 부여 코드와 액세스 토큰을 요청합니다. 우선 애플리케이션의 `/oauth/authorize` 경로로 리디렉션 요청을 수행합니다:

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
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
#### 권한 부여 코드를 액세스 토큰으로 변환

사용자가 승인하면 클라이언트 애플리케이션으로 리디렉션됩니다. `state` 값을 확인 후 POST 요청으로 액세스 토큰을 요청하세요. 요청에는 권한 부여 코드와 원래 생성한 코드 검증자를 포함해야 합니다:

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
## 패스워드 그랜트 토큰

> [!WARNING]  
> 패스워드 그랜트 토큰 사용은 더 이상 권장하지 않습니다. 대신 [OAuth2 서버 권장 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

OAuth2 패스워드 그랜트를 사용하면, 모바일 앱과 같은 다른 1차 클라이언트가 이메일 / 사용자명과 패스워드로 액세스 토큰을 받아갈 수 있습니다. 이 방식은 전체 리다이렉션 흐름 없이 1차 클라이언트에 안전하게 토큰을 발급할 수 있습니다.

패스워드 그랜트를 사용하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 `enablePasswordGrant` 메서드를 호출하세요:

```php
/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Passport::enablePasswordGrant();
}
```

<a name="creating-a-password-grant-client"></a>
### 패스워드 그랜트 클라이언트 생성

패스워드 그랜트 토큰을 발급하려면 `--password` 옵션으로 패스워드 그랜트 클라이언트를 생성해야 합니다. 단, `passport:install` 명령어를 이미 실행했다면 이 과정은 생략해도 됩니다:

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청

패스워드 그랜트 클라이언트 생성 후, 사용자의 이메일과 패스워드를 포함한 POST 요청으로 `/oauth/token` 경로에 접근해 액세스 토큰을 요청할 수 있습니다. 성공 시 JSON 응답으로 `access_token`과 `refresh_token`이 반환됩니다:

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
> 액세스 토큰은 기본적으로 장기 토큰입니다. 필요한 경우 [최대 토큰 수명 설정](#configuration)도 가능합니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청

패스워드 그랜트나 클라이언트 자격 증명 그랜트를 쓸 때는 애플리케이션에서 지원하는 모든 스코프를 허용하는 토큰을 요청할 수 있습니다. `scope`에 `*`를 기재하면 되고, 이 경우 토큰의 `can` 메서드는 항상 `true`를 반환합니다. `*` 스코프는 이 두 그랜트 유형으로 발급된 토큰에만 할당 가능합니다:

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
### 사용자 프로바이더 커스터마이징

애플리케이션에서 여러 인증 사용자 프로바이더를 사용하는 경우, 패스워드 그랜트 클라이언트를 생성할 때 `--provider` 옵션으로 클라이언트가 사용할 프로바이더를 지정할 수 있습니다. `--provider`에 전달한 이름은 `config/auth.php`에 정의된 유효한 프로바이더명이어야 합니다. 이후 [미들웨어를 통한 라우트 보호](#via-middleware) 시 해당 가드에 맞는 사용자만 인증되게 할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명 필드 커스터마이징

패스워드 그랜트를 이용한 인증 시 기본적으로 인증 가능한 모델의 `email` 필드를 사용자명(username)으로 사용합니다. 이를 변경하려면 모델에 `findForPassport` 메서드를 정의하세요:

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
     * 주어진 사용자명에 해당하는 사용자 인스턴스를 찾음
     */
    public function findForPassport(string $username): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### 패스워드 검증 커스터마이징

패스워드 그랜트 인증 시 Passport는 모델의 `password` 속성으로 검증합니다. `password` 속성이 없거나 검증 로직을 바꾸고 싶으면 `validateForPassportPasswordGrant` 메서드를 모델에 구현하세요:

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
     * Passport 패스워드 그랜트용 사용자 패스워드 검증
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant-tokens"></a>
## 암묵적 그랜트 토큰

> [!WARNING]  
> 암묵적 그랜트 토큰은 더 이상 권장하지 않습니다. 대신 [OAuth2 서버 권장 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

암묵적 그랜트는 권한 부여 코드 그랜트와 비슷하지만, 권한 부여 코드를 교환하지 않고 바로 토큰을 클라이언트에 반환하는 방식입니다. 보통 JavaScript나 모바일 앱에서 클라이언트 시크릿을 안전하게 저장할 수 없을 때 사용합니다.

활성화하려면 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 `enableImplicitGrant` 메서드를 호출하세요:

```php
/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

활성화 후 클라이언트는 자신의 클라이언트 ID를 사용해 `/oauth/authorize` 경로로 리디렉션해 액세스 토큰을 요청합니다:

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
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

> [!NOTE]  
> `/oauth/authorize` 경로는 Passport가 기본 제공하므로 직접 구현할 필요가 없습니다.

<a name="client-credentials-grant-tokens"></a>
## 클라이언트 자격 증명 그랜트 토큰

클라이언트 자격 증명 그랜트는 머신 간 인증에 적합합니다. 예를 들어 스케줄링된 작업이 API를 통해 유지보수 작업을 수행할 때 쓸 수 있습니다.

이 그랜트를 사용하려면 우선 `passport:client` 명령어의 `--client` 옵션으로 클라이언트를 생성하세요:

```shell
php artisan passport:client --client
```

이 그랜트를 사용할 때는 `CheckClientCredentials` 미들웨어의 별칭을 등록해야 합니다. 애플리케이션의 `bootstrap/app.php` 파일에서 아래와 같이 미들웨어 별칭을 정의하세요:

```php
use Laravel\Passport\Http\Middleware\CheckClientCredentials;

->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'client' => CheckClientCredentials::class
    ]);
})
```

이후 라우트에 미들웨어를 붙여 클라이언트 자격 증명으로 보호할 수 있습니다:

```php
Route::get('/orders', function (Request $request) {
    ...
})->middleware('client');
```

특정 스코프 권한이 있어야 접근 가능하도록 스코프를 쉼표로 구분해 미들웨어에 넘길 수도 있습니다:

```php
Route::get('/orders', function (Request $request) {
    ...
})->middleware('client:check-status,your-scope');
```

<a name="retrieving-tokens"></a>
### 토큰 요청

클라이언트 자격 증명 그랜트로 토큰을 얻으려면 `oauth/token` 엔드포인트에 아래와 같이 요청합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('http://passport-app.test/oauth/token', [
    'grant_type' => 'client_credentials',
    'client_id' => 'client-id',
    'client_secret' => 'client-secret',
    'scope' => 'your-scope',
]);

return $response->json()['access_token'];
```

<a name="personal-access-tokens"></a>
## 개인 액세스 토큰

종종 사용자들이 OAuth2 전체 권한 부여 흐름 없이 직접 자신의 액세스 토큰을 발급받고 싶어할 때가 있습니다. 애플리케이션 UI를 통해 사용자에게 토큰을 발급할 수 있게 하는 것은 API를 실험해보거나 간단한 액세스 토큰 발급 방식을 제공할 때 유용합니다.

> [!NOTE]  
> 대부분 개인 액세스 토큰 발급에 Passport를 사용하는 경우, Laravel가 제공하는 경량 API 토큰 라이브러리인 [Laravel Sanctum](/docs/11.x/sanctum)을 고려해보세요.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성

개인 액세스 토큰 발급을 위해서는 `--personal` 옵션으로 개인 액세스 클라이언트를 생성해야 합니다. `passport:install` 명령어를 이미 실행했다면 이 단계는 생략 가능합니다:

```shell
php artisan passport:client --personal
```

클라이언트 ID와 평문 시크릿 값을 `.env` 파일에 등록하세요:

```ini
PASSPORT_PERSONAL_ACCESS_CLIENT_ID="client-id-value"
PASSPORT_PERSONAL_ACCESS_CLIENT_SECRET="unhashed-client-secret-value"
```

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리

개인 액세스 클라이언트 생성 후, `App\Models\User` 인스턴스의 `createToken` 메서드로 토큰을 발급할 수 있습니다. 첫 번째 인자는 토큰 이름이고, 두 번째는 선택적 스코프 배열입니다:

```php
use App\Models\User;

$user = User::find(1);

// 스코프 없는 토큰 생성
$token = $user->createToken('Token Name')->accessToken;

// 스코프 포함 토큰 생성
$token = $user->createToken('My Token', ['place-orders'])->accessToken;
```

<a name="personal-access-tokens-json-api"></a>
#### JSON API

Passport는 개인 액세스 토큰 관리를 위한 JSON API도 제공합니다. 이를 자신의 프론트엔드와 합쳐 사용자에게 토큰을 관리하는 대시보드를 제공할 수 있습니다.

JSON API는 `web`과 `auth` 미들웨어가 적용되어 외부에서 호출 불가능합니다.

<a name="get-oauthscopes"></a>
#### `GET /oauth/scopes`

애플리케이션에 정의된 모든 [스코프](#token-scopes)를 반환합니다. 사용자가 개인 액세스 토큰에 지정할 수 있는 스코프들을 나열하는 데 쓸 수 있습니다:

```js
axios.get('/oauth/scopes')
    .then(response => {
        console.log(response.data);
    });
```

<a name="get-oauthpersonal-access-tokens"></a>
#### `GET /oauth/personal-access-tokens`

인증된 사용자가 생성한 모든 개인 액세스 토큰을 반환합니다. 사용자 토큰 편집이나 폐기 시 유용합니다:

```js
axios.get('/oauth/personal-access-tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthpersonal-access-tokens"></a>
#### `POST /oauth/personal-access-tokens`

새 개인 액세스 토큰을 만듭니다. 토큰 `name`과 할당할 `scopes` 배열이 필요합니다:

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
        // 에러 처리...
    });
```

<a name="delete-oauthpersonal-access-tokenstoken-id"></a>
#### `DELETE /oauth/personal-access-tokens/{token-id}`

개인 액세스 토큰을 폐기합니다:

```js
axios.delete('/oauth/personal-access-tokens/' + tokenId);
```

<a name="protecting-routes"></a>
## 라우트 보호

<a name="via-middleware"></a>
### 미들웨어 사용법

Passport는 들어오는 요청의 액세스 토큰을 검증하는 [인증 가드](/docs/11.x/authentication#adding-custom-guards)를 포함합니다. `api` 가드를 `passport` 드라이버로 설정한 후, 인증이 필요한 라우트에 `auth:api` 미들웨어만 붙이면 유효한 액세스 토큰이 있어야 접근할 수 있습니다:

```php
Route::get('/user', function () {
    // ...
})->middleware('auth:api');
```

> [!WARNING]  
> 클라이언트 자격 증명 그랜트를 사용하는 경우, `auth:api` 대신 [‘client’ 미들웨어](#client-credentials-grant-tokens)를 사용하세요.

<a name="multiple-authentication-guards"></a>
#### 다중 인증 가드

애플리케이션에서 서로 다른 Eloquent 모델을 사용하는 여러 사용자 유형을 인증할 경우, 각각의 사용자 프로바이더에 맞춰 가드 설정을 해야 합니다. 예를 들어 `config/auth.php`에 다음과 같은 설정이 있을 수 있습니다:

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

이때 다음과 같이 `api-customers` 가드를 사용하는 라우트가 가능해집니다:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]  
> Passport에서 다중 사용자 프로바이더를 사용하는 방법은 [패스워드 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달

Passport로 보호된 라우트를 호출할 때, API 소비자는 요청의 `Authorization` 헤더에 `Bearer` 토큰을 지정해야 합니다. 예를 들어 Guzzle HTTP 라이브러리 사용 시:

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => 'Bearer '.$accessToken,
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
## 토큰 스코프

스코프를 사용하면 API 클라이언트가 특정 권한만 요청할 수 있습니다. 예를 들어 전자상거래 앱에서 모든 API 소비자가 주문을 생성할 필요는 없고, 배송 상태 확인 권한만 요청할 수 있게 하는 식입니다.

즉, 스코프는 사용자가 3자 앱에게 허용하는 액션 범위를 제한하게 합니다.

<a name="defining-scopes"></a>
### 스코프 정의

애플리케이션 스코프는 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드 내에서 `Passport::tokensCan` 메서드로 정의합니다. 배열 키는 스코프 이름, 값은 설명입니다. 설명은 승인 화면에 표시됩니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩
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
### 기본 스코프

클라이언트가 특정 스코프를 요청하지 않으면 Passport 서버에서 기본으로 할당할 스코프도 설정할 수 있습니다. `setDefaultScope` 메서드를 사용하며, 보통 `AppServiceProvider` 클래스 `boot` 메서드에 배치합니다:

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
> 기본 스코프 설정은 사용자가 직접 생성하는 개인 액세스 토큰에는 적용되지 않습니다.

<a name="assigning-scopes-to-tokens"></a>
### 토큰에 스코프 할당

<a name="when-requesting-authorization-codes"></a>
#### 권한 부여 코드 요청 시

권한 부여 코드 그랜트로 액세스 토큰을 요청할 때는 `scope` 쿼리 스트링에 원하는 스코프를 공백으로 구분해 명시해야 합니다:

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
#### 개인 액세스 토큰 발급 시

`App\Models\User` 모델 `createToken` 메서드로 개인 액세스 토큰을 발급할 때 두 번째 인자로 스코프 배열을 전달할 수 있습니다:

```php
$token = $user->createToken('My Token', ['place-orders'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 체크

Passport는 두 가지 미들웨어를 제공해 토큰에 특정 스코프가 부여되었는지 확인할 수 있습니다. `bootstrap/app.php`에서 별칭을 등록하세요:

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
#### 모든 스코프 확인

`scopes` 미들웨어는 접속 토큰이 나열된 모든 스코프를 포함하는지 검사합니다:

```php
Route::get('/orders', function () {
    // 액세스 토큰이 "check-status"와 "place-orders" 스코프 모두 갖고 있음
})->middleware(['auth:api', 'scopes:check-status,place-orders']);
```

<a name="check-for-any-scopes"></a>
#### 최소 하나 이상 스코프 확인

`scope` 미들웨어는 접속 토큰이 나열된 스코프 중 최소 하나라도 가지고 있는지 검사합니다:

```php
Route::get('/orders', function () {
    // 액세스 토큰에 "check-status" 또는 "place-orders" 스코프 중 하나 이상 있음
})->middleware(['auth:api', 'scope:check-status,place-orders']);
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 검사

토큰 인증된 요청 내부에서는 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드로 특정 스코프 보유 여부를 확인할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('place-orders')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
#### 추가 스코프 메서드

- `scopeIds`: 정의된 모든 스코프 ID / 이름 배열 반환

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

- `scopes`: 정의된 모든 스코프를 `Laravel\Passport\Scope` 인스턴스 배열로 반환

```php
Passport::scopes();
```

- `scopesFor`: 주어진 이름들의 `Laravel\Passport\Scope` 인스턴스 배열 반환

```php
Passport::scopesFor(['place-orders', 'check-status']);
```

- `hasScope`: 특정 스코프가 정의됐는지 확인 (불리언 반환)

```php
Passport::hasScope('place-orders');
```

<a name="consuming-your-api-with-javascript"></a>
## JavaScript로 API 사용하기

API를 개발할 때, 자신의 JavaScript 앱에서도 동일 API를 사용할 수 있으면 매우 편리합니다. 자신뿐 아니라 모바일 및 타사 앱, SDK 등에서 동일한 API를 쓸 수 있어 개발 생산성을 높여줍니다.

일반적으로는 액세스 토큰을 자바스크립트로 전달하고 각 요청에 포함시켜야 하지만, Passport는 이를 자동으로 처리하는 미들웨어를 제공합니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어만 추가하면 됩니다:

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]  
> `CreateFreshApiToken` 미들웨어는 반드시 미들웨어 스택에서 가장 마지막에 위치해야 합니다.

이 미들웨어는 `laravel_token` 쿠키를 응답에 첨부합니다. 이 쿠키는 암호화된 JWT를 담고 있으며, Passport가 자바스크립트 API 요청 인증에 활용합니다. JWT 수명은 `session.lifetime` 설정과 동일합니다.

브라우저가 자동으로 쿠키를 요청에 포함시키므로, 액세스 토큰을 명시적으로 전달하지 않고도 API 요청이 가능합니다:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이징

필요하다면 `Passport::cookie` 메서드로 `laravel_token` 쿠키 이름을 변경할 수 있습니다. 보통 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드에서 호출합니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Passport::cookie('custom_name');
}
```

<a name="csrf-protection"></a>
#### CSRF 보호

이 인증 방식은 요청에 유효한 CSRF 토큰 헤더를 포함해야 합니다. 기본 Laravel JavaScript 스캐폴딩에는 Axios 인스턴스가 포함되어 있어, 암호화된 `XSRF-TOKEN` 쿠키 값을 동일 출처 요청에 `X-XSRF-TOKEN` 헤더로 자동 전송합니다.

> [!NOTE]  
> 대신 `X-CSRF-TOKEN` 헤더를 보내려면, `csrf_token()` 함수가 제공하는 **암호화되지 않은** 토큰 값을 사용해야 합니다.

<a name="events"></a>
## 이벤트

Passport는 액세스 토큰과 리프레시 토큰 발급 시 이벤트를 발생시킵니다. [이벤트 리스너](/docs/11.x/events)를 등록해 데이터베이스 내 기존 토큰을 정리하거나 폐기할 수 있습니다:

| 이벤트명 |
| --- |
| `Laravel\Passport\Events\AccessTokenCreated` |
| `Laravel\Passport\Events\RefreshTokenCreated` |

<a name="testing"></a>
## 테스트

Passport의 `actingAs` 메서드를 사용해 현재 인증된 사용자 인스턴스와 해당 토큰의 스코프를 지정할 수 있습니다. 첫 번째 인자는 사용자 인스턴스, 두 번째는 부여할 스코프 배열입니다:

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

`actingAsClient` 메서드는 현재 인증된 클라이언트 인스턴스와 토큰 스코프를 지정할 때 사용합니다. 첫 번째 인자는 클라이언트, 두 번째는 부여할 스코프 배열입니다:

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