# HTTP 클라이언트 (HTTP Client)

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 데이터](#request-data)
    - [헤더](#headers)
    - [인증](#authentication)
    - [타임아웃](#timeout)
    - [재시도](#retries)
    - [오류 처리](#error-handling)
    - [Guzzle 미들웨어](#guzzle-middleware)
    - [Guzzle 옵션](#guzzle-options)
- [동시 요청](#concurrent-requests)
    - [요청 풀링](#request-pooling)
    - [요청 배치](#request-batching)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 가짜 처리](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [비정상 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 감싸는 간결하고 표현력 있는 API를 제공하여, 다른 웹 애플리케이션과의 통신을 위해 외부 HTTP 요청을 빠르게 만들 수 있게 해줍니다. Laravel의 Guzzle 래퍼는 가장 일반적으로 사용되는 활용 사례와 개발자 경험에 초점을 맞추고 있습니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보내기 위해, `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이 객체를 통해 응답을 다양한 방식으로 확인할 수 있습니다:

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있어서 JSON 응답 데이터를 배열처럼 바로 접근할 수 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```

위에 나열된 응답 관련 메서드 외에도, 응답이 특정 HTTP 상태 코드를 가졌는지 확인할 수 있는 다음과 같은 메서드들도 사용할 수 있습니다:

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

HTTP 클라이언트는 [URI 템플릿 사양](https://www.rfc-editor.org/rfc/rfc6570)에 따라 요청 URL을 구성할 수 있습니다. URI 템플릿에서 확장할 수 있는 URL 매개변수를 정의하려면 `withUrlParameters` 메서드를 사용하면 됩니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프(dump)

요청이 전송되기 전에 해당 요청 인스턴스를 덤프하고 스크립트 실행을 중단하고 싶을 때, 요청 정의의 맨 앞에 `dd` 메서드를 추가하면 됩니다:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

`POST`, `PUT`, `PATCH` 요청을 할 때는 추가 데이터를 함께 전송하는 것이 일반적이며, 이때 두 번째 인자로 데이터 배열을 전달합니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 할 때, URL에 쿼리 문자열을 직접 추가하거나, 두 번째 인자로 key-value 배열을 전달할 수 있습니다:

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
#### 폼 URL 인코딩 요청 전송

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내고 싶을 경우, 요청 전에 `asForm` 메서드를 호출하세요:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### RAW 요청 바디 전송

요청 시 RAW 데이터(가공하지 않은 데이터)를 바디로 보내고 싶을 때는 `withBody` 메서드를 사용합니다. 이때 콘텐츠 타입은 두 번째 인자로 지정할 수 있습니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트 방식으로 전송해야 한다면, 요청 전에 `attach` 메서드를 사용해야 합니다. 이 메서드는 파일명과 파일 내용을 인수로 받으며, 필요에 따라 세 번째 인자로 파일의 이름, 네 번째 인자로 파일 관련 헤더를 지정할 수 있습니다:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 RAW 내용을 넘기는 대신, 스트림 리소스를 넘길 수도 있습니다:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용할 수 있습니다. 이 메서드는 key-value로 구성된 배열을 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

응답으로부터 어떤 콘텐츠 타입을 기대하는지 명시하려면 `accept` 메서드를 사용할 수 있습니다:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

편의를 위해, `acceptJson` 메서드를 사용하면 `application/json` 콘텐츠 타입을 기대한다는 것을 쉽게 지정할 수 있습니다:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 요청 헤더에 새 헤더를 병합합니다. 필요하다면, `replaceHeaders` 메서드를 사용해 기존 헤더를 완전히 교체할 수도 있습니다:

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

기본 인증 및 다이제스트 인증 자격증명을 각각 `withBasicAuth`와 `withDigestAuth` 메서드를 통해 지정할 수 있습니다:

```php
// Basic 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### 베어러 토큰

요청의 `Authorization` 헤더에 베어러 토큰을 쉽게 추가하려면, `withToken` 메서드를 사용하세요:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

응답을 기다릴 최대 시간을 지정하려면 `timeout` 메서드를 사용할 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 후 타임아웃됩니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```

설정한 타임아웃이 초과되면, `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버에 연결을 시도하는 최대 시간을 지정하려면 `connectTimeout` 메서드를 사용하세요. 기본값은 10초입니다:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트 오류 또는 서버 오류가 발생했을 때 HTTP 클라이언트가 요청을 자동으로 재시도하도록 하려면, `retry` 메서드를 사용할 수 있습니다. `retry` 메서드는 최대 시도 횟수와 각 시도 사이 대기 시간(밀리초)을 인수로 받습니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

각 시도 간의 대기 시간을 직접 계산해야 한다면, 두 번째 인자로 클로저를 전달할 수도 있습니다:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

편의를 위해, 첫 번째 인자로 배열을 전달할 수도 있습니다. 이 배열은 각 시도 사이 대기 시간(밀리초)을 순차적으로 사용합니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요할 경우, 세 번째 인자로 콜러블을 전달하여 실제로 재시도를 수행할지 결정할 수 있습니다. 예를 들어, 처음 요청에서 `ConnectionException`이 발생했을 때만 재시도하고 싶을 수 있습니다:

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청 시도가 실패하면, 새로운 시도 전에 요청을 일부 수정하고 싶을 수 있습니다. 이 경우 `retry` 메서드에 넘긴 콜러블에서 요청 인스턴스를 수정하면 됩니다. 예를 들어, 인증 오류(401)가 발생했을 때 새로운 인증 토큰으로 재시도하고 싶을 때 다음과 같이 할 수 있습니다:

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 예외가 발생합니다. 이 동작을 원하지 않는 경우, `throw` 인자에 `false` 값을 전달하면 됩니다. 이때 모든 재시도가 끝난 후 마지막 응답이 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패할 경우, `throw` 인자가 `false`로 설정되어 있어도 `Illuminate\Http\Client\ConnectionException` 예외는 여전히 발생합니다.

<a name="error-handling"></a>
### 오류 처리

Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트 오류나 서버 오류(서버로부터의 `400`, `500`번대 응답)에 대해 예외를 발생시키지 않습니다. 이러한 오류가 반환되었는지 여부는 `successful`, `clientError`, `serverError` 메서드로 확인할 수 있습니다:

```php
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상이면...
$response->failed();

// 400번대 상태 코드인지 확인...
$response->clientError();

// 500번대 상태 코드인지 확인...
$response->serverError();

// 클라이언트 또는 서버 오류가 발생했을 때 바로 콜백 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생

응답 인스턴스가 있고, 클라이언트 또는 서버 오류 상태 코드일 때 `Illuminate\Http\Client\RequestException` 예외를 발생시키고 싶다면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트 또는 서버 오류가 발생하면 예외를 던짐...
$response->throw();

// 오류가 발생했으며 주어진 조건이 참이면 예외를 던짐...
$response->throwIf($condition);

// 오류가 발생했고 주어진 클로저 결과가 참이면 예외를 던짐...
$response->throwIf(fn (Response $response) => true);

// 오류가 발생했으며 조건이 거짓이면 예외를 던짐...
$response->throwUnless($condition);

// 오류가 발생했고 주어진 클로저 결과가 거짓이면 예외를 던짐...
$response->throwUnless(fn (Response $response) => false);

// 응답이 특정 상태 코드면 예외를 던짐...
$response->throwIfStatus(403);

// 응답이 특정 상태 코드가 아니면 예외를 던짐...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스는 반환된 응답을 검사할 수 있도록 public `$response` 속성을 가지고 있습니다.

`throw` 메서드는 오류가 없을 때 응답 인스턴스를 반환하므로, 이후 다양한 작업을 체이닝할 수 있습니다:

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전에 추가 작업을 수행하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 이 경우 클로저 실행 후 예외는 자동으로 던져지므로 클로저 내에서 다시 던질 필요가 없습니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그 또는 보고 시 120자까지만 잘려서 출력됩니다. 이 동작을 바꾸거나 비활성화하려면, 애플리케이션의 `bootstrap/app.php` 파일에 등록된 동작에서 `truncateAt`, `dontTruncate` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Client\RequestException;

->registered(function (): void {
    // 예외 메시지를 240자까지 자르기...
    RequestException::truncateAt(240);

    // 예외 메시지 자르기 비활성화...
    RequestException::dontTruncate();
})
```

또는, 요청별로 `truncateExceptionsAt` 메서드를 사용해 예외 메시지 자르기 동작을 맞춤 설정할 수도 있습니다:

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel의 HTTP 클라이언트는 Guzzle을 기반으로 하므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 외부로 보내는 요청을 조작하거나 들어오는 응답을 감시할 수 있습니다. 요청을 조작하려면, `withRequestMiddleware` 메서드를 통해 Guzzle 미들웨어를 등록하세요:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

또한, 들어오는 HTTP 응답을 감시하려면 `withResponseMiddleware` 메서드로 미들웨어를 등록할 수 있습니다:

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

모든 외부 요청 및 응답에 적용되는 미들웨어를 등록하고 싶을 수 있습니다. 이럴 때는 `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용하면 됩니다. 보통, 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

`withOptions` 메서드를 통해, 외부로 보내는 요청에 추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정할 수 있습니다. 이 메서드는 key-value 배열을 받습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션

모든 외부 요청에 대해 기본 옵션을 설정하려면, `globalOptions` 메서드를 사용합니다. 보통 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

여러 HTTP 요청을 동시에(Parallel) 보내고 싶을 때가 있습니다. 즉, 여러 요청을 순차적으로 보내는 대신 동시에 전송하여, 느린 HTTP API와 통신할 때 성능을 크게 개선할 수 있습니다.

<a name="request-pooling"></a>
### 요청 풀링

다행히도, `pool` 메서드를 통해 동시 요청을 구현할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 인자로 받는 클로저를 인수로 받아, 요청 풀에 요청을 쉽게 추가할 수 있습니다:

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

보시다시피, 각 응답 인스턴스는 풀에 추가된 순서대로 접근할 수 있습니다. 원한다면 `as` 메서드를 사용해 요청에 이름을 지정할 수도 있습니다. 그러면 해당 이름으로 응답에 접근할 수 있습니다:

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

동시 요청 풀의 최대 동시성은 `pool` 메서드의 `concurrency` 인자를 통해 제어할 수 있습니다. 이 값은 동시에 처리될 수 있는 HTTP 요청의 최대 개수를 의미합니다:

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

<a name="customizing-concurrent-requests"></a>
#### 동시 요청 커스터마이징

`pool` 메서드는 `withHeaders`나 `middleware`와 같은 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀에 속한 각 요청에 사용자 지정 헤더나 미들웨어를 적용하려면, 각 요청을 생성할 때 설정해야 합니다:

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
### 요청 배치

Laravel에서 동시 요청을 처리하는 또 다른 방법은 `batch` 메서드를 사용하는 것입니다. 이 메서드도 `pool` 메서드와 마찬가지로 `Illuminate\Http\Client\Batch` 인스턴스를 인자로 받는 클로저를 인수로 받아 요청들을 모으거나, 완료 콜백을 정의할 수 있습니다:

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
    // 배치가 생성됐지만, 아직 요청이 초기화되지 않은 시점...
})->progress(function (Batch $batch, int|string $key, Response $response) {
    // 개별 요청 하나가 성공적으로 완료됨...
})->then(function (Batch $batch, array $results) {
    // 모든 요청이 성공적으로 끝나면...
})->catch(function (Batch $batch, int|string $key, Response|RequestException|ConnectionException $response) {
    // 배치 내 실패가 탐지되었을 때...
})->finally(function (Batch $batch, array $results) {
    // 배치가 완전히 끝났을 때...
})->send();
```

`pool` 메서드와 마찬가지로, `as` 메서드로 각 요청에 이름을 붙일 수 있습니다:

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

`send` 메서드를 호출해 `batch`가 시작되면, 새로운 요청을 추가할 수 없습니다. 추가 시도 시 `Illuminate\Http\Client\BatchInProgressException` 예외가 던져집니다.

요청 배치의 최대 동시성은 `concurrency` 메서드로 조절할 수 있습니다. 이 값은 배치 처리 중 동시에 실행 가능한 HTTP 요청의 최대 개수를 의미합니다:

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a name="inspecting-batches"></a>
#### 배치 검사

배치 완료 콜백으로 전달된 `Illuminate\Http\Client\Batch` 인스턴스에서는 다음과 같은 여러 속성과 메서드를 통해 요청 배치를 확인하고 조작할 수 있습니다:

```php
// 배치에 할당된 전체 요청 수...
$batch->totalRequests;
 
// 아직 처리되지 않은 요청 수...
$batch->pendingRequests;
 
// 실패한 요청 수...
$batch->failedRequests;

// 지금까지 처리된 요청 수...
$batch->processedRequests();

// 배치가 모두 완료되었는지 여부...
$batch->finished();

// 배치에 실패한 요청이 있는지 여부...
$batch->hasFailures();
```
<a name="deferring-batches"></a>
#### 배치 실행 지연

`defer` 메서드를 호출하면, 요청 배치는 바로 실행되지 않고 현재 애플리케이션 요청의 HTTP 응답이 사용자에게 전송된 후 실행됩니다. 이렇게 하면 애플리케이션의 응답 속도를 유지할 수 있습니다:

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->then(function (Batch $batch, array $results) {
    // 모든 요청이 성공적으로 완료됨...
})->defer();
```

<a name="macros"></a>
## 매크로

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있습니다. 매크로를 사용하면 서비스 간 자주 사용하는 요청 경로나 헤더 설정을 자유롭고 표현력 있게 재사용할 수 있습니다. 먼저, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 매크로를 정의합니다:

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

매크로를 정의한 후에는, 애플리케이션 어디서든 지정된 설정으로 요청을 생성할 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

Laravel의 다양한 서비스들은 테스트를 쉽고 표현력 있게 작성할 수 있는 기능을 제공합니다. HTTP 클라이언트 역시 예외가 아닙니다. `Http` 파사드의 `fake` 메서드를 통해, 요청이 발생할 때 가짜(더미) 응답을 반환하도록 지시할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜 처리

예를 들어, 모든 요청에 대해 빈 `200` 상태의 응답을 반환하려면, 인수 없이 `fake` 메서드를 호출하면 됩니다:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 가짜 처리

또는, `fake` 메서드에 배열을 전달할 수도 있습니다. 배열의 키는 가짜로 만들고 싶은 URL 패턴이며, 값은 해당 URL이 반환할 응답입니다. `*` 문자를 와일드카드로 사용 가능합니다. 엔드포인트를 위한 가짜 응답 생성에는 `Http` 파사드의 `response` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트용 JSON 응답 스텁
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트용 문자열 응답 스텁
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

가짜 처리되지 않은 URL로 요청이 들어오면 실제 요청이 전송됩니다. 모든 매칭되지 않은 URL에 대해 스텁을 지정하려면 `*`만 키로 사용하면 됩니다:

```php
Http::fake([
    // GitHub 엔드포인트용 JSON 응답 스텁
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 나머지 엔드포인트용 문자열 응답 스텁
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

편의상, 문자열, 배열, 정수를 응답값으로 넘기면 간단한 문자열, JSON, 빈 응답을 쉽게 생성할 수 있습니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 가짜 처리

HTTP 클라이언트가 요청할 때 `Illuminate\Http\Client\ConnectionException`이 발생하는 경우를 테스트해야 할 때가 있습니다. 이 경우 `failedConnection` 메서드를 사용해 연결 예외를 강제로 발생시킬 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException`를 발생시키고 싶을 때는 `failedRequest` 메서드를 사용할 수 있습니다:

```php
$this->mock(GithubService::class);
    ->shouldReceive('getUser')
    ->andThrow(
        Http::failedRequest(['code' => 'not_found'], 404)
    );
```

<a name="faking-response-sequences"></a>
#### 연속된 응답 가짜 처리

단일 URL에 대해 여러 개의 가짜 응답을 순차적으로 반환하도록 지정해야 할 때는, `Http::sequence` 메서드를 통해 연속된 응답을 만들 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 여러 응답 스텁
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

연속 응답이 모두 소비된 이후에 추가 요청이 들어오면, 예외가 발생합니다. 시퀀스가 비어있을 때 반환할 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용하세요:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 여러 응답 스텁
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴 없이 연속된 응답을 가짜 처리하고 싶을 땐, `Http::fakeSequence` 메서드를 사용할 수 있습니다:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 가짜 콜백

특정 엔드포인트에 대해 어떤 응답을 반환할지 더 복잡한 로직이 필요하다면, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받고, 응답 인스턴스를 반환해야 합니다. 클로저 안에서 원하는 로직을 수행해 적절한 응답을 반환할 수 있습니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사

응답을 가짜로 처리하는 경우, 애플리케이션이 올바른 데이터나 헤더를 전송하는지 확인하고 싶을 때가 있습니다. 이럴 때는 `Http::fake`를 호출한 뒤 `Http::assertSent` 메서드를 사용하세요.

`assertSent` 메서드는 클로저를 받는데, 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받고, 요청이 기대에 맞는지 여부를 나타내는 불리언 값을 반환해야 합니다. 조건을 만족하는 요청이 하나라도 있으면 테스트는 성공합니다:

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

특정 요청이 전송되지 않았음을 확인하려면 `assertNotSent` 메서드를 사용하면 됩니다:

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

`assertSentCount` 메서드를 사용해 테스트 중 "전송"된 요청 수를 검증할 수 있습니다:

```php
Http::fake();

Http::assertSentCount(5);
```

또는, 테스트 중 아무런 요청도 전송되지 않았음을 검증하려면 `assertNothingSent` 메서드를 사용하세요:

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용하면 모든 요청과 그에 대응하는 응답을 수집할 수 있습니다. `recorded` 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스로 이루어진 배열의 컬렉션을 반환합니다:

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

또한, `recorded` 메서드에 클로저를 전달해 요청/응답 쌍을 원하는 조건으로 필터링할 수도 있습니다:

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

HTTP 클라이언트를 통해 전송된 모든 요청에 가짜 응답이 적용되었는지 개별 테스트 또는 전체 테스트 슈트에서 보장하고 싶다면 `preventStrayRequests` 메서드를 사용하세요. 이 메서드 호출 후에는 가짜 응답이 없는 요청이 실제 HTTP 요청을 발생시키지 않고 예외를 던집니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답이 반환됨...
Http::get('https://github.com/laravel/framework');

// 예외가 던져짐...
Http::get('https://laravel.com');
```

대부분의 비정상 요청은 막고, 특정 요청만 허용하고 싶을 수 있습니다. 이럴 땐 `allowStrayRequests` 메서드에 허용할 URL 패턴을 배열로 전달하면 됩니다. 허용된 패턴과 일치하는 요청은 실행되고, 나머지는 예외가 발생합니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// 이 요청은 실제로 실행됨...
Http::get('http://127.0.0.1:5000/generate');

// 예외가 던져짐...
Http::get('https://laravel.com');
```

<a name="events"></a>
## 이벤트

Laravel은 HTTP 요청을 전송하는 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 전송되기 전에, `ResponseReceived` 이벤트는 특정 요청에 대한 응답이 도착했을 때 발생합니다. 그리고 `ConnectionFailed` 이벤트는 특정 요청에 대해 응답을 받지 못한 경우에 발생합니다.

`RequestSending` 및 `ConnectionFailed` 이벤트는 모두 `Illuminate\Http\Client\Request` 인스턴스를 검사할 수 있도록 public `$request` 속성을 가집니다. `ResponseReceived` 이벤트는 `$request`와 `$response` 속성을 모두 제공하여 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 검사할 수 있게 해줍니다. 이 이벤트들에 대해 애플리케이션 내에서 [이벤트 리스너](/docs/12.x/events)를 생성할 수 있습니다:

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
