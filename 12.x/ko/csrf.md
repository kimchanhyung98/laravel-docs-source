# CSRF 보호

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [URI 제외하기](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개

크로스 사이트 요청 위조(Cross-site request forgeries, CSRF)는 인증된 사용자를 대신하여 무단 명령이 수행되는 악의적인 공격입니다. 다행히도 Laravel은 [크로스 사이트 요청 위조](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) 공격으로부터 애플리케이션을 쉽게 보호할 수 있습니다.

<a name="csrf-explanation"></a>
#### 취약점에 대한 설명

크로스 사이트 요청 위조에 익숙하지 않다면, 이 취약점이 어떻게 악용될 수 있는지 예제를 통해 알아보겠습니다. 예를 들어, 여러분의 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `POST` 요청을 받는 `/user/email` 라우트가 있다고 가정해봅시다. 이 라우트는 보통 사용자가 사용하고자 하는 이메일 주소를 담은 `email` 입력 필드를 기대할 것입니다.

CSRF 보호가 없다면, 악의적인 웹사이트는 여러분 애플리케이션의 `/user/email` 라우트로 향하는 HTML 폼을 만들고, 악성 사용자의 이메일 주소를 전송할 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

이렇게 만든 악의적인 사이트가 페이지가 로드될 때 폼을 자동으로 제출하도록 했다면, 악성 사용자는 여러분 애플리케이션의 사용자에게 자신의 웹사이트를 방문하게끔 유도하기만 하면, 그 사용자의 이메일 주소가 여러분의 애플리케이션에서 변경됩니다.

이 취약점을 막으려면, 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청마다 악의적인 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지

Laravel은 애플리케이션에서 관리하는 각 활성 [사용자 세션](/docs/{{version}}/session)에 대해 자동으로 CSRF "토큰"을 생성합니다. 이 토큰은 인증된 사용자가 실제로 해당 요청을 보낸 것인지 확인하는 데 사용됩니다. 이 토큰은 사용자의 세션에 저장되며 세션이 재생성될 때마다 변경되므로, 악의적인 애플리케이션이 이 토큰에 접근할 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션이나 `csrf_token` 헬퍼 함수를 통해 접근할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션 내에서 "POST", "PUT", "PATCH", "DELETE" HTML 폼을 정의할 때마다, 요청 유효성 검사를 위해 CSRF 보호 미들웨어가 처리할 수 있도록 숨겨진 CSRF `_token` 필드를 폼에 포함시켜야 합니다. 편리하게도, `@csrf` Blade 디렉티브를 사용하여 숨겨진 토큰 입력 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- 아래와 동일합니다. -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

`Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` [미들웨어](/docs/{{version}}/middleware)는 기본적으로 `web` 미들웨어 그룹에 포함되어 있으며, 요청 입력의 토큰과 세션에 저장된 토큰이 일치하는지 자동으로 확인합니다. 이 두 토큰이 일치하면, 요청을 시작한 사람이 인증된 사용자임을 알 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰 & SPA

Laravel을 API 백엔드로 사용하는 SPA를 개발 중이라면 [Laravel Sanctum 문서](/docs/{{version}}/sanctum)를 참고하여 API 인증과 CSRF 취약점 방지 방법을 확인해야 합니다.

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외하기

때때로 CSRF 보호에서 특정 URI 집합을 제외하고 싶을 수 있습니다. 예를 들어, [Stripe](https://stripe.com)를 사용해 결제를 처리하고 웹훅 시스템을 사용한다면, Stripe가 여러분의 라우트에 CSRF 토큰을 보낼 수 없기 때문에 Stripe 웹훅 핸들러 라우트를 CSRF 보호에서 제외해야 합니다.

보통 이러한 라우트는 `routes/web.php` 파일에서 Laravel이 모든 라우트에 적용하는 `web` 미들웨어 그룹 바깥에 두는 것이 좋습니다. 그러나, 애플리케이션의 `bootstrap/app.php` 파일에서 `validateCsrfTokens` 메서드에 제외할 URI를 전달하여 특정 라우트만 제외할 수도 있습니다:

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
> 편의를 위해 [테스트 실행](/docs/{{version}}/testing) 시 모든 라우트에 대해 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

POST 파라미터로 CSRF 토큰을 확인하는 것 외에도, 기본적으로 `web` 미들웨어 그룹에 포함되어 있는 `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` 미들웨어는 `X-CSRF-TOKEN` 요청 헤더도 확인합니다. 예를 들어, 토큰을 HTML `meta` 태그에 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

이후, jQuery와 같은 라이브러리를 통해 모든 요청 헤더에 토큰을 자동으로 추가하게 할 수 있습니다. 이를 통해 레거시 JavaScript 기술로 개발된 AJAX 기반 애플리케이션에서도 간편하게 CSRF 보호를 적용할 수 있습니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장해 프레임워크가 생성하는 모든 응답에 포함합니다. 이 쿠키 값으로 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 주로 개발자의 편의를 위해 제공되며, Angular나 Axios 등의 일부 JavaScript 프레임워크 및 라이브러리에서는 동일 출처 요청에서 자동으로 이 값을 `X-XSRF-TOKEN` 헤더에 넣어줍니다.

> [!NOTE]
> 기본적으로, `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있으며, 이 라이브러리가 `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.