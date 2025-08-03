# CSRF 보호 (CSRF Protection)

- [소개](#csrf-introduction)
- [CSRF 요청 차단하기](#preventing-csrf-requests)
    - [URI 예외 처리](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개

크로스사이트 요청 위조(cross-site request forgery, CSRF)는 인증된 사용자를 가장하여 권한 없이 명령을 수행하는 악의적인 공격 유형입니다. 다행히도 Laravel은 애플리케이션을 [CSRF 공격](https://en.wikipedia.org/wiki/Cross-site_request_forgery)으로부터 쉽게 보호할 수 있도록 기능을 제공합니다.

<a name="csrf-explanation"></a>
#### 취약점 설명

CSRF 공격에 익숙하지 않은 분들을 위해, 이 취약점이 어떻게 악용될 수 있는지 예시를 들어 설명하겠습니다. 애플리케이션에 `/user/email` 경로가 있고, `POST` 요청으로 인증된 사용자의 이메일 주소를 변경한다고 가정해 보겠습니다. 일반적으로 이 경로는 사용자가 새로 변경하고자 하는 이메일 주소를 담은 `email` 입력 필드를 기대할 것입니다.

만약 CSRF 보호가 없다면, 악의적인 웹사이트가 다음과 같은 HTML 폼을 만들어 애플리케이션의 `/user/email` 경로로 악성 사용자의 이메일 주소를 전송할 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

악의적 웹사이트에서 페이지가 로드될 때 자동으로 이 폼을 전송하면, 해당 악의적 사용자는 애플리케이션 사용자를 속여 자신의 사이트에 방문하게 만들기만 하면, 사용자의 이메일 주소가 해당 악성 이메일 주소로 변경됩니다.

이러한 취약점을 막기 위해서는, 들어오는 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해 악성 애플리케이션이 알 수 없는 비밀 세션 값이 있는지 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 차단하기

Laravel은 애플리케이션에서 관리하는 각 활성 [사용자 세션](/docs/master/session)에 대해 자동으로 CSRF "토큰"을 생성합니다. 이 토큰은 인증된 사용자가 실제로 요청을 수행하는 사람임을 확인하는 데 사용됩니다. 사용자의 세션에 저장되고 세션이 새로 고침될 때마다 토큰이 변경되기 때문에, 악의적인 애플리케이션은 이 값을 알 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션을 통해 접근하거나 `csrf_token` 헬퍼 함수를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션에서 "POST", "PUT", "PATCH", "DELETE" HTML 폼을 정의할 때는 반드시 CSRF 보호 미들웨어가 요청을 검증할 수 있도록 폼 안에 숨겨진 CSRF `_token` 필드를 포함해야 합니다. 이를 위해 `@csrf` Blade 디렉티브를 이용해 쉽게 숨겨진 토큰 입력 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- 다음과 동일합니다... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

기본적으로 `web` 미들웨어 그룹에 포함된 `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` [미들웨어](/docs/master/middleware)는 요청 입력의 토큰이 세션에 저장된 토큰과 일치하는지 자동으로 확인합니다. 두 토큰이 일치할 경우, 인증된 사용자 본인이 요청을 보낸 것임을 알 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰과 SPA

Laravel을 API 백엔드로 사용하는 SPA(Single Page Application)를 구축하는 경우, API 인증과 CSRF 취약점 방어를 위해 [Laravel Sanctum 문서](/docs/master/sanctum)를 참고하세요.

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외하기

가끔 특정 URI들을 CSRF 보호 대상에서 제외해야 할 때가 있습니다. 예를 들어, [Stripe](https://stripe.com)로 결제를 처리하면서 웹훅 시스템을 사용하는 경우, Stripe가 CSRF 토큰을 보내지 않기 때문에 Stripe 웹훅 핸들러 경로를 CSRF 보호 대상에서 빼야 합니다.

보통 이런 경로들은 `routes/web.php` 파일 내 `web` 미들웨어 그룹 밖에 두는 것이 권장됩니다. 하지만 애플리케이션의 `bootstrap/app.php` 파일에서 `validateCsrfTokens` 메서드에 URI를 지정하여 특정 경로를 제외할 수도 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'stripe/*',
        'http://example.com/foo/bar',
        'http://example.com/foo/*',
    ]);
})
```

> [!NOTE]
> 편의를 위해, [테스트](/docs/master/testing) 실행 시 CSRF 미들웨어는 모든 경로에 대해 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

`web` 미들웨어 그룹에 기본 포함된 `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` 미들웨어는 POST 파라미터의 CSRF 토큰뿐만 아니라 `X-CSRF-TOKEN` 요청 헤더도 검사합니다. 예를 들어, HTML `meta` 태그에 토큰을 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그런 다음 jQuery 같은 라이브러리에 모든 요청 헤더에 자동으로 토큰을 추가하도록 설정할 수 있습니다. 이 방법은 전통적인 JavaScript 기반 AJAX 애플리케이션에 간편한 CSRF 보호를 제공합니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장하여 프레임워크가 생성하는 모든 응답에 포함시킵니다. 이 쿠키 값을 사용해 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 주로 개발자 편의용으로, Angular나 Axios 같은 일부 JavaScript 프레임워크와 라이브러리는 동일 출처(same-origin) 요청에 대해 자동으로 쿠키 값을 `X-XSRF-TOKEN` 헤더에 포함시킵니다.

> [!NOTE]
> 기본적으로 `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있어 `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.