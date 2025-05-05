# Laravel Socialite

- [소개](#introduction)
- [설치](#installation)
- [Socialite 업그레이드](#upgrading-socialite)
- [설정](#configuration)
- [인증](#authentication)
    - [라우팅](#routing)
    - [인증 및 저장](#authentication-and-storage)
    - [액세스 범위](#access-scopes)
    - [Slack 봇 범위](#slack-bot-scopes)
    - [옵션 파라미터](#optional-parameters)
- [사용자 정보 가져오기](#retrieving-user-details)

<a name="introduction"></a>
## 소개

일반적인 폼 기반 인증 외에도, Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 활용해 OAuth 제공자를 통한 간단하고 편리한 인증 방법을 제공합니다. 현재 Socialite는 Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket, Slack을 통한 인증을 지원합니다.

> [!NOTE]
> 기타 플랫폼을 위한 어댑터는 커뮤니티 기반 [Socialite Providers](https://socialiteproviders.com/) 웹사이트에서 제공됩니다.

<a name="installation"></a>
## 설치

Socialite를 시작하려면, Composer 패키지 관리자를 사용하여 프로젝트의 의존성에 해당 패키지를 추가하세요:

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## Socialite 업그레이드

Socialite의 새로운 주요 버전으로 업그레이드할 때에는 반드시 [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 꼼꼼히 확인하세요.

<a name="configuration"></a>
## 설정

Socialite를 사용하기 전에, 애플리케이션에서 사용하는 OAuth 제공자의 자격 증명을 추가해야 합니다. 일반적으로, 이러한 자격 증명은 인증할 서비스의 대시보드에서 "개발자 애플리케이션"을 생성하여 얻을 수 있습니다.

이 자격 증명은 애플리케이션의 `config/services.php` 설정 파일에 추가해야 하며, 애플리케이션에서 필요한 제공자에 따라 `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack`, 또는 `slack-openid` 키를 사용해야 합니다:

```php
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!NOTE]
> `redirect` 옵션에 상대 경로를 지정할 경우, 해당 경로는 자동으로 완전한 URL로 변환됩니다.

<a name="authentication"></a>
## 인증

<a name="routing"></a>
### 라우팅

OAuth 제공자를 사용해 사용자를 인증하려면, 사용자를 OAuth 제공자로 리디렉션하는 라우트와 인증 후 제공자로부터 콜백을 받는 라우트가 필요합니다. 아래 예시 라우트는 두 라우트의 구현을 보여줍니다:

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

`Socialite` 파사드에서 제공하는 `redirect` 메서드는 사용자를 OAuth 제공자로 리디렉션해주며, `user` 메서드는 들어오는 요청을 검사하고 사용자가 인증 요청을 승인한 후 제공자에서 사용자 정보를 가져옵니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장

사용자 정보를 OAuth 제공자로부터 받아온 뒤, 해당 사용자가 애플리케이션 데이터베이스에 존재하는지 확인하고 [사용자를 인증](/docs/{{version}}/authentication#authenticate-a-user-instance)할 수 있습니다. 사용자가 데이터베이스에 없다면, 일반적으로 새 레코드를 만들어 사용자를 저장합니다:

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
> 특정 OAuth 제공자에서 제공하는 사용자 정보에 대한 자세한 내용은 [사용자 정보 가져오기](#retrieving-user-details) 문서를 참고하세요.

<a name="access-scopes"></a>
### 액세스 범위

사용자를 리디렉션하기 전에, `scopes` 메서드를 사용해 인증 요청에 포함할 "범위(scope)"를 지정할 수 있습니다. 이 메서드는 이전에 지정된 모든 범위와 새로 지정한 범위를 병합합니다:

```php
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

`setScopes` 메서드를 사용하면 인증 요청에 기존 범위를 모두 덮어쓸 수 있습니다:

```php
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="slack-bot-scopes"></a>
### Slack 봇 범위

Slack의 API는 [여러 종류의 액세스 토큰](https://api.slack.com/authentication/token-types)을 제공하며, 각각의 [권한 범위](https://api.slack.com/scopes)가 존재합니다. Socialite는 아래 두 가지 타입의 Slack 액세스 토큰을 모두 지원합니다:

<div class="content-list" markdown="1">

- 봇(Bot, 접두어 `xoxb-`)
- 사용자(User, 접두어 `xoxp-`)

</div>

기본적으로, `slack` 드라이버는 `user` 토큰을 생성하며, 드라이버의 `user` 메서드를 호출하면 사용자의 상세 정보를 반환합니다.

봇 토큰은 애플리케이션이 외부 Slack 워크스페이스(사용자의 워크스페이스)로 알림을 보내야 하는 경우에 주로 사용됩니다. 봇 토큰을 생성하려면, 사용자를 Slack으로 인증 리디렉션하기 전에 `asBotUser` 메서드를 호출하세요:

```php
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

또한, 인증 후 Slack이 사용자를 애플리케이션으로 다시 리디렉션한 뒤에도 `user` 메서드를 호출하기 전에 `asBotUser`를 반드시 호출해야 합니다:

```php
$user = Socialite::driver('slack')->asBotUser()->user();
```

봇 토큰을 생성할 때 `user` 메서드는 여전히 `Laravel\Socialite\Two\User` 인스턴스를 반환하지만, `token` 속성만 채워집니다. 이 토큰은 [인증된 사용자의 Slack 워크스페이스에 알림을 보내는 데](/docs/{{version}}/notifications#notifying-external-slack-workspaces) 사용할 수 있습니다.

<a name="optional-parameters"></a>
### 옵션 파라미터

많은 OAuth 제공자가 리디렉션 요청시, 옵션 파라미터를 추가하는 것을 지원합니다. 옵션 파라미터를 요청에 포함하려면 `with` 메서드에 연관 배열을 전달하세요:

```php
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]
> `with` 메서드를 사용할 때, `state` 나 `response_type` 등 예약어는 파라미터로 넘기지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
## 사용자 정보 가져오기

사용자가 애플리케이션의 인증 콜백 라우트로 리디렉션된 후, Socialite의 `user` 메서드를 사용해 사용자 정보를 가져올 수 있습니다. `user` 메서드가 반환하는 사용자 객체는 데이터베이스에 저장할 수 있는 다양한 속성과 메서드를 제공합니다.

이 객체가 제공하는 속성과 메서드는, 인증에 사용하는 OAuth 제공자가 OAuth 1.0을 지원하는지, 또는 OAuth 2.0을 지원하는지에 따라 다를 수 있습니다:

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
#### 토큰에서 사용자 정보 가져오기

이미 사용자의 유효한 액세스 토큰이 있다면, Socialite의 `userFromToken` 메서드를 사용해 사용자 정보를 얻을 수 있습니다:

```php
use Laravel\Socialite\Facades\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

iOS 애플리케이션을 통한 Facebook Limited Login을 사용하는 경우, Facebook은 액세스 토큰 대신 OIDC 토큰을 반환합니다. OIDC 토큰도 액세스 토큰과 동일하게 `userFromToken` 메서드에 전달해 사용자 정보를 가져올 수 있습니다.

<a name="stateless-authentication"></a>
#### 무상태 인증

`stateless` 메서드는 세션 상태 검증을 비활성화합니다. 이는 쿠키 기반 세션을 사용하지 않는 무상태 API에 소셜 인증을 적용할 때 유용합니다:

```php
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')->stateless()->user();
```