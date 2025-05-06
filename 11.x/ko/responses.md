# HTTP 응답

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리디렉션](#redirects)
    - [이름이 지정된 라우트로 리디렉션하기](#redirecting-named-routes)
    - [컨트롤러 액션으로 리디렉션하기](#redirecting-controller-actions)
    - [외부 도메인으로 리디렉션하기](#redirecting-external-domains)
    - [플래시 세션 데이터와 함께 리디렉션하기](#redirecting-with-flashed-session-data)
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

모든 라우트와 컨트롤러는 사용자의 브라우저로 전송될 응답을 반환해야 합니다. 라라벨은 여러 가지 방법으로 응답을 반환할 수 있습니다. 가장 기본적인 응답은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 해당 문자열을 자동으로 전체 HTTP 응답으로 변환합니다:

    Route::get('/', function () {
        return 'Hello World';
    });

라우트와 컨트롤러에서 문자열뿐만 아니라 배열도 반환할 수 있습니다. 프레임워크는 배열을 자동으로 JSON 응답으로 변환합니다:

    Route::get('/', function () {
        return [1, 2, 3];
    });

> [!NOTE]  
> [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections)도 라우트나 컨트롤러에서 반환할 수 있다는 사실을 알고 계셨나요? 자동으로 JSON으로 변환됩니다. 한 번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

보통 라우트 액션에서 단순한 문자열이나 배열만 반환하지 않게 됩니다. 대신, 전체 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/{{version}}/views)를 반환하게 됩니다.

전체 `Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 자유롭게 커스터마이즈할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 이 클래스는 HTTP 응답을 구성하기 위한 다양한 메서드를 제공합니다:

    Route::get('/home', function () {
        return response('Hello World', 200)
            ->header('Content-Type', 'text/plain');
    });

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델 및 컬렉션

[엘로퀀트 ORM](/docs/{{version}}/eloquent) 모델이나 컬렉션을 라우트 또는 컨트롤러에서 직접 반환할 수도 있습니다. 이 경우 라라벨은 모델의 [숨김 속성](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)을 그대로 반영하여 자동으로 JSON 응답으로 변환합니다:

    use App\Models\User;

    Route::get('/user/{user}', function (User $user) {
        return $user;
    });

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 메서드는 체이닝이 가능하므로 응답 인스턴스를 유연하게 구성할 수 있습니다. 예를 들어, `header` 메서드를 사용하면 응답에 여러 헤더를 연달아 추가할 수 있습니다:

    return response($content)
        ->header('Content-Type', $type)
        ->header('X-Header-One', 'Header Value')
        ->header('X-Header-Two', 'Header Value');

또는 `withHeaders` 메서드를 사용하여 헤더 array를 한 번에 추가할 수 있습니다:

    return response($content)
        ->withHeaders([
            'Content-Type' => $type,
            'X-Header-One' => 'Header Value',
            'X-Header-Two' => 'Header Value',
        ]);

<a name="cache-control-middleware"></a>
#### 캐시 제어 미들웨어

라라벨에는 `cache.headers` 미들웨어가 포함되어 있어 라우트 그룹에 대해 `Cache-Control` 헤더를 빠르게 설정할 수 있습니다. 디렉티브는 "snake case"로 작성하여 세미콜론(;)으로 구분해야 합니다. 만약 `etag`이 디렉티브에 포함되어 있으면, 응답 내용의 MD5 해시가 ETag 식별자로 자동 지정됩니다:

    Route::middleware('cache.headers:public;max_age=2628000;etag')->group(function () {
        Route::get('/privacy', function () {
            // ...
        });

        Route::get('/terms', function () {
            // ...
        });
    });

<a name="attaching-cookies-to-responses"></a>
### 응답에 쿠키 추가하기

아웃고잉 `Illuminate\Http\Response` 인스턴스에 `cookie` 메서드를 사용하여 쿠키를 첨부할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 그리고 유효 시간(분 단위)을 인수로 전달해야 합니다:

    return response('Hello World')->cookie(
        'name', 'value', $minutes
    );

`cookie` 메서드는 추가적인 인수들도 받을 수 있는데, 이는 PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수와 동일한 의미와 용도를 가집니다:

    return response('Hello World')->cookie(
        'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
    );

만약 아직 응답 인스턴스가 없지만, 아웃고잉 응답과 함께 쿠키를 전송하고 싶다면 `Cookie` 파사드를 이용해서 쿠키를 "큐"에 등록할 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 생성하는 데 필요한 인수들을 받습니다. 이 쿠키들은 브라우저로 응답이 전송되기 전에 첨부됩니다:

    use Illuminate\Support\Facades\Cookie;

    Cookie::queue('name', 'value', $minutes);

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성

`Symfony\Component\HttpFoundation\Cookie` 인스턴스를 나중에 응답 인스턴스에 첨부할 목적으로 생성하고 싶다면, 글로벌 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 응답 인스턴스에 첨부되지 않으면 클라이언트로 전송되지 않습니다:

    $cookie = cookie('name', 'value', $minutes);

    return response('Hello World')->cookie($cookie);

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료

아웃고잉 응답의 `withoutCookie` 메서드를 이용하면 쿠키를 만료시킬 수 있습니다:

    return response('Hello World')->withoutCookie('name');

아직 응답 인스턴스가 없다면, `Cookie` 파사드의 `expire` 메서드를 사용할 수도 있습니다:

    Cookie::expire('name');

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에 라라벨에서 생성되는 모든 쿠키는 암호화되고 서명되어, 클라이언트에서 변조되거나 읽힐 수 없습니다. 애플리케이션에서 생성하는 일부 쿠키에 대해 암호화를 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용하면 됩니다:

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->encryptCookies(except: [
            'cookie_name',
        ]);
    })

<a name="redirects"></a>
## 리디렉션

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리디렉션하기에 필요한 올바른 헤더를 내장합니다. 여러 가지 방법으로 `RedirectResponse` 인스턴스를 생성할 수 있습니다. 가장 간단한 방법은 글로벌 `redirect` 헬퍼를 사용하는 것입니다:

    Route::get('/dashboard', function () {
        return redirect('/home/dashboard');
    });

경우에 따라서는, 제출된 폼이 유효하지 않을 때처럼 사용자를 이전 위치로 되돌리고 싶을 수 있습니다. 이럴 때는 글로벌 `back` 헬퍼 함수를 사용하면 됩니다. 이 기능은 [세션](/docs/{{version}}/session)을 사용하므로, `back` 함수를 호출하는 라우트가 반드시 `web` 미들웨어 그룹을 사용해야 합니다:

    Route::post('/user/profile', function () {
        // 요청 검증...

        return back()->withInput();
    });

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리디렉션하기

`redirect` 헬퍼를 인수 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어 `Redirector`의 모든 메서드를 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리디렉션 응답을 생성하려면 `route` 메서드를 사용할 수 있습니다:

    return redirect()->route('login');

라우트에 파라미터가 있다면, `route` 메서드의 두 번째 인수로 파라미터를 전달할 수 있습니다:

    // URI가 /profile/{id}인 라우트의 경우

    return redirect()->route('profile', ['id' => 1]);

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델로 파라미터 채우기

"ID" 파라미터가 Eloquent 모델에서 채워지는 라우트로 리디렉션할 때에는, 모델 자체를 전달해도 됩니다. 라라벨이 ID를 자동으로 추출해 줍니다:

    // URI가 /profile/{id}인 라우트의 경우

    return redirect()->route('profile', [$user]);

라우트 파라미터에 들어가는 값을 커스터마이즈하고 싶다면 라우트 파라미터 정의에서 컬럼을 지정(`/profile/{id:slug}`)하거나, Eloquent 모델의 `getRouteKey` 메서드를 오버라이드하면 됩니다:

    /**
     * 모델의 라우트 키 값을 반환합니다.
     */
    public function getRouteKey(): mixed
    {
        return $this->slug;
    }

<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리디렉션하기

[컨트롤러 액션](/docs/{{version}}/controllers)으로의 리디렉션 생성도 가능합니다. 이때는 컨트롤러와 액션 이름을 `action` 메서드에 전달하세요:

    use App\Http\Controllers\UserController;

    return redirect()->action([UserController::class, 'index']);

컨트롤러 라우트에 파라미터가 필요하다면, `action` 메서드의 두 번째 인수로 전달할 수 있습니다:

    return redirect()->action(
        [UserController::class, 'profile'], ['id' => 1]
    );

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션하기

애플리케이션 외부의 도메인으로 사용자 리디렉션이 필요할 때는, `away` 메서드를 사용하세요. 이 메서드는 추가적인 URL 인코딩, 검증 없이 `RedirectResponse`를 생성합니다:

    return redirect()->away('https://www.google.com');

<a name="redirecting-with-flashed-session-data"></a>
### 플래시 세션 데이터와 함께 리디렉션하기

새로운 URL로 리디렉션과 [세션으로 데이터 플래시](/docs/{{version}}/session#flash-data)는 보통 동시에 이루어집니다. 예를 들어, 어떤 작업이 성공적으로 완료된 후, 성공 메시지를 세션에 플래시한 뒤 리디렉션하는 경우가 많습니다. 편의를 위해, `RedirectResponse` 인스턴스를 생성하면서 플루언트 체이닝으로 세션 데이터도 플래시할 수 있습니다:

    Route::post('/user/profile', function () {
        // ...

        return redirect('/dashboard')->with('status', 'Profile updated!');
    });

사용자가 리디렉션된 후, [세션](/docs/{{version}}/session)에서 플래시 메시지를 표시할 수 있습니다. 예를 들어, [Blade 문법](/docs/{{version}}/blade)로 다음과 같이 할 수 있습니다:

    @if (session('status'))
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    @endif

<a name="redirecting-with-input"></a>
#### 입력 값과 함께 리디렉션하기

`RedirectResponse` 인스턴스의 `withInput` 메서드를 사용하면, 현재 요청의 입력 값을 세션에 플래시하여 새로운 위치로 리디렉션할 때 전달할 수 있습니다. 이는 보통 유효성 검증 오류가 발생한 경우에 사용됩니다. 한 번 입력 값이 세션에 플래시되면, 다음 요청에서 [쉽게 가져와서](/docs/{{version}}/requests#retrieving-old-input) 폼을 다시 채울 수 있습니다:

    return back()->withInput();

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼는 다른 종류의 응답 인스턴스도 생성할 수 있습니다. 인수 없이 호출하면, `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/{{version}}/contracts)의 구현체가 반환됩니다. 이 컨트랙트에는 다양한 응답을 생성할 수 있는 여러 유용한 메서드가 포함되어 있습니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드와 헤더를 제어하면서 [뷰](/docs/{{version}}/views)를 응답 본문으로 사용해야 한다면, `view` 메서드를 사용하세요:

    return response()
        ->view('hello', $data, 200)
        ->header('Content-Type', $type);

물론, 특별히 HTTP 상태 코드나 커스텀 헤더를 지정할 필요가 없으면 글로벌 `view` 헬퍼 함수를 사용하면 됩니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 `application/json`으로 자동 설정하고, 전달한 배열을 PHP의 `json_encode` 함수를 이용해 JSON으로 변환합니다:

    return response()->json([
        'name' => 'Abigail',
        'state' => 'CA',
    ]);

JSONP 응답을 생성하려면, `json` 메서드와 함께 `withCallback` 메서드를 사용하세요:

    return response()
        ->json(['name' => 'Abigail', 'state' => 'CA'])
        ->withCallback($request->input('callback'));

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저가 지정한 경로의 파일을 다운로드하도록 강제하는 응답을 생성합니다. 두 번째 인수로 전달한 파일명을 사용자가 다운로드할 때 볼 수 있습니다. 마지막으로, 세 번째 인수에 HTTP 헤더의 배열을 전달할 수 있습니다:

    return response()->download($pathToFile);

    return response()->download($pathToFile, $name, $headers);

> [!WARNING]  
> 파일 다운로드를 관리하는 Symfony HttpFoundation은 다운로드되는 파일의 파일명이 반드시 ASCII여야 한다는 점에 유의하세요.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 이미지나 PDF와 같은 파일을 사용자의 브라우저에서 곧바로 표시할 수 있도록 합니다(다운로드를 유도하는 것이 아니라). 이 메서드는 파일의 절대 경로를 첫 번째 인수로, 헤더 배열을 두 번째 인수로 받습니다:

    return response()->file($pathToFile);

    return response()->file($pathToFile, $headers);

<a name="streamed-responses"></a>
### 스트림 응답

데이터를 생성과 동시에 클라이언트로 스트리밍하면, 메모리 사용량을 크게 줄이고 성능을 향상시킬 수 있습니다. 특히 매우 큰 응답에 유용합니다. 스트림 응답을 이용하면 서버가 모든 응답 데이터를 전송하기 전에 클라이언트에서 데이터를 처리할 수 있습니다:

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
                sleep(2); // 청크 사이에 딜레이를 시뮬레이션...
            }
        }, 200, ['X-Accel-Buffering' => 'no']);
    });

