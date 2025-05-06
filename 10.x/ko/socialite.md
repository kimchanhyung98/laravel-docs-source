# Laravel Socialite

- [소개](#introduction)
- [설치](#installation)
- [Socialite 업그레이드](#upgrading-socialite)
- [설정](#configuration)
- [인증](#authentication)
    - [라우팅](#routing)
    - [인증 및 저장](#authentication-and-storage)
    - [접근 범위(스코프)](#access-scopes)
    - [Slack 봇 스코프](#slack-bot-scopes)
    - [옵션 파라미터](#optional-parameters)
- [유저 정보 가져오기](#retrieving-user-details)

<a name="introduction"></a>
## 소개

Laravel은 일반적인 폼 기반 인증 외에도, [Laravel Socialite](https://github.com/laravel/socialite)를 사용하여 OAuth 제공자와의 인증을 간단하고 편리하게 제공합니다. Socialite는 현재 Facebook, Twitter, LinkedIn, Google, GitHub, GitLab, Bitbucket, Slack을 통한 인증을 지원합니다.

> [!NOTE]  
> 기타 플랫폼에 대한 어댑터는 커뮤니티 주도로 운영되는 [Socialite Providers](https://socialiteproviders.com/) 사이트에서 확인하실 수 있습니다.

<a name="installation"></a>
## 설치

Socialite를 시작하려면, Composer 패키지 관리자를 사용하여 프로젝트 의존성에 패키지를 추가하세요:

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## Socialite 업그레이드

Socialite의 새로운 주요 버전으로 업그레이드할 경우, 반드시 [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 꼼꼼하게 검토하시기 바랍니다.

<a name="configuration"></a>
## 설정

Socialite를 사용하기 전에, 애플리케이션에서 사용하는 OAuth 제공자에 대한 자격 증명을 추가해야 합니다. 일반적으로 이러한 자격 증명은 인증하고자 하는 서비스의 대시보드에서 "개발자 애플리케이션"을 생성하여 얻을 수 있습니다.

이 자격 증명 정보는 애플리케이션의 `config/services.php` 설정 파일에 위치해야 하며, 사용하고자 하는 제공자에 따라 `facebook`, `twitter`(OAuth 1.0), `twitter-oauth-2`(OAuth 2.0), `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack` 키를 사용합니다:

    'github' => [
        'client_id' => env('GITHUB_CLIENT_ID'),
        'client_secret' => env('GITHUB_CLIENT_SECRET'),
        'redirect' => 'http://example.com/callback-url',
    ],

> [!NOTE]  
> `redirect` 옵션에 상대 경로가 포함되어 있다면, 자동으로 전체 URL로 변환됩니다.

<a name="authentication"></a>
## 인증

<a name="routing"></a>
### 라우팅

OAuth 제공자를 사용하여 사용자를 인증하려면 두 개의 라우트가 필요합니다: 하나는 사용자를 OAuth 제공자로 리디렉션하는 라우트이고, 다른 하나는 인증 후 제공자로부터 콜백을 받는 라우트입니다. 아래 예시는 두 라우트의 구현을 보여줍니다:

    use Laravel\Socialite\Facades\Socialite;

    Route::get('/auth/redirect', function () {
        return Socialite::driver('github')->redirect();
    });

    Route::get('/auth/callback', function () {
        $user = Socialite::driver('github')->user();

        // $user->token
    });

`Socialite` 퍼사드의 `redirect` 메소드는 사용자를 OAuth 제공자로 리디렉션해주며, `user` 메소드는 콜백 요청을 받아 사용자가 인증을 승인한 후 제공자로부터 사용자 정보를 가져옵니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장

OAuth 제공자로부터 사용자를 가져온 후, 해당 사용자가 애플리케이션의 데이터베이스에 존재하는지 판단하고, [사용자를 인증](/docs/{{version}}/authentication#authenticate-a-user-instance)할 수 있습니다. 데이터베이스에 사용자가 없을 경우, 일반적으로 신규로 사용자를 생성하여 저장합니다:

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

> [!NOTE]  
> 각 OAuth 제공자에서 제공하는 유저 정보에 대한 자세한 내용은 [유저 정보 가져오기](#retrieving-user-details) 문서를 참고하세요.

<a name="access-scopes"></a>
### 접근 범위(스코프)

사용자를 리디렉션하기 전에, `scopes` 메소드를 사용하여 인증 요청에 포함되어야 할 "스코프"를 지정할 수 있습니다. 이 메소드는 이전에 지정된 스코프와 새로 추가하는 스코프를 병합합니다:

    use Laravel\Socialite\Facades\Socialite;

    return Socialite::driver('github')
        ->scopes(['read:user', 'public_repo'])
        ->redirect();

`setScopes` 메소드를 사용하면 기존의 모든 스코프를 덮어쓸 수 있습니다:

    return Socialite::driver('github')
        ->setScopes(['read:user', 'public_repo'])
        ->redirect();

<a name="slack-bot-scopes"></a>
### Slack 봇 스코프

Slack의 API는 각기 다른 [액세스 토큰 타입](https://api.slack.com/authentication/token-types)과 해당 [권한 스코프](https://api.slack.com/scopes)를 제공합니다. Socialite는 다음 두 가지 Slack 액세스 토큰 타입과 호환됩니다:

<div class="content-list" markdown="1">

- 봇(Bot) (접두어: `xoxb-`)
- 사용자(User) (접두어: `xoxp-`)

</div>

기본적으로, `slack` 드라이버는 `user` 토큰을 생성하며, 드라이버의 `user` 메소드를 호출하면 사용자의 상세 정보를 반환합니다.

봇 토큰은 애플리케이션이 외부 Slack 워크스페이스(해당 애플리케이션의 사용자가 소유)를 대상으로 알림을 전송해야 하는 경우에 주로 사용됩니다. 봇 토큰을 생성하려면, 사용자를 Slack 인증 화면으로 리디렉션하기 전에 `asBotUser` 메소드를 호출하세요:

    return Socialite::driver('slack')
        ->asBotUser()
        ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
        ->redirect();

또한, 인증 후 Slack이 사용자를 애플리케이션으로 다시 리디렉션할 때, `user` 메소드를 호출하기 전에 반드시 `asBotUser` 메소드를 호출해야 합니다:

    $user = Socialite::driver('slack')->asBotUser()->user();

봇 토큰을 생성해도 `user` 메소드는 여전히 `Laravel\Socialite\Two\User` 인스턴스를 반환하지만, 이때는 `token` 속성만이 할당됩니다. 이 토큰을 저장하여 [인증된 사용자의 Slack 워크스페이스에 알림을 전송](/docs/{{version}}/notifications#notifying-external-slack-workspaces)할 수 있습니다.

<a name="optional-parameters"></a>
### 옵션 파라미터

일부 OAuth 제공자는, 리디렉트 요청 시 추가 파라미터를 지원합니다. 옵션 파라미터를 추가하려면, `with` 메소드에 연관 배열을 전달하세요:

    use Laravel\Socialite\Facades\Socialite;

    return Socialite::driver('google')
        ->with(['hd' => 'example.com'])
        ->redirect();

> [!WARNING]  
> `with` 메소드 사용 시, `state` 또는 `response_type`과 같은 예약어를 전달하지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
## 유저 정보 가져오기

사용자가 애플리케이션의 인증 콜백 라우트로 리디렉션되면, Socialite의 `user` 메소드를 통해 사용자 정보를 가져올 수 있습니다. `user` 메소드가 반환하는 사용자 객체는 데이터베이스에 사용자 정보를 저장하는 데 활용할 수 있는 다양한 속성과 메소드를 제공합니다.

OAuth 제공자가 OAuth 1.0 또는 OAuth 2.0을 지원하는지에 따라 사용 가능한 속성과 메소드가 다를 수 있습니다:

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

<a name="retrieving-user-details-from-a-token-oauth2"></a>
#### 토큰으로 유저 정보 가져오기 (OAuth2)

이미 사용자의 유효한 액세스 토큰이 있다면, Socialite의 `userFromToken` 메소드로 사용자 정보를 가져올 수 있습니다:

    use Laravel\Socialite\Facades\Socialite;

    $user = Socialite::driver('github')->userFromToken($token);

<a name="retrieving-user-details-from-a-token-and-secret-oauth1"></a>
#### 토큰과 시크릿으로 유저 정보 가져오기 (OAuth1)

이미 사용자의 유효한 토큰과 시크릿이 있다면, Socialite의 `userFromTokenAndSecret` 메소드로 사용자 정보를 가져올 수 있습니다:

    use Laravel\Socialite\Facades\Socialite;

    $user = Socialite::driver('twitter')->userFromTokenAndSecret($token, $secret);

<a name="stateless-authentication"></a>
#### 상태 비저장(stateless) 인증

`stateless` 메소드를 사용하면 세션 상태 검증을 비활성화할 수 있습니다. 쿠키 기반 세션을 사용하지 않는 stateless API에 소셜 인증을 추가할 때 유용합니다:

    use Laravel\Socialite\Facades\Socialite;

    return Socialite::driver('google')->stateless()->user();

> [!WARNING]  
> Twitter OAuth 1.0 드라이버에서는 상태 비저장 인증을 사용할 수 없습니다.