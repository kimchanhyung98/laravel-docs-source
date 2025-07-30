# Laravel Passport

- [소개](#introduction)
    - [Passport 아니면 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [마이그레이션 커스터마이징](#migration-customization)
    - [Passport 업그레이드하기](#upgrading-passport)
- [설정](#configuration)
    - [클라이언트 비밀값 해싱](#client-secret-hashing)
    - [토큰 수명 설정](#token-lifetimes)
    - [기본 모델 오버라이드하기](#overriding-default-models)
- [액세스 토큰 발급하기](#issuing-access-tokens)
    - [클라이언트 관리하기](#managing-clients)
    - [토큰 요청하기](#requesting-tokens)
    - [토큰 갱신하기](#refreshing-tokens)
    - [토큰 폐기하기](#revoking-tokens)
    - [토큰 정리하기](#purging-tokens)
- [PKCE를 사용하는 인증 코드 그랜트](#code-grant-pkce)
    - [클라이언트 생성하기](#creating-a-auth-pkce-grant-client)
    - [토큰 요청하기](#requesting-auth-pkce-grant-tokens)
- [비밀번호 그랜트 토큰](#password-grant-tokens)
    - [비밀번호 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청하기](#requesting-password-grant-tokens)
    - [모든 스코프 요청하기](#requesting-all-scopes)
    - [사용자 프로바이더 커스터마이징](#customizing-the-user-provider)
    - [사용자 이름 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 커스터마이징](#customizing-the-password-validation)
- [암시적 그랜트 토큰](#implicit-grant-tokens)
- [클라이언트 자격 증명 그랜트 토큰](#client-credentials-grant-tokens)
- [개인 액세스 토큰](#personal-access-tokens)
    - [개인 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [개인 액세스 토큰 관리하기](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어를 사용하여](#via-middleware)
    - [액세스 토큰 전달하기](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의하기](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당하기](#assigning-scopes-to-tokens)
    - [스코프 체크하기](#checking-scopes)
- [JavaScript로 API 사용하기](#consuming-your-api-with-javascript)
- [이벤트](#events)
- [테스트하기](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Passport](https://github.com/laravel/passport)는 몇 분 만에 Laravel 애플리케이션용 완전한 OAuth2 서버 구현을 제공합니다. Passport는 Andy Millington과 Simon Hamp가 유지 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server)를 기반으로 구축되었습니다.

> [!NOTE]
> 이 문서는 OAuth2에 익숙하다는 가정 하에 작성되었습니다. OAuth2에 대해 모른다면, 계속 진행하기 전에 일반적인 [용어 정리](https://oauth2.thephpleague.com/terminology/)와 OAuth2 기능에 대한 이해를 먼저 하는 것을 권장합니다.

<a name="passport-or-sanctum"></a>
### Passport 아니면 Sanctum? (Passport Or Sanctum?)

시작하기 전에, Laravel Passport를 사용할지 [Laravel Sanctum](/docs/{{version}}/sanctum)을 사용할지 결정하는 것이 좋습니다. 애플리케이션이 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용해야 합니다.

하지만, 싱글 페이지 애플리케이션, 모바일 애플리케이션의 인증이나 API 토큰 발급이 목적이라면 [Laravel Sanctum](/docs/{{version}}/sanctum)을 사용하는 것이 좋습니다. Laravel Sanctum은 OAuth2를 지원하지 않지만 훨씬 간단한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면 Composer를 사용하여 Passport 패키지를 설치하세요:

```
composer require laravel/passport
```

Passport의 [서비스 프로바이더](/docs/{{version}}/providers)는 자체 데이터베이스 마이그레이션 디렉터리를 등록하므로, 패키지 설치 후 데이터베이스를 마이그레이션해야 합니다. Passport 마이그레이션은 OAuth2 클라이언트 및 액세스 토큰을 저장하는 데 필요한 테이블을 생성합니다:

```
php artisan migrate
```

그 다음, `passport:install` Artisan 명령어를 실행하세요. 이 명령어는 안전한 액세스 토큰을 생성하기 위해 필요한 암호화 키를 생성합니다. 또한, "개인 액세스" 및 "비밀번호 그랜트" 클라이언트도 생성됩니다. 이 클라이언트는 액세스 토큰을 생성할 때 사용됩니다:

```
php artisan passport:install
```

> [!TIP]
> Passport `Client` 모델의 기본 키를 자동 증가하는 정수 대신 UUID로 사용하려면 [ `uuids` 옵션](#client-uuids)으로 Passport를 설치하세요.

`passport:install` 명령어 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트를 추가하세요. 이 트레이트는 인증된 사용자의 토큰과 스코프를 검사할 수 있는 몇 가지 헬퍼 메서드를 제공합니다. 이미 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용 중이라면 제거해도 됩니다:

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

다음으로, `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드 내에서 `Passport::routes` 메서드를 호출해야 합니다. 이 메서드는 액세스 토큰 발급, 토큰 폐기, 클라이언트 및 개인 액세스 토큰 관련 라우트를 등록합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Gate;
use Laravel\Passport\Passport;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 정책 매핑
     *
     * @var array
     */
    protected $policies = [
        'App\Models\Model' => 'App\Policies\ModelPolicy',
    ];

    /**
     * 인증 및 인가 서비스 등록
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        if (! $this->app->routesAreCached()) {
            Passport::routes();
        }
    }
}
```

마지막으로, `config/auth.php` 설정 파일에서 `api` 인증 가드의 `driver` 옵션을 `passport`로 설정하세요. 이렇게 하면 들어오는 API 요청을 인증할 때 Passport의 `TokenGuard`가 사용됩니다:

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
#### 클라이언트 UUID 사용하기 (Client UUIDs)

`passport:install` 명령어를 `--uuids` 옵션과 함께 실행할 수도 있습니다. 이 옵션을 사용하면 Passport가 클라이언트 모델의 기본 키로 자동 증가 정수가 아닌 UUID를 사용하도록 지정하게 됩니다. 이 옵션 사용 후에는 Passport 기본 마이그레이션 비활성화 방법에 관한 추가 안내도 받게 됩니다:

```
php artisan passport:install --uuids
```

<a name="deploying-passport"></a>
### Passport 배포하기 (Deploying Passport)

애플리케이션 서버에 Passport를 처음 배포할 때는 `passport:keys` 명령어를 실행해야 하는 경우가 많습니다. 이 명령어는 액세스 토큰 생성에 필요한 암호화 키를 생성합니다. 생성된 키는 보통 소스 관리에 포함하지 않습니다:

```
php artisan passport:keys
```

필요하다면, Passport 키를 로드할 경로를 정의할 수도 있습니다. `Passport::loadKeysFrom` 메서드를 사용하면 됩니다. 보통 이 메서드는 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
/**
 * 인증 / 인가 서비스 등록
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::routes();

    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
}
```

<a name="loading-keys-from-the-environment"></a>
#### 환경 변수에서 키 로드하기 (Loading Keys From The Environment)

또는 `vendor:publish` Artisan 명령어로 Passport 설정 파일을 발행할 수도 있습니다:

```
php artisan vendor:publish --tag=passport-config
```

발행한 설정 파일에서 앱 암호화 키를 환경 변수로 정의하여 로드할 수 있습니다:

```bash
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="migration-customization"></a>
### 마이그레이션 커스터마이징 (Migration Customization)

Passport 기본 마이그레이션을 사용하지 않으려면 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에 `Passport::ignoreMigrations` 메서드를 호출하세요. 기본 마이그레이션 파일은 `vendor:publish` Artisan 명령어로 내보낼 수 있습니다:

```
php artisan vendor:publish --tag=passport-migrations
```

<a name="upgrading-passport"></a>
### Passport 업그레이드하기 (Upgrading Passport)

Passport의 메이저 버전 업그레이드시, 꼭 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 주의 깊게 확인하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="client-secret-hashing"></a>
### 클라이언트 비밀값 해싱 (Client Secret Hashing)

클라이언트 비밀값을 데이터베이스에 저장할 때 해싱하려면 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `Passport::hashClientSecrets` 메서드를 호출하세요:

```php
use Laravel\Passport\Passport;

Passport::hashClientSecrets();
```

이 기능을 활성화하면 클라이언트 비밀값은 생성 직후에만 사용자에게 보여지며, 데이터베이스에 평문으로 저장되지 않아서 분실 시 복구가 불가능합니다.

<a name="token-lifetimes"></a>
### 토큰 수명 설정 (Token Lifetimes)

기본적으로 Passport는 1년 뒤 만료되는 장기 액세스 토큰을 발행합니다. 더 길거나 짧은 토큰 수명을 설정하려면 `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용하세요. 보통 이 메서드들은 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
/**
 * 인증 / 인가 서비스 등록
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::routes();

    Passport::tokensExpireIn(now()->addDays(15));
    Passport::refreshTokensExpireIn(now()->addDays(30));
    Passport::personalAccessTokensExpireIn(now()->addMonths(6));
}
```

> [!NOTE]
> Passport 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며, 표시용입니다. 실제 토큰 발급 시 만료 정보는 암호화된 토큰 내부에 저장됩니다. 토큰을 무효화하려면 [토큰 폐기](#revoking-tokens)를 하세요.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드하기 (Overriding Default Models)

내부적으로 사용되는 Passport 모델을 직접 확장하여 커스터마이징할 수 있습니다. 예를 들어 다음과 같이 자신만의 모델을 정의할 수 있습니다:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

정의한 모델을 Passport에 알려주려면 `Laravel\Passport\Passport` 클래스의 메서드를 사용합니다. 보통 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 아래처럼 호출하세요:

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\PersonalAccessClient;
use App\Models\Passport\Token;

/**
 * 인증 / 인가 서비스 등록
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::routes();

    Passport::useTokenModel(Token::class);
    Passport::useClientModel(Client::class);
    Passport::useAuthCodeModel(AuthCode::class);
    Passport::usePersonalAccessClientModel(PersonalAccessClient::class);
}
```

<a name="issuing-access-tokens"></a>
## 액세스 토큰 발급하기 (Issuing Access Tokens)

대부분 개발자는 OAuth2의 인증 코드 그랜트를 가장 익숙하게 사용할 것입니다. 이 방식을 쓸 경우, 클라이언트 애플리케이션이 사용자를 서버로 리다이렉트하고 사용자는 토큰 발급 요청을 승인하거나 거부합니다.

<a name="managing-clients"></a>
### 클라이언트 관리하기 (Managing Clients)

먼저, 애플리케이션 API와 상호작용하려는 개발자는 자신의 애플리케이션을 “클라이언트”로 등록해야 합니다. 보통 애플리케이션 이름과 사용자가 권한 요청을 승인 이후 리다이렉트할 URL을 제공합니다.

<a name="the-passportclient-command"></a>
#### `passport:client` 명령어 (The `passport:client` Command)

가장 간단한 클라이언트 생성 방법은 `passport:client` Artisan 명령어를 사용하는 것입니다. 이 명령어는 OAuth2 기능 테스트용 클라이언트를 쉽게 생성합니다. 실행하면 클라이언트에 관한 정보를 묻고 클라이언트 ID와 시크릿을 제공합니다:

```
php artisan passport:client
```

**리다이렉트 URL 다중 지정**

여러 리다이렉트 URL을 허용하려면 `passport:client` 명령어에서 URL 입력 시 쉼표(,)로 구분하여 나열할 수 있습니다. 쉼표가 포함된 URL은 URL 인코딩하세요:

```bash
http://example.com/callback,http://examplefoo.com/callback
```

<a name="clients-json-api"></a>
#### JSON API

사용자들이 직접 `client` 명령어를 사용할 수 없기에, Passport는 클라이언트 생성/수정/삭제용 JSON API를 제공합니다. 이를 자체 프론트엔드와 연동해 대시보드로 활용할 수 있습니다. 편의를 위해 [Axios](https://github.com/axios/axios)를 사용한 HTTP 요청 예시를 소개합니다.

JSON API는 `web` 및 `auth` 미들웨어로 보호되므로 외부에서 호출할 수 없고, 반드시 애플리케이션 내부에서만 호출 가능합니다.

<a name="get-oauthclients"></a>
#### `GET /oauth/clients`

인증된 사용자의 모든 클라이언트 정보를 반환합니다. 주로 사용자가 자신의 클라이언트를 조회하고 수정하거나 삭제할 때 유용합니다:

```js
axios.get('/oauth/clients')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthclients"></a>
#### `POST /oauth/clients`

새 클라이언트를 생성하며, 클라이언트 이름과 리다이렉트 URL이 필요합니다. 생성 시 클라이언트 ID와 시크릿이 발급되며 새 클라이언트 인스턴스를 반환합니다:

```js
const data = {
    name: 'Client Name',
    redirect: 'http://example.com/callback'
};

axios.post('/oauth/clients', data)
    .then(response => {
        console.log(response.data);
    })
    .catch(response => {
        // 오류 처리...
    });
```

<a name="put-oauthclientsclient-id"></a>
#### `PUT /oauth/clients/{client-id}`

기존 클라이언트를 수정하며, 클라이언트 이름과 리다이렉트 URL을 받습니다. 수정된 클라이언트 인스턴스를 반환합니다:

```js
const data = {
    name: 'New Client Name',
    redirect: 'http://example.com/callback'
};

axios.put('/oauth/clients/' + clientId, data)
    .then(response => {
        console.log(response.data);
    })
    .catch(response => {
        // 오류 처리...
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
### 토큰 요청하기 (Requesting Tokens)

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 권한 요청을 위한 리다이렉트 (Redirecting For Authorization)

클라이언트가 생성되고 나면, 클라이언트 ID와 시크릿을 이용해 인증 코드를 요청하고 액세스 토큰을 받기 위해 앱의 `/oauth/authorize` 라우트로 리다이렉트해야 합니다:

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
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

> [!TIP]
> `/oauth/authorize` 라우트는 이미 `Passport::routes` 메서드에서 정의되어 있어 직접 추가할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 권한 요청 승인하기 (Approving The Request)

권한 요청 수신 시 Passport는 사용자에게 권한 요청 승인 또는 거부 화면을 자동으로 보여줍니다. 승인이 되면 소비자 앱에서 요청한 `redirect_uri`로 리다이렉션됩니다. 이 `redirect_uri`는 클라이언트 생성 시 지정했던 `redirect` URL과 일치해야 합니다.

승인 화면을 커스터마이징 하려면 `vendor:publish` Artisan 명령어로 뷰 파일을 게시하세요. 게시된 뷰는 `resources/views/vendor/passport` 경로에 위치합니다:

```
php artisan vendor:publish --tag=passport-views
```

첫 번째 당사자(First-party) 클라이언트처럼 권한 요청 화면을 건너뛰고 싶으면, [`Client` 모델 확장](#overriding-default-models) 후 `skipsAuthorization` 메서드를 정의하면 됩니다. 이 메서드가 `true`를 반환하면 클라이언트가 즉시 승인되어 사용자에게 리다이렉트됩니다:

```php
<?php

namespace App\Models\Passport;

use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 클라이언트가 권한 요청 화면을 건너뛸지 결정합니다.
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
#### 인증 코드를 액세스 토큰으로 변환하기 (Converting Authorization Codes To Access Tokens)

사용자가 권한 요청을 승인하면 소비자 앱으로 리다이렉트됩니다. 소비자 앱은 먼저 `state` 파라미터가 미리 저장했던 값과 같은지 검증해야 합니다. 일치할 경우, `POST` 요청을 보내 승인을 통해 발급 받은 인증 코드를 액세스 토큰으로 교환할 수 있습니다:

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

`/oauth/token` 경로는 JSON 형태로 `access_token`, `refresh_token`, `expires_in` 값을 반환합니다. `expires_in`은 토큰 만료까지 남은 초 단위 시간이 됩니다.

> [!TIP]
> `/oauth/token` 경로도 `Passport::routes` 메서드에 의해 자동 등록되므로 직접 라우트를 정의할 필요 없습니다.

<a name="tokens-json-api"></a>
#### JSON API

Passport는 권한 부여된 액세스 토큰을 관리할 수 있는 JSON API를 제공합니다. 이를 자체 프론트엔드와 연동해 사용자에게 액세스 토큰 관리 대시보드를 제공할 수 있습니다. Axios로 요청하는 예시는 다음과 같습니다. JSON API는 `web` 및 `auth` 미들웨어로 보호되어 애플리케이션 내부에서만 호출 가능합니다.

<a name="get-oauthtokens"></a>
#### `GET /oauth/tokens`

인증된 사용자가 생성한 모든 액세스 토큰을 반환합니다. 사용자는 이 목록에서 토큰을 취소할 수 있습니다:

```js
axios.get('/oauth/tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="delete-oauthtokenstoken-id"></a>
#### `DELETE /oauth/tokens/{token-id}`

인증된 액세스 토큰과 관련된 리프레시 토큰을 폐기(취소)할 수 있습니다:

```js
axios.delete('/oauth/tokens/' + tokenId);
```

<a name="refreshing-tokens"></a>
### 토큰 갱신하기 (Refreshing Tokens)

단기 만료 액세스 토큰을 사용한다면, 사용자는 액세스 토큰 발급 시 받은 리프레시 토큰을 통해 토큰을 갱신해야 합니다:

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

`/oauth/token` 경로는 위와 같이 새로운 `access_token`, `refresh_token`, `expires_in`을 반환합니다.

<a name="revoking-tokens"></a>
### 토큰 폐기하기 (Revoking Tokens)

`Laravel\Passport\TokenRepository`의 `revokeAccessToken` 메서드를 사용해 액세스 토큰을 폐기할 수 있습니다. 관련 리프레시 토큰은 `Laravel\Passport\RefreshTokenRepository`의 `revokeRefreshTokensByAccessTokenId` 메서드로 폐기합니다. 두 클래스는 Laravel 서비스 컨테이너를 통해 인스턴스를 가져올 수 있습니다:

```php
use Laravel\Passport\TokenRepository;
use Laravel\Passport\RefreshTokenRepository;

$tokenRepository = app(TokenRepository::class);
$refreshTokenRepository = app(RefreshTokenRepository::class);

// 액세스 토큰 폐기...
$tokenRepository->revokeAccessToken($tokenId);

// 관련 리프레시 토큰 모두 폐기...
$refreshTokenRepository->revokeRefreshTokensByAccessTokenId($tokenId);
```

<a name="purging-tokens"></a>
### 토큰 정리하기 (Purging Tokens)

폐기되거나 만료된 토큰을 데이터베이스에서 삭제하려면 Passport가 제공하는 `passport:purge` Artisan 명령어를 사용할 수 있습니다:

```
# 폐기되거나 만료된 토큰 및 인증 코드 정리...
php artisan passport:purge

# 폐기된 토큰 및 인증 코드만 정리...
php artisan passport:purge --revoked

# 만료된 토큰 및 인증 코드만 정리...
php artisan passport:purge --expired
```

또한 [스케줄링 기능](/docs/{{version}}/scheduling)을 이용해 `App\Console\Kernel` 클래스에서 정기적으로 토큰을 정리하도록 설정할 수 있습니다:

```php
/**
 * 애플리케이션 명령어 스케줄 정의
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
## PKCE를 사용하는 인증 코드 그랜트 (Authorization Code Grant with PKCE)

PKCE("Proof Key for Code Exchange")가 적용된 인증 코드 그랜트는 싱글 페이지 앱이나 네이티브 앱을 안전하게 인증할 수 있는 방법입니다. 클라이언트 시크릿을 안전하게 저장하기 어렵거나 인증 코드 탈취 위험을 줄이고자 할 때 권장됩니다. 클라이언트 시크릿 대신 “코드 베리파이어”와 “코드 챌린지” 조합으로 토큰 교환을 진행합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성하기 (Creating The Client)

PKCE 지원 클라이언트를 생성하려면 `passport:client` Artisan 명령어를 `--public` 옵션과 함께 실행하세요:

```
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청하기 (Requesting Tokens)

<a name="code-verifier-code-challenge"></a>
#### 코드 베리파이어 & 코드 챌린지 (Code Verifier & Code Challenge)

이 인증 그랜트는 클라이언트 시크릿을 사용하지 않으므로, 개발자는 토큰 요청 시 사용할 코드 베리파이어와 코드 챌린지를 생성해야 합니다.

코드 베리파이어는 RFC 7636 스펙에 따라 영문 및 숫자, `"-"`, `"."`, `"_"`, `"~"` 문자를 포함하는 길이 43~128자의 랜덤 문자열입니다.

코드 챌린지는 SHA-256 해시값을 base64 인코딩 후 URL/파일 이름 안전한 문자열로 만듭니다. 끝에 붙은 `'='`는 제거하고 줄바꿈, 공백 등의 문자도 포함하면 안 됩니다.

```php
$encoded = base64_encode(hash('sha256', $code_verifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 권한 요청을 위한 리다이렉트 (Redirecting For Authorization)

클라이언트가 생성되면, 클라이언트 ID와 생성된 코드 베리파이어/챌린지를 사용해 `/oauth/authorize` 경로로 리다이렉션 요청을 합니다:

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
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
#### 인증 코드를 액세스 토큰으로 변환하기 (Converting Authorization Codes To Access Tokens)

승인 후 리다이렉트될 때 기본 인증 코드 그랜트와 같이 `state` 검증을 수행합니다. 검증이 성공하면 클라이언트는 요청 시 생성했던 코드 베리파이어와 함께 `POST` 요청을 보내 액세스 토큰을 요청합니다:

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
## 비밀번호 그랜트 토큰 (Password Grant Tokens)

> [!NOTE]
> 비밀번호 그랜트 토큰은 더 이상 추천하지 않습니다. 대신 [OAuth2 서버에서 권장하는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 사용하세요.

OAuth2 비밀번호 그랜트는 모바일 등 첫 번째 당사자(First-party) 클라이언트가 이메일 또는 사용자 이름과 비밀번호를 사용해 액세스 토큰을 발급받을 수 있게 합니다. 이를 통해 사용자가 OAuth2 인증 코드 리다이렉트 과정을 거치지 않고도 액세스 토큰을 안전하게 발급받을 수 있습니다.

<a name="creating-a-password-grant-client"></a>
### 비밀번호 그랜트 클라이언트 생성 (Creating A Password Grant Client)

비밀번호 그랜트 토큰 발급을 위해 먼저 `passport:client` Artisan 명령어를 `--password` 옵션과 함께 실행해 비밀번호 그랜트 클라이언트를 생성하세요. **`passport:install` 명령어를 이미 실행했다면 이 단계는 건너뛰세요:**

```
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청하기 (Requesting Tokens)

비밀번호 그랜트 클라이언트 생성 후, 사용자 이메일 및 비밀번호를 포함하여 `/oauth/token` 경로로 `POST` 요청을 보내 액세스 토큰을 요청합니다. 이 경로는 이미 `Passport::routes` 메서드로 등록되어 있으므로 직접 정의할 필요는 없습니다. 성공시 JSON 응답에 액세스 토큰과 리프레시 토큰이 포함됩니다:

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

> [!TIP]
> 기본적으로 액세스 토큰은 장기 유효하지만 필요하면 [최대 액세스 토큰 수명](#configuration)을 조절할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청하기 (Requesting All Scopes)

비밀번호 그랜트 또는 클라이언트 자격 증명 그랜트 사용 시 애플리케이션에서 지원하는 모든 스코프에 대해 토큰 권한을 부여하려면 `*` 스코프를 요청하세요. `*` 스코프가 포함된 토큰은 `can` 메서드 실행 시 항상 `true`를 반환합니다. 이 스코프는 이 두 그랜트 타입에서만 사용가능합니다:

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
### 사용자 프로바이더 커스터마이징 (Customizing The User Provider)

애플리케이션에서 둘 이상의 [인증 사용자 프로바이더](/docs/{{version}}/authentication#introduction)를 사용하는 경우, 비밀번호 그랜트 클라이언트를 생성 시 `--provider` 옵션으로 사용 프로바이더를 지정하세요. 지정한 프로바이더 이름은 `config/auth.php`에서 정의한 유효한 프로바이더여야 합니다. 이후 미들웨어를 이용해 해당 프로바이더만 권한을 허용할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자 이름 필드 커스터마이징 (Customizing The Username Field)

비밀번호 그랜트에서 Passport는 기본적으로 인증 가능한 모델의 `email` 속성을 사용자 이름으로 사용합니다. 이 동작을 바꾸려면 모델에 `findForPassport` 메서드를 정의하세요:

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
     * 지정한 사용자 이름으로 사용자 인스턴스 조회
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
### 비밀번호 검증 커스터마이징 (Customizing The Password Validation)

비밀번호 그랜트로 인증 시 Passport는 기본적으로 모델의 `password` 속성으로 비밀번호를 검증합니다. 모델에 `password` 속성이 없거나 검증 로직을 커스터마이징하려면 `validateForPassportPasswordGrant` 메서드를 정의하세요:

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
     * 비밀번호 그랜트용 비밀번호 검증
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
## 암시적 그랜트 토큰 (Implicit Grant Tokens)

> [!NOTE]
> 암시적 그랜트 토큰은 더 이상 추천하지 않습니다. 대신 [OAuth2 서버에서 권장하는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 사용하세요.

암시적 그랜트는 인증 코드 그랜트와 비슷하나, 권한 코드를 교환하지 않고 바로 토큰을 클라이언트에 반환합니다. 보통 클라이언트 시크릿을 안전하게 저장할 수 없는 JavaScript 앱이나 모바일 앱에 사용됩니다. 이 그랜트를 사용하려면 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에 `enableImplicitGrant` 메서드를 추가하세요:

```php
/**
 * 인증 / 인가 서비스 등록
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::routes();

    Passport::enableImplicitGrant();
}
```

이제 개발자는 클라이언트 ID를 사용해 `/oauth/authorize` 경로로 리다이렉트 요청을 하여 액세스 토큰을 요청할 수 있습니다:

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
    ]);

    return redirect('http://passport-app.test/oauth/authorize?'.$query);
});
```

> [!TIP]
> `/oauth/authorize` 라우트는 `Passport::routes` 메서드에서 이미 정의되어 있어 수동으로 추가할 필요 없습니다.

<a name="client-credentials-grant-tokens"></a>
## 클라이언트 자격 증명 그랜트 토큰 (Client Credentials Grant Tokens)

클라이언트 자격 증명 그랜트는 머신 간 인증에 알맞습니다. 예를 들어, API를 통한 스케줄 작업에 사용할 수 있습니다.

사용하려면 먼저 `passport:client` Artisan 명령어를 `--client` 옵션과 함께 실행해 클라이언트 자격 증명 클라이언트를 생성하세요:

```
php artisan passport:client --client
```

그 다음, `app/Http/Kernel.php` 의 `$routeMiddleware` 배열에 `CheckClientCredentials` 미들웨어를 등록하세요:

```php
use Laravel\Passport\Http\Middleware\CheckClientCredentials;

protected $routeMiddleware = [
    'client' => CheckClientCredentials::class,
];
```

미들웨어를 라우트에 붙입니다:

```php
Route::get('/orders', function (Request $request) {
    //
})->middleware('client');
```

특정 스코프에 대한 접근만 허용하려면 미들웨어에 콤마 구분 스코프 목록을 인자로 넘기면 됩니다:

```php
Route::get('/orders', function (Request $request) {
    //
})->middleware('client:check-status,your-scope');
```

<a name="retrieving-tokens"></a>
### 토큰 가져오기 (Retrieving Tokens)

이 그랜트로 토큰을 요청하려면 `oauth/token` 엔드포인트에 아래와 같이 요청하세요:

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
## 개인 액세스 토큰 (Personal Access Tokens)

사용자가 일반적인 인증 코드 플로우 없이 스스로 액세스 토큰을 발급받는 경우가 있습니다. 이는 API 실험용이나 간단한 토큰 발급 수단으로 유용합니다.

> [!TIP]
> 주로 개인 액세스 토큰 용도로 Passport를 쓴다면, 라이트웨이트 API 토큰 발급용 라이브러리인 [Laravel Sanctum](/docs/{{version}}/sanctum) 사용을 고려해보세요.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성 (Creating A Personal Access Client)

개인 액세스 토큰을 발급하려면 먼저 `passport:client` 명령어에 `--personal` 옵션을 붙여 개인 액세스 클라이언트를 생성해야 합니다. 이미 `passport:install` 명령어를 실행했다면 이 단계는 건너뛰세요:

```
php artisan passport:client --personal
```

개인 액세스 클라이언트를 생성하면 클라이언트 ID 및 평문 시크릿 값을 `.env` 파일에 추가하세요:

```bash
PASSPORT_PERSONAL_ACCESS_CLIENT_ID="client-id-value"
PASSPORT_PERSONAL_ACCESS_CLIENT_SECRET="unhashed-client-secret-value"
```

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리하기 (Managing Personal Access Tokens)

개인 액세스 클라이언트가 생성되면, `App\Models\User` 인스턴스에서 `createToken` 메서드로 토큰을 발급할 수 있습니다. 첫 번째 인자는 토큰 이름이고, 두 번째에는 선택적으로 배열 형태의 [스코프](#token-scopes)를 지정할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

// 스코프 없이 토큰 생성...
$token = $user->createToken('Token Name')->accessToken;

// 스코프를 지정해 토큰 생성...
$token = $user->createToken('My Token', ['place-orders'])->accessToken;
```

<a name="personal-access-tokens-json-api"></a>
#### JSON API

Passport는 개인 액세스 토큰 관리를 위한 JSON API도 제공합니다. 자체 프론트엔드에서 연동해 사용자에게 개인 액세스 토큰 관리 대시보드를 제공할 수 있습니다. Axios 요청 예시는 다음과 같습니다. 이 API 역시 `web` 및 `auth` 미들웨어로 보호되어 외부 호출이 불가능합니다.

<a name="get-oauthscopes"></a>
#### `GET /oauth/scopes`

애플리케이션에 정의된 모든 [스코프](#token-scopes)를 반환합니다. 사용자가 개인 액세스 토큰에 할당할 수 있는 스코프 목록을 보여줄 때 유용합니다:

```js
axios.get('/oauth/scopes')
    .then(response => {
        console.log(response.data);
    });
```

<a name="get-oauthpersonal-access-tokens"></a>
#### `GET /oauth/personal-access-tokens`

사용자가 생성한 개인 액세스 토큰 목록을 반환합니다. 주로 토큰 수정 또는 폐기용입니다:

```js
axios.get('/oauth/personal-access-tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthpersonal-access-tokens"></a>
#### `POST /oauth/personal-access-tokens`

새 개인 액세스 토큰을 생성합니다. `name` 및 `scopes` 데이터가 필요합니다:

```js
const data = {
    name: 'Token Name',
    scopes: []
};

axios.post('/oauth/personal-access-tokens', data)
    .then(response => {
        console.log(response.data.accessToken);
    })
    .catch(response => {
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
## 라우트 보호하기 (Protecting Routes)

<a name="via-middleware"></a>
### 미들웨어를 사용하여 (Via Middleware)

Passport는 액세스 토큰 유효성을 검사하는 인증 가드를 포함합니다. `api` 가드 드라이버를 `passport`로 설정 후, 액세스 토큰을 요구하는 라우트에 `auth:api` 미들웨어를 붙이기만 하면 됩니다:

```php
Route::get('/user', function () {
    //
})->middleware('auth:api');
```

> [!NOTE]
> 만약 [클라이언트 자격 증명 그랜트](#client-credentials-grant-tokens)를 사용하는 경우, `auth:api` 대신 [클라이언트 미들웨어](#client-credentials-grant-tokens)를 써서 라우트를 보호해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 다중 인증 가드 (Multiple Authentication Guards)

애플리케이션에서 다른 유형의 사용자를 완전히 다른 Eloquent 모델로 인증한다면, 사용자 프로바이더 타입별로 여러 개 가드를 `config/auth.php`에 정의해야 합니다. 이렇게 하면 특정 사용자 프로바이더용 요청을 개별 가드로 보호할 수 있습니다. 예를 들어, 아래와 같은 가드 설정일 때:

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

아래 경로는 `customers` 프로바이더를 사용하는 `api-customers` 가드로 인증합니다:

```php
Route::get('/customer', function () {
    //
})->middleware('auth:api-customers');
```

> [!TIP]
> Passport에서 여러 사용자 프로바이더를 사용할 때는 [비밀번호 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달하기 (Passing The Access Token)

Passport로 보호된 라우트 호출 시, API 이용자는 HTTP 요청의 `Authorization` 헤더에 액세스 토큰을 `Bearer` 토큰 형태로 포함해야 합니다. 예를 들어 Guzzle HTTP 클라이언트 사용 시:

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

스코프는 API 클라이언트가 계정 접근 권한 요청 시 특정 권한 범위를 제한할 수 있게 합니다. 예를 들어, 이커머스 앱에서 모든 API 사용자가 주문을 처리할 필요는 없으나 배송 상태 조회 권한만 요청할 수 있도록 제한할 수 있습니다. 즉, 스코프를 통해 제3자 애플리케이션이 사용자를 대신해 수행할 수 있는 행위를 제한할 수 있습니다.

<a name="defining-scopes"></a>
### 스코프 정의하기 (Defining Scopes)

API 스코프는 `App\Providers\AuthServiceProvider` 클래스 `boot` 메서드에서 `Passport::tokensCan` 메서드로 정의할 수 있습니다. 이 메서드는 스코프 이름과 이를 설명하는 문자열을 배열 형태로 받습니다. 설명은 권한 승인 화면에 표시됩니다:

```php
/**
 * 인증 / 인가 서비스 등록
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::routes();

    Passport::tokensCan([
        'place-orders' => 'Place orders',
        'check-status' => 'Check order status',
    ]);
}
```

<a name="default-scope"></a>
### 기본 스코프 (Default Scope)

클라이언트가 특정 스코프를 요청하지 않은 경우, 기본 스코프를 토큰에 붙이도록 Passport 서버를 설정할 수 있습니다. `setDefaultScope` 메서드를 보통 `App\Providers\AuthServiceProvider` 클래스 내 `boot`에서 호출하세요:

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

<a name="assigning-scopes-to-tokens"></a>
### 토큰에 스코프 할당하기 (Assigning Scopes To Tokens)

<a name="when-requesting-authorization-codes"></a>
#### 인증 코드 요청 시 (When Requesting Authorization Codes)

인증 코드 그랜트로 액세스 토큰을 요청할 때는 `scope` 쿼리 파라미터에 원하는 스코프를 스페이스로 구분하여 지정해야 합니다:

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

`App\Models\User` 모델의 `createToken` 메서드로 개인 액세스 토큰을 생성할 때 두 번째 인자로 스코프 배열을 넘겨 지정할 수 있습니다:

```php
$token = $user->createToken('My Token', ['place-orders'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 체크하기 (Checking Scopes)

Passport는 토큰에 부여된 스코프 유무를 검사하는 두 가지 미들웨어를 제공합니다. 먼저 `app/Http/Kernel.php`의 `$routeMiddleware`에 아래를 추가하세요:

```php
'scopes' => \Laravel\Passport\Http\Middleware\CheckScopes::class,
'scope' => \Laravel\Passport\Http\Middleware\CheckForAnyScope::class,
```

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인하기 (Check For All Scopes)

`scopes` 미들웨어는 해당 토큰이 나열된 모든 스코프를 갖고 있는지 검사합니다:

```php
Route::get('/orders', function () {
    // 액세스 토큰이 "check-status" 와 "place-orders" 스코프를 모두 가지고 있음
})->middleware(['auth:api', 'scopes:check-status,place-orders']);
```

<a name="check-for-any-scopes"></a>
#### 하나 이상의 스코프 확인하기 (Check For Any Scopes)

`scope` 미들웨어는 토큰이 나열된 스코프 중 하나라도 포함하고 있는지 확인합니다:

```php
Route::get('/orders', function () {
    // 액세스 토큰이 "check-status" 또는 "place-orders" 스코프 중 하나라도 가짐
})->middleware(['auth:api', 'scope:check-status,place-orders']);
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인하기 (Checking Scopes On A Token Instance)

토큰 인증 요청이 애플리케이션에 진입한 후, `tokenCan` 메서드로 토큰에 특정 스코프가 있는지 검증할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('place-orders')) {
        //
    }
});
```

<a name="additional-scope-methods"></a>
#### 추가 스코프 메서드 (Additional Scope Methods)

`scopeIds` 메서드는 정의된 모든 스코프 ID 또는 이름 배열을 반환합니다:

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

`scopes` 메서드는 `Laravel\Passport\Scope` 인스턴스로 이루어진 모든 스코프 배열을 반환합니다:

```php
Passport::scopes();
```

`scopesFor` 메서드는 ID 또는 이름 배열과 일치하는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다:

```php
Passport::scopesFor(['place-orders', 'check-status']);
```

`hasScope` 메서드로 특정 스코프가 정의되어 있는지 확인할 수 있습니다:

```php
Passport::hasScope('place-orders');
```

<a name="consuming-your-api-with-javascript"></a>
## JavaScript로 API 사용하기 (Consuming Your API With JavaScript)

API를 개발할 때, 자바스크립트 애플리케이션에서 직접 API를 사용하면 편리합니다. 이렇게 하면 웹, 모바일, 서드파티 앱, SDK 등 여러 클라이언트가 동일한 API를 사용할 수 있습니다.

일반적으로 자바스크립트 앱에 액세스 토큰을 수동으로 전달해야 하지만, Passport는 이를 처리해주는 미들웨어를 제공합니다. `app/Http/Kernel.php`에서 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어를 추가하세요:

```php
'web' => [
    // 다른 미들웨어...
    \Laravel\Passport\Http\Middleware\CreateFreshApiToken::class,
],
```

> [!NOTE]
> `CreateFreshApiToken` 미들웨어는 미들웨어 스택의 가장 마지막에 위치시켜야 합니다.

이 미들웨어는 응답에 `laravel_token` 쿠키를 첨부합니다. 이 쿠키는 암호화된 JWT를 포함하고 있으며, Passport는 이를 통해 자바스크립트 앱의 API 요청을 인증합니다. JWT 만료 시간은 `session.lifetime` 설정값과 같습니다. 브라우저가 자동으로 쿠키를 전송하므로, 별도로 액세스 토큰을 전달하지 않아도 요청을 수행할 수 있습니다:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 변경하기 (Customizing The Cookie Name)

필요 시 `Passport::cookie` 메서드로 `laravel_token` 쿠키 이름을 변경할 수 있습니다. 보통 `App\Providers\AuthServiceProvider` 클래스 `boot` 메서드에서 호출하세요:

```php
/**
 * 인증 / 인가 서비스 등록
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Passport::routes();

    Passport::cookie('custom_name');
}
```

<a name="csrf-protection"></a>
#### CSRF 보호 (CSRF Protection)

이 인증 방식 사용 시 요청에 유효한 CSRF 토큰 헤더가 포함되어야 합니다. 기본 Laravel JavaScript 스캐폴딩은 Axios 인스턴스를 포함하며, 암호화된 `XSRF-TOKEN` 쿠키 값을 읽어 자동으로 동일 출처 요청에 `X-XSRF-TOKEN` 헤더를 삽입합니다.

> [!TIP]
> `X-CSRF-TOKEN` 헤더를 직접 사용할 경우, `csrf_token()` 함수로 만든 비암호화 토큰을 사용해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

Passport는 액세스 토큰 및 리프레시 토큰 발급 시 이벤트를 발행합니다. 이 이벤트를 사용해 데이터베이스에서 오래된 토큰을 정리하거나 폐기할 수 있습니다. 이벤트 리스너는 `App\Providers\EventServiceProvider` 클래스에서 등록할 수 있습니다:

```php
/**
 * 이벤트와 리스너 매핑
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
## 테스트하기 (Testing)

Passport의 `actingAs` 메서드는 현재 인증된 사용자와 해당 토큰에 부여할 스코프를 지정할 때 사용합니다. 첫 번째 인자는 사용자 인스턴스, 두 번째는 허용할 스코프 배열입니다:

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

`actingAsClient` 메서드는 현재 인증된 클라이언트와 부여할 스코프를 지정할 때 사용합니다:

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