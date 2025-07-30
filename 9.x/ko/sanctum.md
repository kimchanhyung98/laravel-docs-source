# Laravel Sanctum

- [소개](#introduction)
    - [작동 방식](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 권한](#token-abilities)
    - [라우트 보호](#protecting-routes)
    - [토큰 취소](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증 처리](#spa-authenticating)
    - [라우트 보호](#protecting-spa-routes)
    - [비공개 방송 채널 권한 부여](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호](#protecting-mobile-api-routes)
    - [토큰 취소](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션, 그리고 간단한 토큰 기반 API를 위한 경량 인증 시스템을 제공합니다. Sanctum을 통해 각 사용자 계정마다 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰들에는 토큰이 수행할 수 있는 작업을 지정하는 권한(abilities) 또는 범위(scopes)를 부여할 수 있습니다.

<a name="how-it-works"></a>
### 작동 방식 (How It Works)

Laravel Sanctum은 두 가지 별개의 문제를 해결하기 위해 존재합니다. 라이브러리의 세부 내용을 살펴보기 전에 각각의 문제를 설명하겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰 (API Tokens)

먼저, Sanctum은 OAuth의 복잡함 없이 사용자에게 API 토큰을 발급하는 간단한 패키지입니다. 이 기능은 GitHub 및 기타 애플리케이션의 "개인 액세스 토큰" 방식에서 영감을 받았습니다. 예를 들어, 애플리케이션의 '계정 설정' 화면에서 사용자가 자신의 계정을 위한 API 토큰을 생성할 수 있다고 상상해보세요. Sanctum은 이러한 토큰들을 생성하고 관리할 수 있는 기능을 제공합니다. 보통 이 토큰들은 매우 긴 만료 시간(수년)을 갖지만 사용자가 언제든지 수동으로 취소할 수 있습니다.

Laravel Sanctum은 사용자 API 토큰을 단일 데이터베이스 테이블에 저장하며, HTTP 요청의 `Authorization` 헤더에 올바른 API 토큰이 포함되어 있는지 확인하여 인증을 수행합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증 (SPA Authentication)

두 번째로, Sanctum은 Laravel 기반 API와 통신이 필요한 싱글 페이지 애플리케이션(SPA)을 간단히 인증할 수 있도록 합니다. 이러한 SPA는 Laravel 애플리케이션과 같은 저장소에 있거나 Vue CLI 또는 Next.js로 만든 완전히 별도의 저장소일 수도 있습니다.

이 기능에서는 토큰을 전혀 사용하지 않고 Laravel의 기본 쿠키 기반 세션 인증 서비스를 이용합니다. 보통 Sanctum은 이를 위해 Laravel의 `web` 인증 guard를 사용합니다. 이 방식은 CSRF 보호, 세션 인증 및 XSS 공격으로부터 인증 자격 증명 노출 방지의 이점을 제공합니다.

Sanctum은 요청이 자체 SPA 프론트엔드에서 오면 쿠키를 사용해 인증을 시도합니다. 요청을 검사할 때 인증 쿠키가 없으면 `Authorization` 헤더에 유효한 API 토큰이 있는지 확인합니다.

> [!NOTE]
> Sanctum을 API 토큰 인증에만, 또는 SPA 인증에만 사용하는 것도 전혀 문제없습니다. Sanctum을 사용한다고 해서 반드시 두 기능을 모두 사용해야 하는 것은 아닙니다.

<a name="installation"></a>
## 설치 (Installation)

> [!NOTE]
> 최신 버전의 Laravel에는 기본적으로 Laravel Sanctum이 포함되어 있습니다. 그러나 애플리케이션의 `composer.json`에 `laravel/sanctum`이 포함되어 있지 않다면 아래 설치 방법을 따라 설치할 수 있습니다.

Composer 패키지 매니저를 통해 Laravel Sanctum을 설치할 수 있습니다:

```shell
composer require laravel/sanctum
```

다음으로 Sanctum 구성 파일과 마이그레이션을 공개하려면 `vendor:publish` Artisan 명령어를 실행하세요. `sanctum` 구성 파일이 애플리케이션의 `config` 디렉터리에 생성됩니다:

```shell
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
```

마지막으로 데이터베이스 마이그레이션을 실행하세요. Sanctum이 API 토큰을 저장할 데이터베이스 테이블을 하나 생성합니다:

```shell
php artisan migrate
```

SPA 인증에 Sanctum을 사용하려면 애플리케이션의 `app/Http/Kernel.php` 파일 안에 있는 `api` 미들웨어 그룹에 Sanctum 미들웨어를 추가해야 합니다:

```
'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    'throttle:api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

<a name="migration-customization"></a>
#### 마이그레이션 커스터마이징 (Migration Customization)

Sanctum의 기본 마이그레이션 파일을 사용하지 않으려면, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Sanctum::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션은 다음 명령어로 내보낼 수 있습니다: `php artisan vendor:publish --tag=sanctum-migrations`

<a name="configuration"></a>
## 설정 (Configuration)

<a name="overriding-default-models"></a>
### 기본 모델 재정의 (Overriding Default Models)

보통은 필요하지 않지만, Sanctum이 내부에서 사용하는 `PersonalAccessToken` 모델을 확장할 수도 있습니다:

```
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

그다음 Sanctum에게 커스텀 모델을 사용하도록 지시하려면, 애플리케이션 서비스 프로바이더의 `boot` 메서드 내에서 `usePersonalAccessTokenModel` 메서드를 호출하세요:

```
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a name="api-token-authentication"></a>
## API 토큰 인증 (API Token Authentication)

> [!NOTE]
> 직접 만든 자체 SPA를 인증할 때 API 토큰을 사용하지 마세요. 대신 Sanctum의 내장 [SPA 인증 기능](#spa-authentication)을 사용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

Sanctum은 API 요청을 인증하는 데 사용할 수 있는 API 토큰과 개인 액세스 토큰을 발급할 수 있도록 합니다. API 토큰으로 요청할 때는 토큰을 `Authorization` 헤더에 `Bearer` 토큰 형태로 포함시켜야 합니다.

사용자에게 토큰 발급을 시작하려면, User 모델에 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용해야 합니다:

```
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

토큰을 발급하려면 `createToken` 메서드를 사용할 수 있습니다. 이 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전에 SHA-256 해시로 암호화되지만, 토큰의 평문 값은 `NewAccessToken` 인스턴스의 `plainTextToken` 속성으로 접근할 수 있습니다. 토큰을 생성한 직후 이 값을 사용자에게 보여줘야 합니다:

```
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

`HasApiTokens` 트레이트가 제공하는 `tokens` Eloquent 연관관계를 통해 사용자의 모든 토큰에 접근할 수 있습니다:

```
foreach ($user->tokens as $token) {
    //
}
```

<a name="token-abilities"></a>
### 토큰 권한 (Token Abilities)

Sanctum은 토큰에 "권한(abilities)"을 부여할 수 있습니다. 이 권한은 OAuth의 "스코프(scopes)"와 유사한 개념입니다. `createToken` 메서드의 두 번째 인수로 문자열 배열 형태의 권한 목록을 전달할 수 있습니다:

```
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Sanctum으로 인증된 요청을 처리할 때, `tokenCan` 메서드를 사용해 토큰이 특정 권한을 갖고 있는지 확인할 수 있습니다:

```
if ($user->tokenCan('server:update')) {
    //
}
```

<a name="token-ability-middleware"></a>
#### 토큰 권한 미들웨어 (Token Ability Middleware)

Sanctum은 특정 권한이 부여된 토큰인지 확인할 수 있는 두 개의 미들웨어를 포함합니다. 사용을 위해 애플리케이션의 `app/Http/Kernel.php` 파일 내 `$routeMiddleware` 속성에 아래 미들웨어를 추가하세요:

```
'abilities' => \Laravel\Sanctum\Http\Middleware\CheckAbilities::class,
'ability' => \Laravel\Sanctum\Http\Middleware\CheckForAnyAbility::class,
```

`abilities` 미들웨어는 요청 토큰이 나열된 **모든** 권한을 갖고 있음을 확인합니다:

```
Route::get('/orders', function () {
    // 토큰이 "check-status"와 "place-orders" 권한을 모두 갖고 있음
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` 미들웨어는 요청 토큰이 나열된 권한 중 **적어도 하나**를 갖고 있는지 확인합니다:

```
Route::get('/orders', function () {
    // 토큰이 "check-status" 또는 "place-orders" 권한을 갖고 있음
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### 자체 UI에서 시작된 요청 (First-Party UI Initiated Requests)

편의를 위해, 요청이 자체 SPA에서 발생하고 Sanctum의 내장 [SPA 인증](#spa-authentication)을 사용하는 경우 `tokenCan` 메서드는 항상 `true`를 반환합니다.

그러나 이것이 반드시 애플리케이션이 해당 동작을 허락해야 한다는 의미는 아닙니다. 보통 애플리케이션의 [인가 정책](/docs/9.x/authorization#creating-policies)이 토큰이 권한을 갖고 있는지, 그리고 사용자 인스턴스가 그 작업을 수행할 자격이 있는지를 함께 판단합니다.

예를 들어 서버를 관리하는 애플리케이션에서는 토큰이 서버 업데이트 권한을 가지고 있는지, 그리고 해당 서버가 현재 사용자에게 속해 있는지 함께 검사할 수 있습니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

처음에는 자체 UI에서 시작된 요청에 대해 항상 `tokenCan`이 `true`를 반환하는 것이 이상해 보일 수 있습니다. 하지만 이렇게 하면 API 토큰의 존재와 권한을 항상 가정할 수 있으므로, API 소비자가 직접 요청을 보냈는지 UI에서 보낸 요청인지 구분하지 않고 항상 `tokenCan`을 사용해 권한 검사를 수행할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

모든 들어오는 요청을 인증해야 하는 라우트를 보호하려면, `routes/web.php`와 `routes/api.php`에 있는 보호할 라우트에 `sanctum` 인증 guard를 붙이세요. 이 guard는 요청이 상태 기반 쿠키 인증이든, 타사 요청 시 유효한 API 토큰이든 인증 여부를 보장합니다.

왜 `routes/web.php`에 `sanctum` 가드를 이용해 라우트 인증을 권장하는지 궁금할 수 있습니다. Sanctum은 요청 쿠키를 우선 검사해서 세션 인증을 시도하며, 쿠키가 없으면 `Authorization` 헤더의 토큰으로 인증합니다. 또한 Sanctum 인증을 사용하면 언제든 현재 인증된 사용자 인스턴스에서 `tokenCan` 메서드를 호출할 수 있습니다:

```
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="revoking-tokens"></a>
### 토큰 취소 (Revoking Tokens)

토큰을 "취소"하려면, `Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 관계를 통해 데이터베이스에서 삭제하면 됩니다:

```
// 모든 토큰 취소...
$user->tokens()->delete();

// 현재 요청을 인증한 토큰 취소...
$request->user()->currentAccessToken()->delete();

// 특정 토큰 취소...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### 토큰 만료 (Token Expiration)

기본적으로 Sanctum 토큰은 만료되지 않으며, [토큰 취소](#revoking-tokens)로만 무효화할 수 있습니다. 그러나 애플리케이션의 API 토큰에 만료 시간을 지정하려면 `sanctum` 설정 파일의 `expiration` 옵션을 수정하면 됩니다. 이 옵션은 토큰 만료까지의 분(minutes) 단위를 의미합니다:

```php
'expiration' => 525600,
```

토큰 만료 시간을 설정했다면, 애플리케이션 토큰의 만료 기록을 정리하는 예약 작업([스케줄링](/docs/9.x/scheduling))을 추가하는 것도 좋습니다. 다행히 Sanctum은 만료된 토큰을 정리하는 `sanctum:prune-expired` Artisan 명령어를 제공합니다. 아래 예시는 만료된지 24시간 이상 지난 토큰을 매일 삭제하는 스케줄입니다:

```php
$schedule->command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

Sanctum은 Laravel API와 통신하는 SPA 인증을 쉽게 제공하기 위해 만들어졌습니다. SPA는 Laravel 애플리케이션과 같은 저장소에 있거나 별도의 저장소에 있을 수도 있습니다.

이 기능에서는 토큰을 사용하지 않고, Laravel의 기본 쿠키 기반 세션 인증 방식을 사용합니다. 이 인증 방식은 CSRF 보호, 세션 인증, 그리고 XSS로 인한 자격 증명 노출 방지의 이점을 제공합니다.

> [!WARNING]
> SPA와 API는 동일한 최상위 도메인을 사용해야 합니다(단, 서브도메인은 달라도 됨). 또한 요청 시 `Accept: application/json` 헤더를 함께 보내는지 확인하세요.

<a name="spa-configuration"></a>
### 설정 (Configuration)

<a name="configuring-your-first-party-domains"></a>
#### 자체 도메인 설정 (Configuring Your First-Party Domains)

먼저, SPA가 요청을 보내는 도메인을 설정해야 합니다. 이는 `sanctum` 구성 파일의 `stateful` 옵션을 통해 할 수 있습니다. 이 설정은 API 요청 시 Laravel 세션 쿠키를 사용한 "상태 기반" 인증을 유지할 도메인 목록을 의미합니다.

> [!WARNING]
> 만약 포트가 포함된 URL(예: `127.0.0.1:8000`)로 접근한다면, 도메인에 포트 번호를 반드시 포함해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어 (Sanctum Middleware)

다음으로, `app/Http/Kernel.php`의 `api` 미들웨어 그룹에 Sanctum 미들웨어를 추가하세요. 이 미들웨어는 SPA에서 보낸 Laravel 세션 쿠키를 통한 인증을 허용하면서도 타사 API 호출이나 모바일 앱 요청에는 토큰 인증을 계속 사용할 수 있도록 합니다:

```
'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    'throttle:api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

<a name="cors-and-cookies"></a>
#### CORS 및 쿠키 설정 (CORS & Cookies)

만약 별도의 서브도메인에서 실행 중인 SPA가 애플리케이션 인증에 실패한다면 CORS 또는 세션 쿠키 설정이 잘못되었을 가능성이 높습니다.

애플리케이션의 CORS 설정에서 `Access-Control-Allow-Credentials` 헤더가 `true`로 반환되는지 반드시 확인하세요. Laravel에서는 `config/cors.php` 내 `supports_credentials` 옵션을 `true`로 지정하면 됩니다.

또한 프론트엔드에서 사용하는 `axios` 글로벌 인스턴스에 `withCredentials` 옵션을 활성화하는 게 필요합니다. 보통 이 설정은 `resources/js/bootstrap.js`에서 수행합니다. Axios 외 다른 HTTP 클라이언트를 사용할 경우, 해당 클라이언트에 맞는 옵션 설정을 해주세요:

```js
axios.defaults.withCredentials = true;
```

마지막으로 애플리케이션 세션 쿠키의 도메인 설정이 루트 도메인 및 모든 서브도메인을 지원하도록 설정해야 합니다. `config/session.php`의 `domain` 옵션에 앞에 점(`.`)을 붙여주세요:

```
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 인증 처리 (Authenticating)

<a name="csrf-protection"></a>
#### CSRF 보호 (CSRF Protection)

SPA 인증을 위해, 로그인 페이지에서 먼저 `/sanctum/csrf-cookie` 엔드포인트에 요청을 보내 CSRF 보호를 초기화해야 합니다:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // 로그인 요청 실행...
});
```

이 요청을 보내면 Laravel이 현재 CSRF 토큰을 담은 `XSRF-TOKEN` 쿠키를 설정합니다. 이후 HTTP 요청에는 이 토큰 값을 담은 `X-XSRF-TOKEN` 헤더가 자동으로 포함되어야 하며, Axios 같은 일부 HTTP 라이브러리는 이를 자동 처리합니다. 만약 사용 중인 라이브러리가 자동 처리하지 않으면 직접 헤더에 쿠키 값을 복사해서 넣어야 합니다.

<a name="logging-in"></a>
#### 로그인 (Logging In)

CSRF 보호가 초기화된 이후, `/login` 경로에 `POST` 요청으로 로그인 정보를 보내세요. 이 `/login` 경로는 직접 구현할 수도 있고, [Laravel Fortify](/docs/9.x/fortify) 같은 헤드리스 인증 패키지를 사용할 수도 있습니다.

로그인이 성공하면 인증되며, Laravel 애플리케이션이 클라이언트에 발급한 세션 쿠키를 통해 이후 요청은 자동으로 인증됩니다. 또한 `/sanctum/csrf-cookie` 요청을 이미 했기 때문에 JavaScript HTTP 클라이언트가 `XSRF-TOKEN`을 자동으로 헤더에 포함시켜 CSRF 보호를 받을 수 있습니다.

하지만 사용자의 세션이 유효 기간 만료로 종료되면 이후 요청에 대해 401 또는 419 HTTP 오류가 발생할 수 있습니다. 이 경우 SPA 로그인 페이지로 리다이렉트해야 합니다.

> [!WARNING]
> 자체 `/login` 엔드포인트를 구현할 수 있으나, 반드시 Laravel이 제공하는 표준 [세션 기반 인증 서비스](/docs/9.x/authentication#authenticating-users)를 사용해야 합니다. 보통 `web` 인증 guard를 사용합니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호 (Protecting Routes)

모든 요청이 인증된 상태여야 하는 SPA 관련 API 라우트에 `sanctum` 인증 가드를 붙이세요. 이를 통해 요청이 SPA에서 보낸 상태 기반 인증이든, 타사 API 토큰이든 인증 여부를 검증합니다:

```
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="authorizing-private-broadcast-channels"></a>
### 비공개 방송 채널 권한 부여 (Authorizing Private Broadcast Channels)

SPA가 [비공개/프레즌스 방송 채널](/docs/9.x/broadcasting#authorizing-channels)을 인증해야 하면, `Broadcast::routes` 호출을 `routes/api.php`에 추가하세요:

```
Broadcast::routes(['middleware' => ['auth:sanctum']]);
```

그다음 Pusher 권한 요청이 성공하려면, [Laravel Echo](#) 초기화 시 Pusher의 `authorizer`를 커스텀으로 제공해야 합니다. 이로써 `axios` 인스턴스를 사용해 [크로스 도메인 요청](#cors-and-cookies)이 제대로 되도록 설정할 수 있습니다:

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

또한 Sanctum 토큰을 사용해 모바일 애플리케이션의 API 요청을 인증할 수도 있습니다. 모바일 인증 과정은 타사 API 요청을 인증하는 과정과 유사하지만 토큰 발급에는 약간의 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

시작하려면, 사용자의 이메일/아이디, 비밀번호, 디바이스 이름을 받아 새로운 Sanctum 토큰으로 교환하는 라우트를 만드세요. 디바이스 이름은 단순히 식별용이며, 예를 들어 "Nuno's iPhone 12"처럼 사용자가 인지할 수 있는 이름이면 됩니다.

보통 모바일 애플리케이션 로그인 화면에서 이 토큰 엔드포인트에 요청을 보내고, 평문 API 토큰을 받아 기기에 저장한 뒤 이후 API 요청 시 사용합니다:

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

모바일 앱이 발급받은 토큰으로 API 요청할 때는 `Authorization` 헤더에 `Bearer` 형식으로 토큰을 포함시켜야 합니다.

> [!NOTE]
> 모바일 애플리케이션 토큰 발급 시 [토큰 권한](#token-abilities)도 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호 (Protecting Routes)

앞서 설명한 것처럼 `sanctum` 인증 가드를 라우트에 붙여 모든 요청이 인증되도록 보호할 수 있습니다:

```
Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="revoking-mobile-api-tokens"></a>
### 토큰 취소 (Revoking Tokens)

사용자가 모바일 기기에 발급된 API 토큰을 취소하도록 하려면, 웹 애플리케이션의 "계정 설정" UI에 토큰 이름과 "취소" 버튼을 리스트로 보여주고, 사용자가 버튼을 클릭하면 해당 토큰을 데이터베이스에서 삭제하도록 구현하세요. 사용자 토큰은 `Laravel\Sanctum\HasApiTokens` 트레이트의 `tokens` 관계로 접근할 수 있습니다:

```
// 모든 토큰 취소...
$user->tokens()->delete();

// 특정 토큰 취소...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 중에는 `Sanctum::actingAs` 메서드를 사용해 사용자를 인증하고, 토큰에 부여할 권한 목록을 지정할 수 있습니다:

```
use App\Models\User;
use Laravel\Sanctum\Sanctum;

public function test_task_list_can_be_retrieved()
{
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
}
```

모든 권한을 부여하고 싶다면 `actingAs` 메서드에 `['*']`를 포함시키면 됩니다:

```
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
