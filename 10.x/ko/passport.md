# Laravel Passport

- [소개](#introduction)
    - [Passport 또는 Sanctum?](#passport-or-sanctum)
- [설치하기](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [마이그레이션 커스터마이징](#migration-customization)
    - [Passport 업그레이드](#upgrading-passport)
- [설정](#configuration)
    - [클라이언트 시크릿 해싱](#client-secret-hashing)
    - [토큰 수명](#token-lifetimes)
    - [기본 모델 오버라이드](#overriding-default-models)
    - [라우트 오버라이드](#overriding-routes)
- [액세스 토큰 발급](#issuing-access-tokens)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청하기](#requesting-tokens)
    - [토큰 갱신하기](#refreshing-tokens)
    - [토큰 폐기하기](#revoking-tokens)
    - [토큰 정리하기](#purging-tokens)
- [PKCE가 포함된 인증 코드 그랜트](#code-grant-pkce)
    - [클라이언트 생성하기](#creating-a-auth-pkce-grant-client)
    - [토큰 요청하기](#requesting-auth-pkce-grant-tokens)
- [패스워드 그랜트 토큰](#password-grant-tokens)
    - [패스워드 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청하기](#requesting-password-grant-tokens)
    - [모든 스코프 요청하기](#requesting-all-scopes)
    - [User Provider 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 커스터마이징](#customizing-the-password-validation)
- [암시적 그랜트 토큰](#implicit-grant-tokens)
- [클라이언트 크레덴셜 그랜트 토큰](#client-credentials-grant-tokens)
- [개인 액세스 토큰](#personal-access-tokens)
    - [개인 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [개인 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어로 보호](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의하기](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당](#assigning-scopes-to-tokens)
    - [스코프 확인](#checking-scopes)
- [자바스크립트로 API 소비하기](#consuming-your-api-with-javascript)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Passport](https://github.com/laravel/passport)는 여러분의 Laravel 애플리케이션에 몇 분 만에 완전한 OAuth2 서버 구현을 제공합니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server) 위에 구축되었습니다.

> [!WARNING]  
> 이 문서는 이미 OAuth2에 익숙하다는 전제 하에 작성되었습니다. OAuth2에 대해 잘 모른다면 일반적인 [용어](https://oauth2.thephpleague.com/terminology/)와 OAuth2 기능을 먼저 학습하시는 것을 추천합니다.

<a name="passport-or-sanctum"></a>
### Passport 또는 Sanctum?

시작하기 전에, 여러분의 애플리케이션에 Laravel Passport와 [Laravel Sanctum](/docs/{{version}}/sanctum) 중 어떤 것이 더 적합한지 판단할 수 있습니다. 애플리케이션이 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용해야 합니다.

하지만 단일 페이지 애플리케이션(SPA), 모바일 애플리케이션, 또는 단순히 API 토큰 발급이 목적이라면 [Laravel Sanctum](/docs/{{version}}/sanctum)을 사용하는 것이 좋습니다. Sanctum은 OAuth2를 지원하지 않지만, 훨씬 단순한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치하기

시작하려면 Composer 패키지 관리자를 통해 Passport를 설치하세요:

```shell
composer require laravel/passport
```

Passport의 [서비스 프로바이더](/docs/{{version}}/providers)는 자체 데이터베이스 마이그레이션 디렉터리를 등록하므로, 패키지 설치 후 데이터베이스를 마이그레이트해야 합니다. Passport 마이그레이션은 OAuth2 클라이언트와 액세스 토큰을 저장하는 데 필요한 테이블을 만듭니다.

```shell
php artisan migrate
```

다음으로 `passport:install` Artisan 명령어를 실행해야 합니다. 이 명령어는 안전한 액세스 토큰 생성을 위한 암호화 키를 만듭니다. 그리고 "개인 액세스" 및 "패스워드 그랜트" 클라이언트도 함께 생성합니다:

```shell
php artisan passport:install
```

> [!NOTE]  
> 만약 Passport의 `Client` 모델의 기본 키 값을 자동 증가 정수 대신 UUID로 사용하고 싶다면, [`uuids` 옵션](#client-uuids)을 사용하여 설치하세요.

`passport:install` 명령 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트를 추가하세요. 이 트레이트는 인증된 사용자의 토큰 및 스코프를 확인할 수 있는 유틸리티 메서드를 제공해줍니다. 만약 이미 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용 중이라면 제거해도 됩니다:

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

마지막으로 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고, `driver` 옵션을 `passport`로 설정하세요. 이렇게 하면 API 요청 인증시 Passport의 `TokenGuard`를 사용하도록 지정됩니다:

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

<a name="client-uuids"></a>
#### 클라이언트 UUIDs

`passport:install` 명령에 `--uuids` 옵션을 줄 수도 있습니다. 이 옵션을 사용하면 Passport의 `Client` 모델의 기본 키가 자동 증가 정수 대신 UUID로 설정됩니다. 이 옵션으로 설치 후, Passport의 기본 마이그레이션 비활성화 방법에 대한 추가 안내가 제공됩니다:

```shell
php artisan passport:install --uuids
```

<a name="deploying-passport"></a>
### Passport 배포하기

애플리케이션 서버에 처음으로 Passport를 배포할 때는 `passport:keys` 명령을 실행해야 할 수 있습니다. 이 명령은 Passport가 액세스 토큰을 생성하기 위해 필요한 암호화 키를 만듭니다. 생성된 키는 일반적으로 소스 제어에 포함하지 않습니다:

```shell
php artisan passport:keys
```

필요하다면 Passport의 키가 로드될 경로를 정의할 수 있습니다. `Passport::loadKeysFrom` 메서드를 사용하여 구현할 수 있으며, 일반적으로 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

    /**
     * 인증/인가 서비스 등록.
     */
    public function boot(): void
    {
        Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
    }

<a name="loading-keys-from-the-environment"></a>
#### 환경에서 키 불러오기

또는 `vendor:publish` Artisan 명령으로 Passport의 설정 파일을 퍼블리시 할 수도 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일을 퍼블리시한 후, 애플리케이션의 암호화 키를 환경 변수로 정의하여 불러올 수 있습니다:

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

Passport의 기본 마이그레이션을 사용하지 않을 경우, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Passport::ignoreMigrations`를 호출해야 합니다. Passport의 기본 마이그레이션을 `vendor:publish` 명령을 통해 내보낼 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-migrations
```

<a name="upgrading-passport"></a>
### Passport 업그레이드

Passport를 새로운 주요 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼭 참고하세요.

---

*이하 문서도 같은 방식(마크다운 유지, 코드와 링크 제외 번역, 전문용어 유지)을 참고하여 번역 가능합니다! 나머지 필요 부분이 있다면 요청해주세요.*