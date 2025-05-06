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
    - [응답 페이크](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [잘못된 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 감싸는 표현적이고 최소한의 API를 제공하여, 다른 웹 애플리케이션과 통신하기 위한 HTTP 요청을 빠르게 보낼 수 있도록 도와줍니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례와 훌륭한 개발자 경험에 초점을 맞춥니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보내기 위해 `Http` 파사드가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL로 기본적인 `GET` 요청을 어떻게 보내는지 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 응답을 검사하는 다양한 메서드를 제공합니다:

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있어서, 응답의 JSON 데이터에 직접 접근할 수 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```

위에 나열된 응답 메서드 외에도, 다음의 메서드로 응답이 특정 상태 코드를 가졌는지 확인할 수 있습니다:

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

HTTP 클라이언트는 [URI 템플릿 사양](https://www.rfc-editor.org/rfc/rfc6570)을 사용하여 요청 URL을 구성할 수도 있습니다. URI 템플릿에서 확장될 URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용하세요.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '11.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프

전송 전 요청 인스턴스를 덤프하고 스크립트 실행을 종료하고 싶으면, 요청 정의 시작에 `dd` 메서드를 추가하세요:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

보통 `POST`, `PUT`, `PATCH` 요청에서는 추가 데이터를 함께 전송합니다. 이들 메서드는 두 번째 인자로 데이터 배열을 받으며, 기본적으로 `application/json` 콘텐츠 타입으로 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청 시 쿼리 스트링을 URL에 직접 추가하거나, 키/값 배열을 두 번째 인자로 `get` 메서드에 전달할 수 있습니다:

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
])->get('http://example.com/users')
```

<a name="sending-form-url-encoded-requests"></a>
#### Form URL Encoded 요청 전송

`application/x-www-form-urlencoded` 타입으로 데이터를 전송하려면, 요청 전에 `asForm` 메서드를 호출하세요:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 본문 전송

요청 시 raw 데이터를 본문으로 지정하려면 `withBody` 메서드를 사용할 수 있습니다. 두 번째 인자로 콘텐츠 타입을 넘겨줍니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티 파트 요청

파일을 멀티 파트로 전송하려면, 요청 전에 `attach` 메서드를 호출하세요. 이 메서드는 파일명과 내용, 필요시 파일명을 세 번째 인자로, 파일 관련 헤더를 네 번째 인자로 받을 수 있습니다:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 원본 콘텐츠 대신 스트림 리소스를 넘길 수도 있습니다:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

헤더는 `withHeaders` 메서드를 이용해 추가할 수 있습니다. `withHeaders`는 키/값 쌍의 배열을 인자로 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

응답의 콘텐츠 타입을 지정하려면 `accept` 메서드를 사용하세요:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

`acceptJson` 메서드를 사용해 응답을 `application/json`으로 받겠다는 의지를 빠르게 나타낼 수 있습니다:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders`는 기존 요청 헤더에 새 헤더를 병합합니다. 모든 헤더를 완전히 대체하려면 `replaceHeaders` 메서드를 사용하세요:

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

베이직과 다이제스트 인증은 각각 `withBasicAuth`, `withDigestAuth` 메서드로 지정 가능합니다:

```php
// 베이직 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

`Authorization` 헤더에 베어러 토큰을 추가하려면 `withToken` 메서드를 사용하세요:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드로 응답을 기다리는 제한 시간을(초 단위로) 지정할 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 이후 타임아웃됩니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 타임아웃을 초과하는 경우, `Illuminate\Http\Client\ConnectionException`이 발생합니다.

서버에 접속을 시도하는 최대 시간을 `connectTimeout` 메서드로 별도 지정할 수 있습니다:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트 또는 서버 오류가 발생할 경우, HTTP 클라이언트가 자동으로 요청을 재시도하게 하려면 `retry` 메서드를 사용할 수 있습니다. 첫 번째 인자는 최대 재시도 횟수, 두 번째 인자는 재시도 사이의 대기 시간(밀리초)입니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

재시도 사이의 대기 시간을 직접 산출하려면 두 번째 인자로 클로저를 전달하세요:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

첫 번째 인자에 배열을 전달하면 순서에 따라 재시도간 대기 시간을 설정할 수 있습니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

세 번째 인자로 콜러블을 지정하여 실제로 재시도를 수행할지 여부를 결정할 수 있습니다. 예를 들어, 초기 요청에서 `ConnectionException`일 때만 재시도하게 만들 수 있습니다:

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청 시도가 실패하면, 새 시도를 하기 전에 요청 객체를 수정할 수 있습니다. 예를 들어, 첫 시도가 인증 오류(401)로 실패했다면 새 인증 토큰으로 재시도할 수 있습니다:

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException`이 발생합니다. 이 동작을 끄려면 `throw` 인자에 `false` 값을 전달하세요. 비활성화하면 마지막으로 받은 응답이 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]  
> 연결 문제로 모든 요청이 실패한 경우에는 `throw` 옵션이 `false`여도 `Illuminate\Http\Client\ConnectionException`이 계속 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, Laravel HTTP 클라이언트 래퍼는 클라이언트/서버 오류(서버에서 400/500 수준 응답)를 예외로 던지지 않습니다. 이런 오류가 반환되었는지 `successful`, `clientError`, `serverError` 메서드로 확인할 수 있습니다:

```php
// 상태 코드가 200 이상 300 미만인지 확인
$response->successful();

// 상태 코드가 400 이상인지 확인
$response->failed();

// 400대 상태 코드인 경우 확인
$response->clientError();

// 500대 상태 코드인 경우 확인
$response->serverError();

// 클라이언트/서버 오류 시 즉시 콜백 실행
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 던지기

응답 상태 코드가 클라이언트/서버 오류일 때 `Illuminate\Http\Client\RequestException`을 발생시키고 싶으면 `throw` 또는 `throwIf` 메서드를 사용하세요:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 에러 발생 시 예외 발생
$response->throw();

// 에러 발생 및 조건이 참일 때 예외 발생
$response->throwIf($condition);

// 에러 발생 및 클로저가 참일 때 예외 발생
$response->throwIf(fn (Response $response) => true);

// 에러 발생 및 조건이 거짓일 때 예외 발생
$response->throwUnless($condition);

// 에러 발생 및 클로저가 거짓일 때 예외 발생
$response->throwUnless(fn (Response $response) => false);

// 특정 상태 코드를 가진 응답이면 예외 발생
$response->throwIfStatus(403);

// 특정 상태 코드가 아니면 예외 발생
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스는 반환된 응답을 확인할 수 있는 public `$response` 프로퍼티를 가집니다.

`throw` 메서드는 오류가 없을 경우 응답 인스턴스를 반환하므로, 이후 메서드 체이닝이 가능합니다:

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전 추가 로직을 수행하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저 실행 후 자동으로 예외가 발생하므로 클로저 내에서 재-throw하지 않아도 됩니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그 또는 리포팅 시 120자로 잘립니다. 예외 트렁케이션 길이를 조절하거나 비활성화하려면, `bootstrap/app.php`에서 `truncateRequestExceptionsAt`과 `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다:

```php
->withExceptions(function (Exceptions $exceptions) {
    // 예외 메시지 240자로 자르기
    $exceptions->truncateRequestExceptionsAt(240);

    // 예외 메시지 자르기 비활성화
    $exceptions->dontTruncateRequestExceptions();
})
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel HTTP 클라이언트는 Guzzle을 기반으로 하므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 요청/응답을 조작할 수 있습니다. 요청을 조작하려면 `withRequestMiddleware` 메서드로 Guzzle 미들웨어를 등록하세요:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 응답을 검사하려면 `withResponseMiddleware` 메서드로 미들웨어를 등록하세요:

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

모든 아웃바운드 요청 및 인바운드 응답에 적용되는 미들웨어를 등록하려면 `globalRequestMiddleware`와 `globalResponseMiddleware`를 사용하세요. 보통 이 메서드들은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

아웃바운드 요청에 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 추가하고 싶다면 `withOptions` 메서드를 사용하세요. 이 메서드는 키/값 쌍의 배열을 받습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션

모든 아웃바운드 요청의 기본 옵션을 지정하려면 `globalOptions` 메서드를 사용하세요. 주로 이 메서드는 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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
## 동시 요청

여러 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 일렬이 아니라 동시에 요청을 보냄으로써 느린 HTTP API 작업시 성능이 대폭 향상됩니다.

다행히 `pool` 메서드를 이용하면 손쉽게 이를 구현할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 인자로 받는 클로저를 파라미터로 받으며, 요청 풀에 여러 요청을 추가할 수 있습니다:

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

각 응답 인스턴스는 추가한 순서에 따라 인덱스로 접근할 수 있습니다. 요청에 이름을 붙이고 싶다면 `as` 메서드로 요청별 이름을 부여한 뒤 이름으로 응답에 접근할 수 있습니다:

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

`pool` 메서드는 `withHeaders`, `middleware`와 같은 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀에 추가되는 각 요청마다 옵션을 개별 설정해야 합니다:

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

Laravel HTTP 클라이언트는 "매크로" 정의를 지원합니다. 매크로는 다양한 서비스와 상호작용할 때 공통 경로나 헤더를 유창하게 커스텀할 수 있는 메커니즘입니다. 매크로 정의는 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 할 수 있습니다:

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

매크로를 구성하고 나면, 어디서든 해당 매크로를 호출해 지정 설정을 가진 요청을 손쉽게 생성할 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

많은 Laravel 서비스처럼, HTTP 클라이언트 역시 쉽고 표현적으로 테스트를 작성할 수 있도록 다양한 기능을 제공합니다. `Http` 파사드의 `fake` 메서드로 요청시 모의(더미) 응답을 반환하게 할 수 있습니다.

<a name="faking-responses"></a>
### 응답 페이크

예를 들어, 모든 요청에 대해 빈 `200` 상태 코드 응답을 반환하려면 다음과 같이 `fake` 메서드를 인자 없이 호출하면 됩니다:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 응답 페이크

또는 배열을 `fake` 메서드에 전달할 수 있습니다. 배열의 키는 페이크할 URL 패턴이며, 값은 반환할 응답입니다. `*` 문자를 와일드카드로 사용할 수 있습니다. 페이크하지 않은 URL에 보내는 요청은 실제로 전송됩니다. 페이크 응답은 `Http` 파사드의 `response` 메서드를 이용해 만들 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트 Mock JSON 응답...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // 구글 엔드포인트 Mock 문자열 응답...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

모든 일치하지 않는 URL의 기본값을 지정하려면 `*` 하나만 사용하세요:

```php
Http::fake([
    // GitHub 엔드포인트 Mock JSON 응답...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트 Mock 문자열 응답...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

간단한 문자열, JSON, 빈 응답을 반환할 때는 문자열, 배열, 정수만으로도 가능합니니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 연결 예외 페이크

HTTP 클라이언트가 요청 중 `Illuminate\Http\Client\ConnectionException`을 만나는 상황을 테스트하려면, `failedConnection` 메서드를 사용하세요:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 페이크

하나의 URL이 순서대로 여러 페이크 응답을 반환해야 하는 경우, `Http::sequence` 메서드로 시퀀스를 정의하세요:

```php
Http::fake([
    // GitHub 엔드포인트 Mock 시퀀스 응답...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

시퀀스의 모든 응답을 소진하면 이후 요청은 예외를 발생시킵니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용하세요:

```php
Http::fake([
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 없이 응답 시퀀스만 페이크할 경우 `Http::fakeSequence`를 사용합니다:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 페이크 콜백

엔드포인트별로 더 복잡한 로직이 필요하다면, 클로저를 `fake` 메서드에 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 인자로 받고, 적절한 응답 인스턴스를 반환해야 합니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="preventing-stray-requests"></a>
### 잘못된 요청 방지

테스트 중 HTTP 클라이언트를 통한 모든 요청이 페이크되는지 강제하고 싶다면 `preventStrayRequests`를 호출하세요. 이 후 페이크되지 않은 모든 요청은 예외를 발생시킵니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답 반환됨
Http::get('https://github.com/laravel/framework');

// 예외 발생
Http::get('https://laravel.com');
```

<a name="inspecting-requests"></a>
### 요청 검사

응답을 페이크할 때, 클라이언트가 올바른 데이터, 헤더로 요청을 보냈는지 검사하고 싶을 수 있습니다. `Http::fake` 호출 후 `Http::assertSent` 메서드를 사용하세요.

`assertSent`는 `Illuminate\Http\Client\Request` 인스턴스를 전달받는 클로저를 인자로 하며, 일치하면 true를 반환해야 합니다. 조건을 만족하는 요청이 1개 이상 있으면 테스트가 통과합니다:

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

특정 요청이 전송되지 않았는지 검증하려면 `assertNotSent`를 사용하세요:

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

`assertSentCount`로 테스트 중 "전송된" 요청 수를 검증할 수 있습니다:

```php
Http::fake();

Http::assertSentCount(5);
```

`assertNothingSent`로 아무 요청도 전송되지 않았는지 검증할 수 있습니다:

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드로 모든 요청과 그에 해당하는 응답들을 수집할 수 있습니다. 반환값은 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response`를 포함하는 배열의 컬렉션입니다:

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

또한, `recorded` 메서드에 클로저를 전달해, 원하는 조건에 맞는 요청/응답 쌍만 필터링할 수 있습니다:

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

Laravel은 HTTP 요청을 보내는 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청 전송 직전에, `ResponseReceived` 이벤트는 응답 수신 후, `ConnectionFailed` 이벤트는 응답을 받지 못했을 때 발생합니다.

`RequestSending` 및 `ConnectionFailed` 이벤트는 요청을 확인할 수 있는 public `$request` 프로퍼티를 가집니다. `ResponseReceived` 이벤트는 `$request`와 함께, 응답을 확인할 수 있는 `$response` 프로퍼티도 가집니다. 애플리케이션에서 이 이벤트들에 [이벤트 리스너](/docs/{{version}}/events)를 만들 수 있습니다:

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * Handle the given event.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```
