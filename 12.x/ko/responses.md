# HTTP 응답 (HTTP Responses)

- [응답 생성하기](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리다이렉트 (Redirects)](#redirects)
    - [이름이 지정된 라우트로 리다이렉트하기](#redirecting-named-routes)
    - [컨트롤러 액션으로 리다이렉트하기](#redirecting-controller-actions)
    - [외부 도메인으로 리다이렉트하기](#redirecting-external-domains)
    - [플래시된 세션 데이터와 함께 리다이렉트하기](#redirecting-with-flashed-session-data)
- [기타 응답 타입](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [스트리밍 응답](#streamed-responses)
    - [스트리밍 응답 사용하기](#consuming-streamed-responses)
    - [스트리밍 JSON 응답](#streamed-json-responses)
    - [이벤트 스트림 (SSE)](#event-streams)
    - [스트리밍 다운로드](#streamed-downloads)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성하기 (Creating Responses)

<a name="strings-arrays"></a>
#### 문자열과 배열

모든 라우트와 컨트롤러는 사용자의 브라우저로 응답을 반환해야 합니다. Laravel은 응답을 반환하는 여러 방법을 제공합니다. 가장 기본적인 응답은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크가 이 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다:

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열뿐만 아니라 배열도 반환할 수 있습니다. 이 배열은 자동으로 JSON 응답으로 변환됩니다:

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> Eloquent 컬렉션도 라우트나 컨트롤러에서 반환할 수 있다는 사실을 알고 계셨나요? 이들도 자동으로 JSON으로 변환됩니다. 직접 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로 라우트 액션에서 단순한 문자열이나 배열만 반환하지는 않습니다. 대신, `Illuminate\Http\Response` 인스턴스 또는 [뷰](/docs/12.x/views)를 반환하는 경우가 많습니다.

`Response` 인스턴스를 반환하면 HTTP 상태 코드와 헤더를 세밀하게 제어할 수 있습니다. 이 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 다양한 HTTP 응답 생성 메서드를 제공합니다:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션

Eloquent ORM 모델과 컬렉션도 라우트와 컨트롤러에서 직접 반환할 수 있습니다. 이 경우 Laravel은 모델이나 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [숨김 속성](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)도 존중합니다:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기 (Attaching Headers to Responses)

대부분의 응답 메서드는 체인 형태로 호출할 수 있어 응답을 유연하게 구성할 수 있습니다. 예를 들어, `header` 메서드를 사용하여 여러 헤더를 응답에 추가한 후 사용자에게 보낼 수 있습니다:

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는, `withHeaders` 메서드에 배열 형태로 다수의 헤더를 지정할 수도 있습니다:

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

<a name="cache-control-middleware"></a>
#### 캐시 컨트롤 미들웨어

Laravel은 `cache.headers` 미들웨어를 포함하여, 여러 라우트 그룹에 대해 빠르게 `Cache-Control` 헤더를 설정할 수 있게 합니다. 이 지시어들은 해당하는 캐시 컨트롤 지시어를 스네이크 케이스로 표현하며 세미콜론으로 구분해야 합니다. `etag`가 포함되면 응답 콘텐츠의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다:

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

`Illuminate\Http\Response` 인스턴스에 쿠키를 추가하려면 `cookie` 메서드를 사용하세요. 이 메서드에는 쿠키 이름, 값, 그리고 쿠키 유효 시간(분)을 넘겨줍니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수와 유사한 추가 인수들도 받을 수 있습니다. 일반적으로 이 인수들은 setcookie 함수의 인수와 동일한 의미를 가집니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

아직 응답 인스턴스가 없는 상황에서 쿠키를 전송하고자 할 때는 `Cookie` 파사드를 사용하여 쿠키를 "대기열"에 추가할 수 있습니다. 이 쿠키들은 응답이 전송되기 직전에 부착됩니다:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기

나중에 응답 인스턴스에 부착할 수 있는 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 만들고 싶다면 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 응답에 부착되지 않는 한 클라이언트에 전송되지 않습니다:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료시키기

응답에서 쿠키를 제거하려면 응답의 `withoutCookie` 메서드를 사용해 쿠키를 만료시킬 수 있습니다:

```php
return response('Hello World')->withoutCookie('name');
```

응답 인스턴스가 아직 없을 경우, `Cookie` 파사드의 `expire` 메서드를 사용해 쿠키를 만료시킬 수 있습니다:

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화 (Cookies and Encryption)

기본적으로 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에 Laravel에서 생성된 모든 쿠키는 암호화되고 서명되어, 클라이언트가 쿠키를 읽거나 수정할 수 없습니다. 애플리케이션에서 일부 쿠키에 한해 암호화를 비활성화하고 싶다면, `bootstrap/app.php` 파일 내에서 `encryptCookies` 메서드를 사용하면 됩니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

<a name="redirects"></a>
## 리다이렉트 (Redirects)

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스 인스턴스이며, 사용자를 다른 URL로 이동시키기 위한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 만드는 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

폼이 유효하지 않을 때처럼 사용자를 이전 위치로 리다이렉트하고 싶을 때는 전역 `back` 헬퍼를 사용할 수 있습니다. 이 기능은 [세션](/docs/12.x/session)에 의존하므로, `back` 함수가 호출되는 라우트는 `web` 미들웨어 그룹을 사용해야 합니다:

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검증...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리다이렉트하기 (Redirecting to Named Routes)

`redirect` 헬퍼에 인수를 넘기지 않으면 `Illuminate\Routing\Redirector` 인스턴스가 반환되어, 이 인스턴스의 메서드를 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리다이렉트하려면 `route` 메서드를 사용합니다:

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요한 경우 `route` 메서드의 두 번째 인수로 전달할 수 있습니다:

```php
// URI가 /profile/{id}인 라우트 예시

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 자동 채우기

Eloquent 모델로부터 채워지는 "ID" 파라미터가 있는 라우트로 리다이렉트할 때, 모델 인스턴스를 직접 전달해도 됩니다. ID가 자동으로 추출됩니다:

```php
// URI가 /profile/{id}인 라우트 예시

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 넣을 값을 커스텀하고 싶다면, 라우트 파라미터 정의에 컬럼명을 지정하거나(`/profile/{id:slug}`), Eloquent 모델 내에서 `getRouteKey` 메서드를 오버라이드할 수 있습니다:

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
### 컨트롤러 액션으로 리다이렉트하기 (Redirecting to Controller Actions)

[컨트롤러 액션](/docs/12.x/controllers)으로 리다이렉트할 수도 있습니다. 이때는 `action` 메서드에 컨트롤러와 액션 이름을 전달하세요:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러에 파라미터가 필요하면 `action` 메서드의 두 번째 인수로 전달합니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리다이렉트하기 (Redirecting to External Domains)

애플리케이션 외부 도메인으로 리다이렉트해야 하는 경우가 있습니다. 이때는 `away` 메서드를 사용하며, URL 인코딩이나 검증 없이 `RedirectResponse`를 생성합니다:

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 플래시된 세션 데이터와 함께 리다이렉트하기 (Redirecting With Flashed Session Data)

리다이렉트와 동시에 세션에 [플래시 데이터](/docs/12.x/session#flash-data)를 저장하는 경우가 많습니다. 보통 어떤 작업이 성공적으로 완료됐을 때 성공 메시지를 세션에 플래시하는 방식입니다. 이렇게 할 때는 메서드 체이닝으로 응답을 만들고 세션에 데이터를 저장할 수 있습니다:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

리다이렉트 후 [세션](/docs/12.x/session)에서 플래시 메시지를 Blade 구문으로 표시할 수 있습니다:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리다이렉트하기

`RedirectResponse` 인스턴스의 `withInput` 메서드를 사용하면 현재 요청의 입력 데이터를 세션에 플래시하고, 다음 요청에서 쉽게 [이전 입력값을 조회](/docs/12.x/requests#retrieving-old-input)해 폼에 다시 채울 수 있습니다. 주로 유효성 검증 실패시 사용합니다:

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입 (Other Response Types)

`response` 헬퍼는 여러 종류의 응답 인스턴스 생성에 사용할 수 있습니다. 인수를 주지 않고 호출하면, `Illuminate\Contracts\Routing\ResponseFactory` 인터페이스 구현체가 반환됩니다. 이 인터페이스는 다양한 편리한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답 (View Responses)

응답의 HTTP 상태 코드와 헤더를 직접 지정하면서, 내용으로 [뷰](/docs/12.x/views)를 반환하려면 `view` 메서드를 사용하면 됩니다:

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

커스텀 상태 코드나 헤더가 필요 없으면 전역 `view` 헬퍼 함수를 사용해도 됩니다.

<a name="json-responses"></a>
### JSON 응답 (JSON Responses)

`json` 메서드는 `Content-Type` 헤더를 `application/json`으로 자동 설정하고, 배열을 PHP `json_encode` 함수로 변환합니다:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 만들고 싶으면 `json`과 `withCallback` 메서드를 함께 사용할 수 있습니다:

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드 (File Downloads)

`download` 메서드는 브라우저가 해당 경로의 파일을 다운로드하도록 강제하는 응답을 생성합니다. 두 번째 인수는 다운로드 시 사용자에게 보여질 파일명이며, 세 번째 인수로 HTTP 헤더 배열을 전달할 수 있습니다:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> Symfony HttpFoundation는 다운로드 파일의 이름이 ASCII 문자로만 되어 있어야 합니다.

<a name="file-responses"></a>
### 파일 응답 (File Responses)

`file` 메서드는 파일을 다운로드시키지 않고 브라우저 내에서 직접(예: 이미지, PDF) 열어 보여줍니다. 절대 경로를 첫 번째 인수로 받고, 두 번째 인수로 헤더 배열을 전달할 수 있습니다:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트리밍 응답 (Streamed Responses)

생성되는 데이터를 실시간으로 스트리밍하면 대용량 응답에서 메모리 사용을 줄이고 성능을 개선할 수 있습니다. 스트리밍 응답은 서버가 데이터를 모두 전송하기 전에 클라이언트가 처리를 시작할 수 있습니다:

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // 청크 사이 지연 시뮬레이션...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

`stream` 메서드에 전달하는 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면, Laravel이 각 제네레이터 반환 값 사이에 자동으로 출력 버퍼를 플러시하고 Nginx 출력 버퍼링도 비활성화합니다:

```php
Route::post('/chat', function () {
    return response()->stream(function (): Generator {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```

<a name="consuming-streamed-responses"></a>
### 스트리밍 응답 사용하기 (Consuming Streamed Responses)

스트리밍 응답은 Laravel의 `stream` npm 패키지를 이용해 쉽게 사용할 수 있습니다. 시작하려면 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

`useStream` 훅은 스트림 URL을 주면 라라벨 앱에서 반환되는 콘텐츠를 연결해 `data` 상태를 자동으로 업데이트합니다:

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

`send`로 스트림에 데이터를 보내면, 활성화된 연결이 먼저 취소되고 새 요청이 JSON POST로 전송됩니다.

> [!WARNING]
> `useStream` 훅은 POST 요청을 보내므로 유효한 CSRF 토큰이 필요합니다. 가장 쉬운 방법은 앱 레이아웃의 `<head>`에 메타 태그로 CSRF 토큰을 포함하는 것입니다(/docs/12.x/csrf#csrf-x-csrf-token).

`useStream`의 두 번째 인수로 옵션 객체를 주어 스트림 동작을 조정할 수 있습니다. 기본값은 다음과 같습니다:

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

`onResponse`는 성공적으로 초기 응답을 받아 원시 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response)를 콜백에 전달하고, `onData`는 스트림의 각 청크 데이터가 수신될 때 호출됩니다. `onFinish`는 스트림 종료나 에러 발생 시 호출됩니다.

초기 요청 시 스트림에 페이로드를 전달하고 싶으면 `initialInput` 옵션을 사용하세요:

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

수동으로 스트림을 종료하려면 훅이 반환하는 `cancel` 메서드를 호출하세요:

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

`useStream` 훅을 사용할 때마다 스트림을 식별하기 위한 무작위 `id`가 생성되어 요청에 `X-STREAM-ID` 헤더로 포함됩니다. 여러 컴포넌트가 같은 스트림을 소비할 때는 직접 `id`를 지정해 데이터를 공유할 수 있습니다:

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
### 스트리밍 JSON 응답 (Streamed JSON Responses)

점진적으로 JSON 데이터를 스트리밍해야 할 때 `streamJson` 메서드를 사용하세요. 대규모 데이터를 브라우저로 점진적으로 전송하면서 JavaScript가 쉽게 파싱할 수 있는 형태로 보내는 데 적합합니다:

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 [useStream 훅](#consuming-streamed-responses)과 동일하지만 스트림이 끝난 후 데이터를 JSON으로 파싱한다는 점이 다릅니다:

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
### 이벤트 스트림 (SSE) (Event Streams (SSE))

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용하는 서버-전송 이벤트 (SSE) 스트림 응답을 반환합니다. 콜백(클로저)에서 스트림에 [yield](https://www.php.net/manual/en/language.generators.overview.php)로 데이터를 점진적으로 보내야 합니다:

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

이벤트 이름을 커스텀하고 싶다면 `StreamedEvent` 클래스 인스턴스를 yield할 수 있습니다:

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 사용하기

이벤트 스트림도 `stream` npm 패키지를 사용해 쉽게 소비할 수 있습니다. 시작하려면 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

`useEventStream` 훅을 사용해 스트림 URL을 제공하면 서버로부터 메시지가 도착할 때마다 `message` 상태를 자동으로 갱신합니다:

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

`useEventStream` 두 번째 인수는 스트림 동작을 세밀하게 제어할 수 있는 옵션 객체입니다. 기본값은 다음과 같습니다:

```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/stream", {
    eventName: "update",
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
  eventName: "update",
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

프론트엔드에서 직접 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체로 이벤트 스트림을 수신할 수도 있습니다. `eventStream` 메서드는 스트림 종료 시 `</stream>` 이벤트를 자동으로 전송합니다:

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

마지막 이벤트를 커스터마이징하려면 `eventStream` 메서드의 `endStreamWith` 인수에 `StreamedEvent` 인스턴스를 지정하세요:

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트리밍 다운로드 (Streamed Downloads)

때때로 문자열 응답을 즉시 파일 다운로드로 전환하고 싶을 수 있습니다. 이 경우 `streamDownload` 메서드를 사용하세요. 콜백, 파일명, 선택적 헤더 배열을 인수로 받습니다:

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

여러 라우트와 컨트롤러에서 재사용할 수 있는 사용자 정의 응답을 만들고 싶다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 보통 `App\Providers\AppServiceProvider` 같은 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출합니다:

```php
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

`macro` 함수는 첫 번째 인수로 이름을 받고, 두 번째 인수로 클로저를 받습니다. 이후 `ResponseFactory` 구현체나 `response` 헬퍼에서 매크로 이름을 호출하면 클로저가 실행됩니다:

```php
return response()->caps('foo');
```