> [!NOTE]
> 라라벨 내부적으로 PHP의 출력 버퍼링(output buffering) 기능을 사용합니다. 위 예제처럼, `ob_flush`와 `flush` 함수를 이용해 버퍼된 콘텐츠를 클라이언트로 밀어 보내야 합니다.

<a name="streamed-json-responses"></a>
#### 스트리밍 JSON 응답

점진적으로 JSON 데이터를 스트리밍하려면 `streamJson` 메서드를 사용할 수 있습니다. 이 메서드는 대용량 데이터를 JavaScript에서 쉽게 파싱할 수 있는 형식으로 브라우저에 점진적으로 전송해야 할 때 특히 유용합니다:

    use App\Models\User;

    Route::get('/users.json', function () {
        return response()->streamJson([
            'users' => User::cursor(),
        ]);
    });

<a name="event-streams"></a>
#### 이벤트 스트림

`eventStream` 메서드는 `text/event-stream` 컨텐츠 타입을 활용해 서버 전송 이벤트(Server-Sent Events, SSE) 스트림 응답을 반환할 수 있습니다. `eventStream` 메서드는 클로저를 인수로 받으며, 클로저는 응답이 준비되는 대로 스트림에 [yield](https://www.php.net/manual/en/language.generators.overview.php)해야 합니다:

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

이 이벤트 스트림은 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체로 소비할 수 있습니다. 스트림이 완료되면 `eventStream` 메서드는 자동으로 `</stream>` 업데이트를 이벤트 스트림에 전송합니다:

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

<a name="streamed-downloads"></a>
#### 스트리밍 다운로드

특정 작업의 문자열 응답을 디스크에 기록하지 않고 즉시 다운로드 응답으로 전환하려는 경우 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일 이름, 그리고(optional) 헤더 배열을 인수로 받습니다:

    use App\Services\GitHub;

    return response()->streamDownload(function () {
        echo GitHub::api('repo')
            ->contents()
            ->readme('laravel', 'laravel')['contents'];
    }, 'laravel-readme.md');

<a name="response-macros"></a>
## 응답 매크로

여러 라우트 및 컨트롤러에서 반복 사용할 수 있는 커스텀 응답을 정의하려면 `Response` 파사드의 `macro` 메서드를 사용하면 됩니다. 일반적으로, 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers), 예를 들어 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

`macro` 함수의 첫 번째 인수는 이름이고, 두 번째 인수는 클로저입니다. 매크로의 클로저는 `ResponseFactory` 구현체나 `response` 헬퍼에서 매크로 이름을 호출할 때 실행됩니다:

    return response()->caps('foo');
