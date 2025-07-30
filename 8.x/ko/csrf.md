# CSRF 보호 (CSRF Protection)

- [소개](#csrf-introduction)
- [CSRF 요청 방지하기](#preventing-csrf-requests)
    - [URI 제외하기](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개 (Introduction)

크로스 사이트 요청 위조(CSRF)는 인증된 사용자를 가장하여 권한 없는 명령을 수행하는 악의적인 공격 유형입니다. 다행히도 Laravel은 애플리케이션을 [크로스 사이트 요청 위조 공격](https://en.wikipedia.org/wiki/Cross-site_request_forgery)으로부터 쉽게 보호할 수 있도록 지원합니다.

<a name="csrf-explanation"></a>
#### 취약점에 대한 설명

크로스 사이트 요청 위조가 익숙하지 않은 경우, 이 취약점이 어떻게 악용될 수 있는지 예를 들어 설명하겠습니다. 예를 들어, 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `/user/email` 경로가 `POST` 요청을 허용한다고 가정합니다. 이 경로는 아마도 사용자가 새로 사용하고자 하는 이메일 주소를 담은 `email` 입력 필드를 기대할 것입니다.

CSRF 보호가 적용되어 있지 않으면, 악성 웹사이트는 본인의 이메일 주소를 포함해 당신의 애플리케이션 `/user/email` 경로로 전송하는 HTML 폼을 작성할 수 있습니다:

```
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

이 악성 웹사이트가 페이지가 로드될 때 자동으로 폼을 제출하면, 단지 당신의 애플리케이션 사용자를 속여 그 웹사이트를 방문하게 하는 것만으로도 그 사용자의 이메일 주소가 악성 사용자의 주소로 변경되어 버립니다.

이러한 취약점을 방지하려면, 애플리케이션으로 들어오는 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해 악성 애플리케이션이 알 수 없는 비밀 세션 값을 반드시 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지하기 (Preventing CSRF Requests)

Laravel은 애플리케이션에서 관리하는 각 활성 [사용자 세션](/docs/{{version}}/session)에 대해 CSRF "토큰"을 자동으로 생성합니다. 이 토큰은 인증된 사용자가 실제 요청을 보내고 있는지를 검증하는 데 사용됩니다. 이 토큰은 사용자 세션에 저장되며 세션이 재생성될 때마다 바뀌기 때문에, 악의적 애플리케이션은 토큰에 접근할 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션에서 또는 `csrf_token` 헬퍼 함수를 통해 얻을 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션에서 "POST", "PUT", "PATCH", "DELETE" HTML 폼을 정의할 때마다, CSRF 보호 미들웨어가 요청을 검증할 수 있도록 숨겨진 CSRF `_token` 필드를 반드시 폼에 포함해야 합니다. 편의를 위해, `@csrf` Blade 지시어를 사용해 숨겨진 토큰 입력 필드를 쉽게 생성할 수 있습니다:

```
<form method="POST" action="/profile">
    @csrf

    <!-- 다음과 동일합니다... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

`App\Http\Middleware\VerifyCsrfToken` [미들웨어](/docs/{{version}}/middleware)는 기본적으로 `web` 미들웨어 그룹에 포함되어 있으며, 요청 입력에 있는 토큰이 세션에 저장된 토큰과 일치하는지 자동으로 검사합니다. 이 두 토큰이 일치할 때, 요청을 시작한 사용자가 인증된 사용자임을 알 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰과 SPA

Laravel을 API 백엔드로 사용하는 SPA(싱글 페이지 애플리케이션)를 구축 중이라면, API 인증과 CSRF 취약점 방지에 관한 정보는 [Laravel Sanctum 문서](/docs/{{version}}/sanctum)를 참고하세요.

<a name="csrf-excluding-uris"></a>
### CSRF 보호 대상에서 URI 제외하기

가끔은 CSRF 보호 대상에서 특정 URI를 제외해야 할 필요가 있습니다. 예를 들어, 결제 처리에 [Stripe](https://stripe.com)를 사용하며 웹훅(webhook) 시스템을 이용한다면, Stripe는 CSRF 토큰을 보내지 않기 때문에 웹훅 처리 라우트를 CSRF 보호에서 제외해야 합니다.

보통 이와 같은 라우트는 `routes/web.php` 파일의 모든 라우트에 `App\Providers\RouteServiceProvider`가 적용하는 `web` 미들웨어 그룹 밖에 두는 것이 좋습니다. 하지만, `VerifyCsrfToken` 미들웨어의 `$except` 속성에 URI를 추가하여 제외시킬 수도 있습니다:

```
<?php

namespace App\Http\Middleware;

use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as Middleware;

class VerifyCsrfToken extends Middleware
{
    /**
     * CSRF 검증에서 제외할 URI 리스트
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

> [!TIP]
> 편의를 위해, CSRF 미들웨어는 [테스트 실행시](/docs/{{version}}/testing) 모든 라우트에서 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

CSRF 토큰을 POST 파라미터로 검사하는 것 외에도, `App\Http\Middleware\VerifyCsrfToken` 미들웨어는 `X-CSRF-TOKEN` 요청 헤더도 검사합니다. 예를 들어 HTML `meta` 태그에 토큰을 저장할 수 있습니다:

```
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그런 다음 jQuery 같은 라이브러리에 모든 요청 헤더에 이 토큰을 자동으로 추가하도록 지시할 수 있습니다. 이렇게 하면 이전 버전의 자바스크립트 기술을 사용하는 AJAX 기반 애플리케이션에서 간단하고 편리하게 CSRF 보호를 적용할 수 있습니다:

```
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키로 저장하여 프레임워크가 생성하는 각 응답에 이 쿠키를 포함시킵니다. 이 쿠키 값을 이용해 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 주로 개발자의 편의를 위한 것으로, Angular나 Axios 같은 일부 자바스크립트 라이브러리 및 프레임워크가 동일 출처(same-origin) 요청 시 자동으로 이 값을 `X-XSRF-TOKEN` 헤더에 넣어 전송하기 위해 제공됩니다.

> [!TIP]
> 기본적으로 `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있으며, Axios가 자동으로 `X-XSRF-TOKEN` 헤더를 전송해 줍니다.