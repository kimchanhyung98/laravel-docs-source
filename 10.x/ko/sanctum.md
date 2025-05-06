# Laravel Sanctum

- [소개](#introduction)
    - [작동 방식](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 오버라이드](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 권한(Abilities)](#token-abilities)
    - [라우트 보호](#protecting-routes)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증하기](#spa-authenticating)
    - [라우트 보호](#protecting-spa-routes)
    - [비공개 브로드캐스트 채널 권한 부여](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호](#protecting-mobile-api-routes)
    - [토큰 폐기](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션 및 간단한 토큰 기반 API를 위한 경량 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 자신의 계정에 대해 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰들은 수행할 수 있는 작업을 지정하는 권한(abilities)/스코프(scopes)를 부여받을 수 있습니다.

<a name="how-it-works"></a>
### 작동 방식

Laravel Sanctum은 두 가지 별도의 문제를 해결하기 위해 존재합니다. 라이브러리에 대해 더 깊이 알아보기 전에 각각에 대해 살펴보겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰

먼저, Sanctum은 OAuth의 복잡함 없이 사용자에게 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 "개인 액세스 토큰"을 발급하는 GitHub 등 여러 애플리케이션에서 영감을 얻었습니다. 예를 들어, 애플리케이션의 "계정 설정" 화면에 사용자가 자신의 계정에 대한 API 토큰을 생성할 수 있는 인터페이스가 있다면 Sanctum을 사용해 토큰을 생성하고 관리할 수 있습니다. 이 토큰은 일반적으로 매우 긴 만료 기간(수년)을 가지며, 사용자가 언제든 수동으로 폐기할 수 있습니다.

Laravel Sanctum은 사용자 API 토큰을 단일 데이터베이스 테이블에 저장하고, `Authorization` 헤더에 유효한 API 토큰이 포함된 HTTP 요청을 인증하는 방식으로 이 기능을 제공합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증

두 번째로, Sanctum은 Laravel 기반 API와 통신해야 하는 싱글 페이지 애플리케이션(SPA)을 간단히 인증할 수 있는 방법도 제공합니다. 이 SPA들은 Laravel 애플리케이션과 동일한 저장소에 있을 수도 있고, Vue CLI나 Next.js로 만든 완전히 별도의 저장소일 수도 있습니다.

이 기능의 경우, Sanctum은 토큰을 사용하지 않습니다. 대신 Laravel의 기본 쿠키 기반 세션 인증 서비스를 활용합니다. 일반적으로 Sanctum은 Laravel의 `web` 인증 가드를 사용합니다. 이 방식은 CSRF 보호, 세션 인증, XSS를 통한 인증 정보 유출 방지 등 여러 이점을 제공합니다.

Sanctum은 오직 요청이 자신의 SPA 프론트엔드에서 비롯된 경우에만 쿠키로 인증을 시도합니다. Sanctum이 수신된 HTTP 요청을 검사할 때, 먼저 인증 쿠키를 확인하고, 쿠키가 없으면 `Authorization` 헤더에서 유효한 API 토큰을 찾습니다.

> [!NOTE]  
> Sanctum을 오직 API 토큰 인증에만, 또는 SPA 인증에만 사용할 수도 있습니다. 둘 다 반드시 사용할 필요는 없습니다.

<a name="installation"></a>
## 설치

> [!NOTE]  
> 최신 버전의 Laravel에는 이미 Laravel Sanctum이 포함되어 있습니다. 그러나 애플리케이션의 `composer.json`에 `laravel/sanctum`이 포함되어 있지 않다면 아래 설치 방법을 따라주세요.

Composer 패키지 관리자를 이용해 Laravel Sanctum을 설치할 수 있습니다.

```shell
composer require laravel/sanctum
```

다음으로, `vendor:publish` 아티즌 명령어를 사용해 Sanctum의 설정 파일과 마이그레이션 파일을 퍼블리시 하세요. `sanctum` 설정 파일이 애플리케이션의 `config` 디렉터리에 생성됩니다:

```shell
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
```

마지막으로 데이터베이스 마이그레이션을 실행하세요. Sanctum은 API 토큰을 저장할 하나의 데이터베이스 테이블을 생성합니다.

```shell
php artisan migrate
```

SPA 인증에 Sanctum을 사용할 계획이라면, `app/Http/Kernel.php` 파일 내의 `api` 미들웨어 그룹에 Sanctum의 미들웨어를 추가해야 합니다:

    'api' => [
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        \Illuminate\Routing\Middleware\ThrottleRequests::class.':api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

<a name="migration-customization"></a>
#### 마이그레이션 커스터마이징

Sanctum의 기본 마이그레이션 파일을 사용하지 않을 경우, `App\Providers\AppServiceProvider` 클래스의 `register` 메소드에서 `Sanctum::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션 파일을 추출하려면 다음 명령어를 실행하세요: `php artisan vendor:publish --tag=sanctum-migrations`

<a name="configuration"></a>
## 설정

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

일반적으로 필요하지 않지만, Sanctum이 내부적으로 사용하는 `PersonalAccessToken` 모델을 확장할 수 있습니다:

    use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

    class PersonalAccessToken extends SanctumPersonalAccessToken
    {
        // ...
    }

이후 Sanctum의 `usePersonalAccessTokenModel` 메소드를 활용해 커스텀 모델을 사용할 수 있습니다. 일반적으로 이 메소드는 애플리케이션의 서비스 프로바이더의 `boot` 메소드에서 호출해야 합니다:

    use App\Models\Sanctum\PersonalAccessToken;
    use Laravel\Sanctum\Sanctum;

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
    }

<a name="api-token-authentication"></a>
## API 토큰 인증

> [!NOTE]  
> 1st-party SPA를 인증할 때는 API 토큰을 사용하지 마세요. 대신, Sanctum의 내장 [SPA 인증 기능](#spa-authentication)을 사용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급

Sanctum을 사용하면 애플리케이션에 대한 API 요청을 인증할 수 있는 API 토큰(개인 액세스 토큰)을 발급할 수 있습니다. API 토큰을 사용할 때는 토큰을 `Authorization` 헤더에 `Bearer` 토큰으로 포함해야 합니다.

사용자를 위해 토큰을 발급하려면, User 모델에서 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용하세요:

    use Laravel\Sanctum\HasApiTokens;

    class User extends Authenticatable
    {
        use HasApiTokens, HasFactory, Notifiable;
    }

토큰을 발급하려면 `createToken` 메소드를 사용하세요. 이 메소드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장될 때 SHA-256 해싱으로 암호화되지만, 토큰을 생성하면 `NewAccessToken` 인스턴스의 `plainTextToken` 속성으로 토큰의 평문 값을 즉시 확인할 수 있습니다. 이 값을 바로 사용자에게 보여주어야 합니다:

    use Illuminate\Http\Request;

    Route::post('/tokens/create', function (Request $request) {
        $token = $request->user()->createToken($request->token_name);

        return ['token' => $token->plainTextToken];
    });

`HasApiTokens` 트레이트로 제공되는 `tokens` Eloquent 관계를 이용하여 사용자의 모든 토큰에 접근할 수 있습니다:

    foreach ($user->tokens as $token) {
        // ...
    }

<a name="token-abilities"></a>
### 토큰 권한(Abilities)

Sanctum에서는 토큰에 "권한(abilities)"을 지정할 수 있습니다. 권한은 OAuth의 "스코프(scopes)"와 비슷한 개념입니다. `createToken` 메소드의 두 번째 인자로 문자열 배열을 전달하여 권한을 지정할 수 있습니다:

    return $user->createToken('token-name', ['server:update'])->plainTextToken;

Sanctum으로 인증된 요청을 처리할 때, `tokenCan` 메소드를 사용하여 토큰에 특정 권한이 있는지 확인할 수 있습니다:

    if ($user->tokenCan('server:update')) {
        // ...
    }

<a name="token-ability-middleware"></a>
#### 토큰 권한 미들웨어

Sanctum에는 요청이 특정 권한을 가진 토큰으로 인증되었는지 확인하는 두 가지 미들웨어도 있습니다. 먼저, 아래와 같이 `app/Http/Kernel.php` 파일의 `$middlewareAliases`에 미들웨어를 등록하세요:

    'abilities' => \Laravel\Sanctum\Http\Middleware\CheckAbilities::class,
    'ability' => \Laravel\Sanctum\Http\Middleware\CheckForAnyAbility::class,

`abilities` 미들웨어는 요청 토큰이 나열된 모든 권한을 가지고 있는지 검사합니다:

    Route::get('/orders', function () {
        // 토큰이 "check-status"와 "place-orders" 권한을 모두 가지고 있어야 함...
    })->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);

`ability` 미들웨어는 요청 토큰이 나열된 권한 중 하나라도 가지고 있는지 검사합니다:

    Route::get('/orders', function () {
        // 토큰이 "check-status" 또는 "place-orders" 권한 중 하나라도 있어야 함...
    })->middleware(['auth:sanctum', 'ability:check-status,place-orders']);

<a name="first-party-ui-initiated-requests"></a>
#### 1st-party UI에서 시작된 요청

편의상, 인증된 요청이 SPA에서 비롯되었고 Sanctum의 내장 [SPA 인증](#spa-authentication)을 사용하는 경우, `tokenCan` 메소드는 항상 `true`를 반환합니다.

하지만, 이는 반드시 사용자가 해당 작업을 수행할 수 있음을 의미하지 않습니다. 보통 애플리케이션의 [권한 정책](/docs/{{version}}/authorization#creating-policies)이 토큰에 부여된 권한과 사용자가 실제로 작업을 수행할 수 있는지 여부를 함께 판별합니다.

예를 들어, 서버 관리를 위한 애플리케이션에서는 토큰이 서버를 업데이트할 권한을 가지고 있고, 서버가 현재 사용자 소유인지 확인할 수 있습니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

UI를 통해 시작된 1st-party 요청에서 `tokenCan` 메소드가 항상 `true`를 반환하는 것이 처음에는 어색해 보일 수 있지만, 어디서든 `tokenCan` 메소드를 통해 API 토큰에 접근하고 그 권한을 참조할 수 있기 때문에 실용적입니다. 이 방식으로, 애플리케이션의 권한 정책 내에서 요청이 UI에서 왔는지, 외부 제3자에서 왔는지에 상관없이 항상 `tokenCan`을 안전하게 사용할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호

모든 수신 요청이 인증되도록 라우트를 보호하려면, `routes/web.php` 및 `routes/api.php` 파일에서 인증이 필요한 라우트에 `sanctum` 인증 가드를 적용하세요. 이 인증 가드는 요청이 상태를 가진(쿠키 인증) 요청이거나, 제3자 요청이라면 유효한 API 토큰 헤더가 있는지 확인합니다.

`routes/web.php`에서 인증 라우트에 `sanctum` 가드를 추천하는 이유는, Sanctum이 우선적으로 Laravel의 세션 인증 쿠키를 사용해 인증을 시도하고, 쿠키가 없으면 `Authorization` 헤더의 토큰으로 인증하기 때문입니다. 모든 요청을 Sanctum으로 인증하면, 현재 인증된 사용자 인스턴스에서 언제든 `tokenCan` 메소드를 사용할 수 있습니다:

    use Illuminate\Http\Request;

    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

<a name="revoking-tokens"></a>
### 토큰 폐기

`Laravel\Sanctum\HasApiTokens` 트레이트에서 제공하는 `tokens` 관계를 이용해 데이터베이스에서 토큰을 삭제하는 방식으로 토큰을 폐기할 수 있습니다:

    // 모든 토큰 폐기
    $user->tokens()->delete();

    // 현재 요청에 사용된 토큰만 폐기
    $request->user()->currentAccessToken()->delete();

    // 특정 토큰만 폐기
    $user->tokens()->where('id', $tokenId)->delete();

<a name="token-expiration"></a>
### 토큰 만료

기본적으로 Sanctum 토큰은 만료되지 않으며, [토큰 폐기](#revoking-tokens)로만 무효화할 수 있습니다. 하지만 애플리케이션 API 토큰의 만료 시간를 설정하려면, `sanctum` 설정 파일의 `expiration` 옵션을 통해 분 단위로 지정할 수 있습니다:

```php
'expiration' => 525600,
```

각 토큰의 만료 시간을 개별적으로 지정하려면, `createToken` 메소드의 세 번째 인자로 만료 날짜를 전달하세요:

```php
return $user->createToken(
    'token-name', ['*'], now()->addWeek()
)->plainTextToken;
```

토큰 만료 시간을 지정한 경우, [스케줄링](/docs/{{version}}/scheduling)을 이용해 만료된 토큰을 정리하는 작업을 예약하세요. Sanctum에는 만료된 토큰을 삭제할 수 있는 `sanctum:prune-expired` 아티즌 명령어가 포함되어 있습니다. 예를 들어, 24시간 이상 경과한 만료 토큰을 매일 삭제하도록 스케줄링할 수 있습니다:

```php
$schedule->command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증

Sanctum은 또한 Laravel 기반 API와 통신해야 하는 싱글 페이지 애플리케이션(SPA)의 인증을 간단하게 처리하는 방법을 제공합니다. 이 SPA는 Laravel 애플리케이션 저장소와 동일한 저장소에 있을 수도, 완전히 별도의 저장소에 있을 수도 있습니다.

이 기능에서는 어떠한 토큰도 사용하지 않고, Laravel의 기본 쿠키 기반 세션 인증 서비스를 사용합니다. 이 방식은 CSRF 보호, 세션 인증, XSS로 인한 인증 정보 유출 방지 등의 이점이 있습니다.

> [!WARNING]  
> SPA와 API가 반드시 같은 최상위 도메인이어야 합니다. 다른 서브도메인일 수는 있습니다. 또한, 요청 시 `Accept: application/json` 헤더와 `Referer` 또는 `Origin` 헤더를 반드시 포함하세요.

<a name="spa-configuration"></a>
### 설정

<a name="configuring-your-first-party-domains"></a>
#### 1st-party 도메인 설정

우선, SPA가 어떤 도메인에서 요청을 보내는지 설정해야 합니다. `sanctum` 설정 파일의 `stateful` 옵션에서 이를 지정할 수 있습니다. 이 옵션은 API 요청 시 Laravel 세션 쿠키를 사용하는 "stateful" 인증이 허용되는 도메인을 결정합니다.

> [!WARNING]  
> 포트 번호(`127.0.0.1:8000`)가 포함된 URL로 접속 중이라면, 포트 번호까지 반드시 명시해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

다음으로, 애플리케이션의 `app/Http/Kernel.php` 파일의 `api` 미들웨어 그룹에 Sanctum 미들웨어를 추가하세요. 이 미들웨어는 SPA에서 오는 요청은 Laravel 세션 쿠키로 인증하도록 하고, 제3자 또는 모바일 앱의 요청은 API 토큰으로 인증할 수 있게 보장합니다:

    'api' => [
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        \Illuminate\Routing\Middleware\ThrottleRequests::class.':api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

<a name="cors-and-cookies"></a>
#### CORS 및 쿠키

별도의 서브도메인에서 실행되는 SPA가 인증에 실패한다면, CORS(교차 출처 자원 공유) 또는 세션 쿠키 설정이 잘못되었을 가능성이 큽니다.

애플리케이션의 CORS 설정에서 `Access-Control-Allow-Credentials` 헤더가 `True`로 반환되는지 확인해야 합니다. `config/cors.php` 파일의 `supports_credentials` 옵션을 `true`로 설정하면 됩니다.

또한, SPA에서 axios를 사용할 경우, 전역 `axios` 인스턴스에 `withCredentials`와 `withXSRFToken` 옵션을 활성화해야 합니다. 보통 `resources/js/bootstrap.js` 파일에서 설정합니다. Axios를 사용하지 않을 경우, 사용하는 HTTP 클라이언트에 맞게 동등하게 설정하세요:

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

마지막으로, 세션 쿠키 도메인 설정에 루트 도메인의 모든 서브도메인을 지원하도록 `config/session.php`에서 도메인 앞에 `.`을 넣어 설정하세요:

    'domain' => '.domain.com',

<a name="spa-authenticating"></a>
### 인증하기

<a name="csrf-protection"></a>
#### CSRF 보호

SPA에서는 "로그인" 페이지에서 먼저 `/sanctum/csrf-cookie` 엔드포인트로 요청해 애플리케이션의 CSRF 보호를 초기화해야 합니다:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // 로그인 실행...
});
```

이 요청 동안, Laravel은 `XSRF-TOKEN` 쿠키에 현재 CSRF 토큰을 설정합니다. 이 토큰은 이후 요청에서 `X-XSRF-TOKEN` 헤더로 전달되어야 하며, Axios나 Angular HttpClient 등은 이를 자동으로 처리해줍니다. 만약 사용하는 자바스크립트 HTTP 라이브러리가 자동으로 헤더를 추가하지 않는다면, 반드시 직접 `X-XSRF-TOKEN` 헤더를 `XSRF-TOKEN` 쿠키 값과 일치하게 설정해야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호가 초기화되었다면, `/login` 라우트에 `POST` 요청을 보내야 합니다. 이 `/login` 라우트는 [직접 구현](/docs/{{version}}/authentication#authenticating-users)할 수도 있고, [Laravel Fortify](/docs/{{version}}/fortify)와 같은 헤드리스 인증 패키지를 사용할 수도 있습니다.

로그인이 성공하면, 클라이언트에 발급된 세션 쿠키를 통해 이후 요청은 자동으로 인증됩니다. 또한, 이미 `/sanctum/csrf-cookie` 엔드포인트를 사용했으므로, 추가 요청에서도 HTTP 클라이언트가 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더에 실어 보내도록 하면 자동으로 CSRF 보호를 받게 됩니다.

물론, 사용자의 세션이 만료되어 이후 요청에서 401 또는 419 HTTP 오류가 발생한다면 SPA의 로그인 페이지로 리다이렉션해야 합니다.

> [!WARNING]  
> 직접 `/login` 엔드포인트를 구현할 수 있지만, 반드시 Laravel의 [표준 세션 인증 서비스](/docs/{{version}}/authentication#authenticating-users)를 사용해 사용자를 인증해야 합니다. 보통 `web` 인증 가드를 사용합니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호

모든 수신 요청이 인증을 거치도록 하려면, API 라우트에 `sanctum` 인증 가드를 적용하세요. 그러면 SPA에서 상태를 가진 인증 요청이거나, 제3자 요청의 경우에는 API 토큰 헤더가 있어야 인증이 됩니다:

    use Illuminate\Http\Request;

    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

<a name="authorizing-private-broadcast-channels"></a>
### 비공개 브로드캐스트 채널 권한 부여

SPA에서 [비공개/프레즌스 브로드캐스트 채널](/docs/{{version}}/broadcasting#authorizing-channels)에 인증이 필요할 경우, `routes/api.php` 파일에 `Broadcast::routes` 메소드를 아래와 같이 넣어야 합니다:

    Broadcast::routes(['middleware' => ['auth:sanctum']]);

Pusher의 인증 요청이 성공하려면, [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation) 초기화 시 맞춤 Pusher `authorizer`를 제공해야 합니다. 이를 통해 [CORS 및 쿠키 설정이 올바른 axios 인스턴스](#cors-and-cookies)를 사용할 수 있습니다:

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

모바일 애플리케이션이 API에 요청할 때도 Sanctum 토큰을 이용해 인증할 수 있습니다. 모바일 앱 요청 인증 절차는 제3자 API 요청과 비슷하지만, API 토큰 발급 방식에서 몇 가지 작은 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급

우선, 사용자의 이메일/사용자명, 비밀번호, 디바이스 이름을 받아서 새로운 Sanctum 토큰을 반환하는 라우트를 만드세요. 이때 "디바이스 이름"은 정보 전달용이며 임의의 값이어도 상관없지만, 사용자가 쉽게 식별할 수 있는 값으로 지정하는 것이 좋습니다(예: "Nuno의 iPhone 12").

일반적으로 모바일 앱의 "로그인" 화면에서 이 엔드포인트로 요청을 보냅니다. 평문 API 토큰이 반환되며, 모바일 기기에 저장했다가 추가 API 요청에 사용합니다:

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

모바일 앱이 토큰을 이용해 API 요청을 할 때는, `Authorization` 헤더에 `Bearer` 토큰 형식으로 넣어야 합니다.

> [!NOTE]  
> 모바일 애플리케이션을 위한 토큰 발급 시에도 [토큰 권한](#token-abilities)을 자유롭게 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호

앞서 설명한 것처럼, 아래와 같이 라우트에 `sanctum` 인증 가드를 달아 모든 요청이 인증되어야 하도록 할 수 있습니다:

    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

<a name="revoking-mobile-api-tokens"></a>
### 토큰 폐기

모바일 기기에 발급된 API 토큰을 폐기할 수 있도록, 웹 애플리케이션의 "계정 설정"과 같은 UI에서 토큰 이름과 "폐기" 버튼을 함께 보여주면 됩니다. 사용자가 "폐기" 버튼을 클릭하면 해당 토큰을 데이터베이스에서 삭제하세요. `Laravel\Sanctum\HasApiTokens` 트레이트의 `tokens` 관계를 통해 접근할 수 있습니다:

    // 모든 토큰 폐기
    $user->tokens()->delete();

    // 특정 토큰만 폐기
    $user->tokens()->where('id', $tokenId)->delete();

<a name="testing"></a>
## 테스트

테스트 시에는, `Sanctum::actingAs` 메소드를 사용해 사용자를 인증하고 토큰에 부여할 권한을 지정할 수 있습니다:

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

토큰에 모든 권한을 부여하려면, `actingAs` 메소드에 `*`를 포함하세요:

    Sanctum::actingAs(
        User::factory()->create(),
        ['*']
    );
