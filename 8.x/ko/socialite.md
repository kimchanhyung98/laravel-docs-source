# Laravel Socialite

- [소개](#introduction)
- [설치](#installation)
- [Socialite 업그레이드](#upgrading-socialite)
- [환경 설정](#configuration)
- [인증](#authentication)
    - [라우팅](#routing)
    - [인증 및 저장](#authentication-and-storage)
    - [액세스 범위(Scopes)](#access-scopes)
    - [옵션 파라미터](#optional-parameters)
- [사용자 정보 조회](#retrieving-user-details)

<a name="introduction"></a>
## 소개

일반적인 폼 기반 인증 외에도, Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 사용하여 OAuth 제공자와 간편하게 인증할 수 있는 직관적인 방법을 제공합니다. Socialite는 현재 Facebook, Twitter, LinkedIn, Google, GitHub, GitLab, Bitbucket 인증을 지원합니다.

> {tip} 다른 플랫폼용 어댑터는 커뮤니티에서 운영되는 [Socialite Providers](https://socialiteproviders.com/) 웹사이트에서 확인할 수 있습니다.

<a name="installation"></a>
## 설치

Socialite를 시작하려면 Composer 패키지 관리자를 사용하여 패키지를 프로젝트의 의존성에 추가하세요:

    composer require laravel/socialite

<a name="upgrading-socialite"></a>
## Socialite 업그레이드

Socialite의 새로운 주요 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 꼼꼼히 확인하는 것이 중요합니다.

<a name="configuration"></a>
## 환경 설정

Socialite를 사용하기 전에, 애플리케이션에서 사용할 OAuth 제공자 자격 증명을 추가해야 합니다. 이 자격 증명은 애플리케이션의 `config/services.php` 환경설정 파일에 추가해야 하며, 애플리케이션에서 필요한 제공자에 따라 `facebook`, `twitter`, `linkedin`, `google`, `github`, `gitlab`, `bitbucket` 중 하나의 키를 사용해야 합니다:

    'github' => [
        'client_id' => env('GITHUB_CLIENT_ID'),
        'client_secret' => env('GITHUB_CLIENT_SECRET'),
        'redirect' => 'http://example.com/callback-url',
    ],

> {tip} `redirect` 옵션에 상대 경로가 지정된 경우, 자동으로 전체 URL로 변환됩니다.

<a name="authentication"></a>
## 인증

<a name="routing"></a>
### 라우팅

OAuth 제공자를 사용하여 사용자를 인증하려면 두 개의 라우트가 필요합니다: 사용자를 OAuth 제공자로 리디렉션하는 라우트와, 인증 후 제공자로부터 콜백을 수신하는 라우트입니다. 아래의 컨트롤러 예시에서 두 라우트의 구현 방법을 보여줍니다:

    use Laravel\Socialite\Facades\Socialite;

    Route::get('/auth/redirect', function () {
        return Socialite::driver('github')->redirect();
    });

    Route::get('/auth/callback', function () {
        $user = Socialite::driver('github')->user();

        // $user->token
    });

`Socialite` 파사드에서 제공하는 `redirect` 메서드는 사용자를 OAuth 제공자로 리디렉션해주고, `user` 메서드는 인증 후 제공자로부터의 응답을 읽어서 사용자 정보를 조회합니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장

OAuth 제공자로부터 사용자를 조회한 후, 해당 사용자가 애플리케이션 데이터베이스에 존재하는지 확인하고 [사용자를 인증](/docs/{{version}}/authentication#authenticate-a-user-instance)할 수 있습니다. 데이터베이스에 사용자가 없으면 일반적으로 새 사용자를 생성합니다:

    use App\Models\User;
    use Illuminate\Support\Facades\Auth;
    use Laravel\Socialite\Facades\Socialite;

    Route::get('/auth/callback', function () {
        $githubUser = Socialite::driver('github')->user();

        $user = User::where('github_id', $githubUser->id)->first();

        if ($user) {
            $user->update([
                'github_token' => $githubUser->token,
                'github_refresh_token' => $githubUser->refreshToken,
            ]);
        } else {
            $user = User::create([
                'name' => $githubUser->name,
                'email' => $githubUser->email,
                'github_id' => $githubUser->id,
                'github_token' => $githubUser->token,
                'github_refresh_token' => $githubUser->refreshToken,
            ]);
        }

        Auth::login($user);

        return redirect('/dashboard');
    });

> {tip} 특정 OAuth 제공자로부터 얻을 수 있는 사용자 정보에 대해 더 알고 싶다면, [사용자 정보 조회](#retrieving-user-details) 문서를 참고하세요.

<a name="access-scopes"></a>
### 액세스 범위(Scopes)

사용자를 리디렉션하기 전에, `scopes` 메서드를 사용하여 인증 요청에 추가적인 "스코프"를 설정할 수 있습니다. 이 메서드는 기존 스코프와 새로 지정한 스코프를 병합합니다:

    use Laravel\Socialite\Facades\Socialite;

    return Socialite::driver('github')
        ->scopes(['read:user', 'public_repo'])
        ->redirect();

`setScopes` 메서드를 사용하면 기존 스코프를 모두 덮어쓸 수 있습니다:

    return Socialite::driver('github')
        ->setScopes(['read:user', 'public_repo'])
        ->redirect();

<a name="optional-parameters"></a>
### 옵션 파라미터

다양한 OAuth 제공자는 리디렉션 요청에 옵션 파라미터를 지원합니다. 옵션 파라미터를 포함하려면, 연관 배열을 `with` 메서드에 전달하세요:

    use Laravel\Socialite\Facades\Socialite;

    return Socialite::driver('google')
        ->with(['hd' => 'example.com'])
        ->redirect();

> {note} `with` 메서드를 사용할 때는 `state`나 `response_type`과 같은 예약어를 전달하지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
## 사용자 정보 조회

사용자가 인증 콜백 라우트로 다시 리디렉션된 후, Socialite의 `user` 메서드를 사용하여 사용자 정보를 조회할 수 있습니다. `user` 메서드에서 반환된 사용자 객체는 사용자를 데이터베이스에 저장할 때 사용할 수 있는 다양한 속성과 메서드를 제공합니다. 인증하려는 OAuth 제공자가 OAuth 1.0 또는 OAuth 2.0을 지원하는지에 따라 사용 가능한 속성 및 메서드가 다를 수 있습니다:

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
#### 토큰에서 사용자 정보 조회 (OAuth2)

이미 사용자의 유효한 액세스 토큰을 가지고 있다면, Socialite의 `userFromToken` 메서드를 사용해 정보를 조회할 수 있습니다:

    use Laravel\Socialite\Facades\Socialite;

    $user = Socialite::driver('github')->userFromToken($token);

<a name="retrieving-user-details-from-a-token-and-secret-oauth1"></a>
#### 토큰 및 시크릿에서 사용자 정보 조회 (OAuth1)

이미 사용자의 유효한 토큰과 시크릿을 가지고 있다면, Socialite의 `userFromTokenAndSecret` 메서드를 사용하여 정보를 조회할 수 있습니다:

    use Laravel\Socialite\Facades\Socialite;

    $user = Socialite::driver('twitter')->userFromTokenAndSecret($token, $secret);

<a name="stateless-authentication"></a>
#### 상태 비저장(stateless) 인증

`stateless` 메서드를 사용하여 세션 상태 확인을 비활성화할 수 있습니다. 이것은 API에 소셜 인증을 추가할 때 유용합니다:

    use Laravel\Socialite\Facades\Socialite;

    return Socialite::driver('google')->stateless()->user();

> {note} 상태 비저장 인증은 OAuth 1.0을 사용하는 Twitter 드라이버에서는 지원되지 않습니다.