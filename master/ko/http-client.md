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
- [매크로](#macros)
- [테스트](#testing)
    - [응답 가짜 처리](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [원치 않는 실제 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 감싼 간결하고 표현력이 뛰어난 API를 제공하여 다른 웹 애플리케이션과 통신하기 위한 아웃고잉 HTTP 요청을 빠르게 보낼 수 있도록 지원합니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례와 훌륭한 개발자 경험에 중점을 두고 있습니다.

<a name="making-requests"></a>
## 요청 보내기 (Making Requests)

요청을 보내기 위해 `Http` 파사드가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL에 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이 인스턴스는 응답을 검사하는 데 사용할 수 있는 다양한 메서드를 제공합니다:

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있어, 응답의 JSON 데이터를 직접 배열 접근 방식으로 조회할 수 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```

위에 나열된 메서드 이외에도, 특정 상태 코드인지 확인할 수 있는 다음 메서드들을 사용할 수 있습니다:

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
#### URI 템플릿 (URI Templates)

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 사용하여 요청 URL을 구성할 수도 있습니다. URI 템플릿에 의해 확장될 수 있는 URL 매개변수를 정의하려면 `withUrlParameters` 메서드를 사용할 수 있습니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '11.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프하기 (Dumping Requests)

보내기 전의 요청 인스턴스를 덤프하고 스크립트 실행을 중단하고 싶다면, 요청 정의의 시작 부분에 `dd` 메서드를 추가하면 됩니다:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터 (Request Data)

일반적으로 `POST`, `PUT`, `PATCH` 요청에서는 추가 데이터를 함께 보내는 경우가 많아, 이 메서드들은 두 번째 인수로 배열 형태의 데이터를 받습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청 시에는 URL에 직접 쿼리 문자열을 붙이거나, `get` 메서드의 두 번째 인수로 키/값 배열을 전달할 수 있습니다:

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
#### Form URL Encoded 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내고 싶다면, 요청하기 전에 `asForm` 메서드를 호출해야 합니다:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### 원시 요청 본문 보내기

요청 시 원시 요청 본문을 직접 제공하려면 `withBody` 메서드를 사용할 수 있습니다. 콘텐츠 타입은 두 번째 인수로 지정합니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청 (Multi-Part Requests)

파일을 멀티파트 요청으로 보내려면, 요청 전에 `attach` 메서드를 호출하세요. 이 메서드는 파일 이름과 파일 내용을 받으며, 필요하면 세 번째 인수로 파일명, 네 번째 인수로 파일과 관련된 헤더 배열을 전달할 수 있습니다:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 원시 내용을 전달하는 대신, 스트림 리소스를 전달할 수도 있습니다:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더 (Headers)

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용합니다. 이 메서드는 키/값 배열을 인수로 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` 메서드를 사용하여 요청에 대해 애플리케이션이 기대하는 응답 콘텐츠 타입을 지정할 수 있습니다:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

더 간편하게 `acceptJson` 메서드를 사용하면, 애플리케이션이 `application/json` 콘텐츠 타입을 예상함을 빠르게 지정할 수 있습니다:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 요청 헤더와 새로운 헤더를 병합합니다. 모든 헤더를 완전히 교체하려면 `replaceHeaders` 메서드를 사용할 수 있습니다:

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

기본 및 다이제스트 인증 자격증명은 각각 `withBasicAuth`, `withDigestAuth` 메서드를 사용하여 지정할 수 있습니다:

```php
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### 베어러 토큰 (Bearer Tokens)

빠르게 요청 `Authorization` 헤더에 베어러 토큰을 추가하려면 `withToken` 메서드를 사용할 수 있습니다:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃 (Timeout)

`timeout` 메서드를 사용하여 최대 응답 대기 시간을 초 단위로 지정할 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 후에 타임아웃됩니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```

제한 시간을 초과하면 `Illuminate\Http\Client\ConnectionException` 인스턴스가 발생합니다.

서버에 연결 시도할 때 최대 대기 시간을 초 단위로 지정하려면 `connectTimeout` 메서드를 사용하세요:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도 (Retries)

클라이언트나 서버 오류 발생 시 HTTP 클라이언트가 자동으로 재시도하게 하려면 `retry` 메서드를 사용합니다. 이 메서드는 시도할 최대 횟수와 시도 간 대기할 밀리초를 인수로 받습니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

시도 간 대기 시간을 직접 계산하려면 두 번째 인수에 클로저를 전달할 수 있습니다:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

편의를 위해 `retry`의 첫 번째 인수로 밀리초 배열을 전달하여, 시도 간 대기 시간을 설정할 수도 있습니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면 세 번째 인수로 재시도를 실제로 수행할지를 결정하는 콜러블을 전달할 수 있습니다. 예를 들어, 재시도가 `ConnectionException` 발생 시에만 이루어지도록 할 수 있습니다:

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

재시도 전 요청을 변경하고 싶다면, `retry`에 전달한 콜러블에서 `$request` 객체를 수정하면 됩니다. 예: 첫 시도가 인증 오류였다면 새 토큰으로 재시도하기:

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

모든 시도가 실패하면 `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 이를 비활성화하려면 `throw` 인수에 `false`를 전달하세요. 비활성화할 경우, 모든 시도 후에 마지막 응답이 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 연결 문제로 모든 요청이 실패하면, `throw` 인수가 `false`여도 `Illuminate\Http\Client\ConnectionException`은 여전히 발생합니다.

<a name="error-handling"></a>
### 오류 처리 (Error Handling)

Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(서버의 `400`, `500` 응답) 시 예외를 발생시키지 않습니다. `successful`, `clientError`, `serverError` 메서드를 사용하여 이런 오류들을 확인할 수 있습니다:

```php
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 상태 코드가 400대인지 확인...
$response->clientError();

// 상태 코드가 500대인지 확인...
$response->serverError();

// 클라이언트나 서버 오류가 발생하면 즉시 지정한 콜백 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생시키기

응답 인스턴스가 있고, 상태 코드가 클라이언트 또는 서버 오류일 때 `Illuminate\Http\Client\RequestException`을 발생시키고 싶다면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트 또는 서버 오류 발생 시 예외 던지기...
$response->throw();

// 오류가 발생하고 주어진 조건이 참일 때 예외 던지기...
$response->throwIf($condition);

// 오류가 발생하고 주어진 클로저가 true를 반환할 때 예외 던지기...
$response->throwIf(fn (Response $response) => true);

// 오류가 발생하고 주어진 조건이 거짓일 때 예외 던지기...
$response->throwUnless($condition);

// 오류가 발생하고 주어진 클로저가 false를 반환할 때 예외 던지기...
$response->throwUnless(fn (Response $response) => false);

// 특정 상태 코드일 때 예외 던지기...
$response->throwIfStatus(403);

// 특정 상태 코드가 아닐 때 예외 던지기...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스는 `$response` 공개 속성을 가지고 있어 반환된 응답을 확인할 수 있습니다.

`throw` 메서드는 오류가 없으면 응답 인스턴스를 반환하므로, 메서드 체이닝으로 추가 작업을 할 수 있습니다:

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 던져지기 전 추가 로직을 수행하고 싶다면 `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저가 호출된 후 자동으로 예외가 던져집니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그 또는 리포트 시 120자로 잘립니다. 이 동작을 커스터마이징하거나 비활성화하려면 애플리케이션 예외 처리 설정(`bootstrap/app.php`)에서 `truncateRequestExceptionsAt` 및 `dontTruncateRequestExceptions` 메서드를 사용하세요:

```php
->withExceptions(function (Exceptions $exceptions) {
    // 요청 예외 메시지 길이 240자로 자르기...
    $exceptions->truncateRequestExceptionsAt(240);

    // 요청 예외 메시지 자르기 비활성화...
    $exceptions->dontTruncateRequestExceptions();
})
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어 (Guzzle Middleware)

Laravel HTTP 클라이언트는 Guzzle 기반이므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 아웃고잉 요청을 조작하거나 인커밍 응답을 검사할 수 있습니다. 아웃고잉 요청 조작을 위해 `withRequestMiddleware` 메서드에 미들웨어를 등록하세요:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 인커밍 HTTP 응답을 조사하려면 `withResponseMiddleware` 메서드를 사용합니다:

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
#### 글로벌 미들웨어 (Global Middleware)

때로는 모든 아웃고잉 요청과 인커밍 응답에 적용할 미들웨어가 필요할 수 있습니다. 이 경우 `globalRequestMiddleware` 및 `globalResponseMiddleware` 메서드를 사용하세요. 보통 애플리케이션의 `AppServiceProvider` 클래스 `boot` 메서드에서 호출합니다:

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

아웃고잉 요청에 추가 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정하려면 `withOptions` 메서드를 사용하세요. 이 메서드는 키/값 쌍 배열을 받습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 글로벌 옵션 (Global Options)

모든 아웃고잉 요청에 대한 기본 옵션을 설정하려면 `globalOptions` 메서드를 사용할 수 있습니다. 보통 이 메서드는 애플리케이션 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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

여러 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 여러 요청을 순차가 아니라 동시에 디스패치합니다. 느린 HTTP API와 통신할 때 성능 향상에 큰 도움이 됩니다.

`pool` 메서드를 사용하면 이 작업을 쉽게 할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 받는 클로저를 인수로 사용하여, 요청 풀에 요청을 추가하고 일괄 수행할 수 있게 합니다:

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

각 응답 인스턴스는 풀에 추가된 순서대로 접근할 수 있습니다. `as` 메서드로 요청에 이름을 붙이면, 이름으로 응답을 액세스할 수도 있습니다:

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

`pool` 메서드는 `withHeaders`, `middleware` 같은 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 헤더 또는 미들웨어를 풀 내 모든 요청에 적용하려면, 각 요청마다 직접 옵션을 설정해야 합니다:

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

Laravel HTTP 클라이언트를 사용하면 매크로를 정의하여, 애플리케이션 내에서 공통 요청 경로나 헤더 구성을 표현력 있게 구성할 수 있습니다. 매크로는 보통 애플리케이션 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드 내에서 정의합니다:

```php
use Illuminate\Support\Facades.Http;

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

매크로를 설정한 후, 애플리케이션 어디에서든 지정한 구성을 가진 보류 중인 요청(pending request)을 생성할 때 매크로를 호출할 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

Laravel 서비스 다수는 테스트를 쉽게 그리고 표현력 있게 작성할 수 있는 기능을 제공합니다. Laravel의 HTTP 클라이언트도 예외가 아닙니다. `Http` 파사드의 `fake` 메서드를 사용하면 요청 시 가짜 응답을 반환하도록 클라이언트를 설정할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜 처리 (Faking Responses)

예를 들어, 모든 요청에 빈 `200` 상태 응답을 반환하도록 클라이언트를 설정하려면 `fake` 메서드를 인수 없이 호출하면 됩니다:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 가짜 처리

또는 `fake` 메서드에 배열을 전달해 URL 패턴별로 가짜 응답을 설정할 수 있습니다. `*`는 와일드카드로 사용할 수 있습니다. 가짜 처리하지 않은 URL 요청은 실제로 수행됩니다. 이때 `Http` 파사드의 `response` 메서드로 가짜 응답을 구성할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 가짜 처리...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대한 문자열 응답 가짜 처리...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

모든 일치하지 않는 URL에 대해 기본 가짜 응답을 지정하려면 `'*'`를 사용하세요:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 가짜 처리...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 다른 모든 엔드포인트에 대한 문자열 응답 가짜 처리...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

간단한 문자열, JSON, 빈 응답은 문자열, 배열, 정수 전달로 쉽게 생성할 수 있습니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 연결 예외 가짜 처리

HTTP 클라이언트가 `Illuminate\Http\Client\ConnectionException`을 발생시킬 때 애플리케이션 동작을 테스트해야 할 때가 있습니다. `failedConnection` 메서드를 사용하면 연결 예외를 발생시키도록 클라이언트를 가짜 처리할 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 가짜 처리

특정 URL이 순서대로 여러 가짜 응답을 반환하도록 설정할 수도 있습니다. `Http::sequence` 메서드로 응답 시퀀스를 만듭니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 응답 시퀀스 가짜 처리...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

시퀀스의 모든 응답이 소진되면 더 이상 요청 받을 때 예외가 발생합니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용하세요:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 응답 시퀀스 가짜 처리...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴 지정 없이 응답 시퀀스만 가짜 처리하려면 `Http::fakeSequence` 메서드를 사용합니다:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 가짜 콜백

특정 엔드포인트에 대해 반환 응답을 결정하는 훨씬 복잡한 로직이 필요하면 클로저를 `fake` 메서드에 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받고, 반환할 응답 인스턴스를 반환해야 합니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="preventing-stray-requests"></a>
### 원치 않는 실제 요청 방지 (Preventing Stray Requests)

각 테스트에서 HTTP 클라이언트로 발생하는 모든 요청이 가짜 처리됐는지 보장하고 싶다면 `preventStrayRequests` 메서드를 호출하세요. 이 메서드를 호출한 뒤에는 가짜 응답이 없는 요청이 있으면 실제 요청 대신 예외가 발생합니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답이 반환됩니다...
Http::get('https://github.com/laravel/framework');

// 예외가 발생합니다...
Http::get('https://laravel.com');
```

<a name="inspecting-requests"></a>
### 요청 검사 (Inspecting Requests)

가짜 응답을 사용할 때, 클라이언트가 올바른 데이터나 헤더를 보내는지 검사하고 싶을 때가 있습니다. `Http::fake` 호출 이후에 `Http::assertSent` 메서드를 이용해 요청 검증이 가능합니다.

`assertSent` 메서드는 `Illuminate\Http\Client\Request` 인스턴스를 받은 클로저를 인수로 받고, 요청이 기대에 부합하면 `true`를 반환해야 합니다. 테스트가 통과하려면 하나 이상의 요청이 이 조건과 일치해야 합니다:

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

특정 요청이 보내지지 않았음을 단언하려면 `assertNotSent` 메서드를 사용합니다:

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

`assertSentCount` 메서드로 테스트 중에 몇 건의 요청이 "전송"됐는지도 확인할 수 있습니다:

```php
Http::fake();

Http::assertSentCount(5);
```

`assertNothingSent` 메서드는 테스트 중에 어떠한 요청도 보내지지 않았음을 단언합니다:

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청 / 응답 기록하기

`recorded` 메서드를 사용하면 모든 요청과 그 대응 응답을 수집할 수 있습니다. 이 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스 배열이 담긴 컬렉션을 반환합니다:

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

또한, `recorded` 메서드는 `Illuminate\Http\Client\Request` 및 `Illuminate\Http\Client\Response` 인스턴스를 받는 클로저를 인수로 받으며, 이를 통해 조건에 맞는 요청/응답 쌍만 필터링할 수 있습니다:

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

Laravel은 HTTP 요청을 보내는 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 보내지기 전에, `ResponseReceived` 이벤트는 응답이 수신된 후, `ConnectionFailed` 이벤트는 요청에 대해 응답을 받지 못했을 때 발생합니다.

`RequestSending` 및 `ConnectionFailed` 이벤트는 모두 공개 `$request` 속성을 가지고 있어 `Illuminate\Http\Client\Request` 인스턴스를 확인할 수 있습니다. `ResponseReceived` 이벤트는 `$request` 속성 외에 `$response` 속성도 가지고 있어, `Illuminate\Http\Client\Response` 인스턴스를 검사할 수 있습니다. 애플리케이션 내에서 이 이벤트들에 대한 [이벤트 리스너](/docs/master/events)를 생성할 수 있습니다:

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 이벤트 처리 메서드.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```