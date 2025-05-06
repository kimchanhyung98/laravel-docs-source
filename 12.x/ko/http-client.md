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
    - [의도하지 않은 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/) 위에 간결하고 표현적인 API를 제공하여, 다른 웹 애플리케이션과 통신하는 데 필요한 외부 HTTP 요청을 빠르게 만들 수 있도록 도와줍니다. Laravel의 Guzzle 래퍼는 가장 흔히 쓰이는 사용 사례에 중점을 두고 있으며, 개발자 경험에 초점을 맞추고 있습니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보내기 위해 `Http` 파사드가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL에 기본 `GET` 요청을 보내는 방법을 살펴봅시다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이 인스턴스는 다양한 응답 확인 메서드를 제공합니다:

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

또한, `Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스를 구현하기 때문에, JSON 응답 데이터를 배열처럼 바로 접근할 수 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```

위의 응답 메서드 외에도, 응답이 특정 상태 코드인지 확인할 수 있는 다음 메서드를 사용할 수 있습니다:

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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 사용하여 요청 URL을 만들 수 있도록 지원합니다. 템플릿에 확장될 URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용할 수 있습니다:

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

보내기 전 요청 인스턴스를 덤프(출력)하고 스크립트 실행을 중단하고 싶다면, 요청 정의 맨 앞에 `dd` 메소드를 추가하세요:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

`POST`, `PUT`, `PATCH` 요청을 보낼 때는 추가 데이터를 함께 전송하는 것이 일반적입니다. 이 메서드들은 두 번째 인수로 데이터 배열을 받으며, 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청 시, 쿼리 스트링을 직접 URL에 붙이거나, key/value 쌍의 배열을 `get` 메서드의 두 번째 인수로 전달할 수 있습니다:

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는 `withQueryParameters` 메서드를 사용할 수 있습니다:

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users')
```

<a name="sending-form-url-encoded-requests"></a>
#### Form URL Encoded 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내고 싶다면, 요청 전에 `asForm` 메서드를 호출하세요:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 바디 보내기

요청 시 raw 요청 바디를 직접 제공하려면 `withBody` 메서드를 사용하세요. 콘텐츠 타입은 두 번째 인수로 지정할 수 있습니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트 요청 형태로 보내려면, 요청 전에 `attach` 메서드를 사용하세요. 이 메서드는 파일 이름과 내용을 받으며, 필요하다면 세 번째 인수로 파일 이름을, 네 번째 인수로 파일 헤더를 지정할 수 있습니다:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 raw 내용을 전달하는 대신, 스트림 리소스를 전달할 수도 있습니다:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

헤더는 `withHeaders` 메서드로 추가할 수 있습니다. 이 메서드는 key/value 쌍의 배열을 인수로 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` 메서드로 요청에 대한 응답으로 기대하는 콘텐츠 타입을 지정할 수 있습니다:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

빠르게 `application/json` 콘텐츠 타입을 요청하려면 `acceptJson` 메서드를 사용할 수 있습니다:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 요청 헤더에 새로운 헤더를 병합합니다. 기존 헤더를 완전히 교체하고 싶다면 `replaceHeaders` 메서드를 사용하세요:

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

기본 인증(Basic Auth)과 다이제스트 인증(Digest Auth)은 각각 `withBasicAuth`, `withDigestAuth` 메서드로 지정할 수 있습니다:

```php
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

Bearer 토큰을 `Authorization` 헤더에 빠르게 추가하려면 `withToken` 메서드를 사용할 수 있습니다:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드는 응답 대기 최대 초(seconds)를 지정합니다. 기본적으로 HTTP 클라이언트는 요청 후 30초가 지나면 타임아웃됩니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정된 제한 시간을 초과하면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버로 연결을 시도할 때의 최대 대기 시간(초)은 `connectTimeout` 메서드로 지정할 수 있습니다. 기본값은 10초입니다:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트나 서버 오류 발생 시 HTTP 요청을 자동 재시도하려면 `retry` 메서드를 사용할 수 있습니다. 이 메서드는 시도할 최대 횟수와 각 시도 사이에 대기할 밀리초(ms) 시간을 인수로 받습니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

시도 사이의 대기 시간을 직접 계산하려면, 두 번째 인수로 클로저를 전달할 수 있습니다:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

또한, 첫 번째 인수에 배열을 넘길 수도 있습니다. 각 시도별 대기 시간을 배열로 지정하면 해당 순서대로 대기합니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면 `retry` 메서드의 세 번째 인수로 실제로 재시도를 할지 여부를 결정하는 콜러블을 지정할 수 있습니다. 예를 들어, 초기 요청에서 `ConnectionException`이 발생한 경우에만 재시도하고 싶을 때 사용합니다:

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

재시도 전 요청을 변경하고 싶다면, 세 번째 인수 콜러블 내에서 요청 인스턴스를 수정할 수 있습니다. 예를 들어, 인증 오류가 발생한 경우 새로운 토큰으로 재시도할 수 있습니다:

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

모든 요청이 실패했을 경우 `Illuminate\Http\Client\RequestException` 예외가 발생합니다. 이 동작을 비활성화하려면 `throw` 인수에 `false`를 전달하세요. 비활성화 시 마지막 응답이 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 연결 실패로 모든 요청이 실패할 경우, `throw`를 `false`로 설정해도 여전히 `Illuminate\Http\Client\ConnectionException`이 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, Laravel HTTP 클라이언트는 클라이언트/서버 오류(4xx, 5xx 응답)시 예외를 발생시키지 않습니다. `successful`, `clientError`, `serverError` 메서드로 이러한 오류가 반환되었는지 확인할 수 있습니다:

```php
// 상태 코드가 200 이상 300 미만인지 확인
$response->successful();

