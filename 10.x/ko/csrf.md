# CSRF 보호 (CSRF Protection)

- [소개](#csrf-introduction)
- [CSRF 요청 방지하기](#preventing-csrf-requests)
    - [URI 제외하기](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개 (Introduction)

크로스 사이트 요청 위조(Cross-site request forgery, CSRF)는 인증된 사용자를 가장해 무단 명령을 실행하는 악의적인 공격 유형입니다. 다행히 Laravel은 여러분의 애플리케이션을 CSRF 공격으로부터 쉽게 보호할 수 있도록 도와줍니다.

<a name="csrf-explanation"></a>
#### 취약점 설명

크로스 사이트 요청 위조에 익숙하지 않다면, 이 취약점이 어떻게 악용될 수 있는지 살펴보겠습니다. 예를 들어, 애플리케이션에 `/user/email` 경로가 있고, 이 경로는 인증된 사용자의 이메일 주소를 변경하기 위해 `POST` 요청을 받는다고 합시다. 이 경로는 아마도 사용자가 새로 사용하길 원하는 이메일 주소를 담은 `email` 입력 필드를 기대할 것입니다.

CSRF 보호가 없다면, 악의적인 웹사이트가 여러분의 애플리케이션 `/user/email` 경로로 POST 요청을 보내는 HTML 폼을 만들어 공격자의 이메일 주소를 전송할 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

만약 악의적인 웹사이트가 페이지가 로드될 때 자동으로 이 폼을 제출한다면, 애플리케이션 사용자를 속여 그 사이트를 방문하게만 하면 공격자의 이메일 주소가 해당 사용자의 이메일로 변경됩니다.

이 취약점을 방지하려면, 모든 들어오는 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해 악의적인 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지하기 (Preventing CSRF Requests)

Laravel은 애플리케이션에서 관리하는 각 활성 [사용자 세션](/docs/10.x/session)마다 CSRF "토큰"을 자동 생성합니다. 이 토큰은 인증된 사용자가 실제 요청을 보내는 사람인지 검증하는 데 쓰입니다. 토큰은 사용자 세션에 저장되고 세션이 재생성될 때마다 변경되므로, 악의적인 애플리케이션은 토큰에 접근할 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션에서, 또는 `csrf_token` 헬퍼 함수를 통해 접근할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션에서 "POST", "PUT", "PATCH", "DELETE" 방식의 HTML 폼을 정의할 때는, CSRF 보호 미들웨어가 요청을 검증할 수 있도록 숨겨진 CSRF `_token` 필드를 반드시 포함해야 합니다. 편의상 `@csrf` Blade 지시문을 사용하여 숨겨진 토큰 입력 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- 다음과 같습니다... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

기본적으로 `web` 미들웨어 그룹에 포함된 `App\Http\Middleware\VerifyCsrfToken` [미들웨어](/docs/10.x/middleware)는 요청의 토큰과 세션에 저장된 토큰이 일치하는지 자동으로 검증합니다. 이 두 토큰이 일치하면 해당 요청을 보내는 사용자가 인증된 사용자임을 알 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰과 SPA

만약 Laravel을 API 백엔드로 사용하는 SPA(단일 페이지 애플리케이션)를 만들고 있다면, API 인증 및 CSRF 보호와 관련된 정보는 [Laravel Sanctum 문서](/docs/10.x/sanctum)를 참조하세요.

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외하기

때때로 CSRF 보호 대상에서 일부 URI를 제외해야 할 때가 있습니다. 예를 들어, [Stripe](https://stripe.com)를 결제 처리에 사용하고 Stripe 웹훅 시스템을 활용한다면, Stripe는 CSRF 토큰을 알 수 없기 때문에 Stripe 웹훅 처리 경로를 CSRF 보호 대상에서 제외해야 합니다.

일반적으로, 이러한 경로는 `routes/web.php` 파일 내에서 `App\Providers\RouteServiceProvider`가 `web` 미들웨어 그룹으로 설정한 경로 밖에 두는 것이 좋습니다. 하지만, `VerifyCsrfToken` 미들웨어의 `$except` 속성에 URI를 추가하는 방식으로도 제외할 수 있습니다:

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
> 편의를 위해, [테스트 실행 시](/docs/10.x/testing) 모든 경로에 대해 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

`App\Http\Middleware\VerifyCsrfToken` 미들웨어는 POST 파라미터로 토큰을 검사하는 것 외에도 `X-CSRF-TOKEN` 요청 헤더가 있는지 확인합니다. 예를 들어, 토큰을 HTML `meta` 태그에 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그 후 jQuery 같은 라이브러리에 모든 요청 헤더에 토큰을 자동으로 포함하도록 할 수 있습니다. 이는 기존 자바스크립트 기술을 이용한 AJAX 애플리케이션에 간단하고 편리한 CSRF 보호 수단을 제공합니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장하며, 이 쿠키는 프레임워크가 생성하는 모든 응답에 포함됩니다. 이 쿠키 값을 사용해 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 개발자 편의를 위해 주로 사용되며, Angular, Axios 같은 일부 자바스크립트 프레임워크와 라이브러리들은 동일 출처(same-origin) 요청 시 이 쿠키 값을 자동으로 `X-XSRF-TOKEN` 헤더에 넣습니다.

> [!NOTE]  
> 기본적으로, `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있어 `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.