# CSRF 보호

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [URI 제외](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개

크로스 사이트 요청 위조(CSRF, Cross-site request forgery)는 인증된 사용자를 대신하여 무단 명령이 수행되는 악의적인 공격 유형입니다. 다행히도 Laravel은 [크로스 사이트 요청 위조](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) 공격으로부터 애플리케이션을 쉽게 보호할 수 있도록 지원합니다.

<a name="csrf-explanation"></a>
#### 취약점 설명

크로스 사이트 요청 위조에 익숙하지 않은 경우, 이 취약점이 어떻게 악용될 수 있는지 예시를 통해 설명하겠습니다.  
예를 들어, 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `POST` 요청을 받는 `/user/email` 경로가 있다고 가정해봅시다. 이 경로는 사용자가 새로 사용하고자 하는 이메일 주소가 입력된 `email` 입력 필드를 기대할 것입니다.

CSRF 보호가 없다면, 악의적인 웹사이트는 애플리케이션의 `/user/email` 경로를 대상으로, 공격자의 이메일 주소가 포함된 HTML 폼을 생성할 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

 이 악의적인 웹사이트가 페이지 로드 시 자동으로 폼을 제출하도록 하면, 공격자는 단지 아무것도 모르는 애플리케이션 사용자가 자신의 웹사이트를 방문하도록 유도하기만 하면 되고, 사용자의 이메일 주소는 곧바로 변경됩니다.

 이 취약점을 막으려면 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해 악의적인 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지

Laravel은 애플리케이션이 관리하는 각 활성 [사용자 세션](/docs/{{version}}/session)마다 자동으로 CSRF "토큰"을 생성합니다. 이 토큰은 실제로 인증된 사용자가 애플리케이션에 요청을 보내고 있는지 확인하는 데 사용됩니다. 이 토큰은 사용자 세션에 저장되며, 세션이 재생성될 때마다 변경되기 때문에, 외부 악성 애플리케이션은 이를 알 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션을 통해 또는 `csrf_token` 헬퍼 함수를 통해 접근할 수 있습니다:

    use Illuminate\Http\Request;

    Route::get('/token', function (Request $request) {
        $token = $request->session()->token();

        $token = csrf_token();

        // ...
    });

애플리케이션에서 "POST", "PUT", "PATCH", "DELETE" HTML 폼을 정의할 때마다, CSRF 보호 미들웨어가 요청을 검증할 수 있도록 폼에 숨겨진 CSRF `_token` 필드를 반드시 포함해야 합니다. 편리하게도, `@csrf` Blade 지시문을 사용하여 숨겨진 토큰 입력 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- 아래와 동일합니다... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

애플리케이션의 `web` 미들웨어 그룹에 기본 포함되어 있는 `App\Http\Middleware\VerifyCsrfToken` [미들웨어](/docs/{{version}}/middleware)는, 요청 입력값의 토큰과 세션에 저장된 토큰이 일치하는지 자동으로 확인합니다. 두 토큰이 일치하면, 인증된 사용자가 실제로 요청을 시작한 것임을 알 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰 & SPA

Laravel을 API 백엔드로 사용하는 SPA(Single Page Application)를 구축한다면, API 인증 및 CSRF 취약점 방지에 관한 정보는 [Laravel Sanctum 문서](/docs/{{version}}/sanctum)를 참고하세요.

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외하기

때때로 일부 URI는 CSRF 보호 대상에서 제외하고 싶을 수 있습니다.  
예를 들어 [Stripe](https://stripe.com)와 같은 결제 서비스를 사용하고, 해당 웹훅 시스템을 적용한다면 Stripe 웹훅 처리 경로는 CSRF 보호에서 제외해야 합니다. Stripe는 어떤 CSRF 토큰을 보내야 할지 알지 못하기 때문입니다.

일반적으로 이런 경로는 `App\Providers\RouteServiceProvider`가 `routes/web.php` 파일 내의 모든 경로에 적용하는 `web` 미들웨어 그룹 밖에 두는 것이 좋습니다. 하지만, `VerifyCsrfToken` 미들웨어의 `$except` 프로퍼티에 해당 URI를 추가하여 경로를 쉽게 제외할 수도 있습니다:

    <?php

    namespace App\Http\Middleware;

    use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as Middleware;

    class VerifyCsrfToken extends Middleware
    {
        /**
         * CSRF 검증에서 제외되어야 할 URI들.
         *
         * @var array
         */
        protected $except = [
            'stripe/*',
            'http://example.com/foo/bar',
            'http://example.com/foo/*',
        ];
    }

> **참고**  
> 테스트를 [수행할 때](/docs/{{version}}/testing)는 CSRF 미들웨어가 모든 경로에 대해 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

CSRF 토큰을 POST 파라미터로 확인하는 것 외에도, `App\Http\Middleware\VerifyCsrfToken` 미들웨어는 `X-CSRF-TOKEN` 요청 헤더도 검사합니다. 예를 들어, 토큰을 HTML `meta` 태그에 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그런 다음, jQuery와 같은 라이브러리에게 모든 요청 헤더에 이 토큰을 자동으로 추가하도록 지시할 수 있습니다. 이를 통해 레거시 자바스크립트 기술을 사용하는 AJAX 기반 애플리케이션에 간편하고 편리한 CSRF 보호가 가능합니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장하여 프레임워크가 생성한 모든 응답에 포함합니다. 이 쿠키 값을 이용해 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 개발자 편의를 위해 주로 제공되며, Angular, Axios와 같은 일부 자바스크립트 프레임워크·라이브러리는 동일 출처 요청에서 이 값을 자동으로 `X-XSRF-TOKEN` 헤더에 넣어줍니다.

> **참고**  
> 기본적으로, `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있어 `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.