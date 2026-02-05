# HTTP 클라이언트 (HTTP Client)

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
    - [요청 풀링](#request-pooling)
    - [요청 배치 처리](#request-batching)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 페이크 처리](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [의도치 않은 요청 차단](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/) 위에 표현적이고 간결한 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 빠르게 HTTP 요청을 주고받을 수 있습니다. Laravel에서 제공하는 Guzzle 래퍼는 가장 일반적인 사용 사례와 개발자 경험에 초점을 맞추고 있습니다.

<a name="making-requests"></a>
## 요청 보내기 (Making Requests)

요청을 보내려면 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 우선 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이 객체는 응답을 점검할 수 있는 다양한 메서드를 제공합니다:

```php
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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하므로, JSON 응답 데이터를 배열처럼 바로 접근할 수 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```

위에서 소개한 응답 메서드 외에도, 특정 응답 상태 코드를 판별할 수 있는 다음과 같은 메서드들도 사용할 수 있습니다:

```php
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
#### URI 템플릿

HTTP 클라이언트는 [URI 템플릿 사양](https://www.rfc-editor.org/rfc/rfc6570)을 활용해 요청 URL을 손쉽게 구성할 수 있습니다. URI 템플릿에서 확장할 URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용합니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프(Dump) 출력

요청을 실제로 전송하기 전, 요청 인스턴스를 확인하고 스크립트 실행을 중지하고 싶다면, 요청 정의의 시작 부분에 `dd` 메서드를 추가하면 됩니다:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터 (Request Data)

`POST`, `PUT`, `PATCH` 요청을 보낼 때는 추가 데이터를 함께 전달하는 경우가 많습니다. 이런 메서드들은 두 번째 인수로 데이터 배열을 받을 수 있습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 할 때는 쿼리 스트링을 직접 URL에 붙이거나, 두 번째 인수로 키/값 쌍의 배열을 넘길 수 있습니다:

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는, `withQueryParameters` 메서드를 사용할 수도 있습니다:

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
#### 폼 URL 인코딩 방식의 요청 전송

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내고 싶다면 요청 전에 `asForm` 메서드를 호출하세요:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 본문 전송

요청을 보낼 때, 직접 raw 본문을 지정하고자 할 때는 `withBody` 메서드를 사용할 수 있습니다. 두 번째 인수로 콘텐츠 타입을 지정할 수 있습니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트(Multi-Part) 요청

파일을 멀티파트 요청으로 전송하고 싶을 때는 요청 전에 `attach` 메서드를 사용하세요. 이 메서드는 파일의 이름과 내용을 받습니다. 필요하다면 세 번째 인수에 파일명을, 네 번째 인수에는 파일과 관련된 헤더를 지정할 수 있습니다:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 raw 내용을 전달하는 대신, 스트림 리소스를 넘길 수도 있습니다:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더 (Headers)

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용합니다. 이 메서드는 키/값 쌍의 배열을 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

요청에 대해 애플리케이션이 응답에서 기대하는 콘텐츠 타입을 지정하려면 `accept` 메서드를 사용할 수 있습니다:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

더 간편하게 `application/json` 타입을 기대한다면 `acceptJson` 메서드를 사용할 수 있습니다:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 새로운 헤더를 기존 요청 헤더에 병합합니다. 모든 헤더를 완전히 교체하고 싶다면 `replaceHeaders` 메서드를 사용하세요:

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

기본 인증(Basic Authentication)과 다이제스트 인증(Digest Authentication) 정보를 각각 `withBasicAuth` 및 `withDigestAuth` 메서드로 지정할 수 있습니다:

```php
// Basic authentication...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest authentication...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### 베어러 토큰(Bearer Tokens)

`Authorization` 헤더로 간편하게 베어러 토큰을 추가하고 싶다면 `withToken` 메서드를 사용하세요:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃 (Timeout)

응답을 기다리는 최대 초 수는 `timeout` 메서드로 지정할 수 있습니다. 기본값은 30초입니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버에 연결을 시도하는 동안 대기할 최대 초 수를 지정하려면 `connectTimeout` 메서드를 사용하세요. 기본값은 10초입니다:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도 (Retries)

클라이언트 또는 서버 에러가 발생했을 때 요청을 자동으로 재시도하고 싶다면 `retry` 메서드를 사용할 수 있습니다. 이 메서드는 요청을 최대 몇 번까지 시도할지, 각 시도 사이에 Laravel이 기다릴 밀리초(ms) 단위의 시간을 받습니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

시도 간 대기시간을 직접 계산하고 싶다면 두 번째 인수에 클로저를 전달할 수 있습니다:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

편의상, 첫 번째 인수로 배열을 제공할 수도 있습니다. 이 배열의 각 값은 각각 다음 시도 전 대기할 밀리초를 의미합니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면, 세 번째 인수로 콜러블(callable)을 전달할 수 있습니다. 이 콜러블이 true를 반환해야만 재시도가 실제로 이루어집니다. 예를 들어 최초 요청이 `ConnectionException` 발생 시에만 재시도하도록 할 수 있습니다:

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청 시도가 실패하면, 새로 시도하기 전에 요청을 변경하고 싶을 수 있습니다. 이럴 때는 `retry` 메서드에 넘긴 콜러블의 `request` 인수를 수정하면 됩니다. 예를 들어, 첫 요청에서 인증 에러가 발생하면 새 토큰으로 재시도할 수 있습니다:

```php
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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 이 동작을 비활성화하고 싶다면, `throw` 인자를 false로 지정하세요. 이 경우 모든 재시도가 끝난 뒤 마지막 응답 인스턴스가 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패하면, `throw` 인자를 false로 하더라도 `Illuminate\Http\Client\ConnectionException`이 여전히 발생합니다.

<a name="error-handling"></a>
### 에러 처리 (Error Handling)

Guzzle의 기본 동작과는 달리, Laravel HTTP 클라이언트 래퍼는 클라이언트/서버 에러(서버로부터의 400 또는 500 응답)에 대해 예외를 발생시키지 않습니다. 이러한 에러가 반환됐는지는 `successful`, `clientError`, `serverError` 메서드로 확인할 수 있습니다:

```php
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 400대 상태 코드인지 확인...
$response->clientError();

// 500대 상태 코드인지 확인...
$response->serverError();

// 클라이언트/서버 에러 시 바로 콜백 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생 (Throwing Exceptions)

응답 인스턴스에서 상태 코드가 클라이언트/서버 에러에 해당한다면, `Illuminate\Http\Client\RequestException` 예외를 발생시키고 싶을 때는 `throw` 또는 `throwIf` 메서드를 사용합니다:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트/서버 에러 발생 시 예외 발생...
$response->throw();

// 조건이 true이고 오류가 발생했을 때 예외 발생...
$response->throwIf($condition);

// 클로저가 true를 반환하고 오류가 발생했을 때 예외 발생...
$response->throwIf(fn (Response $response) => true);

// 조건이 false이고 오류가 발생했을 때 예외 발생...
$response->throwUnless($condition);

// 클로저가 false를 반환하고 오류가 발생했을 때 예외 발생...
$response->throwUnless(fn (Response $response) => false);

// 특정 상태 코드면 예외 발생...
$response->throwIfStatus(403);

// 특정 상태 코드가 아니면 예외 발생...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스는 public `$response` 속성을 가지고 있어 반환된 응답을 검사할 수 있습니다.

`throw` 메서드는 오류가 없을 경우 그 응답 인스턴스를 반환하므로, 이후 조작을 체이닝할 수 있습니다:

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전에 추가 작업을 하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저 호출 후 자동으로 예외가 재발생하므로, 클로저 내부에서 직접 예외를 재던질 필요는 없습니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로, `RequestException` 메시지는 로그 또는 리포트 시 120자까지 잘려서 기록됩니다. 이 동작을 커스터마이즈하거나 비활성화하려면, 애플리케이션의 `bootstrap/app.php`에서 `truncateAt` 또는 `dontTruncate` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Client\RequestException;

->registered(function (): void {
    // 예외 메시지를 240자로 잘라서 기록...
    RequestException::truncateAt(240);

    // 예외 메시지만 잘리지 않게 함...
    RequestException::dontTruncate();
})
```

또한, 요청별로 예외 메시지 잘림 동작을 `truncateExceptionsAt` 메서드로 설정할 수 있습니다:

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어 (Guzzle Middleware)

Laravel HTTP 클라이언트는 내부적으로 Guzzle을 사용하므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 요청을 조작하거나 응답을 확인할 수 있습니다. 요청을 조작하려면 `withRequestMiddleware` 메서드로 Guzzle 미들웨어를 등록하세요:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 응답을 검사하려면 `withResponseMiddleware` 메서드로 미들웨어를 등록할 수 있습니다:

```php
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
#### 글로벌 미들웨어

모든 아웃바운드 요청/인바운드 응답에 미들웨어를 적용하고 싶다면 `globalRequestMiddleware`, `globalResponseMiddleware` 메서드를 사용하세요. 보통 이 메서드들은 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 사용하려면, `withOptions` 메서드에 배열로 지정할 수 있습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 글로벌 옵션

모든 요청에 기본 옵션을 지정하고 싶다면, `globalOptions` 메서드를 이용합니다. 이 역시 보통 `AppServiceProvider`의 `boot` 메서드에서 사용합니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스 부트스트랩 메서드.
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

여러 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 여러 요청을 순차적으로가 아니라 한 번에 병렬로 전송하고 싶을 때입니다. 이는 느린 HTTP API와 통신할 때 성능을 크게 향상시킬 수 있습니다.

<a name="request-pooling"></a>
### 요청 풀링 (Request Pooling)

이런 경우 `pool` 메서드를 이용하면 됩니다. `pool` 메서드는 클로저를 받고, 이 클로저는 `Illuminate\Http\Client\Pool` 인스턴스를 전달받아 여러 요청을 쉽게 한 번에 추가할 수 있습니다:

```php
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

각 응답 인스턴스는 풀에 추가된 순서대로 배열 인덱스 또는 이름으로 접근할 수 있습니다. 요청에 이름을 붙여서 응답에 이름으로도 접근할 수 있습니다:

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->as('first')->get('http://localhost/first'),
    $pool->as('second')->get('http://localhost/second'),
    $pool->as('third')->get('http://localhost/third'),
]);

return $responses['first']->ok();
```

요청 풀의 최대 동시 전송 수(concurrency)는 `pool` 메서드의 `concurrency` 인자로 제어할 수 있습니다:

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

<a name="customizing-concurrent-requests"></a>
#### 동시 요청 커스터마이징

`pool` 메서드는 `withHeaders`나 `middleware` 같은 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀에 들어가는 개별 요청마다 직접 옵션을 지정해야 합니다:

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

<a name="request-batching"></a>
### 요청 배치 처리 (Request Batching)

Laravel에서 동시 요청을 다루는 또 다른 방법은 `batch` 메서드를 사용하는 것입니다. 이 메서드 역시 클로저를 받아 `Illuminate\Http\Client\Batch` 인스턴스를 전달하고, 요청 풀에 쉽게 요청들을 추가할 수 있을 뿐만 아니라 완료 콜백도 지정할 수 있습니다:

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\RequestException;
use Illuminate\Http\Client\Response;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->before(function (Batch $batch) {
    // 배치가 생성됐지만 아직 실행 전...
})->progress(function (Batch $batch, int|string $key, Response $response) {
    // 개별 요청이 성공적으로 완료됨...
})->then(function (Batch $batch, array $results) {
    // 모든 요청이 성공적으로 완료됨...
})->catch(function (Batch $batch, int|string $key, Response|RequestException|ConnectionException $response) {
    // 첫 실패 발생 시 처리...
})->finally(function (Batch $batch, array $results) {
    // 배치 실행이 마감됨...
})->send();
```

`pool` 메서드와 마찬가지로 `as` 메서드로 요청에 이름을 붙일 수 있습니다:

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

`send` 메서드를 호출해 `batch`가 실행된 이후에는 더 이상 새로운 요청을 추가할 수 없습니다. 시도하면 `Illuminate\Http\Client\BatchInProgressException` 예외가 발생합니다.

배치의 최대 동시 처리 개수는 `concurrency` 메서드로 지정할 수 있습니다:

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a name="inspecting-batches"></a>
#### 배치 검사

완료 콜백에 전달되는 `Illuminate\Http\Client\Batch` 인스턴스는 배치 요청과 상호작용하거나 점검하는 데 도움이 되는 여러 속성과 메서드를 제공합니다:

```php
// 배치에 할당된 요청 수
$batch->totalRequests;
 
// 아직 처리되지 않은 요청 수
$batch->pendingRequests;
 
// 실패한 요청 수
$batch->failedRequests;

// 지금까지 처리된 요청 수
$batch->processedRequests();

// 배치 실행 완료 여부
$batch->finished();

// 배치에 실패한 요청이 있는지
$batch->hasFailures();
```

<a name="deferring-batches"></a>
#### 배치 실행 지연

`defer` 메서드를 사용하면, 해당 요청 배치는 즉시 실행되지 않습니다. 대신 현재 애플리케이션 요청의 HTTP 응답이 사용자에게 전송된 후에 비로소 실행됩니다. 이를 통해 애플리케이션이 더욱 빠르고 반응성 있게 느껴질 수 있습니다:

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->then(function (Batch $batch, array $results) {
    // 모든 요청 성공...
})->defer();
```

<a name="macros"></a>
## 매크로 (Macros)

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있습니다. 매크로를 이용하면 애플리케이션 전반에 걸쳐 자주 쓰는 요청 경로나 헤더 구성을 fluent하게 재사용할 수 있습니다. 매크로는 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에 정의합니다:

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

매크로 설정이 끝나면, 애플리케이션 어디서든 해당 매크로를 호출해 미리 정의된 설정이 적용된 PendingRequest를 만들 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

Laravel의 여러 서비스는 테스트 작성이 쉽고 직관적이도록 다양한 기능을 제공합니다. HTTP 클라이언트 역시 마찬가지로, `Http` 파사드의 `fake` 메서드를 사용해 HTTP 요청 시 모의/더미 응답을 반환하도록 지정할 수 있습니다.

<a name="faking-responses"></a>
### 응답 페이크 처리 (Faking Responses)

예를 들어, 모든 요청에 대해 빈 200 코드 응답을 반환하도록 하려면 인수 없이 `fake` 메서드를 호출하면 됩니다:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL에 대한 응답 페이크

또한, 배열을 `fake` 메서드에 넘길 수 있습니다. 배열의 키는 페이크 처리할 URL 패턴이고 값은 응답입니다. `*` 문자는 와일드카드로 사용할 수 있습니다. `Http` 파사드의 `response` 메서드로 엔드포인트마다 가짜 응답을 유연하게 만들 수도 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 JSON 응답 페이크 지정...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 문자열 응답 페이크 지정...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

페이크가 지정되지 않은 URL로의 요청은 실제로 전송됩니다. 모든 기타 URL에 대해서도 페이크로 대체하고 싶다면 와일드카드 키 `*`만 사용하세요:

```php
Http::fake([
    // GitHub 엔드포인트용 JSON 응답 페이크...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 나머지 모든 엔드포인트에 문자열 응답...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

편의를 위해, 응답으로 문자열, 배열 또는 정수만 지정해 간단하게 문자열, JSON, 빈 응답을 만들 수도 있습니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 페이크 처리

요청 시 `Illuminate\Http\Client\ConnectionException`이 발생하는 경우를 테스트하고 싶을 수 있습니다. 이럴 때는 `failedConnection` 메서드를 사용해 HTTP 클라이언트가 연결 예외를 발생시켜야 함을 지정할 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException` 발생 상황을 테스트하고 싶다면 `failedRequest` 메서드를 사용하세요:

```php
$this->mock(GithubService::class);
    ->shouldReceive('getUser')
    ->andThrow(
        Http::failedRequest(['code' => 'not_found'], 404)
    );
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 페이크

때론 동일 URL에서 여러 개의 페이크 응답 시나리오를 순서대로 반환하도록 지정해야 할 때도 있습니다. 이럴 때는 `Http::sequence` 메서드를 활용해 응답 시퀀스를 구성할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 여러 응답 순차적으로 지정...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

시퀀스 내 모든 응답이 소진되면 추후 요청에서는 예외가 발생합니다. 시퀀스가 모두 소진된 경우의 기본 응답을 지정하려면 `whenEmpty`를 사용합니다:

```php
Http::fake([
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴 지정 없이 시퀀스 페이크를 쓰고 싶다면 `Http::fakeSequence`를 사용할 수 있습니다:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 페이크 콜백

특정 엔드포인트에 대해 반환할 응답을 동적으로 결정해야 하는 복잡한 경우, 클로저를 `fake` 메서드에 넘길 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받고, 응답 인스턴스를 반환해야 합니다. 클로저 내에서 필요에 따라 다양한 로직을 구현할 수 있습니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사 (Inspecting Requests)

응답을 페이크 처리하는 동안에도, 실제 클라이언트가 받은 요청들을 점검해 애플리케이션이 올바른 데이터 혹은 헤더를 전송하고 있는지 확인하고 싶을 때가 있습니다. `Http::fake` 이후 `Http::assertSent` 메서드를 사용하면 됩니다.

`assertSent` 메서드는 클로저를 받고, 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 전달받습니다. 반환값이 true이면 요청 조건을 충족한 것으로 간주합니다. 최소한 하나의 요청이 이 조건을 만족해야 테스트가 통과됩니다:

```php
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

특정 요청이 전송되지 않았는지 확인하고 싶으면 `assertNotSent` 메서드를 사용할 수 있습니다:

```php
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

`assertSentCount`로 테스트 중 "전송된" 요청의 개수를 검증할 수도 있습니다:

```php
Http::fake();

Http::assertSentCount(5);
```

아무 요청도 전송되지 않았는지를 검증하려면 `assertNothingSent`를 사용할 수 있습니다:

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용하면 모든 요청과 대응하는 응답을 수집할 수 있습니다. `recorded`는 `Illuminate\Http\Client\Request`, `Illuminate\Http\Client\Response` 인스턴스 쌍의 컬렉션을 반환합니다:

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

또한, `recorded` 메서드는 클로저도 인수로 받아, 요청/응답 쌍을 원하는 기준으로 필터링할 수 있습니다:

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

<a name="preventing-stray-requests"></a>
### 의도치 않은 요청 차단 (Preventing Stray Requests)

테스트 전체 또는 개별 테스트 수행 중, HTTP 클라이언트가 전송하는 모든 요청이 반드시 페이크 처리되었는지 확실히 하고 싶다면 `preventStrayRequests` 메서드를 사용하세요. 이 메서드 호출 후에는 페이크로 지정하지 않은 요청을 보내면 실제 HTTP 요청 대신 예외가 발생합니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답 반환
Http::get('https://github.com/laravel/framework');

// 예외 발생
Http::get('https://laravel.com');
```

대부분의 의도치 않은 요청은 차단하면서, 특정 요청만 허용하고 싶은 경우엔 `allowStrayRequests` 메서드로 허용할 패턴을 정할 수 있습니다. 지정한 패턴에 맞는 요청만 실제로 전송되고, 나머지는 예외를 발생시킵니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// 이 요청은 실행됨
Http::get('http://127.0.0.1:5000/generate');

// 나머지 요청은 예외 발생
Http::get('https://laravel.com');
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 HTTP 요청 전송 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청 전송 전에, `ResponseReceived` 이벤트는 요청에 대한 응답을 수신한 후, `ConnectionFailed` 이벤트는 응답을 받지 못한 경우에 발생합니다.

`RequestSending`, `ConnectionFailed` 이벤트는 모두 `Illuminate\Http\Client\Request` 인스턴스를 확인할 수 있는 public `$request` 속성을 가집니다. `ResponseReceived` 이벤트 역시 `$request` 속성과 함께 응답을 점검할 수 있는 `$response` 속성을 함께 가집니다. 애플리케이션 내에서 이러한 이벤트에 대한 [이벤트 리스너](/docs/master/events)를 생성할 수 있습니다:

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 이벤트 핸들러.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```
