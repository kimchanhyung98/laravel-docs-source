# Laravel Sanctum

- [소개](#introduction)
    - [동작 방식](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 권한(Abilities)](#token-abilities)
    - [라우트 보호](#protecting-routes)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증](#spa-authenticating)
    - [라우트 보호](#protecting-spa-routes)
    - [비공개 브로드캐스트 채널 권한 부여](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호](#protecting-mobile-api-routes)
    - [토큰 폐기](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 앱, 단순 토큰 기반 API를 위한 경량 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 자신의 계정에 대해 여러 API 토큰을 생성할 수 있습니다. 이 토큰들은 토큰이 수행할 수 있는 동작을 지정하는 권한/스코프(Abilities/Scopes)를 부여받을 수 있습니다.

<a name="how-it-works"></a>
### 동작 방식

Laravel Sanctum은 두 가지 별개의 문제를 해결하기 위해 존재합니다. 라이브러리를 더 깊이 파헤치기 전에 각각에 대해 설명하겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰

첫째, Sanctum은 OAuth의 복잡함 없이도 사용자의 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 Github 및 기타 "개인 액세스 토큰"을 발급하는 서비스에서 영감을 얻었습니다. 예를 들어, 애플리케이션의 "계정 설정" 화면에서 사용자가 자신의 계정에 대해 API 토큰을 생성할 수 있다고 가정해 보세요. 이때 Sanctum을 사용해 토큰을 생성 및 관리할 수 있습니다. 이런 토큰은 일반적으로 매우 긴 만료 기간(수년)을 가지지만, 사용자가 언제든 수동으로 폐기할 수 있습니다.

Laravel Sanctum은 사용자 API 토큰을 단일 데이터베이스 테이블에 저장하고, 유효한 API 토큰이 포함된 `Authorization` 헤더를 통해 들어오는 HTTP 요청을 인증하는 방식으로 이 기능을 제공합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증

둘째, Sanctum은 Laravel 기반 API와 통신이 필요한 싱글 페이지 애플리케이션(SPA)에서 간단히 인증할 수 있도록 지원합니다. 이 SPA는 Laravel 애플리케이션과 같은 저장소에 있을 수도 있고, Next.js나 Nuxt로 생성된 분리된 저장소일 수도 있습니다.

이 기능에서는 어떤 종류의 토큰도 사용하지 않습니다. Sanctum은 Laravel의 내장 쿠키 기반 세션 인증 기능을 사용합니다. 보통 Sanctum은 이 목적을 위해 Laravel의 `web` 인증 가드를 사용합니다. 덕분에 CSRF 보호, 세션 인증, XSS를 통한 인증 정보 유출 방지 등의 이점을 누릴 수 있습니다.

Sanctum은 들어오는 요청이 SPA 프론트엔드에서 온 경우에만 쿠키 인증을 시도합니다. Sanctum이 들어오는 HTTP 요청을 검사할 때, 우선 인증 쿠키를 확인하고 없으면 `Authorization` 헤더를 체크하여 유효한 API 토큰이 있는지 검사합니다.

> [!NOTE]
> Sanctum을 API 토큰 인증에만 사용하거나 SPA 인증에만 사용하는 것 모두 문제없습니다. Sanctum을 사용한다고 해서 두 가지 기능 모두를 반드시 사용할 필요는 없습니다.

<a name="installation"></a>
## 설치

`install:api` Artisan 명령어를 통해 Laravel Sanctum을 설치할 수 있습니다:

```shell
php artisan install:api
```

다음으로, Sanctum을 SPA 인증에 사용할 경우 문서의 [SPA 인증](#spa-authentication) 섹션을 참고하세요.

<a name="configuration"></a>
## 설정

<a name="overriding-default-models"></a>
### 기본 모델 재정의

일반적으로 필요하지는 않지만, Sanctum 내부적으로 사용하는 `PersonalAccessToken` 모델을 확장할 수 있습니다:

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

그런 다음, Sanctum이 사용자 정의 모델을 사용하도록 `usePersonalAccessTokenModel` 메서드로 지정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 파일의 `boot` 메서드에서 호출합니다:

```php
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a name="api-token-authentication"></a>
## API 토큰 인증

> [!NOTE]
> 자체 1st-party SPA 인증에는 API 토큰을 사용하지 말고, Sanctum의 내장 [SPA 인증 기능](#spa-authentication)을 활용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급

Sanctum을 사용하면 API 요청을 인증할 수 있는 API 토큰/개인 액세스 토큰을 발급할 수 있습니다. API 토큰을 사용할 때는 토큰을 `Authorization` 헤더에 `Bearer` 토큰 방식으로 포함해야 합니다.

사용자를 위해 토큰을 발급하려면 User 모델에 `Laravel\Sanctum\HasApiTokens` 트레이트를 적용하세요:

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

토큰을 발급하려면 `createToken` 메서드를 사용하면 됩니다. 이 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전에 SHA-256 해싱을 거치지만, `NewAccessToken` 인스턴스의 `plainTextToken` 속성을 통해 토큰의 평문 값을 얻을 수 있습니다. 토큰이 발급된 후 즉시 이 값을 사용자에게 보여줘야 합니다:

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
### 토큰 권한(Abilities)

Sanctum에서는 토큰에 “권한(Abilities)”을 부여할 수 있습니다. 권한은 OAuth의 "스코프"와 유사한 목적으로 사용됩니다. 토큰을 생성할 때 `createToken` 메서드의 두 번째 인수에 문자열 권한 배열을 넘길 수 있습니다:

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Sanctum으로 인증된 요청을 처리할 때, `tokenCan` 또는 `tokenCant` 메서드로 해당 권한이 있는지 확인할 수 있습니다:

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

Sanctum에는 특정 권한이 부여된 토큰으로 인증되었는지 확인하는 두 가지 미들웨어가 포함되어 있습니다. 먼저, 애플리케이션의 `bootstrap/app.php` 파일에 다음 미들웨어 별칭을 등록합니다:

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

`abilities` 미들웨어는 들어오는 요청 토큰에 모든 권한이 있는지 확인합니다:

```php
Route::get('/orders', function () {
    // "check-status" 및 "place-orders" 권한 모두 가지고 있는 토큰만 접근 가능
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` 미들웨어는 나열된 권한 중 **하나 이상** 가지고 있는지 확인합니다:

```php
Route::get('/orders', function () {
    // "check-status" 또는 "place-orders" 권한 중 하나라도 있으면 접근 가능
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### 1st-party UI에서 시작된 요청

편의상, Sanctum의 내장 [SPA 인증](#spa-authentication)을 사용하는 경우, 자체 1st-party SPA에서 온 인증 요청에 대해 `tokenCan` 메서드는 항상 `true`를 반환합니다.

그러나 이것이 반드시 사용자가 해당 동작을 수행할 수 있어야 함을 의미하진 않습니다. 일반적으로 애플리케이션의 [인증 정책](/docs/{{version}}/authorization#creating-policies)에서 해당 권한이 허용되었는지 여부 및 실제 사용자 인스턴스가 동작을 수행할 수 있어야 하는지를 추가로 확인합니다.

예를 들어 서버 관리 애플리케이션이라면, 토큰에 서버 업데이트 권한이 있고 **서버가 해당 사용자 소유인지**도 확인할 수 있습니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

처음에는 UI에서 요청이 발생한 경우 `tokenCan`이 항상 참이 되도록 허용하는 것이 이상하게 보일 수 있지만, 언제나 API 토큰이 존재한다고 가정하는 것이 더 편리합니다. 이렇게 하면 UI 요청과 타사 API 소비자 요청 모두에서 인증 정책 내에서 안심하고 `tokenCan`을 사용할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호

모든 요청에서 인증이 필요하도록 라우트를 보호하려면, `routes/web.php` 또는 `routes/api.php` 라우트 파일의 보호 대상 라우트에 `sanctum` 인증 가드를 지정하세요. 이 가드는 들어오는 요청이 상태 저장 쿠키 인증이든, 유효한 API 토큰을 갖고 있는 타사 요청이든 상관없이 인증을 보장합니다.

왜 `routes/web.php`에서 인증을 추천하는지 궁금할 수 있습니다. Sanctum은 우선 Laravel의 일반 세션 인증 쿠키를 검사하고, 쿠키가 없으면 요청의 `Authorization` 헤더의 토큰을 검사합니다. 또한 모든 요청을 Sanctum으로 인증하면 항상 현재 인증된 사용자 인스턴스에서 `tokenCan`을 호출할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-tokens"></a>
### 토큰 폐기

`Laravel\Sanctum\HasApiTokens` 트레이트에서 제공하는 `tokens` 관계를 통해 토큰을 데이터베이스에서 삭제해 "폐기"할 수 있습니다:

```php
// 모든 토큰 폐기
$user->tokens()->delete();

// 현재 요청에서 사용된 토큰 폐기
$request->user()->currentAccessToken()->delete();

// 특정 토큰 폐기
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### 토큰 만료

기본적으로 Sanctum 토큰은 만료되지 않으며, [토큰 폐기](#revoking-tokens)를 통해서만 무효화할 수 있습니다. 만약 토큰 만료 시간을 설정하고 싶다면, 애플리케이션의 `sanctum` 설정 파일에서 `expiration` 옵션을 통해 분(minute) 단위로 지정할 수 있습니다:

```php
'expiration' => 525600,
```

각 토큰별로 만료 시간을 지정하고 싶다면, `createToken` 메서드의 세 번째 인수로 만료 시간을 넘겨주면 됩니다:

```php
return $user->createToken(
    'token-name', ['*'], now()->addWeek()
)->plainTextToken;
```

애플리케이션에 토큰 만료 시간을 설정했다면, [스케줄 작업](/docs/{{version}}/scheduling)을 추가해 만료된 토큰을 주기적으로 정리할 수도 있습니다. Sanctum은 이를 위한 `sanctum:prune-expired` Artisan 명령어를 제공합니다. 예시로, 만료된 지 24시간 이상 된 토큰 레코드를 매일 삭제하는 작업을 스케줄링할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증

Sanctum은 Laravel 기반 API와 통신해야 하는 싱글 페이지 애플리케이션(SPA)을 간단하게 인증하도록 설계되었습니다. 이 SPA는 Laravel 애플리케이션과 같은 저장소일 수도, 분리된 저장소일 수도 있습니다.

이 기능에서는 어떤 종류의 토큰도 사용하지 않고, Laravel의 내장 쿠키 기반 세션 인증 서비스를 사용합니다. 이렇게 하면 CSRF 보호, 세션 인증, 인증 정보의 XSS 유출 방지 등 다양한 보안상의 이점을 누릴 수 있습니다.

> [!WARNING]
> SPA와 API는 반드시 동일한 최상위 도메인을 공유해야 하고, 서로 다른 서브도메인에 위치해도 괜찮습니다. 또한 요청 시 `Accept: application/json` 헤더와 `Referer` 또는 `Origin` 헤더를 반드시 포함해야 합니다.

<a name="spa-configuration"></a>
### 설정

<a name="configuring-your-first-party-domains"></a>
#### 1st-party 도메인 설정

먼저, SPA가 요청을 보내는 도메인을 설정하세요. 이는 `sanctum` 설정 파일의 `stateful` 옵션을 통해 지정할 수 있습니다. 이 설정은 어떤 도메인이 API에 요청을 보낼 때 Laravel 세션 쿠키를 통해 "상태 유지(stateful)" 인증을 할지 결정합니다.

Stateful 도메인 설정을 돕기 위해 Sanctum에서는 두 개의 헬퍼 함수를 제공합니다. `Sanctum::currentApplicationUrlWithPort()`는 `APP_URL` 환경변수에서 현재 애플리케이션 URL을 반환하고, `Sanctum::currentRequestHost()`는 런타임 도중 요청의 호스트로 대체되는 플레이스홀더를 stateful 도메인 목록에 추가합니다.

> [!WARNING]
> 만약 포트가 포함된 URL(`127.0.0.1:8000`)로 접근한다면, 도메인에 포트 번호도 반드시 포함해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

다음으로, SPA에서 온 요청은 Laravel 세션 쿠키로 인증하고, 타사나 모바일 앱에서 온 요청은 API 토큰으로 인증하도록 Laravel에 알려야 합니다. 이는 애플리케이션의 `bootstrap/app.php`에서 `statefulApi` 미들웨어 메서드를 호출하면 간단히 처리가 가능합니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->statefulApi();
})
```

<a name="cors-and-cookies"></a>
#### CORS와 쿠키

분리된 서브도메인에서 실행되는 SPA에서 인증이 잘 되지 않는다면 CORS(교차 출처 리소스 공유) 또는 세션 쿠키 설정이 잘못되었을 가능성이 있습니다.

`config/cors.php` 설정 파일은 기본적으로 게시(publish)되지 않습니다. Laravel의 CORS 옵션을 커스터마이즈하려면, `config:publish` Artisan 명령어로 전체 `cors` 설정 파일을 게시하세요:

```shell
php artisan config:publish cors
```

또한 CORS 설정에서 `Access-Control-Allow-Credentials` 헤더의 값이 `True`로 반환되도록 해야 합니다. 이는 `config/cors.php` 파일에서 `supports_credentials` 옵션을 `true`로 지정함으로써 가능합니다.

그리고 애플리케이션의 전역 `axios` 인스턴스에서 `withCredentials`와 `withXSRFToken` 옵션을 활성화해야 합니다. 보통은 `resources/js/bootstrap.js`에서 설정합니다. 프런트엔드에서 Axios를 사용하지 않는다면, 사용하는 HTTP 클라이언트의 설정에서 이를 따로 적용해 주세요:

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

마지막으로, 세션 쿠키의 도메인이 루트 도메인의 모든 서브도메인을 지원해야 합니다. 이는 `config/session.php` 파일에서 도메인 앞에 `.`(점)를 붙여 지정하면 됩니다:

```php
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 인증

<a name="csrf-protection"></a>
#### CSRF 보호

SPA를 인증하기 위해 우선 SPA의 "로그인" 페이지에서 `/sanctum/csrf-cookie` 엔드포인트에 요청을 보내 CSRF 보호를 초기화해야 합니다:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // 로그인 처리…
});
```

이 요청 시 Laravel은 현재 CSRF 토큰을 담은 `XSRF-TOKEN` 쿠키를 발급합니다. 이 토큰은 URL 디코딩된 후 차후 요청의 `X-XSRF-TOKEN` 헤더에 담겨야 하며, Axios나 Angular HttpClient 같은 HTTP 라이브러리는 이를 자동으로 처리해 줍니다. 만약 사용하는 라이브러리가 자동으로 값을 넣어주지 않는다면, `XSRF-TOKEN` 쿠키에 저장된 값을 URL 디코딩해서 `X-XSRF-TOKEN` 헤더에 직접 세팅해야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호가 초기화되면, Laravel 애플리케이션의 `/login` 라우트에 `POST` 요청을 보내야 합니다. `/login` 라우트는 [직접 구현](/docs/{{version}}/authentication#authenticating-users)하거나 [Laravel Fortify](/docs/{{version}}/fortify) 등의 인증 패키지로 구현할 수 있습니다.

로그인 요청이 성공하면 인증이 완료되고, 클라이언트의 세션 쿠키를 통해 이후 요청들이 자동으로 인증됩니다. 또한 `/sanctum/csrf-cookie` 경로에 이미 요청했기 때문에, HTTP 클라이언트가 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더에 전달하는 한, 차후 요청들 역시 자동으로 CSRF 보호를 받게 됩니다.

물론, 사용자의 세션이 만료되면 이후 Laravel 요청에서 401 또는 419 에러가 발생할 수 있습니다. 이 경우 사용자를 SPA의 로그인 페이지로 리다이렉트 시켜야 합니다.

> [!WARNING]
> `/login` 엔드포인트를 직접 구현해도 상관없으나, 반드시 Laravel이 제공하는 표준 [세션 기반 인증 서비스](/docs/{{version}}/authentication#authenticating-users)로 사용자를 인증해야 합니다. 보통은 `web` 인증 가드를 사용합니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호

모든 요청이 인증되어야 하는 API 라우트에는 `routes/api.php` 파일에서 `sanctum` 인증 가드를 적용하세요. 이것은 SPA의 상태 저장 인증 요청이든, 유효한 API 토큰을 가진 타사 요청이든 인증을 보장합니다:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="authorizing-private-broadcast-channels"></a>
### 비공개 브로드캐스트 채널 권한 부여

SPA가 [비공개 또는 presence 브로드캐스트 채널](/docs/{{version}}/broadcasting#authorizing-channels)에 인증해야 한다면, 애플리케이션의 `bootstrap/app.php` 파일 내 `withRouting` 메서드에서 `channels` 항목을 제거하세요. 대신, `withBroadcasting` 메서드를 호출하여 브로드캐스트 라우트에 적절한 미들웨어를 지정할 수 있습니다:

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

그리고, Pusher 인증 요청이 성공하려면 [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation)를 초기화할 때 커스텀 Pusher `authorizer`를 제공해야 합니다. 이렇게 하면 [CORS 및 쿠키 처리가 올바르게 설정된](#cors-and-cookies) `axios` 인스턴스를 사용할 수 있습니다:

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

모바일 애플리케이션의 API 요청을 인증하는 데도 Sanctum 토큰을 사용할 수 있습니다. 모바일 앱 인증 방식은 서드파티 API 요청 인증과 유사하지만, API 토큰 발급 방식에 일부 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급

먼저 사용자의 이메일/유저명, 비밀번호, 디바이스명을 받아 새로운 Sanctum 토큰으로 교환하는 라우트를 생성하세요. 이때 "디바이스명"은 정보 제공용이고, 원하는 어떤 값이든 허용됩니다. 보통은 사용자가 식별 가능한 기기명을 씁니다(예: "Nuno의 iPhone 12").

일반적으로 모바일 앱의 "로그인" 화면에서 이 엔드포인트로 요청을 보내고, 엔드포인트는 평문 API 토큰을 반환합니다. 반환된 토큰은 모바일 기기에 저장해 추가 API 요청을 보낼 때 사용하면 됩니다:

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
            'email' => ['The provided credentials are incorrect.'],
        ]);
    }

    return $user->createToken($request->device_name)->plainTextToken;
});
```

모바일 앱은 이 토큰을 `/api` 요청의 `Authorization` 헤더에 `Bearer` 토큰 형태로 넣어 보내야 합니다.

> [!NOTE]
> 모바일 애플리케이션을 위한 토큰 생성 시에도 [토큰 권한(Abilities)](#token-abilities)을 자유롭게 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호

앞서 설명한대로 모든 요청에서 인증이 필요하도록 `sanctum` 인증 가드를 적용할 수 있습니다:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-mobile-api-tokens"></a>
### 토큰 폐기

모바일 기기에 발급된 API 토큰을 폐기하려면, 웹 애플리케이션 UI의 "계정 설정" 등에서 토큰 이름과 함께 "폐기" 버튼을 제공할 수 있습니다. 사용자가 "폐기" 버튼을 클릭하면 해당 토큰을 데이터베이스에서 삭제하면 됩니다. 사용자의 API 토큰에는 `Laravel\Sanctum\HasApiTokens` 트레이트의 `tokens` 관계로 접근할 수 있습니다:

```php
// 모든 토큰 폐기
$user->tokens()->delete();

// 특정 토큰 폐기
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## 테스트

테스트 시에는 `Sanctum::actingAs` 메서드로 사용자를 인증하며, 토큰에 부여할 권한도 지정할 수 있습니다:

```php tab=Pest
use App\Models\User;
use Laravel\Sanctum\Sanctum;

test('task list can be retrieved', function () {
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

토큰에 모든 권한을 부여하려면, `actingAs` 메서드에 권한 리스트에 `*`를 포함하세요:

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
