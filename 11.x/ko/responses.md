# HTTP 응답 (HTTP Responses)

- [응답 생성하기](#creating-responses)
    - [응답에 헤더 붙이기](#attaching-headers-to-responses)
    - [응답에 쿠키 붙이기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리디렉션](#redirects)
    - [이름이 지정된 라우트로 리디렉션하기](#redirecting-named-routes)
    - [컨트롤러 액션으로 리디렉션하기](#redirecting-controller-actions)
    - [외부 도메인으로 리디렉션하기](#redirecting-external-domains)
    - [플래시 세션 데이터와 함께 리디렉션하기](#redirecting-with-flashed-session-data)
- [다른 응답 타입](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
    - [스트림 응답](#streamed-responses)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성하기 (Creating Responses)

<a name="strings-arrays"></a>
#### 문자열과 배열

모든 라우트와 컨트롤러는 사용자 브라우저로 전송할 응답을 반환해야 합니다. Laravel은 다양한 방식으로 응답을 반환할 수 있게 지원합니다. 가장 기본적인 응답은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. Laravel은 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다:

```
Route::get('/', function () {
    return 'Hello World';
});
```

라우트나 컨트롤러에서 문자열뿐만 아니라 배열도 반환할 수 있습니다. Laravel은 배열을 자동으로 JSON 응답으로 변환합니다:

```
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]  
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/11.x/eloquent-collections)을 반환할 수도 있다는 것을 알고 계셨나요? 이들 역시 자동으로 JSON으로 변환됩니다. 한 번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

보통 라우트 액션에서 단순 문자열이나 배열만 반환하지는 않습니다. 대신, 완전한 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/11.x/views)를 반환하는 경우가 많습니다.

완전한 `Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 직접 설정할 수 있습니다. `Response`는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, HTTP 응답을 만드는 다양한 메서드를 제공합니다:

```
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션

라우트와 컨트롤러에서 [Eloquent ORM](/docs/11.x/eloquent) 모델과 컬렉션을 직접 반환할 수도 있습니다. 이 경우 Laravel은 모델과 컬렉션을 자동으로 JSON 응답으로 변환하는데, 이때 모델의 [숨김 속성](/docs/11.x/eloquent-serialization#hiding-attributes-from-json)도 자동으로 반영됩니다:

```
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 붙이기 (Attaching Headers to Responses)

대부분의 응답 메서드는 체이닝이 가능해서 응답 인스턴스를 유창하게 구성할 수 있습니다. 예를 들어 `header` 메서드를 사용해 여러 헤더를 차례로 응답에 추가할 수 있습니다:

```
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는 `withHeaders` 메서드를 사용해 응답에 추가할 헤더를 배열로 지정할 수도 있습니다:

```
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

<a name="cache-control-middleware"></a>
#### 캐시 제어 미들웨어

Laravel은 `cache.headers` 미들웨어를 제공하며, 이를 사용하면 그룹화한 라우트에 대해 `Cache-Control` 헤더를 빠르게 설정할 수 있습니다. 캐시 제어 지시어는 대응하는 캐시-컨트롤 지시어의 "스네이크 케이스" 형태로 지정하며 세미콜론(;)으로 구분해야 합니다. 만약 지시어 목록에 `etag`가 포함되어 있으면, 응답 콘텐츠의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다:

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
### 응답에 쿠키 붙이기 (Attaching Cookies to Responses)

`Illuminate\Http\Response` 인스턴스에 쿠키를 붙이려면 `cookie` 메서드를 사용합니다. 이 메서드에는 쿠키 이름, 값, 유효 기간(분 단위)을 전달해야 합니다:

```
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 이외에도 PHP의 네이티브 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수의 인수와 거의 동일한 좀 더 적은 빈도의 인자를 받습니다:

```
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

아직 응답 인스턴스가 없지만 쿠키를 반드시 응답과 함께 보내고 싶을 경우, `Cookie` 파사드를 이용해 쿠키를 "대기열(큐)"에 넣을 수도 있습니다. `queue` 메서드는 쿠키 인스턴스 생성에 필요한 인자를 받고, 이 쿠키는 응답이 전송되기 전에 자동으로 응답에 붙여집니다:

```
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성

나중에 응답에 붙일 수 있는 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 직접 생성하려면 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 반드시 응답 인스턴스에 붙여야 클라이언트에 전달됩니다:

```
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료시키기

응답에 포함된 쿠키를 만료시켜 삭제하려면 `withoutCookie` 메서드를 사용할 수 있습니다:

```
return response('Hello World')->withoutCookie('name');
```

아직 응답 인스턴스가 없을 때는 `Cookie` 파사드의 `expire` 메서드를 사용해 쿠키를 만료시킬 수 있습니다:

```
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화 (Cookies and Encryption)

기본적으로 Laravel은 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에 모든 쿠키를 암호화 및 서명하여 클라이언트가 변조하거나 내용을 읽지 못하게 합니다. 하지만 애플리케이션에서 일부 쿠키에 대해 암호화를 비활성화하려면, `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용해 예외 쿠키를 지정할 수 있습니다:

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

<a name="redirects"></a>
## 리디렉션 (Redirects)

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스로, 사용자를 다른 URL로 이동시키기 위한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

사용자가 제출한 폼이 유효하지 않을 때처럼 이전 위치로 리디렉션하고 싶다면, 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/11.x/session)을 사용하므로 `back`을 호출하는 라우트가 반드시 `web` 미들웨어 그룹을 사용해야 합니다:

```
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리디렉션하기 (Redirecting to Named Routes)

`redirect` 헬퍼를 인수 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환됩니다. 이 인스턴스에 대해 여러 메서드를 호출할 수 있는데, 예를 들어 이름이 지정된 라우트로 리디렉션하려면 `route` 메서드를 사용합니다:

```
return redirect()->route('login');
```

라우트에 매개변수가 있으면 `route` 메서드의 두 번째 인수로 전달합니다:

```
// URI가 /profile/{id} 인 라우트의 경우

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 매개변수 전달

Eloquent 모델에서 "ID" 매개변수를 자동으로 채우는 라우트로 리디렉션할 경우, 모델 자체를 전달할 수도 있습니다. 그러면 모델의 ID가 자동으로 추출됩니다:

```
// URI가 /profile/{id} 인 라우트의 경우

return redirect()->route('profile', [$user]);
```

라우트 매개변수에 들어갈 값을 직접 제어하려면 라우트 매개변수 정의에 컬럼명을 지정(`/profile/{id:slug}`)하거나, 모델에서 `getRouteKey` 메서드를 오버라이드하면 됩니다:

```
/**
 * 모델의 라우트 키 값 반환
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리디렉션하기 (Redirecting to Controller Actions)

컨트롤러 액션으로 리디렉션하려면 `action` 메서드에 컨트롤러 클래스와 액션 이름을 배열로 전달합니다:

```
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 루트가 매개변수를 요구한다면, 두 번째 인수로 매개변수를 전달합니다:

```
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션하기 (Redirecting to External Domains)

애플리케이션 외부 도메인으로 리디렉션이 필요할 때는 `away` 메서드를 사용하면 됩니다. 이 메서드는 추가 URL 인코딩, 검증, 확인을 하지 않고 `RedirectResponse`를 생성합니다:

```
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 플래시 세션 데이터와 함께 리디렉션하기 (Redirecting With Flashed Session Data)

리디렉션과 동시에 세션에 [플래시 데이터](/docs/11.x/session#flash-data)를 저장하는 작업은 보통 함께 이루어집니다. 예를 들어 동작이 성공적으로 수행된 후 성공 메시지를 세션에 플래시 할 때 한 번에 처리할 수 있습니다. 이 경우, 유창한 체이닝으로 `RedirectResponse`를 만들면서 세션 데이터를 플래시합니다:

```
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리디렉션된 후에는 [세션](/docs/11.x/session)에서 플래시 메시지를 읽어와 보여줄 수 있습니다. 예를 들어 [Blade 문법](/docs/11.x/blade)을 사용한다면 다음과 같습니다:

```
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력 데이터와 함께 리디렉션하기

`RedirectResponse` 인스턴스에서 제공하는 `withInput` 메서드를 사용하면 현재 요청의 입력 데이터를 세션에 플래시한 뒤 사용자를 새 위치로 리디렉션할 수 있습니다. 보통 입력 유효성 검사 실패 시 사용합니다. 입력은 다음 요청 때 쉽게 [재사용](/docs/11.x/requests#retrieving-old-input)해 폼에 채울 수 있습니다:

```
return back()->withInput();
```

<a name="other-response-types"></a>
## 다른 응답 타입 (Other Response Types)

`response` 헬퍼는 다양한 타입의 응답 인스턴스를 생성하는 데 사용할 수 있습니다. 인자를 주지 않고 `response` 헬퍼를 호출하면, `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/11.x/contracts) 구현체를 반환합니다. 이 컨트랙트는 여러 유용한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답 (View Responses)

응답의 상태 코드와 헤더를 제어하면서도 [뷰](/docs/11.x/views)를 내용으로 반환해야 할 경우, `view` 메서드를 사용합니다:

```
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

물론, 사용자 정의 HTTP 상태 코드나 헤더가 필요 없을 경우 전역 `view` 헬퍼 함수만 사용해도 됩니다.

<a name="json-responses"></a>
### JSON 응답 (JSON Responses)

`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 설정하고, 주어진 배열을 PHP의 `json_encode` 함수를 통해 JSON으로 변환해 응답을 만듭니다:

```
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 만들고 싶으면 `json` 메서드와 `withCallback` 메서드를 조합해 사용할 수 있습니다:

```
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드 (File Downloads)

`download` 메서드는 주어진 경로의 파일을 사용자 브라우저가 다운로드하도록 강제하는 응답을 생성합니다. 두 번째 인수로는 다운로드 시 표시할 파일명을 지정할 수 있으며, 세 번째 인수에는 HTTP 헤더 배열을 전달할 수 있습니다:

```
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]  
> Symfony HttpFoundation은 다운로드할 파일 이름이 ASCII 문자로 되어 있어야 합니다.

<a name="file-responses"></a>
### 파일 응답 (File Responses)

`file` 메서드는 이미지나 PDF 등 파일을 브라우저에서 직접 표시할 때 사용합니다. 다운로드가 아니라 브라우저 내에 표시할 파일의 절대 경로를 첫 번째 인수로 받고, 두 번째 인수로 헤더 배열을 지정할 수 있습니다:

```
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
### 스트림 응답 (Streamed Responses)

데이터가 생성되는 즉시 스트리밍하여 클라이언트에 보내면, 매우 큰 응답이라도 메모리 사용량을 크게 줄이고 성능을 개선할 수 있습니다. 스트림 응답은 서버가 데이터를 모두 보내기 전에도 클라이언트가 데이터를 처리하기 시작할 수 있게 합니다:

```
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
            sleep(2); // 청크 사이의 지연을 시뮬레이션...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

> [!NOTE]
> 내부적으로 Laravel은 PHP의 출력 버퍼링을 활용합니다. 위 예제에서처럼 `ob_flush`와 `flush` 함수로 버퍼링된 내용을 클라이언트로 푸시해야 합니다.

<a name="streamed-json-responses"></a>
#### 스트림 JSON 응답

JSON 데이터를 점진적으로 스트리밍해야 할 경우, `streamJson` 메서드를 사용할 수 있습니다. 대량 데이터셋을 자바스크립트가 쉽게 파싱할 수 있는 형태로 점진 전송할 때 유용합니다:

```
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

<a name="event-streams"></a>
#### 이벤트 스트림

`eventStream` 메서드는 서버 발행 이벤트(SSE, Server-Sent Events)를 위한 스트림 응답을 `text/event-stream` 콘텐츠 타입으로 반환합니다. 클로저를 전달하며, 이 클로저는 스트림에 응답을 [yield](https://www.php.net/manual/en/language.generators.overview.php)하여 순차적으로 전송합니다:

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

이벤트 스트림은 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체로 소비할 수 있습니다. `eventStream` 메서드는 스트림이 끝나면 자동으로 `</stream>` 업데이트를 이벤트 스트림에 전송합니다:

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

<a name="streamed-downloads"></a>
#### 스트림 다운로드

어떤 작업의 문자열 응답을 디스크에 저장하지 않고 바로 다운로드 가능하게 만들고 싶을 때 `streamDownload` 메서드를 사용합니다. 이 메서드는 콜백, 파일명, (선택적) 헤더 배열을 인수로 받습니다:

```
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
        ->contents()
        ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a name="response-macros"></a>
## 응답 매크로 (Response Macros)

여러 라우트와 컨트롤러에서 재사용 가능한 커스텀 응답을 정의하려면 `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 `App\Providers\AppServiceProvider` 같은 애플리케이션의 [서비스 프로바이더](/docs/11.x/providers)의 `boot` 메서드 안에서 호출합니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

`macro` 메서드는 첫 번째 인수로 이름을, 두 번째 인수로 클로저를 받습니다. 매크로 이름으로 호출할 때 클로저가 실행됩니다. 예를 들어 `ResponseFactory` 구현체나 `response` 헬퍼에서 다음과 같이 호출할 수 있습니다:

```
return response()->caps('foo');
```