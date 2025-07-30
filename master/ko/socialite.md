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

일반적인 폼 기반 인증 외에도, Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 사용하여 OAuth 제공자와 간단하고 편리하게 인증할 수 있는 방법을 제공합니다. Socialite는 현재 Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket, Slack을 통한 인증을 지원합니다.

> [!NOTE]
> 다른 플랫폼에 대한 어댑터는 커뮤니티 주도 [Socialite Providers](https://socialiteproviders.com/) 웹사이트를 통해 이용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

Socialite를 시작하려면 Composer 패키지 관리자를 사용해 프로젝트 의존성에 패키지를 추가하세요:

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## Socialite 업그레이드 (Upgrading Socialite)

Socialite의 메이저 버전을 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 꼼꼼히 검토하는 것이 중요합니다.

<a name="configuration"></a>
## 설정 (Configuration)

Socialite를 사용하기 전에, 애플리케이션에서 이용할 OAuth 제공자들의 자격 증명(credentials)을 추가해야 합니다. 일반적으로 이 자격 증명은 인증할 서비스의 대시보드에서 "개발자 애플리케이션"을 생성해 얻을 수 있습니다.

이 자격 증명은 애플리케이션의 `config/services.php` 설정 파일에 다음과 같은 키(`facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack`, `slack-openid`)를 사용해 추가해야 합니다. 이는 애플리케이션에서 필요한 제공자에 따라 다릅니다:

```php
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!NOTE]
> `redirect` 옵션에 상대 경로가 포함된 경우, 자동으로 완전한 URL로 변환됩니다.

<a name="authentication"></a>
## 인증 (Authentication)

<a name="routing"></a>
### 라우팅 (Routing)

OAuth 제공자를 사용해 사용자를 인증하려면, 사용자를 해당 OAuth 제공자로 리다이렉트하는 경로와 인증 후 제공자로부터 콜백을 받는 경로, 두 개의 라우트가 필요합니다. 아래 예시는 이 두 경로의 구현을 보여줍니다:

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

`Socialite` 파사드의 `redirect` 메서드는 사용자를 OAuth 제공자 페이지로 리다이렉트하는 동작을 처리하며, `user` 메서드는 사용자가 인증 요청을 승인한 후 해당 요청을 검사하고 제공자로부터 사용자 정보를 받아옵니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장 (Authentication and Storage)

OAuth 제공자로부터 사용자를 받아온 후, 애플리케이션 데이터베이스에서 해당 사용자가 존재하는지 확인하고 [사용자 인증](/docs/master/authentication#authenticate-a-user-instance) 과정을 진행할 수 있습니다. 만약 사용자가 데이터베이스에 존재하지 않는다면, 일반적으로 사용자 레코드를 새로 만들어 저장합니다:

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
> 특정 OAuth 제공자로부터 어떤 사용자 정보를 제공받을 수 있는지 더 자세한 내용은 [사용자 정보 조회](#retrieving-user-details) 문서를 참고하세요.

<a name="access-scopes"></a>
### 접근 권한 범위 (Access Scopes)

사용자를 리다이렉트하기 전에 `scopes` 메서드를 이용해 인증 요청에 포함될 "권한 범위(scopes)"를 지정할 수 있습니다. 이 메서드는 이전에 지정된 범위들과 지정한 범위들을 합칩니다:

```php
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

인증 요청의 모든 기존 권한 범위를 덮어쓰려면 `setScopes` 메서드를 사용하세요:

```php
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="slack-bot-scopes"></a>
### Slack 봇 권한 범위 (Slack Bot Scopes)

Slack API는 각각 고유한 [권한 범위](https://api.slack.com/scopes)를 가진 여러 종류의 [접근 토큰](https://api.slack.com/authentication/token-types)을 제공합니다. Socialite는 다음 두 가지 Slack 토큰 타입과 호환됩니다:

- 봇 토큰 (Bot, 접두사 `xoxb-`)
- 사용자 토큰 (User, 접두사 `xoxp-`)

기본적으로 `slack` 드라이버는 `user` 토큰을 생성하며, 드라이버의 `user` 메서드를 호출하면 사용자의 세부사항을 반환합니다.

봇 토큰은 주로 애플리케이션 사용자가 소유한 외부 Slack 작업공간에 알림을 보내야 할 때 유용합니다. 봇 토큰을 생성하려면 Slack 인증을 위해 사용자를 리다이렉트하기 전에 `asBotUser` 메서드를 호출합니다:

```php
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

또한 Slack이 인증 후 사용자를 애플리케이션으로 리다이렉트할 때, `user` 메서드를 호출하기 전에 반드시 `asBotUser` 메서드를 호출해야 합니다:

```php
$user = Socialite::driver('slack')->asBotUser()->user();
```

봇 토큰을 생성할 때 `user` 메서드는 여전히 `Laravel\Socialite\Two\User` 인스턴스를 반환하지만, 채워지는 속성은 `token` 속성뿐입니다. 이 토큰은 [인증된 사용자의 Slack 작업공간에 알림을 보내기](/docs/master/notifications#notifying-external-slack-workspaces) 위해 저장할 수 있습니다.

<a name="optional-parameters"></a>
### 선택적 매개변수 (Optional Parameters)

일부 OAuth 제공자는 리다이렉트 요청 시 추가 선택적 매개변수를 지원합니다. 요청에 선택적 매개변수를 포함하려면 연관 배열을 `with` 메서드에 전달하세요:

```php
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]
> `with` 메서드를 사용할 때는 `state` 또는 `response_type`과 같은 예약어를 전달하지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
## 사용자 정보 조회 (Retrieving User Details)

사용자가 애플리케이션의 인증 콜백 라우트로 리다이렉트된 후에는 Socialite의 `user` 메서드를 사용해 사용자 정보를 받아올 수 있습니다. `user` 메서드가 반환하는 사용자 객체는 애플리케이션 데이터베이스에 저장할 사용자 정보를 다양하게 제공합니다.

이 객체가 제공하는 속성과 메서드는 인증에 사용한 OAuth 제공자가 OAuth 1.0인지 OAuth 2.0인지에 따라 다를 수 있습니다:

```php
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
#### 토큰으로부터 사용자 정보 조회

유효한 액세스 토큰이 이미 있다면 Socialite의 `userFromToken` 메서드를 사용해 토큰으로부터 사용자 정보를 얻을 수 있습니다:

```php
use Laravel\Socialite\Facades\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

iOS 애플리케이션에서 Facebook Limited Login을 사용하는 경우, Facebook은 액세스 토큰 대신 OIDC 토큰을 반환합니다. OIDC 토큰 역시 `userFromToken` 메서드에 전달할 수 있어 사용자 정보를 조회할 수 있습니다.

<a name="stateless-authentication"></a>
#### 상태 비저장 인증

`stateless` 메서드는 세션 상태 검증을 비활성화하는 데 사용됩니다. 이는 쿠키 기반 세션을 사용하지 않는 상태 비저장 API에 소셜 인증을 추가할 때 유용합니다:

```php
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')->stateless()->user();
```