# HTTP 클라이언트 (HTTP Client)

- [소개](#introduction)
- [요청 만들기](#making-requests)
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
    - [요청 검증](#inspecting-requests)
    - [원하지 않는 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 기반으로 하는 표현력 있으면서도 최소한의 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 통신하기 위해 빠르게 HTTP 요청을 보낼 수 있습니다. Laravel이 Guzzle을 감싸는 래퍼는 가장 일반적인 사용 사례에 초점을 맞추었으며, 개발자 경험을 크게 향상시킵니다.

<a name="making-requests"></a>
## 요청 만들기 (Making Requests)

요청을 만들기 위해 `Http` 퍼사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저 기본적인 다른 URL로의 `GET` 요청 예제를 살펴보겠습니다:

```
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이 객체는 응답을 검사하는 데 사용할 수 있는 다양한 메서드를 제공합니다:

```
$response->body() : string;
$response->json($key = null, $default = null) : mixed;
$response->object() : object;
$response->collect($key = null) : Illuminate\Support\Collection;
$response->resource() : resource;
$response->status() : int;
$response->successful() : bool;
$response->redirect(): bool;
$response->failed() : bool;
$response->clientError() : bool;
$response->header($header) : string;
$response->headers() : array;
```

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하므로 JSON 응답 데이터를 직접 배열 접근하듯이 가져올 수도 있습니다:

```
return Http::get('http://example.com/users/1')['name'];
```

위에 나열된 응답 메서드 외에도, 다음 메서드들로 특정 상태 코드인지 확인할 수 있습니다:

```
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
```

<a name="uri-templates"></a>
#### URI 템플릿 (URI Templates)

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 사용해 요청 URL을 구성할 수 있습니다. URL 매개변수는 `withUrlParameters` 메서드를 사용해 정의할 수 있습니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '11.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 내용 덤프 (Dumping Requests)

보내기 전의 요청 인스턴스를 덤프하고 스크립트 실행을 종료하고 싶다면, 요청 정의의 시작 부분에 `dd` 메서드를 추가하세요:

```
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터 (Request Data)

`POST`, `PUT`, `PATCH` 요청을 할 때 추가 데이터를 전송하는 일이 일반적입니다. 이들 메서드는 두 번째 인수로 배열 형태의 데이터를 받습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청 시 URL에 직접 쿼리 문자열을 붙이거나, `get` 메서드 두 번째 인수로 키/값 쌍의 배열을 전달할 수 있습니다:

```
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는 `withQueryParameters` 메서드를 사용할 수도 있습니다:

```
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users')
```

<a name="sending-form-url-encoded-requests"></a>
#### Form URL Encoded 요청 보내기

데이터를 `application/x-www-form-urlencoded` 콘텐츠 타입으로 전송하고 싶다면, 요청 전에 `asForm` 메서드를 호출하세요:

```
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### RAW 요청 본문 전송

요청 시 원시(raw) 본문을 제공하고 싶다면 `withBody` 메서드를 사용하세요. 콘텐츠 타입은 메서드의 두 번째 인수로 지정할 수 있습니다:

```
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청 (Multi-Part Requests)

파일을 멀티파트 요청으로 전송하려면, 요청 전에 `attach` 메서드를 호출하세요. 이 메서드는 파일명(폼 필드 명)과 내용(바이트) 두 개를 받습니다. 필요에 따라 세 번째 인수로 파일 이름, 네 번째 인수로 파일 관련 헤더를 전달할 수 있습니다:

```
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 실제 내용을 넘기지 않고 스트림 리소스를 사용할 수도 있습니다:

```
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더 (Headers)

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용하세요. 이 메서드는 키/값 배열을 인수로 받습니다:

```
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` 메서드로는 요청에 대해 기대하는 응답 콘텐츠 타입을 지정할 수 있습니다:

```
$response = Http::accept('application/json')->get('http://example.com/users');
```

간편하게 `acceptJson` 메서드를 사용해 `application/json` 타입을 빠르게 지정할 수도 있습니다:

```
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 헤더에 새 헤더를 병합합니다. 완전히 대체하고 싶으면 `replaceHeaders` 메서드를 사용하세요:

```php
$response = Http::withHeaders([
    'X-Original' => 'foo',
])->replaceHeaders([
    'X-Replacement' => 'bar',
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

<a name="authentication"></a>
### 인증 (Authentication)

기본 및 다이제스트 인증은 각각 `withBasicAuth`와 `withDigestAuth` 메서드로 지정 가능합니다:

```
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

`Authorization` 헤더에 Bearer 토큰을 빠르게 추가하려면 `withToken` 메서드를 사용하세요:

```
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃 (Timeout)

`timeout` 메서드는 응답을 기다릴 최대 시간을 초 단위로 지정합니다. 기본값은 30초입니다:

```
$response = Http::timeout(3)->get(/* ... */);
```

제한 시간을 초과하면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버 연결 시도에 걸리는 최대 초를 지정하려면 `connectTimeout` 메서드를 사용하세요:

```
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도 (Retries)

클라이언트 또는 서버 에러가 발생하면 HTTP 클라이언트가 자동으로 재시도하도록 하려면 `retry` 메서드를 사용하세요. `retry`는 최대 재시도 횟수와 재시도 사이의 대기 시간(밀리초)을 인수로 받습니다:

```
$response = Http::retry(3, 100)->post(/* ... */);
```

재시도 사이 대기 시간을 직접 계산하고 싶다면, 두 번째 인수로 클로저를 전달할 수 있습니다. 클로저는 재시도 횟수와 예외 인스턴스를 받으며, 밀리초 단위 대기 시간을 반환해야 합니다:

```
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

편의를 위해 첫 번째 인수로 밀리초 배열을 전달할 수도 있으며, 각 시도 전 대기 시간이 배열 순서대로 지정됩니다:

```
$response = Http::retry([100, 200])->post(/* ... */);
```

세 번째 인수로 재시도 여부를 결정하는 callable 함수를 전달할 수 있습니다. 예를 들어, `ConnectionException`인 경우에만 재시도하도록 할 수 있습니다:

```
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

재시도 시마다 요청을 수정하고 싶을 수 있습니다. `retry` 메서드에 넘기는 callable의 두 번째 인수로 전달되는 요청 인스턴스를 수정하면 됩니다. 예를 들어 첫 시도에서 인증 실패(401)가 있으면 토큰을 새로 발급해 재시도하도록 할 수 있습니다:

```
use Exception;
use Illuminate\Http\Client\PendingRequest;
use Illuminate\Http\Client\RequestException;

$response = Http::withToken($this->getToken())->retry(2, 0, function (Exception $exception, PendingRequest $request) {
    if (! $exception instanceof RequestException || $exception->response->status() !== 401) {
        return false;
    }

    $request->withToken($this->getNewToken());

    return true;
})->post(/* ... */);
```

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException`이 발생합니다. 이 동작을 끄려면 `throw` 인수에 `false`를 지정하세요. 비활성화 시 재시도 후 마지막 응답을 반환합니다:

```
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]  
> 만약 모든 요청이 연결 문제로 실패한다면 `throw`가 `false`여도 `Illuminate\Http\Client\ConnectionException`은 여전히 발생합니다.

<a name="error-handling"></a>
### 에러 처리 (Error Handling)

Guzzle 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트 또는 서버 쪽 에러(`400`, `500` 번대 응답) 시 예외를 발생시키지 않습니다. 반환된 응답에서 이들 에러 여부를 다음 메서드로 확인할 수 있습니다:

```
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 상태 코드가 400번대인지 확인...
$response->clientError();

// 상태 코드가 500번대인지 확인...
$response->serverError();

// 클라이언트 또는 서버 에러가 있을 경우 즉시 콜백 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생 (Throwing Exceptions)

응답 인스턴스가 있고, 클라이언트 혹은 서버 에러시 `Illuminate\Http\Client\RequestException`을 발생시키고 싶다면 `throw` 또는 `throwIf` 메서드를 사용하세요:

```
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 에러가 있으면 예외 발생...
$response->throw();

// 에러가 있고 조건이 참이면 예외 발생...
$response->throwIf($condition);

// 에러가 있고 주어진 클로저가 true를 반환하면 예외 발생...
$response->throwIf(fn (Response $response) => true);

// 에러가 있고 조건이 거짓이면 예외 발생...
$response->throwUnless($condition);

// 에러가 있고 주어진 클로저가 false를 반환하면 예외 발생...
$response->throwUnless(fn (Response $response) => false);

// 특정 상태 코드일 때 예외 발생...
$response->throwIfStatus(403);

// 특정 상태 코드가 아닐 때 예외 발생...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`RequestException` 인스턴스는 `$response` 공용 속성을 가지고 있어 반환된 응답을 확인할 수 있습니다.

`throw` 메서드는 에러가 없으면 응답 인스턴스를 반환해서 다른 메서드를 체인으로 이어갈 수 있습니다:

```
return Http::post(/* ... */)->throw()->json();
```

예외 발생 전에 추가 작업을 하고 싶다면, `throw` 메서드에 클로저를 넘길 수 있습니다. 클로저 내부에서 예외를 다시 던질 필요 없이 자동으로 예외가 발생합니다:

```
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본 설정으로 `RequestException` 로그 메시지는 120자까지만 기록됩니다. 이 동작은 `bootstrap/app.php`에서 예외 처리 설정 시 `truncateRequestExceptionsAt` 또는 `dontTruncateRequestExceptions` 메서드로 조정하거나 비활성화할 수 있습니다:

```
->withExceptions(function (Exceptions $exceptions) {
    // 요청 예외 메시지를 240자까지만 자르기...
    $exceptions->truncateRequestExceptionsAt(240);

    // 요청 예외 메시지 자르기 비활성화...
    $exceptions->dontTruncateRequestExceptions();
})
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어 (Guzzle Middleware)

Laravel HTTP 클라이언트는 Guzzle을 기반으로 하므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 보낼 요청을 조작하거나 응답을 검사할 수 있습니다. 요청을 조작하려면 `withRequestMiddleware` 메서드로 미들웨어를 등록하세요:

```
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 응답을 검사하려면 `withResponseMiddleware` 메서드에 미들웨어를 등록할 수 있습니다:

```
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\ResponseInterface;

$response = Http::withResponseMiddleware(
    function (ResponseInterface $response) {
        $header = $response->getHeader('X-Example');

        // ...

        return $response;
    }
)->get('http://example.com');
```

<a name="global-middleware"></a>
#### 전역 미들웨어 (Global Middleware)

모든 요청과 응답에 적용할 미들웨어를 등록하고 싶다면, `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용하세요. 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Http;

Http::globalRequestMiddleware(fn ($request) => $request->withHeader(
    'User-Agent', 'Example Application/1.0'
));

Http::globalResponseMiddleware(fn ($response) => $response->withHeader(
    'X-Finished-At', now()->toDateTimeString()
));
```

<a name="guzzle-options"></a>
### Guzzle 옵션 (Guzzle Options)

외부 요청에 대해 추가 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정하려면 `withOptions` 메서드를 사용하세요. 인수는 키/값 배열입니다:

```
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션 (Global Options)

모든 요청의 기본 옵션을 설정하려면 `globalOptions` 메서드를 사용하세요. 역시 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Http::globalOptions([
        'allow_redirects' => false,
    ]);
}
```

<a name="concurrent-requests"></a>
## 동시 요청 (Concurrent Requests)

때로는 여러 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 순차가 아닌 동시에 여러 요청을 발송해 느린 HTTP API와 통신 시 성능을 크게 높일 수 있습니다.

이럴 때는 `pool` 메서드를 사용하세요. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 받는 클로저를 인수로 받고, 요청 풀에 요청을 쉽게 추가할 수 있습니다:

```
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
```

각 응답은 추가된 순서대로 배열 인덱스에 접근할 수 있습니다. 필요하다면 `as` 메서드로 요청에 이름을 붙여, 응답을 이름으로도 조회할 수 있습니다:

```
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->as('first')->get('http://localhost/first'),
    $pool->as('second')->get('http://localhost/second'),
    $pool->as('third')->get('http://localhost/third'),
]);

