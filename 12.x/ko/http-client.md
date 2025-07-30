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
    - [예기치 않은 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 쉽게 사용할 수 있도록 표현력 높고 간결한 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 빠르게 HTTP 요청을 통해 통신할 수 있습니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례에 초점을 맞추고 있어 뛰어난 개발자 경험을 제공합니다.

<a name="making-requests"></a>
## 요청 보내기 (Making Requests)

요청을 보내려면 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL에 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이 객체를 통해 다양한 메서드로 응답을 검사할 수 있습니다:

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

또한 `Illuminate\Http\Client\Response` 객체는 PHP `ArrayAccess` 인터페이스를 구현해서 JSON 응답 데이터를 응답 객체에서 직접 접근할 수 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```

위에 나열된 응답 메서드 외에도, 특정 상태 코드를 판별하기 위한 메서드들도 있습니다:

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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 사용해 요청 URL을 구성할 수도 있습니다. URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용하세요:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 내용 덤프

전송 전에 요청 인스턴스를 덤프하고 스크립트 실행을 종료하고 싶다면, 요청 정의 시작 부분에 `dd` 메서드를 추가하세요:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터 (Request Data)

`POST`, `PUT`, `PATCH` 요청에는 추가 데이터를 포함하는 경우가 많으며 이들 메서드는 두 번째 인수로 데이터 배열을 받습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청 시 URL에 직접 쿼리 문자열을 붙이거나 `get` 메서드의 두 번째 인수로 키/값 배열을 전달할 수 있습니다:

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

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내려면 요청 전에 `asForm` 메서드를 호출하세요:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### 원시 요청 본문 보내기

원시 요청 본문을 제공하려면 `withBody` 메서드를 사용할 수 있습니다. 두 번째 인수로 콘텐츠 타입도 지정할 수 있습니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트로 전송하려면, 요청 전에 `attach` 메서드를 호출하세요. 첫 번째 인수는 파일 이름, 두 번째는 파일 내용입니다. 세 번째 인수로는 파일 이름(별칭), 네 번째 인수로는 파일 관련 헤더를 전달할 수 있습니다:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 원시 내용을 전달하는 대신 스트림 리소스를 넘길 수도 있습니다:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더 (Headers)

`withHeaders` 메서드를 통해 요청에 헤더를 추가할 수 있습니다. 이 메서드는 키/값 배열을 인수로 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` 메서드를 사용하면 요청에 대한 응답으로 기대하는 콘텐츠 타입을 지정할 수 있습니다:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

간편하게 `application/json` 콘텐츠 타입을 지정하려면 `acceptJson` 메서드를 사용하세요:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 새로운 헤더를 기존 헤더에 병합합니다. 모든 헤더를 새로 교체하려면 `replaceHeaders` 메서드를 사용하세요:

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

기본 인증과 다이제스트 인증 자격 증명은 각각 `withBasicAuth`와 `withDigestAuth` 메서드를 사용해 지정할 수 있습니다:

```php
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### 베어러 토큰

요청의 `Authorization` 헤더에 베어러 토큰을 빠르게 추가하려면 `withToken` 메서드를 사용하세요:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃 (Timeout)

`timeout` 메서드는 응답을 기다릴 최대 시간(초 단위)을 지정합니다. 기본값은 30초입니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```

타임아웃이 초과되면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버 연결 시도 최대 시간을 지정하려면 `connectTimeout` 메서드를 사용하세요. 기본값은 10초입니다:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도 (Retries)

클라이언트 또는 서버 오류 시 자동으로 요청을 재시도하려면 `retry` 메서드를 사용하세요. `retry`는 최대 시도 횟수와 재시도 사이 대기 시간(ms)을 인수로 받습니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

재시도 사이 대기 시간을 직접 계산하려면, 두 번째 인수로 클로저를 전달할 수 있습니다:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

재시도 간 대기 시간을 배열로 지정하는 것도 가능합니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

만약 재시도를 할지 여부를 판단하는 콜백을 세 번째 인수로 전달하고 싶다면 다음과 같이 할 수 있습니다 (예: 연결 예외 시만 재시도):

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

재시도 시 요청을 변경하고 싶다면, 콜백 내에서 요청 인스턴스를 수정할 수 있습니다. 예를 들어, 첫 시도에서 인증 오류가 발생하면 새로운 토큰으로 재시도할 경우:

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 인스턴스가 던져집니다. 이 동작을 비활성화하려면 `throw` 인수에 `false`를 전달하세요. 비활성화하면 모든 재시도가 끝난 후 마지막 응답이 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패했다면, `throw` 인수를 `false`로 설정해도 `Illuminate\Http\Client\ConnectionException` 예외가 여전히 발생합니다.

<a name="error-handling"></a>
### 에러 처리 (Error Handling)

Guzzle 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트 및 서버 오류(`400`, `500`대 응답) 시 예외를 던지지 않습니다. 다음 메서드로 이런 오류 여부를 확인할 수 있습니다:

```php
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 400번대 상태 코드인지 확인...
$response->clientError();

// 500번대 상태 코드인지 확인...
$response->serverError();

// 클라이언트 또는 서버 오류가 있을 때 콜백 즉시 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 던지기

응답 인스턴스가 있고, 클라이언트 또는 서버 오류 시 `Illuminate\Http\Client\RequestException`을 던지고 싶으면 `throw` 또는 `throwIf` 메서드를 사용하세요:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 오류가 발생하면 예외 던지기...
$response->throw();

// 오류 발생 및 조건이 true면 예외 던지기...
$response->throwIf($condition);

// 오류 발생 및 클로저가 true 반환 시 예외 던지기...
$response->throwIf(fn (Response $response) => true);

// 오류 발생 및 조건이 false면 예외 던지기...
$response->throwUnless($condition);

// 오류 발생 및 클로저가 false 반환 시 예외 던지기...
$response->throwUnless(fn (Response $response) => false);

// 특정 상태 코드인 경우 예외 던지기...
$response->throwIfStatus(403);

// 특정 상태 코드가 아닌 경우 예외 던지기...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`RequestException` 인스턴스는 공개 `$response` 속성을 가지고 있어 반환된 응답을 살펴볼 수 있습니다.

`throw` 메서드는 오류가 없을 시 응답 인스턴스를 반환해 체이닝을 지원합니다:

```php
return Http::post(/* ... */)->throw()->json();
```

예외 던지기 전에 추가 작업을 하려면 `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저 실행 후 자동으로 예외가 던져집니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그 또는 리포트 시 120자로 잘립니다. 이 동작은 `bootstrap/app.php` 핸들러 설정에서 `truncateRequestExceptionsAt` 및 `dontTruncateRequestExceptions` 메서드로 조절할 수 있습니다:

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions) {
    // 요청 예외 메시지를 240자로 자르기...
    $exceptions->truncateRequestExceptionsAt(240);

    // 메시지 잘림 비활성화...
    $exceptions->dontTruncateRequestExceptions();
})
```

개별 요청마다 잘림 길이를 설정하려면 `truncateExceptionsAt` 메서드를 사용하세요:

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel HTTP 클라이언트는 Guzzle 기반이므로 [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 이용해 요청 전송 과정이나 응답 수신 후를 조작할 수 있습니다. 요청을 조작하려면 `withRequestMiddleware` 메서드로 미들웨어를 등록하세요:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

응답을 검사하려면 `withResponseMiddleware` 메서드로 미들웨어를 등록합니다:

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

모든 요청과 응답에 공통으로 적용할 미들웨어가 필요하다면, `globalRequestMiddleware` 와 `globalResponseMiddleware` 메서드를 사용하세요. 보통 애플리케이션 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 `withOptions` 메서드로 전달할 수 있습니다. 이는 키/값 배열을 인수로 받습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 글로벌 옵션

모든 요청에 공통 적용할 옵션은 `globalOptions` 메서드를 사용해 설정하세요. 보통 애플리케이션 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스 초기화
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

때로는 여러 HTTP 요청을 동시에 보내는 게 필요할 수 있습니다. 순차적으로 요청하는 대신 여러 요청을 동시에 전송하면 느린 HTTP API와 상호작용 시 성능이 크게 향상됩니다.

`pool` 메서드를 사용하면 이를 쉽게 구현할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 전달받는 클로저를 인수로 받아 요청 풀에 요청을 추가할 수 있도록 합니다:

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

응답 인스턴스는 요청을 추가한 순서대로 배열에 저장됩니다. `as` 메서드로 요청에 이름을 붙여, 이름으로 응답에 접근할 수도 있습니다:

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

`pool` 메서드는 `withHeaders`, `middleware` 같은 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 커스텀 헤더나 미들웨어를 적용하려면 풀 내 각 요청에서 직접 설정하세요:

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

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있어, 애플리케이션 전반의 서비스와 상호작용 시 공통 요청 경로나 헤더를 손쉽게 구성할 수 있습니다. 매크로는 보통 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 정의합니다:

```php
use Illuminate\Support\Facades.Http;

