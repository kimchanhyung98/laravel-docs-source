# HTTP 클라이언트

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
    - [응답 페이킹](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [예기치 않은 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 기반으로 하는 간결하고 표현력 있는 API를 제공하여, 다른 웹 애플리케이션과 통신하기 위한 HTTP 요청을 쉽고 빠르게 보낼 수 있게 해줍니다. Laravel의 Guzzle 래퍼는 가장 흔하게 사용되는 케이스와 뛰어난 개발자 경험에 초점을 맞추고 있습니다.

<a name="making-requests"></a>
## 요청 보내기

`Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메소드를 사용하여 요청을 보낼 수 있습니다. 먼저, 기본적인 `GET` 요청이 어떻게 동작하는지 살펴봅시다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 다양한 메서드를 통해 응답을 검사할 수 있습니다:

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있어, JSON 응답 데이터를 배열처럼 바로 접근할 수 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```

위에서 언급한 응답 메서드 외에도, 다음과 같은 메서드로 응답의 상태 코드를 확인할 수 있습니다:

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

HTTP 클라이언트는 [URI 템플릿 사양](https://www.rfc-editor.org/rfc/rfc6570)에 따라 요청 URL을 쉽게 구성할 수 있도록 지원합니다. URI 템플릿에서 확장할 URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용할 수 있습니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '11.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 디버깅(dump)

요청이 발송되기 전에 해당 요청 인스턴스를 출력하고 스크립트 실행을 종료하고 싶다면, 요청 정의의 시작 부분에 `dd` 메서드를 추가하면 됩니다:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

일반적으로 `POST`, `PUT`, `PATCH` 요청을 보낼 때는 추가 데이터를 함께 전송합니다. 이때 해당 메서드의 두 번째 인자에 데이터 배열을 전달하면 됩니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청 시에는 URL에 직접 쿼리 문자열을 붙이거나, 두 번째 인자에 key/value 배열을 넘길 수 있습니다:

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
])->get('http://example.com/users')
```

<a name="sending-form-url-encoded-requests"></a>
#### Form URL 인코딩 요청 보내기

`application/x-www-form-urlencoded` 타입으로 데이터를 전송하려면, 요청 전에 `asForm` 메서드를 호출하세요:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 본문 전송

요청 시 raw 요청 본문을 직접 지정하려면 `withBody` 메서드를 사용할 수 있습니다. 콘텐츠 타입은 두 번째 인자로 지정할 수 있습니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트로 전송해야 한다면, 요청 전에 `attach` 메서드를 사용하세요. 이 메서드는 파일 이름과 파일 내용을 받으며, 필요에 따라 파일 이름(세 번째 인자)과 파일에 적용할 헤더(네 번째 인자)도 지정할 수 있습니다:

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
### 헤더

`withHeaders` 메서드를 사용해서 요청에 헤더를 추가할 수 있습니다. 이 메서드는 key/value 배열을 인자로 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

요청에 대한 응답으로 어떤 콘텐츠 타입을 기대하는지 지정하려면 `accept` 메서드를 사용할 수 있습니다:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

편의상, 응답으로 `application/json` 콘텐츠 타입을 기대한다면 `acceptJson` 메서드로 빠르게 지정할 수 있습니다:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders`는 기존 헤더에 새로운 헤더를 병합합니다. 모든 헤더를 완전히 교체하고 싶다면 `replaceHeaders` 메서드를 이용하세요:

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

기본 인증과 다이제스트 인증을 각각 `withBasicAuth`, `withDigestAuth` 메소드를 통해 지정할 수 있습니다:

```php
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

Bearer 토큰을 요청의 `Authorization` 헤더에 빠르게 추가하려면, `withToken` 메서드를 사용하세요:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드를 사용하면 응답을 기다릴 최대 시간(초 단위)을 지정할 수 있습니다. 기본적으로 HTTP 클라이언트의 타임아웃은 30초입니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버 연결 시도를 위해 대기하는 최대 시간은 `connectTimeout` 메서드로 지정할 수 있습니다. 기본값은 10초입니다:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트 혹은 서버 오류가 발생했을 때 요청을 자동으로 재시도하고 싶다면 `retry` 메서드를 사용할 수 있습니다. `retry` 메서드는 최대 시도 횟수와 재시도 간 대기 시간(밀리초)을 인자로 받습니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

재시도 간 대기 시간을 직접 계산하고 싶다면 두 번째 인자로 클로저를 전달할 수 있습니다:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

편의상, 첫 번째 인자로 배열을 전달해서 각 시도 간 대기 시간을 지정할 수 있습니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면, 세 번째 인자로 콜러블을 전달해 재시도 여부를 제어할 수 있습니다. 예를 들어, 최초 요청에서 `ConnectionException`이 발생한 경우에만 재시도하도록 할 수 있습니다:

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청이 실패하면, 새로운 시도를 하기 전에 요청을 수정하고 싶을 수 있습니다. 이런 경우에는 재시도 콜러블로 전달된 요청 인자를 수정하면 됩니다. 예를 들어, 첫 번째 시도에서 인증 오류가 발생하면 새로운 인증 토큰으로 재시도할 수 있습니다:

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

모든 재시도가 실패하면 `Illuminate\Http\Client\RequestException`이 발생합니다. 이 동작을 비활성화하려면 `throw` 인자에 `false` 값을 전달하세요. 비활성화된 경우, 모든 재시도를 마친 뒤 클라이언트가 받은 마지막 응답이 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패한 경우에는, `throw` 인자가 `false`로 설정되어 있어도 `Illuminate\Http\Client\ConnectionException`이 여전히 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, Laravel HTTP 클라이언트 래퍼는 클라이언트 또는 서버 에러(서버가 반환하는 400, 500번대 응답)에 대해 예외를 발생시키지 않습니다. 이러한 에러가 반환되었는지 확인하려면 `successful`, `clientError`, `serverError` 같은 메서드를 사용할 수 있습니다:

```php
// 200 이상 300 미만 상태 코드를 반환했는지 확인
$response->successful();

// 400 이상 상태 코드를 반환했는지 확인
$response->failed();

// 400번대 상태 코드인지 확인
$response->clientError();

// 500번대 상태 코드인지 확인
$response->serverError();

// 클라이언트/서버 에러 발생 시 콜백 즉시 실행
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생

응답 인스턴스가 있을 때, 응답 상태 코드가 클라이언트 또는 서버 에러임을 나타내면 `Illuminate\Http\Client\RequestException`을 던지고 싶다면 `throw` 또는 `throwIf` 메서드를 사용하세요:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트 또는 서버 에러 발생 시 예외 발생
$response->throw();

// 에러가 발생하고 특정 조건이 true일 때 예외 발생
$response->throwIf($condition);

// 에러 발생하고 클로저 결과가 true일 때 예외 발생
$response->throwIf(fn (Response $response) => true);

// 에러 발생하고 조건이 false일 때 예외 발생
$response->throwUnless($condition);

// 에러 발생하고 클로저 결과가 false일 때 예외 발생
$response->throwUnless(fn (Response $response) => false);

// 특정 상태 코드(403)이면 예외 발생
$response->throwIfStatus(403);

// 특정 상태 코드(200)가 아니면 예외 발생
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 확인할 수 있도록 public `$response` 프로퍼티가 있습니다.

`throw` 메서드는 에러가 없으면 원래 응답 인스턴스를 반환하므로, 연쇄적으로 다른 동작을 연결할 수 있습니다:

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전에 추가 로직을 수행하고 싶다면 클로저를 `throw` 메서드에 전달할 수 있습니다. 클로저가 호출된 후 예외가 자동으로 발생하므로, 클로저 내부에서 다시 예외를 던질 필요는 없습니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그 또는 리포트 시 120자로 잘려서 출력됩니다. 이 동작을 변경하거나 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `truncateRequestExceptionsAt`, `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions) {
    // 예외 메시지 240자로 잘라서 출력
    $exceptions->truncateRequestExceptionsAt(240);

    // 예외 메시지 자르기 비활성화
    $exceptions->dontTruncateRequestExceptions();
})
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel HTTP 클라이언트는 Guzzle을 기반으로 하므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 나가는 요청을 조작하거나 들어오는 응답을 검사할 수 있습니다. 나가는 요청을 조작하려면 `withRequestMiddleware` 메서드로 미들웨어를 등록하면 됩니다:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 들어오는 HTTP 응답을 검사하려면 `withResponseMiddleware` 메서드로 미들웨어를 등록하면 됩니다:

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

모든 나가는 요청과 들어오는 응답에 적용되는 글로벌 미들웨어를 등록하고 싶을 때가 있습니다. 이럴 때는 `globalRequestMiddleware`와 `globalResponseMiddleware`를 사용하면 됩니다. 일반적으로 이 메서드들은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 호출해야 합니다:

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

나가는 요청에 대해 [추가 Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정하려면 `withOptions` 메서드를 사용하세요. 이 메서드는 key/value 배열을 인자로 받습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 글로벌 옵션

모든 나가는 요청의 기본 옵션을 지정하려면 `globalOptions` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메소드를 통해 호출해야 합니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스 부트스트랩
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

때로는 여러 HTTP 요청을 동시에(순차적으로가 아닌) 전송하고 싶을 수 있습니다. 즉, 여러 요청을 동시에 발송하여 HTTP API와의 느린 통신을 상당히 빠르게 할 수 있습니다.

이를 위해 `pool` 메서드를 사용할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 받아, 해당 풀에 쉽게 여러 요청을 추가할 수 있게 합니다:

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

위 예시에서, 각 응답 인스턴스는 풀에 추가된 순서대로 접근할 수 있습니다. 요청에 이름을 붙이고 싶다면, `as` 메서드를 사용하여 각 응답을 이름으로 접근할 수도 있습니다:

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

`pool` 메서드는 `withHeaders`나 `middleware` 등의 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 만약 풀에 포함된 각 요청에 개별적으로 커스텀 헤더나 미들웨어를 적용하고 싶다면, 풀 안의 각 요청에 직접 옵션을 지정해 주세요:

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
## 매크로

Laravel HTTP 클라이언트에서는 "매크로"를 정의할 수 있으며, 이를 통해 여러 서비스와 상호작용할 때 공통 요청 경로나 헤더 구성을 간결하고 표현적으로 재사용할 수 있습니다. 시작하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에서 매크로를 정의하세요:

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

매크로를 구성했다면, 이제 애플리케이션 내 어디에서나 호출해서 지정된 구성으로 Pending Request를 만들 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

Laravel의 많은 서비스는 테스트를 쉽고 직관적으로 작성할 수 있는 기능을 제공합니다. HTTP 클라이언트 역시 예외가 아닙니다. `Http` 파사드의 `fake` 메서드를 사용하면, 요청 시 더미/가짜 응답을 반환하도록 클라이언트를 설정할 수 있습니다.

<a name="faking-responses"></a>
### 응답 페이킹

모든 요청에 대해 빈 200 응답을 반환하려면, 인자 없이 `fake` 메서드를 호출하세요:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 페이킹

또는 `fake` 메서드에 배열을 전달해 페이크할 URL 패턴별 응답을 지정할 수 있습니다. `*` 문자는 와일드카드로 사용할 수 있습니다. 지정되지 않은 URL 요청은 실제로 수행됩니다. 해당 엔드포인트에 대한 가짜 응답을 만들 때는 `Http` 파사드의 `response` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 페이크...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대한 문자열 응답 페이크...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

모든 매치되지 않은 URL까지 페이크하려면, 단일 `*` 패턴을 써서 기본값을 지정할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 페이크...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트에 문자열 응답 페이크...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

편하게, 응답에 문자열, 배열, 정수(상태 코드)를 직접 지정해도 간단히 응답이 생성됩니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 페이킹

HTTP 클라이언트가 요청 시 `Illuminate\Http\Client\ConnectionException`을 마주한 상황을 테스트하고 싶을 때는, `failedConnection` 메서드를 사용하면 됩니다:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException` 발생 상황을 테스트하려면, `failedRequest` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 페이킹

특정 URL이 여러 번 호출될 때, 차례로 여러 페이크 응답을 반환하게 하려면, `Http::sequence` 메서드를 사용합니다:

```php
Http::fake([
    // GitHub 엔드포인트에 응답 시퀀스 페이크...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

응답 시퀀스가 다 소비되면 남은 요청은 예외가 발생합니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하려면, `whenEmpty` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 응답 시퀀스 페이크...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴과 관계 없이 응답 시퀀스를 페이크하고 싶다면, `Http::fakeSequence` 메서드를 사용할 수 있습니다:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 페이크 콜백

엔드포인트별 응답 논리가 더 복잡해야 한다면, 클로저를 `fake` 메서드에 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받아 응답 인스턴스를 반환해야 합니다. 클로저 안에서 필요한 만큼 로직을 구현할 수 있습니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="preventing-stray-requests"></a>
### 예기치 않은 요청 방지

테스트 중 HTTP 클라이언트를 통한 모든 요청이 반드시 페이크되어야 한다면, `preventStrayRequests` 메서드를 호출하세요. 이때 페이크가 없는 실제 요청이 발생하면 예외가 발생하며, 실제 HTTP 요청이 이뤄지지 않습니다:

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

<a name="inspecting-requests"></a>
### 요청 검사

응답을 페이크할 때, 클라이언트가 받은 요청을 검사하여 애플리케이션이 올바른 데이터나 헤더를 보내는지 확인해야 할 때가 종종 있습니다. 이런 검증은 `Http::fake` 호출 후 `Http::assertSent` 메서드를 통해 할 수 있습니다.

`assertSent` 메서드는 `Illuminate\Http\Client\Request` 인스턴스를 받아 조건을 판단하는 클로저를 받습니다. 하나 이상의 요청이 조건에 맞으면 테스트가 통과합니다:

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

특정 요청이 전송되지 않았는지 확인하려면 `assertNotSent` 메서드를 사용하세요:

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

보내진 요청 수가 몇 개인지 단언하려면 `assertSentCount`를 사용할 수 있습니다:

```php
Http::fake();

Http::assertSentCount(5);
```

또는, 테스트 중에 아무 요청도 보내지지 않았음을 검증하려면 `assertNothingSent`를 사용할 수 있습니다:

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용해 모든 요청 및 해당 응답을 수집할 수 있습니다. 이 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response`가 쌍으로 들어있는 배열 컬렉션을 반환합니다:

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

추가적으로, `recorded` 메서드는 클로저를 받아 해당 조건에 맞는 요청/응답 쌍만 필터링해서 반환할 수도 있습니다:

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
## 이벤트

Laravel은 HTTP 요청을 보내는 과정에서 세 개의 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 발송되기 직전에 발생하고, `ResponseReceived` 이벤트는 해당 요청의 응답을 받은 후 발생합니다. 만약 요청에 대한 응답을 받지 못하면 `ConnectionFailed` 이벤트가 발생합니다.

`RequestSending` 및 `ConnectionFailed` 이벤트에는 `Illuminate\Http\Client\Request` 인스턴스를 검사할 수 있는 public `$request` 프로퍼티가 있습니다. 마찬가지로 `ResponseReceived` 이벤트에는 `$request`와 `$response` 프로퍼티가 있어 `Illuminate\Http\Client\Response` 인스턴스를 확인할 수 있습니다. 이러한 이벤트에 대한 [이벤트 리스너](/docs/{{version}}/events)를 애플리케이션 내에 정의할 수 있습니다:

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 지정된 이벤트를 처리합니다.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```