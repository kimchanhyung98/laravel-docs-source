# Laravel Socialite

- [소개](#introduction)
- [설치](#installation)
- [Socialite 업그레이드](#upgrading-socialite)
- [설정](#configuration)
- [인증](#authentication)
    - [라우팅](#routing)
    - [인증 및 저장](#authentication-and-storage)
    - [액세스 범위](#access-scopes)
    - [옵션 파라미터](#optional-parameters)
- [사용자 정보 조회](#retrieving-user-details)

<a name="introduction"></a>
## 소개

일반적인 폼 기반 인증 외에도, Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 사용하여 OAuth 제공자를 통한 간편하고 편리한 인증 방식을 제공합니다. Socialite는 현재 Facebook, Twitter, LinkedIn, Google, GitHub, GitLab, Bitbucket을 통한 인증을 지원합니다.

> **참고**  
> 기타 플랫폼에 대한 어댑터는 커뮤니티가 운영하는 [Socialite Providers](https://socialiteproviders.com/) 사이트에서 제공합니다.

<a name="installation"></a>
## 설치

Socialite를 시작하려면 Composer 패키지 관리자를 사용하여 패키지를 프로젝트의 의존성에 추가하세요:

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## Socialite 업그레이드

Socialite의 새로운 주요 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 꼼꼼히 검토하는 것이 중요합니다.

<a name="configuration"></a>
## 설정

Socialite를 사용하기 전에 애플리케이션에서 활용할 OAuth 제공자에 대한 자격 증명을 추가해야 합니다. 일반적으로 이러한 자격 증명은 인증할 서비스의 대시보드에서 "개발자 애플리케이션"을 생성하여 얻을 수 있습니다.

이 자격 증명은 애플리케이션의 `config/services.php` 설정 파일에 위치해야 하며, 사용하는 제공자에 따라 `facebook`, `twitter` (OAuth 1.0), `twitter-oauth-2` (OAuth 2.0), `linkedin`, `google`, `github`, `gitlab`, 또는 `bitbucket` 키를 사용해야 합니다:

    'github' => [
        'client_id' => env('GITHUB_CLIENT_ID'),
        'client_secret' => env('GITHUB_CLIENT_SECRET'),
        'redirect' => 'http://example.com/callback-url',
    ],

> **참고**  
> `redirect` 옵션에 상대 경로가 입력된 경우, 자동으로 전체 URL로 변환됩니다.

<a name="authentication"></a>
## 인증

<a name="routing"></a>
### 라우팅

OAuth 제공자를 사용하여 사용자를 인증하려면 두 개의 라우트가 필요합니다. 하나는 사용자를 OAuth 제공자로 리디렉션하는 것이고, 다른 하나는 인증 후 제공자로부터 콜백을 받는 라우트입니다. 아래 예제는 두 라우트의 구현을 보여줍니다:

    use Laravel\Socialite\Facades\Socialite;

    Route::get('/auth/redirect', function () {
        return Socialite::driver('github')->redirect();
    });

    Route::get('/auth/callback', function () {
        $user = Socialite::driver('github')->user();

        // $user->token
    });

`Socialite` 파사드가 제공하는 `redirect` 메서드는 사용자를 OAuth 제공자로 리디렉션하는 역할을 하며, `user` 메서드는 인증 요청 승인 후 들어오는 요청을 검사하고 제공자로부터 사용자 정보를 가져옵니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장

OAuth 제공자로부터 사용자를 가져온 후, 해당 사용자가 애플리케이션의 데이터베이스에 존재하는지 판단하여 [사용자를 인증](/docs/{{version}}/authentication#authenticate-a-user-instance)할 수 있습니다. 데이터베이스에 사용자가 존재하지 않는 경우, 일반적으로 새로운 사용자 레코드를 생성합니다:

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

> **참고**  
> 특정 OAuth 제공자로부터 어떤 사용자 정보가 제공되는지에 관해서는 [사용자 정보 조회](#retrieving-user-details) 문서를 참고하세요.

<a name="access-scopes"></a>
### 액세스 범위

사용자를 리디렉션하기 전에, `scopes` 메서드를 사용하여 인증 요청에 포함할 "스코프"를 지정할 수 있습니다. 이 메서드는 이전에 지정한 모든 스코프에 지정한 스코프를 병합합니다:

    use Laravel\Socialite\Facades\Socialite;

    return Socialite::driver('github')
        ->scopes(['read:user', 'public_repo'])
        ->redirect();

`setScopes` 메서드를 사용하면 인증 요청에 포함된 기존 모든 스코프를 덮어쓸 수 있습니다:

    return Socialite::driver('github')
        ->setScopes(['read:user', 'public_repo'])
        ->redirect();

<a name="optional-parameters"></a>
### 옵션 파라미터

여러 OAuth 제공자는 리디렉션 요청에 다른 옵션 파라미터를 지원합니다. 요청에 옵션 파라미터를 포함하려면, 연관 배열을 `with` 메서드에 전달하세요:

    use Laravel\Socialite\Facades\Socialite;

    return Socialite::driver('google')
        ->with(['hd' => 'example.com'])
        ->redirect();

> **경고**  
> `with` 메서드를 사용할 때는 `state`나 `response_type`과 같은 예약어를 전달하지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
## 사용자 정보 조회

사용자가 애플리케이션의 인증 콜백 라우트로 리디렉션된 이후에는, Socialite의 `user` 메서드를 사용하여 사용자 정보를 가져올 수 있습니다. `user` 메서드가 반환하는 사용자 객체는 다양한 속성과 메서드를 제공하므로, 이를 활용해 데이터베이스에 사용자 정보를 저장할 수 있습니다.

인증에 사용한 OAuth 제공자가 OAuth 1.0 또는 OAuth 2.0을 지원하는지에 따라 이 객체에서 사용할 수 있는 속성과 메서드가 다를 수 있습니다:

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
#### 토큰으로 사용자 정보 조회 (OAuth2)

이미 사용자의 유효한 액세스 토큰이 있는 경우, Socialite의 `userFromToken` 메서드를 사용해 해당 사용자의 정보를 가져올 수 있습니다:

    use Laravel\Socialite\Facades\Socialite;

    $user = Socialite::driver('github')->userFromToken($token);

<a name="retrieving-user-details-from-a-token-and-secret-oauth1"></a>
#### 토큰과 시크릿으로 사용자 정보 조회 (OAuth1)

이미 사용자의 유효한 토큰과 시크릿이 있다면, Socialite의 `userFromTokenAndSecret` 메서드를 사용하여 정보를 조회할 수 있습니다:

    use Laravel\Socialite\Facades\Socialite;

    $user = Socialite::driver('twitter')->userFromTokenAndSecret($token, $secret);

<a name="stateless-authentication"></a>
#### 상태 비저장(Stateless) 인증

`stateless` 메서드는 세션 상태 검증을 비활성화하는 데 사용할 수 있습니다. 쿠키 기반 세션을 사용하지 않는 상태 비저장 API에 소셜 인증을 추가할 때 유용합니다:

    use Laravel\Socialite\Facades\Socialite;

    return Socialite::driver('google')->stateless()->user();

> **경고**  
> 상태 비저장 인증은 Twitter OAuth 1.0 드라이버에서는 사용할 수 없습니다.
