# HTTP 응답

- [응답 생성](#creating-responses)
    - [응답에 헤더 붙이기](#attaching-headers-to-responses)
    - [응답에 쿠키 붙이기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리다이렉트](#redirects)
    - [이름이 지정된 라우트로 리다이렉트](#redirecting-named-routes)
    - [컨트롤러 액션으로 리다이렉트](#redirecting-controller-actions)
    - [외부 도메인으로 리다이렉트](#redirecting-external-domains)
    - [플래시 세션 데이터와 함께 리다이렉트](#redirecting-with-flashed-session-data)
- [기타 응답 타입](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
    - [스트림 응답](#streamed-responses)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성

<a name="strings-arrays"></a>
#### 문자열 및 배열

모든 라우트와 컨트롤러는 사용자의 브라우저로 전송될 응답을 반환해야 합니다. Laravel은 다양한 방법으로 응답을 반환할 수 있도록 지원합니다. 가장 기본적인 응답은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 해당 문자열을 자동으로 전체 HTTP 응답으로 변환합니다:

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열뿐만 아니라 배열을 반환할 수도 있습니다. 프레임워크는 배열을 자동으로 JSON 응답으로 변환합니다:

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트 또는 컨트롤러에서 [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections)도 반환할 수 있다는 것, 알고 계셨나요? 자동으로 JSON으로 변환됩니다. 한번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

대부분의 경우 라우트 액션에서 단순 문자열이나 배열만 반환하지 않습니다. 대신, 보통은 전체 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/{{version}}/views)를 반환합니다.

전체 `Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 커스터마이징할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속받아, HTTP 응답을 구성하는 다양한 메서드를 제공합니다:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션

라우트와 컨트롤러에서 [Eloquent ORM](/docs/{{version}}/eloquent) 모델 및 컬렉션을 직접 반환할 수도 있습니다. 이 경우, Laravel은 모델과 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [숨김 속성](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json) 또한 적용됩니다:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 붙이기

대부분의 응답 메서드는 체인 호출이 가능하므로, 응답 인스턴스를 유연하게 구성할 수 있습니다. 예를 들어, `header` 메서드를 사용해 응답을 사용자에게 반환하기 전에 여러 헤더를 추가할 수 있습니다:

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는 `withHeaders` 메서드를 사용해 헤더 배열을 한 번에 지정할 수도 있습니다:

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

<a name="cache-control-middleware"></a>
#### 캐시 제어 미들웨어

Laravel은 `cache.headers` 미들웨어를 제공하여, 여러 라우트에 대해 `Cache-Control` 헤더를 간편하게 설정할 수 있습니다. 지시어는 해당 cache-control 지시어의 "snake case"로 작성하고 세미콜론으로 구분합니다. 지시어 목록에 `etag`를 지정하면, 응답 내용의 MD5 해시가 자동으로 ETag 식별자로 지정됩니다:

```php
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
### 응답에 쿠키 붙이기

`Illuminate\Http\Response` 인스턴스의 `cookie` 메서드를 이용해 전송되는 응답에 쿠키를 첨부할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 그리고 쿠키가 유효하다고 판단되는 시간(분)을 전달해야 합니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 메서드와 유사한 추가 인자를 지원합니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

응답 인스턴스가 없더라도 쿠키를 "큐"에 등록해 응답과 함께 전송되도록 할 수 있습니다. `Cookie` 파사드의 `queue` 메서드를 사용하면, 쿠키가 생성되어 브라우저로 전송되는 시점에 응답에 자동으로 첨부됩니다:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기

나중에 응답 인스턴스에 첨부할 수 있도록 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하고자 할 때는, 전역 `cookie` 헬퍼를 이용할 수 있습니다. 이 쿠키는 응답 객체에 첨부하지 않는 이상 클라이언트로 전송되지 않습니다:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료시키기

응답의 `withoutCookie` 메서드를 사용하여 쿠키를 제거(만료)할 수 있습니다:

```php
return response('Hello World')->withoutCookie('name');
```

응답 인스턴스가 없어도, `Cookie` 파사드의 `expire` 메서드를 사용해 쿠키를 만료시킬 수 있습니다:

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로, `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에, Laravel이 생성하는 모든 쿠키는 암호화되고 서명되어 클라이언트에서 내용을 읽거나 조작할 수 없습니다. 애플리케이션에서 일부 쿠키에만 암호화를 비활성화하려면, 애플리케이션의 `bootstrap/app.php` 파일 내에서 `encryptCookies` 메서드를 사용하세요:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

<a name="redirects"></a>
## 리다이렉트

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때로는 제출된 폼이 유효하지 않을 때와 같이, 사용자를 이전 위치로 리다이렉트하고 싶을 때가 있습니다. 이때는 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/{{version}}/session)을 활용하므로, `back` 함수를 호출하는 라우트가 반드시 `web` 미들웨어 그룹을 사용해야 합니다:

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리다이렉트

인자가 없는 `redirect` 헬퍼 호출 시 `Illuminate\Routing\Redirector` 인스턴스가 반환되어, 이 인스턴스의 다양한 메서드를 사용할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리다이렉트하려면 `route` 메서드를 사용하세요:

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요한 경우, 두 번째 인자로 전달할 수 있습니다:

```php
// 예: URI가 /profile/{id}인 경우

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 이용해 파라미터 채우기

Eloquent 모델로 채워지는 "ID" 파라미터가 있는 라우트로 리다이렉트할 경우, 모델 자체를 전달하면 ID가 자동으로 추출되어 사용됩니다:

```php
// 예: URI가 /profile/{id}인 경우

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 들어갈 값을 커스터마이징하고 싶다면, 라우트 파라미터 정의(`/profile/{id:slug}`)에서 컬럼을 지정하거나, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드할 수 있습니다:

```php
/**
 * 모델의 라우트 키 값을 반환.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리다이렉트

[컨트롤러 액션](/docs/{{version}}/controllers)으로도 리다이렉트를 생성할 수 있습니다. 이때는 컨트롤러와 액션명을 `action` 메서드에 전달하세요:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요하다면 두 번째 인자로 전달할 수 있습니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리다이렉트

애플리케이션 외부의 도메인으로 리다이렉트해야 할 때가 있습니다. 이 경우, `away` 메서드를 사용하세요. URL 인코딩, 검증, 검사 없이 `RedirectResponse`를 생성합니다:

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 플래시 세션 데이터와 함께 리다이렉트

새 URL로 리다이렉트할 때, [데이터를 세션에 플래시](/docs/{{version}}/session#flash-data)하는 경우가 많습니다. 일반적으로 이는 작업 성공 후 세션에 성공 메시지를 플래시할 때 사용됩니다. 편의를 위해, `RedirectResponse` 인스턴스를 만들면서 체인으로 데이터를 세션에 플래시할 수 있습니다:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리다이렉트된 후에는 [세션](/docs/{{version}}/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어 [Blade 구문](/docs/{{version}}/blade)을 사용해:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리다이렉트

`RedirectResponse` 인스턴스가 제공하는 `withInput` 메서드를 사용해, 현재 요청의 입력값을 세션에 플래시한 뒤 사용자를 다른 위치로 리다이렉트할 수 있습니다. 이는 주로 사용자가 유효성 검사 오류를 만난 경우에 활용됩니다. 입력값이 세션에 플래시되면, 다음 요청에서 [쉽게 가져와](/docs/{{version}}/requests#retrieving-old-input) 폼을 재채울 수 있습니다:

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼를 사용해 다양한 유형의 응답 인스턴스를 생성할 수 있습니다. 인자 없이 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/{{version}}/contracts)의 구현체가 반환됩니다. 이 컨트랙트는 다양한 응답 생성에 유용한 여러 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드와 헤더는 제어하면서 [뷰](/docs/{{version}}/views)를 응답으로 반환해야 할 경우, `view` 메서드를 사용하세요:

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

상태 코드나 커스텀 헤더를 지정할 필요가 없다면, 전역 `view` 헬퍼 함수를 사용해도 됩니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 설정하며, 전달한 배열을 PHP의 `json_encode` 함수로 JSON으로 변환합니다:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 생성하려면, `json` 메서드와 `withCallback` 메서드를 조합해 사용할 수 있습니다:

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드는 지정한 경로의 파일을 사용자의 브라우저가 강제로 다운로드하도록 하는 응답을 생성합니다. 두 번째 인수로 파일명을 지정하면, 사용자가 다운로드할 때 보게 되는 파일명이 됩니다. 세 번째 인수로는 HTTP 헤더 배열을 전달할 수 있습니다:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은 다운로드되는 파일명에 ASCII 문자만 허용합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드를 사용하면 파일(이미지나 PDF 등)을 브라우저에서 직접 표시할 수 있습니다. 첫 번째 인수로는 파일의 절대 경로를, 두 번째 인수로는 헤더 배열을 받습니다:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
### 스트림 응답

생성되는 데이터가 클라이언트로 바로 전송되도록 하면, 메모리 사용량을 크게 줄이고 성능을 향상시킬 수 있습니다(특히 대용량 응답에서). 스트림 응답을 활용하면 서버가 전송을 마치기 전에도 클라이언트가 데이터를 처리할 수 있습니다:

```php
function streamedContent(): Generator {
    yield 'Hello, ';
    yield 'World!';
}

Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (streamedContent() as $chunk) {
            echo $chunk;
            ob_flush();
            flush();
            sleep(2); // 청크 사이를 시뮬레이션하는 지연...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

> [!NOTE]
> 내부적으로 Laravel은 PHP의 출력 버퍼링 기능을 사용합니다. 위의 예제에서 볼 수 있듯이, `ob_flush` 및 `flush` 함수를 사용해서 버퍼링된 내용을 클라이언트에 푸시해야 합니다.

<a name="streamed-json-responses"></a>
#### 스트리밍되는 JSON 응답

점진적으로 JSON 데이터를 스트리밍하려면 `streamJson` 메서드를 사용할 수 있습니다. 이 메서드는 특히 대량 데이터를 자바스크립트에서 쉽게 파싱할 수 있는 방식으로 순차적으로 브라우저에 전송할 때 유용합니다:

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

<a name="event-streams"></a>
#### 이벤트 스트림

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용하는 서버 전송 이벤트(SSE) 스트림 응답을 반환할 수 있습니다. 이 메서드는 닫힌 클로저를 받아, 스트림에 전송할 응답들을 [yield](https://www.php.net/manual/en/language.generators.overview.php)할 수 있습니다:

```php
Route::get('/chat', function () {
    return response()->eventStream(function () {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```

이벤트 이름을 커스터마이즈하려면, `StreamedEvent` 클래스의 인스턴스를 yield 하면 됩니다:

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

이벤트 스트림은 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체로 수신할 수 있습니다. 스트림이 완료되면, `eventStream` 메서드가 `</stream>` 업데이트를 자동으로 전송합니다:

```js
const source = new EventSource('/chat');

source.addEventListener('update', (event) => {
    if (event.data === '</stream>') {
        source.close();

        return;
    }

    console.log(event.data);
})
```

마지막에 전송하는 이벤트를 커스터마이즈하려면 `eventStream` 메서드의 `endStreamWith` 인수에 `StreamedEvent` 인스턴스를 전달할 수 있습니다:

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
#### 스트리밍 다운로드

때로는 작업의 문자열 응답 결과를 임시 파일에 저장하지 않고 바로 다운로드 가능한 응답으로 전환하고 싶을 수 있습니다. 이때는 `streamDownload` 메서드를 사용하면 됩니다. 콜백, 파일명, 옵션 헤더 배열을 인자로 받습니다:

```php
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
        ->contents()
        ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a name="response-macros"></a>
## 응답 매크로

다양한 라우트와 컨트롤러에서 재사용 가능한 커스텀 응답을 정의하려면 `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드 내에서 호출합니다. 예로 `App\Providers\AppServiceProvider`에서 다음과 같이 작성할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록 후 실행.
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

`macro` 함수는 첫 번째 인수로 매크로 이름, 두 번째 인수로 클로저를 받습니다. 정의된 매크로는 `ResponseFactory` 구현체나 `response` 헬퍼에서 호출할 때 실행됩니다:

```php
return response()->caps('foo');
```
