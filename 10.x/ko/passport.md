# Laravel Passport

- [소개](#introduction)
    - [Passport 또는 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [마이그레이션 커스터마이징](#migration-customization)
    - [Passport 업그레이드](#upgrading-passport)
- [설정](#configuration)
    - [클라이언트 비밀값 해싱](#client-secret-hashing)
    - [토큰 수명 설정](#token-lifetimes)
    - [기본 모델 재정의하기](#overriding-default-models)
    - [라우트 재정의하기](#overriding-routes)
- [액세스 토큰 발급](#issuing-access-tokens)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청하기](#requesting-tokens)
    - [토큰 갱신하기](#refreshing-tokens)
    - [토큰 폐기하기](#revoking-tokens)
    - [토큰 정리하기](#purging-tokens)
- [PKCE가 적용된 Authorization Code Grant](#code-grant-pkce)
    - [클라이언트 생성하기](#creating-a-auth-pkce-grant-client)
    - [토큰 요청하기](#requesting-auth-pkce-grant-tokens)
- [Password Grant 토큰](#password-grant-tokens)
    - [Password Grant 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [사용자 프로바이더 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 커스터마이징](#customizing-the-password-validation)
- [Implicit Grant 토큰](#implicit-grant-tokens)
- [Client Credentials Grant 토큰](#client-credentials-grant-tokens)
- [개인 액세스 토큰](#personal-access-tokens)
    - [개인 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [개인 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어 사용](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의하기](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당하기](#assigning-scopes-to-tokens)
    - [스코프 확인하기](#checking-scopes)
- [JavaScript로 API 사용하기](#consuming-your-api-with-javascript)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Passport](https://github.com/laravel/passport)는 몇 분 만에 Laravel 애플리케이션에 완전한 OAuth2 서버 구현을 제공합니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 서버](https://github.com/thephpleague/oauth2-server) 위에 구축되었습니다.

> [!WARNING]  
> 이 문서는 OAuth2에 익숙하다고 가정합니다. OAuth2에 대해 잘 모른다면, 계속하기 전에 일반적인 [용어](https://oauth2.thephpleague.com/terminology/)와 OAuth2의 기능들을 먼저 익히는 것이 좋습니다.

<a name="passport-or-sanctum"></a>
### Passport 또는 Sanctum?

시작하기 전에, 애플리케이션에 Laravel Passport와 [Laravel Sanctum](/docs/10.x/sanctum) 중 어느 것이 더 적합한지 결정할 필요가 있습니다. 애플리케이션이 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용하세요.

하지만, 단일 페이지 애플리케이션, 모바일 애플리케이션 인증 또는 API 토큰 발급이 목적이라면 [Laravel Sanctum](/docs/10.x/sanctum)을 사용하는 것이 적합합니다. Laravel Sanctum은 OAuth2를 지원하지 않지만, 훨씬 간단한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 관리자를 통해 Passport를 설치합니다:

```shell
composer require laravel/passport
```

Passport의 [서비스 프로바이더](/docs/10.x/providers)는 자체 데이터베이스 마이그레이션 경로를 등록하므로, 패키지 설치 후 데이터베이스 마이그레이션을 실행해야 합니다. Passport 마이그레이션은 OAuth2 클라이언트와 액세스 토큰을 저장하는 테이블들을 만듭니다:

```shell
php artisan migrate
```

다음으로 `passport:install` Artisan 명령을 실행하세요. 이 명령은 안전한 액세스 토큰을 생성하는 데 필요한 암호화 키를 생성합니다. 또한, "퍼스널 액세스" 클라이언트와 "패스워드 그랜트" 클라이언트를 생성하며 이를 통해 액세스 토큰을 발급할 수 있습니다:

```shell
php artisan passport:install
```

> [!NOTE]  
> Passport `Client` 모델의 기본키를 자동 증가 정수가 아닌 UUID로 사용하려면, [``uuids`` 옵션](#client-uuids)을 사용해 Passport를 설치하세요.

`passport:install` 명령 실행 후 `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트를 추가하세요. 이 트레이트는 인증된 사용자의 토큰과 스코프를 검사하는 몇 가지 헬퍼 메서드를 제공합니다. 만약 모델에서 이미 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용 중이라면 제거해도 됩니다:

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

마지막으로 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고 `driver` 옵션을 `passport`로 설정하세요. 이를 통해 들어오는 API 요청 인증 시 Passport의 `TokenGuard`가 사용됩니다:

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

<a name="client-uuids"></a>
#### 클라이언트 UUID 사용

`passport:install` 명령을 실행할 때 `--uuids` 옵션을 함께 지정할 수 있습니다. 이 옵션은 Passport `Client` 모델의 기본키를 자동증가 정수가 아닌 UUID로 사용하도록 Passport에 지시합니다. `--uuids` 옵션과 함께 명령어 실행 후, 기본 마이그레이션을 비활성화하는 추가 지침이 출력됩니다:

```shell
php artisan passport:install --uuids
```

<a name="deploying-passport"></a>
### Passport 배포하기

애플리케이션 서버에 처음 Passport를 배포할 때는 `passport:keys` 명령을 실행해야 할 수도 있습니다. 이 명령은 액세스 토큰 생성에 필요한 암호화 키를 생성합니다. 생성된 키는 일반적으로 소스 컨트롤에 포함되지 않습니다:

```shell
php artisan passport:keys
```

필요시, Passport 키를 불러올 경로를 정의할 수 있습니다. `Passport::loadKeysFrom` 메서드를 사용하며, 일반적으로 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스 `boot` 메서드에서 호출합니다:

```php
/**
 * 인증 / 인가 관련 서비스 등록.
 */
public function boot(): void
{
    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
}
```

<a name="loading-keys-from-the-environment"></a>
#### 환경변수로 키 불러오기

대안으로 `vendor:publish` Artisan 명령으로 Passport 설정 파일을 발행할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일 발행 후, `.env` 파일에 애플리케이션 암호화 키를 환경변수로 정의하여 불러올 수 있습니다:

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="migration-customization"></a>
### 마이그레이션 커스터마이징

Passport의 기본 마이그레이션을 사용하지 않을 경우, `App\Providers\AppServiceProvider` 클래스 `register` 메서드에서 `Passport::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션을 내보내려면 다음 명령어를 사용하세요:

```shell
php artisan vendor:publish --tag=passport-migrations
```

<a name="upgrading-passport"></a>
### Passport 업그레이드

Passport를 새 주요 버전으로 업그레이드할 경우, [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼히 검토하는 것이 중요합니다.

<a name="configuration"></a>
## 설정

<a name="client-secret-hashing"></a>
### 클라이언트 비밀값 해싱

클라이언트 비밀값을 데이터베이스에 해시된 상태로 저장하려면 `App\Providers\AuthServiceProvider` 클래스 `boot` 메서드에서 `Passport::hashClientSecrets`를 호출하세요:

```php
use Laravel\Passport\Passport;

Passport::hashClientSecrets();
```

활성화 후에는 클라이언트 비밀값이 생성 직후에만 사용자에게 노출됩니다. 원본 평문 비밀값은 데이터베이스에 저장되지 않아 분실 시 복구가 불가능합니다.

<a name="token-lifetimes"></a>
### 토큰 수명 설정

기본적으로 Passport는 1년 후 만료되는 장기 액세스 토큰을 발급합니다. 수명을 더 길게 또는 짧게 설정하려면 `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용합니다. 이 메서드들은 보통 `App\Providers\AuthServiceProvider` 클래스 `boot` 메서드에서 호출합니다:

```php
/**
 * 인증 / 인가 서비스 등록.
 */
public function boot(): void
{
    Passport::tokensExpireIn(now()->addDays(15));
    Passport::refreshTokensExpireIn(now()->addDays(30));
    Passport::personalAccessTokensExpireIn(now()->addMonths(6));
}
```

> [!WARNING]  
> Passport 데이터베이스 테이블의 `expires_at` 칼럼은 읽기 전용이며 단지 표시 목적입니다. 토큰 발급 시 유효 기간 정보는 서명되고 암호화된 토큰 내부에 저장됩니다. 토큰을 무효화하려면 반드시 [토큰 폐기](#revoking-tokens)를 수행하세요.

<a name="overriding-default-models"></a>
### 기본 모델 재정의하기

Passport에서 내부적으로 사용하는 모델을 자유롭게 확장할 수 있습니다. 커스텀 모델을 정의하고 해당 Passport 모델을 상속하면 됩니다:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

커스텀 모델을 정의한 이후에는 `Laravel\Passport\Passport` 클래스를 통해 Passport가 해당 모델을 사용하도록 알려야 합니다. 보통 애플리케이션 `App\Providers\AuthServiceProvider` 클래스 `boot` 메서드에서 설정합니다:

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\PersonalAccessClient;
use App\Models\Passport\RefreshToken;
use App\Models\Passport\Token;

/**
 * 인증 / 인가 서비스 등록.
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
### 라우트 재정의하기

Passport가 정의한 라우트를 커스터마이징하고 싶다면, 먼저 애플리케이션의 `AppServiceProvider` 클래스 `register` 메서드에서 `Passport::ignoreRoutes`를 호출해 Passport가 라우트를 등록하지 않도록 해야 합니다:

```php
use Laravel\Passport\Passport;

/**
 * 애플리케이션 서비스 등록.
 */
public function register(): void
{
    Passport::ignoreRoutes();
}
```

그 후 [Passport의 라우트 파일](https://github.com/laravel/passport/blob/11.x/routes/web.php)에 정의된 라우트를 복사해 애플리케이션 `routes/web.php` 파일에 붙여넣고 원하는 대로 수정할 수 있습니다:

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

OAuth2 권한 부여 코드를 사용하는 방식은 대부분의 개발자가 OAuth2를 익히는 데 친숙한 방법입니다. 권한 부여 코드를 사용할 때 클라이언트 애플리케이션은 사용자를 서버의 인증 페이지로 리다이렉트하고, 사용자는 해당 클라이언트에 액세스 토큰 발급을 승인하거나 거부합니다.

<a name="managing-clients"></a>
### 클라이언트 관리

API와 상호작용하려면 개발자는 "클라이언트"를 등록해야 합니다. 일반적으로 클라이언트 이름과 사용자가 권한 부여 요청을 승인한 후 리다이렉트할 URL을 지정합니다.

<a name="the-passportclient-command"></a>
#### `passport:client` 명령

클라이언트를 생성하는 가장 간단한 방법은 `passport:client` Artisan 명령을 사용하는 것입니다. 이 명령어는 OAuth2 기능을 테스트하기 위한 클라이언트를 만들 수 있습니다. 명령 실행 시 Passport는 클라이언트 정보를 물어보고 클라이언트 ID와 비밀값을 제공합니다:

```shell
php artisan passport:client
```

**리다이렉트 URL**

여러 개의 리다이렉트 URL을 허용하려면, `passport:client` 명령 실행 중 URL 입력 시 쉼표로 구분해 나열할 수 있습니다. 쉼표가 포함된 URL은 URL 인코딩해야 합니다:

```shell
http://example.com/callback,http://examplefoo.com/callback
```

<a name="clients-json-api"></a>
#### JSON API

사용자가 `client` 명령을 직접 이용할 수 없으므로, Passport는 클라이언트 생성, 수정, 삭제용 JSON API를 제공합니다. 이 API와 사용자용 대시보드를 결합해 클라이언트를 관리할 수 있습니다.

API는 `web`과 `auth` 미들웨어로 보호되므로 외부에서 호출할 수 없고 애플리케이션 내부에서만 호출 가능합니다.

<a name="get-oauthclients"></a>
#### `GET /oauth/clients`

인증된 사용자의 모든 클라이언트를 반환합니다. 클라이언트 목록을 보여주고 편집, 삭제 시 유용합니다:

```js
axios.get('/oauth/clients')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthclients"></a>
#### `POST /oauth/clients`

새 클라이언트를 생성할 때 사용합니다. 클라이언트의 `name`과 사용자 승인 후 리다이렉트할 `redirect` URL이 필요합니다. 성공하면 새 클라이언트 인스턴스를 반환합니다:

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
        // 오류 처리...
    });
```

<a name="put-oauthclientsclient-id"></a>
#### `PUT /oauth/clients/{client-id}`

기존 클라이언트를 업데이트합니다. `name`과 `redirect` URL을 요구하며 업데이트된 클라이언트를 반환합니다:

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
        // 오류 처리...
    });
```

<a name="delete-oauthclientsclient-id"></a>
#### `DELETE /oauth/clients/{client-id}`

클라이언트를 삭제합니다:

```js
axios.delete('/oauth/clients/' + clientId)
    .then(response => {
        // 삭제 완료 후 처리...
    });
```

<a name="requesting-tokens"></a>
### 토큰 요청하기

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 권한 부여를 위한 리다이렉트

클라이언트 생성 후, 앱 개발자는 클라이언트 ID와 비밀값을 사용해 권한 부여 코드와 액세스 토큰을 요청합니다. 먼저 클라이언트는 애플리케이션의 `/oauth/authorize` 라우트로 리다이렉션 요청을 보냅니다:

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

`prompt` 파라미터는 Passport 애플리케이션의 인증 동작을 제어합니다.

- `none`: 사용자가 인증되지 않은 경우 인증 오류 발생  
- `consent`: 모든 권한 부여 화면을 항상 표시  
- `login`: 사용자가 로그인 세션이 있어도 재로그인 요구

`prompt`가 없으면 요청된 스코프로 이전에 승인되지 않은 경우에만 권한 부여 화면을 표시합니다.

> [!NOTE]  
> `/oauth/authorize` 라우트는 Passport가 이미 정의하므로 직접 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 승인 처리

권한 부여 요청을 받으면 Passport는 `prompt` 값에 따라 자동으로 응답하거나 사용자에게 승인/거부 화면을 보여줍니다. 승인이 완료되면 정의된 `redirect_uri`(클라이언트 생성 시 지정한 URL)로 리다이렉트됩니다.

권한 부여 승인 화면을 커스터마이징 하려면 `vendor:publish` 명령으로 뷰 파일을 발행할 수 있습니다. 발행된 뷰는 `resources/views/vendor/passport` 디렉토리에 위치합니다:

```shell
php artisan vendor:publish --tag=passport-views
```

일부 경우, 예를 들어 1인칭 클라이언트에서 승인 프롬프트를 생략하려면 [클라이언트 모델 확장](#overriding-default-models)과 `skipsAuthorization` 메서드를 구현하세요. 해당 메서드가 `true`를 반환하면 바로 승인된 것으로 간주됩니다 (단, 리다이렉트 시 클라이언트가 직접 `prompt`를 지정했을 경우는 제외):

```php
<?php

namespace App\Models\Passport;

use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 클라이언트 승인 프롬프트 생략 여부 결정.
     */
    public function skipsAuthorization(): bool
    {
        return $this->firstParty();
    }
}
```

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
#### 권한 코드 -> 액세스 토큰 변환

사용자가 승인하면 클라이언트 애플리케이션으로 리다이렉트됩니다. 클라이언트는 세션에 저장된 `state` 값과 리다이렉트된 `state` 파라미터를 비교해 검증합니다. 일치하면 애플리케이션에 `POST` 요청을 보내 액세스 토큰을 요청합니다. 요청에는 권한 부여 코드와 클라이언트 ID, 비밀값, 리다이렉트 URL 등이 포함되어야 합니다:

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

`/oauth/token` 라우트는 JSON 형식으로 `access_token`, `refresh_token`, `expires_in` 항목을 반환합니다. `expires_in`은 토큰 만료까지 남은 시간을 초 단위로 나타냅니다.

> [!NOTE]  
> `/oauth/token` 라우트도 Passport가 미리 정의하므로 직접 정의할 필요 없습니다.

<a name="tokens-json-api"></a>
#### 토큰 JSON API

Passport는 인증된 사용자의 액세스 토큰을 관리하기 위한 JSON API도 제공합니다. 이를 이용해 사용자가 대시보드에서 토큰을 관리할 수 있도록 프론트엔드와 연동할 수 있습니다. JSON API는 `web`과 `auth` 미들웨어로 보호되어 외부 호출이 불가능합니다.

<a name="get-oauthtokens"></a>
#### `GET /oauth/tokens`

사용자의 모든 인증된 액세스 토큰을 반환합니다. 토큰 목록 확인 및 폐기할 때 유용합니다:

```js
axios.get('/oauth/tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="delete-oauthtokenstoken-id"></a>
#### `DELETE /oauth/tokens/{token-id}`

액세스 토큰 및 관련된 리프레시 토큰을 폐기합니다:

```js
axios.delete('/oauth/tokens/' + tokenId);
```

<a name="refreshing-tokens"></a>
### 토큰 갱신하기

단기 만료 토큰을 사용하는 경우, 사용자가 발급받은 리프레시 토큰을 사용해 액세스 토큰을 갱신할 수 있습니다:

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

`/oauth/token` 라우트는 JSON 형식으로 갱신된 `access_token`, `refresh_token`, `expires_in`을 반환합니다.

<a name="revoking-tokens"></a>
### 토큰 폐기하기

`Laravel\Passport\TokenRepository` 클래스의 `revokeAccessToken` 메서드를 사용해 액세스 토큰을 폐기할 수 있습니다. 관련 리프레시 토큰들은 `Laravel\Passport\RefreshTokenRepository`의 `revokeRefreshTokensByAccessTokenId` 메서드를 사용해 폐기합니다. 두 클래스는 Laravel의 [서비스 컨테이너](/docs/10.x/container)를 통해 주입받을 수 있습니다:

```php
use Laravel\Passport\TokenRepository;
use Laravel\Passport\RefreshTokenRepository;

$tokenRepository = app(TokenRepository::class);
$refreshTokenRepository = app(RefreshTokenRepository::class);

// 액세스 토큰 폐기...
$tokenRepository->revokeAccessToken($tokenId);

// 해당 액세스 토큰의 모든 리프레시 토큰 폐기...
$refreshTokenRepository->revokeRefreshTokensByAccessTokenId($tokenId);
```

<a name="purging-tokens"></a>
### 토큰 정리하기

폐기되거나 만료된 토큰 및 권한 코드를 데이터베이스에서 정리하려면 `passport:purge` Artisan 명령을 사용하세요:

```shell
# 폐기되고 만료된 토큰 및 권한 코드 정리
php artisan passport:purge

# 6시간 이상 만료된 경우에만 정리
php artisan passport:purge --hours=6

# 폐기된 토큰 및 권한 코드만 정리
php artisan passport:purge --revoked

# 만료된 토큰 및 권한 코드만 정리
php artisan passport:purge --expired
```

자동 정리를 위해, 애플리케이션 `App\Console\Kernel` 클래스에서 [스케줄 작업](/docs/10.x/scheduling)으로 등록할 수 있습니다:

```php
/**
 * 애플리케이션 명령 스케줄 정의.
 */
protected function schedule(Schedule $schedule): void
{
    $schedule->command('passport:purge')->hourly();
}
```

<a name="code-grant-pkce"></a>
## PKCE가 적용된 Authorization Code Grant

PKCE(Proof Key for Code Exchange)가 적용된 Authorization Code grant는 클라이언트 비밀값 보관이 불가능한 SPA 또는 네이티브 앱이 API에 안전하게 접근하도록 돕는 방식입니다. 권한 부여 코드를 액세스 토큰으로 교환할 때 클라이언트 비밀값 대신 "코드 검증기(code verifier)"와 "코드 챌린지(code challenge)" 조합을 사용합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성하기

PKCE 구현 클라이언트를 생성하려면 `passport:client` Artisan 명령을 `--public` 옵션과 함께 실행하세요:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청하기

<a name="code-verifier-code-challenge"></a>
#### 코드 검증기와 코드 챌린지

클라이언트 비밀값 없이 토큰을 요청하려면, 개발자는 43~128자 범위의 임의 문자열 `code_verifier`를 생성해야 합니다. 이 문자열은 영문자, 숫자, `- . _ ~` 문자 조합으로 구성되어야 하며 [RFC 7636 규격](https://tools.ietf.org/html/rfc7636)을 따릅니다.

`code_challenge`는 `code_verifier`를 SHA256 해시 후 Base64 URL-safe 인코딩한 문자열입니다. 아래와 같이 생성할 수 있습니다:

```
$encoded = base64_encode(hash('sha256', $code_verifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 권한 부여 리다이렉트

클라이언트 ID, 코드 검증기 및 코드 챌린지를 사용해 권한 부여 코드를 요청하려면 `/oauth/authorize` 라우트로 리다이렉트합니다:

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
#### 권한 코드 -> 액세스 토큰 변환

사용자가 승인하면 클라이언트 애플리케이션으로 리다이렉트됩니다. `state` 값을 검증한 후, 생성해둔 `code_verifier` 값을 포함하여 액세스 토큰을 요청합니다:

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
## Password Grant 토큰

> [!WARNING]  
> Password grant 토큰 사용은 더 이상 권장되지 않습니다. 대신 OAuth2 Server에서 현재 권장하는 [다른 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

OAuth2 Password Grant는 모바일 애플리케이션 같은 1인칭 클라이언트가 이메일/사용자명과 패스워드로 손쉽게 액세스 토큰을 발급 받도록 도와줍니다. 전체 권한 부여 코드 리다이렉트 과정을 거치지 않아도 되어 편리합니다.

<a name="creating-a-password-grant-client"></a>
### Password Grant 클라이언트 생성

Password Grant 토큰을 발급하려면 먼저 Password Grant 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령에 `--password` 옵션을 사용하세요. 이미 `passport:install` 실행 시 생성되었다면 이 단계는 생략해도 됩니다:

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청

Password Grant 클라이언트 생성 후, 사용자 이메일과 패스워드를 포함해 `/oauth/token` 경로에 `POST` 요청을 보내 액세스 토큰을 발급받습니다. 이 라우트는 Passport가 기본 제공하므로 직접 만들 필요 없습니다. 성공 시 JSON 응답에 `access_token`, `refresh_token`이 포함됩니다:

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
> 액세스 토큰 기본 수명은 길지만 [설정 변경도 자유롭게 가능](#configuration)합니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청

Password Grant나 Client Credentials Grant를 이용할 땐 애플리케이션에서 지원하는 모든 스코프를 허가하도록 `*` 스코프를 요청할 수 있습니다. 이 경우 토큰 인스턴스의 `can` 메서드는 항상 `true`를 반환합니다. 단, 이 스코프는 반드시 `password` 또는 `client_credentials` 그랜트에서 발급된 토큰에만 할당할 수 있습니다:

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

애플리케이션에 여러 인증 사용자 프로바이더가 있을 때는 `artisan passport:client --password` 명령에 `--provider` 옵션으로 Password Grant 클라이언트가 사용할 프로바이더를 지정할 수 있습니다. 지정한 프로바이더 이름은 `config/auth.php` 설정 내 유효한 프로바이더명과 일치해야 합니다. 이후 [미들웨어로 라우트를 보호](#via-middleware)해 지정 프로바이더 사용자를 인증할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명 필드 커스터마이징

Password Grant 인증 시, Passport는 기본적으로 인증 가능한 모델의 `email` 속성을 "사용자명"으로 사용합니다. 다르게 하려면 모델에 `findForPassport` 메서드를 정의하세요:

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
     * 주어진 사용자명으로 사용자 인스턴스 탐색.
     */
    public function findForPassport(string $username): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### 비밀번호 검증 커스터마이징

Password Grant를 사용할 때 Passport는 모델의 `password` 속성으로 비밀번호를 검증합니다. 만약 `password` 속성이 없거나 검증 로직을 바꾸고 싶다면 모델에 `validateForPassportPasswordGrant` 메서드를 정의하세요:

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
     * Passport Password Grant용 사용자 비밀번호 검증.
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant-tokens"></a>
## Implicit Grant 토큰

> [!WARNING]  
> Implicit grant 토큰 사용은 더 이상 권장되지 않습니다. 대신 OAuth2 Server가 현재 권장하는 [다른 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

Implicit grant는 Authorization Code grant와 비슷하지만, 권한 코드 없이 직접 토큰이 클라이언트에 반환됩니다. 보통 클라이언트 자격증명을 안전하게 저장할 수 없는 JavaScript 또는 모바일 앱에서 사용됩니다. 사용하려면 애플리케이션 `App\Providers\AuthServiceProvider` 클래스 `boot` 메서드에서 `enableImplicitGrant` 메서드를 호출하세요:

```php
/**
 * 인증 / 인가 서비스 등록.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

활성화 후에는 클라이언트 ID로 `/oauth/authorize` 라우트에 리다이렉트 요청을 보낼 수 있습니다:

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
> `/oauth/authorize` 라우트는 Passport가 이미 정의하므로 직접 만들 필요 없습니다.

<a name="client-credentials-grant-tokens"></a>
## Client Credentials Grant 토큰

Client Credentials grant는 머신 간 인증에 적합합니다. 예를 들어 스케줄 작업에서 API를 이용해 유지보수 작업을 할 때 사용합니다.

먼저, `passport:client` Artisan 명령을 `--client` 옵션과 함께 실행해 클라이언트를 생성하세요:

```shell
php artisan passport:client --client
```

이 그랜트를 사용하려면 `app/Http/Kernel.php` 파일 `$middlewareAliases` 속성에 `CheckClientCredentials` 미들웨어를 추가하세요:

```php
use Laravel\Passport\Http\Middleware\CheckClientCredentials;

protected $middlewareAliases = [
    'client' => CheckClientCredentials::class,
];
```

이후 라우트에 미들웨어를 붙여 접근을 제한할 수 있습니다:

```php
Route::get('/orders', function (Request $request) {
    // ...
})->middleware('client');
```

필요할 때는 미들웨어에 쉼표로 구분한 스코프 목록을 넘겨 특정 스코프가 있어야만 접근 허용하도록 할 수 있습니다:

```php
Route::get('/orders', function (Request $request) {
    // ...
})->middleware('client:check-status,your-scope');
```

<a name="retrieving-tokens"></a>
### 토큰 받기

이 그랜트를 이용해 토큰을 받으려면 `oauth/token` 엔드포인트에 다음과 같이 요청하세요:

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

사용자가 전형적인 권한 부여 코드 리다이렉트 과정을 거치지 않고 본인에게 직접 액세스 토큰을 발급하도록 할 수도 있습니다. 사용자 UI에서 직접 토큰 생성 기능을 제공하는 것이 유용할 수 있으며, API 체험이나 간단한 토큰 발급 용도로도 적합합니다.

> [!NOTE]  
> 애플리케이션에서 주로 개인 액세스 토큰을 사용하려면 Laravel의 경량 API 토큰 라이브러리인 [Laravel Sanctum](/docs/10.x/sanctum) 사용을 고려하세요.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성

개인 액세스 토큰 발급을 위해 개인 액세스 클라이언트를 생성해야 합니다. `passport:client` 명령에 `--personal` 옵션을 붙여 실행하세요. 이미 `passport:install` 실행 시 생성된 경우는 생략 가능:

```shell
php artisan passport:client --personal
```

클라이언트 ID와 평문 비밀값을 `.env` 파일에 작성해둡니다:

```ini
PASSPORT_PERSONAL_ACCESS_CLIENT_ID="client-id-value"
PASSPORT_PERSONAL_ACCESS_CLIENT_SECRET="unhashed-client-secret-value"
```

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리

개인 액세스 클라이언트 생성 후, `App\Models\User` 인스턴스의 `createToken` 메서드를 사용해 토큰을 발급할 수 있습니다. 첫 번째 인자는 토큰 이름, 두 번째 인자는 선택적 스코프 배열입니다:

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

Passport는 개인 액세스 토큰 관리용 JSON API도 포함합니다. 프론트엔드 대시보드와 연동해 사용자가 직접 토큰을 관리할 수 있습니다. JSON API는 `web`과 `auth` 미들웨어가 적용되어 외부에서 호출할 수 없습니다.

<a name="get-oauthscopes"></a>
#### `GET /oauth/scopes`

애플리케이션 정의된 모든 스코프 목록을 반환합니다. 사용자가 개인 액세스 토큰에 할당할 수 있는 스코프를 보여줄 때 사용합니다:

```js
axios.get('/oauth/scopes')
    .then(response => {
        console.log(response.data);
    });
```

<a name="get-oauthpersonal-access-tokens"></a>
#### `GET /oauth/personal-access-tokens`

인증된 사용자가 생성한 모든 개인 액세스 토큰을 반환합니다. 토큰 목록 확인, 수정, 폐기 시 유용합니다:

```js
axios.get('/oauth/personal-access-tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthpersonal-access-tokens"></a>
#### `POST /oauth/personal-access-tokens`

새 개인 액세스 토큰을 생성합니다. 토큰의 `name`과 할당할 `scopes` 배열을 포함해야 합니다:

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
        // 오류 처리...
    });
```

<a name="delete-oauthpersonal-access-tokenstoken-id"></a>
#### `DELETE /oauth/personal-access-tokens/{token-id}`

개인 액세스 토큰을 폐기합니다:

```js
axios.delete('/oauth/personal-access-tokens/' + tokenId);
```

<a name="protecting-routes"></a>
## 라우트 보호하기

<a name="via-middleware"></a>
### 미들웨어 사용

Passport는 들어오는 요청의 액세스 토큰을 검증하는 [인증 가드](/docs/10.x/authentication#adding-custom-guards)를 제공합니다. `api` 가드가 `passport` 드라이버를 사용하도록 설정됐으면, 액세스 토큰이 필요한 라우트에 `auth:api` 미들웨어만 붙이면 됩니다:

```php
Route::get('/user', function () {
    // ...
})->middleware('auth:api');
```

> [!WARNING]  
> 만약 [클라이언트 자격증명 그랜트](#client-credentials-grant-tokens)를 사용한다면, `auth:api` 대신 [client 미들웨어](#client-credentials-grant-tokens)를 사용해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 다중 인증 가드

애플리케이션에 서로 다른 Eloquent 모델을 사용하는 여러 유형의 사용자 인증이 필요하면, 각 사용자 프로바이더별로 가드를 정의해야 합니다. 예를 들어 `config/auth.php` 설정에서 다음과 같이 여러 가드를 정의할 수 있습니다:

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

아래 라우트는 `customers` 사용자 프로바이더를 사용하는 `api-customers` 가드로 인증합니다:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]  
> Passport에서 다중 사용자 프로바이더를 사용하는 자세한 내용은 [password grant 설명](#customizing-the-user-provider)을 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달

Passport가 보호하는 라우트를 호출할 때, API 클라이언트는 HTTP 요청 헤더 `Authorization`에 `Bearer` 토큰으로 액세스 토큰을 포함해야 합니다. 예를 들어 Guzzle HTTP 라이브러리 사용 시:

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

스코프는 API 클라이언트가 계정 접근 시 특정 권한만 요청하도록 제한하는 권한 세분화 기능입니다. 예를 들어 이커머스 앱에서는 전체 주문 권한 대신 주문 배송 상태 확인 권한만 줄 수도 있습니다. 다시 말해, 스코프는 사용자가 타사 애플리케이션이 자신의 대리로 수행할 수 있는 행위를 제한하도록 돕습니다.

<a name="defining-scopes"></a>
### 스코프 정의하기

애플리케이션의 API 스코프는 `App\Providers\AuthServiceProvider` 클래스 `boot` 메서드에서 `Passport::tokensCan` 메서드를 사용해 정의합니다. `tokensCan` 메서드는 스코프 이름과 설명의 배열을 받으며, 설명은 권한 승인 화면에 표시됩니다:

```php
/**
 * 인증 / 인가 서비스 등록.
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

클라이언트가 특정 스코프를 요청하지 않으면, `setDefaultScope` 메서드를 사용해 Passport 서버가 토큰에 붙일 기본 스코프를 설정할 수 있습니다. 보통 `App\Providers\AuthServiceProvider` 클래스 `boot` 메서드에서 호출합니다:

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
> 기본 스코프 설정은 사용자가 생성하는 개인 액세스 토큰에는 적용되지 않습니다.

<a name="assigning-scopes-to-tokens"></a>
### 토큰에 스코프 할당하기

<a name="when-requesting-authorization-codes"></a>
#### 권한 코드 요청 시

Authorization Code Grant 방식으로 액세스 토큰 요청 시, 클라이언트는 쿼리 스트링 `scope` 파라미터에 요청할 스코프를 공백으로 구분해 전달해야 합니다:

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

`App\Models\User` 모델의 `createToken` 메서드로 개인 액세스 토큰을 생성할 때, 두 번째 인자로 스코프 배열을 전달할 수 있습니다:

```php
$token = $user->createToken('My Token', ['place-orders'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 확인하기

Passport는 특정 스코프가 부여된 토큰인지 검증할 수 있는 두 가지 미들웨어를 제공합니다. 이들을 사용하려면 `app/Http/Kernel.php` 파일 `$middlewareAliases` 배열에 추가하세요:

```php
'scopes' => \Laravel\Passport\Http\Middleware\CheckScopes::class,
'scope' => \Laravel\Passport\Http\Middleware\CheckForAnyScope::class,
```

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인

`scopes` 미들웨어는 요청 토큰이 지정한 모든 스코프를 가지고 있는지 확인합니다:

```php
Route::get('/orders', function () {
    // "check-status"와 "place-orders" 스코프 모두 보유 확인
})->middleware(['auth:api', 'scopes:check-status,place-orders']);
```

<a name="check-for-any-scopes"></a>
#### 일부 스코프 확인

`scope` 미들웨어는 요청 토큰이 지정한 스코프 중 적어도 하나 이상을 가지고 있는지 확인합니다:

```php
Route::get('/orders', function () {
    // "check-status" 또는 "place-orders" 스코프 중 하나 이상 보유 확인
})->middleware(['auth:api', 'scope:check-status,place-orders']);
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인

인증된 요청이 애플리케이션에 들어온 후, `App\Models\User` 인스턴스의 `tokenCan` 메서드로 스코프를 확인할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('place-orders')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
#### 추가 스코프 관련 메서드

- `scopeIds()` 메서드는 정의된 모든 스코프 ID(이름)를 배열로 반환합니다:

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

- `scopes()` 메서드는 정의한 모든 스코프를 `Laravel\Passport\Scope` 인스턴스 배열로 반환합니다:

```php
Passport::scopes();
```

- `scopesFor(array $ids)` 메서드는 주어진 ID/이름과 일치하는 `Scope` 인스턴스 배열을 반환합니다:

```php
Passport::scopesFor(['place-orders', 'check-status']);
```

- `hasScope(string $id)` 메서드는 특정 스코프가 정의되어 있는지 여부를 반환합니다:

```php
Passport::hasScope('place-orders');
```

<a name="consuming-your-api-with-javascript"></a>
## JavaScript로 API 사용하기

API를 개발할 때, JavaScript 애플리케이션에서 동일한 API를 호출해 활용한다면 매우 유용합니다. 웹 애플리케이션, 모바일 앱, 서드파티 앱, 각종 SDK 등에서도 동일한 API를 사용할 수 있게 됩니다.

일반적으로 JavaScript 앱에 액세스 토큰을 전달하고 각각의 요청마다 토큰을 포함해야 합니다. Passport는 이를 자동화하는 미들웨어 `CreateFreshApiToken`을 제공합니다. `app/Http/Kernel.php` 파일의 `web` 미들웨어 그룹에 이 미들웨어를 추가하기만 하면 됩니다:

```php
'web' => [
    // 기존 미들웨어들...
    \Laravel\Passport\Http\Middleware\CreateFreshApiToken::class,
],
```

> [!WARNING]  
> `CreateFreshApiToken` 미들웨어는 미들웨어 스택에서 마지막에 위치하도록 하세요.

이 미들웨어는 응답에 `laravel_token` 쿠키를 추가합니다. 쿠키에는 암호화된 JWT가 들어있으며, Passport가 자바스크립트에서 API 요청 시 인증에 사용합니다. JWT는 Laravel 세션 `session.lifetime` 값과 동일한 수명을 갖습니다. 브라우저가 이 쿠키를 자동으로 전송하므로 토큰을 명시적으로 전달하지 않고 API 요청이 가능합니다:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 변경하기

필요에 따라 `Passport::cookie` 메서드로 `laravel_token` 쿠키 이름을 변경할 수 있습니다. 보통 `App\Providers\AuthServiceProvider` 클래스 `boot` 메서드에서 호출합니다:

```php
/**
 * 인증 / 인가 서비스 등록.
 */
public function boot(): void
{
    Passport::cookie('custom_name');
}
```

<a name="csrf-protection"></a>
#### CSRF 보호

이 인증 방법을 사용할 때, 요청에 올바른 CSRF 토큰 헤더가 포함돼야 합니다. Laravel 기본 자바스크립트 스캐폴딩은 Axios 인스턴스를 포함하며, 자동으로 암호화된 `XSRF-TOKEN` 쿠키 값을 사용해 동일 출처 요청에 `X-XSRF-TOKEN` 헤더를 추가합니다.

> [!NOTE]  
> 만약 `X-CSRF-TOKEN` 헤더를 보낼 경우에는 `csrf_token()`이 제공하는 비암호화 토큰 값을 사용해야 합니다.

<a name="events"></a>
## 이벤트

Passport는 액세스 토큰과 리프레시 토큰 발급 시 이벤트를 발생시킵니다. 이를 활용해 DB 내 오래된 토큰을 정리하거나 폐기하는 작업을 수행할 수 있습니다. `App\Providers\EventServiceProvider` 클래스에서 이벤트 리스너를 등록할 수 있습니다:

```php
/**
 * 애플리케이션 이벤트-리스너 매핑.
 *
 * @var array
 */
protected $listen = [
    'Laravel\Passport\Events\AccessTokenCreated' => [
        'App\Listeners\RevokeOldTokens',
    ],

    'Laravel\Passport\Events\RefreshTokenCreated' => [
        'App\Listeners\PruneOldTokens',
    ],
];
```

<a name="testing"></a>
## 테스트

Passport의 `actingAs` 메서드를 사용하면 현재 인증 사용자와 부여할 스코프를 지정할 수 있습니다. 첫 번째 인자는 사용자 인스턴스, 두 번째 인자는 토큰에 허용할 스코프 배열입니다:

```php
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

`actingAsClient` 메서드는 현재 인증된 클라이언트와 부여할 스코프 배열을 지정할 때 사용합니다:

```php
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