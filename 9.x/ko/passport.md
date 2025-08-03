# Laravel Passport

- [소개](#introduction)
    - [Passport 아니면 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [마이그레이션 커스터마이징](#migration-customization)
    - [Passport 업그레이드](#upgrading-passport)
- [설정](#configuration)
    - [클라이언트 비밀 해싱(Client Secret Hashing)](#client-secret-hashing)
    - [토큰 수명(Token Lifetimes)](#token-lifetimes)
    - [기본 모델 덮어쓰기(Overriding Default Models)](#overriding-default-models)
    - [라우트 덮어쓰기(Overriding Routes)](#overriding-routes)
- [액세스 토큰 발급](#issuing-access-tokens)
    - [클라이언트 관리하기](#managing-clients)
    - [토큰 요청하기](#requesting-tokens)
    - [토큰 갱신하기](#refreshing-tokens)
    - [토큰 취소하기](#revoking-tokens)
    - [토큰 정리하기](#purging-tokens)
- [PKCE를 사용하는 인증 코드 그랜트(Authorization Code Grant with PKCE)](#code-grant-pkce)
    - [클라이언트 생성하기](#creating-a-auth-pkce-grant-client)
    - [토큰 요청하기](#requesting-auth-pkce-grant-tokens)
- [비밀번호 그랜트 토큰(Password Grant Tokens)](#password-grant-tokens)
    - [비밀번호 그랜트 클라이언트 생성하기](#creating-a-password-grant-client)
    - [토큰 요청하기](#requesting-password-grant-tokens)
    - [모든 스코프 요청하기](#requesting-all-scopes)
    - [사용자 프로바이더 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 로직 커스터마이징](#customizing-the-password-validation)
- [암시적 그랜트 토큰(Implicit Grant Tokens)](#implicit-grant-tokens)
- [클라이언트 자격 증명 그랜트 토큰(Client Credentials Grant Tokens)](#client-credentials-grant-tokens)
- [개인 액세스 토큰(Personal Access Tokens)](#personal-access-tokens)
    - [개인 액세스 클라이언트 생성하기](#creating-a-personal-access-client)
    - [개인 액세스 토큰 관리하기](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어를 통한 보호](#via-middleware)
    - [액세스 토큰 전달하기](#passing-the-access-token)
- [토큰 스코프(Token Scopes)](#token-scopes)
    - [스코프 정의하기](#defining-scopes)
    - [기본 스코프 설정하기](#default-scope)
    - [토큰에 스코프 할당하기](#assigning-scopes-to-tokens)
    - [스코프 체크하기](#checking-scopes)
- [JavaScript로 API 사용하기](#consuming-your-api-with-javascript)
- [이벤트(Events)](#events)
- [테스트(Test)](#testing)

<a name="introduction"></a>
## 소개

[Laravel Passport](https://github.com/laravel/passport)는 Laravel 애플리케이션에 대해 몇 분 만에 완전한 OAuth2 서버 구현을 제공합니다. Passport는 Andy Millington과 Simon Hamp가 유지 관리하는 [League OAuth2 서버](https://github.com/thephpleague/oauth2-server)를 기반으로 구축되어 있습니다.

> [!WARNING]
> 이 문서는 OAuth2에 대해 이미 알고 있다고 가정합니다. OAuth2에 대해 모른다면, 계속 진행하기 전에 일반적인 [용어](https://oauth2.thephpleague.com/terminology/)와 OAuth2 기능을 익히는 것을 권장합니다.

<a name="passport-or-sanctum"></a>
### Passport 아니면 Sanctum?

시작하기 전에, 자신의 애플리케이션에 Laravel Passport를 사용할지 아니면 [Laravel Sanctum](/docs/9.x/sanctum)을 사용할지 결정해야 할 수 있습니다. 애플리케이션이 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용해야 합니다.

그러나 싱글 페이지 애플리케이션, 모바일 애플리케이션을 인증하거나 API 토큰을 발급하려는 경우에는 [Laravel Sanctum](/docs/9.x/sanctum)을 사용하는 편이 좋습니다. Laravel Sanctum은 OAuth2를 지원하지 않지만 훨씬 간단한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치

시작하려면 Composer 패키지 매니저를 통해 Passport를 설치하세요:

```shell
composer require laravel/passport
```

Passport의 [서비스 프로바이더](/docs/9.x/providers)는 자체 데이터베이스 마이그레이션 디렉토리를 등록하므로, 패키지를 설치한 후 데이터베이스 마이그레이션을 수행해야 합니다. Passport 마이그레이션은 애플리케이션이 OAuth2 클라이언트 및 액세스 토큰을 저장하는 데 필요한 테이블을 생성합니다:

```shell
php artisan migrate
```

다음으로 `passport:install` Artisan 명령어를 실행하세요. 이 명령어는 안전한 액세스 토큰 생성에 필요한 암호화 키를 생성합니다. 또한 "personal access"와 "password grant" 클라이언트를 생성해, 액세스 토큰을 발급하는 데 사용합니다:

```shell
php artisan passport:install
```

> [!NOTE]
> Passport의 `Client` 모델의 기본 키를 자동 증가 정수 대신 UUID로 사용하고 싶다면, [uuids 옵션](#client-uuids)을 사용해 Passport를 설치하세요.

`passport:install` 명령어 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트를 추가하세요. 이 트레이트는 인증된 사용자의 토큰과 스코프를 조회할 수 있는 몇 가지 헬퍼 메서드를 제공합니다. 만약 모델이 이미 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용 중이라면 제거해도 됩니다:

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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고 `driver` 옵션을 `passport`로 설정하세요. 이렇게 하면 들어오는 API 요청을 인증할 때 Passport의 `TokenGuard`를 사용하도록 애플리케이션에 지시하게 됩니다:

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
#### 클라이언트 UUIDs

또한 `passport:install` 명령어에 `--uuids` 옵션을 붙여 실행할 수 있습니다. 이 옵션은 Passport가 `Client` 모델의 기본 키 값으로 자동 증가 정수 대신 UUID를 사용하도록 지시합니다. 이 옵션으로 명령어를 실행하면 Passport 기본 마이그레이션을 비활성화하는 방법에 관한 추가 안내도 받게 됩니다:

```shell
php artisan passport:install --uuids
```

<a name="deploying-passport"></a>
### Passport 배포하기

애플리케이션 서버에 Passport를 처음 배포할 때는 `passport:keys` 명령어를 실행해야 합니다. 이 명령어는 액세스 토큰 생성에 필요한 암호화 키를 생성하며, 생성된 키는 일반적으로 소스 관리에 포함되지 않습니다:

```shell
php artisan passport:keys
```

필요 시, Passport가 키를 로드할 경로를 정의할 수 있습니다. `Passport::loadKeysFrom` 메서드를 사용하며, 일반적으로 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
}
```

<a name="loading-keys-from-the-environment"></a>
#### 환경 변수에서 키 불러오기

또는, `vendor:publish` Artisan 명령어로 Passport의 설정 파일을 공개할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일이 공개되면, 환경 변수에 애플리케이션의 암호화 키를 선언함으로써 불러올 수 있습니다:

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

Passport의 기본 마이그레이션을 사용하지 않으려면, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에 `Passport::ignoreMigrations`를 호출하세요. 기본 마이그레이션을 내보내려면 `vendor:publish` Artisan 명령어를 사용합니다:

```shell
php artisan vendor:publish --tag=passport-migrations
```

<a name="upgrading-passport"></a>
### Passport 업그레이드

Passport의 주 버전을 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 주의 깊게 검토하는 것이 중요합니다.

<a name="configuration"></a>
## 설정

<a name="client-secret-hashing"></a>
### 클라이언트 비밀 해싱(Client Secret Hashing)

클라이언트 비밀 값이 데이터베이스에 저장될 때 해싱되도록 하려면, `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `Passport::hashClientSecrets`를 호출하세요:

```php
use Laravel\Passport\Passport;

Passport::hashClientSecrets();
```

활성화하면, 클라이언트 비밀은 생성 직후 한 번만 사용자에게 표시되고, 데이터베이스에는 평문 값이 저장되지 않아 분실 시 복구할 수 없습니다.

<a name="token-lifetimes"></a>
### 토큰 수명(Token Lifetimes)

기본적으로 Passport는 만료 기간이 1년인 장기간 액세스 토큰을 발급합니다. 더 길거나 짧은 토큰 수명을 설정하고 싶다면 `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이들은 일반적으로 `AuthServiceProvider`의 `boot` 메서드에서 호출됩니다:

```php
/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::tokensExpireIn(now()->addDays(15));
    Passport::refreshTokensExpireIn(now()->addDays(30));
    Passport::personalAccessTokensExpireIn(now()->addMonths(6));
}
```

> [!WARNING]
> Passport 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며 단지 표시 용도입니다. 토큰 발급 시, 만료 정보는 서명되고 암호화된 토큰 내부에 저장됩니다. 토큰을 무효화해야 한다면 [토큰 취소하기](#revoking-tokens)를 사용하세요.

<a name="overriding-default-models"></a>
### 기본 모델 덮어쓰기(Overriding Default Models)

Passport가 내부에서 사용하는 모델을 확장하여 자신만의 모델을 사용할 수 있습니다. 아래 예제처럼 Passport 모델을 상속받아 모델을 정의하세요:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 만든 후에는 `Laravel\Passport\Passport` 클래스를 사용하여 Passport가 사용자 정의 모델을 사용하도록 지정합니다. 보통 이런 작업은 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 수행합니다:

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\PersonalAccessClient;
use App\Models\Passport\RefreshToken;
use App\Models\Passport\Token;

/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::useTokenModel(Token::class);
    Passport::useRefreshTokenModel(RefreshToken::class);
    Passport::useAuthCodeModel(AuthCode::class);
    Passport::useClientModel(Client::class);
    Passport::usePersonalAccessClientModel(PersonalAccessClient::class);
}
```

<a name="overriding-routes"></a>
### 라우트 덮어쓰기(Overriding Routes)

가끔 Passport가 기본으로 제공하는 라우트를 커스터마이징하고 싶을 때가 있습니다. 이를 위해서는 먼저 `AppServiceProvider`의 `register` 메서드에 `Passport::ignoreRoutes`를 추가하여 Passport가 자동으로 등록하는 라우트를 무시하도록 해야 합니다:

```php
use Laravel\Passport\Passport;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    Passport::ignoreRoutes();
}
```

그 다음, Passport가 제공하는 라우트 정의([routes/web.php](https://github.com/laravel/passport/blob/11.x/routes/web.php))를 복사해 자신의 애플리케이션 `routes/web.php` 파일에 붙여넣고 원하는 대로 수정하세요:

```php
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => 'Laravel\Passport\Http\Controllers',
], function () {
    // Passport 라우트들...
});
```

<a name="issuing-access-tokens"></a>
## 액세스 토큰 발급

인증 코드를 이용한 OAuth2 사용법은 대부분의 개발자가 익숙한 방식입니다. 인증 코드 그랜트를 사용할 때 클라이언트 애플리케이션은 사용자를 서버의 인증 승인 페이지로 리디렉션하여 액세스 토큰 발급 허용 여부를 확인합니다.

<a name="managing-clients"></a>
### 클라이언트 관리하기

먼저, API와 상호작용할 다른 클라이언트 애플리케이션을 만드는 개발자는 "클라이언트"를 등록해야 합니다. 일반적으로 클라이언트 이름과 사용자가 승인을 허락한 뒤 리디렉션할 URL을 제공합니다.

<a name="the-passportclient-command"></a>
#### `passport:client` 커맨드

클라이언트를 생성하는 가장 간단한 방법은 `passport:client` Artisan 명령어를 사용하는 것입니다. 이 명령어로 OAuth2 기능 테스트를 위한 클라이언트를 만들 수 있습니다. 실행하면 클라이언트에 관한 추가 정보를 입력받고 클라이언트 ID와 비밀 값을 제공합니다:

```shell
php artisan passport:client
```

**리디렉션 URL**

여러 개의 리디렉션 URL을 허용하려면 `passport:client` 명령어가 URL을 물어볼 때 쉼표로 구분된 리스트를 입력하세요. 쉼표가 포함된 URL은 URL 인코딩된 상태여야 합니다:

```shell
http://example.com/callback,http://examplefoo.com/callback
```

<a name="clients-json-api"></a>
#### JSON API

사용자들이 직접 `client` 명령어를 사용할 수 없기 때문에, Passport는 클라이언트 생성, 수정, 삭제를 위한 JSON API를 제공합니다. 이 API로 사용자용 클라이언트 관리 대시보드를 쉽게 구현할 수 있습니다.

아래는 이 API 엔드포인트들을 다루는 방법을 Axios를 사용해 예시로 보여줍니다.

이 API는 `web`과 `auth` 미들웨어로 보호되기 때문에, 외부에서 호출할 수 없고 애플리케이션 내부에서만 사용할 수 있습니다.

<a name="get-oauthclients"></a>
#### `GET /oauth/clients`

인증된 사용자가 생성한 모든 클라이언트를 반환합니다. 사용자가 자신의 클라이언트를 편집하거나 삭제할 때 주로 사용됩니다:

```js
axios.get('/oauth/clients')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthclients"></a>
#### `POST /oauth/clients`

새 클라이언트를 생성합니다. `name`과 `redirect` URL이 필요하며, 사용자 승인 후 리디렉션할 URL입니다.

클라이언트 생성 시 클라이언트 ID와 비밀 값이 발급되며, 토큰 요청에 사용됩니다. 생성 후 새 클라이언트 정보가 반환됩니다:

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
        // 에러 리스트 출력...
    });
```

<a name="put-oauthclientsclient-id"></a>
#### `PUT /oauth/clients/{client-id}`

기존 클라이언트를 수정합니다. `name`과 `redirect` URL을 받아 업데이트된 클라이언트 정보를 반환합니다:

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
        // 에러 리스트 출력...
    });
```

<a name="delete-oauthclientsclient-id"></a>
#### `DELETE /oauth/clients/{client-id}`

클라이언트를 삭제합니다:

```js
axios.delete('/oauth/clients/' + clientId)
    .then(response => {
        //
    });
```

<a name="requesting-tokens"></a>
### 토큰 요청하기

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인증을 위한 리디렉션

클라이언트가 생성되면 클라이언트 ID와 비밀을 사용해 인증 코드와 액세스 토큰을 요청할 수 있습니다. 먼저 소비 애플리케이션은 `/oauth/authorize` 경로로 리디렉션 요청을 아래처럼 해야 합니다:

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

`prompt` 파라미터는 Passport의 인증 동작을 제어합니다.

- `none`일 때, 사용자가 로그인되어 있지 않으면 항상 인증 에러를 발생시킵니다.
- `consent`일 때, 이전에 승인한 모든 스코프가 있어도 항상 승인 화면을 표시합니다.
- `login`일 때, 기존 세션이 있어도 항상 재로그인을 요구합니다.

`prompt`가 없으면, 사용자가 특정 클라이언트를 승인한 적이 없거나 요청한 스코프가 다를 경우 승인 화면을 표시합니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 Passport가 미리 정의해줘서 직접 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 승인 처리

Passport는 `prompt` 값에 따라 자동으로 반응하며, 필요 시 사용자에게 승인 요청 화면을 보여줍니다. 사용자가 요청을 승인하면 소비 애플리케이션에서 지정한 `redirect_uri`로 리디렉션됩니다. 이 URI는 클라이언트 생성 시 등록한 URL과 일치해야 합니다.

권한 승인 화면을 커스터마이징하려면 `vendor:publish` 명령으로 뷰를 공개하세요. 공개된 뷰는 `resources/views/vendor/passport`에 저장됩니다:

```shell
php artisan vendor:publish --tag=passport-views
```

만약 퍼스트파티 클라이언트처럼 승인 화면을 건너뛰고 싶다면, `Client` 모델을 확장하면서 `skipsAuthorization` 메서드를 정의해 `true`를 반환하도록 하세요. 이 경우 `prompt`가 명시되지 않으면 즉시 승인되어 리디렉션됩니다:

```php
<?php

namespace App\Models\Passport;

use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 클라이언트가 승인 화면을 생략할지 결정합니다.
     *
     * @return bool
     */
    public function skipsAuthorization()
    {
        return $this->firstParty();
    }
}
```

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
#### 인증 코드를 액세스 토큰으로 변환하기

사용자가 요청을 승인하면 소비 애플리케이션으로 리디렉션됩니다. 이때 저장했던 `state` 값과 전달받은 `state` 파라미터를 비교하여 검증합니다. 일치하면 다음과 같이 `POST` 요청을 보내 액세스 토큰을 요청합니다. 요청에는 승인 시 발급받은 인증 코드도 포함됩니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class
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

이 `/oauth/token` 경로는 `access_token`, `refresh_token`, `expires_in` 등을 포함한 JSON 응답을 반환합니다. `expires_in`은 액세스 토큰 만료까지 남은 시간을 초 단위로 제공합니다.

> [!NOTE]
> `/oauth/token` 경로도 Passport가 기본 제공하므로 직접 정의할 필요가 없습니다.

<a name="tokens-json-api"></a>
#### JSON API

Passport는 승인된 액세스 토큰을 관리하는 JSON API도 제공합니다. 사용자 대시보드를 구현할 때 이 API와 프런트엔드 인터페이스를 연동할 수 있습니다. API는 `web`과 `auth` 미들웨어로 보호되어 외부에서 호출할 수 없습니다.

<a name="get-oauthtokens"></a>
#### `GET /oauth/tokens`

인증된 사용자가 만든 모든 액세스 토큰을 반환합니다. 주로 사용자가 자격을 취소할 토큰을 확인할 때 사용합니다:

```js
axios.get('/oauth/tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="delete-oauthtokenstoken-id"></a>
#### `DELETE /oauth/tokens/{token-id}`

액세스 토큰과 관련된 리프레시 토큰을 취소합니다:

```js
axios.delete('/oauth/tokens/' + tokenId);
```

<a name="refreshing-tokens"></a>
### 토큰 갱신하기

애플리케이션이 단기간 만료되는 액세스 토큰을 발급한다면, 리프레시 토큰을 통해 액세스 토큰을 갱신할 수 있습니다:

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

이 `/oauth/token` 경로는 갱신된 `access_token`, `refresh_token`, `expires_in` 정보를 포함한 JSON 응답을 반환합니다.

<a name="revoking-tokens"></a>
### 토큰 취소하기

`Laravel\Passport\TokenRepository`의 `revokeAccessToken` 메서드를 사용해 액세스 토큰을 취소할 수 있습니다. 또한 `Laravel\Passport\RefreshTokenRepository`의 `revokeRefreshTokensByAccessTokenId` 메서드로 해당 토큰의 모든 리프레시 토큰도 취소할 수 있습니다. 이 클래스들은 Laravel 서비스 컨테이너에서 해석할 수 있습니다:

```php
use Laravel\Passport\TokenRepository;
use Laravel\Passport\RefreshTokenRepository;

$tokenRepository = app(TokenRepository::class);
$refreshTokenRepository = app(RefreshTokenRepository::class);

// 액세스 토큰 취소...
$tokenRepository->revokeAccessToken($tokenId);

// 해당 토큰의 리프레시 토큰 모두 취소...
$refreshTokenRepository->revokeRefreshTokensByAccessTokenId($tokenId);
```

<a name="purging-tokens"></a>
### 토큰 정리하기

만료되거나 취소된 토큰을 데이터베이스에서 정리하고 싶다면 `passport:purge` Artisan 명령어를 사용할 수 있습니다:

```shell
# 취소되고 만료된 토큰과 인증 코드를 정리...
php artisan passport:purge

# 6시간 이상 만료된 토큰만 정리...
php artisan passport:purge --hours=6

# 취소된 토큰과 인증 코드만 정리...
php artisan passport:purge --revoked

# 만료된 토큰과 인증 코드만 정리...
php artisan passport:purge --expired
```

자동화하려면 `App\Console\Kernel` 클래스의 스케줄러 작업에 명령어를 등록하세요:

```php
/**
 * 애플리케이션 명령 스케줄 정의.
 *
 * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
 * @return void
 */
protected function schedule(Schedule $schedule)
{
    $schedule->command('passport:purge')->hourly();
}
```

<a name="code-grant-pkce"></a>
## PKCE를 사용하는 인증 코드 그랜트(Authorization Code Grant with PKCE)

"Proof Key for Code Exchange"(PKCE)를 적용한 인증 코드 그랜트는 클라이언트 비밀(Secret)을 안전하게 저장하기 어려운 싱글 페이지 또는 네이티브 애플리케이션을 위한 보안 방식입니다. 인증 코드를 액세스 토큰으로 교환할 때 클라이언트 비밀 대신 코드 검증자와 코드 챌린지를 이용해 공격자가 인증 코드를 가로채는 위험을 완화합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성하기

먼저, PKCE를 지원하는 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령어에 `--public` 옵션을 붙여 생성합니다:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청하기

<a name="code-verifier-code-challenge"></a>
#### 코드 검증자 및 코드 챌린지

이 그랜트는 클라이언트 비밀이 없으므로, 토큰을 요청하려면 코드 검증자와 코드 챌린지를 생성해야 합니다.

- 코드 검증자는 [RFC 7636](https://tools.ietf.org/html/rfc7636)에 정의된대로 43~128자 길이의 임의 문자열로, 알파벳, 숫자, `"-"`, `"."`, `"_"`, `"~"` 문자를 포함합니다.
- 코드 챌린지는 코드 검증자를 SHA256 해시한 후 Base64 URL-safe 인코딩을 하며, 끝의 `'='` 문자는 제거하고 공백이나 줄바꿈이 없어야 합니다.

```php
$encoded = base64_encode(hash('sha256', $code_verifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 인증을 위한 리디렉션

클라이언트 생성 후, 클라이언트 ID와 코드 검증자 및 코드 챌린지를 사용해 `/oauth/authorize` 경로로 리디렉션 요청을 합니다:

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
#### 인증 코드를 액세스 토큰으로 변환하기

사용자가 승인하면 리디렉션 후 표준 인증 코드 그랜트와 같이 `state`를 검증합니다.

검증 성공 시, 승인 시 발급받은 인증 코드와 세션에 저장했던 `code_verifier`를 포함해 액세스 토큰 요청을 합니다:

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
## 비밀번호 그랜트 토큰(Password Grant Tokens)

> [!WARNING]
> 더 이상 비밀번호 그랜트는 권장하지 않습니다. 대신 [OAuth2 서버에서 현재 권장하는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

OAuth2 비밀번호 그랜트를 사용하면 모바일 애플리케이션과 같은 퍼스트파티 클라이언트가 이메일/사용자명과 비밀번호만으로 액세스 토큰을 받을 수 있습니다. 사용자를 전체 OAuth2 인증 코드 리디렉션 흐름을 거치게 하지 않고 안전하게 토큰을 발급할 수 있게 합니다.

<a name="creating-a-password-grant-client"></a>
### 비밀번호 그랜트 클라이언트 생성하기

비밀번호 그랜트를 사용하려면 해당 클라이언트를 생성해야 합니다. `passport:client` 명령어에 `--password` 옵션을 붙여 생성하며, 만약 이미 `passport:install`을 실행했다면 다시 할 필요 없습니다:

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청하기

비밀번호 그랜트 클라이언트를 생성한 후, 사용자 이메일과 비밀번호를 포함해 `POST` 요청으로 `/oauth/token`에 액세스 토큰을 요청할 수 있습니다. 경로는 Passport가 기본 등록하므로 직접 정의하지 않아도 됩니다:

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
> 기본적으로 액세스 토큰은 장기간 유효하지만, 필요에 따라 최대 수명을 [설정할 수 있습니다](#configuration).

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청하기

비밀번호 그랜트 또는 클라이언트 자격 증명 그랜트를 사용할 때, 애플리케이션이 지원하는 모든 스코프 권한을 부여받는 토큰이 필요하다면 `*` 스코프를 요청하세요. 이 경우 토큰의 `can` 메서드는 항상 `true`를 반환합니다. `*` 스코프는 `password` 또는 `client_credentials` 그랜트로 발급된 토큰에서만 사용할 수 있습니다:

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

애플리케이션에서 여러 [인증 사용자 프로바이더](/docs/9.x/authentication#introduction)를 사용할 경우, `passport:client --password` 커맨드 실행 시 `--provider` 옵션을 지정해 비밀번호 그랜트 클라이언트에서 사용할 프로바이더를 선택할 수 있습니다. 해당 프로바이더명은 `config/auth.php`에 정의된 프로바이더와 일치해야 합니다. 이후 [미들웨어](#via-middleware)를 통해 지정한 프로바이더 소속 사용자의 요청만 인증할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명 필드 커스터마이징

비밀번호 그랜트를 사용하는 기본 방식을 보면, Passport는 `email` 속성값을 사용자명으로 간주합니다. 필요한 경우 아래 예시처럼 모델에 `findForPassport` 메서드를 정의해 다른 필드를 사용할 수 있습니다:

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
     * 주어진 사용자명에 해당하는 사용자 인스턴스를 찾습니다.
     *
     * @param  string  $username
     * @return \App\Models\User
     */
    public function findForPassport($username)
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### 비밀번호 검증 로직 커스터마이징

비밀번호 그랜트 사용 시 Passport는 기본적으로 `password` 속성으로 비밀번호를 검증합니다. 만약 모델에 `password` 속성이 없거나 직접 검증 로직을 변경하고 싶다면, 아래처럼 `validateForPassportPasswordGrant` 메서드를 모델에 정의하세요:

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
     * Passport 비밀번호 그랜트용 비밀번호 검증 메서드.
     *
     * @param  string  $password
     * @return bool
     */
    public function validateForPassportPasswordGrant($password)
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant-tokens"></a>
## 암시적 그랜트 토큰(Implicit Grant Tokens)

> [!WARNING]
> 암시적 그랜트는 현재 권장되지 않습니다. 대신 [OAuth2 서버 권장 그랜트](https://oauth2.thephpleague.com/authorization-server/which-grant/)를 사용하세요.

암시적 그랜트는 인증 코드 교환 과정 없이 토큰을 클라이언트에 바로 반환합니다. 주로 JavaScript SPA나 모바일 앱 같이 클라이언트 자격 증명을 안전하게 저장할 수 없는 환경에 적합합니다. 활성화하려면 `App\Providers\AuthServiceProvider`의 `boot` 메서드에 `Passport::enableImplicitGrant`를 호출하세요:

```php
/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::enableImplicitGrant();
}
```

활성화되면 클라이언트는 다음과 같이 `/oauth/authorize` 경로로 리디렉션해 액세스 토큰을 요청할 수 있습니다:

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
> `/oauth/authorize` 라우트는 Passport가 기본 정의하여 직접 정의할 필요 없습니다.

<a name="client-credentials-grant-tokens"></a>
## 클라이언트 자격 증명 그랜트 토큰(Client Credentials Grant Tokens)

클라이언트 자격 증명 그랜트는 서버 간 인증에 적합합니다. 예를 들어 스케줄러 작업 등 API 유지보수를 위해 사용할 수 있습니다.

이 그랜트를 사용하려면 `passport:client` 커맨드에 `--client` 옵션으로 클라이언트를 생성하세요:

```shell
php artisan passport:client --client
```

그 다음, `app/Http/Kernel.php` 파일의 `$routeMiddleware` 배열에 `CheckClientCredentials` 미들웨어를 추가합니다:

```php
use Laravel\Passport\Http\Middleware\CheckClientCredentials;

protected $routeMiddleware = [
    'client' => CheckClientCredentials::class,
];
```

미들웨어를 특정 라우트에 붙여서 클라이언트 그랜트를 이용한 인증만 허용할 수 있습니다:

```php
Route::get('/orders', function (Request $request) {
    ...
})->middleware('client');
```

특정 스코프만 허용하고 싶으면 콤마 구분으로 미들웨어에 스코프를 지정하세요:

```php
Route::get('/orders', function (Request $request) {
    ...
})->middleware('client:check-status,your-scope');
```

<a name="retrieving-tokens"></a>
### 토큰 가져오기

이 그랜트를 이용하려면 `oauth/token` 엔드포인트에 다음처럼 요청하세요:

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
## 개인 액세스 토큰(Personal Access Tokens)

때때로 사용자는 일반 인증 코드 리디렉션 과정을 거치지 않고 직접 액세스 토큰을 발급받고 싶어할 수 있습니다. 자신의 토큰을 발급할 수 있게 하면 API 테스트나 단순한 토큰 관리에 유용합니다.

> [!NOTE]
> 개인 액세스 토큰 발급이 주 목적이라면 Laravel의 경량 API 액세스 토큰 관리 라이브러리인 [Laravel Sanctum](/docs/9.x/sanctum) 사용을 고려하세요.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성하기

개인 액세스 토큰 발급을 위해서는 `passport:client` 명령어에 `--personal` 옵션을 붙여 클라이언트를 생성해야 합니다. 이미 `passport:install`을 실행했다면 이 과정은 생략할 수 있습니다:

```shell
php artisan passport:client --personal
```

생성 후 `.env` 파일에 클라이언트 ID와 평문 비밀 값을 넣으세요:

```ini
PASSPORT_PERSONAL_ACCESS_CLIENT_ID="client-id-value"
PASSPORT_PERSONAL_ACCESS_CLIENT_SECRET="unhashed-client-secret-value"
```

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리하기

개인 액세스 클라이언트를 만든 뒤, `App\Models\User` 모델 인스턴스에서 `createToken` 메서드로 토큰을 생성할 수 있습니다. 이 메서드는 토큰 이름을 첫 번째 인자로 받고, 두 번째 인자로 선택적인 스코프 배열을 받습니다:

```php
use App\Models\User;

$user = User::find(1);

// 스코프 없이 토큰 생성...
$token = $user->createToken('Token Name')->accessToken;

// 스코프와 함께 토큰 생성...
$token = $user->createToken('My Token', ['place-orders'])->accessToken;
```

<a name="personal-access-tokens-json-api"></a>
#### JSON API

Passport는 개인 액세스 토큰을 관리하는 JSON API도 제공합니다. 자신의 프런트엔드와 연동해 사용자 대시보드를 구성하세요. API는 `web`과 `auth` 미들웨어로 보호되어 외부 호출이 안 됩니다.

<a name="get-oauthscopes"></a>
#### `GET /oauth/scopes`

애플리케이션에 정의된 모든 스코프를 반환합니다. 사용자가 개인 액세스 토큰에 할당 가능한 스코프 목록을 보여줄 때 사용합니다:

```js
axios.get('/oauth/scopes')
    .then(response => {
        console.log(response.data);
    });
```

<a name="get-oauthpersonal-access-tokens"></a>
#### `GET /oauth/personal-access-tokens`

인증된 사용자가 생성한 개인 액세스 토큰을 모두 반환합니다. 토큰을 관리 및 취소할 때 유용합니다:

```js
axios.get('/oauth/personal-access-tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthpersonal-access-tokens"></a>
#### `POST /oauth/personal-access-tokens`

새 개인 액세스 토큰을 생성합니다. `name`과 부여할 `scopes` 배열이 필요합니다:

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
        // 에러 출력
    });
```

<a name="delete-oauthpersonal-access-tokenstoken-id"></a>
#### `DELETE /oauth/personal-access-tokens/{token-id}`

개인 액세스 토큰을 취소합니다:

```js
axios.delete('/oauth/personal-access-tokens/' + tokenId);
```

<a name="protecting-routes"></a>
## 라우트 보호하기

<a name="via-middleware"></a>
### 미들웨어를 통한 보호

Passport는 액세스 토큰을 검증하는 [인증 가드](/docs/9.x/authentication#adding-custom-guards)를 제공합니다. `api` 가드를 `passport` 드라이버로 설정한 후, 액세스 토큰이 필요한 라우트에 `auth:api` 미들웨어를 붙이세요:

```php
Route::get('/user', function () {
    //
})->middleware('auth:api');
```

> [!WARNING]
> 만약 [클라이언트 자격 증명 그랜트](#client-credentials-grant-tokens)를 사용한다면, `auth:api` 대신 [client 미들웨어](#client-credentials-grant-tokens)를 사용하세요.

<a name="multiple-authentication-guards"></a>
#### 다중 인증 가드

애플리케이션에서 여러 종류의 사용자(예: 서로 다른 Eloquent 모델)를 인증해야 한다면, 각각에 맞는 인증 가드를 `config/auth.php`에 정의할 수 있습니다. 예를 들어 아래와 같이 설정하면:

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

아래 라우트는 `customers` 프로바이더를 사용하는 `api-customers` 가드를 통해 인증합니다:

```php
Route::get('/customer', function () {
    //
})->middleware('auth:api-customers');
```

> [!NOTE]
> 여러 사용자 프로바이더와 Passport를 사용하는 자세한 내용은 [비밀번호 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달하기

Passport로 보호된 라우트 호출 시, API 사용자는 요청 헤더 `Authorization`에 `Bearer` 토큰 형식으로 액세스 토큰을 전달해야 합니다. 예를 들어 Guzzle HTTP 클라이언트 사용 시:

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => 'Bearer '.$accessToken,
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
## 토큰 스코프(Token Scopes)

스코프는 API 클라이언트가 특정 권한만 요청하도록 제한하는 방법입니다. 예를 들어, 일부 클라이언트는 주문 접수 권한이 필요 없고 배송 상태 확인만 필요할 수 있습니다. 이렇게 스코프로 사용자의 권한을 제한할 수 있습니다.

<a name="defining-scopes"></a>
### 스코프 정의하기

`App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `Passport::tokensCan` 메서드를 사용해 API 스코프를 정의할 수 있습니다. 키는 스코프명, 값은 설명으로 쓰여 승인 화면에 표시됩니다:

```php
/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::tokensCan([
        'place-orders' => 'Place orders',
        'check-status' => 'Check order status',
    ]);
}
```

<a name="default-scope"></a>
### 기본 스코프 설정하기

클라이언트가 특정 스코프를 요청하지 않은 경우 기본 스코프를 토큰에 할당하고 싶다면 `setDefaultScope` 메서드를 사용하세요. 보통 `AuthServiceProvider`의 `boot` 메서드 내에 정의합니다:

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
> 기본 스코프는 사용자가 생성하는 개인 액세스 토큰에는 적용되지 않습니다.

<a name="assigning-scopes-to-tokens"></a>
### 토큰에 스코프 할당하기

<a name="when-requesting-authorization-codes"></a>
#### 인증 코드 요청 시

인증 코드 그랜트를 사용할 때, 클라이언트는 `scope` 쿼리 매개변수에 요청할 스코프를 공백으로 구분해 지정합니다:

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

`App\Models\User` 모델의 `createToken` 메서드를 사용할 때 원하는 스코프 배열을 두 번째 인자로 전달할 수 있습니다:

```php
$token = $user->createToken('My Token', ['place-orders'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 체크하기

Passport는 미들웨어 두 가지를 제공합니다. 이를 등록하려면 `app/Http/Kernel.php` 파일 내부 `$routeMiddleware` 배열에 아래를 추가하세요:

```php
'scopes' => \Laravel\Passport\Http\Middleware\CheckScopes::class,
'scope' => \Laravel\Passport\Http\Middleware\CheckForAnyScope::class,
```

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인(`scopes`)

`scopes` 미들웨어는 요청된 토큰이 나열된 모든 스코프를 갖고 있는지 검사합니다:

```php
Route::get('/orders', function () {
    // "check-status"와 "place-orders" 스코프를 모두 가진 경우
})->middleware(['auth:api', 'scopes:check-status,place-orders']);
```

<a name="check-for-any-scopes"></a>
#### 일부 스코프 확인(`scope`)

`scope` 미들웨어는 요청된 토큰이 나열한 스코프 중 하나라도 갖고 있는지 검사합니다:

```php
Route::get('/orders', function () {
    // "check-status" 또는 "place-orders" 스코프 중 하나만 있어도 통과
})->middleware(['auth:api', 'scope:check-status,place-orders']);
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인하기

인증 처리된 요청 내에서 현재 토큰이 특정 스코프가 있는지 `tokenCan` 메서드를 통해 확인할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('place-orders')) {
        //
    }
});
```

<a name="additional-scope-methods"></a>
#### 추가 스코프 관련 메서드

- `scopeIds`: 정의된 모든 스코프명 배열 반환

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

- `scopes`: `Laravel\Passport\Scope` 인스턴스 배열 반환

```php
Passport::scopes();
```

- `scopesFor`: 지정한 스코프명에 대응하는 `Scope` 인스턴스 배열 반환

```php
Passport::scopesFor(['place-orders', 'check-status']);
```

- `hasScope`: 특정 스코프가 정의되어 있는지 여부 반환

```php
Passport::hasScope('place-orders');
```

<a name="consuming-your-api-with-javascript"></a>
## JavaScript로 API 사용하기

API를 개발할 때, JavaScript 앱에서 직접 API를 호출할 수 있으면 매우 편리합니다. 이렇게 하면 웹 앱, 모바일 앱, 서드파티 앱, SDK 등 다양한 클라이언트에서 동일한 API를 사용할 수 있습니다.

일반적으로는 클라이언트에 액세스 토큰을 전달하고 요청할 때마다 보내야 하지만, Passport는 이를 쉽게 처리해주는 미들웨어를 제공합니다. `app/Http/Kernel.php`의 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어를 추가하세요:

```php
'web' => [
    // 기타 미들웨어...
    \Laravel\Passport\Http\Middleware\CreateFreshApiToken::class,
],
```

> [!WARNING]
> 이 미들웨어는 스택 내에서 가장 마지막에 위치해야 합니다.

이 미들웨어는 응답에 암호화된 JWT를 담은 `laravel_token` 쿠키를 첨부합니다. 브라우저가 이후 모든 요청에 이 쿠키를 자동으로 보내므로, 클라이언트가 매번 액세스 토큰을 명시적으로 전달하지 않아도 됩니다:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이징

필요하면 `Passport::cookie` 메서드로 쿠키 이름을 지정할 수 있습니다. 보통 `AuthServiceProvider`의 `boot` 메서드에서 호출하세요:

```php
/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::cookie('custom_name');
}
```

<a name="csrf-protection"></a>
#### CSRF 보호

이 방식으로 인증할 때는 요청에 올바른 CSRF 토큰 헤더가 포함되어야 합니다. 기본 Laravel JavaScript 스캐폴딩에서는 Axios가 암호화된 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더로 자동 설정합니다.

> [!NOTE]
> 만약 `X-CSRF-TOKEN` 헤더를 사용한다면, `csrf_token()`에서 제공하는 비암호화 토큰을 사용해야 합니다.

<a name="events"></a>
## 이벤트(Events)

Passport는 액세스 토큰과 리프레시 토큰이 생성될 때 이벤트를 발생시킵니다. 이를 통해 데이터베이스에서 이전 토큰을 정리하거나 취소할 수 있습니다. 필요한 경우 `App\Providers\EventServiceProvider`에서 아래처럼 이벤트 리스너를 연결하세요:

```php
/**
 * 이벤트와 리스너 매핑.
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
## 테스트(Test)

Passport의 `actingAs` 메서드는 현재 인증된 사용자와 부여할 스코프를 지정하는 데 사용할 수 있습니다. 첫 번째 인자로 사용자 인스턴스를, 두 번째 인자로는 토큰에 부여할 스코프 배열을 전달합니다:

```php
use App\Models\User;
use Laravel\Passport\Passport;

public function test_servers_can_be_created()
{
    Passport::actingAs(
        User::factory()->create(),
        ['create-servers']
    );

    $response = $this->post('/api/create-server');

    $response->assertStatus(201);
}
```

`actingAsClient` 메서드는 현재 인증된 클라이언트와 스코프를 지정하는 데 사용합니다. 첫 번째 인자는 클라이언트 인스턴스, 두 번째는 부여할 스코프 배열입니다:

```php
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

public function test_orders_can_be_retrieved()
{
    Passport::actingAsClient(
        Client::factory()->create(),
        ['check-status']
    );

    $response = $this->get('/api/orders');

    $response->assertStatus(200);
}
```