# HTTP 응답 (HTTP Responses)

- [응답 생성하기](#creating-responses)
    - [응답에 헤더 첨부하기](#attaching-headers-to-responses)
    - [응답에 쿠키 첨부하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리다이렉트](#redirects)
    - [이름 있는 라우트로 리다이렉트하기](#redirecting-named-routes)
    - [컨트롤러 액션으로 리다이렉트하기](#redirecting-controller-actions)
    - [외부 도메인으로 리다이렉트하기](#redirecting-external-domains)
    - [플래시 세션 데이터와 함께 리다이렉트하기](#redirecting-with-flashed-session-data)
- [기타 응답 유형](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성하기 (Creating Responses)

<a name="strings-arrays"></a>
#### 문자열과 배열 (Strings and Arrays)

모든 라우트와 컨트롤러는 사용자 브라우저로 전송할 응답을 반환해야 합니다. Laravel은 여러 가지 방법으로 응답을 반환할 수 있게 지원합니다. 가장 기본적인 응답은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 이 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다:

```
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열 대신 배열을 반환할 수도 있습니다. 이 경우 프레임워크는 배열을 자동으로 JSON 응답으로 변환합니다:

```
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]  
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/10.x/eloquent-collections)을 반환할 수도 있다는 것을 알고 계셨나요? 이들도 자동으로 JSON으로 변환됩니다. 한 번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체 (Response Objects)

보통 라우트 액션에서 단순 문자열이나 배열만 반환하는 경우는 많지 않습니다. 대신 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/10.x/views)를 반환합니다.

완전한 `Response` 인스턴스를 반환하면 HTTP 상태 코드와 헤더를 자유롭게 커스터마이징할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, HTTP 응답을 구성하기 위한 다양한 메서드를 제공합니다:

```
Route::get('/home', function () {
    return response('Hello World', 200)
                  ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션 (Eloquent Models and Collections)

라우트나 컨트롤러에서 직접 [Eloquent ORM](/docs/10.x/eloquent) 모델이나 컬렉션을 반환할 수도 있습니다. 이 경우 Laravel은 모델의 [숨겨진 속성](/docs/10.x/eloquent-serialization#hiding-attributes-from-json)을 고려하여 JSON 응답으로 자동 변환합니다:

```
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 첨부하기 (Attaching Headers to Responses)

대부분의 응답 메서드는 체인 방식으로 호출할 수 있어, 응답 인스턴스를 유창하게 구성할 수 있습니다. 예를 들어, `header` 메서드를 사용해 응답에 여러 헤더를 추가한 후 사용자에게 전송할 수 있습니다:

```
return response($content)
            ->header('Content-Type', $type)
            ->header('X-Header-One', 'Header Value')
            ->header('X-Header-Two', 'Header Value');
```

또는 `withHeaders` 메서드를 사용하여 배열 형태로 여러 헤더를 한 번에 지정할 수도 있습니다:

```
return response($content)
            ->withHeaders([
                'Content-Type' => $type,
                'X-Header-One' => 'Header Value',
                'X-Header-Two' => 'Header Value',
            ]);
```

<a name="cache-control-middleware"></a>
#### 캐시 제어 미들웨어 (Cache Control Middleware)

Laravel은 `cache.headers` 미들웨어를 포함하고 있어, 그룹 라우트에 대해 `Cache-Control` 헤더를 손쉽게 설정할 수 있습니다. 지시자는 해당 캐시-컨트롤 규칙의 "스네이크 케이스" 변환 값을 사용하며 세미콜론으로 구분합니다. 만약 `etag`가 지시자에 포함되면, 응답 콘텐츠의 MD5 해시가 ETag 식별자로 자동 설정됩니다:

```
Route::middleware('cache.headers:public;max_age=2628000;etag')->group(function () {
    Route::get('/privacy', function () {
        // ...
    });

    Route::get('/terms', function () {
        // ...
    });
});
```

<a name="attaching-cookies-to-responses"></a>
### 응답에 쿠키 첨부하기 (Attaching Cookies to Responses)

`Illuminate\Http\Response` 인스턴스에 쿠키를 첨부하려면 `cookie` 메서드를 사용합니다. 이때 쿠키 이름, 값, 쿠키가 유효한 분(minutes)을 인수로 전달해야 합니다:

```
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 이 외에도 추가 인수를 받는데, PHP의 네이티브 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수의 인자와 동일한 의미를 가집니다:

```
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

아직 응답 인스턴스가 없지만 쿠키를 응답에 첨가하고 싶다면, `Cookie` 파사드를 사용해 쿠키를 큐에 "대기"시킬 수 있습니다. 이 쿠키들은 응답이 전송되기 전에 자동으로 첨부됩니다:

```
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기 (Generating Cookie Instances)

나중에 응답에 첨부할 수 있는 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하고 싶다면 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 응답에 첨부하지 않으면 클라이언트에 전송되지 않습니다:

```
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료시키기 (Expiring Cookies Early)

응답에서 쿠키를 제거하려면, 해당 응답 인스턴스의 `withoutCookie` 메서드를 호출해 쿠키를 만료시킬 수 있습니다:

```
return response('Hello World')->withoutCookie('name');
```

아직 응답 인스턴스가 없더라도 `Cookie` 파사드의 `expire` 메서드로 쿠키를 만료시킬 수 있습니다:

```
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화 (Cookies and Encryption)

기본적으로 Laravel에서 생성하는 모든 쿠키는 암호화되고 서명되어 클라이언트가 내용을 변경하거나 읽지 못하게 보호합니다. 만약 애플리케이션에서 생성하는 특정 쿠키에 대해 암호화를 해제하고 싶다면 `app/Http/Middleware/EncryptCookies` 미들웨어의 `$except` 속성에 해당 쿠키 이름을 추가하면 됩니다:

```
/**
 * 암호화하지 않을 쿠키 이름 목록.
 *
 * @var array
 */
protected $except = [
    'cookie_name',
];
```

<a name="redirects"></a>
## 리다이렉트 (Redirects)

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스 인스턴스이며, 사용자를 다른 URL로 리다이렉트하기 위한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 가장 쉬운 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```
Route::get('/dashboard', function () {
    return redirect('home/dashboard');
});
```

종종, 제출한 폼이 유효하지 않은 경우처럼 사용자를 이전 페이지로 되돌리려 할 때가 있습니다. 이때는 전역 `back` 헬퍼 함수를 사용하세요. 이 기능은 [세션](/docs/10.x/session)을 사용하므로, `back` 함수가 호출되는 라우트는 `web` 미들웨어 그룹을 사용해야 합니다:

```
Route::post('/user/profile', function () {
    // 요청을 검증...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름 있는 라우트로 리다이렉트하기 (Redirecting to Named Routes)

매개변수 없이 `redirect` 헬퍼를 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환되고, 이 인스턴스의 메서드를 호출할 수 있습니다. 예를 들어, 이름 있는 라우트로 리다이렉트하려면 `route` 메서드를 사용합니다:

```
return redirect()->route('login');
```

라우트에 파라미터가 있다면, 두 번째 인자로 전달할 수 있습니다:

```
// URI가 다음과 같을 경우: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델로 파라미터 채우기

"ID" 파라미터가 Eloquent 모델에서 자동 매핑되는 라우트로 리다이렉트할 때는 모델 인스턴스를 직접 전달할 수 있습니다. 그러면 해당 모델의 ID가 자동으로 추출됩니다:

```
// URI가 다음과 같을 경우: /profile/{id}

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 들어갈 값을 커스터마이징하려면, 라우트 파라미터 정의에 컬럼명을 명시(`/profile/{id:slug}`)하거나 Eloquent 모델의 `getRouteKey` 메서드를 재정의할 수 있습니다:

```
/**
 * 모델의 라우트 키 값을 반환합니다.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리다이렉트하기 (Redirecting to Controller Actions)

컨트롤러 액션으로도 리다이렉트를 생성할 수 있습니다. `action` 메서드에 컨트롤러 클래스와 액션 이름을 전달하면 됩니다:

```
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요하면 두 번째 인자로 전달하세요:

```
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리다이렉트하기 (Redirecting to External Domains)

애플리케이션 외부 도메인으로 리다이렉트해야 할 때가 있습니다. 이때는 `away` 메서드를 사용하며, URL 인코딩이나 유효성 검사 없이 `RedirectResponse`를 생성합니다:

```
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 플래시 세션 데이터와 함께 리다이렉트하기 (Redirecting With Flashed Session Data)

리다이렉트와 동시에 [플래시 데이터](/docs/10.x/session#flash-data)를 세션에 저장하는 경우가 많습니다. 주로 작업 성공 후 성공 메시지를 세션에 플래시할 때 사용합니다. 이 기능은 `RedirectResponse` 생성과 데이터 플래시를 한 번에 메서드 체이닝으로 쉽게 수행할 수 있습니다:

```
Route::post('/user/profile', function () {
    // ...

    return redirect('dashboard')->with('status', 'Profile updated!');
});
```

리다이렉트 후에는 세션에서 플래시 메시지를 꺼내서 보여줄 수 있습니다. 예를 들어, [Blade 문법](/docs/10.x/blade)으로는 다음과 같습니다:

```
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리다이렉트하기

`RedirectResponse` 인스턴스는 `withInput` 메서드를 제공하여, 현재 요청의 입력값을 세션에 플래시한 뒤 사용자에게 리다이렉트할 수 있게 합니다. 보통 검증 오류가 발생한 경우에 사용합니다. 이후 요청에서 이 입력값을 쉽게 [다시 불러와](/docs/10.x/requests#retrieving-old-input) 폼을 채울 수 있습니다:

```
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 유형 (Other Response Types)

전역 `response` 헬퍼는 다양한 타입의 응답 인스턴스를 생성할 수 있습니다. 인자를 주지 않고 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [계약](/docs/10.x/contracts) 구현체를 반환하며, 이 계약은 응답 생성에 유용한 여러 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답 (View Responses)

응답 상태 코드와 헤더를 제어하면서 응답 내용으로 [뷰](/docs/10.x/views)를 반환해야 할 때 `view` 메서드를 사용하세요:

```
return response()
            ->view('hello', $data, 200)
            ->header('Content-Type', $type);
```

HTTP 상태 코드나 커스텀 헤더가 필요하지 않다면 전역 `view` 헬퍼 함수를 사용하는 것이 더 간단합니다.

<a name="json-responses"></a>
### JSON 응답 (JSON Responses)

`json` 메서드는 `Content-Type` 헤더를 `application/json`으로 자동 설정하며, PHP의 `json_encode` 함수를 사용해 배열을 JSON 형식으로 변환합니다:

```
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 만들고 싶다면 `json` 메서드와 함께 `withCallback` 메서드를 사용할 수 있습니다:

```
return response()
            ->json(['name' => 'Abigail', 'state' => 'CA'])
            ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드 (File Downloads)

`download` 메서드는 사용자가 지정한 경로의 파일을 브라우저에서 다운로드하도록 강제하는 응답을 생성합니다. 두 번째 인자에 파일명을 지정하면 사용자가 보게 될 파일명이 됩니다. 세 번째 인자로는 HTTP 헤더 배열을 전달할 수 있습니다:

```
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]  
> 파일 다운로드를 다루는 Symfony HttpFoundation은 다운로드할 파일명이 ASCII 문자로 되어 있어야 합니다.

<a name="streamed-downloads"></a>
#### 스트림 다운로드 (Streamed Downloads)

디스크에 내용을 저장하지 않고, 문자열 결과를 다운로드 가능한 응답으로 만들고 싶을 때는 `streamDownload` 메서드를 사용하세요. 콜백, 파일명, 선택적 헤더 배열을 인자로 받습니다:

```
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
                ->contents()
                ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a name="file-responses"></a>
### 파일 응답 (File Responses)

`file` 메서드는 파일 다운로드를 강제하지 않고, 브라우저에서 직접 파일(이미지, PDF 등)을 표시합니다. 절대 경로를 첫 번째 인자로 받고, 선택적 헤더 배열을 두 번째 인자로 받습니다:

```
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="response-macros"></a>
## 응답 매크로 (Response Macros)

여러 라우트나 컨트롤러에서 재사용 가능한 커스텀 응답을 정의하고 싶다면 `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 보통은 `App\Providers\AppServiceProvider` 같은 [서비스 프로바이더](/docs/10.x/providers)의 `boot` 메서드에서 호출합니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

`macro` 함수는 첫 번째 인자로 이름을, 두 번째 인자로 클로저를 받습니다. `response` 헬퍼나 `ResponseFactory` 구현체에서 매크로 이름으로 호출할 때 클로저가 실행됩니다:

```
return response()->caps('foo');
```
