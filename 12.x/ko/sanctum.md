# Laravel Sanctum

- [소개](#introduction)
    - [동작 방식](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 권한(abilities)](#token-abilities)
    - [라우트 보호](#protecting-routes)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증 과정](#spa-authenticating)
    - [SPA 라우트 보호](#protecting-spa-routes)
    - [개인 브로드캐스트 채널 권한 부여](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호](#protecting-mobile-api-routes)
    - [토큰 폐기](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(single page applications), 모바일 애플리케이션, 그리고 간단한 토큰 기반 API를 위한 가벼운 인증 시스템을 제공합니다. Sanctum을 사용하면 각 사용자가 자신의 계정에 대해 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰들에는 토큰이 수행할 수 있는 작업을 지정하는 권한(abilities) 또는 범위(scopes)를 부여할 수 있습니다.

<a name="how-it-works"></a>
### 동작 방식 (How it Works)

Laravel Sanctum은 두 가지 문제를 해결하기 위해 존재합니다. 라이브러리 내용을 깊이 파기 전에 각각을 알아보겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰 (API Tokens)

먼저, Sanctum은 OAuth의 복잡함 없이 사용자에게 API 토큰을 발급하는 간단한 패키지입니다. 이 기능은 GitHub와 같은 애플리케이션에서 발급하는 "개인 액세스 토큰(personal access tokens)"에서 영감을 받았습니다. 예를 들어, 애플리케이션의 "계정 설정" 화면에서 사용자가 자신의 계정에 대해 API 토큰을 생성할 수 있다고 가정해봅시다. Sanctum을 사용하여 이러한 토큰을 생성하고 관리할 수 있습니다. 이 토큰들은 보통 수년간 매우 긴 만료 시간을 가지지만, 사용자가 언제든지 수동으로 토큰을 폐기할 수 있습니다.

Laravel Sanctum은 사용자 API 토큰을 단일 데이터베이스 테이블에 저장하고, 유효한 API 토큰이 포함된 `Authorization` 헤더를 통해 들어오는 HTTP 요청을 인증하는 방식으로 이 기능을 제공합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증 (SPA Authentication)

두 번째로, Sanctum은 Laravel 기반 API와 통신해야 하는 SPA(single page application)를 간단하게 인증할 방법을 제공합니다. 이러한 SPA들은 동일한 저장소(repository)에 존재할 수도 있고, Next.js 또는 Nuxt와 같이 완전히 별개의 저장소로 존재할 수도 있습니다.

이 기능을 위해 Sanctum은 어떤 토큰도 사용하지 않습니다. 대신, Laravel의 내장된 쿠키 기반 세션 인증 서비스를 활용합니다. 일반적으로 Sanctum은 Laravel의 `web` 인증 가드를 사용하여 이를 수행합니다. 이렇게 하면 CSRF 보호와 세션 인증은 물론, XSS 공격으로부터 인증 자격 증명 노출을 방지할 수 있습니다.

Sanctum은 들어오는 요청이 자신의 SPA 프론트엔드에서 온 경우에만 쿠키를 사용해 인증을 시도합니다. 요청이 들어오면 Sanctum은 먼저 인증 쿠키를 확인하고 없으면 `Authorization` 헤더 내 유효한 API 토큰을 확인합니다.

> [!NOTE]
> Sanctum을 API 토큰 인증에만 사용하거나 SPA 인증에만 사용할 수도 있습니다. Sanctum을 사용한다고 해서 두 기능을 모두 반드시 사용해야 하는 것은 아닙니다.

<a name="installation"></a>
## 설치 (Installation)

Laravel Sanctum은 다음 `install:api` Artisan 명령어로 설치할 수 있습니다:

```shell
php artisan install:api
```

그 다음, SPA 인증 기능을 이용할 예정이라면 본 문서의 [SPA 인증](#spa-authentication) 부분을 참고하세요.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="overriding-default-models"></a>
### 기본 모델 재정의 (Overriding Default Models)

보통 필요하지는 않지만, Sanctum이 내부적으로 사용하는 `PersonalAccessToken` 모델을 확장할 수 있습니다:

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

그 다음, `usePersonalAccessTokenModel` 메서드를 통해 Sanctum에 커스텀 모델을 사용하도록 지시할 수 있습니다. 보통 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다:

```php
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a name="api-token-authentication"></a>
## API 토큰 인증 (API Token Authentication)

> [!NOTE]
> 1차 당사자 SPA를 인증하기 위해 API 토큰을 사용하는 것은 권장하지 않습니다. 대신 Sanctum 내장 [SPA 인증 기능](#spa-authentication)을 사용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

Sanctum은 API 요청 인증에 사용할 수 있는 API 토큰(개인 액세스 토큰)을 발급할 수 있게 합니다. API 토큰을 이용해 요청할 경우 `Authorization` 헤더에 `Bearer` 토큰 형식으로 토큰을 포함해야 합니다.

토큰 발급을 위해 User 모델에 `Laravel\Sanctum\HasApiTokens` 트레이트를 추가하세요:

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

토큰 발급은 `createToken` 메서드를 호출하는데, 이 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. 토큰은 데이터베이스에 저장되기 전에 SHA-256 해시 방식으로 해시되지만, 생성 직후 사용자에게 보여주기 위해 `plainTextToken` 속성으로 평문 토큰 값을 얻을 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

사용자가 가진 모든 토큰은 `HasApiTokens` 트레이트가 제공하는 `tokens` Eloquent 연관관계를 통해 접근할 수 있습니다:

```php
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
### 토큰 권한(abilities) (Token Abilities)

Sanctum은 토큰에 "abilities"(권한)을 지정할 수 있습니다. OAuth의 "scopes"와 비슷한 개념입니다. `createToken` 메서드의 두 번째 인자로 문자열 배열 형태의 권한 목록을 전달할 수 있습니다:

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Sanctum 인증을 거친 요청을 처리할 때, 토큰에 특정 권한이 있는지 `tokenCan` 또는 `tokenCant` 메서드로 확인할 수 있습니다:

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

Sanctum에는 인가된 요청이 지정된 권한을 가진 토큰인지 검증하는 두 가지 미들웨어가 포함되어 있습니다. 시작하려면 애플리케이션의 `bootstrap/app.php` 파일에서 다음 미들웨어 별칭을 정의하세요:

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

`abilities` 미들웨어는 해당 라우트에 할당된 토큰이 모든 나열된 권한을 가졌는지 검증합니다:

```php
Route::get('/orders', function () {
    // 토큰이 "check-status"와 "place-orders" 권한 모두 보유...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` 미들웨어는 토큰이 나열된 권한 중 적어도 하나를 보유했는지 검증합니다:

```php
Route::get('/orders', function () {
    // 토큰이 "check-status" 또는 "place-orders" 권한 중 하나 이상 보유...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### 1차 당사자 UI 발신 요청 (First-Party UI Initiated Requests)

편의를 위해, `tokenCan` 메서드는 인증된 요청이 1차 당사자 SPA에서 왔고 Sanctum의 내장 [SPA 인증](#spa-authentication)을 사용하는 경우 항상 `true`를 반환합니다.

하지만 이것이 반드시 애플리케이션이 사용자의 동작 수행을 허용해야 함을 의미하지는 않습니다. 보통 애플리케이션의 [인가 정책](/docs/12.x/authorization#creating-policies)이 토큰에 권한이 부여되었는지 그리고 사용자 인스턴스가 해당 동작을 수행할 수 있는지를 함께 판단합니다.

예를 들어, 서버를 관리하는 애플리케이션이라면, 토큰이 서버 업데이트 권한을 가지고 있고, 또한 해당 서버가 현재 사용자 소유인지 확인할 수 있습니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update');
```

처음에는 1차 당사자 UI 요청에 대해 `tokenCan`이 항상 `true`를 반환하는 것이 이상해 보일 수 있지만, 이는 API 토큰이 항상 존재하고 `tokenCan`으로 검사할 수 있다는 가정을 편리하게 만들기 위한 설계입니다. 이렇게 하면 API가 3자 클라이언트에서 호출되었는지, 애플리케이션 UI 내부에서 호출되었는지 걱정하지 않고도 언제나 `tokenCan`을 인가 정책 내에서 호출할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

모든 들어오는 요청에 인증을 요구하려면 `routes/web.php`와 `routes/api.php` 파일에서 보호할 라우트에 `sanctum` 인증 가드를 적용하세요. 이 가드는 요청이 상태 유지 쿠키 인증 또는 유효한 API 토큰이 포함된 경우에만 인증하도록 보장합니다.

여기서 왜 `routes/web.php` 파일의 라우트에서도 `sanctum` 가드를 적용해야 하냐고 궁금할 수도 있습니다. Sanctum은 우선 Laravel의 일반적인 세션 인증 쿠키를 사용해 요청을 인증하려 시도합니다. 쿠키가 없으면 `Authorization` 헤더에 토큰이 있는지 확인합니다. 또한, `sanctum` 인증 가드를 사용하면 언제나 현재 인증된 사용자 인스턴스에 대해 `tokenCan` 메서드를 호출할 수 있다는 점도 유리합니다:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-tokens"></a>
### 토큰 폐기 (Revoking Tokens)

토큰을 "폐기"하려면 `Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 관계를 통해 데이터베이스에서 삭제하세요:

```php
// 모든 토큰 폐기...
$user->tokens()->delete();

// 현재 요청 인증에 사용된 토큰 폐기...
$request->user()->currentAccessToken()->delete();

// 특정 토큰 폐기...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### 토큰 만료 (Token Expiration)

기본적으로 Sanctum 토큰은 만료되지 않으며, 오직 [토큰 폐기](#revoking-tokens)를 통해서만 무효화됩니다. 하지만 애플리케이션의 API 토큰에 만료 시간을 설정하고 싶다면, `sanctum` 설정 파일 내 `expiration` 옵션으로 분 단위 만료 시간을 지정할 수 있습니다:

```php
'expiration' => 525600,
```

각 토큰마다 개별 만료 시간을 적용하려면 `createToken` 메서드의 세 번째 인자로 만료 시간을 전달하면 됩니다:

```php
return $user->createToken(
    'token-name', ['*'], now()->addWeek()
)->plainTextToken;
```

토큰 만료 시간을 설정했다면, 만료된 토큰을 주기적으로 정리하는 작업이 필요할 수 있습니다. Sanctum은 `sanctum:prune-expired` Artisan 명령어를 제공하므로 이를 스케줄러에 등록하여 예를 들어 24시간 이상 만료된 토큰을 삭제할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

Sanctum은 Laravel 기반 API와 통신하는 SPA(single page application)를 간단하게 인증하는 방법도 제공합니다. SPA는 Laravel 애플리케이션과 같은 저장소 내에 존재할 수도 있고, 완전히 별도의 저장소일 수도 있습니다.

이 기능에서 Sanctum은 어떤 토큰도 사용하지 않고 Laravel 내장 쿠키 기반 세션 인증 서비스를 활용합니다. 이 방식은 CSRF 보호, 세션 인증을 보장하며 XSS를 통한 인증 자격 증명 유출도 방지합니다.

> [!WARNING]
> SPA와 API는 최상위 도메인이 같아야 합니다. 서브도메인은 달라도 무방합니다. 또한 요청 시 `Accept: application/json` 헤더와 `Referer` 또는 `Origin` 헤더를 함께 보내야 합니다.

<a name="spa-configuration"></a>
### 설정 (Configuration)

<a name="configuring-your-first-party-domains"></a>
#### 1차 당사자 도메인 설정 (Configuring Your First-Party Domains)

먼저 SPA가 요청을 보내는 도메인을 설정해야 합니다. `sanctum` 설정 파일 내 `stateful` 옵션을 통해 어떤 도메인들이 세션 쿠키를 통한 "상태 유지(stateful)" 인증을 지원할지 결정할 수 있습니다.

이 설정을 쉽게 하기 위해 Sanctum은 두 가지 헬퍼 함수를 제공합니다. `Sanctum::currentApplicationUrlWithPort()`는 `APP_URL` 환경변수 기준 현재 애플리케이션 URL을 반환하며, `Sanctum::currentRequestHost()`는 현재 요청의 호스트명을 런타임에 반영하여 상태유지 도메인 리스트에 동적 플레이스홀더로 주입합니다.

> [!WARNING]
> 만약 포트가 포함된 URL(예: `127.0.0.1:8000`)로 접근한다면, 도메인에 포트 번호도 반드시 포함시켜야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

다음으로 SPA에서 들어오는 요청은 Laravel 세션 쿠키로 인증하고, 외부 요청이나 모바일 앱 요청은 API 토큰으로 인증하도록 Laravel 미들웨어를 설정해야 합니다. 이는 애플리케이션 `bootstrap/app.php` 파일 내 `statefulApi` 미들웨어 메서드를 호출해 쉽게 할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->statefulApi();
})
```

<a name="cors-and-cookies"></a>
#### CORS 및 쿠키 설정

별도 서브도메인에서 실행되는 SPA에서 인증이 안 된다면, CORS(Cross-Origin Resource Sharing) 혹은 세션 쿠키 설정이 잘못됐을 가능성이 큽니다.

`config/cors.php` 설정 파일은 기본 공개되어 있지 않습니다. CORS 설정을 커스터마이징 해야 한다면 `config:publish` Artisan 명령어로 완전한 `cors` 설정 파일을 게시하세요:

```shell
php artisan config:publish cors
```

그리고 `config/cors.php` 안 `supports_credentials` 옵션을 `true`로 설정하여 `Access-Control-Allow-Credentials` 헤더가 응답에 포함되도록 해야 합니다.

또한, 전역 axios 인스턴스에 `withCredentials`와 `withXSRFToken` 옵션을 활성화해 CSRF 쿠키 및 인증 쿠키와 연동하도록 설정하세요. 보통 `resources/js/bootstrap.js`에서 수행합니다. Axios가 아닌 다른 HTTP 클라이언트를 사용한다면 동등한 설정이 필요합니다:

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

마지막으로 세션 쿠키 도메인이 루트 도메인의 모든 서브도메인을 지원하도록 `config/session.php` 파일 내 도메인 설정에 앞에 `.`을 붙여주세요:

```php
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 인증 과정 (Authenticating)

<a name="csrf-protection"></a>
#### CSRF 보호

SPA 인증을 위해 먼저 SPA 내 "로그인" 페이지가 `/sanctum/csrf-cookie` 엔드포인트로 요청을 보내 CSRF 보호를 초기화해야 합니다:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // 로그인 로직 실행...
});
```

이 요청 중 Laravel은 현재 CSRF 토큰을 담은 `XSRF-TOKEN` 쿠키를 설정합니다. 이후 요청에서 이 토큰을 URL 디코딩해 `X-XSRF-TOKEN` 헤더로 전송하는데, Axios나 Angular HttpClient 같은 클라이언트는 이를 자동으로 처리합니다. 만약 자동 처리하지 않는 경우, 직접 `X-XSRF-TOKEN` 헤더에 쿠키 값을 넣어야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호 초기화 후에는 Laravel 애플리케이션의 `/login` 경로에 `POST` 요청을 보내 로그인합니다. `/login` 경로는 [수동 구현](/docs/12.x/authentication#authenticating-users)하거나 [Laravel Fortify](/docs/12.x/fortify) 같은 헤드리스 인증 패키지를 이용해 구현할 수 있습니다.

로그인이 성공하면 세션 쿠키를 통해 이후 라우트 요청이 자동 인증되며, `/sanctum/csrf-cookie` 요청으로 CSRF 토큰도 설정되어 있어 JavaScript HTTP 클라이언트가 쿠키값을 헤더에 포함하면 CSRF 보호가 유지됩니다.

만약 사용자 세션이 비활성으로 인해 만료(로그아웃)되면, 이후 요청 시 401 또는 419 HTTP 에러가 발생할 수 있으니 SPA 로그인 페이지로 리다이렉션하세요.

> [!WARNING]
> 직접 `/login` 엔드포인트를 구현해도 되나, 반드시 Laravel에서 기본 제공하는 [세션 기반 인증 서비스](/docs/12.x/authentication#authenticating-users)를 사용해야 하며 보통은 `web` 인증 가드를 사용해야 합니다.

<a name="protecting-spa-routes"></a>
### SPA 라우트 보호 (Protecting Routes)

모든 요청에 인증을 요구하려면 `routes/api.php` 파일에서 API 라우트에 `sanctum` 인증 가드를 적용하세요. 이 가드는 SPA에서 세션 인증을 통한 상태 기반 인증과 외부 요청의 유효한 API 토큰 인증을 모두 처리합니다:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="authorizing-private-broadcast-channels"></a>
### 개인 브로드캐스트 채널 권한 부여 (Authorizing Private Broadcast Channels)

SPA가 [개인 및 프레즌스 방송 채널](/docs/12.x/broadcasting#authorizing-channels)을 인증해야 할 경우, 애플리케이션의 `bootstrap/app.php` 파일에서 `withRouting` 메서드의 `channels` 항목을 제거하고 대신 `withBroadcasting` 메서드를 호출하여 방송 라우트에 적절한 미들웨어를 지정하세요:

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

Pusher의 인증 요청이 성공하려면, [Laravel Echo](/docs/12.x/broadcasting#client-side-installation) 초기화 시에 적절히 설정된 `axios` 인스턴스를 사용하는 커스텀 Pusher `authorizer`를 지정해야 합니다. 이렇게 하면 Pusher가 교차 도메인 요청에 대응할 수 있습니다:

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

모바일 애플리케이션의 API 요청 인증에도 Sanctum 토큰을 사용할 수 있습니다. 모바일 앱 인증 과정은 3자 API 인증과 유사하지만, API 토큰 발급 방식에 약간의 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

먼저 사용자 이메일/아이디, 비밀번호, 그리고 기기 이름을 받아 새 Sanctum 토큰을 발급하는 라우트를 만듭니다. 기기 이름은 정보 제공 용도로 임의의 값을 받을 수 있으며, 보통 사용자가 인지하기 쉬운 이름(e.g. "Nuno's iPhone 12")을 씁니다.

대개 모바일 앱 내 "로그인" 화면에서 이 토큰 엔드포인트로 요청하며, 반환된 평문 API 토큰을 앱 내 저장 후 API 요청에 사용합니다:

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

요청 시 모바일 애플리케이션은 `Authorization` 헤더에 `Bearer` 토큰 형식으로 토큰을 전달해야 합니다.

> [!NOTE]
> 모바일 앱용 토큰 발급 시에도 [토큰 권한](#token-abilities)을 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호 (Protecting Routes)

앞서 설명한 것처럼, 모든 요청을 인증하도록 하려면 라우트에 `sanctum` 인증 가드를 붙이세요:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-mobile-api-tokens"></a>
### 토큰 폐기 (Revoking Tokens)

모바일 기기에 발급한 API 토큰을 사용자가 폐기할 수 있게 하려면, 웹 UI 내 "계정 설정" 화면 등에 토큰 목록과 "폐기" 버튼을 표시하세요. 사용자가 버튼을 클릭하면 관련 토큰을 데이터베이스에서 삭제하면 됩니다. 앞서 언급했듯이 `Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 관계를 통해 토큰에 접근할 수 있습니다:

```php
// 모든 토큰 폐기...
$user->tokens()->delete();

// 특정 토큰 폐기...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 중에는 `Sanctum::actingAs` 메서드를 사용하여 사용자 인증을 시뮬레이트하고 토큰에 부여할 권한을 지정할 수 있습니다:

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

모든 권한을 부여하고 싶으면 `actingAs` 인자의 권한 배열에 `'*'`를 포함하세요:

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```