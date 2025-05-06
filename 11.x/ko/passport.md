# Laravel Passport

- [소개](#introduction)
    - [Passport 또는 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [Passport 업그레이드하기](#upgrading-passport)
- [설정](#configuration)
    - [클라이언트 시크릿 해싱](#client-secret-hashing)
    - [토큰 유효 기간](#token-lifetimes)
    - [기본 모델 오버라이딩](#overriding-default-models)
    - [라우트 오버라이딩](#overriding-routes)
- [액세스 토큰 발급](#issuing-access-tokens)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청](#requesting-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 철회](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [PKCE를 사용한 권한 코드 그랜트](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청](#requesting-auth-pkce-grant-tokens)
- [패스워드 그랜트 토큰](#password-grant-tokens)
    - [패스워드 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [사용자 프로바이더 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 검증 커스터마이징](#customizing-the-password-validation)
- [임플리시트 그랜트 토큰](#implicit-grant-tokens)
- [클라이언트 크리덴셜 그랜트 토큰](#client-credentials-grant-tokens)
- [개인 액세스 토큰](#personal-access-tokens)
    - [개인 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [개인 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호](#protecting-routes)
    - [미들웨어를 통해](#via-middleware)
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

[Laravel Passport](https://github.com/laravel/passport)는 몇 분 만에 Laravel 애플리케이션을 위한 완전한 OAuth2 서버 구현을 제공합니다. Passport는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server)를 기반으로 하며, Andy Millington과 Simon Hamp가 유지 보수합니다.

> [!WARNING]  
> 이 문서에서는 이미 OAuth2에 익숙하다고 가정합니다. 만약 OAuth2에 대해 아무것도 모른다면, 계속 진행하기 전에 [용어](https://oauth2.thephpleague.com/terminology/) 및 OAuth2의 특징을 먼저 숙지하는 것이 좋습니다.

<a name="passport-or-sanctum"></a>
### Passport 또는 Sanctum?

시작하기 전에, 애플리케이션에 Laravel Passport 또는 [Laravel Sanctum](/docs/{{version}}/sanctum) 중 어느 것이 더 적합한지 결정해야 할 수 있습니다. 만약 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용하세요.

그러나 단일 페이지 애플리케이션(SPA), 모바일 애플리케이션 인증 또는 API 토큰 발급을 시도하는 경우에는 [Laravel Sanctum](/docs/{{version}}/sanctum)을 사용하는 것이 좋습니다. Laravel Sanctum은 OAuth2를 지원하지 않지만 훨씬 간단한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치

다음 `install:api` Artisan 명령어를 통해 Laravel Passport를 설치할 수 있습니다.

```shell
php artisan install:api --passport
```

이 명령은 애플리케이션이 OAuth2 클라이언트와 액세스 토큰을 저장하는 데 필요한 데이터베이스 마이그레이션을 수행하고 테이블을 생성합니다. 또한, 보안 액세스 토큰 생성을 위한 암호화 키도 생성합니다.

추가로, 이 명령을 실행할 때 Passport의 `Client` 모델의 기본키를 증가하는 정수 대신 UUID로 사용할지 여부를 물어봅니다.

`install:api` 명령어를 실행한 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레잇을 추가하세요. 이 트레잇은 인증된 사용자의 토큰과 스코프를 검사할 수 있는 몇 가지 헬퍼 메서드를 제공합니다.

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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서, `api` 인증 가드를 정의하고 `driver` 옵션을 `passport`로 설정해야 합니다. 이로써 API 요청을 인증할 때 Passport의 `TokenGuard`를 사용하도록 지정합니다.

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

<a name="deploying-passport"></a>
### Passport 배포하기

Passport를 서버에 처음 배포할 때는 `passport:keys` 명령을 실행해야 할 수 있습니다. 이 명령은 Passport에서 액세스 토큰을 생성하는 데 필요한 암호화 키를 생성합니다. 생성된 키는 일반적으로 소스 컨트롤에 포함하지 않습니다.

```shell
php artisan passport:keys
```

필요하다면, Passport의 키를 로드할 경로를 지정할 수 있습니다. `Passport::loadKeysFrom` 메서드를 사용하세요. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
    }

<a name="loading-keys-from-the-environment"></a>
#### 환경 변수에서 키 로딩

또는, `vendor:publish` Artisan 명령어로 Passport의 설정 파일을 publish할 수 있습니다.

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일이 publish된 후, 환경 변수에 암호화 키를 정의하여 로드할 수 있습니다.

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

Passport를 새 메이저 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼하게 검토하세요.

<a name="configuration"></a>
## 설정

<a name="client-secret-hashing"></a>
### 클라이언트 시크릿 해싱

클라이언트 시크릿을 데이터베이스에 저장할 때 해싱하고 싶다면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 `Passport::hashClientSecrets` 메서드를 호출하세요.

    use Laravel\Passport\Passport;

    Passport::hashClientSecrets();

이 기능을 활성화하면, 모든 클라이언트 시크릿은 생성 직후에만 사용자에게 표시됩니다. 일반 텍스트 시크릿 값은 데이터베이스에 저장되지 않으므로, 시크릿을 분실한 경우 복구할 수 없습니다.

<a name="token-lifetimes"></a>
### 토큰 유효 기간

기본적으로 Passport는 1년 후 만료되는 장기 액세스 토큰을 발급합니다. 더 짧거나 긴 토큰 유효 기간을 설정하려면 `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출되어야 합니다.

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Passport::tokensExpireIn(now()->addDays(15));
        Passport::refreshTokensExpireIn(now()->addDays(30));
        Passport::personalAccessTokensExpireIn(now()->addMonths(6));
    }

> [!WARNING]  
> Passport의 데이터베이스 테이블에 있는 `expires_at` 컬럼은 읽기 전용이며, 표시 용도로만 사용됩니다. 토큰 발급 시 만료 정보는 서명되고 암호화된 토큰 내부에 저장됩니다. 토큰을 무효화하려면 [토큰 철회](#revoking-tokens)를 사용하세요.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이딩

Passport에서 내부적으로 사용하는 모델을 직접 확장할 수 있습니다. 사용자 정의 모델을 정의하고 해당 Passport 모델을 상속하세요.

    use Laravel\Passport\Client as PassportClient;

    class Client extends PassportClient
    {
        // ...
    }

모델을 정의한 후, `Laravel\Passport\Passport` 클래스를 통해 Passport가 사용자 정의 모델을 사용하도록 지정할 수 있습니다. 일반적으로 이 설정도 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 이루어집니다.

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

<a name="overriding-routes"></a>
### 라우트 오버라이딩

Passport에서 정의된 라우트를 커스터마이징 하고 싶을 때는 먼저 `AppServiceProvider`의 `register` 메서드에 `Passport::ignoreRoutes`를 추가하여 Passport가 라우트를 등록하지 않도록 해야 합니다.

    use Laravel\Passport\Passport;

    /**
     * Register any application services.
     */
    public function register(): void
    {
        Passport::ignoreRoutes();
    }

그 다음, [Passport의 라우트 파일](https://github.com/laravel/passport/blob/11.x/routes/web.php)에서 라우트를 복사하여 애플리케이션의 `routes/web.php` 파일에 붙여넣고 원하는 대로 수정하세요.

    Route::group([
        'as' => 'passport.',
        'prefix' => config('passport.path', 'oauth'),
        'namespace' => '\Laravel\Passport\Http\Controllers',
    ], function () {
        // Passport routes...
    });

<a name="issuing-access-tokens"></a>
## 액세스 토큰 발급

OAuth2를 권한 코드 방식(authorization codes)으로 사용하는 방법이 가장 일반적입니다. 이 방식을 사용할 때 클라이언트 애플리케이션은 사용자를 서버로 리다이렉트시키고, 사용자는 액세스 토큰 발급 요청을 승인/거부할 수 있습니다.

<a name="managing-clients"></a>
### 클라이언트 관리

API와 상호작용해야 하는 애플리케이션을 개발하는 개발자는 여러분의 애플리케이션에 "클라이언트"로 등록해야 합니다. 이는 일반적으로 애플리케이션 이름과 인가 요청이 승인된 후 리다이렉션될 URL을 제공하는 것을 의미합니다.

<a name="the-passportclient-command"></a>
#### `passport:client` 명령어

가장 간단한 방법은 `passport:client` Artisan 명령어를 사용하는 것입니다. 이 명령어는 OAuth2 기능을 테스트하기 위한 클라이언트를 생성할 때 사용할 수 있습니다. `client` 명령어 실행 시 클라이언트에 대한 추가 정보를 입력하라는 메시지가 표시되며, 클라이언트 ID와 시크릿이 발급됩니다.

```shell
php artisan passport:client
```

**Redirect URL**

클라이언트의 리다이렉트 URL이 여러 개인 경우 콤마(,)로 구분하여 입력할 수 있습니다. 만약 URL에 콤마가 포함되어 있다면 URL 인코딩해야 합니다.

```shell
http://example.com/callback,http://examplefoo.com/callback
```

<a name="clients-json-api"></a>
#### JSON API

애플리케이션 사용자가 직접 `client` 명령어를 사용할 수 없으므로, Passport는 클라이언트 생성을 위한 JSON API를 제공합니다. 이를 통해 별도의 컨트롤러 코드를 작성하지 않고도 클라이언트 생성, 업데이트, 삭제가 가능합니다.

단, Passport의 JSON API는 자체 프론트엔드와 조합해서 클라이언트 관리 대시보드를 제공할 수 있게 합니다. 아래는 API 엔드포인트 예시입니다. [Axios](https://github.com/axios/axios)를 이용한 HTTP 요청 예시도 포함되어 있습니다.

JSON API는 `web` 및 `auth` 미들웨어로 보호되므로 외부에서 호출할 수 없고 애플리케이션 내부에서만 사용할 수 있습니다.

<a name="get-oauthclients"></a>
#### `GET /oauth/clients`

이 라우트는 인증된 사용자의 모든 클라이언트를 반환합니다. 사용자가 클라이언트를 편집 혹은 삭제할 수 있도록 나열할 때 유용합니다.

```js
axios.get('/oauth/clients')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthclients"></a>
#### `POST /oauth/clients`

이 라우트는 새 클라이언트 생성을 위한 것입니다. 두 가지 데이터를 필요로 합니다: 클라이언트 `name`과 `redirect` URL. 클라이언트가 생성되면 ID와 시크릿이 발급됩니다.

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

이 라우트는 클라이언트 정보를 수정할 때 사용합니다.

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

이 라우트는 클라이언트를 삭제할 때 사용합니다.

```js
axios.delete('/oauth/clients/' + clientId)
    .then(response => {
        // ...
    });
```

<a name="requesting-tokens"></a>
### 토큰 요청

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인가를 위한 리다이렉트

클라이언트를 생성한 뒤, 개발자는 클라이언트 ID와 시크릿으로 인가 코드 및 액세스 토큰을 요청할 수 있습니다. 먼저, 클라이언트 애플리케이션에서 `/oauth/authorize`로 리다이렉트 요청을 보냅니다.

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

`prompt` 파라미터로 Passport 애플리케이션의 인증 동작 방식을 지정할 수 있습니다.

`prompt`가 `none`이면 인증되지 않은 사용자인 경우 인증 오류를 반환합니다. `consent`이면 이전에 모든 스코프를 이미 허용했더라도 항상 인가 승인 화면이 표시됩니다. `login`이면 기존에 세션이 있어도 항상 사용자가 다시 로그인하도록 합니다.

`prompt`가 없는 경우, 사용자가 요청한 스코프에 대해 이전에 인가하지 않았다면 승인 화면이 나타납니다.

> [!NOTE]  
> `/oauth/authorize` 라우트는 Passport에서 이미 정의하므로, 라우트를 따로 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 요청 승인

인가 요청을 받을 경우, Passport는 `prompt` 파라미터 값을 기반으로 자동 응답하며, 사용자가 승인 또는 거절할 수 있는 템플릿을 표시합니다. 승인을 하면, 사용자는 클라이언트가 지정한 `redirect_uri`로 이동하게 됩니다. 해당 `redirect_uri`는 클라이언트 생성 시 설정했던 `redirect` URL과 일치해야 합니다.

승인 화면을 커스터마이징하려면 다음 명령어로 Passport의 뷰를 publish 하세요.

```shell
php artisan vendor:publish --tag=passport-views
```

첫 번째 파티 클라이언트 등에서 승인 프롬프트를 건너뛰고 싶다면 [Client 모델을 확장](#overriding-default-models)하고 `skipsAuthorization` 메서드를 정의하세요. 만약 `skipsAuthorization`이 `true`를 반환하면, 즉시 승인 후 `redirect_uri`로 이동합니다(단, 클라이언트 애플리케이션이 `prompt` 파라미터를 명시적으로 설정했다면 프롬프트가 나옵니다).

    <?php

    namespace App\Models\Passport;

    use Laravel\Passport\Client as BaseClient;

    class Client extends BaseClient
    {
        /**
         * Determine if the client should skip the authorization prompt.
         */
        public function skipsAuthorization(): bool
        {
            return $this->firstParty();
        }
    }

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
#### 인가 코드를 액세스 토큰으로 변환

사용자가 인가 요청을 승인하면, 사용자는 클라이언트 애플리케이션으로 리다이렉트됩니다. 클라이언트 애플리케이션은 먼저 인가 요청 전 저장한 `state` 파라미터와 반환받은 값을 비교해야 합니다. 일치하면 애플리케이션에 POST 요청을 보내 액세스 토큰을 요청할 수 있습니다. 요청에는 인가 코드가 포함되어야 합니다.

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

이 `/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성이 있는 JSON 응답을 반환합니다. `expires_in`은 액세스 토큰 만료까지 남은 초(second) 수입니다.

> [!NOTE]  
> `/oauth/authorize`와 마찬가지로 `/oauth/token` 라우트 역시 Passport에서 자동으로 정의되므로 명시적으로 정의할 필요가 없습니다.

<a name="tokens-json-api"></a>
#### JSON API

Passport에는 인가된 액세스 토큰을 관리하기 위한 JSON API도 포함되어 있습니다. 이를 프론트엔드와 조합하여 사용자에게 액세스 토큰 대시보드를 제공할 수 있습니다. [Axios](https://github.com/axios/axios)로 HTTP 요청 예시를 제공합니다. 이 API 또한 `web` 및 `auth` 미들웨어로 보호되며 애플리케이션 내부에서만 호출할 수 있습니다.

<a name="get-oauthtokens"></a>
#### `GET /oauth/tokens`

이 라우트는 인증된 사용자가 생성한 모든 액세스 토큰을 반환합니다. 토큰을 나열하거나 개별 토큰의 철회(revoke)에 유용합니다.

```js
axios.get('/oauth/tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="delete-oauthtokenstoken-id"></a>
#### `DELETE /oauth/tokens/{token-id}`

이 라우트로 인증된 액세스 토큰 및 관련된 리프레시 토큰을 모두 휴효화(revoke)할 수 있습니다.

```js
axios.delete('/oauth/tokens/' + tokenId);
```

<a name="refreshing-tokens"></a>
### 토큰 갱신

애플리케이션이 단명 액세스 토큰을 발급한다면, 사용자는 토큰 만료 시 함께 발급된 리프레시 토큰으로 새 액세스 토큰을 발급받을 수 있습니다:

    use Illuminate\Support\Facades\Http;

    $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
        'grant_type' => 'refresh_token',
        'refresh_token' => 'the-refresh-token',
        'client_id' => 'client-id',
        'client_secret' => 'client-secret',
        'scope' => '',
    ]);

    return $response->json();

이 `/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 필드를 포함한 JSON을 반환합니다.

<a name="revoking-tokens"></a>
### 토큰 철회

토큰을 무효화하려면 `Laravel\Passport\TokenRepository`의 `revokeAccessToken` 메서드를 사용하세요. 리프레시 토큰의 경우 `Laravel\Passport\RefreshTokenRepository`의 `revokeRefreshTokensByAccessTokenId` 메서드를 사용합니다. 이 클래스들은 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)로 해결할 수 있습니다.

    use Laravel\Passport\TokenRepository;
    use Laravel\Passport\RefreshTokenRepository;

    $tokenRepository = app(TokenRepository::class);
    $refreshTokenRepository = app(RefreshTokenRepository::class);

    // 액세스 토큰 철회
    $tokenRepository->revokeAccessToken($tokenId);

    // 해당 토큰과 연결된 리프레시 토큰 모두 철회
    $refreshTokenRepository->revokeRefreshTokensByAccessTokenId($tokenId);

<a name="purging-tokens"></a>
### 토큰 정리

토큰이 철회되거나 만료된 경우, 데이터베이스에서 정리(purge)할 수 있습니다. Passport의 `passport:purge` Artisan 명령으로 삭제할 수 있습니다.

```shell
# 철회/만료된 토큰 및 인가 코드 모두 삭제
php artisan passport:purge

# 6시간 이상 만료된 토큰만 삭제
php artisan passport:purge --hours=6

# 철회된 것만 삭제
php artisan passport:purge --revoked

# 만료된 것만 삭제
php artisan passport:purge --expired
```

[스케줄링](/docs/{{version}}/scheduling) 기능을 사용하여 자동 정리를 설정할 수도 있습니다.

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('passport:purge')->hourly();

<a name="code-grant-pkce"></a>
## PKCE를 사용한 권한 코드 그랜트

"Proof Key for Code Exchange" (PKCE)가 적용된 권한 코드 그랜트는 SPA(싱글 페이지 애플리케이션)나 네이티브 앱에서 안전하게 API에 인증하는 방법입니다. 클라이언트 시크릿을 안전하게 저장할 수 없는 환경 또는 인가 코드 탈취 위협을 방지해야 할 때 이 방식을 사용해야 합니다. 인가 코드와 액세스 토큰 교환 시 클라이언트 시크릿 대신 "code verifier"와 "code challenge"를 사용합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성

인가 코드 그랜트(PKCE)로 토큰을 발급하려면 우선 PKCE를 지원하는 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령에서 `--public` 옵션을 사용합니다.

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청

<a name="code-verifier-code-challenge"></a>
#### 코드 검증자와 코드 챌린지(Verifier/Challenge)

이 인증 방식은 클라이언트 시크릿 대신, 코드 검증자(code verifier)와 코드 챌린지(code challenge)가 필요합니다.

코드 검증자는 [RFC 7636](https://tools.ietf.org/html/rfc7636) 스펙에 명시된 43~128자 사이의 임의 문자열이어야 하며, 영문, 숫자와 `"-"`, `"."`, `"_"`, `"~"` 문자로 구성됩니다.

코드 챌린지는 base64 인코딩된 문자열이며, URL 및 파일 이름에 안전해야 하고, 끝의 `=`는 제거되어야 하며, 줄바꿈/공백/기타 불필요한 문자가 없어야 합니다.

    $encoded = base64_encode(hash('sha256', $code_verifier, true));

    $codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 인가를 위한 리다이렉트

클라이언트를 생성한 뒤, 클라이언트 ID 및 생성한 코드 검증자/챌린지로 `/oauth/authorize`로 리다이렉트 요청을 만듭니다.

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

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
#### 인가 코드를 액세스 토큰으로 교환

사용자가 인가를 승인하면, 기존 권한 코드 그랜트와 마찬가지로 `state`의 유효성을 검증하고, 애플리케이션에 POST 요청을 보내 액세스 토큰을 요청합니다. 이때는 인가 코드와 함께 기존에 생성한 코드 검증자도 함께 전송해야 합니다.

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

<a name="password-grant-tokens"></a>
## 패스워드 그랜트 토큰

> [!WARNING]  
> 패스워드 그랜트 토큰 방식은 더 이상 권장되지 않습니다. 대신 [OAuth2 서버에서 현재 권장하는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

OAuth2 패스워드 그랜트는 모바일 앱 등과 같은 퍼스트파티(First Party) 클라이언트가 이메일/아이디 및 비밀번호로 액세스 토큰을 발급받을 수 있도록 합니다. 사용자가 OAuth2 인가 코드 리다이렉트 플로를 거치지 않고도 토큰을 안전하게 발급받을 수 있습니다.

패스워드 그랜트를 활성화하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enablePasswordGrant`를 호출하세요.

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Passport::enablePasswordGrant();
    }

<a name="creating-a-password-grant-client"></a>
### 패스워드 그랜트 클라이언트 생성

패스워드 그랜트를 사용하기 전, 패스워드 그랜트 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령에 `--password` 옵션을 사용하세요. **이미 `passport:install`을 실행했다면, 이 명령은 추가로 실행할 필요 없습니다.**

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청

패스워드 그랜트 클라이언트를 만들었으면, 사용자의 이메일과 비밀번호로 `/oauth/token`에 POST 요청을 보내 토큰을 발급받을 수 있습니다. 이 라우트는 Passport가 이미 등록하므로 별도 정의하지 않아도 됩니다. 요청이 성공하면 서버로부터 `access_token`, `refresh_token`을 포함하는 JSON 응답이 반환됩니다.

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

> [!NOTE]  
> 액세스 토큰은 기본적으로 장기 토큰입니다. 필요하다면 [최대 액세스 토큰 만료 시간 설정](#configuration)이 가능합니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청

패스워드 그랜트 또는 클라이언트 크리덴셜 그랜트를 사용할 때 토큰에 애플리케이션이 지원하는 모든 스코프를 부여할 수 있습니다. 이 경우 `*` 스코프를 요청하세요. `*` 스코프가 포함된 토큰의 `can` 메서드는 항상 `true`를 반환합니다. 이 스코프는 `password` 또는 `client_credentials` 그랜트 타입으로 발급된 토큰에만 지정할 수 있습니다.

    use Illuminate\Support\Facades\Http;

    $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
        'grant_type' => 'password',
        'client_id' => 'client-id',
        'client_secret' => 'client-secret',
        'username' => 'taylor@laravel.com',
        'password' => 'my-password',
        'scope' => '*',
    ]);

<a name="customizing-the-user-provider"></a>
### 사용자 프로바이더 커스터마이징

애플리케이션에서 두 개 이상의 [사용자 프로바이더](/docs/{{version}}/authentication#introduction)를 사용하는 경우, `artisan passport:client --password` 명령 실행 시 `--provider` 옵션으로 패스워드 그랜트 클라이언트에 사용할 프로바이더를 지정할 수 있습니다. 값은 `config/auth.php` 설정에 정의된 프로바이더와 일치해야 합니다. 이후 [미들웨어를 이용해 라우트 보호](#via-middleware)를 적용하여 특정 프로바이더의 사용자만 인증하도록 설정할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자명 필드 커스터마이징

패스워드 그랜트를 사용할 때 Passport는 인증 모델의 `email` 속성을 "유저네임"으로 사용합니다. 동작을 변경하려면 모델에 `findForPassport` 메서드를 정의하세요.

    <?php

    namespace App\Models;

    use Illuminate\Foundation\Auth\User as Authenticatable;
    use Illuminate\Notifications\Notifiable;
    use Laravel\Passport\HasApiTokens;

    class User extends Authenticatable
    {
        use HasApiTokens, Notifiable;

        /**
         * Find the user instance for the given username.
         */
        public function findForPassport(string $username): User
        {
            return $this->where('username', $username)->first();
        }
    }

<a name="customizing-the-password-validation"></a>
### 비밀번호 검증 커스터마이징

패스워드 그랜트 인증 시 기본적으로 모델의 `password` 속성으로 비밀번호를 검증합니다. 만약 속성이 존재하지 않거나 검증 방식을 변경하고 싶다면, 모델에 `validateForPassportPasswordGrant` 메서드를 정의하세요.

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
         * Validate the password of the user for the Passport password grant.
         */
        public function validateForPassportPasswordGrant(string $password): bool
        {
            return Hash::check($password, $this->password);
        }
    }

<a name="implicit-grant-tokens"></a>
## 임플리시트 그랜트 토큰

> [!WARNING]  
> 임플리시트 그랜트 토큰 방식은 더 이상 권장되지 않습니다. [OAuth2 서버 권장 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

임플리시트 그랜트는 권한 코드 그랜트와 비슷하지만, 인가 코드 교환 없이 바로 토큰이 클라이언트로 전달됩니다. 주로 자바스크립트/모바일 애플리케이션 등에서 클라이언트 크리덴셜을 안전하게 저장할 수 없는 경우 사용됩니다. 활성화하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 `enableImplicitGrant`를 호출하세요.

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Passport::enableImplicitGrant();
    }

활성화 후 개발자는 클라이언트 ID로 토큰 발급을 요청할 수 있습니다. `/oauth/authorize`로 리다이렉트 요청을 보내면 됩니다.

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

> [!NOTE]  
> `/oauth/authorize` 라우트는 Passport에서 자동으로 정의합니다.

<a name="client-credentials-grant-tokens"></a>
## 클라이언트 크리덴셜 그랜트 토큰

클라이언트 크리덴셜 그랜트는 머신-투-머신 인증에 적합합니다. 예를 들어, 예약된 작업이 API를 통해 유지보수를 할 때 이 방식을 사용할 수 있습니다.

클라이언트 크리덴셜 그랜트로 토큰을 발급하려면, `passport:client` Artisan 명령어의 `--client` 옵션을 사용하여 클라이언트를 생성하세요.

```shell
php artisan passport:client --client
```

이후, `CheckClientCredentials` 미들웨어에 대한 별칭을 등록해야 합니다. `bootstrap/app.php`에서 별칭을 정의하세요.

    use Laravel\Passport\Http\Middleware\CheckClientCredentials;

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->alias([
            'client' => CheckClientCredentials::class
        ]);
    })

그 다음, 라우트에 해당 미들웨어를 적용하세요.

    Route::get('/orders', function (Request $request) {
        ...
    })->middleware('client');

특정 스코프만 허용하려면 미들웨어에 콤마로 구분하여 스코프를 설정할 수 있습니다.

    Route::get('/orders', function (Request $request) {
        ...
    })->middleware('client:check-status,your-scope');

<a name="retrieving-tokens"></a>
### 토큰 조회

이 그랜트 타입을 사용해 토큰을 발급받으려면 `oauth/token` 엔드포인트로 요청을 보냅니다.

    use Illuminate\Support\Facades\Http;

    $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
        'grant_type' => 'client_credentials',
        'client_id' => 'client-id',
        'client_secret' => 'client-secret',
        'scope' => 'your-scope',
    ]);

    return $response->json()['access_token'];

<a name="personal-access-tokens"></a>
## 개인 액세스 토큰

때로는 사용자 스스로 애플리케이션 UI에서 리다이렉트 코드 플로 없이 액세스 토큰을 직접 발급할 수 있어야 합니다. 이렇게 하면, API 테스트 또는 액세스 토큰 발급을 좀 더 단순하게 처리할 수 있습니다.

> [!NOTE]  
> 애플리케이션이 주로 개인 액세스 토큰 발급에 Passport를 사용한다면, [Laravel Sanctum](/docs/{{version}}/sanctum) 사용도 고려해보세요.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성

개인 액세스 토큰을 발급하려면 먼저 개인 액세스 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령에 `--personal` 옵션을 사용하세요. 이미 `passport:install`을 실행했다면 추가 실행할 필요 없습니다.

```shell
php artisan passport:client --personal
```

생성 후, 클라이언트 ID와 일반 텍스트 시크릿 값을 `.env` 파일에 설정하세요.

```ini
PASSPORT_PERSONAL_ACCESS_CLIENT_ID="client-id-value"
PASSPORT_PERSONAL_ACCESS_CLIENT_SECRET="unhashed-client-secret-value"
```

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리

개인 액세스 클라이언트를 만들고 나면, `App\Models\User` 인스턴스의 `createToken` 메서드로 토큰을 발급할 수 있습니다. 첫 번째 인수는 토큰 이름, 두 번째는 [스코프](#token-scopes) 배열(선택)입니다.

    use App\Models\User;

    $user = User::find(1);

    // 스코프 없이 토큰 생성
    $token = $user->createToken('Token Name')->accessToken;

    // 스코프 포함 토큰 생성
    $token = $user->createToken('My Token', ['place-orders'])->accessToken;

<a name="personal-access-tokens-json-api"></a>
#### JSON API

Passport에는 개인 액세스 토큰을 관리하기 위한 JSON API도 포함되어 있습니다. 이것을 프론트엔드와 조합해 사용자 대시보드를 만들 수 있습니다. 아래는 API 엔드포인트별 예시입니다. [Axios](https://github.com/axios/axios) 사용 예시를 제공합니다.

이 API는 `web` 및 `auth` 미들웨어로 보호되어 외부에서 사용 불가하고 애플리케이션 내부에서만 사용 가능합니다.

<a name="get-oauthscopes"></a>
#### `GET /oauth/scopes`

이 라우트는 애플리케이션의 [스코프](#token-scopes) 전체 목록을 반환합니다.

```js
axios.get('/oauth/scopes')
    .then(response => {
        console.log(response.data);
    });
```

<a name="get-oauthpersonal-access-tokens"></a>
#### `GET /oauth/personal-access-tokens`

이 라우트는 인증된 사용자가 생성한 모든 개인 액세스 토큰을 반환합니다.

```js
axios.get('/oauth/personal-access-tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthpersonal-access-tokens"></a>
#### `POST /oauth/personal-access-tokens`

이 라우트는 새로운 개인 액세스 토큰을 생성합니다. 토큰 이름과 할당할 스코프 배열을 입력해야 합니다.

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

이 라우트로 개인 액세스 토큰을 철회(무효화)할 수 있습니다.

```js
axios.delete('/oauth/personal-access-tokens/' + tokenId);
```

<a name="protecting-routes"></a>
## 라우트 보호

<a name="via-middleware"></a>
### 미들웨어를 통해

Passport는 유입 요청에서 액세스 토큰을 검증할 수 있는 [인증 가드](/docs/{{version}}/authentication#adding-custom-guards)를 제공합니다. `api` 가드를 `passport` 드라이버로 설정했다면, 유효 액세스 토큰이 필요한 라우트에 `auth:api` 미들웨어만 추가하면 됩니다.

    Route::get('/user', function () {
        // ...
    })->middleware('auth:api');

> [!WARNING]  
> [클라이언트 크리덴셜 그랜트](#client-credentials-grant-tokens)를 사용하는 경우, 라우트 보호에 `auth:api` 대신 [`client` 미들웨어](#client-credentials-grant-tokens)를 사용해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 다중 인증 가드

애플리케이션에서 Eloquent 모델이 서로 다른 두 사용자 유형을 인증할 필요가 있을 때, 사용자 프로바이더 유형별로 가드 설정을 정의해야 할 수 있습니다. 예를 들어 다음과 같이 `config/auth.php`에 가드를 설정할 수 있습니다.

    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],

    'api-customers' => [
        'driver' => 'passport',
        'provider' => 'customers',
    ],

예를 들어, 아래 라우트는 `customers` 프로바이더와 연결된 `api-customers` 가드로 인증합니다.

    Route::get('/customer', function () {
        // ...
    })->middleware('auth:api-customers');

> [!NOTE]  
> Passport로 여러 사용자 프로바이더를 사용하는 방법은 [패스워드 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달

Passport로 보호된 엔드포인트를 호출할 때 API 소비자는 `Authorization` 헤더에 `Bearer` 토큰 방식으로 액세스 토큰을 전달해야 합니다. 예를 들어 Guzzle HTTP 사용 시 다음과 같이 사용할 수 있습니다.

    use Illuminate\Support\Facades\Http;

    $response = Http::withHeaders([
        'Accept' => 'application/json',
        'Authorization' => 'Bearer '.$accessToken,
    ])->get('https://passport-app.test/api/user');

    return $response->json();

<a name="token-scopes"></a>
## 토큰 스코프

스코프는 API 클라이언트가 계정 접근 권한 요청 시 특정 권한 집합만 요청하도록 제한합니다. 예를 들어 전자상거래 애플리케이션에서 전체 주문 권한이 아니라 배송 상태만 조회하도록 제한할 수 있습니다. 즉, 스코프를 통해 써드파티 애플리케이션이 사용자를 대신하여 실행할 수 있는 작업을 제한할 수 있습니다.

<a name="defining-scopes"></a>
### 스코프 정의

API 스코프는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `Passport::tokensCan` 메서드로 등록합니다. 이름/설명 쌍으로 배열을 넘기면 됩니다. 설명은 승인 화면에 표시됩니다.

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

<a name="default-scope"></a>
### 기본 스코프

클라이언트가 특정 스코프를 요청하지 않으면, `setDefaultScope` 메서드로 기본 스코프 자동 부여가 가능합니다. 이 설정도 `boot` 메서드에서 지정하세요.

    use Laravel\Passport\Passport;

    Passport::tokensCan([
        'place-orders' => 'Place orders',
        'check-status' => 'Check order status',
    ]);

    Passport::setDefaultScope([
        'check-status',
        'place-orders',
    ]);

> [!NOTE]  
> Passport의 기본 스코프는 사용자가 발급한 개인 액세스 토큰에는 적용되지 않습니다.

<a name="assigning-scopes-to-tokens"></a>
### 토큰에 스코프 할당

<a name="when-requesting-authorization-codes"></a>
#### 권한 코드 요청 시

권한 코드 그랜트로 액세스 토큰을 요청할 때, `scope` 쿼리 스트링 파라미터에 원하는 스코프(들)를 공백으로 구분해 지정하세요.

    Route::get('/redirect', function () {
        $query = http_build_query([
            'client_id' => 'client-id',
            'redirect_uri' => 'http://example.com/callback',
            'response_type' => 'code',
            'scope' => 'place-orders check-status',
        ]);

        return redirect('http://passport-app.test/oauth/authorize?'.$query);
    });

<a name="when-issuing-personal-access-tokens"></a>
#### 개인 액세스 토큰 발급 시

`App\Models\User`의 `createToken` 메서드 두 번째 인수로 원하는 스코프 배열을 지정하면 됩니다.

    $token = $user->createToken('My Token', ['place-orders'])->accessToken;

<a name="checking-scopes"></a>
### 스코프 확인

Passport에는 특정 스코프가 포함된 토큰인지 검증하는 미들웨어 두 가지가 있습니다. 아래와 같이 `bootstrap/app.php`에 별칭을 등록하세요.

    use Laravel\Passport\Http\Middleware\CheckForAnyScope;
    use Laravel\Passport\Http\Middleware\CheckScopes;

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->alias([
            'scopes' => CheckScopes::class,
            'scope' => CheckForAnyScope::class,
        ]);
    })

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인

`scopes` 미들웨어를 라우트에 지정하면, 토큰에 모든 지정 스코프가 존재하는지 검사합니다.

    Route::get('/orders', function () {
        // "check-status"와 "place-orders" 스코프 모두 있어야 함
    })->middleware(['auth:api', 'scopes:check-status,place-orders']);

<a name="check-for-any-scopes"></a>
#### 하나라도 스코프 확인

`scope` 미들웨어는 하나 이상의 지정 스코프만 있으면 통과합니다.

    Route::get('/orders', function () {
        // "check-status" 또는 "place-orders" 중 하나라도 있는 경우
    })->middleware(['auth:api', 'scope:check-status,place-orders']);

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인

인증된 요청이 애플리케이션에 전달된 후에도 `App\Models\User` 인스턴스의 `tokenCan` 메서드로 해당 스코프 포함 여부를 검사할 수 있습니다.

    use Illuminate\Http\Request;

    Route::get('/orders', function (Request $request) {
        if ($request->user()->tokenCan('place-orders')) {
            // ...
        }
    });

<a name="additional-scope-methods"></a>
#### 추가 스코프 메서드

`scopeIds` 메서드는 정의된 스코프 ID/이름 배열을 반환합니다.

    use Laravel\Passport\Passport;

    Passport::scopeIds();

`scopes` 메서드는 정의된 모든 스코프를 `Laravel\Passport\Scope` 인스턴스 배열로 반환합니다.

    Passport::scopes();

`scopesFor`는 주어진 ID/이름에 해당하는 스코프 인스턴스 배열을 반환합니다.

    Passport::scopesFor(['place-orders', 'check-status']);

특정 스코프가 정의되어있는지 `hasScope`로 확인할 수 있습니다.

    Passport::hasScope('place-orders');

<a name="consuming-your-api-with-javascript"></a>
## JavaScript로 API 사용

API를 개발하면서 자신의 JavaScript 애플리케이션에서 직접 API를 사용할 수 있다면 매우 유용합니다. 이 방식은 여러분의 웹, 모바일, 서드파티 애플리케이션, 각종 SDK 등에서 동일한 API를 활용할 수 있게 합니다.

일반적으로 JavaScript 애플리케이션에서 API를 사용하려면 액세스 토큰을 수동으로 전달해야 하지만, Passport의 미들웨어가 이를 자동 처리할 수 있습니다. `CreateFreshApiToken` 미들웨어를 `web` 미들웨어 그룹에 추가하세요(`bootstrap/app.php`).

    use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->web(append: [
            CreateFreshApiToken::class,
        ]);
    })

> [!WARNING]  
> `CreateFreshApiToken` 미들웨어는 미들웨어 스택의 맨 마지막에 위치해야 합니다.

이 미들웨어는 `laravel_token` 쿠키를 발급합니다. 이 쿠키에는 Passport가 API 요청을 인증하는 데 사용할 암호화된 JWT가 포함되어 있습니다(JWT 유효 기간은 `session.lifetime` 설정을 따름). 브라우저가 자동으로 쿠키를 전송하므로, API 요청 시 액세스 토큰 전달을 신경 쓰지 않아도 됩니다.

    axios.get('/api/user')
        .then(response => {
            console.log(response.data);
        });

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이징

필요하다면, Passport의 `cookie` 메서드로 `laravel_token` 쿠키 이름을 변경할 수 있습니다. 이 메서드는 보통 `App\Providers\AppServiceProvider` 클래스의 `boot`에서 호출됩니다.

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Passport::cookie('custom_name');
    }

<a name="csrf-protection"></a>
#### CSRF 보호

이 인증 방식을 사용할 때, 요청에 유효한 CSRF 토큰 헤더가 포함되어야 합니다. Laravel의 기본 JavaScript 스캐폴딩은 Axios 인스턴스를 제공하며, 이 인스턴스는 암호화된 `XSRF-TOKEN` 쿠키 값을 자동으로 `X-XSRF-TOKEN` 헤더로 전송합니다.

> [!NOTE]  
> 만약 `X-XSRF-TOKEN` 대신 `X-CSRF-TOKEN`을 보내야 한다면, 반드시 `csrf_token()`에서 제공하는 *암호화되지 않은* 토큰을 사용해야 합니다.

<a name="events"></a>
## 이벤트

Passport는 액세스 토큰 및 리프레시 토큰을 발급할 때 이벤트를 발생시킵니다. 이 이벤트에 [리스너를 등록](/docs/{{version}}/events)하여 데이터베이스의 다른 액세스 토큰을 정리(prune)하거나 철회(revoke)할 수 있습니다.

<div class="overflow-auto">

| 이벤트 이름 |
| --- |
| `Laravel\Passport\Events\AccessTokenCreated` |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## 테스트

Passport의 `actingAs` 메서드는 현재 인증된 사용자 및 스코프를 지정하는 데 사용할 수 있습니다. 첫 번째 인자는 사용자 인스턴스, 두 번째는 사용자 토큰에 부여할 스코프 배열입니다.

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

Passport의 `actingAsClient` 메서드는 현재 인증된 클라이언트 및 스코프를 지정할 수 있습니다. 첫 번째 인자는 클라이언트 인스턴스, 두 번째는 클라이언트 토큰에 부여할 스코프 배열입니다.

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