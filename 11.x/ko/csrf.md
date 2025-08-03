# CSRF 보호 (CSRF Protection)

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [URI 제외하기](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개

크로스 사이트 요청 위조(Cross-site request forgeries, CSRF)는 인증된 사용자를 가장하여 무단 명령을 실행하는 악의적인 공격 유형입니다. 다행히도 Laravel은 애플리케이션을 [크로스 사이트 요청 위조](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) 공격으로부터 쉽게 보호할 수 있도록 도와줍니다.

<a name="csrf-explanation"></a>
#### 취약점 설명

크로스 사이트 요청 위조가 익숙하지 않은 분들을 위해, 이 취약점이 어떻게 악용될 수 있는지 예를 들어 설명하겠습니다. 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `/user/email` 경로가 있고, 이 경로는 `POST` 요청을 받는다고 가정해 보겠습니다. 이 경로는 사용자가 새로 사용할 이메일 주소를 포함하는 `email` 입력 필드를 기대할 것입니다.

CSRF 보호가 없다면, 악의적인 웹사이트가 애플리케이션의 `/user/email` 경로를 가리키는 HTML 폼을 작성하고, 공격자의 이메일 주소를 제출할 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

만약 악의적인 웹사이트가 페이지 로드 시 폼을 자동으로 제출한다면, 단순히 애플리케이션의 사용자를 속여 그 웹사이트를 방문하게 하는 것만으로도 사용자의 이메일이 공격자의 이메일로 변경될 수 있습니다.

이 취약점을 방지하기 위해, 우리는 모든 들어오는 `POST`, `PUT`, `PATCH`, 또는 `DELETE` 요청에서 악의적인 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지

Laravel은 애플리케이션에서 관리하는 각 활성 [사용자 세션](/docs/11.x/session)에 대해 자동으로 CSRF "토큰"을 생성합니다. 이 토큰은 인증된 사용자가 실제로 애플리케이션에 요청을 보내는 사람인지 검증하는 데 사용됩니다. 이 토큰은 사용자의 세션에 저장되고 세션이 재생성될 때마다 변경되므로, 악의적인 애플리케이션은 이 토큰에 접근할 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션을 통해 또는 `csrf_token` 헬퍼 함수를 사용해 참조할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션 내에서 "POST", "PUT", "PATCH" 또는 "DELETE"용 HTML 폼을 정의할 때마다, CSRF 보호 미들웨어가 요청을 검증할 수 있도록 폼에 숨겨진 CSRF `_token` 필드를 반드시 포함해야 합니다. 편의를 위해 `@csrf` Blade 지시어를 사용해 숨겨진 토큰 입력 필드를 쉽게 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- 다음과 동등합니다... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

기본적으로 `web` 미들웨어 그룹에 포함된 `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` [미들웨어](/docs/11.x/middleware)는 요청 본문의 토큰이 세션에 저장된 토큰과 일치하는지 자동으로 확인합니다. 두 토큰이 일치하면 인증된 사용자가 요청을 시작한 것임을 알 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰과 SPA

Laravel을 API 백엔드로 사용하여 SPA(Single Page Application)를 개발하는 경우, API 인증과 CSRF 취약점 보호에 관한 자세한 내용은 [Laravel Sanctum 문서](/docs/11.x/sanctum)를 참고하시기 바랍니다.

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외하기

때로는 특정 URI들을 CSRF 보호 대상에서 제외해야 할 수도 있습니다. 예를 들어, 결제를 처리하기 위해 [Stripe](https://stripe.com)를 사용하고 Stripe의 웹훅 시스템을 활용하는 경우, Stripe는 CSRF 토큰을 보내지 않기 때문에 Stripe 웹훅 핸들러 경로를 CSRF 보호 대상에서 제외해야 합니다.

보통 이런 경로들은 `routes/web.php` 파일 내 `web` 미들웨어 그룹에서 제외된 별도의 라우트 파일이나 그룹에 배치하는 것이 좋습니다. 그러나 애플리케이션의 `bootstrap/app.php` 파일 내의 `validateCsrfTokens` 메서드에 예외 URI를 지정해 특정 경로만 제외할 수도 있습니다:

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: [
        'stripe/*',
        'http://example.com/foo/bar',
        'http://example.com/foo/*',
    ]);
})
```

> [!NOTE]  
> 테스트 실행 시 [CSRF 미들웨어는 자동으로 비활성화](/docs/11.x/testing)되어 편리합니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

`Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` 미들웨어는 기본적으로 `web` 미들웨어 그룹에 포함되어 있으며, CSRF 토큰이 POST 파라미터로 전달되는 것 외에도 `X-CSRF-TOKEN` 요청 헤더도 검사합니다. 예를 들어 토큰을 HTML `meta` 태그에 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그 다음 jQuery 같은 라이브러리에게 모든 요청 헤더에 이 토큰을 자동으로 추가하도록 지시할 수 있습니다. 이것은 이전 JavaScript 기술을 사용하는 AJAX 기반 애플리케이션에 간단하고 편리한 CSRF 보호를 제공합니다:

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

이 쿠키는 개발자 편의를 위해 주로 사용되며, Angular나 Axios 같은 일부 JavaScript 프레임워크 및 라이브러리가 동일 출처 요청에 대해 자동으로 이 쿠키 값을 `X-XSRF-TOKEN` 헤더에 넣습니다.

> [!NOTE]  
> 기본적으로 `resources/js/bootstrap.js` 파일에 포함된 Axios HTTP 라이브러리는 `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.