# Laravel Passport

- [소개](#introduction)
    - [Passport 또는 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포](#deploying-passport)
    - [마이그레이션 커스터마이징](#migration-customization)
    - [Passport 업그레이드](#upgrading-passport)
- [설정](#configuration)
    - [클라이언트 시크릿 해시화](#client-secret-hashing)
    - [토큰 수명](#token-lifetimes)
    - [기본 모델 오버라이딩](#overriding-default-models)
    - [라우트 오버라이딩](#overriding-routes)
- [액세스 토큰 발급](#issuing-access-tokens)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청하기](#requesting-tokens)
    - [토큰 갱신하기](#refreshing-tokens)
    - [토큰 폐기하기](#revoking-tokens)
    - [토큰 정리하기](#purging-tokens)
- [PKCE가 포함된 인증 코드 그랜트](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청하기](#requesting-auth-pkce-grant-tokens)
- [패스워드 그랜트 토큰](#password-grant-tokens)
    - [패스워드 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청하기](#requesting-password-grant-tokens)
    - [모든 스코프 요청하기](#requesting-all-scopes)
    - [유저 프로바이더 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 커스터마이징](#customizing-the-password-validation)
- [임플리싯 그랜트 토큰](#implicit-grant-tokens)
- [클라이언트 크리덴셜 그랜트 토큰](#client-credentials-grant-tokens)
- [퍼스널 액세스 토큰](#personal-access-tokens)
    - [퍼스널 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [퍼스널 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호](#protecting-routes)
    - [미들웨어를 통한 보호](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당](#assigning-scopes-to-tokens)
    - [스코프 확인](#checking-scopes)
- [JavaScript로 API 사용](#consuming-your-api-with-javascript)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Passport](https://github.com/laravel/passport)는 여러분의 Laravel 애플리케이션에 몇 분만에 완전한 OAuth2 서버를 구현할 수 있도록 도와줍니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server) 위에 구축되었습니다.

> **경고**  
> 이 문서는 여러분이 이미 OAuth2에 익숙하다고 가정합니다. OAuth2에 대해 전혀 모른다면 계속하기 전에 [용어](https://oauth2.thephpleague.com/terminology/)와 주요 기능을 익히는 것을 추천합니다.

<a name="passport-or-sanctum"></a>
### Passport 또는 Sanctum?

시작하기 전에, Laravel Passport가 여러분의 애플리케이션에 더 적합한지 아니면 [Laravel Sanctum](/docs/{{version}}/sanctum)이 나은지 결정해야 할 수 있습니다. 반드시 OAuth2 지원이 필요한 경우에는 Laravel Passport를 사용해야 합니다.

하지만 싱글 페이지 애플리케이션(SPA), 모바일 앱 인증, 혹은 API 토큰 발급이 목적이라면 [Laravel Sanctum](/docs/{{version}}/sanctum)을 사용하는 것이 좋습니다. Laravel Sanctum은 OAuth2를 지원하지 않지만, 훨씬 더 간단한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 매니저로 Passport를 설치하세요:

```shell
composer require laravel/passport
```

Passport의 [서비스 프로바이더](/docs/{{version}}/providers)는 자체 데이터베이스 마이그레이션 디렉토리를 등록하므로, 패키지 설치 후 데이터베이스 마이그레이션을 진행해야 합니다. 이 마이그레이션은 OAuth2 클라이언트와 액세스 토큰 정보를 저장할 테이블을 생성합니다:

```shell
php artisan migrate
```

이후 `passport:install` Artisan 명령어를 실행하세요. 이 명령어는 보안 액세스 토큰 생성을 위한 암호화 키를 생성합니다. 또한 "personal access" 및 "password grant" 클라이언트를 생성하여 토큰 발급에 사용됩니다:

```shell
php artisan passport:install
```

> **참고**  
> Passport의 `Client` 모델에서 기본키로 자동 증가 정수 대신 UUID를 사용하려면 [uuids 옵션](#client-uuids)을 참고하세요.

`passport:install` 명령어 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트를 추가해야 합니다. 이 트레이트는 인증된 사용자의 토큰과 스코프를 확인하는 여러 헬퍼 메서드를 제공합니다. 이미 `Laravel\Sanctum\HasApiTokens`를 사용하고 있다면 해당 트레이트를 제거하세요:

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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고, `driver` 옵션을 `passport`로 지정하세요. 이를 통해 API 요청 인증 시 Passport의 `TokenGuard`를 사용하게 됩니다:

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
#### 클라이언트 UUID

`passport:install` 명령어에 `--uuids` 옵션을 사용할 수도 있습니다. 이 옵션은 Passport의 `Client` 모델의 기본키로 자동 증가 대신 UUID를 사용하도록 합니다. `--uuids`와 함께 `passport:install`을 실행하면, Passport 기본 마이그레이션 비활성화와 관련한 추가 안내가 나옵니다:

```shell
php artisan passport:install --uuids
```

<a name="deploying-passport"></a>
### Passport 배포

애플리케이션 서버에 Passport를 처음 배포할 때는 `passport:keys` 명령어를 실행해야 할 수도 있습니다. 이 명령어는 액세스 토큰 생성을 위한 암호화 키를 생성하며, 보통 소스 제어에 포함시키지 않습니다:

```shell
php artisan passport:keys
```

필요하다면 Passport의 키가 불러와질 경로를 지정할 수 있습니다. 보통 이 메서드는 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드 안에서 호출하면 됩니다:

    /**
     * 인증/권한 서비스를 등록합니다.
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
    }

<a name="loading-keys-from-the-environment"></a>
#### 환경 변수에서 키 불러오기

또는 `vendor:publish` Artisan 명령어로 Passport의 설정 파일을 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일을 퍼블리시한 후, 암호화 키를 환경변수로 지정할 수 있습니다:

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

Passport의 기본 마이그레이션을 사용하지 않으려면, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Passport::ignoreMigrations`를 호출하세요. 기본 마이그레이션 파일은 다음 명령어로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-migrations
```

<a name="upgrading-passport"></a>
### Passport 업그레이드

Passport를 새로운 주요 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

<a name="configuration"></a>
## 설정

<a name="client-secret-hashing"></a>
### 클라이언트 시크릿 해시화

클라이언트 시크릿을 데이터베이스에 저장할 때 해시화하고 싶다면, `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `Passport::hashClientSecrets`를 호출하세요:

    use Laravel\Passport\Passport;

    Passport::hashClientSecrets();

이 기능을 활성화하면 모든 클라이언트 시크릿은 생성 직후 사용자에게만 표시됩니다. 평문 시크릿 값은 데이터베이스에 따로 저장되지 않으므로 시크릿을 분실한 경우 복구가 불가합니다.

<a name="token-lifetimes"></a>
### 토큰 수명

기본적으로 Passport는 1년 만료의 장기 액세스 토큰을 발급합니다. 토큰 수명을 더 길게/짧게 설정하려면 `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용하세요. 이 메서드들은 앱의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다:

    /**
     * 인증/권한 서비스를 등록합니다.
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

> **경고**  
> Passport 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며, 표시 용도로만 사용됩니다. 실제 만료 정보는 서명되고 암호화된 토큰 안에 저장됩니다. 토큰을 무효화해야 하는 경우 [폐기(revoke)](#revoking-tokens) 하세요.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이딩

Passport에서 내부적으로 사용하는 모델을 직접 확장하여 사용할 수 있습니다. 자신만의 모델을 만들고, 해당 Passport 모델을 상속하세요:

    use Laravel\Passport\Client as PassportClient;

    class Client extends PassportClient
    {
        // ...
    }

모델을 정의한 후, `Laravel\Passport\Passport` 클래스를 통해 Passport에게 사용자 지정 모델을 사용하도록 알릴 수 있습니다. 보통 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 호출하면 됩니다:

    use App\Models\Passport\AuthCode;
    use App\Models\Passport\Client;
    use App\Models\Passport\PersonalAccessClient;
    use App\Models\Passport\RefreshToken;
    use App\Models\Passport\Token;

    /**
     * 인증/권한 서비스를 등록합니다.
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

<a name="overriding-routes"></a>
### 라우트 오버라이딩

Passport에서 정의된 라우트를 커스터마이징하고 싶은 경우, 우선 애플리케이션의 `AppServiceProvider`의 `register` 메서드에서 `Passport::ignoreRoutes`를 호출해 Passport의 기본 라우트를 무시하세요:

    use Laravel\Passport\Passport;

    /**
     * 애플리케이션 서비스를 등록합니다.
     *
     * @return void
     */
    public function register()
    {
        Passport::ignoreRoutes();
    }

그런 다음, [Passport의 라우트 파일](https://github.com/laravel/passport/blob/11.x/routes/web.php)에 정의된 라우트를 복사하여 직접 원하는 대로 수정해 사용하면 됩니다:

    Route::group([
        'as' => 'passport.',
        'prefix' => config('passport.path', 'oauth'),
        'namespace' => 'Laravel\Passport\Http\Controllers',
    ], function () {
        // Passport routes...
    });

<a name="issuing-access-tokens"></a>
## 액세스 토큰 발급

대부분의 개발자들이 익숙한 OAuth2 방식인 인증 코드(authorization code) 방식으로 사용합니다. 이 방식에서는 클라이언트 애플리케이션이 사용자를 서버로 리디렉션 시키고, 사용자는 액세스 토큰 발급을 승인 또는 거절할 수 있습니다.

<a name="managing-clients"></a>
### 클라이언트 관리

우선, 여러분의 API와 상호작용이 필요한 애플리케이션 개발자들은 "클라이언트"를 등록해야 합니다. 보통 애플리케이션의 이름과 승인 후 리디렉션할 URL을 제공합니다.

<a name="the-passportclient-command"></a>
#### `passport:client` 명령어

가장 간단한 방법은 `passport:client` Artisan 명령어를 활용하는 것입니다. 이 명령어로 직접 테스트용 클라이언트를 만들 수 있습니다. 실행하면 Passport가 필요한 정보를 입력받아 클라이언트 ID와 시크릿을 제공합니다:

```shell
php artisan passport:client
```

**리디렉션 URL 여러 개 설정하기**

클라이언트에 여러 리디렉션 URL을 허용하려면, 명령어 실행 중 URL 입력 시 콤마(,)로 구분하여 입력하면 됩니다. URL에 콤마가 포함되어야 한다면 URL 인코딩 되어야 합니다:

```shell
http://example.com/callback,http://examplefoo.com/callback
```

<a name="clients-json-api"></a>
#### JSON API

애플리케이션 사용자가 직접 `client` 명령어를 사용하는 것은 불가능하므로, Passport는 JSON API로 클라이언트 생성/수정/삭제를 지원합니다.

하지만 이 API를 UI 대시보드와 연결하려면 프론트엔드를 직접 구현해야 합니다. 아래는 모든 클라이언트 API 엔드포인트입니다. 예시로 [Axios](https://github.com/axios/axios)를 사용합니다.

JSON API는 `web` 및 `auth` 미들웨어로 보호되므로, 외부에서는 호출할 수 없으며, 애플리케이션 내부에서만 호출 가능합니다.

...  
(아래 내용도 같은 원칙으로 이어집니다 — **코드, HTML, URL 번역X, 마크다운 구조 유지**)

(문서가 매우 길기 때문에, 모든 항목을 한 번에 번역해드릴 수 없습니다. 이어서 추가적으로 번역이 필요하다면 "이어서"라고 입력해 주세요. 어느 구간까지 번역해드릴까요?)