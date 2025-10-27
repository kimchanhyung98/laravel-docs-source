# Laravel Socialite (Laravel Socialite)

- [소개](#introduction)
- [설치](#installation)
- [Socialite 업그레이드](#upgrading-socialite)
- [설정](#configuration)
- [인증](#authentication)
    - [라우팅](#routing)
    - [인증 및 저장](#authentication-and-storage)
    - [액세스 스코프](#access-scopes)
    - [Slack 봇 스코프](#slack-bot-scopes)
    - [선택적 파라미터](#optional-parameters)
- [사용자 정보 가져오기](#retrieving-user-details)

<a name="introduction"></a>
## 소개 (Introduction)

일반적인 폼 기반 인증 외에도, Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 사용하여 OAuth 공급자와의 인증을 쉽고 편리하게 처리할 수 있는 방법을 제공합니다. 현재 Socialite는 Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket, Slack을 통한 인증을 지원합니다.

> [!NOTE]
> 기타 플랫폼에 대한 어댑터는 커뮤니티 기반의 [Socialite Providers](https://socialiteproviders.com/) 웹사이트에서 제공됩니다.

<a name="installation"></a>
## 설치 (Installation)

Socialite를 사용하려면, Composer 패키지 매니저를 이용하여 프로젝트의 의존성 목록에 Socialite를 추가하세요.

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## Socialite 업그레이드 (Upgrading Socialite)

Socialite의 새 주요 버전으로 업그레이드할 때는, [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 반드시 꼼꼼히 검토하시기 바랍니다.

<a name="configuration"></a>
## 설정 (Configuration)

Socialite를 사용하기 전에, 애플리케이션에서 사용할 OAuth 공급자 각각에 대한 자격 증명을 추가해야 합니다. 일반적으로 이 자격 증명은 인증을 진행할 서비스의 대시보드에서 "개발자 애플리케이션"을 생성하여 받게 됩니다.

이 자격 증명 값들은 애플리케이션의 `config/services.php` 설정 파일에 추가해야 하며, 사용하려는 공급자에 따라 `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack`, `slack-openid` 등의 키를 사용해야 합니다.

```php
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!NOTE]
> `redirect` 옵션에 상대 경로가 포함되어 있다면, 자동으로 전체 경로의 URL로 변환됩니다.

<a name="authentication"></a>
## 인증 (Authentication)

<a name="routing"></a>
### 라우팅 (Routing)

OAuth 공급자를 이용해 사용자를 인증하려면 두 개의 라우트가 필요합니다. 하나는 사용자를 OAuth 공급자로 리다이렉트하는 라우트이고, 다른 하나는 인증 후 공급자로부터 콜백을 받아 처리하는 라우트입니다. 아래 예시는 두 라우트의 구현 방식을 보여줍니다.

```php
use Laravel\Socialite\Socialite;

Route::get('/auth/redirect', function () {
    return Socialite::driver('github')->redirect();
});

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // $user->token
});
```

`Socialite` 파사드의 `redirect` 메서드는 사용자를 OAuth 공급자로 리다이렉트하는 작업을 담당합니다. `user` 메서드는 인증 승인이 완료된 후, 들어오는 요청을 검사하고 해당 공급자로부터 사용자 정보를 받아옵니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장 (Authentication and Storage)

OAuth 공급자로부터 사용자를 받아온 뒤, 해당 사용자가 애플리케이션 데이터베이스에 존재하는지 확인하고 [사용자를 인증](/docs/12.x/authentication#authenticate-a-user-instance)할 수 있습니다. 만약 데이터베이스에 존재하지 않는 사용자라면, 일반적으로 새로운 사용자 레코드를 생성하여 저장합니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Laravel\Socialite\Socialite;

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
> 각 OAuth 공급자별로 제공되는 사용자 정보에 대해 더 알고 싶다면, [사용자 정보 가져오기](#retrieving-user-details) 문서를 참고하세요.

<a name="access-scopes"></a>
### 액세스 스코프 (Access Scopes)

사용자를 리다이렉트하기 전에, `scopes` 메서드를 사용하여 인증 요청 시 포함할 “스코프(scope)”를 지정할 수 있습니다. 이 메서드는 기존에 지정된 스코프에 새로 지정한 스코프를 병합하여 적용합니다.

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

인증 요청에 존재하는 모든 스코프를 새 목록으로 덮어쓰려면, `setScopes` 메서드를 사용할 수 있습니다.

```php
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="slack-bot-scopes"></a>
### Slack 봇 스코프 (Slack Bot Scopes)

Slack의 API는 [다양한 종류의 액세스 토큰](https://api.slack.com/authentication/token-types)을 제공하며, 각각 [고유의 권한 스코프](https://api.slack.com/scopes)가 있습니다. Socialite는 다음과 같은 Slack 액세스 토큰 유형 모두를 지원합니다.

<div class="content-list" markdown="1">

- 봇(Bot) 토큰 (`xoxb-`로 시작)
- 사용자(User) 토큰 (`xoxp-`로 시작)

</div>

기본적으로 `slack` 드라이버는 `user` 토큰을 생성하며, 드라이버의 `user` 메서드를 호출하면 사용자의 상세 정보를 반환합니다.

봇 토큰은 애플리케이션의 사용자가 소유한 외부 Slack 워크스페이스에 알림을 보내야 하는 경우에 주로 유용합니다. 봇 토큰을 생성하려면, 인증을 위해 사용자를 Slack으로 리다이렉트하기 전에 `asBotUser` 메서드를 호출하세요.

```php
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

또한, 사용자가 Slack 인증을 완료하고 애플리케이션으로 리다이렉트된 이후, `user` 메서드를 호출하기 전에 반드시 `asBotUser` 메서드를 먼저 호출해야 합니다.

```php
$user = Socialite::driver('slack')->asBotUser()->user();
```

봇 토큰을 생성할 때에도 `user` 메서드는 여전히 `Laravel\Socialite\Two\User` 인스턴스를 반환하지만, 이 경우에는 `token` 속성만이 채워집니다. 해당 토큰은 [인증된 사용자의 Slack 워크스페이스에 알림을 전송](/docs/12.x/notifications#notifying-external-slack-workspaces)하는 데 사용할 수 있습니다.

<a name="optional-parameters"></a>
### 선택적 파라미터 (Optional Parameters)

일부 OAuth 공급자는 리다이렉트 요청 시 다른 선택적 파라미터의 지원을 제공합니다. 요청에 선택적 파라미터를 포함하려면, 연관 배열을 `with` 메서드에 전달하세요.

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]
> `with` 메서드를 사용할 때, `state` 또는 `response_type`과 같은 예약어는 전달하지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
## 사용자 정보 가져오기 (Retrieving User Details)

사용자가 애플리케이션의 인증 콜백 라우트로 리다이렉트된 후, Socialite의 `user` 메서드를 이용해 사용자 정보를 받아올 수 있습니다. 이 메서드가 반환하는 사용자 객체는 다양한 속성과 메서드를 제공하며, 이 정보들을 데이터베이스에 저장할 때 사용할 수 있습니다.

OAuth 공급자가 OAuth 1.0인지 OAuth 2.0인지에 따라, 사용 가능한 속성과 메서드가 다를 수 있습니다.

```php
use Laravel\Socialite\Socialite;

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // OAuth 2.0 공급자용...
    $token = $user->token;
    $refreshToken = $user->refreshToken;
    $expiresIn = $user->expiresIn;

    // OAuth 1.0 공급자용...
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // 모든 공급자 공통...
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();
});
```

<a name="retrieving-user-details-from-a-token-oauth2"></a>
#### 토큰으로 사용자 정보 가져오기 (Retrieving User Details From a Token)

이미 사용자의 유효한 액세스 토큰이 있다면, Socialite의 `userFromToken` 메서드를 사용하여 해당 사용자의 정보를 불러올 수 있습니다.

```php
use Laravel\Socialite\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

iOS 애플리케이션을 통한 Facebook Limited Login을 사용하는 경우, Facebook이 액세스 토큰 대신 OIDC 토큰을 반환합니다. OIDC 토큰 역시 액세스 토큰과 마찬가지로 `userFromToken` 메서드에 전달하여 사용자 세부 정보를 조회할 수 있습니다.

<a name="stateless-authentication"></a>
#### 무상태 인증 (Stateless Authentication)

`stateless` 메서드는 세션 기반 상태 검증을 비활성화할 때 사용할 수 있습니다. 이 기능은 쿠키 기반 세션을 사용하지 않는 무상태 API에 소셜 인증 기능을 적용할 때 유용합니다.

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')->stateless()->user();
```