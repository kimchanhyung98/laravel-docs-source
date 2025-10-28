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
    - [요청 배칭](#request-batching)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 페이킹](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [비정상 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/) 위에 간결하고 직관적인 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 상호작용하기 위한 외부 HTTP 요청을 신속하게 보낼 수 있습니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례와 개발자 경험 개선에 중점을 두고 있습니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보내려면 `Http` 파사드가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 다양한 응답 검사를 위한 여러 메서드를 제공합니다:

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스를 구현하므로, 응답된 JSON 데이터를 배열처럼 바로 접근할 수 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```

위 응답 관련 메서드 외에도, 특정 HTTP 상태 코드를 판별할 수 있는 다음 메서드들을 사용할 수 있습니다:

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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 이용해 요청 URL을 동적으로 구성할 수 있습니다. URI 템플릿에 값을 확장할 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용하세요:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프(dump) 기능

요청이 실제로 보내지기 전에 해당 요청 인스턴스를 덤프하고, 스크립트 실행을 즉시 종료하고 싶다면, 요청 앞에 `dd` 메서드를 추가하세요:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

보통 `POST`, `PUT`, `PATCH` 요청 시 추가 데이터를 함께 보내는 경우가 많으므로, 해당 메서드들은 두 번째 인수로 데이터 배열을 받습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청 시, 쿼리스트링을 URL에 직접 추가하거나, 키-값 쌍 배열을 `get` 메서드의 두 번째 인수로 전달할 수 있습니다:

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
#### Form URL Encoded 방식으로 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 전송하고 싶다면, 요청 전에 `asForm` 메서드를 호출해야 합니다:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 바디 전송

요청 시 raw 바디를 직접 지정하고 싶다면 `withBody` 메서드를 사용하세요. 두 번째 인수로 콘텐츠 타입을 지정할 수 있습니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트(Multi-Part) 요청

파일을 멀티파트 폼으로 전송하려면, 요청 전에 `attach` 메서드를 사용해야 합니다. 이 메서드는 파일의 이름과 내용(필요하다면 파일명, 헤더도 추가) 등의 인수를 받습니다:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 raw 내용을 전달하는 대신 스트림 리소스를 넘길 수도 있습니다:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용하세요. 이 메서드는 키-값 쌍의 배열을 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` 메서드를 사용하면, 요청에 대한 응답에서 애플리케이션이 기대하는 콘텐츠 타입을 명시할 수 있습니다:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

편의를 위해, `acceptJson` 메서드를 활용해 애플리케이션이 `application/json` 타입을 기대한다고 간단히 지정할 수 있습니다:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 헤더에 새로운 헤더를 병합합니다. 모든 헤더를 완전히 교체하고 싶다면 `replaceHeaders` 메서드를 사용하세요:

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
### 인증

Basic 및 Digest 인증 정보를 각각 `withBasicAuth`와 `withDigestAuth` 메서드로 지정할 수 있습니다:

```php
// Basic 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

`Authorization` 헤더에 Bearer 토큰을 빠르게 추가하려면 `withToken` 메서드를 사용하세요:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드로 응답을 기다릴 최대 초(second)를 지정할 수 있습니다. 기본값은 30초입니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException` 인스턴스가 발생합니다.

서버 연결 시도 최대 대기시간을 지정하려면 `connectTimeout` 메서드를 사용하세요. 기본값은 10초입니다:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트 또는 서버 오류가 발생했을 때 HTTP 클라이언트가 자동으로 요청을 재시도 하길 원한다면, `retry` 메서드를 사용할 수 있습니다. 이 메서드는 시도 최대 횟수와 각 시도 사이 대기 시간(밀리초 단위, ms)을 인수로 받습니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

시도 간 대기 시간을 직접 계산하고 싶다면, 두 번째 인수로 클로저를 전달할 수 있습니다:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

또한, 첫 번째 인수로 배열을 주면 요청 간 각각의 대기시간을 다르게 지정할 수 있습니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면, 세 번째 인수로 콜러블을 넘겨 실제로 재시도를 해야 하는지 여부를 제어할 수 있습니다. 예를 들어, 연결 예외(`ConnectionException`)가 발생했을 때만 재시도 하고 싶다면 다음처럼 작성하세요:

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

시도가 실패할 경우, 재시도 전 요청을 수정해야 할 때도 있습니다. 예를 들어, 인증 오류가 발생하면 새 토큰으로 재시도하는 상황을 들 수 있습니다:

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

모든 재시도가 실패할 경우, `Illuminate\Http\Client\RequestException`이 발생합니다. 이 동작을 비활성화하려면 `throw` 인수를 `false`로 지정하세요. 이 경우, 모든 시도 후 마지막 응답 객체가 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 연결 문제로 인해 모든 요청이 실패할 경우, `throw` 인수와 상관없이 `Illuminate\Http\Client\ConnectionException` 예외는 여전히 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트(`400번대`)/서버(`500번대`) 오류가 반환되어도 예외를 던지지 않습니다. 이런 오류가 반환되었는지 확인하려면 `successful`, `clientError`, `serverError` 메서드를 사용할 수 있습니다:

```php
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 400번대 상태 코드인지 확인...
$response->clientError();

// 500번대 상태 코드인지 확인...
$response->serverError();

// 클라이언트 또는 서버 오류 발생 시, 콜백 즉시 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생

응답 인스턴스가 있고, 응답 상태코드가 클라이언트/서버 오류를 나타낸다면 `Illuminate\Http\Client\RequestException` 예외를 발생시키고 싶을 때는 `throw` 또는 `throwIf` 메서드를 사용하세요:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트/서버 오류 시 예외 발생...
$response->throw();

// 오류가 발생하고 특정 조건이 true일 때 예외 발생...
$response->throwIf($condition);

// 오류가 발생하고 해당 클로저가 true일 때 예외 발생...
$response->throwIf(fn (Response $response) => true);

// 오류가 발생하고 조건이 false일 때 예외 발생...
$response->throwUnless($condition);

// 오류가 발생하고 해당 클로저가 false일 때 예외 발생...
$response->throwUnless(fn (Response $response) => false);

// 응답이 특정 상태 코드일 때 예외 발생...
$response->throwIfStatus(403);

// 응답이 특정 상태 코드가 아닐 경우 예외 발생...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스의 공개 `$response` 속성을 통해 반환된 응답을 검사할 수 있습니다.

`throw` 메서드는 에러가 없다면 응답 인스턴스를 반환하기 때문에 체이닝하여 추가 작업도 가능합나다:

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전에 추가 작업을 하고 싶다면 `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저 실행 후 예외는 자동으로 던져지며, 별도로 re-throw하지 않아도 됩니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로깅 또는 보고 시 120자까지로 잘립니다. 이 동작을 사용자 정의하거나 비활성화하려면, `bootstrap/app.php` 파일의 예외 설정에서 `truncateRequestExceptionsAt`, `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions): void {
    // 요청 예외 메시지를 240자로 잘라서 로깅...
    $exceptions->truncateRequestExceptionsAt(240);

    // 예외 메시지 잘라내기 비활성화...
    $exceptions->dontTruncateRequestExceptions();
})
```

또는, 개별 요청 단위로 `truncateExceptionsAt` 메서드를 사용할 수도 있습니다:

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel의 HTTP 클라이언트는 Guzzle로 구동되므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용하여 요청/응답을 조작할 수 있습니다. 요청을 조작하려면 `withRequestMiddleware` 메서드를 통해 Guzzle 미들웨어를 등록하세요:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 응답을 검사하려면 `withResponseMiddleware` 메서드에 미들웨어를 등록할 수 있습니다:

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

모든 요청 또는 응답에 적용될 미들웨어를 등록하고 싶다면, `globalRequestMiddleware`, `globalResponseMiddleware` 메서드를 사용하세요. 일반적으로 이들 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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
### Guzzle 옵션

`withOptions` 메서드를 통해 요청별 추가적인 [Guzzle 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정할 수 있습니다. 이 메서드는 키-값 쌍 배열을 인수로 받습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 글로벌 옵션

모든 요청에 대해 기본 옵션을 지정하려면 `globalOptions` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Http::globalOptions([
        'allow_redirects' => false,
    ]);
}
```

<a name="concurrent-requests"></a>
## 동시 요청

여러 HTTP 요청을 동시에, 즉 순차적으로가 아니라 동시에 보낼 때도 있습니다. 이런 동시성 처리는 느린 API와 상호작용할 때 특히 성능 향상에 도움이 됩니다.

<a name="request-pooling"></a>
### 요청 풀링

이럴 때는 `pool` 메서드를 사용하면 됩니다. `pool` 메서드는 클로저를 인수로 받으며, 이 클로저는 `Illuminate\Http\Client\Pool` 인스턴스를 받아 요청 풀에 요청을 추가할 수 있습니다:

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

이처럼 각 응답은 추가 순서대로 배열 인덱스로 접근할 수 있습니다. 요청에 이름을 붙이고 싶다면 `as` 메서드를 써서 각 응답을 이름으로도 조회할 수 있습니다:

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

풀의 최대 동시 처리 개수는 `pool` 메서드의 `concurrency` 인수로 제어할 수 있습니다. 이 값은 해당 풀에서 동시에 진행 중인 HTTP 요청의 최대 개수를 결정합니다:

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

<a name="customizing-concurrent-requests"></a>
#### 동시 요청 커스터마이징

`pool` 메서드는 `withHeaders`나 `middleware` 등 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀에 추가한 각 요청에 개별적으로 옵션을 설정해야 합니다:

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
### 요청 배칭

Laravel에서 동시 요청을 처리하는 또 다른 방법으로 `batch` 메서드가 있습니다. `pool`과 마찬가지로 클로저로 `Illuminate\Http\Client\Batch` 인스턴스를 받아 요청을 추가할 수 있고, 완료 콜백도 지정할 수 있습니다:

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
    // 배치가 생성되었지만 아직 요청이 초기화되지 않은 상태...
})->progress(function (Batch $batch, int|string $key, Response $response) {
    // 각 개별 요청이 성공적으로 완료될 때마다 호출...
})->then(function (Batch $batch, array $results) {
    // 모든 요청이 성공적으로 완료...
})->catch(function (Batch $batch, int|string $key, Response|RequestException|ConnectionException $response) {
    // 첫 번째 실패 요청 감지 시...
})->finally(function (Batch $batch, array $results) {
    // 전체 배치 실행 종료 시...
})->send();
```

`pool`과 동일하게, `as` 메서드로 요청에 이름을 붙일 수 있습니다:

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

`send` 메서드로 배치가 시작된 후엔 새로운 요청을 추가할 수 없습니다. 이때 추가하려 하면 `Illuminate\Http\Client\BatchInProgressException` 예외가 발생합니다.

배치의 최대 동시 요청 수는 `concurrency` 메서드로 지정합니다:

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a name="inspecting-batches"></a>
#### 배치 검사

배치 완료 콜백에서 전달되는 `Illuminate\Http\Client\Batch` 인스턴스는 여러 속성과 메서드를 제공해, 각 배치의 상태를 쉽게 확인할 수 있습니다:

```php
// 배치에 포함된 총 요청 수...
$batch->totalRequests;
 
// 아직 처리되지 않은 요청 수...
$batch->pendingRequests;
 
// 실패한 요청 수...
$batch->failedRequests;

// 현재까지 처리된 요청 수...
$batch->processedRequests();

// 배치 실행 종료 여부...
$batch->finished();

// 실패 요청 존재 여부...
$batch->hasFailures();
```

<a name="deferring-batches"></a>
#### 배치 지연 실행(Defer)

`defer` 메서드를 호출하면, 배치 요청들이 즉시 실행되지 않습니다. 대신, 현재 애플리케이션 요청의 HTTP 응답이 사용자에게 전송된 후에 실행됩니다. 이를 통해 애플리케이션의 반응성을 높일 수 있습니다:

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->then(function (Batch $batch, array $results) {
    // 모든 요청이 완료된 후...
})->defer();
```

<a name="macros"></a>
## 매크로

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있습니다. 매크로를 통해 공통 경로 및 헤더 설정을 유창하게 재사용할 수 있습니다. 매크로는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의하세요:

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스 부트스트랩.
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

매크로를 설정한 후에는, 애플리케이션 어디서든 해당 매크로를 호출해 지정된 설정을 가진 대기(request pending) 객체를 생성할 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

Laravel의 여러 서비스처럼, HTTP 클라이언트도 쉽고 직관적인 테스트 작성 기능을 제공합니다. `Http` 파사드의 `fake` 메서드는 요청에 대해 더미/스텁 응답을 반환하도록 HTTP 클라이언트를 지시합니다.

<a name="faking-responses"></a>
### 응답 페이킹

예를 들어, 모든 요청에 대해 비어있는 `200` 상태 응답을 반환하게 하려면 인수를 생략한 채 `fake` 메서드를 호출하세요:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL에 대한 페이킹

또는, `fake` 메서드에 배열을 전달해 URL 패턴별로 페이크 응답을 지정할 수 있습니다. `*` 문자를 와일드카드로 사용할 수 있으며, `Http` 파사드의 `response` 메서드로 스텁 응답을 작성할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대해 JSON 응답 반환
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대해 문자열 응답 반환
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

지정한 URL 패턴에 없는 요청은 실제로 전송됩니다. 모든 패턴에 매칭되지 않는 요청도 스텁하려면 단일 `*` 패턴을 사용하세요:

```php
Http::fake([
    // GitHub 엔드포인트에 대해 JSON 응답 반환
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 나머지는 모두 문자열 응답 반환
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

편의를 위해 문자열, 배열, 정수 등 간단한 값으로도 응답을 페이킹할 수 있습니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 상황 페이킹

HTTP 클라이언트가 요청을 보낼 때 `Illuminate\Http\Client\ConnectionException`이 발생하는 상황을 테스트하려면 `failedConnection` 메서드를 사용하세요:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException` 발생 테스트는 `failedRequest` 메서드를 사용합니다:

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 페이킹

하나의 URL에 대해 여러 개의 페이크 응답을 순차적으로 지정하려면 `Http::sequence`를 이용해 응답 시퀀스를 만들어주세요:

```php
Http::fake([
    // GitHub 엔드포인트에 순차적으로 응답 스텁
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

응답 시퀀스가 소진되면 이후 추가 요청에서는 예외가 발생합니다. 시퀀스가 비었을 때 반환할 기본 응답이 필요하다면 `whenEmpty` 메서드를 사용하세요:

```php
Http::fake([
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴 없이도 응답 시퀀스만 페이킹하려면 `Http::fakeSequence`를 사용할 수 있습니다:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 사용자 정의 페이크 콜백

특정 엔드포인트에 어떤 응답을 줄지 복잡한 조건이 필요하다면, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받고, 응답 인스턴스를 반환해야 합니다. 클로저 내부에서 원하는 로직을 자유롭게 구현할 수 있습니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사

페이크 응답을 사용하는 경우, 클라이언트가 실제로 어떤 데이터를 보내는지, 헤더가 제대로 붙었는지 검사하고 싶을 수 있습니다. 이럴 때는 `Http::fake` 호출 후, `Http::assertSent` 메서드를 사용하세요.

`assertSent`는 클로저를 받으며, 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 인수로 받아, 일치 여부를 boolean으로 반환해야 합니다. 조건과 일치하는 요청이 하나 이상 존재해야 테스트가 통과합니다:

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

특정 요청이 전송되지 않았는지 확인하려면 `assertNotSent`를 사용하세요:

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

전체 테스트에서 보낸 요청 개수를 검증하려면 `assertSentCount`를 사용합니다:

```php
Http::fake();

Http::assertSentCount(5);
```

또는, 아예 어떤 요청도 전송되지 않아야 할 때는 `assertNothingSent`를 쓰세요:

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용해 모든 요청 및 해당 응답을 수집할 수 있습니다. 이 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스 쌍의 컬렉션을 반환합니다:

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

또한, 클로저를 전달해 요청/응답 쌍을 필터링할 수도 있습니다:

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
### 비정상 요청 방지

테스트 전체에서 HTTP 클라이언트를 통해 나가는 모든 요청이 반드시 페이킹되어야 한다면, `preventStrayRequests` 메서드를 호출하세요. 이 상태에서 페이크 응답이 지정되지 않은 실제 요청을 보내면 예외가 발생합니다:

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

대부분의 비정상 요청을 막으면서 특정 요청만 허용하고 싶다면, `allowStrayRequests` 메서드에 허용할 URL 패턴의 배열을 전달하면 됩니다. 패턴과 일치하는 요청은 정상 실행되고, 나머지는 여전히 예외가 발생합니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// 이 요청은 허용
Http::get('http://127.0.0.1:5000/generate');

// 나머지는 예외 발생
Http::get('https://laravel.com');
```

<a name="events"></a>
## 이벤트

Laravel은 HTTP 요청 처리 중 세 가지 이벤트를 발생시킵니다. 요청이 전송되기 전에는 `RequestSending` 이벤트, 응답을 받은 후에는 `ResponseReceived` 이벤트가 실행됩니다. 응답을 받지 못하면 `ConnectionFailed` 이벤트가 발생합니다.

`RequestSending`과 `ConnectionFailed` 이벤트에는 요청 객체를 담은 `$request` 속성이 존재하며, `ResponseReceived` 이벤트에서는 `$request`와 `$response` 속성을 통해 각 객체를 참조할 수 있습니다. 이러한 이벤트에 대해 [이벤트 리스너](/docs/12.x/events)를 만들 수 있습니다:

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