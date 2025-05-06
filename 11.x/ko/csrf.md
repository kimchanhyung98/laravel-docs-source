# CSRF 보호

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [URI 제외](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개

교차 사이트 요청 위조(Cross-site request forgery, CSRF)는 인증된 사용자를 대신하여 무단 명령이 실행되는 악성 공격의 일종입니다. 다행히도, Laravel은 [교차 사이트 요청 위조](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) 공격으로부터 애플리케이션을 쉽게 보호할 수 있게 해줍니다.

<a name="csrf-explanation"></a>
#### 취약점 설명

CSRF에 익숙하지 않으신 경우, 이 취약점이 어떻게 악용될 수 있는지 예시를 들어 설명해보겠습니다. 예를 들어, 여러분의 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `POST` 요청을 받는 `/user/email` 라우트가 있다고 가정해봅시다. 이 라우트는 보통 사용자가 바꾸고자 하는 이메일 주소를 담은 `email` 입력값을 받습니다.

CSRF 보호가 없다면, 악의적인 웹사이트에서 여러분의 애플리케이션의 `/user/email` 라우트로 자신의 이메일 주소를 보내는 HTML 폼을 만들 수도 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

이러한 악의적 웹페이지가 로드될 때 폼이 자동으로 제출되도록 만들면, 악의적 사용자는 단지 여러분의 애플리케이션 사용자를 유인하여 자신의 사이트를 방문하게만 하면 이메일 주소가 여러분의 애플리케이션에서 변경됩니다.

이 취약점을 방지하려면 모든 들어오는 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해 악의적인 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지

Laravel은 애플리케이션에 의해 관리되는 각 활성 [사용자 세션](/docs/{{version}}/session)마다 자동으로 CSRF "토큰"을 생성합니다. 이 토큰은 인증된 사용자가 실제로 애플리케이션에 요청을 하는지 검증하는 데 사용됩니다. 이 토큰은 사용자의 세션에 저장되며, 세션이 다시 생성될 때마다 변경되기 때문에 악의적 애플리케이션에서 접근할 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션이나 `csrf_token` 헬퍼 함수를 통해 접근할 수 있습니다:

    use Illuminate\Http\Request;

    Route::get('/token', function (Request $request) {
        $token = $request->session()->token();

        $token = csrf_token();

        // ...
    });

애플리케이션에서 "POST", "PUT", "PATCH" 또는 "DELETE" 방식의 HTML 폼을 정의할 때마다, CSRF 보호 미들웨어가 요청을 검증할 수 있도록 폼에 숨겨진 CSRF `_token` 필드를 포함해야 합니다. 편의상, `@csrf` Blade 지시어를 사용하여 숨겨진 토큰 입력 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- 아래와 동일합니다 -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

기본적으로 `web` 미들웨어 그룹에 포함되어 있는 `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` [미들웨어](/docs/{{version}}/middleware)는 요청 입력의 토큰과 세션에 저장된 토큰이 일치하는지 자동으로 검증합니다. 두 토큰이 일치한다면, 인증된 사용자가 직접 요청을 보냈다는 사실을 확인할 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰 & SPA

만약 Laravel을 API 백엔드로 사용하는 SPA를 개발하고 있다면, API 인증 및 CSRF 취약점 방지에 대한 자세한 내용은 [Laravel Sanctum 문서](/docs/{{version}}/sanctum)를 참고하세요.

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외하기

때로는 특정 URI 집합을 CSRF 보호에서 제외하고 싶을 수 있습니다. 예를 들어, [Stripe](https://stripe.com)와 같은 결제 서비스를 사용하고 웹훅 시스템을 활용할 경우, Stripe 웹훅 핸들러 라우트는 CSRF 보호에서 제외해야 합니다. 이유는 Stripe가 어떤 CSRF 토큰을 여러분의 라우트로 보내야 하는지 알지 못하기 때문입니다.

일반적으로 이런 종류의 라우트는 Laravel이 `routes/web.php` 파일 내의 모든 라우트에 적용하는 `web` 미들웨어 그룹 밖에 두는 것이 좋습니다. 그러나, 애플리케이션의 `bootstrap/app.php` 파일에서 `validateCsrfTokens` 메소드에 제외할 URI를 지정하여 특정 라우트만 CSRF 보호에서 제외할 수도 있습니다:

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->validateCsrfTokens(except: [
            'stripe/*',
            'http://example.com/foo/bar',
            'http://example.com/foo/*',
        ]);
    })

> [!NOTE]  
> 편의를 위해 [테스트 실행 시](/docs/{{version}}/testing) 모든 라우트에 대해서 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

POST 파라미터로서의 CSRF 토큰 검사 외에도, 기본적으로 `web` 미들웨어 그룹에 포함된 `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` 미들웨어는 `X-CSRF-TOKEN` 요청 헤더도 검사합니다. 예를 들어, HTML의 `meta` 태그에 토큰을 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그런 다음 jQuery와 같은 라이브러리를 활용하여 모든 요청 헤더에 자동으로 토큰을 추가하도록 할 수 있습니다. 이 방식은 레거시 JavaScript 기술 기반의 AJAX 애플리케이션에서도 간편하게 CSRF 보호를 제공합니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재의 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장하여 프레임워크가 생성하는 각 응답에 포함시켜 보냅니다. 쿠키 값을 사용해 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 주로 개발자 편의를 위한 것으로, Angular나 Axios와 같은 일부 JavaScript 프레임워크 및 라이브러리는 동일 출처 요청에서 이 값을 `X-XSRF-TOKEN` 헤더에 자동으로 넣어줍니다.

> [!NOTE]  
> 기본적으로 `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있으며, 이 라이브러리는 `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.