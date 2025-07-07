# HTTP 응답 (HTTP Responses)

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리다이렉트](#redirects)
    - [이름이 지정된 라우트로 리다이렉트](#redirecting-named-routes)
    - [컨트롤러 액션으로 리다이렉트](#redirecting-controller-actions)
    - [외부 도메인으로 리다이렉트](#redirecting-external-domains)
    - [세션 데이터와 함께 리다이렉트](#redirecting-with-flashed-session-data)
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

모든 라우트와 컨트롤러는 사용자 브라우저로 보낼 응답을 반환해야 합니다. 라라벨은 응답을 반환하는 여러 가지 방법을 제공합니다. 가장 기본적인 방식은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크가 이 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다.

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트나 컨트롤러에서 문자열뿐만 아니라 배열을 반환할 수도 있습니다. 이 경우 프레임워크가 배열을 자동으로 JSON 응답으로 변환해줍니다.

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/12.x/eloquent-collections)도 반환할 수 있다는 사실, 알고 계셨나요? 이 경우에도 자동으로 JSON으로 변환됩니다. 한번 사용해 보세요!

<a name="response-objects"></a>
#### 응답 객체

실제로는 라우트 액션에서 단순한 문자열이나 배열만 반환하는 경우보다, `Illuminate\Http\Response` 인스턴스 또는 [뷰](/docs/12.x/views)를 반환하는 경우가 더 많습니다.

전체 `Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 자유롭게 지정할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, HTTP 응답을 다양한 방식으로 구성할 수 있는 여러 메서드를 제공합니다.

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델 및 컬렉션

[엘로퀀트 ORM](/docs/12.x/eloquent) 모델이나 컬렉션을 라우트나 컨트롤러에서 직접 반환할 수도 있습니다. 이 경우에도 라라벨이 모델과 컬렉션을 자동으로 JSON 응답으로 변환해주며, 모델의 [숨겨진 속성](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)은 노출하지 않습니다.

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 메서드는 메서드 체이닝이 가능합니다. 이를 이용하면 응답 인스턴스를 유연하게 조합할 수 있습니다. 예를 들어, `header` 메서드를 사용하면 응답에 여러 헤더를 추가한 뒤 사용자에게 보낼 수 있습니다.

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또한, `withHeaders` 메서드를 사용하면 배열로 여러 헤더를 한 번에 지정할 수도 있습니다.

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

라라벨에는 `cache.headers` 미들웨어가 기본 제공되어, 라우트 그룹에 대해 `Cache-Control` 헤더를 빠르게 설정할 수 있습니다. 캐시-컨트롤 지시어는 스네이크 케이스(snake case)로 제공하며, 각 지시어는 세미콜론(;)으로 구분합니다. 목록에 `etag`를 포함하면, 응답 내용의 MD5 해시가 자동으로 ETag 식별자로 추가됩니다.

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

`cookie` 메서드를 사용하면 나가는 `Illuminate\Http\Response` 인스턴스에 쿠키를 첨부할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 유효기간(분 단위)을 전달해야 합니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 추가적으로 몇 가지 다양한 인자도 받을 수 있으며, 이 인자들은 PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수와 동일한 역할 및 의미를 가집니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

응답 인스턴스가 아직 없지만, 향후 응답에 쿠키가 포함되도록 미리 지정하고 싶다면, `Cookie` 파사드를 사용해 쿠키를 "큐잉"할 수 있습니다. `queue` 메서드는 쿠키 인스턴스 생성을 위한 인자를 그대로 전달받습니다. 이렇게 큐에 추가된 쿠키는 응답이 브라우저로 전송되기 전에 응답에 자동으로 추가됩니다.

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 직접 생성

나중에 응답 인스턴스에 첨부할 수 있도록 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 직접 생성하고 싶다면, 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이렇게 생성된 쿠키는 응답 인스턴스에 첨부하지 않는 한 클라이언트에 전송되지 않습니다.

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료

응답의 `withoutCookie` 메서드를 사용하면 특정 쿠키를 만료시켜(삭제하여) 제거할 수 있습니다.

```php
return response('Hello World')->withoutCookie('name');
```

아직 응답 인스턴스가 없는 경우에는, `Cookie` 파사드의 `expire` 메서드를 이용해 쿠키를 만료시킬 수 있습니다.

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로는 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에 라라벨에서 생성된 모든 쿠키는 암호화되고 서명되어, 클라이언트가 그 내용을 수정하거나 읽을 수 없습니다. 만약 여러분의 애플리케이션에서 생성하는 일부 쿠키의 암호화를 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php`에서 `encryptCookies` 메서드를 사용할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

<a name="redirects"></a>
## 리다이렉트

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 이동시키는 데 필요한 헤더를 포함합니다. `RedirectResponse` 인스턴스는 여러 가지 방법으로 생성할 수 있는데, 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다.

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때때로 사용자가 이전 페이지로 돌아가도록 리다이렉트해야 할 수도 있습니다. 예를 들어, 폼 제출이 유효하지 않은 경우입니다. 전역 `back` 헬퍼 함수를 사용하면 사용자를 이전 위치로 간편하게 리다이렉트할 수 있습니다. 이 기능은 [세션](/docs/12.x/session)을 활용하기 때문에, `back` 함수를 호출하는 라우트가 반드시 `web` 미들웨어 그룹을 사용해야 합니다.

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검사 등...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리다이렉트

`redirect` 헬퍼를 인자 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스를 반환하므로, `Redirector` 인스턴스의 다양한 메서드를 이어서 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리다이렉트 응답을 생성하려면 `route` 메서드를 사용하세요.

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요한 경우, `route` 메서드의 두 번째 인자로 전달할 수 있습니다.

```php
// 예: 라우트의 URI가 /profile/{id}인 경우

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델로 파라미터 지정

만약 "ID" 파라미터가 Eloquent 모델에서 추출되어야 한다면, 모델 객체 자체를 전달하면 됩니다. 라라벨이 모델에서 ID를 자동으로 추출합니다.

```php
// 예: 라우트의 URI가 /profile/{id}인 경우

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 설정될 값을 직접 지정하고 싶다면, 라우트 파라미터 정의에서 컬럼명을 직접 명시할 수 있습니다 (`/profile/{id:slug}`와 같이). 또는, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드해서 원하는 값을 반환하도록 할 수도 있습니다.

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

[컨트롤러 액션](/docs/12.x/controllers)으로 리다이렉트를 생성할 수도 있습니다. 이때는 컨트롤러와 액션명을 `action` 메서드에 전달하면 됩니다.

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요한 경우, 두 번째 인자로 전달하면 됩니다.

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리다이렉트

애플리케이션 외부의 도메인으로 리다이렉트해야 할 경우, `away` 메서드를 사용하면 추가적인 URL 인코딩, 검증 혹은 확인 없이 `RedirectResponse`를 생성할 수 있습니다.

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 세션 데이터와 함께 리다이렉트

새 URL로 리다이렉트하면서 [세션에 데이터를 플래시](/docs/12.x/session#flash-data)하는 경우가 일반적입니다. 보통 작업을 성공적으로 처리한 후, 성공 메시지를 세션에 저장(플래시)하고 리다이렉트하곤 합니다. 편의를 위해, `RedirectResponse` 인스턴스를 생성하면서 플루언트하게 세션에 데이터를 플래시할 수 있습니다.

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리다이렉트 된 후, [세션](/docs/12.x/session)에서 플래시된 메시지를 블레이드 구문 등으로 출력할 수 있습니다.

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력 값과 함께 리다이렉트

리다이렉트 응답 인스턴스의 `withInput` 메서드를 사용하면 현재 요청의 입력 데이터를 세션에 플래시한 뒤 사용자를 새 위치로 리다이렉트할 수 있습니다. 주로 유효성 검증 오류가 발생했을 때 사용하며, 이후 요청에서 [이전 입력값을 쉽게 가져와](/docs/12.x/requests#retrieving-old-input), 폼을 다시 채울 수 있습니다.

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼는 다양한 타입의 응답 인스턴스를 생성하는 데 사용할 수 있습니다. 아무 인자 없이 호출하면, `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/12.x/contracts)를 구현한 인스턴스를 반환합니다. 이 컨트랙트는 여러 편리한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드와 헤더를 직접 지정해야 하면서, 동시에 [뷰](/docs/12.x/views)를 응답 본문으로 반환하고 싶다면 `view` 메서드를 사용하세요.

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

만약 HTTP 상태 코드와 헤더를 지정할 필요가 없다면, 전역 `view` 헬퍼 함수로도 충분합니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 지정하며, 주어진 배열을 PHP `json_encode` 함수로 JSON으로 변환해 응답합니다.

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 생성하고 싶을 때는, `json` 메서드와 함께 `withCallback` 메서드를 사용할 수 있습니다.

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드를 사용하면 주어진 경로의 파일을 사용자의 브라우저에서 강제로 다운로드하도록 응답을 생성할 수 있습니다. `download`의 두 번째 인자로 파일 이름을 지정할 수 있고, 다운로드시 사용자에게 보이는 파일명이 결정됩니다. 마지막으로 HTTP 헤더 배열을 세 번째 인자로 전달할 수 있습니다.

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은, 다운로드하는 파일의 파일명이 ASCII로 되어 있어야 합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 이미지를 비롯한 파일(PDF 등)을 사용자의 브라우저에 바로 표시(다운로드가 아닌)할 때 사용할 수 있습니다. 첫 번째 인자로는 파일의 절대 경로를, 두 번째 인자로 헤더 배열을 넘길 수 있습니다.

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트림 응답

데이터를 생성하면서 곧바로 클라이언트로 전송하면, 메모리 사용량을 크게 줄이고 성능을 개선할 수 있습니다. 특히 매우 크기가 큰 응답의 경우 효과적입니다. 스트림 응답을 사용하면 서버가 모든 데이터를 보내기 전에, 클라이언트가 먼저 데이터를 받기 시작할 수 있습니다.

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // 청크 간 지연을 시뮬레이션합니다...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

편의를 위해, `stream` 메서드에 전달된 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면, 라라벨이 자동으로 각 문자열 사이에서 출력 버퍼를 플러시하고, Nginx 출력 버퍼링도 비활성화합니다.

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
### 스트림 응답 소비하기

스트림 응답은 Laravel의 `stream` npm 패키지를 사용해 소비할 수 있으며, 라라벨 응답 및 이벤트 스트림에 편리하게 접근하도록 API를 제공합니다. 우선 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치해야 합니다.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

그 다음, `useStream`을 사용해 스트림 이벤트를 소비할 수 있습니다. 스트림 URL을 지정하면, 해당 Hook이 응용 프로그램에서 반환되는 컨텐츠를 스트림으로 받아와 `data`에 누적 업데이트합니다.

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

`send`를 통해 스트림에 데이터를 전송할 때마다, 기존 스트림 연결이 취소되고 새로운 데이터가 전송됩니다. 모든 요청은 JSON `POST` 방식으로 전송됩니다.

> [!WARNING]
> `useStream` 훅은 애플리케이션에 `POST` 요청을 보내므로, 유효한 CSRF 토큰이 필요합니다. CSRF 토큰을 제공하는 가장 쉬운 방법은 [애플리케이션 레이아웃의 head에 meta 태그로 포함하는 것](/docs/12.x/csrf#csrf-x-csrf-token)입니다.

`useStream`의 두 번째 인자로 전달하는 옵션 객체를 활용해, 스트림 소비 동작을 커스터마이즈할 수 있습니다. 기본값은 아래와 같습니다.

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

`onResponse`는 스트림에서 초기 응답을 성공적으로 받은 직후 호출되며, 해당 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) 객체가 콜백에 전달됩니다. `onData`는 각 청크가 도착할 때마다 호출되며, 현재 청크가 콜백으로 넘어옵니다. `onFinish`는 스트림이 종료될 때, 혹은 fetch/읽기 도중 에러가 발생할 때 호출됩니다.

기본적으로 스트림 초기화 시에는 요청이 바로 전송되지 않습니다. 만약 스트림에 기본 페이로드를 전달하고 싶다면 `initialInput` 옵션을 사용할 수 있습니다.

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

`useStream` 훅이 사용될 때마다 스트림을 식별하는 무작위 `id`가 생성되며, 각 요청 시 `X-STREAM-ID` 헤더로 서버에 전달됩니다. 여러 컴포넌트에서 동일한 스트림을 소비할 때는, 직접 `id`를 지정해주면 같은 스트림에 접근할 수 있습니다.

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

대용량 데이터를 점진적으로 브라우저에 전송해야 하는 경우, `streamJson` 메서드를 사용할 수 있습니다. 이 메서드는 대량의 데이터를 자바스크립트에서 쉽게 파싱할 수 있는 형식으로 점진적으로 전송해야 할 때 특히 유용합니다.

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 [useStream 훅](#consuming-streamed-responses)과 동일하게 동작하지만, 스트리밍이 끝난 후 데이터를 JSON으로 파싱한다는 점이 다릅니다.

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
### 이벤트 스트림(Event Streams, SSE)

`eventStream` 메서드를 사용하면 `text/event-stream` 콘텐츠 타입을 이용한 서버 전송 이벤트(Server-Sent Events, SSE) 스트리밍 응답을 반환할 수 있습니다. `eventStream` 메서드에는 클로저를 인자로 전달하며, 이 클로저는 응답을 사용할 수 있게 될 때마다 [yield](https://www.php.net/manual/en/language.generators.overview.php)로 스트림에 데이터를 추가해야 합니다.

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

이벤트의 이름을 커스터마이즈하고 싶다면, `StreamedEvent` 클래스의 인스턴스를 `yield`하면 됩니다.

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 소비(Consuming Event Streams)

이벤트 스트림은 라라벨의 `stream` npm 패키지를 사용하여 소비할 수 있습니다. 이 패키지는 라라벨 이벤트 스트림과 쉽게 상호작용할 수 있는 편리한 API를 제공합니다. 먼저, `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치합니다.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

그 다음, `useEventStream` 훅을 사용하여 이벤트 스트림을 소비할 수 있습니다. 스트림 URL을 제공하면, 훅이 Laravel 애플리케이션으로부터 반환받은 응답을 합쳐서 `message` 값을 자동으로 업데이트합니다.

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

`useEventStream`에 두 번째 인자로 옵션 객체를 전달하면, 스트림 소비 동작을 세부적으로 조정할 수 있습니다. 이 객체의 기본값은 아래와 같습니다.

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

이벤트 스트림은 애플리케이션의 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체를 이용해 직접 수동으로 소비할 수도 있습니다. 스트림이 완료되면, `eventStream` 메서드는 자동으로 스트림에 `</stream>` 업데이트를 전송합니다.

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

스트림에 전송되는 마지막 이벤트를 커스터마이즈하려면, `eventStream` 메서드의 `endStreamWith` 인자에 `StreamedEvent` 인스턴스를 제공할 수 있습니다.

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트리밍 다운로드

때때로 어떤 작업의 문자열 결과를 파일로 저장하지 않고도 다운로드 응답으로 전환하고 싶은 경우가 있습니다. 이럴 때 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, 그리고 선택적으로 헤더 배열을 인자로 받습니다.

```php
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
        ->contents()
        ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a name="response-macros"></a>
## 응답 매크로(Response Macros)

여러 라우트와 컨트롤러에서 재사용할 수 있는 커스텀 응답을 정의하고 싶다면, `Response` 파사드에서 `macro` 메서드를 사용할 수 있습니다. 보통 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) 중 하나의 `boot` 메서드에서 호출하는 것이 좋습니다. 예를 들어 `App\Providers\AppServiceProvider` 서비스 프로바이더를 사용할 수 있습니다.

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

`macro` 함수는 첫 번째 인자로 이름, 두 번째 인자로 클로저를 받습니다. 매크로의 클로저는 `ResponseFactory` 구현체나 `response` 헬퍼에서 매크로 이름으로 호출할 때 실행됩니다.

```php
return response()->caps('foo');
```