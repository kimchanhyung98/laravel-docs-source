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
    - [요청 배치](#request-batching)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 가짜화](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [의도치 않은 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/) 위에 간결하고 표현력 있는 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과의 통신을 위한 HTTP 요청을 빠르게 보낼 수 있습니다. Laravel의 Guzzle 래퍼는 가장 흔한 사용 사례와 개발자 경험에 초점을 맞추고 있습니다.

<a name="making-requests"></a>
## 요청 보내기 (Making Requests)

요청을 보내기 위해서는 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 가장 기본적인 `GET` 요청을 다른 URL로 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 다양한 응답 확인 메서드를 제공합니다:

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스를 구현하므로 JSON 응답 데이터를 배열 스타일로 접근할 수 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```

위에 소개된 응답 메서드 외에도, 다음 메서드로 특정 HTTP 상태 코드를 응답이 포함하고 있는지 확인할 수 있습니다:

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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 활용해 요청 URL을 쉽게 구성할 수 있습니다. URI 템플릿에서 확장할 URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용합니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 내용 덤프하기

요청을 실제로 전송하기 전에 요청 인스턴스를 덤프하고 스크립트 실행을 종료하고 싶다면, 요청 정의의 맨 앞에 `dd` 메서드를 추가하세요:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터 (Request Data)

`POST`, `PUT`, `PATCH` 요청에서는 추가 데이터를 같이 보내는 것이 일반적입니다. 이때 두 번째 인수로 데이터 배열을 전달할 수 있습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청에서는 쿼리 스트링을 URL에 직접 추가하거나, `get` 메서드의 두 번째 인수로 키-값 배열을 전달할 수 있습니다:

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
#### Form URL 인코딩 요청 전송

`application/x-www-form-urlencoded` 형식으로 데이터를 보내고 싶다면, 요청을 보내기 전에 `asForm` 메서드를 호출해야 합니다:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 바디 전송

요청 시 raw 바디 데이터를 직접 지정하려면 `withBody` 메서드를 사용하세요. 두 번째 인수로 콘텐츠 타입도 지정할 수 있습니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트 형식으로 전송하려면, 요청을 보내기 전에 `attach` 메서드를 사용합니다. 파일의 이름과 내용을 전달하며, 필요에 따라 세 번째 인수로 파일명, 네 번째 인수로 파일 전용 헤더도 전달할 수 있습니다:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 raw 데이터 대신 스트림 리소스를 직접 전달할 수도 있습니다:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더 (Headers)

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용합니다. 이 메서드는 키/값 쌍 배열을 인수로 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

응답에서 기대하는 콘텐츠 타입을 지정하려면 `accept` 메서드를 사용할 수 있습니다:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

더 편리하게, `acceptJson` 메서드는 응답을 `application/json`으로 기대한다고 빠르게 지정할 수 있습니다:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 요청 헤더에 새 헤더를 병합합니다. 모든 헤더를 완전히 대체하고 싶다면 `replaceHeaders` 메서드를 사용하세요:

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

기본 인증과 다이제스트 인증을 사용하려면 각각 `withBasicAuth` 와 `withDigestAuth` 메서드를 사용합니다:

```php
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### 베어러 토큰

`Authorization` 헤더에 베어러 토큰을 추가하려면 `withToken` 메서드를 사용하면 됩니다:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃 (Timeout)

`timeout` 메서드를 사용해 응답을 기다릴 최대 초 수를 지정할 수 있습니다. 기본값은 30초입니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정된 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버 연결 시도 시 기다릴 최대 초 수는 `connectTimeout` 메서드로 지정할 수 있습니다(기본값은 10초):

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도 (Retries)

클라이언트나 서버 오류 발생 시 자동으로 요청을 다시 시도하게 하려면 `retry` 메서드를 사용하세요. 이 메서드는 최대 시도 횟수와 두 번의 시도 사이에 Laravel이 대기할 밀리초(ms)를 인수로 받습니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

시도 사이의 대기 시간을 수동으로 계산하려면, 두 번째 인수로 클로저를 전달할 수 있습니다:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

또는, 첫 번째 인수로 배열을 전달해 각각의 시도마다 대기할 시간을 지정할 수도 있습니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면 `retry` 메서드의 세 번째 인수로 재시도 여부를 결정하는 콜러블을 전달할 수 있습니다. 예를 들어, 첫 요청에서 `ConnectionException`이 발생한 경우만 재시도하고 싶을 때 사용할 수 있습니다:

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청이 실패했다면, 새로운 시도 전에 요청을 변경하고 싶을 수 있습니다. 이 경우, 재시도 콜러블의 두 번째 인수로 제공되는 요청 인스턴스를 수정할 수 있습니다. 예시로, 인증 오류가 발생하면 새 인증 토큰으로 재시도하도록 할 수 있습니다:

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

모든 요청이 실패할 경우 `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 이 동작을 비활성화하려면 `throw` 인수를 `false`로 전달할 수 있습니다. 비활성화하면 모든 재시도 후 받은 마지막 응답이 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 인해 실패하면, `throw` 인자를 `false`로 설정했어도 `Illuminate\Http\Client\ConnectionException` 예외는 계속 발생합니다.

<a name="error-handling"></a>
### 에러 처리 (Error Handling)

Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트나 서버 오류(`400` 및 `500`대 응답)가 발생해도 예외를 발생시키지 않습니다. 이러한 오류가 반환되었는지 확인하려면 `successful`, `clientError`, 또는 `serverError` 메서드를 사용할 수 있습니다:

```php
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 400대 상태 코드인지 확인...
$response->clientError();

// 500대 상태 코드인지 확인...
$response->serverError();

// 클라이언트나 서버 오류가 있을 시 바로 콜백 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생시키기

응답 인스턴스가 있고, 상태 코드가 클라이언트나 서버 오류에 해당한다면 `Illuminate\Http\Client\RequestException`을 발생시키려면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트나 서버 오류 시 예외 발생...
$response->throw();

// 오류 발생했고, 특정 조건이 참이면 예외 발생...
$response->throwIf($condition);

// 오류 발생했고, 클로저가 참을 반환하면 예외 발생...
$response->throwIf(fn (Response $response) => true);

// 오류 발생했고, 특정 조건이 거짓이면 예외 발생...
$response->throwUnless($condition);

// 오류 발생했고, 클로저가 거짓을 반환하면 예외 발생...
$response->throwUnless(fn (Response $response) => false);

// 응답이 특정 상태 코드라면 예외 발생...
$response->throwIfStatus(403);

// 응답이 특정 상태 코드가 아니면 예외 발생...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스에는 응답을 확인할 수 있도록 public `$response` 속성이 있습니다.

`throw` 메서드는 오류가 없으면 응답 인스턴스를 반환하므로, 메서드 체이닝을 계속해서 사용할 수 있습니다:

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전에 추가 작업을 수행하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저 실행 후에는 예외가 자동으로 발생하므로 클로저 내부에서 별도로 예외를 다시 발생시킬 필요는 없습니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그 기록 또는 리포트 시 120자로 잘려 저장됩니다. 이 동작을 수정하거나 비활성화하려면, `bootstrap/app.php` 파일에서 `truncateRequestExceptionsAt` 및 `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions): void {
    // 예외 메시지를 240자로 잘라 저장...
    $exceptions->truncateRequestExceptionsAt(240);

    // 예외 메시지 잘라내기 비활성화...
    $exceptions->dontTruncateRequestExceptions();
})
```

또한, `truncateExceptionsAt` 메서드를 통해 요청별로 예외 메시지 자르기 동작을 직접 설정할 수 있습니다:

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어 (Guzzle Middleware)

Laravel의 HTTP 클라이언트는 Guzzle 기반이므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 나가는 요청을 조작하거나 들어오는 응답을 검사할 수 있습니다. 나가는 요청을 조작하려면 `withRequestMiddleware` 메서드로 미들웨어를 등록하세요:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, `withResponseMiddleware` 메서드로 들어오는 HTTP 응답을 검사하는 미들웨어를 등록할 수 있습니다:

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

모든 나가는 요청과 들어오는 응답에 공통적으로 적용할 미들웨어를 등록하려면, `globalRequestMiddleware` 및 `globalResponseMiddleware` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출되어야 합니다:

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

나가는 요청에 대해 추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정하려면 `withOptions` 메서드를 사용할 수 있습니다. 이 메서드는 키/값 쌍 배열을 인수로 받습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 글로벌 옵션

모든 나가는 요청에 대한 기본값을 설정하려면 `globalOptions` 메서드를 활용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출해야 합니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
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

여러 HTTP 요청을 동시에 보내고자 할 때가 있습니다. 즉, 각 요청을 순차적으로 처리하는 대신 여러 요청을 한 번에 발송하여, 느린 HTTP API와 연동할 때 성능을 크게 향상시킬 수 있습니다.

<a name="request-pooling"></a>
### 요청 풀링 (Request Pooling)

이럴 때 `pool` 메서드를 활용하면 됩니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 전달받는 클로저를 받으며, 여기서 여러 요청을 풀에 추가할 수 있습니다:

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

각 응답 인스턴스는 풀에 추가된 순서대로 배열 인덱스로 접근할 수 있습니다. 또한 `as` 메서드로 각 요청에 별칭을 지정하여, 해당 응답에 명시적으로 접근할 수도 있습니다:

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

<a name="customizing-concurrent-requests"></a>
#### 동시 요청 커스터마이징

`pool` 메서드는 `withHeaders`나 `middleware`와 같은 다른 HTTP 클라이언트 메서드들과 체이닝할 수 없습니다. 풀에 추가된 각각의 요청에 직접 옵션을 지정해야 합니다:

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
### 요청 배치 (Request Batching)

여러 요청을 동시 처리하는 또 다른 방법으로는 `batch` 메서드를 사용할 수 있습니다. 이 메서드 역시 `Illuminate\Http\Client\Batch` 인스턴스를 전달받는 클로저를 받으며, 요청 풀에 쉽게 추가할 수 있고, 완료 콜백도 정의할 수 있습니다:

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
    // 배치가 생성되었지만 요청이 아직 시작되지 않음...
})->progress(function (Batch $batch, int|string $key, Response $response) {
    // 개별 요청이 성공적으로 완료됨...
})->then(function (Batch $batch, array $results) {
    // 모든 요청이 성공적으로 완료됨...
})->catch(function (Batch $batch, int|string $key, Response|RequestException|ConnectionException $response) {
    // 첫 번째 배치 요청 실패를 감지...
})->finally(function (Batch $batch, array $results) {
    // 배치 실행이 모두 끝남...
})->send();
```

`pool`과 마찬가지로, `as` 메서드로 요청에 이름을 부여할 수 있습니다:

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

`batch`의 `send` 메서드를 호출해 배치 처리를 시작하면 새로운 요청을 추가할 수 없습니다. 나중에 추가하면 `Illuminate\Http\Client\BatchInProgressException` 예외가 발생합니다.

<a name="inspecting-batches"></a>
#### 배치 검사

배치 완료 콜백에서 제공되는 `Illuminate\Http\Client\Batch` 인스턴스에는 여러 속성과 메서드가 있어 배치의 상태를 확인하고 상호작용할 수 있습니다:

```php
// 배치에 할당된 총 요청 개수...
$batch->totalRequests;
 
