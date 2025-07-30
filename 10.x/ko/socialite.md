# Laravel Socialite

- [소개](#introduction)
- [설치](#installation)
- [Socialite 업그레이드](#upgrading-socialite)
- [설정](#configuration)
- [인증](#authentication)
    - [라우팅](#routing)
    - [인증 및 저장](#authentication-and-storage)
    - [접근 권한 범위(Scopes)](#access-scopes)
    - [Slack 봇 권한 범위](#slack-bot-scopes)
    - [선택적 파라미터](#optional-parameters)
- [사용자 정보 가져오기](#retrieving-user-details)

<a name="introduction"></a>
## 소개 (Introduction)

일반적인 폼 기반 인증 외에도, Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 사용하여 OAuth 공급자를 통한 간단하고 편리한 인증 방법을 제공합니다. Socialite는 현재 Facebook, Twitter, LinkedIn, Google, GitHub, GitLab, Bitbucket, Slack을 통한 인증을 지원합니다.

> [!NOTE]  
> 커뮤니티 주도 [Socialite Providers](https://socialiteproviders.com/) 웹사이트를 통해 다른 플랫폼을 위한 어댑터도 제공됩니다.

<a name="installation"></a>
## 설치 (Installation)

Socialite를 시작하려면 Composer 패키지 관리자를 사용하여 패키지를 프로젝트 의존성에 추가하세요:

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## Socialite 업그레이드 (Upgrading Socialite)

Socialite의 주요 버전을 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 꼼꼼히 검토하는 것이 중요합니다.

<a name="configuration"></a>
## 설정 (Configuration)

Socialite를 사용하기 전에, 애플리케이션에서 사용할 OAuth 공급자의 자격 증명을 추가해야 합니다. 일반적으로 이 자격 증명은 인증할 서비스의 대시보드에서 "개발자 애플리케이션"을 생성하여 얻습니다.

이 자격 증명은 애플리케이션의 `config/services.php` 설정 파일에 추가하며, 애플리케이션이 요구하는 공급자에 따라 `facebook`, `twitter` (OAuth 1.0), `twitter-oauth-2` (OAuth 2.0), `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, 또는 `slack` 키를 사용하세요:

```
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!NOTE]  
> `redirect` 옵션에 상대 경로를 넣으면 자동으로 완전한 URL로 변환됩니다.

<a name="authentication"></a>
## 인증 (Authentication)

<a name="routing"></a>
### 라우팅 (Routing)

OAuth 공급자를 사용해 사용자를 인증하려면, 두 개의 라우트가 필요합니다: 하나는 사용자를 OAuth 공급자로 리디렉션하기 위한 라우트, 다른 하나는 인증 후 공급자로부터 콜백을 받기 위한 라우트입니다. 아래 예시는 두 라우트 구현을 보여줍니다:

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

`Socialite` 파사드의 `redirect` 메서드는 사용자를 OAuth 공급자로 리디렉션하며, `user` 메서드는 요청을 검사해 사용자가 인증을 승인한 후 공급자로부터 사용자 정보를 가져옵니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장 (Authentication and Storage)

OAuth 공급자로부터 사용자를 받은 후, 애플리케이션 데이터베이스에 해당 사용자가 존재하는지 확인하고 [사용자를 인증](/docs/10.x/authentication#authenticate-a-user-instance)할 수 있습니다. 만약 사용자 데이터베이스에 존재하지 않는다면, 일반적으로 새 레코드를 만들어 사용자를 등록합니다:

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
> 각 OAuth 공급자가 제공하는 사용자 정보에 관한 자세한 내용은 [사용자 정보 가져오기](#retrieving-user-details) 문서를 확인하세요.

<a name="access-scopes"></a>
### 접근 권한 범위(Scopes)

사용자를 리디렉션하기 전에 `scopes` 메서드를 사용하여 인증 요청에 포함시킬 "권한 범위"를 지정할 수 있습니다. 이 메서드는 이전에 지정한 모든 범위와 새로 지정한 범위를 병합합니다:

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

인증 요청에 포함된 모든 범위를 덮어쓰려면 `setScopes` 메서드를 사용하세요:

```
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="slack-bot-scopes"></a>
### Slack 봇 권한 범위 (Slack Bot Scopes)

Slack API는 서로 다른 종류의 액세스 토큰([토큰 종류](https://api.slack.com/authentication/token-types))을 제공하며, 각각 고유한 [권한 범위](https://api.slack.com/scopes)를 가집니다. Socialite는 다음 두 Slack 토큰 유형과 호환됩니다:

<div class="content-list" markdown="1">

- Bot (접두사 `xoxb-`)
- User (접두사 `xoxp-`)

</div>

기본적으로 `slack` 드라이버는 `user` 토큰을 생성하며, `user` 메서드를 호출하면 사용자 정보를 반환합니다.

봇 토큰은 주로 애플리케이션 사용자가 소유한 외부 Slack 작업공간에 알림을 보내려는 경우에 유용합니다. 봇 토큰을 생성하려면, 사용자를 Slack 인증으로 리디렉션하기 전에 `asBotUser` 메서드를 호출하세요:

```
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

또한 Slack이 인증 후 사용자를 애플리케이션으로 리디렉션할 때, `user` 메서드를 호출하기 전에 반드시 `asBotUser` 메서드를 먼저 호출해야 합니다:

```
$user = Socialite::driver('slack')->asBotUser()->user();
```

봇 토큰을 생성할 경우, `user` 메서드는 여전히 `Laravel\Socialite\Two\User` 인스턴스를 반환하지만, 오직 `token` 속성만 채워집니다. 이 토큰은 [인증된 사용자의 Slack 작업공간에 알림을 보내는 데](/docs/10.x/notifications#notifying-external-slack-workspaces) 저장해 둘 수 있습니다.

<a name="optional-parameters"></a>
### 선택적 파라미터 (Optional Parameters)

일부 OAuth 공급자는 리디렉션 요청 시 추가적인 선택적 파라미터를 지원합니다. 요청에 선택적 파라미터를 포함하려면, 연관 배열을 인자로 `with` 메서드를 호출하세요:

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]  
> `with` 메서드를 사용할 때는 `state`, `response_type` 등의 예약어를 포함하지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
## 사용자 정보 가져오기 (Retrieving User Details)

사용자가 애플리케이션의 인증 콜백 라우트로 리디렉션된 후에는 Socialite의 `user` 메서드를 사용해 사용자의 정보를 가져올 수 있습니다. `user` 메서드가 반환하는 사용자 객체는 여러 속성과 메서드를 제공하며, 이를 통해 사용자 정보를 데이터베이스에 저장할 수 있습니다.

OAuth 공급자가 OAuth 1.0 또는 OAuth 2.0을 지원하는지에 따라 객체의 사용 가능한 속성과 메서드는 다를 수 있습니다:

```
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
#### 토큰으로 사용자 정보 가져오기 (OAuth2) (Retrieving User Details From a Token (OAuth2))

이미 유효한 사용자의 액세스 토큰이 있는 경우, Socialite의 `userFromToken` 메서드를 사용해 사용자 정보를 가져올 수 있습니다:

```
use Laravel\Socialite\Facades\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

<a name="retrieving-user-details-from-a-token-and-secret-oauth1"></a>
#### 토큰과 시크릿으로 사용자 정보 가져오기 (OAuth1) (Retrieving User Details From a Token and Secret (OAuth1))

이미 유효한 토큰과 시크릿이 있는 경우, Socialite의 `userFromTokenAndSecret` 메서드를 사용해 사용자 정보를 가져올 수 있습니다:

```
use Laravel\Socialite\Facades\Socialite;

$user = Socialite::driver('twitter')->userFromTokenAndSecret($token, $secret);
```

<a name="stateless-authentication"></a>
#### 상태 비저장 인증 (Stateless Authentication)

`stateless` 메서드는 세션 상태 검증을 비활성화하는 데 사용합니다. 쿠키 기반 세션을 사용하지 않는 상태 비저장 API에 소셜 인증을 추가할 때 유용합니다:

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')->stateless()->user();
```

> [!WARNING]  
> 상태 비저장 인증은 Twitter OAuth 1.0 드라이버에서는 지원되지 않습니다.