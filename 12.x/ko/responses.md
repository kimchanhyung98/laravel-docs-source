# HTTP 응답 (HTTP Responses)

- [응답 생성하기](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리디렉션](#redirects)
    - [네임드 라우트로 리디렉션](#redirecting-named-routes)
    - [컨트롤러 액션으로 리디렉션](#redirecting-controller-actions)
    - [외부 도메인으로 리디렉션](#redirecting-external-domains)
    - [세션 데이터와 함께 리디렉션](#redirecting-with-flashed-session-data)
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
## 응답 생성하기

<a name="strings-arrays"></a>
#### 문자열과 배열

모든 라우트와 컨트롤러는 사용자의 브라우저로 전송될 응답을 반환해야 합니다. 라라벨에서는 여러 방법으로 응답을 반환할 수 있습니다. 가장 기본적인 방법은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 이 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다.

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열뿐만 아니라 배열을 반환할 수도 있습니다. 배열을 반환하면 프레임워크가 자동으로 배열을 JSON 응답으로 변환합니다.

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/12.x/eloquent-collections)도 반환할 수 있다는 사실, 알고 계셨나요? 자동으로 JSON으로 변환됩니다. 한 번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로는 라우트 액션에서 단순한 문자열이나 배열만 반환하지 않고, `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/12.x/views)를 반환하게 됩니다.

완전한 `Response` 인스턴스를 반환하면, 응답의 HTTP 상태 코드와 헤더를 자유롭게 커스터마이즈할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 다양한 방법으로 HTTP 응답을 만들 수 있는 여러 메서드를 제공합니다.

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션

[엘로퀀트 ORM](/docs/12.x/eloquent) 모델과 컬렉션도 라우트나 컨트롤러에서 직접 반환할 수 있습니다. 이 경우 라라벨은 모델과 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [숨김 속성](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)도 자동으로 반영됩니다.

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 메서드는 체이닝이 가능하여, 응답 인스턴스를 유연하게 구성할 수 있습니다. 예를 들어, 응답을 사용자에게 돌려주기 전에 `header` 메서드를 사용해 여러 헤더를 추가할 수 있습니다.

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는, `withHeaders` 메서드를 사용하여 한 번에 여러 헤더를 배열로 지정할 수도 있습니다.

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

라라벨에는 `cache.headers` 미들웨어가 포함되어 있어, 라우트 그룹에 대해 `Cache-Control` 헤더를 간편하게 설정할 수 있습니다. 각 디렉티브는 관련된 cache-control 명령을 "스네이크 케이스(snake case)"로 입력하며, 각 디렉티브는 세미콜론으로 구분합니다. 만약 `etag`을 지정하면, 응답 내용의 MD5 해시를 ETag 식별자로 자동 설정합니다.

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

`Illuminate\Http\Response` 인스턴스에서 `cookie` 메서드를 이용해 쿠키를 응답에 첨부할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 그리고 쿠키가 유효한 분(minute) 단위를 전달해야 합니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 더 많은 인자를 받을 수도 있습니다. 일반적으로 이 인자들은 PHP의 내장 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수에서 사용되는 인자와 비슷한 역할을 합니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

아직 응답 인스턴스가 없는 상태에서 쿠키를 응답에 반드시 포함시키고 싶다면, `Cookie` 파사드를 사용해서 쿠키를 "큐(queue)"에 담을 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 만드는 데 필요한 인자들을 받아들이며, 응답을 브라우저에 전송하기 전에 해당 쿠키가 자동으로 포함됩니다.

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기

나중에 응답 인스턴스에 첨부할 수 있도록 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 직접 만들고 싶다면, 글로벌 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 응답 인스턴스에 추가되지 않는 한 클라이언트에게 전송되지 않습니다.

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료(삭제)

출력 응답에서 `withoutCookie` 메서드를 이용해 쿠키를 만료시켜 삭제할 수 있습니다.

```php
return response('Hello World')->withoutCookie('name');
```

아직 응답 인스턴스가 없다면, `Cookie` 파사드의 `expire` 메서드를 사용해서 쿠키를 만료시킬 수 있습니다.

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로 라라벨의 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에, 라라벨에서 생성하는 모든 쿠키는 암호화 및 서명되어 클라이언트가 쿠키를 읽거나 변조하지 못하게 보호됩니다. 만약 애플리케이션에서 일부 쿠키에 대해 암호화를 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

<a name="redirects"></a>
## 리디렉션

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리디렉션하는 데 필요한 적절한 헤더를 포함합니다. 여러 방법으로 `RedirectResponse` 인스턴스를 생성할 수 있습니다. 가장 간단한 방법은 글로벌 `redirect` 헬퍼를 사용하는 것입니다.

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

제출한 폼이 유효하지 않은 경우와 같이, 사용자를 이전 위치로 리디렉션하고 싶을 때가 있습니다. 이때는 글로벌 `back` 헬퍼 함수를 이용할 수 있습니다. 이 기능은 [세션](/docs/12.x/session)을 사용하므로, `back` 함수를 호출하는 라우트에서 반드시 `web` 미들웨어 그룹을 사용해야 합니다.

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 네임드 라우트로 리디렉션

`redirect` 헬퍼를 파라미터 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어 Redirector의 다양한 메서드를 사용할 수 있습니다. 예를 들어, 네임드 라우트로 리디렉션하려면 `route` 메서드를 사용할 수 있습니다.

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요한 경우, `route` 메서드의 두 번째 인자로 전달할 수 있습니다.

```php
// 해당 URI: /profile/{id} 인 라우트

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 이용한 파라미터 전달

"ID" 파라미터와 같이 Eloquent 모델에서 값을 가져와 라우트에 전달하려면, 그냥 모델 인스턴스를 전달해주면 됩니다. 라라벨이 자동으로 ID 값을 추출해서 파라미터로 사용합니다.

```php
// 해당 URI: /profile/{id} 인 라우트

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 원하는 값을 직접 지정하고 싶다면, 라우트 파라미터 정의에서 컬럼명을 명시적으로 지정하거나(`/profile/{id:slug}`), Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드하면 됩니다.

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

[컨트롤러 액션](/docs/12.x/controllers)으로 리디렉션하려면, 컨트롤러와 액션명을 `action` 메서드에 전달하면 됩니다.

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요한 경우, 두 번째 인자로 전달할 수 있습니다.

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션

때로는 애플리케이션 외부의 도메인으로 리디렉션해야 할 때가 있습니다. 이럴 때는 추가적인 URL 인코딩, 검증 또는 확인 없이 `RedirectResponse`를 생성하는 `away` 메서드를 사용할 수 있습니다.

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 세션 데이터와 함께 리디렉션

새 URL로 리디렉션하면서 [데이터를 세션에 플래시](/docs/12.x/session#flash-data)하는 경우가 많습니다. 보통 어떤 작업을 성공적으로 처리한 뒤, 성공 메시지를 세션에 저장할 때 사용합니다. 이를 편리하게 하기 위해, 하나의 체이닝 메서드로 `RedirectResponse` 인스턴스 생성과 세션 데이터 플래시를 동시에 처리할 수 있습니다.

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리디렉션된 이후에는 [세션](/docs/12.x/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어, [Blade 문법](/docs/12.x/blade)으로 다음과 같이 사용할 수 있습니다.

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리디렉션

사용자가 폼 유효성 검사에 실패한 경우처럼, 리디렉션 전에 현재 요청의 입력값을 세션에 플래시하려면 `RedirectResponse`의 `withInput` 메서드를 사용하면 됩니다. 이렇게 입력값을 세션에 저장해두면, 다음 요청에서 [입력값을 쉽게 가져와](/docs/12.x/requests#retrieving-old-input) 폼을 자동으로 다시 채워줄 수 있습니다.

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼는 다양한 타입의 응답 인스턴스를 생성하는 데 사용할 수 있습니다. `response` 헬퍼를 인자 없이 호출하면, `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/12.x/contracts)의 구현체가 반환됩니다. 이 컨트랙트는 여러 유용한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드와 헤더를 직접 제어하면서, [뷰](/docs/12.x/views)를 응답 내용으로 반환하려면 `view` 메서드를 사용합니다.

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

만약 커스텀 HTTP 상태 코드나 헤더가 필요 없다면, 글로벌 `view` 헬퍼 함수를 그대로 사용할 수 있습니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드를 사용하면 `Content-Type` 헤더가 `application/json`으로 자동 설정되고, 전달한 배열을 PHP의 `json_encode` 함수로 JSON 형태로 변환합니다.

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 만들고 싶다면, `json` 메서드를 사용한 뒤 `withCallback` 메서드를 함께 사용할 수 있습니다.

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드는 지정한 경로의 파일을 사용자 브라우저가 바로 다운로드하도록 하는 응답을 생성합니다. 두 번째 인자로는 사용자가 내려받을 파일의 표시 이름을 지정할 수 있고, 마지막 세 번째 인자로는 HTTP 헤더 배열을 전달할 수 있습니다.

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은, 다운로드하려는 파일의 이름이 반드시 ASCII 문자여야 한다는 점에 유의하세요.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 파일(예: 이미지, PDF 등)을 다운로드하지 않고 사용자의 브라우저에서 바로 표시하도록 응답을 생성합니다. 이 메서드는 첫 번째 인자로 파일의 절대 경로, 두 번째 인자로 헤더 배열을 받습니다.

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트림 응답

서버가 데이터를 생성하는 즉시 클라이언트로 스트리밍하면, 메모리 사용량을 크게 줄이고 속도를 높일 수 있습니다. 스트림 응답을 사용하면, 서버가 모든 데이터를 전송하기 전에도 클라이언트가 미리 데이터를 처리할 수 있습니다.

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

편의를 위해, `stream` 메서드에 전달하는 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환할 경우, 라라벨이 자동으로 각 제너레이터 반환값마다 출력 버퍼를 플러시하고, Nginx의 출력 버퍼링도 비활성화합니다.

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

라라벨의 `stream` npm 패키지를 사용하면, 라라벨 응답 및 이벤트 스트림과 쉽게 상호작용할 수 있는 편리한 API를 제공합니다. 먼저, `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

이후, `useStream`을 이용하여 이벤트 스트림을 소비할 수 있습니다. 스트림의 URL만 전달하면, 훅이 라라벨 애플리케이션에서 콘텐츠가 반환될 때마다 `data`를 자동으로 갱신해줍니다.

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

스트림에 데이터를 다시 전달할 때는 `send`를 사용하며, 기존 연결이 취소되고 새로운 POST JSON 요청이 전송됩니다.

> [!WARNING]
> `useStream` 훅은 애플리케이션에 `POST` 요청을 보내기 때문에, 유효한 CSRF 토큰이 필요합니다. 가장 쉬운 설정 방법은 [애플리케이션 레이아웃의 head에 `meta` 태그로 토큰을 삽입하는 것](/docs/12.x/csrf#csrf-x-csrf-token)입니다.

`useStream`에 전달하는 두 번째 인자는 옵션 객체로, 스트림 소비 동작을 커스터마이즈할 수 있습니다. 기본 옵션 값은 아래와 같습니다.

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

`onResponse`는 스트림에서 최초 응답이 성공적으로 반환된 후 트리거되며, 원시 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) 객체를 콜백에 전달합니다. `onData`는 각 청크를 받을 때마다 호출되며, 해당 청크 값을 전달합니다. `onFinish`는 스트림이 정상적으로 끝날 때와 fetch/read 과정 중 에러가 발생할 때 모두 호출됩니다.

기본적으로, 스트림은 초기화 시 자동으로 요청을 전송하지 않습니다. 스트림으로 최초 데이터를 전송하려면 `initialInput` 옵션에 페이로드를 전달하면 됩니다.

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

`useStream` 훅이 호출될 때마다 스트림을 식별하는 랜덤 `id`가 생성되어 요청의 `X-STREAM-ID` 헤더에 포함되어 전송됩니다. 여러 컴포넌트에서 동일한 스트림을 소비할 때는, 동일한 `id`를 직접 전달하면 같은 스트림을 읽고 쓸 수 있습니다.

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

JSON 데이터를 점진적으로(순차적으로) 스트리밍해야 하는 경우, `streamJson` 메서드를 사용할 수 있습니다. 이 메서드는 특히 대용량 데이터를 점진적으로 브라우저에 전송해야 할 때 유용하며, JavaScript에서 쉽게 파싱할 수 있는 포맷으로 데이터를 제공합니다.

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 [`useStream` 훅](#consuming-streamed-responses)과 동일하게 동작하지만, 스트림이 완료되면 데이터를 JSON으로 파싱한다는 점이 다릅니다.

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

`eventStream` 메서드를 사용하면 `text/event-stream` 컨텐츠 타입을 이용하여 서버-전송 이벤트(Server-Sent Events, SSE) 스트림 응답을 반환할 수 있습니다. `eventStream` 메서드는 클로저를 인자로 받고, 이 클로저는 [yield](https://www.php.net/manual/en/language.generators.overview.php) 키워드를 통해 응답이 준비되는 대로 스트림에 데이터를 보낼 수 있습니다.

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

이벤트의 이름을 커스텀하고 싶다면, `StreamedEvent` 클래스의 인스턴스를 `yield`할 수 있습니다.

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 소비(Consuming Event Streams)

이벤트 스트림은 라라벨의 `stream` npm 패키지를 이용해 소비할 수 있으며, 이 패키지는 라라벨 이벤트 스트림과 상호작용하기 위한 편리한 API를 제공합니다. 먼저 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치합니다.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

이제 스트림 URL을 제공하고, `useEventStream` 훅을 사용해 이벤트 스트림을 소비할 수 있습니다. 스트림에서 메시지가 반환될 때마다 훅은 응답을 자동으로 합쳐서 `message` 값에 반영합니다.

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

`useEventStream`에 두 번째 인자로 옵션 객체를 전달하여 스트림 처리 방식을 커스터마이즈할 수 있습니다. 이 객체의 기본값은 아래와 같습니다.

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

이벤트 스트림은 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체를 통해 직접 소비할 수도 있습니다. `eventStream` 메서드는 스트림이 완료될 때 자동으로 `</stream>` 업데이트를 이벤트 스트림에 전송합니다.

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

최종 이벤트로 전송되는 데이터를 커스터마이즈하려면, `eventStream` 메서드의 `endStreamWith` 인자에 `StreamedEvent` 인스턴스를 전달할 수 있습니다.

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트리밍 다운로드

특정 작업의 문자열 응답을 디스크에 저장하지 않고 바로 다운로드 가능한 응답으로 만들고 싶은 경우가 있습니다. 이럴 때는 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, 그리고 선택적으로 헤더 배열을 인수로 받습니다.

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

다양한 라우트와 컨트롤러에서 반복적으로 사용할 수 있는 사용자 정의 응답을 정의하고 싶다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 보통 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers), 예를 들어 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

`macro` 함수는 첫 번째 인수로 이름, 두 번째 인수로 클로저를 받습니다. 이후 `ResponseFactory` 구현체나 `response` 헬퍼에서 매크로 이름을 호출하면 이 클로저가 실행됩니다.

```php
return response()->caps('foo');
```