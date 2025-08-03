# Laravel Socialite

- [소개](#introduction)
- [설치](#installation)
- [Socialite 업그레이드](#upgrading-socialite)
- [설정](#configuration)
- [인증](#authentication)
    - [라우팅](#routing)
    - [인증 및 저장](#authentication-and-storage)
    - [접근 권한 범위](#access-scopes)
    - [Slack 봇 권한 범위](#slack-bot-scopes)
    - [선택적 매개변수](#optional-parameters)
- [사용자 정보 조회](#retrieving-user-details)

<a name="introduction"></a>
## 소개 (Introduction)

일반적인 폼 기반 인증 외에도, Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 사용하여 OAuth 공급자와 간단하고 편리하게 인증할 수 있는 방법을 제공합니다. Socialite는 현재 Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket, Slack을 통한 인증을 지원합니다.

> [!NOTE]
> 다른 플랫폼용 어댑터는 커뮤니티에서 운영하는 [Socialite Providers](https://socialiteproviders.com/) 웹사이트에서 제공됩니다.

<a name="installation"></a>
## 설치 (Installation)

Socialite를 시작하려면, Composer 패키지 관리자를 사용하여 프로젝트의 의존성에 패키지를 추가하세요:

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## Socialite 업그레이드 (Upgrading Socialite)

Socialite의 새로운 메이저 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 꼼꼼히 확인하는 것이 중요합니다.

<a name="configuration"></a>
## 설정 (Configuration)

Socialite를 사용하기 전에, 애플리케이션에서 사용할 OAuth 공급자의 자격 증명을 추가해야 합니다. 일반적으로 이 자격 증명은 인증하려는 서비스의 대시보드에서 "개발자 애플리케이션"을 생성하여 얻을 수 있습니다.

이 자격 증명은 애플리케이션의 `config/services.php` 설정 파일에 아래 예시처럼 `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack`, `slack-openid` 중 해당하는 키로 추가해야 합니다:

```php
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!NOTE]
> `redirect` 옵션에 상대 경로를 사용해도, 자동으로 완전한 URL로 변환됩니다.

<a name="authentication"></a>
## 인증 (Authentication)

<a name="routing"></a>
### 라우팅 (Routing)

OAuth 공급자를 통해 사용자를 인증하려면 두 가지 라우트가 필요합니다: 하나는 사용자를 OAuth 공급자로 리디렉션하는 용도이며, 다른 하나는 인증 후 공급자로부터 콜백을 받는 용도입니다. 아래 예시는 두 라우트를 어떻게 구현하는지 보여줍니다:

```php
use Laravel\Socialite\Facades\Socialite;

Route::get('/auth/redirect', function () {
    return Socialite::driver('github')->redirect();
});

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // $user->token
});
```

`Socialite` 페이사드가 제공하는 `redirect` 메서드는 사용자를 OAuth 공급자로 안전하게 리디렉션하고, `user` 메서드는 인증 요청을 승인한 후 사용자 정보를 공급자로부터 받아옵니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장 (Authentication and Storage)

OAuth 공급자로부터 유저 정보를 받은 후, 애플리케이션의 데이터베이스에 해당 사용자가 있는지 확인하고 [사용자를 인증](/docs/12.x/authentication#authenticate-a-user-instance)할 수 있습니다. 만약 사용자가 없다면, 일반적으로 새 사용자를 데이터베이스에 등록합니다:

```php
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
> 특정 OAuth 공급자에서 어떤 사용자 정보를 제공하는지 더 궁금하다면 [사용자 정보 조회](#retrieving-user-details) 문서를 참고하세요.

<a name="access-scopes"></a>
### 접근 권한 범위 (Access Scopes)

사용자를 리디렉션하기 전에, 인증 요청에 포함할 "권한 범위(scopes)"를 `scopes` 메서드로 지정할 수 있습니다. 이 메서드는 이전에 지정한 모든 scopes와 새로 지정한 scopes를 병합합니다:

```php
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

모든 기존 권한 범위를 덮어쓰려면 `setScopes` 메서드를 사용하세요:

```php
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="slack-bot-scopes"></a>
### Slack 봇 권한 범위 (Slack Bot Scopes)

Slack API는 [여러 종류의 액세스 토큰](https://api.slack.com/authentication/token-types)을 제공하며, 각각 고유한 [권한 범위](https://api.slack.com/scopes)를 갖습니다. Socialite는 다음 두 Slack 액세스 토큰 유형을 모두 지원합니다:

<div class="content-list" markdown="1">

- 봇 토큰 (접두사 `xoxb-`)
- 사용자 토큰 (접두사 `xoxp-`)

</div>

기본적으로 `slack` 드라이버는 사용자 토큰을 생성하며, `user` 메서드를 호출하면 해당 사용자의 정보를 반환합니다.

봇 토큰은 주로 애플리케이션이 사용자의 외부 Slack 워크스페이스에 알림을 보낼 때 유용합니다. 봇 토큰을 생성하려면, Slack 인증 전에 `asBotUser` 메서드를 호출하세요:

```php
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

또한 Slack 인증 후 사용자 콜백에서 `user` 메서드를 호출하기 전에 반드시 `asBotUser` 메서드를 호출해야 합니다:

```php
$user = Socialite::driver('slack')->asBotUser()->user();
```

봇 토큰 생성 시 `user` 메서드는 여전히 `Laravel\Socialite\Two\User` 인스턴스를 반환하지만, `token` 속성만 채워집니다. 이 토큰은 인증된 사용자의 Slack 워크스페이스에 알림을 보내기 위해 저장할 수 있습니다.(/docs/12.x/notifications#notifying-external-slack-workspaces)

<a name="optional-parameters"></a>
### 선택적 매개변수 (Optional Parameters)

여러 OAuth 공급자는 리디렉션 요청에 추가적인 선택적 매개변수를 지원합니다. 요청에 선택적 매개변수를 포함하려면, 연관 배열을 `with` 메서드에 전달하세요:

```php
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]
> `with` 메서드를 사용할 때는 `state` 또는 `response_type` 같은 예약어를 전달하지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
## 사용자 정보 조회 (Retrieving User Details)

사용자가 애플리케이션의 인증 콜백 경로로 리디렉션되면, Socialite의 `user` 메서드를 사용해 사용자의 상세 정보를 가져올 수 있습니다. `user` 메서드가 반환하는 사용자 객체는 데이터베이스에 저장할 수 있는 다양한 속성과 메서드를 제공합니다.

OAuth 1.0 또는 OAuth 2.0 지원 여부에 따라 이 객체의 프로퍼티와 메서드에 차이가 있을 수 있습니다:

```php
use Laravel\Socialite\Facades\Socialite;

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // OAuth 2.0 공급자...
    $token = $user->token;
    $refreshToken = $user->refreshToken;
    $expiresIn = $user->expiresIn;

    // OAuth 1.0 공급자...
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // 모든 공급자...
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();
});
```

<a name="retrieving-user-details-from-a-token-oauth2"></a>
#### 토큰으로 사용자 정보 조회 (Retrieving User Details From a Token)

이미 유효한 액세스 토큰을 갖고 있다면, Socialite의 `userFromToken` 메서드를 통해 사용자 정보를 직접 조회할 수 있습니다:

```php
use Laravel\Socialite\Facades\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

iOS 앱을 통해 Facebook Limited Login을 사용하는 경우, Facebook은 액세스 토큰 대신 OIDC 토큰을 반환합니다. 이 토큰도 `userFromToken` 메서드에 전달하여 사용자 정보를 조회할 수 있습니다.

<a name="stateless-authentication"></a>
#### 상태 비유지 인증 (Stateless Authentication)

`stateless` 메서드는 세션 상태 확인을 비활성화할 때 사용합니다. 쿠키 기반 세션을 사용하지 않는 무상태(stateless) API에 소셜 인증을 추가할 때 유용합니다:

```php
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')->stateless()->user();
```