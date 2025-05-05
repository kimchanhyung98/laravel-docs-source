# Laravel Sanctum

- [소개](#introduction)
    - [동작 원리](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 권한](#token-abilities)
    - [라우트 보호](#protecting-routes)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증](#spa-authenticating)
    - [라우트 보호](#protecting-spa-routes)
    - [프라이빗 브로드캐스트 채널 권한 부여](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호](#protecting-mobile-api-routes)
    - [토큰 폐기](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션, 그리고 단순한 토큰 기반 API를 위한 경량 인증 시스템을 제공합니다. Sanctum을 통해 각 사용자는 자신의 계정에 여러 API 토큰을 생성할 수 있습니다. 이 토큰들은 수행할 수 있는 동작(권한/Scope)을 지정하는 능력을 부여받을 수 있습니다.

<a name="how-it-works"></a>
### 동작 원리

Laravel Sanctum은 두 가지 별도의 문제를 해결하기 위해 존재합니다. 라이브러리를 더 깊이 파기 전에 각각을 살펴보겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰

첫째, Sanctum은 OAuth의 복잡성 없이 사용자에게 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 GitHub 및 기타 애플리케이션에서 "개인 접근 토큰(Personal Access Token)"을 발급하는 방식에서 영감을 받았습니다. 예를 들어, 애플리케이션의 "계정 설정" 화면에 사용자가 자신의 계정에 사용할 API 토큰을 생성할 수 있는 화면이 있다고 가정해보세요. Sanctum을 통해 이러한 토큰을 생성하고 관리할 수 있습니다. 이 토큰들은 보통 매우 긴 만료 기간(수년)을 가지나, 사용자가 언제든지 직접 폐기할 수 있습니다.

Laravel Sanctum은 사용자 API 토큰을 단일 데이터베이스 테이블에 저장하고, 유효한 API 토큰을 포함한 `Authorization` 헤더를 통해 들어오는 HTTP 요청을 인증합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증

둘째, Sanctum은 Laravel 기반 API와 통신해야 하는 SPA(싱글 페이지 애플리케이션) 인증을 간단하게 처리하기 위해 존재합니다. 이러한 SPA는 Laravel 애플리케이션과 같은 저장소에 있을 수도 있고, Next.js나 Nuxt 등 완전히 별도의 저장소에 있을 수도 있습니다.

이 기능을 위해 Sanctum은 토큰을 전혀 사용하지 않습니다. 대신 Laravel의 내장 쿠키 기반 세션 인증 서비스를 사용합니다. 일반적으로 Sanctum은 Laravel의 `web` 인증 가드를 활용합니다. 이러한 방식은 CSRF 보호, 세션 인증, 그리고 XSS로 인한 인증 정보 유출 방지의 이점을 제공합니다.

Sanctum은 들어오는 요청의 출처가 자체 SPA 프론트엔드일 때만 쿠키를 이용한 인증을 시도합니다. Sanctum이 들어오는 HTTP 요청을 검사할 때 먼저 인증 쿠키를 살펴보고, 쿠키가 없으면 이후 `Authorization` 헤더에 유효한 API 토큰이 있는지를 검사합니다.

> [!NOTE]
> Sanctum을 반드시 API 토큰 인증 또는 SPA 인증 중 하나만 사용해도 전혀 문제 없습니다. Sanctum을 사용한다고 해서 두 기능 모두를 써야 하는 것은 아닙니다.

<a name="installation"></a>
## 설치

`install:api` Artisan 명령어를 통해 Laravel Sanctum을 설치할 수 있습니다:

```shell
php artisan install:api
```

이후, Sanctum으로 SPA 인증을 하려는 경우 이 문서의 [SPA 인증](#spa-authentication) 섹션을 참고하세요.

<a name="configuration"></a>
## 설정

<a name="overriding-default-models"></a>
### 기본 모델 재정의

반드시 필요한 것은 아니지만, 내부적으로 Sanctum이 사용하는 `PersonalAccessToken` 모델을 확장할 수 있습니다:

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

이후, Sanctum이 여러분의 커스텀 모델을 사용하도록 `usePersonalAccessTokenModel` 메서드로 지정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 파일의 `boot` 메서드에서 호출해야 합니다:

```php
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * 어플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a name="api-token-authentication"></a>
## API 토큰 인증

> [!NOTE]
> SPA(퍼스트 파티 프론트엔드) 인증에는 API 토큰을 사용하지 않아야 합니다. 대신 Sanctum의 내장 [SPA 인증 기능](#spa-authentication)을 사용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급

Sanctum을 통해 애플리케이션의 API 요청을 인증할 수 있는 API 토큰(개인 접근 토큰)을 발급할 수 있습니다. API 토큰을 사용할 때는 `Authorization` 헤더에 `Bearer` 토큰으로 포함해야 합니다.

토큰 발급을 시작하려면, User 모델에서 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용해야 합니다:

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

토큰을 발급하려면 `createToken` 메서드를 사용할 수 있습니다. 이 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전에 SHA-256으로 해싱되지만, 토큰 생성 직후라면 `NewAccessToken` 인스턴스의 `plainTextToken` 속성을 통해 평문 값을 얻을 수 있습니다. 이 값을 토큰이 생성된 직후 사용자에게 안내해야 합니다:

```php
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

`HasApiTokens` 트레이트에서 제공하는 `tokens` Eloquent 관계를 통해 사용자의 모든 토큰에 접근할 수 있습니다:

```php
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
### 토큰 권한

Sanctum을 사용하면 토큰에 "권한(abilities)"을 부여할 수 있습니다. 권한은 OAuth의 "스코프"와 비슷한 역할을 합니다. `createToken` 메서드의 두 번째 인자로 문자열 배열 형태로 권한을 지정할 수 있습니다:

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Sanctum으로 인증된 들어오는 요청을 처리할 때, `tokenCan`이나 `tokenCant` 메서드를 사용하여 토큰이 특정 권한을 가지고 있는지 판단할 수 있습니다:

```php
if ($user->tokenCan('server:update')) {
    // ...
}

if ($user->tokenCant('server:update')) {
    // ...
}
```

<a name="token-ability-middleware"></a>
#### 토큰 권한 미들웨어

Sanctum에는 토큰이 특정 권한을 갖추었는지 검사하는 데 사용할 수 있는 두 개의 미들웨어가 있습니다. 먼저, 애플리케이션의 `bootstrap/app.php` 파일에 아래와 같이 미들웨어 별칭을 정의하세요:

```php
use Laravel\Sanctum\Http\Middleware\CheckAbilities;
use Laravel\Sanctum\Http\Middleware\CheckForAnyAbility;

->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'abilities' => CheckAbilities::class,
        'ability' => CheckForAnyAbility::class,
    ]);
})
```

`abilities` 미들웨어를 라우트에 할당하면, 요청의 토큰이 나열된 모든 권한을 가지고 있는지 확인합니다:

```php
Route::get('/orders', function () {
    // 토큰이 "check-status"와 "place-orders" 두 권한 모두 보유해야 합니다.
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` 미들웨어는 라우트에 할당할 경우, 요청의 토큰이 나열된 권한 중 **적어도 하나**를 가지고 있는지 확인합니다:

```php
Route::get('/orders', function () {
    // 토큰이 "check-status" 또는 "place-orders" 둘 중 하나의 권한만 보유해도 됩니다.
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### 퍼스트 파티 UI에서 발생한 요청

편의상, 인증된 요청이 퍼스트 파티 SPA를 통해 발생했다면, 그리고 Sanctum의 내장 [SPA 인증](#spa-authentication)을 사용할 경우, `tokenCan` 메서드는 항상 `true`를 반환합니다.

하지만 이것이 반드시 사용자가 해당 작업을 수행할 수 있어야 한다는 의미는 아닙니다. 일반적으로 애플리케이션의 [인가(authorization) 정책](/docs/{{version}}/authorization#creating-policies)에서 토큰에 명시된 권한과 더불어, 해당 사용자 인스턴스가 실제로 작업을 수행할 자격이 있는지도 판단해야 합니다.

예를 들어, 서버 관리를 하는 애플리케이션이라면, 토큰이 서버 업데이트 권한을 갖추었는지와 **동시에** 해당 서버가 사용자 소유인지도 검사해야 합니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

처음에는 `tokenCan` 메서드를 항상 호출하고 퍼스트 파티 UI 요청에서 언제나 `true`를 반환하는 게 다소 이상하게 느껴질 수 있습니다. 하지만 API 토큰이 항상 있다고 가정하고, `tokenCan`을 인가 정책 내에서 부를 수 있다는 점에서 매우 편리합니다.

<a name="protecting-routes"></a>
### 라우트 보호

모든 들어오는 요청이 인증되도록 라우트를 보호하려면, `routes/web.php`나 `routes/api.php` 파일에서 해당 라우트에 `sanctum` 인증 가드를 할당하세요. 이 가드는 들어오는 요청이 상태 유지(쿠키 인증)인지, 아니면 써드파티의 API 토큰 인증인지 판단해 올바르게 인증합니다.

왜 `routes/web.php`에서 `sanctum` 가드를 사용하라고 권장하는지 궁금할 수 있습니다. Sanctum은 들어오는 요청을 먼저 Laravel의 일반적인 세션 인증 쿠키로 인증합니다. 쿠키가 없으면 Authorization 헤더로 토큰 인증을 시도합니다. 그렇게 하면 항상 인증된 사용자 인스턴스에서 `tokenCan` 메서드를 호출할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-tokens"></a>
### 토큰 폐기

`Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 관계를 통해 데이터베이스에서 토큰을 삭제함으로써 토큰을 "폐기(revoke)"할 수 있습니다:

```php
// 모든 토큰 폐기
$user->tokens()->delete();

// 현재 요청을 인증한 토큰 폐기
$request->user()->currentAccessToken()->delete();

// 특정 토큰 폐기
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### 토큰 만료

기본적으로 Sanctum 토큰은 만료되지 않으며, [토큰 폐기](#revoking-tokens)를 통해서만 무효화할 수 있습니다. 하지만 애플리케이션의 API 토큰 만료 시간을 설정하고 싶다면, 애플리케이션의 `sanctum` 설정 파일에 `expiration` 옵션을 지정하면 됩니다. 이 값은 토큰이 만료될 때까지의 분 단위 시간입니다:

```php
'expiration' => 525600,
```

토큰마다 만료 시간을 따로 지정하고 싶다면, `createToken` 메서드의 세 번째 인자로 만료 시간을 전달할 수 있습니다:

```php
return $user->createToken(
    'token-name', ['*'], now()->addWeek()
)->plainTextToken;
```

애플리케이션에 토큰 만료 시간을 설정했다면, [스케줄러](/docs/{{version}}/scheduling)를 통해 만료된 토큰 데이터를 정리(prune)하는 작업을 예약할 수도 있습니다. 다행히 Sanctum에는 만료된 토큰을 삭제하는 `sanctum:prune-expired` Artisan 명령어가 포함되어 있습니다. 예를 들어, 지난 24시간 이상 만료된 토큰을 삭제하는 작업을 아래와 같이 등록할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증

Sanctum은 또한 Laravel 기반 API와 통신하기 위해 SPA 인증을 간편하게 처리할 수 있게 해줍니다. 이러한 SPA는 Laravel 애플리케이션의 동일 리포지토리에 있거나, 완전히 별도 저장소로 존재할 수 있습니다.

이 기능에서는 어떤 종류의 토큰도 사용하지 않습니다. 대신, Sanctum은 Laravel의 내장 쿠키 기반 세션 인증을 사용합니다. 이런 방식을 이용하면 CSRF 보호, 세션 인증, XSS로 인한 인증 정보 유출 방지의 장점이 있습니다.

> [!WARNING]
> 인증을 위해 SPA와 API가 반드시 동일한 최상위 도메인을 사용해야 하지만, 서로 다른 서브도메인에 위치해도 무방합니다. 그리고 요청 시 `Accept: application/json` 헤더와 함께 `Referer` 또는 `Origin` 헤더를 보내야 합니다.

<a name="spa-configuration"></a>
### 설정

<a name="configuring-your-first-party-domains"></a>
#### 퍼스트 파티 도메인 설정

먼저, SPA에서 요청을 보낼 도메인을 Sanctum의 `sanctum` 설정 파일의 `stateful` 옵션에 지정해야 합니다. 이 설정은 어떤 도메인이 Laravel 세션 쿠키를 이용하여 "상태 유지" 인증을 수행할지 결정합니다.

> [!WARNING]
> 애플리케이션에 포트(`127.0.0.1:8000`)가 포함된 URL로 접근한다면 도메인에 반드시 포트번호까지 포함해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

그 다음에는, SPA에서 들어오는 요청은 Laravel 세션 쿠키를 통해 인증하고, 써드파티나 모바일 앱에서는 API 토큰으로 인증할 수 있도록 해야 합니다. 이는 `bootstrap/app.php` 파일에서 `statefulApi` 미들웨어 메서드를 호출하여 쉽게 처리할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->statefulApi();
})
```

<a name="cors-and-cookies"></a>
#### CORS와 쿠키

별도 서브도메인에서 실행되는 SPA에서 인증이 잘 안 된다면, CORS(교차 출처 리소스 공유)나 세션 쿠키 설정이 잘못되어 있는 경우가 많습니다.

`config/cors.php` 설정 파일은 기본적으로 자동 생성되지 않습니다. 만약 Laravel의 CORS 옵션을 커스터마이즈할 필요가 있다면 `config:publish` Artisan 명령어로 전체 `cors` 설정 파일을 퍼블리시하세요:

```shell
php artisan config:publish cors
```

그 다음, `Access-Control-Allow-Credentials` 헤더가 `True`로 반환되도록, `config/cors.php`에서 `supports_credentials` 옵션을 `true`로 지정해야 합니다.

그리고, 전역 `axios` 인스턴스에서 `withCredentials`와 `withXSRFToken` 옵션을 활성화해야 합니다. 보통 `resources/js/bootstrap.js` 파일에 아래 코드가 들어갑니다. 만약 프론트엔드에서 axios를 사용하지 않는다면, 사용하는 HTTP 클라이언트에 맞게 동일하게 설정하세요:

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

마지막으로, 세션 쿠키 도메인 설정에 루트 도메인 아래 모든 서브도메인이 허용되도록, `config/session.php` 파일의 도메인 앞에 점(`.`)을 붙이세요:

```php
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 인증

<a name="csrf-protection"></a>
#### CSRF 보호

SPA 인증을 위해서는 "로그인" 페이지에서 우선 `/sanctum/csrf-cookie` 엔드포인트로 요청을 보내 애플리케이션의 CSRF 보호를 초기화해야 합니다:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // 로그인...
});
```

이 요청 시 Laravel은 현재 CSRF 토큰이 포함된 `XSRF-TOKEN` 쿠키를 설정합니다. 이 토큰은 URL 디코딩된 값으로 이후 모든 요청의 `X-XSRF-TOKEN` 헤더에 포함되어야 하며, axios나 Angular HttpClient 같은 라이브러리는 이를 자동으로 처리해줍니다. 만약 사용 중인 JS HTTP 라이브러리에서 자동 처리하지 않는다면, `X-XSRF-TOKEN` 헤더에 `XSRF-TOKEN` 쿠키 값을 직접 넣어야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호가 끝나면, Laravel 애플리케이션의 `/login` 라우트에 `POST` 요청을 보냅니다. `/login` 라우트는 직접 [구현](/docs/{{version}}/authentication#authenticating-users)하거나 [Laravel Fortify](/docs/{{version}}/fortify) 같은 인증 패키지를 쓸 수 있습니다.

로그인 요청이 성공하면, 인증이 완료되고 이후 모든 요청에도 Laravel이 구현한 세션 쿠키로 자동 인증됩니다. 또한, 이미 `/sanctum/csrf-cookie` 라우트로 요청했으므로, JS HTTP 클라이언트가 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더에 잘 포함시키기만 하면 이후 요청도 자동으로 CSRF 보호를 받습니다.

물론, 사용자의 세션이 만료(활동 없음 등)되면, 이후 요청은 401 또는 419 HTTP 오류를 받을 수 있습니다. 이 경우 사용자를 SPA의 로그인 페이지로 리다이렉트해야 합니다.

> [!WARNING]
> `/login` 엔드포인트는 직접 구현해도 되지만, Laravel이 제공하는 표준 [세션 기반 인증 서비스](/docs/{{version}}/authentication#authenticating-users)를 반드시 사용해야 합니다. 보통 `web` 인증 가드를 써야 합니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호

모든 들어오는 요청을 인증하도록 라우트를 보호하려면, `routes/api.php`에서 API 라우트에 `sanctum` 인증 가드를 붙이세요. 이 가드는 SPA의 상태 유지 인증 요청 또는 써드파티의 API 토큰이 모두 올바르게 처리됩니다:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="authorizing-private-broadcast-channels"></a>
### 프라이빗 브로드캐스트 채널 권한 부여

SPA가 [프라이빗/프레즌스 채널](/docs/{{version}}/broadcasting#authorizing-channels) 인증이 필요하다면, `bootstrap/app.php`의 `withRouting` 메서드에서 `channels` 항목을 제거하고, 대신 `withBroadcasting` 메서드를 호출하여 브로드캐스팅 라우트에 올바른 미들웨어를 지정하세요:

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        // ...
    )
    ->withBroadcasting(
        __DIR__.'/../routes/channels.php',
        ['prefix' => 'api', 'middleware' => ['api', 'auth:sanctum']],
    )
```

그리고 Pusher의 인증 요청이 성공하려면, [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation) 초기화 시 직접 authorizer를 지정해야 합니다. 이렇게 하면 [크로스 도메인 요청](#cors-and-cookies)에 적합하게 설정된 axios 인스턴스를 사용할 수 있습니다:

```js
window.Echo = new Echo({
    broadcaster: "pusher",
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    encrypted: true,
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    authorizer: (channel, options) => {
        return {
            authorize: (socketId, callback) => {
                axios.post('/api/broadcasting/auth', {
                    socket_id: socketId,
                    channel_name: channel.name
                })
                .then(response => {
                    callback(false, response.data);
                })
                .catch(error => {
                    callback(true, error);
                });
            }
        };
    },
})
```

<a name="mobile-application-authentication"></a>
## 모바일 애플리케이션 인증

모바일 애플리케이션에서 API 요청을 인증할 때도 Sanctum 토큰을 사용할 수 있습니다. 인증 흐름은 써드파티 API 인증과 비슷하지만, API 토큰 발급 방법에 약간 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급

먼저, 사용자의 이메일/아이디, 비밀번호, 기기명을 받아 Sanctum 토큰을 발급하는 라우트를 생성하세요. 이때 "기기명"은 참고용 정보이며 아무 값이나 지정할 수 있지만, 일반적으로 사용자가 알 수 있는 이름(예: "홍길동의 iPhone 12")을 사용해야 합니다.

보통 모바일 앱의 "로그인" 화면에서 이 엔드포인트로 요청을 보내 평문 API 토큰을 받습니다. 받은 토큰은 모바일 기기에 저장해두고 이후 API 요청마다 사용하게 됩니다:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

Route::post('/sanctum/token', function (Request $request) {
    $request->validate([
        'email' => 'required|email',
        'password' => 'required',
        'device_name' => 'required',
    ]);

    $user = User::where('email', $request->email)->first();

    if (! $user || ! Hash::check($request->password, $user->password)) {
        throw ValidationException::withMessages([
            'email' => ['입력한 자격 증명이 올바르지 않습니다.'],
        ]);
    }

    return $user->createToken($request->device_name)->plainTextToken;
});
```

모바일 애플리케이션에서 토큰을 API 요청에 사용할 때는 `Authorization` 헤더에 `Bearer` 토큰 형식으로 포함해야 합니다.

> [!NOTE]
> 모바일 애플리케이션 토큰 발급 시에도 [토큰 권한](#token-abilities)을 명시할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호

앞에서 다룬 대로, 모든 요청을 인증받게 하려면 라우트에 `sanctum` 인증 가드를 붙이면 됩니다:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-mobile-api-tokens"></a>
### 토큰 폐기

사용자에게 모바일 기기에서 발급받은 API 토큰을 "계정 설정" 화면 등에서 명칭과 함께 보여주고, "폐기" 버튼을 제공할 수 있습니다. 삭제 시 데이터베이스에서 토큰을 삭제하면 됩니다. 사용자의 API 토큰은 `Laravel\Sanctum\HasApiTokens` 트레이트의 `tokens` 관계로 접근할 수 있습니다:

```php
// 모든 토큰 폐기
$user->tokens()->delete();

// 특정 토큰 폐기
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## 테스트

테스트 시에는, `Sanctum::actingAs` 메서드를 사용해 사용자를 인증하고 토큰에 권한을 부여할 수 있습니다:

```php tab=Pest
use App\Models\User;
use Laravel\Sanctum\Sanctum;

test('작업 목록을 가져올 수 있다', function () {
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Sanctum\Sanctum;

public function test_task_list_can_be_retrieved(): void
{
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
}
```

토큰에 모든 권한을 부여하고 싶다면, `actingAs` 메서드의 권한 목록에 `*`를 지정하면 됩니다:

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
