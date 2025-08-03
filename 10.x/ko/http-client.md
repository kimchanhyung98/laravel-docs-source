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
    - [요청 검증](#inspecting-requests)
    - [불필요한 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 감싸는 간결하고 표현력 있는 API를 제공하여, 다른 웹 애플리케이션과 빠르게 HTTP 요청을 주고받을 수 있도록 지원합니다. Laravel의 Guzzle 래퍼는 가장 흔한 사용 사례와 훌륭한 개발자 경험에 중점을 두고 있습니다.

시작하기 전에, 애플리케이션의 의존성으로 Guzzle 패키지가 설치되어 있는지 확인해야 합니다. Laravel은 기본적으로 이 패키지를 자동 포함하지만, 이전에 제거했다면 Composer를 통해 다시 설치할 수 있습니다:

```shell
composer require guzzlehttp/guzzle
```

<a name="making-requests"></a>
## 요청 보내기 (Making Requests)

요청을 보내기 위해 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 기본적인 `GET` 요청을 다른 URL로 보내는 방법을 살펴보겠습니다:

```
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이 인스턴스를 통해 다양한 응답을 검사하는 메서드를 사용할 수 있습니다:

```
$response->body() : string;
$response->json($key = null, $default = null) : array|mixed;
$response->object() : object;
$response->collect($key = null) : Illuminate\Support\Collection;
$response->status() : int;
$response->successful() : bool;
$response->redirect(): bool;
$response->failed() : bool;
$response->clientError() : bool;
$response->header($header) : string;
$response->headers() : array;
```

또한, `Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스를 구현하여, JSON 응답 데이터를 응답에서 직접 액세스할 수 있습니다:

```
return Http::get('http://example.com/users/1')['name'];
```

위에서 나온 메서드 외에도, 응답이 특정 상태 코드를 갖는지를 확인하는 다양한 메서드도 제공합니다:

```
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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 사용해 요청 URL을 구성할 수 있습니다. 템플릿에서 확장될 URL 파라미터를 지정하려면 `withUrlParameters` 메서드를 사용하면 됩니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '9.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프하기

보내는 요청 인스턴스를 덤프하고 스크립트 실행을 종료하려면, 요청 정의의 맨 앞에 `dd` 메서드를 추가하세요:

```
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터 (Request Data)

`POST`, `PUT`, `PATCH` 요청을 보낼 때 추가 데이터를 함께 보내는 일이 흔하므로, 이 메서드들은 두 번째 인수로 데이터 배열을 받습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```
use Illuminate\Support\Facades.Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청 시, URL에 쿼리 문자열을 직접 붙이거나, 두 번째 인수로 키-값 배열을 전달할 수 있습니다:

```
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는 `withQueryParameters` 메서드를 사용할 수도 있습니다:

```
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users')
```

<a name="sending-form-url-encoded-requests"></a>
#### application/x-www-form-urlencoded 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내려면, 요청 전에 `asForm` 메서드를 호출해야 합니다:

```
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### 원시 요청 본문 보내기

원시 요청 본문(raw request body)을 제공하려면 `withBody` 메서드를 사용할 수 있으며, 두 번째 인수로 콘텐츠 타입을 지정할 수 있습니다:

```
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청 (Multi-Part Requests)

파일을 멀티파트 요청으로 보내려면, 요청 전에 `attach` 메서드를 호출하세요. 이 메서드는 파일 이름과 내용물을 받으며, 필요하다면 세 번째 인수로 파일명, 네 번째 인수로 파일 관련 헤더를 제공할 수 있습니다:

```
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

원시 파일 내용을 넘기는 대신 스트림 리소스를 전달할 수도 있습니다:

```
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더 (Headers)

헤더는 `withHeaders` 메서드를 통해 요청에 추가할 수 있으며, 이 메서드는 키-값 쌍의 배열을 받습니다:

```
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

요청에 대한 응답에서 기대하는 콘텐츠 타입을 지정하려면 `accept` 메서드를 사용할 수 있습니다:

```
$response = Http::accept('application/json')->get('http://example.com/users');
```

편리하게도 `acceptJson` 메서드는 `application/json` 콘텐츠 타입을 간단히 지정하는 역할을 합니다:

```
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 헤더에 새 헤더를 병합합니다. 만약 헤더를 완전히 교체하고 싶다면 `replaceHeaders` 메서드를 사용하세요:

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

기본 및 다이제스트 인증은 각각 `withBasicAuth`와 `withDigestAuth` 메서드로 지정할 수 있습니다:

```
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

요청의 `Authorization` 헤더에 빠르게 Bearer 토큰을 추가하려면 `withToken` 메서드를 사용하세요:

```
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃 (Timeout)

`timeout` 메서드는 응답을 기다리는 최대 시간을 초 단위로 지정합니다. 기본 타임아웃은 30초입니다:

```
$response = Http::timeout(3)->get(/* ... */);
```

타임아웃 초과 시 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버에 연결을 시도하는 최대 대기 시간을 설정하려면 `connectTimeout` 메서드를 사용하세요:

```
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도 (Retries)

클라이언트 또는 서버 오류 발생 시 자동으로 요청을 재시도하려면 `retry` 메서드를 사용하세요. 첫 번째 인수는 최대 재시도 횟수, 두 번째 인수는 재시도 간 대기 시간(밀리초)입니다:

```
$response = Http::retry(3, 100)->post(/* ... */);
```

밀리초 단위 대기 시간을 직접 계산하고 싶다면, 두 번째 인수에 클로저를 전달할 수 있습니다:

```
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

편의를 위해, 첫 번째 인수로 밀리초 배열을 전달해 각 재시도 간 대기 시간을 지정할 수도 있습니다:

```
$response = Http::retry([100, 200])->post(/* ... */);
```

세 번째 인수로는 재시도 여부를 결정하는 콜러블을 전달할 수 있습니다. 예를 들어, 연결 예외가 발생할 때만 재시도하도록 설정할 수 있습니다:

```
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

재시도되기 전 요청을 변경해야 할 경우, `retry` 메서드에 전달되는 콜러블의 두 번째 인자인 요청 객체를 수정할 수 있습니다. 예를 들어, 인증 오류 발생 시 토큰을 새로 발급해 재시도하는 경우:

```
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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException`이 던져집니다. 이 동작을 비활성화하려면 `throw` 인수를 `false`로 지정하세요. 비활성화하면 모든 재시도를 수행한 후 마지막 응답이 반환됩니다:

```
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]  
> 모든 요청이 연결 문제로 실패하면, `throw` 인수가 `false`여도 `Illuminate\Http\Client\ConnectionException` 예외는 여전히 던져집니다.

<a name="error-handling"></a>
### 오류 처리 (Error Handling)

Guzzle 기본 동작과 달리, Laravel HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(`400` 또는 `500`대 응답)에서 예외를 자동으로 던지지 않습니다. 대신, 다음 메서드로 해당 오류 여부를 확인할 수 있습니다:

```
// 상태 코드가 200 이상 300 미만인지 판단...
$response->successful();

// 상태 코드가 400 이상인지 판단...
$response->failed();

// 상태 코드가 400대 오류인지 판단...
$response->clientError();

// 상태 코드가 500대 오류인지 판단...
$response->serverError();

// 클라이언트 또는 서버 오류가 있을 때 즉시 콜백 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 던지기 (Throwing Exceptions)

응답 인스턴스가 있을 때, 클라이언트 또는 서버 오류 상태면 `Illuminate\Http\Client\RequestException` 예외를 던지도록 하려면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

```
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트/서버 오류 시 예외 발생
$response->throw();

// 오류 발생 및 조건이 참일 때 예외 발생
$response->throwIf($condition);

// 오류 발생 및 클로저가 true 반환 시 예외 발생
$response->throwIf(fn (Response $response) => true);

// 오류 발생 및 조건이 false일 때 예외 발생
$response->throwUnless($condition);

// 오류 발생 및 클로저가 false 반환 시 예외 발생
$response->throwUnless(fn (Response $response) => false);

// 특정 상태 코드가 있으면 예외 발생
$response->throwIfStatus(403);

// 특정 상태 코드가 없으면 예외 발생
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스는 공개 `$response` 속성이 있어 반환된 응답을 검사할 수 있습니다.

`throw` 메서드는 오류가 없으면 응답 인스턴스를 반환하므로 체이닝에 활용할 수 있습니다:

```
return Http::post(/* ... */)->throw()->json();
```

예외를 던지기 전에 추가 작업을 수행하려면 클로저를 `throw`에 전달할 수 있습니다. 클로저가 호출된 후 예외가 자동으로 던져지므로, 클로저 내에서 재던질 필요는 없습니다:

```
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // 추가 작업...
})->json();
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어 (Guzzle Middleware)

Laravel HTTP 클라이언트는 Guzzle 기반이므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 요청을 조작하거나 응답을 검사할 수 있습니다. 요청을 조작하려면 `withRequestMiddleware` 메서드로 미들웨어를 등록하세요:

```
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

응답을 검사하려면 `withResponseMiddleware` 메서드를 사용하세요:

```
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
#### 전역 미들웨어 (Global Middleware)

모든 요청과 응답에 공통으로 미들웨어를 적용하려면, `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용하세요. 보통 애플리케이션의 `AppServiceProvider` `boot` 메서드에서 호출합니다:

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

`withOptions` 메서드를 사용해 추가 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정할 수 있습니다. 배열로 키-값 쌍을 전달합니다:

```
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="concurrent-requests"></a>
## 동시 요청 (Concurrent Requests)

가끔 여러 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 요청들을 순서대로 보내는 대신 한꺼번에 발송하여 느린 API 호출 시 성능을 크게 개선할 수 있습니다.

이를 위해 `pool` 메서드를 사용할 수 있습니다. `pool`은 클로저를 받으며, 클로저의 인수로 `Illuminate\Http\Client\Pool` 인스턴스를 전달받아 요청 풀에 요청을 쉽게 추가할 수 있습니다:

```
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

각 응답은 풀에 추가한 순서대로 배열에서 접근할 수 있습니다. 필요하면 `as` 메서드로 요청 이름을 지정해 이름으로 응답에 접근할 수도 있습니다:

```
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
#### 동시 요청 사용자 지정

`pool` 메서드는 `withHeaders`, `middleware` 같은 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀 내 각 요청에 개별적으로 헤더나 미들웨어를 설정해야 합니다:

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

Laravel HTTP 클라이언트는 매크로를 정의할 수 있어, 애플리케이션 전반에서 공통 요청 경로나 헤더 구성을 간결하게 재사용할 수 있습니다. 매크로는 보통 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의합니다:

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

매크로가 정의된 후, 애플리케이션 어디서든 호출해 지정한 구성을 가진 대기 요청을 만들 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

Laravel의 많은 서비스가 그렇듯, HTTP 클라이언트도 쉽고 표현력 있는 테스트 작성을 지원합니다. `Http` 파사드의 `fake` 메서드를 사용해 요청 시 가짜 응답을 반환하도록 지정할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜 처리 (Faking Responses)

예를 들어, 모든 요청에 대해 빈 `200` 상태 코드 응답을 반환하려면 인수 없이 `fake`를 호출하세요:

```
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 가짜 처리

`fake`에 배열을 전달하면, 키는 가짜 처리를 원하는 URL 패턴, 값은 해당 응답을 지정합니다. 와일드카드 `*`를 사용할 수 있으며, 가짜 처리하지 않은 URL 요청은 실제 실행됩니다. `Http::response` 메서드로 가짜 응답을 쉽게 생성할 수 있습니다:

```
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 스텁
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대한 문자열 응답 스텁
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

모든 일치하지 않는 URL에 대한 기본 가짜 응답을 지정하려면 단일 `*` 키를 사용할 수 있습니다:

```
Http::fake([
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 가짜 처리

한 URL에 대해 순서대로 여러 가짜 응답을 지정하려면 `Http::sequence` 메서드로 응답 시퀀스를 만들 수 있습니다:

```
Http::fake([
    'github.com/*' => Http::sequence()
                            ->push('Hello World', 200)
                            ->push(['foo' => 'bar'], 200)
                            ->pushStatus(404),
]);
```

시퀀스 내 모든 응답이 소진되면 추가 요청 시 예외가 발생합니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용하세요:

```
Http::fake([
    'github.com/*' => Http::sequence()
                            ->push('Hello World', 200)
                            ->push(['foo' => 'bar'], 200)
                            ->whenEmpty(Http::response()),
]);
```

시퀀스 지정 시 특정 URL 패턴이 꼭 필요하지 않다면 `Http::fakeSequence`를 사용할 수도 있습니다:

```
Http::fakeSequence()
        ->push('Hello World', 200)
        ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 가짜 콜백

특정 엔드포인트에 어떤 응답을 반환할지 복잡한 로직이 필요한 경우, `fake` 메서드에 클로저를 넘길 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 객체와 옵션 배열을 받아 적절한 응답을 반환해야 합니다:

```
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request, array $options) {
    return Http::response('Hello World', 200);
});
```

<a name="preventing-stray-requests"></a>
### 불필요한 요청 방지 (Preventing Stray Requests)

개별 테스트 혹은 전체 테스트 스위트에서 HTTP 클라이언트를 통한 모든 요청이 가짜인지를 보장하려면 `preventStrayRequests` 메서드를 사용하세요. 이 메서드 호출 후 대응하는 가짜 응답이 없는 요청은 실제 요청 대신 예외를 발생시킵니다:

```
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
### 요청 검증 (Inspecting Requests)

가짜 응답 중에 클라이언트가 올바른 데이터를 보내고 있는지 확인하고 싶다면, `Http::assertSent` 메서드를 사용할 수 있습니다. `assertSent`는 `Illuminate\Http\Client\Request` 객체를 인수로 받는 클로저를 인수로 받아, 클로저가 true를 반환하는 요청이 최소 하나 있어야 테스트가 통과합니다:

```
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades.Http;

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

필요하다면 특정 요청이 보내지지 않았음을 검증하는 `assertNotSent` 메서드도 있습니다:

```
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

`assertSentCount` 메서드로 테스트 동안 전송된 요청 개수를 검증할 수도 있습니다:

```
Http::fake();

Http::assertSentCount(5);
```

혹은 `assertNothingSent`로 요청이 전혀 없음을 검증할 수도 있습니다:

```
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용하면 모든 요청과 그에 대한 응답을 수집할 수 있습니다. 반환값은 `Illuminate\Http\Client\Request`와 `Response` 인스턴스를 포함하는 배열들의 컬렉션입니다:

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

또한, `recorded` 메서드는 요청과 응답을 인수로 받는 클로저를 받아, 원하는 조건에 따라 필터링할 수도 있습니다:

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

Laravel은 HTTP 요청 처리 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 전송되기 직전에, `ResponseReceived` 이벤트는 응답을 받았을 때, 그리고 `ConnectionFailed` 이벤트는 응답을 받지 못했을 때 발생합니다.

`RequestSending`과 `ConnectionFailed` 이벤트는 공통적으로 요청 객체(`Illuminate\Http\Client\Request`)를 검사할 수 있는 공개 `$request` 속성을 포함합니다. `ResponseReceived` 이벤트는 `$request`와 함께 응답 객체(`Illuminate\Http\Client\Response`)를 검사할 수 있는 `$response` 속성도 포함합니다.

이벤트 리스너들은 `App\Providers\EventServiceProvider` 서비스 프로바이더에 등록할 수 있습니다:

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Http\Client\Events\RequestSending' => [
        'App\Listeners\LogRequestSending',
    ],
    'Illuminate\Http\Client\Events\ResponseReceived' => [
        'App\Listeners\LogResponseReceived',
    ],
    'Illuminate\Http\Client\Events\ConnectionFailed' => [
        'App\Listeners\LogConnectionFailed',
    ],
];
```