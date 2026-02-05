# CSRF 보호 (CSRF Protection)

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [URI 제외](#csrf-excluding-uris)
- [X-CSRF-TOKEN](#csrf-x-csrf-token)
- [X-XSRF-TOKEN](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개 (Introduction)

크로스 사이트 요청 위조(Cross-site request forgeries, CSRF)는 인증된 사용자를 가장해 무단 명령을 실행하는 악의적인 공격 기법 중 하나입니다. 다행히도, Laravel은 [크로스 사이트 요청 위조](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) 공격으로부터 애플리케이션을 보호하는 기능을 쉽게 제공합니다.

<a name="csrf-explanation"></a>
#### 취약점에 대한 설명

크로스 사이트 요청 위조(CSRF)가 익숙하지 않다면, 이 취약점이 어떻게 악용될 수 있는지 예시를 살펴보겠습니다. 예를 들어, 여러분의 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `POST` 요청을 받는 `/user/email` 라우트가 있다고 가정해봅시다. 이 라우트는 보통 `email` 입력 필드에 사용자가 새로 사용하고자 하는 이메일 주소가 담겨 있기를 기대할 것입니다.

만약 CSRF 보호가 없다면, 악의적인 웹사이트는 여러분의 애플리케이션의 `/user/email` 라우트로 향하는 HTML 폼을 만들어, 공격자의 이메일 주소를 제출하도록 할 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

이렇게 악의적인 웹사이트가 페이지를 로드할 때 폼을 자동으로 제출하면, 공격자는 여러분의 애플리케이션 이용자가 자신의 웹사이트를 방문하도록 유도하기만 하면 됩니다. 그 결과, 공격자의 이메일 주소로 사용자의 정보가 변경될 수 있습니다.

이런 취약점을 막으려면, 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해 악의적인 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지 (Preventing CSRF Requests)

Laravel은 애플리케이션이 관리하는 각 활성 [사용자 세션](/docs/master/session)마다 자동으로 CSRF "토큰"을 생성합니다. 이 토큰은 인증된 사용자가 실제로 요청을 보내는지 검증하는데 사용됩니다. 이 토큰은 사용자의 세션에 저장되며, 세션이 재생성될 때마다 변경되므로, 악의적인 애플리케이션이 접근할 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션이나 `csrf_token` 헬퍼 함수를 통해 얻을 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션에서 "POST", "PUT", "PATCH", "DELETE" HTML 폼을 정의할 때마다, 폼에 숨겨진 CSRF `_token` 필드를 반드시 포함시켜 CSRF 보호 미들웨어가 요청을 검증할 수 있도록 해야 합니다. 편의상, 숨겨진 토큰 입력 필드는 `@csrf` Blade 지시어를 사용해 쉽게 추가할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- 아래 코드와 동일합니다... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

`Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` [미들웨어](/docs/master/middleware)는 기본적으로 `web` 미들웨어 그룹에 포함되어 있으며, 요청 데이터에 담긴 토큰과 세션에 저장된 토큰이 일치하는지 자동으로 검증합니다. 이 두 토큰이 일치한다면, 인증된 사용자가 실제로 요청을 보낸 것임을 확인할 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰과 SPA (CSRF Tokens & SPAs)

Laravel을 API 백엔드로 사용하며 SPA(싱글 페이지 애플리케이션, Single Page Application)를 개발하는 경우, API 인증 및 CSRF 취약점 보호와 관련해 [Laravel Sanctum 문서](/docs/master/sanctum)를 참고하시기 바랍니다.

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 특정 URI 제외 (Excluding URIs From CSRF Protection)

경우에 따라, 일부 URI를 CSRF 보호에서 제외해야 할 수도 있습니다. 예를 들어, [Stripe](https://stripe.com)로 결제 처리를 하면서 그들의 webhook 시스템을 사용할 경우, Stripe는 어떤 CSRF 토큰을 보낼지 알 수 없으므로 Stripe webhook 처리용 라우트는 CSRF 보호에서 제외해야 합니다.

이러한 라우트는 일반적으로 Laravel이 `routes/web.php` 파일의 모든 라우트에 적용하는 `web` 미들웨어 그룹 외부에 두는 것이 좋습니다. 그러나, `bootstrap/app.php` 파일에서 `validateCsrfTokens` 메서드에 URI를 지정하여 특정 라우트만 제외할 수도 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->validateCsrfTokens(except: [
        'stripe/*',
        'http://example.com/foo/bar',
        'http://example.com/foo/*',
    ]);
})
```

> [!NOTE]
> 편의를 위해, [테스트 실행](/docs/master/testing) 시에는 모든 라우트에 대해 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

POST 파라미터로 CSRF 토큰을 확인하는 것 외에도, `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` 미들웨어(기본적으로 `web` 미들웨어 그룹에 포함)는 `X-CSRF-TOKEN` 요청 헤더도 확인합니다. 예를 들어, 토큰을 HTML의 `meta` 태그에 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그리고 jQuery와 같은 라이브러리에서 모든 요청 헤더에 토큰을 자동으로 추가하도록 설정할 수 있습니다. 이렇게 하면, 기존 JavaScript 기술을 활용한 AJAX 기반 애플리케이션에서도 간단하게 CSRF 보호가 가능합니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화한 `XSRF-TOKEN` 쿠키로 저장해 프레임워크에서 생성된 각 응답에 함께 포함시킵니다. 이 쿠키의 값을 사용해 `X-XSRF-TOKEN` 요청 헤더에 지정할 수 있습니다.

이 쿠키는 주로 개발자 편의를 위해 제공되며, Angular, Axios와 같은 일부 JavaScript 프레임워크나 라이브러리는 동일 출처 요청 시 해당 값을 자동으로 `X-XSRF-TOKEN` 헤더에 포함합니다.

> [!NOTE]
> 기본적으로, `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있어, `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.