return $responses['first']->ok();
```

<a name="customizing-concurrent-requests"></a>
#### 동시 요청 맞춤 설정

`pool` 메서드는 `withHeaders`, `middleware` 같은 다른 HTTP 클라이언트 메서드와 체인할 수 없습니다. 각 요청마다 헤더나 미들웨어를 적용하려면, 풀 내 요청 각각에 설정해 주세요:

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$headers = [
    'X-Example' => 'example',
];

$responses = Http::pool(fn (Pool $pool) => [
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
]);
```

<a name="macros"></a>
## 매크로 (Macros)

Laravel HTTP 클라이언트는 매크로를 정의할 수 있습니다. 매크로는 애플리케이션 내에서 서비스와 상호작용할 때 공통 요청 경로나 헤더 구성을 표현력 있게 정의해 둘 수 있는 방법입니다. 매크로는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Http::macro('github', function () {
        return Http::withHeaders([
            'X-Example' => 'example',
        ])->baseUrl('https://github.com');
    });
}
```

매크로가 설정되면, 애플리케이션 어디서든 호출해 지정된 설정으로 요청을 만들 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

많은 Laravel 서비스가 쉽고 표현력 있는 테스트 작성 기능을 제공하며, HTTP 클라이언트도 그렇습니다. `Http` 퍼사드의 `fake` 메서드를 사용하면 요청이 발생할 때 가짜/스텁 응답을 반환하도록 할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜 처리 (Faking Responses)

예를 들어, 모든 요청에 대해 빈 200 응답을 반환하려면 `fake` 메서드를 인수 없이 호출하세요:

```
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 가짜 처리

