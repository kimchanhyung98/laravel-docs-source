# CSRF 방어 (CSRF Protection)

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [URI 제외하기](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개

크로스 사이트 요청 위조(Cross-site request forgery, CSRF)는 인증된 사용자를 가장하여 무단 명령을 수행하는 악의적인 공격 유형입니다. 다행히 Laravel은 애플리케이션을 [CSRF 공격](https://en.wikipedia.org/wiki/Cross-site_request_forgery)으로부터 쉽게 보호할 수 있는 기능을 제공합니다.

<a name="csrf-explanation"></a>
#### 취약점에 대한 설명

크로스 사이트 요청 위조가 익숙하지 않은 경우, 이 취약점이 어떻게 악용될 수 있는지 예를 들어 설명하겠습니다. 예를 들어, 애플리케이션에 인증된 사용자의 이메일 주소를 변경하기 위해 `POST` 요청을 받는 `/user/email` 경로가 있다고 가정합니다. 대부분 이 경로는 사용자가 새로 사용하고자 하는 이메일 주소를 담고 있는 `email` 입력 필드를 기대합니다.

CSRF 보호가 없다면, 악의적인 웹사이트가 사용자의 애플리케이션 `/user/email` 경로를 가리키는 HTML 폼을 만들어 악성 사용자의 이메일 주소를 제출하는 상황을 상상할 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

만약 악의적인 웹사이트가 페이지가 로드될 때 자동으로 폼을 제출한다면, 악성 사용자는 단지 애플리케이션 사용자를 속여 해당 웹사이트를 방문하게 하는 것만으로도, 사용자의 이메일 주소를 강제로 변경할 수 있습니다.

이 취약점을 방지하려면, 악의적인 애플리케이션이 접근할 수 없는 비밀 세션 값을 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청마다 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지

Laravel은 애플리케이션에서 관리하는 각 활성 [사용자 세션](/docs/12.x/session)에 대해 CSRF "토큰"을 자동으로 생성합니다. 이 토큰은 인증된 사용자가 실제로 요청을 보내는 사람인지 검증하는 데 사용됩니다. 토큰은 사용자 세션에 저장되고 세션이 재생성될 때마다 변경되므로, 악의적인 애플리케이션은 이를 알 수 없습니다.

현재 세션의 CSRF 토큰은 요청 세션을 통해 또는 `csrf_token` 헬퍼 함수를 사용해 얻을 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션 내에서 "POST", "PUT", "PATCH", "DELETE" 형식의 HTML 폼을 정의할 때마다, CSRF 보호 미들웨어가 요청을 검증할 수 있도록 반드시 숨겨진 CSRF `_token` 필드를 포함해야 합니다. 편의를 위해 `@csrf` Blade 지시자를 사용하여 숨겨진 토큰 입력 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- 다음과 동일합니다... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

기본적으로 `web` 미들웨어 그룹에 포함된 `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` [미들웨어](/docs/12.x/middleware)가 요청 입력 내 토큰과 세션에 저장된 토큰이 일치하는지 자동으로 검증합니다. 이 두 토큰이 일치하면, 인증된 사용자가 요청을 시작한 사람임을 알 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰과 SPA

Laravel을 API 백엔드로 사용하는 SPA를 구축하는 경우, API 인증 및 CSRF 취약점 방지에 관한 정보는 [Laravel Sanctum 문서](/docs/12.x/sanctum)를 참고하세요.

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외하기

가끔 CSRF 보호 대상에서 특정 URI들을 제외해야 할 때가 있습니다. 예를 들어, 결제 처리를 위해 [Stripe](https://stripe.com)를 사용하며 그들의 웹훅 시스템을 활용할 경우, Stripe에서 CSRF 토큰을 알 수 없으므로 해당 웹훅 처리 경로는 CSRF 보호에서 제외해야 합니다.

일반적으로, 이러한 종류의 경로는 `routes/web.php` 파일 내 Laravel이 모든 경로에 적용하는 `web` 미들웨어 그룹 외부에 두어야 합니다. 하지만, 특정 경로를 애플리케이션 `bootstrap/app.php` 파일의 `validateCsrfTokens` 메서드에 URI를 명시하여 제외할 수도 있습니다:

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
> 편의를 위해, [테스트 실행 시](/docs/12.x/testing) CSRF 미들웨어는 모든 경로에 대해 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

`Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` 미들웨어는 POST 파라미터로 토큰 외에도 기본적으로 `web` 미들웨어 그룹에 포함되어 `X-CSRF-TOKEN` 요청 헤더도 검사합니다. 예를 들어, HTML `meta` 태그에 토큰을 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그다음 jQuery 같은 라이브러리에 모든 요청 헤더에 토큰을 자동으로 추가하도록 설정할 수 있습니다. 이는 기존 자바스크립트 기술을 사용하는 AJAX 기반 애플리케이션에 간단하고 편리한 CSRF 방어를 제공합니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키로 저장하여 프레임워크가 생성하는 모든 응답에 포함시킵니다. 이 쿠키 값을 사용하여 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 개발자 편의를 위한 기능으로, Angular나 Axios와 같은 일부 자바스크립트 프레임워크 및 라이브러리는 동종 출처 요청 시 자동으로 `X-XSRF-TOKEN` 헤더에 쿠키 값을 포함시킵니다.

> [!NOTE]
> 기본적으로 `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있어 자동으로 `X-XSRF-TOKEN` 헤더를 전송합니다.