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
    - [불필요한 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 감싸는 간결하고 표현력 있는 API를 제공합니다. 이를 활용해 다른 웹 애플리케이션과 통신하기 위한 HTTP 요청을 신속하게 보낼 수 있습니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례에 집중되어 있으며, 개발자에게 훌륭한 사용 경험을 제공합니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보내기 위해 `Http` 파사드가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 우선, 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 다양한 응답 검사용 메서드를 제공하는 `Illuminate\Http\Client\Response` 인스턴스를 반환합니다.

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스를 구현하므로, JSON 형태의 응답 데이터를 배열처럼 바로 접근할 수 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

위에 나온 응답 메서드 외에도, 특정 HTTP 상태 코드 여부를 확인할 수 있는 아래 메서드들도 사용할 수 있습니다.

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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 활용해 요청 URL을 만들 수 있습니다. URI 템플릿에서 확장될 URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용할 수 있습니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프

요청이 실제로 전송되기 전에 해당 요청 인스턴스를 덤프(출력 후 종료)하려면, 요청 정의 처음에 `dd` 메서드를 추가합니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

`POST`, `PUT`, `PATCH` 요청 시 추가 데이터를 함께 보내는 경우가 많으므로, 이 메서드들의 두 번째 인수로 데이터를 배열 형태로 전달할 수 있습니다. 기본적으로 데이터는 `application/json` Content-Type으로 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청시, URL에 쿼리 문자열을 직접 붙이거나, `get` 메서드의 두 번째 인수로 키/값 배열을 전달할 수 있습니다.

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또한, `withQueryParameters` 메서드를 사용할 수도 있습니다.

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
#### Form URL Encoded 방식 요청 데이터 전송

`application/x-www-form-urlencoded` Content-Type으로 데이터를 보내고 싶다면, 요청 전에 `asForm` 메서드를 호출하세요.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 바디 전송

요청시 Raw 데이터 바디를 직접 지정하고 싶다면, `withBody` 메서드를 사용할 수 있습니다. 이때 Content-Type은 두 번째 인수로 지정합니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트(Multi-Part) 요청

파일을 멀티파트 방식으로 전송하려면, 요청 전에 `attach` 메서드를 사용해야 합니다. 이 메서드는 파일의 이름과 내용을 인수로 받으며, 필요하다면 세 번째 인수에 파일명을, 네 번째 인수에는 파일 관련 추가 헤더를 지정할 수 있습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 실제 내용을 직접 전달하는 대신 스트림 리소스를 전달할 수도 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용할 수 있습니다. 배열 형태의 키/값 쌍을 인수로 전달하세요.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

응답에서 기대하는 Content-Type을 지정하려면 `accept` 메서드를 사용할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

좀 더 간단하게, `application/json` Content-Type을 기대한다고 명시하고 싶은 경우 `acceptJson` 메서드를 사용할 수 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 헤더에 새로운 헤더를 병합합니다. 필요하다면, `replaceHeaders` 메서드를 사용해 모든 헤더를 완전히 교체할 수 있습니다.

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

기본 인증(basic authentication)과 다이제스트 인증(digest authentication) 자격 증명을 각각 `withBasicAuth`와 `withDigestAuth` 메서드로 지정할 수 있습니다.

```php
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

`Authorization` 헤더에 Bearer 토큰을 빠르게 추가하려면 `withToken` 메서드를 사용합니다.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

응답 대기 최대 시간을 초 단위로 지정하고 싶다면 `timeout` 메서드를 사용할 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 후에 타임아웃 됩니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버 연결 시도에 대해 대기할 최대 초를 지정하려면 `connectTimeout` 메서드를 사용할 수 있습니다. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트 또는 서버 오류 발생 시 자동으로 재시도하려면 `retry` 메서드를 사용할 수 있습니다. 이 메서드는 요청을 시도할 최대 횟수와 시도 사이에 대기할 밀리초(ms) 단위의 시간을 인수로 받습니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

재시도 사이 대기 시간을 직접 계산하고 싶다면, 두 번째 인수로 클로저를 전달할 수 있습니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

첫 번째 인수에 배열을 전달하면, 각 재시도 시점마다 해당 배열의 밀리초 값만큼 대기합니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요에 따라, 세 번째 인수에 콜러블을 제공해 재시도가 실제로 수행될지 판단할 수 있습니다. 예를 들어, 최초 요청에서 `ConnectionException`이 발생했을 때만 재시도하도록 할 수 있습니다.

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청 시도에 실패하면, 새로운 시도 전에 요청 객체를 수정할 수도 있습니다. 예를 들어, 첫 시도에서 인증 오류가 발생하면 새 토큰으로 재시도할 수 있습니다.

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 예외가 발생합니다. 이 동작을 비활성화하려면 `throw` 인수를 `false`로 지정할 수 있으며, 이 경우 모든 재시도 후 마지막 응답이 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 이슈로 인해 실패한 경우, `throw` 인수가 `false`여도 `Illuminate\Http\Client\ConnectionException` 예외는 여전히 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, Laravel HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(`400`, `500`번대 서버 응답)에 대해 예외를 발생시키지 않습니다. 이 오류가 반환되었는지 확인하려면 `successful`, `clientError`, `serverError` 등의 메서드를 사용할 수 있습니다.

```php
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 상태 코드가 400번대인지 확인...
$response->clientError();

// 상태 코드가 500번대인지 확인...
$response->serverError();

// 클라이언트 또는 서버 오류가 있을 시 콜백 바로 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생시키기

응답 인스턴스에서 상태 코드가 클라이언트 또는 서버 오류임을 나타내면, `Illuminate\Http\Client\RequestException` 예외를 발생시키고 싶을 때는 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트 또는 서버 오류 시 예외 발생...
$response->throw();

// 오류이며 주어진 조건이 true일 때 예외 발생...
$response->throwIf($condition);

// 오류이며 주어진 클로저가 true를 반환하면 예외 발생...
$response->throwIf(fn (Response $response) => true);

// 오류이며 조건이 false면 예외 발생...
$response->throwUnless($condition);

// 오류이며 클로저가 false면 예외 발생...
$response->throwUnless(fn (Response $response) => false);

// 지정된 상태 코드일 때 예외 발생...
$response->throwIfStatus(403);

// 지정된 상태 코드가 아니면 예외 발생...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 객체에는 반환된 응답을 확인할 수 있는 공개 속성 `$response`가 있습니다.

`throw` 메서드는 오류가 없으면 응답 인스턴스를 반환하므로, 후속 작업을 체이닝할 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 직전에 추가 로직을 실행하려면, `throw` 메서드에 클로저를 전달하세요. 이때 클로저 실행 후 예외가 자동으로 발생하므로, 클로저 내부에서 별도로 예외를 다시 던질 필요는 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로, `RequestException` 메시지는 로그 또는 보고시 120자로 잘립니다(Truncate). 이를 커스터마이징하거나 비활성화하려면, 애플리케이션의 `bootstrap/app.php`에서 `truncateAt`, `dontTruncate` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Client\RequestException;

->registered(function (): void {
    // 예외 메시지 최대 240자로 잘라서 저장...
    RequestException::truncateAt(240);

    // 예외 메시지 자르기 비활성화...
    RequestException::dontTruncate();
})
```

또는, `truncateExceptionsAt` 메서드를 사용해 요청 단위로 잘림 동작을 제어할 수도 있습니다.

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel의 HTTP 클라이언트는 Guzzle로 구현되어 있으므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용하여 요청이나 응답을 조작할 수 있습니다. 요청을 조작하려면 `withRequestMiddleware` 메서드를 통해 미들웨어를 등록하세요.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

응답을 검사하려면 `withResponseMiddleware` 메서드를 사용합니다.

```php
use Illuminate\Support\Facades.Http;
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

모든 요청 및 응답에 적용되는 전역 미들웨어를 등록하고자 할 때는 `globalRequestMiddleware`, `globalResponseMiddleware` 메서드를 사용하세요. 이 메서드는 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 설정하려면 `withOptions` 메서드를 사용할 수 있습니다. 이 메서드의 인수는 키/값 배열입니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션

모든 요청에 적용할 기본 옵션을 설정하고 싶다면, `globalOptions` 메서드를 활용하세요. 이 메서드도 역시 `AppServiceProvider`의 `boot` 메서드에서 호출하면 됩니다.

```php
use Illuminate\Support\Facades.Http;

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
## 동시 요청

여러 개의 HTTP 요청을 동시에 보내야 할 때가 있습니다. 즉, 요청을 순차적으로 보내는 대신 여러 요청을 한 번에 동시에 보내고자 할 때 사용합니다. 느린 HTTP API와 연동할 때 성능을 크게 개선할 수 있습니다.

<a name="request-pooling"></a>
### 요청 풀링

이때는 `pool` 메서드를 사용하면 쉽게 동시 요청을 할 수 있습니다. `pool` 메서드는 클로저를 인수로 받으며, 이 클로저에서는 `Illuminate\Http\Client\Pool` 인스턴스를 받아 여러 요청을 요청 풀에 추가합니다.

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

보시다시피, 각 응답 인스턴스는 풀에 추가된 순서에 따라 인덱스 또는 이름으로 접근할 수 있습니다. 원하는 경우, `as` 메서드를 사용해 각 요청에 이름을 부여할 수 있습니다.

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

요청 풀의 최대 동시성(concurrency)은 `pool` 메서드에 `concurrency` 인수를 제공하여 제어할 수 있습니다. 이 값은 한 번에 동시에 진행될 수 있는 HTTP 요청의 최대 개수를 의미합니다.

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

<a name="customizing-concurrent-requests"></a>
#### 동시 요청 커스터마이징

`pool` 메서드는 `withHeaders`나 `middleware`와 같은 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀에 들어가는 각 요청마다 직접 옵션을 지정해야 합니다.

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
### 요청 배치 처리

Laravel에서 동시 요청을 다루는 또 다른 방법은 `batch` 메서드를 사용하는 것입니다. 이 메서드는 `pool`과 마찬가지로 클로저로 `Illuminate\Http\Client\Batch` 인스턴스를 받아 요청들을 한 번에 추가할 수 있으며, 완료 콜백도 정의할 수 있습니다.

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
    // 배치가 생성됐지만 아직 요청이 초기화되지 않았을 때...
})->progress(function (Batch $batch, int|string $key, Response $response) {
    // 개별 요청이 성공적으로 완료됐을 때...
})->then(function (Batch $batch, array $results) {
    // 모든 요청이 성공적으로 완료됐을 때...
})->catch(function (Batch $batch, int|string $key, Response|RequestException|ConnectionException $response) {
    // 배치에서 첫 실패 상황 감지 시...
})->finally(function (Batch $batch, array $results) {
    // 배치가 실행을 모두 마쳤을 때...
})->send();
```

`pool` 메서드처럼, `as` 메서드로 요청에 이름을 지정할 수 있습니다.

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

`send` 메서드로 `batch`가 시작된 이후에는, 새로운 요청을 더 추가할 수 없습니다. 이를 시도하면 `Illuminate\Http\Client\BatchInProgressException` 예외가 발생합니다.

요청 배치의 최대 동시성(concurrency)은 `concurrency` 메서드를 통해 제어할 수 있습니다. 이 값은 한 번에 동시에 처리할 수 있는 HTTP 요청의 최대 개수를 나타냅니다.

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a name="inspecting-batches"></a>
#### 배치 검사

배치 완료 콜백에 전달되는 `Illuminate\Http\Client\Batch` 인스턴스는, 해당 배치의 상태를 확인하고 상호작용할 수 있는 여러 속성 및 메서드를 제공합니다.

```php
// 배치에 할당된 요청 개수
$batch->totalRequests;
 
// 아직 처리되지 않은 요청 개수
$batch->pendingRequests;
 
// 실패한 요청 개수
$batch->failedRequests;

// 지금까지 처리된 요청 수
$batch->processedRequests();

// 배치가 실행 종료됐는지 여부
$batch->finished();

// 배치 내 요청 실패가 있는지 여부
$batch->hasFailures();
```

<a name="deferring-batches"></a>
#### 배치 지연 실행

`defer` 메서드를 호출하면, 요청 배치가 즉시 실행되지 않고, 현재 애플리케이션 응답이 사용자에게 전송된 후 비동기적으로 실행됩니다. 이를 통해 애플리케이션의 반응속도를 높일 수 있습니다.

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->then(function (Batch $batch, array $results) {
    // 모든 요청이 성공적으로 완료됐을 때...
})->defer();
```

<a name="macros"></a>
## 매크로

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있는데, 이는 애플리케이션 전역적으로 공통 요청 경로와 헤더를 간편하게 구성할 수 있는 유연한 메커니즘입니다. 매크로를 정의하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 아래와 같이 설정하세요.

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

매크로가 정의되었다면, 애플리케이션 어디서든 매크로를 호출해 지정된 설정 값을 가진 PendingRequest 객체를 쉽게 생성할 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

많은 Laravel 서비스는 테스트를 더 쉽게 작성할 수 있는 기능을 제공합니다. HTTP 클라이언트 역시 예외가 아닙니다. `Http` 파사드의 `fake` 메서드를 이용해, 요청이 발생할 때 stub(더미) 응답을 반환하도록 할 수 있습니다.

<a name="faking-responses"></a>
### 응답 페이크 처리

예를 들어, 모든 요청에 대해 빈 200 상태 응답을 반환하게 하려면 인수 없이 `fake` 메서드를 호출하세요.

```php
use Illuminate\Support\Facades.Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL의 페이크 처리

또는 배열을 전달할 수도 있습니다. 배열의 키에는 페이크를 처리할 URL 패턴을, 값에는 해당 패턴에 대한 응답을 지정합니다. `*`는 와일드카드 문자로 사용될 수 있습니다. 스텁(더미) 응답을 만들 때는 `Http` 파사드의 `response` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 스텁...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대한 문자열 응답 스텁...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

페이크되지 않은 URL로의 요청은 실제로 실행됩니다. 모든 패턴에 일치하지 않는 요청도 스텁하려면, 키에 단일 `*` 문자를 사용하면 됩니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 스텁...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트에 대한 문자열 응답 스텁...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

편의상, 문자열, 배열, 정수 값을 응답 값으로 사용해 간단한 문자열·JSON·빈 응답을 만들 수 있습니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 페이크 처리

애플리케이션이 요청에 실패하여 `Illuminate\Http\Client\ConnectionException`이 발생할 때의 동작을 테스트하고 싶다면, `failedConnection` 메서드를 통해 HTTP 클라이언트가 연결 예외를 발생시키도록 지정할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException` 예외가 발생하는 상황을 테스트하려면, `failedRequest` 메서드를 사용할 수 있습니다.

```php
$this->mock(GithubService::class);
    ->shouldReceive('getUser')
    ->andThrow(
        Http::failedRequest(['code' => 'not_found'], 404)
    );
```

<a name="faking-response-sequences"></a>
#### 순차적 응답 페이크 처리

특정 URL이 순서대로 여러 개의 응답을 반환하는 경우를 테스트하려면, `Http::sequence` 메서드를 사용해 응답 시퀀스를 구성할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트 응답 시퀀스 스텁...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

모든 응답 시퀀스가 소진되면 이후 요청은 예외가 발생합니다. 빈 시퀀스일 때 반환할 기본 응답을 지정하려면, `whenEmpty` 메서드를 사용하세요.

```php
Http::fake([
    // GitHub 엔드포인트 응답 시퀀스 스텁...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴과 상관없이 응답 시퀀스를 페이크하고 싶을 땐 `Http::fakeSequence` 메서드를 사용할 수 있습니다.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 페이크 콜백

더 복잡한 논리로 특정 엔드포인트의 페이크 응답을 반환하려면, 클로저를 `fake` 메서드에 전달하세요. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받아서, 적절한 응답 인스턴스를 반환해야 합니다.

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사

응답을 페이크할 때, 올바른 데이터나 헤더가 실제로 요청되는지 검사하고 싶을 수 있습니다. `Http::fake` 호출 후 `Http::assertSent` 메서드를 사용하세요.

`assertSent` 메서드는 클로저를 인수로 받는데, 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받아 불리언을 반환해야 합니다. 주어진 조건을 만족하는 요청이 한 번 이상 있었다면 테스트는 통과합니다.

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

특정 요청이 발송되지 않았음을 확인하고 싶다면, `assertNotSent` 메서드를 사용합니다.

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

`assertSentCount` 메서드로 테스트 중 "보내진" 요청의 개수를 검사할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

혹은 `assertNothingSent`로 아무 요청도 보내지지 않았음을 확인할 수도 있습니다.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용해, 모든 요청과 해당 응답을 수집할 수 있습니다. `recorded`는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 가진 배열 컬렉션을 반환합니다.

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

또한, `recorded`에 클로저를 전달해 요청/응답 쌍을 필터링할 수도 있습니다.

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
### 불필요한 요청 방지

개별 테스트 또는 전체 테스트에서 HTTP 클라이언트로 보내는 모든 요청이 반드시 페이크되었는지 확인하고 싶다면, `preventStrayRequests` 메서드를 호출하세요. 이후 일치하는 페이크 응답이 없는 요청은 실제로 전송되지 않고 예외가 발생합니다.

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

특정 요청만 실제로 허용하고 나머지는 막고 싶다면, `allowStrayRequests` 메서드에 URL 패턴 배열을 전달하면 됩니다. 주어진 패턴과 일치하는 요청만 허용되고, 나머지는 예외가 발생합니다.

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

Laravel에서는 HTTP 요청을 보내는 과정에서 세 가지 이벤트가 발생합니다. 요청이 전송되기 직전에 `RequestSending` 이벤트, 응답을 받은 뒤에는 `ResponseReceived` 이벤트, 그리고 응답을 받지 못한 경우 `ConnectionFailed` 이벤트가 각각 발생합니다.

`RequestSending`과 `ConnectionFailed` 이벤트에는 `Illuminate\Http\Client\Request` 인스턴스를 검사할 수 있는 공개 속성 `$request`가 포함되어 있습니다. 마찬가지로, `ResponseReceived` 이벤트에는 `$request`와 `$response` 속성이 있어 `Illuminate\Http\Client\Response` 인스턴스도 확인할 수 있습니다. 이러한 이벤트에 대한 [이벤트 리스너](/docs/12.x/events)를 아래와 같이 애플리케이션에 등록해 사용할 수 있습니다.

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * Handle the event.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```