// 상태 코드가 400 이상인지 확인
$response->failed();

// 400대 상태 코드인지 확인
$response->clientError();

// 500대 상태 코드인지 확인
$response->serverError();

// 클라이언트 또는 서버 오류가 있을 때 콜백 실행
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생시키기

응답 인스턴스가 있고, 응답 코드가 클라이언트나 서버 오류일 경우 `Illuminate\Http\Client\RequestException`을 발생시키려면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트/서버 오류 시 예외 발생
$response->throw();

// 오류 및 지정 조건이 참일 때 예외 발생
$response->throwIf($condition);

// 오류 및 클로저 평가 결과가 참일 때 예외 발생
$response->throwIf(fn (Response $response) => true);

// 오류 및 지정 조건이 거짓일 때 예외 발생
$response->throwUnless($condition);

// 오류 및 클로저 평가 결과가 거짓일 때 예외 발생
$response->throwUnless(fn (Response $response) => false);

// 특정 상태 코드일 때 예외 발생
$response->throwIfStatus(403);

// 특정 상태 코드가 아닐 때 예외 발생
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 살펴볼 수 있는 public `$response` 속성이 있습니다.

오류가 없다면 `throw` 메서드는 응답 인스턴스를 그대로 반환하므로, `throw` 뒤에 체이닝하여 다른 메서드도 사용할 수 있습니다:

```php
return Http::post(/* ... */)->throw()->json();
```

예외 발생 전에 추가 로직을 실행하려면 `throw` 메서드에 클로저를 전달하면 됩니다. 이 클로저 실행 후 예외는 자동으로 발생하므로, 클로저 내에서 예외를 다시 던질 필요는 없습니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그나 리포트 시 120자까지만 잘려서 기록됩니다. 이 동작을 변경하거나 비활성화하려면 `bootstrap/app.php`에서 `truncateRequestExceptionsAt` 및 `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다:

```php
->withExceptions(function (Exceptions $exceptions) {
    // 예외 메시지를 240자로 제한
    $exceptions->truncateRequestExceptionsAt(240);

    // 예외 메시지 자르기 비활성화
    $exceptions->dontTruncateRequestExceptions();
})
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel HTTP 클라이언트는 Guzzle 기반이므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 요청/응답을 조작할 수 있습니다. 요청을 조작하고 싶으면 `withRequestMiddleware` 메서드로 미들웨어를 등록하세요:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 응답을 검사/조작하려면 `withResponseMiddleware` 메서드를 사용하세요:

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

모든 요청과 응답에 미들웨어를 적용하고 싶을 때는 `globalRequestMiddleware`, `globalResponseMiddleware` 메서드를 사용할 수 있습니다. 일반적으로 이들은 앱의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

추가 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)은 `withOptions` 메서드로 지정할 수 있습니다. 이 메서드는 key/value 배열을 인수로 받습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션

모든 요청에 기본적으로 옵션을 지정하려면 `globalOptions` 메서드를 사용합니다. 이 메서드도 보통 `AppServiceProvider`의 `boot`에서 호출합니다:

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

여러 개의 HTTP 요청을 동시에 보내고 싶은 경우가 있습니다. 즉, 요청이 순차적으로 처리되지 않고, 여러 요청이 한 번에 전송되는 방식입니다. 이는 느린 HTTP API와 통신 때 성능 향상에 도움이 될 수 있습니다.

이를 위해 `pool` 메서드를 사용할 수 있습니다. `pool` 메서드는 클로저를 받아, 그 내부에서 `Illuminate\Http\Client\Pool` 인스턴스에 여러 요청을 추가할 수 있습니다:

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

각 응답 인스턴스는 풀에 추가된 순서대로 접근 가능합니다. `as` 메서드로 요청별 이름을 지정하면, 해당 이름으로 응답에 접근할 수도 있습니다:

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
#### 동시 요청 커스터마이즈

`pool` 메서드는 `withHeaders`, `middleware` 등 기타 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀에 담긴 각 요청에 개별적으로 헤더 또는 미들웨어를 적용하려면, 각 요청에 직접 옵션을 지정하세요:

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

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있어, 서비스와 통신할 때 자주 쓰는 요청 경로나 헤더 설정을 유창하게 지정하는 메커니즘을 제공합니다. 매크로는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의합니다:

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

