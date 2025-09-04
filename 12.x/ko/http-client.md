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
- [매크로](#macros)
- [테스트](#testing)
    - [응답 가짜 처리](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [불필요한 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/) 위에 표현력 있고 최소한의 API를 제공함으로써, 다른 웹 애플리케이션과 통신하기 위한 HTTP 요청을 빠르게 보낼 수 있도록 지원합니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례와 개발자의 생산성을 우선적으로 고려해 설계되었습니다.

<a name="making-requests"></a>
## 요청 보내기 (Making Requests)

요청을 보내기 위해서는 `Http` 파사드가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL로 기본적인 `GET` 요청을 보내는 방법부터 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 응답을 확인할 수 있는 다양한 메서드를 제공합니다:

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있으므로, 응답의 JSON 데이터를 배열처럼 직접 참조할 수 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```

위에 나열한 메서드 외에도, 아래 메서드들을 사용하여 응답의 특정 상태 코드를 쉽게 확인할 수 있습니다:

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

HTTP 클라이언트는 [URI 템플릿 스펙](https://www.rfc-editor.org/rfc/rfc6570)을 사용하여 요청 URL을 동적으로 생성하는 것도 지원합니다. `withUrlParameters` 메서드를 이용해 URI 템플릿에 사용할 파라미터를 지정할 수 있습니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 디버깅(dd)

요청을 실제로 전송하기 전에 해당 요청 인스턴스를 덤프하여 코드 실행을 중단하고 싶다면, 요청 정의 앞에 `dd` 메서드를 추가하면 됩니다:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터 (Request Data)

`POST`, `PUT`, `PATCH` 요청을 보낼 때는 추가 데이터를 함께 전송하는 것이 일반적입니다. 이런 경우 두 번째 인수로 데이터를 배열 형태로 전달할 수 있습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청의 쿼리 파라미터

`GET` 요청을 보낼 때는 쿼리 스트링을 직접 URL에 추가하거나, 두 번째 인수로 키/값 쌍의 배열을 전달할 수 있습니다:

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
#### Form URL Encoded 타입 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내고 싶다면, 요청 전에 `asForm` 메서드를 호출해야 합니다:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 본문 데이터 전송

요청 시 Raw 데이터로 본문을 직접 지정하려면 `withBody` 메서드를 사용할 수 있습니다. 두 번째 인수로 콘텐츠 타입을 지정하면 됩니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트(Multi-Part) 요청

파일을 멀티파트 요청으로 전송하려면, 요청 전에 `attach` 메서드를 호출해야 합니다. 이 메서드는 파일의 이름과 내용을 인수로 받으며, 필요하다면 세 번째 인수로 파일명, 네 번째 인수로 파일에 사용될 헤더 정보를 추가할 수 있습니다:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 실제 내용을 바로 전달하는 대신, 스트림 리소스를 전달할 수도 있습니다:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더 (Headers)

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용할 수 있습니다. 이 메서드는 키/값 쌍의 배열을 인수로 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

응답에서 기대하는 콘텐츠 타입을 지정하고 싶다면 `accept` 메서드를 사용할 수 있습니다:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

응답 타입으로 `application/json`을 기대한다면, 더 간단하게 `acceptJson` 메서드를 사용해도 됩니다:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 새로운 헤더를 기존 요청 헤더에 병합합니다. 모든 헤더를 완전히 교체하고 싶다면, `replaceHeaders` 메서드를 사용하면 됩니다:

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

기본 인증(Basic authentication) 및 다이제스트 인증(Digest authentication)은 `withBasicAuth`와 `withDigestAuth` 메서드를 각각 사용해 지정할 수 있습니다:

```php
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

요청의 `Authorization` 헤더에 바로 Bearer 토큰을 추가하려면 `withToken` 메서드를 사용할 수 있습니다:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃 (Timeout)

`timeout` 메서드로 응답 대기 최대 시간을 초 단위로 지정할 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 후 타임아웃됩니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```

만약 지정된 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버에 연결을 시도하는 동안 대기할 최대 시간을 지정하려면 `connectTimeout` 메서드를 사용할 수 있습니다. 기본값은 10초입니다:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도 (Retries)

HTTP 클라이언트가 클라이언트나 서버 오류(4xx, 5xx)가 발생하면 자동으로 요청을 재시도하게 하려면, `retry` 메서드를 사용할 수 있습니다. 이 메서드는 최대 시도 횟수와 각 시도 간 대기 시간을 밀리초 단위로 받습니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

재시도 대기 시간을 직접 계산하고 싶다면, 두 번째 인수에 클로저를 전달할 수 있습니다:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

편의를 위해, 첫 번째 인수에 배열을 전달해서 각 재시도마다 대기할 밀리초 시간을 지정할 수도 있습니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면, 세 번째 인수로 재시도가 수행되어야 하는지 여부를 판별하는 콜러블(callable)을 전달할 수도 있습니다. 예를 들어, 연결 예외(`ConnectionException`)가 발생했을 때만 재시도하려는 경우 다음과 같이 사용할 수 있습니다:

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

각 재시도 전에 요청을 수정해야 할 경우, `retry` 메서드에 전달한 콜러블에서 인수로 전달받은 요청 객체를 수정할 수 있습니다. 예를 들어, 첫 번째 시도에서 인증 오류(401)가 발생하면 새 토큰으로 재요청하도록 만들 수 있습니다:

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

모든 재시도 요청이 실패한 경우, 기본적으로 `Illuminate\Http\Client\RequestException` 예외가 발생합니다. 이 동작을 끄고 싶다면, `throw` 인수를 `false`로 전달하면 됩니다. 비활성화 시에는 재시도 후 마지막으로 받은 응답이 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 연결 문제로 인해 모든 요청이 실패하면, `throw` 인수를 `false`로 지정하더라도 여전히 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

<a name="error-handling"></a>
### 에러 처리 (Error Handling)

Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 서버로부터 클라이언트 오류(4xx)나 서버 오류(5xx)가 반환되어도 예외를 발생시키지 않습니다. 이러한 오류가 반환되었는지 확인하려면 `successful`, `clientError`, `serverError` 메서드를 사용할 수 있습니다:

```php
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 400대 상태 코드인지 확인...
$response->clientError();

// 500대 상태 코드인지 확인...
$response->serverError();

// 클라이언트 또는 서버 오류가 발생하면 콜백 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생 (Throwing Exceptions)

응답 인스턴스가 있을 때, 상태 코드가 오류를 의미하면 `Illuminate\Http\Client\RequestException` 예외를 발생시키려면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트 또는 서버 오류가 발생하면 예외 발생...
$response->throw();

// 오류가 발생했고 조건이 참이면 예외 발생...
$response->throwIf($condition);

// 오류가 발생했고 클로저 결과가 참이면 예외 발생...
$response->throwIf(fn (Response $response) => true);

// 오류가 발생했고 조건이 거짓이면 예외 발생...
$response->throwUnless($condition);

// 오류가 발생했고 클로저 결과가 거짓이면 예외 발생...
$response->throwUnless(fn (Response $response) => false);

// 상태 코드가 특정 값일 때 예외 발생...
$response->throwIfStatus(403);

// 상태 코드가 특정 값이 아닐 때 예외 발생...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 점검할 수 있는 공개 `$response` 속성이 있습니다.

`throw` 메서드는 오류가 없으면 응답 인스턴스를 반환하므로, 이후 메서드와 체이닝해서 사용할 수 있습니다:

```php
return Http::post(/* ... */)->throw()->json();
```

예외 발생 전에 추가 로직을 실행하고 싶다면 `throw` 메서드에 클로저를 전달하면 됩니다. 이때 클로저 내부에서 예외를 명시적으로 다시 throw할 필요는 없습니다. 클로저 실행 후 예외가 자동으로 발생합니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그 작성이나 예외 리포트 시 120자까지만 표시됩니다. 이 동작을 커스터마이즈하거나 비활성화하려면, `bootstrap/app.php` 파일에서 `truncateRequestExceptionsAt` 또는 `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions): void {
    // 예외 메시지 240자로 제한...
    $exceptions->truncateRequestExceptionsAt(240);

    // 예외 메시지 자르기 비활성화...
    $exceptions->dontTruncateRequestExceptions();
})
```

또는, `truncateExceptionsAt` 메서드를 사용해 각 요청별로 예외 메시지 절단 길이를 지정할 수 있습니다:

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어 (Guzzle Middleware)

Laravel의 HTTP 클라이언트는 Guzzle 기반이므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 나가는 요청의 조작이나 들어오는 응답의 검사를 할 수 있습니다. 나가는 요청을 조작하려면 `withRequestMiddleware` 메서드로 Guzzle 미들웨어를 등록합니다:

```php
use Illuminate\Support\Facades.Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 들어오는 HTTP 응답을 검사하려면 `withResponseMiddleware` 메서드에 미들웨어를 등록하면 됩니다:

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

모든 나가는 요청/들어오는 응답에 적용되는 전역 미들웨어를 등록하고 싶을 때는 `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용할 수 있습니다. 보통은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 등록합니다:

```php
use Illuminate\Support\Facades.Http;

Http::globalRequestMiddleware(fn ($request) => $request->withHeader(
    'User-Agent', 'Example Application/1.0'
));

Http::globalResponseMiddleware(fn ($response) => $response->withHeader(
    'X-Finished-At', now()->toDateTimeString()
));
```

<a name="guzzle-options"></a>
### Guzzle 옵션 (Guzzle Options)

추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정하려면 `withOptions` 메서드를 사용할 수 있습니다. 이 메서드는 키/값 쌍의 배열을 인수로 받습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 글로벌 옵션

모든 나가는 요청의 기본 옵션을 설정하려면 `globalOptions` 메서드를 사용할 수 있습니다. 일반적으로는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 설정합니다:

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
## 동시 요청 (Concurrent Requests)

때때로 여러 개의 HTTP 요청을 동시에(병렬로) 보내고 싶을 수 있습니다. 즉, 요청을 순차적으로 보내지 않고 동시에 여러 개를 전송하여 속도가 느린 HTTP API와 통신할 때 성능을 크게 개선할 수 있습니다.

이럴 때는 `pool` 메서드를 사용하면 됩니다. 이 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 전달받는 클로저를 인수로 받으며, 클로저 내에서 요청 풀에 여러 요청을 간단히 추가할 수 있습니다:

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

위 예처럼, 각 응답 인스턴스는 풀에 추가한 순서대로 배열로 접근할 수 있습니다. 요청에 이름을 붙이고 싶다면, `as` 메서드를 사용해서 각 요청을 명명하고, 응답도 이름으로 접근할 수 있습니다:

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

`pool` 메서드는 `withHeaders`나 `middleware` 같은 HTTP 클라이언트의 다른 메서드와 체이닝할 수 없습니다. 풀에 포함되는 각 요청에 커스텀 헤더나 미들웨어를 적용하고 싶다면, 풀 내의 각 요청별로 따로 옵션을 지정해야 합니다:

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

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있어, 서비스와 상호작용할 때 공통적으로 사용되는 요청 경로나 헤더를 유연하고 간편하게 구성할 수 있습니다. 매크로는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 정의할 수 있습니다:

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

매크로가 정의되면, 애플리케이션 어디서든 호출해 지정한 구성을 가진 대기 중(Pending) 요청을 생성할 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

Laravel의 다양한 서비스들처럼, Laravel HTTP 클라이언트도 테스트 코드를 손쉽게 작성할 수 있는 기능을 제공합니다. `Http` 파사드의 `fake` 메서드를 사용하면 요청이 실제로 실행되는 대신, 더미/가짜 응답을 반환하도록 만들 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜 처리 (Faking Responses)

예를 들어, 모든 요청에 대해 비어 있는 200 응답을 반환하도록 하려면 인수 없이 `fake` 메서드를 호출합니다:

```php
use Illuminate\Support\Facades.Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 응답 가짜화

배열을 `fake` 메서드에 전달하면, 배열의 키에는 가짜화할 URL 패턴과 응답을 매핑할 수 있습니다. `*` 문자는 와일드카드로 사용할 수 있습니다. 지정한 엔드포인트에 대한 가짜/더미 응답을 만들려면 `Http` 파사드의 `response` 메서드를 사용합니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대한 문자열 응답...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

가짜화하지 않은 URL로의 요청은 실제로 실행됩니다. 모든 매칭되지 않은 URL에 대해 기본 응답을 사용하려면 와일드카드 `*`를 사용할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 기타 모든 엔드포인트는 문자열 응답...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

더 간단하게, 문자열, 배열, 정수 등을 응답으로 넣으면 각각 문자열, JSON, 비어있는 응답으로 처리됩니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 가짜화

때로는 HTTP 클라이언트가 요청 중 `Illuminate\Http\Client\ConnectionException`을 만났을 때 애플리케이션이 어떻게 동작하는지 테스트하고 싶을 수 있습니다. 이럴 때는 `failedConnection` 메서드를 사용해 클라이언트가 연결 예외를 발생시키게 할 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

또한, `Illuminate\Http\Client\RequestException`이 발생했을 때의 동작을 테스트하려면 `failedRequest` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 가짜화

단일 URL에서 정해진 순서대로 여러 개의 가짜 응답을 반환하고 싶은 경우, `Http::sequence` 메서드를 사용해 응답 시퀀스를 설정할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 연속 응답 구성...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

응답 시퀀스에 등록된 모든 응답이 소진되면, 이후 요청에는 예외가 발생합니다. 시퀀스가 비었을 때 반환될 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용하세요:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 연속 응답 구성...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴을 따로 지정하지 않고 응답 시퀀스만 만들고 싶을 땐 `Http::fakeSequence`를 사용할 수 있습니다:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 가짜 콜백 (Fake Callback)

특정 엔드포인트에 대해 반환할 응답을 복잡한 논리로 결정하고 싶을 때는, `fake` 메서드에 클로저를 전달하면 됩니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받아, 응답 인스턴스를 반환해야 합니다. 클로저 내에서 필요한 논리를 수행해 적절한 응답을 반환할 수 있습니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사 (Inspecting Requests)

응답을 가짜로 처리하는 경우, 실제로 클라이언트가 받은 요청을 확인하여 올바른 데이터/헤더가 전송되었는지 검사하고 싶을 수 있습니다. 이럴 때는 `Http::fake`를 호출한 후 `Http::assertSent` 메서드를 사용할 수 있습니다.

`assertSent` 메서드는 `Illuminate\Http\Client\Request` 인스턴스를 받아, 검사 조건에 맞으면 true를 반환해야 하며, 조건을 만족하는 요청이 최소 한 번은 실행되어야 합니다:

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

특정 요청이 전송되지 않았음을 검증하려면 `assertNotSent` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades.Http;

Http::fake();

Http::post('http://example.com/users', [
    'name' => 'Taylor',
    'role' => 'Developer',
]);

Http::assertNotSent(function (Request $request) {
    return $request->url() === 'http://example.com/posts';
});
```

테스트 중 "전송된" 요청의 개수를 검증하려면 `assertSentCount` 메서드를 사용하세요:

```php
Http::fake();

Http::assertSentCount(5);
```

또는, 아무 요청도 전송되지 않았는지 검증하려면 `assertNothingSent` 메서드를 사용할 수 있습니다:

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드로 모든 요청과 각 요청에 대한 응답을 모을 수 있습니다. `recorded` 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스가 쌍으로 담긴 배열의 컬렉션을 반환합니다:

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

또한, `recorded` 메서드에 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response`를 받아 원하는 요청/응답 쌍만 필터링할 수 있는 클로저를 전달할 수도 있습니다:

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

HTTP 클라이언트를 통해 전송된 모든 요청이 테스트 중 반드시 가짜 처리되었는지 확인하려면 `preventStrayRequests` 메서드를 호출하면 됩니다. 이 메서드가 활성화되면, 가짜 응답이 없는 요청은 실제 전송되는 대신 예외가 발생합니다:

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

때로는 대부분의 불필요한 요청을 막으면서, 특정 요청만 실제로 실행하고 싶을 수 있습니다. 이를 위해 `allowStrayRequests` 메서드에 허용할 URL 패턴의 배열을 전달할 수 있으며, 해당 패턴에 일치하는 요청만 통과시키고 나머지는 예외를 발생시킵니다:

```php
use Illuminate\Support\Facades.Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// 이 요청은 실행됨...
Http::get('http://127.0.0.1:5000/generate');

// 예외 발생...
Http::get('https://laravel.com');
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 HTTP 요청을 보내는 과정에서 세 개의 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 전송되기 전에 발생하며, `ResponseReceived` 이벤트는 응답이 수신된 후 발생합니다. 요청에 대해 응답을 받지 못하면 `ConnectionFailed` 이벤트가 발생합니다.

`RequestSending` 및 `ConnectionFailed` 이벤트에는 `Illuminate\Http\Client\Request` 인스턴스를 확인할 수 있는 공개 `$request` 속성이 있습니다. `ResponseReceived` 이벤트는 `$request`와 함께 응답 인스턴스인 `$response` 속성을 제공합니다. 이 이벤트들은 [이벤트 리스너](/docs/12.x/events)로 처리할 수 있습니다:

```php
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