// 아직 처리되지 않은 요청 개수...
$batch->pendingRequests;
 
// 실패한 요청 개수...
$batch->failedRequests;

// 지금까지 처리된 요청 개수...
$batch->processedRequests();

// 배치 실행이 끝났는지 여부...
$batch->finished();

// 배치에 요청 실패가 있는지 여부...
$batch->hasFailures();
```
<a name="deferring-batches"></a>
#### 배치 지연 실행

`defer` 메서드를 호출하면, 요청 배치는 즉시 실행되지 않습니다. 대신, 현재 애플리케이션의 HTTP 응답이 사용자에게 전송된 뒤에 배치가 처리되어, 애플리케이션이 더욱 빠르고 반응성 있게 느껴질 수 있습니다:

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->then(function (Batch $batch, array $results) {
    // 모든 요청이 성공적으로 완료됩니다...
})->defer();
```

<a name="macros"></a>
## 매크로 (Macros)

Laravel HTTP 클라이언트는 "매크로"라는 기능을 제공하여, 흔히 사용하는 요청 경로나 헤더 구성을 손쉽게 재사용할 수 있습니다. 매크로는 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 정의합니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
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

매크로가 정의되면, 애플리케이션 어느 곳에서도 해당 설정을 갖춘 요청을 쉽게 만들 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