매크로를 설정한 후에는, 어디서든 지정된 설정으로 대기 중인 요청(pending request)을 생성할 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

Laravel의 많은 서비스는 테스트를 쉽고 유창하게 작성할 수 있는 기능을 제공합니다. HTTP 클라이언트 역시 마찬가지이며, `Http` 파사드의 `fake` 메서드는 HTTP 요청이 이루어졌을 때 스텁/더미 응답을 반환하도록 설정할 수 있습니다.

<a name="faking-responses"></a>
### 응답 페이크

예를 들어, 모든 요청에 대해 빈 200 상태 코드 응답을 반환하게 하려면, 별도의 인수 없이 `fake` 메서드를 호출하세요:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 페이크

배열을 `fake` 메서드에 넘겨, 배열의 키에 지정한 URL 패턴과 그에 대응되는 응답을 지정할 수 있습니다. `*` 문자는 와일드카드로 사용할 수 있습니다. 페이크되지 않은 URL로의 요청은 실제 요청이 이루어집니다. `Http` 파사드의 `response` 메서드로 가짜 응답을 만들 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트를 위한 JSON 응답 스텁
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트를 위한 문자열 응답 스텁
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

모든 대응되지 않은 URL에 대해 공통 응답을 지정하려면 단일 `*` 패턴을 사용하세요:

```php
Http::fake([
    // GitHub 엔드포인트의 JSON 응답 스텁
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 엔드포인트의 문자열 응답 스텁
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

간단한 문자열, JSON, 빈 응답은 문자열, 배열, 정수만 전달해도 자동으로 만들어집니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 페이크

HTTP 클라이언트가 요청 시 `Illuminate\Http\Client\ConnectionException`을 만나는 시나리오를 테스트하려면, `failedConnection` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException` 발생 시 동작을 테스트하려면 `failedRequest` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 페이크

단일 URL에서 여러 개의 가짜 응답을 순차적으로 반환하고 싶다면 `Http::sequence` 메서드를 활용하세요:

```php
Http::fake([
    // GitHub 엔드포인트의 연속 응답 스텁
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

시퀀스의 모든 응답이 소진되면, 추가 요청에서 예외가 발생합니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하려면 `whenEmpty`를 사용하세요:

```php
Http::fake([
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴 없이 응답 시퀀스를 사용할 때는 `Http::fakeSequence`를 사용할 수 있습니다:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 페이크 콜백

특정 엔드포인트에 반환할 응답을 좀 더 복잡하게 제어하려면, `fake` 메서드에 클로저를 전달하세요. 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받아 다양한 로직을 활용해 응답을 생성할 수 있습니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="preventing-stray-requests"></a>
### 의도하지 않은 요청 방지

테스트 개별 혹은 전체에서 HTTP 클라이언트를 통해 전송된 모든 요청이 페이크 처리되었는지 보장하려면 `preventStrayRequests` 메서드를 호출하세요. 이후 페이크되지 않은 요청은 실제로 실행되지 않고, 예외가 발생합니다:

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

응답을 페이크할 때, 보내진 요청을 확인하여 실제로 올바른 데이터와 헤더가 전송되는지 검증하고 싶을 수 있습니다. `Http::assertSent` 메서드를 이용하면, 최근에 페이크된 요청을 검사할 수 있습니다.

`assertSent`는 `Illuminate\Http\Client\Request` 인스턴스를 받아 부울 값을 리턴하는 클로저를 인수로 받습니다. 주어진 조건과 일치하는 요청이 있었다면 테스트가 통과합니다:

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

특정 요청이 보내지지 않았는지 검증하려면 `assertNotSent`를 사용할 수 있습니다:

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

테스트 중 "보내졌다"고 간주된 요청의 개수를 검증하려면 `assertSentCount`를 사용하세요:

```php
Http::fake();

Http::assertSentCount(5);
```

아무 요청도 없었는지 검증하려면 `assertNothingSent`를 사용할 수 있습니다:

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용하면, 모든 요청과 해당 응답을 모을 수 있습니다. 이 메서드는 `Illuminate\Http\Client\Request` 및 `Illuminate\Http\Client\Response` 인스턴스가 포함된 배열의 컬렉션을 반환합니다:

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

또한, `recorded`는 클로저를 인수로 받을 수 있는데, 이는 요청/응답 쌍에 대해 추가 필터링을 하고 싶을 때 쓸 수 있습니다:

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

Laravel은 HTTP 요청 처리 중 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청 전, `ResponseReceived` 이벤트는 응답을 받은 후, `ConnectionFailed` 이벤트는 응답을 받지 못했을 때 발생합니다.

`RequestSending`, `ConnectionFailed` 이벤트에는 요청 인스턴스를 확인할 수 있는 public `$request` 속성이 있습니다. `ResponseReceived` 이벤트에는 `$request`와 응답을 확인할 수 있는 `$response` 속성이 있습니다. 이 이벤트들에 [이벤트 리스너](/docs/{{version}}/events)를 생성할 수 있습니다:

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 주어진 이벤트를 처리합니다.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```
