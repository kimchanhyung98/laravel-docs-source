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
    - [뷰(View) 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [스트리밍 응답](#streamed-responses)
    - [스트리밍 응답 소비하기](#consuming-streamed-responses)
    - [스트리밍 JSON 응답](#streamed-json-responses)
    - [이벤트 스트림(SSE)](#event-streams)
    - [스트리밍 다운로드](#streamed-downloads)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성

<a name="strings-arrays"></a>
#### 문자열 및 배열

모든 라우트와 컨트롤러는 사용자의 브라우저로 전송할 응답을 반환해야 합니다. Laravel에서는 다양한 방식으로 응답을 반환할 수 있습니다. 가장 기본적인 방법은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 자동으로 문자열을 전체 HTTP 응답으로 변환합니다.

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트 및 컨트롤러에서 문자열 외에도 배열을 반환할 수 있습니다. 배열을 반환하면 프레임워크가 자동으로 배열을 JSON 응답으로 변환합니다.

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> [Eloquent 컬렉션](/docs/12.x/eloquent-collections)도 라우트나 컨트롤러에서 반환할 수 있다는 사실을 알고 계셨나요? 반환 시 자동으로 JSON으로 변환됩니다. 직접 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로 라우트 액션에서 단순 문자나 배열만 반환하는 경우는 드뭅니다. 대신 전체 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/12.x/views)를 반환하게 됩니다.

`Response` 인스턴스를 반환하면 HTTP 상태 코드 및 헤더를 다양하게 커스텀할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, HTTP 응답을 구성하기 위한 다양한 메서드를 제공합니다.

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델 및 컬렉션

[Eloquent ORM](/docs/12.x/eloquent) 모델이나 컬렉션도 라우트나 컨트롤러에서 직접 반환할 수 있습니다. 이 경우 Laravel은 모델과 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [숨김 속성](/docs/12.x/eloquent-serialization#hiding-attributes-from-json) 규칙을 존중합니다.

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가

대부분의 응답 메서드는 체이닝이 가능하므로, 응답 인스턴스를 유연하게 생성할 수 있습니다. 예를 들어, `header` 메서드로 응답을 사용자에게 전송하기 전에 여러 헤더를 연속적으로 추가할 수 있습니다.

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는, `withHeaders` 메서드를 사용해 여러 헤더를 한 번에 배열로 추가할 수 있습니다.

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

Laravel에는 `cache.headers` 미들웨어가 포함되어 있어서, 라우트 그룹에 대해 `Cache-Control` 헤더를 손쉽게 설정할 수 있습니다. 지시어는 캐시 컨트롤 지시어와 동일한 "snake case" 키워드를 사용하고, 세미콜론(;)으로 구분합니다. `etag` 지시어를 사용하면, 응답 내용의 MD5 해시가 자동으로 ETag 식별자로 지정됩니다.

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
### 응답에 쿠키 추가

`Illuminate\Http\Response` 인스턴스에 `cookie` 메서드를 사용해 쿠키를 첨부할 수 있습니다. 이 메서드에는 쿠키 이름, 값, 쿠키 유효 기간(분 단위)을 전달해야 합니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 추가적으로 여러 인자를 더 받을 수 있으며, 이들은 PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수 인자와 목적 및 의미가 같습니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

아직 응답 인스턴스가 없는 상황에서 쿠키를 응답에 첨부하려면, `Cookie` 파사드를 사용해 쿠키를 "큐잉"할 수 있습니다. `queue` 메서드에 쿠키 정보들을 전달하면, 생성되는 쿠키가 곧 전송될 응답에 자동으로 첨부됩니다.

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성

나중에 응답 인스턴스에 첨부할 수 있도록 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하고자 한다면, 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이렇게 생성된 쿠키는 응답에 첨부하지 않는 한 클라이언트에 전송되지 않습니다.

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료

`withoutCookie` 메서드를 사용해 응답에서 쿠키를 만료(삭제)시킬 수 있습니다.

```php
return response('Hello World')->withoutCookie('name');
```

응답 인스턴스가 없는 경우, `Cookie` 파사드의 `expire` 메서드를 사용해 쿠키를 만료시킬 수 있습니다.

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

Laravel의 모든 쿠키는 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에 기본적으로 암호화 및 서명되어, 클라이언트가 내용을 읽거나 수정하지 못하게 보호됩니다. 만약 일부 쿠키에 대해서는 암호화 적용을 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 이용해 예외 리스트를 지정할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

<a name="redirects"></a>
## 리디렉션

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자가 다른 URL로 이동할 수 있도록 필요한 헤더를 포함합니다. `RedirectResponse` 인스턴스는 다양한 방법으로 생성할 수 있습니다. 가장 단순한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다.

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

경우에 따라 사용자를 이전 위치로 되돌리고 싶을 때도 있습니다. 예를 들어, 제출된 폼의 유효성 검증에 실패했을 때 등입니다. 이 경우 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/12.x/session)을 활용하므로, 해당 라우트는 `web` 미들웨어 그룹을 사용해야 합니다.

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리디렉션

`redirect` 헬퍼를 인자 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어, 이 인스턴스의 다양한 메서드를 사용할 수 있습니다. 예를 들어, 라우트의 이름을 이용해 리디렉션하려면 `route` 메서드를 사용합니다.

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요한 경우, 두 번째 인자로 파라미터 배열을 전달할 수 있습니다.

```php
// 다음과 같은 URI를 가진 라우트: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 이용한 파라미터 자동 지정

"ID" 파라미터가 있는 라우트로 리디렉션할 때 Eloquent 모델 인스턴스를 직접 전달할 수 있습니다. 이 경우 id 값이 자동 추출되어 적용됩니다.

```php
// 다음과 같은 URI를 가진 라우트: /profile/{id}

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 적용되는 값을 커스터마이징하고 싶다면, 라우트 파라미터 정의(예: `/profile/{id:slug}`)에 컬럼명을 지정하거나, Eloquent 모델의 `getRouteKey` 메서드를 오버라이드할 수 있습니다.

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

[컨트롤러 액션](/docs/12.x/controllers)으로 리디렉션하는 것도 가능합니다. 이 경우 컨트롤러와 액션명을 `action` 메서드에 전달하면 됩니다.

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요한 경우, 두 번째 인자에 파라미터 배열을 전달합니다.

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션

애플리케이션 외부 도메인으로 리디렉션이 필요할 때도 있습니다. 이럴 때는 `away` 메서드를 사용하면, 추가적인 URL 인코딩이나 검증 없이 바로 외부 URL로 리디렉션됩니다.

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 플래시 세션 데이터와 함께 리디렉션

리디렉션과 동시에 [데이터를 세션에 플래시](/docs/12.x/session#flash-data)로 저장하는 경우가 흔합니다. 일반적으로 어떤 작업을 성공적으로 처리한 뒤, 성공 메시지를 세션에 플래시하여 사용자가 다음 페이지에서 메시지를 볼 수 있게 합니다. 이 경우, `RedirectResponse` 인스턴스를 생성하고, `with` 메서드 체이닝만으로 동시 처리가 가능합니다.

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리디렉션된 후에는 [세션](/docs/12.x/session)에 저장된 플래시 메시지를 표시할 수 있습니다. 예를 들어, [Blade 문법](/docs/12.x/blade)으로 다음과 같이 출력할 수 있습니다.

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력 값과 함께 리디렉션

`RedirectResponse` 인스턴스의 `withInput` 메서드를 이용해, 현재 요청의 입력값을 세션에 플래시로 남긴 뒤, 사용자를 새로운 위치로 리디렉션할 수 있습니다. 이는 보통 유효성 검증 오류가 발생했을 때 활용하며, 플래시된 입력값은 다음 요청에서 [간편하게 조회](/docs/12.x/requests#retrieving-old-input)하여 폼을 재구성할 때 사용할 수 있습니다.

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼는 여러 종류의 응답 인스턴스를 생성할 수 있습니다. `response` 헬퍼를 인수 없이 호출하면, `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/12.x/contracts) 구현체가 반환됩니다. 이 컨트랙트에는 다양한 편리한 응답 생성 메서드가 포함되어 있습니다.

<a name="view-responses"></a>
### 뷰(View) 응답

HTTP 상태 코드와 헤더를 직접 지정하면서도, [뷰](/docs/12.x/views)의 내용을 응답 본문으로 반환해야 한다면 `view` 메서드를 사용할 수 있습니다.

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

HTTP 상태 코드나 헤더를 직접 지정할 필요가 없다면, 전역 `view` 헬퍼를 간편하게 사용할 수 있습니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 설정하며, 전달된 배열을 `json_encode` PHP 함수로 변환하여 본문에 담습니다.

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 생성하고 싶다면, `json` 메서드와 `withCallback` 메서드를 조합할 수 있습니다.

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드는 지정한 경로의 파일을 사용자의 브라우저가 강제로 다운로드하게 하는 응답을 생성합니다. 두 번째 인자로 전달하는 파일명은 사용자가 받게 되는 파일 이름이 되며, 세 번째 인자로는 HTTP 헤더 배열을 추가할 수 있습니다.

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 담당하는 Symfony HttpFoundation은, 다운로드되는 파일명이 반드시 ASCII 문자로 되어 있기를 요구합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드를 사용하면, 예를 들어 이미지나 PDF 파일을 사용자 브라우저에 바로 표시할 수 있습니다(다운로드가 아닌). 이 메서드는 첫 번째 인자로 파일의 절대 경로, 두 번째 인자로 헤더 배열을 받습니다.

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트리밍 응답

서버에서 데이터를 바로 생성해 전송하는 스트리밍 방식을 사용하면, 메모리 사용량을 크게 줄이고 성능도 개선할 수 있습니다. 특히 대용량 응답을 빠르게 처리할 때 효과적입니다. 스트리밍 응답은 서버가 데이터를 다 전송하기 전에, 클라이언트가 수신된 데이터부터 바로 처리할 수 있게 해줍니다.

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // 각 청크 사이에 딜레이를 흉내냄...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

편의를 위해, `stream` 메서드에 제공하는 클로저에서 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면, Laravel이 제너레이터로부터 반환되는 각 문자열 사이에 출력 버퍼를 자동으로 플러시하고, Nginx의 출력 버퍼링도 비활성화합니다.

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
### 스트리밍 응답 소비하기

스트리밍 응답은 Laravel의 `stream` npm 패키지를 사용하면 손쉽게 사용할 수 있습니다. 이 패키지는 Laravel의 응답 및 이벤트 스트림과 상호작용하는 API를 제공합니다. 먼저 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치합니다.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

설치 후, `useStream`을 사용해 이벤트 스트림을 구독할 수 있습니다. 스트림 URL을 전달하면, Laravel 애플리케이션에서 데이터가 반환됨에 따라 `data`가 자동으로 누적되어 업데이트됩니다.

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

`send`를 통한 메시지 전송 시, 기존의 스트림 연결은 취소되고 새 요청이 전송됩니다. 모든 요청은 JSON 형식의 `POST`로 전송됩니다.

> [!WARNING]
> `useStream` 훅은 애플리케이션에 대해 `POST` 요청을 만들기 때문에, 올바른 CSRF 토큰이 필요합니다. 가장 쉬운 방법은 [애플리케이션 레이아웃의 head에 meta 태그로 CSRF 토큰을 포함](/docs/12.x/csrf#csrf-x-csrf-token)하는 것입니다.

`useStream`의 두 번째 인자는 옵션 객체로, 스트림 동작을 커스터마이즈할 수 있습니다. 이 객체의 기본값 예시는 아래와 같습니다.

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

`onResponse`는 스트림에서 초기 응답을 정상적으로 받은 후, 해당 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) 객체를 콜백에 넘깁니다. `onData`는 각 청크를 받을 때마다, 현재 청크 데이터를 콜백에 전달합니다. `onFinish`는 스트림이 끝나거나 fetch/읽기 과정에서 에러가 발생했을 때 호출됩니다.

기본적으로 스트림이 초기화될 때 바로 요청이 발생하지 않습니다. 첫 요청의 페이로드를 미리 전달하려면 `initialInput` 옵션을 사용할 수 있습니다.

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

`useStream` 훅을 사용할 때마다 고유의 난수 `id`가 생성되어 스트림 식별자로 사용됩니다. 이 값은 매 요청마다 `X-STREAM-ID` 헤더로 서버에 전송됩니다. 동일 스트림을 여러 컴포넌트에서 소비하려면, id를 직접 지정하여 읽기/쓰기를 할 수 있습니다.

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

점진적으로 JSON 데이터를 브라우저로 스트리밍하기 원할 경우에는 `streamJson` 메서드를 사용할 수 있습니다. 이 메서드는 대용량 데이터셋을 단계적으로 JavaScript에서도 쉽게 파싱할 수 있는 형식으로 전송할 때 매우 유용합니다.

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 [useStream 훅](#consuming-streamed-responses)과 거의 동일하지만, 데이터를 모두 스트리밍 받은 후 JSON으로 파싱을 시도합니다.

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

`eventStream` 메서드를 통해 `text/event-stream` 타입으로 서버-센트 이벤트(SSE)를 반환할 수 있습니다. 이 메서드에는 클로저를 인자로 전달하며, 이 클로저 안에서 응답을 [yield](https://www.php.net/manual/en/language.generators.overview.php)로 차례차례 스트림에 보냅니다.

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

이벤트 이름을 커스터마이즈하고 싶다면, `StreamedEvent` 클래스의 인스턴스를 yield로 반환할 수 있습니다.

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 소비하기

이벤트 스트림 역시 Laravel의 `stream` npm 패키지로 쉽게 소비할 수 있습니다. 먼저 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

이후, `useEventStream`을 통해 이벤트 스트림을 소비할 수 있습니다. 스트림 URL을 지정하면, Laravel 애플리케이션에서 메시지가 반환될 때마다 `message`가 누적되어 업데이트됩니다.

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

`useEventStream`의 두 번째 인자는 스트림 소비 동작을 커스터마이즈할 수 있는 옵션 객체입니다. 기본값 예시는 아래와 같습니다.

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

이벤트 스트림은 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체를 이용해 프론트엔드에서 직접 소비할 수도 있습니다. `eventStream` 메서드는 스트림 완료 시 자동으로 `</stream>`을 이벤트로 보내줍니다.

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

마지막 이벤트를 직접 지정해 이벤트 스트림에 보낼 수도 있습니다. `eventStream`의 `endStreamWith` 인자에 `StreamedEvent` 인스턴스를 전달하세요.

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트리밍 다운로드

특정 작업의 문자열 결과물을 디스크에 직접 저장하지 않고, 곧바로 다운로드로 전환해 사용자에게 제공하고 싶은 경우 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, 선택적으로 헤더 배열을 인자로 받습니다.

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

여러 라우트와 컨트롤러에서 재사용 가능한 커스텀 응답을 정의하고 싶다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) 중 하나(예: `App\Providers\AppServiceProvider`)의 `boot` 메서드 안에서 호출합니다.

```php
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

`macro` 함수는 첫 번째 인자로 이름을, 두 번째 인자로 클로저를 받습니다. 이 매크로 이름을 `ResponseFactory` 구현체나 `response` 헬퍼에서 호출할 때, 매크로의 클로저가 실행됩니다.

```php
return response()->caps('foo');
```
