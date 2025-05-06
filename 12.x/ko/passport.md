# Laravel Passport

- [소개](#introduction)
    - [Passport 또는 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [Passport 업그레이드](#upgrading-passport)
- [구성](#configuration)
    - [토큰 수명](#token-lifetimes)
    - [기본 모델 재정의](#overriding-default-models)
    - [라우트 재정의](#overriding-routes)
- [인증 코드 그랜트](#authorization-code-grant)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청](#requesting-tokens)
    - [토큰 관리](#managing-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [PKCE와 함께하는 인증 코드 그랜트](#code-grant-pkce)
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
- [임플리시트 그랜트](#implicit-grant)
- [클라이언트 크레덴셜 그랜트](#client-credentials-grant)
- [개인용 액세스 토큰](#personal-access-tokens)
    - [개인용 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [User Provider 커스터마이징](#customizing-the-user-provider-for-pat)
    - [개인용 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어를 통한 보호](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
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

[Laravel Passport](https://github.com/laravel/passport)는 몇 분 만에 Laravel 애플리케이션에 완전한 OAuth2 서버 구현을 제공합니다. Passport는 Andy Millington과 Simon Hamp가 유지보수하는 [League OAuth2 서버](https://github.com/thephpleague/oauth2-server) 위에 구축되었습니다.

> [!NOTE]
> 이 문서에서는 이미 OAuth2에 익숙하다고 가정합니다. OAuth2에 대해 잘 모른다면, 계속 읽기 전에 일반적인 [용어](https://oauth2.thephpleague.com/terminology/)와 OAuth2의 기능을 먼저 익혀보세요.

<a name="passport-or-sanctum"></a>
### Passport 또는 Sanctum?

시작하기 전에, Laravel Passport 또는 [Laravel Sanctum](/docs/{{version}}/sanctum) 중 어느 것이 애플리케이션에 더 적합한지 결정하는 것이 좋습니다. 애플리케이션이 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용해야 합니다.

그러나, 싱글 페이지 애플리케이션(SPA), 모바일 앱, 또는 API 토큰 발급이 목적이라면 [Laravel Sanctum](/docs/{{version}}/sanctum)을 사용하는 것이 좋습니다. Laravel Sanctum은 OAuth2를 지원하지 않지만, 훨씬 간단한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치

`install:api` 아티즌 명령어를 통해 Laravel Passport를 설치할 수 있습니다:

```shell
php artisan install:api --passport
```

이 명령은 OAuth2 클라이언트와 액세스 토큰을 저장하는 데 필요한 데이터베이스 마이그레이션을 게시 및 실행합니다. 또한 보안 액세스 토큰 생성을 위한 암호화 키도 생성됩니다.

`install:api` 명령 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가하세요. 이 트레이트는 인증된 사용자의 토큰과 스코프를 점검하는 헬퍼 메서드를 제공합니다.

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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고 `driver` 옵션을 `passport`로 설정하세요. 이를 통해 들어오는 API 요청 인증 시 Passport의 `TokenGuard`를 사용하게 됩니다.

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

처음으로 애플리케이션 서버에 Passport를 배포할 때는 `passport:keys` 명령을 실행해야 할 수 있습니다. 이 명령은 액세스 토큰 생성을 위한 Passport의 암호화 키를 생성합니다. 생성된 키는 보통 소스 제어에 포함하지 않습니다.

```shell
php artisan passport:keys
```

필요하다면, Passport 키가 로드될 경로를 직접 지정할 수 있습니다. `Passport::loadKeysFrom` 메서드를 사용하면 됩니다. 보통 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출됩니다.

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
#### 환경변수에서 키 로딩하기

또는, `vendor:publish` 아티즌 명령으로 Passport의 설정 파일을 게시할 수 있습니다.

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일이 게시된 후에는 환경 변수로 암호화 키를 지정할 수 있습니다:

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

Passport의 새 주요 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 반드시 주의 깊게 확인하세요.

<a name="configuration"></a>
## 구성

<a name="token-lifetimes"></a>
### 토큰 수명

Passport는 기본적으로 1년 후 만료되는 장기 액세스 토큰을 발급합니다. 토큰의 만료 기간을 더 길게/짧게 설정하고 싶다면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출하세요.

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
> Passport 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며 표시용입니다. 토큰 발급 시 만료 정보는 서명, 암호화된 토큰 내에 저장됩니다. 토큰을 무효화하려면 반드시 [폐기(revoke)](#revoking-tokens) 하세요.

<a name="overriding-default-models"></a>
### 기본 모델 재정의

Passport가 내부적으로 사용하는 모델들은 자유롭게 확장할 수 있습니다. 직접 모델을 작성하여 해당 Passport 모델을 상속하세요.

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의한 후, `Laravel\Passport\Passport` 클래스를 통해 Passport가 당신의 커스텀 모델을 사용하도록 지시할 수 있습니다. 보통 이 코드는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 추가합니다.

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
    Passport::useDeviceCodeModel(DeviceCode::class);
}
```

<a name="overriding-routes"></a>
### 라우트 재정의

때론 Passport가 정의한 기본 라우트를 커스터마이징하고 싶을 수 있습니다. 이럴 땐, 우선 `AppServiceProvider`의 `register` 메서드에 `Passport::ignoreRoutes`를 추가해 Passport의 라우트 등록을 비활성화하세요.

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

그런 다음, [Passport의 라우트 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 애플리케이션의 `routes/web.php`로 복사한 후 원하는 대로 수정합니다.

```php
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => '\Laravel\Passport\Http\Controllers',
], function () {
    // Passport 라우트...
});
```

<a name="authorization-code-grant"></a>
## 인증 코드 그랜트

개발자들이 가장 익숙한 OAuth2 방식은 인증 코드 그랜트입니다. 인증 코드 사용 시, 클라이언트 애플리케이션은 사용자를 서버로 리다이렉트하여 접근 토큰 발급 요청을 승인 또는 거부하게 만듭니다.

먼저 Passport가 "authorization" 뷰를 반환하는 방법을 지정해야 합니다.

모든 권한 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스의 관련 메서드로 커스터마이즈할 수 있습니다. 일반적으로는 이 메서드를 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름 전달
    Passport::authorizationView('auth.oauth.authorize');
    
    // 클로저 전달
    Passport::authorizationView(fn ($parameters) => Inertia::render('Auth/OAuth/Authorize', [
        'request' => $parameters['request'],
        'authToken' => $parameters['authToken'],
        'client' => $parameters['client'],
        'user' => $parameters['user'],
        'scopes' => $parameters['scopes'],
    ]));
}
```

Passport는 `/oauth/authorize` 라우트를 자동으로 정의하게 되며, 이 라우트는 위에서 지정한 뷰를 반환합니다. `auth.oauth.authorize` 템플릿에는 권한 승인을 위한 `passport.authorizations.approve`(POST)와 거부를 위한 `passport.authorizations.deny`(DELETE)의 두 라우트로 요청하는 폼이 들어 있어야 합니다. 이 라우트들은 `state`, `client_id`, `auth_token` 필드를 기대합니다.

<a name="managing-clients"></a>
### 클라이언트 관리

API와 상호작용해야 하는 애플리케이션을 개발하는 개발자는 "클라이언트"를 생성하여 당신의 애플리케이션에 등록해야 합니다. 일반적으로 애플리케이션 이름과 사용자가 접근권한을 승인한 후 리다이렉트할 URI를 제공합니다.

<a name="managing-first-party-clients"></a>
#### 1차 클라이언트(자사 앱)

가장 간단한 클라이언트 생성 방법은 `passport:client` 아티즌 명령어를 사용하는 것입니다. 이 명령은 1차 클라이언트나 OAuth2 기능 테스트에 사용할 수 있습니다. 명령 실행 시 클라이언트 정보가 프롬프트되고, 클라이언트 ID와 시크릿이 제공됩니다.

```shell
php artisan passport:client
```

클라이언트에 여러 리다이렉트 URI를 지정하고 싶다면, 쉼표로 구분된 URI 목록을 입력하세요. 만약 URI에 쉼표가 있으면 URI 인코딩하세요.

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 3차 클라이언트(타사 앱)

애플리케이션 사용자는 `passport:client` 명령을 직접 사용할 수 없으므로, `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드를 통해 사용자별로 클라이언트를 등록할 수 있습니다.

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// 주어진 사용자 소유의 OAuth 앱 클라이언트 생성
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// 해당 사용자가 소유한 모든 OAuth 앱 클라이언트 가져오기
$clients = $user->oauthApps()->get();
```

`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. 사용자에게 `$client->id`(클라이언트 ID)와 `$client->plainSecret`(클라이언트 시크릿)을 표시하면 됩니다.

<a name="requesting-tokens"></a>
### 토큰 요청

...

---

**[아래 내용은 분량상 일부 생략합니다. 계속 요청 시 이어서 번역해드릴 수 있습니다.]**

---

*(나머지 이어서 필요하시면 말씀해 주세요!)*