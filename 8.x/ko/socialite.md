# Laravel Socialite

- [소개](#introduction)
- [설치](#installation)
- [Socialite 업그레이드](#upgrading-socialite)
- [설정](#configuration)
- [인증](#authentication)
    - [라우팅](#routing)
    - [인증 및 저장](#authentication-and-storage)
    - [접근 권한 범위](#access-scopes)
    - [선택적 매개변수](#optional-parameters)
- [사용자 정보 조회](#retrieving-user-details)

<a name="introduction"></a>
## 소개 (Introduction)

일반적인 폼 기반 인증 외에도, Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 사용하여 OAuth 제공자와 간단하고 편리하게 인증할 수 있는 방법을 제공합니다. Socialite는 현재 Facebook, Twitter, LinkedIn, Google, GitHub, GitLab 및 Bitbucket에서 인증을 지원합니다.

> [!TIP]
> 다른 플랫폼용 어댑터는 커뮤니티 주도 사이트인 [Socialite Providers](https://socialiteproviders.com/)에서 확인할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

Socialite를 시작하려면, Composer 패키지 관리자를 사용하여 프로젝트의 의존성에 패키지를 추가하세요:

```
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## Socialite 업그레이드 (Upgrading Socialite)

Socialite의 메이저 버전을 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 꼼꼼히 검토하는 것이 중요합니다.

<a name="configuration"></a>
## 설정 (Configuration)

Socialite를 사용하기 전에, 애플리케이션에서 사용하는 OAuth 제공자의 자격 증명을 추가해야 합니다. 이 자격 증명은 애플리케이션의 `config/services.php` 설정 파일에 추가하며, 사용하는 제공자에 따라 `facebook`, `twitter`, `linkedin`, `google`, `github`, `gitlab`, 또는 `bitbucket` 키를 사용하세요:

```
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!TIP]
> `redirect` 옵션에 상대 경로가 포함된 경우, 자동으로 완전한 URL로 변환됩니다.

<a name="authentication"></a>
## 인증 (Authentication)

<a name="routing"></a>
### 라우팅 (Routing)

OAuth 제공자를 사용해 사용자를 인증하려면 두 개의 라우트가 필요합니다. 하나는 사용자를 OAuth 제공자 쪽으로 리디렉션하는 라우트이고, 다른 하나는 인증 후 제공자로부터 콜백을 받는 라우트입니다. 아래 예시 컨트롤러는 두 라우트 구현을 보여줍니다:

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

`Socialite` 파사드에서 제공하는 `redirect` 메서드는 사용자를 OAuth 제공자로 리디렉션하고, `user` 메서드는 인증 후 들어오는 요청을 읽어 사용자 정보를 제공합니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장 (Authentication & Storage)

OAuth 제공자에서 사용자를 받아오면, 해당 사용자가 애플리케이션 데이터베이스에 존재하는지 확인하고 [사용자를 인증](/docs/{{version}}/authentication#authenticate-a-user-instance)할 수 있습니다. 만약 존재하지 않는다면, 보통 새 사용자 레코드를 생성합니다:

```
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
```

> [!TIP]
> 특정 OAuth 제공자에서 어떤 사용자 정보가 제공되는지에 대한 자세한 내용은 [사용자 정보 조회](#retrieving-user-details) 문서를 참고하세요.

<a name="access-scopes"></a>
### 접근 권한 범위 (Access Scopes)

사용자를 리디렉션하기 전, 인증 요청에 추가적인 "스코프"를 `scopes` 메서드를 사용해 포함할 수 있습니다. 이 메서드는 기존 스코프와 전달한 스코프를 병합합니다:

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

`setScopes` 메서드를 사용하면 인증 요청의 모든 기존 스코프를 새롭게 지정한 스코프로 덮어쓸 수 있습니다:

```
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="optional-parameters"></a>
### 선택적 매개변수 (Optional Parameters)

일부 OAuth 제공자는 리디렉션 요청에 선택적 매개변수를 지원합니다. 요청에 선택적 매개변수를 포함하려면, 연관 배열을 전달하여 `with` 메서드를 호출하세요:

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!NOTE]
> `with` 메서드를 사용할 때는 `state`나 `response_type` 같은 예약어를 전달하지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
## 사용자 정보 조회 (Retrieving User Details)

사용자가 인증 콜백 라우트로 리디렉션 된 후, Socialite의 `user` 메서드를 이용해 사용자 세부 정보를 받을 수 있습니다. `user` 메서드가 반환하는 사용자 객체는 애플리케이션 데이터베이스에 저장할 수 있는 다양한 속성과 메서드를 제공합니다. 사용 중인 OAuth 제공자가 OAuth 1.0인지 OAuth 2.0인지에 따라 제공되는 속성과 메서드가 다를 수 있습니다:

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
#### 토큰으로 사용자 정보 조회 (OAuth2) (Retrieving User Details From A Token (OAuth2))

유효한 접근 토큰이 이미 있다면, Socialite의 `userFromToken` 메서드를 사용해 사용자의 정보를 조회할 수 있습니다:

```
use Laravel\Socialite\Facades\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

<a name="retrieving-user-details-from-a-token-and-secret-oauth1"></a>
#### 토큰과 시크릿으로 사용자 정보 조회 (OAuth1) (Retrieving User Details From A Token And Secret (OAuth1))

유효한 토큰과 시크릿을 이미 가지고 있다면, Socialite의 `userFromTokenAndSecret` 메서드를 사용해 사용자의 정보를 조회할 수 있습니다:

```
use Laravel\Socialite\Facades\Socialite;

$user = Socialite::driver('twitter')->userFromTokenAndSecret($token, $secret);
```

<a name="stateless-authentication"></a>
#### 상태 비저장 인증 (Stateless Authentication)

`stateless` 메서드는 세션 상태 검증을 비활성화할 때 사용합니다. API에서 소셜 인증을 추가할 때 유용합니다:

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')->stateless()->user();
```

> [!NOTE]
> 상태 비저장 인증은 OAuth 1.0을 사용하는 Twitter 드라이버에서는 제공되지 않습니다.