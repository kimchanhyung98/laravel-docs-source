# HTTP 응답 (HTTP Responses)

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리디렉션](#redirects)
    - [이름이 지정된 라우트로 리디렉션](#redirecting-named-routes)
    - [컨트롤러 액션으로 리디렉션](#redirecting-controller-actions)
    - [외부 도메인으로 리디렉션](#redirecting-external-domains)
    - [세션 데이터 플래시와 리디렉션](#redirecting-with-flashed-session-data)
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

모든 라우트와 컨트롤러에서는 사용자 브라우저로 전송할 응답을 반환해야 합니다. Laravel은 다양한 방식으로 응답을 반환할 수 있도록 지원합니다. 가장 기본적인 방법은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크가 문자열을 자동으로 전체 HTTP 응답으로 변환합니다:

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트나 컨트롤러에서 배열을 반환할 수도 있습니다. 프레임워크가 배열을 자동으로 JSON 응답으로 변환합니다:

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/12.x/eloquent-collections)을 반환할 수도 있다는 사실을 알고 계셨나요? 자동으로 JSON으로 변환되어 동작합니다. 직접 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

실제 애플리케이션에서는 단순한 문자열이나 배열만 반환하는 것이 아니라, 보통 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/12.x/views)를 반환합니다.

`Response` 인스턴스를 반환함으로써 HTTP 상태 코드와 헤더 등을 자유롭게 커스터마이즈할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 다양한 HTTP 응답을 만들기 위한 여러 메서드를 제공합니다:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션

[Eloquent ORM](/docs/12.x/eloquent) 모델이나 컬렉션을 라우트 또는 컨트롤러에서 바로 반환할 수도 있습니다. 이 경우 Laravel이 모델과 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [hidden 속성](/docs/12.x/eloquent-serialization#hiding-attributes-from-json) 설정도 자동으로 반영합니다:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 메서드는 체이닝을 지원하므로, 응답 인스턴스를 유연하게 생성할 수 있습니다. 예를 들어, `header` 메서드를 사용해 여러 헤더를 응답에 연속적으로 추가할 수 있습니다:

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는, `withHeaders` 메서드를 사용하여 헤더 배열을 한 번에 추가할 수도 있습니다:

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

Laravel에는 `cache.headers` 미들웨어가 내장되어 있어, 라우트 그룹에 대해 `Cache-Control` 헤더를 빠르게 설정할 수 있습니다. 지시어는 해당 cache-control 디렉티브의 snake case 버전으로 전달하며, 세미콜론(;)으로 구분합니다. 만약 `etag`를 지정하면, 응답 내용의 MD5 해시가 ETag 식별자로 자동 설정됩니다:

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

`cookie` 메서드를 사용해 `Illuminate\Http\Response` 인스턴스에 쿠키를 추가할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 그리고 쿠키가 유효한 시간(분)을 전달해야 합니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 더 다양한 인자도 받을 수 있습니다. 일반적으로 이 인자들은 PHP의 기본 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수와 동일한 목적과 의미를 갖습니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

미리 응답 인스턴스가 없는 상황에서 쿠키를 반드시 전송하고 싶다면, `Cookie` 파사드를 사용해 쿠키를 '큐'에 등록할 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 만드는데 필요한 인자를 받으며, 이 쿠키는 실제 응답이 브라우저로 보내지기 전에 자동으로 첨부됩니다:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성

`Symfony\Component\HttpFoundation\Cookie` 인스턴스를 직접 생성해 두었다가 나중에 응답에 첨부하고 싶을 때는, 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이렇게 생성된 쿠키는 직접 응답 인스턴스에 첨부하지 않으면 클라이언트로 전송되지 않습니다:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 미리 만료시키기

`withoutCookie` 메서드를 사용해 응답에서 쿠키를 만료시켜 제거할 수 있습니다:

```php
return response('Hello World')->withoutCookie('name');
```

아직 응답 인스턴스가 없는 경우에는 `Cookie` 파사드의 `expire` 메서드를 이용해 쿠키를 만료처리할 수 있습니다:

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로, `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에 Laravel이 생성하는 모든 쿠키는 암호화 및 서명되어, 클라이언트에서 읽거나 변조할 수 없습니다. 애플리케이션에서 생성하는 일부 쿠키에 대해 암호화를 비활성화하고 싶다면, `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용하세요:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

> [!NOTE]
> 일반적으로 쿠키 암호화는 절대 비활성화해서는 안됩니다. 비활성화할 경우, 쿠키 데이터가 클라이언트에서 노출되거나 변조될 수 있습니다.

<a name="redirects"></a>
## 리디렉션

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스 인스턴스이며, 사용자가 새로운 URL로 리디렉션되는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 여러 방법이 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

사용자가 원래 위치로 다시 이동해야 할 상황(예: 폼 유효성 검증 실패 등)이 있다면, 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/12.x/session)을 사용하므로, `back` 함수를 호출하는 라우트는 반드시 `web` 미들웨어 그룹을 사용해야 합니다:

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검증...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리디렉션

`redirect` 헬퍼에 인자를 전달하지 않으면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어, 해당 인스턴스의 모든 메서드를 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리디렉션하려면 `route` 메서드를 사용할 수 있습니다:

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요한 경우, 두 번째 인자로 파라미터를 전달할 수 있습니다:

```php
// 다음과 같은 URI를 가진 라우트: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델로 라우트 파라미터 자동 채우기

ID 파라미터가 필요한 라우트로 Eloquent 모델을 전달하면, 모델의 기본키(ID) 값을 자동으로 추출하여 라우트 파라미터에 넣을 수 있습니다:

```php
// 다음과 같은 URI를 가진 라우트: /profile/{id}

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 들어가는 값을 커스터마이즈하고자 한다면, 라우트 파라미터 정의시 컬럼을 지정(`/profile/{id:slug}`)하거나, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드할 수 있습니다:

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

[컨트롤러 액션](/docs/12.x/controllers)으로 리디렉션을 생성할 수도 있는데, 이 경우 컨트롤러 클래스와 액션명을 `action` 메서드에 전달하면 됩니다:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요하다면 두 번째 인자로 전달할 수 있습니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션

애플리케이션 외부의 도메인으로 사용자를 리디렉션해야 하는 경우, `away` 메서드를 호출하면 됩니다. 이 메서드로 만든 `RedirectResponse`는 추가적인 URL 인코딩, 검증, 확인 절차 없이 직접 이동시킵니다:

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 세션 데이터 플래시와 리디렉션

새로운 URL로 리디렉션과 동시에 [세션에 데이터 플래시](/docs/12.x/session#flash-data)를 하는 경우가 많습니다. 예를 들어, 작업을 성공적으로 처리한 후 세션에 성공 메시지를 플래시하는 것 등이 대표적입니다. 하나의 메서드 체인에서 `RedirectResponse` 인스턴스 생성과 세션 데이터 플래시를 모두 처리할 수 있습니다:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리디렉션된 이후에는, [세션](/docs/12.x/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들면, [Blade 문법](/docs/12.x/blade)을 사용해 다음과 같이 구현합니다:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리디렉션

`RedirectResponse` 인스턴스의 `withInput` 메서드를 이용하면, 현재 요청의 입력값을 세션에 플래시한 뒤 새로운 위치로 사용자 리디렉션이 가능합니다. 보통 유효성 검증 에러가 발생했을 때 사용자의 입력값을 다시 폼에 전달하고 싶을 때 사용합니다. 세션에 입력값이 플래시되면 [다음 요청에 해당 값](/docs/12.x/requests#retrieving-old-input)을 쉽게 사용할 수 있습니다:

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼를 사용하면 다양한 응답 인스턴스를 생성할 수 있습니다. 이 헬퍼를 인자 없이 호출하면, `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/12.x/contracts)의 구현체가 반환됩니다. 이 컨트랙트는 여러 가지 유용한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드나 헤더를 제어하면서 [뷰](/docs/12.x/views)를 응답 콘텐츠로 반환하려면, `view` 메서드를 사용해야 합니다:

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

물론, HTTP 상태 코드나 헤더 정보가 필요 없다면, 전역 `view` 헬퍼를 바로 사용할 수도 있습니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 설정하고, 지정한 배열을 `json_encode`로 변환합니다:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답이 필요하다면, `json` 메서드와 `withCallback` 메서드를 함께 사용할 수 있습니다:

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드를 사용하면, 지정한 경로의 파일을 브라우저가 강제로 다운로드하도록 하는 응답을 만들 수 있습니다. 두 번째 인자로 파일명을 넘기면, 사용자가 다운로드 창에서 확인할 수 있는 파일명으로 지정됩니다. 세 번째 인자로 HTTP 헤더 배열을 추가할 수도 있습니다:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> Symfony HttpFoundation(파일 다운로드를 관리하는 라이브러리)은 다운로드할 파일의 파일명이 반드시 ASCII로 되어있어야 합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드를 사용하면, 이미지나 PDF 등과 같이 파일을 브라우저에서 바로 표시하도록 응답을 만들 수 있습니다(다운로드가 아닌 브라우저 내 표시). 이 메서드는 첫 번째 인자로 파일의 절대 경로를, 두 번째 인자로 헤더 배열을 받습니다:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트림 응답

데이터가 생성되는 동안 바로바로 클라이언트로 스트리밍하면, 메모리 사용량을 크게 줄이고 성능을 개선할 수 있습니다. 특히 용량이 매우 큰 응답에서 유리합니다. 스트림 응답을 사용하면, 서버가 전송을 완료하기 전에도 클라이언트에서 데이터를 미리 처리할 수 있습니다:

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // 각 데이터 조각 사이에 지연을 시뮬레이션합니다...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

`stream` 메서드에 전달하는 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하는 경우, Laravel이 각 값 사이에 자동으로 출력 버퍼를 비워주며 Nginx의 출력 버퍼링도 비활성화해줍니다:

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

스트림 응답은 Laravel의 `stream` npm 패키지를 이용해 손쉽게 사용할 수 있습니다. 이 패키지는 Laravel 응답 및 이벤트 스트림과 상호 작용할 수 있는 편리한 API를 제공합니다. 먼저 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

설치 후에는, `useStream` 훅을 사용해서 이벤트 스트림을 소비할 수 있습니다. 스트림 URL을 전달하면, 해당 훅이 Laravel 애플리케이션에서 응답으로 반환되는 내용을 점진적으로 받아 `data` 값에 누적해서 업데이트합니다:

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

데이터를 `send`로 스트림에 다시 보낼 때는, 현재 스트림 연결이 우선 취소된 뒤 새로운 데이터가 전송됩니다. 모든 요청은 JSON 형식의 `POST` 요청으로 전송됩니다.

> [!WARNING]
> `useStream` 훅은 애플리케이션으로 `POST` 요청을 전송하므로, 반드시 올바른 CSRF 토큰이 필요합니다. 가장 쉬운 방법은 [레이아웃 헤드에 meta 태그로 CSRF 토큰을 포함](/docs/12.x/csrf#csrf-x-csrf-token)하는 것입니다.

`useStream`의 두 번째 인자는 옵션 객체로, 스트림 소비 행동을 커스터마이즈할 수 있습니다. 기본값은 아래와 같습니다:

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

`onResponse`는 스트림으로부터 초기 응답을 성공적으로 받은 후 호출되며, 원시 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) 객체가 콜백에 전달됩니다. `onData`는 각 데이터 조각을 받을 때 호출되어, 현재 조각이 콜백으로 전달됩니다. `onFinish`는 스트림 전송이 종료되거나, fetch/read 사이클 중 오류가 발생할 때 호출됩니다.

기본적으로 초기화 시 스트림 요청은 자동으로 발생하지 않습니다. 스트림 시작 시 초기 페이로드를 보내고 싶다면, `initialInput` 옵션을 사용합니다:

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

스트림을 수동으로 취소하려면, 훅에서 반환되는 `cancel` 메서드를 사용하면 됩니다:

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

`useStream` 훅을 사용할 때마다, 스트림 식별용으로 무작위 `id`가 생성되어 각 요청의 `X-STREAM-ID` 헤더에 전송됩니다. 여러 컴포넌트에서 동일한 스트림을 소비할 때, 직접 `id`를 지정해 공유할 수 있습니다:

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

점진적으로 JSON 데이터를 스트림으로 전송할 필요가 있다면, `streamJson` 메서드를 사용할 수 있습니다. 이 방식은 대용량 데이터를 브라우저로 점진적으로 전송하면서 자바스크립트에서 손쉽게 파싱하는 데 특히 유용합니다:

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 [useStream 훅](#consuming-streamed-responses)과 거의 동일하나, 스트림이 완료되면 데이터를 JSON으로 자동 파싱합니다:

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

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용해 서버-전송 이벤트(Server-Sent Events, SSE) 스트림 응답을 반환할 수 있습니다. `eventStream` 메서드는, 스트림에 전달할 응답을 [yield](https://www.php.net/manual/en/language.generators.overview.php) 형태로 반환하는 클로저를 인자로 받습니다:

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

이벤트의 이름을 커스터마이즈하고 싶다면, `StreamedEvent` 클래스를 new로 생성해 yield하세요:

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 소비하기

Laravel의 `stream` npm 패키지를 사용하면, 이벤트 스트림을 편리하게 소비할 수 있습니다. 먼저 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

설치 후에는, `useEventStream` 훅을 사용해 이벤트 스트림을 소비할 수 있습니다. 스트림 URL만 지정하면, Laravel 애플리케이션이 반환하는 메시지가 점진적으로 `message` 값에 누적됩니다:

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

두 번째 인자는 옵션 객체로, 스트림 소비 행동을 커스터마이즈할 수 있습니다. 기본값은 다음과 같습니다:

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

이벤트 스트림은 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체로 직접 사용할 수도 있습니다. `eventStream` 메서드는 스트림이 완료될 때 `</stream>` 업데이트를 자동으로 전송합니다:

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

마지막 이벤트 스트림 값을 커스터마이즈하고 싶다면, `eventStream` 메서드의 `endStreamWith` 인자에 직접 `StreamedEvent` 인스턴스를 전달할 수 있습니다:

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트림 다운로드

필요에 따라, 어떤 작업의 결과 문자열을 파일로 바로 다운로드 응답으로 전환하고 싶을 수도 있습니다. 이때는 내용을 디스크에 저장하지 않고도 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, (선택적으로) 헤더 배열을 인자로 받습니다:

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

여러 라우트나 컨트롤러에서 재사용 가능한 커스텀 응답을 정의하고 싶다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션 [서비스 제공자](/docs/12.x/providers)의 `boot` 메서드에서 호출하는 것이 좋습니다(예: `App\Providers\AppServiceProvider`):

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 어떤 애플리케이션 서비스라도 부트스트랩합니다.
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

`macro` 함수는 첫 번째 인자로 매크로 이름, 두 번째 인자로 클로저를 받습니다. 매크로의 클로저는 `ResponseFactory` 구현체나 `response` 헬퍼에서 매크로 이름을 호출할 때 실행됩니다:

```php
return response()->caps('foo');
```
