# Laravel Sanctum

- [소개](#introduction)
    - [작동 원리](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 재정의하기](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급하기](#issuing-api-tokens)
    - [토큰 권한(Abilities)](#token-abilities)
    - [라우트 보호하기](#protecting-routes)
    - [토큰 취소하기](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증하기](#spa-authenticating)
    - [라우트 보호하기](#protecting-spa-routes)
    - [비공개 브로드캐스트 채널 권한 부여하기](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급하기](#issuing-mobile-api-tokens)
    - [라우트 보호하기](#protecting-mobile-api-routes)
    - [토큰 취소하기](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션 및 간단한 토큰 기반 API를 위한 가벼운 인증 시스템을 제공합니다. Sanctum을 이용하면 애플리케이션 사용자가 자신의 계정에 대해 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰에는 해당 토큰이 수행할 수 있는 작업을 지정하는 권한(abilities) 또는 범위(scopes)를 부여할 수 있습니다.

<a name="how-it-works"></a>
### 작동 원리 (How it Works)

Laravel Sanctum은 두 가지 별개의 문제를 해결하기 위해 설계되었습니다. 라이브러리를 자세히 살펴보기 전에 각각의 문제를 먼저 설명하겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰

첫째, Sanctum은 OAuth 같은 복잡한 과정을 거치지 않고도 사용자에게 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 GitHub 등에서 사용하는 "개인 접근 토큰(personal access tokens)"에서 영감을 받았습니다. 예를 들어, 애플리케이션의 "계정 설정" 화면에서 사용자가 자신의 계정에 대해 API 토큰을 생성할 수 있다고 가정해봅시다. Sanctum을 사용하면 이러한 토큰을 생성하고 관리할 수 있습니다. 이 토큰들은 일반적으로 만료 기간이 매우 길며(몇 년 단위), 사용자가 언제든지 수동으로 취소할 수 있습니다.

Laravel Sanctum은 사용자 API 토큰을 하나의 데이터베이스 테이블에 저장하고, 들어오는 HTTP 요청에서 `Authorization` 헤더에 유효한 API 토큰이 포함되었는지 확인하여 인증합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증

둘째, Sanctum은 Laravel API와 통신하는 SPA를 간단하게 인증하는 방법을 제공합니다. 이 SPA들은 Laravel 애플리케이션과 같은 저장소에 있을 수도 있고, Next.js나 Nuxt 같은 별도의 저장소에 있을 수도 있습니다.

이 경우 Sanctum은 어떤 종류의 토큰도 사용하지 않습니다. 대신 Laravel의 내장된 쿠키 기반 세션 인증 서비스를 사용합니다. 보통 Sanctum은 Laravel의 `web` 인증 가드를 이용해서 이 기능을 수행합니다. 이 방법은 CSRF 보호, 세션 인증 기능, 그리고 XSS로 인한 인증 정보 누출 방지 등 여러 이점이 있습니다.

Sanctum은 들어오는 요청이 사용자 SPA 프론트엔드에서 온 경우에만 쿠키 기반 인증을 시도합니다. 요청을 처리할 때 먼저 인증 쿠키를 탐색하고, 쿠키가 없으면 `Authorization` 헤더에 포함된 API 토큰을 확인합니다.

> [!NOTE]
> Sanctum을 API 토큰 인증용으로만 사용하거나 SPA 인증용으로만 사용할 수 있습니다. Sanctum을 쓴다고 해서 두 가지 기능을 모두 반드시 사용해야 하는 것은 아닙니다.

<a name="installation"></a>
## 설치 (Installation)

Laravel Sanctum은 `install:api` Artisan 명령어로 설치할 수 있습니다:

```shell
php artisan install:api
```

SPA 인증 기능을 사용하려면, 이 문서의 [SPA 인증](#spa-authentication) 섹션을 참고하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="overriding-default-models"></a>
### 기본 모델 재정의하기 (Overriding Default Models)

보통 필요하지는 않지만, Sanctum 내부에서 사용하는 `PersonalAccessToken` 모델을 확장해서 사용할 수 있습니다:

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

그다음, Sanctum에 사용자 정의 모델을 사용하도록 `usePersonalAccessTokenModel` 메서드로 알려줄 수 있습니다. 보통 이 메서드는 애플리케이션의 `AppServiceProvider` 파일의 `boot` 메서드에서 호출합니다:

```php
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a name="api-token-authentication"></a>
## API 토큰 인증 (API Token Authentication)

> [!NOTE]
> 자체 SPA 인증에는 API 토큰을 사용하지 마시고, Sanctum의 내장 [SPA 인증](#spa-authentication) 기능을 사용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급하기 (Issuing API Tokens)

Sanctum을 사용하면 API 요청을 인증하는 데 사용할 수 있는 API 토큰(또는 개인 접근 토큰)을 발급할 수 있습니다. API 토큰을 사용하는 요청은 `Authorization` 헤더에 `Bearer` 토큰으로 포함시켜야 합니다.

사용자에 대한 토큰 발급을 시작하려면 User 모델에 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용해야 합니다:

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

토큰을 발급하려면 `createToken` 메서드를 사용하면 됩니다. `createToken` 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장하기 전에 SHA-256 해싱으로 암호화되지만, `NewAccessToken` 인스턴스의 `plainTextToken` 속성을 통해 원본 텍스트 값을 바로 확인할 수 있습니다. 토큰을 생성한 직후 사용자에게 이 값을 보여줘야 합니다:

```php
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

사용자의 모든 토큰은 `HasApiTokens` 트레이트에서 제공하는 `tokens` Eloquent 연관관계를 통해 조회할 수 있습니다:

```php
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
### 토큰 권한(Abilities) (Token Abilities)

Sanctum은 토큰에 "abilities"라 불리는 권한을 부여할 수 있습니다. abilities는 OAuth의 "범위(scopes)"와 유사한 개념입니다. `createToken` 메서드의 두 번째 인자로 문자열 형태의 권한 배열을 넘길 수 있습니다:

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Sanctum으로 인증된 요청을 처리할 때, 토큰에 특정 권한이 부여되었는지 여부는 `tokenCan` 또는 `tokenCant` 메서드를 사용해 판단할 수 있습니다:

```php
if ($user->tokenCan('server:update')) {
    // ...
}

if ($user->tokenCant('server:update')) {
    // ...
}
```

<a name="token-ability-middleware"></a>
#### 토큰 권한 미들웨어 (Token Ability Middleware)

Sanctum은 지정된 권한이 부여된 토큰으로 인증된 요청인지 확인하는 데 사용할 수 있는 두 개의 미들웨어를 제공합니다. 시작하려면, 애플리케이션의 `bootstrap/app.php` 파일에 아래와 같이 미들웨어 별칭을 정의하세요:

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

`abilities` 미들웨어는 요청 토큰이 나열된 모든 권한을 보유했는지 검증합니다:

```php
Route::get('/orders', function () {
    // 토큰이 "check-status"와 "place-orders" 권한을 모두 가지고 있을 때...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` 미들웨어는 요청 토큰이 나열된 권한 중 *하나 이상*을 보유했는지 검증합니다:

```php
Route::get('/orders', function () {
    // 토큰이 "check-status" 또는 "place-orders" 권한을 가지고 있을 때...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### 퍼스트파티 UI가 시작한 요청 (First-Party UI Initiated Requests)

편의를 위해, Sanctum의 `tokenCan` 메서드는 요청이 퍼스트파티 SPA에서 호출된 것이고 Sanctum의 내장 [SPA 인증](#spa-authentication)을 사용 중인 경우 무조건 `true`를 반환합니다.

하지만 이것이 곧 사용자가 행동을 수행할 수 있다는 의미는 아닙니다. 일반적으로 애플리케이션의 [인가 정책](/docs/master/authorization#creating-policies)이 토큰이 권한을 갖고 있는지, 그리고 사용자가 실제로 행동을 수행할 수 있는지 확인합니다.

예를 들어, 서버를 관리하는 애플리케이션이라면 아래처럼 토큰이 서버를 업데이트할 권한이 있으면서 서버가 사용자 소유인지 함께 확인할 수 있습니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

처음에는 `tokenCan` 메서드가 퍼스트파티 UI에서 실행한 요청에 대해 항상 `true`를 반환하는 것이 어색할 수 있습니다. 그러나 API 토큰이 항상 존재하고 `tokenCan`을 통해 검사할 수 있다고 가정하는 것이 편리합니다. 이런 방식을 택하면, 애플리케이션의 인가 정책 내에서 요청이 UI에서 발생했는지 또는 제3자 API 소비자가 시작했는지 신경 쓰지 않고 `tokenCan`을 호출할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호하기 (Protecting Routes)

모든 들어오는 요청이 인증되어야 하는 라우트를 보호하려면, `routes/web.php`와 `routes/api.php` 파일에서 보호할 라우트에 `sanctum` 인증 가드를 붙여야 합니다. 이 가드는 들어오는 요청이 상태 기반 쿠키 인증 요청인지 아니면 제3자의 토큰 인증 요청인지 모두 인증할 수 있게 합니다.

왜 `routes/web.php` 파일에서 Sanctum 인증 가드를 사용하는지 궁금할 수도 있는데, Sanctum은 먼저 Laravel의 세션 인증 쿠키로 인증을 시도하고, 쿠키가 없으면 `Authorization` 헤더의 토큰으로 인증을 시도하기 때문입니다. 그리고 Sanctum으로 인증된 요청에 대해 `tokenCan` 메서드를 항상 호출할 수 있다는 장점도 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-tokens"></a>
### 토큰 취소하기 (Revoking Tokens)

데이터베이스에서 토큰을 삭제해 토큰을 "취소"할 수 있습니다. `Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 관계를 통해 토큰을 관리합니다:

```php
// 모든 토큰 취소하기...
$user->tokens()->delete();

// 현재 요청을 인증하는 토큰 취소하기...
$request->user()->currentAccessToken()->delete();

// 특정 토큰 취소하기...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### 토큰 만료 (Token Expiration)

기본적으로 Sanctum 토큰은 만료되지 않으며, 오직 [토큰 취소](#revoking-tokens)를 통해서만 무효화됩니다. 그러나 애플리케이션 API 토큰에 만료 시간을 설정하려면 `sanctum` 설정 파일의 `expiration` 옵션을 조정하면 됩니다. 이 옵션은 토큰이 만료로 간주되기까지 분 단위로 시간을 지정합니다:

```php
'expiration' => 525600,
```

각 토큰마다 만료 시간을 다르게 지정하려면 `createToken` 메서드의 세 번째 인자로 만료 시간을 넘겨줄 수 있습니다:

```php
return $user->createToken(
    'token-name', ['*'], now()->addWeek()
)->plainTextToken;
```

만약 애플리케이션에 토큰 만료 시간을 설정하면, [스케줄 작업](#)을 만들어 만료된 토큰을 주기적으로 정리하는 것이 좋습니다. 다행히 Sanctum은 `sanctum:prune-expired` Artisan 명령어를 제공하여 만료된 토큰을 쉽게 삭제할 수 있습니다. 예를 들어, 만료된 지 24시간 지난 토큰을 매일 삭제하는 작업은 아래처럼 설정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

Sanctum은 Laravel API와 통신하는 SPA를 간단히 인증하는 방법도 제공합니다. 이 SPA는 Laravel 애플리케이션과 같은 저장소에 있을 수도 있고, 별도의 저장소에 있을 수도 있습니다.

이 경우 Sanctum은 토큰을 사용하지 않습니다. 대신 Laravel의 내장 쿠키 기반 세션 인증 서비스를 이용합니다. 이 인증 방식은 CSRF 보호, 세션 인증, 그리고 XSS 공격에 의한 인증 정보 누출 방지 등 여러 이점이 있습니다.

> [!WARNING]
> SPA와 API는 동일한 최상위 도메인을 사용해야 합니다. 다만 서로 다른 서브도메인에 위치할 수 있습니다. 그리고 요청에 `Accept: application/json` 헤더와 `Referer` 또는 `Origin` 헤더를 반드시 포함시키도록 해야 합니다.

<a name="spa-configuration"></a>
### 설정 (Configuration)

<a name="configuring-your-first-party-domains"></a>
#### 퍼스트파티 도메인 설정하기

먼저 SPA가 요청을 보낼 도메인을 설정해야 합니다. 이는 `sanctum` 설정 파일의 `stateful` 옵션을 통해 할 수 있습니다. 이 설정은 어떤 도메인들이 API에 요청할 때 Laravel 세션 쿠키를 사용해 "상태 기반(stateful)" 인증을 유지할지 결정합니다.

> [!WARNING]
> 만약 포트 번호가 포함된 주소(예: `127.0.0.1:8000`)로 애플리케이션에 접근한다면, 포트 번호까지 정확히 포함해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

그다음, SPA에서 온 요청은 Laravel 세션 쿠키로 인증하되, 제3자나 모바일 앱 요청은 API 토큰을 사용하도록 Laravel에 알려야 합니다. 이는 `bootstrap/app.php` 파일에서 `statefulApi` 미들웨어 메서드를 호출해서 간단히 설정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->statefulApi();
})
```

<a name="cors-and-cookies"></a>
#### CORS 및 쿠키

만약 다른 서브도메인에서 SPA가 실행되어 인증 문제가 생긴다면, CORS(Cross-Origin Resource Sharing)와 세션 쿠키 설정을 잘못했을 가능성이 큽니다.

`config/cors.php` 파일은 기본으로 게시되지 않으므로, Laravel의 CORS 옵션을 직접 맞추고 싶으면 `config:publish` Artisan 명령어로 전체 설정 파일을 게시하세요:

```shell
php artisan config:publish cors
```

그리고 `config/cors.php` 파일에서 `supports_credentials` 옵션을 `true`로 설정해 `Access-Control-Allow-Credentials` 헤더가 반환되도록 해야 합니다.

또한, SPA의 전역 `axios` 인스턴스에 `withCredentials`와 `withXSRFToken` 옵션을 활성화해야 합니다. 일반적으로 `resources/js/bootstrap.js` 파일에서 설정하며, 만약 axios를 사용하지 않는다면 사용하는 HTTP 클라이언트에 맞게 동일한 설정을 해야 합니다:

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

마지막으로, 세션 쿠키의 도메인 설정이 루트 도메인의 서브도메인들도 지원해야 합니다. `config/session.php` 설정에서 도메인 앞에 `.`(점)를 붙여서 설정하세요:

```php
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 인증하기 (Authenticating)

<a name="csrf-protection"></a>
#### CSRF 보호

SPA 인증을 위해서는 "로그인" 페이지가 먼저 `/sanctum/csrf-cookie` 엔드포인트를 요청해 CSRF 보호를 활성화해야 합니다:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // 로그인 요청...
});
```

이 요청에서 Laravel은 현재 CSRF 토큰을 담은 `XSRF-TOKEN` 쿠키를 설정합니다. 이후 요청 헤더에 `X-XSRF-TOKEN`에 이 쿠키 값을 URL 디코딩한 값을 전달해야 하며, axios나 Angular HttpClient 같은 일부 HTTP 라이브러리는 이를 자동으로 처리합니다. 직접 설정할 경우 `XSRF-TOKEN` 쿠키 값을 URL 디코딩해 `X-XSRF-TOKEN` 헤더에 넣어야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호가 활성화된 후, Laravel 애플리케이션의 `/login` 라우트에 `POST` 요청을 보내 로그인합니다. 이 라우트는 [직접 구현](/docs/master/authentication#authenticating-users)하거나 [Laravel Fortify](/docs/master/fortify) 같은 헤드리스 인증 패키지를 사용할 수 있습니다.

로그인에 성공하면 인증되며, 이후 요청은 Laravel에서 발행한 세션 쿠키로 자동 인증됩니다. `/sanctum/csrf-cookie` 경로도 미리 요청했으므로, JavaScript HTTP 클라이언트가 `XSRF-TOKEN` 쿠키 값을 반드시 `X-XSRF-TOKEN` 헤더에 넣어 보내면 CSRF 보호가 계속 유지됩니다.

만약 사용자의 세션이 비활성으로 인해 만료되면, 401 또는 419 HTTP 에러가 발생할 수 있고, 이때는 사용자를 SPA 로그인 페이지로 리다이렉트해야 합니다.

> [!WARNING]
> 직접 `/login` 엔드포인트를 작성해도 되지만, 반드시 Laravel이 제공하는 표준 [세션 기반 인증 서비스](/docs/master/authentication#authenticating-users)를 이용해 인증하도록 해야 합니다. 보통 `web` 인증 가드를 사용합니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호하기 (Protecting Routes)

들어오는 모든 요청이 인증되어야 하는 API 라우트에는 `routes/api.php` 파일에서 `sanctum` 인증 가드를 붙여야 합니다. 이 가드는 SPA의 상태 기반 인증 요청이나 제3자의 유효한 API 토큰 요청 모두 인증할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="authorizing-private-broadcast-channels"></a>
### 비공개 브로드캐스트 채널 권한 부여하기 (Authorizing Private Broadcast Channels)

SPA가 [비공개 또는 출석 브로드캐스트 채널](/docs/master/broadcasting#authorizing-channels)을 인증해야 하는 경우, 애플리케이션의 `bootstrap/app.php` 파일에서 `withRouting` 메서드에 포함된 `channels` 항목을 제거하세요. 그리고 대신 `withBroadcasting` 메서드를 호출하여 브로드캐스트 라우트에 적절한 미들웨어를 지정해야 합니다:

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

그리고 Pusher 권한 요청이 성공하려면, [Laravel Echo](/docs/master/broadcasting#client-side-installation) 초기화 시에 커스텀 Pusher `authorizer`를 제공해야 합니다. 이 설정은 크로스 도메인 요청에 적절히 설정된 `axios` 인스턴스를 사용하도록 해 줍니다:

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
## 모바일 애플리케이션 인증 (Mobile Application Authentication)

Sanctum 토큰은 모바일 애플리케이션에서 API 요청을 인증하는 데 사용할 수도 있습니다. 모바일 애플리케이션 인증은 제3자 API 요청 인증과 비슷하지만, 토큰 발급 과정에 약간 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급하기 (Issuing API Tokens)

시작하려면, 사용자 이메일/사용자명, 비밀번호, 그리고 디바이스 이름을 받는 라우트를 만들고, 이 정보를 바탕으로 새 Sanctum 토큰을 발급하는 로직을 작성해야 합니다. 디바이스 이름은 사용자가 인식하기 쉬운 이름이면 됩니다. 예를 들어 "Nuno's iPhone 12" 등이 될 수 있습니다.

보통 모바일 애플리케이션 로그인 화면에서 이 토큰 발급 라우트에 요청을 보내고, 반환된 원문 API 토큰을 모바일 기기에 저장하여 추가 API 요청에 사용합니다:

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

모바일 애플리케이션은 발급받은 토큰을 `Authorization` 헤더에 `Bearer` 토큰으로 포함해 API 요청을 보냅니다.

> [!NOTE]
> 모바일 애플리케이션용 토큰을 발급할 때도 [토큰 권한](#token-abilities)을 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호하기 (Protecting Routes)

앞서 설명한 대로 보호하려는 라우트에 `sanctum` 인증 가드를 적용하면, 모든 들어오는 요청이 인증 요구합니다:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-mobile-api-tokens"></a>
### 토큰 취소하기 (Revoking Tokens)

사용자가 모바일 기기에 발급한 토큰을 취소할 수 있도록, 웹 애플리케이션 "계정 설정" UI에서 토큰 목록과 함께 "취소" 버튼을 표시할 수 있습니다. 사용자가 "취소" 버튼을 누르면 데이터베이스에서 해당 토큰을 삭제하면 됩니다. `Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 관계를 이용해 토큰을 관리하세요:

```php
// 모든 토큰 취소하기...
$user->tokens()->delete();

// 특정 토큰 취소하기...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 시에는 `Sanctum::actingAs` 메서드를 사용해 사용자를 인증하고 토큰에 부여할 권한을 지정할 수 있습니다:

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

모든 권한을 부여하려면 `actingAs` 메서드에 `'*'`를 포함시키면 됩니다:

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```