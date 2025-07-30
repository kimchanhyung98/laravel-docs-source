# Laravel Socialite

- [소개](#introduction)
- [설치](#installation)
- [Socialite 업그레이드](#upgrading-socialite)
- [설정](#configuration)
- [인증](#authentication)
    - [라우팅](#routing)
    - [인증 및 저장](#authentication-and-storage)
    - [접근 권한 범위(Access Scopes)](#access-scopes)
    - [선택적 매개변수](#optional-parameters)
- [사용자 정보 조회](#retrieving-user-details)

<a name="introduction"></a>
## 소개 (Introduction)

일반적인 폼 기반 인증 외에도 Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 사용하여 OAuth 제공자를 통한 간단하고 편리한 인증 방법을 제공합니다. Socialite는 현재 Facebook, Twitter, LinkedIn, Google, GitHub, GitLab, Bitbucket 인증을 지원합니다.

> [!NOTE]
> 다른 플랫폼용 어댑터는 커뮤니티 주도의 [Socialite Providers](https://socialiteproviders.com/) 사이트에서 제공됩니다.

<a name="installation"></a>
## 설치 (Installation)

Socialite를 시작하려면 Composer 패키지 관리자를 사용하여 프로젝트의 의존성에 패키지를 추가하세요:

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## Socialite 업그레이드 (Upgrading Socialite)

Socialite의 새로운 메이저 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 꼼꼼히 검토하는 것이 중요합니다.

<a name="configuration"></a>
## 설정 (Configuration)

Socialite를 사용하기 전에, 애플리케이션에서 사용할 OAuth 제공자의 인증 정보를 추가해야 합니다. 일반적으로 이 인증 정보는 인증할 서비스의 대시보드에서 "개발자 애플리케이션"을 생성해서 얻을 수 있습니다.

이 인증 정보는 애플리케이션의 `config/services.php` 설정 파일에 추가하며, 애플리케이션이 요구하는 제공자에 따라 `facebook`, `twitter`(OAuth 1.0), `twitter-oauth-2`(OAuth 2.0), `linkedin`, `google`, `github`, `gitlab`, 또는 `bitbucket` 키를 사용합니다:

```
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!NOTE]
> `redirect` 옵션에 상대 경로가 포함되어 있으면, 자동으로 완전한 URL로 변환됩니다.

<a name="authentication"></a>
## 인증 (Authentication)

<a name="routing"></a>
### 라우팅 (Routing)

OAuth 제공자를 사용해 사용자를 인증하려면 두 개의 라우트가 필요합니다. 하나는 사용자를 OAuth 제공자로 리다이렉트하는 용도이며, 다른 하나는 인증 후 제공자가 호출하는 콜백을 받는 용도입니다. 다음 예시는 두 라우트를 구현한 예입니다:

```
use Laravel\Socialite\Facades\Socialite;

Route::get('/auth/redirect', function () {
    return Socialite::driver('github')->redirect();
});

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // $user->token
});
```

`Socialite` 페이사드의 `redirect` 메서드는 사용자를 OAuth 제공자로 안전하게 리다이렉트하며, `user` 메서드는 인증 요청이 승인된 후 요청을 처리해 제공자로부터 사용자 정보를 가져옵니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장 (Authentication & Storage)

OAuth 제공자로부터 사용자를 획득한 후 애플리케이션의 데이터베이스에 사용자가 존재하는지 확인하고, 존재한다면 [사용자 인증](/docs/9.x/authentication#authenticate-a-user-instance)을 수행하세요. 사용자가 데이터베이스에 없을 경우, 일반적으로 새로운 사용자 레코드를 생성합니다:

```
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Laravel\Socialite\Facades\Socialite;

Route::get('/auth/callback', function () {
    $githubUser = Socialite::driver('github')->user();

    $user = User::updateOrCreate([
        'github_id' => $githubUser->id,
    ], [
        'name' => $githubUser->name,
        'email' => $githubUser->email,
        'github_token' => $githubUser->token,
        'github_refresh_token' => $githubUser->refreshToken,
    ]);

    Auth::login($user);

    return redirect('/dashboard');
});
```

> [!NOTE]
> 특정 OAuth 제공자에서 어떤 사용자 정보가 제공되는지 자세한 내용은 [사용자 정보 조회](#retrieving-user-details) 문서를 참고하세요.

<a name="access-scopes"></a>
### 접근 권한 범위(Access Scopes)

사용자를 리다이렉트하기 전에 `scopes` 메서드를 사용해 인증 요청에 포함할 "권한 범위"를 지정할 수 있습니다. 이 메서드는 이전에 지정된 모든 권한 범위와 새로 지정한 권한 범위를 병합합니다:

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

만약 기존 권한 범위를 모두 덮어쓰고 싶다면 `setScopes` 메서드를 사용하세요:

```
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="optional-parameters"></a>
### 선택적 매개변수 (Optional Parameters)

몇몇 OAuth 제공자는 리다이렉트 요청에 다른 선택적 매개변수를 지원합니다. 선택적 매개변수를 포함하려면, `with` 메서드에 연관 배열을 전달하세요:

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]
> `with` 메서드를 사용할 때는 `state`나 `response_type` 같은 예약어를 전달하지 않도록 주의해야 합니다.

<a name="retrieving-user-details"></a>
## 사용자 정보 조회 (Retrieving User Details)

사용자가 애플리케이션의 인증 콜백 라우트로 리다이렉트된 후, Socialite의 `user` 메서드를 사용해 사용자의 정보를 조회할 수 있습니다. `user` 메서드가 반환하는 사용자 객체에는 애플리케이션에서 사용자를 저장할 때 활용할 수 있는 다양한 속성 및 메서드가 포함되어 있습니다.

이 객체에서 제공되는 속성과 메서드는 사용하는 OAuth 제공자가 OAuth 1.0 또는 OAuth 2.0을 지원하는지에 따라 차이가 있을 수 있습니다:

```
use Laravel\Socialite\Facades\Socialite;

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // OAuth 2.0 제공자...
    $token = $user->token;
    $refreshToken = $user->refreshToken;
    $expiresIn = $user->expiresIn;

    // OAuth 1.0 제공자...
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // 모든 제공자...
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();
});
```

<a name="retrieving-user-details-from-a-token-oauth2"></a>
#### 토큰으로 사용자 정보 조회 (OAuth2)

이미 유효한 액세스 토큰이 있다면, Socialite의 `userFromToken` 메서드를 사용해 해당 사용자의 상세 정보를 조회할 수 있습니다:

```
use Laravel\Socialite\Facades\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

<a name="retrieving-user-details-from-a-token-and-secret-oauth1"></a>
#### 토큰과 시크릿으로 사용자 정보 조회 (OAuth1)

이미 유효한 토큰과 시크릿이 있다면, Socialite의 `userFromTokenAndSecret` 메서드를 사용해 사용자 정보를 조회할 수 있습니다:

```
use Laravel\Socialite\Facades\Socialite;

$user = Socialite::driver('twitter')->userFromTokenAndSecret($token, $secret);
```

<a name="stateless-authentication"></a>
#### 상태 비저장 인증 (Stateless Authentication)

`stateless` 메서드는 세션 상태 검증을 비활성화할 때 사용합니다. 이는 쿠키 기반 세션을 사용하지 않는 상태 비저장(stateless) API에 소셜 인증 기능을 추가할 때 유용합니다:

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')->stateless()->user();
```

> [!WARNING]
> 상태 비저장 인증은 Twitter OAuth 1.0 드라이버에서는 사용할 수 없습니다.