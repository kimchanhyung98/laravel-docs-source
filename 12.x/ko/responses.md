# HTTP 응답 (HTTP Responses)

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리다이렉트](#redirects)
    - [명명된 라우트로 리다이렉트](#redirecting-named-routes)
    - [컨트롤러 액션으로 리다이렉트](#redirecting-controller-actions)
    - [외부 도메인으로 리다이렉트](#redirecting-external-domains)
    - [세션에 플래시 데이터와 함께 리다이렉트](#redirecting-with-flashed-session-data)
- [기타 응답 유형](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [스트림 응답](#streamed-responses)
    - [스트림 응답 사용하기](#consuming-streamed-responses)
    - [스트리밍 JSON 응답](#streamed-json-responses)
    - [이벤트 스트림(SSE)](#event-streams)
    - [스트리밍 다운로드](#streamed-downloads)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성

<a name="strings-arrays"></a>
#### 문자열 및 배열

모든 라우트와 컨트롤러는 사용자 브라우저로 반환할 응답을 리턴해야 합니다. 라라벨에서는 여러 가지 방법으로 응답을 반환할 수 있습니다. 가장 기본적인 방법은 라우트나 컨트롤러에서 문자열을 리턴하는 것입니다. 프레임워크는 해당 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다.

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열뿐만 아니라 배열도 반환할 수 있습니다. 프레임워크는 배열을 자동으로 JSON 응답으로 변환합니다.

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/12.x/eloquent-collections)도 반환할 수 있다는 사실, 알고 계셨나요? Eloquent 컬렉션은 자동으로 JSON으로 변환됩니다. 한 번 시도해보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로 라우트에서 단순한 문자열이나 배열만 반환하는 경우는 많지 않습니다. 대신, 대부분은 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/12.x/views)를 반환하게 됩니다.

`Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 자유롭게 커스텀할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 다양한 HTTP 응답을 만들기 위한 여러 메서드를 제공합니다.

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델 및 컬렉션

[엘로퀀트 ORM](/docs/12.x/eloquent)의 모델이나 컬렉션을 라우트 또는 컨트롤러에서 직접 반환할 수도 있습니다. 이 경우 라라벨이 모델과 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [숨김 속성](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)도 정상적으로 적용됩니다.

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 관련 메서드는 체이닝이 가능하므로, 응답 인스턴스를 더욱 유연하게 구성할 수 있습니다. 예를 들어, `header` 메서드를 사용하여 여러 개의 헤더를 응답에 연달아 추가할 수 있습니다.

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는 `withHeaders` 메서드를 사용해 한 번에 여러 헤더를 배열로 전달할 수도 있습니다.

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

라라벨에는 `cache.headers` 미들웨어가 내장되어 있어, 여러 라우트에 `Cache-Control` 헤더를 빠르게 적용할 수 있습니다. 캐시 제어 지시어는 해당 캐시 디렉티브의 스네이크 케이스 형태로 전달하고, 각 지시어는 세미콜론(`;`)으로 구분해야 합니다. 만약 지시어 목록에 `etag`를 지정하면, 응답 내용의 MD5 해시가 ETag 식별자로 자동으로 설정됩니다.

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
### 응답에 쿠키 추가하기

`Illuminate\Http\Response` 인스턴스에 `cookie` 메서드를 사용하여 쿠키를 첨부할 수 있습니다. 이 메서드에는 쿠키 이름, 값, 그리고 해당 쿠키가 유효한 기간(분 단위)을 전달해야 합니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 그 외에도 몇 가지 추가 인자를 지원합니다. 일반적으로 이 인자들은 PHP의 기본 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수에서 전달하는 인자와 동일한 역할과 의미를 가집니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

아직 응답 인스턴스를 만들지 않은 시점에 앞으로 전송될 응답에 반드시 쿠키를 포함하고 싶다면, `Cookie` 파사드를 사용하여 쿠키를 "큐"에 등록할 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 생성하는 데 필요한 인자들을 받으며, 이러한 쿠키들은 브라우저로 전송되기 전 응답에 첨부됩니다.

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기

나중에 응답 인스턴스에 첨부할 수 있는 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 직접 생성하고 싶을 때는 글로벌 `cookie` 헬퍼를 사용하면 됩니다. 이렇게 생성된 쿠키는 실제로 응답에 첨부하지 않는 한 클라이언트로 전송되지 않습니다.

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료

`withoutCookie` 메서드를 사용하면, 응답에 포함된 쿠키를 만료시켜서 삭제할 수 있습니다.

```php
return response('Hello World')->withoutCookie('name');
```

아직 응답 인스턴스가 없을 때는, `Cookie` 파사드의 `expire` 메서드를 사용해 쿠키를 만료시킬 수 있습니다.

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로, `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에 라라벨에서 생성하는 모든 쿠키는 암호화되고 서명되므로, 클라이언트에서 수정하거나 내용을 읽을 수 없습니다. 애플리케이션에서 특정 쿠키에 대해서만 암호화를 해제하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용하세요.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

<a name="redirects"></a>
## 리다이렉트

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스로, 사용자를 다른 URL로 이동시키기에 필요한 적절한 헤더를 포함합니다. 여러 가지 방법으로 `RedirectResponse` 인스턴스를 생성할 수 있는데, 그 중 가장 간단한 방법은 글로벌 `redirect` 헬퍼를 사용하는 것입니다.

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

사용자가 이전 방문 페이지로 다시 돌아가길 원할 때(예: 제출한 폼이 유효하지 않은 경우 등), 글로벌 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/12.x/session)을 활용하므로, 해당 라우트가 반드시 `web` 미들웨어 그룹을 사용해야 합니다.

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 명명된 라우트로 리다이렉트

`redirect` 헬퍼를 파라미터 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환되어, 이 인스턴스의 다양한 메서드를 사용할 수 있습니다. 예를 들어, 명명된 라우트로 리다이렉트하려면 `route` 메서드를 사용할 수 있습니다.

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요한 경우, 해당 값을 `route` 메서드의 두 번째 인자로 전달하면 됩니다.

```php
// 아래와 같은 URI를 가진 라우트: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 값 자동 전달

"ID" 파라미터가 존재하는 라우트로 리다이렉트할 때, 바로 Eloquent 모델 인스턴스를 전달해도 됩니다. 라라벨이 모델에서 ID 값을 자동으로 추출해 라우트 파라미터에 채워줍니다.

```php
// 아래와 같은 URI를 가진 라우트: /profile/{id}

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 사용할 값을 커스텀하고 싶다면, 라우트 파라미터 정의에서 컬럼명을 지정하거나(`/profile/{id:slug}`), Eloquent 모델의 `getRouteKey` 메서드를 오버라이드할 수 있습니다.

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
### 컨트롤러 액션으로 리다이렉트

[컨트롤러 액션](/docs/12.x/controllers)으로 리다이렉트하는 것도 가능합니다. 이 경우, 컨트롤러와 액션명을 `action` 메서드에 전달하면 됩니다.

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요한 경우, 해당 값을 두 번째 인자로 전달할 수 있습니다.

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리다이렉트

가끔 애플리케이션 외부의 도메인으로 리다이렉트해야 할 경우가 있습니다. 이때는 추가적인 URL 인코딩, 검증, 확인 없이 `RedirectResponse`를 생성하는 `away` 메서드를 사용하면 됩니다.

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 세션에 플래시 데이터와 함께 리다이렉트

일반적으로 새로운 URL로 리다이렉트 하면서 동시에 정보를 [세션에 플래시](/docs/12.x/session#flash-data)하는 경우가 많습니다. 주로 어떤 작업을 성공적으로 처리한 다음, 성공 메시지를 세션에 저장하기 위해서입니다. 이런 경우, 하나의 메서드 체이닝으로 `RedirectResponse` 인스턴스를 생성하고, 데이터를 세션에 플래시할 수 있습니다.

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리다이렉트된 후에는, [세션](/docs/12.x/session)에 저장된 메시지를 다음과 같이 [Blade 문법](/docs/12.x/blade)으로 보여줄 수 있습니다.

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리다이렉트

리다이렉트 직전에 현재 요청의 입력값(input data)을 세션에 플래시하려면, `RedirectResponse` 인스턴스의 `withInput` 메서드를 사용할 수 있습니다. 주로 폼 입력값에 유효성 에러가 발생했을 때 사용됩니다. 이렇게 입력값을 세션에 플래시하면, 다음 요청에서 [이전 입력값을 쉽게 가져와](/docs/12.x/requests#retrieving-old-input) 폼을 다시 채울 수 있습니다.

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 유형

`response` 헬퍼를 사용하면 다양한 유형의 응답 인스턴스를 생성할 수 있습니다. `response` 헬퍼를 아무런 인자 없이 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/12.x/contracts)의 구현체가 반환됩니다. 이 컨트랙트는 여러 유용한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드와 헤더를 직접 지정하면서, 동시에 [뷰](/docs/12.x/views)를 응답으로 반환해야 할 때는 `view` 메서드를 사용해야 합니다.

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

단, 특별히 HTTP 상태 코드나 헤더를 지정할 필요가 없다면, 글로벌 `view` 헬퍼 함수를 사용하는 것으로도 충분합니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 설정하고, 전달된 배열을 PHP의 `json_encode` 함수로 JSON 문자열로 변환해줍니다.

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 생성하려면, `json` 메서드와 함께 `withCallback` 메서드를 사용할 수 있습니다.

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드를 사용하면, 사용자의 브라우저가 지정한 경로의 파일을 강제로 다운로드하도록 하는 응답을 만들 수 있습니다. `download` 메서드의 두 번째 인자로 파일명을 전달하면, 사용자가 파일을 받을 때 표시되는 파일명으로 지정됩니다. 마지막 인자로는 HTTP 헤더 배열도 전달할 수 있습니다.

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은 다운로드 대상 파일의 파일명이 반드시 ASCII 문자로만 구성되어야 함을 요구합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 파일(예: 이미지나 PDF 등)을 브라우저에서 직접 볼 수 있도록 응답에 포함시켜줍니다. 이 메서드는 첫 번째 인자로 파일의 절대경로, 두 번째 인자로 헤더 배열을 받습니다.

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트림 응답

데이터가 생성되는 즉시 클라이언트로 전송(스트리밍)하면, 특히 응답이 매우 큰 경우 메모리 사용량이 크게 감소하고 성능이 향상될 수 있습니다. 스트림 응답을 사용하면 서버가 모든 데이터를 다 전송하기 전에, 클라이언트가 먼저 데이터를 받아 처리할 수 있습니다.

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // 청크 간 딜레이를 시뮬레이션...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

편의상, `stream` 메서드에 전달한 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하는 경우, 라라벨은 제너레이터가 반환하는 각 문자열마다 출력 버퍼를 자동으로 플러시하고, Nginx의 출력 버퍼링도 비활성화합니다.

```php
Route::post('/chat', function () {
    return response()->stream(function (): void {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```

<a name="consuming-streamed-responses"></a>
### 스트림 응답 사용하기

라라벨의 스트림 응답 및 이벤트 스트림과 상호작용하기 위해, `stream` npm 패키지를 사용할 수 있습니다. 이 패키지는 라라벨의 응답 스트림을 이용하기 위한 편리한 API를 제공합니다. 먼저 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

그 다음, `useStream` 훅(React/Vue)을 사용하여 이벤트 스트림을 소비할 수 있습니다. 스트림의 URL을 전달하면, 이 훅은 라라벨 애플리케이션으로부터 반환되는 모든 응답을 content로 연결(concatenate)해 `data`를 자동으로 업데이트합니다.

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, isFetching, isStreaming, send } = useStream("chat");

    const sendMessage = () => {
        send({
            message: `Current timestamp: ${Date.now()}`,
        });
    };

    return (
        <div>
            <div>{data}</div>
            {isFetching && <div>Connecting...</div>}
            {isStreaming && <div>Generating...</div>}
            <button onClick={sendMessage}>Send Message</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data, isFetching, isStreaming, send } = useStream("chat");

const sendMessage = () => {
    send({
        message: `Current timestamp: ${Date.now()}`,
    });
};
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <div v-if="isFetching">Connecting...</div>
        <div v-if="isStreaming">Generating...</div>
        <button @click="sendMessage">Send Message</button>
    </div>
</template>
```

`send`로 데이터를 전송할 때마다, 스트림에 대한 기존 연결이 종료된 뒤 새 데이터 요청이 전송됩니다. 모든 요청은 JSON 형식의 `POST` 요청으로 이루어집니다.

> [!WARNING]
> `useStream` 훅은 애플리케이션에 `POST` 요청을 보내므로, 유효한 CSRF 토큰이 필요합니다. 가장 쉬운 방법은 [레이아웃의 `head`에 `meta` 태그로 CSRF 토큰을 포함](/docs/12.x/csrf#csrf-x-csrf-token)시키는 것입니다.

`useStream`의 두 번째 인자는 옵션 객체이며, 스트림 소비 동작을 커스텀할 수 있습니다. 이 객체의 기본값은 아래와 같습니다.

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data } = useStream("chat", {
        id: undefined,
        initialInput: undefined,
        headers: undefined,
        csrfToken: undefined,
        onResponse: (response: Response) => void,
        onData: (data: string) => void,
        onCancel: () => void,
        onFinish: () => void,
        onError: (error: Error) => void,
    });

    return <div>{data}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data } = useStream("chat", {
    id: undefined,
    initialInput: undefined,
    headers: undefined,
    csrfToken: undefined,
    onResponse: (response: Response) => void,
    onData: (data: string) => void,
    onCancel: () => void,
    onFinish: () => void,
    onError: (error: Error) => void,
});
</script>

<template>
    <div>{{ data }}</div>
</template>
```

`onResponse`는 스트림의 첫 응답이 성공적으로 도착한 후 호출되며, 순수 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) 객체가 콜백으로 전달됩니다. `onData`는 각 데이터 청크(chunk)가 도착할 때마다 호출되며, 해당 청크가 콜백으로 넘어옵니다. `onFinish`는 스트림이 종료되거나 fetch/읽기(loop) 과정에서 에러가 발생할 때 호출됩니다.

기본적으로 스트림은 초기화 시 요청이 자동으로 전송되지 않습니다. 만약 스트림에 미리 전송할 데이터를 지정하고 싶다면, `initialInput` 옵션을 사용할 수 있습니다.

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data } = useStream("chat", {
        initialInput: {
            message: "Introduce yourself.",
        },
    });

    return <div>{data}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data } = useStream("chat", {
    initialInput: {
        message: "Introduce yourself.",
    },
});
</script>

<template>
    <div>{{ data }}</div>
</template>
```

스트림을 수동으로 취소하려면, 훅에서 반환되는 `cancel` 메서드를 사용할 수 있습니다.

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, cancel } = useStream("chat");

    return (
        <div>
            <div>{data}</div>
            <button onClick={cancel}>Cancel</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data, cancel } = useStream("chat");
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <button @click="cancel">Cancel</button>
    </div>
</template>
```

`useStream` 훅을 사용할 때마다 랜덤한 `id`가 생성되어, 각 요청에 `X-STREAM-ID` 헤더로 서버로 전송됩니다. 여러 컴포넌트에서 같은 스트림을 사용하면서 읽고 쓰려면, 직접 `id`를 지정해서 사용할 수 있습니다.

```tsx tab=React
// App.tsx
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, id } = useStream("chat");

    return (
        <div>
            <div>{data}</div>
            <StreamStatus id={id} />
        </div>
    );
}

// StreamStatus.tsx
import { useStream } from "@laravel/stream-react";

function StreamStatus({ id }) {
    const { isFetching, isStreaming } = useStream("chat", { id });

    return (
        <div>
            {isFetching && <div>Connecting...</div>}
            {isStreaming && <div>Generating...</div>}
        </div>
    );
}
```

```vue tab=Vue
<!-- App.vue -->
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";
import StreamStatus from "./StreamStatus.vue";

const { data, id } = useStream("chat");
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <StreamStatus :id="id" />
    </div>
</template>

<!-- StreamStatus.vue -->
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const props = defineProps<{
    id: string;
}>();

const { isFetching, isStreaming } = useStream("chat", { id: props.id });
</script>

<template>
    <div>
        <div v-if="isFetching">Connecting...</div>
        <div v-if="isStreaming">Generating...</div>
    </div>
</template>
```

<a name="streamed-json-responses"></a>

### 스트리밍 JSON 응답

대용량 데이터를 조금씩 나눠 브라우저로 전송해야 할 때는 `streamJson` 메서드를 사용할 수 있습니다. 이 메서드는 데이터를 JavaScript에서 쉽게 파싱할 수 있는 JSON 형식으로 점진적으로 보낼 때 특히 유용합니다.

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 [`useStream` 훅](#consuming-streamed-responses)과 동일하게 동작하지만, 스트리밍이 끝나면 데이터를 JSON 형식으로 파싱하려고 시도합니다.

```tsx tab=React
import { useJsonStream } from "@laravel/stream-react";

type User = {
    id: number;
    name: string;
    email: string;
};

function App() {
    const { data, send } = useJsonStream<{ users: User[] }>("users");

    const loadUsers = () => {
        send({
            query: "taylor",
        });
    };

    return (
        <div>
            <ul>
                {data?.users.map((user) => (
                    <li>
                        {user.id}: {user.name}
                    </li>
                ))}
            </ul>
            <button onClick={loadUsers}>Load Users</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useJsonStream } from "@laravel/stream-vue";

type User = {
    id: number;
    name: string;
    email: string;
};

const { data, send } = useJsonStream<{ users: User[] }>("users");

const loadUsers = () => {
    send({
        query: "taylor",
    });
};
</script>

<template>
    <div>
        <ul>
            <li v-for="user in data?.users" :key="user.id">
                {{ user.id }}: {{ user.name }}
            </li>
        </ul>
        <button @click="loadUsers">Load Users</button>
    </div>
</template>
```

<a name="event-streams"></a>
### 이벤트 스트림 (SSE)

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용하여 서버 전송 이벤트(Server-Sent Events, SSE) 스트리밍 응답을 반환할 때 활용할 수 있습니다. 이 메서드는 클로저를 인수로 받아, 해당 클로저에서 [yield](https://www.php.net/manual/en/language.generators.overview.php)를 사용해 스트림에 응답 데이터를 차례로 보낼 수 있습니다.

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

이벤트 이름을 원하는 값으로 커스터마이즈하고 싶다면, `StreamedEvent` 클래스의 인스턴스를 yield 하면 됩니다.

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 소비하기

이벤트 스트림은 라라벨의 `stream` npm 패키지를 사용하여 소비할 수 있습니다. 이 패키지는 라라벨 이벤트 스트림과 편리하게 상호작용할 수 있는 API를 제공합니다. 먼저 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

설치 후에는 `useEventStream` 훅을 이용해 이벤트 스트림을 받아올 수 있습니다. 스트림 URL을 전달하면, 스트림에서 라라벨 애플리케이션이 메시지를 전송할 때마다 이 메시지들을 합쳐서 `message` 상태로 반환합니다.

```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/chat");

  return <div>{message}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useEventStream } from "@laravel/stream-vue";

const { message } = useEventStream("/chat");
</script>

<template>
  <div>{{ message }}</div>
</template>
```

`useEventStream`의 두 번째 인수로 옵션 객체를 전달하여 스트림 소비 방식을 세부적으로 조정할 수 있습니다. 이 객체의 기본값은 아래와 같습니다.

```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/stream", {
    event: "update",
    onMessage: (message) => {
      //
    },
    onError: (error) => {
      //
    },
    onComplete: () => {
      //
    },
    endSignal: "</stream>",
    glue: " ",
  });

  return <div>{message}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useEventStream } from "@laravel/stream-vue";

const { message } = useEventStream("/chat", {
  event: "update",
  onMessage: (message) => {
    // ...
  },
  onError: (error) => {
    // ...
  },
  onComplete: () => {
    // ...
  },
  endSignal: "</stream>",
  glue: " ",
});
</script>
```

이벤트 스트림은 또한 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)를 사용해 직접 수동으로도 소비할 수 있습니다. `eventStream` 메서드는 스트림이 완료될 때 자동으로 `</stream>`을 이벤트 스트림에 전송합니다.

```js
const source = new EventSource('/chat');

source.addEventListener('update', (event) => {
    if (event.data === '</stream>') {
        source.close();

        return;
    }

    console.log(event.data);
});
```

마지막으로 스트림에 전송되는 이벤트를 커스터마이즈하려면, `eventStream` 메서드의 `endStreamWith` 인수로 `StreamedEvent` 인스턴스를 전달하면 됩니다.

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트리밍 다운로드

특정 작업의 문자열 응답을 파일로 저장하지 않고도 바로 다운로드 가능한 응답으로 전환하고 싶을 때는 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, 그리고 선택적인 헤더 배열을 인수로 받습니다.

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

여러 라우트와 컨트롤러에서 재사용할 수 있는 커스텀 응답을 정의하고자 한다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) 중 하나의 `boot` 메서드, 예를 들어 `App\Providers\AppServiceProvider`에서 호출하는 것이 좋습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

`macro` 함수는 첫 번째 인수로 매크로 이름을, 두 번째 인수로 클로저를 받습니다. 이렇게 정의된 매크로의 이름은 `ResponseFactory` 구현체 또는 `response` 헬퍼에서 호출할 때 실행됩니다.

```php
return response()->caps('foo');
```