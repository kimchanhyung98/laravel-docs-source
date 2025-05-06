# HTTP 클라이언트

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 데이터](#request-data)
    - [헤더](#headers)
    - [인증](#authentication)
    - [타임아웃](#timeout)
    - [재시도](#retries)
    - [에러 처리](#error-handling)
    - [Guzzle 미들웨어](#guzzle-middleware)
    - [Guzzle 옵션](#guzzle-options)
- [동시 요청](#concurrent-requests)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 가짜 처리](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [불필요한 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 감싼 간결하고 직관적인 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 통신하기 위해 빠르게 외부 HTTP 요청을 만들 수 있습니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례와 개발자 경험에 초점을 맞춥니다.

시작하기 전에 애플리케이션에서 Guzzle 패키지가 설치되어 있는지 확인해야 합니다. 기본적으로 Laravel은 해당 의존성을 자동으로 포함합니다. 만약 이전에 이 패키지를 제거했다면 Composer를 통해 다시 설치할 수 있습니다:

```shell
composer require guzzlehttp/guzzle
```

<a name="making-requests"></a>
## 요청 보내기

요청을 보내려면 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL에 기본 `GET` 요청을 만드는 방법을 살펴보겠습니다.

    use Illuminate\Support\Facades\Http;

    $response = Http::get('http://example.com');

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환합니다. 이 객체를 통해 응답을 다양한 방식으로 검사할 수 있는 여러 메서드를 제공합니다.

    $response->body() : string;
    $response->json($key = null, $default = null) : array|mixed;
    $response->object() : object;
    $response->collect($key = null) : Illuminate\Support\Collection;
    $response->status() : int;
    $response->successful() : bool;
    $response->redirect(): bool;
    $response->failed() : bool;
    $response->clientError() : bool;
    $response->header($header) : string;
    $response->headers() : array;

`Illuminate\Http\Client\Response` 객체는 PHP `ArrayAccess` 인터페이스를 구현하므로, 응답의 JSON 데이터를 직접 배열처럼 접근할 수 있습니다:

    return Http::get('http://example.com/users/1')['name'];

위 응답 메서드 외에도, 응답의 특정 상태 코드를 확인하기 위한 다음과 같은 메서드를 사용할 수 있습니다.

    $response->ok() : bool;                  // 200 OK
    $response->created() : bool;             // 201 Created
    $response->accepted() : bool;            // 202 Accepted
    $response->noContent() : bool;           // 204 No Content
    $response->movedPermanently() : bool;    // 301 Moved Permanently
    $response->found() : bool;               // 302 Found
    $response->badRequest() : bool;          // 400 Bad Request
    $response->unauthorized() : bool;        // 401 Unauthorized
    $response->paymentRequired() : bool;     // 402 Payment Required
    $response->forbidden() : bool;           // 403 Forbidden
    $response->notFound() : bool;            // 404 Not Found
    $response->requestTimeout() : bool;      // 408 Request Timeout
    $response->conflict() : bool;            // 409 Conflict
    $response->unprocessableEntity() : bool; // 422 Unprocessable Entity
    $response->tooManyRequests() : bool;     // 429 Too Many Requests
    $response->serverError() : bool;         // 500 Internal Server Error

<a name="uri-templates"></a>
#### URI 템플릿

HTTP 클라이언트는 [URI 템플릿 사양](https://www.rfc-editor.org/rfc/rfc6570)을 사용하여 요청 URL을 구성할 수도 있습니다. URI 템플릿에서 확장할 수 있는 URL 파라미터는 `withUrlParameters` 메서드를 통해 정의할 수 있습니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '9.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프(dump)하기

요청이 전송되기 전 요청 인스턴스를 덤프하고 스크립트 실행을 종료하고 싶다면, 요청 정의의 시작에 `dd` 메서드를 추가할 수 있습니다.

    return Http::dd()->get('http://example.com');

<a name="request-data"></a>
### 요청 데이터

일반적으로 `POST`, `PUT`, `PATCH` 요청을 보낼 때 추가 데이터를 함께 전송하게 됩니다. 이러한 메서드들은 두 번째 인자로 데이터 배열을 받을 수 있습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다.

    use Illuminate\Support\Facades\Http;

    $response = Http::post('http://example.com/users', [
        'name' => 'Steve',
        'role' => 'Network Administrator',
    ]);

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 할 때, 쿼리 문자열을 직접 URL에 추가하거나, key/value 파라미터 배열을 `get` 메서드의 두 번째 인자로 전달할 수 있습니다.

    $response = Http::get('http://example.com/users', [
        'name' => 'Taylor',
        'page' => 1,
    ]);

<a name="sending-form-url-encoded-requests"></a>
#### Form URL 인코딩 요청 보내기

`application/x-www-form-urlencoded` 방식으로 데이터를 보내려면 `asForm` 메서드를 요청 전에 호출해야 합니다.

    $response = Http::asForm()->post('http://example.com/users', [
        'name' => 'Sara',
        'role' => 'Privacy Consultant',
    ]);

<a name="sending-a-raw-request-body"></a>
#### Raw 바디로 요청 보내기

raw 형식의 요청 바디를 전송하고 싶을 경우, `withBody` 메서드를 사용할 수 있습니다. 콘텐츠 타입은 두 번째 인자로 지정할 수 있습니다.

    $response = Http::withBody(
        base64_encode($photo), 'image/jpeg'
    )->post('http://example.com/photo');

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트 요청으로 전송하고 싶다면, 요청 전에 `attach` 메서드를 사용하세요. 이 메서드는 파일의 이름, 내용, 그리고 필요하다면 파일명을 인자로 받습니다.

    $response = Http::attach(
        'attachment', file_get_contents('photo.jpg'), 'photo.jpg'
    )->post('http://example.com/attachments');

파일의 원본 내용을 전달하는 대신, 스트림 리소스를 전달할 수도 있습니다:

    $photo = fopen('photo.jpg', 'r');

    $response = Http::attach(
        'attachment', $photo, 'photo.jpg'
    )->post('http://example.com/attachments');

<a name="headers"></a>
### 헤더

헤더는 `withHeaders` 메서드를 사용해 요청에 추가할 수 있습니다. 이 메서드는 key/value 쌍의 배열을 받습니다.

    $response = Http::withHeaders([
        'X-First' => 'foo',
        'X-Second' => 'bar'
    ])->post('http://example.com/users', [
        'name' => 'Taylor',
    ]);

응답 데이터의 콘텐츠 타입을 지정하려면 `accept` 메서드를 사용할 수 있습니다.

    $response = Http::accept('application/json')->get('http://example.com/users');

더 간편하게, `acceptJson` 메서드를 사용하면 응답의 `application/json` 콘텐츠 타입을 기대함을 빠르게 지정할 수 있습니다.

    $response = Http::acceptJson()->get('http://example.com/users');

<a name="authentication"></a>
### 인증

기본 인증(basic auth)이나 다이제스트 인증(digest auth) 정보는 각각 `withBasicAuth`, `withDigestAuth` 메서드를 통해 지정할 수 있습니다:

    // 기본 인증...
    $response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

    // 다이제스트 인증...
    $response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);

<a name="bearer-tokens"></a>
#### Bearer 토큰

`Authorization` 헤더에 Bearer 토큰을 추가하려면 `withToken` 메서드를 사용할 수 있습니다.

    $response = Http::withToken('token')->post(/* ... */);

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드는 응답을 기다릴 최대 초 단위를 지정할 수 있습니다.

    $response = Http::timeout(3)->get(/* ... */);

타임아웃이 초과되면 `Illuminate\Http\Client\ConnectionException` 인스턴스가 발생합니다.

서버에 연결을 시도하는데 기다릴 최대 초 단위는 `connectTimeout` 메서드로 지정할 수 있습니다.

    $response = Http::connectTimeout(3)->get(/* ... */);

<a name="retries"></a>
### 재시도

클라이언트나 서버 오류가 발생할 때 HTTP 클라이언트가 자동으로 요청을 재시도하도록 하려면 `retry` 메서드를 사용할 수 있습니다. 이 메서드는 최대 시도 횟수와 각 시도 사이에 대기할 밀리초(ms)를 받습니다.

    $response = Http::retry(3, 100)->post(/* ... */);

필요하다면 `retry`의 세 번째 인자로 콜러블을 전달하여 재시도 여부를 동적으로 결정할 수 있습니다. 예를 들어, `ConnectionException` 예외가 발생했을 때만 재시도하고 싶다면 다음과 같이 작성할 수 있습니다:

    $response = Http::retry(3, 100, function ($exception, $request) {
        return $exception instanceof ConnectionException;
    })->post(/* ... */);

요청 시도가 실패한 경우, 새로운 시도 전에 요청을 변경하고 싶을 수도 있습니다. 이런 경우, `retry`에 넘긴 콜러블 내에서 `$request` 인자를 조작할 수 있습니다. 예를 들어, 인증 에러(401)가 발생할 때 새 인증 토큰으로 재시도할 수 있습니다:

    $response = Http::withToken($this->getToken())->retry(2, 0, function ($exception, $request) {
        if (! $exception instanceof RequestException || $exception->response->status() !== 401) {
            return false;
        }

        $request->withToken($this->getNewToken());

        return true;
    })->post(/* ... */);

모든 요청이 실패할 경우, 기본적으로 `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 이 동작을 비활성화하려면 `throw` 인자를 `false`로 줄 수 있습니다. 비활성화된 경우, 모든 재시도 후 마지막 응답이 반환됩니다.

    $response = Http::retry(3, 100, throw: false)->post(/* ... */);

> **경고**  
> 모든 요청이 연결 문제로 실패할 경우, `throw` 인자를 `false`로 설정해도 `Illuminate\Http\Client\ConnectionException`이 계속 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트 or 서버 오류(즉, 400, 500 레벨 응답)가 발생해도 예외를 발생시키지 않습니다. 이러한 오류가 반환되었는지는 `successful`, `clientError`, `serverError` 등의 메서드로 확인할 수 있습니다.

    // 상태 코드가 200 <= code < 300 인가?
    $response->successful();

    // 상태 코드가 400 이상인가?
    $response->failed();

    // 400대 응답인가?
    $response->clientError();

    // 500대 응답인가?
    $response->serverError();

    // 클라이언트/서버 오류 발생 시 콜백을 바로 실행
    $response->onError(callable $callback);

<a name="throwing-exceptions"></a>
#### 예외 발생

응답 인스턴스에서 클라이언트/서버 오류 발생 시 `Illuminate\Http\Client\RequestException`을 즉시 발생시키고 싶다면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

    $response = Http::post(/* ... */);

    // 오류가 있으면 예외 발생
    $response->throw();

    // 주어진 조건이 true일 때만 예외 발생
    $response->throwIf($condition);

    // 콜로저가 true를 반환하면 예외 발생
    $response->throwIf(fn ($response) => true);

    // 조건이 false일 때만 예외 발생
    $response->throwUnless($condition);

    // 콜로저가 false를 반환하면 예외 발생
    $response->throwUnless(fn ($response) => false);

    // 특정 상태 코드일 때 예외 발생
    $response->throwIfStatus(403);

    // 특정 상태 코드가 아닐 때 예외 발생
    $response->throwUnlessStatus(200);

    return $response['user']['id'];

`Illuminate\Http\Client\RequestException` 인스턴스는 반환된 응답을 확인할 수 있는 public `$response` 프로퍼티를 가집니다.

`throw` 메서드는 오류가 없으면 응답 인스턴스 스스로를 반환하므로 추가적인 체이닝이 가능합니다.

    return Http::post(/* ... */)->throw()->json();

예외가 발생하기 전 추가 작업을 하고 싶다면 콜로저를 `throw` 메서드에 전달할 수 있습니다. 이 경우 콜로저 실행 후 예외는 자동으로 던져지므로 별도의 re-throw가 필요 없습니다.

    return Http::post(/* ... */)->throw(function ($response, $e) {
        //
    })->json();

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel HTTP 클라이언트는 Guzzle을 기반으로 하므로, [Guzzle Middleware](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 통해 요청/응답을 가로채고 조작할 수 있습니다. 요청을 조작하려면, Guzzle의 `mapRequest` 미들웨어 팩토리와 함께 `withMiddleware` 메서드를 사용하세요:

    use GuzzleHttp\Middleware;
    use Illuminate\Support\Facades\Http;
    use Psr\Http\Message\RequestInterface;

    $response = Http::withMiddleware(
        Middleware::mapRequest(function (RequestInterface $request) {
            $request = $request->withHeader('X-Example', 'Value');
            
            return $request;
        })
    )->get('http://example.com');

마찬가지로, HTTP 응답을 검사하려면 Guzzle의 `mapResponse` 미들웨어 팩토리와 함께 `withMiddleware` 메서드를 사용하세요:

    use GuzzleHttp\Middleware;
    use Illuminate\Support\Facades\Http;
    use Psr\Http\Message\ResponseInterface;

    $response = Http::withMiddleware(
        Middleware::mapResponse(function (ResponseInterface $response) {
            $header = $response->getHeader('X-Example');

            // ...
            
            return $response;
        })
    )->get('http://example.com');

<a name="guzzle-options"></a>
### Guzzle 옵션

`withOptions` 메서드를 사용하여 추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정할 수 있습니다. 이 메서드는 key/value 배열을 받습니다:

    $response = Http::withOptions([
        'debug' => true,
    ])->get('http://example.com/users');

<a name="concurrent-requests"></a>
## 동시 요청

여러 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 순차적으로 요청하는 대신 여러 요청을 한꺼번에 보낼 수 있는데, 이는 느린 HTTP API와 상호작용할 때 성능을 향상시킬 수 있습니다.

이 경우 `pool` 메서드를 사용할 수 있습니다. `pool` 메서드는 클로저를 인자로 받고, 클로저는 `Illuminate\Http\Client\Pool` 인스턴스를 받아서 요청을 쉽고 명확하게 추가할 수 있게 합니다:

    use Illuminate\Http\Client\Pool;
    use Illuminate\Support\Facades\Http;

    $responses = Http::pool(fn (Pool $pool) => [
        $pool->get('http://localhost/first'),
        $pool->get('http://localhost/second'),
        $pool->get('http://localhost/third'),
    ]);

    return $responses[0]->ok() &&
           $responses[1]->ok() &&
           $responses[2]->ok();

각 응답 인스턴스는 추가한 순서대로 접근할 수 있습니다. 이름을 명시적으로 지정하고 싶다면 `as` 메서드를 사용하세요:

    use Illuminate\Http\Client\Pool;
    use Illuminate\Support\Facades\Http;

    $responses = Http::pool(fn (Pool $pool) => [
        $pool->as('first')->get('http://localhost/first'),
        $pool->as('second')->get('http://localhost/second'),
        $pool->as('third')->get('http://localhost/third'),
    ]);

    return $responses['first']->ok();

<a name="macros"></a>
## 매크로

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있어, 특정 서비스와 상호작용할 때 반복되는 요청 경로와 헤더 설정을 유연하고 선언적으로 관리할 수 있습니다. 매크로는 `App\Providers\AppServiceProvider`의 `boot` 메서드 내에서 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * 어플리케이션 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    Http::macro('github', function () {
        return Http::withHeaders([
            'X-Example' => 'example',
        ])->baseUrl('https://github.com');
    });
}
```

매크로가 설정된 후에는 어디서든 해당 매크로를 호출하여 지정된 설정을 가진 pending 요청을 생성할 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

Laravel의 여러 서비스는 테스트 작성을 쉽게 도와주는 다양한 기능을 제공합니다. HTTP 클라이언트도 예외가 아닙니다. `Http` 파사드의 `fake` 메서드는 테스트 시 요청을 보낼 때 더미/가짜 응답을 반환하게 할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜 처리

예를 들어, 모든 요청에 대해 비어 있고 200 상태 코드를 가진 응답을 반환하게 하려면 인자 없이 `fake` 메서드를 호출하면 됩니다:

    use Illuminate\Support\Facades\Http;

    Http::fake();

    $response = Http::post(/* ... */);

<a name="faking-specific-urls"></a>
#### 특정 URL 가짜 처리

또는 배열을 `fake` 메서드에 전달할 수도 있습니다. 배열의 키는 가짜 요청을 위한 URL 패턴, 값은 해당 응답입니다. `*`는 와일드카드로 사용할 수 있습니다. 가짜 설정되지 않은 요청은 실제로 전송됩니다. 이때 `Http` 파사드의 `response` 메서드를 사용해 더미 응답을 만들 수 있습니다:

    Http::fake([
        // GitHub 엔드포인트에 대한 JSON 응답 더미 처리...
        'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

        // Google 엔드포인트에 대해 문자열 응답 더미 처리...
        'google.com/*' => Http::response('Hello World', 200, $headers),
    ]);

매치되지 않은 모든 URL에 대한 기본 반환 응답을 지정하려면 `*`를 사용할 수 있습니다:

    Http::fake([
        // GitHub 엔드포인트에 대한 JSON 응답...
        'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

        // 모든 다른 엔드포인트에 대해 문자열 반환...
        '*' => Http::response('Hello World', 200, ['Headers']),
    ]);

<a name="faking-response-sequences"></a>
#### 순차적 응답 가짜 처리

특정 URL에 대해 순차적으로 일련의 가짜 응답을 반환해야 할 때가 있습니다. 이럴 때는 `Http::sequence` 메서드를 사용하여 응답 시퀀스를 구성할 수 있습니다:

    Http::fake([
        // GitHub 엔드포인트에 대해 응답 시퀀스 설정...
        'github.com/*' => Http::sequence()
                                ->push('Hello World', 200)
                                ->push(['foo' => 'bar'], 200)
                                ->pushStatus(404),
    ]);

시퀀스의 모든 응답이 소진되면 추가 요청 시 예외가 발생합니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용하세요.

    Http::fake([
        // GitHub 엔드포인트에 대해 응답 시퀀스 설정...
        'github.com/*' => Http::sequence()
                                ->push('Hello World', 200)
                                ->push(['foo' => 'bar'], 200)
                                ->whenEmpty(Http::response()),
    ]);

특정 URL 패턴 없이 응답 시퀀스를 가짜 처리할 때는 `Http::fakeSequence`를 사용할 수 있습니다.

    Http::fakeSequence()
            ->push('Hello World', 200)
            ->whenEmpty(Http::response());

<a name="fake-callback"></a>
#### 가짜 콜백

엔드포인트별로 반환할 응답을 동적으로 결정해야 하는 복잡한 로직이 필요하다면, `fake`에 클로저를 넘길 수 있습니다. 이 콜백은 `Illuminate\Http\Client\Request` 인스턴스를 받고, 반환값으로 응답 인스턴스를 반환해야 합니다.

    use Illuminate\Http\Client\Request;

    Http::fake(function (Request $request) {
        return Http::response('Hello World', 200);
    });

<a name="preventing-stray-requests"></a>
### 불필요한 요청 방지

테스트 전체 또는 테스트 케이스 내에서 HTTP 클라이언트로 보낸 모든 요청이 반드시 가짜 처리되도록 강제하고 싶다면, `preventStrayRequests` 메서드를 사용할 수 있습니다. 이후 가짜 처리가 없는 요청은 실제 요청하는 대신 예외를 발생시킵니다.

    use Illuminate\Support\Facades\Http;

    Http::preventStrayRequests();

    Http::fake([
        'github.com/*' => Http::response('ok'),
    ]);

    // "ok" 응답 반환
    Http::get('https://github.com/laravel/framework');

    // 예외 발생
    Http::get('https://laravel.com');

<a name="inspecting-requests"></a>
### 요청 검사

응답을 가짜 처리할 때, 클라이언트가 받은 요청이 예상대로 데이터와 헤더를 보내는지 검사하고 싶을 수 있습니다. `Http::fake` 호출 후 `Http::assertSent` 메서드를 사용하면 됩니다.

`assertSent`는 클로저를 인자로 받으며, 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받고, 테스트가 통과하려면 true를 반환해야 합니다. 지정한 조건과 일치하는 요청이 하나라도 보내지면 테스트는 성공합니다:

    use Illuminate\Http\Client\Request;
    use Illuminate\Support\Facades\Http;

    Http::fake();

    Http::withHeaders([
        'X-First' => 'foo',
    ])->post('http://example.com/users', [
        'name' => 'Taylor',
        'role' => 'Developer',
    ]);

    Http::assertSent(function (Request $request) {
        return $request->hasHeader('X-First', 'foo') &&
               $request->url() == 'http://example.com/users' &&
               $request['name'] == 'Taylor' &&
               $request['role'] == 'Developer';
    });

특정 요청이 전송되지 않았음을 확인하고 싶다면 `assertNotSent` 메서드를 사용할 수 있습니다:

    use Illuminate\Http\Client\Request;
    use Illuminate\Support\Facades\Http;

    Http::fake();

    Http::post('http://example.com/users', [
        'name' => 'Taylor',
        'role' => 'Developer',
    ]);

    Http::assertNotSent(function (Request $request) {
        return $request->url() === 'http://example.com/posts';
    });

테스트에서 "전송"된 요청 수를 검증하려면 `assertSentCount`를 사용하세요.

    Http::fake();

    Http::assertSentCount(5);

또는, 테스트 중 아무 요청도 보내지지 않았음을 검증하려면 `assertNothingSent`를 사용할 수 있습니다.

    Http::fake();

    Http::assertNothingSent();

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용해 모든 요청과 그에 따른 응답을 수집할 수 있습니다. `recorded`는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response`의 쌍(chained array) 컬렉션을 반환합니다.

```php
Http::fake([
    'https://laravel.com' => Http::response(status: 500),
    'https://nova.laravel.com/' => Http::response(),
]);

Http::get('https://laravel.com');
Http::get('https://nova.laravel.com/');

$recorded = Http::recorded();

[$request, $response] = $recorded[0];
```

추가적으로, `recorded` 메서드는 클로저를 받아 각 `Illuminate\Http\Client\Request`, `Illuminate\Http\Client\Response` 조합에 대해 필터링할 수 있습니다:

```php
use Illuminate\Http\Client\Request;
use Illuminate\Http\Client\Response;

Http::fake([
    'https://laravel.com' => Http::response(status: 500),
    'https://nova.laravel.com/' => Http::response(),
]);

Http::get('https://laravel.com');
Http::get('https://nova.laravel.com/');

$recorded = Http::recorded(function (Request $request, Response $response) {
    return $request->url() !== 'https://laravel.com' &&
           $response->successful();
});
```

<a name="events"></a>
## 이벤트

Laravel은 HTTP 요청 처리 과정에서 세 개의 이벤트를 발생시킵니다. 요청이 전송되기 전에 `RequestSending` 이벤트가 발생하고, 요청에 대한 응답을 받은 후 `ResponseReceived` 이벤트가 발생합니다. 특정 요청에 대한 응답을 받지 못한 경우 `ConnectionFailed` 이벤트가 발생합니다.

`RequestSending`와 `ConnectionFailed` 이벤트는 `Illuminate\Http\Client\Request` 인스턴스를 확인할 수 있는 public `$request` 프로퍼티를 포함합니다. `ResponseReceived`는 `$request` 및 `$response` 프로퍼티를 포함하며, 이는 `Illuminate\Http\Client\Response` 인스턴스를 확인하는 데 사용할 수 있습니다. 해당 이벤트에 대한 리스너는 `App\Providers\EventServiceProvider`의 `$listen` 프로퍼티에 등록할 수 있습니다:

    /**
     * 어플리케이션 이벤트 리스너 매핑.
     *
     * @var array
     */
    protected $listen = [
        'Illuminate\Http\Client\Events\RequestSending' => [
            'App\Listeners\LogRequestSending',
        ],
        'Illuminate\Http\Client\Events\ResponseReceived' => [
            'App\Listeners\LogResponseReceived',
        ],
        'Illuminate\Http\Client\Events\ConnectionFailed' => [
            'App\Listeners\LogConnectionFailed',
        ],
    ];