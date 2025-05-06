# CSRF 보호

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [URI 제외](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개

크로스 사이트 요청 위조(CSRF)는 인증된 사용자를 대신하여 무단 명령이 수행되도록 하는 악의적인 공격 유형입니다. 다행히 Laravel은 [크로스 사이트 요청 위조](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) 공격으로부터 애플리케이션을 쉽게 보호할 수 있게 해줍니다.

<a name="csrf-explanation"></a>
#### 취약점 설명

CSRF에 익숙하지 않은 경우, 이 취약점이 어떻게 악용될 수 있는지 예시를 통해 설명하겠습니다. 예를 들어, 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `POST` 요청을 받는 `/user/email` 라우트가 있다고 가정해 보겠습니다. 이 라우트는 사용자가 사용하려는 이메일 주소를 입력하는 `email` 입력 필드를 기대할 것입니다.

CSRF 보호가 없다면, 악의적인 웹사이트가 여러분의 애플리케이션의 `/user/email` 라우트를 지정하고 악성 사용자의 이메일 주소를 제출하는 HTML 폼을 만들 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

만약 악성 웹사이트가 페이지를 로드할 때 자동으로 해당 폼을 제출하도록 한다면, 공격자는 여러분의 애플리케이션을 이용하는 사용자에게 자신의 사이트에 방문하도록 유도하기만 하면 되고, 그들의 이메일 주소가 여러분의 애플리케이션에서 변경됩니다.

이런 취약점을 막기 위해서는, 모든 `POST`, `PUT`, `PATCH`, 또는 `DELETE` 요청에 대해 악의적인 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지

Laravel은 애플리케이션에서 관리하는 각 활성 [사용자 세션](/docs/{{version}}/session)마다 자동으로 CSRF "토큰"을 생성합니다. 이 토큰은 인증된 사용자가 실제로 요청을 보내는지 확인하는 데 사용됩니다. 이 토큰은 사용자의 세션에 저장되고 세션이 재생성될 때마다 변경되므로, 악의적인 애플리케이션은 이 값에 접근할 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션 또는 `csrf_token` 헬퍼 함수를 통해 접근할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션에서 "POST", "PUT", "PATCH", 또는 "DELETE" HTML 폼을 정의할 때마다, CSRF 보호 미들웨어가 요청을 검증할 수 있도록 폼에 숨겨진 CSRF `_token` 필드를 포함해야 합니다. 편의를 위해, `@csrf` Blade 지시어를 사용하여 해당 필드를 쉽게 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- 아래와 동일 -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

기본적으로 `web` 미들웨어 그룹에 포함된 [`App\Http\Middleware\VerifyCsrfToken`](/docs/{{version}}/middleware) 미들웨어가 요청 데이터의 토큰이 세션에 저장된 토큰과 일치하는지 자동으로 검증합니다. 이 두 토큰이 일치하면, 실제로 인증된 사용자가 요청을 보낸 것임을 알 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
### CSRF 토큰 & SPA

Laravel을 API 백엔드로 사용하는 SPA(Single Page Application)를 구축하고 있다면, API 인증 및 CSRF 취약점으로부터 보호하는 방법에 대해서는 [Laravel Sanctum 문서](/docs/{{version}}/sanctum)를 참고하세요.

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외하기

특정 URI 세트를 CSRF 보호에서 제외하고 싶을 때가 있습니다. 예를 들어, [Stripe](https://stripe.com)를 이용해 결제를 처리하고 해당 Webhook 시스템을 사용할 경우, Stripe가 여러분의 라우트로 CSRF 토큰을 보낼 수 없으므로 Stripe Webhook 핸들러 라우트를 CSRF 보호에서 제외해야 할 수도 있습니다.

일반적으로 이러한 라우트는 `App\Providers\RouteServiceProvider`가 `routes/web.php`의 모든 라우트에 적용하는 `web` 미들웨어 그룹 밖에 배치하는 것이 좋습니다. 그러나, `VerifyCsrfToken` 미들웨어의 `$except` 속성에 URI를 추가하여 해당 라우트를 CSRF 보호에서 제외할 수도 있습니다:

```php
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
```

> [!NOTE]  
> 편의를 위해 [테스트 실행 시](/docs/{{version}}/testing) 모든 라우트에 대해 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

POST 파라미터의 CSRF 토큰을 확인하는 것 외에, `App\Http\Middleware\VerifyCsrfToken` 미들웨어는 `X-CSRF-TOKEN` 요청 헤더도 검사합니다. 예를 들어, HTML의 `meta` 태그에 토큰을 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그리고 jQuery와 같은 라이브러리를 통해 모든 요청 헤더에 토큰을 자동으로 추가하도록 할 수 있습니다. 이렇게 하면 레거시 JavaScript 기술로 작성된 AJAX 기반 애플리케이션도 간편하게 CSRF 보호를 적용할 수 있습니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장하여 프레임워크에서 생성하는 각 응답과 함께 전송합니다. 이 쿠키 값을 사용하여 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 주로 개발 편의를 위해 제공되며, Angular, Axios와 같은 일부 JavaScript 프레임워크 및 라이브러리는 동일 출처 요청 시 해당 쿠키 값을 자동으로 `X-XSRF-TOKEN` 헤더에 넣어 전송합니다.

> [!NOTE]  
> 기본적으로, `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있으며, Axios가 `X-XSRF-TOKEN` 헤더를 자동으로 전송해줍니다.