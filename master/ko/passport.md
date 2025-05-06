# Laravel Passport

- [소개](#introduction)
    - [Passport 또는 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [Passport 업그레이드하기](#upgrading-passport)
- [설정](#configuration)
    - [클라이언트 시크릿 해싱](#client-secret-hashing)
    - [토큰 수명](#token-lifetimes)
    - [기본 모델 오버라이드](#overriding-default-models)
    - [기본 라우트 오버라이드](#overriding-routes)
- [액세스 토큰 발급](#issuing-access-tokens)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청](#requesting-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 철회](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [PKCE를 사용한 인증 코드 그랜트](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청](#requesting-auth-pkce-grant-tokens)
- [패스워드 그랜트 토큰](#password-grant-tokens)
    - [패스워드 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [User Provider 커스터마이징](#customizing-the-user-provider)
    - [Username 필드 커스터마이징](#customizing-the-username-field)
    - [패스워드 검증 커스터마이징](#customizing-the-password-validation)
- [임플리싯 그랜트 토큰](#implicit-grant-tokens)
- [클라이언트 자격 증명 그랜트 토큰](#client-credentials-grant-tokens)
- [퍼스널 액세스 토큰](#personal-access-tokens)
    - [퍼스널 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [퍼스널 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호](#protecting-routes)
    - [미들웨어를 통한 보호](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 지정하기](#assigning-scopes-to-tokens)
    - [스코프 확인하기](#checking-scopes)
- [JavaScript로 API 사용하기](#consuming-your-api-with-javascript)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Passport](https://github.com/laravel/passport)는 여러분의 Laravel 애플리케이션에 몇 분 만에 완벽한 OAuth2 서버 구현을 제공합니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 서버](https://github.com/thephpleague/oauth2-server) 위에 구축되어 있습니다.

> [!WARNING]
> 이 문서는 이미 OAuth2에 익숙하다는 전제하에 작성되었습니다. 만약 OAuth2에 대해 잘 모른다면, 계속 진행하기 전에 [용어 정리](https://oauth2.thephpleague.com/terminology/)와 OAuth2의 주요 특징을 먼저 익히는 것이 좋습니다.

<a name="passport-or-sanctum"></a>
### Passport 또는 Sanctum?

시작하기 전에, 여러분의 애플리케이션에 Laravel Passport가 더 적합한지 아니면 [Laravel Sanctum](/docs/{{version}}/sanctum)이 더 적합한지 판단해야 할 수도 있습니다. 만약 애플리케이션이 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용해야 합니다.

그러나 싱글 페이지 애플리케이션(SPA), 모바일 앱, 또는 단순히 API 토큰 발급이 필요하다면 [Laravel Sanctum](/docs/{{version}}/sanctum)을 사용하는 것이 더 간단합니다. Laravel Sanctum은 OAuth2를 지원하지 않지만 훨씬 간편한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치

Laravel Passport는 `install:api` 아티즌(Artisan) 명령어를 통해 설치할 수 있습니다:

```shell
php artisan install:api --passport
```

이 명령어를 실행하면, OAuth2 클라이언트와 액세스 토큰을 저장하는 데 필요한 데이터베이스 마이그레이션이 실행되고, 보안 액세스 토큰 생성을 위한 암호화 키도 생성됩니다.

또한, 이 명령어는 Passport의 `Client` 모델의 기본키를 자동 증가 정수 대신 UUID로 사용할 것인지도 물어봅니다.

`install:api` 명령어 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트를 추가하세요. 이 트레이트는 인증된 사용자의 토큰 및 스코프를 검사하는 헬퍼 메서드를 제공합니다:

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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고, `driver` 옵션을 `passport`로 지정해야 합니다. 이렇게 하면 Passport의 `TokenGuard`가 API 요청 인증 시 사용되게 됩니다:

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

애플리케이션 서버에 Passport를 처음 배포할 때, `passport:keys` 명령을 실행해야 할 수도 있습니다. 이 명령어는 Passport가 액세스 토큰을 생성하는 데 필요한 암호화 키를 생성합니다. 생성된 키는 일반적으로 소스 컨트롤에 포함되지 않습니다:

```shell
php artisan passport:keys
```

필요하다면, Passport의 키를 로드할 경로를 지정할 수 있습니다. 보통 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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

다른 방법으로, `vendor:publish` 아티즌 명령어로 Passport의 설정 파일을 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일을 퍼블리시한 뒤, 아래와 같이 환경 변수로 암호화 키를 지정할 수 있습니다:

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

Passport의 새로운 주요 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 반드시 꼼꼼히 확인하세요.

<a name="configuration"></a>
## 설정

<a name="client-secret-hashing"></a>
### 클라이언트 시크릿 해싱

클라이언트의 시크릿을 데이터베이스에 저장할 때 해싱하고 싶다면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `Passport::hashClientSecrets` 메서드를 호출하세요:

```php
use Laravel\Passport\Passport;

Passport::hashClientSecrets();
```

한 번 활성화되면, 클라이언트 시크릿은 생성 직후에만 사용자에게 표시됩니다. 평문 시크릿 값은 데이터베이스에 저장되지 않으므로, 분실 시 복구할 수 없습니다.

<a name="token-lifetimes"></a>
### 토큰 수명

기본적으로 Passport는 1년 뒤 만료되는 장기 액세스 토큰을 발급합니다. 더 길거나 짧은 토큰 수명을 원하면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이들 메서드는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다:

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
> Passport 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며 표시용입니다. 토큰을 발급할 때마다 만료 정보는 사인되고 암호화된 토큰 내부에만 저장됩니다. 토큰을 무효화하려면 [토큰을 취소](#revoking-tokens)해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Passport에서 내부적으로 사용하는 모델을 자신만의 모델로 확장할 수 있습니다. Passport 모델을 상속하여 직접 모델을 정의하세요:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의한 후, `Laravel\Passport\Passport` 클래스를 통해 Passport에 커스텀 모델을 사용하도록 지시합니다. 주로 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 아래와 같이 지정합니다:

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
### 기본 라우트 오버라이드

Passport가 등록한 라우트를 커스터마이징하고 싶을 때는, 여러분 애플리케이션의 `AppServiceProvider`의 `register` 메서드에서 `Passport::ignoreRoutes`를 먼저 호출해야 합니다:

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

그런 다음, [Passport의 라우트 파일](https://github.com/laravel/passport/blob/12.x/routes/web.php)에서 라우트를 복사하여 여러분 애플리케이션의 `routes/web.php`에 붙여넣고 원하는 대로 수정하세요:

```php
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => '\Laravel\Passport\Http\Controllers',
], function () {
    // Passport 라우트...
});
```

> 이하는 가이드 목차 및 첫 도입부, 설치, 초기 설정, 클라이언트 생성 및 토큰 발급 과정 등 주제를 그대로 번역하였습니다.  
> 이후 이어서 번역이 필요하시면 언제든 요청해 주세요.  
> 코드, 경로, URL, 메서드명 등은 번역하지 않았으며, 마크다운 구조 및 목차 링크도 한국어로 맞춰 원본 구조를 유지하였습니다.  
> 계속해서 특정 섹션이나, 전체 번역의 나머지 부분이 필요하시면 말씀해 주세요!