많은 Laravel 서비스처럼, HTTP 클라이언트도 손쉽고 표현력 있게 테스트를 작성할 수 있도록 설계되어 있습니다. `Http` 파사드의 `fake` 메서드는 요청이 발생할 때 미리 준비된(dummy) 응답을 반환하도록 HTTP 클라이언트에게 지시합니다.

<a name="faking-responses"></a>
### 응답 가짜화 (Faking Responses)

예를 들어, 모든 요청에 대해 빈 `200` 상태 코드의 응답을 반환하도록 하려면, 아무 인수 없이 `fake` 메서드를 호출합니다:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 응답 가짜화

또는, `fake` 메서드에 배열을 전달해 URL 패턴과 원하는 응답을 지정할 수도 있습니다. `*`는 와일드카드로 사용할 수 있습니다. 엔드포인트별 가짜 응답 생성에는 `Http` 파사드의 `response` 메서드를 사용합니다:

```php
Http::fake([
    // GitHub 엔드포인트에는 JSON 응답을...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에는 문자열 응답을...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

가짜 처리가 되지 않은 모든 URL에 대해서는 실제 HTTP 요청이 이루어집니다. 모든 매치되지 않은 URL에 대한 기본 가짜 응답을 지정하려면, `' * '` 패턴을 사용하세요:

```php
Http::fake([
    // GitHub 엔드포인트에는 JSON 응답을...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트에는 문자열 응답을...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

간단히 문자열, JSON, 빈 응답을 반환하려면, 응답값으로 문자열, 배열, 정수를 전달할 수도 있습니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 응답 가짜화

HTTP 클라이언트가 요청 시 `Illuminate\Http\Client\ConnectionException`을 만났을 때 애플리케이션의 동작을 테스트하려면 `failedConnection` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException` 발생 상황을 테스트하려면 `failedRequest` 메서드를 사용하세요:

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 가짜화

특정 URL이 여러 번 호출될 때, 순서대로 다른 응답을 반환하도록 하려면 `Http::sequence` 메서드로 응답 시퀀스를 만들 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 일련의 응답 생성...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

응답 시퀀스에 있는 모든 응답이 소비되면(소진되면), 추가 요청은 예외를 발생시킵니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용합니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 일련의 응답 생성...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴 없이도 응답 시퀀스를 사용할 수 있으며, 이때는 `Http::fakeSequence`를 사용합니다:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 가짜 콜백

특정 엔드포인트에 반환할 응답을 더 복잡하게 결정해야 한다면, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받아서 적절한 응답 인스턴스를 반환해야 합니다. 클로저 내에서 필요한 모든 로직을 실행할 수 있습니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사 (Inspecting Requests)

가짜 응답을 사용하는 중에도, 클라이언트가 받은 요청을 검사하여 애플리케이션이 올바른 데이터 혹은 헤더를 전송했는지 확인할 수 있습니다. `Http::fake` 이후에 `Http::assertSent` 메서드를 호출하세요.

`assertSent` 메서드는 클로저를 인수로 받으며, 인수로 전달된 `Illuminate\Http\Client\Request` 인스턴스가 기대에 부합하면 `true`를 반환해야 합니다. 주어진 조건을 만족하는 요청이 하나라도 있으면 테스트를 통과합니다:

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

특정 요청이 전송되지 않았음을 보장하려면 `assertNotSent` 메서드를 사용할 수 있습니다:

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

`assertSentCount` 메서드로 테스트 도중 전송된 요청의 개수도 확인할 수 있습니다:

```php
Http::fake();

Http::assertSentCount(5);
```

`assertNothingSent` 메서드를 사용하면 테스트 도중 어느 요청도 전송되지 않았는지 확인할 수 있습니다:

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록하기

`recorded` 메서드로 모든 요청과 그에 대응하는 응답을 모을 수 있습니다. `recorded` 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스로 구성된 배열 컬렉션을 반환합니다:

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

또한, `recorded` 메서드에 클로저를 전달하면, 요청/응답 쌍을 원하는 조건으로 필터링할 수 있습니다:

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
### 의도치 않은 요청 방지 (Preventing Stray Requests)

HTTP 클라이언트를 통한 모든 요청이 반드시 가짜 응답을 사용하도록 테스트(혹은 전체 테스트 스위트)에서 강제하려면, `preventStrayRequests` 메서드를 호출하면 됩니다. 이 메서드 호출 뒤에는, 가짜 응답이 정의되지 않은 URL로 요청이 들어오면 실제 HTTP 요청 대신 예외를 발생시킵니다:

```php
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

특정 요청만 실제로 허용하면서 나머지는 모두 차단하고 싶다면, `allowStrayRequests` 메서드에 허용하고 싶은 URL 패턴 배열을 전달하면 됩니다. 지정한 패턴에 일치하는 요청만 허용되며, 그 외는 계속 예외를 발생시킵니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// 이 요청은 실제로 실행됨...
Http::get('http://127.0.0.1:5000/generate');

// 이 요청은 예외 발생...
Http::get('https://laravel.com');
```

<a name="events"></a>
## 이벤트 (Events)

HTTP 요청 전송 과정에서 Laravel은 세 가지 이벤트를 발행합니다. `RequestSending` 이벤트는 요청이 전송되기 직전에 발행되고, `ResponseReceived` 이벤트는 해당 요청의 응답이 도착하면 발행됩니다. 만약 응답을 받지 못한다면 `ConnectionFailed` 이벤트가 발행됩니다.

`RequestSending`과 `ConnectionFailed` 이벤트에는 모두 public `$request` 속성이 있어서, 해당 `Illuminate\Http\Client\Request` 인스턴스를 검사할 수 있습니다. 마찬가지로 `ResponseReceived` 이벤트에는 `$request`와 `$response` 속성이 모두 포함되어, 받은 응답(`Illuminate\Http\Client\Response`)도 확인할 수 있습니다. 이 이벤트에 대해 [이벤트 리스너](/docs/12.x/events)를 애플리케이션 내에서 만들 수도 있습니다:

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 이벤트 처리 메서드
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```