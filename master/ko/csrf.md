# CSRF 보호

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [URI 제외하기](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개

사이트 간 요청 위조(CSRF, Cross-site request forgeries)는 인증된 사용자를 대신해 무단 명령이 실행되는 악의적인 공격 유형입니다. 다행히도, Laravel은 [사이트 간 요청 위조](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) 공격으로부터 애플리케이션을 쉽게 보호할 수 있도록 지원합니다.

<a name="csrf-explanation"></a>
#### 취약점 설명

사이트 간 요청 위조(CSRF)에 익숙하지 않은 경우, 이 취약점이 어떻게 악용될 수 있는지 예시를 통해 살펴보겠습니다. 예를 들어, 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `POST` 요청을 받는 `/user/email` 라우트가 있다고 가정해 보십시오. 이 라우트는 일반적으로 사용자가 사용하고자 하는 이메일 주소를 담는 `email` 입력 필드를 기대할 것입니다.

CSRF 보호 장치가 없을 경우, 악의적인 웹사이트는 해당 애플리케이션의 `/user/email` 경로를 대상으로 하여 자신의 이메일 주소를 제출하는 HTML 폼을 만들 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

악의적인 사이트가 페이지가 로드될 때 자동으로 폼을 제출하도록 만들면, 공격자는 애플리케이션 사용자가 이 사이트를 방문하도록 유도하기만 하면 자신의 이메일 주소가 해당 애플리케이션에서 변경됩니다.

이 취약점을 방지하려면, 들어오는 모든 `POST`, `PUT`, `PATCH`, 또는 `DELETE` 요청에 대해 악의적인 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지

Laravel은 애플리케이션이 관리하는 각 활성 [사용자 세션](/docs/{{version}}/session)마다 자동으로 CSRF "토큰"을 생성합니다. 이 토큰은 인증된 사용자가 실제로 애플리케이션에 요청을 보내는 사용자인지 확인하는 데 사용됩니다. 이 토큰은 사용자 세션에 저장되고 세션이 갱신될 때마다 변경되므로, 악의적인 애플리케이션이 이를 알 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션이나 `csrf_token` 헬퍼 함수를 통해 접근할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션에서 "POST", "PUT", "PATCH", 또는 "DELETE" HTML 폼을 정의할 때는 항상 숨겨진 CSRF `_token` 필드를 폼에 포함시켜야 하며, CSRF 보호 미들웨어가 요청을 검증할 수 있도록 해야 합니다. 편의를 위해, `@csrf` Blade 지시어로 숨겨진 토큰 입력 필드를 쉽게 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- 아래와 동일합니다... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

`Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` [미들웨어](/docs/{{version}}/middleware)는 기본적으로 `web` 미들웨어 그룹에 포함되어 있으며, 요청 입력에 있는 토큰과 세션에 저장된 토큰이 일치하는지 자동으로 검사합니다. 이 두 토큰이 일치하면, 인증된 사용자가 이 요청을 보낸 것임을 확신할 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰 & SPA

만약 Laravel을 API 백엔드로 사용하는 SPA(싱글 페이지 애플리케이션)를 구축한다면, API 인증 및 CSRF 취약점 방지에 관한 자세한 내용은 [Laravel Sanctum 문서](/docs/{{version}}/sanctum)를 참고하세요.

<a name="csrf-excluding-uris"></a>
### URI를 CSRF 보호에서 제외하기

때로는 일부 URI를 CSRF 보호 대상에서 제외하고 싶을 수 있습니다. 예를 들어, [Stripe](https://stripe.com)로 결제를 처리하고 웹훅 시스템을 사용할 경우, Stripe는 어떤 CSRF 토큰을 전송해야 하는지 알지 못하므로 Stripe 웹훅 처리 라우트를 CSRF 보호 대상에서 제외해야 합니다.

일반적으로 이러한 라우트는 Laravel이 모든 라우트에 적용하는 `routes/web.php`의 `web` 미들웨어 그룹 밖에 배치하는 것이 좋습니다. 하지만 필요하다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `validateCsrfTokens` 메서드에 제외할 URI를 지정해 특정 라우트만 제외할 수 있습니다:

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
> 편의를 위해, [테스트 실행 시](/docs/{{version}}/testing)에는 모든 라우트에 대해 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

POST 파라미터로 CSRF 토큰을 확인하는 것 외에도, `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` 미들웨어(기본적으로 `web` 미들웨어 그룹에 포함됨)는 `X-CSRF-TOKEN` 요청 헤더도 검사합니다. 예를 들어, HTML의 `meta` 태그에 토큰을 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

이제 jQuery와 같은 라이브러리에 토큰이 모든 요청 헤더에 자동으로 추가되도록 지시할 수 있습니다. 이렇게 하면, 레거시 JavaScript를 사용하는 AJAX 기반 애플리케이션에서도 간편하게 CSRF 보호를 구현할 수 있습니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장하며, 이 쿠키는 프레임워크가 생성하는 각 응답마다 포함됩니다. 응답에 포함된 쿠키 값을 사용해 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 주로 개발 인편을 위해 제공되며, Angular나 Axios와 같은 일부 JavaScript 프레임워크 및 라이브러리는 동일 출처 요청 시 이 값을 자동으로 `X-XSRF-TOKEN` 헤더에 넣어줍니다.

> [!NOTE]
> 기본적으로 `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있으며, 이 라이브러리는 `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.