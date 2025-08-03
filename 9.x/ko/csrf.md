# CSRF 보호 (CSRF Protection)

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [URI 제외하기](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개 (Introduction)

크로스 사이트 요청 위조(Cross-site request forgeries)는 인증된 사용자를 가장하여 권한 없는 명령을 실행하는 악의적인 공격 유형입니다. 다행히 Laravel은 애플리케이션을 [크로스 사이트 요청 위조(CSRF)](https://en.wikipedia.org/wiki/Cross-site_request_forgery) 공격으로부터 쉽게 보호할 수 있도록 지원합니다.

<a name="csrf-explanation"></a>
#### 취약점 설명

크로스 사이트 요청 위조가 익숙하지 않은 경우, 이 취약점이 어떻게 악용될 수 있는지 예를 들어 설명하겠습니다. 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `POST` 요청을 받는 `/user/email` 경로가 있다고 가정해 보겠습니다. 대개 이 경로는 사용자가 새로 사용할 이메일 주소를 담고 있는 `email` 입력 필드를 기대합니다.

CSRF 보호가 없는 상태라면, 악의적인 웹사이트가 HTML 폼을 만들어서 애플리케이션의 `/user/email` 경로로 자신의 이메일 주소를 전송할 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

만약 악의적인 웹사이트가 페이지가 로드될 때 폼을 자동 제출한다면, 악의적인 사용자는 당신의 애플리케이션 사용자를 이 웹사이트로 유인하는 것만으로 그 사용자의 이메일 주소가 변경되게 할 수 있습니다.

이 취약점을 막기 위해서는 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해 악의적인 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지 (Preventing CSRF Requests)

Laravel은 애플리케이션에서 관리하는 각 활성 [사용자 세션](/docs/9.x/session)마다 CSRF "토큰"을 자동으로 생성합니다. 이 토큰은 인증된 사용자가 실제로 요청을 보내는 사람인지 확인하는 데 사용됩니다. 토큰은 사용자의 세션에 저장되고 세션이 재생성될 때마다 변경되기에, 악성 애플리케이션이 이를 알 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션을 통해 또는 `csrf_token` 헬퍼 함수를 통해 접근할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션에서 "POST", "PUT", "PATCH", "DELETE" HTML 폼을 정의할 때마다, CSRF 보호 미들웨어가 요청을 검증할 수 있도록 폼에 숨겨진 CSRF `_token` 필드를 반드시 포함해야 합니다. 편의를 위해 `@csrf` Blade 지시자를 사용하여 숨겨진 토큰 입력 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- 다음과 같습니다... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

기본적으로 `web` 미들웨어 그룹에 포함된 `App\Http\Middleware\VerifyCsrfToken` [미들웨어](/docs/9.x/middleware)가 요청 입력의 토큰과 세션에 저장된 토큰이 일치하는지 자동으로 검증합니다. 두 토큰이 일치할 때, 인증된 사용자가 요청을 시작한 사람임을 확인할 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰과 SPA

Laravel을 API 백엔드로 사용하는 SPA를 구축하는 경우, API 인증 및 CSRF 공격으로부터 보호에 관한 내용은 [Laravel Sanctum 문서](/docs/9.x/sanctum)를 참고하세요.

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외하기

가끔 특정 URI를 CSRF 보호 대상에서 제외하고 싶을 때가 있습니다. 예를 들어, 결제 처리에 [Stripe](https://stripe.com)를 사용하고 Stripe 웹훅 시스템을 이용한다면, Stripe는 CSRF 토큰을 전송하지 않으므로 Stripe 웹훅 처리기가 등록된 경로를 CSRF 보호 대상에서 제외해야 합니다.

일반적으로 이런 종류의 경로는 `routes/web.php` 파일의 모든 경로에 기본 적용되는 `web` 미들웨어 그룹 밖에 두는 것이 좋습니다. 그러나 `VerifyCsrfToken` 미들웨어의 `$except` 속성에 URI를 추가하여 명시적으로 제외할 수도 있습니다:

```
<?php

namespace App\Http\Middleware;

use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as Middleware;

class VerifyCsrfToken extends Middleware
{
    /**
     * CSRF 검증에서 제외할 URI 목록입니다.
     *
     * @var array
     */
    protected $except = [
        'stripe/*',
        'http://example.com/foo/bar',
        'http://example.com/foo/*',
    ];
}
```

> [!NOTE]
> 편의를 위해 테스트 실행 시 CSRF 미들웨어는 모든 경로에 대해 자동으로 비활성화됩니다([테스트 문서](/docs/9.x/testing) 참고).

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

CSRF 토큰을 POST 파라미터로 확인하는 것 외에, `App\Http\Middleware\VerifyCsrfToken` 미들웨어는 `X-CSRF-TOKEN` 요청 헤더도 검사합니다. 예를 들어 토큰을 HTML의 `meta` 태그에 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그리고 jQuery 같은 라이브러리에 모든 요청 헤더에 이 토큰을 자동으로 추가하도록 설정할 수 있습니다. 이는 구버전 JavaScript를 사용하는 AJAX 애플리케이션에서 간편하게 CSRF 보호를 적용하는 방법입니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키로 저장하며, 이는 프레임워크가 생성하는 모든 응답에 포함됩니다. 이 쿠키 값을 사용해 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 Angular, Axios 같은 일부 JavaScript 프레임워크나 라이브러리가 동일 출처(same-origin) 요청 시 자동으로 쿠키 값을 `X-XSRF-TOKEN` 헤더에 넣어 보내는 개발자 편의용입니다.

> [!NOTE]
> 기본적으로 `resources/js/bootstrap.js` 파일에 포함된 Axios HTTP 라이브러리는 `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.