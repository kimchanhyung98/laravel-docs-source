# HTTP 응답

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가](#attaching-headers-to-responses)
    - [응답에 쿠키 추가](#attaching-cookies-to-responses)
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
    - [스트리밍 응답](#streamed-responses)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성

<a name="strings-arrays"></a>
#### 문자열과 배열

모든 라우트와 컨트롤러는 사용자의 브라우저로 다시 전송할 응답을 반환해야 합니다. Laravel은 여러 가지 방식으로 응답을 반환할 수 있습니다. 가장 기본적인 응답은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 이 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다.

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트나 컨트롤러에서 문자열뿐만 아니라 배열을 반환할 수도 있습니다. 프레임워크는 배열을 자동으로 JSON 응답으로 변환합니다.

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트 또는 컨트롤러에서 [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections)도 반환할 수 있다는 사실, 알고 계셨나요? 이 역시 자동으로 JSON으로 변환됩니다. 한 번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로 라우트 액션에서는 단순한 문자열이나 배열을 반환하는 것 이상을 하게 됩니다. 대신, 전체 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/{{version}}/views)를 반환하게 됩니다.

전체 `Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 자유롭게 커스터마이즈할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 이 클래스는 HTTP 응답을 작성하기 위한 다양한 메서드를 제공합니다.

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션

[엘로퀀트 ORM](/docs/{{version}}/eloquent) 모델과 컬렉션 역시 라우트와 컨트롤러에서 직접 반환할 수 있습니다. 이렇게 하면 Laravel이 모델과 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [숨김 속성](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)도 자동으로 처리됩니다.

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가

대부분의 응답 메서드는 체이닝이 가능하므로, 응답 인스턴스를 유연하게 작성할 수 있습니다. 예를 들어, `header` 메서드를 사용해 여러 개의 헤더를 응답에 추가할 수 있습니다.

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또한, `withHeaders` 메서드를 사용해 한 번에 헤더 배열을 지정할 수 있습니다.

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

Laravel에는 `cache.headers` 미들웨어가 내장되어 있어, 해당 미들웨어를 사용하는 라우트 그룹에 대해 `Cache-Control` 헤더를 빠르게 설정할 수 있습니다. 지시어는 대응되는 cache-control 지시어의 "스네이크 케이스"로 써주고, 세미콜론으로 구분하여 전달합니다. 지시어 목록에 `etag`를 지정하면, 응답 내용의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다.

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

`Illuminate\Http\Response` 인스턴스의 `cookie` 메서드를 사용하면 응답에 쿠키를 첨부할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 그리고 쿠키가 유효한 분(minutes) 수를 전달합니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 추가로 몇 가지 인자를 더 받을 수 있습니다. 이 인자들은 PHP의 기본 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수의 인자와 비슷한 목적과 의미를 가집니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

아직 응답 인스턴스가 없는 경우에도, `Cookie` 파사드의 `queue` 메서드를 사용해 나중에 응답이 전송될 때 쿠키가 첨부되도록 "큐잉" 할 수 있습니다. 이 메서드는 쿠키 인스턴스 생성을 위해 필요한 인자들을 받습니다. 큐잉된 쿠키는 브라우저로 응답이 전송되기 전에 자동으로 첨부됩니다.

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성

나중에 응답 인스턴스에 첨부할 수 있는 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 직접 생성하려면 글로벌 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키 인스턴스는 응답 인스턴스에 첨부되지 않는 한 클라이언트로 전송되지 않습니다.

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키를 조기에 만료시키기

아웃고잉 응답의 `withoutCookie` 메서드를 사용해 쿠키를 만료(삭제)할 수 있습니다.

```php
return response('Hello World')->withoutCookie('name');
```

아직 응답 인스턴스가 없는 경우라면, `Cookie` 파사드의 `expire` 메서드를 사용해 쿠키를 만료시킬 수 있습니다.

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에, Laravel에서 생성되는 모든 쿠키는 암호화되고 서명됩니다. 따라서 클라이언트가 쿠키를 읽거나 조작할 수 없습니다. 애플리케이션에서 생성되는 일부분의 쿠키에 대해 암호화를 비활성화하고 싶을 때에는 애플리케이션의 `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

<a name="redirects"></a>
## 리다이렉트

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 이동시키는 데 필요한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있습니다. 가장 간단한 방법은 글로벌 `redirect` 헬퍼를 사용하는 것입니다.

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때로는, 제출된 폼이 잘못된 경우와 같이 사용자를 이전 위치로 리다이렉트하고 싶을 수 있습니다. 이럴 때는 글로벌 `back` 헬퍼 함수를 사용하면 됩니다. 이 기능은 [세션](/docs/{{version}}/session)을 이용하므로, 해당 라우트가 `web` 미들웨어 그룹을 사용하고 있는지 확인하세요.

```php
Route::post('/user/profile', function () {
    // 요청 검증...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리다이렉트

`redirect` 헬퍼를 파라미터 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환되며, 이를 통해 여러 메서드를 연결(chain)해서 사용할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리다이렉트할 때 `route` 메서드를 사용할 수 있습니다.

```php
return redirect()->route('login');
```

라우트에 파라미터가 있다면, `route` 메서드의 두 번째 인수로 전달하세요.

```php
// 라우트 URI가: /profile/{id} 일 때

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 자동 매핑

ID 파라미터가 있는 라우트로 리다이렉트할 때, 해당 파라미터를 Eloquent 모델에서 가져오려면 모델 인스턴스 자체를 전달하면 됩니다. ID 값이 자동으로 추출됩니다.

```php
// 라우트 URI가: /profile/{id} 일 때

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 대입할 값을 커스터마이징하려면, 라우트 파라미터 정의에서 컬럼을 명시(`/profile/{id:slug}`)하거나, 모델에서 `getRouteKey` 메서드를 오버라이드하면 됩니다.

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

[컨트롤러 액션](/docs/{{version}}/controllers)으로 리다이렉트하려면 컨트롤러와 액션 이름을 `action` 메서드에 전달하세요.

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요한 경우 두 번째 인수로 배열을 전달합니다.

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리다이렉트

때로는 애플리케이션 외부의 도메인으로 리다이렉트해야 할 때가 있습니다. 이럴 땐 추가 URL 인코딩, 검증, 확인 없이 리다이렉트 응답을 생성하는 `away` 메서드를 사용할 수 있습니다.

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 세션 데이터와 함께 리다이렉트

새로운 URL로 리다이렉트하면서 [데이터를 세션에 플래시](/docs/{{version}}/session#flash-data)하는 경우가 많습니다. 보통 어떤 동작이 성공한 후, 성공 메시지를 세션에 잠깐 저장할 때 주로 사용됩니다. `RedirectResponse` 인스턴스를 만들고 플래시 데이터를 메서드 체이닝으로 한 번에 담을 수 있습니다.

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리다이렉트된 후에는 [세션](/docs/{{version}}/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어, [Blade 문법](/docs/{{version}}/blade)을 이용해 다음과 같이 표시할 수 있습니다.

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리다이렉트

`RedirectResponse` 인스턴스가 제공하는 `withInput` 메서드를 사용하면, 현재 요청의 입력값을 세션에 플래시 하고 새 위치로 리다이렉트할 수 있습니다. 주로 입력값이 있는 폼 검증에 실패할 때 사용합니다. 입력값이 세션에 플래시된 후에는, [이전 입력값을 요청에서 쉽게 확인](/docs/{{version}}/requests#retrieving-old-input)해 폼을 복원할 수 있습니다.

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼는 다양한 타입의 응답 인스턴스를 생성할 수 있습니다. 인자를 전달하지 않고 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/{{version}}/contracts)의 구현체가 반환됩니다. 이 컨트랙트에는 여러 유용한 응답 생성 메서드가 포함되어 있습니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태/헤더를 제어하면서, [뷰](/docs/{{version}}/views)를 응답 본문으로 반환하고 싶다면 `view` 메서드를 사용하면 됩니다.

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

HTTP 상태코드나 커스텀 헤더 지정이 필요 없다면, 글로벌 `view` 헬퍼 함수를 그대로 사용할 수 있습니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 자동으로 `Content-Type` 헤더를 `application/json`으로 설정하고, 넘겨준 배열을 PHP의 `json_encode` 함수로 변환해 반환합니다.

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 생성하려면 `json` 메서드와 함께 `withCallback` 메서드를 사용할 수 있습니다.

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드는 주어진 경로의 파일을 강제로 사용자의 브라우저가 다운로드하도록 응답을 생성합니다. 두 번째 인자로 파일명을 지정하면, 사용자에게 보이는 다운로드 파일명이 결정됩니다. 마지막 인자로는 HTTP 헤더 배열을 전달할 수 있습니다.

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 담당하는 Symfony HttpFoundation은 다운로드되는 파일명이 반드시 ASCII 문자여야 함을 요구합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 이미지를 비롯한 파일(이미지, PDF 등)을 사용자의 브라우저에서 곧바로 표시하는 파일 응답을 생성합니다. 첫 번째 인자로는 파일의 절대 경로, 두 번째 인자로는 헤더 배열을 받을 수 있습니다.

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
### 스트리밍 응답

데이터 생성과 동시에 클라이언트로 스트리밍 전송하면, 메모리 사용을 대폭 줄이고 성능을 향상시킬 수 있습니다. 특히 대용량 응답에서 효과가 큽니다. 스트리밍 응답은 서버가 데이터를 모두 보내기 전에 클라이언트가 데이터를 처리할 수 있도록 해줍니다.

```php
function streamedContent(): Generator {
    yield 'Hello, ';
    yield 'World!';
}

Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (streamedContent() as $chunk) {
            echo $chunk;
            ob_flush();
            flush();
            sleep(2); // 청크 간 딜레이를 시뮬레이션...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

> [!NOTE]
> 내부적으로, Laravel은 PHP의 출력 버퍼링 기능(output buffering)을 사용합니다. 위 예시에서 볼 수 있듯이, `ob_flush` 및 `flush` 함수를 이용해 버퍼링된 내용을 즉시 클라이언트로 전달하세요.

<a name="streamed-json-responses"></a>
#### 스트리밍 JSON 응답

점진적으로 JSON 데이터를 스트리밍해야 할 경우, `streamJson` 메서드를 사용할 수 있습니다. 이 방법은 브라우저로 대량의 데이터를 점진적으로 전송해야 하고, 자바스크립트로 쉽게 처리 가능한 형식일 때 유용합니다.

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

<a name="event-streams"></a>
#### 이벤트 스트림

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용하여 Server-Sent Events(SSE) 스트리밍 응답을 반환합니다. 이 메서드는 클로저를 받으며, 스트림에 쓸 응답을 [yield](https://www.php.net/manual/en/language.generators.overview.php)로 반환할 수 있습니다.

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

이벤트 이름을 직접 지정하려면, `StreamedEvent` 클래스의 인스턴스를 yield 하면 됩니다.

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

이벤트 스트림은 Laravel의 `stream` npm 패키지를 사용하여 소비할 수 있습니다. 이 패키지는 Laravel 이벤트 스트림과 상호작용하기 위한 편리한 API를 제공합니다. 먼저 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

이제 `useEventStream`을 사용해 이벤트 스트림을 구독할 수 있습니다. 스트림 URL을 제공하면, 훅이 자동으로 메시지를 갱신하여 Laravel 애플리케이션에서 반환되는 응답을 누적(concatenate)하여 반환합니다.

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

`useEventStream`에 전달하는 두 번째 인수는 옵션 객체로, 스트림 소비 동작을 커스터마이즈할 수 있습니다. 아래는 이 옵션 객체의 기본값입니다.

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

이벤트 스트림은 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체로 수동으로 소비할 수도 있습니다. 스트림이 완료되면 `eventStream` 메서드가 자동으로 이벤트 스트림에 `</stream>` 업데이트를 전송합니다.

```js
const source = new EventSource('/chat');

source.addEventListener('update', (event) => {
    if (event.data === '</stream>') {
        source.close();

        return;
    }

    console.log(event.data);
})
```

스트림에 전송되는 마지막 이벤트를 커스터마이징하려면, `eventStream` 메서드의 `endStreamWith` 인자에 `StreamedEvent` 인스턴스를 전달할 수 있습니다.

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
#### 스트리밍 다운로드

어떤 연산에서 나온 문자열 응답을 직접 디스크에 쓰지 않고 바로 다운로드 가능한 응답으로 만들고 싶을 때는 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일 이름, 추가적으로 헤더 배열을 인자로 받습니다.

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

여러 라우트와 컨트롤러에서 반복적으로 사용할 수 있는 커스텀 응답을 정의하려면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 보통 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) 중 하나(예: `App\Providers\AppServiceProvider`)의 `boot` 메서드 안에서 호출하는 것이 일반적입니다.

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

`macro` 함수는 첫 번째 인수로 이름, 두 번째 인수로 클로저를 받습니다. 매크로 이름을 `ResponseFactory` 구현체나 `response` 헬퍼에서 호출하면, 매크로의 클로저가 실행됩니다.

```php
return response()->caps('foo');
```
