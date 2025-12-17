# HTTP 응답 (HTTP Responses)

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가](#attaching-headers-to-responses)
    - [응답에 쿠키 추가](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리디렉션](#redirects)
    - [이름이 지정된 라우트로 리디렉션](#redirecting-named-routes)
    - [컨트롤러 액션으로 리디렉션](#redirecting-controller-actions)
    - [외부 도메인으로 리디렉션](#redirecting-external-domains)
    - [플래시 세션 데이터와 함께 리디렉션](#redirecting-with-flashed-session-data)
- [기타 응답 타입](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [스트리밍 응답](#streamed-responses)
    - [스트리밍 응답 활용하기](#consuming-streamed-responses)
    - [스트리밍 JSON 응답](#streamed-json-responses)
    - [이벤트 스트림 (SSE)](#event-streams)
    - [스트리밍 다운로드](#streamed-downloads)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성

<a name="strings-arrays"></a>
#### 문자열과 배열

모든 라우트와 컨트롤러에서는 사용자 브라우저로 전송할 응답을 반환해야 합니다. Laravel은 여러 가지 방식의 응답 반환을 지원합니다. 가장 기본적인 방식은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 이 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다.

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트나 컨트롤러에서 문자열을 반환하는 것 외에도, 배열을 반환할 수도 있습니다. 프레임워크는 배열을 자동으로 JSON 응답으로 변환합니다.

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/12.x/eloquent-collections)을 반환할 수도 있다는 사실을 알고 계셨나요? 이 경우에도 자동으로 JSON 응답으로 변환됩니다. 한 번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로 라우트 액션에서 단순한 문자열이나 배열만 반환하는 것은 드문 일입니다. 대신 대개 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/12.x/views)를 반환하게 됩니다.

전체 `Response` 인스턴스를 반환하면 HTTP 상태 코드 및 헤더를 더 세밀하게 커스터마이징할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 다양한 HTTP 응답 생성 메서드를 제공합니다.

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션

라우트나 컨트롤러에서 [Eloquent ORM](/docs/12.x/eloquent) 모델 및 컬렉션을 직접 반환할 수도 있습니다. 이 경우 Laravel은 모델과 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [hidden 속성](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)을 자동으로 적용하여 숨겨줍니다.

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가

대부분의 응답 메서드는 체이닝이 가능하므로 응답 인스턴스를 유연하게 구성할 수 있습니다. 예를 들어, `header` 메서드를 사용해 여러 개의 헤더를 응답에 추가할 수 있습니다.

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는 `withHeaders` 메서드를 사용해 배열 형태로 여러 헤더를 한 번에 추가할 수도 있습니다.

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

Laravel에는 `cache.headers` 미들웨어가 내장되어 있어, 여러 라우트에 대해 `Cache-Control` 헤더를 빠르게 설정할 수 있습니다. 지시어는 해당 cache-control 디렉티브에 해당하는 "스네이크 케이스" 형식으로 작성하며, 세미콜론(;)으로 구분해서 지정합니다. 만약 지시어에 `etag`가 포함되어 있다면, 응답 콘텐츠의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다.

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
### 응답에 쿠키 추가

`cookie` 메서드를 이용해 반환할 `Illuminate\Http\Response` 인스턴스에 쿠키를 추가할 수 있습니다. 이 메서드에는 쿠키 이름, 값, 유효 기간(분 단위)을 전달해야 합니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 추가적으로 자주 사용되지는 않지만, PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php)와 동일하게 여러 인수 값을 받을 수 있습니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

아직 응답 인스턴스가 없는 상황에서 미리 쿠키를 등록하고 싶다면, `Cookie` 파사드를 사용해 쿠키를 "큐"에 추가할 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 생성할 때 필요한 인수를 받습니다. 이렇게 등록된 쿠키는 응답이 브라우저로 전송되기 전에 자동으로 포함됩니다.

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성

나중에 응답 인스턴스에 붙이기 위해 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하고 싶다면, 전역 `cookie` 헬퍼 함수를 사용할 수 있습니다. 이렇게 생성한 쿠키는 직접 응답 인스턴스에 붙이지 않는 한 클라이언트에 전송되지 않습니다.

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료

응답의 `withoutCookie` 메서드를 사용해 쿠키를 만료시켜 삭제할 수 있습니다.

```php
return response('Hello World')->withoutCookie('name');
```

또한 응답 인스턴스가 없어도, `Cookie` 파사드의 `expire` 메서드를 사용해 쿠키를 만료시킬 수 있습니다.

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에, Laravel이 생성하는 모든 쿠키는 암호화되고 서명되어 클라이언트에서 변경하거나 읽을 수 없습니다. 애플리케이션에서 생성하는 쿠키 중 일부에 대해서만 암호화를 비활성화하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

> [!NOTE]
> 일반적으로 쿠키 암호화는 비활성화해서는 안 됩니다. 암호화를 끄면 클라이언트 측 데이터 노출이나 변조 위험에 노출될 수 있습니다.

<a name="redirects"></a>
## 리디렉션 (Redirects)

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 이동시키는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다.

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

특정 상황, 예를 들어 제출한 폼에 유효성 검증 오류가 있을 때 사용자를 이전 위치로 리디렉션하고 싶을 수 있습니다. 이럴 때는 전역 `back` 헬퍼 함수를 사용하면 됩니다. 이 기능은 [세션](/docs/12.x/session)을 활용하므로, `back` 함수를 호출하는 라우트에는 반드시 `web` 미들웨어 그룹이 적용되어야 합니다.

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검증...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리디렉션

파라미터 없이 `redirect` 헬퍼를 호출하면 `Illuminate\Routing\Redirector` 인스턴스를 반환합니다. 이를 통해 `Redirector` 인스턴스의 다양한 메서드를 사용할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리디렉션하려면 `route` 메서드를 사용합니다.

```php
return redirect()->route('login');
```

해당 라우트에 파라미터가 필요하다면, 두 번째 인수로 파라미터 배열을 전달할 수 있습니다.

```php
// 라우트 URI: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 자동 채우기

"ID" 파라미터가 있는 라우트로 리디렉션할 때, Eloquent 모델 인스턴스를 바로 전달할 수도 있습니다. 이 경우, ID 값은 자동으로 추출됩니다.

```php
// 라우트 URI: /profile/{id}

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 들어갈 값을 커스터마이즈하고 싶다면, 라우트 파라미터 정의에서 컬럼을 지정하거나(`/profile/{id:slug}`), Eloquent 모델의 `getRouteKey` 메서드를 오버라이드할 수 있습니다.

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

[컨트롤러 액션](/docs/12.x/controllers)으로 리디렉션을 생성할 수도 있습니다. 이때는 컨트롤러와 액션명을 `action` 메서드에 전달합니다.

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요하다면, 두 번째 인수로 전달할 수 있습니다.

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션

애플리케이션 외부의 도메인으로 리디렉션해야 하는 경우가 있습니다. 이때는 `away` 메서드를 사용하면, 추가적인 URL 인코딩이나 검증 없이 바로 외부 도메인으로 이동하는 `RedirectResponse`가 생성됩니다.

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 플래시 세션 데이터와 함께 리디렉션

보통 어떤 작업을 성공적으로 처리한 후, 성공 메시지를 세션에 플래시(일시 저장)하고 새로운 URL로 리디렉션하는 일이 많습니다. 편의를 위해, `RedirectResponse` 인스턴스를 생성하고 플래시 데이터를 한 번의 체이닝으로 세션에 저장할 수 있습니다.

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리디렉션된 후, [세션](/docs/12.x/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어 [Blade 문법](/docs/12.x/blade)에서는 다음과 같이 할 수 있습니다.

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리디렉션하기

`RedirectResponse` 인스턴스의 `withInput` 메서드를 사용해, 현재 요청의 입력 데이터를 세션에 플래시로 저장한 뒤 사용자를 새 위치로 리디렉션할 수 있습니다. 주로 유효성 검증 오류가 발생한 경우에 사용합니다. 입력 데이터가 세션에 저장된 후 다음 요청 때 [이 데이터를 손쉽게 가져와](/docs/12.x/requests#retrieving-old-input) 폼을 다시 채울 수 있습니다.

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼를 사용하면 다양한 타입의 응답 인스턴스를 생성할 수 있습니다. `response` 헬퍼를 인수 없이 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [계약](/docs/12.x/contracts) 구현체가 반환되며, 여러 편리한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드와 헤더 제어가 필요하면서, 동시에 [뷰](/docs/12.x/views)를 응답 내용으로 반환하려면 `view` 메서드를 사용하면 됩니다.

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

만약 커스텀 HTTP 상태 코드나 헤더를 따로 지정할 필요가 없다면, 전역 `view` 헬퍼 함수를 사용해도 됩니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 `application/json`으로 자동 설정하며, 전달된 배열을 PHP의 `json_encode` 함수로 JSON으로 변환합니다.

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 생성하고 싶다면, `json` 메서드와 `withCallback` 메서드를 함께 사용할 수 있습니다.

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드는 지정된 경로의 파일을 사용자의 브라우저에 다운로드하도록 강제하는 응답을 생성합니다. 두 번째 인수로 파일명을 지정할 수 있으며, 사용자에게 다운로드될 때 보이는 파일명이 됩니다. 세 번째 인수로 HTTP 헤더 배열을 전달할 수도 있습니다.

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은 다운로드되는 파일의 파일명이 반드시 ASCII 문자만을 사용해야 함을 요구합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 이미지나 PDF 등 파일을 브라우저에서 바로 보여주도록 반환할 수 있습니다. 첫 번째 인수로 파일의 절대 경로, 두 번째 인수로 헤더 배열을 전달합니다.

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트리밍 응답

데이터가 생성되는 즉시 클라이언트로 스트리밍하면, 메모리 사용량을 크게 줄이고 특히 매우 큰 응답에서 성능을 향상시킬 수 있습니다. 스트리밍 응답을 사용하면 서버가 모든 데이터를 다 보내기 전에 클라이언트가 먼저 데이터를 처리할 수 있게 됩니다.

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // 청크 간 지연을 시뮬레이션...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

편의를 위해, `stream` 메서드에 전달한 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면, Laravel이 generator에서 반환된 문자열마다 자동으로 출력 버퍼를 플러시하고 Nginx의 출력 버퍼링도 비활성화합니다.

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
### 스트리밍 응답 활용하기

스트리밍 응답은 Laravel의 `stream` npm 패키지를 통해 소비할 수 있습니다. 이 패키지는 Laravel 응답 스트림 및 이벤트 스트림과 상호작용할 수 있는 편리한 API를 제공합니다. 사용하려면 우선 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치합니다.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

이후, `useStream`을 이용해 스트림을 소비할 수 있습니다. 스트림 URL을 전달하면, 해당 훅이 Laravel로부터 돌아온 콘텐츠를 실시간으로 합치며 `data` 값을 자동으로 갱신합니다.

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

`send`로 데이터를 보내면, 해당 스트림과의 기존 연결은 종료되고 새로 요청을 보냅니다. 모든 요청은 JSON 방식의 `POST`로 전송됩니다.

> [!WARNING]
> `useStream` 훅은 애플리케이션에 `POST` 요청을 보내기 때문에, 올바른 CSRF 토큰이 반드시 필요합니다. 가장 쉬운 방법은 [애플리케이션 레이아웃의 head에 메타 태그로 포함시키는 것](/docs/12.x/csrf#csrf-x-csrf-token)입니다.

`useStream`에 전달하는 두 번째 인수는 스트림 소비 행위를 커스터마이즈할 수 있는 옵션 객체이며, 기본값은 다음과 같습니다.

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

`onResponse`는 스트림에서 첫 응답을 성공적으로 받은 후 호출되며, 원본 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) 객체가 콜백에 전달됩니다. `onData`는 각 청크(chunk)를 받을 때마다 호출되며, 현재 청크가 콜백에 전달됩니다. `onFinish`는 스트림이 끝나거나 fetch/read 과정에서 에러가 발생했을 때 호출됩니다.

기본적으로 스트림을 초기화할 때는 요청이 자동으로 전송되지 않습니다. `initialInput` 옵션에 값을 넘기면 스트림이 초기화될 때 첫 페이로드를 전송할 수 있습니다.

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

스트림을 수동으로 취소하려면, 훅에서 반환된 `cancel` 메서드를 사용할 수 있습니다.

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

`useStream` 훅을 사용할 때마다 무작위로 생성된 `id`가 스트림을 식별하기 위해 사용되며, 각 요청마다 `X-STREAM-ID` 헤더로 전송됩니다. 여러 컴포넌트에서 같은 스트림을 소비하거나, 직접 `id`를 관리하고 싶다면 옵션을 지정할 수 있습니다.

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

대량의 데이터를 점진적으로 브라우저에 전송하면서 JavaScript로 쉽게 파싱되도록 하고 싶다면, `streamJson` 메서드를 사용할 수 있습니다. 이 메서드는 큰 데이터셋을 점진적으로 전송해야 하는 상황에 적합합니다.

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 [useStream 훅](#consuming-streamed-responses)과 거의 동일하지만, 스트리밍이 끝나면 데이터를 JSON으로 파싱하려고 시도합니다.

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

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입의 서버 전송 이벤트(SSE) 스트리밍 응답을 반환하는 데 사용할 수 있습니다. 이 메서드는 클로저를 받아, [yield](https://www.php.net/manual/en/language.generators.overview.php)로 반환할 이벤트를 스트림에 전달할 수 있습니다.

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

이벤트 이름을 커스터마이즈하고 싶다면, `StreamedEvent` 클래스의 인스턴스를 yield로 반환하면 됩니다.

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 소비하기

이벤트 스트림도 Laravel의 `stream` npm 패키지로 손쉽게 소비할 수 있습니다. 이 패키지로 Laravel 이벤트 스트림과 상호작용이 가능합니다. 우선 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치합니다.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

이후, `useEventStream`을 활용해 이벤트 스트림을 소비할 수 있습니다. 스트림 URL을 넘기면, 메시지 렌더링에 응답이 자동으로 이어 붙여집니다.

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

`useEventStream`의 두 번째 인수는 스트림 소비 동작을 커스터마이즈할 수 있는 옵션 객체로, 기본값 예시는 다음과 같습니다.

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

이벤트 스트림은 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체로 직접 소비할 수도 있습니다. `eventStream` 메서드는 스트림이 완료될 때 `</stream>` 업데이트 메시지를 자동으로 전송합니다.

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

마지막에 전송될 이벤트를 커스터마이즈하려면, `eventStream` 메서드의 `endStreamWith` 인수에 `StreamedEvent` 인스턴스를 넘길 수 있습니다.

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트리밍 다운로드

특정 작업의 문자열 결과를 디스크에 파일로 기록하지 않고 다운로드 가능한 응답으로 변환하고 싶을 때는 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, (옵션) 헤더 배열을 인수로 받습니다.

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

여러 라우트 및 컨트롤러에서 재사용할 수 있는 커스텀 응답을 만들고 싶다면, `Response` 파사드의 `macro` 메서드를 사용하세요. 이 메서드는 주로 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers), 예를 들어 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출하는 것이 일반적입니다.

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

`macro` 함수는 첫 번째 인수로 매크로의 이름을 받고, 두 번째 인수로 클로저를 받습니다. 매크로명으로 `ResponseFactory` 구현체나 `response` 헬퍼에서 호출할 수 있습니다.

```php
return response()->caps('foo');
```