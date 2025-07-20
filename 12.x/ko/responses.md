# HTTP 응답 (HTTP Responses)

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리다이렉트](#redirects)
    - [네임드 라우트로 리다이렉트하기](#redirecting-named-routes)
    - [컨트롤러 액션으로 리다이렉트하기](#redirecting-controller-actions)
    - [외부 도메인으로 리다이렉트하기](#redirecting-external-domains)
    - [플래시 세션 데이터와 함께 리다이렉트하기](#redirecting-with-flashed-session-data)
- [기타 응답 유형](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [스트림 응답](#streamed-responses)
    - [스트림 응답 사용하기](#consuming-streamed-responses)
    - [스트림 JSON 응답](#streamed-json-responses)
    - [이벤트 스트림(SSE)](#event-streams)
    - [스트림 다운로드](#streamed-downloads)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성

<a name="strings-arrays"></a>
#### 문자열과 배열

모든 라우트와 컨트롤러는 사용자의 브라우저로 전송할 응답을 반환해야 합니다. 라라벨에서는 여러 가지 방식으로 응답을 반환할 수 있습니다. 가장 기본적인 방식은 라우트나 컨트롤러에서 문자열을 반환하는 방식입니다. 프레임워크가 해당 문자열을 자동으로 HTTP 응답으로 변환하여 전송합니다.

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열뿐만 아니라 배열을 반환하는 것도 가능합니다. 이 경우 배열은 자동으로 JSON 응답으로 변환됩니다.

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/12.x/eloquent-collections)을 직접 반환할 수도 있다는 사실을 알고 계셨나요? 자동으로 JSON으로 변환됩니다. 한 번 시도해보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로, 라우트에서 단순 문자열이나 배열만 반환하지 않고, 전체 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/12.x/views)를 반환하는 경우가 더 많습니다.

전체 `Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 자유롭게 수정할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 다양하고 강력한 HTTP 응답 빌더 메서드를 제공합니다.

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델 및 컬렉션

[Eloquent ORM](/docs/12.x/eloquent)의 모델이나 컬렉션을 라우트 또는 컨트롤러에서 직접 반환할 수도 있습니다. 이 경우 라라벨이 해당 모델과 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [히든 속성](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)도 올바르게 처리합니다.

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 관련 메서드는 체이닝이 가능하기 때문에, 응답 인스턴스를 유연하게 만들 수 있습니다. 예를 들어, `header` 메서드를 사용해 여러 개의 헤더를 연달아 추가할 수 있습니다.

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는 `withHeaders` 메서드를 사용해 헤더의 배열을 한 번에 추가할 수도 있습니다.

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

라라벨은 `cache.headers` 미들웨어를 제공합니다. 이 미들웨어를 사용하면 여러 라우트에 대해 `Cache-Control` 헤더를 신속하게 지정할 수 있습니다. 디렉티브는 "스네이크 케이스"로 작성해 세미콜론으로 구분합니다. `etag` 디렉티브를 지정하면, 응답 내용의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다.

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

`Illuminate\Http\Response` 인스턴스의 `cookie` 메서드를 이용해, 응답에 쿠키를 추가할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 유효 기간(분 단위)을 인수로 전달합니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 그 외에도 여러 인수를 지원합니다. 이 인수들은 PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수의 인수와 비슷한 용도와 의미를 갖습니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

응답 인스턴스가 아직 없지만, 반드시 쿠키를 응답과 함께 전송하고 싶을 때는 `Cookie` 파사드를 이용해 쿠키를 "대기(queue)" 상태로 등록할 수 있습니다. `queue` 메서드는 쿠키 생성에 필요한 인수를 전달받습니다. 이 쿠키들은 응답이 브라우저로 전송되기 전에 자동으로 붙게 됩니다.

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기

후에 응답 인스턴스에 부착할 수 있는 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 미리 생성하고 싶을 때는, 글로벌 헬퍼인 `cookie` 함수를 사용할 수 있습니다. 이 쿠키는 응답 인스턴스에 실제로 추가되기 전까지는 클라이언트에 전송되지 않습니다.

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 미리 만료시키기

`withoutCookie` 메서드를 사용하면, 특정 쿠키를 만료시켜 브라우저에서 제거할 수 있습니다.

```php
return response('Hello World')->withoutCookie('name');
```

응답 인스턴스가 아직 없는 경우에는 `Cookie` 파사드의 `expire` 메서드를 이용해 쿠키를 만료시킬 수도 있습니다.

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로 라라벨은 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에 생성된 모든 쿠키를 암호화 및 서명합니다. 따라서 클라이언트에서 쿠키를 읽거나 변경할 수 없습니다. 애플리케이션에서 생성하는 쿠키 중 일부의 암호화를 비활성화하고 싶다면, `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용하면 됩니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

<a name="redirects"></a>
## 리다이렉트

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스로, 사용자를 다른 URL로 이동하는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있으며, 가장 간단한 방법은 글로벌 헬퍼 함수인 `redirect`를 사용하는 것입니다.

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

사용자가 폼 제출에 실패했을 때와 같이, 종종 이전 위치로 리다이렉트하고 싶을 때가 있습니다. 이럴 때는 글로벌 헬퍼 함수인 `back`을 사용할 수 있습니다. 이 기능은 [세션](/docs/12.x/session)을 활용하므로, `back`을 호출하는 라우트가 반드시 `web` 미들웨어 그룹을 사용해야 합니다.

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 네임드 라우트로 리다이렉트하기

`redirect` 헬퍼에 인수를 전달하지 않으면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어 관련 메서드를 다양하게 호출할 수 있습니다. 예를 들어, 특정 이름을 가진 라우트로 리다이렉트하려면, `route` 메서드를 사용할 수 있습니다.

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요한 경우, `route` 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
// 아래와 같은 URI를 가진 라우트: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 자동 전달

만약 Eloquent 모델에서 "ID" 파라미터가 생성되는 라우트로 리다이렉트한다면, 모델 인스턴스 자체를 전달하면 됩니다. 라라벨이 자동으로 ID를 추출하여 파라미터로 사용합니다.

```php
// 아래와 같은 URI를 가진 라우트: /profile/{id}

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 들어갈 값을 직접 지정하고 싶다면, 라우트 파라미터 정의에서 컬럼을 명시(`/{id:slug}`)하거나, 모델의 `getRouteKey` 메서드를 오버라이드할 수 있습니다.

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
### 컨트롤러 액션으로 리다이렉트하기

[컨트롤러 액션](/docs/12.x/controllers)으로 리다이렉트도 가능합니다. 이 경우 컨트롤러와 액션명을 `action` 메서드에 전달하세요.

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트가 파라미터를 필요로 할 때는, 두 번째 인수로 파라미터 배열을 전달할 수 있습니다.

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리다이렉트하기

때로는 애플리케이션 외부의 도메인으로 리다이렉트해야 할 수도 있습니다. 이때는 `away` 메서드를 사용하면 되고, 이 메서드는 URL 인코딩, 검증, 확인 같은 추가 작업 없이 `RedirectResponse`를 생성합니다.

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 플래시 세션 데이터와 함께 리다이렉트하기

새 URL로 리다이렉트하면서 [세션에 데이터를 플래시](/docs/12.x/session#flash-data)하는 경우가 흔히 있습니다. 예를 들어, 어떤 작업이 성공적으로 완료된 후 성공 메시지를 세션에 저장하고 리다이렉트할 수 있습니다. 이때 하나의 연쇄 메서드를 통해 `RedirectResponse` 생성과 세션 플래시를 동시에 처리할 수 있습니다.

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리다이렉트된 후에는 [세션](/docs/12.x/session)에 저장된 메시지를 표시할 수 있습니다. 예시로 [Blade 문법](/docs/12.x/blade)을 사용할 수 있습니다.

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력 데이터와 함께 리다이렉트하기

`RedirectResponse` 인스턴스의 `withInput` 메서드를 사용하면, 현재 요청의 입력 데이터를 세션에 플래시하여 사용자를 새 위치로 리다이렉트할 수 있습니다. 주로 유효성 검사 실패 시 활용하며, 입력 데이터가 세션에 저장된 후 다음 요청에서 손쉽게 [값을 다시 가져와](/docs/12.x/requests#retrieving-old-input) 폼을 자동으로 채울 수 있습니다.

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 유형

`response` 헬퍼는 다양한 유형의 응답 인스턴스를 생성하는 데 사용할 수 있습니다. 인수가 없는 경우 `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/12.x/contracts)의 구현체가 반환됩니다. 이 컨트랙트에는 다양한 응답 생성을 위한 유용한 메서드들이 포함되어 있습니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드와 헤더를 직접 지정하면서, [뷰](/docs/12.x/views)를 응답 본문으로 반환하려면 `view` 메서드를 사용하세요.

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

만약 상태 코드나 헤더를 커스텀할 필요가 없다면, 전역 헬퍼 함수인 `view`를 바로 써도 됩니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 `application/json`으로 자동으로 설정하며, 전달된 배열을 PHP의 `json_encode` 함수로 JSON으로 변환해 반환합니다.

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 생성하려면, `json` 메서드와 함께 `withCallback`을 사용할 수 있습니다.

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저에 특정 위치의 파일을 다운로드하도록 강제하는 응답을 생성합니다. 두 번째 인수로 다운로드 시 표시할 파일명을 지정할 수 있고, 세 번째 인수로 HTTP 헤더의 배열을 전달할 수 있습니다.

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 담당하는 Symfony HttpFoundation은, 다운로드되는 파일이 ASCII 파일명을 가져야 함을 요구합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 이미지나 PDF와 같이 특정 파일을 다운로드가 아닌 브라우저에 바로 보여주는 용도로 사용할 수 있습니다. 첫 번째 인수로 파일의 절대 경로, 두 번째 인수로는 헤더 배열을 받습니다.

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트림 응답

데이터를 생성하자마자 클라이언트로 스트리밍하면, 메모리 사용량을 줄이고 성능을 개선할 수 있습니다. 특히 대용량 응답에서 효과적입니다. 스트림 응답은 서버가 모든 데이터를 다 보내기 전에 클라이언트가 먼저 일부 데이터를 받아 처리할 수 있도록 합니다.

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // 청크 간 지연 시뮬레이션
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

편의를 위해, `stream` 메서드에 전달하는 클로저에서 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면, 라라벨이 generator에서 반환된 각 문자열마다 출력 버퍼를 자동으로 비우고, Nginx의 출력 버퍼링도 비활성화합니다.

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
### 스트림 응답 사용하기

라라벨의 스트림 응답/이벤트 스트림과 상호작용할 수 있도록, `@laravel/stream-react` 또는 `@laravel/stream-vue` npm 패키지를 사용할 수 있습니다. 먼저 아래와 같이 패키지를 설치하세요.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

이후 `useStream` 훅을 사용해서 이벤트 스트림을 구독할 수 있습니다. 스트림 URL을 제공하면, 라라벨 애플리케이션에서 반환되는 내용을 반환받으며, 수신될 때마다 `data`가 자동으로 이어집니다.

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

스트림으로 데이터를 보낼 때는 `send`를 사용하며, 이때 현재의 스트림 연결을 먼저 취소한 후 새 데이터를 전송합니다. 모든 요청은 JSON `POST` 요청으로 전송됩니다.

> [!WARNING]
> `useStream` 훅이 애플리케이션으로 `POST` 요청을 보내므로, 유효한 CSRF 토큰이 필요합니다. CSRF 토큰은 [레이아웃의 head에 메타 태그로 포함](/docs/12.x/csrf#csrf-x-csrf-token)하는 것이 가장 간편한 방법입니다.

`useStream`에 두 번째 인수로 전달하는 옵션 객체를 사용해, 스트림 소비 동작을 세밀하게 제어할 수 있습니다. 기본값은 아래와 같습니다.

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

`onResponse`는 스트림으로부터의 최초 응답이 성공적으로 도착했을 때 호출되며, 원본 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) 객체를 콜백에 전달합니다. `onData`는 각 청크가 도착할 때마다 호출되며, 해당 청크가 인수로 전달됩니다. `onFinish`는 스트림이 완료되거나 fetch/read 사이클에서 오류가 발생하면 호출됩니다.

스트림이 초기화 될 때 자동으로 요청을 보내지 않습니다. 최초에 보낼 페이로드가 있다면, `initialInput` 옵션으로 값을 전달하십시오.

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

스트림을 수동으로 취소하고 싶다면, 훅에서 반환되는 `cancel` 메서드를 사용하세요.

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

`useStream` 훅을 사용할 때마다 무작위의 `id`가 생성되어, 각 요청의 `X-STREAM-ID` 헤더에 담깁니다. 여럿 컴포넌트에서 동일한 스트림을 사용할 경우, 원하는 `id`를 전달해 스트림의 읽기/쓰기를 공유할 수 있습니다.

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
### 스트림 JSON 응답

JSON 데이터를 점진적으로 스트림으로 전송하고 싶다면, `streamJson` 메서드를 사용할 수 있습니다. 이 방식은 브라우저로 대용량 데이터를 점진적으로 전송하고, JavaScript에서 바로 파싱할 수 있게 할 때 유용합니다.

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 [useStream 훅](#consuming-streamed-responses)과 거의 동일하지만, 스트리밍이 완료되면 데이터를 JSON으로 파싱하려 시도한다는 점이 다릅니다.

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
### 이벤트 스트림(SSE)

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용하여 서버 센트 이벤트(Server-Sent Events, SSE) 스트림 응답을 생성합니다. 이 메서드는 클로저를 인수로 받아, [yield](https://www.php.net/manual/en/language.generators.overview.php)로 응답을 반환할 때마다 스트림으로 전송합니다.

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

이벤트의 이름을 직접 지정하고 싶다면, `StreamedEvent` 인스턴스를 `yield` 하면 됩니다.

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 사용하기

이벤트 스트림도 라라벨의 `stream` npm 패키지를 사용해 쉽게 소비할 수 있습니다. 먼저, 아래와 같이 패키지를 설치하세요.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

이후 `useEventStream` 훅을 사용해 이벤트 스트림을 구독하세요. 스트림 URL을 지정하면, 메시지가 수신될 때마다 `message`에 이어 받아 사용할 수 있습니다.

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

`useEventStream`의 두 번째 인수로 옵션 객체를 전달해, 스트림 소비 동작을 세부적으로 조정할 수 있습니다. 기본값은 아래와 같습니다.

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

이벤트 스트림은 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체를 직접 사용해 수동으로 소비할 수도 있습니다. 라라벨의 `eventStream` 메서드는 스트림 완료 시 자동으로 `</stream>` 업데이트를 전송합니다.

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

스트림에 전송할 마지막 이벤트를 커스터마이즈하고 싶다면, `eventStream`의 `endStreamWith` 인수에 `StreamedEvent` 인스턴스를 지정하세요.

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트림 다운로드

특정 작업의 결과 문자열을 파일로 저장하지 않고 바로 다운로드 가능한 응답으로 전환하고 싶을 때는, `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, 선택적 헤더 배열을 인수로 받습니다.

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

여러 라우트와 컨트롤러에서 재사용할 수 있는 커스텀 응답을 정의하고 싶다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드(예: `App\Providers\AppServiceProvider`)에서 호출하는 것이 좋습니다.

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

`macro` 함수는 첫 번째 인수로 매크로명, 두 번째 인수로 클로저를 받습니다. 매크로의 클로저는 `ResponseFactory` 구현체나 `response` 헬퍼에서 매크로명을 호출했을 때 실행됩니다.

```php
return response()->caps('foo');
```