/**
 * 애플리케이션 서비스 초기화
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

매크로 설정 후에는 애플리케이션 어디서든 호출해 지정된 설정으로 대기 요청을 생성할 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

많은 Laravel 서비스는 테스트 코드를 쉽게 작성할 수 있도록 도와주며, HTTP 클라이언트도 마찬가지입니다. `Http` 파사드의 `fake` 메서드는 요청이 이루어질 때 가짜 응답을 반환하도록 HTTP 클라이언트를 조작할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜 처리 (Faking Responses)

예를 들어, 모든 요청에 대해 빈 200 상태 코드 응답을 반환하려면 `fake` 메서드를 인수 없이 호출하세요:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 가짜 처리

`fake`에 배열을 전달하면, 키는 가짜 처리할 URL 패턴, 값은 해당 응답이 됩니다. `*` 와일드카드를 사용할 수 있고, `Http::response`로 가짜 응답을 생성할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 JSON 응답...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 문자열 응답...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

가짜 처리하지 않은 URL 요청은 실제로 전송됩니다. 모든 매칭되지 않은 URL을 가짜 처리하려면 `*`를 키로 사용하세요:

```php
Http::fake([
    // GitHub 엔드포인트에 JSON 응답...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트에 문자열 응답...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

간단한 문자열, JSON, 빈 응답도 문자열, 배열, 숫자를 값으로 제공해 생성할 수 있습니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 가짜 처리

`Illuminate\Http\Client\ConnectionException` 예외 발생 상황을 테스트하려면 `failedConnection` 메서드를 사용하세요:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException` 예외를 발생시키려면 `failedRequest` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 가짜 처리

하나의 URL이 특정 순서로 여러 응답을 반환하도록 하려면 `Http::sequence` 메서드를 사용합니다:

```php
Http::fake([
    // GitHub 엔드포인트에 연속된 응답 시퀀스...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

시퀀스의 모든 응답을 다 사용하면 추가 요청 시 예외가 발생합니다. 빈 시퀀스 시 기본 반환할 응답은 `whenEmpty` 메서드로 지정할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 연속된 응답 시퀀스...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴 없이 시퀀스를 가짜 처리하려면 `Http::fakeSequence` 메서드를 사용하세요:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 가짜 콜백

응답 로직을 복잡하게 하려면, `fake` 메서드에 클로저를 전달하세요. 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받아야 하며 응답 인스턴스를 반환해야 합니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사 (Inspecting Requests)

가짜 응답 설정 후, 요청이 올바른 데이터 또는 헤더를 포함하는지 검사하려면 `Http::assertSent` 메서드를 사용하세요. 이 메서드는 `Illuminate\Http\Client\Request`를 받는 클로저를 인수로 받고, 검사 조건에 맞는 요청이 최소 하나 있어야 테스트가 통과합니다:

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

반대로 특정 요청이 보내지지 않았음을 검사하려면 `assertNotSent`를 사용하세요:

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

테스트 중 총 요청 횟수를 검사하려면 `assertSentCount`를, 요청이 전혀 없었음을 검사하려면 `assertNothingSent`를 사용하세요:

```php
Http::fake();

Http::assertSentCount(5);
```

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청 / 응답 기록

`recorded` 메서드로 요청 및 그 응답의 컬렉션을 받아올 수 있습니다. 각 요소는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스 배열입니다:

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

또한, 필터링할 클로저를 인수로 전달할 수 있습니다. 클로저는 요청과 응답을 받아 조건에 맞는 요청/응답만 반환합니다:

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
### 예기치 않은 요청 방지 (Preventing Stray Requests)

테스트 도중 HTTP 클라이언트가 모든 요청을 가짜 처리해야 한다면 `preventStrayRequests` 메서드를 호출하세요. 이 후 가짜 응답이 없는 실제 요청은 예외를 발생시킵니다:

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

<a name="events"></a>
## 이벤트 (Events)

Laravel은 HTTP 요청 전송 과정에서 세 가지 이벤트를 발행합니다. `RequestSending` 이벤트는 요청 전송 직전에, `ResponseReceived` 이벤트는 응답 수신 후, `ConnectionFailed` 이벤트는 응답을 받지 못했을 때 발생합니다.

`RequestSending`과 `ConnectionFailed` 이벤트는 공통으로 `$request` 공개 속성이 있어 `Illuminate\Http\Client\Request` 인스턴스를 조회할 수 있습니다. `ResponseReceived` 이벤트는 `$request`와 `$response` 속성을 가지고 있습니다. 애플리케이션 내에서 이 이벤트들에 대한 [이벤트 리스너](/docs/12.x/events)를 생성할 수 있습니다:

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