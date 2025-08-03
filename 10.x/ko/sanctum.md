# Laravel Sanctum

- [소개](#introduction)
    - [작동 방식](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 덮어쓰기](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 권한](#token-abilities)
    - [라우트 보호](#protecting-routes)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증 과정](#spa-authenticating)
    - [라우트 보호](#protecting-spa-routes)
    - [비공개 방송 채널 권한 부여](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호](#protecting-mobile-api-routes)
    - [토큰 폐기](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션, 그리고 간단한 토큰 기반 API를 위한 가벼운 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 자신의 계정에 대해 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰에는 토큰이 수행할 수 있는 작업을 지정하는 권한/스코프(abilities/scopes)를 부여할 수 있습니다.

<a name="how-it-works"></a>
### 작동 방식 (How it Works)

Laravel Sanctum은 두 가지 문제를 해결하기 위해 존재합니다. 각각을 설명한 후 라이브러리의 세부 내용을 살펴보겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰 (API Tokens)

우선, Sanctum은 OAuth의 복잡함 없이 사용자에게 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 GitHub 등의 "개인 액세스 토큰(personal access tokens)"에서 영감을 받았습니다. 예를 들어, 애플리케이션의 "계정 설정" 페이지에서 사용자가 자신의 계정을 위한 API 토큰을 생성할 수 있다고 가정해보세요. Sanctum을 사용하면 이러한 토큰을 생성하고 관리할 수 있습니다. 이 토큰들은 보통 매우 긴 만료 기간(수년)을 가지지만, 사용자가 언제든지 수동으로 폐기할 수 있습니다.

Laravel Sanctum은 사용자 API 토큰을 단일 데이터베이스 테이블에 저장하고, 유효한 API 토큰을 포함한 `Authorization` 헤더를 통해 들어오는 HTTP 요청을 인증하는 방식으로 이 기능을 제공합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증 (SPA Authentication)

둘째로, Sanctum은 Laravel 기반 API와 통신해야 하는 SPA(싱글 페이지 애플리케이션)를 간단히 인증하는 방법을 제공합니다. SPA는 Laravel 애플리케이션과 같은 저장소에 존재할 수도 있고 Vue CLI, Next.js 등으로 만든 완전 별도의 저장소일 수도 있습니다.

이 기능을 위해 Sanctum은 어떤 종류의 토큰도 사용하지 않습니다. 대신, Laravel에 내장된 쿠키 기반 세션 인증 서비스를 사용합니다. 보통 Sanctum은 이 기능을 구현하기 위해 Laravel의 `web` 인증 가드를 사용합니다. 이는 CSRF 보호, 세션 인증의 장점과 XSS 공격으로 인한 인증 정보 노출 방지 효과를 제공합니다.

Sanctum은 들어오는 요청이 자신의 SPA 프런트엔드에서 온 경우에만 쿠키 기반 인증을 시도합니다. 요청을 받으면 먼저 인증 쿠키가 있는지 확인하고, 없으면 `Authorization` 헤더에 유효한 API 토큰이 있는지 검사합니다.

> [!NOTE]  
> Sanctum을 API 토큰 인증에만 사용하거나 SPA 인증에만 사용할 수 있습니다. Sanctum을 쓴다고 해서 두 기능을 모두 반드시 써야 하는 것은 아닙니다.

<a name="installation"></a>
## 설치 (Installation)

> [!NOTE]  
> 최신 버전의 Laravel에는 이미 Laravel Sanctum이 포함되어 있습니다. 하지만 애플리케이션의 `composer.json` 파일에 `laravel/sanctum`이 없다면, 아래 설치 지침을 따라 주세요.

Composer 패키지 관리자로 Laravel Sanctum을 설치할 수 있습니다:

```shell
composer require laravel/sanctum
```

그다음 `vendor:publish` Artisan 명령어를 사용해 Sanctum 설정 파일과 마이그레이션 파일을 공개해야 합니다. `sanctum` 설정 파일이 애플리케이션의 `config` 디렉터리에 위치하게 됩니다:

```shell
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
```

마지막으로 데이터베이스 마이그레이션을 실행하세요. Sanctum은 API 토큰 저장을 위해 하나의 데이터베이스 테이블을 생성합니다:

```shell
php artisan migrate
```

다음으로, SPA 인증을 사용할 계획이라면 Sanctum 미들웨어를 애플리케이션의 `app/Http/Kernel.php` 파일 내 `api` 미들웨어 그룹에 추가해야 합니다:

```
'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    \Illuminate\Routing\Middleware\ThrottleRequests::class.':api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

<a name="migration-customization"></a>
#### 마이그레이션 커스터마이징 (Migration Customization)

Sanctum의 기본 마이그레이션을 사용하지 않으려면, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에서 `Sanctum::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션 파일을 내보내려면 다음 명령을 실행하세요: `php artisan vendor:publish --tag=sanctum-migrations`

<a name="configuration"></a>
## 설정 (Configuration)

<a name="overriding-default-models"></a>
### 기본 모델 덮어쓰기 (Overriding Default Models)

일반적으로 필요하지는 않지만, Sanctum에서 내부적으로 사용하는 `PersonalAccessToken` 모델을 확장할 수 있습니다:

```
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

그 후, Sanctum에서 사용자 정의 모델을 사용하도록 `usePersonalAccessTokenModel` 메서드를 호출해 지정할 수 있습니다. 일반적으로 애플리케이션 서비스 프로바이더 중 하나의 `boot` 메서드 내에서 호출합니다:

```
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
> 자체 SPA 인증에 API 토큰을 사용하지 마세요. 대신 Sanctum의 내장된 [SPA 인증 기능](#spa-authentication)을 사용해야 합니다.

<a name="issuing-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

Sanctum을 사용하면 API 요청 인증에 사용할 수 있는 API 토큰 또는 개인 액세스 토큰을 발급할 수 있습니다. API 토큰으로 요청할 때는 `Authorization` 헤더에 `Bearer` 토큰으로 포함해야 합니다.

사용자에게 토큰 발급을 시작하려면, User 모델에 `Laravel\Sanctum\HasApiTokens` 트레잇을 사용해야 합니다:

```
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

토큰을 발급할 때는 `createToken` 메서드를 사용할 수 있습니다. `createToken`은 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장하기 전에 SHA-256으로 해시하지만, 생성 직후 토큰의 평문 값을 `NewAccessToken` 인스턴스의 `plainTextToken` 속성으로 얻을 수 있습니다. 이 값을 사용자에게 바로 보여줘야 합니다:

```
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

`HasApiTokens` 트레잇이 제공하는 `tokens` Eloquent 연관관계로 사용자의 모든 토큰에 접근할 수도 있습니다:

```
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
### 토큰 권한 (Token Abilities)

Sanctum은 토큰에 "abilities"(권한)를 할당할 수 있습니다. 이 능력은 OAuth의 "scopes"와 유사한 역할을 합니다. `createToken` 메서드의 두 번째 인수로 문자열 배열 형태의 권한을 전달할 수 있습니다:

```
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Sanctum으로 인증된 들어오는 요청을 처리할 때, 토큰이 특정 권한을 가지고 있는지 `tokenCan` 메서드로 확인할 수 있습니다:

```
if ($user->tokenCan('server:update')) {
    // ...
}
```

<a name="token-ability-middleware"></a>
#### 토큰 권한 미들웨어

Sanctum은 특정 권한이 할당된 토큰으로 인증된 요청인지 확인할 수 있도록 두 가지 미들웨어를 포함합니다. 시작하려면 애플리케이션 `app/Http/Kernel.php` 파일의 `$middlewareAliases` 속성에 아래 미들웨어를 추가하세요:

```
'abilities' => \Laravel\Sanctum\Http\Middleware\CheckAbilities::class,
'ability' => \Laravel\Sanctum\Http\Middleware\CheckForAnyAbility::class,
```

`abilities` 미들웨어는 요청의 토큰이 나열된 모든 권한을 가지고 있는지 확인합니다:

```
Route::get('/orders', function () {
    // 토큰이 "check-status" 및 "place-orders" 권한 모두를 가짐...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` 미들웨어는 요청의 토큰이 나열된 권한 중 *최소 하나*를 가지고 있는지 확인합니다:

```
Route::get('/orders', function () {
    // 토큰이 "check-status" 또는 "place-orders" 권한 중 하나를 가짐...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### 1차 UI에서 시작된 요청 (First-Party UI Initiated Requests)

편의상, `tokenCan` 메서드는 들어오는 인증 요청이 1차 SPA에서 온 경우 항상 `true`를 반환합니다. 이때 Sanctum의 내장된 [SPA 인증](#spa-authentication)을 사용 중임을 전제로 합니다.

하지만 이 뜻이 사용자가 반드시 행동을 수행할 수 있다는 의미는 아닙니다. 보통은 애플리케이션의 [인가 정책](/docs/10.x/authorization#creating-policies)이 토큰 권한 허용 여부와 해당 사용자가 실제 작업을 수행할 권한이 있는지를 판단합니다.

예를 들어, 서버를 관리하는 애플리케이션이라면 다음과 같은 조건을 확인할 수 있습니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

첫째, 1차 UI 요청에 대해 `tokenCan` 메서드가 항상 `true`를 반환하는 것은 처음에는 이상하게 느껴질 수 있지만, API 토큰이 항상 있고 `tokenCan` 메서드로 검사할 수 있다는 점이 편리합니다. 이렇게 하면 요청이 UI에서 왔는지 제3자 API 소비자에서 왔는지 상관 없이 인가 정책 내에서 항상 `tokenCan` 메서드를 호출할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

모든 들어오는 요청을 인증해야만 접근할 수 있도록 라우트를 보호하려면, `routes/web.php`와 `routes/api.php` 파일에서 보호할 라우트에 `sanctum` 인증 가드를 연결해야 합니다. 이 가드는 요청이 1차 쿠키 인증된 상태이거나, 제3자 요청일 경우 올바른 API 토큰이 들어있는지 확인합니다.

왜 `routes/web.php` 파일 내에서도 `sanctum` 가드를 쓰라고 권장하는지 궁금할 수 있습니다. Sanctum은 먼저 기본 세션 인증 쿠키로 인증을 시도하고, 쿠키가 없으면 `Authorization` 헤더 토큰으로 시도하기 때문입니다. 게다가 Sanctum으로 모든 요청을 인증하면 현재 인증된 사용자 인스턴스에서 항상 `tokenCan` 메서드를 호출할 수 있습니다:

```
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="revoking-tokens"></a>
### 토큰 폐기 (Revoking Tokens)

`Laravel\Sanctum\HasApiTokens` 트레잇이 제공하는 `tokens` 관계를 사용해 데이터베이스에서 토큰을 삭제하며 "폐기"할 수 있습니다:

```
// 모든 토큰 폐기...
$user->tokens()->delete();

// 현재 요청에 사용된 토큰 폐기...
$request->user()->currentAccessToken()->delete();

// 특정 토큰 폐기...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### 토큰 만료 (Token Expiration)

기본적으로 Sanctum 토큰은 만료하지 않고, [토큰 폐기](#revoking-tokens)로만 무효화할 수 있습니다. 그러나 애플리케이션에 API 토큰 만료 시간을 설정하려면 `sanctum` 설정 파일 내 `expiration` 옵션을 사용하세요. 이 옵션은 토큰 발급 후 만료 처리까지의 분 단위 시간을 정의합니다:

```php
'expiration' => 525600,
```

토큰마다 만료 시간을 개별적으로 지정하고 싶다면, `createToken` 메서드 세 번째 인수로 만료 시간을 제공할 수 있습니다:

```php
return $user->createToken(
    'token-name', ['*'], now()->addWeek()
)->plainTextToken;
```

만약 토큰 만료를 설정했다면, 만료된 토큰을 정리할 [스케줄 작업](/docs/10.x/scheduling)을 추가하는 것이 좋습니다. 다행히 Sanctum은 `sanctum:prune-expired` Artisan 명령어를 제공합니다. 예를 들어, 만료된 지 최소 24시간 지난 모든 토큰 기록을 매일 삭제하도록 스케줄링할 수 있습니다:

```php
$schedule->command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

Sanctum은 Laravel 기반 API와 통신하는 싱글 페이지 애플리케이션(SPA)을 간편하게 인증하는 방법도 제공합니다. SPA는 Laravel 애플리케이션과 같은 저장소에 있거나 완전히 별도의 저장소일 수 있습니다.

이 기능은 토큰을 전혀 사용하지 않고 Laravel의 쿠키 기반 세션 인증을 활용합니다. 이 인증 방법은 CSRF 보호, 세션 인증, 그리고 XSS 공격으로 인한 인증 정보 유출 방지를 제공합니다.

> [!WARNING]  
> SPA와 API는 반드시 같은 최상위 도메인을 공유해야 합니다. 다만 서브도메인은 달라도 무방합니다. 또한 요청에 `Accept: application/json` 헤더와 `Referer` 또는 `Origin` 헤더를 반드시 포함해야 합니다.

<a name="spa-configuration"></a>
### 설정 (Configuration)

<a name="configuring-your-first-party-domains"></a>
#### 1차 도메인 구성 (Configuring Your First-Party Domains)

먼저, SPA가 요청을 보내는 도메인을 설정해야 합니다. `sanctum` 설정 파일 내 `stateful` 옵션에서 해당 도메인을 구성합니다. 이 옵션은 어떤 도메인이 Laravel 세션 쿠키를 사용해 "상태 유지(stateful)" 인증을 할 수 있을지를 결정합니다.

> [!WARNING]  
> 애플리케이션에 포트 번호를 포함한 URL(예: `127.0.0.1:8000`)로 접근하는 경우, 도메인에 포트 번호도 반드시 포함해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어 (Sanctum Middleware)

다음으로 `app/Http/Kernel.php` 파일 내 `api` 미들웨어 그룹에 Sanctum 미들웨어를 추가하세요. 이 미들웨어는 SPA에서 들어오는 요청을 Laravel 세션 쿠키를 통해 인증할 수 있도록 하면서, 제3자나 모바일 앱에서 오는 요청도 API 토큰으로 인증할 수 있도록 합니다:

```
'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    \Illuminate\Routing\Middleware\ThrottleRequests::class.':api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

<a name="cors-and-cookies"></a>
#### CORS 및 쿠키 설정 (CORS and Cookies)

서브도메인에서 SPA를 실행할 때 인증에 실패한다면, CORS(교차 출처 자원 공유)나 세션 쿠키 설정이 잘못되었을 가능성이 큽니다.

애플리케이션의 CORS 설정이 `Access-Control-Allow-Credentials` 헤더를 `true` 값으로 반환하도록 해야 합니다. 이는 `config/cors.php` 파일의 `supports_credentials` 옵션을 `true`로 설정해 달성할 수 있습니다.

또한, Axios 글로벌 인스턴스의 `withCredentials` 및 `withXSRFToken` 옵션을 활성화해야 합니다. 보통 이 작업은 `resources/js/bootstrap.js` 파일에서 수행합니다. 만약 Axios가 아닌 다른 HTTP 클라이언트를 사용한다면 이에 상응하는 설정을 해야 합니다:

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

마지막으로, 세션 쿠키 도메인 설정도 루트 도메인의 모든 서브도메인을 지원하도록 해야 합니다. `config/session.php` 파일에서 도메인 앞에 점(.)을 붙여 설정하면 됩니다:

```
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 인증 과정 (Authenticating)

<a name="csrf-protection"></a>
#### CSRF 보호 (CSRF Protection)

SPA를 인증하려면 먼저 SPA "로그인" 페이지에서 `/sanctum/csrf-cookie` 경로에 요청을 보내 CSRF 보호를 초기화해야 합니다:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // 로그인 처리...
});
```

이때 Laravel은 현재 CSRF 토큰이 담긴 `XSRF-TOKEN` 쿠키를 설정합니다. 이후 요청에는 `X-XSRF-TOKEN` 헤더에 이 값이 포함되어야 하며, Axios, Angular HttpClient 같은 HTTP 클라이언트는 이 과정을 자동으로 처리합니다. 만약 자동 설정을 지원하지 않는다면, 직접 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더에 넣어야 합니다.

<a name="logging-in"></a>
#### 로그인 (Logging In)

CSRF 보호가 초기화되면, Laravel 애플리케이션의 `/login` 경로에 `POST` 요청을 보냅니다. 이 경로는 [직접 구현](/docs/10.x/authentication#authenticating-users)하거나 [Laravel Fortify](/docs/10.x/fortify) 같은 무상태 인증 패키지를 사용할 수 있습니다.

로그인이 성공하면, Laravel 애플리케이션이 클라이언트에게 전달한 세션 쿠키를 통해 인증이 유지됩니다. 그리고 이미 `/sanctum/csrf-cookie`에 요청한 덕분에, 자바스크립트 HTTP 클라이언트가 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더에 자동으로 포함시키므로 CSRF 보호도 함께 유지됩니다.

단, 사용자의 세션이 비활성으로 만료되면 401 또는 419 HTTP 오류가 발생할 수 있으므로 이 경우 SPA 로그인 페이지로 리다이렉트해야 합니다.

> [!WARNING]  
> `/login` 엔드포인트를 직접 구현해도 무방하지만, Laravel이 제공하는 [표준 세션 기반 인증 서비스](/docs/10.x/authentication#authenticating-users)를 반드시 사용해야 합니다. 보통 `web` 인증 가드 사용을 의미합니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호 (Protecting Routes)

모든 들어오는 SPA 요청이 인증된 상태여야만 접근 가능하도록 하려면, API 라우트(`routes/api.php`)에서 라우트에 `sanctum` 인증 가드를 적용하세요. 이 가드는 요청이 SPA에서 온 상태 유지 인증이거나, 제3자 요청일 경우 유효한 API 토큰이 포함되어 있는지 확인합니다:

```
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="authorizing-private-broadcast-channels"></a>
### 비공개 방송 채널 권한 부여 (Authorizing Private Broadcast Channels)

SPA가 [비공개/프레즌스 방송 채널(private/presence broadcast channels)](/docs/10.x/broadcasting#authorizing-channels)을 인증해야 한다면, `Broadcast::routes` 메서드를 `routes/api.php`에 배치합니다:

```
Broadcast::routes(['middleware' => ['auth:sanctum']]);
```

그 다음, Pusher의 권한 부여 요청이 성공하도록 [Laravel Echo](/docs/10.x/broadcasting#client-side-installation)를 초기화할 때 커스텀 Pusher `authorizer`를 설정해야 합니다. 이를 통해 크로스 도메인 요청에 적절히 설정된 `axios` 인스턴스를 사용하도록 할 수 있습니다:

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

Sanctum 토큰으로 모바일 애플리케이션의 API 요청도 인증할 수 있습니다. 모바일 앱 인증 과정은 제3자 API 요청 인증과 유사하지만, API 토큰 발급 과정에 약간 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

시작하려면, 이메일/사용자명, 비밀번호, 그리고 디바이스 이름을 받아 새 Sanctum 토큰과 교환하는 엔드포인트를 만드세요. 디바이스 이름은 사용자가 알아볼 수 있는 임의의 값이면 됩니다. 보통 "Nuno's iPhone 12" 같은 이름이 적절합니다.

이 토큰 엔드포인트는 모바일 앱의 로그인 화면에서 호출됩니다. 평문 API 토큰이 반환되고, 모바일 장치에 저장해 추가 API 요청 시 사용합니다:

```
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

모바일 앱이 API 요청 시 토큰을 `Authorization` 헤더의 `Bearer` 토큰으로 전달해야 합니다.

> [!NOTE]  
> 모바일용 토큰 발급 시에도 [토큰 권한](#token-abilities)을 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호 (Protecting Routes)

앞서 문서에 나온 것처럼, 요청을 인증해야 하는 라우트에 `sanctum` 인증 가드를 추가해 보호할 수 있습니다:

```
Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="revoking-mobile-api-tokens"></a>
### 토큰 폐기 (Revoking Tokens)

모바일 기기에 발급된 API 토큰을 사용자가 폐기할 수 있도록, 웹 애플리케이션의 "계정 설정" UI에 토큰 명과 "폐기" 버튼을 나열할 수 있습니다. 사용자가 버튼을 클릭하면 데이터베이스에서 해당 토큰을 삭제하면 됩니다. `Laravel\Sanctum\HasApiTokens` 트레잇이 제공하는 `tokens` 관계로 접근할 수 있습니다:

```
// 모든 토큰 폐기...
$user->tokens()->delete();

// 특정 토큰 폐기...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 중에는 `Sanctum::actingAs` 메서드를 사용해 사용자를 인증하고 토큰에 부여할 권한을 지정할 수 있습니다:

```
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

모든 권한을 부여하고 싶다면, `actingAs` 메서드에 `'*'`을 권한 배열에 포함시키면 됩니다:

```
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
