# HTTP 응답

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
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
    - [스트림 응답](#streamed-responses)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성

<a name="strings-arrays"></a>
#### 문자열 및 배열

모든 라우트 및 컨트롤러는 사용자의 브라우저로 전송될 응답을 반환해야 합니다. Laravel은 다양한 방식으로 응답을 반환할 수 있도록 지원합니다. 가장 기본적인 방법은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다:

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열뿐만 아니라 배열도 반환할 수 있습니다. 프레임워크는 배열을 자동으로 JSON 응답으로 변환해줍니다:

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections) 역시 라우트 또는 컨트롤러에서 그대로 반환할 수 있다는 사실, 알고 계셨나요? 자동으로 JSON으로 변환됩니다. 한 번 시도해보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로 라우트 액션에서 간단한 문자열이나 배열만 반환하지 않습니다. 대신, 전체 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/{{version}}/views)를 반환하게 됩니다.

전체 `Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 커스터마이징할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 이는 HTTP 응답을 구축하기 위한 다양한 메서드를 제공합니다:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델 및 컬렉션

[Eloquent ORM](/docs/{{version}}/eloquent) 모델 및 컬렉션을 라우트나 컨트롤러에서 직접 반환할 수도 있습니다. 이 경우 라라벨은 모델 및 컬렉션을 JSON 응답으로 자동 변환하며, 모델의 [hidden 속성](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)을 준수합니다:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 메서드는 체이닝이 가능하므로, 응답 인스턴스를 유연하게 구성할 수 있습니다. 예를 들어 `header` 메서드를 사용해 여러 개의 헤더를 응답에 추가할 수 있습니다:

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

혹은 `withHeaders` 메서드를 사용해 배열로 헤더를 지정할 수도 있습니다:

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

라라벨에는 `cache.headers` 미들웨어가 내장되어 있어, 라우트 그룹에 대해 `Cache-Control` 헤더를 빠르게 설정할 수 있습니다. 디렉티브는 해당 cache-control 디렉티브의 스네이크케이스 이름으로 세미콜론으로 구분하여 전달해야 합니다. 만약 디렉티브 목록에 `etag`를 지정하면, 응답 콘텐츠의 MD5 해시가 ETag 식별자로 자동 설정됩니다:

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

`Illuminate\Http\Response` 인스턴스에 `cookie` 메서드를 사용해 쿠키를 응답에 첨부할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 유효 기간(분)을 전달해야 합니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 더 다양한 인자를 받을 수 있으며, 이 인자들은 PHP 내장 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수와 목적이나 의미가 동일합니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

아직 응답 인스턴스를 가지고 있지 않지만, 응답이 전송될 때 쿠키가 함께 전송되도록 하고 싶을 경우, `Cookie` 파사드를 사용해 쿠키를 "큐 입력"할 수 있습니다. `queue` 메서드는 쿠키 인스턴스 생성을 위한 인자를 받습니다. 이 쿠키는 브라우저로 응답이 전송되기 전에 자동으로 첨부됩니다:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성

나중에 응답 인스턴스에 첨부할 수 있도록 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하려면, 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 응답 인스턴스에 첨부하지 않는 한 클라이언트에 전송되지 않습니다:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료시키기

응답의 `withoutCookie` 메서드를 사용해 쿠키를 만료(삭제)시킬 수 있습니다:

```php
return response('Hello World')->withoutCookie('name');
```

아직 응답 인스턴스가 없다면, `Cookie` 파사드의 `expire` 메서드를 사용해서 쿠키를 만료시킬 수 있습니다:

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에, 라라벨에서 생성되는 모든 쿠키는 암호화되고 서명되어 클라이언트가 내용을 읽거나 수정할 수 없습니다. 애플리케이션에서 생성된 일부 쿠키에 대해 암호화를 비활성화하려면, `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

<a name="redirects"></a>
## 리디렉션

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리디렉션하는 데 필요한 올바른 헤더를 포함하고 있습니다. `RedirectResponse` 인스턴스를 생성하는 방법에는 여러 가지가 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 이용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때때로, 예를 들어 폼 제출이 유효하지 않을 때 이전 위치로 사용자를 리디렉션하고 싶을 수 있습니다. 전역 `back` 헬퍼 함수를 사용할 수 있으며, 이 기능은 [세션](/docs/{{version}}/session)을 이용하므로 호출하는 라우트는 `web` 미들웨어 그룹에 속해야 합니다:

```php
Route::post('/user/profile', function () {
    // 요청 검증...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리디렉션

`redirect` 헬퍼를 파라미터 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어, `Redirector`의 다양한 메서드를 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리디렉션하려면 `route` 메서드를 사용하세요:

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요한 경우, 두 번째 인수로 전달하면 됩니다:

```php
// URI: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델로 파라미터 자동 채우기

"Eloquent 모델"에서 "ID" 파라미터를 자동으로 채워야 한다면, 모델 인스턴스를 그대로 전달해도 됩니다. ID가 자동으로 추출됩니다:

```php
// URI: /profile/{id}

return redirect()->route('profile', [$user]);
```

라우트 파라미터로 들어가는 값을 커스터마이징하려면, 라우트 파라미터 정의 시 컬럼을 지정(/profile/{id:slug})하거나 모델의 `getRouteKey` 메서드를 오버라이드할 수 있습니다:

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

[컨트롤러 액션](/docs/{{version}}/controllers)으로 리디렉션하는 것도 가능합니다. 컨트롤러와 액션명을 `action` 메서드에 전달하세요:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

파라미터가 필요한 경우, 두 번째 인수에 전달하면 됩니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션

