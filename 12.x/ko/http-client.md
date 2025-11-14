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
    - [응답 가짜 처리(Fake)](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [불필요한 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/) 위에 표현적이고 미니멀한 API를 제공하며, 다른 웹 애플리케이션과의 통신을 위해 쉽고 빠르게 HTTP 요청을 보낼 수 있도록 지원합니다. Laravel의 Guzzle 래퍼(wrapper)는 가장 일반적으로 사용되는 케이스와 뛰어난 개발자 경험에 초점을 맞추고 있습니다.

<a name="making-requests"></a>
## 요청 보내기 (Making Requests)

요청을 보내기 위해서는 `Http` 파사드가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 응답을 검사할 수 있는 다양한 메서드를 제공합니다.

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스를 구현하고 있어, 응답의 JSON 데이터를 배열처럼 바로 접근할 수 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

위에서 소개한 응답 메서드 외에도, 응답이 특정 상태 코드를 가지고 있는지 확인할 때 다음과 같은 메서드를 사용할 수 있습니다.

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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 사용해 요청 URL을 동적으로 구성할 수 있습니다. `withUrlParameters` 메서드를 사용하여 URI 템플릿에서 확장될 URL 파라미터를 정의할 수 있습니다.

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

요청이 전송되기 전에 해당 요청 인스턴스를 덤프한 뒤, 스크립트 실행을 중단하고 싶다면, 요청 정의의 맨 앞에 `dd` 메서드를 붙이면 됩니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터 (Request Data)

`POST`, `PUT`, `PATCH` 요청을 보낼 때는 추가 데이터를 함께 보내는 경우가 많으므로, 이들 메서드는 두 번째 인수로 데이터 배열을 받습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 보낼 때, 쿼리 스트링을 직접 URL에 붙이거나, `get` 메서드의 두 번째 인자로 키/값 배열을 전달할 수 있습니다.

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는 `withQueryParameters` 메서드를 사용할 수도 있습니다.

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
#### 폼 URL 인코딩 방식 요청

만약 데이터를 `application/x-www-form-urlencoded` 방식으로 전송하고 싶다면, 요청 전에 `asForm` 메서드를 호출하세요.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 본문 전송

요청을 보낼 때 raw 형태의 본문(payload)을 추가로 보내고 싶다면, `withBody` 메서드를 사용하세요. 두 번째 인자로 콘텐츠 타입도 지정할 수 있습니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트(multipart)로 전송하고자 할 때는, 요청 전에 `attach` 메서드를 호출하면 됩니다. 이 메서드는 파일의 이름, 내용, (필요하다면) 파일명과 관련 헤더들을 받습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 원본 데이터를 직접 전달하는 대신, 스트림 리소스를 전달할 수도 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더 (Headers)

요청에 헤더를 추가하고 싶다면 `withHeaders` 메서드를 사용하세요. 이 메서드는 키/값 배열을 받습니다.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

요청에 대해 애플리케이션이 어떤 콘텐츠 타입을 기대하는지 명시하려면, `accept` 메서드를 사용할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

간편하게 `application/json` 응답을 기대한다면, `acceptJson` 메서드를 사용할 수도 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 요청 헤더에 새 헤더를 추가(병합)합니다. 필요하다면 `replaceHeaders` 메서드로 모든 헤더를 완전히 교체할 수도 있습니다.

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

기본 인증(Basic Authentication) 혹은 다이제스트 인증(Digest Authentication) 자격 증명을 각각 `withBasicAuth`, `withDigestAuth` 메서드로 지정할 수 있습니다.

```php
// Basic 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

`Authorization` 헤더에 Bearer 토큰을 간단히 추가하려면 `withToken` 메서드를 사용하세요.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃 (Timeout)

응답을 기다릴 최대 시간(초)을 지정하려면 `timeout` 메서드를 사용하세요. 기본적으로 HTTP 클라이언트는 30초 후 타임아웃됩니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 시간 내에 응답이 오지 않으면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버에 연결을 시도할 때 기다릴 최대 시간(초)은 `connectTimeout` 메서드로 지정할 수 있습니다. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도 (Retries)

클라이언트 또는 서버 오류가 발생했을 때 HTTP 클라이언트가 자동으로 요청을 재시도하도록 하려면 `retry` 메서드를 사용하면 됩니다. 첫 번째 인수는 최대 재시도 횟수, 두 번째 인수는 각 재시도 사이에 대기할 밀리초(ms) 단위 대기 시간입니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

재시도마다 대기 시간(ms)을 직접 계산하고 싶다면, 두 번째 인수에 클로저를 전달할 수 있습니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

간편하게 배열로 각 재시도 사이에 대기할 시간(ms)을 지정할 수도 있습니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면 `retry` 메서드의 세 번째 인수로 콜러블을 전달하여 실제로 재시도가 이루어져야 할지 판단할 수 있습니다. 예를 들어, 요청이 `ConnectionException`을 만났을 때만 재시도하고 싶다면 아래와 같이 작성할 수 있습니다.

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청이 실패하면, 새로운 시도를 하기 전에 요청을 수정하고 싶을 때가 있습니다. 이 경우, `retry` 메서드에 전달하는 콜러블에서 두 번째 인수로 전달되는 요청 인스턴스를 수정하여 원하는 조치를 취할 수 있습니다. 예를 들어, 인증 오류(401)가 발생하면 새 토큰으로 재시도할 수 있습니다.

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

모든 재시도 시도가 실패하면 `Illuminate\Http\Client\RequestException` 인스턴스가 던져집니다. 이 동작을 비활성화하려면 `throw` 인수에 `false`를 넘겨주세요. 비활성화하면, 모든 시도가 끝난 뒤 마지막 클라이언트 응답이 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 만약 모든 요청이 연결 문제로 실패할 경우, `throw` 인수가 `false`로 설정되어 있더라도 `Illuminate\Http\Client\ConnectionException`이 계속 던져집니다.

<a name="error-handling"></a>
### 에러 처리 (Error Handling)

Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트(4xx) 또는 서버(5xx) 오류 상태 코드에 대해 예외를 자동으로 던지지 않습니다. 이런 오류가 발생했는지는 `successful`, `clientError`, `serverError` 메서드로 확인할 수 있습니다.

```php
// 상태 코드가 200 이상 300 미만인지 확인
$response->successful();

// 상태 코드가 400 이상인지 확인
$response->failed();

// 응답이 400번대 상태 코드를 가지는지 확인
$response->clientError();

// 응답이 500번대 상태 코드를 가지는지 확인
$response->serverError();

// 클라이언트 또는 서버 오류가 발생했을 때, 콜백을 즉시 실행
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생시키기

응답 인스턴스가 있을 때, 응답 상태 코드가 클라이언트 또는 서버 오류를 뜻한다면 `Illuminate\Http\Client\RequestException`을 던지고 싶을 경우, `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트 또는 서버 오류 발생 시 예외 던지기
$response->throw();

// 오류 발생 시, 조건이 true일 때만 예외 던지기
$response->throwIf($condition);

// 오류 발생 시, 주어진 클로저가 true를 반환하면 예외 던지기
$response->throwIf(fn (Response $response) => true);

// 오류 발생 시, 조건이 false일 때 예외 던지기
$response->throwUnless($condition);

// 오류 발생 시, 주어진 클로저가 false를 반환하면 예외 던지기
$response->throwUnless(fn (Response $response) => false);

// 응답이 특정 상태 코드일 때 예외 던지기
$response->throwIfStatus(403);

// 응답이 특정 상태 코드가 아니라면 예외 던지기
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스는 반환된 응답을 확인할 수 있는 public `$response` 속성을 가지고 있습니다.

`throw` 메서드는 오류가 없으면 응답 인스턴스를 그대로 반환하기 때문에, 이어서 다른 연산을 체이닝할 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 던져지기 전에 추가 로직을 수행하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 이 클로저 호출 뒤 자동으로 예외가 발생하므로, 클로저 내에서 예외를 직접 다시 던질 필요는 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그 또는 리포트 시 120자로 잘립니다. 이 동작을 사용자 정의하거나 비활성화하려면 `bootstrap/app.php` 파일에서 `truncateAt` 또는 `dontTruncate` 메서드를 사용하세요.

```php
use Illuminate\Http\Client\RequestException;

->registered(function (): void {
    // 예외 메시지 최대 길이를 240자로 제한
    RequestException::truncateAt(240);

    // 예외 메시지 자르기 비활성화
    RequestException::dontTruncate();
})
```

또는 `truncateExceptionsAt` 메서드로 요청별로 예외 메시지 길이 제한을 지정할 수 있습니다.

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어 (Guzzle Middleware)

Laravel의 HTTP 클라이언트는 Guzzle을 기반으로 하기 때문에, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 요청을 조작하거나 응답을 검사할 수 있습니다.  
요청을 조작하려면 `withRequestMiddleware` 메서드를 통해 Guzzle 미들웨어를 등록하세요.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 요청에 대한 응답을 검사하려면 `withResponseMiddleware` 메서드를 통해 미들웨어를 등록할 수 있습니다.

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

때로는 모든 아웃고잉 요청과 응답에 늘 적용되는 미들웨어를 등록하고 싶을 수 있습니다. 이럴 땐 `globalRequestMiddleware`, `globalResponseMiddleware` 메서드를 사용하면 됩니다. 보통 이 메서드들은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출하는 것이 좋습니다.

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

아웃고잉 요청에 대해 추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정하려면 `withOptions` 메서드를 사용할 수 있습니다. `withOptions` 메서드는 키/값 배열을 받습니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 글로벌 옵션

모든 아웃고잉 요청의 기본 옵션을 설정하려면 `globalOptions` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

여러 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 요청을 하나씩 순차적으로 보내는 대신 몇 가지 요청을 동시에 보낼 수 있다는 뜻입니다. 이렇게 하면 응답이 느린 HTTP API와 상호작용할 때 성능이 크게 향상될 수 있습니다.

<a name="request-pooling"></a>
### 요청 풀링 (Request Pooling)

이 기능은 `pool` 메서드로 구현할 수 있습니다. `pool` 메서드는 클로저를 인수로 받으며, 이 클로저에는 요청 풀에 요청을 추가할 수 있는 `Illuminate\Http\Client\Pool` 인스턴스가 전달됩니다.

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

이처럼 각 응답 인스턴스는 추가 순서대로 배열로 접근할 수 있습니다. 요청에 이름을 지정하고 싶을 때는 `as` 메서드를 사용하면, 각각의 응답을 이름으로도 접근할 수 있습니다.

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

요청 풀의 최대 동시성은 `pool` 메서드에 `concurrency` 인수를 지정해 제어할 수 있습니다. 이 값은 요청 풀 처리 중 동시에 진행 가능한 HTTP 요청의 최대 개수를 결정합니다.

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

<a name="customizing-concurrent-requests"></a>
#### 동시 요청 커스터마이징

`pool` 메서드는 `withHeaders`, `middleware` 같은 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀에 들어가는 각 요청에 커스텀 헤더나 미들웨어를 적용하고 싶다면, 각 요청마다 직접 옵션을 설정해야 합니다.

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

Laravel에서 동시 요청을 처리하는 또 다른 방법은 `batch` 메서드를 사용하는 것입니다. `batch` 메서드는 `pool`과 마찬가지로 클로저를 받아, 해당 클로저에 `Illuminate\Http\Client\Batch` 인스턴스를 전달합니다. 이 방식은 요청을 쉽게 추가할 수 있을 뿐 아니라, 완료 콜백도 정의할 수 있습니다.

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
    // 배치가 생성되었지만, 아직 요청이 초기화되지 않은 상태...
})->progress(function (Batch $batch, int|string $key, Response $response) {
    // 개별 요청이 성공적으로 완료됨...
})->then(function (Batch $batch, array $results) {
    // 모든 요청이 성공적으로 완료됨...
})->catch(function (Batch $batch, int|string $key, Response|RequestException|ConnectionException $response) {
    // 첫 번째로 실패한 요청이 감지됨...
})->finally(function (Batch $batch, array $results) {
    // 배치 처리가 완료됨...
})->send();
```

`pool` 메서드와 마찬가지로, `as` 메서드로 요청에 이름을 지정할 수 있습니다.

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

`send` 메서드를 통해 배치가 시작된 이후에는 새로운 요청을 추가할 수 없습니다. 시도할 경우 `Illuminate\Http\Client\BatchInProgressException` 예외가 발생합니다.

요청 배치의 최대 동시성은 `concurrency` 메서드로 제어할 수 있습니다. 이 값은 배치 처리 중 동시에 처리될 수 있는 HTTP 요청의 최대 개수를 결정합니다.

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a name="inspecting-batches"></a>
#### 배치 검사

배치 완료 콜백에서 제공되는 `Illuminate\Http\Client\Batch` 인스턴스는 배치 요청 상태를 확인하고 다루는 데 유용한 속성과 메서드를 제공합니다.

```php
// 배치에 할당된 전체 요청 수
$batch->totalRequests;
 
// 아직 처리되지 않은 요청 수
$batch->pendingRequests;
 
// 실패한 요청 수
$batch->failedRequests;

// 지금까지 처리된 요청 수
$batch->processedRequests();

// 배치 처리가 완료되었는지 여부
$batch->finished();

// 배치에 실패한 요청이 있는지 여부
$batch->hasFailures();
```
<a name="deferring-batches"></a>
#### 배치 지연 실행

`defer` 메서드를 호출하면, 요청 배치가 즉시 실행되지 않고, 현재 애플리케이션 요청의 HTTP 응답이 사용자에게 전송된 이후에 실행됩니다. 이렇게 하면 애플리케이션이 더욱 빠르고 반응성 있게 느껴질 수 있습니다.

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
## 매크로 (Macros)

Laravel HTTP 클라이언트에서는 "매크로"를 정의할 수 있습니다. 매크로는 서비스와 상호 작용할 때 자주 사용하는 경로나 헤더 설정을 간결하고 표현적으로 재사용할 수 있게 해줍니다. 매크로를 정의하려면, 일반적으로 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에서 작성합니다.

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

매크로가 정의되었다면, 애플리케이션 어디서든 해당 설정이 적용된 요청을 빠르게 만들 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

Laravel의 많은 서비스가 손쉽고 표현적으로 테스트를 작성할 수 있게 다양한 기능을 제공합니다. HTTP 클라이언트 역시 예외는 아니며, `Http` 파사드의 `fake` 메서드를 이용해 요청 시 더미(Fake) 응답을 반환하도록 할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜 처리(Fake Responses)

예를 들어, 모든 HTTP 요청에 대해 상태 코드 200의 빈 응답을 돌려주고 싶다면, 인수 없이 `fake` 메서드를 호출하면 됩니다.

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL에 대한 응답 가짜 처리

또는, `fake` 메서드에 배열을 전달해 URL 패턴별로 지정한 응답을 반환하게 할 수 있습니다. 배열의 키는 대상 URL 패턴이 되고, 값은 해당 패턴의 응답이 됩니다. `*`는 와일드카드 문자로 사용할 수 있습니다. 엔드포인트별로 더미 응답을 만들 때는 `Http` 파사드의 `response` 메서드를 활용하세요.

```php
Http::fake([
    // GitHub 엔드포인트의 JSON 응답 가짜 처리
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트의 문자열 응답 가짜 처리
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

가짜 처리하지 않은 URL로의 요청은 실제로 실행됩니다. 모든 매치되지 않는 URL도 가짜로 처리하려면 `*` 하나만 키로 전달하면 됩니다.

```php
Http::fake([
    // GitHub 엔드포인트의 JSON 응답 가짜 처리
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 나머지 모든 엔드포인트는 기본 문자열 응답 처리
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

간단히 문자열, 배열, 정수만으로도 응답을 지정할 수 있어 편리합니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 가짜 처리

애플리케이션이 HTTP 클라이언트에서 `Illuminate\Http\Client\ConnectionException`이 발생할 때의 동작을 테스트하고 싶을 때는 `failedConnection` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException`이 던져지는 상황을 테스트하려면, `failedRequest` 메서드를 사용하세요.

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 순차 응답 가짜 처리

특정 URL에 대해 일련의 더미 응답을 순차적으로 반환하고 싶을 때는 `Http::sequence` 메서드를 이용해 응답을 만들 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 일련의 응답 순차 가짜 처리
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

응답 시퀀스의 모든 응답이 소진되었다면, 추가 요청 시 예외가 발생합니다. 시퀀스가 비었을 때 반환되는 기본 응답을 지정하고 싶다면, `whenEmpty` 메서드를 사용하세요.

```php
Http::fake([
    // GitHub 엔드포인트에 일련의 응답 순차 가짜 처리
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴을 정하지 않고, 순차적으로 여러 응답을 가짜로 만들고 싶을 때는 `Http::fakeSequence` 메서드를 사용하세요.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### Fake 콜백

특정 엔드포인트에 반환할 응답을 결정하는 데 보다 복잡한 로직이 필요하다면, `fake` 메서드에 클로저를 전달하세요. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받고, 응답 인스턴스를 반환해야 합니다.

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사 (Inspecting Requests)

응답을 가짜로 하면서, 실제로 클라이언트가 받은 요청을 검증하고 싶을 때가 있습니다. 예를 들어, 올바른 데이터나 헤더가 전송되었는지 확인하고 싶다면, `Http::fake` 호출 후 `Http::assertSent` 메서드를 사용할 수 있습니다.

`assertSent`는 클로저를 받으며, 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 인수로 받고, 요청이 기대에 부합하면 true를 반환해야 합니다. 테스트를 통과시키려면, 최소 하나의 요청이 해당 조건을 만족해야 합니다.

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

반대로, 특정 요청이 전송되지 않았음을 검증하려면 `assertNotSent` 메서드를 사용하세요.

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

`assertSentCount` 메서드로 테스트 중에 "전송된" 요청 개수도 검증할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

또한, 아무 요청도 전송되지 않았음을 검증하려면 `assertNothingSent`를 사용하세요.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청·응답 기록(Recording)

`recorded` 메서드를 사용해, 모든 요청과 해당 응답을 수집할 수 있습니다. 이 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스 배열의 컬렉션을 반환합니다.

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

또한, 요청·응답 쌍을 원하는 조건에 맞게 필터링하려면 클로저를 인수로 넘길 수 있습니다.

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
### 불필요한 요청 방지 (Preventing Stray Requests)

테스트의 특정 상황이나 전체 테스트 스위트에서, HTTP 클라이언트의 모든 요청이 반드시 가짜로 처리되도록 보장하려면 `preventStrayRequests` 메서드를 사용하면 됩니다. 이 메서드를 호출하면, 가짜 응답에 해당되지 않는 모든 요청은 실제 HTTP 요청을 전송하는 대신 예외를 던집니다.

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답이 반환됨
Http::get('https://github.com/laravel/framework');

// 예외가 발생함
Http::get('https://laravel.com');
```

특정 요청만 실제로 전송하고, 나머지는 차단하고 싶을 때는 `allowStrayRequests` 메서드에 URL 패턴 배열을 전달하세요. 지정한 패턴과 일치하는 요청만 허용되며, 나머지는 예외를 던집니다.

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// 이 요청은 실제 실행됨
Http::get('http://127.0.0.1:5000/generate');

// 예외가 발생함
Http::get('https://laravel.com');
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 HTTP 요청 처리 중 3가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 보내지기 전에 발생하고, `ResponseReceived` 이벤트는 요청에 대한 응답을 받은 뒤 발생합니다. 그리고 `ConnectionFailed` 이벤트는 요청에 대한 응답이 도착하지 못했을 때 발생합니다.

`RequestSending` 및 `ConnectionFailed` 이벤트는 모두 요청 인스턴스를 확인할 수 있는 public `$request` 속성을 제공합니다. 또한, `ResponseReceived` 이벤트에는 `$request`와 함께 응답을 확인할 수 있는 `$response` 속성도 있습니다. 이 이벤트들에 대해 [이벤트 리스너](/docs/12.x/events)를 만들어 활용할 수 있습니다.

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 이벤트 처리기
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```