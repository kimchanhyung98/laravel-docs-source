# Laravel Passport

- [소개](#introduction)
    - [Passport 또는 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [마이그레이션 커스터마이징](#migration-customization)
    - [Passport 업그레이드](#upgrading-passport)
- [설정](#configuration)
    - [클라이언트 시크릿 해싱](#client-secret-hashing)
    - [토큰 수명 설정](#token-lifetimes)
    - [기본 모델 오버라이드](#overriding-default-models)
- [액세스 토큰 발급](#issuing-access-tokens)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청](#requesting-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [PKCE를 이용한 권한 코드 그랜트](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청](#requesting-auth-pkce-grant-tokens)
- [패스워드 그랜트 토큰](#password-grant-tokens)
    - [패스워드 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [유저 프로바이더 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [패스워드 검증 커스터마이징](#customizing-the-password-validation)
- [임플리시트 그랜트 토큰](#implicit-grant-tokens)
- [클라이언트 크리덴셜 그랜트 토큰](#client-credentials-grant-tokens)
- [퍼스널 액세스 토큰](#personal-access-tokens)
    - [퍼스널 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [퍼스널 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호](#protecting-routes)
    - [미들웨어 사용](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당](#assigning-scopes-to-tokens)
    - [스코프 확인](#checking-scopes)
- [JavaScript로 API 소비하기](#consuming-your-api-with-javascript)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Passport](https://github.com/laravel/passport)는 여러분의 Laravel 애플리케이션에 완전한 OAuth2 서버 구현을 몇 분 안에 제공합니다. Passport는 Andy Millington, Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server) 위에 구축되어 있습니다.

> {note} 이 문서는 여러분이 OAuth2에 대해 이미 알고 있다는 것을 전제로 합니다. OAuth2를 잘 모른다면, 계속 읽기 전에 [용어](https://oauth2.thephpleague.com/terminology/) 및 OAuth2의 일반적인 기능에 대해 익혀두는 것을 추천합니다.

<a name="passport-or-sanctum"></a>
### Passport 또는 Sanctum?

시작에 앞서, 여러분의 애플리케이션이 Laravel Passport가 더 적합한지, 아니면 [Laravel Sanctum](/docs/{{version}}/sanctum)이 더 적합한지 결정해야 할 수도 있습니다. 애플리케이션이 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용해야 합니다.

하지만 싱글 페이지 애플리케이션, 모바일 애플리케이션 인증 또는 API 토큰 발급이 목적이라면 [Laravel Sanctum](/docs/{{version}}/sanctum)을 사용하는 것이 좋습니다. Sanctum은 OAuth2를 지원하지 않지만 더 단순한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 통해 Passport를 설치하세요:

    composer require laravel/passport

Passport의 [서비스 프로바이더](/docs/{{version}}/providers)는 자체 마이그레이션 디렉터리를 등록합니다. 패키지 설치 후 데이터베이스 마이그레이션을 실행해야 합니다. Passport 마이그레이션은 OAuth2 클라이언트 및 액세스 토큰 저장에 필요한 테이블을 생성합니다.

    php artisan migrate

그 다음, `passport:install` Artisan 명령어를 실행해야 합니다. 이 명령어는 보안 액세스 토큰 생성을 위한 암호화 키를 생성합니다. 또한 이 명령어는 "퍼스널 액세스" 및 "패스워드 그랜트" 클라이언트도 생성해줍니다.

    php artisan passport:install

> {tip} Passport의 `Client` 모델의 기본키를 auto-increment가 아닌 UUID로 사용하려면 [uuids 옵션](#client-uuids)을 참고하세요.

`passport:install` 명령 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트를 추가합니다. 이 트레이트는 인증된 사용자의 토큰 및 스코프를 조회할 수 있는 헬퍼 메서드를 제공합니다. 이미 `Laravel\Sanctum\HasApiTokens` 트레이트가 있다면 제거해도 됩니다.

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

그 다음, `App\Providers\AuthServiceProvider`의 `boot` 메서드에서 `Passport::routes`를 호출합니다. 이 메서드는 액세스 토큰, 개인 액세스 토큰 발급 및 토큰 폐기를 위한 라우트를 등록합니다.

```php
<?php

namespace App\Providers;

use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Gate;
use Laravel\Passport\Passport;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * The policy mappings for the application.
     *
     * @var array
     */
    protected $policies = [
        'App\Models\Model' => 'App\Policies\ModelPolicy',
    ];

    /**
     * Register any authentication / authorization services.
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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드의 `driver` 옵션을 `passport`로 설정해야 합니다. 이렇게 하면 Passport의 `TokenGuard`가 API 요청 인증에 사용됩니다.

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
#### 클라이언트 UUID 지원

`passport:install` 명령을 `--uuids` 옵션과 함께 실행할 수도 있습니다. 이 옵션은 Passport의 `Client` 모델의 기본키를 auto-increment 정수 대신 UUID로 사용하게 합니다. `--uuids` 옵션과 함께 명령을 실행하면, Passport 기본 마이그레이션 비활성화 안내도 제공합니다:

    php artisan passport:install --uuids

<a name="deploying-passport"></a>
### Passport 배포하기

Passport를 처음 서버에 배포할 때는 `passport:keys` 명령을 실행해야 할 수 있습니다. 이 명령은 액세스 토큰 발급에 필요한 암호화 키를 생성합니다. 생성된 키는 보통 소스 관리에 포함하지 않습니다:

    php artisan passport:keys

필요하다면 Passport의 키를 불러올 경로를 지정할 수 있습니다. 이를 위해 `Passport::loadKeysFrom` 메서드를 사용할 수 있습니다. 이 메서드는 보통 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```php
/**
 * Register any authentication / authorization services.
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
#### 환경 변수에서 키 불러오기

또는 `vendor:publish` Artisan 명령으로 Passport 설정 파일을 배포할 수 있습니다.

    php artisan vendor:publish --tag=passport-config

설정 파일이 배포된 뒤, 아래와 같이 환경 변수로 암호화 키를 지정할 수 있습니다.

```bash
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="migration-customization"></a>
### 마이그레이션 커스터마이징

Passport의 기본 마이그레이션을 사용하지 않을 경우, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Passport::ignoreMigrations`를 호출하세요. 기본 마이그레이션은 아래 명령으로 내보낼 수 있습니다.

    php artisan vendor:publish --tag=passport-migrations

<a name="upgrading-passport"></a>
### Passport 업그레이드

Passport의 주요 버전을 업그레이드할 때는 항상 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼히 검토해야 합니다.

<a name="configuration"></a>
## 설정

<a name="client-secret-hashing"></a>
### 클라이언트 시크릿 해싱

클라이언트의 시크릿을 데이터베이스에 저장할 때 해싱하고 싶다면, `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `Passport::hashClientSecrets`를 호출하세요.

```php
use Laravel\Passport\Passport;

Passport::hashClientSecrets();
```

해싱이 활성화되면, 클라이언트 시크릿은 생성 직후에만 사용자에게 표기됩니다. 평문 시크릿이 데이터베이스에 저장되지 않으므로, 시크릿을 분실하면 값을 복구할 수 없습니다.

<a name="token-lifetimes"></a>
### 토큰 수명 설정

기본적으로 Passport는 1년 후 만료되는 장수명 액세스 토큰을 발급합니다. 만약 더 긴/짧은 토큰 수명을 설정하고자 한다면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 보통 `App\Providers\AuthServiceProvider`의 `boot` 메서드에 아래처럼 추가합니다.

```php
/**
 * Register any authentication / authorization services.
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

> {note} Passport 테이블의 `expires_at` 컬럼은 읽기 전용(디스플레이 용도)입니다. 토큰 발급시, Passport는 만료 정보를 서명/암호화된 토큰 내부에 저장합니다. 토큰 무효화가 필요하다면 [토큰 폐기](#revoking-tokens)를 이용하세요.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

Passport가 내부적으로 사용하는 모델을 자유롭게 커스터마이징할 수 있습니다. 모델을 정의하고 Passport 모델을 상속하세요.

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 만들었으면, `Laravel\Passport\Passport`에서 직접 사용할 수 있도록 등록해야 합니다. 보통 `App\Providers\AuthServiceProvider`의 `boot` 메서드에서 지정합니다.

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\PersonalAccessClient;
use App\Models\Passport\Token;

/**
 * Register any authentication / authorization services.
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

---

(분량 문제로 인해 라인 수 제한에 의해 중단됩니다. 전체 요청이 매우 길기 때문에, 추가 분량 요청 시 이어서 번역 드릴 수 있습니다. 필요하신 부분이나 이어서 원하시면 말씀해주세요!)