애플리케이션 외부의 도메인으로 리디렉션해야 할 경우 `away` 메서드를 사용할 수 있습니다. 이 메서드는 추가적인 URL 인코딩, 검증, 확인 없이 `RedirectResponse`를 생성합니다:

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 플래시 세션 데이터와 함께 리디렉션

새 URL로 리디렉션하면서 [플래시 데이터를 세션에 저장](/docs/{{version}}/session#flash-data)하는 경우가 많습니다. 보통 어떤 동작을 성공적으로 수행한 후, 성공 메시지를 세션에 플래시할 때 활용됩니다. 이를 위해, 하나의 유창한 메서드 체인으로 `RedirectResponse` 인스턴스를 생성하고, 세션에 데이터를 플래시할 수 있습니다:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리디렉션된 후, [세션](/docs/{{version}}/session)에서 플래시 메시지를 표시할 수 있습니다. 예를 들어 [Blade 문법](/docs/{{version}}/blade)를 사용하면:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리디렉션 

`RedirectResponse` 인스턴스에서 제공하는 `withInput` 메서드를 이용해, 리디렉션 이전에 현재 요청의 입력 데이터를 세션에 플래시할 수 있습니다. 보통 사용자가 유효성 검사 오류를 만났을 때 사용합니다. 이 입력 데이터는 다음 요청에서 폼 재입력에 쉽게 [조회할 수 있습니다](/docs/{{version}}/requests#retrieving-old-input):

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼는 여러 타입의 응답 인스턴스 생성을 지원합니다. 인수를 지정하지 않고 호출하면, `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/{{version}}/contracts)를 구현한 객체가 반환됩니다. 이 컨트랙트는 다양한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

HTTP 상태와 헤더를 직접 제어해야 하면서도 [뷰](/docs/{{version}}/views)를 응답 콘텐츠로 반환하려면, `view` 메서드를 사용하세요:

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

HTTP 상태 코드나 커스텀 헤더가 필요 없다면 전역 `view` 헬퍼 함수를 사용할 수 있습니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 설정하고, 지정한 배열을 PHP의 `json_encode` 함수로 변환합니다:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 생성하려면, `json` 메서드와 `withCallback` 메서드를 조합해 사용할 수 있습니다:

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드는 지정한 경로의 파일을 브라우저에서 강제로 다운로드하게끔 하는 응답을 생성합니다. 두 번째 인수로는 사용자가 다운로드 시 보게 될 파일명을 지정할 수 있으며, 세 번째 인수로 HTTP 헤더 배열을 전달할 수 있습니다:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은 다운로드 대상 파일명이 반드시 ASCII 문자로만 구성되어야 함을 요구합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 예를 들어 이미지나 PDF 등을 브라우저에서 직접 표시하고자 할 때 사용합니다. 첫 번째 인수로 절대 파일 경로를, 두 번째 인수로 헤더 배열을 전달할 수 있습니다:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
### 스트림 응답

데이터 생성과 동시에 클라이언트로 전송하면, 특히 매우 큰 응답의 경우 메모리 사용량을 줄이고 성능을 개선할 수 있습니다. 스트림 응답은 서버에서 데이터를 모두 전송하기 전에 클라이언트가 먼저 처리할 수 있도록 해줍니다:

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
            sleep(2); // 청크 전송 간 지연을 시뮬레이션...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

> [!NOTE]
> 라라벨은 내부적으로 PHP의 출력 버퍼링 기능을 활용합니다. 위와 같이, `ob_flush`와 `flush` 함수를 사용해서 버퍼링된 콘텐츠를 클라이언트로 전송해야 합니다.

<a name="streamed-json-responses"></a>
#### 스트림 JSON 응답

JSON 데이터를 점진적으로 스트리밍해야 한다면, `streamJson` 메서드를 사용할 수 있습니다. 이 메서드는 대용량 데이터를 브라우저로 점진적으로 전송할 때 유용하며, 자바스크립트에서 쉽게 파싱할 수 있도록 형식을 맞춰줍니다:

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

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용해 서버 전송 이벤트(SSE: Server-Sent Events) 스트림 응답을 반환합니다. `eventStream` 메서드는 클로저를 받으며, 응답이 준비될 때마다 [yield](https://www.php.net/manual/en/language.generators.overview.php)로 데이터를 반환해야 합니다:

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

이벤트의 이름을 커스터마이즈하려면, `StreamedEvent` 클래스를 인스턴스화해서 yield 할 수 있습니다:

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

이벤트 스트림은 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체를 통해 구독할 수 있습니다. 스트림이 완료되면 `eventStream` 메서드는 자동으로 `</stream>` 업데이트를 이벤트 스트림에 보냅니다:

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

마지막으로 전송되는 이벤트를 커스터마이즈하려면, `eventStream` 메서드의 `endStreamWith` 인수에 `StreamedEvent` 인스턴스를 전달할 수 있습니다:

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
#### 스트림 다운로드

어떤 작업의 결과 문자열을 파일로 저장하지 않고, 곧바로 다운로드 응답으로 전환하고 싶을 때는 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, (선택사항) 헤더 배열을 인수로 받습니다:

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

여러 라우트와 컨트롤러에서 재사용하고 싶은 커스텀 응답을 정의하려면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) 중 하나(예: `App\Providers\AppServiceProvider`)의 `boot` 메서드에서 호출합니다:

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

`macro` 함수는 첫 번째 인수로 이름을, 두 번째 인수로 클로저를 받습니다. 매크로의 클로저는 `ResponseFactory` 구현이나 `response` 헬퍼에서 매크로 이름으로 호출할 때 실행됩니다:

```php
return response()->caps('foo');
```