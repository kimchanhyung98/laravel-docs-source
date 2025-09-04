# Laravel Sanctum (Laravel Sanctum)

- [소개](#introduction)
    - [동작 방식](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 오버라이드](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 능력](#token-abilities)
    - [라우트 보호](#protecting-routes)
    - [토큰 철회](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증 처리](#spa-authenticating)
    - [라우트 보호](#protecting-spa-routes)
    - [프라이빗 브로드캐스트 채널 인가](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호](#protecting-mobile-api-routes)
    - [토큰 철회](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션, 그리고 단순한 토큰 기반 API를 위한 매우 가벼운 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 계정당 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰들은 각각 특정 동작만 수행할 수 있도록 권한(abilities / scopes)을 지정할 수 있습니다.

<a name="how-it-works"></a>
### 동작 방식 (How it Works)

Laravel Sanctum은 두 가지 별도의 문제를 해결하기 위해 존재합니다. 본격적으로 라이브러리를 살펴보기 전에 각각에 대해 설명합니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰

첫째, Sanctum은 OAuth와 같은 복잡한 설정 없이도 사용자에게 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 GitHub 등의 서비스에서 제공하는 "퍼스널 액세스 토큰"에서 영감을 받았습니다. 예를 들어, 애플리케이션의 "계정 설정" 화면에서 사용자가 자신의 계정에 대한 API 토큰을 생성할 수 있는 화면을 생각해보세요. Sanctum을 사용하여 이러한 토큰을 손쉽게 생성하고 관리할 수 있습니다. 이 토큰들은 보통 유효기간이 몇 년에 이르며, 사용자가 원하면 언제든지 직접 철회할 수 있습니다.

Laravel Sanctum은 사용자 API 토큰을 단일 데이터베이스 테이블에 저장하고, 들어오는 HTTP 요청의 `Authorization` 헤더에 포함된 유효한 API 토큰을 통해 인증을 수행합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증

둘째, Sanctum은 Laravel 기반 API와 통신해야 하는 SPA(싱글 페이지 애플리케이션)를 간단하게 인증하는 방법을 제공합니다. 이러한 SPA는 Laravel 애플리케이션과 동일한 저장소(repository)에 존재할 수도 있고, Next.js나 Nuxt로 제작된 완전히 별도의 저장소일 수도 있습니다.

이 기능에서는 어떠한 토큰도 사용하지 않습니다. 대신 Sanctum은 Laravel에 내장된 쿠키 기반 세션 인증 서비스를 사용합니다. 보통 Sanctum은 `web` 인증 가드를 활용하여 쿠키 기반 인증을 처리합니다. 덕분에 CSRF 방어, 세션 인증 및 XSS로 인한 인증 정보 유출 방지가 이루어집니다.

Sanctum은 들어오는 요청의 출처가 직접 개발한 SPA 프론트엔드일 때만 쿠키 기반 인증을 시도합니다. HTTP 요청을 검사할 때 우선 인증 쿠키가 있는지를 확인하고, 없으면 `Authorization` 헤더에서 유효한 API 토큰을 찾습니다.

> [!NOTE]
> Sanctum의 API 토큰 인증 또는 SPA 인증 중 하나만 선택적으로 사용해도 무방합니다. Sanctum을 도입한다고 해서 두 기능을 모두 사용할 필요는 없습니다.

<a name="installation"></a>
## 설치 (Installation)

`install:api` Artisan 명령어를 통해 Laravel Sanctum을 설치할 수 있습니다.

```shell
php artisan install:api
```

이후, SPA 인증을 활용하려는 경우 이 문서의 [SPA 인증](#spa-authentication) 섹션을 참고하시기 바랍니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

보통 필요하지 않지만, Sanctum 내부에서 사용하는 `PersonalAccessToken` 모델을 자유롭게 확장할 수 있습니다.

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

그 다음, Sanctum에서 여러분이 만든 커스텀 모델을 사용하도록 `usePersonalAccessTokenModel` 메서드를 호출할 수 있습니다. 보통 이 코드는 애플리케이션의 `AppServiceProvider` 파일의 `boot` 메서드에서 호출합니다.

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
## API 토큰 인증 (API Token Authentication)

> [!NOTE]
> 자체 개발한 1st 파티 SPA에서는 API 토큰 인증을 사용하지 않아야 합니다. 대신, Sanctum의 내장된 [SPA 인증 기능](#spa-authentication)을 활용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

Sanctum은 API 요청에 사용할 수 있는 API 토큰/퍼스널 엑세스 토큰을 발급할 수 있습니다. API 토큰을 사용하여 요청을 보낼 경우, 토큰을 반드시 `Authorization` 헤더에 `Bearer` 타입으로 포함해야 합니다.

토큰 발급을 시작하려면, 사용자 모델에 `Laravel\Sanctum\HasApiTokens` 트레잇을 추가해야 합니다.

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

토큰을 발급하려면 `createToken` 메서드를 사용하면 됩니다. 이 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전에 SHA-256 해시로 암호화되어 저장되지만, `NewAccessToken` 인스턴스의 `plainTextToken` 속성을 사용해 평문 토큰 값을 받을 수 있습니다. 생성 후, 이 값을 사용자에게 즉시 보여주어야 합니다.

```php
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

사용자의 모든 토큰은 `HasApiTokens` 트레잇에서 제공하는 `tokens` Eloquent 연관관계를 통해 접근할 수 있습니다.

```php
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
### 토큰 능력 (Token Abilities)

Sanctum은 토큰에 "능력(abilities)"을 할당할 수 있습니다. 능력은 OAuth의 "스코프(scopes)"와 비슷한 역할을 합니다. `createToken` 메서드의 두 번째 인수로 문자열 배열 형태의 능력 목록을 전달할 수 있습니다.

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Sanctum으로 인증된 요청을 처리할 때, 해당 토큰이 특정 능력을 보유했는지 `tokenCan` 또는 `tokenCant` 메서드로 확인할 수 있습니다.

```php
if ($user->tokenCan('server:update')) {
    // ...
}

if ($user->tokenCant('server:update')) {
    // ...
}
```

<a name="token-ability-middleware"></a>
#### 토큰 능력 미들웨어

Sanctum은 요청에 사용된 토큰이 특정 능력을 보유하고 있는지 검증하는 두 가지 미들웨어도 제공합니다. 먼저, `bootstrap/app.php` 파일에 아래와 같은 미들웨어 별칭을 등록하세요.

```php
use Laravel\Sanctum\Http\Middleware\CheckAbilities;
use Laravel\Sanctum\Http\Middleware\CheckForAnyAbility;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'abilities' => CheckAbilities::class,
        'ability' => CheckForAnyAbility::class,
    ]);
})
```

`abilities` 미들웨어는 지정한 모든 능력을 토큰이 가지고 있는지 검증합니다.

```php
Route::get('/orders', function () {
    // 토큰이 "check-status", "place-orders" 능력을 모두 가지고 있어야 접근 허용...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` 미들웨어는 지정한 능력 중 하나라도 보유하고 있으면 요청을 허용합니다.

```php
Route::get('/orders', function () {
    // 토큰이 "check-status" 또는 "place-orders" 능력 중 하나라도 소유하면 접근 허용...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### 1st 파티 UI에서의 요청

편의를 위해, 요청이 여러분의 1st 파티 SPA에서 오고, Sanctum의 [SPA 인증](#spa-authentication)을 사용하는 경우에는 `tokenCan` 메서드가 항상 `true`를 반환합니다.

하지만, 그렇다고 해서 무조건 기능 사용을 허용해야 한다는 의미는 아닙니다. 일반적으로 애플리케이션의 [인가 정책](/docs/12.x/authorization#creating-policies)을 통해 토큰이 해당 능력을 허용받았는지, 그리고 사용자 인스턴스 자체가 해당 작업을 수행할 자격이 있는지 재확인해야 합니다.

예를 들어, 서버를 관리하는 애플리케이션이라면 토큰이 서버 업데이트 권한을 보유하고 있을 뿐만 아니라 해당 서버가 사용자의 소유인지도 검사할 수 있습니다.

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

처음에는 1st 파티 UI에서의 요청에 대해 `tokenCan`이 항상 `true`를 반환하도록 한 점이 다소 이상하게 느껴질 수 있습니다. 그러나 항상 API 토큰이 있다고 가정하고 `tokenCan`을 호출할 수 있다는 점에서 매우 편리합니다. 이 접근 방식 덕분에 요청이 SPA UI에서 발생했든, 외부에서 API를 사용하든 신경쓰지 않고 인가 정책 내부에서 항상 `tokenCan`을 활용할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

들어오는 모든 요청이 인증되어야 하는 라우트의 경우, `routes/web.php` 또는 `routes/api.php` 파일 내 라우트에 `sanctum` 인증 가드를 적용하세요. 이 가드는 상태 저장 쿠키 인증 요청(보통 내 애플리케이션 SPA에서 옴)이든, 3rd 파티의 API 토큰이 헤더로 제공된 경우이든 대응할 수 있습니다.

`routes/web.php` 파일의 라우트에 `sanctum` 가드를 사용하도록 권장하는 이유가 궁금할 수 있습니다. Sanctum은 우선 일반적인 쿠키 기반 세션 인증을 시도하고, 쿠키가 없으면 요청의 `Authorization` 헤더에 토큰이 있는지 확인하기 때문입니다. 이렇게 하면 항상 인증된 사용자 인스턴스에서 `tokenCan` 메서드를 호출할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-tokens"></a>
### 토큰 철회 (Revoking Tokens)

`Laravel\Sanctum\HasApiTokens` 트레잇에서 제공하는 `tokens` 관계를 통해 데이터베이스에서 토큰을 삭제함으로써 "토큰 철회"가 가능합니다.

```php
// 모든 토큰 철회...
$user->tokens()->delete();

// 현재 요청에 사용된 토큰 철회...
$request->user()->currentAccessToken()->delete();

// 특정 토큰 철회...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### 토큰 만료 (Token Expiration)

기본적으로 Sanctum 토큰은 만료되지 않으며, [토큰을 철회](#revoking-tokens)해서만 무효화할 수 있습니다. 만약 API 토큰에 만료 기간을 설정하고 싶다면, 애플리케이션의 `sanctum` 설정 파일에 있는 `expiration` 옵션을 사용하세요. 이 설정은 토큰이 만료되기까지의 분(minutes) 단위 기간을 결정합니다.

```php
'expiration' => 525600,
```

각 토큰마다 만료 기간을 개별적으로 지정하고 싶다면, `createToken` 메서드의 세 번째 인수로 만료 시간을 넘겨주면 됩니다.

```php
return $user->createToken(
    'token-name', ['*'], now()->addWeek()
)->plainTextToken;
```

애플리케이션에 토큰 만료 시간이 설정된 경우, [스케줄러를 이용해](/docs/12.x/scheduling) 만료된 토큰을 주기적으로 정리하는 작업도 권장합니다. Sanctum은 이를 위한 `sanctum:prune-expired` Artisan 명령어를 제공합니다. 예를 들어, 24시간 이상 지난 만료 토큰 레코드를 일괄 삭제하는 스케줄을 구성할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

Sanctum은 또한 Laravel 기반 API와 통신이 필요한 SPA를 손쉽게 인증하는 방법도 제공합니다. 이 SPA는 Laravel 애플리케이션과 동일 저장소에 있거나, 완전히 별도의 저장소에 있을 수 있습니다.

이 기능에서는 어떠한 토큰도 사용하지 않으며, Laravel의 내장 쿠키 기반 세션 인증만 활용합니다. 이 접근법은 CSRF 방어, 세션 인증, XSS로 인한 인증 정보 유출 방지까지 포괄적으로 지원합니다.

> [!WARNING]
> 인증을 위해서는 SPA와 API가 동일한 최상위 도메인(Top-level domain)을 공유해야 합니다. 단, 서브도메인은 달라도 무방합니다. 또한 반드시 요청 시 `Accept: application/json` 헤더와 `Referer` 또는 `Origin` 헤더를 함께 보내야 합니다.

<a name="spa-configuration"></a>
### 설정 (Configuration)

<a name="configuring-your-first-party-domains"></a>
#### 1st 파티 도메인 설정

우선, SPA가 요청을 보내는 도메인을 지정해야 합니다. 이 도메인은 `sanctum` 설정 파일의 `stateful` 옵션에 지정할 수 있습니다. 이 설정은 어떤 도메인이 API 요청 시 Laravel 세션 쿠키를 이용해 "상태를 유지하는" 인증을 사용할지를 결정합니다.

1st 파티 상태 저장 도메인 설정을 돕는 헬퍼 함수가 두 가지 제공됩니다. `Sanctum::currentApplicationUrlWithPort()`는 환경 변수 `APP_URL`의 현재 애플리케이션 URL을 반환하고, `Sanctum::currentRequestHost()`는 상태 저장 도메인 리스트에 플레이스홀더를 삽입하여 런타임 시 현재 요청의 호스트로 대체합니다. 덕분에 동일 도메인에서 오는 모든 요청이 상태 저장 요청으로 처리됩니다.

> [!WARNING]
> URL에 포트(`127.0.0.1:8000`)가 포함될 경우, 반드시 해당 포트까지 포함해서 도메인을 지정해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

다음으로, SPA에서 오는 요청은 Laravel 세션 쿠키로 인증을 처리하고, 외부 3rd 파티나 모바일 앱의 요청은 API 토큰 인증을 허용하도록 설정해야 합니다. 이를 위해 `bootstrap/app.php` 파일에서 `statefulApi` 미들웨어 메서드를 호출하면 됩니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->statefulApi();
})
```

<a name="cors-and-cookies"></a>
#### CORS와 쿠키

별도의 서브도메인에서 실행되는 SPA에서 인증이 제대로 동작하지 않는다면, CORS(크로스 오리진 리소스 공유)나 세션 쿠키 설정이 올바르지 않았을 확률이 높습니다.

`config/cors.php` 설정 파일은 기본적으로 공개되지 않습니다. Laravel의 CORS 옵션을 직접 수정하려면, `config:publish` Artisan 명령어로 전체 `cors` 설정 파일을 퍼블리시하세요.

```shell
php artisan config:publish cors
```

그리고 CORS 응답에 반드시 `Access-Control-Allow-Credentials` 헤더값이 `True`로 반환되도록 해야 합니다. 이는 `config/cors.php`의 `supports_credentials` 옵션을 `true`로 설정하면 됩니다.

또한, 전역 `axios` 인스턴스에서는 `withCredentials`와 `withXSRFToken` 옵션을 활성화해야 합니다. 보통 `resources/js/bootstrap.js` 파일에서 설정합니다. 만약 Axios를 사용하지 않는다면, 사용하는 HTTP 클라이언트에서 이와 동등한 설정을 적용하십시오.

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

마지막으로, 세션 쿠키 도메인 설정에서 루트 도메인의 모든 서브도메인을 지원하도록 설정해야 합니다. 이를 위해 `config/session.php`에서 도메인명 앞에 `.`을 붙이세요.

```php
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 인증 처리 (Authenticating)

<a name="csrf-protection"></a>
#### CSRF 보호

SPA 인증을 위해, SPA의 "로그인" 페이지에서 먼저 `/sanctum/csrf-cookie` 엔드포인트에 요청을 보내어 CSRF 보호를 초기화해야 합니다.

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // 로그인 진행...
});
```

이 요청 중에 Laravel은 현재 CSRF 토큰 값을 가진 `XSRF-TOKEN` 쿠키를 설정합니다. 이 토큰은 URL 디코드 후 이후 요청의 `X-XSRF-TOKEN` 헤더로 전달되어야 합니다. Axios나 Angular HttpClient 같은 HTTP 클라이언트 라이브러리는 이 설정을 자동으로 처리해줍니다. 만약 사용 중인 라이브러리가 자동 처리하지 않는다면, 여러분이 직접 `XSRF-TOKEN` 쿠키의 URL 디코드 값을 `X-XSRF-TOKEN` 헤더로 보내야 합니다.

<a name="logging-in"></a>
#### 로그인 처리

CSRF 보호가 초기화되면, SPA에서 애플리케이션의 `/login` 경로에 `POST` 요청을 보내 로그인 처리를 진행해야 합니다. 이 `/login` 경로는 [직접 구현할 수도](/docs/12.x/authentication#authenticating-users), [Laravel Fortify](/docs/12.x/fortify)와 같은 헤드리스 인증 패키지를 사용할 수도 있습니다.

로그인 요청이 성공하면 이후 모든 API 요청에서 세션 쿠키를 통해 자동 인증이 이루어집니다. 이미 `/sanctum/csrf-cookie` 요청을 거쳤으므로, JavaScript HTTP 클라이언트가 `XSRF-TOKEN` 쿠키의 값을 `X-XSRF-TOKEN` 헤더로 전송하기만 하면 이후 모든 요청이 CSRF 보호를 받습니다.

물론 사용자의 세션이 비활동 등으로 만료될 경우, 이후 요청에서 401 또는 419 HTTP 오류가 반환될 수 있습니다. 이 경우 사용자를 SPA의 로그인 화면으로 리다이렉트 해야 합니다.

> [!WARNING]
> 원하는 대로 `/login` 엔드포인트를 직접 작성해도 무방하지만, 표준 [세션 기반 인증 서비스](/docs/12.x/authentication#authenticating-users)를 반드시 사용해야 합니다. 일반적으로는 `web` 인증 가드를 활용하여야 합니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호 (Protecting Routes)

모든 요청이 인증된 사용자만 접근 가능하도록 하고 싶다면, `routes/api.php` 라우트에 `sanctum` 인증 가드를 적용하세요. 이 가드는 SPA의 상태 저장 인증 쿠키 요청과 외부 3rd 파티의 API 토큰 요청 양쪽 모두를 처리합니다.

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="authorizing-private-broadcast-channels"></a>
### 프라이빗 브로드캐스트 채널 인가

SPA에서 [프라이빗/프레즌스 브로드캐스트 채널](/docs/12.x/broadcasting#authorizing-channels) 인증이 필요하다면, `bootstrap/app.php`의 `withRouting` 메서드에서 `channels` 엔트리를 제거하고, `withBroadcasting`를 호출해 브로드캐스팅 라우트를 위한 적절한 미들웨어를 직접 지정하세요.

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

그리고 푸셔(Pusher)의 인증 요청이 정상 동작하려면, [Laravel Echo](/docs/12.x/broadcasting#client-side-installation) 초기화 시 커스텀 Pusher `authorizer`를 지정해야 합니다. 이렇게 하면 [CORS 및 쿠키 설정이 올바르게 구성된 axios 인스턴스](#cors-and-cookies)를 사용할 수 있습니다.

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

모바일 애플리케이션의 요청도 Sanctum 토큰을 사용하여 인증할 수 있습니다. 전체적인 인증 방식은 3rd 파티 API 요청과 유사하지만, API 토큰 발급 방식에 다소 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

먼저, 사용자의 이메일/아이디, 비밀번호, 기기명(device name)을 입력 받아 새로운 Sanctum 토큰을 생성해주는 엔드포인트를 만듭니다. 여기서 "기기명"은 정보 제공용이며, 사용자가 쉽게 알아볼 수 있는 이름(예: "Nuno의 iPhone 12")이면 됩니다.

보통 모바일 앱의 "로그인" 화면에서 이 엔드포인트에 요청하여 토큰을 받고, 받은 평문 API 토큰을 모바일 기기에 저장해 이후 요청에 사용합니다.

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

모바일 애플리케이션은 이후 API 요청 시, 반드시 `Authorization` 헤더에 `Bearer` 토큰으로 해당 토큰 값을 전달해야 합니다.

> [!NOTE]
> 모바일 애플리케이션용 토큰 발급 시에도 [토큰 능력](#token-abilities)을 추가 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호 (Protecting Routes)

앞서 설명한 것과 같이, 라우트에서 `sanctum` 인증 가드를 적용해 모든 요청이 인증을 거치도록 할 수 있습니다.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-mobile-api-tokens"></a>
### 토큰 철회 (Revoking Tokens)

모바일 기기용으로 발급한 API 토큰을 사용자에게 직접 철회(삭제)할 수 있는 기능을 제공하려면 "계정 설정" 페이지 등에서 토큰 목록과 "철회" 버튼을 함께 제공합니다. 사용자가 "철회" 버튼을 클릭하면 해당 토큰을 데이터베이스에서 삭제하면 됩니다. 사용자의 API 토큰은 `Laravel\Sanctum\HasApiTokens` 트레잇의 `tokens` 관계로 접근 가능합니다.

```php
// 모든 토큰 철회...
$user->tokens()->delete();

// 특정 토큰 철회...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 시에는 `Sanctum::actingAs` 메서드를 활용해 테스트용 사용자에 인증 및 토큰 능력 부여를 쉽게 할 수 있습니다.

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

토큰에 모든 권한을 주고 싶을 때는 `actingAs` 메서드에 능력 리스트로 `*`을 포함시키면 됩니다.

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```