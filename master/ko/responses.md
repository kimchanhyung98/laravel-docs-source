# HTTP 응답 (HTTP Responses)

- [응답 생성하기](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리디렉션 (Redirects)](#redirects)
    - [이름이 지정된 라우트로 리디렉션하기](#redirecting-named-routes)
    - [컨트롤러 액션으로 리디렉션하기](#redirecting-controller-actions)
    - [외부 도메인으로 리디렉션하기](#redirecting-external-domains)
    - [플래시된 세션 데이터와 함께 리디렉션하기](#redirecting-with-flashed-session-data)
- [다른 응답 타입](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
    - [스트리밍 응답](#streamed-responses)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성하기 (Creating Responses)

<a name="strings-arrays"></a>
#### 문자열 및 배열 (Strings and Arrays)

모든 라우트와 컨트롤러는 사용자의 브라우저로 반환할 응답을 리턴해야 합니다. Laravel은 여러 가지 방법으로 응답을 반환할 수 있도록 지원합니다. 가장 기본적인 응답은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크가 이 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다:

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열뿐만 아니라 배열도 반환할 수 있습니다. 프레임워크가 배열을 자동으로 JSON 응답으로 변환합니다:

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/master/eloquent-collections)을 반환할 수도 있다는 사실을 알고 계셨나요? Eloquent 컬렉션도 자동으로 JSON으로 변환됩니다. 한 번 시도해보세요!

<a name="response-objects"></a>
#### 응답 객체 (Response Objects)

일반적으로 라우트 액션에서는 단순 문자열이나 배열을 반환하는 대신에 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/master/views)를 반환합니다.

`Response` 인스턴스를 반환하면 HTTP 상태 코드와 헤더를 직접 설정할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, HTTP 응답을 구성할 때 유용한 여러 메서드를 제공합니다:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델 및 컬렉션 (Eloquent Models and Collections)

라우트나 컨트롤러에서 직접 [Eloquent ORM](/docs/master/eloquent) 모델이나 컬렉션을 반환할 수도 있습니다. 이 경우, Laravel이 자동으로 모델과 컬렉션을 JSON 응답으로 변환하며, 모델의 [숨긴 속성](/docs/master/eloquent-serialization#hiding-attributes-from-json)을 반영합니다:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기 (Attaching Headers to Responses)

대부분의 응답 메서드는 체이닝이 가능하여 유창하게 응답 인스턴스를 구성할 수 있습니다. 예를 들어, `header` 메서드를 사용하여 사용자에게 반환하기 전에 여러 헤더를 응답에 추가할 수 있습니다:

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는 `withHeaders` 메서드를 사용하여 응답에 추가할 헤더 배열을 지정할 수도 있습니다:

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

<a name="cache-control-middleware"></a>
#### 캐시 제어 미들웨어 (Cache Control Middleware)

Laravel은 `cache.headers` 미들웨어를 포함하며, 이를 통해 라우트 그룹에 대해 `Cache-Control` 헤더를 빠르게 설정할 수 있습니다. 지시어들은 해당 캐시 제어 지시어의 "스네이크 케이스" 표기법으로 세미콜론(`;`)으로 구분하여 전달해야 합니다. 만약 지시어 목록에 `etag`가 있으면, 응답 내용의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다:

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
### 응답에 쿠키 추가하기 (Attaching Cookies to Responses)

`Illuminate\Http\Response` 인스턴스에 쿠키를 추가하려면 `cookie` 메서드를 사용할 수 있습니다. 이 메서드에는 쿠키 이름, 값, 쿠키가 유효한 분(minutes) 수를 전달해야 합니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 이외에도 PHP의 네이티브 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수와 유사한 목적으로 사용되는 추가 인수를 받을 수 있습니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

만약 아직 응답 인스턴스를 가지지 않은 상태에서 응답에 쿠키를 반드시 포함시키고 싶다면, `Cookie` 파사드를 사용해 쿠키를 "큐잉"할 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 생성하는 데 필요한 인수를 받고, 이 쿠키들은 응답이 전송되기 전 자동으로 응답에 첨부됩니다:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기 (Generating Cookie Instances)

응답 인스턴스에 나중에 첨부할 수 있는 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하려면 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 응답에 첨부되지 않으면 클라이언트로 전송되지 않습니다:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키를 조기 만료 처리하기 (Expiring Cookies Early)

응답에서 쿠키를 제거하려면 아웃고잉 응답의 `withoutCookie` 메서드로 만료 처리할 수 있습니다:

```php
return response('Hello World')->withoutCookie('name');
```

아직 응답 인스턴스가 없는 경우에도 `Cookie` 파사드의 `expire` 메서드로 쿠키를 만료 처리할 수 있습니다:

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화 (Cookies and Encryption)

기본적으로 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에, Laravel이 생성하는 모든 쿠키는 암호화되고 서명되어 클라이언트가 쿠키를 수정하거나 읽지 못하도록 보호합니다. 애플리케이션에서 생성하는 쿠키 중 일부에 대해 암호화를 비활성화하려면, `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

<a name="redirects"></a>
## 리디렉션 (Redirects)

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스 인스턴스로, 사용자를 다른 URL로 리디렉션하는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 여러 방법이 있으며, 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때로는 제출된 폼에 오류가 있거나 무언가가 올바르지 않을 때 사용자를 이전 위치로 리디렉션하고 싶을 수 있습니다. 이때는 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/master/session)을 사용하므로, `back` 함수를 호출하는 라우트가 `web` 미들웨어 그룹에 속해 있어야 합니다:

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리디렉션하기 (Redirecting to Named Routes)

`redirect` 헬퍼를 파라미터 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스를 반환하며, 이 인스턴스에서 다양한 메서드를 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리디렉션할 때는 `route` 메서드를 사용할 수 있습니다:

```php
return redirect()->route('login');
```

라우트에 파라미터가 있다면 `route` 메서드의 두 번째 인수로 전달할 수 있습니다:

```php
// 다음 URI를 가진 라우트가 있을 때: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 채우기

라우트의 ID 파라미터가 Eloquent 모델에서 채워질 때, 모델 인스턴스를 직접 넘길 수 있습니다. 그러면 ID가 자동으로 추출됩니다:

```php
// 다음 URI를 가진 라우트가 있을 때: /profile/{id}

return redirect()->route('profile', [$user]);
```

라우트 파라미터 자리에 들어갈 값을 커스터마이징하고 싶다면, 라우트 파라미터 정의에서 컬럼을 지정(`/profile/{id:slug}`)하거나, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드할 수 있습니다:

```php
/**
 * 모델의 라우트 키 값을 반환합니다.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리디렉션하기 (Redirecting to Controller Actions)

[컨트롤러 액션](/docs/master/controllers)으로 리디렉션을 만들고 싶다면, `action` 메서드에 컨트롤러 클래스와 액션 메서드 이름을 전달하세요:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트가 파라미터를 필요로 하면 `action` 메서드의 두 번째 인수로 파라미터 배열을 전달할 수 있습니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션하기 (Redirecting to External Domains)

가끔 애플리케이션 외부의 도메인으로 리디렉션해야 할 때가 있습니다. 이 경우, `away` 메서드를 호출하면 URL 인코딩, 검증, 확인 없이 `RedirectResponse`를 생성합니다:

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 플래시된 세션 데이터와 함께 리디렉션하기 (Redirecting With Flashed Session Data)

일반적으로 새 URL로 리디렉션할 때 연관된 [세션에 플래시 데이터](/docs/master/session#flash-data)를 함께 저장하는 경우가 많습니다. 예를 들어 무언가를 성공적으로 수행한 후 성공 메시지를 세션에 플래시하는 방식입니다. 간단한 메서드 체인을 이용해 리디렉션 응답을 만들고 세션에 데이터를 동시에 플래시할 수 있습니다:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리디렉션된 후, [세션](/docs/master/session)에서 플래시된 메시지를 출력할 수 있습니다. 아래는 [Blade 문법](/docs/master/blade)을 사용한 예시입니다:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리디렉션하기 (Redirecting With Input)

`RedirectResponse` 인스턴스가 제공하는 `withInput` 메서드를 사용하면, 현재 요청의 입력값을 세션에 플래시하고 사용자를 새 위치로 리디렉션할 수 있습니다. 보통 검증 오류가 발생했을 때 사용합니다. 입력값이 세션에 플래시되면 다음 요청에서 쉽게 [이전 입력값을 불러와](/docs/master/requests#retrieving-old-input) 폼을 다시 채울 수 있습니다:

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 다른 응답 타입 (Other Response Types)

`response` 헬퍼를 사용하면 여러 다른 응답 인스턴스를 생성할 수 있습니다. 인수를 제공하지 않고 `response` 헬퍼를 호출하면, `Illuminate\Contracts\Routing\ResponseFactory` [계약](/docs/master/contracts) 구현체가 반환됩니다. 이 계약은 다양한 응답 생성에 유용한 메서드들을 제공합니다.

<a name="view-responses"></a>
### 뷰 응답 (View Responses)

응답의 상태 코드와 헤더를 제어하면서, 동시에 [뷰](/docs/master/views)를 응답 내용으로 반환하고 싶다면 `view` 메서드를 사용하세요:

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

물론, 상태 코드나 헤더를 따로 지정할 필요가 없다면 전역 `view` 헬퍼 함수를 사용할 수 있습니다.

<a name="json-responses"></a>
### JSON 응답 (JSON Responses)

`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 설정하고, 전달된 배열을 PHP의 `json_encode` 함수로 JSON 형식으로 변환합니다:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답이 필요할 때는 `json` 메서드와 `withCallback` 메서드를 조합해서 사용할 수 있습니다:

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드 (File Downloads)

`download` 메서드는 사용자의 브라우저가 특정 경로의 파일을 다운로드하도록 강제하는 응답을 생성합니다. 두 번째 인자로 다운로드 시 보여질 파일명을 지정할 수 있으며, 세 번째 인자로는 HTTP 헤더 배열을 추가할 수 있습니다:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation 라이브러리는 다운로드되는 파일명이 ASCII 문자만 포함해야 한다는 점을 요구합니다.

<a name="file-responses"></a>
### 파일 응답 (File Responses)

`file` 메서드는 다운로드를 시작하지 않고, 이미지나 PDF 같은 파일을 사용자의 브라우저에서 직접 보여줄 때 사용합니다. 첫 번째 인자로는 파일의 절대 경로를 전달하고, 두 번째 인자로는 헤더 배열을 전달할 수 있습니다:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
### 스트리밍 응답 (Streamed Responses)

데이터가 생성됨과 동시에 클라이언트에 스트리밍하면, 메모리 사용량을 크게 줄이고 성능을 개선할 수 있습니다. 특히 매우 큰 응답에 효과적입니다. 스트리밍 응답을 사용하면 서버가 데이터를 모두 생성하기 전부터 클라이언트가 데이터를 처리하기 시작할 수 있습니다:

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
            sleep(2); // 데이터 청크 간의 지연을 시뮬레이션...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

> [!NOTE]
> Laravel은 내부적으로 PHP의 출력 버퍼링 기능을 활용합니다. 위 예제처럼 `ob_flush`와 `flush` 함수를 사용해 버퍼에 쌓인 내용을 클라이언트로 즉시 전송해야 합니다.

<a name="streamed-json-responses"></a>
#### 스트리밍 JSON 응답 (Streamed JSON Responses)

크고 점진적으로 전송해야 하는 JSON 데이터를 스트리밍하며 클라이언트에서 쉽게 파싱할 수 있도록 하려면 `streamJson` 메서드를 이용할 수 있습니다:

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

<a name="event-streams"></a>
#### 이벤트 스트림 (Event Streams)

`eventStream` 메서드는 서버 전송 이벤트(SSE) 타입인 `text/event-stream` 콘텐츠 타입의 스트리밍 응답을 반환합니다. `eventStream` 메서드는 이벤트 데이터를 스트림에 전송해야 할 때마다 [yield](https://www.php.net/manual/en/language.generators.overview.php)하는 클로저를 인수로 받습니다:

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

이벤트 이름을 맞춤 지정하려면 `StreamedEvent` 클래스를 이용해 이벤트 인스턴스를 yield할 수 있습니다:

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

이벤트 스트림은 애플리케이션 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체로 소비할 수 있습니다. `eventStream` 메서드는 스트림 종료 시점을 알리는 `</stream>` 이벤트를 자동으로 전송합니다:

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

스트림이 완료되었음을 알리는 최종 이벤트는 `eventStream` 메서드의 `endStreamWith` 인수에 `StreamedEvent` 인스턴스로 전달하여 커스터마이즈할 수 있습니다:

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
#### 스트리밍 다운로드 (Streamed Downloads)

작업의 문자열 응답 결과를 디스크에 저장하지 않고도 다운로드 가능한 응답으로 만들고 싶을 때는 `streamDownload` 메서드를 사용하세요. 이 메서드는 콜백 함수, 다운로드할 파일명, 선택적으로 헤더 배열을 인수로 받습니다:

```php
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
        ->contents()
        ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a name="response-macros"></a>
## 응답 매크로 (Response Macros)

다수의 라우트와 컨트롤러에서 재사용할 수 있는 커스텀 응답을 정의하고 싶다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 보통 이 메서드는 `App\Providers\AppServiceProvider` 같은 애플리케이션의 [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드 안에서 호출합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

`macro` 함수는 첫 번째 인수로 매크로 이름을, 두 번째 인수로 클로저를 받습니다. 해당 매크로는 `ResponseFactory` 구현체 또는 `response` 헬퍼에서 매크로 이름으로 호출될 때 실행됩니다:

```php
return response()->caps('foo');
```