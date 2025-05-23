# HTTP 응답 (HTTP Responses)

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리디렉션](#redirects)
    - [이름이 지정된 라우트로 리디렉션](#redirecting-named-routes)
    - [컨트롤러 액션으로 리디렉션](#redirecting-controller-actions)
    - [외부 도메인으로 리디렉션](#redirecting-external-domains)
    - [세션 데이터 플래시와 함께 리디렉션](#redirecting-with-flashed-session-data)
- [기타 응답 타입](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [스트림 응답](#streamed-responses)
    - [스트림 응답 소비하기](#consuming-streamed-responses)
    - [스트림 JSON 응답](#streamed-json-responses)
    - [이벤트 스트림(SSE)](#event-streams)
    - [스트림 다운로드](#streamed-downloads)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성

<a name="strings-arrays"></a>
#### 문자열과 배열

모든 라우트와 컨트롤러는 사용자의 브라우저로 다시 전송될 응답을 반환해야 합니다. 라라벨에서는 여러 방식으로 응답을 반환할 수 있습니다. 가장 기본적인 방법은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크가 해당 문자열을 자동으로 전체 HTTP 응답으로 변환해 줍니다:

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열뿐 아니라 배열을 반환할 수도 있습니다. 배열을 반환하면 프레임워크가 해당 배열을 자동으로 JSON 응답으로 변환합니다:

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/12.x/eloquent-collections)을 직접 반환할 수 있다는 것을 알고 계셨나요? 컬렉션도 자동으로 JSON으로 변환됩니다. 한 번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

실제 개발에서는 라우트 액션에서 단순한 문자열이나 배열만 반환하는 경우는 드뭅니다. 대부분은 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/12.x/views)를 반환하게 됩니다.

전체 `Response` 인스턴스를 반환하면, 응답의 HTTP 상태 코드와 헤더를 자유롭게 지정할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 다양한 HTTP 응답을 만들기 위한 여러 메서드를 제공합니다:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션

[엘로퀀트 ORM](/docs/12.x/eloquent) 모델이나 컬렉션을 라우트 또는 컨트롤러에서 직접 반환할 수도 있습니다. 이렇게 반환하면 라라벨에서 모델과 컬렉션을 자동으로 JSON 응답으로 변환하고, 모델의 [숨김 속성](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)도 적절히 처리합니다:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 메서드는 체이닝이 가능해서, 응답 인스턴스를 유연하게 만들 수 있습니다. 예를 들어, `header` 메서드를 사용해 응답에 여러 헤더를 추가할 수 있습니다:

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또한, `withHeaders` 메서드를 이용해 배열 형태로 여러 헤더를 한 번에 지정할 수도 있습니다:

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

라라벨에는 `cache.headers` 미들웨어가 내장되어 있어 라우트 그룹에 대해 `Cache-Control` 헤더를 간편하게 지정할 수 있습니다. 지시자는 해당 명령문의 "snake case" 버전으로 작성하며, 세미콜론으로 구분합니다. 만약 `etag`를 지시자 목록에 포함시키면 응답 내용의 MD5 해시값이 ETag 식별자로 자동 적용됩니다:

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

`Illuminate\Http\Response` 인스턴스의 `cookie` 메서드를 사용하여 응답에 쿠키를 추가할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 유효 기간(분 단위)을 전달하면 됩니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 이외에도 종종 사용되지 않는 몇 가지 추가 인수를 받을 수 있습니다. 일반적으로 해당 인수들은 PHP의 기본 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수의 인수와 동일한 목적과 의미를 가집니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

아직 응답 인스턴스가 없는 상황에서, 쿠키가 나가는 응답에 꼭 포함되도록 하고 싶다면, `Cookie` 파사드를 활용해 쿠키를 "queue" 할 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 만드는 데 필요한 인수들을 받아, 해당 쿠키를 응답이 전송되기 전에 자동으로 추가합니다:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기

나중에 응답 인스턴스에 첨부할 수 있도록 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하고 싶다면, 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이렇게 생성된 쿠키 인스턴스는 응답 객체에 붙이지 않는 한 클라이언트로 전송되지 않습니다:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 즉시 만료 처리

`withoutCookie` 메서드를 활용해, 나가는 응답에서 쿠키를 만료 처리하여 삭제할 수 있습니다:

```php
return response('Hello World')->withoutCookie('name');
```

아직 응답 인스턴스가 없는 경우에는, `Cookie` 파사드의 `expire` 메서드를 이용하여 쿠키를 만료시키면 됩니다:

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에, 라라벨이 생성한 모든 쿠키는 암호화 및 서명되어, 클라이언트가 쿠키 값을 임의로 변경하거나 읽을 수 없도록 보호됩니다. 애플리케이션에서 일부 쿠키에 대해 암호화를 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용하면 됩니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

<a name="redirects"></a>
## 리디렉션

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 이동시키는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때때로, 사용자를 이전 페이지로 되돌리고 싶을 때가 있습니다. 예를 들어, 사용자가 입력한 폼 데이터가 유효하지 않은 경우가 그렇습니다. 이때는 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/12.x/session)을 내부적으로 사용하므로, `back` 함수를 호출하는 라우트는 반드시 `web` 미들웨어 그룹을 사용해야 합니다:

```php
Route::post('/user/profile', function () {
    // 요청 검증...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리디렉션

`redirect` 헬퍼를 파라미터 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어, 다양한 메서드를 체이닝해서 사용할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리디렉션하려면 `route` 메서드를 사용합니다:

```php
return redirect()->route('login');
```

만약 해당 라우트가 파라미터를 요구한다면, 두 번째 인수로 전달할 수 있습니다:

```php
// 이 라우트의 URI가 /profile/{id}일 때

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델로 라우트 파라미터 채우기

라우트의 "ID" 파라미터가 Eloquent 모델에서 채워지는 경우, 파라미터에 모델 인스턴스 자체를 바로 전달할 수 있습니다. 이 경우, ID가 자동으로 추출되어 사용됩니다:

```php
// 이 라우트의 URI가 /profile/{id}일 때

return redirect()->route('profile', [$user]);
```

만약 라우트 파라미터에 들어갈 값을 직접 커스터마이징하고 싶다면, 라우트 파라미터 정의에서 컬럼을 명시하거나(`/profile/{id:slug}`), Eloquent 모델의 `getRouteKey` 메서드를 재정의하면 됩니다:

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
### 컨트롤러 액션으로 리디렉션

[컨트롤러 액션](/docs/12.x/controllers)으로 리디렉션을 생성할 수도 있습니다. 이를 위해선 컨트롤러와 액션명을 `action` 메서드에 전달하면 됩니다:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트가 파라미터를 요구한다면, `action` 메서드의 두 번째 인수에 파라미터 배열을 전달하면 됩니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션

가끔은 애플리케이션 외부의 도메인으로 리디렉션해야 할 때가 있습니다. 이럴 땐 `away` 메서드를 사용하면, 추가적인 URL 인코딩, 검증 또는 확인 작업 없이 곧바로 `RedirectResponse`를 생성합니다:

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 세션 데이터 플래시와 함께 리디렉션

새 URL로 리디렉션과 동시에 [세션에 데이터를 플래시](/docs/12.x/session#flash-data)하는 작업은 보통 함께 이루어집니다. 예를 들어, 어떤 작업이 성공적으로 끝난 뒤 성공 메시지를 세션에 플래시하는 경우가 많습니다. 라라벨에서는 리디렉션 응답을 생성할 때 플래시 데이터도 한 번의 체인으로 편리하게 함께 지정할 수 있습니다:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리디렉션된 후 [세션](/docs/12.x/session)에 저장된 플래시 메시지를 아래처럼 [Blade 문법](/docs/12.x/blade)으로 표시할 수 있습니다:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리디렉션

`RedirectResponse` 인스턴스가 제공하는 `withInput` 메서드를 사용하면, 현재 요청의 입력값을 세션에 플래시한 뒤 사용자를 새 위치로 리디렉션할 수 있습니다. 일반적으로 유효성 검증에 실패했을 때 입력값을 유지하고자 할 때 사용합니다. 입력값이 세션에 플래시되면, 이후 요청에서 [해당 값을 쉽게 가져와](/docs/12.x/requests#retrieving-old-input) 폼을 다시 채울 수 있습니다:

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼는 다양한 종류의 응답 인스턴스를 생성할 때 사용할 수 있습니다. `response` 헬퍼를 인수 없이 호출하면, `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/12.x/contracts)의 구현체가 반환됩니다. 이 컨트랙트는 여러 유용한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드와 헤더도 설정하면서, 동시에 [뷰](/docs/12.x/views)를 응답 본문으로 반환하고 싶을 때는 `view` 메서드를 사용합니다:

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

물론, 따로 HTTP 상태 코드나 헤더를 지정하지 않아도 된다면 전역 `view` 헬퍼 함수를 사용할 수 있습니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 지정하고, 전달받은 배열을 PHP의 `json_encode` 함수로 JSON으로 변환합니다:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 만들어야 한다면, `json` 메서드와 `withCallback` 메서드를 함께 사용할 수 있습니다:

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드를 사용하면, 사용자의 브라우저로 해당 경로의 파일을 강제로 다운로드하게 할 수 있습니다. `download` 메서드는 두 번째 인수로 파일명을 받을 수 있는데, 이는 사용자가 다운로드 시 볼 파일명에 해당합니다. 마지막으로 세 번째 인수에는 HTTP 헤더 배열을 전달할 수 있습니다:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은 다운로드 대상으로 지정된 파일명이 반드시 ASCII 문자여야 함을 요구합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 이미지나 PDF와 같은 파일을 브라우저에서 바로 표시하고 싶을 때 사용할 수 있습니다(다운로드가 아니라 직접 표시). 이 메서드는 첫 번째 인수로 파일의 절대 경로를, 두 번째 인수로 헤더 배열을 받습니다:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트림 응답

데이터가 생성되는 즉시 스트리밍 방식으로 클라이언트에 전달하면, 메모리 사용량을 대폭 줄이고 (특히 대용량 응답의 경우) 성능을 크게 향상시킬 수 있습니다. 스트림 응답을 활용하면, 서버가 모든 데이터를 다 전송하기 전에 클라이언트에서 데이터를 바로 처리할 수 있습니다:

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // 청크 단위 전송 간의 지연을 시뮬레이션
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

더 편리하게 사용하려면 `stream` 메서드에 전달하는 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하게 할 수도 있습니다. 이렇게 하면 라라벨이 제너레이터에서 반환하는 문자열마다 자동으로 출력 버퍼를 비우고, Nginx의 출력 버퍼링도 비활성화해 줍니다:

```php
Route::get('/chat', function () {
    return response()->stream(function (): void {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```

<a name="consuming-streamed-responses"></a>
### 스트림 응답 소비하기

스트림 응답은 라라벨의 `stream` npm 패키지를 사용해 소비(수신)할 수 있습니다. 이 패키지는 라라벨의 응답/이벤트 스트림과 상호작용하는 편리한 API를 제공합니다. 먼저, 다음과 같이 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치합니다:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

설치 후에는 `useStream` 훅을 사용해 이벤트 스트림을 소비할 수 있습니다. 스트림 URL을 지정하고 나면, 이 훅이 라라벨 애플리케이션에서 반환되는 응답을 이어붙여 `data`에 자동으로 업데이트합니다:

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

`send`를 통해 데이터를 스트림에 다시 전송하면, 기존 연결은 취소되고 새로운 데이터가 전송됩니다. 모든 요청은 JSON `POST` 방식으로 전송됩니다.

`useStream`에 전달하는 두 번째 인수는 스트림 소비 동작을 커스터마이즈할 수 있는 옵션 객체입니다. 디폴트 값은 아래와 같습니다:

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

`onResponse`는 스트림에서 초기 응답을 성공적으로 받은 후에 호출되며, 원본 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) 객체가 콜백으로 전달됩니다. `onData`는 각 청크가 수신될 때마다 콜백이 호출되고, 해당 청크가 파라미터로 전달됩니다. `onFinish`는 스트림이 완료되거나 데이터를 읽는 도중 에러가 발생했을 때 호출됩니다.

기본적으로, 스트림 초기화시 즉시 요청을 보내지 않습니다. 스트림에 초깃값을 미리 전달하고 싶다면, `initialInput` 옵션을 사용할 수 있습니다:

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

스트림을 수동으로 취소하려면, 훅에서 반환된 `cancel` 메서드를 사용할 수 있습니다:

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

`useStream` 훅을 사용할 때마다 무작위 `id`가 생성되며, 각 요청마다 `X-STREAM-ID` 헤더에 이 값이 함께 전송됩니다. 만약 여러 컴포넌트에서 같은 스트림을 공유하고 싶다면, 직접 `id`를 지정해서 읽기/쓰기를 수행할 수 있습니다:

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

JSON 데이터를 점진적으로 스트리밍해야 할 경우, `streamJson` 메서드를 사용할 수 있습니다. 이 방법은 대용량 데이터셋을 자바스크립트에서 쉽게 파싱할 수 있는 형식으로 브라우저에 점진적으로 전송하려고 할 때 특히 유용합니다.

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 [`useStream` 훅](#consuming-streamed-responses)과 동일하게 동작하지만, 스트리밍이 끝나면 데이터를 JSON으로 파싱하려고 시도한다는 점이 다릅니다.

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

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용해 서버 전송 이벤트(Server-Sent Events, SSE) 기반의 스트리밍 응답을 반환하는 데 사용합니다. 이 메서드는 클로저를 인수로 받으며, 스트림에 응답이 준비될 때마다 [yield](https://www.php.net/manual/en/language.generators.overview.php) 키워드로 데이터를 스트림에 추가해야 합니다.

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

이벤트의 이름을 커스터마이즈하고 싶다면, `StreamedEvent` 클래스의 인스턴스를 yield할 수 있습니다.

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 사용하기

이벤트 스트림은 라라벨의 `stream` npm 패키지를 사용해 소비할 수 있습니다. 이 패키지는 라라벨 이벤트 스트림과 상호작용할 수 있는 편리한 API를 제공합니다. 우선, `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

그런 다음, `useEventStream` 훅을 사용해 이벤트 스트림을 구독할 수 있습니다. 스트림 URL을 전달하면, 해당 훅은 라라벨 애플리케이션에서 메시지가 반환될 때마다 응답을 이어붙여 `message` 값을 자동으로 업데이트합니다.

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

`useEventStream`의 두 번째 인수로 옵션 객체를 전달하여 스트림 수신 동작을 커스터마이즈할 수 있습니다. 해당 옵션의 기본값은 다음과 같습니다.

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

이벤트 스트림은 애플리케이션 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체를 통해서도 수동으로 소비할 수 있습니다. `eventStream` 메서드는 스트림이 완료되면 자동으로 `</stream>`을 이벤트 스트림에 전송합니다.

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

이벤트 스트림에 마지막으로 전송되는 이벤트를 커스터마이즈하려면, `StreamedEvent` 인스턴스를 `eventStream` 메서드의 `endStreamWith` 인수에 전달하면 됩니다.

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트리밍 다운로드

어떤 작업의 결과 문자열을 디스크에 따로 저장하지 않고, 바로 다운로드 가능한 응답으로 전환하고 싶을 때가 있습니다. 이럴 때는 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, 그리고 옵션으로 헤더 배열을 인수로 받습니다.

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

여러 라우트와 컨트롤러에서 재사용할 수 있는 사용자 정의 응답을 정의하고 싶다면, `Response` 파사드에서 `macro` 메서드를 사용할 수 있습니다. 일반적으로는 애플리케이션의 [서비스 제공자](/docs/12.x/providers) 중 하나, 예를 들면 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 이 메서드를 호출해야 합니다.

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

`macro` 함수는 첫 번째 인수로 이름을, 두 번째 인수로 클로저를 받습니다. 이렇게 등록해두면, `ResponseFactory` 구현체나 `response` 헬퍼에서 매크로 이름을 호출할 때 해당 클로저가 실행됩니다.

```php
return response()->caps('foo');
```