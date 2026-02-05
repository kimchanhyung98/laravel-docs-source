# HTTP 응답 (HTTP Responses)

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리디렉션](#redirects)
    - [이름 있는 라우트로 리디렉션](#redirecting-named-routes)
    - [컨트롤러 액션으로 리디렉션](#redirecting-controller-actions)
    - [외부 도메인으로 리디렉션](#redirecting-external-domains)
    - [세션 플래시 데이터와 함께 리디렉션](#redirecting-with-flashed-session-data)
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
## 응답 생성 (Creating Responses)

<a name="strings-arrays"></a>
#### 문자열과 배열

모든 라우트와 컨트롤러에서는 사용자의 브라우저로 전송할 응답을 반환해야 합니다. Laravel은 여러 방식으로 응답을 반환하는 기능을 제공합니다. 가장 기본적인 방식은 라우트나 컨트롤러에서 단순히 문자열을 반환하는 것입니다. 이 경우 프레임워크가 자동으로 문자열을 HTTP 응답으로 변환합니다:

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트나 컨트롤러에서 문자열뿐만 아니라 배열도 반환할 수 있습니다. 이 경우, Laravel이 배열을 자동으로 JSON 응답으로 변환합니다:

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/master/eloquent-collections) 역시 반환할 수 있다는 사실을 알고 계셨나요? Eloquent 컬렉션도 자동으로 JSON으로 변환됩니다. 한 번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로 라우트 액션에서는 단순한 문자열이나 배열만 반환하는 것이 아니라, `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/master/views)를 반환하는 경우가 많습니다.

`Response` 인스턴스를 직접 반환하면 응답의 HTTP 상태 코드와 헤더를 자유롭게 조작할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하므로 HTTP 응답을 만들기 위한 다양한 메서드를 제공합니다:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션

[ORM Eloquent](/docs/master/eloquent)의 모델이나 컬렉션도 라우트와 컨트롤러에서 직접 반환할 수 있습니다. 이 경우, Laravel이 자동으로 해당 모델 또는 컬렉션을 JSON 응답으로 변환하며, 모델의 [hidden 속성](/docs/master/eloquent-serialization#hiding-attributes-from-json) 역시 올바르게 처리합니다:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 관련 메서드는 체이닝이 가능하여 유연하게 응답 인스턴스를 구성할 수 있습니다. 예를 들어, `header` 메서드를 사용하면 다양한 헤더를 응답에 순차적으로 추가할 수 있습니다:

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는, `withHeaders` 메서드를 사용해 여러 헤더를 배열로 한 번에 지정할 수 있습니다:

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

<a name="cache-control-middleware"></a>
#### Cache Control 미들웨어

Laravel에는 `cache.headers` 미들웨어가 내장되어 있어, 라우트 그룹에 `Cache-Control` 헤더를 빠르게 설정할 수 있습니다. 지시어는 각 cache-control 디렉티브의 "snake case" 형태로, 세미콜론으로 구분하여 지정합니다. 만약 지시어 목록에 `etag`가 포함되어 있다면 응답 내용의 MD5 해시가 ETag 식별자로 자동 설정됩니다:

```php
Route::middleware('cache.headers:public;max_age=30;s_maxage=300;stale_while_revalidate=600;etag')->group(function () {
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

`Illuminate\Http\Response` 인스턴스의 `cookie` 메서드를 사용하여 응답에 쿠키를 추가할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 적용 시간을(분 단위로) 전달해야 합니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수와 유사하게, 추가적인 인수를 더 받을 수 있습니다. 일반적으로 이 인수들은 PHP의 setcookie 함수와 같은 의도와 의미를 가집니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

응답 인스턴스가 아직 없다면, `Cookie` 파사드를 통해 "큐"(queue) 형태로 쿠키를 등록하고, 실제 응답이 전송될 때 쿠키가 첨부되게 할 수도 있습니다. `queue` 메서드는 쿠키 인스턴스 생성을 위해 필요한 인수들을 받습니다. 이렇게 큐에 등록된 쿠키는 브라우저로 전송되는 응답에 자동으로 첨부됩니다:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기

추후에 응답 인스턴스에 첨부할 쿠키를 미리 `Symfony\Component\HttpFoundation\Cookie` 인스턴스로 만들고 싶다면, 전역 `cookie` 헬퍼를 사용하면 됩니다. 이렇게 생성한 쿠키는 응답 인스턴스에 첨부되어야만 클라이언트로 전송됩니다:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료시키기

`withoutCookie` 메서드를 이용하여 응답에서 해당 이름의 쿠키를 미리 만료시키면 쿠키를 삭제할 수 있습니다:

```php
return response('Hello World')->withoutCookie('name');
```

응답 인스턴스가 없는 경우에는 `Cookie` 파사드의 `expire` 메서드를 사용하여 쿠키를 만료시킬 수 있습니다:

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로, `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에 Laravel에서 생성되는 모든 쿠키는 암호화 및 서명되어 클라이언트에 의해 조작되거나 읽힐 수 없습니다. 애플리케이션에서 일부 쿠키에 대해 암호화를 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용하면 됩니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

> [!NOTE]
> 일반적으로 쿠키 암호화는 절대 비활성화해서는 안 됩니다. 암호화를 끄면 쿠키가 클라이언트에서 쉽게 노출되거나 조작될 위험이 있습니다.

<a name="redirects"></a>
## 리디렉션 (Redirects)

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스입니다. 이 객체는 사용자를 다른 URL로 리디렉션하는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있지만, 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

폼 제출이 유효하지 않을 때 등, 사용자를 이전 위치로 리디렉션하고 싶을 때는 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/master/session)을 활용하므로, 해당 라우트가 `web` 미들웨어 그룹을 사용하도록 설정했는지 확인하세요:

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검증 등...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름 있는 라우트로 리디렉션

`redirect` 헬퍼를 아무 인수 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환됩니다. 따라서 다양한 `Redirector` 메서드를 연달아 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리디렉션하려면 `route` 메서드를 사용하세요:

```php
return redirect()->route('login');
```

만약 라우트에 파라미터가 필요하다면, 두 번째 인수에 배열로 전달하면 됩니다:

```php
// URI가 /profile/{id}인 라우트의 경우

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델로 파라미터 채우기

ID 파라미터가 Eloquent 모델에서 직접 추출될 경우, 모델 인스턴스를 바로 전달할 수 있습니다. 이때 ID 값이 자동으로 추출됩니다:

```php
// URI가 /profile/{id}인 라우트의 경우

return redirect()->route('profile', [$user]);
```

라우트 파라미터로 전달할 값을 커스터마이징하고 싶다면, 라우트 파라미터 정의에서 사용하는 컬럼을 지정하거나(`/profile/{id:slug}`), Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드하면 됩니다:

```php
/**
 * 모델의 라우트 키 값을 반환
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리디렉션

[컨트롤러 액션](/docs/master/controllers)으로 리디렉션하고 싶다면, `action` 메서드에 컨트롤러와 액션명을 배열로 전달하세요:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요하다면, 두 번째 인수에 배열로 지정할 수 있습니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션

애플리케이션 외부의 도메인으로도 리디렉션이 가능합니다. 이때는 추가적인 URL 인코딩이나 유효성 검증 없이, `away` 메서드를 사용하면 됩니다:

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 세션 플래시 데이터와 함께 리디렉션

새로운 URL로의 리디렉션과 [세션에 데이터 플래시](/docs/master/session#flash-data)는 한 번에 이루어지는 경우가 많습니다. 일반적으로 작업이 성공적으로 수행된 후, 세션에 성공 메시지를 플래시할 때 이런 방식이 사용됩니다. 편의를 위해, 하나의 메서드 체이닝으로 `RedirectResponse` 인스턴스 생성과 세션 데이터 플래시를 할 수 있습니다:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리디렉트된 후에는 [세션](/docs/master/session)에서 플래시된 메시지를 출력할 수 있습니다. 예를 들어, [Blade 문법](/docs/master/blade)을 사용해서 다음과 같이 표시할 수 있습니다:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리디렉션

`RedirectResponse` 인스턴스의 `withInput` 메서드를 사용하면, 현재 요청의 입력값을 세션에 플래시하여 다음 요청에서 폼을 쉽게 재구성할 수 있습니다. 보통 유효성 검증에 실패했을 때 사용됩니다. 플래시된 입력값은 다음 요청에서 [손쉽게 조회](/docs/master/requests#retrieving-old-input)할 수 있습니다:

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입 (Other Response Types)

`response` 헬퍼를 사용하면 다양한 타입의 응답 인스턴스를 생성할 수 있습니다. `response` 헬퍼를 인수 없이 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/master/contracts)의 구현체를 반환합니다. 이 컨트랙트는 유용한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드와 헤더를 직접 제어하면서 [뷰](/docs/master/views)를 콘텐츠로 반환하고 싶다면, `view` 메서드를 사용하세요:

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

HTTP 상태 코드나 커스텀 헤더가 필요 없다면, 전역 `view` 헬퍼 함수만 단독으로 사용해도 됩니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 자동으로 `Content-Type` 헤더를 `application/json`으로 설정하며, 전달된 배열을 PHP의 `json_encode` 함수로 JSON 문자열로 변환합니다:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답이 필요하다면, `json` 메서드와 함께 `withCallback` 메서드를 체이닝해서 사용할 수 있습니다:

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드를 이용하면 사용자의 브라우저가 지정된 경로의 파일을 강제로 다운로드하도록 응답을 생성할 수 있습니다. 두 번째 인수로 파일명을 전달하면, 다운로드 시 사용자에게 보여질 파일명이 결정됩니다. 세 번째 인수로는 HTTP 헤더 배열을 지정할 수 있습니다:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은 다운로드 파일의 파일명이 반드시 ASCII 문자로만 이루어져야 함을 요구합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드를 이용하면 이미지나 PDF와 같이 브라우저에서 바로 렌더링할 수 있는 파일을 직접 표시할 수 있습니다(다운로드가 아니라). 이 메서드는 첫 번째 인수로 파일의 절대 경로, 두 번째 인수로 헤더 배열을 받습니다:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트림 응답 (Streamed Responses)

데이터가 생성되는 즉시 클라이언트로 스트리밍하여, 대용량 응답에서도 서버 메모리 사용량을 크게 줄이고 응답 성능을 높일 수 있습니다. 스트림 응답에서는 서버가 모든 데이터를 전송하기 전에 클라이언트가 데이터를 받기 시작할 수 있습니다:

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // 청크 사이의 지연을 시뮬레이션
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

또한, `stream` 메서드에 전달하는 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면, Laravel이 자동으로 청크 문자열 반환 시마다 출력 버퍼를 플러시하고, Nginx 출력 버퍼링도 비활성화해줍니다:

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
### 스트림 응답 소비하기

스트림 응답은 Laravel의 `stream` npm 패키지를 이용하여 쉽게 사용 가능합니다. 이 패키지는 Laravel의 응답 및 이벤트 스트림과 상호작용할 수 있는 편리한 API를 제공합니다. 시작하려면 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

이후, `useStream` 훅을 사용해 이벤트 스트림을 구독할 수 있습니다. 스트림 URL만 지정하면, 콘텐츠가 반환될 때마다 `data` 값이 자동으로 업데이트됩니다:

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

`send`를 사용해 데이터를 스트림으로 전송하면, 이전 활성화된 연결은 취소됩니다. 모든 데이터 요청은 JSON 포맷의 `POST` 요청으로 전송됩니다.

> [!WARNING]
> `useStream` 훅이 애플리케이션에 `POST` 요청을 보내므로, 유효한 CSRF 토큰이 필요합니다. 가장 쉬운 방법은 [애플리케이션 레이아웃의 head 태그에 메타 태그로 포함](/docs/master/csrf#csrf-x-csrf-token)하는 것입니다.

`useStream`의 두 번째 인자는 옵션 객체로, 스트림 소비 동작을 커스터마이즈할 수 있습니다. 이 객체의 기본값은 아래와 같습니다:

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

`onResponse`는 스트림에서 최초 응답을 성공적으로 수신했을 때 호출되며, 원시 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) 객체를 전달합니다. `onData`는 각 청크를 받을 때마다 호출되어 해당 데이터를 전달하고, `onFinish`는 스트림이 종료될 때와 fetch/읽기 사이클 중 에러 발생 시 호출됩니다.

기본적으로, 스트림 연결 시 즉시 데이터 요청이 전송되지 않습니다. `initialInput` 옵션을 사용하여 스트림 시작 시 초기 페이로드를 보낼 수 있습니다:

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

스트림을 수동으로 취소하려면 훅에서 반환된 `cancel` 메서드를 사용할 수 있습니다:

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

`useStream` 훅이 호출될 때마다, 스트림을 식별할 수 있는 임의의 `id`가 생성되어 각 요청의 `X-STREAM-ID` 헤더에 포함됩니다. 여러 컴포넌트에서 동일한 스트림을 소비하려면, 직접 `id`를 지정해 읽기/쓰기가 가능합니다:

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

대량의 데이터를 자바스크립트에서 손쉽게 파싱 가능한 JSON 형태로 점진적으로 전송하고 싶다면, `streamJson` 메서드를 사용할 수 있습니다. 이 메서드는 대용량 데이터셋을 점진적으로 브라우저에 전송할 때 특히 유용합니다:

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 [useStream 훅](#consuming-streamed-responses)과 동일하게 동작하지만, 스트리밍 종료 후 데이터를 JSON으로 파싱하는 점만 다릅니다:

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

`eventStream` 메서드를 사용하여 `text/event-stream` 콘텐츠 타입의 서버 전송 이벤트(SSE) 스트림 방식 응답을 반환할 수 있습니다. 이 메서드에는 응답 데이터를 스트림에 [yield](https://www.php.net/manual/en/language.generators.overview.php)하는 클로저를 전달하면 됩니다:

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

이벤트의 이름을 커스터마이징하고 싶다면, `StreamedEvent` 인스턴스를 yield 하면 됩니다:

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 소비하기

이벤트 스트림은 Laravel의 `stream` npm 패키지를 통해 편리하게 구독할 수 있습니다. `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

`useEventStream` 훅을 사용해 이벤트 스트림을 받아올 수 있습니다. 스트림 URL만 지정하면, 메시지가 반환될 때마다 `message`가 자동으로 업데이트됩니다:

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

`useEventStream`의 두 번째 인자는 옵션 객체로, 스트림 소비 방식을 커스터마이즈할 수 있습니다. 기본값은 아래와 같습니다:

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

이벤트 스트림은 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체로 직접 구독할 수도 있습니다. `eventStream` 메서드는 스트림 완료 시 자동으로 `</stream>` 이벤트를 전송합니다:

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

이벤트 스트림에 마지막으로 전송될 이벤트를 커스터마이즈하고 싶다면, `eventStream` 메서드의 `endStreamWith` 인수에 `StreamedEvent` 인스턴스를 전달하세요:

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트림 다운로드

특정 연산의 문자열 결과를 별도의 파일로 저장하지 않고, 곧바로 다운로드 응답으로 전환하고 싶을 때는 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, (선택적으로) 헤더 배열을 인수로 받습니다:

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

여러 라우트나 컨트롤러에서 재사용할 수 있는 커스텀 응답을 정의하고 싶다면, `Response` 파사드의 `macro` 메서드를 사용하세요. 이 메서드는 보통 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드에서 호출합니다. 예를 들어 `App\Providers\AppServiceProvider`에서 다음과 같이 작성할 수 있습니다:

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

`macro` 함수는 첫 번째 인수로 이름, 두 번째 인수로 클로저를 받습니다. 정의한 매크로는 `ResponseFactory` 구현체나 `response` 헬퍼를 통해 사용 가능합니다:

```php
return response()->caps('foo');
```