또는 `fake` 메서드에 배열을 전달할 수 있습니다. 키는 가짜 처리할 URL 패턴, 값은 대응 응답입니다. `*`는 와일드카드로 사용할 수 있습니다. 가짜 처리하지 않은 URL 요청은 실제로 실행됩니다. `Http::response` 메서드로 스텁/가짜 응답을 쉽게 만들 수 있습니다:

```
Http::fake([
    // GitHub 엔드포인트에 대해 JSON 응답 스텁...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대해 문자열 응답 스텁...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

모든 매치되지 않은 URL을 가짜 처리하는 기본값을 지정하려면 단일 `*`를 키로 사용하세요:

```
Http::fake([
    // GitHub 엔드포인트 JSON 스텁...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트 문자열 응답...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

간단한 문자열, JSON, 빈 응답은 문자열, 배열, 정수를 바로 값으로 지정해 생성할 수도 있습니다:

```
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 연결 예외 가짜 처리

HTTP 클라이언트가 `Illuminate\Http\Client\ConnectionException` 예외를 던질 때 애플리케이션 동작을 테스트해야 할 수도 있습니다. `failedConnection` 메서드를 사용해 연결 예외 발생을 가짜 처리할 수 있습니다:

```
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 가짜 처리

하나의 URL에 대해 여러 가짜 응답을 순차적으로 반환하고 싶다면 `Http::sequence` 메서드를 사용하세요:

```
Http::fake([
    // GitHub 엔드포인트에 응답 시퀀스 스텁...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

시퀀스의 모든 응답이 소진되면 이후 요청은 예외를 발생시킵니다. 빈 시퀀스일 때 반환할 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용하세요:

```
Http::fake([
    // GitHub에 응답 시퀀스 스텁...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴 지정 없이 응답 시퀀스를 가짜 처리하려면 `Http::fakeSequence` 메서드를 사용할 수 있습니다:

```
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 가짜 처리 콜백

응답을 반환할 때 더 복잡한 조건부 로직이 필요하다면, `fake` 메서드에 클로저를 전달하세요. 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받고 적절한 응답을 반환해야 합니다:

```
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="preventing-stray-requests"></a>
### 원하지 않는 요청 방지 (Preventing Stray Requests)

테스트 중 모든 요청이 가짜 처리되었는지 보장하려면 `preventStrayRequests` 메서드를 호출하세요. 호출 후 가짜 응답이 없는 요청은 실제 요청 대신 예외가 발생합니다:

```
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답 반환...
Http::get('https://github.com/laravel/framework');

// 예외 발생...
Http::get('https://laravel.com');
```

<a name="inspecting-requests"></a>
### 요청 검증 (Inspecting Requests)

가짜 응답을 사용하는 동안, 클라이언트가 올바른 데이터나 헤더를 보내는지 확인하기 위해 요청 내용을 검사할 수 있습니다. `Http::fake` 후 `Http::assertSent` 메서드를 호출하면 됩니다.

`assertSent`는 `Illuminate\Http\Client\Request` 인스턴스를 받는 클로저를 인수로 받아 요청이 예상에 부합하는지 불린으로 반환합니다. 테스트가 통과하려면 조건에 맞는 요청이 최소 하나 이상 존재해야 합니다:

```
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
```

특정 요청이 보내지 않았음을 검증하려면 `assertNotSent` 메서드를 사용하세요:

```
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
```

테스트 중 보낸 요청 수를 확인하려면 `assertSentCount` 메서드를 사용할 수 있습니다:

```
Http::fake();

Http::assertSentCount(5);
```

아예 요청을 보내지 않았음을 확인하려면 `assertNothingSent` 메서드를 호출하세요:

```
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청 및 응답 기록 (Recording Requests / Responses)

`recorded` 메서드는 모든 요청과 대응되는 응답을 수집합니다. 반환값은 각각 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스 쌍으로 이루어진 컬렉션입니다:

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

또한 `recorded`는 클로저를 받아 요청/응답 쌍을 필터링할 수 있습니다:

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
## 이벤트 (Events)

Laravel은 HTTP 요청 전송 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청을 보내기 직전에, `ResponseReceived` 이벤트는 요청에 대한 응답을 받은 후에, `ConnectionFailed` 이벤트는 응답을 받지 못했을 때 각각 발생합니다.

`RequestSending`과 `ConnectionFailed` 이벤트에는 `Illuminate\Http\Client\Request` 인스턴스가 담긴 공용 `$request` 속성이 있습니다. `ResponseReceived` 이벤트에는 `$request`와 응답 인스턴스를 담은 `$response` 속성이 있습니다. 애플리케이션 내에서 이 이벤트들에 대한 [리스너](/docs/11.x/events)를 작성할 수 있습니다:

```
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 이벤트 핸들러
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```