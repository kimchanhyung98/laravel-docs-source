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
    - [요청 풀](#request-pooling)
    - [배치 요청](#request-batching)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 페이킹](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [예상치 못한 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/) 위에 표현적이면서도 최소한의 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과의 통신을 위한 HTTP 요청을 간편하게 보낼 수 있습니다. Laravel의 Guzzle 래퍼는 가장 흔하게 사용되는 사례와 개발자의 편리함에 중점을 두고 있습니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보내기 위해서는 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 외부 URL로의 기본적인 `GET` 요청을 만드는 방법을 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이를 통해 응답을 검사할 수 있는 다양한 메서드를 제공합니다:

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있으므로, JSON 응답 데이터를 배열처럼 바로 접근할 수도 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```

위에 나열된 응답 메서드 외에도, 응답이 특정 상태 코드를 가졌는지 판단할 때 사용할 수 있는 다음과 같은 메서드들도 있습니다:

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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 이용해 URL을 동적으로 생성할 수도 있습니다. URI 템플릿에서 확장될 URL 매개변수는 `withUrlParameters` 메서드로 정의할 수 있습니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 디버깅(dump)

실제 요청을 보내기 전에 요청 인스턴스를 덤프하고 스크립트 실행을 종료하고 싶다면, 요청 정의 앞에 `dd` 메서드를 추가할 수 있습니다:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

일반적으로 `POST`, `PUT`, `PATCH` 요청을 할 때 추가 데이터를 보내는 경우가 많으므로, 이 메서드들은 두 번째 인수로 데이터 배열을 받을 수 있습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 보낼 때는 URL에 쿼리 문자열을 직접 붙이거나, `get` 메서드의 두 번째 인수로 키/값 배열을 전달할 수 있습니다:

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는 `withQueryParameters` 메서드를 사용할 수도 있습니다:

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
#### Form URL Encoded 요청 전송

데이터를 `application/x-www-form-urlencoded` 형태로 전송하고 싶다면, 요청 전에 `asForm` 메서드를 호출해야 합니다:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### 원시 요청 본문(raw body) 전송

요청을 보낼 때 원시 요청 본문을 직접 지정하고 싶다면 `withBody` 메서드를 사용할 수 있습니다. 콘텐츠 타입은 두 번째 인수로 지정 가능합니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트(Multi-Part) 요청

파일을 멀티파트로 전송하고 싶다면, 요청 전에 `attach` 메서드를 사용해야 합니다. 이 메서드는 파일 이름과 내용이 필요하며, 필요에 따라 세 번째 인수로 파일명을, 네 번째 인수로 파일과 관련된 헤더를 지정할 수 있습니다:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 로(raw) 데이터를 전달하는 대신 스트림 리소스를 사용할 수도 있습니다:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

헤더는 `withHeaders` 메서드를 통해 요청에 추가할 수 있습니다. 이 메서드는 키/값 배열을 인수로 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

애플리케이션이 해당 요청에 대해 기대하는 콘텐츠 타입을 지정할 때는 `accept` 메서드를 사용할 수 있습니다:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

간편하게 응답이 `application/json` 타입임을 기대할 때는 `acceptJson` 메서드를 사용할 수도 있습니다:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 새로운 헤더를 기존 요청 헤더에 머지(병합)합니다. 모든 헤더를 완전히 교체하길 원한다면, `replaceHeaders` 메서드를 사용할 수 있습니다:

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

기본 인증(베이직 인증)과 다이제스트 인증을 각각 `withBasicAuth`와 `withDigestAuth` 메서드로 지정할 수 있습니다:

```php
// 베이직 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### 베어러 토큰(Bearer Token)

`Authorization` 헤더에 베어러 토큰을 손쉽게 추가하고 싶을 때는 `withToken` 메서드를 사용하세요:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드는 응답을 기다릴 최대 초 단위를 지정할 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 후에 타임아웃됩니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버에 연결을 시도할 때 대기할 최대 시간을 지정하려면 `connectTimeout` 메서드를 사용할 수 있습니다. 기본값은 10초입니다:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트 또는 서버 에러가 발생했을 때 HTTP 클라이언트가 자동으로 재시도하도록 하려면, `retry` 메서드를 사용할 수 있습니다. `retry` 메서드는 시도할 최대 횟수와 각 시도 사이의 대기 시간을 밀리초 단위로 받습니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

시도 사이의 대기 시간을 직접 계산하여 지정하고 싶다면 두 번째 인수로 클로저를 전달할 수 있습니다:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

간단하게 각 시도마다 대기 시간을 배열로 지정할 수도 있습니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면 세 번째 인수로 콜러블을 전달하여 실제로 재시도를 시도할지 결정할 수 있습니다. 예를 들어, 최초 요청이 `ConnectionException`을 만난 경우에만 재시도하려면 다음과 같이 할 수 있습니다:

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청 시도가 실패했다면, 두 번째 이후 재시도 전에 요청을 수정하고 싶을 수도 있습니다. 이럴 경우, `retry` 메서드에서 넘겨받는 `$request` 인수를 수정하면 됩니다. 예를 들어, 첫 요청에서 인증 오류가 발생했을 때 새로운 인증 토큰으로 재시도하고 싶다면 다음과 같이 합니다:

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

요청이 모두 실패한 경우에는 `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 이 동작을 비활성화하려면 `throw` 인수를 `false`로 전달하세요. 비활성화 시에는 모든 재시도 후 마지막 요청의 응답이 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패한 경우에는 `throw` 인수가 `false`여도 `Illuminate\Http\Client\ConnectionException` 예외가 여전히 발생합니다.

<a name="error-handling"></a>
### 에러 처리

기본 Guzzle 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트 혹은 서버 에러(`400` 및 `500`번대 응답)에서 예외를 던지지 않습니다. 이러한 에러가 발생했는지 여부는 `successful`, `clientError`, `serverError` 메서드로 확인할 수 있습니다:

```php
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 응답이 400번대 상태 코드인지 확인...
$response->clientError();

// 응답이 500번대 상태 코드인지 확인...
$response->serverError();

// 클라이언트 또는 서버 오류가 발생했을 때 바로 콜백 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생

응답 인스턴스에서 상태 코드가 클라이언트 또는 서버 오류임을 나타낼 경우 `Illuminate\Http\Client\RequestException` 예외를 발생시키고 싶다면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트 또는 서버 에러가 발생하면 예외 발생...
$response->throw();

// 오류가 발생하고 지정한 조건이 true이면 예외 발생...
$response->throwIf($condition);

// 오류가 발생하고 클로저 결과가 true이면 예외 발생...
$response->throwIf(fn (Response $response) => true);

// 오류가 발생하고 지정한 조건이 false이면 예외 발생...
$response->throwUnless($condition);

// 오류가 발생하고 클로저 결과가 false이면 예외 발생...
$response->throwUnless(fn (Response $response) => false);

// 응답이 특정 상태 코드일 때 예외 발생...
$response->throwIfStatus(403);

// 응답이 특정 상태 코드가 아닐 때 예외 발생...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스는 반환된 응답을 살펴볼 수 있도록 공개 `$response` 속성을 가집니다.

`throw` 메서드는 에러가 없다면 응답 인스턴스를 반환하므로, 이후 메서드 체이닝이 가능합니다:

```php
return Http::post(/* ... */)->throw()->json();
```

예외를 발생시키기 전에 추가 로직을 실행하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 이때 클로저가 실행된 후 별도로 예외를 다시 던질 필요 없이 자동으로 예외가 발생합니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로, `RequestException` 메시지는 로그 또는 리포팅 시 120자로 잘려서 출력됩니다. 이 동작을 직접 커스터마이즈하거나 비활성화하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `truncateRequestExceptionsAt` 및 `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions): void {
    // 예외 메시지를 240자로 잘라서 출력...
    $exceptions->truncateRequestExceptionsAt(240);

    // 예외 메시지 잘림 비활성화...
    $exceptions->dontTruncateRequestExceptions();
})
```

또는, 요청별로 `truncateExceptionsAt` 메서드를 이용하여 예외 메시지 잘림을 커스터마이즈할 수도 있습니다:

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel HTTP 클라이언트는 Guzzle 기반이므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 나가는 요청을 조작하거나, 들어오는 응답을 검사할 수 있습니다. 요청을 조작하고자 할 때는 `withRequestMiddleware` 메서드로 Guzzle 미들웨어를 등록하세요:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 응답을 처리할 때는 `withResponseMiddleware` 메서드로 미들웨어를 등록할 수 있습니다:

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
#### 전역 미들웨어

때로는 모든 나가는 요청과 들어오는 응답에 미들웨어를 적용하고 싶을 수 있습니다. 이 경우, `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용하면 됩니다. 주로 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)은 `withOptions` 메서드를 통해 설정할 수 있습니다. 이 메서드는 키/값 쌍의 배열을 인수로 받습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션

모든 나가는 요청에 대한 기본 옵션을 설정하려면, `globalOptions` 메서드를 활용할 수 있습니다. 이 메서드 역시 `AppServiceProvider`의 `boot` 메서드 내에서 호출하는 것이 일반적입니다:

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

때로는 여러 HTTP 요청을 동시에 보낼 필요가 있을 수 있습니다. 즉, 요청들을 순차적으로 보내지 않고 동시에 전송하여 느린 HTTP API와 통신할 때 성능을 크게 향상시킬 수 있습니다.

<a name="request-pooling"></a>
### 요청 풀

다행히도, `pool` 메서드를 사용해 이를 손쉽게 구현할 수 있습니다. `pool` 메서드는 클로저를 인수로 받으며, 이 클로저는 `Illuminate\Http\Client\Pool` 인스턴스를 전달받으므로 여러 요청을 풀에 추가/관리할 수 있습니다:

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

보시다시피, 각 응답 인스턴스는 풀에 추가된 순서대로 접근할 수 있습니다. 원한다면, `as` 메서드로 요청에 이름을 붙여 해당 이름으로 응답에 접근할 수 있습니다:

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

`pool` 메서드는 `withHeaders`, `middleware` 등 HTTP 클라이언트의 다른 메서드와 체이닝할 수 없습니다. 풀 내 개별 요청에 커스텀 헤더 또는 미들웨어를 적용하고자 할 경우, 각 요청마다 직접 옵션을 지정해주어야 합니다:

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
### 배치 요청

Laravel에서 동시 요청을 처리하는 또 다른 방법은 `batch` 메서드를 사용하는 것입니다. 이 메서드는 `pool`과 마찬가지로 `Illuminate\Http\Client\Batch` 인스턴스를 넘겨받는 클로저를 받고 요청들을 추가할 수 있습니다. 또한, 완료 콜백을 정의할 수 있다는 점이 다릅니다:

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Http\Client\RequestException;
use Illuminate\Http\Client\Response;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->before(function (Batch $batch) {
    // 배치가 생성됐지만 아직 어떤 요청도 시작되지 않았습니다...
})->progress(function (Batch $batch, int|string $key, Response $response) {
    // 개별 요청 하나가 성공적으로 완료됨...
})->then(function (Batch $batch, array $results) {
    // 모든 요청이 성공적으로 완료됨...
})->catch(function (Batch $batch, int|string $key, Response|RequestException $response) {
    // 첫 번째 실패 요청이 감지됨...
})->finally(function (Batch $batch, array $results) {
    // 배치가 모두 실행 완료됨...
})->send();
```

`pool` 메서드와 마찬가지로 `as` 메서드로 요청에 이름을 지정할 수 있습니다:

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

`send` 메서드로 `batch`를 시작한 뒤에는 새 요청을 추가할 수 없으며, 시도할 경우 `Illuminate\Http\Client\BatchInProgressException` 예외가 발생합니다.

<a name="inspecting-batches"></a>
#### 배치 검사

배치 완료 콜백에 전달되는 `Illuminate\Http\Client\Batch` 인스턴스는 주어진 배치 내 요청을 점검 및 조작하는 데 도움이 되는 여러 속성과 메서드를 제공합니다:

```php
// 배치에 등록된 전체 요청 수
$batch->totalRequests;
 
// 아직 처리되지 않은 요청 수
$batch->pendingRequests;
 
// 실패한 요청 수
$batch->failedRequests;

// 지금까지 처리된 요청 수
$batch->processedRequests();

// 배치 실행이 완료되었는지 여부
$batch->finished();

// 배치에 실패한 요청이 있는지 여부
$batch->hasFailures();
```

<a name="macros"></a>
## 매크로

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있도록 하여, 서비스와 상호작용할 때 반복되는 요청 경로나 헤더 설정을 유연하게 구성할 수 있습니다. 시작하려면, 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 매크로를 정의합시다:

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

매크로를 정의했다면, 애플리케이션 어디에서든 지정 설정이 적용된 Pending 요청을 만들 때 호출할 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

많은 Laravel 서비스와 마찬가지로, HTTP 클라이언트 역시 테스트 작성시 쉽게 사용할 수 있는 여러 기능을 제공합니다. `Http` 파사드의 `fake` 메서드는 요청 시 더미(stub) 응답을 반환하도록 HTTP 클라이언트를 설정할 수 있게 해줍니다.

<a name="faking-responses"></a>
### 응답 페이킹

예를 들어, 모든 요청에 대해 빈 응답과 함께 200 상태 코드를 반환하도록 하려면, 인수 없이 `fake`를 호출하면 됩니다:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 응답 페이킹

또는, `fake` 메서드에 배열을 전달하여 페이크 처리하고자 하는 URL 패턴을 키로, 해당 URL에 대한 응답을 값으로 지정할 수 있습니다. `*` 문자를 와일드카드로 사용할 수 있습니다. 그리고 `Http` 파사드의 `response` 메서드를 이용해 해당 엔드포인트에 대한 스텁/가짜 응답을 만들 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 가짜 처리
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대한 문자열 응답 가짜 처리
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

페이크로 지정하지 않은 URL에의 요청은 실제로 실행됩니다. 매칭되지 않는 모든 URL에 대해 fallback 응답을 지정하고 싶다면, `*`만을 키로 써서 처리할 수도 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 가짜 처리
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트에 대한 문자열 응답 가짜 처리
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

더 간단하게, 문자열, 배열, 정수값을 응답으로 전달하면 각각 텍스트, JSON, 빈 응답이 쉽게 생성됩니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 페이킹

HTTP 클라이언트가 요청 도중 `Illuminate\Http\Client\ConnectionException`을 만나면 애플리케이션의 동작을 테스트하고 싶을 때가 있을 수 있습니다. 이 경우 `failedConnection` 메서드로 예외를 발생하게 할 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

마찬가지로, `Illuminate\Http\Client\RequestException`이 발생하는 시나리오를 테스트하려면 `failedRequest` 메서드를 사용하면 됩니다:

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 페이킹

특정 URL에서 일정 순서의 가짜 응답을 차례차례 반환하도록 설정하고 싶을 때는 `Http::sequence` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 일련의 응답 가짜 처리
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

응답 시퀀스의 모든 응답이 소진되면 이후 추가 요청 시에는 예외가 발생합니다. 시퀀스가 비었을 때 기본적으로 반환할 응답을 지정하려면 `whenEmpty` 메서드를 사용하세요:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 일련의 응답 가짜 처리
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴을 지정하지 않고 응답 시퀀스를 페이크하고 싶다면 `Http::fakeSequence` 메서드를 사용할 수 있습니다:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 페이크 콜백

특정 엔드포인트에 대한 응답을 결정하는 더 복잡한 로직이 필요하다면, `fake` 메서드에 클로저를 넘겨줄 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받으며, 적절한 응답 인스턴스를 반환해야 합니다. 클로저 안에서 원하는 조건/로직을 구현할 수 있습니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사

응답을 페이킹할 때, 애플리케이션이 올바른 데이터 및 헤더를 보내고 있는지 확인하기 위해 실제 보낸 요청을 검사하고 싶을 때도 있습니다. 이 경우, `Http::fake` 사용 후 `Http::assertSent` 메서드를 호출하여 검사할 수 있습니다.

`assertSent`는 클로저를 받아, 인수로 받은 `Illuminate\Http\Client\Request` 인스턴스가 기대에 부합하는지 boolean을 반환해야 합니다. 최소 한 번이라도 조건에 일치하는 요청이 있었을 때 테스트는 성공하게 됩니다:

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

특정 요청이 보내지지 않았음을 검사하고 싶을 경우 `assertNotSent` 메서드를 사용할 수 있습니다:

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

`assertSentCount`로 테스트 중에 총 몇 번의 요청이 "보내졌는지"도 검증할 수 있습니다:

```php
Http::fake();

Http::assertSentCount(5);
```

또, `assertNothingSent`를 사용해 테스트 중 보내진 요청이 없었는지 확인할 수도 있습니다:

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용하여 모든 요청과 각 요청에 대한 응답을 수집할 수 있습니다. 이 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스로 구성된 배열 컬렉션을 반환합니다:

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

또한, `recorded` 메서드에 클로저를 전달해 요청/응답 쌍을 원하는 기준으로 필터링할 수도 있습니다:

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
### 예상치 못한 요청 방지

테스트(개별 또는 전체 스위트)에서 **모든** HTTP 클라이언트의 요청이 반드시 페이크되어야 함을 보장하고 싶다면, `preventStrayRequests` 메서드를 호출할 수 있습니다. 이렇게 하면 가짜 응답이 없는 모든 요청은 실제 HTTP 요청을 보내지 않고 예외를 발생시킵니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답이 반환됨
Http::get('https://github.com/laravel/framework');

// 예외 발생
Http::get('https://laravel.com');
```

기본적으로는 모든 예상치 못한 요청을 차단하지만, 특정 요청만 허용하고 싶다면 `allowStrayRequests` 메서드에 URL 패턴 배열을 넘겨 허용할 수 있습니다. 지정한 패턴에 맞는 요청만 허용되며, 그 외는 계속 예외가 발생합니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// 이 요청은 실제로 실행됨
Http::get('http://127.0.0.1:5000/generate');

// 예외 발생
Http::get('https://laravel.com');
```

<a name="events"></a>
## 이벤트

Laravel은 HTTP 요청 전후 및 연결 실패 시점에 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 전송되기 **직전**에 발생하고, `ResponseReceived` 이벤트는 각 요청에 대한 응답을 받은 **후**에 발생합니다. `ConnectionFailed` 이벤트는 해당 요청에 대해 응답을 받지 못할 경우에 발생합니다.

`RequestSending` 및 `ConnectionFailed` 이벤트에는 `Illuminate\Http\Client\Request` 인스턴스를 담은 공개 `$request` 속성이 포함됩니다. 마찬가지로, `ResponseReceived` 이벤트에는 `$request`와 함께 응답을 살펴볼 수 있는 `$response` 속성도 있습니다. 이 이벤트들에 대해 애플리케이션 내 [이벤트 리스너](/docs/12.x/events)를 생성하여 다룰 수 있습니다:

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 이벤트 처리.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```
