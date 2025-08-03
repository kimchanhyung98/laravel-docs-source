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
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증](#spa-authenticating)
    - [SPA 라우트 보호](#protecting-spa-routes)
    - [비공개 방송 채널 권한 부여](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호](#protecting-mobile-api-routes)
    - [토큰 취소](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션, 그리고 간단한 토큰 기반 API를 위한 가벼운 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 자신의 계정에 대해 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰들은 특정 작업 권한(abilities) 또는 범위(scopes)를 부여받아 토큰이 수행할 수 있는 작업을 지정할 수 있습니다.

<a name="how-it-works"></a>
### 작동 방식 (How It Works)

Laravel Sanctum은 두 가지 별개의 문제를 해결하기 위해 존재합니다. 라이브러리의 자세한 내용을 다루기 전에 각 문제를 간략히 설명하겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰 (API Tokens)

먼저, Sanctum은 OAuth 복잡성 없이 사용자에게 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 GitHub와 같은 서비스에서 제공하는 개인 액세스 토큰(personal access tokens)에서 영감을 받았습니다. 예를 들어, 여러분 애플리케이션의 "계정 설정" 화면에서 사용자가 자신의 계정에 대해 API 토큰을 생성할 수 있다고 가정해 보세요. Sanctum을 사용하여 해당 토큰들을 생성하고 관리할 수 있습니다. 이 토큰들은 일반적으로 만료 기간이 매우 길며(수년 단위), 사용자가 언제든 수동으로 취소할 수 있습니다.

Laravel Sanctum은 사용자의 API 토큰을 단일 데이터베이스 테이블에 저장하고, 들어오는 HTTP 요청이 `Authorization` 헤더에 유효한 API 토큰을 포함하는지 확인하여 인증하는 방식으로 이 기능을 제공합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증 (SPA Authentication)

둘째로, Sanctum은 Laravel API와 통신하는 SPA를 간단히 인증할 수 있는 방법을 제공합니다. SPA는 Laravel 애플리케이션과 같은 저장소에 있거나, Vue CLI나 Next.js 같은 별도의 저장소에 존재할 수 있습니다.

이 기능을 위해 Sanctum은 어떠한 토큰도 사용하지 않습니다. 대신, Laravel의 기본 쿠키 기반 세션 인증 서비스를 이용합니다. 일반적으로 Sanctum은 Laravel의 `web` 인증 가드를 활용하여 CSRF 보호, 세션 인증, XSS로 인한 인증 정보 누출 방지 등의 이점을 제공합니다.

Sanctum은 들어오는 요청이 SPA 프런트엔드에서 발생한 경우에만 쿠키 인증을 시도합니다. 요청이 들어오면 먼저 인증 쿠키를 찾고, 없으면 `Authorization` 헤더에 유효한 API 토큰이 있는지 검사합니다.

> [!TIP]
> Sanctum을 사용할 때 API 토큰 인증만, 또는 SPA 인증만 단독으로 사용할 수도 있습니다. 두 기능 모두를 반드시 함께 사용할 필요는 없습니다.

<a name="installation"></a>
## 설치 (Installation)

> [!TIP]
> 최신 버전의 Laravel에는 Laravel Sanctum이 이미 포함되어 있습니다. 그러나 `composer.json`에 `laravel/sanctum`이 없으면, 아래 설치 과정을 따라 설치할 수 있습니다.

Laravel Sanctum은 Composer 패키지 매니저를 통해 설치할 수 있습니다:

```
composer require laravel/sanctum
```

그 다음, `vendor:publish` Artisan 명령어를 사용하여 Sanctum 설정 및 마이그레이션 파일을 퍼블리시하세요. `sanctum` 설정 파일은 애플리케이션의 `config` 디렉터리에 배치됩니다:

```
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
```

마지막으로 데이터베이스 마이그레이션을 실행하세요. Sanctum은 API 토큰을 저장할 데이터베이스 테이블 하나를 생성합니다:

```
php artisan migrate
```

만약 SPA 인증을 사용한다면, 애플리케이션의 `app/Http/Kernel.php` 파일 내 `api` 미들웨어 그룹에 Sanctum 미들웨어를 추가해야 합니다:

```
'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    'throttle:api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

<a name="migration-customization"></a>
#### 마이그레이션 커스터마이징 (Migration Customization)

Sanctum 기본 마이그레이션을 사용하지 않을 경우, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Sanctum::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션 파일은 다음 명령어로 추출할 수 있습니다: `php artisan vendor:publish --tag=sanctum-migrations`

<a name="configuration"></a>
## 설정 (Configuration)

<a name="overriding-default-models"></a>
### 기본 모델 재정의 (Overriding Default Models)

보통 필요하진 않지만, Sanctum이 내부에서 사용하는 `PersonalAccessToken` 모델을 자유롭게 확장할 수 있습니다:

```
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

그 다음, Sanctum에 커스텀 모델을 사용하도록 지시할 수 있습니다. 보통 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 다음과 같이 호출합니다:

```
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * 애플리케이션 서비스 부트스트랩
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

> [!TIP]
> 직접 만든 SPA를 인증하는 데는 API 토큰을 사용하지 말고 Sanctum이 제공하는 [SPA 인증 기능](#spa-authentication)을 사용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

Sanctum은 API 요청 인증에 사용할 수 있는 API 토큰 또는 개인 액세스 토큰을 발급할 수 있습니다. 토큰으로 인증 시, `Authorization` 헤더에 `Bearer` 토큰 형식으로 전달해야 합니다.

사용자 모델이 토큰 발급 기능을 사용하려면, `Laravel\Sanctum\HasApiTokens` 트레이트를 추가해야 합니다:

```
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

토큰을 발급하려면 `createToken` 메서드를 사용하세요. 이 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장 전 SHA-256 해싱되지만, 토큰의 평문 값은 `NewAccessToken` 인스턴스의 `plainTextToken` 속성으로 접근할 수 있습니다. 토큰 생성 직후 사용자에게 평문 토큰을 보여줘야 합니다:

```
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

또한 `HasApiTokens` 트레이트가 제공하는 `tokens` Eloquent 연관관계를 통해 사용자의 모든 토큰을 조회할 수 있습니다:

```
foreach ($user->tokens as $token) {
    //
}
```

<a name="token-abilities"></a>
### 토큰 권한 (Token Abilities)

Sanctum은 토큰에 "권한(abilities)"을 부여할 수 있습니다. 토큰 권한은 OAuth의 "스코프"와 유사한 역할을 합니다. `createToken` 메서드의 두 번째 인자로 권한 문자열 배열을 전달할 수 있습니다:

```
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Sanctum으로 인증된 요청을 처리할 때, 토큰이 특정 권한을 가지고 있는지 `tokenCan` 메서드로 확인할 수 있습니다:

```
if ($user->tokenCan('server:update')) {
    //
}
```

<a name="token-ability-middleware"></a>
#### 토큰 권한 미들웨어 (Token Ability Middleware)

Sanctum은 토큰 권한을 점검하는 두 가지 미들웨어를 제공합니다. 사용하려면 애플리케이션의 `app/Http/Kernel.php` 파일 내 `$routeMiddleware` 배열에 다음을 추가하세요:

```
'abilities' => \Laravel\Sanctum\Http\Middleware\CheckAbilities::class,
'ability' => \Laravel\Sanctum\Http\Middleware\CheckForAnyAbility::class,
```

`abilities` 미들웨어는 라우트에 할당 시, 요청의 토큰이 나열된 모든 권한을 보유했는지 확인합니다:

```
Route::get('/orders', function () {
    // 토큰이 "check-status" 와 "place-orders" 권한을 모두 가짐
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` 미들웨어는 라우트에 할당 시, 요청의 토큰이 나열된 권한 중 최소 한 가지라도 갖고 있는지 확인합니다:

```
Route::get('/orders', function () {
    // 토큰이 "check-status" 또는 "place-orders" 권한을 가짐
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### 1차 UI에서 시작한 요청 (First-Party UI Initiated Requests)

편의를 위해, 요청이 여러분의 1차 SPA에서 왔고 Sanctum의 [SPA 인증](#spa-authentication)을 사용 중이라면 `tokenCan` 메서드는 항상 `true`를 반환합니다.

하지만 이것이 반드시 애플리케이션이 사용자가 동작을 수행하도록 허용해야 한다는 의미는 아닙니다. 보통 애플리케이션의 [인가 정책](/docs/{{version}}/authorization#creating-policies)이 토큰이 권한을 갖는지 그리고 사용자 인스턴스가 해당 동작을 수행할 수 있는지 함께 확인합니다.

예를 들어, 서버를 관리하는 애플리케이션이라면 토큰이 서버 업데이트 권한을 갖고, 그리고 그 서버가 해당 사용자에 속하는지 검사하는 로직이 있을 수 있습니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update');
```

처음에는 1차 UI에서 오는 요청에 대해 `tokenCan`이 항상 `true`를 반환하는 것이 낯설 수 있지만, 이렇게 하면 API 토큰이 항상 존재한다고 가정하고 `tokenCan` 메서드를 사용할 수 있어 편리합니다. 따라서 UI에서 온 요청인지 또는 제3자 API 호출인지 상관없이 언제든 인가 정책에서 `tokenCan`을 호출할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

들어오는 모든 요청이 인증되어야 하는 라우트는 `routes/web.php`나 `routes/api.php` 파일의 라우트에 `sanctum` 인증 가드를 적용하세요. 이 가드는 요청이 상태 유지 쿠키 인증을 통한 것인지, 아니면 제3자가 보낸 유효 토큰 헤더 인증인지를 검증합니다.

왜 `routes/web.php`에 있는 라우트도 `sanctum` 가드로 인증하라고 권장하는지 궁금할 수 있습니다. Sanctum은 먼저 Laravel의 세션 인증 쿠키로 인증 시도를 하고, 쿠키가 없으면 `Authorization` 헤더 토큰으로 인증을 시도하기 때문입니다. 또한 Sanctum 인증 시 현재 사용자 인스턴스에서 언제든 `tokenCan` 메서드를 호출할 수 있다는 장점도 있습니다:

```
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="revoking-tokens"></a>
### 토큰 취소 (Revoking Tokens)

토큰을 "취소"하려면 데이터베이스에서 삭제하면 됩니다. `Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 관계를 통해 다음과 같이 할 수 있습니다:

```
// 모든 토큰 취소
$user->tokens()->delete();

// 현재 요청에 사용된 토큰 취소
$request->user()->currentAccessToken()->delete();

// 특정 토큰만 취소
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

Sanctum은 Laravel API와 통신하는 SPA를 간단히 인증할 수 있는 방법을 제공합니다. SPA는 Laravel 애플리케이션과 같은 저장소에 있거나 완전히 별도의 저장소에 존재할 수도 있습니다.

이 기능은 어떠한 토큰도 사용하지 않고, Laravel의 기본 쿠키 기반 세션 인증 서비스를 사용합니다. 이를 통해 CSRF 보호, 세션 인증, 인증 정보 XSS 유출 방지 등을 제공합니다.

> [!NOTE]
> SPA와 API가 인증되려면 동일한 최상위 도메인을 공유해야 합니다. 다만 서로 다른 서브도메인에 위치할 수는 있습니다. 또한 요청 시 `Accept: application/json` 헤더를 반드시 보내야 합니다.

<a name="spa-configuration"></a>
### 설정 (Configuration)

<a name="configuring-your-first-party-domains"></a>
#### 1차 도메인 설정 (Configuring Your First-Party Domains)

먼저, SPA가 요청을 보낼 도메인을 설정해야 합니다. Sanctum 설정 파일 `sanctum.php` 내 `stateful` 옵션에 이 도메인들을 정의하세요. 이 설정은 지정한 도메인에서 Laravel 세션 쿠키를 통한 상태 유지 인증을 사용할 수 있게 합니다.

> [!NOTE]
> 로컬 개발 시 포트 번호가 포함된 URL(`127.0.0.1:8000`)이라면 포트 번호도 포함하여 설정해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

다음으로, `app/Http/Kernel.php` 파일의 `api` 미들웨어 그룹에 Sanctum 미들웨어를 추가하세요. 이 미들웨어는 SPA 요청을 세션 쿠키로 인증할 수 있게 하면서, 제3자나 모바일 애플리케이션 요청은 API 토큰으로 인증할 수 있도록 합니다:

```
'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    'throttle:api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

<a name="cors-and-cookies"></a>
#### CORS 및 쿠키

만약 별도 서브도메인에서 SPA를 실행하다가 인증이 안 되는 문제가 발생하면, CORS 또는 세션 쿠키 설정이 잘못되었을 가능성이 큽니다.

애플리케이션의 CORS 설정이 `Access-Control-Allow-Credentials` 헤더를 `true`로 반환하는지 확인하세요. 보통 `config/cors.php` 파일 내 `supports_credentials` 옵션을 `true`로 설정하면 됩니다.

그리고 글로벌 `axios` 인스턴스에서 `withCredentials` 옵션을 활성화해야 합니다. 보통 `resources/js/bootstrap.js` 파일에서 설정합니다. 만약 Axios 대신 다른 HTTP 클라이언트를 사용하는 경우, 동일한 목적의 설정을 적용하세요:

```
axios.defaults.withCredentials = true;
```

마지막으로, 애플리케이션 `config/session.php` 파일에서 세션 쿠키의 `domain` 옵션이 루트 도메인의 모든 서브도메인에 대해 동작하도록 도메인 앞에 `.`을 붙여 설정해야 합니다:

```
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 인증 (Authenticating)

<a name="csrf-protection"></a>
#### CSRF 보호

SPA 인증을 위한 "로그인" 페이지는 먼저 `/sanctum/csrf-cookie` 엔드포인트에 요청을 보내 CSRF 보호를 초기화해야 합니다:

```
axios.get('/sanctum/csrf-cookie').then(response => {
    // 로그인 처리...
});
```

이 요청을 통해 Laravel은 현재 CSRF 토큰이 담긴 `XSRF-TOKEN` 쿠키를 설정합니다. 이후 요청에는 `X-XSRF-TOKEN` 헤더에 이 토큰 값을 포함해야 합니다. Axios와 Angular HttpClient 같은 라이브러리는 이를 자동으로 처리하지만, 그렇지 않은 경우 직접 헤더를 설정해야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호 초기화 후, 애플리케이션의 `/login` 경로에 `POST` 요청을 보내 로그인합니다. `/login` 경로는 수동으로 구현하거나, [Laravel Fortify](/docs/{{version}}/fortify) 같은 헤드리스 인증 패키지를 사용할 수 있습니다.

로그인 요청이 성공하면 인증되고, 이후 라우트 요청은 Laravel이 발급한 세션 쿠키를 통해 자동 인증됩니다. 또한 `/sanctum/csrf-cookie` 요청을 이미 했으므로, HTTP 클라이언트가 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더로 보내면 CSRF 보호가 적용됩니다.

만약 사용자의 세션이 활동 부재로 만료되면, 401 또는 419 HTTP 에러가 발생할 수 있습니다. 이 경우 SPA 로그인 페이지로 리디렉션해야 합니다.

> [!NOTE]
> 직접 `/login` 엔드포인트를 작성할 수 있지만, 반드시 [Laravel 기본 세션 인증 서비스](/docs/{{version}}/authentication#authenticating-users)를 이용하도록 해야 합니다. 보통은 `web` 인증 가드를 사용합니다.

<a name="protecting-spa-routes"></a>
### SPA 라우트 보호 (Protecting Routes)

들어오는 모든 요청이 인증되어야 하는 API 라우트는 `routes/api.php` 파일에 `sanctum` 인증 가드를 할당하세요. 이 가드는 SPA에서 온 요청은 상태 유지 인증으로, 제3자 요청은 API 토큰으로 인증합니다:

```
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="authorizing-private-broadcast-channels"></a>
### 비공개 방송 채널 권한 부여 (Authorizing Private Broadcast Channels)

SPA가 [비공개 또는 프레즌스 방송 채널](/docs/{{version}}/broadcasting#authorizing-channels)에서 인증해야 하는 경우, `routes/api.php` 파일에 다음과 같이 `Broadcast::routes` 메서드를 호출하세요:

```
Broadcast::routes(['middleware' => ['auth:sanctum']]);
```

Pusher 권한 요청을 정상 처리하려면, [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation)를 초기화할 때 다음과 같이 커스텀 `authorizer`를 제공해야 합니다. 이를 통해 Pusher가 CORS 설정에 맞게 올바른 `axios` 인스턴스를 사용하도록 합니다:

```
window.Echo = new Echo({
    broadcaster: "pusher",
    cluster: process.env.MIX_PUSHER_APP_CLUSTER,
    encrypted: true,
    key: process.env.MIX_PUSHER_APP_KEY,
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

Sanctum 토큰을 사용하여 모바일 애플리케이션이 API를 인증하는 데에도 사용할 수 있습니다. 모바일 인증 과정은 제3자 API 요청 인증과 유사하지만, API 토큰 발급 방식에 약간 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

먼저 사용자 이메일/사용자명, 비밀번호, 디바이스명을 받아 새 Sanctum 토큰과 교환하는 라우트를 생성합니다. 디바이스명은 정보를 구분하기 위한 것으로, 예를 들어 "Nuno's iPhone 12" 같은 사용자 인식이 쉬운 이름이면 됩니다.

일반적으로 모바일 애플리케이션 로그인 화면에서 이 토큰 발급 엔드포인트에 요청하며, 평문 API 토큰을 받아 모바일 기기에 저장하고 추가 API 요청 시 사용합니다:

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

모바일 앱이 API 요청 시 토큰을 `Authorization` 헤더에 `Bearer` 토큰으로 포함해서 보내야 합니다.

> [!TIP]
> 모바일 애플리케이션 토큰 발급 시에도 [토큰 권한](#token-abilities)을 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호 (Protecting Routes)

이미 설명한 것처럼, 들어오는 요청이 모두 인증되도록 하려면 `sanctum` 인증 가드를 라우트에 할당하세요:

```
Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="revoking-mobile-api-tokens"></a>
### 토큰 취소 (Revoking Tokens)

사용자가 모바일 디바이스에 발급된 API 토큰을 취소할 수 있도록, 웹 애플리케이션의 "계정 설정" 화면에 토큰 이름과 "취소" 버튼을 나열할 수 있습니다. 사용자가 취소 버튼을 누르면 데이터베이스에서 해당 토큰을 삭제하면 됩니다. `Laravel\Sanctum\HasApiTokens` 트레이트의 `tokens` 관계로 접근 가능합니다:

```
// 모든 토큰 취소
$user->tokens()->delete();

// 특정 토큰 취소
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 중에는 `Sanctum::actingAs` 메서드를 사용해 사용자를 인증하고 토큰에 부여할 권한을 지정할 수 있습니다:

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

만약 모든 권한을 부여하고 싶다면 `actingAs` 메서드에 `['*']`를 전달하세요:

```
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```