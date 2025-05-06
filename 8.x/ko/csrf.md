# CSRF 보호

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [URI 제외하기](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개

크로스 사이트 요청 위조(CSRF)는 인증된 사용자를 가장하여 비인가 명령을 수행하는 악성 공격 중 하나입니다. 다행히도 Laravel은 [크로스 사이트 요청 위조](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) 공격으로부터 애플리케이션을 손쉽게 보호할 수 있도록 도와줍니다.

<a name="csrf-explanation"></a>
#### 취약점 설명

CSRF에 익숙하지 않은 분들을 위해, 이 취약점이 어떻게 악용될 수 있는지 예시를 들어보겠습니다. 예를 들어, 여러분의 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `/user/email`이라는 `POST` 요청을 받는 라우트가 있다고 가정해봅시다. 이 라우트는 일반적으로 사용자가 사용할 이메일 주소를 포함하는 `email` 입력 필드를 기대합니다.

CSRF 보호 없이, 악의적인 웹사이트는 여러분의 애플리케이션의 `/user/email` 라우트를 대상으로 HTML 폼을 만들고, 공격자의 이메일 주소를 입력하여 보낼 수 있습니다:

    <form action="https://your-application.com/user/email" method="POST">
        <input type="email" value="malicious-email@example.com">
    </form>

    <script>
        document.forms[0].submit();
    </script>

만약 악의적인 웹사이트가 페이지가 로드될 때 자동으로 이 폼을 제출한다면, 그 공격자는 애플리케이션의 실제 사용자가 자신들의 웹사이트를 방문하도록 유도하기만 하면 이메일 주소가 공격자의 것으로 변경됩니다.

이런 취약점을 방지하려면, 들어오는 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해 악의적인 애플리케이션이 접근할 수 없는 비공개 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지

Laravel은 애플리케이션에서 관리되는 각 활성 [사용자 세션](/docs/{{version}}/session)에 대해 자동으로 CSRF "토큰"을 생성합니다. 이 토큰은 인증된 사용자가 실제로 요청을 보내는 사용자인지 검증하는 데 사용됩니다. 이 토큰은 사용자의 세션에 저장되고, 세션이 재생성될 때마다 변경되기 때문에 악의적인 애플리케이션에서 접근할 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션이나 `csrf_token` 헬퍼 함수를 통해 액세스할 수 있습니다:

    use Illuminate\Http\Request;

    Route::get('/token', function (Request $request) {
        $token = $request->session()->token();

        $token = csrf_token();

        // ...
    });

애플리케이션에서 "POST", "PUT", "PATCH", "DELETE" HTML 폼을 정의할 때마다, 보이지 않는 CSRF `_token` 필드를 폼 안에 포함시켜야 CSRF 보호 미들웨어가 요청을 검증할 수 있습니다. 편의를 위해, `@csrf` Blade 디렉티브를 사용하면 숨겨진 토큰 입력 필드를 자동으로 생성할 수 있습니다:

    <form method="POST" action="/profile">
        @csrf

        <!-- 아래와 동일합니다... -->
        <input type="hidden" name="_token" value="{{ csrf_token() }}" />
    </form>

`App\Http\Middleware\VerifyCsrfToken` [미들웨어](/docs/{{version}}/middleware)는 기본적으로 `web` 미들웨어 그룹에 포함되어 있으며, 요청 입력의 토큰과 세션에 저장된 토큰이 일치하는지 자동으로 검증합니다. 두 토큰이 일치한다면, 해당 요청을 시작한 사용자가 실제 인증된 사용자임을 확신할 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰 & SPA

Laravel을 API 백엔드로 사용하는 SPA를 개발한다면, API 인증 및 CSRF 취약점 방지와 관련한 정보는 [Laravel Sanctum 문서](/docs/{{version}}/sanctum)를 참고하세요.

<a name="csrf-excluding-uris"></a>
### 특정 URI의 CSRF 보호 제외

특정 URI를 CSRF 보호에서 제외해야 할 때가 있습니다. 예를 들어, 결제 처리를 위해 [Stripe](https://stripe.com)를 사용하고 웹훅 시스템을 활용한다면, Stripe가 라우트에 어떤 CSRF 토큰을 보내야 할지 알 수 없으므로 해당 Stripe 웹훅 핸들러 라우트는 CSRF 보호에서 제외해야 합니다.

이런 종류의 라우트는 보통 `App\Providers\RouteServiceProvider`가 `routes/web.php` 파일의 모든 라우트에 적용하는 `web` 미들웨어 그룹 바깥에 두는 것이 좋습니다. 하지만, `VerifyCsrfToken` 미들웨어의 `$except` 속성에 URI를 추가하여 라우트를 제외할 수도 있습니다:

    <?php

    namespace App\Http\Middleware;

    use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as Middleware;

    class VerifyCsrfToken extends Middleware
    {
        /**
         * CSRF 검증에서 제외할 URI 목록
         *
         * @var array
         */
        protected $except = [
            'stripe/*',
            'http://example.com/foo/bar',
            'http://example.com/foo/*',
        ];
    }

> {tip} 편의를 위해 [테스트 실행 중](/docs/{{version}}/testing)에는 모든 라우트의 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

POST 파라미터로 CSRF 토큰을 검사하는 것 외에도, `App\Http\Middleware\VerifyCsrfToken` 미들웨어는 `X-CSRF-TOKEN` 요청 헤더도 검사합니다. 이 토큰은 HTML의 `meta` 태그에 저장할 수 있습니다:

    <meta name="csrf-token" content="{{ csrf_token() }}">

이후 jQuery 같은 라이브러리에 토큰을 모든 요청 헤더에 자동으로 추가하도록 설정할 수 있습니다. 이를 통해 레거시 JavaScript 기술로 작성된 AJAX 기반 애플리케이션에도 간편하게 CSRF 보호를 적용할 수 있습니다:

    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장하여 프레임워크가 생성하는 각 응답에 포함시킵니다. 해당 쿠키 값을 사용하여 `X-XSRF-TOKEN` 요청 헤더를 지정할 수 있습니다.

이 쿠키는 주로 개발자 편의를 위해 제공되며, Angular나 Axios 같은 일부 JavaScript 프레임워크·라이브러리는 같은 출처의 요청에 대해 이 값을 `X-XSRF-TOKEN` 헤더에 자동으로 포함시킵니다.

> {tip} 기본적으로, `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있어 `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.