# Laravel Sanctum

- [소개](#introduction)
    - [동작 방식](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 오버라이드](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 능력(Abilities)](#token-abilities)
    - [라우트 보호](#protecting-routes)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증 수행](#spa-authenticating)
    - [라우트 보호](#protecting-spa-routes)
    - [프라이빗 브로드캐스트 채널 권한 부여](#authorizing-private-broadcast-channels)
- [모바일 앱 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호](#protecting-mobile-api-routes)
    - [토큰 폐기](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션, 그리고 단순한 토큰 기반 API를 위한 경량의 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 계정에 대해 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰들에는 토큰이 수행할 수 있는 작업을 지정하는 능력(Ability) 또는 스코프(Scope)를 부여할 수 있습니다.

<a name="how-it-works"></a>
### 동작 방식

Laravel Sanctum은 서로 다른 두 가지 문제를 해결하기 위해 만들어졌습니다. 라이브러리를 더 깊이 들여다보기 전에 각각에 대해 설명하겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰

먼저, Sanctum은 OAuth의 복잡성 없이 사용자에게 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 GitHub이나 기타 "개인 액세스 토큰"을 발급하는 애플리케이션에서 영감을 받았습니다. 예를 들어, 애플리케이션의 "계정 설정" 화면에서 사용자가 계정용 API 토큰을 생성할 수 있는 화면이 있다고 상상해 보세요. 이러한 토큰을 생성 및 관리하는 데 Sanctum을 사용할 수 있습니다. 이 토큰은 일반적으로 매우 긴 만료 기간(수년)을 가지지만, 사용자가 언제든지 직접 폐기할 수 있습니다.

Laravel Sanctum은 사용자 API 토큰을 하나의 데이터베이스 테이블에 저장하고, `Authorization` 헤더에 유효한 API 토큰이 포함된 HTTP 요청을 인증하는 방식으로 이 기능을 제공합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증

두 번째로, Sanctum은 Laravel 기반 API와 통신해야 하는 싱글 페이지 애플리케이션(SPA)을 인증하는 간단한 방법을 제공합니다. 이 SPA는 Laravel 애플리케이션과 같은 저장소에 있을 수도 있고, Vue CLI나 Next.js로 생성된 완전히 별도의 저장소에 있을 수도 있습니다.

이 기능을 위해 Sanctum은 어떤 형태의 토큰도 사용하지 않습니다. 대신, Laravel의 내장 쿠키 기반 세션 인증 서비스를 사용합니다. 일반적으로 Sanctum은 Laravel의 `web` 인증 가드를 활용합니다. 이는 CSRF 보호, 세션 인증, 인증 자격 증명의 XSS 노출로부터의 보호 등 여러 장점을 제공합니다.

Sanctum은 웹 브라우저에서 SPA 프론트엔드에서 온 요청에 한해서만 쿠키 기반 인증을 시도합니다. 요청이 들어오면 먼저 인증 쿠키를 확인하고, 없을 경우 `Authorization` 헤더에 유효한 API 토큰이 있는지 확인합니다.

> **참고**  
> Sanctum을 오직 API 토큰 인증 용도로만 또는 SPA 인증 용도로만 사용하는 것도 문제 없습니다. Sanctum을 쓴다고 해서 두 가지 기능을 모두 필수로 사용할 필요는 없습니다.

<a name="installation"></a>
## 설치

> **참고**  
> 최신 버전의 Laravel에는 이미 Sanctum이 포함되어 있습니다. 그러나 애플리케이션의 `composer.json`에 `laravel/sanctum`이 포함되어 있지 않다면 아래 설치 방법을 따라 주시기 바랍니다.

Composer 패키지 관리자를 통해 Laravel Sanctum을 설치할 수 있습니다:

```shell
composer require laravel/sanctum
```

다음으로, `vendor:publish` Artisan 명령어를 사용해 Sanctum 설정 및 마이그레이션 파일을 배포해야 합니다. `sanctum` 설정 파일은 애플리케이션의 `config` 디렉터리에 위치합니다:

```shell
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
```

마지막으로 데이터베이스 마이그레이션을 실행해야 합니다. Sanctum은 API 토큰을 저장할 데이터베이스 테이블을 하나 생성합니다:

```shell
php artisan migrate
```

SPA 인증을 사용할 예정이라면 `app/Http/Kernel.php` 파일의 `api` 미들웨어 그룹에 Sanctum 미들웨어를 추가해야 합니다:

    'api' => [
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

<a name="migration-customization"></a>
#### 마이그레이션 커스터마이즈

Sanctum의 기본 마이그레이션을 사용하지 않을 예정이라면, `App\Providers\AppServiceProvider` 클래스의 `register` 메소드 내에 `Sanctum::ignoreMigrations`를 호출해야 합니다. 기본 마이그레이션을 내보내려면 다음 명령을 실행할 수 있습니다: `php artisan vendor:publish --tag=sanctum-migrations`

<a name="configuration"></a>
## 설정

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드

필수 사항은 아니지만, 필요하다면 Sanctum이 내부적으로 사용하는 `PersonalAccessToken` 모델을 확장할 수 있습니다:

    use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

    class PersonalAccessToken extends SanctumPersonalAccessToken
    {
        // ...
    }

이후 Sanctum에게 커스텀 모델을 사용하도록 지시하려면, Sanctum이 제공하는 `usePersonalAccessTokenModel` 메소드를 사용하세요. 일반적으로 이 메소드는 애플리케이션 서비스 프로바이더의 `boot` 메소드에서 호출합니다:

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

<a name="api-token-authentication"></a>
## API 토큰 인증

> **참고**  
> 여러분의 1st-party SPA를 인증할 때 API 토큰을 사용하지 마세요. 대신 Sanctum의 내장 [SPA 인증 기능](#spa-authentication)을 사용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급

Sanctum을 사용하면 API 요청을 인증하는 데 사용할 수 있는 API 토큰(=개인 액세스 토큰)을 발급할 수 있습니다. API 토큰을 사용할 때에는 토큰을 `Authorization` 헤더에 `Bearer` 토큰 형태로 포함해야 합니다.

사용자에게 토큰을 발급하려면 User 모델에 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용해야 합니다:

    use Laravel\Sanctum\HasApiTokens;

    class User extends Authenticatable
    {
        use HasApiTokens, HasFactory, Notifiable;
    }

토큰을 발급하려면 `createToken` 메소드를 사용하세요. 이 메소드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전 SHA-256 해시로 암호화되지만, 반환된 인스턴스의 `plainTextToken` 속성을 통해 평문 값을 얻을 수 있습니다. 토큰 생성 후 즉시 이 값을 사용자에게 보여줘야 합니다:

    use Illuminate\Http\Request;

    Route::post('/tokens/create', function (Request $request) {
        $token = $request->user()->createToken($request->token_name);

        return ['token' => $token->plainTextToken];
    });

`HasApiTokens` 트레이트가 제공하는 `tokens` Eloquent 관계를 통해 사용자의 모든 토큰에 접근할 수 있습니다:

    foreach ($user->tokens as $token) {
        //
    }

<a name="token-abilities"></a>
### 토큰 능력(Abilities)

Sanctum을 사용하면 토큰에 "능력(ability)"을 부여할 수 있습니다. 이는 OAuth의 "스코프(scope)"와 유사한 역할을 합니다. `createToken` 메소드의 두 번째 인자로 문자열 배열을 전달하여 토큰의 능력을 지정할 수 있습니다:

    return $user->createToken('token-name', ['server:update'])->plainTextToken;

Sanctum으로 인증된 요청을 처리하면서, `tokenCan` 메소드를 통해 토큰이 특정 능력을 가지고 있는지 판단할 수 있습니다:

    if ($user->tokenCan('server:update')) {
        //
    }

<a name="token-ability-middleware"></a>
#### 토큰 능력 미들웨어

Sanctum은 요청이 특정 능력을 가진 토큰으로 인증되었는지 확인하는 두 개의 미들웨어도 제공합니다. 먼저, 이 미들웨어를 `app/Http/Kernel.php` 파일의 `$routeMiddleware` 속성에 추가하세요:

    'abilities' => \Laravel\Sanctum\Http\Middleware\CheckAbilities::class,
    'ability' => \Laravel\Sanctum\Http\Middleware\CheckForAnyAbility::class,

`abilities` 미들웨어는 요청 토큰이 모든 나열된 능력을 가지고 있는지 검사합니다:

    Route::get('/orders', function () {
        // 토큰이 "check-status"와 "place-orders" 모두의 능력을 가짐
    })->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);

`ability` 미들웨어는 요청 토큰이 나열된 능력 중 *하나라도* 가지면 통과합니다:

    Route::get('/orders', function () {
        // 토큰이 "check-status" 또는 "place-orders" 중 하나의 능력을 가짐
    })->middleware(['auth:sanctum', 'ability:check-status,place-orders']);

<a name="first-party-ui-initiated-requests"></a>
#### 1st-party UI에서 시작된 요청

편의를 위해, 인증된 요청이 여러분의 1st-party SPA에서 왔고, Sanctum의 [SPA 인증](#spa-authentication)을 사용할 때, `tokenCan` 메소드는 항상 `true`를 반환합니다.

하지만 이것이 곧 사용자가 모든 행동을 할 수 있다는 의미는 아닙니다. 일반적으로 애플리케이션의 [인가 정책](/docs/{{version}}/authorization#creating-policies)에서 토큰의 능력 부여 여부와 실제로 사용자가 해당 행동을 해도 되는지 추가로 확인해야 합니다.

예를 들어, 서버를 관리하는 애플리케이션에서 서버 업데이트를 위해선, 토큰의 능력이 충족되고 서버 소유권도 일치해야 할 수 있습니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

처음에는 `tokenCan` 호출 시 항상 `true`가 반환되는 것처럼 보일 수 있으나, 항상 `tokenCan`을 사용할 수 있다는 점은 매우 편리합니다. 이런 방식으로, 요청이 UI에서 왔는지, API의 외부 소비자에서 왔는지 걱정 없이 인가 정책 내에서 항상 `tokenCan`을 사용할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호

모든 요청이 인증되어야 하는 라우트를 보장하려면, 해당 라우트에 `sanctum` 인증 가드를 붙여야 합니다(`routes/web.php`, `routes/api.php`). 이 가드는 들어오는 요청이 stateful 쿠키 인증 요청이거나, 3rd-party 요청일 때는 올바른 API 토큰 헤더를 가지고 있는지 확인합니다.

`routes/web.php`에서 `sanctum` 가드를 사용하라고 권장하는 이유는, Sanctum이 Laravel의 세션 인증 쿠키로 먼저 인증을 시도하기 때문입니다. 쿠키가 없는 경우, `Authorization` 헤더로 토큰 인증을 시도합니다. 또한, 모든 요청이 Sanctum을 통해 인증된다는 것은 항상 현재 인증된 사용자 인스턴스에서 `tokenCan`을 호출할 수 있음을 의미합니다:

    use Illuminate\Http\Request;

    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

<a name="revoking-tokens"></a>
### 토큰 폐기

`Laravel\Sanctum\HasApiTokens` 트레이트에서 제공하는 `tokens` 관계를 사용하여 데이터베이스에서 토큰을 삭제함으로써 토큰을 "폐기"할 수 있습니다:

    // 모든 토큰 폐기
    $user->tokens()->delete();

    // 현재 요청에 사용된 토큰만 폐기
    $request->user()->currentAccessToken()->delete();

    // 특정 토큰 폐기
    $user->tokens()->where('id', $tokenId)->delete();

<a name="token-expiration"></a>
### 토큰 만료

기본적으로 Sanctum 토큰은 만료되지 않으며, [토큰 폐기](#revoking-tokens)를 통해서만 무효화할 수 있습니다. 그러나 애플리케이션의 `sanctum` 설정 파일에서 `expiration` 옵션을 통해 만료 시간을 설정할 수 있습니다. 이 설정은 토큰이 발급된 후 만료까지의 분(minute) 수를 정의합니다:

```php
'expiration' => 525600,
```

토큰 만료 시간을 설정했다면, [스케줄러 작업](/docs/{{version}}/scheduling)으로 만료된 토큰을 청소하는 것이 좋습니다. Sanctum은 만료된 토큰을 정리하는 `sanctum:prune-expired` Artisan 명령어를 제공합니다. 예를 들어, 만료 후 최소 24시간 지난 토큰을 매일 삭제하도록 작업을 예약할 수 있습니다:

```php
$schedule->command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증

Sanctum은 Laravel 기반 API와 통신해야 하는 싱글 페이지 애플리케이션(SPA)을 쉽고 간단하게 인증하기 위해서도 존재합니다. 이 SPA는 Laravel 애플리케이션과 같은 저장소에 있을 수도 있고, 완전히 별도의 저장소에 있을 수도 있습니다.

이 기능을 위해 Sanctum은 토큰을 전혀 사용하지 않습니다. 대신 Laravel의 내장 쿠키 기반 세션 인증 서비스를 사용하며, 이를 통해 CSRF 보호와 인증, 그리고 인증 자격 증명의 XSS 노출 방지 등 다양한 장점을 제공합니다.

> **경고**  
> 인증을 위해 SPA와 API는 동일한 최상위 도메인을 공유해야 합니다(서브도메인은 달라도 무방). 또한 요청 시 반드시 `Accept: application/json` 헤더를 함께 전송하세요.

<a name="spa-configuration"></a>
### 설정

<a name="configuring-your-first-party-domains"></a>
#### 1st-party 도메인 설정

먼저, SPA가 어느 도메인에서 요청하는지 설정해야 합니다. 이는 `sanctum` 설정 파일의 `stateful` 옵션을 통해 가능합니다. 이 옵션은 어떤 도메인에서 API로의 요청 시 Laravel 세션 쿠키를 통한 "stateful" 인증이 유지될지 결정합니다.

> **경고**  
> 만약 포트가 포함된 URL(예: `127.0.0.1:8000`)로 애플리케이션에 접근한다면, 반드시 도메인 설정에 포트 번호도 포함해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

다음으로, `app/Http/Kernel.php` 파일의 `api` 미들웨어 그룹에 Sanctum 미들웨어를 추가합니다. 이 미들웨어는 SPA의 쿠키 기반 인증 요청을 허용하면서, 3rd-party나 모바일 앱으로부터의 API 토큰 인증도 정상 동작하게 해줍니다:

    'api' => [
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

<a name="cors-and-cookies"></a>
#### CORS 및 쿠키

서브도메인에서 구동되는 SPA로부터의 인증에 문제가 있다면, CORS(교차 출처 리소스 공유) 또는 세션 쿠키 설정이 잘못된 경우일 수 있습니다.

애플리케이션의 CORS 설정이 `Access-Control-Allow-Credentials` 헤더를 `True` 값으로 반환하는지 확인해야 합니다. 이는 `config/cors.php` 파일의 `supports_credentials` 옵션을 `true`로 설정하면 됩니다.

또한, 프론트엔드의 전역 `axios` 인스턴스에 `withCredentials` 옵션을 활성화해야 합니다. 일반적으로 `resources/js/bootstrap.js`에서 수행합니다. Axios를 사용하지 않는 경우 직접 사용하는 HTTP 클라이언트에 맞는 설정을 해야 합니다:

```js
axios.defaults.withCredentials = true;
```

마지막으로, 루트 도메인의 어떤 서브도메인에서도 사용될 수 있도록 세션 쿠키의 도메인 설정을 해야 합니다. `config/session.php` 파일의 도메인 앞에 점(`.`)을 붙이면 됩니다:

    'domain' => '.domain.com',

<a name="spa-authenticating"></a>
### 인증 수행

<a name="csrf-protection"></a>
#### CSRF 보호

SPA에서 인증을 수행하기 위해, SPA의 "로그인" 페이지에서 `/sanctum/csrf-cookie` 엔드포인트에 먼저 요청을 보내 CSRF 보호를 초기화해야 합니다:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // 로그인 처리...
});
```

이 요청 동안, Laravel은 현재 CSRF 토큰이 담긴 `XSRF-TOKEN` 쿠키를 설정합니다. 이후의 요청에서 이 토큰은 `X-XSRF-TOKEN` 헤더로 전달되어야 하며, Axios나 Angular HttpClient 같은 라이브러리들은 이를 자동으로 처리해줍니다. 만약 자동으로 처리되지 않는다면, `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더에 직접 넣어야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호가 초기화된 후, `/login` 라우트에 `POST` 요청을 보내야 합니다. 이 `/login` 라우트는 [직접 구현](/docs/{{version}}/authentication#authenticating-users)하거나 [Laravel Fortify](/docs/{{version}}/fortify) 등 헤드리스 인증 패키지를 사용할 수 있습니다.

로그인 요청이 성공하면, 애플리케이션이 발급한 세션 쿠키를 통해 이후의 모든 요청이 자동으로 인증됩니다. 또한 이미 `/sanctum/csrf-cookie` 요청을 보냈으므로, HTTP 클라이언트가 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더에 자동으로 보내는 한 CSRF 보호가 계속 적용됩니다.

물론, 사용자의 세션이 활동 부족 등으로 만료(ft. 로그아웃)된 경우 이후 요청에 401 또는 419 HTTP 에러가 발생할 수 있습니다. 이럴 경우 사용자를 SPA 로그인 페이지로 리디렉션해야 합니다.

> **경고**  
> 커스텀 `/login` 엔드포인트를 작성하는 것도 자유지만, 반드시 Laravel의 [세션 기반 인증 서비스](/docs/{{version}}/authentication#authenticating-users)를 사용해 사용자를 인증해야 합니다. 일반적으로는 `web` 인증 가드를 사용합니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호

모든 요청이 인증을 필요로 하도록 API 라우트에 `sanctum` 인증 가드를 붙여야 합니다(`routes/api.php`). 이 가드는 SPA의 인증 요청 뿐 아니라 3rd-party에서 오는 유효한 API 토큰 헤더 인증도 모두 처리합니다:

    use Illuminate\Http\Request;

    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

<a name="authorizing-private-broadcast-channels"></a>
### 프라이빗 브로드캐스트 채널 권한 부여

SPA가 [프라이빗/프레즌스 브로드캐스트 채널](/docs/{{version}}/broadcasting#authorizing-channels) 인증이 필요하다면, `Broadcast::routes`를 `routes/api.php`에 넣으세요:

    Broadcast::routes(['middleware' => ['auth:sanctum']]);

다음으로, Pusher의 인증 요청이 성공하려면 [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation) 초기화 시 커스텀 Pusher `authorizer`를 지정해야 합니다. 이를 통해 CORS 및 쿠키가 올바르게 설정된 상태에서 axios 인스턴스를 사용할 수 있습니다:

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

Sanctum 토큰을 사용해 모바일 애플리케이션의 API 요청도 인증할 수 있습니다. 모바일 앱 인증 방식은 외부 API 요청 인증과 거의 비슷하지만, API 토큰 발급 방식에는 약간의 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급

먼저, 이메일/사용자명, 비밀번호, 그리고 디바이스 이름을 받아 새로운 Sanctum 토큰으로 교환해주는 라우트를 만들어야 합니다. 여기서 "디바이스 이름"은 정보 표시용이므로 아무 값이나 사용해도 되고, 일반적으로 "홍길동의 iPhone 12" 같은 식으로 사용자가 디바이스를 구별할 수 있는 명칭이면 좋습니다.

보통 모바일 앱의 "로그인" 화면에서 이 엔드포인트로 요청을 보내 토큰을 받아오고, 받은 토큰은 기기에 저장하여 추가 API 요청에 사용합니다:

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

모바일 앱이 애플리케이션에 API 요청을 보낼 때는, 토큰을 `Authorization` 헤더에 `Bearer` 토큰으로 담아야 합니다.

> **참고**  
> 모바일 앱을 위해 토큰을 발급할 때 [토큰 능력](#token-abilities)을 지정하는 것도 가능합니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호

앞서 설명한 것처럼, 모든 요청이 인증되도록 라우트에 `sanctum` 인증 가드를 붙이면 됩니다:

    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

<a name="revoking-mobile-api-tokens"></a>
### 토큰 폐기

모바일 기기에 발급된 API 토큰을 사용자 스스로 폐기하도록 하려면, "계정 설정" UI에서 토큰 목록을 나열하고 "폐기" 버튼을 제공할 수 있습니다. 사용자가 폐기를 누르면 해당 토큰을 데이터베이스에서 삭제하면 됩니다. 사용자의 API 토큰은 `Laravel\Sanctum\HasApiTokens` 트레이트의 `tokens` 관계를 통해 접근할 수 있습니다:

    // 모든 토큰 폐기
    $user->tokens()->delete();

    // 특정 토큰 폐기
    $user->tokens()->where('id', $tokenId)->delete();

<a name="testing"></a>
## 테스트

테스트 중에는 `Sanctum::actingAs` 메소드를 사용해 사용자를 인증 상태로 만들고, 토큰에 부여할 능력 리스트를 지정할 수 있습니다:

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

토큰에 모든 능력을 부여하려면, `actingAs`에 전달하는 능력 리스트에 `*`를 포함시키세요:

    Sanctum::actingAs(
        User::factory()->create(),
        ['*']
    );